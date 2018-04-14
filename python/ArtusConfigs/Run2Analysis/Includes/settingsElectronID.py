# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import re


class Electron_ID(dict):
	def __init__(self, nickname):
		
		self["ElectronID_documentation"] = ["https://twiki.cern.ch/twiki/bin/view/CMS/MultivariateElectronIdentificationRun2",
						"https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsToTauTauWorking2015#Electrons"]
	
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
		elif re.search("(Run2017|Fall17)", nickname):
			self["ElectronIDName"] = "electronMVAValueMapProducer:ElectronMVAEstimatorRun2Fall17IsoV1Values"
			self["ElectronMvaIDCutEB1"] = 0.9897
			self["ElectronMvaIDCutEB2"] = 0.9819
			self["ElectronMvaIDCutEE"] = 0.9625
			self["ElectronIDList"] = [
				"electronMVAValueMapProducer:ElectronMVAEstimatorRun2Fall17IsoV1Values",
				"egmGsfElectronIDs:mvaEleID-Fall17-iso-V1-wp90",
				"egmGsfElectronIDs:mvaEleID-Fall17-iso-V1-wp80",
				"egmGsfElectronIDs:mvaEleID-Fall17-iso-V1-wpLoose"
			]

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
		elif re.search("(Run2017|Fall17)", nickname):
			self["LooseElectronIDName"] = "electronMVAValueMapProducer:ElectronMVAEstimatorRun2Fall17IsoV1Values"
			self["LooseElectronMvaIDCutEB1"] =  0.9718
			self["LooseElectronMvaIDCutEB2"] =  0.9459
			self["LooseElectronMvaIDCutEE"] =  0.8979
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

	def vetoElectron_ID(self, nickname):
		self["VetoElectronReco"] = "none"

		self["VetoElectronID"] = "user"

		if re.search("(Run2015|Fall15MiniAODv2)", nickname):
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

