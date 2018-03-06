# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import ROOT
import hashlib

import Artus.HarryPlotter.analysisbase as analysisbase

class UnrollTwoDHistogram(analysisbase.AnalysisBase):
	"""Convert two dimensional histogram into concatenation of one dimensional histograms"""
	
	def __init__(self):
		super(UnrollTwoDHistogram, self).__init__()
	
	def modify_argument_parser(self, parser, args):
		super(UnrollTwoDHistogram, self).modify_argument_parser(parser, args)
		
		self.unroll_twod_histogram_options = parser.add_argument_group("UnrollTwoDHistogram options")
		self.unroll_twod_histogram_options.add_argument("--two-d-input-nicks", nargs="+", default=[""],
				help="Nick names of two dimensional input histograms. [Default: %(default)s]")
		self.unroll_twod_histogram_options.add_argument("--unroll-along-y", action="store_true", default=False,
				help="Unroll histogram along y instead of x axis. [Default: %(default)s]")
		self.unroll_twod_histogram_options.add_argument("--unrolled-hist-nicks", nargs="+", default=[""],
				help="Nick names of resulting one dimensional histograms. [Default: %(default)s]")
		
	def prepare_args(self, parser, plotData):
		super(UnrollTwoDHistogram, self).prepare_args(parser, plotData)
		self._plotdict_keys = ["two_d_input_nicks", "unrolled_hist_nicks"]
		self.prepare_list_args(plotData, self._plotdict_keys)
		
		for two_d_input_nick, unrolled_hist_nick in zip(*[plotData.plotdict[key] for key in self._plotdict_keys]):
			if (two_d_input_nick != unrolled_hist_nick) and (not unrolled_hist_nick in plotData.plotdict["nicks"]):
				plotData.plotdict["nicks"].insert(
					plotData.plotdict["nicks"].index(two_d_input_nick),
					unrolled_hist_nick
				)
	
	def run(self, plotData=None):
		super(UnrollTwoDHistogram, self).run(plotData)
		
		for two_d_input_nick, unrolled_hist_nick in zip(*[plotData.plotdict[key] for key in self._plotdict_keys]):
			
			two_d_histogram = plotData.plotdict["root_objects"][two_d_input_nick]
			input_number_bins_x = two_d_histogram.GetNbinsX()
			input_number_bins_y = two_d_histogram.GetNbinsY()
			result_number_of_bins = input_number_bins_x * input_number_bins_y
			
			unrolled_histogram = ROOT.TH1D("histogram_" + hashlib.md5("_".join([two_d_input_nick, unrolled_hist_nick])).hexdigest(), "",
			                              result_number_of_bins, 0, result_number_of_bins)
			
			if plotData.plotdict["unroll_along_y"]:
				bin_y = 1
				for x in range(1,input_number_bins_x+1):
					for y in range(1,input_number_bins_y+1):
						unrolled_histogram.SetBinContent(bin_y, two_d_histogram.GetBinContent(x,y))
						unrolled_histogram.SetBinError(bin_y, two_d_histogram.GetBinError(x,y))
						bin_y += 1
			else:
				bin_x = 1
				for y in range(1,input_number_bins_y+1):
					for x in range(1,input_number_bins_x+1):
						unrolled_histogram.SetBinContent(bin_x, two_d_histogram.GetBinContent(x,y))
						unrolled_histogram.SetBinError(bin_x, two_d_histogram.GetBinError(x,y))
						bin_x += 1
			
			unrolled_histogram.SetEntries(two_d_histogram.GetEntries())
			#import array
			#print two_d_histogram.GetEntries(), two_d_histogram.GetEffectiveEntries(), array.array("d", two_d_histogram.GetSumw2())
			#print unrolled_histogram.GetEntries(), unrolled_histogram.GetEffectiveEntries(), array.array("d", unrolled_histogram.GetSumw2())
			
			plotData.plotdict.setdefault("root_objects", {})[unrolled_hist_nick] = unrolled_histogram

