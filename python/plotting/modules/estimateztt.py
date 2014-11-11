# -*- coding: utf-8 -*-

"""
"""

import logging
import HarryPlotter.Utility.logger as logger
log = logging.getLogger(__name__)

import ROOT

import HiggsAnalysis.KITHiggsToTauTau.plotting.modules.estimatebase as estimatebase


class EstimateZtt(estimatebase.EstimateBase):
	def __init__(self):
		super(EstimateZtt, self).__init__()

	def modify_argument_parser(self, parser, args):
		super(EstimateZtt, self).modify_argument_parser(parser, args)
		
		self.estimate_ztt_options = parser.add_argument_group("ZTT estimation options")
		self.estimate_ztt_options.add_argument("--ztt-from-mc", action="store_true", default=False,
		                                       help="Estimate ZTT from MC samples.")

	def prepare_args(self, parser, plotData):
		super(EstimateZtt, self).prepare_args(parser, plotData)
		
		# make sure that all necessary histograms are available
		assert isinstance(plotData.plotdict["root_objects"].get("ztt"), ROOT.TH1)
		if not plotData.plotdict["ztt_from_mc"]:
			assert isinstance(plotData.plotdict["root_objects"].get("noplot_ztt_mc_inc"), ROOT.TH1)
			assert isinstance(plotData.plotdict["root_objects"].get("noplot_ztt_emb_inc"), ROOT.TH1)
	
	def run(self, plotData=None):
		super(EstimateZtt, self).run(plotData)
		
		if not plotData.plotdict["ztt_from_mc"]:
			yield_inclusive_mc = plotData.plotdict["root_objects"]["noplot_ztt_mc_inc"].Integral()
			yield_inclusive_emb = plotData.plotdict["root_objects"]["noplot_ztt_emb_inc"].Integral()
			
			assert yield_inclusive_emb != 0.0
			plotData.plotdict["root_objects"]["ztt"].Scale(yield_inclusive_mc / yield_inclusive_emb)
		
		else:
			pass # TODO

