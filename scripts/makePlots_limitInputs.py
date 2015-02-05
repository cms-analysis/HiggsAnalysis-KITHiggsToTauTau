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

import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.mt as mt
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
	parser.add_argument("--tau-es-shifts", nargs="+", type=float, default=[1.0, -1.0],
	                    help="Tau ES shifts. [Default: %(default)s]")
	parser.add_argument("--svfit-mass-shifts", nargs="+", type=float, default=[1.0, -1.0],
	                    help="Svfit mass shifts. [Default: %(default)s]")
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
	
	harry_configs = []
	harry_args = []
	
	systematic_shifts = [(systematics.Nominal, "", 0.0)]
	systematic_shifts += [(systematics.TauEsSystematic, "CMS_scale_t_%s_8TeV", shift) for shift in args["tau_es_shifts"] if shift != 0.0]
	systematic_shifts += [(systematics.SvfitMassSystematic, "CMS_htt_ZLScale_%s_8TeV", shift) for shift in args["svfit_mass_shifts"] if shift != 0.0]
	
	for uncertainty, name, shift in systematic_shifts:
		
		for channel in args["channels"]:
			if "%s" in name:
				name = name % channel_renamings.get(channel, channel)
		
			channel_settings = mt.MT(add_data=uncertainty.add_data(),
			                         add_ztt=uncertainty.add_ztt(),
			                         add_zl=uncertainty.add_zl(),
			                         add_zj=uncertainty.add_zj(),
			                         add_ttj=uncertainty.add_ttj(),
			                         add_diboson=uncertainty.add_vv(),
			                         add_wjets=uncertainty.add_wjets(),
			                         add_qcd=uncertainty.add_qcd(),
			                         add_ggh_signal=args["higgs_masses"] if uncertainty.add_ggh() else [],
			                         add_vbf_signal=args["higgs_masses"] if uncertainty.add_qqh() else [],
			                         add_vh_signal=args["higgs_masses"] if uncertainty.add_vh() else []) if channel == "mt" else None
			
			for category in args["categories"]:
				if category == "None":
					category = None
			
				config = channel_settings.get_config(category=category) if channel == "mt" else jsonTools.JsonDict()
			
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
							                                          label_renamings.get(label, label))
					
					json_defaults = uncertainty(json_defaults, name).get_config(shift)
					
					if "PrintInfos" in json_defaults.get("analysis_modules", []):
						json_defaults.get("analysis_modules", []).remove("PrintInfos")
					
					harry_configs.append(json_defaults)
					harry_args.append("-d %s %s -f png pdf %s" % (args["input_dir"], ("" if json_exists else ("-x %s" % quantity)), args["args"]))
			
	higgs_plotter = higgsplot.HiggsPlotter(list_of_config_dicts=harry_configs, list_of_args_strings=harry_args, n_processes=args["n_processes"])
	
	root_outputs = list(set([output for output in tools.flattenList(higgs_plotter.output_filenames) if output.endswith(".root")]))
	logger.subprocessCall(shlex.split("hadd -f %s %s" % (args["root_output"], " ".join(root_outputs))))
	log.info("Merged ROOT output is saved to \"%s\"." % args["root_output"])

