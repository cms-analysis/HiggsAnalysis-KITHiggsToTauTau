# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import CombineHarvester.CombineTools.ch as ch

import HiggsAnalysis.KITHiggsToTauTau.datacards.datacards as datacards


class ZttXsecDatacards(datacards.Datacards):
	def __init__(self, cb=None, model='default'):
		super(ZttXsecDatacards, self).__init__(cb)
		
		if cb is None:
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
			self.cb.cp().channel(["mt"]).process(["ZTT", "ZL", "ZJ", "TT", "VV"]).AddSyst(self.cb, *self.muon_efficieny_syst_args)
			if "taueff" not in model:
				self.cb.cp().channel(["mt"]).process(["ZTT", "TT", "VV"]).AddSyst(self.cb, *self.tau_efficieny_syst_args)

			# Tau ES
			self.cb.cp().channel(["mt"]).process(["ZTT"]).AddSyst(self.cb, *self.tau_es_syst_args)

			# fake-rate
			self.cb.cp().channel(["mt"]).process(["ZL", "ZJ"]).AddSyst(self.cb, *self.zllFakeTau_syst_args)
		
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
			self.cb.cp().channel(["et"]).process(["ZTT", "ZL", "ZJ", "TT", "VV"]).AddSyst(self.cb, *self.electron_efficieny_syst_args)
			if "taueff" not in model:
				self.cb.cp().channel(["et"]).process(["ZTT", "TT", "VV"]).AddSyst(self.cb, *self.tau_efficieny_syst_args)

			# Tau ES
			self.cb.cp().channel(["et"]).process(["ZTT"]).AddSyst(self.cb, *self.tau_es_syst_args)

			# fake-rate
			self.cb.cp().channel(["et"]).process(["ZL", "ZJ"]).AddSyst(self.cb, *self.zllFakeTau_syst_args)
		
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
			self.cb.cp().channel(["em"]).process(["ZTT", "ZLL", "TT", "VV", "W", "QCD"]).AddSyst(self.cb, *self.electron_efficieny_syst_args)
			self.cb.cp().channel(["em"]).process(["ZTT", "ZLL", "TT", "VV", "W", "QCD"]).AddSyst(self.cb, *self.muon_efficieny_syst_args)
		
			# ======================================================================
			# All channels
			#self.cb.cp().process(["ZTT"]).AddSyst(self.cb, "ZTT_uniform_2", "lnU", ch.SystMap()(2.0))
		
			# lumi
			self.cb.cp().process(["ZTT", "ZLL", "ZL", "ZJ", "TT", "W", "VV", "QCD"]).AddSyst(self.cb, *self.lumi_syst_args)
		
			# cross section
			self.cb.cp().process(["TT"]).AddSyst(self.cb, *self.ttj_cross_section_syst_args)
			self.cb.cp().process(["VV"]).AddSyst(self.cb, *self.vv_cross_section_syst_args)
			self.cb.cp().process(["W"]).AddSyst(self.cb, *self.wj_cross_section_syst_args)

			# QCD systematic
			self.cb.cp().process(["QCD"]).AddSyst(self.cb, *self.qcd_syst_args)
		
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
					categories=["mt_"+category for category in ["tauidpass", "tauidfail"]],
					bkg_processes=["ZL", "ZJ", "TT", "VV", "W", "QCD"],
					sig_processes=["ZTT"],
					analysis=["ztt"],
					era=["13TeV"],
					mass=["90"]
			)
		
			# efficiencies
			self.cb.cp().channel(["mt"]).process(["ZL", "ZJ", "TT", "VV", "W", "QCD"]).AddSyst(self.cb, *self.muon_efficieny_syst_args)
		
			# Tau ES
			self.cb.cp().channel(["mt"]).process(["ZTT", "ZL", "ZJ"]).AddSyst(self.cb, *self.tau_es_syst_args)

			# fake-rate
			self.cb.cp().channel(["mt"]).process(["ZL", "ZJ"]).AddSyst(self.cb, *self.zllFakeTau_syst_args)
		
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
			self.cb.cp().channel(["et"]).process(["ZL", "ZJ", "TT", "VV", "W", "QCD"]).AddSyst(self.cb, *self.electron_efficieny_syst_args)
			self.cb.cp().channel(["et"]).process(["TT", "VV"]).AddSyst(self.cb, *self.tau_efficieny_syst_args)
			
			# Tau ES
			self.cb.cp().channel(["et"]).process(["ZTT", "ZL", "ZJ"]).AddSyst(self.cb, *self.tau_es_syst_args)

			# fake-rate
			self.cb.cp().channel(["et"]).process(["ZL", "ZJ"]).AddSyst(self.cb, *self.zllFakeTau_syst_args)
		
			# ======================================================================
			# All channels
			# lumi
			self.cb.cp().process(["ZTT", "ZLL", "ZL", "ZJ", "TT", "W", "VV", "QCD"]).AddSyst(self.cb, *self.lumi_syst_args)
		
			# cross section
			self.cb.cp().process(["TT"]).AddSyst(self.cb, *self.ttj_cross_section_syst_args)
			self.cb.cp().process(["VV"]).AddSyst(self.cb, *self.vv_cross_section_syst_args)
			self.cb.cp().process(["W"]).AddSyst(self.cb, *self.wj_cross_section_syst_args)

			# QCD systematic
			self.cb.cp().process(["QCD"]).AddSyst(self.cb, *self.qcd_syst_args)
		
			if log.isEnabledFor(logging.DEBUG):
				self.cb.PrintAll()


