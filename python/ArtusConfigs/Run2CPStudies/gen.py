# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import re
import copy

import HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Run2CPStudies.CPQuantities as quantities

import HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Run2Analysis.Includes.settingsJetID as sJID
import HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Run2Analysis.Includes.settingsBTaggedJetID as sBTJID
import HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Run2Analysis.Includes.settingsTauES as sTES
import HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Run2Analysis.Includes.settingsJEC as sJEC


class gen_ArtusConfig(dict):

	def __init__(self):
		pass

	def build_config(self, nickname, *args, **kwargs):

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
		quantities_dict = quantities.quantities() 
		
		quantities_dict["Quantities"] += quantities_dict.weightQuantities()
		quantities_dict["Quantities"] += [
			"run",
			"lumi",
			"event",
		]
		
		if re.search("DY.?JetsToLL", nickname):
			quantities_dict["Quantities"] += quantities_dict.genQuantities()
			quantities_dict["Quantities"] += quantities_dict.genCPQuantities()
			quantities_dict["Quantities"] += quantities_dict.genQuantitiesZ()
			quantities_dict["Quantities"] += [
				"tauSpinnerValidOutputs",
				"tauSpinnerPolarisation",
				"tauSpinnerPdgIdTau_1",
				"tauSpinnerPdgIdTau_2",
				"tauSpinnerETau_1",
				"tauSpinnerETau_2",
				"tauSpinnerEPi_1",
				"tauSpinnerEPi_2",
				"polarisationOmegaGen_1",
				"polarisationOmegaGen_2",
				"polarisationOmegaBarGen_1",
				"polarisationOmegaBarGen_2",
				"polarisationOmegaVisibleGen_1",
				"polarisationOmegaVisibleGen_2",
				"polarisationCombinedOmegaGen",
				"polarisationCombinedOmegaBarGen",
				"polarisationCombinedOmegaVisibleGen",
			]

		elif re.search("LFV", nickname):
			quantities_dict["Quantities"] += quantities_dict.genCPQuantities()  
			quantities_dict["Quantities"] += quantities_dict.genQuantitiesZ()

		elif re.search("HToTauTau|H2JetsToTauTau|Higgs",nickname):
			quantities_dict["Quantities"] += quantities_dict.genQuantities()
			quantities_dict["Quantities"] += quantities_dict.genHiggsQuantities()
			quantities_dict["Quantities"] += quantities_dict.genCPQuantities()  
			quantities_dict["Quantities"] += [
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
			quantities_dict["Quantities"] += [
				"tauSpinnerValidOutputs",
				"tauSpinnerPolarisation",
			]


		self.update(copy.deepcopy(quantities_dict))

		self["Quantities"]=list(set(self["Quantities"])) #removes dublicates from list by making it a set and then again a list


		if re.search("HToTauTau|H2JetsToTauTau|Higgs",nickname):
			self["Processors"] = [
				"producer:TaggedJetCorrectionsProducer",
				"producer:ValidTaggedJetsProducer",
				"#producer:ValidBTaggedJetsProducer",
				"producer:DiJetQuantitiesProducer"
			]
		elif re.search("DY.?JetsToLL", nickname):
			self["Processors"] = [
				"producer:GenPolarisationQuantitiesProducer",
			]
		else:
			self["Processors"] = []

