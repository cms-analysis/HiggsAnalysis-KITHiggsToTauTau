# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import hashlib

import ROOT

import Artus.HarryPlotter.analysisbase as analysisbase
import TauPolSoftware.TauDecaysInterface.polarisationsignalscaling as polarisationsignalscaling
import HiggsAnalysis.KITHiggsToTauTau.tools as tools


class NormalizeForPolarisation(analysisbase.AnalysisBase):
	"""Normalize zttpospol and zttnegpol histograms to same integrals at generator level."""
	
	def __init__(self):
		super(NormalizeForPolarisation, self).__init__()
	
	def modify_argument_parser(self, parser, args):
		super(NormalizeForPolarisation, self).modify_argument_parser(parser, args)
		
		self.normalize_polarisation_options = parser.add_argument_group("{} options".format(self.name()))
		self.normalize_polarisation_options.add_argument("--ztt-pos-pol-gen-nicks", type=str, nargs="+",
				help="Nick names of the histogram for the positive ZTT polarisation at generator level.")
		self.normalize_polarisation_options.add_argument("--ztt-neg-pol-gen-nicks", type=str, nargs="+",
				help="Nick names of the histogram for the negative ZTT polarisation at generator level.")
		self.normalize_polarisation_options.add_argument("--ztt-pos-pol-reco-nicks", type=str, nargs="+",
				help="Nick names of the histogram for the positive ZTT polarisation at reconstruction level.")
		self.normalize_polarisation_options.add_argument("--ztt-neg-pol-reco-nicks", type=str, nargs="+",
				help="Nick names of the histogram for the negative ZTT polarisation at reconstruction level.")
		self.normalize_polarisation_options.add_argument("--ztt-forced-gen-polarisations", type=str, nargs="+", default=[None],
				help="Enforce a certain generator polarisation for the unpolarisation step.")
		self.normalize_polarisation_options.add_argument("--ztt-pos-pol-reco-result-nicks", type=str, nargs="+", default=[None],
				help="Nick names of the resulting scaled histogram for the positive ZTT polarisation at reconstruction level. [Default: replace inputs in-place.]")
		self.normalize_polarisation_options.add_argument("--ztt-neg-pol-reco-result-nicks", type=str, nargs="+", default=[None],
				help="Nick names of the resulting scaled histogram for the negative ZTT polarisation at reconstruction level. [Default: replace inputs in-place.]")
	
	def prepare_args(self, parser, plotData):
		super(NormalizeForPolarisation, self).prepare_args(parser, plotData)
		self.prepare_list_args(plotData, ["ztt_pos_pol_gen_nicks", "ztt_neg_pol_gen_nicks", "ztt_pos_pol_reco_nicks", "ztt_neg_pol_reco_nicks", "ztt_forced_gen_polarisations", "ztt_pos_pol_reco_result_nicks", "ztt_neg_pol_reco_result_nicks"])
		
		for index, (ztt_pos_pol_reco_nick, ztt_neg_pol_reco_nick, ztt_forced_gen_polarisation, ztt_pos_pol_reco_result_nick, ztt_neg_pol_reco_result_nick) in enumerate(zip(*[plotData.plotdict[key] for key in ["ztt_pos_pol_reco_nicks", "ztt_neg_pol_reco_nicks", "ztt_forced_gen_polarisations", "ztt_pos_pol_reco_result_nicks", "ztt_neg_pol_reco_result_nicks"]])):
			
			if ztt_pos_pol_reco_result_nick is None:
				plotData.plotdict["ztt_pos_pol_reco_result_nicks"][index] = ztt_pos_pol_reco_nick
			else:
				plotData.plotdict["nicks"].insert(plotData.plotdict["nicks"].index(ztt_pos_pol_reco_nick)+1, ztt_pos_pol_reco_result_nick)
			
			if (ztt_forced_gen_polarisation is None) or (ztt_forced_gen_polarisation=="None"):
				plotData.plotdict["ztt_forced_gen_polarisations"][index] = None
			else:
				plotData.plotdict["ztt_forced_gen_polarisations"][index] = float(ztt_forced_gen_polarisation)
			
			if ztt_neg_pol_reco_result_nick is None:
				plotData.plotdict["ztt_neg_pol_reco_result_nicks"][index] = ztt_neg_pol_reco_nick
			else:
				plotData.plotdict["nicks"].insert(plotData.plotdict["nicks"].index(ztt_neg_pol_reco_nick)+1, ztt_neg_pol_reco_result_nick)
	
	def run(self, plotData=None):
		super(NormalizeForPolarisation, self).run(plotData)
		
		for ztt_pos_pol_gen_nick, ztt_neg_pol_gen_nick, ztt_pos_pol_reco_nick, ztt_neg_pol_reco_nick, ztt_forced_gen_polarisation, ztt_pos_pol_reco_result_nick, ztt_neg_pol_reco_result_nick in zip(*[plotData.plotdict[key] for key in ["ztt_pos_pol_gen_nicks", "ztt_neg_pol_gen_nicks", "ztt_pos_pol_reco_nicks", "ztt_neg_pol_reco_nicks", "ztt_forced_gen_polarisations", "ztt_pos_pol_reco_result_nicks", "ztt_neg_pol_reco_result_nicks"]]):
			
			if ztt_pos_pol_reco_result_nick != ztt_pos_pol_reco_nick:
				new_name = "zttpospol_"+hashlib.md5(ztt_pos_pol_gen_nick+ztt_pos_pol_reco_nick+ztt_pos_pol_reco_result_nick).hexdigest()
				new_histogram = plotData.plotdict["root_objects"][ztt_pos_pol_reco_nick].Clone(new_name)
				plotData.plotdict["root_objects"][ztt_pos_pol_reco_result_nick] = new_histogram
			
			if ztt_neg_pol_reco_result_nick != ztt_neg_pol_reco_nick:
				new_name = "zttnegpol_"+hashlib.md5(ztt_neg_pol_gen_nick+ztt_neg_pol_reco_nick+ztt_neg_pol_reco_result_nick).hexdigest()
				new_histogram = plotData.plotdict["root_objects"][ztt_neg_pol_reco_nick].Clone(new_name)
				plotData.plotdict["root_objects"][ztt_neg_pol_reco_result_nick] = new_histogram
			
			pos_reco_norm = tools.PoissonYield(plotData.plotdict["root_objects"][ztt_pos_pol_reco_nick])()
			neg_reco_norm = tools.PoissonYield(plotData.plotdict["root_objects"][ztt_neg_pol_reco_nick])()
			pos_gen_norm = tools.PoissonYield(plotData.plotdict["root_objects"][ztt_pos_pol_gen_nick])()
			neg_gen_norm = tools.PoissonYield(plotData.plotdict["root_objects"][ztt_neg_pol_gen_nick])()
			
			scale_factors = polarisationsignalscaling.PolarisationScaleFactors(pos_reco_norm, neg_reco_norm, pos_gen_norm, neg_gen_norm, forced_gen_polarisation=ztt_forced_gen_polarisation)
			log.debug("Gen.  level polarisation = {polarisation}".format(polarisation=scale_factors.get_gen_polarisation()))
			log.debug("Reco. level polarisation = {polarisation}".format(polarisation=scale_factors.get_reco_polarisation()))
			
			pos_reco_scale_factor = scale_factors.get_scale_factor_pospol()
			plotData.plotdict["root_objects"][ztt_pos_pol_reco_result_nick].Scale(pos_reco_scale_factor.nominal_value)
			log.debug("Scaled histogram \"{nick}\" by a factor of {factor}".format(nick=ztt_pos_pol_reco_result_nick, factor=pos_reco_scale_factor))
			
			neg_reco_scale_factor = scale_factors.get_scale_factor_negpol()
			plotData.plotdict["root_objects"][ztt_neg_pol_reco_result_nick].Scale(neg_reco_scale_factor.nominal_value)
			log.debug("Scaled histogram \"{nick}\" by a factor of {factor}".format(nick=ztt_neg_pol_reco_result_nick, factor=neg_reco_scale_factor))
			
			if log.isEnabledFor(logging.DEBUG):
				reco_polarisation_before_scaling = (pos_reco_norm - neg_reco_norm) / (pos_reco_norm + neg_reco_norm)
				reco_polarisation_after_scaling = (pos_reco_norm*pos_reco_scale_factor - neg_reco_norm*neg_reco_scale_factor) / (pos_reco_norm*pos_reco_scale_factor + neg_reco_norm*neg_reco_scale_factor)
				log.debug("Tau polarisation changed from {before} to {after}.".format(before=reco_polarisation_before_scaling, after=reco_polarisation_after_scaling))
				
				# gen_polarisation_before_scaling = (pos_gen_norm - neg_gen_norm) / (pos_gen_norm + neg_gen_norm)
				# gen_polarisation_after_scaling = (pos_gen_norm*pos_reco_scale_factor - neg_gen_norm*neg_reco_scale_factor) / (pos_gen_norm*pos_reco_scale_factor + neg_gen_norm*neg_reco_scale_factor)
				# log.debug("Tau polarisation changed from {before} to {after} (on GEN level).".format(before=gen_polarisation_before_scaling, after=gen_polarisation_after_scaling))

