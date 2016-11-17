#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
The code is entended to calculate Theoretical uncertainties
by varying the pdf sets provided in the MC sample.

Htt and DY samples are supported, this was previously used
for Htt and Ztt channels.
'''
from array import array
import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import argparse
import os
import sys
import math
import ROOT
import pprint

ROOT.gROOT.SetBatch(True)
ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gErrorIgnoreLevel = ROOT.kError

from Kappa.Skimming.registerDatasetHelper import *
from HiggsAnalysis.KITHiggsToTauTau.plotting.configs.expressions import ExpressionsDict
from HiggsAnalysis.KITHiggsToTauTau.plotting.configs.cutstrings import CutStringsDict
from HiggsAnalysis.KITHiggsToTauTau.plotting.configs.samples_run2_2016 import Samples

def rms(ivec): return math.sqrt(sum(i*i for i in ivec) / len(ivec))

def mse(ivec, central = 0):
	if central == 0:
		return rms([ (value - rms(ivec)) for value in ivec])
	else:
		return rms([ (value - central) for value in ivec])

def count(file_name, pdfkeys, inclusive_weight, channel):
	if not isinstance(pdfkeys, list): pdfkeys = [pdfkeys]
	root_file = ROOT.TFile(file_name, "READ")
	eventTree = ROOT.gDirectory.Get(channel)
	n_entries = eventTree.GetEntries()
	list_of_leaves = eventTree.GetListOfLeaves()
	weight_names = []
	weights = {}

	for leave in list_of_leaves:
		if any(c == "_".join(leave.GetTitle().split("_")[:-2]) for c in pdfkeys) or "muR" in leave.GetTitle():
			if not any(c in leave.GetTitle() for c in ("muR0p5_muF0p5", "muR2p0_muF2p0")): 
				weight_names.append(str(leave.GetTitle()))

	c = ROOT.TCanvas()
	for name in weight_names:
		eventTree.Draw("1>>htemp(1,0,2)", name + "*" +  inclusive_weight)
		hist = ROOT.gPad.GetPrimitive("htemp") 
		'''
		if not "inclusive" in channel and index == 0: 
			print "count:", weight_names[index],  hist.Integral()
			hist.Print("All")
		if index == 0: c.SaveAs(weight_names[index] + ".png")
		'''
		weights[name] = hist.Integral()
	root_file.Close()

	return weights

def fill_histogram(unc, unctype):
	new_unc = {}
	print unctype, ":", unc
	for key, value in unc.iteritems():
		if "_inclusive" in key: continue
		elif unctype in key: 
			print key, ":", value
			new_unc[key] = value
	if len(new_unc) == 0 : return
	new_histo = ROOT.TH1F(unctype, "", len(new_unc), 0, len(new_unc))
	print new_unc
	print len(new_unc.iteritems())
	print sorted(new_unc.iteritems())
	for i, key  in zip(xrange(len(new_unc.iteritems())), sorted(new_unc.iteritems())):
		new_histo.SetBinContent(i + 1, new_unc.iteritems()[key])
		new_histo.GetXaxis().SetBinLabel(i + 1, key)

	new_histo.Write()

# print uncertainties
# numbers from https://twiki.cern.ch/twiki/bin/view/LHCPhysics/CERNYellowReportPageAt13TeV
residuals = { 	"ggH" : { "scale" : 0.081, "pdf" : 0.018 , "alphas" : 0.025 },
				"qqH" : { "scale" : 0.004, "pdf" : 0.021 , "alphas" : 0.005 },
				"WH" :  { "scale" : 0.007, "pdf" : 0.017 , "alphas" : 0.009 },
				"ZH" :  { "scale" : 0.038, "pdf" : 0.016 , "alphas" : 0.009 },
				"DY" : {"scale" : 0, "pdf" : 0, "alphas" : 0} 
				}

def print_uncertainty(unc, unctype, process):
	out_tuples = []
	for key, value in unc.iteritems():
		if "_inclusive" in key: continue
		elif unctype in key:
			category = key.replace(unctype + "_", "")
			out_tuple = ["13TeV"], [process], [category], 1 + value + residuals[process][unctype]
			out_tuples.append(out_tuple)
	return out_tuples

def acceptance_to_tree(A, method, channel, category = "inclusive"):
	name = "_".join([method, channel, category])
	print "acceptance_to_tree::name:", name 
	acceptance_tree = ROOT.TTree(name, name)
	acceptance = array('d', [0])
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
	HttSets = ["NNPDF30_nlo_as_0118", "NNPDF30_nlo_as_0117", "NNPDF30_nlo_as_0119", "CT10nlo", "CT10nlo_as_0117", "CT10nlo_as_0119", "MMHT2014nlo68clas118", "MMHT2014nlo_asmzsmallrange"]
	DYSets = ["NNPDF30_lo_as_0130", "NNPDF30_lo_as_0130_nf_4", "NNPDF30_lo_as_0118", "NNPDF23_lo_as_0130_qed", "NNPDF23_lo_as_0119_qed", "cteq6l1", "MMHT2014lo68cl", "MMHT2014lo_asmzsmallrange", "HERAPDF15LO_EIG", "NNPDF30_nlo_as_0118", "NNPDF23_nlo_as_0119", "CT10nlo", "MMHT2014nlo68cl"]

	parser = argparse.ArgumentParser(description="Determine the full weight of a sample for inclusive acceptance studies",
	                                 parents=[logger.loggingParser])
	parser.add_argument("-i", "--input-file", help="Input files.")
	parser.add_argument("--channels", default=["em", "et" ,"mt", "tt"], nargs="+", help="Channels. [Default: %(default)s]") # for the Z->ll : ["et", "mt", "tt", "em", "mm"]
	parser.add_argument("--categories", default=["0jet_low", "0jet_high", "1jet_low", "1jet_high", "2jet_vbf"], nargs="+", help="Channels. [Default: %(default)s]") # for Htt
	parser.add_argument("--process", default="", help="Process Name [Default: %(default)s]. Possible options: GluGlu, VBF, Wminus, Wplus, ZH, DY")
	parser.add_argument("--pdfkey", default="NNPDF30", help="PDF set  KEY Name [Default: %(default)s]")# Htt : NNPDF30
	parser.add_argument("--addpdfs", default=["NNPDF30_nlo_as_0119_weight", "NNPDF30_nlo_as_0117_weight"], help="PDF set Name [Default: %(default)s]")# NNPDF30_nlo_as_0119_weight NNPDF30_nlo_as_0118_00_weight NNPDF30_nlo_as_0117_weight
	parser.add_argument("--cut_type", default="baseline2016", help="Selection type [Default: %(default)s]")# By changes add: if "2016" in os.path.basename(input_file): cut_type = "baseline2016"

	args = parser.parse_args()
	logger.initLogger(args)
	channels = args.channels
	process = args.process
	input_file = args.input_file
	pdfkey = args.pdfkey
	addpdfs = args.addpdfs
	cut_type = args.cut_type
	if "2016" in os.path.basename(input_file): cut_type = "baseline2016"

	categoty_key = "catHtt13TeV_"
	if process == "":
		input_file_name = os.path.basename(input_file)
		if input_file_name == "output.root": input_file_name = "DY"
		print "input_file_name:", input_file_name
		sieve = {"GluGlu": "ggh", "VBF": "qqH", "Wminus": "WH", "Wplus": "WH", "ZH": "ZH" , "DY": "DY"}
		process = ''.join([sieve[proc] for proc in sieve.keys() if proc in input_file_name])
		if process == "DY": categoty_key = "catZtt13TeV_"
	print "process:", process

	categories = ["inclusive"] + args.categories
	pdfkeys = HttSets
	if process == "DY" and categories[1] == "0jet_low":# Better way?
		#channels.append("mm") # Better way? 
		print "CHANNEL mm OMMITED because of am error - need investigation"
		categories = ["inclusive", "2jet_inclusive", "1jet_inclusive", "0jet_inclusive"]
		pdfkey = "CT10nlo"
		addpdfs = ["NNPDF30_lo_as_0130_0_weight", "NNPDF30_lo_as_0130_nf_4_0_weight"]
		print "Automatic channels were assighned:", channels
		print "Automatic categories were assighned:", categories
		print "Automatic pdfkey is assighned:", pdfkey
		pdfkeys = [pdfkey]
		[pdfkeys.append( "_".join(c.split("_")[:-2])) for c in addpdfs]#pdfkeys = DYSets
	print "pdfkeys:", pdfkeys
		
	full_dict = {}
	n_events_total = count(input_file, pdfkeys, "1", Samples.root_file_folder("inclusive"))["muR1p0_muF1p0_weight"]
	print n_events_total

	print "Inclusive assighnment"
	for channel in channels:
		full_dict[channel] = {}
		full_dict[channel]["full"] = count(input_file, pdfkeys, "isZ" + channel + ">0.5", Samples.root_file_folder("inclusive")) #? isZ count total number of events by using inclusive pipeline
		weight_string = ""
		cutstrings = CutStringsDict.baseline(channel, cut_type)
		del cutstrings["blind"]
		for cutstring in cutstrings.values():
			weight_string += "*" + cutstring
		full_dict[channel]["inclusive"] = count(input_file, pdfkeys, weight_string[1:], Samples.root_file_folder(channel)) 

	print "Out of", n_events_total, "simulated events:" 
	for channel in channels:
		n_ev_passing_category_sel = full_dict[channel]["full"]["muR1p0_muF1p0_weight"]
		print "\t", channel, ": ",  n_ev_passing_category_sel / n_events_total * 100, "% of all events,",
		if n_ev_passing_category_sel == 0: 
			print "NAN, n_ev_passing_category_sel = 0 "  
		else: 
			print "\t selection efficincy is ", full_dict[channel]["inclusive"]["muR1p0_muF1p0_weight"], "/", n_ev_passing_category_sel , "=", full_dict[channel]["inclusive"]["muR1p0_muF1p0_weight"] / n_ev_passing_category_sel * 100, "% "
	
	print "Categories: apply eventWeight"
	print "\nCategories: apply eventWeight"
	for channel in channels:
		print "channel:", channel
		for category in categories:
			lookup_string = categoty_key + channel + "_" + category
			weight_string = "(" + ExpressionsDict.static_get_expression(lookup_string) + ")"
			cutstrings = CutStringsDict.baseline(channel, cut_type)
			del cutstrings["blind"]
			for cutstring in cutstrings.values():
				weight_string += "*" + cutstring
			if channel=="tt": print "\tweight_string", weight_string
			full_dict[channel][category] = count(input_file, pdfkeys, weight_string, Samples.root_file_folder(channel))

	unc = {}
	eff = {}
	root_tree_file=ROOT.TFile("theory_uncertainties_" + process + ".root", "RECREATE")
	print "######## calculate inclusive weights"
	print "\tscale"
	for channel in channels:
		A = {}
		for weight in [weight for weight in full_dict[channel]["full"] if "muR" in weight]:
			A[weight] = full_dict[channel]["inclusive"][weight] / full_dict[channel]["full"][weight]
		unc["scale_" + channel + "_inclusive"] = (max(A.values()) - min(A.values()))/2. / A["muR1p0_muF1p0_weight"]
		eff[channel] = A["muR1p0_muF1p0_weight"]
		acceptance_to_tree(A, "scale", channel)

	print "\tPDF Sets"
	for channel in channels:
		A = {}
		for weight in full_dict[channel]["full"]:
			if pdfkey in weight:
				A[weight] = full_dict[channel]["inclusive"][weight] / full_dict[channel]["full"][weight]
		unc["pdf_" + channel + "_inclusive"] =  mse(A.values(), A[pdfkey + "_0_weight"]) / A[pdfkey + "_0_weight"]
		acceptance_to_tree(A, "pdf", channel)

	print "\talpha_s"
	for channel in channels:
		A = {}
		for weight in [ addpdfs[0], pdfkey + "_0_weight", addpdfs[1] ]:
			A[weight] = full_dict[channel]["inclusive"][weight] / full_dict[channel]["full"][weight]
		unc["alphas_" + channel + "_inclusive"] = (max(A.values()) - min(A.values()))/2. / A[pdfkey + "_0_weight"]
		acceptance_to_tree(A, "alphas", channel)

	print "####### calculate category uncertainties"
	print "\tscale"
	for channel in channels:
		print "\t\t", channel
		for category in categories:
			print "\t\t\t", category
			A = {}
			for weight in full_dict[channel][category]:
				if "muR" in weight:
					A[weight] = full_dict[channel][category][weight] / full_dict[channel]["inclusive"][weight]
					print "\t\t\t\t", "A[",weight,"] = ", full_dict[channel][category][weight], "/", full_dict[channel]["inclusive"][weight], "=", A[weight]
			if A["muR1p0_muF1p0_weight"] == 0: 
				unc["scale_" + channel + "_" + category] = float('nan')
			else: 
				unc["scale_" + channel + "_" + category] = (max(A.values()) - min(A.values())) / 2. / A["muR1p0_muF1p0_weight"]
			print "\t\t\tscale uncertainty", max(A.values()), "-", min(A.values()), "...", unc["scale_" + channel + "_" + category]
			acceptance_to_tree(A, "scale", channel, category)
			eff[channel + '_' + category] = A["muR1p0_muF1p0_weight"]

	print "\tPDF Sets"
	for channel in channels:
		for category in categories:
			A = {}
			for weight in full_dict[channel][category]:
				if pdfkey in weight:
					A[weight] = full_dict[channel][category][weight] / full_dict[channel]["inclusive"][weight]
			if A[pdfkey + "_0_weight"] == 0: 
				unc["pdf_" + channel + "_" + category] = float('nan')
			else: 
				unc["pdf_" + channel + "_" + category] = mse(A.values(), A[pdfkey + "_0_weight"]) / A[pdfkey + "_0_weight"]
			acceptance_to_tree(A, "pdf", channel, category)

	print "\talpha_s"
	for channel in channels:
		for category in categories:
			A = {}
			for weight in [addpdfs[0], pdfkey + "_0_weight", addpdfs[1] ]:
				A[weight] = full_dict[channel][category][weight] / full_dict[channel]["inclusive"][weight]
			if A[pdfkey + "_0_weight"] == 0: 
				unc["alphas_" + channel + "_" + category] = float('nan')
			else: 
				unc["alphas_" + channel + "_" + category] = (max(A.values()) - min(A.values()))/2. / A[pdfkey + "_0_weight"]
			acceptance_to_tree(A, "alphas", channel, category)

	print "uncertainties: "
	save_as_histograms(unc, root_tree_file)
	root_tree_file.Close()
	pprint.pprint(unc)

	print "efficiencies: "
	pprint.pprint(eff)

	print "qcd scale uncertainties: "
	scale_tuples = print_uncertainty(unc, "scale", process)
	for s_tuple in scale_tuples:
		pprint.pprint(s_tuple)

	print "PDF scale uncertainites: "
	pdf_tuples = print_uncertainty(unc, "pdf", process)
	for pdf_tuple in pdf_tuples:
		pprint.pprint(pdf_tuple)


if __name__ == "__main__":
	main()

