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
	parser.add_argument("--channel", default="mt",
						help="channel this config is meant for. [Default: %(default)s]")
	args = parser.parse_args()
	logger.initLogger(args)
	Channel = args.channel
	log_file_list = []
	log_exclude_list = []
	log_vbf_list2 = []
	log_vbf_list = []
	log_vbf_name_list = []
	accepted_dirs = []
	variables = []
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
						  "iso_1":"lep1IsoOverPt:=iso_1", "m_vis":"diLepMass:=m_vis",
						  "jdeta":"diJetAbsDeltaEta:=jdeta", "mjj":"diJetMass:=mjj"}
	for log_file in log_file_list:
		c_log = jsonTools.JsonDict(log_file)
		quantities = ",".join(map(lambda ls: ls.pop(0), map(lambda s: s.split(";"), c_log["variables"].split(","))))
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
	jsonTools.JsonDict(settings_info).save(os.path.join(out_dir, "%s_settingsMVATestMethods.json"%Channel), indent = 4)
	jsonTools.JsonDict(settings_quantities).save(os.path.join(out_dir, "%s_MVATestMethodsQuantities.json"%Channel), indent = 4)
	categories = []
	vbf_categories = []
	print log_vbf_name_list
	with open(os.path.join(out_dir, "%s_mvadatacards.cfg"%Channel), "w") as logfile:
		for name in settings_info["MVATestMethodsNames"]:
			if name in log_vbf_name_list:
				continue
			categories.append("%s_%s_signal"%(Channel,name))
			categories.append("%s_%s_bkg"%(Channel,name))
			categories.append("%s_%s_mixed"%(Channel,name))
		for vbf_tag in log_vbf_name_list:
			for name in settings_info["MVATestMethodsNames"]:
				if name in log_vbf_name_list:
					continue
				categories.append("%s_%s_%s_%s_signal"%(Channel,vbf_tag,name,"not_tagged"))
				#vbf_categories.append("%s_%s_%s_%s_signal"%(Channel,vbf_tag,name,"not_tagged"))
				vbf_categories.append("%s_%s_%s_%s_signal"%(Channel,vbf_tag,name,"tagged"))
		logfile.write("\n".join(categories))
		logfile.write("\n")
		logfile.write("\n".join(vbf_categories))
		categories.append("%s_inclusive"%Channel)
		variables_plot_string = "python $CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/scripts/makePlots_controlPlots.py -r -i $ArtusInput -a '--legend 0.23 0.63 0.9 0.83 --formats png eps pdf --y-rel-lims 0.9 1.75 --y-subplot-lims 0.5 1.5' -s ztt zll ttj vv wj qcd ggh qqh vh htt data -m $Masses -c {channel} -w $Weights --scale-signal {scale} -o $PlotPath/Controllplots/{channel} -n $Paralells --blinding-threshold 0.1 --categories {categories} -x {variables} --scale-mc-only $scale_mc --project-to-lumi $project_lumi --cut-mc-only $cut_mc\n"

		fold5_stepped_string = "# python $CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/scripts/makePlots_controlPlots.py -i $ArtusInput -a '--legend 0.23 0.63 0.9 0.83 --formats png eps pdf --y-rel-lims 0.9 1.75 --x-bins \"{nfold},0,100\" --filename \"stepped_{name}\"' -s ztt zll ttj vv wj qcd ggh qqh vh htt data -m $Masses -e 'iso_1' 'mt' -c {channel} -w $Weights --scale-signal 250 -o $PlotPath/BDTs/{channel}/{name} -n $Paralells -x 'TrainingSelectionValue' -w '1*(T1{name}=={name})+2*(T2{name}=={name})+3*(T3{name}=={name})+4*(T4{name}=={name})+5*(T5{name}=={name})' --scale-mc-only $scale_mc --project-to-lumi $project_lumi --cut-mc-only $cut_mc\n"

		ratio_string = "python $CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/scripts/makePlots_controlPlots.py -i $ArtusInput -a '--legend 0.23 0.63 0.9 0.83 --formats png eps pdf --y-rel-lims 0.9 1.75 --y-subplot-lims 0.5 1.5 --x-bins \"40,-1,1\" --filename \"ratio_{name}\"' -s ztt zll ttj vv wj qcd ggh qqh vh htt data -m $Masses  -r --blinding-threshold 0.15 -c {channel} -w $Weights --scale-signal 250 -o $PlotPath/BDTs/{channel}/{name} -n $Paralells -x {name} --scale-mc-only $scale_mc --project-to-lumi $project_lumi --cut-mc-only $cut_mc\n"

		integral_string = "python $CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/scripts/makePlots_controlPlots.py -i $ArtusInput -a '--legend 0.23 0.63 0.9 0.83 --formats png eps pdf --y-rel-lims 0.9 1.75 --x-bins \"{binning}\" --filename \"integral_{name}\" --sob-frontname \"regular_name : \"' -s ztt zll ttj vv wj qcd ggh qqh vh htt data -m $Masses  --integrated-sob --integration-directions 'righttoleft' 'righttoleft' 'righttoleft' 'rcombination' --integration-output $PlotPath/BDTs/{channel}_minmax.txt -c {channel} -w $Weights --blinding-threshold 0.15 --scale-signal 250 -o $PlotPath/BDTs/{channel}/{name} -n $Paralells -x {name} --scale-mc-only $scale_mc --project-to-lumi $project_lumi --cut-mc-only $cut_mc\n"

		vbf_integral_string = "python $CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/scripts/makePlots_controlPlots.py -i $ArtusInput -a '--legend 0.23 0.63 0.9 0.83 --formats png eps pdf --y-rel-lims 0.9 1.75 --x-bins \"{binning}\" --filename \"integral_{regular_bdt}\" --sob-frontname \"vbf_tagger : \"' -s ggh qqh -m $Masses  --integrated-sob --integration-nick qqh --integration-background ggh --integration-methods soversqrtsplusb --integration-directions 'righttoleft' 'righttoleft' 'rcombination' --integration-output $PlotPath/BDTs/{channel}_minmax.txt -c {channel} -w $Weights -o $PlotPath/BDTs/{channel}/{vbf_tagger} -n $Paralells --categories {channel}_{regular_bdt}_signal -x {vbf_tagger} --scale-mc-only $scale_mc --project-to-lumi $project_lumi --cut-mc-only $cut_mc\n"

		sqrt_plot_string = "python $CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/scripts/makePlots_controlPlots.py -s ztt zll vv wj ttj qcd data htt -c {channel} -w $Weights -m $Masses -i $ArtusInput -a '--plot-modules \"{plot_module}\" --x-bins \"{bins}\" --x-label \"#scale[1.1]{{(#sum((T(i)-Fin)/{nFold})^{{2}})^{{0.5}}}}\" --formats eps png pdf --filename \"sqrt_diff\" --y-subplot-lims 0 2' -o $PlotPath/BDTs/{channel}/{name} -r -x 'sqrt({sqrts})' --scale-mc-only $scale_mc --project-to-lumi $project_lumi --cut-mc-only $cut_mc\n"

		overlap_plot_string = "python $CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/scripts/makePlots_controlPlots.py -s ggh qqh -c {channel} -w $Weights -m $Masses -i $ArtusInput -a '--x-bins \"3,0.5,3.5\" --x-label \"\" --formats eps png pdf --filename \"{name}_vbfOverlap\" --x-ticks 1 2 3 --x-tick-labels classic {name} overlap' -o $PlotPath/BDTs/{channel}/{folder} -x '{comp}'\n"

		mva_limit_string = "python $CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/scripts/makePlots_datacardsMVATest.py -i $ArtusInput -x $Variable --add-bbb-uncs -m $Masses -n $Paralells --log-level debug --clear-output-dir -c {channel} -w $Weights --categories {tagger}_{mva_name}_tagged_signal {tagger}_{mva_name}_not_tagged_signal {mva_name}_bkg {mva_name}_mixed -o $PlotPath/{channel}/{tagger}_{mva_name} --scale-mc-only $scale_mc --project-to-lumi $project_lumi --cut-mc-only $cut_mc\n\n"

		copy_print_string = "#=====copy files with new categories=====\ncp $PlotPath/BDTs/{channel}_minmax.txt $CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/mva_configs/{channel}_expressions.cfg\ncp {path} $CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/mva_configs/{channel}_mvadatacards.cfg\n"

	with open(os.path.join(out_dir, "{channel}_plot_commands.sh".format(channel=Channel)), "w") as logfile:
		logfile.write("#!/bin/bash\n")
		logfile.write("#Adjust these export commands to meet your directory settings\n")
		logfile.write("export PlotPath=\n")
		logfile.write("export ArtusInput=\n")
		logfile.write("export Masses=\n")
		logfile.write("export Weights=\n")
		logfile.write("export Paralells=\n")
		logfile.write("export scale_mc='1.0'\n")
		logfile.write("export project_lumi='1.0'\n")
		logfile.write("export cut_mc='1.0'\n")
		logfile.write("export Variable=m_vis\n\n")
		logfile.write("#=====BDT plotting commands start here=====\n")
		logfile.write("mkdir -p $PlotPath/BDTs\n")
		logfile.write("rm $PlotPath/BDTs/{channel}_minmax.txt\n".format(channel=Channel))
		logfile.write("touch $PlotPath/BDTs/{channel}_minmax.txt\n".format(channel=Channel))
		logfile.write("\n#============Control Plots =============\n")

		logfile.write("\n\n#=====BDT Overview=====\n\n")
		for i,name in enumerate(settings_info["MVATestMethodsNames"]):
			#if int(settings_info["MVATestMethodsNFolds"][i]) == 5:
				#logfile.write(fold5_stepped_string.format(channel=Channel,name=name, nfold=settings_info["MVATestMethodsNFolds"][i]))
			if name in log_vbf_name_list:
				logfile.write("\n")
				continue
			logfile.write(ratio_string.format(channel=Channel,name=name))
			logfile.write(integral_string.format(channel=Channel,name=name,binning="400,-1,1"))
			logfile.write(copy_print_string.format(path=os.path.join(out_dir, "%s_mvadatacards.cfg"%(Channel)), channel=Channel))
			for vbf_tag in log_vbf_name_list:
				logfile.write(vbf_integral_string.format(channel=Channel,vbf_tagger= vbf_tag, regular_bdt=name, binning="400,-1,1"))
			logfile.write("\n")
		logfile.write("\n\n")
		logfile.write(copy_print_string.format(path=os.path.join(out_dir, "%s_mvadatacards.cfg"%(Channel)), channel=Channel))
		logfile.write("\n")
		variables.append("m_sv")
		variables.append("m_vis")
		logfile.write(variables_plot_string.format(channel=Channel,categories=" ".join(categories),variables=" ".join(variables),scale=250))
		logfile.write(variables_plot_string.format(channel=Channel,categories=" ".join(vbf_categories),variables=" ".join(variables),scale=25))

		logfile.write("\n\n#=====BDT Overtraining=====\n\n")
		for in_dir in accepted_dirs:
			IN_DIR = os.path.join(in_dir, "*")
			logfile.write("python $CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/scripts/plot_overtraining.py -i %s -o $PlotPath/BDTs/%s -n $Paralells\n"%(IN_DIR,Channel))
		logfile.write("\n")
		for name, nfold in zip(settings_info["MVATestMethodsNames"], settings_info["MVATestMethodsNFolds"]):
			if nfold == 1:
				continue
			reg_x = []
			rel_x = []
			sqrt_x = []
			for i in range(1,nfold+1):
				#reg_x.append("((T%i%s-%s)/%i)"%(i,name,name,nfold-1))
				#rel_x.append("abs((T%i%s-%s)/%i)"%(i,name,name,nfold-1))
				sqrt_x.append("((T%i%s-%s)/%i)**2"%(i,name,name,nfold-1))
			#logfile.write("python $CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/scripts/makePlots_controlPlots.py -s ztt zll vv wj ttj qcd data htt -c {channel} -w $Weights -m $Masses -i $ArtusInput -a '--x-bins \"40,0.5,0.5\" --x-label \"#scale[1.1]{#sum(T(i)-Fin)/%i}\" --formats eps png pdf --filename \"sum_diff\" --y-subplot-lims 0 2' -o $PlotPath/BDTs/%s -r -x '%s'\n"%(nfold-1,name, "+".join(reg_x)))
			#logfile.write("python $CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/scripts/makePlots_controlPlots.py -s ztt zll vv wj ttj qcd data htt -c {channel} -w $Weights -m $Masses -i $ArtusInput -a '--x-bins \"20,0,0.5\" --x-label \"#scale[1.1]{#sum#cbar(T(i)-Fin)/%i#cbar}\" --formats eps png pdf --filename \"abs_diff\" --y-subplot-lims 0 2' -o $PlotPath/BDTs/%s -r -x '%s'\n"%(nfold-1,name, "+".join(rel_x)))
			logfile.write(sqrt_plot_string.format(channel=Channel,nFold=nfold-1,name=name, sqrts="+".join(sqrt_x), bins="20,0,0.5", plot_module="PlotRootHtt"))
			logfile.write(sqrt_plot_string.format(channel=Channel,nFold=nfold-1,name=name, sqrts="+".join(sqrt_x), bins="1000,0,2", plot_module="ExportRoot"))
		logfile.write("python $CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/scripts/nFold_DiffScan.py -i $PlotPath/BDTs/{channel} -o $PlotPath/{channel}_DiffScans -m $Masses".format(channel=Channel))

		logfile.write("\n\n#=====Categorization Overlap=====\n\n")
		for vbf_tag in log_vbf_name_list:
			for name in settings_info["MVATestMethodsNames"]:
				if name in log_vbf_name_list:
					continue
				tagger_vbf = "%s_%s_%s_%s_signal"%(Channel,vbf_tag,name,"tagged")
				comp_string = "1*{classic_vbf}+2*{tagger_vbf}".format(tagger_vbf=tagger_vbf, classic_vbf="catHtt13TeV_%s_2jet_vbf"%Channel)
				logfile.write(overlap_plot_string.format(name=name, channel=Channel, folder=vbf_tag, comp=comp_string))


		logfile.write("\n\n#=====Limit commands start here=====\n\n")
		logfile.write("python $CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/scripts/makePlots_datacardsSMHtt.py -i $ArtusInput -x $Variable --add-bbb-uncs -m $Masses -n $Paralells --clear-output-dir -c {channel} -w $Weights -o $PlotPath/{channel}/classic\n\n".format(channel=Channel))
		limit_folders = ["$PlotPath/{channel}/classic".format(channel=Channel)]
		for cat in settings_info["MVATestMethodsNames"]:
			if cat in log_vbf_name_list:
				continue
			for vbf_tag in log_vbf_name_list:
				logfile.write(mva_limit_string.format(channel=Channel,mva_name=cat, tagger=vbf_tag))
				limit_folders.append("$PlotPath/{channel}/{tagger}_{mva_name}".format(channel=Channel,mva_name=cat, tagger=vbf_tag))
		logfile.write("\npython $CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/scripts/limit_collector.py -i %s -o $PlotPath/limits_vbftagging -m $Masses\n"%(" ".join(limit_folders)))

		logfile.write("\n\n#=====remove files with new categories=====\n\n")
		logfile.write("rm $CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/mva_configs/{channel}_expressions.cfg\n".format(channel=Channel))
		logfile.write("rm $CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/mva_configs/{channel}_mvadatacards.cfg\n".format(channel=Channel))
		logfile.write("touch $CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/mva_configs/{channel}_expressions.cfg\n".format(channel=Channel))
		logfile.write("touch $CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/mva_configs/{channel}_mvadatacards.cfg\n".format(channel=Channel))