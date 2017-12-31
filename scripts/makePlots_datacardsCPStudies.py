#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import argparse
import copy
import numpy
import os

import Artus.Utility.tools as tools
import Artus.HarryPlotter.utility.plotconfigs as plotconfigs
import Artus.Utility.jsonTools as jsonTools

import HiggsAnalysis.KITHiggsToTauTau.plotting.higgsplot as higgsplot
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.samples_run2_2016 as samples
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.binnings as binnings
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.systematics_run2 as systematics
import HiggsAnalysis.KITHiggsToTauTau.datacards.cpstudiesdatacards as cpstudiesdatacards


def _call_command(command):
	log.debug(command)
	logger.subprocessCall(command, shell=True)


if __name__ == "__main__":

	parser = argparse.ArgumentParser(description="Create ROOT inputs and datacards for CP studies.",
	                                 parents=[logger.loggingParser])

	parser.add_argument("-i", "--input-dir", required=True,
	                    help="Input directory.")
	parser.add_argument("-c", "--channel", action="append",
	                    default=["all"],
	                    help="Channel. This agument can be set multiple times. [Default: %(default)s]")
	parser.add_argument("--cp-mixings", nargs="+", type=float,
                        default=list(numpy.arange(0.0, 1.001, 0.05)),
                        help="CP mixing angles alpha_tau (in units of pi/2) to be probed. [Default: %(default)s]")
	parser.add_argument("--cp-mixing-scan-points", type=int, default=((len(parser.get_default("cp_mixings"))-1)*4)+1,
                        help="Number of points for CP mixing angles alpha_tau (in units of pi/2) to be scanned. [Default: %(default)s]")
	parser.add_argument("--categories", action="append", nargs="+",
	                    default=[["all"]] * len(parser.get_default("channel")),
	                    help="Categories per channel. This argument needs to be set as often as --channels. [Default: %(default)s]")
	parser.add_argument("-m", "--higgs-masses", nargs="+", default=["120", "130", "125"], # we do not have 125 GeV MSSM samples
	                    help="Higgs masses. The first mass defines the mass of interest and additional masses are used to increase the statistics by preserving the yield given by the first mass. [Default: %(default)s]")
	parser.add_argument("-x", "--quantity", default="0",
	                    help="Quantity. [Default: %(default)s]")
	parser.add_argument("--no-bbb-uncs", action="store_true", default=False,
	                    help="Do not add bin-by-bin uncertainties. [Default: %(default)s]")
	parser.add_argument("--lumi", type=float, default=samples.default_lumi/1000.0,
	                    help="Luminosity for the given data in fb^(-1). [Default: %(default)s]")
	parser.add_argument("-w", "--weight", default="1.0",
	                    help="Additional weight (cut) expression. [Default: %(default)s]")
	parser.add_argument("--add-data", action="store_true", default=False,
	                    help="Use data instead of an asimov dataset. [Default: %(default)s]")
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
	                    default="$CMSSW_BASE/src/plots/htt_datacards/",
	                    help="Output directory. [Default: %(default)s]")
	parser.add_argument("--clear-output-dir", action="store_true", default=False,
	                    help="Delete/clear output directory before running this script. [Default: %(default)s]")
	parser.add_argument("--scale-lumi", default=False,
                        help="Scale datacard to luminosity specified. [Default: %(default)s]")
	parser.add_argument("--era", default="2016",
	                    help="Era of samples to be used. [Default: %(default)s]")
	parser.add_argument("--no-ewk-samples", default=False, action="store_true",
	                    help="Do not use EWK Z/W samples. [Default: %(default)s]")
	parser.add_argument("--no-ewkz-as-dy", default=False, action="store_true",
	                    help="Do not include EWKZ samples in inputs for DY. [Default: %(default)s]")
	parser.add_argument("--no-shape-uncs", default=False, action="store_true",
	                    help="Do not include shape-uncertainties. [Default: %(default)s]")

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
	cp_mixing_angles_over_pi_half = ["{mixing:03d}".format(mixing=int(mixing*100)) for mixing in args.cp_mixings]
	cp_mixings_str = ["{mixing:0.2f}".format(mixing=mixing) for mixing in args.cp_mixings]

	cp_mixings_scan = list(numpy.arange(args.cp_mixings[0], args.cp_mixings[-1]+0.001, (args.cp_mixings[-1]-args.cp_mixings[0])/(args.cp_mixing_scan_points-1)))
	cp_mixings_combine_range_min = (3*cp_mixings_scan[0]-cp_mixings_scan[1]) / 2.0
	cp_mixings_combine_range_max = (3*cp_mixings_scan[-1]-cp_mixings_scan[-2]) / 2.0

	# initialisations for plotting
	sample_settings = samples.Samples()
	binnings_settings = binnings.BinningsDict()
	systematics_factory = systematics.SystematicsFactory()

	plot_configs = []
	output_files = []
	merged_output_files = []
	hadd_commands = []

	datacards = cpstudiesdatacards.CPStudiesDatacards(cp_mixings_str, add_data=True) # add_data=args.add_data)

	# initialise datacards
	tmp_input_root_filename_template = "input/${ANALYSIS}_${CHANNEL}_${BIN}_${SYSTEMATIC}_${ERA}.root"
	input_root_filename_template = "input/${ANALYSIS}_${CHANNEL}_${BIN}_${ERA}.root"
	bkg_histogram_name_template = "${BIN}/${PROCESS}"
	sig_histogram_name_template = "${BIN}/${PROCESS}${MASS}"
	bkg_syst_histogram_name_template = "${BIN}/${PROCESS}_${SYSTEMATIC}"
	sig_syst_histogram_name_template = "${BIN}/${PROCESS}${MASS}_${SYSTEMATIC}"
	datacard_filename_templates = [
		"datacards/individual/${CHANNEL}/${BINID}/${ANALYSIS}_${CHANNEL}_${BINID}_${ERA}.txt",
		"datacards/channel/${CHANNEL}/${ANALYSIS}_${CHANNEL}_${ERA}.txt",
		"datacards/category/${BINID}/${ANALYSIS}_${BINID}_${ERA}.txt",
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

	# restrict combine to lnN systematics only if no_shape_uncs is set
	if args.no_shape_uncs:
		log.debug("Deactivate shape uncertainties")
		datacards.cb.FilterSysts(lambda systematic : systematic.type() == "shape")
		if log.isEnabledFor(logging.DEBUG):
			datacards.cb.PrintSysts()

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
			datacards_per_channel_category = cpstudiesdatacards.CPStudiesDatacards(cb=datacards.cb.cp().channel([channel]).bin([category]))

			higgs_masses = args.higgs_masses[:1]
			additional_higgs_masses_for_shape = args.higgs_masses[1:]

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
				list_of_bkg_samples = [datacards.configs.process2sample(process) for process in list_of_samples if process in datacards_per_channel_category.cb.cp().backgrounds().process_set()]
				list_of_sig_samples = [datacards.configs.process2sample(process) for process in list_of_samples if process in datacards_per_channel_category.cb.cp().signals().process_set()]

				for shift_up in ([True] if nominal else [True, False]):
					systematic = "nominal" if nominal else (shape_systematic + ("Up" if shift_up else "Down"))


					# prepare plotting configs for retrieving the input histograms
					
					#TODO: Check which cut_type should be used and whether baseline2016 is up-to-date
					config={}

					log.debug("Create inputs for (samples, systematic) = ([\"{samples}\"], {systematic}), (channel, category) = ({channel}, {category}).".format(
							samples="\", \"".join((["data"] if nominal and args.add_data else []) + list_of_bkg_samples),
							channel=channel,
							category=category,
							systematic=systematic
					))
					config_bkg = sample_settings.get_config(
							samples=[getattr(samples.Samples, sample) for sample in (["data"] if nominal and args.add_data else []) + list_of_bkg_samples],
							channel=channel,
							category="catHtt13TeV_"+category,
							weight=args.weight,
							cut_type = "baseline2016",
							lumi=args.lumi * 1000,
							no_ewk_samples = args.no_ewk_samples,
							no_ewkz_as_dy = args.no_ewkz_as_dy
					)


					config_bkg["labels"] = [(bkg_histogram_name_template if nominal else bkg_syst_histogram_name_template).replace("$", "").format(
						PROCESS=datacards.configs.sample2process(sample),
						BIN=category,
						SYSTEMATIC=systematic
					) for sample in config_bkg["labels"]]
					config = samples.Samples.merge_configs(config, config_bkg)

					for cp_mixing, cp_mixing_angle_over_pi_half, cp_mixing_str in zip(args.cp_mixings, cp_mixing_angles_over_pi_half, cp_mixings_str):
						tmp_additional_higgs_masses_for_shape = copy.deepcopy(additional_higgs_masses_for_shape)
						if (cp_mixing > 0.5) and ("125" in tmp_additional_higgs_masses_for_shape):
							tmp_additional_higgs_masses_for_shape.remove("125")

						log.debug("Create inputs for (samples, systematic) = ([\"{samples}\"], {systematic}), (channel, category) = ({channel}, {category}).".format(
								samples="\", \"".join(list_of_sig_samples),
								channel=channel,
								category=category,
								systematic=systematic
						))
						config_sig = sample_settings.get_config(
								samples=[getattr(samples.Samples, sample) for sample in list_of_sig_samples],
								channel=channel,
								category="catHtt13TeV_"+category,
								nick_suffix="_"+cp_mixing_str,
								weight=args.weight+"*"+"tauSpinnerWeightInvSample"+"*tauSpinnerWeight"+cp_mixing_angle_over_pi_half,
								lumi=args.lumi * 1000,
								higgs_masses=higgs_masses,
								cut_type = "baseline2016",
								additional_higgs_masses_for_shape=tmp_additional_higgs_masses_for_shape,
								mssm=None,
								normalise_to_sm_xsec=False
						)
						config_sig["labels"] = [(sig_histogram_name_template if nominal else sig_syst_histogram_name_template).replace("$", "").format(
								PROCESS=datacards.configs.sample2process(sample).replace("120", "").replace("125", "").replace("130", ""),
								BIN=category,
								MASS=cp_mixing_str,
								SYSTEMATIC=systematic
						) for sample in config_sig["labels"]]

						config = samples.Samples.merge_configs(config, config_sig, additional_keys=["shape_nicks", "yield_nicks", "shape_yield_nicks"])

					if "stacks" in config:
						config.pop("stacks")

					# create asimov dataset
					if not args.add_data:
						if not "SumOfHistograms" in config.get("analysis_modules", []):
							config.setdefault("analysis_modules", []).append("SumOfHistograms")
						nicks_to_sum = copy.deepcopy(list_of_bkg_samples)
						nicks_to_sum.extend([sample+higgs_masses[0]+"_{mixing:0.2f}".format(mixing=min(args.cp_mixings)) for sample in list_of_sig_samples])
						config.setdefault("sum_nicks", []).append(" ".join(nicks_to_sum))
						config.setdefault("sum_result_nicks", []).append("asimov_s")
						config.setdefault("labels", []).insert(0, (bkg_histogram_name_template if nominal else bkg_syst_histogram_name_template).replace("$", "").format(
								PROCESS=datacards.configs.sample2process("data"),
								BIN=category,
								SYSTEMATIC=systematic
						))
						config.setdefault("colors", []).insert(0, "data")
						config.setdefault("markers", []).insert(0, "data")

					systematics_settings = systematics_factory.get(shape_systematic)(config)
					# TODO: evaluate shift from datacards_per_channel_category.cb
					config = systematics_settings.get_config(shift=(0.0 if nominal else (1.0 if shift_up else -1.0)))

					config["x_expressions"] = [args.quantity]

					binnings_key = "binningHtt13TeV_"+category+"_svfitMass"
					if binnings_key in binnings_settings.binnings_dict:
						config["x_bins"] = [binnings_key]
					else:
						config["x_bins"] = ["30,0.0,6.28"]

					config["directories"] = [args.input_dir]

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
			merged_output_files.append(output_file)

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
	for output_file in merged_output_files:
		debug_plot_configs.extend(plotconfigs.PlotConfigs().all_histograms(output_file, plot_config_template={"markers":["E"], "colors":["#FF0000"]}))
	higgsplot.HiggsPlotter(list_of_config_dicts=debug_plot_configs, list_of_args_strings=[args.args], n_processes=args.n_processes, n_plots=args.n_plots[0])

	# update CombineHarvester with the yields and shapes
	datacards.extract_shapes(
			os.path.join(args.output_dir, input_root_filename_template.replace("$", "")),
			bkg_histogram_name_template, sig_histogram_name_template,
			bkg_syst_histogram_name_template, sig_syst_histogram_name_template,
			update_systematics=True
	)

	# signals morphing according to alpha_tau / (pi/2)
	datacards.create_morphing_signals("cpmixing", 0.0, 0.0, 1.0)

	# add bin-by-bin uncertainties
	if not args.no_bbb_uncs:
		datacards.add_bin_by_bin_uncertainties(
				processes=datacards.cb.cp().backgrounds().process_set(),
				add_threshold=0.1, merge_threshold=0.5, fix_norm=True
		)

	# scale
	if(args.scale_lumi):
		datacards.scale_expectation(float(args.scale_lumi) / args.lumi)

	# write datacards and call text2workspace
	datacards_cbs = {}
	for datacard_filename_template in datacard_filename_templates:
		datacards_cbs.update(datacards.write_datacards(
				datacard_filename_template.replace("{", "").replace("}", ""),
				output_root_filename_template.replace("{", "").replace("}", ""),
				args.output_dir
		))

	datacards_workspaces = datacards.text2workspace(datacards_cbs, n_processes=args.n_processes)

	result_plot_configs = []

	# Max. likelihood fit and postfit plots
	datacards.combine(
			datacards_cbs,
			datacards_workspaces,
			None,
			args.n_processes,
			"-M FitDiagnostics --saveShapes --redefineSignalPOIs cpmixing --expectSignal=1 -t -1 --setParameters cpmixing=0.0 {stable} -n \"\"".format(stable=datacards.stable_options)
	)

	datacards_postfit_shapes = datacards.postfit_shapes_fromworkspace(datacards_cbs, datacards_workspaces, False, args.n_processes, "--sampling" + (" --print" if args.n_processes <= 1 else ""))
	datacards.prefit_postfit_plots(datacards_cbs, datacards_postfit_shapes, plotting_args={"ratio" : args.ratio, "args" : args.args, "lumi" : args.lumi, "x_expressions" : args.quantity}, n_processes=args.n_processes)

	datacards.pull_plots(datacards_postfit_shapes, s_fit_only=False, plotting_args={"fit_poi" : ["cpmixing"], "formats" : ["pdf", "png"]}, n_processes=args.n_processes)
	datacards.print_pulls(datacards_cbs, args.n_processes, "-A -p {POI}".format(POI="cpmixing"))

	datacards.combine(
			datacards_cbs,
			datacards_workspaces,
			None,
			args.n_processes,
			"-M MultiDimFit --algo grid --redefineSignalPOIs cpmixing --expectSignal=1 -t -1 --setParameters cpmixing=0.0 --setParameterRanges cpmixing={RANGE} --points {POINTS} {STABLE} -n \"\"".format(
					STABLE=datacards.stable_options,
					RANGE="{0:f},{1:f}".format(cp_mixings_combine_range_min, cp_mixings_combine_range_max),
					POINTS=args.cp_mixing_scan_points
			)
	)

	for datacard, workspace in datacards_workspaces.iteritems():
		config = jsonTools.JsonDict(os.path.expandvars("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/combine/likelihood_ratio_alphatau.json"))
		config["directories"] = [os.path.dirname(workspace)]
		config["labels"] = ["TODO"]
		config["output_dir"] = os.path.join(os.path.dirname(workspace), "plots")
		config["filename"] = "likelihoodScan"
		result_plot_configs.append(config)

	if log.isEnabledFor(logging.DEBUG):
		import pprint
		pprint.pprint(plot_configs)

	higgsplot.HiggsPlotter(list_of_config_dicts=result_plot_configs, list_of_args_strings=[args.args], n_processes=args.n_processes, n_plots=args.n_plots[1])
