# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import CombineHarvester.CombineTools.ch as ch

import HiggsAnalysis.KITHiggsToTauTau.datacards.datacards as datacards
<<<<<<< Updated upstream
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.systematics_libary as systematics_libary
=======
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.systematics_libary as SystLib
>>>>>>> Stashed changes


class ZttPolarisationDatacards(datacards.Datacards):
	def __init__(self, cb=None):
		super(ZttPolarisationDatacards, self).__init__(cb)
		
		if cb is None:
<<<<<<< Updated upstream
			
			systematics_library = systematics_libary.SystematicLibary()
			
=======

			##Generate instance of systematic libary, in which the relevant information about the systematics are safed

			systematics_list = SystLib.SystematicLibary()
	
>>>>>>> Stashed changes
			# ======================================================================
			# MT channel
			self.add_processes(
					channel="mt",
					categories=["mt_"+category for category in ["rho", "oneprong"]], # "a1"
					bkg_processes=["ZL", "ZJ", "TT", "VV", "W", "QCD"],
					sig_processes=["ZTTPOSPOL", "ZTTNEGPOL"],
					analysis=["ztt"],
					era=["13TeV"],
					mass=["0"]
			)
		
			# efficiencies
<<<<<<< Updated upstream
			self.cb.cp().channel(["mt"]).process(["ZTTPOSPOL", "ZTTNEGPOL", "ZL", "ZJ", "TT", "VV"]).AddSyst(self.cb, *systematics_library.muon_efficiency_syst_args)
			
			self.cb.cp().channel(["mt"]).process(["ZTTPOSPOL", "ZTTNEGPOL"]).AddSyst(self.cb, *systematics_library.tau_efficiency_corr_syst_args)
			self.cb.cp().channel(["mt"]).process(["ZTTPOSPOL", "ZTTNEGPOL"]).AddSyst(self.cb, *systematics_library.tau_es_syst_args)
			#self.cb.cp().channel(["mt"]).process(["ZTTPOSPOL", "ZTTNEGPOL"]).AddSyst(self.cb, *systematics_library.tau_efficiency_syst_args)
			
			# from Yuta
			self.cb.cp().channel(["mt"]).process(["ZL", "ZJ", "W"]).AddSyst(self.cb, *systematics_library.boson_scale_met_syst_args)
			self.cb.cp().channel(["mt"]).process(["ZL", "ZJ", "W"]).AddSyst(self.cb, *systematics_library.boson_resolution_met_syst_args)
			self.cb.cp().channel(["mt"]).process(["TT", "VV"]).AddSyst(self.cb, *systematics_library.ewk_top_scale_met_syst_args)
			self.cb.cp().channel(["mt"]).process(["TT", "VV"]).AddSyst(self.cb, *systematics_library.ewk_top_resolution_met_syst_args)

			# extrapolation uncertainty
			self.cb.cp().channel(["mt"]).process(["TT"]).AddSyst(self.cb, *systematics_library.ttj_extrapol_syst_args)
			self.cb.cp().channel(["mt"]).process(["W"]).AddSyst(self.cb, *systematics_library.wj_extrapol_syst_args)

			# Tau ES
			self.cb.cp().channel(["mt"]).process(["ZTTPOSPOL", "ZTTNEGPOL"]).AddSyst(self.cb, *systematics_library.tau_es_syst_args)

			# fake-rate
			self.cb.cp().channel(["mt"]).process(["ZL"]).AddSyst(self.cb, *systematics_library.eFakeTau_vloose_syst_args)
			self.cb.cp().channel(["mt"]).process(["ZL"]).AddSyst(self.cb, *systematics_library.muFakeTau_syst_args)
			self.cb.cp().channel(["mt"]).process(["ZJ"]).AddSyst(self.cb, *systematics_library.zjFakeTau_syst_args)
			
			# Top pT reweight
			#self.cb.cp().channel(["mt"]).process(["TT"]).AddSyst(self.cb, *systematics_library.ttj_syst_args)
