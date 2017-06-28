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


class EstimateQcdTauHadTauHad(estimatebase.EstimateBase):
	def __init__(self):
		super(EstimateQcdTauHadTauHad, self).__init__()

	def modify_argument_parser(self, parser, args):
		super(EstimateQcdTauHadTauHad, self).modify_argument_parser(parser, args)
		
		self.estimate_qcd_options = parser.add_argument_group("QCD estimation options")
		self.estimate_qcd_options.add_argument("--qcd-data-shape-nicks", nargs="+", default=["qcd"],
				help="Nicks for histogram to plot. [Default: %(default)s]")
		self.estimate_qcd_options.add_argument("--qcd-data-signal-control-nicks", nargs="+", default=["noplot_data_qcd_signal_control"],
				help="Nicks for histogram to plot. [Default: %(default)s]")
		self.estimate_qcd_options.add_argument("--qcd-data-relaxed-control-nicks", nargs="+", default=["noplot_data_qcd_relaxed_control"],
				help="Nicks for histogram to plot. [Default: %(default)s]")
		self.estimate_qcd_options.add_argument("--qcd-data-subtract-nicks", nargs="+",
				default=["noplot_ztt_mc_qcd_control noplot_zll_qcd_control noplot_ttj_qcd_control noplot_vv_qcd_control noplot_wj_ss"],
				help="Nicks for control region histogram to subtract from data (whitespace separated). [Default: %(default)s]")
		self.estimate_qcd_options.add_argument("--qcd-control-signal-subtract-nicks", nargs="+", default=[""],
				help="Nicks for control region histogram to subtract from data (whitespace separated). [Default: %(default)s]")
		self.estimate_qcd_options.add_argument("--qcd-control-relaxed-subtract-nicks", nargs="+", default=[""],
				help="Nicks for control region histogram to subtract from data (whitespace separated). [Default: %(default)s]")

	def prepare_args(self, parser, plotData):
		super(EstimateQcdTauHadTauHad, self).prepare_args(parser, plotData)
		
                self._plotdict_keys = ["qcd_data_shape_nicks", "qcd_data_signal_control_nicks", "qcd_data_relaxed_control_nicks", "qcd_data_subtract_nicks", "qcd_control_signal_subtract_nicks", "qcd_control_relaxed_subtract_nicks"]
		self.prepare_list_args(plotData, self._plotdict_keys)
		
                plotData.plotdict["qcd_data_subtract_nicks"] = [nicks.split() for nicks in plotData.plotdict["qcd_data_subtract_nicks"]]
                plotData.plotdict["qcd_control_signal_subtract_nicks"] = [nicks.split() for nicks in plotData.plotdict["qcd_control_signal_subtract_nicks"]]
                plotData.plotdict["qcd_control_relaxed_subtract_nicks"] = [nicks.split() for nicks in plotData.plotdict["qcd_control_relaxed_subtract_nicks"]]
		
		# make sure that all necessary histograms are available
		# for nicks in zip(*[plotData.plotdict[key] for key in self._plotdict_keys]):
			# for nick in nicks:
				# if isinstance(nick, basestring):
					# assert isinstance(plotData.plotdict["root_objects"].get(nick), ROOT.TH1)
				# elif (not isinstance(nick, float) and not isinstance(nick, bool)):
					# for subnick in nick:
						# assert isinstance(plotData.plotdict["root_objects"].get(subnick), ROOT.TH1)
	
	def run(self, plotData=None):
		super(EstimateQcdTauHadTauHad, self).run(plotData)
		
		for qcd_data_shape_nick, qcd_data_signal_control_nick, qcd_data_relaxed_control_nick, qcd_data_subtract_nicks, qcd_control_signal_subtract_nicks, qcd_control_relaxed_subtract_nicks in zip(*[plotData.plotdict[key] for key in self._plotdict_keys]):
			
			print "qcd ", tools.PoissonYield(plotData.plotdict["root_objects"][qcd_data_shape_nick])()
			for nick in qcd_data_subtract_nicks:
				plotData.plotdict["root_objects"][qcd_data_shape_nick].Add(plotData.plotdict["root_objects"][nick], -1.0)
				print nick, tools.PoissonYield(plotData.plotdict["root_objects"][nick])()
			
			# log.debug("Relative statistical uncertainty of the yield for process QCD (nick \"{nick}\") is {unc}.".format(nick=qcd_data_shape_nick, unc=final_yield.std_dev/final_yield.nominal_value if final_yield.nominal_value != 0.0 else 0.0))
			
			# plotData.metadata[qcd_data_shape_nick] = {
				# "yield" : final_yield.nominal_value,
				# "yield_unc" : final_yield.std_dev,
				# "yield_unc_rel" : abs(final_yield.std_dev/final_yield.nominal_value if final_yield.nominal_value != 0.0 else 0.0),
			# }
