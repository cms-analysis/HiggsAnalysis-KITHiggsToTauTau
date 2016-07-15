#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import argparse
import copy
import os

import Artus.Utility.jsonTools as jsonTools
import Artus.Utility.tools as aTools
import sys
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.samples_run2 as samples
import glob
import time
import ROOT
import shutil
import math
import AddMVATrainingToTrees
import GetFocussedTrainingCut
import array

ROOT.PyConfig.IgnoreCommandLineOptions = True
def get_configs(args, info_log):
	plot_configs = []
	#generate config_list containing one config file per requested nick for training
	log.info("prepare config files to extract file paths, weights and cuts")
	sample_settings = samples.Samples()
	for channel in args["channels"]:
		category = args.get("category",None)
		for requested_sample in (args["bkg_samples"]+args["signal_samples"]):
			if requested_sample == "samesigndata":
				list_of_samples = [getattr(samples.Samples, "data")]
			else:
				list_of_samples = [getattr(samples.Samples, requested_sample)]
			config = sample_settings.get_config(
					samples=list_of_samples,
					channel=channel,
					category=category,
					higgs_masses=args["higgs_masses"],
					normalise_signal_to_one_pb=False,
					ztt_from_mc=False,
					weight=args["weight"],
					lumi = args["lumi"] * 1000,
					exclude_cuts=args["exclude_cuts"],
					stack_signal=False,
					scale_signal=1.0,
					mssm=False
					)
			config["request_nick"] = requested_sample
			if requested_sample in args["bkg_samples"] and requested_sample in args["signal_samples"]:
				log.error("Sample %s is scheduled for signal and background" %requested_sample)
				sys.exit()
			if requested_sample in args["bkg_samples"]:
				config["sig_bkg"] = "Background"
			elif requested_sample in args["signal_samples"]:
				config["sig_bkg"] = "Signal"
			if args.get("loop",1) > 1:
				#config.setdefault("files", []).append(os.path.basename(args["output_file"]) + "*" + requested_sample + "*.root")
				del config["files"][:]
				config["files"].append("L%i_%s*%s*.root"%(args["loop"]-1, os.path.basename(args["output_file"]).split("_",1)[1], requested_sample))
				print "L%i_%s*%s*.root"%(args["loop"]-1, os.path.basename(args["output_file"]).split("_",1)[1], requested_sample)
				del config["folders"][:]
				config["folders"].append("SplitTree")
			if requested_sample == "samesigndata":
				config["weights"][0]=config["weights"][0].replace("(q_1*q_2)<0.0", "(q_1*q_2)>0.0")
			plot_configs.append(config)
			info_log["config_list"].append(config)
	log.info("Config information aquired")
	return (plot_configs, info_log)

def do_splitting(args, plot_configs):

	splits_list = []
	stored_files_list = []
	s_b_extension = []
	if args["Split"] and args["n_fold"] == 1:
		splits_list.append("(TrainingSelectionValue>=%i)"%int(args["Split"]))
		splits_list.append("(TrainingSelectionValue<%i)"%int(args["Split"]))
	elif args["n_fold"] and len(args["custom_splitting"]) == int(args["n_fold"]):
		for split in args["custom_splitting"]:
			splits_list.append(split)
	elif args["n_fold"]:
		part_size = 100./((args["n_fold"])*10.)
		temp_splits = []
		for i in range((args["n_fold"])*10):
			temp_splits.append("(TrainingSelectionValue>=%i)*(TrainingSelectionValue<%i)"%(int(i*part_size),int((i+1)*part_size)))
		for i in range(args["n_fold"]):
			splits_list.append("("+"||".join(temp_splits[i::args["n_fold"]])+")")
	# create output file
	dir_path, filename = os.path.split(args["output_file"])
	filename = filename.replace(".root", "")
	storage_name_extension = dir_path + "/storage/" + filename + "_storage"
	log.info("prepare output directory")
	if dir_path is None:
		pass
	elif not os.path.exists(dir_path):
		os.makedirs(dir_path)
		os.makedirs(dir_path+"/storage")
	if not os.path.exists(dir_path+"/storage"):
		os.makedirs(dir_path+"/storage")

	#produce trees
	log.info("start production of input trees for training - splitting included")
	for config in plot_configs:
		c_tree_list = ROOT.TList()
		root_file_name_list = []
		stored_files_list.append("%s_%s_"%(storage_name_extension, config["request_nick"]))
		s_b_extension.append(config["sig_bkg"])
		log.info("Prepare sample: %s" %config["request_nick"])
		cuts = ""
		#if the splitted files already exists, sckip producing them
		if sum([os.path.exists("%s_%s_%s.root"%(storage_name_extension, config["request_nick"], "split%i"%(j+1))) for j, split in enumerate(splits_list)]):
			log.info("Splitsamples already there, skip production")
			continue

		for i,nick in enumerate(config["nicks"]):
			if not bool(sum([x in nick for x in ["wmh", "wph", "zh"]])) and "noplot" in nick:
				continue
			#next line splits file_string into filenames, those could contain * -> use glob.glob to map * to real names, add the list to root_file_name_list
			map(root_file_name_list.__iadd__, map(glob.glob, map(args["input_dir"].__add__, config["files"][i].split(" "))))
			if (not cuts == "") and (not cuts == config["weights"][i]):
				log.error("can not decide which weight to use for sample %s nick %s" %(config["request_nick"],nick))
			cuts = config["weights"][i]
		for root_file_name in root_file_name_list:
			#load the requested rootfiles with their containing ntuples
			log.debug("Prepare Rootfile %s as Sample %s" %(root_file_name, config["request_nick"]))
			#info_log["steps"].append("Prepare Rootfile %s as Sample %s" %(root_file_name, config["request_nick"]))
			#time.sleep(5)
			c_tree_list.Add(ROOT.TChain())
			root_file_name = root_file_name + '/' + config["folders"][0]
			c_tree_list[-1].Add(root_file_name)
			c_tree_list[-1].SetBranchStatus("*", 1)
			#for iname in c_tree_list[-1].GetListOfBranches():
				#print iname
			#import pdb
			#pdb.set_trace()
		for j,split in enumerate(splits_list):
			#combine the root ntuples from c_tree_list into one ntuple. this happens for every split sample for the nfold training
			c_tree_list2 = ROOT.TList()
			c_tree = ""
			store_file = ROOT.TFile("%s_%s_%s.root"%(storage_name_extension, config["request_nick"], "split%i"%(j+1)), "RECREATE")
			selection_string = "*".join((split,cuts,args["pre_selection"])).replace("eventWeight*", "")
			for index in range(len(c_tree_list)):
				#import pdb
				log.debug("Cut Tree %s for Sample %s "%(root_file_name_list[index], stored_files_list[-1]))
				log.debug("Selection string: " + selection_string)
				#pdb.set_trace()
				c_tree_list2.Add(c_tree_list[index].CopyTree(selection_string, "tree%i"%index))
			log.debug("Merge Trees for Sample %s "%stored_files_list[-1])
			if len(c_tree_list2) > 1:
				c_tree = ROOT.TTree.MergeTrees(c_tree_list2)
			else:
				c_tree = c_tree_list2[0]
			log.debug("Prepare Sample %s "%stored_files_list[-1])
			storage_tree = ""
			if config["request_nick"] in ["ztt", "zll"]:
				mod_name = "ZTT" if config["request_nick"] == "zll" else "ZLL"
				c_tree.SetBranchStatus("stitchWeight%s"%mod_name, 0)
				storage_tree = c_tree.CopyTree("", "tree%i"%(j+1))
				ptr = array.array('f',[1])
				new_branch = storage_tree.Branch("stitchWeight%s"%mod_name, ptr, "ModWeight/F")
				for evt in storage_tree:
					new_branch.Fill()
			else:
				storage_tree = c_tree.CopyTree("", "tree%i"%(j+1))
			storage_tree.SetName("SplitTree")
			storage_tree.Write()
			store_file.Close()
	return (splits_list, stored_files_list, s_b_extension)

