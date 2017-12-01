# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import CombineHarvester.CombineTools.ch as ch

import HiggsAnalysis.KITHiggsToTauTau.datacards.datacards as datacards
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.systematics_libary as SystLib


class TauEsDatacards(datacards.Datacards):
	def __init__(self, shifts=[], decaymodes=[], quantity="m_2", weight_bins=[], weight_type="pt", year="", mapping_category2binid=None, cb=None):
		super(TauEsDatacards, self).__init__(cb)
		
		if mapping_category2binid is not None:
			self.configs._mapping_category2binid.update(mapping_category2binid)

		##Generate instance of systematic libary, in which the relevant information about the systematics are safed

		systematics_list = SystLib.SystematicLibary()

		# some systematics are only applied to 1-prongs and 1-prong+Pi0s
		decaymodesNoThreeProng = [decaymode for decaymode in decaymodes if decaymode != "ThreeProng"]
		
		all_mc_bkgs = ["ZTT", "ZL", "ZJ", "TTT", "TTJJ", "VVT", "VVJ", "W"]
		all_mc_bkgs_no_W = ["ZTT", "ZL", "ZJ", "TTT", "TTJJ", "VVT", "VVJ"]
		
		if cb is None:
			# ======================================================================
			# MT channel
			self.add_processes(
					channel="mt",
					categories=["mt_"+quantity+"_"+decaymode+"_"+weight_type+"bin"+weight_bin for decaymode in decaymodes for weight_bin in weight_bins],
					bkg_processes=["ZL", "ZJ", "TTJJ", "VVJ", "W", "QCD"],
					sig_processes=["ZTT", "TTT", "VVT"],
					analysis=["ztt"],
					era=["13TeV"],
					mass=shifts
			)
		
			# efficiencies
			if year == "2016":
				self.cb.cp().channel(["mt"]).process(all_mc_bkgs_no_W).AddSyst(self.cb, *systematics_list.trigger_efficiency2016_syst_args)
				self.cb.cp().channel(["mt"]).process(all_mc_bkgs_no_W).AddSyst(self.cb, *systematics_list.muon_efficiency2016_syst_args)
				self.cb.cp().channel(["mt"]).process(["ZTT", "TTT", "VVT"]).AddSyst(self.cb, *systematics_list.tau_efficiency2016_syst_args)
			else:
				self.cb.cp().channel(["mt"]).process(all_mc_bkgs_no_W).AddSyst(self.cb, *systematics_list.muon_efficiency_syst_args)
				self.cb.cp().channel(["mt"]).process(["ZTT", "TTT", "VVT"]).AddSyst(self.cb, *systematics_list.tau_efficiency_syst_args)

			# mu->tau fake ES (only for 1-prongs and 1-prong+Pi0s)
			categoriesForMuFakeTauES = ["mt_"+quantity+"_"+decaymode+"_"+weight_type+"bin"+weight_bin for decaymode in decaymodesNoThreeProng for weight_bin in weight_bins]
			self.cb.cp().channel(["mt"]).process(["ZL"]).bin(categoriesForMuFakeTauES).AddSyst(self.cb, *systematics_list.muFakeTau_es_syst_args)

			# fake-rate
			if year == "2016":
				self.cb.cp().channel(["mt"]).process(["ZL"]).bin(categoriesForMuFakeTauES).AddSyst(self.cb, *systematics_list.muFakeTau2016_syst_args)
			else:
				self.cb.cp().channel(["mt"]).process(["ZL"]).bin(categoriesForMuFakeTauES).AddSyst(self.cb, *systematics_list.eFakeTau_vloose_syst_args)
				self.cb.cp().channel(["mt"]).process(["ZL"]).bin(categoriesForMuFakeTauES).AddSyst(self.cb, *systematics_list.muFakeTau_syst_args)

			# ======================================================================
			# ET channel
			self.add_processes(
					channel="et",
					categories=["et_"+quantity+"_"+decaymode+"_"+weight_type+"bin"+weight_bin for decaymode in decaymodes for weight_bin in weight_bins],
					bkg_processes=["ZL", "ZJ", "TTJJ", "VVJ", "W", "QCD"],
					sig_processes=["ZTT", "TTT", "VVT"],
					analysis=["ztt"],
					era=["13TeV"],
					mass=shifts
			)

			# efficiencies
			if year == "2016":
				self.cb.cp().channel(["et"]).process(all_mc_bkgs_no_W).AddSyst(self.cb, *systematics_list.trigger_efficiency2016_syst_args)
				self.cb.cp().channel(["et"]).process(all_mc_bkgs_no_W).AddSyst(self.cb, *systematics_list.electron_efficiency2016_syst_args)
				self.cb.cp().channel(["et"]).process(["ZTT", "TTT", "VVT"]).AddSyst(self.cb, *systematics_list.tau_efficiency2016_syst_args)
			else:
				self.cb.cp().channel(["et"]).process(all_mc_bkgs_no_W).AddSyst(self.cb, *systematics_list.electron_efficiency_syst_args)
				self.cb.cp().channel(["et"]).process(["ZTT", "TTT", "VVT"]).AddSyst(self.cb, *systematics_list.tau_efficiency_syst_args)
			
			# e->tau fake ES (only for 1-prongs and 1-prong+Pi0s)
			categoriesForEleFakeTauES = ["et_"+quantity+"_"+decaymode+"_"+weight_type+"bin"+weight_bin for decaymode in decaymodesNoThreeProng for weight_bin in weight_bins]
			self.cb.cp().channel(["et"]).process(["ZL"]).bin(categoriesForEleFakeTauES).AddSyst(self.cb, *systematics_list.eleFakeTau_es_syst_args)

			# fake-rate
			if year == "2016":
				self.cb.cp().channel(["et"]).process(["ZL"]).bin(categoriesForEleFakeTauES).AddSyst(self.cb, *systematics_list.eFakeTau2016_syst_args)
			else:
				self.cb.cp().channel(["et"]).process(["ZL"]).bin(categoriesForEleFakeTauES).AddSyst(self.cb, *systematics_list.eFakeTau_tight_syst_args)

			# ======================================================================
			# All channels
		
			# lumi
			# (hopefully) temporary fix
			if year == "2016":
				self.cb.cp().process(all_mc_bkgs_no_W).AddSyst(self.cb, *systematics_list.lumi2016_syst_args)
			else:
				self.cb.cp().process(all_mc_bkgs_no_W).AddSyst(self.cb, *systematics_list.lumi_syst_args)

			# cross section
			self.cb.cp().process(["ZTT", "ZL", "ZJ"]).AddSyst(self.cb, *systematics_list.ztt_cross_section_syst_args)
			if year == "2016":
				self.cb.cp().process(["VVT", "VVJ"]).AddSyst(self.cb, *systematics_list.vv_cross_section2016_syst_args)
			else:
				self.cb.cp().process(["VVT", "VVJ"]).AddSyst(self.cb, *systematics_list.vv_cross_section_syst_args)
			self.cb.cp().process(["TTT", "TTJJ"]).AddSyst(self.cb, *systematics_list.ttj_cross_section_syst_args)

			# signal acceptance/efficiency
			self.cb.cp().process(["ZTT"]).AddSyst(self.cb, *systematics_list.ztt_pdf_scale_syst_args)
			self.cb.cp().process(["ZTT"]).AddSyst(self.cb, *systematics_list.ztt_qcd_scale_syst_args)

			# QCD systematic
			self.cb.cp().channel(["mt", "et"]).process(["QCD"]).AddSyst(self.cb, "QCD_Extrap_Iso_nonIso_lt_13TeV", "lnN", ch.SystMap()(1.20))
			self.cb.cp().channel(["mt", "et"]).process(["QCD"]).AddSyst(self.cb, "WSFUncert_lt_13TeV", "shape", ch.SystMap()(1.0))

			# W+jets high->low mt extrapolation uncertainty
			self.cb.cp().channel(["mt", "et"]).process(["W"]).AddSyst(self.cb, "WHighMTtoLowMT_13TeV", "lnN", ch.SystMap()(1.10))

			if year == "2016":
				self.cb.cp().channel(["mt", "et"]).process(["ZTT", "TTT", "VVT"]).AddSyst(self.cb, *systematics_list.tau_efficiency2016_corr_syst_args)
			else:
				self.cb.cp().channel(["mt", "et"]).process(["ZTT", "TTT", "VV"]).AddSyst(self.cb, *systematics_list.tau_efficiency_corr_syst_args)

			# jet->tau fakes
			if year == "2016":
				self.cb.cp().channel(["mt", "et"]).process(["ZJ", "TTJJ", "VVJ"]).AddSyst(self.cb, "CMS_htt_jetToTauFake_13TeV", "shape", ch.SystMap()(1.0))
			else:
				self.cb.cp().channel(["mt", "et"]).process(["ZJ", "TTJJ", "VVJ"]).AddSyst(self.cb, *systematics_list.jetFakeTau_syst_args)

			# MET ES
			self.cb.cp().channel(["mt", "et"]).process(all_mc_bkgs).AddSyst(self.cb, "CMS_scale_met_clustered_13TeV", "shape", ch.SystMap()(1.0))
			self.cb.cp().channel(["mt", "et"]).process(all_mc_bkgs).AddSyst(self.cb, "CMS_scale_met_unclustered_13TeV", "shape", ch.SystMap()(1.0))

			# ttbar shape
			self.cb.cp().channel(["mt", "et"]).process(["TTT", "TTJJ"]).AddSyst(self.cb, *systematics_list.ttj_syst_args)

			# dy shape
			self.cb.cp().channel(["mt", "et"]).process(["ZTT", "ZL", "ZJ"]).AddSyst(self.cb, *systematics_list.dy_shape_syst_args)
		
			if log.isEnabledFor(logging.DEBUG):
				self.cb.PrintAll()
