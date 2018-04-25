# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import ROOT

import Artus.HarryPlotter.analysisbase as analysisbase
import CombineHarvester.ZTTPOL2016.polarisationsignalscaling as polarisationsignalscaling


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
	
	def prepare_args(self, parser, plotData):
		super(NormalizeForPolarisation, self).prepare_args(parser, plotData)
		self.prepare_list_args(plotData, ["ztt_pos_pol_gen_nicks", "ztt_neg_pol_gen_nicks", "ztt_pos_pol_reco_nicks", "ztt_neg_pol_reco_nicks"])
	
	def run(self, plotData=None):
		super(NormalizeForPolarisation, self).run(plotData)
		
		for ztt_pos_pol_gen_nick, ztt_neg_pol_gen_nick, ztt_pos_pol_reco_nick, ztt_neg_pol_reco_nick in zip(*[plotData.plotdict[key] for key in ["ztt_pos_pol_gen_nicks", "ztt_neg_pol_gen_nicks", "ztt_pos_pol_reco_nicks", "ztt_neg_pol_reco_nicks"]]):
			
			pos_reco_norm = plotData.plotdict["root_objects"][ztt_pos_pol_reco_nick].Integral()
			neg_reco_norm = plotData.plotdict["root_objects"][ztt_neg_pol_reco_nick].Integral()
			pos_gen_norm = plotData.plotdict["root_objects"][ztt_pos_pol_gen_nick].Integral()
			neg_gen_norm = plotData.plotdict["root_objects"][ztt_neg_pol_gen_nick].Integral()
			
			scale_factors = polarisationsignalscaling.PolarisationScaleFactors(pos_reco_norm, neg_reco_norm, pos_gen_norm, neg_gen_norm)
			
			pos_reco_scale_factor = scale_factors.get_scale_factor_pospol()
			plotData.plotdict["root_objects"][ztt_pos_pol_reco_nick].Scale(pos_reco_scale_factor)
			log.debug("Scaled histogram \"%s\" by a factor of %f" % (ztt_pos_pol_reco_nick, pos_reco_scale_factor))
			
			neg_reco_scale_factor = scale_factors.get_scale_factor_negpol()
			plotData.plotdict["root_objects"][ztt_neg_pol_reco_nick].Scale(neg_reco_scale_factor)
			log.debug("Scaled histogram \"%s\" by a factor of %f" % (ztt_neg_pol_reco_nick, neg_reco_scale_factor))

