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
		self.estimate_wjets_options.add_argument("--wjets-do-main-bkg", action="store_true", default=True,
		                                         help="Estimate main WJets background")
		self.estimate_wjets_options.add_argument("--wjets-do-bkg-for-qcd", action="store_true", default=True,
		                                         help="Estimate WJets contribution for QCD estimation")

	def prepare_args(self, parser, plotData):
		super(EstimateWjets, self).prepare_args(parser, plotData)
		
		# make sure that all necessary histograms are available
		necessary_histograms = []
		if plotData.plotdict["wjets_do_main_bkg"]:
			necessary_histograms.extend(["wjets", "noplot_wjets_data_control",
			                             "noplot_wjets_mc_signal", "noplot_wjets_mc_control"])
		if plotData.plotdict["wjets_do_bkg_for_qcd"]:
			necessary_histograms.extend(["noplot_wjets_ss", "noplot_wjets_ss_data_control",
			                             "noplot_wjets_ss_mc_signal", "noplot_wjets_ss_mc_control"])
		
		for histogram in necessary_histograms:
			assert isinstance(plotData.plotdict["root_objects"].get(histogram), ROOT.TH1)
	
	def run(self, plotData=None):
		super(EstimateWjets, self).run(plotData)
		
		if plotData.plotdict["wjets_do_main_bkg"]:
			self._estimate_wjets(plotData, "wjets", "noplot_wjets_data_control",
			                     "noplot_wjets_mc_signal", "noplot_wjets_mc_control")
		
		if plotData.plotdict["wjets_do_bkg_for_qcd"]:
			self._estimate_wjets(plotData, "noplot_wjets_ss", "noplot_wjets_ss_data_control",
			                     "noplot_wjets_ss_mc_signal", "noplot_wjets_ss_mc_control")
	
	def _estimate_wjets(self, plotData, nick_shape, nick_data_control, nick_mc_signal, nick_mc_control):
		yield_data_control = plotData.plotdict["root_objects"][nick_data_control].Integral()
		yield_mc_signal = plotData.plotdict["root_objects"][nick_mc_signal].Integral()
		yield_mc_control = plotData.plotdict["root_objects"][nick_mc_control].Integral()
		
		assert yield_mc_control != 0.0
		final_yield = yield_data_control * yield_mc_signal / yield_mc_control
		
		integral_shape = plotData.plotdict["root_objects"][nick_shape].Integral()
		if integral_shape != 0.0:
			plotData.plotdict["root_objects"][nick_shape].Scale(final_yield / integral_shape)

