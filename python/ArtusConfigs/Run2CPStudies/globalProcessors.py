# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import re
import json
import Artus.Utility.jsonTools as jsonTools
import Kappa.Skimming.datasetsHelperTwopz as datasetsHelperTwopz
import copy 

class globalProccesors(dict):
	def __init__(self, nickname):
		print 'init'
		if re.search("(DY.?JetsToLLM(10to50|50|150))", nickname):
			self["Processors"] = [
				"#producer:PrintGenParticleDecayTreeProducer",
				"#filter:RunLumiEventFilter",
				"producer:GenBosonFromGenParticlesProducer",
				"producer:GenBosonDiLeptonDecayModeProducer",
				"producer:ValidGenTausProducer",
				"producer:GenDiLeptonDecayModeProducer",
				"#producer:LHEDiLeptonDecayModeProducer",
				"producer:GenDiLeptonDecayModeLFVProducer",
				"producer:GenParticleProducer",
				"producer:RecoElectronGenParticleMatchingProducer",
				"producer:RecoElectronGenTauMatchingProducer",
				"producer:RecoMuonGenParticleMatchingProducer",
				"producer:RecoMuonGenTauMatchingProducer",
				"producer:RecoTauGenParticleMatchingProducer",
				"producer:RecoTauGenTauMatchingProducer",
				"producer:MatchedLeptonsProducer",
				"producer:GenTauDecayProducer",
				"producer:GenTauCPProducer",
				"producer:TauSpinnerProducer",
				"#producer:TaggedJetCorrectionsProducer",
				"producer:NicknameProducer",
				"producer:CrossSectionWeightProducer",
				"producer:GeneratorWeightProducer",
				"producer:NumberGeneratedEventsWeightProducer",
				"producer:PUWeightProducer",
				"producer:ScaleVariationProducer",
				"#filter:RunLumiEventFilter",
				"#filter:MetFilter"
			]

		elif re.search("LFV", nickname):
			self["Processors"] = [
				"#producer:PrintGenParticleDecayTreeProducer",
				"#filter:RunLumiEventFilter",
				"producer:GenBosonFromGenParticlesProducer",
				"producer:GenBosonDiLeptonDecayModeProducer",
				"producer:ValidGenTausProducer",
				"producer:GenDiLeptonDecayModeProducer",
				"producer:LHEDiLeptonDecayModeProducer",
				"producer:GenDiLeptonDecayModeLFVProducer",
				"producer:GenParticleProducer",
				"producer:RecoElectronGenParticleMatchingProducer",
				"producer:RecoElectronGenTauMatchingProducer",
				"producer:RecoMuonGenParticleMatchingProducer",
				"producer:RecoMuonGenTauMatchingProducer",
				"producer:RecoTauGenParticleMatchingProducer",
				"producer:RecoTauGenTauMatchingProducer",
				"producer:MatchedLeptonsProducer",
				"producer:GenTauDecayProducer",
				"producer:GenTauCPProducer",
				"producer:TauSpinnerProducer",
				"#producer:TaggedJetCorrectionsProducer",
				"producer:NicknameProducer",
				"producer:CrossSectionWeightProducer",
				"producer:GeneratorWeightProducer",
				"producer:NumberGeneratedEventsWeightProducer",
				"producer:PUWeightProducer",
				"#producer:ScaleVariationProducer",
				"#filter:RunLumiEventFilter",
				"#filter:MetFilter"
			]

		elif re.search("Run201",nickname):
			self["Processors"] = [
				"#producer:PrintGenParticleDecayTreeProducer",
				"#filter:RunLumiEventFilter",
				"#filter:MetFilter",
				"filter:JsonFilter",
				"#producer:TaggedJetCorrectionsProducer",
				"producer:NicknameProducer"
			]
	
		elif re.search("Embedding201", nickname):
			self["Processors"] = [
				"#producer:PrintGenParticleDecayTreeProducer",
				"#filter:RunLumiEventFilter",
				"#filter:MetFilter",
				"filter:JsonFilter",
				"producer:NicknameProducer",
				"producer:GenParticleProducer",
				"producer:RecoElectronGenParticleMatchingProducer",
				"producer:RecoElectronGenTauMatchingProducer",
				"producer:RecoMuonGenParticleMatchingProducer",
				"producer:RecoMuonGenTauMatchingProducer",
				"producer:RecoTauGenParticleMatchingProducer",
				"producer:RecoTauGenTauMatchingProducer",
				"producer:MatchedLeptonsProducer",
				"#producer:TaggedJetCorrectionsProducer",
				"producer:CrossSectionWeightProducer",
				"producer:GeneratorWeightProducer",
				"producer:NumberGeneratedEventsWeightProducer"
			]

		elif re.search("EmbeddingMC", nickname):
			self["Processors"] =[
				"#producer:PrintGenParticleDecayTreeProducer",
				"#filter:RunLumiEventFilter",
				"#filter:MetFilter",
				"#filter:JsonFilter",
				"producer:NicknameProducer",
				"producer:GenParticleProducer",
				"producer:RecoElectronGenParticleMatchingProducer",
				"producer:RecoElectronGenTauMatchingProducer",
				"producer:RecoMuonGenParticleMatchingProducer",
				"producer:RecoMuonGenTauMatchingProducer",
				"producer:RecoTauGenParticleMatchingProducer",
				"producer:RecoTauGenTauMatchingProducer",
				"producer:MatchedLeptonsProducer",
				"#producer:TaggedJetCorrectionsProducer",
				"producer:CrossSectionWeightProducer",
				"producer:GeneratorWeightProducer",
				"producer:NumberGeneratedEventsWeightProducer"
			]

		elif re.search("(HToTauTau|H2JetsToTauTau|Higgs)",nickname):
			self["Processors"] = [
				"#producer:PrintGenParticleDecayTreeProducer",
				"#filter:RunLumiEventFilter",
				"producer:GenBosonFromGenParticlesProducer",
				"producer:GenBosonDiLeptonDecayModeProducer",
				"producer:GenBosonProductionProducer",
				"producer:ValidGenTausProducer",
				"producer:GenDiLeptonDecayModeProducer",
				"producer:GenParticleProducer",
				"producer:RecoElectronGenParticleMatchingProducer",
				"producer:RecoMuonGenParticleMatchingProducer",
				"producer:RecoTauGenParticleMatchingProducer",
				"producer:RecoElectronGenTauMatchingProducer",
				"producer:RecoMuonGenTauMatchingProducer",
				"producer:RecoTauGenTauMatchingProducer",
				"producer:MatchedLeptonsProducer",
				"producer:GenTauDecayProducer",
				"producer:GenTauCPProducer",
				"producer:GenHiggsCPProducer",
				"producer:TauSpinnerProducer",
				"#producer:TaggedJetCorrectionsProducer",
				"producer:NicknameProducer",
				"producer:CrossSectionWeightProducer",
				"producer:GeneratorWeightProducer",
				"producer:NumberGeneratedEventsWeightProducer",
				"producer:PUWeightProducer",
				"producer:ScaleVariationProducer",
				"filter:MetFilter"
			]
		else:
			self["Processors"] = [
				"#producer:PrintGenParticleDecayTreeProducer",
				"#filter:RunLumiEventFilter",
				"producer:NicknameProducer",
				"producer:GenParticleProducer",
				"producer:RecoElectronGenParticleMatchingProducer",
				"producer:RecoElectronGenTauMatchingProducer",
				"producer:RecoMuonGenParticleMatchingProducer",
				"producer:RecoMuonGenTauMatchingProducer",
				"producer:RecoTauGenParticleMatchingProducer",
				"producer:RecoTauGenTauMatchingProducer",
				"producer:MatchedLeptonsProducer",
				"#producer:TaggedJetCorrectionsProducer",
				"producer:CrossSectionWeightProducer",
				"producer:GeneratorWeightProducer",
				"producer:NumberGeneratedEventsWeightProducer",
				"producer:PUWeightProducer",
				"#producer:ScaleVariationProducer",
				"#filter:MetFilter"
			]



