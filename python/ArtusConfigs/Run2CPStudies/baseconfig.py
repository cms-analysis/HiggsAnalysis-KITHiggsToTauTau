# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import re
import json
import Artus.Utility.jsonTools as jsonTools
import Kappa.Skimming.datasetsHelperTwopz as datasetsHelperTwopz

import HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Run2Analysis.Includes.Run2Quantities as r2q
import HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Run2CPStudies.Includes.Run2CPQuantities as r2cpq

class Baseconfig_tt(dict):

	def __init__(self, nickname):
		self.datasetsHelper = datasetsHelperTwopz.datasetsHelperTwopz("Kappa/Skimming/data/datasets.json") 
		self["include"] = ["$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/ArtusConfigs/Run2Analysis/baseConfig.json",
		"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/ArtusConfigs/Includes/settingsTauSpinner.json",
		"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/ArtusConfigs/Run2CPStudies/Includes/settingsMadGraphReweighting.json"
		] 	
		#self["RunWhitelist"] = [1]
		#self["LumiWhitelist"] = [194]
		self["EventWhitelist"] = [38756]
	
	
		isData = self.datasetsHelper.isData(nickname)
		isSignal = self.datasetsHelper.isSignal(nickname)
		isEmbedding = self.datasetsHelper.isEmbedded(nickname)
		isTTbar = re.match("TT(To|_|Jets)", nickname)
		isDY = re.match("DY.?JetsToLLM(50|150)", nickname)
		isWjets = re.match("W.?JetsToLNu", nickname)
		isLFV = ("LFV" in nickname)
		is2015 = re.match("(Run2015|Fall15|Embedding15)*?",nickname) #I am not 100% sure if this is exclusive
		is2016 = re.match("(Run2016|Sprint16|Summer16|Fall16|Embedding16)*?",nickname) #I am not 100% sure if this is exclusive	
		is2017 = re.match("(Run2017|Summer17|Embedding17)*?",nickname) #I am not 100% sure if this is exclusive		
		

		if (isData and is2015) or is2015:
			self["RefitVertices"] = ""
			self["RefitBSVertices"] = ""
		else:
			self["RefitVertices"] = "AdvancedRefittedVerticesNoBS"
			self["RefitBSVertices"] = "AdvancedRefittedVerticesBS"
		if isSignal or isLFV: 
			self["LheParticles"] = "LHEafter"
		else:
			self["LheParticles"] = ""

