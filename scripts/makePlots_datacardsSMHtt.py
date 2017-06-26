#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import argparse
import copy
import os
import sys

import Artus.Utility.tools as tools
import Artus.HarryPlotter.utility.plotconfigs as plotconfigs

import HiggsAnalysis.KITHiggsToTauTau.plotting.higgsplot as higgsplot
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.samples_run2_2016 as samples
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.binnings as binnings
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.systematics_run2 as systematics
import HiggsAnalysis.KITHiggsToTauTau.datacards.smhttdatacards as smhttdatacards



def _call_command(command):
	log.debug(command)
	logger.subprocessCall(command, shell=True)


if __name__ == "__main__":

	parser = argparse.ArgumentParser(description="Create ROOT inputs and datacards for SM HTT analysis.",
	                                 parents=[logger.loggingParser])

	parser.add_argument("-i", "--input-dir", required=True,
	                    help="Input directory.")
	parser.add_argument("-c", "--channel", action = "append",
	                    default=["et", "mt", "tt", "em", "mm"],
	                    help="Channel. This agument can be set multiple times. [Default: %(default)s]")
	parser.add_argument("--categories", nargs="+", action = "append",
	                    default=[["inclusive"]],
	                    help="Categories per channel. This agument needs to be set as often as --channels. [Default: %(default)s]")
	parser.add_argument("-m", "--higgs-masses", nargs="+", default=["125"],
	                    help="Higgs masses. [Default: %(default)s]")
	parser.add_argument("-x", "--quantity", default="0",
	                    help="Quantity. [Default: %(default)s]")
	parser.add_argument("--add-bbb-uncs", action="store_true", default=False,
	                    help="Add bin-by-bin uncertainties. [Default: %(default)s]")
	parser.add_argument("--auto-rebin", action="store_true", default=False,
	                    help="Do auto rebinning [Default: %(default)s]")
	parser.add_argument("--lumi", type=float, default=samples.default_lumi/1000.0,
	                    help="Luminosity for the given data in fb^(-1). [Default: %(default)s]")
	parser.add_argument("--for-dcsync", action="store_true", default=False,
	                    help="Produces simplified datacards for the synchronization exercise. [Default: %(default)s]")
	parser.add_argument("-w", "--weight", default="1.0",
	                    help="Additional weight (cut) expression. [Default: %(default)s]")
	parser.add_argument("--do-not-normalize-by-bin-width", default=False, action="store_true",
	                    help="Turn off normalization by bin width [Default: %(default)s]")
	parser.add_argument("-r", "--ratio", default=False, action="store_true",
	                    help="Add ratio subplot. [Default: %(default)s]")
	parser.add_argument("-a", "--args", default="",
	                    help="Additional Arguments for HarryPlotter. [Default: %(default)s]")
	parser.add_argument("--qcd-subtract-shapes", action="store_false", default=True, help="subtract shapes for QCD estimation [Default:%(default)s]")
	parser.add_argument("-b", "--background-method", default="new",
	                    help="Background estimation method to be used. [Default: %(default)s]")
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
	parser.add_argument("--use-asimov-dataset", action="store_true", default=False,
						help="Use s+b expectation as observation instead of real data. [Default: %(default)s]")
	parser.add_argument("--ttbar-fit", action="store_true", default=False,
						help="Use rate parameter to propagate ttbar normalization from control region to all categories. [Default: %(default)s]")
	parser.add_argument("--mm-fit", action="store_true", default=False,
						help="Use rate parameter to propagate zll normalization from mm control region to all categories. [Default: %(default)s]")
	parser.add_argument("--remote", action="store_true", default=False,
						help="Pack result to tarball, necessary for grid-control. [Default: %(default)s]")
	parser.add_argument("--era", default="2016",
	                    help="Era of samples to be used. [Default: %(default)s]")
	parser.add_argument("--x-bins", default=None,
	                    help="Manualy set the binning. Default is taken from configuration files.")
	parser.add_argument("--debug-plots", default=False, action="store_true",
	                    help="Produce debug Plots [Default: %(default)s]")
	parser.add_argument("-e", "--exclude-cuts", nargs="+", default=[],
	                    help="Exclude (default) selection cuts. [Default: %(default)s]")
	parser.add_argument("--plot-nuisance-impacts", action="store_true", default=False,
	                    help="Produce nuisance impact plots. [Default: %(default)s]")
	parser.add_argument("--do-not-ignore-category-removal", default=False, action="store_true",
						help="Exit program in case categories are removed from CH. [Default: %(default)s]")
	
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
	
	datacards = smhttdatacards.SMHttDatacards(higgs_masses=args.higgs_masses,ttbarFit=args.ttbar_fit,mmFit=args.mm_fit,year=args.era)
	if args.for_dcsync:
		datacards = smhttdatacards.SMHttDatacardsForSync(higgs_masses=args.higgs_masses)
	
	# initialise datacards
	tmp_input_root_filename_template = "input/${ANALYSIS}_${CHANNEL}_${BIN}_${SYSTEMATIC}_${ERA}.root"
	input_root_filename_template = "input/${ANALYSIS}_${CHANNEL}_${BIN}_${ERA}.root"
	bkg_histogram_name_template = "${BIN}/${PROCESS}"
	sig_histogram_name_template = "${BIN}/${PROCESS}${MASS}"
	bkg_syst_histogram_name_template = "${BIN}/${PROCESS}_${SYSTEMATIC}"
	sig_syst_histogram_name_template = "${BIN}/${PROCESS}${MASS}_${SYSTEMATIC}"
	datacard_filename_templates = datacards.configs.htt_datacard_filename_templates
	output_root_filename_template = "datacards/common/${ANALYSIS}.input_${ERA}.root"
	if args.for_dcsync:
		output_root_filename_template = "datacards/common/${ANALYSIS}.inputs-sm-${ERA}-2D.root" if args.era == "2016" else "datacards/common/${ANALYSIS}.inputs-sm-${ERA}-mvis.root"
	
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
		"em_ZeroJet2D" : 1.8,
		"em_Boosted2D" : 1.89,
		"em_Vbf2D" : 1.74
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
	zmm_cr_factors_official = {
		"mt_ZeroJet2D" : "(1.02)",
		"et_ZeroJet2D" : "(1.02)",
		"em_ZeroJet2D" : "(1.02)",
		"tt_ZeroJet2D" : "(1.02)",
		"mt_Boosted2D" : "(1.02)",
		"et_Boosted2D" : "(1.02)",
		"em_Boosted2D" : "(1.02)",
		"tt_Boosted2D" : "(1.02)",
		"mt_Vbf2D" : "(1.02)*(((mjj>=300)*(mjj<700)*1.06) + ((mjj>=700)*(mjj<1100)*0.98) + ((mjj>=1100)*(mjj<1500)*0.95) + ((mjj>=1500)*0.95))",
		"et_Vbf2D" : "(1.02)*(((mjj>=300)*(mjj<700)*1.06) + ((mjj>=700)*(mjj<1100)*0.98) + ((mjj>=1100)*(mjj<1500)*0.95) + ((mjj>=1500)*0.95))",
		"em_Vbf2D" : "(1.02)*(((mjj>=300)*(mjj<700)*1.06) + ((mjj>=700)*(mjj<1100)*0.98) + ((mjj>=1100)*(mjj<1500)*0.95) + ((mjj>=1500)*0.95))",
		"tt_Vbf2D" : "(1.02)*(((mjj<300)*1.00) + ((mjj>=300)*(mjj<500)*1.02) + ((mjj>=500)*(mjj<800)*1.06) + ((mjj>=800)*1.04))",
		"mt_Vbf2D_Up" : "(1.02)*(((mjj>=300)*(mjj<700)*1.12) + ((mjj>=700)*(mjj<1100)*0.96) + ((mjj>=1100)*(mjj<1500)*0.90) + ((mjj>=1500)*0.90))",
		"et_Vbf2D_Up" : "(1.02)*(((mjj>=300)*(mjj<700)*1.12) + ((mjj>=700)*(mjj<1100)*0.96) + ((mjj>=1100)*(mjj<1500)*0.90) + ((mjj>=1500)*0.90))",
		"em_Vbf2D_Up" : "(1.02)*(((mjj>=300)*(mjj<700)*1.12) + ((mjj>=700)*(mjj<1100)*0.96) + ((mjj>=1100)*(mjj<1500)*0.90) + ((mjj>=1500)*0.90))",
		"tt_Vbf2D_Up" : "(1.02)*(((mjj<300)*1.00) + ((mjj>=300)*(mjj<500)*1.04) + ((mjj>=500)*(mjj<800)*1.12) + ((mjj>=800)*1.08))",
		"mt_Vbf2D_Down" : "(1.02)",
		"et_Vbf2D_Down" : "(1.02)",
		"em_Vbf2D_Down" : "(1.02)",
		"tt_Vbf2D_Down" : "(1.02)"
	}
	
	do_not_normalize_by_bin_width = args.do_not_normalize_by_bin_width

	#restriction to CH
	datacards.cb.channel(args.channel)

	for index, (channel, categories) in enumerate(zip(args.channel, args.categories)):
		# include channel prefix
		categories= [channel + "_" + category for category in categories]
		# prepare category settings based on args and datacards
		categories_save = sorted(categories)
		categories = list(set(categories).intersection(set(datacards.cb.cp().channel([channel]).bin_set())))
		if(categories_save != sorted(categories)) and args.do_not_ignore_category_removal:
			log.fatal("CombineHarverster removed the following categories automatically. Was this intended?")
			log.fatal(list(set(categories_save) - set(categories)))
			sys.exit(1)
		
		# restrict CombineHarvester to configured categories:
		datacards.cb.FilterAll(lambda obj : (obj.channel() == channel) and (obj.bin() not in categories))
		
		for category in categories:
			datacards_per_channel_category = smhttdatacards.SMHttDatacards(cb=datacards.cb.cp().channel([channel]).bin([category]))
			
			exclude_cuts = copy.deepcopy(args.exclude_cuts)
			if "TTbarCR" in category and channel == "ttbar":
				exclude_cuts += ["pzeta"]
				do_not_normalize_by_bin_width = True
			# TODO: check that this does what it should in samples_run2_2016.py !!!
			#       a workaround solution may be necessary
			if ("ZeroJet2D_WJCR" in category or "Boosted2D_WJCR" in category) and channel in ["mt", "et"]:
				if channel in ["mt", "et"]:
					exclude_cuts += ["mt"]
					do_not_normalize_by_bin_width = True
			if ("ZeroJet2D_QCDCR" in category or "Boosted2D_QCDCR" in category or "Vbf2D_QCDCR" in category)  and channel in ["mt", "et", "tt"]:
				if channel in ["mt", "et"]:
					exclude_cuts += ["iso_1"]
					do_not_normalize_by_bin_width = True
				elif channel == "tt":
					exclude_cuts += ["iso_1", "iso_2"]
					do_not_normalize_by_bin_width = True
				
				datacards_per_channel_category = smhttdatacards.SMHttDatacardsForSync(cb=datacards.cb.cp().channel([channel]).bin([category]))
			
			higgs_masses = [mass for mass in datacards_per_channel_category.cb.mass_set() if mass != "*"]
			
			output_file = os.path.join(args.output_dir, input_root_filename_template.replace("$", "").format(
					ANALYSIS="htt",
					CHANNEL=channel,
					BIN=category,
					ERA="13TeV"
			))
			output_files.append(output_file)
			tmp_output_files = []
			
			for shape_systematic, list_of_samples in datacards_per_channel_category.get_samples_per_shape_systematic().iteritems():
				nominal = (shape_systematic == "nominal")
				list_of_samples = (["data"] if nominal else []) + [datacards.configs.process2sample(process) for process in list_of_samples]
				
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
							cut_type="smhtt2016" if args.era == "2016" else "baseline",
							estimationMethod=args.background_method,
							ss_os_factor=ss_os_factor,
							wj_sf_shift=wj_sf_shift,
							zmm_cr_factor=zmm_cr_factor
					)
					
					if "CMS_scale_gg_13TeV" in shape_systematic:
						systematics_settings = systematics_factory.get(shape_systematic)(config, category)
					elif "CMS_scale_j_" in shape_systematic and shape_systematic.split("_")[-2] in jecUncertNames:
						systematics_settings = systematics_factory.get(shape_systematic)(config, shape_systematic.split("_")[-2])
					else:
						systematics_settings = systematics_factory.get(shape_systematic)(config)
					# TODO: evaluate shift from datacards_per_channel_category.cb
					config = systematics_settings.get_config(shift=(0.0 if nominal else (1.0 if shift_up else -1.0)))
					config["qcd_subtract_shape"] = [args.qcd_subtract_shapes]
					config["x_expressions"] = ["m_vis"] if channel == "mm" and args.quantity == "m_sv" else [args.quantity]

					if "2D" not in category:
						binnings_key = "binningHtt13TeV_"+category+"_%s"%args.quantity
						if (binnings_key in binnings_settings.binnings_dict) and args.x_bins == None:
							config["x_bins"] = [binnings_settings.binnings_dict[binnings_key]]
						elif args.x_bins != None:
							config["x_bins"] = [args.x_bins]
						else:
							log.fatal("binnings key " + binnings_key + " not found in binnings_dict! Available binnings are (see HiggsAnalysis/KITHiggsToTauTau/python/plotting/configs/binnings.py):")
							for key in binnings_settings.binnings_dict:
								print key
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
					elif "Boosted2D" in category and not ("WJCR" in category or "QCDCR" in category):
						config["x_expressions"] = ["m_vis"] if channel == "mm" else ["m_sv"]
						config["y_expressions"] = ["H_pt"]
						config["x_bins"] = [binnings_settings.binnings_dict["binningHtt13TeV_"+category+("_m_vis" if channel == "mm" else "_m_sv")]]
						config["y_bins"] = [binnings_settings.binnings_dict["binningHtt13TeV_"+category+"_H_pt"]]
					elif "Vbf2D" in category and not "QCDCR" in category:
						config["x_expressions"] = ["m_vis"] if channel == "mm" else ["m_sv"]
						config["y_expressions"] = ["mjj"]
						config["x_bins"] = [binnings_settings.binnings_dict["binningHtt13TeV_"+category+("_m_vis" if channel == "mm" else "_m_sv")]]
						config["y_bins"] = [binnings_settings.binnings_dict["binningHtt13TeV_"+category+"_mjj"]]
					
					# Unroll 2d distribution to 1d in order for combine to fit it
					if "2D" in category and not ("WJCR" in category or "QCDCR" in category) and not (channel == "tt" and "ZeroJet2D" in category):
						two_d_inputs = []
						for mass in higgs_masses:
							two_d_inputs.extend([sample+(mass if sample in ["wh","zh","ggh",'qqh'] else "") for sample in list_of_samples])
						if not "UnrollTwoDHistogram" in config.get("analysis_modules", []):
							config.setdefault("analysis_modules", []).append("UnrollTwoDHistogram")
						config.setdefault("two_d_input_nicks", two_d_inputs)
						config.setdefault("unrolled_hist_nicks", two_d_inputs)
						
					config["directories"] = [args.input_dir]
					
					histogram_name_template = bkg_histogram_name_template if nominal else bkg_syst_histogram_name_template
					config["labels"] = [histogram_name_template.replace("$", "").format(
							PROCESS=datacards.configs.sample2process(sample),
							BIN=category,
							SYSTEMATIC=systematic
					) for sample in config["labels"]]
					
					tmp_output_file = os.path.join(args.output_dir, tmp_input_root_filename_template.replace("$", "").format(
							ANALYSIS="htt",
							CHANNEL=channel,
							BIN=category,
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
	higgsplot.HiggsPlotter(list_of_config_dicts=plot_configs, list_of_args_strings=[args.args], n_processes=args.n_processes, n_plots=args.n_plots[0])
	if args.n_plots[0] != 0:
		tools.parallelize(_call_command, hadd_commands, n_processes=args.n_processes)
	if args.debug_plots:
		debug_plot_configs = []
		for output_file in output_files:
			debug_plot_configs.extend(plotconfigs.PlotConfigs().all_histograms(output_file, plot_config_template={"markers":["E"], "colors":["#FF0000"]}))
		higgsplot.HiggsPlotter(list_of_config_dicts=debug_plot_configs, list_of_args_strings=[args.args], n_processes=args.n_processes, n_plots=args.n_plots[1])
	
	# update CombineHarvester with the yields and shapes
	datacards.extract_shapes(
			os.path.join(args.output_dir, input_root_filename_template.replace("$", "")),
			bkg_histogram_name_template, sig_histogram_name_template,
			bkg_syst_histogram_name_template, sig_syst_histogram_name_template,
			update_systematics=True
	)
	
	# add bin-by-bin uncertainties
	if args.add_bbb_uncs:
		datacards.add_bin_by_bin_uncertainties(
				processes=datacards.cb.cp().backgrounds().process_set(),
				add_threshold=0.05, merge_threshold=0.8, fix_norm=False
		)

	# scale
	if(args.scale_lumi):
		datacards.scale_expectation( float(args.scale_lumi) / args.lumi)
	
	# normalize DM systematic templates to the nominal one in order to get a pure shape systematic
	datacards.cb.cp().channel(["mt", "et"]).ForEachSyst(lambda systematic: systematic.set_value_u(1 if "tauDMReco" in systematic.name() else systematic.value_u()))
	datacards.cb.cp().channel(["mt", "et"]).ForEachSyst(lambda systematic: systematic.set_value_d(1 if "tauDMReco" in systematic.name() else systematic.value_d()))
	
	# remove processes with zero yield
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
	
	datacards.cb.FilterProcs(remove_procs_and_systs_with_zero_yield)
	
	# convert shapes in control regions to lnN
	datacards.cb.cp().ForEachSyst(lambda systematic: systematic.set_type("lnN") if is_control_region(systematic) and systematic.type() == "shape" else systematic.set_type(systematic.type()))
	
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
		if args.quantity == "m_sv" and not(do_not_normalize_by_bin_width):
			args.args += " --y-label 'dN / dm_{#tau #tau}  (1 / GeV)'"
	
		# adapt prefit and postfit plot configs
		backgrounds_to_merge = {
			"ZLL" : ["ZL", "ZJ"],
			"TT" : ["TTT", "TTJJ"],
			"EWK" : ["VVT", "VVJ", "VV", "W", "hww_gg125", "hww_qq125"]
		}
		prefit_postfit_plot_configs = datacards.prefit_postfit_plots(datacards_cbs, datacards_postfit_shapes, plotting_args={"ratio" : args.ratio, "args" : args.args, "lumi" : args.lumi, "normalize" : not(do_not_normalize_by_bin_width), "era" : args.era, "x_expressions" : config["x_expressions"][0], "return_configs" : True, "merge_backgrounds" : backgrounds_to_merge}, n_processes=args.n_processes)
		for plot_config in prefit_postfit_plot_configs:
			plot_category = plot_config["filename"].split("_")[-1]
			plot_channel = plot_config["title"].split("_")[-1]
			if "2D" in plot_category and not ("WJCR" in plot_category or "QCDCR" in plot_category):
					plot_config["canvas_width"] = 1200
					plot_config["y_rel_lims"] = [0.5, 10.0] if "--y-log" in args.args else [0.0, 2 if args.ratio else 1.9]
					plot_config["legend"] = [0.23, 0.63, 0.9, 0.83] if args.ratio else [0.23, 0.73, 0.9, 0.89]
					plot_config["legend_cols"] = 3
					plot_config["x_label"] = "bins"
					plot_config["texts"] = []
					plot_config["texts_x"] = []
					if "ZeroJet2D" in plot_category:
						if plot_channel in ["mt", "et"]:
							plot_config["texts"] = ["h^{#pm}", "h^{#pm}#pi^{0}", "h^{#pm}h^{#pm}h^{#mp}"]
							plot_config["texts_x"] = [0.3, 0.57, 0.83]
						elif plot_channel == "em":
							plot_config["texts"] = ["15 < p_{T}(#mu) < 25 GeV", "25 < p_{T}(#mu) < 35 GeV", "p_{T}(#mu) > 35 GeV"]
							plot_config["texts_x"] = [0.3, 0.57, 0.83]
					elif "Boosted2D" in plot_category:
						if plot_channel in ["mt", "et", "em"]:
							config["texts"] = ["0 < p_{T}^{#tau#tau} < 100 GeV", "100 < p_{T}^{#tau#tau} < 150 GeV", "150 < p_{T}^{#tau#tau} < 200 GeV", "200 < p_{T}^{#tau#tau} < 250 GeV", "250 < p_{T}^{#tau#tau} < 300 GeV", "p_{T}^{#tau#tau} > 300 GeV"]
							config["texts_x"] = [0.25, 0.37, 0.50, 0.64, 0.77, 0.89]
						elif plot_channel == "tt":
							config["texts"] = ["0 < p_{T}^{#tau#tau} < 100 GeV", "100 < p_{T}^{#tau#tau} < 170 GeV", "1750 < p_{T}^{#tau#tau} < 300 GeV", "p_{T}^{#tau#tau} > 300 GeV"]
							config["texts_x"] = [0.25, 0.45, 0.65, 0.85]
					elif "Vbf2D" in plot_category:
						if plot_channel in ["mt", "et", "em"]:
							config["texts"] = ["300 < m_{jj} < 700 GeV", "700 < m_{jj} < 1100 GeV", "1100 < m_{jj} < 1500 GeV", "m_{jj} > 1500 GeV"]
						elif plot_channel == "tt":
							config["texts"] = ["0 < m_{jj} < 300 GeV", "300 < m_{jj} < 500 GeV", "500 < m_{jj} < 800 GeV", "m_{jj} > 800 GeV"]
						config["texts_x"] = [0.25, 0.45, 0.65, 0.85]
					plot_config["texts_y"] = list((0.55 for i in range(len(plot_config["texts"]))))
					plot_config["texts_size"] = [0.075]
		higgsplot.HiggsPlotter(list_of_config_dicts=prefit_postfit_plot_configs, list_of_args_strings=[args.args], n_processes=args.n_processes, n_plots=args.n_plots[1])
		
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
