# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import hashlib
import math

import Artus.HarryPlotter.analysisbase as analysisbase
import Artus.HarryPlotter.utility.roottools as roottools


class UncertaintiesAlphaS(analysisbase.AnalysisBase):
	"""Evaluate PDF Variations/Uncertainties."""

	def modify_argument_parser(self, parser, args):
		super(UncertaintiesAlphaS, self).modify_argument_parser(parser, args)

		self.uncertainties_alpha_s_options = parser.add_argument_group("{} options".format(self.name()))
		self.uncertainties_alpha_s_options.add_argument(
				"--uncertainties-alpha-s-reference-nicks", nargs="+",
				help="Nick names for the reference histograms"
		)
		self.uncertainties_alpha_s_options.add_argument(
				"--uncertainties-alpha-s-reference-values", type=float, nargs="+", default=[0.130],
				help="alpha_s values for the reference histograms. [Default: %(default)s]"
		)
		self.uncertainties_alpha_s_options.add_argument(
				"--uncertainties-alpha-s-shifts-nicks", nargs="+",
				help="Nick names for the weighted/shifted histograms (whitespace separated)."
		)
		self.uncertainties_alpha_s_options.add_argument(
				"--uncertainties-alpha-s-shifts-values", nargs="+", default=["0.118"],
				help="alpha_s values for the weighted/shifted histograms (whitespace separated)"
		)
		self.uncertainties_alpha_s_options.add_argument(
				"--uncertainties-alpha-s-result-nicks", nargs="+",
				help="Nick names for the resulting histograms. \"_up\"/\"_down\" will be appended automatically."
		)

	def prepare_args(self, parser, plotData):
		super(UncertaintiesAlphaS, self).prepare_args(parser, plotData)
		
		self.prepare_list_args(plotData, ["uncertainties_alpha_s_reference_nicks", "uncertainties_alpha_s_reference_values", "uncertainties_alpha_s_shifts_nicks", "uncertainties_alpha_s_shifts_values", "uncertainties_alpha_s_result_nicks"])
		
		for index, (reference_nick, reference_value, shift_nicks, shift_values, result_nick) in enumerate(zip(
				*[plotData.plotdict[k] for k in ["uncertainties_alpha_s_reference_nicks", "uncertainties_alpha_s_reference_values", "uncertainties_alpha_s_shifts_nicks", "uncertainties_alpha_s_shifts_values", "uncertainties_alpha_s_result_nicks"]]
		)):
			plotData.plotdict["uncertainties_alpha_s_shifts_nicks"][index] = shift_nicks.split()
			plotData.plotdict["uncertainties_alpha_s_shifts_values"][index] = [float(value) for value in shift_values.split()]
			assert len(plotData.plotdict["uncertainties_alpha_s_shifts_nicks"][index]) == len(plotData.plotdict["uncertainties_alpha_s_shifts_values"][index])
			if len(plotData.plotdict["uncertainties_alpha_s_shifts_nicks"][index]) > 1:
				log.warning("Uncertainty estimation for alpha_s currently only implemented for one shifted histogram. Take first given histogram.")
			
			if result_nick is None:
				result_nick = "unc_alpha_s_" + reference_nick
			for shift in ["down", "up"]:
				final_result_nick = result_nick + "_" + shift
				if not final_result_nick in plotData.plotdict["nicks"]:
					plotData.plotdict["nicks"].insert(
							max([plotData.plotdict["nicks"].index(nick) for nick in plotData.plotdict["uncertainties_alpha_s_shifts_nicks"][index]])+1,
							final_result_nick
					)

	def run(self, plotData=None):
		super(UncertaintiesAlphaS, self).run(plotData)
		
		for index, (reference_nick, reference_value, shift_nicks, shift_values, result_nick) in enumerate(zip(
				*[plotData.plotdict[k] for k in ["uncertainties_alpha_s_reference_nicks", "uncertainties_alpha_s_reference_values", "uncertainties_alpha_s_shifts_nicks", "uncertainties_alpha_s_shifts_values", "uncertainties_alpha_s_result_nicks"]]
		)):
			
			reference_histogram = plotData.plotdict["root_objects"][reference_nick]
			reference_integral = reference_histogram.Integral()
			
			shift_histogram = plotData.plotdict["root_objects"][shift_nicks[0]]
			shift_integral = shift_histogram.Integral()
			shift_value = shift_values[0]
			
			uncertainty = 0.0
			if reference_integral != 0.0:
				uncertainty = 0.0015 * (shift_integral - reference_integral) / ((shift_value - reference_value) * reference_integral)
			log.info("alpha_s uncertainty on nick \"{nick}\" is {unc}.".format(
					nick=reference_nick,
					unc=uncertainty
			))
			
			uncertainty_up_histogram = roottools.RootTools.histogram_calculation(
					lambda *args: args[0] + 0.0015 * (args[1] - args[0]) / (shift_value - reference_value),
					None,
					reference_histogram,
					shift_histogram
			)
			plotData.plotdict["root_objects"][result_nick+"_up"] = uncertainty_up_histogram
			
			uncertainty_down_histogram = roottools.RootTools.histogram_calculation(
					lambda *args: args[0] - 0.0015 * (args[1] - args[0]) / (shift_value - reference_value),
					None,
					reference_histogram,
					shift_histogram
			)
			plotData.plotdict["root_objects"][result_nick+"_down"] = uncertainty_down_histogram

