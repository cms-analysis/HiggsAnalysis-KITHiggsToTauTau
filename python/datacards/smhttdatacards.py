# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.categories as Categories
import HiggsAnalysis.KITHiggsToTauTau.datacards.datacards as datacards
import CombineHarvester.CombineTools.ch as ch

class SMHttDatacards(datacards.Datacards):
	def __init__(self, higgs_masses=["125"], cb=None):
		super(SMHttDatacards, self).__init__(cb)

		if cb is None:
			signal_processes = ["ggH", "qqH", "WH", "ZH"]

			# ======================================================================
			# MT channel
			self.add_processes(
					channel="mt",
					categories=Categories.CategoriesDict().getCategories(["mt"])["mt"],
					bkg_processes=["ZTT", "ZL", "ZJ", "TT", "VV", "W", "QCD"],
					sig_processes=signal_processes,
					analysis=["htt"],
					era=["13TeV"],
					mass=higgs_masses
			)

			# efficiencies
			self.cb.cp().channel(["mt"]).process(["ZTT", "ZL", "ZJ", "TT", "VV"]).AddSyst(self.cb, *self.muon_efficieny_syst_args)
			self.cb.cp().channel(["mt"]).signals().AddSyst(self.cb, *self.muon_efficieny_syst_args)

			self.cb.cp().channel(["mt"]).process(["ZTT", "TT", "VV"]).AddSyst(self.cb, *self.tau_efficieny_syst_args)
			self.cb.cp().channel(["mt"]).signals().AddSyst(self.cb, *self.tau_efficieny_syst_args)
			self.cb.cp().channel(["mt"]).process(["ZTT", "TT", "VV"]).AddSyst(self.cb, *self.tau_efficieny_corr_syst_args)
			self.cb.cp().channel(["mt"]).signals().AddSyst(self.cb, *self.tau_efficieny_corr_syst_args)

			# Tau ES
			self.cb.cp().channel(["mt"]).process(["ZTT"]).AddSyst(self.cb, *self.tau_es_syst_args)
			self.cb.cp().channel(["mt"]).signals().AddSyst(self.cb, *self.tau_es_syst_args)

			# fake-rate
			self.cb.cp().channel(["mt"]).process(["ZL", "ZJ"]).AddSyst(self.cb, *self.zllFakeTau_syst_args)
			
			for category in Categories.CategoriesDict().getCategories(["mt"], False)["mt"]:
				self.cb.cp().channel(["mt"]).bin(["mt_"+category]).process(["ZTT"]).AddSyst(self.cb, "n_zll_"+category+"_norm", "rateParam", ch.SystMap()(1.0))

			# ======================================================================
			# ET channel
			self.add_processes(
					channel="et",
					categories=Categories.CategoriesDict().getCategories(["et"])["et"],
					bkg_processes=["ZTT", "ZL", "ZJ", "TT", "VV", "W", "QCD"],
					sig_processes=signal_processes,
					analysis=["htt"],
					era=["13TeV"],
					mass=higgs_masses
			)

			# efficiencies
			self.cb.cp().channel(["et"]).process(["ZTT", "ZL", "ZJ", "TT", "VV"]).AddSyst(self.cb, *self.electron_efficieny_syst_args)
			self.cb.cp().channel(["et"]).signals().AddSyst(self.cb, *self.electron_efficieny_syst_args)

			self.cb.cp().channel(["et"]).process(["ZTT", "TT", "VV"]).AddSyst(self.cb, *self.tau_efficieny_syst_args)
			self.cb.cp().channel(["et"]).signals().AddSyst(self.cb, *self.tau_efficieny_syst_args)

			# Tau ES
			self.cb.cp().channel(["et"]).process(["ZTT"]).AddSyst(self.cb, *self.tau_es_syst_args)
			self.cb.cp().channel(["et"]).signals().AddSyst(self.cb, *self.tau_es_syst_args)

			# fake-rate
			self.cb.cp().channel(["et"]).process(["ZL", "ZJ"]).AddSyst(self.cb, *self.zllFakeTau_syst_args)
			
			for category in Categories.CategoriesDict().getCategories(["et"], False)["et"]:
				self.cb.cp().channel(["et"]).bin(["et_"+category]).process(["ZTT"]).AddSyst(self.cb, "n_zll_"+category+"_norm", "rateParam", ch.SystMap()(1.0))

			# ======================================================================
			# EM channel
			self.add_processes(
					channel="em",
					categories=Categories.CategoriesDict().getCategories(["em"])["em"],
					bkg_processes=["ZTT", "ZLL", "TT", "VV", "W", "QCD"],
					sig_processes=signal_processes,
					analysis=["htt"],
					era=["13TeV"],
					mass=higgs_masses
			)

			# efficiencies
			self.cb.cp().channel(["em"]).process(["ZTT", "ZLL", "TT", "VV"]).AddSyst(self.cb, *self.electron_efficieny_syst_args)
			self.cb.cp().channel(["em"]).signals().AddSyst(self.cb, *self.electron_efficieny_syst_args)

			self.cb.cp().channel(["em"]).process(["ZTT", "ZLL", "TT", "VV"]).AddSyst(self.cb, *self.muon_efficieny_syst_args)
			self.cb.cp().channel(["em"]).signals().AddSyst(self.cb, *self.muon_efficieny_syst_args)
		
			for category in Categories.CategoriesDict().getCategories(["em"], False)["em"]:
				self.cb.cp().channel(["em"]).bin(["em_"+category]).process(["ZTT"]).AddSyst(self.cb, "n_zll_"+category+"_norm", "rateParam", ch.SystMap()(1.0))

			# ======================================================================
			# TT channel
			self.add_processes(
					channel="tt",
					categories=Categories.CategoriesDict().getCategories(["tt"])["tt"],
					bkg_processes=["ZTT", "ZL", "ZJ", "TT", "VV", "W", "QCD"],
					sig_processes=signal_processes,
					analysis=["htt"],
					era=["13TeV"],
					mass=higgs_masses
			)

			# efficiencies
			self.cb.cp().channel(["tt"]).process(["ZTT", "TT", "VV"]).AddSyst(self.cb, *self.tau_efficieny_syst_args)
			self.cb.cp().channel(["tt"]).signals().AddSyst(self.cb, *self.tau_efficieny_syst_args)

			# Tau ES
			self.cb.cp().channel(["tt"]).process(["ZTT"]).AddSyst(self.cb, *self.tau_es_syst_args)
			self.cb.cp().channel(["tt"]).signals().AddSyst(self.cb, *self.tau_es_syst_args)

			# fake-rate
			self.cb.cp().channel(["tt"]).process(["ZL", "ZJ"]).AddSyst(self.cb, *self.zllFakeTau_syst_args)
			
			for category in Categories.CategoriesDict().getCategories(["tt"], False)["tt"]:
				self.cb.cp().channel(["tt"]).bin(["tt_"+category]).process(["ZTT"]).AddSyst(self.cb, "n_zll_"+category+"_norm", "rateParam", ch.SystMap()(1.0))
			
			# ======================================================================
			# MM channel
			self.add_processes(
					channel="mm",
					categories=Categories.CategoriesDict().getCategories(["mm"])["mm"],
					bkg_processes=["ZTT", "ZLL", "TT", "VV", "W", "QCD"],
					sig_processes=signal_processes,
					analysis=["htt"],
					era=["13TeV"],
					mass=higgs_masses
			)
			
			self.cb.cp().channel(["mm"]).process(["ZTT", "ZLL", "TT", "VV"]).AddSyst(self.cb, *self.muon_efficieny_syst_args)
			self.cb.cp().channel(["mm"]).signals().AddSyst(self.cb, *self.muon_efficieny_syst_args)
			
			for category in Categories.CategoriesDict().getCategories(["mm"], False)["mm"]:
				self.cb.cp().channel(["mm"]).bin(["mm_"+category]).process(["ZLL"]).AddSyst(self.cb, "n_zll_"+category+"_norm", "rateParam", ch.SystMap()(1.0))

			# ======================================================================
			# All channels

			# lumi
			self.cb.cp().signals().AddSyst(self.cb, *self.lumi_syst_args)
			self.cb.cp().process(["ZTT", "ZLL", "ZL", "ZJ", "TT", "W", "VV"]).AddSyst(self.cb, *self.lumi_syst_args)

			# jets
			self.cb.cp().process(["ZTT", "ZL", "ZJ", "TT", "VV", "W"]).AddSyst(self.cb, *self.jec_syst_args)
			self.cb.cp().signals().AddSyst(self.cb, *self.jec_syst_args)
			self.cb.cp().process(["TT"]).AddSyst(self.cb, *self.btag_efficieny_syst_args)

			# MET
			self.cb.cp().AddSyst(self.cb, *self.met_scale_syst_args)

			# QCD systematic
			self.cb.cp().process(["QCD"]).channel(["tt"]).AddSyst(self.cb, *self.qcd_syst_args) # automatically in other channels
			#self.cb.cp().process(["QCD"]).AddSyst(self.cb, *self.qcd_syst_args)

			# cross section
			self.cb.cp().process(["ZTT", "ZL", "ZJ","ZLL"]).AddSyst(self.cb, *self.ztt_cross_section_syst_args)
			self.cb.cp().process(["TT"]).channel(["mt", "et", "tt"]).AddSyst(self.cb, *self.ttj_cross_section_syst_args) # automatically in other channels determined
			#self.cb.cp().process(["TT"]).AddSyst(self.cb, *self.ttj_cross_section_syst_args)
			self.cb.cp().process(["VV"]).AddSyst(self.cb, *self.vv_cross_section_syst_args)
			self.cb.cp().process(["W"]).channel(["em", "tt"]).AddSyst(self.cb, *self.wj_cross_section_syst_args) # automatically in other channels determined
			#self.cb.cp().process(["W"]).AddSyst(self.cb, *self.wj_cross_section_syst_args)

			# signal
			self.cb.cp().signals().AddSyst(self.cb, *self.htt_qcd_scale_syst_args)
			self.cb.cp().signals().AddSyst(self.cb, *self.htt_pdf_scale_syst_args)
			self.cb.cp().signals().AddSyst(self.cb, *self.htt_ueps_syst_args)

			if log.isEnabledFor(logging.DEBUG):
				self.cb.PrintAll()