=======
			self.cb.cp().channel(["mt"]).process(["ZTTPOSPOL", "ZTTNEGPOL", "ZL", "ZJ", "TT", "VV"]).AddSyst(self.cb, *systematics_list.muon_efficiency_syst_args)
			
			self.cb.cp().channel(["mt"]).process(["ZTTPOSPOL", "ZTTNEGPOL"]).AddSyst(self.cb, *systematics_list.tau_efficiency_corr_syst_args)
			self.cb.cp().channel(["mt"]).process(["ZTTPOSPOL", "ZTTNEGPOL"]).AddSyst(self.cb, *systematics_list.tau_es_syst_args)
			#self.cb.cp().channel(["mt"]).process(["ZTTPOSPOL", "ZTTNEGPOL"]).AddSyst(self.cb, *systematics_list.tau_efficiency_syst_args)
			
			# from Yuta
			self.cb.cp().channel(["mt"]).process(["ZL", "ZJ", "W"]).AddSyst(self.cb, *systematics_list.boson_scale_met_syst_args)
			self.cb.cp().channel(["mt"]).process(["ZL", "ZJ", "W"]).AddSyst(self.cb, *systematics_list.boson_resolution_met_syst_args)
			self.cb.cp().channel(["mt"]).process(["TT", "VV"]).AddSyst(self.cb, *systematics_list.ewk_top_scale_met_syst_args)
			self.cb.cp().channel(["mt"]).process(["TT", "VV"]).AddSyst(self.cb, *systematics_list.ewk_top_resolution_met_syst_args)

			# extrapolation uncertainty
			self.cb.cp().channel(["mt"]).process(["TT"]).AddSyst(self.cb, *systematics_list.ttj_extrapol_syst_args)
			self.cb.cp().channel(["mt"]).process(["W"]).AddSyst(self.cb, *systematics_list.wj_extrapol_syst_args)

			# Tau ES
			self.cb.cp().channel(["mt"]).process(["ZTTPOSPOL", "ZTTNEGPOL"]).AddSyst(self.cb, *systematics_list.tau_es_syst_args)

			# fake-rate
			self.cb.cp().channel(["mt"]).process(["ZL"]).AddSyst(self.cb, *systematics_list.eFakeTau_vloose_syst_args)
			self.cb.cp().channel(["mt"]).process(["ZL"]).AddSyst(self.cb, *systematics_list.muFakeTau_syst_args)
			self.cb.cp().channel(["mt"]).process(["ZJ"]).AddSyst(self.cb, *systematics_list.zjFakeTau_syst_args)
			
			# Top pT reweight
			#self.cb.cp().channel(["mt"]).process(["TT"]).AddSyst(self.cb, *systematics_list.ttj_syst_args)
>>>>>>> Stashed changes
		
			# ======================================================================
			# ET channel
			self.add_processes(
					channel="et",
					categories=["et_"+category for category in ["rho", "oneprong"]], # "a1"
					bkg_processes=["ZL", "ZJ", "TT", "VV", "W", "QCD"],
					sig_processes=["ZTTPOSPOL", "ZTTNEGPOL"],
					analysis=["ztt"],
					era=["13TeV"],
					mass=["0"]
			)
		
			# efficiencies
