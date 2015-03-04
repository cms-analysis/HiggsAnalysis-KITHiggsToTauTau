# -*- coding: utf-8 -*-

"""
"""

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import os
import ROOT

import Artus.HarryPlotter.plot_modules.plotroot as plotroot


class PlotRootHtt(plotroot.PlotRoot):
	def __init__(self):
		super(PlotRootHtt, self).__init__()
	
	def modify_argument_parser(self, parser, args):
		super(PlotRootHtt, self).modify_argument_parser(parser, args)
		
		parser.set_defaults(y_label="Number of Entries")
	
	def run(self, plotData):
		super(PlotRootHtt, self).run(plotData)

	def set_style(self, plotData):
		super(PlotRootHtt, self).set_style(plotData)
		
		# load HttStyles
		cwd = os.getcwd()
		os.chdir(os.path.expandvars("$CMSSW_BASE/src"))
		ROOT.gROOT.LoadMacro(os.path.expandvars("$CMSSW_BASE/src/HiggsAnalysis/HiggsToTauTau/src/HttStyles.cc")+"+")
		ROOT.SetStyle()
		os.chdir(cwd)
	
	def create_canvas(self, plotData):
		self.canvas = ROOT.MakeCanvas("canvas", "")

		#Modify right side margin for 2d-plots
		if not isinstance(plotData.plotdict["root_objects"][plotData.plotdict["nicks"][0]], ROOT.TGraph):
			if plotData.plotdict["root_objects"][plotData.plotdict["nicks"][0]].GetDimension() == 2:
				self.canvas.SetRightMargin(0.15)

		if len(plotData.plotdict["subplot_nicks"]) > 0:
			self.plot_subplot_slider_y = 0.35
			self.canvas.cd()
			self.plot_pad = ROOT.TPad("plot_pad", "", 0.0, self.plot_subplot_slider_y, 1.0, 1.0)
			self.subplot_pad = ROOT.TPad("subplot_pad", "", 0.0, 0.0, 1.0, self.plot_subplot_slider_y)
			self.plot_pad.SetNumber(1)
			self.subplot_pad.SetNumber(2)
			self.plot_pad.Draw()
			self.subplot_pad.Draw()
			ROOT.InitSubPad(self.canvas, 1)
			ROOT.InitSubPad(self.canvas, 2)
   		
		super(PlotRootHtt, self).create_canvas(plotData)

	def prepare_histograms(self, plotData):
		for nick, color, fill_style in zip(plotData.plotdict["nicks"], plotData.plotdict["colors"], plotData.plotdict["fill_styles"]):
			root_object = plotData.plotdict["root_objects"][nick]
			if isinstance(root_object, ROOT.TH1):
				ROOT.InitHist(root_object, "", "", color, fill_style)
		
		super(PlotRootHtt, self).prepare_histograms(plotData)
	
	def add_labels(self, plotData):
		super(PlotRootHtt, self).add_labels(plotData)
		
		if self.legend != None:
			ROOT.SetLegendStyle(self.legend)

