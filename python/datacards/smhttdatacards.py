# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.categories as Categories
import HiggsAnalysis.KITHiggsToTauTau.datacards.datacards as datacards
import CombineHarvester.CombineTools.ch as ch
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.systematics_libary as SystLib

class SMHttDatacards(datacards.Datacards):
	def __init__(self, higgs_masses=["125"], ttbarFit=False, mmFit=False, year="", noJECuncSplit=False, cb=None, signal_processes=None):
		super(SMHttDatacards, self).__init__(cb)

		if cb is None:
			if signal_processes is None:
				signal_processes = ["ggH", "qqH", "WH", "ZH"]

			background_processes_mt = ["ZTT", "ZL", "ZJ", "EWKZ", "TTT", "TTJJ", "VV", "W", "QCD"]
			background_processes_et = ["ZTT", "ZL", "ZJ", "EWKZ", "TTT", "TTJJ", "VV", "W", "QCD"]
			background_processes_tt = ["ZTT", "ZL", "ZJ", "EWKZ", "TTT", "TTJJ", "VVT", "VVJ", "W", "QCD"]
			background_processes_em = ["ZTT", "ZLL", "EWKZ", "TT", "VV", "hww_gg125", "hww_qq125", "W", "QCD"]
			background_processes_mm = ["ZLL", "TT", "VV", "W"]
			background_processes_ttbar = ["ZTT", "ZLL", "EWKZ", "TT", "VV", "W", "QCD"]

			all_mc_bkgs = ["ZTT", "ZL", "ZJ", "ZLL", "EWKZ", "TT", "TTT", "TTJJ", "VV", "VVT", "VVJ", "W", "hww_gg125", "hww_qq125"]
			all_mc_bkgs_no_W = ["ZTT", "ZL", "ZJ", "ZLL", "EWKZ", "TT", "TTT", "TTJJ", "VV", "VVT", "VVJ", "hww_gg125", "hww_qq125"]
			all_mc_bkgs_no_TTJ = ["ZTT", "ZL", "ZJ", "ZLL", "EWKZ", "TT", "TTT", "VV", "VVT", "VVJ", "W", "hww_gg125", "hww_qq125"]
			
			# Lists of categories
			CP_categories = ["Vbf3D", "Vbf3D_CP", "Vbf3D_CP_jdeta", "Vbf3D_mela_GGH_DCPPlus", "Vbf3D_mela_GGH_DCPMinus", "TwoJet_CP_mjjlow", "TwoJet_CP_mvislow", "TwoJet_CP_boosted", "TwoJet_CP_mvishigh"]
			sm_categories = ["ZeroJet2D", "Boosted2D", "Vbf2D"]
			##Generate instance of systematic libary, in which the relevant information about the systematics are safed

			systematics_list = SystLib.SystematicLibary()	

			# list of JEC uncertainties
			jecUncertNames = [
				"AbsoluteFlavMap",
				"AbsoluteMPFBias",
				"AbsoluteScale",
				"AbsoluteStat",
				"FlavorQCD",
				"Fragmentation",
				"PileUpDataMC",
				"PileUpPtBB",
				"PileUpPtEC1",
				"PileUpPtEC2",
				"PileUpPtHF",
				"PileUpPtRef",
				"RelativeBal",
				"RelativeFSR",
				"RelativeJEREC1",
				"RelativeJEREC2",
				"RelativeJERHF",
				"RelativePtBB",
				"RelativePtEC1",
				"RelativePtEC2",
				"RelativePtHF",
				"RelativeStatEC",
				"RelativeStatFSR",
				"RelativeStatHF",
				"SinglePionECAL",
				"SinglePionHCAL",
				"TimePtEta"
			]

			# ======================================================================
			# MT channel
			self.add_processes(
					channel="mt",
					categories=Categories.CategoriesDict().getCategories(["mt"])["mt"],
					bkg_processes=background_processes_mt,
					sig_processes=signal_processes,
					analysis=["htt"],
					era=["13TeV"],
					mass=higgs_masses
			)

			# efficiencies
			if year == "2016":
				self.cb.cp().channel(["mt"]).process(signal_processes+all_mc_bkgs_no_W).AddSyst(self.cb, *systematics_list.trigger_efficiency2016_syst_args)
				self.cb.cp().channel(["mt"]).process(signal_processes+all_mc_bkgs_no_W).AddSyst(self.cb, *systematics_list.muon_efficiency2016_syst_args)
				self.cb.cp().channel(["mt"]).process(signal_processes+all_mc_bkgs).AddSyst(self.cb, *systematics_list.tau_efficiency2016_syst_args)
			else:
				self.cb.cp().channel(["mt"]).process(signal_processes+all_mc_bkgs_no_W).AddSyst(self.cb, *systematics_list.muon_efficiency_syst_args)
				self.cb.cp().channel(["mt"]).process(signal_processes+["ZTT", "TTT", "VVT"]).AddSyst(self.cb, *systematics_list.tau_efficiency_syst_args)

			# mu->tau fake ES
			self.cb.cp().channel(["mt"]).process(["ZL"]).AddSyst(self.cb, *systematics_list.zl_shape_1prong_syst_args)
			self.cb.cp().channel(["mt"]).process(["ZL"]).AddSyst(self.cb, *systematics_list.zl_shape_1prong1pizero_syst_args)

			# mu->tau fake rate
			if year == "2016":
				self.cb.cp().channel(["mt"]).process(["ZL"]).bin(["mt_"+category for category in sm_categories+CP_categories]).AddSyst(self.cb, *systematics_list.mFakeTau_1prong_syst_args)
				self.cb.cp().channel(["mt"]).process(["ZL"]).bin(["mt_"+category for category in sm_categories+CP_categories]).AddSyst(self.cb, *systematics_list.mFakeTau_1prong1pizero_syst_args)
			else:
				self.cb.cp().channel(["mt"]).process(["ZL"]).AddSyst(self.cb, *systematics_list.muFakeTau_syst_args)

			# decay mode reweighting
			self.cb.cp().channel(["mt"]).process(["ZTT"]).bin(["mt_ZeroJet2D"]).AddSyst(self.cb, "CMS_tauDMReco_1prong_13TeV", "shape", ch.SystMap()(1.0))
			self.cb.cp().channel(["mt"]).process(["ZTT"]).bin(["mt_ZeroJet2D"]).AddSyst(self.cb, "CMS_tauDMReco_1prong1pizero_13TeV", "shape", ch.SystMap()(1.0))
			self.cb.cp().channel(["mt"]).process(["ZTT"]).bin(["mt_ZeroJet2D"]).AddSyst(self.cb, "CMS_tauDMReco_3prong_13TeV", "shape", ch.SystMap()(1.0))

			# ======================================================================
			# ET channel
			self.add_processes(
					channel="et",
					categories=Categories.CategoriesDict().getCategories(["et"])["et"],
					bkg_processes=background_processes_et,
					sig_processes=signal_processes,
					analysis=["htt"],
					era=["13TeV"],
					mass=higgs_masses
			)

			# efficiencies
			if year == "2016":
				self.cb.cp().channel(["et"]).process(signal_processes+all_mc_bkgs_no_W).AddSyst(self.cb, *systematics_list.trigger_efficiency2016_syst_args)
				self.cb.cp().channel(["et"]).process(signal_processes+all_mc_bkgs_no_W).AddSyst(self.cb, *systematics_list.electron_efficiency2016_syst_args)
				self.cb.cp().channel(["et"]).process(signal_processes+all_mc_bkgs).AddSyst(self.cb, *systematics_list.tau_efficiency2016_syst_args)
			else:
				self.cb.cp().channel(["et"]).process(signal_processes+all_mc_bkgs_no_W).AddSyst(self.cb, *systematics_list.electron_efficiency_syst_args)
				self.cb.cp().channel(["et"]).process(signal_processes+["ZTT", "TTT", "VVT"]).AddSyst(self.cb, *systematics_list.tau_efficiency_syst_args)

			# e->tau fake ES
			self.cb.cp().channel(["et"]).process(["ZL"]).AddSyst(self.cb, *systematics_list.zl_shape_1prong_syst_args)
			self.cb.cp().channel(["et"]).process(["ZL"]).AddSyst(self.cb, *systematics_list.zl_shape_1prong1pizero_syst_args)

			# e->tau fake rate
			if year == "2016":
				self.cb.cp().channel(["et"]).process(["ZL"]).bin(["et_"+category for category in sm_categories+CP_categories]).AddSyst(self.cb, *systematics_list.eFakeTau_1prong_syst_args)
				self.cb.cp().channel(["et"]).process(["ZL"]).bin(["et_"+category for category in sm_categories+CP_categories]).AddSyst(self.cb, *systematics_list.eFakeTau_1prong1pizero_syst_args)
			else:
				self.cb.cp().channel(["et"]).process(["ZL"]).AddSyst(self.cb, *systematics_list.eFakeTau_tight_syst_args)

			# decay mode reweighting
			self.cb.cp().channel(["et"]).process(["ZTT"]).bin(["et_ZeroJet2D"]).AddSyst(self.cb, "CMS_tauDMReco_1prong_13TeV", "shape", ch.SystMap()(1.0))
			self.cb.cp().channel(["et"]).process(["ZTT"]).bin(["et_ZeroJet2D"]).AddSyst(self.cb, "CMS_tauDMReco_1prong1pizero_13TeV", "shape", ch.SystMap()(1.0))
			self.cb.cp().channel(["et"]).process(["ZTT"]).bin(["et_ZeroJet2D"]).AddSyst(self.cb, "CMS_tauDMReco_3prong_13TeV", "shape", ch.SystMap()(1.0))

			# ======================================================================
			# EM channel
			self.add_processes(
					channel="em",
					categories=Categories.CategoriesDict().getCategories(["em"])["em"],
					bkg_processes=background_processes_em,
					sig_processes=signal_processes,
					analysis=["htt"],
					era=["13TeV"],
					mass=higgs_masses
			)

			# efficiencies
			if year == "2016":
				self.cb.cp().channel(["em"]).process(signal_processes+all_mc_bkgs).AddSyst(self.cb, *systematics_list.trigger_efficiency2016_em_syst_args)
				self.cb.cp().channel(["em"]).process(signal_processes+all_mc_bkgs).AddSyst(self.cb, *systematics_list.electron_efficiency2016_syst_args)
				self.cb.cp().channel(["em"]).process(signal_processes+all_mc_bkgs).AddSyst(self.cb, *systematics_list.muon_efficiency2016_syst_args)
			else:
				self.cb.cp().channel(["em"]).process(signal_processes+all_mc_bkgs).AddSyst(self.cb, *systematics_list.electron_efficiency_syst_args)
				self.cb.cp().channel(["em"]).process(signal_processes+all_mc_bkgs).AddSyst(self.cb, *systematics_list.muon_efficiency_syst_args)

			# B-Tag
			if year == "2016":
				self.cb.cp().channel(["em"]).process(["TT", "VV"]).bin(["em_"+category for category in sm_categories+CP_categories]).AddSyst(self.cb, *systematics_list.btag_efficiency2016_syst_args)

			# electron ES
			self.cb.cp().channel(["em"]).process(signal_processes+all_mc_bkgs+["QCD"]).AddSyst(self.cb, *systematics_list.ele_es_syst_args)

			# ======================================================================
			# TT channel
			self.add_processes(
					channel="tt",
					categories=Categories.CategoriesDict().getCategories(["tt"])["tt"],
					bkg_processes=background_processes_tt,
					sig_processes=signal_processes,
					analysis=["htt"],
					era=["13TeV"],
					mass=higgs_masses
			)


			# efficiencies
			if year == "2016":
				self.cb.cp().channel(["tt"]).process(signal_processes+all_mc_bkgs).AddSyst(self.cb, *systematics_list.trigger_efficiency2016_syst_args)
				self.cb.cp().channel(["tt"]).process(signal_processes+all_mc_bkgs).AddSyst(self.cb, *systematics_list.tau_efficiency2016_tt_syst_args)
			else:
				self.cb.cp().channel(["tt"]).process(signal_processes+["ZTT", "TTT", "VVT"]).AddSyst(self.cb, *systematics_list.tau_efficiency_syst_args)

			# ======================================================================
			# MM channel
			self.add_processes(
					channel="mm",
					categories=Categories.CategoriesDict().getCategories(["mm"])["mm"],
					bkg_processes=background_processes_mm,
					sig_processes=signal_processes,
					analysis=["htt"],
					era=["13TeV"],
					mass=higgs_masses
			)

			# efficiencies
			if year == "2016":
				self.cb.cp().channel(["mm"]).process(all_mc_bkgs).AddSyst(self.cb, *systematics_list.muon_efficiency2016_syst_args)
			else:
				self.cb.cp().channel(["mm"]).process(all_mc_bkgs).AddSyst(self.cb, *systematics_list.muon_efficiency_syst_args)

			# ======================================================================
			# ttbar "channel" to extract normalization of ttbar process
			self.add_processes(
					channel="ttbar",
					categories=Categories.CategoriesDict().getCategories(["ttbar"])["ttbar"],
					bkg_processes=background_processes_ttbar,
					sig_processes=signal_processes,
					analysis=["htt"],
					era=["13TeV"],
					mass=higgs_masses
			)

			if year == "2016":
				self.cb.cp().channel(["ttbar"]).process(signal_processes+all_mc_bkgs).AddSyst(self.cb, *systematics_list.trigger_efficiency2016_em_syst_args)
				self.cb.cp().channel(["ttbar"]).process(signal_processes+all_mc_bkgs).AddSyst(self.cb, *systematics_list.electron_efficiency2016_syst_args)
				self.cb.cp().channel(["ttbar"]).process(signal_processes+all_mc_bkgs).AddSyst(self.cb, *systematics_list.muon_efficiency2016_syst_args)

			self.cb.cp().channel(["ttbar"]).bin(["ttbar_TTbarCR"]).process(all_mc_bkgs).AddSyst(self.cb, "CMS_htt_scale_met_13TeV", "lnN", ch.SystMap()(1.01))

			# ======================================================================
			# All channels

			# ======================================================================
			# lumi
			if year == "2016":
				self.cb.cp().process(signal_processes+["VV", "VVT", "VVJ", "hww_gg125", "hww_qq125"]).AddSyst(self.cb, *systematics_list.lumi2016_syst_args)
				if not ttbarFit:
					self.cb.cp().process(["TT", "TTT", "TTJJ"]).AddSyst(self.cb, *systematics_list.lumi2016_syst_args)
				if mmFit:
					self.cb.cp().channel(["mt", "et", "tt", "em", "ttbar"]).process(["ZL", "ZJ", "ZLL"]).AddSyst(self.cb, *systematics_list.lumi2016_syst_args)
					self.cb.cp().channel(["mt", "et"]).process(["ZTT"]).bin([channel + "_" + category + "_" + cr for channel in ["mt", "et"] for category in ["ZeroJet2D", "Boosted2D"] for cr in ["WJCR", "QCDCR"]]).AddSyst(self.cb, *systematics_list.lumi2016_syst_args)
					self.cb.cp().channel(["tt"]).process(["ZTT"]).bin(["tt_" + category + "_QCDCR" for category in sm_categories]).AddSyst(self.cb, *systematics_list.lumi2016_syst_args)
					self.cb.cp().channel(["ttbar"]).process(["ZTT"]).bin(["ttbar_TTbarCR"]).AddSyst(self.cb, *systematics_list.lumi2016_syst_args)
					self.cb.cp().channel(["mm"]).process(["ZTT"]).AddSyst(self.cb, *systematics_list.lumi2016_syst_args)
				self.cb.cp().process(["W"]).channel(["em", "tt", "mm", "ttbar"]).AddSyst(self.cb, *systematics_list.lumi2016_syst_args)
			else:
				self.cb.cp().process(signal_processes+all_mc_bkgs_no_W).AddSyst(self.cb, *systematics_list.lumi_syst_args)
				self.cb.cp().process(["W"]).channel(["em", "tt", "mm"]).AddSyst(self.cb, *systematics_list.lumi_syst_args)

			# ======================================================================
			# cross section
			if mmFit:
				self.cb.cp().channel(["mt", "et", "tt", "em", "ttbar"]).process(["ZL", "ZJ", "ZLL"]).AddSyst(self.cb, *systematics_list.ztt_cross_section_syst_args)
				# add uncertainty for ZTT only in control regions
				self.cb.cp().channel(["mt", "et"]).process(["ZTT"]).bin([channel + "_" + category + "_" + cr for channel in ["mt", "et"] for category in ["ZeroJet2D", "Boosted2D"] for cr in ["WJCR", "QCDCR"]]).AddSyst(self.cb, *systematics_list.ztt_cross_section_syst_args)
				self.cb.cp().channel(["tt"]).process(["ZTT"]).bin(["tt_" + category + "_QCDCR" for category in ["ZeroJet2D", "Boosted2D", "Vbf2D"]]).AddSyst(self.cb, *systematics_list.ztt_cross_section_syst_args)
				self.cb.cp().channel(["ttbar"]).process(["ZTT"]).bin(["ttbar_TTbarCR"]).AddSyst(self.cb, *systematics_list.ztt_cross_section_syst_args)
			else:
				self.cb.cp().channel(["em"]).process(["ZTT", "ZLL", "EWKZ"]).bin(["em_ZeroJet2D"]).AddSyst(self.cb, "CMS_htt_zmm_norm_extrap_0jet_em_13TeV", "lnN", ch.SystMap()(1.07))
				self.cb.cp().channel(["tt"]).process(["ZTT", "ZL", "ZJ", "EWKZ"]).bin(["tt_ZeroJet2D", "tt_ZeroJet2D_QCDCR"]).AddSyst(self.cb, "CMS_htt_zmm_norm_extrap_0jet_tt_13TeV", "lnN", ch.SystMap()(1.07))
				self.cb.cp().channel(["mt", "et"]).process(["ZTT", "ZL", "ZJ", "EWKZ"]).bin(["mt_ZeroJet2D", "mt_ZeroJet2D_WJCR", "mt_ZeroJet2D_QCDCR", "et_ZeroJet2D", "et_ZeroJet2D_WJCR", "et_ZeroJet2D_QCDCR"]).AddSyst(self.cb, "CMS_htt_zmm_norm_extrap_0jet_lt_13TeV", "lnN", ch.SystMap()(1.07))

				self.cb.cp().channel(["em"]).process(["ZTT", "ZLL", "EWKZ"]).bin(["em_Boosted2D"]).AddSyst(self.cb, "CMS_htt_zmm_norm_extrap_boosted_em_13TeV", "lnN", ch.SystMap()(1.07))
				self.cb.cp().channel(["tt"]).process(["ZTT", "ZL", "ZJ", "EWKZ"]).bin(["tt_Boosted2D", "tt_Boosted2D_QCDCR"]).AddSyst(self.cb, "CMS_htt_zmm_norm_extrap_boosted_tt_13TeV", "lnN", ch.SystMap()(1.07))
				self.cb.cp().channel(["mt", "et"]).process(["ZTT", "ZL", "ZJ", "EWKZ"]).bin(["mt_Boosted2D", "mt_Boosted2D_WJCR", "mt_Boosted2D_QCDCR", "et_Boosted2D", "et_Boosted2D_WJCR", "et_Boosted2D_QCDCR"]).AddSyst(self.cb, "CMS_htt_zmm_norm_extrap_boosted_lt_13TeV", "lnN", ch.SystMap()(1.07))

				self.cb.cp().channel(["em"]).process(["ZTT", "ZLL", "EWKZ"]).bin(["em_Vbf2D"]+["em_"+category for category in CP_categories]).AddSyst(self.cb, "CMS_htt_zmm_norm_extrap_VBF_em_13TeV", "lnN", ch.SystMap()(1.15))
				self.cb.cp().channel(["tt"]).process(["ZTT", "ZL", "ZJ", "EWKZ"]).bin(["tt_Vbf2D", "tt_Vbf2D_QCDCR"]+["tt_"+category for category in CP_categories]).AddSyst(self.cb, "CMS_htt_zmm_norm_extrap_VBF_tt_13TeV", "lnN", ch.SystMap()(1.15))
				self.cb.cp().channel(["mt", "et"]).process(["ZTT", "ZL", "ZJ", "EWKZ"]).bin(["mt_Vbf2D", "mt_Vbf3D", "mt_Vbf3D_CP", "mt_Vbf3D_CP_jdeta", "et_Vbf2D", "et_Vbf3D", "et_Vbf3D_CP", "et_Vbf3D_CP_jdeta", "et_TwoJet_CP_boosted", "et_TwoJet_CP_mvishigh", "et_TwoJet_CP_mvislow", "et_TwoJet_CP_mjjlow"]).AddSyst(self.cb, "CMS_htt_zmm_norm_extrap_VBF_lt_13TeV", "lnN", ch.SystMap()(1.10))

				self.cb.cp().channel(["mt", "et", "tt"]).process(["ZTT", "ZL", "ZJ", "EWKZ"]).bin([channel + "_Vbf2D" for channel in ["mt", "et", "tt"]]).AddSyst(self.cb, "CMS_htt_zmumuShape_VBF_13TeV", "shape", ch.SystMap()(1.0))
				self.cb.cp().channel(["tt"]).process(["ZTT", "ZL", "ZJ", "EWKZ"]).bin(["tt_Vbf2D_QCDCR"]).AddSyst(self.cb, "CMS_htt_zmumuShape_VBF_13TeV", "shape", ch.SystMap()(1.0))
				self.cb.cp().channel(["em"]).process(["ZTT", "ZLL"]).bin(["em_Vbf2D", "em_Vbf3D", "em_Vbf3D_CP", "em_Vbf3D_CP_jdeta", "em_TwoJet_CP_boosted", "em_TwoJet_CP_mvishigh", "em_TwoJet_CP_mvislow", "em_TwoJet_CP_mjjlow"]).AddSyst(self.cb, "CMS_htt_zmumuShape_VBF_13TeV", "shape", ch.SystMap()(1.0))
			if not ttbarFit:
				self.cb.cp().process(["TT", "TTT", "TTJJ"]).channel(["mt", "et", "em", "tt"]).AddSyst(self.cb, *systematics_list.ttj_cross_section_syst_args)
			if year == "2016":
				self.cb.cp().process(["VV", "VVT", "VVJ"]).AddSyst(self.cb, *systematics_list.vv_cross_section2016_syst_args)
			else:
				self.cb.cp().process(["VV", "VVT", "VVJ"]).AddSyst(self.cb, *systematics_list.vv_cross_section_syst_args)
			self.cb.cp().process(["W"]).channel(["em"]).AddSyst(self.cb, *systematics_list.htt_jetFakeLep_syst_args)
			self.cb.cp().process(["W"]).channel(["tt", "mm"]).AddSyst(self.cb, *systematics_list.wj_cross_section_syst_args)

			# ======================================================================
			# tau id efficiency
			if year == "2016":
				self.cb.cp().channel(["mt", "et"]).process(signal_processes+all_mc_bkgs).AddSyst(self.cb, *systematics_list.tau_efficiency2016_corr_syst_args)
				self.cb.cp().channel(["tt"]).process(signal_processes+all_mc_bkgs).AddSyst(self.cb, *systematics_list.tau_efficiency2016_tt_corr_syst_args)
			else:
				self.cb.cp().channel(["mt", "et", "tt"]).process(signal_processes+["ZTT", "TTT", "VVT"]).AddSyst(self.cb, *systematics_list.tau_efficiency_corr_syst_args)

			# ======================================================================
			# energy scales

			# tau ES
			self.cb.cp().channel(["mt", "et", "tt"]).process(signal_processes+all_mc_bkgs).AddSyst(self.cb, *systematics_list.scale_t_1prong_syst_args)
			self.cb.cp().channel(["mt", "et", "tt"]).process(signal_processes+all_mc_bkgs).AddSyst(self.cb, *systematics_list.scale_t_3prong_syst_args)
			self.cb.cp().channel(["mt", "et", "tt"]).process(signal_processes+all_mc_bkgs).AddSyst(self.cb, *systematics_list.scale_t_1prong1pizero_syst_args)

			# jet ES
			# TODO: use mix of lnN/shape systematics as done in official analysis?
			if noJECuncSplit:
				self.cb.cp().process(signal_processes+all_mc_bkgs+["QCD"]).bin([channel+"_"+category for channel in ["et", "mt", "tt", "em"] for category in sm_categories+CP_categories]).AddSyst(self.cb, "CMS_scale_j_Total_13TeV", "shape", ch.SystMap()(1.0))
				self.cb.cp().channel(["mt"]).process(signal_processes+all_mc_bkgs).bin(["mt_ZeroJet2D_WJCR", "mt_Boosted2D_WJCR", "mt_ZeroJet2D_QCDCR", "mt_Boosted2D_QCDCR"]).AddSyst(self.cb, "CMS_scale_j_Total_13TeV", "shape", ch.SystMap()(1.0))
				self.cb.cp().channel(["et"]).process(signal_processes+all_mc_bkgs).bin(["et_ZeroJet2D_WJCR", "et_Boosted2D_WJCR", "et_Boosted2D_QCDCR"]).AddSyst(self.cb, "CMS_scale_j_Total_13TeV", "shape", ch.SystMap()(1.0))
				self.cb.cp().channel(["et"]).process(signal_processes+all_mc_bkgs_no_TTJ).bin(["et_ZeroJet2D_QCDCR"]).AddSyst(self.cb, "CMS_scale_j_Total_13TeV", "shape", ch.SystMap()(1.0))
				self.cb.cp().channel(["tt"]).process(signal_processes+all_mc_bkgs).bin(["tt_ZeroJet2D_QCDCR", "tt_Boosted2D_QCDCR", "tt_Vbf2D_QCDCR"]).AddSyst(self.cb, "CMS_scale_j_Total_13TeV", "shape", ch.SystMap()(1.0))
			else:
				for jecUncert in jecUncertNames:
					self.cb.cp().process(signal_processes+all_mc_bkgs+["QCD"]).bin([channel+"_"+category for channel in ["et", "mt", "tt", "em"] for category in sm_categories+CP_categories]).AddSyst(self.cb, "CMS_scale_j_"+jecUncert+"_13TeV", "shape", ch.SystMap()(1.0))
					self.cb.cp().channel(["mt"]).process(signal_processes+all_mc_bkgs).bin(["mt_ZeroJet2D_WJCR", "mt_Boosted2D_WJCR", "mt_ZeroJet2D_QCDCR", "mt_Boosted2D_QCDCR"]).AddSyst(self.cb, "CMS_scale_j_"+jecUncert+"_13TeV", "shape", ch.SystMap()(1.0))
					self.cb.cp().channel(["et"]).process(signal_processes+all_mc_bkgs).bin(["et_ZeroJet2D_WJCR", "et_Boosted2D_WJCR", "et_Boosted2D_QCDCR"]).AddSyst(self.cb, "CMS_scale_j_"+jecUncert+"_13TeV", "shape", ch.SystMap()(1.0))
					self.cb.cp().channel(["et"]).process(signal_processes+all_mc_bkgs_no_TTJ).bin(["et_ZeroJet2D_QCDCR"]).AddSyst(self.cb, "CMS_scale_j_"+jecUncert+"_13TeV", "shape", ch.SystMap()(1.0))
					self.cb.cp().channel(["tt"]).process(signal_processes+all_mc_bkgs).bin(["tt_ZeroJet2D_QCDCR", "tt_Boosted2D_QCDCR", "tt_Vbf2D_QCDCR"]).AddSyst(self.cb, "CMS_scale_j_"+jecUncert+"_13TeV", "shape", ch.SystMap()(1.0))

			# jet->tau fake ES
			if year == "2016":
				self.cb.cp().channel(["et", "mt", "tt"]).process(["ZJ", "TTJJ", "VVJ"]).AddSyst(self.cb, "CMS_htt_jetToTauFake_13TeV", "shape", ch.SystMap()(1.0))
				self.cb.cp().channel(["et", "mt", "tt"]).process(["W"]).bin([channel+"_"+category for channel in ["et", "mt", "tt"] for category in sm_categories+CP_categories]).AddSyst(self.cb, "CMS_htt_jetToTauFake_13TeV", "shape", ch.SystMap()(1.0))
				self.cb.cp().channel(["et", "mt"]).process(["W"]).bin([channel+"_"+category for channel in ["et", "mt"] for category in ["ZeroJet2D_QCDCR", "Boosted2D_QCDCR"]]).AddSyst(self.cb, "CMS_htt_jetToTauFake_13TeV", "shape", ch.SystMap()(1.0))
			else:
				self.cb.cp().channel(["et", "mt", "tt"]).process(["ZJ", "W", "TTJJ", "VVJ"]).AddSyst(self.cb, *systematics_list.jetFakeTau_syst_args)

			# MET ES
			self.cb.cp().channel(["et", "mt", "tt", "em"]).process(signal_processes+all_mc_bkgs).bin([channel+"_"+category for channel in ["et", "mt", "tt", "em"] for category in sm_categories+CP_categories]).AddSyst(self.cb, "CMS_scale_met_clustered_13TeV", "shape", ch.SystMap()(1.0))
			self.cb.cp().channel(["et", "mt", "tt", "em"]).process(signal_processes+all_mc_bkgs).bin([channel+"_"+category for channel in ["et", "mt", "tt", "em"] for category in sm_categories+CP_categories]).AddSyst(self.cb, "CMS_scale_met_unclustered_13TeV", "shape", ch.SystMap()(1.0))
			self.cb.cp().channel(["et", "mt"]).process(all_mc_bkgs).bin([channel+"_"+category for channel in ["et", "mt"] for category in ["ZeroJet2D_WJCR", "ZeroJet2D_QCDCR", "Boosted2D_WJCR", "Boosted2D_QCDCR"]]).AddSyst(self.cb, "CMS_scale_met_clustered_13TeV", "shape", ch.SystMap()(1.0))
			self.cb.cp().channel(["et", "mt"]).process(all_mc_bkgs).bin([channel+"_"+category for channel in ["et", "mt"] for category in ["ZeroJet2D_WJCR", "ZeroJet2D_QCDCR", "Boosted2D_WJCR", "Boosted2D_QCDCR"]]).AddSyst(self.cb, "CMS_scale_met_unclustered_13TeV", "shape", ch.SystMap()(1.0))

			# ======================================================================
			# W+jets and QCD estimation uncertainties

			# QCD normalization
			self.cb.cp().channel(["em"]).process(["QCD"]).bin(["em_ZeroJet2D"]).AddSyst(self.cb, *systematics_list.htt_QCD_0jet_syst_args)
			self.cb.cp().channel(["em"]).process(["QCD"]).bin(["em_Boosted2D"]).AddSyst(self.cb, *systematics_list.htt_QCD_boosted_syst_args)
			self.cb.cp().channel(["em"]).process(["QCD"]).bin(["em_Vbf2D", "em_Vbf3D", "em_Vbf3D_CP", "em_Vbf3D_CP_jdeta", "em_TwoJet_CP_boosted", "em_TwoJet_CP_mvishigh", "em_TwoJet_CP_mvislow", "em_TwoJet_CP_mjjlow"]).AddSyst(self.cb, "CMS_htt_QCD_VBF_em_13TeV", "lnN", ch.SystMap()(1.20))

			self.cb.cp().channel(["tt"]).process(["QCD"]).bin(["tt_ZeroJet2D"]).AddSyst(self.cb, "CMS_htt_QCD_0jet_tt_13TeV", "lnN", ch.SystMap()(1.027))
			self.cb.cp().channel(["tt"]).process(["QCD"]).bin(["tt_Boosted2D"]).AddSyst(self.cb, "CMS_htt_QCD_boosted_tt_13TeV", "lnN", ch.SystMap()(1.027))
			self.cb.cp().channel(["tt"]).process(["QCD"]).bin(["tt_Vbf2D", "tt_Vbf3D", "tt_Vbf3D_CP", "tt_Vbf3D_CP_jdeta", "tt_TwoJet_CP_boosted", "tt_TwoJet_CP_mvishigh", "tt_TwoJet_CP_mvislow", "tt_TwoJet_CP_mjjlow"]).AddSyst(self.cb, "CMS_htt_QCD_VBF_tt_13TeV", "lnN", ch.SystMap()(1.15))

			self.cb.cp().channel(["mt"]).process(["QCD"]).bin(["mt_"+category for category in sm_categories+CP_categories]).AddSyst(self.cb, *systematics_list.QCD_Extrap_Iso_nonIso_syst_args)
			self.cb.cp().channel(["et"]).process(["QCD"]).bin(["et_"+category for category in sm_categories+CP_categories]).AddSyst(self.cb, *systematics_list.QCD_Extrap_Iso_nonIso_syst_args)

			self.cb.cp().channel(["et", "mt"]).process(["QCD"]).bin([channel+"_ZeroJet2D" for channel in ["et", "mt"]]).AddSyst(self.cb, "WSFUncert_$CHANNEL_0jet_13TeV", "shape", ch.SystMap()(1.0))			
			self.cb.cp().channel(["et", "mt"]).process(["QCD"]).bin([channel+"_Boosted2D" for channel in ["et", "mt"]]).AddSyst(self.cb, "WSFUncert_$CHANNEL_boosted_13TeV", "shape", ch.SystMap()(1.0))
			self.cb.cp().channel(["et", "mt"]).process(["QCD"]).bin([channel+"_Vbf2D" for channel in ["et", "mt"]]).AddSyst(self.cb, "WSFUncert_$CHANNEL_vbf_13TeV", "shape", ch.SystMap()(1.0))

			# W+jets high->low mt extrapolation uncertainty
			self.cb.cp().channel(["et", "mt"]).process(["W"]).bin([channel+"_ZeroJet2D" for channel in ["et", "mt"]]).AddSyst(self.cb, *systematics_list.WHighMTtoLowMT_0jet_syst_args)
			self.cb.cp().channel(["et", "mt"]).process(["W"]).bin([channel+"_Boosted2D" for channel in ["et", "mt"]]).AddSyst(self.cb, *systematics_list.WHighMTtoLowMT_boosted_syst_args)
			self.cb.cp().channel(["et", "mt"]).process(["W"]).bin([channel+"_Vbf2D" for channel in ["et", "mt"]]).AddSyst(self.cb, "WHighMTtoLowMT_vbf_13TeV", "lnN", ch.SystMap()(1.10))
			self.cb.cp().channel(["et", "mt"]).process(["W"]).bin([channel+"_Vbf3D" for channel in ["et", "mt"]]).AddSyst(self.cb, "WHighMTtoLowMT_vbf_13TeV", "lnN", ch.SystMap()(1.10))
			self.cb.cp().channel(["et", "mt"]).process(["W"]).bin([channel+"_Vbf3D_CP" for channel in ["et", "mt"]]).AddSyst(self.cb, "WHighMTtoLowMT_vbf_13TeV", "lnN", ch.SystMap()(1.10))
			self.cb.cp().channel(["et", "mt"]).process(["W"]).bin([channel+"_Vbf3D_CP_jdeta" for channel in ["et", "mt"]]).AddSyst(self.cb, "WHighMTtoLowMT_vbf_13TeV", "lnN", ch.SystMap()(1.10))

			# ======================================================================
			# pt reweighting uncertainties

			# ttbar shape
			self.cb.cp().channel(["et", "mt", "em", "tt"]).process(["TTT", "TTJJ"]).AddSyst(self.cb, *systematics_list.ttj_syst_args)
			self.cb.cp().channel(["em"]).process(["TT"]).AddSyst(self.cb, *systematics_list.ttj_syst_args)

			# dy shape
			self.cb.cp().channel(["et", "mt", "tt"]).process(["ZTT", "ZL", "ZJ"]).AddSyst(self.cb, *systematics_list.dy_shape_syst_args)
			self.cb.cp().channel(["em"]).process(["ZTT", "ZLL"]).AddSyst(self.cb, *systematics_list.dy_shape_syst_args)

			# ======================================================================
			# Theory uncertainties
			self.cb.cp().channel(["mt", "et", "tt", "em"]).process(["ggH", "ggHsm", "ggHps", "ggHmm"]).bin([channel+"_"+category for channel in ["et", "mt", "em", "tt"] for category in sm_categories+CP_categories]).AddSyst(self.cb, "CMS_scale_gg_13TeV", "shape", ch.SystMap()(1.0))
			self.cb.cp().process(["qqH", "qqHsm", "qqHps", "qqHmm"]).AddSyst(self.cb, *systematics_list.htt_qcd_scale_qqh_syst_args)
			self.cb.cp().process(["ggH", "ggHsm", "ggHps", "ggHmm", "qqH", "qqHsm", "qqHps", "qqHmm"]).AddSyst(self.cb, *systematics_list.htt_pdf_scale_smhtt_syst_args)
			self.cb.cp().process(["ggH", "ggHsm", "ggHps", "ggHmm", "qqH", "qqHsm", "qqHps", "qqHmm"]).AddSyst(self.cb, *systematics_list.htt_ueps_smhtt_syst_args)

			# Uncertainty on BR of HTT @ 125 GeV
			self.cb.cp().signals().AddSyst(self.cb, "BR_htt_THU", "lnN", ch.SystMap()(1.017))
			self.cb.cp().signals().AddSyst(self.cb, "BR_htt_PU_mq", "lnN", ch.SystMap()(1.0099))
			self.cb.cp().signals().AddSyst(self.cb, "BR_htt_PU_alphas", "lnN", ch.SystMap()(1.0062))

			# Uncertainty on BR of HWW @ 125 GeV
			self.cb.cp().process(["hww_gg125", "hww_qq125"]).AddSyst(self.cb, "BR_hww_THU", "lnN", ch.SystMap()(1.0099))
			self.cb.cp().process(["hww_gg125", "hww_qq125"]).AddSyst(self.cb, "BR_hww_PU_mq", "lnN", ch.SystMap()(1.0099))
			self.cb.cp().process(["hww_gg125", "hww_qq125"]).AddSyst(self.cb, "BR_hww_PU_alphas", "lnN", ch.SystMap()(1.0066))

			self.cb.cp().process(["ggH", "ggHsm", "ggHps", "ggHmm", "hww_gg125"]).AddSyst(self.cb, "QCDScale_ggH", "lnN", ch.SystMap()(1.039))
			self.cb.cp().process(["qqH", "qqHsm", "qqHps", "qqHmm", "hww_qq125"]).AddSyst(self.cb, "QCDScale_qqH", "lnN", ch.SystMap()(1.004))
			self.cb.cp().process(["WH"]).AddSyst(self.cb, "QCDScale_VH", "lnN", ch.SystMap()(1.007))
			self.cb.cp().process(["ZH"]).AddSyst(self.cb, "QCDScale_VH", "lnN", ch.SystMap()(1.038))

			self.cb.cp().process(["ggH", "ggHsm", "ggHps", "ggHmm", "hww_gg125"]).AddSyst(self.cb, "pdf_Higgs_gg", "lnN", ch.SystMap()(1.032))
			self.cb.cp().process(["qqH", "qqHsm", "qqHps", "qqHmm", "hww_qq125"]).AddSyst(self.cb, "pdf_Higgs_qq", "lnN", ch.SystMap()(1.021))
			self.cb.cp().process(["WH"]).AddSyst(self.cb, "pdf_Higgs_VH", "lnN", ch.SystMap()(1.019))
			self.cb.cp().process(["ZH"]).AddSyst(self.cb, "pdf_Higgs_VH", "lnN", ch.SystMap()(1.016))

			# ======================================================================
			# ttbar rate parameters
			if ttbarFit:
				self.cb.cp().process(["TTT", "TTJJ"]).bin(["mt_ZeroJet2D"]).AddSyst(self.cb, "rate_ttbar", "rateParam", ch.SystMap()(1.0))
				self.cb.cp().process(["TTT", "TTJJ"]).bin(["et_ZeroJet2D"]).AddSyst(self.cb, "rate_ttbar", "rateParam", ch.SystMap()(1.0))
				self.cb.cp().process(["TTT", "TTJJ"]).bin(["tt_ZeroJet2D"]).AddSyst(self.cb, "rate_ttbar", "rateParam", ch.SystMap()(1.0))
				self.cb.cp().process(["TT"]).bin(["em_ZeroJet2D"]).AddSyst(self.cb, "rate_ttbar", "rateParam", ch.SystMap()(1.0))

				self.cb.cp().process(["TTT", "TTJJ"]).bin(["mt_Boosted2D"]).AddSyst(self.cb, "rate_ttbar", "rateParam", ch.SystMap()(1.0))
				self.cb.cp().process(["TTT", "TTJJ"]).bin(["et_Boosted2D"]).AddSyst(self.cb, "rate_ttbar", "rateParam", ch.SystMap()(1.0))
				self.cb.cp().process(["TTT", "TTJJ"]).bin(["tt_Boosted2D"]).AddSyst(self.cb, "rate_ttbar", "rateParam", ch.SystMap()(1.0))
				self.cb.cp().process(["TT"]).bin(["em_Boosted2D"]).AddSyst(self.cb, "rate_ttbar", "rateParam", ch.SystMap()(1.0))

				self.cb.cp().process(["TTT", "TTJJ"]).bin(["mt_Vbf2D", "mt_Vbf3D"]).AddSyst(self.cb, "rate_ttbar", "rateParam", ch.SystMap()(1.0))
				self.cb.cp().process(["TTT", "TTJJ"]).bin(["et_Vbf2D", "et_Vbf3D"]).AddSyst(self.cb, "rate_ttbar", "rateParam", ch.SystMap()(1.0))
				self.cb.cp().process(["TTT", "TTJJ"]).bin(["tt_Vbf2D", "tt_Vbf3D"]).AddSyst(self.cb, "rate_ttbar", "rateParam", ch.SystMap()(1.0))
				self.cb.cp().process(["TT"]).bin(["em_Vbf2D", "em_Vbf3D"]).AddSyst(self.cb, "rate_ttbar", "rateParam", ch.SystMap()(1.0))

				self.cb.cp().process(["TT"]).bin(["ttbar_TTbarCR"]).AddSyst(self.cb, "rate_ttbar", "rateParam", ch.SystMap()(1.0))

				self.cb.cp().GetParameter("rate_ttbar").set_range(0.8, 1.2)

			# ======================================================================
			# mm rate parameters
			if mmFit:
				self.cb.cp().process(["ZTT"]).bin(["mt_ZeroJet2D"]).AddSyst(self.cb, "rate_mm_ZTT_0jet", "rateParam", ch.SystMap()(1.0))
				self.cb.cp().process(["ZTT"]).bin(["et_ZeroJet2D"]).AddSyst(self.cb, "rate_mm_ZTT_0jet", "rateParam", ch.SystMap()(1.0))
				self.cb.cp().process(["ZTT"]).bin(["tt_ZeroJet2D"]).AddSyst(self.cb, "rate_mm_ZTT_0jet", "rateParam", ch.SystMap()(1.0))
				self.cb.cp().process(["ZTT"]).bin(["em_ZeroJet2D"]).AddSyst(self.cb, "rate_mm_ZTT_0jet", "rateParam", ch.SystMap()(1.0))
				self.cb.cp().process(["ZLL"]).bin(["mm_ZeroJet2D"]).AddSyst(self.cb, "rate_mm_ZTT_0jet", "rateParam", ch.SystMap()(1.0))

				self.cb.cp().process(["ZTT"]).bin(["mt_Boosted2D"]).AddSyst(self.cb, "rate_mm_ZTT_boosted", "rateParam", ch.SystMap()(1.0))
				self.cb.cp().process(["ZTT"]).bin(["et_Boosted2D"]).AddSyst(self.cb, "rate_mm_ZTT_boosted", "rateParam", ch.SystMap()(1.0))
				self.cb.cp().process(["ZTT"]).bin(["tt_Boosted2D"]).AddSyst(self.cb, "rate_mm_ZTT_boosted", "rateParam", ch.SystMap()(1.0))
				self.cb.cp().process(["ZTT"]).bin(["em_Boosted2D"]).AddSyst(self.cb, "rate_mm_ZTT_boosted", "rateParam", ch.SystMap()(1.0))
				self.cb.cp().process(["ZLL"]).bin(["mm_Boosted2D"]).AddSyst(self.cb, "rate_mm_ZTT_boosted", "rateParam", ch.SystMap()(1.0))

				self.cb.cp().process(["ZTT"]).bin(["mt_Vbf2D", "mt_Vbf3D"]).AddSyst(self.cb, "rate_mm_ZTT_vbf", "rateParam", ch.SystMap()(1.0))
				self.cb.cp().process(["ZTT"]).bin(["et_Vbf2D", "et_Vbf3D"]).AddSyst(self.cb, "rate_mm_ZTT_vbf", "rateParam", ch.SystMap()(1.0))
				self.cb.cp().process(["ZTT"]).bin(["tt_Vbf2D", "tt_Vbf3D"]).AddSyst(self.cb, "rate_mm_ZTT_vbf", "rateParam", ch.SystMap()(1.0))
				self.cb.cp().process(["ZTT"]).bin(["em_Vbf2D", "em_Vbf3D"]).AddSyst(self.cb, "rate_mm_ZTT_vbf", "rateParam", ch.SystMap()(1.0))
				self.cb.cp().process(["ZLL"]).bin(["mm_Vbf2D"]).AddSyst(self.cb, "rate_mm_ZTT_vbf", "rateParam", ch.SystMap()(1.0))

				self.cb.cp().GetParameter("rate_mm_ZTT_0jet").set_range(0.9, 1.1)
				self.cb.cp().GetParameter("rate_mm_ZTT_boosted").set_range(0.9, 1.1)
				self.cb.cp().GetParameter("rate_mm_ZTT_vbf").set_range(0.9, 1.1)

			# ======================================================================
			# control region rate parameters
			self.cb.cp().process(["W"]).bin(["mt_ZeroJet2D", "mt_ZeroJet2D_WJCR"]).AddSyst(self.cb, "rate_W_cr_0jet_mt", "rateParam", ch.SystMap()(1.0))
			self.cb.cp().process(["W"]).bin(["mt_Boosted2D", "mt_Boosted2D_WJCR", "mt_Vbf2D", "mt_Vbf3D"]).AddSyst(self.cb, "rate_W_cr_boosted_mt", "rateParam", ch.SystMap()(1.0))
			self.cb.cp().process(["W"]).bin(["et_ZeroJet2D", "et_ZeroJet2D_WJCR"]).AddSyst(self.cb, "rate_W_cr_0jet_et", "rateParam", ch.SystMap()(1.0))
			self.cb.cp().process(["W"]).bin(["et_Boosted2D", "et_Boosted2D_WJCR", "et_Vbf2D", "et_Vbf3D"]).AddSyst(self.cb, "rate_W_cr_boosted_et", "rateParam", ch.SystMap()(1.0))

			self.cb.cp().process(["QCD"]).bin(["mt_ZeroJet2D", "mt_ZeroJet2D_QCDCR"]).AddSyst(self.cb, "rate_QCD_cr_0jet_mt", "rateParam", ch.SystMap()(1.0))
			self.cb.cp().process(["QCD"]).bin(["mt_Boosted2D", "mt_Boosted2D_QCDCR", "mt_Vbf2D", "mt_Vbf3D"]).AddSyst(self.cb, "rate_QCD_cr_boosted_mt", "rateParam", ch.SystMap()(1.0))
			self.cb.cp().process(["QCD"]).bin(["et_ZeroJet2D", "et_ZeroJet2D_QCDCR"]).AddSyst(self.cb, "rate_QCD_cr_0jet_et", "rateParam", ch.SystMap()(1.0))
			self.cb.cp().process(["QCD"]).bin(["et_Boosted2D", "et_Boosted2D_QCDCR", "et_Vbf2D", "et_Vbf3D"]).AddSyst(self.cb, "rate_QCD_cr_boosted_et", "rateParam", ch.SystMap()(1.0))
			self.cb.cp().process(["QCD"]).bin(["tt_ZeroJet2D", "tt_ZeroJet2D_QCDCR"]).AddSyst(self.cb, "rate_QCD_cr_0jet_tt", "rateParam", ch.SystMap()(1.0))
			self.cb.cp().process(["QCD"]).bin(["tt_Boosted2D", "tt_Boosted2D_QCDCR"]).AddSyst(self.cb, "rate_QCD_cr_boosted_tt", "rateParam", ch.SystMap()(1.0))
			self.cb.cp().process(["QCD"]).bin(["tt_Vbf2D", "tt_Vbf3D", "tt_Vbf3D_CP", "tt_Vbf3D_CP_jdeta", "tt_Vbf2D_QCDCR"]).AddSyst(self.cb, "rate_QCD_cr_vbf_tt", "rateParam", ch.SystMap()(1.0))

			self.cb.cp().GetParameter("rate_W_cr_0jet_mt").set_range(0, 5)
			self.cb.cp().GetParameter("rate_W_cr_boosted_mt").set_range(0, 5)
			self.cb.cp().GetParameter("rate_W_cr_0jet_et").set_range(0, 5)
			self.cb.cp().GetParameter("rate_W_cr_boosted_et").set_range(0, 5)

			self.cb.cp().GetParameter("rate_QCD_cr_0jet_mt").set_range(0, 5)
			self.cb.cp().GetParameter("rate_QCD_cr_boosted_mt").set_range(0, 5)
			self.cb.cp().GetParameter("rate_QCD_cr_0jet_et").set_range(0, 5)
			self.cb.cp().GetParameter("rate_QCD_cr_boosted_et").set_range(0, 5)
			self.cb.cp().GetParameter("rate_QCD_cr_0jet_tt").set_range(0, 5)
			self.cb.cp().GetParameter("rate_QCD_cr_boosted_tt").set_range(0, 5)
			self.cb.cp().GetParameter("rate_QCD_cr_vbf_tt").set_range(0, 5)

			# ======================================================================

			if log.isEnabledFor(logging.DEBUG):
				self.cb.PrintAll()

