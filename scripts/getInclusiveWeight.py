#!/usr/bin/env python
# -*- coding: utf-8 -*-

from array import array
import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import argparse
import os
import sys
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

def mse(ivec, central=0):
	nrms = rms(ivec) if central ==0 else central
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
			if(not "muR0p5_muF0p5" in leave.GetTitle() and not "muR2p0_muF2p0" in leave.GetTitle()):
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

def fill_histogram(unc, unctype):
	new_unc = {}
	from collections import OrderedDict
	for key, value in unc.iteritems():
		if "_inclusive" in key:
			continue
		if unctype in key:
			new_unc[key] = value
	new_histo = ROOT.TH1F(unctype, "", len(new_unc), 0, len(new_unc))
	i = 1
	for key, value in sorted(new_unc.iteritems()):
		new_histo.SetBinContent(i, value)
		new_histo.GetXaxis().SetBinLabel(i, key)
		i=i+1
	new_histo.Write()

def acceptance_to_tree(A, method, channel, category="inclusive"):
	name = "_".join([method, channel, category])
	acceptance_tree = ROOT.TTree(name, name)
	acceptance=array('d', [0])
	acceptance_tree.Branch('acceptance', acceptance, 'acceptance/D')
	for a in A.values():
		acceptance[0] = float(a)
		acceptance_tree.Fill()
	acceptance_tree.Write()

def save_as_histograms(unc, root_tree_file):
	alphas = fill_histogram(unc, "alphas")
	scale = fill_histogram(unc, "scale")
	pdf = fill_histogram(unc, "pdf")
	root_tree_file.Write()

