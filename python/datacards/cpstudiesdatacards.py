# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import HiggsAnalysis.KITHiggsToTauTau.datacards.datacards as datacards
import HiggsAnalysis.KITHiggsToTauTau.datacards.smhttdatacards as smhttdatacards
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.systematics_libary as SystLib
import CombineHarvester.CombineTools.ch as ch


#TODO: Class should be editing such that it is derived from smhttdatacards. Currently it
# is just copied from there.

class CPStudiesDatacards(datacards.Datacards):
	def __init__(self, cp_mixing_angles_over_pi_half=[], higgs_masses=["125"], year="2016", add_data=True, cb=None):
		super(CPStudiesDatacards, self).__init__(cb)

		if cb is None:
			signal_processes = ["ggH", "qqH", "VH", "WH"]


			#background_processes_tt = ["ZTT", "ZLL", "QCD"]
			background_processes_mt = ["ZTT", "ZL", "ZJ", "EWKZ", "TTT", "TTJJ", "VV", "W", "QCD"]
			background_processes_et = ["ZTT", "ZL", "ZJ", "EWKZ", "TTT", "TTJJ", "VV", "W", "QCD"]
			#background_processes_tt = ["ZTT", "ZL", "ZJ", "EWKZ", "TTT", "TTJJ", "VVT", "VVJ", "W", "QCD"]
			background_processes_tt = ["ZTT", "ZLL", "TTJJ", "QCD"]
			background_processes_em = ["ZTT", "ZLL", "EWKZ", "TT", "VV", "hww_gg125", "hww_qq125", "W", "QCD"]
			background_processes_mm = ["ZLL", "TT", "VV", "W"]
			all_mc_bkgs = ["ZTT", "ZL", "ZJ", "ZLL", "TT", "TTT", "TTJJ", "VV", "VVT", "VVJ", "W", "hww_gg125", "hww_qq125"]
			all_mc_bkgs_no_W = ["ZTT", "ZL", "ZJ", "ZLL", "EWKZ", "TT", "TTT", "TTJJ", "VV", "VVT", "VVJ", "hww_gg125", "hww_qq125"]
			all_mc_bkgs_no_TTJ = ["ZTT", "ZL", "ZJ", "ZLL", "EWKZ", "TT", "TTT", "VV", "VVT", "VVJ", "W", "hww_gg125", "hww_qq125"]


			##Generate instance of systematic libary, in which the relevant information about the systematics are safed

			systematics_list = SystLib.SystematicLibary()

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
					#categories=["mt_"+category for category in ["0jet_low", "0jet_high", "1jet_low", "1jet_high", "2jet_vbf"]],
					categories=["mt_"+category for category in ["CP_mt"]],
					bkg_processes=["ZTT", "ZLL"],
					sig_processes=signal_processes,
					analysis=["htt"],
					era=["13TeV"],
					mass=cp_mixing_angles_over_pi_half,
					add_data=add_data
			)

			# efficiencies
			self.cb.cp().channel(["mt"]).process(["ZTT", "ZLL"]).AddSyst(self.cb, *systematics_list.muon_efficiency2016_syst_args)
			self.cb.cp().channel(["mt"]).signals().AddSyst(self.cb, *systematics_list.muon_efficiency2016_syst_args)

			self.cb.cp().channel(["mt"]).process(["ZTT"]).AddSyst(self.cb, *systematics_list.tau_efficiency2016_syst_args)
			self.cb.cp().channel(["mt"]).signals().AddSyst(self.cb, *systematics_list.tau_efficiency2016_syst_args)
			self.cb.cp().channel(["mt"]).process(["ZTT"]).AddSyst(self.cb, *systematics_list.tau_efficiency2016_corr_syst_args)
			self.cb.cp().channel(["mt"]).signals().AddSyst(self.cb, *systematics_list.tau_efficiency2016_corr_syst_args)

			# Tau ES
			self.cb.cp().channel(["mt"]).process(["ZTT"]).AddSyst(self.cb, *systematics_list.tau_es_syst_args)
			self.cb.cp().channel(["mt"]).signals().AddSyst(self.cb, *systematics_list.tau_es_syst_args)

			# fake-rate
			self.cb.cp().channel(["mt"]).process(["ZLL"]).AddSyst(self.cb, *systematics_list.zllFakeTau_syst_args)

			# ======================================================================
			# ET channel
			self.add_processes(
					channel="et",
					#categories=["et_"+category for category in ["0jet_low", "0jet_high", "1jet_low", "1jet_high", "2jet_vbf"]],
					categories=["et_"+category for category in ["CP_et"]],
					bkg_processes=["ZTT", "ZLL"],
					sig_processes=signal_processes,
					analysis=["htt"],
					era=["13TeV"],
					mass=cp_mixing_angles_over_pi_half,
					add_data=add_data
			)

			# efficiencies
			self.cb.cp().channel(["et"]).process(["ZTT", "ZLL"]).AddSyst(self.cb, *systematics_list.electron_efficiency2016_syst_args)
			self.cb.cp().channel(["et"]).signals().AddSyst(self.cb, *systematics_list.electron_efficiency2016_syst_args)

			self.cb.cp().channel(["et"]).process(["ZTT"]).AddSyst(self.cb, *systematics_list.tau_efficiency2016_syst_args)
			self.cb.cp().channel(["et"]).signals().AddSyst(self.cb, *systematics_list.tau_efficiency2016_syst_args)

			# Tau ES
			self.cb.cp().channel(["et"]).process(["ZTT"]).AddSyst(self.cb, *systematics_list.tau_es_syst_args)
			self.cb.cp().channel(["et"]).signals().AddSyst(self.cb, *systematics_list.tau_es_syst_args)

			# fake-rate
			self.cb.cp().channel(["et"]).process(["ZLL"]).AddSyst(self.cb, *systematics_list.zllFakeTau_syst_args)

			# ======================================================================
			# EM channel
			self.add_processes(
					channel="em",
					#categories=["em_"+category for category in ["0jet_low", "0jet_high", "1jet_low", "1jet_high", "2jet_vbf"]],
					categories=["em_"+category for category in ["CP_em"]],
					bkg_processes=["ZTT", "ZLL"],
					sig_processes=signal_processes,
					analysis=["htt"],
					era=["13TeV"],
					mass=cp_mixing_angles_over_pi_half,
					add_data=add_data
			)

			# efficiencies
			self.cb.cp().channel(["em"]).process(["ZTT", "ZLL"]).AddSyst(self.cb, *systematics_list.electron_efficiency2016_syst_args)
			self.cb.cp().channel(["em"]).signals().AddSyst(self.cb, *systematics_list.electron_efficiency2016_syst_args)

			self.cb.cp().channel(["em"]).process(["ZTT", "ZLL"]).AddSyst(self.cb, *systematics_list.muon_efficiency2016_syst_args)
			self.cb.cp().channel(["em"]).signals().AddSyst(self.cb, *systematics_list.muon_efficiency2016_syst_args)

			# ======================================================================
			# TT channel
			self.add_processes(
					channel="tt",
					categories=["tt_"+category for category in ["CP_tt"]],
					bkg_processes=["ZTT", "ZLL"],
					sig_processes=signal_processes,
					analysis=["htt"],
					era=["13TeV"],
					mass=cp_mixing_angles_over_pi_half,
					add_data=add_data
			)

			# TT channel for rho analysis
			# TODO: There are 3 different processes here. -> Merge to one. 
			self.add_processes(
					channel="tt",
					categories=["tt_"+category for category in ["CP_rho_merged"]],
					bkg_processes=background_processes_tt,
					sig_processes=signal_processes,
					analysis=["htt"],
					era=["13TeV"],
					mass=cp_mixing_angles_over_pi_half,
					add_data=add_data
			)

			self.add_processes(
					channel="tt",
					categories=["tt_"+category for category in ["CP_rho_yLhigh"]],
					bkg_processes=background_processes_tt,
					sig_processes=signal_processes,
					analysis=["htt"],
					era=["13TeV"],
					mass=cp_mixing_angles_over_pi_half,
					add_data=add_data
			)

			self.add_processes(
					channel="tt",
					categories=["tt_"+category for category in ["CP_rho_yLlow"]],
					bkg_processes=background_processes_tt,
					sig_processes=signal_processes,
					analysis=["htt"],
					era=["13TeV"],
					mass=cp_mixing_angles_over_pi_half,
					add_data=add_data
			)

			# efficiencies
			if year == "2016":
				self.cb.cp().channel(["tt"]).process(signal_processes+all_mc_bkgs).AddSyst(self.cb, *systematics_list.trigger_efficiency2016_syst_args)
				self.cb.cp().channel(["tt"]).process(signal_processes+all_mc_bkgs).AddSyst(self.cb, *systematics_list.tau_efficiency2016_tt_syst_args)
			else:
				self.cb.cp().channel(["tt"]).process(signal_processes+["ZTT", "TTT", "VVT"]).AddSyst(self.cb, *systematics_list.tau_efficiency_syst_args)


			# # efficiencies
			# self.cb.cp().channel(["tt"]).process(signal_processes+all_mc_bkgs).AddSyst(self.cb, *systematics_list.tau_efficiency2016_syst_args)
			# #self.cb.cp().channel(["tt"]).signals().AddSyst(self.cb, *systematics_list.tau_efficiency2016_syst_args)
			#
			# # Tau ES
			# self.cb.cp().channel(["tt"]).process(signal_processes+all_mc_bkgs).AddSyst(self.cb, *systematics_list.tau_es_syst_args)
			# #self.cb.cp().channel(["tt"]).signals().AddSyst(self.cb, *systematics_list.tau_es_syst_args)
			#
			# # fake-rate
			# self.cb.cp().channel(["tt"]).process(["ZLL"]).AddSyst(self.cb, *systematics_list.zllFakeTau_syst_args)

			# ======================================================================
			# All channels

			# ======================================================================
			# lumi
			if year == "2016":
				self.cb.cp().process(signal_processes+["VV", "VVT", "VVJ", "hww_gg125", "hww_qq125"]).AddSyst(self.cb, *systematics_list.lumi2016_syst_args)

				self.cb.cp().process(["TT", "TTT", "TTJJ"]).AddSyst(self.cb, *systematics_list.lumi2016_syst_args)
				self.cb.cp().process(["W"]).channel(["em", "tt", "mm", "ttbar"]).AddSyst(self.cb, *systematics_list.lumi2016_syst_args)
			else:
				self.cb.cp().process(signal_processes+all_mc_bkgs_no_W).AddSyst(self.cb, *systematics_list.lumi_syst_args)
				self.cb.cp().process(["W"]).channel(["em", "tt", "mm"]).AddSyst(self.cb, *systematics_list.lumi_syst_args)

			# ======================================================================
			# cross section

			self.cb.cp().channel(["em"]).process(["ZTT", "ZLL", "EWKZ"]).bin(["em_ZeroJet2D"]).AddSyst(self.cb, "CMS_htt_zmm_norm_extrap_0jet_em_13TeV", "lnN", ch.SystMap()(1.07))
			self.cb.cp().channel(["tt"]).process(["ZTT", "ZL", "ZJ", "EWKZ"]).bin(["tt_ZeroJet2D", "tt_ZeroJet2D_QCDCR"]).AddSyst(self.cb, "CMS_htt_zmm_norm_extrap_0jet_tt_13TeV", "lnN", ch.SystMap()(1.07))
			self.cb.cp().channel(["mt", "et"]).process(["ZTT", "ZL", "ZJ", "EWKZ"]).bin(["mt_ZeroJet2D", "mt_ZeroJet2D_WJCR", "mt_ZeroJet2D_QCDCR", "et_ZeroJet2D", "et_ZeroJet2D_WJCR", "et_ZeroJet2D_QCDCR"]).AddSyst(self.cb, "CMS_htt_zmm_norm_extrap_0jet_lt_13TeV", "lnN", ch.SystMap()(1.07))

			self.cb.cp().channel(["em"]).process(["ZTT", "ZLL", "EWKZ"]).bin(["em_Boosted2D"]).AddSyst(self.cb, "CMS_htt_zmm_norm_extrap_boosted_em_13TeV", "lnN", ch.SystMap()(1.07))
			self.cb.cp().channel(["tt"]).process(["ZTT", "ZL", "ZJ", "EWKZ"]).bin(["tt_Boosted2D", "tt_Boosted2D_QCDCR"]).AddSyst(self.cb, "CMS_htt_zmm_norm_extrap_boosted_tt_13TeV", "lnN", ch.SystMap()(1.07))
			self.cb.cp().channel(["mt", "et"]).process(["ZTT", "ZL", "ZJ", "EWKZ"]).bin(["mt_Boosted2D", "mt_Boosted2D_WJCR", "mt_Boosted2D_QCDCR", "et_Boosted2D", "et_Boosted2D_WJCR", "et_Boosted2D_QCDCR"]).AddSyst(self.cb, "CMS_htt_zmm_norm_extrap_boosted_lt_13TeV", "lnN", ch.SystMap()(1.07))

			self.cb.cp().channel(["em"]).process(["ZTT", "ZLL", "EWKZ"]).bin(["em_Vbf2D"]).AddSyst(self.cb, "CMS_htt_zmm_norm_extrap_VBF_em_13TeV", "lnN", ch.SystMap()(1.15))
			self.cb.cp().channel(["tt"]).process(["ZTT", "ZL", "ZJ", "EWKZ"]).bin(["tt_Vbf2D", "tt_Vbf2D_QCDCR"]).AddSyst(self.cb, "CMS_htt_zmm_norm_extrap_VBF_tt_13TeV", "lnN", ch.SystMap()(1.15))
			self.cb.cp().channel(["mt", "et"]).process(["ZTT", "ZL", "ZJ", "EWKZ"]).bin(["mt_vbf2D", "et_vbf2D"]).AddSyst(self.cb, "CMS_htt_zmm_norm_extrap_VBF_lt_13TeV", "lnN", ch.SystMap()(1.10))

			self.cb.cp().channel(["mt", "et", "tt"]).process(["ZTT", "ZL", "ZJ", "EWKZ"]).bin([channel + "_Vbf2D" for channel in ["mt", "et", "tt"]]).AddSyst(self.cb, "CMS_htt_zmumuShape_VBF_13TeV", "shape", ch.SystMap()(1.0))
			self.cb.cp().channel(["tt"]).process(["ZTT", "ZL", "ZJ", "EWKZ"]).bin(["tt_Vbf2D_QCDCR"]).AddSyst(self.cb, "CMS_htt_zmumuShape_VBF_13TeV", "shape", ch.SystMap()(1.0))
			self.cb.cp().channel(["em"]).process(["ZTT", "ZLL"]).bin(["em_Vbf2D"]).AddSyst(self.cb, "CMS_htt_zmumuShape_VBF_13TeV", "shape", ch.SystMap()(1.0))

			self.cb.cp().process(["TT", "TTT", "TTJJ"]).channel(["mt", "et", "em", "tt"]).AddSyst(self.cb, *systematics_list.ttj_cross_section_syst_args)
			if year == "2016":
				self.cb.cp().process(["VV", "VVT", "VVJ"]).AddSyst(self.cb, *systematics_list.vv_cross_section2016_syst_args)
			else:
				self.cb.cp().process(["VV", "VVT", "VVJ"]).AddSyst(self.cb, *systematics_list.vv_cross_section_syst_args)
			self.cb.cp().process(["W"]).channel(["em"]).AddSyst(self.cb, "CMS_htt_jetFakeLep_13TeV", "lnN", ch.SystMap()(1.20))
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
			self.cb.cp().channel(["mt", "et", "tt"]).process(signal_processes+all_mc_bkgs).AddSyst(self.cb, "CMS_scale_t_1prong_13TeV", "shape", ch.SystMap()(1.0))
			self.cb.cp().channel(["mt", "et", "tt"]).process(signal_processes+all_mc_bkgs).AddSyst(self.cb, "CMS_scale_t_1prong1pizero_13TeV", "shape", ch.SystMap()(1.0))
			self.cb.cp().channel(["mt", "et", "tt"]).process(signal_processes+all_mc_bkgs).AddSyst(self.cb, "CMS_scale_t_3prong_13TeV", "shape", ch.SystMap()(1.0))

			# jet ES
			# TODO: use mix of lnN/shape systematics as done in official analysis?

			for jecUncert in jecUncertNames:
				self.cb.cp().process(signal_processes+all_mc_bkgs+["QCD"]).bin([channel+"_"+category for channel in ["et", "mt", "tt", "em"] for category in ["ZeroJet2D", "Boosted2D", "Vbf2D"]]).AddSyst(self.cb, "CMS_scale_j_"+jecUncert+"_13TeV", "shape", ch.SystMap()(1.0))
				self.cb.cp().channel(["mt"]).process(signal_processes+all_mc_bkgs).bin(["mt_ZeroJet2D_WJCR", "mt_Boosted2D_WJCR", "mt_ZeroJet2D_QCDCR", "mt_Boosted2D_QCDCR"]).AddSyst(self.cb, "CMS_scale_j_"+jecUncert+"_13TeV", "shape", ch.SystMap()(1.0))
				self.cb.cp().channel(["et"]).process(signal_processes+all_mc_bkgs).bin(["et_ZeroJet2D_WJCR", "et_Boosted2D_WJCR", "et_Boosted2D_QCDCR"]).AddSyst(self.cb, "CMS_scale_j_"+jecUncert+"_13TeV", "shape", ch.SystMap()(1.0))
				self.cb.cp().channel(["et"]).process(signal_processes+all_mc_bkgs_no_TTJ).bin(["et_ZeroJet2D_QCDCR"]).AddSyst(self.cb, "CMS_scale_j_"+jecUncert+"_13TeV", "shape", ch.SystMap()(1.0))
				self.cb.cp().channel(["tt"]).process(signal_processes+all_mc_bkgs).bin(["tt_ZeroJet2D_QCDCR", "tt_Boosted2D_QCDCR", "tt_Vbf2D_QCDCR"]).AddSyst(self.cb, "CMS_scale_j_"+jecUncert+"_13TeV", "shape", ch.SystMap()(1.0))

			# jet->tau fake ES
			if year == "2016":
				self.cb.cp().channel(["et", "mt", "tt"]).process(["ZJ", "TTJJ", "VVJ"]).AddSyst(self.cb, "CMS_htt_jetToTauFake_13TeV", "shape", ch.SystMap()(1.0))
				self.cb.cp().channel(["et", "mt", "tt"]).process(["W"]).bin([channel+"_"+category for channel in ["et", "mt", "tt"] for category in ["ZeroJet2D", "Boosted2D", "Vbf2D"]]).AddSyst(self.cb, "CMS_htt_jetToTauFake_13TeV", "shape", ch.SystMap()(1.0))
				self.cb.cp().channel(["et", "mt"]).process(["W"]).bin([channel+"_"+category for channel in ["et", "mt"] for category in ["ZeroJet2D_QCDCR", "Boosted2D_QCDCR"]]).AddSyst(self.cb, "CMS_htt_jetToTauFake_13TeV", "shape", ch.SystMap()(1.0))
			else:
				self.cb.cp().channel(["et", "mt", "tt"]).process(["ZJ", "W", "TTJJ", "VVJ"]).AddSyst(self.cb, *systematics_list.jetFakeTau_syst_args)

			# MET ES
			self.cb.cp().channel(["et", "mt", "tt", "em"]).process(signal_processes+all_mc_bkgs).bin([channel+"_"+category for channel in ["et", "mt", "tt", "em"] for category in ["ZeroJet2D", "Boosted2D", "Vbf2D"]]).AddSyst(self.cb, "CMS_scale_met_clustered_13TeV", "shape", ch.SystMap()(1.0))
			self.cb.cp().channel(["et", "mt", "tt", "em"]).process(signal_processes+all_mc_bkgs).bin([channel+"_"+category for channel in ["et", "mt", "tt", "em"] for category in ["ZeroJet2D", "Boosted2D", "Vbf2D"]]).AddSyst(self.cb, "CMS_scale_met_unclustered_13TeV", "shape", ch.SystMap()(1.0))
			self.cb.cp().channel(["et", "mt"]).process(all_mc_bkgs).bin([channel+"_"+category for channel in ["et", "mt"] for category in ["ZeroJet2D_WJCR", "ZeroJet2D_QCDCR", "Boosted2D_WJCR", "Boosted2D_QCDCR"]]).AddSyst(self.cb, "CMS_scale_met_clustered_13TeV", "shape", ch.SystMap()(1.0))
			self.cb.cp().channel(["et", "mt"]).process(all_mc_bkgs).bin([channel+"_"+category for channel in ["et", "mt"] for category in ["ZeroJet2D_WJCR", "ZeroJet2D_QCDCR", "Boosted2D_WJCR", "Boosted2D_QCDCR"]]).AddSyst(self.cb, "CMS_scale_met_unclustered_13TeV", "shape", ch.SystMap()(1.0))

			# ======================================================================
			# W+jets and QCD estimation uncertainties

			# QCD normalization
			self.cb.cp().channel(["em"]).process(["QCD"]).bin(["em_ZeroJet2D"]).AddSyst(self.cb, "CMS_htt_QCD_0jet_em_13TeV", "lnN", ch.SystMap()(1.10))
			self.cb.cp().channel(["em"]).process(["QCD"]).bin(["em_Boosted2D"]).AddSyst(self.cb, "CMS_htt_QCD_boosted_em_13TeV", "lnN", ch.SystMap()(1.10))
			self.cb.cp().channel(["em"]).process(["QCD"]).bin(["em_Vbf2D"]).AddSyst(self.cb, "CMS_htt_QCD_VBF_em_13TeV", "lnN", ch.SystMap()(1.20))

			self.cb.cp().channel(["tt"]).process(["QCD"]).bin(["tt_ZeroJet2D"]).AddSyst(self.cb, "CMS_htt_QCD_0jet_tt_13TeV", "lnN", ch.SystMap()(1.027))
			self.cb.cp().channel(["tt"]).process(["QCD"]).bin(["tt_Boosted2D"]).AddSyst(self.cb, "CMS_htt_QCD_boosted_tt_13TeV", "lnN", ch.SystMap()(1.027))
			self.cb.cp().channel(["tt"]).process(["QCD"]).bin(["tt_Vbf2D"]).AddSyst(self.cb, "CMS_htt_QCD_VBF_tt_13TeV", "lnN", ch.SystMap()(1.15))

			self.cb.cp().channel(["mt"]).process(["QCD"]).bin(["mt_"+category for category in ["ZeroJet2D", "Boosted2D", "Vbf2D"]]).AddSyst(self.cb, "QCD_Extrap_Iso_nonIso_mt_13TeV", "lnN", ch.SystMap()(1.20))
			self.cb.cp().channel(["et"]).process(["QCD"]).bin(["et_"+category for category in ["ZeroJet2D", "Boosted2D", "Vbf2D"]]).AddSyst(self.cb, "QCD_Extrap_Iso_nonIso_et_13TeV", "lnN", ch.SystMap()(1.20))

			self.cb.cp().channel(["et", "mt"]).process(["QCD"]).bin([channel+"_ZeroJet2D" for channel in ["et", "mt"]]).AddSyst(self.cb, "WSFUncert_$CHANNEL_0jet_13TeV", "shape", ch.SystMap()(1.0))
			self.cb.cp().channel(["et", "mt"]).process(["QCD"]).bin([channel+"_Boosted2D" for channel in ["et", "mt"]]).AddSyst(self.cb, "WSFUncert_$CHANNEL_boosted_13TeV", "shape", ch.SystMap()(1.0))
			self.cb.cp().channel(["et", "mt"]).process(["QCD"]).bin([channel+"_Vbf2D" for channel in ["et", "mt"]]).AddSyst(self.cb, "WSFUncert_$CHANNEL_vbf_13TeV", "shape", ch.SystMap()(1.0))

			# W+jets high->low mt extrapolation uncertainty
			self.cb.cp().channel(["et", "mt"]).process(["W"]).bin([channel+"_ZeroJet2D" for channel in ["et", "mt"]]).AddSyst(self.cb, "WHighMTtoLowMT_0jet_13TeV", "lnN", ch.SystMap()(1.10))
			self.cb.cp().channel(["et", "mt"]).process(["W"]).bin([channel+"_Boosted2D" for channel in ["et", "mt"]]).AddSyst(self.cb, "WHighMTtoLowMT_boosted_13TeV", "lnN", ch.SystMap()(1.05))
			self.cb.cp().channel(["et", "mt"]).process(["W"]).bin([channel+"_Vbf2D" for channel in ["et", "mt"]]).AddSyst(self.cb, "WHighMTtoLowMT_vbf_13TeV", "lnN", ch.SystMap()(1.10))

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
			self.cb.cp().channel(["mt", "et", "tt", "em"]).process(["ggH"]).bin([channel+"_"+category for channel in ["et", "mt", "em", "tt"] for category in ["ZeroJet2D", "Boosted2D", "Vbf2D"]]).AddSyst(self.cb, "CMS_scale_gg_13TeV", "shape", ch.SystMap()(1.0))
			self.cb.cp().process(["qqH"]).AddSyst(self.cb, *systematics_list.htt_qcd_scale_qqh_syst_args)
			self.cb.cp().process(["ggH", "qqH"]).AddSyst(self.cb, *systematics_list.htt_pdf_scale_smhtt_syst_args)
			self.cb.cp().process(["ggH", "qqH"]).AddSyst(self.cb, *systematics_list.htt_ueps_smhtt_syst_args)

			# Uncertainty on BR of HTT @ 125 GeV
			self.cb.cp().signals().AddSyst(self.cb, "BR_htt_THU", "lnN", ch.SystMap()(1.017))
			self.cb.cp().signals().AddSyst(self.cb, "BR_htt_PU_mq", "lnN", ch.SystMap()(1.0099))
			self.cb.cp().signals().AddSyst(self.cb, "BR_htt_PU_alphas", "lnN", ch.SystMap()(1.0062))

			# Uncertainty on BR of HWW @ 125 GeV
			self.cb.cp().process(["hww_gg125", "hww_qq125"]).AddSyst(self.cb, "BR_hww_THU", "lnN", ch.SystMap()(1.0099))
			self.cb.cp().process(["hww_gg125", "hww_qq125"]).AddSyst(self.cb, "BR_hww_PU_mq", "lnN", ch.SystMap()(1.0099))
			self.cb.cp().process(["hww_gg125", "hww_qq125"]).AddSyst(self.cb, "BR_hww_PU_alphas", "lnN", ch.SystMap()(1.0066))

			self.cb.cp().process(["ggH", "hww_gg125"]).AddSyst(self.cb, "QCDScale_ggH", "lnN", ch.SystMap()(1.039))
			self.cb.cp().process(["qqH", "hww_qq125"]).AddSyst(self.cb, "QCDScale_qqH", "lnN", ch.SystMap()(1.004))
			self.cb.cp().process(["WH"]).AddSyst(self.cb, "QCDScale_VH", "lnN", ch.SystMap()(1.007))
			self.cb.cp().process(["ZH"]).AddSyst(self.cb, "QCDScale_VH", "lnN", ch.SystMap()(1.038))

			self.cb.cp().process(["ggH", "hww_gg125"]).AddSyst(self.cb, "pdf_Higgs_gg", "lnN", ch.SystMap()(1.032))
			self.cb.cp().process(["qqH", "hww_qq125"]).AddSyst(self.cb, "pdf_Higgs_qq", "lnN", ch.SystMap()(1.021))
			self.cb.cp().process(["WH"]).AddSyst(self.cb, "pdf_Higgs_VH", "lnN", ch.SystMap()(1.019))
			self.cb.cp().process(["ZH"]).AddSyst(self.cb, "pdf_Higgs_VH", "lnN", ch.SystMap()(1.016))


			# ======================================================================
			# control region rate parameters
			self.cb.cp().process(["W"]).bin(["mt_ZeroJet2D", "mt_ZeroJet2D_WJCR"]).AddSyst(self.cb, "rate_W_cr_0jet_mt", "rateParam", ch.SystMap()(1.0))
			self.cb.cp().process(["W"]).bin(["mt_Boosted2D", "mt_Boosted2D_WJCR", "mt_Vbf2D"]).AddSyst(self.cb, "rate_W_cr_boosted_mt", "rateParam", ch.SystMap()(1.0))
			self.cb.cp().process(["W"]).bin(["et_ZeroJet2D", "et_ZeroJet2D_WJCR"]).AddSyst(self.cb, "rate_W_cr_0jet_et", "rateParam", ch.SystMap()(1.0))
			self.cb.cp().process(["W"]).bin(["et_Boosted2D", "et_Boosted2D_WJCR", "et_Vbf2D"]).AddSyst(self.cb, "rate_W_cr_boosted_et", "rateParam", ch.SystMap()(1.0))

			self.cb.cp().process(["QCD"]).bin(["mt_ZeroJet2D", "mt_ZeroJet2D_QCDCR"]).AddSyst(self.cb, "rate_QCD_cr_0jet_mt", "rateParam", ch.SystMap()(1.0))
			self.cb.cp().process(["QCD"]).bin(["mt_Boosted2D", "mt_Boosted2D_QCDCR", "mt_Vbf2D"]).AddSyst(self.cb, "rate_QCD_cr_boosted_mt", "rateParam", ch.SystMap()(1.0))
			self.cb.cp().process(["QCD"]).bin(["et_ZeroJet2D", "et_ZeroJet2D_QCDCR"]).AddSyst(self.cb, "rate_QCD_cr_0jet_et", "rateParam", ch.SystMap()(1.0))
			self.cb.cp().process(["QCD"]).bin(["et_Boosted2D", "et_Boosted2D_QCDCR", "et_Vbf2D"]).AddSyst(self.cb, "rate_QCD_cr_boosted_et", "rateParam", ch.SystMap()(1.0))
			self.cb.cp().process(["QCD"]).bin(["tt_ZeroJet2D", "tt_ZeroJet2D_QCDCR"]).AddSyst(self.cb, "rate_QCD_cr_0jet_tt", "rateParam", ch.SystMap()(1.0))
			self.cb.cp().process(["QCD"]).bin(["tt_Boosted2D", "tt_Boosted2D_QCDCR"]).AddSyst(self.cb, "rate_QCD_cr_boosted_tt", "rateParam", ch.SystMap()(1.0))
			self.cb.cp().process(["QCD"]).bin(["tt_Vbf2D", "tt_Vbf2D_QCDCR"]).AddSyst(self.cb, "rate_QCD_cr_vbf_tt", "rateParam", ch.SystMap()(1.0))

			#self.cb.cp().GetParameter("rate_W_cr_0jet_mt").set_range(0, 5)
			#self.cb.cp().GetParameter("rate_W_cr_boosted_mt").set_range(0, 5)
			#self.cb.cp().GetParameter("rate_W_cr_0jet_et").set_range(0, 5)
			#self.cb.cp().GetParameter("rate_W_cr_boosted_et").set_range(0, 5)

			# self.cb.cp().GetParameter("rate_QCD_cr_0jet_mt").set_range(0, 5)
			# self.cb.cp().GetParameter("rate_QCD_cr_boosted_mt").set_range(0, 5)
			# self.cb.cp().GetParameter("rate_QCD_cr_0jet_et").set_range(0, 5)
			# self.cb.cp().GetParameter("rate_QCD_cr_boosted_et").set_range(0, 5)
			# self.cb.cp().GetParameter("rate_QCD_cr_0jet_tt").set_range(0, 5)
			# self.cb.cp().GetParameter("rate_QCD_cr_boosted_tt").set_range(0, 5)
			# self.cb.cp().GetParameter("rate_QCD_cr_vbf_tt").set_range(0, 5)

			# ======================================================================

			if log.isEnabledFor(logging.DEBUG):
				self.cb.PrintAll()
