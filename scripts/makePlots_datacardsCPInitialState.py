#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import argparse
import copy
import os
import sys
import pprint
import numpy

import Artus.Utility.tools as tools
import Artus.HarryPlotter.utility.plotconfigs as plotconfigs

import HiggsAnalysis.KITHiggsToTauTau.plotting.higgsplot as higgsplot
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.samples_run2_2016 as samples
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.binnings as binnings
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.systematics_run2 as systematics
import HiggsAnalysis.KITHiggsToTauTau.datacards.smhttdatacards as smhttdatacards
import HiggsAnalysis.KITHiggsToTauTau.datacards.initialstatecpstudiesdatacards as initialstatecpstudiesdatacards



def _call_command(command):
	log.debug(command)
	logger.subprocessCall(command, shell=True)


if __name__ == "__main__":

	parser = argparse.ArgumentParser(description="Create ROOT inputs and datacards for SM HTT analysis.",
	                                 parents=[logger.loggingParser])

	parser.add_argument("-i", "--input-dir", required=True,
	                    help="Input directory.")
	parser.add_argument("--cpstudy", nargs="+", required=True,
	                    default=["initial"],
	                    choices=["initial", "final"],
						help="Choose which CP study to do: initial state or final state. [Default: %(default)s]")
	parser.add_argument("-c", "--channel", action = "append",
	                    default=["et", "mt", "tt", "em"],
	                    help="Channel. This argument can be set multiple times. [Default: %(default)s]")
	parser.add_argument("--categories", nargs="+", action = "append",
	                    default=[["inclusive"]],
	                    help="Categories per channel. This argument needs to be set as often as --channels. [Default: %(default)s]")
	parser.add_argument("-m", "--higgs-masses", nargs="+", default=["125"],
	                    help="Higgs masses. [Default: %(default)s]")
	parser.add_argument("--cp-mixings", nargs="+", type=float,
						default=list(numpy.arange(0.0, 1.001, 0.1)),
						help="CP mixing angles alpha_tau (in units of pi/2) to be probed. [Default: %(default)s]")
	parser.add_argument("-x", "--quantity", default="jdphi",
	                    help="Quantity. [Default: %(default)s]")
	parser.add_argument("--add-bbb-uncs", action="store_true", default=False,
	                    help="Add bin-by-bin uncertainties. [Default: %(default)s]")
	parser.add_argument("--auto-rebin", action="store_true", default=False,
	                    help="Do auto rebinning [Default: %(default)s]")
	parser.add_argument("--lumi", type=float, default=samples.default_lumi/1000.0,
	                    help="Luminosity for the given data in fb^(-1). [Default: %(default)s]")
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
	parser.add_argument("--use-rateParam", action="store_true", default=False,
						help="Use rate parameter to estimate ZTT normalization from ZMM. [Default: %(default)s]")
	parser.add_argument("--era", default="2016",
	                    help="Era of samples to be used. [Default: %(default)s]")
	parser.add_argument("--x-bins", default=None,
	                    help="Manualy set the binning. Default is taken from configuration files.")
	parser.add_argument("--debug-plots", default=False, action="store_true",
	                    help="Produce debug Plots [Default: %(default)s]")
	parser.add_argument("-e", "--exclude-cuts", nargs="+", default=[],
	                    help="Exclude (default) selection cuts. [Default: %(default)s]")
	parser.add_argument("--no-shape-uncs", default=False, action="store_true",
						help="Do not include shape uncertainties. [Default: %(default)s]")
	parser.add_argument("--no-syst-uncs", default=False, action="store_true",
						help="Do not include systematic uncertainties. This should only be used together with --use-asimov-dataset. [Default: %(default)s]")
	parser.add_argument("--steps", nargs="+",
	                    default=["maxlikelihoodfit", "prefitpostfitplots", "pvalue", "nuisanceimpacts"],
	                    choices=["maxlikelihoodfit", "prefitpostfitplots", "pvalue", "nuisanceimpacts"],
						help="Steps to perform. [Default: %(default)s]")
	parser.add_argument("--use-shape-only", action="store_true", default=False,
						help="Use only shape to distinguish between cp hypotheses. [Default: %(default)s]")
	parser.add_argument("--production-mode", nargs="+",
	                    default=["ggh", "qqh"],
	                    choices=["ggh", "qqh"],
						help="Choose the production modes. Option needed for initial state studies. [Default: %(default)s]")
	parser.add_argument("--hypothesis", nargs="+",
	                    default=["susycpodd"],
	                    choices=["susycpodd", "cpodd", "cpmix"],
						help="Choose the hypothesis to test against CPeven hypothesis. Option needed for final state studies. [Default: %(default)s]")

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
	
	# preparation of CP mixing angles alpha_tau/(pi/2)
	args.cp_mixings.sort()
	cp_mixing_angles = ["{mixing:03d}".format(mixing=int(mixing*100)) for mixing in args.cp_mixings]
	cp_mixings_str = ["{mixing:0.2f}".format(mixing=mixing) for mixing in args.cp_mixings]
	
	# initialisations for plotting
	sample_settings = samples.Samples()
	binnings_settings = binnings.BinningsDict()
	systematics_factory = systematics.SystematicsFactory()
	
	plot_configs = []
	output_files = []
	merged_output_files = []
	hadd_commands = []
	signal_processes = []

	# set the signal processes
	# initial state studies
	if "initial" in args.cpstudy:
		if "ggh" in args.production_mode:
			signal_processes.append("ggHsm")
			signal_processes.append("ggHps_ALT")
		if "qqh" in args.production_mode:
			signal_processes.append("qqHsm")
			signal_processes.append("qqHps_ALT")
	# final state studies
	if "final" in args.cpstudy:
		if "susycpodd" in args.hypothesis:
			signal_processes.append("CPEVEN")
			signal_processes.append("SUSYCPODD_ALT")
		if "cpodd" in args.hypothesis:
			signal_processes.append("CPEVEN")
			signal_processes.append("CPODD_ALT")
		if "cpmix" in args.hypothesis:
			signal_processes.append("CPEVEN")
			signal_processes.append("CPMIX_ALT")
	

	datacards = initialstatecpstudiesdatacards.InitialStateCPStudiesDatacards(cp_mixings_str, higgs_masses=args.higgs_masses,useRateParam=args.use_rateParam,year=args.era, signal_processes=signal_processes) # TODO: derive own version from this class DONE
	
	# restrict combine to lnN systematics only if no_shape_uncs is set
	if args.no_shape_uncs or args.no_syst_uncs:
		log.debug("Deactivate shape uncertainties")
		datacards.cb.FilterSysts(lambda systematic : systematic.type() == "shape")
		if log.isEnabledFor(logging.DEBUG):
			datacards.cb.PrintSysts()
	
	# initialise datacards
	tmp_input_root_filename_template = "input/${ANALYSIS}_${CHANNEL}_${BIN}_${SYSTEMATIC}_${ERA}.root"
	input_root_filename_template = "input/${ANALYSIS}_${CHANNEL}_${BIN}_${ERA}.root"
	bkg_histogram_name_template = "${BIN}/${PROCESS}"
	sig_histogram_name_template = "${BIN}/${PROCESS}${MASS}"
	bkg_syst_histogram_name_template = "${BIN}/${PROCESS}_${SYSTEMATIC}"
	sig_syst_histogram_name_template = "${BIN}/${PROCESS}${MASS}_${SYSTEMATIC}"
	datacard_filename_templates = datacards.configs.htt_datacard_filename_templates
	output_root_filename_template = "datacards/common/${ANALYSIS}.input_${ERA}.root"

	if args.channel != parser.get_default("channel"):
		args.channel = args.channel[len(parser.get_default("channel")):]

	if args.categories != parser.get_default("categories"):
		args.categories = args.categories[1:]

	# catch if on command-line only one set has been specified and repeat it
	if(len(args.categories) == 1):
		args.categories = [args.categories[0]] * len(args.channel)

	#restriction to CH
	datacards.cb.channel(args.channel)
	for index, (channel, categories) in enumerate(zip(args.channel, args.categories)):
		# include channel prefix
		categories= [channel + "_" + category for category in categories]
		# prepare category settings based on args and datacards
		categories_save = sorted(categories)
		categories = list(set(categories).intersection(set(datacards.cb.cp().channel([channel]).bin_set())))
		if(categories_save != sorted(categories)):
			log.fatal("CombineHarverster removed the following categories automatically. Was this intended?")
			log.fatal(list(set(categories_save) - set(categories)))
			sys.exit(1)
		
		# restrict CombineHarvester to configured categories:
		datacards.cb.FilterAll(lambda obj : (obj.channel() == channel) and (obj.bin() not in categories))
		
		for category in categories:	
			
			datacards_per_channel_category = initialstatecpstudiesdatacards.InitialStateCPStudiesDatacards(cb=datacards.cb.cp().channel([channel]).bin([category]))

			exclude_cuts = args.exclude_cuts
			higgs_masses = [mass for mass in datacards.cb.mass_set() if mass != "*"]
			
			output_file = os.path.join(args.output_dir, input_root_filename_template.replace("$", "").format(
					ANALYSIS="htt",
					CHANNEL=channel,
					BIN=category,
					ERA="13TeV"
			))
			merged_output_files.append(output_file)
			output_files.append(output_file)
			tmp_output_files = []
			
			for shape_systematic, list_of_samples in datacards.get_samples_per_shape_systematic(channel, category).iteritems():
				nominal = (shape_systematic == "nominal")
				list_of_samples = (["data"] if nominal else []) + [datacards.configs.process2sample(process) for process in list_of_samples]
				
				for shift_up in ([True] if nominal else [True, False]):
					systematic = "nominal" if nominal else (shape_systematic + ("Up" if shift_up else "Down"))
					
					log.debug("Create inputs for (samples, systematic) = ([\"{samples}\"], {systematic}), (channel, category) = ({channel}, {category}).".format(
							samples="\", \"".join(list_of_samples),
							channel=channel,
							category=category,
							systematic=systematic
					))
					
					
					# prepare plotting configs for retrieving the input histograms
					config = sample_settings.get_config(
							samples=[getattr(samples.Samples, sample) for sample in list_of_samples],
							channel=channel,
							category="catHtt13TeV_"+category,
							weight=args.weight,
							lumi = args.lumi * 1000,
							exclude_cuts=exclude_cuts,
							higgs_masses=higgs_masses,
							cut_type="cp2016",
							estimationMethod=args.background_method
					)
					
					systematics_settings = systematics_factory.get(shape_systematic)(config)
					
					# TODO: evaluate shift from datacards.cb
					config = systematics_settings.get_config(shift=(0.0 if nominal else (1.0 if shift_up else -1.0)))
					config["qcd_subtract_shape"] = [args.qcd_subtract_shapes]
					config["x_expressions"] = ["m_vis"] if channel == "mm" and args.quantity == "m_sv" else [args.quantity]

					if "initial" in args.cpstudy:
						binnings_key = "tt_absjdphi"
					if "final" in args.cpstudy:
						binnings_key = "tt_phiStarCP"
					if (binnings_key in binnings_settings.binnings_dict) and args.x_bins == None:
						config["x_bins"] = [binnings_key]
					elif args.x_bins != None:
						config["x_bins"] = [args.x_bins]
					else:
						log.fatal("binnings key " + binnings_key + " not found in binnings_dict! Available binnings are (see HiggsAnalysis/KITHiggsToTauTau/python/plotting/configs/binnings.py):")
						for key in binnings_settings.binnings_dict:
							log.debug(key)
						sys.exit()

					# set quantity x depending on the category
					if "final" in args.cpstudy and args.x==None:
						if "RHOmethod" in args.categories:
							config["x_expressions"] = ["recoPhiStarCP_rho_merged"]
						if "COMBmethod" in args.categories:
							config["x_expressions"] = ["recoPhiStarCPCombMerged"]


					config["directories"] = [args.input_dir]
					
					histogram_name_template = bkg_histogram_name_template if nominal else bkg_syst_histogram_name_template
					config["labels"] = [histogram_name_template.replace("$", "").format(
							PROCESS=datacards.configs.sample2process(sample.replace("wh125", "wh").replace("zh125", "zh")),
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
	higgsplot.HiggsPlotter(list_of_config_dicts=plot_configs, list_of_args_strings=[args.args], n_processes=args.n_processes, n_plots=args.n_plots[0])
	if args.n_plots[0] != 0:
		tools.parallelize(_call_command, hadd_commands, n_processes=args.n_processes)
	if args.debug_plots:
		debug_plot_configs = []
		for output_file in merged_output_files:
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
				add_threshold=0.1, merge_threshold=0.5, fix_norm=True
		)
	
	# restrict combine to lnN systematics only if no_shape_uncs is set
	if args.no_syst_uncs:
		log.debug("Deactivate systematic uncertainties")
		if not args.use_asimov_dataset:
			log.warning("Fitting MC to data without systematic uncertainties can lead to unreasonable results.")
		datacards.cb.FilterSysts(lambda systematic : True)
		if log.isEnabledFor(logging.DEBUG):
			datacards.cb.PrintSysts()
	
	# scale
	if(args.scale_lumi):
		datacards.scale_expectation( float(args.scale_lumi) / args.lumi)
	#after additional cuts
	#datacards.cb.cp().signals().ForEachProc(lambda process: process.set_rate(process.no_norm_rate() * (0.1)))
	#befor cuts
	#datacards.cb.cp().signals().ForEachProc(lambda process: process.set_rate(process.no_norm_rate() * (0.207)))
	# use asimov dataset for s+b
	if args.use_asimov_dataset:
		signal_null_hypothesis = datacards.cb.cp().signals()
		signal_null_hypothesis.FilterAll(lambda obj : ("ALT" in obj.process()))
		signal_null_hypothesis.ForEachProc(lambda process: process.set_rate(process.no_norm_rate() * (1.)))

		signal_alt_hypothesis = datacards.cb.cp().signals()
		signal_alt_hypothesis.FilterAll(lambda obj : ("ALT" not in obj.process()))
		signal_alt_hypothesis.ForEachProc(lambda process: process.set_rate(process.no_norm_rate() * (0.000000001)))
		#signal_alt_hypothesis.ForEachProc(lambda process: process.set_rate(process.no_norm_rate() * (0.000000000451)))
		
		datacards.replace_observation_by_asimov_dataset("125")
		
		signal_null_hypothesis.ForEachProc(lambda process: process.set_rate(process.no_norm_rate() / (1.0)))
		signal_alt_hypothesis.ForEachProc(lambda process: process.set_rate(process.no_norm_rate() / (0.000000001)))

	if args.auto_rebin:
		datacards.auto_rebin(bin_threshold = 1.0, rebin_mode = 0)
	#datacards.cb.PrintAll()
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
	#cb.PrintAll()

	# Physics model used for H->ZZ spin/CP studies
	# https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit/blob/74x-root6/python/HiggsJPC.py
	datacards_workspaces = datacards.text2workspace(
			datacards_cbs,
			args.n_processes,
			"-P {MODEL} {MODEL_PARAMETERS}".format(
				MODEL="HiggsAnalysis.CombinedLimit.HiggsJPC:twoHypothesisHiggs",
				MODEL_PARAMETERS=("--PO=muFloating" if args.use_shape_only else "")
			)
	)
	""" custom physics model
	datacards_workspaces = datacards.text2workspace(
			datacards_cbs,
			args.n_processes,
			"-P {MODEL} {MODEL_PARAMETERS}".format(
				MODEL="HiggsAnalysis.KITHiggsToTauTau.datacards.higgsmodels:HiggsCPI",
				MODEL_PARAMETERS=""
			)
	)
	"""

	#annotation_replacements = {channel : index for (index, channel) in enumerate(["combined", "tt", "mt", "et", "em"])}

	# Max. likelihood fit and postfit plots
	if "maxlikelihoodfit" in args.steps:
		datacards.combine(datacards_cbs, datacards_workspaces, datacards_poi_ranges, args.n_processes, "-M MaxLikelihoodFit "+datacards.stable_options+" -n \"\""+" --expectSignal 1.0 -t -1 --setPhysicsModelParameters \"x=1\"")
	#datacards.nuisance_impacts(datacards_cbs, datacards_workspaces, args.n_processes)
	if "prefitpostfitplots" in args.steps:
		datacards_postfit_shapes = datacards.postfit_shapes_fromworkspace(datacards_cbs, datacards_workspaces, False, args.n_processes, "--sampling" + (" --print" if args.n_processes <= 1 else ""))

	# divide plots by bin width and change the label correspondingly
		if args.quantity == "m_sv" and not(args.do_not_normalize_by_bin_width):
			args.args += " --y-label 'dN / dm_{#tau #tau}  (1 / GeV)'"

		datacards.prefit_postfit_plots(datacards_cbs, datacards_postfit_shapes, plotting_args={"ratio" : args.ratio, "args" : args.args, "lumi" : args.lumi, "x_expressions" : args.quantity, "normalize" : not(args.do_not_normalize_by_bin_width), "era" : args.era}, n_processes=args.n_processes,signal_stacked_on_bkg=True)
		datacards.pull_plots(datacards_postfit_shapes, s_fit_only=False, plotting_args={"fit_poi" : ["x"], "formats" : ["pdf", "png"]}, n_processes=args.n_processes)
		datacards.print_pulls(datacards_cbs, args.n_processes, "-A -p {POI}".format(POI="x") )
		if "nuisanceimpacts" in args.steps:
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
	if "pvalue" in args.steps:
		datacards.combine(datacards_cbs, datacards_workspaces, None, args.n_processes, " -M HybridNew --testStat=TEV --saveHybridResult --generateNuis=0 --singlePoint 1  --fork 8 -T 20000 -i 1 --clsAcc 0 --fullBToys --generateExt=1 -n \"\"") # TODO: change to HybridNew in the old: --expectSignal=1 -t -1
		#-M HybridNew --testStat=TEV --generateExt=1 --generateNuis=0 fixedMu.root --singlePoint 1 --saveHybridResult --fork 40 -T 1000 -i 1 --clsAcc 0 --fullBToys

		#datacards.combine(datacards_cbs, datacards_workspaces, None, args.n_processes, "-M ProfileLikelihood -t -1 --expectSignal 1 --toysFrequentist --significance -s %s\"\""%index) # TODO: maybe this can be used to get p-values

		datacards_hypotestresult=datacards.hypotestresulttree(datacards_cbs, n_processes=args.n_processes, poiname="x" )
		log.info(datacards_hypotestresult)
		if args.use_shape_only:
			datacards.combine(datacards_cbs, datacards_workspaces, None, args.n_processes, " -M MultiDimFit --algo=grid --points 100 -m 125 -v 2 -n \"\"")

		pconfigs_plot=[]
		for filename in datacards_hypotestresult.values():
			log.info(filename)
			pconfigs={}
			pconfigs["files"]= [filename]
			pconfigs["nicks"]= ["noplot","alternative_hyptothesis","null_hypothesis", "q_obs"]
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

			#pconfigs["scale_factors"]=[1,1,1,900]
			#pconfig["plot_modules"] = ["ExportRoot"]

			pconfigs["analysis_modules"]=["PValue"]
			pconfigs["p_value_alternative_hypothesis_nicks"]=["alternative_hyptothesis"]
			pconfigs["p_value_null_hypothesis_nicks"]=["null_hypothesis"]
			pconfigs["p_value_observed_nicks"]=["q_obs"]
			pconfigs["legend"]=[0.7,0.6,0.9,0.88]
			pconfigs_plot.append(pconfigs)
			pconfigs["labels"]=["CP-even", "CP-odd", "observed"]
			if "final" in args.cpstudy:
				if "susycpodd" or "cpodd" in args.hypothesis:
					pconfigs["labels"]=["CP-even", "CP-odd", "observed"]
					if args.use_asimov_dataset:
						pconfigs["labels"]=["CP-even", "CP-odd", "asimov"]
				if "cpmix" in args.hypothesis:
					pconfigs["labels"]=["CP-even", "CP-mix", "observed"]
					if args.use_asimov_dataset:
						pconfigs["labels"]=["CP-even", "CP-mix", "asimov"]

	
	#pprint.pprint(pconfigs_plot)
	higgsplot.HiggsPlotter(list_of_config_dicts=pconfigs_plot, list_of_args_strings=[args.args], n_processes=args.n_processes)