def do_focussed_training(args):
	dir_path, filename = os.path.split(args["output_file"])
	BDTScoreCut = -1.
	significanceimprovement = 1.
	totalSE = 1.
	totalBR = 0.
	if dir_path is None:
		pass
	elif not os.path.exists(dir_path):
		os.makedirs(dir_path)
	CutInfo = open(os.path.join(dir_path,"CutInfo.txt"),"w")
	#do -f training loops
	for loop in range(1, args["focussed_training"]+1):
		log.info("#####################")
		log.info("### Launch Loop %i ###"%loop)
		log.info("#####################")
		#determine output and input paths for each loop
		args["output_file"] = os.path.join(dir_path, "Loop%i"%loop, "L%i_%s"%(loop, filename))
		if loop > 1:
			args["input_dir"] = os.path.join(dir_path, "Loop%i"%(loop-1), "storage", "")
			log.info("Cut at BDT score " + str(BDTScoreCut))
			args["pre_selection"] = "(BDTScore%i>=%f)"%(loop-1, BDTScoreCut)
		args["loop"] = loop
		do_training(args)
		#add bdt-values to sample
		log.info("Calculate BDT scores and append to event trees")
		AddMVATrainingToTrees.append_MVAbranch(glob.glob(os.path.join(dir_path, "Loop%i"%loop, "storage", "*")), ["SplitTree"],[jsonTools.JsonDict(os.path.join(dir_path, "Loop%i"%loop, "L%i_%s_TrainingLog.json"%(loop, filename)))], ["BDTScore%i"%loop])
		#create histograms and find cut value 'BDTScoreCut' for next loop
		signalfiles = []
		for sample in args["signal_samples"]:
			for samplefile in glob.glob(os.path.join(dir_path, "Loop%i"%loop, "storage", "L%i_%s_storage_%s_*"%(loop, filename, sample))):
				signalfiles.append(samplefile)
		log.debug("Signalfiles: " + str(signalfiles))
		backgroundfiles = []
		for sample in args["bkg_samples"]:
                	for samplefile in glob.glob(os.path.join(dir_path, "Loop%i"%loop, "storage", "L%i_%s_storage_%s_*"%(loop, filename, sample))):
				backgroundfiles.append(samplefile)
		log.debug("Backgroundfiles: " + str(backgroundfiles))
		BDTScoreCut, signaleff, backgroundrej = GetFocussedTrainingCut.get_cut(os.path.join(dir_path, "Loop%i"%loop), signalfiles, backgroundfiles, "BDTScore%i"%loop, args["FT_cut_method"], args["FT_cut_parameter"])
		log.info("Significance improvement of the current loop appliying this cut: " + str(signaleff/math.sqrt(1.0-backgroundrej)))
		significanceimprovement = significanceimprovement*signaleff/math.sqrt(1.0-backgroundrej)
		totalSE = totalSE*signaleff
		totalBR = 1.0-((1.0-totalBR)*(1.0-backgroundrej))
		log.info("Total significance improvement: " + str(significanceimprovement))
		log.info("Total signal efficiency: " + str(totalSE))
		log.info("Total background rejection: " + str(totalBR))
		CutInfo.write("#############\n")
		CutInfo.write("### Loop%i ###\n"%loop)
		CutInfo.write("#############\n")
		CutInfo.write("Cut method:                     %s\n"%args["FT_cut_method"])
		CutInfo.write("Cut parameter:                  %f\n"%args["FT_cut_parameter"])
		CutInfo.write("Cutting at BDT score            %f\n"%BDTScoreCut)
		CutInfo.write("Signal efficiency:              %f\n"%signaleff)
		CutInfo.write("Background rejection:           %f\n"%backgroundrej)
		CutInfo.write("Significance improvement:       %f\n"%(signaleff/math.sqrt(1.0-backgroundrej)))
		CutInfo.write("Total signal efficiency:        %f\n"%totalSE)
		CutInfo.write("Total background rejection:     %f\n"%totalBR)
		CutInfo.write("Total significance improvement: %f\n"%significanceimprovement)

	CutInfo.close()
	#copy files to remote workdir in order to have them transfered from batch system to your local storage
	if args["batch_system"]:
		for loop in range(1, args["focussed_training"]+1):
			#copy weightfiles
			for weightfile in glob.glob(os.path.join(dir_path, "Loop" + str(loop), "*weight*")):
				path, weightfilename = os.path.split(weightfile)
				shutil.copyfile(weightfile, os.path.join(dir_path, weightfilename))
			#copy rootfiles
			for rootfile in glob.glob(os.path.join(dir_path, "Loop" + str(loop), "*.root")):
				path, rootfilename = os.path.split(rootfile)
				if rootfile == "BDThistograms.root":
					shutil.copyfile(rootfile, os.path.join(dir_path, "L%i_%s"%(loop, rootfilename)))
				else:
					shutil.copyfile(rootfile, os.path.join(dir_path, rootfilename))
			#copy .C files
			for Cfile in glob.glob(os.path.join(dir_path, "Loop" + str(loop), "*.C")):
                                path, Cfilename = os.path.split(Cfile)
                                shutil.copyfile(Cfile, os.path.join(dir_path, Cfilename))
			#copy jsonfiles
			for jsonfile in glob.glob(os.path.join(dir_path, "Loop" + str(loop), "*.json")):
                                path, jsonfilename = os.path.split(jsonfile)
                                shutil.copyfile(jsonfile, os.path.join(dir_path, jsonfilename))
