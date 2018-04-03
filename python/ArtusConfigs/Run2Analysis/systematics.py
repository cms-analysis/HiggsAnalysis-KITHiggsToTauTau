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
		
		
	
		#Nominal
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
		isData = self.datasetsHelper.isData(nickname)
		isSignal = self.datasetsHelper.isSignal(nickname)
		isEmbedding = self.datasetsHelper.isEmbedded(nickname)
		isTTbar = re.match("TT(To|_|Jets)", nickname)
		isDY = re.match("DY.?JetsToLLM(50|150)", nickname)
		isWjets = re.match("W.?JetsToLNu", nickname)
		isLFV = ("LFV" in nickname)
		is2015 = re.search("(Run2015|Fall15|Embedding15)*?",nickname) #I am not 100% sure if this is exclusive
		is2016 = re.search("(Run2016|Sprint16|Summer16|Fall16|Embedding16)*?",nickname) #I am not 100% sure if this is exclusive	
		is2017 = re.search("(Run2017|Summer17|Fall17|Embedding17)*?",nickname) #I am not 100% sure if this is exclusive		
		print "SYST=", systematic
		if isData==False or isEmbedding:     #data has no systematic
			if is2016: 
				if systematic == "eleEsUp":
					print systematic, " == eleEsUp"
					self["ElectronEnergyCorrectionShiftEB"] = 1.01
					self["ElectronEnergyCorrectionShiftEE"] = 1.025
					self["SvfitCacheFileFolder"] = "eleEsUp"
				elif systematic == "eleEsDown":
					print systematic, " == eleEsDown"
					self["ElectronEnergyCorrectionShiftEB"] =  0.99
					self["ElectronEnergyCorrectionShiftEE"] = 0.975
					self["SvfitCacheFileFolder"] = "eleEsDown"
			
			if isEmbedding==False: #should not be data or embedding, might have to give one more indent if runyear is included
				if systematic == "jecUncUp":					
					self["JetEnergyCorrectionUncertaintyShift"] = 1
					self["SvfitCacheFileFolder"] = "nominal"
				elif systematic == "jecUncDown":
					self["JetEnergyCorrectionUncertaintyShift"] = 1
					self["SvfitCacheFileFolder"] = "nominal"

			if is2016 and isEmbedding==False:   #note was metuncshift.json is both metjecuncertainty.json and metunclustered.json
				if systematic == "metJetEnUp":
					self["MetUncertaintyShift"] = True
					self["MetUncertaintyType"] = "JetEnUp"
					self["SvfitCacheFileFolder"] = "metJetEnUp"
				elif systematic == "metJetEnDown":
					self["MetUncertaintyShift"] = True
					self["MetUncertaintyType"] = "JetEnDown"
					self["SvfitCacheFileFolder"] = "metJetEnDown"

				if systematic == "metUnclusteredEnUp":
					self["MetUncertaintyShift"] = True
					self["MetUncertaintyType"] = "UnclusteredEnUp"
					self["SvfitCacheFileFolder"] = "metUnclusteredEnUp"
				elif systematic == "metUnclusteredEnDown":
					self["MetUncertaintyShift"] = True
					self["MetUncertaintyType"] = "UnclusteredEnDown"
					self["SvfitCacheFileFolder"] = "metUnclusteredEnDown"

			if re.match("(DY.?JetsToLL|EWKZ2Jets).*(?=(Spring16|Summer16))", nickname):
				if systematic == "tauEleFakeEsUp":
					self["TauElectronFakeEnergyCorrection"] = 1.03
					self["SvfitCacheFileFolder"] = "tauEleFakeEsUp"
				elif systematic == "tauEleFakeEsDown":
					self["TauElectronFakeEnergyCorrection"] = 0.097
					self["SvfitCacheFileFolder"] = "tauEleFakeEsDown"

				if systematic == "tauMuFakeEsUp":
					self["TauMuonFakeEnergyCorrection"] = 1.015
					self["SvfitCacheFileFolder"] = "tauMuFakeEsUp"
				elif systematic == "tauMuFakeEsDown":
					self["TauMuonFakeEnergyCorrection"] = 0.985
					self["SvfitCacheFileFolder"] = "tauMuFakeEsDown"

				if systematic == "tauMuFakeEsOneProngUp":
					self["TauMuonFakeEnergyCorrectionOneProngShift"] = 1.015
					self["SvfitCacheFileFolder"] = "tauMuFakeEsOneProngUp"
				elif systematic == "tauMuFakeEsOneProngDown":
					self["TauMuonFakeEnergyCorrectionOneProngShift"] = 0.985
					self["SvfitCacheFileFolder"] = "tauMuFakeEsOneProngDown"

				if systematic == "tauMuFakeEsOneProngPiZerosUp":
					self["TauMuonFakeEnergyCorrectionOneProngPiZerosShift"] = 1.015
					self["SvfitCacheFileFolder"] =  "tauMuFakeEsOneProngPiZerosUp"
				elif systematic == "tauMuFakeEsOneProngPiZerosDown":
					self["TauMuonFakeEnergyCorrectionOneProngPiZerosShift"] = 0.985
					self["SvfitCacheFileFolder"] =  "tauMuFakeEsOneProngPiZerosDown"



			if re.match("(DY.?JetsToLL|EWKZ2Jets|LFV).*(?=(Spring16|Summer16))", nickname):
				if systematic == "tauEleFakeEsOneProngUp":
					self["TauElectronFakeEnergyCorrectionOneProngShift"] = 1.03
					self["SvfitCacheFileFolder"] = "tauEleFakeEsOneProngUp"
				elif systematic == "tauEleFakeEsOneProngDown":
					self["TauElectronFakeEnergyCorrectionOneProngShift"] = 0.97
					self["SvfitCacheFileFolder"] = "tauEleFakeEsOneProngDown" 

				if systematic == "tauEleFakeEsOneProngPiZerosUp":
					self["TauElectronFakeEnergyCorrectionOneProngPiZerosShift"] = 1.03
					self["SvfitCacheFileFolder"] = "tauEleFakeEsOneProngPiZerosUp"
				elif systematic == "tauEleFakeEsOneProngPiZerosDown":
					self["TauElectronFakeEnergyCorrectionOneProngPiZerosShift"] = 0.97
					self["SvfitCacheFileFolder"] = "tauEleFakeEsOneProngPiZerosDown"
			
			#caution tauEs splitted for several nicknames/files
			if re.match("(HToTauTau|H2JetsToTauTau|Higgs|DY.?JetsToLL|EWKZ2Jets).*(?=Fall15)", nickname):
				if systematic == "tauEsUp":
					self["TauEnergyCorrectionShift"] = 1.03
					self["SvfitCacheFileFolder"] = "tauEsUp"
				elif systematic == "tauEsDown":
					self["TauEnergyCorrectionShift"] = 0.97
					self["SvfitCacheFileFolder"] = "tauEsDown"

				if systematic == "tauEsOneProngUp":
					self["TauEnergyCorrectionOneProngShift"] = 1.03
					self["SvfitCacheFileFolder"] = "tauEsOneProngUp"
				elif systematic == "tauEsOneProngDown":
					self["TauEnergyCorrectionOneProngShift"] = 0.97
					self["SvfitCacheFileFolder"] = "tauEsOneProngDown"				
	
				if systematic == "tauEsOneProngPiZerosUp":
					self["TauEnergyCorrectionOneProngPiZerosShift"] = 1.03
					self["SvfitCacheFileFolder"] = "tauEsOneProngPiZerosUp"
				elif systematic == "tauEsOneProngPiZerosDown":
					self["TauEnergyCorrectionOneProngPiZerosShift"] = 0.97
					self["SvfitCacheFileFolder"] = "tauEsOneProngPiZerosDown"

				if systematic == "tauEsThreeProngUp":
					self["TauEnergyCorrectionThreeProngShift"] = 1.03
					self["SvfitCacheFileFolder"] = "tauEsThreeProngUp"
				elif systematic == "tauEsThreeProngDown":
					self["TauEnergyCorrectionThreeProngShift"] = 0.97
					self["SvfitCacheFileFolder"] = "tauEsThreeProngDown"


			elif "Embedding2016" in nickname:
				if systematic == "tauEsUp":
					self["TauEnergyCorrectionShift"] = 1.03
					self["SvfitCacheFileFolder"] = "tauEsUp"
				elif systematic == "tauEsDown":
					self["TauEnergyCorrectionShift"] = 0.97
					self["SvfitCacheFileFolder"] = "tauEsDown"

				if systematic == "tauEsOneProngUp":
					self["TauEnergyCorrectionOneProngShift"] = 1.03
					self["SvfitCacheFileFolder"] = "tauEsOneProngUp"
				elif systematic == "tauEsOneProngDown":
					self["TauEnergyCorrectionOneProngShift"] = 0.97
					self["SvfitCacheFileFolder"] = "tauEsOneProngDown"		

				if systematic == "tauEsOneProngPiZerosUp":
					self["TauEnergyCorrectionOneProngPiZerosShift"] = 1.03
					self["SvfitCacheFileFolder"] = "tauEsOneProngPiZerosUp"
				elif systematic == "tauEsOneProngPiZerosDown":
					self["TauEnergyCorrectionOneProngPiZerosShift"] = 0.97
					self["SvfitCacheFileFolder"] = "tauEsOneProngPiZerosDown"

				if systematic ==  "tauEsThreeProngUp":
					self["TauEnergyCorrectionThreeProngShift"] = 1.03
					self["SvfitCacheFileFolder"] = "tauEsThreeProngUp"
				elif systematic == "tauEsThreeProngDown":
					self["TauEnergyCorrectionThreeProngShift"] = 0.97
					self["SvfitCacheFileFolder"] = "tauEsThreeProngDown"
			

			elif re.search("Spring16|Summer16", nickname):
				if systematic == "tauEsUp":
					self["TauEnergyCorrectionShift"] = 1.012
					self["SvfitCacheFileFolder"] = "tauEsUp"
				elif systematic == "tauEsDown":
					self["TauEnergyCorrectionShift"] = 0.988
					self["SvfitCacheFileFolder"] = "tauEsDown"

				if systematic == "tauEsOneProngUp":
					self["TauEnergyCorrectionOneProngShift"] = 1.012
					self["SvfitCacheFileFolder"] = "tauEsOneProngUp"
				elif systematic == "tauEsOneProngDown":
					self["TauEnergyCorrectionOneProngShift"] = 0.988
					self["SvfitCacheFileFolder"] = "tauEsOneProngDown"	

				if systematic == "tauEsOneProngPiZerosUp":
					self["TauEnergyCorrectionOneProngPiZerosShift"] = 1.012
					self["SvfitCacheFileFolder"] = "tauEsOneProngPiZerosUp"
				elif systematic == "tauEsOneProngPiZerosDown":
					self["TauEnergyCorrectionOneProngPiZerosShift"] = 0.988
					self["SvfitCacheFileFolder"] = "tauEsOneProngPiZerosDown"

				if systematic == "tauEsThreeProngUp":
					self["TauEnergyCorrectionThreeProngShift"] = 1.012
					self["SvfitCacheFileFolder"] = "tauEsThreeProngUp"
				elif systematic == "tauEsThreeProngDown":
					self["TauEnergyCorrectionThreeProngShift"] = 0.988
					self["SvfitCacheFileFolder"] = "tauEsThreeProngDown"	
				#TODO tauJetFakeEsIncl
				if systematic == "tauJetFakeEsUp":
					self["TauJetFakeEnergyCorrection"] = 1.0
					self["SvfitCacheFileFolder"] = "tauJetFakeEsUp"
				elif systematic == "tauJetFakeEsDown":
					self["TauJetFakeEnergyCorrection"] = -1.0
					self["SvfitCacheFileFolder"] = "tauJetFakeEsDown"

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








