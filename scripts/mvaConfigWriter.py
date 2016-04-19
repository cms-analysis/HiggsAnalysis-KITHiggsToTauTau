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
	parser.add_argument("--vbf-tags", nargs="+", default=[],
						help="trainings which are used for vbf tagging")
	args = parser.parse_args()
	logger.initLogger(args)

	log_file_list = []
	log_exclude_list = []
	log_vbf_list2 = []
	log_vbf_list = []
	log_vbf_name_list = []
	accepted_dirs = []
	variables = ["TrainingSelectionValue"]
	if args.output_dir == None:
		out_dir = args.input_dir[0]
	else:
		out_dir = args.output_dir
	if not os.path.exists(out_dir):
		os.makedirs(out_dir)
	for in_dir in args.input_dir:
		map(log_file_list.__iadd__, map(glob.glob, [os.path.join(in_dir, l) for l in args.combine_log]))
		map(log_exclude_list.__iadd__, map(glob.glob, [os.path.join(in_dir, l) for l in args.exclude_log]))
		map(log_vbf_list2.__iadd__, map(glob.glob, [os.path.join(in_dir, l) for l in args.vbf_tags]))
	for ex_log in log_exclude_list:
		if ex_log in log_file_list:
			log_file_list.pop(log_file_list.index(ex_log))
	for tag in log_vbf_list2:
		if tag in log_file_list:
			log_vbf_list.append(tag)
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
	variable_name_mapping = {"pt_1":"lep1Pt:=pt_1", "mt_1":"lep1MetMt:=mt_1",
						  "pt_2":"lep2Pt:=pt_2", "mt_2":"lep2MetMt:=mt_2",
						  ",met":",pfMetPt:=met","mvamet":"mvaMetPt:=mvamet",
						  ",pzetamiss,":",pZetaMiss:=pzetamiss,",
						  ",pzetavis,":",pZetaVis:=pzetavis,",
						  "njets":"nJets30:=njets","nbtag":"nBJets20:=nbtag",
						  "iso_1":"lep1IsoOverPt:=iso_1", "m_vis":"diLepMass:=m_vis"}
	for log_file in log_file_list:
		c_log = jsonTools.JsonDict(log_file)
		quantities = c_log["variables"]
		for quan in quantities.split(","):
			if not quan in variables:
				variables.append(quan)
		for key, repl in variable_name_mapping.iteritems():
			quantities = quantities.replace(key, repl)
		weight_path, dump = os.path.split(log_file)
		accepted_dirs.append(weight_path)
		n_fold = c_log["N-Fold"]
		training_name = c_log["training_name"]
		if log_file in log_vbf_list:
			log_vbf_name_list.append(training_name)
		methods = c_log["methods"]
		found_variable_string = False
		for i in range(0,quantities_index+1,1):
			if ("%i;"%i + quantities) in settings_info["MVATestMethodsInputQuantities"]:
				found_variable_string = True
				found_quantities_index = i
				break
		if not found_variable_string:
			quantities_index += 1
			found_quantities_index = quantities_index
			settings_info["MVATestMethodsInputQuantities"].append("%i;"%found_quantities_index + quantities)
		settings_info["MVATestMethodsNames"].append(training_name)
		settings_info["MVATestMethodsNFolds"].append(n_fold)
		for method in methods:
			method = method.split(";")[0]
			settings_quantities["property"].append(training_name)
			if n_fold == 1:
				settings_info["MVATestMethodsMethods"].append("%i;%s"%(found_quantities_index, method))
				settings_info["MVATestMethodsWeights"].append(full_path(weight_path+"/T%i_%s_%s.weights.xml"%(1,method,training_name)))
			else:
				for i in range(1,n_fold+1):
					settings_info["MVATestMethodsMethods"].append("%i;%s"%(found_quantities_index, method))
					settings_info["MVATestMethodsWeights"].append(full_path(weight_path+"/T%i_%s_%s.weights.xml"%(i,method,training_name)))
					settings_quantities["property"].append("T%i%s"%(i, training_name))
	jsonTools.JsonDict(settings_info).save(os.path.join(out_dir, "settingsMVATestMethods.json"), indent = 4)
	jsonTools.JsonDict(settings_quantities).save(os.path.join(out_dir, "MVATestMethodsQuantities.json"), indent = 4)

	with open(os.path.join(out_dir, "mvadatacards.cfg"), "w") as logfile:
		out_lines=[]
		for name in settings_info["MVATestMethodsNames"]:
			if name in log_vbf_name_list:
				continue
			out_lines.append("%s_signal\n"%name)
			out_lines.append("%s_bkg\n"%name)
			out_lines.append("%s_mixed\n"%name)
		for vbf_tag in log_vbf_name_list:
			for name in settings_info["MVATestMethodsNames"]:
				if name in log_vbf_name_list:
					continue
				for tag in ("not_tagged", "tagged", "inclusive"):
					out_lines.append("%s_%s_%s_signal\n"%(vbf_tag,name,tag))
					out_lines.append("%s_%s_%s_bkg\n"%(vbf_tag,name,tag))
					out_lines.append("%s_%s_%s_mixed\n"%(vbf_tag,name,tag))
		logfile.write("".join(out_lines))

	with open(os.path.join(out_dir, "plot_commands.sh"), "w") as logfile:
		logfile.write("#!/bin/bash\n")
		logfile.write("#Adjust these export commands to meet your directory settings\n")
		logfile.write("export PlotPath=\n")
		logfile.write("export ArtusInput=\n")
		logfile.write("export Channels=\n")
		logfile.write("export Masses=\n")
		logfile.write("export Weights=\n")
		logfile.write("export Paralells=\n")
		logfile.write("export Variable=m_vis\n\n")
		logfile.write("#=====BDT plotting commands start here=====\n")
		logfile.write("mkdir -p $PlotPath/BDTs\n")
		logfile.write("rm $PlotPath/BDTs/minmax.txt\n")
		logfile.write("touch $PlotPath/BDTs/minmax.txt\n")
		logfile.write("\n#============Control Plots =============\n")
		logfile.write("python $CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/scripts/makePlots_controlPlots.py -r -i $ArtusInput -a '--legend 0.23 0.63 0.9 0.83 --formats png eps pdf --y-rel-lims 0.9 1.75' -s ztt zll ttj vv wj qcd ggh qqh vh htt data -m $Masses -c $Channels -w $Weights --scale-signal 250 -o $PlotPath/Controllplots -n $Paralells -x {variables}\n".format(variables=" ".join(variables)))
		logfile.write("python $CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/scripts/makePlots_controlPlots.py -r -i $ArtusInput -a '--legend 0.23 0.63 0.9 0.83 --formats png eps pdf --y-rel-lims 0.9 1.75' -s ztt zll ttj vv wj qcd ggh qqh vh htt data -m $Masses -c $Channels -w $Weights --scale-signal 250 -o $PlotPath/Controllplots_ext -e mt iso_1 -n $Paralells -x {variables}\n".format(variables=" ".join(variables)))
		logfile.write("\n\n#=====BDT Overview=====\n\n")
		for i,name in enumerate(settings_info["MVATestMethodsNames"]):
			if int(settings_info["MVATestMethodsNFolds"][i]) == 5:
				#logfile.write("python $CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/scripts/makePlots_controlPlots.py -i $ArtusInput -a '--legend 0.23 0.63 0.9 0.83 --formats png eps pdf --y-rel-lims 0.9 1.75 --x-bins \"{nfold},0,100\" --filename \"stepped_{name}\"' -s ztt zll ttj vv wj qcd ggh qqh vh htt data -m $Masses -e 'iso_1' 'mt' -c $Channels -w $Weights --scale-signal 250 -o $PlotPath/BDTs/{name} -n $Paralells -x 'TrainingSelectionValue' -w '1*(T1{name}=={name})+2*(T2{name}=={name})+3*(T3{name}=={name})+4*(T4{name}=={name})+5*(T5{name}=={name})'\n".format(name=name, nfold=settings_info["MVATestMethodsNFolds"][i]))
				logfile.write("python $CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/scripts/makePlots_controlPlots.py -i $ArtusInput -a '--legend 0.23 0.63 0.9 0.83 --formats png eps pdf --y-rel-lims 0.9 1.75 --y-subplot-lims 0.5 1.5 --x-bins \"40,-1,1\" --filename \"ratio_%s\"' -s ztt zll ttj vv wj qcd ggh qqh vh htt data -m $Masses  -r --blinding-threshold 0.15 -c $Channels -w $Weights --scale-signal 250 -o $PlotPath/BDTs/%s -n $Paralells -x %s\n"%(name,name,name))
			if name in log_vbf_name_list:
				logfile.write("\n")
				continue
			logfile.write("python $CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/scripts/makePlots_controlPlots.py -i $ArtusInput -a '--legend 0.23 0.63 0.9 0.83 --formats png eps pdf --y-rel-lims 0.9 1.75 --x-bins \"40,-1,1\" --filename \"integral_%s\" --sob-frontname \" : \"' -s ztt zll ttj vv wj qcd ggh qqh vh htt data -m $Masses  --integrated-sob --integration-methods 'righttoleft' 'righttoleft' 'righttoleft' 'rcombination' --integration-output $PlotPath/BDTs/minmax.txt -c $Channels -w $Weights --blinding-threshold 0.15 --scale-signal 250 -o $PlotPath/BDTs/%s -n $Paralells -x %s\n\n"%(name,name,name))
		for vbf_tag in log_vbf_name_list:
			logfile.write("python $CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/scripts/makePlots_controlPlots.py -i $ArtusInput -a '--legend 0.23 0.63 0.9 0.83 --formats png eps pdf --y-rel-lims 0.9 1.75 --x-bins \"40,-1,1\" --filename \"integral_{name}\" --sob-frontname \"vbf_tagger : \"' -s ztt zll ttj vv wj qcd ggh qqh vh htt data -m $Masses  --integrated-sob --integration-nick qqh --integration-methods 'righttoleft' 'righttoleft' 'rcombination' --integration-output $PlotPath/BDTs/minmax.txt -c $Channels -w $Weights --blinding-threshold 0.15 --scale-signal 250 -o $PlotPath/BDTs/{name} -n $Paralells -x {name}\n".format(name= vbf_tag))
			logfile.write("\n\n#=====copy files with new categories=====\n")
			logfile.write("cp $PlotPath/BDTs/minmax.txt $CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/mva_configs/expressions.cfg\n")
			logfile.write("cp %s $CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/mva_configs/mvadatacards.cfg\n"%os.path.join(out_dir, "mvadatacards.cfg"))
			for i,name in enumerate(settings_info["MVATestMethodsNames"]):
				if name in log_vbf_name_list:
					continue
				logfile.write("python $CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/scripts/makePlots_controlPlots.py -i $ArtusInput -a '--legend 0.23 0.63 0.9 0.83 --formats png eps pdf --y-rel-lims 0.9 1.75 --x-bins \"40,-1,1\" --filename \"integral_{name}_{vbf_tag}_tagged\" --sob-frontname \"tagged : \"' -s ztt zll ttj vv wj qcd ggh qqh vh htt data -m $Masses  --integrated-sob --integration-methods 'righttoleft' 'righttoleft' 'righttoleft' 'rcombination' --integration-output $PlotPath/BDTs/minmax.txt -c $Channels --categories {name}_{vbf_tag}_tagged -w $Weights --blinding-threshold 0.15 --scale-signal 250 -o $PlotPath/BDTs/{name} -n $Paralells -x {name}\n".format(name=name, vbf_tag=vbf_tag))
				logfile.write("python $CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/scripts/makePlots_controlPlots.py -i $ArtusInput -a '--legend 0.23 0.63 0.9 0.83 --formats png eps pdf --y-rel-lims 0.9 1.75 --x-bins \"40,-1,1\" --filename \"integral_{name}_{vbf_tag}_not_tagged\" --sob-frontname \"not_tagged : \"' -s ztt zll ttj vv wj qcd ggh qqh vh htt data -m $Masses  --integrated-sob --integration-methods 'righttoleft' 'righttoleft' 'righttoleft' 'rcombination' --integration-output $PlotPath/BDTs/minmax.txt -c $Channels --categories -{name}_{vbf_tag}_not_tagged w $Weights --blinding-threshold 0.15 --scale-signal 250 -o $PlotPath/BDTs/{name} -n $Paralells -x {name}\n".format(name=name, vbf_tag=vbf_tag))
			logfile.write("\n")

		logfile.write("\n\n#=====copy files with new categories=====\n")
		logfile.write("cp $PlotPath/BDTs/minmax.txt $CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/mva_configs/expressions.cfg\n")
		logfile.write("cp %s $CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/mva_configs/mvadatacards.cfg\n"%os.path.join(out_dir, "mvadatacards.cfg"))

		logfile.write("\n\n#=====BDT Overtraining=====\n\n")
		for in_dir in accepted_dirs:
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
			#logfile.write("python $CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/scripts/makePlots_controlPlots.py -s ztt zll vv wj ttj qcd data htt -c $Channels -w $Weights -m $Masses -i $ArtusInput -e mt iso_1 -a '--x-bins \"40,0.5,0.5\" --x-label \"#scale[1.1]{#sum(T(i)-Fin)/%i}\" --formats eps png pdf --filename \"sum_diff\" --y-subplot-lims 0 2' -o $PlotPath/BDTs/%s -r -x '%s'\n"%(nfold-1,name, "+".join(reg_x)))
			#logfile.write("python $CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/scripts/makePlots_controlPlots.py -s ztt zll vv wj ttj qcd data htt -c $Channels -w $Weights -m $Masses -i $ArtusInput -e mt iso_1 -a '--x-bins \"20,0,0.5\" --x-label \"#scale[1.1]{#sum#cbar(T(i)-Fin)/%i#cbar}\" --formats eps png pdf --filename \"abs_diff\" --y-subplot-lims 0 2' -o $PlotPath/BDTs/%s -r -x '%s'\n"%(nfold-1,name, "+".join(rel_x)))
			logfile.write("python $CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/scripts/makePlots_controlPlots.py -s ztt zll vv wj ttj qcd data htt -c $Channels -w $Weights -m $Masses -i $ArtusInput -e mt iso_1 -a '--x-bins \"20,0,0.5\" --x-label \"#scale[1.1]{(#sum((T(i)-Fin)/%i)^{2})^{0.5}}\" --formats eps png pdf --filename \"sqrt_diff\" --y-subplot-lims 0 2' -o $PlotPath/BDTs/%s -r -x 'sqrt(%s)'\n"%(nfold-1,name, "+".join(sqrt_x)))
			logfile.write("python $CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/scripts/makePlots_controlPlots.py -s ztt zll vv wj ttj qcd data htt -c $Channels -w $Weights -m $Masses -i $ArtusInput -e mt iso_1 -a '--plot-modules \"ExportRoot\" --x-bins \"1000,0,2\" --x-label \"#scale[1.1]{(#sum((T(i)-Fin)/%i)^{2})^{0.5}}\" --formats eps png pdf --filename \"sqrt_diff\"' -o $PlotPath/BDTs/%s -x 'sqrt(%s)'\n\n"%(nfold-1,name, "+".join(sqrt_x)))
		logfile.write("python $CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/scripts/nFold_DiffScan.py -i $PlotPath/BDTs -o $PlotPath/DiffScans -m $Masses")
		logfile.write("\n\n#=====Limit commands start here=====\n\n")
		logfile.write("python $CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/scripts/makePlots_datacardsSMHtt.py -i $ArtusInput -x $Variable --add-bbb-uncs -m $Masses -n $Paralells --clear-output-dir -c $Channels -w $Weights -o $PlotPath/classic\n\n")
		limit_folders = ["$PlotPath/classic"]
		logfile.write("\n\n#=====No VBF-Tag=====\n\n")
		for cat in settings_info["MVATestMethodsNames"]:
			if cat in log_vbf_name_list:
				continue
			logfile.write("python $CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/scripts/makePlots_datacardsMVATest.py -i $ArtusInput -x $Variable --add-bbb-uncs -m $Masses -n $Paralells --log-level debug --clear-output-dir -c $Channels -w $Weights --categories %s_signal %s_bkg %s_mixed -o $PlotPath/%s_nec\n\n"%(cat,cat,cat,cat))
			limit_folders.append("$PlotPath/%s_nec"%cat)
		logfile.write("python $CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/scripts/limit_collector.py -i %s -o $PlotPath/limits_notaggin -m $Masses\n"%(" ".join(limit_folders)))

		logfile.write("\n\n#=====With VBF-Tag=====\n\n")
		limit_folders = ["$PlotPath/classic"]
		for vbf_tag in log_vbf_name_list:
			logfile.write("#=====VBF Tag variable: %s ===========\n" %vbf_tag)
			for cat in settings_info["MVATestMethodsNames"]:
				if cat in log_vbf_name_list:
					continue
				logfile.write("python $CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/scripts/makePlots_datacardsMVATest.py -i $ArtusInput -x $Variable --add-bbb-uncs -m $Masses -n $Paralells --log-level debug --clear-output-dir -c $Channels -w $Weights --categories {tagger}_{mva_name}_tagged_signal {tagger}_{mva_name}_not_tagged_signal {tagger}_{mva_name}_inclusive_bkg {tagger}_{mva_name}_inclusive_mixed -o $PlotPath/{tagger}_{mva_name}_nec\n\n".format(mva_name=cat, tagger=vbf_tag))
				limit_folders.append("$PlotPath/{tagger}_{mva_name}_nec".format(tagger=vbf_tag, mva_name=cat))
			logfile.write("\n")

		logfile.write("python $CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/scripts/limit_collector.py -i %s -o $PlotPath/limits_vbftagging -m $Masses\n"%(" ".join(limit_folders)))
		logfile.write("\n\n#=====remove files with new categories=====\n\n")
		logfile.write("\n\nrm $CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/mva_configs/expressions.cfg\n")
		logfile.write("rm $CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/mva_configs/mvadatacards.cfg\n")
		logfile.write("touch $CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/mva_configs/expressions.cfg\n")
		logfile.write("touch $CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/mva_configs/mvadatacards.cfg\n")