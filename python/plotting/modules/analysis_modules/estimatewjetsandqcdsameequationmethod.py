# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import ROOT

import HiggsAnalysis.KITHiggsToTauTau.plotting.modules.analysis_modules.estimatebase as estimatebase
import HiggsAnalysis.KITHiggsToTauTau.tools as tools
import HiggsAnalysis.KITHiggsToTauTau.uncertainties.uncertainties as uncertainties


class EstimateWjetsAndQCDPrefit(estimatebase.EstimateBase):
	""" This modules estimates W+jets and QCD backgrounds using the same-equation method."""
	def __init__(self):
		super(EstimateWjetsAndQCDPrefit, self).__init__()

	def modify_argument_parser(self, parser, args):
		super(EstimateWjetsAndQCDPrefit, self).modify_argument_parser(parser, args)
		
		self.estimate_wjets_and_qcd_prefit_options = parser.add_argument_group("WJets and QCD estimation options")
		
		# Step 1
		self.estimate_wjets_and_qcd_prefit_options.add_argument("--wjets-ss-mc-nicks", nargs="+", default=[""],
				help="Nicks for inclusive (No mT cut applied) ss mc histogram. [Default: %(default)s]")
		self.estimate_wjets_and_qcd_prefit_options.add_argument("--wjets-os-mc-nicks", nargs="+", default=[""],
				help="Nicks for inclusive (No mT cut applied) os mc histogram. [Default: %(default)s]")	
		# Step 2		
		self.estimate_wjets_and_qcd_prefit_options.add_argument("--wjets-os-highmt-mc-nicks", nargs="+", default=[""],
				help="Nicks for highmt os W+jets mc histogram. [Default: %(default)s]")
		self.estimate_wjets_and_qcd_prefit_options.add_argument("--wjets-os-lowmt-mc-nicks", nargs="+", default=[""],
				help="Nicks for lowmt os W+jets mc histogram. [Default: %(default)s]")
		# Step 3		
		self.estimate_wjets_and_qcd_prefit_options.add_argument("--wjets-ss-highmt-mc-nicks", nargs="+", default=[""],
				help="Nicks for highmt ss W+jets mc histogram. [Default: %(default)s]")
		self.estimate_wjets_and_qcd_prefit_options.add_argument("--wjets-ss-lowmt-mc-nicks", nargs="+", default=[""],
				help="Nicks for lowmt ss W+jets mc histogram. [Default: %(default)s]")
		# Step 4
		self.estimate_wjets_and_qcd_prefit_options.add_argument("--qcd-extrapolation-factors-ss-os", nargs="+", type=float, default=[1.00],
				help="Extrapolation factors of QCD OS/SS yields. [Default: %(default)s]")		
		# Step 5 
		self.estimate_wjets_and_qcd_prefit_options.add_argument("--wjets-ss-highmt-data-nicks", nargs="+", default=[""],
				help="Nicks for ss highmt data histogram. [Default: %(default)s]")				
		self.estimate_wjets_and_qcd_prefit_options.add_argument("--wjets-ss-highmt-substract-nicks", nargs="+",
				default=[""],
				help="Nicks for ss control region histogram to substract from data to get the W+jets yield (whitespace separated). [Default: %(default)s]")
		self.estimate_wjets_and_qcd_prefit_options.add_argument("--wjets-os-highmt-data-nicks", nargs="+", default=[""],
				help="Nicks for ss highmt data histogram. [Default: %(default)s]")				
		self.estimate_wjets_and_qcd_prefit_options.add_argument("--wjets-os-highmt-substract-nicks", nargs="+",
				default=[""],
				help="Nicks for ss control region histogram to substract from data to get the W+jets yield (whitespace separated). [Default: %(default)s]")
		self.estimate_wjets_and_qcd_prefit_options.add_argument("--wjets-ss-highmt-shape-nicks", nargs="+", default=[""],
				help="Nicks for histogram to plot. [Default: %(default)s]")
		# Step 6
		self.estimate_wjets_and_qcd_prefit_options.add_argument("--wjets-os-lowmt-shape-nicks", nargs="+", default=[""],
				help="Nicks for histogram to plot. [Default: %(default)s]")	
		self.estimate_wjets_and_qcd_prefit_options.add_argument("--wjets-ss-lowmt-shape-nicks", nargs="+", default=[""],
				help="Nicks for histogram to plot. [Default: %(default)s]")						
		# Step 7
		self.estimate_wjets_and_qcd_prefit_options.add_argument("--qcd-ss-data-nicks", nargs="+", default=[""],
				help="Nicks for ss highmt data histogram. [Default: %(default)s]")			
		self.estimate_wjets_and_qcd_prefit_options.add_argument("--qcd-ss-lowmt-subtract-nicks", nargs="+", default=[""],
				help="Nicks for histogram to plot. [Default: %(default)s]")					
		self.estimate_wjets_and_qcd_prefit_options.add_argument("--qcd-ss-lowmt-shape-nicks", nargs="+", default=[""],
				help="Nicks for histogram to plot. [Default: %(default)s]")	


				
		self.estimate_wjets_and_qcd_prefit_options.add_argument("--qcd-shape-nicks", nargs="+", default=[""],
				help="Nicks for histogram to plot. [Default: %(default)s]")
		self.estimate_wjets_and_qcd_prefit_options.add_argument("--qcd-yield-nicks", nargs="+", default=[""],
				help="Nicks for histogram to plot. [Default: %(default)s]")

		self.estimate_wjets_and_qcd_prefit_options.add_argument("--qcd-ss-highmt-shape-nicks", nargs="+", default=[""],
				help="Nicks for histogram to plot. [Default: %(default)s]")
		self.estimate_wjets_and_qcd_prefit_options.add_argument("--qcd-os-highmt-nicks", nargs="+", default=[""],
				help="Nicks for histogram to plot. [Default: %(default)s]")
		self.estimate_wjets_and_qcd_prefit_options.add_argument("--qcd-shape-highmt-substract-nicks", nargs="+",
				default=[""],
				help="Nicks for control region histogram to substract from data  to get the QCD yield (whitespace separated). [Default: %(default)s]")
		self.estimate_wjets_and_qcd_prefit_options.add_argument("--qcd-yield-substract-nicks", nargs="+",
				default=[""],
				help="Nicks for control region histogram to substract from data  to get the QCD yield (whitespace separated). [Default: %(default)s]")
		self.estimate_wjets_and_qcd_prefit_options.add_argument("--qcd-shape-substract-nicks", nargs="+",
				default=[""],
				help="Nicks for control region histogram to substract from data to get the QCD shape (whitespace separated). [Default: %(default)s]")
		self.estimate_wjets_and_qcd_prefit_options.add_argument("--wjets-os-substract-nicks", nargs="+",
				default=[""],
				help="Nicks for os control region histogram to substract from data to get the W+jets yield (whitespace separated). [Default: %(default)s]")

		self.estimate_wjets_and_qcd_prefit_options.add_argument("--wjets-os-data-nicks", nargs="+", default=[""],
				help="Nicks for os highmt data histogram. [Default: %(default)s]")
			
		self.estimate_wjets_and_qcd_prefit_options.add_argument("--wjets-shape-nicks", nargs="+", default=[""],
				help="Nicks for W+jets signal region histogram. [Default: %(default)s]")
		self.estimate_wjets_and_qcd_prefit_options.add_argument("--wjets-wj-final-selection", nargs="+", default=[""],
				help="Nicks for W+jets in final category. [Default: %(default)s]")
		self.estimate_wjets_and_qcd_prefit_options.add_argument("--wjets-relaxed-os-highmt-nicks", nargs="+", default=[""],
				help="Nicks for os highmt W+jets histogram with relaxed selection. [Default: %(default)s]")
		self.estimate_wjets_and_qcd_prefit_options.add_argument("--wjets-relaxed-os-lowmt-nicks", nargs="+", default=[""],
				help="Nicks for os lowmt W+jets histogram with relaxed selection. [Default: %(default)s]")
		self.estimate_wjets_and_qcd_prefit_options.add_argument("--wjets-scale-factor-shifts", nargs="+", type=float, default=[1.0],
				help="Determine by how much the W+jets scale factor should be shifted for the QCD estimation in the low mt region. [Default: %(default)s]")

	def prepare_args(self, parser, plotData):
		super(EstimateWjetsAndQCDPrefit, self).prepare_args(parser, plotData)
		self._plotdict_keys = ["qcd_extrapolation_factors_ss_os", "qcd_shape_nicks", "qcd_ss_lowmt_nicks", "qcd_ss_highmt_shape_nicks", "qcd_os_highmt_nicks", "qcd_shape_highmt_substract_nicks", "qcd_yield_nicks", "qcd_shape_substract_nicks", "qcd_yield_substract_nicks", "wjets_os_highmt_mc_nicks", "wjets_ss_highmt_mc_nicks", "wjets_ss_substract_nicks", "wjets_ss_data_nicks", "wjets_ss_mc_nicks", "wjets_os_substract_nicks", "wjets_os_data_nicks", "wjets_os_mc_nicks", 
		"wjets_shape_nicks","wjets_relaxed_os_highmt_nicks", "wjets_relaxed_os_lowmt_nicks", "wjets_scale_factor_shifts"]
		self.prepare_list_args(plotData, self._plotdict_keys)
		for index in ["qcd_shape_substract_nicks", "qcd_yield_substract_nicks", "wjets_ss_substract_nicks", "wjets_os_substract_nicks","qcd_shape_highmt_substract_nicks"]:
			plotData.plotdict[index] = [nicks.split() for nicks in plotData.plotdict[index]]
		
		# do not check because it's allowed to be None
		self._plotdict_keys.append("wjets_wj_final_selection")

	def run(self, plotData=None):
		super(EstimateWjetsAndQCDPrefit, self).run(plotData)
		
		# make sure that all necessary histograms are available
		for nicks in zip(*[plotData.plotdict[key] for key in self._plotdict_keys[:-1]]):
			for nick in nicks:
				if isinstance(nick, basestring):
					assert isinstance(plotData.plotdict["root_objects"].get(nick), ROOT.TH1)
				elif (not isinstance(nick, float) and not isinstance(nick, bool)):
					for subnick in nick:
						assert isinstance(plotData.plotdict["root_objects"].get(subnick), ROOT.TH1)

		for qcd_extrapolation_factor_ss_os, qcd_shape_nick, qcd_ss_lowmt_nick, qcd_ss_highmt_shape_nick, qcd_os_highmt_nick, qcd_shape_highmt_substract_nick, qcd_yield_nick, qcd_shape_substract_nick, qcd_yield_substract_nick, wjets_os_highmt_mc_nick, wjets_ss_highmt_mc_nick, wjets_ss_substract_nick, wjets_ss_data_nick, wjets_os_substract_nick, wjets_os_data_nick, wjets_shape_nick, wjets_relaxed_os_highmt_nick, wjets_relaxed_os_lowmt_nick, wjets_scale_factor_shift, wjets_final_selection in 
		zip(*[plotData.plotdict[key] for key in self._plotdict_keys]):
			########################################
			# ------------ Step 1 ------------------
			# Measure W OS/SS factor from MonteCarlo
			# 1. Needs inclusive wj_mc for OS and SS 
			# 2. Therefore the scale factor is the same in the high mt control region (mT>70) and the low mt signal like region.
			
			yield_wj_mc_os = tools.PoissonYield(plotData.plotdict["root_objects"][wjets_from_mc_os_nicks])()
			yield_wj_mc_ss = tools.PoissonYield(plotData.plotdict["root_objects"][wjets_from_mc_ss_nicks])()
			
			# correct negative yields
			yield_wj_mc_os = uncertainties.ufloat(max(0.0, yield_wj_mc_os.nominal_value), yield_wj_mc_os.std_dev)
			yield_wj_mc_ss = uncertainties.ufloat(max(0.0, yield_wj_mc_ss.nominal_value), yield_wj_mc_ss.std_dev)
			
			assert (yield_wj_mc_os != 0.0) or (yield_wj_mc_ss != 0.0), "Yield of MC in opposite-sign or same-sign region is zero."
			
			# calculate w_os_ss factor and store it in the metadata
			w_os_ss_extrapolation_factor = yield_wj_mc_os / yield_wj_mc_ss
	
			plotData.metadata[wjets_from_mc_os_nicks] = {
				"w_os_ss_factor" : w_os_ss_extrapolation_factor.nominal_value,
				"w_os_ss_factor_unc" : w_os_ss_extrapolation_factor.std_dev,
				"w_os_ss_factor_unc_rel" : abs(w_os_ss_extrapolation_factor.std_dev/w_os_ss_extrapolation_factor.nominal_value if w_os_ss_extrapolation_factor.nominal_value != 0.0 else 0.0),
			}
			plotData.metadata
			
			########################################
			# ------------ Step 2 ------------------
			# Measure opposite-sign extrapolation factor from high Mt Control region (mT>70) to low Mt (mt<50)
			# 1. Needs wj_mc in opposite region for both mT regions.
			
			yield_wj_mc_os_highmt = tools.PoissonYield(plotData.plotdict["root_objects"][wjets_os_highmt_mc_nick])()
			yield_wj_mc_os_lowmt = tools.PoissonYield(plotData.plotdict["root_objects"][wjets_os_lowmt_mc_nick])()
			
			assert (yield_wj_mc_os_highmt != 0.0) or (yield_wj_mc_os_lowmt != 0.0), "Yield of MC in opposite-sign lowmt or opposite-sign highmt region is zero."
			
			# calculate w_highmt_lowmt factor and store it in the metadata
			w_os_highmt_lowmt_extrapolation_factor = yield_wj_mc_os_lowmt/yield_wj_mc_os_highmt
			
			plotData.metadata[wjets_from_mc_os_nicks] = {
				"w_os_highmt_lowmt_factor" : w_os_highmt_lowmt_extrapolation_factor.nominal_value,
				"w_os_highmt_lowmt_factor_unc" : w_os_highmt_lowmt_extrapolation_factor.std_dev,
				"w_os_highmt_lowmt_factor_unc_rel" : abs(w_os_highmt_lowmt_extrapolation_factor.std_dev/w_os_highmt_lowmt_extrapolation_factor.nominal_value if w_os_highmt_lowmt_extrapolation_factor.nominal_value != 0.0 else 0.0),
			}
			plotData.metadata
			
			########################################
			# ------------ Step 3 ------------------
			# Measure same-sign extrapolation factor from high Mt Control region (mT>70) to low Mt (mt<50)
			# This is needed to get the first estimate for Qcd in the same-sign region.
			# 1. Needs wj_mc in opposite region for both mT regions.

						
			# calculate w_highmt_lowmt factor and store it in the metadata
			if tools.PoissonYield(plotData.plotdict["root_objects"][wjets_ss_highmt_mc_nick])() != 0.0:
				w_ss_highmt_lowmt_extrapolation_factor = tools.PoissonYield(plotData.plotdict["root_objects"][wjets_ss_lowmt_mc_nick])()/tools.PoissonYield(plotData.plotdict["root_objects"][wjets_ss_highmt_mc_nick])()
			else: 
				log.warning("W+jets & QCD estimation: W+jets high mT region in MC has no entries. High->low mT extrapolation factor is set to 1.0!")
				w_ss_highmt_lowmt_extrapolation_factor = 1.0
			
			plotData.metadata[wjets_from_mc_os_nicks] = {
				"w_ss_highmt_lowmt_factor" : w_ss_highmt_lowmt_extrapolation_factor.nominal_value,
				"w_ss_highmt_lowmt_factor_unc" : w_ss_highmt_lowmt_extrapolation_factor.std_dev,
				"w_ss_highmt_lowmt_factor_unc_rel" : abs(w_ss_highmt_lowmt_extrapolation_factor.std_dev/w_ss_highmt_lowmt_extrapolation_factor.nominal_value if w_ss_highmt_lowmt_extrapolation_factor.nominal_value != 0.0 else 0.0),
			}
			plotData.metadata	
			
			########################################		
			# ------------ Step 4 ------------------
			# Estimate same-sign lowMt QCD with inverted isolation 
			# 1. Get the QCD OS/SS extrapolation factor which is measured using the makePlots_datacardsQCDfactors script. 
			
			# qcd_extrapolation_factor_ss_os
						
			########################################
			# ------------ Step 5 ------------------
			# Estimate highmt same-sign W+jets yield 
			# 1. Get data yield in same-sign highmt region	
			# 2. Subtract all MC backgrounds from same-sign highmt region from it. 
			# 3. Scale it by the qcd_ss_os_extrapolation_factor
			# 4. Get data yield in opposite sign high mt region
			# 5. Subtract all MC backgrounds from opposite-sign highmt region from it.
			# 6. Subtract the estimate for the yield for same-sign highmt from it.
			# 7. Scale it by the differene between the W+jets and QCD extrapolation factor.
			# 8. Scale the sahpe according to the scale factor.
					
			yield_wjets_ss_highmt = tools.PoissonYield(plotData.plotdict["root_objects"][wjets_ss_highmt_data_nick])()	
			for nick in wjets_ss_substract_nicks:
				yield_wjets_ss_highmt -= tools.PoissonYield(plotData.plotdict["root_objects"][nick])()
				
			yield_wjets_os_highmt = tools.PoissonYield(plotData.plotdict["root_objects"][wjets_os_highmt_data_nick])()
			for nick in wjets_os_substract_nicks:
				yield_wjets_os_highmt -= tools.PoissonYield(plotData.plotdict["root_objects"][nick])()
							
			yield_wjets_ss_highmt = yield_wjets_os_highmt - qcd_extrapolation_factor_ss_os * yield_wjets_ss_highmt
			
			yield_wjets_ss_highmt = yield_wjets_ss_highmt / (w_os_ss_extrapolation_factor - qcd_extrapolation_factor_ss_os)
			yield_wjets_ss_highmt = uncertainties.ufloat(max(0.0, yield_wjets_ss_highmt.nominal_value), yield_wjets_ss_highmt.std_dev)
			
			assert (yield_wjets_ss_highmt.nominal_value != 0.0), log.warning("W+jets & QCD estimation: data yield in high mT same-sign region after background subtraction is 0!")	
			
			# scale same-sign highmt Wjets histograms for controlplots.
			integral_shape = tools.PoissonYield(plotData.plotdict["root_objects"][wjets_ss_highmt_shape_nick])()
			if integral_shape != 0.0:
				scale_factor = yield_wjets_ss_highmt / integral_shape
				log.debug("Scale factor for process W+jets (nick \"{nick}\") is {scale_factor}.".format(nick=wjets_ss_shape_nick, scale_factor=scale_factor))
				plotData.plotdict["root_objects"][wjets_ss_highmt_shape_nick].Scale(scale_factor.nominal_value)			
			
			########################################
			# ------------ Step 6 a ------------------
			# Estimate final opposite-sign  lowmT W+jets yield 
			# 1. Multiply yield from before the Wjets OS/SS and the low-highmt factor.
			# 2. Scale the shape nicks by the resulting scale factor. 
			
			final_yield_wjets_os_lowmt = w_os_highmt_lowmt_extrapolation_factor * w_os_ss_extrapolation_factor * yield_wjets_ss_highmt

			assert (final_yield_wjets_os_lowmt.nominal_value != 0.0), log.warning("W+jets estimation: Final yield in low mT opposite-sign is 0!")	
			
			# scale same-sign highmt Wjets histograms for controlplots.
			integral_shape = tools.PoissonYield(plotData.plotdict["root_objects"][wjets_os_lowmt_shape_nick])()
			if integral_shape != 0.0:
				scale_factor =final_yield_wjets_os_lowmt / integral_shape
				log.debug("Scale factor for process W+jets (nick \"{nick}\") is {scale_factor}.".format(nick=wjets_ss_shape_nick, scale_factor=scale_factor))
				plotData.plotdict["root_objects"][wjets_os_lowmt_shape_nick].Scale(scale_factor.nominal_value)	
			
			########################################
			# ------------ Step 6 b ------------------
			# Estimate final same-sign  lowmT W+jets yield 
			# 1. Multiply yield from before the Wjets OS/SS and the low-highmt factor.
			# 2. Scale the shape nicks by the resulting scale factor. 				
			
			final_yield_wjets_ss_lowmt = w_ss_highmt_lowmt_extrapolation_factor * yield_wjets_ss_highmt

			assert (final_yield_wjets_ss_lowmt.nominal_value != 0.0), log.warning("W+jets estimation: Final yield in low mT same-sign is 0!")	
			
			# scale same-sign highmt Wjets histograms for controlplots.
			integral_shape = tools.PoissonYield(plotData.plotdict["root_objects"][wjets_ss_lowmt_shape_nick])()
			if integral_shape != 0.0:
				scale_factor =final_yield_wjets_ss_lowmt / integral_shape
				log.debug("Scale factor for process W+jets (nick \"{nick}\") is {scale_factor}.".format(nick=wjets_ss_shape_nick, scale_factor=scale_factor))
				plotData.plotdict["root_objects"][wjets_ss_lowmt_shape_nick].Scale(scale_factor.nominal_value)	
						
			########################################
			# ------------ Step 7 ------------------
			# Get a opposite-sign region QCD estimate
			# 1. Get same-sign low-mt data yield.
			# 2. Subtract all background except for Wjets from it.
			# 3. Calculate same-sign lowmt Wjets estimate using the highMt estimte from step 5.
			# 4. Subtract also Wjets to get the same-sign QCD yield.
			# 5. Get the shapes for all histograms and background and get a QCD shape estimate

							
			yield_qcd_ss = tools.PoissonYield(plotData.plotdict["root_objects"][qcd_ss_data_nick])()
			for nick in qcd_ss_subtract_nicks:
				yield_qcd_ss -= tools.PoissonYield(plotData.plotdict["root_objects"][nick])()
			
			yield_qcd_ss -= final_yield_wjets_ss_lowmt
			assert (yield_qcd_ss_high.nominal_value != 0.0), log.warning("QCD estimation: yield in low mT same-sign is 0!")	
			
			for nick in qcd_ss_shape_lowmt_subtract_nicks:
				plotData.plotdict["root_objects"][qcd_shape_nick].Add(plotData.plotdict["root_objects"][nick], -1)
			
			plotData.plotdict["root_objects"][qcd_shape_nick].Add(plotData.plotdict["root_objects"][wjets_ss_lowmt_shape_nick], -1)
			plotData.plotdict["root_objects"][qcd_shape_nick].Scale(qcd_os_ss_extrapolation_factor)
			pass	
			
			
			########################################
			# estimate QCD for the highmT region
			
			# get qcd ss high mt shape
			# for nick in qcd_shape_highmt_substract_nick+[wjets_ss_highmt_mc_nick]:
			# 	plotData.plotdict["root_objects"][qcd_ss_highmt_shape_nick].Add(plotData.plotdict["root_objects"][nick], -1)
			# 
			# # get qcd yield in ss high mt region
			# yield_qcd_ss_highmt = tools.PoissonYield(plotData.plotdict["root_objects"][wjets_ss_data_nick])()
			# for nick in wjets_ss_substract_nick+[wjets_ss_highmt_mc_nick]:
			# 	yield_qcd_ss_highmt -= tools.PoissonYield(plotData.plotdict["root_objects"][nick])()
			# yield_qcd_ss_highmt = max(uncertainties.ufloat(0.0, yield_qcd_ss_highmt.std_dev), yield_qcd_ss_highmt)
			# 
			# # scale qcd ss high mt shape by qcd yield found in data
			# integral_shape = tools.PoissonYield(plotData.plotdict["root_objects"][qcd_ss_highmt_shape_nick])()
			# if integral_shape != 0.0:
			# 	scale_factor = yield_qcd_ss_highmt / integral_shape
			# 	plotData.plotdict["root_objects"][qcd_ss_highmt_shape_nick].Scale(scale_factor.nominal_value)
			# 
			# # scale qcd os high mt shape by qcd yield found in ss data and ss->os extrapolation factor
			# integral_shape = tools.PoissonYield(plotData.plotdict["root_objects"][qcd_os_highmt_nick])()
			# if integral_shape != 0.0:
			# 	scale_factor = yield_qcd_ss_highmt * qcd_extrapolation_factor_ss_os / integral_shape
			# 	plotData.plotdict["root_objects"][qcd_os_highmt_nick].Scale(scale_factor.nominal_value)
			# 
			# ########################################
			# # estimate W+jets
			# 
			# # get w+jets yield in os high mt region
			# yield_wjets_os_highmt = tools.PoissonYield(plotData.plotdict["root_objects"][wjets_os_data_nick])()
			# for nick in wjets_os_substract_nick:
			# 	yield_wjets_os_highmt -= tools.PoissonYield(plotData.plotdict["root_objects"][nick])()
			# yield_wjets_os_highmt -= qcd_extrapolation_factor_ss_os*yield_qcd_ss_highmt
			# yield_wjets_os_highmt = uncertainties.ufloat(max(0.0, yield_wjets_os_highmt.nominal_value), yield_wjets_os_highmt.std_dev)
			# if yield_wjets_os_highmt.nominal_value == 0.0:
			# 	log.warning("W+jets & QCD estimation: data yield in high mT region after background subtraction is 0!")
			# 
			# # get high mt -> low mt extrapolation factor from MC
			# if tools.PoissonYield(plotData.plotdict["root_objects"][wjets_relaxed_os_highmt_nick])() != 0.0:
			# 	wjets_extrapolation_factor_mt = tools.PoissonYield(plotData.plotdict["root_objects"][wjets_relaxed_os_lowmt_nick])()/tools.PoissonYield(plotData.plotdict["root_objects"][wjets_relaxed_os_highmt_nick])()
			# else:
			# 	log.warning("W+jets & QCD estimation: W+jets high mT region in MC has no entries. High->low mT extrapolation factor is set to 1.0!")
			# 	wjets_extrapolation_factor_mt = 1.0
			# 
			# # get w+jets yield in low mt region
			# wjets_yield = yield_wjets_os_highmt*wjets_extrapolation_factor_mt
			# 
			# # extrapolate to final selection
			# if wjets_final_selection != None:
			# 	wjets_yield = wjets_yield * tools.PoissonYield(plotData.plotdict["root_objects"][wjets_final_selection])() / tools.PoissonYield(plotData.plotdict["root_objects"][wjets_relaxed_os_lowmt_nick])()
			# 
			# # scale signal region histograms
			# integral_shape = tools.PoissonYield(plotData.plotdict["root_objects"][wjets_shape_nick])()
			# if integral_shape != 0.0:
			# 	scale_factor = wjets_yield / integral_shape
			# 	log.debug("Scale factor for process W+jets (nick \"{nick}\") is {scale_factor}.".format(nick=wjets_shape_nick, scale_factor=scale_factor))
			# 	plotData.plotdict["root_objects"][wjets_shape_nick].Scale(scale_factor.nominal_value)
			# 
			# plotData.metadata[wjets_shape_nick] = {
			# 	"yield" : wjets_yield.nominal_value,
			# 	"yield_unc" : wjets_yield.std_dev,
			# 	"yield_unc_rel" : abs(wjets_yield.std_dev/wjets_yield.nominal_value if wjets_yield.nominal_value != 0.0 else 0.0),
			# }
			# 
			# ########################################
			# # estimate QCD for the lowmT
			# 
			# # define w+jets scale factor for qcd estimation
			# if tools.PoissonYield(plotData.plotdict["root_objects"][wjets_os_highmt_mc_nick])() != 0.0:
			# 	wjets_scale_factor = yield_wjets_os_highmt/tools.PoissonYield(plotData.plotdict["root_objects"][wjets_os_highmt_mc_nick])()
			# else:
			# 	log.warning("W+jets & QCD estimation: W+jets high mT region in MC has no entries. Scale factor for W+jets in QCD estimation is set to 1.0!")
			# 	wjets_scale_factor = uncertainties.ufloat(1.0, 0.0)
			# 
			# for nick in qcd_shape_substract_nick:
			# 	if "wj" in nick:
			# 		scale_factor = wjets_scale_factor * wjets_scale_factor_shift
			# 		plotData.plotdict["root_objects"][nick].Scale(scale_factor.nominal_value)
			# 	plotData.plotdict["root_objects"][qcd_shape_nick].Add(plotData.plotdict["root_objects"][nick], -1)
			# 
			# yield_qcd_ss_lowmt = tools.PoissonYield(plotData.plotdict["root_objects"][qcd_yield_nick])()
			# for nick in qcd_yield_substract_nick:
			# 	if "wj" in nick and tools.PoissonYield(plotData.plotdict["root_objects"][nick])() != 0.0:
			# 		scale_factor = wjets_scale_factor * wjets_scale_factor_shift
			# 		plotData.plotdict["root_objects"][nick].Scale(scale_factor.nominal_value)
			# 	yield_qcd_ss_lowmt -= tools.PoissonYield(plotData.plotdict["root_objects"][nick])()
			# yield_qcd_ss_lowmt = max(uncertainties.ufloat(0.0, yield_qcd_ss_lowmt.std_dev), yield_qcd_ss_lowmt)
			# if yield_qcd_ss_lowmt.nominal_value == 0.0:
			# 	log.warning("W+jets & QCD estimation: data yield in low mT SS region after background subtraction is 0!")
			# 
			# # get qcd yield in low mt region
			# qcd_yield = yield_qcd_ss_lowmt * qcd_extrapolation_factor_ss_os
			# 
			# integral_shape = tools.PoissonYield(plotData.plotdict["root_objects"][qcd_shape_nick])()
			# if integral_shape != 0.0:
			# 	scale_factor = qcd_yield / integral_shape
			# 	plotData.plotdict["root_objects"][qcd_shape_nick].Scale(scale_factor.nominal_value)
			# 
			# integral_shape = tools.PoissonYield(plotData.plotdict["root_objects"][qcd_ss_lowmt_nick])()
			# if integral_shape != 0.0:
			# 	scale_factor = yield_qcd_ss_lowmt / integral_shape
			# 	plotData.plotdict["root_objects"][qcd_ss_lowmt_nick].Scale(scale_factor.nominal_value)
			# 
			# # write relative uncertainties to metadata to pick them up with combine
			# plotData.metadata[qcd_shape_nick] = {
			# 	"yield" : qcd_yield.nominal_value,
			# 	"yield_unc" : qcd_yield.std_dev,
			# 	"yield_unc_rel" : abs(qcd_yield.std_dev/qcd_yield.nominal_value if qcd_yield.nominal_value != 0.0 else 0.0),
			# }
