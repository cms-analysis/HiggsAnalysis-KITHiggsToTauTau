# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import hashlib
import math

import Artus.HarryPlotter.analysisbase as analysisbase
import Artus.HarryPlotter.utility.roottools as roottools


class UncertaintiesScale(analysisbase.AnalysisBase):
	"""Evaluate PDF Variations/Uncertainties."""

	def modify_argument_parser(self, parser, args):
		super(UncertaintiesScale, self).modify_argument_parser(parser, args)

		self.uncertainties_scale_options = parser.add_argument_group("{} options".format(self.name()))
		self.uncertainties_scale_options.add_argument(
				"--uncertainties-scale-reference-nicks", nargs="+",
				help="Nick names for the reference histograms"
		)
		self.uncertainties_scale_options.add_argument(
				"--uncertainties-scale-shifts-nicks", nargs="+",
				help="Nick names for the weighted/shifted histograms (whitespace separated)"
		)
		self.uncertainties_scale_options.add_argument(
				"--uncertainties-scale-result-nicks", nargs="+",
				help="Nick names for the resulting histograms. \"_up\"/\"_down\" will be appended automatically."
		)

	def prepare_args(self, parser, plotData):
		super(UncertaintiesScale, self).prepare_args(parser, plotData)
		
		self.prepare_list_args(plotData, ["uncertainties_scale_reference_nicks", "uncertainties_scale_shifts_nicks", "uncertainties_scale_result_nicks"])
		
		for index, (reference_nick, shift_nicks, result_nick) in enumerate(zip(
				*[plotData.plotdict[k] for k in ["uncertainties_scale_reference_nicks", "uncertainties_scale_shifts_nicks", "uncertainties_scale_result_nicks"]]
		)):
			plotData.plotdict["uncertainties_scale_shifts_nicks"][index] = shift_nicks.split()
			
			if result_nick is None:
				result_nick = "unc_scale_" + reference_nick
			for shift in ["down", "up"]:
				final_result_nick = result_nick + "_" + shift
				if not final_result_nick in plotData.plotdict["nicks"]:
					plotData.plotdict["nicks"].insert(
							max([plotData.plotdict["nicks"].index(nick) for nick in plotData.plotdict["uncertainties_scale_shifts_nicks"][index]])+1,
							final_result_nick
					)

	def run(self, plotData=None):
		super(UncertaintiesScale, self).run(plotData)
		
		for index, (reference_nick, shift_nicks, result_nick) in enumerate(zip(
				*[plotData.plotdict[k] for k in ["uncertainties_scale_reference_nicks", "uncertainties_scale_shifts_nicks", "uncertainties_scale_result_nicks"]]
		)):
			
			reference_histogram = plotData.plotdict["root_objects"][reference_nick]
			reference_integral = reference_histogram.Integral()
			
			shift_histograms = [plotData.plotdict["root_objects"][nick] for nick in shift_nicks]
			shift_integrals = [hist.Integral() for hist in shift_histograms]
			
			uncertainty = 0.0
			if reference_integral != 0.0:
				uncertainty = (max(shift_integrals) - min(shift_integrals)) / (2.0 * reference_integral)
			log.info("QCD scale uncertainty on nick \"{nick}\" is {unc}.".format(
					nick=reference_nick,
					unc=uncertainty
			))
			
			uncertainty_up_histogram = roottools.RootTools.histogram_calculation(
					lambda *args: max(args),
					None,
					*shift_histograms
			)
			plotData.plotdict["root_objects"][result_nick+"_up"] = uncertainty_up_histogram
			
			uncertainty_down_histogram = roottools.RootTools.histogram_calculation(
					lambda *args: min(args),
					None,
					reference_histogram,
					*shift_histograms
			)
			plotData.plotdict["root_objects"][result_nick+"_down"] = uncertainty_down_histogram

