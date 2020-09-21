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

	def build_quantities(self, nickname, channel, legacy=True):

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

			if re.search("Embedding(2016|2017)", nickname):
				self.quantities.update(self.genQuantities())
				self.quantities.update(self.genCPQuantities())
				self.quantities.update(["tauSpinnerPolarisation"])

		else:
			# common for all channels and datasets
			self.quantities.update(['nDiTauPairCandidates', 'nLooseElectrons', 'nAllDiTauPairCandidates', 'nLooseMuons'])
			self.quantities.update(self.fourVectorQuantities())
			self.quantities.update(self.syncQuantities(nickname))
			self.quantities.update(self.CPInitialStateQuantities())
			self.quantities.update(self.CPSyncQuantities(nickname))
			self.quantities.update(self.RooWorkSpaceWeightQuantities(nickname, channel, legacy))
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
				elif re.search("Embedding2016", nickname):
					self.quantities.update([
						"triggerWeight_doublemu_1",
						"isoweight_1",
						"idweight_1",
						"triggerWeight_singleE_1",
					])

			elif channel == "MT":
				if re.search("(Autumn18|Run2018|Embedding2018)", nickname):
					self.quantities.update(["trg_singlemuon_24", "trg_singlemuon_27", "trg_crossmuon_mu20tau27"])
				elif re.search("(Summer17|Fall17|Run2017|Embedding2017)", nickname):
					self.quantities.update(["HLT_IsoMu24","HLT_IsoMu27","HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1"])
					self.quantities.update(["trg_singlemuon_24", "trg_singlemuon_27", "trg_crossmuon_mu20tau27"])
					#self.quantities.update(["matched_HLT_IsoMu24","matched_HLT_IsoMu27","matched_HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1"])
				elif re.search("Embedding2016", nickname):
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
			elif channel == "TT":
				if re.search("(Summer17|Fall17|Run2017|Embedding2017)", nickname):
					self.quantities.update([
						"HLT_DoubleTightChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg",
						"HLT_DoubleMediumChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg",
						"HLT_DoubleTightChargedIsoPFTau40_Trk1_eta2p1_Reg"
					])
					self.quantities.update([
						"trg_doubletau_35_tightiso_tightid",
						"trg_doubletau_40_mediso_tightid",
						"trg_doubletau_40_tightiso",
					])
				if re.search("(Autumn18|Run2018|Embedding2018)", nickname):
					self.quantities.update([
						"HLT_DoubleMediumChargedIsoPFTauHPS35_Trk1_eta2p1_Reg",
					])
					self.quantities.update([
						"trg_doubletau_35_mediso",
					])
					if re.search("(Run2018|Embedding2018)", nickname):
						self.quantities.update([
							"HLT_DoubleTightChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg",
							"HLT_DoubleMediumChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg",
							"HLT_DoubleTightChargedIsoPFTau40_Trk1_eta2p1_Reg",
							])
						self.quantities.update([
							"trg_doubletau_35_tightiso_tightid",
							"trg_doubletau_40_mediso_tightid",
							"trg_doubletau_40_tightiso",
						])
				if re.search("Embedding2016", nickname):
					self.quantities.update([
						"triggerWeight_doublemu_1",
						"triggerWeight_tau_1",
						"triggerWeight_tau_2"
					])

			if not channel == "EM":
				self.quantities.update(self.fakefactorQuantities(legacy))

				# if re.search("(Summer17|Fall17)", nickname):
				# 	self.quantities.update(self.tauTriggerEfficiencies2017Quantities())

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
						self.quantities.update(self.recoCPQuantities(melaQuantities=False))

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

				if not channel == "MM":
					self.quantities.update(self.recoPolarisationQuantitiesSvfit())
					self.quantities.update(self.recoPolarisationQuantities())
					self.quantities.update(self.genPolarisationQuantities())

				if channel == "MM":
					self.quantities.update(self.singleTauQuantities())
					self.quantities.update(self.weightQuantities(tauSpinner=False, minimalWeight=True, madGraphWeight=False))

				else:

					self.quantities.update(self.svfitSyncQuantities())
					self.quantities.update(self.fastmttQuantities())
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
				if not channel == "MM" and re.search('(HTo.*TauTau|H2JetsToTauTau|Higgs|JJHiggs).*(?=(Spring16|Summer16|Summer17|Fall17|Autumn18))', nickname):
					self.quantities.update(self.genMatchedCPQuantities())

					if re.search("(Run2017|Summer17|Fall17|Run2018|Autumn18)", nickname) == None:
						#self.quantities.update(self.splitJecUncertaintyQuantities())
						self.quantities.update(self.genHiggsQuantities()) #no lhe in 2017 skim
					if re.search("amcatnlo",nickname):
						self.quantities.update(["lhenpNLO", "quarkmassWeight","quarkmassUpWeight","quarkmassDownWeight"])
					self.quantities.update(self.genQuantities(LFV = False))
					self.quantities.update(self.svfitSyncQuantities())
					self.quantities.update(self.fastmttQuantities())
					self.quantities.update(self.recoCPQuantities(melaQuantities=False))
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
					self.quantities.update(self.genPolarisationQuantities())
					self.quantities.update(self.genQuantities(LFV = False))
					self.quantities.update(self.weightQuantities(tauSpinner=True, minimalWeight=True, madGraphWeight=True))
					#self.quantities.update(self.splitJecUncertaintyQuantities())

				elif not channel == "MM" and re.search('(HTo.*TauTau|H2JetsToTauTau|Higgs).*(?=Fall15)', nickname):
					# self.quantities.update(set(['melaProbCPOddVBF', 'melaDiscriminatorDCPGGH', 'melaM125ProbCPEvenGGH', 'melaProbCPMixVBF', 'melaM125ProbCPMixVBF', 'melaM125DiscriminatorDCPVBF', 'melaDiscriminatorD0MinusGGH', 'melaDiscriminatorD0MinusVBF', 'melaProbCPEvenGGH', 'melaM125ProbCPEvenVBF', 'melaM125ProbCPMixGGH', 'melaProbCPOddGGH', 'melaDiscriminatorDCPVBF', 'melaM125ProbCPOddGGH', 'melaM125DiscriminatorDCPGGH', 'melaProbCPMixGGH', 'melaProbCPEvenVBF', 'melaM125DiscriminatorD0MinusGGH', 'melaM125ProbCPOddVBF', 'melaM125DiscriminatorD0MinusVBF']))
					self.quantities.update(self.recoCPQuantitiesHiggs())
					self.quantities.update(self.genHiggsQuantities())
					self.quantities.update(self.genQuantities(LFV = False))
					self.quantities.update(self.svfitSyncQuantities())
					self.quantities.update(self.fastmttQuantities())
					self.quantities.update(self.genMatchedCPQuantities())
					self.quantities.update(self.weightQuantities(tauSpinner=True, minimalWeight=True, madGraphWeight=True))
					# if channel in ["TT", "MT", "ET"]:
					# 	self.quantities.update(set(['#tauPolarisationTMVA', '#tauPolarisationSKLEARN']))
					if channel in ["ET"]: self.quantities.add('nVetoElectrons')
					if channel in ["MT"]: self.quantities.add('nVetoMuons')

				elif not channel == "MM" and re.search('(DY.?JetsToLL).*(?=Fall15)', nickname):
					self.quantities.add('tauSpinnerPolarisation')
					self.quantities.update(self.recoPolarisationQuantities())
					self.quantities.update(self.genPolarisationQuantities())
					self.quantities.update(self.genQuantities(LFV = False))
					self.quantities.update(self.genMatchedCPQuantities())
					self.quantities.update(self.weightQuantities(tauSpinner=True, minimalWeight=True, madGraphWeight=True))
					if channel == "ET": self.quantities.add('nVetoElectrons')
					if channel in ["MT"]: self.quantities.add('nVetoMuons')

				elif not channel == "MM" and re.search('^((?!(DY.?JetsToLL|HTo.*TauTau|H2JetsToTauTau|Higgs)).)*Fall15', nickname):
					self.quantities.update(self.recoPolarisationQuantities())
					self.quantities.update(self.genPolarisationQuantities())
					self.quantities.update(self.weightQuantities(tauSpinner=True, minimalWeight=True, madGraphWeight=True))
					if channel == "ET": self.quantities.add('nVetoElectrons')
					if channel in ["MT"]: self.quantities.add('nVetoMuons')

				else: # data, 2016/2017/2018 wjets, ttbar, diboson
					self.quantities.update(self.recoCPQuantities(melaQuantities=False))

					if channel == "MM":
						self.quantities.update(self.singleTauQuantities())
						self.quantities.update(self.weightQuantities(tauSpinner=False, minimalWeight=True, madGraphWeight=False))

					else:
						self.quantities.update(self.svfitSyncQuantities())
						self.quantities.update(self.fastmttQuantities())
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
			"genPV",
			"genPhiStarCP",
			"genPhiStar",
			"genOStarCP",
			"genPhiCP",
			"genPhi",
			"genOCP",
			"genPhiStarCPComb",
			"genPhiCPLab",

			"genIP1",
			"genIP2",

			"genCosPsiPlus",
			"genCosPsiMinus",
			"genCosPsiPlus",
			"genCosPsiMinus",
			"genPhiStarCPRho",
			"genPhiCPRho",
			"genPhiStarRho",
			"genPhiRho",
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
			"genPV",
			"genSV1x",
			"genSV1y",
			"genSV1z",
			"genSV2x",
			"genSV2y",
			"genSV2z",

			"genD01",
			"genD02",

			"genIP1",
			"genIP2",

			"genCosPsiPlus",
			"genCosPsiMinus",
			"genPhiStarCP",
			"genPhiStar",
			"genOStarCP",
			"genPhiStarCPComb",
			"genPhiStarCPRho",
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
			"nominalPV",
			"nominalPVchi2",
			"nominalPVnDOF",
			"nominalPVnTracks",
			"nominalPVsigmaxx",
			"nominalPVsigmayy",
			"nominalPVsigmazz",
			"nominalPVsigmaxy",
			"nominalPVsigmaxz",
			"nominalPVsigmayz",

			"refitPV",
			"refitPVchi2OverNdof",
			"refitPVnTracks",
			"refitPVsigmaxx",
			"refitPVsigmayy",
			"refitPVsigmazz",
			"refitPVsigmaxy",
			"refitPVsigmaxz",
			"refitPVsigmayz",

			"refitPVBS",
			"refitPVBSnTracks",
			"refitPVBSsigmaxx",
			"refitPVBSsigmayy",
			"refitPVBSsigmazz",
			"refitPVBSsigmaxy",
			"refitPVBSsigmaxz",
			"refitPVBSsigmayz",

			"theBS",
			"theBSsigmax",
			"theBSsigmay",
			"theBSsigmaz",
			"theBSdxdz",
			"theBSdydz",
			"theBSatRef1",
			"theBSatRef2",
			"theBSatnominalPV",
			"dxy_BSatRef1",
			"dxy_BSatRef2",
			"dxy_BSatnominalPV_1",
			"dxy_BSatnominalPV_2",

			"refP1",
			"refP2",

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

			"track1p4",
			"track2p4",

			"d3DrPV_1",
			"err3DrPV_1",
			"d2DrPV_1",
			"err2DrPV_1",
			"d3DrPV_2",
			"err3DrPV_2",
			"d2DrPV_2",
			"err2DrPV_2",

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

			"errD0rPV_1",
			"errD0rPV_2",

			"errDZrPV_1",
			"errDZrPV_2",

			"errIPrPV_1",
			"errIPrPV_2",

			"IP_1",
			"IP_2",
			# "PVdistanceToPCA1",
			# "PVdistanceToPCA2",
                        "IPSignificance_1",
                        "IPSignificance_2",

			"IPrPV_1",
			"IPrPV_2",
			# "PVdistanceToPCArPV_1",
			# "PVdistanceToPCArPV_2",
                        "IPSignificancerPV_1",
                        "IPSignificancerPV_2",

			"IPHel_1",
			"IPHel_2",
                        "IPSignificanceHel_1",
                        "IPSignificanceHel_2",
                        "IPSignificanceHel_Track_1",
                        "IPSignificanceHel_Track_2",
                        "IPSignificanceHel_PV_1",
                        "IPSignificanceHel_PV_2",

			"IPHelrPV_1",
			"IPHelrPV_2",
                        "IPSignificanceHelrPV_1",
                        "IPSignificanceHelrPV_2",
                        "IPSignificanceHelrPV_Track_1",
                        "IPSignificanceHelrPV_Track_2",
                        "IPSignificanceHelrPV_PV_1",
                        "IPSignificanceHelrPV_PV_2",

			"IPrPVBS_1",
			"IPrPVBS_2",
			# "PVdistanceToPCArPVBS_1",
			# "PVdistanceToPCArPVBS_2",
                        "IPSignificancerPVBS_1",
                        "IPSignificancerPVBS_2",

			"IPHelrPVBS_1",
			"IPHelrPVBS_2",
                        "IPSignificanceHelrPVBS_1",
                        "IPSignificanceHelrPVBS_2",
                        "IPSignificanceHelrPVBS_Track_1",
                        "IPSignificanceHelrPVBS_Track_2",
                        "IPSignificanceHelrPVBS_PV_1",
                        "IPSignificanceHelrPVBS_PV_2",

			"recoIPHelCovxx_1",
			"recoIPHelCovxy_1",
			"recoIPHelCovxz_1",
			"recoIPHelCovyy_1",
			"recoIPHelCovyz_1",
			"recoIPHelCovxy_2",
			"recoIPHelCovxz_2",
			"recoIPHelCovyy_2",
			"recoIPHelCovyz_2",
			"recoIPHelCovzz_2",

			"recoIPHelrPVCovxx_1",
			"recoIPHelrPVCovxy_1",
			"recoIPHelrPVCovxz_1",
			"recoIPHelrPVCovyy_1",
			"recoIPHelrPVCovyz_1",
			"recoIPHelrPVCovzz_1",
			"recoIPHelrPVCovxx_2",
			"recoIPHelrPVCovxy_2",
			"recoIPHelrPVCovxz_2",
			"recoIPHelrPVCovyy_2",
			"recoIPHelrPVCovyz_2",
			"recoIPHelrPVCovzz_2",


			"trackFromBS_1",
			"trackFromBS_2",

			"cosPsiPlus",
			"cosPsiMinus",

			"deltaEtaGenRecoIP_1",
			"deltaEtaGenRecoIP_2",
			"deltaPhiGenRecoIP_1",
			"deltaPhiGenRecoIP_2",
			"deltaRGenRecoIP_1",
			"deltaRGenRecoIP_2",
			"deltaGenRecoIP_1",
			"deltaGenRecoIP_2",

			"deltaEtaGenRecoIPHel_1",
			"deltaEtaGenRecoIPHel_2",
			"deltaPhiGenRecoIPHel_1",
			"deltaPhiGenRecoIPHel_2",
			"deltaRGenRecoIPHel_1",
			"deltaRGenRecoIPHel_2",
			"deltaGenRecoIPHel_1",
			"deltaGenRecoIPHel_2",

			"deltaEtaGenRecoIPHelrPV_1",
			"deltaEtaGenRecoIPHelrPV_2",
			"deltaPhiGenRecoIPHelrPV_1",
			"deltaPhiGenRecoIPHelrPV_2",
			"deltaRGenRecoIPHelrPV_1",
			"deltaRGenRecoIPHelrPV_2",
			"deltaGenRecoIPHelrPV_1",
			"deltaGenRecoIPHelrPV_2",

			"deltaEtaGenRecoIPrPV_1",
			"deltaEtaGenRecoIPrPV_2",
			"deltaPhiGenRecoIPrPV_1",
			"deltaPhiGenRecoIPrPV_2",
			"deltaRGenRecoIPrPV_1",
			"deltaRGenRecoIPrPV_2",
			"deltaGenRecoIPrPV_1",
			"deltaGenRecoIPrPV_2",

			"recoPhiStarCP",
			"recoPhiStarCPRho",
			"recoPhiStarCPRhoMerged",
			"recoPhiStarCPrPV",
			"recoPhiStarCPrPVBS",
			"recoPhiStarCPHel",
			"recoPhiStarCPHelrPV",
			"recoPhiStarCPHelrPVBS",

			"recoPhiStarCPComb",
			"recoPhiStarCPCombMerged",

			"acotautau_00", #phi*CP IP-IP
			"acotautau_01", #phi*CP IP-DP
			"acotautau_11", #phi*CP DP-DP

			"recoPhiPlusIPMeth",
			"recoPhiMinusIPMeth",
			"recoPhiStarPlusIPMeth",
			"recoPhiStarMinusIPMeth",
			"recoPhiPlusCombMeth",
			"recoPhiMinusCombMeth",
			"recoPhiStarPlusCombMeth",
			"recoPhiStarMinusCombMeth",
			"recoPhiPlusRhoMeth",
			"recoPhiMinusRhoMeth",
			"recoPhiStarPlusRhoMeth",
			"recoPhiStarMinusRhoMeth",

			"recoPhiStar",
			"recoPhiStarRho",
			"recoChargedHadron1HiggsFrameEnergy",
			"recoChargedHadron2HiggsFrameEnergy",

			"reco_posyTauL",
			"reco_negyTauL",

			"posLepSumChargedHadronsLV",
			"negLepSumChargedHadronsLV",
			"posLepSumNeutralHadronsLV",
			"negLepSumNeutralHadronsLV",

			"d0rPV_1",
			"d0rPVBS_1",
			"dZrPV_1",
			"dZrPVBS_1",
			"d0rPV_2",
			"d0rPVBS_2",
			"dZrPV_2",
			"dZrPVBS_2",
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

			# "genMatchedTau1LV",
			# "genMatchedTau1Found",
			# "genMatchedTau1VisibleLV",
			# "genMatchedTau1DecayMode",
			# "genMatchedTau1NProngs",
			# "genMatchedTau1NPi0s",

			"lep2SumChargedHadronsLV",
			"lep2SumNeutralHadronsLV",

			# "genMatchedTau2LV",
			# "genMatchedTau2Found",
			# "genMatchedTau2VisibleLV",
			# "genMatchedTau2DecayMode",
			# "genMatchedTau2NProngs",
			# "genMatchedTau2NPi0s",

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

			# "polarisationOmegaGenMatched_1",
			# "polarisationOmegaGenMatched_2",
			"polarisationOmegaSimpleFit_1",
			"polarisationOmegaSimpleFit_2",
			#"polarisationOmegaHHKinFit_1",
			#"polarisationOmegaHHKinFit_2",

			# "polarisationOmegaBarGenMatched_1",
			# "polarisationOmegaBarGenMatched_2",
			"polarisationOmegaBarSimpleFit_1",
			"polarisationOmegaBarSimpleFit_2",
			#"polarisationOmegaBarHHKinFit_1",
			#"polarisationOmegaBarHHKinFit_2",

			# "polarisationOmegaVisibleGenMatched_1",
			# "polarisationOmegaVisibleGenMatched_2",
			"polarisationOmegaVisibleSimpleFit_1",
			"polarisationOmegaVisibleSimpleFit_2",
			#"polarisationOmegaVisibleHHKinFit_1",
			#"polarisationOmegaVisibleHHKinFit_2",

			# "polarisationCombinedOmegaGenMatched",
			"polarisationCombinedOmegaSimpleFit",
			#"polarisationCombinedOmegaHHKinFit",

			#"polarisationCombinedOmegaBarGenMatched",
			"polarisationCombinedOmegaBarSimpleFit",
			#"polarisationCombinedOmegaBarHHKinFit",

			# "polarisationCombinedOmegaVisibleGenMatched",
			"polarisationCombinedOmegaVisibleSimpleFit",
			#"polarisationCombinedOmegaVisibleHHKinFit"
		]

	@staticmethod
	def genPolarisationQuantities():
		return [
			"genMatchedTau1LV",
			"genMatchedTau1Found",
			"genMatchedTau1VisibleLV",
			"genMatchedTau1DecayMode",
			"genMatchedTau1NProngs",
			"genMatchedTau1NPi0s",
			"genMatchedTau2LV",
			"genMatchedTau2Found",
			"genMatchedTau2VisibleLV",
			"genMatchedTau2DecayMode",
			"genMatchedTau2NProngs",
			"genMatchedTau2NPi0s",
			"polarisationOmegaGenMatched_1",
			"polarisationOmegaGenMatched_2",
			"polarisationOmegaBarGenMatched_1",
			"polarisationOmegaBarGenMatched_2",
			"polarisationOmegaVisibleGenMatched_1",
			"polarisationOmegaVisibleGenMatched_2",
			"polarisationCombinedOmegaGenMatched",
			#"polarisationCombinedOmegaBarGenMatched",
			"polarisationCombinedOmegaVisibleGenMatched",
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
	def fakefactorQuantities(legacy=True):
		if legacy:
			return [
				"ffWeight_medium_dmbins_1",
				"ffWeight_medium_mvadmbins_1",
				"ffWeight_medium_mvadmbins_nosig_1",
				"ffWeight_tight_dmbins_1",
				"ffWeight_tight_mvadmbins_1",
				"ffWeight_tight_mvadmbins_nosig_1",
				"ffWeight_vtight_dmbins_1",
				"ffWeight_vtight_mvadmbins_1",
				"ffWeight_vtight_mvadmbins_nosig_1",

				"ffWeight_medium_dmbins_2",
				"ffWeight_medium_mvadmbins_2",
				"ffWeight_medium_mvadmbins_nosig_2",
				"ffWeight_tight_dmbins_2",
				"ffWeight_tight_mvadmbins_2",
				"ffWeight_tight_mvadmbins_nosig_2",
				"ffWeight_vtight_dmbins_2",
				"ffWeight_vtight_mvadmbins_2",
				"ffWeight_vtight_mvadmbins_nosig_2",
			]
		else:
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

	@staticmethod
	def tauTriggerEfficiencies2017Quantities():
		return [
			"tautriggerefficiencyData_1_vloose",
			"tautriggerefficiencyData_1_loose",
			"tautriggerefficiencyData_1_medium",
			"tautriggerefficiencyData_1_tight",
			"tautriggerefficiencyData_1_vtight",
			"tautriggerefficiencyData_1_vvtight",
			"tautriggerefficiencyData_2_vloose",
			"tautriggerefficiencyData_2_loose",
			"tautriggerefficiencyData_2_medium",
			"tautriggerefficiencyData_2_tight",
			"tautriggerefficiencyData_2_vtight",
			"tautriggerefficiencyData_2_vvtight",

			"tautriggerefficiencyMC_1_vloose",
			"tautriggerefficiencyMC_1_loose",
			"tautriggerefficiencyMC_1_medium",
			"tautriggerefficiencyMC_1_tight",
			"tautriggerefficiencyMC_1_vtight",
			"tautriggerefficiencyMC_1_vvtight",
			"tautriggerefficiencyMC_2_vloose",
			"tautriggerefficiencyMC_2_loose",
			"tautriggerefficiencyMC_2_medium",
			"tautriggerefficiencyMC_2_tight",
			"tautriggerefficiencyMC_2_vtight",
			"tautriggerefficiencyMC_2_vvtight",
			]

	@staticmethod
	def RooWorkSpaceWeightQuantities(nickname, channel, legacy):
		if legacy:
			if channel == "ET":
				return [
					"triggerWeight_single_1",
					"triggerWeight_cross_1",
					"triggerWeight_cross_2",
					"triggerWeight_comb",
				]
			elif channel == "MT":
				return [
					"triggerWeight_single_1",
					"triggerWeight_cross_1",
					"triggerWeight_cross_2",
					"triggerWeight_comb",
				]
			elif channel == "TT":
				return [
					"triggerWeight_cross_1",
					"triggerWeight_cross_2",
					"triggerWeight_comb",
				]
			elif channel == "MM":
				return [
					"triggerWeight_single_1",
					"trg_singlemuon_24",
					"trg_singlemuon_27",
				]
		else:
			if channel == "ET":
				if re.search("Embedding2017", nickname):
					return [
						"triggerWeight_doublemu_1",
						"idweight_doublemu_1",
						"idweight_doublemu_2",
						"isoweight_1",
						"idweight_1",
						"triggerWeight_trg27_trg32_trg35_embed_1",
						"triggerWeight_trg_EleTau_Ele24Leg_embed_1",
						"triggerWeight_tauLeg_2",
						"triggerWeight_trg27_trg32_trg35_data_1",
						"triggerWeight_trg_EleTau_Ele24Leg_data_1",
						"tautriggerefficiencyData_2",
					]
				else:
					return [
						#"HLT_Ele32_WPTight_Gsf",
						"HLT_Ele35_WPTight_Gsf",
						"HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTau30_eta2p1_CrossL1",
						"triggerWeight_singleE_1",
						"triggerWeight_etaucross_1",
						"triggerWeight_etaucross_2",
						"triggerWeight_etaucross_vloose_2",
						"triggerWeight_etaucross_loose_2",
						"triggerWeight_etaucross_medium_2",
						"triggerWeight_etaucross_tight_2",
						"triggerWeight_etaucross_vtight_2",
						"triggerWeight_etaucross_vvtight_2",
					]
			elif channel == "MT":
				if re.search("Embedding2017", nickname):
					return [
						"triggerWeight_doublemu_1",
						"idweight_doublemu_1",
						"idweight_doublemu_2",
						"isoweight_1",
						"idweight_1",
						"triggerWeight_mu_1",
						"triggerWeight_mutaucross_1",
						"triggerWeight_mutaucross_2",
					]
				else:
					return [
						"triggerWeight_mu_1",
						"triggerWeight_mutaucross_1",
						"triggerWeight_mutaucross_2",
						"triggerWeight_mutaucross_vloose_2",
						"triggerWeight_mutaucross_loose_2",
						"triggerWeight_mutaucross_medium_2",
						"triggerWeight_mutaucross_tight_2",
						"triggerWeight_mutaucross_vtight_2",
						"triggerWeight_mutaucross_vvtight_2",
					]
			elif channel == "TT":
				if re.search("Embedding2017", nickname):
					return [
						"triggerWeight_doublemu_1",
						"idweight_doublemu_1",
						"idweight_doublemu_2",
						"triggerWeight_tau_1",
						"triggerWeight_tau_2",
					]
				else:
					return [
						"triggerWeight_tautaucross_1",
						"triggerWeight_tautaucross_2",
						"triggerWeight_tautaucross_vloose_1",
						"triggerWeight_tautaucross_loose_1",
						"triggerWeight_tautaucross_medium_1",
						"triggerWeight_tautaucross_tight_1",
						"triggerWeight_tautaucross_vtight_1",
						"triggerWeight_tautaucross_vvtight_1",
						"triggerWeight_tautaucross_vloose_2",
						"triggerWeight_tautaucross_loose_2",
						"triggerWeight_tautaucross_medium_2",
						"triggerWeight_tautaucross_tight_2",
						"triggerWeight_tautaucross_vtight_2",
						"triggerWeight_tautaucross_vvtight_2",
					]
