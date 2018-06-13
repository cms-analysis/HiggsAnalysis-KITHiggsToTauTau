#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import argparse
import copy
import glob
import os
import re
import shlex
import sys

import CombineHarvester.CombineTools.ch as ch

import Artus.Utility.tools as tools
import Artus.HarryPlotter.utility.plotconfigs as plotconfigs

import HiggsAnalysis.KITHiggsToTauTau.plotting.higgsplot as higgsplot
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.samples_run2_2016 as samples
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.binnings as binnings
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.systematics_run2 as systematics
#import HiggsAnalysis.KITHiggsToTauTau.datacards.smhttdatacards as smhttdatacards
import HiggsAnalysis.KITHiggsToTauTau.datacards.finalstatecpstudiesdatacards as finalstatecpstudiesdatacards
import HiggsAnalysis.KITHiggsToTauTau.datacards.datacards as datacards_module


"""
	Script to create ROOT inputs and datacards for the Higgs-boson CP studies in the final state.
"""

# At the moment, the script is setup to work only with the CP rho method, i.e. only tt->rhorho channel.
# TODO adapt script for also combined method and ip method, i.e. adjust categories and so on.
# The categories are the same ones used in the SM Htautau analysis.


def _call_command(command):
	log.debug(command)
	logger.subprocessCall(command, shell=True)


def official2private(category, category_replacements):
	result = copy.deepcopy(category)
	for official, private in category_replacements.iteritems():
		result = re.sub(official+"$", private, result)
	return result

def private2official(category, category_replacements):
	result = copy.deepcopy(category)
	for official, private in category_replacements.iteritems():
		result = re.sub(private+"$", official, result)
	return result

