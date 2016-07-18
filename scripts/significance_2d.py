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
import numpy as np


if __name__ == "__main__":

	parser = argparse.ArgumentParser(description="Plot significance from combine output.", parents=[logger.loggingParser])

	parser.add_argument("-i","--input-dir", help="Input ROOT file")
	parser.add_argument("-m", "--mass", type=int, default=125, help="higgs mass")
	parser.add_argument("-o", "--output-file", default="significance_collection", help="output file")
	parser.add_argument("-c", "--channel", default="mt", help="Channel where categorization is varied")
	channels = ["et", "mt", "tt", "em"]
	args = parser.parse_args()
	logger.initLogger(args)
	fig = plt.figure()
	ax = fig.add_subplot(111)
	plots = []
	mass = args.mass

	# pfade sammeln, signifikanzen auslesen ( gesamt odr nur vbf )
	# in 2-dim array schreiben
	mjjs = range(200,801,200)
	mjj_width = (max(mjjs) - min(mjjs)) / (len(mjjs) -1)
	print mjj_width
	print mjjs
	print max(mjjs)
	print len(mjjs)
	jdetas = np.linspace(2.0, 5.0, 4)
	jdeta_width = (max(jdetas) - min(jdetas)) / (len(jdetas) -1)
	#out_file = ROOT.TFile(args.output_file, "recreate")
	#matrix = ROOT.TH2F("sig", "significances", len(mjjs), min(mjjs) - mjj_width/2, max(mjjs)+mjj_width/2, len(jdetas), min(jdetas)-jdeta_width/2, max(jdetas)+jdeta_width/2)
	matrix = [[0 for x in range(len(mjjs))] for y in range(len(jdetas))]
	for imjj, mjj in enumerate(mjjs, start=1):
		for ijdeta, jdeta in enumerate(jdetas, start=1):
			in_raw =os.path.join(args.input_dir, str(mjj)+"_"+str(jdeta), "datacards/combined", str(mass), "higgsCombineTest.ProfileLikelihood.mH125.*.root")
			print in_raw
			in_file = glob.glob( in_raw)[0] if len(glob.glob(in_raw)) == 1 else "invalid"
			if (not os.path.isfile(in_file)):
				continue

			current_chain = ROOT.TChain("chain_%i_%f"%(mjj, jdeta))
			current_chain.Add(in_file+"/limit", -1)
			for line in current_chain:
					print "line: " + str(line)
					y = line.limit
					print y
					#matrix.SetBinContent(imjj, ijdeta, y)
					matrix[imjj-1][ijdeta-1] = y
	print matrix

	# plotting
	import matplotlib.pyplot as plt
	import numpy as np
	npmatrix = np.matrix(matrix)
	fig = plt.figure(figsize = (4,4))
	ax = fig.add_subplot(1, 1, 1)
	im = plt.imshow(matrix, origin = "lower", cmap=plt.cm.Reds, interpolation="None", extent=[jdetas[0]-jdeta_width/2, jdetas[-1]+jdeta_width/2,mjjs[0]-mjj_width/2, mjjs[-1]+mjj_width/2])
	plt.yticks(mjjs)
	plt.xticks( jdetas)
	ax.set_aspect((jdetas[-1]-jdetas[0])/(mjjs[-1]-mjjs[0]))
	fig.colorbar(im, ax=ax)
	ax.set_ylabel("$m_{jj}$")
	ax.set_xlabel("$\Delta \eta$")
	plt.savefig(args.output_file)
