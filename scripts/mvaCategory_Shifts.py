#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import argparse
import copy
import os
import re
import Artus.Utility.jsonTools as jsonTools
import sys
import glob
import itertools
import ROOT
from string import strip
import matplotlib.pyplot as plt

def calculate_diff(filename, htt_name, sigma_value=0.68):
	tfile = ROOT.TFile(filename, "READ")
	ztt = tfile.Get("ztt")
	zll = tfile.Get("zll")
	wj = tfile.Get("wj")
	qcd = tfile.Get("qcd")
	vv = tfile.Get("vv")
	data = tfile.Get("data")
	ttj = tfile.Get("ttj")
	sig_hist = tfile.Get(htt_name)
	mc_hist = ROOT.TH1F("mc_events", "mc_events", 1000,0,2)
	#Probably add signal_only histogram at some point
	for hist in [ztt, zll, wj, qcd, vv, ttj]:
		mc_hist.Add(hist)
	mc_sum = 0
	data_sum = 0
	sig_sum = 0
	mc_tot = mc_hist.Integral()
	data_tot = data.Integral()
	sig_tot = sig_hist.Integral()
	data_point = False
	mc_point = False
	sig_point = False
	mc_value = 0
	data_value = 0
	sig_value = 0
	for j in range(1,1001,1):
		sig_sum += sig_hist.GetBinContent(j)
		mc_sum += mc_hist.GetBinContent(j)
		data_sum += data.GetBinContent(j)
		if (not mc_point) and (abs(mc_sum/mc_tot - sigma_value)<0.001 or mc_sum/mc_tot>sigma_value):
			mc_point = True
			lower = mc_hist.GetBinLowEdge(j)
			width = mc_hist.GetBinWidth(j)
			mc_value = lower+width
		if (not sig_point) and (abs(sig_sum/sig_tot - sigma_value)<0.001 or sig_sum/sig_tot>sigma_value):
			sig_point = True
			lower = sig_hist.GetBinLowEdge(j)
			width = sig_hist.GetBinWidth(j)
			sig_value = lower+width
			#break
		if (not data_point) and (abs(data_sum/data_tot - sigma_value)<0.001 or data_sum/data_tot>sigma_value):
			data_point = True
			lower = data.GetBinLowEdge(j)
			width = data.GetBinWidth(j)
			data_value = lower+width
	tfile.Close()
	del tfile
	return sig_value + abs(sig_value-mc_value) + abs(data_value-mc_value), mc_value, sig_value, data_value

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Collect and Combine Correlation Information",
									 parents=[logger.loggingParser])
	parser.add_argument("-i", "--input-file", required=True,
						help="File with categories (mt_minmax.txt)")
	parser.add_argument("-b", "--base-folder", required=True,
						help="Folder with subfolders containing sqrt_diff.root. Subfolder names must be identical to x_expression names in mt_minmax.txt")
	parser.add_argument("-m", "--higgs-mass", required=True,
						help="higgs mass")
	parser.add_argument("-c", "--channel", required=True,
						help="Channel")
	parser.add_argument("-o", "--output-file",
							default="Shifts.txt",
							help="Output file. [Default: %(default)s]")
	#parser.add_argument("--legend", default="upper left",
						#help="position of legend, use 'matplotlib position' as argument[Default:%(default)s]")
	#parser.add_argument("--lumi", type=float, default=2.301,
	                    #help="Luminosity for the given data in fb^(-1). [Default: %(default)s]")
	#parser.add_argument("-e", "--exclude-log", nargs="+",
						#default=[],
						#help="exclude training log files from collection. [Default: %(default)s]")
	#parser.add_argument("-c", "--combine-log", nargs="+",
						#default=["*_TrainingLog.json"],
						#help="include training log files into collectionm [Default: %(default)s]")
	args = parser.parse_args()
	logger.initLogger(args)
	Channel = args.channel
	#Extract cuts from minmax.txt
	base_cuts = {} #{reg_bdt: {sqrt_diff: Float, cuts: (c1,c2), vbfs:{vbf1:{cuts:(v1),sqrt_diff:Float} ,vbf2:{...}}, reg_bdt2...}
	vbf_taggers = []
	with open(args.input_file, "r") as exps:
		regular_name = ""
		for line in exps:
			vbf, name, values = map(strip, line.split(" : "))
			values = map(float, values.split(" "))
			values.pop(0)
			values.pop(-1)
			if vbf == "regular_name":
				if name not in base_cuts.keys():
					base_cuts[name]={"cuts":values, "vbfs":{}}
				else:
					base_cuts[name]["cuts"] = values
				regular_name= name
				continue
			elif vbf == "vbf_tagger":
				base_cuts[regular_name]["vbfs"][name]={"cuts":values}
				if name not in vbf_taggers:
					vbf_taggers.append(name)

	for bdt_name in base_cuts.iterkeys():
		diff_root = os.path.join(args.base_folder, bdt_name, "sqrt_diff.root")
		htt = "htt%s"%args.higgs_mass
		base_cuts[bdt_name]["sqrt_diff"], base_cuts[bdt_name]["mc_diff"], base_cuts[bdt_name]["sig_diff"], base_cuts[bdt_name]["data_diff"] = calculate_diff(diff_root, htt, 0.68)
	for bdt_name in vbf_taggers:
		diff_root = os.path.join(args.base_folder, bdt_name, "sqrt_diff.root")
		htt = "htt%s"%args.higgs_mass
		vbf_shift, vbf_mc, vbf_sig, vbf_data = calculate_diff(diff_root, htt, 0.68)
		for reg_bdt in base_cuts.iterkeys():
			try:
				base_cuts[reg_bdt]["vbfs"][bdt_name]["sqrt_diff"] = vbf_shift
				base_cuts[reg_bdt]["vbfs"][bdt_name]["sig_diff"] = vbf_sig
				base_cuts[reg_bdt]["vbfs"][bdt_name]["data_diff"] = vbf_data
				base_cuts[reg_bdt]["vbfs"][bdt_name]["mc_diff"] = vbf_mc

			except KeyError:
				continue
	full_path = os.path.expandvars(args.output_file)
	path, filename = os.path.split(full_path)
	jsonTools.JsonDict(base_cuts).save(os.path.join(path, "CombinedInfo.json"), indent=4)
	shifts_dict = {}
	for reg_bdt_name in base_cuts.iterkeys():
		bdt_name = "%s_%s"%(Channel, reg_bdt_name)
		lower = base_cuts[reg_bdt_name]["cuts"][0]
		upper = base_cuts[reg_bdt_name]["cuts"][1]
		for shift, value in [("up", -1*base_cuts[reg_bdt_name]["sqrt_diff"]), ("down", base_cuts[reg_bdt_name]["sqrt_diff"])]:
			shifts_dict["{reg_bdt}_signal_{shift}".format(reg_bdt=bdt_name, shift=shift)] = "({upper} <= {x_expression})".format(x_expression=reg_bdt_name, upper=upper+value)
			shifts_dict["{reg_bdt}_mixed_{shift}".format(reg_bdt=bdt_name, shift=shift)] = "({lower} <= {x_expression} && {x_expression} < {upper})".format(x_expression=reg_bdt_name, upper=upper+value, lower=lower+value)
			shifts_dict["{reg_bdt}_bkg_{shift}".format(reg_bdt=bdt_name, shift=shift)] = "({x_expression} < {lower})".format(x_expression=reg_bdt_name, lower=lower+value)

		for vbf_name in base_cuts[reg_bdt_name]["vbfs"].keys():
			vbf_cut = base_cuts[reg_bdt_name]["vbfs"][vbf_name]["cuts"][0]
			vbf_shifts_list = [
				("up", "up", -1*base_cuts[reg_bdt_name]["sqrt_diff"], -1*base_cuts[reg_bdt_name]["vbfs"][vbf_name]["sqrt_diff"]),
				("up", "nom", -1*base_cuts[reg_bdt_name]["sqrt_diff"], 0),
				("nom", "up", 0, -1*base_cuts[reg_bdt_name]["vbfs"][vbf_name]["sqrt_diff"]),
				("nom", "down", 0, base_cuts[reg_bdt_name]["vbfs"][vbf_name]["sqrt_diff"]),
				("down", "nom", base_cuts[reg_bdt_name]["sqrt_diff"], 0),
				("down", "down", base_cuts[reg_bdt_name]["sqrt_diff"], base_cuts[reg_bdt_name]["vbfs"][vbf_name]["sqrt_diff"]),
				]
			for reg_shift, vbf_shift, reg_value, vbf_value in vbf_shifts_list:
				shifts_dict["{ch}_{tag}_{reg_bdt}_tagged_signal_{reg_shift}_{vbf_shift}".format(ch=Channel, tag=vbf_name, reg_bdt=reg_bdt_name, reg_shift=reg_shift, vbf_shift=vbf_shift)] = "({upper}<={reg_bdt})*({vbf_cut}<={tag})".format(upper=upper+reg_value, vbf_cut=vbf_cut+vbf_value, reg_bdt=reg_bdt_name, tag=vbf_name)
				shifts_dict["{ch}_{tag}_{reg_bdt}_not_tagged_signal_{reg_shift}_{vbf_shift}".format(ch=Channel, tag=vbf_name, reg_bdt=reg_bdt_name, reg_shift=reg_shift, vbf_shift=vbf_shift)] = "({upper}<={reg_bdt})*({vbf_cut}>{tag})".format(upper=upper+reg_value, vbf_cut=vbf_cut+vbf_value, reg_bdt=reg_bdt_name, tag=vbf_name)
	jsonTools.JsonDict(shifts_dict).save(full_path, indent=4)