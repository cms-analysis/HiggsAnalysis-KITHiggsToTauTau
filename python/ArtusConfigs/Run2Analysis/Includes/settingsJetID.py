# -*- coding: utf-8 -*-

import logging
import re
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)


class Jet_ID(dict):
	def __init__(self, nickname):
		self["JetID"] = "loose"
		if re.search("Run2016|Spring16|Summer16|Embedding2016", nickname):
			self["JetIDVersion"] = "2016"
		else:
			self["JetIDVersion"] = "2015" 

		self["PuJetIDs"] = []
		self["PuJetIDFullDiscrName"] = "pileupJetIdfullDiscriminant"
		self["JetTaggerLowerCuts"] = []
		self["JetTaggerUpperCuts"] = []
	
		self["JetLowerPtCuts"] = ["20.0"]
		self["JetUpperAbsEtaCuts"] = ["4.7"]
	
		self["JetLeptonLowerDeltaRCut"] = 0.5
