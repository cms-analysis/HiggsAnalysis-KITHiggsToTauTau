#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import argparse
import copy
import glob
import os
import shutil
import ROOT
ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit")
import CombineHarvester.CombineTools.ch as ch

import Artus.Utility.jsonTools as jsonTools

import HiggsAnalysis.KITHiggsToTauTau.plotting.higgsplot as higgsplot
import HiggsAnalysis.KITHiggsToTauTau.datacards.datacardconfigs as datacardconfigs
import HiggsAnalysis.KITHiggsToTauTau.datacards.cpstudiesdatacards as cpstudiesdatacards
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.samples_run2 as samples

def _str2bool(string):
	""" Parse string content to bool."""
	return string.lower() in ("yes", "true", "t", "1")

def poi_ranges_default(lumi):
	if lumi < 5000.0:
		return [-19.0, 21.0]
	elif lumi < 20000.0:
		return [-15.0, 16.0]
	elif lumi < 50000.0:
		return [-9.0, 11.0]
	else:
		return [-4.0, 6.0]

def poi_ranges_default_bbb(lumi):
	if lumi < 5000.0:
		return [-14.0, 16.0]
	elif lumi < 20000.0:
		return [-9.0, 11.0]
	elif lumi < 50000.0:
		return [-4.0, 6.0]
	else:
		return [-1.0, 3.0]

