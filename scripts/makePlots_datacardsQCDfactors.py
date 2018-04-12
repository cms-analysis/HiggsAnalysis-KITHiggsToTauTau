#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import argparse
import array
import copy
import os
import sys

import CombineHarvester.CombineTools.ch as ch
import CombineHarvester.CombinePdfs.morphing as morphing
import ROOT

import Artus.Utility.tools as tools
import Artus.Utility.jsonTools as jsonTools

import HiggsAnalysis.KITHiggsToTauTau.plotting.higgsplot as higgsplot
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.samples_run2_2016 as samples
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.systematics_run2 as systematics
import HiggsAnalysis.KITHiggsToTauTau.datacards.qcdfactorsdatacards as qcdfactorsdatacards


def addArguments(parser):
	parser.add_argument("-i", "--input-dir", required=True,
	                    help="Input directory.")
	parser.add_argument("-x", "--quantity", default="m_vis", choices=["m_vis"], 
	                    help="Quantity ot perform fit in sideband region. [Default: %(default)s]")
	parser.add_argument("-c", "--channels", nargs="*", default=["mt","et"],
	                    help="Select final state(s) for measurement. This argument can be set multiple times. [Default: %(default)s]")
	parser.add_argument("--categories", nargs="+", action = "append",
	                    help="Categories per channel. This argument needs to be set as often as --channels. [Default: %(default)s]")
	parser.add_argument("--no-bbb-uncs", action="store_true", default=False,
	                    help="Do not add bin-by-bin uncertainties. [Default: %(default)s]")
	parser.add_argument("--lumi", type=float, default=samples.default_lumi/1000.0,
	                    help="Luminosity for the given data in fb^(-1). [Default: %(default)s]")
	parser.add_argument("-a", "--args", default="",
	                    help="Additional Arguments for HarryPlotter. [Default: %(default)s]")
	parser.add_argument("-n", "--n-processes", type=int, default=1,
	                    help="Number of (parallel) processes. [Default: %(default)s]")
	parser.add_argument("-f", "--n-plots", type=int, nargs=2, default=[None, None],
	                    help="Number of plots for datacard inputs (1st arg) and for postfit plots (2nd arg). [Default: all]")
	parser.add_argument("-o", "--output-dir",
	                    default="$CMSSW_BASE/src/plots/tauEsStudies_datacards/",
	                    help="Output directory. [Default: %(default)s]")
	parser.add_argument("--clear-output-dir", action="store_true", default=False,
	                    help="Delete/clear output directory before running this script. [Default: %(default)s]")
	parser.add_argument("--combine-verbosity", default="1", choices=["-1","0","1","2"],
	                    help="Control output amount of combine. [Default: %(default)s]")
	parser.add_argument("--www", nargs="?", default=None, const="",
	                    help="Publish plots. [Default: %(default)s]")
	parser.add_argument("--era", default="2016",
	                    help="Era of samples to be used. [Default: %(default)s]")
	parser.add_argument("-b", "--background-method", default="new",
	                    help="Background estimation method to be used. [Default: %(default)s]")
	parser.add_argument("--use-scan-without-fit", action="store_true", default=False,
	                    help="Obtain result from likelihood scan without fitting the parabola but instead finding the minimum and the first points crossing 1 on either side. [Default: %(default)s]")
	parser.add_argument("-w", "--weight", default="(1.0)",
	                    help="Additional weight used for both background and all signal templates. [Default: %(default)s]")
	parser.add_argument("--cms", action="store_true", default=False,
	                    help="Display CMS Preliminary on plot. [Default: %(default)s]")
	parser.add_argument("--pdf", action="store_true", default=False,
	                    help="Produce pdf versions of all plots. [Default: %(default)s]")
	parser.add_argument("--no-inclusive", action="store_true", default=False,
	                    help="Do not produce inclusive results if pt or eta ranges are given. [Default: %(default)s]")
	parser.add_argument("--plot-nuisance-impacts", action="store_true", default=False,
	                    help="Produce nuisance impact plots. [Default: %(default)s]")

def _call_command(args):
	command = None
	cwd = None
	if isinstance(args, basestring):
		command = args
	else:
		command = args[0]
		if len(args) > 1:
			cwd = args[1]

	old_cwd = None
	if not cwd is None:
		old_cwd = os.getcwd()
		os.chdir(cwd)

	log.debug(command)
	logger.subprocessCall(command, shell=True)

	if not cwd is None:
		os.chdir(old_cwd)

