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
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.systematics_run2 as systematics
import HiggsAnalysis.KITHiggsToTauTau.datacards.smhttdatacards as smhttdatacards
import HiggsAnalysis.KITHiggsToTauTau.datacards.initialstatecpstudiesdatacards as initialstatecpstudiesdatacards



def _call_command(command):
	log.debug(command)
	logger.subprocessCall(command, shell=True)
	
def official2private(category, category_replacements):
	result = copy.deepcopy(category)
	for official, private in category_replacements.iteritems():
		if not "dijet_boosted" in result:
			result = re.sub(official+"$", private, result)
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
	
def remove_procs_and_systs_with_zero_yield(proc):
	# TODO: find out why zero yield should be ok in control regions. until then remove them
	#null_yield = not (proc.rate() > 0. or is_control_region(proc))
	null_yield = not proc.rate() > 0.
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
	parser.add_argument("--background-method", default="new",
	                    help="Background estimation method to be used. [Default: %(default)s]")
	parser.add_argument("-b", "--batch", default=None, const="rwthcondor", nargs="?",
	                    help="Run with grid-control. Optionally select backend. [Default: %(default)s]")
	parser.add_argument("--remote", action="store_true", default=False,
	                    help="Pack result to tarball, necessary for grid-control. [Default: %(default)s]")
	parser.add_argument("-n", "--n-processes", type=int, default=1,
	                    help="Number of (parallel) processes. [Default: %(default)s]")
	parser.add_argument("-f", "--n-plots", type=int, nargs=2, default=[None, None],
	                    help="Number of plots for datacard inputs (1st arg) and for postfit plots (2nd arg). [Default: all]")
	parser.add_argument("-o", "--output-dir",
	                    default="$CMSSW_BASE/src/plots/htt_datacards/",
	                    help="Output directory. [Default: %(default)s]")
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
	parser.add_argument("--no-syst-uncs", default=False, action="store_true",
	                    help="Do not include systematic uncertainties. This should only be used together with --use-asimov-dataset. [Default: %(default)s]")
	parser.add_argument("--production-mode", nargs="+",
	                    default=["ggh", "qqh"],
	                    choices=["ggh", "qqh"],
	                    help="Choose the production modes. Option needed for initial state studies. [Default: %(default)s]")	
	parser.add_argument("--qcd-subtract-shapes", action="store_false", default=True, help="subtract shapes for QCD estimation [Default:%(default)s]")											
	parser.add_argument("--steps", nargs="+",
	                    default=["inputs","maxlikelihoodfit", "prefitpostfitplots", "pvalue", "likelihoodScan"],
	                    choices=["inputs","maxlikelihoodfit", "prefitpostfitplots", "pvalue", "nuisanceimpacts", "likelihoodScan", "yields"],
	                    help="Steps to perform. [Default: %(default)s]")
	parser.add_argument("--use-shape-only", action="store_true", default=False,
	                    help="Use only shape to distinguish between cp hypotheses. [Default: %(default)s]")
	parser.add_argument("--get-official-dc", action="store_true", default=False,
	                    help="Get official CP datacards. [Default: %(default)s]")
	parser.add_argument("--do-not-ignore-category-removal", default=False, action="store_true",
						help="Exit program in case categories are removed from CH. [Default: %(default)s]")
	parser.add_argument("--use-asimov-dataset", action="store_true", default=False,
	                    help="Use s+b expectation as observation instead of real data. [Default: %(default)s]")
	parser.add_argument("--use-rateParam", action="store_true", default=False,
	                    help="Use rate parameter to estimate ZTT normalization from ZMM. [Default: %(default)s]")
	parser.add_argument("--x-bins", default=None,
	                    help="Manualy set the binning. Default is taken from configuration files.")
        parser.add_argument("-b", "--batch", default=None, const="rwthcondor", nargs="?",
			    help="Run with grid-control. Optionally select backend. [Default: %(default)s]")

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
	
	args.output_dir = os.path.abspath(os.path.expandvars(args.output_dir))
	if args.clear_output_dir and os.path.exists(args.output_dir):
		logger.subprocessCall("rm -r " + args.output_dir, shell=True)
	
	# initialisations for plotting
	sample_settings = samples.Samples()
	binnings_settings = binnings.BinningsDict()
	systematics_factory = systematics.SystematicsFactory()
	
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
	
	if args.get_official_dc:
		# get "official" configuration
		init_directory = os.path.join(args.output_dir, "init")
		command = "MorphingSMCP2016 --control_region=1  --mm_fit=false --ttbar_fit=true --only_init=" + init_directory
		log.debug(command)
		exit_code = logger.subprocessCall(shlex.split(command))
		assert(exit_code == 0)
		
		init_cb = ch.CombineHarvester()
		for init_datacard in glob.glob(os.path.join(init_directory, "*_*_*_*.txt")):			
			init_cb.QuickParseDatacard(init_datacard, '$ANALYSIS_$ERA_$CHANNEL_$BINID_$MASS.txt', False)
		
		datacards = initialstatecpstudiesdatacards.InitialStateCPStudiesDatacards(
				cb=init_cb,
				higgs_masses=args.higgs_masses,
				year=args.era,
				cp_study=args.cp_study
		)
		
		# The processes have different names in the official SM datacards
		# So this workaround is needed to match the right processes
		datacards.configs._mapping_process2sample = {
			"data_obs" : "data",
			"ZTT" : "ztt",
			"ZL" : "zl",
			"ZLL" : "zll",
			"ZJ" : "zj",
			"EWKZ" : "ewkz",
			"TT" : "ttj",
			"TTT" : "ttt",
			"TTJ" : "ttj",
			"VV" : "vv",
			"VVT" : "vvt",
			"VVJ" : "vvj",
			"W" : "wj",
			"QCD" : "qcd",
			"ggH_htt" : "ggh",
			"qqH_htt" : "qqh",
			"ggHps_htt"	: "gghjhups",
			"ggHmm_htt"	: "gghjhumm",
			"ggHsm_htt"	: "gghjhusm",
			"qqHsm_htt"	: "qqhjhusm",
			"qqHmm_htt"	: "qqhjhumm",
			"qqHps_htt"	: "qqhjhups",
			"WH_htt" : "wh",
			"ZH_htt" : "zh",
			"ggH_hww" : "hww_gg",
			"qqH_hww" : "hww_qq",
			}
			
		# Also the categories have different names.
		# Match SM categories and control regions. 
		category_replacements["all"] = "TTbarCR"
		category_replacements["wjets_0jet_cr"] = "ZeroJet2D_WJCR"
		category_replacements["wjets_boosted_cr"] = "Boosted2D_WJCR"
		category_replacements["wjets_vbf_cr"] = "Vbf2D_WJCR"
		category_replacements["antiiso_0jet_cr"] = "ZeroJet2D_QCDCR"
		category_replacements["antiiso_boosted_cr"] = "Boosted2D_QCDCR"
		category_replacements["antiiso_vbf_cr"] = "Vbf2D_QCDCR"
		category_replacements["0jet_qcd_cr"] = "ZeroJet2D_QCDCR"
		category_replacements["boosted_qcd_cr"] = "Boosted2D_QCDCR"
		category_replacements["vbf_qcd_cr"] = "Vbf2D_QCDCR"
		
		category_replacements["0jet"] = "ZeroJet2D"
		category_replacements["boosted"] = "Boosted2D"
		category_replacements["vbf"] = "Vbf2D"
		
	else:
		# use the datacards created within Artus.
		datacards = initialstatecpstudiesdatacards.InitialStateCPStudiesDatacards(
				higgs_masses=args.higgs_masses,
				year=args.era,
				cp_study=args.cp_study
		)
	
		datacards.configs._mapping_process2sample = {
			"data_obs" : "data",
			"ZTT" : "ztt",
			"ZL" : "zl",
			"ZLL" : "zll",
			"ZJ" : "zj",
			"EWKZ" : "ewkz",
			"TT" : "ttj",
			"TTT" : "ttt",
			"TTJJ" : "ttjj",
			"VV" : "vv",
			"VVT" : "vvt",
			"VVJ" : "vvj",
			"W" : "wj",
			"QCD" : "qcd",
			"qqH"	: "qqh",
			"ggHps"	: "gghjhups",
			"ggHmm"	: "gghjhumm",
			"ggHsm"	: "gghjhusm",
			"qqHsm"	: "qqhjhusm",
			"ggH" : "ggh"
		}
		
	if args.channel != parser.get_default("channel"):
		args.channel = args.channel[len(parser.get_default("channel")):]

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
		"Total",
		"Closure"
	]
	
	# os/ss factors for different categories
	ss_os_factors = {
		"mt_ZeroJet2D" : 1.07,
		"mt_Boosted2D" : 1.06,
		"mt_Vbf2D" : 1.0,
		"et_ZeroJet2D" : 1.0,
		"et_Boosted2D" : 1.28,
		"et_Vbf2D" : 1.0,
		"em_ZeroJet2D" : 2.27,
		"em_Boosted2D" : 2.26,
		"em_Vbf2D" : 2.84
	}	
	# w+jets scale factor shifts for different categories
	# same uncertainties as used for WHighMTtoLowMT_$BIN_13TeV
	wj_sf_shifts = {
		"mt_ZeroJet2D" : 0.10,
		"mt_Boosted2D" : 0.05,
		"mt_Vbf2D" : 0.10,
		"et_ZeroJet2D" : 0.10,
		"et_Boosted2D" : 0.05,
		"et_Vbf2D" : 0.10
	}

	# correction factors from ZMM control region
	zmm_cr_factors = {
		"ZeroJet2D" : "(1.0395)",
		"Boosted2D" : "(((ptvis<100)*1.0321) + ((ptvis>=100)*(ptvis<150)*1.023) + ((ptvis>=150)*(ptvis<200)*1.007) + ((ptvis>=200)*(ptvis<250)*1.016) + ((ptvis>=250)*(ptvis<300)*1.02) + ((ptvis>=300)*1.03))",
		"Vbf2D" : "(((mjj<300)*1.0) + ((mjj>=300)*(mjj<700)*1.0605) + ((mjj>=700)*(mjj<1100)*1.017) + ((mjj>=1100)*(mjj<1500)*0.975) + ((mjj>=1500)*0.97))",
		"Vbf2D_Up" : "(((mjj<300)*1.0) + ((mjj>=300)*(mjj<700)*1.121) + ((mjj>=700)*(mjj<1100)*1.034) + ((mjj>=1100)*(mjj<1500)*0.95) + ((mjj>=1500)*0.94))",
		"Vbf2D_Down" : "(1.0)"
	}

	# corrections factors from ZMM control regions as written on SM HTT Twiki
	zmm_cr_0jet_global = "(1.0)"
	zmm_cr_boosted_global = "(1.0)"
	zmm_cr_vbf_global = "(1.02)"
	zmm_cr_factors_official = {
		"mt_ZeroJet2D" : zmm_cr_0jet_global,
		"et_ZeroJet2D" : zmm_cr_0jet_global,
		"em_ZeroJet2D" : "(1.02)",
		"tt_ZeroJet2D" : zmm_cr_0jet_global,
		"mt_Boosted2D" : zmm_cr_boosted_global,
		"et_Boosted2D" : zmm_cr_boosted_global,
		"em_Boosted2D" : zmm_cr_boosted_global,
		"tt_Boosted2D" : zmm_cr_boosted_global,
		"mt_Vbf2D" : zmm_cr_vbf_global+"*(((mjj>=300)*(mjj<700)*1.06) + ((mjj>=700)*(mjj<1100)*0.98) + ((mjj>=1100)*(mjj<1500)*0.95) + ((mjj>=1500)*0.95))",
		"et_Vbf2D" : zmm_cr_vbf_global+"*(((mjj>=300)*(mjj<700)*1.06) + ((mjj>=700)*(mjj<1100)*0.98) + ((mjj>=1100)*(mjj<1500)*0.95) + ((mjj>=1500)*0.95))",
		"em_Vbf2D" : zmm_cr_vbf_global+"*(((mjj>=300)*(mjj<700)*1.06) + ((mjj>=700)*(mjj<1100)*0.98) + ((mjj>=1100)*(mjj<1500)*0.95) + ((mjj>=1500)*0.95))",
		"tt_Vbf2D" : "(((mjj<300)*1.00) + ((mjj>=300)*(mjj<500)*1.02) + ((mjj>=500)*(mjj<800)*1.06) + ((mjj>=800)*1.04))",
		"mt_Vbf2D_Up" : zmm_cr_vbf_global+"*(((mjj>=300)*(mjj<700)*1.12) + ((mjj>=700)*(mjj<1100)*0.96) + ((mjj>=1100)*(mjj<1500)*0.90) + ((mjj>=1500)*0.90))",
		"et_Vbf2D_Up" : zmm_cr_vbf_global+"*(((mjj>=300)*(mjj<700)*1.12) + ((mjj>=700)*(mjj<1100)*0.96) + ((mjj>=1100)*(mjj<1500)*0.90) + ((mjj>=1500)*0.90))",
		"em_Vbf2D_Up" : zmm_cr_vbf_global+"*(((mjj>=300)*(mjj<700)*1.12) + ((mjj>=700)*(mjj<1100)*0.96) + ((mjj>=1100)*(mjj<1500)*0.90) + ((mjj>=1500)*0.90))",
		"tt_Vbf2D_Up" : "(((mjj<300)*1.00) + ((mjj>=300)*(mjj<500)*1.04) + ((mjj>=500)*(mjj<800)*1.12) + ((mjj>=800)*1.08))",
		"mt_Vbf2D_Down" : zmm_cr_vbf_global,
		"et_Vbf2D_Down" : zmm_cr_vbf_global,
		"em_Vbf2D_Down" : zmm_cr_vbf_global,
		"tt_Vbf2D_Down" : "(1.0)"
	}

	# ttbar nicks for which to apply different top pt reweighting
	top_pt_reweight_nicks = [
		"noplot_ttj_ss_lowmt", # mt & et channels: qcd yield subtract
		"noplot_ttj_shape_ss_qcd_control", # mt & et channels: qcd shape subtract
		"noplot_ttj_os_highmt", # mt & et channels: w+jets yield subtract
		"noplot_ttj_ss_highmt" # mt & et channels: qcd high mt yield subtract
	]

	categoriesWithRelaxedIsolationForW = [
		"Boosted2D",
		"Vbf2D"
	]

	categoriesWithRelaxedIsolationForQCD = [
		"ZeroJet2D",
		"Boosted2D",
		"Vbf2D"
	]
	
	do_not_normalize_by_bin_width = args.do_not_normalize_by_bin_width
	
	# initialise datacards
	tmp_input_root_filename_template = "input/${ANALYSIS}_${CHANNEL}_${BIN}_${SYSTEMATIC}_${ERA}.root"
	input_root_filename_template = "input/${ANALYSIS}_${CHANNEL}_${BIN}_${ERA}.root"
	bkg_histogram_name_template = "${BIN}/${PROCESS}"
	sig_histogram_name_template = "${BIN}/${PROCESS}${MASS}"
	bkg_syst_histogram_name_template = "${BIN}/${PROCESS}_${SYSTEMATIC}"
	sig_syst_histogram_name_template = "${BIN}/${PROCESS}${MASS}_${SYSTEMATIC}"
	datacard_filename_templates = []
	if "individual" in args.combinations:
		datacard_filename_templates.append("datacards/individual/${CHANNEL}/${BINID}/${ANALYSIS}_${CHANNEL}_${BINID}_${ERA}.txt")
	if "channel" in args.combinations:
		datacard_filename_templates.append("datacards/channel/${CHANNEL}/${ANALYSIS}_${CHANNEL}_${ERA}.txt")
	if "category" in args.combinations:
		datacard_filename_templates.append("datacards/category/${BINID}/${ANALYSIS}_${BINID}_${ERA}.txt")
	if "combined" in args.combinations:
		datacard_filename_templates.append("datacards/combined/${ANALYSIS}_${ERA}.txt")		
	output_root_filename_template = "datacards/common/${ANALYSIS}.input_${ERA}.root"

	# if args.channel != parser.get_default("channel"):
	# 	args.channel = args.channel[len(parser.get_default("channel")):]
    # 
	# if args.categories != parser.get_default("categories"):
	# 	args.categories = args.categories[1:]

	# catch if on command-line only one set has been specified and repeat it
	if(len(args.categories) == 1):
		args.categories = [args.categories[0]] * len(args.channel)
	
	#restriction to requested masses
	datacards.cb.mass(args.higgs_masses)
	
	#restriction to requested channels
	if not ("all" in args.channel):
		datacards.cb.channel(args.channel)
	args.channel = datacards.cb.cp().channel_set()
	
	# restrict combine to lnN systematics only if no_shape_uncs is set
	if args.no_shape_uncs or args.no_syst_uncs:
		log.debug("Deactivate shape uncertainties")
		datacards.remove_shape_uncertainties()
		if log.isEnabledFor(logging.DEBUG):
			datacards.cb.PrintSysts()
			
	for index, (channel, categories) in enumerate(zip(args.channel, args.categories)):
		
		if channel in ["em", "ttbar"]:
			datacards.configs._mapping_process2sample["ZL"] = "zll"
		else:
			datacards.configs._mapping_process2sample["ZL"] = "zl"
		
		if channel in ["et", "mt", "tt"]:
			datacards.configs._mapping_process2sample.pop("TT", None)
			datacards.configs._mapping_process2sample["TTT"]= "ttt"
			datacards.configs._mapping_process2sample["TTJ"]= "ttj"
		else:
			datacards.configs._mapping_process2sample["TT"] = "ttj"
			#datacards.configs._mapping_process2sample.pop("TTT")
			datacards.configs._mapping_process2sample.pop("TTJ", None)
		
		if "all" in categories:
			categories = datacards.cb.cp().channel([channel]).bin_set()
		else:
			# include channel prefix
			categories = [channel + "_" + category for category in categories]
		
		# prepare category settings based on args and datacards
		categories_save = sorted(categories)
		categories = list(set(categories).intersection(set(datacards.cb.cp().channel([channel]).bin_set())))
		if(categories_save != sorted(categories)) and args.do_not_ignore_category_removal:
			log.fatal("CombineHarverster removed the following categories automatically. Was this intended?")
			log.fatal(list(set(categories_save) - set(categories)))
			sys.exit(1)
		
		
		# restrict CombineHarvester to configured categories:
		datacards.cb.FilterAll(lambda obj : (obj.channel() == channel) and (obj.bin() not in categories))
	 	
		log.info("Building configs for channel = {channel}, categories = {categories}".format(channel=channel, categories=str(categories)))
		for official_category in categories:
			
			category = official2private(official_category, category_replacements)	

			datacards_per_channel_category = initialstatecpstudiesdatacards.InitialStateCPStudiesDatacards(cb=datacards.cb.cp().channel([channel]).bin([official_category]))	
			exclude_cuts = copy.deepcopy(args.exclude_cuts)
			if "TTbarCR" in category and channel == "ttbar":
				exclude_cuts += ["pzeta"]
				do_not_normalize_by_bin_width = True
			# TODO: check that this does what it should in samples_run2_2016.py !!!
			#       a workaround solution may be necessary
			if ("ZeroJet2D_WJCR" in category or "Boosted2D_WJCR" in category) and channel in ["mt", "et"]:
				exclude_cuts += ["mt"]
				do_not_normalize_by_bin_width = True
			if ("ZeroJet2D_QCDCR" in category or "Boosted2D_QCDCR" in category or "Vbf2D_QCDCR" in category)  and channel in ["mt", "et", "tt"]:
				if channel in ["mt", "et"]:
					exclude_cuts += ["iso_1"]
					do_not_normalize_by_bin_width = True
				elif channel == "tt":
					exclude_cuts += ["iso_1", "iso_2"]
					do_not_normalize_by_bin_width = True
				
				datacards_per_channel_category = initialstatecpstudiesdatacards.InitialStateCPStudiesDatacards(cb=datacards.cb.cp().channel([channel]).bin([official_category]))
			
			higgs_masses = [mass for mass in datacards_per_channel_category.cb.mass_set()]
			output_file = os.path.join(args.output_dir, input_root_filename_template.replace("$", "").format(
					ANALYSIS="htt",
					CHANNEL=channel,
					BIN=official_category, # why is this necessary?
					ERA="13TeV"
			))
			#merged_output_files.append(output_file)
			output_files.append(output_file)
			tmp_output_files = []
			
			for shape_systematic, list_of_samples in datacards_per_channel_category.get_samples_per_shape_systematic().iteritems():
				# print(shape_systematic, list_of_samples)
				nominal = (shape_systematic == "nominal")
				list_of_samples = (["data"] if nominal else []) + [datacards.configs.process2sample(re.sub('125', '', process)) for process in list_of_samples]

				# This is needed because wj and qcd are interdependent when using the new background estimation method
				# NB: CH takes care to only use the templates for processes that you specified. This means that any
				#     superfluous histograms created as a result of this problem do not influence the result
				if args.background_method == "new":
					if "qcd" in list_of_samples and "wj" not in list_of_samples:
						list_of_samples += ["wj"]
					elif "wj" in list_of_samples and "qcd" not in list_of_samples:
						list_of_samples += ["qcd"]

				for shift_up in ([True] if nominal else [True, False]):
					systematic = "nominal" if nominal else (shape_systematic + ("Up" if shift_up else "Down"))
									
					config={}
					
					log.debug("Create inputs for (samples, systematic) = ([\"{samples}\"], {systematic}), (channel, category) = ({channel}, {category}).".format(
							samples="\", \"".join(list_of_samples),
							channel=channel,
							category=category,
							systematic=systematic
					))
						
					ss_os_factor = ss_os_factors.get(category,0.0)
					wj_sf_shift = wj_sf_shifts.get(category,0.0)
					if "WSFUncert" in shape_systematic and wj_sf_shift != 0.0:
						wj_sf_shift = 1.0 + wj_sf_shift if shift_up else 1.0 - wj_sf_shift
					else:
						wj_sf_shift = 0.0
					# Use official zmm corrections factors for now
					#zmm_cr_factor = zmm_cr_factors.get(category.split("_")[-1],"(1.0)")
					zmm_cr_factor = zmm_cr_factors_official.get(category, "(1.0)")
					if "zmumuShape_VBF" in shape_systematic:
						#zmm_cr_factor = zmm_cr_factors.get(category.split("_")[-1]+("_Up" if shift_up else "_Down"),"(1.0)")
						zmm_cr_factor = zmm_cr_factors_official.get(category+("_Up" if shift_up else "_Down"),"(1.0)")
					
					# prepare plotting configs for retrieving the input histograms
					config = sample_settings.get_config(
							samples=[getattr(samples.Samples, sample) for sample in list_of_samples],
							channel=channel,
							category="catHtt13TeV_"+category,
							weight=args.weight,
							lumi = args.lumi * 1000,
							exclude_cuts=exclude_cuts,
							higgs_masses=higgs_masses,
							cut_type="cp2016" if args.era == "2016" else "baseline",
							estimationMethod=args.background_method,
							ss_os_factor=ss_os_factor,
							wj_sf_shift=wj_sf_shift,
							zmm_cr_factor=zmm_cr_factor,
							useRelaxedIsolationForW = (category.split("_")[1] in categoriesWithRelaxedIsolationForW),
							useRelaxedIsolationForQCD = (category.split("_")[1] in categoriesWithRelaxedIsolationForQCD)
					)
					
					
					if "CMS_scale_gg_13TeV" in shape_systematic:
						systematics_settings = systematics_factory.get(shape_systematic)(config, category)
					elif "CMS_scale_j_" in shape_systematic and shape_systematic.split("_")[-2] in jecUncertNames:
						systematics_settings = systematics_factory.get(shape_systematic)(config, shape_systematic.split("_")[-2])
					else:
						systematics_settings = systematics_factory.get(shape_systematic)(config)
					# TODO: evaluate shift from datacards_per_channel_category.cb
					config = systematics_settings.get_config(shift=(0.0 if nominal else (1.0 if shift_up else -1.0)))
					
					for index, weight in enumerate(config.get("weights", [])):
						weightAtIndex = config["weights"][index]
						if channel in ["mt", "et", "tt"]:
							if config["nicks"][index] in top_pt_reweight_nicks or channel == "tt":
								weightAtIndex = weightAtIndex.replace("topPtReweightWeight", "topPtReweightWeightRun1")
					
						config["weights"][index] = weightAtIndex
					#config["x_expressions"] = ["m_vis"] if channel == "mm" and args.quantity == "m_sv" else [args.quantity]

					# TODO: evaluate shift from datacards.cb
					#config = systematics_settings.get_config(shift=(0.0 if nominal else (1.0 if shift_up else -1.0)))
					config["qcd_subtract_shape"] = [args.qcd_subtract_shapes]
					config["x_expressions"] =  [args.quantity]
					
					if (args.cp_study == "ggh" or args.cp_study == "vbf") and "mela" not in category:
						binnings_key = "tt_jdphi"
					if (args.cp_study == "ggh" or args.cp_study == "vbf") and "mela" in category:
						binnings_key = "tt_melaDiscriminatorD0Minus"
					elif args.cp_study == "final":
						binnings_key = "tt_phiStarCP"
						
					if "2D" not in category:
						binnings_key = "binningHtt13TeV_"+category+"_%s"%args.quantity
						if (binnings_key in binnings_settings.binnings_dict) and args.x_bins == None:
							config["x_bins"] = [binnings_settings.binnings_dict[binnings_key]]
						elif args.x_bins != None:
							config["x_bins"] = [args.x_bins]
						else:
							log.fatal("binnings key " + binnings_key + " not found in binnings_dict!")
							sys.exit()
					
					# define quantities and binning for control regions
					if ("ZeroJet2D_WJCR" in category or "Boosted2D_WJCR" in category) and channel in ["mt", "et"]:
						config["x_expressions"] = ["mt_1"]
						config["x_bins"] = [binnings_settings.binnings_dict["binningHtt13TeV_"+category+"_mt_1"]]
					if "ZeroJet2D_QCDCR" in category and channel in ["mt", "et", "tt"]:
						if channel in ["mt", "et"]:
							config["x_expressions"] = ["m_vis"]
							config["x_bins"] = [binnings_settings.binnings_dict["binningHtt13TeV_"+category+"_m_vis"]]
						elif channel == "tt":
							config["x_expressions"] = ["m_sv"]
							config["x_bins"] = [binnings_settings.binnings_dict["binningHtt13TeV_"+category+"_m_sv"]]
					if "Boosted2D_QCDCR" in category and channel in ["mt", "et", "tt"]:
						config["x_expressions"] = ["m_sv"]
						config["x_bins"] = [binnings_settings.binnings_dict["binningHtt13TeV_"+category+"_m_sv"]]
					if "Vbf2D_QCDCR" in category and channel == "tt":
						config["x_expressions"] = ["m_sv"]
						config["x_bins"] = [binnings_settings.binnings_dict["binningHtt13TeV_"+category+"_m_sv"]]
					if "TTbarCR" in category and channel == "ttbar":
						config["x_expressions"] = ["m_vis"]
						config["x_bins"] = [binnings_settings.binnings_dict["binningHtt13TeV_"+category+"_m_vis"]]
					
					# Use 2d plots for 2d categories
					if "ZeroJet2D" in category and not ("WJCR" in category or "QCDCR" in category):
						config["x_expressions"] = ["m_vis"]
						config["x_bins"] = [binnings_settings.binnings_dict["binningHtt13TeV_"+category+"_m_vis"]]
						if channel in ["mt", "et"]:
							config["y_expressions"] = ["decayMode_2"]
							config["y_bins"] = [binnings_settings.binnings_dict["binningHtt13TeV_"+category+"_decayMode_2"]]
						elif channel == "em":
							config["y_expressions"] = ["pt_2"]
							config["y_bins"] = [binnings_settings.binnings_dict["binningHtt13TeV_"+category+"_pt_2"]]
						elif channel == "tt":
							config["x_expressions"] = ["m_sv"]
							config["x_bins"] = [binnings_settings.binnings_dict["binningHtt13TeV_"+category+"_m_sv"]]
					elif "Boosted2D" in category and not ("WJCR" in category or "QCDCR" in category or "dijet" in category):
						config["x_expressions"] = ["m_vis"] if channel == "mm" else ["m_sv"]
						config["y_expressions"] = ["H_pt"]
						config["x_bins"] = [binnings_settings.binnings_dict["binningHtt13TeV_"+category+("_m_vis" if channel == "mm" else "_m_sv")]]
						config["y_bins"] = [binnings_settings.binnings_dict["binningHtt13TeV_"+category+"_H_pt"]]
					elif ("Vbf2D" in category or "Vbf3D" in category) and not "QCDCR" in category:
						config["x_expressions"] = ["m_vis"] if channel == "mm" else ["m_sv"]
						
						config["x_bins"] = [binnings_settings.binnings_dict["binningHtt13TeV_"+category+("_m_vis" if channel == "mm" else "_m_sv")]]
						if ("Vbf3D_CP_jdeta" in category):
							config["y_expressions"] = ["jdeta"]
							config["y_bins"] = [binnings_settings.binnings_dict["binningHtt13TeV_"+category+"_jdeta"]]
						else:
							config["y_expressions"] = ["mjj"]	
							config["y_bins"] = [binnings_settings.binnings_dict["binningHtt13TeV_"+category+"_mjj"]]
						
						if "Vbf3D" in category and channel != "mm" and "mela" not in category:
							config["z_expressions"] = ["jdphi"]
							config["z_bins"] = [binnings_settings.binnings_dict["binningHtt13TeV_"+category+"_jdphi"]]
						if "Vbf3D" in category and channel != "mm" and "mela" in category:
							config["z_expressions"] = ["melaDiscriminatorD0MinusGGH"]
							config["z_bins"] = [binnings_settings.binnings_dict["binningHtt13TeV_"+category+"_melaDiscriminatorD0MinusGGH"]]
							
                    
					elif (binnings_key in binnings_settings.binnings_dict) and args.x_bins == None:
						# print(binnings_key)
						config["x_bins"] = [binnings_key]
					elif args.x_bins != None:
						config["x_bins"] = [args.x_bins]
					else:
						log.fatal("binnings key " + binnings_key + " not found in binnings_dict! Available binnings are (see HiggsAnalysis/KITHiggsToTauTau/python/plotting/configs/binnings.py):")
						for key in binnings_settings.binnings_dict:
							log.debug(key)
						sys.exit()
					
					# set quantity x depending on the category
					if args.cp_study == "final":
						if all(["RHOmethod" in c for c in categories]):
							config["x_expressions"] = ["recoPhiStarCP_rho_merged"]
							args.quantity = "recoPhiStarCP_rho_merged"
						elif all(["COMBmethod" in c for c in categories]):
							config["x_expressions"] = ["recoPhiStarCPCombMerged"]
							args.quantity = "recoPhiStarCPCombMerged"
						else:
							log.fatal("YOU SHALL NOT PASS different types of category (COMB and RHO) to the same channel. Repeat the channel for the each type of category.")
							raise ValueError("You shall not pass different types of category (COMB and RHO) to the same channel. Repeat the channel for the each type of category.")

					# Unroll 2d distribution to 1d in order for combine to fit it
					if ("2D" in category or "3D" in category) and not ("WJCR" in category or "QCDCR" in category) and not (channel == "tt" and "ZeroJet2D" in category):
						if not "UnrollHistogram" in config.get("analysis_modules", []):
							config.setdefault("analysis_modules", []).append("UnrollHistogram")
						config["unroll_ordering"] = "zyx"

					config["directories"] = [args.input_dir]
					
					histogram_name_template = bkg_histogram_name_template if nominal else bkg_syst_histogram_name_template
					config["labels"] = [histogram_name_template.replace("$", "").format(
							PROCESS=datacards.configs.sample2process(sample),
							BIN=official_category,
							SYSTEMATIC=systematic
					) for sample in config["labels"]]
					
					tmp_output_file = os.path.join(args.output_dir, tmp_input_root_filename_template.replace("$", "").format(
							ANALYSIS="htt",
							CHANNEL=channel,
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
					plot_configs.append(config)		
			
			hadd_commands.append("hadd -f {DST} {SRC} && rm {SRC}".format(
					DST=output_file,
					SRC=" ".join(tmp_output_files)
			))
			merged_output_files.append(output_file)
			
	if log.isEnabledFor(logging.DEBUG):
		pprint.pprint(plot_configs) 
		
	# delete existing output files
	tmp_output_files = list(set([os.path.join(config["output_dir"], config["filename"]+".root") for config in plot_configs[:args.n_plots[0]]]))
	for output_file_iterator in tmp_output_files:
		if os.path.exists(output_file_iterator):
			os.remove(output_file_iterator)
			log.debug("Removed file \""+output_file_iterator+"\" before it is recreated again.")
	output_files = list(set(output_files))

	# create input histograms with HarryPlotter
	if "inputs" in args.steps:
		log.info("\n -------------------------------------- Creating input histograms with HarryPlotter ---------------------------------")
		higgsplot.HiggsPlotter(list_of_config_dicts=plot_configs, list_of_args_strings=[args.args], n_processes=args.n_processes, n_plots=args.n_plots[0], batch=args.batch)
	
	if args.n_plots[0] != 0:
		tools.parallelize(_call_command, hadd_commands, n_processes=args.n_processes)
	if args.debug_plots:
		debug_plot_configs = []
		for output_file in merged_output_files:
			debug_plot_configs.extend(plotconfigs.PlotConfigs().all_histograms(output_file, plot_config_template={"markers":["E"], "colors":["#FF0000"]}))
		higgsplot.HiggsPlotter(list_of_config_dicts=debug_plot_configs, list_of_args_strings=[args.args], n_processes=args.n_processes, n_plots=args.n_plots[1])
	if "inputs" in args.steps:
		# update CombineHarvester with the yields and shapes
		log.info("\n -------------------------------------- Extract shapes from histogram templates ---------------------------------")
		datacards.extract_shapes(
				os.path.join(args.output_dir, input_root_filename_template.replace("$", "")),
				bkg_histogram_name_template, sig_histogram_name_template,
				bkg_syst_histogram_name_template, sig_syst_histogram_name_template,
				update_systematics=True
		)
	
	
	# add bin-by-bin uncertainties
	if not args.no_bbb_uncs:
		log.info("\n -------------------------------------- Added bin-by-bin uncertainties ---------------------------------")
		datacards.add_bin_by_bin_uncertainties(
				processes=datacards.cb.cp().backgrounds().process_set(),
				add_threshold=0.1, merge_threshold=0.5, fix_norm=True
		)
	
	# restrict combine to lnN systematics only if no_shape_uncs is set
	if args.no_syst_uncs:
		log.debug("\n -------------------------------------- Deactivate systematic uncertainties ---------------------------------")
		if not args.use_asimov_dataset:
			log.warning("Fitting MC to data without systematic uncertainties can lead to unreasonable results.")
		datacards.cb.FilterSysts(lambda systematic : True)
		if log.isEnabledFor(logging.DEBUG):
			datacards.cb.PrintSysts()

	# scale
	if(args.scale_lumi):
		datacards.scale_expectation( float(args.scale_lumi) / args.lumi)
	
	# TODO: comment out the following two commands if you want to use
	#       the SM HTT data card creation method in CombineHarvester
	# print(datacards.cb.process_set())
	datacards.cb.FilterProcs(remove_procs_and_systs_with_zero_yield)	
	# print(datacards.cb.process_set())	
	
	# Use an asimov dataset. This line must be here, because otherwise we
	if args.use_asimov_dataset:
		log.info("\n -------------------------------------- Using asimov dataset instead of actual data ---------------------------------")
		# signal_processes makes combine filter those signal processes that appear in the datacards and can be replaced.
		# if you observe the error that ROOT wasn't able to add up the background and signal histograms due to unequal binnings
		# the reason is possibly a missing signal_process here.
		datacards.replace_observation_by_asimov_dataset(signal_processes=["ggHsm_htt", "qqHsm_htt", "ggH_htt"])
	
	"""
	This option calculates the yields and signal to background ratio for each channel and category defined -c and --categories.
	It considers the
	"""
	
	# TODO: WIP: More elegant programming style planned.
	if "yields" in args.steps:
		log.info("\n -------------------------------------- Yields ---------------------------------")
		for index, (channel, categories) in enumerate(zip(args.channel, args.categories)):
			categories= [channel + "_" + category for category in categories]
			# prepare category settings based on args and datacards
			categories_save = sorted(categories)
			categories = list(set(categories).intersection(set(datacards.cb.cp().channel([channel]).bin_set())))
			if(categories_save != sorted(categories)):
				log.fatal("CombineHarvester removed the following categories automatically. Was this intended?")
				log.fatal(list(set(categories_save) - set(categories)))
				sys.exit(1)
			
			# restrict CombineHarvester to configured categories:
			datacards.cb.FilterAll(lambda obj : (obj.channel() == channel) and (obj.bin() not in categories))
			for category in categories:
				bkg_yield = {}
				sig_yield = {}
				print("\n"+ "Channel: "+str(channel)+ " Category: "+str(category)+"\n")
				bkg_procs = datacards.cb.cp().channel([channel]).bin([category]).cp().backgrounds().process_set()
				sig_procs = datacards.cb.cp().channel([channel]).bin([category]).cp().signals().process_set()
				for bkg in bkg_procs:
					bkg_yield[bkg] = datacards.cb.cp().channel([channel]).bin([category]).process([bkg]).GetRate()
				tot_bkg = sum(bkg_yield.values())
				for sig in sig_procs:
					sig_yield[sig] = datacards.cb.cp().channel([channel]).bin([category]).process([sig]).GetRate()
				tot_sig = sum(sig_yield.values())
				print("TotalBkg: "+str(tot_bkg)+ " TotalSig: "+str(tot_sig)+"\n")
				for sig in sig_procs:
					print(str(sig)+"/tot_bkg: ", str(sig_yield[sig]/tot_bkg))
					print(str(sig)+"/tot_sig: ", str(sig_yield[sig]/tot_sig))
		
	if args.auto_rebin:
		datacards.auto_rebin(bin_threshold = 1.0, rebin_mode = 0)
	
	# write datacards and call text2workspace
	log.info("\n -------------------------------------- Writing datacards and call text2workspace ---------------------------------")
	datacards_cbs = {}
	for datacard_filename_template in datacard_filename_templates:
		datacards_cbs.update(datacards.write_datacards(
				datacard_filename_template.replace("{", "").replace("}", ""),
				output_root_filename_template.replace("{", "").replace("}", ""),
				args.output_dir
		))
	datacards_poi_ranges = {}
	for datacard, cb in datacards_cbs.iteritems():
		channels = cb.channel_set()
		categories = cb.bin_set()
		if len(channels) == 1:
			if len(categories) == 1:
				datacards_poi_ranges[datacard] = [-100.0, 100.0]
			else:
				datacards_poi_ranges[datacard] = [-50.0, 50.0]
		else:
			if len(categories) == 1:
				datacards_poi_ranges[datacard] = [-50.0, 50.0]
			else:
				datacards_poi_ranges[datacard] = [-25.0, 25.0]
		
	if "likelihoodScan" in args.steps:
		log.info("\n -------------------------------------- Likelihood scan ---------------------------------")
		log.info("\n -------------------------------------- Text2Workspace ---------------------------------")
		datacards_workspaces_cp_mixing_angle = datacards.text2workspace(
				datacards_cbs,
				args.n_processes,
				" -P {MODEL} {MODEL_PARAMETERS} ".format(
					MODEL="HiggsAnalysis.KITHiggsToTauTau.datacards.cpmodels_old:cp_mixing",
					MODEL_PARAMETERS=""
				),
				higgs_mass="125"
		)
		
		if "prefitpostfitplots" in args.steps:
			log.info("\n -------------------------------------- Prefit Postfit plots ---------------------------------")
			datacards.combine(datacards_cbs, datacards_workspaces_cp_mixing_angle, datacards_poi_ranges, args.n_processes, "-M FitDiagnostics "+datacards.stable_options+" -n \"\"", higgs_mass="125")
			datacards_postfit_shapes = datacards.postfit_shapes_fromworkspace(datacards_cbs, datacards_workspaces_cp_mixing_angle, False, args.n_processes, "--sampling" + (" --print" if args.n_processes <= 1 else ""), higgs_mass="125")
			
			# divide plots by bin width and change the label correspondingly
			if args.quantity == "m_sv" and not(do_not_normalize_by_bin_width):
				args.args += " --y-label 'dN / dm_{#tau #tau}  (1 / GeV)'"
		
			# adapt prefit and postfit plot configs
			backgrounds_to_merge = {
				"ZLL" : ["ZL", "ZJ"],
				"TT" : ["TTT", "TTJJ"],
				"EWK" : ["EWKZ", "VVT", "VVJ", "VV", "W", "hww_gg125", "hww_qq125"]
			}
			
			prefit_postfit_plot_configs = datacards.prefit_postfit_plots(datacards_cbs, datacards_postfit_shapes, plotting_args={"ratio" : args.ratio, "args" : args.args, "lumi" : args.lumi, "normalize" : not(do_not_normalize_by_bin_width), "era" : args.era, "x_expressions" : config["x_expressions"][0], "return_configs" : True, "merge_backgrounds" : backgrounds_to_merge, "add_soverb_ratio" : True}, n_processes=args.n_processes)
			datacards.print_pulls(datacards_cbs, args.n_processes, "-A -p {POI}".format(POI="cpmixing"))
			if "nuisanceimpacts" in args.steps:
				datacards.nuisance_impacts(datacards_cbs, datacards_workspaces_cp_mixing_angle, args.n_processes, higgs_mass="125")
				
			higgsplot.HiggsPlotter(list_of_config_dicts=prefit_postfit_plot_configs, list_of_args_strings=[args.args], n_processes=args.n_processes, n_plots=args.n_plots[1])

  
		# Determine mixing angle parameter
		datacards.combine(
				datacards_cbs,
				datacards_workspaces_cp_mixing_angle,
				None,
				args.n_processes,
				"-M MultiDimFit --algo grid --redefineSignalPOIs cpmixing --expectSignal=1 -t -1 --setParameters cpmixing=0.0,muF=1.0,muV=1.0 --points {POINTS} {STABLE} -n \"\"".format( # -n \"cp_mixing_angle\"
						STABLE=datacards.stable_options,
						POINTS=args.cp_mixing_scan_points
        ),
				higgs_mass="125"
		)		
		datacards.plot1DScan(datacards_cbs, 
			datacards_workspaces_cp_mixing_angle, 
			"cpmixing", 
			args.n_processes, 
			"",
			higgs_mass="125")
	
	"""
	Pvalue determination to be modified. Treating the mixing angle as MASS the file pattern does not work anymore.
	"""	 	
		# custom physics model
		# datacards_workspaces = datacards.text2workspace(
		# 		datacards_cbs,
		# 		args.n_processes,
		# 		"-P {MODEL} {MODEL_PARAMETERS}".format(
		# 			MODEL="HiggsAnalysis.KITHiggsToTauTau.datacards.higgsmodels:HiggsCPI",
		# 			MODEL_PARAMETERS=""
		# 		)
		# )
	
	#annotation_replacements = {channel : index for (index, channel) in enumerate(["combined", "tt", "mt", "et", "em"])}
	# Max. likelihood fit and postfit plots
	
	#datacards.annotate_trees(
			#datacards_workspaces,
			#"higgsCombine*MaxLikelihoodFit*mH*.root",
			#[[os.path.join(os.path.dirname(template.replace("${CHANNEL}", "(.*)").replace("${MASS}", "\d*")), ".*.root") for template in datacard_filename_templates if "channel" in template][0]],
			#annotation_replacements,
			#args.n_processes,
			#None,
			#"-t limit -b channel"
	#)
	#datacards.annotate_trees(
			#datacards_workspaces,
			#"higgsCombine*MaxLikelihoodFit*mH*.root",
			#[[os.path.join(os.path.dirname(template.replace("combined", "(combined)").replace("${MASS}", "\d*")), ".*.root") for template in datacard_filename_templates if "combined" in template][0]],
			#annotation_replacements,
			#args.n_processes,
			#None,
			#"-t limit -b channel"
	#)

	# Asymptotic limits
	if "pvalue" in args.steps:	
		# Physics model used for H->ZZ spin/CP studies
		# https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit/blob/74x-root6/python/HiggsJPC.py
		datacards_workspaces_twoHypothesisHiggs = datacards.text2workspace(
				datacards_cbs,
				args.n_processes,
				"-P {MODEL} {MODEL_PARAMETERS}".format(
					MODEL="HiggsAnalysis.KITHiggsToTauTau.datacards.higgsmodels:twoHypothesisHiggs",
					MODEL_PARAMETERS=("--PO altSignal=ps --PO ignoreSignal=mm "+("--PO=muFloating" if args.use_shape_only else ""))
				)
		)
				
		datacards.combine(datacards_cbs, datacards_workspaces_twoHypothesisHiggs, None, args.n_processes, " -M HybridNew --testStat=TEV --saveHybridResult --generateNuis=0 --singlePoint 1  --fork 8 -T 20000 -i 1 --clsAcc 0 --fullBToys --generateExt=1 -n \"\"") # TODO: change to HybridNew in the old: --expectSignal=1 -t -1
		#-M HybridNew --testStat=TEV --generateExt=1 --generateNuis=0 fixedMu.root --singlePoint 1 --saveHybridResult --fork 40 -T 1000 -i 1 --clsAcc 0 --fullBToys

		#datacards.combine(datacards_cbs, datacards_workspaces_twoHypothesisHiggs, None, args.n_processes, "-M ProfileLikelihood -t -1 --expectSignal 1 --toysFrequentist --significance -s %s\"\""%index) # TODO: maybe this can be used to get p-values
		if "prefitpostfitplots" in args.steps:
			datacards_postfit_shapes = datacards.postfit_shapes_fromworkspace(datacards_cbs, datacards_workspaces_twoHypothesisHiggs, False, args.n_processes, "--sampling" + (" --print" if args.n_processes <= 1 else ""))
			datacards.prefit_postfit_plots(datacards_cbs, datacards_postfit_shapes, plotting_args={"ratio" : args.ratio, "args" : args.args, "lumi" : args.lumi, "x_expressions" : args.quantity, "normalize" : not(args.do_not_normalize_by_bin_width), "era" : args.era}, n_processes=args.n_processes,signal_stacked_on_bkg=True)
			datacards.print_pulls(datacards_cbs, args.n_processes, "-A -p {POI}".format(POI="x") )
			if "nuisanceimpacts" in args.steps:
				datacards.nuisance_impacts(datacards_cbs, datacards_workspaces_twoHypothesisHiggs, args.n_processes)
				
		datacards_hypotestresult=datacards.hypotestresulttree(datacards_cbs, n_processes=args.n_processes, poiname="x" )
		log.info(datacards_hypotestresult)
		if args.use_shape_only:
			datacards.combine(datacards_cbs, datacards_workspaces_twoHypothesisHiggs, None, args.n_processes, " -M HybridNew --testStat=TEV --saveHybridResult --generateNuis=0 --singlePoint 1  --fork 8 -T 20000 -i 1 --clsAcc 0 --fullBToys --generateExt=1 -n \"\"")
		# TODO: I think this line should be deleted.
		pconfig_plots=[]
		for filename in datacards_hypotestresult.values():
			log.info(filename)
			pconfigs={}
			pconfigs["files"]= [filename]
			pconfigs["nicks"]= ["noplot","alternative_hypothesis","null_hypothesis", "q_obs"]
			pconfigs["tree_draw_options"]=["","","","TGraph"]
			#pconfigs[ "marker_sizes"]=[5]
			#pconfigs["marker_styles"]=[34]
			pconfigs[ "markers"]=["line","line","line"]

			pconfigs["y_expressions"]=["None","None","None","0"]
			pconfigs["folders"]=["q"]
			pconfigs["weights"]=["1","type<0","type>0","type==0"]
			pconfigs["x_expressions"]=["q"]
			pconfigs[ "output_dir"]=str(os.path.dirname(filename))
			pconfigs["x_bins"]=["500,-3.15,3.15"]
			if args.cp_study == "final":
				pconfigs["x_bins"] = ["500,0,6.28"]

			#pconfigs["scale_factors"]=[1,1,1,900]
			#pconfig["plot_modules"] = ["ExportRoot"]

			pconfigs["analysis_modules"]=["PValue"]
			pconfigs["p_value_alternative_hypothesis_nicks"]=["alternative_hypothesis"]
			pconfigs["p_value_null_hypothesis_nicks"]=["null_hypothesis"]
			pconfigs["p_value_observed_nicks"]=["q_obs"]
			pconfigs["legend"]=[0.7,0.6,0.9,0.88]
			pconfigs["labels"]=["CP-even", "CP-odd", "observed"]
			pconfig_plots.append(pconfigs)
			if args.cp_study == "final":
				if "susycpodd" or "cpodd" in args.hypothesis:
					pconfigs["labels"]=["CP-even", "CP-odd", "observed"]
					if args.use_asimov_dataset:
						pconfigs["labels"]=["CP-even", "CP-odd", "asimov"]
				if "cpmix" in args.hypothesis:
					pconfigs["labels"]=["CP-even", "CP-mix", "observed"]
					if args.use_asimov_dataset:
						pconfigs["labels"]=["CP-even", "CP-mix", "asimov"]
			higgsplot.HiggsPlotter(list_of_config_dicts=pconfig_plots, list_of_args_strings=[args.args], n_processes=args.n_processes)
