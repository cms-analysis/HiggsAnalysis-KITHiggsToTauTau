#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import argparse
import os
import shlex

import HiggsAnalysis.KITHiggsToTauTau.plotting.higgsplot as higgsplot
from collections import OrderedDict


# disclaimer: VERY PRELIMINARY script (!!!), just an idea of how can be...
# run with: ./makePlots_controlPlots.py

# dictionary with datasets to be imported from external file
# dictionary (and included data/bkg/signal dictionaries) need to be ordered, because Harry is sensitive to the
# ordering of the parameters given via the command line

datasets = OrderedDict()

datasets["Data"] = OrderedDict()
datasets["Data"]["Data"] = {
			"samples" : [
				"/nfs/dust/cms/user/fcolombo/Data.root",
				#"/nfs/dust/cms/user/fcolombo/Data2.root",
				#"/nfs/dust/cms/user/fcolombo/Data3.root",
				#"/nfs/dust/cms/user/fcolombo/Data4.root"
				],
			"weight" : "weight",
			"color" : 1,
			"label" : "Data",
			"nick" : "Data",
			"stack" : "data"
		}
#datasets["Data"]["DataSecond"] = {
			#"samples" : [
				#"/nfs/dust/cms/user/fcolombo/Data.root",
				#],
			#"weight" : "weight",
			#"color" : 2,
			#"label" : "Data2",
			#"nick" : "Data",
			#"stack" : "data"
		#}
#datasets["Data"]["Third"] = {
			#"samples" : [
				#"/nfs/dust/cms/user/fcolombo/Data.root",
				#],
			#"weight" : "weight",
			#"color" : 3,
			#"label" : "Data3",
			#"nick" : "Data",
			#"stack" : "data"
		#}

datasets["Backgrounds"] = OrderedDict()
datasets["Backgrounds"]["DY"] = {
			"samples" : [
				"/nfs/dust/cms/user/fcolombo/DYJetsToLL_M_50_madgraph_8TeV.root",
				#"/nfs/dust/cms/user/fcolombo/DY1JetsToLL_M_50_madgraph_8TeV.root",
				#"/nfs/dust/cms/user/fcolombo/DY2JetsToLL_M_50_madgraph_8TeV.root",
				#"/nfs/dust/cms/user/fcolombo/DY3JetsToLL_M_50_madgraph_8TeV.root"
				],
			"weight" : "weight",
			"color" : 602,
			"label" : "DrellYan",
			"nick" : "DY",
			"stack" : "bkg"
		}
datasets["Backgrounds"]["WJets"] = {
			"samples" : ["/nfs/dust/cms/user/fcolombo/WJetsToLN_madgraph_8TeV.root"
				],
			"weight" : "weight",
			"color" : 634,
			"label" : "W+jets",
			"nick" : "WJets",
			"stack" : "bkg"
		}
datasets["Backgrounds"]["TTJets"] = {
			"samples" : ["/nfs/dust/cms/user/fcolombo/TTJets_madgraph_tauola_8TeV.root"
				],
			"weight" : "weight",
			"color" : 418,
			"label" : "tt+jets",
			"nick" : "TTJets",
			"stack" : "bkg"
		}

datasets["Signals"] = OrderedDict()



if __name__ == "__main__":

	parser = argparse.ArgumentParser(description="Make data-MC control plots.",
	                                 parents=[logger.loggingParser])
	parser.add_argument("--quantities", nargs="*",
	                    default=["inclusive",
	                             "pt_1", "eta_1", "phi_1", "m_1", "iso_1",
	                             "pt_2", "eta_2", "phi_2", "m_2", "iso_2",
	                             "mvis",
	                             "met", "metphi", "metcov00", "metcov01", "metcov10", "metcov11",
	                             "mvamet", "mvametphi", "mvacov00", "mvacov01", "mvacov10", "mvacov11",
	                             "jpt_1", "jeta_1", "jphi_1",
	                             "jpt_2", "jeta_2", "jphi_2",
	                             "njets", "mjj", "jdeta",
	                             "trigweight_1", "trigweight_2", "puweight",
	                             "npv", "npu", "rho"],
	                    help="Quantities. [Default: %(default)s]")
	
	args = vars(parser.parse_args())
	logger.initLogger(args)
	
	# lumi to be taken from settings, instead than hardcoded
	luminosity = 19000.0
	
	for channel in ["et"]:
		for quantity in args["quantities"]:
			json_exists = True
			json_config = os.path.expandvars("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/control_plots/%s_%s.json" % (channel, quantity))
			if not os.path.exists(json_config):
				json_exists = False
				json_config = os.path.expandvars("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/control_plots/%s_default.json" % (channel))
			
			filesString = ""
			weightsString = ""
			colorsString = ""
			labelsString = ""
			nickString = ""
			stackString = ""
			
			for iData in datasets["Data"]:
				dataDict = datasets["Data"][iData]
				for dataFile in dataDict["samples"]:
					filesString = filesString + "%s " % (dataFile)
					weightsString = weightsString + "%s " % (dataDict["weight"])
					colorsString = colorsString + "%s " % (dataDict["color"])
					labelsString = labelsString + "%s " % (dataDict["label"])
					nickString = nickString + "%s " % (dataDict["nick"])
					stackString = stackString + "%s " % (dataDict["stack"])
			
			for iBkg in datasets["Backgrounds"]:
				bkgDict = datasets["Backgrounds"][iBkg]
				for bkgFile in bkgDict["samples"]:
					filesString = filesString + "%s " % (bkgFile)
					weightsString = weightsString + "%s " % (str(luminosity)+"*"+bkgDict["weight"])
					colorsString = colorsString + "%s " % (bkgDict["color"])
					labelsString = labelsString + "%s " % (bkgDict["label"])
					nickString = nickString + "%s " % (bkgDict["nick"])
					stackString = stackString + "%s " % (bkgDict["stack"])
			
			for iSignal in datasets["Signals"]:
				sigDict = datasets["Signals"][iSignal]
				for sigFile in sigDict["samples"]:
					filesString = filesString + "%s " % (sigFile)
					weightsString = weightsString + "%s " % (str(luminosity)+"*"+sigDict["weight"])
					colorsString = colorsString + "%s " % (sigDict["color"])
					labelsString = labelsString + "%s " % (sigDict["label"])
					nickString = nickString + "%s " % (sigDict["nick"])
					stackString = stackString + "%s " % (sigDict["stack"])
			
			
			# build the config line sequence, connecting all the strings created above
			plot_args = "--json-defaults %s -i %s--weights %s--colors %s--labels %s--nicks %s--stack %s %s" % (json_config, filesString, weightsString, colorsString, labelsString, nickString, stackString, ("" if json_exists else ("-x %s" % quantity)))
			
			plot_args = os.path.expandvars(plot_args)
			print plot_args
			
			log.info("\nhiggsplot.py %s" % plot_args)
			higgsplot.higgs_plot(plot_args)

