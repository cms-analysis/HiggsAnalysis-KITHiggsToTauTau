#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import argparse
import copy
import os

import Artus.Utility.jsonTools as jsonTools

import HiggsAnalysis.KITHiggsToTauTau.plotting.higgsplot as higgsplot
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.binnings as binnings

import sys

def add_s_over_sqrtb_subplot(config, args, bkg_samples, show_subplot, higgsmass):
	config["analysis_modules"].append("ScaleHistograms")
	config["scale_nicks"] = ["htt%i"%higgsmass]
	config["scales"] = [ 1/args.scale_signal ]
	config["scale_result_nicks"] = ["htt%iScaled"%higgsmass]

	config["analysis_modules"].append("BlindingPolicy")
	config["blinding_background_nicks"] = []
	config["blinding_signal_nicks"] = []
	config["blinding_result_nicks"] = []
	config["blinding_parameters"] = []
	config["blinding_method"] = []
	for method in args.blinding_methods:
		config["blinding_method"].append(method)
		config["blinding_result_nicks"].append("blinding_" + method)
		config["blinding_background_nicks"].append(" ".join(bkg_samples))
		config["blinding_signal_nicks"].append("htt%iScaled"%higgsmass)
		config["blinding_parameters"].append(args.blinding_parameter)

	if( show_subplot ):
		config["y_subplot_label"] = ""
		config["subplot_lines"] = [0.1, 0.5, 1.0 ]
		config["y_subplot_lims"] = [0, 1.5]
		config["subplot_nicks"]=["blinding"]
		for method in args.blinding_methods:
			config["markers"].append("LINE")
			config["legend_markers"].append("L")
			if(method == "soversqrtb"):
				config["colors"].append("kit_blau_1")
				config["labels"].append("sbratio")
			elif(method == "ams"):
				config["colors"].append("kit_gruen_1")
				config["labels"].append("ams")
	else:
		config["nicks_blacklist"].append("blinding")

def add_s_over_sqrtb_integral_subplot(config, args, bkg_samples, show_subplot, signal_nick, higgsmass):
	config["analysis_modules"].append("ScaleHistograms")
	config["scale_nicks"] = ["%s%i"%(signal_nick, higgsmass)]
	config["scales"] = [ 1/args.scale_signal ]
	config["scale_result_nicks"] = ["%s%iScaled"%(signal_nick, higgsmass)]

	config["analysis_modules"].append("SignalOverBackgroundIntegral")
	config["sob_integral_background_nicks"] = []
	config["sob_integral_signal_nicks"] = []
	config["sob_integral_result_nicks"] = []
	config["sob_integral_method"] = []
	config["sob_integral_outputs"] = []
	for i,method in enumerate(args.integration_methods):
		config["sob_integral_method"].append(method)
		config["sob_integral_result_nicks"].append("integration_%i"%i + method)
		config["sob_integral_background_nicks"].append(" ".join(bkg_samples))
		config["sob_integral_signal_nicks"].append("htt%iScaled"%higgsmass)
		config["sob_integral_outputs"].append(args.integration_output)
	if(show_subplot):
		config["y_subplot_label"] = "int.(S)/#sqrt{int.(B)}"
		config["subplot_lines"] = [0.1, 0.5, 1.0 ]
		config["y_subplot_lims"] = [0, 1.5]
		config["subplot_nicks"] = ["integration"]
		for method in args.integration_methods:
			config["markers"].append("LINE")
			config["legend_markers"].append("L")
			config["labels"].append("#int{S}/#sqrt{#int{B}}")
			if(method == "righttoleft"):
				config["colors"].append("kit_blau_1")
			elif(method == "lefttoright"):
				config["colors"].append("kit_rot_1")
			elif(method == "rcombination"):
				config["colors"].append("kit_gruen_1")
	else:
		config["nicks_blacklist"].append("integration")

def blind_signal(config, blinding_threshold, ratio_true):
	config["analysis_modules"].append("MaskHistograms")
	config["mask_above_reference_nick"] = config["blinding_result_nicks"][0]
	config["mask_above_reference_value"] = blinding_threshold
	config["mask_histogram_nicks"] = "data"
	if ratio_true:
		config["mask_histogram_nicks"] = ["data", "ratio_Data"]

