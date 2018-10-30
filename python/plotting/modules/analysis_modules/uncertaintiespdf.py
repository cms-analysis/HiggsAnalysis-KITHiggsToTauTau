# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import hashlib
import math

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
		
		for index, (uncertainties_pdf_reference_nick, uncertainties_pdf_shift_nicks, uncertainties_pdf_result_nick) in enumerate(zip(
				*[plotData.plotdict[k] for k in ["uncertainties_pdf_reference_nicks", "uncertainties_pdf_shifts_nicks", "uncertainties_pdf_result_nicks"]]
		)):
			plotData.plotdict["uncertainties_pdf_shifts_nicks"][index] = uncertainties_pdf_shift_nicks.split()
			
			if uncertainties_pdf_result_nick is None:
				uncertainties_pdf_result_nick = "unc_pdf_" + uncertainties_pdf_reference_nick
			for shift in ["down", "up"]:
				final_result_nick = uncertainties_pdf_result_nick + "_" + shift
				if not final_result_nick in plotData.plotdict["nicks"]:
					plotData.plotdict["nicks"].insert(
							max([plotData.plotdict["nicks"].index(nick) for nick in plotData.plotdict["uncertainties_pdf_shifts_nicks"][index]])+1,
							final_result_nick
					)

	def run(self, plotData=None):
		super(UncertaintiesPdf, self).run(plotData)
		
		for index, (uncertainties_pdf_reference_nick, uncertainties_pdf_shift_nicks, uncertainties_pdf_result_nick) in enumerate(zip(
				*[plotData.plotdict[k] for k in ["uncertainties_pdf_reference_nicks", "uncertainties_pdf_shifts_nicks", "uncertainties_pdf_result_nicks"]]
		)):
			
			uncertainties_pdf_reference_histogram = plotData.plotdict["root_objects"][uncertainties_pdf_reference_nick]
			uncertainties_pdf_reference_integral = uncertainties_pdf_reference_histogram.Integral()
			
			uncertainty_pdf = 0.0
			uncertainties_pdf_shift_histograms = [plotData.plotdict["root_objects"][nick] for nick in uncertainties_pdf_shift_nicks]
			for uncertainties_pdf_shift_histogram in uncertainties_pdf_shift_histograms:
				uncertainties_pdf_shift_integral = uncertainties_pdf_shift_histogram.Integral()
				uncertainty_pdf += pow(uncertainties_pdf_shift_integral - uncertainties_pdf_reference_integral, 2)
			
			if uncertainties_pdf_reference_integral != 0.0:
				uncertainty_pdf = math.sqrt(uncertainty_pdf / len(uncertainties_pdf_shift_nicks)) / uncertainties_pdf_reference_integral
			else:
				uncertainty_pdf = 0.0
			log.info("PDF uncertainty on nick \"{nick}\" is {unc}.".format(
					nick=uncertainties_pdf_reference_nick,
					unc=uncertainty_pdf
			))
			
			uncertainty_pdf_up_histogram = roottools.RootTools.histogram_calculation(
					lambda *args: args[0] + math.sqrt(sum([pow(arg-args[0], 2) for arg in args[1:]]) / len(uncertainties_pdf_shift_histograms)),
					None,
					uncertainties_pdf_reference_histogram,
					*uncertainties_pdf_shift_histograms
			)
			plotData.plotdict["root_objects"][uncertainties_pdf_result_nick+"_up"] = uncertainty_pdf_up_histogram
			
			uncertainty_pdf_down_histogram = roottools.RootTools.histogram_calculation(
					lambda *args: args[0] - math.sqrt(sum([pow(arg-args[0], 2) for arg in args[1:]]) / len(uncertainties_pdf_shift_histograms)),
					None,
					uncertainties_pdf_reference_histogram,
					*uncertainties_pdf_shift_histograms
			)
			plotData.plotdict["root_objects"][uncertainties_pdf_result_nick+"_down"] = uncertainty_pdf_down_histogram

