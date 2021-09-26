# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import re
import copy
import os

from HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Run2CPFinalStateStudies.quantities import Quantities

# Use tt CP Initial State config as baseline
import HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Run2CPStudies.tt as ttbaseconfig

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


class tt_ArtusConfig(ttbaseconfig.tt_ArtusConfig):

	def __init__(self):
		pass

	def addProcessors(self, nickname, legacy):
		super(tt_ArtusConfig, self).addProcessors(nickname, legacy)
		if re.search("Run201(6|7|8)|Summer1(6|7)|Fall17|Autumn18|Embedding201(6|7|8)", nickname):
		# if re.search("Run2017|Summer17|Fall17|Embedding2017", nickname):
			self["Processors"] += ["producer:IsomorphicMappingProducer"]
			self["Processors"] += ["producer:QuantileMappingProducer"]

	def build_config(self, nickname, *args, **kwargs):

		super(tt_ArtusConfig, self).build_config(nickname, *args, **kwargs)
		isLegacy = kwargs.get("legacy", False)

		if isLegacy:
			self["FakeFaktorFile"] = ""
			self["FakeFactorRooWorkspaceFunction"] = [
				"ff_tt_medium_dmbins:pt,dm,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_nosig:pt,mvadm,njets,os,met_var_qcd,dR",
				# "ff_tt_tight_dmbins:pt,dm,njets,os,met_var_qcd,dR",
				# "ff_tt_tight_mvadmbins:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				# "ff_tt_tight_mvadmbins_nosig:pt,mvadm,njets,os,met_var_qcd,dR",
				# "ff_tt_vtight_dmbins:pt,dm,njets,os,met_var_qcd,dR",
				# "ff_tt_vtight_mvadmbins:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				# "ff_tt_vtight_mvadmbins_nosig:pt,mvadm,njets,os,met_var_qcd,dR",


				# fake factor systematics
				"ff_tt_medium_mvadmbins_qcd_stat_unc1_njet0_mvadm0_down:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc1_njet0_mvadm0_sig_gt3_down:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc1_njet0_mvadm0_sig_gt3_up:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc1_njet0_mvadm0_sig_lt3_down:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc1_njet0_mvadm0_sig_lt3_up:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc1_njet0_mvadm0_up:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc1_njet0_mvadm10_down:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc1_njet0_mvadm10_up:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc1_njet0_mvadm11_down:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc1_njet0_mvadm11_up:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc1_njet0_mvadm1_down:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc1_njet0_mvadm1_up:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc1_njet0_mvadm2_down:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc1_njet0_mvadm2_up:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc1_njet1_dm0_down:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc1_njet1_dm0_up:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc1_njet1_dm10_down:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc1_njet1_dm10_up:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc1_njet1_dm11_down:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc1_njet1_dm11_up:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc1_njet1_dm1_down:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc1_njet1_dm1_up:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc1_njet1_mvadm0_down:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc1_njet1_mvadm0_sig_gt3_down:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc1_njet1_mvadm0_sig_gt3_up:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc1_njet1_mvadm0_sig_lt3_down:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc1_njet1_mvadm0_sig_lt3_up:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc1_njet1_mvadm0_up:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc1_njet1_mvadm10_down:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc1_njet1_mvadm10_up:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc1_njet1_mvadm11_down:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc1_njet1_mvadm11_up:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc1_njet1_mvadm1_down:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc1_njet1_mvadm1_up:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc1_njet1_mvadm2_down:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc1_njet1_mvadm2_up:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc1_njet2_dm0_down:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc1_njet2_dm0_up:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc1_njet2_dm10_down:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc1_njet2_dm10_up:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc1_njet2_dm11_down:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc1_njet2_dm11_up:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc1_njet2_dm1_down:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc1_njet2_dm1_up:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc1_njet2_mvadm0_down:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc1_njet2_mvadm0_sig_gt3_down:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc1_njet2_mvadm0_sig_gt3_up:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc1_njet2_mvadm0_sig_lt3_down:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc1_njet2_mvadm0_sig_lt3_up:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc1_njet2_mvadm0_up:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc1_njet2_mvadm10_down:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc1_njet2_mvadm10_up:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc1_njet2_mvadm11_down:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc1_njet2_mvadm11_up:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc1_njet2_mvadm1_down:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc1_njet2_mvadm1_up:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc1_njet2_mvadm2_down:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc1_njet2_mvadm2_up:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc2_njet0_dm0_down:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc2_njet0_dm0_up:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc2_njet0_dm10_down:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc2_njet0_dm10_up:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc2_njet0_dm11_down:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc2_njet0_dm11_up:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc2_njet0_dm1_down:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc2_njet0_dm1_up:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc2_njet0_mvadm0_down:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc2_njet0_mvadm0_sig_gt3_down:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc2_njet0_mvadm0_sig_gt3_up:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc2_njet0_mvadm0_sig_lt3_down:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc2_njet0_mvadm0_sig_lt3_up:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc2_njet0_mvadm0_up:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc2_njet0_mvadm10_down:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc2_njet0_mvadm10_up:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc2_njet0_mvadm11_down:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc2_njet0_mvadm11_up:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc2_njet0_mvadm1_down:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc2_njet0_mvadm1_up:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc2_njet0_mvadm2_down:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc2_njet0_mvadm2_up:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc2_njet1_dm0_down:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc2_njet1_dm0_up:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc2_njet1_dm10_down:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc2_njet1_dm10_up:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc2_njet1_dm11_down:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc2_njet1_dm11_up:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc2_njet1_dm1_down:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc2_njet1_dm1_up:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc2_njet1_mvadm0_down:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc2_njet1_mvadm0_sig_gt3_down:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc2_njet1_mvadm0_sig_gt3_up:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc2_njet1_mvadm0_sig_lt3_down:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc2_njet1_mvadm0_sig_lt3_up:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc2_njet1_mvadm0_up:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc2_njet1_mvadm10_down:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc2_njet1_mvadm10_up:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc2_njet1_mvadm11_down:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc2_njet1_mvadm11_up:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc2_njet1_mvadm1_down:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc2_njet1_mvadm1_up:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc2_njet1_mvadm2_down:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc2_njet1_mvadm2_up:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc2_njet2_dm0_down:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc2_njet2_dm0_up:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc2_njet2_dm10_down:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc2_njet2_dm10_up:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc2_njet2_dm11_down:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc2_njet2_dm11_up:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc2_njet2_dm1_down:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc2_njet2_dm1_up:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc2_njet2_mvadm0_down:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc2_njet2_mvadm0_sig_gt3_down:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc2_njet2_mvadm0_sig_gt3_up:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc2_njet2_mvadm0_sig_lt3_down:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc2_njet2_mvadm0_sig_lt3_up:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc2_njet2_mvadm0_up:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc2_njet2_mvadm10_down:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc2_njet2_mvadm10_up:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc2_njet2_mvadm11_down:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc2_njet2_mvadm11_up:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc2_njet2_mvadm1_down:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc2_njet2_mvadm1_up:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc2_njet2_mvadm2_down:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_stat_unc2_njet2_mvadm2_up:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",

				"ff_tt_medium_mvadmbins_qcd_met_down:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_met_up:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",

				"ff_tt_medium_mvadmbins_qcd_syst_down:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
				"ff_tt_medium_mvadmbins_qcd_syst_up:pt,mvadm,ipsig,njets,os,met_var_qcd,dR",
			]

			if re.search("Run2016|Summer16|Embedding2016", nickname):
				self["FakeFactorFractionsRooWorkspaceFile"] = "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/azotz/higgs-IC/ff/fake_factors_tt_dRcorr/fakefactors_ws_tt_lite_2016_dR_corr.root"
			elif re.search("Run2017|Summer17|Fall17|Embedding2017", nickname):
				self["FakeFactorFractionsRooWorkspaceFile"] = "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/azotz/higgs-IC/ff/fake_factors_tt_dRcorr/fakefactors_ws_tt_lite_2017_dR_corr.root"
			elif re.search("Run2018|Autumn18|Embedding2018", nickname):
				self["FakeFactorFractionsRooWorkspaceFile"] = "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/azotz/higgs-IC/ff/fake_factors_tt_dRcorr/fakefactors_ws_tt_lite_2018_dR_corr.root"
		else:
			self["FakeFactorMethod"] = "cpfinalstate2017"
			self["FakeFactorFractionsRooWorkspaceFile"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/fakeFactorWeights/rooworkspacefractions/FF_fractions_workspace_m_vis_njets.root"
			self["FakeFactorRooWorkspaceFunction"] = [
				"w_fracs_1:w_fracs_tt1",
				"qcd_fracs_1:qcd_fracs_tt1",
				"ttbar_fracs_1:ttbar_fracs_tt1",
				"dy_fracs_1:real_taus_fracs_tt1",
				"w_fracs_2:w_fracs_tt2",
				"qcd_fracs_2:qcd_fracs_tt2",
				"ttbar_fracs_2:ttbar_fracs_tt2",
				"dy_fracs_2:real_taus_fracs_tt2"
			]
			if re.search("Run2016|Summer16|Embedding2016", nickname):
				self["FakeFaktorFile"] = "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/azotz/higgs-kit/ff/2017/tt/fakeFactors.root" #FIXME if needed and add FF for 2016
			elif re.search("Run2017|Summer17|Fall17|Embedding2017", nickname):
				self["FakeFaktorFile"] = "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/azotz/higgs-kit/ff/2017/tt/fakeFactors.root"
			        #self["FakeFaktorFile"] = "root://se.cis.gov.pl:1094//store/user/bluj/higgs-kit/FF/2017/tt/fakeFactors.root"
			elif re.search("Run2018|Autumn18|Embedding2018", nickname):
				self["FakeFaktorFile"] = "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/azotz/higgs-kit/ff/2017/tt/fakeFactors.root" #FIXME if needed and add FF for 2018

		quantities_set = Quantities()
		quantities_set.build_quantities(nickname, channel = self["Channel"], legacy=isLegacy)
		quantities_set.quantities.update(self["Quantities"])
		self["Quantities"] = list(quantities_set.quantities)

		self.addProcessors(nickname, isLegacy)
