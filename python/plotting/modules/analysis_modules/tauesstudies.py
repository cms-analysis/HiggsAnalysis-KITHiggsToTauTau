# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import array
import copy
import hashlib
import math

import ROOT

import Artus.HarryPlotter.analysisbase as analysisbase
import Artus.HarryPlotter.utility.roottools as roottools

class TauEsStudies(analysisbase.AnalysisBase):
	"""TauEsStudies for comparing histograms"""

	def __init__(self):
		super(TauEsStudies, self).__init__()

	def modify_argument_parser(self, parser, args):
		super(TauEsStudies, self).modify_argument_parser(parser, args)
		
		self.tauesstudies_options = parser.add_argument_group("TauEsStudies options")
		self.tauesstudies_options.add_argument(
				"--data-nicks", nargs="+",
				help="Nick names (whitespace separated) of data"
		)
		self.tauesstudies_options.add_argument(
				"--ztt-nicks", nargs="+",
				help="Nick names (whitespace separated) of ztt with shifts"
		)
		self.tauesstudies_options.add_argument(
				"--es-shifts", nargs="+",
				help="ES shifts (whitespace separated)"
		)
		self.tauesstudies_options.add_argument(
				"--res-hist-nick", nargs="+",
				help="Nick name of resulting histogram"
		)

	def prepare_args(self, parser, plotData):
		super(TauEsStudies, self).prepare_args(parser, plotData)

		self.prepare_list_args(plotData, ["data_nicks", "ztt_nicks","res_hist_nick"])
		
		for index, (data_nicks, ztt_nicks, res_hist_nick) in enumerate(zip(
				*[plotData.plotdict[k] for k in ["data_nicks", "ztt_nicks","res_hist_nick"]]
		)):
			plotData.plotdict["data_nicks"][index] = data_nicks.split()
			plotData.plotdict["ztt_nicks"][index] = ztt_nicks.split()
			
			if not plotData.plotdict["res_hist_nick"][index] in plotData.plotdict["nicks"]:
				plotData.plotdict["nicks"].insert(
					plotData.plotdict["nicks"].index(plotData.plotdict["ztt_nicks"][index][0]),
					plotData.plotdict["res_hist_nick"][index]
				)
		
	def run(self, plotData=None):
		super(TauEsStudies, self).run(plotData)

		root_histogram = roottools.RootTools.create_root_histogram(
				x_bins=array.array("d", [0]),
				profile_histogram=False,
				name="chi2shifts"
		)

		es_shifts=[0.94,0.95,0.96,0.97,0.98,0.99,1.0,1.01,1.02,1.03,1.04,1.05,1.06,1.07,1.08]
		root_histogram.SetBins(len(es_shifts),es_shifts[0],es_shifts[len(es_shifts)-1]+(es_shifts[len(es_shifts)-1]-es_shifts[0])/len(es_shifts))

		plotData.plotdict["ztt_nicks"]
		
		chi2res = []
		
		for index, (data_nick, ztt_nick) in enumerate(zip(
				*[plotData.plotdict[k] for k in ["data_nicks", "ztt_nicks"]]
		)):
			print "chi2test between ", data_nick, " and ", ztt_nick
			chi2res.extend([plotData.plotdict["root_objects"][ztt_nick[0]].Chi2Test(plotData.plotdict["root_objects"][data_nick[0]], "CHI2")])
#			print(len(chi2res))
#			print(chi2res[index])
			if index == 0:
				chi2min = chi2res[0]
				min_shift = es_shifts[0]
			if chi2min > chi2res[index]:
				chi2min = chi2res[index]
				min_shift = es_shifts[index]

		for x_value, y_value in zip(es_shifts, chi2res):
			print "Shift: ", x_value, " Chi2Val: ", y_value
			global_bin = root_histogram.FindBin(x_value)
			root_histogram.SetBinContent(global_bin, y_value)
			
		print "min found at :", min_shift

		root_histogram = root_histogram.DrawNormalized()
		plotData.plotdict.setdefault("root_objects", {})["chi2_result"] = root_histogram

