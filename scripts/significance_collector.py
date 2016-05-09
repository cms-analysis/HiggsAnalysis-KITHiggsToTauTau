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

	parser = argparse.ArgumentParser(description="Plot significance from combine output.", parents=[logger.loggingParser])

	parser.add_argument("-i","--input-dirs", action="append", nargs = "+", help="Input ROOT file")
	parser.add_argument("-m", "--mass", type=int, default=125, help="higgs mass")
	parser.add_argument("-o", "--output_file", default="significance_collection", help="output file")
	parser.add_argument("-l", "--labels", nargs = "+", default=["limits"],
						help="labels for the legend, has to be specified as often as --input-dirs. [Default%(default)s]")
	parser.add_argument("-c", "--colors", nargs = "+", default=["blue"],
						help="colors for the legend and curves, has to be specified as often as --input-dirs. [Default%(default)s]")
	args = parser.parse_args()
	logger.initLogger(args)
	fig = plt.figure()
	ax = fig.add_subplot(111)
	x_names = []
	plots = []
	print args.input_dirs, args.labels, args.colors
	for (in_dirs, label, color) in zip(args.input_dirs, args.labels, args.colors):
		x_values = []
		y_values = []
		file_list = []
		map(file_list.__iadd__, map(glob.glob, [os.path.join(x, "datacards/combined/%i/*Combine*"%args.mass) for x in in_dirs]))
		print file_list
		file_list = [f for f in file_list if "ProfileLikelihood" in f]
		for i, (in_file, path)  in enumerate(zip(file_list, in_dirs)):
			print "counter " + str(i)
			if not ".root" in in_file:
				print "skipping " + in_file
				continue
			if not os.path.split(path)[1] in x_names:
				x_names.append(os.path.split(path)[1])
			current_chain = ROOT.TChain("chain_%i"%i)
			current_chain.Add(in_file+"/limit", -1)
			counter = 0
#			print "len current chain: " + str(len(current_chain))
			for line in current_chain:
					print "line: " + str(line)
					y = line.limit
			x_values.append(x_names.index(os.path.split(path)[1]))
			y_values.append(y)
		print x_values, y_values
		ax.errorbar(x_values, y_values, color=color, markersize = 12.5, ls = "None", markeredgewidth=2, label=label, marker = "x")

	ax.set_xticks([i for i in range(0,len(x_names)+1)])
	ax.set_xlim(-1, len(x_names)+1)
	#ax.set_xticklabels(x_names, rotation = 90, size='x-large', va='center', ha='right', rotation_mode='anchor')
	ax.set_xticklabels(range(2,21,1), rotation = 0, size='large')
	ax.set_ylabel("expected significance")
	ax.set_xlabel("projected luminosity / fb^-1")
	ax.legend(loc="best")
	plt.tight_layout()
	plt.savefig("%s.png"%args.output_file)
	log.info("create plot %s.png"%args.output_file)
	plt.savefig("%s.pdf"%args.output_file)
	log.info("create plot %s.pdf"%args.output_file)
	plt.savefig("%s.eps"%args.output_file)
	log.info("create plot %s.eps"%args.output_file)