<<<<<<< Updated upstream
			self.cb.cp().channel(["et"]).process(["ZTTPOSPOL", "ZTTNEGPOL", "ZL", "ZJ", "TT", "VV"]).AddSyst(self.cb, *systematics_library.electron_efficiency_syst_args)
			
			self.cb.cp().channel(["et"]).process(["ZTTPOSPOL", "ZTTNEGPOL"]).AddSyst(self.cb, *systematics_library.tau_efficiency_corr_syst_args)
			self.cb.cp().channel(["et"]).process(["ZTTPOSPOL", "ZTTNEGPOL"]).AddSyst(self.cb, *systematics_library.tau_es_syst_args)
			#self.cb.cp().channel(["et"]).process(["ZTTPOSPOL", "ZTTNEGPOL"]).AddSyst(self.cb, *systematics_library.tau_efficiency_syst_args)
			
			# from Yuta
			self.cb.cp().channel(["et"]).process(["ZL", "ZJ", "W"]).AddSyst(self.cb, *systematics_library.boson_scale_met_syst_args)
			self.cb.cp().channel(["et"]).process(["ZL", "ZJ", "W"]).AddSyst(self.cb, *systematics_library.boson_resolution_met_syst_args)
			self.cb.cp().channel(["et"]).process(["TT", "VV"]).AddSyst(self.cb, *systematics_library.ewk_top_scale_met_syst_args)
			self.cb.cp().channel(["et"]).process(["TT", "VV"]).AddSyst(self.cb, *systematics_library.ewk_top_resolution_met_syst_args)

			# extrapolation uncertainty
			self.cb.cp().channel(["et"]).process(["TT"]).AddSyst(self.cb, *systematics_library.ttj_extrapol_syst_args)
			self.cb.cp().channel(["et"]).process(["W"]).AddSyst(self.cb, *systematics_library.wj_extrapol_syst_args)

			# Tau ES
			self.cb.cp().channel(["et"]).process(["ZTTPOSPOL", "ZTTNEGPOL"]).AddSyst(self.cb, *systematics_library.tau_es_syst_args)

			# fake-rate
			self.cb.cp().channel(["et"]).process(["ZL"]).AddSyst(self.cb, *systematics_library.eFakeTau_tight_syst_args)
			self.cb.cp().channel(["et"]).process(["ZL"]).AddSyst(self.cb, *systematics_library.muFakeTau_syst_args)
			self.cb.cp().channel(["et"]).process(["ZJ"]).AddSyst(self.cb, *systematics_library.zjFakeTau_syst_args)
			
			# Top pT reweight
			#self.cb.cp().channel(["et"]).process(["TT"]).AddSyst(self.cb, *systematics_library.ttj_syst_args)
=======
			self.cb.cp().channel(["et"]).process(["ZTTPOSPOL", "ZTTNEGPOL", "ZL", "ZJ", "TT", "VV"]).AddSyst(self.cb, *systematics_list.electron_efficiency_syst_args)
			
			self.cb.cp().channel(["et"]).process(["ZTTPOSPOL", "ZTTNEGPOL"]).AddSyst(self.cb, *systematics_list.tau_efficiency_corr_syst_args)
			self.cb.cp().channel(["et"]).process(["ZTTPOSPOL", "ZTTNEGPOL"]).AddSyst(self.cb, *systematics_list.tau_es_syst_args)
			#self.cb.cp().channel(["et"]).process(["ZTTPOSPOL", "ZTTNEGPOL"]).AddSyst(self.cb, *systematics_list.tau_efficiency_syst_args)
			
			# from Yuta
			self.cb.cp().channel(["et"]).process(["ZL", "ZJ", "W"]).AddSyst(self.cb, *systematics_list.boson_scale_met_syst_args)
			self.cb.cp().channel(["et"]).process(["ZL", "ZJ", "W"]).AddSyst(self.cb, *systematics_list.boson_resolution_met_syst_args)
			self.cb.cp().channel(["et"]).process(["TT", "VV"]).AddSyst(self.cb, *systematics_list.ewk_top_scale_met_syst_args)
			self.cb.cp().channel(["et"]).process(["TT", "VV"]).AddSyst(self.cb, *systematics_list.ewk_top_resolution_met_syst_args)

			# extrapolation uncertainty
			self.cb.cp().channel(["et"]).process(["TT"]).AddSyst(self.cb, *systematics_list.ttj_extrapol_syst_args)
			self.cb.cp().channel(["et"]).process(["W"]).AddSyst(self.cb, *systematics_list.wj_extrapol_syst_args)

			# Tau ES
			self.cb.cp().channel(["et"]).process(["ZTTPOSPOL", "ZTTNEGPOL"]).AddSyst(self.cb, *systematics_list.tau_es_syst_args)

			# fake-rate
			self.cb.cp().channel(["et"]).process(["ZL"]).AddSyst(self.cb, *systematics_list.eFakeTau_tight_syst_args)
			self.cb.cp().channel(["et"]).process(["ZL"]).AddSyst(self.cb, *systematics_list.muFakeTau_syst_args)
			self.cb.cp().channel(["et"]).process(["ZJ"]).AddSyst(self.cb, *systematics_list.zjFakeTau_syst_args)
			
			# Top pT reweight
			#self.cb.cp().channel(["et"]).process(["TT"]).AddSyst(self.cb, *systematics_list.ttj_syst_args)
