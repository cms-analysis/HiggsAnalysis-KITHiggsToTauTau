# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import re


class TauES(dict):
	def __init__(self, nickname):
	#HttTauCorrectionsProducer.cc in kithiggs
	#tau.p4*shiftvalue     shiftvalue = 1. means no shift
		if re.search("(Spring16|Summer16)",nickname):
			self["TauEnergyCorrection"] = "smhtt2016"
			self["TauEnergyCorrectionOneProng"] = 0.982
			self["TauEnergyCorrectionOneProngPiZeros"] = 1.01
			self["TauEnergyCorrectionThreeProng"] = 1.004
		elif re.search("(Summer17|Fall17)",nickname):
			#https://indico.cern.ch/event/738043/contributions/3048471/attachments/1674773/2688351/TauId_26062018.pdf old
			#newest look at tautwiki
			self["TauEnergyCorrection"] = "smhtt2017"
			self["TauEnergyCorrectionOneProng"] = 1.007 #+-0.8%  
			self["TauEnergyCorrectionOneProngPiZeros"] = 0.998 #+-0.8%
			self["TauEnergyCorrectionThreeProng"] = 1.001 #+-0.9%
			self["TauEnergyCorrectionThreeProngPizeros"] = 0.999 #+-1%
			if re.search("(DY.?JetsToLL|EWKZ2Jets)", nickname):
				self["TauElectronFakeEnergyCorrectionOneProng"] = 1.01  #+-1.4%
				self["TauElectronFakeEnergyCorrectionOneProngPiZeros"] = 1.041 #+-1.8%
				self["TauElectronFakeEnergyCorrectionThreeProng"] = 1.0
				self["TauMuonFakeEnergyCorrectionOneProng"] = 0.999 #+-3%
				self["TauMuonFakeEnergyCorrectionOneProngPiZeros"] = 1.012 #+-0.3%
				self["TauMuonFakeEnergyCorrectionThreeProng"] = 1.0

		else:
			self["TauEnergyCorrection"] = "none"

		self["TauEnergyCorrectionOneProng"] = 0.995
		self["TauEnergyCorrectionOneProngPiZeros"] = 1.011
		self["TauEnergyCorrectionThreeProng"] = 1.006

		if re.search("(DY.?JetsToLL|EWKZ2Jets|LFV).*(?=(Spring16|Summer16))", nickname):
			self["TauElectronFakeEnergyCorrectionOneProng"] = 1.0
			self["TauElectronFakeEnergyCorrectionOneProngPiZeros"] = 1.095
			self["TauElectronFakeEnergyCorrectionThreeProng"] = 1.0
			self["TauMuonFakeEnergyCorrectionOneProng"] = 0.998
			self["TauMuonFakeEnergyCorrectionOneProngPiZeros"] = 1.015
			self["TauMuonFakeEnergyCorrectionThreeProng"] = 1.0