def is_control_region(obj):
	return ("WJCR" in obj.bin() or "QCDCR" in obj.bin() or "TTbarCR" in obj.bin() or obj.channel() == "mm")

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

	parser = argparse.ArgumentParser(description="Create ROOT inputs and datacards for Higgs-boson CP studies in the final state.",
	                                 parents=[logger.loggingParser])

	parser.add_argument("-i", "--input-dir", required=True,
	                    help="Input directory.")
	parser.add_argument("-c", "--channel", action = "append", default=["all"],
	                    help="Channel. This argument can be set multiple times. [Default: %(default)s]")
	parser.add_argument("--categories", nargs="+", action = "append", default=[["all"]] * len(parser.get_default("channel")),
	                    help="Categories per channel. This argument needs to be set as often as --channels. [Default: %(default)s]")
	parser.add_argument("-x", "--quantity", default="0",
	                    help="Quantity. [Default: %(default)s]")
	parser.add_argument("-m", "--higgs-masses", nargs="+", default=["125"],
	                    help="Higgs masses. [Default: %(default)s]")
	parser.add_argument("-w", "--weight", default="1.0",
	                    help="Additional weight (cut) expression. [Default: %(default)s]")
	parser.add_argument("--cp-study", default="rhometh",
	                    help="Choose which CP study to do. [Default: %(default)s]")
	parser.add_argument("--hypothesis", nargs="+", default=["susycpodd"],
	                    help="Choose the hypothesis to test against CPeven hypothesis. [Default: %(default)s]")
	parser.add_argument("-a", "--args", default="",
	                    help="Additional arguments for HarryPlotter. [Default: %(default)s]")
	parser.add_argument("--no-bbb-uncs", action="store_true", default=False,
	                    help="Do not add bin-by-bin uncertainties. [Default: %(default)s]")
	parser.add_argument("--auto-rebin", action="store_true", default=False,
	                    help="Do auto rebinning [Default: %(default)s]")
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
	parser.add_argument("--only-config", action="store_true", default=False,
					    help="Only build configs and terminate after that. For debug purposes. [Default: %(default)s]")
	parser.add_argument("-n", "--n-processes", type=int, default=1,
	                    help="Number of (parallel) processes. [Default: %(default)s]")
	parser.add_argument("-f", "--n-plots", type=int, nargs=2, default=[None, None],
	                    help="Number of plots for datacard inputs (1st arg) and for postfit plots (2nd arg). [Default: all]")
	parser.add_argument("-o", "--output-dir", default="$CMSSW_BASE/src/CombineHarvester/HTTSM2016/", #default="$CMSSW_BASE/src/plots/htt_datacards/",
	                    help="Output directory. [Default: %(default)s]")
	parser.add_argument("--output-plots-dir", default="$CMSSW_BASE/src/plots/htt_datacards/",
	                    help="Output directory for the prefit/postfit plots. [Default: %(default)s]")
	parser.add_argument("--output-suffix", default="RWTH",
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
	parser.add_argument("--no-shape-uncs", default=False, action="store_true",
	                    help="Do not include shape-uncertainties. [Default: %(default)s]")
	parser.add_argument("--use-asimov-dataset", action="store_true", default=False,
	                    help="Use s+b expectation as observation instead of real data. [Default: %(default)s]")
	parser.add_argument("--x-bins", default=None,
	                    help="Manually set the binning. Default is taken from configuration files.")
	parser.add_argument("--do-not-ignore-category-removal", default=False, action="store_true",
	                    help="Exit program in case categories are removed from CH. [Default: %(default)s]")
	parser.add_argument("--no-ewkz-as-dy", default=True, action="store_true",
	                    help="Do not include EWKZ samples in inputs for DY. [Default: %(default)s]")
	parser.add_argument("--no-jec-unc-split", default=False, action="store_true",
	                    help="Do not split JEC uncertainties into the 27 different sources but use the envelope instead. [Default: %(default)s]")
	parser.add_argument("--ttbar-fit", action="store_true", default=False,
	                    help="Use rate parameter to propagate ttbar normalization from control region to all categories. [Default: %(default)s]")
	parser.add_argument("--mm-fit", action="store_true", default=False,
	                    help="Use rate parameter to propagate zll normalization from mm control region to all categories. [Default: %(default)s]")
	parser.add_argument("--plot-nuisance-impacts", action="store_true", default=False,
	                    help="Produce nuisance impact plots. [Default: %(default)s]")
	# TODO: to be removed?
	parser.add_argument("--steps", nargs="+", default=["inputs", "t2w", "likelihoodscan"],
	                    choices=["inputs", "t2w", "likelihoodscan", "prefitpostfitplots"],
	                    help="Steps to perform.[Default: %(default)s]\n 'inputs': Writes datacards and fills them using HP.\n 't2w': Create ws.root files form the datacards. 't2w': Perform likelihood scans for various physical models and plot them.")
	parser.add_argument("--for-dcsync", action="store_true", default=False,
	                    help="Produces simplified datacards for the synchronization exercise. [Default: %(default)s]")
	parser.add_argument("--new-tau-id", default=False, action="store_true",
	                    help="Use rerun tau Id instead of nominal one. [Default: %(default)s]")

	
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
	
	
	# the old init folder needs to be deleted to again run the script
	args.output_dir = os.path.abspath(os.path.expandvars(args.output_dir))
	if args.clear_output_dir and os.path.exists(os.path.join(args.output_dir, "init")):
		logger.subprocessCall("rm -r " + os.path.join(args.output_dir, "init"), shell=True)
	if args.clear_output_dir and os.path.exists(os.path.join(args.output_dir, "shapes/", args.output_suffix)):
		logger.subprocessCall("rm -r " + os.path.join(args.output_dir, "shapes/", args.output_suffix), shell=True)
	if args.clear_output_dir and os.path.exists(os.path.join(args.output_dir, "output/", args.output_suffix)):
		logger.subprocessCall("rm -r " + os.path.join(args.output_dir, "output/", args.output_suffix), shell=True)
	

	# initialisations for plotting
	sample_settings = samples.Samples()
	binnings_settings = binnings.BinningsDict()
	systematics_factory = systematics.SystematicsFactory()
	
	plot_configs = []
	output_files = []
	merged_output_files = []
	hadd_commands = []
	#signal_processes = []

	#signal_processes.append("smHcpeven")
	#if "susycpodd" in args.hypothesis:
	#	signal_processes.append("susyHcpodd_ALT")
	#else:
	#	log.critical("Invalid hypothesis: " + args.hypothesis)
	#	sys.exit(1)
	
	datacards = None
	category_replacements = {}
	
	# get "official" configuration
	init_directory = os.path.join(args.output_dir, "init")
	command = "MorphingSM2016 --control_region=1 --manual_rebin=false --mm_fit=false --ttbar_fit=false --only_init=" + init_directory
#	init_directory = os.path.join(args.output_dir, "output/{OUTPUT_SUFFIX}/".format(OUTPUT_SUFFIX=args.output_suffix))
#	command = "MorphingSM2016 --control_region=1 --manual_rebin=false --mm_fit=false --ttbar_fit=false {INIT}".format(
#				INIT="--only_init="+os.path.join(init_directory, "init")
#				)
	log.debug(command)
	exit_code = logger.subprocessCall(shlex.split(command))
	assert(exit_code == 0)
	

	init_cb = ch.CombineHarvester()
	for init_datacard in glob.glob(os.path.join(init_directory, "*_*_*_*.txt")):
		init_cb.QuickParseDatacard(init_datacard, "$ANALYSIS_$ERA_$CHANNEL_$BINID_$MASS.txt", False)
	
	datacards = finalstatecpstudiesdatacards.FinalStateCPStudiesDatacards(
			cb=init_cb,
			higgs_masses=args.higgs_masses,
			ttbarFit=args.ttbar_fit,
			mmFit=args.mm_fit,
			year=args.era,
			noJECuncSplit=args.no_jec_unc_split,
			cp_study=args.cp_study
			#signal_processes=signal_processes,
	)



	# sample = function in samples_run2
	# process = process in CH/datacard
	datacards.configs._mapping_process2sample = {
		"data_obs" : "data",
		"ZTT" : "ztt",
		"ZL" : "zl",
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
		#"ggH_htt" : "ggh",
		#"qqH_htt" : "qqh",
		#"WH_htt" : "wh",
		#"ZH_htt" : "zh",
		"ggH_hww" : "hww_gg",
		"qqH_hww" : "hww_qq",
		"smHcpeven" : "httcpeven",
		"susyHcpodd_ALT" : "susycpoddALT",
	}
	
	category_replacements["0jet"] = "ZeroJet2D"
	category_replacements["boosted"] = "Boosted2D"
	category_replacements["vbf"] = "Vbf2D"
	category_replacements["0jet_qcd_cr"] = "ZeroJet2D_QCDCR"
	category_replacements["boosted_qcd_cr"] = "Boosted2D_QCDCR"
	category_replacements["vbf_qcd_cr"] = "Vbf2D_QCDCR"
	category_replacements["all"] = "TTbarCR"
	# only semileptonic channels
	category_replacements["wjets_0jet_cr"] = "ZeroJet2D_WJCR"
	category_replacements["wjets_boosted_cr"] = "Boosted2D_WJCR"
	category_replacements["wjets_vbf_cr"] = "Vbf2D_WJCR"
	category_replacements["antiiso_0jet_cr"] = "ZeroJet2D_QCDCR"
	category_replacements["antiiso_boosted_cr"] = "Boosted2D_QCDCR"
	category_replacements["antiiso_vbf_cr"] = "Vbf2D_QCDCR"
	
	# initialise datacards
	tmp_input_root_filename_template = "shapes/"+args.output_suffix+"/${ANALYSIS}_${CHANNEL}_${BIN}_${SYSTEMATIC}_${ERA}.root"
	input_root_filename_template = "shapes/"+args.output_suffix+"/${ANALYSIS}_${CHANNEL}.inputs-sm-${ERA}-2D.root"
	bkg_histogram_name_template = "${BIN}/${PROCESS}"
	sig_histogram_name_template = "${BIN}/${PROCESS}${MASS}"
	bkg_syst_histogram_name_template = "${BIN}/${PROCESS}_${SYSTEMATIC}"
	sig_syst_histogram_name_template = "${BIN}/${PROCESS}${MASS}_${SYSTEMATIC}"
	datacard_filename_templates = datacards.configs.htt_datacard_filename_templates
	output_root_filename_template = "datacards/common/${ANALYSIS}.input_${ERA}.root"
	#if args.for_dcsync:
	#	output_root_filename_template = "datacards/common/${ANALYSIS}.inputs-sm-${ERA}-2D.root" if args.era == "2016" else "datacards/common/${ANALYSIS}.inputs-sm-${ERA}-mvis.root"
	
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
	
	# used only in semileptonic channels
	categoriesWithRelaxedIsolationForW = [
		"Boosted2D",
		"Vbf2D"
	]
	
	# used only in semileptonic channels
	categoriesWithRelaxedIsolationForQCD = [
		"ZeroJet2D",
		"Boosted2D",
		"Vbf2D"
	]
	
	do_not_normalize_by_bin_width = args.do_not_normalize_by_bin_width

	
	#restriction to requested systematics
	if args.no_shape_uncs:
		datacards.remove_shape_uncertainties()
	
	#restriction to requested masses
	datacards.cb.mass(["*"]+args.higgs_masses)
	
	#restriction to requested channels
	if args.channel != parser.get_default("channel"):
		datacards.cb.channel(args.channel)
	args.channel = datacards.cb.cp().channel_set()
	if args.categories == parser.get_default("categories"):
		args.categories = len(args.channel) * args.categories
	
	

	
	for index, (channel, categories) in enumerate(zip(args.channel, args.categories)):
		#print index, (channel, categories)
		
		if channel in ["em", "ttbar"]:
			datacards.configs._mapping_process2sample["ZL"] = "zll"
		else:
			datacards.configs._mapping_process2sample["ZL"] = "zl"
		
		if channel in ["et", "mt", "tt"]:
			datacards.configs._mapping_process2sample.pop("TT", None)
			datacards.configs._mapping_process2sample["TTT"]= "ttt"
			datacards.configs._mapping_process2sample["TTJ"]= "ttjj"
		else:
			datacards.configs._mapping_process2sample["TT"] = "ttj"
			datacards.configs._mapping_process2sample.pop("TTT")
			datacards.configs._mapping_process2sample.pop("TTJ")
		
		tmp_output_files = []
		output_file = os.path.join(args.output_dir, input_root_filename_template.replace("$", "").format(
				ANALYSIS="htt",
				CHANNEL=channel,
				ERA="13TeV"
		))
		output_files.append(output_file)
		
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
			#print "\t", category, " ", official_category

			datacards_per_channel_category = finalstatecpstudiesdatacards.FinalStateCPStudiesDatacards(cb=datacards.cb.cp().channel([channel]).bin([official_category]))
			
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
				
				datacards_per_channel_category = finalstatecpstudiesdatacards.FinalStateCPStudiesDatacards(cb=datacards.cb.cp().channel([channel]).bin([official_category]))
			
			higgs_masses = [mass for mass in datacards_per_channel_category.cb.mass_set() if mass != "*"]
			

			
#			for shape_systematic, list_of_samples in datacards_per_channel_category.get_samples_per_shape_systematic(lnN_syst=["CMS_ggH_STXSVBF2j", "CMS_ggH_STXSmig01", "CMS_ggH_STXSmig12"]).iteritems():
			for shape_systematic, list_of_samples in datacards_per_channel_category.get_samples_per_shape_systematic(lnN_syst=["CMS_ggH_STXSVBF2j", "CMS_ggH_STXSmig01", "CMS_ggH_STXSmig12"], shape_syst=["CMS_scale_j_RelativePtHF_13TeV", "CMS_scale_j_FlavorQCD_13TeV"]).iteritems():
				#print "\t\t", shape_systematic, list_of_samples

				nominal = (shape_systematic == "nominal")
				list_of_samples = [datacards.configs.process2sample(process) for process in list_of_samples]
				
				# This is needed because wj and qcd are interdependent when using the new background estimation method
				# NB: CH takes care to only use the templates for processes that you specified. This means that any
				#     superfluous histograms created as a result of this problem do not influence the result
				if args.background_method == "new":
					if "qcd" in list_of_samples and "wj" not in list_of_samples:
						list_of_samples += ["wj"]
					elif "wj" in list_of_samples and "qcd" not in list_of_samples:
						list_of_samples += ["qcd"]
				
				for shift_up in ([True] if nominal else [True, False]):
					#print "\t\t\t", shift_up
					
					systematic = "nominal" if nominal else (shape_systematic + ("Up" if shift_up else "Down"))
					
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
					
					# set cut_type
					cut_type=""
					if args.era == "2016":
						if args.cp_study=="rhometh":
							cut_type="cprho2016"
						#elif args.cp_study=="combmeth":
						#	cut_type=="cpcomb2016"
						#elif args.cp_study=="ipmeth":
						#	cut_type=="cpip2016"
					else:
						cut_type=="baseline"

					# prepare plotting configs for retrieving the input histograms
					config = sample_settings.get_config(
							samples=[getattr(samples.Samples, sample) for sample in list_of_samples],
							channel=channel,
							category="catHtt13TeV_"+category,
							weight=args.weight,
							lumi = args.lumi * 1000,
							exclude_cuts=exclude_cuts,
							higgs_masses=higgs_masses,
							#cut_type="smhtt2016" if args.era == "2016" else "baseline",
							cut_type=cut_type,
							estimationMethod=args.background_method,
							ss_os_factor=ss_os_factor,
							wj_sf_shift=wj_sf_shift,
							zmm_cr_factor=zmm_cr_factor,
							no_ewkz_as_dy = args.no_ewkz_as_dy,
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
						if args.new_tau_id:
							weightAtIndex = weightAtIndex.replace("byTightIsolationMVArun2v1DBoldDMwLT", "rerunDiscriminationByIsolationMVAOldDMrun2v1Medium").replace("byMediumIsolationMVArun2v1DBoldDMwLT", "rerunDiscriminationByIsolationMVAOldDMrun2v1Loose").replace("byLooseIsolationMVArun2v1DBoldDMwLT", "rerunDiscriminationByIsolationMVAOldDMrun2v1VLoose")
						config["weights"][index] = weightAtIndex
					config["x_expressions"] = ["m_vis"] if channel == "mm" and args.quantity == "m_sv" else [args.quantity]


					if "2D" not in category:
						binnings_key = "binningHtt13TeV_"+category+"_%s"%args.quantity
						if (binnings_key in binnings_settings.binnings_dict) and args.x_bins == None:
							config["x_bins"] = [binnings_settings.binnings_dict[binnings_key]]
						elif args.x_bins != None:
							config["x_bins"] = [args.x_bins]
						else:
							log.fatal("binnings key " + binnings_key + " not found in binnings_dict!")
							sys.exit(1)
					
	
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
					
	
					# For the moment binning is hardcoded.
					# TODO: optimise categories and define corresponding binning in binnings.py
					tt_binnings_m_sv = "0 95 115 135 155 350"
					tt_binnings_phiStarCP = "10,0.0,6.3"
					# Use 2d plots for 2d categories
					if channel=="tt":
						if ("ZeroJet2D" in category or "Boosted2D" in category or "Vbf2D" in category) and not ("WJCR" in category or "QCDCR" in category):
							config["x_expressions"] = ["recoPhiStarCP_rho_merged"]
							config["x_bins"] = [tt_binnings_phiStarCP]
							config["y_expressions"] = ["m_sv"]
							config["y_bins"] = [tt_binnings_m_sv]
					else:
						log.fatal("The following channel is not yet configured in this script: " + args.channel)
						sys.exit(1)

					#if "ZeroJet2D" in category and not ("WJCR" in category or "QCDCR" in category):
					#	config["x_expressions"] = ["m_sv" if channel == "tt" else "m_vis"]
					#	config["x_bins"] = [binnings_settings.binnings_dict["binningHtt13TeV_"+category+("_m_sv" if channel == "tt" else "_m_vis")]]
					#	if channel in ["mt", "et"]:
					#		config["y_expressions"] = ["decayMode_2"]
					#		config["y_bins"] = [binnings_settings.binnings_dict["binningHtt13TeV_"+category+"_decayMode_2"]]
					#	elif channel == "em":
					#		config["y_expressions"] = ["pt_2"]
					#		config["y_bins"] = [binnings_settings.binnings_dict["binningHtt13TeV_"+category+"_pt_2"]]
					#elif "Boosted2D" in category and not ("WJCR" in category or "QCDCR" in category):
					#	config["x_expressions"] = ["m_vis"] if channel == "mm" else ["m_sv"]
					#	config["y_expressions"] = ["H_pt"]
					#	config["x_bins"] = [binnings_settings.binnings_dict["binningHtt13TeV_"+category+("_m_vis" if channel == "mm" else "_m_sv")]]
					#	config["y_bins"] = [binnings_settings.binnings_dict["binningHtt13TeV_"+category+"_H_pt"]]
					#elif "Vbf2D" in category and not "QCDCR" in category:
					#	config["x_expressions"] = ["m_vis"] if channel == "mm" else ["m_sv"]
					#	config["y_expressions"] = ["mjj"]
					#	config["x_bins"] = [binnings_settings.binnings_dict["binningHtt13TeV_"+category+("_m_vis" if channel == "mm" else "_m_sv")]]
					#	config["y_bins"] = [binnings_settings.binnings_dict["binningHtt13TeV_"+category+"_mjj"]]
					

					# Unroll 2d distribution to 1d in order for combine to fit it
					if "2D" in category and not ("WJCR" in category or "QCDCR" in category):
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
	
			
		hadd_commands.append("hadd -f {DST} {SRC}".format(
				DST=output_file,
				SRC=" ".join(tmp_output_files)
		))
	
	#if log.isEnabledFor(logging.DEBUG):
	#	import pprint
	#	pprint.pprint(plot_configs)
	
	# delete existing output files
	tmp_output_files = list(set([os.path.join(config["output_dir"], config["filename"]+".root") for config in plot_configs[:args.n_plots[0]]]))
	for output_file in tmp_output_files:
		if os.path.exists(output_file):
			os.remove(output_file)
			log.debug("Removed file \""+output_file+"\" before it is recreated again.")
	output_files = list(set(output_files))
	

	# create input histograms with HarryPlotter
	log.info("\n -------------------------------------- Creating input histograms with HarryPlotter ---------------------------------")
	higgsplot.HiggsPlotter(list_of_config_dicts=plot_configs, list_of_args_strings=[args.args], n_processes=args.n_processes, n_plots=args.n_plots[0], batch=args.batch)
	if args.n_plots[0] != 0:
		tools.parallelize(_call_command, hadd_commands, n_processes=args.n_processes)
	if args.debug_plots:
		debug_plot_configs = []
		for output_file in output_files:
			debug_plot_configs.extend(plotconfigs.PlotConfigs().all_histograms(output_file, plot_config_template={"markers":["E"], "colors":["#FF0000"]}))
		higgsplot.HiggsPlotter(list_of_config_dicts=debug_plot_configs, list_of_args_strings=[args.args], n_processes=args.n_processes, n_plots=args.n_plots[1])
	
	# call official script again with shapes that have just been created
	datacards_module._call_command([
			"MorphingSM2016 --output_folder {OUTPUT_SUFFIX} --postfix -2D --control_region=1 --manual_rebin=false --mm_fit=false --ttbar_fit=false --input_folder_tt {OUTPUT_SUFFIX}".format(
			OUTPUT_SUFFIX=args.output_suffix,
			SHAPE_UNCS="--no_shape_systs=true" if args.no_shape_uncs else "",
			),
			args.output_dir
	])
	log.info("\nDatacards have been written to \"%s\"." % os.path.join(os.path.join(args.output_dir, "output/", args.output_suffix)))




	datacards_path = args.output_dir+"/output/"+args.output_suffix+"/tt/125/"
	official_cb = ch.CombineHarvester()
	
	datacards_cbs = {}
	datacards_workspaces = {}

	# push the datacards just created in the official_cb object
	for official_datacard in glob.glob(os.path.join(datacards_path, "*_*_*_*.txt")):
		official_cb.QuickParseDatacard(official_datacard, '$MASS/$ANALYSIS_$CHANNEL_$BINID_$ERA.txt', False)
		
		tmp_datacard = ch.CombineHarvester()
		tmp_datacard.QuickParseDatacard(official_datacard, '$MASS/$ANALYSIS_$CHANNEL_$BINID_$ERA.txt', False)

		# this if statement is needed in order to avoid the creation of workspaces for single CR only
		if int(official_datacard.split("_")[-2]) < 10 and not "ttbar" in official_datacard:
			# fill dicts datacards_cbs and datacards_workspaces
			datacards_cbs[official_datacard] = tmp_datacard.cp()
			datacards_module._call_command([
				"combineTool.py -M T2W -P HiggsAnalysis.CombinedLimit.HiggsJPC:twoHypothesisHiggs -i {DATACARD} -o {OUTPUT} --parallel {N_PROCESSES}".format(
					DATACARD=official_datacard,
					OUTPUT=os.path.splitext(official_datacard)[0]+"_cp.root",
					N_PROCESSES=args.n_processes
					),
					args.output_dir
			])
			datacards_workspaces[official_datacard] = os.path.splitext(official_datacard)[0]+"_cp.root"
	

	# the object datacards is now filled with the datacards created previously
	datacards = finalstatecpstudiesdatacards.FinalStateCPStudiesDatacards(
			cb=official_cb,
			higgs_masses=args.higgs_masses,
			ttbarFit=args.ttbar_fit,
			mmFit=args.mm_fit,
			year=args.era,
			noJECuncSplit=args.no_jec_unc_split,
			cp_study=args.cp_study
	)

	
	# add bin-by-bin uncertainties
	if not args.no_bbb_uncs:
		datacards.add_bin_by_bin_uncertainties(
				processes=datacards.cb.cp().backgrounds().process_set(),
				add_threshold=0.05, merge_threshold=0.8, fix_norm=False
		)
	
	# scale
	if(args.scale_lumi):
		datacards.scale_expectation( float(args.scale_lumi) / args.lumi)
	
	# use asimov dataset for s+b
	if args.use_asimov_dataset:
		datacards.replace_observation_by_asimov_dataset("125")


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

	## create workspaces from the datacards 
	#datacards_module._call_command([
	#		"combineTool.py -M T2W -P HiggsAnalysis.CombinedLimit.HiggsJPC:twoHypothesisHiggs -i output/{OUTPUT_SUFFIX}/tt/* -o ws.root --parallel {N_PROCESSES}".format(
	#		OUTPUT_SUFFIX=args.output_suffix,
	#		N_PROCESSES=args.n_processes
	#		),
	#		args.output_dir
	#]) 
	#log.info("\nWorkspace has been created in \"%s\"." % os.path.join(os.path.join(args.output_dir, "output/{OUTPUT_SUFFIX}/tt/*".format(
	#			OUTPUT_SUFFIX=args.output_suffix
	#			)
	#		))
	#)


	# Max. likelihood fit and prefit/postfit plots
	datacards.combine(datacards_cbs, datacards_workspaces, datacards_poi_ranges, args.n_processes,
		"-M MaxLikelihoodFit "+datacards.stable_options+" -n \"\" -t -1 --setPhysicsModelParameters \"x=1\" ",
		higgs_mass="125"
	)
	datacards_postfit_shapes = datacards.postfit_shapes_fromworkspace(datacards_cbs, datacards_workspaces, False, args.n_processes, "--sampling" + (" --print" if args.n_processes <= 1 else ""), higgs_mass="125")


	# from now on the categories are given with the numbers instead of the name
	# ZeroJet2D = 1
	# Boosted2D = 2
	# Vbf2D = 3

	# adapt prefit and postfit plot configs
	backgrounds_to_merge = {
		"ZLL" : ["ZL", "ZJ"],
		"TT" : ["TTT", "TTJJ"],
		"EWK" : ["EWKZ", "VVT", "VVJ", "VV", "W", "hww_gg125", "hww_qq125"]
	}
	x_tick_labels = {
		"tt_1" : ["0.0-0.63","0.63-1.26","1.26-1.89","1.89-2.52","2.52-3.15","3.15-3.78","3.78-4.41","4.41-5.04","5.04-5.67","5.67-6.3"] * 5,
		"tt_2" : ["0.0-0.63","0.63-1.26","1.26-1.89","1.89-2.52","2.52-3.15","3.15-3.78","3.78-4.41","4.41-5.04","5.04-5.67","5.67-6.3"] * 5,
		"tt_3" : ["0.0-0.63","0.63-1.26","1.26-1.89","1.89-2.52","2.52-3.15","3.15-3.78","3.78-4.41","4.41-5.04","5.04-5.67","5.67-6.3"] * 5
	}
	texts = {
		"tt_1" : ["0 < m_{#tau#tau} < 95 GeV", "95 < m_{#tau#tau} < 115 GeV", "115 < m_{#tau#tau} < 135 GeV", "135 < m_{#tau#tau} < 155 GeV", "155 < m_{#tau#tau} < 350 GeV"],
		"tt_2" : ["0 < m_{#tau#tau} < 95 GeV", "95 < m_{#tau#tau} < 115 GeV", "115 < m_{#tau#tau} < 135 GeV", "135 < m_{#tau#tau} < 155 GeV", "155 < m_{#tau#tau} < 350 GeV"],
		"tt_3" : ["0 < m_{#tau#tau} < 95 GeV", "95 < m_{#tau#tau} < 115 GeV", "115 < m_{#tau#tau} < 135 GeV", "135 < m_{#tau#tau} < 155 GeV", "155 < m_{#tau#tau} < 350 GeV"]
	}
	texts_x = {
		"tt_1" : [0.14, 0.28, 0.42, 0.56, 0.70],
		"tt_2" : [0.14, 0.28, 0.42, 0.56, 0.70],
		"tt_3" : [0.14, 0.28, 0.42, 0.56, 0.70]
	}
	vertical_lines = {
		"tt_1" : [10, 20, 30, 40],
		"tt_2" : [10, 20, 30, 40],
		"tt_3" : [10, 20, 30, 40]
	}
	

	prefit_postfit_plot_configs = datacards.prefit_postfit_plots(datacards_cbs, datacards_postfit_shapes, plotting_args={"ratio" : args.ratio, "args" : args.args, "lumi" : args.lumi, "normalize" : not(do_not_normalize_by_bin_width), "era" : args.era, "x_expressions" : config["x_expressions"][0], "return_configs" : True, "merge_backgrounds" : backgrounds_to_merge, "add_soverb_ratio" : True}, n_processes=args.n_processes)

	
	for plot_config in prefit_postfit_plot_configs:
		
		plot_category = plot_config["filename"].split("_")[-2]
		plot_channel = plot_config["filename"].split("_")[-3]
		# NB: in order for the channel to be displayed in the proper position,
		#     change x_title in plotroot.py from 0.2 to 0.12.
		# NB2: in order for the lumi text to be displayed in the proper position,
		#      adjust the first two arguments of latex.DrawLatex(1-r,1-t+lumiTextOffset*t,lumiText)
		#      in CMS_lumi.py. 0.8875 and 0.94 seem to be ok values.
		# NB3: in order for pdf output to be readable, the following manual changes are needed:
		#      1.) defaultrootstyle.py:
		#           - default_root_style.SetLineWidth(1) (currently line 44)
		#           - default_root_style.SetFrameLineWidth(1) (currently line 49)
		#      2.) plotroot.py:
		#           - line_graph.SetLineWidth(1) (concerns vertical lines, curretnly line 309)
		if ("1" in plot_category or "2" in plot_category or "3" in plot_category) and not ("10" in plot_category or "11" in plot_category or "12" in plot_category):
			plot_config["canvas_width"] = 1800
			plot_config["canvas_height"] = 1000
			plot_config["y_rel_lims"] = [0.5, 10.0] if "--y-log" in args.args else [0.0, 2 if args.ratio else 1.9]
			plot_config["legend"] = [0.895, 0.1, 0.995, 0.8]
			plot_config["legend_cols"] = 1
			plot_config["x_label"] = "#varphi^{*}_{CP} / rad"
			plot_config["y_label"] = "Events/bin"
			plot_config["formats"] = ["pdf", "png"]
			plot_config["y_title_offset"] = 0.8
			plot_config["y_subplot_title_offset"] = 0.31
			plot_config["left_pad_margin"] = 0.1
			plot_config["right_pad_margin"] = 0.11
			plot_config["line_widths"] = [3]
			plot_config["x_tick_labels"] = x_tick_labels[plot_channel+"_"+plot_category]
			plot_config["texts"] = texts[plot_channel+"_"+plot_category]
			plot_config["texts_x"] = texts_x[plot_channel+"_"+plot_category]
			plot_config["texts_y"] = list((0.8 for i in range(len(plot_config["texts"]))))
			plot_config["texts_size"] = [0.02]
			plot_config["x_labels_vertical"] = True
			plot_config["x_title_offset"] = 1.8
			plot_config["bottom_pad_margin"] = 0.5
			plot_config["vertical_lines"] = vertical_lines[plot_channel+"_"+plot_category]
			plot_config["subplot_lines"] = vertical_lines[plot_channel+"_"+plot_category]

	higgsplot.HiggsPlotter(list_of_config_dicts=prefit_postfit_plot_configs, list_of_args_strings=[args.args], n_processes=args.n_processes, n_plots=args.n_plots[1])





	sys.exit(0)
	

	




########################### as done in SM script
	
	# update CombineHarvester with the yields and shapes
	datacards.extract_shapes(
			os.path.join(args.output_dir, input_root_filename_template.replace("$", "")),
			bkg_histogram_name_template, sig_histogram_name_template,
			bkg_syst_histogram_name_template, sig_syst_histogram_name_template,
			update_systematics=True
	)
	
	# add bin-by-bin uncertainties
	if not args.no_bbb_uncs:
		datacards.add_bin_by_bin_uncertainties(
				processes=datacards.cb.cp().backgrounds().process_set(),
				add_threshold=0.05, merge_threshold=0.8, fix_norm=False
		)
	
	# scale
	if(args.scale_lumi):
		datacards.scale_expectation( float(args.scale_lumi) / args.lumi)
	

	# normalize DM systematic templates to the nominal one in order to get a pure shape systematic
	#datacards.cb.cp().channel(["mt", "et"]).ForEachSyst(lambda systematic: systematic.set_value_u(1 if "tauDMReco" in systematic.name() else systematic.value_u()))
	#datacards.cb.cp().channel(["mt", "et"]).ForEachSyst(lambda systematic: systematic.set_value_d(1 if "tauDMReco" in systematic.name() else systematic.value_d()))
	
	# TODO: comment out the following two commands if you want to use
	#       the SM HTT datacard creation method in CombineHarvester

	## remove processes with zero yield
	#datacards.cb.FilterProcs(remove_procs_and_systs_with_zero_yield)
	#
	## convert shapes in control regions to lnN
	#datacards.cb.cp().ForEachSyst(lambda systematic: systematic.set_type("lnN") if is_control_region(systematic) and systematic.type() == "shape" else systematic.set_type(systematic.type()))
	
	# use asimov dataset for s+b
	if args.use_asimov_dataset:
		datacards.replace_observation_by_asimov_dataset("125")

	if args.auto_rebin:
		datacards.auto_rebin(bin_threshold = 1.0, rebin_mode = 0)

	# write datacards and call text2workspace
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
	
	datacards_workspaces = datacards.text2workspace(datacards_cbs, n_processes=args.n_processes)
	
	if not args.for_dcsync:
		#annotation_replacements = {channel : index for (index, channel) in enumerate(["combined", "tt", "mt", "et", "em"])}
		
		# Max. likelihood fit and postfit plots
		datacards.combine(datacards_cbs, datacards_workspaces, datacards_poi_ranges, args.n_processes, "-M MaxLikelihoodFit "+datacards.stable_options+" -n \"\"")
		#datacards.nuisance_impacts(datacards_cbs, datacards_workspaces, args.n_processes)
		datacards_postfit_shapes = datacards.postfit_shapes_fromworkspace(datacards_cbs, datacards_workspaces, False, args.n_processes, "--sampling" + (" --print" if args.n_processes <= 1 else ""))
	
		# divide plots by bin width and change the label correspondingly
		#if args.quantity == "m_sv" and not(do_not_normalize_by_bin_width):
		#	args.args += " --y-label 'dN / dm_{#tau #tau}  (1 / GeV)'"
	
		# adapt prefit and postfit plot configs
		backgrounds_to_merge = {
			"ZLL" : ["ZL", "ZJ"],
			"TT" : ["TTT", "TTJJ"],
			"EWK" : ["EWKZ", "VVT", "VVJ", "VV", "W", "hww_gg125", "hww_qq125"]
		}
		x_tick_labels = {
			"tt_ZeroJet2D" : ["0.0-0.63","0.63-1.26","1.26-1.89","1.89-2.52","2.52-3.15","3.15-3.78","3.78-4.41","4.41-5.04","5.04-5.67","5.67-6.3"] * 5,
			"tt_Boosted2D" : ["0.0-0.63","0.63-1.26","1.26-1.89","1.89-2.52","2.52-3.15","3.15-3.78","3.78-4.41","4.41-5.04","5.04-5.67","5.67-6.3"] * 5,
			"tt_Vbf2D" : ["0.0-0.63","0.63-1.26","1.26-1.89","1.89-2.52","2.52-3.15","3.15-3.78","3.78-4.41","4.41-5.04","5.04-5.67","5.67-6.3"] * 5
			#"mt_ZeroJet2D" : ["0-60","60-65","65-70","70-75","75-80","80-85","85-90","90-95","95-100","100-105","105-110","110-400"] * 3,
			#"et_ZeroJet2D" : ["0-60","60-65","65-70","70-75","75-80","80-85","85-90","90-95","95-100","100-105","105-110","110-400"] * 3,
			#"em_ZeroJet2D" : ["0-50","50-55", "55-60","60-65","65-70","70-75","75-80","80-85","85-90","90-95","95-100","100-400"] * 3,
			#"mt_Boosted2D" : ["0-80","80-90","90-100","100-110","110-120","120-130","130-140","140-150","150-160","160-300"] * 6,
			#"et_Boosted2D" : ["0-80","80-90","90-100","100-110","110-120","120-130","130-140","140-150","150-160","160-300"] * 6,
			#"em_Boosted2D" : ["0-80","80-90","90-100","100-110","110-120","120-130","130-140","140-150","150-160","160-300"] * 6,
			#"tt_Boosted2D" : ["0-40","40-60","60-70","70-80","80-90","90-100","100-110","110-120","120-130","130-150","150-200","200-250"] * 4,
			#"mt_Vbf2D" : ["0-95","95-115","115-135","135-155","155-400"] * 4,
			#"et_Vbf2D" : ["0-95","95-115","115-135","135-155","155-400"] * 4,
			#"em_Vbf2D" : ["0-95","95-115","115-135","135-155","155-400"] * 4,
			#"tt_Vbf2D" : ["0-40","40-60","60-70","70-80","80-90","90-100","100-110","110-120","120-130","130-150","150-200","200-250"] * 4
		}
		texts = {
			"tt_ZeroJet2D" : ["0 < m_{#tau#tau} < 95 GeV", "95 < m_{#tau#tau} < 115 GeV", "115 < m_{#tau#tau} < 135 GeV", "135 < m_{#tau#tau} < 155 GeV", "155 < m_{#tau#tau} < 350 GeV"],
			"tt_Boosted2D" : ["0 < m_{#tau#tau} < 95 GeV", "95 < m_{#tau#tau} < 115 GeV", "115 < m_{#tau#tau} < 135 GeV", "135 < m_{#tau#tau} < 155 GeV", "155 < m_{#tau#tau} < 350 GeV"],
			"tt_Vbf2D" : ["0 < m_{#tau#tau} < 95 GeV", "95 < m_{#tau#tau} < 115 GeV", "115 < m_{#tau#tau} < 135 GeV", "135 < m_{#tau#tau} < 155 GeV", "155 < m_{#tau#tau} < 350 GeV"]
			#"mt_ZeroJet2D" : ["h^{#pm}", "h^{#pm}#pi^{0}", "h^{#pm}h^{#pm}h^{#mp}"],
			#"et_ZeroJet2D" : ["h^{#pm}", "h^{#pm}#pi^{0}", "h^{#pm}h^{#pm}h^{#mp}"],
			#"em_ZeroJet2D" : ["15 < p_{T}(#mu) < 25 GeV", "25 < p_{T}(#mu) < 35 GeV", "p_{T}(#mu) > 35 GeV"],
			#"mt_Boosted2D" : ["0 < p_{T}^{#tau#tau} < 100 GeV", "100 < p_{T}^{#tau#tau} < 150 GeV", "150 < p_{T}^{#tau#tau} < 200 GeV", "200 < p_{T}^{#tau#tau} < 250 GeV", "250 < p_{T}^{#tau#tau} < 300 GeV", "p_{T}^{#tau#tau} > 300 GeV"],
			#"et_Boosted2D" : ["0 < p_{T}^{#tau#tau} < 100 GeV", "100 < p_{T}^{#tau#tau} < 150 GeV", "150 < p_{T}^{#tau#tau} < 200 GeV", "200 < p_{T}^{#tau#tau} < 250 GeV", "250 < p_{T}^{#tau#tau} < 300 GeV", "p_{T}^{#tau#tau} > 300 GeV"],
			#"em_Boosted2D" : ["0 < p_{T}^{#tau#tau} < 100 GeV", "100 < p_{T}^{#tau#tau} < 150 GeV", "150 < p_{T}^{#tau#tau} < 200 GeV", "200 < p_{T}^{#tau#tau} < 250 GeV", "250 < p_{T}^{#tau#tau} < 300 GeV", "p_{T}^{#tau#tau} > 300 GeV"],
			#"tt_Boosted2D" : ["0 < p_{T}^{#tau#tau} < 100 GeV", "100 < p_{T}^{#tau#tau} < 170 GeV", "170 < p_{T}^{#tau#tau} < 300 GeV", "p_{T}^{#tau#tau} > 300 GeV"],
			#"mt_Vbf2D" : ["300 < m_{jj} < 700 GeV", "700 < m_{jj} < 1100 GeV", "1100 < m_{jj} < 1500 GeV", "m_{jj} > 1500 GeV"],
			#"et_Vbf2D" : ["300 < m_{jj} < 700 GeV", "700 < m_{jj} < 1100 GeV", "1100 < m_{jj} < 1500 GeV", "m_{jj} > 1500 GeV"],
			#"em_Vbf2D" : ["300 < m_{jj} < 700 GeV", "700 < m_{jj} < 1100 GeV", "1100 < m_{jj} < 1500 GeV", "m_{jj} > 1500 GeV"],
			#"tt_Vbf2D" : ["0 < m_{jj} < 300 GeV", "300 < m_{jj} < 500 GeV", "500 < m_{jj} < 800 GeV", "m_{jj} > 800 GeV"]
		}
		texts_x = {
			"tt_ZeroJet2D" : [0.14, 0.28, 0.42, 0.56, 0.70],
			"tt_Boosted2D" : [0.14, 0.28, 0.42, 0.56, 0.70],
			"tt_Vbf2D" : [0.14, 0.28, 0.42, 0.56, 0.70]
			#"mt_ZeroJet2D" : [0.14, 0.4, 0.67],
			#"et_ZeroJet2D" : [0.14, 0.4, 0.67],
			#"em_ZeroJet2D" : [0.2, 0.46, 0.705],
			#"mt_Boosted2D" : [0.17, 0.2975, 0.43, 0.56, 0.6925, 0.81],
			#"et_Boosted2D" : [0.17, 0.2975, 0.43, 0.56, 0.6925, 0.81],
			#"em_Boosted2D" : [0.17, 0.2975, 0.43, 0.56, 0.6925, 0.81],
			#"tt_Boosted2D" : [0.19, 0.38, 0.58, 0.76],
			#"mt_Vbf2D" : [0.19, 0.39, 0.59, 0.76],
			#"et_Vbf2D" : [0.19, 0.39, 0.59, 0.76],
			#"em_Vbf2D" : [0.19, 0.39, 0.59, 0.76],
			#"tt_Vbf2D" : [0.18, 0.38, 0.58, 0.75]
		}
		vertical_lines = {
			"tt_ZeroJet2D" : [10, 20, 30, 40],
			"tt_Boosted2D" : [10, 20, 30, 40],
			"tt_Vbf2D" : [10, 20, 30, 40]
			#"mt_ZeroJet2D" : [12, 24],
			#"et_ZeroJet2D" : [12, 24],
			#"em_ZeroJet2D" : [12, 24],
			#"mt_Boosted2D" : [10, 20, 30, 40, 50],
			#"et_Boosted2D" : [10, 20, 30, 40, 50],
			#"em_Boosted2D" : [10, 20, 30, 40, 50],
			#"tt_Boosted2D" : [12, 24, 36],
			#"mt_Vbf2D" : [5, 10, 15],
			#"et_Vbf2D" : [5, 10, 15],
			#"em_Vbf2D" : [5, 10, 15],
			#"tt_Vbf2D" : [12, 24, 36]
		}
		
		prefit_postfit_plot_configs = datacards.prefit_postfit_plots(datacards_cbs, datacards_postfit_shapes, plotting_args={"ratio" : args.ratio, "args" : args.args, "lumi" : args.lumi, "normalize" : not(do_not_normalize_by_bin_width), "era" : args.era, "x_expressions" : config["x_expressions"][0], "return_configs" : True, "merge_backgrounds" : backgrounds_to_merge, "add_soverb_ratio" : True}, n_processes=args.n_processes)
		for plot_config in prefit_postfit_plot_configs:
			plot_category = plot_config["filename"].split("_")[-1]
			plot_channel = plot_config["title"].split("_")[-1]
			plot_config["output_dir"] = "$CMSSW_BASE/src/plots/htt_datacards/"
			# NB: in order for the channel to be displayed in the proper position,
			#     change x_title in plotroot.py from 0.2 to 0.12.
			# NB2: in order for the lumi text to be displayed in the proper position,
			#      adjust the first two arguments of latex.DrawLatex(1-r,1-t+lumiTextOffset*t,lumiText)
			#      in CMS_lumi.py. 0.8875 and 0.94 seem to be ok values.
			# NB3: in order for pdf output to be readable, the following manual changes are needed:
			#      1.) defaultrootstyle.py:
			#           - default_root_style.SetLineWidth(1) (currently line 44)
			#           - default_root_style.SetFrameLineWidth(1) (currently line 49)
			#      2.) plotroot.py:
			#           - line_graph.SetLineWidth(1) (concerns vertical lines, curretnly line 309)
			if "2D" in plot_category and not ("WJCR" in plot_category or "QCDCR" in plot_category):
					plot_config["canvas_width"] = 1800
					plot_config["canvas_height"] = 1000
					plot_config["y_rel_lims"] = [0.5, 10.0] if "--y-log" in args.args else [0.0, 2 if args.ratio else 1.9]
					plot_config["legend"] = [0.895, 0.1, 0.995, 0.8]
					plot_config["legend_cols"] = 1
					plot_config["x_label"] = "#varphi^{*}_{CP} / rad" #"m_{vis} (GeV)" if "ZeroJet" in plot_category and plot_channel in ["mt", "et", "em"] else "m_{#tau#tau} (GeV)"
					plot_config["y_label"] = "Events/bin"
					plot_config["formats"] = ["pdf", "png"]
					plot_config["y_title_offset"] = 0.6
					plot_config["y_subplot_title_offset"] = 0.31
					plot_config["left_pad_margin"] = 0.1
					plot_config["right_pad_margin"] = 0.11
					plot_config["line_widths"] = [3]
					#if not (plot_channel == "tt" and plot_category == "ZeroJet2D"):
					#	plot_config["x_tick_labels"] = x_tick_labels[plot_channel+"_"+plot_category]
					#	plot_config["texts"] = texts[plot_channel+"_"+plot_category]
					#	plot_config["texts_x"] = texts_x[plot_channel+"_"+plot_category]
					#	plot_config["texts_y"] = list((0.8 for i in range(len(plot_config["texts"]))))
					#	plot_config["texts_size"] = [0.04] if "Boosted2D" in plot_category and plot_channel in ["mt", "et", "em"] else [0.05]
					#	plot_config["x_labels_vertical"] = True
					#	plot_config["x_title_offset"] = 1.5
					#	plot_config["bottom_pad_margin"] = 0.5
					#	plot_config["vertical_lines"] = vertical_lines[plot_channel+"_"+plot_category]
					# now stack signal on top manually
					plot_config["colors"].insert(0, "kRed")
					plot_config["labels"].insert(0, "htt")
					plot_config["legend_markers"].insert(0, "F")
					plot_config["markers"].insert(0, "HIST")
					plot_config["nicks"].insert(0, "HTT")
					plot_config["nicks_whitelist"].insert(0, "HTT")
					plot_config["stacks"].insert(0, "stack")
					plot_config["x_expressions"].insert(0, "TotalSig")
		higgsplot.HiggsPlotter(list_of_config_dicts=prefit_postfit_plot_configs, list_of_args_strings=[args.args], n_processes=args.n_processes, n_plots=args.n_plots[1])
		
		sys.exit(0)

		# create pull plots
		datacards.pull_plots(datacards_postfit_shapes, s_fit_only=False, plotting_args={"fit_poi" : ["r"], "formats" : ["pdf", "png"]}, n_processes=args.n_processes)
		datacards.print_pulls(datacards_cbs, args.n_processes, "-A -p {POI}".format(POI="r"))
		if args.plot_nuisance_impacts:
			datacards.nuisance_impacts(datacards_cbs, datacards_workspaces, args.n_processes)
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
		datacards.combine(datacards_cbs, datacards_workspaces, None, args.n_processes, "--expectSignal=1 -t -1 -M Asymptotic -n \"\"")
		datacards.combine(datacards_cbs, datacards_workspaces, None, args.n_processes, "-M ProfileLikelihood -t -1 --expectSignal 1 --toysFrequentist --significance -s %s\"\""%index)
		if args.remote:
			#os.system("tar cfv " + os.path.join(args.output_dir, "jobresult.tar") + " " + os.path.join(args.output_dir, "datacards") + " " + os.path.join(args.output_dir, "input"))
			os.system("tar cfv jobresult.tar datacards/ input/")
