#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import argparse
import copy
import os

import combineharvester as ch

import Artus.Utility.jsonTools as jsonTools

import HiggsAnalysis.KITHiggsToTauTau.plotting.higgsplot as higgsplot
import HiggsAnalysis.KITHiggsToTauTau.datacards.datacardconfigs as datacardconfigs
import HiggsAnalysis.KITHiggsToTauTau.datacards.smhttdatacards as smhttdatacards


if __name__ == "__main__":

	parser = argparse.ArgumentParser(description="Make Projections of the expected limits based on existing datacards.",
	                                 parents=[logger.loggingParser])

	parser.add_argument("-d", "--datacards", nargs="+", required=True,
	                    help="Datacards.")
	parser.add_argument("-L", "--lumi-datacards", type=float, default=40.03,
	                    help="Integrated luminosity / pb used for the datacards. [Default: %(default)s]")
	parser.add_argument("-l", "--lumis", nargs="+", type=int, default=[1000, 5000, 10000, 15000, 20000, 25000],
	                    help="Projection values for integrated luminosities / pb.")
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
	
	args = parser.parse_args()
	logger.initLogger(args)
	
	datacards_configs = datacardconfigs.DatacardConfigs()
	
	for datacard in args.datacards:
		cb = ch.CombineHarvester()
		
		for template in datacards_configs.htt_datacard_filename_templates:
			template = template.replace("${BIN}", "[\\w\\.]+")
			template_tag = template.split("$")[0]
			if template_tag in datacard:
				matched_template = os.path.join(datacard[:datacard.index(template_tag)], template).replace("{", "").replace("}", "")
				cb.QuickParseDatacard(datacard, matched_template)
				break
		
		datacards = smhttdatacards.SMHttDatacards(cb=cb)
		
		for freeze_syst_uncs in [False, True]:
			
			output_dir_base = args.output_dir
			if output_dir_base is None:
				output_dir_base = os.path.join(os.path.splitext(datacard)[0], "projection/defaultModel", "statUnc" if freeze_syst_uncs else "totUnc")
			output_dir_base = os.path.abspath(os.path.expandvars(output_dir_base))
			
			if args.clear_output_dir and os.path.exists(output_dir_base):
				logger.subprocessCall("rm -r " + output_dir_base, shell=True)
			
			# scale datacards
			datacards_cbs = {}
			for lumi in args.lumis:
				output_dir = os.path.join(output_dir_base, "{:06}".format(lumi))
				if not os.path.exists(output_dir):
					os.makedirs(output_dir)
			
				scaled_datacards = smhttdatacards.SMHttDatacards(cb=datacards.cb.deep())
				
				lumi_scale_factor = lumi / args.lumi_datacards
				scaled_datacards.scale_expectation(lumi_scale_factor)
				#scaled_datacards.replace_observation_by_asimov_dataset("125")
				
				datacards_cbs.update(scaled_datacards.write_datacards(
						os.path.basename(datacard),
						os.path.splitext(os.path.basename(datacard))[0]+"_input.root",
						output_dir
				))
				
				if freeze_syst_uncs:
					logger.subprocessCall("cp {src} {dst}".format(
							src=os.path.join(output_dir.replace("projection/defaultModel/statUnc", "projection/defaultModel/totUnc"), "higgsCombine*MultiDimFit*mH*.root"),
							dst=os.path.join(output_dir, "workspacePlusSnapshot.root")
					), shell=True)
			
			datacards_workspaces = datacards.text2workspace(datacards_cbs, n_processes=args.n_processes)
			if freeze_syst_uncs:
				datacards_workspaces = {datacard : workspace.replace(os.path.splitext(os.path.basename(datacard))[0]+".root", "workspacePlusSnapshot.root") for datacard, workspace in datacards_workspaces.iteritems()}
			
			json_configs = []
			
			stable_options = "--robustFit=1 --preFitValue=1. --X-rtd FITTER_NEW_CROSSING_ALGO --minimizerAlgoForMinos=Minuit2 --minimizerToleranceForMinos=0.1 --X-rtd FITTER_NEVER_GIVE_UP --X-rtd FITTER_BOUND --minimizerAlgo=Minuit2 --minimizerStrategy=0 --minimizerTolerance=0.1 --cminFallbackAlgo \"Minuit2,0:1.\""
			
			# Multi-dimensional fit (in 1D)
			datacards.combine(datacards_cbs, datacards_workspaces, args.n_processes, "-t -1 --expectSignal 1 -M MultiDimFit --algo singles {freeze} {stable} -n \"\"".format(
					freeze="--snapshotName MultiDimFit -S 0" if freeze_syst_uncs else "--saveWorkspace",
					stable=stable_options
			))
			datacards.annotate_trees(datacards_workspaces, "higgsCombine*MultiDimFit*mH*.root", "projection/defaultModel/.*Unc/(\d*)/.*.root", args.n_processes, "-t limit -b lumi")
			
			json_configs.extend([
				"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/combine/exp_best_fit_mu_over_lumi.json",
				"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/combine/exp_best_fit_mu_unc_over_lumi.json",
			])
			
			if not freeze_syst_uncs:
			
				# Max. likelihood fit and postfit plots
				datacards.combine(datacards_cbs, datacards_workspaces, args.n_processes, "-t -1 --expectSignal 1 -M MaxLikelihoodFit {stable} -n \"\"".format(stable=stable_options))
				datacards_postfit_shapes = datacards.postfit_shapes(datacards_cbs, False, args.n_processes, "--sampling" + (" --print" if args.n_processes <= 1 else ""))
				#datacards.prefit_postfit_plots(datacards_cbs, datacards_postfit_shapes, plotting_args={"ratio" : args.ratio, "args" : args.args}, n_processes=args.n_processes)
				datacards.pull_plots(datacards_postfit_shapes, s_fit_only=False, plotting_args={"fit_poi" : ["r"], "formats" : ["pdf", "png"]}, n_processes=args.n_processes)
				datacards.print_pulls(datacards_cbs, args.n_processes, "-A -p {POI}".format(POI="r"))
				datacards.annotate_trees(datacards_workspaces, "higgsCombine*MaxLikelihoodFit*mH*.root", "projection/defaultModel/.*Unc/(\d*)/.*.root", args.n_processes, "-t limit -b lumi")
				
				# Asymptotic limits
				datacards.combine(datacards_cbs, datacards_workspaces, args.n_processes, "-t -1 --expectSignal 1 -M Asymptotic -n \"\"")
				datacards.annotate_trees(datacards_workspaces, "higgsCombine*Asymptotic*mH*.root", "projection/defaultModel/.*Unc/(\d*)/.*.root", args.n_processes, "-t limit -b lumi")
				json_configs.extend([
					"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/combine/exp_limit_over_lumi.json",
					"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/combine/exp_limit_unc_over_lumi.json",
					"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/combine/exp_obs_limit_over_lumi.json",
				])
		
				# Significances/p-values
				datacards.combine(datacards_cbs, datacards_workspaces, args.n_processes, "-t -1 --expectSignal 1 --toysFreq -M ProfileLikelihood --significance --pvalue -n \"\"")
				datacards.annotate_trees(datacards_workspaces, "higgsCombine*ProfileLikelihood*mH125*.root", "projection/defaultModel/.*Unc/(\d*)/.*.root", args.n_processes, "-t limit -b lumi")
				json_configs.extend([
					"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/combine/exp_pvalue_over_lumi.json",
				])
		
			plot_configs = []
			json_configs = [jsonTools.JsonDict(os.path.expandvars(json_config_file)).doIncludes().doComments() for json_config_file in json_configs]
			for config in json_configs:
				config["directories"] = os.path.join(output_dir_base, "*")
				config["x_expressions"] = [x.replace("lumi", "(lumi/1000.0)") for x in config.get("x_expressions", [])]
			
				if not config.get("labels", None) is None:
					config["legend"] = [0.45, 0.88-(len(config["labels"])*0.05), 0.9, 0.88]
			
				if "pvalue" in config.get("filename", ""):
					config["x_lims"] = [min(args.lumis)/1000.0, max(args.lumis)/1000.0]
			
				config["output_dir"] = os.path.join(output_dir_base, "plots")
		
				plot_configs.append(config)
		
			if log.isEnabledFor(logging.DEBUG):
				import pprint
				pprint.pprint(plot_configs)
		
			higgsplot.HiggsPlotter(list_of_config_dicts=plot_configs, list_of_args_strings=[args.args], n_processes=args.n_processes, n_plots=args.n_plots)

