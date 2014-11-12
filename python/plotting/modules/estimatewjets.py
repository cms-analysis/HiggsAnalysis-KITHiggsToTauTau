# -*- coding: utf-8 -*-

"""
"""

import logging
import HarryPlotter.Utility.logger as logger
log = logging.getLogger(__name__)

import ROOT

import HiggsAnalysis.KITHiggsToTauTau.plotting.modules.estimatebase as estimatebase


class EstimateWjets(estimatebase.EstimateBase):
	def __init__(self):
		super(EstimateWjets, self).__init__()

	def modify_argument_parser(self, parser, args):
		super(EstimateWjets, self).modify_argument_parser(parser, args)
		
		self.estimate_wjets_options = parser.add_argument_group("WJets estimation options")
		self.estimate_wjets_options.add_argument("--wjets-shape-nicks", nargs="+",
		                                         default=["wjets", "noplot_wjets_ss"],
		                                         help="Nicks for histogram to plot. [Default: %(default)s]")
		self.estimate_wjets_options.add_argument("--wjets-data-control-nicks", nargs="+",
		                                         default=["noplot_wjets_data_control", "noplot_wjets_ss_data_control"],
		                                         help="Nicks for control region data histogram. [Default: %(default)s]")
		self.estimate_wjets_options.add_argument("--wjets-mc-signal-nicks", nargs="+",
		                                         default=["noplot_wjets_mc_signal", "noplot_wjets_ss_mc_signal"],
		                                         help="Nicks for signal region MC histogram. [Default: %(default)s]")
		self.estimate_wjets_options.add_argument("--wjets-mc-control-nicks", nargs="+",
		                                         default=["noplot_wjets_mc_control", "noplot_wjets_ss_mc_control"],
		                                         help="Nicks for control region MC histogram. [Default: %(default)s]")

	def prepare_args(self, parser, plotData):
		super(EstimateWjets, self).prepare_args(parser, plotData)
		
		self._plotdict_keys = ["wjets_shape_nicks", "wjets_data_control_nicks", "wjets_mc_signal_nicks", "wjets_mc_control_nicks"]
		self.prepare_list_args(plotData, self._plotdict_keys)
		
		# make sure that all necessary histograms are available
		for nicks in zip(*[plotData.plotdict[key] for key in self._plotdict_keys]):
			for nick in nicks:
				assert isinstance(plotData.plotdict["root_objects"].get(nick), ROOT.TH1)
	
	def run(self, plotData=None):
		super(EstimateWjets, self).run(plotData)
		
		for wjets_shape_nick, wjets_data_control_nick, wjets_mc_signal_nick, wjets_mc_control_nick in zip(*[plotData.plotdict[key] for key in self._plotdict_keys]):
			self._estimate_wjets(plotData, wjets_shape_nick, wjets_data_control_nick, wjets_mc_signal_nick, wjets_mc_control_nick)
	
	def _estimate_wjets(self, plotData, wjets_shape_nick, wjets_data_control_nick, wjets_mc_signal_nick, wjets_mc_control_nick):
		yield_data_control = plotData.plotdict["root_objects"][wjets_data_control_nick].Integral()
		yield_mc_signal = plotData.plotdict["root_objects"][wjets_mc_signal_nick].Integral()
		yield_mc_control = plotData.plotdict["root_objects"][wjets_mc_control_nick].Integral()
		
		assert yield_mc_control != 0.0
		final_yield = yield_data_control * yield_mc_signal / yield_mc_control
		
		integral_shape = plotData.plotdict["root_objects"][wjets_shape_nick].Integral()
		if integral_shape != 0.0:
			plotData.plotdict["root_objects"][wjets_shape_nick].Scale(final_yield / integral_shape)

