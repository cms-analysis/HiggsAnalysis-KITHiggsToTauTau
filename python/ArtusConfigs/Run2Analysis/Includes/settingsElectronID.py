# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import re


class Electron_ID(dict):
	def __init__(self, nickname, wp=90, iso=False):  #might change to wp=90 iso False
		
		self["ElectronID_documentation"] = [
			"https://twiki.cern.ch/twiki/bin/view/CMS/MultivariateElectronIdentificationRun2",
			"https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsToTauTauWorking2015#Electrons"
		]
	
		self["ElectronReco"] = "mvanontrig"
	
		self["ElectronID"] = "user"
		self["ElectronIDType"] = "mvabased2015andlater"
		self["ElectronEtaBinnedEAValues"] = [] #if empty than not rho corrected
		self["ElectronEtaBinsForEA"] = []      #if empty than not rho corrected
		if re.search("(Run2015|Fall15MiniAODv2)", nickname):
			self["ElectronIDName"] = "electronMVAValueMapProducer:ElectronMVAEstimatorRun2Spring15NonTrig25nsV1Values"
			self["ElectronMvaIDCutEB1"] = 0.967083
			self["ElectronMvaIDCutEB2"] = 0.929117
			self["ElectronMvaIDCutEE"] = 0.726311
			self["ElectronIDList"] = [
				"electronMVAValueMapProducer:ElectronMVAEstimatorRun2Spring15NonTrig25nsV1Values",
				"egmGsfElectronIDs:cutBasedElectronID-Spring15-25ns-V1-standalone-veto",
				"egmGsfElectronIDs:cutBasedElectronID-Spring15-25ns-V1-standalone-loose",
				"egmGsfElectronIDs:cutBasedElectronID-Spring15-25ns-V1-standalone-medium",
				"egmGsfElectronIDs:cutBasedElectronID-Spring15-25ns-V1-standalone-tight"
			]
			#self["ElectronIDType"] = "mvabased2017andlater"

		elif re.search("(Run2017|Fall17)", nickname):
			self["ElectronIDName"] = "electronMVAValueMapProducer:ElectronMVAEstimatorRun2Fall17NoIsoV1Values" #TODO check if this is the one used in analysis
			self["ElectronMvaIDCutEB1"] = 0.9897
			self["ElectronMvaIDCutEB2"] = 0.9819
			self["ElectronMvaIDCutEE"] = 0.9625
			self["ElectronIDType"] = "mvabased2017andlater"
			#rho corrections
			#https://github.com/cms-sw/cmssw/blob/master/RecoEgamma/ElectronIdentification/data/Fall17/effAreaElectrons_cone03_pfNeuHadronsAndPhotons_94X.txt
			self["ElectronEtaBinnedEAValues"] = [0.1440, 0.1562, 0.1032, 0.0859, 0.1116, 0.1321, 0.1654]
			self["ElectronEtaBinsForEA"] = [0.0, 1.0, 1.479, 2.0, 2.2, 2.3, 2.4, 5.0]

			assert (wp==80 or wp==90), "wp should be 80 or 90. look inside settingselectronID.py"
			#In 2017 the working points are determined by a function dependent on pt, WP(pT) = c − Aexp( − pt/t), and the number there corresponds to [c, A, t] in this function
			# https://rembserj.web.cern.ch/rembserj/notes/Electron_MVA_ID_2017_documentation/
			if iso:
				self["ElectronIDName"] = "electronMVAValueMapProducer:ElectronMVAEstimatorRun2Fall17IsoV1Values"
				if wp==80:
					self["ElectronMvaIDCutEB1ParamsLowPt"] = [0.9725509559754997, 0.2653858736397496, 2.976593261509491]
					self["ElectronMvaIDCutEB2ParamsLowPt"] = [0.9508038141601247, 0.2355820499260076, 2.6633500558725713]
					self["ElectronMvaIDCutEEParamsLowPt"] = [0.9365037167596238, 3.067015289215309, 1.5765442323949856]
					self["ElectronMvaIDCutEB1ParamsHighPt"] = [0.9896562087723659, 0.40204156417414094, 10.342490511998674] 
					self["ElectronMvaIDCutEB2ParamsHighPt"] = [0.9819232656533827, 0.772674931169389, 9.05548836482051]
					self["ElectronMvaIDCutEEParamsHighPt"] = [0.9625098201744635, 8.42589315557279, 2.2916152615134173]
				if wp==90:
					self["ElectronMvaIDCutEB1ParamsLowPt"] = [0.9387070396095831, 0.8222647164151365, 2.6525585228167636]
					self["ElectronMvaIDCutEB2ParamsLowPt"] = [0.8948802925677235, 0.4123381218697539, 2.7645670358783523]
					self["ElectronMvaIDCutEEParamsLowPt"] = [-1830.8583661119892, -1831.2083578116517,-36578.11055382301]
					self["ElectronMvaIDCutEB1ParamsHighPt"] = [0.9717674837607253, 1.9712414940437244, 8.912850985100356] 
					self["ElectronMvaIDCutEB2ParamsHighPt"] = [0.9458745023265976, 2.40849932040698, 8.83104420392795]
					self["ElectronMvaIDCutEEParamsHighPt"] = [0.8979112012086751, 4.171581694893849, 9.814082144168015]
			else:
				self["ElectronIDName"] = "electronMVAValueMapProducer:ElectronMVAEstimatorRun2Fall17NoIsoV1Values"
				if wp==80:
					
					self["ElectronMvaIDCutEB1ParamsLowPt"] = [ 0.9530240956555949, 0.4669644718545271, 2.7591425841003647 ]
					self["ElectronMvaIDCutEB2ParamsLowPt"] = [ 0.9336564763961019, 0.33512286599215946, 2.709276284272272 ]
					self["ElectronMvaIDCutEEParamsLowPt"] = [ 0.9313133688365339, 3.8889462619659265, 1.5821934800715558 ]
					self["ElectronMvaIDCutEB1ParamsHighPt"] = [ 0.9825268564943458, 1.1974861596609097, 8.702601455860762 ] 
					self["ElectronMvaIDCutEB2ParamsHighPt"] = [ 0.9727509457929913, 1.7111755094657688, 8.179525631018565 ]
					self["ElectronMvaIDCutEEParamsHighPt"] = [ 0.9562619539540145, 3.013927699126942, 8.109845366281608 ]
				elif wp==90:
					self["ElectronMvaIDCutEB1ParamsLowPt"] = [ 0.9165112826974601, 1.03549199648109 , 2.7381703555094217]
					self["ElectronMvaIDCutEB2ParamsLowPt"] = [0.8655738322220173, 0.7975615613282494, 2.4027944652597073]
					self["ElectronMvaIDCutEEParamsLowPt"] = [-3016.035055227131, -3016.3029387236506, -52140.61856333602]
					self["ElectronMvaIDCutEB1ParamsHighPt"] = [0.9616542816132922, 3.1390200321591206, 8.757943837889817] 
					self["ElectronMvaIDCutEB2ParamsHighPt"] = [0.9319258011430132, 3.5985063793347787, 8.846057432565809]
					self["ElectronMvaIDCutEEParamsHighPt"] = [0.8899260780999244, 4.352791250718547, 10.124234115859881]

			self["ElectronIDList"] = [
				"egmGsfElectronIDs:cutBasedElectronID-Fall17-94X-V1-veto",
				"egmGsfElectronIDs:cutBasedElectronID-Fall17-94X-V1-loose",
				"egmGsfElectronIDs:cutBasedElectronID-Fall17-94X-V1-medium",
				"egmGsfElectronIDs:cutBasedElectronID-Fall17-94X-V1-tight",
				"egmGsfElectronIDs:mvaEleID-Fall17-iso-V1-wp90",
				"egmGsfElectronIDs:mvaEleID-Fall17-iso-V1-wp80",
				"egmGsfElectronIDs:mvaEleID-Fall17-iso-V1-wpLoose",
				"electronMVAValueMapProducer:ElectronMVAEstimatorRun2Fall17IsoV1Values",
				"egmGsfElectronIDs:mvaEleID-Fall17-noIso-V1-wp90",
				"egmGsfElectronIDs:mvaEleID-Fall17-noIso-V1-wp80",
				"egmGsfElectronIDs:mvaEleID-Fall17-noIso-V1-wpLoose",
				"electronMVAValueMapProducer:ElectronMVAEstimatorRun2Fall17NoIsoV1Values"
			]
	
		else:
			self["ElectronIDName"] = "electronMVAValueMapProducer:ElectronMVAEstimatorRun2Spring16GeneralPurposeV1Values"
			#corresponds to wp80
			self["ElectronMvaIDCutEB1"] = 0.941
			self["ElectronMvaIDCutEB2"] = 0.899
			self["ElectronMvaIDCutEE"] = 0.758
			self["ElectronIDList"] = [
				"electronMVAValueMapProducer:ElectronMVAEstimatorRun2Spring16GeneralPurposeV1Values",
				"egmGsfElectronIDs:cutBasedElectronID-Summer16-80X-V1-veto",
				"egmGsfElectronIDs:cutBasedElectronID-Summer16-80X-V1-loose",
				"egmGsfElectronIDs:cutBasedElectronID-Summer16-80X-V1-medium",
				"egmGsfElectronIDs:cutBasedElectronID-Summer16-80X-V1-tight"
			]
			self["ElectronIDType"] = "mvabased2015andlater"

		self["ElectronIsoType"] = "user"
		self["ElectronIso"] = "none"
	
		self["ElectronIsoSignalConeSize"] = 0.3
		self["ElectronDeltaBetaCorrectionFactor"] = 0.5
	
		self["ElectronTrackDxyCut"] = 0.045
		self["ElectronTrackDzCut"] = 0.2

	#since looseElectron_ID includes Electron_ID settings, when this is not ok then just write everything in init to seperate function electron_ID
	def looseElectron_ID(self, nickname, iso=False):
		#"Loose" tagged electrons by artus are used for third lepton vetos
		self["LooseElectronReco"] = "mvanontrig"

		self["LooseElectronID"] = "user"

	
		if re.search("(Run2015|Fall15MiniAODv2)", nickname):
			self["LooseElectronIDName"] = "electronMVAValueMapProducer:ElectronMVAEstimatorRun2Spring15NonTrig25nsV1Values"
			self["LooseElectronMvaIDCutEB1"] = 0.913286
			self["LooseElectronMvaIDCutEB2"] = 0.805013
			self["LooseElectronMvaIDCutEE"] = 0.358969
			self["LooseElectronIDType"] = "mvabased2015andlater"

		elif re.search("(Run2017|Fall17)", nickname):
			self["LooseElectronIDName"] = "electronMVAValueMapProducer:ElectronMVAEstimatorRun2Fall17NoIsoV1Values"
			self["LooseElectronMvaIDCutEB1"] =  0.9718
			self["LooseElectronMvaIDCutEB2"] =  0.9459
			self["LooseElectronMvaIDCutEE"] =  0.8979
			self["LooseElectronIDType"] = "mvabased2017andlater"

			# https://github.com/guitargeek/cmssw/blob/ElectronID_MVA2017_940pre3/RecoEgamma/ElectronIdentification/python/Identification/mvaElectronID_Fall17_noIso_V1_cff.py#L60-L81
			#always use the wp90
			if iso:
				self["LooseElectronIDName"] = "electronMVAValueMapProducer:ElectronMVAEstimatorRun2Fall17IsoV1Values"

				self["LooseElectronMvaIDCutEB1ParamsLowPt"] = [0.9387070396095831, 0.8222647164151365, 2.6525585228167636]
				self["LooseElectronMvaIDCutEB2ParamsLowPt"] = [0.8948802925677235, 0.4123381218697539, 2.7645670358783523]
				self["LooseElectronMvaIDCutEEParamsLowPt"] = [-1830.8583661119892, -1831.2083578116517,-36578.11055382301]
				self["LooseElectronMvaIDCutEB1ParamsHighPt"] = [0.9717674837607253, 1.9712414940437244, 8.912850985100356] 
				self["LooseElectronMvaIDCutEB2ParamsHighPt"] = [0.9458745023265976, 2.40849932040698, 8.83104420392795]
				self["LooseElectronMvaIDCutEEParamsHighPt"] = [0.8979112012086751, 4.171581694893849, 9.814082144168015]
			else:
				self["LooseElectronIDName"] = "electronMVAValueMapProducer:ElectronMVAEstimatorRun2Fall17NoIsoV1Values"
				#wp 90 no iso
				self["LooseElectronMvaIDCutEB1ParamsLowPt"] = [ 0.9165112826974601, 1.03549199648109, 2.7381703555094217 ]
				self["LooseElectronMvaIDCutEB2ParamsLowPt"] = [ 0.8655738322220173, 0.7975615613282494, 2.4027944652597073 ]
				self["LooseElectronMvaIDCutEEParamsLowPt"] = [ -3016.035055227131, -3016.3029387236506, -52140.61856333602 ]   # - this is minus alot??
				self["LooseElectronMvaIDCutEB1ParamsHighPt"] = [ 0.9616542816132922, 3.1390200321591206, 8.757943837889817 ]
				self["LooseElectronMvaIDCutEB2ParamsHighPt"] = [0.9319258011430132, 3.5985063793347787, 8.846057432565809 ]
				self["LooseElectronMvaIDCutEEParamsHighPt"] = [ 0.8899260780999244, 4.352791250718547, 10.124234115859881 ]

		else:
			self["LooseElectronIDName"] = "electronMVAValueMapProducer:ElectronMVAEstimatorRun2Spring16GeneralPurposeV1Values"
			self["LooseElectronMvaIDCutEB1"] = 0.837
			self["LooseElectronMvaIDCutEB2"] = 0.715
			self["LooseElectronMvaIDCutEE"] = 0.357
			self["LooseElectronIDType"] = "mvabased2015andlater"
		
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
		elif re.search("(Run2017|Fall17)", nickname):
			self["VetoElectronIDType"] = "cutbased2015andlater"
			self["VetoElectronIDName"] = "egmGsfElectronIDs:cutBasedElectronID-Fall17-94X-V1-veto"
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

