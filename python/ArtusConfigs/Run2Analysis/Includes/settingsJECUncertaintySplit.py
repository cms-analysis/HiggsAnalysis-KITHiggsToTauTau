# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import re
import json
import Artus.Utility.jsonTools as jsonTools
import Kappa.Skimming.datasetsHelperTwopz as datasetsHelperTwopz
import copy

class JECUncertaintySplit(dict):
	def __init__(self, nickname):
		if re.search("(Run2016|Spring16|Summer16)", nickname):
			self["JetEnergyCorrectionSplitUncertainty"] = True
		else: 
			self["JetEnergyCorrectionSplitUncertainty"] = False


		if re.search("(Run201|Embedding)", nickname):
			self["AbsJetEnergyCorrectionSplitUncertaintyShift"] = 0.0
		else:
			self["AbsJetEnergyCorrectionSplitUncertaintyShift"] = 1.0

		self["JetEnergyCorrectionSplitUncertaintyParameterNames"] = [
									"AbsoluteFlavMap",
									"AbsoluteMPFBias",
									"AbsoluteScale",
									"AbsoluteStat",
									"FlavorQCD",
									"Fragmentation",
									"PileUpDataMC",
									"PileUpPtBB",
									"PileUpPtEC1",
									"PileUpPtEC2",
									"PileUpPtHF",
									"PileUpPtRef",
									"RelativeBal",
									"RelativeFSR",
									"RelativeJEREC1",
									"RelativeJEREC2",
									"RelativeJERHF",
									"RelativePtBB",
									"RelativePtEC1",
									"RelativePtEC2",
									"RelativePtHF",
									"RelativeStatEC",
									"RelativeStatFSR",
									"RelativeStatHF",
									"SinglePionECAL",
									"SinglePionHCAL",
									"TimePtEta",
									"Total",
									"Closure"
								]









