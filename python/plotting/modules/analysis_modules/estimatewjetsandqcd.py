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
		self.estimate_wjets_and_qcd_options.add_argument("--wjets-ss-lowmt-mc-nicks", nargs="+", default=[""],
				help="Nicks for lowmt os W+jets histogram. [Default: %(default)s]")
		self.estimate_wjets_and_qcd_options.add_argument("--wjets-ss-data-nicks", nargs="+", default=[""],
				help="Nicks for ss highmt data histogram. [Default: %(default)s]")
		self.estimate_wjets_and_qcd_options.add_argument("--wjets-os-data-nicks", nargs="+", default=[""],
				help="Nicks for os highmt data histogram. [Default: %(default)s]")
		self.estimate_wjets_and_qcd_options.add_argument("--wjets-shape-nicks", nargs="+", default=[""],
				help="Nicks for W+jets signal region histogram. [Default: %(default)s]")
		self.estimate_wjets_and_qcd_options.add_argument("--wjets-wj-final-selection", nargs="+", default=[""],
				help="Nicks for W+jets in final category. [Default: %(default)s]")
		self.estimate_wjets_and_qcd_options.add_argument("--wjets-relaxed-ss-wj-nicks", nargs="+", default=[""],
				help="Nicks for W+jets in relaxed ss category. [Default: %(default)s]")
		self.estimate_wjets_and_qcd_options.add_argument("--wjets-relaxed-ss-data-nicks", nargs="+", default=[""],
				help="Nicks for data in relaxed ss category. [Default: %(default)s]")
		self.estimate_wjets_and_qcd_options.add_argument("--wjets-relaxed-ss-subtract-nicks", nargs="+", default=[""],
				help="Nicks for subtraction from data in relaxed ss category. [Default: %(default)s]")
		self.estimate_wjets_and_qcd_options.add_argument("--wjets-relaxed-os-lowmt-wj-nicks", nargs="+", default=[""],
				help="Nicks for W+jets in relaxed os lowmt category. [Default: %(default)s]")
		self.estimate_wjets_and_qcd_options.add_argument("--wjets-relaxed-os-wj-nicks", nargs="+", default=[""],
				help="Nicks for W+jets in relaxed os category. [Default: %(default)s]")
		self.estimate_wjets_and_qcd_options.add_argument("--wjets-relaxed-os-data-nicks", nargs="+", default=[""],
				help="Nicks for data in relaxed os category. [Default: %(default)s]")
		self.estimate_wjets_and_qcd_options.add_argument("--wjets-relaxed-os-subtract-nicks", nargs="+", default=[""],
				help="Nicks for subtraction from data in relaxed os category. [Default: %(default)s]")
		self.estimate_wjets_and_qcd_options.add_argument("--wjets-relaxed-os-highmt-mc-nicks", nargs="+", default=[""],
				help="Nicks for W+jets in relaxed os highmt category. [Default: %(default)s]")

	def prepare_args(self, parser, plotData):
		super(EstimateWjetsAndQCD, self).prepare_args(parser, plotData)
		self._plotdict_keys = ["qcd_extrapolation_factors_ss_os", "qcd_shape_nicks", "qcd_ss_lowmt_nicks", "qcd_ss_highmt_shape_nicks", "qcd_os_highmt_nicks", "qcd_shape_highmt_substract_nicks", "qcd_yield_nicks", "qcd_shape_substract_nicks", "qcd_yield_substract_nicks", "wjets_ss_mc_nicks", "wjets_os_mc_nicks", "wjets_os_highmt_mc_nicks", "wjets_os_lowmt_mc_nicks", "wjets_ss_lowmt_mc_nicks", "wjets_ss_highmt_mc_nicks", "wjets_ss_substract_nicks", "wjets_ss_data_nicks", "wjets_os_substract_nicks", "wjets_os_data_nicks", "wjets_shape_nicks"]
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
		self._plotdict_keys.append("wjets_relaxed_ss_wj_nicks")
		self._plotdict_keys.append("wjets_relaxed_ss_data_nicks")
		self._plotdict_keys.append("wjets_relaxed_ss_subtract_nicks")
		self._plotdict_keys.append("wjets_relaxed_os_lowmt_wj_nicks")
		self._plotdict_keys.append("wjets_relaxed_os_wj_nicks")
		self._plotdict_keys.append("wjets_relaxed_os_data_nicks")
		self._plotdict_keys.append("wjets_relaxed_os_subtract_nicks")
		self._plotdict_keys.append("wjets_relaxed_os_highmt_mc_nicks")
		for index in ["wjets_relaxed_os_subtract_nicks", "wjets_relaxed_ss_subtract_nicks"]:
			if plotData.plotdict[index] != [None]:
				plotData.plotdict[index] = [nicks.split() for nicks in plotData.plotdict[index]]

	def run(self, plotData=None):
		super(EstimateWjetsAndQCD, self).run(plotData)


		for qcd_extrapolation_factor_ss_os, qcd_shape_nick, qcd_ss_lowmt_nick, qcd_ss_highmt_shape_nick, qcd_os_highmt_nick, qcd_shape_highmt_substract_nick, qcd_yield_nick, qcd_shape_substract_nick, qcd_yield_substract_nick, wjets_ss_mc_nick, wjets_os_mc_nick, wjets_os_highmt_mc_nick, wjets_os_lowmt_mc_nick, wjets_ss_lowmt_mc_nick, wjets_ss_highmt_mc_nick, wjets_ss_substract_nick, wjets_ss_data_nick, wjets_os_substract_nick, wjets_os_data_nick, wjets_shape_nick, wjets_final_selection, wjets_relaxed_ss_wj_nick, wjets_relaxed_ss_data_nick, wjets_relaxed_ss_subtract_nick, wjets_relaxed_os_lowmt_wj_nick, wjets_relaxed_os_wj_nick, wjets_relaxed_os_data_nick, wjets_relaxed_os_subtract_nick, wjets_relaxed_os_highmt_mc_nick in zip(*[plotData.plotdict[key] for key in self._plotdict_keys]):
			if (wjets_relaxed_ss_wj_nick and wjets_relaxed_ss_data_nick and wjets_relaxed_ss_subtract_nick and wjets_relaxed_os_wj_nick and wjets_relaxed_os_data_nick and wjets_relaxed_os_subtract_nick):
				# estimate W+jets
				yield_ss_control = tools.PoissonYield(plotData.plotdict["root_objects"][wjets_ss_data_nick])()
				print "ss control ", yield_ss_control
				for nick in wjets_ss_substract_nick:
					yield_bkg_control = tools.PoissonYield(plotData.plotdict["root_objects"][nick])()
					print nick, " ", yield_bkg_control
					yield_ss_control -= yield_bkg_control
				print "ss control ", yield_ss_control
				yield_relaxed_ss_control = tools.PoissonYield(plotData.plotdict["root_objects"][wjets_relaxed_ss_data_nick])()
				print "----"
				print "ss relaxed control ", yield_relaxed_ss_control
				for nick in wjets_relaxed_ss_subtract_nick:
					yield_bkg_control = tools.PoissonYield(plotData.plotdict["root_objects"][nick])()
					print nick, " ", yield_bkg_control
					yield_relaxed_ss_control -= yield_bkg_control
				print "ss relaxed control ", yield_relaxed_ss_control
				yield_relaxed_os_control = tools.PoissonYield(plotData.plotdict["root_objects"][wjets_relaxed_os_data_nick])()
				print "----"
				print "os relaxed control ", yield_relaxed_os_control
				for nick in wjets_relaxed_os_subtract_nick:
					yield_bkg_control = tools.PoissonYield(plotData.plotdict["root_objects"][nick])()
					print nick, " ", yield_bkg_control
					yield_relaxed_os_control -= yield_bkg_control
				print "os relaxed control ", yield_relaxed_os_control

				wjets_extrapolation_factor_ss_os = tools.PoissonYield(plotData.plotdict["root_objects"][wjets_os_mc_nick])()/tools.PoissonYield(plotData.plotdict["root_objects"][wjets_ss_mc_nick])()
				if wjets_relaxed_os_highmt_mc_nick:
					wjets_extrapolation_factor_mt = tools.PoissonYield(plotData.plotdict["root_objects"][wjets_os_lowmt_mc_nick])()/tools.PoissonYield(plotData.plotdict["root_objects"][wjets_relaxed_os_highmt_mc_nick])()
				else:
					wjets_extrapolation_factor_mt = tools.PoissonYield(plotData.plotdict["root_objects"][wjets_os_lowmt_mc_nick])()/tools.PoissonYield(plotData.plotdict["root_objects"][wjets_os_highmt_mc_nick])()
				print "wj os ", tools.PoissonYield(plotData.plotdict["root_objects"][wjets_os_mc_nick])()
				print "wj ss ", tools.PoissonYield(plotData.plotdict["root_objects"][wjets_ss_mc_nick])()
				print "os/ss factor ", wjets_extrapolation_factor_ss_os
				print "wj lowmt ", tools.PoissonYield(plotData.plotdict["root_objects"][wjets_os_lowmt_mc_nick])()
				print "wj highmt ", tools.PoissonYield(plotData.plotdict["root_objects"][wjets_os_highmt_mc_nick])()
				print "mt factor ", wjets_extrapolation_factor_mt
				
				wjets_extrapolation_factor_relaxed_highmt = tools.PoissonYield(plotData.plotdict["root_objects"][wjets_os_highmt_mc_nick])()/tools.PoissonYield(plotData.plotdict["root_objects"][wjets_relaxed_os_wj_nick])()
				wjets_extrapolation_factor_relaxed_lowmt = tools.PoissonYield(plotData.plotdict["root_objects"][wjets_shape_nick])()/tools.PoissonYield(plotData.plotdict["root_objects"][wjets_relaxed_os_lowmt_wj_nick])()
				print "relaxed highmt factor ", wjets_extrapolation_factor_relaxed_highmt
				print "relaxed lowmt factor ", wjets_extrapolation_factor_relaxed_lowmt

				wjets_yield_relaxed_ss_highmt = (yield_relaxed_os_control-qcd_extrapolation_factor_ss_os*yield_relaxed_ss_control)/(wjets_extrapolation_factor_ss_os-qcd_extrapolation_factor_ss_os)
				wjets_yield_relaxed_os_highmt = wjets_yield_relaxed_ss_highmt*wjets_extrapolation_factor_ss_os
				print "wjets yield relaxed os highmt", wjets_yield_relaxed_os_highmt
				print "wjets yield relaxed ss highmt", wjets_yield_relaxed_ss_highmt

				wjets_yield_ss_highmt = wjets_yield_relaxed_ss_highmt*wjets_extrapolation_factor_relaxed_highmt
				wjets_yield_os_highmt = wjets_yield_relaxed_os_highmt*wjets_extrapolation_factor_relaxed_highmt
				wjets_yield_ss_lowmt = wjets_yield_ss_highmt*wjets_extrapolation_factor_mt
				wjets_yield_os_lowmt = wjets_yield_os_highmt*wjets_extrapolation_factor_mt
				print "wjets yield os highmt", wjets_yield_os_highmt
				print "wjets yield ss highmt", wjets_yield_ss_highmt
				print "wjets yield os lowmt", wjets_yield_os_lowmt
				print "wjets yield ss lowmt", wjets_yield_ss_lowmt
			else:
				# estimate W+jets
				yield_ss_control = tools.PoissonYield(plotData.plotdict["root_objects"][wjets_ss_data_nick])()
				print "ss control ", yield_ss_control
				for nick in wjets_ss_substract_nick:
					yield_bkg_control = tools.PoissonYield(plotData.plotdict["root_objects"][nick])()
					print nick, " ", yield_bkg_control
					yield_ss_control -= yield_bkg_control
				print "ss control ", yield_ss_control
				yield_os_control = tools.PoissonYield(plotData.plotdict["root_objects"][wjets_os_data_nick])()
				print "----"
				print "os control ", yield_os_control
				for nick in wjets_os_substract_nick:
					yield_bkg_control = tools.PoissonYield(plotData.plotdict["root_objects"][nick])()
					print nick, " ", yield_bkg_control
					yield_os_control -= yield_bkg_control
				print "os control ", yield_os_control

				wjets_extrapolation_factor_ss_os = tools.PoissonYield(plotData.plotdict["root_objects"][wjets_os_mc_nick])()/tools.PoissonYield(plotData.plotdict["root_objects"][wjets_ss_mc_nick])()
				wjets_extrapolation_factor_mt = tools.PoissonYield(plotData.plotdict["root_objects"][wjets_os_lowmt_mc_nick])()/tools.PoissonYield(plotData.plotdict["root_objects"][wjets_os_highmt_mc_nick])()
				print "wj os ", tools.PoissonYield(plotData.plotdict["root_objects"][wjets_os_mc_nick])()
				print "wj ss ", tools.PoissonYield(plotData.plotdict["root_objects"][wjets_ss_mc_nick])()
				print "os/ss factor ", wjets_extrapolation_factor_ss_os
				print "wj lowmt ", tools.PoissonYield(plotData.plotdict["root_objects"][wjets_os_lowmt_mc_nick])()
				print "wj highmt ", tools.PoissonYield(plotData.plotdict["root_objects"][wjets_os_highmt_mc_nick])()
				print "mt factor ", wjets_extrapolation_factor_mt

				wjets_yield_ss_highmt = (yield_os_control-qcd_extrapolation_factor_ss_os*yield_ss_control)/(wjets_extrapolation_factor_ss_os-qcd_extrapolation_factor_ss_os)
				wjets_yield_os_highmt = wjets_yield_ss_highmt*wjets_extrapolation_factor_ss_os
				wjets_yield_ss_lowmt = wjets_yield_ss_highmt*wjets_extrapolation_factor_mt
				wjets_yield_os_lowmt = wjets_yield_os_highmt*wjets_extrapolation_factor_mt
				print "wjets yield os highmt", wjets_yield_os_highmt
				print "wjets yield ss highmt", wjets_yield_ss_highmt
				print "wjets yield os lowmt", wjets_yield_os_lowmt
				print "wjets yield ss lowmt", wjets_yield_ss_lowmt

			# extrapolate to final selection
			if wjets_final_selection != None:
				wjets_yield_os_lowmt = wjets_yield_os_lowmt * tools.PoissonYield(plotData.plotdict["root_objects"][wjets_final_selection])() / tools.PoissonYield(plotData.plotdict["root_objects"][wjets_os_lowmt_mc_nick])()

			# rescale wjets shape for signal region
			integral_shape = tools.PoissonYield(plotData.plotdict["root_objects"][wjets_shape_nick])()
			if integral_shape != 0.0:
				scale_factor = wjets_yield_os_lowmt / integral_shape
				log.debug("Scale factor for process W+jets (nick \"{nick}\") is {scale_factor}.".format(nick=wjets_shape_nick, scale_factor=scale_factor))
				plotData.plotdict["root_objects"][wjets_shape_nick].Scale(scale_factor.nominal_value)

			# get wjets yield and shape for QCD control region (ss lowmt)
			integral_shape = tools.PoissonYield(plotData.plotdict["root_objects"][wjets_ss_lowmt_mc_nick])()
			if integral_shape != 0.0:
				scale_factor = wjets_yield_ss_lowmt / integral_shape
				log.debug("Scale factor for process W+jets (nick \"{nick}\") is {scale_factor}.".format(nick=wjets_ss_lowmt_mc_nick, scale_factor=scale_factor))
				plotData.plotdict["root_objects"][wjets_ss_lowmt_mc_nick].Scale(scale_factor.nominal_value)
			
			# estimate QCD for the lowmT
			for nick in qcd_shape_substract_nick:
				# scale up the wjets contribution to the corresponding yield. Could be done in a better way
				if "wj" in nick:
					integral_shape = tools.PoissonYield(plotData.plotdict["root_objects"][nick])()
					if integral_shape != 0.0:
						scale_factor = wjets_yield_ss_lowmt / integral_shape
						plotData.plotdict["root_objects"][nick].Scale(scale_factor.nominal_value)
				plotData.plotdict["root_objects"][qcd_shape_nick].Add(plotData.plotdict["root_objects"][nick], -1)
			yield_qcd_ss_lowmt = tools.PoissonYield(plotData.plotdict["root_objects"][qcd_yield_nick])()
			for nick in qcd_yield_substract_nick:
				yield_bkg_control = tools.PoissonYield(plotData.plotdict["root_objects"][nick])()
				if nick in plotData.metadata:
					yield_bkg_control = uncertainties.ufloat(
							plotData.metadata[nick].get("yield", yield_bkg_control.nominal_value),
							plotData.metadata[nick].get("yield_unc", yield_bkg_control.std_dev)
					)
				yield_qcd_ss_lowmt -= yield_bkg_control
			yield_qcd_ss_lowmt = max(0.0, yield_qcd_ss_lowmt)

			# scale QCD to corresponding weight
			integral_shape = tools.PoissonYield(plotData.plotdict["root_objects"][qcd_shape_nick])()
			if integral_shape != 0.0:
				scale_factor = yield_qcd_ss_lowmt * qcd_extrapolation_factor_ss_os / integral_shape
				final_qcd_yield = yield_qcd_ss_lowmt * qcd_extrapolation_factor_ss_os
				log.debug("Scale factor for process QCD (nick \"{nick}\") is {scale_factor}.".format(nick=qcd_shape_nick, scale_factor=scale_factor))
				plotData.plotdict["root_objects"][qcd_shape_nick].Scale(scale_factor.nominal_value)

			# set shape for highmt os region to the same as lowmt os
			plotData.plotdict["root_objects"][qcd_ss_lowmt_nick] = plotData.plotdict["root_objects"][qcd_shape_nick].Clone(qcd_ss_lowmt_nick)
			integral_shape = tools.PoissonYield(plotData.plotdict["root_objects"][qcd_ss_lowmt_nick])()
			if integral_shape != 0.0:
				scale_factor = yield_qcd_ss_lowmt / integral_shape
				log.debug("Scale factor for process QCD (nick \"{nick}\") is {scale_factor}.".format(nick=qcd_ss_lowmt_nick, scale_factor=scale_factor))
				plotData.plotdict["root_objects"][qcd_ss_lowmt_nick].Scale(scale_factor.nominal_value)

			# write relative uncertainties to metadata to pick them up with combine
			# plotData.metadata[qcd_shape_nick] = {
				# "yield" : final_qcd_yield.nominal_value,
				# "yield_unc" : final_qcd_yield.std_dev,
				# "yield_unc_rel" : abs(final_qcd_yield.std_dev/final_qcd_yield.nominal_value if final_qcd_yield.nominal_value != 0.0 else 0.0),
			# }



			# scale wjets in the highmt control regions
			integral_shape = tools.PoissonYield(plotData.plotdict["root_objects"][wjets_os_highmt_mc_nick])()
			if integral_shape != 0.0:
				scale_factor = wjets_yield_os_highmt / integral_shape
				log.debug("Scale factor for process W+jets (nick \"{nick}\") is {scale_factor}.".format(nick=wjets_os_highmt_mc_nick, scale_factor=scale_factor))
				plotData.plotdict["root_objects"][wjets_os_highmt_mc_nick].Scale(scale_factor.nominal_value)

			integral_shape = tools.PoissonYield(plotData.plotdict["root_objects"][wjets_ss_highmt_mc_nick])()
			if integral_shape != 0.0:
				scale_factor = wjets_yield_ss_highmt / integral_shape
				log.debug("Scale factor for process W+jets (nick \"{nick}\") is {scale_factor}.".format(nick=wjets_ss_highmt_mc_nick, scale_factor=scale_factor))
				plotData.plotdict["root_objects"][wjets_ss_highmt_mc_nick].Scale(scale_factor.nominal_value)


			# estimate QCD for the highmT control regions
			for nick in qcd_shape_highmt_substract_nick+[wjets_ss_highmt_mc_nick]:
				plotData.plotdict["root_objects"][qcd_ss_highmt_shape_nick].Add(plotData.plotdict["root_objects"][nick], -1)

			# need to fix?
			yield_qcd_ss_highmt = yield_ss_control - tools.PoissonYield(plotData.plotdict["root_objects"][wjets_ss_highmt_mc_nick])()
			yield_qcd_ss_highmt = max(0.0, yield_qcd_ss_highmt)
			yield_qcd_os_highmt = yield_qcd_ss_highmt*qcd_extrapolation_factor_ss_os

			integral_shape = tools.PoissonYield(plotData.plotdict["root_objects"][qcd_ss_highmt_shape_nick])()
			if integral_shape != 0.0:
				scale_factor = yield_qcd_ss_highmt / integral_shape
				log.debug("Scale factor for process QCD (nick \"{nick}\") is {scale_factor}.".format(nick=qcd_ss_highmt_shape_nick, scale_factor=scale_factor))
				plotData.plotdict["root_objects"][qcd_ss_highmt_shape_nick].Scale(scale_factor.nominal_value)

			# set shape for highmt os region to the same as highmt ss
			plotData.plotdict["root_objects"][qcd_os_highmt_nick] = plotData.plotdict["root_objects"][qcd_ss_highmt_shape_nick].Clone(qcd_os_highmt_nick)
			integral_shape = tools.PoissonYield(plotData.plotdict["root_objects"][qcd_os_highmt_nick])()
			if integral_shape != 0.0:
				scale_factor = yield_qcd_os_highmt / integral_shape
				log.debug("Scale factor for process QCD (nick \"{nick}\") is {scale_factor}.".format(nick=qcd_os_highmt_nick, scale_factor=scale_factor))
				plotData.plotdict["root_objects"][qcd_os_highmt_nick].Scale(scale_factor.nominal_value)

			plotData.metadata[wjets_shape_nick] = {
				"yield" : wjets_yield_os_lowmt.nominal_value,
				"yield_unc" : wjets_yield_os_lowmt.std_dev,
				"yield_unc_rel" : abs(wjets_yield_os_lowmt.std_dev/wjets_yield_os_lowmt.nominal_value if wjets_yield_os_lowmt.nominal_value != 0.0 else 0.0),
			}




