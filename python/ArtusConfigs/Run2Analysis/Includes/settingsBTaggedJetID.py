# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import re


class BTaggedJet_ID(dict):
	def __init__(self, nickname):

		self["BTaggedJetID_documentation"] = ["https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsToTauTauWorking2016#b_tagging"]

		self["BTaggedJetCombinedSecondaryVertexName"] = "pfCombinedInclusiveSecondaryVertexV2BJetTags" #TODO might change to deepbtagger
		self["BTagger"] = "pfCombinedInclusiveSecondaryVertexV2BJetTags"

		if re.search("(Fall15MiniAODv2|Run2015D)", nickname):
			self["BTaggedJetCombinedSecondaryVertexMediumWP"] = 0.8
			self["BTaggerWorkingPoints"] = [
				"tight:0.935",
				"medium:0.800",
				"loose:0.460"
			]
			self["BTaggedJetAbsEtaCut"] = 2.4

		if re.search("Run201(6|7|8)|Summer1(6|7)|Fall17|Autumn18|Embedding201(6|7|8)", nickname):
			self["BTagger"] = "deepcsv"
			self["BTaggedJetCombinedSecondaryVertexName"] = "pfDeepCSVDiscriminatorsJetTagsBvsAll"

			self["BTaggedJetDdeepCSVName"]= "pfDeepCSVDiscriminatorsJetTagsBvsAll"

			if re.search("Run2016|Summer16|Embedding2016", nickname):
				self["BTaggedJetCombinedSecondaryVertexMediumWP"] = 0.6321
				self["BTaggerWorkingPoints"] = [
					"tight:0.8953",
					"medium:0.6321",
					"loose:0.2217"
				]
			elif re.search("Run2017|Fall17|Embedding2017", nickname):
				self["BTaggedJetCombinedSecondaryVertexMediumWP"] = 0.4941
				self["BTaggerWorkingPoints"] = [
					"tight:0.8001",
					"medium:0.4941",
					"loose:0.1522"
				]
			elif re.search("Run2018|Autumn18|Embedding2018", nickname):
				self["BTaggedJetCombinedSecondaryVertexMediumWP"] = 0.4184
				self["BTaggerWorkingPoints"] = [
					"tight:0.7527",
					"medium:0.4184",
					"loose:0.1241"
				]


			self["BTaggedJetAbsEtaCut"] = 2.4
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

