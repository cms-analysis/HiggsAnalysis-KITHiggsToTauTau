# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import re


class Muon_ID(dict):
	def __init__(self, nickname):

		self["MuonID_documentation"] = ["https://twiki.cern.ch/twiki/bin/view/CMS/HiggsToTauTauWorking2015#Muons"]
		if re.search("(Spring16|Summer16|Run2016|Embedding2016)", nickname):
			self["Year"] = 2016
			self["MuonIsoTypeUserMode"] = "fromcmsswr04"
		if re.search("Run2017|Summer17|Fall17", nickname):
			self["Year"] = 2016
			self["MuonIsoTypeUserMode"] = "fromcmsswr04" #took the same as for 2016, needs update https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsToTauTauWorking2017#Muons
		else:
			self["Year"] = 2015
			self["MuonIsoTypeUserMode"] = "fromcmssw"

		if re.search("Run2016(B|C|D|E|F)",nickname):
			self["MuonID"] = "mediumHIPsafe2016"

		else:
			self["MuonID"] = "medium"
		
		self["MuonIsoType"] = "user"
		self["MuonIso"] = "none"
		if re.search("Run2017|Summer17|Fall17", nickname):
			self["MuonIsoSignalConeSize"] = 0.4

		self["MuonIsoSignalConeSize"] = 0.3
		self["MuonDeltaBetaCorrectionFactor"] = 0.5
	
		self["MuonTrackDxyCut"] = 0.045
		self["MuonTrackDzCut"] = 0.2

	def looseMuon_ID(self, nickname):

		if re.search("Run2016(B|C|D|E|F)",nickname):
			self["LooseMuonID"] = "mediumHIPsafe2016"

		else:
			self["LooseMuonID"] = "medium"

		self["LooseMuonIsoType"] = "user"
		self["LooseMuonIso"] = "none"

		self["LooseMuonIsoPtSumOverPtUpperThresholdEB"] = 0.3
		self["LooseMuonIsoPtSumOverPtUpperThresholdEE"] = 0.3

		self["LooseMuonLowerPtCuts"] = ["10.0"]
		self["LooseMuonUpperAbsEtaCuts"] = ["2.4"]

		self["LooseMuonTrackDxyCut"] = 0.045
		self["LooseMuonTrackDzCut"] = 0.2
		self["DirectIso"] = True

	def vetoMuon_ID(self, nickname):
		
		self["VetoMuonID"] = "veto"

		self["VetoMuonIsoType"] = "user"
		self["VetoMuonIso"] = "none"

		self["VetoMuonIsoPtSumOverPtUpperThresholdEB"] = 0.3
		self["VetoMuonIsoPtSumOverPtUpperThresholdEE"] = 0.3

		self["VetoMuonLowerPtCuts"] = ["15.0"]
		self["VetoMuonUpperAbsEtaCuts"] = ["2.4"]
		self["DiVetoMuonMinDeltaRCut"] = 0.15
		self["DiVetoMuonVetoMode"] = "veto_os_keep_ss"
		self["DirectIso"] = True

