# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import re
import json
import Artus.Utility.jsonTools as jsonTools
import Kappa.Skimming.datasetsHelperTwopz as datasetsHelperTwopz

class Systematics_Config(dict):
	def __init__(self):
		#doppelgemoppel allready in the config class
		self.datasetsHelper = datasetsHelperTwopz.datasetsHelperTwopz("Kappa/Skimming/data/datasets.json") 
		
		
	
		#Nominal
		self["ElectronEnergyCorrectionShiftEB"] = 1.0 
		self["ElectronEnergyCorrectionShiftEE"] = 1.0, 
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
		isData = self.datasetsHelper.isData(nickname)
		isSignal = self.datasetsHelper.isSignal(nickname)
		isEmbedding = self.datasetsHelper.isEmbedded(nickname)
		isTTbar = re.match("TT(To|_|Jets)", nickname)
		isDY = re.match("DY.?JetsToLLM(50|150)", nickname)
		isWjets = re.match("W.?JetsToLNu", nickname)
		isLFV = ("LFV" in nickname)
		is2015 = re.match("(.*)15", nickname) #I am not 100% sure if this is exclusive
		is2016 = re.match("(.*)16", nickname) #I am not 100% sure if this is exclusive	
		is2017 = re.match("(.*)17", nickname) #I am not 100% sure if this is exclusive		
		
		if isData==False or isEmbedding:     #data has no systematics
			if is2016: 
				if "eleEsUp" in systematic:
					self["ElectronEnergyCorrectionShiftEB"] = 1.01
					self["ElectronEnergyCorrectionShiftEE"] = 1.025
					self["SvfitCacheFileFolder"] = "eleEsUp"
				elif "eleEsDown" in systematics :
					self["ElectronEnergyCorrectionShiftEB"] =  0.99
					self["ElectronEnergyCorrectionShiftEE"] = 0.975
					self["SvfitCacheFileFolder"] = "eleEsDown"
			
			if isEmbedding==False: #should not be data or embedding, might have to give one more indent if runyear is included
				if "jecUncUp" in systematic:					
					self["JetEnergyCorrectionUncertaintyShift"] = 1
					self["SvfitCacheFileFolder"] = "nominal"
				elif "jecUncDown" in systematic:
					self["JetEnergyCorrectionUncertaintyShift"] = 1
					self["SvfitCacheFileFolder"] = "nominal"

			if is2016 and isEmbedding==False:   #note was metuncshift.json is both metjecuncertainty.json and metunclustered.json
				if "metJetEnUp" in systematic:
					self["MetUncertaintyShift"] = True
					self["MetUncertaintyType"] = "JetEnUp"
					self["SvfitCacheFileFolder"] = "metJetEnUp"
				elif "metJetEnDown" in systematic:
					self["MetUncertaintyShift"] = True
					self["MetUncertaintyType"] = "JetEnDown"
					self["SvfitCacheFileFolder"] = "metJetEnDown"

				if "metUnclusteredEnUp" in systematic:
					self["MetUncertaintyShift"] = True
					self["MetUncertaintyType"] = "UnclusteredEnUp"
					self["SvfitCacheFileFolder"] = "metUnclusteredEnUp"
				elif "metUnclusteredEnDown" in systematic:
					self["MetUncertaintyShift"] = True
					self["MetUncertaintyType"] = "UnclusteredEnDown"
					self["SvfitCacheFileFolder"] = "metUnclusteredEnDown"

			if re.match("(DY.?JetsToLL|EWKZ2Jets).*(?=(Spring16|Summer16))", nickname):
				if "tauEleFakeEsUp" in systematic:
					self["TauElectronFakeEnergyCorrection"] = 1.03
					self["SvfitCacheFileFolder"] = "tauEleFakeEsUp"
				elif "tauEleFakeEsDown" in systematic:
					self["TauElectronFakeEnergyCorrection"] = 0.097
					self["SvfitCacheFileFolder"] = "tauEleFakeEsDown"

				if "tauMuFakeEsUp" in systematic:
					self["TauMuonFakeEnergyCorrection"] = 1.015
					self["SvfitCacheFileFolder"] = "tauMuFakeEsUp"
				elif "tauMuFakeEsDown" in systematic:
					self["TauMuonFakeEnergyCorrection"] = 0.985
					self["SvfitCacheFileFolder"] = "tauMuFakeEsDown"

				if "tauMuFakeEsOneProngUp" in systematic:
					self["TauMuonFakeEnergyCorrectionOneProngShift"] = 1.015
					self["SvfitCacheFileFolder"] = "tauMuFakeEsOneProngUp"
				elif "tauMuFakeEsOneProngDown" in systematic:
					self["TauMuonFakeEnergyCorrectionOneProngShift"] = 0.985
					self["SvfitCacheFileFolder"] = "tauMuFakeEsOneProngDown"

				if "tauMuFakeEsOneProngPiZerosUp" in systematic:
					self["TauMuonFakeEnergyCorrectionOneProngPiZerosShift"] = 1.015
					self["SvfitCacheFileFolder"] =  "tauMuFakeEsOneProngPiZerosUp"
				elif "tauMuFakeEsOneProngPiZerosDown" in systematic:
					self["TauMuonFakeEnergyCorrectionOneProngPiZerosShift"] = 0.985
					self["SvfitCacheFileFolder"] =  "tauMuFakeEsOneProngPiZerosDown"



			if re.match("(DY.?JetsToLL|EWKZ2Jets|LFV).*(?=(Spring16|Summer16))", nickname):
				if "tauEleFakeEsOneProngUp" in systematic:
					self["TauElectronFakeEnergyCorrectionOneProngShift"] = 1.03
					self["SvfitCacheFileFolder"] = "tauEleFakeEsOneProngUp"
				elif "tauEleFakeEsOneProngDown" in systematic:
					self["TauElectronFakeEnergyCorrectionOneProngShift"] = 0.97
					self["SvfitCacheFileFolder"] = "tauEleFakeEsOneProngDown" 

				if "tauEleFakeEsOneProngPiZerosUp" in systematic:
					self["TauElectronFakeEnergyCorrectionOneProngPiZerosShift"] = 1.03
					self["SvfitCacheFileFolder"] = "tauEleFakeEsOneProngPiZerosUp"
				elif "tauEleFakeEsOneProngPiZerosDown" in systematic:
					self["TauElectronFakeEnergyCorrectionOneProngPiZerosShift"] = 0.97
					self["SvfitCacheFileFolder"] = "tauEleFakeEsOneProngPiZerosDown"
			
			#caution tauEs splitted for several nicknames/files
			if re.match("(HToTauTau|H2JetsToTauTau|Higgs|DY.?JetsToLL|EWKZ2Jets).*(?=Fall15)", nickname):
				if "tauEsUp" in systematic:
					self["TauEnergyCorrectionShift"] = 1.03
					self["SvfitCacheFileFolder"] = "tauEsUp"
				elif "tauEsDown" in systematic:
					self["TauEnergyCorrectionShift"] = 0.97
					self["SvfitCacheFileFolder"] = "tauEsDown"

				if "tauEsOneProngUp" in systematic:
					self["TauEnergyCorrectionOneProngShift"] = 1.03
					self["SvfitCacheFileFolder"] = "tauEsOneProngUp"
				elif "tauEsOneProngDown" in systematic:
					self["TauEnergyCorrectionOneProngShift"] = 0.97
					self["SvfitCacheFileFolder"] = "tauEsOneProngDown"				
	
				if "tauEsOneProngPiZerosUp" in systematic:
					self["TauEnergyCorrectionOneProngPiZerosShift"] = 1.03
					self["SvfitCacheFileFolder"] = "tauEsOneProngPiZerosUp"
				elif "tauEsOneProngPiZerosDown" in systematics:
					self["TauEnergyCorrectionOneProngPiZerosShift"] = 0.97
					self["SvfitCacheFileFolder"] = "tauEsOneProngPiZerosDown"

				if "tauEsThreeProngUp" in systematic:
					self["TauEnergyCorrectionThreeProngShift"] = 1.03
					self["SvfitCacheFileFolder"] = "tauEsThreeProngUp"
				elif "tauEsThreeProngDown" in systematic:
					self["TauEnergyCorrectionThreeProngShift"] = 0.97
					self["SvfitCacheFileFolder"] = "tauEsThreeProngDown"


			elif "Embedding2016" in nickname:
				if "tauEsUp" in systematics:
					self["TauEnergyCorrectionShift"] = 1.03
					self["SvfitCacheFileFolder"] = "tauEsUp"
				elif "tauEsDown" in systematics:
					self["TauEnergyCorrectionShift"] = 0.97
					self["SvfitCacheFileFolder"] = "tauEsDown"

				if "tauEsOneProngUp" in systematics:
					self["TauEnergyCorrectionOneProngShift"] = 1.03
					self["SvfitCacheFileFolder"] = "tauEsOneProngUp"
				elif "tauEsOneProngDown" in systematics:
					self["TauEnergyCorrectionOneProngShift"] = 0.97
					self["SvfitCacheFileFolder"] = "tauEsOneProngDown"		

				if "tauEsOneProngPiZerosUp" in systematics:
					self["TauEnergyCorrectionOneProngPiZerosShift"] = 1.03
					self["SvfitCacheFileFolder"] = "tauEsOneProngPiZerosUp"
				elif "tauEsOneProngPiZerosDown" in systematics:
					self["TauEnergyCorrectionOneProngPiZerosShift"] = 0.97
					self["SvfitCacheFileFolder"] = "tauEsOneProngPiZerosDown"

				if "tauEsThreeProngUp" in systematic:
					self["TauEnergyCorrectionThreeProngShift"] = 1.03
					self["SvfitCacheFileFolder"] = "tauEsThreeProngUp"
				elif "tauEsThreeProngDown" in systematic:
					self["TauEnergyCorrectionThreeProngShift"] = 0.97
					self["SvfitCacheFileFolder"] = "tauEsThreeProngDown"
			

			elif re.match("Spring16|Summer16", nickname):
				if "tauEsUp" in systematics:
					self["TauEnergyCorrectionShift"] = 1.012
					self["SvfitCacheFileFolder"] = "tauEsUp"
				elif "tauEsDown" in systematics:
					self["TauEnergyCorrectionShift"] = 0.988
					self["SvfitCacheFileFolder"] = "tauEsDown"

				if "tauEsOneProngUp" in systematics:
					self["TauEnergyCorrectionOneProngShift"] = 1.012
					self["SvfitCacheFileFolder"] = "tauEsOneProngUp"
				elif "tauEsOneProngDown" in systematics:
					self["TauEnergyCorrectionOneProngShift"] = 0.988
					self["SvfitCacheFileFolder"] = "tauEsOneProngDown"	

				if "tauEsOneProngPiZerosUp" in systematics:
					self["TauEnergyCorrectionOneProngPiZerosShift"] = 1.012
					self["SvfitCacheFileFolder"] = "tauEsOneProngPiZerosUp"
				elif "tauEsOneProngPiZerosDown" in systematics:
					self["TauEnergyCorrectionOneProngPiZerosShift"] = 0.988
					self["SvfitCacheFileFolder"] = "tauEsOneProngPiZerosDown"

				if "tauEsThreeProngUp" in systematic:
					self["TauEnergyCorrectionThreeProngShift"] = 1.012
					self["SvfitCacheFileFolder"] = "tauEsThreeProngUp"
				elif "tauEsThreeProngDown" in systematic:
					self["TauEnergyCorrectionThreeProngShift"] = 0.988
					self["SvfitCacheFileFolder"] = "tauEsThreeProngDown"	
				#TODO tauJetFakeEsIncl
				if "tauJetFakeEsUp" in systematic:
					self["TauJetFakeEnergyCorrection"] = 1.0
					self["SvfitCacheFileFolder"] = "tauJetFakeEsUp"
				elif "tauJetFakeEsDonw" in systematic:
					self["TauJetFakeEnergyCorrection"] = -1.0
					self["SvfitCacheFileFolder"] = "tauJetFakeEsDown"










