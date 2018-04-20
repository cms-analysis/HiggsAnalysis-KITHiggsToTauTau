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


class CalculateQcdOStoSSFactor(estimatebase.EstimateBase):
	def __init__(self):
		super(CalculateQcdOStoSSFactor, self).__init__()

	def modify_argument_parser(self, parser, args):
		super(CalculateQcdOStoSSFactor, self).modify_argument_parser(parser, args)
		
		self.calculate_qcd_scalefactor_options = parser.add_argument_group("QCD Scale Factor calculation options")
		
		self.calculate_qcd_scalefactor_options.add_argument("--qcd_extrapolate_ss_yield_nicks", nargs="+", default=[""],
				help="Nicks for histogram to plot. [Default: %(default)s]")
		self.calculate_qcd_scalefactor_options.add_argument("--qcd_extrapolate_os_yield_nicks", nargs="+", default=[""],
				help="Nicks for histogram to plot. [Default: %(default)s]")
		self.calculate_qcd_scalefactor_options.add_argument("--qcd_extrapolate_ss_substract_nicks", nargs="+", default=[""],
				help="Nicks for histogram to plot. [Default: %(default)s]")
		self.calculate_qcd_scalefactor_options.add_argument("--qcd_extrapolate_os_substract_nicks", nargs="+", default=[""],
				help="Nicks for histogram to plot. [Default: %(default)s]")
		self.calculate_qcd_scalefactor_options.add_argument("--qcd_os_invertedEIso_nicks", nargs="+", default=[""],
				help="Nicks for histogram to plot. [Default: %(default)s]")
		self.calculate_qcd_scalefactor_options.add_argument("--qcd_ss_invertedEIso_nicks", nargs="+", default=[""],
				help="Nicks for histogram to plot. [Default: %(default)s]")
		
	def prepare_args(self, parser, plotData):
		super(CalculateQcdOStoSSFactor, self).prepare_args(parser, plotData)
		self._plotdict_keys = ["qcd_extrapolate_ss_yield_nicks", "qcd_extrapolate_os_yield_nicks", "qcd_extrapolate_ss_substract_nicks", "qcd_extrapolate_os_substract_nicks", "qcd_ss_invertedEIso_nicks", "qcd_os_invertedEIso_nicks"]
		self.prepare_list_args(plotData, self._plotdict_keys)
		for index in ["qcd_extrapolate_ss_substract_nicks", "qcd_extrapolate_os_substract_nicks"]:
			plotData.plotdict[index] = [nicks.split() for nicks in plotData.plotdict[index]]

	def run(self, plotData=None):
		super(CalculateQcdOStoSSFactor, self).run(plotData)

		# make sure that all necessary histograms are available
		for nicks in zip(*[plotData.plotdict[key] for key in self._plotdict_keys[:-1]]):
			print " self._plotdict_keys[:-1]",  self._plotdict_keys[:-1]
			for nick in nicks:
				if isinstance(nick, basestring):
					assert isinstance(plotData.plotdict["root_objects"].get(nick), ROOT.TH1)
				elif (not isinstance(nick, float) and not isinstance(nick, bool)):
					for subnick in nick:
						assert isinstance(plotData.plotdict["root_objects"].get(subnick), ROOT.TH1)

		for  qcd_extrapolate_ss_yield_nick, qcd_extrapolate_os_yield_nick, qcd_extrapolate_ss_substract_nick, qcd_extrapolate_os_substract_nick, qcd_ss_invertedEIso_nick, qcd_os_invertedEIso_nick in zip(*[plotData.plotdict[key] for key in self._plotdict_keys]):
			########################################
			# calculate QCD os to ss extrapolation factor
			print "=======QCD========="
			print "self._plotdict_keys", self._plotdict_keys 

			yield_qcd_ss_invertedIso = tools.PoissonYield(plotData.plotdict["root_objects"][qcd_extrapolate_ss_yield_nick])()			
			yield_qcd_os_invertedIso = tools.PoissonYield(plotData.plotdict["root_objects"][qcd_extrapolate_os_yield_nick])()

			for nick in qcd_extrapolate_ss_substract_nick:
				yield_qcd_ss_invertedIso -= tools.PoissonYield(plotData.plotdict["root_objects"][nick])()
			
			for nick in qcd_extrapolate_os_substract_nick:
				yield_qcd_os_invertedIso -= tools.PoissonYield(plotData.plotdict["root_objects"][nick])()
			
			# qcd_ss_invertedEIso_nick stored the data, yield_qcd_ss_invertedIso stored the values subtracted MC from data, then one has to normalise stored value with the ratio
			integral_shape = tools.PoissonYield(plotData.plotdict["root_objects"][qcd_ss_invertedEIso_nick])()
			if integral_shape != 0.0:
				scale_factor = yield_qcd_ss_invertedIso / integral_shape
				plotData.plotdict["root_objects"][qcd_ss_invertedEIso_nick].Scale(scale_factor.nominal_value)

			integral_shape = tools.PoissonYield(plotData.plotdict["root_objects"][qcd_os_invertedEIso_nick])()
			if integral_shape != 0.0:
				scale_factor = yield_qcd_os_invertedIso / integral_shape
				plotData.plotdict["root_objects"][qcd_os_invertedEIso_nick].Scale(scale_factor.nominal_value)
			
			ss_os_extrapolation_factor = yield_qcd_os_invertedIso / yield_qcd_ss_invertedIso
			print "ss_os_extrapolation_factor", ss_os_extrapolation_factor

