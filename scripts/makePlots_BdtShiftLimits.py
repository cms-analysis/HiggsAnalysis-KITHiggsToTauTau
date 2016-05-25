#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import argparse
import os
import glob
import ROOT
import Artus.Utility.jsonTools as jsonTools
import numpy as np
import matplotlib.pyplot as plt

def get_limit(root_file, file_type="asymptotic"):
	if root_file is None:
		return (0,0,0)
	chain = ROOT.TChain(root_file)
	chain.Add(root_file+"/limit", -1)
	up = 0
	mid = 0
	down = 0
	counter = 0
	if file_type == "asymptotic":
		for line in chain:
			if counter == 1:
				down = line.limit
			elif counter == 2:
				mid = line.limit
			elif counter == 3:
				up = line.limit
				break
			counter += 1
	elif file_type == "multidim":
		for line in chain:
			if counter == 0:
				mid = line.r
			elif counter == 1:
				down = line.r
			elif counter == 2:
				up = line.r
				break
			counter += 1
	#print down, mid, up
	return (down,mid,up)

if __name__ == "__main__":

	parser = argparse.ArgumentParser(description="Print contents of trees.", parents=[logger.loggingParser])

	parser.add_argument("-i","--input-dirs",action="append", nargs = "+", help="Input ROOT file")
	parser.add_argument("-d","--diff-dirs", action="append", nargs="+", default = [],help="Diff Dirs, calculate and plot difference between input dirs and diff-dirs")
	#parser.add_argument("--unc-files", nargs = "+",default=[], action="append", help="BDT uncertainty files")

	parser.add_argument("-l", "--labels", nargs = "+", default=["limits"],
						help="labels for the legend, has to be specified as often as --input-dirs. [Default%(default)s]")
	parser.add_argument("-c", "--colors", nargs = "+", default=["blue"],
						help="colors for the legend and curves, has to be specified as often as --input-dirs. [Default%(default)s]")
	parser.add_argument("--limits-type", default="asymptotic", choices=["asymptotic", "multidim"],
						help="use one of the following limit types: [Default:%(default)s, choices:%(choices)s]")
	parser.add_argument("--base-line", default=None,
						help="use the limit extracted from this workspace as baseline for the others: other-this")
	parser.add_argument("--channel", default="mt",
						help="channels. [Default%(default)s]")
	parser.add_argument("-m", "--mass", type=int, default=125, help="higgs mass")
	parser.add_argument("-o", "--output_file", default="limit_collection", help="output file")

	args = parser.parse_args()
	logger.initLogger(args)
	fig = plt.figure()
	ax = fig.add_subplot(111)
	x_names = []
	categories_names = []
	values_list = []
	calculate_diff = True
	uncertainties = True
	if args.base_line:
		base_line = get_limit(args.base_line, args.limits_type)[1]
	else:
		base_line = 0

	if args.diff_dirs == []:
		args.diff_dirs = [[]]*len(args.input_dirs)
		calculate_diff = False
	elif len(args.diff_dirs) is not len(args.input_dirs):
		args.diff_dirs = args.diff_dirs * len(args.input_dirs)
	if len(args.diff_dirs[0]) is not len (args.input_dirs[0]):
		args.diff_dirs = [[]]*len(args.input_dirs)
		calculate_diff = False

	search_pattern = "{mass}/*Combine*Asymp*".format(mass=args.mass)
	if args.limits_type == "multidim":
		search_pattern = "{mass}/*Combine*MultiDim*".format(mass=args.mass)
	#print args.input_dirs, args.labels, args.colors, args.diff_dirs, args.unc_files
	for (in_dirs, label, color, diff_dirs) in zip(args.input_dirs, args.labels, args.colors, args.diff_dirs):
		values = {}
		file_list = []
		diff_list = []
		map(file_list.__iadd__, map(glob.glob, [os.path.join(x, "datacards/combined/"+search_pattern) for x in in_dirs]))
		map(diff_list.__iadd__, map(glob.glob, [os.path.join(x, "datacards/combined/"+search_pattern) for x in diff_dirs]))
		if len(diff_list) != len(file_list) and len(diff_list) == 0:
			diff_list = [None]*len(file_list)
		for i, (in_file, diff_file, path)  in enumerate(zip(file_list, diff_list, in_dirs)):
			if not ".root" in in_file:
				continue
			name = os.path.split(path)[1]
			if not name in x_names:
				x_names.append(os.path.split(path)[1])
			values[name]={"categories":{}}
			values[name]["combined_diff"] = get_limit(diff_file, args.limits_type)
			values[name]["combined"] = get_limit(in_file, args.limits_type)
			values[name]["x_val"] = x_names.index(name)
			d = os.path.join(path, "datacards/individual/")
			categories = [os.path.join(d,o) for o in os.listdir(d) if os.path.isdir(os.path.join(d,o))]
			category_files = []
			map(category_files.__iadd__, map(glob.glob, [os.path.join(x, search_pattern) for x in categories]))
			for cat, cat_path in zip(category_files, categories):
				cat_name = os.path.split(cat_path)[1]
				if not args.channel in cat_name:
					continue
				split_name = cat_name.replace("%s_"%args.channel,"")
				for repl in name.split("_"):
					split_name = split_name.replace(repl+"_", "")
				if split_name not in categories_names:
					categories_names.append(split_name)
				if split_name not in values[name]["categories"].keys():
					values[name]["categories"][split_name] = {}
				values[name]["categories"][split_name]["value"] = get_limit(cat, args.limits_type)
		values_list.append(values)
		#print values
		x_values = np.array([values[name]["x_val"] for name in x_names])
		lower = np.array([values[name]["combined"][0]-values[name]["combined_diff"][0] for name in x_names])
		upper = np.array([values[name]["combined"][2]-values[name]["combined_diff"][2] for name in x_names])
		y_values = upper - lower
		un_value = []
		for i,cat in enumerate(categories_names):
			if i == 0:
				unc_value = np.array([values[name]["categories"][cat]["unc"] for name in x_names])**2
			unc_value += np.array([values[name]["categories"][cat]["unc"] for name in x_names])**2
		unc_value = unc_value**0.5
		if args.limits_type == "asymptotic":
			y_values = np.array([values[name]["combined"][1]-values[name]["combined_diff"][1] for name in x_names])
		ax.errorbar(x_values,y_values, yerr= [y_values-lower, upper-y_values], marker="x", label=label, color = color, markersize = 12.5, ls = "None", markeredgewidth=2)

		#if args.limits_type == "asymptotic":

		#elif args.limits_type == "multidim":


	#print values_list

		#abs_value = np.array([values[name]["combined"][1] for name in x_names])
		#x_list = [values[name]["x_val"] for name in x_names]
		##lim_value = abs_value-np.average(abs_value)
		##diff_value = np.array([values[name]["combined_diff"][1] for name in x_names])
		#lim_value = abs_value - base_line
		#quad_diff = np.sum(lim_value*lim_value)
		#unc_value = []
		#print x_names
		#jsonTools.JsonDict(values).save("Test.json", indent=4)
		#print unc_value
		#unc_value = unc_value**0.5




















		#ax.plot(unc_value,lim_value, marker="x", label=label, color = color, markersize = 12.5, ls = "None", markeredgewidth=2)
		##ax.plot(np.array([values[name]["x_val"] for name in x_names]),lim_value, marker="x", label=label, markersize = 12.5, ls = "None", markeredgewidth=2)
			##ax.plot(unc_value, lim_value, marker="x", label=label+" diff: %1.5f"%quad_diff, markersize = 12.5, ls = "None", markeredgewidth=2)
		##if calculate_diff:
			##diff_value = np.array([values[name]["combined_diff"][1] for name in x_names])
			##lim_value = (abs_value - diff_value)
		##tagger_unc_value = []
		##reg_unc_value = []
		##unc_value = unc_value**0.5
		##mean = lim_value/unc_value
		##lim_value =(lim_value - mean)/mean
		##ax.errorbar(x_values, y_mid, yerr=[y_down, y_up], color=color, markersize = 12.5, ls = "None", markeredgewidth=2, label=label, marker = "x")




	##if not args.bdt_uncertainties:
		##ax.set_xticks([i for i in range(0,len(x_names))])
		##ax.set_xlim(-0.5, len(x_names)+0.2*len(x_names))
		##x_names = [name.replace("ggh_xxh", "reg").replace("_all", "").replace("qqh", "vbf") for name in x_names]
		##ax.set_xticklabels(x_names, rotation = 90, size='x-large', va='center', ha='right', rotation_mode='anchor')
		##ax.set_ylabel("Limit")
		##if calculate_diff:
	#ax.set_ylabel("$\\Delta$Limits")
	lgd = ax.legend(bbox_to_anchor=(1, 1), loc=2, borderaxespad=0.)
	##else:
		##os.path.exists(args.bdt_uncertainties)
		##unc_dict = jsonTools.JsonDict(args.bdt_uncertainties)
		##mean = np.mean(values["y_mid"])
		##values["y_mid"]=np.array(values["y_mid"])-mean




	##plt.tight_layout()
	plt.savefig("%s.png"%args.output_file, bbox_extra_artists=(lgd,), bbox_inches='tight')
	log.info("create plot %s.png"%args.output_file)
	##plt.savefig("%s.pdf"%args.output_file)
	##log.info("create plot %s.pdf"%args.output_file)
	##plt.savefig("%s.eps"%args.output_file)
	##log.info("create plot %s.eps"%args.output_file)

