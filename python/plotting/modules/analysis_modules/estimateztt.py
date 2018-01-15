# -*- coding: utf-8 -*-

"""
"""

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import ROOT

import HiggsAnalysis.KITHiggsToTauTau.plotting.modules.analysis_modules.estimatebase as estimatebase


class EstimateZtt(estimatebase.EstimateBase):
	def __init__(self):
		super(EstimateZtt, self).__init__()

	def modify_argument_parser(self, parser, args):
		super(EstimateZtt, self).modify_argument_parser(parser, args)
		
		self.estimate_ztt_options = parser.add_argument_group("ZTT estimation options")
		self.estimate_ztt_options.add_argument("--ztt-from-mc", nargs="+", type="bool", default=[False],
		                                       help="Estimate ZTT from MC samples. [Default: %(default)s]")
		self.estimate_ztt_options.add_argument("--ztt-plot-nicks", nargs="+", default=["ztt"],
		                                       help="Nicks for histogram to plot. [Default: %(default)s]")
		self.estimate_ztt_options.add_argument("--ztt-mc-inc-nicks", nargs="+", default=["noplot_ztt_mc_inc"],
		                                       help="Nicks for inclusive MC histogram. [Default: %(default)s]")
		self.estimate_ztt_options.add_argument("--ztt-emb-inc-nicks", nargs="+", default=["noplot_ztt_emb_inc"],
		                                       help="Nicks for inclusive embedding histogram. [Default: %(default)s]")

	def prepare_args(self, parser, plotData):
		super(EstimateZtt, self).prepare_args(parser, plotData)
		
		self._plotdict_keys = ["ztt_from_mc", "ztt_plot_nicks", "ztt_mc_inc_nicks", "ztt_emb_inc_nicks"]
		self.prepare_list_args(plotData, self._plotdict_keys)
	
	def run(self, plotData=None):
		super(EstimateZtt, self).run(plotData)
		
		# make sure that all necessary histograms are available
		for ztt_from_mc, ztt_plot_nick, ztt_mc_inc_nick, ztt_emb_inc_nick in zip(*[plotData.plotdict[key] for key in self._plotdict_keys]):
			assert isinstance(plotData.plotdict["root_objects"].get(ztt_plot_nick), ROOT.TH1)
			if not ztt_from_mc:
				assert isinstance(plotData.plotdict["root_objects"].get(ztt_mc_inc_nick), ROOT.TH1)
				assert isinstance(plotData.plotdict["root_objects"].get(ztt_emb_inc_nick), ROOT.TH1)
		
		for ztt_from_mc, ztt_plot_nick, ztt_mc_inc_nick, ztt_emb_inc_nick in zip(*[plotData.plotdict[key] for key in self._plotdict_keys]):
			if not ztt_from_mc:
				yield_inclusive_mc = plotData.plotdict["root_objects"][ztt_mc_inc_nick].Integral()
				yield_inclusive_emb = plotData.plotdict["root_objects"][ztt_emb_inc_nick].Integral()
				
				if yield_inclusive_mc == 0.0:
					plotData.plotdict["root_objects"][ztt_plot_nick].Scale(0.0)
				else:
					assert yield_inclusive_emb != 0.0
					plotData.plotdict["root_objects"][ztt_plot_nick].Scale(yield_inclusive_mc / yield_inclusive_emb)

