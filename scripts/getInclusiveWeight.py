#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import argparse
import os
import re
from datetime import datetime
import math
import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gErrorIgnoreLevel = ROOT.kError

import pprint
from Kappa.Skimming.registerDatasetHelper import *
from HiggsAnalysis.KITHiggsToTauTau.plotting.configs.expressions import ExpressionsDict
from HiggsAnalysis.KITHiggsToTauTau.plotting.configs.cutstrings import CutStringsDict


def rms(ivec):
	result = 0
	for entry in ivec:
		result += entry * entry
	result /= len(ivec)
	result = math.sqrt(result)
	return result

def mse(ivec):
	nrms = rms(ivec)
	return rms([ (value - nrms) for value in ivec])


def count(file_name, inclusive_weight, channel):
	root_file = ROOT.TFile(file_name, "READ")
	eventTree = ROOT.gDirectory.Get(channel + "/ntuple")
	n_entries = eventTree.GetEntries()
	list_of_leaves = eventTree.GetListOfLeaves()
	weight_names = []
	weights = {}
	for leave in list_of_leaves:
		if("NNPDF30" in leave.GetTitle() or "muR" in leave.GetTitle()):
	#	if("muR" in leave.GetTitle()):
			weight_names.append(str(leave.GetTitle()))
	for index in range(len(weight_names)):
		eventTree.Draw("1", weight_names[index] + "*" +  inclusive_weight)
		hist = ROOT.gPad.GetPrimitive("htemp") 
		weights[weight_names[index]] = hist.Integral()
	root_file.Close()
	return weights

def get_channel_string(ichannel):
	channel_strings = ["em_jecUncNom", "et_jecUncNom_tauEsNom", "mt_jecUncNom_tauEsNom", "tt_jecUncNom_tauEsNom"]
	for channel in channel_strings:
		if ichannel in channel:
			return channel

def main():
	
	ROOT.gSystem.Load(os.path.expandvars("$CMSSW_BASE/src/Kappa/lib/libKappa"))
	
	parser = argparse.ArgumentParser(description="Determine the full weight of a sample for inclusive acceptance studies",
	                                 parents=[logger.loggingParser])

	parser.add_argument("--full-file", help="Input files.")
	parser.add_argument("--inclusive-file", help="Input files.")
	parser.add_argument("--channels", default=["et", "mt", "tt", "em"], nargs="+", help="Channels. [Default: %(default)s]")
	parser.add_argument("--categories", default=["inclusive", "0jet_low", "0jet_high", "1jet_low", "1jet_high", "2jet_vbf"], nargs="+", help="Channels. [Default: %(default)s]")

	args = parser.parse_args()
	logger.initLogger(args)
	
	full_dict = {}


	#inclusive
	for channel in args.channels:
		full_dict[channel] = {}
		full_dict[channel]["full"] = count(args.full_file, "(1)", get_channel_string(channel))
		weight_string = ""
		cutstrings = CutStringsDict.baseline(channel, "sm")
		del cutstrings["blind"]
		for cutstring in cutstrings.values():
			weight_string += "*" + cutstring
		full_dict[channel]["fullinclusive"] = count(args.inclusive_file, weight_string, get_channel_string(channel))

	# categories: apply eventWeight
	for channel in args.channels:
		for category in args.categories:
			lookup_string = "catHtt13TeV_"+channel+"_"+category
			weight_string = "(" + ExpressionsDict.static_get_expression(lookup_string) + ")"
			weight_string += "*(eventWeight)"
			# add baseline selection string
			cutstrings = CutStringsDict.baseline(channel, "sm")
			del cutstrings["blind"]
			for cutstring in cutstrings.values():
				weight_string += "*" + cutstring
			full_dict[channel][category] = count(args.inclusive_file, weight_string, get_channel_string(channel))
			#print "channel:category:weight_string:count:" + channel + "," +category + "," + weight_string 
			#print str(full_dict[channel][category] )


	unc = {}
	######## calculate inclusive weights
	# scale
	for channel in args.channels:
		A = {}
		for weight in [weight for weight in full_dict[channel]["full"] if "muR" in weight]:
			A[weight] = full_dict[channel]["fullinclusive"][weight] / full_dict[channel]["full"][weight]
		unc["scale_" + channel + "_fullinclusive"] = (max(A.values()) - min(A.values()))/2. / A["muR1p0_muF1p0_weight"]

	# PDF Sets
	for channel in args.channels:
		A = {}
		for weight in [weight for weight in full_dict[channel]["full"] if "NNPDF30_nlo_as_0118" in weight ]:
			A[weight] = full_dict[channel]["fullinclusive"][weight] / full_dict[channel]["full"][weight]
#		print "rms: " + str(rms(A.values())) + ", mse: " + str(mse(A.values()))
		unc["pdf_" + channel + "_fullinclusive"] = mse(A.values()) / rms(A.values()) 

	#alpha_s
	for channel in args.channels:
		A = {}
		for weight in ['NNPDF30_nlo_as_0119_weight','NNPDF30_nlo_as_0118_00_weight','NNPDF30_nlo_as_0117_weight' ]:
			A[weight] = full_dict[channel]["fullinclusive"][weight] / full_dict[channel]["full"][weight]
		unc["alphas_" + channel + "_fullinclusive"] = (max(A.values()) - min(A.values()))/2. / A["NNPDF30_nlo_as_0118_00_weight"]

	####### calculate category uncertainties
	# scale
	for channel in args.channels:
		for category in args.categories:
			A = {}
			for weight in [weight for weight in full_dict[channel][category] if "muR" in weight]:
				A[weight] = full_dict[channel][category][weight] / full_dict[channel]["inclusive"][weight]
			unc["scale_" + channel+"_"+category] = (max(A.values()) - min(A.values()))/2. / A["muR1p0_muF1p0_weight"]
	# PDF Sets
	for channel in args.channels:
		for category in args.categories:
			A = {}
			for weight in [weight for weight in full_dict[channel][category] if "NNPDF30_nlo_as_0118" in weight ]:
				A[weight] = full_dict[channel][category][weight] / full_dict[channel]["inclusive"][weight]
				unc["pdf_" + channel+"_"+category] = mse(A.values()) / rms(A.values()) 

	#alpha_s
	for channel in args.channels:
		for category in args.categories:
			A = {}
			for weight in ['NNPDF30_nlo_as_0119_weight','NNPDF30_nlo_as_0118_00_weight','NNPDF30_nlo_as_0117_weight' ]:
				A[weight] = full_dict[channel][category][weight] / full_dict[channel]["inclusive"][weight]
			unc["alphas_" + channel+"_"+category] = (max(A.values()) - min(A.values()))/2. / A["NNPDF30_nlo_as_0118_00_weight"]
	pprint.pprint(unc)


if __name__ == "__main__":
	main()

