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

import ROOT
import Artus.Utility.jsonTools as jsonTools
import Artus.Utility.tools as tools
import Artus.HarryPlotter.utility.roottools as roottools
import Artus.HarryPlotter.plotbase as plotbase
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.expressions as expressions
import HiggsAnalysis.KITHiggsToTauTau.plotting.higgsplot as higgsplot
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.binnings as binnings
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.samples_run2_2015 as samples

if __name__ == "__main__":

	parser = argparse.ArgumentParser(description="Make Data-MC control plots.",
	                                 parents=[logger.loggingParser])

	parser.add_argument("-i", "--input-dir", required=True,
	                    help="Input directory.")
	parser.add_argument("-s", "--samples", nargs="+",
	                    # default=["ztt", "zll", "ttj", "vv", "wj", "qcd", "data"],
						default = ["wj", "zl", "zj", "ttt", "ttjj", "ttl", "vvt", "vvj", "vvl", "ztt_emb", "data"],
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
	parser.add_argument("-ff", "--fakefactor-method", default=False, action="store_true",
			help="Optional background estimation using the Fake-Factor method. [Default: %(default)s]")
	parser.add_argument("--scale-mc-only", default="1.0",
                        help="scales only MC events. [Default: %(default)s]")
	parser.add_argument("--cut-mc-only", default="1.0",
                        help="cut applied only on MC. [Default: %(default)s]")
	parser.add_argument("--project-to-lumi", default=1.0,
                        help="multiplies current lumi. 2 would mean double lumi you have right now [Default: %(default)s]")
	parser.add_argument("-c", "--channels", nargs="*",
	                    default=["et" , "mt" , "tt1" , "tt2"],
	                    help="Channels. tt channel has to be run twice, once per tau inverting the isolation of tau 1 in tt1 and tau 2 in tt2. [Default: %(default)s]")
	parser.add_argument("--categories", nargs="+", default=[None],
	                    help="Categories. [Default: %(default)s]")
	parser.add_argument("--category-quantities", nargs="+", default=["njets"],
	                    help="Variables used in categories. [Default: %(default)s]")
	parser.add_argument("-x", "--quantities", nargs="+",
	                    default=["m_vis", "decayMode_2", "pt_2"],
	                    help="Quantities. Up to 3 quantities can be binned in a single histogram. Further quantities have to be incorporated via categories. In the 'tt1' channel the quantity of the other tau will be taken instead (tt1 : pt_2 --> pt_1) [Default: %(default)s]")
	                    # default=["integral",
	                    #          "pt_1", "eta_1", "phi_1", "m_1", "iso_1", "mt_1",
	                    #          "pt_2", "eta_2", "phi_2", "m_2", "iso_2", "mt_2",
	                    #          "pt_sv", "eta_sv", "phi_sv", "m_sv", "m_vis", "ptvis",
	                    #          "met", "metphi", "metcov00", "metcov01", "metcov10", "metcov11",
	                    #          "mvamet", "mvametphi", "mvacov00", "mvacov01", "mvacov10", "mvacov11",
	                    #          "pZetaMissVis", "pzetamiss", "pzetavis",
	                    #          "jpt_1", "jeta_1", "jphi_1",
	                    #          "jpt_2", "jeta_2", "jphi_2",
	                    #          "njetspt30", "mjj", "jdeta", "njetingap20", "njetingap",
	                    #          "trigweight_1", "trigweight_2", "puweight",
	                    #          "npv", "npu", "rho"],
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
	parser.add_argument("--cptautau", default=False, action="store_true",
				help="Produce plots for the Higgs CP tau tau final state analysis. [Default: %(default)s]")
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
	                    default="$CMSSW_BASE/src/plots/FF_fractions/",
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
	parser.add_argument("--use-relaxed-isolation-for-W", default=False, action="store_true",
	                    help="Use relaxed isolation for W+jets shape estimation in MT and ET channels. [Default: %(default)s]")
	parser.add_argument("--use-relaxed-isolation-for-QCD", default=False, action="store_true",
	                    help="Use relaxed isolation for QCD shape estimation in MT and ET channels. [Default: %(default)s]")
	parser.add_argument("--calculate-QCD-os-ss-scalefactor", default=False, action="store_true",
	                    help="Calculate os to ss extrapolation factor of QCD estimation in MT and ET channels. [Default: %(default)s]")
	parser.add_argument("--invertiso", default=False, action="store_true",
	                    help="Invert isolation of taus (tau 1 for channel tt1 and tau 2 for tt2). [Default: %(default)s]")
	parser.add_argument("--qcd-from-sum", default=False, action="store_true",
	                    help="Get QCD estimate from Data - Sum of MC in each bin. [Default: %(default)s]")
	parser.add_argument("--combine-fractions", default=False, action="store_true",
	                    help="Combine MC fractions to the three FF categories. [Default: %(default)s]")
	parser.add_argument("--make-root-files", default=False, action="store_true",
	                    help="Produce root output files instead of plots. [Default: %(default)s]")

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
		elif args.era == "2017" and args.calculate_QCD_os_ss_scalefactor==False:
			import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.samples_run2_2017_mcv2 as samples
			if args.lumi == parser.get_default("lumi"):
				args.lumi = samples.default_lumi/1000.0
		elif args.era == "2017" and args.calculate_QCD_os_ss_scalefactor==True:
			import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.samples_run2_OStoSSExtSF as samples
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
	if args.era == "2016":
		if args.smhtt:
			global_cut_type = "smhtt"
		if args.cpggh:
			global_cut_type = "cpggh"
		global_cut_type += "2016"
	elif args.era == "2017":
		if args.smhtt:
			global_cut_type = "smhtt"
		if args.cpggh:
			global_cut_type = "cpggh"
		if args.cptautau:
			global_cut_type = "cptautau"
		global_cut_type += "2017"
		global_category_string = "catFFfractions13TeV"
		if args.invertiso:
			if args.categories == [None]:
				args.categories = ["inclusive_jet", "0_jet", "1_jet", "2_jet"] # inclusive = no cut on jets, 2_jets = 2 jets or more
	if args.channel_comparison:
		args.weights = (args.weights * len(args.channels))[:len(args.channels)]
	else:
		args.weights = (args.weights * len(args.quantities))[:len(args.quantities)]

	cut_type = global_cut_type
	FFfractions_names = [] # NOTE: set during creation of ratios
	quantities = []

	# Configs construction for HP
	for category in args.categories:

		channel_config = {}
		channels_background_methods = zip(args.channels, args.background_method)
		for index_channel, (channel, background_method) in enumerate(channels_background_methods):

			ff_channel = channel
			if args.invertiso:
				quantities = copy.deepcopy(args.quantities)
				print(channel, quantities)
				for index, quantity in enumerate(quantities):
					quantities[index] = quantity.replace("_2","_1") if channel == "tt1" else quantity

				if channel == "tt1":
					cut_type = global_cut_type + "invertedTauIsolationFF_1"
				else:
					cut_type = global_cut_type + "invertedTauIsolationFF_2"

				if channel == "tt1" or channel == "tt2":
					channel = "tt"

				cut_type += "_" + category

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

			last_loop = index_channel == len(channels_background_methods) - 1

			category_string = None
			if category != None:
				category_string = (global_category_string + "_{channel}_{category}").format(channel = channel, category = category)
			# print category_string

			# json_config = {}
			# json_filenames = [os.path.join(args.json_dir, "8TeV" if args.run1 else "13TeV", channel_dir, quantity + ".json") for channel_dir in [channel, "default"]]
			# 
			# for json_filename in json_filenames:
			# 	json_filename = os.path.expandvars(json_filename)
			# 	if os.path.exists(json_filename):
			# 		json_config = jsonTools.JsonDict(json_filename).doIncludes().doComments()
			# 		break
			# 
			# quantity = json_config.pop(axis + "_expressions", [quantity])[0]
			# weight = args.weights[index_channel if args.channel_comparison else index_quantity]

			config = sample_settings.get_config(
					samples = list_of_samples,
					channel = channel,
					category = category_string,
					higgs_masses = args.higgs_masses,
					normalise_signal_to_one_pb = False,
					ztt_from_mc = args.ztt_from_mc,
					weight = "(1.0)", # "((%s)*(%s))" % (json_config.pop("weights", ["1.0"])[0], weight),
					lumi  =  args.lumi * 1000,
					exclude_cuts = args.exclude_cuts, # + json_config.pop("exclude_cuts", []),
					blind_expression = channel, # + "_" + quantity,
					fakefactor_method = args.fakefactor_method,
					stack_signal = args.stack_signal,
					scale_signal = args.scale_signal,
					project_to_lumi = args.project_to_lumi,
					cut_mc_only = args.cut_mc_only,
					scale_mc_only = args.scale_mc_only,
					estimationMethod = background_method,
					mssm = args.mssm,
					controlregions = args.controlregions,
					cut_type = cut_type,
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

			print(channel, quantities)
			for index_quantity, [quantity, axis] in enumerate(zip(quantities, ["x", "y", "z"])):

				json_config = {}
				json_filenames = [os.path.join(args.json_dir, "8TeV" if args.run1 else "13TeV", channel_dir, quantity + ".json") for channel_dir in [channel, "default"]]
				
				for json_filename in json_filenames:
					json_filename = os.path.expandvars(json_filename)
					if os.path.exists(json_filename):
						json_config = jsonTools.JsonDict(json_filename).doIncludes().doComments()
						break
				
				quantity = json_config.pop(axis + "_expressions", [quantity])[0]
				axis_expression = json_config.pop(axis + "_expressions", [quantity])
				config[axis + "_expressions"] = [("0" if (("gen_zttpospol" in nick) or ("gen_zttnegpol" in nick)) else axis_expression) for nick in config["nicks"]]
				config["category"] = category
				# print(axis + "_expressions", config[axis + "_expressions"])

				binning_string = "binningHtt13TeV"
				if args.mssm:
					binning_string = "binningHttMSSM13TeV"
				elif args.mva:
					binning_string = "binningMVAStudies"
				elif args.polarisation:
					binning_string = "binningZttPol13TeV"
				elif args.invertiso:
					binning_string = "binningFFfractions13TeV"

				binnings_key = "{binning_string}{channel}{category}_{quantity}".format(
						binning_string = binning_string + "_" if binning_string else "",
						channel = channel,
						category = "_" + category if (category and not args.invertiso) else "",
						quantity = quantity
				)
				# print binnings_key
				if binnings_key not in binnings_settings.binnings_dict and channel + "_" + quantity in binnings_settings.binnings_dict and ("--" + axis + "-bins") not in args.args:
					binnings_key = channel + "_" + quantity
				if binnings_key not in binnings_settings.binnings_dict:
					binnings_key = None
				if binnings_key is not None and ("--" + axis + "-bins") not in args.args:
					x_bins = json_config.pop(axis + "_bins", [binnings_key])
					config[axis + "_bins"] = [("1,-1,1" if (("gen_zttpospol" in nick) or ("gen_zttnegpol" in nick)) else x_bins) for nick in config["nicks"]]
				elif ("--" + axis + "-bins") in args.args:
					x_binning = re.search("(--" + axis + "-bins)[\s=\"\']*(?P<" + axis + " _bins>\S*)[\"\']?\S", args.args)
					config[axis + "_bins"] = [" ".join(x_binning.group(2))]

				config[axis + "_label"] = json_config.pop(axis + "_label", channel + "_" + quantity)
				# print(axis + "_label", config[axis + "_label"])

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

			samples_used = []
			samples_used_noplot = []
			nps = "noplot_" if args.make_root_files else ""
			cat_suffix = "_" + category if args.make_root_files else ""

			if args.make_root_files:
				for index, nick in enumerate(config["nicks"]):
					config["nicks"][index] = nps + nick
					# del config["markers"][:len(config["markers"])-4]
					# del config["stacks"][:len(config["stacks"])-4]
					# del config["colors"][:len(config["colors"])-4]
					# del config["labels"][:len(config["labels"])-4]

			if args.qcd_from_sum:
				if "AddHistograms" not in config.get("analysis_modules", []):
					config.setdefault("analysis_modules", []).append("AddHistograms")
				config.setdefault("add_nicks", []).extend([" ".join(nps + sample for sample in args.samples)])
				config.setdefault("add_scale_factors", []).extend(["".join("-1.0 "*(len(args.samples)-1)) + "1.0"])
				config.setdefault("add_result_nicks", []).extend([nps + "qcd"])
				config.setdefault("markers", []).insert(config["nicks"].index(config["add_nicks"][0].split()[0]), ["HIST"])
				config.setdefault("colors", []).insert(config["nicks"].index(config["add_nicks"][0].split()[0]), ["qcd"])
				config.setdefault("labels", []).insert(config["nicks"].index(config["add_nicks"][0].split()[0]), ["qcd"])
				config.setdefault("legend_markers", []).insert(config["nicks"].index(config["add_nicks"][0].split()[0]), ["F"])
				config.setdefault("stacks", []).insert(config["nicks"].index(config["add_nicks"][0].split()[0]), ["bkg"])
				config.setdefault("nicks_correct_negative_bins", []).extend([nps + "qcd"])

			if args.ratio_subplot:
				if channel == "tt":
					if "invertedTauIsolationFF_1" in cut_type:
						channel = "tt1"
					else:
						channel = "tt2"
				# if not args.make_root_files:
				# 	if channel == "tt":
				# 		if "invertedTauIsolationFF_1" in cut_type:
				# 			channel = "tt1"
				# 		else:
				# 			channel = "tt2"
				samples_used = [nick for nick in bkg_samples if nick in config["nicks"]] + ["qcd"]
				samples_used_noplot = [nps + nick for nick in bkg_samples if nick in config["nicks"]] + [nps + "qcd"]
				if "Ratio" not in config.get("analysis_modules", []):
					config.setdefault("analysis_modules", []).append("Ratio")

				if args.combine_fractions:
					FFfractions = ["noplot_qcd", "noplot_wj noplot_zj noplot_vvj", "noplot_ttjj", "noplot_ttt noplot_vvt noplot_ztt_emb noplot_zl noplot_ttl noplot_vvl"] if args.make_root_files else ["qcd", "wj zj vvj", "ttjj", "ttt vvt ztt_emb zl ttl vvl"]
					FFfractions_names = ["qcd", "w", "ttbar", "real_taus"]
					FFfractions_colors = ["qcd", "wj", "ttj", "ztt"]
					FFfractions_labels = ["ff_qcd_frac", "ff_w_frac", "ff_ttbar_frac", "ff_real_tau_frac"]
					config.setdefault("ratio_numerator_nicks", []).extend(FFfractions)
					config.setdefault("ratio_denominator_nicks", []).extend([nps + "data"]*len(FFfractions))
					config.setdefault("ratio_result_nicks", []).extend([str(frac)+"_fracs_"+ ff_channel + cat_suffix for frac in FFfractions_names])
					config.setdefault("markers", []).extend(["HIST"]*len(FFfractions))
					config.setdefault("colors", []).extend(FFfractions_colors)
					config.setdefault("labels", []).extend(FFfractions_labels)
					config.setdefault("legend_markers", []).extend(["F"]*len(FFfractions))
					config.setdefault("stacks", []).extend(["ratio_subplot"]*len(FFfractions))
					config.setdefault("subplot_nicks", []).extend([str(frac)+"_fracs_"+ ff_channel for frac in FFfractions_names])
				else:
					config.setdefault("ratio_numerator_nicks", []).extend([str(bkg) for bkg in samples_used_noplot])
					config.setdefault("ratio_denominator_nicks", []).extend([nps + "data"]*len(samples_used))
					config.setdefault("ratio_result_nicks", []).extend([str(bkg)+"_fracs_"+ ff_channel + cat_suffix for bkg in samples_used])
					config.setdefault("markers", []).extend(["HIST"]*len(samples_used))
					config.setdefault("colors", []).extend([str(bkg) for bkg in samples_used])
					config.setdefault("labels", []).extend([str(bkg)+"_fracs_"+ ff_channel + cat_suffix for bkg in samples_used])
					config.setdefault("legend_markers", []).extend([""]*len(samples_used))
					config.setdefault("stacks", []).extend(["ratio_subplot"]*len(samples_used))
					config.setdefault("subplot_nicks", []).extend([str(bkg)+"_fracs_"+ ff_channel + cat_suffix for bkg in samples_used])

				config["y_subplot_lims"] = [-0.3, 1.7]
				config["y_subplot_label"] = "fracs"

			if args.ratio_subplot and args.qcd_from_sum:
				fracs_used = ["qcd", "w", "ttbar", "real_taus"] if args.combine_fractions else samples_used
				config.setdefault("nicks_correct_negative_bins", []).extend([str(bkg)+"_fracs_"+ ff_channel + cat_suffix for bkg in samples_used])
				# config["nicks_whitelist"] = ["^"+str(bkg)+"$" for bkg in samples_used] + ["^data$"]+ ["^"+str(bkg)+"_fracs_"+channel+"$" for bkg in fracs_used]
				config["no_integral_preservation"] = True
				config["analysis_modules"] = ["BinErrorsOfEmptyBins", "AddHistograms", "Ratio", "CorrectNegativeBinContents"]
				# config["analysis_modules"] = ["BinErrorsOfEmptyBins", "Ratio", "AddHistograms", "CorrectNegativeBinContents"]

				# for index, nick in enumerate(config["nicks"]):
				# 	print nick
				# 	config.setdefault("line_widths", []).extend([2] if nick=="data" else [1])	

			config["output_dir"] = os.path.expandvars(os.path.join(
					args.output_dir,
					channel if not args.channel_comparison else "",
					"" if category is None else category
			))

			if not args.www is None and not args.make_root_files:
				config["www"] = os.path.join(
						args.www,
						channel if not args.channel_comparison else "",
						"" if category is None else category
				)

			if args.make_root_files:
				config["plot_modules"] = ["ExportRoot"]
				config["nicks_instead_labels"] = True
				config["file_mode"] = "RECREATE"

			config.update(json_config)

			# if (not args.channel_comparison) or last_loop:
			# 	plot_configs.append(config)
			# print("last loop over quantities - appending plot config")
			plot_configs.append(config)

	if log.isEnabledFor(logging.DEBUG):
		import pprint
		pprint.pprint(plot_configs)
	plot_results = higgsplot.HiggsPlotter(
			list_of_config_dicts=plot_configs, list_of_args_strings=[args.args],
			n_processes=args.n_processes, n_plots=args.n_plots, batch=args.batch
	)

	# print(plot_results.output_filenames)
	if args.make_root_files:
		output_root_filename = os.path.expandvars(os.path.join(args.output_dir,"FF_fractions.root"))
		tools.hadd(output_root_filename, tools.flattenList(plot_results.output_filenames), hadd_args="-f")
		w = ROOT.RooWorkspace("w", "w") # create an empty RooWorkSpace with name "w" and title "w"
		import_function = getattr(w, 'import')
		
		rootfile = ROOT.TFile.Open(output_root_filename, "read")
		histos = []
		realvars = []
		datahists = []
		histfuncs = []
		formularvars = []
		rootfile.cd()

		expressions_dict = expressions.ExpressionsDict().expressions_dict
		category_quantities = args.category_quantities

		first_histo = rootfile.GetListOfKeys().At(0).ReadObj()

		plot_quantity_limits = [roottools.RootTools.get_binning(first_histo, i) for i in range(first_histo.GetDimension()) ]
		plot_quantity_limits = [[plot_quantity_limits[i][0],plot_quantity_limits[i][-1]] for i in range(len(plot_quantity_limits))]

		for index, quantity in enumerate(quantities):
			quantity = quantity.replace("_2","").replace("_1","")
			quantities[index] = quantity
			import_function(ROOT.RooRealVar(quantity, quantity, plot_quantity_limits[index][0], -float('Inf'), float('Inf')))
			import_function(ROOT.RooFormulaVar(quantity + "_range", "".join(["TMath::Range(",str(plot_quantity_limits[index][0]),",",str(plot_quantity_limits[index][1]),",@0)"]), ROOT.RooArgList(w.var(quantity))))

		for index, quantity in enumerate(category_quantities):
			import_function(ROOT.RooRealVar(quantity, quantity, 0., -float('Inf'), float('Inf')))
			# import_function(ROOT.RooFormulaVar(quantity + "_range", "TMath::Range(" + args.category_quantities_bin_ranges[index].split()[0] + "," + args.category_quantities_bin_ranges[index].split()[1] + ",@0)", ROOT.RooArgList(w.var(quantity))))

		elements = roottools.RootTools.walk_root_directory(rootfile)
		for index, (key, path) in enumerate(elements):
			histos.append(key.ReadObj())
			histos[index].SetName(key.GetName())
			realvars.append([])
			formularvars.append([])
			for index_q, quantity in enumerate(quantities):
				realvars[index].append(ROOT.RooRealVar(key.GetName() + "_" +  quantity + "_var", key.GetName() + "_" +  quantity + "_var_title", plot_quantity_limits[index_q][0], plot_quantity_limits[index_q][1]))
				formularvars[index].append(ROOT.RooFormulaVar(key.GetName() + "_" +  quantity + "_range", "TMath::Range(" + str(plot_quantity_limits[index_q][0]) + "," + str(plot_quantity_limits[index_q][1]) + ",@0)", ROOT.RooArgList(w.function(quantity))))
			datahists.append(ROOT.RooDataHist(key.GetName() + "_dh", key.GetName() + "_dh_title", ROOT.RooArgList(*realvars[index]), ROOT.RooFit.Import(histos[index])))
			histfuncs.append(ROOT.RooHistFunc(key.GetName() + "_hf", key.GetName() + "_hf_title", ROOT.RooArgList(*formularvars[index]), ROOT.RooArgList(*realvars[index]), datahists[index]))

			if "inclusive" not in key.GetName():
				import_function(histos[index])
				import_function(histfuncs[index])

		for channel in args.channels:
			for process in FFfractions_names:
				rootformular_string = ""
				rooarglist = [w.var(i) for i in category_quantities]
				for category in args.categories:
					if "inclusive" not  in category:
						rooarglist_string = "_".join([process,"fracs",channel,category,"hf"])
						rooarglist.append(w.function(rooarglist_string))
						c_tmp = channel if "tt" not in channel else "tt"
						category_string = expressions_dict["_".join([global_category_string,c_tmp,category])]
						rootformular_string += category_string + "*" + rooarglist_string + "+"
				import_function(ROOT.RooFormulaVar("_".join([process,"fracs",channel]), rootformular_string[:-1], ROOT.RooArgList(*rooarglist)))

		w.Print()
		output_workspace_filename = os.path.expandvars(os.path.join(args.output_dir,
		"FF_fractions_workspace_" + "_".join(quantity.replace("_2","").replace("_1","") for quantity in (args.quantities+args.category_quantities)) + ".root"))
		w.writeToFile(output_workspace_filename) # save workspace
		if os.path.isfile(output_root_filename):
			print("Created Root file " + output_root_filename)
		if os.path.isfile(output_workspace_filename):
			print("Created Rooworkspace " + output_workspace_filename)
		import_function = None # crashes otherwise
		w = None # crashes otherwise
		rootfile.Close()
