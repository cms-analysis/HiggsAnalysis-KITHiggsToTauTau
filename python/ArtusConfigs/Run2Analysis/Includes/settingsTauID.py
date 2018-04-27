# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import re


class Tau_ID(dict):
	def __init__(self, nickname):

		self["TauID_documentation"] = []
		if re.search("(Run2017|Fall17)", nickname):
			self["TauDiscriminatorIsolationName"] = "byIsolationMVArun2017v2DBoldDMwLTraw2017"
		else:
			self["TauDiscriminatorIsolationName"] = "byIsolationMVArun2v1DBoldDMwLTraw"

		self["TauElectronLowerDeltaRCut"] = -1.0
		self["TauMuonLowerDeltaRCut"] = -1.0