# simplified version just for the purpose of datacard synchronization (no systematics)
class SMHttDatacardsForSync(datacards.Datacards):
	def __init__(self, higgs_masses=["125"], cb=None):
		super(SMHttDatacardsForSync, self).__init__(cb)

		if cb is None:
			signal_processes = ["ggH", "qqH", "WH", "ZH"]

			background_processes_mt = ["ZTT", "ZL", "ZJ", "EWKZ", "TTT", "TTJJ", "VV", "W", "QCD"]
			background_processes_et = ["ZTT", "ZL", "ZJ", "EWKZ", "TTT", "TTJJ", "VV", "W", "QCD"]
			background_processes_tt = ["ZTT", "ZL", "ZJ", "EWKZ", "TTT", "TTJJ", "VVT", "VVJ", "W", "QCD"]
			background_processes_em = ["ZTT", "ZLL", "EWKZ", "TT", "VV", "hww_gg125", "hww_qq125", "W", "QCD"]
			background_processes_mm = ["ZLL", "TT", "VV", "W"]
			background_processes_ttbar = ["ZTT", "ZLL", "EWKZ", "TT", "VV", "W", "QCD"]

			# ======================================================================
			# MT channel
			self.add_processes(
					channel="mt",
					categories=Categories.CategoriesDict().getCategories(["mt"])["mt"],
					bkg_processes=background_processes_mt,
					sig_processes=signal_processes,
					analysis=["htt"],
					era=["13TeV"],
					mass=higgs_masses
			)

			# ======================================================================
			# ET channel
			self.add_processes(
					channel="et",
					categories=Categories.CategoriesDict().getCategories(["et"])["et"],
					bkg_processes=background_processes_et,
					sig_processes=signal_processes,
					analysis=["htt"],
					era=["13TeV"],
					mass=higgs_masses
			)

			# ======================================================================
			# EM channel
			self.add_processes(
					channel="em",
					categories=Categories.CategoriesDict().getCategories(["em"])["em"],
					bkg_processes=background_processes_em,
					sig_processes=signal_processes,
					analysis=["htt"],
					era=["13TeV"],
					mass=higgs_masses
			)

			# ======================================================================
			# TT channel
			self.add_processes(
					channel="tt",
					categories=Categories.CategoriesDict().getCategories(["tt"])["tt"],
					bkg_processes=background_processes_tt,
					sig_processes=signal_processes,
					analysis=["htt"],
					era=["13TeV"],
					mass=higgs_masses
			)

			# ======================================================================
			# MM channel
			self.add_processes(
					channel="mm",
					categories=Categories.CategoriesDict().getCategories(["mm"])["mm"],
					bkg_processes=background_processes_mm,
					sig_processes=signal_processes,
					analysis=["htt"],
					era=["13TeV"],
					mass=higgs_masses
			)

			# ======================================================================
			# ttbar "channel" to extract normalization of ttbar process
			self.add_processes(
					channel="ttbar",
					categories=Categories.CategoriesDict().getCategories(["ttbar"])["ttbar"],
					bkg_processes=background_processes_ttbar,
					sig_processes=signal_processes,
					analysis=["htt"],
					era=["13TeV"],
					mass=higgs_masses
			)

			if log.isEnabledFor(logging.DEBUG):
				self.cb.PrintAll()
