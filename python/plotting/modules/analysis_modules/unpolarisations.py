# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import hashlib
import math

import ROOT

import Artus.HarryPlotter.analysisbase as analysisbase
import TauPolSoftware.TauDecaysInterface.polarisationsignalscaling as polarisationsignalscaling
import HiggsAnalysis.KITHiggsToTauTau.tools as tools
import HiggsAnalysis.KITHiggsToTauTau.uncertainties.uncertainties as uncertainties


class Unpolarisation(analysisbase.AnalysisBase):
	"""Determine unpolarisation scale factors and their uncertainties differentially."""
	
	def __init__(self):
		super(Unpolarisation, self).__init__()
	
	def modify_argument_parser(self, parser, args):
		super(Unpolarisation, self).modify_argument_parser(parser, args)
		
		self.normalize_polarisation_options = parser.add_argument_group("{} options".format(self.name()))
		self.normalize_polarisation_options.add_argument("--unpolarisation-nominal-pos-pol-nicks", type=str, nargs="+",
				help="Nick names of the nominal histogram(s) for positive helicity.")
		self.normalize_polarisation_options.add_argument("--unpolarisation-shift-up-pos-pol-nicks", type=str, nargs="+", default=[None],
				help="Nick names of the shift-up histogram(s) for positive helicity. [Default: %(default)s]")
		self.normalize_polarisation_options.add_argument("--unpolarisation-shift-down-pos-pol-nicks", type=str, nargs="+", default=[None],
				help="Nick names of the shift-down histogram(s) for positive helicity. [Default: %(default)s]")
		self.normalize_polarisation_options.add_argument("--unpolarisation-nominal-neg-pol-nicks", type=str, nargs="+",
				help="Nick names of the nominal histogram(s) for negative helicity.")
		self.normalize_polarisation_options.add_argument("--unpolarisation-shift-up-neg-pol-nicks", type=str, nargs="+", default=[None],
				help="Nick names of the shift-up histogram(s) for negative helicity. [Default: %(default)s]")
		self.normalize_polarisation_options.add_argument("--unpolarisation-shift-down-neg-pol-nicks", type=str, nargs="+", default=[None],
				help="Nick names of the shift-down histogram(s) for negative helicity. [Default: %(default)s]")
		self.normalize_polarisation_options.add_argument("--unpolarisation-remove-bias-instead-unpolarisation", default=False, action="store_true",
				help="Remove all polarisation effects except for the generator level polarisation. [Default: %(default)s]")
		self.normalize_polarisation_options.add_argument("--unpolarisation-forced-gen-polarisations", type=str, nargs="+", default=[None],
				help="Enforce a certain generator polarisation for the unpolarisation step.")
		self.normalize_polarisation_options.add_argument("--unpolarisation-scale-factor-pos-pol-nicks", type=str, nargs="+",
				help="Nick names of the resulting scale factor histogram(s) for positive helicity.")
		self.normalize_polarisation_options.add_argument("--unpolarisation-scale-factor-neg-pol-nicks", type=str, nargs="+",
				help="Nick names of the resulting scale factor histogram(s) for negative helicity.")
		self.normalize_polarisation_options.add_argument("--unpolarisation-polarisation-before-nicks", type=str, nargs="+",
				help="Nick names of the resulting polarisation histogram(s) before unpolarisation.")
		self.normalize_polarisation_options.add_argument("--unpolarisation-polarisation-after-nicks", type=str, nargs="+",
				help="Nick names of the resulting polarisation histogram(s) after unpolarisation.")
	
	def prepare_args(self, parser, plotData):
		super(Unpolarisation, self).prepare_args(parser, plotData)
		self.prepare_list_args(plotData, ["unpolarisation_nominal_pos_pol_nicks", "unpolarisation_shift_up_pos_pol_nicks", "unpolarisation_shift_down_pos_pol_nicks", "unpolarisation_nominal_neg_pol_nicks", "unpolarisation_shift_up_neg_pol_nicks", "unpolarisation_shift_down_neg_pol_nicks", "unpolarisation_forced_gen_polarisations", "unpolarisation_scale_factor_pos_pol_nicks", "unpolarisation_scale_factor_neg_pol_nicks", "unpolarisation_polarisation_before_nicks", "unpolarisation_polarisation_after_nicks"])
		
		for index, (nominal_pos_pol_nick, shift_up_pos_pol_nicks, shift_down_pos_pol_nicks, nominal_neg_pol_nick, shift_up_neg_pol_nicks, shift_down_neg_pol_nicks, forced_gen_polarisation, scale_factor_pos_pol_nick, scale_factor_neg_pol_nick, polarisation_before_nick, polarisation_after_nick) in enumerate(zip(*[plotData.plotdict[key] for key in ["unpolarisation_nominal_pos_pol_nicks", "unpolarisation_shift_up_pos_pol_nicks", "unpolarisation_shift_down_pos_pol_nicks", "unpolarisation_nominal_neg_pol_nicks", "unpolarisation_shift_up_neg_pol_nicks", "unpolarisation_shift_down_neg_pol_nicks", "unpolarisation_forced_gen_polarisations", "unpolarisation_scale_factor_pos_pol_nicks", "unpolarisation_scale_factor_neg_pol_nicks", "unpolarisation_polarisation_before_nicks", "unpolarisation_polarisation_after_nicks"]])):
			
			plotData.plotdict["unpolarisation_shift_up_pos_pol_nicks"][index] = shift_up_pos_pol_nicks.split() if shift_up_pos_pol_nicks else [shift_up_pos_pol_nicks]
			plotData.plotdict["unpolarisation_shift_down_pos_pol_nicks"][index] = shift_down_pos_pol_nicks.split() if shift_down_pos_pol_nicks else [shift_up_pos_pol_nicks]
			plotData.plotdict["unpolarisation_shift_up_neg_pol_nicks"][index] = shift_up_neg_pol_nicks.split() if shift_up_neg_pol_nicks else [shift_up_pos_pol_nicks]
			plotData.plotdict["unpolarisation_shift_down_neg_pol_nicks"][index] = shift_down_neg_pol_nicks.split() if shift_down_neg_pol_nicks else [shift_up_pos_pol_nicks]
			
			if (forced_gen_polarisation is None) or (forced_gen_polarisation=="None"):
				plotData.plotdict["unpolarisation_forced_gen_polarisations"][index] = None
			else:
				plotData.plotdict["unpolarisation_forced_gen_polarisations"][index] = float(forced_gen_polarisation)
			
			if scale_factor_pos_pol_nick not in plotData.plotdict["nicks"]:
				plotData.plotdict["nicks"].insert(plotData.plotdict["nicks"].index(nominal_pos_pol_nick)+1, scale_factor_pos_pol_nick)
			if scale_factor_neg_pol_nick not in plotData.plotdict["nicks"]:
				plotData.plotdict["nicks"].insert(plotData.plotdict["nicks"].index(nominal_neg_pol_nick)+1, scale_factor_neg_pol_nick)
			max_index = max([plotData.plotdict["nicks"].index(nick) for nick in [nominal_pos_pol_nick, nominal_neg_pol_nick, scale_factor_pos_pol_nick, scale_factor_neg_pol_nick]])
			if polarisation_before_nick not in plotData.plotdict["nicks"]:
				plotData.plotdict["nicks"].insert(max_index+1, polarisation_before_nick)
			if polarisation_after_nick not in plotData.plotdict["nicks"]:
				plotData.plotdict["nicks"].insert(max_index+2, polarisation_after_nick)
	
	def run(self, plotData=None):
		super(Unpolarisation, self).run(plotData)
		
		remove_bias_instead_unpolarisation = plotData.plotdict["unpolarisation_remove_bias_instead_unpolarisation"]
		
		for index, (nominal_pos_pol_nick, shift_up_pos_pol_nicks, shift_down_pos_pol_nicks, nominal_neg_pol_nick, shift_up_neg_pol_nicks, shift_down_neg_pol_nicks, forced_gen_polarisation, scale_factor_pos_pol_nick, scale_factor_neg_pol_nick, polarisation_before_nick, polarisation_after_nick) in enumerate(zip(*[plotData.plotdict[key] for key in ["unpolarisation_nominal_pos_pol_nicks", "unpolarisation_shift_up_pos_pol_nicks", "unpolarisation_shift_down_pos_pol_nicks", "unpolarisation_nominal_neg_pol_nicks", "unpolarisation_shift_up_neg_pol_nicks", "unpolarisation_shift_down_neg_pol_nicks", "unpolarisation_forced_gen_polarisations", "unpolarisation_scale_factor_pos_pol_nicks", "unpolarisation_scale_factor_neg_pol_nicks", "unpolarisation_polarisation_before_nicks", "unpolarisation_polarisation_after_nicks"]])):
			
			nominal_pos_pol_hist = plotData.plotdict["root_objects"][nominal_pos_pol_nick]
			shift_up_pos_pol_hists = [plotData.plotdict["root_objects"][nick] for nick in shift_up_pos_pol_nicks if not nick is None]
			shift_down_pos_pol_hists = [plotData.plotdict["root_objects"][nick] for nick in shift_down_pos_pol_nicks if not nick is None]
			
			nominal_neg_pol_hist = plotData.plotdict["root_objects"][nominal_neg_pol_nick]
			shift_up_neg_pol_hists = [plotData.plotdict["root_objects"][nick] for nick in shift_up_neg_pol_nicks if not nick is None]
			shift_down_neg_pol_hists = [plotData.plotdict["root_objects"][nick] for nick in shift_down_neg_pol_nicks if not nick is None]
			
			name = hashlib.md5("_".join(map(str, [nominal_pos_pol_nick, shift_up_pos_pol_nicks, shift_down_pos_pol_nicks, nominal_neg_pol_nick, shift_up_neg_pol_nicks, shift_down_neg_pol_nicks, forced_gen_polarisation, scale_factor_pos_pol_nick, scale_factor_neg_pol_nick]))).hexdigest()
			
			scale_factor_pos_pol_hist = nominal_pos_pol_hist.Clone("unpol_pos_"+name)
			scale_factor_pos_pol_hist.Reset()
			scale_factor_neg_pol_hist = nominal_neg_pol_hist.Clone("unpol_neg_"+name)
			scale_factor_neg_pol_hist.Reset()
			
			polarisation_before_hist = nominal_pos_pol_hist.Clone("unpol_pol_before_"+name)
			polarisation_before_hist.Reset()
			polarisation_after_hist = nominal_pos_pol_hist.Clone("unpol_pol_after_"+name)
			polarisation_after_hist.Reset()
			
			# assume same binning for all histograms
			for x_bin in xrange(1, nominal_pos_pol_hist.GetNbinsX()+1):
				for y_bin in xrange(1, nominal_pos_pol_hist.GetNbinsY()+1):
					for z_bin in xrange(1, nominal_pos_pol_hist.GetNbinsZ()+1):
						global_bin = nominal_pos_pol_hist.GetBin(x_bin, y_bin, z_bin)
						
						n_pos_pol = uncertainties.ufloat(
								nominal_pos_pol_hist.GetBinContent(global_bin),
								nominal_pos_pol_hist.GetBinError(global_bin)
						)
						
						unc_up = pow(n_pos_pol.std_dev, 2)
						for shift_hist in shift_up_pos_pol_hists:
							n_shift = uncertainties.ufloat(shift_hist.GetBinContent(global_bin), shift_hist.GetBinError(global_bin))
							unc_up += pow(n_shift-n_pos_pol, 2).nominal_value
						unc_up = math.sqrt(unc_up)
						
						unc_down = pow(n_pos_pol.std_dev, 2)
						for shift_hist in shift_down_pos_pol_hists:
							n_shift = uncertainties.ufloat(shift_hist.GetBinContent(global_bin), shift_hist.GetBinError(global_bin))
							unc_down += pow(n_shift-n_pos_pol, 2).nominal_value
						unc_down = math.sqrt(unc_down)
						
						n_pos_pol.std_dev = max(unc_up, unc_down)
						
						n_neg_pol = uncertainties.ufloat(
								nominal_neg_pol_hist.GetBinContent(global_bin),
								nominal_neg_pol_hist.GetBinError(global_bin)
						)
						
						unc_up = pow(n_neg_pol.std_dev, 2)
						for shift_hist in shift_up_neg_pol_hists:
							n_shift = uncertainties.ufloat(shift_hist.GetBinContent(global_bin), shift_hist.GetBinError(global_bin))
							unc_up += pow(n_shift-n_neg_pol, 2).nominal_value
						unc_up = math.sqrt(unc_up)
						
						unc_down = pow(n_neg_pol.std_dev, 2)
						for shift_hist in shift_down_neg_pol_hists:
							n_shift = uncertainties.ufloat(shift_hist.GetBinContent(global_bin), shift_hist.GetBinError(global_bin))
							unc_down += pow(n_shift-n_neg_pol, 2).nominal_value
						unc_down = math.sqrt(unc_down)
						
						n_neg_pol.std_dev = max(unc_up, unc_down)
						
						scale_factors = polarisationsignalscaling.PolarisationScaleFactors(
								n_pos_pol, n_neg_pol,
								n_pos_pol, n_neg_pol,
								forced_gen_polarisation=forced_gen_polarisation
						)
						
						scale_factor_pos_pol = scale_factors.get_bias_removal_factor_pospol() if remove_bias_instead_unpolarisation else scale_factors.get_scale_factor_pospol()
						scale_factor_pos_pol_hist.SetBinContent(global_bin, scale_factor_pos_pol.nominal_value)
						scale_factor_pos_pol_hist.SetBinError(global_bin, scale_factor_pos_pol.std_dev)
						
						scale_factor_neg_pol = scale_factors.get_bias_removal_factor_negpol() if remove_bias_instead_unpolarisation else scale_factors.get_scale_factor_negpol()
						scale_factor_neg_pol_hist.SetBinContent(global_bin, scale_factor_neg_pol.nominal_value)
						scale_factor_neg_pol_hist.SetBinError(global_bin, scale_factor_neg_pol.std_dev)
						
						polarisation_before = scale_factors.get_gen_polarisation()
						polarisation_before_hist.SetBinContent(global_bin, polarisation_before.nominal_value)
						polarisation_before_hist.SetBinError(global_bin, polarisation_before.std_dev)
						
						# Caution: scale_factors object is modified!
						scale_factors.n_gen_pospol *= scale_factor_pos_pol
						scale_factors.n_gen_negpol *= scale_factor_neg_pol
						polarisation_after = scale_factors.get_gen_polarisation()
						polarisation_after_hist.SetBinContent(global_bin, polarisation_after.nominal_value)
						polarisation_after_hist.SetBinError(global_bin, polarisation_after.std_dev)
						
			plotData.plotdict["root_objects"][scale_factor_pos_pol_nick] = scale_factor_pos_pol_hist
			plotData.plotdict["root_objects"][scale_factor_neg_pol_nick] = scale_factor_neg_pol_hist
			
			plotData.plotdict["root_objects"][polarisation_before_nick] = polarisation_before_hist
			plotData.plotdict["root_objects"][polarisation_after_nick] = polarisation_after_hist

