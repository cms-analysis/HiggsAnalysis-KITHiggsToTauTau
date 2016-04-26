#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import argparse
import copy
import os

import CombineHarvester.CombineTools.ch as ch
import CombineHarvester.CombinePdfs.morphing as morphing
import ROOT

import Artus.Utility.tools as tools
import Artus.Utility.jsonTools as jsonTools

import HiggsAnalysis.KITHiggsToTauTau.plotting.higgsplot as higgsplot
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.samples_run2 as samples
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.systematics_run2 as systematics
import HiggsAnalysis.KITHiggsToTauTau.datacards.taupogdatacards as taupogdatacards



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

	models = {
		"default" : {
			"P" : "HiggsAnalysis.KITHiggsToTauTau.datacards.zttmodels:ztt_xsec",
			"fit" : {
				"" : {
					"method" : "MaxLikelihoodFit",
					"options" : "--skipBOnlyFit --expectSignal=1 --toys -1",
					"poi" : "r",
				},
			},
			"fit_plots" : {
				"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/combine/ztt_mlfit_bestfitvalues.json"
			},
		}
	}

	parser = argparse.ArgumentParser(description="Create ROOT inputs and datacards for tau energy scale measurement.",
	                                 parents=[logger.loggingParser])

	parser.add_argument("-i", "--input-dir", required=True,
	                    help="Input directory.")
	parser.add_argument("--quantity", default="m_2", choices=["m_2","m_vis"],
	                    help="Quantity. [Default: %(default)s]")
	parser.add_argument("--es-shifts", nargs="*",
	                    default=[0.96,0.97,0.98,0.99,1.0,1.01,1.02,1.03,1.04,1.05,1.06],
	                    help="Energy scale shifts."),
	parser.add_argument("--pt-ranges", nargs="*",
	                    default=["20.0"],
	                    help="Enter the lower bin edges for the pt ranges."	)
	parser.add_argument("--decay-modes", nargs="+",
	                    default=["OneProngPiZeros"],
	                    choices=["OneProng","OneProngPiZeros", "ThreeProng"],
	                    help="Decay modes of reconstructed hadronic tau leptons in Z #rightarrow #tau#tau. [Default: %(default)s]")
	parser.add_argument("--add-bbb-uncs", action="store_true", default=False,
	                    help="Add bin-by-bin uncertainties. [Default: %(default)s]")
	parser.add_argument("--lumi", type=float, default=2.301,
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
	
	
	args = parser.parse_args()
	logger.initLogger(args)
	
	args.output_dir = os.path.abspath(os.path.expandvars(args.output_dir))
	if args.clear_output_dir and os.path.exists(args.output_dir):
		logger.subprocessCall("rm -r " + args.output_dir, shell=True)
	
	# initialisations for plotting
	sample_settings = samples.Samples()
	systematics_factory = systematics.SystematicsFactory()
	
	plot_configs = []
	hadd_commands = []

	datacards = taupogdatacards.TauEsDatacards()
	
	# initialise datacards
	tmp_input_root_filename_template = "input/${ANALYSIS}_${CHANNEL}_${BIN}_${SYSTEMATIC}_${ERA}.root"
	input_root_filename_template = "input/${ANALYSIS}_${CHANNEL}_${BIN}_${ERA}.root"
	bkg_histogram_name_template = "${BIN}/${PROCESS}"
	sig_histogram_name_template = "${BIN}/${PROCESS}${MASS}"
	bkg_syst_histogram_name_template = "${BIN}/${PROCESS}_${SYSTEMATIC}"
	sig_syst_histogram_name_template = "${BIN}/${PROCESS}${MASS}_${SYSTEMATIC}"
	datacard_filename_templates = [
		"datacards/${CHANNEL}/${ANALYSIS}_${CHANNEL}_${ERA}.txt",
		"datacards/combined/${ANALYSIS}_${ERA}.txt",
	]
	output_root_filename_template = "datacards/common/${ANALYSIS}.input_${ERA}.root"
	
	# restrict CombineHarvester to configured channels:
	channel = "mt"
	category = "mt_inclusive"
	quantity = args.quantity
	datacards.cb.channel([channel])

	output_file = os.path.join(args.output_dir, input_root_filename_template.replace("$", "").format(
					ANALYSIS="ztt",
					CHANNEL=channel,
					BIN=category,
					ERA="13TeV"
	))
	
	for decayMode in args.decay_modes:
		for pt_index, (pt_range) in enumerate(args.pt_ranges):
			
			merged_config={}
			
			lowEdge = str(args.pt_ranges[pt_index])
			if len(args.pt_ranges) > pt_index+1:
				highEdge = args.pt_ranges[pt_index+1]
			else:
				highEdge = "500"
			
			ptweight = "(pt_2>" + lowEdge + ")*(pt_2<" + highEdge + ")"
			
			datacards_per_channel_category = taupogdatacards.TauEsDatacards(cb=datacards.cb.cp().channel([channel]).bin([category]))
	
			tmp_output_files = []

			for shape_systematic, list_of_samples in datacards_per_channel_category.get_samples_per_shape_systematic().iteritems():
				nominal = (shape_systematic == "nominal")
		
				#for the moment, no shape systematics
				if not nominal:
					continue
		
				list_of_samples = (["data"] if nominal else []) + [datacards.configs.process2sample(process) for process in list_of_samples]
		
				for shift_up in ([True] if nominal else [True, False]):
					systematic = "nominal" if nominal else (shape_systematic + ("Up" if shift_up else "Down"))
			
					log.debug("Create inputs for (samples, systematic) = ([\"{samples}\"], {systematic}), (channel, category) = ({channel}, {category}).".format(
						samples="\", \"".join(list_of_samples),
						channel=channel,
						category=category,
						systematic=systematic
					))
		
					# config for rest for each pt range
					# need to get "rest" first in order for corrections of negative bin contents to have an effect
					config_rest = sample_settings.get_config(
						samples=[getattr(samples.Samples, sample) for sample in list_of_samples if sample != "ztt" ],
						channel=channel,
						category="cat" + decayMode + "_" + channel,
						nick_suffix="_" + str(pt_index),
						weight=ptweight,
						lumi=args.lumi * 1000
					)
					
					config_rest["x_expressions"] = [quantity] * len(config_rest["nicks"])
					histogram_name_template = bkg_histogram_name_template if nominal else bkg_syst_histogram_name_template
					config_rest["labels"] = [histogram_name_template.replace("$", "").format(
						PROCESS=datacards.configs.sample2process(sample),
						BIN=category,
						SYSTEMATIC=systematic
					) for sample in config_rest["labels"]]
					
					# merge configs
					merged_config = samples.Samples.merge_configs(merged_config, config_rest)
					
					#one ztt nick config for each es shift
					for shift in args.es_shifts:
						config_ztt = sample_settings.get_config(
							samples=[getattr(samples.Samples, "ztt")],
							channel=channel,
							category="cat" + decayMode + "_" + channel,
							nick_suffix="_" + str(shift).replace(".", "_") + "_" + str(pt_index),
							weight=ptweight,
							lumi=args.lumi * 1000
						)
						
						if decayMode == "OneProng" and quantity == "m_2":
							log.error("Tau mass (m_2) fit not possible in 1prong decay mode")
							sys.exit(1)
						if quantity == "m_2":
							config_ztt["x_expressions"] = [quantity + "*" + str(shift)] * len(config_ztt["nicks"])
						elif quantity == "m_vis":
							config_ztt["x_expressions"] = [quantity + "*sqrt(" + str(shift) + ")"] * len(config_ztt["nicks"])
						
						histogram_name_template = sig_histogram_name_template if nominal else sig_syst_histogram_name_template
						config_ztt["labels"] = [histogram_name_template.replace("$", "").format(
							PROCESS=datacards.configs.sample2process(sample),
							BIN=category,
							MASS=str(shift),
							SYSTEMATIC=systematic
						) for sample in config_ztt["labels"]]
						
						# merge configs
						merged_config = samples.Samples.merge_configs(merged_config, config_ztt)
					
					systematics_settings = systematics_factory.get(shape_systematic)(merged_config)
					# TODO: evaluate shift from datacards_per_channel_category.cb
					merged_config = systematics_settings.get_config(shift=(0.0 if nominal else (1.0 if shift_up else -1.0)))
			
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
						merged_config.setdefault("x_bins", []).append(["39,0.3,4.2"])
					elif decayMode == "ThreeProng" and quantity == "m_2":
						merged_config.setdefault("x_bins", []).append(["7,0.8,1.5"])
					elif decayMode == "OneProng" or quantity == "m_vis":
						merged_config.setdefault("x_bins", []).append(["20,0.0,200.0"])
					
					plot_configs.append(merged_config)
			
			hadd_commands.append("hadd -f {DST} {SRC} && rm {SRC}".format(
				DST=output_file,
				SRC=" ".join(tmp_output_files)
			))

			# delete existing output files
			output_files = list(set([os.path.join(config["output_dir"], config["filename"]+".root") for config in plot_configs[:args.n_plots[0]]]))
			for output_file in output_files:
				if os.path.exists(output_file):
					os.remove(output_file)
					log.debug("Removed file \""+output_file+"\" before it is recreated again.")
	
			# create input histograms with HarryPlotter
			higgsplot.HiggsPlotter(list_of_config_dicts=plot_configs, n_processes=args.n_processes, n_plots=args.n_plots[0])
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
					processes=datacards.cb.cp().backgrounds().process_set()+datacards.cb.cp().signals().process_set(),
					add_threshold=0.1, merge_threshold=0.5, fix_norm=True
				)
			
			# create morphing
			ws = ROOT.RooWorkspace("w","w")
			mes = ROOT.RooRealVar("mes","", 1.0, 0.94, 1.06)
			
			morphing.BuildRooMorphing(ws,datacards.cb,category,datacards.configs.sample2process(sample),mes,"norm",True,True)
			
			# For some reason the default arguments are not working in the python wrapper
			# of AddWorkspace and ExtractPdfs. Hence, the last argument in either function
			# is set by hand to their default values
			datacards.cb.AddWorkspace(ws, False)
			datacards.cb.cp().signals().ExtractPdfs(datacards.cb, "w", "$BIN_$PROCESS_morph","")
	
			# write datacards
			datacards_cbs = {}
			for datacard_filename_template in datacard_filename_templates:
				dcname = os.path.join(args.output_dir, datacard_filename_template.replace("$", "").format(
										ANALYSIS="ztt",
										CHANNEL=channel,
										ERA="13TeV"))
				output = os.path.join(args.output_dir, output_root_filename_template.replace("$", "").format(
										ANALYSIS="ztt",
										ERA="13TeV"))
				
				if not os.path.exists(os.path.dirname(dcname)):
					os.makedirs(os.path.dirname(dcname))
				if not os.path.exists(os.path.dirname(output)):
					os.makedirs(os.path.dirname(output))
				datacards.cb.cp().channel([channel]).mass(["*"]).WriteDatacard(dcname, output)
				datacards_cbs[dcname] = datacards.cb
			
			#text2workspace call
			commands = []
			for datacard, cb in datacards_cbs.iteritems():
				commands.append("text2workspace.py {DATACARD} -o {OUTPUT}".format(
					DATACARD=datacard,
					OUTPUT=os.path.splitext(datacard)[0]+".root"))
		
			tools.parallelize(_call_command, commands, n_processes=1)
			
			#combine call
			commands = []
			commands.extend([[
				"combine -M MaxLikelihoodFit -m 1.0 {WORKSPACE}".format(
					WORKSPACE=os.path.splitext(datacard)[0]+".root",
				),
				os.path.dirname(datacard)
			] for datacard, cb in datacards_cbs.iteritems()])
		
			tools.parallelize(_call_command, commands, n_processes=1)
