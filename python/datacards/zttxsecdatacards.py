# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import CombineHarvester.CombineTools.ch as ch

import HiggsAnalysis.KITHiggsToTauTau.datacards.datacards as datacards
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.systematics_libary as SystLib


class ZttXsecDatacards(datacards.Datacards):
	def __init__(self, cb=None, model='default'):
		super(ZttXsecDatacards, self).__init__(cb)

		
		if cb is None:
			
			##Generate instance of systematic libary, in which the relevant information about the systematics are safed

			systematics_list = SystLib.SystematicLibary()
			# ======================================================================
			# MT channel
			self.add_processes(
					channel="mt",
					categories=["mt_"+category for category in ["inclusive"]],
					bkg_processes=["ZL", "ZJ", "TT", "VV", "W", "QCD"],
					sig_processes=["ZTT"],
					analysis=["ztt"],
					era=["13TeV"],
					mass=["90"]
			)
		
			# efficiencies
			self.cb.cp().channel(["mt"]).process(["ZTT", "ZL", "ZJ", "TT", "VV"]).AddSyst(self.cb, *systematics_list.muon_efficiency_syst_args)
			if "taueff" not in model:
				self.cb.cp().channel(["mt"]).process(["ZTT", "TT", "VV"]).AddSyst(self.cb, *systematics_list.tau_efficiency_corr_syst_args)
				self.cb.cp().channel(["mt"]).process(["ZTT", "TT", "VV"]).AddSyst(self.cb, *systematics_list.tau_efficiency_syst_args)

			# extrapolation uncertainty
			self.cb.cp().channel(["mt"]).process(["W"]).AddSyst(self.cb, *systematics_list.wj_extrapol_syst_args)

			# Tau ES
			self.cb.cp().channel(["mt"]).process(["ZTT"]).AddSyst(self.cb, *systematics_list.tau_es_syst_args)

			# fake-rate
			self.cb.cp().channel(["mt"]).process(["ZL"]).AddSyst(self.cb, *systematics_list.eFakeTau_vloose_syst_args)
			self.cb.cp().channel(["mt"]).process(["ZL"]).AddSyst(self.cb, *systematics_list.muFakeTau_syst_args)
			
			# Top pT reweight
			self.cb.cp().channel(["mt"]).process(["TT"]).AddSyst(self.cb, *systematics_list.ttj_syst_args)
		
			# ======================================================================
			# ET channel
			self.add_processes(
					channel="et",
					categories=["et_"+category for category in ["inclusive"]],
					bkg_processes=["ZL", "ZJ", "TT", "VV", "W", "QCD"],
					sig_processes=["ZTT"],
					analysis=["ztt"],
					era=["13TeV"],
					mass=["90"]
			)
		
			# efficiencies
			self.cb.cp().channel(["et"]).process(["ZTT", "ZL", "ZJ", "TT", "VV"]).AddSyst(self.cb, *systematics_list.electron_efficiency_syst_args)
			if "taueff" not in model:
				self.cb.cp().channel(["et"]).process(["ZTT", "TT", "VV"]).AddSyst(self.cb, *systematics_list.tau_efficiency_corr_syst_args)
				self.cb.cp().channel(["et"]).process(["ZTT", "TT", "VV"]).AddSyst(self.cb, *systematics_list.tau_efficiency_syst_args)

			# extrapolation uncertainty
			self.cb.cp().channel(["et"]).process(["W"]).AddSyst(self.cb, *systematics_list.wj_extrapol_syst_args)

			# Tau ES
			self.cb.cp().channel(["et"]).process(["ZTT"]).AddSyst(self.cb, *systematics_list.tau_es_syst_args)

			# fake-rate
			self.cb.cp().channel(["et"]).process(["ZL"]).AddSyst(self.cb, *systematics_list.eFakeTau_tight_syst_args)
			self.cb.cp().channel(["et"]).process(["ZL"]).AddSyst(self.cb, *systematics_list.muFakeTau_syst_args)
			
			# Top pT reweight
			self.cb.cp().channel(["et"]).process(["TT"]).AddSyst(self.cb, *systematics_list.ttj_syst_args)
		
			# ======================================================================
			# EM channel
			self.add_processes(
					channel="em",
					categories=["em_"+category for category in ["inclusive"]],
					bkg_processes=["ZLL", "TT", "VV", "W", "QCD"],
					sig_processes=["ZTT"],
					analysis=["ztt"],
					era=["13TeV"],
					mass=["90"]
			)
		
			# efficiencies
			self.cb.cp().channel(["em"]).process(["ZTT", "ZLL", "TT", "VV", "W", "QCD"]).AddSyst(self.cb, *systematics_list.electron_efficiency_syst_args)
			self.cb.cp().channel(["em"]).process(["ZTT", "ZLL", "TT", "VV", "W", "QCD"]).AddSyst(self.cb, *systematics_list.muon_efficiency_syst_args)

			# extrapolation uncertainty
			self.cb.cp().channel(["em"]).process(["TT"]).AddSyst(self.cb, *systematics_list.ttj_extrapol_syst_args)

			# Electron ES
			self.cb.cp().channel(["em"]).process(["ZTT", "TT", "W", "VV"]).AddSyst(self.cb, *systematics_list.ele_es_syst_args)

			# Muon ES
			self.cb.cp().channel(["em"]).process(["ZTT", "TT", "W", "VV"]).AddSyst(self.cb, *systematics_list.mu_es_syst_args)

			# Top pT reweight
			self.cb.cp().channel(["em"]).process(["TT"]).AddSyst(self.cb, *systematics_list.ttj_syst_args)

			# ======================================================================
			# All channels
			#self.cb.cp().process(["ZTT"]).AddSyst(self.cb, "ZTT_uniform_2", "lnU", ch.SystMap()(2.0))
		
			# lumi
			self.cb.cp().process(["ZTT", "ZLL", "ZL", "ZJ", "TT", "VV"]).AddSyst(self.cb, *systematics_list.lumi_syst_args)
		
			# cross section
			self.cb.cp().process(["VV"]).AddSyst(self.cb, *systematics_list.vv_cross_section_syst_args)
			self.cb.cp().process(["TT"]).AddSyst(self.cb, *systematics_list.ttj_cross_section_syst_args)
			self.cb.cp().process(["W"]).AddSyst(self.cb, *systematics_list.wj_cross_section_syst_args)

			# signal acceptance/efficiency
			self.cb.cp().process(["ZTT"]).AddSyst(self.cb, *systematics_list.ztt_pdf_scale_syst_args)
			self.cb.cp().process(["ZTT"]).AddSyst(self.cb, *systematics_list.ztt_qcd_scale_syst_args)

			# QCD systematic
			self.cb.cp().process(["QCD"]).AddSyst(self.cb, *systematics_list.qcd_syst_args)
		
			if log.isEnabledFor(logging.DEBUG):
				self.cb.PrintAll()


