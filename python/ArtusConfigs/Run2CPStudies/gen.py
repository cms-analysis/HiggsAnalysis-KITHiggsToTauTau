# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import re
import copy
import os

from HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Run2CPStudies.quantities import Quantities
from HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Includes.processorOrdering import ProcessorsOrdered

import HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Run2Analysis.Includes.settingsJetID as sJID
import HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Run2Analysis.Includes.settingsBTaggedJetID as sBTJID
import HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Run2Analysis.Includes.settingsTauES as sTES
import HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Run2Analysis.Includes.settingsJEC as sJEC

import Kappa.Skimming.datasetsHelperTwopz as datasetsHelperTwopz

class gen_ArtusConfig(dict):

	def __init__(self):
		pass

	def addProcessors(self, nickname):
		self["Processors"] = []
		if re.search("Summer17|Fall17|Embedding2017", nickname):
			self["Processors"] += [
				"producer:HltProducer",
				"producer:GenParticleProducer",
				"producer:GenBosonFromGenParticlesProducer",
				"producer:GenBosonDiLeptonDecayModeProducer",
				# "producer:GenBosonProductionProducer",
				"producer:GenDiLeptonDecayModeProducer",
				"producer:GenTauDecayProducer",
				"producer:GenTauCPProducer",
				]

		if re.search("HToTauTau|H2JetsToTauTau|Higgs",nickname):
			self["Processors"] += [
				"producer:TaggedJetCorrectionsProducer",
				"producer:ValidTaggedJetsProducer",
				"#producer:ValidBTaggedJetsProducer",
				"producer:DiJetQuantitiesProducer",
				"producer:CPInitialStateQuantitiesProducer"
			]

	def build_config(self, nickname, *args, **kwargs):

		datasetsHelper = datasetsHelperTwopz.datasetsHelperTwopz(os.path.expandvars("$CMSSW_BASE/src/Kappa/Skimming/data/datasets.json"))

		# define frequently used conditions
		isEmbedded = datasetsHelper.isEmbedded(nickname)
		isData = datasetsHelper.isData(nickname) and (not isEmbedded)

		JEC_config = sJEC.JEC(nickname)  #Is already in baseconfig, for now leave it in; possibly remove it
		self.update(JEC_config)

		JetID_config = sJID.Jet_ID(nickname)
		self.update(JetID_config)

		BTaggedJet_config = sBTJID.BTaggedJet_ID(nickname)
		self.update(BTaggedJet_config)

		self["Channel"] = "GEN"
		self["EventWeight"] = "eventWeight"

		self["Consumers"] = [
			"cutflow_histogram",
			"KappaLambdaNtupleConsumer",
			"#RunTimeConsumer",
			"#PrintEventsConsumer",
			"#PrintGenParticleDecayTreeConsumer"
			]

		if re.search("Summer17|Fall17|Embedding2017", nickname):
			self["HltPaths"] = [
					#Electrontriggers
					"HLT_Ele32_WPTight_Gsf",
					"HLT_Ele35_WPTight_Gsf",
					"HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTau30_eta2p1_CrossL1",
					#Muontriggers
					"HLT_IsoMu24",
					"HLT_IsoMu27", #only in data recommended
					"HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1",
					#tautau
					"HLT_DoubleTightChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg",
					"HLT_DoubleMediumChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg",
					"HLT_DoubleTightChargedIsoPFTau40_Trk1_eta2p1_Reg"
				]
			
			self["DiTauPairHltPathsWithoutCommonMatchRequired"] = [
					#electron
					"HLT_Ele32_WPTight_Gsf_v",
					"HLT_Ele35_WPTight_Gsf_v",
					"HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTau30_eta2p1_CrossL1_v",
					#Muon
					"HLT_IsoMu24_v",
					"HLT_IsoMu27_v",
					"HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1_v",
					#tautau
					"HLT_DoubleTightChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg_v",
					"HLT_DoubleMediumChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg_v",
					"HLT_DoubleTightChargedIsoPFTau40_Trk1_eta2p1_Reg_v"
				]

		if re.search("HToTauTau|H2JetsToTauTau|Higgs",nickname):
			if re.search("amcatnlo",nickname):
				self["DoLhenpNLO"] = True	#NEEDED for stitching

		quantities_set = Quantities()
		quantities_set.build_quantities(nickname, channel = self["Channel"])
		self["Quantities"] = list(quantities_set.quantities)

		self.addProcessors(nickname)
