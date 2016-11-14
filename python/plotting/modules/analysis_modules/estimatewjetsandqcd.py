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
		self.estimate_wjets_and_qcd_options.add_argument("--wjets-ss-mc-nicks", nargs="+", default=[""],
				help="Nicks for inclusive ss W+jets histogram. [Default: %(default)s]")
		self.estimate_wjets_and_qcd_options.add_argument("--wjets-os-mc-nicks", nargs="+", default=[""],
				help="Nicks for inclusive os W+jets histogram. [Default: %(default)s]")
		self.estimate_wjets_and_qcd_options.add_argument("--wjets-os-highmt-mc-nicks", nargs="+", default=[""],
				help="Nicks for highmt os W+jets histogram. [Default: %(default)s]")
		self.estimate_wjets_and_qcd_options.add_argument("--wjets-ss-highmt-mc-nicks", nargs="+", default=[""],
				help="Nicks for highmt ss W+jets histogram. [Default: %(default)s]")
		self.estimate_wjets_and_qcd_options.add_argument("--wjets-os-lowmt-mc-nicks", nargs="+", default=[""],
				help="Nicks for lowmt os W+jets histogram. [Default: %(default)s]")
		self.estimate_wjets_and_qcd_options.add_argument("--wjets-ss-data-nicks", nargs="+", default=[""],
				help="Nicks for ss highmt data histogram. [Default: %(default)s]")
		self.estimate_wjets_and_qcd_options.add_argument("--wjets-os-data-nicks", nargs="+", default=[""],
				help="Nicks for os highmt data histogram. [Default: %(default)s]")
		self.estimate_wjets_and_qcd_options.add_argument("--wjets-shape-nicks", nargs="+", default=[""],
				help="Nicks for W+jets signal region histogram. [Default: %(default)s]")
		self.estimate_wjets_and_qcd_options.add_argument("--wjets-wj-final-selection", nargs="+", default=[""],
				help="Nicks for W+jets in final category. [Default: %(default)s]")

	def prepare_args(self, parser, plotData):
		super(EstimateWjetsAndQCD, self).prepare_args(parser, plotData)
		self._plotdict_keys = ["qcd_extrapolation_factors_ss_os", "qcd_shape_nicks", "qcd_ss_lowmt_nicks", "qcd_ss_highmt_shape_nicks", "qcd_os_highmt_nicks", "qcd_shape_highmt_substract_nicks", "qcd_yield_nicks", "qcd_shape_substract_nicks", "qcd_yield_substract_nicks", "wjets_ss_mc_nicks", "wjets_os_mc_nicks", "wjets_os_highmt_mc_nicks", "wjets_os_lowmt_mc_nicks", "wjets_ss_highmt_mc_nicks", "wjets_ss_substract_nicks", "wjets_ss_data_nicks", "wjets_os_substract_nicks", "wjets_os_data_nicks", "wjets_shape_nicks", "wjets_wj_final_selection"]
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

	def run(self, plotData=None):
		super(EstimateWjetsAndQCD, self).run(plotData)

		for qcd_extrapolation_factor_ss_os, qcd_shape_nick, qcd_ss_lowmt_nick, qcd_ss_highmt_shape_nick, qcd_os_highmt_nick, qcd_shape_highmt_substract_nick, qcd_yield_nick, qcd_shape_substract_nick, qcd_yield_substract_nick, wjets_ss_mc_nick, wjets_os_mc_nick, wjets_os_highmt_mc_nick, wjets_os_lowmt_mc_nick, wjets_ss_highmt_mc_nick, wjets_ss_substract_nick, wjets_ss_data_nick, wjets_os_substract_nick, wjets_os_data_nick, wjets_shape_nick, wjets_final_selection in zip(*[plotData.plotdict[key] for key in self._plotdict_keys]):
			# estimate QCD for the lowmT
			for nick in qcd_shape_substract_nick:
				plotData.plotdict["root_objects"][qcd_shape_nick].Add(plotData.plotdict["root_objects"][nick], -1)
			yield_qcd_control = tools.PoissonYield(plotData.plotdict["root_objects"][qcd_yield_nick])()
			for nick in qcd_yield_substract_nick:
				yield_bkg_control = tools.PoissonYield(plotData.plotdict["root_objects"][nick])()
				if nick in plotData.metadata:
					yield_bkg_control = uncertainties.ufloat(
							plotData.metadata[nick].get("yield", yield_bkg_control.nominal_value),
							plotData.metadata[nick].get("yield_unc", yield_bkg_control.std_dev)
					)
				yield_qcd_control -= yield_bkg_control
			yield_qcd_control = max(0.0, yield_qcd_control)

			integral_shape = tools.PoissonYield(plotData.plotdict["root_objects"][qcd_shape_nick])()
			if integral_shape != 0.0:
				scale_factor = yield_qcd_control * qcd_extrapolation_factor_ss_os / integral_shape
				plotData.plotdict["root_objects"][qcd_shape_nick].Scale(scale_factor.nominal_value)

			integral_shape = tools.PoissonYield(plotData.plotdict["root_objects"][qcd_ss_lowmt_nick])()
			if integral_shape != 0.0:
				scale_factor = yield_qcd_control / integral_shape
				plotData.plotdict["root_objects"][qcd_ss_lowmt_nick].Scale(scale_factor.nominal_value)

			# estimate W+jets
			yield_ss_control = tools.PoissonYield(plotData.plotdict["root_objects"][wjets_ss_data_nick])()
			for nick in wjets_ss_substract_nick:
				yield_bkg_control = tools.PoissonYield(plotData.plotdict["root_objects"][nick])()
				yield_ss_control -= yield_bkg_control
			yield_os_control = tools.PoissonYield(plotData.plotdict["root_objects"][wjets_os_data_nick])()
			for nick in wjets_os_substract_nick:
				yield_bkg_control = tools.PoissonYield(plotData.plotdict["root_objects"][nick])()
				yield_os_control -= yield_bkg_control

			wjets_extrapolation_factor_ss_os = tools.PoissonYield(plotData.plotdict["root_objects"][wjets_os_mc_nick])()/tools.PoissonYield(plotData.plotdict["root_objects"][wjets_ss_mc_nick])()
			wjets_extrapolation_factor_mt = tools.PoissonYield(plotData.plotdict["root_objects"][wjets_os_lowmt_mc_nick])()/tools.PoissonYield(plotData.plotdict["root_objects"][wjets_os_highmt_mc_nick])()

			wjets_yield = (yield_os_control-qcd_extrapolation_factor_ss_os*yield_ss_control)*wjets_extrapolation_factor_ss_os/(wjets_extrapolation_factor_ss_os-qcd_extrapolation_factor_ss_os)*wjets_extrapolation_factor_mt
			# extrapolate to final selection
			wjets_yield = wjets_yield * tools.PoissonYield(plotData.plotdict["root_objects"][wjets_final_selection])() / tools.PoissonYield(plotData.plotdict["root_objects"][wjets_os_lowmt_mc_nick])()

			# scale signal region histograms
			integral_shape = tools.PoissonYield(plotData.plotdict["root_objects"][wjets_shape_nick])()
			if integral_shape != 0.0:
				scale_factor = wjets_yield / integral_shape
				log.debug("Scale factor for process W+jets (nick \"{nick}\") is {scale_factor}.".format(nick=wjets_shape_nick, scale_factor=scale_factor))
				plotData.plotdict["root_objects"][wjets_shape_nick].Scale(scale_factor.nominal_value)

			integral_shape = tools.PoissonYield(plotData.plotdict["root_objects"][wjets_os_highmt_mc_nick])()
			if integral_shape != 0.0:
				scale_factor = wjets_yield / (integral_shape * wjets_extrapolation_factor_mt)
				log.debug("Scale factor for process W+jets (nick \"{nick}\") is {scale_factor}.".format(nick=wjets_os_highmt_mc_nick, scale_factor=scale_factor))
				plotData.plotdict["root_objects"][wjets_os_highmt_mc_nick].Scale(scale_factor.nominal_value)

			integral_shape = tools.PoissonYield(plotData.plotdict["root_objects"][wjets_ss_highmt_mc_nick])()
			if integral_shape != 0.0:
				scale_factor = wjets_yield / (integral_shape * wjets_extrapolation_factor_mt * wjets_extrapolation_factor_ss_os)
				log.debug("Scale factor for process W+jets (nick \"{nick}\") is {scale_factor}.".format(nick=wjets_ss_highmt_mc_nick, scale_factor=scale_factor))
				plotData.plotdict["root_objects"][wjets_ss_highmt_mc_nick].Scale(scale_factor.nominal_value)


			# estimate QCD for the highmT region
			for nick in qcd_shape_highmt_substract_nick+[wjets_ss_highmt_mc_nick]:
				plotData.plotdict["root_objects"][qcd_ss_highmt_shape_nick].Add(plotData.plotdict["root_objects"][nick], -1)

			yield_qcd_ss_highmt = yield_ss_control - tools.PoissonYield(plotData.plotdict["root_objects"][wjets_ss_highmt_mc_nick])()
			yield_qcd_ss_highmt = max(0.0, yield_qcd_ss_highmt)

			integral_shape = tools.PoissonYield(plotData.plotdict["root_objects"][qcd_ss_highmt_shape_nick])()
			if integral_shape != 0.0:
				scale_factor = yield_qcd_ss_highmt / integral_shape
				plotData.plotdict["root_objects"][qcd_ss_highmt_shape_nick].Scale(scale_factor.nominal_value)

			integral_shape = tools.PoissonYield(plotData.plotdict["root_objects"][qcd_os_highmt_nick])()
			if integral_shape != 0.0:
				scale_factor = yield_qcd_ss_highmt * qcd_extrapolation_factor_ss_os / integral_shape
				plotData.plotdict["root_objects"][qcd_os_highmt_nick].Scale(scale_factor.nominal_value)
