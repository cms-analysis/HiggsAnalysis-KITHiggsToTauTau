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
	if lumi < 5000.0:
		return [-24.0, 26.0]
	elif lumi < 20000.0:
		return [-9.0, 11.0]
	elif lumi < 50000.0:
		return [-4.0, 6.0]
	else:
		return [-1.0, 3.0]

def poi_ranges_default_bbb(lumi):
	if lumi < 5000.0:
		return [-24.0, 26.0]
	elif lumi < 20000.0:
		return [-14.0, 16.0]
	elif lumi < 50000.0:
		return [-9.0, 11.0]
	else:
		return [-4.0, 6.0]

def poi_ranges_fermion(lumi):
	if lumi < 5000.0:
		return [-19.0, 21.0]
	elif lumi < 20000.0:
		return [-14.0, 16.0]
	elif lumi < 50000.0:
		return [-9.0, 11.0]
	else:
		return [-4.0, 6.0]

def poi_ranges_fermion_bbb(lumi):
	if lumi < 5000.0:
		return [-19.0, 21.0]
	elif lumi < 20000.0:
		return [-14.0, 16.0]
	elif lumi < 50000.0:
		return [-9.0, 11.0]
	else:
		return [-4.0, 6.0]

def poi_ranges_vector(lumi):
	if lumi < 5000.0:
		return [-24.0, 26.0]
	elif lumi < 20000.0:
		return [-9.0, 11.0]
	elif lumi < 50000.0:
		return [-4.0, 6.0]
	else:
		return [-1.0, 3.0]