class ZttEffDatacards(datacards.Datacards):
	def __init__(self, cb=None):
		super(ZttEffDatacards, self).__init__(cb)
		
		systematics_list = SystLib.SystematicLibary()
		
		if cb is None:
			# ======================================================================
			# MT channel
			self.add_processes(
					channel="mt",
					categories=["mt_"+category for category in ["tauidvtightpass", "tauidvtightfail"]],
					bkg_processes=["ZL", "ZJ", "TT", "VV", "W", "QCD"],
					sig_processes=["ZTT"],
					analysis=["ztt"],
					era=["13TeV"],
					mass=["90"]
			)
		
			# efficiencies
			self.cb.cp().channel(["mt"]).process(["ZL", "ZJ", "TT", "VV", "W", "QCD"]).AddSyst(self.cb, *systematics_list.muon_efficiency_syst_args)

			# mu->tau fake ES
			self.cb.cp().channel(["mt"]).process(["ZL"]).AddSyst(self.cb, *systematics_list.muFakeTau_es_syst_args)

			# Tau ES
			self.cb.cp().channel(["mt"]).process(["ZTT"]).AddSyst(self.cb, *systematics_list.tau_es_syst_args)

			# fake-rate
			self.cb.cp().channel(["mt"]).process(["ZL"]).AddSyst(self.cb, *systematics_list.eFakeTau_vloose_syst_args)
			self.cb.cp().channel(["mt"]).process(["ZL"]).AddSyst(self.cb, *systematics_list.muFakeTau_syst_args)

			# b-tag efficiency and mistag
			self.cb.cp().channel(["mt"]).process(["ZTT", "TT"]).AddSyst(self.cb, *systematics_list.btag_efficiency_syst_args)
			self.cb.cp().channel(["mt"]).process(["ZTT", "TT"]).AddSyst(self.cb, *systematics_list.btag_mistag_syst_args)

			# ======================================================================
			# ET channel
			self.add_processes(
					channel="et",
					categories=["et_"+category for category in ["tauidpass", "tauidfail"]],
					bkg_processes=["ZL", "ZJ", "TT", "VV", "W", "QCD"],
					sig_processes=["ZTT"],
					analysis=["ztt"],
					era=["13TeV"],
					mass=["90"]
			)
		
			# efficiencies
			self.cb.cp().channel(["et"]).process(["ZL", "ZJ", "TT", "VV", "W", "QCD"]).AddSyst(self.cb, *systematics_list.electron_efficiency_syst_args)

			# Tau ES
			self.cb.cp().channel(["et"]).process(["ZTT"]).AddSyst(self.cb, *systematics_list.tau_es_syst_args)

			# fake-rate
			self.cb.cp().channel(["et"]).process(["ZL"]).AddSyst(self.cb, *systematics_list.eFakeTau_tight_syst_args)
			self.cb.cp().channel(["et"]).process(["ZL"]).AddSyst(self.cb, *systematics_list.muFakeTau_syst_args)

			# b-tag efficiency and mistag
			self.cb.cp().channel(["et"]).process(["ZTT", "TT"]).AddSyst(self.cb, *systematics_list.btag_efficiency_syst_args)
			self.cb.cp().channel(["et"]).process(["ZTT", "TT"]).AddSyst(self.cb, *systematics_list.btag_mistag_syst_args)

			# ======================================================================
			# All channels
			# lumi
			self.cb.cp().process(["ZTT", "ZLL", "ZL", "ZJ", "TT", "VV"]).AddSyst(self.cb, *systematics_list.lumi_syst_args)
		
			# cross section
			self.cb.cp().process(["ZL", "ZJ"]).AddSyst(self.cb, *systematics_list.ztt_cross_section_syst_args)
			self.cb.cp().process(["VV"]).AddSyst(self.cb, *systematics_list.vv_cross_section_syst_args)
			self.cb.cp().process(["TT"]).AddSyst(self.cb, *systematics_list.ttj_cross_section_syst_args)
			self.cb.cp().process(["W"]).AddSyst(self.cb, *systematics_list.wj_cross_section_syst_args)

			# signal acceptance/efficiency
			self.cb.cp().process(["ZTT"]).AddSyst(self.cb, *systematics_list.ztt_pdf_scale_syst_args)
			self.cb.cp().process(["ZTT"]).AddSyst(self.cb, *systematics_list.ztt_qcd_scale_syst_args)

			# W+jets extrapolation
			self.cb.cp().process(["W"]).AddSyst(self.cb, *systematics_list.wj_extrapol_syst_args)
			
			# QCD systematic
			self.cb.cp().process(["QCD"]).AddSyst(self.cb, *systematics_list.qcd_syst_inclusive_args)
		
			if log.isEnabledFor(logging.DEBUG):
				self.cb.PrintAll()


