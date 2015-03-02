#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import argparse
import copy
import glob
import os
import shlex

import ROOT

from HiggsAnalysis.HiggsToTauTau.utils import parseArgs

import Artus.Utility.jsonTools as jsonTools
import Artus.Utility.progressiterator as progressiterator
import HiggsAnalysis.KITHiggsToTauTau.plotting.higgsplot as higgsplot


def clear_output_dir(output_dir, print_only=False):
	if os.path.exists(output_dir):
		command = "rm -rfv {o}".format(o=output_dir)
		log.info(command)
		if not print_only:
			logger.subprocessCall(shlex.split(command))
	if not print_only:
		os.makedirs(output_dir)

def do_limits(output_dir, print_only=False):
	command = "submit.py --interactive --stable-new --asymptotic {datacards}".format(
		datacards=os.path.join(output_dir, "*")
	)
	log.info(command)
	if not print_only:
			logger.subprocessCall(shlex.split(command))

def do_p_values(output_dir, print_only=False):
	command = "submit.py --interactive --stable-new --pvalue-frequentist {datacards}".format(
		datacards=os.path.join(output_dir, "*")
	)
	log.info(command)
	if not print_only:
			logger.subprocessCall(shlex.split(command))

def do_cv_cf_scan(output_dir, mass="125", print_only=False):
	command = "submit.py --interactive --stable-new --multidim-fit --physics-model cV-cF --points 400 {datacards}".format(
		datacards=os.path.join(output_dir, mass)
	)
	log.info(command)
	if not print_only:
			logger.subprocessCall(shlex.split(command))
	
	command = command.replace("submit.py --interactive", "limit.py --algo grid")
	log.info(command)
	if not print_only:
			logger.subprocessCall(shlex.split(command))
	
	command = "rm -rfv {dirs} log/".format(dirs=" ".join(glob.glob("*CV-CF-{mass}/".format(mass=mass)))
	)
	log.info(command)
	if not print_only:
			logger.subprocessCall(shlex.split(command))


def annotate_lumi(output_dir, lumi, print_only=False):
	command = "annotate-trees.py {root_files} --tree limit --values {l} --branches lumi".format(
		root_files=" ".join(glob.glob(os.path.join(output_dir, "*", "higgsCombine*.root"))),
		l=lumi
	)
	log.info(command)
	if not print_only:
			logger.subprocessCall(shlex.split(command))


	


