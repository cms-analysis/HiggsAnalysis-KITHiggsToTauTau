import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import argparse
import copy
import os
import re

import Artus.Utility.jsonTools as jsonTools
import sys
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.samples_run2 as samples
import ROOT
import glob
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

if __name__ == "__main__":

	parser = argparse.ArgumentParser(description="Train BDTs using TMVA interface.",
									 parents=[logger.loggingParser])
	parser.add_argument("-i", "--input-dir", required=True,
						help="Input directory. Use directory of artusoutput, which contains output and merged folder")
	parser.add_argument("-s", "--samples", nargs="+",
						default=["ggh", "qqh", "vh", "ztt", "zll", "ttj", "vv", "wj", "data"],
						choices=["ggh", "qqh", "vh", "ztt", "zll", "ttj", "vv", "wj", "data"],
						help="Samples for correlation calculation and scatter plots. [Default: %(default)s]")
	parser.add_argument("-M", "--Mvas", nargs="+",
						default=[],
						help="Calculate correlation within each bin of every MVA. [Default: %(default)s]")
	parser.add_argument("-n", "--n-processes", type=int, default=1,
							help="Number of (parallel) processes. [Default: %(default)s]")
	parser.add_argument("-o", "--output-dir",
							default="$CMSSW_BASE/src/plots/correlations",
							help="Output directory. [Default: %(default)s]")
	parser.add_argument("-e", "--exclude-cuts", nargs="+",
						default=["iso_1", "mt"],
						choices=["pZetaMiss", "pZetaVis", "iso_1", "iso_2", "mt_1", "mt_2", "mt"],
						help="""Exclude (default) selection cuts.
						[Default: %(default)s]""")
	parser.add_argument("-c", "--channels", nargs="*",
						default=["tt", "mt", "et", "em", "mm", "ee"],
						help="Channels. [Default: %(default)s]")
	parser.add_argument("--higgs-masses", nargs="+", default=["125"],
						help="Higgs masses. [Default: %(default)s]")
	parser.add_argument("-w", "--weight", default="1.0",
						help="""Additional weight (cut) expression.
						[Default: %(default)s]""")
	parser.add_argument("-p", "--pre-selection", default = "(1.0)",
						help="preselection for event selection [Default: %(default)s)")
	args = parser.parse_args()
	logger.initLogger(args)
	plot_configs = []

	#dir_path, filename = os.path.split(args.output_dir)
	dir_path = args.output_dir
	#filename = filename.replace(".root", "")
	storage_name_extension = dir_path + "/storage/reduced"
	if dir_path is None:
		pass
	elif not os.path.exists(dir_path):
		os.makedirs(dir_path)
		os.makedirs(dir_path+"/storage")
	sample_settings = samples.Samples()
	for channel in args.channels:
		category = None
		for requested_sample in args.samples:
			list_of_samples = [getattr(samples.Samples, requested_sample)]
			config = sample_settings.get_config(
					samples=list_of_samples,
					channel=channel,
					category=category,
					higgs_masses=args.higgs_masses,
					normalise_signal_to_one_pb=False,
					ztt_from_mc=False,
					weight=args.weight,
					exclude_cuts=args.exclude_cuts,
					stack_signal=False,
					scale_signal=1.0,
					mssm=False
					)
			config["request_nick"] = requested_sample
			config["channel"] = channel
			plot_configs.append(config)
	stored_files_list = []
	for config in plot_configs:
		c_tree = ""
		c_tree_list = ROOT.TList()
		root_file_name_list = []
		stored_files_list.append("%s_%s_%s.root"%(storage_name_extension, config["channel"], config["request_nick"]))
		cuts = ""
		#find all physical files and store them in root_filename_list
		for i,nick in enumerate(config["nicks"]):
			if not bool(sum([x in nick for x in ["wmh", "wph", "zh"]])) and "noplot" in nick:
				continue
			#next line splits file_string into filenames, those could contain * -> use glob.glob to map * to real names, add the list to root_file_name_list
			map(root_file_name_list.__iadd__, map(glob.glob, map(args.input_dir.__add__, config["files"][i].split(" "))))
			if (not cuts == "") and (not cuts == config["weights"][i]):
				log.error("can not decide which weight to use for sample %s nick %s" %(config["request_nick"],nick))
				print config
				sys.exit()
			cuts = config["weights"][i]

		for root_file_name in root_file_name_list:
			log.debug("Prepare Rootfile %s as Sample %s" %(root_file_name, config["request_nick"]))
			c_tree_list.append(ROOT.TChain())
			root_file_name = root_file_name + '/' + config["folders"][0]
			c_tree_list[-1].Add(root_file_name)
			c_tree_list[-1].SetName("list_tree")


		store_file = ROOT.TFile(stored_files_list[-1], "RECREATE")
		selection_string = cuts.replace("eventWeight*", "")
		for index in range(len(c_tree_list)):
			log.debug("Cut Tree %s for Sample %s "%(root_file_name_list[index], stored_files_list[-1]))
			c_tree_list[index]=c_tree_list[index].CopyTree(selection_string)
		log.debug("Merge Trees for Sample %s "%stored_files_list[-1])
		if len(c_tree_list) > 1:
			c_tree = ROOT.TTree.MergeTrees(c_tree_list)
		else:
			c_tree = c_tree_list[0]
		log.debug("Prepare Sample %s "%stored_files_list[-1])
		c_tree.SetName(config["folders"][0])
		for i in range(len(c_tree_list)):
			del c_tree_list[i]
		store_file.Write()
		store_file.Close()