class ZttLepTauFakeRateDatacards(datacards.Datacards):
	def __init__(self, year="", noJECuncSplit=True, cb=None):
		super(ZttLepTauFakeRateDatacards, self).__init__(cb)
		
		all_mc_bkgs = ["ZTT", "ZL", "ZJ", "TTT", "TTJJ", "VV", "W"]
		all_mc_bkgs_no_W = ["ZTT", "ZL", "ZJ","TTT", "TTJJ", "VV"]
		
		systematics_list = SystLib.SystematicLibary()	

		if cb is None:
			# ======================================================================
			# MT channel
			self.add_processes(
					channel="mt",
					categories=["mt_"+category for category in ["antimutightpass", "antimutightfail"]],
					bkg_processes=["ZTT", "ZJ", "TT", "VV", "W", "QCD"],
					sig_processes=["ZL"],
					analysis=["ztt"],
					era=["13TeV"],
					mass=["90"]
			)
		
			# efficiencies
			self.cb.cp().channel(["mt"]).process(["ZL", "ZJ", "TT", "VV", "W", "QCD"]).AddSyst(self.cb, *systematics_list.muon_efficiency_syst_args)
			self.cb.cp().channel(["mt"]).process(["ZTT", "TT", "VV"]).AddSyst(self.cb, *systematics_list.tau_efficiency_syst_args)
			
			# Tau ES
			self.cb.cp().channel(["mt"]).process(["ZTT"]).AddSyst(self.cb, *systematics_list.tau_es_syst_args)
			
			# ======================================================================
			# ET channel
			self.add_processes(
					channel="et",
					categories=["et_"+category for category in ["antievloosepass", "antievloosefail"]],
					bkg_processes=["ZTT", "ZJ", "TT", "VV", "W", "QCD"],
					sig_processes=["ZL"],
					analysis=["ztt"],
					era=["13TeV"],
					mass=["90"]
			)
		
			# efficiencies
			if year == "2016":
				self.cb.cp().channel(["et"]).process(all_mc_bkgs_no_W).AddSyst(self.cb, *systematics_list.electron_efficiency2016_syst_args)
				self.cb.cp().channel(["et"]).process(all_mc_bkgs_no_W).AddSyst(self.cb, *systematics_list.trigger_efficiency2016_syst_args)   
				self.cb.cp().channel(["et"]).process(["ZTT", "TTT", "VV"]).AddSyst(self.cb, *systematics_list.tau_efficiency2016_corr_syst_args) 
				self.cb.cp().channel(["et"]).process(["ZTT", "TTT", "VV"]).AddSyst(self.cb, *systematics_list.tau_efficiency2016_syst_args)
			else:
				self.cb.cp().channel(["et"]).process(all_mc_bkgs_no_W).AddSyst(self.cb, *systematics_list.electron_efficiency_syst_args)
				self.cb.cp().channel(["et"]).process(["ZTT", "TTT", "VV"]).AddSyst(self.cb, *systematics_list.tau_efficiency_corr_syst_args)
				self.cb.cp().channel(["et"]).process(["ZTT", "TTT", "VV"]).AddSyst(self.cb, *systematics_list.tau_efficiency_syst_args)

			# Probe Tau ES
			self.cb.cp().channel(["et"]).process(["ZTT"]).AddSyst(self.cb, *systematics_list.probetau_es_syst_args)
			
			# Probe Electron ES
			self.cb.cp().channel(["et"]).process(["ZL"]).AddSyst(self.cb, *systematics_list.probeele_es_syst_args)
			
			# Tag Electron ES
			self.cb.cp().channel(["et"]).process(["ZL"]).AddSyst(self.cb, *systematics_list.tagele_es_syst_args)
			
			# Visible mass resolution
			self.cb.cp().channel(["et"]).process(["ZL"]).AddSyst(self.cb, *systematics_list.massres_syst_args)
		
			# additional nuisance for possible differences in Z -> ee norm., in addition to the Z->tautau norm.
			self.cb.cp().channel(["et"]).process(["ZL"]).AddSyst(self.cb, *systematics_list.zee_norm_syst_args)
			
			# ===========================================================================
			# All channels
			# lumi
			if year == "2016":
				self.cb.cp().process(all_mc_bkgs_no_W).AddSyst(self.cb, *systematics_list.lumi2016_syst_args)
			else:
				self.cb.cp().process(all_mc_bkgs_no_W).AddSyst(self.cb, *systematics_list.lumi_syst_args)
		
			# cross section
			self.cb.cp().process(["ZTT", "ZL", "ZJ"]).AddSyst(self.cb, *systematics_list.ztt_cross_section_syst_args)
			self.cb.cp().process(["TTJ", "TTJJ"]).AddSyst(self.cb, *systematics_list.ttj_cross_section_syst_args)
			self.cb.cp().process(["W"]).AddSyst(self.cb, *systematics_list.wj_cross_section_syst_args)
			if year == "2016":
				self.cb.cp().process(["VV"]).AddSyst(self.cb, *systematics_list.vv_cross_section2016_syst_args)
			else:
				self.cb.cp().process(["VV"]).AddSyst(self.cb, *systematics_list.vv_cross_section_syst_args)

			# W+jets extrapolation
			self.cb.cp().process(["W"]).AddSyst(self.cb, *systematics_list.wj_extrapol_syst_args)
			
			# QCD systematic
			self.cb.cp().process(["QCD"]).AddSyst(self.cb, *systematics_list.qcd_syst_args)

			# QCD systematic
			self.cb.cp().channel(["mt", "et"]).process(["QCD"]).AddSyst(self.cb, "QCD_Extrap_Iso_nonIso_lt_13TeV", "lnN", ch.SystMap()(1.20))
			self.cb.cp().channel(["mt", "et"]).process(["QCD"]).AddSyst(self.cb, "WSFUncert_lt_13TeV", "shape", ch.SystMap()(1.0))

			# W+jets high->low mt extrapolation uncertainty
			#self.cb.cp().channel(["mt", "et"]).process(["W"]).AddSyst(self.cb, "WHighMTtoLowMT_13TeV", "lnN", ch.SystMap()(1.10))

		
			if log.isEnabledFor(logging.DEBUG):
				self.cb.PrintAll()


