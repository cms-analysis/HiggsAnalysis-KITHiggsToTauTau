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
		else:
			self["TauEnergyCorrection"] = "none"

		if re.search("(Summer17|Fall17|Embedding2017)",nickname):
			if re.search("(Summer17|Fall17)",nickname):
				# self["TauIDEfficiencyWeightTight"] = 0.89 # +-3%
				# self["TauIDEfficiencyWeightVLoose"] = 0.88 # +-3%
				self["TauTrackReconstructionEfficiencyWeightOneProng"] = 1.0
				self["TauTrackReconstructionEfficiencyWeightOneProngPiZeros"] = 1.0
				self["TauTrackReconstructionEfficiencyWeightThreeProng"] = 1.0
				self["TauTrackReconstructionEfficiencyWeightThreeProngPiZeros"] = 1.0
			if re.search("(Embedding2017)",nickname):
				# if legacy:
				# 	self["TauIDEfficiencyWeightTight"] = 0.99
				# else:
				# 	self["TauIDEfficiencyWeightTight"] = 0.97
				self["TauTrackReconstructionEfficiencyWeightOneProng"] =  0.975 # https://hypernews.cern.ch/HyperNews/CMS/get/AUX/2018/07/05/17:57:09-21650-janek_bechtel_emb_2018_07_05.pdf
				self["TauTrackReconstructionEfficiencyWeightOneProngPiZeros"] = 0.975*1.051
				self["TauTrackReconstructionEfficiencyWeightThreeProng"] = 0.975*0.975*0.975
				self["TauTrackReconstructionEfficiencyWeightThreeProngPiZeros"] = 0.975*0.975*0.975*1.051



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