>>>>>>> Stashed changes
		
			# ======================================================================
			# TT channel
			self.add_processes(
					channel="tt",
					categories=["tt_"+category for category in ["rho", "rho_1", "rho_2", "oneprong", "combined_oneprong_oneprong", "combined_rho_rho"]], # "a1"
					bkg_processes=["ZL", "ZJ", "TT", "VV", "W", "QCD"],
					sig_processes=["ZTTPOSPOL", "ZTTNEGPOL"],
					analysis=["ztt"],
					era=["13TeV"],
					mass=["0"]
			)
		
			# efficiencies
<<<<<<< Updated upstream
			self.cb.cp().channel(["tt"]).process(["ZTTPOSPOL", "ZTTNEGPOL"]).AddSyst(self.cb, *systematics_library.tau_efficiency_corr_syst_args)
			self.cb.cp().channel(["tt"]).process(["ZTTPOSPOL", "ZTTNEGPOL"]).AddSyst(self.cb, *systematics_library.tau_es_syst_args)
			#self.cb.cp().channel(["tt"]).process(["ZTTPOSPOL", "ZTTNEGPOL"]).AddSyst(self.cb, *systematics_library.tau_efficiency_syst_args)
			
			# from Yuta
			self.cb.cp().channel(["tt"]).process(["ZL", "ZJ", "W"]).AddSyst(self.cb, *systematics_library.boson_scale_met_syst_args)
			self.cb.cp().channel(["tt"]).process(["ZL", "ZJ", "W"]).AddSyst(self.cb, *systematics_library.boson_resolution_met_syst_args)
			self.cb.cp().channel(["tt"]).process(["TT", "VV"]).AddSyst(self.cb, *systematics_library.ewk_top_scale_met_syst_args)
			self.cb.cp().channel(["tt"]).process(["TT", "VV"]).AddSyst(self.cb, *systematics_library.ewk_top_resolution_met_syst_args)

			# extrapolation uncertainty
			self.cb.cp().channel(["mt"]).process(["TT"]).AddSyst(self.cb, *systematics_library.ttj_extrapol_syst_args)
			self.cb.cp().channel(["tt"]).process(["W"]).AddSyst(self.cb, *systematics_library.wj_extrapol_syst_args)

			# Tau ES
			self.cb.cp().channel(["tt"]).process(["ZTTPOSPOL", "ZTTNEGPOL"]).AddSyst(self.cb, *systematics_library.tau_es_syst_args)

			# fake-rate
			self.cb.cp().channel(["tt"]).process(["ZL"]).AddSyst(self.cb, *systematics_library.eFakeTau_tight_syst_args)
			self.cb.cp().channel(["tt"]).process(["ZL"]).AddSyst(self.cb, *systematics_library.muFakeTau_syst_args)
			self.cb.cp().channel(["tt"]).process(["ZJ"]).AddSyst(self.cb, *systematics_library.zjFakeTau_syst_args)
			
			# Top pT reweight
			#self.cb.cp().channel(["tt"]).process(["TT"]).AddSyst(self.cb, *systematics_library.ttj_syst_args)
