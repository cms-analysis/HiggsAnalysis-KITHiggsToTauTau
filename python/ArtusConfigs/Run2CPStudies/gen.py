# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import re

import HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Run2CPStudies.Includes.Run2CPQuantities as r2cpq

import HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Run2Analysis.Includes.settingsJetID as sJID
import HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Run2Analysis.Includes.settingsBTaggedJetID as sBTJID
import HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Run2Analysis.Includes.settingsTauES as sTES
import HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Run2Analysis.Includes.settingsJEC as sJEC


class gen_ArtusConfig(dict):

	def __init__(self):
		pass

	def build_config(self, nickname):

		JEC_config = sJEC.JEC(nickname)  #Is allready in baseconfig, for now leave it in; possibly remove it
		self.update(JEC_config)
		
		JetID_config = sJID.Jet_ID(nickname)
		self.update(JetID_config)

		BTaggedJet_config = sBTJID.BTaggedJet_ID(nickname)
		self.update(BTaggedJet_config)

		self["EventWeight"] = "eventWeight"

		self["Consumers"] = [
			"cutflow_histogram",
			"KappaLambdaNtupleConsumer",
			"#RunTimeConsumer",
			"#PrintEventsConsumer",
			"#PrintGenParticleDecayTreeConsumer"
			]
		self["Quantities"]=[]
		if re.search("DY.?JetsToLL",nickname):
			self["Quantities"] += r2cpq.genQuantities()
			self["Quantities"] += r2cpq.weightQuantities()
			self["Quantities"] += r2cpq.genCPQuantities()

		elif re.search("LFV",nickname):
			self["Quantities"] += r2cpq.genQuantitiesLFV()
			self["Quantities"] += r2cpq.weightQuantities()
			self["Quantities"] += r2cpq.genCPQuantities()
			self["Quantities"] += ["tauSpinnerPolarisation"]

		elif re.search("HToTauTau|H2JetsToTauTau|Higgs",nickname):
			self["Quantities"] += r2cpq.genQuantities()
			self["Quantities"] += r2cpq.weightQuantities()
			self["Quantities"] += r2cpq.genCPQuantities()
			self["Quantities"] += r2cpq.genHiggsQuantities()
			self["Quantities"] += [
				"nJets",
				"nJets30",
				"leadingJetLV",
				"trailingJetLV",
				"thirdJetLV",
				"fourthJetLV",
				"fifthJetLV",
				"sixthJetLV",
				"diJetDeltaPhi"
			]

		elif re.search("Embedding2016", nickname):
			self["Quantities"] += r2cpq.genQuantities()
			self["Quantities"] += r2cpq.weightQuantities()
			self["Quantities"] += ["tauSpinnerPolarisation"]

		else:
			self["Quantities"] += r2cpq.weightQuantities()

		if re.search("HToTauTau|H2JetsToTauTau|Higgs",nickname):
			self["Processors"] = [
				"producer:TaggedJetCorrectionsProducer",
				"producer:ValidTaggedJetsProducer",
				"#producer:ValidBTaggedJetsProducer",
				"producer:DiJetQuantitiesProducer"
			]
		else:
			self["Processors"] = []

