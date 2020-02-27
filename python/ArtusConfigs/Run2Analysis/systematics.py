# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import re
import sys

import HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Run2Analysis.Includes.settingsJECUncertaintySplit as sJECUS


class Systematics_Config(dict):
	def __init__(self, nickname):

		#Nominal the clear config function is also just a copy of this. (caution python does strange things when updating a dict!!!!)
		self["ElectronEnergyCorrectionShiftEB"] = 1.0
		self["ElectronEnergyCorrectionShiftEE"] = 1.0
		self["JetEnergyCorrectionUncertaintyShift"] = 0.0
		self["MetUncertaintyShift"] = False
		self["MetUncertaintyType"] = ""
		self["SvfitCacheFileFolder"] = "nominal"
		self["TauElectronFakeEnergyCorrection"] = 1.0

		self["TauElectronFakeEnergyCorrectionOneProngPiZerosShift"] = 0.0
		self["TauElectronFakeEnergyCorrectionOneProngShift"] = 0.0

		self["TauEnergyCorrectionOneProngPiZerosShift"] = 0.0
		self["TauEnergyCorrectionOneProngShift"] = 0.0
		self["TauEnergyCorrectionShift"] = 0.0
		self["TauEnergyCorrectionThreeProngShift"] = 0.0
		self["TauEnergyCorrectionThreeProngPiZerosShift"] = 0.0

		self["TauJetFakeEnergyCorrection"] = 0.0

		self["TauMuonFakeEnergyCorrection"] = 0.0

		self["TauMuonFakeEnergyCorrectionOneProngPiZerosShift"] = 0.0
		self["TauMuonFakeEnergyCorrectionOneProngShift"] = 0.0

		self.JECUncertaintySplit_config = sJECUS.JECUncertaintySplit(nickname)
		self.update(self.JECUncertaintySplit_config)
		self["DoJecGroupings"] = False

		#CP FINAL STATE UNCERTAINTIES
		self["MuonEnergyCorrectionShiftEta0p4to1p2"] = 1.0
		self["MuonEnergyCorrectionShiftEta1p2to2p1"] = 1.0
		self["MuonEnergyCorrectionShiftEtaGt2p1"] = 1.0


	#for each systematic shift if statement which changes the config accordingly
	def build_systematic_config(self, nickname, systematic_uncertainty, legacy, *args, **kwargs):
		log.debug("SYST= " + systematic_uncertainty)
		#Jet uncertainties:

		if "eta0to5" in systematic_uncertainty:
			self.JECUncertaintySplit_config.group_eta0to5()
			self.update(self.JECUncertaintySplit_config)
			self["DoJecGroupings"] = True #will only run if no met-
			if "Down" in systematic_uncertainty:
				self["IsShiftUp"] = False
			elif "Up" in systematic_uncertainty:
				self["IsShiftUp"] = True
			if "Uncorrelated" in systematic_uncertainty:
				self["IsCorrelated"] = False
			else:
				self["IsCorrelated"] = True
		elif "eta0to3" in systematic_uncertainty:
			self.JECUncertaintySplit_config.group_eta0to3()
			self.update(self.JECUncertaintySplit_config)
			self["DoJecGroupings"] = True
			if "Down" in systematic_uncertainty:
				self["IsShiftUp"] = False
			elif "Up" in systematic_uncertainty:
				self["IsShiftUp"] = True
			if "Uncorrelated" in systematic_uncertainty:
				self["IsCorrelated"] = False
			else:
				self["IsCorrelated"] = True


		elif "eta3to5" in systematic_uncertainty:
			self.JECUncertaintySplit_config.group_eta3to5()
			self.update(self.JECUncertaintySplit_config)
			self["DoJecGroupings"] = True
			if "Down" in systematic_uncertainty:
				self["IsShiftUp"] = False
			elif "Up" in systematic_uncertainty:
				self["IsShiftUp"] = True
			if "Uncorrelated" in systematic_uncertainty:
				self["IsCorrelated"] = False
			else:
				self["IsCorrelated"] = True
		elif "relativeBal" in systematic_uncertainty:
			self.JECUncertaintySplit_config.group_relativebal()
			self.update(self.JECUncertaintySplit_config)
			self["DoJecGroupings"] = True
			if "Down" in systematic_uncertainty:
				self["IsShiftUp"] = False
			elif "Up" in systematic_uncertainty:
				self["IsShiftUp"] = True
			#50 % correlated, however this results in the same shape for corr and uncorr (1-0.5)=0.5
			self["IsCorrelated"] = True

		elif "relativeSample" in systematic_uncertainty: #only for 2017
			self.JECUncertaintySplit_config.group_relativesample()
			self.update(self.JECUncertaintySplit_config)
			self["DoJecGroupings"] = True
			if "Down" in systematic_uncertainty:
				self["IsShiftUp"] = False
			elif "Up" in systematic_uncertainty:
				self["IsShiftUp"] = True
			#only in 2017 so 0% correlated
			self["IsCorrelated"] = False

		elif re.search("Run201", nickname) == None:    #data has no systematic
			print "not a JEC"
			#I dont remember why I did this, it looks wrong if re.search("JetEnergyCorrectionSplitUncertainty", nickname):
			if systematic_uncertainty == "eleEsUp":

				if re.search("Spring16|Summer16|Embedding(2016|2017)|Fall17", nickname):
					self["ElectronEnergyCorrectionShiftEB"] = 1.01
					self["ElectronEnergyCorrectionShiftEE"] = 1.025
					self["SvfitCacheFileFolder"] = "eleEsUp"
				else:
					self["ElectronEnergyCorrectionShiftEB"] = 1.0
					self["ElectronEnergyCorrectionShiftEE"] = 1.0
					self["SvfitCacheFileFolder"] = "nominal"

			elif systematic_uncertainty == "eleEsDown":
				if re.search("Spring16|Summer16|Embedding(2016|2017)|Fall17", nickname):
					self["ElectronEnergyCorrectionShiftEB"] =  0.99
					self["ElectronEnergyCorrectionShiftEE"] = 0.975
					self["SvfitCacheFileFolder"] = "eleEsDown"
				else:
					self["ElectronEnergyCorrectionShiftEB"] = 1.0
					self["ElectronEnergyCorrectionShiftEE"] = 1.0
					self["SvfitCacheFileFolder"] = "nominal"

			#FIXME this is the total JEC if I am not mistaken
			elif systematic_uncertainty == "jecUncUp":
				if re.search("Run201|Embedding", nickname):
					self["JetEnergyCorrectionUncertaintyShift"] = 0.0
				else:
					self["JetEnergyCorrectionUncertaintyShift"] = 1.0

				self["JetEnergyCorrectionSplitUncertainty"] = False
				self["AbsJetEnergyCorrectionSplitUncertaintyShift"] = 0.0

				self["SvfitCacheFileFolder"] = "nominal"
			elif systematic_uncertainty == "jecUncDown":
				if re.search("Run201|Embedding", nickname):
					self["JetEnergyCorrectionUncertaintyShift"] = 0.0
				else:
					self["JetEnergyCorrectionUncertaintyShift"] = -1.0

				self["JetEnergyCorrectionSplitUncertainty"] = False
				self["AbsJetEnergyCorrectionSplitUncertaintyShift"] = 0.0

				self["SvfitCacheFileFolder"] = "nominal"

			elif systematic_uncertainty == "metJetEnUp":
				if re.search("Spring16|Summer16", nickname):
					self["MetUncertaintyShift"] = True
					self["MetUncertaintyType"] = "JetEnUp"
					self["SvfitCacheFileFolder"] = "metJetEnUp"
				elif re.search("Fall17", nickname):
					self["MetUncertaintyShift"] = True
					self["MetUncertaintyType"] = "JetEnUp"
					self["SvfitCacheFileFolder"] = "metJetEnUp"
				else:
					self["MetUncertaintyShift"] = False
					self["MetUncertaintyType"] = ""
					self["SvfitCacheFileFolder"] = "nominal"

			elif systematic_uncertainty == "metJetEnDown":
				if re.search("Spring16|Summer16", nickname):
					self["MetUncertaintyShift"] = True
					self["MetUncertaintyType"] = "JetEnDown"
					self["SvfitCacheFileFolder"] = "metJetEnDown"
				elif re.search("Fall17", nickname):
					self["MetUncertaintyShift"] = True
					self["MetUncertaintyType"] = "JetEnDown"
					self["SvfitCacheFileFolder"] = None #"metJetEnDown"
				else:
					self["MetUncertaintyShift"] = False
					self["MetUncertaintyType"] = ""
					self["SvfitCacheFileFolder"] = "nominal"

			elif systematic_uncertainty == "metUnclusteredEnUp":
				if re.search("Spring16|Summer16", nickname):
					self["MetUncertaintyShift"] = True
					self["MetUncertaintyType"] = "UnclusteredEnUp"
					self["SvfitCacheFileFolder"] = "metUnclusteredEnUp"
				elif re.search("Fall17", nickname):
					self["MetUncertaintyShift"] = True
					self["MetUncertaintyType"] = "UnclusteredEnUp"
					self["SvfitCacheFileFolder"] = None #"metUnclusteredEnUp"
				else:
					self["MetUncertaintyShift"] = False
					self["MetUncertaintyType"] = ""
					self["SvfitCacheFileFolder"] = "nominal"

			elif systematic_uncertainty == "metUnclusteredEnDown":
				if re.search("Spring16|Summer16", nickname):
					self["MetUncertaintyShift"] = True
					self["MetUncertaintyType"] = "UnclusteredEnDown"
					self["SvfitCacheFileFolder"] = "metUnclusteredEnDown"
				elif re.search("Fall17",nickname):
					self["MetUncertaintyShift"] = True
					self["MetUncertaintyType"] = "UnclusteredEnDown"
					self["SvfitCacheFileFolder"] = None#"metUnclusteredEnDown"
				else:
					self["MetUncertaintyShift"] = False
					self["MetUncertaintyType"] = ""
					self["SvfitCacheFileFolder"] = "nominal"

			elif systematic_uncertainty == "tauEleFakeEsUp":
				if re.search("(DY.?JetsToLL|EWKZ2Jets).*(?=(Spring16|Summer16))", nickname):
					self["TauElectronFakeEnergyCorrection"] = 1.03
					self["SvfitCacheFileFolder"] = "tauEleFakeEsUp"
				else:
					self["TauElectronFakeEnergyCorrection"] = 1.0
					self["SvfitCacheFileFolder"] = "nominal"

			elif systematic_uncertainty == "tauEleFakeEsDown":
				if re.search("(DY.?JetsToLL|EWKZ2Jets).*(?=(Spring16|Summer16))", nickname):
					self["TauElectronFakeEnergyCorrection"] = 0.097
					self["SvfitCacheFileFolder"] = "tauEleFakeEsDown"
				else:
					self["TauElectronFakeEnergyCorrection"] = 1.0
					self["SvfitCacheFileFolder"] = "nominal"

			elif systematic_uncertainty == "tauMuFakeEsUp": #FIXME also taucorrectionsproducer
				if re.search("(DY.?JetsToLL|EWKZ2Jets).*(?=(Spring16|Summer16))", nickname):
					self["TauMuonFakeEnergyCorrection"] = 1.015
					self["SvfitCacheFileFolder"] = "tauMuFakeEsUp"
				else:
					self["TauMuonFakeEnergyCorrection"] = 1.0
					self["SvfitCacheFileFolder"] = "nominal"

			elif systematic_uncertainty == "tauMuFakeEsDown": #FIXME also taucorrectionsproducer
				if re.search("(DY.?JetsToLL|EWKZ2Jets).*(?=(Spring16|Summer16))", nickname):
					self["TauMuonFakeEnergyCorrection"] = 0.985
					self["SvfitCacheFileFolder"] = "tauMuFakeEsDown"
				else:
					self["TauMuonFakeEnergyCorrection"] = 1.0
					self["SvfitCacheFileFolder"] = "nominal"

			elif systematic_uncertainty == "tauMuFakeEsOneProngUp":
				if re.search("(DY.?JetsToLL|EWKZ2Jets|LFV).*(?=(Spring16|Summer16))", nickname):
					self["TauMuonFakeEnergyCorrectionOneProngShift"] = 0.015
					self["SvfitCacheFileFolder"] = "tauMuFakeEsOneProngUp"
				elif re.search("(DY.?JetsToLL|EWKZ2Jets).*(?=(Fall17))", nickname):
					self["TauMuonFakeEnergyCorrectionOneProngShift"] = 0.003
					#self["SvfitCacheFileFolder"] = "tauMuFakeEsOneProngUp"
				else:
					self["TauMuonFakeEnergyCorrectionOneProngShift"] = 0.0
					self["SvfitCacheFileFolder"] = "nominal"

			elif systematic_uncertainty == "tauMuFakeEsOneProngDown":
				if re.search("(DY.?JetsToLL|EWKZ2Jets|LFV).*(?=(Spring16|Summer16))", nickname):
					self["TauMuonFakeEnergyCorrectionOneProngShift"] = -0.015
					self["SvfitCacheFileFolder"] = "tauMuFakeEsOneProngDown"
				elif re.search("(DY.?JetsToLL|EWKZ2Jets).*(?=(Fall17))", nickname):
					self["TauMuonFakeEnergyCorrectionOneProngShift"] = -0.003
					#self["SvfitCacheFileFolder"] = "tauMuFakeEsOneProngDown"
				else:
					self["TauMuonFakeEnergyCorrectionOneProngShift"] = 0.0
					self["SvfitCacheFileFolder"] = "nominal"

			elif systematic_uncertainty == "tauMuFakeEsOneProngPiZerosUp":
				if re.search("(DY.?JetsToLL|EWKZ2Jets|LFV).*(?=(Spring16|Summer16))", nickname):
					self["TauMuonFakeEnergyCorrectionOneProngPiZerosShift"] = 0.015
					self["SvfitCacheFileFolder"] =  "tauMuFakeEsOneProngPiZerosUp"
				elif re.search("(DY.?JetsToLL|EWKZ2Jets).*(?=(Fall17))", nickname):
					self["TauMuonFakeEnergyCorrectionOneProngPiZerosShift"] = 0.01
					#self["SvfitCacheFileFolder"] = "tauMuFakeEsOneProngPiZerosUp"
			elif systematic_uncertainty == "tauMuFakeEsOneProngPiZerosDown":
				if re.search("(DY.?JetsToLL|EWKZ2Jets|LFV).*(?=(Spring16|Summer16))", nickname):
					self["TauMuonFakeEnergyCorrectionOneProngPiZerosShift"] = -0.015
					self["SvfitCacheFileFolder"] =  "tauMuFakeEsOneProngPiZerosDown"
				elif re.search("(DY.?JetsToLL|EWKZ2Jets).*(?=(Fall17))", nickname):
					self["TauMuonFakeEnergyCorrectionOneProngPiZerosShift"] = -0.01
					#self["SvfitCacheFileFolder"] = "tauMuFakeEsOneProngPiZerosDown"


			elif systematic_uncertainty == "tauEleFakeEsOneProngUp":
				if re.search("(DY.?JetsToLL|EWKZ2Jets|LFV).*(?=(Spring16|Summer16))", nickname):
					self["TauElectronFakeEnergyCorrectionOneProngShift"] = 0.03
					self["SvfitCacheFileFolder"] = "tauEleFakeEsOneProngUp"
				elif re.search("(DY.?JetsToLL|EWKZ2Jets).*(?=(Fall17))", nickname):
					self["TauElectronFakeEnergyCorrectionOneProngShift"] = 0.014
					self["SvfitCacheFileFolder"] = "tauEleFakeEsOneProngUp"
				else:
					self["TauElectronFakeEnergyCorrectionOneProngShift"] = 0.0
					self["SvfitCacheFileFolder"] = "nominal"

			elif systematic_uncertainty == "tauEleFakeEsOneProngDown":
				if re.search("(DY.?JetsToLL|EWKZ2Jets|LFV).*(?=(Spring16|Summer16))", nickname):
					self["TauElectronFakeEnergyCorrectionOneProngShift"] = -0.03
					self["SvfitCacheFileFolder"] = "tauEleFakeEsOneProngDown"
				elif re.search("(DY.?JetsToLL|EWKZ2Jets).*(?=(Fall17))", nickname):
					self["TauElectronFakeEnergyCorrectionOneProngShift"] = -0.014
					self["SvfitCacheFileFolder"] = "tauEleFakeEsOneProngDown"
				else:
					self["TauElectronFakeEnergyCorrectionOneProngShift"] = 0.0
					self["SvfitCacheFileFolder"] = "nominal"

			elif systematic_uncertainty == "tauEleFakeEsOneProngPiZerosUp":
				if re.search("(DY.?JetsToLL|EWKZ2Jets|LFV).*(?=(Spring16|Summer16))", nickname):
					self["TauElectronFakeEnergyCorrectionOneProngPiZerosShift"] = 0.03
					self["SvfitCacheFileFolder"] = "tauEleFakeEsOneProngPiZerosUp"
				elif re.search("(DY.?JetsToLL|EWKZ2Jets).*(?=(Fall17))", nickname):
					self["TauElectronFakeEnergyCorrectionOneProngPiZerosShift"] = 0.018
					self["SvfitCacheFileFolder"] = "tauEleFakeEsOneProngPiZerosUp"
				else:
					self["TauElectronFakeEnergyCorrectionOneProngPiZerosShift"] = 0.0
					self["SvfitCacheFileFolder"] = "nominal"
			elif systematic_uncertainty == "tauEleFakeEsOneProngPiZerosDown":
				if re.search("(DY.?JetsToLL|EWKZ2Jets|LFV).*(?=(Spring16|Summer16))", nickname):
					self["TauElectronFakeEnergyCorrectionOneProngPiZerosShift"] = -0.03
					self["SvfitCacheFileFolder"] = "tauEleFakeEsOneProngPiZerosDown"
				elif re.search("(DY.?JetsToLL|EWKZ2Jets).*(?=(Fall17))", nickname):
					self["TauElectronFakeEnergyCorrectionOneProngPiZerosShift"] = -0.018
					self["SvfitCacheFileFolder"] = "tauEleFakeEsOneProngPiZerosDown"
				else:
					self["TauElectronFakeEnergyCorrectionOneProngPiZerosShift"] = 0.0
					self["SvfitCacheFileFolder"] = "nominal"

			#caution tauEs splitted for several nicknames/files
			elif systematic_uncertainty == "tauEsUp": #FIXME als htttaucorrectionsproducer
				if re.search("(HToTauTau|H2JetsToTauTau|Higgs|DY.?JetsToLL|EWKZ2Jets).*(?=Fall15)", nickname):
					self["TauEnergyCorrectionShift"] = 1.03
				elif re.search("Embedding2016", nickname):
					self["TauEnergyCorrectionShift"] = 1.03
				elif re.search("Spring16|Summer16", nickname):
					self["TauEnergyCorrectionShift"] = 1.012
				else:
					self["TauEnergyCorrectionShift"] = 1.0

				if re.search("HToTauTau|H2JetsToTauTau|Higgs|DY.?JetsToLL|EWKZ2Jets|Spring16|Summer16|Embedding(2016|2017)", nickname):
					self["SvfitCacheFileFolder"] = "tauEsUp"
				else:
					self["SvfitCacheFileFolder"] = "nominal"
			elif systematic_uncertainty == "tauEsDown": #FIXME also taucorrectionsproducer
				if re.search("(HToTauTau|H2JetsToTauTau|Higgs|DY.?JetsToLL|EWKZ2Jets).*(?=Fall15)", nickname):
					self["TauEnergyCorrectionShift"] = 0.97
				elif re.search("Embedding2016", nickname):
					self["TauEnergyCorrectionShift"] = 0.97
				elif re.search("Spring16|Summer16", nickname):
					self["TauEnergyCorrectionShift"] = 0.988
				else:
					self["TauEnergyCorrectionShift"] = 1.0

				if re.search("HToTauTau|H2JetsToTauTau|Higgs|DY.?JetsToLL|EWKZ2Jets|Spring16|Summer16|Embedding(2016|2017)", nickname):
					self["SvfitCacheFileFolder"] = "tauEsDown"

				else:
					self["SvfitCacheFileFolder"] = "nominal"

			elif systematic_uncertainty == "tauEsOneProngUp":
				if legacy:
					self["IsShiftUp"] = True
					self["SvfitCacheFileFolder"] = "tauEsOneProngUp"
				else:
					if re.search("(HToTauTau|H2JetsToTauTau|Higgs|DY.?JetsToLL|EWKZ2Jets).*(?=Fall15)", nickname):
						self["TauEnergyCorrectionOneProngShift"] = 0.03
					elif re.search("Embedding2016", nickname):
						self["TauEnergyCorrectionOneProngShift"] = 0.012
					elif re.search("Spring16|Summer16", nickname):
						self["TauEnergyCorrectionOneProngShift"] = 0.012
					elif re.search("Fall17", nickname):
						self["TauEnergyCorrectionOneProngShift"] = 0.008
					elif re.search("Embedding2017", nickname):
						self["TauEnergyCorrectionOneProngShift"] = 0.015
					else:
						self["TauEnergyCorrectionOneProngShift"] = 0.0

					if re.search("HToTauTau|H2JetsToTauTau|Higgs|DY.?JetsToLL|EWKZ2Jets|Spring16|Summer16|Embedding(2016|2017)", nickname):
						self["SvfitCacheFileFolder"] = "tauEsOneProngUp"
					else:
						self["SvfitCacheFileFolder"] = "nominal"

			elif systematic_uncertainty == "tauEsOneProngDown":
				if legacy:
					self["IsShiftUp"] = False
					self["SvfitCacheFileFolder"] = "tauEsOneProngDown"
				else:
					if re.search("(HToTauTau|H2JetsToTauTau|Higgs|DY.?JetsToLL|EWKZ2Jets).*(?=Fall15)", nickname):
						self["TauEnergyCorrectionOneProngShift"] = -0.03
					elif re.search("Embedding2016", nickname):
						self["TauEnergyCorrectionOneProngShift"] = -0.012
					elif re.search("Spring16|Summer16", nickname):
						self["TauEnergyCorrectionOneProngShift"] = -0.012
					elif re.search("Fall17", nickname):
						self["TauEnergyCorrectionOneProngShift"] = -0.008
					elif re.search("Embedding2017", nickname):
						self["TauEnergyCorrectionOneProngShift"] = -0.015
					else:
						self["TauEnergyCorrectionOneProngShift"] = 0.0

					if re.search("HToTauTau|H2JetsToTauTau|Higgs|DY.?JetsToLL|EWKZ2Jets|Spring16|Summer16|Embedding(2016|2017)", nickname):
						self["SvfitCacheFileFolder"] = "tauEsOneProngDown"
					else:
						self["SvfitCacheFileFolder"] = "nominal"

			elif systematic_uncertainty == "tauEsOneProngPiZerosUp":
				if legacy:
					self["IsShiftUp"] = True
					self["SvfitCacheFileFolder"] = "tauEsOneProngUp"
				else:
					if re.search("(HToTauTau|H2JetsToTauTau|Higgs|DY.?JetsToLL|EWKZ2Jets).*(?=Fall15)", nickname):
						self["TauEnergyCorrectionOneProngPiZerosShift"] = 0.03
					elif re.search("Embedding2016", nickname):
						self["TauEnergyCorrectionOneProngPiZerosShift"] = 0.03
					elif re.search("Spring16|Summer16", nickname):
						self["TauEnergyCorrectionOneProngPiZerosShift"] = 0.012
					elif re.search("Fall17", nickname):
						self["TauEnergyCorrectionOneProngPiZerosShift"] = 0.008
					elif re.search("Embedding2017", nickname):
						self["TauEnergyCorrectionOneProngPiZerosShift"] = 0.015
					else:
						self["TauEnergyCorrectionOneProngPiZerosShift"] = 0.0

					if re.search("HToTauTau|H2JetsToTauTau|Higgs|DY.?JetsToLL|EWKZ2Jets|Spring16|Summer16|Embedding(2016|2017)", nickname):
						self["SvfitCacheFileFolder"] = "tauEsOneProngPiZerosUp"
					else:
						self["SvfitCacheFileFolder"] = "nominal"

			elif systematic_uncertainty == "tauEsOneProngPiZerosDown":
				if legacy:
					self["IsShiftUp"] = False
					self["SvfitCacheFileFolder"] = "tauEsOneProngDown"
				else:
					if re.search("(HToTauTau|H2JetsToTauTau|Higgs|DY.?JetsToLL|EWKZ2Jets).*(?=Fall15)", nickname):
						self["TauEnergyCorrectionOneProngPiZerosShift"] = -0.03
					elif re.search("Embedding2016", nickname):
						self["TauEnergyCorrectionOneProngPiZerosShift"] = -0.012
					elif re.search("Spring16|Summer16", nickname):
						self["TauEnergyCorrectionOneProngPiZerosShift"] = -0.012
					elif re.search("Fall17", nickname):
						self["TauEnergyCorrectionOneProngPiZerosShift"] = -0.008
					elif re.search("Embedding2017", nickname):
						self["TauEnergyCorrectionOneProngPiZerosShift"] = -0.015
					else:
						self["TauEnergyCorrectionOneProngPiZerosShift"] = 0.0


					if re.search("HToTauTau|H2JetsToTauTau|Higgs|DY.?JetsToLL|EWKZ2Jets|Spring16|Summer16|Embedding(2016|2017)", nickname):
						self["SvfitCacheFileFolder"] = "tauEsOneProngPiZerosDown"
					else:
						self["SvfitCacheFileFolder"] = "nominal"

			elif systematic_uncertainty == "tauEsThreeProngUp":
				if legacy:
					self["IsShiftUp"] = True
					self["SvfitCacheFileFolder"] = "tauEsOneProngUp"
				else:
					if re.search("(HToTauTau|H2JetsToTauTau|Higgs|DY.?JetsToLL|EWKZ2Jets).*(?=Fall15)", nickname):
						self["TauEnergyCorrectionThreeProngShift"] = 0.03
					elif re.search("Embedding2016", nickname):
						self["TauEnergyCorrectionThreeProngShift"] = 0.012
					elif re.search("Spring16|Summer16", nickname):
						self["TauEnergyCorrectionThreeProngShift"] = 0.012
					elif re.search("Fall17", nickname):
						self["TauEnergyCorrectionThreeProngShift"] = 0.009
					elif re.search("Embedding2017", nickname):
						self["TauEnergyCorrectionThreeProngShift"] = 0.015
					else:
						self["TauEnergyCorrectionThreeProngShift"] = 0.0


					if re.search("HToTauTau|H2JetsToTauTau|Higgs|DY.?JetsToLL|EWKZ2Jets|Spring16|Summer16|Embedding(2016|2017)", nickname):
						self["SvfitCacheFileFolder"] = "tauEsThreeProngUp"
					else:
						self["SvfitCacheFileFolder"] = "nominal"

			elif systematic_uncertainty == "tauEsThreeProngDown":
				if legacy:
					self["IsShiftUp"] = False
					self["SvfitCacheFileFolder"] = "tauEsOneProngDown"
				else:
					if re.search("(HToTauTau|H2JetsToTauTau|Higgs|DY.?JetsToLL|EWKZ2Jets).*(?=Fall15)", nickname):
						self["TauEnergyCorrectionThreeProngShift"] = -0.03
					elif re.search("Embedding2016", nickname):
						self["TauEnergyCorrectionThreeProngShift"] = -0.012
					elif re.search("Spring16|Summer16", nickname):
						self["TauEnergyCorrectionThreeProngShift"] = -0.012
					elif re.search("Fall17", nickname):
						self["TauEnergyCorrectionThreeProngShift"] = -0.009
					elif re.search("Embedding2017", nickname):
						self["TauEnergyCorrectionThreeProngShift"] = -0.015
					else:
						self["TauEnergyCorrectionThreeProngShift"] = 0.0

					if re.search("HToTauTau|H2JetsToTauTau|Higgs|DY.?JetsToLL|EWKZ2Jets|Spring16|Summer16|Embedding(2016|2017)", nickname):
						self["SvfitCacheFileFolder"] = "tauEsThreeProngDown"
					else:
						self["SvfitCacheFileFolder"] = "nominal"

			elif systematic_uncertainty == "tauEsThreeProngPiZerosUp":
				if legacy:
					self["IsShiftUp"] = True
					self["SvfitCacheFileFolder"] = "tauEsOneProngUp"
				else:
					if re.search("Fall17", nickname):
						self["TauEnergyCorrectionThreeProngPiZerosShift"] = 0.01
					elif re.search("Embedding2017", nickname):
						self["TauEnergyCorrectionThreeProngShift"] = 0.015
					else:
						self["TauEnergyCorrectionThreeProngPiZerosShift"] = 0.0

			elif systematic_uncertainty == "tauEsThreeProngPiZerosDown":
				if legacy:
					self["IsShiftUp"] = False
					self["SvfitCacheFileFolder"] = "tauEsOneProngDown"
				else:
					if re.search("Fall17", nickname):
						self["TauEnergyCorrectionThreeProngPiZerosShift"] = -0.01
					elif re.search("Embedding2017", nickname):
						self["TauEnergyCorrectionThreeProngShift"] = -0.015
					else:
						self["TauEnergyCorrectionThreeProngPiZerosShift"] = 0.0

			elif systematic_uncertainty == "tauJetFakeEsUp":
				if re.search("Spring16|Summer16", nickname):
					self["TauJetFakeEnergyCorrection"] = 1.0
					self["SvfitCacheFileFolder"] = "tauJetFakeEsUp"
				else:
					self["TauJetFakeEnergyCorrection"] = 0.0
					self["SvfitCacheFileFolder"] = "nominal"
			elif systematic_uncertainty == "tauJetFakeEsDown":
				if re.search("Spring16|Summer16", nickname):
					self["TauJetFakeEnergyCorrection"] = -1.0
					self["SvfitCacheFileFolder"] = "tauJetFakeEsDown"
				else:
					self["TauJetFakeEnergyCorrection"] = 0.0
					self["SvfitCacheFileFolder"] = "nominal"
			elif systematic_uncertainty == "muonEsUp":
					self["MuonEnergyCorrectionShiftEta0p4to1p2"] = 0.004
					self["MuonEnergyCorrectionShiftEta1p2to2p1"] = 0.009
					self["MuonEnergyCorrectionShiftEtaGt2p1"] = 0.017
			elif systematic_uncertainty == "muonEsDown":
					self["MuonEnergyCorrectionShiftEta0p4to1p2"] = -0.004
					self["MuonEnergyCorrectionShiftEta1p2to2p1"] = -0.009
					self["MuonEnergyCorrectionShiftEtaGt2p1"] = -0.017
			elif re.search("CMS_scale_t_.*_13TeV.*", systematic_uncertainty) != None:
				if "Down" in systematic_uncertainty:
					self["IsShiftUp"] = False
				elif "Up" in systematic_uncertainty:
					self["IsShiftUp"] = True
			else:
				log.critical("COULD NOT FIND THE SYSTEMATIC %s" %systematic_uncertainty)
				sys.exit(1)

	def clear_config(self, nickname):
		self["ElectronEnergyCorrectionShiftEB"] = 1.0
		self["ElectronEnergyCorrectionShiftEE"] = 1.0
		self["JetEnergyCorrectionUncertaintyShift"] = 0.0
		self["MetUncertaintyShift"] = False
		self["MetUncertaintyType"] = ""
		self["SvfitCacheFileFolder"] = "nominal"
		self["TauElectronFakeEnergyCorrection"] = 1.0

		self["TauElectronFakeEnergyCorrectionOneProngPiZerosShift"] = 0.0
		self["TauElectronFakeEnergyCorrectionOneProngShift"] = 0.0

		self["TauEnergyCorrectionOneProngPiZerosShift"] = 0.0
		self["TauEnergyCorrectionOneProngShift"] = 0.0
		self["TauEnergyCorrectionShift"] = 0.0
		self["TauEnergyCorrectionThreeProngShift"] = 0.0
		self["TauEnergyCorrectionThreeProngPiZerosShift"] = 0.0

		self["TauJetFakeEnergyCorrection"] = 0.0

		self["TauMuonFakeEnergyCorrection"] = 0.0

		self["TauMuonFakeEnergyCorrectionOneProngPiZerosShift"] = 0.0
		self["TauMuonFakeEnergyCorrectionOneProngShift"] = 0.0

		self.JECUncertaintySplit_config = sJECUS.JECUncertaintySplit(nickname)
		self.update(self.JECUncertaintySplit_config)
		self["DoJecGroupings"] = False

		#CP FINAL STATE UNCERTAINTIES
		self["MuonEnergyCorrectionShiftEta0p4to1p2"] = 1.0
		self["MuonEnergyCorrectionShiftEta1p2to2p1"] = 1.0
		self["MuonEnergyCorrectionShiftEtaGt2p1"] = 1.0