=======
			self.cb.cp().channel(["tt"]).process(["ZTTPOSPOL", "ZTTNEGPOL"]).AddSyst(self.cb, *systematics_list.tau_efficiency_corr_syst_args)
			self.cb.cp().channel(["tt"]).process(["ZTTPOSPOL", "ZTTNEGPOL"]).AddSyst(self.cb, *systematics_list.tau_es_syst_args)
			#self.cb.cp().channel(["tt"]).process(["ZTTPOSPOL", "ZTTNEGPOL"]).AddSyst(self.cb, *systematics_list.tau_efficiency_syst_args)
			
			# from Yuta
			self.cb.cp().channel(["tt"]).process(["ZL", "ZJ", "W"]).AddSyst(self.cb, *systematics_list.boson_scale_met_syst_args)
			self.cb.cp().channel(["tt"]).process(["ZL", "ZJ", "W"]).AddSyst(self.cb, *systematics_list.boson_resolution_met_syst_args)
			self.cb.cp().channel(["tt"]).process(["TT", "VV"]).AddSyst(self.cb, *systematics_list.ewk_top_scale_met_syst_args)
			self.cb.cp().channel(["tt"]).process(["TT", "VV"]).AddSyst(self.cb, *systematics_list.ewk_top_resolution_met_syst_args)

			# extrapolation uncertainty
			self.cb.cp().channel(["mt"]).process(["TT"]).AddSyst(self.cb, *systematics_list.ttj_extrapol_syst_args)
			self.cb.cp().channel(["tt"]).process(["W"]).AddSyst(self.cb, *systematics_list.wj_extrapol_syst_args)

			# Tau ES
			self.cb.cp().channel(["tt"]).process(["ZTTPOSPOL", "ZTTNEGPOL"]).AddSyst(self.cb, *systematics_list.tau_es_syst_args)

			# fake-rate
			self.cb.cp().channel(["tt"]).process(["ZL"]).AddSyst(self.cb, *systematics_list.eFakeTau_tight_syst_args)
			self.cb.cp().channel(["tt"]).process(["ZL"]).AddSyst(self.cb, *systematics_list.muFakeTau_syst_args)
			self.cb.cp().channel(["tt"]).process(["ZJ"]).AddSyst(self.cb, *systematics_list.zjFakeTau_syst_args)
			
			# Top pT reweight
			#self.cb.cp().channel(["tt"]).process(["TT"]).AddSyst(self.cb, *systematics_list.ttj_syst_args)
>>>>>>> Stashed changes
		
			# ======================================================================
			# EM channel
			self.add_processes(
					channel="em",
					categories=["em_"+category for category in ["oneprong"]],
					bkg_processes=["ZL", "ZJ", "TT", "VV", "W", "QCD"],
					sig_processes=["ZTTPOSPOL", "ZTTNEGPOL"],
					analysis=["ztt"],
					era=["13TeV"],
					mass=["0"]
			)
		
			# efficiencies
<<<<<<< Updated upstream
			self.cb.cp().channel(["em"]).process(["ZTTPOSPOL", "ZTTNEGPOL", "ZL", "ZJ", "TT", "VV"]).AddSyst(self.cb, *systematics_library.electron_efficiency_syst_args)
			self.cb.cp().channel(["em"]).process(["ZTTPOSPOL", "ZTTNEGPOL", "ZL", "ZJ", "TT", "VV"]).AddSyst(self.cb, *systematics_library.muon_efficiency_syst_args)
			
			# from Yuta
			self.cb.cp().channel(["em"]).process(["ZL", "ZJ", "W"]).AddSyst(self.cb, *systematics_library.boson_scale_met_syst_args)
			self.cb.cp().channel(["em"]).process(["ZL", "ZJ", "W"]).AddSyst(self.cb, *systematics_library.boson_resolution_met_syst_args)
			self.cb.cp().channel(["em"]).process(["TT", "VV"]).AddSyst(self.cb, *systematics_library.ewk_top_scale_met_syst_args)
			self.cb.cp().channel(["em"]).process(["TT", "VV"]).AddSyst(self.cb, *systematics_library.ewk_top_resolution_met_syst_args)

			# extrapolation uncertainty
			self.cb.cp().channel(["em"]).process(["TT"]).AddSyst(self.cb, *systematics_library.ttj_extrapol_syst_args)
			self.cb.cp().channel(["em"]).process(["W"]).AddSyst(self.cb, *systematics_library.wj_extrapol_syst_args)
			
			# Top pT reweight
			#self.cb.cp().channel(["em"]).process(["TT"]).AddSyst(self.cb, *systematics_library.ttj_syst_args)
