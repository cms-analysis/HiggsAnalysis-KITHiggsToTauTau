# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import ROOT

import Artus.HarryPlotter.analysisbase as analysisbase


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
	
	def normalize_histogram(self, refhisto_nicks, nicks_to_normalize, plotData=None ):
		for refhisto, histos_to_normalize in zip(refhisto_nicks, nicks_to_normalize):
			refhisto_int = plotData.plotdict["root_objects"][refhisto].Integral()

			for histo_to_normalize in histos_to_normalize.split(" "):
				root_histogram = plotData.plotdict["root_objects"][histo_to_normalize]
				if isinstance(root_histogram, ROOT.TH1):
					root_histogram.Sumw2()
					if root_histogram.Integral() != 0.0:
						log.debug("{0}: Scaling histogram {1} by {2}".format(self.name(), histo_to_normalize, (refhisto_int / root_histogram.Integral())))
						root_histogram.Scale(refhisto_int / root_histogram.Integral())

	def run(self, plotData=None):
		super(NormalizeForPolarisation, self).run(plotData)
		
		for ztt_pos_pol_gen_nick, ztt_neg_pol_gen_nick, ztt_pos_pol_reco_nick, ztt_neg_pol_reco_nick in zip(*[plotData.plotdict[key] for key in ["ztt_pos_pol_gen_nicks", "ztt_neg_pol_gen_nicks", "ztt_pos_pol_reco_nicks", "ztt_neg_pol_reco_nicks"]]):
			
			ztt_pos_pol_gen_norm = plotData.plotdict["root_objects"][ztt_pos_pol_gen_nick].Integral()
			ztt_neg_pol_gen_norm = plotData.plotdict["root_objects"][ztt_neg_pol_gen_nick].Integral()
			ztt_gen_norm = ztt_pos_pol_gen_norm + ztt_neg_pol_gen_norm
			
			integral_preserving_scale_factor = 1.0
			if True: # TODO: control via program option
				ztt_pos_pol_reco_norm = plotData.plotdict["root_objects"][ztt_pos_pol_reco_nick].Integral()
				ztt_neg_pol_reco_norm = plotData.plotdict["root_objects"][ztt_neg_pol_reco_nick].Integral()
				
				if ((ztt_pos_pol_gen_norm != 0.0) and (ztt_neg_pol_gen_norm != 0.0)):
					denominator = 0.5 * (ztt_gen_norm) * ((ztt_pos_pol_reco_norm / ztt_pos_pol_gen_norm) + (ztt_neg_pol_reco_norm / ztt_neg_pol_gen_norm))
					if denominator != 0.0:
						integral_preserving_scale_factor = (ztt_pos_pol_reco_norm + ztt_neg_pol_reco_norm) / denominator
			
			if (ztt_pos_pol_gen_norm != 0.0):
				ztt_pos_pol_reco_scale_factor = integral_preserving_scale_factor * 0.5 * ztt_gen_norm / ztt_pos_pol_gen_norm
				plotData.plotdict["root_objects"][ztt_pos_pol_reco_nick].Scale(ztt_pos_pol_reco_scale_factor)
				log.debug("Scaled histogram \"%s\" by a factor of %f" % (ztt_pos_pol_reco_nick, ztt_pos_pol_reco_scale_factor))
			
			if (ztt_neg_pol_gen_norm != 0.0):
				ztt_neg_pol_reco_scale_factor = integral_preserving_scale_factor * 0.5 * ztt_gen_norm / ztt_neg_pol_gen_norm
				plotData.plotdict["root_objects"][ztt_neg_pol_reco_nick].Scale(ztt_neg_pol_reco_scale_factor)
				log.debug("Scaled histogram \"%s\" by a factor of %f" % (ztt_neg_pol_reco_nick, ztt_neg_pol_reco_scale_factor))