# simplified version just for the purpose of datacard synchronization (no systematics)
class SMHttDatacardsForSync(datacards.Datacards):
	def __init__(self, higgs_masses=["125"], cb=None):
		super(SMHttDatacardsForSync, self).__init__(cb)

		if cb is None:
			signal_processes = []

			# ======================================================================
			# MT channel
			self.add_processes(
					channel="mt",
					categories=["mt_"+category for category in ["inclusivemt40"]],
					bkg_processes=["ZTT", "ZL", "ZJ", "TT", "VV", "W", "QCD"],
					sig_processes=signal_processes,
					analysis=["htt"],
					era=["13TeV"],
					mass=higgs_masses
			)

			# ======================================================================
			# ET channel
			self.add_processes(
					channel="et",
					categories=["et_"+category for category in ["inclusivemt40"]],
					bkg_processes=["ZTT", "ZL", "ZJ", "TT", "VV", "W", "QCD"],
					sig_processes=signal_processes,
					analysis=["htt"],
					era=["13TeV"],
					mass=higgs_masses
			)

			# ======================================================================
			# EM channel
			self.add_processes(
					channel="em",
					categories=["em_"+category for category in []],
					bkg_processes=["ZTT", "ZLL", "TT", "VV", "W", "QCD"],
					sig_processes=signal_processes,
					analysis=["htt"],
					era=["13TeV"],
					mass=higgs_masses
			)

			# ======================================================================
			# TT channel
			self.add_processes(
					channel="tt",
					categories=["tt_"+category for category in []],
					bkg_processes=["ZTT", "ZL", "ZJ", "TT", "VV", "W", "QCD"],
					sig_processes=signal_processes,
					analysis=["htt"],
					era=["13TeV"],
					mass=higgs_masses
			)

			if log.isEnabledFor(logging.DEBUG):
				self.cb.PrintAll()
