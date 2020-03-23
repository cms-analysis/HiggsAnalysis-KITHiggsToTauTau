#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import argparse
import copy
import os
import glob
import re
import sys
import pprint
import shlex
import numpy

import CombineHarvester.CombineTools.ch as ch

import Artus.Utility.tools as tools
import Artus.HarryPlotter.utility.plotconfigs as plotconfigs
import Artus.Utility.jsonTools as jsonTools

import HiggsAnalysis.KITHiggsToTauTau.plotting.higgsplot as higgsplot
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.samples_run2_2016 as samples
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.binnings as binnings
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.labels as labels
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.systematics_run2 as systematics
import HiggsAnalysis.KITHiggsToTauTau.datacards.smhttdatacards as smhttdatacards
import HiggsAnalysis.KITHiggsToTauTau.datacards.initialstatecpstudiesdatacards as initialstatecpstudiesdatacards
import HiggsAnalysis.KITHiggsToTauTau.datacards.datacards as datacards_module



def _call_command(command):
	log.debug(command)
	logger.subprocessCall(command, shell=True)

def official2private(category, category_replacements):
	result = copy.deepcopy(category)
	result = category_replacements[category]
	return result

def private2official(category, category_replacements):
	result = copy.deepcopy(category)
	for official, private in category_replacements.iteritems():
		result = re.sub(private+"$", official, result)
	return result

def matching_process(obj1, obj2):
	matches = (obj1.bin() == obj2.bin())
	matches = matches and (obj1.process() == obj2.process())
	matches = matches and (obj1.signal() == obj2.signal())
	matches = matches and (obj1.analysis() == obj2.analysis())
	matches = matches and (obj1.era() == obj2.era())
	matches = matches and (obj1.channel() == obj2.channel())
	matches = matches and (obj1.bin_id() == obj2.bin_id())
	matches = matches and (obj1.mass() == obj2.mass())
	return matches

def is_control_region(obj):
	return ("WJCR" in obj.bin() or "QCDCR" in obj.bin() or "qcd_cr" in obj.bin() or "ttbar" in obj.bin() or obj.channel() == "mm")

def remove_procs_and_systs_with_zero_yield(proc):
	# TODO: find out why zero yield should be ok in control regions. until then remove them
	null_yield = not (proc.rate() > 0. or is_control_region(proc))
	#null_yield = not proc.rate() > 0.
	if null_yield:
		datacards.cb.FilterSysts(lambda systematic: matching_process(proc,systematic))
	return null_yield


