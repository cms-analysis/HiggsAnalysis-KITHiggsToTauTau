# -*- coding: utf-8 -*-

"""
"""

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import Artus.HarryPlotter.plot_modules.plotroot as plotroot
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.colors as colors
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.labels as labels


class PlotRootHtt(plotroot.PlotRoot):
	def __init__(self):
		super(PlotRootHtt, self).__init__()
		
		self.nice_labels = labels.LabelsDict(latex_version="root")
	
	def prepare_args(self, parser, plotData):
		if self.predefined_colors is None:
			self.predefined_colors = colors.ColorsDict(color_scheme=plotData.plotdict["color_scheme"])
		
		super(PlotRootHtt, self).prepare_args(parser, plotData)
