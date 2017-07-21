# -*- coding: utf-8 -*-

"""
"""

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import ROOT

import HiggsAnalysis.KITHiggsToTauTau.plotting.modules.analysis_modules.estimatebase as estimatebase
import HiggsAnalysis.KITHiggsToTauTau.tools as tools
import HiggsAnalysis.KITHiggsToTauTau.uncertainties.uncertainties as uncertainties


class EstimateWjetsAndQCD(estimatebase.EstimateBase):
	def __init__(self):
		super(EstimateWjetsAndQCD, self).__init__()

	def modify_argument_parser(self, parser, args):
		super(EstimateWjetsAndQCD, self).modify_argument_parser(parser, args)
		
		self.estimate_wjets_and_qcd_options = parser.add_argument_group("WJets and QCD estimation options")
		self.estimate_wjets_and_qcd_options.add_argument("--qcd-extrapolation-factors-ss-os", nargs="+", type=float, default=[1.00],
				help="Extrapolation factors of QCD OS/SS yields. [Default: %(default)s]")
		self.estimate_wjets_and_qcd_options.add_argument("--qcd-shape-nicks", nargs="+", default=[""],
				help="Nicks for histogram to plot. [Default: %(default)s]")
		self.estimate_wjets_and_qcd_options.add_argument("--qcd-yield-nicks", nargs="+", default=[""],
				help="Nicks for histogram to plot. [Default: %(default)s]")
		self.estimate_wjets_and_qcd_options.add_argument("--qcd-ss-lowmt-nicks", nargs="+", default=[""],
				help="Nicks for histogram to plot. [Default: %(default)s]")
		self.estimate_wjets_and_qcd_options.add_argument("--qcd-ss-highmt-shape-nicks", nargs="+", default=[""],
				help="Nicks for histogram to plot. [Default: %(default)s]")
		self.estimate_wjets_and_qcd_options.add_argument("--qcd-os-highmt-nicks", nargs="+", default=[""],
				help="Nicks for histogram to plot. [Default: %(default)s]")
		self.estimate_wjets_and_qcd_options.add_argument("--qcd-shape-highmt-substract-nicks", nargs="+",
				default=[""],
				help="Nicks for control region histogram to substract from data  to get the QCD yield (whitespace separated). [Default: %(default)s]")
		self.estimate_wjets_and_qcd_options.add_argument("--qcd-yield-substract-nicks", nargs="+",
				default=[""],
				help="Nicks for control region histogram to substract from data  to get the QCD yield (whitespace separated). [Default: %(default)s]")
		self.estimate_wjets_and_qcd_options.add_argument("--qcd-shape-substract-nicks", nargs="+",
				default=[""],
				help="Nicks for control region histogram to substract from data to get the QCD shape (whitespace separated). [Default: %(default)s]")
		self.estimate_wjets_and_qcd_options.add_argument("--wjets-ss-substract-nicks", nargs="+",
				default=[""],
				help="Nicks for ss control region histogram to substract from data to get the W+jets yield (whitespace separated). [Default: %(default)s]")
		self.estimate_wjets_and_qcd_options.add_argument("--wjets-os-substract-nicks", nargs="+",
				default=[""],
				help="Nicks for os control region histogram to substract from data to get the W+jets yield (whitespace separated). [Default: %(default)s]")
		self.estimate_wjets_and_qcd_options.add_argument("--wjets-os-highmt-mc-nicks", nargs="+", default=[""],
				help="Nicks for highmt os W+jets histogram. [Default: %(default)s]")
		self.estimate_wjets_and_qcd_options.add_argument("--wjets-ss-highmt-mc-nicks", nargs="+", default=[""],
				help="Nicks for highmt ss W+jets histogram. [Default: %(default)s]")
		self.estimate_wjets_and_qcd_options.add_argument("--wjets-ss-data-nicks", nargs="+", default=[""],
				help="Nicks for ss highmt data histogram. [Default: %(default)s]")
		self.estimate_wjets_and_qcd_options.add_argument("--wjets-os-data-nicks", nargs="+", default=[""],
				help="Nicks for os highmt data histogram. [Default: %(default)s]")
		self.estimate_wjets_and_qcd_options.add_argument("--wjets-shape-nicks", nargs="+", default=[""],
				help="Nicks for W+jets signal region histogram. [Default: %(default)s]")
		self.estimate_wjets_and_qcd_options.add_argument("--wjets-wj-final-selection", nargs="+", default=[""],
				help="Nicks for W+jets in final category. [Default: %(default)s]")
		self.estimate_wjets_and_qcd_options.add_argument("--wjets-relaxed-os-highmt-nicks", nargs="+", default=[""],
				help="Nicks for os highmt W+jets histogram with relaxed selection. [Default: %(default)s]")
		self.estimate_wjets_and_qcd_options.add_argument("--wjets-relaxed-os-lowmt-nicks", nargs="+", default=[""],
				help="Nicks for os lowmt W+jets histogram with relaxed selection. [Default: %(default)s]")
		self.estimate_wjets_and_qcd_options.add_argument("--wjets-scale-factor-shifts", nargs="+", type=float, default=[1.0],
				help="Determine by how much the W+jets scale factor should be shifted for the QCD estimation in the low mt region. [Default: %(default)s]")

	def prepare_args(self, parser, plotData):
		super(EstimateWjetsAndQCD, self).prepare_args(parser, plotData)
		self._plotdict_keys = ["qcd_extrapolation_factors_ss_os", "qcd_shape_nicks", "qcd_ss_lowmt_nicks", "qcd_ss_highmt_shape_nicks", "qcd_os_highmt_nicks", "qcd_shape_highmt_substract_nicks", "qcd_yield_nicks", "qcd_shape_substract_nicks", "qcd_yield_substract_nicks", "wjets_os_highmt_mc_nicks", "wjets_ss_highmt_mc_nicks", "wjets_ss_substract_nicks", "wjets_ss_data_nicks", "wjets_os_substract_nicks", "wjets_os_data_nicks", "wjets_shape_nicks", "wjets_relaxed_os_highmt_nicks", "wjets_relaxed_os_lowmt_nicks", "wjets_scale_factor_shifts"]
		self.prepare_list_args(plotData, self._plotdict_keys)
		for index in ["qcd_shape_substract_nicks", "qcd_yield_substract_nicks", "wjets_ss_substract_nicks", "wjets_os_substract_nicks","qcd_shape_highmt_substract_nicks"]:
			plotData.plotdict[index] = [nicks.split() for nicks in plotData.plotdict[index]]
		# make sure that all necessary histograms are available
		for nicks in zip(*[plotData.plotdict[key] for key in self._plotdict_keys]):
			for nick in nicks:
				if isinstance(nick, basestring):
					assert isinstance(plotData.plotdict["root_objects"].get(nick), ROOT.TH1)
				elif (not isinstance(nick, float) and not isinstance(nick, bool)):
					for subnick in nick:
						assert isinstance(plotData.plotdict["root_objects"].get(subnick), ROOT.TH1)
		# do not check because it's allowed to be None
		self._plotdict_keys.append("wjets_wj_final_selection")

	def run(self, plotData=None):
		super(EstimateWjetsAndQCD, self).run(plotData)

		for qcd_extrapolation_factor_ss_os, qcd_shape_nick, qcd_ss_lowmt_nick, qcd_ss_highmt_shape_nick, qcd_os_highmt_nick, qcd_shape_highmt_substract_nick, qcd_yield_nick, qcd_shape_substract_nick, qcd_yield_substract_nick, wjets_os_highmt_mc_nick, wjets_ss_highmt_mc_nick, wjets_ss_substract_nick, wjets_ss_data_nick, wjets_os_substract_nick, wjets_os_data_nick, wjets_shape_nick, wjets_relaxed_os_highmt_nick, wjets_relaxed_os_lowmt_nick, wjets_scale_factor_shift, wjets_final_selection in zip(*[plotData.plotdict[key] for key in self._plotdict_keys]):
			########################################
			# estimate QCD for the highmT region
			
			# get qcd ss high mt shape
			for nick in qcd_shape_highmt_substract_nick+[wjets_ss_highmt_mc_nick]:
				plotData.plotdict["root_objects"][qcd_ss_highmt_shape_nick].Add(plotData.plotdict["root_objects"][nick], -1)
			
			# get qcd yield in ss high mt region
			yield_qcd_ss_highmt = tools.PoissonYield(plotData.plotdict["root_objects"][wjets_ss_data_nick])()
			for nick in wjets_ss_substract_nick+[wjets_ss_highmt_mc_nick]:
				yield_qcd_ss_highmt -= tools.PoissonYield(plotData.plotdict["root_objects"][nick])()
			yield_qcd_ss_highmt = max(uncertainties.ufloat(0.0, yield_qcd_ss_highmt.std_dev), yield_qcd_ss_highmt)
			
			# scale qcd ss high mt shape by qcd yield found in data
			integral_shape = tools.PoissonYield(plotData.plotdict["root_objects"][qcd_ss_highmt_shape_nick])()
			if integral_shape != 0.0:
				scale_factor = yield_qcd_ss_highmt / integral_shape
				plotData.plotdict["root_objects"][qcd_ss_highmt_shape_nick].Scale(scale_factor.nominal_value)
			
			# scale qcd os high mt shape by qcd yield found in ss data and ss->os extrapolation factor
			integral_shape = tools.PoissonYield(plotData.plotdict["root_objects"][qcd_os_highmt_nick])()
			if integral_shape != 0.0:
				scale_factor = yield_qcd_ss_highmt * qcd_extrapolation_factor_ss_os / integral_shape
				plotData.plotdict["root_objects"][qcd_os_highmt_nick].Scale(scale_factor.nominal_value)
			
			########################################
			# estimate W+jets
			
			# get w+jets yield in os high mt region
			yield_wjets_os_highmt = tools.PoissonYield(plotData.plotdict["root_objects"][wjets_os_data_nick])()
			for nick in wjets_os_substract_nick:
				yield_wjets_os_highmt -= tools.PoissonYield(plotData.plotdict["root_objects"][nick])()
			yield_wjets_os_highmt -= qcd_extrapolation_factor_ss_os*yield_qcd_ss_highmt
			yield_wjets_os_highmt = max(uncertainties.ufloat(0.0, yield_wjets_os_highmt.std_dev), yield_wjets_os_highmt)
			if yield_wjets_os_highmt.nominal_value == 0.0:
				log.warning("W+jets & QCD estimation: data yield in high mT region after background subtraction is 0!")
			
			# get high mt -> low mt extrapolation factor from MC
			if tools.PoissonYield(plotData.plotdict["root_objects"][wjets_relaxed_os_highmt_nick])() != 0.0:
				wjets_extrapolation_factor_mt = tools.PoissonYield(plotData.plotdict["root_objects"][wjets_relaxed_os_lowmt_nick])()/tools.PoissonYield(plotData.plotdict["root_objects"][wjets_relaxed_os_highmt_nick])()
			else:
				log.warning("W+jets & QCD estimation: W+jets high mT region in MC has no entries. High->low mT extrapolation factor is set to 1.0!")
				wjets_extrapolation_factor_mt = 1.0
			
			# get w+jets yield in low mt region
			wjets_yield = yield_wjets_os_highmt*wjets_extrapolation_factor_mt
			
			# extrapolate to final selection
			if wjets_final_selection != None:
				wjets_yield = wjets_yield * tools.PoissonYield(plotData.plotdict["root_objects"][wjets_final_selection])() / tools.PoissonYield(plotData.plotdict["root_objects"][wjets_relaxed_os_lowmt_nick])()
			
			# scale signal region histograms
			integral_shape = tools.PoissonYield(plotData.plotdict["root_objects"][wjets_shape_nick])()
			if integral_shape != 0.0:
				scale_factor = wjets_yield / integral_shape
				log.debug("Scale factor for process W+jets (nick \"{nick}\") is {scale_factor}.".format(nick=wjets_shape_nick, scale_factor=scale_factor))
				plotData.plotdict["root_objects"][wjets_shape_nick].Scale(scale_factor.nominal_value)
			
			plotData.metadata[wjets_shape_nick] = {
				"yield" : wjets_yield.nominal_value,
				"yield_unc" : wjets_yield.std_dev,
				"yield_unc_rel" : abs(wjets_yield.std_dev/wjets_yield.nominal_value if wjets_yield.nominal_value != 0.0 else 0.0),
			}
			
			########################################
			# estimate QCD for the lowmT
			
			# define w+jets scale factor for qcd estimation
			if tools.PoissonYield(plotData.plotdict["root_objects"][wjets_os_highmt_mc_nick])() != 0.0:
				wjets_scale_factor = yield_wjets_os_highmt/tools.PoissonYield(plotData.plotdict["root_objects"][wjets_os_highmt_mc_nick])()
			else:
				log.warning("W+jets & QCD estimation: W+jets high mT region in MC has no entries. Scale factor for W+jets in QCD estimation is set to 1.0!")
				wjets_scale_factor = uncertainties.ufloat(1.0, 0.0)
			
			for nick in qcd_shape_substract_nick:
				if "wj" in nick:
					scale_factor = wjets_scale_factor * wjets_scale_factor_shift
					plotData.plotdict["root_objects"][nick].Scale(scale_factor.nominal_value)
				plotData.plotdict["root_objects"][qcd_shape_nick].Add(plotData.plotdict["root_objects"][nick], -1)
			
			yield_qcd_ss_lowmt = tools.PoissonYield(plotData.plotdict["root_objects"][qcd_yield_nick])()
			for nick in qcd_yield_substract_nick:
				if "wj" in nick and tools.PoissonYield(plotData.plotdict["root_objects"][nick])() != 0.0:
					scale_factor = wjets_scale_factor * wjets_scale_factor_shift
					plotData.plotdict["root_objects"][nick].Scale(scale_factor.nominal_value)
				yield_qcd_ss_lowmt -= tools.PoissonYield(plotData.plotdict["root_objects"][nick])()
			yield_qcd_ss_lowmt = max(uncertainties.ufloat(0.0, yield_qcd_ss_lowmt.std_dev), yield_qcd_ss_lowmt)
			if yield_qcd_ss_lowmt.nominal_value == 0.0:
				log.warning("W+jets & QCD estimation: data yield in low mT SS region after background subtraction is 0!")
			
			integral_shape = tools.PoissonYield(plotData.plotdict["root_objects"][qcd_shape_nick])()
			if integral_shape != 0.0:
				scale_factor = yield_qcd_ss_lowmt * qcd_extrapolation_factor_ss_os / integral_shape
				final_qcd_yield = yield_qcd_ss_lowmt * qcd_extrapolation_factor_ss_os
				plotData.plotdict["root_objects"][qcd_shape_nick].Scale(scale_factor.nominal_value)
			
			integral_shape = tools.PoissonYield(plotData.plotdict["root_objects"][qcd_ss_lowmt_nick])()
			if integral_shape != 0.0:
				scale_factor = yield_qcd_ss_lowmt / integral_shape
				plotData.plotdict["root_objects"][qcd_ss_lowmt_nick].Scale(scale_factor.nominal_value)
			
			# write relative uncertainties to metadata to pick them up with combine
			plotData.metadata[qcd_shape_nick] = {
				"yield" : final_qcd_yield.nominal_value,
				"yield_unc" : final_qcd_yield.std_dev,
				"yield_unc_rel" : abs(final_qcd_yield.std_dev/final_qcd_yield.nominal_value if final_qcd_yield.nominal_value != 0.0 else 0.0),
			}
