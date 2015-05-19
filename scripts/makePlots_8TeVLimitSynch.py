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

import HiggsAnalysis.KITHiggsToTauTau.plotting.higgsplot as higgsplot

# for channel in et mt; do rm -rf plots/; mkdir -p HiggsAnalysis/KITHiggsToTauTau/auxiliaries/combine/shapes/${channel}; ./HiggsAnalysis/KITHiggsToTauTau/scripts/makePlots_limitInputs.py -i /nfs/dust/cms/user/tmuller/htautau/artus/2015-03-16_17-02_svfitTest/merged/ --quantities svfitMass --channels ${channel} -o HiggsAnalysis/KITHiggsToTauTau/auxiliaries/combine/shapes/${channel}/htt_${channel}.inputs-sm-8TeV.root; done

def clear_output_dir(output_dir, print_only=False):
	if os.path.exists(output_dir):
		command = "rm -rfv {o}".format(o=output_dir)
		log.info(command)
		if not print_only:
			logger.subprocessCall(shlex.split(command))
	if not print_only:
		os.makedirs(output_dir)

def do_max_likelihood_fits(output_dir, print_only=False):
	command = "limit.py --stable-new --max-likelihood {datacards}".format(
		datacards=os.path.join(output_dir, "125")
	)
	log.info(command)
	if not print_only:
		os.system(command)
		#logger.subprocessCall(shlex.split(command))

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


	


if __name__ == "__main__":

	parser = argparse.ArgumentParser(description="Project results to 13TeV conditions.",
	                                 parents=[logger.loggingParser])
	
	parser.add_argument("--channels", nargs="*",
	                    default=["mt"], choices=["et", "mt", "em"],
	                    #default=["tt", "mt", "et", "em", "mm", "ee"], # other channels currently not supported
	                    help="Channels. [Default: %(default)s]")
	parser.add_argument("-p", "--plots-only", default=False, action="store_true",
	                    help="Do only the plotting assuming the ROOT files are only created. [Default: %(default)s]")
	parser.add_argument("--print-only", default=False, action="store_true",
	                    help="Print only the commands to be executed. [Default: %(default)s]")
	parser.add_argument("-a", "--args", default="--plot-modules PlotRootHtt",
	                    help="Additional Arguments for HarryPlotter. [Default: %(default)s]")
	parser.add_argument("-n", "--n-processes", type=int, default=1,
	                    help="Number of (parallel) processes. [Default: %(default)s]")
	parser.add_argument("-f", "--n-plots", type=int,
	                    help="Number of plots. [Default: all]")
	
	args = parser.parse_args()
	logger.initLogger(args)
	
	channels = " ".join(["--channel "+channel for channel in args.channels])
	
	cb_commands = [
		"SMDatacards --output {output_dir} {channels}",
		"SMLegacyDatacards --output {output_dir} {channels}",
	]
	output_dirs = [
		os.path.expandvars("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/auxiliaries/combine/datacards/"),
		os.path.expandvars("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/auxiliaries/combine/legacy_datacards/"),
	]
	
	plot_configs = [{
			"json_defaults" : ["$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/combine/exp_limit_over_mass_without_band.json"],
			"output_dir" : os.path.join(output_dirs[0], "plots"),
			"analysis_modules" : ["Divide"],
			"divide_result_nicks" : ["divide"],
			"subplot_nicks" : ["divide"],
			"colors": ["kRed", "kBlack", "kBlack"],
			"labels": ["KIT", "legacy", ""],
			"legend": [0.25, 0.7, 0.5, 0.9],
			"y_lims": [0.0, 3.5],
	}]
	plot_configs.append(copy.deepcopy(plot_configs[-1]))
	plot_configs[-1]["json_defaults"] = ["$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/combine/obs_limit_over_mass_without_band.json"],
	plot_configs[-1]["y_lims"] = [0.0, 12.0],
	
	for cb_command, output_dir in zip(cb_commands, output_dirs):
		if not args.plots_only:
			clear_output_dir(output_dir, args.print_only)
		
			# datacards
			command = cb_command.format(output_dir=output_dir, channels=channels)
			log.info(command)
			if not args.print_only:
				logger.subprocessCall(shlex.split(command))
		
			# max likelihood fits
			do_max_likelihood_fits(output_dir, args.print_only)
		
			# limits
			do_limits(output_dir, args.print_only)
		
			# p-values
			#do_p_values(output_dir, args.print_only)
		
			# cV-cF scan
			#do_cv_cf_scan(output_dir, print_only=args.print_only)
	
		# plotting
		plot_configs[0].setdefault("directories", []).append(os.path.join(output_dir, "*"))
		plot_configs[1].setdefault("directories", []).append(os.path.join(output_dir, "*"))
		
		for json in ["exp_limit_over_mass.json", "exp_obs_limit_over_mass.json",
				     ]:#"exp_pvalue_over_mass.json", "exp_obs_pvalue_over_mass.json"]:
			plot_configs.append({
					"json_defaults" : [os.path.join("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/combine/", json)],
					"directories" : [os.path.join(output_dir, "*")],
					"output_dir" : os.path.join(output_dir, "plots"),
					"y_lims" : ([0.0, 12.0] if "_obs_" in json else [0.0, 3.5]),
			})
	
	if not args.print_only:
		higgsplot.HiggsPlotter(list_of_config_dicts=plot_configs, list_of_args_strings=[args.args], n_processes=args.n_processes, n_plots=args.n_plots)

