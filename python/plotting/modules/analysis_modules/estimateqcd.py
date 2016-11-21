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


class EstimateQcd(estimatebase.EstimateBase):
	def __init__(self):
		super(EstimateQcd, self).__init__()

	def modify_argument_parser(self, parser, args):
		super(EstimateQcd, self).modify_argument_parser(parser, args)
		
		self.estimate_qcd_options = parser.add_argument_group("QCD estimation options")
		self.estimate_qcd_options.add_argument("--qcd-shape-nicks", nargs="+",
				help="Nicks for histogram to plot. [Default: %(default)s]")
		self.estimate_qcd_options.add_argument("--qcd-yield-nicks", nargs="+",
				help="Nicks for histogram containing the yield in data with the final selection that is then scaled. [Default: %(default)s]")
		self.estimate_qcd_options.add_argument("--qcd-shape-subtract-nicks", nargs="+",
				help="Nicks for histogram to be subtracted from the shape. [Default: %(default)s]")
		self.estimate_qcd_options.add_argument("--qcd-yield-subtract-nicks", nargs="+",
				help="Nicks for control region histogram to substract from data (whitespace separated). [Default: %(default)s]")
		self.estimate_qcd_options.add_argument("--qcd-extrapolation-factors-ss-os", nargs="+", type=float, default=[1.06],
				help="Extrapolation factors of OS/SS yields. [Default: %(default)s]")
		self.estimate_qcd_options.add_argument("--qcd-subtract-shape", action="store_true", default=False,
				help="Subtract the shape of control region histograms from data. [Default: %(default)s]")
		self.estimate_qcd_options.add_argument("--qcd-scale-factor", default=1.0, type=float,
				help="Scale QCD by this factor. [Default: %(default)s]")

	def prepare_args(self, parser, plotData):
		super(EstimateQcd, self).prepare_args(parser, plotData)
		
		self._plotdict_keys = ["qcd_shape_nicks", "qcd_yield_nicks", "qcd_yield_subtract_nicks", "qcd_shape_subtract_nicks", "qcd_extrapolation_factors_ss_os"]
		self.prepare_list_args(plotData, self._plotdict_keys)

		plotData.plotdict["qcd_shape_subtract_nicks"] = [nicks.split() for nicks in plotData.plotdict["qcd_shape_subtract_nicks"]]	
		plotData.plotdict["qcd_yield_subtract_nicks"] = [nicks.split() for nicks in plotData.plotdict["qcd_yield_subtract_nicks"]]	
		
		# make sure that all necessary histograms are available
		for nicks in zip(*[plotData.plotdict[key] for key in self._plotdict_keys]):
			for nick in nicks:
				if isinstance(nick, basestring):
					assert isinstance(plotData.plotdict["root_objects"].get(nick), ROOT.TH1)
				elif (not isinstance(nick, float) and not isinstance(nick, bool)):
					for subnick in nick:
						assert isinstance(plotData.plotdict["root_objects"].get(subnick), ROOT.TH1)
	
	def run(self, plotData=None):
		super(EstimateQcd, self).run(plotData)
		
		for qcd_shape_nick, qcd_yield_nick, qcd_yield_subtract_nicks, qcd_shape_subtract_nicks, qcd_extrapolation_factor_ss_os in zip(*[plotData.plotdict[key] for key in self._plotdict_keys]):
			
			yield_qcd = tools.PoissonYield(plotData.plotdict["root_objects"][qcd_yield_nick])()
			# estimate the QCD yield
			# print "yield qcd total: " + str(yield_qcd)
			for nick in qcd_yield_subtract_nicks:
				yield_bkg = tools.PoissonYield(plotData.plotdict["root_objects"][nick])()
				#print "minus " + nick + "  " + str(yield_bkg)	
				yield_qcd -= yield_bkg
			yield_qcd = max(0.0, yield_qcd)
			if(yield_qcd == 0.0):
				log.warning("QCD yield is 0!")
			#  QCD shape
			
			#print "shape total: " + str(tools.PoissonYield(plotData.plotdict["root_objects"][qcd_shape_nick])())
			for nick in qcd_shape_subtract_nicks:
				#print "\t minus " + nick + " " + str(tools.PoissonYield(plotData.plotdict["root_objects"][nick])())
				plotData.plotdict["root_objects"][qcd_shape_nick].Add(plotData.plotdict["root_objects"][nick], -1.0/plotData.plotdict["qcd_scale_factor"])
			
			shape_yield = tools.PoissonYield(plotData.plotdict["root_objects"][qcd_shape_nick])()
			if shape_yield != 0.0:
				scale_factor = yield_qcd / shape_yield * qcd_extrapolation_factor_ss_os
			final_yield_qcd = yield_qcd * qcd_extrapolation_factor_ss_os
			#log.debug("Relative statistical uncertainty of the yield for process QCD (nick \"{nick}\") is {unc}.".format(nick=qcd_data_shape_nick, unc=final_yield.std_dev/final_yield.nominal_value if final_yield.nominal_value != 0.0 else 0.0))
			plotData.plotdict["root_objects"][qcd_shape_nick].Scale(scale_factor.nominal_value)
			#print "QCD em estimation summary"
			#print "scale factor : " + str(scale_factor)
			#print "shape_yield :"  + str(shape_yield)
			#print "yield_qcd :" + str(yield_qcd)
			# save to be picked up
			plotData.metadata[qcd_shape_nick] = {
				"yield" : final_yield_qcd.nominal_value,
				"yield_unc" : final_yield_qcd.std_dev,
				"yield_unc_rel" : abs(final_yield_qcd.std_dev/final_yield_qcd.nominal_value if final_yield_qcd.nominal_value != 0.0 else 0.0),
			}
