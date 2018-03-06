# -*- coding: utf-8 -*-

"""
"""

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import ROOT

import HiggsAnalysis.KITHiggsToTauTau.plotting.modules.analysis_modules.estimatebase as estimatebase
import HiggsAnalysis.KITHiggsToTauTau.tools as tools
import HiggsAnalysis.KITHiggsToTauTau.uncertainties.uncertainties as uncertainties


class EstimateFF(estimatebase.EstimateBase):
	def __init__(self):
		super(EstimateFF, self).__init__()

	def modify_argument_parser(self, parser, args):
		super(EstimateFF, self).modify_argument_parser(parser, args)
		
		self.estimate_ff_options = parser.add_argument_group("FF estimation options")
		self.estimate_ff_options.add_argument("--ff-data-nicks", nargs="+", default=["ff"],
				help="Nicks for histogram to plot. [Default: %(default)s]")
		self.estimate_ff_options.add_argument("--ff-mc-subtract-nicks", nargs="+",
				default=["noplot_dy_ff_control  noplot_tt_ff_control noplot_vv_ff_control"],
				help="Nicks for MC control region histogram(s) to substract from data fake factors (whitespace separated). [Default: %(default)s]")
		self.estimate_ff_options.add_argument("--ff-norm-data-nicks", nargs="+", default=["noplot_ff_norm"],
				help="Nicks for histogram to plot. [Default: %(default)s]")
		self.estimate_ff_options.add_argument("--ff-norm-mc-subtract-nicks", nargs="+",
				default=["noplot_dy_ff_norm  noplot_tt_ff_norm noplot_vv_ff_norm"],
				help="Nicks for MC control region histogram(s) to substract from data fake factors (whitespace separated). [Default: %(default)s]")

	def prepare_args(self, parser, plotData):
		super(EstimateFF, self).prepare_args(parser, plotData)
		
		self._plotdict_keys = ["ff_data_nicks",  "ff_mc_subtract_nicks", "ff_norm_data_nicks", "ff_norm_mc_subtract_nicks"]
		self.prepare_list_args(plotData, self._plotdict_keys)
		
		plotData.plotdict["ff_mc_subtract_nicks"] = [nicks.split() for nicks in plotData.plotdict["ff_mc_subtract_nicks"]]
		plotData.plotdict["ff_norm_mc_subtract_nicks"] = [nicks.split() for nicks in plotData.plotdict["ff_norm_mc_subtract_nicks"]]
		
	
	def run(self, plotData=None):
		super(EstimateFF, self).run(plotData)
		
		# make sure that all necessary histograms are available
		for nicks in zip(*[plotData.plotdict[key] for key in self._plotdict_keys]):
			for nick in nicks:
				if isinstance(nick, basestring):
					assert isinstance(plotData.plotdict["root_objects"].get(nick), ROOT.TH1)
				elif (not isinstance(nick, float) and not isinstance(nick, bool)):
					for subnick in nick:
						assert isinstance(plotData.plotdict["root_objects"].get(subnick), ROOT.TH1)
		
		for (ff_data_nick, ff_mc_subtract_nicks, ff_norm_data_nick, ff_norm_mc_subtract_nicks) in zip(*[plotData.plotdict[key] for key in self._plotdict_keys]):
			for nick in ff_mc_subtract_nicks:
				plotData.plotdict["root_objects"][ff_data_nick].Add(plotData.plotdict["root_objects"][nick], -1.0)
			for nick in ff_norm_mc_subtract_nicks:
				plotData.plotdict["root_objects"][ff_norm_data_nick].Add(plotData.plotdict["root_objects"][nick], -1.0)
			ff_yield = tools.PoissonYield(plotData.plotdict["root_objects"][ff_data_nick])()
			ff_norm_yield = tools.PoissonYield(plotData.plotdict["root_objects"][ff_norm_data_nick])()
			if ff_yield != 0.0:
				scale_factor = ff_norm_yield/ff_yield
				plotData.plotdict["root_objects"][ff_data_nick].Scale(scale_factor.nominal_value)



