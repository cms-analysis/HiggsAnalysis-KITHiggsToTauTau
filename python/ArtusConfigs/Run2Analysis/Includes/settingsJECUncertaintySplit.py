# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import re


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
			"ClosureEtaGrouping",
			"Closure"
		]
		self["JetEnergyCorrectionSplitUncertaintyGroupings"] = {
		"Eta0To5" :  [
			"AbsoluteFlavMap",
			"AbsoluteMPFBias",
			"AbsoluteScale",
			"AbsoluteStat",
			"FlavorQCD",
			"Fragmentation",
			"PileUpDataMC",
			"PileUpPtRef",		
			"RelativeFSR",
			"RelativeStatFSR",							
			"SinglePionECAL",
			"SinglePionHCAL",						
			"TimePtEta"					
			],
		"Eta0To3" : [
			"PileUpPtBB",
			"PileUpPtEC1",
			"PileUpPtEC2",
			"RelativeJEREC1",
			"RelativeJEREC2",
			"RelativePtBB",		
			"RelativePtEC1",
			"RelativePtEC2",
			"RelativeStatEC"							
			],
		"Eta3To5" : [
			"PileUpPtHF",
			"RelativeJERHF",			
			"RelativePtHF",
			"RelativeStatHF",
			]
		}
