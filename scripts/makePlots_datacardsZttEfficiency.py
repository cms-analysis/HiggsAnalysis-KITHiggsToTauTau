#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import argparse
import copy
import os

import combineharvester as ch
import ROOT

import Artus.Utility.tools as tools

import HiggsAnalysis.KITHiggsToTauTau.plotting.higgsplot as higgsplot
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.samples_run2 as samples
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.systematics_run2 as systematics
import HiggsAnalysis.KITHiggsToTauTau.datacards.zttxsecdatacards as zttxsecdatacards



def _call_command(command):
	log.debug(command)
	logger.subprocessCall(command, shell=True)


if __name__ == "__main__":

	parser = argparse.ArgumentParser(description="Create ROOT inputs and datacards for tau ID efficiency measurement.",
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
	parser.add_argument("-r", "--ratio", default=True, action="store_true",
	                    help="Add ratio subplot. [Default: %(default)s]")
	parser.add_argument("-a", "--args", default="",
	                    help="Additional Arguments for HarryPlotter. [Default: %(default)s]")
	parser.add_argument("-n", "--n-processes", type=int, default=1,
	                    help="Number of (parallel) processes. [Default: %(default)s]")
	parser.add_argument("-f", "--n-plots", type=int, nargs=2, default=[None, None],
	                    help="Number of plots for datacard inputs (1st arg) and for postfit plots (2nd arg). [Default: all]")
	parser.add_argument("-o", "--output-dir",
	                    default="$CMSSW_BASE/src/plots/ztt_datacards_eff/",
	                    help="Output directory. [Default: %(default)s]")
	parser.add_argument("--clear-output-dir", action="store_true", default=False,
	                    help="Delete/clear output directory before running this script. [Default: %(default)s]")
	
	
	args = parser.parse_args()
	logger.initLogger(args)
	
	args.output_dir = os.path.expandvars(args.output_dir)
	if args.clear_output_dir and os.path.exists(args.output_dir):
		logger.subprocessCall("rm -r " + args.output_dir, shell=True)

	# statistical models
	modeldict = {
		"exclude_cuts" : ['iso_2'],
		"poi" : "r"
	}

	excludecut_settings = modeldict['exclude_cuts'] if modeldict.has_key('exclude_cuts') else ['']

	# initialisations for plotting
	sample_settings = samples.Samples()
	systematics_factory = systematics.SystematicsFactory()
	
	plot_configs = []
	hadd_commands = []
	
	datacards = zttxsecdatacards.ZttEffDatacards()
	
	# initialise datacards
	tmp_input_root_filename_template = "input/${ANALYSIS}_${CHANNEL}_${BIN}_${SYSTEMATIC}_${ERA}.root"
	input_root_filename_template = "input/${ANALYSIS}_${CHANNEL}_${BIN}_${ERA}.root"
	bkg_histogram_name_template = "${BIN}/${PROCESS}"
	sig_histogram_name_template = "${BIN}/${PROCESS}"
	bkg_syst_histogram_name_template = "${BIN}/${PROCESS}_${SYSTEMATIC}"
	sig_syst_histogram_name_template = "${BIN}/${PROCESS}_${SYSTEMATIC}"
	datacard_filename_templates = [
		"datacards/${CHANNEL}/${ANALYSIS}_${CHANNEL}_${ERA}.txt",
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
			categories = datacards.cb.cp().channel([channel]).bin_set()
		else:
			categories = list(set(categories).intersection(set(datacards.cb.cp().channel([channel]).bin_set())))
		args.categories[index] = categories
		
		# restrict CombineHarvester to configured categories:
		datacards.cb.FilterAll(lambda obj : (obj.channel() == channel) and (obj.bin() not in categories))
		
		for category in categories:
			if (channel != category[:2]):
				continue

			datacards_per_channel_category = zttxsecdatacards.ZttEffDatacards(cb=datacards.cb.cp().channel([channel]).bin([category]))
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
			bkg_histogram_name_template, sig_histogram_name_template,
			bkg_syst_histogram_name_template, sig_syst_histogram_name_template,
			update_systematics=False
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
	datacards_workspaces = {}

	for datacard, cb in datacards_cbs.iteritems():
		for channel in cb.cp().analysis(["ztt"]).era(["13TeV"]).channel_set():
			yieldpass = 0
			yieldfail = 0
			for category in cb.cp().analysis(["ztt"]).era(["13TeV"]).channel([channel]).bin_set():
				if "pass" in category:
					yieldpass = cb.cp().bin([category]).process(["ZTT"]).GetRate()
				elif "fail" in category:
					yieldfail = cb.cp().bin([category]).process(["ZTT"]).GetRate()
			efficiency = yieldpass / (yieldpass + yieldfail)

			command = ["text2workspace.py -m {MASS} -P HiggsAnalysis.KITHiggsToTauTau.datacards.zttmodels:ztt_eff --PO \"eff={EFF}\" {DATACARD} -o {OUTPUT}".format(
				MASS=[mass for mass in cb.mass_set() if mass != "*"][0],
				EFF=efficiency,
				DATACARD=datacard,
				OUTPUT=os.path.splitext(datacard)[0]+".root")]

			tools.parallelize(_call_command, command, n_processes=args.n_processes)

		datacards_workspaces[datacard] = os.path.splitext(datacard)[0]+".root"
	
	# Max. likelihood fit and postfit plots
	datacards.combine(datacards_cbs, datacards_workspaces, args.n_processes, "-M MaxLikelihoodFit --skipBOnlyFit -n \"\"")
	#datacards.combine(datacards_cbs, datacards_workspaces, args.n_processes, "-M MultiDimFit --floatOtherPOIs 1 -n \"\"")
	datacards_postfit_shapes = datacards.postfit_shapes(datacards_cbs, True, args.n_processes, "--sampling" + (" --print" if args.n_processes <= 1 else ""))
	#datacards.print_pulls(datacards_cbs, args.n_processes, "-A -p {POI}".format(POI=modeldict['poi']))
	datacards.pull_plots(datacards_postfit_shapes, s_fit_only=True, plotting_args={"fit_poi" : [modeldict['poi']]}, n_processes=args.n_processes)

	config_summary = {}
	y_point = 0.5	
	bkg_plotting_order = ["ZTT", "ZLL", "TTJ", "VV", "WJ", "QCD"]
	for level in ["prefit", "postfit"]:
		for index, (fit_type, datacards_postfit_shapes_dict) in enumerate(datacards_postfit_shapes.iteritems()):
			if (index == 0) or (level == "postfit"):
				for datacard, postfit_shapes in datacards_postfit_shapes_dict.iteritems():

					datacardpath = os.path.dirname(datacard)
					datacardfolder = datacardpath.split("/")[-1:][0]
					if (level == "postfit" and (datacardfolder == "combined" or datacardfolder in ["em","et","mt"])):
						channel = "channel_"+datacardfolder if datacardfolder in ["em","et","mt"] else "combination"
						config_summary.setdefault("files", []).append(os.path.join(datacardpath, "mlfit.root"))
						config_summary["folders"] = ["tree_fit_sb"]
						config_summary["tree_draw_options"] = ["TGraphAsymmErrorsX"]
						config_summary["x_expressions"] = ["mu:muLoErr:muHiErr"]
						config_summary.setdefault("y_expressions", []).append("0.5" if datacardfolder == "combined" else str(y_point+1))
						config_summary.setdefault("y_tick_labels", []).append(channel)
						if (datacardfolder != "combined"):
							y_point += 1

					for category in datacards_cbs[datacard].cp().bin_set():

						results_file = ROOT.TFile(os.path.join(datacardpath, "mlfit.root"))
						results_tree = results_file.Get("tree_fit_sb")
						results_tree.GetEntry(0)
						bestfit = results_tree.mu

						processes = datacards_cbs[datacard].cp().bin([category]).backgrounds().process_set() + datacards_cbs[datacard].cp().bin([category]).signals().process_set()
						processes.sort(key=lambda process: bkg_plotting_order.index(process) if process in bkg_plotting_order else len(bkg_plotting_order))

						config = {}
						config["files"] = [postfit_shapes]
						config["folders"] = [category+"_"+level]
						config["x_expressions"] = processes + ["data_obs", "TotalBkg", "TotalSig"]
						config["nicks"] = processes + ["data_obs", "noplot_TotalBkg", "noplot_TotalSig"]
						config["stacks"] = ["bkg"]*len(processes) + ["data"]

						if level == "postfit":
								config["scale_factors"] = [bestfit] + [1.0]*(len(processes) - 1) + [1.0, 1.0, bestfit]

						config.setdefault("analysis_modules", []).append("SumOfHistograms")
						config["sum_nicks"] = ["noplot_TotalBkg noplot_TotalSig"]
						config["sum_scale_factors"] = ["1.0 1.0"]
						config["sum_result_nicks"] = ["Total"]

						config["labels"] = [label.lower() for label in processes + ["data_obs"] + [""]]
						config["colors"] = [color.lower() for color in processes + ["data_obs"] + ["#000000"]]
						config["markers"] = ["HIST"]*len(processes) + ["E"] + ["E2"]
						config["legend_markers"] = ["F"]*len(processes) + ["ELP"] + ["F"]
						config["x_label"] = category[:2]+"_"+args.quantity
						config["title"] = "channel_"+category[:2]
						config["energies"] = [13.0]
						config["lumis"] = [0.04]
						config["legend"] = [0.7, 0.6, 0.9, 0.88]
						
						config["output_dir"] = os.path.join(datacardpath, "plots")
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
							config["y_subplot_lims"] = [0.5, 1.5]
							
						plot_configs.append(config)

	config_summary["output_dir"] = args.output_dir
	config_summary["filename"] = "bestfit"
	config_summary["markers"] = ["P"]*len(config_summary["files"])
	config_summary["x_lims"] = [0.0, 2.0]
	config_summary["y_lims"] = [0.0, len(config_summary["files"])]
	config_summary["x_label"] = "Best fit r"
	config_summary["y_label"] = ""
	config_summary["y_tick_labels"].remove("combination")
	config_summary["y_tick_labels"].insert(0, "combination")
	config_summary["grid"] = True
	plot_configs.append(config_summary)
	
	# create result plots HarryPlotter
	higgsplot.HiggsPlotter(list_of_config_dicts=plot_configs, list_of_args_strings=[args.args], n_processes=args.n_processes, n_plots=args.n_plots[1])