if __name__ == "__main__":

	parser = argparse.ArgumentParser(description="Project results to 13TeV conditions.",
	                                 parents=[logger.loggingParser])
	
	parser.add_argument("-l", "--lumis", nargs="+",
	                    default=[5.0, 10.0, 15.0, 20.0, 50.0, 100.0, 300.0],
	                    help="Luminosities. [Default: %(default)s]")
	parser.add_argument("-o", "--output-dir", default="output/datacards/projection",
	                    help="Output directory. Contents will be cleaned up. [Default: %(default)s]")
	parser.add_argument("-p", "--plots-only", default=False, action="store_true",
	                    help="Do only the plotting assuming the ROOT files are only created. [Default: %(default)s]")
	parser.add_argument("--print-only", default=False, action="store_true",
	                    help="Print only the commands to be executed. [Default: %(default)s]")
	parser.add_argument("-a", "--args", default="--plot-modules PlotRootHtt",
	                    help="Additional Arguments for HarryPlotter. [Default: %(default)s]")
	parser.add_argument("-n", "--n-processes", type=int, default=1,
	                    help="Number of (parallel) processes. [Default: %(default)s]")
	
	args = parser.parse_args()
	logger.initLogger(args)
	
	plot_configs = []
	
	# 8TeV results
	output_dir = os.path.join(args.output_dir, "8TeV")
	if not args.plots_only:
		clear_output_dir(output_dir, args.print_only)
		
		# datacards
		command = "SMLegacyDatacards --output {output_dir} --asimov --asimov-mass 125".format(
				output_dir=output_dir
		)
		log.info(command)
		if not args.print_only:
			logger.subprocessCall(shlex.split(command))
		
		# limits
		do_limits(output_dir, args.print_only)
		
		# p-values
		do_p_values(output_dir, args.print_only)
		
		# cV-cF scan
		do_cv_cf_scan(output_dir, print_only=args.print_only)
		
		# annotations for plotting
		annotate_lumi(output_dir, lumi=-1.0, print_only=args.print_only)
	
	# plotting
	for json in ["exp_limit_over_mass.json", "exp_obs_limit_over_mass.json",
	             "exp_pvalue_over_mass.json", "exp_obs_pvalue_over_mass.json"]:
		plot_configs.append({
				"json_defaults" : [os.path.join("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/combine/", json)],
				"directories" : [os.path.join(output_dir, "*")],
				"output_dir" : os.path.join(output_dir, "plots"),
		})
	
	# 13TeV projections
	cv_cf_scan_plot_configs = {
		"json_defaults" : ["$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/combine/cv_cf_scan_1sigma_over_lumi.json"],
		"output_dir" : os.path.join(args.output_dir, "13TeV", "plots"),
	}
	cv_cf_scan_plot_configs = [copy.deepcopy(cv_cf_scan_plot_configs), copy.deepcopy(cv_cf_scan_plot_configs)]
	
	cv_cf_scan_plot_configs[0].setdefault("directories", []).append(os.path.join(output_dir, "125"))
	cv_cf_scan_plot_configs[0].setdefault("nicks", []).append("2d_hist_8TeV")
	cv_cf_scan_plot_configs[0].setdefault("2d_histogram_nicks", []).append(cv_cf_scan_plot_configs[0]["nicks"][-1])
	cv_cf_scan_plot_configs[0].setdefault("contour_graph_nicks", []).append("contour_8TeV")
	cv_cf_scan_plot_configs[0].setdefault("labels", []).append("8 TeV")
	cv_cf_scan_plot_configs[0]["colors"] = [
		"#FF0000",
		"#99CCFF",
		"#66CCFF",
		"#3399FF",
		"#3366FF",
		"#0000FF",
		"#0000CC",
		"#000099",
		"#000066"
	]
	cv_cf_scan_plot_configs[0]["filename"] = "cv_cf_scan_1sigma_over_lumi_8_13_TeV"
	cv_cf_scan_plot_configs[1]["filename"] = "cv_cf_scan_1sigma_over_lumi_13_TeV"
	
	for lumi in progressiterator.ProgressIterator(args.lumis, description="Process projections"):
		output_dir = os.path.join(args.output_dir, "13TeV", "lumi_{l}".format(l=lumi))
		if not args.plots_only:
			clear_output_dir(output_dir, args.print_only)
		
			# datacards
			command = "SMLegacyDatacards {channels} --output {output_dir} --asimov --asimov-mass 125 --energy 13 --lumi {l} --masses 125".format(
					channels=channels,
					output_dir=output_dir,
					l=lumi
			)
			log.info(command)
			if not args.print_only:
				logger.subprocessCall(shlex.split(command))
			
			# limits
			do_limits(output_dir, args.print_only)
			
			# p-values
			do_p_values(output_dir, args.print_only)
			
			# cV-cF scan
			do_cv_cf_scan(output_dir, print_only=args.print_only)
			
			# annotations for plotting
			annotate_lumi(output_dir, lumi=lumi, print_only=args.print_only)
		
		# plotting
		for cv_cf_scan_plot_config in cv_cf_scan_plot_configs:
			cv_cf_scan_plot_config.setdefault("directories", []).append(os.path.join(output_dir, "*"))
			cv_cf_scan_plot_config.setdefault("nicks", []).append("2d_hist_{l}".format(l=lumi))
			cv_cf_scan_plot_config.setdefault("2d_histogram_nicks", []).append(cv_cf_scan_plot_config["nicks"][-1])
			cv_cf_scan_plot_config.setdefault("contour_graph_nicks", []).append("contour_{l}".format(l=lumi))
			cv_cf_scan_plot_config.setdefault("labels", []).append("{l}/fb".format(l=lumi))
		
	# plotting
	plot_configs.extend(cv_cf_scan_plot_configs)
	for json in ["exp_limit_over_lumi.json", "exp_obs_limit_over_lumi.json",
	             "exp_pvalue_over_lumi.json", "exp_obs_pvalue_over_lumi.json"]:
		plot_configs.append({
				"json_defaults" : [os.path.join("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/combine/", json)],
				"directories" : [os.path.join(args.output_dir, "13TeV", "lumi_*", "125")],
				"output_dir" : os.path.join(args.output_dir, "13TeV", "plots"),
		})
	
	if not args.print_only:
		higgsplot.HiggsPlotter(list_of_config_dicts=plot_configs, list_of_args_strings=[args.args], n_processes=args.n_processes)
	
