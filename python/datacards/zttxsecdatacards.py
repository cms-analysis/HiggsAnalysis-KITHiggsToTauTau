# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import HiggsAnalysis.KITHiggsToTauTau.datacards.datacards as datacards


class ZttXsecDatacards(datacards.Datacards):
	def __init__(self, cb=None):
		super(ZttXsecDatacards, self).__init__(cb)
		
		# ======================================================================
		# MT channel
		self.add_processes(channel="mt", categories=["inclusive"], bkg_processes=["TTJ", "VV", "WJ", "QCD"], sig_processes=["ZTT"], analysis=["ztt"], era=["13TeV"])
		
		# lumi
		self.cb.cp().process(["ztt", "TTJ", "VV", "WJ", "QCD"]).AddSyst(self.cb, *self.lumi_syst_args)
		
		
		# ======================================================================
		# ET channel
		self.add_processes(channel="et", categories=["inclusive"], bkg_processes=["TTJ", "VV", "WJ", "QCD"], sig_processes=["ZTT"], analysis=["ztt"], era=["13TeV"])
		
		# lumi
		self.cb.cp().process(["ZTT", "TTJ", "VV", "WJ", "QCD"]).AddSyst(self.cb, *self.lumi_syst_args)
		
		
		# ======================================================================
		# EM channel
		# TODO
		
		
		# ======================================================================
		# TT channel
		# TODO
		
		
		if log.isEnabledFor(logging.DEBUG):
			self.cb.PrintAll()