class ZttJetTauFakeFactorDatacards(datacards.Datacards):
	def __init__(self, cb=None, model='default'):
		super(ZttJetTauFakeFactorDatacards, self).__init__(cb)
		
		if cb is None:
			# ======================================================================
			# MT channel
			self.add_processes(
					channel="mt",
					categories=["mt_"+category for category in ["inclusive"]],
					bkg_processes=["ZL", "TTJT", "TTJL", "VVT", "VVL", "WJT", "WJL", "FF"],
					sig_processes=["ZTT"],
					analysis=["ztt"],
					era=["13TeV"],
					mass=["90"]
			)
		
			# efficiencies
			self.cb.cp().channel(["mt"]).process(["ZL", "TTJT", "TTJL", "VVT", "VVL", "WJT", "WJL", "ZTT"]).AddSyst(self.cb, *systematics_list.muon_efficiency_syst_args)
			self.cb.cp().channel(["mt"]).process(["ZL", "TTJT", "VVT", "WJT", "ZTT"]).AddSyst(self.cb, *systematics_list.tau_efficiency_syst_args)
			self.cb.cp().channel(["mt"]).process(["ZL", "TTJT", "VVT", "WJT", "ZTT"]).AddSyst(self.cb, *systematics_list.tau_efficiency_corr_syst_args)

			# extrapolation uncertainty
			self.cb.cp().channel(["mt"]).process(["WJT", "WJL"]).AddSyst(self.cb, *systematics_list.wj_extrapol_syst_args)
			
			# Tau ES
			#self.cb.cp().channel(["mt"]).process(["TTJT", "VVT", "WJT", "ZTT"]).AddSyst(self.cb, *systematics_list.tau_es_syst_args)
			self.cb.cp().channel(["mt"]).process(["ZTT"]).AddSyst(self.cb, *systematics_list.tau_es_syst_args)

			# fake-rate
			self.cb.cp().channel(["mt"]).process(["TTJL", "VVL", "WJL", "ZL"]).AddSyst(self.cb, *systematics_list.eFakeTau_vloose_syst_args)
			self.cb.cp().channel(["mt"]).process(["TTJL", "VVL", "WJL", "ZL"]).AddSyst(self.cb, *systematics_list.muFakeTau_syst_args)

			# Top pT reweight
			self.cb.cp().channel(["mt"]).process(["TTJT", "TTJL"]).AddSyst(self.cb, *systematics_list.ttj_syst_args)
			
			# Fake-Factor (Jets faking Taus)
			self.cb.cp().channel(["mt"]).process(["FF"]).AddSyst(self.cb, *systematics_list.jetFakeTau_qcd_syst_args)
			self.cb.cp().channel(["mt"]).process(["FF"]).AddSyst(self.cb, *systematics_list.jetFakeTau_w_syst_args)
			self.cb.cp().channel(["mt"]).process(["FF"]).AddSyst(self.cb, *systematics_list.jetFakeTau_tt_corr_syst_args)
			self.cb.cp().channel(["mt"]).process(["FF"]).AddSyst(self.cb, *systematics_list.jetFakeTau_tt_stat_syst_args)
			self.cb.cp().channel(["mt"]).process(["FF"]).AddSyst(self.cb, *systematics_list.jetFakeTau_frac_qcd_syst_args)
			self.cb.cp().channel(["mt"]).process(["FF"]).AddSyst(self.cb, *systematics_list.jetFakeTau_frac_w_syst_args)
			self.cb.cp().channel(["mt"]).process(["FF"]).AddSyst(self.cb, *systematics_list.jetFakeTau_frac_tt_syst_args)
			self.cb.cp().channel(["mt"]).process(["FF"]).AddSyst(self.cb, *systematics_list.jetFakeTau_frac_dy_syst_args)
			

			# ======================================================================
			# ET channel
			self.add_processes(
					channel="et",
					categories=["et_"+category for category in ["inclusive"]],
					bkg_processes=["ZL", "TTJT", "TTJL", "VVT", "VVL", "WJT", "WJL", "FF"],
					sig_processes=["ZTT"],
					analysis=["ztt"],
					era=["13TeV"],
					mass=["90"]
			)
		
			# efficiencies
			self.cb.cp().channel(["et"]).process(["ZL", "TTJT", "TTJL", "VVT", "VVL", "WJT", "WJL", "ZTT"]).AddSyst(self.cb, *systematics_list.electron_efficiency_syst_args)
			self.cb.cp().channel(["et"]).process(["ZL", "TTJT", "VVT", "WJT", "ZTT"]).AddSyst(self.cb, *systematics_list.tau_efficiency_syst_args)
			self.cb.cp().channel(["et"]).process(["ZL", "TTJT", "VVT", "WJT", "ZTT"]).AddSyst(self.cb, *systematics_list.tau_efficiency_corr_syst_args)
			
			# extrapolation uncertainty
			self.cb.cp().channel(["et"]).process(["WJT", "WJL"]).AddSyst(self.cb, *systematics_list.wj_extrapol_syst_args)

			# Tau ES
			#self.cb.cp().channel(["et"]).process(["TTJT", "VVT", "WJT", "ZTT"]).AddSyst(self.cb, *systematics_list.tau_es_syst_args)
			self.cb.cp().channel(["et"]).process(["ZTT"]).AddSyst(self.cb, *systematics_list.tau_es_syst_args)

			# fake-rate
			self.cb.cp().channel(["et"]).process(["TTJL", "VVL", "WJL", "ZL"]).AddSyst(self.cb, *systematics_list.eFakeTau_vloose_syst_args)
			self.cb.cp().channel(["et"]).process(["TTJL", "VVL", "WJL", "ZL"]).AddSyst(self.cb, *systematics_list.muFakeTau_syst_args)

			# Top pT reweight
			self.cb.cp().channel(["et"]).process(["TTJT", "TTJL"]).AddSyst(self.cb, *systematics_list.ttj_syst_args)

			# Fake-Factor (Jets faking Taus)
			self.cb.cp().channel(["et"]).process(["FF"]).AddSyst(self.cb, *systematics_list.jetFakeTau_qcd_syst_args)
			self.cb.cp().channel(["et"]).process(["FF"]).AddSyst(self.cb, *systematics_list.jetFakeTau_w_syst_args)
			self.cb.cp().channel(["et"]).process(["FF"]).AddSyst(self.cb, *systematics_list.jetFakeTau_tt_corr_syst_args)
			self.cb.cp().channel(["et"]).process(["FF"]).AddSyst(self.cb, *systematics_list.jetFakeTau_tt_stat_syst_args)
			self.cb.cp().channel(["et"]).process(["FF"]).AddSyst(self.cb, *systematics_list.jetFakeTau_frac_qcd_syst_args)
			self.cb.cp().channel(["et"]).process(["FF"]).AddSyst(self.cb, *systematics_list.jetFakeTau_frac_w_syst_args)
			self.cb.cp().channel(["et"]).process(["FF"]).AddSyst(self.cb, *systematics_list.jetFakeTau_frac_tt_syst_args)
			self.cb.cp().channel(["et"]).process(["FF"]).AddSyst(self.cb, *systematics_list.jetFakeTau_frac_dy_syst_args)
			
			# ======================================================================
			# All channels
			# lumi
			self.cb.cp().process(["ZTT", "ZLL", "TTJT", "TTJL", "VVT", "VVL", "WJT", "WJL", "ZL", "ZJ", "TT", "VV"]).AddSyst(self.cb, *systematics_list.lumi_syst_args)
		
			# cross section
			#self.cb.cp().process(["ZL", "ZJ"]).AddSyst(self.cb, *systematics_list.ztt_cross_section_syst_args)
			self.cb.cp().process(["TTJT", "TTJL"]).AddSyst(self.cb, *systematics_list.ttj_cross_section_syst_args)
			self.cb.cp().process(["VVT", "VVL"]).AddSyst(self.cb, *systematics_list.vv_cross_section_syst_args)
			self.cb.cp().process(["WJT", "WJL"]).AddSyst(self.cb, *systematics_list.wj_cross_section_syst_args)
			
			# signal acceptance/efficiency
			self.cb.cp().process(["ZTT"]).AddSyst(self.cb, *systematics_list.ztt_pdf_scale_syst_args)
			self.cb.cp().process(["ZTT"]).AddSyst(self.cb, *systematics_list.ztt_qcd_scale_syst_args)
		
			if log.isEnabledFor(logging.DEBUG):
				self.cb.PrintAll()
