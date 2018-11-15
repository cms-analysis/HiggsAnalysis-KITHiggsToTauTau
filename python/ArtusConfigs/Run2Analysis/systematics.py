# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import re
import sys


class Systematics_Config(dict):
	def __init__(self):
		
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

		self["TauJetFakeEnergyCorrection"] = 0.0

		self["TauMuonFakeEnergyCorrection"] = 0.0

		self["TauMuonFakeEnergyCorrectionOneProngPiZerosShift"] = 0.0
		self["TauMuonFakeEnergyCorrectionOneProngShift"] = 0.0


	#for each systematic shift if statement which changes the config accordingly
	def build_systematic_config(self, nickname, systematic_uncertainty, *args, **kwargs):
		log.debug("SYST= " + systematic_uncertainty)
		if re.search("Run201", nickname) == None:    #data has no systematic
			#I dont remember why I did this, it looks wrong if re.search("JetEnergyCorrectionSplitUncertainty", nickname):
			if systematic_uncertainty == "eleEsUp":

				if re.search("Spring16|Summer16|Embedding2016", nickname):
					self["ElectronEnergyCorrectionShiftEB"] = 1.01
					self["ElectronEnergyCorrectionShiftEE"] = 1.025
					self["SvfitCacheFileFolder"] = "eleEsUp"
				else:
					self["ElectronEnergyCorrectionShiftEB"] = 1.0
					self["ElectronEnergyCorrectionShiftEE"] = 1.0
					self["SvfitCacheFileFolder"] = "nominal"
			
			elif systematic_uncertainty == "eleEsDown":
				if re.search("Spring16|Summer16|Embedding2016", nickname):
					self["ElectronEnergyCorrectionShiftEB"] =  0.99
					self["ElectronEnergyCorrectionShiftEE"] = 0.975
					self["SvfitCacheFileFolder"] = "eleEsDown"
				else:
					self["ElectronEnergyCorrectionShiftEB"] = 1.0
					self["ElectronEnergyCorrectionShiftEE"] = 1.0
					self["SvfitCacheFileFolder"] = "nominal"
			
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
				else:
					self["MetUncertaintyShift"] = False
					self["MetUncertaintyType"] = ""
					self["SvfitCacheFileFolder"] = "nominal"

			elif systematic_uncertainty == "metJetEnDown":
				if re.search("Spring16|Summer16", nickname):
					self["MetUncertaintyShift"] = True
					self["MetUncertaintyType"] = "JetEnDown"
					self["SvfitCacheFileFolder"] = "metJetEnDown"
				else:
					self["MetUncertaintyShift"] = False
					self["MetUncertaintyType"] = ""
					self["SvfitCacheFileFolder"] = "nominal"

			elif systematic_uncertainty == "metUnclusteredEnUp":
				if re.search("Spring16|Summer16", nickname):
					self["MetUncertaintyShift"] = True
					self["MetUncertaintyType"] = "UnclusteredEnUp"
					self["SvfitCacheFileFolder"] = "metUnclusteredEnUp"
				else:
					self["MetUncertaintyShift"] = False
					self["MetUncertaintyType"] = ""
					self["SvfitCacheFileFolder"] = "nominal"

			elif systematic_uncertainty == "metUnclusteredEnDown":
				if re.search("Spring16|Summer16", nickname):
					self["MetUncertaintyShift"] = True
					self["MetUncertaintyType"] = "UnclusteredEnDown"
					self["SvfitCacheFileFolder"] = "metUnclusteredEnDown"
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
				else:
					self["TauMuonFakeEnergyCorrectionOneProngShift"] = 0.0
					self["SvfitCacheFileFolder"] = "nominal"

			elif systematic_uncertainty == "tauMuFakeEsOneProngDown":
				if re.search("(DY.?JetsToLL|EWKZ2Jets|LFV).*(?=(Spring16|Summer16))", nickname):
					self["TauMuonFakeEnergyCorrectionOneProngShift"] = -0.015
					self["SvfitCacheFileFolder"] = "tauMuFakeEsOneProngDown"
				else:
					self["TauMuonFakeEnergyCorrectionOneProngShift"] = 0.0
					self["SvfitCacheFileFolder"] = "nominal"

			elif systematic_uncertainty == "tauMuFakeEsOneProngPiZerosUp":
					self["TauMuonFakeEnergyCorrectionOneProngPiZerosShift"] = 0.015
					self["SvfitCacheFileFolder"] =  "tauMuFakeEsOneProngPiZerosUp"
			elif systematic_uncertainty == "tauMuFakeEsOneProngPiZerosDown":
					self["TauMuonFakeEnergyCorrectionOneProngPiZerosShift"] = -0.015
					self["SvfitCacheFileFolder"] =  "tauMuFakeEsOneProngPiZerosDown"

			elif systematic_uncertainty == "tauEleFakeEsOneProngUp":
				if re.search("(DY.?JetsToLL|EWKZ2Jets|LFV).*(?=(Spring16|Summer16))", nickname):
					self["TauElectronFakeEnergyCorrectionOneProngShift"] = 0.03
					self["SvfitCacheFileFolder"] = "tauEleFakeEsOneProngUp"
				else:
					self["TauElectronFakeEnergyCorrectionOneProngShift"] = 0.0
					self["SvfitCacheFileFolder"] = "nominal"

			elif systematic_uncertainty == "tauEleFakeEsOneProngDown":
				if re.search("(DY.?JetsToLL|EWKZ2Jets|LFV).*(?=(Spring16|Summer16))", nickname):
					self["TauElectronFakeEnergyCorrectionOneProngShift"] = -0.03
					self["SvfitCacheFileFolder"] = "tauEleFakeEsOneProngDown"
				else:
					self["TauElectronFakeEnergyCorrectionOneProngShift"] = 0.0
					self["SvfitCacheFileFolder"] = "nominal"

			elif systematic_uncertainty == "tauEleFakeEsOneProngPiZerosUp":
				if re.search("(DY.?JetsToLL|EWKZ2Jets|LFV).*(?=(Spring16|Summer16))", nickname):
					self["TauElectronFakeEnergyCorrectionOneProngPiZerosShift"] = 0.03
					self["SvfitCacheFileFolder"] = "tauEleFakeEsOneProngPiZerosUp"
				else:
					self["TauElectronFakeEnergyCorrectionOneProngPiZerosShift"] = 0.0
					self["SvfitCacheFileFolder"] = "nominal"
			elif systematic_uncertainty == "tauEleFakeEsOneProngPiZerosDown":
				if re.search("(DY.?JetsToLL|EWKZ2Jets|LFV).*(?=(Spring16|Summer16))", nickname):
					self["TauElectronFakeEnergyCorrectionOneProngPiZerosShift"] = -0.03
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

				if re.search("HToTauTau|H2JetsToTauTau|Higgs|DY.?JetsToLL|EWKZ2Jets|Spring16|Summer16|Embedding2016", nickname):
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

				if re.search("HToTauTau|H2JetsToTauTau|Higgs|DY.?JetsToLL|EWKZ2Jets|Spring16|Summer16|Embedding2016", nickname):
					self["SvfitCacheFileFolder"] = "tauEsDown"
				else:
					self["SvfitCacheFileFolder"] = "nominal"

			elif systematic_uncertainty == "tauEsOneProngUp":
				if re.search("(HToTauTau|H2JetsToTauTau|Higgs|DY.?JetsToLL|EWKZ2Jets).*(?=Fall15)", nickname):
					self["TauEnergyCorrectionOneProngShift"] = 0.03
				elif re.search("Embedding2016", nickname):
					self["TauEnergyCorrectionOneProngShift"] = 0.012
				elif re.search("Spring16|Summer16", nickname):
					self["TauEnergyCorrectionOneProngShift"] = 0.012
				else:
					self["TauEnergyCorrectionOneProngShift"] = 0.0

				if re.search("HToTauTau|H2JetsToTauTau|Higgs|DY.?JetsToLL|EWKZ2Jets|Spring16|Summer16|Embedding2016", nickname):
					self["SvfitCacheFileFolder"] = "tauEsOneProngUp"
				else:
					self["SvfitCacheFileFolder"] = "nominal"

			elif systematic_uncertainty == "tauEsOneProngDown":
				if re.search("(HToTauTau|H2JetsToTauTau|Higgs|DY.?JetsToLL|EWKZ2Jets).*(?=Fall15)", nickname):
					self["TauEnergyCorrectionOneProngShift"] = -0.03
				elif re.search("Embedding2016", nickname):
					self["TauEnergyCorrectionOneProngShift"] = -0.012
				elif re.search("Spring16|Summer16", nickname):
					self["TauEnergyCorrectionOneProngShift"] = -0.012
				else:
					self["TauEnergyCorrectionOneProngShift"] = 0.0

				if re.search("HToTauTau|H2JetsToTauTau|Higgs|DY.?JetsToLL|EWKZ2Jets|Spring16|Summer16|Embedding2016", nickname):
					self["SvfitCacheFileFolder"] = "tauEsOneProngDown"
				else:
					self["SvfitCacheFileFolder"] = "nominal"
		
			elif systematic_uncertainty == "tauEsOneProngPiZerosUp":
				if re.search("(HToTauTau|H2JetsToTauTau|Higgs|DY.?JetsToLL|EWKZ2Jets).*(?=Fall15)", nickname):
					self["TauEnergyCorrectionOneProngPiZerosShift"] = 0.03
				elif re.search("Embedding2016", nickname):
					self["TauEnergyCorrectionOneProngPiZerosShift"] = 0.03
				elif re.search("Spring16|Summer16", nickname):
					self["TauEnergyCorrectionOneProngPiZerosShift"] = 0.012
				else:
					self["TauEnergyCorrectionOneProngPiZerosShift"] = 0.0
				
				if re.search("HToTauTau|H2JetsToTauTau|Higgs|DY.?JetsToLL|EWKZ2Jets|Spring16|Summer16|Embedding2016", nickname):
					self["SvfitCacheFileFolder"] = "tauEsOneProngPiZerosUp"
				else:
					self["SvfitCacheFileFolder"] = "nominal"

			elif systematic_uncertainty == "tauEsOneProngPiZerosDown":
				if re.search("(HToTauTau|H2JetsToTauTau|Higgs|DY.?JetsToLL|EWKZ2Jets).*(?=Fall15)", nickname):
					self["TauEnergyCorrectionOneProngPiZerosShift"] = -0.03
				elif re.search("Embedding2016", nickname):
					self["TauEnergyCorrectionOneProngPiZerosShift"] = -0.012
				elif re.search("Spring16|Summer16", nickname):
					self["TauEnergyCorrectionOneProngPiZerosShift"] = -0.012
				else:
					self["TauEnergyCorrectionOneProngPiZerosShift"] = 0.0
				

				if re.search("HToTauTau|H2JetsToTauTau|Higgs|DY.?JetsToLL|EWKZ2Jets|Spring16|Summer16|Embedding2016", nickname):
					self["SvfitCacheFileFolder"] = "tauEsOneProngPiZerosDown"
				else:
					self["SvfitCacheFileFolder"] = "nominal"

			elif systematic_uncertainty == "tauEsThreeProngUp":
				if re.search("(HToTauTau|H2JetsToTauTau|Higgs|DY.?JetsToLL|EWKZ2Jets).*(?=Fall15)", nickname):
					self["TauEnergyCorrectionThreeProngShift"] = 0.03
				elif re.search("Embedding2016", nickname):
					self["TauEnergyCorrectionThreeProngShift"] = 0.012
				elif re.search("Spring16|Summer16", nickname):
					self["TauEnergyCorrectionThreeProngShift"] = 0.012
				else:
					self["TauEnergyCorrectionThreeProngShift"] = 0.0


				if re.search("HToTauTau|H2JetsToTauTau|Higgs|DY.?JetsToLL|EWKZ2Jets|Spring16|Summer16|Embedding2016", nickname):
					self["SvfitCacheFileFolder"] = "tauEsThreeProngUp"
				else:
					self["SvfitCacheFileFolder"] = "nominal"

			elif systematic_uncertainty == "tauEsThreeProngDown":
				if re.search("(HToTauTau|H2JetsToTauTau|Higgs|DY.?JetsToLL|EWKZ2Jets).*(?=Fall15)", nickname):
					self["TauEnergyCorrectionThreeProngShift"] = -0.03
				elif re.search("Embedding2016", nickname):
					self["TauEnergyCorrectionThreeProngShift"] = -0.012
				elif re.search("Spring16|Summer16", nickname):
					self["TauEnergyCorrectionThreeProngShift"] = -0.012
				else:
					self["TauEnergyCorrectionThreeProngShift"] = 0.0

				if re.search("HToTauTau|H2JetsToTauTau|Higgs|DY.?JetsToLL|EWKZ2Jets|Spring16|Summer16|Embedding2016", nickname):
					self["SvfitCacheFileFolder"] = "tauEsThreeProngDown"
				else:
					self["SvfitCacheFileFolder"] = "nominal"

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

			else:
				log.critical("COULD NOT FIND THE SYSTEMATIC %s" %systematic_uncertainty)
				sys.exit(1)

	def clear_config(self):
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

		self["TauJetFakeEnergyCorrection"] = 0.0

		self["TauMuonFakeEnergyCorrection"] = 0.0

		self["TauMuonFakeEnergyCorrectionOneProngPiZerosShift"] = 0.0
		self["TauMuonFakeEnergyCorrectionOneProngShift"] = 0.0

