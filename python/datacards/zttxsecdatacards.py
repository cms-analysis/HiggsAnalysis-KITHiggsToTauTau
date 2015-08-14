# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import HiggsAnalysis.KITHiggsToTauTau.datacards.datacards as datacards


class ZttXsecDatacards(datacards.Datacards):
	def __init__(self, cb=None):
		super(ZttXsecDatacards, self).__init__(cb)
		
		self.add_processes(channel="mt", categories=["inclusive"], bkg_processes=["ttj", "vv", "wj", "qcd"], sig_processes=["ztt"], analysis=["ztt"], era=["13TeV"])
		self.add_processes(channel="et", categories=["inclusive"], bkg_processes=["ttj", "vv", "wj", "qcd"], sig_processes=["ztt"], analysis=["ztt"], era=["13TeV"])
