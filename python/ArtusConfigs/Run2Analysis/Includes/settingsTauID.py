# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import re


class Tau_ID(dict):
	def __init__(self, nickname):

		self["TauID_documentation"] = []
		if re.search("(Run2017|Fall17|Embedding2017)", nickname):
			self["TauDiscriminatorIsolationName"] = "byDeepTau2017v2p1VSjetraw"
			self["TauIDType"] = "deepTau"
			self["TauAllowedDMs"] = [0,1,2,10,11] # exclude DM 5 and 6
			self["TauUseOldDMs"] = False
			self["TauDiscriminators"] = {"byVVVLooseDeepTau2017v2p1VSjet", "byVVVLooseDeepTau2017v2p1VSe", "byVLooseDeepTau2017v2p1VSmu"}
		else:
			self["TauDiscriminatorIsolationName"] = "byIsolationMVArun2v1DBoldDMwLTraw"
			self["TauIDType"] = ""
			self["TauAllowedDMs"] = [0,1,2,10] # old DMs
			self["TauUseOldDMs"] = True

		self["TauElectronLowerDeltaRCut"] = -1.0
		self["TauMuonLowerDeltaRCut"] = -1.0

		self["TauID"] = "TauIDRecommendation13TeV"
