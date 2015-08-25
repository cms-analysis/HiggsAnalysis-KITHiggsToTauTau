# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import HiggsAnalysis.KITHiggsToTauTau.datacards.datacards as datacards


class SMHttDatacards(datacards.Datacards):
	def __init__(self, higgs_masses=["125"], cb=None):
		super(SMHttDatacards, self).__init__(cb)
		signal_processes = ["ggH", "qqH", "VH"]
		
		# ======================================================================
		# MT channel
		self.add_processes(
				channel="mt",
				categories=["inclusive", "zerojet", "onejet", "twojet"],
				bkg_processes=["ZTT", "TTJ", "VV", "WJ", "QCD"],
				sig_processes=signal_processes,
				analysis=["ztt"],
				era=["13TeV"],
				mass=higgs_masses
		)
		
		# efficiencies
		self.cb.cp().channel(["mt"]).process(["ZTT", "TTJ", "VV", "WJ", "QCD"]).AddSyst(self.cb, *self.muon_efficieny_syst_args)
		self.cb.cp().channel(["mt"]).process(["ZTT", "TTJ", "VV"]).AddSyst(self.cb, *self.tau_efficieny_syst_args)
		
		# ======================================================================
		# ET channel
		self.add_processes(
				channel="et",
				categories=["inclusive", "zerojet", "onejet", "twojet"],
				bkg_processes=["ZTT", "TTJ", "VV", "WJ", "QCD"],
				sig_processes=signal_processes,
				analysis=["ztt"],
				era=["13TeV"],
				mass=higgs_masses
		)
		
		# efficiencies
		self.cb.cp().channel(["et"]).process(["ZTT", "TTJ", "VV", "WJ", "QCD"]).AddSyst(self.cb, *self.electron_efficieny_syst_args)
		self.cb.cp().channel(["et"]).process(["ZTT", "TTJ", "VV"]).AddSyst(self.cb, *self.tau_efficieny_syst_args)
		
		# ======================================================================
		# EM channel
		self.add_processes(
				channel="em",
				categories=["inclusive", "zerojet", "onejet", "twojet"],
				bkg_processes=["ZTT", "TTJ", "VV", "WJ"],
				sig_processes=signal_processes,
				analysis=["ztt"],
				era=["13TeV"],
				mass=higgs_masses
		)
		
		# efficiencies
		self.cb.cp().channel(["em"]).process(["ZTT", "TTJ", "VV", "WJ", "QCD"]).AddSyst(self.cb, *self.electron_efficieny_syst_args)
		self.cb.cp().channel(["em"]).process(["ZTT", "TTJ", "VV", "WJ", "QCD"]).AddSyst(self.cb, *self.muon_efficieny_syst_args)
		
		# ======================================================================
		# TT channel
		# TODO
		
		# ======================================================================
		# All channels
		
		# lumi
		self.cb.cp().process(["ZTT", "TTJ", "VV", "WJ"]).AddSyst(self.cb, *self.lumi_syst_args)
		self.cb.cp().signals().AddSyst(self.cb, *self.lumi_syst_args)
		
		# cross section
		self.cb.cp().process(["ZTT"]).AddSyst(self.cb, *self.ztt_cross_section_syst_args)
		self.cb.cp().process(["TTJ"]).AddSyst(self.cb, *self.ttj_cross_section_syst_args)
		self.cb.cp().process(["VV"]).AddSyst(self.cb, *self.vv_cross_section_syst_args)
		self.cb.cp().process(["WJ"]).AddSyst(self.cb, *self.wj_cross_section_syst_args)
		
		if log.isEnabledFor(logging.DEBUG):
			self.cb.PrintAll()
