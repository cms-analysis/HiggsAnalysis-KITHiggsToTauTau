# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import re

import HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Run2Analysis.baseconfig as smbaseconfig
import HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Includes.settingsTauSpinner as sTauSpinner
import HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Run2CPStudies.Includes.settingsMadGraphReweighting as sMGReweighting


class Baseconfig_cp(smbaseconfig.Baseconfig):

	def __init__(self, nickname):
		"""
		self["include"] = ["$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/ArtusConfigs/Run2Analysis/baseConfig.json",
		"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/ArtusConfigs/Includes/settingsTauSpinner.json",
		"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/ArtusConfigs/Run2CPStudies/Includes/settingsMadGraphReweighting.json"   #TODO
		]
		"""
		super(Baseconfig_cp, self).__init__(nickname)
		TauSpinner_config = sTauSpinner.TauSpinner(nickname)
		self.update(TauSpinner_config)

		MadGraphReweighting_config = sMGReweighting.MadGraphReweighting(nickname)
		self.update(MadGraphReweighting_config)
		#self["RunWhitelist"] = [1]
		#self["LumiWhitelist"] = [194]
		#self["EventWhitelist"] = [38756]
		
		if re.search("(Fall15MiniAODv2|Run2015)", nickname) or re.search("(Run2017|Summer17|Fall17)", nickname):
			self["RefitVertices"] = ""
			self["RefitBSVertices"] = ""
		else:
			self["RefitVertices"] = "AdvancedRefittedVerticesNoBS"
			self["RefitBSVertices"] = "AdvancedRefittedVerticesBS"
		if re.search("HToTauTau|H2JetsToTauTau|Higgs|DY.?JetsToLLM(10to50|50|150)|LFV", nickname):
			self["LheParticles"] = "LHEafter"
		else:
			self["LheParticles"] = ""
		
		self["GenCollectionToPrint"] = "LHE"

