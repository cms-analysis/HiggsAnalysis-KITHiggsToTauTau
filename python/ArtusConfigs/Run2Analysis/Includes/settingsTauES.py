# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import re


class TauES(dict):
	def __init__(self, nickname, legacy=True):
	#HttTauCorrectionsProducer.cc in kithiggs
	#tau.p4*shiftvalue     shiftvalue = 1. means no shift
		if re.search("(Spring16|Summer16|Embedding2016)",nickname):
			if legacy:
				self["TauEnergyCorrection"] = "legacy2016"
			else:
				self["TauEnergyCorrection"] = "smhtt2016"

				if re.search("Embedding2016",nickname):
					self["TauEnergyCorrectionOneProng"] = 0.997
					self["TauEnergyCorrectionOneProngPiZeros"] = 1.002
				else:
					self["TauEnergyCorrectionOneProng"] = 0.995
					self["TauEnergyCorrectionOneProngPiZeros"] = 1.011
				self["TauEnergyCorrectionThreeProng"] = 1.006

		elif re.search("(Summer17|Fall17|Embedding2017)",nickname):
			#https://indico.cern.ch/event/738043/contributions/3048471/attachments/1674773/2688351/TauId_26062018.pdf old
			#newest look at tautwiki
			if legacy:
				self["TauEnergyCorrection"] = "legacy2017"
			else:
				self["TauEnergyCorrection"] = "smhtt2017"
				self["TauEnergyCorrectionOneProng"] = 1.007 #+-0.8%
				self["TauEnergyCorrectionOneProngPiZeros"] = 0.998 #+-0.8%
				self["TauEnergyCorrectionThreeProng"] = 1.001 #+-0.9%
				self["TauEnergyCorrectionThreeProngPizeros"] = 0.999 #+-1%

				if re.search("Embedding2017", nickname): # no ES corrections for embedding 2017, but uncertainties are needed
					self["TauEnergyCorrectionOneProng"] = 1.0 #+-1.5%
					self["TauEnergyCorrectionOneProngPiZeros"] = 1.0 #+-1.5%
					self["TauEnergyCorrectionThreeProng"] = 1.0 #+-1.5%
					self["TauEnergyCorrectionThreeProngPizeros"] = 1.0 #+-1.5%

				if re.search("(DY.?JetsToLL|EWKZ2Jets)", nickname):
					# official e/mu fake ES factors
					self["TauElectronFakeEnergyCorrectionOneProng"] = 1.003
					self["TauElectronFakeEnergyCorrectionOneProngPiZeros"] = 1.036
					self["TauElectronFakeEnergyCorrectionThreeProng"] = 1.0
					self["TauMuonFakeEnergyCorrectionOneProng"] = 1.0
					self["TauMuonFakeEnergyCorrectionOneProngPiZeros"] = 1.0
					self["TauMuonFakeEnergyCorrectionThreeProng"] = 1.0

					# IC e/mu fake ES factors
					# self["TauElectronFakeEnergyCorrectionOneProng"] = 1.01  #+-1.4%
					# self["TauElectronFakeEnergyCorrectionOneProngPiZeros"] = 1.041 #+-1.8%
					# self["TauElectronFakeEnergyCorrectionThreeProng"] = 1.0
					# self["TauMuonFakeEnergyCorrectionOneProng"] = 0.999 #+-3%
					# self["TauMuonFakeEnergyCorrectionOneProngPiZeros"] = 1.012 #+-0.3%
					# self["TauMuonFakeEnergyCorrectionThreeProng"] = 1.0
		elif re.search("(Run2018|Autumn18)", nickname):
			if legacy:
				self["TauEnergyCorrection"] = "legacy2018"
			else:
				self["TauEnergyCorrection"] = "none"
		else:
			self["TauEnergyCorrection"] = "none"

		# if re.search("(Summer17|Fall17|Embedding2017)",nickname):
		# 	if re.search("(Summer17|Fall17)",nickname):
		# 		# self["TauIDEfficiencyWeightTight"] = 0.89 # +-3%
		# 		# self["TauIDEfficiencyWeightVLoose"] = 0.88 # +-3%
		# 		pass # TODO clean this up

		if re.search("(Embedding201(6|7|8))",nickname):
			if legacy:
				# https://twiki.cern.ch/twiki/bin/view/CMS/TauTauEmbeddingSamples2016Legacy#Lepton_energy_scale_corrections
				# https://twiki.cern.ch/twiki/bin/viewauth/CMS/TauTauEmbeddingSamples2017#Lepton_energy_scale_corrections
				# https://twiki.cern.ch/twiki/bin/viewauth/CMS/TauTauEmbeddingSamples2018#Lepton_energy_scale_corrections
				self["TauEnergyCorrection"] = "embedding"
				if re.search("(Embedding2016)",nickname):
					self["TauEnergyCorrectionOneProng"] = 0.998
					self["TauEnergyCorrectionOneProngShiftUp"] = 0.0046
					self["TauEnergyCorrectionOneProngShiftDown"] = 0.0046
					self["TauEnergyCorrectionOneProngPiZeros"] = 0.9978
					self["TauEnergyCorrectionOneProngPiZerosShiftUp"] = 0.0022
					self["TauEnergyCorrectionOneProngPiZerosShiftDown"] = 0.0025
					self["TauEnergyCorrectionThreeProng"] = 0.9874
					self["TauEnergyCorrectionThreeProngShiftUp"] = 0.0033
					self["TauEnergyCorrectionThreeProngShiftDown"] = 0.0051

					# Barrel: abs(eta) < 1.479, endcap: abs(eta) > 1.479
					self["TauElectronFakeEnergyCorrectionBarrel"] = 0.9976
					self["TauElectronFakeEnergyCorrectionBarrelShift"] = 0.005
					self["TauElectronFakeEnergyCorrectionEndCap"] = 0.993
					self["TauElectronFakeEnergyCorrectionEndCapShift"] = 0.0125

				if re.search("(Embedding2017)",nickname):
					self["TauEnergyCorrectionOneProng"] = 0.9996
					self["TauEnergyCorrectionOneProngShiftUp"] = 0.0041
					self["TauEnergyCorrectionOneProngShiftDown"] = 0.0042
					self["TauEnergyCorrectionOneProngPiZeros"] = 0.988
					self["TauEnergyCorrectionOneProngPiZerosShiftUp"] = 0.0052
					self["TauEnergyCorrectionOneProngPiZerosShiftDown"] = 0.0021
					self["TauEnergyCorrectionThreeProng"] = 0.9925
					self["TauEnergyCorrectionThreeProngShiftUp"] = 0.0044
					self["TauEnergyCorrectionThreeProngShiftDown"] = 0.0046

					# Barrel: abs(eta) < 1.479, endcap: abs(eta) > 1.479
					self["TauElectronFakeEnergyCorrectionBarrel"] = 0.9993
					self["TauElectronFakeEnergyCorrectionBarrelShift"] = 0.005
					self["TauElectronFakeEnergyCorrectionEndCap"] = 0.9887
					self["TauElectronFakeEnergyCorrectionEndCapShift"] = 0.0125

				if re.search("(Embedding2018)",nickname):
					self["TauEnergyCorrectionOneProng"] = 0.9967
					self["TauEnergyCorrectionOneProngShiftUp"] = 0.0039
					self["TauEnergyCorrectionOneProngShiftDown"] = 0.0039
					self["TauEnergyCorrectionOneProngPiZeros"] = 0.9943
					self["TauEnergyCorrectionOneProngPiZerosShiftUp"] = 0.0037
					self["TauEnergyCorrectionOneProngPiZerosShiftDown"] = 0.0031
					self["TauEnergyCorrectionThreeProng"] = 0.9926
					self["TauEnergyCorrectionThreeProngShiftUp"] = 0.0032
					self["TauEnergyCorrectionThreeProngShiftDown"] = 0.0032

					# Barrel: abs(eta) < 1.479, endcap: abs(eta) > 1.479
					self["TauElectronFakeEnergyCorrectionBarrel"] = 0.9967
					self["TauElectronFakeEnergyCorrectionBarrelShift"] = 0.005
					self["TauElectronFakeEnergyCorrectionEndCap"] = 0.9944
					self["TauElectronFakeEnergyCorrectionEndCapShift"] = 0.0125

		# NOTE: not applied here anymore. Easier to apply as cutstring later
		# 		self["TauTrackReconstructionEfficiencyWeightOneProng"] =  0.975 # https://hypernews.cern.ch/HyperNews/CMS/get/AUX/2018/07/05/17:57:09-21650-janek_bechtel_emb_2018_07_05.pdf
		# 		self["TauTrackReconstructionEfficiencyWeightOneProngPiZeros"] = 0.975*1.051
		# 		self["TauTrackReconstructionEfficiencyWeightThreeProng"] = 0.975*0.975*0.975
		# 		self["TauTrackReconstructionEfficiencyWeightThreeProngPiZeros"] = 0.975*0.975*0.975*1.051

		if re.search("(DY.?JetsToLL|EWKZ2Jets|LFV).*(?=(Spring16|Summer16))", nickname):
			self["TauElectronFakeEnergyCorrectionOneProng"] = 1.0
			self["TauElectronFakeEnergyCorrectionOneProngPiZeros"] = 1.095
			self["TauElectronFakeEnergyCorrectionThreeProng"] = 1.0
			self["TauMuonFakeEnergyCorrectionOneProng"] = 0.998
			self["TauMuonFakeEnergyCorrectionOneProngPiZeros"] = 1.015
			self["TauMuonFakeEnergyCorrectionThreeProng"] = 1.0

		if re.search("(Fall15MiniAODv2)", nickname):
			self["SimpleMuTauFakeRateWeightLoose"] = [1.0, 1.0, 1.0, 1.0, 1.0]
			self["SimpleMuTauFakeRateWeightTight"] = [1.0, 1.0, 1.0, 1.0, 1.0]
			self["SimpleEleTauFakeRateWeightVLoose"] = [1.02, 1.11]
			self["SimpleEleTauFakeRateWeightTight"] = [1.80, 1.30]

		elif re.search("(Spring16|Summer16)", nickname):
			self["SimpleMuTauFakeRateWeightLoose"]	= [1.22, 1.12, 1.26, 1.22, 2.39]
			self["SimpleMuTauFakeRateWeightTight"] = [1.47, 1.55, 1.33, 1.72, 2.50]
			self["SimpleEleTauFakeRateWeightVLoose"] = [1.213, 1.375]
			self["SimpleEleTauFakeRateWeightTight"] = [1.402, 1.90]

		# https://indico.cern.ch/event/738043/contributions/3048471/attachments/1674773/2688351/TauId_26062018.pdf
		elif re.search("(Summer17|Fall17)", nickname):
			self["SimpleMuTauFakeRateWeightLoose"]	= [1.06, 1.02, 1.10, 1.03, 1.94]
			self["SimpleMuTauFakeRateWeightTight"] = [1.17, 1.29, 1.14, 0.93, 1.61]
			self["SimpleEleTauFakeRateWeightVLoose"] = [1.09, 1.19]
			self["SimpleEleTauFakeRateWeightTight"] = [1.80, 1.53] #also available are other wp
