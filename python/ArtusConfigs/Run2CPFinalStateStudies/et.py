# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import re
import copy
import os

from HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Run2CPFinalStateStudies.quantities import Quantities

# Use et CP Initial State config as baseline
import HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Run2CPStudies.et as etbaseconfig

import HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Run2Analysis.Includes.settingsElectronID as sEID
import HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Run2Analysis.Includes.settingsMuonID as sMID
import HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Run2Analysis.Includes.settingsTauID as sTID
import HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Run2Analysis.Includes.settingsJetID as sJID
import HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Run2Analysis.Includes.settingsBTaggedJetID as sBTJID
import HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Run2Analysis.Includes.settingsSvfit as sSvfit
import HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Run2Analysis.Includes.settingsMinimalPlotlevelFilter as sMPlF
import HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Run2Analysis.Includes.settingsTauES as sTES
import HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Run2Analysis.Includes.settingsJEC as sJEC
import HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Run2Analysis.Includes.settingsJECUncertaintySplit as sJECUS

import HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Includes.settingsMVATestMethods as sMVATM
import HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Run2CPStudies.Includes.settingsTauPolarisationMva as sTPMVA

from HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Run2Analysis.Includes.idAndTriggerSF import IdAndTriggerSF
import Kappa.Skimming.datasetsHelperTwopz as datasetsHelperTwopz


class et_ArtusConfig(etbaseconfig.et_ArtusConfig):

	def __init__(self):
		pass

	def addProcessors(self, nickname, legacy):
		super(et_ArtusConfig, self).addProcessors(nickname, legacy)
		if re.search("Run201(6|7|8)|Summer1(6|7)|Fall17|Autumn18|Embedding201(6|7|8)", nickname):
		# if re.search("Run2017|Summer17|Fall17|Embedding2017", nickname):
			self["Processors"] += ["producer:IsomorphicMappingProducer"]
			self["Processors"] += ["producer:QuantileMappingProducer"]

	def build_config(self, nickname, *args, **kwargs):

		super(et_ArtusConfig, self).build_config(nickname, *args, **kwargs)
		isLegacy = kwargs.get("legacy", False)

		if False: # FIXME: remove when "if isLegacy" is uncommented
			print "Dummy to be removed"
		# if isLegacy:
		# 	# use MT IC FakeFactor here as ET does not exist yet
		# 	self["FakeFaktorFile"] = ""
		# 	self["FakeFactorRooWorkspaceFunction"] = [
		# 		"ff_mt_medium_dmbins:pt,dm,njets,m_pt,os,met,mt,m_iso,pass_single,mvis",
		# 		"ff_mt_medium_mvadmbins:pt,mvadm,ipsig,njets,m_pt,os,met,mt,m_iso,pass_single,mvis",
		# 		"ff_mt_medium_mvadmbins_nosig:pt,mvadm,njets,m_pt,os,met,mt,m_iso,pass_single,mvis",
		# 		"ff_mt_tight_dmbins:pt,dm,njets,m_pt,os,met,mt,m_iso,pass_single,mvis",
		# 		"ff_mt_tight_mvadmbins:pt,mvadm,ipsig,njets,m_pt,os,met,mt,m_iso,pass_single,mvis",
		# 		"ff_mt_tight_mvadmbins_nosig:pt,mvadm,njets,m_pt,os,met,mt,m_iso,pass_single,mvis",
		# 		"ff_mt_vtight_dmbins:pt,dm,njets,m_pt,os,met,mt,m_iso,pass_single,mvis",
		# 		"ff_mt_vtight_mvadmbins:pt,mvadm,ipsig,njets,m_pt,os,met,mt,m_iso,pass_single,mvis",
		# 		"ff_mt_vtight_mvadmbins_nosig:pt,mvadm,njets,m_pt,os,met,mt,m_iso,pass_single,mvis",
		# 	]
		# 	if re.search("Run2016|Summer16|Embedding2016", nickname):
		# 		self["FakeFactorFractionsRooWorkspaceFile"] = "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/azotz/higgs-IC/ff/fakefactors_ws_2016.root"
		# 	elif re.search("Run2017|Summer17|Fall17|Embedding2017", nickname):
		# 		self["FakeFactorFractionsRooWorkspaceFile"] = "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/azotz/higgs-IC/ff/fakefactors_ws_2017.root"
		# 	elif re.search("Run2018|Autumn18|Embedding2018", nickname):
		# 		self["FakeFactorFractionsRooWorkspaceFile"] = "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/azotz/higgs-IC/ff/fakefactors_ws_2018.root"
		else:
			self["FakeFactorMethod"] = "cpfinalstate2017"
			self["FakeFactorFractionsRooWorkspaceFile"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/fakeFactorWeights/rooworkspacefractions/FF_fractions_workspace_m_vis_njets.root"
			self["FakeFactorRooWorkspaceFunction"] = [
				"w_fracs:w_fracs_et",
				"qcd_fracs:qcd_fracs_et",
				"ttbar_fracs:ttbar_fracs_et",
				"dy_fracs:real_taus_fracs_et",
			]
			if re.search("Run2016|Summer16|Embedding2016", nickname):
				self["FakeFaktorFile"] = "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/azotz/higgs-kit/ff/2017/et/fakeFactors.root" #FIXME if needed and add FF for 2016
			elif re.search("Run2017|Summer17|Fall17|Embedding2017", nickname):
				self["FakeFaktorFile"] = "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/azotz/higgs-kit/ff/2017/et/fakeFactors.root"
			        #self["FakeFaktorFile"] = "root://se.cis.gov.pl:1094//store/user/bluj/higgs-kit/FF/2017/et/fakeFactors.root"
			elif re.search("Run2018|Autumn18|Embedding2018", nickname):
				self["FakeFaktorFile"] = "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/azotz/higgs-kit/ff/2017/et/fakeFactors.root" #FIXME if needed and add FF for 2018

		self["TauUpperAbsEtaCuts"] = ["2.3"] # tau trigger SFs only allow abs(eta) up to 2.1

		quantities_set = Quantities()
		quantities_set.build_quantities(nickname, channel = self["Channel"], legacy=isLegacy)
		quantities_set.quantities.update(self["Quantities"])
		self["Quantities"] = list(quantities_set.quantities)

		self.addProcessors(nickname, isLegacy)