def do_training(args):
	info_log = copy.deepcopy(args)
	info_log["comment"] = " ".join(sys.argv)
	info_log["config_list"] = []
	info_log["variables"] = ",".join(args["quantities"])
	info_log["N-Fold"] = args["n_fold"]

	if "qcd" in (args["bkg_samples"]+args["signal_samples"]):
		log.error("qcd not possible for training")
		sys.exit()

	# create output file
	dir_path, filename = os.path.split(args["output_file"])
	filename = filename.replace(".root", "")
	info_log["training_name"] = filename
	info_log["dir_path"] = dir_path
	#getting config
	plot_configs, info_log = get_configs(args, info_log)
	#acquire splitted samples
	splits_list, stored_files_list, s_b_extension = do_splitting(args, plot_configs)
	#TMVA Stuff
	ROOT.TMVA.Tools.Instance()
	ROOT.gPluginMgr.AddHandler("TMVA@@MethodBase", ".*_FastBDT.*", "TMVA::MethodFastBDT", "TMVAFastBDT", "MethodFastBDT(TMVA::DataSetInfo&,TString)")
	ROOT.gPluginMgr.AddHandler("TMVA@@MethodBase", ".*FastBDT.*", "TMVA::MethodFastBDT", "TMVAFastBDT", "MethodFastBDT(TString&,TString&,TMVA::DataSetInfo&,TString&)")
	info_log["splits"] = splits_list

	#due to backward compatibillity: args["n_fold"] is per default 1 and Split None, if one wishes to do a non n-fold training with a specified split value:
	#set Split = desired split value, n_fold = 0 or default -> use n_fold + 1 for iterations range(n+1) = [0,...,n]
	log.info("Preparations for input samples is done, start with TMVA setup")
	for ifac in range(1,args["n_fold"]+1):
		iteration = args["n_fold"]+1 #this variable is used for iterating over the input samples it must be different from n_fold due to backward compatibility
		output = ROOT.TFile(os.path.join(dir_path, filename+"T%i.root"%ifac), "RECREATE")
		# create factory
		log.debug("TMVA.Factory(\"T%i"%ifac + "\", TFile(\"" + os.path.join(dir_path, filename+"T%i.root"%ifac) +
				"\", \"RECREATE\"), \"" + args["factory_options"] + "\")")
		ROOT.TMVA.gConfig().GetIONames().fWeightFileDir = dir_path
		factory=ROOT.TMVA.Factory("T%i"%ifac, output,
									args["factory_options"])
		# add training variables
		for variable in args["quantities"]:
			log.debug("TMVA.Factory.AddVariable(" +
						", ".join(["\"" + v + "\""
								for v in variable.split(";")]) + ")")
			var = variable.split(";")
			if len(var)==4:
				log.warning("Setting range for input variables")
				var[2] = float(var[2])
				var[3] = float(var[3])
			factory.AddVariable(*var)
		#add trees to factories
		skip = False
		if args["n_fold"] == 1: #this is for backward compatibiliy: iterate over all splits (2 splits)
			iteration += 1;
		for j,stored_file in enumerate(stored_files_list):
			for i in range(1,iteration):
				tree = ROOT.TChain()
				tree.Add(stored_file+"split%i.root/SplitTree"%(i))
				if i == ifac:
					factory.AddTree(tree, s_b_extension[j],
													1,
													ROOT.TCut(''), "test")
					log.debug("Add to Factory_%i sample %s as TestSample as %s" %(ifac, stored_file+"split%i.root/SplitTree"%(i), s_b_extension[j]))
				else:

					factory.AddTree(tree, s_b_extension[j],
													1,
													ROOT.TCut(''), "train")
					log.debug("Add to Factory_%i sample %s as TrainingsSample as %s"%(ifac, stored_file+"split%i.root/SplitTree"%(i), s_b_extension[j]))
		stitching = "stitchWeightZLL*stitchWeightZTT"
		#if 'ztt' in (args["bkg_samples"]+args['signal_samples']) and 'zll' in (args["bkg_samples"]+args['signal_samples']):
			#log.error("Due to general weight expression there can be only one of the z samples, ZTT or ZLL")
		#elif 'ztt' in (args["bkg_samples"]+args['signal_samples']):
			#stitching = "stitchWeightZTT"
		#elif 'zll' in (args["bkg_samples"]+args['signal_samples']):
			#stitching = "stitchWeightZLL"
		factory.SetBackgroundWeightExpression('eventWeight*{zstitch}*stitchWeightWJ'.format(zstitch=stitching) + (("*" + args["weight"]) if args["weight"] != "1.0" else ""))
		factory.SetSignalWeightExpression('eventWeight*{zstitch}*stitchWeightWJ'.format(zstitch=stitching) + (("*" + args["weight"]) if args["weight"] != "1.0" else ""))
		factory.PrepareTrainingAndTestTree(ROOT.TCut(''),
												ROOT.TCut(''),
												"NormMode=None:!V")
		# book methods
		for method in args["methods"]:
			log.debug("prepare method %s"%method)
			method, options = method.split(';')
			name = method + '_' + filename
			if(method == "FastBDT"):
				factory.BookMethod(ROOT.TMVA.Types.kPlugins, name, options)
			else:
				factory.BookMethod(method, name, options)
			log.debug("TMVA.Factory.BookMethod(" + ", ".join(
				["\"" + m + "\"" for m in (method, name, options)]) + ")")
		#perform full training
		log.debug("TMVA.Factory.TrainAllMethods()")
		#import pdb
		#pdb.set_trace()
		factory.TrainAllMethods()

		log.debug("TMVA.Factory.TestAllMethods()")
		factory.TestAllMethods()

		log.debug("TMVA.Factory.EvaluateAllMethods()")
		factory.EvaluateAllMethods()

		# finish
		output.Close()
		del factory
		log.info("Training output is written to \"" + os.path.join(dir_path, filename+"T%i.root"%ifac) + "\".")
	log_log = jsonTools.JsonDict(info_log)
	log_log.save(os.path.join(dir_path,"%s_TrainingLog.json"%filename), indent=4)


