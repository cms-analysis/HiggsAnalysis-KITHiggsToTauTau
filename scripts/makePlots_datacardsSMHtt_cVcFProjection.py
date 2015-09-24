#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import argparse
import copy
import glob
import os

import combineharvester as ch

import Artus.Utility.jsonTools as jsonTools

import HiggsAnalysis.KITHiggsToTauTau.plotting.higgsplot as higgsplot
import HiggsAnalysis.KITHiggsToTauTau.datacards.datacardconfigs as datacardconfigs
import HiggsAnalysis.KITHiggsToTauTau.datacards.smhttdatacards as smhttdatacards


if __name__ == "__main__":

	parser = argparse.ArgumentParser(description="Make Projections of the cV-cF scan based on existing datacards.",
	                                 parents=[logger.loggingParser])

	parser.add_argument("-d", "--datacards", nargs="+", required=True,
	                    help="Datacards.")
	parser.add_argument("-L", "--lumi-datacards", type=float, default=40.03,
	                    help="Integrated luminosity / pb used for the datacards. [Default: %(default)s]")
	parser.add_argument("-l", "--lumis", nargs="+", type=int, default=[1000, 5000, 10000, 15000, 20000, 25000],
	                    help="Projection values for integrated luminosities / pb.")
	parser.add_argument("--cv-bins", default="30,0.0,3.0",
	                    help="Binning of the grid for the cV axis.")
	parser.add_argument("--cf-bins", default="30,0.0,2.0",
	                    help="Binning of the grid for the cF axis.")
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
		
		output_dir_base = args.output_dir
		if output_dir_base is None:
			output_dir_base = os.path.join(os.path.splitext(datacard)[0], "projection/cv_cf")
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
		
		cv_bins = [float(b) for b in args.cv_bins.split(",")]
		cf_bins = [float(b) for b in args.cf_bins.split(",")]
		assert cv_bins[0] == cf_bins[0]
		# cV-cF scans
		datacards_workspaces = scaled_datacards.text2workspace(
				datacards_cbs,
				args.n_processes,
				"-P \"HiggsAnalysis.CombinedLimit.HiggsCouplings:cVcF\" --PO \"cVRange={CV_MIN}:{CV_MAX}\" --PO \"cFRange={CF_MIN}:{CF_MAX}\"".format(
						CV_MIN=cv_bins[1],
						CV_MAX=cv_bins[2],
						CF_MIN=cf_bins[1],
						CF_MAX=cf_bins[2],
				)
		)
		scaled_datacards.combine(
				datacards_cbs,
				datacards_workspaces,
				args.n_processes,
				"-t -1 --expectSignal 1 -M MultiDimFit --algo grid --points {N_BINS} -n \"\"".format( # --firstPoint 1 --lastPoint 900
						N_BINS=int(cv_bins[0] * cf_bins[0])
				)
		)
		datacards.annotate_trees(datacards_workspaces, "higgsCombine*MultiDimFit*mH*.root", "projection/cv_cf/(\d*)/.*.root", args.n_processes, "-t limit -b lumi")

		# plotting
		plot_configs = []
		
		config = jsonTools.JsonDict(os.path.expandvars("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/combine/cv_cf_scan_1sigma_over_lumi.json")).doIncludes().doComments()
		
		config["directories"] = sorted(glob.glob(os.path.join(output_dir_base, "*")))
		config["weights"] = [w.replace("lumi", "(lumi/1000.0)") for w in config.get("weights", [])]
		config["x_bins"] = args.cv_bins
		config["y_bins"] = args.cf_bins
		
		if not "CombineHistograms" in config.get("analysis_modules", []):
			config.setdefault("analysis_modules", []).append("CombineHistograms")
		config.setdefault("combine_result_nicks", []).append("cVcF_lumi")
		config.setdefault("nicks_whitelist", []).extend(config["combine_result_nicks"])
		
		"""
		if not "ContourFromHistogram" in config.get("analysis_modules", []):
			config.setdefault("analysis_modules", []).append("ContourFromHistogram")
		config.setdefault("2d_histogram_nicks", []).append("cVcF_lumi")
		config.setdefault("contour_thresholds", []).append(" ".join([str(lumi) for lumi in args.lumis]))
		"""
		
		config["markers"] = "COLZ" # "CONT1Z"
		
		config["output_dir"] = os.path.join(output_dir_base, "plots")
		
		plot_configs.append(config)
		
		if log.isEnabledFor(logging.DEBUG):
			import pprint
			pprint.pprint(plot_configs)
		
		higgsplot.HiggsPlotter(list_of_config_dicts=plot_configs, list_of_args_strings=[args.args], n_processes=args.n_processes, n_plots=args.n_plots)
