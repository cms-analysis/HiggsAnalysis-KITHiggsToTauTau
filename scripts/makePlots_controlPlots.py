#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import argparse
import copy
import os
import sys

import Artus.Utility.jsonTools as jsonTools
import HiggsAnalysis.KITHiggsToTauTau.plotting.higgsplot as higgsplot
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.binnings as binnings
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.samples_run2 as samples


def add_s_over_sqrtb_subplot(config, args, bkg_samples, show_subplot, higgs_nick):
	if not "scale_nicks" in config.keys():
		config["scale_nicks"]=[]
		config["scales"]=[]
		config["scale_result_nicks"]=[]
	config["analysis_modules"].append("ScaleHistograms")
	config["scale_nicks"].append(higgs_nick)
	config["scales"].append(1.0/args.scale_signal)
	config["scale_result_nicks"].append("%s_SoB_Scaled"%higgs_nick)

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
		config["blinding_signal_nicks"].append("%s_SoB_Scaled"%higgs_nick)
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

def add_s_over_sqrtb_integral_subplot(config, args, bkg_samples, show_subplot, signal_samples):
	config["analysis_modules"].append("SignalOverBackgroundIntegral")
	config["sob_integral_background_nicks"] = []
	config["sob_integral_signal_nicks"] = []
	config["sob_integral_result_nicks"] = []
	config["sob_integral_method"] = []
	config["sob_integral_outputs"] = args.integration_output
	config["sob_integral_direction"]=[]
	for i,direction in enumerate(args.integration_directions):
		config["sob_integral_direction"].append(direction)
		config["sob_integral_method"].append(args.integration_methods)
		config["sob_integral_result_nicks"].append("integration_%i"%i + direction)
		config["sob_integral_background_nicks"].append(" ".join(bkg_samples))
		config["sob_integral_signal_nicks"].append(" ".join(signal_samples))
		#config["sob_integral_outputs"].append(args.integration_output)
	if(show_subplot):
		config["y_subplot_label"] = "int.(S)/#sqrt{int.(B)+int(S)}"
		config["y_subplot_lims"] = None
		config["subplot_nicks"] = ["integration"]
		for direction in args.integration_directions:
			config["markers"].append("LINE")
			config["legend_markers"].append("L")
			config["labels"].append("#int{S}/#sqrt{#int{B}}")
			if(direction == "righttoleft"):
				config["colors"].append("kit_blau_1")
			elif(direction == "lefttoright"):
				config["colors"].append("kit_rot_1")
			elif(direction == "rcombination"):
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
	                    default=["ztt", "zll", "ttj", "vv", "wj", "qcd", "data"],
	                    choices=["ztt", "zttpospol", "zttnegpol", "zll", "zl", "zj", "ttj", "vv", "wj", "qcd", "ewk", "ff", "ggh", "qqh", "vh", "htt", "data"],
	                    help="Samples. [Default: %(default)s]")
	parser.add_argument("--stack-signal", default=False, action="store_true",
	                    help="Draw signal (htt) stacked on top of each backgrounds. [Default: %(default)s]")
	parser.add_argument("--scale-signal", type=int, default=1,
	                    help="Scale signal (htt). Allowed values are 1, 10, 25, 100 and 250. [Default: %(default)s]")
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
	parser.add_argument("--blinding-variables", default=["all"], nargs="*",
	                    help="Variables to blind. [Default: %(default)s]")
	parser.add_argument("--integrated-sob", default=False, action="store_true",
	                    help="Add integrated s/sqrt(b) subplot [Default: %(default)s]")
	parser.add_argument("--integration-methods", default="soversqrtb", choices = ["soversqrtb", "soversplusb", "soversqrtsplusb"],
	                    help="Integration Method. [Default: %(default)s]")
	parser.add_argument("--integration-directions", default=["righttoleft", "righttoleft"], nargs="*",
	                    help="Integration direction. Chose lefttoright or righttoleft, !!!combination needs to be specified last!!!. [Default: %(default)s]")
	parser.add_argument("--integration-output", default=None,
						help="outputfile to specifiy where to write calculated maxima/minima, None is no output [Default:%(default)s]")
	parser.add_argument("--integration-nicks",nargs="+", default=["htt"],
						help="integration signal nicks [Default:%(default)s]")
	parser.add_argument("--integration-backgrounds", nargs="+", default=["all"],
						help="integration background nicks [Default:%(default)s]")
	parser.add_argument("--full-integral", action="store_true",
						help="calculate full integral of all histograms and write to file")
	parser.add_argument("-ff", "--fakefactor-method", choices = ["standard", "comparison"],
			help="Optional background estimation using the Fake-Factor method. [Default: %(default)s]")
	parser.add_argument("--scale-mc-only", default="1.0",
                        help="scales only MC events. [Default: %(default)s]")
	parser.add_argument("--cut-mc-only", default="1.0",
                        help="cut applied only on MC. [Default: %(default)s]")
	parser.add_argument("--project-to-lumi", default=1.0,
                        help="multiplies current lumi. 2 would mean double lumi you have right now [Default: %(default)s]")
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
	parser.add_argument("--run1", default=False, action="store_true",
	                    help="Use Run1 samples. [Default: %(default)s]")
	parser.add_argument("--cms", default=False, action="store_true",
	                    help="CMS Preliminary lable. [Default: %(default)s]")
	parser.add_argument("--lumi", type=float, default=samples.default_lumi/1000.0,
	                    help="Luminosity for the given data in fb^(-1). [Default: %(default)s]")
	parser.add_argument("-w", "--weight", default="1.0",
	                    help="Additional weight (cut) expression. [Default: %(default)s]")
	parser.add_argument("-e", "--exclude-cuts", nargs="+", default=[],
	                    help="Exclude (default) selection cuts. [Default: %(default)s]")
	parser.add_argument("-m", "--higgs-masses", nargs="+", default=["125"],
	                    help="Higgs masses. [Default: %(default)s]")
	parser.add_argument("--mssm", default=False, action="store_true",
	                    help="Produce the plots for the MSSM. [Default: %(default)s]")
	parser.add_argument("--qcd-subtract-shapes", action="store_false", default=True, help="subtract shapes for QCD estimation [Default:%(default)s]")
	parser.add_argument("--mva", default=False, action="store_true",
	                    help="Produce plots for the mva studies. [Default: %(default)s]")
	parser.add_argument("--analysis-modules", default=[], nargs="+",
	                    help="Additional analysis Modules. [Default: %(default)s]")
	parser.add_argument("--era", default="2015",
	                    help="Era of samples to be used. [Default: %(default)s]")
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
	parser.add_argument("--www", nargs="?", default=None, const="control_plots",
	                    help="Publish plots. [Default: %(default)s]")

	args = parser.parse_args()
	logger.initLogger(args)

	if not args.run1:
		if args.era == "2015":
			import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.samples_run2 as samples
		elif args.era == "2015new":
			import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.samples_run2_2015 as samples
		elif args.era == "2016":
			import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.samples_run2_2016 as samples
			if args.lumi == parser.get_default("lumi"):
				args.lumi = samples.default_lumi/1000.0
		else:
			log.critical("Invalid era string selected: " + args.era)
			sys.exit(1)
	else:
		import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.samples_run1 as samples

	if args.shapes:
		args.ratio = False

	if args.samples == parser.get_default("samples"):
		args.samples = [sample for sample in args.samples if hasattr(samples.Samples, sample)]
		if not args.run1:
			if "zl" in args.samples:
				args.samples.remove("zl") 
			if "zj" in args.samples:
				args.samples.remove("zj")
	if ("zj" in args.samples or "zl" in args.samples) and not args.run1:
		log.critical("Plot will fail: zl or zj samples given as input. Remove to continue")
		sys.exit(1)

	list_of_samples = [getattr(samples.Samples, sample) for sample in args.samples]
	sample_settings = samples.Samples()
	bkg_samples = [sample for sample in args.samples if sample not in ["data", "htt", "ggh", "qqh", "vh"]]
	sig_samples_raw = [sample for sample in args.samples if sample in ["htt", "ggh", "qqh", "vh"]]
	sig_samples = []
	for mass in args.higgs_masses:
		scale_str = "_%i"%args.scale_signal
		if int(args.scale_signal) == 1:
			scale_str = ""
		for sample in sig_samples_raw:
			#if sample is not "htt":
				#sig_samples.append(sample+"%s"%(mass))
			#else:
				#sig_samples.append(sample+"%s%s"%(mass, scale_str))
			sig_samples.append(sample+"%s%s"%(mass, scale_str))


	log.debug("used bkg + signal nicks")
	log.debug(" ".join(bkg_samples+sig_samples))
	binnings_settings = binnings.BinningsDict()


	args.categories = [None if category == "None" else category for category in args.categories]

	plot_configs = []
	for channel in args.channels:
		for category in args.categories:
			for quantity in args.quantities:
				category_string = None
				if category != None:
					if(args.mssm):
						category_string = "catHttMSSM13TeV"
					if args.mva:
						category_string = "catMVAStudies"
					else:
						category_string = "catHtt13TeV"
					category_string = (category_string + "_{channel}_{category}").format(channel=channel, category=category)
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
						category=category_string,
						higgs_masses=args.higgs_masses,
						normalise_signal_to_one_pb=False,
						ztt_from_mc=args.ztt_from_mc,
						weight="({0})*({1})".format(json_config.pop("weights", ["1.0"])[0], args.weight),
						lumi = args.lumi * 1000,
						exclude_cuts=args.exclude_cuts+json_config.pop("exclude_cuts", []),
						blind_expression=channel+"_"+quantity,
						fakefactor_method=args.fakefactor_method,
						stack_signal=args.stack_signal,
						scale_signal=args.scale_signal,
						project_to_lumi=args.project_to_lumi,
						cut_mc_only=args.cut_mc_only,
						scale_mc_only=args.scale_mc_only,
						mssm=args.mssm
				)


				config["x_expressions"] = json_config.pop("x_expressions", [quantity])
				config["category"] = category

				if(args.mssm):
						binning_string = "binningHttMSSM13TeV"
				if args.mva:
					binning_string = "binningMVAStudies"
				else:
					binning_string = "binningHtt13TeV"
				binnings_key = (binning_string + "_{channel}_{category}").format(channel=channel, category=category)
				if binnings_key in binnings_settings.binnings_dict:
					config["x_bins"] = json_config.pop("x_bins", [binnings_key])
				elif channel+"_"+quantity in binnings_settings.binnings_dict:
					binnings_key = channel+"_"+quantity
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
					config.setdefault("stacks", []).extend(["unc", "ratio"])


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
					config["legend"] = [0.7, 0.4, 0.95, 0.83] if args.ratio or args.integrated_sob or args.sbratio else [0.7, 0.5, 0.9, 0.85]
				elif args.shapes:
					config["legend"] = [0.55, 0.65, 0.9, 0.88]
				else:
					config["y_rel_lims"] = [0.5, 10.0] if "--y-log" in args.args else [0.0, 1.5 if args.ratio or args.integrated_sob or args.sbratio else 1.4]
					config["legend"] = [0.23, 0.63, 0.9, 0.83] if args.ratio or args.integrated_sob or args.sbratio else [0.23, 0.73, 0.9, 0.89]
					config["legend_cols"] = 3
				if not args.shapes:
					if not args.lumi is None:
						config["lumis"] = [float("%.1f" % args.lumi)]
					config["energies"] = [8] if args.run1 else [13]

				#add integrated s/sqrt(b) subplot
				if(args.integrated_sob):
					scale_nicks_temp = []
					scale_nicks = []
					replaced_sig_nicks = []
					replaced_bkg_nicks = []
					for sample in args.integration_nicks:
						if sample in sig_samples_raw and len(args.higgs_masses) > 1:
							log.fatal("found non specific signal nick %s while plotting more than 1 mass, please use [name][mass]_[scale_signal] as specifier"%(sample))
							sys.exit()
						elif sample in sig_samples_raw:
							replaced_sig_nicks += [nick for nick in sig_samples if sample in nick]
						elif sample in bkg_samples:
							replaced_sig_nicks.append(sample)

					for sample in args.integration_backgrounds:
						if sample in sig_samples_raw and len(args.higgs_masses) > 1:
							log.fatal("found non specific signal nick %s while plotting more than 1 mass, please use [name][mass]_[scale_signal] as specifier"%(sample))
							sys.exit()
						elif sample in sig_samples_raw:
							replaced_bkg_nicks += [nick for nick in sig_samples if sample in nick]
						elif sample in bkg_samples:
							replaced_bkg_nicks.append(sample)
						elif sample == "all":
							replaced_bkg_nicks += bkg_samples
					log.debug("replace bkg + signal nicks")
					log.debug(" ".join(replaced_bkg_nicks+replaced_sig_nicks))
					for sample in replaced_bkg_nicks+replaced_sig_nicks:
						nick = sample
						if sample in sig_samples_raw and len(args.higgs_masses) > 1:
							log.fatal("found non specific signal nick %s while plotting more than 1 mass, please use [name][mass]_[scale_signal] as specifier"%(sample))
							sys.exit()
						if nick in sig_samples and args.scale_signal != 1:
							scale_nicks_temp.append(sample)
					for nick in scale_nicks_temp:
						if nick not in scale_nicks:
							scale_nicks.append(nick)
					bkg_samples_used = [nick if nick not in scale_nicks else "%s_Scaled"%nick for nick in replaced_bkg_nicks]
					sig_samples_used = [nick if nick not in scale_nicks else "%s_Scaled"%nick for nick in replaced_sig_nicks]
					if not "scale_nicks" in config.keys():
						config["analysis_modules"].append("ScaleHistograms")
						config["scale_nicks"]=[]
						config["scales"]=[]
						config["scale_result_nicks"]=[]
					for sample in scale_nicks:
						config["scale_nicks"].append(sample)
						config["scales"].append(1.0/args.scale_signal)
						config["scale_result_nicks"].append(sample+"_Scaled")
					log.debug(config["scale_nicks"])
					log.debug(scale_nicks)
					log.debug(bkg_samples_used)
					log.debug(sig_samples_used)
					#sys.exit()
					add_s_over_sqrtb_integral_subplot(config, args, bkg_samples_used, args.integrated_sob, sig_samples_used)

				#add FullIntegral
				if(args.full_integral):
					bkg_samples_used = [nick for nick in bkg_samples if nick in config["nicks"]]
					hmass_temp = 125
					if len(args.higgs_masses) > 0 and "125" not in args.higgs_masses:
						hmass_temp = int(args.higgs_masses[0])
					sig_nick = "htt%i"%hmass_temp
					bkg_samples_used.append(sig_nick)
					config["full_integral_nicks"]=[" ".join(bkg_samples_used)]
					config["analysis_modules"].append("FullIntegral")

				# add s/sqrt(b) subplot
				if(args.sbratio or args.blinding_threshold > 0):
					bkg_samples_used = [nick for nick in bkg_samples if nick in config["nicks"]]
					higgs_temp = "htt125"
					if len(args.higgs_masses) > 0 and "125" not in args.higgs_masses:
						higgs_temp = "htt%i"%int(args.higgs_masses[0])
					for sample in sig_samples:
						if higgs_temp in sample:
							higgs_temp = sample
							break
					add_s_over_sqrtb_subplot(config, args, bkg_samples_used, args.sbratio, higgs_temp)

				if(args.blinding_threshold > 0):
					if(args.blinding_variables[0] == "all" or quantity in args.blinding_variables):
						blind_signal(config, args.blinding_threshold, args.ratio)

				config["output_dir"] = os.path.expandvars(os.path.join(
						args.output_dir,
						channel if len(args.channels) > 1 else "",
						category if len(args.categories) > 1 else ""
				))
				
				if "qcd" in bkg_samples:
					config["qcd_subtract_shape"] = [args.qcd_subtract_shapes]
				
				if not args.www is None:
					config["www"] = os.path.join(args.www, channel, "" if category is None else category)

				config.update(json_config)
				plot_configs.append(config)

	if log.isEnabledFor(logging.DEBUG):
		import pprint
		pprint.pprint(plot_configs)

	higgsplot.HiggsPlotter(list_of_config_dicts=plot_configs, list_of_args_strings=[args.args], n_processes=args.n_processes, n_plots=args.n_plots)

