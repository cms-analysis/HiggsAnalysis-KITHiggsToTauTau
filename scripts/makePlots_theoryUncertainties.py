#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import argparse
import copy
import os
import re
import sys

import Artus.Utility.jsonTools as jsonTools
import Artus.Utility.tools as tools
import HiggsAnalysis.KITHiggsToTauTau.plotting.higgsplot as higgsplot
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.binnings as binnings
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.samples_run2_2015 as samples


if __name__ == "__main__":

	parser = argparse.ArgumentParser(description="Make plots for the study of theory uncertainties.",
	                                 parents=[logger.loggingParser])

	parser.add_argument("-i", "--input-dir", required=True,
	                    help="Input directory.")
	parser.add_argument("-s", "--samples", nargs=1,
	                    help="Samples.")
	parser.add_argument("-c", "--channels", nargs="*",
	                    default=["tt", "mt", "et", "em", "mm"],
	                    help="Channels. [Default: %(default)s]")
	parser.add_argument("--categories", nargs="+", default=[None],
	                    help="Categories. [Default: %(default)s]")
	parser.add_argument("-x", "--quantities", nargs="*",
	                    default=["integral",
	                             "pt_1", "eta_1", "phi_1", "m_1", "iso_1", "mt_1",
	                             "pt_2", "eta_2", "phi_2", "m_2", "iso_2", "mt_2",
	                             "pt_sv", "eta_sv", "phi_sv", "m_sv", "m_vis", "ptvis",
	                             "met", "metphi", "metcov00", "metcov01", "metcov10", "metcov11",
	                             "mvamet", "mvametphi", "mvacov00", "mvacov01", "mvacov10", "mvacov11",
	                             "pZetaMissVis", "pzetamiss", "pzetavis",
	                             "jpt_1", "jeta_1", "jphi_1",
	                             "jpt_2", "jeta_2", "jphi_2",
	                             "njetspt30", "mjj", "jdeta", "njetingap20", "njetingap",
	                             "trigweight_1", "trigweight_2", "puweight",
	                             "npv", "npu", "rho"],
	                    help="Quantities. [Default: %(default)s]")
	parser.add_argument("-j", "--json-dir", default="$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/control_plots/",
	                    help="Base directory for optional JSON configs. [Default: %(default)s]")
	parser.add_argument("--cms", default=False, action="store_true",
	                    help="CMS Preliminary lable. [Default: %(default)s]")
	parser.add_argument("--lumi", type=float, default=samples.default_lumi/1000.0,
	                    help="Luminosity for the given data in fb^(-1). [Default: %(default)s]")
	parser.add_argument("--weights-up", nargs="+", required=True,
	                    help="LHE weights for shift up.")
	parser.add_argument("--weights-down", nargs="+", required=True,
	                    help="LHE weights for shift down.")
	parser.add_argument("-e", "--exclude-cuts", nargs="+", default=[],
	                    help="Exclude (default) selection cuts. [Default: %(default)s]")
	parser.add_argument("-m", "--higgs-masses", nargs="+", default=["125"],
	                    help="Higgs masses. [Default: %(default)s]")
	parser.add_argument("-b", "--background-method", default=["new"], nargs="+",
	                    help="Background estimation method to be used, channel dependent. [Default: %(default)s]")
	parser.add_argument("--mssm", default=False, action="store_true",
	                    help="Produce the plots for the MSSM. [Default: %(default)s]")
	parser.add_argument("--mva", default=False, action="store_true",
	                    help="Produce plots for the mva studies. [Default: %(default)s]")
	parser.add_argument("--polarisation", default=False, action="store_true",
	                    help="Produce the plots for the polarisation analysis. [Default: %(default)s]")
	parser.add_argument("--smhtt", default=False, action="store_true",
	                    help="Produce the plots for the SM HTT analysis. [Default: %(default)s]")
	parser.add_argument("--taues", default=False, action="store_true",
	                    help="Produce the plots for the tau energy scale analysis. [Default: %(default)s]")
	parser.add_argument("--analysis-modules", default=[], nargs="+",
	                    help="Additional analysis Modules. [Default: %(default)s]")
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
	parser.add_argument("--www", nargs="?", default=None, const="control_plots",
	                    help="Publish plots. [Default: %(default)s]")
	parser.add_argument("--no-ewk-samples", default=False, action="store_true",
	                    help="Do not use EWK Z/W samples. [Default: %(default)s]")
	parser.add_argument("--no-ewkz-as-dy", default=False, action="store_true",
	                    help="Do not include EWKZ samples in inputs for DY. [Default: %(default)s]")
	
	args = parser.parse_args()
	logger.initLogger(args)

	if (args.era == "2015") or (args.era == "2015new"):
		import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.samples_run2_2015 as samples
	elif args.era == "2016":
		import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.samples_run2_2016 as samples
		if args.lumi == parser.get_default("lumi"):
			args.lumi = samples.default_lumi/1000.0
	else:
		log.critical("Invalid era string selected: " + args.era)
		sys.exit(1)

	if args.samples == parser.get_default("samples"):
		args.samples = [sample for sample in args.samples if hasattr(samples.Samples, sample)]

	list_of_samples = [getattr(samples.Samples, sample) for sample in args.samples]
	sample_settings = samples.Samples()
	
	args.categories = [None if category == "None" else category for category in args.categories]
	
	binnings_settings = binnings.BinningsDict()

	plot_configs = []
	# fill in hp-style
	for index in range(len(args.channels) - len(args.background_method)):
		args.background_method.append(args.background_method[index])

	# Category and Cut type assignment for respective studies
	global_category_string = "catHtt13TeV"
	global_cut_type = "baseline"
	if args.mssm:
		global_category_string = "catHttMSSM13TeV"
		global_cut_type = "mssm"
	elif args.mva:
		global_category_string = "catMVAStudies"
	elif args.polarisation:
		global_category_string = "catZttPol13TeV"
		global_cut_type = "low_mvis_smhtt"
	elif args.taues:
		global_cut_type = "tauescuts"
	if args.era == "2016":
		if args.smhtt:
			global_cut_type = "smhtt"
		global_cut_type += "2016"

	# Configs construction for HP
	for category in args.categories:
		for quantity in args.quantities:
			
			channels_background_methods = zip(args.channels, args.background_method)
			channel_config = {}
			for index, (channel, background_method) in enumerate(channels_background_methods):
				if args.mssm:
					if args.era == "2016":
						cut_type = "mssm2016"
					elif "looseiso" in category:
						cut_type = "mssm2016looseiso"
					elif "loosemt" in category:
						cut_type = "mssm2016loosemt"
					elif "tight" in category:
						cut_type = "mssm2016tight"
					else:
						cut_type = "mssm2016full"
				
				if category != None:
					category_string = (global_category_string + "_{channel}_{category}").format(channel = channel, category = category)
				else:
					category_string = None
				
				for weight_up, weight_down in zip(args.weights_up, args.weights_down):
					json_config = {}
					json_filenames = [os.path.join(args.json_dir, "13TeV", channel_dir, quantity + ".json") for channel_dir in [channel, "default"]]
					for json_filename in json_filenames:
						json_filename = os.path.expandvars(json_filename)
						if os.path.exists(json_filename):
							json_config = jsonTools.JsonDict(json_filename).doIncludes().doComments()
							break
				
					quantity = json_config.pop("x_expressions", [quantity])[0]
					
					config_kwargs = {
						"samples" : list_of_samples,
						"channel" : channel,
						"category" : category_string,
						"higgs_masses" : args.higgs_masses,
						"normalise_signal_to_one_pb" : False,
						"ztt_from_mc" : True,
						"lumi " :  args.lumi * 1000,
						"exclude_cuts" : args.exclude_cuts + json_config.pop("exclude_cuts", []),
						"estimationMethod" : background_method,
						"mssm" : args.mssm,
						"cut_type" : global_cut_type,
						"no_ewk_samples" : args.no_ewk_samples,
						"no_ewkz_as_dy" : args.no_ewkz_as_dy,
					}
					
					config_up = sample_settings.get_config(
							weight = "((%s)*(%s))" % (json_config.pop("weights", ["1.0"])[0], weight_up),
							nick_suffix = "up",
							**config_kwargs
					)
					config_up["colors"] = ["kRed" for index in xrange(len(config_up.get("colors", [None])))]
					config_up["labels"] = ["shift up" for index in xrange(len(config_up.get("colors", [None])))]
					
					config_down = sample_settings.get_config(
							weight = "((%s)*(%s))" % (json_config.pop("weights", ["1.0"])[0], weight_down),
							nick_suffix = "down",
							**config_kwargs
					)
					config_down["colors"] = ["kGreen" for index in xrange(len(config_down.get("colors", [None])))]
					config_down["labels"] = ["shift down" for index in xrange(len(config_down.get("colors", [None])))]
				
					config_nominal = sample_settings.get_config(
							weight = "((%s)*(%s))" % (json_config.pop("weights", ["1.0"])[0], "1.0"),
							nick_suffix = "",
							**config_kwargs
					)
					config_nominal["colors"] = ["kBlack" for index in xrange(len(config_nominal.get("colors", [None])))]
					config_nominal["labels"] = ["nominal" for index in xrange(len(config_nominal.get("colors", [None])))]
					
					config = copy.deepcopy(config_up)
					config = samples.Samples.merge_configs(config, config_down)
					config = samples.Samples.merge_configs(config, config_nominal)

					config["x_expressions"] = [("0" if "pol_gen" in nick else json_config.pop("x_expressions", [quantity])) for nick in config["nicks"]]
					
					if "stacks" in config:
						config.pop("stacks")

					binning_string = None
					if args.mssm:
						binning_string = "binningHttMSSM13TeV"
					elif args.mva:
						binning_string = "binningMVAStudies"
					elif args.polarisation:
						binning_string = "binningZttPol13TeV"
					else:
						binning_string = "binningHtt13TeV"
					
					binnings_key = "{binning_string}{channel}{category}_{quantity}".format(
							binning_string=((binning_string+"_") if binning_string else ""),
							channel=channel,
							category=(("_"+category) if category else ""),
							quantity=quantity
					)
					if not binnings_key in binnings_settings.binnings_dict:
						binnings_key = channel+"_"+quantity
					if not binnings_key in binnings_settings.binnings_dict:
						binnings_key = None
					
					if not binnings_key is None:
						config["x_bins"] = [("1,-1,1" if "pol_gen" in nick else json_config.pop("x_bins", [binnings_key])) for nick in config["nicks"]]

					config["x_label"] = json_config.pop("x_label", channel+"_"+quantity)
					config["markers"] = ["ELINE"]*3
					config["legend_markers"] = ["ELP"]*3
					config["title"] = "channel_"+channel

					config["directories"] = [args.input_dir]
					config["filename"] = re.sub("[^a-zA-Z0-9]", "_", quantity+"__"+weight_up+"__"+weight_down)

					if args.ratio:
						if not "Ratio" in config.get("analysis_modules", []):
							config.setdefault("analysis_modules", []).append("Ratio")
						config.setdefault("ratio_numerator_nicks", []).extend([args.samples[0]+shift for shift in ["up", "down"]])
						config.setdefault("ratio_denominator_nicks", []).extend([args.samples[0]]*2)
						config.setdefault("ratio_result_nicks", []).extend(["ratio_up", "ratio_down"])
						config.setdefault("colors", []).extend(["kRed", "kGreen"])
						config.setdefault("markers", []).extend(["ELINE"]*2)
						config.setdefault("legend_markers", []).extend(["ELP"]*2)
						config.setdefault("labels", []).extend([""] * 2)
						config["sym_y_subplot_lims"] = 1.0

					for analysis_module in args.analysis_modules:
						if not analysis_module in config.get("analysis_modules", []):
							config.setdefault("analysis_modules", []).append(analysis_module)

					if log.isEnabledFor(logging.DEBUG) and (not "PrintInfos" in config.get("analysis_modules", [])):
						config.setdefault("analysis_modules", []).append("PrintInfos")

					if not "--y-log" in args.args:
						config["y_lims"] = [0.0]
					if args.cms:
						config["cms"] = True
						config["extra_text"] = "Preliminary"
						config["legend"] = [0.7, 0.4, 0.95, 0.83] if args.ratio else [0.7, 0.5, 0.9, 0.85]
						if not args.lumi is None:
							config["lumis"] = [float("%.1f" % args.lumi)]
						config["energies"] = [13]
						config["year"] = args.era
					else:
						config["y_rel_lims"] = [0.5, 10.0] if "--y-log" in args.args else [0.0, 1.5 if args.ratio else 1.4]
						config["legend"] = [0.23, 0.63, 0.9, 0.83] if args.ratio else [0.23, 0.73, 0.9, 0.89]
						config["legend_cols"] = 3

					config["output_dir"] = os.path.expandvars(os.path.join(
							args.output_dir,
							channel if len(args.channels) > 1 else "",
							category if len(args.categories) > 1 else ""
					))
				
					if not args.www is None:
						config["www"] = os.path.join(
								args.www,
								channel if len(args.channels) > 1 else "",
								"" if category is None else category
						)

					config.update(json_config)
				
					plot_configs.append(config)

	if log.isEnabledFor(logging.DEBUG):
		import pprint
		pprint.pprint(plot_configs)
		
	higgsplot.HiggsPlotter(list_of_config_dicts=plot_configs, list_of_args_strings=[args.args], n_processes=args.n_processes, n_plots=args.n_plots)

