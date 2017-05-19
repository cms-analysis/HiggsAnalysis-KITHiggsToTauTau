# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import copy
import glob
import os
import re
import shutil

import ROOT

# http://cms-analysis.github.io/CombineHarvester/python-interface.html
import CombineHarvester.CombineTools.ch as ch
import CombineHarvester.CombinePdfs.morphing as morphing

import Artus.Utility.tools as tools
import Artus.Utility.jsonTools as jsonTools
import Artus.HarryPlotter.utility.roottools as roottools
import Artus.Utility.tfilecontextmanager as tfilecontextmanager

import HiggsAnalysis.KITHiggsToTauTau.datacards.datacardconfigs as datacardconfigs
import HiggsAnalysis.KITHiggsToTauTau.plotting.higgsplot as higgsplot


def _call_command(args):
	command = None
	cwd = None
	if isinstance(args, basestring):
		command = args
	else:
		command = args[0]
		if len(args) > 1:
			cwd = args[1]

	old_cwd = None
	if not cwd is None:
		old_cwd = os.getcwd()
		os.chdir(cwd)

	log.debug(command)
	logger.subprocessCall(command, shell=True)

	if not cwd is None:
		os.chdir(old_cwd)


class Datacards(object):
	def __init__(self, cb=None):
		super(Datacards, self).__init__()

		self.cb = cb
		if self.cb is None:
			self.cb = ch.CombineHarvester()
		if log.isEnabledFor(logging.DEBUG):
			self.cb.SetVerbosity(1)

		self.configs = datacardconfigs.DatacardConfigs()
		
		self.stable_options = r"--robustFit 1 --preFitValue 1.0 --minimizerAlgoForMinos Minuit2 --minimizerAlgo Minuit2 --minimizerStrategy 0 --minimizerTolerance 0.1 --cminFallbackAlgo Minuit2,0:1.0"

		# common systematics
		self.lumi_syst_args = [
			"lumi_$ERA",
			"lnN",
			ch.SystMap("era")
				(["7TeV", "8TeV"], 1.026)
				(       ["13TeV"], 1.027) # CMS-PAS-LUM-15-001
		]
		self.lumi2016_syst_args = [
			"lumi_$ERA",
			"lnN",
			ch.SystMap("era")
				(       ["13TeV"], 1.025)
		]
		self.trigger_efficiency2016_syst_args = [ # https://github.com/cms-analysis/CombineHarvester/blob/SM2016-dev/HTTSM2016/src/HttSystematics_SMRun2.cc#L76-L88
			"CMS_eff_trigger_$CHANNEL_$ERA",
			"lnN",
			ch.SystMap("era", "channel")
				(["13TeV"], ["mt", "et"], 1.02)
				(["13TeV"], ["tt"], 1.10)
		]
		self.trigger_efficiency2016_em_syst_args = [ # https://github.com/cms-analysis/CombineHarvester/blob/SM2016-dev/HTTSM2016/src/HttSystematics_SMRun2.cc#L82-L84
			"CMS_eff_trigger_em_$ERA",
			"lnN",
			ch.SystMap("era", "channel")
				(["13TeV"], ["em", "ttbar"], 1.02)
		]
		self.electron_efficiency_syst_args = [
			"CMS_eff_e",
			"lnN",
			ch.SystMap("era")
				(["7TeV", "8TeV"], 1.02)
				(       ["13TeV"], 1.04) # https://github.com/cms-analysis/CombineHarvester/blob/HIG15007/HIG15007/scripts/setupDatacards.py#L107-L110
		]
		self.electron_efficiency2016_syst_args = [
			"CMS_eff_e",
			"lnN",
			ch.SystMap("era")
				(       ["13TeV"], 1.02) # https://indico.cern.ch/event/566822/contributions/2377598/attachments/1374111/2085739/systematics.pdf
		]
		self.muon_efficiency_syst_args = [
			"CMS_eff_m",
			"lnN",
			ch.SystMap("era")
				(["7TeV", "8TeV"], 1.02)
				(       ["13TeV"], 1.03) # https://github.com/cms-analysis/CombineHarvester/blob/HIG15007/HIG15007/scripts/setupDatacards.py#L101-L105
		]
		self.muon_efficiency2016_syst_args = [
			"CMS_eff_m",
			"lnN",
			ch.SystMap("era")
				(       ["13TeV"], 1.02) # https://indico.cern.ch/event/566822/contributions/2377598/attachments/1374111/2085739/systematics.pdf
		]
		self.tau_efficiency_corr_syst_args = [
			"CMS_eff_t_$ERA",
			"lnN",
			ch.SystMap("era", "channel")
				(["7TeV", "8TeV"], ["mt", "et"], 1.08)
				(["7TeV", "8TeV"], ["tt"],       1.19)
				(       ["13TeV"], ["mt", "et", "tt"], 1.05) # CV https://indico.cern.ch/event/515350/contributions/1194776/attachments/1257261/1856581/HttNuisanceParamUpdate_2016Apr13.pdf
		]
		self.tau_efficiency_syst_args = [
			"CMS_eff_t_$CHANNEL_$ERA",
			"lnN",
			ch.SystMap("era", "channel")
				(["7TeV", "8TeV"], ["mt", "et"], 1.08)
				(["7TeV", "8TeV"], ["tt"],       1.19)
				(       ["13TeV"], ["mt", "et", "tt"], 1.03) # CV https://indico.cern.ch/event/515350/contributions/1194776/attachments/1257261/1856581/HttNuisanceParamUpdate_2016Apr13.pdf
		]
		self.tau_efficiency2016_corr_syst_args = [
			"CMS_eff_t_$ERA",
			"lnN",
			ch.SystMap("era", "channel")
				(       ["13TeV"], ["mt", "et"], 1.045) # https://github.com/cms-analysis/CombineHarvester/blob/SM2016-dev/HTTSM2016/src/HttSystematics_SMRun2.cc#L103-L128
		]
		self.tau_efficiency2016_tt_corr_syst_args = [
			"CMS_eff_t_$ERA",
			"lnN",
			ch.SystMap("era", "channel", "process")
				(       ["13TeV"], ["tt"], ["ZTT", "VVT", "TTT", "ggH", "qqH", "WH", "ZH"], 1.09) # https://github.com/cms-analysis/CombineHarvester/blob/SM2016-dev/HTTSM2016/src/HttSystematics_SMRun2.cc#L103-L128
				(       ["13TeV"], ["tt"], ["ZJ", "VVJ", "TTJJ", "W"], 1.06) # https://github.com/cms-analysis/CombineHarvester/blob/SM2016-dev/HTTSM2016/src/HttSystematics_SMRun2.cc#L103-L128
		]
		self.tau_efficiency2016_syst_args = [
			"CMS_eff_t_$CHANNEL_$ERA",
			"lnN",
			ch.SystMap("era", "channel")
				(       ["13TeV"], ["mt", "et"], 1.02) # https://github.com/cms-analysis/CombineHarvester/blob/SM2016-dev/HTTSM2016/src/HttSystematics_SMRun2.cc#L103-L128
		]
		self.tau_efficiency2016_tt_syst_args = [
			"CMS_eff_t_$CHANNEL_$ERA",
			"lnN",
			ch.SystMap("era", "channel", "process")
				(       ["13TeV"], ["tt"], ["ZTT", "VVT", "TTT", "ggH", "qqH", "WH", "ZH"], 1.04) # https://github.com/cms-analysis/CombineHarvester/blob/SM2016-dev/HTTSM2016/src/HttSystematics_SMRun2.cc#L103-L128
				(       ["13TeV"], ["tt"], ["ZJ", "VVJ", "TTJJ", "W"], 1.02) # https://github.com/cms-analysis/CombineHarvester/blob/SM2016-dev/HTTSM2016/src/HttSystematics_SMRun2.cc#L103-L128
		]
		self.btag_efficiency_syst_args = [
			"CMS_eff_b_$ERA",
			"shape",
			ch.SystMap("era", "channel")
				(["13TeV"], ["em","et","mt"], 1.0)
		]
		self.btag_efficiency2016_syst_args = [ # https://github.com/cms-analysis/CombineHarvester/blob/SM2016-dev/HTTSM2016/src/HttSystematics_SMRun2.cc#L151-L154
			"CMS_htt_eff_b_$ERA",
			"lnN",
			ch.SystMap("era", "bin", "process")
				(["13TeV"], ["TTJ", "TTJJ", "TTT", "TT"], ["em_ZeroJet2D"], 1.035)
				(["13TeV"], ["TTJ", "TTJJ", "TTT", "TT"], ["em_Boosted2D", "em_Vbf2D"], 1.05)
		]
		self.btag_mistag_syst_args = [
			"CMS_mistag_b_$ERA",
			"shape",
			ch.SystMap("era", "channel")
				(["13TeV"], ["em","et","mt"], 1.0)
		]
		self.btag_mistag2016_syst_args = [ # https://github.com/cms-analysis/CombineHarvester/blob/SM2016-dev/HTTSM2016/src/HttSystematics_SMRun2.cc#L156-L157
			"CMS_htt_mistag_b_$ERA",
			"lnN",
			ch.SystMap("era", "bin", "process")
				(["13TeV"], ["VVJ", "VVT", "VV"], ["em_Boosted2D", "em_Vbf2D"], 1.015)
		]
		self.met_scale_syst_args = [
			"CMS_$ANALYSIS_scale_met_$ERA",
			"lnN",
			ch.SystMap("era", "process")
				(["13TeV"], ["ggH", "qqH", "WH", "ZH", "VH"], 0.98) # copied from 8TeV
				(["13TeV"], ["ZTT", "ZLL", "ZL", "ZJ", "TTJ", "TTJJ", "TTT", "TT", "VV", "WJ", "W"], 1.03) # copied from 8TeV
		]
		self.ztt_cross_section_syst_args = [
			"CMS_$ANALYSIS_zttNorm_$ERA",
			"lnN",
			ch.SystMap("era", "process")
				(["7TeV", "8TeV"], ["ZTT", "ZLL", "ZL", "ZJ"], 1.03)
				(       ["13TeV"], ["ZTT", "ZLL", "ZL", "ZJ"], 1.04)
		]
		self.zll_cross_section_syst_args = [
			"CMS_$ANALYSIS_zjXsec_$ERA",
			"lnN",
			ch.SystMap("era", "process")
				(       ["13TeV"], ["ZLL", "ZL", "ZJ"], 1.04) # CV https://indico.cern.ch/event/515350/contributions/1194776/attachments/1257261/1856581/HttNuisanceParamUpdate_2016Apr13.pdf
		]
		self.ttj_cross_section_syst_args = [
			"CMS_$ANALYSIS_ttjXsec_$ERA",
			"lnN",
			ch.SystMap("era", "process")
				( ["7TeV"], ["TTJ"], 1.08)
				( ["8TeV"], ["TTJ"], 1.1)
				(["13TeV"], ["TTJ", "TT", "TTT", "TTJJ"], 1.06) # CV https://indico.cern.ch/event/515350/contributions/1194776/attachments/1257261/1856581/HttNuisanceParamUpdate_2016Apr13.pdf
		]
		self.ttj_extrapol_syst_args = [
			"CMS_$ANALYSIS_ttjExtrapol_$ERA",
			"lnN",
			ch.SystMap("era", "process")
				(["13TeV"], ["TTJ", "TT"], 1.10) # CV https://indico.cern.ch/event/515350/contributions/1194776/attachments/1257261/1856581/HttNuisanceParamUpdate_2016Apr13.pdf
		]
		self.singlet_cross_section_syst_args = [
			"CMS_$ANALYSIS_singletXsec_$ERA",
			"lnN",
			ch.SystMap("era", "process")
				(["13TeV"], ["VV"], 1.04) # CV https://indico.cern.ch/event/515350/contributions/1194776/attachments/1257261/1856581/HttNuisanceParamUpdate_2016Apr13.pdf
		]
		self.vv_cross_section_syst_args = [
			"CMS_$ANALYSIS_vvXsec_$ERA",
			"lnN",
			ch.SystMap("era", "process")
				(["7TeV", "8TeV"], ["VV"], 1.15)
				(       ["13TeV"], ["VV", "VVT", "VVJ"], 1.10) # https://indico.cern.ch/event/515350/contributions/1194776/attachments/1257261/1856581/HttNuisanceParamUpdate_2016Apr13.pdf
		]
		self.vv_cross_section2016_syst_args = [
			"CMS_$ANALYSIS_vvXsec_$ERA",
			"lnN",
			ch.SystMap("era", "process")
				(       ["13TeV"], ["VV", "VVT", "VVJ"], 1.05) # https://indico.cern.ch/event/566822/contributions/2377598/attachments/1374111/2085739/systematics.pdf
		]
		self.wj_cross_section_syst_args = [
			"CMS_$ANALYSIS_wjXsec_$ERA",
			"lnN",
			ch.SystMap("era", "process")
				(       ["13TeV"], ["WJ", "W"], 1.04) # CV https://indico.cern.ch/event/515350/contributions/1194776/attachments/1257261/1856581/HttNuisanceParamUpdate_2016Apr13.pdf
		]
		self.wj_extrapol_syst_args = [
			"CMS_$ANALYSIS_wjExtrapol_$ERA",
			"lnN",
			ch.SystMap("era", "process")
				(       ["13TeV"], ["WJ", "W"], 1.2) # CV https://indico.cern.ch/event/515350/contributions/1194776/attachments/1257261/1856581/HttNuisanceParamUpdate_2016Apr13.pdf
		]

		self.qcd_syst_args = [
			"CMS_$ANALYSIS_qcdSyst_$BIN_$ERA",
			"lnN",
			ch.SystMap("era", "process", "bin")
				(["13TeV"], ["QCD"], ["mt_inclusive", "et_inclusive"], 1.06) # copied from 8TeV

				(["13TeV"], ["QCD"], ["mt_0jet_high"], 1.1) # copied from 8TeV
				(["13TeV"], ["QCD"], ["mt_0jet_low"], 1.1) # copied from 8TeV
				(["13TeV"], ["QCD"], ["mt_1jet_high"], 1.1) # copied from 8TeV
				(["13TeV"], ["QCD"], ["mt_1jet_low"], 1.1) # copied from 8TeV
				(["13TeV"], ["QCD"], ["mt_2jet_vbf"], 1.3) # copied from 8TeV

				(["13TeV"], ["QCD"], ["et_0jet_high"], 1.06) # copied from 8TeV
				(["13TeV"], ["QCD"], ["et_0jet_low"], 1.06) # copied from 8TeV
				(["13TeV"], ["QCD"], ["et_1jet_high"], 1.1) # copied from 8TeV
				(["13TeV"], ["QCD"], ["et_1jet_low"], 1.1) # copied from 8TeV
				(["13TeV"], ["QCD"], ["et_2jet_vbf"], 1.3) # copied from 8TeV

				(["13TeV"], ["QCD"], ["tt_inclusive"], 1.35) # copied from 8TeV
		]
		self.qcd_syst_inclusive_args = [
			"CMS_$ANALYSIS_qcdSyst_$ERA",
			"lnN",
			ch.SystMap("era", "process")
				(["13TeV"], ["QCD"], 1.10)
		]
		self.zllFakeTau_syst_args = [
			"CMS_$ANALYSIS_eFakeTau_$CHANNEL_$ERA",
			"lnN",
			ch.SystMap("era", "process", "channel")
				(["7TeV", "8TeV"], ["ZLL"], ["mt", "et"], 1.30)
				(       ["13TeV"], ["ZLL", "ZL", "ZJ"], ["mt", "tt"], 1.15) #CV https://indico.cern.ch/event/515350/contributions/1194776/attachments/1257261/1856581/HttNuisanceParamUpdate_2016Apr13.pdf
				(       ["13TeV"], ["ZLL", "ZL", "ZJ"], ["et"], 1.30) # CV https://indico.cern.ch/event/515350/contributions/1194776/attachments/1257261/1856581/HttNuisanceParamUpdate_2016Apr13.pdf
		]
		self.eFakeTau_vloose_syst_args = [
			"CMS_$ANALYSIS_rate_eFakeTau_vloose_$ERA",
			"lnN",
			ch.SystMap("era", "process", "channel")
				(       ["13TeV"], ["ZLL", "ZL"], ["mt", "tt"], 1.10) # CV https://indico.cern.ch/event/515350/contributions/1194776/attachments/1257261/1856581/HttNuisanceParamUpdate_2016Apr13.pdf
		]
		self.eFakeTau_tight_syst_args = [
			"CMS_$ANALYSIS_rate_eFakeTau_tight_$ERA",
			"lnN",
			ch.SystMap("era", "process", "channel")
				(       ["13TeV"], ["ZLL", "ZL"], ["et"], 1.30) # CV https://indico.cern.ch/event/515350/contributions/1194776/attachments/1257261/1856581/HttNuisanceParamUpdate_2016Apr13.pdf
		]
		self.eFakeTau2016_syst_args = [
			"CMS_$ANALYSIS_eFakeTau_$ERA",
			"lnN",
			ch.SystMap("era", "process")
				(       ["13TeV"], ["ZLL", "ZL"], 1.12) # https://indico.cern.ch/event/566822/contributions/2377598/attachments/1374111/2085739/systematics.pdf
		]
		self.muFakeTau_syst_args = [
			"CMS_$ANALYSIS_mFakeTau_$ERA",
			"lnN",
			ch.SystMap("era", "process",)
				(       ["13TeV"], ["ZLL", "ZL"], 2.00) # CV https://indico.cern.ch/event/515350/contributions/1194776/attachments/1257261/1856581/HttNuisanceParamUpdate_2016Apr13.pdf
		]
		self.muFakeTau2016_syst_args = [
			"CMS_$ANALYSIS_mFakeTau_$ERA",
			"lnN",
			ch.SystMap("era", "process",)
				(       ["13TeV"], ["ZLL", "ZL"], 1.25) # https://indico.cern.ch/event/566822/contributions/2377598/attachments/1374111/2085739/systematics.pdf
		]
		self.zjFakeTau_syst_args = [
			"CMS_$ANALYSIS_zjFakeTau_$ERA",
			"lnN",
			ch.SystMap("era", "process",)
				(       ["13TeV"], ["ZLL", "ZL"], 1.30) # From Yuta's polarisation analysis
		]

		self.jetFakeTau_syst_args = [
			"CMS_$ANALYSIS_jetFakeTau_$ERA",
			"lnN",
			ch.SystMap("era", "process",)
				(       ["13TeV"], ["ZJ", "TTJJ", "VVJ"], 1.20)
		]

		self.zee_norm_syst_args = [
			"CMS_$ANALYSIS_zeeNorm_$ERA",
			"lnN",
			ch.SystMap("era", "process")
				(       ["13TeV"], ["ZLL", "ZL"], 1.03) # Source?
		]

		self.jec_syst_args = [
			"CMS_scale_j_$ERA",
			"shape",
			ch.SystMap("era")
				(["13TeV"], 1.0)
		]
		self.tau_es_syst_args = [
			"CMS_scale_t_$CHANNEL_$ERA",
			"shape",
			ch.SystMap("era", "channel")
				(["13TeV"], ["mt"], 1.0)
				(["13TeV"], ["et"], 1.0)
				(["13TeV"], ["tt"], 1.0)
		]
		self.tau_es_corr_syst_args = [
			"CMS_scale_t_$ERA",
			"shape",
			ch.SystMap("era")
				(["13TeV"], 1.0)
		]
		self.ele_es_syst_args = [
			"CMS_scale_e_$CHANNEL_$ERA",
			"shape",
			ch.SystMap("era", "channel")
				(["13TeV"], ["em"], 1.0)
				(["13TeV"], ["et"], 1.0)
		]
		self.mu_es_syst_args = [
			"CMS_scale_m_$CHANNEL_$ERA",
			"shape",
			ch.SystMap("era", "channel")
				(["13TeV"], ["em"], 1.0)
				(["13TeV"], ["mt"], 1.0)
		]
		self.ttj_syst_args = [
			"CMS_htt_ttbarShape_$ERA",
			"shape",
			ch.SystMap("era")
				(["13TeV"], 1.0)
		]
		self.dy_shape_syst_args = [
			"CMS_htt_dyShape_$ERA",
			"shape",
			ch.SystMap("era")
				(["13TeV"], 1.0)
		]
		self.jetFakeTau_qcd_syst_args = [
			"CMS_$ANALYSIS_jetFakeTau_qcd_Shape_$ERA",
			"shape",
			ch.SystMap("era")
			(["13TeV"], 1.0)
		]
		self.jetFakeTau_w_syst_args = [
			"CMS_$ANALYSIS_jetFakeTau_w_Shape_$ERA",
			"shape",
			ch.SystMap("era")
			(["13TeV"], 1.0)
		]
		self.jetFakeTau_tt_corr_syst_args = [
			"CMS_$ANALYSIS_jetFakeTau_tt_corr_Shape_$ERA",
			"shape",
			ch.SystMap("era")
			(["13TeV"], 1.0)
		]
		self.jetFakeTau_tt_stat_syst_args = [
			"CMS_$ANALYSIS_jetFakeTau_tt_stat_Shape_$ERA",
			"shape",
			ch.SystMap("era")
			(["13TeV"], 1.0)
		]
		self.jetFakeTau_frac_qcd_syst_args = [
			"CMS_$ANALYSIS_jetFakeTau_frac_qcd_Shape_$ERA",
			"shape",
			ch.SystMap("era")
			(["13TeV"], 1.0)
		]
		self.jetFakeTau_frac_tt_syst_args = [
			"CMS_$ANALYSIS_jetFakeTau_frac_tt_Shape_$ERA",
			"shape",
			ch.SystMap("era")
			(["13TeV"], 1.0)
		]
		self.jetFakeTau_frac_w_syst_args = [
			"CMS_$ANALYSIS_jetFakeTau_frac_w_Shape_$ERA",
			"shape",
			ch.SystMap("era")
			(["13TeV"], 1.0)
		]
		self.jetFakeTau_frac_dy_syst_args = [
			"CMS_$ANALYSIS_jetFakeTau_frac_dy_Shape_$ERA",
			"shape",
			ch.SystMap("era")
			(["13TeV"], 1.0)
		]
		
		self.boson_scale_met_syst_args = [
			"CMS_$ANALYSIS_boson_scale_met",
			"lnN",
			ch.SystMap("channel")
				(["mt"], 1.02)
		]
		self.boson_resolution_met_syst_args = [
			"CMS_$ANALYSIS_boson_reso_met",
			"lnN",
			ch.SystMap("channel")
				(["mt"], 1.02)
		]
		self.ewk_top_scale_met_syst_args = [
			"CMS_$ANALYSIS_ewkTop_scale_met",
			"lnN",
			ch.SystMap("channel")
				(["mt"], 1.03)
		]
		self.ewk_top_resolution_met_syst_args = [
			"CMS_$ANALYSIS_ewkTop_reso_met",
			"lnN",
			ch.SystMap("channel")
				(["mt"], 1.01)
		]

		self.met_resp_syst_args = [
			"CMS_scale_met_$CHANNEL_$ERA",
			"shape",
			ch.SystMap("era", "channel")
				(["13TeV"], ["em"], 1.0)
				(["13TeV"], ["et"], 1.0)
				(["13TeV"], ["mt"], 1.0)
				(["13TeV"], ["tt"], 1.0)
		]

		self.probetau_es_syst_args = [
			"CMS_scale_probetau_$CHANNEL_$ERA",
			"shape",
			ch.SystMap("era", "channel")
				(["13TeV"], ["et"], 1.0)
		]
		self.probeele_es_syst_args = [
			"CMS_scale_probeele_$CHANNEL_$ERA",
			"shape",
			ch.SystMap("era", "channel")
				(["13TeV"], ["et"], 1.0)
		]
		self.tagele_es_syst_args = [
			"CMS_scale_tagele_$CHANNEL_$ERA",
			"shape",
			ch.SystMap("era", "channel")
				(["13TeV"], ["et"], 1.0)
		]
		self.muFakeTau_es_syst_args = [
			"CMS_$ANALYSIS_scale_mFakeTau_$ERA",
			"shape",
			ch.SystMap("era", "channel")
				(["13TeV"], ["mt"], 1.0)
		]
		self.eleFakeTau_es_syst_args = [
			"CMS_$ANALYSIS_scale_eFakeTau_$ERA",
			"shape",
			ch.SystMap("era", "channel")
				(["13TeV"], ["et"], 1.0)
		]

		self.massres_syst_args = [
			"CMS_scale_massRes_$CHANNEL_$ERA",
			"shape",
			ch.SystMap("era", "channel")
				(["13TeV"], ["et"], 1.0)
		]
		
		# https://twiki.cern.ch/twiki/bin/view/LHCPhysics/CERNYellowReportPageAt1314TeV2014#s_13_0_TeV
		self.htt_qcd_scale_syst_args = [
			"QCD_scale_$PROCESS",
			"lnN",
			ch.SystMap("era", "process")
				(["13TeV"], ["ggH"], 1.079)
				(["13TeV"], ["qqH"], 1.007)
				(["13TeV"], ["VH"], 1.015)
				(["13TeV"], ["WH"], 1.015)
				(["13TeV"], ["ZH"], 1.038)
		]
		self.htt_pdf_scale_syst_args = [
			"PDF_scale_$PROCESS",
			"lnN",
			ch.SystMap("era", "process")
				(["13TeV"], ["ggH"], 1.071)
				(["13TeV"], ["qqH"], 1.032)
				(["13TeV"], ["VH"], 1.022)
				(["13TeV"], ["WH"], 1.022)
				(["13TeV"], ["ZH"], 1.022)
		]

		self.ztt_qcd_scale_syst_args = [
			"CMS_$ANALYSIS_QCDscale_$ERA",
			"lnN",
			ch.SystMap("era", "process")
				(["13TeV"], ["ZTT"], 1.005) # CV https://indico.cern.ch/event/515350/contributions/1194776/attachments/1257261/1856581/HttNuisanceParamUpdate_2016Apr13.pdf
		]
		self.ztt_qcd_scale_tt_syst_args = [
			"CMS_$ANALYSIS_QCDscale_$CHANNEL_$ERA",
			"lnN",
			ch.SystMap("era", "process", "channel")
				(["13TeV"], ["ZTT"], ["tt"], 1.06)
		]
		self.ztt_pdf_scale_syst_args = [
			"CMS_$ANALYSIS_pdf_$ERA",
			"lnN",
			ch.SystMap("era", "process")
				(["13TeV"], ["ZTT"], 1.015) # CV https://indico.cern.ch/event/515350/contributions/1194776/attachments/1257261/1856581/HttNuisanceParamUpdate_2016Apr13.pdf
		]

		# CMS AN-13-262 (v8, table 3)
		self.htt_ueps_syst_args = [
			"UEPS",
			"lnN",
			ch.SystMap("era", "process", "bin")
				(["13TeV"], ["ggH"], ["mt_0jet_high"], 1.060) # copied from 8TeV
				(["13TeV"], ["ggH"], ["mt_0jet_low"], 1.073) # copied from 8TeV
				(["13TeV"], ["ggH"], ["mt_1jet_high"], 0.996) # copied from 8TeV
				(["13TeV"], ["ggH"], ["mt_1jet_low"], 1.007) # copied from 8TeV
				(["13TeV"], ["ggH"], ["mt_2jet_vbf"], 0.988) # copied from 8TeV

				(["13TeV"], ["ggH"], ["et_0jet_high"], 1.060) # copied from 8TeV
				(["13TeV"], ["ggH"], ["et_0jet_low"], 1.073) # copied from 8TeV
				(["13TeV"], ["ggH"], ["et_1jet_high"], 0.996) # copied from 8TeV
				(["13TeV"], ["ggH"], ["et_1jet_low"], 1.007) # copied from 8TeV
				(["13TeV"], ["ggH"], ["et_2jet_vbf"], 0.988) # copied from 8TeV

				(["13TeV"], ["ggH"], ["em_0jet_high"], 1.063) # copied from 8TeV
				(["13TeV"], ["ggH"], ["em_0jet_low"], 1.089) # copied from 8TeV
				(["13TeV"], ["ggH"], ["em_1jet_high"], 1.004) # copied from 8TeV
				(["13TeV"], ["ggH"], ["em_1jet_low"], 1.000) # copied from 8TeV
				(["13TeV"], ["ggH"], ["em_2jet_vbf"], 0.988) # copied from 8TeV

				(["13TeV"], ["ggH"], ["tt_inclusive"], 1.025) # copied from 8TeV

				(["13TeV"], ["qqH", "WH", "ZH", "VH"], ["mt_0jet_high"], 1.028) # copied from 8TeV
				(["13TeV"], ["qqH", "WH", "ZH", "VH"], ["mt_0jet_low"], 1.018) # copied from 8TeV
				(["13TeV"], ["qqH", "WH", "ZH", "VH"], ["mt_1jet_high"], 0.954) # copied from 8TeV
				(["13TeV"], ["qqH", "WH", "ZH", "VH"], ["mt_1jet_low"], 0.946) # copied from 8TeV
				(["13TeV"], ["qqH", "WH", "ZH", "VH"], ["mt_2jet_vbf"], 0.893) # copied from 8TeV

				(["13TeV"], ["qqH", "WH", "ZH", "VH"], ["et_0jet_high"], 1.028) # copied from 8TeV
				(["13TeV"], ["qqH", "WH", "ZH", "VH"], ["et_0jet_low"], 1.018) # copied from 8TeV
				(["13TeV"], ["qqH", "WH", "ZH", "VH"], ["et_1jet_high"], 0.954) # copied from 8TeV
				(["13TeV"], ["qqH", "WH", "ZH", "VH"], ["et_1jet_low"], 0.946) # copied from 8TeV
				(["13TeV"], ["qqH", "WH", "ZH", "VH"], ["et_2jet_vbf"], 0.893) # copied from 8TeV

				(["13TeV"], ["qqH", "WH", "ZH", "VH"], ["em_0jet_high"], 1.042) # copied from 8TeV
				(["13TeV"], ["qqH", "WH", "ZH", "VH"], ["em_0jet_low"], 1.035) # copied from 8TeV
				(["13TeV"], ["qqH", "WH", "ZH", "VH"], ["em_1jet_high"], 0.978) # copied from 8TeV
				(["13TeV"], ["qqH", "WH", "ZH", "VH"], ["em_1jet_low"], 0.984) # copied from 8TeV
				(["13TeV"], ["qqH", "WH", "ZH", "VH"], ["em_2jet_vbf"], 0.893) # copied from 8TeV

				(["13TeV"], ["qqH", "WH", "ZH", "VH"], ["tt_inclusive"], 1.025) # copied from 8TeV
		]

		path=os.path.expandvars("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/mva_configs/")
		self.mva_bdt_syst_uncs =[
			"mva_regular_BDT_shifts",
			"lnN"]
		mapster_1 = ch.SystMap("bin", "process")
		if os.path.exists(os.path.join(path, "Reg_BDT.cfg")):
			reg_bdt = jsonTools.JsonDict(os.path.join(path, "Reg_BDT.cfg"))
			for category in reg_bdt.keys():
				call = ([category], ["ZTT", "ZLL", "ZL", "ZJ", "TTJ", "TT", "VV", "WJ", "W", "ggH", "qqH", "WH", "ZH", "VH"], reg_bdt[category])
				mapster_1(*call)
		else:
			mapster_1(["dummy"], ["ZTT", "ZLL", "ZL", "ZJ", "TTJ", "TT", "VV", "WJ", "W", "ggH", "qqH", "WH", "ZH", "VH"], (1.0,1.0))
		self.mva_bdt_syst_uncs.append(mapster_1)
			#values without process mapping [3.734375, 3.609375, 3.640625]
		self.mva_vbf_bdt_syst_uncs =[
			"mva_vbftagger_BDT_shifts",
			"lnN"]
		mapster_2 = ch.SystMap("bin", "process")
		if os.path.exists(os.path.join(path, "VBF_BDT.cfg")):
			vbf_bdt = jsonTools.JsonDict(os.path.join(path, "VBF_BDT.cfg"))
			for category in vbf_bdt.keys():
				call = ([category], ["ZTT", "ZLL", "ZL", "ZJ", "TTJ", "TT", "VV", "WJ", "W", "ggH", "qqH", "WH", "ZH", "VH"], vbf_bdt[category])
				mapster_2(*call)
		else:
			mapster_2(["dummy"], ["ZTT", "ZLL", "ZL", "ZJ", "TTJ", "TT", "VV", "WJ", "W", "ggH", "qqH", "WH", "ZH", "VH"], (1.0,1.0))
		self.mva_vbf_bdt_syst_uncs.append(mapster_2)

	def add_processes(self, channel, categories, bkg_processes, sig_processes=["ztt"], add_data=True, *args, **kwargs):
		bin = [(self.configs.category2binid(category, channel), category) for category in categories]

		for key in ["channel", "procs", "bin", "signal"]:
			if key in kwargs:
				kwargs.pop(key)

		non_sig_kwargs = copy.deepcopy(kwargs)
		if "mass" in non_sig_kwargs:
			non_sig_kwargs.pop("mass")

		if add_data:		
			self.cb.AddObservations(channel=[channel], mass=["*"], bin=bin, *args, **non_sig_kwargs)
		self.cb.AddProcesses(channel=[channel], mass=["*"], procs=bkg_processes, bin=bin, signal=False, *args, **non_sig_kwargs)
		self.cb.AddProcesses(channel=[channel], procs=sig_processes, bin=bin, signal=True, *args, **kwargs)

	def get_samples_per_shape_systematic(self):
		samples_per_shape_systematic = {}
		samples_per_shape_systematic["nominal"] = self.cb.process_set()
		for shape_systematic in self.cb.cp().syst_type(["shape"]).syst_name_set():
			samples_per_shape_systematic[shape_systematic] = self.cb.cp().syst_type(["shape"]).syst_name([shape_systematic]).SetFromSysts(ch.Systematic.process)
		return samples_per_shape_systematic

	def extract_shapes(self, root_filename_template,
	                   bkg_histogram_name_template, sig_histogram_name_template,
	                   bkg_syst_histogram_name_template, sig_syst_histogram_name_template,
	                   update_systematics=False):
		for analysis in self.cb.analysis_set():
			for era in self.cb.cp().analysis([analysis]).era_set():
				for channel in self.cb.cp().analysis([analysis]).era([era]).channel_set():
					for category in self.cb.cp().analysis([analysis]).era([era]).channel([channel]).bin_set():
						root_filename = root_filename_template.format(
								ANALYSIS=analysis,
								CHANNEL=channel,
								BIN=category,
								ERA=era
						)

						cb_backgrounds = self.cb.cp().analysis([analysis]).era([era]).channel([channel]).bin([category]).backgrounds()
						cb_backgrounds.ExtractShapes(
								root_filename,
								bkg_histogram_name_template.replace("{", "").replace("}", ""),
								bkg_syst_histogram_name_template.replace("{", "").replace("}", "")
						)

						cb_signals = self.cb.cp().analysis([analysis]).era([era]).channel([channel]).bin([category]).signals()
						cb_signals.ExtractShapes(
								root_filename,
								sig_histogram_name_template.replace("{", "").replace("}", ""),
								sig_syst_histogram_name_template.replace("{", "").replace("}", "")
						)

						# update/add systematics related to the estimation of backgrounds/signals
						# these uncertainties are stored in the input root files
						if update_systematics:
							with tfilecontextmanager.TFileContextManager(root_filename, "READ") as root_file:
								root_object_paths = [path for key, path in roottools.RootTools.walk_root_directory(root_file)]

								processes_histogram_names = []
								for process in cb_backgrounds.process_set():
									bkg_histogram_name = bkg_histogram_name_template.replace("$", "").format(
											ANALYSIS=analysis,
											CHANNEL=channel,
											BIN=category,
											ERA=era,
											PROCESS=process
									)
									yield_unc_rel = Datacards.get_yield_unc_rel(bkg_histogram_name, root_file, root_object_paths)
									if (not yield_unc_rel is None) and (yield_unc_rel != 0.0):
										cb_backgrounds.cp().process([process]).AddSyst(
												self.cb,
												"CMS_$ANALYSIS_$PROCESS_estimation_$ERA",
												"lnN",
												ch.SystMap("process")([process], 1.0+yield_unc_rel)
										)

								for process in cb_signals.process_set():
									for mass in cb_signals.mass_set():
										if mass != "*":
											sig_histogram_name = sig_histogram_name_template.replace("$", "").format(
													ANALYSIS=analysis,
													CHANNEL=channel,
													BIN=category,
													ERA=era,
													PROCESS=process,
													MASS=mass
											)
											yield_unc_rel = Datacards.get_yield_unc_rel(sig_histogram_name, root_file, root_object_paths)
											if (not yield_unc_rel is None) and (yield_unc_rel != 0.0):
												cb_backgrounds.cp().process([process]).mass([mass]).AddSyst(
														self.cb,
														"CMS_$ANALYSIS_$PROCESS$MASS_estimation_$ERA",
														"lnN",
														ch.SystMap("process", "mass")([process], [mass], 1.0+yield_unc_rel)
												)

		if log.isEnabledFor(logging.DEBUG):
			self.cb.PrintAll()
	
	def create_morphing_signals(self, morphing_variable_name, nominal_value, min_value, max_value):
		self.workspace = ROOT.RooWorkspace("workspace", "workspace")
		self.morphing_variable = ROOT.RooRealVar(morphing_variable_name, morphing_variable_name, nominal_value, min_value, max_value)
		
		cb_signals = self.cb.cp().signals()
		for category in cb_signals.bin_set():
			cb_signals_category = cb_signals.cp().bin([category])
			for signal_process in cb_signals_category.process_set():
				morphing.BuildRooMorphing(self.workspace, self.cb, category, signal_process, self.morphing_variable, "norm", True, log.isEnabledFor(logging.DEBUG))
		
		self.cb.AddWorkspace(self.workspace, False)
		self.cb.cp().signals().ExtractPdfs(self.cb, "workspace", "$BIN_$PROCESS_morph", "")

		if log.isEnabledFor(logging.DEBUG):
			self.cb.PrintAll()

	@staticmethod
	def get_yield_unc_rel(histogram_path, root_file, root_object_paths):
		metadata_path = histogram_path+"_metadata"
		if metadata_path in root_object_paths:
			metadata = jsonTools.JsonDict(root_file.Get(metadata_path).GetString().Data())
			return metadata.get("yield_unc_rel", None)
		else:
			return None

	def add_bin_by_bin_uncertainties(self, processes, add_threshold=0.1, merge_threshold=0.5, fix_norm=True):
		bin_by_bin_factory = ch.BinByBinFactory()
		if log.isEnabledFor(logging.DEBUG):
			bin_by_bin_factory.SetVerbosity(100)

		bin_by_bin_factory.SetAddThreshold(add_threshold)
		bin_by_bin_factory.SetMergeThreshold(merge_threshold)
		bin_by_bin_factory.SetFixNorm(fix_norm)

		bin_by_bin_factory.MergeBinErrors(self.cb.cp().process(processes))
		bin_by_bin_factory.AddBinByBin(self.cb.cp().process(processes), self.cb)
		#ch.SetStandardBinNames(self.cb) # TODO: this line seems to mix up the categories
		
		self.cb.SetGroup("bbb", [".*_bin_\\d+"])
		self.cb.SetGroup("syst_plus_bbb", [".*"])

	def scale_expectation(self, scale_factor, no_norm_rate_bkg=False, no_norm_rate_sig=False):
		self.cb.cp().backgrounds().ForEachProc(lambda process: process.set_rate((process.no_norm_rate() if no_norm_rate_bkg else process.rate()) * scale_factor))
		self.cb.cp().signals().ForEachProc(lambda process: process.set_rate((process.no_norm_rate() if no_norm_rate_sig else process.rate()) * scale_factor))
	
	def scale_processes(self, scale_factor, processes, no_norm_rate=False):
		self.cb.cp().process(processes).ForEachProc(lambda process: process.set_rate((process.no_norm_rate() if no_norm_rate else process.rate()) * scale_factor))

	def replace_observation_by_asimov_dataset(self, signal_mass=None):
		def _replace_observation_by_asimov_dataset(observation):
			cb = self.cb.cp().analysis([observation.analysis()]).era([observation.era()]).channel([observation.channel()]).bin([observation.bin()])
			background = cb.cp().backgrounds()
			signal = cb.cp().signals() if signal_mass is None else cb.cp().signals().mass([signal_mass])
			observation.set_shape(background.GetShape() + signal.GetShape(), True)
			observation.set_rate(background.GetRate() + signal.GetRate())

		self.cb.cp().ForEachObs(_replace_observation_by_asimov_dataset)

	def write_datacards(self, datacard_filename_template, root_filename_template, output_directory="."):
		writer = ch.CardWriter(os.path.join("$TAG", datacard_filename_template),
		                       os.path.join("$TAG", root_filename_template))
		if log.isEnabledFor(logging.DEBUG):
			writer.SetVerbosity(1)
		
		# enable writing datacards in cases where the mass does not have its original meaning
		if (len(self.cb.mass_set()) == 1) and (self.cb.mass_set()[0] == "*"):
			writer.SetWildcardMasses([])

		return writer.WriteCards(output_directory[:-1] if output_directory.endswith("/") else output_directory, self.cb)

	def text2workspace(self, datacards_cbs, n_processes=1, *args):
		commands = ["text2workspace.py -m {MASS} {ARGS} {DATACARD} -o {OUTPUT}".format(
				MASS=[mass for mass in cb.mass_set() if mass != "*"][0] if len(cb.mass_set()) > 1 else "0", # TODO: maybe there are more masses?
				ARGS=" ".join(args),
				DATACARD=datacard,
				OUTPUT=os.path.splitext(datacard)[0]+".root"
		) for datacard, cb in datacards_cbs.iteritems()]

		tools.parallelize(_call_command, commands, n_processes=n_processes, description="text2workspace.py")

		return {datacard : os.path.splitext(datacard)[0]+".root" for datacard in datacards_cbs.keys()}

	def combine(self, datacards_cbs, datacards_workspaces, datacards_poi_ranges=None, n_processes=1, *args, **kwargs):
		if datacards_poi_ranges is None:
			datacards_poi_ranges = {}
		tmp_args = " ".join(args)

		chunks = [[None, None]]
		if "{CHUNK}" in tmp_args and "--points" in tmp_args:
			splited_args = tmp_args.split()
			n_points = int(splited_args[splited_args.index("--points") + 1])
			n_points_per_chunk = 199
			chunks = [[chunk*n_points_per_chunk, (chunk+1)*n_points_per_chunk-1] for chunk in xrange(n_points/n_points_per_chunk+1)]
		
		method = re.search("(-M|--method)[\s=\"\']*(?P<method>\w*)[\"\']?\s", tmp_args)
		if not method is None:
			method = method.groupdict()["method"]
		
		name = re.search("(-n|--name)[\s=\"\']*(?P<name>\w*)[\"\']?\s", tmp_args)
		if not name is None:
			name = name.groupdict()["name"]
		
		split_stat_syst_uncs = kwargs.get("split_stat_syst_uncs", False)
		if split_stat_syst_uncs and (method is None):
			log.error("Uncertainties are not split into stat. and syst. components, since the method for combine is unknown!")
			split_stat_syst_uncs = False
		if split_stat_syst_uncs and (not "MultiDimFit" in method):
			log.error("Uncertainties are not split into stat. and syst. components. This is only supported for the MultiDimFit method!")
			split_stat_syst_uncs = False
		
		split_stat_syst_uncs_options = [""]
		split_stat_syst_uncs_names = [""]
		if split_stat_syst_uncs:
			split_stat_syst_uncs_options = [
				"--saveWorkspace",
				"--snapshotName {method} -w w".format(method=method),
				"--snapshotName {method} -w w --freezeNuisances {uncs}".format(method=method, uncs="{uncs}"),
			]
			split_stat_syst_uncs_names = [
				"Workspace",
				"TotUnc",
				"StatUnc",
			]
		
		for split_stat_syst_uncs_index, (split_stat_syst_uncs_option, split_stat_syst_uncs_name) in enumerate(zip(split_stat_syst_uncs_options, split_stat_syst_uncs_names)):
			prepared_tmp_args = None
			new_name = None
			if split_stat_syst_uncs:
				new_name = ("" if name is None else name) + split_stat_syst_uncs_name
				if name is None:
					prepared_tmp_args = tmp_args + " -n " + new_name
				else:
					prepared_tmp_args = copy.deepcopy(tmp_args)
					prepared_tmp_args = re.sub("(--algo)([\s=\"\']*)(\w*)([\"\']?\s)", "\\1\\2 "+("none" if split_stat_syst_uncs_index == 0 else "\\3")+"\\4", prepared_tmp_args)
					prepared_tmp_args = re.sub("(-n|--name)([\s=\"\']*)(\w*)([\"\']?\s)", "\\1\\2"+new_name+"\\4", prepared_tmp_args)
			else:
				prepared_tmp_args = tmp_args
			
			commands = []
			for chunk_index, (chunk_min, chunk_max) in enumerate(chunks):
				commands.extend([[
						"combine -m {MASS} {POI_RANGE} {ARGS} {CHUNK_POINTS} {SPLIT_STAT_SYST_UNCS} {WORKSPACE}".format(
								MASS=[mass for mass in datacards_cbs[datacard].mass_set() if mass != "*"][0] if len(datacards_cbs[datacard].mass_set()) > 1 else "0", # TODO: maybe there are more masses?
								POI_RANGE="--rMin {RMIN} --rMax {RMAX}" if datacard in datacards_poi_ranges else "",
								ARGS=prepared_tmp_args.format(CHUNK=str(chunk_index), RMIN="{RMIN}", RMAX="{RMAX}"),
								CHUNK_POINTS = "" if (chunk_min is None) or (chunk_max is None) else "--firstPoint {CHUNK_MIN} --lastPoint {CHUNK_MAX}".format(
										CHUNK_MIN=chunk_min,
										CHUNK_MAX=chunk_max
								),
								SPLIT_STAT_SYST_UNCS=split_stat_syst_uncs_option.format(uncs=",".join(kwargs.get("additional_freeze_nuisances", [])+datacards_cbs[datacard].syst_name_set())),
								WORKSPACE="-d "+workspace
						).format(RMIN=datacards_poi_ranges.get(datacard, ["", ""])[0], RMAX=datacards_poi_ranges.get(datacard, ["", ""])[1]),
						os.path.dirname(workspace)
				] for datacard, workspace in datacards_workspaces.iteritems()])

			tools.parallelize(_call_command, commands, n_processes=n_processes, description="combine")
			
			if split_stat_syst_uncs and (split_stat_syst_uncs_index == 0):
				# replace workspaces by saved versions from the first fit including the postfit nuisance parameter values
				for datacard, workspace in datacards_workspaces.iteritems():
					datacards_workspaces[datacard] = glob.glob(os.path.join(os.path.dirname(workspace), "higgsCombine"+new_name+"."+method+".*.root"))[0]

	def annotate_trees(self, datacards_workspaces, root_filename, value_regex_list, value_replacements=None, n_processes=1, values_tree_files=None, *args):
		if value_replacements is None:
			value_replacements = {}

		if values_tree_files is None:
			values_tree_files = {}
		
		commands = []
		for datacard, workspace in datacards_workspaces.iteritems():
			float_values = []
			found_match = False
			for value_regex in value_regex_list:
				search_result = re.search(value_regex, workspace)
				if not search_result is None:
					value = search_result.groups()[0]
					float_values.append(float(value_replacements.get(value, value)))
					found_match = True
				else:
					float_values.append(-999.0)
			
			if found_match:
				files = os.path.join(os.path.dirname(workspace), root_filename)
				values_tree_files.setdefault(tuple(float_values), []).extend(glob.glob(files))

				commands.append("annotate-trees.py {FILES} --values {VALUES} {ARGS}".format(
						FILES=files,
						VALUES=" ".join([str(value) for value in float_values]),
						ARGS=" ".join(args)
				))
		
		tools.parallelize(_call_command, commands, n_processes=n_processes, description="annotate-trees.py")
		return values_tree_files

	def hypotestresulttree(self, datacards_cbs, n_processes=1, rvalue="1", poiname="x"):
		commands = []
		hypotestresulttree = {}
		

		#for fit_type in fit_type_list:
		commands.extend(["root -q -b \"HiggsAnalysis/KITHiggsToTauTau/scripts/hypoTestResultTree.cxx(\\\"{INPUT}\\\",\\\"{OUTPUT}\\\",{MASS},{RVALUE},\\\"{POINAME}\\\")\"".format(
				INPUT=os.path.join(os.path.dirname(datacard),"higgsCombine.HybridNew.mH125.root"),
				OUTPUT=os.path.join(os.path.dirname(datacard), "higgsCombine.HybridNew.mH125_qmu.root"),
				MASS=[mass for mass in cb.mass_set() if mass != "*"][0] if len(cb.mass_set()) > 1 else "0", # TODO: maybe there are more masses?
				RVALUE= str(rvalue),
				POINAME=str(poiname)
				
				#ARGS=", ".join(args)
			) for datacard, cb in datacards_cbs.iteritems()])

			#datacards_postfit_shapes.setdefault(fit_type, {}).update({
			#		datacard : os.path.splitext(datacard)[0]+"_"+fit_type+".root"
			#for datacard, cb in datacards_cbs.iteritems()})

		tools.parallelize(_call_command, commands, n_processes=n_processes, description="hypoTestResultTree.cxx")

		return {datacard : os.path.join(os.path.dirname(datacard), "higgsCombine.HybridNew.mH125_qmu.root") for datacard in datacards_cbs.keys()}


	def postfit_shapes(self, datacards_cbs, s_fit_only=False, n_processes=1, *args):
		commands = []
		datacards_postfit_shapes = {}
		fit_type_list = kwargs.get("fit_type_list", ["fit_s", "fit_b"])
		if s_fit_only:
			fit_type_list.remove("fit_b")

		for fit_type in fit_type_list:
			commands.extend(["PostFitShapes --postfit -d {DATACARD} -o {OUTPUT} -m {MASS} -f {FIT_RESULT} {ARGS}".format(
					DATACARD=datacard,
					OUTPUT=os.path.splitext(datacard)[0]+"_"+fit_type+".root",
					MASS=[mass for mass in cb.mass_set() if mass != "*"][0] if len(cb.mass_set()) > 1 else "0", # TODO: maybe there are more masses?
					FIT_RESULT=os.path.join(os.path.dirname(datacard), kwargs.get("fit_result", "mlfit.root")+":"+fit_type),
					ARGS=" ".join(args)
			) for datacard, cb in datacards_cbs.iteritems()])

			datacards_postfit_shapes.setdefault(fit_type, {}).update({
					datacard : os.path.splitext(datacard)[0]+"_"+fit_type+".root"
			for datacard, cb in datacards_cbs.iteritems()})

		tools.parallelize(_call_command, commands, n_processes=n_processes, description="PostFitShapes")

		return datacards_postfit_shapes

	def postfit_shapes_fromworkspace(self, datacards_cbs, datacards_workspaces, s_fit_only=False, n_processes=1, *args, **kwargs):
		commands = []
		datacards_postfit_shapes = {}
		fit_type_list = kwargs.get("fit_type_list", ["fit_s", "fit_b"])
		if s_fit_only:
			fit_type_list.remove("fit_b")

		for fit_type in fit_type_list:
			commands.extend(["PostFitShapesFromWorkspace --postfit -w {WORKSPACE} -d {DATACARD} -o {OUTPUT} -m {MASS} -f {FIT_RESULT} {ARGS}".format(
					WORKSPACE=datacards_workspaces[datacard],
					DATACARD=datacard,
					OUTPUT=os.path.splitext(datacard)[0]+"_"+fit_type+".root",
					MASS=[mass for mass in cb.mass_set() if mass != "*"][0] if len(cb.mass_set()) > 1 else "0", # TODO: maybe there are more masses?
					FIT_RESULT=os.path.join(os.path.dirname(datacard), kwargs.get("fit_result", "mlfit.root")+":"+fit_type),
					ARGS=" ".join(args)
			) for datacard, cb in datacards_cbs.iteritems()])

			datacards_postfit_shapes.setdefault(fit_type, {}).update({
					datacard : os.path.splitext(datacard)[0]+"_"+fit_type+".root"
			for datacard, cb in datacards_cbs.iteritems()})

		tools.parallelize(_call_command, commands, n_processes=n_processes, description="PostFitShapesFromWorkspace")

		return datacards_postfit_shapes

	def prefit_postfit_plots(self, datacards_cbs, datacards_postfit_shapes, plotting_args=None, n_processes=1, signal_stacked_on_bkg=False, *args):
		if plotting_args is None:
			plotting_args = {}
		
		base_path = reduce(lambda datacard1, datacard2: tools.longest_common_substring(datacard1, datacard2), datacards_cbs.keys())
		
		plot_configs = []
		bkg_plotting_order = ["ZTTPOSPOL", "ZTTNEGPOL", "ZTT", "ZLL", "ZL", "ZJ", "TTTAUTAU", "TTJ", "TT", "VV", "WJ", "W", "QCD"]
		for level in ["prefit", "postfit"]:
			for index, (fit_type, datacards_postfit_shapes_dict) in enumerate(datacards_postfit_shapes.iteritems()):
				if (index == 0) or (level == "postfit"):
					for datacard, postfit_shapes in datacards_postfit_shapes_dict.iteritems():
						for category in datacards_cbs[datacard].cp().bin_set():
							stacked_processes = []
							if signal_stacked_on_bkg:
								stacked_processes.extend(datacards_cbs[datacard].cp().bin([category]).signals().process_set())
							stacked_processes.extend(datacards_cbs[datacard].cp().bin([category]).backgrounds().process_set())
							stacked_processes.sort(key=lambda process: bkg_plotting_order.index(process) if process in bkg_plotting_order else len(bkg_plotting_order))

							config = {}
							config["files"] = [postfit_shapes]
							config["folders"] = [category+"_"+level]
							config["x_expressions"] = [p.strip("_noplot") for p in stacked_processes] + ["TotalSig"] + ["data_obs", "TotalBkg"]
							config["nicks"] = stacked_processes + ["TotalSig" + ("_noplot" if signal_stacked_on_bkg else "")] + ["data_obs", "TotalBkg" + ("_noplot" if signal_stacked_on_bkg else "")]
							config["stacks"] = (["stack"]*len(stacked_processes)) + (["data"] if signal_stacked_on_bkg else ["sig", "data", "bkg_unc"])

							config["labels"] = [label.lower() for label in stacked_processes + (["data_obs"] if signal_stacked_on_bkg else ["TotalSig", "data_obs", "TotalBkg"])]
							config["colors"] = [color.lower() for color in stacked_processes + (["data_obs"] if signal_stacked_on_bkg else ["TotalSig", "data_obs", "TotalBkg"])]
							config["markers"] = (["HIST"]*len(stacked_processes)) + (["E"] if signal_stacked_on_bkg else ["LINE", "E", "E2"])
							config["legend_markers"] = (["F"]*len(stacked_processes)) + (["ELP"] if signal_stacked_on_bkg else ["L", "ELP", "F"])

							config["x_label"] = category.split("_")[0]+"_"+plotting_args.get("x_expressions", None)
							config["title"] = "channel_"+category.split("_")[0]
							config["energies"] = [13.0]
							config["lumis"] = [float("%.1f" % plotting_args.get("lumi", 1.0))]
							if plotting_args.get("era", False):
								config["year"] = plotting_args.get("era")
							config["legend"] = [0.7, 0.6, 0.9, 0.88]
							config["y_lims"] = [0.0]
							if plotting_args.get("unrolled", False):
								config["canvas_width"] = 1200
								config["x_label"] = "bins"
								if plotting_args.get("texts", False) and plotting_args.get("texts_x", False):
									config["texts"] = plotting_args.get("texts")
									config["texts_x"] = plotting_args.get("texts_x")
									config["texts_y"] = list((0.65 for i in range(len(config["texts"]))))
									config["texts_size"] = [0.05]

							config["output_dir"] = os.path.join(os.path.dirname(datacard), "plots")
							config["filename"] = level+("_"+fit_type if level == "postfit" else "")+"_"+category
							if plotting_args.get("www", False):
								config["www"] = os.path.join(config["output_dir"].replace(base_path, plotting_args["www"]+"/"))

							if plotting_args.get("normalize", False):
								config.setdefault("analysis_modules", []).append("NormalizeByBinWidth")

							if plotting_args.get("ratio", False):
								if signal_stacked_on_bkg:
									if not "SumOfHistograms" in config.get("analysis_modules", []):
										config.setdefault("analysis_modules", []).append("SumOfHistograms")
									config.setdefault("sum_nicks", []).append("TotalBkg_noplot TotalSig_noplot")
									config.setdefault("sum_result_nicks", []).append("TotalBkg")
								
								if not "Ratio" in config.get("analysis_modules", []):
									config.setdefault("analysis_modules", []).append("Ratio")
								config.setdefault("ratio_numerator_nicks", []).extend(["TotalBkg", "data_obs"])
								config.setdefault("ratio_denominator_nicks", []).extend(["TotalBkg"] * 2)
								config.setdefault("ratio_result_nicks", []).extend(["ratio_unc", "ratio"])
								config["ratio_denominator_no_errors"] = True
								
								config.setdefault("colors", []).extend(["totalbkg", "#000000"])
								config.setdefault("markers", []).extend(["E2", "E"])
								config.setdefault("legend_markers", []).extend(["F", "ELP"])
								config.setdefault("labels", []).extend([""] * 2)
								config.setdefault("stacks", []).extend(["unc", "ratio"])
								config["legend"] = [0.7, 0.4, 0.95, 0.83]
								config["subplot_grid"] = "True"
								config["y_subplot_lims"] = [0.5, 1.5]
								config["y_subplot_label"] = "Obs./Exp."

							plot_configs.append(config)

		# create result plots HarryPlotter
		return higgsplot.HiggsPlotter(list_of_config_dicts=plot_configs, list_of_args_strings=[plotting_args.get("args", "")], n_processes=n_processes)

	def print_pulls(self, datacards_cbs, n_processes=1, *args, **kwargs):
		commands = []
		for pulls_format, file_format in zip(["latex", "text"], ["tex", "txt"]):
			for all_nuissances in [False, True]:
				commands.extend([[
						"execute-command.py \"python $CMSSW_BASE/src/HiggsAnalysis/CombinedLimit/test/diffNuisances.py -f {FORMAT} {ALL} {PLOT} {ARGS} {FIT_RESULT}\" --log-file {LOG_FILE}".format(
								FORMAT=pulls_format,
								ALL=("-a" if all_nuissances else ""),
								PLOT="-g "+("" if all_nuissances else "largest_")+"pulls.root",
								ARGS=" ".join(args),
								FIT_RESULT=os.path.join(os.path.dirname(datacard), kwargs.get("fit_result", "mlfit.root")),
								LOG_FILE=("" if all_nuissances else "largest_")+"pulls."+file_format
						),
						os.path.dirname(datacard)
				] for datacard in datacards_cbs.keys()])

		tools.parallelize(_call_command, commands, n_processes=n_processes, description="diffNuisances.py")

	def pull_plots(self, datacards_postfit_shapes, s_fit_only=False, plotting_args=None, n_processes=1, *args):
		if plotting_args is None:
			plotting_args = {}
		
		datacards = []
		for fit_type, datacards_postfit_shapes_dict in datacards_postfit_shapes.iteritems():
			datacards.extend(datacards_postfit_shapes_dict.keys())
		base_path = reduce(lambda datacard1, datacard2: tools.longest_common_substring(datacard1, datacard2), datacards)

		plot_configs = []
		for index, (fit_type, datacards_postfit_shapes_dict) in enumerate(datacards_postfit_shapes.iteritems()):
			if (index == 0):
				for datacard, postfit_shapes in datacards_postfit_shapes_dict.iteritems():

					config = {}
					config["files"] = [os.path.join(os.path.dirname(datacard), "mlfit.root")]
					config["input_modules"] = ["InputRootSimple"]
					config["root_names"] = ["fit_s", "fit_b", "nuisances_prefit"]
					if s_fit_only:
						config["root_names"] = ["fit_s", "nuisances_prefit"]
						config["fit_s_only"] = [True]
					config["analysis_modules"] = ["ComputePullValues"]
					config["nicks_blacklist"] = ["graph_b"]
					config["fit_poi"] = plotting_args.get("fit_poi", "r")

					config["left_pad_margin"] = 0.40
					config["labels"] = ["prefit", "S+B model"]
					config["markers"] = ["L2", "P"]
					config["fill_styles"] = [3001, 0]
					config["legend"] = [0.75, 0.8]
					config["legend_markers"] = ["LF", "LP"]
					config["x_lims"] = [-5.0, 5.0]
					config["x_label"] = "Pull values"

					config["output_dir"] = os.path.join(os.path.dirname(datacard), "plots")
					config["filename"] = "pulls"
					if plotting_args.get("www", False):
						config["www"] = os.path.join(config["output_dir"].replace(base_path, plotting_args["www"]+"/"))

					plot_configs.append(config)

		# create result plots HarryPlotter
		return higgsplot.HiggsPlotter(list_of_config_dicts=plot_configs, list_of_args_strings=[plotting_args.get("args", "")], n_processes=n_processes)
	
	def nuisance_impacts(self, datacards_cbs, datacards_workspaces, n_processes=1, *args):
		tmp_args = " ".join(args)
		
		commandsInitialFit = []
		commandsInitialFit.extend([[
				"combineTool.py -M Impacts -d {WORKSPACE} -m {MASS} --robustFit 1 --minimizerTolerance 0.1 --minimizerStrategy 0 --minimizerAlgoForMinos Minuit2,migrad --doInitialFit --allPars {ARGS}".format(
						MASS=[mass for mass in datacards_cbs[datacard].mass_set() if mass != "*"][0] if len(datacards_cbs[datacard].mass_set()) > 1 else "0",
						ARGS=tmp_args.format(),
						WORKSPACE=workspace
				),
				os.path.dirname(workspace)
		] for datacard, workspace in datacards_workspaces.iteritems()])
		
		commandsFits = []
		commandsFits.extend([[
				"combineTool.py -M Impacts -d {WORKSPACE} -m {MASS} --robustFit 1 --minimizerTolerance 0.1 --minimizerStrategy 0 --minimizerAlgoForMinos Minuit2,migrad --doFits --parallel {NPROCS} --allPars {ARGS}".format(
						MASS=[mass for mass in datacards_cbs[datacard].mass_set() if mass != "*"][0] if len(datacards_cbs[datacard].mass_set()) > 1 else "0",
						ARGS=tmp_args.format(),
						WORKSPACE=workspace,
						NPROCS=n_processes
				),
				os.path.dirname(workspace)
		] for datacard, workspace in datacards_workspaces.iteritems()])
		
		commandsOutput = []
		commandsOutput.extend([[
				"combineTool.py -M Impacts -d {WORKSPACE} -m {MASS} --robustFit 1 --minimizerTolerance 0.1 --minimizerStrategy 0 --minimizerAlgoForMinos Minuit2,migrad --output impacts.json --parallel {NPROCS} --allPars {ARGS}".format(
						MASS=[mass for mass in datacards_cbs[datacard].mass_set() if mass != "*"][0] if len(datacards_cbs[datacard].mass_set()) > 1 else "0",
						ARGS=tmp_args.format(),
						WORKSPACE=workspace,
						NPROCS=n_processes
				),
				os.path.dirname(workspace)
		] for datacard, workspace in datacards_workspaces.iteritems()])
		
		commandsPlot = []
		commandsPlot.extend([[
				"plotImpacts.py -i {INPUT} -o {OUTPUT}".format(
						INPUT="impacts.json",
						OUTPUT="plots/nuisance_impacts"
				),
				os.path.dirname(workspace)
		] for datacard, workspace in datacards_workspaces.iteritems()])

		tools.parallelize(_call_command, commandsInitialFit, n_processes=n_processes, description="combineTool.py (initial fits)")
		tools.parallelize(_call_command, commandsFits, n_processes=1, description="combineTool.py (fits)")
		tools.parallelize(_call_command, commandsOutput, n_processes=1, description="combineTool.py (outputs)")
		tools.parallelize(_call_command, commandsPlot, n_processes=n_processes, description="combineTool.py (plots)")

	def auto_rebin(self, bin_threshold = 1.0, rebin_mode = 0):
		rebin = ch.AutoRebin()
		rebin.SetBinThreshold(bin_threshold)
		rebin.SetRebinMode(rebin_mode)
		rebin.SetPerformRebin(True)
		rebin.SetVerbosity(0)
		rebin.Rebin(self.cb, self.cb)

