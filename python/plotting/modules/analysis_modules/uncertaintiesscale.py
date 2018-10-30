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
		
		for index, (uncertainties_scale_reference_nick, uncertainties_scale_shift_nicks, uncertainties_scale_result_nick) in enumerate(zip(
				*[plotData.plotdict[k] for k in ["uncertainties_scale_reference_nicks", "uncertainties_scale_shifts_nicks", "uncertainties_scale_result_nicks"]]
		)):
			plotData.plotdict["uncertainties_scale_shifts_nicks"][index] = uncertainties_scale_shift_nicks.split()
			
			if uncertainties_scale_result_nick is None:
				uncertainties_scale_result_nick = "unc_scale_" + uncertainties_scale_reference_nick
			for shift in ["down", "up"]:
				final_result_nick = uncertainties_scale_result_nick + "_" + shift
				if not final_result_nick in plotData.plotdict["nicks"]:
					plotData.plotdict["nicks"].insert(
							max([plotData.plotdict["nicks"].index(nick) for nick in plotData.plotdict["uncertainties_scale_shifts_nicks"][index]])+1,
							final_result_nick
					)

	def run(self, plotData=None):
		super(UncertaintiesScale, self).run(plotData)
		
		for index, (uncertainties_scale_reference_nick, uncertainties_scale_shift_nicks, uncertainties_scale_result_nick) in enumerate(zip(
				*[plotData.plotdict[k] for k in ["uncertainties_scale_reference_nicks", "uncertainties_scale_shifts_nicks", "uncertainties_scale_result_nicks"]]
		)):
			
			uncertainties_scale_reference_histogram = plotData.plotdict["root_objects"][uncertainties_scale_reference_nick]
			uncertainties_scale_reference_integral = uncertainties_scale_reference_histogram.Integral()
			
			uncertainties_scale_shift_histograms = [plotData.plotdict["root_objects"][nick] for nick in uncertainties_scale_shift_nicks]
			uncertainties_scale_shift_integrals = [hist.Integral() for hist in uncertainties_scale_shift_histograms]
			
			uncertainty_scale = 0.0
			if uncertainties_scale_reference_integral != 0.0:
				uncertainty_scale = (max(uncertainties_scale_shift_integrals) - min(uncertainties_scale_shift_integrals)) / (2.0 * uncertainties_scale_reference_integral)
			log.info("Scale uncertainty on nick \"{nick}\" is {unc}.".format(
					nick=uncertainties_scale_reference_nick,
					unc=uncertainty_scale
			))
			
			uncertainty_scale_up_histogram = roottools.RootTools.histogram_calculation(
					lambda *args: max(args),
					None,
					*uncertainties_scale_shift_histograms
			)
			plotData.plotdict["root_objects"][uncertainties_scale_result_nick+"_up"] = uncertainty_scale_up_histogram
			
			uncertainty_scale_down_histogram = roottools.RootTools.histogram_calculation(
					lambda *args: min(args),
					None,
					uncertainties_scale_reference_histogram,
					*uncertainties_scale_shift_histograms
			)
			plotData.plotdict["root_objects"][uncertainties_scale_result_nick+"_down"] = uncertainty_scale_down_histogram

