#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import argparse
import copy
import os

import Artus.Utility.jsonTools as jsonTools
import sys
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.samples_run2 as samples
import ROOT
import glob
ROOT.PyConfig.IgnoreCommandLineOptions = True

if __name__ == "__main__":

	parser = argparse.ArgumentParser(description="Train BDTs using TMVA interface.",
									 parents=[logger.loggingParser])

	parser.add_argument("-i", "--input-dir", required=True,
						help="Input directory.")
	parser.add_argument("-s", "--signal_samples", nargs="+",
						default=["ggh", "qqh", "vh"],
						choices=["ggh", "qqh", "vh", "ztt", "zll", "ttj", "vv", "wj"],
						help="Signal-Samples. [Default: %(default)s]")
	parser.add_argument("-b", "--bkg_samples", nargs="+",
						default=["ztt", "zll", "ttj", "vv", "wj"],
						choices=["ztt", "zll", "ttj", "vv", "wj", "qcd", "ggh", "qqh", "vh"],
						help="Bkg-Samples. [Default: %(default)s]")
	parser.add_argument("-c", "--channels", nargs="*",
						default=["tt", "mt", "et", "em", "mm", "ee"],
						help="Channels. [Default: %(default)s]")
	parser.add_argument("-x", "--quantities", nargs="*",
						default=["pVecSum", "pt_1", "mt_1", "pt_2", "mt_2", "met",
								"mvamet", "pZetaMissVis", "pZetaMiss",
								"pZetaVis","njets", "nbtag",
								"min_ll_jet_eta","lep1_centrality",
								"lep2_centrality",
								"delta_lep_centrality", "iso_1"],
						help="Quantities to train on. [Default: %(default)s]")
	parser.add_argument("--lumi", type=float, default=2.155,
						help="""Luminosity for the given data in fb^(-1).
								[Default: %(default)s]""")
	parser.add_argument("-w", "--weight", default="1.0",
						help="""Additional weight (cut) expression.
						[Default: %(default)s]""")
	parser.add_argument("-e", "--exclude-cuts", nargs="+",
						default=["iso_1", "mt"],
						choices=["pZetaMiss", "pZetaVis", "iso_1", "iso_2", "mt_1", "mt_2", "mt"],
						help="""Exclude (default) selection cuts.
						[Default: %(default)s]""")
	parser.add_argument("--higgs-masses", nargs="+", default=["125"],
						help="Higgs masses. [Default: %(default)s]")
	parser.add_argument("-S", "--Split", default=None,
						help="""If set enables splitting into training and test
						tree, use value between 0 and 99 to split tree using
						variable TrainingSelectionValue. [Default: %(default)s]""")
	parser.add_argument("-o", "--output-file",required=True,
						default="tmvaClassification/output.root",
						help="Output file. [Default: %(default)s]")
	parser.add_argument("--factory-options", default="",
						help="Options for TMVA.Factory constructor. [Default: %(default)s]")
	parser.add_argument("-m", "--methods", nargs="+", default=['BDT;nCuts=1200:NTrees=150:MinNodeSize=0.25:BoostType=Grad:Shrinkage=0.2'],
						help="MVA methods. Multiple arguments for TMVA.Factory.BookMethod are split by semicolon. Format: name;options. [Default: %(default)s]")
	parser.add_argument("--preparation-trees-options", default="",
						help="Options for preparation of inputs trees as passed to TMVA.Factory.PrepareTrainingAndTestTree. [Default: %(default)s]")
	parser.add_argument("-n", "--n-fold", type=int, default=0,
						help="number of splits for n-fold training. 0 is regular splitting according to --Split, 1 is one split,which results in 2 parts...[Default: %(default)s]")
	parser.add_argument("-p", "--pre-selection", default = "(1.0)",
						help="preselection for event selection [Default: %(default)s)")
	args = parser.parse_args()
	logger.initLogger(args)

	#if args.signal_samples == parser.get_default("signal_samples"):
		#args.signal_samples = [sample for sample in args.signal_samples
								#if hasattr(samples.Samples, sample)]
	#if args.bkg_samples == parser.get_default("bkg_samples"):
		#args.bkg_samples = [sample for sample in args.bkg_samples
								#if hasattr(samples.Samples, sample)]
	info_log = vars(args)
	info_log["comment"] = " ".join(sys.argv)
	info_log["config_list"] = []
	if "qcd" in (args.bkg_samples+args.signal_samples):
		log.error("qcd not possible for training")
		sys.exit()

	sample_settings = samples.Samples()
	#getting config
	plot_configs = []
	for channel in args.channels:
		category = None
		for requested_sample in (args.bkg_samples+args.signal_samples):
			list_of_samples = [getattr(samples.Samples, requested_sample)]
			config = sample_settings.get_config(
					samples=list_of_samples,
					channel=channel,
					category=category,
					higgs_masses=args.higgs_masses,
					normalise_signal_to_one_pb=False,
					ztt_from_mc=False,
					weight=args.weight,
					lumi = args.lumi * 1000,
					exclude_cuts=args.exclude_cuts,
					stack_signal=False,
					scale_signal=1.0,
					mssm=False
					)
			config["request_nick"] = requested_sample
			if requested_sample in args.bkg_samples and requested_sample in args.signal_samples:
				log.error("Sample %s is scheduled for signal and background" %requested_sample)
				sys.exit()
			if requested_sample in args.bkg_samples:
				config["sig_bkg"] = "Background"
			elif requested_sample in args.signal_samples:
				config["sig_bkg"] = "Signal"
			info_log["config_list"].append(config)
			plot_configs.append(config)

	splits_list = []
	stored_files_list = []
	s_b_extension = []
	#TMVA Stuff
	ROOT.TMVA.Tools.Instance()
	if args.Split and args.n_fold == 0:
		splits_list.append("(TrainingSelectionValue>=%i)*"%int(args.Split))
		splits_list.append("(TrainingSelectionValue<%i)*"%int(args.Split))
	elif args.n_fold:
		part_size = 100/(args.n_fold+1)
		for i in range(args.n_fold+1):
			splits_list.append("(TrainingSelectionValue>=%i)*(TrainingSelectionValue<%i)"%(int(i*part_size),int((i+1)*part_size)))

	info_log["splits"] = splits_list

	# create output file
	dir_path, filename = os.path.split(args.output_file)
	filename = filename.replace(".root", "")
	storage_name_extension = dir_path + "/storage/" + filename + "_storage"
	if dir_path is None:
		pass
	elif not os.path.exists(dir_path):
		os.makedirs(dir_path)
		os.makedirs(dir_path+"/storage")
		os.makedirs(dir_path+"/weights")

	#produce trees
	info_log["steps"] = []
	for config in plot_configs:
		c_tree_list = ROOT.TList()
		root_file_name_list = []
		stored_files_list.append("%s_%s_"%(storage_name_extension, config["request_nick"]))
		s_b_extension.append(config["sig_bkg"])
		cuts = ""
		for i,nick in enumerate(config["nicks"]):
			if not bool(sum([x in nick for x in ["wmh", "wph", "zh"]])) and "noplot" in nick:
				continue
			#next line splits file_string into filenames, those could contain * -> use glob.glob to map * to real names, add the list to root_file_name_list
			map(root_file_name_list.__iadd__, map(glob.glob, map(args.input_dir.__add__, config["files"][i].split(" "))))
			cuts = config["weights"][i]
		for root_file_name in root_file_name_list:
			log.debug("Prepare Rootfile %s as Sample %s" %(root_file_name, config["request_nick"]))
			info_log["steps"].append("Prepare Rootfile %s as Sample %s" %(root_file_name, config["request_nick"]))
			c_tree_list.append(ROOT.TChain())
			root_file_name = root_file_name + '/' + config["folders"][0]
			c_tree_list[-1].Add(root_file_name)
		for j,split in enumerate(splits_list):
			c_tree_list2 = ROOT.TList()
			c_tree = ""
			store_file = ROOT.TFile("%s_%s_%s.root"%(storage_name_extension, config["request_nick"], "split%i"%j), "RECREATE")
			selection_string = "*".join((split,cuts,args.pre_selection)).replace("eventWeight*", "")
			for index in range(len(c_tree_list)):
				log.debug("Cut Tree %s for Sample %s "%(root_file_name_list[index], stored_files_list[-1]))
				c_tree_list2.Add(c_tree_list[index].CopyTree(selection_string, "tree%i"%index))
			log.debug("Merge Trees for Sample %s "%stored_files_list[-1])
			if len(c_tree_list2) > 1:
				c_tree = ROOT.TTree.MergeTrees(c_tree_list2)
			else:
				c_tree = c_tree_list2[0]
			log.debug("Prepare Sample %s "%stored_files_list[-1])
			storage_tree = c_tree.CopyTree("", "tree%i"%j)
			storage_tree.SetName("SplitTree")
			store_file.Write()
			store_file.Close()

	#due to backward compatibillity: args.n_fold is per default 0 and Split None, if one wishes to do a non n-fold training with a specified split value:
	#set Split = desired split value, n_fold = 0 or default -> use n_fold + 1 for iterations range(n+1) = [0,...,n]
	for ifac in range(args.n_fold+1):
		iteration = args.n_fold + 1 #this variable is used for iterating over the input samples it must be different from n_fold due to backward compatibility
		output = ROOT.TFile(os.path.join(dir_path, filename+"T%i.root"%ifac), "RECREATE")
		# create factory
		log.debug("TMVA.Factory(\"T%i"%ifac + "\", TFile(\"" + os.path.join(dir_path, filename+"T%i.root"%ifac) +
				"\", \"RECREATE\"), \"" + args.factory_options + "\")")
		ROOT.TMVA.gConfig().GetIONames().fWeightFileDir = dir_path+"/weights"
		factory=ROOT.TMVA.Factory("T%i"%ifac, output,
									args.factory_options)
		# add training variables
		for variable in args.quantities:
			log.debug("TMVA.Factory.AddVariable(" +
						", ".join(["\"" + v + "\""
								for v in variable.split(";")]) + ")")
			factory.AddVariable(*(variable.split(";")))
		#add trees to factories
		skip = False
		if args.n_fold == 0: #this is for backward compatibiliy: iterate over all splits (2 splits)
			iteration += 1;
		for j,stored_file in enumerate(stored_files_list):
			for i in range(iteration):
				tree = ROOT.TChain()
				tree.Add(stored_file+"split%i.root/SplitTree"%(i))
				if i == ifac:
					factory.AddTree(tree, s_b_extension[j],
													1,
													ROOT.TCut(''), "test")
					log.debug("Add to Factory_%i sample %s as TestSample as %s" %(ifac, stored_file+"split%i.root/SplitTree"%(i), s_b_extension))
				else:

					factory.AddTree(tree, s_b_extension[j],
													1,
													ROOT.TCut(''), "train")
					log.debug("Add to Factory_%i sample %s as TrainingsSample as %s"%(ifac, stored_file+"split%i.root/SplitTree"%(i), s_b_extension))
			log.debug("factory.AddTree(%s,%s,%s,TCut(''), train/test)" %(
				nick, s_b_extension[j], cuts[j]))

		factory.SetBackgroundWeightExpression('eventWeight')
		factory.SetSignalWeightExpression('eventWeight')
		factory.PrepareTrainingAndTestTree(ROOT.TCut(''),
												ROOT.TCut(''),
												"NormMode=None:!V")
		# book methods
		for method in args.methods:
			method, options = method.split(';')
			name = method + '_' + filename
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
	log_log.save(dir_path+"/training_log.log", indent=4)
