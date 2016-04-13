#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import argparse
import os
import glob
import ROOT
import matplotlib.pyplot as plt

if __name__ == "__main__":

	parser = argparse.ArgumentParser(description="Print contents of trees.", parents=[logger.loggingParser])

	parser.add_argument("-i","--input-dirs", nargs = "+", help="Input ROOT file")
	parser.add_argument("-m", "--mass", type=int, default=125, help="higgs mass")
	parser.add_argument("-o", "--output_file", default="limit_collection", help="output file")


	x_names = []
	x_values = []
	y_mid = []
	y_down = []
	y_up = []
	args = parser.parse_args()
	logger.initLogger(args)
	file_list = []
	map(file_list.__iadd__, map(glob.glob, [os.path.join(x, "datacards/combined/%i/*Combine*"%args.mass) for x in args.input_dirs]))
	for i, (in_file, path)  in enumerate(zip(file_list, args.input_dirs)):
		if not ".root" in in_file:
			continue
		x_names.append(os.path.split(path)[1])
		current_chain = ROOT.TChain("chain_%i"%i)
		current_chain.Add(in_file+"/limit", -1)
		counter = 0
		up = 0
		mid = 0
		down = 0
		for line in current_chain:
			if counter == 1:
				down = line.limit
			elif counter == 2:
				mid = line.limit
			elif counter == 3:
				up = line.limit
				break
			counter += 1
		x_values.append(i)
		y_mid.append(mid)
		y_up.append(up-mid)
		y_down.append(mid-down)

	fig = plt.figure()
	ax = fig.add_subplot(111)
	ax.errorbar(x_values, y_mid, yerr=[y_down, y_up], color="blue", markersize = 12.5, ls = "None", markeredgewidth=2)
	ax.set_xticks(x_values)
	ax.set_xlim(-1, len(x_values))
	ax.set_xticklabels(x_names, rotation = 90, size='x-large', va='center', ha='right', rotation_mode='anchor')
	ax.set_ylabel("Limit$")
	plt.tight_layout()
	plt.savefig("%s.png"%args.output_file)
	log.info("create plot %s.png"%args.output_file)
	plt.savefig("%s.pdf"%args.output_file)
	log.info("create plot %s.pdf"%args.output_file)
	plt.savefig("%s.eps"%args.output_file)
	log.info("create plot %s.eps"%args.output_file)

