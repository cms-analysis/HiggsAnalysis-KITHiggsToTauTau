# -*- coding: utf-8 -*-

"""
"""

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import ROOT

import HiggsAnalysis.KITHiggsToTauTau.plotting.modules.analysis_modules.estimatebase as estimatebase


class EstimateTtbar(estimatebase.EstimateBase):
	def __init__(self):
		super(EstimateTtbar, self).__init__()

	def modify_argument_parser(self, parser, args):
		super(EstimateTtbar, self).modify_argument_parser(parser, args)
		
		self.estimate_ttbar_options = parser.add_argument_group("TTbar estimation options")
		self.estimate_ttbar_options.add_argument("--ttbar-from-mc", nargs="+", type="bool", default=[False],
				help="Estimate TTJ from MC samples. [Default: %(default)s]")
		self.estimate_ttbar_options.add_argument("--ttbar-shape-nicks", nargs="+",
				default=["ttj"],
				help="Nicks for histogram to plot. [Default: %(default)s]")
		self.estimate_ttbar_options.add_argument("--ttbar-data-control-nicks", nargs="+",
				default=["noplot_ttj_data_control"],
				help="Nicks for control region data histogram. [Default: %(default)s]")
		self.estimate_ttbar_options.add_argument("--ttbar-data-substract-nicks", nargs="+",
				default=["noplot_ztt_mc_ttj_control noplot_zll_ttj_control noplot_wj_ttj_control noplot_vv_ttj_control"],
				help="Nicks for control region histogram to substract from data (whitespace separated). [Default: %(default)s]")
		self.estimate_ttbar_options.add_argument("--ttbar-mc-signal-nicks", nargs="+",
				default=["noplot_ttj_mc_signal"],
				help="Nicks for signal region MC histogram. [Default: %(default)s]")
		self.estimate_ttbar_options.add_argument("--ttbar-mc-control-nicks", nargs="+",
				default=["noplot_ttj_mc_control"],
				help="Nicks for control region MC histogram. [Default: %(default)s]")

	def prepare_args(self, parser, plotData):
		super(EstimateTtbar, self).prepare_args(parser, plotData)
		
		self._plotdict_keys = ["ttbar_from_mc", "ttbar_shape_nicks", "ttbar_data_control_nicks",
		                       "ttbar_data_substract_nicks", "ttbar_mc_signal_nicks", "ttbar_mc_control_nicks"]
		self.prepare_list_args(plotData, self._plotdict_keys)
		
		plotData.plotdict["ttbar_data_substract_nicks"] = [nicks.split() for nicks in plotData.plotdict["ttbar_data_substract_nicks"]]
		
		# make sure that all necessary histograms are available
		for nicks in zip(*[plotData.plotdict[key] for key in self._plotdict_keys]):
			for nick in nicks:
				if isinstance(nick, basestring):
					assert isinstance(plotData.plotdict["root_objects"].get(nick), ROOT.TH1)
				elif not isinstance(nick, bool):
					for subnick in nick:
						assert isinstance(plotData.plotdict["root_objects"].get(subnick), ROOT.TH1)
	
	def run(self, plotData=None):
		super(EstimateTtbar, self).run(plotData)
		
		for ttbar_from_mc, ttbar_shape_nick, ttbar_data_control_nick, ttbar_data_substract_nicks, ttbar_mc_signal_nick, ttbar_mc_control_nick in zip(*[plotData.plotdict[key] for key in self._plotdict_keys]):
			if not ttbar_from_mc:
				yield_data_control = plotData.plotdict["root_objects"][ttbar_data_control_nick].Integral()
				for nick in ttbar_data_substract_nicks:
					yield_data_control -= plotData.plotdict["root_objects"][nick].Integral()
				yield_data_control = max(0.0, yield_data_control)
		
				yield_mc_signal = plotData.plotdict["root_objects"][ttbar_mc_signal_nick].Integral()
				yield_mc_control = plotData.plotdict["root_objects"][ttbar_mc_control_nick].Integral()
			
				assert (yield_data_control*yield_mc_signal == 0.0) or (yield_mc_control != 0.0)
				final_yield = yield_data_control * yield_mc_signal
				if final_yield != 0.0:
					final_yield /= yield_mc_control
		
				integral_shape = plotData.plotdict["root_objects"][ttbar_shape_nick].Integral()
				if integral_shape != 0.0:
					log.debug("Scale factor for process ttbar+jets (nick \"{nick}\") is {scale_factor}.".format(nick=ttbar_shape_nick, scale_factor=final_yield/integral_shape))
					plotData.plotdict["root_objects"][ttbar_shape_nick].Scale(final_yield / integral_shape)

