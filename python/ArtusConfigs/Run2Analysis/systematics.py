# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import re
import json
import copy
import os
import Artus.Utility.jsonTools as jsonTools
import Kappa.Skimming.datasetsHelperTwopz as datasetsHelperTwopz

class Systematics_Config(dict):
	def __init__(self):
		#doppelgemoppel allready in the config class
		self.datasetsHelper = datasetsHelperTwopz.datasetsHelperTwopz(os.path.expandvars("$CMSSW_BASE/src/Kappa/Skimming/data/datasets.json")) 
		
		
	
		#Nominal the clear config function is also just a copy of this. (caution python does strange things when updating a dict!!!!)
		self["ElectronEnergyCorrectionShiftEB"] = 1.0 
		self["ElectronEnergyCorrectionShiftEE"] = 1.0
		self["JetEnergyCorrectionUncertaintyShift"] = 0.0 
		self["MetUncertaintyShift"] = False 
		self["MetUncertaintyType"] = "" 
		self["SvfitCacheFileFolder"] = "nominal"
		self["TauElectronFakeEnergyCorrection"] = 1.0 
		self["TauElectronFakeEnergyCorrectionOneProngPiZerosShift"] = 1.0
		self["TauElectronFakeEnergyCorrectionOneProngShift"] = 1.0 
		self["TauEnergyCorrectionOneProngPiZerosShift"] = 1.0 
		self["TauEnergyCorrectionOneProngShift"] = 1.0 
		self["TauEnergyCorrectionShift"] = 1.0 
		self["TauEnergyCorrectionThreeProngShift"] = 1.0 
		self["TauJetFakeEnergyCorrection"] = 0.0 
		self["TauMuonFakeEnergyCorrection"] = 1.0 
		self["TauMuonFakeEnergyCorrectionOneProngPiZerosShift"] = 1.0 
		self["TauMuonFakeEnergyCorrectionOneProngShift"] = 1.0

		
    
	#for each systematic shift if statement which changes the config accordingly
	def build_systematic_config(self, nickname, systematic):
		log.debug("SYST=", systematic)
		if isData==False or isEmbedding:     #data has no systematic
			#I dont remember why I did this, it looks wrong if re.search("JetEnergyCorrectionSplitUncertainty", nickname): 
			if systematic == "eleEsUp":
				if re.search("Spring16|Summer16|Embedding2016", nickname): 
					self["ElectronEnergyCorrectionShiftEB"] = 1.01
					self["ElectronEnergyCorrectionShiftEE"] = 1.025
					self["SvfitCacheFileFolder"] = "eleEsUp"
				else:
					self["ElectronEnergyCorrectionShiftEB"] = 1.0
					self["ElectronEnergyCorrectionShiftEE"] = 1.0
					self["SvfitCacheFileFolder"] = "nominal"
				


			elif systematic == "eleEsDown":
				if re.search("Spring16|Summer16|Embedding2016", nickname): 
					self["ElectronEnergyCorrectionShiftEB"] =  0.99
					self["ElectronEnergyCorrectionShiftEE"] = 0.975
					self["SvfitCacheFileFolder"] = "eleEsDown"
				else:
					self["ElectronEnergyCorrectionShiftEB"] = 1.0
					self["ElectronEnergyCorrectionShiftEE"] = 1.0
					self["SvfitCacheFileFolder"] = "nominal"
			
			
			if systematic == "jecUncUp":					
				if re.search("Run201|Embedding"): 
					self["JetEnergyCorrectionUncertaintyShift"] = 0.0
				else:
					self["JetEnergyCorrectionUncertaintyShift"] = 1.0

				self["JetEnergyCorrectionSplitUncertainty"] = False
				self["AbsJetEnergyCorrectionSplitUncertaintyShift"] = 0.0				

				self["SvfitCacheFileFolder"] = "nominal"
			elif systematic == "jecUncDown":
				if re.search("Run201|Embedding"): 
					self["JetEnergyCorrectionUncertaintyShift"] = 0.0
				else:
					self["JetEnergyCorrectionUncertaintyShift"] = -1.0		
				
				self["JetEnergyCorrectionSplitUncertainty"] = False
				self["AbsJetEnergyCorrectionSplitUncertaintyShift"] = 0.0

				self["SvfitCacheFileFolder"] = "nominal"

			
			if systematic == "metJetEnUp":
				if re.search("Spring16|Summer16", nickname):
					self["MetUncertaintyShift"] = True
					self["MetUncertaintyType"] = "JetEnUp"
					self["SvfitCacheFileFolder"] = "metJetEnUp"
				else:
					self["MetUncertaintyShift"] = False
					self["MetUncertaintyType"] = ""
					self["SvfitCacheFileFolder"] = "nominal"




			elif systematic == "metJetEnDown":
				if re.search("Spring16|Summer16", nickname):
					self["MetUncertaintyShift"] = True
					self["MetUncertaintyType"] = "JetEnDown"
					self["SvfitCacheFileFolder"] = "metJetEnDown"
				else:
					self["MetUncertaintyShift"] = False
					self["MetUncertaintyType"] = ""
					self["SvfitCacheFileFolder"] = "nominal"

			if systematic == "metUnclusteredEnUp":
				if re.search("Spring16|Summer16", nickname):
					self["MetUncertaintyShift"] = True
					self["MetUncertaintyType"] = "UnclusteredEnUp"
					self["SvfitCacheFileFolder"] = "metUnclusteredEnUp"
				else:
					self["MetUncertaintyShift"] = False
					self["MetUncertaintyType"] = ""
					self["SvfitCacheFileFolder"] = "nominal"

			elif systematic == "metUnclusteredEnDown":
				if re.search("Spring16|Summer16", nickname):
					self["MetUncertaintyShift"] = True
					self["MetUncertaintyType"] = "UnclusteredEnDown"
					self["SvfitCacheFileFolder"] = "metUnclusteredEnDown"
				else:
					self["MetUncertaintyShift"] = False
					self["MetUncertaintyType"] = ""
					self["SvfitCacheFileFolder"] = "nominal"



			if systematic == "tauEleFakeEsUp":
				if re.search("(DY.?JetsToLL|EWKZ2Jets).*(?=(Spring16|Summer16))", nickname):
					self["TauElectronFakeEnergyCorrection"] = 1.03
					self["SvfitCacheFileFolder"] = "tauEleFakeEsUp"
				else:
					self["TauElectronFakeEnergyCorrection"] = 1.0
					self["SvfitCacheFileFolder"] = "nominal"

			elif systematic == "tauEleFakeEsDown":
				if re.search("(DY.?JetsToLL|EWKZ2Jets).*(?=(Spring16|Summer16))", nickname):
					self["TauElectronFakeEnergyCorrection"] = 0.097
					self["SvfitCacheFileFolder"] = "tauEleFakeEsDown"
				else:
					self["TauElectronFakeEnergyCorrection"] = 1.0
					self["SvfitCacheFileFolder"] = "nominal"



			if systematic == "tauMuFakeEsUp":
				if re.search("(DY.?JetsToLL|EWKZ2Jets).*(?=(Spring16|Summer16))", nickname):
					self["TauMuonFakeEnergyCorrection"] = 1.015
					self["SvfitCacheFileFolder"] = "tauMuFakeEsUp"
				else:
					self["TauMuonFakeEnergyCorrection"] = 1.0
					self["SvfitCacheFileFolder"] = "nominal"

			elif systematic == "tauMuFakeEsDown":
				if re.search("(DY.?JetsToLL|EWKZ2Jets).*(?=(Spring16|Summer16))", nickname):
					self["TauMuonFakeEnergyCorrection"] = 0.985
					self["SvfitCacheFileFolder"] = "tauMuFakeEsDown"
				else:
					self["TauMuonFakeEnergyCorrection"] = 1.0
					self["SvfitCacheFileFolder"] = "nominal"

			if systematic == "tauMuFakeEsOneProngUp":
				if re.search("(DY.?JetsToLL|EWKZ2Jets|LFV).*(?=(Spring16|Summer16))", nickname):
					self["TauMuonFakeEnergyCorrectionOneProngShift"] = 1.015
					self["SvfitCacheFileFolder"] = "tauMuFakeEsOneProngUp"
				else:
					self["TauMuonFakeEnergyCorrectionOneProngShift"] = 1.0
					self["SvfitCacheFileFolder"] = "nominal"



			elif systematic == "tauMuFakeEsOneProngDown":
				if re.search("(DY.?JetsToLL|EWKZ2Jets|LFV).*(?=(Spring16|Summer16))", nickname):
					self["TauMuonFakeEnergyCorrectionOneProngShift"] = 0.985
					self["SvfitCacheFileFolder"] = "tauMuFakeEsOneProngDown"
				else:
					self["TauMuonFakeEnergyCorrectionOneProngShift"] = 1.0
					self["SvfitCacheFileFolder"] = "nominal"


			if systematic == "tauMuFakeEsOneProngPiZerosUp":
					self["TauMuonFakeEnergyCorrectionOneProngPiZerosShift"] = 1.015
					self["SvfitCacheFileFolder"] =  "tauMuFakeEsOneProngPiZerosUp"
			elif systematic == "tauMuFakeEsOneProngPiZerosDown":
					self["TauMuonFakeEnergyCorrectionOneProngPiZerosShift"] = 0.985
					self["SvfitCacheFileFolder"] =  "tauMuFakeEsOneProngPiZerosDown"




			if systematic == "tauEleFakeEsOneProngUp":
				if re.search("(DY.?JetsToLL|EWKZ2Jets|LFV).*(?=(Spring16|Summer16))", nickname):
					self["TauElectronFakeEnergyCorrectionOneProngShift"] = 1.03
					self["SvfitCacheFileFolder"] = "tauEleFakeEsOneProngUp"
				else:
					self["TauElectronFakeEnergyCorrectionOneProngShift"] = 1.0
					self["SvfitCacheFileFolder"] = "nominal"

			elif systematic == "tauEleFakeEsOneProngDown":
				if re.search("(DY.?JetsToLL|EWKZ2Jets|LFV).*(?=(Spring16|Summer16))", nickname):
					self["TauElectronFakeEnergyCorrectionOneProngShift"] = 0.97
					self["SvfitCacheFileFolder"] = "tauEleFakeEsOneProngDown" 
				else:
					self["TauElectronFakeEnergyCorrectionOneProngShift"] = 1.0
					self["SvfitCacheFileFolder"] = "nominal"


			if systematic == "tauEleFakeEsOneProngPiZerosUp":
				if re.search("(DY.?JetsToLL|EWKZ2Jets|LFV).*(?=(Spring16|Summer16))", nickname):
					self["TauElectronFakeEnergyCorrectionOneProngPiZerosShift"] = 1.03
					self["SvfitCacheFileFolder"] = "tauEleFakeEsOneProngPiZerosUp"
				else:
					self["TauElectronFakeEnergyCorrectionOneProngPiZerosShift"] = 1.0
					self["SvfitCacheFileFolder"] = "nominal"
			elif systematic == "tauEleFakeEsOneProngPiZerosDown":
				if re.search("(DY.?JetsToLL|EWKZ2Jets|LFV).*(?=(Spring16|Summer16))", nickname):
					self["TauElectronFakeEnergyCorrectionOneProngPiZerosShift"] = 0.97
					self["SvfitCacheFileFolder"] = "tauEleFakeEsOneProngPiZerosDown"
				else:
					self["TauElectronFakeEnergyCorrectionOneProngPiZerosShift"] = 1.0
					self["SvfitCacheFileFolder"] = "nominal"
			
			#caution tauEs splitted for several nicknames/files

			if systematic == "tauEsUp":
				if re.search("(HToTauTau|H2JetsToTauTau|Higgs|DY.?JetsToLL|EWKZ2Jets).*(?=Fall15)", nickname):
					self["TauEnergyCorrectionShift"] = 1.03
				elif re.search("Embedding2016". nickname):
					self["TauEnergyCorrectionShift"] = 1.03
				elif re.search("Spring16|Summer16", nickname):
					self["TauEnergyCorrectionShift"] = 1.012
				else:
					self["TauEnergyCorrectionShift"] = 1.0

				if re.search("HToTauTau|H2JetsToTauTau|Higgs|DY.?JetsToLL|EWKZ2Jets|Spring16|Summer16|Embedding2016", nickname):
					self["SvfitCacheFileFolder"] = "tauEsUp"
				else:
					self["SvfitCacheFileFolder"] = "nominal"
			elif systematic == "tauEsDown":
				if re.search("(HToTauTau|H2JetsToTauTau|Higgs|DY.?JetsToLL|EWKZ2Jets).*(?=Fall15)", nickname):
					self["TauEnergyCorrectionShift"] = 0.97
				elif re.search("Embedding2016". nickname):
					self["TauEnergyCorrectionShift"] = 0.97
				elif re.search("Spring16|Summer16", nickname):
					self["TauEnergyCorrectionShift"] = 0.988
				else:
					self["TauEnergyCorrectionShift"] = 1.0

				if re.search("HToTauTau|H2JetsToTauTau|Higgs|DY.?JetsToLL|EWKZ2Jets|Spring16|Summer16|Embedding2016", nickname):
					self["SvfitCacheFileFolder"] = "tauEsDown"
				else:
					self["SvfitCacheFileFolder"] = "nominal"

			if systematic == "tauEsOneProngUp":
				if re.search("(HToTauTau|H2JetsToTauTau|Higgs|DY.?JetsToLL|EWKZ2Jets).*(?=Fall15)", nickname):
					self["TauEnergyCorrectionOneProngShift"] = 1.03
				elif re.search("Embedding2016". nickname):
					self["TauEnergyCorrectionOneProngShift"] = 1.03
				elif re.search("Spring16|Summer16", nickname):
					self["TauEnergyCorrectionOneProngShift"] = 1.012
				else:
					self["TauEnergyCorrectionOneProngShift"] = 1.0

				if re.search("HToTauTau|H2JetsToTauTau|Higgs|DY.?JetsToLL|EWKZ2Jets|Spring16|Summer16|Embedding2016", nickname):
					self["SvfitCacheFileFolder"] = "tauEsOneProngUp"
				else:
					self["SvfitCacheFileFolder"] = "nominal"

			
			elif systematic == "tauEsOneProngDown":
				if re.search("(HToTauTau|H2JetsToTauTau|Higgs|DY.?JetsToLL|EWKZ2Jets).*(?=Fall15)", nickname):
					self["TauEnergyCorrectionOneProngShift"] = 0.97
				elif re.search("Embedding2016". nickname):
					self["TauEnergyCorrectionOneProngShift"] = 0.97
				elif re.search("Spring16|Summer16", nickname):
					self["TauEnergyCorrectionOneProngShift"] = 0.988
				else:
					self["TauEnergyCorrectionOneProngShift"] = 1.0

				if re.search("HToTauTau|H2JetsToTauTau|Higgs|DY.?JetsToLL|EWKZ2Jets|Spring16|Summer16|Embedding2016", nickname):
					self["SvfitCacheFileFolder"] = "tauEsOneProngDown"	
				else:
					self["SvfitCacheFileFolder"] = "nominal"
		
	
			if systematic == "tauEsOneProngPiZerosUp":
				if re.search("(HToTauTau|H2JetsToTauTau|Higgs|DY.?JetsToLL|EWKZ2Jets).*(?=Fall15)", nickname):
					self["TauEnergyCorrectionOneProngPiZerosShift"] = 1.03
				elif re.search("Embedding2016". nickname):
					self["TauEnergyCorrectionOneProngPiZerosShift"] = 1.03
				elif re.search("Spring16|Summer16", nickname):
					self["TauEnergyCorrectionOneProngPiZerosShift"] = 1.012
				else:
					self["TauEnergyCorrectionOneProngPiZerosShift"] = 1.0
					


				if re.search("HToTauTau|H2JetsToTauTau|Higgs|DY.?JetsToLL|EWKZ2Jets|Spring16|Summer16|Embedding2016", nickname):
					self["SvfitCacheFileFolder"] = "tauEsOneProngPiZerosUp"
				else:
					self["SvfitCacheFileFolder"] = "nominal"

			elif systematic == "tauEsOneProngPiZerosDown":
				if re.search("(HToTauTau|H2JetsToTauTau|Higgs|DY.?JetsToLL|EWKZ2Jets).*(?=Fall15)", nickname):
					self["TauEnergyCorrectionOneProngPiZerosShift"] = 0.97
				elif re.search("Embedding2016". nickname):
					self["TauEnergyCorrectionOneProngPiZerosShift"] = 0.97
				elif re.search("Spring16|Summer16", nickname):
					self["TauEnergyCorrectionOneProngPiZerosShift"] = 0.988
				else:
					self["TauEnergyCorrectionOneProngPiZerosShift"] = 1.0
				

				if re.search("HToTauTau|H2JetsToTauTau|Higgs|DY.?JetsToLL|EWKZ2Jets|Spring16|Summer16|Embedding2016", nickname):
					self["SvfitCacheFileFolder"] = "tauEsOneProngPiZerosDown"
				else:
					self["SvfitCacheFileFolder"] = "nominal"

			if systematic == "tauEsThreeProngUp":
				if re.search("(HToTauTau|H2JetsToTauTau|Higgs|DY.?JetsToLL|EWKZ2Jets).*(?=Fall15)", nickname):	
					self["TauEnergyCorrectionThreeProngShift"] = 1.03
				elif re.search("Embedding2016". nickname):
					self["TauEnergyCorrectionThreeProngShift"] = 1.03
				elif re.search("Spring16|Summer16", nickname):
					self["TauEnergyCorrectionThreeProngShift"] = 1.012
				else:		
					self["TauEnergyCorrectionThreeProngShift"] = 1.0


				if re.search("HToTauTau|H2JetsToTauTau|Higgs|DY.?JetsToLL|EWKZ2Jets|Spring16|Summer16|Embedding2016", nickname):
					self["SvfitCacheFileFolder"] = "tauEsThreeProngUp"
				else:
					self["SvfitCacheFileFolder"] = "nominal"


			elif systematic == "tauEsThreeProngDown":
				if re.search("(HToTauTau|H2JetsToTauTau|Higgs|DY.?JetsToLL|EWKZ2Jets).*(?=Fall15)", nickname):	
					self["TauEnergyCorrectionThreeProngShift"] = 0.97
				elif re.search("Embedding2016". nickname):
					self["TauEnergyCorrectionThreeProngShift"] = 0.97
				elif re.search("Spring16|Summer16", nickname):
					self["TauEnergyCorrectionThreeProngShift"] = 0.988
				else:		
					self["TauEnergyCorrectionThreeProngShift"] = 1.0

				if re.search("HToTauTau|H2JetsToTauTau|Higgs|DY.?JetsToLL|EWKZ2Jets|Spring16|Summer16|Embedding2016", nickname):
					self["SvfitCacheFileFolder"] = "tauEsThreeProngDown"
				else:
					self["SvfitCacheFileFolder"] = "nominal"


			

			
			if systematic == "tauJetFakeEsUp":
				if re.search("Spring16|Summer16", nickname):
					self["TauJetFakeEnergyCorrection"] = 1.0
					self["SvfitCacheFileFolder"] = "tauJetFakeEsUp"
				else:
					self["TauJetFakeEnergyCorrection"] = 0.0
					self["SvfitCacheFileFolder"] = "nominal"
			elif systematic == "tauJetFakeEsDown":
				if re.search("Spring16|Summer16", nickname):
					self["TauJetFakeEnergyCorrection"] = -1.0
					self["SvfitCacheFileFolder"] = "tauJetFakeEsDown"
				else:
					self["TauJetFakeEnergyCorrection"] = 0.0
					self["SvfitCacheFileFolder"] = "nominal"



	def clear_config(self):
		self["ElectronEnergyCorrectionShiftEB"] = 1.0 
		self["ElectronEnergyCorrectionShiftEE"] = 1.0
		self["JetEnergyCorrectionUncertaintyShift"] = 0.0 
		self["MetUncertaintyShift"] = False 
		self["MetUncertaintyType"] = "" 
		self["SvfitCacheFileFolder"] = "nominal"
		self["TauElectronFakeEnergyCorrection"] = 1.0 
		self["TauElectronFakeEnergyCorrectionOneProngPiZerosShift"] = 1.0
		self["TauElectronFakeEnergyCorrectionOneProngShift"] = 1.0 
		self["TauEnergyCorrectionOneProngPiZerosShift"] = 1.0 
		self["TauEnergyCorrectionOneProngShift"] = 1.0 
		self["TauEnergyCorrectionShift"] = 1.0 
		self["TauEnergyCorrectionThreeProngShift"] = 1.0 
		self["TauJetFakeEnergyCorrection"] = 0.0 
		self["TauMuonFakeEnergyCorrection"] = 1.0 
		self["TauMuonFakeEnergyCorrectionOneProngPiZerosShift"] = 1.0 
		self["TauMuonFakeEnergyCorrectionOneProngShift"] = 1.0








