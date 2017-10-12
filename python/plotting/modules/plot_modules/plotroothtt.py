# -*- coding: utf-8 -*-

"""
"""

import logging
import math
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import Artus.HarryPlotter.plot_modules.plotroot as plotroot
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.colors as colors
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.labels as labels


class PlotRootHtt(plotroot.PlotRoot):
	def __init__(self):
		super(PlotRootHtt, self).__init__()
		
		self.nice_labels = labels.LabelsDict(latex_version="root")
	
	def modify_argument_parser(self, parser, args):
		super(PlotRootHtt, self).modify_argument_parser(parser, args)
		
		self.axis_options.add_argument("--angular-plot", action="store_true", default=False,
									   help="Use proper x tick labels for angular plots. [Default: %(default)s]")	
		self.axis_options.add_argument("--absjdphi-plot", action="store_true", default=False,
									   help="Use proper x tick labels for abs(jdphi) plots. [Default: %(default)s]")
									
									   
	
	def prepare_args(self, parser, plotData):
		if self.predefined_colors is None:
			self.predefined_colors = colors.ColorsDict(color_scheme=plotData.plotdict["color_scheme"])
		
		super(PlotRootHtt, self).prepare_args(parser, plotData)
		
	def make_plots(self, plotData):
		super(PlotRootHtt, self).make_plots(plotData)
	
		if plotData.plotdict["angular_plot"]:		
			self.axes_histogram.GetXaxis().Set(1000,0,2*math.pi)
			self.axes_histogram.GetXaxis().SetBinLabel(1, "0")
			self.axes_histogram.GetXaxis().SetBinLabel(250, "#pi/2")
			self.axes_histogram.GetXaxis().SetBinLabel(500, "#pi")
			self.axes_histogram.GetXaxis().SetBinLabel(750, "3#pi/2")		
			self.axes_histogram.GetXaxis().SetBinLabel(1000, "2#pi")
			#TODO: Figure out why this adjustment is necessary to obtain equally sized labels on both axes.
		
			self.axes_histogram.GetXaxis().SetLabelSize(1.35*self.axes_histogram.GetYaxis().GetLabelSize())
			self.axes_histogram.LabelsOption("h", "X")
			#TODO: Set Number of divisions such that the tick marks are aligned with the custom tick labels.
		
		if plotData.plotdict["absjdphi_plot"]:		
			self.axes_histogram.GetXaxis().Set(1000,0,math.pi)
			self.axes_histogram.GetXaxis().SetBinLabel(1, "0")
			self.axes_histogram.GetXaxis().SetBinLabel(250, "#pi/4")
			self.axes_histogram.GetXaxis().SetBinLabel(500, "#pi/2")
			self.axes_histogram.GetXaxis().SetBinLabel(750, "3#pi/4")		
			self.axes_histogram.GetXaxis().SetBinLabel(1000, "#pi")
			#TODO: Figure out why this adjustment is necessary to obtain equally sized labels on both axes.
			self.axes_histogram.GetXaxis().SetLabelSize(1.35*self.axes_histogram.GetYaxis().GetLabelSize())
			self.axes_histogram.GetXaxis().SetNdivisions(4, 1, 0, True)
			self.axes_histogram.LabelsOption("h", "X")
	
	
