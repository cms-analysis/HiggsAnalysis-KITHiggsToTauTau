#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)
import sys
import os
import argparse
import glob
import ROOT
import array
import matplotlib.pyplot as plt
import Artus.Utility.jsonTools as jsonTools
ROOT.PyConfig.IgnoreCommandLineOptions = True
  
if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Get information on overtraining.",
									 parents=[logger.loggingParser])
	#parser.add_argument("-i", "--input-files", nargs="+", required=True,
	#					help="input files")
	parser.add_argument("-o", "--output-name", default="same_as_score_name",
						help="output file pattern")
	parser.add_argument("-O", "--output-dir", default=".",
						help="output directory")
	parser.add_argument("-c", "--channel",
						default="mt",
						choices=["tt", "mt", "et", "em", "mm", "ee"],
						help="Channels. [Default: %(default)s]")
	parser.add_argument("-N", "--NTrees", type=int, nargs="+",
						default=[700, 1000, 1500, 2000, 3000],
						help="NTrees in BDT trainings. [Default: %(default)s]")
	parser.add_argument("-x", "--X", type=int, nargs="+",
						default=[1, 5, 13, 29],
						help="Xmasses in BDT trainings. [Default: %(default)s]")
	parser.add_argument("-s", "--score-name",
						default="M120_NTrees$N$_bbh_vs_ggh",
						help="Name of BDT variable (channel prefix is automatically added. Use '$N$' where NTrees should be inserted. [Default: %(default)s]")
	parser.add_argument("-ROC", "--plot-ROC-curves", default = False, action="store_true",
						help="plot ROC curves. [Default: %(default)s]")
	args = parser.parse_args()
	
	outputfolder = os.path.dirname(args.output_dir)
	if args.output_name == "same_as_score_name":
		outputname = args.score_name
	else:
		outputname = args.output_name
		print outputname
	if args.channel in ["ee", "em", "mm"]:
		ntuple_string = args.channel+"_jecUncNom/ntuple"
	else:
		ntuple_string = args.channel+"_jecUncNom_tauEsNom/ntuple"
	
	#filenames = glob.glob(os.path.join(args.input_folder, "*", "*.root"))
	#filenames = args.input_files
	
	Output = open(os.path.join(outputfolder, outputname.replace("$N$", "_N_").replace("$X$", "_X_") + ".txt"),"w")
	fig2 = plt.figure()
	ax2 = fig2.add_subplot(111, xlabel='number of trees', ylabel='integral over ROC curve', xlim=[1.1*min(args.NTrees)-0.1*max(args.NTrees),1.1*max(args.NTrees)-0.1*min(args.NTrees)])
	colors=["r", "b", "g", "y"]
	
	for iX, X in enumerate(args.X):
		keys = []
		for entry in args.NTrees:
		  	filename = args.channel + "_" + args.score_name.replace("$N$", str(entry)).replace("$X$", str(X))+"T1.root"
			if os.path.isfile(filename):
				keys.append(str(entry))
		TestLeafs = {}
		#Variance = {}
		ROCintegral = {}
		ROCintegralTrain = {}
		for key in keys:
			TestLeafs[key] = args.channel + "_" + args.score_name.replace("$N$", key).replace("$X$", str(X))
			ROCintegral[key] = 0.0
			ROCintegralTrain[key] = 0.0
		#Get ROC data
		for key in keys:
			#Variance[key] /= weightSums[key]
			#OvertrainingScore[key] /= weightSums[key]
			y1=[1.0]
			y2=[1.0]
			ymean=[1.0]
			y1T=[1.0]
			y2T=[1.0]
			ymeanT=[1.0]
			for i in range(1,3):
				f = ROOT.TFile.Open(TestLeafs[key]+"T%i.root"%(i))
				hist = f.Get("Method_BDT/BDT_"+TestLeafs[key]+"/MVA_BDT_"+TestLeafs[key]+"_rejBvsS")
				ROCintegral[key] += hist.Integral(1,100)/200.0
				hist2 = f.Get("Method_BDT/BDT_"+TestLeafs[key]+"/MVA_BDT_"+TestLeafs[key]+"_trainingRejBvsS")
				ROCintegralTrain[key] += hist2.Integral(1,100)/200.0
				
				#check ROC curves
				ROCcrossing = 0.0
				for j in range(1, hist.GetNbinsX()+1):
					if args.plot_ROC_curves:
						if i==1:
							y1.append(hist.GetBinContent(j))
							y1T.append(hist2.GetBinContent(j))
						else:
							y2.append(hist.GetBinContent(j))
							y2T.append(hist2.GetBinContent(j))
							ymean.append((y1[j]+y2[j])/2.0)
							ymeanT.append((y1T[j]+y2T[j])/2.0)
					if hist.GetBinContent(j)>hist2.GetBinContent(j):
						ROCcrossing += (hist.GetBinContent(j)-hist2.GetBinContent(j))/200.0
						#print "Warning: ROC(TestSample)>ROC(TrainingSample) at signal efficiency %f"%(j/100.0)
				if ROCcrossing > 0.001:
					print "Warning: Large area where ROC(TestSample)>ROC(TrainingSample) at NTrees " + key + "; area size = " + str(ROCcrossing)
				f.Close()
			if args.plot_ROC_curves:
				x_values=[0.0]
				for i in range(100):
					x_values.append((i+0.5)/100.0)
				x_values.append(1.0)
				y1.append(0.0)
				y2.append(0.0)
				ymean.append(0.0)
				y1T.append(0.0)
				y2T.append(0.0)
				ymeanT.append(0.0)
				
				fig = plt.figure()#xlabel='signal efficiency', ylabel='background rejection')
				ax = fig.add_subplot(111, xlabel='signal efficiency', ylabel='background rejection')
				ax.plot(x_values, y1T, color="b", linestyle='dotted', label='Training set 1')
				ax.plot(x_values, y2T, color="b", linestyle='dashed', label='Training set 2')
				ax.plot(x_values, ymeanT, color="b", linestyle='solid', label='Training mean')
				ax.plot(x_values, y1, color="r", linestyle='dotted', label='Test set 1')
				ax.plot(x_values, y2, color="r", linestyle='dashed', label='Test set 2')
				ax.plot(x_values, ymean, color="r", linestyle='solid', label='Test mean')
				ax.plot(0.18, 0.984, color="g", marker='o', ls='', label='btag categorization')
				ax.legend(loc='lower left', numpoints=1)
				fig.savefig(os.path.join(outputfolder, "ROC_%s.png"%(outputname.replace("$N$", key).replace("$X$", str(X)))))
				plt.close(fig)
			
		#write txt output	
		for key in keys:
			Output.write(key+" "+str(ROCintegralTrain[key])+" "+str(ROCintegral[key])+"\n")
		
		#plots
		y_values = []
		yT_values = []
		x_values = []
		for key in keys:
			y_values.append(ROCintegral[key])
			yT_values.append(ROCintegralTrain[key])
			x_values.append(int(key))
			
		
		ax2.plot(x_values, y_values, color=colors[iX], label='X%i Test set'%X, linestyle='None', marker='v')
		ax2.plot(x_values, yT_values, color=colors[iX], label='X%i Training set'%X, linestyle='None', marker='^')
		ax2.legend(loc='center right')
		
	Output.close()
	fig2.savefig(os.path.join(outputfolder, "%s.png"%outputname.replace("$N$", "_N_").replace("$X$", "_X_")))
