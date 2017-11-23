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
import Artus.Utility.jsonTools as jsonTools
import Artus.HarryPlotter.utility.plotconfigs as plotconfigs

import HiggsAnalysis.KITHiggsToTauTau.plotting.higgsplot as higgsplot
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.samples_run2_2015 as samples
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.binnings as binnings
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.systematics_run2 as systematics
import HiggsAnalysis.KITHiggsToTauTau.datacards.zttpolarisationdatacards as zttpolarisationdatacards



def _call_command(command):
	log.debug(command)
	logger.subprocessCall(command, shell=True)


def replace_observation_by_asimov_dataset(datacards, pol=-0.159, r=1.0):
	# asimov_options = "--expectSignal 1.0 -t -1 --setPhysicsModelParameters \"pol=-0.159,r=1\""
	
	pospol_signals = datacards.cb.cp().signals()
	pospol_signals.FilterAll(lambda obj : ("pospol" not in obj.process().lower()))
	
	negpol_signals = datacards.cb.cp().signals()
	negpol_signals.FilterAll(lambda obj : ("negpol" not in obj.process().lower()))
	
	pospol_signals.ForEachProc(lambda process: process.set_rate(process.no_norm_rate() * (r * (1.0 + pol))))
	negpol_signals.ForEachProc(lambda process: process.set_rate(process.no_norm_rate() * (r * (1.0 - pol))))
	
	datacards.replace_observation_by_asimov_dataset()
	
	pospol_signals.ForEachProc(lambda process: process.set_rate(process.no_norm_rate() / (r * (1.0 + pol))))
	negpol_signals.ForEachProc(lambda process: process.set_rate(process.no_norm_rate() / (r * (1.0 - pol))))


