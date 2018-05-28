#-*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import re


class TauSpinner(dict):
	def __init__(self, nickname):
		self["TauSpinnerSettingsPDF"] = "MSTW2008nnlo90cl.LHgrid"
		if re.search("(7TeV)", nickname):
			self["TauSpinnerSettingsCmsEnergy"] = 7000.0
		elif re.search("(8TeV)", nickname):
			self["TauSpinnerSettingsCmsEnergy"] = 8000.0
		elif re.search("(13TeV)", nickname):
			self["TauSpinnerSettingsCmsEnergy"] = 13000.0
		elif re.search("(14TeV)", nickname):
			self["TauSpinnerSettingsCmsEnergy"] = 14000.0

		self["TauSpinnerSettingsIpp"] = True
		
		self["TauSpinnerSettingsIpol_documentation"] = {
			"0/1" : "Applying longitudinal spin effects, https://arxiv.org/pdf/1402.2068v1.pdf (section 5.4)",
			"2" : "Working on the input file with spin correlations but without polarization",
			"3" : "Replacing spin effects of Z/gammaStar with the Higgs-like spin-0 state spin correlations",
			"4" : "Validation"
		}
		if re.search("(DY.?JetsToLL)", nickname):
			self["TauSpinnerSettingsIpol"] = "2"
		else:
			self["TauSpinnerSettingsIpol"] = "1"
		
		self["TauSpinnerSettingsNonSM2_documentation"] = {
			"0" : "SM calculations (spin = 0)",
			"1" : "non SM calculations (spin = 2): http://tauolapp.web.cern.ch/tauolapp/tau__reweight__lib_8cxx_source.html (line 558)"
		},
		self["TauSpinnerSettingsNonSM2"] = "0"
		
		self["TauSpinnerSettingsNonSMN"] = "0"
		if re.search("(HToTauTau|H2JetsToTauTau|Higgs)", nickname):
			self["TauSpinnerMixingAnglesOverPiHalf"] = [
				0.00,
				0.05,
				0.10,
				0.15,
				0.20,
				0.25,
				0.30,
				0.35,
				0.40,
				0.45,
				0.50,
				0.55,
				0.60,
				0.65,
				0.70,
				0.75,
				0.80,
				0.85,
				0.90,
				0.95,
				1.00
			]
		else:
			self["TauSpinnerMixingAnglesOverPiHalf"] = []

		if re.search("SM_(WH_ZH_TTH_|VBF|GluGlu|GluGluTo)HToTauTau", nickname):
			self["TauSpinnerMixingAnglesOverPiHalfSample"] = 0.0
		elif re.search("^(W(minus|plus)|Z|VBF|GluGlu|GluGluTo)HToTauTau", nickname):
			self["TauSpinnerMixingAnglesOverPiHalfSample"] = 0.0
		elif re.search("SUSY(BB|GluGlu|GluGluTo)HToTauTau", nickname):
			self["TauSpinnerMixingAnglesOverPiHalfSample"] = 1.0
		else:
			self["TauSpinnerMixingAnglesOverPiHalfSample"] = -1.0

