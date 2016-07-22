#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import argparse
import copy
import os
import sys

import CombineHarvester.CombineTools.ch as ch
import CombineHarvester.CombinePdfs.morphing as morphing
import ROOT

import Artus.Utility.tools as tools
import Artus.Utility.jsonTools as jsonTools

import HiggsAnalysis.KITHiggsToTauTau.plotting.higgsplot as higgsplot
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.samples_run2 as samples
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.systematics_run2 as systematics
import HiggsAnalysis.KITHiggsToTauTau.datacards.taupogdatacards as taupogdatacards


decayMode_dict = {
	"AllDMs" : {
		"color" : "1",
		"label" : "All decay modes"
	},
	"OneProng" : {
		"color" : "2",
		"label" : "h^{#pm} decay mode"
	},
	"OneProngPiZeros" : {
		"color" : "4",
		"label" : "h^{#pm}(#geq 1 #pi^{0}) decay mode"
	},
	"ThreeProng" : {
		"color" : "6",
		"label" : "h^{#pm}h^{#mp}h^{#pm} decay mode"
	}
}

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

	parser = argparse.ArgumentParser(description="Create ROOT inputs and datacards for tau energy scale measurement.",
	                                 parents=[logger.loggingParser])

	parser.add_argument("-i", "--input-dir", required=True,
	                    help="Input directory.")
	parser.add_argument("--quantity", default="m_2", choices=["m_2","m_vis"],
	                    help="Quantity. [Default: %(default)s]")
	parser.add_argument("--shift-ranges", nargs="*", type=float,
                        default=[0.94,1.06],
                        help="Provide minimum and maximum energy scale shift. [Default: %(default)s]")
	parser.add_argument("--shift-binning", type=float, default=0.001,
						help="Provide binning to use for energy scale shifts. [Default: %(default)s]")
	parser.add_argument("--pt-ranges", nargs="*",
	                    default=[],
	                    help="Enter the lower bin edges for the pt ranges."	)
	parser.add_argument("--decay-modes", nargs="+",
	                    default=["OneProngPiZeros"],
	                    choices=["AllDMs","OneProng","OneProngPiZeros","ThreeProng"],
	                    help="Decay modes of reconstructed hadronic tau leptons in Z #rightarrow #tau#tau. [Default: %(default)s]")
	parser.add_argument("--add-bbb-uncs", action="store_true", default=True,
	                    help="Add bin-by-bin uncertainties. [Default: %(default)s]")
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
	parser.add_argument("--era", default="2015",
	                    help="Era of samples to be used. [Default: %(default)s]")
	parser.add_argument("--tighten-mass-window", action="store_true", default=False,
						help="Enable to study effect mass window cut has on tau ES when using m_2. [Default: %(default)s]")
	parser.add_argument("--plot-with-shift", type=float, default=0.0,
						help="For plot presentation purposes only: produce prefit plot for a certain energy scale shift. [Default: %(default)s]")
	parser.add_argument("--colors-dm-dependent", action="store_true", default=False,
						help="Use different colors for each decay mode corresponding to m_tau in TAU-14-001. [Default: %(default)s]")
	
	args = parser.parse_args()
	logger.initLogger(args)
	
	args.output_dir = os.path.abspath(os.path.expandvars(args.output_dir))
	if args.clear_output_dir and os.path.exists(args.output_dir):
		logger.subprocessCall("rm -r " + args.output_dir, shell=True)
		
	# produce es shifts from input arguments
	es_shifts = [args.shift_ranges[0]]
	es_shifts_str = [str(args.shift_ranges[0])] #taupogdatacards needs a list of strings. this can maybe be done better
	while es_shifts[-1] < args.shift_ranges[-1]:
		# sometimes, we get numbers like 0.990000000001 without round
		current_shift = round(es_shifts[-1]+args.shift_binning,4)
		es_shifts.append(current_shift)
		es_shifts_str.append(str(current_shift))
	if args.plot_with_shift != 0.0:
		es_shifts = [args.plot_with_shift-0.0001,args.plot_with_shift+0.0001]
		es_shifts_str = [str(es_shifts[0]),str(es_shifts[1])]
		
	# produce decaymode bins
	decay_modes = []
	for decayMode in args.decay_modes:
		decay_modes.append(decayMode)
	
	# produce pt-bins (first one is always inclusive)
	pt_ranges = ["0.0"]
	for pt_index, (pt_range) in enumerate(args.pt_ranges):
		pt_ranges.append(args.pt_ranges[pt_index])
	pt_weights = []
	pt_strings = []
	pt_bins = []
	for pt_index, (pt_range) in enumerate(pt_ranges):
		if pt_range == "0.0":
			pt_weights.append("(pt_2>20)")
			pt_strings.append("p_{T}^{#tau_{h}} > 20 GeV")
		else:
			if len(pt_ranges) > pt_index+1:
				pt_weights.append("(pt_2>"+str(pt_ranges[pt_index])+")*(pt_2<"+str(pt_ranges[pt_index+1])+")")
				pt_strings.append(pt_ranges[pt_index]+" < p_{T}^{#tau_{h}} < "+pt_ranges[pt_index+1]+ " GeV")
			else:
				pt_weights.append("(pt_2>"+str(pt_ranges[pt_index])+")")
				pt_strings.append("p_{T}^{#tau_{h}} > "+pt_ranges[pt_index]+" GeV")
		pt_bins.append(str(pt_index))
	
	# initialisations for plotting
	if args.era == "2015":
		import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.samples_run2 as samples
	else:
		import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.samples_run2_2016 as samples
		if args.lumi == parser.get_default("lumi"):
			args.lumi = samples.default_lumi/1000.0
	sample_settings = samples.Samples()
	systematics_factory = systematics.SystematicsFactory()
	www_output_dirs_postfit = []
	www_output_dirs_ptbin = []
	www_output_dirs_parabola = []
	
	# initialise datacards
	tmp_input_root_filename_template = "input/${ANALYSIS}_${CHANNEL}_${BIN}_${SYSTEMATIC}_${ERA}.root"
	input_root_filename_template = "input/${ANALYSIS}_${CHANNEL}_${BIN}_${ERA}.root"
	bkg_histogram_name_template = "${BIN}/${PROCESS}"
	sig_histogram_name_template = "${BIN}/${PROCESS}${MASS}"
	bkg_syst_histogram_name_template = "${BIN}/${PROCESS}_${SYSTEMATIC}"
	sig_syst_histogram_name_template = "${BIN}/${PROCESS}${MASS}_${SYSTEMATIC}"
	datacard_template = "datacards/${BIN}/${ANALYSIS}_${CHANNEL}_${BIN}_${ERA}.txt"
	datacard_combined_template = "datacards/combined/${ANALYSIS}_${CHANNEL}_${ERA}.txt"
	output_root_template = "datacards/${BIN}/${ANALYSIS}_${CHANNEL}_${BIN}.input_${ERA}.root"
	output_root_combined_template = "datacards/combined/${ANALYSIS}_${CHANNEL}.input_${ERA}.root"
	
	# restrict CombineHarvester to configured channels:
	channel = "mt"
	quantity = args.quantity
	datacards = taupogdatacards.TauEsDatacards(es_shifts_str, decay_modes, pt_bins)
	datacards.cb.channel([channel])
	
	for decayMode in args.decay_modes:
		for pt_index, (pt_range) in enumerate(pt_ranges):
			
			category = "mt_inclusive_"+decayMode+"_ptbin"+pt_bins[pt_index]
			output_file = os.path.join(args.output_dir, input_root_filename_template.replace("$", "").format(
					ANALYSIS="ztt",
					CHANNEL=channel,
					BIN=category,
					ERA="13TeV"
			))
			
			input_plot_configs = []
			hadd_commands = []
			
			datacards_per_channel_category = taupogdatacards.TauEsDatacards(cb=datacards.cb.cp().channel([channel]).bin([category]))
	
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

					merged_config={}
					
					# config for rest for each pt range
					# need to get "rest" first in order for corrections of negative bin contents to have an effect
					catForConfig = "cat" + decayMode + "_" + channel
					if (decayMode == "AllDMs" and quantity == "m_2"):
						catForConfig = "catAllDMsNotOneProng_" + channel
					config_rest = sample_settings.get_config(
						samples=[getattr(samples.Samples, sample) for sample in list_of_samples if sample != "ztt"],
						channel=channel,
						category=catForConfig,
						nick_suffix="_" + str(pt_index),
						weight=pt_weights[pt_index],
						lumi=args.lumi * 1000,
						cut_type="tauescuts"
					)
					
					config_rest["x_expressions"] = [quantity] * len(config_rest["nicks"])
					histogram_name_template = bkg_histogram_name_template if nominal else bkg_syst_histogram_name_template
					config_rest["labels"] = [histogram_name_template.replace("$", "").format(
						PROCESS=datacards.configs.sample2process(sample),
						BIN=category,
						SYSTEMATIC=systematic
					) for sample in config_rest["labels"]]
					
					systematics_settings = systematics_factory.get(shape_systematic)(config_rest)
					config_rest = systematics_settings.get_config(shift=(0.0 if nominal else (1.0 if shift_up else -1.0)))
					
					# merge configs
					merged_config = samples.Samples.merge_configs(merged_config, config_rest)
					
					#one ztt nick config for each es shift
					for shift in es_shifts:
						if "ztt" not in list_of_samples:
							continue
						
						config_ztt = sample_settings.get_config(
							samples=[getattr(samples.Samples, sample) for sample in list_of_samples if sample == "ztt"],
							channel=channel,
							category=catForConfig,
							nick_suffix="_" + str(shift).replace(".", "_") + "_" + str(pt_index),
							weight=pt_weights[pt_index],
							lumi=args.lumi * 1000,
							cut_type="tauescuts"
						)
						# shift also pt to account for acceptance effects
						config_ztt["weights"] = [weight.replace("pt_2","("+str(shift)+"*pt_2)") for weight in config_ztt["weights"]]
						
						if decayMode == "OneProng" and quantity == "m_2":
							log.error("Tau mass (m_2) fit not possible in 1prong decay mode")
							sys.exit(1)
						if quantity == "m_2":
							config_ztt["x_expressions"] = [quantity + "*" + str(shift)] * len(config_ztt["nicks"])
						elif quantity == "m_vis":
							config_ztt["x_expressions"] = [quantity + "*sqrt(" + str(shift) + ")"] * len(config_ztt["nicks"])
						
						systematics_settings = systematics_factory.get(shape_systematic)(config_ztt)
						config_ztt = systematics_settings.get_config(shift=(0.0 if nominal else (1.0 if shift_up else -1.0)))
						
						histogram_name_template = sig_histogram_name_template if nominal else sig_syst_histogram_name_template
						config_ztt["labels"] = [histogram_name_template.replace("$", "").format(
							PROCESS=datacards.configs.sample2process(sample),
							BIN=category,
							MASS=str(shift),
							SYSTEMATIC=systematic
						) for sample in config_ztt["labels"]]
						
						# merge configs
						merged_config = samples.Samples.merge_configs(merged_config, config_ztt)
			
					merged_config["directories"] = [args.input_dir]
					merged_config["qcd_subtract_shape"] = [False]
			
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
						
					# set proper binnings of the distributions
					if decayMode == "OneProngPiZeros" and quantity == "m_2":
						if args.tighten_mass_window:
							merged_config["weights"] = [weight+"*(m_2 >= 0.212)*(m_2 < 1.316)" for weight in merged_config["weights"]]
						merged_config.setdefault("x_bins", []).append(["12,0.2,1.4"])
					elif decayMode == "ThreeProng" and quantity == "m_2":
						if args.tighten_mass_window:
							merged_config["weights"] = [weight+"*(m_2 >= 0.848)*(m_2 < 1.41)" for weight in merged_config["weights"]]
						merged_config.setdefault("x_bins", []).append(["9,0.7,1.6"])
					elif decayMode == "AllDMs" and quantity != "m_vis":
						merged_config.setdefault("x_bins", []).append(["14,0.2,1.6"])
					elif decayMode == "OneProng" or quantity == "m_vis":
						merged_config.setdefault("x_bins", []).append(["40,0.0,200.0"])
						merged_config.setdefault("custom_rebin", []).append([40,45,50,55,60,65,70,75,80,85])
					
					input_plot_configs.append(merged_config)
			
			hadd_commands.append("hadd -f {DST} {SRC} && rm {SRC}".format(
				DST=output_file,
				SRC=" ".join(tmp_output_files)
			))

			# delete existing output files
			output_files = list(set([os.path.join(config["output_dir"], config["filename"]+".root") for config in input_plot_configs[:args.n_plots[0]]]))
			for output_file in output_files:
				if os.path.exists(output_file):
					os.remove(output_file)
					log.debug("Removed file \""+output_file+"\" before it is recreated again.")
	
			# create input histograms with HarryPlotter
			higgsplot.HiggsPlotter(list_of_config_dicts=input_plot_configs, n_processes=args.n_processes, n_plots=args.n_plots[0])
			tools.parallelize(_call_command, hadd_commands, n_processes=args.n_processes)
	
	# update CombineHarvester with the yields and shapes
	datacards.extract_shapes(
		os.path.join(args.output_dir, input_root_filename_template.replace("$", "")),
		bkg_histogram_name_template, sig_histogram_name_template,
		bkg_syst_histogram_name_template, sig_syst_histogram_name_template,
		update_systematics=False
	)
	
	# create morphing
	ws = ROOT.RooWorkspace("w","w")
	mes = ROOT.RooRealVar("mes","", 1.0, args.shift_ranges[0], args.shift_ranges[1])
	
	for decayMode in args.decay_modes:
		for pt_index, (pt_range) in enumerate(pt_ranges):
			category = "mt_inclusive_"+decayMode+"_ptbin"+pt_bins[pt_index]
			morphing.BuildRooMorphing(ws,datacards.cb,category,"ZTT",mes,"norm",True,True)
	
	# For some reason the default arguments are not working in the python wrapper
	# of AddWorkspace and ExtractPdfs. Hence, the last argument in either function
	# is set by hand to their default values
	datacards.cb.AddWorkspace(ws, False)
	datacards.cb.cp().signals().ExtractPdfs(datacards.cb, "w", "$BIN_$PROCESS_morph","")
	
	# add bin-by-bin uncertainties
	if args.add_bbb_uncs:
		datacards.add_bin_by_bin_uncertainties(
			processes=datacards.cb.cp().backgrounds().process_set()+datacards.cb.cp().signals().process_set(),
			add_threshold=0.1, merge_threshold=0.5, fix_norm=True
		)
	
	# write datacards
	datacards_cbs = {}
	for decayMode in args.decay_modes:
		for pt_index, (pt_range) in enumerate(pt_ranges):
			category = "mt_inclusive_"+decayMode+"_ptbin"+pt_bins[pt_index]
			dcname = os.path.join(args.output_dir, datacard_template.replace("$", "").format(
							ANALYSIS="ztt",
							CHANNEL=channel,
							BIN=category,
							ERA="13TeV"))
			output = os.path.join(args.output_dir, output_root_template.replace("$", "").format(
							ANALYSIS="ztt",
							CHANNEL=channel,
							BIN=category,
							ERA="13TeV"))
			
			if not os.path.exists(os.path.dirname(dcname)):
				os.makedirs(os.path.dirname(dcname))
			if not os.path.exists(os.path.dirname(output)):
				os.makedirs(os.path.dirname(output))
			datacards.cb.cp().channel([channel]).bin([category]).mass(["*"]).WriteDatacard(dcname, output)
			datacards_cbs[dcname] = datacards.cb
	# write combined datacard
	dcname = os.path.join(args.output_dir, datacard_combined_template.replace("$", "").format(
					ANALYSIS="ztt",
					CHANNEL=channel,
					ERA="13TeV"))
	output = os.path.join(args.output_dir, output_root_combined_template.replace("$", "").format(
					ANALYSIS="ztt",
					CHANNEL=channel,
					ERA="13TeV"))
	
	if not os.path.exists(os.path.dirname(dcname)):
		os.makedirs(os.path.dirname(dcname))
	if not os.path.exists(os.path.dirname(output)):
		os.makedirs(os.path.dirname(output))
	datacards.cb.cp().channel([channel]).mass(["*"]).WriteDatacard(dcname, output)
	datacards_cbs[dcname] = datacards.cb

	#text2workspace call
	datacards_workspaces = {}
	commands = []
	for datacard, cb in datacards_cbs.iteritems():
		commands.append("text2workspace.py {DATACARD} -o {OUTPUT}".format(
			DATACARD=datacard,
			OUTPUT=os.path.splitext(datacard)[0]+".root"))
		datacards_workspaces[datacard] = os.path.splitext(datacard)[0]+".root"
	
	tools.parallelize(_call_command, commands, n_processes=1)
	
	#combine call
	#important: redefine the POI of the fit, such that is the es-shift and not the signal scale modifier (r)
	commands = []
	commands.extend([[
		"combine -M MaxLikelihoodFit -m 1.0 --redefineSignalPOIs mes -v {VERBOSITY} --robustFit=1 --preFitValue=1. --X-rtd FITTER_NEW_CROSSING_ALGO --minimizerAlgoForMinos=Minuit2 --minimizerToleranceForMinos=0.1 --X-rtd FITTER_NEVER_GIVE_UP --X-rtd FITTER_BOUND --minimizerAlgo=Minuit2 --minimizerStrategy=0 --minimizerTolerance=0.1 --cminFallbackAlgo \"Minuit2,0:1.\" {WORKSPACE}".format(
			VERBOSITY=args.combine_verbosity,
			WORKSPACE=os.path.splitext(datacard)[0]+".root",
		),
		os.path.dirname(datacard)
	] for datacard, cb in datacards_cbs.iteritems()])
	
	tools.parallelize(_call_command, commands, n_processes=1)
	
	#2nd combine call to get deltaNLL distribution
	#(always done, since the bestfit value and uncertainties are taken from this scan)
	commands = []
	commands.extend([[
		"combine -M MultiDimFit --algo grid --points {BINNING} --setPhysicsModelParameterRanges mes={RANGE} --redefineSignalPOIs mes -v {VERBOSITY} --robustFit=1 --preFitValue=1. --X-rtd FITTER_NEW_CROSSING_ALGO --minimizerAlgoForMinos=Minuit2 --minimizerToleranceForMinos=0.1 --X-rtd FITTER_NEVER_GIVE_UP --X-rtd FITTER_BOUND --minimizerAlgo=Minuit2 --minimizerStrategy=0 --minimizerTolerance=0.1 --cminFallbackAlgo \"Minuit2,0:1.\" {WORKSPACE}".format(
			BINNING=int((args.shift_ranges[1]-args.shift_ranges[0])/args.shift_binning),
			RANGE=str(args.shift_ranges[0])+","+str(args.shift_ranges[1]),
			VERBOSITY=args.combine_verbosity,
			WORKSPACE=os.path.splitext(datacard)[0]+".root",
		),
		os.path.dirname(datacard)
	] for datacard, cb in datacards_cbs.iteritems()])
	
	tools.parallelize(_call_command, commands, n_processes=1)
	
	#plot nuisance impacts
	datacards.print_pulls(datacards_cbs, args.n_processes, "-A -p {POI}".format(POI="mes"))
	datacards.nuisance_impacts(datacards_cbs, datacards_workspaces, args.n_processes, "--redefineSignalPOIs mes")
	
	#postfitshapes call
	datacards_postfit_shapes = {}
	commands = []
	commands.extend(["PostFitShapesFromWorkspace --postfit -w {WORKSPACE} -d {DATACARD} -o {OUTPUT} -f {FIT_RESULT}".format(
			WORKSPACE=datacards_workspaces[datacard],
			DATACARD=datacard,
			OUTPUT=os.path.splitext(datacard)[0]+"_fit_s.root",
			FIT_RESULT=os.path.join(os.path.dirname(datacard), "mlfit.root:fit_s"),
	) for datacard, cb in datacards_cbs.iteritems()])
	datacards_postfit_shapes.setdefault("fit_s", {}).update({
			datacard : os.path.splitext(datacard)[0]+"_fit_s.root"
	for datacard, cb in datacards_cbs.iteritems()})
	
	tools.parallelize(_call_command, commands, n_processes=args.n_processes)
	
	#pull plots
	datacards.pull_plots(datacards_postfit_shapes, s_fit_only=True, plotting_args={"fit_poi" : ["mes"]}, n_processes=args.n_processes)
	
	#plot postfit
	postfit_plot_configs = [] #reset list containing the plot configs
	bkg_plotting_order = ["ZTT", "ZLL", "TT", "VV", "W", "QCD"]
	
	for level in ["prefit", "postfit"]:
		for datacard in datacards_cbs.keys():
			postfit_shapes = datacards_postfit_shapes.get("fit_s", {}).get(datacard)
			for category in datacards_cbs[datacard].cp().bin_set():

				if (("combined" not in datacard) and (category not in datacard)):
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
				processes = [p.replace("VV", "VV_noplot").replace("W", "W_noplot") for p in processes]
				processes_to_plot = [p for p in processes if not "noplot" in p]
				processes_to_plot.insert(3, "EWK")
				config["sum_nicks"].append("VV_noplot W_noplot")
				config["sum_scale_factors"].append("1.0 1.0")
				config["sum_result_nicks"].append("EWK")
				
				config["files"] = [postfit_shapes]
				config["folders"] = [category+"_"+level]
				config["nicks"] = [processes + ["noplot_TotalBkg", "noplot_TotalSig", "data_obs"]]
				config["x_expressions"] = [p.strip("_noplot") for p in processes] + ["TotalBkg", "TotalSig", "data_obs"]
				config["stacks"] = ["bkg"]*len(processes_to_plot) + ["data"] + [""]
				config["labels"] = [label.lower() for label in processes_to_plot + ["totalbkg"] + ["data_obs"]]
				config["colors"] = [color.lower() for color in processes_to_plot + ["#000000 transgrey"] + ["data_obs"]]
				if args.colors_dm_dependent:
					if "OneProng" in category and not "OneProngPiZeros" in category:
						config["colors"] = [color.replace("ztt", "#000000 #FF6633") for color in config["colors"]]
					elif "OneProngPiZeros" in category:
						config["colors"] = [color.replace("ztt", "#000000 kOrange-4") for color in config["colors"]]
					elif "ThreeProng" in category:
						config["colors"] = [color.replace("ztt", "#000000 #FFFFCC") for color in config["colors"]]
				config["markers"] = ["HIST"]*len(processes_to_plot) + ["E2"] + ["E"]
				config["legend_markers"] = ["F"]*len(processes_to_plot) + ["F"] + ["ELP"]
				
				config["y_label"] = "Events / bin"
				if "OneProngPiZeros" in category and quantity == "m_2":
					config["x_label"] = "m_{#tau_{h}} [GeV]"
					config["x_lims"] = [0.2,1.4]
				elif "ThreeProng" in category and quantity == "m_2":
					config["x_label"] = "m_{#tau_{h}} [GeV]"
					config["x_lims"] = [0.8,1.5]
				elif "AllDMs" in category and quantity == "m_2":
					config["x_label"] = "m_{#tau_{h}} [GeV]"
					config["x_lims"] = [0.2,1.8]
				elif "OneProng" in category or quantity == "m_vis":
					config["x_label"] = "m_{vis}(#mu#tau_{h}) [GeV]"
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
				config["cms"] = True
				config["extra_text"] = "Preliminary"
				config["year"] = args.era
				config["output_dir"] = os.path.join(os.path.dirname(datacard), "plots")
				config["filename"] = level+"_"+category+"_"+quantity
				#config["formats"] = ["png", "pdf"]
				
				decayMode = category.split("_")[-2]
				ptBin = int(category.split("_")[-1].split("ptbin")[-1])
				config["texts"] = [decayMode_dict[decayMode]["label"], pt_strings[ptBin]]
				config["texts_x"] = [0.52, 0.52]
				config["texts_y"] = [0.81, 0.74]
				config["texts_size"] = [0.055]
				
				if not (config["output_dir"] in www_output_dirs_postfit):
					www_output_dirs_postfit.append(config["output_dir"])
				
				postfit_plot_configs.append(config)
	
	higgsplot.HiggsPlotter(list_of_config_dicts=postfit_plot_configs, n_processes=args.n_processes, n_plots=args.n_plots[1])

	# compute parabola from NLL scan and from here extract the best fit value and the uncertainties
	output_dict_mu, output_dict_errHi, output_dict_errLo = {}, {}, {}
	output_dict_scan_mu, output_dict_scan_errHi, output_dict_scan_errLo = {}, {}, {}
	
	for decayMode in decay_modes:
		for ptBin in pt_bins:
			output_dict_mu.setdefault(decayMode, {})[ptBin] = 0
			output_dict_errHi.setdefault(decayMode, {})[ptBin] = 0
			output_dict_errLo.setdefault(decayMode, {})[ptBin] = 0
			output_dict_scan_mu.setdefault(decayMode, {})[ptBin] = 0
			output_dict_scan_errHi.setdefault(decayMode, {})[ptBin] = 0
			output_dict_scan_errLo.setdefault(decayMode, {})[ptBin] = 0
	
	parabola_plot_configs = []
	ptbin_plot_configs = []
	for datacard, cb in datacards_cbs.iteritems():
		filename = os.path.join(os.path.dirname(datacard), "higgsCombineTest.MultiDimFit.mH120.root")
		if "combined" in filename:
			continue
		
		resultsfilename = os.path.join(os.path.dirname(datacard), "mlfit.root")
		resultsfile = ROOT.TFile(resultsfilename)
		resultstree = resultsfile.Get("tree_fit_sb")
		resultstree.GetEntry(0)
		
		for category in datacards_cbs[datacard].cp().bin_set():
			if category not in filename:
				continue
			
			decayMode = category.split("_")[-2]
			ptBin = category.split("_")[-1].split("ptbin")[-1]
			
			file = ROOT.TFile(filename)
			tree = file.Get("limit")
			mes_list = []
			deltaNLL_list = []
			deltaNLLshifted_list = []
			
			# the entry '0' contains the best shift and deltaNLL=0 --> start from 1
			for entry in range(1, tree.GetEntries()):
				tree.GetEntry(entry)
				mes_list.append(tree.mes)
				deltaNLL_list.append(2*tree.deltaNLL)
			
			#find minimum
			for index, (nll) in enumerate(deltaNLL_list):
				if index == 0:
					min_nll = deltaNLL_list[0]
					min_shift = mes_list[0]
				if min_nll > deltaNLL_list[index]:
					min_nll = deltaNLL_list[index]
					min_shift = mes_list[index]
			
			#find left-right intercept for 1sigma uncertainty
			for index, (nll) in enumerate(deltaNLL_list):
				deltaNLLshifted_list.append(nll - min_nll)
			
			found2sigmaLow, found1sigmaLow, found1sigmaHi, found2sigmaHi = False, False, False, False
			err2sigmaLow,err1sigmaLow, err1sigmaHi, err2sigmaHi = 0.0, 0.0, 0.0, 0.0
			
			for index, (nll) in enumerate(deltaNLLshifted_list):
				if (mes_list[index] <= min_shift):
					if (nll <= 4.0 and not found2sigmaLow): #crossing 2-sigma line from the left
						found2sigmaLow = True
						err2sigmaLow = abs((mes_list[index-1]+mes_list[index])/2.0 - min_shift)
					if (nll <= 1.0 and not found1sigmaLow): #crossing 1-sigma line from the left
						found1sigmaLow = True
						err1sigmaLow = abs((mes_list[index-1]+mes_list[index])/2.0 - min_shift)
				else:
					if (nll >= 1.0 and not found1sigmaHi): #crossing 1-sigma line again
						found1sigmaHi = True
						err1sigmaHi = abs((mes_list[index]+mes_list[index+1])/2.0 - min_shift)
					if (nll >= 4.0 and not found2sigmaHi): #crossing 2-sigma line again
						found2sigmaHi = True
						err2sigmaHi = abs((mes_list[index]+mes_list[index+1])/2.0 - min_shift)
			
			#values for parabola plot
			xvalues = ""
			yvalues = ""
			for index, (nll) in enumerate(deltaNLLshifted_list):
				xvalues += str((mes_list[index]-1.0)*100) + " "
				yvalues += str(nll) + " "
		
			output_dict_mu[decayMode][ptBin] = (resultstree.mu-1.0)*100
			output_dict_errHi[decayMode][ptBin] = resultstree.muHiErr*100
			output_dict_errLo[decayMode][ptBin] = resultstree.muLoErr*100
			output_dict_scan_mu[decayMode][ptBin] = (min_shift-1.0)*100
			output_dict_scan_errHi[decayMode][ptBin] = err1sigmaHi*100
			output_dict_scan_errLo[decayMode][ptBin] = err1sigmaLow*100
			
			config = {}
			config["input_modules"] = ["InputInteractive"]
			config["analysis_modules"] = ["AddLine"]
			config["x_label"] = "#tau_{h}-ES [%]"
			config["y_label"] = "-2 \\\mathrm{\\\Delta ln} \\\mathscr{L}"
			config["x_lims"] = [(min(es_shifts)-1.0)*100, (max(es_shifts)-1.0)*100]
			config["y_lims"] = [0.0, 10.0]
			config["x_lines"] = ["-6 6"]
			config["y_lines"] = ["1 1", "4 4"]
			config["markers"] = ["P", "L", "L"]
			config["marker_styles"] = [5]
			config["line_styles"] = [2]
			config["colors"] = ["kBlack", "kBlue", "kBlue"]
			config["output_dir"] = os.path.join(os.path.dirname(datacard), "plots")
			config["filename"] = "parabola_" + category + "_" + quantity
			config["x_expressions"] = [xvalues]
			config["y_expressions"] = [yvalues]
			config["texts"] = [decayMode_dict[decayMode]["label"], pt_strings[int(ptBin)], "1#sigma", "2#sigma"]
			config["texts_x"] = [0.52, 0.52, 0.98, 0.98]
			config["texts_y"] = [0.81, 0.74, 0.23, 0.46]
			config["texts_size"] = [0.035]
			config["cms"] = True
			config["extra_text"] = "Preliminary"
			config["year"] = args.era
			
			if not (config["output_dir"] in www_output_dirs_parabola):
				www_output_dirs_parabola.append(config["output_dir"])
			
			parabola_plot_configs.append(config)
		resultsfile.Close()

	#plot parabolas
	higgsplot.HiggsPlotter(list_of_config_dicts=parabola_plot_configs, n_processes=args.n_processes, n_plots=args.n_plots[1])
	
	# plot best fit result as function of pt bins
	config = {}
	xbins, xerrs, ybins, yerrslo, yerrshi = [], [], [], [], []
	for decayMode in decay_modes:
		xval, xerrsval, yval, yerrsloval, yerrshival = "", "", "", "", ""
		for index, ptBin in enumerate(pt_bins[1:]):
			yval += str(output_dict_scan_mu[decayMode][ptBin])+" "
			yerrsloval += str(output_dict_scan_errLo[decayMode][ptBin])+" "
			yerrshival += str(output_dict_scan_errHi[decayMode][ptBin])+" "
			if index < (len(pt_bins[1:])-1):
				xval += str((float(pt_ranges[index+1])+float(pt_ranges[index+2]))/2.0)+" "
				xerrsval += str((float(pt_ranges[index+2])-float(pt_ranges[index+1]))/2.0)+" "
		
		if len(pt_bins[1:]) > 0:
			xval += str((float(pt_ranges[index+1])+200.0)/2.0)
			xerrsval += str((200.0 - float(pt_ranges[index+1]))/2.0)
		else: # no pt ranges were given - plot only inclusive result
			xval += "110.0 "
			xerrsval += "90.0 "
			yval += str(output_dict_scan_mu[decayMode]["0"])+" "
			yerrsloval += str(output_dict_scan_errLo[decayMode]["0"])+" "
			yerrshival += str(output_dict_scan_errHi[decayMode]["0"])+" "
		
		xbins.append(xval)
		xerrs.append(xerrsval)
		ybins.append(yval)
		yerrslo.append(yerrsloval)
		yerrshi.append(yerrshival)
		config.setdefault("colors", []).append(decayMode_dict[decayMode]["color"])
		config.setdefault("labels", []).append(decayMode_dict[decayMode]["label"].split(" decay")[0])
	
	config["input_modules"] = ["InputInteractive"]
	config["x_lims"] = [0.0, 200.0]
	config["y_lims"] = [(min(es_shifts)-1.0)*100, (max(es_shifts)-1.0)*100]
	config["x_label"] = "p^{#tau_{h}}_{T} [GeV]"
	config["y_label"] = "#tau_{h}-ES [%]"
	config["markers"] = ["P"]
	config["legend"] = [0.2,0.78,0.6,0.9]
	config["output_dir"] = os.path.expandvars(args.output_dir)+"/datacards/"
	config["filename"] = "result_vs_pt_" + quantity
	config["x_expressions"] = xbins
	config["x_errors"] = xerrs
	config["x_errors_up"] = xerrs
	config["y_expressions"] = ybins
	config["y_errors"] = yerrslo
	config["y_errors_up"] = yerrshi
	
	if not (config["output_dir"] in www_output_dirs_ptbin):
		www_output_dirs_ptbin.append(config["output_dir"])
	
	ptbin_plot_configs.append(config)
	
	higgsplot.HiggsPlotter(list_of_config_dicts=ptbin_plot_configs, n_processes=args.n_processes, n_plots=args.n_plots[1])

	# print output table to shell
	print "################### Fit results table (in parentheses numbers from logL scan) ###################"
	row_format = "{:^20}" * (len(decay_modes) + 1)
	print row_format.format("", *decay_modes)
	print
	for ptBin in pt_bins:
		if ptBin == "0":
			print "{:^20}".format("Inclusive"),
		else:
			print "{:^20}".format("Pt bin "+ptBin),
		for decayMode in decay_modes:
			if decayMode != decay_modes[-1]:
				print "{:<10.2f}({:<3.2f})%\t".format(output_dict_mu[decayMode][ptBin],output_dict_scan_mu[decayMode][ptBin]),
			else:
				print "{:<10.2f}({:<3.2f})%\t".format(output_dict_mu[decayMode][ptBin],output_dict_scan_mu[decayMode][ptBin])
		print "{:^20}".format("+ 1sigma "),
		for decayMode in decay_modes:
			if decayMode != decay_modes[-1]:
				print "{:<10.2f}({:<3.2f})%\t".format(output_dict_errHi[decayMode][ptBin],output_dict_scan_errHi[decayMode][ptBin]),
			else:
				print "{:<10.2f}({:<3.2f})%\t".format(output_dict_errHi[decayMode][ptBin],output_dict_scan_errHi[decayMode][ptBin])
		print "{:^20}".format("- 1sigma "),
		for decayMode in decay_modes:
			if decayMode != decay_modes[-1]:
				print "{:<10.2f}({:<3.2f})%\t".format(output_dict_errLo[decayMode][ptBin],output_dict_scan_errLo[decayMode][ptBin]),
			else:
				print "{:<10.2f}({:<3.2f})%\t".format(output_dict_errLo[decayMode][ptBin],output_dict_scan_errLo[decayMode][ptBin])
		print

	# it's not pretty but it works :)
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
		for output_dir in www_output_dirs_ptbin:
			subpath = os.path.normpath(output_dir).split("/")[-1]
			output_filenames = []
			for config in ptbin_plot_configs:
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
