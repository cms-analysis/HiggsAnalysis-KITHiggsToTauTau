# -*- coding: utf-8 -*-

"""
"""

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import os
import ROOT

import Artus.HarryPlotter.plot_modules.plotroot as plotroot
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.colors as colors
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.labels as labels


class PlotRootHtt(plotroot.PlotRoot):
	def __init__(self):
		super(PlotRootHtt, self).__init__()
		
		self.nice_labels = labels.LabelsDict(latex_version="root")
	
	def modify_argument_parser(self, parser, args):
		super(PlotRootHtt, self).modify_argument_parser(parser, args)
	
	def prepare_args(self, parser, plotData):
		if self.predefined_colors is None:
			self.predefined_colors = colors.ColorsDict(color_scheme=plotData.plotdict["color_scheme"])
		
		super(PlotRootHtt, self).prepare_args(parser, plotData)
	
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
		canvas = ROOT.MakeCanvas("canvas", "")
		plot_pad = None
		subplot_pad = None
		
		if len(plotData.plotdict["subplot_nicks"]) > 0:
			canvas.cd()
			plot_pad = ROOT.TPad("plot_pad", "", 0.0, self.plot_subplot_slider_y, 1.0, 0.95)
			subplot_pad = ROOT.TPad("subplot_pad", "", 0.0, 0.0, 1.0, self.plot_subplot_slider_y)
			plot_pad.SetNumber(1)
			subplot_pad.SetNumber(2)
			plot_pad.Draw()
			subplot_pad.Draw()
			ROOT.InitSubPad(canvas, 1)
			ROOT.InitSubPad(canvas, 2)
   		
		plotData.plot = plotroot.RootPlotContainer(canvas, plot_pad, subplot_pad)
		super(PlotRootHtt, self).create_canvas(plotData)

	def prepare_histograms(self, plotData):
		for nick, colors, fill_style in zip(plotData.plotdict["nicks"], plotData.plotdict["colors"], plotData.plotdict["fill_styles"]):
			root_object = plotData.plotdict["root_objects"][nick]
			if isinstance(root_object, ROOT.TH1):
				ROOT.InitHist(root_object, "", "", colors[0], fill_style)
		
		super(PlotRootHtt, self).prepare_histograms(plotData)
	
	def add_labels(self, plotData):
		super(PlotRootHtt, self).add_labels(plotData)
		
		if self.legend != None:
			ROOT.SetLegendStyle(self.legend)

