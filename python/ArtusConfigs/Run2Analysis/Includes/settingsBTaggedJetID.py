# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import re


class BTaggedJet_ID(dict):
	def __init__(self, nickname):

		self["BTaggedJetID_documentation"] = ["https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsToTauTauWorking2016#b_tagging"]

		self["BTaggedJetCombinedSecondaryVertexName"] = "pfCombinedInclusiveSecondaryVertexV2BJetTags"

		if re.search("(Fall15MiniAODv2|Run2015D)", nickname):
			self["BTaggedJetCombinedSecondaryVertexMediumWP"] = 0.8
			self["BTaggerWorkingPoints"] = [
				"tight:0.935",
				"medium:0.800",
				"loose:0.460"
			]

		else:
			self["BTaggedJetCombinedSecondaryVertexMediumWP"] = 0.8484
			self["BTaggerWorkingPoints"] = [
				"tight:0.9535",
				"medium:0.8484",
				"loose:0.5426"
			]
		
		self["BTaggedJetAbsEtaCut"] = 2.4
		if re.search("(Fall15|Spring16)", nickname):
			self["ApplyBTagSF"] = False
		elif re.search("(Summer17|Embedding)", nickname):
			self["ApplyBTagSF"] = False
		else:
			self["ApplyBTagSF"] = True
		
		self["BTagSFMethod"] = "PromotionDemotion"

