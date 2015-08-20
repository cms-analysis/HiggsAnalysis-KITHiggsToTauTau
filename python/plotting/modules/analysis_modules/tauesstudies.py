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
		self.prepare_list_args(plotData, ["data_nicks", "ztt_nicks","es_shifts","res_hist_nick"])

		for index, (data_nicks, ztt_nicks, es_shifts, res_hist_nick) in enumerate(zip(
				*[plotData.plotdict[k] for k in ["data_nicks", "ztt_nicks","es_shifts","res_hist_nick"]]
		)):
			plotData.plotdict["data_nicks"][index] = data_nicks.split()
			plotData.plotdict["ztt_nicks"][index] = ztt_nicks.split()
			plotData.plotdict["es_shifts"][index] = es_shifts.split()

			if not plotData.plotdict["res_hist_nick"][index] in plotData.plotdict["nicks"]:
				plotData.plotdict["nicks"].insert(
					plotData.plotdict["nicks"].index(plotData.plotdict["ztt_nicks"][index][0]),
					plotData.plotdict["res_hist_nick"][index]
				)

	def run(self, plotData=None):
		super(TauEsStudies, self).run(plotData)

		es_shifts=[]
		chi2res=[]

		for index, (data_nick, ztt_nick, es_shift) in enumerate(zip(
				*[plotData.plotdict[k] for k in ["data_nicks", "ztt_nicks","es_shifts"]]
		)):
			print "chi2test between ", data_nick, " and ", ztt_nick
			es_shifts.append(float(es_shift[0]))
			chi2res.extend([plotData.plotdict["root_objects"][ztt_nick[0]].Chi2Test(plotData.plotdict["root_objects"][data_nick[0]], "CHI2")])

			if index == 0:
				chi2min = chi2res[0]
				min_shift = es_shifts[0]
			if chi2min > chi2res[index]:
				chi2min = chi2res[index]
				min_shift = es_shifts[index]

		for x_value, y_value in zip(es_shifts, chi2res):
			print "Shift: ", x_value, " Chi2Val: ", y_value

		print "Minimum found at: ", min_shift

		for res_hist_nick in zip(
				*[plotData.plotdict["res_hist_nick"]]
		):

			#Graph
			Chi2Graph = ROOT.TGraphErrors(
					len(es_shifts),
					array.array("d", es_shifts), array.array("d", chi2res)
			)
			plotData.plotdict.setdefault("root_objects", {})[res_hist_nick[0]] = Chi2Graph

			plotData.plotdict["root_objects"][res_hist_nick[0]].SetName(res_hist_nick[0])
			plotData.plotdict["root_objects"][res_hist_nick[0]].SetTitle("")

			#Fit function
			fit2chi = ROOT.TF1("f1","[0] + [1]*(x-[2])*(x-[2])",min(es_shifts),max(es_shifts))
			Chi2Graph.Fit("f1","R")

			#get minimum
			print "Minimum of fitfunction at: ", fit2chi.GetMinimumX(min(es_shifts),max(es_shifts))