if __name__ == "__main__":

	parser = argparse.ArgumentParser(description="Create ROOT inputs and datacards for ZTT polarisation analysis.",
	                                 parents=[logger.loggingParser])

	parser.add_argument("-i", "--input-dir", required=True,
	                    help="Input directory.")
	parser.add_argument("-c", "--channel", action = "append",
	                    default=["mt", "et", "tt", "em"],
	                    help="Channel. This agument can be set multiple times. [Default: %(default)s]")
	parser.add_argument("--categories", action="append", nargs="+",
	                    default=[["all"]] * len(parser.get_default("channel")),
	                    help="Categories per channel. This agument needs to be set as often as --channels. [Default: %(default)s]")
	parser.add_argument("--combinations", nargs="+",
	                    default=["individual", "channel", "category", "combined"],
	                    choices=["individual", "channel", "category", "combined"],
	                    help="Combinations to perform. [Default: %(default)s]")
	parser.add_argument("--add-bbb-uncs", action="store_true", default=False,
	                    help="Add bin-by-bin uncertainties. [Default: %(default)s]")
	parser.add_argument("--steps", nargs="+",
	                    default=["maxlikelihoodfit", "totstatuncs", "prefitpostfitplots", "pulls"],
	                    choices=["maxlikelihoodfit", "totstatuncs", "prefitpostfitplots", "pulls", "deltanll", "nuisanceimpacts"],
	                    help="Steps to perform. [Default: %(default)s]")
	parser.add_argument("--auto-rebin", action="store_true", default=False,
	                    help="Do auto rebinning [Default: %(default)s]")
	parser.add_argument("--lumi", type=float, default=samples.default_lumi/1000.0,
	                    help="Luminosity for the given data in fb^(-1). [Default: %(default)s]")
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
	                    default="$CMSSW_BASE/src/plots/ztt_polarisation_datacards/",
	                    help="Output directory. [Default: %(default)s]")
	parser.add_argument("--clear-output-dir", action="store_true", default=False,
	                    help="Delete/clear output directory before running this script. [Default: %(default)s]")
	parser.add_argument("--lumi-projection", type=float, nargs="+", default=[],
                        help="Specify luminosity values in fb^(-1) for a projection. [Default: %(default)s]")
	parser.add_argument("--use-asimov-dataset", action="store_true", default=False,
						help="Use s+b expectation as observation instead of real data. [Default: %(default)s]")
	parser.add_argument("--check-linearity", type=float, nargs="+", default=[],
						help="Specify the polarisation values for which to check the linearity of the discriminator. [Default: %(default)s]")
	parser.add_argument("--no-ewk-samples", default=False, action="store_true",
	                    help="Do not use EWK Z/W samples. [Default: %(default)s]")
	parser.add_argument("--no-ewkz-as-dy", default=False, action="store_true",
	                    help="Do not include EWKZ samples in inputs for DY. [Default: %(default)s]")
	parser.add_argument("--no-shape-uncs", default=False, action="store_true",
	                    help="Do not include shape-uncertainties. [Default: %(default)s]")
	parser.add_argument("--era", default="2016",
	                    help="Era of samples to be used. [Default: %(default)s]")
	parser.add_argument("--www", nargs="?", default=None, const="datacards",
	                    help="Publish plots. [Default: %(default)s]")
	
	args = parser.parse_args()
	logger.initLogger(args)
	
	args.n_plots = [n_plots if n_plots >= 0 else None for n_plots in args.n_plots]
	
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
	
	datacards = zttpolarisationdatacards.ZttPolarisationDatacards() # useRateParam=args.use_rate_parameter
	
	# initialise datacards
	tmp_input_root_filename_template = "input/${ANALYSIS}_${CHANNEL}_${BIN}_${SYSTEMATIC}_${ERA}.root"
	input_root_filename_template = "input/${ANALYSIS}_${CHANNEL}_${BIN}_${ERA}.root"
	bkg_histogram_name_template = "${BIN}/${PROCESS}"
	sig_histogram_name_template = "${BIN}/${PROCESS}"
	bkg_syst_histogram_name_template = "${BIN}/${PROCESS}_${SYSTEMATIC}"
	sig_syst_histogram_name_template = "${BIN}/${PROCESS}_${SYSTEMATIC}"
	output_root_filename_template = "datacards/common/${ANALYSIS}.input_${ERA}.root"
	datacard_filename_templates = []
	if "individual" in args.combinations:
		datacard_filename_templates.append("datacards/individual/${CHANNEL}/${BINID}/${ANALYSIS}_${CHANNEL}_${BINID}_${ERA}.txt")
	if "channel" in args.combinations:
		datacard_filename_templates.append("datacards/channel/${CHANNEL}/${ANALYSIS}_${CHANNEL}_${ERA}.txt")
	if "category" in args.combinations:
		datacard_filename_templates.append("datacards/category/${BINID}/${ANALYSIS}_${BINID}_${ERA}.txt")
	if "combined" in args.combinations:
		datacard_filename_templates.append("datacards/combined/${ANALYSIS}_${ERA}.txt")
	
	if args.channel != parser.get_default("channel"):
		args.channel = args.channel[len(parser.get_default("channel")):]
	
	if args.categories != parser.get_default("categories"):
		args.categories = args.categories[len(parser.get_default("categories")):]
	args.categories = (args.categories * len(args.channel))[:len(args.channel)]
	
	# restrict CombineHarvester to configured channels
	datacards.cb.channel(args.channel)

	if args.no_shape_uncs:
 		print("No shape uncs")
 		datacards.cb.FilterSysts(lambda systematic : systematic.type() == "shape")
 		datacards.cb.PrintSysts()

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
			datacards_per_channel_category = zttpolarisationdatacards.ZttPolarisationDatacards(cb=datacards.cb.cp().channel([channel]).bin([category]))
			
			higgs_masses = [mass for mass in datacards_per_channel_category.cb.mass_set() if mass != "*"]
			
			output_file = os.path.join(args.output_dir, input_root_filename_template.replace("$", "").format(
					ANALYSIS="ztt",
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
							category="catZttPol13TeV_"+category,
							weight=args.weight,
							lumi = args.lumi * 1000,
							higgs_masses=higgs_masses,
							estimationMethod="new",
							polarisation_bias_correction=True,
							cut_type="baseline_low_mvis",
							no_ewk_samples = args.no_ewk_samples,
							no_ewkz_as_dy = args.no_ewkz_as_dy
					)
					
					systematics_settings = systematics_factory.get(shape_systematic)(config)
					# TODO: evaluate shift from datacards_per_channel_category.cb
					config = systematics_settings.get_config(shift=(0.0 if nominal else (1.0 if shift_up else -1.0)))
					
					#config["qcd_subtract_shape"] =[args.qcd_subtract_shapes]
					
					config["x_expressions"] = [("0" if "_gen" in nick else "testZttPol13TeV_"+category) for nick in config["nicks"]]

					binnings_key = "binningZttPol13TeV_"+category
					if binnings_key in binnings_settings.binnings_dict:
						config["x_bins"] = [("1,-1,1" if "_gen" in nick else binnings_key) for nick in config["nicks"]]
						
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
	
	if log.isEnabledFor(logging.DEBUG):
		import pprint
		pprint.pprint(plot_configs)
	
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
	for output_file in (output_files):
		debug_plot_configs.extend(plotconfigs.PlotConfigs().all_histograms(output_file, plot_config_template={"markers":["E"], "colors":["#FF0000"]}))
	if args.www:
		for debug_plot_config in debug_plot_configs:
			debug_plot_config["www"] = debug_plot_config["output_dir"].replace(args.output_dir, args.www)
	higgsplot.HiggsPlotter(list_of_config_dicts=debug_plot_configs, list_of_args_strings=[args.args], n_processes=args.n_processes, n_plots=args.n_plots[0])
	
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
	
	plot_configs = []
	
	# lumi scale
	for scaled_lumi in [None]+args.lumi_projection:
		tmp_output_dir = os.path.join(args.output_dir, "" if scaled_lumi is None else ("lumi{:07}pb".format(int(scale_lumi*1000))))
		tmp_www = None
		if args.www:
			tmp_www = os.path.join(args.www, "" if scaled_lumi is None else ("lumi{:07}pb".format(int(scale_lumi*1000))))
		
		if not scaled_lumi is None:
			datacards.scale_expectation(scaled_lumi / args.lumi)
		
		# linearity
		polarisation_values_tree_files = {}
		for asimov_polarisation in [None]+(args.check_linearity if scaled_lumi is None else []):
			output_dir = os.path.join(tmp_output_dir, "" if asimov_polarisation is None else ("pol{:04}".format(int(asimov_polarisation*1000))))
			www = None
			if args.www:
				www = os.path.join(tmp_www, "" if asimov_polarisation is None else ("pol{:04}".format(int(asimov_polarisation*1000))))
			
			if not asimov_polarisation is None:
				replace_observation_by_asimov_dataset(datacards, asimov_polarisation, 1.0)
			elif args.use_asimov_dataset:
				replace_observation_by_asimov_dataset(datacards, -0.159, 1.0)

			if args.auto_rebin:
				datacards.auto_rebin(bin_threshold = 1.0, rebin_mode = 0)

			# write datacards and call text2workspace
			datacards_cbs = {}
			for datacard_filename_template in datacard_filename_templates:
				datacards_cbs.update(datacards.write_datacards(
						datacard_filename_template.replace("{", "").replace("}", ""),
						output_root_filename_template.replace("{", "").replace("}", ""),
						output_dir
				))
	
			datacards_workspaces = datacards.text2workspace(
					datacards_cbs,
					args.n_processes,
					"-P {MODEL} {MODEL_PARAMETERS}".format(
							MODEL="HiggsAnalysis.KITHiggsToTauTau.datacards.zttmodels:ztt_pol",
							MODEL_PARAMETERS=""
					)
			)
			
			if "maxlikelihoodfit" in args.steps:
				datacards.combine(
						datacards_cbs,
						datacards_workspaces,
						None,
						args.n_processes,
						"-M MaxLikelihoodFit --redefineSignalPOIs pol "+datacards.stable_options+" -n \"\"",
						split_stat_syst_uncs=False # MaxLikelihoodFit does not support the splitting of uncertainties
				)
			
			if (scaled_lumi is None) and (asimov_polarisation is None):
				if "prefitpostfitplots" in args.steps:
					datacards_postfit_shapes = datacards.postfit_shapes_fromworkspace(
							datacards_cbs,
							datacards_workspaces,
							False,
							args.n_processes,
							"--sampling" + (" --print" if args.n_processes <= 1 else ""),
							#fit_type_list=["fit_mdf"],
							#fit_result="multidimfit.root"
					)
	
					datacards.prefit_postfit_plots(
							datacards_cbs,
							datacards_postfit_shapes,
							plotting_args={"ratio" : args.ratio, "args" : args.args, "lumi" : args.lumi, "x_expressions" : "tauPolarisationDiscriminatorSvfit", "era" : "2015", "www" : www},
							n_processes=args.n_processes,
							signal_stacked_on_bkg=True
					)
				
				if "pulls" in args.steps:
					datacards.print_pulls(datacards_cbs, args.n_processes, "-A -p {POI}".format(POI="pol"))
					datacards.pull_plots(
							datacards_postfit_shapes,
							s_fit_only=True,
							plotting_args={"fit_poi" : ["pol"], "formats" : ["pdf", "png"], "args" : args.args, "www" : www},
							n_processes=args.n_processes
					)
				
				if "nuisanceimpacts" in args.steps:
					datacards.nuisance_impacts(datacards_cbs, datacards_workspaces, args.n_processes, "-P pol --redefineSignalPOIs pol")
				
				if "deltanll" in args.steps:
					datacards.combine(
							datacards_cbs,
							datacards_workspaces,
							None,
							args.n_processes,
							"-M MultiDimFit --algo grid --points 200 -P pol --redefineSignalPOIs pol "+datacards.stable_options+" -n Scan "
					)
	
			if "totstatuncs" in args.steps: # (scaled_lumi is None) and (asimov_polarisation is None):
				datacards.combine(
						datacards_cbs,
						datacards_workspaces,
						None,
						args.n_processes,
						"-M MultiDimFit --algo singles -P pol --redefineSignalPOIs pol "+datacards.stable_options+" -n ",
						split_stat_syst_uncs=True,
						additional_freeze_nuisances=["r"]
				)
	
			annotation_replacements = {channel : index for (index, channel) in enumerate(["combined"] + args.channel)}
			annotation_replacements.update({binid : index+1 for (index, binid) in enumerate(sorted(list(set([datacards.configs.category2binid(category, channel=category[:2]) for category in tools.flattenList(args.categories)]))))})
			if not asimov_polarisation is None:
				annotation_replacements.update({"pol{:04}".format(int(asimov_polarisation*1000)) : asimov_polarisation})
			values_tree_files = {}
			if ("channel" in args.combinations) or ("category" in args.combinations):
				datacards.annotate_trees(
						datacards_workspaces,
						"higgsCombine*.*.mH*.root",
						([[os.path.join(os.path.dirname(template.replace("${CHANNEL}", "(.*)").replace("${MASS}", "\d*")), ".*.root") for template in datacard_filename_templates if "channel" in template][0]] if "channel" in args.combinations else [])+
						([[os.path.join(os.path.dirname(template.replace("${BINID}", "(\d*)").replace("${MASS}", "\d*")), ".*.root") for template in datacard_filename_templates if "category" in template][0]] if "category" in args.combinations else [])+
						([os.path.join("/(pol-?\d*)", ".*.root")] if not asimov_polarisation is None else []),
						annotation_replacements,
						args.n_processes,
						values_tree_files,
						"-t limit -b" + (" channel" if "channel" in args.combinations else "") + (" category" if "category" in args.combinations else "") + (" polarisation" if not asimov_polarisation is None else "")
				)
				datacards.annotate_trees(
						datacards_workspaces,
						"higgsCombine*.*.mH*.root",
						[[os.path.join(os.path.dirname(template.replace("combined", "(combined)").replace("${MASS}", "\d*")), ".*.root") for template in datacard_filename_templates if "combined" in template][0]]*(2 if ("channel" in args.combinations) and ("category" in args.combinations) else 1)+
						([os.path.join("/(pol-?\d*)", ".*.root")] if not asimov_polarisation is None else []),
						annotation_replacements,
						args.n_processes,
						values_tree_files,
						"-t limit -b" + (" channel" if "channel" in args.combinations else "") + (" category" if "category" in args.combinations else "") + (" polarisation" if not asimov_polarisation is None else "")
				)
			if not asimov_polarisation is None:
				polarisation_values_tree_files.update(values_tree_files)
	
			# plot best fit values of parameter pol from physics model
			if "channel" in args.combinations:
				for template in ([
						"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/combine/best_fit_pol_over_channel.json",
						"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/combine/best_fit_weinberg_angle_over_channel.json",
				] if "maxlikelihoodfit" in args.steps else []) + ([
						"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/combine/best_fit_pol_over_channel_tot_stat_unc.json",
						"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/combine/best_fit_pol_over_channel_tot_unc.json",
						"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/combine/best_fit_pol_over_channel_stat_unc.json",
						"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/combine/best_fit_weinberg_angle_over_channel_tot_stat_unc.json",
						"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/combine/best_fit_weinberg_angle_over_channel_tot_unc.json",
						"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/combine/best_fit_weinberg_angle_over_channel_stat_unc.json",
				] if "totstatuncs" in args.steps else []): # if (scaled_lumi is None) and (asimov_polarisation is None) else []):
					
					x_values = sorted([values[0] for values in values_tree_files.keys() if values[0] > -990.0])
					config = jsonTools.JsonDict(os.path.expandvars(template))
					config["directories"] = [" ".join(set([os.path.dirname(root_file) for root_file in sorted(tools.flattenList(values_tree_files.values())) if ("datacards/channel" in root_file) or ("datacards/combined" in root_file)]))]
					config["x_ticks"] = x_values
					inv_annotation_replacements = {value : key for key, value in annotation_replacements.iteritems() if (type(key) != int) or (key < 1000)}
					config["x_tick_labels"] = [str(inv_annotation_replacements.get(int(value), value)) for value in x_values]
					#config["x_tick_labels"] = ["#scale[1.5]{" + ("" if label == "combined" else "channel_") + label + "}" for label in config["x_tick_labels"]]
					config["x_tick_labels"] = ["" + ("" if label == "combined" else "channel_") + label for label in config["x_tick_labels"]]
					config["x_lims"] = [min(x_values) - 0.5, max(x_values) + 0.5]
					config["output_dir"] = os.path.join(output_dir, "datacards/combined/plots")
					if args.www:
						config["www"] = os.path.join(www, "combined/plots")
					plot_configs.append(config)
				
				if ("deltanll" in args.steps) and (scaled_lumi is None) and (asimov_polarisation is None):
					for template in [
							"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/combine/likelihood_ratio_over_pol.json",
					]:
						config = jsonTools.JsonDict(os.path.expandvars(template))
						config["directories"] = list(set([os.path.dirname(root_file) for root_file in sorted(tools.flattenList(values_tree_files.values())) if ("datacards/channel" in root_file) or ("datacards/combined" in root_file)]))
						config["labels"] = [""]
						config["output_dir"] = os.path.join(output_dir, "datacards/combined/plots")
						config["filename"] += "_per_channel"
						if args.www:
							config["www"] = os.path.join(www, "combined/plots")
						plot_configs.append(config)
	
			if "category" in args.combinations:
				for template in ([
						"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/combine/best_fit_pol_over_category.json",
						"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/combine/best_fit_weinberg_angle_over_category.json",
				] if "maxlikelihoodfit" in args.steps else []) + ([
						"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/combine/best_fit_pol_over_category_tot_stat_unc.json",
						"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/combine/best_fit_pol_over_category_tot_unc.json",
						"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/combine/best_fit_pol_over_category_stat_unc.json",
						"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/combine/best_fit_weinberg_angle_over_category_tot_stat_unc.json",
						"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/combine/best_fit_weinberg_angle_over_category_tot_unc.json",
						"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/combine/best_fit_weinberg_angle_over_category_stat_unc.json",
				] if "totstatuncs" in args.steps else []): # if (scaled_lumi is None) and (asimov_polarisation is None) else []):
					
					x_values_raw = sorted([values[1] for values in values_tree_files.keys() if values[1] > -990.0])
					x_values = [(((value-1000.0)/10.0-1.0) if value > 1000.0 else value) for value in x_values_raw]
					config = jsonTools.JsonDict(os.path.expandvars(template))
					config["directories"] = [" ".join(set([os.path.dirname(root_file) for root_file in sorted(tools.flattenList(values_tree_files.values())) if ("datacards/category" in root_file) or ("datacards/combined" in root_file)]))]
					config["x_ticks"] = x_values
					inv_annotation_replacements = {value : key for key, value in annotation_replacements.iteritems() if (type(key) != int) or (key > 1000)}
					config["x_tick_labels"] = [str(inv_annotation_replacements.get(int(value), value)).replace("1020.0", "rho").replace("1030.0", "oneprong") for value in x_values_raw]
					config["x_lims"] = [min(x_values) - 0.5, max(x_values) + 0.5]
					config["output_dir"] = os.path.join(output_dir, "datacards/combined/plots")
					if args.www:
						config["www"] = os.path.join(www, "combined/plots")
					plot_configs.append(config)
				
				if ("deltanll" in args.steps) and (scaled_lumi is None) and (asimov_polarisation is None):
					for template in [
							"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/combine/likelihood_ratio_over_pol.json",
					]:
						config = jsonTools.JsonDict(os.path.expandvars(template))
						config["directories"] = list(set([os.path.dirname(root_file) for root_file in sorted(tools.flattenList(values_tree_files.values())) if ("datacards/category" in root_file) or ("datacards/combined" in root_file)]))
						config["labels"] = [""]
						config["output_dir"] = os.path.join(output_dir, "datacards/combined/plots")
						config["filename"] += "_per_category"
						if args.www:
							config["www"] = os.path.join(www, "combined/plots")
						plot_configs.append(config)
			
			if ("deltanll" in args.steps) and (scaled_lumi is None) and (asimov_polarisation is None):
				for directory in set([os.path.dirname(root_file) for root_file in sorted(tools.flattenList(values_tree_files.values())) if "higgsCombineScan.MultiDimFit" in root_file]):
					for template in [
							"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/combine/likelihood_ratio_over_pol.json",
					]:
						config = jsonTools.JsonDict(os.path.expandvars(template))
						config["directories"] = [directory]
						config["labels"] = [""]
						config["output_dir"] = os.path.join(directory, "plots")
						if args.www:
							config["www"] = os.path.join(www, os.path.join(directory).replace(os.path.join(output_dir, "datacards"), "").strip("/"), "plots")
						plot_configs.append(config)
		
		if len(args.check_linearity) > 0:
			for template in ([
				"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/combine/best_fit_pol_over_polarisation.json",
			] if "maxlikelihoodfit" in args.steps else []) + ([
					"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/combine/best_fit_pol_over_polarisation_tot_stat_unc.json",
					"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/combine/best_fit_pol_over_polarisation_tot_unc.json",
					"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/combine/best_fit_pol_over_polarisation_stat_unc.json",
			] if "totstatuncs" in args.steps else []): # if (scaled_lumi is None) and (asimov_polarisation is None) else []): (scaled_lumi is None) and (asimov_polarisation is None) else []):
				
				config = jsonTools.JsonDict(os.path.expandvars(template))
				config["directories"] = [" ".join(set([os.path.dirname(root_file) for root_file in sorted(tools.flattenList(polarisation_values_tree_files.values())) if "datacards/combined" in root_file])).replace("/pol{:04}/".format(int(args.check_linearity[-1]*1000)), "/*/")]
				config["x_rel_lims"] = [0.95, 1.05]
				config["output_dir"] = os.path.join(args.output_dir, "pol/datacards/combined/plots")
				if args.www:
					config["www"] = os.path.join(args.www, "pol/combined/plots")
				plot_configs.append(config)
		
		# scale back to preserve initial state
		if not scaled_lumi is None:
			datacards.scale_expectation(args.lumi / scaled_lumi)
	
	higgsplot.HiggsPlotter(list_of_config_dicts=plot_configs, list_of_args_strings=[args.args], n_processes=args.n_processes, n_plots=args.n_plots[1])

