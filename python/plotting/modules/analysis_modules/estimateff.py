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
		self.estimate_ff_options.add_argument("--ff-mc-substract-nicks", nargs="+",
				default=["noplot_dy_ff_control  noplot_tt_ff_control noplot_vv_ff_control"],
				help="Nicks for MC control region histogram(s) to substract from data fake factors (whitespace separated). [Default: %(default)s]")
		#self.estimate_ff_options.add_argument("--ff-subtract-shape", action="store_true", default=True,
		#		help="Subtract the shape of control region histograms from data. [Default: %(default)s]")
		#self.estimate_ff_options.add_argument("--ff-scale-factor", default=1.0, type=float,
		#		help="Scale FF by this factor. [Default: %(default)s]")

	def prepare_args(self, parser, plotData):
		super(EstimateFF, self).prepare_args(parser, plotData)
		
		self._plotdict_keys = ["ff_data_nicks",  "ff_mc_substract_nicks"]#,  "ff_subtract_shape", "ff_scale_factor"]
		self.prepare_list_args(plotData, self._plotdict_keys)
		
		plotData.plotdict["ff_mc_substract_nicks"] = [nicks.split() for nicks in plotData.plotdict["ff_mc_substract_nicks"]]
		
		# make sure that all necessary histograms are available
		for nicks in zip(*[plotData.plotdict[key] for key in self._plotdict_keys]):
			for nick in nicks:
				if isinstance(nick, basestring):
					assert isinstance(plotData.plotdict["root_objects"].get(nick), ROOT.TH1)
				elif (not isinstance(nick, float) and not isinstance(nick, bool)):
					for subnick in nick:
						assert isinstance(plotData.plotdict["root_objects"].get(subnick), ROOT.TH1)
		
	
	def run(self, plotData=None):
		super(EstimateFF, self).run(plotData)
		
		for ff_data_nick, ff_mc_substract_nicks in zip(*[plotData.plotdict[key] for key in self._plotdict_keys]):
			
			for nick in ff_mc_substract_nicks:
				
				plotData.plotdict["root_objects"][ff_data_nick].Add(plotData.plotdict["root_objects"][nick], -1.0)
			
				#plotData.plotdict["root_objects"][ff_data_nick].Scale(plotData.plotdict["ff_scale_factor"])
