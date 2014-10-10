# -*- coding: utf-8 -*-

"""
"""

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import os
import ROOT

import HarryPlotter.Plotting.plotroot as plotroot


class PlotRootHtt(plotroot.PlotRoot):
	def __init__(self):
		super(PlotRootHtt, self).__init__()
		
		# load HttStyles
		cwd = os.getcwd()
		os.chdir(os.path.expandvars("$CMSSW_BASE/src"))
		ROOT.gROOT.LoadMacro(os.path.expandvars("$CMSSW_BASE/src/HiggsAnalysis/HiggsToTauTau/src/HttStyles.cc")+"+")
		os.chdir(cwd)
	
	def modify_argument_parser(self, parser, args):
		super(PlotRootHtt, self).modify_argument_parser(parser, args)
		
		parser.set_defaults(y_label="Number of Entries")
	
	def run(self, plotData):
		# apply HttStyles
		ROOT.SetStyle()
		
		super(PlotRootHtt, self).run(plotData)

	def create_canvas(self, plotData):
		self.canvas = ROOT.MakeCanvas("canvas", "")
		
		if plotData.plotdict["ratio"]:
			plot_ratio_slider_y = 0.35
			self.canvas.cd()
			self.plot_pad = ROOT.TPad("plot_pad", "", 0.0, plot_ratio_slider_y, 1.0, 1.0)
			self.ratio_pad = ROOT.TPad("ratio_pad", "", 0.0, 0.0, 1.0, plot_ratio_slider_y)
			self.plot_pad.SetNumber(1)
			self.ratio_pad.SetNumber(2)
			self.plot_pad.Draw()
			self.ratio_pad.Draw()
			ROOT.InitSubPad(self.canvas, 1)
			ROOT.InitSubPad(self.canvas, 2)
   		
		super(PlotRootHtt, self).create_canvas(plotData)

	def prepare_histograms(self, plotData):
		for root_histogram in plotData.plotdict["root_objects"].values() + plotData.plotdict.get("root_ratio_histos", []):
			ROOT.InitHist(root_histogram, root_histogram.GetTitle())
		
		super(PlotRootHtt, self).prepare_histograms(plotData)
	
	def add_labels(self, plotData):
		super(PlotRootHtt, self).add_labels(plotData)
		
		if self.legend != None:
			ROOT.SetLegendStyle(self.legend)

