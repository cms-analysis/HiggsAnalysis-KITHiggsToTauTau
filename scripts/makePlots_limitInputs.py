#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import argparse
import os

import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gErrorIgnoreLevel = ROOT.kError
from HiggsAnalysis.HiggsToTauTau.utils import parseArgs

import Artus.Utility.jsonTools as jsonTools

import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.mt as mt
import HiggsAnalysis.KITHiggsToTauTau.plotting.higgsplot as higgsplot



if __name__ == "__main__":

	parser = argparse.ArgumentParser(description="Make Data-MC control plots.",
	                                 parents=[logger.loggingParser])

	parser.add_argument("-i", "--input-dir", required=True,
	                    help="Input directory.")
	parser.add_argument("--channels", nargs="*",
	                    default=["mt"], choices=["mt"],
	                    #default=["tt", "mt", "et", "em", "mm", "ee"], # other channels currently not supported
	                    help="Channels. [Default: %(default)s]")
	parser.add_argument("--categories", nargs="*",
	                    default=["Inc", "0Jet", "1Jet", "2Jet"],
	                    help="Categories. [Default: %(default)s]")
	parser.add_argument("--quantities", nargs="*",
	                    default=["inclusive", "m_ll", "m_sv"],
	                    help="Quantities. [Default: %(default)s]")
	parser.add_argument("-m", "--higgs-masses", nargs="+", default=["110_145:5"],
	                    help="Higgs masses. [Default: %(default)s]")
	parser.add_argument("--tau-es-shifts", nargs="+", default=["Nom", "Up", "Down"],
	                    choices=["Nom", "Up", "Down"],
	                    help="Tau ES shifts. [Default: %(default)s]")
	parser.add_argument("-a", "--args", default="--plot-modules ExportRoot PlotRootHtt",
	                    help="Additional Arguments for HarryPlotter. [Default: %(default)s]")
	parser.add_argument("-n", "--n-processes", type=int, default=1,
	                    help="Number of (parallel) processes. [Default: %(default)s]")
	                    
	
	args = vars(parser.parse_args())
	logger.initLogger(args)
	args["higgs_masses"] = parseArgs(args["higgs_masses"])
	
	channel_renamings = {
		"mt" : "muTau",
	}
	category_renamings = {
		"0Jet" : "0jet",
		"1Jet" : "1jet",
		"2Jet" : "vbf",
	}
	label_renamings = {
		"Data" : "data_obs",
	}
	label_suffix = ""
	
	harry_configs = []
	harry_args = []
	
	for tau_es_shift in args["tau_es_shifts"]:
		label_suffix = ("_CMS_scale_t_%s_8TeV" + tau_es_shift) if tau_es_shift != "Nom" else ""
		
		for channel in args["channels"]:
			if "%" in label_suffix:
				label_suffix = label_suffix % channel_renamings.get(channel, channel)
			
			add_data = (tau_es_shift == "Nom")
			add_ztt = True
			add_zl = (tau_es_shift == "Nom")
			add_zj = (tau_es_shift == "Nom")
			add_ttj = (tau_es_shift == "Nom")
			add_diboson = (tau_es_shift == "Nom")
			add_wjets = (tau_es_shift == "Nom")
			add_qcd = (tau_es_shift == "Nom")
			add_signal = args["higgs_masses"]
			
			channel_settings = mt.MT(add_data=add_data,
			                         add_ztt=add_ztt,
			                         add_zl=add_zl,
			                         add_zj=add_zj,
			                         add_ttj=add_ttj,
			                         add_diboson=add_diboson,
			                         add_wjets=add_wjets,
			                         add_qcd=add_qcd,
			                         add_ggh_signal=add_signal,
			                         add_vbf_signal=add_signal,
			                         add_vh_signal=add_signal) if channel == "mt" else None
			
			for category in args["categories"]:
				if category == "None":
					category = None
			
				config = channel_settings.get_config(category=category, tau_es_shift=tau_es_shift) if channel == "mt" else jsonTools.JsonDict()
			
				for quantity in args["quantities"]:
					json_exists = True
					json_configs = [
						os.path.expandvars("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/control_plots/%s_%s.json" % (channel, quantity)),
						os.path.expandvars("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/samples/complete/%s.json" % (channel))
					] if channel != "mt" else [os.path.expandvars("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/control_plots/%s_%s.json" % (channel, quantity))]
					if not os.path.exists(json_configs[0]):
						json_exists = False
						json_configs[0] = os.path.expandvars("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/sync_exercise/%s_default.json" % (channel))
					json_defaults = jsonTools.JsonDict([os.path.expandvars(json_file) for json_file in json_configs]).doIncludes().doComments()
					if channel == "mt":
						json_defaults += config
				
					if not category is None:
						json_defaults["output_dir"] = os.path.join(json_defaults.setdefault("output_dir", "plots"), category)
			
					for index, label in enumerate(json_defaults.setdefault("labels", [])):
						json_defaults["labels"][index] = os.path.join("%s_%s" % (channel_renamings.get(channel, channel),
							                                                     category_renamings.get(category, category)),
							                                          label_renamings.get(label, label)+label_suffix)
			
					harry_configs.append(json_defaults)
					harry_args.append("-d %s %s -f png pdf %s" % (args["input_dir"], ("" if json_exists else ("-x %s" % quantity)), args["args"]))
			
	higgsplot.HiggsPlotter(list_of_config_dicts=harry_configs, list_of_args_strings=harry_args, n_processes=args["n_processes"])

