#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import argparse
import os
import shlex

import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gErrorIgnoreLevel = ROOT.kError
from HiggsAnalysis.HiggsToTauTau.utils import parseArgs

import Artus.Utility.jsonTools as jsonTools
import Artus.Utility.tools as tools

import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.samples as samples
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.quantities as quantities
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.systematics as systematics
import HiggsAnalysis.KITHiggsToTauTau.plotting.higgsplot as higgsplot



if __name__ == "__main__":

	parser = argparse.ArgumentParser(description="Make Data-MC control plots.",
	                                 parents=[logger.loggingParser])

	parser.add_argument("-i", "--input-dir", required=True,
	                    help="Input directory.")
	parser.add_argument("-o", "--root-output", default="htt.inputs-sm-8TeV.root",
	                    help="Merged ROOT output. [Default: %(default)s]")
	parser.add_argument("--channels", nargs="*",
	                    default=["mt"], choices=["et", "mt", "em", "mm"],
	                    #default=["tt", "mt", "et", "em", "mm", "ee"], # other channels currently not supported
	                    help="Channels. [Default: %(default)s]")
	parser.add_argument("--categories", nargs="*",
	                    default=["0JetMedium", "0JetHigh", "1JetMedium", "1JetHigh", "1JetHighBoost", "2JetVbfLoose", "2JetVbfTight"],
	                    help="Categories. [Default: %(default)s]")
	parser.add_argument("--quantities", nargs="*",
	                    default=["inclusive", "m_ll", "svfitMass"],
	                    help="Quantities. [Default: %(default)s]")
	parser.add_argument("-m", "--higgs-masses", nargs="+", default=["110_145:5"],
	                    help="Higgs masses. [Default: %(default)s]")
	parser.add_argument("--tau-es-shifts", nargs="+", type=float, default=[1.0, -1.0],
	                    help="Tau ES shifts. [Default: %(default)s]")
	parser.add_argument("--svfit-mass-shifts", nargs="+", type=float, default=[1.0, -1.0],
	                    help="Svfit mass shifts. [Default: %(default)s]")
	parser.add_argument("-a", "--args", default="--plot-modules ExportRoot",
	                    help="Additional Arguments for HarryPlotter. [Default: %(default)s]")
	parser.add_argument("-n", "--n-processes", type=int, default=1,
	                    help="Number of (parallel) processes. [Default: %(default)s]")
	parser.add_argument("-f", "--n-plots", type=int,
	                    help="Number of plots. [Default: all]")

	args = vars(parser.parse_args())
	logger.initLogger(args)
	args["higgs_masses"] = parseArgs(args["higgs_masses"])
	
	channel_renamings = {
		#"mt" : "muTau",
	}
	category_renamings = {
		"0Jet" : "0jet",
		"0JetLow" : "0jet_low",
		"0JetMedium" : "0jet_medium",
		"0JetHigh" : "0jet_high",
		"1Jet" : "1jet",
		"1JetLow" : "1jet_low",
		"1JetMedium" : "1jet_medium",
		"1JetHigh" : "1jet_high_lowhiggs",
		"1JetHighBoost" : "1jet_high_mediumhiggs",
		"1JetHighLargeBoost" : "1jet_high_highhiggs",
		"2Jet" : "vbf",
		"2JetVbfLoose" : "vbf_loose",
		"2JetVbfTight" : "vbf_tight",
	}
	label_renamings = {
		"Data" : "data_obs",
		"WJets" : "W",
		"TTJ" : "TT",
		"VBF90" : "qqH90",
		"VBF95" : "qqH95",
		"VBF100" : "qqH100",
		"VBF105" : "qqH105",
		"VBF110" : "qqH110",
		"VBF115" : "qqH115",
		"VBF120" : "qqH120",
		"VBF125" : "qqH125",
		"VBF130" : "qqH130",
		"VBF135" : "qqH135",
		"VBF140" : "qqH140",
		"VBF145" : "qqH145",
		"VBF150" : "qqH150",
		"VBF155" : "qqH155",
		"VBF160" : "qqH160",
	}
	
	harry_configs = []
	harry_args = []
	
	systematic_shifts = [(systematics.Nominal, "", 0.0)]
	systematic_shifts += [(systematics.TauEsSystematic, "CMS_scale_t_%s_8TeV", shift) for shift in args["tau_es_shifts"] if shift != 0.0]
	systematic_shifts += [(systematics.SvfitMassSystematic, "CMS_htt_ZLScale_%s_8TeV", shift) for shift in args["svfit_mass_shifts"] if shift != 0.0]
	
	sample_settings = samples.Sample()
	for uncertainty, name, shift in systematic_shifts:
		list_of_samples = []
		if uncertainty.add_ztt():
			list_of_samples.append(samples.Sample.ztt)
		if uncertainty.add_zl():
			list_of_samples.append(samples.Sample.zl)
		if uncertainty.add_zj():
			list_of_samples.append(samples.Sample.zj)
		if uncertainty.add_ttj():
			list_of_samples.append(samples.Sample.ttj)
		if uncertainty.add_vv():
			list_of_samples.append(samples.Sample.vv)
		if uncertainty.add_wj():
			list_of_samples.append(samples.Sample.wj)
		if uncertainty.add_qcd():
			list_of_samples.append(samples.Sample.qcd)
		if uncertainty.add_ggh():
			list_of_samples.append(samples.Sample.ggh)
		if uncertainty.add_qqh():
			list_of_samples.append(samples.Sample.qqh)
		if uncertainty.add_vh():
			list_of_samples.append(samples.Sample.vh)
		if uncertainty.add_data():
			list_of_samples.append(samples.Sample.data)
			
		for channel in args["channels"]:
			if "%s" in name:
				name = name % channel_renamings.get(channel, channel)
			
			for category in args["categories"]:
				if category == "None":
					category = None
				
				config = sample_settings.get_config(
						samples=list_of_samples,
						channel=channel,
						category=category,
						higgs_masses=args["higgs_masses"],
						normalise_signal_to_one_pb=True
				)
			
				for quantity in args["quantities"]:
					
					config["x_expressions"] = quantity
					config["x_bins"] = [channel+"_"+quantity]
					config["x_label"] = channel+"_"+quantity
				
					if not category is None:
						config["output_dir"] = os.path.join(config.setdefault("output_dir", "plots"), category)
			
					for index, label in enumerate(config.setdefault("labels", [])):
						config["labels"][index] = os.path.join("%s_%s" % (channel_renamings.get(channel, channel),
							                                                     category_renamings.get(category, category)),
							                                          label_renamings.get(label, label))
					
					config = uncertainty(config, name).get_config(shift)
					
					if quantity == "m_ll":
						config = quantities.VisibleMass(config).get_config(channel, category)
					if quantity == "svitMass":
						config = quantities.VisibleMass(config).get_config(channel, category)
					
					if "PrintInfos" in config.get("analysis_modules", []):
						config.get("analysis_modules", []).remove("PrintInfos")
					
					harry_configs.append(config)
					harry_args.append("-d %s --formats png pdf %s" % (args["input_dir"], args["args"]))
			
	higgs_plotter = higgsplot.HiggsPlotter(list_of_config_dicts=harry_configs, list_of_args_strings=harry_args, n_processes=args["n_processes"], n_plots=args["n_plots"])
	
	root_outputs = list(set([output for output in tools.flattenList(higgs_plotter.output_filenames) if output.endswith(".root")]))
	command = "hadd -f %s %s" % (args["root_output"], " ".join(root_outputs))
	log.info(command)
	logger.subprocessCall(shlex.split(command))
	log.info("Merged ROOT output is saved to \"%s\"." % args["root_output"])

