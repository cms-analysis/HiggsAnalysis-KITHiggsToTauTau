# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import re


class JEC(dict):
	def __init__(self, nickname):
		if re.search("(Summer17)",nickname):
			self["JetEnergyCorrectionUncertaintyParameters"] = ""
		elif re.search("(Run2017)", nickname):
			self["JetEnergyCorrectionUncertaintyParameters"] = ""
		elif re.search("(Run2016|Spring16|Summer16)", nickname):
			self["JetEnergyCorrectionUncertaintyParameters"] =  "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Summer16/Summer16_23Sep2016V4_DATA_UncertaintySources_AK4PFchs.txt"
		#elif re.search("Run2016|Embedding2016", nickname):
		#	self["JetEnergyCorrectionUncertaintyParameters"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Summer16/Summer16_23Sep2016V4_DATA_Uncertainty_AK4PFchs.txt"	
		elif re.search("(Fall15MiniAODv2)", nickname):
			self["JetEnergyCorrectionUncertaintyParameters"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Fall15/Fall15_25nsV2_MC_Uncertainty_AK4PFchs.txt"
		elif re.search("(Run2015|Embedding2015)", nickname):
			self["JetEnergyCorrectionUncertaintyParameters"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Fall15/Fall15_25nsV2_DATA_Uncertainty_AK4PFchs.txt"
		
		self["JetEnergyCorrectionUncertaintySource"] = "Total"
		#self["JetEnergyCorrectionUncertaintyShift"] = 0.0
		
		#All commented out
		
		if re.search("Run2015|Embedding2016", nickname):
			self["JetEnergyCorrectionParameters"] = [
					"#$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Fall15/Fall15_25nsV2_DATA_L1FastJet_AK4PFchs.txt",
					"#$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Fall15/Fall15_25nsV2_DATA_L2Relative_AK4PFchs.txt",
					"#$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Fall15/Fall15_25nsV2_DATA_L3Absolute_AK4PFchs.txt",
					"#$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Fall15/Fall15_25nsV2_DATA_L2L3Residual_AK4PFchs.txt"
				]

		else:
			self["JetEnergyCorrectionParameters"] = ["#$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Fall15/Fall15_25nsV2_MC_L1FastJet_AK4PFchs.txt",
					"#$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Fall15/Fall15_25nsV2_MC_L2Relative_AK4PFchs.txt",
					"#$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/jec/Fall15/Fall15_25nsV2_MC_L3Absolute_AK4PFchs.txt"
				]
	
		








