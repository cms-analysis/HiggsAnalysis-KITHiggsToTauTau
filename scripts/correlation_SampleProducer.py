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
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.binnings as binnings
import ROOT
import glob
import itertools
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

if __name__ == "__main__":

	parser = argparse.ArgumentParser(description="Produce reduced samples and calculate correlations",
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
	parser.add_argument("-P", "--prepare-samples", action="store_true",
						help="produce reduced files")
	args = parser.parse_args()
	logger.initLogger(args)
	plot_configs = []
	dir_path = os.path.expandvars(args.output_dir)
	root_input_dir = os.path.join(args.input_dir, "merged/")
	storage_name_extension = dir_path + "/storage/reduced"

	if dir_path is None:
		pass
	elif not os.path.exists(dir_path):
		os.makedirs(dir_path)
		os.makedirs(dir_path+"/storage")
	elif not os.path.exists(dir_path+"/storage"):
		os.makedirs(dir_path+"/storage")

	sample_settings = samples.Samples()
	#get all configs
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
	#construct list of rootfiles, if prepare samples is enabled, files are produced
	for config in plot_configs:
		c_tree = ""
		c_tree_list = ROOT.TList()
		root_file_name_list = []
		stored_files_list.append("%s_%s_%s.root"%(storage_name_extension, config["channel"], config["request_nick"]))
		config["storage_file"] = stored_files_list[-1]
		config["storage_ntuple"]=config["folders"][0].replace("/ntuple", "")
		if args.prepare_samples:
			cuts = ""
			#find all physical files and store them in root_filename_list
			for i,nick in enumerate(config["nicks"]):
				if not bool(sum([x in nick for x in ["wmh", "wph", "zh"]])) and "noplot" in nick:
					continue
				#next line splits file_string into filenames, those could contain * -> use glob.glob to map * to real names, add the list to root_file_name_list
				map(root_file_name_list.__iadd__, map(glob.glob, map(root_input_dir.__add__, config["files"][i].split(" "))))
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
			if config["request_nick"] in ["ztt", "zll"]:
				selection_string = cuts.replace("eventWeight*", "").replace("*stitchWeight%s"%(config["request_nick"].upper()), "")
			for index in range(len(c_tree_list)):
				log.debug("Cut Tree %s for Sample %s "%(root_file_name_list[index], stored_files_list[-1]))
				c_tree_list[index]=c_tree_list[index].CopyTree(selection_string)
			log.debug("Merge Trees for Sample %s "%stored_files_list[-1])
			if len(c_tree_list) > 1:
				c_tree = ROOT.TTree.MergeTrees(c_tree_list)
			elif len(c_tree_list) == 1:
				c_tree = c_tree_list[0]
			else:
				c_tree =ROOT.TChain()
			log.debug("Prepare Sample %s from %i files"%(stored_files_list[-1],len(c_tree_list)))
			c_tree.SetName(config["folders"][0].replace("/ntuple", ""))
			for i in range(len(c_tree_list)):
				del c_tree_list[0]
			del c_tree_list
			store_file.Write()
			store_file.Close()

	artus =jsonTools.JsonDict(glob.glob(os.path.join(args.input_dir, "artus_*.json")))
	#find all correlations to be calculated and plottet
	for config in plot_configs:
		parsed_parameters = []
		unparsed_ParameterList = []
		map(unparsed_ParameterList.__iadd__,
			map(lambda b: b[1].split(","), map(lambda s: s.split(";"),
												artus["Pipelines"][config["folders"][0].replace("/ntuple", "")]["MVATestMethodsInputQuantities"])))
		for unsplitted_vars in unparsed_ParameterList:
			if ":=" in unsplitted_vars:
				var = unsplitted_vars.split(":=")[1]
			else:
				var = unsplitted_vars
			if not var in parsed_parameters:
				parsed_parameters.append(var)
		config["parameters_list"] = parsed_parameters


	for config in plot_configs:
		root_histograms = {}
		corr_vars = {}
		binnings_dict = binnings.BinningsDict()
		nick_path = os.path.join(dir_path, config["request_nick"])
		if not os.path.exists(nick_path):
			os.makedirs(nick_path)
		root_inf = ROOT.TFile(config["storage_file"], "read")
		root_inst = root_inf.Get(config["storage_ntuple"])
		for variables in itertools.combinations(config["parameters_list"], 2):
			#print variables
			xbins_list = binnings_dict.get_binning("%s_"%config["channel"]+variables[0])
			ybins_list = binnings_dict.get_binning("%s_"%config["channel"]+variables[1])
			xbins = []
			ybins = []
			if "," in xbins_list:
				xbins_list = map(float, xbins_list.split(","))
				xbins += xbins_list
				xbins[0] = int(xbins[0])
			elif len(xbins_list.split(" ")) >= 2 and xbins_list.split(" ")[1] != "":
				xbins_list = map(float, xbins_list.split(","))
				xbins.append(len(xbins_list.split(" "))-1)
				xbins.apped(a_bins_list)
			else:
				xbins = [100,0.,0.]

			if "," in ybins_list:
				ybins_list = map(float, ybins_list.split(","))
				ybins += ybins_list
				ybins[0] = int(ybins[0])
			elif len(ybins_list.split(" ")) >= 2 and ybins_list.split(" ")[1] != "":
				ybins_list = map(float, ybins_list.split(","))
				ybins.append(len(ybins_list.split(" "))-1)
				ybins.apped(a_bins_list)
			else:
				ybins = [100,0.,0.]

			binnings = xbins + ybins
			log.debug("Generate RootHistogram TH2F: %s"%("+-+".join(variables)))
			log.debug(binnings)
			root_histograms["+-+".join(variables)] = ROOT.TH2F("+-+".join(variables),
													  "correlation: %s vs %s"%variables, *binnings)
			corr_vars["+-+".join(variables)] = 0
			root_histograms["+-+".join(variables)].SetDirectory(0)
			ROOT.SetOwnership (root_histograms["+-+".join(variables)], False)
		for variable in config["parameters_list"]:
			xbins_list = binnings_dict.get_binning("%s_"%config["channel"]+variables[0])
			xbins = []
			if "," in xbins_list:
				xbins_list = map(float, xbins_list.split(","))
				xbins += xbins_list
				xbins[0] = int(xbins[0])
			elif len(xbins_list.split(" ")) >= 2 and xbins_list.split(" ")[1] != "":
				xbins_list = map(float, xbins_list.split(","))
				xbins.append(len(xbins_list.split(" "))-1)
				xbins.apped(a_bins_list)
			else:
				xbins = [100,0.,0.]

			binnings = xbins + xbins
			root_histograms["+-+".join([variable,variable])] = ROOT.TH2F("+-+".join([variable,variable]),
													  "correlation: %s vs %s"%(variable,variable), *binnings)
			corr_vars["+-+".join([variable,variable])] = 0
			corr_vars[variable] = 0
			corr_vars["var_%s"%variable] = 0
			root_histograms["+-+".join([variable,variable])].SetDirectory(0)
			ROOT.SetOwnership (root_histograms["+-+".join([variable,variable])], False)
		print "======================================================================"
		print "Calculate correlations and make scatter plots for %i variable pairs."%len(root_histograms)
		print "======================================================================"

		i = 0.
		n = 0
		zero_vals = {}
		for event in root_inst:
			calced_means = []
			w = event.__getattr__("eventWeight")
			for varxy in root_histograms.iterkeys():
				varx, vary = map(str, varxy.split("+-+"))
				x, y = map(event.__getattr__, map(str, varxy.split("+-+")))
				root_histograms[varxy].Fill(x, y, w)

				if varx not in zero_vals:
					zero_vals[varx] = 0
				if vary not in zero_vals:
					zero_vals[vary] = 0

				if varx not in calced_means:
					#print "calculate mean for %s" %varx
					corr_vars[varx] += w*(x -zero_vals[varx])
					corr_vars["var_%s"%varx] += w*(x -zero_vals[varx])**2
					calced_means.append(varx)
				if vary not in calced_means:
					#print "calculate mean for %s" %vary
					corr_vars[vary] += w*(y - zero_vals[vary])
					corr_vars["var_%s"%vary] += w*(y - zero_vals[vary])**2
					calced_means.append(vary)
				corr_vars[varxy] += w*(x -zero_vals[varx]) * (y - zero_vals[vary])
			#sys.exit()
			i += w
			n += 1
			#if n == 1000:
				#break

		#root_inf.Close()
		hist_file = ROOT.TFile(os.path.join(nick_path, "%s_histograms.root"%config["channel"]),"RECREATE")
		for varxy in root_histograms.iterkeys():
			root_histograms[varxy].Write()
		#calculate variances and correlations -> moved to collector_script
		#calced_variances = []
		#for varxy in root_histograms.iterkeys():
			#varx, vary = map(str, varxy.split("+-+"))
			#if varx not in calced_variances:
				#corr_vars["var_%s"%varx] = (corr_vars["var_%s"%varx] - (corr_vars[varx]**2.)/i)/i
				#calced_variances.append(varx)
			#if vary not in calced_variances:
				#corr_vars["var_%s"%vary] = (corr_vars["var_%s"%vary] - (corr_vars[vary]**2.)/i)/i
				#calced_variances.append(vary)
			#try:
				#corr_vars[varxy] = (corr_vars[varxy]-corr_vars[varx]*corr_vars[vary]/i)/i/(corr_vars["var_%s"%varx])**0.5/(corr_vars["var_%s"%vary])**0.5
			#except ZeroDivisionError:
				#log.error("ZeroDivisonError: %s" %varxy)
				#corr_vars[varxy] = None
			#except ValueError:
				#log.error("ValueError: %s" %varxy)
				#corr_vars[varxy] = None
		corr_vars["weight_sum"] = i
		corr_vars["n"] = n
		hist_file.Write()
		hist_file.Close()
		root_inf.Close()
		config["correlations"] = corr_vars
		jsonTools.JsonDict(config).save(os.path.join(nick_path,"%s_corr-config.json"%config["channel"]),indent=4)