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


class EstimateWjets(estimatebase.EstimateBase):
	def __init__(self):
		super(EstimateWjets, self).__init__()

	def modify_argument_parser(self, parser, args):
		super(EstimateWjets, self).modify_argument_parser(parser, args)
		
		self.estimate_wjets_options = parser.add_argument_group("WJets estimation options")
		self.estimate_wjets_options.add_argument("--wjets-from-mc", nargs="+", type="bool", default=[False],
				help="Estimate WJets from MC samples. [Default: %(default)s]")
		self.estimate_wjets_options.add_argument("--wjets-shape-nicks", nargs="+",
				default=["wj", "noplot_wj_ss"],
				help="Nicks for histogram to plot. [Default: %(default)s]")
		self.estimate_wjets_options.add_argument("--wjets-data-control-nicks", nargs="+",
				default=["noplot_wj_data_control", "noplot_wj_ss_data_control"],
				help="Nicks for control region data histogram. [Default: %(default)s]")
		self.estimate_wjets_options.add_argument("--wjets-data-substract-nicks", nargs="+",
				default=["noplot_ztt_mc_wj_control noplot_zll_wj_control noplot_ttj_wj_control noplot_vv_wj_control",
		                 "noplot_ztt_ss_mc_wj_control noplot_zll_ss_wj_control noplot_ttj_ss_wj_control noplot_vv_ss_wj_control"],
				help="Nicks for control region histogram to substract from data (whitespace separated). [Default: %(default)s]")
		self.estimate_wjets_options.add_argument("--wjets-mc-signal-nicks", nargs="+",
				default=["noplot_wj_mc_signal", "noplot_wj_ss_mc_signal"],
				help="Nicks for signal region MC histogram. [Default: %(default)s]")
		self.estimate_wjets_options.add_argument("--wjets-mc-control-nicks", nargs="+",
				default=["noplot_wj_mc_control", "noplot_wj_ss_mc_control"],
				help="Nicks for control region MC histogram. [Default: %(default)s]")

	def prepare_args(self, parser, plotData):
		super(EstimateWjets, self).prepare_args(parser, plotData)
		
		self._plotdict_keys = ["wjets_from_mc", "wjets_shape_nicks", "wjets_data_control_nicks",
		                       "wjets_data_substract_nicks", "wjets_mc_signal_nicks", "wjets_mc_control_nicks"]
		self.prepare_list_args(plotData, self._plotdict_keys)
		
		plotData.plotdict["wjets_data_substract_nicks"] = [nicks.split() for nicks in plotData.plotdict["wjets_data_substract_nicks"]]
	
	def run(self, plotData=None):
		super(EstimateWjets, self).run(plotData)
		
		# make sure that all necessary histograms are available
		for nicks in zip(*[plotData.plotdict[key] for key in self._plotdict_keys]):
			for nick in nicks:
				if isinstance(nick, basestring):
					assert isinstance(plotData.plotdict["root_objects"].get(nick), ROOT.TH1)
				elif not isinstance(nick, bool):
					for subnick in nick:
						assert isinstance(plotData.plotdict["root_objects"].get(subnick), ROOT.TH1)
		
		for wjets_from_mc, wjets_shape_nick, wjets_data_control_nick, wjets_data_substract_nicks, wjets_mc_signal_nick, wjets_mc_control_nick in zip(*[plotData.plotdict[key] for key in self._plotdict_keys]):
			if not wjets_from_mc: # skips the full estimation of this module and uses MC estimate of WJ instead.
				# Get yield and uncertainity in data in the control region
				yield_data_control = tools.PoissonYield(plotData.plotdict["root_objects"][wjets_data_control_nick])()
				for nick in wjets_data_substract_nicks:
					# subtract yields of all backgrounds
					yield_bkg_control = tools.PoissonYield(plotData.plotdict["root_objects"][nick])()
					if nick in plotData.metadata:
						yield_bkg_control = uncertainties.ufloat(
								plotData.metadata[nick].get("yield", yield_bkg_control.nominal_value),
								plotData.metadata[nick].get("yield_unc", yield_bkg_control.std_dev)
						)
					yield_data_control -= yield_bkg_control
				# make sure we don't have negative yields	
				yield_data_control = uncertainties.ufloat(max(0.0, yield_data_control.nominal_value), yield_data_control.std_dev)
				
				yield_mc_signal = tools.PoissonYield(plotData.plotdict["root_objects"][wjets_mc_signal_nick])()
				yield_mc_control = tools.PoissonYield(plotData.plotdict["root_objects"][wjets_mc_control_nick])()
				
				assert (yield_data_control*yield_mc_signal == 0.0) or (yield_mc_control != 0.0)
				# the final yield in the signal region is N_data, WJ^{SR} = N_data, WJ^{CR} * N_MC,WJ^{SR} / N_MC,WJ^{CR}
				final_yield = yield_data_control * yield_mc_signal
				if final_yield != 0.0:
					final_yield /= yield_mc_control
				log.debug("Relative statistical uncertainty of the yield for process W+jets (nick \"{nick}\") is {unc}.".format(nick=wjets_shape_nick, unc=final_yield.std_dev/final_yield.nominal_value if final_yield.nominal_value != 0.0 else 0.0))
				
				plotData.metadata[wjets_shape_nick] = {
					"yield" : final_yield.nominal_value,
					"yield_unc" : final_yield.std_dev,
					"yield_unc_rel" : abs(final_yield.std_dev/final_yield.nominal_value if final_yield.nominal_value != 0.0 else 0.0),
				}
				plotData.metadata
				# scale the wj file by the ratio of the estimated yield and the yield given by MC.
				integral_shape = tools.PoissonYield(plotData.plotdict["root_objects"][wjets_shape_nick])()
				if integral_shape != 0.0:
					scale_factor = final_yield / integral_shape
					log.debug("Scale factor for process W+jets (nick \"{nick}\") is {scale_factor}.".format(nick=wjets_shape_nick, scale_factor=scale_factor))
					plotData.plotdict["root_objects"][wjets_shape_nick].Scale(scale_factor.nominal_value)
