#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import argparse
import copy
import os
import sys
import re

import Artus.Utility.jsonTools as jsonTools
import HiggsAnalysis.KITHiggsToTauTau.plotting.higgsplot as higgsplot
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.binnings as binnings
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.samples_run2_2015 as samples


if __name__ == "__main__":

	parser = argparse.ArgumentParser(description="Study impact of theoretical uncertainties.",
	                                 parents=[logger.loggingParser])

	parser.add_argument("-i", "--input-dir", required=True,
	                    help="Input directory.")
	parser.add_argument("-s", "--samples", nargs="+", required=True,
	                    help="Samples. [Default: %(default)s]")
	parser.add_argument("-c", "--channels", nargs="*",
	                    default=["tt", "mt", "et", "em", "mm"],
	                    help="Channels. [Default: %(default)s]")
	parser.add_argument("--categories", nargs="+", default=[None],
	                    help="Categories. [Default: %(default)s]")
	parser.add_argument("-x", "--quantities", nargs="+", required=True,
	                    help="Quantities. [Default: %(default)s]")
	parser.add_argument("-j", "--json-dir", default="$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/control_plots/",
	                    help="Base directory for optional JSON configs. [Default: %(default)s]")
	parser.add_argument("--cms", default=False, action="store_true",
	                    help="CMS Preliminary lable. [Default: %(default)s]")
	parser.add_argument("--lumi", type=float, default=samples.default_lumi/1000.0,
	                    help="Luminosity for the given data in fb^(-1). [Default: %(default)s]")
	parser.add_argument("-w", "--weights", nargs="+", required=True,
	                    help="LHE weights to shift nominal histogram and estimate effect on acceptances.")
	parser.add_argument("--evaluate-alpha-s-uncertainties", default=False, action="store_true",
	                    help="Run analysis module for alpha_s uncertainty evaluation. [Default: %(default)s]")
	parser.add_argument("--evaluate-pdf-uncertainties", default=False, action="store_true",
	                    help="Run analysis module for PDF uncertainty evaluation. [Default: %(default)s]")
	parser.add_argument("--evaluate-scale-uncertainties", default=False, action="store_true",
	                    help="Run analysis module for scale (muR and muF) uncertainty evaluation. [Default: %(default)s]")
	parser.add_argument("-e", "--exclude-cuts", nargs="+", default=[],
	                    help="Exclude (default) selection cuts. [Default: %(default)s]")
	parser.add_argument("--controlregions", action="store_true", default=False,
	                    help="Also create histograms for control regions. [Default: %(default)s]")
	parser.add_argument("-m", "--higgs-masses", nargs="+", default=["125"],
	                    help="Higgs masses. [Default: %(default)s]")
	parser.add_argument("--qcd-subtract-shapes", action="store_false", default=True, help="subtract shapes for QCD estimation [Default:%(default)s]")
	parser.add_argument("--background-method", default=["new"], nargs="+",
	                    help="Background estimation method to be used, channel dependent. [Default: %(default)s]")
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
	parser.add_argument("-b", "--batch", default=None, const="rwthcondor", nargs="?",
	                    help="Run with grid-control. Optionally select backend. [Default: %(default)s]")
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
	elif args.era == "2017":
		import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.samples_run2_2017 as samples
		if args.lumi == parser.get_default("lumi"):
			args.lumi = samples.default_lumi/1000.0
	else:
		log.critical("Invalid era string selected: " + args.era)
		sys.exit(1)
	
	if args.polarisation:
		args.no_ewkz_as_dy = True

	sample_settings = samples.Samples()
	binnings_settings = binnings.BinningsDict()

	args.categories = [None if category == "None" else category for category in args.categories]

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
	elif args.lfv:
		global_category_string = "catLFV13TeV"
	elif args.polarisation:
		global_category_string = "catZttPol13TeV"
		global_cut_type = "low_mvis_smhtt"
	elif args.taues:
		global_cut_type = "tauescuts"
	elif args.cp:
		global_cut_type = "cp"
	elif args.cprho:
		global_cut_type = "cprho"
	elif args.cpcomb:
		global_cut_type = "cpcomb"
	elif args.etaufakerate:
		global_category_string = "catETauFakeRate13TeV"
		global_cut_type = "etaufake"
		if args.categories == [None]:
			args.categories = ["vloose_pass", "vloose_fail", "loose_pass", "loose_fail", "medium_pass", "medium_fail", "tight_pass", "tight_fail", "vtight_pass", "vtight_fail"]
		log.info("Use the following option to exclude the necessary cuts for etaufakerate studies: [ --exclude-cuts 'dilepton_veto' 'extra_lepton_veto' 'anti_e_tau_discriminators' ]")
	if args.era == "2016":
		if args.smhtt:
			global_cut_type = "smhtt"
		if args.cpggh:
			global_cut_type = "cpggh"
		global_cut_type += "2016"

	evaluate_uncertainties = args.evaluate_alpha_s_uncertainties or args.evaluate_pdf_uncertainties or args.evaluate_scale_uncertainties

	# Configs construction for HP
	for sample in args.samples:
		for category in args.categories:
			for index_quantity, quantity in enumerate(args.quantities):

				channels_background_methods = zip(args.channels, args.background_method)
				channel_config = {}
				for index_channel, (channel, background_method) in enumerate(channels_background_methods):
					if args.mssm:
						cut_type = "mssm2016full"
						if args.era == "2016":
							cut_type = "mssm2016"
						elif "looseiso" in category:
							cut_type = "mssm2016looseiso"
						elif "loosemt" in category:
							cut_type = "mssm2016loosemt"
						elif "tight" in category:
							cut_type = "mssm2016tight"

					if args.etaufakerate:
						# TODO: add the default global_cut_type
						if "vloose_pass" in category:
							global_cut_type = "etaufake2016_antievloosepass"
						elif "vloose_fail" in category:
							global_cut_type = "etaufake2016_antievloosefail"
						elif "loose_pass" in category:
							global_cut_type = "etaufake2016_antieloosepass"
						elif "loose_fail" in category:
							global_cut_type = "etaufake2016_antieloosefail"
						elif "medium_pass" in category:
							global_cut_type = "etaufake2016_antiemediumpass"
						elif "medium_fail" in category:
							global_cut_type = "etaufake2016_antiemediumfail"
						elif "tight_pass" in category:
							global_cut_type = "etaufake2016_antietightpass"
						elif "tight_fail" in category:
							global_cut_type = "etaufake2016_antietightfail"
						elif "vtight_pass" in category:
							global_cut_type = "etaufake2016_antievtightpass"
						elif "vtight_fail" in category:
							global_cut_type = "etaufake2016_antievtightfail"

					last_loop = index_channel == len(channels_background_methods) - 1

					category_string = None
					if category != None:
						category_string = (global_category_string + "_{channel}_{category}").format(channel = channel, category = category)

					json_config = {}
					json_filenames = [os.path.join(args.json_dir, "13TeV", channel_dir, quantity + ".json") for channel_dir in [channel, "default"]]
					for json_filename in json_filenames:
						json_filename = os.path.expandvars(json_filename)
						if os.path.exists(json_filename):
							json_config = jsonTools.JsonDict(json_filename).doIncludes().doComments()
							break

					quantity = json_config.pop("x_expressions", [quantity])[0]
					
					config = {}
					for index_weight, weight in enumerate(["1.0"]+args.weights):
						weight_config = sample_settings.get_config(
								samples = [getattr(samples.Samples, sample)],
								channel = channel,
								category = category_string,
								higgs_masses = args.higgs_masses,
								normalise_signal_to_one_pb = False,
								weight = "((%s)*(%s))" % (json_config.get("weights", ["1.0"])[0], weight),
								lumi  =  args.lumi * 1000,
								exclude_cuts = args.exclude_cuts + json_config.get("exclude_cuts", []),
								blind_expression = channel + "_" + quantity,
								estimationMethod = background_method,
								mssm = args.mssm,
								controlregions = args.controlregions,
								cut_type = global_cut_type,
								no_ewk_samples = args.no_ewk_samples,
								no_ewkz_as_dy = args.no_ewkz_as_dy,
								nick_suffix = "" if index_weight == 0 else (weight + ("_noplot" if evaluate_uncertainties else ""))
								#polarisation_bias_correction=True,
								#polarisation_gen_ztt_plots=False,
						)
						config = samples.Samples.merge_configs(config, weight_config)
					
					if "weights" in json_config:
						json_config.pop("weights")
					if "exclude_cuts" in json_config:
						json_config.pop("exclude_cuts")
					
					x_expression = json_config.pop("x_expressions", [quantity])
					config["x_expressions"] = [("0" if (("gen_zttpospol" in nick) or ("gen_zttnegpol" in nick)) else x_expression) for nick in config["nicks"]]
					config["category"] = category

					# Introduced due to missing samples in 2017 MCv1, can be removed when 2017 MCv2 samples are out, and samples_rnu2_2017.py script is updated correspondingly.
					if args.era == "2017":
						sub_conf_index = 0
						while (sub_conf_index < len(config["files"])):
							if config["files"][sub_conf_index] is None:
								config["files"].pop(sub_conf_index)
								config["x_expressions"].pop(sub_conf_index)
								config["scale_factors"].pop(sub_conf_index)
								config["folders"].pop(sub_conf_index)
								config["weights"].pop(sub_conf_index)
								config["nicks"].pop(sub_conf_index)
							else:
								sub_conf_index +=1

					binning_string = "binningHtt13TeV"
					if args.mssm:
						binning_string = "binningHttMSSM13TeV"
					elif args.mva:
						binning_string = "binningMVAStudies"
					elif args.polarisation:
						binning_string = "binningZttPol13TeV"

					binnings_key = "{binning_string}{channel}{category}_{quantity}".format(
							binning_string = binning_string + "_" if binning_string else "",
							channel = channel,
							category = "_" + category if category else "",
							quantity = quantity
					)
					if binnings_key not in binnings_settings.binnings_dict and channel + "_" + quantity in binnings_settings.binnings_dict and "--x-bins" not in args.args:
						binnings_key = channel + "_" + quantity
					if binnings_key not in binnings_settings.binnings_dict:
						binnings_key = None
					
					if binnings_key is not None and "--x-bins" not in args.args:
						x_bins = json_config.pop("x_bins", [binnings_key])
						config["x_bins"] = [("1,-1,1" if (("gen_zttpospol" in nick) or ("gen_zttnegpol" in nick)) else x_bins) for nick in config["nicks"]]
					elif "--x-bins" in args.args:
						x_binning = re.search("(--x-bins)[\s=\"\']*(?P<x_bins>\S*)[\"\']?\S", args.args)
						config["x_bins"] = [" ".join(x_binning.group(2))]
					
					if "stacks" in config:
						config.pop("stacks")
					
					n_shifted_plots = 2 if evaluate_uncertainties else len(args.weights)
					config["markers"] = ["E"]+(["LINE"] * n_shifted_plots)
					config["legend_markers"] = ["ELP"]+(["L"] * n_shifted_plots)
					config["colors"] = [str(color+1) for color in range(n_shifted_plots+1)]
					
					config["x_label"] = json_config.pop("x_label", channel + "_" + quantity)
					config["labels"] = ["nominal"]+ (["shift up", "shift down"] if evaluate_uncertainties else args.weights)

					if args.polarisation:
						config["title"] = "channel_" + channel + ("" if category is None else ("_"+category))
					else:
						config["title"] = "channel_" + channel

					config["directories"] = [args.input_dir]
					
					if args.evaluate_alpha_s_uncertainties:
						if "UncertaintiesAlphaS" not in config.get("analysis_modules", []):
							config.setdefault("analysis_modules", []).append("UncertaintiesAlphaS")
						config.setdefault("uncertainties_alpha_s_reference_nicks", []).append(sample)
						config.setdefault("uncertainties_alpha_s_shifts_nicks", []).append(" ".join([sample+weight+"_noplot" for weight in args.weights]))
						config.setdefault("uncertainties_alpha_s_result_nicks", []).append(sample)
					
					if args.evaluate_pdf_uncertainties:
						if "UncertaintiesPdf" not in config.get("analysis_modules", []):
							config.setdefault("analysis_modules", []).append("UncertaintiesPdf")
						config.setdefault("uncertainties_pdf_reference_nicks", []).append(sample)
						config.setdefault("uncertainties_pdf_shifts_nicks", []).append(" ".join([sample+weight+"_noplot" for weight in args.weights]))
						config.setdefault("uncertainties_pdf_result_nicks", []).append(sample)
					
					if args.evaluate_scale_uncertainties:
						if "UncertaintiesScale" not in config.get("analysis_modules", []):
							config.setdefault("analysis_modules", []).append("UncertaintiesScale")
						config.setdefault("uncertainties_scale_reference_nicks", []).append(sample)
						config.setdefault("uncertainties_scale_shifts_nicks", []).append(" ".join([sample+weight+"_noplot" for weight in args.weights]))
						config.setdefault("uncertainties_scale_result_nicks", []).append(sample)
					
					if args.ratio:
						if "Ratio" not in config.get("analysis_modules", []):
							config.setdefault("analysis_modules", []).append("Ratio")
						config.setdefault("ratio_numerator_nicks", []).extend([sample+weight for weight in (["_up", "_down"] if evaluate_uncertainties else args.weights)])
						config.setdefault("ratio_denominator_nicks", []).extend([sample] * n_shifted_plots)
						config.setdefault("ratio_result_nicks", []).extend(["ratio"+weight for weight in (["_up", "_down"] if evaluate_uncertainties else args.weights)])
						config.setdefault("colors", []).extend([str(color+1) for color in range(1, n_shifted_plots+1)])
						config.setdefault("markers", []).extend(["LINE"] * n_shifted_plots)
						config.setdefault("legend_markers", []).extend(["L"] * n_shifted_plots)
						config.setdefault("labels", []).extend([""] * n_shifted_plots)

					if log.isEnabledFor(logging.DEBUG) and "PrintInfos" not in config.get("analysis_modules", []):
						config.setdefault("analysis_modules", []).append("PrintInfos")

					if "--y-log" not in args.args:
						config["y_lims"] = [0.0]
					if args.cms:
						config["cms"] = True
						config["extra_text"] = "Preliminary"
						config["legend"] = [0.7, 0.4, 0.95, 0.83] if args.ratio else [0.7, 0.5, 0.9, 0.85]
					config["y_rel_lims"] = [0.5, 10.0] if "--y-log" in args.args else [0.0, 1.4]
					config["legend"] = [0.23, 0.63, 0.9, 0.83] if args.ratio else [0.23, 0.73, 0.9, 0.89]
					config["legend_cols"] = 3
					
					if args.lumi is not None:
						config["lumis"] = [float("%.1f" % args.lumi)]
					config["energies"] = [13]
					config["year"] = args.era

					config["output_dir"] = os.path.expandvars(os.path.join(
							args.output_dir,
							channel,
							"" if category is None else category,
							sample
					))

					if not args.www is None:
						config["www"] = os.path.join(
								args.www,
								channel,
								"" if category is None else category,
								sample
						)

					config.update(json_config)

					plot_configs.append(config)

	if log.isEnabledFor(logging.DEBUG):
		import pprint
		pprint.pprint(plot_configs)
	higgsplot.HiggsPlotter(
			list_of_config_dicts=plot_configs, list_of_args_strings=[args.args],
			n_processes=args.n_processes, n_plots=args.n_plots, batch=args.batch
	)
