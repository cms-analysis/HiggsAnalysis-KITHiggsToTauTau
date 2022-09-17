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

	parser = argparse.ArgumentParser(description="Make Data-MC control plots.",
	                                 parents=[logger.loggingParser])

	parser.add_argument("-i", "--input-dir", required=True,
	                    help="Input directory.")
	parser.add_argument("-s", "--samples", nargs="+",
	                    default=["ztt", "zll", "ttj", "vv", "wj", "qcd", "data"],
	                    help="Samples. [Default: %(default)s]")
	parser.add_argument("--use-asimov-dataset", default=None, const="", nargs="?",
						help="Use expectation as observation instead of real data. Specify the nickts of samples (separated by whitespaces) to be used as expectation. [Default: all samples plotted appart from data]")
	parser.add_argument("--stack-signal", default=False, action="store_true",
	                    help="Draw signal (htt) stacked on top of each backgrounds. [Default: %(default)s]")
	parser.add_argument("--scale-signal", type=int, default=1,
	                    help="Scale signal (htt). Allowed values are 1, 10, 25, 100 and 250. [Default: %(default)s]")
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
	parser.add_argument("-ff", "--fakefactor-method", default=False, action="store_true",
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
	parser.add_argument("-fs", "--final-state", nargs="*",
	                    default=[],
                        help="Final states. Overwrites channels. Choices \"a1e\", \"a1mu\", \"a1pi\", \"a1rho\", \"a1a1\". [Default: %(default)s]")
	parser.add_argument("--categories", nargs="+", default=[None],
	                    help="Categories. [Default: %(default)s]")
	parser.add_argument("-x", "--quantities", nargs="+",
	                    default=[
							"simpleFitConverged",
							"simpleFitCsum",
							"simpleFitNiterations",
							# "simpleFitIndex:genSimpleFitIndex2",
							#
							"simpleFitTau1LV-genMatchedTau1LV",
							"simpleFitTau2LV-genMatchedTau2LV",
							"simpleFitLV-genBosonLV",
							#
							"simpleFitTau1LV-simpleFitTau1ResolvedGenLV",
							"simpleFitTau2LV-simpleFitTau2ResolvedGenLV",

							"simpleFitTau1ResolvedGenLV-genMatchedTau1LV",
							"simpleFitTau2ResolvedGenLV-genMatchedTau2LV",

							"simpleFitTau1LV-simpleFitTau1PrefitResolvedGenLV",
							"simpleFitTau2LV-simpleFitTau2PrefitResolvedGenLV",
							# "simpleFitTau1LV-simpleFitTau1PrefitResolvedFitLV",
							# "simpleFitTau2LV-simpleFitTau2PrefitResolvedFitLV",

							# "simpleFitLV-simpleFitResonancePrefitResolvedFitLV",
							# "simpleFitLV-simpleFitResonancePrefitResolvedGenLV",
							# #
							# "simpleFitTau1PrefitResolvedGenLV-genMatchedTau1LV",
							# "simpleFitTau2PrefitResolvedGenLV-genMatchedTau2LV",
							# "simpleFitTau1PrefitResolvedFitLV-genMatchedTau1LV",
							# "simpleFitTau2PrefitResolvedFitLV-genMatchedTau2LV",
							# "simpleFitResonancePrefitResolvedFitLV-genBosonLV",
							# "simpleFitResonancePrefitResolvedGenLV-genBosonLV",

							"recoPhiStarCPPolVecTauOneProngTauA1",
							"recoPhiStarCPRhoMerged",
						],
	                    help="Quantities. [Default: %(default)s]")
	parser.add_argument("-j", "--json-dir", default="$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/control_plots/",
	                    help="Base directory for optional JSON configs. [Default: %(default)s]")
	parser.add_argument("--cms", default=False, action="store_true",
	                    help="CMS Preliminary lable. [Default: %(default)s]")
	parser.add_argument("--lumi", type=float, default=samples.default_lumi/1000.0,
	                    help="Luminosity for the given data in fb^(-1). [Default: %(default)s]")
	parser.add_argument("-w", "--weights", default=["1.0"], nargs="+",
	                    help="Additional weight (cut) expressions. The list of weigths is repeated until it matches the number of quantities [Default: %(default)s]")
	parser.add_argument("-e", "--exclude-cuts", nargs="+", default=[],
	                    help="Exclude (default) selection cuts. [Default: %(default)s]")
	parser.add_argument("--controlregions", action="store_true", default=False,
	                    help="Also create histograms for control regions. [Default: %(default)s]")
	parser.add_argument("-m", "--higgs-masses", nargs="+", default=["125"],
	                    help="Higgs masses. [Default: %(default)s]")
	parser.add_argument("--background-method", default=["new"], nargs="+",
	                    help="Background estimation method to be used, channel dependent. [Default: %(default)s]")
	parser.add_argument("--smhtt", default=False, action="store_true",
	                    help="Produce the plots for the SM HTT analysis. [Default: %(default)s]")
	parser.add_argument("--cpggh", default=False, action="store_true",
			    help="Produce plots for the Higgs CP ggH analysis. [Default: %(default)s]")
	parser.add_argument("--cptautau", default=False, action="store_true",
				help="Produce plots for the Higgs CP tau tau final state analysis. [Default: %(default)s]")
	parser.add_argument("--cp", default=False, action="store_true",
	                    help="Produce the plots for the CP analysis. [Default: %(default)s]")  #TODO instead of 3 different boolean flag, change to option with 3 possible values
	parser.add_argument("--analysis-modules", default=[], nargs="+",
	                    help="Additional analysis Modules. [Default: %(default)s]")
	parser.add_argument("--add-analysis-modules-before-ratio", default=False, action="store_true",
	                    help="Analysis modules are called according to their position in the list of analysis modules. This option stores them after the call of the ratio option. [Default: %(default)s]")
	parser.add_argument("--era", default="2016",
	                    help="Era of samples to be used. [Default: %(default)s]")
	parser.add_argument("-a", "--args", default="--plot-modules PlotRootHtt",
	                    help="Additional Arguments for HarryPlotter. [Default: %(default)s]")
	parser.add_argument("-r", "--ratio", default=False, action="store_true",
	                    help="Add ratio subplot. [Default: %(default)s]")
	parser.add_argument("--ratio-subplot", default=False, action="store_true",
	                    help="Add a subplot showing the relative fraction of the processes per bin. [Default: %(default)s]")
	parser.add_argument("--shapes", default=False, action="store_true",
	                    help="Show shape comparisons. [Default: %(default)s]")
	parser.add_argument("--channel-comparison", default=False, action="store_true",
	                    help="Show channel comparisons. [Default: %(default)s]")
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
	parser.add_argument("--emb", default=False, action="store_true",
	                    help="Use embedded samples. [Default: %(default)s]")
	parser.add_argument("--ttbar-retuned", default=False, action="store_true",
	                    help="Use retuned ttbar samples. [Default: %(default)s]")
	parser.add_argument("--embedded-weights", default=['1.0','1.0','1.0','1.0'], nargs='*',
	                    help="Custom Embedding weights for mt, et, em, tt (in this order). [Default: %(default)s]")
	parser.add_argument("--no-ewk-samples", default=False, action="store_true",
	                    help="Do not use EWK Z/W samples. [Default: %(default)s]")
	parser.add_argument("--no-ewkz-as-dy", default=False, action="store_true",
	                    help="Do not include EWKZ samples in inputs for DY. [Default: %(default)s]")
	parser.add_argument("--inclusive-diboson-samples", default=False, action="store_true",
	                    help="Use inclusive Diboson Samples. [Default: %(default)s]")
	parser.add_argument("--use-proxy-fakefactors", default=False, action="store_true",
	                    help="Use proxy to calculate fake factors. [Default: %(default)s]")
	parser.add_argument("--legacy", default=False, action="store_true",
	                    help="Use legacy Samples and Settings. [Default: %(default)s]")
	parser.add_argument("--nicks-blacklist", default=False, action="store_true",
	                    help="Blacklist all background and data. [Default: %(default)s]")
	args = parser.parse_args()
	logger.initLogger(args)

	if (args.era == "2015") or (args.era == "2015new"):
		import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.samples_run2_2015 as samples
	elif args.era == "2016":
		import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.samples_run2_2016 as samples
		if args.lumi == parser.get_default("lumi"):
			args.lumi = samples.default_lumi/1000.0
	elif args.era == "2017":
		import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.samples_run2_2017_mcv2 as samples
		if args.lumi == parser.get_default("lumi"):
			args.lumi = samples.default_lumi/1000.0
	elif args.era == "2018":
		import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.samples_run2_2018 as samples
		if args.lumi == parser.get_default("lumi"):
			args.lumi = samples.default_lumi/1000.0
	else:
		log.critical("Invalid era string selected: " + args.era)
		sys.exit(1)

	if args.shapes:
		args.ratio = False
		args.ratio_subplot = False

	if args.samples == parser.get_default("samples"):
		args.samples = [sample for sample in args.samples if hasattr(samples.Samples, sample)]

	list_of_samples = [getattr(samples.Samples, sample) for sample in args.samples]
	asimov_nicks = []
	if not (args.use_asimov_dataset is None):
		args.use_asimov_dataset = args.use_asimov_dataset.split()
		asimov_nicks = copy.deepcopy(args.samples if len(args.use_asimov_dataset) == 0 else args.use_asimov_dataset)
		if "data" in asimov_nicks:
			asimov_nicks.remove("data")

	sample_settings = samples.Samples(embedding=args.emb,embedding_weight=args.embedded_weights,ttbar_retuned=args.ttbar_retuned,legacy=args.legacy)

	bkg_samples = [sample for sample in args.samples if sample not in ["data", "htt", "ggh", "qqh", "vh"]]
	sig_samples_raw = [sample for sample in args.samples if sample in ["htt", "ggh", "qqh", "vh", "gghjhusm", "gghjhumm", "gghjhups", "qqhjhusm", "qqhjhumm", "qqhjhups"]]

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
			sig_samples.append(sample + "%s%s"%(mass, scale_str))

	log.debug("used bkg + signal nicks")
	log.debug(" ".join(bkg_samples+sig_samples))
	binnings_settings = binnings.BinningsDict()

	args.categories = [None if category == "None" else category for category in args.categories]

	plot_configs = []
	channels = []
	final_states = args.final_state
	background_methods = args.background_method
	# fill in hp-style

	all_finalstates = {
		"et": ["a1e"],
		"mt": ["a1mu"],
		"tt": ["a1a1", "a1pi", "a1rho"]
	}

	if args.final_state:
		for state in args.final_state:
			for channel, final_state in all_finalstates.items():
				if state in final_state:
					channels.append(channel)
	else:
		for channel in args.channels:
			for state in all_finalstates[channel]:
				channels.append(channel)
				final_states.append(state)

	for index in range(len(channels) - len(background_methods)):
		background_methods.append(background_methods[index])

	# Category and Cut type assignment for respective studies
	global_category_string = "catHtt13TeV"
	global_cut_type = "baseline"
	if args.cp:
		global_cut_type = "cp"
	if args.era == "2016":
		if args.smhtt:
			global_cut_type = "smhtt"
		if args.cpggh:
			global_cut_type = "cpggh"
		global_cut_type += "2016"
	elif args.era == "2017" or args.era == "2018":
		if args.smhtt:
			global_cut_type = "smhtt"
		if args.cpggh:
			global_cut_type = "cpggh"
		if args.cptautau:
			global_category_string = "catcptautau2017"
			global_cut_type = "cptautau"
		global_cut_type += "2017"
	if args.legacy == True:
		global_cut_type += "legacy"

	quantities = []
	# x_labels = []
	for index, quantity in enumerate(args.quantities):
		if "-" in quantity and "LV" in quantity:
			for var in ["P", "Px", "Py", "Pz", "Pt", "Eta", "Phi"]:
				new_quantity = "-".join("".join([q,".",var,"()"]) for q in quantity.split("-"))
				quantities.append(new_quantity)
				# new_x_label =
			for var in ["P", "Pt"]:
				new_quantity = "/".join(["("+"-".join("".join([q,".",var,"()"]) for q in quantity.split("-"))+")", "".join([quantity.split("-")[-1],".",var,"()"])])
				quantities.append(new_quantity)
		elif ":" in quantity and "LV" in quantity:
			for var in ["P", "Px", "Py", "Pz", "Pt", "Eta", "Phi"]:
				new_quantity = ":".join("".join([q,".",var,"()"]) for q in quantity.split(":"))
				quantities.append(new_quantity)
		else:
			quantities.append(quantity)
	print(quantities)

	if args.channel_comparison:
		args.weights = (args.weights * len(channels))[:len(channels)]
	else:
		args.weights = (args.weights * len(quantities))[:len(quantities)]

	# Configs construction for HP
	for category in args.categories:
		for index_quantity, quantity in enumerate(quantities):

			channels_final_states_background_methods = zip(channels, final_states, background_methods)
			print "channels", channels
			print "final_states", final_states
			print "background_methods", background_methods
			print "channels_final_states_background_methods ", channels_final_states_background_methods
			channel_config = {}
			for index_channel, (channel, final_state, background_method) in enumerate(channels_final_states_background_methods):

				last_loop = index_channel == len(channels_final_states_background_methods) - 1

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
				weight = args.weights[index_channel if args.channel_comparison else index_quantity]

				config = sample_settings.get_config(
						samples = list_of_samples,
						channel = channel,
						category = category_string,
						higgs_masses = args.higgs_masses,
						normalise_signal_to_one_pb = False,
						ztt_from_mc = args.ztt_from_mc,
						weight = "((%s)*(%s))" % (json_config.pop("weights", ["1.0"])[0], weight),
						lumi  =  args.lumi * 1000,
						exclude_cuts = args.exclude_cuts + json_config.pop("exclude_cuts", []),
						blind_expression = channel + "_" + quantity,
						fakefactor_method = args.fakefactor_method,
						fake_factor_name_1 = "ffWeight_medium_mvadmbins_1",
						fake_factor_name_2 = "ffWeight_medium_mvadmbins_2",
						stack_signal = args.stack_signal,
						scale_signal = args.scale_signal,
						project_to_lumi = args.project_to_lumi,
						cut_mc_only = args.cut_mc_only,
						scale_mc_only = args.scale_mc_only,
						estimationMethod = background_method,
						controlregions = args.controlregions,
						cut_type = global_cut_type,
						no_ewk_samples = args.no_ewk_samples,
						no_ewkz_as_dy = args.no_ewkz_as_dy,
						inclusive_diboson_samples=args.inclusive_diboson_samples,
						nick_suffix = (channel+str(index_channel) if args.channel_comparison else ""),
						asimov_nicks = asimov_nicks,
						cpfinalstate = args.cptautau,
						proxy_fakefactors = args.use_proxy_fakefactors
				)
				if (args.channel_comparison):
					channel_config = samples.Samples.merge_configs(channel_config, config)
					if last_loop:
						config = channel_config

				x_expression = json_config.pop("x_expressions", [quantity])
				if ":" in quantity:
					x_expression = quantity.split(":")[0]
					config["y_expressions"] = [quantity.split(":")[1] for nick in config["nicks"]]
					# print config["y_expressions"]
					# print quantity.split(":")
					print "x_expression: ", x_expression
				config["x_expressions"] = [x_expression for nick in config["nicks"]]
				config["category"] = category

				binning_string = "binningHtt13TeV"

				binnings_key = "{binning_string}{channel}{category}_{quantity}".format(
						binning_string = binning_string + "_" if binning_string else "",
						channel = channel,
						category = "_" + category if category else "",
						quantity = quantity
				)
				print binnings_key, quantity
				# print binnings_settings.binnings_dict
				config["x_label"] = json_config.pop("x_label", channel + "_" + quantity)
				if ":" in binnings_key:
					binnings_key = channel + "_" + quantity.split(":")[0]
					y_bins = json_config.pop("y_bins", [channel + "_" + quantity.split(":")[1]])
					config["y_bins"] = [y_bins for nick in config["nicks"]]
					config["x_label"] = quantity.split(":")[0]
				# elif "-" in binnings_key: TODO fix labels. regex gen/simplefit/prefit --> replace --> add quantity after
					# config["x_label"] = re.sub(quantity.split(":")[0])
				else:
					if binnings_key not in binnings_settings.binnings_dict and channel + "_" + quantity in binnings_settings.binnings_dict and "--x-bins" not in args.args:
						binnings_key = channel + "_" + quantity
				if binnings_key not in binnings_settings.binnings_dict:
					if "LV" in binnings_key and not ("Phi" in binnings_key or "Eta" in binnings_key):
						if "/" in binnings_key:
							binnings_key = "50,-1,1"
						elif "-" in binnings_key:
							if "Tau2" in binnings_key:
								binnings_key = "50,-50,50"
							else:
								binnings_key = "50,-100,100"
					elif "LV" in binnings_key and "Phi" in binnings_key:
						# binnings_key = "32,-3.14159,3.141591"
						if "Tau2" in binnings_key:
							binnings_key = "32,-0.05,0.05"
						else:
							binnings_key = "32,-0.2,0.2"
					elif "LV" in binnings_key and "Eta" in binnings_key:
						if "Tau2" in binnings_key:
							binnings_key = "50,-0.1,0.1"
						else:
							binnings_key = "50,-3,3"
					else:
						binnings_key = None
				if binnings_key is not None and "--x-bins" not in args.args:
					x_bins = json_config.pop("x_bins", [binnings_key])
					config["x_bins"] = [x_bins for nick in config["nicks"]]
				elif "--x-bins" in args.args:
					x_binning = re.search("(--x-bins)[\s=\"\']*(?P<x_bins>\S*)[\"\']?\S", args.args)
					config["x_bins"] = [" ".join(x_binning.group(2))]

				if args.channel_comparison:
					config["labels"] = ["channel_" + channel for channel in channels]
					config["title"] = ", ".join(args.samples)
				elif args.cptautau:
					config["title"] = "_".join(["channel_cptautau", channel, final_state])
				else:
					config["title"] = "channel_" + channel

				config["directories"] = [args.input_dir]

				if args.channel_comparison:
					if "stacks" in config: config.pop("stacks")
					if "colors" in config: config.pop("colors")
					config["markers"] = ["LINE"]
					config["legend_markers"] = ["L"]
					config["line_widths"] = [3]

				if args.shapes:
					if "stacks" in config: config.pop("stacks")
					if "NormalizeToUnity" not in config.get("analysis_modules", []):
						config.setdefault("analysis_modules", []).append("NormalizeToUnity")
					config["y_label"] = "arb. u."
					config["markers"] = ["LINE"]
					config["legend_markers"] = ["L"]
					config["line_widths"] = [3]

				if args.add_analysis_modules_before_ratio:
					for analysis_module in args.analysis_modules:
						if analysis_module not in config.get("analysis_modules", []):
							config.setdefault("analysis_modules", []).append(analysis_module)

				if args.nicks_blacklist:
					bkg_samples_used = [nick for nick in bkg_samples if (nick in config["nicks"] or nick == "ff")]
					config["nicks_blacklist"].extend([" ".join(bkg_samples_used).split()])
					config["nicks_blacklist"].append("data")

				if args.ratio:
					bkg_samples_used = [nick for nick in bkg_samples if (nick in config["nicks"] or nick == "ff")]
					if "Ratio" not in config.get("analysis_modules", []):
						config.setdefault("analysis_modules", []).append("Ratio")
					config.setdefault("ratio_numerator_nicks", []).extend([" ".join(bkg_samples_used), "data"])
					config.setdefault("ratio_denominator_nicks", []).extend([" ".join(bkg_samples_used)] * 2)
					config.setdefault("ratio_result_nicks", []).extend(["ratio_MC", "ratio_Data"])
					config.setdefault("colors", []).extend(["#000000"] * 2)
					config.setdefault("markers", []).extend(["E2", "E"])
					config.setdefault("legend_markers", []).extend(["ELP"] * 2)
					config.setdefault("labels", []).extend([""] * 2)
					config.setdefault("stacks", []).extend(["unc", "ratio"])

				if not args.add_analysis_modules_before_ratio:
					for analysis_module in args.analysis_modules:
						if analysis_module not in config.get("analysis_modules", []):
							config.setdefault("analysis_modules", []).append(analysis_module)

				if log.isEnabledFor(logging.DEBUG) and "PrintInfos" not in config.get("analysis_modules", []):
					config.setdefault("analysis_modules", []).append("PrintInfos")

				if "--y-log" not in args.args:
					config["y_lims"] = [0.0]
				if args.cms:
					config["cms"] = True
					config["extra_text"] = "Private work"
					config["legend"] = [0.58, 0.25, 0.9, 0.83] if args.ratio or args.ratio_subplot else [0.63, 0.63, 0.9, 0.9]
				elif args.shapes:
					config["legend"] = [0.55, 0.65, 0.9, 0.88]
				else:
					config["y_rel_lims"] = [0.5, 10.0] if "--y-log" in args.args else [0.0, 1.5 if args.ratio else 1.4]
					config["legend"] = [0.23, 0.63, 0.9, 0.83] if args.ratio or args.ratio_subplot else [0.23, 0.73, 0.9, 0.89]
					config["legend_cols"] = 3
				if not args.shapes:
					if args.lumi is not None:
						config["lumis"] = [float("%.1f" % args.lumi)]
					config["energies"] = [13]
					config["year"] = args.era

				config["output_dir"] = os.path.expandvars(os.path.join(
						args.output_dir,
						channel if not args.channel_comparison else "",
						"" if category is None else category
				))
				if args.ratio_subplot:
					samples_used = [nick for nick in bkg_samples if (nick in config["nicks"] or nick == "ff")]
					if "Ratio" not in config.get("analysis_modules", []):
						config.setdefault("analysis_modules", []).append("Ratio")
					config.setdefault("ratio_numerator_nicks", []).extend([str(bkg) for bkg in samples_used] + [" ".join(samples_used), "data"])
					config.setdefault("ratio_denominator_nicks", []).extend([" ".join(samples_used)] * len(samples_used) + [" ".join(samples_used)]*2 )
					# config.setdefault("ratio_denominator_nicks", []).extend(["data"]*len(samples_used) + [" ".join(samples_used)] )
					config.setdefault("ratio_result_nicks", []).extend([str(bkg)+"_subplot" for bkg in samples_used] + ["mc_unc_subplot", "data_subplot"])
					config.setdefault("markers", []).extend(["HIST"]*len(samples_used) + ["E2", "E"])
					config.setdefault("colors", []).extend([str(bkg) for bkg in samples_used] + ["#000000"]*2)
					config.setdefault("legend_markers", []).extend(["ELP"]*len(samples_used) + ["ELP"]*2)
					config.setdefault("labels", []).extend([""]*len(samples_used) + [""]*2)
					config.setdefault("stacks", []).extend(["ratio_subplot"]*len(samples_used) + ["mc_unc_subplot", "ratio_data_subplot"])
					config.setdefault("subplot_nicks", []).extend([str(bkg)+"_subplot" for bkg in samples_used] + ["mc_unc_subplot", "data_subplot"])
					config["y_subplot_lims"] = [0.0, 1.3]
					# config["y_subplot_label"] = "a.u."

				if not args.www is None:
					config["www"] = os.path.join(
							args.www,
							channel if not args.channel_comparison else "",
							"" if final_state is None else final_state,
							"" if category is None else category,
							"phistarcp" if "PhiStarCPPolVec" in quantity else "simplefit"
					)

				# final_state_string_1 = ""
				# final_state_string_2 = ""
				final_state_strings = []
				if final_state in ["a1e", "a1mu"]:
					final_state_strings.append("(decayModeMVA_2 == 10)")
				elif final_state in ["a1pi"]:
					final_state_strings.append("(decayModeMVA_2 == 10)*(decayModeMVA_1 == 0)")
					final_state_strings.append("(decayModeMVA_2 == 0)*(decayModeMVA_1 == 10)")
				elif final_state in ["a1rho"]:
					final_state_strings.append("(decayModeMVA_2 == 10)*(decayModeMVA_1 == 1)")
					final_state_strings.append("(decayModeMVA_2 == 1)*(decayModeMVA_1 == 10)")
				elif final_state in ["a1a1"]:
					final_state_strings.append("(decayModeMVA_2 == 10)*(decayModeMVA_1 == 10)")

				if final_state in ["a1pi", "a1rho"] and "2" in config["x_expressions"][0][0]:
					config["x_expressions"].append([config["x_expressions"][0][0].replace("2", "1")])
				elif final_state in ["a1pi", "a1rho"] and "1" in config["x_expressions"][0][0]:
					config["x_expressions"].append([config["x_expressions"][0][0].replace("1", "2")])

				if "PhiStarCPPolVec" in quantity: # TODO append (Fitconverged==1) when phiStarCP variable
					config.setdefault("weights", [1.0]).append("simpleFitConverged>0")

				new_weights = []
				for  weight_index, weight in enumerate(config.setdefault("weights", [1.0])):
					for fs_index, fs_string in enumerate(final_state_strings):
						new_weights.append("((%s)*(%s))" % (weight, fs_string))

				config["stacks"] = config["stacks"]*len(final_state_strings)
				# print config["weights"]
				# print new_weights
				# print config["stacks"]
				config["weights"] = new_weights
				# weight = "((%s)*(%s))" % (final_state_string, weight)
				# print weight

				print "config[\"weights\"]", config["weights"]
				print "config[\"x_expressions\"]", config["x_expressions"]

				config.update(json_config)

				if (not args.channel_comparison) or last_loop:
					plot_configs.append(config)

	if log.isEnabledFor(logging.DEBUG):
		import pprint
		pprint.pprint(plot_configs)
	higgsplot.HiggsPlotter(
			list_of_config_dicts=plot_configs, list_of_args_strings=[args.args],
			n_processes=args.n_processes, n_plots=args.n_plots, batch=args.batch
	)
