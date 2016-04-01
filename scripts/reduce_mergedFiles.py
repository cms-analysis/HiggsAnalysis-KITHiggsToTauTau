#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import ROOT, glob, itertools, sys, argparse, copy, os, re

import Artus.Utility.jsonTools as jsonTools
import Artus.Utility.tools as aTools
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.samples_run2 as samples
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.binnings as binnings
ROOT.PyConfig.IgnoreCommandLineOptions = True

def reduce_file(input_dict):
	for filename, item in input_dict.iteritems():
		#setting file paths
		#print item
		input_dir = item["in_dir"]
		output_dir = item["out_dir"]
		input_file_path = os.path.join(input_dir, os.path.join(filename.replace(".root", ""), filename))
		output_file_path = os.path.join(output_dir, os.path.join(filename.replace(".root", ""), filename))
		if not os.path.exists(os.path.join(output_dir, filename.replace(".root", ""))):
			os.makedirs(os.path.join(output_dir, filename.replace(".root", "")))
		#debugging to check which files are processed
		log.debug("Reduce input from file:")
		log.debug(input_file_path)
		if os.path.isfile(input_file_path):
			log.debug("=====ACCEPTED=====")
		else:
			log.debug("=====REJECTED=====")
			return
		#creating root files
		#input_file = ROOT.TFile(input_file_path, "read")
		output_file = ROOT.TFile(output_file_path, "RECREATE")
		for channel, reduce_package in item.iteritems():
			if channel == "in_dir" or channel == "out_dir":
				continue
			folders = []
			#find all root-directories to be processed and sort the weights accordingly
			#print reduce_package["ntuples"]
			map(lambda ie: folders.append(ie) if ie not in folders else False, reduce_package["ntuples"])
			weightlist_list = [[] for x in range(len(folders))]
			map(lambda w: weightlist_list[folders.index(w[0])].append(w[1]), zip(reduce_package["ntuples"], reduce_package["weights"]))
			weightstr_list = map(lambda c: " || ".join(c).replace("eventWeight*", ""), weightlist_list)
			for i, folder in enumerate(folders):
				output_file.cd()
				#ROOT.gDirectory.cd(str(c_dir))
				copy_file = ROOT.TChain()
				copy_file.SetName("TChain%i"%(i))
				copy_file.SetDirectory(0)
				amount_of_files = copy_file.Add(input_file_path+"/"+folder, -1)
				copy_file.SetDirectory(0)
				copy_file.SetName("TChainAdd%i"%(i))
				if amount_of_files > 0:
					log.debug("%i_%s"%(i, folder.replace("/ntuple", "")))
					log.debug(folder)
					log.debug("=====ACCEPTED=====")
				else:
					copy_file.SetDirectory(0)
					copy_file.SetName("Abort%i"%(i))
					del copy_file
					log.debug(folder)
					log.debug("=====REJECTED=====")
					continue
				copy_file = copy_file.CopyTree(weightstr_list[i])
				copy_file.SetName("%i_%s"%(i, folder.replace("/ntuple", "")))
				c_dir = output_file.mkdir(folder.replace("/ntuple", ""), folder.replace("/ntuple", ""))
				c_dir.cd()
				copy_file.Write()
				del copy_file
				output_file.cd()
		output_file.Close()


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Produce reduced samples and calculate correlations",
									 parents=[logger.loggingParser])
	parser.add_argument("-i", "--input-dir", required=True,
						help="Input directory. Use directory of artusoutput, which contains merged folder")
	parser.add_argument("-s", "--samples", nargs="+",
						default=["ggh", "qqh", "vh", "ztt", "zll", "ttj", "vv", "wj", "data"],
						choices=["ggh", "qqh", "vh", "ztt", "zll", "ttj", "vv", "wj", "data"],
						help="Samples for correlation calculation and scatter plots. [Default: %(default)s]")
	parser.add_argument("-n", "--n-processes", type=int, default=1,
							help="Number of (parallel) processes. [Default: %(default)s]")
	parser.add_argument("-e", "--exclude-cuts", nargs="+",
						default=["iso_1", "mt", "os"],
						help="""Exclude (default) selection cuts.
						[Default: %(default)s]""")
	parser.add_argument("-r", "--replacements", nargs="+",
						default=["Up", "Down"],
						help="Shape uncertainty string replacement. Strings to replace replacement string with [Default: %(default)s]")
	parser.add_argument("--rs",
						default="Nom",
						help="Shape uncertainty replacement string. String to be replaced [Default: %(default)s]")
	parser.add_argument("-c", "--channels", nargs="*",
						default=["tt", "mt", "et", "em", "mm", "ee"],
						help="Channels. [Default: %(default)s]")
	parser.add_argument("--higgs-masses", nargs="+", default=["120", "125", "130"],
						help="Higgs masses. [Default: %(default)s]")
	parser.add_argument("-p", "--pre-selection", default = "(1.0)",
						help="preselection for event selection [Default: %(default)s]")
	args = parser.parse_args()
	logger.initLogger(args)
	plot_configs = []
	dir_path = os.path.expandvars(args.input_dir)
	input_dir = os.path.join(dir_path, "merged/")
	output_dir = os.path.join(dir_path, "reduced/")

	if not os.path.exists(output_dir):
		os.makedirs(output_dir)

	sample_settings = samples.Samples()
	list_of_samples = [getattr(samples.Samples, rs) for rs in args.samples]
	#get all configs
	for channel in args.channels:
		category = None
		config = sample_settings.get_config(
				samples=list_of_samples,
				channel=channel,
				category=category,
				higgs_masses=args.higgs_masses,
				normalise_signal_to_one_pb=False,
				ztt_from_mc=False,
				exclude_cuts=args.exclude_cuts,
				stack_signal=False,
				scale_signal=1.0,
				mssm=False
				)
		config["channel"] = channel
		plot_configs.append(config)
	jsonTools.JsonDict(plot_configs[0]).save(os.path.join(output_dir, "ReduceFilesConfig.json"), indent=4)

	files_dict = {}
	for config in plot_configs:
		channel = config["channel"]
		for num, file_string in enumerate(config["files"]):
			ntuple = config["folders"][num]
			weight = config["weights"][num]
			real_files = []
			map(real_files.__iadd__, map(glob.glob, map(input_dir.__add__, file_string.split(" "))))
			weight_list = [weight for x in range(len(real_files))]
			ntuple_list = [ntuple for x in range(len(real_files))]
			for fnum, file_path in enumerate(real_files):
				file_name = file_path.split("/")[-1]
				w = weight_list[fnum]
				n = ntuple_list[fnum]
				if file_name not in files_dict:
					files_dict[file_name] = {"%s"%channel:{"weights":[], "ntuples":[]}}
				elif channel not in files_dict[file_name]:
					files_dict[file_name][channel] = {"weights":[], "ntuples":[]}
				if w not in files_dict[file_name][channel]["weights"] or n not in files_dict[file_name][channel]["ntuples"]:
					files_dict[file_name][channel]["weights"].append(w)
					files_dict[file_name][channel]["ntuples"].append(n)
					for front, back in itertools.product(args.replacements+["-.;+"], repeat = 2):
						n2 = n.replace(args.rs, front, 1).replace(args.rs, back,1).replace("-.;+", args.rs)
						if w not in files_dict[file_name][channel]["weights"] or n2 not in files_dict[file_name][channel]["ntuples"]:
							files_dict[file_name][channel]["weights"].append(w)
							files_dict[file_name][channel]["ntuples"].append(n2)
				#if n not in files_dict[file_name][channel]["ntuples"]:
	jsonTools.JsonDict(files_dict).save(os.path.join(output_dir, "ReduceFiles.json"), indent=4)

	give_away_list = []
	for filename, item in files_dict.iteritems():
		item["in_dir"] = input_dir
		item["out_dir"] = output_dir
		give_away_list.append({filename:item})

	aTools.parallelize(reduce_file, give_away_list, n_processes=args.n_processes)

	#for aufruf in give_away_list:
		#reduce_file(aufruf)















	#for filename, item in files_dict.iteritems():
		##setting file paths
		#input_file_path = os.path.join(input_dir, os.path.join(filename.replace(".root", ""), filename))
		#output_file_path = os.path.join(output_dir, os.path.join(filename.replace(".root", ""), filename))
		#if not os.path.exists(os.path.join(output_dir, filename.replace(".root", ""))):
			#os.makedirs(os.path.join(output_dir, filename.replace(".root", "")))
		##debugging to check which files are processed
		#log.debug("Reduce input from file:")
		#log.debug(input_file_path)
		#if os.path.isfile(input_file_path):
			#log.debug("=====ACCEPTED=====")
		#else:
			#log.debug("=====REJECTED=====")
		##creating root files
		##input_file = ROOT.TFile(input_file_path, "read")
		#output_file = ROOT.TFile(output_file_path, "RECREATE")
		#for channel, reduce_package in item.iteritems():
			#folders = []
			##find all root-directories to be processed and sort the weights accordingly
			#map(lambda ie: folders.append(ie) if ie not in folders else False, reduce_package["ntuples"])
			#weightlist_list = [[] for x in range(len(folders))]
			#map(lambda w: weightlist_list[folders.index(w[0])].append(w[1]), zip(reduce_package["ntuples"], reduce_package["weights"]))
			#weightstr_list = map(lambda c: " || ".join(c).replace("eventWeight*", ""), weightlist_list)
			#for i, folder in enumerate(folders):
				#c_dir = output_file.mkdir(folder.replace("/ntuple", ""), folder.replace("/ntuple", ""))
				#c_dir.cd()
				##ROOT.gDirectory.cd(str(c_dir))
				#print input_file_path+"/"+folder
				#copy_file = ROOT.TChain()
				##copy_file.SetDirectory(0)
				#copy_file.Add(input_file_path+"/"+folder)
				##copy_file.SetDirectory(0)
				#copy_file = copy_file.CopyTree(weightstr_list[i])
				#copy_file.SetName("ntuple")
				##copy_file.SetDirectory(c_dir)
				#copy_file.Write()
				#del copy_file
				#output_file.cd()
		#output_file.Close()