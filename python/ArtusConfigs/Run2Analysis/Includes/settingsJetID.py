# -*- coding: utf-8 -*-

import logging
import re
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)


class Jet_ID(dict):
	def __init__(self, nickname):
		if re.search("(Fall17|Run2017|Embedding2017)", nickname):
			# self["JetID"] = "Tight"
			self["JetID"] = "tight"
			self["JetIDVersion"] = "2017"
		elif re.search("Run2016|Spring16|Summer16", nickname):
			self["JetIDVersion"] = "2016"
			self["JetID"] = "loose"
		else:
			self["JetID"] = "loose"
			self["JetIDVersion"] = "2015"

		self["PuJetIDs"] = []
		self["PuJetID"] = "loose"
		self["PuJetIDVersion"] = "2016" # TODO: implement 2017 and 2018 WPs; not avalaible yet https://twiki.cern.ch/twiki/bin/view/CMS/PileupJetID#Working_points
		self["PuJetIDFullDiscrName"] = "pileupJetIdfullDiscriminant"
		# self["PuJetIDFullDiscrName"] = "pileupJetIdUpdatedfullDiscriminant"
		self["JetTaggerLowerCuts"] = []
		self["JetTaggerUpperCuts"] = []

		self["JetLowerPtCuts"] = ["20.0"]
		self["JetUpperAbsEtaCuts"] = ["4.7"]

		self["JetLeptonLowerDeltaRCut"] = 0.5
