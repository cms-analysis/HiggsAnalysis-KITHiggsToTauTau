# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import re


class JECUncertaintySplit(dict):
	def __init__(self, nickname):
		self["JetEnergyCorrectionSplitUncertainty"] = False
		self["JetEnergyCorrectionSplitUncertaintyParameterNames"] = []
		if re.search("(Run201|Embedding)", nickname):
			self["AbsJetEnergyCorrectionSplitUncertaintyShift"] = 0.0
		else:
			self["AbsJetEnergyCorrectionSplitUncertaintyShift"] = 1.0
		if re.search("(Run2017|Fall17)", nickname):
			self["JetsCorrectedInKappa"] = True
		else:
			self["JetsCorrectedInKappa"] = False

		self["JetEnergyCorrectionCorrelationMap"] = [
			"AbsoluteFlavMap:0.",
			"AbsoluteMPFBias:1.",
			"AbsoluteScale:1.",
			"AbsoluteStat:0.",
			"FlavorQCD:1.",
			"Fragmentation:1.",
			"PileUpDataMC:0.5",
			"PileUpPtBB:0.5",
			"PileUpPtEC1:0.5",
			"PileUpPtEC2:0.5",
			"PileUpPtHF:0.5",
			"PileUpPtRef:0.5",
			"RelativeFSR:0.5",
			"RelativeJEREC1:0.",
			"RelativeJEREC2:0.",
			"RelativeJERHF:0.5",
			"RelativePtBB:0.5",
			"RelativePtEC1:0.",
			"RelativePtEC2:0.",
			"RelativePtHF:0.5",
			"RelativeBal:0.5",
			"RelativeSample:0.",
			"RelativeStatEC:0.",
			"RelativeStatFSR:0.",
			"RelativeStatHF:0.",
			"SinglePionECAL:1.",
			"SinglePionHCAL:1.",
			"TimePtEta:0"
		]
		print len(self["JetEnergyCorrectionCorrelationMap"])

	def group_eta0to5(self):
		self["JetEnergyCorrectionSplitUncertainty"] = True
		self["JetEnergyCorrectionSplitUncertaintyParameterNames"] = [
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
		]

	def group_eta0to3(self):
		self["JetEnergyCorrectionSplitUncertainty"] = True
		self["JetEnergyCorrectionSplitUncertaintyParameterNames"] = [
			"PileUpPtBB",
			"PileUpPtEC1",
			"PileUpPtEC2",
			"RelativeJEREC1",
			"RelativeJEREC2",
			"RelativePtBB",		
			"RelativePtEC1",
			"RelativePtEC2",
			"RelativeStatEC"							
		]
	def group_eta3to5(self):
		self["JetEnergyCorrectionSplitUncertainty"] = True
		self["JetEnergyCorrectionSplitUncertaintyParameterNames"] = [
			"PileUpPtHF",
			"RelativeJERHF",			
			"RelativePtHF",
			"RelativeStatHF",
		]

	def group_relativebal(self):
		self["JetEnergyCorrectionSplitUncertainty"] = True
		self["JetEnergyCorrectionSplitUncertaintyParameterNames"] = [
			"RelativeBal"
		]

		
	def group_relativesample(self):
		self["JetEnergyCorrectionSplitUncertainty"] = True
		self["JetEnergyCorrectionSplitUncertaintyParameterNames"] = [
			"RelativeSample"
		]

	"""



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
			"Total"
		]
		
		# WARNING: Do not forget to add new jet Energy Correction Groupings as Quantities to Run2Quantities.py! 
		# WARNING: Do not forget to add new jet Energy Correction uncertainty names in HttEnumTypes.h! 
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
			],
			"Closure" : [
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
				"TimePtEta"
			],
			"ClosureCPGroupings" : [
				"RelativeBal",
				"Eta0To5",
				"Eta0To3",
				"Eta3To5"
			]
		}
	"""
