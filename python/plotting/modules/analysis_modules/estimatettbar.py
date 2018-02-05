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


class EstimateTtbar(estimatebase.EstimateBase):
	def __init__(self):
		super(EstimateTtbar, self).__init__()

	def modify_argument_parser(self, parser, args):
		super(EstimateTtbar, self).modify_argument_parser(parser, args)
		
		self.estimate_ttbar_options = parser.add_argument_group("TTbar estimation options")
		self.estimate_ttbar_options.add_argument("--ttbar-shape-nicks", nargs="+",
				default=["ttj"],
				help="Nicks for histogram to plot. [Default: %(default)s]")
		self.estimate_ttbar_options.add_argument("--ttbar-data-control-nicks", nargs="+",
				default=["noplot_ttj_data_control"],
				help="Nicks for control region data histogram. [Default: %(default)s]")
		self.estimate_ttbar_options.add_argument("--ttbar-data-subtract-nicks", nargs="+",
				default=["noplot_ztt_mc_ttj_control noplot_zll_ttj_control noplot_wj_ttj_control noplot_vv_ttj_control"],
				help="Nicks for control region histogram to subtract from data (whitespace separated). [Default: %(default)s]")
		self.estimate_ttbar_options.add_argument("--ttbar-mc-signal-nicks", nargs="+",
				default=["noplot_ttj_mc_signal"],
				help="Nicks for signal region MC histogram. [Default: %(default)s]")
		self.estimate_ttbar_options.add_argument("--ttbar-mc-control-nicks", nargs="+",
				default=["noplot_ttj_mc_control"],
				help="Nicks for control region MC histogram. [Default: %(default)s]")

	def prepare_args(self, parser, plotData):
		super(EstimateTtbar, self).prepare_args(parser, plotData)
		
		self._plotdict_keys = ["ttbar_shape_nicks", "ttbar_data_control_nicks",
		                       "ttbar_data_subtract_nicks", "ttbar_mc_signal_nicks", "ttbar_mc_control_nicks"]
		self.prepare_list_args(plotData, self._plotdict_keys)
		
		plotData.plotdict["ttbar_data_subtract_nicks"] = [nicks.split() for nicks in plotData.plotdict["ttbar_data_subtract_nicks"]]
	
	def run(self, plotData=None):
		super(EstimateTtbar, self).run(plotData)
		
		# make sure that all necessary histograms are available
		for nicks in zip(*[plotData.plotdict[key] for key in self._plotdict_keys]):
			for nick in nicks:
				if isinstance(nick, basestring):
					assert isinstance(plotData.plotdict["root_objects"].get(nick), ROOT.TH1)
				elif not isinstance(nick, bool):
					for subnick in nick:
						assert isinstance(plotData.plotdict["root_objects"].get(subnick), ROOT.TH1)
		
		for ttbar_shape_nick, ttbar_data_control_nick, ttbar_data_subtract_nicks, ttbar_mc_signal_nick, ttbar_mc_control_nick in zip(*[plotData.plotdict[key] for key in self._plotdict_keys]):
				yield_data_control = tools.PoissonYield(plotData.plotdict["root_objects"][ttbar_data_control_nick])()
				#print "data_control_yield from nick " + ttbar_data_control_nick + " : " + str(yield_data_control)
				for nick in ttbar_data_subtract_nicks:
					yield_bkg_control = tools.PoissonYield(plotData.plotdict["root_objects"][nick])()
					#print "\t minus " + nick + " : " + str(yield_bkg_control)
					if nick in plotData.metadata:
						yield_bkg_control = uncertainties.ufloat(
								plotData.metadata[nick].get("yield", yield_bkg_control.nominal_value),
								plotData.metadata[nick].get("yield_unc", yield_bkg_control.std_dev)
						)
					yield_data_control -= yield_bkg_control
				#print "data_control_yield final "  + str(yield_data_control)
				yield_data_control = max(0.0, yield_data_control)
				
				yield_mc_signal = tools.PoissonYield(plotData.plotdict["root_objects"][ttbar_mc_signal_nick])()
				yield_mc_control = tools.PoissonYield(plotData.plotdict["root_objects"][ttbar_mc_control_nick])()
				
				#print "data_mc_signal "  + str(yield_mc_signal)
				#print "data_mc_control "  + str(yield_mc_control)
				integral_shape = plotData.plotdict["root_objects"][ttbar_shape_nick].Integral()
				final_yield = yield_mc_control / yield_data_control * integral_shape
				log.debug("Relative statistical uncertainty of the yield for process ttbar+jets (nick \"{nick}\") is {unc}.".format(nick=ttbar_shape_nick, unc=final_yield.std_dev/final_yield.nominal_value if final_yield.nominal_value != 0.0 else 0.0))
					
				plotData.metadata[ttbar_shape_nick] = {
					"yield" : final_yield.nominal_value,
					"yield_unc" : final_yield.std_dev,
					"yield_unc_rel" : abs(final_yield.std_dev/final_yield.nominal_value if final_yield.nominal_value != 0.0 else 0.0),
				}
				
				if integral_shape != 0.0:
					scale_factor = integral_shape / final_yield
					#print "scale factor: " + str(scale_factor)
					log.debug("Scale factor for process ttbar+jets (nick \"{nick}\") is {scale_factor}.".format(nick=ttbar_shape_nick, scale_factor=scale_factor))
					plotData.plotdict["root_objects"][ttbar_shape_nick].Scale(scale_factor.nominal_value)

