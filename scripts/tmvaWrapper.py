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
ROOT.PyConfig.IgnoreCommandLineOptions = True
def get_configs(args, info_log):
	plot_configs = []
	#generate config_list containing one config file per requested nick for training
	log.info("prepare config files to extract file paths, weights and cuts")
	sample_settings = samples.Samples()
	for channel in args["channels"]:
		category = None
		for requested_sample in (args["bkg_samples"]+args["signal_samples"]):
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
			plot_configs.append(config)
			info_log["config_list"].append(config)
	log.info("Config information aquired")
	return (plot_configs, info_log)

def do_splitting(args, plot_configs):

	splits_list = []
	stored_files_list = []
	s_b_extension = []
	if args["Split"] and args["n_fold"] == 1:
		splits_list.append("(TrainingSelectionValue>=%i)*"%int(args["Split"]))
		splits_list.append("(TrainingSelectionValue<%i)*"%int(args["Split"]))
	elif args["n_fold"] and len(args["custom_splitting"]) == int(args["n_fold"]):
		for split in args["custom_splitting"]:
			splits_list.append(split)
	elif args["n_fold"]:
		part_size = 100/(args["n_fold"])
		for i in range(args["n_fold"]):
			splits_list.append("(TrainingSelectionValue>=%i)*(TrainingSelectionValue<%i)"%(int(i*part_size),int((i+1)*part_size)))

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
		for j,split in enumerate(splits_list):
			#combine the root ntuples from c_tree_list into one ntuple. this happens for every split sample for the nfold training
			c_tree_list2 = ROOT.TList()
			c_tree = ""
			store_file = ROOT.TFile("%s_%s_%s.root"%(storage_name_extension, config["request_nick"], "split%i"%(j+1)), "RECREATE")
			selection_string = "*".join((split,cuts,args["pre_selection"])).replace("eventWeight*", "")
			for index in range(len(c_tree_list)):
				#import pdb
				log.debug("Cut Tree %s for Sample %s "%(root_file_name_list[index], stored_files_list[-1]))
				#pdb.set_trace()
				c_tree_list2.Add(c_tree_list[index].CopyTree(selection_string, "tree%i"%index))
			log.debug("Merge Trees for Sample %s "%stored_files_list[-1])
			if len(c_tree_list2) > 1:
				c_tree = ROOT.TTree.MergeTrees(c_tree_list2)
			else:
				c_tree = c_tree_list2[0]
			log.debug("Prepare Sample %s "%stored_files_list[-1])
			storage_tree = c_tree.CopyTree("", "tree%i"%(j+1))
			storage_tree.SetName("SplitTree")
			store_file.Write()
			store_file.Close()
	return (splits_list, stored_files_list, s_b_extension)

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
			factory.AddVariable(*(variable.split(";")))
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

		factory.SetBackgroundWeightExpression('eventWeight' + (("*" + args["weight"]) if args["weight"] != "1.0" else ""))
		factory.SetSignalWeightExpression('eventWeight' + (("*" + args["weight"]) if args["weight"] != "1.0" else ""))
		factory.PrepareTrainingAndTestTree(ROOT.TCut(''),
												ROOT.TCut(''),
												"NormMode=None:!V")
		# book methods
		for method in args["methods"]:
			log.debug("prepare method %s"%method)
			method, options = method.split(';')
			name = method + '_' + filename
			if(method == "FastBDT"):
				factory.BookMethod(ROOT.TMVA.Types.kPlugins, method, options)
			else:
				factory.BookMethod(method, name, options)
			log.debug("TMVA.Factory.BookMethod(" + ", ".join(
				["\"" + m + "\"" for m in (method, name, options)]) + ")")
		#perform full training
		log.debug("TMVA.Factory.TrainAllMethods()")
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
						choices=["ztt", "zll", "ttj", "vv", "wj", "qcd", "ggh", "qqh", "vh"],
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
								"delta_lep_centrality;F", "pScalSum;F"],
						help="Quantities to train on.  [Default: %(default)s]")
	parser.add_argument("--lumi", type=float, default=2.301,
						help="""Luminosity for the given data in fb^(-1).
								[Default: %(default)s]""")
	parser.add_argument("-w", "--weight", default="1.0",
						help="""Additional weight (cut) expression.
						[Default: %(default)s]""")
	parser.add_argument("-e", "--exclude-cuts", nargs="+",
						default=[],
						choices=["pZetaMiss", "pZetaVis", "iso_1", "iso_2", "mt_1", "mt_2", "mt"],
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
	parser.add_argument("--dry-run", default = False, action="store_true",
						help="number of parallel processes for training, only used for local jobs [Default: %(default)s]")


	cargs = parser.parse_args()
	logger.initLogger(cargs)
	cargs_values = vars(cargs)
	#=====If jobs are to run on batch-system, the ouputpath must be adjusted this is done below in if, elif
	if cargs.output_file == None:
		cargs.output_file = os.getcwd()
	if cargs.batch_system:
		dir_path, filename = os.path.split(cargs.output_file)
		cargs.output_file = os.getcwd()
	#=====here starts predefined code for scans and collection of signal background combinations
	if cargs.modify:
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
				copy_cargs["methods"] = ["BDT;nCuts=1200:NTrees={i}:MinNodeSize=0.25:BoostType=Grad:Shrinkage=0.1".format(i=1500)]
				copy_cargs["n_fold"] = 2
				config_list.append(copy.deepcopy(copy_cargs))

				copy_cargs["signal_samples"] = ['qqh']
				copy_cargs["bkg_samples"] = ["ggh"]
				copy_cargs["output_file"] = os.path.join(copy_path, "vbf_{i}").format(i=i)
				copy_cargs["methods"] = ["BDT;nCuts=1200:NTrees={i}:MinNodeSize=0.25:BoostType=Grad:Shrinkage=0.1".format(i=500)]
				copy_cargs["quantities"].append("jdeta")
				copy_cargs["quantities"].append("mjj")
				config_list.append(copy.deepcopy(copy_cargs))

		if cargs.batch_system:
			log.info("Start training of BDT config number %i"%cargs.config_number)
			if cargs.dry_run:
				log.info("Dry-Run: aborting training")
				jsonTools.JsonDict(config_list[cargs.config_number]).save("TrainingConfigs.config", indent = 4)
				log.info("TrainingConfigs[%i] saved to TrainingConfigs.config"%cargs.config_number)
				log.info(config_list[cargs.config_number])
				sys.exit()
			if cargs.config_number > len(config_list):
				log.error("config_number is greater than length of config_list, cancel program")
				sys.exit(-2)
			do_training(config_list[cargs.config_number])
		else:
			log.info("Start training of %i BDTs"%len(config_list))
			if cargs.dry_run:
				log.info("Dry-Run: aborting training")
				jsonTools.JsonDict(config_list).save("TrainingConfigs.config", indent = 4)
				log.info("TrainingConfigs saved to TrainingConfigs.config")
				sys.exit()
			aTools.parallelize(do_training, config_list, n_processes=int(cargs.j))
	else:
		config_list = []
		config_list.append(cargs_values)
		log.info("Start training of %i BDTs"%len(config_list))
		if cargs.dry_run:
			log.info("Dry-Run: aborting training")
			sys.exit()
		do_training(config_list[0])