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
		
		for index, (uncertainties_alpha_s_reference_nick, uncertainties_alpha_s_reference_value, uncertainties_alpha_s_shift_nicks, uncertainties_alpha_s_shift_values, uncertainties_alpha_s_result_nick) in enumerate(zip(
				*[plotData.plotdict[k] for k in ["uncertainties_alpha_s_reference_nicks", "uncertainties_alpha_s_reference_values", "uncertainties_alpha_s_shifts_nicks", "uncertainties_alpha_s_shifts_values", "uncertainties_alpha_s_result_nicks"]]
		)):
			plotData.plotdict["uncertainties_alpha_s_shifts_nicks"][index] = uncertainties_alpha_s_shift_nicks.split()
			plotData.plotdict["uncertainties_alpha_s_shifts_values"][index] = [float(value) for value in uncertainties_alpha_s_shift_values.split()]
			assert len(plotData.plotdict["uncertainties_alpha_s_shifts_nicks"][index]) == len(plotData.plotdict["uncertainties_alpha_s_shifts_values"][index])
			if len(plotData.plotdict["uncertainties_alpha_s_shifts_nicks"][index]) > 1:
				log.warning("Uncertainty estimation for alpha_s currently only implemented for one shifted histogram. Take first given histogram.")
			
			if uncertainties_alpha_s_result_nick is None:
				uncertainties_alpha_s_result_nick = "unc_alpha_s_" + uncertainties_alpha_s_reference_nick
			for shift in ["down", "up"]:
				final_result_nick = uncertainties_alpha_s_result_nick + "_" + shift
				if not final_result_nick in plotData.plotdict["nicks"]:
					plotData.plotdict["nicks"].insert(
							max([plotData.plotdict["nicks"].index(nick) for nick in plotData.plotdict["uncertainties_alpha_s_shifts_nicks"][index]])+1,
							final_result_nick
					)

	def run(self, plotData=None):
		super(UncertaintiesAlphaS, self).run(plotData)
		
		for index, (uncertainties_alpha_s_reference_nick, uncertainties_alpha_s_reference_value, uncertainties_alpha_s_shift_nicks, uncertainties_alpha_s_shift_values, uncertainties_alpha_s_result_nick) in enumerate(zip(
				*[plotData.plotdict[k] for k in ["uncertainties_alpha_s_reference_nicks", "uncertainties_alpha_s_reference_values", "uncertainties_alpha_s_shifts_nicks", "uncertainties_alpha_s_shifts_values", "uncertainties_alpha_s_result_nicks"]]
		)):
			
			uncertainties_alpha_s_reference_histogram = plotData.plotdict["root_objects"][uncertainties_alpha_s_reference_nick]
			uncertainties_alpha_s_reference_integral = uncertainties_alpha_s_reference_histogram.Integral()
			
			uncertainties_alpha_s_shift_histogram = plotData.plotdict["root_objects"][uncertainties_alpha_s_shift_nicks[0]]
			uncertainties_alpha_s_shift_integral = uncertainties_alpha_s_shift_histogram.Integral()
			uncertainties_alpha_s_shift_value = uncertainties_alpha_s_shift_values[0]
			
			uncertainty_alpha_s = 0.0
			if uncertainties_alpha_s_reference_integral != 0.0:
				uncertainty_alpha_s = 0.0015 * (uncertainties_alpha_s_shift_integral - uncertainties_alpha_s_reference_integral) / ((uncertainties_alpha_s_shift_value - uncertainties_alpha_s_reference_value) * uncertainties_alpha_s_reference_integral)
			log.info("alpha_s uncertainty on nick \"{nick}\" is {unc}.".format(
					nick=uncertainties_alpha_s_reference_nick,
					unc=uncertainty_alpha_s
			))
			
			uncertainty_alpha_s_up_histogram = roottools.RootTools.histogram_calculation(
					lambda *args: args[0] + 0.0015 * (args[1] - args[0]) / (uncertainties_alpha_s_shift_value - uncertainties_alpha_s_reference_value),
					None,
					uncertainties_alpha_s_reference_histogram,
					uncertainties_alpha_s_shift_histogram
			)
			plotData.plotdict["root_objects"][uncertainties_alpha_s_result_nick+"_up"] = uncertainty_alpha_s_up_histogram
			
			uncertainty_alpha_s_down_histogram = roottools.RootTools.histogram_calculation(
					lambda *args: args[0] - 0.0015 * (args[1] - args[0]) / (uncertainties_alpha_s_shift_value - uncertainties_alpha_s_reference_value),
					None,
					uncertainties_alpha_s_reference_histogram,
					uncertainties_alpha_s_shift_histogram
			)
			plotData.plotdict["root_objects"][uncertainties_alpha_s_result_nick+"_down"] = uncertainty_alpha_s_down_histogram

