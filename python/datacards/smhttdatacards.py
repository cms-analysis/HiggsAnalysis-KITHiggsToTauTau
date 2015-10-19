# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import HiggsAnalysis.KITHiggsToTauTau.datacards.datacards as datacards


class SMHttDatacards(datacards.Datacards):
	def __init__(self, higgs_masses=["125"], cb=None):
		super(SMHttDatacards, self).__init__(cb)
		
		if cb is None:
			signal_processes = ["ggH", "qqH", "WH", "ZH"]
		
			# ======================================================================
			# MT channel
			self.add_processes(
					channel="mt",
					categories=["mt_"+category for category in ["0jet_low", "0jet_high", "1jet_low", "1jet_high", "2jet_vbf"]],
					bkg_processes=["ZTT", "ZLL", "TTJ", "VV", "WJ", "QCD"],
					sig_processes=signal_processes,
					analysis=["htt"],
					era=["13TeV"],
					mass=higgs_masses
			)
		
			# efficiencies
			self.cb.cp().channel(["mt"]).process(["ZTT", "ZLL", "TTJ", "VV", "WJ", "QCD"]).AddSyst(self.cb, *self.muon_efficieny_syst_args)
			self.cb.cp().channel(["mt"]).signals().AddSyst(self.cb, *self.muon_efficieny_syst_args)
			
			self.cb.cp().channel(["mt"]).process(["ZTT", "TTJ", "VV"]).AddSyst(self.cb, *self.tau_efficieny_syst_args)
			self.cb.cp().channel(["mt"]).signals().AddSyst(self.cb, *self.tau_efficieny_syst_args)
			
			# Tau ES
			self.cb.cp().channel(["mt"]).process(["ZTT"]).AddSyst(self.cb, *self.tau_es_syst_args)
			self.cb.cp().channel(["mt"]).signals().AddSyst(self.cb, *self.tau_es_syst_args)

			# fake-rate
			self.cb.cp().channel(["mt"]).process(["ZLL"]).AddSyst(self.cb, *self.zllFakeTau_syst_args)
			
			# ======================================================================
			# ET channel
			self.add_processes(
					channel="et",
					categories=["et_"+category for category in ["0jet_low", "0jet_high", "1jet_low", "1jet_high", "2jet_vbf"]],
					bkg_processes=["ZTT", "ZLL", "TTJ", "VV", "WJ", "QCD"],
					sig_processes=signal_processes,
					analysis=["htt"],
					era=["13TeV"],
					mass=higgs_masses
			)
		
			# efficiencies
			self.cb.cp().channel(["et"]).process(["ZTT", "ZLL", "TTJ", "VV", "WJ", "QCD"]).AddSyst(self.cb, *self.electron_efficieny_syst_args)
			self.cb.cp().channel(["et"]).signals().AddSyst(self.cb, *self.electron_efficieny_syst_args)
			
			self.cb.cp().channel(["et"]).process(["ZTT", "TTJ", "VV"]).AddSyst(self.cb, *self.tau_efficieny_syst_args)
			self.cb.cp().channel(["et"]).signals().AddSyst(self.cb, *self.tau_efficieny_syst_args)
			
			# Tau ES
			self.cb.cp().channel(["et"]).process(["ZTT"]).AddSyst(self.cb, *self.tau_es_syst_args)
			self.cb.cp().channel(["et"]).signals().AddSyst(self.cb, *self.tau_es_syst_args)

			# fake-rate
			self.cb.cp().channel(["et"]).process(["ZLL"]).AddSyst(self.cb, *self.zllFakeTau_syst_args)
			
			# ======================================================================
			# EM channel
			self.add_processes(
					channel="em",
					categories=["em_"+category for category in ["0jet_low", "0jet_high", "1jet_low", "1jet_high", "2jet_vbf"]],
					bkg_processes=["ZTT", "ZLL", "TTJ", "VV", "WJ", "QCD"],
					sig_processes=signal_processes,
					analysis=["htt"],
					era=["13TeV"],
					mass=higgs_masses
			)
		
			# efficiencies
			self.cb.cp().channel(["em"]).process(["ZTT", "ZLL", "TTJ", "VV", "WJ", "QCD"]).AddSyst(self.cb, *self.electron_efficieny_syst_args)
			self.cb.cp().channel(["em"]).signals().AddSyst(self.cb, *self.electron_efficieny_syst_args)
			
			self.cb.cp().channel(["em"]).process(["ZTT", "ZLL", "TTJ", "VV", "WJ", "QCD"]).AddSyst(self.cb, *self.muon_efficieny_syst_args)
			self.cb.cp().channel(["em"]).signals().AddSyst(self.cb, *self.muon_efficieny_syst_args)
			
			# ======================================================================
			# TT channel
			self.add_processes(
					channel="tt",
					categories=["tt_"+category for category in ["inclusive"]],
					bkg_processes=["ZTT", "ZLL", "TTJ", "VV", "WJ", "QCD"],
					sig_processes=signal_processes,
					analysis=["htt"],
					era=["13TeV"],
					mass=higgs_masses
			)
		
			# efficiencies
			self.cb.cp().channel(["tt"]).process(["ZTT", "TTJ", "VV"]).AddSyst(self.cb, *self.tau_efficieny_syst_args)
			self.cb.cp().channel(["tt"]).signals().AddSyst(self.cb, *self.tau_efficieny_syst_args)
			
			# Tau ES
			self.cb.cp().channel(["tt"]).process(["ZTT"]).AddSyst(self.cb, *self.tau_es_syst_args)
			self.cb.cp().channel(["tt"]).signals().AddSyst(self.cb, *self.tau_es_syst_args)

			# fake-rate
			self.cb.cp().channel(["tt"]).process(["ZLL"]).AddSyst(self.cb, *self.zllFakeTau_syst_args)
			
			# ======================================================================
			# All channels
		
			# lumi
			self.cb.cp().process(["ZTT", "ZLL", "TTJ", "VV", "WJ"]).AddSyst(self.cb, *self.lumi_syst_args)
			self.cb.cp().signals().AddSyst(self.cb, *self.lumi_syst_args)
			
			# jets
			self.cb.cp().AddSyst(self.cb, *self.jec_syst_args)
			self.cb.cp().AddSyst(self.cb, *self.btag_efficieny_syst_args)

			# QCD systematic
			self.cb.cp().process(["QCD"]).AddSyst(self.cb, *self.qcd_syst_args)
		
			# cross section
			self.cb.cp().process(["ZTT", "ZLL"]).AddSyst(self.cb, *self.ztt_cross_section_syst_args)
			self.cb.cp().process(["TTJ"]).channel(["mt", "et", "tt"]).AddSyst(self.cb, *self.ttj_cross_section_syst_args) # automatically in other channels determined
			self.cb.cp().process(["VV"]).AddSyst(self.cb, *self.vv_cross_section_syst_args)
			self.cb.cp().process(["WJ"]).channel(["em", "tt"]).AddSyst(self.cb, *self.wj_cross_section_syst_args) # automatically in other channels determined
		
			# signal
			self.cb.cp().signals().AddSyst(self.cb, *self.htt_qcd_scale_syst_args)
			self.cb.cp().signals().AddSyst(self.cb, *self.htt_pdf_scale_syst_args)
			self.cb.cp().signals().AddSyst(self.cb, *self.htt_ueps_syst_args)
		
			if log.isEnabledFor(logging.DEBUG):
				self.cb.PrintAll()

