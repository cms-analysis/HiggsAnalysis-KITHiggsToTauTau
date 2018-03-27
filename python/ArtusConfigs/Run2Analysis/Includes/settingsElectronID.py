# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import re
import json
import Artus.Utility.jsonTools as jsonTools
import Kappa.Skimming.datasetsHelperTwopz as datasetsHelperTwopz
import copy

class Electron_ID(dict):
	def __init__(self, nickname):
		#doppelgemoppel allready in the config class
		self.datasetsHelper = datasetsHelperTwopz.datasetsHelperTwopz("Kappa/Skimming/data/datasets.json") 

		self["ElectronID_documentation"] = ["https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsToTauTauWorking2015#Electrons"]
	
		self["ElectronReco"] = "mvanontrig"
	
		self["ElectronID"] = "user"
		self["ElectronIDType"] = "mvabased2015andlater"

		if re.search("(Run2015|Fall15MiniAODv2)", nickname):
			self["ElectronIDName"] = "electronMVAValueMapProducer:ElectronMVAEstimatorRun2Spring15NonTrig25nsV1Values"
			self["ElectronMvaIDCutEB1"] = 0.967083
			self["ElectronMvaIDCutEB2"] = 0.929117
			self["ElectronMvaIDCutEE"] = 0.726311
			self["ElectronIDList"] = ["electronMVAValueMapProducer:ElectronMVAEstimatorRun2Spring15NonTrig25nsV1Values",
						"egmGsfElectronIDs:cutBasedElectronID-Spring15-25ns-V1-standalone-veto",
						"egmGsfElectronIDs:cutBasedElectronID-Spring15-25ns-V1-standalone-loose",
						"egmGsfElectronIDs:cutBasedElectronID-Spring15-25ns-V1-standalone-medium",
						"egmGsfElectronIDs:cutBasedElectronID-Spring15-25ns-V1-standalone-tight"]
		else:
			self["ElectronIDName"] = "electronMVAValueMapProducer:ElectronMVAEstimatorRun2Spring16GeneralPurposeV1Values"
			self["ElectronMvaIDCutEB1"] = 0.941
			self["ElectronMvaIDCutEB2"] = 0.899
			self["ElectronMvaIDCutEE"] = 0.758
			self["ElectronIDList"] = ["electronMVAValueMapProducer:ElectronMVAEstimatorRun2Spring16GeneralPurposeV1Values",
						"egmGsfElectronIDs:cutBasedElectronID-Summer16-80X-V1-veto",
						"egmGsfElectronIDs:cutBasedElectronID-Summer16-80X-V1-loose",
						"egmGsfElectronIDs:cutBasedElectronID-Summer16-80X-V1-medium",
						"egmGsfElectronIDs:cutBasedElectronID-Summer16-80X-V1-tight"]		

	
		self["ElectronIsoType"] = "user"
		self["ElectronIso"] = "none"
	
		self["ElectronIsoSignalConeSize"] = 0.3
		self["ElectronDeltaBetaCorrectionFactor"] = 0.5
	
		self["ElectronTrackDxyCut"] = 0.045
		self["ElectronTrackDzCut"] = 0.2

	#since looseElectron_ID includes Electron_ID settings, when this is not ok then just write everything in init to seperate function electron_ID
	def looseElectron_ID(self, nickname):
		self["LooseElectronReco"] = "mvanontrig"

		self["LooseElectronID"] = "user"
		self["LooseElectronIDType"] = "mvabased2015andlater"
	
		if re.search("(Run2015|Fall15MiniAODv2)", nickname):
			self["LooseElectronIDName"] = "electronMVAValueMapProducer:ElectronMVAEstimatorRun2Spring15NonTrig25nsV1Values"
			self["LooseElectronMvaIDCutEB1"] = 0.913286
			self["LooseElectronMvaIDCutEB2"] = 0.805013
			self["LooseElectronMvaIDCutEE"] = 0.358969
		else:
			self["LooseElectronIDName"] = "electronMVAValueMapProducer:ElectronMVAEstimatorRun2Spring16GeneralPurposeV1Values"
			self["LooseElectronMvaIDCutEB1"] = 0.837
			self["LooseElectronMvaIDCutEB2"] = 0.715
			self["LooseElectronMvaIDCutEE"] = 0.357
			

		self["LooseElectronIsoType"] = "user"
		self["LooseElectronIso"] = "none"

		self["LooseElectronIsoPtSumOverPtUpperThresholdEB"] = 0.3
		self["LooseElectronIsoPtSumOverPtUpperThresholdEE"] = 0.3

		self["LooseElectronLowerPtCuts"] = ["10.0"]
		self["LooseElectronUpperAbsEtaCuts"] = ["2.5"]
		self["LooseElectronTrackDxyCut"] = 0.045
		self["LooseElectronTrackDzCut"] = 0.2
		self["DirectIso"] = True

	def vetoElectronID(self, nickname):
		self["VetoElectronReco"] = "none"

		self["VetoElectronID"] = "user"

		if re.search("(Run2015|Fall15MiniAODv2)*?", nickname):
			self["VetoElectronIDType"] = "cutbased2015noisoandipcutsveto"
			self["VetoElectronIDName"] = "egmGsfElectronIDs:cutBasedElectronID-Spring15-25ns-V1-standalone-veto"
		else:
			self["VetoElectronIDType"] = "cutbased2016noisocutsveto"
			self["VetoElectronIDName"] =  "egmGsfElectronIDs:cutBasedElectronID-Summer16-80X-V1-veto"
			
		
		self["VetoElectronIsoType"] = "user"
		self["VetoElectronIso"] = "none"
		self["VetoElectronIsoPtSumOverPtUpperThresholdEB"] = 0.3
		self["VetoElectronIsoPtSumOverPtUpperThresholdEE"] = 0.3

		self["VetoElectronLowerPtCuts"] = ["15.0"]
		self["VetoElectronUpperAbsEtaCuts"] = ["2.5"]
		self["DiVetoElectronMinDeltaRCut"] = 0.15
		self["DiVetoElectronVetoMode"] = "veto_os_keep_ss"
		self["DirectIso"] = True























