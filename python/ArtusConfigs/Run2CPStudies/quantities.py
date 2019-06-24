# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import re

from run2Quantities import Run2Quantities
# from HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Run2Analysis.Run2Quantities import Run2Quantities

class Quantities(Run2Quantities):

	def __init__(self):
		self.quantities = set()
		# quantities = {"Quantities" : set()}
		# self.quantities = set()

	def build_quantities(self, nickname, channel):
		print "build_quantities"

		if channel == "GEN":
			self.quantities.update(self.weightQuantities(tauSpinner=False, minimalWeight=True, madGraphWeight=False))

			if re.search("(Summer17|Fall17)", nickname):
				#electron tau triggers
				self.quantities.update([
					#"HLT_Ele32_WPTight_Gsf",
					"HLT_Ele35_WPTight_Gsf",
					"HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTau30_eta2p1_CrossL1"
				])
				#muon tau triggers
				self.quantities.update([
					"HLT_IsoMu24",
					"HLT_IsoMu27", #only in data recommended
					"HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1"
				])
				#tautau triggers
				"""
				self.quantities.update([
					"HLT_DoubleTightChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg",
					"HLT_DoubleMediumChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg",
					"HLT_DoubleTightChargedIsoPFTau40_Trk1_eta2p1_Reg"
				])
				"""

			if re.search("DY.?JetsToLL",nickname):
				self.quantities.update(self.genQuantities())
				self.quantities.update(self.genCPQuantities())
				if re.search("(Summer17|Fall17)", nickname):
					self.quantities.update(self.genQuantities(LFV = False, Z= False))
				else:
					self.quantities.update(self.genQuantities(LFV = False, Z= True))
				self.quantities.update(["tauSpinnerPolarisation"])

			elif re.search("LFV",nickname):
				self.quantities.update(self.genCPQuantities())
				self.quantities.update(self.genQuantities(LFV = True))

			elif re.search("HTo.*TauTau|H2JetsToTauTau|Higgs|JJHiggs",nickname):
				self.quantities.update(self.genQuantities())
				if re.search("(Summer17|Fall17)", nickname) == None:
					self.quantities.update(self.genHiggsQuantities())
					self.quantities.update(self.genCPQuantities())
				self.quantities.update([
					"nJets",
					"nJets30",
					"leadingJetLV",
					"trailingJetLV",
					"thirdJetLV",
					"fourthJetLV",
					"fifthJetLV",
					"sixthJetLV",
					"diJetDeltaPhi"
				])
				if re.search("amcatnlo",nickname):
					self.quantities.update(["lhenpNLO"])

			elif re.search("Embedding2016", nickname):
				self.quantities.update(["tauSpinnerPolarisation"])

		else:
			# common for all channels and datasets
			self.quantities.update(['nDiTauPairCandidates', 'nLooseElectrons', 'nAllDiTauPairCandidates', 'nLooseMuons'])
			self.quantities.update(self.fourVectorQuantities())
			self.quantities.update(self.syncQuantities(nickname))
			if re.search("(Summer17|Fall17|Run2017|Embedding2017)", nickname):
					self.quantities.update(["prefiringWeight","prefiringWeightUp", "prefiringWeightDown" ,"globalWeight"])
					self.quantities.update(self.singleTauQuantities())

			if channel == "ET":
				if re.search("(Summer17|Fall17|Run2017|Embedding2017)", nickname):
					self.quantities.update([
						"trg_singleelectron_27",
						"trg_singleelectron_32",
						"trg_singleelectron_32_fallback",
						"trg_singleelectron_35",
						"trg_crosselectron_ele24tau30"
					])
					if  re.search("Run2017(B|C)", nickname):
						self.quantities.update([
							#"HLT_Ele32_WPTight_Gsf",
							"HLT_Ele35_WPTight_Gsf",
							"HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTau30_eta2p1_CrossL1"
						])
					if  re.search("Embedding2017", nickname):
						self.quantities.update([
							"triggerWeight_doublemu_1",
							"idweight_doublemu_1",
							"idweight_doublemu_2",
							"isoweight_1",
							"idweight_1",
							"triggerWeight_trg27_trg32_trg35_embed_1",
							"triggerWeight_trg_EleTau_Ele24Leg_embed_1",
							"triggerWeight_tauLeg_2",
							"triggerWeight_trg27_trg32_trg35_data_1",
							"triggerWeight_trg_EleTau_Ele24Leg_data_1"
						])
						self.quantities.update([
							"tautriggerefficiencyData"
						])
					else:
						self.quantities.update([
							#"HLT_Ele32_WPTight_Gsf",
							"HLT_Ele35_WPTight_Gsf",
							"HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTau30_eta2p1_CrossL1",
							"triggerWeight_singleE_1",
							"triggerWeight_etaucross_1",
							"triggerWeight_etaucross_2",
						])
				elif re.search("Embedding2016", nickname):
					self.quantities.update([
						"triggerWeight_doublemu_1",
						"isoweight_1",
						"idweight_1",
						"triggerWeight_singleE_1",
					])

			elif channel == "MT":
				if re.search("(Summer17|Fall17|Run2017|Embedding2017)", nickname):
					self.quantities.update(["HLT_IsoMu24","HLT_IsoMu27","HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1"])
					self.quantities.update(["trg_singlemuon_24", "trg_singlemuon_27", "trg_crossmuon_mu20tau27"])
					#self.quantities.update(["matched_HLT_IsoMu24","matched_HLT_IsoMu27","matched_HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1"])
				if re.search("Embedding2016", nickname):
					self.quantities.update([
						"trg_singlemuon",
						"triggerWeight_doublemu_1",
						"isoweight_1",
						"idweight_1",
						"triggerWeight_singleMu_1",
						"trg_mutaucross",
						"triggerWeight_muTauCross_2",
						"MuTau_TauLeg_EmbeddedEfficiencyWeight_2",
						"MuTau_TauLeg_DataEfficiencyWeight_2"
					])
				if re.search("Embedding2017", nickname):
					self.quantities.update([
						"triggerWeight_doublemu_1",
						"idweight_doublemu_1",
						"idweight_doublemu_2",
						"isoweight_1",
						"idweight_1",
						"triggerWeight_mu_1",
						"triggerWeight_mutaucross_1",
						"triggerWeight_mutaucross_2"
					])
				else:
					self.quantities.update([
						"triggerWeight_mu_1",
						"triggerWeight_mutaucross_1",
						"triggerWeight_mutaucross_2",
					])
			elif channel == "TT":
				if re.search("(Summer17|Fall17|Run2017)", nickname):
					self.quantities.update([
						"HLT_DoubleTightChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg",
						"HLT_DoubleMediumChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg",
						"HLT_DoubleTightChargedIsoPFTau40_Trk1_eta2p1_Reg"
					])
				if re.search("Embedding2017", nickname):
					self.quantities.update([
						"triggerWeight_doublemu_1",
						"idweight_doublemu_1",
						"idweight_doublemu_2",
						"isoweight_1",
						"idweight_1",
						"triggerWeight_tau_1",
						"triggerWeight_tau_2",
					])
				if re.search("Embedding2016", nickname):
					self.quantities.update([
						"triggerWeight_doublemu_1",
						"triggerWeight_tau_1",
						"triggerWeight_tau_2"
					])

			if not channel == "EM":
				self.quantities.update(self.fakefactorQuantities())

			# *********** datasets(groups, samples) common across all channels including mm
			if re.search("(LFV).*(?=(Spring16|Summer16))", nickname):
				# common:
				self.quantities.update(self.genQuantities(LFV = True))

				if channel == "MM":
					self.quantities.update(self.singleTauQuantities())
					self.quantities.update(self.weightQuantities(tauSpinner=False, minimalWeight=True, madGraphWeight=False))

				else:
					self.quantities.update(self.weightQuantities(tauSpinner=True, minimalWeight=True, madGraphWeight=True))
					#self.quantities.update(self.splitJecUncertaintyQuantities())

					if not channel == "TT":
						self.quantities.update(self.recoCPQuantities(melaQuantities=True))

						if channel == "EM":
							self.quantities.update(set([ 'jetCorrectionWeight']))
						else:
							print "for et there should be diTauMass(singleTauQuantities)"
							self.quantities.update(self.singleTauQuantities())
							self.quantities.update(set(['nVetoElectrons', 'jetCorrectionWeight']))

			elif re.search('(DY.?JetsToLL).*(?=(Spring16|Summer16|Summer17|Fall17))', nickname):
				self.quantities.update(self.recoCPQuantities(melaQuantities=False))
				if re.search("(Run2017|Summer17|Fall17)", nickname) == None:
					self.quantities.update(self.genQuantities(LFV = False)) #TODO for 2017 also , Z = True
					#self.quantities.update(self.splitJecUncertaintyQuantities())  #no lhe in 2017 skim
				self.quantities.update(self.genMatchedCPQuantities())

				self.quantities.update(self.recoPolarisationQuantitiesSvfit())
				self.quantities.update(self.recoPolarisationQuantities())

				if channel == "MM":
					self.quantities.update(self.singleTauQuantities())
					self.quantities.update(self.weightQuantities(tauSpinner=False, minimalWeight=True, madGraphWeight=False))

				else:

					self.quantities.update(self.svfitSyncQuantities())
					self.quantities.update(self.weightQuantities(tauSpinner=True, minimalWeight=True, madGraphWeight=True))

					self.quantities.add('tauSpinnerPolarisation')


					if channel == "EM":
						self.quantities.update(self.lheWeightsDYQuantities())
					else:
						self.quantities.update(self.singleTauQuantities())
						if channel in ["ET"]: self.quantities.add('nVetoElectrons')
						if channel in ["MT"]: self.quantities.add('nVetoMuons')

			# ************ datasets(groups, samples) common across all except mm channels are all the rest
			else:
				if not channel == "MM" and re.search('(HTo.*TauTau|H2JetsToTauTau|Higgs|JJHiggs).*(?=(Spring16|Summer16|Summer17|Fall17))', nickname):
					self.quantities.update(self.genMatchedCPQuantities())

					if re.search("(Run2017|Summer17|Fall17)", nickname) == None:
						#self.quantities.update(self.splitJecUncertaintyQuantities())
						self.quantities.update(self.genHiggsQuantities()) #no lhe in 2017 skim
					if re.search("amcatnlo",nickname):
						self.quantities.update(["lhenpNLO", "quarkmassWeight","quarkmassUpWeight","quarkmassDownWeight"])
					self.quantities.update(self.genQuantities(LFV = False))
					self.quantities.update(self.svfitSyncQuantities())
					self.quantities.update(self.recoCPQuantities(melaQuantities=True))
					self.quantities.update(self.weightQuantities(tauSpinner=True, minimalWeight=True, madGraphWeight=True))
					# if channel in ["TT", "MT", "ET"]:
					# 	self.quantities.update(set(['#tauPolarisationTMVA', '#tauPolarisationSKLEARN']))
					if channel in ["ET"]: self.quantities.add('nVetoElectrons')
					if channel in ["MT"]: self.quantities.add('nVetoMuons')

				elif not channel == "MM" and re.search('Run2015', nickname): # data
					self.quantities.update(self.recoPolarisationQuantities())
					self.quantities.update(self.weightQuantities(tauSpinner=True, minimalWeight=True, madGraphWeight=True))
					if channel in ["ET"]: self.quantities.add('nVetoElectrons')
					if channel in ["MT"]: self.quantities.add('nVetoMuons')

				elif not channel == "MM" and re.search('Embedding2016', nickname):
					self.quantities.add('tauSpinnerPolarisation')
					self.quantities.update(self.recoPolarisationQuantities())
					self.quantities.update(self.genQuantities(LFV = False))
					self.quantities.update(self.weightQuantities(tauSpinner=True, minimalWeight=True, madGraphWeight=True))
					#self.quantities.update(self.splitJecUncertaintyQuantities())

				elif not channel == "MM" and re.search('(HTo.*TauTau|H2JetsToTauTau|Higgs).*(?=Fall15)', nickname):
					self.quantities.update(set(['melaProbCPOddVBF', 'melaDiscriminatorDCPGGH', 'melaM125ProbCPEvenGGH', 'melaProbCPMixVBF', 'melaM125ProbCPMixVBF', 'melaM125DiscriminatorDCPVBF', 'melaDiscriminatorD0MinusGGH', 'melaDiscriminatorD0MinusVBF', 'melaProbCPEvenGGH', 'melaM125ProbCPEvenVBF', 'melaM125ProbCPMixGGH', 'melaProbCPOddGGH', 'melaDiscriminatorDCPVBF', 'melaM125ProbCPOddGGH', 'melaM125DiscriminatorDCPGGH', 'melaProbCPMixGGH', 'melaProbCPEvenVBF', 'melaM125DiscriminatorD0MinusGGH', 'melaM125ProbCPOddVBF', 'melaM125DiscriminatorD0MinusVBF']))
					self.quantities.update(self.recoCPQuantitiesHiggs())
					self.quantities.update(self.genHiggsQuantities())
					self.quantities.update(self.genQuantities(LFV = False))
					self.quantities.update(self.svfitSyncQuantities())
					self.quantities.update(self.genMatchedCPQuantities())
					self.quantities.update(self.weightQuantities(tauSpinner=True, minimalWeight=True, madGraphWeight=True))
					# if channel in ["TT", "MT", "ET"]:
					# 	self.quantities.update(set(['#tauPolarisationTMVA', '#tauPolarisationSKLEARN']))
					if channel in ["ET"]: self.quantities.add('nVetoElectrons')
					if channel in ["MT"]: self.quantities.add('nVetoMuons')

				elif not channel == "MM" and re.search('(DY.?JetsToLL).*(?=Fall15)', nickname):
					self.quantities.add('tauSpinnerPolarisation')
					self.quantities.update(self.recoPolarisationQuantities())
					self.quantities.update(self.genQuantities(LFV = False))
					self.quantities.update(self.genMatchedCPQuantities())
					self.quantities.update(self.weightQuantities(tauSpinner=True, minimalWeight=True, madGraphWeight=True))
					if channel == "ET": self.quantities.add('nVetoElectrons')
					if channel in ["MT"]: self.quantities.add('nVetoMuons')

				elif not channel == "MM" and re.search('^((?!(DY.?JetsToLL|HTo.*TauTau|H2JetsToTauTau|Higgs)).)*Fall15', nickname):
					self.quantities.update(self.recoPolarisationQuantities())
					self.quantities.update(self.weightQuantities(tauSpinner=True, minimalWeight=True, madGraphWeight=True))
					if channel == "ET": self.quantities.add('nVetoElectrons')
					if channel in ["MT"]: self.quantities.add('nVetoMuons')

				else: # data, 2016/2017 wjets, ttbar, diboson
					self.quantities.update(self.recoCPQuantities(melaQuantities=True))

					if channel == "MM":
						self.quantities.update(self.singleTauQuantities())
						self.quantities.update(self.weightQuantities(tauSpinner=False, minimalWeight=True, madGraphWeight=False))

					else:
						self.quantities.update(self.svfitSyncQuantities())
						self.quantities.update(self.weightQuantities(tauSpinner=True, minimalWeight=True, madGraphWeight=True))
						#if re.search("(Run2017|Summer17|Fall17|Embedding2017)", nickname) == None:
							#self.quantities.update(self.splitJecUncertaintyQuantities())
						self.quantities.update(self.recoPolarisationQuantitiesSvfit())
						self.quantities.update(self.recoPolarisationQuantities())

						if channel == "ET": self.quantities.update(set(['nVetoElectrons']))
						if channel in ["MT"]: self.quantities.add('nVetoMuons')

	@staticmethod
	def genCPQuantities():    #used in gen.py
		return [
			#"1genBosonDaughterSize",
			#"1genBoson1DaughterPt",
			#"1genBoson1DaughterPz",
			#"1genBoson1DaughterEta",
			#"1genBoson1DaughterPhi",
			#"1genBoson1DaughterMass",
			#"1genBoson1DaughterCharge",
			#"1genBoson1DaughterEnergy",
			#"1genBoson1DaughterPdgId",
			#"1genBoson1DaughterStatus",
			#"1genBoson2DaughterPt",
			#"1genBoson2DaughterPz",
			#"1genBoson2DaughterEta",
			#"1genBoson2DaughterPhi",
			#"1genBoson2DaughterMass",
			#"1genBoson2DaughterEnergy",
			#"1genBoson2DaughterPdgId",
			#"1genBoson2DaughterStatus",
			#"1genBoson1DaughterGranddaughterSize",
			#"1genBoson1Daughter1GranddaughterPt",
			#"1genBoson1Daughter1GranddaughterPz",
			#"1genBoson1Daughter1GranddaughterEta",
			#"1genBoson1Daughter1GranddaughterPhi",
			#"1genBoson1Daughter1GranddaughterMass",
			#"1genBoson1Daughter1GranddaughterEnergy",
			#"1genBoson1Daughter1GranddaughterPdgId",
			#"1genBoson1Daughter1GranddaughterStatus",
			#"1genBoson1Daughter2GranddaughterPt",
			#"1genBoson1Daughter2GranddaughterPz",
			#"1genBoson1Daughter2GranddaughterEta",
			#"1genBoson1Daughter2GranddaughterPhi",
			#"1genBoson1Daughter2GranddaughterMass",
			#"1genBoson1Daughter2GranddaughterEnergy",
			#"1genBoson1Daughter2GranddaughterPdgId",
			#"1genBoson1Daughter2GranddaughterStatus",
			#"1genBoson1Daughter3GranddaughterPt",
			#"1genBoson1Daughter3GranddaughterPz",
			#"1genBoson1Daughter3GranddaughterEta",
			#"1genBoson1Daughter3GranddaughterPhi",
			#"1genBoson1Daughter3GranddaughterMass",
			#"1genBoson1Daughter3GranddaughterEnergy",
			#"1genBoson1Daughter3GranddaughterPdgId",
			#"1genBoson1Daughter3GranddaughterStatus",
			#"1genBoson1Daughter4GranddaughterPt",
			#"1genBoson1Daughter4GranddaughterPz",
			#"1genBoson1Daughter4GranddaughterEta",
			#"1genBoson1Daughter4GranddaughterPhi",
			#"1genBoson1Daughter4GranddaughterMass",
			#"1genBoson1Daughter4GranddaughterEnergy",
			#"1genBoson1Daughter4GranddaughterPdgId",
			#"1genBoson1Daughter4GranddaughterStatus",
			#"1genBoson2DaughterGranddaughterSize",
			#"1genBoson2Daughter1GranddaughterPt",
			#"1genBoson2Daughter1GranddaughterPz",
			#"1genBoson2Daughter1GranddaughterEta",
			#"1genBoson2Daughter1GranddaughterPhi",
			#"1genBoson2Daughter1GranddaughterMass",
			#"1genBoson2Daughter1GranddaughterEnergy",
			#"1genBoson2Daughter1GranddaughterPdgId",
			#"1genBoson2Daughter1GranddaughterStatus",
			#"1genBoson2Daughter2GranddaughterPt",
			#"1genBoson2Daughter2GranddaughterPz",
			#"1genBoson2Daughter2GranddaughterEta",
			#"1genBoson2Daughter2GranddaughterPhi",
			#"1genBoson2Daughter2GranddaughterMass",
			#"1genBoson2Daughter2GranddaughterEnergy",
			#"1genBoson2Daughter2GranddaughterPdgId",
			#"1genBoson2Daughter2GranddaughterStatus",
			#"1genBoson2Daughter3GranddaughterPt",
			#"1genBoson2Daughter3GranddaughterPz",
			#"1genBoson2Daughter3GranddaughterEta",
			#"1genBoson2Daughter3GranddaughterPhi",
			#"1genBoson2Daughter3GranddaughterMass",
			#"1genBoson2Daughter3GranddaughterEnergy",
			#"1genBoson2Daughter3GranddaughterPdgId",
			#"1genBoson2Daughter3GranddaughterStatus",
			#"1genBoson2Daughter4GranddaughterPt",
			#"1genBoson2Daughter4GranddaughterPz",
			#"1genBoson2Daughter4GranddaughterEta",
			#"1genBoson2Daughter4GranddaughterPhi",
			#"1genBoson2Daughter4GranddaughterMass",
			#"1genBoson2Daughter4GranddaughterEnergy",
			#"1genBoson2Daughter4GranddaughterPdgId",
			#"1genBoson2Daughter4GranddaughterStatus",
			#"1genBoson1Daughter2GranddaughterGrandGranddaughterSize",
			#"1genBoson1Daughter2Granddaughter1GrandGranddaughterPdgId",
			#"1genBoson1Daughter2Granddaughter1GrandGranddaughterStatus",
			#"1genBoson1Daughter2Granddaughter2GrandGranddaughterPdgId",
			#"1genBoson1Daughter2Granddaughter2GrandGranddaughterStatus",
			#"1genBoson1Daughter2Granddaughter3GrandGranddaughterPdgId",
			#"1genBoson1Daughter2Granddaughter3GrandGranddaughterStatus",
			#"1genBoson1Daughter2Granddaughter4GrandGranddaughterPdgId",
			#"1genBoson1Daughter2Granddaughter4GrandGranddaughterStatus",
			#"1genBoson1Daughter2Granddaughter5GrandGranddaughterPdgId",
			#"1genBoson1Daughter2Granddaughter5GrandGranddaughterStatus",
			#"1genBoson1Daughter2Granddaughter6GrandGranddaughterPdgId",
			#"1genBoson1Daughter2Granddaughter6GrandGranddaughterStatus",
			#"1genBoson2Daughter2GranddaughterGrandGranddaughterSize",
			"genPVx",
			"genPVy",
			"genPVz",
			"genPhiStarCP",
			"genPhiStar",
			"genOStarCP",
			"genPhiCP",
			"genPhi",
			"genOCP",
			"genPhiStarCPComb",
			"genPhiCPLab",

			"genIP1mag",
			"genIP1x",
			"genIP1y",
			"genIP1z",

			"genIP2mag",
			"genIP2x",
			"genIP2y",
			"genIP2z",
			"genCosPsiPlus",
			"genCosPsiMinus",
			"genCosPsiPlus",
			"genCosPsiMinus",
			"genPhiStarCP_rho",
			"genPhiCP_rho",
			"genPhiStar_rho",
			"genPhi_rho",
			"gen_yTau",
			"gen_posyTauL",
			"gen_negyTauL",
			"TauMProngEnergy",
			"TauPProngEnergy",
			"Tau1OneProngsSize",
			"Tau2OneProngsSize",
			"Tau1DecayMode",
			"Tau2DecayMode",
			"TauTree1DecayMode",
			"TauTree2DecayMode",
			"OneProngChargedPart1Pt",
			"OneProngChargedPart1Pz",
			"OneProngChargedPart1Eta",
			"OneProngChargedPart1Phi",
			"OneProngChargedPart1Mass",
			"OneProngChargedPart1Energy",
			"OneProngChargedPart1PdgId",
			"OneProngChargedPart2Pt",
			"OneProngChargedPart2Pz",
			"OneProngChargedPart2Eta",
			"OneProngChargedPart2Phi",
			"OneProngChargedPart2Mass",
			"OneProngChargedPart2Energy",
			"OneProngChargedPart2PdgId",
			"genZPlus",
			"genZMinus",
			"genZs"
		]

	@staticmethod
	def genHiggsQuantities():
		return [
			"lheSignedDiJetDeltaPhi",
			"lheDiJetAbsDeltaEta",
			"lheDiJetMass",
			"lheNJets",
			"lheParticleIn1LV",
			"lheParticleIn2LV",
			"lheParticleOut1LV",
			"lheParticleOut2LV",
			"lheParticleBoson1LV",
			"lheParticleIn1PdgId",
			"lheParticleIn2PdgId",
			"lheParticleOut1PdgId",
			"lheParticleOut2PdgId",
			"lheParticleBoson1PdgId"
		]

	@staticmethod
	def genMatchedCPQuantities():
		return [
			#"1genBosonDaughterSize",
			#"1genBoson1DaughterPt",
			#"1genBoson1DaughterPz",
			#"1genBoson1DaughterEta",
			#"1genBoson1DaughterPhi",
			#"1genBoson1DaughterMass",
			#"1genBoson1DaughterCharge",
			#"1genBoson1DaughterEnergy",
			#"1genBoson1DaughterPdgId",
			#"1genBoson1DaughterStatus",
			#"1genBoson2DaughterPt",
			#"1genBoson2DaughterPz",
			#"1genBoson2DaughterEta",
			#"1genBoson2DaughterPhi",
			#"1genBoson2DaughterMass",
			#"1genBoson2DaughterEnergy",
			#"1genBoson2DaughterPdgId",
			#"1genBoson2DaughterStatus",
			#"1genBoson1DaughterGranddaughterSize",
			#"1genBoson1Daughter1GranddaughterPt",
			#"1genBoson1Daughter1GranddaughterPz",
			#"1genBoson1Daughter1GranddaughterEta",
			#"1genBoson1Daughter1GranddaughterPhi",
			#"1genBoson1Daughter1GranddaughterMass",
			#"1genBoson1Daughter1GranddaughterEnergy",
			#"1genBoson1Daughter1GranddaughterPdgId",
			#"1genBoson1Daughter1GranddaughterStatus",
			#"1genBoson1Daughter2GranddaughterPt",
			#"1genBoson1Daughter2GranddaughterPz",
			#"1genBoson1Daughter2GranddaughterEta",
			#"1genBoson1Daughter2GranddaughterPhi",
			#"1genBoson1Daughter2GranddaughterMass",
			#"1genBoson1Daughter2GranddaughterEnergy",
			#"1genBoson1Daughter2GranddaughterPdgId",
			#"1genBoson1Daughter2GranddaughterStatus",
			#"1genBoson1Daughter3GranddaughterPt",
			#"1genBoson1Daughter3GranddaughterPz",
			#"1genBoson1Daughter3GranddaughterEta",
			#"1genBoson1Daughter3GranddaughterPhi",
			#"1genBoson1Daughter3GranddaughterMass",
			#"1genBoson1Daughter3GranddaughterEnergy",
			#"1genBoson1Daughter3GranddaughterPdgId",
			#"1genBoson1Daughter3GranddaughterStatus",
			#"1genBoson1Daughter4GranddaughterPt",
			#"1genBoson1Daughter4GranddaughterPz",
			#"1genBoson1Daughter4GranddaughterEta",
			#"1genBoson1Daughter4GranddaughterPhi",
			#"1genBoson1Daughter4GranddaughterMass",
			#"1genBoson1Daughter4GranddaughterEnergy",
			#"1genBoson1Daughter4GranddaughterPdgId",
			#"1genBoson1Daughter4GranddaughterStatus",
			#"1genBoson2DaughterGranddaughterSize",
			#"1genBoson2Daughter1GranddaughterPt",
			#"1genBoson2Daughter1GranddaughterPz",
			#"1genBoson2Daughter1GranddaughterEta",
			#"1genBoson2Daughter1GranddaughterPhi",
			#"1genBoson2Daughter1GranddaughterMass",
			#"1genBoson2Daughter1GranddaughterEnergy",
			#"1genBoson2Daughter1GranddaughterPdgId",
			#"1genBoson2Daughter1GranddaughterStatus",
			#"1genBoson2Daughter2GranddaughterPt",
			#"1genBoson2Daughter2GranddaughterPz",
			#"1genBoson2Daughter2GranddaughterEta",
			#"1genBoson2Daughter2GranddaughterPhi",
			#"1genBoson2Daughter2GranddaughterMass",
			#"1genBoson2Daughter2GranddaughterEnergy",
			#"1genBoson2Daughter2GranddaughterPdgId",
			#"1genBoson2Daughter2GranddaughterStatus",
			#"1genBoson2Daughter3GranddaughterPt",
			#"1genBoson2Daughter3GranddaughterPz",
			#"1genBoson2Daughter3GranddaughterEta",
			#"1genBoson2Daughter3GranddaughterPhi",
			#"1genBoson2Daughter3GranddaughterMass",
			#"1genBoson2Daughter3GranddaughterEnergy",
			#"1genBoson2Daughter3GranddaughterPdgId",
			#"1genBoson2Daughter3GranddaughterStatus",
			#"1genBoson2Daughter4GranddaughterPt",
			#"1genBoson2Daughter4GranddaughterPz",
			#"1genBoson2Daughter4GranddaughterEta",
			#"1genBoson2Daughter4GranddaughterPhi",
			#"1genBoson2Daughter4GranddaughterMass",
			#"1genBoson2Daughter4GranddaughterEnergy",
			#"1genBoson2Daughter4GranddaughterPdgId",
			#"1genBoson2Daughter4GranddaughterStatus",
			#"1genBoson1Daughter2GranddaughterGrandGranddaughterSize",
			#"1genBoson1Daughter2Granddaughter1GrandGranddaughterPdgId",
			#"1genBoson1Daughter2Granddaughter1GrandGranddaughterStatus",
			#"1genBoson1Daughter2Granddaughter2GrandGranddaughterPdgId",
			#"1genBoson1Daughter2Granddaughter2GrandGranddaughterStatus",
			#"1genBoson1Daughter2Granddaughter3GrandGranddaughterPdgId",
			#"1genBoson1Daughter2Granddaughter3GrandGranddaughterStatus",
			#"1genBoson1Daughter2Granddaughter4GrandGranddaughterPdgId",
			#"1genBoson1Daughter2Granddaughter4GrandGranddaughterStatus",
			#"1genBoson1Daughter2Granddaughter5GrandGranddaughterPdgId",
			#"1genBoson1Daughter2Granddaughter5GrandGranddaughterStatus",
			#"1genBoson1Daughter2Granddaughter6GrandGranddaughterPdgId",
			#"1genBoson1Daughter2Granddaughter6GrandGranddaughterStatus",
			#"1genBoson2Daughter2GranddaughterGrandGranddaughterSize",
			"genQ_1",
			"genQ_2",
			"genPVx",
			"genPVy",
			"genPVz",
			"genSV1x",
			"genSV1y",
			"genSV1z",
			"genSV2x",
			"genSV2y",
			"genSV2z",

			"genD01",
			"genD02",

			"genIP1mag",
			"genIP1x",
			"genIP1y",
			"genIP1z",

			"genIP2mag",
			"genIP2x",
			"genIP2y",
			"genIP2z",
			"genCosPsiPlus",
			"genCosPsiMinus",
			"genPhiStarCP",
			"genPhiStar",
			"genOStarCP",
			"genPhiStarCPComb",
			"genPhiStarCP_rho",
			"gen_posyTauL",
			"gen_negyTauL",
			"TauMProngEnergy",
			"TauPProngEnergy",
			"Tau1OneProngsSize",
			"Tau2OneProngsSize",
			"OneProngChargedPart1Pt",
			"OneProngChargedPart1Pz",
			"OneProngChargedPart1Eta",
			"OneProngChargedPart1Phi",
			"OneProngChargedPart1Mass",
			"OneProngChargedPart1Energy",
			"OneProngChargedPart1PdgId",
			"OneProngChargedPart2Pt",
			"OneProngChargedPart2Pz",
			"OneProngChargedPart2Eta",
			"OneProngChargedPart2Phi",
			"OneProngChargedPart2Mass",
			"OneProngChargedPart2Energy",
			"OneProngChargedPart2PdgId",
			"genZPlus",
			"genZMinus",
			"genZs",
			"d0s_area",
			"d0s_dist"
		]

	@classmethod
	def genQuantities(klass, LFV = False, Z = False):
		s = [
			"genBosonLV",
			"genBosonParticleFound",
			"genBosonLVFound",
			"genBosonLep1PdgId",
			"genBosonLep1LV",
			"genBosonTau1PdgId",
			"genBosonTau1LV",
			"genBosonTau1VisibleLV",
			"genBosonTau1DecayMode",
			"genBosonTau1NProngs",
			"genBosonTau1NPi0s",
			"genBosonLep2PdgId",
			"genBosonLep2LV",
			"genBosonTau2PdgId",
			"genBosonTau2LV",
			"genBosonTau2VisibleLV",
			"genBosonTau2DecayMode",
			"genBosonTau2NProngs",
			"genBosonTau2NPi0s",
			"genDiLeptonDecayMode",
			"isZEE",
			"isZMM",
			"isZTT",
			"genTauTauDecayMode",
			"isZtt",
			"isZmt",
			"isZet",
			"isZem",
			"isZmm",
			"isZee",
			"npartons"
		]
		if LFV:
			s.remove("npartons")
			s += klass.genQuantitiesLFV()

		if Z:
			s += [
				"lheZBosonProductionMode",
				"lheZfromUUbar",
				"lheZfromDDbar",
				"lheZfromCCbar",
				"lheZfromSSbar",
				"lheZfromBBbar"
			]
		return s

	@staticmethod
	def genQuantitiesLFV():
		return [
			"genBosonLV",
			"genBosonParticleFound",
			"genBosonLVFound",
			"genBosonLep1PdgId",
			"genBosonLep1LV",
			"genBosonTau1PdgId",
			"genBosonTau1LV",
			"genBosonTau1VisibleLV",
			"genBosonTau1DecayMode",
			"genBosonTau1NProngs",
			"genBosonTau1NPi0s",
			"genBosonLep2PdgId",
			"genBosonLep2LV",
			"genBosonTau2PdgId",
			"genBosonTau2LV",
			"genBosonTau2VisibleLV",
			"genBosonTau2DecayMode",
			"genBosonTau2NProngs",
			"genBosonTau2NPi0s",
			"genDiLeptonDecayMode",
			"isZEE",
			"isZMM",
			"isZTT",
			"genTauTauDecayMode",
			"isZtt",
			"isZmt",
			"isZet",
			"isZem",
			"isZmm",
			"isZee",
			"genDiLeptonDecayModeLFV",
			"isZET",
			"isZEM",
			"isZMT",
			"genTauDecayMode",
			"isZmt",
			"isZet",
			"isZem",
			"isZmm",
			"isZee",
			"lheZBosonProductionMode",
			"lheZfromUUbar",
			"lheZfromDDbar",
			"lheZfromCCbar",
			"lheZfromSSbar",
			"lheZfromBBbar",
			"lheDiLeptonDecayMode",
			"lheZtoEE",
			"lheZtoMM",
			"lheZtoTT",
			"lheZtoEM",
			"lheZtoET",
			"lheZtoMT",
			"LHE_p_1",
			"LHE_p_2"
		]

	@staticmethod
	def melaQuantities(m125=False):
		l= [
			"melaProbCPEvenGGH",
			"melaProbCPOddGGH",
			"melaProbCPMixGGH",
			"melaDiscriminatorD0MinusGGH",
			"melaDiscriminatorDCPGGH",

			"melaProbCPEvenVBF",
			"melaProbCPOddVBF",
			"melaProbCPMixVBF",
			"melaDiscriminatorD0MinusVBF",
			"melaDiscriminatorDCPVBF"]

			#"melaProbCPEvenWlepH",
			#"melaProbCPOddWlepH",
			#"melaProbCPMixWlepH",
			#"melaDiscriminatorD0MinusWlepH",
			#"melaDiscriminatorDCPWlepH",

			#"melaProbCPEvenWhadH",
			#"melaProbCPOddWhadH",
			#"melaProbCPMixWhadH",
			#"melaDiscriminatorD0MinusWhadH",
			#"melaDiscriminatorDCPWhadH",

			#"melaProbCPEvenZlepH",
			#"melaProbCPOddZlepH",
			#"melaProbCPMixZlepH",
			#"melaDiscriminatorD0MinusZlepH",
			#"melaDiscriminatorDCPZlepH",

			#"melaProbCPEvenZhadH",
			#"melaProbCPOddZhadH",
			#"melaProbCPMixZhadH",
			#"melaDiscriminatorD0MinusZhadH",
			#"melaDiscriminatorDCPZhadH",
		if m125:
			l += [
				"melaM125ProbCPEvenGGH",
				"melaM125ProbCPOddGGH",
				"melaM125ProbCPMixGGH",
				"melaM125DiscriminatorD0MinusGGH",
				"melaM125DiscriminatorDCPGGH",

				"melaM125ProbCPEvenVBF",
				"melaM125ProbCPOddVBF",
				"melaM125ProbCPMixVBF",
				"melaM125DiscriminatorD0MinusVBF",
				"melaM125DiscriminatorDCPVBF"]

				#"melaM125ProbCPEvenWlepH",
				#"melaM125ProbCPOddWlepH",
				#"melaM125ProbCPMixWlepH",
				#"melaM125DiscriminatorD0MinusWlepH",
				#"melaM125DiscriminatorDCPWlepH",

				#"melaM125ProbCPEvenWhadH",
				#"melaM125ProbCPOddWhadH",
				#"melaM125ProbCPMixWhadH",
				#"melaM125DiscriminatorD0MinusWhadH",
				#"melaM125DiscriminatorDCPWhadH",

				#"melaM125ProbCPEvenZlepH",
				#"melaM125ProbCPOddZlepH",
				#"melaM125ProbCPMixZlepH",
				#"melaM125DiscriminatorD0MinusZlepH",
				#"melaM125DiscriminatorDCPZlepH",

				#"melaM125ProbCPEvenZhadH",
				#"melaM125ProbCPOddZhadH",
				#"melaM125ProbCPMixZhadH",
				#"melaM125DiscriminatorD0MinusZhadH",
				#"melaM125DiscriminatorDCPZhadH"
		return l

	@classmethod
	def recoCPQuantities(klass, melaQuantities=True):
		s = [
			"thePVx",
			"thePVy",
			"thePVz",
			"thePVchi2",
			"thePVnDOF",
			"thePVnTracks",
			"thePVsigmaxx",
			"thePVsigmayy",
			"thePVsigmazz",
			"thePVsigmaxy",
			"thePVsigmaxz",
			"thePVsigmayz",

			"refitPVx",
			"refitPVy",
			"refitPVz",
			"refitPVchi2OverNdof",
			"refitPVnTracks",
			"refitPVsigmaxx",
			"refitPVsigmayy",
			"refitPVsigmazz",
			"refitPVsigmaxy",
			"refitPVsigmaxz",
			"refitPVsigmayz",

			"refitPVBSx",
			"refitPVBSy",
			"refitPVBSz",
			"refitPVBSchi2OverNdof",
			"refitPVBSnTracks",
			"refitPVBSsigmaxx",
			"refitPVBSsigmayy",
			"refitPVBSsigmazz",
			"refitPVBSsigmaxy",
			"refitPVBSsigmaxz",
			"refitPVBSsigmayz",

			"theBSx",
			"theBSy",
			"theBSz",
			"theBSsigmax",
			"theBSsigmay",
			"theBSsigmaz",

			"refP1x",
			"refP1y",
			"refP1z",
			"refP2x",
			"refP2y",
			"refP2z",

			"lep1TrackChi2OverNdof",
			"lep1TrackNInnerHits",
			"lep1TrackIsLooseQuality",
			"lep1TrackIsTightQuality",
			"lep1TrackIsHighPurityQuality",

			"lep2TrackChi2OverNdof",
			"lep2TrackNInnerHits",
			"lep2TrackIsLooseQuality",
			"lep2TrackIsTightQuality",
			"lep2TrackIsHighPurityQuality",

			"track1p4x",
			"track1p4y",
			"track1p4z",
			"track2p4x",
			"track2p4y",
			"track2p4z",

			"d3D_refitPV_1",
			"err3D_refitPV_1",
			"d2D_refitPV_1",
			"err2D_refitPV_1",
			"d3D_refitPV_2",
			"err3D_refitPV_2",
			"d2D_refitPV_2",
			"err2D_refitPV_2",

			"errD0_1",
			"errD0_1_newErr",
			"errD0_2",
			"errD0_2_newErr",

			"errDZ_1",
			"errDZ_1_newErr",
			"errDZ_2",
			"errDZ_2_newErr",

			"errIP_1",
			"errIP_2",

			"errD0_refitPV_1",
			"errD0_refitPV_2",

			"errDZ_refitPV_1",
			"errDZ_refitPV_2",

			"errIP_refitPV_1",
			"errIP_refitPV_2",

			"IP_1mag",
			"IP_1x",
			"IP_1y",
			"IP_1z",
			"IP_2mag",
			"IP_2x",
			"IP_2y",
			"IP_2z",
			"thePVdistanceToPCA1",
			"thePVdistanceToPCA2",
			"thePCA1projToPVellipsoid",
			"thePCA2projToPVellipsoid",

			"IP_refitPV_1mag",
			"IP_refitPV_1x",
			"IP_refitPV_1y",
			"IP_refitPV_1z",
			"IP_refitPV_2mag",
			"IP_refitPV_2x",
			"IP_refitPV_2y",
			"IP_refitPV_2z",
			"thePVdistanceToPCA1_refitPV",
			"thePVdistanceToPCA2_refitPV",
			"thePCA1projToPVellipsoid_refitPV",
			"thePCA2projToPVellipsoid_refitPV",

			"IP_helical_1mag",
			"IP_helical_1x",
			"IP_helical_1y",
			"IP_helical_1z",
			"IP_helical_2mag",
			"IP_helical_2x",
			"IP_helical_2y",
			"IP_helical_2z",

			"IP_helical_refitPV_1mag",
			"IP_helical_refitPV_1x",
			"IP_helical_refitPV_1y",
			"IP_helical_refitPV_1z",
			"IP_helical_refitPV_2mag",
			"IP_helical_refitPV_2x",
			"IP_helical_refitPV_2y",
			"IP_helical_refitPV_2z",

			"recoIP1_helicalCovxx",
			"recoIP1_helicalCovxy",
			"recoIP1_helicalCovxz",
			"recoIP1_helicalCovyy",
			"recoIP1_helicalCovyz",
			"recoIP2_helicalCovxy",
			"recoIP2_helicalCovxz",
			"recoIP2_helicalCovyy",
			"recoIP2_helicalCovyz",
			"recoIP2_helicalCovzz",

			"recoIP1_helical_refitPVCovxx",
			"recoIP1_helical_refitPVCovxy",
			"recoIP1_helical_refitPVCovxz",
			"recoIP1_helical_refitPVCovyy",
			"recoIP1_helical_refitPVCovyz",
			"recoIP1_helical_refitPVCovzz",
			"recoIP2_helical_refitPVCovxx",
			"recoIP2_helical_refitPVCovxy",
			"recoIP2_helical_refitPVCovxz",
			"recoIP2_helical_refitPVCovyy",
			"recoIP2_helical_refitPVCovyz",
			"recoIP2_helical_refitPVCovzz",

			"trackFromBS_1mag",
			"trackFromBS_1x",
			"trackFromBS_1y",
			"trackFromBS_1z",
			"trackFromBS_2mag",
			"trackFromBS_2x",
			"trackFromBS_2y",
			"trackFromBS_2z",

			"cosPsiPlus",
			"cosPsiMinus",

			"deltaEtaGenRecoIP1",
			"deltaEtaGenRecoIP2",
			"deltaPhiGenRecoIP1",
			"deltaPhiGenRecoIP2",
			"deltaRGenRecoIP1",
			"deltaRGenRecoIP2",
			"deltaGenRecoIP1",
			"deltaGenRecoIP2",

			"deltaEtaGenRecoIP1_helical",
			"deltaEtaGenRecoIP2_helical",
			"deltaPhiGenRecoIP1_helical",
			"deltaPhiGenRecoIP2_helical",
			"deltaRGenRecoIP1_helical",
			"deltaRGenRecoIP2_helical",
			"deltaGenRecoIP1_helical",
			"deltaGenRecoIP2_helical",

			"deltaEtaGenRecoIP1_helical_refitPV",
			"deltaEtaGenRecoIP2_helical_refitPV",
			"deltaPhiGenRecoIP1_helical_refitPV",
			"deltaPhiGenRecoIP2_helical_refitPV",
			"deltaRGenRecoIP1_helical_refitPV",
			"deltaRGenRecoIP2_helical_refitPV",
			"deltaGenRecoIP1_helical_refitPV",
			"deltaGenRecoIP2_helical_refitPV",

			"deltaEtaGenRecoIP1_refitPV",
			"deltaEtaGenRecoIP2_refitPV",
			"deltaPhiGenRecoIP1_refitPV",
			"deltaPhiGenRecoIP2_refitPV",
			"deltaRGenRecoIP1_refitPV",
			"deltaRGenRecoIP2_refitPV",
			"deltaGenRecoIP1_refitPV",
			"deltaGenRecoIP2_refitPV",

			"recoPhiStarCP",
			#"recoPhiStarCPrPV2",
			#"recoPhiStarCPrPV_rho",
			#"recoPhiStarCPrPVbs",
			#"recoPhiStarCPrPVbs_rho",

			"recoPhiStarCP_rho",
			"recoPhiStarCP_rho_merged",
			"recoPhiStarCPrPV",
			"recoPhiStarCPComb",
			"recoPhiStarCPCombMerged",
			"recoPhiStarCPComb_norefit",
			"recoPhiStarCPCombMerged_norefit",

			"recoPhiPlus_ipmeth",
			"recoPhiMinus_ipmeth",
			"recoPhiStarPlus_ipmeth",
			"recoPhiStarMinus_ipmeth",
			"recoPhiPlus_combmeth",
			"recoPhiMinus_combmeth",
			"recoPhiStarPlus_combmeth",
			"recoPhiStarMinus_combmeth",
			"recoPhiPlus_rhometh",
			"recoPhiMinus_rhometh",
			"recoPhiStarPlus_rhometh",
			"recoPhiStarMinus_rhometh",

			"recoPhiStar",
			"recoPhiStar_rho",
			"recoChargedHadron1HiggsFrameEnergy",
			"recoChargedHadron2HiggsFrameEnergy",

			"reco_posyTauL",
			"reco_negyTauL",

			"posLepSumChargedHadronsLV",
			"negLepSumChargedHadronsLV",
			"posLepSumNeutralHadronsLV",
			"negLepSumNeutralHadronsLV",

			"d0_refitPV_1",
			"d0_refitPVBS_1",
			"dZ_refitPV_1",
			"dZ_refitPVBS_1",
			"d0_refitPV_2",
			"d0_refitPVBS_2",
			"dZ_refitPV_2",
			"dZ_refitPVBS_2",
			#"recoImpactParameter1",
			#"recoImpactParameter2",

			"recoTrackRefError1",
			"recoTrackRefError2",

			"d0s_area",
			"d0s_dist"
			]
		if melaQuantities: s += klass.melaQuantities(m125=False)
		return s

	@staticmethod
	def recoCPQuantitiesHiggs():
		return [
			"madGraphLheParticle1LV",
			"madGraphLheParticle2LV",
			"madGraphLheParticle3LV",
			"madGraphLheParticle4LV",
			"madGraphLheParticle5LV",
			"madGraphLheParticle6LV",
			"madGraphLheParticle1PdgId",
			"madGraphLheParticle2PdgId",
			"madGraphLheParticle3PdgId",
			"madGraphLheParticle4PdgId",
			"madGraphLheParticle5PdgId",
			"madGraphLheParticle6PdgId",
			"subProcessCode",
			"lheParticleJetNumber"
		]

	@staticmethod
	def recoPolarisationQuantities():
		return [
			"lep1SumChargedHadronsLV",
			"lep1SumNeutralHadronsLV",

			"genMatchedTau1LV",
			"genMatchedTau1Found",
			"genMatchedTau1VisibleLV",
			"genMatchedTau1DecayMode",
			"genMatchedTau1NProngs",
			"genMatchedTau1NPi0s",

			"lep2SumChargedHadronsLV",
			"lep2SumNeutralHadronsLV",

			"genMatchedTau2LV",
			"genMatchedTau2Found",
			"genMatchedTau2VisibleLV",
			"genMatchedTau2DecayMode",
			"genMatchedTau2NProngs",
			"genMatchedTau2NPi0s",

			"leadingTauLV",
			"trailingTauLV",

			#"hhKinFitTau1LV",
			#"hhKinFitTau2LV",

			"simpleFitAvailable",
			"simpleFitLV",
			"simpleFitTau1Available",
			"simpleFitTau1LV",
			"simpleFitTau2Available",
			"simpleFitTau2LV",

			"leadingTauDecayMode",
			"leadingTauSumChargedHadronsLV",
			"leadingTauSumNeutralHadronsLV",

			"trailingTauDecayMode",
			"trailingTauSumChargedHadronsLV",
			"trailingTauSumNeutralHadronsLV",

			#"a1OmegaHHKinFit_1",
			#"a1OmegaHHKinFit_2",
			#"a1OmegaSimpleFit_1",
			#"a1OmegaSimpleFit_2",

			#"rhoNeutralChargedAsymmetry_1",
			#"rhoNeutralChargedAsymmetry_2",

			#"visibleOverFullEnergyHHKinFit_1",
			#"visibleOverFullEnergyHHKinFit_2",
			#"visibleOverFullEnergySimpleFit_1",
			#"visibleOverFullEnergySimpleFit_2",
			#"visibleToFullAngleHHKinFit_1",
			#"visibleToFullAngleHHKinFit_2",
			#"visibleToFullAngleSimpleFit_1",
			#"visibleToFullAngleSimpleFit_2",

			#"tauPolarisationDiscriminatorHHKinFit",
			#"tauPolarisationDiscriminatorSimpleFit",

			"polarisationOmegaGenMatched_1",
			"polarisationOmegaGenMatched_2",
			"polarisationOmegaSimpleFit_1",
			"polarisationOmegaSimpleFit_2",
			#"polarisationOmegaHHKinFit_1",
			#"polarisationOmegaHHKinFit_2",

			"polarisationOmegaBarGenMatched_1",
			"polarisationOmegaBarGenMatched_2",
			"polarisationOmegaBarSimpleFit_1",
			"polarisationOmegaBarSimpleFit_2",
			#"polarisationOmegaBarHHKinFit_1",
			#"polarisationOmegaBarHHKinFit_2",

			"polarisationOmegaVisibleGenMatched_1",
			"polarisationOmegaVisibleGenMatched_2",
			"polarisationOmegaVisibleSimpleFit_1",
			"polarisationOmegaVisibleSimpleFit_2",
			#"polarisationOmegaVisibleHHKinFit_1",
			#"polarisationOmegaVisibleHHKinFit_2",

			"polarisationCombinedOmegaGenMatched",
			"polarisationCombinedOmegaSimpleFit",
			#"polarisationCombinedOmegaHHKinFit",

			#"polarisationCombinedOmegaBarGenMatched",
			"polarisationCombinedOmegaBarSimpleFit",
			#"polarisationCombinedOmegaBarHHKinFit",

			"polarisationCombinedOmegaVisibleGenMatched",
			"polarisationCombinedOmegaVisibleSimpleFit",
			#"polarisationCombinedOmegaVisibleHHKinFit"
		]

	@staticmethod
	def recoPolarisationQuantitiesSvfit(m91=False):
		l= [
			"polarisationOmegaSvfit_1",
			"polarisationOmegaSvfit_2",
			"polarisationOmegaBarSvfit_1",
			"polarisationOmegaBarSvfit_2",
			"polarisationOmegaVisibleSvfit_1",
			"polarisationOmegaVisibleSvfit_2",
			"polarisationCombinedOmegaSvfit",
			"polarisationCombinedOmegaBarSvfit",
			"polarisationCombinedOmegaVisibleSvfit"]
		if m91:
			l+=[

				"polarisationOmegaSvfitM91_1",
				"polarisationOmegaSvfitM91_2",
				"polarisationOmegaBarSvfitM91_1",
				"polarisationOmegaBarSvfitM91_2",
				"polarisationOmegaVisibleSvfitM91_1",
				"polarisationOmegaVisibleSvfitM91_2",
				"polarisationCombinedOmegaSvfitM91",
				"polarisationCombinedOmegaBarSvfitM91",
				"polarisationCombinedOmegaVisibleSvfitM91"
			]
		return l

	@staticmethod
	def singleTauQuantities():
		return [
			"run",
			"lumi",
			"evt",
			"npv",
			"npu",
			"rho",
			"nLooseElectrons",
			"nLooseMuons",
			"nElectrons",
			"nMuons",
			"nTaus",
			"leadingElePt",
			"leadingEleEta",
			"leadingEleIso",
			"leadingEleIsoOverPt",
			"leadingMuonPt",
			"leadingMuonEta",
			"leadingMuonIso",
			"leadingMuonIsoOverPt",
			"leadingTauPt",
			"leadingTauEta",
			"leadingTauIso",
			"leadingTauIsoOverPt",
			"trailingTauPt",
			"trailingTauEta",
			"trailingTauIso",
			"trailingTauIsoOverPt",
			"diTauPt",
			"diTauEta",
			"diTauPhi",
			"diTauMass",
			"diTauSystemReconstructed",
			"weight",
			"collinearMass"
		]

	@staticmethod
	def minimalWeightQuantities():
		return [
			"hltWeight",
			"totalTriggerWeight",
			"triggerWeight_1",
			"triggerWeight_2",
			"identificationWeight_1",
			"identificationWeight_2",
			"puWeight",
			"tauEnergyScaleWeight",
			"generatorWeight",
			"crossSectionPerEventWeight",
			"numberGeneratedEventsWeight",
			"embeddingWeight",
			"eventWeight",
			"sampleStitchingWeight",
			"tauSpinnerWeight",
			"tauSpinnerWeight000",
			"tauSpinnerWeight005",
			"tauSpinnerWeight010",
			"tauSpinnerWeight015",
			"tauSpinnerWeight020",
			"tauSpinnerWeight025",
			"tauSpinnerWeight030",
			"tauSpinnerWeight035",
			"tauSpinnerWeight040",
			"tauSpinnerWeight045",
			"tauSpinnerWeight050",
			"tauSpinnerWeight055",
			"tauSpinnerWeight060",
			"tauSpinnerWeight065",
			"tauSpinnerWeight070",
			"tauSpinnerWeight075",
			"tauSpinnerWeight080",
			"tauSpinnerWeight085",
			"tauSpinnerWeight090",
			"tauSpinnerWeight095",
			"tauSpinnerWeight100",
			"tauSpinnerWeightSample",
			"tauSpinnerWeightInvSample",
			"antiEVLooseSFWeight_1",
			"antiELooseSFWeight_1",
			"antiEMediumSFWeight_1",
			"antiETightSFWeight_1",
			"antiEVTightSFWeight_1",
			"antiEVLooseSFWeight_2",
			"antiELooseSFWeight_2",
			"antiEMediumSFWeight_2",
			"antiETightSFWeight_2",
			"antiEVTightSFWeight_2",
			"emuQcdWeightUp",
			"emuQcdWeightNom",
			"emuQcdWeightDown",
			"emuQcdOsssWeight",
			"emuQcdOsssRateUpWeight",
			"emuQcdOsssRateDownWeight",
			"emuQcdOsssShapeUpWeight",
			"emuQcdOsssShapeDownWeight",
			"emuQcdExtrapUpWeight",
			"emuQcdExtrapDownWeight",
			"topPtReweightWeight",
			"topPtReweightWeightRun1",
			"topPtReweightWeightRun2",
			"zPtReweightWeight",
			"eleTauFakeRateWeight",
			"muTauFakeRateWeight",
			"metFilterWeight",
		]

	@staticmethod
	def madGraphWeightQuantities():
		return [
			"madGraphWeight000",
			"madGraphWeight010",
			"madGraphWeight020",
			"madGraphWeight030",
			"madGraphWeight040",
			"madGraphWeight050",
			"madGraphWeight060",
			"madGraphWeight070",
			"madGraphWeight080",
			"madGraphWeight090",
			"madGraphWeight100",
			"madGraphWeightSample",
			"madGraphWeightInvSample"
		]

	@classmethod
	def tauSpinnerWeightQuantities(klass):
		return [
			"tauSpinnerWeight",
			"tauSpinnerWeight000",
			"tauSpinnerWeight005",
			"tauSpinnerWeight010",
			"tauSpinnerWeight015",
			"tauSpinnerWeight020",
			"tauSpinnerWeight025",
			"tauSpinnerWeight030",
			"tauSpinnerWeight035",
			"tauSpinnerWeight040",
			"tauSpinnerWeight045",
			"tauSpinnerWeight050",
			"tauSpinnerWeight055",
			"tauSpinnerWeight060",
			"tauSpinnerWeight065",
			"tauSpinnerWeight070",
			"tauSpinnerWeight075",
			"tauSpinnerWeight080",
			"tauSpinnerWeight085",
			"tauSpinnerWeight090",
			"tauSpinnerWeight095",
			"tauSpinnerWeight100",
			"tauSpinnerWeightSample",
			"tauSpinnerWeightInvSample"
		]

	@classmethod
	def weightQuantities(klass, tauSpinner=True, minimalWeight=True, madGraphWeight=True):
		s = []
		if tauSpinner: s += klass.tauSpinnerWeightQuantities()
		if minimalWeight: s += klass.minimalWeightQuantities()
		if madGraphWeight: s += klass.madGraphWeightQuantities()
		return s

	@staticmethod
	def fakefactorQuantities():
		return [
		    "fakefactorWeight_comb_inclusive_1",
		    "fakefactorWeight_qcd_syst_up_inclusive_1",
		    "fakefactorWeight_qcd_syst_down_inclusive_1",
		    "fakefactorWeight_qcd_dm0_njet0_stat_up_inclusive_1",
		    "fakefactorWeight_qcd_dm0_njet0_stat_down_inclusive_1",
		    "fakefactorWeight_qcd_dm0_njet1_stat_up_inclusive_1",
		    "fakefactorWeight_qcd_dm0_njet1_stat_down_inclusive_1",
		    "fakefactorWeight_qcd_dm1_njet0_stat_up_inclusive_1",
		    "fakefactorWeight_qcd_dm1_njet0_stat_down_inclusive_1",
		    "fakefactorWeight_qcd_dm1_njet1_stat_up_inclusive_1",
		    "fakefactorWeight_qcd_dm1_njet1_stat_down_inclusive_1",
		    "fakefactorWeight_w_syst_up_inclusive_1",
		    "fakefactorWeight_w_syst_down_inclusive_1",
		    "fakefactorWeight_w_dm0_njet0_stat_up_inclusive_1",
		    "fakefactorWeight_w_dm0_njet0_stat_down_inclusive_1",
		    "fakefactorWeight_w_dm0_njet1_stat_up_inclusive_1",
		    "fakefactorWeight_w_dm0_njet1_stat_down_inclusive_1",
		    "fakefactorWeight_w_dm1_njet0_stat_up_inclusive_1",
		    "fakefactorWeight_w_dm1_njet0_stat_down_inclusive_1",
		    "fakefactorWeight_w_dm1_njet1_stat_up_inclusive_1",
		    "fakefactorWeight_w_dm1_njet1_stat_down_inclusive_1",
		    "fakefactorWeight_tt_syst_up_inclusive_1",
		    "fakefactorWeight_tt_syst_down_inclusive_1",
		    "fakefactorWeight_tt_dm0_njet0_stat_up_inclusive_1",
		    "fakefactorWeight_tt_dm0_njet0_stat_down_inclusive_1",
		    "fakefactorWeight_tt_dm0_njet1_stat_up_inclusive_1",
		    "fakefactorWeight_tt_dm0_njet1_stat_down_inclusive_1",
		    "fakefactorWeight_tt_dm1_njet0_stat_up_inclusive_1",
		    "fakefactorWeight_tt_dm1_njet0_stat_down_inclusive_1",
		    "fakefactorWeight_tt_dm1_njet1_stat_up_inclusive_1",
		    "fakefactorWeight_tt_dm1_njet1_stat_down_inclusive_1",



		    "fakefactorWeight_realtau_up_inclusive_1",
		    "fakefactorWeight_realtau_down_inclusive_1",

		    "fakefactorWeight_comb_inclusive_2",
		    "fakefactorWeight_qcd_syst_up_inclusive_2",
		    "fakefactorWeight_qcd_syst_down_inclusive_2",
		    "fakefactorWeight_qcd_dm0_njet0_stat_up_inclusive_2",
		    "fakefactorWeight_qcd_dm0_njet0_stat_down_inclusive_2",
		    "fakefactorWeight_qcd_dm0_njet1_stat_up_inclusive_2",
		    "fakefactorWeight_qcd_dm0_njet1_stat_down_inclusive_2",
		    "fakefactorWeight_qcd_dm1_njet0_stat_up_inclusive_2",
		    "fakefactorWeight_qcd_dm1_njet0_stat_down_inclusive_2",
		    "fakefactorWeight_qcd_dm1_njet1_stat_up_inclusive_2",
		    "fakefactorWeight_qcd_dm1_njet1_stat_down_inclusive_2",
		    "fakefactorWeight_w_syst_up_inclusive_2",
		    "fakefactorWeight_w_syst_down_inclusive_2",
		    "fakefactorWeight_w_dm0_njet0_stat_up_inclusive_2",
		    "fakefactorWeight_w_dm0_njet0_stat_down_inclusive_2",
		    "fakefactorWeight_w_dm0_njet1_stat_up_inclusive_2",
		    "fakefactorWeight_w_dm0_njet1_stat_down_inclusive_2",
		    "fakefactorWeight_w_dm1_njet0_stat_up_inclusive_2",
		    "fakefactorWeight_w_dm1_njet0_stat_down_inclusive_2",
		    "fakefactorWeight_w_dm1_njet1_stat_up_inclusive_2",
		    "fakefactorWeight_w_dm1_njet1_stat_down_inclusive_2",
		    "fakefactorWeight_tt_syst_up_inclusive_2",
		    "fakefactorWeight_tt_syst_down_inclusive_2",
		    "fakefactorWeight_tt_dm0_njet0_stat_up_inclusive_2",
		    "fakefactorWeight_tt_dm0_njet0_stat_down_inclusive_2",
		    "fakefactorWeight_tt_dm0_njet1_stat_up_inclusive_2",
		    "fakefactorWeight_tt_dm0_njet1_stat_down_inclusive_2",
		    "fakefactorWeight_tt_dm1_njet0_stat_up_inclusive_2",
		    "fakefactorWeight_tt_dm1_njet0_stat_down_inclusive_2",
		    "fakefactorWeight_tt_dm1_njet1_stat_up_inclusive_2",
		    "fakefactorWeight_tt_dm1_njet1_stat_down_inclusive_2",

		    #"fakefactorWeight_dy_frac_syst_up_inclusive_1",
		    #"fakefactorWeight_dy_frac_syst_down_inclusive_1",
		    #"fakefactorWeight_dy_frac_syst_up_inclusive_2",
		    #"fakefactorWeight_dy_frac_syst_down_inclusive_2",

		    "fakefactorWeight_realtau_up_inclusive_1",
		    "fakefactorWeight_realtau_down_inclusive_1",

		    "fakefactorWeight_realtau_up_inclusive_2",
		    "fakefactorWeight_realtau_down_inclusive_2",

		    "fakefactorWeight_w_frac_syst_up_inclusive_1",
		    "fakefactorWeight_tt_frac_syst_up_inclusive_1",

		    "fakefactorWeight_w_frac_syst_up_inclusive_2",
		    "fakefactorWeight_tt_frac_syst_up_inclusive_2",

		    "fakefactorWeight_w_frac_syst_down_inclusive_1",
		    "fakefactorWeight_tt_frac_syst_down_inclusive_1",

		    "fakefactorWeight_w_frac_syst_down_inclusive_2",
		    "fakefactorWeight_tt_frac_syst_down_inclusive_2"


		  ]

		#TODO if other wp or setting this can be added, but also producer has to be changed
		"""
		    "fakefactorWeight_comb_nobtag_tight",
		    "fakefactorWeight_qcd_syst_up_nobtag_tight",
		    "fakefactorWeight_qcd_syst_down_nobtag_tight",
		    "fakefactorWeight_qcd_dm0_njet0_stat_up_nobtag_tight",
		    "fakefactorWeight_qcd_dm0_njet0_stat_down_nobtag_tight",
		    "fakefactorWeight_qcd_dm0_njet1_stat_up_nobtag_tight",
		    "fakefactorWeight_qcd_dm0_njet1_stat_down_nobtag_tight",
		    "fakefactorWeight_qcd_dm1_njet0_stat_up_nobtag_tight",
		    "fakefactorWeight_qcd_dm1_njet0_stat_down_nobtag_tight",
		    "fakefactorWeight_qcd_dm1_njet1_stat_up_nobtag_tight",
		    "fakefactorWeight_qcd_dm1_njet1_stat_down_nobtag_tight",
		    "fakefactorWeight_w_syst_up_nobtag_tight",
		    "fakefactorWeight_w_syst_down_nobtag_tight",
		    "fakefactorWeight_w_dm0_njet0_stat_up_nobtag_tight",
		    "fakefactorWeight_w_dm0_njet0_stat_down_nobtag_tight",
		    "fakefactorWeight_w_dm0_njet1_stat_up_nobtag_tight",
		    "fakefactorWeight_w_dm0_njet1_stat_down_nobtag_tight",
		    "fakefactorWeight_w_dm1_njet0_stat_up_nobtag_tight",
		    "fakefactorWeight_w_dm1_njet0_stat_down_nobtag_tight",
		    "fakefactorWeight_w_dm1_njet1_stat_up_nobtag_tight",
		    "fakefactorWeight_w_dm1_njet1_stat_down_nobtag_tight",
		    "fakefactorWeight_tt_syst_up_nobtag_tight",
		    "fakefactorWeight_tt_syst_down_nobtag_tight",
		    "fakefactorWeight_tt_dm0_njet0_stat_up_nobtag_tight",
		    "fakefactorWeight_tt_dm0_njet0_stat_down_nobtag_tight",
		    "fakefactorWeight_tt_dm0_njet1_stat_up_nobtag_tight",
		    "fakefactorWeight_tt_dm0_njet1_stat_down_nobtag_tight",
		    "fakefactorWeight_tt_dm1_njet0_stat_up_nobtag_tight",
		    "fakefactorWeight_tt_dm1_njet0_stat_down_nobtag_tight",
		    "fakefactorWeight_tt_dm1_njet1_stat_up_nobtag_tight",
		    "fakefactorWeight_tt_dm1_njet1_stat_down_nobtag_tight",
		    "fakefactorWeight_comb_nobtag_loosemt",
		    "fakefactorWeight_qcd_syst_up_nobtag_loosemt",
		    "fakefactorWeight_qcd_syst_down_nobtag_loosemt",
		    "fakefactorWeight_qcd_dm0_njet0_stat_up_nobtag_loosemt",
		    "fakefactorWeight_qcd_dm0_njet0_stat_down_nobtag_loosemt",
		    "fakefactorWeight_qcd_dm0_njet1_stat_up_nobtag_loosemt",
		    "fakefactorWeight_qcd_dm0_njet1_stat_down_nobtag_loosemt",
		    "fakefactorWeight_qcd_dm1_njet0_stat_up_nobtag_loosemt",
		    "fakefactorWeight_qcd_dm1_njet0_stat_down_nobtag_loosemt",
		    "fakefactorWeight_qcd_dm1_njet1_stat_up_nobtag_loosemt",
		    "fakefactorWeight_qcd_dm1_njet1_stat_down_nobtag_loosemt",
		    "fakefactorWeight_w_syst_up_nobtag_loosemt",
		    "fakefactorWeight_w_syst_down_nobtag_loosemt",
		    "fakefactorWeight_w_dm0_njet0_stat_up_nobtag_loosemt",
		    "fakefactorWeight_w_dm0_njet0_stat_down_nobtag_loosemt",
		    "fakefactorWeight_w_dm0_njet1_stat_up_nobtag_loosemt",
		    "fakefactorWeight_w_dm0_njet1_stat_down_nobtag_loosemt",
		    "fakefactorWeight_w_dm1_njet0_stat_up_nobtag_loosemt",
		    "fakefactorWeight_w_dm1_njet0_stat_down_nobtag_loosemt",
		    "fakefactorWeight_w_dm1_njet1_stat_up_nobtag_loosemt",
		    "fakefactorWeight_w_dm1_njet1_stat_down_nobtag_loosemt",
		    "fakefactorWeight_tt_syst_up_nobtag_loosemt",
		    "fakefactorWeight_tt_syst_down_nobtag_loosemt",
		    "fakefactorWeight_tt_dm0_njet0_stat_up_nobtag_loosemt",
		    "fakefactorWeight_tt_dm0_njet0_stat_down_nobtag_loosemt",
		    "fakefactorWeight_tt_dm0_njet1_stat_up_nobtag_loosemt",
		    "fakefactorWeight_tt_dm0_njet1_stat_down_nobtag_loosemt",
		    "fakefactorWeight_tt_dm1_njet0_stat_up_nobtag_loosemt",
		    "fakefactorWeight_tt_dm1_njet0_stat_down_nobtag_loosemt",
		    "fakefactorWeight_tt_dm1_njet1_stat_up_nobtag_loosemt",
		    "fakefactorWeight_tt_dm1_njet1_stat_down_nobtag_loosemt",
		    "fakefactorWeight_comb_btag_tight",
		    "fakefactorWeight_qcd_syst_up_btag_tight",
		    "fakefactorWeight_qcd_syst_down_btag_tight",
		    "fakefactorWeight_qcd_dm0_njet0_stat_up_btag_tight",
		    "fakefactorWeight_qcd_dm0_njet0_stat_down_btag_tight",
		    "fakefactorWeight_qcd_dm0_njet1_stat_up_btag_tight",
		    "fakefactorWeight_qcd_dm0_njet1_stat_down_btag_tight",
		    "fakefactorWeight_qcd_dm1_njet0_stat_up_btag_tight",
		    "fakefactorWeight_qcd_dm1_njet0_stat_down_btag_tight",
		    "fakefactorWeight_qcd_dm1_njet1_stat_up_btag_tight",
		    "fakefactorWeight_qcd_dm1_njet1_stat_down_btag_tight",
		    "fakefactorWeight_w_syst_up_btag_tight",
		    "fakefactorWeight_w_syst_down_btag_tight",
		    "fakefactorWeight_w_dm0_njet0_stat_up_btag_tight",
		    "fakefactorWeight_w_dm0_njet0_stat_down_btag_tight",
		    "fakefactorWeight_w_dm0_njet1_stat_up_btag_tight",
		    "fakefactorWeight_w_dm0_njet1_stat_down_btag_tight",
		    "fakefactorWeight_w_dm1_njet0_stat_up_btag_tight",
		    "fakefactorWeight_w_dm1_njet0_stat_down_btag_tight",
		    "fakefactorWeight_w_dm1_njet1_stat_up_btag_tight",
		    "fakefactorWeight_w_dm1_njet1_stat_down_btag_tight",
		    "fakefactorWeight_tt_syst_up_btag_tight",
		    "fakefactorWeight_tt_syst_down_btag_tight",
		    "fakefactorWeight_tt_dm0_njet0_stat_up_btag_tight",
		    "fakefactorWeight_tt_dm0_njet0_stat_down_btag_tight",
		    "fakefactorWeight_tt_dm0_njet1_stat_up_btag_tight",
		    "fakefactorWeight_tt_dm0_njet1_stat_down_btag_tight",
		    "fakefactorWeight_tt_dm1_njet0_stat_up_btag_tight",
		    "fakefactorWeight_tt_dm1_njet0_stat_down_btag_tight",
		    "fakefactorWeight_tt_dm1_njet1_stat_up_btag_tight",
		    "fakefactorWeight_tt_dm1_njet1_stat_down_btag_tight",
		    "fakefactorWeight_comb_btag_loosemt",
		    "fakefactorWeight_qcd_syst_up_btag_loosemt",
		    "fakefactorWeight_qcd_syst_down_btag_loosemt",
		    "fakefactorWeight_qcd_dm0_njet0_stat_up_btag_loosemt",
		    "fakefactorWeight_qcd_dm0_njet0_stat_down_btag_loosemt",
		    "fakefactorWeight_qcd_dm0_njet1_stat_up_btag_loosemt",
		    "fakefactorWeight_qcd_dm0_njet1_stat_down_btag_loosemt",
		    "fakefactorWeight_qcd_dm1_njet0_stat_up_btag_loosemt",
		    "fakefactorWeight_qcd_dm1_njet0_stat_down_btag_loosemt",
		    "fakefactorWeight_qcd_dm1_njet1_stat_up_btag_loosemt",
		    "fakefactorWeight_qcd_dm1_njet1_stat_down_btag_loosemt",
		    "fakefactorWeight_w_syst_up_btag_loosemt",
		    "fakefactorWeight_w_syst_down_btag_loosemt",
		    "fakefactorWeight_w_dm0_njet0_stat_up_btag_loosemt",
		    "fakefactorWeight_w_dm0_njet0_stat_down_btag_loosemt",
		    "fakefactorWeight_w_dm0_njet1_stat_up_btag_loosemt",
		    "fakefactorWeight_w_dm0_njet1_stat_down_btag_loosemt",
		    "fakefactorWeight_w_dm1_njet0_stat_up_btag_loosemt",
		    "fakefactorWeight_w_dm1_njet0_stat_down_btag_loosemt",
		    "fakefactorWeight_w_dm1_njet1_stat_up_btag_loosemt",
		    "fakefactorWeight_w_dm1_njet1_stat_down_btag_loosemt",
		    "fakefactorWeight_tt_syst_up_btag_loosemt",
		    "fakefactorWeight_tt_syst_down_btag_loosemt",
		    "fakefactorWeight_tt_dm0_njet0_stat_up_btag_loosemt",
		    "fakefactorWeight_tt_dm0_njet0_stat_down_btag_loosemt",
		    "fakefactorWeight_tt_dm0_njet1_stat_up_btag_loosemt",
		    "fakefactorWeight_tt_dm0_njet1_stat_down_btag_loosemt",
		    "fakefactorWeight_tt_dm1_njet0_stat_up_btag_loosemt",
		    "fakefactorWeight_tt_dm1_njet0_stat_down_btag_loosemt",
		    "fakefactorWeight_tt_dm1_njet1_stat_up_btag_loosemt",
		    "fakefactorWeight_tt_dm1_njet1_stat_down_btag_loosemt",
		"""
