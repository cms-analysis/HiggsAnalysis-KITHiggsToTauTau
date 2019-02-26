# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import hashlib
import math
import numpy

import Artus.HarryPlotter.analysisbase as analysisbase
import Artus.HarryPlotter.utility.roottools as roottools


class UncertaintiesPdf(analysisbase.AnalysisBase):
	"""Evaluate PDF Variations/Uncertainties."""

	def modify_argument_parser(self, parser, args):
		super(UncertaintiesPdf, self).modify_argument_parser(parser, args)

		self.uncertainties_pdf_options = parser.add_argument_group("{} options".format(self.name()))
		self.uncertainties_pdf_options.add_argument(
				"--uncertainties-pdf-reference-nicks", nargs="+",
				help="Nick names for the reference histograms"
		)
		self.uncertainties_pdf_options.add_argument(
				"--uncertainties-pdf-shifts-nicks", nargs="+",
				help="Nick names for the weighted/shifted histograms (whitespace separated)"
		)
		self.uncertainties_pdf_options.add_argument(
				"--uncertainties-pdf-result-nicks", nargs="+",
				help="Nick names for the resulting histograms. \"_up\"/\"_down\" will be appended automatically."
		)

	def prepare_args(self, parser, plotData):
		super(UncertaintiesPdf, self).prepare_args(parser, plotData)
		
		self.prepare_list_args(plotData, ["uncertainties_pdf_reference_nicks", "uncertainties_pdf_shifts_nicks", "uncertainties_pdf_result_nicks"])
		
		for index, (reference_nick, shift_nicks, result_nick) in enumerate(zip(
				*[plotData.plotdict[k] for k in ["uncertainties_pdf_reference_nicks", "uncertainties_pdf_shifts_nicks", "uncertainties_pdf_result_nicks"]]
		)):
			plotData.plotdict["uncertainties_pdf_shifts_nicks"][index] = shift_nicks.split()
			
			if result_nick is None:
				result_nick = "unc_pdf_" + reference_nick
			for shift in ["down", "up", "correlation"]:
				final_result_nick = result_nick + "_" + shift
				if not final_result_nick in plotData.plotdict["nicks"]:
					plotData.plotdict["nicks"].insert(
							max([plotData.plotdict["nicks"].index(nick) for nick in plotData.plotdict["uncertainties_pdf_shifts_nicks"][index]])+1,
							final_result_nick
					)

	def run(self, plotData=None):
		super(UncertaintiesPdf, self).run(plotData)
		
		for index, (reference_nick, shift_nicks, result_nick) in enumerate(zip(
				*[plotData.plotdict[k] for k in ["uncertainties_pdf_reference_nicks", "uncertainties_pdf_shifts_nicks", "uncertainties_pdf_result_nicks"]]
		)):
			
			reference_histogram = plotData.plotdict["root_objects"][reference_nick]
			reference_integral = reference_histogram.Integral()
			
			uncertainty = 0.0
			shift_histograms = [plotData.plotdict["root_objects"][nick] for nick in shift_nicks]
			for shift_histogram in shift_histograms:
				shift_integral = shift_histogram.Integral()
				uncertainty += pow(shift_integral - reference_integral, 2)
			
			if reference_integral != 0.0:
				uncertainty = math.sqrt(uncertainty / len(shift_nicks)) / reference_integral
			else:
				uncertainty = 0.0
			log.info("PDF uncertainty on nick \"{nick}\" is {unc}.".format(
					nick=reference_nick,
					unc=uncertainty
			))
			
			uncertainty_up_histogram = roottools.RootTools.histogram_calculation(
					lambda *args: args[0] + math.sqrt(sum([pow(arg-args[0], 2) for arg in args[1:]]) / len(shift_histograms)),
					None,
					reference_histogram,
					*shift_histograms
			)
			plotData.plotdict["root_objects"][result_nick+"_up"] = uncertainty_up_histogram
			
			uncertainty_down_histogram = roottools.RootTools.histogram_calculation(
					lambda *args: args[0] - math.sqrt(sum([pow(arg-args[0], 2) for arg in args[1:]]) / len(shift_histograms)),
					None,
					reference_histogram,
					*shift_histograms
			)
			plotData.plotdict["root_objects"][result_nick+"_down"] = uncertainty_down_histogram
			
			covariance_histogram = roottools.RootTools.histogram_calculation_2d(
					lambda *args: numpy.corrcoef(args[0], args[1])[0, 1],
					None,
					*shift_histograms
			)
			plotData.plotdict["root_objects"][result_nick+"_correlation"] = covariance_histogram

