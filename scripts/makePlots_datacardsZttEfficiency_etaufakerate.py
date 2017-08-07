#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import argparse
import copy
import os

import CombineHarvester.CombineTools.ch as ch
import ROOT

import Artus.Utility.tools as tools
import Artus.Utility.jsonTools as jsonTools

import HiggsAnalysis.KITHiggsToTauTau.plotting.higgsplot as higgsplot
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.systematics_run2 as systematics
import HiggsAnalysis.KITHiggsToTauTau.datacards.zttxsecdatacards as zttxsecdatacards
import HiggsAnalysis.KITHiggsToTauTau.uncertainties.uncertainties as uncertainties
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.samples_run2_2016 as samples


def _call_command(command):
	log.debug(command)
	logger.subprocessCall(command, shell=True)


if __name__ == "__main__":

	models = {
		"tauideff" : {
			"P" : "HiggsAnalysis.KITHiggsToTauTau.datacards.zttmodels:ztt_eff",
			"exclude_cuts" : ["iso_2"],
			"fit" : {
				"poi" : "r",
			},
			"fit_plots" : {
				"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/combine/ztt_mlfit_bestfitvalues.json"
			},
		},
		"etaufakerate" : {
			"P" : "HiggsAnalysis.KITHiggsToTauTau.datacards.zttmodels:ztt_eff",
			"exclude_cuts" : ["dilepton_veto", "extra_lepton_veto", "anti_e_tau_discriminators"],
			"fit" : {
				"poi" : "r",
			},
			"fit_plots" : {
				"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/combine/ztt_mlfit_bestfitvalues.json"
			},
		},
		"mutaufakerate" : {
			"P" : "HiggsAnalysis.KITHiggsToTauTau.datacards.zttmodels:ztt_eff",
			"exclude_cuts" : ["anti_mu_tau_discriminators"],
			"fit" : {
				"poi" : "r",
			},
			"fit_plots" : {
				"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/combine/ztt_mlfit_bestfitvalues.json"
			},
		}
	}

	parser = argparse.ArgumentParser(description="Create ROOT inputs and datacards for tau ID efficiency or lep->tau fake-rate measurement.",
	                                 parents=[logger.loggingParser])

	parser.add_argument("-i", "--input-dir", required=True,
	                    help="Input directory.")
	parser.add_argument("-m", "--model", required=True,
	                    choices=models.keys(),
	                    help="Statistics models. [Default: %(default)s]")
	parser.add_argument("-c", "--channel", action="append",
	                    default=["all"],
	                    help="Channel. This argument can be set multiple times. [Default: %(default)s]")
	parser.add_argument("--categories", action="append", nargs="+",
	                    default=[["all"]] * len(parser.get_default("channel")),
	                    help="Categories per channel. This argument needs to be set as often as --channels. [Default: %(default)s]")
	parser.add_argument("-x", "--quantity", default="m_vis",
	                    help="Quantity. [Default: %(default)s]")
	parser.add_argument("--lumi", type=float, default=samples.default_lumi/1000.0,
	                    help="Luminosity for the given data in fb^(-1). [Default: %(default)s]")
	parser.add_argument("--add-bbb-uncs", action="store_true", default=True,
	                    help="Add bin-by-bin uncertainties. [Default: %(default)s]")
	parser.add_argument("-w", "--weight", default="1.0",
	                    help="Additional weight (cut) expression. [Default: %(default)s]")
	parser.add_argument("--analysis-modules", default=[], nargs="+",
	                    help="Additional analysis Modules. [Default: %(default)s]")	
	parser.add_argument("-r", "--ratio", default=True, action="store_true",
	                    help="Add ratio subplot. [Default: %(default)s]")
	parser.add_argument("-a", "--args", default="",
	                    help="Additional Arguments for HarryPlotter. [Default: %(default)s]")
        parser.add_argument("--debug-plots", default=False, action="store_true",
                            help="Produce debug Plots [Default: %(default)s]")
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
	
	args.output_dir = os.path.abspath(os.path.expandvars(args.output_dir))
	if args.clear_output_dir and os.path.exists(args.output_dir):
		logger.subprocessCall("rm -r " + args.output_dir, shell=True)

	weight_string = "(fabs(eta_2) < 1.460)"
	#weight_string = "(fabs(eta_2) < 1.460)*(decayMode_2 == 1)"
	#weight_string = "(fabs(eta_2) > 1.558)"
	#weight_string = "1.0"
	
	# initialisations for plotting
	if args.model == "etaufakerate":
		import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.samples_run2_etaufakerate_2016 as samples
	else:
		import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.samples_run2_2016 as samples
	
	sample_settings = samples.Samples()
	systematics_factory = systematics.SystematicsFactory()
	
	plot_configs = []
	hadd_commands = []

	if args.model in ["etaufakerate", "mutaufakerate"]:
		datacards = zttxsecdatacards.ZttLepTauFakeRateDatacards()
	elif args.model == "tauideff":
		datacards = zttxsecdatacards.ZttEffDatacards()
	
	# statistical models
	model_settings = models.get(args.model, {})
	fit_settings = model_settings.get("fit", {"" : {}})
	
	excludecut_settings = model_settings['exclude_cuts'] if model_settings.has_key('exclude_cuts') else ['']
	
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
        
        args.channel = ['et']
	
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
			
			if args.model in ["etaufakerate", "mutaufakerate"]: 
				datacards_per_channel_category = zttxsecdatacards.ZttLepTauFakeRateDatacards(cb=datacards.cb.cp().channel([channel]).bin([category]))
			elif args.model == "tauideff":
				datacards_per_channel_category = zttxsecdatacards.ZttEffDatacards(cb=datacards.cb.cp().channel([channel]).bin([category]))
			
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
                                log.debug(list_of_samples)
                                log.debug(shape_systematic)
                        
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
							category=None,
							weight = weight_string,
							lumi = args.lumi * 1000,
							exclude_cuts=excludecut_settings,
							cut_type=category[3:]
					)
					
					if args.model in ["etaufakerate", "mutaufakerate"]:
						#do not apply shape subtraction in QCD estimate, to avoid poorly described templates
						config["qcd_subtract_shape"] = [False]
						config["x_bins"] = ["60,0,300"]
						if "pass" in category:
							#config["custom_rebin"] = [60,70,80,90,100,110,120]
							config["custom_rebin"] = [60,65,70,75,80,85,90,95,100,105,110,115,120]
						elif "fail" in category:
							config["custom_rebin"] = [60,120]
					if args.model == "tauideff":
						config["x_bins"] = ["33,35,200"]
						config["qcd_extrapolation_factors_ss_os"] = [1.06]
						#if "pass" in category:
							#config["custom_rebin"] = [20,30,40,50,60,70,80,90,100,110,120,130,140,150]
						#elif "fail" in category:
							#config["custom_rebin"] = [20,30,40,50,60,70,80,90,100,110,120,130,140,150]
					
					config["x_expressions"] = [args.quantity]
					config["directories"] = [args.input_dir]
					
					systematics_settings = systematics_factory.get(shape_systematic)(config)
					# TODO: evaluate shift from datacards_per_channel_category.cb
					config = systematics_settings.get_config(shift=(0.0 if nominal else (1.0 if shift_up else -1.0)))
					
					histogram_name_template = bkg_histogram_name_template if nominal else bkg_syst_histogram_name_template
					config["labels"] = [histogram_name_template.replace("$", "").format(
							PROCESS=datacards.configs.sample2process(sample),
							BIN=category,
							SYSTEMATIC=systematic
					) for sample in config["labels"]]
					
                                        
                                        #import pprint 
                                        #print "sample", sample
                                        #if(sample == 'ztt'):
                                              #  pprint.pprint(config)
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
	output_files = list(set([os.path.join(config["output_dir"], config["filename"]+".root") for config in plot_configs[:args.n_plots[0]]]))
	for output_file in output_files:
		if os.path.exists(output_file):
			os.remove(output_file)
			log.debug("Removed file \""+output_file+"\" before it is recreated again.")
	

	# create input histograms with HarryPlotter
        higgsplot.HiggsPlotter(list_of_config_dicts=plot_configs, list_of_args_strings=[args.args], n_processes=args.n_processes, n_plots=args.n_plots[0])

	import sys
	#sys.exit()
        if args.n_plots[0] != 0:
                tools.parallelize(_call_command, hadd_commands, n_processes=args.n_processes)
        if args.debug_plots:
		debug_plot_configs = []
		for output_file in output_files:
			debug_plot_configs.extend(plotconfigs.PlotConfigs().all_histograms(output_file, plot_config_template={"markers":["E"], "colors":["#FF0000"]}))
		higgsplot.HiggsPlotter(list_of_config_dicts=debug_plot_configs, list_of_args_strings=[args.args], n_processes=args.n_processes, n_plots=args.n_plots[1])
	log.debug("ARE YOU HERE?")
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
	efficiency = {}

	for datacard, cb in datacards_cbs.iteritems():
		for channel in cb.cp().analysis(["ztt"]).era(["13TeV"]).channel_set():
			nPassPre = 0
			nFailPre = 0
			sig_process = cb.cp().bin([category]).signals().process_set()
			
			for category in cb.cp().analysis(["ztt"]).era(["13TeV"]).channel([channel]).bin_set():
				if "pass" in category:
					nPassPre = uncertainties.ufloat(cb.cp().bin([category]).process(sig_process).GetRate(),
									cb.cp().bin([category]).process(sig_process).GetUncertainty())
				elif "fail" in category:
					nFailPre = uncertainties.ufloat(cb.cp().bin([category]).process(sig_process).GetRate(),
									cb.cp().bin([category]).process(sig_process).GetUncertainty())
			efficiency[channel] = nPassPre / (nPassPre + nFailPre)
                      
			command = ["text2workspace.py -m {MASS} -P {MODEL} --PO \"eff={EFF}\" {DATACARD} -o {OUTPUT}".format(
				MASS=[mass for mass in cb.mass_set() if mass != "*"][0],
				MODEL=model_settings["P"],
				EFF=efficiency[channel].nominal_value,
				DATACARD=datacard,
				OUTPUT=os.path.splitext(datacard)[0]+".root")]
			
			print "command -->", command
			tools.parallelize(_call_command, command, n_processes=args.n_processes)

		datacards_workspaces[datacard] = os.path.splitext(datacard)[0]+".root"
	
	# Max. likelihood fit and postfit plots
       
	#--expectSignal=1 --toys -1 for Asimov dataset
	datacards.combine(datacards_cbs, datacards_workspaces, None, args.n_processes, "-M MaxLikelihoodFit {STABLE} -n \"\"".format(
			STABLE=datacards.stable_options
	))
	#datacards_postfit_shapes = datacards.postfit_shapes(datacards_cbs, True, args.n_processes, "--sampling" + (" --print" if args.n_processes <= 1 else ""))
	datacards_postfit_shapes = datacards.postfit_shapes_fromworkspace(datacards_cbs, datacards_workspaces, True, args.n_processes, "--sampling" + (" --print" if args.n_processes <= 1 else ""))
	datacards.pull_plots(datacards_postfit_shapes, s_fit_only=True, plotting_args={"fit_poi" : [fit_settings['poi']]}, n_processes=args.n_processes)

	# plotting
	plot_configs = []
	plot_configs.extend(model_settings.get("fit_plots", []))
	plot_configs = [jsonTools.JsonDict(os.path.expandvars(plot_config_file)).doIncludes().doComments() for plot_config_file in plot_configs]
	
	for config in plot_configs:
		if config.get("output_dir") is None:
			config["output_dir"] = args.output_dir
		config["directories"] = [directory.format(OUTDIR=args.output_dir) for directory in config.get("directories", [])]

	# create plots using HarryPlotter
	#higgsplot.HiggsPlotter(list_of_config_dicts=plot_configs, n_processes=args.n_processes, n_plots=args.n_plots[1])
	
	# prefit-postfit plots
	plot_configs = []
	if args.model in ["etaufakerate", "mutaufakerate"]:
		bkg_plotting_order = ["ZLL", "ZL", "ZTT", "ZJ", "TT", "VV", "W", "QCD"]
	elif args.model == "tauideff":
		bkg_plotting_order = ["ZTT", "ZLL", "ZL", "ZJ", "TT", "VV", "W", "QCD"]
	
	for level in ["prefit", "postfit"]:
		if not datacards_postfit_shapes:
			continue
		for datacard in datacards_cbs.keys():
			postfit_shapes = datacards_postfit_shapes.get("fit_s", {}).get(datacard)
			nPass = 0
			nFail = 0
			for category in datacards_cbs[datacard].cp().bin_set():
				print "category = ", category
				
				results_file = ROOT.TFile(os.path.join(os.path.dirname(datacard), "mlfit.root"))
				results_tree = results_file.Get("tree_fit_sb")
				results_tree.GetEntry(0)
				bestfit = results_tree.mu
				
				bkg_process = datacards_cbs[datacard].cp().bin([category]).backgrounds().process_set()
				sig_process = datacards_cbs[datacard].cp().bin([category]).signals().process_set()
				if "pass" in category:
					nPass = uncertainties.ufloat(datacards_cbs[datacard].cp().bin([category]).process(sig_process).GetRate(),datacards_cbs[datacard].cp().bin([category]).process(sig_process).GetUncertainty())
					signal_scale = bestfit
					if level == "postfit":
						nPass = nPass * signal_scale
					print "\tNpass ({}) = {:6.0f}".format(level, nPass)
				elif "fail" in category:
					nFail = uncertainties.ufloat(datacards_cbs[datacard].cp().bin([category]).process(sig_process).GetRate(),datacards_cbs[datacard].cp().bin([category]).process(sig_process).GetUncertainty())
					effnom = efficiency[category[:2]].nominal_value
					signal_scale = (1.0 - bestfit*effnom)/(1.0 - effnom)
					if level == "postfit":
						nFail = nFail * signal_scale
					print "\tNfail ({}) = {:6.0f}".format(level, nFail)
				
				processes = bkg_process + sig_process
				processes.sort(key=lambda process: bkg_plotting_order.index(process) if process in bkg_plotting_order else len(bkg_plotting_order))

				config = {}
				config.setdefault("analysis_modules", []).extend(["SumOfHistograms"])
				config.setdefault("sum_nicks", []).append("noplot_TotalBkg noplot_TotalSig")
				config.setdefault("sum_scale_factors", []).append("1.0 1.0")
				config.setdefault("sum_result_nicks", []).append("Total")
				
				processes_to_plot = list(processes)
				if category[:2] in ["et", "mt", "tt"]:
					processes = [p.replace("ZJ","ZJ_noplot").replace("VV", "VV_noplot").replace("W", "W_noplot") for p in processes]
					processes_to_plot = [p for p in processes if not "noplot" in p]
					processes_to_plot.insert(3, "EWK")
					config["sum_nicks"].append("ZJ_noplot VV_noplot W_noplot")
					config["sum_scale_factors"].append("1.0 1.0 1.0")
					config["sum_result_nicks"].append("EWK")
				
				config["files"] = [postfit_shapes]
				config["folders"] = [category+"_"+level]
				config["nicks"] = processes + ["noplot_TotalBkg", "noplot_TotalSig", "data_obs"]
				config["x_expressions"] = [p.strip("_noplot") for p in processes] + ["TotalBkg", "TotalSig", "data_obs"]
				config["stacks"] = ["bkg"]*len(processes_to_plot) + ["data"]
				config["labels"] = [label.lower() for label in processes_to_plot + ["totalbkg"] + ["data_obs"]]
				config["colors"] = [color.lower() for color in processes_to_plot + ["#000000 transgrey"] + ["data_obs"]]
				config["markers"] = ["HIST"]*len(processes_to_plot) + ["E2"] + ["E"]
				config["legend_markers"] = ["F"]*len(processes_to_plot) + ["F"] + ["ELP"]
				config["x_label"] = "m_{vis} [GeV]" #category[:2]+"_"+args.quantity
				config["y_label"] = "Events / bin"
				if args.model in ["etaufakerate", "mutaufakerate"]:
					config["x_lims"] = [60, 120]
				elif args.model == "tauideff":
					config["x_lims"] = [35, 200]
				
				#config["title"] = "channel_"+category[:2]
				config["energies"] = [13.0]
				config["lumis"] = [float("%.1f" % args.lumi)]
				#config["cms"] = True
				#config["extra_text"] = "Preliminary"
				config["legend"] = [0.7, 0.5, 0.9, 0.78]
				config["output_dir"] = os.path.join(os.path.dirname(datacard), "plots")
				config["filename"] = level+"_"+category
				config["formats"] = ["png", "pdf"]
				
				if args.ratio:
					if not "Ratio" in config.get("analysis_modules", []):
						config.setdefault("analysis_modules", []).append("Ratio")
					config.setdefault("ratio_numerator_nicks", []).extend(["noplot_TotalBkg noplot_TotalSig", "data_obs"])
					config.setdefault("ratio_denominator_nicks", []).extend(["noplot_TotalBkg noplot_TotalSig"] * 2)
					config.setdefault("ratio_result_nicks", []).extend(["ratio_unc", "ratio"])
					config["ratio_denominator_no_errors"] = True
					config.setdefault("colors", []).extend(["#000000 transgrey", "#000000"])
					config.setdefault("markers", []).extend(["E2", "E"])
					config.setdefault("legend_markers", []).extend(["F", "ELP"])
					config.setdefault("labels", []).extend([""] * 2)
					config["legend"] = [0.65, 0.4, 0.92, 0.82]
					config["y_subplot_lims"] = [0.5, 1.5]
					config["y_subplot_label"] = "Obs./Exp."
					config["subplot_grid"] = True
				
				if "fail" in category and args.model in ["etaufakerate", "mutaufakerate"]:
					config.pop("legend")
				
				plot_configs.append(config)
			print "\tefficiency ({}) = Npass/(Npass+Nfail) = {:6.5f}".format(level, nPass/(nPass+nFail))
	
	# create plots using HarryPlotter
	higgsplot.HiggsPlotter(list_of_config_dicts=plot_configs, list_of_args_strings=[args.args], n_processes=args.n_processes, n_plots=args.n_plots[1])
