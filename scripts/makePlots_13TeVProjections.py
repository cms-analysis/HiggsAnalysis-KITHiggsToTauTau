#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import argparse
import glob
import os
import shlex

import ROOT

from HiggsAnalysis.HiggsToTauTau.utils import parseArgs

import Artus.Utility.jsonTools as jsonTools
import Artus.Utility.progressiterator as progressiterator
import HiggsAnalysis.KITHiggsToTauTau.plotting.higgsplot as higgsplot


def clear_output_dir(output_dir):
	if os.path.exists(output_dir):
		command = "rm -rfv {o}".format(o=output_dir)
		log.info(command)
		logger.subprocessCall(shlex.split(command))
	os.makedirs(output_dir)

def do_limits(output_dir):
	command = "submit.py --interactive --stable-new --asymptotic {datacards}".format(
		datacards=os.path.join(output_dir, "*")
	)
	log.info(command)
	logger.subprocessCall(shlex.split(command))

def do_p_values(output_dir):
	command = "submit.py --interactive --stable-new --pvalue-frequentist {datacards}".format(
		datacards=os.path.join(output_dir, "*")
	)
	log.info(command)
	logger.subprocessCall(shlex.split(command))

def do_cv_cf_scan(output_dir, mass="125"):
	command = "submit.py --interactive --stable-new --multidim-fit --physics-model cV-cF {datacards}".format(
		datacards=os.path.join(output_dir, mass)
	)
	log.info(command)
	logger.subprocessCall(shlex.split(command))
	
	command = command.replace("submit.py --interactive", "limit.py --algo grid")
	log.info(command)
	logger.subprocessCall(shlex.split(command))


def annotate_lumi_scale(output_dir, lumi_scale):
	command = "annotate-trees.py {root_files} --tree limit --values {l} --branches lumi".format(
		root_files=" ".join(glob.glob(os.path.join(output_dir, "*", "higgsCombine*.root"))),
		l=lumi_scale
	)
	log.info(command)
	logger.subprocessCall(shlex.split(command))


	


if __name__ == "__main__":

	parser = argparse.ArgumentParser(description="Project results to 13TeV conditions.",
	                                 parents=[logger.loggingParser])
	
	parser.add_argument("-l", "--lumi-scales", nargs="+",
	                    default=[0.1, 0.25, 0.5, 1.0, 2.0, 5.0, 10.0],
	                    help="Luminosity scale factors. [Default: %(default)s]")
	parser.add_argument("-o", "--output-dir", default="output/datacards/projection",
	                    help="Output directory. Contents will be cleaned up. [Default: %(default)s]")
	parser.add_argument("-a", "--args", default="--plot-modules PlotRootHtt",
	                    help="Additional Arguments for HarryPlotter. [Default: %(default)s]")
	parser.add_argument("-n", "--n-processes", type=int, default=1,
	                    help="Number of (parallel) processes. [Default: %(default)s]")
	
	args = parser.parse_args()
	logger.initLogger(args)
	
	plot_configs = []
	
	# 8TeV results
	output_dir = os.path.join(args.output_dir, "8TeV")
	clear_output_dir(output_dir)
	
	# datacards
	command = "SMLegacyDatacards --output {output_dir} --asimov --asimov-mass 125".format(
			output_dir=output_dir
	)
	log.info(command)
	logger.subprocessCall(shlex.split(command))
	
	# limits
	do_limits(output_dir)
	
	# p-values
	do_p_values(output_dir)
	
	# cV-cF scan
	do_cv_cf_scan(output_dir)
	
	# annotations for plotting
	annotate_lumi_scale(output_dir, lumi_scale=-1.0)
	
	# plotting
	for json in ["exp_limit_over_mass.json", "exp_obs_limit_over_mass.json", "exp_obs_pvalue_over_mass.json"]:
		plot_configs.append({
				"json_defaults" : [os.path.join("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/combine/", json)],
				"directories" : [os.path.join(output_dir, "*")],
				"output_dir" : os.path.join(output_dir, "plots"),
		})
	
	# 13TeV projections
	cv_cf_scan_plot_config = {
		"json_defaults" : ["$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/combine/cv_cf_scan_1sigma_over_lumi.json"],
		"output_dir" : os.path.join(args.output_dir, "13TeV", "plots"),
	}
	
	for lumi_scale in progressiterator.ProgressIterator(args.lumi_scales, description="Process projections"):
		output_dir = os.path.join(args.output_dir, "13TeV", "lumi_scale_{l}".format(l=lumi_scale))
		clear_output_dir(output_dir)
		
		# datacards
		command = "SMLegacyDatacards --output {output_dir} --asimov --asimov-mass 125 --energy 13 --lumi-scale {l} --masses 125".format(
				output_dir=output_dir,
				l=lumi_scale
		)
		log.info(command)
		logger.subprocessCall(shlex.split(command))
		
		# limits
		do_limits(output_dir)
		
		# p-values
		do_p_values(output_dir)
		
		# cV-cF scan
		do_cv_cf_scan(output_dir)
		
		# annotations for plotting
		annotate_lumi_scale(output_dir, lumi_scale=lumi_scale)
		
		# plotting
		cv_cf_scan_plot_config.setdefault("directories", []).append(os.path.join(output_dir, "*"))
		cv_cf_scan_plot_config.setdefault("nicks", []).append("noplot_2d_hist_{l}".format(l=lumi_scale))
		cv_cf_scan_plot_config.setdefault("2d_histogram_nicks", []).append(cv_cf_scan_plot_config["nicks"][-1])
		cv_cf_scan_plot_config.setdefault("contour_graph_nicks", []).append("contour_{l}".format(l=lumi_scale))
		cv_cf_scan_plot_config.setdefault("labels", []).append("lumi scale {l}".format(l=lumi_scale))
		
		
	# plotting
	plot_configs.append(cv_cf_scan_plot_config)
	for json in ["exp_limit_over_lumi.json", "exp_obs_limit_over_lumi.json", "exp_obs_pvalue_over_lumi.json"]:
		plot_configs.append({
				"json_defaults" : [os.path.join("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/combine/", json)],
				"directories" : [os.path.join(args.output_dir, "13TeV", "lumi_scale_*", "125")],
				"output_dir" : os.path.join(args.output_dir, "13TeV", "plots"),
		})
	
	higgsplot.HiggsPlotter(list_of_config_dicts=plot_configs, list_of_args_strings=[args.args], n_processes=args.n_processes)
	
