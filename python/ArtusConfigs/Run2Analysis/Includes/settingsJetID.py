# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import re


class Jet_ID(dict):
	def __init__(self, nickname):
		if re.search("(Fall17|Run2017)", nickname):
			self["JetID"] = "Tight"
			self["JetIDVersion"] = "2017"
		else:
			self["JetID"] = "loose"
			self["JetIDVersion"] = "2015"

		self["PuJetIDs"] = []
		self["PuJetIDFullDiscrName"] = "pileupJetIdfullDiscriminant"
		self["JetTaggerLowerCuts"] = []
		self["JetTaggerUpperCuts"] = []
	
		self["JetLowerPtCuts"] = ["20.0"]
		self["JetUpperAbsEtaCuts"] = ["4.7"]
	
		self["JetLeptonLowerDeltaRCut"] = 0.5
