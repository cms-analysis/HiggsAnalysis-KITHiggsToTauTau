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

import combineharvester as ch

import Artus.Utility.jsonTools as jsonTools

import HiggsAnalysis.KITHiggsToTauTau.plotting.higgsplot as higgsplot
import HiggsAnalysis.KITHiggsToTauTau.datacards.datacardconfigs as datacardconfigs
import HiggsAnalysis.KITHiggsToTauTau.datacards.smhttdatacards as smhttdatacards


def _str2bool(string):
	""" Parse string content to bool."""
	return string.lower() in ("yes", "true", "t", "1")


def poi_ranges_default(lumi):
	if lumi < 10000.0:
		return [-20.0, 20.0]
	elif lumi < 100000.0:
		return [-15.0, 15.0]
	else:
		return [-10.0, 10.0]


if __name__ == "__main__":
	
	models = {
		"default" : {
			"MultiDimFit" : {
				"" : {
					"options" : "--algo singles",
					"poi_ranges" : poi_ranges_default,
				},
			},
			"MultiDimFit_plots" : {
				"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/combine/exp_best_fit_mu_over_lumi.json",
				"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/combine/exp_best_fit_mu_unc_over_lumi.json",
			},
		},
		"cvcf" : {
			"P" : "HiggsAnalysis.CombinedLimit.HiggsCouplings:cVcF",
			"PO" : [
				"cVRange={CV_MIN}:{CV_MAX}",
				"cFRange={CF_MIN}:{CF_MAX}",
			],
			"MultiDimFit" : {
				"CV" : {
					"options" : "--algo singles -P CV --floatOtherPOIs 1",
					"poi_ranges" : poi_ranges_default,
				},
				"CF" : {
					"options" : "--algo singles -P CF --floatOtherPOIs 1",
					"poi_ranges" : poi_ranges_default,
				},
				"CVCF" : {
					"options" : "--algo grid --points {CVCF_BINS}",
				},
			},
			"MultiDimFit_plots" : {
				"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/combine/exp_best_fit_cv_over_lumi.json",
				"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/combine/exp_best_fit_cv_unc_over_lumi.json",
				"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/combine/exp_best_fit_cf_over_lumi.json",
				"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/combine/exp_best_fit_cf_unc_over_lumi.json",
			},
		},
		"rvrf" : {
			"P" : "HiggsAnalysis.CombinedLimit.PhysicsModel:rVrFXSHiggs",
			"MultiDimFit" : {
				"RV" : {
					"options" : "--algo singles -P RV --floatOtherPOIs 1",
					"poi_ranges" : poi_ranges_default,
				},
				"RF" : {
					"options" : "--algo singles -P RF --floatOtherPOIs 1",
					"poi_ranges" : poi_ranges_default,
				},
				"RVRF" : {
					"options" : "--algo grid --points {RVRF_BINS}",
				},
			},
			"MultiDimFit_plots" : {
				"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/combine/exp_best_fit_rv_over_lumi.json",
				"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/combine/exp_best_fit_rv_unc_over_lumi.json",
				"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/combine/exp_best_fit_rf_over_lumi.json",
				"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/combine/exp_best_fit_rf_unc_over_lumi.json",
			},
		},
	}
	
	parser = argparse.ArgumentParser(description="Make Projections of the expected limits based on existing datacards.",
	                                 parents=[logger.loggingParser])
	parser.register("type", "bool", _str2bool)
	
	parser.add_argument("-d", "--datacards", nargs="+", required=True,
	                    help="Datacards.")
	parser.add_argument("-L", "--lumi-datacards", type=float, default=40.03,
	                    help="Integrated luminosity / pb used for the datacards. [Default: %(default)s]")
	parser.add_argument("-l", "--lumis", nargs="+", type=int, default=[1000, 5000, 10000, 15000, 20000, 25000],
	                    help="Projection values for integrated luminosities / pb.")
	parser.add_argument("-m", "--models", nargs="+", default=["default"],
	                    choices=models.keys(),
	                    help="Statistics models. [Default: %(default)s]")
	parser.add_argument("--cv-bins", default="30,0.0,3.0",
	                    help="Binning of the grid for the cV axis. [Default: %(default)s]")
	parser.add_argument("--cf-bins", default="30,0.0,2.0",
	                    help="Binning of the grid for the cF axis. [Default: %(default)s]")
	parser.add_argument("--rvrf-bins", type=int, default=900,
	                    help="Number of points for the RV-RF scan. [Default: %(default)s]")
	parser.add_argument("--freeze-syst-uncs", nargs="+", type="bool", default=[False, True],
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
	
	args = parser.parse_args()
	logger.initLogger(args)
	
	args.cv_bins = [float(b) for b in args.cv_bins.split(",")]
	args.cf_bins = [float(b) for b in args.cf_bins.split(",")]
	assert args.cv_bins[0] == args.cf_bins[0]
	
	args.freeze_syst_uncs = sorted(list(set(args.freeze_syst_uncs)), key=lambda b: b)
	
	datacards_configs = datacardconfigs.DatacardConfigs()
	
	plot_configs = []
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
					
					scaled_datacards = smhttdatacards.SMHttDatacards(cb=datacards.cb.deep())
					
					lumi_scale_factor = lumi / args.lumi_datacards
					scaled_datacards.scale_expectation(lumi_scale_factor)
					#scaled_datacards.replace_observation_by_asimov_dataset("125")
					
					scaled_datacards_cbs = scaled_datacards.write_datacards(
							os.path.basename(datacard),
							os.path.splitext(os.path.basename(datacard))[0]+"_input.root",
							output_dir
					)
					datacards_cbs.update(scaled_datacards_cbs)
					for scaled_datacard, cb in scaled_datacards_cbs.iteritems():
						for multidimfit_name, multidimfit_settings in model_settings.get("MultiDimFit", {"" : {}}).iteritems():
							poi_ranges = multidimfit_settings.get("poi_ranges", None)
							if not poi_ranges is None:
								datacards_poi_ranges.setdefault(multidimfit_name, {})[scaled_datacard] = poi_ranges(lumi)
							
							if freeze_syst_uncs:
								srcs = os.path.join(
										output_dir.replace(sub_dir_base, sub_dir_base.replace("statUnc", "totUnc")),
										"higgsCombine{name}.MultiDimFit*mH*.root".format(name=multidimfit_name)
								)
								for src in glob.glob(srcs):
									dst = src.replace(sub_dir_base.replace("statUnc", "totUnc"), sub_dir_base).replace("higgsCombine", "workspaceSnapshot")
									shutil.copyfile(src, dst)
									datacards_workspaces.setdefault(multidimfit_name, {})[scaled_datacard] = dst
				
				text2workspace_args = []
				if "P" in model_settings:
					text2workspace_args.append("-P \"{P}\"".format(P=model_settings["P"]))
				for physics_option in model_settings.get("PO", []):
					tmp_physics_option = copy.deepcopy(physics_option)
					if "CV_M" in tmp_physics_option:
						tmp_physics_option = tmp_physics_option.format(CV_MIN=args.cv_bins[1], CV_MAX=args.cv_bins[2])
					if "CF_M" in tmp_physics_option:
						tmp_physics_option = tmp_physics_option.format(CF_MIN=args.cf_bins[1], CF_MAX=args.cf_bins[2])
					
					text2workspace_args.append("--PO \"{PO}\"".format(PO=tmp_physics_option))
				
				if not freeze_syst_uncs:
					datacards_workspaces = datacards.text2workspace(datacards_cbs, args.n_processes, *text2workspace_args)
				
				json_configs = []
				
				stable_options = "--robustFit=1 --preFitValue=1. --X-rtd FITTER_NEW_CROSSING_ALGO --minimizerAlgoForMinos=Minuit2 --minimizerToleranceForMinos=0.1 --X-rtd FITTER_NEVER_GIVE_UP --X-rtd FITTER_BOUND --minimizerAlgo=Minuit2 --minimizerStrategy=0 --minimizerTolerance=0.1 --cminFallbackAlgo \"Minuit2,0:1.\""
				
				# Multi-dimensional fits
				for multidimfit_name, multidimfit_options in model_settings.get("MultiDimFit", {"" : ""}).iteritems():
					print freeze_syst_uncs
					print datacards_workspaces.keys()
					tmp_datacards_workspaces = datacards_workspaces[multidimfit_name] if freeze_syst_uncs else datacards_workspaces
					
					tmp_multidimfit_options = copy.deepcopy(multidimfit_options.get("options", ""))
					if "CVCF_BINS" in tmp_multidimfit_options:
						tmp_multidimfit_options = tmp_multidimfit_options.format(CVCF_BINS=int(args.cv_bins[0] * args.cf_bins[0]))
					if "RVRF_BINS" in tmp_multidimfit_options:
						tmp_multidimfit_options = tmp_multidimfit_options.format(RVRF_BINS=args.rvrf_bins)
					
					datacards.combine(datacards_cbs, tmp_datacards_workspaces, datacards_poi_ranges.get(multidimfit_name, None), args.n_processes, "-t -1 --expectSignal 1 -M MultiDimFit {multidimfit_options} {freeze} {stable} -n {name}".format(
							multidimfit_options=tmp_multidimfit_options,
							freeze="--snapshotName MultiDimFit -S 0" if freeze_syst_uncs else "--saveWorkspace",
							stable=stable_options,
							name="\"\"" if multidimfit_name == "" else multidimfit_name
					))
				datacards.annotate_trees(tmp_datacards_workspaces, "higgsCombine*MultiDimFit*mH*.root", os.path.join(sub_dir_base, "(\d*)/.*.root"), None, args.n_processes, "-t limit -b lumi")
				
				json_configs.extend(model_settings.get("MultiDimFit_plots", []))
				
				if (not freeze_syst_uncs) and (model == "default"):
					
					# Max. likelihood fit and postfit plots
					datacards.combine(datacards_cbs, datacards_workspaces, None, args.n_processes, "-t -1 --expectSignal 1 -M MaxLikelihoodFit {stable} -n \"\"".format(stable=stable_options))
					datacards_postfit_shapes = datacards.postfit_shapes(datacards_cbs, False, args.n_processes, "--sampling" + (" --print" if args.n_processes <= 1 else ""))
					datacards.prefit_postfit_plots(datacards_cbs, datacards_postfit_shapes, plotting_args={"ratio" : args.ratio, "args" : args.args}, n_processes=args.n_processes)
					datacards.pull_plots(datacards_postfit_shapes, s_fit_only=False, plotting_args={"fit_poi" : ["r"], "formats" : ["pdf", "png"]}, n_processes=args.n_processes)
					datacards.print_pulls(datacards_cbs, args.n_processes, "-A -p {POI}".format(POI="r"))
					datacards.annotate_trees(datacards_workspaces, "higgsCombine*MaxLikelihoodFit*mH*.root", os.path.join(sub_dir_base, "(\d*)/.*.root"), None, args.n_processes, "-t limit -b lumi")
					
					# Asymptotic limits
					datacards.combine(datacards_cbs, datacards_workspaces, None, args.n_processes, "-t -1 --expectSignal 1 -M Asymptotic -n \"\"")
					datacards.annotate_trees(datacards_workspaces, "higgsCombine*Asymptotic*mH*.root", os.path.join(sub_dir_base, "(\d*)/.*.root"), None, args.n_processes, "-t limit -b lumi")
					json_configs.extend([
						"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/combine/exp_limit_over_lumi.json",
						"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/combine/exp_limit_unc_over_lumi.json",
						"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/combine/exp_obs_limit_over_lumi.json",
					])
					
					# Significances/p-values
					datacards.combine(datacards_cbs, datacards_workspaces, None, args.n_processes, "-t -1 --expectSignal 1 --toysFreq -M ProfileLikelihood --significance --pvalue -n \"\"")
					datacards.annotate_trees(datacards_workspaces, "higgsCombine*ProfileLikelihood*mH125*.root", os.path.join(sub_dir_base, "(\d*)/.*.root"), None, args.n_processes, "-t limit -b lumi")
					json_configs.extend([
						"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/combine/exp_pvalue_over_lumi.json",
					])
				
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

