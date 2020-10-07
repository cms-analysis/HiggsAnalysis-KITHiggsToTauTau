# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import re
import copy
import os

from HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Run2LFVStudies.quantities import Quantities

# Use mt CP Initial State config as baseline
import HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Run2LFVStudies.mt as mtbaseconfig

import Kappa.Skimming.datasetsHelperTwopz as datasetsHelperTwopz


class mt_ArtusConfig(mtbaseconfig.mt_ArtusConfig):

	def __init__(self):
		pass

	def addProcessors(self, nickname, legacy):
		super(mt_ArtusConfig, self).addProcessors(nickname, legacy)
		if re.search("Run201(6|7|8)|Summer1(6|7)|Fall17|Autumn18|Embedding201(6|7|8)", nickname):
		# if re.search("Run2017|Summer17|Fall17|Embedding2017", nickname):
			self["Processors"] += ["producer:IsomorphicMappingProducer"]
			self["Processors"] += ["producer:QuantileMappingProducer"]


	def build_config(self, nickname, *args, **kwargs):

		super(mt_ArtusConfig, self).build_config(nickname, *args, **kwargs)

		isLegacy = kwargs.get("legacy", False)

		if isLegacy:
			self["FakeFaktorFile"] = ""
			self["FakeFactorRooWorkspaceFunction"] = [
				"ff_mt_medium_dmbins:pt,dm,njets,m_pt,os,mt,m_iso,pass_single,met_var_qcd,met_var_w,WpT",
				"ff_mt_medium_mvadmbins:pt,mvadm,ipsig,njets,m_pt,os,mt,m_iso,pass_single,met_var_qcd,met_var_w,WpT",
				"ff_mt_medium_mvadmbins_nosig:pt,mvadm,njets,m_pt,os,mt,m_iso,pass_single,met_var_qcd,met_var_w,WpT",
				# "ff_mt_tight_dmbins:pt,dm,njets,m_pt,os,mt,m_iso,pass_single,met_var_qcd,met_var_w,WpT",
				# "ff_mt_tight_mvadmbins:pt,mvadm,ipsig,njets,m_pt,os,mt,m_iso,pass_single,met_var_qcd,met_var_w,WpT",
				# "ff_mt_tight_mvadmbins_nosig:pt,mvadm,njets,m_pt,os,mt,m_iso,pass_single,met_var_qcd,met_var_w,WpT",
				# "ff_mt_vtight_dmbins:pt,dm,njets,m_pt,os,mt,m_iso,pass_single,met_var_qcd,met_var_w,WpT",
				# "ff_mt_vtight_mvadmbins:pt,mvadm,ipsig,njets,m_pt,os,mt,m_iso,pass_single,met_var_qcd,met_var_w,WpT",
				# "ff_mt_vtight_mvadmbins_nosig:pt,mvadm,njets,m_pt,os,mt,m_iso,pass_single,met_var_qcd,met_var_w,WpT",
			]
			if re.search("Run2016|Summer16|Embedding2016", nickname):
				self["FakeFactorFractionsRooWorkspaceFile"] = "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/azotz/higgs-IC/ff/fake_factors_cpdecay_ipsig1p5_v3/fakefactors_ws_mt_lite_2016.root"
			elif re.search("Run2017|Summer17|Fall17|Embedding2017", nickname):
				self["FakeFactorFractionsRooWorkspaceFile"] = "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/azotz/higgs-IC/ff/fake_factors_cpdecay_ipsig1p5_v3/fakefactors_ws_mt_lite_2017.root"
			elif re.search("Run2018|Autumn18|Embedding2018", nickname):
				self["FakeFactorFractionsRooWorkspaceFile"] = "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/azotz/higgs-IC/ff/fake_factors_cpdecay_ipsig1p5_v3/fakefactors_ws_mt_lite_2018.root"
		else:
				self["FakeFactorMethod"] = "cpfinalstate2017"
				self["FakeFactorFractionsRooWorkspaceFile"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/fakeFactorWeights/rooworkspacefractions/FF_fractions_workspace_m_vis_njets.root"
				self["FakeFactorRooWorkspaceFunction"] = [
					"w_fracs:w_fracs_mt",
					"qcd_fracs:qcd_fracs_mt",
					"ttbar_fracs:ttbar_fracs_mt",
					"dy_fracs:real_taus_fracs_mt",
				]
				if re.search("Run2016|Summer16|Embedding2016", nickname):
					self["FakeFaktorFile"] = "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/azotz/higgs-kit/ff/2016/mt/fakeFactors.root"
				elif re.search("Run2017|Summer17|Fall17|Embedding2017", nickname):
					self["FakeFaktorFile"] = "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/azotz/higgs-kit/ff/2017/mt/fakeFactors.root"
					#self["FakeFaktorFile"] = "root://se.cis.gov.pl:1094//store/user/bluj/higgs-kit/FF/2017/mt/fakeFactors.root"
				elif re.search("Run2018|Autumn18|Embedding2018", nickname):
					self["FakeFaktorFile"] = "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/azotz/higgs-kit/ff/2018/mt/fakeFactors.root"

		quantities_set = Quantities()
		quantities_set.build_quantities(nickname, channel = self["Channel"], legacy=isLegacy)
		quantities_set.quantities.update(self["Quantities"])
		self["Quantities"] = list(quantities_set.quantities)

		self.addProcessors(nickname, isLegacy)