if __name__ == "__main__":

	parser = argparse.ArgumentParser(description="Create ROOT inputs and datacards for SM HTT analysis.",
	                                 parents=[logger.loggingParser])

	parser.add_argument("-i", "--input-dir", required=True,
	                    help="Input directory.")
	parser.add_argument("-c", "--channel", action = "append",
	                    default=["all"],
	                    help="Channel. This argument can be set multiple times. [Default: %(default)s]")
	parser.add_argument("--categories", nargs="+", action = "append",
	                    default=[["all"]] * len(parser.get_default("channel")),
	                    help="Categories per channel. This argument needs to be set as often as --channels. [Default: %(default)s]")
	parser.add_argument("-x", "--quantity", default="jdphi",
	                    help="Quantity. [Default: %(default)s]")
	parser.add_argument("-m", "--higgs-masses", nargs="+", default=["125"],
	                    help="Higgs masses. [Default: %(default)s]")
	parser.add_argument("-w", "--weight", default="1.0",
	                    help="Additional weight (cut) expression. [Default: %(default)s]")
	parser.add_argument("-a", "--args", default="",
	                    help="Additional Arguments for HarryPlotter. [Default: %(default)s]")
	parser.add_argument("--no-bbb-uncs", action="store_true", default=False,
	                    help="Do not add bin-by-bin uncertainties. [Default: %(default)s]")
	parser.add_argument("--auto-rebin", action="store_true", default=False,
	                    help="Do auto rebinning [Default: %(default)s]")
	parser.add_argument("--combinations", nargs="+",
	                    default=["individual", "channel", "category", "combined"],
	                    choices=["individual", "channel", "category", "combined"],
	                    help="Combinations to perform. [Default: %(default)s]")
	parser.add_argument("--cp-mixings", nargs="+", type=float,
	                    default=list(numpy.arange(0.0, 1.001, 0.1)),
	                    help="CP mixing angles alpha_tau (in units of pi/2) to be probed. [Default: %(default)s]")
	parser.add_argument("--cp-mixing-scan-points", type=int, default=((len(parser.get_default("cp_mixings"))-1)*4)+1,
	                    help="Number of points for CP mixing angles alpha_tau (in units of pi/2) to be scanned. [Default: %(default)s]")
	parser.add_argument("--cp-study", default="ggh",
	                    choices=["ggh", "vbf", "final"],
	                    help="Choose which CP study to do. [Default: %(default)s]")
	parser.add_argument("--lumi", type=float, default=samples.default_lumi/1000.0,
	                    help="Luminosity for the given data in fb^(-1). [Default: %(default)s]")
	parser.add_argument("--do-not-normalize-by-bin-width", default=False, action="store_true",
	                    help="Turn off normalization by bin width [Default: %(default)s]")
	parser.add_argument("-r", "--ratio", default=False, action="store_true",
	                    help="Add ratio subplot. [Default: %(default)s]")
	parser.add_argument("--background-method", default="simeqn",
	                    help="Background estimation method to be used. [Default: %(default)s]")
	parser.add_argument("-b", "--batch", default=None, const="rwthcondor", nargs="?",
	                    help="Run with grid-control. Optionally select backend. [Default: %(default)s]")
	parser.add_argument("--remote", action="store_true", default=False,
	                    help="Pack result to tarball, necessary for grid-control. [Default: %(default)s]")
	parser.add_argument("--only-config", action="store_true", default=False,
					    help="Only build configs and terminate after that. For debug purposes. [Default: %(default)s]")
	parser.add_argument("-n", "--n-processes", type=int, default=1,
	                    help="Number of (parallel) processes. [Default: %(default)s]")
	parser.add_argument("-f", "--n-plots", type=int, nargs=2, default=[None, None],
	                    help="Number of plots for datacard inputs (1st arg) and for postfit plots (2nd arg). [Default: all]")
	parser.add_argument("-o", "--output-dir",
	                    default="$CMSSW_BASE/src/CombineHarvester/HTTSMCPDecays18/",
	                    help="Output directory. [Default: %(default)s]")
	parser.add_argument("--output-suffix",
	                    default="RWTH",
	                    help="Output folder within output directory. [Default: %(default)s]")
	parser.add_argument("--clear-output-dir", action="store_true", default=False,
	                    help="Delete/clear output directory before running this script. [Default: %(default)s]")
	parser.add_argument("--scale-lumi", default=False,
	                    help="Scale datacard to luminosity specified. [Default: %(default)s]")
	parser.add_argument("--era", default="2016",
	                    help="Era of samples to be used. [Default: %(default)s]")
	parser.add_argument("--debug-plots", default=False, action="store_true",
	                    help="Produce debug Plots [Default: %(default)s]")
	parser.add_argument("-e", "--exclude-cuts", nargs="+", default=[],
	                    help="Exclude (default) selection cuts. [Default: %(default)s]")
	parser.add_argument("--hypothesis", nargs="+",
	                    default=["susycpodd"],
	                    choices=["susycpodd", "cpodd", "cpmix"],
	                    help="Choose the hypothesis to test against CPeven hypothesis. Option needed for final state studies. [Default: %(default)s]")
	parser.add_argument("--no-shape-uncs", default=False, action="store_true",
	                    help="Do not include shape uncertainties. [Default: %(default)s]")
	parser.add_argument("--scale-sig-IC", default=False, action="store_true",
	                    help="Scale signal cross section to IC cross section. [Default: %(default)s]")
	parser.add_argument("--no-syst-uncs", default=False, action="store_true",
	                    help="Do not include systematic uncertainties. This should only be used together with --use-asimov-dataset. [Default: %(default)s]")
	parser.add_argument("--production-mode", nargs="+",
	                    default=["ggh", "qqh"],
	                    choices=["ggh", "qqh"],
	                    help="Choose the production modes. Option needed for initial state studies. [Default: %(default)s]")
	parser.add_argument("--qcd-subtract-shapes", action="store_false", default=True, help="subtract shapes for QCD estimation [Default:%(default)s]")
	parser.add_argument("--steps", nargs="+",
	                    default=["inputs", "datacards", "t2w", "likelihoodscan"],
	                    choices=["inputs", "datacards", "t2w", "likelihoodscan", "prefitpostfitplots_setup", "prefitpostfitplots_makeplots"],
	                    help="Steps to perform.[Default: %(default)s]\n 'inputs': Writes datacards and fills them using HP.\n 't2w': Create ws.root files form the datacards. 't2w': Perform likelihood scans for various physical models and plot them.")
	parser.add_argument("--use-shape-only", action="store_true", default=False,
	                    help="Use only shape to distinguish between cp hypotheses. [Default: %(default)s]")
	parser.add_argument("--get-official-dc", action="store_true", default=True,
	                    help="Get official CP datacards. [Default: %(default)s]")
	parser.add_argument("--do-not-ignore-category-removal", default=False, action="store_true",
						help="Exit program in case categories are removed from CH. [Default: %(default)s]")
	parser.add_argument("--use-asimov-dataset", action="store_true", default=False,
	                    help="Use s+b expectation as observation instead of real data. [Default: %(default)s]")
	parser.add_argument("--use-rateParam", action="store_true", default=False,
	                    help="Use rate parameter to estimate ZTT normalization from ZMM. [Default: %(default)s]")
	parser.add_argument("--x-bins", default=None,
	                    help="Manualy set the binning. Default is taken from configuration files.")
	parser.add_argument("--no-ewkz-as-dy", default=False, action="store_true",
	                    help="Do not include EWKZ samples in inputs for DY. [Default: %(default)s]")
	parser.add_argument("--emb", default=False, action="store_true",
	                    help="Use Embedded Samples instead of DY MC. [Default: %(default)s]")
	parser.add_argument("--legacy", default=False, action="store_true",
	                    help="Use legacy Samples and Settings. [Default: %(default)s]")

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
	else:
		log.critical("Invalid era string selected: " + args.era)
		sys.exit(1)

	args.output_dir = os.path.abspath(os.path.expandvars(args.output_dir))
	if args.clear_output_dir:
		clear_output_dir = raw_input("Do you really want to clear the output directory? [yes]").lower() == "yes"
		if not clear_output_dir:
			log.info("Terminate. Remove the clear_output_dir option and run the programm again.")
			sys.exit(1)
		logger.subprocessCall("rm -r " + args.output_dir, shell=True)

	# initialisations for plotting
	sample_settings = samples.Samples()
	binnings_settings = binnings.BinningsDict()
	labels_settings = labels.LabelsDict(latex_version="root")
	systematics_factory = systematics.SystematicsFactory()
	background_method = args.background_method

	plot_configs = []
	output_files = []
	merged_output_files = []
	hadd_commands = []

	"""
	# final state studies
	if args.cp_study == "final":
		if "susycpodd" in args.hypothesis:
			signal_processes.append("CPEVEN")
			signal_processes.append("SUSYCPODD_ALT")
		if "cpodd" in args.hypothesis:
			signal_processes.append("CPEVEN")
			signal_processes.append("CPODD_ALT")
		if "cpmix" in args.hypothesis:
			signal_processes.append("CPEVEN")
			signal_processes.append("CPMIX_ALT")
	"""

	datacards = None
	category_replacements = {}
	if len(args.channel)>1:
		channelstring = ",".join(args.channel[1:])
	else:
		channelstring = "all"
	print channelstring
	# get "official" configuration
	init_directory = os.path.join(args.output_dir, "output/{OUTPUT_SUFFIX}/".format(OUTPUT_SUFFIX=args.output_suffix))
	# if args.emb:
	# 	command = "MorphingSMCPDecays18 --real_data=false --era={ERA} --channels={CHANNELS} --postfix -2D --ttbar_fit=false {INIT}".format(
	# 		ERA=args.era,
	# 		CHANNELS = channelstring,
	# 		INIT="--only_init="+os.path.join(init_directory, "init")
	# 	)
	if args.emb:
		command = "MorphingSMCPDecays18 --era={ERA} --channels={CHANNELS} --do_mva=false --do_jetfakes=true --do_embedding=true --postfix=\"-2D\" --ttbar_fit=false {INIT} {SHAPE_UNCS}".format(
			ERA=args.era,
			CHANNELS = channelstring,
			INIT="--only_init="+os.path.join(init_directory, "init"),
			SHAPE_UNCS="--no_shape_systs=1" if args.no_shape_uncs else "",
		)
	else:
		command = "MorphingSMCPDecays18 --era={ERA} --channels={CHANNELS} --do_mva=false --do_jetfakes=true --do_embedding=false --postfix=\"-2D\" --ttbar_fit=false {INIT} {SHAPE_UNCS}".format(
			ERA=args.era,
			CHANNELS = channelstring,
			INIT="--only_init="+os.path.join(init_directory, "init"),
			SHAPE_UNCS="--no_shape_systs=1" if args.no_shape_uncs else "",
		)
	log.debug(command)
	exit_code = logger.subprocessCall(shlex.split(command))
	assert(exit_code == 0)

	init_cb = ch.CombineHarvester()
	for init_datacard in glob.glob(os.path.join(os.path.join(init_directory, "init"), "*_*_*_*.txt")):
		init_cb.QuickParseDatacard(init_datacard, '$ANALYSIS_$CHANNEL_$ERA_$BINID_$MASS.txt')

	#init_cb.PrintObs().PrintProcs().PrintSysts()

	if args.era == "2017":
		print "THINGS TO BE CHANGED FOR 2017"
		#print datacards.cb.cp().process(["qqHmm_htt"])
		#datacards.cb.cp().process(["qqHmm_htt"]).FilterAll()
		#cmb.FilterProcs([]
		a_ = init_cb

		#filter_proc2017 = ["qqHsm_htt125", "qqHsm_htt", "qqHps_htt", "qqHmm_htt", "WH_htt125", "ZH_htt125", "VV", "VVT", "VVJ"]

		#a_ = a_.cp().process(filter_proc2017, False)

		print args.channel[1:]
		a_ = a_.cp().channel(args.channel[1:], True)

		print "-----------------------------------------------------------------"
		#datacards.cb.PrintObs().PrintProcs().PrintSysts()
		init_cb = a_


	#init_cb.PrintObs().PrintProcs().PrintSysts()
	datacards = initialstatecpstudiesdatacards.InitialStateCPStudiesDatacards(
			cb=init_cb,
			higgs_masses=args.higgs_masses,
			year=args.era,
			cp_study=args.cp_study
	)
	datacards.lnN2shape(is_lnN=["CMS_ggH_STXSVBF2j", "CMS_ggH_STXSmig01", "CMS_ggH_STXSmig12"])

		# The processes have different names in the official SM datacards
		# So this workaround is needed to match the right processes
	datacards.configs._mapping_process2sample = {
		"data_obs" : "data",
		"EWKZ" : "ewkz",
		"ggH_ph_htt" : "ggh",
		# "ggH_ps_htt"	: "gghmadgraphps",
		# "ggH_mm_htt"	: "gghmadgraphmm",
		# "ggH_sm_htt"	: "gghmadgraphsm",
		"ggH_ps_htt"	: "gghps",
		"ggH_mm_htt"	: "gghmm",
		"ggH_sm_htt"	: "gghsm",
		"ggH_hww" : "hww_gg",
		"QCD" : "qcd",
		# "qqH_mm_htt"	: "qqhjhumm",
		# "qqH_ps_htt"	: "qqhjhups",
		# "qqH_sm_htt"	: "qqhjhusm",
		"qqH_mm_htt"	: "qqhmm",
		"qqH_ps_htt"	: "qqhps",
		"qqH_sm_htt"	: "qqhsm",
		"qqH_hww" : "hww_qq",
		"TT" : "ttj",
		"TTT" : "ttt",
		"TTJ" : "ttj",
		"VV" : "vv",
		"VVT" : "vvt",
		"VVJ" : "vvj",
		"WH_sm_htt" : "whsm",
		"WH_mm_htt" : "whmm",
		"WH_ps_htt" : "whps",
		"W" : "wj",
		"ZH_sm_htt" : "zhsm",
		"ZH_mm_htt" : "zhmm",
		"ZH_ps_htt" : "zhps",
		"ZJ" : "zj",
		"ZL" : "zl",
		"ZLL" : "zll",
		"ZTT" : "ztt",
		"jetFakes" : "ff",
		"WH_htt125" : "wh",
		"ZH_htt125" : "zh",
		"qqHsm_htt125": "qqh",
		"EmbedZTT" : "ztt_emb"
		}

	# Also the categories have different names.
	# Match SM categories and control regions.
	category_replacements["all"] = "TTbarCR"

	category_replacements["0jet"] = "ZeroJetCP"
	category_replacements["boosted"] = "BoostedCP"
	category_replacements["dijet_lowboost_mixed"] = "dijet_lowboost_mixed"
	category_replacements["dijet_boosted_mixed"] = "dijet_boosted_mixed"

	# initialise datacards
	year_string = "/2017/" if args.era=="2017" else ""
	tmp_input_root_filename_template = "shapes/"+args.output_suffix+"/${CHANNEL}/"+year_string+"${ANALYSIS}_${CHN}_${BIN}_${SYSTEMATIC}_${ERA}.root"
	input_root_filename_template = "shapes/"+args.output_suffix+"/${CHANNEL}$/"+year_string+"{ANALYSIS}_${CHN}.inputs-sm-${ERA}-2D.root"
	bkg_histogram_name_template = "${BIN}/${PROCESS}"
	sig_histogram_name_template = "${BIN}/${PROCESS}${MASS}"
	bkg_syst_histogram_name_template = "${BIN}/${PROCESS}_${SYSTEMATIC}"
	sig_syst_histogram_name_template = "${BIN}/${PROCESS}${MASS}_${SYSTEMATIC}"
	datacard_filename_templates = datacards.configs.cp_datacard_filename_templates
	output_root_filename_template = "datacards/common/${ANALYSIS}.inputs-sm-${ERA}-2D.root"

	if args.channel != parser.get_default("channel"):
		channel_list = args.channel[len(parser.get_default("channel")):]
	else:
		channel_list = ["em","et","mt","tt","ttbar"]

	print channel_list

	for chan in channel_list:
		category_replacements["all"] = "TTbarCR"

		category_replacements[chan+"_0jet"] = chan+"_ZeroJetCP"
		category_replacements[chan+"_boosted"] = chan+"_BoostedCP"
		category_replacements[chan+"_dijet_lowboost_mixed"] = chan+"_dijet_lowboost_mixed"
		category_replacements[chan+"_dijet_boosted_mixed"] = chan+"_dijet_boosted_mixed"


	if args.categories != parser.get_default("categories"):
		args.categories = args.categories[1:]

	# catch if on command-line only one set has been specified and repeat it
	if(len(args.categories) == 1):
		args.categories = [args.categories[0]] * len(args.channel)

	# list of JEC uncertainties
	jecUncertNames = [
		"AbsoluteFlavMap",
		"AbsoluteMPFBias",
		"AbsoluteScale",
		"AbsoluteStat",
		"FlavorQCD",
		"Fragmentation",
		"PileUpDataMC",
		"PileUpPtBB",
		"PileUpPtEC1",
		"PileUpPtEC2",
		"PileUpPtHF",
		"PileUpPtRef",
		"RelativeBal",
		"RelativeFSR",
		"RelativeJEREC1",
		"RelativeJEREC2",
		"RelativeJERHF",
		"RelativePtBB",
		"RelativePtEC1",
		"RelativePtEC2",
		"RelativePtHF",
		"RelativeStatEC",
		"RelativeStatFSR",
		"RelativeStatHF",
		"SinglePionECAL",
		"SinglePionHCAL",
		"TimePtEta",
		"eta0to5",
		"eta0to3",
		"eta3to5",
		"Total",
		"Closure"
	]

	do_not_normalize_by_bin_width = args.do_not_normalize_by_bin_width

	#restriction to requested systematics
	if args.no_shape_uncs:
		datacards.remove_shape_uncertainties()
	#restriction to requested masses

	if args.get_official_dc:
		datacards.cb.mass(["*"]+args.higgs_masses)

	#restriction to requested channels
	if args.channel != parser.get_default("channel"):
		datacards.cb.channel(args.channel[1:])
	args.channel = datacards.cb.cp().channel_set()
	if args.categories == parser.get_default("categories"):
		args.categories = (len(args.channel)-1) * args.categories


	for index, (channel, categories) in enumerate(zip(args.channel, args.categories)):
		chn = channel if channel != "ttbar" else "em"
		if args.get_official_dc:
			if channel in ["ttbar","em"]:
				datacards.configs._mapping_process2sample["ZLL"] = "zll"
			else:
				datacards.configs._mapping_process2sample["ZL"] = "zl"

			if channel in ["et", "mt", "tt"] :
				datacards.configs._mapping_process2sample.pop("TT", None)
				datacards.configs._mapping_process2sample["TTT"]= "ttt"
				datacards.configs._mapping_process2sample["TTJ"]= "ttjj"
			else:
				datacards.configs._mapping_process2sample["TT"] = "ttj"
				datacards.configs._mapping_process2sample.pop("TTT")
				datacards.configs._mapping_process2sample.pop("TTJ")

		tmp_output_files = []


		if "all" in categories:
			categories = datacards.cb.cp().channel([channel]).bin_set()
		else:
			# include channel prefix
			categories = [chn + "_" + category for category in categories]

		# prepare category settings based on args and datacards
		categories_save = sorted(categories)
		categories = list(set(categories).intersection(set(datacards.cb.cp().channel([channel]).bin_set())))
		if(categories_save != sorted(categories)) and args.do_not_ignore_category_removal:
			log.fatal("CombineHarverster removed the following categories automatically. Was this intended?")
			log.fatal(list(set(categories_save) - set(categories)))
			sys.exit(1)

		output_file = os.path.join(args.output_dir, input_root_filename_template.replace("$", "").format(
				ANALYSIS="htt",
				CHANNEL=chn,
				CHN=chn,
				ERA="13TeV"
		))

		# restrict CombineHarvester to configured categories:
		datacards.cb.FilterAll(lambda obj : (obj.channel() == channel) and (obj.bin() not in categories))
		log.info("Building configs for channel = {channel}, categories = {categories}".format(channel=channel, categories=str(categories)))
		for official_category in categories:
			# Do the category replacement to get the names defined in expressions.py
			print("official_category    " , official_category)
			category = official2private(official_category, category_replacements)
			print("category    ", category)
			datacards_per_channel_category = initialstatecpstudiesdatacards.InitialStateCPStudiesDatacards(cb=datacards.cb.cp().channel([channel]).bin([official_category]))
			exclude_cuts = copy.deepcopy(args.exclude_cuts)

			# Custumization necessary for the control regions
			if "ttbar" in category:
				exclude_cuts += ["pzeta"] # Studies show that the operator is the fastest way to add something to a list
				do_not_normalize_by_bin_width = True

			higgs_masses = [mass for mass in datacards_per_channel_category.cb.mass_set() if mass != "*"]

			#merged_output_files.append(output_file)
			#from IPython import embed;embed()
			for shape_systematic, list_of_samples in datacards_per_channel_category.get_samples_per_shape_systematic(lnN_syst=["CMS_ggH_STXSVBF2j", "CMS_ggH_STXSmig01", "CMS_ggH_STXSmig12", "CMS_eff_b_13TeV"]).iteritems():

				nominal = (shape_systematic == "nominal")
				list_of_samples = [datacards.configs.process2sample(process) for process in list_of_samples]
				#print "<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<"
				#print shape_systematic

				if shape_systematic == "CMS_ttbar_embeded_13TeV":
					list_of_samples += ["vvt", "ttt"]

				# This is needed because wj and qcd are interdependent when using the new background estimation method
				# NB: CH takes care to only use the templates for processes that you specified. This means that any
				#     superfluous histograms created as a result of this problem do not influence the result
				if background_method == "simeqn":
					if "qcd" in list_of_samples and "wj" not in list_of_samples:
						list_of_samples += ["wj"]
					elif "wj" in list_of_samples and "qcd" not in list_of_samples:
						list_of_samples += ["qcd"]

				for shift_up in ([True] if nominal else [True, False]):
					systematic = "nominal" if nominal else (shape_systematic + ("Up" if shift_up else "Down"))

					config={}

					log.debug("Create inputs for (samples, systematic) = ([\"{samples}\"], {systematic}), (channel, category) = ({channel}, {category}).".format(
							samples="\", \"".join(list_of_samples),
							channel=channel  if category not in "em_ttbar" else "em",
							category=category,
							systematic=systematic
					))
					"""
					wj_sf_shift = wj_sf_shifts.get(category,0.0)
					if "WSFUncert" in shape_systematic and wj_sf_shift != 0.0:
						wj_sf_shift = 1.0 + wj_sf_shift if shift_up else 1.0 - wj_sf_shift
					else:
						wj_sf_shift = 0.0
					"""
					# Use official zmm corrections factors for now TODO: To be updated
					#zmm_cr_factor = zmm_cr_factors.get(category.split("_")[-1],"(1.0)")
					#zmm_cr_factor = zmm_cr_factors_official.get(category, "(1.0)")
					if "zmumuShape_VBF" in shape_systematic:
						#zmm_cr_factor = zmm_cr_factors.get(category.split("_")[-1]+("_Up" if shift_up else "_Down"),"(1.0)")
						zmm_cr_factor = zmm_cr_factors_official.get(category+("_Up" if shift_up else "_Down"),"(1.0)")
					# prepare plotting configs for retrieving the input histograms

					category_suffix =""

					if "dijet" in category and "recoPhiStarCPCombMergedHelrPVBS" in args.quantity:
						category_suffix = "_CPCombMerged"

					if "boosted" in category and "recoPhiStarCPCombMergedHelrPVBS" in args.quantity:
						category_suffix = "_CPCombMerged"

					config = sample_settings.get_config(
							samples=[getattr(samples.Samples, sample) for sample in list_of_samples],
							channel=channel if category not in "em_ttbar" else "em",
							category="catcptautau2017_"+category+category_suffix,
							weight=args.weight,
							lumi = args.lumi * 1000,
							exclude_cuts=exclude_cuts,
							higgs_masses=higgs_masses,
							cut_type="cpggh2016" if args.era == "2016" else "cptautau2017legacy" if args.era == "2017" else "baseline",
							estimationMethod="simeqn",
							#zmm_cr_factor=zmm_cr_factor,
							no_ewkz_as_dy = args.no_ewkz_as_dy,
							fakefactor_method = True,
							state = "finalState",
							asimov_nicks= ["ff", "zl", "vvt", "ttt", "ewkz", "gghsm125", "qqhsm125", ("ztt_emb" if args.emb else "ztt")] if args.use_asimov_dataset else [], # TODO: generalize
							# proxy_fakefactors = True # doesn't work for 2D plots
					)
					print shape_systematic
					if "CMS_scale_gg_13TeV" in shape_systematic:
						systematics_settings = systematics_factory.get(shape_systematic)(config, category)
					elif "CMS_scale_j_" in shape_systematic:
						systematics_settings = systematics_factory.get(shape_systematic)(config, shape_systematic)

					elif shape_systematic.startswith("ff_"):
						systematics_settings = systematics_factory.get(shape_systematic)(config, shape_systematic)
					else:
						systematics_settings = systematics_factory.get(shape_systematic)(config)
					# TODO: evaluate shift from datacards_per_channel_category.cb
					config = systematics_settings.get_config(shift=(0.0 if nominal else (1.0 if shift_up else -1.0)))

					#if "CMS_scale_j_" in shape_systematic:
					#	from IPython import embed; embed()
					"""
					for index, weight in enumerate(config.get("weights", [])):
						weightAtIndex = config["weights"][index]
						if channel in ["mt", "et", "tt"]:
							if config["nicks"][index] in top_pt_reweight_nicks or channel == "tt":
								weightAtIndex = weightAtIndex.replace("topPtReweightWeight", "topPtReweightWeightRun1")

						config["weights"][index] = weightAtIndex
					"""

					config["x_expressions"] = ["melaDiscriminatorD0MinusGGH"] if "mela" in args.quantity else ["recoPhiStarCPCombMergedHelrPVBS"]

					if (args.cp_study == "ggh" or args.cp_study == "vbf") and "mela" not in category:
						binnings_key = "tt_jdphi"
					if (args.cp_study == "final") and "mela" not in category:
						binnings_key = "tt_" + args.quantity;
					if (args.cp_study == "ggh" or args.cp_study == "vbf") and "mela" in category:
						binnings_key = "tt_melaDiscriminatorD0Minus"
					if (args.cp_study == "ggh" or args.cp_study == "vbf") and "mela" in category and "Vbf4D" in category:
						binnings_key = "tt_melaDiscriminatorD0Minus_signDCP"

					"""
					# customizations necessary for the control regions
					# define quantities and binning for control regions
					if ("wjets" in category or "qcd_cr" in category) and channel in ["mt", "et"]:
						config["x_expressions"] = ["m_sv"]
						config["x_bins"] = [binnings_settings.binnings_dict["binningHtt13TeV_tt_dijet_boosted_qcd_cr_m_sv"]] # 0.0-250-0 one bin
					if "qcd_cr" in category and channel == "tt":
						config["x_expressions"] = ["m_sv"]
						config["x_bins"] = [binnings_settings.binnings_dict["binningHtt13TeV_tt_dijet_boosted_qcd_cr_m_sv"]] # 0.0-250-0 one bin
					if "ttbar" in category:
						config["x_expressions"] = ["m_sv"]
						config["x_bins"] = [binnings_settings.binnings_dict["binningHtt13TeV_"+category+"_m_sv"]]

					if any( cr in category for cr in ["dijet2D_boosted_qcd_cr", "dijet2D_lowboost_qcd_cr"]) and channel == "tt" and args.quantity == "jdphi":
						config["x_bins"] = [binnings_settings.binnings_dict["binningHtt13TeV_"+category+"_jdphi"]]

					# if any( cr in category for cr in ["dijet2D_lowboost_qcd_cr", "dijet2D_boosted_qcd_cr"]) and channel == "tt" and "mela" in args.quantity:
					# 	config["x_bins"] = [binnings_settings.binnings_dict["binningHtt13TeV_"+category+"_dcp_star"]]
					"""

					# Use 2d plots for 2d categories
					if "ZeroJetCP" in category and not ("wjets" in category or "qcd_cr" in category):
						# Use only m_sv/ m_vis as discriminator opposed to SM analysis. By neglecting the split into decay mode we can drop 5 systematic uncertainites.
						# Also use only m_sv as a further simplification.
						config["x_expressions"] = ["m_sv"]
						config["x_bins"] = [binnings_settings.binnings_dict["binningHttCP13TeV_"+category+"_m_sv"]]
					elif "BoostedCP" in category and not ("wjets" in category or "qcd_cr" in category or "dijet" in category):
						config["x_expressions"] = ["m_vis" if channel == "mm" else "m_sv"]
						# config["y_expressions"] = ["H_pt"]
						config["x_bins"] = [binnings_settings.binnings_dict["binningHttCP13TeV_"+category+("_m_vis" if channel == "mm" else "_m_sv")]]
						# config["y_bins"] = [binnings_settings.binnings_dict["binningHttCP13TeV_"+category+"_H_pt"]]

					elif "dijet" in category:
						config["x_expressions"] = ["m_vis" if channel == "mm" else "m_sv"]
						config["x_bins"] = [binnings_settings.binnings_dict["binningHtt13TeV_"+category+("_m_vis" if channel == "mm" else "_m_sv")]]

						if "mela2D" in args.quantity:
							config["y_expressions"] = ["melaDiscriminatorD0MinusGGH*TMath::Sign(1, melaDiscriminatorDCPGGH)"]
							config["y_bins"] = [binnings_settings.binnings_dict["binningHtt13TeV_"+category+"_dcp_star"]]
						elif "mela3D" in args.quantity:
							config["y_expressions"] = ["melaDiscriminatorD0MinusGGH"]
							config["y_bins"] = [binnings_settings.binnings_dict["binningHtt13TeV_"+category+"_melaDiscriminatorD0MinusGGH"]]
							config["z_expressions"] = ["melaDiscriminatorDCPGGH"]
							config["z_bins"] = [binnings_settings.binnings_dict["binningHtt13TeV_"+category+"_melaDiscriminatorDCPGGH"]]
						elif "mela_eta" in args.quantity:
							config["z_expressions"] = ["melaDiscriminatorD0MinusGGH*TMath::Sign(1, melaDiscriminatorDCPGGH)"]
							config["z_bins"] = [binnings_settings.binnings_dict["binningHtt13TeV_"+category+"_dcp_star"]]
							config["y_expressions"] = ["min(abs(eta_sv-jeta_1),abs(eta_sv-jeta_2))"]
							config["y_bins"] = [binnings_settings.binnings_dict["binningHtt13TeV_"+category+"_eta_sep"]]
						elif "recoPhiStarCPCombMergedHelrPVBS" in args.quantity:
							config["y_expressions"] = ["recoPhiStarCPCombMergedHelrPVBS"]
							config["y_bins"] = [binnings_settings.binnings_dict["binningHtt13TeV_"+category+"_recoPhiStarCPCombMergedHelrPVBS"]]
							config["x_bins"] = [binnings_settings.binnings_dict["binningHtt13TeV_"+category+("_m_vis" if channel == "mm" else "_m_sv")]]

					# Unroll 2d distribution to 1d in order for combine to fit it
					if ("dijet" in category) and not ("wjets" in category or "qcd_cr" in category) and not (channel == "tt" and "ZeroJetCP" in category):
						if not "UnrollHistogram" in config.get("analysis_modules", []):
							config.setdefault("analysis_modules", []).append("UnrollHistogram")
						config["unroll_ordering"] = "xyz"

					config["directories"] = [args.input_dir]
					#print "labels:      ", config["labels"]
					labellist=config["labels"]

					config["labels"]=[]
					for sample in list_of_samples:
						histogram_name_template = bkg_histogram_name_template if nominal else bkg_syst_histogram_name_template

						# if sample in ["gghmadgraphmm", "gghmadgraphps", "gghmadgraphsm"]:
						if sample in ["gghmm", "gghps", "gghsm", "qqhmm", "qqhps", "qqhsm"]:
							histogram_name_template = sig_histogram_name_template if nominal else sig_syst_histogram_name_template
							config["labels"].append( histogram_name_template.replace("$", "").format(
								PROCESS=datacards.configs.sample2process(sample),
								BIN=official_category,
								SYSTEMATIC=systematic,
								MASS="125"
							))
						else:
							config["labels"].append( histogram_name_template.replace("$", "").format(
								PROCESS=datacards.configs.sample2process(sample),
								BIN=official_category,
								SYSTEMATIC=systematic
						))

					tmp_output_file = os.path.join(args.output_dir, tmp_input_root_filename_template.replace("$", "").format(
							ANALYSIS="htt",
							CHANNEL=chn,
							CHN=chn,
							BIN=official_category,
							SYSTEMATIC=systematic,
							ERA="13TeV"
					))

					tmp_output_files.append(tmp_output_file)
					config["output_dir"] = os.path.dirname(tmp_output_file)
					config["filename"] = os.path.splitext(os.path.basename(tmp_output_file))[0]
					config["plot_modules"] = ["ExportRoot"]
					config["file_mode"] = "UPDATE"
					if "legend_markers" in config:
						config.pop("legend_markers")

					#pprint.pprint( config["files"])
					for i in range(len(config["files"])):
						if config["files"][i] == None:
							print i
							print config["nicks"][i]

					if ("qcd_cr" in category):
						print category
						print config["weights"]

					config["analysis_modules"] = ["AddHistograms", "SumOfHistograms", "BinErrorsOfEmptyBins", "CorrectNegativeBinContents", "UnrollHistogram"]
					print(config["analysis_modules"])
					config["labels"].append(config["labels"].pop(config["stacks"].index("data")))
					config["colors"].append(config["colors"].pop(config["stacks"].index("data")))
					config["markers"].append(config["markers"].pop(config["stacks"].index("data")))
					config["stacks"].append(config["stacks"].pop(config["stacks"].index("data")))
					print(config["labels"])
					print(config["colors"])
					print(config["markers"])
					print(config["stacks"])
					plot_configs.append(config)
			if "inputs" in args.steps:
				hadd_commands.append("hadd -f {DST} {SRC}".format(
						DST=output_file,
						SRC=" ".join(tmp_output_files)
				))
			merged_output_files.append(output_file)

		output_files.append(output_file)
	if log.isEnabledFor(logging.DEBUG):
		pprint.pprint(plot_configs)

	if args.only_config:
		sys.exit(1)
	# create input histograms with HarryPlotter
	if "inputs" in args.steps:
		log.info("\n -------------------------------------- Creating input histograms with HarryPlotter ---------------------------------")
		higgsplot.HiggsPlotter(list_of_config_dicts=plot_configs, list_of_args_strings=[args.args], n_processes=args.n_processes, n_plots=args.n_plots[0], batch=args.batch)

	if args.n_plots[0] != 0 and "t2w" in args.steps:
		print "====================================================================================================================="
		# tools.parallelize(_call_command, hadd_commands, n_processes=args.n_processes)
		for channel in channel_list:
			print channel
			if channel != "ttbar":
				channel_ = channel
			else: channel_="em"
			datacards_module._call_command([
				"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/scripts/hadd_shapes.sh {OUTPUT_FOLDER} {CHANNEL} {CHN}".format(OUTPUT_FOLDER=os.path.join(args.output_dir, "shapes", args.output_suffix), CHANNEL=channel_+year_string, CHN=channel if channel != "ttbar" else "em")
			])

	if args.debug_plots:
		debug_plot_configs = []
		for output_file in merged_output_files:
			debug_plot_configs.extend(plotconfigs.PlotConfigs().all_histograms(output_file, plot_config_template={"markers":["E"], "colors":["#FF0000"]}))
		higgsplot.HiggsPlotter(list_of_config_dicts=debug_plot_configs, list_of_args_strings=[args.args], n_processes=args.n_processes, n_plots=args.n_plots[1])

	# call official script again with shapes that have just been created
	# this steps creates the filled datacards in the output folder.

	if "datacards" in args.steps:
		print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
		print channelstring
		if args.emb:
			datacards_module._call_command([
				"MorphingSMCPDecays18 --output_folder={OUTPUT_SUFFIX} --era={ERA} --channels={CHANNELS} --do_mva=false --do_jetfakes=true --do_embedding=true --postfix=\"-2D\" {SHAPE_UNCS} {SCALE_SIG} --ttbar_fit=false --input_folder_mt={OUTPUT_SUFFIX}/mt/ --input_folder_et={OUTPUT_SUFFIX}/et/".format(
				OUTPUT_SUFFIX=args.output_suffix,
				ERA=args.era,
				CHANNELS = channelstring,
				SHAPE_UNCS="--no_shape_systs=1" if args.no_shape_uncs else "",
				SCALE_SIG="--scale_sig_procs=true" if args.scale_sig_IC else ""
				),
				args.output_dir
			])
		else:
			datacards_module._call_command([
				"MorphingSMCPDecays18 --output_folder={OUTPUT_SUFFIX} --era={ERA} --channels={CHANNELS} --do_mva=false --do_jetfakes=true --do_embedding=false --postfix=\"-2D\" {SHAPE_UNCS} {SCALE_SIG} --ttbar_fit=false --input_folder_mt={OUTPUT_SUFFIX}/mt/ --input_folder_et={OUTPUT_SUFFIX}/et/".format(
				OUTPUT_SUFFIX=args.output_suffix,
				ERA=args.era,
				CHANNELS = channelstring,
				SHAPE_UNCS="--no_shape_systs=1" if args.no_shape_uncs else "",
				SCALE_SIG="--scale_sig_procs=true" if args.scale_sig_IC else ""
				),
				args.output_dir
			])
		log.info("\nDatacards have been written to \"%s\"." % os.path.join(os.path.join(args.output_dir)))
	print "--------------------------------------------------------------------------------------------------------------------------------------"
	datacards_path = args.output_dir+"/output/"+args.output_suffix+"/cmb/125/"
	official_cb = ch.CombineHarvester()

	# sys.exit(0)

	datacards_cbs = {}
	datacards_workspaces_alpha = {}

	for official_datacard in glob.glob(os.path.join(datacards_path, "*_*_*_*.txt")):
		official_cb.QuickParseDatacard(official_datacard, '$ANALYSIS_$CHANNEL_$ERA_$BINID_$MASS.txt')
		#official_cb.PrintObs().PrintProcs().PrintSysts()

		if args.era == "2017":
			print "THINGS TO BE CHANGED FOR 2017"
			#print datacards.cb.cp().process(["qqHmm_htt"])
			#datacards.cb.cp().process(["qqHmm_htt"]).FilterAll()
			#cmb.FilterProcs([]
			b_ = official_cb

			#filter_proc2017 = ["qqHsm_htt125", "qqHsm_htt", "qqHps_htt", "qqHmm_htt", "WH_htt125", "ZH_htt125", "VV", "VVT", "VVJ"]

			#b_ = b_.cp().process(filter_proc2017, False)

			print args.channel
			b_ = b_.cp().channel(args.channel[1:], True)
			print "-----------------------------------------------------------------"
			#datacards.cb.PrintObs().PrintProcs().PrintSysts()
			#official_cb = b_
		#official_cb.PrintObs().PrintProcs().PrintSysts()

		tmp_datacard = ch.CombineHarvester()
		tmp_datacard.QuickParseDatacard(official_datacard, '$ANALYSIS_$CHANNEL_$ERA_$BINID_$MASS.txt')
			#from IPython import embed; embed()
		print "int(official_datacard.split(\"_\")[-2]): ", int(official_datacard.split("_")[-2])
		if int(official_datacard.split("_")[-2]) < 10 and not "ttbar" in official_datacard: #this statement avoids the creation of workspaces for single CR only.
			datacards_cbs[official_datacard] = tmp_datacard.cp()
			if "prefitpostfitplots_setup" in args.steps:
				print "Starting step: prefitpostfitplots_setup"
				datacards_module._call_command([
						"combineTool.py -M T2W -P CombineHarvester.CombinePdfs.CPMixtureDecays:CPMixtureDecays -i {DATACARD} -o {OUTPUT} --parallel {N_PROCESSES}".format(
						DATACARD=official_datacard,
						OUTPUT=os.path.splitext(official_datacard)[0]+"_cpmixture.root",
						N_PROCESSES=args.n_processes
						),
						args.output_dir
				])
				datacards_workspaces_alpha[official_datacard] = os.path.splitext(official_datacard)[0]+"_cpmixture.root"

	datacards = initialstatecpstudiesdatacards.InitialStateCPStudiesDatacards(
			cb=official_cb,
			higgs_masses=args.higgs_masses,
			year=args.era,
			cp_study=args.cp_study
	)
	datacards.configs._mapping_process2sample = {
		"data_obs" : "data",
		"EWKZ" : "ewkz",
		"ggH_htt" : "ggh",
		# "ggHps_htt"	: "gghmadgraphps",
		# "ggHmm_htt"	: "gghmadgraphmm",
		# "ggHsm_htt"	: "gghmadgraphsm",
		"ggH_ps_htt"	: "gghps",
		"ggH_mm_htt"	: "gghmm",
		"ggH_sm_htt"	: "gghsm",
		"ggH_hww" : "hww_gg",
		"QCD" : "qcd",
		"qqH_htt" : "qqh",
		# "qqHmm_htt"	: "qqhjhumm",
		# "qqHps_htt"	: "qqhjhups",
		# "qqHsm_htt"	: "qqhjhusm",
		"qqH_mm_htt"	: "qqhmm",
		"qqH_ps_htt"	: "qqhps",
		"qqH_sm_htt"	: "qqhsm",
		"qqH_hww" : "hww_qq",
		"TT" : "ttj",
		"TTT" : "ttt",
		"TTJ" : "ttj",
		"VV" : "vv",
		"VVT" : "vvt",
		"VVJ" : "vvj",
		"WH_htt125" : "wh",
		"W" : "wj",
		"ZH_htt125" : "zh",
		"ZJ" : "zj",
		"ZL" : "zl",
		"ZLL" : "zll",
		"ZTT" : "ztt",
		# "ggHps_htt125"	: "gghmadgraphps",
		# "ggHmm_htt125"	: "gghmadgraphmm",
		# "ggHsm_htt125"	: "gghmadgraphsm",
		"ggH_ps_htt125"	: "gghps",
		"ggH_mm_htt125"	: "gghmm",
		"ggH_sm_htt125"	: "gghsm",
		"qqH_mm_htt125"	: "qqhmm",
		"qqH_ps_htt125"	: "qqhps",
		"qqH_sm_htt125"	: "qqhsm",
		"EmbedZTT" : "ztt_emb"
		}

	# Create workspaces from the datacards
	if "t2w" in args.steps:
		datacards_module._call_command([
				"combineTool.py -M T2W -P CombineHarvester.CombinePdfs.CPMixtureDecays:CPMixtureDecays -i output/{OUTPUT_SUFFIX}/{{cmb,{CHANNELS}}}/* -o ws.root --parallel {N_PROCESSES}".format(
				OUTPUT_SUFFIX=args.output_suffix,
				CHANNELS=",".join(channel_list)+"_2017" if args.era == "2017" else "",
				N_PROCESSES=args.n_processes
				),
				args.output_dir
		])
		log.info("\nWorkspaces have been created in \"%s\"." % os.path.join(os.path.join(args.output_dir, "output/{OUTPUT_SUFFIX}/{{cmb,em,et,mt,tt}}/*".format(
				OUTPUT_SUFFIX=args.output_suffix,
				YEAR = "_2017" if args.era == "2017" else ""
				)
				)))

	# Perform likelihoodscan
	if "likelihoodscan" in args.steps:
		if args.era == "2017":
			combine_dir_list = [s +"_2017" for s in channel_list]
		else:
			combine_dir_list = channel_list
		print combine_dir_list
		log.info("\nScanning alpha with muF=1,alpha=0 with asimov dataset.") #FIXME ,muV=1, f=0
		datacards_module._call_command([
				"combineTool.py -m 125 -M MultiDimFit --setParameters alpha=0 --setParameterRanges alpha=-1,1 --points 20 --redefineSignalPOIs alpha -d output/{OUTPUT_SUFFIX}/{{cmb,{CHANNELS}}}/125/ws.root --algo grid -t -1 --there -n .alpha --parallel={N_PROCESSES} --floatOtherPOIs 1 --cminFallbackAlgo Minuit2,0:1.0".format(
				OUTPUT_SUFFIX=args.output_suffix,
				CHANNELS=",".join(combine_dir_list), #TODO change this to use only a single channel
				N_PROCESSES=args.n_processes
				),
				args.output_dir
		])
		# datacards_module._call_command([
		# 		"combineTool.py -m 125 -M MultiDimFit --setParameters muF=1,muV=1,alpha=0,f=0 --freezeParameters f --setParameterRanges muF=0,4 --points 20 --redefineSignalPOIs muF -d output/{OUTPUT_SUFFIX}/{{cmb,em,et,mt,tt}}/125/ws.root --algo grid -t -1 --there -n .muF --parallel={N_PROCESSES}".format(
		# 		OUTPUT_SUFFIX=args.output_suffix,
		# 		N_PROCESSES=args.n_processes
		# 		),
		# 		args.output_dir
		# ])
		# datacards_module._call_command([
		# 		"combineTool.py -m 125 -M MultiDimFit --setParameters muF=1,muV=1,alpha=0,f=0 --freezeParameters f,muF --setParameterRanges alpha=0,1 --points 20 --redefineSignalPOIs alpha_freezemuF -d output/{OUTPUT_SUFFIX}/{{cmb,em,et,mt,tt}}/125/ws.root --algo grid -t -1 --there -n .muF --parallel={N_PROCESSES}".format(
		# 		OUTPUT_SUFFIX=args.output_suffix,
		# 		N_PROCESSES=args.n_processes
		# 		),
		# 		args.output_dir
		# ])
		# datacards_module._call_command([
		# 		"combineTool.py -m 125 -M MultiDimFit --setParameters muF=1,muV=1,alpha=0,f=0 --freezeParameters f --setParameterRanges alpha=0,1 --redefineSignalPOIs alpha,muF -d output/{OUTPUT_SUFFIX}/{{cmb,em,et,mt,tt}}/125/ws.root --points 500 --algo grid -t -1 --there -n .2DScan --parallel={N_PROCESSES}".format(
		# 		OUTPUT_SUFFIX=args.output_suffix,
		# 		N_PROCESSES=args.n_processes
		# 		),
		# 		args.output_dir
		# ])

		for channel in ["cmb"]+channel_list:
			directory = "output/"+args.output_suffix+"/"+channel+"_2017/125/" if (args.era == "2017" and channel!="cmb") else "/125/"
			datacards_module._call_command([
					"python $CMSSW_BASE/src/CombineHarvester/HTTSMCPDecays18/scripts/plot1DScan.py --main={INPUT_FILE} --POI=alpha --output={OUTPUT_FILE} --no-numbers --no-box --x_title='#alpha (#frac{{#pi}}{{2}})' --y-max=3.0 --logo 'Work in progress' --logo-sub '' ".format(
					INPUT_FILE=directory+"higgsCombine.alpha.MultiDimFit.mH125.root",
					OUTPUT_FILE=directory+"alpha"
					),
					args.output_dir
			])
			# datacards_module._call_command([
			# 		"python $CMSSW_BASE/src/CombineHarvester/HTTSMCPDecays18/scripts/plot1DScan.py --main={INPUT_FILE} --POI=muF --output={OUTPUT_FILE} --no-numbers --no-box --x_title='#mu_{{F}}' --y-max=10.0".format(
			# 		INPUT_FILE=directory+"higgsCombine.muF.MultiDimFit.mH125.root",
			# 		OUTPUT_FILE=directory+"muF"
			# 		),
			# 		args.output_dir
			# ])
		if args.era == "2017":
			datacards_module._call_command([
				"python $CMSSW_BASE/src/CombineHarvester/HTTSMCPDecays18/scripts/plot1DScan.py --main={INPUT_FILE} --POI=alpha --output={OUTPUT_FILE} --no-numbers --no-box --x_title='#alpha (#frac{{#pi}}{{2}})' --y-max=3.0 --others output/{OUTPUT_SUFFIX}/mt_2017/125/higgsCombine.alpha.MultiDimFit.mH125.root:#mu#tau_{{h}}:7 output/{OUTPUT_SUFFIX}/et_2017/125/higgsCombine.alpha.MultiDimFit.mH125.root:e#tau_{{h}}:9 --logo 'Work in progress' --logo-sub '' --main-label Expected ".format(
				INPUT_FILE="output/"+args.output_suffix+"/cmb/125/higgsCombine.alpha.MultiDimFit.mH125.root",
				OUTPUT_FILE="output/"+args.output_suffix+"/cmb/125/alpha_channel_comparison",
				OUTPUT_SUFFIX=args.output_suffix
				),
				args.output_dir
		])
		else:
			datacards_module._call_command([
					"python $CMSSW_BASE/src/CombineHarvester/HTTSMCPDecays18/scripts/plot1DScan.py --main={INPUT_FILE} --POI=alpha --output={OUTPUT_FILE} --no-numbers --no-box --x_title='#alpha (#frac{{#pi}}{{2}})' --y-max=3.0 --others output/{OUTPUT_SUFFIX}/tt/125/higgsCombine.alpha.MultiDimFit.mH125.root:#tau_{{h}}#tau_{{h}}:2 output/{OUTPUT_SUFFIX}/mt/125/higgsCombine.alpha.MultiDimFit.mH125.root:#mu#tau_{{h}}:7 output/{OUTPUT_SUFFIX}/et/125/higgsCombine.alpha.MultiDimFit.mH125.root:e#tau_{{h}}:9 output/{OUTPUT_SUFFIX}/em/125/higgsCombine.alpha.MultiDimFit.mH125.root:e#mu:8  --logo 'Work in progress' --logo-sub '' --main-label Expected ".format(
					INPUT_FILE="output/"+args.output_suffix+"/cmb/125/higgsCombine.alpha.MultiDimFit.mH125.root",
					OUTPUT_FILE="output/"+args.output_suffix+"/cmb/125/alpha_channel_comparison",
					OUTPUT_SUFFIX=args.output_suffix
					),
					args.output_dir
			])

			# datacards_module._call_command([
			# 		"python $CMSSW_BASE/src/CombineHarvester/HTTSMCPDecays18/scripts/plot1DScan.py --main={INPUT_FILE} --POI=alpha --output={OUTPUT_FILE} --no-numbers --no-box --x_title='#alpha (#frac{{#pi}}{{2}})' --y-max=3.0".format(
			# 		INPUT_FILE=directory+"higgsCombine.alpha_freezemuF.MultiDimFit.mH125.root",
			# 		OUTPUT_FILE=directory+"alpha_freezemuF"
			# 		),
			# 		args.output_dir
			# ])
			# datacards_module._call_command([
			# 		"python $CMSSW_BASE/src/CombineHarvester/HTTSMCPDecays18/scripts/plotMultiDimFit.py --title-right='35.9 fb^{-1}' --mass=125 --cms-sub='Preliminary' --POI=alpha -o {OUTPUT_FILE}  {INPUT_FILE}".format(
			# 		INPUT_FILE=directory+"higgsCombine.2DScan.MultiDimFit.mH125.root",
			# 		OUTPUT_FILE=directory+"muF_vs_alpha"
			# 		),
			# 		args.output_dir
			# ])

	datacards_poi_ranges = {}
	for datacard, cb in datacards_cbs.iteritems():
		channels = cb.channel_set()
		categories = cb.bin_set()
		if len(channels) == 1:
			if len(categories) == 1:
				datacards_poi_ranges[datacard] = [-1.0, 1.0]
			else:
				datacards_poi_ranges[datacard] = [-1.0, 1.0]
		else:
			if len(categories) == 1:
				datacards_poi_ranges[datacard] = [-1., 1.0]
			else:
				datacards_poi_ranges[datacard] = [-1., 1.]

		# fit diagnostics
	if "prefitpostfitplots_makeplots" in args.steps:
		# https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsWG/HiggsPAGPreapprovalChecks
		# TODO: Somehow I need provide an interface to the old prefitpost fit functions.
		# TODO: I need a function that takes the created workspaces and datacards and wraps them up in the form of datacards_cbs and
		log.info("\n -------------------------------------- Prefit Postfit plots ---------------------------------")
		pprint.pprint( datacards_cbs)
		pprint.pprint( datacards_workspaces_alpha)
		#this is done in CPInitialstatePrefitPostfitPlots.sh
		#for key in datacards_cbs:
		#datacards.combine(datacards_cbs, datacards_workspaces_alpha, datacards_poi_ranges, args.n_processes, "-M FitDiagnostics "+datacards.stable_options+" -n " , higgs_mass="125")

		#datacards_postfit_shapes = datacards.postfit_shapes_fromworkspace(datacards_cbs, datacards_workspaces_alpha, False, args.n_processes, "--sampling" + (" --print" if args.n_processes <= 1 else ""), higgs_mass="125")
		#from IPython import embed; embed()

		datacards_cbs[official_datacard] = tmp_datacard.cp()

		datacards_postfit_shapes_fit_b = {}
		datacards_postfit_shapes_fit_s = {}
		for channel in channel_list:
			datacards_postfit_shapes_fit_b[datacards_path+'htt_'+channel+'_2017_1_13TeV.txt'] = datacards_path+'htt_'+channel+'_2017_postFitShapesFromWorkspace.alpha1_fit_b.root'
			datacards_postfit_shapes_fit_b[datacards_path+'htt_'+channel+'_2017_2_13TeV.txt'] = datacards_path+'htt_'+channel+'_2017_postFitShapesFromWorkspace.alpha2_fit_b.root'
			# datacards_postfit_shapes_fit_b[datacards_path+'htt_'+channel+'_2017_3_13TeV.txt'] = datacards_path+'htt_'+channel+'_2017_postFitShapesFromWorkspace.alpha3_fit_b.root'
			# datacards_postfit_shapes_fit_b[datacards_path+'htt_'+channel+'_2017_4_13TeV.txt'] = datacards_path+'htt_'+channel+'_2017_postFitShapesFromWorkspace.alpha4_fit_b.root'
			# datacards_postfit_shapes_fit_b[datacards_path+'htt_'+channel+'_2017_5_13TeV.txt'] = datacards_path+'htt_'+channel+'_2017_postFitShapesFromWorkspace.alpha5_fit_b.root'
			# datacards_postfit_shapes_fit_b[datacards_path+'htt_'+channel+'_2017_6_13TeV.txt'] = datacards_path+'htt_'+channel+'_2017_postFitShapesFromWorkspace.alpha6_fit_b.root'



			datacards_postfit_shapes_fit_s[datacards_path+'htt_'+channel+'_2017_1_13TeV.txt'] = datacards_path+'htt_'+channel+'_2017_postFitShapesFromWorkspace.alpha1_fit_s.root'
			datacards_postfit_shapes_fit_s[datacards_path+'htt_'+channel+'_2017_2_13TeV.txt'] = datacards_path+'htt_'+channel+'_2017_postFitShapesFromWorkspace.alpha2_fit_s.root'
			# datacards_postfit_shapes_fit_s[datacards_path+'htt_'+channel+'_2017_3_13TeV.txt'] = datacards_path+'htt_'+channel+'_2017_postFitShapesFromWorkspace.alpha3_fit_s.root'
			# datacards_postfit_shapes_fit_s[datacards_path+'htt_'+channel+'_2017_4_13TeV.txt'] = datacards_path+'htt_'+channel+'_2017_postFitShapesFromWorkspace.alpha4_fit_s.root'
			# datacards_postfit_shapes_fit_s[datacards_path+'htt_'+channel+'_2017_5_13TeV.txt'] = datacards_path+'htt_'+channel+'_2017_postFitShapesFromWorkspace.alpha5_fit_s.root'
			# datacards_postfit_shapes_fit_s[datacards_path+'htt_'+channel+'_2017_6_13TeV.txt'] = datacards_path+'htt_'+channel+'_2017_postFitShapesFromWorkspace.alpha6_fit_s.root'


		datacards_postfit_shapes={
			"fit_b" : datacards_postfit_shapes_fit_b,
			"fit_s" : datacards_postfit_shapes_fit_s
			}

		# adapt prefit and postfit plot configs
		backgrounds_to_merge = {
			#"ZLL" : ["ZL", "ZJ"],
			#"TT" : ["TTT", "TTJJ", "TTJ"],
			"EWK" : ["EWKZ", "VVT", "VVJ", "VV", "W", "hww_gg125", "hww_qq125", "ggH_hww125", "qqH_hww125"],
			#"qqh" : ["qqHsm_htt125", "qqH", "WH_htt125", "ZH_htt125", "qqH_htt125"]
		}
		titles = {
			"mt_1" : "#mu#tau_{h} - 0jet",
			"et_1" : "e#tau_{h} - 0jet",
			"em_1" : "e#mu - 0jet",
			"tt_1" : "#tau_{h}#tau_{h} - 0jet",
			"mt_2" : "#mu#tau_{h} - boosted",
			"et_2" : "e#tau_{h} - boosted",
			"em_2" : "e#mu - boosted",
			"tt_2" : "#tau_{h}#tau_{h} - boosted",
			"mt_3" : "#mu#tau_{h} - dijet lowboost failed",
			"et_3" : "e#tau_{h} - dijet lowboost failed",
			"em_3" : "e#mu - dijet lowboost",
			"tt_3" : "#tau_{h}#tau_{h} - dijet lowboost",

			"em_4" : "e#mu - dijet boosted",
			"tt_4" : "#tau_{h}#tau_{h} - dijet boosted",

			#"mt_2017_1" : "#mu#tau_{h} - 0jet",
			#"et_2017_1" : "e#tau_{h} - 0jet",

			#"mt_2017_2" : "#mu#tau_{h} - boosted",
			#"et_2017_2" : "e#tau_{h} - boosted",

			#"mt_2017_3" : "#mu#tau_{h} - dijet lowboost loose mjj",
			#"et_2017_3" : "e#tau_{h} - dijet lowboost loose mjj",

			"mt_4" : "#mu#tau_{h} - dijet boosted failed",
			"et_4" : "e#tau_{h} - dijet boosted failed",

			"mt_5" : "#mu#tau_{h} - dijet lowboosted passed",
			"et_5" : "e#tau_{h} - dijet lowboosted passed",

			"mt_6" : "#mu#tau_{h} - dijet boosted passed",
			"et_6" : "e#tau_{h} - dijet boosted passed"
		}
		ylog_lims = {
			"mt_1" : [1, 10000],
			"et_1" : [1, 10000],
			"em_1" : [1, 10000],
			"tt_1" : [1, 10000],
			"mt_2" : [0.1, 10000],
			"et_2" : [0.1, 10000],
			"em_2" : [0.1, 10000],
			"tt_2" : [0.1, 10000],
			"mt_3" : [0.01, 2000],
			"et_3" : [0.01, 1000],
			"em_3" : [0.01, 200],
			"tt_3" : [0.01, 200],
			"mt_4" : [0.01, 1000],
			"et_4" : [0.01, 500],
			"em_4" : [0.01, 100],
			"tt_4" : [0.01, 100],
			"mt_5" : [0.01, 1000],
			"et_5" : [0.01, 500],
			"em_5" : [0.01, 100],
			"tt_5" : [0.01, 100],
			"mt_6" : [0.01, 1000],
			"et_6" : [0.01, 500],
			"em_6" : [0.01, 100],
			"tt_6" : [0.01, 100]
		}
		if "mela3D" in args.quantity:
			titles = {
				"mt_1" : "#mu#tau_{h} - 0jet",
				"et_1" : "e#tau_{h} - 0jet",
				"em_1" : "e#mu - 0jet",
				"tt_1" : "#tau_{h}#tau_{h} - 0jet",
				"mt_2" : "#mu#tau_{h} - boosted",
				"et_2" : "e#tau_{h} - boosted",
				"em_2" : "e#mu - boosted",
				"tt_2" : "#tau_{h}#tau_{h} - boosted",
				"mt_3" : "#mu#tau_{h} - dijet lowboost",
				"et_3" : "e#tau_{h} - dijet lowboost",
				"em_3" : "e#mu - dijet lowboost",
				"tt_3" : "#tau_{h}#tau_{h} - dijet lowboost",
				"mt_4" : "#mu#tau_{h} - dijet boosted",
				"et_4" : "e#tau_{h} - dijet boosted",
				"em_4" : "e#mu - dijet boosted",
				"tt_4" : "#tau_{h}#tau_{h} - dijet boosted"
			}
			x_tick_labels = {
				"mt_1" : ["0-60","60-65","65-70","70-75","75-80","80-85","85-90","90-95","95-100","100-105","105-110","110-400"] * 3,
				"et_1" : ["0-60","60-65","65-70","70-75","75-80","80-85","85-90","90-95","95-100","100-105","105-110","110-400"] * 3,
				"em_1" : ["0-50","50-55", "55-60","60-65","65-70","70-75","75-80","80-85","85-90","90-95","95-100","100-400"] * 3,
				"mt_2" : ["0-80","80-90","90-100","100-110","110-120","120-130","130-140","140-150","150-160","160-300"] * 6,
				"et_2" : ["0-80","80-90","90-100","100-110","110-120","120-130","130-140","140-150","150-160","160-300"] * 6,
				"em_2" : ["0-80","80-90","90-100","100-110","110-120","120-130","130-140","140-150","150-160","160-300"] * 6,
				"tt_2" : ["0-40","40-60","60-70","70-80","80-90","90-100","100-110","110-120","120-130","130-150","150-200","200-250"] * 4,
				"mt_3" : ["0.00--0.25","0.25--0.5","-0.05--0.75","0.75--1.0"] * 18,
				"et_3" : ["0.00--0.25","0.25--0.5","-0.05--0.75","0.75--1.0"] * 18,
				"em_3" : ["0.00--0.25","0.25--0.5","-0.05--0.75","0.75--1.0"] * 18,
				"tt_3" : ["0.00--0.25","0.25--0.5","-0.05--0.75","0.75--1.0"] * 18,
				"mt_4" : ["0.00--0.25","0.25--0.5","-0.05--0.75","0.75--1.0"] * 18,
				"et_4" : ["0.00--0.25","0.25--0.5","-0.05--0.75","0.75--1.0"] * 18,
				"em_4" : ["0.00--0.25","0.25--0.5","-0.05--0.75","0.75--1.0"] * 18,
				"tt_4" : ["0.00--0.25","0.25--0.5","-0.05--0.75","0.75--1.0"] * 18,
				"mt_5" : ["0.00--0.25","0.25--0.5","-0.05--0.75","0.75--1.0"] * 18,
				"et_5" : ["0.00--0.25","0.25--0.5","-0.05--0.75","0.75--1.0"] * 18,
				"em_5" : ["0.00--0.25","0.25--0.5","-0.05--0.75","0.75--1.0"] * 18,
				"tt_5" : ["0.00--0.25","0.25--0.5","-0.05--0.75","0.75--1.0"] * 18,
				"mt_6" : ["0.00--0.25","0.25--0.5","-0.05--0.75","0.75--1.0"] * 18,
				"et_6" : ["0.00--0.25","0.25--0.5","-0.05--0.75","0.75--1.0"] * 18,
				"em_6" : ["0.00--0.25","0.25--0.5","-0.05--0.75","0.75--1.0"] * 18,
				"tt_6" : ["0.00--0.25","0.25--0.5","-0.05--0.75","0.75--1.0"] * 18
			}
			texts = {
				"mt_1" : ["h^{#pm}", "h^{#pm}#pi^{0}", "h^{#pm}h^{#pm}h^{#mp}"],
				"et_1" : ["h^{#pm}", "h^{#pm}#pi^{0}", "h^{#pm}h^{#pm}h^{#mp}"],
				"em_1" : ["15 < p_{T}(#mu) < 25 GeV", "25 < p_{T}(#mu) < 35 GeV", "p_{T}(#mu) > 35 GeV"],
				"mt_2" : ["0 < p_{T}^{#tau#tau} < 100 GeV", "100 < p_{T}^{#tau#tau} < 150 GeV", "150 < p_{T}^{#tau#tau} < 200 GeV", "200 < p_{T}^{#tau#tau} < 250 GeV", "250 < p_{T}^{#tau#tau} < 300 GeV", "p_{T}^{#tau#tau} > 300 GeV"],
				"et_2" : ["0 < p_{T}^{#tau#tau} < 100 GeV", "100 < p_{T}^{#tau#tau} < 150 GeV", "150 < p_{T}^{#tau#tau} < 200 GeV", "200 < p_{T}^{#tau#tau} < 250 GeV", "250 < p_{T}^{#tau#tau} < 300 GeV", "p_{T}^{#tau#tau} > 300 GeV"],
				"em_2" : ["0 < p_{T}^{#tau#tau} < 100 GeV", "100 < p_{T}^{#tau#tau} < 150 GeV", "150 < p_{T}^{#tau#tau} < 200 GeV", "200 < p_{T}^{#tau#tau} < 250 GeV", "250 < p_{T}^{#tau#tau} < 300 GeV", "p_{T}^{#tau#tau} > 300 GeV"],
				"tt_2" : ["0 < p_{T}^{#tau#tau} < 100 GeV", "100 < p_{T}^{#tau#tau} < 170 GeV", "170 < p_{T}^{#tau#tau} < 300 GeV", "p_{T}^{#tau#tau} > 300 GeV"],
				"mt_3" : ["0 < m_{#tau#tau} < 80 GeV", "80 < m_{#tau#tau} < 100 GeV","100 < m_{#tau#tau} < 115 GeV","115 < m_{#tau#tau} < 130 GeV","130 < m_{#tau#tau} < 150 GeV","m_{#tau#tau} > 150 GeV","D_{CP}< -0.4", "-0.4 < D_{CP} < 0.4","D_{CP} > 0.4","D_{CP}< -0.4", "-0.4 < D_{CP} < 0.4","D_{CP} > 0.4","D_{CP}< -0.4", "-0.4 < D_{CP} < 0.4","D_{CP} > 0.4","D_{CP}< -0.4", "-0.4 < D_{CP} < 0.4","D_{CP} > 0.4","D_{CP}< -0.4", "-0.4 < D_{CP} < 0.4","D_{CP} > 0.4","D_{CP}< -0.4", "-0.4 < D_{CP} < 0.4","D_{CP} > 0.4"],
				"et_3" : ["0 < m_{#tau#tau} < 80 GeV", "80 < m_{#tau#tau} < 100 GeV","100 < m_{#tau#tau} < 115 GeV","115 < m_{#tau#tau} < 130 GeV","130 < m_{#tau#tau} < 150 GeV","m_{#tau#tau} > 150 GeV","D_{CP}< -0.4", "-0.4 < D_{CP} < 0.4","D_{CP} > 0.4","D_{CP}< -0.4", "-0.4 < D_{CP} < 0.4","D_{CP} > 0.4","D_{CP}< -0.4", "-0.4 < D_{CP} < 0.4","D_{CP} > 0.4","D_{CP}< -0.4", "-0.4 < D_{CP} < 0.4","D_{CP} > 0.4","D_{CP}< -0.4", "-0.4 < D_{CP} < 0.4","D_{CP} > 0.4","D_{CP}< -0.4", "-0.4 < D_{CP} < 0.4","D_{CP} > 0.4"],
				"em_3" : ["0 < m_{#tau#tau} < 80 GeV", "80 < m_{#tau#tau} < 100 GeV","100 < m_{#tau#tau} < 115 GeV","115 < m_{#tau#tau} < 130 GeV","130 < m_{#tau#tau} < 150 GeV","m_{#tau#tau} > 150 GeV","D_{CP}< -0.4", "-0.4 < D_{CP} < 0.4","D_{CP} > 0.4","D_{CP}< -0.4", "-0.4 < D_{CP} < 0.4","D_{CP} > 0.4","D_{CP}< -0.4", "-0.4 < D_{CP} < 0.4","D_{CP} > 0.4","D_{CP}< -0.4", "-0.4 < D_{CP} < 0.4","D_{CP} > 0.4","D_{CP}< -0.4", "-0.4 < D_{CP} < 0.4","D_{CP} > 0.4","D_{CP}< -0.4", "-0.4 < D_{CP} < 0.4","D_{CP} > 0.4"],
				"tt_3" : ["0 < m_{#tau#tau} < 80 GeV", "80 < m_{#tau#tau} < 100 GeV","100 < m_{#tau#tau} < 115 GeV","115 < m_{#tau#tau} < 130 GeV","130 < m_{#tau#tau} < 150 GeV","m_{#tau#tau} > 150 GeV","D_{CP}< -0.4", "-0.4 < D_{CP} < 0.4","D_{CP} > 0.4","D_{CP}< -0.4", "-0.4 < D_{CP} < 0.4","D_{CP} > 0.4","D_{CP}< -0.4", "-0.4 < D_{CP} < 0.4","D_{CP} > 0.4","D_{CP}< -0.4", "-0.4 < D_{CP} < 0.4","D_{CP} > 0.4","D_{CP}< -0.4", "-0.4 < D_{CP} < 0.4","D_{CP} > 0.4","D_{CP}< -0.4", "-0.4 < D_{CP} < 0.4","D_{CP} > 0.4"],
				"mt_4" : ["0 < m_{#tau#tau} < 80 GeV", "80 < m_{#tau#tau} < 100 GeV","100 < m_{#tau#tau} < 115 GeV","115 < m_{#tau#tau} < 130 GeV","130 < m_{#tau#tau} < 150 GeV","m_{#tau#tau} > 150 GeV","D_{CP}< -0.4", "-0.4 < D_{CP} < 0.4","D_{CP} > 0.4","D_{CP}< -0.4", "-0.4 < D_{CP} < 0.4","D_{CP} > 0.4","D_{CP}< -0.4", "-0.4 < D_{CP} < 0.4","D_{CP} > 0.4","D_{CP}< -0.4", "-0.4 < D_{CP} < 0.4","D_{CP} > 0.4","D_{CP}< -0.4", "-0.4 < D_{CP} < 0.4","D_{CP} > 0.4","D_{CP}< -0.4", "-0.4 < D_{CP} < 0.4","D_{CP} > 0.4"],
				"et_4" : ["0 < m_{#tau#tau} < 80 GeV", "80 < m_{#tau#tau} < 100 GeV","100 < m_{#tau#tau} < 115 GeV","115 < m_{#tau#tau} < 130 GeV","130 < m_{#tau#tau} < 150 GeV","m_{#tau#tau} > 150 GeV","D_{CP}< -0.4", "-0.4 < D_{CP} < 0.4","D_{CP} > 0.4","D_{CP}< -0.4", "-0.4 < D_{CP} < 0.4","D_{CP} > 0.4","D_{CP}< -0.4", "-0.4 < D_{CP} < 0.4","D_{CP} > 0.4","D_{CP}< -0.4", "-0.4 < D_{CP} < 0.4","D_{CP} > 0.4","D_{CP}< -0.4", "-0.4 < D_{CP} < 0.4","D_{CP} > 0.4","D_{CP}< -0.4", "-0.4 < D_{CP} < 0.4","D_{CP} > 0.4"],
				"em_4" : ["0 < m_{#tau#tau} < 80 GeV", "80 < m_{#tau#tau} < 100 GeV","100 < m_{#tau#tau} < 115 GeV","115 < m_{#tau#tau} < 130 GeV","130 < m_{#tau#tau} < 150 GeV","m_{#tau#tau} > 150 GeV","D_{CP}< -0.4", "-0.4 < D_{CP} < 0.4","D_{CP} > 0.4","D_{CP}< -0.4", "-0.4 < D_{CP} < 0.4","D_{CP} > 0.4","D_{CP}< -0.4", "-0.4 < D_{CP} < 0.4","D_{CP} > 0.4","D_{CP}< -0.4", "-0.4 < D_{CP} < 0.4","D_{CP} > 0.4","D_{CP}< -0.4", "-0.4 < D_{CP} < 0.4","D_{CP} > 0.4","D_{CP}< -0.4", "-0.4 < D_{CP} < 0.4","D_{CP} > 0.4"],
				"tt_4" : ["0 < m_{#tau#tau} < 80 GeV", "80 < m_{#tau#tau} < 100 GeV","100 < m_{#tau#tau} < 115 GeV","115 < m_{#tau#tau} < 130 GeV","130 < m_{#tau#tau} < 150 GeV","m_{#tau#tau} > 150 GeV","D_{CP}< -0.4", "-0.4 < D_{CP} < 0.4","D_{CP} > 0.4","D_{CP}< -0.4", "-0.4 < D_{CP} < 0.4","D_{CP} > 0.4","D_{CP}< -0.4", "-0.4 < D_{CP} < 0.4","D_{CP} > 0.4","D_{CP}< -0.4", "-0.4 < D_{CP} < 0.4","D_{CP} > 0.4","D_{CP}< -0.4", "-0.4 < D_{CP} < 0.4","D_{CP} > 0.4","D_{CP}< -0.4", "-0.4 < D_{CP} < 0.4","D_{CP} > 0.4"]
			}
			sub_texts = {
				"mt_1" : ["h^{#pm}", "h^{#pm}#pi^{0}", "h^{#pm}h^{#pm}h^{#mp}"],
				"et_1" : ["h^{#pm}", "h^{#pm}#pi^{0}", "h^{#pm}h^{#pm}h^{#mp}"],
				"em_1" : ["15 < p_{T}(#mu) < 25 GeV", "25 < p_{T}(#mu) < 35 GeV", "p_{T}(#mu) > 35 GeV"],
				"mt_2" : ["0 < p_{T}^{#tau#tau} < 100 GeV", "100 < p_{T}^{#tau#tau} < 150 GeV", "150 < p_{T}^{#tau#tau} < 200 GeV", "200 < p_{T}^{#tau#tau} < 250 GeV", "250 < p_{T}^{#tau#tau} < 300 GeV", "p_{T}^{#tau#tau} > 300 GeV"],
				"et_2" : ["0 < p_{T}^{#tau#tau} < 100 GeV", "100 < p_{T}^{#tau#tau} < 150 GeV", "150 < p_{T}^{#tau#tau} < 200 GeV", "200 < p_{T}^{#tau#tau} < 250 GeV", "250 < p_{T}^{#tau#tau} < 300 GeV", "p_{T}^{#tau#tau} > 300 GeV"],
				"em_2" : ["0 < p_{T}^{#tau#tau} < 100 GeV", "100 < p_{T}^{#tau#tau} < 150 GeV", "150 < p_{T}^{#tau#tau} < 200 GeV", "200 < p_{T}^{#tau#tau} < 250 GeV", "250 < p_{T}^{#tau#tau} < 300 GeV", "p_{T}^{#tau#tau} > 300 GeV"],
				"tt_2" : ["0 < p_{T}^{#tau#tau} < 100 GeV", "100 < p_{T}^{#tau#tau} < 170 GeV", "170 < p_{T}^{#tau#tau} < 300 GeV", "p_{T}^{#tau#tau} > 300 GeV"],
				"mt_3" : ["D_{CP}< -0.4", "-0.4 < D_{CP} < 0.4","D_{CP} > 0.4"]*6,
				"et_3" : ["D_{CP}< -0.4", "-0.4 < D_{CP} < 0.4","D_{CP} > 0.4"]*6,
				"em_3" : ["D_{CP}< -0.4", "-0.4 < D_{CP} < 0.4","D_{CP} > 0.4"]*6,
				"tt_3" : ["D_{CP}< -0.4", "-0.4 < D_{CP} < 0.4","D_{CP} > 0.4"]*6,
				"mt_4" : ["D_{CP}< -0.4", "-0.4 < D_{CP} < 0.4","D_{CP} > 0.4"]*6,
				"et_4" : ["D_{CP}< -0.4", "-0.4 < D_{CP} < 0.4","D_{CP} > 0.4"]*6,
				"em_4" : ["D_{CP}< -0.4", "-0.4 < D_{CP} < 0.4","D_{CP} > 0.4"]*6,
				"tt_4" : ["D_{CP}< -0.4", "-0.4 < D_{CP} < 0.4","D_{CP} > 0.4"]*6
			}
			sub_texts_x = {
				"mt_1" : [0.14, 0.4, 0.67],
				"et_1" : [0.14, 0.4, 0.67],
				"em_1" : [0.2, 0.46, 0.705],
				"mt_2" : [0.17, 0.2975, 0.43, 0.56, 0.6925, 0.81],
				"et_2" : [0.17, 0.2975, 0.43, 0.56, 0.6925, 0.81],
				"em_2" : [0.17, 0.2975, 0.43, 0.56, 0.6925, 0.81],
				"tt_2" : [0.17, 0.2975, 0.43, 0.56, 0.6925, 0.81],
				"mt_3" : [0.13, 0.17, 0.21, 0.26, 0.30, 0.34, 0.4, 0.44, 0.48, 0.52, 0.56, 0.6, 0.65, 0.69, 0.73, 0.78, 0.82, 0.86],
				"et_3" : [0.13, 0.17, 0.21, 0.26, 0.30, 0.34, 0.4, 0.44, 0.48, 0.52, 0.56, 0.6, 0.65, 0.69, 0.73, 0.78, 0.82, 0.86],
				"em_3" : [0.13, 0.17, 0.21, 0.26, 0.30, 0.34, 0.4, 0.44, 0.48, 0.52, 0.56, 0.6, 0.65, 0.69, 0.73, 0.78, 0.82, 0.86],
				"tt_3" : [0.13, 0.17, 0.21, 0.26, 0.30, 0.34, 0.4, 0.44, 0.48, 0.52, 0.56, 0.6, 0.65, 0.69, 0.73, 0.78, 0.82, 0.86],
				"mt_4" : [0.13, 0.17, 0.21, 0.26, 0.30, 0.34, 0.4, 0.44, 0.48, 0.52, 0.56, 0.6, 0.65, 0.69, 0.73, 0.78, 0.82, 0.86],
				"et_4" : [0.13, 0.17, 0.21, 0.26, 0.30, 0.34, 0.4, 0.44, 0.48, 0.52, 0.56, 0.6, 0.65, 0.69, 0.73, 0.78, 0.82, 0.86],
				"em_4" : [0.13, 0.17, 0.21, 0.26, 0.30, 0.34, 0.4, 0.44, 0.48, 0.52, 0.56, 0.6, 0.65, 0.69, 0.73, 0.78, 0.82, 0.86],
				"tt_4" : [0.13, 0.17, 0.21, 0.26, 0.30, 0.34, 0.4, 0.44, 0.48, 0.52, 0.56, 0.6, 0.65, 0.69, 0.73, 0.78, 0.82, 0.86]
			}
			texts_x = {
				"mt_1" : [0.14, 0.4, 0.67],
				"et_1" : [0.14, 0.4, 0.67],
				"em_1" : [0.2, 0.46, 0.705],
				"mt_2" : [0.17, 0.2975, 0.43, 0.56, 0.6925, 0.81],
				"et_2" : [0.17, 0.2975, 0.43, 0.56, 0.6925, 0.81],
				"em_2" : [0.17, 0.2975, 0.43, 0.56, 0.6925, 0.81],
				"tt_2" : [0.17, 0.2975, 0.43, 0.56, 0.6925, 0.81],
				"mt_3" : [0.17, 0.30, 0.44, 0.56, 0.69, 0.82, 0.13, 0.17, 0.21, 0.26, 0.30, 0.34, 0.4, 0.44, 0.48, 0.52, 0.56, 0.6, 0.65, 0.69, 0.73, 0.78, 0.82, 0.86],
				"et_3" : [0.17, 0.30, 0.44, 0.56, 0.69, 0.82, 0.13, 0.17, 0.21, 0.26, 0.30, 0.34, 0.4, 0.44, 0.48, 0.52, 0.56, 0.6, 0.65, 0.69, 0.73, 0.78, 0.82, 0.86],
				"em_3" : [0.17, 0.30, 0.44, 0.56, 0.69, 0.82, 0.13, 0.17, 0.21, 0.26, 0.30, 0.34, 0.4, 0.44, 0.48, 0.52, 0.56, 0.6, 0.65, 0.69, 0.73, 0.78, 0.82, 0.86],
				"tt_3" : [0.17, 0.30, 0.44, 0.56, 0.69, 0.82, 0.13, 0.17, 0.21, 0.26, 0.30, 0.34, 0.4, 0.44, 0.48, 0.52, 0.56, 0.6, 0.65, 0.69, 0.73, 0.78, 0.82, 0.86],
				"mt_4" : [0.17, 0.30, 0.44, 0.56, 0.69, 0.82, 0.13, 0.17, 0.21, 0.26, 0.30, 0.34, 0.4, 0.44, 0.48, 0.52, 0.56, 0.6, 0.65, 0.69, 0.73, 0.78, 0.82, 0.86],
				"et_4" : [0.17, 0.30, 0.44, 0.56, 0.69, 0.82, 0.13, 0.17, 0.21, 0.26, 0.30, 0.34, 0.4, 0.44, 0.48, 0.52, 0.56, 0.6, 0.65, 0.69, 0.73, 0.78, 0.82, 0.86],
				"em_4" : [0.17, 0.30, 0.44, 0.56, 0.69, 0.82, 0.13, 0.17, 0.21, 0.26, 0.30, 0.34, 0.4, 0.44, 0.48, 0.52, 0.56, 0.6, 0.65, 0.69, 0.73, 0.78, 0.82, 0.86],
				"tt_4" : [0.17, 0.30, 0.44, 0.56, 0.69, 0.82, 0.13, 0.17, 0.21, 0.26, 0.30, 0.34, 0.4, 0.44, 0.48, 0.52, 0.56, 0.6, 0.65, 0.69, 0.73, 0.78, 0.82, 0.86]
			}
			texts_y = {
				"mt_1" : [0.8],
				"et_1" : [0.8],
				"em_1" : [0.8],
				"mt_2" : [0.8],
				"et_2" : [0.8],
				"em_2" : [0.8],
				"tt_2" : [0.8],
				"mt_3" : [0.8]*6+[0.75, 0.7, 0.75]*6,
				"et_3" : [0.8]*6+[0.75, 0.7, 0.75]*6,
				"em_3" : [0.8]*6+[0.75, 0.7, 0.75]*6,
				"tt_3" : [0.8]*6+[0.75, 0.7, 0.75]*6,
				"mt_4" : [0.8]*6+[0.75, 0.7, 0.75]*6,
				"et_4" : [0.8]*6+[0.75, 0.7, 0.75]*6,
				"em_4" : [0.8]*6+[0.75, 0.7, 0.75]*6,
				"tt_4" : [0.8]*6+[0.75, 0.7, 0.75]*6
			}
			vertical_lines = {
				"mt_1" : [12, 24],
				"et_1" : [12, 24],
				"em_1" : [12, 24],
				"mt_2" : [10, 20, 30, 40, 50],
				"et_2" : [10, 20, 30, 40, 50],
				"em_2" : [10, 20, 30, 40, 50],
				"tt_2" : [12, 24, 36, 48, 60],
				"mt_3" : [4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48, 52, 56, 60],
				"et_3" : [4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48, 52, 56, 60],
				"em_3" : [4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48, 52, 56, 60],
				"tt_3" : [4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48, 52, 56, 60],
				"mt_4" : [4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48, 52, 56, 60],
				"et_4" : [4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48, 52, 56, 60],
				"em_4" : [4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48, 52, 56, 60],
				"tt_4" : [4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48, 52, 56, 60]
			}

		if "CP1" in args.quantity or "CP2" in args.quantity:
			x_tick_labels = {
				"mt_1" : ["0-60","60-65","65-70","70-75","75-80","80-85","85-90","90-95","95-100","100-105","105-110","110-400"] * 3,
				"et_1" : ["0-60","60-65","65-70","70-75","75-80","80-85","85-90","90-95","95-100","100-105","105-110","110-400"] * 3,
				"em_1" : ["0-50","50-55", "55-60","60-65","65-70","70-75","75-80","80-85","85-90","90-95","95-100","100-400"] * 3,
				"mt_2" : ["0-100","100-150","150-200","200-250","250-300", ">300"] * 10,
				"et_2" : ["0-100","100-150","150-200","200-250","250-300", ">300"] * 10,
				"em_2" : ["0-80","80-90","90-100","100-110","110-120","120-130","130-140","140-150","150-160","160-300"] * 6,
				"tt_2" : ["0-40","40-60","60-70","70-80","80-90","90-100","100-110","110-120","120-130","130-150","150-200","200-250"] * 4,
				"mt_3" : ["-3.15--2.63","-2.63--2.1","-2.1--1.58","-1.58--1.05","-1.05--0.53","-0.53-0", "0-0.53","0.53-1.05", "1.05-1.58", "1.58-2.1", "2.1-2.63", "2.63-3.15"] * 6,
				"et_3" : ["-3.15--2.63","-2.63--2.1","-2.1--1.58","-1.58--1.05","-1.05--0.53","-0.53-0", "0-0.53","0.53-1.05", "1.05-1.58", "1.58-2.1", "2.1-2.63", "2.63-3.15"] * 6,
				"em_3" : ["-3.15--2.63","-2.63--2.1","-2.1--1.58","-1.58--1.05","-1.05--0.53","-0.53-0", "0-0.53","0.53-1.05", "1.05-1.58", "1.58-2.1", "2.1-2.63", "2.63-3.15"] * 6,
				"tt_3" : ["-3.15--2.63","-2.63--2.1","-2.1--1.58","-1.58--1.05","-1.05--0.53","-0.53-0", "0-0.53","0.53-1.05", "1.05-1.58", "1.58-2.1", "2.1-2.63", "2.63-3.15"] * 6,
				"mt_4" : ["-3.15--2.63","-2.63--2.1","-2.1--1.58","-1.58--1.05","-1.05--0.53","-0.53-0", "0-0.53","0.53-1.05", "1.05-1.58", "1.58-2.1", "2.1-2.63", "2.63-3.15"] * 6,
				"et_4" : ["-3.15--2.63","-2.63--2.1","-2.1--1.58","-1.58--1.05","-1.05--0.53","-0.53-0", "0-0.53","0.53-1.05", "1.05-1.58", "1.58-2.1", "2.1-2.63", "2.63-3.15"] * 5,
				"em_4" : ["-3.15--2.63","-2.63--2.1","-2.1--1.58","-1.58--1.05","-1.05--0.53","-0.53-0", "0-0.53","0.53-1.05", "1.05-1.58", "1.58-2.1", "2.1-2.63", "2.63-3.15"] * 6,
				"tt_4" : ["-3.15--2.63","-2.63--2.1","-2.1--1.58","-1.58--1.05","-1.05--0.53","-0.53-0", "0-0.53","0.53-1.05", "1.05-1.58", "1.58-2.1", "2.1-2.63", "2.63-3.15"] * 6,

				"mt_5" : ["-1.6","0","1.6","3.15"] * 12,
				"et_5" : ["-1.6","0","1.6","3.15"] * 10,
				"mt_6" : ["-1.6","0","1.6","3.15"] * 12,
				"et_6" : ["-1.6","0","1.6","3.15"] * 10,
			}

			x_ticks = {
				"mt_5" : [0.0, 4.0, 7.0, 10.0, 13.0, 16.0, 19.0, 22.0, 25.0, 28.0, 31.0, 34.0, 37.0, 40.0, 43.0, 46.0, 49.0, 52.0, 55.0, 58.0, 61.0, 64.0, 67.0, 70.0, 73.0, 76.0, 79.0, 82.0, 85.0, 88.0, 91.0, 94.0, 97.0, 100.0, 103.0, 106.0, 109.0, 112.0, 115.0, 118.0, 121.0, 124.0, 127.0, 130.0, 133.0, 136.0, 139.0, 142.0, 144.0],
				"mt_6" : [0.0, 4.0, 7.0, 10.0, 13.0, 16.0, 19.0, 22.0, 25.0, 28.0, 31.0, 34.0, 37.0, 40.0, 43.0, 46.0, 49.0, 52.0, 55.0, 58.0, 61.0, 64.0, 67.0, 70.0, 73.0, 76.0, 79.0, 82.0, 85.0, 88.0, 91.0, 94.0, 97.0, 100.0, 103.0, 106.0, 109.0, 112.0, 115.0, 118.0, 121.0, 124.0, 127.0, 130.0, 133.0, 136.0, 139.0, 142.0, 144.0],
				"et_5" : [0.0, 4.0, 7.0, 10.0, 13.0, 16.0, 19.0, 22.0, 25.0, 28.0, 31.0, 34.0, 37.0, 40.0, 43.0, 46.0, 49.0, 52.0, 55.0, 58.0, 61.0, 64.0, 67.0, 70.0, 73.0, 76.0, 79.0, 82.0, 85.0, 88.0, 91.0, 94.0, 97.0, 100.0, 103.0, 106.0, 109.0, 112.0, 115.0, 118.0, 120],
				"et_6" : [0.0, 4.0, 7.0, 10.0, 13.0, 16.0, 19.0, 22.0, 25.0, 28.0, 31.0, 34.0, 37.0, 40.0, 43.0, 46.0, 49.0, 52.0, 55.0, 58.0, 61.0, 64.0, 67.0, 70.0, 73.0, 76.0, 79.0, 82.0, 85.0, 88.0, 91.0, 94.0, 97.0, 100.0, 103.0, 106.0, 109.0, 112.0, 115.0, 118.0, 120]
			}



			#"-3.15--2.63","-2.63--2.1","-2.1--1.58","-1.58--1.05","-1.05--0.53","-0.53-0", "0-0.53","0.53-1.05", "1.05-1.58", "1.58-2.1", "2.1-2.63", "2.63-3.15"


			texts = {
				"mt_1" : [""],
				"et_1" : [""],
				"em_1" : [""],
				"mt_2" : [""],
				"et_2" : [""],
				"em_2" : ["0 < p_{T}^{#tau#tau} < 100 GeV", "100 < p_{T}^{#tau#tau} < 150 GeV", "150 < p_{T}^{#tau#tau} < 200 GeV", "200 < p_{T}^{#tau#tau} < 250 GeV", "250 < p_{T}^{#tau#tau} < 300 GeV", "p_{T}^{#tau#tau} > 300 GeV"],
				"tt_2" : ["0 < p_{T}^{#tau#tau} < 100 GeV", "100 < p_{T}^{#tau#tau} < 170 GeV", "170 < p_{T}^{#tau#tau} < 300 GeV", "p_{T}^{#tau#tau} > 300 GeV"],

				"mt_3" : ["50 < m_{#tau#tau} < 80 GeV", "80 < m_{#tau#tau} < 100 GeV","100 < m_{#tau#tau} < 115 GeV","115 < m_{#tau#tau} < 130 GeV","130 < m_{#tau#tau} < 150 GeV","150 GeV < m_{#tau#tau} < 200 GeV"],
				"et_3" : ["50 < m_{#tau#tau} < 80 GeV", "80 < m_{#tau#tau} < 100 GeV","100 < m_{#tau#tau} < 115 GeV","115 < m_{#tau#tau} < 130 GeV", "130 < m_{#tau#tau} < 150 GeV","150 GeV < m_{#tau#tau} < 200 GeV"],
				"em_3" : ["0 < m_{#tau#tau} < 80 GeV", "80 < m_{#tau#tau} < 100 GeV","100 < m_{#tau#tau} < 115 GeV","115 < m_{#tau#tau} < 130 GeV","130 < m_{#tau#tau} < 150 GeV","m_{#tau#tau} > 150 GeV"],
				"tt_3" : ["0 < m_{#tau#tau} < 80 GeV", "80 < m_{#tau#tau} < 100 GeV","100 < m_{#tau#tau} < 115 GeV","115 < m_{#tau#tau} < 130 GeV","130 < m_{#tau#tau} < 150 GeV","m_{#tau#tau} > 150 GeV"],

				"mt_4" : ["50 < m_{#tau#tau} < 80 GeV", "80 < m_{#tau#tau} < 100 GeV","100 < m_{#tau#tau} < 115 GeV","115 < m_{#tau#tau} < 130 GeV","130 < m_{#tau#tau} < 150 GeV","150 GeV < m_{#tau#tau} < 200 GeV"],
				"et_4" : ["50 < m_{#tau#tau} < 80 GeV", "80 < m_{#tau#tau} < 100 GeV","100 < m_{#tau#tau} < 115 GeV","115 < m_{#tau#tau} < 150 GeV","150 GeV < m_{#tau#tau} < 200 GeV"],
				"em_4" : ["0 < m_{#tau#tau} < 80 GeV", "80 < m_{#tau#tau} < 100 GeV","100 < m_{#tau#tau} < 115 GeV","115 < m_{#tau#tau} < 130 GeV","130 < m_{#tau#tau} < 150 GeV","150 GeV < m_{#tau#tau} < 200 GeV"],
				"tt_4" : ["0 < m_{#tau#tau} < 80 GeV", "80 < m_{#tau#tau} < 100 GeV","100 < m_{#tau#tau} < 115 GeV","115 < m_{#tau#tau} < 130 GeV","130 < m_{#tau#tau} < 150 GeV","m_{#tau#tau} > 150 GeV"],

				"mt_5" : ["50 < m_{#tau#tau} < 80 GeV", "80 < m_{#tau#tau} < 100 GeV","100 < m_{#tau#tau} < 115 GeV","115 < m_{#tau#tau} < 130 GeV","130 < m_{#tau#tau} < 150 GeV","150 GeV < m_{#tau#tau} < 200 GeV"],
				"et_5" : ["50 < m_{#tau#tau} < 80 GeV", "80 < m_{#tau#tau} < 100 GeV","100 < m_{#tau#tau} < 115 GeV", "115 < m_{#tau#tau} < 150 GeV","150 GeV < m_{#tau#tau} < 200 GeV"],

				"mt_6" : ["50 < m_{#tau#tau} < 80 GeV", "80 < m_{#tau#tau} < 100 GeV","100 < m_{#tau#tau} < 115 GeV","115 < m_{#tau#tau} < 130 GeV","130 < m_{#tau#tau} < 150 GeV","150 GeV < m_{#tau#tau} < 200 GeV"],
				"et_6" : ["50 < m_{#tau#tau} < 80 GeV", "80 < m_{#tau#tau} < 100 GeV","100 < m_{#tau#tau} < 115 GeV", "115 < m_{#tau#tau} < 150 GeV","150 GeV < m_{#tau#tau} < 200 GeV"]
			}
			texts_x = {
				"mt_1" : [0.14],
				"et_1" : [0.14],
				"em_1" : [0.2],
				"mt_2" : [0.17, 0.2975, 0.43, 0.56, 0.6925, 0.81],
				"et_2" : [0.17, 0.2975, 0.43, 0.56, 0.6925, 0.81],
				"em_2" : [0.17, 0.2975, 0.43, 0.56, 0.6925, 0.81],
				"tt_2" : [0.17, 0.2975, 0.43, 0.56, 0.6925, 0.81],
				"mt_3" : [0.17, 0.30, 0.44, 0.56, 0.69, 0.82],
				"et_3" : [0.17, 0.30, 0.44, 0.56, 0.69, 0.82],
				"em_3" : [0.17, 0.30, 0.44, 0.56, 0.69, 0.82],
				"tt_3" : [0.17, 0.30, 0.44, 0.56, 0.69, 0.82],
				"mt_4" : [0.17, 0.30, 0.44, 0.56, 0.69, 0.82],
				"et_4" : [0.18, 0.34, 0.5, 0.66, 0.81],
				"em_4" : [0.17, 0.30, 0.44, 0.56, 0.69, 0.82],
				"tt_4" : [0.17, 0.30, 0.44, 0.56, 0.69, 0.82],

				"mt_5" : [0.17, 0.30, 0.44, 0.56, 0.69, 0.82],
				"et_5" : [0.18, 0.34, 0.5, 0.66, 0.81],
				"mt_6" : [0.17, 0.30, 0.44, 0.56, 0.69, 0.82],
				"et_6" : [0.18, 0.34, 0.5, 0.66, 0.81]
			}
			texts_y = {
				"mt_1" : [0.8],
				"et_1" : [0.8],
				"em_1" : [0.8],
				"mt_2" : [0.8],
				"et_2" : [0.8],
				"em_2" : [0.8],
				"tt_2" : [0.8],
				"mt_3" : [0.8],
				"et_3" : [0.8],
				"em_3" : [0.8],
				"tt_3" : [0.8],
				"mt_4" : [0.8],
				"et_4" : [0.8],
				"em_4" : [0.8],
				"tt_4" : [0.8],
				"mt_5" : [0.8],
				"et_5" : [0.8],
				"em_5" : [0.8],
				"tt_5" : [0.8],
				"mt_6" : [0.8],
				"et_6" : [0.8],
				"em_6" : [0.8],
				"tt_6" : [0.8]
			}

			vertical_lines_x = {
				"mt_1" : ["12 12", "24 24"],
				"et_1" : ["12 12", "24 24"],
				"em_1" : ["12 12", "24 24"],
				"mt_2" : ["6 6", "12 12", "18 18", "24 24", "30 30", "36 36", "42 42", "48 48", "54 54"],
				"et_2" : ["6 6", "12 12", "18 18", "24 24", "30 30", "36 36", "42 42", "48 48", "54 54"],
				"em_2" : ["10 10", "20 20", "30 30", "40 40", "50 50"],
				"tt_2" : ["12 12", "24 24", "36 36", "48 48", "60 60"],
				"mt_3" : ["12 12", "24 24", "36 36", "48 48", "60 60"],
				"et_3" : ["12 12", "24 24", "36 36", "48 48", "60 60"],
				"em_3" : ["12 12", "24 24", "36 36", "48 48", "60 60"],
				"tt_3" : ["12 12", "24 24", "36 36", "48 48", "60 60"],
				"mt_4" : ["12 12", "24 24", "36 36", "48 48", "60 60"],
				"et_4" : ["12 12", "24 24", "36 36", "48 48", "60 60"],
				"em_4" : ["12 12", "24 24", "36 36", "48 48", "60 60"],
				"tt_4" : ["12 12", "24 24", "36 36", "48 48", "60 60"],
				"mt_5" : ["12 12", "24 24", "36 36", "48 48", "60 60","72 72","84 84","96 96","108 108","120 120","132 132","144 144"],
				"mt_6" : ["12 12", "24 24", "36 36", "48 48", "60 60","72 72","84 84","96 96","108 108","120 120","132 132","144 144"],
				"et_5" : ["12 12", "24 24", "36 36", "48 48", "60 60","72 72","84 84","96 96","108 108","120 120"],
				"et_6" : ["12 12", "24 24", "36 36", "48 48", "60 60","72 72","84 84","96 96","108 108","120 120"]
			}
		if "recoPhiStarCPCombMergedHelrPVBS" in args.quantity:
			x_tick_labels = {
				"mt_1" : ["0-60","60-65","65-70","70-75","75-80","80-85","85-90","90-95","95-100","100-105","105-110","110-400"] * 3,
				"et_1" : ["0-60","60-65","65-70","70-75","75-80","80-85","85-90","90-95","95-100","100-105","105-110","110-400"] * 3,
				"em_1" : ["0-50","50-55", "55-60","60-65","65-70","70-75","75-80","80-85","85-90","90-95","95-100","100-400"] * 3,
				"mt_2" : ["0-100","100-150","150-200","200-250","250-300", ">300"] * 10,
				"et_2" : ["0-100","100-150","150-200","200-250","250-300", ">300"] * 10,
				"em_2" : ["0-80","80-90","90-100","100-110","110-120","120-130","130-140","140-150","150-160","160-300"] * 6,
				"tt_2" : ["0-40","40-60","60-70","70-80","80-90","90-100","100-110","110-120","120-130","130-150","150-200","200-250"] * 4,
				"mt_3" : ["-3.15--2.63","-2.63--2.1","-2.1--1.58","-1.58--1.05","-1.05--0.53","-0.53-0", "0-0.53","0.53-1.05", "1.05-1.58", "1.58-2.1", "2.1-2.63", "2.63-3.15"] * 6,
				"et_3" : ["-3.15--2.63","-2.63--2.1","-2.1--1.58","-1.58--1.05","-1.05--0.53","-0.53-0", "0-0.53","0.53-1.05", "1.05-1.58", "1.58-2.1", "2.1-2.63", "2.63-3.15"] * 6,
				"em_3" : ["-3.15--2.63","-2.63--2.1","-2.1--1.58","-1.58--1.05","-1.05--0.53","-0.53-0", "0-0.53","0.53-1.05", "1.05-1.58", "1.58-2.1", "2.1-2.63", "2.63-3.15"] * 6,
				"tt_3" : ["-3.15--2.63","-2.63--2.1","-2.1--1.58","-1.58--1.05","-1.05--0.53","-0.53-0", "0-0.53","0.53-1.05", "1.05-1.58", "1.58-2.1", "2.1-2.63", "2.63-3.15"] * 6,
				"mt_4" : ["-3.15--2.63","-2.63--2.1","-2.1--1.58","-1.58--1.05","-1.05--0.53","-0.53-0", "0-0.53","0.53-1.05", "1.05-1.58", "1.58-2.1", "2.1-2.63", "2.63-3.15"] * 6,
				"et_4" : ["-3.15--2.63","-2.63--2.1","-2.1--1.58","-1.58--1.05","-1.05--0.53","-0.53-0", "0-0.53","0.53-1.05", "1.05-1.58", "1.58-2.1", "2.1-2.63", "2.63-3.15"] * 5,
				"em_4" : ["-3.15--2.63","-2.63--2.1","-2.1--1.58","-1.58--1.05","-1.05--0.53","-0.53-0", "0-0.53","0.53-1.05", "1.05-1.58", "1.58-2.1", "2.1-2.63", "2.63-3.15"] * 6,
				"tt_4" : ["-3.15--2.63","-2.63--2.1","-2.1--1.58","-1.58--1.05","-1.05--0.53","-0.53-0", "0-0.53","0.53-1.05", "1.05-1.58", "1.58-2.1", "2.1-2.63", "2.63-3.15"] * 6,

				"mt_5" : ["-1.6","0","1.6","3.15"] * 12,
				"et_5" : ["-1.6","0","1.6","3.15"] * 10,
				"mt_6" : ["-1.6","0","1.6","3.15"] * 12,
				"et_6" : ["-1.6","0","1.6","3.15"] * 10,
			}

			x_ticks = {
				"mt_5" : [0.0, 4.0, 7.0, 10.0, 13.0, 16.0, 19.0, 22.0, 25.0, 28.0, 31.0, 34.0, 37.0, 40.0, 43.0, 46.0, 49.0, 52.0, 55.0, 58.0, 61.0, 64.0, 67.0, 70.0, 73.0, 76.0, 79.0, 82.0, 85.0, 88.0, 91.0, 94.0, 97.0, 100.0, 103.0, 106.0, 109.0, 112.0, 115.0, 118.0, 121.0, 124.0, 127.0, 130.0, 133.0, 136.0, 139.0, 142.0, 144.0],
				"mt_6" : [0.0, 4.0, 7.0, 10.0, 13.0, 16.0, 19.0, 22.0, 25.0, 28.0, 31.0, 34.0, 37.0, 40.0, 43.0, 46.0, 49.0, 52.0, 55.0, 58.0, 61.0, 64.0, 67.0, 70.0, 73.0, 76.0, 79.0, 82.0, 85.0, 88.0, 91.0, 94.0, 97.0, 100.0, 103.0, 106.0, 109.0, 112.0, 115.0, 118.0, 121.0, 124.0, 127.0, 130.0, 133.0, 136.0, 139.0, 142.0, 144.0],
				"et_5" : [0.0, 4.0, 7.0, 10.0, 13.0, 16.0, 19.0, 22.0, 25.0, 28.0, 31.0, 34.0, 37.0, 40.0, 43.0, 46.0, 49.0, 52.0, 55.0, 58.0, 61.0, 64.0, 67.0, 70.0, 73.0, 76.0, 79.0, 82.0, 85.0, 88.0, 91.0, 94.0, 97.0, 100.0, 103.0, 106.0, 109.0, 112.0, 115.0, 118.0, 120],
				"et_6" : [0.0, 4.0, 7.0, 10.0, 13.0, 16.0, 19.0, 22.0, 25.0, 28.0, 31.0, 34.0, 37.0, 40.0, 43.0, 46.0, 49.0, 52.0, 55.0, 58.0, 61.0, 64.0, 67.0, 70.0, 73.0, 76.0, 79.0, 82.0, 85.0, 88.0, 91.0, 94.0, 97.0, 100.0, 103.0, 106.0, 109.0, 112.0, 115.0, 118.0, 120]
			}



			#"-3.15--2.63","-2.63--2.1","-2.1--1.58","-1.58--1.05","-1.05--0.53","-0.53-0", "0-0.53","0.53-1.05", "1.05-1.58", "1.58-2.1", "2.1-2.63", "2.63-3.15"


			texts = {
				"mt_1" : [""],
				"et_1" : [""],
				"em_1" : [""],
				"mt_2" : [""],
				"et_2" : [""],
				"em_2" : ["0 < p_{T}^{#tau#tau} < 100 GeV", "100 < p_{T}^{#tau#tau} < 150 GeV", "150 < p_{T}^{#tau#tau} < 200 GeV", "200 < p_{T}^{#tau#tau} < 250 GeV", "250 < p_{T}^{#tau#tau} < 300 GeV", "p_{T}^{#tau#tau} > 300 GeV"],
				"tt_2" : ["0 < p_{T}^{#tau#tau} < 100 GeV", "100 < p_{T}^{#tau#tau} < 170 GeV", "170 < p_{T}^{#tau#tau} < 300 GeV", "p_{T}^{#tau#tau} > 300 GeV"],

				"mt_3" : ["50 < m_{#tau#tau} < 80 GeV", "80 < m_{#tau#tau} < 100 GeV","100 < m_{#tau#tau} < 115 GeV","115 < m_{#tau#tau} < 130 GeV","130 < m_{#tau#tau} < 150 GeV","150 GeV < m_{#tau#tau} < 200 GeV"],
				"et_3" : ["50 < m_{#tau#tau} < 80 GeV", "80 < m_{#tau#tau} < 100 GeV","100 < m_{#tau#tau} < 115 GeV","115 < m_{#tau#tau} < 130 GeV", "130 < m_{#tau#tau} < 150 GeV","150 GeV < m_{#tau#tau} < 200 GeV"],
				"em_3" : ["0 < m_{#tau#tau} < 80 GeV", "80 < m_{#tau#tau} < 100 GeV","100 < m_{#tau#tau} < 115 GeV","115 < m_{#tau#tau} < 130 GeV","130 < m_{#tau#tau} < 150 GeV","m_{#tau#tau} > 150 GeV"],
				"tt_3" : ["0 < m_{#tau#tau} < 80 GeV", "80 < m_{#tau#tau} < 100 GeV","100 < m_{#tau#tau} < 115 GeV","115 < m_{#tau#tau} < 130 GeV","130 < m_{#tau#tau} < 150 GeV","m_{#tau#tau} > 150 GeV"],

				"mt_4" : ["50 < m_{#tau#tau} < 80 GeV", "80 < m_{#tau#tau} < 100 GeV","100 < m_{#tau#tau} < 115 GeV","115 < m_{#tau#tau} < 130 GeV","130 < m_{#tau#tau} < 150 GeV","150 GeV < m_{#tau#tau} < 200 GeV"],
				"et_4" : ["50 < m_{#tau#tau} < 80 GeV", "80 < m_{#tau#tau} < 100 GeV","100 < m_{#tau#tau} < 115 GeV","115 < m_{#tau#tau} < 150 GeV","150 GeV < m_{#tau#tau} < 200 GeV"],
				"em_4" : ["0 < m_{#tau#tau} < 80 GeV", "80 < m_{#tau#tau} < 100 GeV","100 < m_{#tau#tau} < 115 GeV","115 < m_{#tau#tau} < 130 GeV","130 < m_{#tau#tau} < 150 GeV","150 GeV < m_{#tau#tau} < 200 GeV"],
				"tt_4" : ["0 < m_{#tau#tau} < 80 GeV", "80 < m_{#tau#tau} < 100 GeV","100 < m_{#tau#tau} < 115 GeV","115 < m_{#tau#tau} < 130 GeV","130 < m_{#tau#tau} < 150 GeV","m_{#tau#tau} > 150 GeV"],

				"mt_5" : ["50 < m_{#tau#tau} < 80 GeV", "80 < m_{#tau#tau} < 100 GeV","100 < m_{#tau#tau} < 115 GeV","115 < m_{#tau#tau} < 130 GeV","130 < m_{#tau#tau} < 150 GeV","150 GeV < m_{#tau#tau} < 200 GeV"],
				"et_5" : ["50 < m_{#tau#tau} < 80 GeV", "80 < m_{#tau#tau} < 100 GeV","100 < m_{#tau#tau} < 115 GeV", "115 < m_{#tau#tau} < 150 GeV","150 GeV < m_{#tau#tau} < 200 GeV"],

				"mt_6" : ["50 < m_{#tau#tau} < 80 GeV", "80 < m_{#tau#tau} < 100 GeV","100 < m_{#tau#tau} < 115 GeV","115 < m_{#tau#tau} < 130 GeV","130 < m_{#tau#tau} < 150 GeV","150 GeV < m_{#tau#tau} < 200 GeV"],
				"et_6" : ["50 < m_{#tau#tau} < 80 GeV", "80 < m_{#tau#tau} < 100 GeV","100 < m_{#tau#tau} < 115 GeV", "115 < m_{#tau#tau} < 150 GeV","150 GeV < m_{#tau#tau} < 200 GeV"]
			}
			texts_x = {
				"mt_1" : [0.14],
				"et_1" : [0.14],
				"em_1" : [0.2],
				"mt_2" : [0.17, 0.2975, 0.43, 0.56, 0.6925, 0.81],
				"et_2" : [0.17, 0.2975, 0.43, 0.56, 0.6925, 0.81],
				"em_2" : [0.17, 0.2975, 0.43, 0.56, 0.6925, 0.81],
				"tt_2" : [0.17, 0.2975, 0.43, 0.56, 0.6925, 0.81],
				"mt_3" : [0.17, 0.30, 0.44, 0.56, 0.69, 0.82],
				"et_3" : [0.17, 0.30, 0.44, 0.56, 0.69, 0.82],
				"em_3" : [0.17, 0.30, 0.44, 0.56, 0.69, 0.82],
				"tt_3" : [0.17, 0.30, 0.44, 0.56, 0.69, 0.82],
				"mt_4" : [0.17, 0.30, 0.44, 0.56, 0.69, 0.82],
				"et_4" : [0.18, 0.34, 0.5, 0.66, 0.81],
				"em_4" : [0.17, 0.30, 0.44, 0.56, 0.69, 0.82],
				"tt_4" : [0.17, 0.30, 0.44, 0.56, 0.69, 0.82],

				"mt_5" : [0.17, 0.30, 0.44, 0.56, 0.69, 0.82],
				"et_5" : [0.18, 0.34, 0.5, 0.66, 0.81],
				"mt_6" : [0.17, 0.30, 0.44, 0.56, 0.69, 0.82],
				"et_6" : [0.18, 0.34, 0.5, 0.66, 0.81]
			}
			texts_y = {
				"mt_1" : [0.8],
				"et_1" : [0.8],
				"em_1" : [0.8],
				"mt_2" : [0.8],
				"et_2" : [0.8],
				"em_2" : [0.8],
				"tt_2" : [0.8],
				"mt_3" : [0.8],
				"et_3" : [0.8],
				"em_3" : [0.8],
				"tt_3" : [0.8],
				"mt_4" : [0.8],
				"et_4" : [0.8],
				"em_4" : [0.8],
				"tt_4" : [0.8],
				"mt_5" : [0.8],
				"et_5" : [0.8],
				"em_5" : [0.8],
				"tt_5" : [0.8],
				"mt_6" : [0.8],
				"et_6" : [0.8],
				"em_6" : [0.8],
				"tt_6" : [0.8]
			}

			vertical_lines_x = {
				"mt_1" : ["12 12", "24 24"],
				"et_1" : ["12 12", "24 24"],
				"em_1" : ["12 12", "24 24"],
				"mt_2" : ["6 6", "12 12", "18 18", "24 24", "30 30", "36 36", "42 42", "48 48", "54 54"],
				"et_2" : ["6 6", "12 12", "18 18", "24 24", "30 30", "36 36", "42 42", "48 48", "54 54"],
				"em_2" : ["10 10", "20 20", "30 30", "40 40", "50 50"],
				"tt_2" : ["12 12", "24 24", "36 36", "48 48", "60 60"],
				"mt_3" : ["12 12", "24 24", "36 36", "48 48", "60 60"],
				"et_3" : ["12 12", "24 24", "36 36", "48 48", "60 60"],
				"em_3" : ["12 12", "24 24", "36 36", "48 48", "60 60"],
				"tt_3" : ["12 12", "24 24", "36 36", "48 48", "60 60"],
				"mt_4" : ["12 12", "24 24", "36 36", "48 48", "60 60"],
				"et_4" : ["12 12", "24 24", "36 36", "48 48", "60 60"],
				"em_4" : ["12 12", "24 24", "36 36", "48 48", "60 60"],
				"tt_4" : ["12 12", "24 24", "36 36", "48 48", "60 60"],
				"mt_5" : ["12 12", "24 24", "36 36", "48 48", "60 60","72 72","84 84","96 96","108 108","120 120","132 132","144 144"],
				"mt_6" : ["12 12", "24 24", "36 36", "48 48", "60 60","72 72","84 84","96 96","108 108","120 120","132 132","144 144"],
				"et_5" : ["12 12", "24 24", "36 36", "48 48", "60 60","72 72","84 84","96 96","108 108","120 120"],
				"et_6" : ["12 12", "24 24", "36 36", "48 48", "60 60","72 72","84 84","96 96","108 108","120 120"]
			}
		else:
			titles = {
			"mt_1" : "#mu#tau_{h} - 0jet",
			"et_1" : "e#tau_{h} - 0jet",
			"em_1" : "e#mu - 0jet",
			"tt_1" : "#tau_{h}#tau_{h} - 0jet",
			"mt_2" : "#mu#tau_{h} - boosted",
			"et_2" : "e#tau_{h} - boosted",
			"em_2" : "e#mu - boosted",
			"tt_2" : "#tau_{h}#tau_{h} - boosted",
			"mt_3" : "#mu#tau_{h} - dijet lowboost loose mjj",
			"et_3" : "e#tau_{h} - dijet lowboost loose mjj",
			"em_3" : "e#mu - dijet lowboost",
			"tt_3" : "#tau_{h}#tau_{h} - dijet lowboost",

			"em_4" : "e#mu - dijet boosted",
			"tt_4" : "#tau_{h}#tau_{h} - dijet boosted",

			#"mt_2017_1" : "#mu#tau_{h} - 0jet",
			#"et_2017_1" : "e#tau_{h} - 0jet",

			#"mt_2017_2" : "#mu#tau_{h} - boosted",
			#"et_2017_2" : "e#tau_{h} - boosted",

			#"mt_2017_3" : "#mu#tau_{h} - dijet lowboost loose mjj",
			#"et_2017_3" : "e#tau_{h} - dijet lowboost loose mjj",

			"mt_4" : "#mu#tau_{h} - dijet boosted loose mjj",
			"et_4" : "e#tau_{h} - dijet boosted loose mjj",

			"mt_5" : "#mu#tau_{h} - dijet lowboosted tight mjj",
			"et_5" : "e#tau_{h} - dijet lowboosted tight mjj",

			"mt_6" : "#mu#tau_{h} - dijet boosted tight mjj",
			"et_6" : "e#tau_{h} - dijet boosted tight mjj"
		}

			#0 100 150 200 250 300 10000
			x_tick_labels = {
				"mt_1" : ["0-60","60-65","65-70","70-75","75-80","80-85","85-90","90-95","95-100","100-105","105-110","110-400"] * 3,
				"et_1" : ["0-60","60-65","65-70","70-75","75-80","80-85","85-90","90-95","95-100","100-105","105-110","110-400"] * 3,
				"em_1" : ["0-50","50-55", "55-60","60-65","65-70","70-75","75-80","80-85","85-90","90-95","95-100","100-400"] * 3,
				"mt_2" : ["0-100","100-150","150-200","200-250","250-300", ">300"] * 10,
				"et_2" : ["0-100","100-150","150-200","200-250","250-300",">300"] * 10,
				"em_2" : ["0-80","80-90","90-100","100-110","110-120","120-130","130-140","140-150","150-160","160-300"] * 6,
				"tt_2" : ["0-40","40-60","60-70","70-80","80-90","90-100","100-110","110-120","120-130","130-150","150-200","200-250"] * 4,
				"mt_3" : ["-3.15--2.63","-2.63--2.1","-2.1--1.58","-1.58--1.05","-1.05--0.53","-0.53-0", "0-0.53","0.53-1.05", "1.05-1.58", "1.58-2.1", "2.1-2.63", "2.63-3.15"] * 5,
				"et_3" : ["-3.15--2.63","-2.63--2.1","-2.1--1.58","-1.58--1.05","-1.05--0.53","-0.53-0", "0-0.53","0.53-1.05", "1.05-1.58", "1.58-2.1", "2.1-2.63", "2.63-3.15"] * 5,
				"em_3" : ["-3.15--2.63","-2.63--2.1","-2.1--1.58","-1.58--1.05","-1.05--0.53","-0.53-0", "0-0.53","0.53-1.05", "1.05-1.58", "1.58-2.1", "2.1-2.63", "2.63-3.15"] * 6,
				"tt_3" : ["-3.15--2.63","-2.63--2.1","-2.1--1.58","-1.58--1.05","-1.05--0.53","-0.53-0", "0-0.53","0.53-1.05", "1.05-1.58", "1.58-2.1", "2.1-2.63", "2.63-3.15"] * 6,
				"mt_4" : ["-3.15--2.63","-2.63--2.1","-2.1--1.58","-1.58--1.05","-1.05--0.53","-0.53-0", "0-0.53","0.53-1.05", "1.05-1.58", "1.58-2.1", "2.1-2.63", "2.63-3.15"] * 6,
				"et_4" : ["-3.15--2.63","-2.63--2.1","-2.1--1.58","-1.58--1.05","-1.05--0.53","-0.53-0", "0-0.53","0.53-1.05", "1.05-1.58", "1.58-2.1", "2.1-2.63", "2.63-3.15"] * 5,
				"em_4" : ["-3.15--2.63","-2.63--2.1","-2.1--1.58","-1.58--1.05","-1.05--0.53","-0.53-0", "0-0.53","0.53-1.05", "1.05-1.58", "1.58-2.1", "2.1-2.63", "2.63-3.15"] * 6,
				"tt_4" : ["-3.15--2.63","-2.63--2.1","-2.1--1.58","-1.58--1.05","-1.05--0.53","-0.53-0", "0-0.53","0.53-1.05", "1.05-1.58", "1.58-2.1", "2.1-2.63", "2.63-3.15"] * 6,

				"mt_5" : ["-3.15--2.63","-2.63--2.1","-2.1--1.58","-1.58--1.05","-1.05--0.53","-0.53-0", "0-0.53","0.53-1.05", "1.05-1.58", "1.58-2.1", "2.1-2.63", "2.63-3.15"] * 6,
				"et_5" : ["-3.15--2.63","-2.63--2.1","-2.1--1.58","-1.58--1.05","-1.05--0.53","-0.53-0", "0-0.53","0.53-1.05", "1.05-1.58", "1.58-2.1", "2.1-2.63", "2.63-3.15"] * 4,
				"mt_6" : ["-3.15--2.63","-2.63--2.1","-2.1--1.58","-1.58--1.05","-1.05--0.53","-0.53-0", "0-0.53","0.53-1.05", "1.05-1.58", "1.58-2.1", "2.1-2.63", "2.63-3.15"] * 6,
				"et_6" : ["-3.15--2.63","-2.63--2.1","-2.1--1.58","-1.58--1.05","-1.05--0.53","-0.53-0", "0-0.53","0.53-1.05", "1.05-1.58", "1.58-2.1", "2.1-2.63", "2.63-3.15"] * 4,
			}

			texts = {
				"mt_1" : [""],
				"et_1" : [""],
				"em_1" : [""],
				"mt_2" : [""],
				"et_2" : [""],
				"em_2" : ["0 < p_{T}^{#tau#tau} < 100 GeV", "100 < p_{T}^{#tau#tau} < 150 GeV", "150 < p_{T}^{#tau#tau} < 200 GeV", "200 < p_{T}^{#tau#tau} < 250 GeV", "250 < p_{T}^{#tau#tau} < 300 GeV", "p_{T}^{#tau#tau} > 300 GeV"],
				"tt_2" : ["0 < p_{T}^{#tau#tau} < 100 GeV", "100 < p_{T}^{#tau#tau} < 170 GeV", "170 < p_{T}^{#tau#tau} < 300 GeV", "p_{T}^{#tau#tau} > 300 GeV"],

				"mt_3" : ["50 < m_{#tau#tau} < 80 GeV", "80 < m_{#tau#tau} < 100 GeV","100 < m_{#tau#tau} < 115 GeV","130 < m_{#tau#tau} < 150 GeV","150 GeV < m_{#tau#tau} < 200 GeV"],
				"et_3" : ["50 < m_{#tau#tau} < 80 GeV", "80 < m_{#tau#tau} < 100 GeV","100 < m_{#tau#tau} < 115 GeV","115 < m_{#tau#tau} < 150 GeV","150 GeV < m_{#tau#tau} < 200 GeV"],
				"em_3" : ["0 < m_{#tau#tau} < 80 GeV", "80 < m_{#tau#tau} < 100 GeV","100 < m_{#tau#tau} < 115 GeV","115 < m_{#tau#tau} < 130 GeV","130 < m_{#tau#tau} < 150 GeV","m_{#tau#tau} > 150 GeV"],
				"tt_3" : ["0 < m_{#tau#tau} < 80 GeV", "80 < m_{#tau#tau} < 100 GeV","100 < m_{#tau#tau} < 115 GeV","115 < m_{#tau#tau} < 130 GeV","130 < m_{#tau#tau} < 150 GeV","m_{#tau#tau} > 150 GeV"],

				"mt_4" : ["50 < m_{#tau#tau} < 80 GeV", "80 < m_{#tau#tau} < 100 GeV","100 < m_{#tau#tau} < 115 GeV","115 < m_{#tau#tau} < 130 GeV","130 < m_{#tau#tau} < 150 GeV","150 GeV < m_{#tau#tau} < 200 GeV"],
				"et_4" : ["50 < m_{#tau#tau} < 80 GeV", "80 < m_{#tau#tau} < 100 GeV","100 < m_{#tau#tau} < 115 GeV","115 < m_{#tau#tau} < 150 GeV","150 GeV < m_{#tau#tau} < 200 GeV"],
				"em_4" : ["0 < m_{#tau#tau} < 80 GeV", "80 < m_{#tau#tau} < 100 GeV","100 < m_{#tau#tau} < 115 GeV","115 < m_{#tau#tau} < 130 GeV","130 < m_{#tau#tau} < 150 GeV","150 GeV < m_{#tau#tau} < 200 GeV"],
				"tt_4" : ["0 < m_{#tau#tau} < 80 GeV", "80 < m_{#tau#tau} < 100 GeV","100 < m_{#tau#tau} < 115 GeV","115 < m_{#tau#tau} < 130 GeV","130 < m_{#tau#tau} < 150 GeV","m_{#tau#tau} > 150 GeV"],

				"mt_5" : ["50 < m_{#tau#tau} < 80 GeV", "80 < m_{#tau#tau} < 100 GeV","100 < m_{#tau#tau} < 115 GeV","115 < m_{#tau#tau} < 130 GeV","130 < m_{#tau#tau} < 150 GeV","150 GeV < m_{#tau#tau} < 200 GeV"],
				"et_5" : ["50 < m_{#tau#tau} < 80 GeV", "80 < m_{#tau#tau} < 100 GeV","100 < m_{#tau#tau} < 150 GeV","150 GeV < m_{#tau#tau} < 200 GeV"],

				"mt_6" : ["50 < m_{#tau#tau} < 80 GeV", "80 < m_{#tau#tau} < 100 GeV","100 < m_{#tau#tau} < 115 GeV","115 < m_{#tau#tau} < 130 GeV","130 < m_{#tau#tau} < 150 GeV","150 GeV < m_{#tau#tau} < 200 GeV"],
				"et_6" : ["50 < m_{#tau#tau} < 80 GeV", "80 < m_{#tau#tau} < 100 GeV","100 < m_{#tau#tau} < 150 GeV","150 GeV < m_{#tau#tau} < 200 GeV"]
			}
			texts_x = {
				"mt_1" : [0.14],
				"et_1" : [0.14],
				"em_1" : [0.2],
				"mt_2" : [0.17, 0.2975, 0.43, 0.56, 0.6925, 0.81],
				"et_2" : [0.17, 0.2975, 0.43, 0.56, 0.6925, 0.81],
				"em_2" : [0.17, 0.2975, 0.43, 0.56, 0.6925, 0.81],
				"tt_2" : [0.17, 0.2975, 0.43, 0.56, 0.6925, 0.81],
				"mt_3" : [0.18, 0.34, 0.5, 0.66, 0.81],
				"et_3" : [0.18, 0.34, 0.5, 0.66, 0.81],
				"em_3" : [0.17, 0.30, 0.44, 0.56, 0.69, 0.82],
				"tt_3" : [0.17, 0.30, 0.44, 0.56, 0.69, 0.82],
				"mt_4" : [0.17, 0.30, 0.44, 0.56, 0.69, 0.82],
				"et_4" : [0.18, 0.34, 0.5, 0.66, 0.81],
				"em_4" : [0.17, 0.30, 0.44, 0.56, 0.69, 0.82],
				"tt_4" : [0.17, 0.30, 0.44, 0.56, 0.69, 0.82],

				"mt_5" : [0.17, 0.30, 0.44, 0.56, 0.69, 0.82],
				"et_5" : [0.2, 0.4, 0.6, 0.8],
				"mt_6" : [0.17, 0.30, 0.44, 0.56, 0.69, 0.82],
				"et_6" : [0.2, 0.4, 0.6, 0.8]
			}
			texts_y = {
				"mt_1" : [0.8],
				"et_1" : [0.8],
				"em_1" : [0.8],
				"mt_2" : [0.8],
				"et_2" : [0.8],
				"em_2" : [0.8],
				"tt_2" : [0.8],
				"mt_3" : [0.8],
				"et_3" : [0.8],
				"em_3" : [0.8],
				"tt_3" : [0.8],
				"mt_4" : [0.8],
				"et_4" : [0.8],
				"em_4" : [0.8],
				"tt_4" : [0.8],
				"mt_5" : [0.8],
				"et_5" : [0.8],
				"em_5" : [0.8],
				"tt_5" : [0.8],
				"mt_6" : [0.8],
				"et_6" : [0.8],
				"em_6" : [0.8],
				"tt_6" : [0.8]
			}

			vertical_lines_x = {
				"mt_1" : ["12 12", "24 24"],
				"et_1" : ["12 12", "24 24"],
				"em_1" : ["12 12", "24 24"],
				"mt_2" : ["6 6", "12 12", "18 18", "24 24", "30 30", "36 36", "42 42", "48 48", "54 54"],
				"et_2" : ["6 6", "12 12", "18 18", "24 24", "30 30", "36 36", "42 42", "48 48", "54 54"],
				"em_2" : ["10 10", "20 20", "30 30", "40 40", "50 50"],
				"tt_2" : ["12 12", "24 24", "36 36", "48 48", "60 60"],
				"mt_3" : ["12 12", "24 24", "36 36", "48 48"],
				"et_3" : ["12 12", "24 24", "36 36", "48 48"],
				"em_3" : ["12 12", "24 24", "36 36", "48 48", "60 60"],
				"tt_3" : ["12 12", "24 24", "36 36", "48 48", "60 60"],
				"mt_4" : ["12 12", "24 24", "36 36", "48 48", "60 60"],
				"et_4" : ["12 12", "24 24", "36 36", "48 48"],
				"em_4" : ["12 12", "24 24", "36 36", "48 48", "60 60"],
				"tt_4" : ["12 12", "24 24", "36 36", "48 48", "60 60"],
				"mt_5" : ["12 12", "24 24", "36 36", "48 48", "60 60"],
				"mt_6" : ["12 12", "24 24", "36 36", "48 48", "60 60"],
				"et_5" : ["12 12", "24 24", "36 36"],
				"et_6" : ["12 12", "24 24", "36 36"]
			}

		prefit_postfit_plot_configs = datacards.prefit_postfit_plots(datacards_cbs, datacards_postfit_shapes, plotting_args={"ratio" : args.ratio, "args" : args.args, "lumi" : args.lumi, "normalize" : not(do_not_normalize_by_bin_width), "era" : args.era, "x_expressions" : config["x_expressions"][0], "return_configs" : True, "merge_backgrounds" : backgrounds_to_merge, "add_soverb_ratio" : True}, n_processes=args.n_processes, no_plot=[""])
		for plot_config in prefit_postfit_plot_configs:

			plot_category = (plot_config["filename"].split("_")[-2])
			plot_year = (plot_config["filename"].split("_")[-3])
			plot_channel = plot_config["filename"].split("_")[-4]

			if ("1" in plot_category or "2" in plot_category or "3" in plot_category or "4" in plot_category or "5" in plot_category or "6" in plot_category) and not any(control_region_ID in plot_category for control_region_ID in ["10","11","12","13","14","15","16","17","18","19","20"]):

				print("Category to be plotted: ", plot_category)
				a = plot_category
				#if plot_category == "5" or plot_category == "6":  #hack if no binning in etasep is used
				#	a = "4"
				plot_config["canvas_width"] = 2100
				plot_config["canvas_height"] = 1000
				if plot_category == "1":
					plot_config["x_label"] = "m_{sv} / GeV"
				elif  plot_category == "2":
					plot_config["x_label"] = "p_{T}^{#tau#tau} / GeV"
				else:
					plot_config["x_label"] = "#Delta#phi_{jj}" #if "jdphi" == args.quantity else "D_{CP}^{*}"
				if "--y-log" in args.args:
					plot_config["y_lims"] = ylog_lims[plot_channel+"_"+a]
				else:
					plot_config["y_rel_lims"] = [0.5, 1.2]
				plot_config["legend"] = [0.895, 0.2, 0.995, 0.9]
				plot_config["legend_cols"] = 1
				# plot_config["x_label"] = "m_{vis} (GeV)" if "1" in plot_category and plot_channel in ["mt", "et", "em"] else "m_{#tau#tau} (GeV)"
				plot_config["y_label"] = "Events/bin"
				plot_config["formats"] = ["pdf", "png"]
				plot_config["title"] = titles[plot_channel+"_"+plot_category]  #+ "\t  CMS, work in progress"
				plot_config["y_title_offset"] = 0.55
				plot_config["y_subplot_title_offset"] = 0.71
				plot_config["y_subplot_lims"] = [-4, 4]
				plot_config["left_pad_margin"] = 0.1
				plot_config["right_pad_margin"] = 0.11
				plot_config["line_widths"] = [3]

				if not (plot_channel == "tt" or plot_category == "1" ):
					plot_config["x_tick_labels"] = x_tick_labels[plot_channel+"_"+a]

					# plot_config["texts"] = texts[plot_channel+"_"+a] #  + sub_texts[plot_channel+"_"+plot_category]
					# plot_config["texts_x"] = texts_x[plot_channel+"_"+a] #  + sub_texts_x[plot_channel+"_"+plot_category]
					# plot_config["texts_y"] = texts_y[plot_channel+"_"+a] #  +  list((0.65 for i in range(len(sub_texts[plot_channel+"_"+plot_category]))))
					# plot_config["texts_size"] = [0.035] if "2" in plot_category and plot_channel in ["mt", "et", "em"] else [0.035]
					if plot_category in ["5","6"]:
						if "CP1" in args.quantity or "CP2" in args.quantity:
							plot_config["x_ticks"] = x_ticks[plot_channel+"_"+plot_category]
							plot_config["n_divisions"] = [12,0,0]
					if plot_category in ["3","4"]:
						if "recoPhiStarCPCombMergedHelrPVBS" in args.quantity:
							plot_config["x_ticks"] = x_ticks[plot_channel+"_"+plot_category]
							plot_config["n_divisions"] = [12,0,0]
					plot_config["x_labels_vertical"] = True
					plot_config["x_title_offset"] = 1.6
					plot_config["bottom_pad_margin"] = 0.5


					plot_config["analysis_modules"].append("AddLine")
					# plot_config["x_lines"] = vertical_lines_x[plot_channel+"_"+a]
					# plot_config["y_lines"] = [" ".join(map(str,plot_config["y_lims"]))]*len(plot_config["x_lines"])
					# if plot_category in ["5","6"] and ("CP1" in args.quantity or "CP2" in args.quantity):
					# 	plot_config["colors"] += ["kRed", "kBlue"]*(len(plot_config["x_lines"])/2)
					# 	plot_config["y_lines"] = [" ".join(map(str,[0.15*ylim for ylim in plot_config["y_lims"]])), " ".join(map(str,plot_config["y_lims"]))]*(len(plot_config["x_lines"])/2)
					# else:
					# 	plot_config["colors"] += ["kBlue"]*(len(plot_config["x_lines"]))

					# for i in range(len(plot_config["x_lines"])):
					# 	#plot_config["labels"].append("line_"+str(i))
					# 	plot_config["markers"].append("L")
					# 	plot_config["stacks"].append("line_"+str(i))
					# 	plot_config["labels"].append("")

					#plot_config["subplot_lines"] = vertical_lines[plot_channel+"_"+plot_category]

				#from IPython import embed; embed()

		if "nuisanceimpacts" in args.steps:
			datacards.nuisance_impacts(datacards_cbs, datacards_workspaces_alpha, args.n_processes, higgs_mass="125")
		higgsplot.HiggsPlotter(list_of_config_dicts=prefit_postfit_plot_configs, list_of_args_strings=[args.args], n_processes=args.n_processes, n_plots=args.n_plots[1])