class ZttLepTauFakeRateDatacards(datacards.Datacards):
	def __init__(self, cb=None):
		super(ZttLepTauFakeRateDatacards, self).__init__(cb)
		
		if cb is None:
			# ======================================================================
			# MT channel
			self.add_processes(
					channel="mt",
					categories=["mt_"+category for category in ["antimuloosepass", "antimuloosefail"]],
					bkg_processes=["ZTT", "ZJ", "TT", "VV", "W", "QCD"],
					sig_processes=["ZL"],
					analysis=["ztt"],
					era=["13TeV"],
					mass=["90"]
			)
		
			# efficiencies
			self.cb.cp().channel(["mt"]).process(["ZL", "ZJ", "TT", "VV", "W", "QCD"]).AddSyst(self.cb, *self.muon_efficieny_syst_args)
			self.cb.cp().channel(["mt"]).process(["ZTT", "TT", "VV"]).AddSyst(self.cb, *self.tau_efficieny_syst_args)
			
			# Tau ES
			self.cb.cp().channel(["mt"]).process(["ZTT", "ZL", "ZJ"]).AddSyst(self.cb, *self.tau_es_syst_args)
			
			# ======================================================================
			# ET channel
			self.add_processes(
					channel="et",
					categories=["et_"+category for category in ["antieloosepass", "antieloosefail"]],
					bkg_processes=["ZTT", "ZJ", "TT", "VV", "W", "QCD"],
					sig_processes=["ZL"],
					analysis=["ztt"],
					era=["13TeV"],
					mass=["90"]
			)
		
			# efficiencies
			self.cb.cp().channel(["et"]).process(["ZTT", "ZL", "ZJ", "TT", "VV"]).AddSyst(self.cb, *self.electron_efficieny_syst_args)
			self.cb.cp().channel(["et"]).process(["ZTT", "TT", "VV"]).AddSyst(self.cb, *self.tau_efficieny_syst_args)

			# Tau ES
			self.cb.cp().channel(["et"]).process(["ZTT", "ZL", "ZJ"]).AddSyst(self.cb, *self.tau_es_syst_args)
		
			# ======================================================================
			# All channels
			# lumi
			self.cb.cp().process(["ZTT", "ZLL", "ZL", "ZJ", "TT", "W", "VV", "QCD"]).AddSyst(self.cb, *self.lumi_syst_args)
		
			# cross section
			self.cb.cp().process(["TT"]).AddSyst(self.cb, *self.ttj_cross_section_syst_args)
			self.cb.cp().process(["VV"]).AddSyst(self.cb, *self.vv_cross_section_syst_args)
			self.cb.cp().process(["W"]).AddSyst(self.cb, *self.wj_cross_section_syst_args)

			# QCD systematic
			self.cb.cp().process(["QCD"]).AddSyst(self.cb, *self.qcd_syst_args)
		
			if log.isEnabledFor(logging.DEBUG):
				self.cb.PrintAll()
