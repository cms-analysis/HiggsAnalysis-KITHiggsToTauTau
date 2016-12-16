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
	parser = argparse.ArgumentParser(description="Read bin contents from shapes for datacards.",
									 parents=[logger.loggingParser])
	parser.add_argument("-i", "--input-file", required=True,
						help="input file")
	parser.add_argument("-o", "--output-name", default="Datacard_bin_contents",
						help="name of output file (.txt will be added) [Default: %(default)s]")
	parser.add_argument("-c", "--channel", nargs="+",
						default=["mt"],
						choices=["tt", "mt", "et", "em", "mm", "ee"],
						help="Channels. [Default: %(default)s]")
	parser.add_argument("-C", "--categories", nargs="+",
						default=["btag", "nobtag"],
						help="NTrees in BDT trainings. [Default: %(default)s]")
	parser.add_argument("-p", "--processes", nargs="+",
						default=["ZTT", "ZLL", "TT", "VV", "W", "ggH", "bbH"], choices=["data_obs", "ZTT", "ZLL", "ZL", "ZJ", "TT", "TTT", "TTJ", "VV", "VVT", "VVJ", "W", "ggH", "bbH"],
						help="processes. [Default: %(default)s]")
	parser.add_argument("-m", "--masses", nargs="+",
						default=["120"],
						help="processes. [Default: %(default)s]")
	args = parser.parse_args()
	
	Output = open(args.output_name + ".txt","w")
	f = ROOT.TFile.Open(args.input_file)
	sigprocs=["ggH", "bbH"]
	bkgprocs=["ZTT", "ZLL", "TT", "VV", "W"]
	for channel in args.channel:
		for category in args.categories:
			Output.write("***********************\n"+channel+" "+category+"\n***********************\n")
			sighist={}
			for mass in args.masses:
				sighist[mass]=[0.0]
			bkghist=[0.0]
			sigflag=True
			bkgflag=True
			for process in args.processes:
				Output.write(process+":\n")
				if process in sigprocs:
					flag=True
					for mass in args.masses:
						hist = f.Get(channel+"_"+category+"/"+process+mass)
						print channel+"_"+category+"/"+process+mass
						nbins=hist.GetNbinsX()
						
						if flag:
							line="lower bin lim:\t"
							for i in range(1,nbins+1):
								line+="{0:9.4g}  ".format(hist.GetBinCenter(i)-hist.GetBinWidth(i)/2.0)
								if sigflag:
									for mass2 in args.masses:
										sighist[mass2].append(0.0)
							sigflag=False
							line+="{0:9.4g}  integral\n".format(hist.GetBinCenter(nbins)+hist.GetBinWidth(nbins)/2.0)
							Output.write(line)
							Output.write("bin content\n")
							flag=False
						
						line=" @ "+mass+" GeV:\t"
						for i in range(1,nbins+1):
							line+="{0:9.4g}  ".format(hist.GetBinContent(i))
							sighist[mass][i-1]+=hist.GetBinContent(i)
						line+="          {0:9.4g}\n".format(hist.Integral(1,nbins))
						sighist[mass][nbins]+=hist.Integral(1,nbins)
						Output.write(line)
				else:
					hist = f.Get(channel+"_"+category+"/"+process)
					print channel+"_"+category+"/"+process
					nbins=hist.GetNbinsX()
					
					line="lower bin lim:\t"
					for i in range(1,nbins+1):
						line+="{0:9.4g}  ".format(hist.GetBinCenter(i)-hist.GetBinWidth(i)/2.0)
						if bkgflag:
							bkghist.append(0.0)
					bkgflag=False
					line+="{0:9.4g}  integral\n".format(hist.GetBinCenter(nbins)+hist.GetBinWidth(nbins)/2.0)
					Output.write(line)
					
					line="bin content:\t"
					for i in range(1,nbins+1):
						line+="{0:9.4g}  ".format(hist.GetBinContent(i))
						bkghist[i-1]+=hist.GetBinContent(i)
					line+="          {0:9.4g}\n".format(hist.Integral(1,nbins))
					bkghist[nbins]+=hist.Integral(1,nbins)
					Output.write(line)
			
			Output.write("Signal:\n")
			Output.write("bin content\n")
			for mass in args.masses:
				line=" @ "+mass+" GeV:\t"
				for entry in sighist[mass]:
					line+="{0:9.4g}  ".format(entry)
				line+="\n"
				Output.write(line)
				
			Output.write("Background:\n")
			line="bin content:\t"
			for entry in bkghist:
				line+="{0:9.4g}  ".format(entry)
			line+="\n"
			Output.write(line)
			
			Output.write("S/Sqrt(B):\n")
			for mass in args.masses:
				line=" @ "+mass+" GeV:\t"
				for i in range(len(sighist[mass])):
					if bkghist[i]>0.0:
						line+="{0:9.4g}  ".format(sighist[mass][i]/(bkghist[i])**0.5)
					else:
						line+="  no bkg!"
				line+="\n"
				Output.write(line)
				
			Output.write("S/Sqrt(S+B):\n")
			for mass in args.masses:
				line=" @ "+mass+" GeV:\t"
				for i in range(len(sighist[mass])):
					if sighist[mass][i]+bkghist[i]>0.0:
						line+="{0:9.4g}  ".format(sighist[mass][i]/(sighist[mass][i]+bkghist[i])**0.5)
					else:
						line+="  no bkg!"
				line+="\n"
				Output.write(line)
			
	f.Close()
	Output.close()
	