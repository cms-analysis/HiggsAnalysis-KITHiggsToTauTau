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
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.samples_run2 as samples
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
	parser.add_argument("--analysis-modules", default=[], nargs="+",
	                    help="Additional analysis Modules. [Default: %(default)s]")
	parser.add_argument("-r", "--ratio", default=False, action="store_true",
	                    help="Add ratio subplot. [Default: %(default)s]")
	parser.add_argument("-a", "--args", default="",
	                    help="Additional Arguments for HarryPlotter. [Default: %(default)s]")
	parser.add_argument("--qcd-subtract-shapes", action="store_false", default=True, help="subtract shapes for QCD estimation [Default:%(default)s]")
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
	parser.add_argument("--remote", action="store_true", default=False,
						help="Pack result to tarball, necessary for grid-control. [Default: %(default)s]")
	parser.add_argument("--era", default="2015",
	                    help="Era of samples to be used. [Default: %(default)s]")
	
	args = parser.parse_args()
	logger.initLogger(args)
	
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
	
	datacards = smhttdatacards.SMHttDatacards(higgs_masses=args.higgs_masses,useRateParam=args.use_rateParam)
	if args.for_dcsync:
		datacards = smhttdatacards.SMHttDatacardsForSync(higgs_masses=args.higgs_masses,useRateParam=args.use_rateParam)
	
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
		output_root_filename_template = "datacards/common/${ANALYSIS}.inputs-sm-${ERA}-mvis.root"
	
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
			datacards_per_channel_category = smhttdatacards.SMHttDatacards(cb=datacards.cb.cp().channel([channel]).bin([category]))
			
			exclude_cuts = []
			if args.for_dcsync:
				if category[3:] == 'inclusive':
					exclude_cuts=["mt", "pzeta"]
				elif category[3:] == 'inclusivemt40':
					exclude_cuts=["pzeta"]
				
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
							higgs_masses=higgs_masses
					)
					
					systematics_settings = systematics_factory.get(shape_systematic)(config)
					# TODO: evaluate shift from datacards_per_channel_category.cb
					config = systematics_settings.get_config(shift=(0.0 if nominal else (1.0 if shift_up else -1.0)))
					config["qcd_subtract_shape"] =[args.qcd_subtract_shapes]
					config["x_expressions"] = [args.quantity]

					binnings_key = "binningHtt13TeV_"+category+"_%s"%args.quantity
					if binnings_key in binnings_settings.binnings_dict:
						config["x_bins"] = [binnings_key]
					else:
						config["x_bins"] = ["35,0.0,350.0"]
					if args.auto_rebin:
						start = 0
						end = 0
						bins = binnings_settings.get_binning(config["x_bins"][0]) # handle different cases : nBins,start_bin,end_bin and bin edgeds specified by hand
						if "," in bins:
							nbins, start, end = bins.split(",")
						else:
							start = bins.split(" ")[0]
							end = bins.split(" ")[-1]
						config["x_bins"] = ["100," + start + "," + end] 
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
					
					if args.for_dcsync:
						config["ttbar_from_mc"] = True
						config["wjets_from_mc"] = True
					
					plot_configs.append(config)
			
			hadd_commands.append("hadd -f {DST} {SRC} && rm {SRC}".format(
					DST=output_file,
					SRC=" ".join(tmp_output_files)
			))
		if args.for_dcsync:
			merged_input_root_filename_template = "input/${ANALYSIS}_${CHANNEL}.inputs-sm-${ERA}-mvis.root"
			merged_output_file = os.path.join(args.output_dir, merged_input_root_filename_template.replace("$", "").format(
					ANALYSIS="htt",
					CHANNEL=channel,
					ERA="13TeV"
			))
			hadd_commands.append("hadd -f {DST} {SRC} && rm {SRC}".format(
					DST=merged_output_file,
					SRC=" ".join(output_files)
			))
			output_files = []
			merged_output_files.append(merged_output_file)
	
	if args.for_dcsync:
		input_root_filename_template = "input/${ANALYSIS}_${CHANNEL}.inputs-sm-${ERA}-mvis.root"
	
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
	
	debug_plot_configs = []
	for output_file in (output_files if not args.for_dcsync else merged_output_files):
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
	

	# scale
	if(args.scale_lumi):
		datacards.scale_expectation( float(args.scale_lumi) / args.lumi)
		
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
	
	#annotation_replacements = {channel : index for (index, channel) in enumerate(["combined", "tt", "mt", "et", "em"])}
	
	# Max. likelihood fit and postfit plots
	stable_options = r"--robustFit=1 --preFitValue=1. --X-rtd FITTER_NEW_CROSSING_ALGO --minimizerAlgoForMinos=Minuit2 --minimizerToleranceForMinos=0.1 --X-rtd FITTER_NEVER_GIVE_UP --X-rtd FITTER_BOUND --minimizerAlgo=Minuit2 --minimizerStrategy=0 --minimizerTolerance=0.1 --cminFallbackAlgo \"Minuit2,0:1.\""
	datacards.combine(datacards_cbs, datacards_workspaces, datacards_poi_ranges, args.n_processes, "-M MaxLikelihoodFit "+stable_options+" -n \"\"")
	#datacards.nuisance_impacts(datacards_cbs, datacards_workspaces, args.n_processes)
	datacards_postfit_shapes = datacards.postfit_shapes_fromworkspace(datacards_cbs, datacards_workspaces, False, args.n_processes, "--sampling" + (" --print" if args.n_processes <= 1 else ""))
	datacards.prefit_postfit_plots(datacards_cbs, datacards_postfit_shapes, plotting_args={"ratio" : args.ratio, "args" : args.args, "lumi" : args.lumi, "x_expressions" : args.quantity}, n_processes=args.n_processes)
	datacards.pull_plots(datacards_postfit_shapes, s_fit_only=False, plotting_args={"fit_poi" : ["r"], "formats" : ["pdf", "png"]}, n_processes=args.n_processes)
	datacards.print_pulls(datacards_cbs, args.n_processes, "-A -p {POI}".format(POI="r"))
	#datacards.annotate_trees(
			#datacards_workspaces,
			#"higgsCombine*MaxLikelihoodFit*mH*.root",
			#[os.path.join(os.path.dirname(template.replace("${CHANNEL}", "(.*)").replace("${MASS}", "\d*")), ".*.root") for template in datacard_filename_templates if "channel" in template][0],
			#annotation_replacements,
			#args.n_processes,
			#"-t limit -b channel"
	#)
	#datacards.annotate_trees(
			#datacards_workspaces,
			#"higgsCombine*MaxLikelihoodFit*mH*.root",
			#[os.path.join(os.path.dirname(template.replace("combined", "(combined)").replace("${MASS}", "\d*")), ".*.root") for template in datacard_filename_templates if "combined" in template][0],
			#annotation_replacements,
			#args.n_processes,
			#"-t limit -b channel"
	#)
	
	# Asymptotic limits
	datacards.combine(datacards_cbs, datacards_workspaces, None, args.n_processes, "--expectSignal=1 -t -1 -M Asymptotic -n \"\"")
	datacards.combine(datacards_cbs, datacards_workspaces, None, args.n_processes, "-M ProfileLikelihood -t -1 --expectSignal 1 --toysFrequentist --significance -s %s\"\""%index)
	if args.remote:
		#os.system("tar cfv " + os.path.join(args.output_dir, "jobresult.tar") + " " + os.path.join(args.output_dir, "datacards") + " " + os.path.join(args.output_dir, "input"))
		os.system("tar cfv jobresult.tar datacards/ input/")
