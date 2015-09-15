# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import combineharvester as ch

import HiggsAnalysis.KITHiggsToTauTau.datacards.datacards as datacards


class ZttXsecDatacards(datacards.Datacards):
	def __init__(self, cb=None):
		super(ZttXsecDatacards, self).__init__(cb)
		
		if cb is None:
			# ======================================================================
			# MT channel
			self.add_processes(
					channel="mt",
					categories=["mt_"+category for category in ["zerojet_inclusive", "onejet_inclusive", "twojet_inclusive"]],
					bkg_processes=["ZLL", "TTJ", "VV", "WJ", "QCD"],
					sig_processes=["ZTT"],
					analysis=["ztt"],
					era=["13TeV"],
					mass=["90"]
			)
		
			# efficiencies
			self.cb.cp().channel(["mt"]).process(["ZTT", "ZLL", "TTJ", "VV", "WJ", "QCD"]).AddSyst(self.cb, *self.muon_efficieny_syst_args)
			self.cb.cp().channel(["mt"]).process(["ZTT", "TTJ", "VV"]).AddSyst(self.cb, *self.tau_efficieny_syst_args)
		
			# ======================================================================
			# ET channel
			self.add_processes(
					channel="et",
					categories=["et_"+category for category in ["zerojet_inclusive", "onejet_inclusive", "twojet_inclusive"]],
					bkg_processes=["ZLL", "TTJ", "VV", "WJ", "QCD"],
					sig_processes=["ZTT"],
					analysis=["ztt"],
					era=["13TeV"],
					mass=["90"]
			)
		
			# efficiencies
			self.cb.cp().channel(["et"]).process(["ZTT", "ZLL", "TTJ", "VV", "WJ", "QCD"]).AddSyst(self.cb, *self.electron_efficieny_syst_args)
			self.cb.cp().channel(["et"]).process(["ZTT", "TTJ", "VV"]).AddSyst(self.cb, *self.tau_efficieny_syst_args)
		
			# ======================================================================
			# EM channel
			self.add_processes(
					channel="em",
					categories=["em_"+category for category in ["zerojet_inclusive", "onejet_inclusive", "twojet_inclusive"]],
					bkg_processes=["TTJ", "VV", "WJ", "QCD"],
					sig_processes=["ZTT"],
					analysis=["ztt"],
					era=["13TeV"],
					mass=["90"]
			)
		
			# efficiencies
			self.cb.cp().channel(["em"]).process(["ZTT", "TTJ", "VV", "WJ", "QCD"]).AddSyst(self.cb, *self.electron_efficieny_syst_args)
			self.cb.cp().channel(["em"]).process(["ZTT", "TTJ", "VV", "WJ", "QCD"]).AddSyst(self.cb, *self.muon_efficieny_syst_args)
		
			# ======================================================================
			# TT channel
			self.add_processes(
					channel="tt",
					categories=["tt_"+category for category in ["zerojet_inclusive", "onejet_inclusive", "twojet_inclusive"]],
					bkg_processes=["TTJ", "VV", "WJ"],
					sig_processes=["ZTT"],
					analysis=["ztt"],
					era=["13TeV"],
					mass=["90"]
			)
		
			# efficiencies
			self.cb.cp().channel(["mt"]).process(["ZTT", "TTJ", "VV"]).AddSyst(self.cb, *self.tau_efficieny_syst_args)
		
			# ======================================================================
			# All channels
			#self.cb.cp().process(["ZTT"]).AddSyst(self.cb, "ZTT_uniform_2", "lnU", ch.SystMap()(2.0))
		
			# lumi
			self.cb.cp().process(["ZTT", "ZLL", "TTJ", "VV", "WJ"]).AddSyst(self.cb, *self.lumi_syst_args)
			
			# JEC
			self.cb.cp().AddSyst(self.cb, *self.jec_syst_args)
		
			# cross section
			self.cb.cp().process(["ZTT"]).AddSyst(self.cb, *self.ztt_cross_section_syst_args)
			self.cb.cp().process(["TTJ"]).AddSyst(self.cb, *self.ttj_cross_section_syst_args)
			self.cb.cp().process(["VV"]).AddSyst(self.cb, *self.vv_cross_section_syst_args)
			self.cb.cp().process(["WJ"]).AddSyst(self.cb, *self.wj_cross_section_syst_args)
		
			if log.isEnabledFor(logging.DEBUG):
				self.cb.PrintAll()


class ZttEffDatacards(datacards.Datacards):
	def __init__(self, cb=None):
		super(ZttEffDatacards, self).__init__(cb)
		
		if cb is None:
			# ======================================================================
			# MT channel
			self.add_processes(
					channel="mt",
					categories=["mt_"+category for category in ["idpass", "idfail"]],
					bkg_processes=["ZLL", "TTJ", "VV", "WJ", "QCD"],
					sig_processes=["ZTT"],
					analysis=["ztt"],
					era=["13TeV"],
					mass=["90"]
			)
		
			# efficiencies
			self.cb.cp().channel(["mt"]).process(["ZTT", "ZLL", "TTJ", "VV", "WJ", "QCD"]).AddSyst(self.cb, *self.muon_efficieny_syst_args)
			self.cb.cp().channel(["mt"]).process(["ZTT", "TTJ", "VV"]).AddSyst(self.cb, *self.tau_efficieny_syst_args)
		
			# ======================================================================
			# ET channel
			self.add_processes(
					channel="et",
					categories=["et_"+category for category in ["idpass", "idfail"]],
					bkg_processes=["ZLL", "TTJ", "VV", "WJ", "QCD"],
					sig_processes=["ZTT"],
					analysis=["ztt"],
					era=["13TeV"],
					mass=["90"]
			)
		
			# efficiencies
			self.cb.cp().channel(["et"]).process(["ZTT", "ZLL", "TTJ", "VV", "WJ", "QCD"]).AddSyst(self.cb, *self.electron_efficieny_syst_args)
			self.cb.cp().channel(["et"]).process(["ZTT", "TTJ", "VV"]).AddSyst(self.cb, *self.tau_efficieny_syst_args)
		
			# ======================================================================
			# All channels
			# lumi
			self.cb.cp().process(["ZTT", "ZLL", "TTJ", "VV", "WJ"]).AddSyst(self.cb, *self.lumi_syst_args)
			
			# JEC
			self.cb.cp().AddSyst(self.cb, *self.jec_syst_args)
		
			# cross section
			self.cb.cp().process(["ZTT"]).AddSyst(self.cb, *self.ztt_cross_section_syst_args)
			self.cb.cp().process(["TTJ"]).AddSyst(self.cb, *self.ttj_cross_section_syst_args)
			self.cb.cp().process(["VV"]).AddSyst(self.cb, *self.vv_cross_section_syst_args)
			self.cb.cp().process(["WJ"]).AddSyst(self.cb, *self.wj_cross_section_syst_args)
		
			if log.isEnabledFor(logging.DEBUG):
				self.cb.PrintAll()

