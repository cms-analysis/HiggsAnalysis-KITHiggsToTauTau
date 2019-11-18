# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import hashlib

import ROOT

import Artus.HarryPlotter.analysisbase as analysisbase
import TauPolSoftware.TauDecaysInterface.polarisationsignalscaling as polarisationsignalscaling
import HiggsAnalysis.KITHiggsToTauTau.tools as tools
import HiggsAnalysis.KITHiggsToTauTau.uncertainties.uncertainties as uncertainties


class UnpolarisationScaleFactors(analysisbase.AnalysisBase):
	"""Determine and print unpolarisation scale factors and their uncertainties."""
	
	def __init__(self):
		super(UnpolarisationScaleFactors, self).__init__()
	
	def modify_argument_parser(self, parser, args):
		super(UnpolarisationScaleFactors, self).modify_argument_parser(parser, args)
		
		self.normalize_polarisation_options = parser.add_argument_group("{} options".format(self.name()))
		self.normalize_polarisation_options.add_argument("--unpolarisation-nominal-nicks", type=str, nargs="+",
				help="Nick names of the nominal (2-bin) histogram(s).")
		self.normalize_polarisation_options.add_argument("--unpolarisation-shift-up-nicks", type=str, nargs="+",
				help="Nick names of the shift-up (2-bin) histogram(s).")
		self.normalize_polarisation_options.add_argument("--unpolarisation-shift-down-nicks", type=str, nargs="+",
				help="Nick names of the shift-down (2-bin) histogram(s).")
		self.normalize_polarisation_options.add_argument("--unpolarisation-remove-bias-instead-unpolarisation", default=False, action="store_true",
				help="Remove all polarisation effects except for the generator level polarisation. [Default: %(default)s]")
		self.normalize_polarisation_options.add_argument("--unpolarisation-forced-gen-polarisations", type=str, nargs="+", default=[None],
				help="Enforce a certain generator polarisation for the unpolarisation step.")
	
	def prepare_args(self, parser, plotData):
		super(UnpolarisationScaleFactors, self).prepare_args(parser, plotData)
		self.prepare_list_args(plotData, ["unpolarisation_nominal_nicks", "unpolarisation_shift_up_nicks", "unpolarisation_shift_down_nicks", "unpolarisation_forced_gen_polarisations"])
		
		for index, unpolarisation_forced_gen_polarisation in enumerate(plotData.plotdict["unpolarisation_forced_gen_polarisations"]):
			if (unpolarisation_forced_gen_polarisation is None) or (unpolarisation_forced_gen_polarisation=="None"):
				plotData.plotdict["unpolarisation_forced_gen_polarisations"][index] = None
			else:
				plotData.plotdict["unpolarisation_forced_gen_polarisations"][index] = float(unpolarisation_forced_gen_polarisation)
	
	def run(self, plotData=None):
		super(UnpolarisationScaleFactors, self).run(plotData)
		
		for unpolarisation_nominal_nick, unpolarisation_shift_up_nick, unpolarisation_shift_down_nick, unpolarisation_forced_gen_polarisation in zip(*[plotData.plotdict[key] for key in ["unpolarisation_nominal_nicks", "unpolarisation_shift_up_nicks", "unpolarisation_shift_down_nicks", "unpolarisation_forced_gen_polarisations"]]):
		
			scale_factors = {}
			scale_factors_pos = {}
			scale_factors_neg = {}
			for shift, nick in zip(*[["nominal", "shift up", "shift down"], [unpolarisation_nominal_nick, unpolarisation_shift_up_nick, unpolarisation_shift_down_nick]]):
				neg_gen_norm = uncertainties.ufloat(
						plotData.plotdict["root_objects"][nick].GetBinContent(1),
						plotData.plotdict["root_objects"][nick].GetBinError(1)
				)
				pos_gen_norm = uncertainties.ufloat(
						plotData.plotdict["root_objects"][nick].GetBinContent(2),
						plotData.plotdict["root_objects"][nick].GetBinError(2)
				)
				scale_factors[shift] = polarisationsignalscaling.PolarisationScaleFactors(pos_gen_norm, neg_gen_norm, pos_gen_norm, neg_gen_norm, forced_gen_polarisation=unpolarisation_forced_gen_polarisation)
				
				scale_factors_pos[shift] = scale_factors[shift].get_bias_removal_factor_pospol() if plotData.plotdict["unpolarisation_remove_bias_instead_unpolarisation"] else scale_factors[shift].get_scale_factor_pospol()
				log.debug("Positive helicity of \"{nick}\" to be scaled by a factor of {factor} ({shift}).".format(
						nick=nick,
						factor=scale_factors_pos[shift],
						shift=shift
				))
				
				scale_factors_neg[shift] = scale_factors[shift].get_bias_removal_factor_neg_pol() if plotData.plotdict["unpolarisation_remove_bias_instead_unpolarisation"] else scale_factors[shift].get_scale_factor_negpol()
				log.debug("Negative helicity of \"{nick}\" to be scaled by a factor of {factor} ({shift}).".format(
						nick=nick,
						factor=scale_factors_neg[shift],
						shift=shift
				))
			
			total_uncertainties_pos = [abs((scale_factors_pos["shift up"]-scale_factors_pos["nominal"])/scale_factors_pos["nominal"]),
			                           abs((scale_factors_pos["shift down"]-scale_factors_pos["nominal"])/scale_factors_pos["nominal"])]
			total_uncertainties_neg = [abs((scale_factors_neg["shift up"]-scale_factors_neg["nominal"])/scale_factors_neg["nominal"]),
			                           abs((scale_factors_neg["shift down"]-scale_factors_neg["nominal"])/scale_factors_neg["nominal"])]
			
			log.info("Total uncertainties on scale factor for positive helicity = (+) {tot_pos_plus} / (-) {tot_pos_minus}".format(
					tot_pos_plus=total_uncertainties_pos[0],
					tot_pos_minus=total_uncertainties_pos[1]
			))
			log.info("Total uncertainties on scale factor for negative helicity = (+) {tot_neg_plus} / (-) {tot_neg_minus}".format(
					tot_neg_plus=total_uncertainties_neg[0],
					tot_neg_minus=total_uncertainties_neg[1]
			))
