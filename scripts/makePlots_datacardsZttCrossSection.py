#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import argparse
import copy
import os

import combineharvester as ch

import Artus.Utility.tools as tools

import HiggsAnalysis.KITHiggsToTauTau.plotting.higgsplot as higgsplot
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.samples_run2 as samples
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.systematics_run2 as systematics
import HiggsAnalysis.KITHiggsToTauTau.datacards.zttxsecdatacards as zttxsecdatacards



def _call_command(command):
	log.debug(command)
	logger.subprocessCall(command, shell=True)


if __name__ == "__main__":

	parser = argparse.ArgumentParser(description="Create ROOT inputs and datacards for ZTT cross section measurement.",
	                                 parents=[logger.loggingParser])

	parser.add_argument("-i", "--input-dir", required=True,
	                    help="Input directory.")
	parser.add_argument("-c", "--channel", action="append",
	                    default=["all"],
	                    help="Channel. This agument can be set multiple times. [Default: %(default)s]")
	parser.add_argument("--categories", action="append", nargs="+",
	                    default=[["all"]] * len(parser.get_default("channel")),
	                    help="Categories per channel. This agument needs to be set as often as --channels. [Default: %(default)s]")
	parser.add_argument("-x", "--quantity", default="0",
	                    help="Quantity. [Default: %(default)s]")
	parser.add_argument("--add-bbb-uncs", action="store_true", default=False,
	                    help="Add bin-by-bin uncertainties. [Default: %(default)s]")
	parser.add_argument("-w", "--weight", default="1.0",
	                    help="Additional weight (cut) expression. [Default: %(default)s]")
	parser.add_argument("--analysis-modules", default=[], nargs="+",
	                    help="Additional analysis Modules. [Default: %(default)s]")	
	parser.add_argument("-r", "--ratio", default=False, action="store_true",
	                    help="Add ratio subplot. [Default: %(default)s]")
	parser.add_argument("-a", "--args", default="",
	                    help="Additional Arguments for HarryPlotter. [Default: %(default)s]")
	parser.add_argument("-n", "--n-processes", type=int, default=1,
	                    help="Number of (parallel) processes. [Default: %(default)s]")
	parser.add_argument("-f", "--n-plots", type=int, nargs=2, default=[None, None],
	                    help="Number of plots for datacard inputs (1st arg) and for postfit plots (2nd arg). [Default: all]")
	parser.add_argument("-o", "--output-dir",
	                    default="$CMSSW_BASE/src/plots/ztt_datacards/",
	                    help="Output directory. [Default: %(default)s]")
	parser.add_argument("--clear-output-dir", action="store_true", default=False,
	                    help="Delete/clear output directory before running this script. [Default: %(default)s]")
	
	
	args = parser.parse_args()
	logger.initLogger(args)
	
	args.output_dir = os.path.expandvars(args.output_dir)
	if args.clear_output_dir and os.path.exists(args.output_dir):
		logger.subprocessCall("rm -r " + args.output_dir, shell=True)

	# statistical models    
	models = {
		"ztt_xsec" : {
			"datacards" : zttxsecdatacards.ZttXsecDatacards,
			"poi" : "r"
		}
		#"ztt_eff" : {
		#       "datacards" : zttxsecdatacards.ZttEffDatacards,
		#       "exclude_cuts" : ['iso_2'],
		#       "poi" : "eff"
		#}
		#"ztt_eff_and_xsec" : {
		#	"datacards" : zttxsecdatacards.ZttEffDatacards,
		#	"exclude_cuts" : ['iso_2']
		#}
	}
	if len(models) != 1:
		log.error("Only one statistical model per time can be switched on")
	for model, model_settings in models.iteritems():
		datacard_settings = model_settings['datacards']
		excludecut_settings = model_settings['exclude_cuts'] if model_settings.has_key('exclude_cuts') else ['']

	# initialisations for plotting
	sample_settings = samples.Samples()
	systematics_factory = systematics.SystematicsFactory()
	
	plot_configs = []
	hadd_commands = []
	
	datacards = datacard_settings()
	
	# initialise datacards
	tmp_input_root_filename_template = "input/${ANALYSIS}_${CHANNEL}_${BIN}_${SYSTEMATIC}_${ERA}.root"
	input_root_filename_template = "input/${ANALYSIS}_${CHANNEL}_${BIN}_${ERA}.root"
	bkg_histogram_name_template = "${BIN}/${PROCESS}"
	sig_histogram_name_template = "${BIN}/${PROCESS}"
	bkg_syst_histogram_name_template = "${BIN}/${PROCESS}_${SYSTEMATIC}"
	sig_syst_histogram_name_template = "${BIN}/${PROCESS}_${SYSTEMATIC}"
	datacard_filename_templates = [
		"datacards/individual/${BIN}/${ANALYSIS}_${CHANNEL}_${BINID}_${ERA}.txt",
		"datacards/${CHANNEL}/${ANALYSIS}_${CHANNEL}_${ERA}.txt",
		#"datacards/${BIN}/${ANALYSIS}_${BINID}_${ERA}.txt",
		"datacards/combined/${ANALYSIS}_${ERA}.txt",
	]
	output_root_filename_template = "datacards/common/${ANALYSIS}.input_${ERA}.root"
	
	# prepare channel settings based on args and datacards
	if args.channel != parser.get_default("channel"):
		args.channel = args.channel[1:]
	if (len(args.channel) == 1) and (args.channel[0] == "all"):
		args.channel = datacards.cb.channel_set()
	else:
		args.channel = list(set(args.channel).intersection(set(datacards.cb.channel_set())))
	
	# restrict CombineHarvester to configured channels:
	datacards.cb.channel(args.channel)
	
	if args.categories != parser.get_default("categories"):
		args.categories = args.categories[1:]
	args.categories = (args.categories * len(args.channel))[:len(args.channel)]
	for index, (channel, categories) in enumerate(zip(args.channel, args.categories)):
		
		# prepare category settings based on args and datacards
		if (len(categories) == 1) and (categories[0] == "all"):
			categories = datacards.cb.bin_set()
		else:
			categories = list(set(categories).intersection(set(datacards.cb.bin_set())))
		args.categories[index] = categories
		
		# restrict CombineHarvester to configured categories:
		datacards.cb.FilterAll(lambda obj : (obj.channel() == channel) and (obj.bin() not in categories))
		
		for category in categories:
			datacards_per_channel_category = datacard_settings(cb=datacards.cb.cp().channel([channel]).bin([category]))
			higgs_masses = [mass for mass in datacards_per_channel_category.cb.mass_set() if mass != "*"]
			
			output_file = os.path.join(args.output_dir, input_root_filename_template.replace("$", "").format(
					ANALYSIS="ztt",
					CHANNEL=channel,
					BIN=category,
					ERA="13TeV"
			))
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
							category="catZtt13TeV_"+category,
							weight=args.weight,
							exclude_cuts=excludecut_settings,
							higgs_masses=higgs_masses
					)
					
					systematics_settings = systematics_factory.get(shape_systematic)(config)
					# TODO: evaluate shift from datacards_per_channel_category.cb
					config = systematics_settings.get_config(shift=(0.0 if nominal else (1.0 if shift_up else -1.0)))
			
					config["x_expressions"] = args.quantity
			
					config["directories"] = [args.input_dir]
					
					histogram_name_template = bkg_histogram_name_template if nominal else bkg_syst_histogram_name_template
					config["labels"] = [histogram_name_template.replace("$", "").format(
							PROCESS=datacards.configs.sample2process(sample),
							BIN=category,
							SYSTEMATIC=systematic
					) for sample in config["labels"]]
					
					tmp_output_file = os.path.join(args.output_dir, tmp_input_root_filename_template.replace("$", "").format(
							ANALYSIS="ztt",
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
	output_files = list(set([os.path.join(config["output_dir"], config["filename"]+".root") for config in plot_configs[:args.n_plots[0]]]))
	for output_file in output_files:
		if os.path.exists(output_file):
			os.remove(output_file)
			log.debug("Removed file \""+output_file+"\" before it is recreated again.")
	
	# create input histograms with HarryPlotter
	higgsplot.HiggsPlotter(list_of_config_dicts=plot_configs, list_of_args_strings=[args.args], n_processes=args.n_processes, n_plots=args.n_plots[0])
	tools.parallelize(_call_command, hadd_commands, n_processes=args.n_processes)
	
	# update CombineHarvester with the yields and shapes
	datacards.extract_shapes(
			os.path.join(args.output_dir, input_root_filename_template.replace("$", "")),
			bkg_histogram_name_template.replace("{", "").replace("}", ""),
			sig_histogram_name_template.replace("{", "").replace("}", ""),
			bkg_syst_histogram_name_template.replace("{", "").replace("}", ""),
			sig_syst_histogram_name_template.replace("{", "").replace("}", "")
	)
	
	# add bin-by-bin uncertainties
	if args.add_bbb_uncs:
		datacards.add_bin_by_bin_uncertainties(
				processes=datacards.cb.cp().backgrounds().process_set(),
				add_threshold=0.1, merge_threshold=0.5, fix_norm=True
		)
	
	# write datacards and call text2workspace
	datacards_cbs = {}
	for datacard_filename_template in datacard_filename_templates:
		datacards_cbs.update(datacards.write_datacards(
				datacard_filename_template.replace("{", "").replace("}", ""),
				output_root_filename_template.replace("{", "").replace("}", ""),
				args.output_dir
		))
	
	plot_configs = []
	
	for model, model_settings in models.iteritems():
		# TODO: create sub-directory for each model
		
		datacards_workspaces = datacards.text2workspace(
				datacards_cbs,
				args.n_processes,
				"-P HiggsAnalysis.KITHiggsToTauTau.datacards.zttmodels:{MODEL} {MODEL_PARAMETERS}".format(
						MODEL=model,
						MODEL_PARAMETERS=model_settings.get("model_parameters", "")
				)
		)
		
		# Max. likelihood fit and postfit plots
		datacards.combine(datacards_cbs, datacards_workspaces, args.n_processes, "-M MaxLikelihoodFit -n \"\"")
		#datacards.combine(datacards_cbs, datacards_workspaces, args.n_processes, "-M MultiDimFit --floatOtherPOIs 1 -n \"\"")

		datacards_postfit_shapes = datacards.postfit_shapes(datacards_cbs, args.n_processes, "--sampling" + (" --print" if args.n_processes <= 1 else ""))
		datacards.print_pulls(datacards_cbs, args.n_processes, "-A -p {POI}".format(POI=model_settings['poi']))
		datacards.pull_plots(datacards_postfit_shapes, plotting_args={"fit_poi" : [model_settings['poi']]}, n_processes=args.n_processes)

		# Asymptotic limits
		#datacards.combine(datacards_cbs, datacards_workspaces, args.n_processes, "-M Asymptotic -n \"\"")
	
		bkg_plotting_order = ["ZTT", "ZLL", "TTJ", "VV", "WJ", "QCD"]
		for level in ["prefit", "postfit"]:
			for index, (fit_type, datacards_postfit_shapes_dict) in enumerate(datacards_postfit_shapes.iteritems()):
				if (index == 0) or (level == "postfit"):
					for datacard, postfit_shapes in datacards_postfit_shapes_dict.iteritems():
						for category in datacards_cbs[datacard].cp().bin_set():
							processes = datacards_cbs[datacard].cp().bin([category]).backgrounds().process_set() + datacards_cbs[datacard].cp().bin([category]).signals().process_set()
							processes.sort(key=lambda process: bkg_plotting_order.index(process) if process in bkg_plotting_order else len(bkg_plotting_order))
						
							config = {}
							config["files"] = [postfit_shapes]
							config["folders"] = [category+"_"+level]
							config["x_expressions"] = processes + ["data_obs", "TotalBkg", "TotalSig"]
							config["nicks"] = processes + ["data_obs", "noplot_TotalBkg", "noplot_TotalSig"]
							config["stacks"] = ["bkg"]*len(processes) + ["data"]
						
							config["labels"] = [label.lower() for label in processes + ["data_obs"]]
							config["colors"] = [color.lower() for color in processes + ["data_obs"]]
							config["markers"] = ["HIST"]*len(processes) + ["E"]
							config["legend_markers"] = ["F"]*len(processes) + ["ELP"]
						
							config["legend"] = [0.7, 0.6, 0.9, 0.88]
						
							config["output_dir"] = os.path.join(os.path.dirname(datacard), "plots")
							config["filename"] = level+("_"+fit_type if level == "postfit" else "")+"_"+category
						
							if args.ratio:
								if not "Ratio" in config.get("analysis_modules", []):
									config.setdefault("analysis_modules", []).append("Ratio")
								config.setdefault("ratio_numerator_nicks", []).extend(["noplot_TotalBkg noplot_TotalSig", "data_obs"])
								config.setdefault("ratio_denominator_nicks", []).extend(["noplot_TotalBkg noplot_TotalSig"] * 2)
								config.setdefault("ratio_result_nicks", []).extend(["ratio_unc", "ratio"])
								config.setdefault("colors", []).extend(["#000000"] * 2)
								config.setdefault("markers", []).extend(["E2", "E"])
								config.setdefault("legend_markers", []).extend(["F", "ELP"])
								config.setdefault("labels", []).extend([""] * 2)
								config["legend"] = [0.7, 0.5, 0.95, 0.92]
						
							plot_configs.append(config)
	
	# create result plots HarryPlotter
	higgsplot.HiggsPlotter(list_of_config_dicts=plot_configs, list_of_args_strings=[args.args], n_processes=args.n_processes, n_plots=args.n_plots[1])