if __name__ == "__main__":

	parser = argparse.ArgumentParser(description="Train BDTs using TMVA interface.",
									 parents=[logger.loggingParser])

	parser.add_argument("-i", "--input-dir", required=True,
						help="Input directory.")
	parser.add_argument("-s", "--signal-samples", nargs="+",
						default=["ggh", "qqh", "vh"],
						choices=["ggh", "qqh", "vh", "ztt", "zll", "ttj", "vv", "wj"],
						help="Signal-Samples. [Default: %(default)s]")
	parser.add_argument("-b", "--bkg-samples", nargs="+",
						default=["ztt", "zll", "ttj", "vv", "wj"],
						choices=["ztt", "zll", "ttj", "vv", "wj", "qcd", "ggh", "qqh", "vh", "samesigndata"],
						help="Bkg-Samples. [Default: %(default)s]")
	parser.add_argument("-c", "--channels", nargs="*",
						default=["tt", "mt", "et", "em", "mm", "ee"],
						help="Channels. [Default: %(default)s]")
	parser.add_argument("-C", "--custom-splitting", nargs="+",
						default=[],
						help="use custom splitting for N-Fold. [Default: %(default)s]")
	parser.add_argument("-x", "--quantities", nargs="+",
						default=["pVecSum;F", "pt_1;F", "mt_1;F", "pt_2;F", "mt_2;F",
								"mvamet;F", "pZetaMissVis;F","njets;I",
								"lep1_centrality;F","lep2_centrality;F",
								"delta_lep_centrality;F", "pScalSum;F", "H_pt;F", "ptvis;F",
								"diLep_centrality;F", "diLep_diJet_deltaR;F"],
						help="Quantities to train on.  [Default: %(default)s]")
	parser.add_argument("--lumi", type=float, default=samples.default_lumi/1000.0,
						help="""Luminosity for the given data in fb^(-1).
								[Default: %(default)s]""")
	parser.add_argument("--category", type=str, default=None,
						help="""Category for sample selection.
								[Default: %(default)s]""")
	parser.add_argument("-w", "--weight", default="1.0",
						help="""Additional weight (cut) expression.
						[Default: %(default)s]""")
	parser.add_argument("-e", "--exclude-cuts", nargs="+",
						default=[],
						choices=["pzeta", "pZetaMiss", "pZetaVis", "iso_1", "iso_2", "mt_1", "mt_2", "mt"],
						help="""Exclude (default) selection cuts.
						[Default: %(default)s]""")
	parser.add_argument("--higgs-masses", nargs="+", default=["125"],
						help="Higgs masses. [Default: %(default)s]")
	parser.add_argument("-S", "--Split", default=None,
						help="""If set enables splitting into training and test
						tree, use value between 0 and 99 to split tree using
						variable TrainingSelectionValue. [Default: %(default)s]""")
	parser.add_argument("-o", "--output-file",required=False,
						default=None,
						help="Output file. [Default: %(default)s]")
	parser.add_argument("--factory-options", default="",
						help="Options for TMVA.Factory constructor. [Default: %(default)s]")
	parser.add_argument("-m", "--methods", nargs="+", default=['BDT;nCuts=1200:NTrees=1250:MinNodeSize=0.25:BoostType=Grad:Shrinkage=0.2'],
						help="MVA methods. Multiple arguments for TMVA.Factory.BookMethod are split by semicolon. Format: name;options. [Default: %(default)s]")
	parser.add_argument("--preparation-trees-options", default="",
						help="Options for preparation of inputs trees as passed to TMVA.Factory.PrepareTrainingAndTestTree. [Default: %(default)s]")
	parser.add_argument("-n", "--n-fold", type=int, default=1,
						help="number of n for n-fold training. 1 is regular splitting according to --Split. [Default: %(default)s]")
	parser.add_argument("-p", "--pre-selection", default = "(1.0)",
						help="preselection for event selection [Default: %(default)s)")
	parser.add_argument("--modify", default = False, action="store_true",
						help="""if used: mode switches to predefined scans. please change according to your needs: ~line 280 and beyond""")
	parser.add_argument("--modification", default = 0, nargs="+", type=int,
						help="""if modify is used: select modification code by number""")
	parser.add_argument("-j", "--j", default = 1,
						help="number of parallel processes for training [Default: %(default)s]")
	parser.add_argument("--batch-system", default = False, action="store_true",
						help="specifiy if tmvaWrapper will be used with batch jobs, this will change output_path accordingly [Default: %(default)s]")
	parser.add_argument("--config-number", type = int, default = 0,
						help="select wich config to be processeed by this job, only used for batch-jobs [Default: %(default)s]")
	parser.add_argument("--config-step", type = int, default = -1,
						help="Process every nth config on one batch-node [Default: %(default)s]")
	parser.add_argument("--dry-run", default = False, action="store_true",
						help="number of parallel processes for training, only used for local jobs [Default: %(default)s]")
	parser.add_argument("-f", "--focussed-training", type=int, default=1,
						help="number of loops for focussed training. 1 is regular training. [Default: %(default)s]")
	parser.add_argument("--FT-cut-method", default="bargaining",
                                                help="Method to cut as specified in 'GetFocussedTrainingCut.py'. [Default: %(default)s]")
	parser.add_argument("--FT-cut-parameter", type=float, default=2.0,
                                                help="Parameter used by the selected cut method. [Default: %(default)s]")


	cargs = parser.parse_args()
	logger.initLogger(cargs)
	cargs_values = vars(cargs)
	#=====If jobs are to run on batch-system, the ouputpath must be adjusted this is done below in if, elif
	if cargs.output_file == None:
		cargs.output_file = os.getcwd()
	if cargs.batch_system:
		dir_path, filename = os.path.split(cargs.output_file)
		cargs.output_file = os.path.join(os.getcwd(), filename)
	#=====here starts predefined code for scans and collection of signal background combinations
	if cargs.modify:
		cargs.output_file = os.getcwd()
		config_list = []
		if 1 in cargs.modification:
			for i in range(500,2500,100):
				#=======This is a very basic scan of NTrees
				copy_cargs = copy.deepcopy(cargs_values)
				copy_cargs["methods"] = ["BDT;nCuts=1200:NTrees={0}:MinNodeSize=0.25:BoostType=Grad:Shrinkage=0.2".format(i)]
				copy_cargs["output_file"] = cargs_values["output_file"].format(i)
				config_list.append(copy_cargs)

		if 2 in cargs.modification:
			for j in range(2,6):
				for i in range(750, 2751, 250):
					for samps in [(['ggh', 'qqh', 'vh'], ["ztt", "zll", "ttj", "vv", "wj"])]:
					#, (['qqh'], ["ztt", "zll", "ttj", "vv", "wj"])]:
						#=======This is a very basic collection of possible signal background combinations
						copy_cargs = copy.deepcopy(cargs_values)
						copy_cargs["signal_samples"] = samps[0]
						copy_cargs["bkg_samples"] = samps[1]
						front = ''
						back = ''
						fill = '_{0}_'
						if len(samps[0]) > 1:
							front = "{fold}_".format(fold=j) + 'xxh'
						else:
							front = "{fold}_".format(fold=j) + samps[0][0]
						if len(samps[1]) > 1:
							back = 'all'
						else:
							back = samps[1][0]
						copy_cargs["output_file"] = os.path.join(copy_cargs["output_file"], front + fill + back).format(i)
						copy_cargs["methods"] = ["BDT;nCuts=1200:NTrees={0}:MinNodeSize=0.25:BoostType=Grad:Shrinkage=0.2".format(i)]
						copy_cargs["n_fold"] = j
						config_list.append(copy.deepcopy(copy_cargs))
						copy_cargs["quantities"].append("m_vis")
						copy_cargs["output_file"] += "_m_vis"
						config_list.append(copy_cargs)
				for i in range(100, 501, 200)+range(750, 1501, 250):
					samps = ['qqh', 'ggh']
					#=======This is a very basic collection of possible signal background combinations
					copy_cargs = copy.deepcopy(cargs_values)
					copy_cargs["signal_samples"] = [samps[0]]
					copy_cargs["bkg_samples"] = [samps[1]]
					front = "{fold}_".format(fold=j)+samps[0]
					back = samps[1]
					fill = '_{i}_'
					copy_cargs["output_file"] = os.path.join(copy_cargs["output_file"], front + fill + back).format(i=i)
					copy_cargs["methods"] = ["BDT;nCuts=1200:NTrees={i}:MinNodeSize=0.25:BoostType=Grad:Shrinkage=0.1".format(i=i)]
					copy_cargs["n_fold"] = j
					copy_cargs["quantities"].append("jdeta")
					copy_cargs["quantities"].append("mjj")
					config_list.append(copy.deepcopy(copy_cargs))
					copy_cargs["quantities"].append("m_vis")
					copy_cargs["output_file"] += "_m_vis"
					config_list.append(copy_cargs)
		if 3 in cargs.modification:
			for i in range(4,9,1):
				copy_cargs = copy.deepcopy(cargs_values)
				copy_cargs["output_file"] = os.path.join(copy_cargs["output_file"], "all_{0}_all".format(i))
				copy_cargs["methods"] = ["BDT;nCuts=1200:NTrees=1500:MinNodeSize=0.25:BoostType=Grad:Shrinkage=1:MaxDepth={0}".format(i)]
				config_list.append(copy_cargs)

		if 4 in cargs.modification:
			for i in range(1,11):
				copy_cargs = copy.deepcopy(cargs_values)
				copy_path = copy_cargs["output_file"]
				splits_list = []
				part_size = 100./(2*i)
				for n in range(2*i):
					splits_list.append("(TrainingSelectionValue>=%i)*(TrainingSelectionValue<%i)"%(int(n*part_size),int((n+1)*part_size)))
				copy_cargs["custom_splitting"].append("||".join(splits_list[::2]))
				copy_cargs["custom_splitting"].append("||".join(splits_list[1::2]))
				print copy_cargs["custom_splitting"]
				copy_cargs["signal_samples"] = ['ggh', 'qqh', 'vh']
				copy_cargs["bkg_samples"] = ["ztt", "zll", "ttj", "vv", "wj"]
				copy_cargs["output_file"] = os.path.join(copy_path, "reg_{i}").format(i=i)
				#copy_cargs["methods"] = ["BDT;nCuts=1200:NTrees={i}:MinNodeSize=0.25:BoostType=Grad:Shrinkage=0.1".format(i=1500)]
				copy_cargs["methods"] = ["FastBDT;H:V:NTrees={i}:Shrinkage=0.1:RandRatio=0.5:NTreeLayers=3:NCutLevel=10:useWeightedFeatureBinning=true:transform2probability=false".format(i=1500)]
				copy_cargs["n_fold"] = 2
				config_list.append(copy.deepcopy(copy_cargs))

				copy_cargs["signal_samples"] = ['qqh']
				copy_cargs["bkg_samples"] = ["ggh"]
				copy_cargs["output_file"] = os.path.join(copy_path, "vbf_{i}").format(i=i)
				#copy_cargs["methods"] = ["BDT;nCuts=1200:NTrees={i}:MinNodeSize=0.25:BoostType=Grad:Shrinkage=0.1".format(i=50)]
				copy_cargs["methods"] = ["FastBDT;H:V:NTrees={i}:Shrinkage=0.1:RandRatio=0.5:NTreeLayers=3:NCutLevel=10:useWeightedFeatureBinning=true:transform2probability=false".format(i=50)]
				copy_cargs["quantities"].append("jdeta")
				copy_cargs["quantities"].append("mjj")
				config_list.append(copy.deepcopy(copy_cargs))
		if 5 in cargs.modification:
			"BDT;nCuts=1200:NTrees=1500:MinNodeSize=2.5:BoostType=Grad:Shrinkage=0.1:MaxDepth=3:SeparationType=SDivSqrtSPlusB"
			copy_cargs = copy.deepcopy(cargs_values)
			copy_cargs["methods"] = ["BDT;nCuts=1200:NTrees=750:MinNodeSize=2.5:BoostType=Grad:Shrinkage=0.1:MaxDepth=3:SeparationType=SDivSqrtSPlusB"]
			copy_cargs["n_fold"] = 2
			copy_path = copy_cargs["output_file"]
			for channel in ["em", "et", "mt"]:
				copy_cargs["signal_samples"] = ["ggh", "qqh"]
				copy_cargs["channels"] = [channel]
				for jets in [2]:
					copy_cargs["bkg_samples"] = ["ztt"]
					copy_cargs["pre_selection"] = "(njetspt30==%i)"%jets

					if jets == 2:
						copy_cargs["signal_samples"] = ["qqh"]
						copy_cargs["pre_selection"] = "(njetspt30>=%i)"%jets
						if channel == "em":
							copy_cargs["quantities"] = ["pt_1", "mt_1", "pt_2", "mt_2", "mvamet", "pZetaMissVis", "H_pt", "ptvis", "pt_sv", "pt_sv*cosh(eta_sv);F;0;2000", "diLepDeltaR", "diLepJet1DeltaR", "diLep_centrality", "diLep_diJet_deltaR", "mjj", "jdeta", "product_lep_centrality", "diLepJet1DeltaR"]
						if channel == "et":
							copy_cargs["quantities"] = ["pt_1", "mt_1", "pt_2", "mt_2", "mvamet", "pZetaMissVis", "H_pt", "ptvis", "pt_sv", "pt_sv*cosh(eta_sv);F;0;2000", "diLepDeltaR", "diLepJet1DeltaR", "diLep_centrality", "diLep_diJet_deltaR", "mjj", "jdeta", "product_lep_centrality", "diLepJet1DeltaR"]
						if channel == "mt":
							copy_cargs["quantities"] = ["pt_1", "mt_1", "pt_2", "mt_2", "mvamet", "pZetaMissVis", "H_pt", "ptvis", "pt_sv", "pt_sv*cosh(eta_sv);F;0;2000", "diLepDeltaR", "diLepJet1DeltaR", "diLep_centrality", "diLep_diJet_deltaR", "mjj", "jdeta", "product_lep_centrality", "diLepJet1DeltaR"]

						for counter in range(len(copy_cargs["quantities"])):
							poped = copy_cargs["quantities"].pop(0)
							poped_name = poped
							if "*" in poped:
								poped_name = "function"
							copy_cargs["output_file"] = os.path.join(copy_path,"%s_%iJets_Cat1_rm_%s"%(channel,jets,poped_name))
							config_list.append(copy.deepcopy(copy_cargs))
							copy_cargs["quantities"].append(poped)

						if channel == "em":
							copy_cargs["quantities"] = ["pt_1", "mt_1", "pt_2", "mt_2", "mvamet", "pZetaMissVis", "H_pt", "ptvis", "pt_sv", "pt_sv*cosh(eta_sv);F;0;2000", "diLepDeltaR", "diLepJet1DeltaR", "diLep_centrality", "diLep_diJet_deltaR", "mjj", "jdeta", "product_lep_centrality", "diLepJet1DeltaR"]
						if channel == "et":
							copy_cargs["quantities"] = ["pt_1", "mt_1", "pt_2", "mt_2", "mvamet", "pZetaMissVis", "H_pt", "ptvis", "pt_sv", "pt_sv*cosh(eta_sv);F;0;2000", "diLepDeltaR", "diLepJet1DeltaR", "diLep_centrality", "diLep_diJet_deltaR", "mjj", "jdeta", "product_lep_centrality", "diLepJet1DeltaR"]
						if channel == "mt":
							copy_cargs["quantities"] = ["pt_1", "mt_1", "pt_2", "mt_2", "mvamet", "pZetaMissVis", "H_pt", "ptvis", "pt_sv", "pt_sv*cosh(eta_sv);F;0;2000", "diLepDeltaR", "diLepJet1DeltaR", "diLep_centrality", "diLep_diJet_deltaR", "mjj", "jdeta", "product_lep_centrality", "diLepJet1DeltaR"]

						for counter in range(len(copy_cargs["quantities"])):
							poped = copy_cargs["quantities"].pop(0)
							poped_name = poped
							if "*" in poped:
								poped_name = "function"
							copy_cargs["output_file"] = os.path.join(copy_path,"%s_%iJets_Cat2_rm_%s"%(channel,jets,poped_name))
							copy_cargs["bkg_samples"] = ["ttj", "wj", "vv"]
							config_list.append(copy.deepcopy(copy_cargs))
							copy_cargs["quantities"].append(poped)

					if jets == 1:
						if channel == "em":
							copy_cargs["quantities"] = ["mt_1", "pt_2", "H_pt", "diLepDeltaR", "diLepJet1DeltaR"]
						if channel == "et":
							#continue
							copy_cargs["quantities"] = ["pt_2", "pt_sv", "diLepDeltaR", "diLepJet1DeltaR"]
						if channel == "mt":
							#continue
							copy_cargs["quantities"] = ["pt_1", "pt_2", "H_pt", "diLepDeltaR", "diLepJet1DeltaR"]
						for counter in range(len(copy_cargs["quantities"])):
							poped = copy_cargs["quantities"].pop(0)
							poped_name = poped
							if "*" in poped:
								poped_name = "function"
							copy_cargs["output_file"] = os.path.join(copy_path,"%s_%iJets_Cat1_rm_%s"%(channel,jets,poped_name))
							config_list.append(copy.deepcopy(copy_cargs))
							copy_cargs["quantities"].append(poped)
						copy_cargs["bkg_samples"] = ["wj", "zll"]
						if channel == "em":
							copy_cargs["quantities"] = ["mt_1", "pt_2", "mt_2", "pZetaMissVis", "diLepDeltaR", "diLepJet1DeltaR"]
							copy_cargs["bkg_samples"] = ["ttj", "vv"]
						if channel == "et":
							copy_cargs["quantities"] = ["pt_2", "mvamet",  "diLepDeltaR", "diLepJet1DeltaR"]
							#continue
						if channel == "mt":
							copy_cargs["quantities"] = ["mt_2", "pZetaMissVis", "ptvis", "diLepDeltaR"]
							#continue
						for counter in range(len(copy_cargs["quantities"])):
							poped = copy_cargs["quantities"].pop(0)
							poped_name = poped
							if "*" in poped:
								poped_name = "function"
							copy_cargs["output_file"] = os.path.join(copy_path,"%s_%iJets_Cat2_rm_%s"%(channel,jets,poped_name))
							config_list.append(copy.deepcopy(copy_cargs))
							copy_cargs["quantities"].append(poped)

					if jets == 0:
						if channel == "em":
							copy_cargs["quantities"] = ["pt_1", "pt_2", "H_pt"]
						if channel == "et":
							copy_cargs["quantities"] = ["pt_1", "pt_2", "mt_2", "diLepDeltaR"]
						if channel == "mt":
							copy_cargs["quantities"] = ["pt_1", "pt_2", "mt_2", "H_pt",  "diLepDeltaR"]
						for counter in range(len(copy_cargs["quantities"])):
							poped = copy_cargs["quantities"].pop(0)
							poped_name = poped
							if "*" in poped:
								poped_name = "function"
							copy_cargs["output_file"] = os.path.join(copy_path,"%s_%iJets_Cat1_rm_%s"%(channel,jets,poped_name))
							config_list.append(copy.deepcopy(copy_cargs))
							copy_cargs["quantities"].append(poped)
						if channel in ["et", "mt"]:
							if channel == "et":
								copy_cargs["quantities"] = ["pt_1", "pt_2", "mvamet"]
							if channel == "mt":
								copy_cargs["quantities"] = ["pt_1", "pt_2", "mvamet", "pZetaMissVis"]
							copy_cargs["bkg_samples"] = ["wj", "zll"]
							for counter in range(len(copy_cargs["quantities"])):
								poped = copy_cargs["quantities"].pop(0)
								poped_name = poped
								if "*" in poped:
									poped_name = "function"
								copy_cargs["output_file"] = os.path.join(copy_path,"%s_%iJets_Cat2_rm_%s"%(channel,jets,poped_name))
								config_list.append(copy.deepcopy(copy_cargs))
								copy_cargs["quantities"].append(poped)
		if 6 in cargs.modification:
			#Full set of variables
			copy_cargs = copy.deepcopy(cargs_values)
			copy_cargs["methods"] = ["BDT;nCuts=1000:NTrees=750:MinNodeSize=2.5:BoostType=Grad:Shrinkage=0.1:MaxDepth=3:SeparationType=GiniIndex"]
			copy_cargs["n_fold"] = 2
			copy_path = copy_cargs["output_file"]
			for channel in ["em", "et", "mt"]:
				copy_cargs["signal_samples"] = ["ggh"]
				copy_cargs["channels"] = [channel]
				for jets in [0,1,2]:
					copy_cargs["bkg_samples"] = ["ztt"]
					copy_cargs["pre_selection"] = "(njetspt30==%i)"%jets
					if jets == 2:
						copy_cargs["signal_samples"] = ["qqh"]
						copy_cargs["pre_selection"] = "(njetspt30>=%i)"%jets
						copy_cargs["quantities"] = ["pt_1", "mt_1", "pt_2", "mt_2", "mvamet", "pZetaMissVis", "H_pt", "diLepDeltaR", "diLepJet1DeltaR", "diLep_diJet_deltaR", "mjj", "jdeta"]
						copy_cargs["output_file"] = os.path.join(copy_path,"%s_%iJets_Cat1_rm_%s"%(channel,jets,"Nothing"))
						config_list.append(copy.deepcopy(copy_cargs))
						copy_cargs["output_file"] = os.path.join(copy_path,"%s_%iJets_Cat2_rm_%s"%(channel,jets,"Nothing"))
						#copy_cargs["bkg_samples"] = ["ttj", "wj", "vv"]
						copy_cargs["bkg_samples"] = ["zll", "ttj", "wj", "vv"]
						config_list.append(copy.deepcopy(copy_cargs))
					if jets == 1:
						copy_cargs["quantities"] = ["pt_1", "mt_1", "pt_2", "mt_2", "mvamet", "pZetaMissVis", "H_pt", "diLepDeltaR", "diLepJet1DeltaR"]
						copy_cargs["output_file"] = os.path.join(copy_path,"%s_%iJets_Cat1_rm_%s"%(channel,jets,"Nothing"))
						config_list.append(copy.deepcopy(copy_cargs))
						#copy_cargs["bkg_samples"] = ["wj", "zll"]
						copy_cargs["bkg_samples"] = ["zll", "ttj", "wj", "vv"]
						#if channel == "em":
							#copy_cargs["bkg_samples"] = ["ttj", "vv"]
						copy_cargs["output_file"] = os.path.join(copy_path,"%s_%iJets_Cat2_rm_%s"%(channel,jets,"Nothing"))
						config_list.append(copy.deepcopy(copy_cargs))
					if jets == 0:
						copy_cargs["quantities"] = ["pt_1", "mt_1", "pt_2", "mt_2", "mvamet", "pZetaMissVis", "H_pt", "diLepDeltaR"]
						copy_cargs["output_file"] = os.path.join(copy_path,"%s_%iJets_Cat1_rm_%s"%(channel,jets,"Nothing"))
						config_list.append(copy.deepcopy(copy_cargs))
						#if channel == "em":
							#continue
						#copy_cargs["bkg_samples"] = ["wj", "zll"]
						copy_cargs["bkg_samples"] = ["zll", "ttj", "wj", "vv"]
						copy_cargs["output_file"] = os.path.join(copy_path,"%s_%iJets_Cat2_rm_%s"%(channel,jets,"Nothing"))
						config_list.append(copy.deepcopy(copy_cargs))
		if 7 in cargs.modification:
			#Final Set of Variables
			copy_cargs = copy.deepcopy(cargs_values)
			copy_cargs["methods"] = ["BDT;nCuts=1000:NTrees=750:MinNodeSize=2.5:BoostType=Grad:Shrinkage=0.1:MaxDepth=3:SeparationType=GiniIndex"]
			copy_cargs["n_fold"] = 2
			copy_path = copy_cargs["output_file"]
			for channel in ["em", "et", "mt"]:
				copy_cargs["signal_samples"] = ["ggh"]
				copy_cargs["channels"] = [channel]
				for jets in [0,1,2]:
					copy_cargs["bkg_samples"] = ["ztt"]
					copy_cargs["pre_selection"] = "(njetspt30==%i)"%jets
					if jets == 2:
						copy_cargs["signal_samples"] = ["qqh"]
						copy_cargs["pre_selection"] = "(njetspt30>=%i)"%jets
						copy_cargs["quantities"] = ["pt_1", "mt_1", "pt_2", "mt_2", "mvamet", "pZetaMissVis", "H_pt", "diLepDeltaR", "diLepJet1DeltaR", "diLep_diJet_deltaR", "mjj", "jdeta"]

						if channel == "em":
							copy_cargs["quantities"] = ["mt_1", "pt_1", "H_pt", "diLepDeltaR", "diLep_diJet_deltaR", "mjj", "jdeta"]
						if channel in ["et", "mt"]:
							copy_cargs["quantities"] = ["pt_1", "pt_2", "mt_2", "H_pt", "diLepDeltaR", "mjj", "jdeta", "diLep_diJet_deltaR"]
							#copy_cargs["quantities"] = ["pt_1", "pt_2", "mt_2", "H_pt", "diLepDeltaR", "diLep_diJet_deltaR", "mjj", "jdeta", "diLepJet1DeltaR"]

						copy_cargs["output_file"] = os.path.join(copy_path,"%s_%iJets_Cat1_rm_%s"%(channel,jets,"Nothing"))
						config_list.append(copy.deepcopy(copy_cargs))
						copy_cargs["bkg_samples"] = ["zll", "ttj", "wj", "vv"]

						if channel == "em":
							copy_cargs["quantities"] = ["mt_1", "mt_2", "pZetaMissVis", "mjj", "H_pt", "jdeta", "diLep_diJet_deltaR"]
						if channel in ["et", "mt"]:
							copy_cargs["quantities"] = ["mt_1", "pt_2", "mt_2", "diLepDeltaR", "diLep_diJet_deltaR", "mjj", "jdeta"]

						copy_cargs["output_file"] = os.path.join(copy_path,"%s_%iJets_Cat2_rm_%s"%(channel,jets,"Nothing"))
						config_list.append(copy.deepcopy(copy_cargs))

					if jets == 1:
						copy_cargs["quantities"] = ["pt_1", "mt_1", "pt_2", "mt_2", "mvamet", "pZetaMissVis", "H_pt", "diLepDeltaR", "diLepJet1DeltaR"]

						if channel == "em":
							copy_cargs["quantities"] = ["pt_1", "mt_1", "pt_2", "H_pt", "diLepDeltaR", "diLepJet1DeltaR"]
						if channel in ["et", "mt"]:
							copy_cargs["quantities"] = ["pt_1", "mt_1", "pt_2", "H_pt", "diLepDeltaR", "diLepJet1DeltaR"]

						copy_cargs["output_file"] = os.path.join(copy_path,"%s_%iJets_Cat1_rm_%s"%(channel,jets,"Nothing"))
						config_list.append(copy.deepcopy(copy_cargs))
						#copy_cargs["bkg_samples"] = ["wj", "zll"]
						copy_cargs["bkg_samples"] = ["zll", "ttj", "wj", "vv"]

						if channel == "em":
							#copy_cargs["bkg_samples"] = ["ttj", "vv"]
							copy_cargs["quantities"] = ["pt_1", "pt_2", "H_pt", "mt_1", "mt_2", "pZetaMissVis"]
						if channel in ["et", "mt"]:
							#copy_cargs["bkg_samples"] = ["wj", "zll"]
							copy_cargs["quantities"] = ["pt_1", "pt_2", "mt_1", "mvamet", "pZetaMissVis", "diLepDeltaR"]


						copy_cargs["output_file"] = os.path.join(copy_path,"%s_%iJets_Cat2_rm_%s"%(channel,jets,"Nothing"))
						config_list.append(copy.deepcopy(copy_cargs))

					if jets == 0:
						copy_cargs["quantities"] = ["pt_1", "mt_1", "pt_2", "mt_2", "mvamet", "pZetaMissVis", "H_pt", "diLepDeltaR"]

						if channel == "em":
							copy_cargs["quantities"] = ["pt_1", "pt_2", "diLepDeltaR", "H_pt", "pZetaMissVis", "mt_1"]
						if channel in ["et", "mt"]:
							copy_cargs["quantities"] = ["pt_1", "pt_2", "mt_2", "H_pt", "diLepDeltaR", "mvamet"]

						copy_cargs["output_file"] = os.path.join(copy_path,"%s_%iJets_Cat1_rm_%s"%(channel,jets,"Nothing"))
						config_list.append(copy.deepcopy(copy_cargs))

						if channel == "em":
							#continue
							copy_cargs["quantities"] = ["pt_1", "pt_2", "diLepDeltaR", "H_pt", "pZetaMissVis", "mt_2"]
						if channel in ["et", "mt"]:
							copy_cargs["quantities"] = ["pt_1", "pt_2", "mt_1", "mvamet", "pZetaMissVis", "diLepDeltaR"]

						#copy_cargs["bkg_samples"] = ["wj", "zll"]
						copy_cargs["bkg_samples"] = ["zll", "ttj", "wj", "vv"]
						copy_cargs["output_file"] = os.path.join(copy_path,"%s_%iJets_Cat2_rm_%s"%(channel,jets,"Nothing"))
						config_list.append(copy.deepcopy(copy_cargs))

		if 10 in cargs.modification:
			"BDT;nCuts=1200:NTrees=1500:MinNodeSize=2.5:BoostType=Grad:Shrinkage=0.1:MaxDepth=3:SeparationType=SDivSqrtSPlusB"
			copy_cargs = copy.deepcopy(cargs_values)
			copy_cargs["methods"] = ["BDT;nCuts=1200:NTrees=750:MinNodeSize=2.5:BoostType=Grad:Shrinkage=0.1:MaxDepth=3:SeparationType=SDivSqrtSPlusB"]
			copy_cargs["n_fold"] = 2
			copy_cargs["signal_samples"] = ["ggh", "qqh"]
			copy_path = copy_cargs["output_file"]
			for channel in ["em", "et", "mt"]:
				jets = 0
				copy_cargs["channels"] = [channel]
				copy_cargs["bkg_samples"] = ["ztt"]
				copy_cargs["pre_selection"] = "(njetspt30==%i)"%jets
				if channel == "em":
					copy_cargs["quantities"] = ["pt_1", "pt_2", "mvamet"]
				if channel == "et":
					copy_cargs["quantities"] = ["pt_1", "pt_2", "mt_2", "diLepDeltaR"]
				if channel == "mt":
					copy_cargs["quantities"] = ["pt_1", "pt_2", "mt_2", "diLepDeltaR"]
				for counter in range(len(copy_cargs["quantities"])):
					poped = copy_cargs["quantities"].pop(0)
					poped_name = poped
					if "*" in poped:
						poped_name = "function"
					copy_cargs["output_file"] = os.path.join(copy_path,"%s_%iJets_Cat1_rm_%s"%(channel,jets,poped_name))
					config_list.append(copy.deepcopy(copy_cargs))
					copy_cargs["quantities"].append(poped)
				if channel in ["et", "mt"]:
					if channel == "et":
						copy_cargs["quantities"] = ["pt_1", "pt_2", "pZetaMissVis", "diLepDeltaR"]
					if channel == "mt":
						copy_cargs["quantities"] = ["pt_2", "mvamet", "pZetaMissVis"]
					copy_cargs["bkg_samples"] = ["wj", "zll"]
					for counter in range(len(copy_cargs["quantities"])):
						poped = copy_cargs["quantities"].pop(0)
						poped_name = poped
						if "*" in poped:
							poped_name = "function"
						copy_cargs["output_file"] = os.path.join(copy_path,"%s_%iJets_Cat2_rm_%s"%(channel,jets,poped_name))
						config_list.append(copy.deepcopy(copy_cargs))
						copy_cargs["quantities"].append(poped)
		if 11 in cargs.modification:
			"BDT;nCuts=1200:NTrees=1500:MinNodeSize=2.5:BoostType=Grad:Shrinkage=0.1:MaxDepth=3:SeparationType=SDivSqrtSPlusB"
			copy_cargs = copy.deepcopy(cargs_values)
			copy_cargs["methods"] = ["BDT;nCuts=1200:NTrees=750:MinNodeSize=2.5:BoostType=Grad:Shrinkage=0.1:MaxDepth=3:SeparationType=SDivSqrtSPlusB"]
			copy_cargs["n_fold"] = 2
			copy_cargs["signal_samples"] = ["ggh", "qqh"]
			copy_path = copy_cargs["output_file"]
			for channel in ["em", "et", "mt"]:
				jets = 1
				copy_cargs["channels"] = [channel]
				copy_cargs["bkg_samples"] = ["ztt"]
				copy_cargs["pre_selection"] = "(njetspt30==%i)"%jets
				if channel == "em":
					copy_cargs["quantities"] = ["H_pt", "diLepDeltaR", "diLepJet1DeltaR"]
				if channel == "et":
					#continue
					copy_cargs["quantities"] = ["pt_2", "mt_2", "pt_sv", "diLepDeltaR", "diLepJet1DeltaR"]
				if channel == "mt":
					#continue
					copy_cargs["quantities"] = ["pt_2", "pt_sv", "diLepDeltaR"]
				for counter in range(len(copy_cargs["quantities"])):
					poped = copy_cargs["quantities"].pop(0)
					poped_name = poped
					if "*" in poped:
						poped_name = "function"
					copy_cargs["output_file"] = os.path.join(copy_path,"%s_%iJets_Cat1_rm_%s"%(channel,jets,poped_name))
					config_list.append(copy.deepcopy(copy_cargs))
					copy_cargs["quantities"].append(poped)
				copy_cargs["bkg_samples"] = ["wj", "zll"]
				if channel == "em":
					copy_cargs["quantities"] = ["mt_1", "pt_2", "mt_2", "pt_sv", "diLepDeltaR"]
					copy_cargs["bkg_samples"] = ["ttj", "vv"]
				if channel == "et":
					copy_cargs["quantities"] = ["pt_1", "pt_2", "mvamet", "pZetaMissVis"]
					#continue
				if channel == "mt":
					copy_cargs["quantities"] = ["pt_2", "mvamet"]
					#continue
				for counter in range(len(copy_cargs["quantities"])):
					poped = copy_cargs["quantities"].pop(0)
					poped_name = poped
					if "*" in poped:
						poped_name = "function"
					copy_cargs["output_file"] = os.path.join(copy_path,"%s_%iJets_Cat2_rm_%s"%(channel,jets,poped_name))
					config_list.append(copy.deepcopy(copy_cargs))
					copy_cargs["quantities"].append(poped)
		if 12 in cargs.modification:
			"BDT;nCuts=1200:NTrees=1500:MinNodeSize=2.5:BoostType=Grad:Shrinkage=0.1:MaxDepth=3:SeparationType=SDivSqrtSPlusB"
			copy_cargs = copy.deepcopy(cargs_values)
			copy_cargs["methods"] = ["BDT;nCuts=1200:NTrees=750:MinNodeSize=2.5:BoostType=Grad:Shrinkage=0.1:MaxDepth=3:SeparationType=SDivSqrtSPlusB"]
			copy_cargs["n_fold"] = 2
			copy_path = copy_cargs["output_file"]
			copy_cargs["signal_samples"] = ["qqh"]
			for channel in ["em", "et", "mt"]:
				jets = 2
				copy_cargs["channels"] = [channel]
				copy_cargs["bkg_samples"] = ["ztt"]
				copy_cargs["pre_selection"] = "(njetspt30==%i)"%jets
				if channel == "em":
					copy_cargs["quantities"] = ["H_pt", "diLepDeltaR", "diLep_diJet_deltaR", "mjj", "jdeta", "product_lep_centrality"]
				if channel == "et":
					copy_cargs["quantities"] = ["pt_2", "H_pt", "diLepDeltaR", "diLep_diJet_deltaR", "mjj", "jdeta"]
				if channel == "mt":
					copy_cargs["quantities"] = ["pt_1", "pt_2", "mt_2", "H_pt", "diLepDeltaR", "diLep_centrality", "diLep_diJet_deltaR", "mjj", "jdeta"]

				for counter in range(len(copy_cargs["quantities"])):
					poped = copy_cargs["quantities"].pop(0)
					poped_name = poped
					if "*" in poped:
						poped_name = "function"
					copy_cargs["output_file"] = os.path.join(copy_path,"%s_%iJets_Cat1_rm_%s"%(channel,jets,poped_name))
					config_list.append(copy.deepcopy(copy_cargs))
					copy_cargs["quantities"].append(poped)

				if channel == "em":
					copy_cargs["quantities"] = ["pZetaMissVis", "pt_sv", "diLep_centrality", "mjj", "product_lep_centrality"]
				if channel == "et":
					copy_cargs["quantities"] = ["mt_1", "pt_2", "mt_2", "mvamet", "diLepDeltaR", "diLep_diJet_deltaR", "jdeta", "product_lep_centrality"]
				if channel == "mt":
					copy_cargs["quantities"] = ["pt_1", "mt_1", "pt_2", "mt_2", "mvamet", "jdeta", "product_lep_centrality"]

				for counter in range(len(copy_cargs["quantities"])):
					poped = copy_cargs["quantities"].pop(0)
					poped_name = poped
					if "*" in poped:
						poped_name = "function"
					copy_cargs["output_file"] = os.path.join(copy_path,"%s_%iJets_Cat2_rm_%s"%(channel,jets,poped_name))
					copy_cargs["bkg_samples"] = ["ttj", "wj", "vv"]
					config_list.append(copy.deepcopy(copy_cargs))
					copy_cargs["quantities"].append(poped)
		if cargs.batch_system:
			log.info("Start training of BDT config number %i"%cargs.config_number)
			if cargs.dry_run and cargs.config_step < 1:
				log.info("Dry-Run: aborting training")
				jsonTools.JsonDict(config_list[cargs.config_number]).save("TrainingConfigs.config", indent = 4)
				log.info("TrainingConfigs[%i] saved to TrainingConfigs.config"%cargs.config_number)
				log.info(config_list[cargs.config_number])
				sys.exit()
			if cargs.config_number > len(config_list):
				log.error("config_number is greater than length of config_list, cancel program")
				sys.exit(-2)
			if cargs.focussed_training >=2:
				do_focussed_training(config_list[cargs.config_number])
			if cargs.config_step >= 1:
				for cnf in config_list[cargs.config_number::cargs.config_step]:
					if cargs.dry_run:
						log.info(cnf)
					else:
						do_training(cnf)
			else:
				do_training(config_list[cargs.config_number])
		else:
			log.info("Start training of %i BDTs"%len(config_list))
			if cargs.dry_run:
				log.info("Dry-Run: aborting training")
				jsonTools.JsonDict(config_list).save("TrainingConfigs.config", indent = 4)
				log.info("TrainingConfigs saved to TrainingConfigs.config")
				sys.exit()
			if cargs.focussed_training >=2:
				aTools.parallelize(do_focussed_training, config_list, n_processes=int(cargs.j))
			else:
				aTools.parallelize(do_training, config_list, n_processes=int(cargs.j))
	else:
		config_list = []
		config_list.append(cargs_values)
		log.info("Start training of %i BDTs"%len(config_list))
		if cargs.dry_run:
			log.info("Dry-Run: aborting training")
			sys.exit()
		if cargs.focussed_training >=2:
			do_focussed_training(config_list[0])
		else:
			do_training(config_list[0])