if __name__ == "__main__":

	parser = argparse.ArgumentParser(description="Make Data-MC control plots.",
	                                 parents=[logger.loggingParser])

	parser.add_argument("-i", "--input-dir", required=True,
	                    help="Input directory.")
	parser.add_argument("-s", "--samples", nargs="+",
	                    default=["ztt", "zll", "zl", "zj", "ttj", "vv", "wj", "qcd", "data"],
	                    choices=["ztt", "zll", "zl", "zj", "ttj", "vv", "wj", "qcd", "ggh", "qqh", "vh", "htt", "data"],
	                    help="Samples. [Default: %(default)s]")
	parser.add_argument("--stack-signal", default=False, action="store_true",
	                    help="Draw signal (htt) stacked on top of each backgrounds. [Default: %(default)s]")
	parser.add_argument("--scale-signal", type=float, default=1.0,
	                    help="Scale signal (htt). Allowed values are 1, 10, 25 and 100. [Default: %(default)s]")
	parser.add_argument("--sbratio", default=False, action="store_true",
	                    help="Add s/sqrt(b) subplot [Default: %(default)s]")
	parser.add_argument("--blinding-threshold", default=0, type=float,
	                    help="Threshold above of s/sqrt(b) above which data is being blinded [Default: %(default)s]")
	parser.add_argument("--ztt-from-mc", default=False, action="store_true",
	                    help="Use MC simulation to estimate ZTT. [Default: %(default)s]")
	parser.add_argument("--blinding-methods", default=["soversqrtb"], nargs="*",
	                    help="Blinding Method. Chose soversqrtb or ams. [Default: %(default)s]")
	parser.add_argument("--blinding-parameter", default=0.0, type=float,
	                    help="b_reg. [Default: %(default)s]")
	parser.add_argument("--integrated-sob", default=False, action="store_true",
	                    help="Add integrated s/sqrt(b) subplot [Default: %(default)s]")
	parser.add_argument("--integration-methods", default=["righttoleft", "righttoleft"], nargs="*",
	                    help="Integration Method. Chose lefttoright or righttoleft, !!!combination needs to be specified last!!!. [Default: %(default)s]")
	parser.add_argument("--integration-output", default=None,
						help="outputfile to specifiy where to write calculated maxima/minima, None is no output [Default:%(default)s]")
	parser.add_argument("--integration-nick", default="htt",
						help="integration signal nick [Default:%(default)s]")
	parser.add_argument("-c", "--channels", nargs="*",
	                    default=["tt", "mt", "et", "em", "mm", "ee"],
	                    help="Channels. [Default: %(default)s]")
	parser.add_argument("--categories", nargs="+", default=[None],
	                    help="Categories. [Default: %(default)s]")
	parser.add_argument("-x", "--quantities", nargs="*",
	                    default=["integral",
	                             "pt_1", "eta_1", "phi_1", "m_1", "iso_1", "mt_1",
	                             "pt_2", "eta_2", "phi_2", "m_2", "iso_2", "mt_2",
	                             "pt_ll", "eta_ll", "phi_ll", "m_ll", "mt_ll",
	                             "pt_llmet", "eta_llmet", "phi_llmet", "m_llmet", "mt_llmet",
	                             "mt_lep1met",
	                             "pt_sv", "eta_sv", "phi_sv", "svfitMass",
	                             "met", "metphi", "metcov00", "metcov01", "metcov10", "metcov11",
	                             "mvamet", "mvametphi", "mvacov00", "mvacov01", "mvacov10", "mvacov11",
	                             "pZetaMissVis", "pzetamiss", "pzetavis"
	                             "jpt_1_pt30", "jeta_1_pt30", "jphi_1_pt30",
	                             "jpt_2_pt30", "jeta_2_pt30", "jphi_2_pt30",
	                             "njetspt30", "mjj_pt30", "jdeta_pt30", "njetingap_pt30",
	                             "trigweight_1", "trigweight_2", "puweight",
	                             "npv", "npu", "rho"],
	                    help="Quantities. [Default: %(default)s]")
	parser.add_argument("-j", "--json-dir", default="$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/control_plots/",
	                    help="Base directory for optional JSON configs. [Default: %(default)s]")
	parser.add_argument("--run1", default=False, action="store_true",
	                    help="Use Run1 samples. [Default: %(default)s]")
	parser.add_argument("--cms", default=False, action="store_true",
	                    help="CMS Preliminary lable. [Default: %(default)s]")
	parser.add_argument("--lumi", type=float, default=2.301,
	                    help="Luminosity for the given data in fb^(-1). [Default: %(default)s]")
	parser.add_argument("-w", "--weight", default="1.0",
	                    help="Additional weight (cut) expression. [Default: %(default)s]")
	parser.add_argument("-e", "--exclude-cuts", nargs="+", default=[],
	                    help="Exclude (default) selection cuts. [Default: %(default)s]")
	parser.add_argument("-m", "--higgs-masses", nargs="+", default=["125"],
	                    help="Higgs masses. [Default: %(default)s]")
	parser.add_argument("--mssm", default=False, action="store_true",
	                    help="Produce the plots for the MSSM. [Default: %(default)s]")
	parser.add_argument("--analysis-modules", default=[], nargs="+",
	                    help="Additional analysis Modules. [Default: %(default)s]")
	parser.add_argument("-a", "--args", default="--plot-modules PlotRootHtt",
	                    help="Additional Arguments for HarryPlotter. [Default: %(default)s]")
	parser.add_argument("-r", "--ratio", default=False, action="store_true",
	                    help="Add ratio subplot. [Default: %(default)s]")
	parser.add_argument("--shapes", default=False, action="store_true",
	                    help="Show shape comparisons. [Default: %(default)s]")
	parser.add_argument("-n", "--n-processes", type=int, default=1,
	                    help="Number of (parallel) processes. [Default: %(default)s]")
	parser.add_argument("-f", "--n-plots", type=int,
	                    help="Number of plots. [Default: all]")
	parser.add_argument("-o", "--output-dir",
	                    default="$CMSSW_BASE/src/plots/control_plots/",
	                    help="Output directory. [Default: %(default)s]")
	parser.add_argument("--www", nargs="?", default=None, const="",
	                    help="Publish plots. [Default: %(default)s]")

	args = parser.parse_args()
	logger.initLogger(args)

	if not args.run1:
		import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.samples_run2 as samples
	else:
		import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.samples_run1 as samples

	if args.shapes:
		args.ratio = False

	if args.samples == parser.get_default("samples"):
		args.samples = [sample for sample in args.samples if hasattr(samples.Samples, sample)]
		if not args.run1:
			args.samples.remove("zl")
			args.samples.remove("zj")
	if ("zj" in args.samples or "zl" in args.samples) and not args.run1:
		log.error("plot will fail: zl or zj samples given as input. Remove to continue")
		sys.exit()
	www_output_dirs = []
	list_of_samples = [getattr(samples.Samples, sample) for sample in args.samples]
	sample_settings = samples.Samples()
	bkg_samples = [sample for sample in args.samples if sample != "data" and sample != "htt"]

	binnings_settings = binnings.BinningsDict()

	args.categories = [None if category == "None" else category for category in args.categories]

	plot_configs = []
	for channel in args.channels:
		for category in args.categories:
			for quantity in args.quantities:

				json_config = {}
				json_filenames = [os.path.join(args.json_dir, "8TeV" if args.run1 else "13TeV", channel_dir, quantity+".json") for channel_dir in [channel, "default"]]
				for json_filename in json_filenames:
					json_filename = os.path.expandvars(json_filename)
					if os.path.exists(json_filename):
						json_config = jsonTools.JsonDict(json_filename).doIncludes().doComments()
						break
				quantity = json_config.pop("x_expressions", [quantity])[0]

				config = sample_settings.get_config(
						samples=list_of_samples,
						channel=channel,
						category=category if not args.mssm else "catHttMSSM13TeV_{channel}_{category}".format(channel=channel, category=category),
						higgs_masses=args.higgs_masses,
						normalise_signal_to_one_pb=False,
						ztt_from_mc=args.ztt_from_mc,
						weight="({0})*({1})".format(json_config.pop("weights", ["1.0"])[0], args.weight),
						lumi = args.lumi * 1000,
						exclude_cuts=args.exclude_cuts+json_config.pop("exclude_cuts", []),
						blind_expression=channel+"_"+quantity,
						stack_signal=args.stack_signal,
						scale_signal=args.scale_signal,
						mssm=args.mssm
				)

				config["x_expressions"] = json_config.pop("x_expressions", [quantity])

				binnings_key = channel+"_"+quantity
				if binnings_key in binnings_settings.binnings_dict:
					config["x_bins"] = json_config.pop("x_bins", [binnings_key])
				config["x_label"] = json_config.pop("x_label", channel+"_"+quantity)

				config["title"] = "channel_"+channel

				config["directories"] = [args.input_dir]

				if args.shapes:
					if "stacks" in config:
						config.pop("stacks")
					if not "NormalizeToUnity" in config.get("analysis_modules", []):
						config.setdefault("analysis_modules", []).append("NormalizeToUnity")
					config["y_label"] = "arb. u."
					config["markers"] = "LINE"
					config["legend_markers"] = "L"
					config["line_widths"] = 3

				if args.ratio:
					bkg_samples_used = [nick for nick in bkg_samples if nick in config["nicks"]]
					if not "Ratio" in config.get("analysis_modules", []):
						config.setdefault("analysis_modules", []).append("Ratio")
					config.setdefault("ratio_numerator_nicks", []).extend([" ".join(bkg_samples_used), "data"])
					config.setdefault("ratio_denominator_nicks", []).extend([" ".join(bkg_samples_used)] * 2)
					config.setdefault("ratio_result_nicks", []).extend(["ratio_MC", "ratio_Data"])
					config.setdefault("colors", []).extend(["#000000"] * 2)
					config.setdefault("markers", []).extend(["E2", "E"])
					config.setdefault("legend_markers", []).extend(["ELP"]*2)
					config.setdefault("labels", []).extend([""] * 2)

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
				elif args.shapes:
					config["legend"] = [0.55, 0.65, 0.9, 0.88]
				else:
					config["y_rel_lims"] = [0.5, 10.0] if "--y-log" in args.args else [0.0, 1.5 if args.ratio else 1.4]
					config["legend"] = [0.23, 0.63, 0.9, 0.83] if args.ratio else [0.23, 0.73, 0.9, 0.89]
					config["legend_cols"] = 3
				if not args.shapes:
					if not args.lumi is None:
						config["lumis"] = [float("%.1f" % args.lumi)]
					config["energies"] = [8] if args.run1 else [13]

				#add integrated s/sqrt(b) subplot
				if(args.integrated_sob):
					bkg_samples_used = [nick for nick in bkg_samples if nick in config["nicks"]]
					hmass_temp = 125
					if len(args.higgs_masses) > 0 and "125" not in args.higgs_masses:
						hmass_temp = int(args.higgs_masses[0])
					add_s_over_sqrtb_integral_subplot(config, args, bkg_samples_used, args.integrated_sob, args.integration_nick, hmass_temp)
				# add s/sqrt(b) subplot
				if(args.sbratio or args.blinding_threshold > 0):
					bkg_samples_used = [nick for nick in bkg_samples if nick in config["nicks"]]
					hmass_temp = 125
					if len(args.higgs_masses) > 0 and "125" not in args.higgs_masses:
						hmass_temp = int(args.higgs_masses[0])
					add_s_over_sqrtb_subplot(config, args, bkg_samples_used, args.sbratio, hmass_temp)

				if(args.blinding_threshold > 0):
					blind_signal(config, args.blinding_threshold, args.ratio)

				config["output_dir"] = os.path.expandvars(os.path.join(
						args.output_dir,
						channel if len(args.channels) > 1 else "",
						category if len(args.categories) > 1 else ""
				))
				if not (config["output_dir"] in www_output_dirs):
					www_output_dirs.append(config["output_dir"])


				config.update(json_config)
				plot_configs.append(config)

	if log.isEnabledFor(logging.DEBUG):
		import pprint
		pprint.pprint(plot_configs)

	higgsplot.HiggsPlotter(list_of_config_dicts=plot_configs, list_of_args_strings=[args.args], n_processes=args.n_processes, n_plots=args.n_plots)

	if not args.www is None:
		for output_dir in www_output_dirs:
			from Artus.HarryPlotter.plotdata import PlotData
			subpath =os.path.normpath(output_dir).split("/")[-1]
			output_filenames = []
			for config in plot_configs:
				if(subpath in config["output_dir"]):
					output_filenames.append(os.path.join(output_dir, config["x_expressions"][0]+ ".png"))

			PlotData.webplotting(
			             www = args.www if(subpath == "control_plots") else os.path.join(args.www, subpath),
			             output_dir = output_dir,
			             export_json = False,
			             output_filenames = output_filenames
			             )
