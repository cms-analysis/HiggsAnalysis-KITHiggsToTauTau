# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import array
import copy
import hashlib
import math

import sys
import ROOT

import Artus.HarryPlotter.analysisbase as analysisbase
import Artus.HarryPlotter.utility.roottools as roottools

class TauEsStudies(analysisbase.AnalysisBase):

	def __init__(self):
		super(TauEsStudies, self).__init__()

	def modify_argument_parser(self, parser, args):
		super(TauEsStudies, self).modify_argument_parser(parser, args)

		self.tauesstudies_options = parser.add_argument_group("TauEsStudies options")
		self.tauesstudies_options.add_argument(
				"--data-nicks", nargs="+",
				help="Nick names of data"
		)
		self.tauesstudies_options.add_argument(
				"--bkg-nicks", nargs="+",
				help="Nick names (whitespace separated) of bkg with shifts"
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
				"--res-hist-nicks", default="fit_result",
				help="Nick name of resulting histogram"
		)
		self.tauesstudies_options.add_argument(
				"--fit-method", default="logllh",
	            help="Choose logllh or chi2"
	    )

	def prepare_args(self, parser, plotData):
		super(TauEsStudies, self).prepare_args(parser, plotData)
		self.prepare_list_args(plotData, ["data_nicks","bkg_nicks","ztt_nicks","es_shifts","res_hist_nicks"])

		for index, (data_nick, bkg_nicks, ztt_nicks, es_shifts, res_hist_nick) in enumerate(zip(
				*[plotData.plotdict[k] for k in ["data_nicks","bkg_nicks","ztt_nicks","es_shifts","res_hist_nicks"]]
		)):
			plotData.plotdict["ztt_nicks"][index] = ztt_nicks.split()
			plotData.plotdict["es_shifts"][index] = es_shifts.split()

			if not bkg_nicks is None:
				plotData.plotdict["bkg_nicks"][index] = bkg_nicks.split()

			if not plotData.plotdict["res_hist_nicks"][index] in plotData.plotdict["nicks"]:
				plotData.plotdict["nicks"].insert(
					plotData.plotdict["nicks"].index(plotData.plotdict["ztt_nicks"][index][0]),
					plotData.plotdict["res_hist_nicks"][index]
				)
				plotData.plotdict["labels"].insert(
					plotData.plotdict["labels"].index(plotData.plotdict["ztt_nicks"][index][0]),
					plotData.plotdict["res_hist_nicks"][index]
				)

	def run(self, plotData=None):
		super(TauEsStudies, self).run(plotData)

		if plotData.plotdict["fit_method"] == "logllh":
			print "Start Roofit Likelihood Scan ..."

			best_shifts=[]
			errors_1sigma = []
			errors_2sigma = []

			# always set this to stop ROOT doing odd things
			ROOT.PyConfig.IgnoreCommandLineOptions = True
			ROOT.gROOT.SetBatch(ROOT.kTRUE)

			#for each pt_range, get the best shift with uncertainty
			for res_hist_nick, data_nick, bkg_nicks, ztt_nicks, es_shifts in zip(
					*[plotData.plotdict[k] for k in ["res_hist_nicks","data_nicks","bkg_nicks","ztt_nicks","es_shifts"]]
			):
				# negative log likelihood list and delta nll list
				nll_list = []
				dnll_list = []
				es_shifts_float=[]

				# Have to define the "x-axis" variable
				mass = ROOT.RooRealVar('mass', 'mass', 0, 2)

				for ztt_nick, es_shift in zip(ztt_nicks, es_shifts):
					es_shifts_float.append(float(es_shift))

					# Convert Bkg TH1s into RooDataHists, Pdfs and norms
					bkg_th1s = []
					bkg_rdhs = []
					bkg_pdfs = []
					bkg_norms = []
					for bkg_nick in zip(bkg_nicks):
						bkg_th1s.append(plotData.plotdict["root_objects"][bkg_nick[0]])
						bkg_rdhs.append(ROOT.RooDataHist(bkg_th1s[-1].GetName(), bkg_th1s[-1].GetName(), ROOT.RooArgList(mass), ROOT.RooFit.Import(bkg_th1s[-1], False)))
						bkg_pdfs.append(ROOT.RooHistPdf(bkg_th1s[-1].GetName()+'_pdf', bkg_th1s[-1].GetName(), ROOT.RooArgSet(mass), bkg_rdhs[-1]))
						bkg_norms.append(ROOT.RooRealVar(bkg_th1s[-1].GetName()+'_norm', bkg_th1s[-1].GetName(), bkg_th1s[-1].Integral(), bkg_th1s[-1].Integral()/2., bkg_th1s[-1].Integral()*2.))

					# no floating bkg
					for bkg_norm in bkg_norms:
						bkg_norm.setConstant(True)

					# Convert data TH1 into a RooDataHist
					data_th1 = plotData.plotdict["root_objects"][data_nick]
					data_rdh = ROOT.RooDataHist(data_th1.GetName(), data_th1.GetName(), ROOT.RooArgList(mass), ROOT.RooFit.Import(data_th1, False))

					# Convert the ztt TH1 into RooDataHist
					ztt_th1 = plotData.plotdict["root_objects"][ztt_nick]
					ztt_rdh = ROOT.RooDataHist(ztt_th1.GetName(), ztt_th1.GetName(), ROOT.RooArgList(mass), ROOT.RooFit.Import(ztt_th1, False))

					# Create PDF for ztt
					ztt_pdf = ROOT.RooHistPdf(ztt_th1.GetName()+'_pdf', ztt_th1.GetName(), ROOT.RooArgSet(mass), ztt_rdh)
					ztt_norm = ROOT.RooRealVar(ztt_th1.GetName()+'_norm', ztt_th1.GetName(), ztt_th1.Integral(), ztt_th1.Integral()/2., ztt_th1.Integral()*2.)

					# Create RooArgLists for the resulting PDF
					ztt_pdf_list = ROOT.RooArgList()
					ztt_norm_list = ROOT.RooArgList()
					ztt_pdf_list.add(ztt_pdf)
					ztt_norm_list.add(ztt_norm)

					for bkg_pdf in bkg_pdfs:
						bkg_pdf.Print()
						ztt_pdf_list.add(bkg_pdf)

					for bkg_norm in bkg_norms:
						ztt_norm_list.add(bkg_norm)

					# Create resulting ztt PDF
					res_pdf = ROOT.RooAddPdf('pdf', 'pdf', ztt_pdf_list, ztt_norm_list)

					# Do the fit
					res = res_pdf.fitTo(data_rdh, ROOT.RooFit.Extended(), ROOT.RooFit.Save(), ROOT.RooFit.Minimizer('Minuit2', 'migrad'))
					nll_list.append(res.minNll())

				#find minimum to set min to zero
				for index, (nll) in enumerate(nll_list):
					print nll
					if index == 0:
						min_nll = nll_list[0]
						min_shift = es_shifts[0]
					if min_nll > nll_list[index]:
						min_nll = nll_list[index]
						min_shift = es_shifts[index]

				print "found minimum at: (", min_shift, ",", min_nll, ")"

				#fill delta nll list
				for index, (nll) in enumerate(nll_list):
					dnll_list.append(2*(nll-min_nll))

				#Graph
				RooFitGraph = ROOT.TGraphErrors(
					len(es_shifts),
					array.array("d", es_shifts_float), array.array("d", dnll_list)
				)

				plotData.plotdict.setdefault("root_objects", {})[res_hist_nick] = RooFitGraph

				plotData.plotdict["root_objects"][res_hist_nick].SetName(res_hist_nick)
				plotData.plotdict["root_objects"][res_hist_nick].SetTitle("")

				#Fit function
				fitf = ROOT.TF1("f1","[0] + [1]*(x-[2])*(x-[2])",min(es_shifts_float),max(es_shifts_float))
				fitf.FixParameter(0,0)
				fitf.SetParLimits(2,min(es_shifts_float),max(es_shifts_float))
				resultfit = RooFitGraph.Fit("f1","R")
				minimum_of_fit = fitf.GetMinimumX(min(es_shifts_float),max(es_shifts_float))

				#calculate sigmas
				sigma1 = abs(fitf.GetX(1) - minimum_of_fit)
				sigma2 = abs(fitf.GetX(4) - minimum_of_fit)

				#get minimum
				print "Minimum of fitfunction at: ", minimum_of_fit, " +- ", sigma1
				print "2 sigma: ", sigma2

				best_shifts.append(minimum_of_fit)
				errors_1sigma.append(sigma1)
				errors_2sigma.append(sigma2)

			#create plot for pt binning
			ptBins = [20.0,30.0,45.0,60.0]
			ptBinsHist = ROOT.TH1F(res_hist_nick,"",3,array.array("d",ptBins))

			for index, (best_shift,error_1sigma) in enumerate(zip(best_shifts,errors_1sigma)):
				ptBinsHist.SetBinContent(index+1,best_shift)
				ptBinsHist.SetBinError(index+1,error_1sigma)
				print best_shift, " +- ", error_1sigma

			plotData.plotdict.setdefault("root_objects", {})[res_hist_nick] = ptBinsHist

		elif plotData.plotdict["fit_method"] == "chi2":
			print "Start Chi2 fit ..."

			es_shifts=[]
			chi2res=[]

			for index, (data_nick, ztt_nick, es_shift) in enumerate(zip(
					*[plotData.plotdict[k] for k in ["data_nicks","ztt_nicks","es_shifts"]]
			)):
				#print "chi2test between ", data_nick, " and ", ztt_nick
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

			#Graph
			Chi2Graph = ROOT.TGraphErrors(
					len(es_shifts),
					array.array("d", es_shifts), array.array("d", chi2res),
					array.array("d",[0.001]*len(es_shifts)),array.array("d",[20.0]*len(chi2res))
			)
			plotData.plotdict.setdefault("root_objects", {})[plotData.plotdict["res_hist_nick"]] = Chi2Graph

			plotData.plotdict["root_objects"][plotData.plotdict["res_hist_nick"]].SetName(plotData.plotdict["res_hist_nick"])
			plotData.plotdict["root_objects"][plotData.plotdict["res_hist_nick"]].SetTitle("")

			#Fit function
			fit2chi = ROOT.TF1("f1","[0] + [1]*(x-[2])*(x-[2])",plotData.plotdict["fit_min"],plotData.plotdict["fit_max"])
			fit2chi.SetParLimits(0,0,1000000)
			fit2chi.SetParLimits(1,0,1000000)
			fit2chi.SetParLimits(2,min(es_shifts),max(es_shifts))
			Chi2Graph.Fit("f1","R")

			#get minimum
			print "Minimum of fitfunction at: ", fit2chi.GetMinimumX(min(es_shifts),max(es_shifts))