if __name__ == "__main__":
	
	models = {
		"default" : {
			"fit" : {
				"" : {
					"method" : "MultiDimFit",#"MaxLikelihoodFit",
					"options" : "--algo singles",
					"poi_ranges" : poi_ranges_default,
					"poi_ranges_bbb" : poi_ranges_default_bbb,
				},
			},
			"fit_plots" : {
				"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/combine/exp_best_fit_mu_over_lumi.json",
				"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/combine/exp_best_fit_mu_split_over_lumi.json",
				"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/combine/exp_best_fit_mu_unc_over_lumi.json",
				"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/combine/exp_best_fit_mu_unc_split_over_lumi.json",
			},
		},
	}
	parser = argparse.ArgumentParser(description="Make Projections of the expected limits based on existing datacards.",
	                                 parents=[logger.loggingParser])
	parser.register("type", "bool", _str2bool)
	
	parser.add_argument("-d", "--datacards", nargs="+", required=True,
	                    help="Datacards.")
	parser.add_argument("-L", "--lumi-datacards", type=float, default=samples.default_lumi,
	                    help="Integrated luminosity / pb used for the datacards. [Default: %(default)s]")
	parser.add_argument("-l", "--lumis", nargs="+", type=int, default=range(1000, 10000, 1000)+range(10000, 100000, 10000)+[100000],#+range(100000, 300001, 100000),
	                    help="Projection values for integrated luminosities / pb. [Default: %(default)s]")
	parser.add_argument("-m", "--models", nargs="+", default=["default"],
	                    choices=models.keys(),
	                    help="Statistics models. [Default: %(default)s]")
	parser.add_argument("--freeze-syst-uncs", nargs="+", type="bool", default=[False],#, True],
	                    help="Freeze systematics (needs run without freezing first). [Default: %(default)s]")
	parser.add_argument("-r", "--ratio", default=False, action="store_true",
	                    help="Add ratio subplot. [Default: %(default)s]")
	parser.add_argument("-a", "--args", default="",
	                    help="Additional Arguments for HarryPlotter. [Default: %(default)s]")
	parser.add_argument("-n", "--n-processes", type=int, default=1,
	                    help="Number of (parallel) processes. [Default: %(default)s]")
	parser.add_argument("-f", "--n-plots", type=int,
	                    help="Number of plots. [Default: all]")
	parser.add_argument("-o", "--output-dir", default=None,
	                    help="Output directory. [Default: relative to datacards]")
	parser.add_argument("--clear-output-dir", action="store_true", default=False,
	                    help="Delete/clear output directory before running this script. [Default: %(default)s]")
	parser.add_argument("--cp-mixings", nargs="+", type=float,
                        default=[mixing/100.0 for mixing in range(0, 101, 25)],
                        help="CP mixing angles alpha_tau (in units of pi/2) to be probed. [Default: %(default)s]")
	
	args = parser.parse_args()
	logger.initLogger(args)
		
	datacards_configs = datacardconfigs.DatacardConfigs()
	
	
	
	plot_configs = []
	for datacard in args.datacards:
		cb = ch.CombineHarvester()
		cb.SetFlag("workspaces-use-clone", True)
		for template in datacards_configs.htt_datacard_filename_templates:
			template_tag = template.split("$")[0]
						
			if template_tag in datacard:
				matched_template = os.path.join(datacard[:datacard.index(template_tag)], template).replace("${BIN}", "[\\w\\.]+").replace("{", "").replace("}", "")
				cb.ParseDatacard(datacard, "htt", "13TeV", "mt", 10, "*")
				break
			
		datacards = cpstudiesdatacards.CPStudiesDatacards(cb=cb)
		
		for model in args.models:
			model_settings = models.get(model, {})
			
			datacards_workspaces = {}
			for freeze_syst_uncs in args.freeze_syst_uncs:
				
				output_dir_base = args.output_dir
				if output_dir_base is None:
					output_dir_base = os.path.splitext(datacard)[0]
				sub_dir_base = os.path.join("projection", model, "statUnc" if freeze_syst_uncs else "totUnc")
				output_dir_base = os.path.abspath(os.path.expandvars(os.path.join(output_dir_base, sub_dir_base)))
				
				if args.clear_output_dir and os.path.exists(output_dir_base):
					logger.subprocessCall("rm -r " + output_dir_base, shell=True)				
				
				# scale datacards
				datacards_cbs = {}
				datacards_poi_ranges = {}
				for lumi in args.lumis:
					output_dir = os.path.join(output_dir_base, "{:06}".format(lumi))
					if not os.path.exists(output_dir):
						os.makedirs(output_dir)
					
					scaled_datacards = cpstudiesdatacards.CPStudiesDatacards(cb=datacards.cb.deep())
					
					lumi_scale_factor = lumi / args.lumi_datacards
					scaled_datacards.scale_expectation(lumi_scale_factor)
					#scaled_datacards.replace_observation_by_asimov_dataset("125")
					scaled_datacards.cb.PrintAll()
					print output_dir
					print os.path.basename(datacard)
					print os.path.splitext(os.path.basename(datacard))[0]+"_input.root"
					scaled_datacards_cbs = scaled_datacards.write_datacards(
							os.path.basename(datacard),
							os.path.splitext(os.path.basename(datacard))[0]+"_input.root",
							output_dir
					)#TODO HIER STÜRZT PROGG AB
					#datacards_workspaces = datacards.text2workspace(datacards_cbs, n_processes=args.n_processes)
					datacards_cbs.update(scaled_datacards_cbs)
					for scaled_datacard, cb in scaled_datacards_cbs.iteritems():
						for fit_name, fit_settings in model_settings.get("fit", {"" : {}}).iteritems():
							if freeze_syst_uncs and (("CVCF" in fit_name) or ("RVRF" in fit_name)):
								continue #TODO syst errors
				if not freeze_syst_uncs:
					datacards_workspaces = datacards.text2workspace(datacards_cbs, args.n_processes)
					
					#continue
				json_configs = []
				
				
				# fits
				for fit_name, fit_options in model_settings.get("fit", {}).iteritems():
					tmp_datacards_workspaces = datacards_workspaces[fit_name] if freeze_syst_uncs else datacards_workspaces
					stable_combine_options = "--robustFit=1 --preFitValue=1. --X-rtd FITTER_NEW_CROSSING_ALGO --minimizerAlgoForMinos=Minuit2 --minimizerToleranceForMinos=0.1 --X-rtd FITTER_NEVER_GIVE_UP --X-rtd FITTER_BOUND --minimizerAlgo=Minuit2 --minimizerStrategy=0 --minimizerTolerance=0.1 --cminFallbackAlgo \"Minuit2,0:1.\""
	
					datacards.combine(
							datacards_cbs,
							datacards_workspaces,
							None,
							args.n_processes,
							"-M MaxLikelihoodFit --redefineSignalPOIs cpmixing --expectSignal=1 -t -1 --setPhysicsModelParameters cpmixing=0.0 {stable} -n \"\"".format(stable=stable_combine_options)
					)
					
					datacards_postfit_shapes = datacards.postfit_shapes_fromworkspace(datacards_cbs, datacards_workspaces, False, args.n_processes, "--sampling" + (" --print" if args.n_processes <= 1 else ""))
					datacards.prefit_postfit_plots(datacards_cbs, datacards_postfit_shapes, plotting_args={"ratio" : args.ratio, "args" : args.args, "x_expressions" : "genPhiStarCP"}, n_processes=args.n_processes)
					
					datacards.pull_plots(datacards_postfit_shapes, s_fit_only=False, plotting_args={"fit_poi" : ["cpmixing"], "formats" : ["pdf", "png"]}, n_processes=args.n_processes)
					datacards.print_pulls(datacards_cbs, args.n_processes, "-A -p {POI}".format(POI="cpmixing"))
				
					datacards.combine(
							datacards_cbs,
							datacards_workspaces,
							None,
							args.n_processes,
							"-M MultiDimFit --algo grid --redefineSignalPOIs cpmixing --expectSignal=1 -t -1 --setPhysicsModelParameters cpmixing=0.0 --setPhysicsModelParameterRanges cpmixing={RANGE} --points {POINTS} {STABLE} -n \"\"".format(
									STABLE=stable_combine_options,
									RANGE="{0:f},{1:f}".format(args.cp_mixings[0]-(args.cp_mixings[1]-args.cp_mixings[0])/2.0, args.cp_mixings[-1]+(args.cp_mixings[-1]-args.cp_mixings[-2])/2.0),
									POINTS=len(args.cp_mixings)
							)
					)
					
				datacards.annotate_trees(tmp_datacards_workspaces, "higgsCombine*{method}*mH*.root".format(method=fit_options.get("method", "MultiDimFit")), os.path.join(sub_dir_base, "(\d*)/.*.root"), None, args.n_processes, "-t limit -b lumi")
				#datacards.annotate_trees(tmp_datacards_workspaces, "higgsCombine*{method}*mH*.root".format(method=fit_options.get("method", "MaxLikelihoodFit")), os.path.join(sub_dir_base, "(\d*)/.*.root"), None, args.n_processes, "-t limit -b lumi")
				plot_configs=[]
				config={
					"folders": [
    					"limit"
    	     			],
					"files": [
						"plots/htt_datacards/datacards/individual/mt_CP_mt/htt_mt_10_13TeV/projection/default/totUnc/*/higgsCombine.MultiDimFit.mH*.root"
						],
					"filename": "lumivscpmixing_normal",
					"x_bins":["1 2 3 4 5 6 7 8 9 10 20 30 40 50 60 70 80 90 100 101"],
					"y_bins":["20,0,1.01"],
					"x_expressions":"lumi/1000",
					"y_expressions":"cpmixing",
					"weights": "deltaNLL",
					"markers": "COLZ",
					"z_label": "deltaNLL"						
						}
				plot_configs.append(config)
		
	if log.isEnabledFor(logging.DEBUG):
		import pprint
		pprint.pprint(plot_configs)
	
	higgsplot.HiggsPlotter(list_of_config_dicts=plot_configs, list_of_args_strings=[args.args], n_processes=args.n_processes, n_plots=args.n_plots)