def poi_ranges_vector_bbb(lumi):
	if lumi < 5000.0:
		return [-24.0, 26.0]
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
		"cvcf" : {
			"P" : "HiggsAnalysis.CombinedLimit.HiggsCouplings:cVcF",
			"PO" : [
				"cVRange={CV_MIN}:{CV_MAX}",
				"cFRange={CF_MIN}:{CF_MAX}",
			],
			"fit" : {
				"CV" : {
					"method" : "MultiDimFit",
					"options" : "--algo singles -P CV --floatOtherPOIs 1 --setPhysicsModelParameterRanges \"CV={RMIN},{RMAX}:CF={RMIN},{RMAX}\"",
					"poi_ranges" : poi_ranges_vector,
					"poi_ranges_bbb" : poi_ranges_vector_bbb,
				},
				"CF" : {
					"method" : "MultiDimFit",
					"options" : "--algo singles -P CF --floatOtherPOIs 1 --setPhysicsModelParameterRanges \"CV={RMIN},{RMAX}:CF={RMIN},{RMAX}\"",
					"poi_ranges" : poi_ranges_fermion,
					"poi_ranges_bbb" : poi_ranges_fermion_bbb,
				},
				"CVCF" : {
					"method" : "MultiDimFit",
					"options" : "--algo grid --points {CVCF_BINS} --setPhysicsModelParameterRanges \"CV={CV_MIN},{CV_MAX}:CF={CF_MIN},{CF_MAX}\"",
					"plots_per_lumi" : [
						"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/combine/cv_cf_scan.json",
					],
				},
			},
			"fit_plots" : {
				"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/combine/exp_best_fit_cv_over_lumi.json",
				"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/combine/exp_best_fit_cv_split_over_lumi.json",
				"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/combine/exp_best_fit_cv_unc_over_lumi.json",
				"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/combine/exp_best_fit_cv_unc_split_over_lumi.json",
				"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/combine/exp_best_fit_cf_over_lumi.json",
				"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/combine/exp_best_fit_cf_split_over_lumi.json",
				"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/combine/exp_best_fit_cf_unc_over_lumi.json",
				"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/combine/exp_best_fit_cf_unc_split_over_lumi.json",
			},
		},
		"rvrf" : {
			"P" : "HiggsAnalysis.CombinedLimit.PhysicsModel:rVrFXSHiggs",
			"PO" : [
				"rVRange={RV_MIN}:{RV_MAX}",
				"rFRange={RF_MIN}:{RF_MAX}",
			],
			"fit" : {
				"RV" : {
					"method" : "MultiDimFit",
					"options" : "--algo singles -P RV --floatOtherPOIs 1 --setPhysicsModelParameterRanges \"RV={RMIN},{RMAX}:RF={RMIN},{RMAX}\"",
					"poi_ranges" : poi_ranges_vector,
					"poi_ranges_bbb" : poi_ranges_vector_bbb,
				},
				"RF" : {
					"method" : "MultiDimFit",
					"options" : "--algo singles -P RF --floatOtherPOIs 1 --setPhysicsModelParameterRanges \"RV={RMIN},{RMAX}:RF={RMIN},{RMAX}\"",
					"poi_ranges" : poi_ranges_fermion,
					"poi_ranges_bbb" : poi_ranges_fermion_bbb,
				},
				"RVRF" : {
					"method" : "MultiDimFit",
					"options" : "--algo grid --points {RVRF_BINS} --setPhysicsModelParameterRanges \"RV={RV_MIN},{RV_MAX}:RF={RF_MIN},{RF_MAX}\"",
					"plots_per_lumi" : [
						"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/combine/rv_rf_scan.json",
					],
				},
			},
			"fit_plots" : {
				"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/combine/exp_best_fit_rv_over_lumi.json",
				"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/combine/exp_best_fit_rv_split_over_lumi.json",
				"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/combine/exp_best_fit_rv_unc_over_lumi.json",
				"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/combine/exp_best_fit_rv_unc_split_over_lumi.json",
				"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/combine/exp_best_fit_rf_over_lumi.json",
				"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/combine/exp_best_fit_rf_split_over_lumi.json",
				"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/combine/exp_best_fit_rf_unc_over_lumi.json",
				"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/combine/exp_best_fit_rf_unc_split_over_lumi.json",
			},
		},
	}
	
	parser = argparse.ArgumentParser(description="Make Projections of the expected limits based on existing datacards.",
	                                 parents=[logger.loggingParser])
	parser.register("type", "bool", _str2bool)
	
	parser.add_argument("-d", "--datacards", nargs="+", required=True,
	                    help="Datacards.")
	parser.add_argument("-L", "--lumi-datacards", type=float, default=71.52,
	                    help="Integrated luminosity / pb used for the datacards. [Default: %(default)s]")
	parser.add_argument("-l", "--lumis", nargs="+", type=int, default=range(1000, 10000, 1000)+range(10000, 100000, 10000)+[100000],#+range(100000, 300001, 100000),
	                    help="Projection values for integrated luminosities / pb. [Default: %(default)s]")
	parser.add_argument("-m", "--models", nargs="+", default=["default"],
	                    choices=models.keys(),
	                    help="Statistics models. [Default: %(default)s]")
	parser.add_argument("--with-bbb-uncs", action="store_true", default=False,
	                    help="Indicate whether the datacard(s) contain bin-by-bin uncertainties, which is important for the POI ranges. [Default: %(default)s]")
	parser.add_argument("--cv-bins", default="30,0.0,3.0",
	                    help="Binning of the grid for the cV axis. [Default: %(default)s]")
	parser.add_argument("--cf-bins", default="30,0.0,2.0",
	                    help="Binning of the grid for the cF axis. [Default: %(default)s]")
	parser.add_argument("--rv-bins", default="30,-3.0,5.0",
	                    help="Binning of the grid for the rV axis. [Default: %(default)s]")
	parser.add_argument("--rf-bins", default="30,-2.0,4.0",
	                    help="Binning of the grid for the rF axis. [Default: %(default)s]")
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
	
	cv_bins = [float(b) for b in args.cv_bins.split(",")]
	cf_bins = [float(b) for b in args.cf_bins.split(",")]
	assert cv_bins[0] == cf_bins[0]
	
	rv_bins = [float(b) for b in args.rv_bins.split(",")]
	rf_bins = [float(b) for b in args.rf_bins.split(",")]
	assert rv_bins[0] == rf_bins[0]
	
	args.freeze_syst_uncs = sorted(list(set(args.freeze_syst_uncs)), key=lambda b: b)
	
	datacards_configs = datacardconfigs.DatacardConfigs()
	
	plot_configs = []
	for datacard in args.datacards:
		cb = ch.CombineHarvester()
		
		for template in datacards_configs.htt_datacard_filename_templates:
			template_tag = template.split("$")[0]
			if template_tag in datacard:
				matched_template = os.path.join(datacard[:datacard.index(template_tag)], template).replace("${BIN}", "[\\w\\.]+").replace("{", "").replace("}", "")
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
						for fit_name, fit_settings in model_settings.get("fit", {"" : {}}).iteritems():
							if freeze_syst_uncs and (("CVCF" in fit_name) or ("RVRF" in fit_name)):
								continue
							
							poi_ranges = fit_settings.get("poi_ranges"+("_bbb" if args.with_bbb_uncs else ""), None)
							if not poi_ranges is None:
								datacards_poi_ranges.setdefault(fit_name, {})[scaled_datacard] = poi_ranges(lumi)
							
							json_configs = [jsonTools.JsonDict(os.path.expandvars(json_config_file)).doIncludes().doComments() for json_config_file in fit_settings.get("plots_per_lumi", [])]
							for config in json_configs:
								config["directories"] = output_dir
								if "CVCF" in fit_name:
									config["x_bins"] = args.cv_bins
									config["y_bins"] = args.cf_bins
								if "RVRF" in fit_name:
									config["x_bins"] = args.rv_bins
									config["y_bins"] = args.rf_bins
								config["lumis"] = [lumi]
								config["output_dir"] = os.path.join(output_dir, "plots")
								plot_configs.append(config)
							
							if freeze_syst_uncs:
								srcs = os.path.join(
										output_dir.replace(sub_dir_base, sub_dir_base.replace("statUnc", "totUnc")),
										"higgsCombine{name}.{method}*mH*.root".format(name=fit_name, method=fit_settings.get("method", "MaxLikelihoodFit"))
								)
								for src in glob.glob(srcs):
									dst = src.replace(sub_dir_base.replace("statUnc", "totUnc"), sub_dir_base).replace("higgsCombine", "workspaceSnapshot")
									shutil.copyfile(src, dst)
									datacards_workspaces.setdefault(fit_name, {})[scaled_datacard] = dst
				
				text2workspace_args = []
				if "P" in model_settings:
					text2workspace_args.append("-P \"{P}\"".format(P=model_settings["P"]))
				for physics_option in model_settings.get("PO", []):
					tmp_physics_option = physics_option.format(
							CV_MIN=cv_bins[1],
							CV_MAX=cv_bins[2],
							CF_MIN=cf_bins[1],
							CF_MAX=cf_bins[2],
							RV_MIN=rv_bins[1],
							RV_MAX=rv_bins[2],
							RF_MIN=rf_bins[1],
							RF_MAX=rf_bins[2]
					)
					
					text2workspace_args.append("--PO \"{PO}\"".format(PO=tmp_physics_option))
				
				if not freeze_syst_uncs:
					datacards_workspaces = datacards.text2workspace(datacards_cbs, args.n_processes, *text2workspace_args)
				
				json_configs = []
				
				stable_options = "--robustFit=1 --preFitValue=1. --X-rtd FITTER_NEW_CROSSING_ALGO --minimizerAlgoForMinos=Minuit2 --minimizerToleranceForMinos=0.1 --X-rtd FITTER_NEVER_GIVE_UP --X-rtd FITTER_BOUND --minimizerAlgo=Minuit2 --minimizerStrategy=0 --minimizerTolerance=0.1 --cminFallbackAlgo \"Minuit2,0:1.\""
				
				# fits
				for fit_name, fit_options in model_settings.get("fit", {}).iteritems():
					if freeze_syst_uncs and (("CVCF" in fit_name) or ("RVRF" in fit_name)):
						continue
					
					tmp_datacards_workspaces = datacards_workspaces[fit_name] if freeze_syst_uncs else datacards_workspaces
					
					tmp_fit_options = fit_options.get("options", "").format(
							CVCF_BINS=int(cv_bins[0] * cf_bins[0]),
							CV_MIN=cv_bins[1],
							CV_MAX=cv_bins[2],
							CF_MIN=cf_bins[1],
							CF_MAX=cf_bins[2],
							RVRF_BINS=int(rv_bins[0] * rf_bins[0]),
							RV_MIN=rv_bins[1],
							RV_MAX=rv_bins[2],
							RF_MIN=rf_bins[1],
							RF_MAX=rf_bins[2],
							RMIN="{RMIN}",
							RMAX="{RMAX}"
					)
					
					datacards.combine(datacards_cbs, tmp_datacards_workspaces, datacards_poi_ranges.get(fit_name, None), args.n_processes, "-t -1 --expectSignal 1 -M {method} {fit_options} {freeze} {stable} -n {name}".format(
							method=fit_options.get("method", "MaxLikelihoodFit"),
							fit_options=tmp_fit_options,
							freeze="--snapshotName {method} -S 0".format(method=fit_options.get("method", "MaxLikelihoodFit")) if freeze_syst_uncs else "--saveWorkspace",
							stable=stable_options,
							name="\"\"" if fit_name == "" else (fit_name + ("{CHUNK}" if "--points" in tmp_fit_options else ""))
					))
					
					if fit_options.get("method", "MaxLikelihoodFit") == "MaxLikelihoodFit":
						datacards_postfit_shapes = datacards.postfit_shapes(datacards_cbs, False, args.n_processes, "--sampling" + (" --print" if args.n_processes <= 1 else ""))
						datacards.prefit_postfit_plots(datacards_cbs, datacards_postfit_shapes, plotting_args={"ratio" : args.ratio, "args" : args.args}, n_processes=args.n_processes)
						datacards.pull_plots(datacards_postfit_shapes, s_fit_only=False, plotting_args={"fit_poi" : ["r"], "formats" : ["pdf", "png"]}, n_processes=args.n_processes)
						datacards.print_pulls(datacards_cbs, args.n_processes, "-A -p {POI}".format(POI="r"))
					
				datacards.annotate_trees(tmp_datacards_workspaces, "higgsCombine*{method}*mH*.root".format(method=fit_options.get("method", "MaxLikelihoodFit")), os.path.join(sub_dir_base, "(\d*)/.*.root"), None, args.n_processes, "-t limit -b lumi")
				
				json_configs.extend(model_settings.get("fit_plots", []))
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

