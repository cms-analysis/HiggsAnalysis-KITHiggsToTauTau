#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import argparse
import copy
import os

import combineharvester as ch

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
	parser.add_argument("-a", "--args", default="",
	                    help="Additional Arguments for HarryPlotter. [Default: %(default)s]")
	parser.add_argument("-n", "--n-processes", type=int, default=1,
	                    help="Number of (parallel) processes. [Default: %(default)s]")
	parser.add_argument("-f", "--n-plots", type=int, nargs=2, default=[None, None],
	                    help="Number of plots for datacard inputs (1st arg) and for postfit plots (2nd arg). [Default: all]")
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
		datacards.replace_observation_by_asimov_dataset("125")
		
		output_dir_base = args.output_dir
		if output_dir_base is None:
			output_dir_base = os.path.join(os.path.splitext(datacard)[0], "projection/limit")
		output_dir_base = os.path.abspath(os.path.expandvars(output_dir_base))
		
		if args.clear_output_dir and os.path.exists(output_dir_base):
			logger.subprocessCall("rm -r " + output_dir_base, shell=True)
		
		# scale datacards
		datacards_cbs = {}
		for lumi in args.lumis:
			output_dir = os.path.join(output_dir_base, "{:05}".format(lumi))
			if not os.path.exists(output_dir):
				os.makedirs(output_dir)
			
			scaled_datacards = smhttdatacards.SMHttDatacards(cb=datacards.cb.deep())
			
			lumi_scale_factor = lumi / args.lumi_datacards
			scaled_datacards.scale_expectation(lumi_scale_factor)
			
			datacards_cbs.update(scaled_datacards.write_datacards(
					os.path.basename(datacard),
					os.path.splitext(os.path.basename(datacard))[0]+"_input.root",
					output_dir
			))
		
		datacards_workspaces = datacards.text2workspace(datacards_cbs, n_processes=args.n_processes)
		
		# Max. likelihood fit and postfit plots
		datacards.combine(datacards_cbs, datacards_workspaces, args.n_processes, "-M MaxLikelihoodFit -n \"\"")
		datacards_postfit_shapes = datacards.postfit_shapes(datacards_cbs, args.n_processes, "--sampling" + (" --print" if args.n_processes <= 1 else ""))
		
		# Asymptotic limits
		datacards.combine(datacards_cbs, datacards_workspaces, args.n_processes, "-M Asymptotic -n \"\"")

