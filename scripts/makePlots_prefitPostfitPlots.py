#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import argparse
import os
import sys

import Artus.Utility.tools as tools
import Artus.Utility.tfilecontextmanager as tfilecontextmanager
import Artus.HarryPlotter.utility.roottools as roottools

import HiggsAnalysis.KITHiggsToTauTau.plotting.higgsplot as higgsplot
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.samples_run2_2016 as samples


if __name__ == "__main__":

	parser = argparse.ArgumentParser(description="Make prefit/postfit plots.",
	                                 parents=[logger.loggingParser])

	parser.add_argument("-i", "--input-files", nargs="+", required=True,
	                    help="Input files = Outputs from PostFitShapesFromWorkspace.")
	parser.add_argument("-s", "--signal-samples", nargs="+", default=[],
	                    help="Signal Samples. Samples in one argument separated by whitespaces are summed up before drawing. [Default: %(default)s]")
	parser.add_argument("-b", "--background-samples", nargs="+", default=["ZTT", "ZLL ZL ZJ", "TT TTT TTJ", "W", "VV VVT VVJ", "QCD"],
	                    help="Background Samples. Samples in one argument separated by whitespaces are summed up before stacking. [Default: %(default)s]")
	parser.add_argument("--cms", default=False, action="store_true",
	                    help="CMS Preliminary lable. [Default: %(default)s]")
	parser.add_argument("--lumi", type=float, default=samples.default_lumi/1000.0,
	                    help="Luminosity for the given data in fb^(-1). [Default: %(default)s]")
	parser.add_argument("--mssm", default=False, action="store_true",
	                    help="Produce the plots for the MSSM. [Default: %(default)s]")
	parser.add_argument("--mva", default=False, action="store_true",
	                    help="Produce plots for the mva studies. [Default: %(default)s]")
	parser.add_argument("--polarisation", default=False, action="store_true",
	                    help="Produce the plots for the polarisation analysis. [Default: %(default)s]")
	parser.add_argument("--smhtt", default=False, action="store_true",
	                    help="Produce the plots for the SM HTT analysis. [Default: %(default)s]")
	parser.add_argument("--cpggh", default=False, action="store_true",
	                    help="Produce plots for the Higgs CP ggH analysis. [Default: %(default)s]")
	parser.add_argument("--cp", default=False, action="store_true",
	                    help="Produce the plots for the CP analysis. [Default: %(default)s]")  #TODO instead of 3 different boolean flag, change to option with 3 possible values
	parser.add_argument("--cprho", default=False, action="store_true",
	                    help="Produce the plots for the CP analysis. [Default: %(default)s]")
	parser.add_argument("--cpcomb", default=False, action="store_true",
	                    help="Produce the plots for the CP analysis. [Default: %(default)s]")
	parser.add_argument("--taues", default=False, action="store_true",
	                    help="Produce the plots for the tau energy scale analysis. [Default: %(default)s]")
	parser.add_argument("--etaufakerate", default=False, action="store_true",
	                    help="Produce the plots for the electron tau fake rate analysis. [Default: %(default)s]")
	parser.add_argument("--lfv", default=False, action="store_true",
	                    help="Produce the plots for the lepton flavour violation analysis. [Default: %(default)s]")
	parser.add_argument("--era", default="2016",
	                    help="Era of samples to be used. [Default: %(default)s]")
	parser.add_argument("-a", "--args", default="--plot-modules PlotRootHtt",
	                    help="Additional Arguments for HarryPlotter. [Default: %(default)s]")
	parser.add_argument("-r", "--ratio", default=False, action="store_true",
	                    help="Add ratio subplot. [Default: %(default)s]")
	parser.add_argument("-n", "--n-processes", type=int, default=1,
	                    help="Number of (parallel) processes. [Default: %(default)s]")
	parser.add_argument("-f", "--n-plots", type=int,
	                    help="Number of plots. [Default: all]")
	parser.add_argument("-o", "--output-dir",
	                    default="$CMSSW_BASE/src/plots/control_plots/",
	                    help="Output directory. [Default: %(default)s]")
	parser.add_argument("--www", nargs="?", default=None, const="prefit_postfit_plots",
	                    help="Publish plots. [Default: %(default)s]")
	
	args = parser.parse_args()
	logger.initLogger(args)
	
	if (args.era == "2015") or (args.era == "2015new"):
		import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.samples_run2_2015 as samples
	elif args.era == "2016":
		import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.samples_run2_2016 as samples
		if args.lumi == parser.get_default("lumi"):
			args.lumi = samples.default_lumi/1000.0
	elif args.era == "2017":
		import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.samples_run2_2017 as samples
		if args.lumi == parser.get_default("lumi"):
			args.lumi = samples.default_lumi/1000.0
	else:
		log.critical("Invalid era string selected: " + args.era)
		sys.exit(1)
	
	args.signal_samples = [sample.split() for sample in args.signal_samples]
	args.background_samples = [sample.split() for sample in args.background_samples]
	
	inputs_base = tools.longest_common_substring_from_list(args.input_files)
	
	input_file_content = {}
	for input_filename in args.input_files:
		with tfilecontextmanager.TFileContextManager(input_filename, "READ") as input_file:
			for histogram in list(zip(*roottools.RootTools.walk_root_directory(input_file))[-1]):
				input_file_content.setdefault(input_filename, {}).setdefault(os.path.dirname(histogram), []).append(os.path.basename(histogram))
	
	plot_configs = []
	for input_file, input_histograms in input_file_content.iteritems():
		short_directory = os.path.dirname(input_file).replace(inputs_base, "")
		
		for folder, histograms in input_histograms.iteritems():
			channel = folder[:folder.find("_")]
			category = folder[folder.find("_")+1:].replace("_prefit", "").replace("_postfit", "")
			fit_type = folder[folder.rfind("_")+1:]
			
			background_expressions = []
			background_nicks = []
			background_colors = []
			background_labels = []
			for tmp_samples in args.background_samples:
				sample = []
				for tmp_sample in tmp_samples:
					if tmp_sample in histograms:
						sample.append(tmp_sample)
				if len(sample) > 0:
					background_expressions.extend(sample)
					background_nicks.extend(["_".join(sample)] * len(sample))
					background_colors.append(sample[0].lower())
					background_labels.append(sample[0].lower())
			n_background_inputs = len(background_expressions)
			n_background_outputs = len(background_colors)
			
			signal_expressions = []
			signal_nicks = []
			signal_colors = []
			signal_labels = []
			for tmp_samples in args.signal_samples:
				sample = []
				for tmp_sample in tmp_samples:
					if tmp_sample in histograms:
						sample.append(tmp_sample)
				if len(sample) > 0:
					signal_expressions.extend(sample)
					signal_nicks.extend(["_".join(sample)] * len(sample))
					signal_colors.append(sample[0].lower())
					signal_labels.append(sample[0].lower())
			n_signal_inputs = len(signal_expressions)
			n_signal_outputs = len(signal_colors)
			
			log.debug("Create {fit_type} plot for \"{short_directory}\" (channel \"{channel}\", category \"{category}\", signal {signal_expressions}, background {background_expressions})".format(
					fit_type=fit_type,
					short_directory=short_directory,
					channel=channel,
					category=category,
					signal_expressions=str(signal_expressions),
					background_expressions=str(background_expressions)
			))
			
			uncertainty_expressions = ["TotalBkg"] + (["TotalSig"] if n_signal_inputs == 0 else [])
			uncertainty_nicks = ["TotalExp"] * len(uncertainty_expressions)
			
			config = {}
			config["files"] = [input_file]
			config["folders"] = [folder]
			config["x_expressions"] = background_expressions + uncertainty_expressions + signal_expressions + ["data_obs"]
			config["nicks"] = background_nicks + uncertainty_nicks + signal_nicks + ["data_obs"]
			
			config["stacks"] = (["background"]*n_background_outputs) + ["totalbkg"] + signal_labels + ["data"]
			config["markers"] = (["HIST"]*n_background_outputs) + ["E2"] + (["LINE"]*n_signal_outputs) + ["E"]
			config["legend_markers"] = (["F"]*n_background_outputs) + ["F"] + (["L"]*n_signal_outputs) + ["ELP"]
			config["colors"] = background_colors + ["totalbkg"] + signal_colors + ["data_obs"]
			config["labels"] = background_labels + ["totalbkg"] + signal_labels + ["data_obs"]
			
			if args.ratio:
				if "Ratio" not in config.get("analysis_modules", []):
					config.setdefault("analysis_modules", []).append("Ratio")
				
				config.setdefault("ratio_numerator_nicks", []).append(" ".join(background_nicks))
				config.setdefault("ratio_denominator_nicks", []).append(" ".join(background_nicks))
				config.setdefault("ratio_result_nicks", []).append("ratio_bkg")
				config.setdefault("stacks", []).append("ratio_bkg")
				config.setdefault("markers", []).append("E2")
				config.setdefault("legend_markers", []).append("ELP")
				config.setdefault("colors", []).append("totalbkg")
				config.setdefault("labels", []).append("")
				
				if n_signal_outputs > 0:
					config.setdefault("ratio_numerator_nicks", []).append(" ".join(background_nicks+signal_nicks))
					config.setdefault("ratio_denominator_nicks", []).append(" ".join(background_nicks))
					config.setdefault("ratio_result_nicks", []).append("ratio_sig")
					config.setdefault("stacks", []).append("ratio_sig")
					config.setdefault("markers", []).append("LINE")
					config.setdefault("legend_markers", []).append("L")
					config.setdefault("colors", []).append(background_colors[0])
					config.setdefault("labels", []).append("")
				
				config.setdefault("ratio_numerator_nicks", []).append("data_obs")
				config.setdefault("ratio_denominator_nicks", []).append(" ".join(background_nicks))
				config.setdefault("ratio_result_nicks", []).append("ratio_data")
				config.setdefault("stacks", []).append("ratio_data")
				config.setdefault("markers", []).append("E")
				config.setdefault("legend_markers", []).append("ELP")
				config.setdefault("colors", []).append("data_obs")
				config.setdefault("labels", []).append("")
			
			config["x_label"] = "Discriminator"
			if args.polarisation:
				config["x_label"] = "testZttPol13TeV_"+channel+"_"+category
			config["title"] = "channel_"+channel
			if args.polarisation:
				config["title"] = "channel_"+channel+"_"+category

			if "--y-log" not in args.args:
				config["y_lims"] = [0.0]
			if args.cms:
				config["cms"] = True
				config["extra_text"] = "Preliminary"
				config["legend"] = [0.7, 0.4, 0.95, 0.83] if args.ratio else [0.7, 0.5, 0.9, 0.85]
			else:
				config["y_rel_lims"] = [0.5, 10.0] if "--y-log" in args.args else [0.0, 1.5 if args.ratio else 1.4]
				config["legend"] = [0.23, 0.63, 0.9, 0.83] if args.ratio else [0.23, 0.73, 0.9, 0.89]
				config["legend_cols"] = 3
			
			if args.lumi is not None:
				config["lumis"] = [float("%.1f" % args.lumi)]
			config["energies"] = [13]
			config["year"] = args.era
			
			config["output_dir"] = os.path.dirname(input_file)
			if args.www:
				config["www"] = os.path.join(args.www, os.path.dirname(input_file).replace(inputs_base, ""))
			config["filename"] = os.path.basename(input_file).replace(".root", "")+"__"+folder
			
			plot_configs.append(config)
	
	if log.isEnabledFor(logging.DEBUG):
		import pprint
		pprint.pprint(plot_configs)
	higgsplot.HiggsPlotter(list_of_config_dicts=plot_configs, list_of_args_strings=[args.args], n_processes=args.n_processes, n_plots=args.n_plots)

