# -*- coding: utf-8 -*-

"""
"""

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import ROOT

import HiggsAnalysis.KITHiggsToTauTau.plotting.modules.analysis_modules.estimatebase as estimatebase


class EstimateQcdRun1(estimatebase.EstimateBase):
	def __init__(self):
		super(EstimateQcdRun1, self).__init__()

	def modify_argument_parser(self, parser, args):
		super(EstimateQcdRun1, self).modify_argument_parser(parser, args)
		
		self.estimate_qcd_options = parser.add_argument_group("QCD estimation options")
		self.estimate_qcd_options.add_argument("--qcd-data-control-nicks", nargs="+", default=["qcd"],
				help="Nicks for histogram to plot. [Default: %(default)s]")
		self.estimate_qcd_options.add_argument("--qcd-data-substract-nicks", nargs="+",
				default=["noplot_ztt_mc_qcd_control noplot_zll_qcd_control noplot_ttj_qcd_control noplot_vv_qcd_control noplot_wj_ss"],
				help="Nicks for control region histogram to substract from data (whitespace separated). [Default: %(default)s]")
		self.estimate_qcd_options.add_argument("--qcd-extrapolation-factors-ss-os", nargs="+", type=float, default=[1.06],
				help="Extrapolation factors of OS/SS yields. [Default: %(default)s]")
		self.estimate_qcd_options.add_argument("--qcd-subtract-shape", action="store_true", default=False,
				help="Subtract the shape of control region histograms from data. [Default: %(default)s]")

	def prepare_args(self, parser, plotData):
		super(EstimateQcdRun1, self).prepare_args(parser, plotData)
		
		self._plotdict_keys = ["qcd_data_control_nicks", "qcd_data_substract_nicks", "qcd_extrapolation_factors_ss_os", "qcd_subtract_shape"]
		self.prepare_list_args(plotData, self._plotdict_keys)
		
		plotData.plotdict["qcd_data_substract_nicks"] = [nicks.split() for nicks in plotData.plotdict["qcd_data_substract_nicks"]]
		
		# make sure that all necessary histograms are available
		for nicks in zip(*[plotData.plotdict[key] for key in self._plotdict_keys]):
			for nick in nicks:
				if isinstance(nick, basestring):
					assert isinstance(plotData.plotdict["root_objects"].get(nick), ROOT.TH1)
				elif (not isinstance(nick, float) and not isinstance(nick, bool)):
					for subnick in nick:
						assert isinstance(plotData.plotdict["root_objects"].get(subnick), ROOT.TH1)
		
	
	def run(self, plotData=None):
		super(EstimateQcdRun1, self).run(plotData)
		
		for qcd_data_control_nick, qcd_data_substract_nicks, qcd_extrapolation_factor_ss_os, qcd_subtract_shape in zip(*[plotData.plotdict[key] for key in self._plotdict_keys]):
			yield_data_control = plotData.plotdict["root_objects"][qcd_data_control_nick].Integral()

			for nick in qcd_data_substract_nicks:
				yield_data_control -= plotData.plotdict["root_objects"][nick].Integral()
				if qcd_subtract_shape:
					plotData.plotdict["root_objects"][qcd_data_control_nick].Add(plotData.plotdict["root_objects"][nick], -1.0)

			yield_data_control = max(0.0, yield_data_control)

			integral_shape = plotData.plotdict["root_objects"][qcd_data_control_nick].Integral()
			if integral_shape != 0.0:
				plotData.plotdict["root_objects"][qcd_data_control_nick].Scale(yield_data_control * qcd_extrapolation_factor_ss_os / integral_shape)

