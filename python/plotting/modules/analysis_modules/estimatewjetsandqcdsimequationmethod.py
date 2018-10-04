# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import ROOT

import HiggsAnalysis.KITHiggsToTauTau.plotting.modules.analysis_modules.estimatebase as estimatebase
import HiggsAnalysis.KITHiggsToTauTau.tools as tools
import HiggsAnalysis.KITHiggsToTauTau.uncertainties.uncertainties as uncertainties


class EstimateWjetsAndQCDSimEquationMethod(estimatebase.EstimateBase):
	""" This modules estimates W+jets and QCD backgrounds using the same-equation method."""
	def __init__(self):
		super(EstimateWjetsAndQCDSimEquationMethod, self).__init__()

	def modify_argument_parser(self, parser, args):
		super(EstimateWjetsAndQCDSimEquationMethod, self).modify_argument_parser(parser, args)
		
		self.estimate_wjets_and_qcd_prefit_options = parser.add_argument_group("WJets and QCD estimation options")
		
		self.estimate_wjets_and_qcd_prefit_options.add_argument("--use-inclusive-wjets-mc", nargs="+", type=bool, default=[False],
				help="Use inclusive selection to determine the Wjets OSSS factor. [Default: %(default)s]")
		# Step 1
		self.estimate_wjets_and_qcd_prefit_options.add_argument("--wjets-ss-mc-nicks", nargs="+", default=[""],
				help="Nicks for inclusive (No mT cut applied) ss mc histogram. [Default: %(default)s]")
		self.estimate_wjets_and_qcd_prefit_options.add_argument("--wjets-os-mc-nicks", nargs="+", default=[""],
				help="Nicks for inclusive (No mT cut applied) os mc histogram. [Default: %(default)s]")	
		# Step 2		
		self.estimate_wjets_and_qcd_prefit_options.add_argument("--wjets-D-mc-nicks", nargs="+", default=[""],
				help="Nicks for highmt os W+jets mc histogram. [Default: %(default)s]")
		self.estimate_wjets_and_qcd_prefit_options.add_argument("--wjets-A-mc-nicks", nargs="+", default=[""],
				help="Nicks for lowmt os W+jets mc histogram. [Default: %(default)s]")
		# Step 3		
		self.estimate_wjets_and_qcd_prefit_options.add_argument("--wjets-C-mc-nicks", nargs="+", default=[""],
				help="Nicks for highmt ss W+jets mc histogram. [Default: %(default)s]")
		self.estimate_wjets_and_qcd_prefit_options.add_argument("--wjets-B-mc-nicks", nargs="+", default=[""],
				help="Nicks for lowmt ss W+jets mc histogram. [Default: %(default)s]")
		# Step 4
		self.estimate_wjets_and_qcd_prefit_options.add_argument("--qcd-extrapolation-factors-ss-os", nargs="+", type=float, default=[1.00],
				help="Extrapolation factors of QCD OS/SS yields. [Default: %(default)s]")		
		# Step 5 
		self.estimate_wjets_and_qcd_prefit_options.add_argument("--wjets-C-data-nicks", nargs="+", default=[""],
				help="Nicks for ss highmt data histogram. [Default: %(default)s]")				
		self.estimate_wjets_and_qcd_prefit_options.add_argument("--C-subtract-nicks", nargs="+",
				default=[""],
				help="Nicks for ss control region histogram to substract from data to get the W+jets yield (whitespace separated). [Default: %(default)s]")
		self.estimate_wjets_and_qcd_prefit_options.add_argument("--wjets-D-data-nicks", nargs="+", default=[""],
				help="Nicks for ss highmt data histogram. [Default: %(default)s]")				
		self.estimate_wjets_and_qcd_prefit_options.add_argument("--D-subtract-nicks", nargs="+",
				default=[""],
				help="Nicks for ss control region histogram to substract from data to get the W+jets yield (whitespace separated). [Default: %(default)s]")
		self.estimate_wjets_and_qcd_prefit_options.add_argument("--wjets-C-shape-nicks", nargs="+", default=[""],
				help="Nicks for histogram to plot. [Default: %(default)s]")
		# Step 6
		self.estimate_wjets_and_qcd_prefit_options.add_argument("--wjets-A-shape-nicks", nargs="+", default=[""],
				help="Nicks for histogram to plot. [Default: %(default)s]")	
		self.estimate_wjets_and_qcd_prefit_options.add_argument("--wjets-B-shape-nicks", nargs="+", default=[""],
				help="Nicks for histogram to plot. [Default: %(default)s]")	
		self.estimate_wjets_and_qcd_prefit_options.add_argument("--wjets-D-shape-nicks", nargs="+", default=[""],
				help="Nicks for histogram to plot. [Default: %(default)s]")										
		# Step 7
		self.estimate_wjets_and_qcd_prefit_options.add_argument("--qcd-os-highmt-nicks", nargs="+", default=[""],
				help="Nicks for os highmt data histogram. [Default: %(default)s]")
		self.estimate_wjets_and_qcd_prefit_options.add_argument("--qcd-ss-highmt-nicks", nargs="+", default=[""],
				help="Nicks for ss highmt data histogram. [Default: %(default)s]")				
		self.estimate_wjets_and_qcd_prefit_options.add_argument("--qcd-ss-lowmt-nicks", nargs="+", default=[""],
				help="Nicks for ss lowmt data histogram. [Default: %(default)s]")
		self.estimate_wjets_and_qcd_prefit_options.add_argument("--qcd-ss-data-nicks", nargs="+", default=[""],
				help="Nicks for ss lowmt data histogram. [Default: %(default)s]")									
		self.estimate_wjets_and_qcd_prefit_options.add_argument("--qcd-shape-nicks", nargs="+", default=[""],
				help="Nicks for histogram to plot. [Default: %(default)s]")						
		self.estimate_wjets_and_qcd_prefit_options.add_argument("--B-subtract-nicks", nargs="+", default=[""],
				help="Nicks for histogram to plot. [Default: %(default)s]")												


	def prepare_args(self, parser, plotData):
		super(EstimateWjetsAndQCDSimEquationMethod, self).prepare_args(parser, plotData)
		self._plotdict_keys = ["use_inclusive_wjets_mc", "wjets_ss_mc_nicks", "wjets_os_mc_nicks", "wjets_D_mc_nicks", "wjets_A_mc_nicks", "wjets_C_mc_nicks", "wjets_B_mc_nicks", "wjets_C_data_nicks", "C_subtract_nicks", "wjets_D_data_nicks", "D_subtract_nicks", "wjets_C_shape_nicks", "wjets_B_shape_nicks", "wjets_A_shape_nicks", "wjets_D_shape_nicks",  "qcd_extrapolation_factors_ss_os",  "qcd_os_highmt_nicks", "qcd_ss_highmt_nicks", "qcd_ss_lowmt_nicks", "qcd_ss_data_nicks", "qcd_shape_nicks", "B_subtract_nicks"]
		self.prepare_list_args(plotData, self._plotdict_keys)
		for index in [ "C_subtract_nicks",  "D_subtract_nicks", "B_subtract_nicks"]:
			plotData.plotdict[index] = [nicks.split() for nicks in plotData.plotdict[index]]


	def run(self, plotData=None):
		super(EstimateWjetsAndQCDSimEquationMethod, self).run(plotData)
		
		# make sure that all necessary histograms are available
		for nicks in zip(*[plotData.plotdict[key] for key in self._plotdict_keys[:-1]]):
			for nick in nicks:
				print(nick)
				if isinstance(nick, basestring):
					assert isinstance(plotData.plotdict["root_objects"].get(nick), ROOT.TH1)
				elif (not isinstance(nick, float) and not isinstance(nick, bool)):
					for subnick in nick:
						print(subnick)
						assert isinstance(plotData.plotdict["root_objects"].get(subnick), ROOT.TH1)

		for use_inclusive_wjets_mc, wjets_ss_mc_nick, wjets_os_mc_nick, wjets_D_mc_nick, wjets_A_mc_nick, wjets_C_mc_nick, wjets_B_mc_nick, wjets_C_data_nick, C_subtract_nicks, wjets_D_data_nick, D_subtract_nicks, wjets_C_shape_nick,  wjets_B_shape_nick,  wjets_A_shape_nick, wjets_D_shape_nick, qcd_extrapolation_factor_ss_os, qcd_os_highmt_nick, qcd_ss_highmt_nick, qcd_ss_lowmt_nick, qcd_ss_data_nick, qcd_shape_nick, B_subtract_nicks in zip(*[plotData.plotdict[key] for key in self._plotdict_keys]):
			########################################
			# ------------ Step 1 ------------------
			# Measure W OS/SS factor from MonteCarlo
			# 1. Needs inclusive wj_mc for OS and SS 
			# 2. Therefore the scale factor is the same in the high mt control region (mT>70) and the low mt signal like region.
			
			yield_wj_mc_os = tools.PoissonYield(plotData.plotdict["root_objects"][wjets_os_mc_nick])()
			yield_wj_mc_ss = tools.PoissonYield(plotData.plotdict["root_objects"][wjets_ss_mc_nick])()
			
			# correct negative yields
			yield_wj_mc_os = uncertainties.ufloat(max(0.0, yield_wj_mc_os.nominal_value), yield_wj_mc_os.std_dev)
			yield_wj_mc_ss = uncertainties.ufloat(max(0.0, yield_wj_mc_ss.nominal_value), yield_wj_mc_ss.std_dev)
			
			yield_wj_mc_os_highmt = tools.PoissonYield(plotData.plotdict["root_objects"][wjets_D_mc_nick])()
			yield_wj_mc_ss_highmt = tools.PoissonYield(plotData.plotdict["root_objects"][wjets_C_mc_nick])()

			assert (yield_wj_mc_os_highmt != 0.0) or (yield_wj_mc_ss_highmt != 0.0), "Yield of MC in opposite-sign or same-sign region is zero."
			
			# calculate w_os_ss factor and store it in the metadata
			if use_inclusive_wjets_mc:
				w_os_ss_extrapolation_factor = yield_wj_mc_os / yield_wj_mc_ss
			else:
				w_os_ss_extrapolation_factor = yield_wj_mc_os_highmt / yield_wj_mc_ss_highmt
				
			log.debug("W+jets Opposite sign Same-sign factor is \"{FACTOR}\".".format(FACTOR = w_os_ss_extrapolation_factor))	

			
			########################################
			# ------------ Step 2 ------------------
			# Measure opposite-sign extrapolation factor from high Mt Control region (mT>70) to low Mt (mt<50)
			# 1. Needs wj_mc in opposite region for both mT regions.
			yield_wj_mc_os_highmt = tools.PoissonYield(plotData.plotdict["root_objects"][wjets_D_mc_nick])()
			yield_wj_mc_os_lowmt = tools.PoissonYield(plotData.plotdict["root_objects"][wjets_A_mc_nick])()
			
			
			assert (yield_wj_mc_os_highmt != 0.0) or (yield_wj_mc_os_lowmt != 0.0), "Yield of MC in opposite-sign lowmt or opposite-sign highmt region is zero."
			
			# calculate w_highmt_lowmt factor and store it in the metadata
			w_os_highmt_lowmt_extrapolation_factor = yield_wj_mc_os_lowmt/yield_wj_mc_os_highmt
			log.debug("W+jets Opposite-sign High mT to low mT factor is \"{FACTOR}\".".format(FACTOR = w_os_highmt_lowmt_extrapolation_factor))	
			
			########################################
			# ------------ Step 3 ------------------
			# Measure same-sign extrapolation factor from high Mt Control region (mT>70) to low Mt (mt<50)
			# This is needed to get the first estimate for Qcd in the same-sign region.
			# 1. Needs wj_mc in opposite region for both mT regions.

						
			# calculate w_highmt_lowmt factor and store it in the metadata
			if tools.PoissonYield(plotData.plotdict["root_objects"][wjets_C_mc_nick])() != 0.0:
				w_ss_highmt_lowmt_extrapolation_factor = tools.PoissonYield(plotData.plotdict["root_objects"][wjets_B_mc_nick])()/tools.PoissonYield(plotData.plotdict["root_objects"][wjets_C_mc_nick])()
			else: 
				log.warning("W+jets & QCD estimation: W+jets high mT region in MC has no entries. High->low mT extrapolation factor is set to 1.0!")
				w_ss_highmt_lowmt_extrapolation_factor = 1.0
			log.debug("W+jets Same-sign High mT to low mT factor is \"{FACTOR}\".".format(FACTOR = w_ss_highmt_lowmt_extrapolation_factor))	

			
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
			# 8. Scale the shape according to the scale factor.
					
			yield_wjets_ss_highmt = tools.PoissonYield(plotData.plotdict["root_objects"][wjets_C_data_nick])()	
			for nick in C_subtract_nicks:
				yield_wjets_ss_highmt -= tools.PoissonYield(plotData.plotdict["root_objects"][nick])()
				
			log.debug("W+jets Same-sign High mT before estimation yield is \"{YIELD}\".".format(YIELD = yield_wjets_ss_highmt))				
			yield_wjets_ss_highmt = uncertainties.ufloat(max(0.0, yield_wjets_ss_highmt.nominal_value), yield_wjets_ss_highmt.std_dev)
			yield_qcd_ss_highmt = yield_wjets_ss_highmt	
			yield_wjets_os_highmt = tools.PoissonYield(plotData.plotdict["root_objects"][wjets_D_data_nick])()
			for nick in D_subtract_nicks:
				yield_wjets_os_highmt -= tools.PoissonYield(plotData.plotdict["root_objects"][nick])()
			yield_wjets_os_highmt = uncertainties.ufloat(max(0.0, yield_wjets_os_highmt.nominal_value), yield_wjets_os_highmt.std_dev)	
				
			log.debug("W+jets Same-sign High mT before estimation yield is \"{YIELD}\".".format(YIELD = yield_wjets_ss_highmt))	
			log.debug("W+jets opposite-sign High mT before estimation yield is \"{YIELD}\".".format(YIELD = yield_wjets_os_highmt))	
			print("qcd_extrapolation_factor_ss_os * yield_wjets_ss_highmt: ", qcd_extrapolation_factor_ss_os * yield_wjets_ss_highmt)
			yield_wjets_ss_highmt = yield_wjets_os_highmt - qcd_extrapolation_factor_ss_os * yield_wjets_ss_highmt
			
			# yield_wjets_ss_highmt = uncertainties.ufloat(max(0.0, yield_wjets_ss_highmt.nominal_value), yield_wjets_ss_highmt.std_dev)
			yield_wjets_ss_highmt = yield_wjets_ss_highmt / (w_os_ss_extrapolation_factor - qcd_extrapolation_factor_ss_os)
			
			log.debug("W+jets Same-sign High mT after estimation yield is \"{YIELD}\".".format(YIELD = yield_wjets_ss_highmt))	
			yield_wjets_ss_highmt = uncertainties.ufloat(max(0.0, yield_wjets_ss_highmt.nominal_value), yield_wjets_ss_highmt.std_dev)
			log.debug("W+jets Same-sign High mT after estimation yield is \"{YIELD}\".".format(YIELD = yield_wjets_ss_highmt))
			# store the eyield that might be expected for QCD after having determined Wjets in the highmt ss region
			yield_qcd_ss_highmt -= yield_wjets_ss_highmt
			if yield_wjets_ss_highmt.nominal_value == 0.0:
				log.warning("W+jets & QCD estimation: data yield in high mT same-sign region after background subtraction is 0!")	
			
			# scale same-sign highmt Wjets histograms for controlplots.
			integral_shape = tools.PoissonYield(plotData.plotdict["root_objects"][wjets_C_shape_nick])()
			if integral_shape != 0.0:
				scale_factor = yield_wjets_ss_highmt / integral_shape
				log.debug("Scale factor for process W+jets (nick \"{nick}\") is {scale_factor}.".format(nick=wjets_C_shape_nick, scale_factor=scale_factor))
				plotData.plotdict["root_objects"][wjets_C_shape_nick].Scale(scale_factor.nominal_value)
				plotData.plotdict["root_objects"][wjets_C_shape_nick].Print()			
			
			########################################
			# ------------ Step 6 a ------------------
			# Estimate final opposite-sign  lowmT W+jets yield 
			# 1. Multiply yield from before the Wjets OS/SS and the low-highmt factor.
			# 2. Scale the shape nicks by the resulting scale factor. 
			
			final_yield_wjets_os_lowmt = w_os_highmt_lowmt_extrapolation_factor * w_os_ss_extrapolation_factor * yield_wjets_ss_highmt
			
			log.debug("W+jets Opposite-sign low mT yield is \"{YIELD}\".".format(YIELD = final_yield_wjets_os_lowmt))	
			if final_yield_wjets_os_lowmt.nominal_value == 0.0:
				log.warning("W+jets estimation: Final yield in low mT opposite-sign is 0!")	
			
			# scale same-sign highmt Wjets histograms for controlplots.
			integral_shape = tools.PoissonYield(plotData.plotdict["root_objects"][wjets_A_shape_nick])()
			if integral_shape != 0.0:
				scale_factor = final_yield_wjets_os_lowmt/integral_shape
				log.debug("Scale factor for process W+jets (nick \"{nick}\") is {scale_factor}.".format(nick=wjets_A_shape_nick, scale_factor=scale_factor))
				plotData.plotdict["root_objects"][wjets_A_shape_nick].Scale(scale_factor.nominal_value)	
				plotData.plotdict["root_objects"][wjets_A_shape_nick].Print()			
			
			########################################
			# ------------ Step 6 b ------------------
			# Estimate final same-sign  lowmT W+jets yield 
			# 1. Multiply yield from before the Wjets OS/SS and the low-highmt factor.
			# 2. Scale the shape nicks by the resulting scale factor. 				
			
			final_yield_wjets_ss_lowmt = w_ss_highmt_lowmt_extrapolation_factor * yield_wjets_ss_highmt
			log.debug("W+jets Same-sign low mT yield is \"{YIELD}\".".format(YIELD = final_yield_wjets_ss_lowmt))	

			if final_yield_wjets_ss_lowmt.nominal_value == 0.0:
			 	log.warning("W+jets estimation: Final yield in low mT same-sign is 0!")	
			
			# scale same-sign highmt Wjets histograms for controlplots.
			integral_shape = tools.PoissonYield(plotData.plotdict["root_objects"][wjets_B_shape_nick])()
			if integral_shape != 0.0:
				scale_factor = final_yield_wjets_ss_lowmt / integral_shape				
				log.debug("Scale factor for process W+jets (nick \"{nick}\") is {scale_factor}.".format(nick=wjets_B_shape_nick, scale_factor=scale_factor))
				plotData.plotdict["root_objects"][wjets_B_shape_nick].Scale(scale_factor.nominal_value)	
				plotData.plotdict["root_objects"][wjets_B_shape_nick].Print()			

			########################################
			# ------------ Step 6 c ------------------
			# Estimate final opposite-sign  highmT W+jets yield 
			# 1. Multiply yield from before the Wjets OS/SS factor.
			# 2. Scale the shape nicks by the resulting scale factor. 				
			
			final_yield_wjets_os_highmt = w_os_ss_extrapolation_factor * yield_wjets_ss_highmt
			log.debug("W+jets opposite-sign high mT yield is \"{YIELD}\".".format(YIELD = final_yield_wjets_os_highmt))	

			if final_yield_wjets_os_highmt.nominal_value == 0.0:
			 	log.warning("W+jets estimation: Final yield in low mT same-sign is 0!")	
			
			# scale same-sign highmt Wjets histograms for controlplots.
			integral_shape = tools.PoissonYield(plotData.plotdict["root_objects"][wjets_D_shape_nick])()
			if integral_shape != 0.0:
				scale_factor = final_yield_wjets_os_highmt / integral_shape				
				log.debug("Scale factor for process W+jets (nick \"{nick}\") is {scale_factor}.".format(nick=wjets_D_shape_nick, scale_factor=scale_factor))
				plotData.plotdict["root_objects"][wjets_D_shape_nick].Scale(scale_factor.nominal_value)	
				plotData.plotdict["root_objects"][wjets_D_shape_nick].Print()
					
			plotData.metadata[wjets_A_shape_nick] = {
				"w_os_ss_factor" : w_os_ss_extrapolation_factor.nominal_value,
				"w_os_ss_factor_unc" : w_os_ss_extrapolation_factor.std_dev,
				"w_os_ss_factor_unc_rel" : abs(w_os_ss_extrapolation_factor.std_dev/w_os_ss_extrapolation_factor.nominal_value if w_os_ss_extrapolation_factor.nominal_value != 0.0 else 0.0),			
				"w_os_highmt_lowmt_factor" : w_os_highmt_lowmt_extrapolation_factor.nominal_value,
				"w_os_highmt_lowmt_factor_unc" : w_os_highmt_lowmt_extrapolation_factor.std_dev,
				"w_os_highmt_lowmt_factor_unc_rel" : abs(w_os_highmt_lowmt_extrapolation_factor.std_dev/w_os_highmt_lowmt_extrapolation_factor.nominal_value if w_os_highmt_lowmt_extrapolation_factor.nominal_value != 0.0 else 0.0),	
				"w_ss_highmt_lowmt_factor" : w_ss_highmt_lowmt_extrapolation_factor.nominal_value,
				"w_ss_highmt_lowmt_factor_unc" : w_ss_highmt_lowmt_extrapolation_factor.std_dev,
				"w_ss_highmt_lowmt_factor_unc_rel" : abs(w_ss_highmt_lowmt_extrapolation_factor.std_dev/w_ss_highmt_lowmt_extrapolation_factor.nominal_value if w_ss_highmt_lowmt_extrapolation_factor.nominal_value != 0.0 else 0.0),
				"w_ss_highmt_yield" : yield_wjets_ss_highmt.nominal_value,
				"w_ss_highmt_yield_unc" : yield_wjets_ss_highmt.std_dev,
				"w_ss_highmt_yield_unc_rel" : abs(yield_wjets_ss_highmt.std_dev/yield_wjets_ss_highmt.nominal_value if yield_wjets_ss_highmt.nominal_value != 0.0 else 0.0),
				"w_os_lowmt_yield" : final_yield_wjets_os_lowmt.nominal_value,
				"w_os_lowmt_yield_unc" : final_yield_wjets_os_lowmt.std_dev,
				"w_os_lowmt_yield_unc_rel" : abs(final_yield_wjets_os_lowmt.std_dev/final_yield_wjets_os_lowmt.nominal_value if final_yield_wjets_os_lowmt.nominal_value != 0.0 else 0.0),
				"w_ss_lowmt_yield" : final_yield_wjets_ss_lowmt.nominal_value,
				"w_ss_lowmt_yield_unc" : final_yield_wjets_ss_lowmt.std_dev,
				"w_ss_lowmt_yield_unc_rel" : abs(final_yield_wjets_ss_lowmt.std_dev/final_yield_wjets_ss_lowmt.nominal_value if final_yield_wjets_ss_lowmt.nominal_value != 0.0 else 0.0),
			}
			log.debug(plotData.metadata)	
						
			########################################
			# ------------ Step 7 ------------------
			# Get a opposite-sign region QCD estimate
			# 1. Get same-sign low-mt data yield.
			# 2. Subtract all background except for Wjets from it.
			# 3. Calculate same-sign lowmt Wjets estimate using the highMt estimte from step 5.
			# 4. Subtract also Wjets to get the same-sign QCD yield.
			# 5. Get the shapes for all histograms and background and get a QCD shape estimate
			
							
			yield_qcd_ss = tools.PoissonYield(plotData.plotdict["root_objects"][qcd_ss_data_nick])()
			for nick in B_subtract_nicks:			
				yield_qcd_ss -= tools.PoissonYield(plotData.plotdict["root_objects"][nick])()
			yield_qcd_ss -= tools.PoissonYield(plotData.plotdict["root_objects"][wjets_B_shape_nick])()
			yield_qcd_ss = uncertainties.ufloat(max(0.0, yield_qcd_ss.nominal_value), yield_qcd_ss.std_dev)

			log.debug("QCD Same-sign yield is \"{YIELD}\".".format(YIELD = yield_qcd_ss))				
			if yield_qcd_ss.nominal_value == 0.0: 
				log.warning("QCD estimation: yield in low mT same-sign is 0!")	
			
			for nick in B_subtract_nicks:
				plotData.plotdict["root_objects"][qcd_shape_nick].Add(plotData.plotdict["root_objects"][nick], -1)
			
			plotData.plotdict["root_objects"][qcd_shape_nick].Add(plotData.plotdict["root_objects"][wjets_B_shape_nick], -1)
			
			qcd_shape_yield = tools.PoissonYield(plotData.plotdict["root_objects"][qcd_shape_nick])()
			qcd_shape_yield = uncertainties.ufloat(max(0.0, qcd_shape_yield.nominal_value), qcd_shape_yield.std_dev)

			yield_qcd_os = yield_qcd_ss * qcd_extrapolation_factor_ss_os
			if qcd_shape_yield.nominal_value != 0:
				scale_factor = yield_qcd_os / qcd_shape_yield 
				log.debug("Scale factor for process QCD (nick \"{nick}\") is {scale_factor}.".format(nick=qcd_shape_nick, scale_factor=scale_factor))
				plotData.plotdict["root_objects"][qcd_shape_nick].Scale(scale_factor.nominal_value)	
				plotData.plotdict["root_objects"][qcd_shape_nick].Print()			
				

			plotData.metadata[qcd_shape_nick] = {
				"QCD SS/OS factor" : qcd_extrapolation_factor_ss_os,
				"QCD Opposite-sign yield" : yield_qcd_os.nominal_value,
				"QCD Opposite-sign yield_unc" : yield_qcd_os.std_dev,
				"QCD Opposite-sign yield_unc_rel" : abs(yield_qcd_os.std_dev/yield_qcd_os.nominal_value if yield_qcd_os.nominal_value != 0.0 else 0.0),
			}

			qcd_shape_yield = tools.PoissonYield(plotData.plotdict["root_objects"][qcd_ss_lowmt_nick])()
			qcd_shape_yield = uncertainties.ufloat(max(0.0, qcd_shape_yield.nominal_value), qcd_shape_yield.std_dev)
			if qcd_shape_yield.nominal_value != 0:
				scale_factor = yield_qcd_ss / qcd_shape_yield
				log.debug("Scale factor for process QCD (nick \"{nick}\") is {scale_factor}.".format(nick=qcd_ss_lowmt_nick, scale_factor=scale_factor))
				plotData.plotdict["root_objects"][qcd_ss_lowmt_nick].Scale(scale_factor.nominal_value)	
				plotData.plotdict["root_objects"][qcd_ss_lowmt_nick].Print()			

			plotData.metadata[qcd_shape_nick] = {
				"QCD Same-sign yield" : yield_qcd_ss.nominal_value,
				"QCD Same-sign yield_unc" : yield_qcd_ss.std_dev,
				"QCD Same-sign yield_unc_rel" : abs(yield_qcd_ss.std_dev/yield_qcd_ss.nominal_value if yield_qcd_ss.nominal_value != 0.0 else 0.0),
			}
			
			qcd_shape_yield = tools.PoissonYield(plotData.plotdict["root_objects"][qcd_ss_highmt_nick])()
			qcd_shape_yield = uncertainties.ufloat(max(0.0, qcd_shape_yield.nominal_value), qcd_shape_yield.std_dev)		
			if qcd_shape_yield.nominal_value != 0:
				scale_factor = yield_qcd_ss_highmt / qcd_shape_yield
				log.debug("Scale factor for process QCD (nick \"{nick}\") is {scale_factor}.".format(nick=qcd_ss_highmt_nick, scale_factor=scale_factor))
				plotData.plotdict["root_objects"][qcd_ss_highmt_nick].Scale(scale_factor.nominal_value)	
				plotData.plotdict["root_objects"][qcd_ss_highmt_nick].Print()			

			plotData.metadata[qcd_shape_nick] = {
				"QCD Same-sign highmt yield" : yield_qcd_ss_highmt.nominal_value,
				"QCD Same-sign highmt yield_unc" : yield_qcd_ss_highmt.std_dev,
				"QCD Same-sign highmt yield_unc_rel" : abs(yield_qcd_ss_highmt.std_dev/yield_qcd_ss_highmt.nominal_value if yield_qcd_ss_highmt.nominal_value != 0.0 else 0.0),
			}
			
			
			qcd_shape_yield = tools.PoissonYield(plotData.plotdict["root_objects"][qcd_os_highmt_nick])()
			qcd_shape_yield = uncertainties.ufloat(max(0.0, qcd_shape_yield.nominal_value), qcd_shape_yield.std_dev)		
			if qcd_shape_yield.nominal_value != 0:
				scale_factor = yield_qcd_ss_highmt * qcd_extrapolation_factor_ss_os / qcd_shape_yield
				log.debug("Scale factor for process QCD (nick \"{nick}\") is {scale_factor}.".format(nick=qcd_os_highmt_nick, scale_factor=scale_factor))
				plotData.plotdict["root_objects"][qcd_os_highmt_nick].Scale(scale_factor.nominal_value)	
				plotData.plotdict["root_objects"][qcd_os_highmt_nick].Print()			

			plotData.metadata[qcd_shape_nick] = {
				"QCD opposite-sign highmt yield" : yield_qcd_ss_highmt.nominal_value,
				"QCD opposite-sign highmt yield_unc" : yield_qcd_ss_highmt.std_dev,
				"QCD opposite-sign highmt yield_unc_rel" : abs(yield_qcd_ss_highmt.std_dev/yield_qcd_ss_highmt.nominal_value if yield_qcd_ss_highmt.nominal_value != 0.0 else 0.0),
			}
							
						
			# log.info(plotData.metadata)