=======
			self.cb.cp().channel(["em"]).process(["ZTTPOSPOL", "ZTTNEGPOL", "ZL", "ZJ", "TT", "VV"]).AddSyst(self.cb, *systematics_list.electron_efficiency_syst_args)
			self.cb.cp().channel(["em"]).process(["ZTTPOSPOL", "ZTTNEGPOL", "ZL", "ZJ", "TT", "VV"]).AddSyst(self.cb, *systematics_list.muon_efficiency_syst_args)
			
			# from Yuta
			self.cb.cp().channel(["em"]).process(["ZL", "ZJ", "W"]).AddSyst(self.cb, *systematics_list.boson_scale_met_syst_args)
			self.cb.cp().channel(["em"]).process(["ZL", "ZJ", "W"]).AddSyst(self.cb, *systematics_list.boson_resolution_met_syst_args)
			self.cb.cp().channel(["em"]).process(["TT", "VV"]).AddSyst(self.cb, *systematics_list.ewk_top_scale_met_syst_args)
			self.cb.cp().channel(["em"]).process(["TT", "VV"]).AddSyst(self.cb, *systematics_list.ewk_top_resolution_met_syst_args)

			# extrapolation uncertainty
			self.cb.cp().channel(["em"]).process(["TT"]).AddSyst(self.cb, *systematics_list.ttj_extrapol_syst_args)
			self.cb.cp().channel(["em"]).process(["W"]).AddSyst(self.cb, *systematics_list.wj_extrapol_syst_args)
			
			# Top pT reweight
			#self.cb.cp().channel(["em"]).process(["TT"]).AddSyst(self.cb, *systematics_list.ttj_syst_args)
>>>>>>> Stashed changes

			# ======================================================================
			# All channels
			#self.cb.cp().process(["ZTTPOSPOL", "ZTTNEGPOL"]).AddSyst(self.cb, "ZTTPOSPOL_uniform_2", "ZTTNEGPOL_uniform_2", "lnU", ch.SystMap()(2.0))
		
			# lumi
<<<<<<< Updated upstream
			self.cb.cp().process(["ZTTPOSPOL", "ZTTNEGPOL", "ZL", "ZJ", "TT", "VV"]).AddSyst(self.cb, *systematics_library.lumi_syst_args)
		
			# cross section
			self.cb.cp().process(["ZTTPOSPOL", "ZTTNEGPOL", "ZL", "ZJ"]).AddSyst(self.cb, *systematics_library.zll_cross_section_syst_args)
			self.cb.cp().process(["VV"]).AddSyst(self.cb, *systematics_library.vv_cross_section_syst_args)
			self.cb.cp().process(["TT"]).AddSyst(self.cb, *systematics_library.ttj_cross_section_syst_args)
			self.cb.cp().process(["W"]).AddSyst(self.cb, *systematics_library.wj_cross_section_syst_args)

			# signal acceptance/efficiency
			self.cb.cp().process(["ZTTPOSPOL", "ZTTNEGPOL"]).AddSyst(self.cb, *systematics_library.ztt_pdf_scale_syst_args)
			self.cb.cp().process(["ZTTPOSPOL", "ZTTNEGPOL"]).AddSyst(self.cb, *systematics_library.ztt_qcd_scale_syst_args)

			# QCD systematic
			self.cb.cp().process(["QCD"]).AddSyst(self.cb, *systematics_library.qcd_syst_inclusive_args)
=======
			self.cb.cp().process(["ZTTPOSPOL", "ZTTNEGPOL", "ZL", "ZJ", "TT", "VV"]).AddSyst(self.cb, *systematics_list.lumi_syst_args)
		
			# cross section
			self.cb.cp().process(["ZTTPOSPOL", "ZTTNEGPOL", "ZL", "ZJ"]).AddSyst(self.cb, *systematics_list.zll_cross_section_syst_args)
			self.cb.cp().process(["VV"]).AddSyst(self.cb, *systematics_list.vv_cross_section_syst_args)
			self.cb.cp().process(["TT"]).AddSyst(self.cb, *systematics_list.ttj_cross_section_syst_args)
			self.cb.cp().process(["W"]).AddSyst(self.cb, *systematics_list.wj_cross_section_syst_args)

			# signal acceptance/efficiency
			self.cb.cp().process(["ZTTPOSPOL", "ZTTNEGPOL"]).AddSyst(self.cb, *systematics_list.ztt_pdf_scale_syst_args)
			self.cb.cp().process(["ZTTPOSPOL", "ZTTNEGPOL"]).AddSyst(self.cb, *systematics_list.ztt_qcd_scale_syst_args)

			# QCD systematic
			self.cb.cp().process(["QCD"]).AddSyst(self.cb, *systematics_list.qcd_syst_inclusive_args)
>>>>>>> Stashed changes
			
			# ======================================================================
			# Groups of systematics
			self.cb.SetGroup("syst", [".*"])
		
			if log.isEnabledFor(logging.DEBUG):
				self.cb.PrintAll()

