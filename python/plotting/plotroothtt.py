# -*- coding: utf-8 -*-

"""
"""

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import os
import ROOT

import Artus.HarryPlotter.plotroot as plotroot


class PlotRootHtt(plotroot.PlotRoot):
	def __init__(self):
		plotroot.PlotRoot.__init__(self)
		
		# load HttStyles
		ROOT.gROOT.LoadMacro(os.path.expandvars("$CMSSW_BASE/src/HiggsAnalysis/HiggsToTauTau/src/HttStyles.cc")+"+")
	
	def run(self, plotData):
		# apply HttStyles
		ROOT.SetStyle()
		
		plotroot.PlotRoot.run(self, plotData)

	def create_canvas(self, plotData):
		self.canvas = ROOT.MakeCanvas("canvas", "")

