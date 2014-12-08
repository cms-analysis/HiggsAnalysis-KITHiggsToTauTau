# -*- coding: utf-8 -*-

"""
"""

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import Artus.HarryPlotter.analysisbase as analysisbase


class EstimateBase(analysisbase.AnalysisBase):
	def __init__(self):
		super(EstimateBase, self).__init__()

	def modify_argument_parser(self, parser, args):
		super(EstimateBase, self).modify_argument_parser(parser, args)
		
		self.estimate_base_options = parser.add_argument_group("General estimation options")
		self.estimate_base_options.add_argument("-c", "--channel", choices=["tt", "mt", "et", "em", "mm", "ee"],
		                                        help="Channel.")
		self.estimate_base_options.add_argument("--category", help="Category.")

	def prepare_args(self, parser, plotData):
		super(EstimateBase, self).prepare_args(parser, plotData)
	
	def run(self, plotData=None):
		super(EstimateBase, self).run(plotData)

