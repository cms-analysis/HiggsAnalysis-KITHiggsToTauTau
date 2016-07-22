#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
#import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import argparse
import os, sys
import glob
import ROOT
import matplotlib.pyplot as plt
import numpy as np
import pprint

if __name__ == "__main__":

	parser = argparse.ArgumentParser(description="Plot significance from combine output.")

	parser.add_argument("-i","--input-dir", help="Input ROOT file")
	parser.add_argument("-m", "--mass", type=int, default=125, help="higgs mass")
	parser.add_argument("-o", "--output-file", default="significance_collection", help="output file")
	parser.add_argument("-c", "--channel", default="mt", help="Channel where categorization is varied")
	parser.add_argument("--x-label", default = "$\Delta$")
	parser.add_argument("--y-label", default = "jdeta")
	parser.add_argument("--folder", default = "datacards/combined")
	parser.add_argument("--x-type", default = "int")
	parser.add_argument("--y-type", default = "int")
	parser.add_argument("--x-range", default = "200,800,4")
	parser.add_argument("--y-range", default = "2.0,5.0,4")
	channels = ["et", "mt", "tt", "em"]
	args = parser.parse_args()
	print args
	#logger.initLogger(args)
	fig = plt.figure()
	ax = fig.add_subplot(111)
	plots = []
	mass = args.mass

	x_range = ([float(a) if "." in a else int(a) for a in args.x_range.split(",")])
	print x_range
	p1s = np.linspace(*x_range) if args.x_type == "float" else range(*x_range)
	p1_width = (max(p1s) - min(p1s)) / (len(p1s) -1)
	y_range = ([float(a) if "." in a else int(a) for a in args.y_range.split(",")])
	p2s = np.linspace(*y_range) if args.y_type == "float" else range(*y_range)
	p2_width = (max(p2s) - min(p2s)) / (len(p2s) -1)

	matrix = [[0 for x in range(len(p1s))] for y in range(len(p2s))]
	pprint.pprint(matrix)

	for ip1, p1 in enumerate(p1s, start=1):
		for ip2, p2 in enumerate(p2s, start=1):
			in_raw =os.path.join(args.input_dir, str(p1)+"_"+str(p2), args.folder, str(mass), "higgsCombineTest.ProfileLikelihood.mH125.*.root")
			print in_raw
			in_file = glob.glob( in_raw)[0] if len(glob.glob(in_raw)) == 1 else "invalid"
			if (not os.path.isfile(in_file)):
				continue
			current_chain = ROOT.TChain("chain_%i_%f"%(p1, p2))
			current_chain.Add(in_file+"/limit", -1)
			for line in current_chain:
					print "line: " + str(line)
					y = line.limit
					print y
					matrix[ip2-1][ip1-1] = y if y < 10 else 0
	pprint.pprint( matrix)

	# plotting
	import matplotlib.pyplot as plt
	import numpy as np
	npmatrix = np.matrix(matrix)
	fig = plt.figure(figsize = (4,4))
	ax = fig.add_subplot(1, 1, 1)
	min_value=np.min(npmatrix[np.nonzero(npmatrix)])
	im = plt.imshow(matrix, origin = "lower", cmap=plt.cm.Reds, interpolation="None", extent=[p1s[0]-p1_width/2, p1s[-1]+p1_width/2,p2s[0]-p2_width/2, p2s[-1]+p2_width/2], clim = (min_value,npmatrix.max()))
	plt.yticks(p2s)
	plt.xticks( p1s, rotation=70)
	
	ax.set_aspect(float((p1s[-1]-p1s[0]))/float((p2s[-1]-p2s[0])))
	fig.colorbar(im, ax=ax)
	labels = { "mjj" : "$m_{jj}$", "jdeta" : "$\Delta \eta_{jj}$", "hpt" : "$p_T^{H}$", "pt2" : "$p_T^2$"}
	ax.set_xlabel(labels[args.x_label])
	ax.set_ylabel(labels[args.y_label])
	plt.tight_layout()
	plt.savefig(args.output_file)