def main():
	
	ROOT.gSystem.Load(os.path.expandvars("$CMSSW_BASE/src/Kappa/lib/libKappa"))
	
	parser = argparse.ArgumentParser(description="Determine the full weight of a sample for inclusive acceptance studies",
	                                 parents=[logger.loggingParser])

	parser.add_argument("-i", "--input-file", help="Input files.")
	parser.add_argument("--channels", default=["et", "mt", "tt", "em"], nargs="+", help="Channels. [Default: %(default)s]")
	parser.add_argument("--categories", default=["0jet_low", "0jet_high", "1jet_low", "1jet_high", "2jet_vbf"], nargs="+", help="Channels. [Default: %(default)s]")
	parser.add_argument("--process", help="Process Name [Default: %(default)s]")

	args = parser.parse_args()
	logger.initLogger(args)
	
	full_dict = {}
	categories = ["inclusive"] + args.categories

	#inclusive
	for channel in args.channels:
		full_dict[channel] = {}
		full_dict[channel]["full"] = count(args.input_file, "isZ"+channel+">0.5", "inclusive") # count total number of events
		weight_string = ""
		cutstrings = CutStringsDict.baseline(channel, "sm")
		del cutstrings["blind"]
		for cutstring in cutstrings.values():
			weight_string += "*" + cutstring
		full_dict[channel]["inclusive"] = count(args.input_file, weight_string, get_channel_string(channel))

	n_events_total = count(args.input_file, "1", "inclusive")["muR1p0_muF1p0_weight"]

	print "out of " + str(n_events_total) + " simulated events: " 
	for channel in args.channels:
		print "\t" + channel + ": " + str(full_dict[channel]["full"]["muR1p0_muF1p0_weight"] / n_events_total * 100) + "% of all events, \t selection efficincy is " + \
			str(full_dict[channel]["inclusive"]["muR1p0_muF1p0_weight"] / full_dict[channel]["full"]["muR1p0_muF1p0_weight"] * 100) + "% "

	# categories: apply eventWeight
	for channel in args.channels:
		for category in categories:
			lookup_string = "catHtt13TeV_"+channel+"_"+category
			weight_string = "(" + ExpressionsDict.static_get_expression(lookup_string) + ")"
			#weight_string += "*puWeight"
			# add baseline selection string
			cutstrings = CutStringsDict.baseline(channel, "sm")
			del cutstrings["blind"]
			for cutstring in cutstrings.values():
				weight_string += "*" + cutstring
			full_dict[channel][category] = count(args.input_file, weight_string, get_channel_string(channel))

	unc = {}
	eff = {}
	root_tree_file=ROOT.TFile("theory_uncertainties_" + args.process+".root","RECREATE")
	######## calculate inclusive weights
	# scale
	for channel in args.channels:
		A = {}
		for weight in [weight for weight in full_dict[channel]["full"] if "muR" in weight]:
			A[weight] = full_dict[channel]["inclusive"][weight] / full_dict[channel]["full"][weight]
		unc["scale_" + channel + "_inclusive"] = (max(A.values()) - min(A.values()))/2. / A["muR1p0_muF1p0_weight"]
		eff[channel] = A["muR1p0_muF1p0_weight"]
		acceptance_to_tree(A, "scale", channel)

	# PDF Sets
	for channel in args.channels:
		A = {}
		for weight in [weight for weight in full_dict[channel]["full"] if "NNPDF30_nlo_as_0118" in weight ]:
			A[weight] = full_dict[channel]["inclusive"][weight] / full_dict[channel]["full"][weight]
		unc["pdf_" + channel + "_inclusive"] =  mse(A.values(), A["NNPDF30_nlo_as_0118_00_weight"]) / A["NNPDF30_nlo_as_0118_00_weight"]
		acceptance_to_tree(A, "pdf", channel)

	#alpha_s
	for channel in args.channels:
		A = {}
		for weight in ['NNPDF30_nlo_as_0119_weight','NNPDF30_nlo_as_0118_00_weight','NNPDF30_nlo_as_0117_weight' ]:
			A[weight] = full_dict[channel]["inclusive"][weight] / full_dict[channel]["full"][weight]
		unc["alphas_" + channel + "_inclusive"] = (max(A.values()) - min(A.values()))/2. / A["NNPDF30_nlo_as_0118_00_weight"]
		acceptance_to_tree(A, "alphas", channel)

	categories = args.categories
	####### calculate category uncertainties
	# scale
	for channel in args.channels:
		for category in categories:
			A = {}
			for weight in [weight for weight in full_dict[channel][category] if "muR" in weight]:
				A[weight] = full_dict[channel][category][weight] / full_dict[channel]["inclusive"][weight]
			unc["scale_" + channel+"_"+category] = (max(A.values()) - min(A.values()))/2. / A["muR1p0_muF1p0_weight"]
			acceptance_to_tree(A, "scale", channel, category)
			eff[channel + '_' + category] = A["muR1p0_muF1p0_weight"]
	# PDF Sets
	for channel in args.channels:
		for category in categories:
			A = {}
			for weight in [weight for weight in full_dict[channel][category] if "NNPDF30_nlo_as_0118" in weight ]:
				A[weight] = full_dict[channel][category][weight] / full_dict[channel]["inclusive"][weight]
			unc["pdf_" + channel+"_"+category] = mse(A.values(), A["NNPDF30_nlo_as_0118_00_weight"]) / A["NNPDF30_nlo_as_0118_00_weight"]
			acceptance_to_tree(A, "pdf", channel, category)

	#alpha_s
	for channel in args.channels:
		for category in categories:
			A = {}
			for weight in ['NNPDF30_nlo_as_0119_weight','NNPDF30_nlo_as_0118_00_weight','NNPDF30_nlo_as_0117_weight' ]:
				A[weight] = full_dict[channel][category][weight] / full_dict[channel]["inclusive"][weight]
			unc["alphas_" + channel+"_"+category] = (max(A.values()) - min(A.values()))/2. / A["NNPDF30_nlo_as_0118_00_weight"]
			acceptance_to_tree(A, "alphas", channel, category)

	#fulldict_to_tree(full_dict)
	save_as_histograms(unc, root_tree_file)
	root_tree_file.Close()
	pprint.pprint(unc)
	print "efficiencies: "
	pprint.pprint(eff)


if __name__ == "__main__":
	main()

