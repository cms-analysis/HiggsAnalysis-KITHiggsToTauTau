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
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.binnings as binnings
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.systematics_run2 as systematics
import HiggsAnalysis.KITHiggsToTauTau.datacards.qcdfactorsdatacards as qcdfactorsdatacards


def addArguments(parser):
	parser.add_argument("-i", "--input-dir", required=True,
	                    help="Input directory.")
	parser.add_argument("-x", "--quantity", default="m_vis", choices=["m_vis"], 
	                    help="Quantity ot perform fit in sideband region. [Default: %(default)s]")
	parser.add_argument("-c", "--channels", action = "append", 
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
	                    default="$CMSSW_BASE/src/plots/QcdFactorsStudies_datacards/",
	                    help="Output directory. [Default: %(default)s]")
	parser.add_argument("--clear-output-dir", action="store_true", default=False,
	                    help="Delete/clear output directory before running this script. [Default: %(default)s]")
	parser.add_argument("--combine-verbosity", default="0", choices=["-1","0","1","2"],
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
	parser.add_argument("-e", "--exclude-cuts", nargs="+", default=[],
	                    help="Exclude (default) selection cuts. [Default: %(default)s]")
	parser.add_argument("-m", "--higgs-masses", nargs="+", default=["125"],
	                    help="Higgs masses. [Default: %(default)s]")
	parser.add_argument("--do-not-ignore-category-removal", default=False, action="store_true",
						help="Exit program in case categories are removed from CH. [Default: %(default)s]")
	parser.add_argument("--steps", nargs="+",
	                    default=["inputs", "t2w", "dofit", "prefitpostfitplots"],
	                    choices=["inputs", "t2w", "dofit", "prefitpostfitplots", "nuisanceimpacts"],
	                    help="Steps to perform.[Default: %(default)s]\n 'inputs': Writes datacards and fills them using HP.\n 't2w': Create ws.root files form the datacards. 't2w': Perform likelihood scans for various physical models and plot them.")
												
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
	binnings_settings = binnings.BinningsDict()
	systematics_factory = systematics.SystematicsFactory()
	www_output_dirs_postfit = []
	www_output_dirs_weightbin = []
	www_output_dirs_parabola = []
			
	plot_configs = []
	output_files = []
	merged_output_files = []
	hadd_commands = []	
	
	# Initialise directory and naming scheme templates for datacards
	tmp_input_root_filename_template = "input/${ANALYSIS}_${CHANNEL}_${BIN}_${SYSTEMATIC}_${ERA}.root"
	input_root_filename_template = "input/${ANALYSIS}_${CHANNEL}_${ERA}.root"
	bkg_histogram_name_template = "${BIN}/${PROCESS}"
	sig_histogram_name_template = "${BIN}/${PROCESS}"
	bkg_syst_histogram_name_template = "${BIN}/${PROCESS}_${SYSTEMATIC}"
	sig_syst_histogram_name_template = "${BIN}/${PROCESS}_${SYSTEMATIC}"
	datacard_filename_templates = ["datacards/${BIN}/${ANALYSIS}_${CHANNEL}_${BIN}_${ERA}.txt"]
	if len(args.channels) > 1: datacard_filename_templates.append("datacards/decaymode/${BIN}/${ANALYSIS}_${BIN}_${ERA}.txt")
	output_root_filename_template = "datacards/common/${ANALYSIS}.input_${ERA}.root"
	
	# define the quantity for the sideband region
	quantity = args.quantity
	
	# Build categories and bin id's for CombineHarvester
	categories = [channel+"_"+category for channel in args.channels for category in args.categories[0]]
	mapping_category2binid = {}
	

	
	# Restrict CombineHarvester to configured channels:
	datacards = qcdfactorsdatacards.QcdFactorsDatacards(quantity, args.era, mapping_category2binid)

	# dict to map Process names to python sample function. 
	datacards.configs._mapping_process2sample = {
		"data_obs" : "data",
		"QCD" : "qcd_prefit",				
		"TTT" : "ttt",
		"TTJJ" : "ttjj",
		"VV" : "vv",
		"VVT" : "vvt",
		"VVJ" : "vvj",
		"W" : "wj",				
		"ZJ" : "zj",
		"ZL" : "zl",
		"ZLL" : "zll",	
		"ZTT" : "ztt",															
		}

	#restriction to requested channels
	if args.channels != parser.get_default("channels"):
		datacards.cb.channel(args.channels)
	args.channels = datacards.cb.cp().channel_set()
	
	args.categories = len(args.channels) * args.categories
	
	
	datacards.cb.mass(["*", "125"])
	if args.categories == parser.get_default("categories"):
		args.categories = len(args.channel) * args.categories
	# create HP configs for each channel_category


	for index, (channel, categories) in enumerate(zip(args.channels, args.categories)):
		# if index != 0: break
		# channel = category.split("_")[0]
		
		tmp_output_files = []
		output_file = os.path.join(args.output_dir, input_root_filename_template.replace("$", "").format(
			ANALYSIS="htt",
			CHANNEL=channel,
			ERA="13TeV"
		))		
		# categories = datacards.cb.cp().channel([channel]).bin_set()
		categories = [channel + "_" + category for category in categories]		
		categories_save = sorted(categories)
		categories = list(set(categories).intersection(set(datacards.cb.cp().channel([channel]).bin_set())))
		if(categories_save != sorted(categories))  and args.do_not_ignore_category_removal:
			log.fatal("CombineHarverster removed the following categories automatically. Was this intended?")
			log.fatal(list(set(categories_save) - set(categories)))
			sys.exit(1)
				
				# restrict CombineHarvester to configured categories:
			
		datacards.cb.FilterAll(lambda obj : (obj.channel() == channel) and (obj.bin() not in categories))
				
		for category in categories:
			exclude_cuts = copy.deepcopy(args.exclude_cuts)
			weight = args.weight
			datacards_per_channel_category = qcdfactorsdatacards.QcdFactorsDatacards(cb=datacards.cb.cp().channel([channel]).bin([category]), mapping_category2binid=mapping_category2binid)
			higgs_masses = [mass for mass in datacards_per_channel_category.cb.mass_set() if mass != "*"]
			# exclude isolation cut which is set by default in cutstrings.py using the smhtt2016 cut_type
			if any(bin in category for bin in ["ZeroJet2D_antiiso","Boosted2D_antiiso","dijet2D_lowboost_antiiso","dijet2D_boosted_antiiso", "ZeroJet2D_antiiso_tau","Boosted2D_antiiso_tau","dijet2D_lowboost_antiiso_tau","dijet2D_boosted_antiiso_tau", "ZeroJet2D_antiiso_taulep","Boosted2D_antiiso_taulep","dijet2D_lowboost_antiiso_taulep","dijet2D_boosted_antiiso_taulep", "dijet2D_antiiso", "ZeroJet2D_antiiso_near","Boosted2D_antiiso_near","dijet2D_lowboost_antiiso_near","dijet2D_boosted_antiiso_near", "dijet2D_antiiso_near", "ZeroJet2D_antiiso_far","Boosted2D_antiiso_far","dijet2D_lowboost_antiiso_far","dijet2D_boosted_antiiso_far", "dijet2D_antiiso_far"])  and channel in ["mt", "et"]:
				# exclude_cuts.append("iso_2")
				# if ("taulep" in category):
				# 	exclude_cuts.append("iso_1")
					# weight+= "*(byLooseIsolationMVArun2v1DBoldDMwLT_2 > 0.5)*((gen_match_2 == 5)*0.95 + (gen_match_2 != 5))"
				exclude_cuts.append("iso_1")
				if ("dijet2D" in category):
					exclude_cuts.append("iso_2")
					weight+= "*(byVLooseIsolationMVArun2v1DBoldDMwLT_2 > 0.5)*((gen_match_2 == 5)*0.95 + (gen_match_2 != 5))"

				do_not_normalize_by_bin_width = True

		
			for shape_systematic, list_of_samples in datacards_per_channel_category.get_samples_per_shape_systematic().iteritems():
				nominal = (shape_systematic == "nominal")
				list_of_samples = [datacards.configs.process2sample(process) for process in list_of_samples]
			
				for shift_up in ([True] if nominal else [True, False]):
					systematic = "nominal" if nominal else (shape_systematic + ("Up" if shift_up else "Down"))
		
					log.debug("Create inputs for (samples, systematic) = ([\"{samples}\"], {systematic}), (channel, category) = ({channel}, {category}).".format(
						samples="\", \"".join(list_of_samples),
						channel=channel,
						category=category,
						systematic=systematic
					))
				
					# very basic config
					config = sample_settings.get_config(
						samples=[getattr(samples.Samples, sample if sample != "data_obs" else "data") for sample in list_of_samples],
						channel=channel,
						category="catHtt13TeV_{CATEGORY}".format(CATEGORY=category),
						weight=weight,
						lumi=args.lumi * 1000,
						higgs_masses=higgs_masses,
						cut_type="smhtt2016", 
						background_method="mc",
						exclude_cuts = exclude_cuts
					)

					systematics_settings = systematics_factory.get(shape_systematic)(config)
					config= systematics_settings.get_config(shift=(0.0 if nominal else (1.0 if shift_up else -1.0)))
				
					# fit is to be performed for 
					config["x_expressions"] = ["m_vis" if "ZeroJet2D" in category else "m_sv"]
								
					# configure binnings etc 				
					if any(bin in category for bin in ["ZeroJet2D_antiiso","Boosted2D_antiiso","dijet2D_lowboost_antiiso","dijet2D_boosted_antiiso", "ZeroJet2D_antiiso_tau","Boosted2D_antiiso_tau","dijet2D_lowboost_antiiso_tau","dijet2D_boosted_antiiso_tau", "ZeroJet2D_antiiso_taulep","Boosted2D_antiiso_taulep","dijet2D_lowboost_antiiso_taulep","dijet2D_boosted_antiiso_taulep", "dijet2D_antiiso", "ZeroJet2D_antiiso_near","Boosted2D_antiiso_near","dijet2D_lowboost_antiiso_near","dijet2D_boosted_antiiso_near", "dijet2D_antiiso_near", "ZeroJet2D_antiiso_far","Boosted2D_antiiso_far","dijet2D_lowboost_antiiso_far","dijet2D_boosted_antiiso_far", "dijet2D_antiiso_far",]) and channel in ["mt", "et"]:
						config["x_bins"] = [binnings_settings.binnings_dict["binningHttCP13TeV_"+category+"_m_vis"]]
				
					# Miscellaneous
					config["directories"] = [args.input_dir]
		
					histogram_name_template = bkg_histogram_name_template if nominal else bkg_syst_histogram_name_template
					config["labels"] = [histogram_name_template.replace("$", "").format(
						PROCESS=datacards.configs.sample2process(sample), # if sample != "data" else "data_obs",
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
					
					plot_configs.append(config)

		hadd_commands.append("hadd -f {DST} {SRC}".format(
			DST=output_file,
			SRC=" ".join(tmp_output_files)
		))

	# 	# Delete existing output files
	# output_files = list(set([os.path.join(config["output_dir"], config["filename"]+".root") for config in plot_configs[:args.n_plots[0]]]))
	# for output_file in output_files:
	# 		if os.path.exists(output_file):
	# 			os.remove(output_file)
	# 			log.debug("Removed file \""+output_file+"\" before it is recreated again.")
	
		# Create input histograms with HarryPlotter
	if "inputs" in args.steps:	
		higgsplot.HiggsPlotter(list_of_config_dicts=plot_configs, n_processes=args.n_processes, n_plots=args.n_plots[0])
		if args.n_plots[0] != 0:
			tools.parallelize(_call_command, hadd_commands, n_processes=args.n_processes)

	# Update CombineHarvester with the yields and shapes
	datacards.extract_shapes(
		os.path.join(args.output_dir, input_root_filename_template.replace("$", "")),
		bkg_histogram_name_template, sig_histogram_name_template,
		bkg_syst_histogram_name_template, sig_syst_histogram_name_template,
		update_systematics=True
	)
	
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
	datacards.cb.PrintAll()
	if "t2w" or "prefitpostfitplots" in args.steps:
		datacards_workspaces = datacards.text2workspace(datacards_cbs, n_processes=args.n_processes, higgs_mass=125)
	
	# Combine call
	if "dofit" in args.steps:
		datacards.combine(
				datacards_cbs,
				datacards_workspaces,
				None,
				args.n_processes,
				"-M FitDiagnostics -v {VERBOSITY} {STABLE}".format(
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
				"-M MultiDimFit --algo grid --points 500 --setParameterRanges r=0,5 -v {VERBOSITY}  {STABLE}".format(
					VERBOSITY=args.combine_verbosity,
					STABLE=datacards.stable_options
				)
			)
		datacards.plot1DScan(datacards_cbs, datacards_workspaces, "r")
			
	# Plot nuisance impacts
	if "nuisanceimpacts" in args.steps:
		datacards.nuisance_impacts(datacards_cbs, datacards_workspaces, args.n_processes)
	
	# Postfitshapes call
	if "prefitpostfitplots" in args.steps:
		datacards_postfit_shapes = datacards.postfit_shapes_fromworkspace(datacards_cbs, datacards_workspaces, True, args.n_processes, "--sampling" + (" --print" if args.n_processes <= 1 else ""))
	# Plot postfit
		postfit_plot_configs = [] #reset list containing the plot configs
		bkg_plotting_order = ["ZTT", "ZL", "ZJ", "TTT", "TTJJ", "VVT", "VVJ", "W"]

		for level in ["prefit", "postfit"]:
			for datacard in datacards_cbs.keys():
				postfit_shapes = datacards_postfit_shapes.get("fit_s", {}).get(datacard)
				# do not produce plots for combination as there is no proper implementation for that
				if len(datacards_cbs[datacard].cp().bin_set()) > 1:
					continue
				for category in datacards_cbs[datacard].cp().bin_set():
					channel = category.split("_")[0]
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
					processes = [p.replace("ZL", "ZL_noplot").replace("ZJ", "ZJ_noplot").replace("VVT", "VVT_noplot").replace("VVJ", "VVJ_noplot").replace("W", "W_noplot")  for p in processes]
					processes_to_plot = [p for p in processes if not "noplot" in p]
				
					processes_to_plot.insert(1, "EWK")
					config["sum_nicks"].append("VVT_noplot VVJ_noplot W_noplot" if not "et_dijet2D_boosted" in category else "VVT_noplot W_noplot")
					config["sum_scale_factors"].append("1.0 1.0 1.0"  if not "et_dijet2D_boosted" in category else "1.0 1.0")
					config["sum_result_nicks"].append("EWK")
					
					if any(bin in category for bin in ["et_dijet2D_antiiso_far", "et_dijet2D_lowboost_antiiso_near","et_dijet2D_lowboost_antiiso"]):
						processes_to_plot.insert(2, "ZLL")
						config["sum_nicks"].append("ZJ_noplot")
						config["sum_scale_factors"].append("1.0")
						config["sum_result_nicks"].append("ZLL")
					elif any(bin in category for bin in ["et_ZeroJet2D_antiiso_far"]):
						processes_to_plot.insert(2, "ZLL")
						config["sum_nicks"].append("ZL_noplot")
						config["sum_scale_factors"].append("1.0")
						config["sum_result_nicks"].append("ZLL")
					elif any(bin in category for bin in ["et_dijet2D_lowboost_antiiso_far", "mt_dijet2D_lowboost_antiiso_far"]): 
						pass
					else:
						processes_to_plot.insert(2, "ZLL")
						config["sum_nicks"].append("ZL_noplot ZJ_noplot")
						config["sum_scale_factors"].append("1.0 1.0")
						config["sum_result_nicks"].append("ZLL")						
										
					config["files"] = [postfit_shapes]
					config["folders"] = [category+"_"+level]
					config["nicks"] = [processes + ["noplot_TotalBkg", "noplot_TotalSig", "data_obs"]]
					config["x_expressions"] = [p.split("_")[0] for p in processes] + ["TotalBkg", "TotalSig", "data_obs"]
					config["stacks"] = ["bkg"]*len(processes_to_plot) + ["data"] + [""]
					config["labels"] = [label.lower() for label in processes_to_plot + ["totalbkg"] + ["data_obs"]]
					config["colors"] = [color.lower() for color in processes_to_plot + ["#000000 transgrey"] + ["data_obs"]]
					config["markers"] = ["HIST"]*len(processes_to_plot) + ["E2"] + ["E"]
					config["legend_markers"] = ["F"]*len(processes_to_plot) + ["F"] + ["ELP"]
				
					config["y_label"] = "Events / bin"
					config["x_label"] = "m_{vis}" if "ZeroJet2D_QCDCR" in category else "m_{#tau#tau}"
				
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
					config["filename"] = level+"_"+category
					if args.pdf:
						config["formats"] = ["png", "pdf"]
						config["texts_x"] = [0.52]
						config["texts_y"] = [0.81]

					config["texts_size"] = [0.055]
					config["title"] = "channel_"+channel
					if not args.www is None:
						config["www"] = os.path.join(
								args.www,
								channel if len(args.channels) > 1 else "",
								"" if category is None else category
						)

				
					if not (config["output_dir"] in www_output_dirs_postfit):
						www_output_dirs_postfit.append(config["output_dir"])
					postfit_plot_configs.append(config)					
		higgsplot.HiggsPlotter(list_of_config_dicts=postfit_plot_configs, n_processes=args.n_processes, n_plots=args.n_plots[1])
