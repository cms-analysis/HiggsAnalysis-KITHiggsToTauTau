# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import re


class JER(dict):
	def __init__(self, nickname):
		# disabled for data and embedded
		self["JEREnabled"] = False
		# MC
		if re.search("Fall17", nickname):
			#for now enable only for signal samples
			if re.search("HToTauTau", nickname) or re.search("H2JetsToTauTau", nickname):
				self["JEREnabled"] = True
			self["JERFile"] = "$CMSSW_BASE/src/Artus/KappaAnalysis/data/JRcorr/JR_Fall17_V3_102X_MC_AK4PFchs/Fall17_V3_MC_PtResolution_AK4PFchs.txt"
			self["JERScaleFactorFile"] = "$CMSSW_BASE/src/Artus/KappaAnalysis/data/JRcorr/JR_Fall17_V3_102X_MC_AK4PFchs/Fall17_V3_MC_SF_AK4PFchs.txt"
			self["JERVariation"] = 0 #+-1 for up/down shifts
		elif re.search("Summer16", nickname):
			#for now enable only for signal samples
			if re.search("HToTauTau", nickname) or re.search("H2JetsToTauTau", nickname):
				self["JEREnabled"] = True
			self["JERFile"] = "$CMSSW_BASE/src/Artus/KappaAnalysis/data/JRcorr/JR_Summer16_25nsV1_1_MC_AK4PFchs/Summer16_25nsV1_MC_PtResolution_AK4PFchs.txt"
			self["JERScaleFactorFile"] = "$CMSSW_BASE/src/Artus/KappaAnalysis/data/JRcorr/JR_Summer16_25nsV1_1_MC_AK4PFchs/Summer16_25nsV1_MC_SF_AK4PFchs.txt"
			self["JERVariation"] = 0 #+-1 for up/down shifts
		elif re.search("Autumn18", nickname):
			#for now enable only for signal samples
			if re.search("HToTauTau", nickname) or re.search("H2JetsToTauTau", nickname):
				self["JEREnabled"] = True
			self["JERFile"] = "$CMSSW_BASE/src/Artus/KappaAnalysis/data/JRcorr/JR_Autumn18_V7_MC_AK4PFchs/Autumn18_V7_MC_PtResolution_AK4PFchs.txt"
			self["JERScaleFactorFile"] = "$CMSSW_BASE/src/Artus/KappaAnalysis/data/JRcorr/JR_Autumn18_V7_MC_AK4PFchs/Autumn18_V7_MC_SF_AK4PFchs.txt"
			self["JERVariation"] = 0 #+-1 for up/down shifts
