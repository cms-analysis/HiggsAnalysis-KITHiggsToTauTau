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

class ComputePullValues(analysisbase.AnalysisBase):
	"""Compares pre-fit and post-fit nuisance parameters from a MaxLikelihood fit."""
	# largely based on https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit/blob/slc6-root5.34.17/test/diffNuisances.py

	def __init__(self):
		super(ComputePullValues, self).__init__()

	def modify_argument_parser(self, parser, args):
		super(ComputePullValues, self).modify_argument_parser(parser, args)

		self.pullvalues_options = parser.add_argument_group("Pull values calculation options")
		self.pullvalues_options.add_argument("--fit-poi", nargs=1,
				help="Fit parameter of interest (POI).")
		self.pullvalues_options.add_argument("--fit-s-nick", nargs=1,
				default=["fit_s"],
				help="Nick fit results (S+B hypothesis). [Default: %(default)s]")
		self.pullvalues_options.add_argument("--fit-b-nick", nargs=1,
				default=["fit_b"],
				help="Nick fit results (B-only hypothesis). [Default: %(default)s]")
		self.pullvalues_options.add_argument("--nuisances_prefit-nick", nargs="1",
				default=["nuisances_prefit"],
				help="Nick prefit of uncertainties parameters. [Default: %(default)s]")
		self.pullvalues_options.add_argument("--result-nicks", nargs="+",
				default=["gr_prefit", "graph_s", "graph_b"],
				help="Nick results. [Default: %(default)s]")
		
	def prepare_args(self, parser, plotData):
		super(ComputePullValues, self).prepare_args(parser, plotData)

		self._plotdict_keys = ["fit_s_nick", "fit_b_nick", "nuisances_prefit_nick"]
		self.prepare_list_args(plotData, self._plotdict_keys)

		for fit_s, fit_b, prefit in zip(*[plotData.plotdict[key] for key in self._plotdict_keys]):
			assert isinstance(plotData.plotdict["root_objects"].get(fit_s), ROOT.RooFitResult)
			assert isinstance(plotData.plotdict["root_objects"].get(fit_b), ROOT.RooFitResult)
			assert isinstance(plotData.plotdict["root_objects"].get(prefit), ROOT.RooArgSet)
			plotData.plotdict['nicks_blacklist'].append(fit_s)
			plotData.plotdict['nicks_blacklist'].append(fit_b)
			plotData.plotdict['nicks_blacklist'].append(prefit)

		for nick in plotData.plotdict["result_nicks"]:
			if not nick in plotData.plotdict["nicks"]:
				plotData.plotdict["nicks"].append(nick)

		if plotData.plotdict["y_tick_labels"] is None:
			plotData.plotdict["y_tick_labels"] = []

	def run(self, plotData=None):
		super(ComputePullValues, self).run(plotData)

		for fit_s, fit_b, prefit in zip(*[plotData.plotdict[key] for key in self._plotdict_keys]):

			# get the fitted parameters
			fpf_s = plotData.plotdict["root_objects"].get(fit_s).floatParsFinal()
			fpf_b = plotData.plotdict["root_objects"].get(fit_b).floatParsFinal()

			pulls = []
			nuis_p_i = 0

			hist_fit_b  = ROOT.TH1F("prefit_fit_b"   ,"B-only fit Nuisances;;#theta ",plotData.plotdict["root_objects"].get(prefit).getSize(),0,plotData.plotdict["root_objects"].get(prefit).getSize())
			hist_fit_s  = ROOT.TH1F("prefit_fit_s"   ,"S+B fit Nuisances   ;;#theta ",plotData.plotdict["root_objects"].get(prefit).getSize(),0,plotData.plotdict["root_objects"].get(prefit).getSize())
			hist_prefit = ROOT.TH1F("prefit_nuisancs","Prefit Nuisances    ;;#theta ",plotData.plotdict["root_objects"].get(prefit).getSize(),0,plotData.plotdict["root_objects"].get(prefit).getSize())

			isFlagged = {}
			table = {}

			# loop over all fitted parameters
			for i in range(fpf_s.getSize()):

				nuis_s = fpf_s.at(i)
				name   = nuis_s.GetName()
				nuis_b = fpf_b.find(name)
				nuis_p = plotData.plotdict["root_objects"].get(prefit).find(name)

				row = []
				mean_p, sigma_p = 0,0

				if nuis_p == None:
        				# nuisance parameter NOT present in the prefit result
					row += [ "[%.2f, %.2f]" % (nuis_s.getMin(), nuis_s.getMax()) ]

				else:
					# get best-fit value and uncertainty at prefit for this 
					# nuisance parameter
					mean_p, sigma_p = (nuis_p.getVal(), nuis_p.getError())

					if not sigma_p > 0:
						sigma_p = (nuis_p.getMax() - nuis_p.getMin())/2
					row += [ "%.6f +/- %.6f" % (nuis_p.getVal(), nuis_p.getError()) ]

				for fit_name, nuis_x in [('b', nuis_b), ('s',nuis_s)]:
					if nuis_x == None:
						row += [ " n/a " ]
					else:
						row += [ "%+.2f +/- %.2f" % (nuis_x.getVal(), nuis_x.getError()) ]

						if nuis_p != None:
							if fit_name == 'b':
								nuis_p_i += 1
								hist_fit_b.SetBinContent(nuis_p_i,nuis_x.getVal())
								hist_fit_b.SetBinError(nuis_p_i,nuis_x.getError())
								plotData.plotdict["y_tick_labels"].append(name)
							if fit_name == 's':
								hist_fit_s.SetBinContent(nuis_p_i,nuis_x.getVal())
								hist_fit_s.SetBinError(nuis_p_i,nuis_x.getError())
							hist_prefit.SetBinContent(nuis_p_i,mean_p)
							hist_prefit.SetBinError(nuis_p_i,sigma_p)

							if sigma_p>0:
								# difference of the nuisance parameter
								# w.r.t to the prefit value in terms of the uncertainty
								valShift = (nuis_x.getVal() - mean_p)/sigma_p

								# ratio of the nuisance parameter's uncertainty
								# w.r.t the prefit uncertainty
								sigShift = nuis_x.getError()/sigma_p
							else :
								log.debug("No definition for prefit uncertainty %s. Printing absolute shifts"%(nuis_p.GetName()))
								valShift = (nuis_x.getVal() - mean_p)
								sigShift = nuis_x.getError()

							if fit_name == 'b':
								pulls.append(valShift)
							row[-1] += " (%+4.2fsig, %4.2f)" % (valShift, sigShift)

							if (abs(valShift) > 2.0 or abs(sigShift-1) > 0.5):
								isFlagged[(name,fit_name)] = 2

							elif (abs(valShift) > 0.3  or abs(sigShift-1) > 0.1):
								isFlagged[(name,fit_name)] = 1

				row += [ "%+4.2f"  % plotData.plotdict["root_objects"].get(fit_s).correlation(name, plotData.plotdict["fit_poi"][0])]
				table[name] = row

			highlight = "*%s*"
			morelight = "!%s!"
			pmsub, sigsub = None, None
        		fmtstring = "%-40s     %15s    %30s    %30s  %10s"
			log.debug(fmtstring % ('name', 'pre fit', 'b-only fit', 's+b fit', 'rho'))
			names = table.keys()
			names.sort()
			highlighters = { 1:highlight, 2:morelight }
			for n in names:
				v = table[n]
				if pmsub  != None: v = [ re.sub(pmsub[0],  pmsub[1],  i) for i in v ]
				if sigsub != None: v = [ re.sub(sigsub[0], sigsub[1], i) for i in v ]
				if (n,'b') in isFlagged: v[-3] = highlighters[isFlagged[(n,'b')]] % v[-3]
				if (n,'s') in isFlagged: v[-2] = highlighters[isFlagged[(n,'s')]] % v[-2]
				log.debug(fmtstring % (n, v[0], v[1], v[2], v[3]))

			# produce graphs
			gr_fit_s = self.getGraph(hist_fit_s, 0.0)
			gr_fit_b = self.getGraph(hist_fit_b, 0.0)
			gr_prefit = self.getGraph(hist_prefit, 0.5)
			
			plotData.plotdict['root_objects'][plotData.plotdict["result_nicks"][0]] = gr_prefit
			plotData.plotdict['root_objects'][plotData.plotdict["result_nicks"][1]] = gr_fit_s
			plotData.plotdict['root_objects'][plotData.plotdict["result_nicks"][2]] = gr_fit_b

			plotData.plotdict['root_objects'].pop(fit_s)
			plotData.plotdict['root_objects'].pop(fit_b)
			plotData.plotdict['root_objects'].pop(prefit)

			if plotData.plotdict['y_lims'] is None:
				plotData.plotdict['y_lims'] = [0, hist_prefit.GetNbinsX()]
			plotData.plotdict['y_label'] = None

	def getGraph(self, hist, shift):
		gr = ROOT.TGraphErrors()
		gr.SetName(hist.GetName())

		for i in range(hist.GetNbinsX()):
			x = hist.GetBinContent(i+1)
			y = hist.GetBinCenter(i+1)
			e = hist.GetBinError(i+1)
			
			gr.SetPoint(i,x,y)
			gr.SetPointError(i,e,shift)

		return gr
