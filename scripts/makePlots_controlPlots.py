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

def add_s_over_sqrtb_subplot(config, args, bkg_samples, show_subplot, higgs_nick):
	if not "scale_nicks" in config.keys():
		config["scale_nicks"] = []
		config["scales"] = []
		config["scale_result_nicks"] = []
	config["analysis_modules"].append("ScaleHistograms")
	config["scale_nicks"].append(higgs_nick)
	config["scales"].append(1.0 / args.scale_signal)
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

	if show_subplot:
		config["y_subplot_label"] = ""
		config["subplot_lines"] = [0.1, 0.5, 1.0 ]
		config["y_subplot_lims"] = [0, 1.5]
		config["subplot_nicks"]=["blinding"]
		for method in args.blinding_methods:
			config["markers"].append("LINE")
			config["legend_markers"].append("L")
			if method == "soversqrtb":
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
	config["sob_integral_direction"] = []
	for i,direction in enumerate(args.integration_directions):
		config["sob_integral_direction"].append(direction)
		config["sob_integral_method"].append(args.integration_methods)
		config["sob_integral_result_nicks"].append("integration_%i"%i + direction)
		config["sob_integral_background_nicks"].append(" ".join(bkg_samples))
		config["sob_integral_signal_nicks"].append(" ".join(signal_samples))
		#config["sob_integral_outputs"].append(args.integration_output)
	if show_subplot:
		config["y_subplot_label"] = "int.(S)/#sqrt{int.(B)+int(S)}"
		config["y_subplot_lims"] = None
		config["subplot_nicks"] = ["integration"]
		for direction in args.integration_directions:
			config["markers"].append("LINE")
			config["legend_markers"].append("L")
			config["labels"].append("#int{S}/#sqrt{#int{B}}")
			if direction == "righttoleft":
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
	                    help="Samples. [Default: %(default)s]")
	parser.add_argument("--use-asimov-dataset", default=None, const="", nargs="?",
						help="Use expectation as observation instead of real data. Specify the nickts of samples (separated by whitespaces) to be used as expectation. [Default: all samples plotted appart from data]")
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
	parser.add_argument("-x", "--quantities", nargs="+",
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
	parser.add_argument("--embedding-selection", default=False, action="store_true",
	                    help="Use samples to consider selection for embedding. [Default: %(default)s]")
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
	parser.add_argument("--new-tau-id", default=False, action="store_true",
	                    help="Use rerun tau Id instead of nominal one. [Default: %(default)s]")
	parser.add_argument("--use-relaxed-isolation-for-W", default=False, action="store_true",
	                    help="Use relaxed isolation for W+jets shape estimation in MT and ET channels. [Default: %(default)s]")
	parser.add_argument("--use-relaxed-isolation-for-QCD", default=False, action="store_true",
	                    help="Use relaxed isolation for QCD shape estimation in MT and ET channels. [Default: %(default)s]")
	args = parser.parse_args()
	logger.initLogger(args)

	if args.run1:
		import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.samples_run1 as samples
	elif args.embedding_selection:
		import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.samples_run2_embedding_selection as samples
	else:
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

	if args.fakefactor_method is not None:
		import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.samples_ff as samples

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
	
	if args.polarisation:
		args.no_ewkz_as_dy = True

	if args.run1 and (args.emb or args.ttbar_retuned):
			log.critical("Embedding --emb and --ttbar-retuned only valid for run2. Remove --emb and --tbar-retuned or select run2 samples.")
			sys.exit(1)
	elif args.run1:
		sample_settings = samples.Samples()
	else:
		sample_settings = samples.Samples(embedding=args.emb,embedding_weight=args.embedded_weights,ttbar_retuned=args.ttbar_retuned)
	if args.mssm:
		bkg_samples = [sample for sample in args.samples if sample not in ["data", "htt", "ggh", "bbh"]]
		sig_samples_raw = [sample for sample in args.samples if sample in ["htt", "ggh", "bbh"]]
	else:
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

	if args.channel_comparison:
		args.weights = (args.weights * len(args.channels))[:len(args.channels)]
	else:
		args.weights = (args.weights * len(args.quantities))[:len(args.quantities)]

	# Configs construction for HP
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
				json_filenames = [os.path.join(args.json_dir, "8TeV" if args.run1 else "13TeV", channel_dir, quantity + ".json") for channel_dir in [channel, "default"]]
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
						stack_signal = args.stack_signal,
						scale_signal = args.scale_signal,
						project_to_lumi = args.project_to_lumi,
						cut_mc_only = args.cut_mc_only,
						scale_mc_only = args.scale_mc_only,
						estimationMethod = background_method,
						mssm = args.mssm,
						controlregions = args.controlregions,
						cut_type = global_cut_type,
						no_ewk_samples = args.no_ewk_samples,
						no_ewkz_as_dy = args.no_ewkz_as_dy,
						useRelaxedIsolationForW = args.use_relaxed_isolation_for_W,
						useRelaxedIsolationForQCD = args.use_relaxed_isolation_for_QCD,
						nick_suffix = (channel+str(index_channel) if args.channel_comparison else ""),
						asimov_nicks = asimov_nicks
				)
				if (args.channel_comparison):
					channel_config = samples.Samples.merge_configs(channel_config, config)
					if last_loop:
						config = channel_config
				
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

				if args.new_tau_id:
					for weight_index, weight in enumerate(config.get("weights", [])):
						config["weights"][weight_index] = weight.replace("byTightIsolationMVArun2v1DBoldDMwLT", "rerunDiscriminationByIsolationMVAOldDMrun2v1Medium").replace("byMediumIsolationMVArun2v1DBoldDMwLT", "rerunDiscriminationByIsolationMVAOldDMrun2v1Loose").replace("byLooseIsolationMVArun2v1DBoldDMwLT", "rerunDiscriminationByIsolationMVAOldDMrun2v1VLoose")

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

				config["x_bins"] = "0 50 80 110 150 200 250 300 1000"
					
				config["x_label"] = json_config.pop("x_label", channel + "_" + quantity)

				if args.channel_comparison:
					config["labels"] = ["channel_" + channel for channel in args.channels]
					config["title"] = ", ".join(args.samples)
				elif args.polarisation:
					config["title"] = "channel_" + channel + ("" if category is None else ("_"+category))
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
						
				if args.ratio:
					bkg_samples_used = [nick for nick in bkg_samples if nick in config["nicks"]]
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
					config["extra_text"] = "Preliminary"
					config["legend"] = [0.7, 0.4, 0.95, 0.83] if args.ratio or args.integrated_sob or args.sbratio or args.ratio_subplot else [0.7, 0.5, 0.9, 0.85]
				elif args.shapes:
					config["legend"] = [0.55, 0.65, 0.9, 0.88]
				else:
					config["y_rel_lims"] = [0.5, 10.0] if "--y-log" in args.args else [0.0, 1.5 if args.ratio or args.integrated_sob or args.sbratio else 1.4]
					config["legend"] = [0.23, 0.63, 0.9, 0.83] if args.ratio or args.integrated_sob or args.sbratio or args.ratio_subplot else [0.23, 0.73, 0.9, 0.89]
					config["legend_cols"] = 3
				if not args.shapes:
					if args.lumi is not None:
						config["lumis"] = [float("%.1f" % args.lumi)]
					config["energies"] = [8] if args.run1 else [13]
					if not args.run1:
						config["year"] = args.era

				#add integrated s/sqrt(b) subplot
				if args.integrated_sob:
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
						config["scale_nicks"] = []
						config["scales"] = []
						config["scale_result_nicks"] = []
					for sample in scale_nicks:
						config["scale_nicks"].append(sample)
						config["scales"].append(1.0 / args.scale_signal)
						config["scale_result_nicks"].append(sample + "_Scaled")
					log.debug(config["scale_nicks"])
					log.debug(scale_nicks)
					log.debug(bkg_samples_used)
					log.debug(sig_samples_used)
					add_s_over_sqrtb_integral_subplot(config, args, bkg_samples_used, args.integrated_sob, sig_samples_used)

				#add FullIntegral
				if args.full_integral:
					bkg_samples_used = [nick for nick in bkg_samples if nick in config["nicks"]]
					bkg_samples_used.append('data')
					if args.emb:
						config["full_integral_outputs"] = './IntegralValues_Embedded.txt'
					config["full_integral_nicks"] = [" ".join(bkg_samples_used)]
					config["analysis_modules"].append("FullIntegral")

				# add s/sqrt(b) subplot
				if args.sbratio or args.blinding_threshold > 0:
					bkg_samples_used = [nick for nick in bkg_samples if nick in config["nicks"]]
					higgs_temp = "htt125"
					if len(args.higgs_masses) > 0 and "125" not in args.higgs_masses:
						higgs_temp = "htt%i"%int(args.higgs_masses[0])
					for sample in sig_samples:
						if higgs_temp in sample:
							higgs_temp = sample
							break
					add_s_over_sqrtb_subplot(config, args, bkg_samples_used, args.sbratio, higgs_temp)

				if args.blinding_threshold > 0:
					if args.blinding_variables[0] == "all" or quantity in args.blinding_variables:
						blind_signal(config, args.blinding_threshold, args.ratio)

				config["output_dir"] = os.path.expandvars(os.path.join(
						args.output_dir,
						channel if not args.channel_comparison else "",
						"" if category is None else category
				))
				if args.ratio_subplot:
					samples_used = [nick for nick in bkg_samples if nick in config["nicks"]]
					if "Ratio" not in config.get("analysis_modules", []):
						config.setdefault("analysis_modules", []).append("Ratio")
					config.setdefault("ratio_numerator_nicks", []).extend([str(bkg) for bkg in samples_used])
					config.setdefault("ratio_denominator_nicks", []).extend([" ".join(samples_used)] *len(samples_used) )
					config.setdefault("ratio_result_nicks", []).extend([str(bkg)+"_subplot" for bkg in samples_used])
					config.setdefault("markers", []).extend(["HIST"]*len(samples_used))
					config.setdefault("legend_markers", []).extend(["ELP"]*len(samples_used))
					config.setdefault("stacks", []).extend(["ratio_subplot"]*len(samples_used))
					config.setdefault("subplot_nicks", []).extend([str(bkg)+"_subplot" for bkg in samples_used])
					config["y_subplot_lims"] = [0.0, 1.0]
					config["y_subplot_label"] = "a.u."			

				if not args.www is None:
					config["www"] = os.path.join(
							args.www,
							channel if not args.channel_comparison else "",
							"" if category is None else category
					)

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
