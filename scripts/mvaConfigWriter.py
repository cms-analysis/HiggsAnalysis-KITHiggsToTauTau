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

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Collect and Combine Correlation Information",
									 parents=[logger.loggingParser])
	parser.add_argument("-i", "--input-dir", required=True, nargs='+',
						help="Input directory. Use output directory of tmvaWrapper.py")
	parser.add_argument("-o", "--output-dir",
						default=None,
						help="Output file. None defaults to location of first Input [Default: %(default)s]")
	parser.add_argument("-e", "--exclude-log", nargs="+",
						default=[],
						help="exclude training log files from collection. [Default: %(default)s]")
	parser.add_argument("-c", "--combine-log", nargs="+",
						default=["*_TrainingLog.json"],
						help="include training log files into collectionm [Default: %(default)s]")
	args = parser.parse_args()
	logger.initLogger(args)

	log_file_list = []
	log_exclude_list = []
	if args.output_dir == None:
		out_dir = args.input_dir[0]
	else:
		out_dir = args.output_dir
	for in_dir in args.input_dir:
		map(log_file_list.__iadd__, map(glob.glob, [os.path.join(in_dir, l) for l in args.combine_log]))
		map(log_exclude_list.__iadd__, map(glob.glob, [os.path.join(in_dir, l) for l in args.exclude_log]))
	for ex_log in log_exclude_list:
		if ex_log in log_file_list:
			log_file_list.pop(log_file_list.index(ex_log))
	settings_info = {
    "MVATestMethodsInputQuantities" : [
	],
    "MVATestMethodsMethods" : [

    ],
    "MVATestMethodsNames" : [

    ],
	"MVATestMethodsNFolds" : [

    ],
    "MVATestMethodsWeights" : [
	]
	}
	settings_quantities = {"property":[]}
	quantities_index = -1
	full_path = lambda s: os.path.realpath(s)
	for log_file in log_file_list:
		c_log = jsonTools.JsonDict(log_file)
		quantities = c_log["variables"]
		weight_path, dump = os.path.split(log_file)
		n_fold = c_log["N-Fold"]
		training_name = c_log["training_name"]
		methods = c_log["methods"]

		if ("%i;"%quantities_index + quantities) not in settings_info["MVATestMethodsInputQuantities"]:
			quantities_index += 1
			settings_info["MVATestMethodsInputQuantities"].append("%i;"%quantities_index + quantities)


		settings_info["MVATestMethodsNames"].append(training_name)
		settings_info["MVATestMethodsNFolds"].append(n_fold)
		for method in methods:
			method = method.split(";")[0]
			settings_quantities["property"].append(training_name)
			if n_fold == 1:
				settings_info["MVATestMethodsMethods"].append("%i;%s"%(quantities_index, method))
				settings_info["MVATestMethodsWeights"].append(full_path(weight_path+"/T%i_%s_%s.weights.xml"%(1,method,training_name)))
			else:
				for i in range(1,n_fold+1):
					settings_info["MVATestMethodsMethods"].append("%i;%s"%(quantities_index, method))
					settings_info["MVATestMethodsWeights"].append(full_path(weight_path+"/T%i_%s_%s.weights.xml"%(i,method,training_name)))
					settings_quantities["property"].append("T%i%s"%(i, training_name))
	jsonTools.JsonDict(settings_info).save(os.path.join(out_dir, "settingsMVATestMethods.json"), indent = 4)
	jsonTools.JsonDict(settings_quantities).save(os.path.join(out_dir, "MVATestMethodsQuantities.json"), indent = 4)

	#with open(os.path.join(out_dir, "mvadatacardsconfigs.json"), "w") as logfile:
		##logfile.write("\ncopy to $CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/python/datacards/mvadatacardsconfigs.py\n")
		#out_lines = []
		#for i,name in enumerate(settings_info["MVATestMethodsNames"]):
			#out_lines.append("%s_up\n"%(name))
			#out_lines.append("%s_down\n"%(name))
			#out_lines.append("%s_mid\n"%(name))
		#out_lines[-1]=out_lines[-1].replace(",", "")
		#for chan in ["mt", "et", "em", "tt"]:
			#logfile.write("%s\n"%chan)
			#for line in out_lines:
				#logfile.write("\t%s_"%chan+line)
			##logfile.write("\t\t\t},\n")
	with open(os.path.join(out_dir, "mvadatacards.cfg"), "w") as logfile:
		out_lines=[]
		for name in settings_info["MVATestMethodsNames"]:
			out_lines.append("%s_up\n"%name)
			out_lines.append("%s_down\n"%name)
			out_lines.append("%s_mid\n"%name)
		#logfile.write("\ncopy to $CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/python/datacards/mvadatacards.py\n")
		#logfile.write("categs = [\n")
		logfile.write("".join(out_lines))
	with open(os.path.join(out_dir, "expressions.cfg"), "w") as logfile:
		#logfile.write("\ncopy to $CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/python/plotting/configs/expressions.py\n")
		for cat in settings_info["MVATestMethodsNames"]:
			logfile.write("mva_{0}_%s_up\t(0.5 <= %s)\n"%(cat,cat))
			logfile.write("mva_{0}_%s_down\t(%s < -0.5)\n"%(cat,cat))
			logfile.write("mva_{0}_%s_mid\t(-0.5 <= %s && %s < 0.5)\n"%(cat,cat,cat))
		#logfile.write("\ncopy to .sh script and execute/source line by line\n")

	with open(os.path.join(out_dir, "plot_commands.sh"), "w") as logfile:
		logfile.write("#!/bin/bash\n")
		logfile.write("#Adjust these export commands to meet your directory settings\n")
		logfile.write("export PlotPath=\n")
		logfile.write("export ArtusInput=\n")
		logfile.write("export Channels=\n")
		logfile.write("export Masses=\n")
		logfile.write("export Paralells=\n")
		logfile.write("export Variable=m_vis\n\n")
		logfile.write("#=====Limit commands start here=====\n\n")
		for cat in settings_info["MVATestMethodsNames"]:
			logfile.write("python $CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/scripts/makePlots_datacardsMVATest.py -i $ArtusInput -x $Variable --add-bbb-uncs -m $Masses -n $Paralells --log-level debug --clear-output-dir -e 'iso_1' 'mt' -w '(TrainingSelectionValue>=40)' -c $Channels --categories %s_up %s_down %s_mid -o $PlotPath/%s\n\n"%(cat,cat,cat,cat))
		logfile.write("\n\n#=====BDT plotting commands start here=====\n\n")
		logfile.write("\n\n#=====BDT Overview=====\n\n")
		for name in settings_info["MVATestMethodsNames"]:
			logfile.write("python $CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/scripts/makePlots_controlPlots.py -i $ArtusInput -a '--legend 0.23 0.63 0.9 0.83 --formats png eps pdf --y-rel-lims 0.9 1.75 --y-subplot-label \"S/#sqrt{B}\" --y-subplot-lims 0 1 --x-bins \"20,-1,1\" --filename overview_%s' -s ztt zll ttj vv wj qcd ggh qqh vh htt -m $Masses -e 'iso_1' 'mt' --sbratio -c $Channels --scale-signal 250 -o $PlotPath/BDTs/%s -n $Paralells -x %s\n\n"%(name,name,name))

		logfile.write("\n\n#=====BDT Overtraining=====\n\n")
		for in_dir in args.input_dir:
			IN_DIR = os.path.join(in_dir, "*")
			logfile.write("python $CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/scripts/plot_overtraining.py -i %s -o $PlotPath/BDTs -n $Paralells\n"%IN_DIR)
		logfile.write("\n")

		for name, nfold in zip(settings_info["MVATestMethodsNames"], settings_info["MVATestMethodsNFolds"]):
			if nfold == 1:
				continue
			reg_x = []
			rel_x = []
			sqrt_x = []
			for i in range(1,nfold+1):
				reg_x.append("((T%i%s-%s)/%i)"%(i,name,name,nfold-1))
				rel_x.append("abs((T%i%s-%s)/%i)"%(i,name,name,nfold-1))
				sqrt_x.append("((T%i%s-%s)/%i)**2"%(i,name,name,nfold-1))
			logfile.write("python $CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/scripts/makePlots_controlPlots.py -s ztt zll vv wj ttj qcd data htt -c $Channels -m $Masses -i $ArtusInput -e mt iso_1 -a '--x-bins \"400,-1,1\" --x-label \"#scale[1.1]{#sum(T(i)-Fin)/%i}\" --formats eps png pdf --filename \"sum_diff\" --y-subplot-lims 0 2' -o $PlotPath/BDTs/%s -r -x '%s'\n"%(nfold-1,name, "+".join(reg_x)))
			logfile.write("python $CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/scripts/makePlots_controlPlots.py -s ztt zll vv wj ttj qcd data htt -c $Channels -m $Masses -i $ArtusInput -e mt iso_1 -a '--x-bins \"200,0,1\" --x-label \"#scale[1.1]{#sum#cbar(T(i)-Fin)/%i#cbar}\" --formats eps png pdf --filename \"abs_diff\" --y-subplot-lims 0 2' -o $PlotPath/BDTs/%s -r -x '%s'\n"%(nfold-1,name, "+".join(rel_x)))
			logfile.write("python $CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/scripts/makePlots_controlPlots.py -s ztt zll vv wj ttj qcd data htt -c $Channels -m $Masses -i $ArtusInput -e mt iso_1 -a '--x-bins \"200,0,1\" --x-label \"#scale[1.1]{(#sum((T(i)-Fin)/%i)^{2})^{0.5}}\" --formats eps png pdf --filename \"sqrt_diff\" --y-subplot-lims 0 2' -o $PlotPath/BDTs/%s -r -x 'sqrt(%s)'\n\n"%(nfold-1,name, "+".join(sqrt_x)))
			logfile.write("python $CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/scripts/makePlots_controlPlots.py -s ztt zll vv wj ttj qcd data htt -c $Channels -m $Masses -i $ArtusInput -e mt iso_1 -a '--plot-modules \"ExportRoot\" --x-bins \"1000,0,2\" --x-label \"#scale[1.1]{(#sum((T(i)-Fin)/%i)^{2})^{0.5}}\" --formats eps png pdf --filename \"sqrt_diff\"' -o $PlotPath/BDTs/%s -x 'sqrt(%s)'\n\n"%(nfold-1,name, "+".join(sqrt_x)))