if __name__ == "__main__":

	parser = argparse.ArgumentParser(description="Create ROOT inputs and datacards for the measurement of the QCD 0S/SS factor from data in a sideband region.",
	                                 parents=[logger.loggingParser])
	addArguments(parser)

	args = parser.parse_args()
	logger.initLogger(args)
	
				
	# Initialisations for plotting
	if (args.era == "2015") or (args.era == "2015new"):
		import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.samples_run2_2015 as samples
	else:
		import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.samples_run2_2016 as samples
		if args.lumi == parser.get_default("lumi"):
			args.lumi = samples.default_lumi/1000.0

	# Clean the output dir	
	args.output_dir = os.path.abspath(os.path.expandvars(args.output_dir))
	if args.clear_output_dir:
		clear_output_dir = raw_input("Do you really want to clear the output directory? [yes]").lower() == "yes"
		if not clear_output_dir:
			log.info("Terminate. Remove the clear_output_dir option and run the programm again.")
			sys.exit(1)
		logger.subprocessCall("rm -r " + args.output_dir, shell=True)			
			
	sample_settings = samples.Samples()
	systematics_factory = systematics.SystematicsFactory()
	www_output_dirs_postfit = []
	www_output_dirs_weightbin = []
	www_output_dirs_parabola = []
	
	# Initialise datacards
	tmp_input_root_filename_template = "input/${ANALYSIS}_${CHANNEL}_${BIN}_${SYSTEMATIC}_${ERA}.root"
	input_root_filename_template = "input/${ANALYSIS}_${CHANNEL}_${BIN}_${ERA}.root"
	bkg_histogram_name_template = "${BIN}/${PROCESS}"
	sig_histogram_name_template = "${BIN}/${PROCESS}${MASS}"
	bkg_syst_histogram_name_template = "${BIN}/${PROCESS}_${SYSTEMATIC}"
	sig_syst_histogram_name_template = "${BIN}/${PROCESS}${MASS}_${SYSTEMATIC}"
	datacard_filename_templates = ["datacards/${BIN}/${ANALYSIS}_${CHANNEL}_${BIN}_${ERA}.txt"]
	if len(args.channels) > 1:
		datacard_filename_templates.append("datacards/decaymode/${BINID}/${ANALYSIS}_${BINID}_${ERA}.txt")
	output_root_filename_template = "datacards/common/${ANALYSIS}.input_${ERA}.root"
	
	# define the quantity for the sideband region
	quantity = args.quantity
	
	# Build categories and bin id's for CombineHarvester
	categories = [channel+"_"+category for channel in args.channels for category in args.categories[0]]
	mapping_category2binid = {}
		
	if args.categories != parser.get_default("categories"):
		args.categories = args.categories[1:]
			
	# catch if on command-line only one set has been specified and repeat it
	if(len(args.categories) == 1):
		args.categories = [args.categories[0]] * len(args.channel)
		
	# Restrict CombineHarvester to configured channels:
	datacards = qcdfactorsdatacards.QcdFactorsDatacards(quantity, args.era, mapping_category2binid)
	
	datacards.cb.channel(args.channels)
	datacards.cb.PrintAll()
	
	for category in categories:
		channel = category.split("_")[0]
	
		# use relaxed isolation criteria for W+jets and QCD estimation
		# if measurement is performed in bins of pt or eta
		useRelaxedIsolation = False

		output_file = os.path.join(args.output_dir, input_root_filename_template.replace("$", "").format(
			ANALYSIS="ztt",
			CHANNEL=channel,
			BIN=category,
			ERA="13TeV"
		))
		
		input_plot_configs = []
		hadd_commands = []
		
		datacards_per_channel_category = qcdfactorsdatacards.QcdFactorsDatacards(cb=datacards.cb.cp().channel([channel]).bin([category]), mapping_category2binid=mapping_category2binid)

		tmp_output_files = []

		for shape_systematic, list_of_samples in datacards_per_channel_category.get_samples_per_shape_systematic().iteritems():
			print(shape_systematic, list_of_samples)
			nominal = (shape_systematic == "nominal")
			list_of_samples = [datacards.configs.process2sample(process) for process in list_of_samples]
			print(list_of_samples)

			
			for shift_up in ([True] if nominal else [True, False]):
				systematic = "nominal" if nominal else (shape_systematic + ("Up" if shift_up else "Down"))
		
				log.debug("Create inputs for (samples, systematic) = ([\"{samples}\"], {systematic}), (channel, category) = ({channel}, {category}).".format(
					samples="\", \"".join(list_of_samples),
					channel=channel,
					category=category,
					systematic=systematic
				))


				merged_config={}

				config_rest = sample_settings.get_config(
					samples=[getattr(samples.Samples, sample) for sample in list_of_samples if sample not in ["qcd"]],
					channel=channel,
					category=category,
					nick_suffix="_",
					weight=args.weight,
					lumi=args.lumi * 1000,
					cut_type="smhtt2016" if args.era == "2016" else "tauescuts",
					estimationMethod="classic", 
					useRelaxedIsolationForW = useRelaxedIsolation,
					useRelaxedIsolationForQCD = useRelaxedIsolation
				)
				
				config_rest["x_expressions"] = [quantity]
				histogram_name_template = bkg_histogram_name_template if nominal else bkg_syst_histogram_name_template
				config_rest["labels"] = [histogram_name_template.replace("$", "").format(
					PROCESS=datacards.configs.sample2process(sample),
					BIN=category,
					SYSTEMATIC=systematic
				) for sample in config_rest["labels"]]

				systematics_settings = systematics_factory.get(shape_systematic)(config_rest)
				config_rest = systematics_settings.get_config(shift=(0.0 if nominal else (1.0 if shift_up else -1.0)))
				
				# Merge configs
				merged_config = samples.Samples.merge_configs(merged_config, config_rest)
				
				# One ztt nick config for each es shift
				for shift in es_shifts:
					if list(set(list_of_samples) & set(["ztt", "ttt", "vvt"])) == []: continue
					
					config_ztt = sample_settings.get_config(
						samples=[getattr(samples.Samples, sample) for sample in list_of_samples if sample in ["ztt", "ttt", "vvt"]],
						channel=channel,
						category=catForConfig,
						nick_suffix="_" + str(shift).replace(".", "_") + "_" + str(weight_index),
						weight="(pt_2>20)*" + args.weight,
						lumi=args.lumi * 1000,
						cut_type="tauescuts2016" if args.era == "2016" else "tauescuts",
						estimationMethod=args.background_method,
						wj_sf_shift=wj_sf_shift,
						ss_os_factor = ss_os_factors.get(channel,0.0),
						useRelaxedIsolation = useRelaxedIsolation
					)
					# Shift also pt to account for acceptance effects
					config_ztt["weights"] = [weight.replace("pt_2","("+str(shift)+"*pt_2)") for weight in config_ztt["weights"]]
					
					if decayMode == "OneProng" and quantity == "m_2":
						log.error("Tau mass (m_2) fit not possible in 1prong decay mode")
						sys.exit(1)
					if quantity == "m_2":
						config_ztt["x_expressions"] = [quantity + "*" + str(shift) + "*" + extra_weights[weight_index].replace("pt_2","("+str(shift)+"*pt_2)")] * len(config_ztt["nicks"])
					elif quantity == "m_vis":
						config_ztt["x_expressions"] = [quantity + "*sqrt(" + str(shift) + ")" + "*" + extra_weights[weight_index].replace("pt_2","("+str(shift)+"*pt_2)")] * len(config_ztt["nicks"])
					
					systematics_settings = systematics_factory.get(shape_systematic)(config_ztt)
					config_ztt = systematics_settings.get_config(shift=(0.0 if nominal else (1.0 if shift_up else -1.0)))
					
					histogram_name_template = sig_histogram_name_template if nominal else sig_syst_histogram_name_template
					config_ztt["labels"] = [histogram_name_template.replace("$", "").format(
						PROCESS=datacards.configs.sample2process(sample),
						BIN=category,
						MASS=str(shift),
						SYSTEMATIC=systematic
					) for sample in config_ztt["labels"]]
					
					# Merge configs
					merged_config = samples.Samples.merge_configs(merged_config, config_ztt)
		
				merged_config["directories"] = [args.input_dir]
		
				histogram_name_template = bkg_histogram_name_template if nominal else bkg_syst_histogram_name_template
		
				tmp_output_file = os.path.join(args.output_dir, tmp_input_root_filename_template.replace("$", "").format(
					ANALYSIS="ztt",
					CHANNEL=channel,
					BIN=category,
					SYSTEMATIC=systematic,
					ERA="13TeV"
				))
				tmp_output_files.append(tmp_output_file)
				merged_config["output_dir"] = os.path.dirname(tmp_output_file)
				merged_config["filename"] = os.path.splitext(os.path.basename(tmp_output_file))[0]
	
				merged_config["plot_modules"] = ["ExportRoot"]
				merged_config["file_mode"] = "UPDATE"
					
				# Set proper binnings of the distributions
				if decayMode == "OneProngPiZeros" and quantity == "m_2":
					if args.tighten_mass_window:
						merged_config["weights"] = [weight+"*(m_2 >= 0.318)*(m_2 < 1.41)" for weight in merged_config["weights"]]
					merged_config.setdefault("x_bins", []).append(["12,0.3,1.5"])
				elif decayMode == "ThreeProng" and quantity == "m_2":
					if args.tighten_mass_window:
						merged_config["weights"] = [weight+"*(m_2 >= 0.848)*(m_2 < 1.41)" for weight in merged_config["weights"]]
					merged_config.setdefault("x_bins", []).append(["7,0.8,1.5"])
				elif decayMode == "AllDMs" and quantity != "m_vis":
					merged_config.setdefault("x_bins", []).append(["12,0.3,1.5"])
				elif decayMode == "OneProng" or quantity == "m_vis":
					merged_config.setdefault("x_bins", []).append(["40,0.0,200.0"])
					merged_config.setdefault("custom_rebin", []).append([40,45,50,55,60,65,70,75,80,85])
				
				input_plot_configs.append(merged_config)
		
		hadd_commands.append("hadd -f {DST} {SRC} && rm {SRC}".format(
			DST=output_file,
			SRC=" ".join(tmp_output_files)
		))

		# Delete existing output files
		output_files = list(set([os.path.join(config["output_dir"], config["filename"]+".root") for config in input_plot_configs[:args.n_plots[0]]]))
		for output_file in output_files:
			if os.path.exists(output_file):
				os.remove(output_file)
				log.debug("Removed file \""+output_file+"\" before it is recreated again.")
	
		# Create input histograms with HarryPlotter
		higgsplot.HiggsPlotter(list_of_config_dicts=input_plot_configs, n_processes=args.n_processes, n_plots=args.n_plots[0])
		if args.n_plots[0] != 0:
			tools.parallelize(_call_command, hadd_commands, n_processes=args.n_processes)
	
	# Update CombineHarvester with the yields and shapes
	datacards.extract_shapes(
		os.path.join(args.output_dir, input_root_filename_template.replace("$", "")),
		bkg_histogram_name_template, sig_histogram_name_template,
		bkg_syst_histogram_name_template, sig_syst_histogram_name_template,
		update_systematics=True
	)
	sys.exit(0)
	# Create morphing
	datacards.create_morphing_signals("mes", 1.0, args.shift_ranges[0], args.shift_ranges[1])
	
	# Add bin-by-bin uncertainties
	if not args.no_bbb_uncs:
		datacards.add_bin_by_bin_uncertainties(
			processes=datacards.cb.cp().backgrounds().process_set()+datacards.cb.cp().signals().process_set(),
			add_threshold=0.1, merge_threshold=0.5, fix_norm=False
		)
	
	# remove processes with zero yield
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
		null_yield = not proc.rate() > 0.
		if null_yield:
			datacards.cb.FilterSysts(lambda systematic: matching_process(proc,systematic))
		return null_yield
	
	datacards.cb.FilterProcs(remove_procs_and_systs_with_zero_yield)
	
	# Write datacards and call text2workspace
	datacards_cbs = {}
	for datacard_filename_template in datacard_filename_templates:
		datacards_cbs.update(datacards.write_datacards(
				datacard_filename_template.replace("{", "").replace("}", ""),
				output_root_filename_template.replace("{", "").replace("}", ""),
				args.output_dir
		))
	
	datacards_workspaces = datacards.text2workspace(datacards_cbs, n_processes=args.n_processes)
	
	# Combine call
	# Important: redefine the POI of the fit, such that is the es-shift and not the signal scale modifier (r)
	datacards.combine(
			datacards_cbs,
			datacards_workspaces,
			None,
			args.n_processes,
			"-M MaxLikelihoodFit --redefineSignalPOIs mes -v {VERBOSITY} {STABLE}".format(
				VERBOSITY=args.combine_verbosity,
				STABLE=datacards.stable_options
			)
	)
	
	# 2nd combine call to get deltaNLL distribution
	# (always done, since the bestfit value and uncertainties are taken from this scan)
	datacards.combine(
			datacards_cbs,
			datacards_workspaces,
			None,
			args.n_processes,
			"-M MultiDimFit --algo grid --points {BINNING} --setParameterRanges mes={RANGE} --redefineSignalPOIs mes -v {VERBOSITY}  {STABLE}".format(
				BINNING=int((args.shift_ranges[1]-args.shift_ranges[0])/args.shift_binning),
				RANGE=str(args.shift_ranges[0])+","+str(args.shift_ranges[1]),
				VERBOSITY=args.combine_verbosity,
				STABLE=datacards.stable_options
			)
	)
	
	# Plot nuisance impacts
	datacards.print_pulls(datacards_cbs, args.n_processes, "-A -p {POI}".format(POI="mes"))
	if args.plot_nuisance_impacts:
		datacards.nuisance_impacts(datacards_cbs, datacards_workspaces, args.n_processes, "--redefineSignalPOIs mes")
	
	# Postfitshapes call
	datacards_postfit_shapes = datacards.postfit_shapes_fromworkspace(datacards_cbs, datacards_workspaces, True, args.n_processes, "--sampling" + (" --print" if args.n_processes <= 1 else ""))
	
	# Pull plots
	datacards.pull_plots(datacards_postfit_shapes, s_fit_only=True, plotting_args={"fit_poi" : ["mes"]}, n_processes=args.n_processes)
	
	# Plot postfit
	postfit_plot_configs = [] #reset list containing the plot configs
	bkg_plotting_order = ["ZTT", "ZL", "ZJ", "TTT","TTJJ", "VVT", "VVJ", "W", "QCD"]
	
	for level in ["prefit", "postfit"]:
		for datacard in datacards_cbs.keys():
			postfit_shapes = datacards_postfit_shapes.get("fit_s", {}).get(datacard)
			# do not produce plots for combination as there is no proper implementation for that
			if len(datacards_cbs[datacard].cp().bin_set()) > 1:
				continue
			for category in datacards_cbs[datacard].cp().bin_set():
				
				channel = category.split("_")[0]
				decayMode = category.split("_")[-2]
				weightBin = int(category.split("_")[-1].split(weight_type+"bin")[-1])

				if category not in datacard:
					continue
				
				bkg_process = datacards_cbs[datacard].cp().bin([category]).backgrounds().process_set()
				sig_process = datacards_cbs[datacard].cp().bin([category]).signals().process_set()
				
				processes = bkg_process + sig_process
				processes.sort(key=lambda process: bkg_plotting_order.index(process) if process in bkg_plotting_order else len(bkg_plotting_order))
				
				config = {}
				config.setdefault("analysis_modules", []).extend(["SumOfHistograms"])
				config.setdefault("sum_nicks", []).append("noplot_TotalBkg noplot_TotalSig")
				config.setdefault("sum_scale_factors", []).append("1.0 1.0")
				config.setdefault("sum_result_nicks", []).append("Total")
				
				processes_to_plot = list(processes)
				processes = [p.replace("ZL", "ZL_noplot").replace("ZJ", "ZJ_noplot").replace("TTT", "TTT_noplot").replace("TTJJ", "TTJJ_noplot").replace("VVT", "VVT_noplot").replace("VVJ", "VVJ_noplot").replace("W", "W_noplot") for p in processes]
				processes_to_plot = [p for p in processes if not "noplot" in p]
				processes_to_plot.insert(1, "TT")
				config["sum_nicks"].append("TTT_noplot TTJJ_noplot")
				config["sum_scale_factors"].append("1.0 1.0")
				config["sum_result_nicks"].append("TT")
				processes_to_plot.insert(2, "ZLL")
				config["sum_nicks"].append("ZL_noplot ZJ_noplot")
				config["sum_scale_factors"].append("1.0 1.0")
				config["sum_result_nicks"].append("ZLL")
				processes_to_plot.insert(3, "EWK")
				config["sum_nicks"].append("VVT_noplot VVJ_noplot W_noplot")
				config["sum_scale_factors"].append("1.0 1.0 1.0")
				config["sum_result_nicks"].append("EWK")
				
				config["files"] = [postfit_shapes]
				config["folders"] = [category+"_"+level]
				config["nicks"] = [processes + ["noplot_TotalBkg", "noplot_TotalSig", "data_obs"]]
				config["x_expressions"] = [p.strip("_noplot") for p in processes] + ["TotalBkg", "TotalSig", "data_obs"]
				config["stacks"] = ["bkg"]*len(processes_to_plot) + ["data"] + [""]
				config["labels"] = [label.lower() for label in processes_to_plot + ["totalbkg"] + ["data_obs"]]
				config["colors"] = [color.lower() for color in processes_to_plot + ["#000000 transgrey"] + ["data_obs"]]
				config["markers"] = ["HIST"]*len(processes_to_plot) + ["E2"] + ["E"]
				config["legend_markers"] = ["F"]*len(processes_to_plot) + ["F"] + ["ELP"]
				
				config["y_label"] = "Events / bin"
				if "OneProngPiZeros" in category and quantity == "m_2":
					config["x_label"] = "m_{#tau_{h}} (GeV)"
					config["x_lims"] = [0.3,1.5]
				elif "ThreeProng" in category and quantity == "m_2":
					config["x_label"] = "m_{#tau_{h}} (GeV)"
					config["x_lims"] = [0.8,1.5]
				elif "AllDMs" in category and quantity == "m_2":
					config["x_label"] = "m_{#tau_{h}} (GeV)"
					config["x_lims"] = [0.3,1.5]
				elif "OneProng" in category or quantity == "m_vis":
					config["x_label"] = "m_{#mu#tau_{h}} (GeV)"
					config["x_lims"] = [20,200]
				
				config.setdefault("analysis_modules", []).append("Ratio")
				config.setdefault("ratio_numerator_nicks", []).extend(["noplot_TotalBkg noplot_TotalSig", "data_obs"])
				config.setdefault("ratio_denominator_nicks", []).extend(["noplot_TotalBkg noplot_TotalSig"] * 2)
				config.setdefault("ratio_result_nicks", []).extend(["ratio_unc", "ratio"])
				config["ratio_denominator_no_errors"] = True
				config.setdefault("colors", []).extend(["#000000 transgrey", "#000000"])
				config.setdefault("markers", []).extend(["E2", "E"])
				config.setdefault("legend_markers", []).extend(["F", "ELP"])
				config.setdefault("labels", []).extend([""] * 2)
				config.setdefault("stacks", []).extend(["unc", "ratio"])
				config["legend"] = [0.7, 0.4, 0.92, 0.82]
				config["y_subplot_lims"] = [0.5, 1.5]
				config["y_subplot_label"] = "Obs./Exp."
				config["subplot_grid"] = True
				
				config["energies"] = [13.0]
				config["lumis"] = [float("%.1f" % args.lumi)]
				if args.cms:
					config["cms"] = True
					config["extra_text"] = "Preliminary"
				config["year"] = args.era
				config["output_dir"] = os.path.join(os.path.dirname(datacard), "plots")
				config["filename"] = level+"_"+category+("_tightenedMassWindow" if args.tighten_mass_window else "")
				if args.pdf:
					config["formats"] = ["png", "pdf"]
				
				config["texts"] = [decayMode_dict[decayMode]["label"]]
				config["texts_x"] = [0.52]
				config["texts_y"] = [0.81]
				if weightBin > 0:
					config["texts"].append(weight_strings[weightBin])
					config["texts_x"].append(0.52)
					config["texts_y"].append(0.74)
				if args.plot_with_shift:
					config["texts"].append("#tau_{h} ES " + ("+" if (float(args.plot_with_shift)-1.0) >0 else "") + str((float(args.plot_with_shift)-1.0)*100) + "%")
					config["texts_x"].append(0.52)
					if weightBin > 0:
						config["texts_y"].append(0.67)
					else:
						config["texts_y"].append(0.74)
				config["texts_size"] = [0.055]
				config["title"] = "channel_"+channel
				
				if not (config["output_dir"] in www_output_dirs_postfit):
					www_output_dirs_postfit.append(config["output_dir"])
				
				postfit_plot_configs.append(config)
	
	higgsplot.HiggsPlotter(list_of_config_dicts=postfit_plot_configs, n_processes=args.n_processes, n_plots=args.n_plots[1])

	# Compute parabola from NLL scan and from here extract the best fit value and the uncertainties.
	output_dict_mu, output_dict_errHi, output_dict_errLo = {}, {}, {}
	output_dict_scan_mu, output_dict_scan_errHi, output_dict_scan_errLo = {}, {}, {}
	output_dict_scan_fit_mu, output_dict_scan_fit_err = {}, {}
	
	parabola_plot_configs = []
	weightbin_plot_configs = []
	for datacard, cb in datacards_cbs.iteritems():
		
		filename_mlfit = os.path.join(os.path.dirname(datacard), "mlfit.root")
		file_mlfit = ROOT.TFile(filename_mlfit)
		tree_mlfit = file_mlfit.Get("tree_fit_sb")
		tree_mlfit.GetEntry(0)
		
		filename_multidimfit = os.path.join(os.path.dirname(datacard), "higgsCombineTest.MultiDimFit.mH0.root")
		
		# The if statement in the loop is a workaround for the combination of channels
		# if you know of a better way, feel free to try it :)
		for category_or_bin_id in (datacards_cbs[datacard].cp().bin_set() if len(datacards_cbs[datacard].cp().bin_set()) == 1 else datacards_cbs[datacard].cp().bin_id_set()):
			if str(category_or_bin_id) not in filename_multidimfit:
				continue

			category = datacards_cbs[datacard].cp().bin_set()[0]
			
			# Redefine category if performing combination
			if len(datacards_cbs[datacard].cp().bin_set()) > 1:
				# Only replace first occurence (otherwise etabin is replaced as well if channel is et)
				category = category.replace(category.split("_")[0], "combined", 1)
			channel = category.split("_")[0]
			decayMode = category.split("_")[-2]
			weightBin = category.split("_")[-1].split(weight_type+"bin")[-1]
			
			output_dict_mu.setdefault(channel + "_" + decayMode, {})[weightBin] = 0
			output_dict_errHi.setdefault(channel + "_" + decayMode, {})[weightBin] = 0
			output_dict_errLo.setdefault(channel + "_" + decayMode, {})[weightBin] = 0
			output_dict_scan_mu.setdefault(channel + "_" + decayMode, {})[weightBin] = 0
			output_dict_scan_errHi.setdefault(channel + "_" + decayMode, {})[weightBin] = 0
			output_dict_scan_errLo.setdefault(channel + "_" + decayMode, {})[weightBin] = 0
			output_dict_scan_fit_mu.setdefault(channel + "_" + decayMode, {})[weightBin] = 0
			output_dict_scan_fit_err.setdefault(channel + "_" + decayMode, {})[weightBin] = 0
			
			file_multidimfit = ROOT.TFile(filename_multidimfit)
			tree_multidimfit = file_multidimfit.Get("limit")
			mes_list = []
			deltaNLL_list = []
			deltaNLLshifted_list = []
			
			# The entry '0' contains the best shift and deltaNLL=0 --> start from 1
			for entry in range(1, tree_multidimfit.GetEntries()):
				tree_multidimfit.GetEntry(entry)
				mes_list.append(tree_multidimfit.mes)
				deltaNLL_list.append(2*tree_multidimfit.deltaNLL)
			
			file_multidimfit.Close()
			
			# Find minimum
			for index, (nll) in enumerate(deltaNLL_list):
				if index == 0:
					min_nll = deltaNLL_list[0]
					min_shift = mes_list[0]
				if min_nll > deltaNLL_list[index]:
					min_nll = deltaNLL_list[index]
					min_shift = mes_list[index]
			
			# Find left-right intercept for 1sigma uncertainty
			for index, (nll) in enumerate(deltaNLL_list):
				deltaNLLshifted_list.append(nll - min_nll)
			
			found2sigmaLow, found1sigmaLow, found1sigmaHi, found2sigmaHi = False, False, False, False
			err2sigmaLow,err1sigmaLow, err1sigmaHi, err2sigmaHi = 0.0, 0.0, 0.0, 0.0
			mes_list_nll_belowX = []
			nll_belowX = []
			
			# Gradually increase range of nll if less than 10 points are captured but stop at 100.
			# This is mostly interesting for very narrow parabolas like in the case of m_2 for 3-prongs
			nllMax = 10
			while (len(mes_list_nll_belowX) < 10 and nllMax < 100):
				for index, (nll) in enumerate(deltaNLLshifted_list):
					if (nll <= nllMax and mes_list[index] not in mes_list_nll_belowX and nll not in nll_belowX):
						mes_list_nll_belowX.append(mes_list[index])
						nll_belowX.append(nll)
				if (len(mes_list_nll_belowX) < 10):
					nllMax += 1
			if nllMax > 10:
				log.warning("nllMax > 10: check position of 1 and 2 sigma texts in parabola plot!")
			
			for index, (nll) in enumerate(deltaNLLshifted_list):
				if (mes_list[index] <= min_shift):
					if (nll <= 4.0 and not found2sigmaLow): #crossing 2-sigma line from the left
						found2sigmaLow = True
						if index > 0:
							err2sigmaLow = abs((mes_list[index-1]+mes_list[index])/2.0 - min_shift)
						else:
							err2sigmaLow = abs(mes_list[index] - min_shift)
					if (nll <= 1.0 and not found1sigmaLow): #crossing 1-sigma line from the left
						found1sigmaLow = True
						if index > 0:
							err1sigmaLow = abs((mes_list[index-1]+mes_list[index])/2.0 - min_shift)
						else:
							err1sigmaLow = abs(mes_list[index] - min_shift)
				else:
					if (nll >= 1.0 and not found1sigmaHi): #crossing 1-sigma line again
						found1sigmaHi = True
						if index < len(mes_list) - 1:
							err1sigmaHi = abs((mes_list[index]+mes_list[index+1])/2.0 - min_shift)
						else:
							err1sigmaHi = abs(mes_list[index] - min_shift)
					if (nll >= 4.0 and not found2sigmaHi): #crossing 2-sigma line again
						found2sigmaHi = True
						if index < len(mes_list) - 1:
							err2sigmaHi = abs((mes_list[index]+mes_list[index+1])/2.0 - min_shift)
						else:
							err2sigmaHi = abs(mes_list[index] - min_shift)
			
			# Values for parabola plot
			xvaluesF = []
			xvalues = ""
			yvalues = ""
			for index, (nll) in enumerate(deltaNLLshifted_list):
				xvaluesF.append((mes_list[index]-1.0)*100)
				xvalues += str((mes_list[index]-1.0)*100) + " "
				yvalues += str(nll) + " "
			
			# Values for fit
			xvaluesF_belowX = []
			for index, (nll) in enumerate(nll_belowX):
				xvaluesF_belowX.append((mes_list_nll_belowX[index]-1.0)*100)
			
			if len(xvaluesF_belowX) == 0:
				for nll in deltaNLLshifted_list:
					print str(nll)
				print decayMode
				print weightBin
			
			# Fill TGraphErrors for parabola fit
			RooFitGraph_Parabola = ROOT.TGraphErrors(
				len(xvaluesF),
				array.array("d", xvaluesF),
				array.array("d", deltaNLLshifted_list),
				array.array("d", [0.1]*len(xvaluesF)),
				array.array("d", [1.0*nllMax/10.0]*len(xvaluesF)) # this is an arbitrary value in order to be able to fit also not so smooth parabolas
			)
			
			# Fit function
			fitf = ROOT.TF1("f1","pol2",min(xvaluesF_belowX),max(xvaluesF_belowX))
			RooFitGraph_Parabola.Fit("f1","R")
			minimumScanFit = fitf.GetMinimumX(min(xvaluesF_belowX),max(xvaluesF_belowX))
			minimumScanFitY = fitf.GetMinimum(min(xvaluesF_belowX),max(xvaluesF_belowX))
			sigmaScanFit = abs(fitf.GetX(minimumScanFitY+1)-minimumScanFit)
			
			# Write parabola with fit result into file
			RooFitGraph_Parabola.GetYaxis().SetRangeUser(0,nllMax)
			graphfilename = os.path.join(os.path.dirname(datacard), "parabola_" + category + ("_tightenedMassWindow" if args.tighten_mass_window else "")+".root")
			graphfile = ROOT.TFile(graphfilename, "RECREATE")
			RooFitGraph_Parabola.Write()
			graphfile.Close()
		
			output_dict_mu[channel + "_" + decayMode][weightBin] = (tree_mlfit.mu-1.0)*100
			output_dict_errHi[channel + "_" + decayMode][weightBin] = tree_mlfit.muHiErr*100
			output_dict_errLo[channel + "_" + decayMode][weightBin] = tree_mlfit.muLoErr*100
			output_dict_scan_mu[channel + "_" + decayMode][weightBin] = (min_shift-1.0)*100
			output_dict_scan_errHi[channel + "_" + decayMode][weightBin] = err1sigmaHi*100
			output_dict_scan_errLo[channel + "_" + decayMode][weightBin] = err1sigmaLow*100
			output_dict_scan_fit_mu[channel + "_" + decayMode][weightBin] = minimumScanFit
			output_dict_scan_fit_err[channel + "_" + decayMode][weightBin] = sigmaScanFit
			
			config = {}
			config["input_modules"] = ["InputInteractive"]
			config["analysis_modules"] = ["AddLine"]
			config["x_label"] = "#tau_{h} ES (%)"
			config["y_label"] = "-2 \\\mathrm{ln} \\\mathscr{L}"
			config["x_lims"] = [(min(es_shifts) - 1.0) * 100, (max(es_shifts) - 1.0) * 100]
			config["y_lims"] = [0.0, nllMax]
			config["x_lines"] = ["-6 6"]
			config["y_lines"] = ["1 1", "4 4"]
			config["markers"] = ["P", "L", "L"]
			config["marker_styles"] = [20]
			config["line_styles"] = [2]
			config["colors"] = ["kBlack", "kBlue", "kBlue"]
			config["output_dir"] = os.path.join(os.path.dirname(datacard), "plots")
			config["filename"] = "parabola_" + category + ("_tightenedMassWindow" if args.tighten_mass_window else "")
			config["x_expressions"] = [xvalues]
			config["y_expressions"] = [yvalues]
			config["texts"] = [decayMode_dict[decayMode]["label"], "1#sigma", "2#sigma"]
			config["texts_x"] = [0.78, 0.98, 0.98]
			config["texts_y"] = [0.85, 0.23, 0.46]
			if int(weightBin) > 0:
				config["texts"].append(weight_strings[int(weightBin)])
				config["texts_x"].append(0.78)
				config["texts_y"].append(0.78)
			config["texts_size"] = [0.035]
			config["title"] = "Combined" if channel == "combined" else "channel_"+channel
			if args.cms:
				config["cms"] = True
				config["extra_text"] = "Preliminary"
			config["year"] = args.era
			if args.pdf:
				# eps file needs to be converted manually because luminosity symbol
				# is not displayed when saving file directly as pdf
				log.warning("Only eps file created due to problem with calligraphic L. Please use epstopdf to convert the file manually.")
				config["formats"] = ["png", "eps"]
			
			if not (config["output_dir"] in www_output_dirs_parabola):
				www_output_dirs_parabola.append(config["output_dir"])
			
			parabola_plot_configs.append(config)
		file_mlfit.Close()

	# Plot parabolas
	higgsplot.HiggsPlotter(list_of_config_dicts=parabola_plot_configs, n_processes=args.n_processes, n_plots=args.n_plots[1])
	
	# Plot best fit result as function of pt/eta bins and fit with polynomials of orders 0 and 1
	config = {}
	xbins, xerrs, ybins, yerrslo, yerrshi = [], [], [], [], []
	
	# Dicts for table
	polZero_dict_p0, polZero_dict_p0err, polZero_dict_chi2, polZero_dict_ndf = {}, {}, {}, {}
	polOne_dict_p0, polOne_dict_p0err,polOne_dict_p1, polOne_dict_p1err, polOne_dict_chi2, polOne_dict_ndf = {}, {}, {}, {}, {}, {}
	
	for datacard, cb in datacards_cbs.iteritems():
		# The if statement in the loop is a workaround for the combination of channels
		# if you know of a better way, feel free to try it :)
		for category_or_bin_id in (datacards_cbs[datacard].cp().bin_set() if len(datacards_cbs[datacard].cp().bin_set()) == 1 else datacards_cbs[datacard].cp().bin_id_set()):
			category = datacards_cbs[datacard].cp().bin_set()[0]
			if len(datacards_cbs[datacard].cp().bin_set()) > 1:
				# only replace first occurence (otherwise etabin is replaced as well if channel is et)
				category = category.replace(category.split("_")[0], "combined", 1)
			
			channel = category.split("_")[0]
			decayMode = category.split("_")[-2]
			
			xval, xerrsval, yval, yerrsloval, yerrshival = "", "", "", "", ""
			xbinsF, xerrsF, ybinsF, yerrsloF, yerrshiF = [], [], [], [], []
			weight_bins_loop = weight_bins if args.no_inclusive else weight_bins[1:]
			weight_ranges_loop = weight_ranges if args.no_inclusive else weight_ranges[1:]
			for index, weightBin in enumerate(weight_bins_loop):
				if args.use_scan_without_fit:
					yval += str(output_dict_scan_mu[channel + "_" + decayMode][weightBin]) + " "
					yerrsloval += str(output_dict_scan_errLo[channel + "_" + decayMode][weightBin]) + " "
					yerrshival += str(output_dict_scan_errHi[channel + "_" + decayMode][weightBin]) + " "
					ybinsF.append(output_dict_scan_mu[channel + "_" + decayMode][weightBin])
					yerrsloF.append(output_dict_scan_errLo[channel + "_" + decayMode][weightBin])
					yerrshiF.append(output_dict_scan_errHi[channel + "_" + decayMode][weightBin])
				else:
					yval += str(output_dict_scan_fit_mu[channel + "_" + decayMode][weightBin]) + " "
					yerrsloval += str(output_dict_scan_fit_err[channel + "_" + decayMode][weightBin]) + " "
					yerrshival += str(output_dict_scan_fit_err[channel + "_" + decayMode][weightBin]) + " "
					ybinsF.append(output_dict_scan_fit_mu[channel + "_" + decayMode][weightBin])
					yerrsloF.append(output_dict_scan_fit_err[channel + "_" + decayMode][weightBin])
					yerrshiF.append(output_dict_scan_fit_err[channel + "_" + decayMode][weightBin])
				if index < (len(weight_bins_loop) - 1):
					xval += str((float(weight_ranges_loop[index]) + float(weight_ranges_loop[index + 1])) / 2.0) + " "
					xerrsval += str((float(weight_ranges_loop[index + 1])-float(weight_ranges_loop[index])) / 2.0) + " "
					xbinsF.append((float(weight_ranges_loop[index]) + float(weight_ranges_loop[index + 1])) / 2.0)
					xerrsF.append((float(weight_ranges_loop[index + 1])-float(weight_ranges_loop[index])) / 2.0)
			
			if len(weight_bins_loop) > 0:
				xval += str((float(weight_ranges_loop[index]) + 200.0) / 2.0)
				xerrsval += str((200.0 - float(weight_ranges_loop[index])) / 2.0)
				xbinsF.append((float(weight_ranges_loop[index]) + 200.0) / 2.0)
				xerrsF.append((200.0 - float(weight_ranges_loop[index])) / 2.0)
			else: # no pt ranges were given - plot only inclusive result
				xval += "110.0 "
				xerrsval += "90.0 "
				xbinsF.append(110.0)
				xerrsF.append(90.0)
				if args.use_scan_without_fit:
					yval += str(output_dict_scan_mu[channel + "_" + decayMode]["0"]) + " "
					yerrsloval += str(output_dict_scan_errLo[channel + "_" + decayMode]["0"]) + " "
					yerrshival += str(output_dict_scan_errHi[channel + "_" + decayMode]["0"]) + " "
					ybinsF.append(output_dict_scan_mu[channel + "_" + decayMode]["0"])
					yerrsloF.append(output_dict_scan_errLo[channel + "_" + decayMode]["0"])
					yerrshiF.append(output_dict_scan_errHi[channel + "_" + decayMode]["0"])
				else:
					yval += str(output_dict_scan_fit_mu[channel + "_" + decayMode]["0"]) + " "
					yerrsloval += str(output_dict_scan_fit_err[channel + "_" + decayMode]["0"]) + " "
					yerrshival += str(output_dict_scan_fit_err[channel + "_" + decayMode]["0"]) + " "
					ybinsF.append(output_dict_scan_fit_mu[channel + "_" + decayMode]["0"])
					yerrsloF.append(output_dict_scan_fit_err[channel + "_" + decayMode]["0"])
					yerrshiF.append(output_dict_scan_fit_err[channel + "_" + decayMode]["0"])
					
			
			if args.eta_binning:
				xval = "0.7395 2.2185"
				xerrsval = "0.7395 0.7395"
				xbinsF = [0.7395, 2.2185]
				xerrsF = [0.7395, 0.7395]
			
			# Fill TGraphErrors for fit
			RooFitGraph_Linear = ROOT.TGraphAsymmErrors(
				len(xbinsF),
				array.array("d", xbinsF),
				array.array("d", ybinsF),
				array.array("d", xerrsF),
				array.array("d", xerrsF),
				array.array("d", yerrsloF),
				array.array("d", yerrshiF)
			)
			
			# Pol0 and Pol1 fit functions
			fit_polZero = ROOT.TF1("f2","pol0",min(xbinsF),max(xbinsF))
			fit_polOne = ROOT.TF1("f3","pol1",min(xbinsF),max(xbinsF))
			
			# Fit Pol0
			RooFitGraph_Linear.Fit("f2","R")
			polZero_dict_p0[channel + "_" + decayMode] = fit_polZero.GetParameter(0)
			polZero_dict_p0err[channel + "_" + decayMode] = fit_polZero.GetParError(0)
			polZero_dict_chi2[channel + "_" + decayMode] = fit_polZero.GetChisquare()
			polZero_dict_ndf[channel + "_" + decayMode] = fit_polZero.GetNDF()
			
			polZero_filename = os.path.join(args.output_dir, "datacards/result_fit_" + ("eta" if args.eta_binning else "pt") + "_pol0_" + decayMode + "_" + quantity + ".root")
			polZero_file = ROOT.TFile(polZero_filename, "RECREATE")
			RooFitGraph_Linear.Write()
			polZero_file.Close()
			
			# Fit Pol1
			RooFitGraph_Linear.Fit("f3","R")
			polOne_dict_p0[channel + "_" + decayMode] = fit_polOne.GetParameter(0)
			polOne_dict_p0err[channel + "_" + decayMode] = fit_polOne.GetParError(0)
			polOne_dict_p1[channel + "_" + decayMode] = fit_polOne.GetParameter(1)
			polOne_dict_p1err[channel + "_" + decayMode] = fit_polOne.GetParError(1)
			polOne_dict_chi2[channel + "_" + decayMode] = fit_polOne.GetChisquare()
			polOne_dict_ndf[channel + "_" + decayMode] = fit_polOne.GetNDF()
			
			polOne_filename = os.path.join(args.output_dir, "datacards/result_fit_" + ("eta" if args.eta_binning else "pt") + "_pol1_" + decayMode + "_" + quantity + ".root")
			polOne_file = ROOT.TFile(polOne_filename, "RECREATE")
			RooFitGraph_Linear.Write()
			polOne_file.Close()
			
			xbins.append(xval)
			xerrs.append(xerrsval)
			ybins.append(yval)
			yerrslo.append(yerrsloval)
			yerrshi.append(yerrshival)
			config.setdefault("colors", []).append(decayMode_dict[decayMode]["color"])
			config.setdefault("labels", []).append(decayMode_dict[decayMode]["label"].split(" decay")[0])
	
		config["input_modules"] = ["InputInteractive"]
		config["x_lims"] = ([0.0, 2.3] if args.eta_binning else [0.0, 200.0])
		config["y_lims"] = [(min(es_shifts) - 1.0) * 100, (max(es_shifts) - 1.0) * 100]
		config["x_label"] = ("#eta_{#tau_{h}}" if args.eta_binning else "p^{#tau_{h}}_{T} (GeV)")
		config["y_label"] = "#tau_{h} ES (%)"
		config["markers"] = ["P"]
		config["legend"] = [0.2,0.78,0.6,0.9]
		config["output_dir"] = os.path.expandvars(args.output_dir) + "/datacards/"
		config["filename"] = ("result_vs_eta_" if args.eta_binning else "result_vs_pt_") + quantity + ("_tightenedMassWindow" if args.tighten_mass_window else "")
		config["x_expressions"] = xbins
		config["x_errors"] = xerrs
		config["x_errors_up"] = xerrs
		config["y_expressions"] = ybins
		config["y_errors"] = yerrslo
		config["y_errors_up"] = yerrshi
		if args.pdf:
			config["formats"] = ["png", "pdf"]
	
		if not (config["output_dir"] in www_output_dirs_weightbin):
			www_output_dirs_weightbin.append(config["output_dir"])
	
		weightbin_plot_configs.append(config)
	
	higgsplot.HiggsPlotter(list_of_config_dicts=weightbin_plot_configs, n_processes=args.n_processes, n_plots=args.n_plots[1])

	# Print output tables to shell
	for channel in args.channels+(["combined"] if len(args.channels) > 1 else []):
		print ">>>>>>>>>>>>>>>>>>> Output summary for channel: "+channel+" <<<<<<<<<<<<<<<<<<<"
		
		print "################### Fit results table: ML fit | MultiDim parabola fit | MultiDim parabola ###################"
		row_format = "{:^22}" * (len(decay_modes) + 1)
		print row_format.format("", *decay_modes)
		print
		for weightBin in weight_bins:
			if weightBin == "0":
				print "{:^22}".format("Inclusive"),
			else:
				print ("{:^22}".format("Eta bin "+weightBin) if args.eta_binning else "{:^22}".format("Pt bin "+weightBin)),
			for decayMode in decay_modes:
				if decayMode != decay_modes[-1]:
					print "{:<3.2f}% | {:<3.2f}% | {:<3.2f}%\t".format(output_dict_mu[channel+"_"+decayMode][weightBin],output_dict_scan_fit_mu[channel+"_"+decayMode][weightBin],output_dict_scan_mu[channel+"_"+decayMode][weightBin]),
				else:
					print "{:<3.2f}% | {:<3.2f}% | {:<3.2f}%\t".format(output_dict_mu[channel+"_"+decayMode][weightBin],output_dict_scan_fit_mu[channel+"_"+decayMode][weightBin],output_dict_scan_mu[channel+"_"+decayMode][weightBin])
			print "{:^22}".format("+ 1sigma "),
			for decayMode in decay_modes:
				if decayMode != decay_modes[-1]:
					print "{:<3.2f}% | {:<3.2f}% | {:<3.2f}%\t".format(output_dict_errHi[channel+"_"+decayMode][weightBin],output_dict_scan_fit_err[channel+"_"+decayMode][weightBin],output_dict_scan_errHi[channel+"_"+decayMode][weightBin]),
				else:
					print "{:<3.2f}% | {:<3.2f}% | {:<3.2f}%\t".format(output_dict_errHi[channel+"_"+decayMode][weightBin],output_dict_scan_fit_err[channel+"_"+decayMode][weightBin],output_dict_scan_errHi[channel+"_"+decayMode][weightBin])
			print "{:^22}".format("- 1sigma "),
			for decayMode in decay_modes:
				if decayMode != decay_modes[-1]:
					print "{:<3.2f}% | {:<3.2f}% | {:<3.2f}%\t".format(output_dict_errLo[channel+"_"+decayMode][weightBin],output_dict_scan_fit_err[channel+"_"+decayMode][weightBin],output_dict_scan_errLo[channel+"_"+decayMode][weightBin]),
				else:
					print "{:<3.2f}% | {:<3.2f}% | {:<3.2f}%\t".format(output_dict_errLo[channel+"_"+decayMode][weightBin],output_dict_scan_fit_err[channel+"_"+decayMode][weightBin],output_dict_scan_errLo[channel+"_"+decayMode][weightBin])
			print
		print "################### Fit results table: polynomial fits to tau energy scale vs. "+("eta" if args.eta_binning else "pt")+" ###################"
		row_format = "{:^22}" * (len(decay_modes) + 1)
		print row_format.format("", *decay_modes)
		print
		print "{:^22}".format("p0"),
		for decayMode in decay_modes:
			polZero_string1 = "%1.2f"%polZero_dict_p0[channel+"_"+decayMode]
			polZero_string2 = "%1.2f"%polZero_dict_p0err[channel+"_"+decayMode]
			if decayMode != decay_modes[-1]:
				print "{:^22}".format(polZero_string1 + " +/- " + polZero_string2),
			else:
				print "{:^22}".format(polZero_string1 + " +/- " + polZero_string2)
		print "{:^22}".format("chi2/ndf"),
		for decayMode in decay_modes:
			polZero_string1 = "%1.2f"%polZero_dict_chi2[channel+"_"+decayMode]
			polZero_string2 = "%1.2f"%polZero_dict_ndf[channel+"_"+decayMode]
			if decayMode != decay_modes[-1]:
				print "{:^22}".format(polZero_string1 + " / " + polZero_string2),
			else:
				print "{:^22}".format(polZero_string1 + " / " + polZero_string2)
		print
		print "{:^22}".format("p0"),
		for decayMode in decay_modes:
			polOne_string1 = "%1.2f"%polOne_dict_p0[channel+"_"+decayMode]
			polOne_string2 = "%1.2f"%polOne_dict_p0err[channel+"_"+decayMode]
			if decayMode != decay_modes[-1]:
				print "{:^22}".format(polOne_string1 + " +/- " + polOne_string2),
			else:
				print "{:^22}".format(polOne_string1 + " +/- " + polOne_string2)
		print "{:^22}".format("p1"),
		for decayMode in decay_modes:
			polOne_string1 = "%1.2f"%polOne_dict_p1[channel+"_"+decayMode]
			polOne_string2 = "%1.2f"%polOne_dict_p1err[channel+"_"+decayMode]
			if decayMode != decay_modes[-1]:
				print "{:^22}".format(polOne_string1 + " +/- " + polOne_string2),
			else:
				print "{:^22}".format(polOne_string1 + " +/- " + polOne_string2)
		print "{:^22}".format("chi2/ndf"),
		for decayMode in decay_modes:
			polOne_string1 = "%1.2f"%polOne_dict_chi2[channel+"_"+decayMode]
			polOne_string2 = "%1.2f"%polOne_dict_ndf[channel+"_"+decayMode]
			if decayMode != decay_modes[-1]:
				print "{:^22}".format(polOne_string1 + " / " + polOne_string2),
			else:
				print "{:^22}".format(polOne_string1 + " / " + polOne_string2)
		print

	# Publish to web : it's not pretty but it works :)
	if not args.www is None:
		from Artus.HarryPlotter.plotdata import PlotData
		for output_dir in www_output_dirs_postfit:
			subpath = os.path.normpath(output_dir).split("/")[-1]
			output_filenames = []
			for config in postfit_plot_configs:
				if(output_dir in config["output_dir"] and not config["filename"] in output_filenames):
					output_filenames.append(os.path.join(output_dir, config["filename"]+".png"))
			PlotData.webplotting(
						www = args.www if(subpath == "tauEsStudies_datacards") else os.path.join(args.www, subpath),
						output_dir = output_dir,
						export_json = False,
						output_filenames = output_filenames
						)
		for output_dir in www_output_dirs_weightbin:
			subpath = os.path.normpath(output_dir).split("/")[-1]
			output_filenames = []
			for config in weightbin_plot_configs:
				if(output_dir in config["output_dir"] and not config["filename"] in output_filenames):
					output_filenames.append(os.path.join(output_dir, config["filename"]+".png"))
			PlotData.webplotting(
						www = args.www if(subpath == "tauEsStudies_datacards") else os.path.join(args.www, subpath),
						output_dir = output_dir,
						export_json = False,
						output_filenames = output_filenames
						)
		for output_dir in www_output_dirs_parabola:
			subpath = os.path.normpath(output_dir).split("/")[-1]
			output_filenames = []
			for config in parabola_plot_configs:
				if(output_dir in config["output_dir"] and not config["filename"] in output_filenames):
					output_filenames.append(os.path.join(output_dir, config["filename"]+".png"))
			PlotData.webplotting(
						www = args.www if(subpath == "tauEsStudies_datacards") else os.path.join(args.www, subpath),
						output_dir = output_dir,
						export_json = False,
						output_filenames = output_filenames
						)
