# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import re


class Kappa(dict):
	def __init__(self, nickname, legacy=True):
		if re.search("(?<!PFembedded).Run201", nickname):
			self["GenParticles"] = ""
			self["GenTaus"] = ""
			self["GenTauJets"] = ""
			self["GenMet"] = ""
			self["GenJets"] = ""
		else:
			self["GenParticles"] = "genParticles"
			self["GenTaus"] = "genTaus"
			self["GenTauJets"] = "tauGenJets"  # * default is set here
			self["GenMet"] = "genmetTrue"
			#for now GenJets presnt only in signal samples
			if re.search("HToTauTau", nickname) or re.search("H2JetsToTauTau", nickname):
				self["GenJets"] = "genJets"
			else:
				self["GenJets"] = ""

		self["Electrons"] = "electrons"
		self["ElectronMetadata"] = "electronMetadata"
		self["Muons"] = "muons"
		self["Taus"] = "taus"
		self["TauMetadata"] = "taus"

		if re.search("8TeV", nickname):
			self["GenTauJets"] = ""   #* watch out default is set before
			self["TaggedJets"] = "AK5PFTaggedJets"
			self["PileupDensity"] = "KT6Area"

		elif re.search("13TeV.*_AODSIM", nickname):
			self["TaggedJets"] = "AK5PFTaggedJets"

		elif re.search("MINIAOD", nickname):
			self["TaggedJets"] = "ak4PF"
		elif re.search("USER",nickname):
			self["TaggedJets"] = "ak4PF"

		if re.search("13TeV", nickname):
			self["PileupDensity"] = "pileupDensity"

		self["Met"] = "met"

		if re.search("(16Dec2015v1|Fall15|Spring16|Run2015)", nickname):
			self["PuppiMet"] = "metPuppi"
		else:
			self["PuppiMet"] = "metPuppi"

		if legacy:
			self["MvaMets"] = ""
		else:
			self["MvaMets"] = "MVAMET"

		#self["PFChargedHadronsPileUp"] = "pfPileUpChargedHadrons"
		##self["PFChargedHadronsNoPileUp"] = "pfNoPileUpChargedHadrons"
		#self["PFChargedHadronsNoPileUp"] = "pfAllChargedParticles"
		#self["PFNeutralHadronsNoPileUp"] = "pfNoPileUpNeutralHadrons"
		#self["PFPhotonsNoPileUp"] = "pfNoPileUpPhotons"
		#self["PackedPFCandidates"] = "packedPFCandidates"
		self["BeamSpot"] = "offlineBeamSpot"
		self["VertexSummary"] = "goodOfflinePrimaryVerticesSummary"
		self["EventInfo"] = "eventInfo"
		self["LumiInfo"] = "lumiInfo"
		self["RunInfo"] = "runInfo"
		self["GenEventInfoMetadata"] = "genEventInfoMetadata"
		self["FilterMetadata"] = ""
		self["FilterSummary"] = ""
		self["JetMetadata"] = "jetMetadata"
		self["BeamSpot"] = "offlineBeamSpot"
		self["TriggerInfos"] = "triggerObjectMetadata"
		self["TriggerObjects"] = "triggerObjects"
