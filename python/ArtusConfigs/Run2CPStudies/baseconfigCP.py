# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import re
import json
import os
import Artus.Utility.jsonTools as jsonTools
import Kappa.Skimming.datasetsHelperTwopz as datasetsHelperTwopz

import HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Run2Analysis.Includes.Run2Quantities as r2q
import HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Run2CPStudies.Includes.Run2CPQuantities as r2cpq

import HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Run2Analysis.baseconfig as smbaseconfig

import HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Includes.settingsTauSpinner as sTauSpinner
import HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Run2CPStudies.Includes.settingsMadGraphReweighting as sMGReweighting

class Baseconfig_cp(smbaseconfig.Baseconfig):

	def __init__(self, nickname):
		self.datasetsHelper = datasetsHelperTwopz.datasetsHelperTwopz(os.path.expandvars("$CMSSW_BASE/src/Kappa/Skimming/data/datasets.json")) 
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
	
	
		isData = self.datasetsHelper.isData(nickname)
		isSignal = self.datasetsHelper.isSignal(nickname)
		isEmbedding = self.datasetsHelper.isEmbedded(nickname)
		isTTbar = re.match("TT(To|_|Jets)", nickname)
		isDY = re.match("DY.?JetsToLLM(50|150)", nickname)
		isWjets = re.match("W.?JetsToLNu", nickname)
		isLFV = ("LFV" in nickname)
		is2015 = re.search("(Run2015|Fall15|Embedding15)",nickname) #I am not 100% sure if this is exclusive
		is2016 = re.search("(Run2016|Sprint16|Summer16|Fall16|Embedding16)",nickname) #I am not 100% sure if this is exclusive	
		is2017 = re.search("(Run2017|Summer17|Fall17|Embedding17)",nickname) #I am not 100% sure if this is exclusive		
		

		if re.search("(Fall15MiniAODv2|Run2015)", nickname):
			self["RefitVertices"] = ""
			self["RefitBSVertices"] = ""
		else:
			self["RefitVertices"] = "AdvancedRefittedVerticesNoBS"
			self["RefitBSVertices"] = "AdvancedRefittedVerticesBS"
		if isSignal or isLFV: 
			self["LheParticles"] = "LHEafter"
		else:
			self["LheParticles"] = ""

