
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import pprint
import copy
import sys
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.samples_run2_2017 as samples
from Kappa.Skimming.registerDatasetHelper import get_nick_list
from Artus.Utility.tools import make_multiplication, split_multiplication, clean_multiplication

default_lumi =  41.5*1000.0

class Samples(samples.Samples):

	def qcd(self, config, channel, category, weight, nick_suffix, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", estimationMethod="classic", controlregions=False,**kwargs):
		if exclude_cuts is None:
			exclude_cuts = []

		zmm_cr_factor = kwargs.get("zmm_cr_factor", "(1.0)")

		scale_factor = 1.0
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("QCD", 1.0)

		data_weight, mc_weight = self.projection(kwargs)

		if channel in ["et", "mt", "em", "tt", "mm", "ee", "ttbar"]:

			if "new" in estimationMethod:
				if channel in ["et","mt"]:
					high_mt_cut_type = cut_type + "highMtControlRegionWJ"
					print "high_mt_cut_type:", high_mt_cut_type
					high_mt_ss_cut_type = cut_type + "highMtSSControlRegionWJ"
					print "high_mt_ss_cut_type:", high_mt_ss_cut_type
					qcd_shape_cut = cut_type
					qcd_invertedIso_cut = cut_type + "invertedLeptonIsolation"
					print "invertedcut:", qcd_invertedIso_cut
					print "qcd_shape_cut:",qcd_shape_cut
					exclude_cuts_high_mt = [cut for cut in exclude_cuts if cut not in ["mt"]]
					exclude_cuts_high_mt_ss = copy.deepcopy(exclude_cuts_high_mt)+["os"]

					if kwargs.get("useRelaxedIsolationForQCD", False):
						qcd_shape_cut = qcd_shape_cut + "relaxedETauMuTauWJ"
						#print "useRelaxedIsolationForQCD", useRelaxedIsolationForQCD
						print "qcd_shape_cut-relaxedisoFalse:", qcd_shape_cut 
					elif category != None:
						qcd_shape_cut = qcd_shape_cut + ("relaxedETauMuTauWJ" if ("1jet" in category or "vbf" in category or "Boosted2D" in category or "Vbf2D" in category) else "")
						print "qcd_shape_cut-for category:", qcd_shape_cut 
					qcd_shape_weight = weight
					print "qcd_shape_weight", qcd_shape_weight
					if "newKIT" in estimationMethod:
						qcd_shape_weight = make_multiplication(Samples.get_jetbin(channel, category, weight))

					Samples._add_input(
							config,
							self.files_ztt(channel),
							self.root_file_folder(channel),
							lumi,
							Samples.ztt_genmatch(channel)+"*"+self.get_weights_ztt(channel=channel,cut_type=cut_type,weight=weight)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=cut_type)+"*((q_1*q_2)>0.0)"+"*zPtReweightWeight"+"*"+zmm_cr_factor,
							("noplot_" if not controlregions else "") + "ztt_ss_lowmt",
							nick_suffix=nick_suffix
					)
					print "nick_suffix", nick_suffix
					if not (kwargs.get("no_ewk_samples", False) or kwargs.get("no_ewkz_as_dy", False)):
						Samples._add_input(
								config,
								self.files_ewkz_zll(channel),
								self.root_file_folder(channel),
								lumi,
								Samples.ztt_genmatch(channel)+"*"+self.get_weights_ztt(channel=channel,cut_type=cut_type,weight=weight,doStitching=False)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=cut_type)+"*((q_1*q_2)>0.0)"+"*"+self.ewkz_zll_stitchingweight()+"*"+zmm_cr_factor,
								("noplot_" if not controlregions else "") + "ztt_ss_lowmt",
								nick_suffix=nick_suffix
						)
						Samples._add_input(
								config,
								self.files_ewkz_znn(channel),
								self.root_file_folder(channel),
								lumi,
								Samples.ztt_genmatch(channel)+"*"+self.get_weights_ztt(channel=channel,cut_type=cut_type,weight=weight,doStitching=False)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=cut_type)+"*((q_1*q_2)>0.0)"+"*"+self.ewkz_znn_stitchingweight()+"*"+zmm_cr_factor,
								("noplot_" if not controlregions else "") + "ztt_ss_lowmt",
								nick_suffix=nick_suffix
						)
					Samples._add_input(
							config,
							self.files_zll(channel),
							self.root_file_folder(channel),
							lumi,
							mc_weight+"*"+weight+"*eventWeight*"+self.zll_stitchingweight()+"*"+Samples.zll_genmatch(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=cut_type)+"*((q_1*q_2)>0.0)"+"*zPtReweightWeight"+"*"+self.zll_zl_shape_weight(channel, cut_type)+"*"+zmm_cr_factor,
							("noplot_" if not controlregions else "") + "zll_ss_lowmt",
							nick_suffix=nick_suffix
					)
					if not (kwargs.get("no_ewk_samples", False) or kwargs.get("no_ewkz_as_dy", False)):
						Samples._add_input(
								config,
								self.files_ewkz_zll(channel),
								self.root_file_folder(channel),
								lumi,
								mc_weight+"*"+weight+"*eventWeight*"+Samples.zll_genmatch(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=cut_type)+"*((q_1*q_2)>0.0)"+"*"+self.zll_zl_shape_weight(channel, cut_type)+"*"+self.ewkz_zll_stitchingweight()+"*"+zmm_cr_factor,
								("noplot_" if not controlregions else "") + "zll_ss_lowmt",
								nick_suffix=nick_suffix
						)
						Samples._add_input(
								config,
								self.files_ewkz_znn(channel),
								self.root_file_folder(channel),
								lumi,
								mc_weight+"*"+weight+"*eventWeight*"+Samples.zll_genmatch(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=cut_type)+"*((q_1*q_2)>0.0)"+"*"+self.zll_zl_shape_weight(channel, cut_type)+"*"+self.ewkz_znn_stitchingweight()+"*"+zmm_cr_factor,
								("noplot_" if not controlregions else "") + "zll_ss_lowmt",
								nick_suffix=nick_suffix
						)
					if not kwargs.get("no_ewk_samples", False) and kwargs.get("no_ewkz_as_dy", False):
						Samples._add_input(
								config,
								self.files_ewkz_zll(channel),
								self.root_file_folder(channel),
								lumi,
								mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=cut_type)+"*((q_1*q_2)>0.0)"+"*"+self.ewkz_zll_stitchingweight()+"*"+zmm_cr_factor,
								("noplot_" if not controlregions else "") + "ewkz_ss_lowmt",
								nick_suffix=nick_suffix
						)
						Samples._add_input(
								config,
								self.files_ewkz_znn(channel),
								self.root_file_folder(channel),
								lumi,
								mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=cut_type)+"*((q_1*q_2)>0.0)"+"*"+self.ewkz_znn_stitchingweight()+"*"+zmm_cr_factor,
								("noplot_" if not controlregions else "") + "ewkz_ss_lowmt",
								nick_suffix=nick_suffix
						)
					Samples._add_input(
							config,
							self.files_ttj(channel),
							self.root_file_folder(channel),
							lumi,
							mc_weight+"*"+weight+"*eventWeight*"+self.embedding_ttbarveto_weight(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=cut_type)+"*((q_1*q_2)>0.0)*topPtReweightWeight",
							("noplot_" if not controlregions else "") + "ttj_ss_lowmt",
							nick_suffix=nick_suffix
					)
					Samples._add_input(
							config,
							self.files_vv(channel),
							self.root_file_folder(channel),
							lumi,
							mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=cut_type)+"*((q_1*q_2)>0.0)"+"*"+self.vv_stitchingweight(),
							("noplot_" if not controlregions else "") + "vv_ss_lowmt",
							nick_suffix=nick_suffix
					)
					Samples._add_input(
							config,
							self.files_diboson(channel),
							self.root_file_folder(channel),
							lumi,
							mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=cut_type)+"*((q_1*q_2)>0.0)",
							("noplot_" if not controlregions else "") + "vv_ss_lowmt",
							nick_suffix=nick_suffix
					)
					Samples._add_input(
							config,
							self.files_wj(channel),
							self.root_file_folder(channel),
							lumi,
							mc_weight+"*"+weight+"*eventWeight*"+self.wj_stitchingweight()+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=cut_type)+"*((q_1*q_2)>0.0)",
							("noplot_" if not controlregions else "") + "wj_ss_lowmt",
							nick_suffix=nick_suffix
					)
					if (not kwargs.get("no_ewk_samples", False)):
						Samples._add_input(
								config,
								self.files_ewkwm(channel),
								self.root_file_folder(channel),
								lumi,
								mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=cut_type)+"*((q_1*q_2)>0.0)"+"*"+self.ewkwm_stitchingweight(),
								("noplot_" if not controlregions else "") + "wj_ss_lowmt",
								nick_suffix=nick_suffix
						)
						Samples._add_input(
								config,
								self.files_ewkwp(channel),
								self.root_file_folder(channel),
								lumi,
								mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=cut_type)+"*((q_1*q_2)>0.0)"+"*"+self.ewkwp_stitchingweight(),
								("noplot_" if not controlregions else "") + "wj_ss_lowmt",
								nick_suffix=nick_suffix
						)
					Samples._add_input(
							config,
							self.files_data(channel),
							self.root_file_folder(channel),
							1.0,
							data_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=cut_type)+"*((q_1*q_2)>0.0)",
							("noplot_" if not controlregions else "") + "data_ss_lowmt",
							nick_suffix=nick_suffix
					)
					Samples._add_input(
							config,
							self.files_ztt(channel),
							self.root_file_folder(channel),
							lumi,
							Samples.ztt_genmatch(channel)+"*"+self.get_weights_ztt(channel=channel,cut_type=cut_type,weight=qcd_shape_weight)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=qcd_shape_cut)+"*((q_1*q_2)>0.0)"+"*zPtReweightWeight"+"*"+zmm_cr_factor,
							"noplot_ztt_shape_ss_qcd_control",
							nick_suffix=nick_suffix
					)
					if not (kwargs.get("no_ewk_samples", False) or kwargs.get("no_ewkz_as_dy", False)):
						Samples._add_input(
								config,
								self.files_ewkz_zll(channel),
								self.root_file_folder(channel),
								lumi,
								Samples.ztt_genmatch(channel)+"*"+self.get_weights_ztt(channel=channel,cut_type=cut_type,weight=qcd_shape_weight,doStitching=False)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=qcd_shape_cut)+"*((q_1*q_2)>0.0)"+"*"+self.ewkz_zll_stitchingweight()+"*"+zmm_cr_factor,
								"noplot_ztt_shape_ss_qcd_control",
								nick_suffix=nick_suffix
						)
						Samples._add_input(
								config,
								self.files_ewkz_znn(channel),
								self.root_file_folder(channel),
								lumi,
								Samples.ztt_genmatch(channel)+"*"+self.get_weights_ztt(channel=channel,cut_type=cut_type,weight=qcd_shape_weight,doStitching=False)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=qcd_shape_cut)+"*((q_1*q_2)>0.0)"+"*"+self.ewkz_znn_stitchingweight()+"*"+zmm_cr_factor,
								"noplot_ztt_shape_ss_qcd_control",
								nick_suffix=nick_suffix
						)
					Samples._add_input(
							config,
							self.files_zll(channel),
							self.root_file_folder(channel),
							lumi,
							mc_weight+"*"+qcd_shape_weight+"*eventWeight*"+self.zll_stitchingweight()+"*"+Samples.zll_genmatch(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=qcd_shape_cut)+"*((q_1*q_2)>0.0)"+"*zPtReweightWeight"+"*"+self.zll_zl_shape_weight(channel, cut_type)+"*"+zmm_cr_factor,
							"noplot_zll_shape_ss_qcd_control",
							nick_suffix=nick_suffix
					)
					if not (kwargs.get("no_ewk_samples", False) or kwargs.get("no_ewkz_as_dy", False)):
						Samples._add_input(
								config,
								self.files_ewkz_zll(channel),
								self.root_file_folder(channel),
								lumi,
								mc_weight+"*"+qcd_shape_weight+"*eventWeight*"+Samples.zll_genmatch(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=qcd_shape_cut)+"*((q_1*q_2)>0.0)"+"*"+self.zll_zl_shape_weight(channel, cut_type)+"*"+self.ewkz_zll_stitchingweight()+"*"+zmm_cr_factor,
								"noplot_zll_shape_ss_qcd_control",
								nick_suffix=nick_suffix
						)
						Samples._add_input(
								config,
								self.files_ewkz_znn(channel),
								self.root_file_folder(channel),
								lumi,
								mc_weight+"*"+qcd_shape_weight+"*eventWeight*"+Samples.zll_genmatch(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=qcd_shape_cut)+"*((q_1*q_2)>0.0)"+"*"+self.zll_zl_shape_weight(channel, cut_type)+"*"+self.ewkz_znn_stitchingweight()+"*"+zmm_cr_factor,
								"noplot_zll_shape_ss_qcd_control",
								nick_suffix=nick_suffix
						)
					if not kwargs.get("no_ewk_samples", False) and kwargs.get("no_ewkz_as_dy", False):
						Samples._add_input(
								config,
								self.files_ewkz_zll(channel),
								self.root_file_folder(channel),
								lumi,
								mc_weight+"*"+qcd_shape_weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=qcd_shape_cut)+"*((q_1*q_2)>0.0)"+"*"+self.ewkz_zll_stitchingweight()+"*"+zmm_cr_factor,
								"noplot_ewkz_shape_ss_qcd_control",
								nick_suffix=nick_suffix
						)
						Samples._add_input(
								config,
								self.files_ewkz_znn(channel),
								self.root_file_folder(channel),
								lumi,
								mc_weight+"*"+qcd_shape_weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=qcd_shape_cut)+"*((q_1*q_2)>0.0)"+"*"+self.ewkz_znn_stitchingweight()+"*"+zmm_cr_factor,
								"noplot_ewkz_shape_ss_qcd_control",
								nick_suffix=nick_suffix
						)
					Samples._add_input(
							config,
							self.files_ttj(channel),
							self.root_file_folder(channel),
							lumi,
							mc_weight+"*"+qcd_shape_weight+"*eventWeight*"+self.embedding_ttbarveto_weight(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=qcd_shape_cut)+"*((q_1*q_2)>0.0)*topPtReweightWeight",
							"noplot_ttj_shape_ss_qcd_control",
							nick_suffix=nick_suffix
					)
					Samples._add_input(
							config,
							self.files_vv(channel),
							self.root_file_folder(channel),
							lumi,
							mc_weight+"*"+qcd_shape_weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=qcd_shape_cut)+"*((q_1*q_2)>0.0)"+"*"+self.vv_stitchingweight(),
							"noplot_vv_shape_ss_qcd_control",
							nick_suffix=nick_suffix
					)
					Samples._add_input(
							config,
							self.files_diboson(channel),
							self.root_file_folder(channel),
							lumi,
							mc_weight+"*"+qcd_shape_weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=qcd_shape_cut)+"*((q_1*q_2)>0.0)",
							"noplot_vv_shape_ss_qcd_control",
							nick_suffix=nick_suffix
					)
					Samples._add_input(
							config,
							self.files_wj(channel),
							self.root_file_folder(channel),
							lumi,
							mc_weight+"*"+qcd_shape_weight+"*eventWeight*"+self.wj_stitchingweight()+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=qcd_shape_cut)+"*((q_1*q_2)>0.0)",
							"noplot_wj_shape_ss_qcd_control",
							nick_suffix=nick_suffix
					)
					if (not kwargs.get("no_ewk_samples", False)):
						Samples._add_input(
								config,
								self.files_ewkwm(channel),
								self.root_file_folder(channel),
								lumi,
								mc_weight+"*"+qcd_shape_weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=qcd_shape_cut)+"*((q_1*q_2)>0.0)"+"*"+self.ewkwm_stitchingweight(),
								"noplot_wj_shape_ss_qcd_control",
								nick_suffix=nick_suffix
						)
						Samples._add_input(
								config,
								self.files_ewkwp(channel),
								self.root_file_folder(channel),
								lumi,
								mc_weight+"*"+qcd_shape_weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=qcd_shape_cut)+"*((q_1*q_2)>0.0)"+"*"+self.ewkwp_stitchingweight(),
								"noplot_wj_shape_ss_qcd_control",
								nick_suffix=nick_suffix
						)
					Samples._add_input(
							config,
							self.files_data(channel),
							self.root_file_folder(channel),
							1.0,
							data_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_high_mt_ss, cut_type=high_mt_ss_cut_type),
							("noplot_" if not controlregions else "") + "qcd_ss_highmt",
							nick_suffix=nick_suffix
					)
					Samples._add_input(
							config,
							self.files_ztt(channel),
							self.root_file_folder(channel),
							lumi,
							Samples.ztt_genmatch(channel)+"*"+self.get_weights_ztt(channel=channel,cut_type=cut_type,weight=weight)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_high_mt_ss, cut_type=high_mt_ss_cut_type)+"*zPtReweightWeight"+"*"+zmm_cr_factor,
							"noplot_ztt_shape_ss_highmt",
							nick_suffix=nick_suffix
					)
					if not (kwargs.get("no_ewk_samples", False) or kwargs.get("no_ewkz_as_dy", False)):
						Samples._add_input(
								config,
								self.files_ewkz_zll(channel),
								self.root_file_folder(channel),
								lumi,
								Samples.ztt_genmatch(channel)+"*"+self.get_weights_ztt(channel=channel,cut_type=cut_type,weight=weight,doStitching=False)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_high_mt_ss, cut_type=high_mt_ss_cut_type)+"*"+self.ewkz_zll_stitchingweight()+"*"+zmm_cr_factor,
								"noplot_ztt_shape_ss_highmt",
								nick_suffix=nick_suffix
						)
						Samples._add_input(
								config,
								self.files_ewkz_znn(channel),
								self.root_file_folder(channel),
								lumi,
								Samples.ztt_genmatch(channel)+"*"+self.get_weights_ztt(channel=channel,cut_type=cut_type,weight=weight,doStitching=False)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_high_mt_ss, cut_type=high_mt_ss_cut_type)+"*"+self.ewkz_znn_stitchingweight()+"*"+zmm_cr_factor,
								"noplot_ztt_shape_ss_highmt",
								nick_suffix=nick_suffix
						)
					Samples._add_input(
							config,
							self.files_zll(channel),
							self.root_file_folder(channel),
							lumi,
							mc_weight+"*"+weight+"*eventWeight*"+self.zll_stitchingweight()+"*"+Samples.zll_genmatch(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_high_mt_ss, cut_type=high_mt_ss_cut_type)+"*zPtReweightWeight"+"*"+self.zll_zl_shape_weight(channel, cut_type)+"*"+zmm_cr_factor,
							"noplot_zll_shape_ss_highmt",
							nick_suffix=nick_suffix
					)
					if not (kwargs.get("no_ewk_samples", False) or kwargs.get("no_ewkz_as_dy", False)):
						Samples._add_input(
								config,
								self.files_ewkz_zll(channel),
								self.root_file_folder(channel),
								lumi,
								mc_weight+"*"+weight+"*eventWeight*"+Samples.zll_genmatch(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_high_mt_ss, cut_type=high_mt_ss_cut_type)+"*"+self.zll_zl_shape_weight(channel, cut_type)+"*"+self.ewkz_zll_stitchingweight()+"*"+zmm_cr_factor,
								"noplot_zll_shape_ss_highmt",
								nick_suffix=nick_suffix
						)
						Samples._add_input(
								config,
								self.files_ewkz_znn(channel),
								self.root_file_folder(channel),
								lumi,
								mc_weight+"*"+weight+"*eventWeight*"+Samples.zll_genmatch(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_high_mt_ss, cut_type=high_mt_ss_cut_type)+"*"+self.zll_zl_shape_weight(channel, cut_type)+"*"+self.ewkz_znn_stitchingweight()+"*"+zmm_cr_factor,
								"noplot_zll_shape_ss_highmt",
								nick_suffix=nick_suffix
						)
					if not kwargs.get("no_ewk_samples", False) and kwargs.get("no_ewkz_as_dy", False):
						Samples._add_input(
								config,
								self.files_ewkz_zll(channel),
								self.root_file_folder(channel),
								lumi,
								mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_high_mt_ss, cut_type=high_mt_ss_cut_type)+"*"+self.ewkz_zll_stitchingweight()+"*"+zmm_cr_factor,
								"noplot_ewkz_shape_ss_highmt",
								nick_suffix=nick_suffix
						)
						Samples._add_input(
								config,
								self.files_ewkz_znn(channel),
								self.root_file_folder(channel),
								lumi,
								mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_high_mt_ss, cut_type=high_mt_ss_cut_type)+"*"+self.ewkz_znn_stitchingweight()+"*"+zmm_cr_factor,
								"noplot_ewkz_shape_ss_highmt",
								nick_suffix=nick_suffix
						)
					Samples._add_input(
							config,
							self.files_ttj(channel),
							self.root_file_folder(channel),
							lumi,
							mc_weight+"*"+weight+"*eventWeight*"+self.embedding_ttbarveto_weight(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_high_mt_ss, cut_type=high_mt_ss_cut_type)+"*topPtReweightWeight",
							"noplot_ttj_shape_ss_highmt",
							nick_suffix=nick_suffix
					)
					Samples._add_input(
							config,
							self.files_vv(channel),
							self.root_file_folder(channel),
							lumi,
							mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_high_mt_ss, cut_type=high_mt_ss_cut_type)+"*"+self.vv_stitchingweight(),
							"noplot_vv_shape_ss_highmt",
							nick_suffix=nick_suffix
					)
					Samples._add_input(
							config,
							self.files_diboson(channel),
							self.root_file_folder(channel),
							lumi,
							mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_high_mt_ss, cut_type=high_mt_ss_cut_type),
							"noplot_vv_shape_ss_highmt",
							nick_suffix=nick_suffix
					)
					Samples._add_input(
							config,
							self.files_data(channel),
							self.root_file_folder(channel),
							1.0,
							data_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_high_mt, cut_type=high_mt_cut_type),
							("noplot_" if not controlregions else "") + "qcd_os_highmt",
							nick_suffix=nick_suffix
					)
					Samples._add_input(
							config,
							self.files_data(channel),
							self.root_file_folder(channel),
							1.0,
							data_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=cut_type)+"*((q_1*q_2)>0.0)",
							("noplot_" if not controlregions else "") + "qcd_ss_lowmt",
							nick_suffix=nick_suffix
					)
					Samples._add_input(
							config,
							self.files_data(channel),
							self.root_file_folder(channel),
							1.0,
							data_weight+"*"+qcd_shape_weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=qcd_shape_cut)+"*((q_1*q_2)>0.0)",
							"qcd",
							nick_suffix=nick_suffix
					)# add samples which will be used for ss_os_extrapolation factor
					Samples._add_input(
							config,
							self.files_ztt(channel),
							self.root_file_folder(channel),
							lumi,
							Samples.ztt_genmatch(channel)+"*"+self.get_weights_ztt(channel=channel,cut_type=cut_type,weight=weight)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=qcd_invertedIso_cut)+"*((q_1*q_2)<0.0)"+"*zPtReweightWeight"+"*"+self.decay_mode_reweight(channel)+"*"+zmm_cr_factor+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
							("noplot_" if not controlregions else "") + "ztt_os_invertedEIso",
							nick_suffix=nick_suffix
					)
					if not (kwargs.get("no_ewk_samples", False) or kwargs.get("no_ewkz_as_dy", False)):
						Samples._add_input(
								config,
								self.files_ewkz_zll(channel),
								self.root_file_folder(channel),
								lumi,
								Samples.ztt_genmatch(channel)+"*"+self.get_weights_ztt(channel=channel,cut_type=cut_type,weight=weight,doStitching=False)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=qcd_invertedIso_cut)+"*((q_1*q_2)<0.0)"+"*"+self.decay_mode_reweight(channel)+"*"+self.ewkz_zll_stitchingweight()+"*"+zmm_cr_factor+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
								("noplot_" if not controlregions else "") + "ztt_os_invertedEIso",
								nick_suffix=nick_suffix
						)
						Samples._add_input(
								config,
								self.files_ewkz_znn(channel),
								self.root_file_folder(channel),
								lumi,
								Samples.ztt_genmatch(channel)+"*"+self.get_weights_ztt(channel=channel,cut_type=cut_type,weight=weight,doStitching=False)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=qcd_invertedIso_cut)+"*((q_1*q_2)<0.0)"+"*"+self.decay_mode_reweight(channel)+"*"+self.ewkz_znn_stitchingweight()+"*"+zmm_cr_factor+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
								("noplot_" if not controlregions else "") + "ztt_os_invertedEIso",
								nick_suffix=nick_suffix
						)
					Samples._add_input(
							config,
							self.files_zll(channel),
							self.root_file_folder(channel),
							lumi,
							mc_weight+"*"+weight+"*eventWeight*"+self.zll_stitchingweight()+"*"+Samples.zll_genmatch(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=qcd_invertedIso_cut)+"*((q_1*q_2)<0.0)"+"*zPtReweightWeight"+"*"+self.zll_zl_shape_weight(channel, cut_type)+"*"+zmm_cr_factor+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
							("noplot_" if not controlregions else "") + "zll_os_invertedEIso",
							nick_suffix=nick_suffix
					)
					if not (kwargs.get("no_ewk_samples", False) or kwargs.get("no_ewkz_as_dy", False)):
						Samples._add_input(
								config,
								self.files_ewkz_zll(channel),
								self.root_file_folder(channel),
								lumi,
								mc_weight+"*"+weight+"*eventWeight*"+Samples.zll_genmatch(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=qcd_invertedIso_cut)+"*((q_1*q_2)<0.0)"+"*"+self.zll_zl_shape_weight(channel, cut_type)+"*"+self.ewkz_zll_stitchingweight()+"*"+zmm_cr_factor+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
								("noplot_" if not controlregions else "") + "zll_os_invertedEIso",
								nick_suffix=nick_suffix
						)
						Samples._add_input(
								config,
								self.files_ewkz_znn(channel),
								self.root_file_folder(channel),
								lumi,
								mc_weight+"*"+weight+"*eventWeight*"+Samples.zll_genmatch(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=qcd_invertedIso_cut)+"*((q_1*q_2)<0.0)"+"*"+self.zll_zl_shape_weight(channel, cut_type)+"*"+self.ewkz_znn_stitchingweight()+"*"+zmm_cr_factor+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
								("noplot_" if not controlregions else "") + "zll_os_invertedEIso",
								nick_suffix=nick_suffix
						)
					if not kwargs.get("no_ewk_samples", False) and kwargs.get("no_ewkz_as_dy", False):
						Samples._add_input(
								config,
								self.files_ewkz_zll(channel),
								self.root_file_folder(channel),
								lumi,
								mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=qcd_invertedIso_cut)+"*((q_1*q_2)<0.0)"+"*"+self.ewkz_zll_stitchingweight()+"*"+zmm_cr_factor,
								("noplot_" if not controlregions else "") + "ewkz_os_invertedEIso",
								nick_suffix=nick_suffix
						)
						Samples._add_input(
								config,
								self.files_ewkz_znn(channel),
								self.root_file_folder(channel),
								lumi,
								mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=qcd_invertedIso_cut)+"*((q_1*q_2)<0.0)"+"*"+self.ewkz_znn_stitchingweight()+"*"+zmm_cr_factor,
								("noplot_" if not controlregions else "") + "ewkz_os_invertedEIso",
								nick_suffix=nick_suffix
						)
					Samples._add_input(
							config,
							self.files_ttj(channel),
							self.root_file_folder(channel),
							lumi,
							mc_weight+"*"+weight+"*eventWeight*"+self.embedding_ttbarveto_weight(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=qcd_invertedIso_cut)+"*((q_1*q_2)<0.0)"+"*topPtReweightWeight"+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
							("noplot_" if not controlregions else "") + "ttj_os_invertedEIso",
							nick_suffix=nick_suffix
					)
					Samples._add_input(
							config,
							self.files_vv(channel),
							self.root_file_folder(channel),
							lumi,
							mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=qcd_invertedIso_cut)+"*((q_1*q_2)<0.0)"+"*"+self.vv_stitchingweight()+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
							("noplot_" if not controlregions else "") + "vv_os_invertedEIso",
							nick_suffix=nick_suffix
					)
					Samples._add_input(
							config,
							self.files_diboson(channel),
							self.root_file_folder(channel),
							lumi,
							mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=qcd_invertedIso_cut)+"*((q_1*q_2)<0.0)"+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
							("noplot_" if not controlregions else "") + "vv_os_invertedEIso",
							nick_suffix=nick_suffix
					)
					Samples._add_input(
							config,
							self.files_wj(channel),
							self.root_file_folder(channel),
							lumi,
							mc_weight+"*"+qcd_shape_weight+"*eventWeight*"+self.wj_stitchingweight()+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=qcd_invertedIso_cut)+"*((q_1*q_2)<0.0)",
							("noplot_" if not controlregions else "") + "wj_os_invertedEIso",
							nick_suffix=nick_suffix
					)
					Samples._add_input(
							config,
							self.files_data(channel),
							self.root_file_folder(channel),
							1.0,
							data_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=qcd_invertedIso_cut)+"*((q_1*q_2)<0.0)",
							("noplot_" if not controlregions else "") + "qcd_os_invertedEIso",
							nick_suffix=nick_suffix
					)
					Samples._add_input(
							config,
							self.files_data(channel),
							self.root_file_folder(channel),
							1.0,
							data_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=qcd_invertedIso_cut)+"*((q_1*q_2)<0.0)",
							("noplot_" if not controlregions else "") + "data_os_invertedEIso",
							nick_suffix=nick_suffix
					)
					Samples._add_input(
							config,
							self.files_ztt(channel),
							self.root_file_folder(channel),
							lumi,
							Samples.ztt_genmatch(channel)+"*"+self.get_weights_ztt(channel=channel,cut_type=cut_type,weight=weight)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=qcd_invertedIso_cut)+"*((q_1*q_2)>0.0)"+"*zPtReweightWeight"+"*"+self.decay_mode_reweight(channel)+"*"+zmm_cr_factor+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
							("noplot_" if not controlregions else "") + "ztt_ss_invertedEIso",
							nick_suffix=nick_suffix
					)
					if not (kwargs.get("no_ewk_samples", False) or kwargs.get("no_ewkz_as_dy", False)):
						Samples._add_input(
								config,
								self.files_ewkz_zll(channel),
								self.root_file_folder(channel),
								lumi,
								Samples.ztt_genmatch(channel)+"*"+self.get_weights_ztt(channel=channel,cut_type=cut_type,weight=weight,doStitching=False)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=qcd_invertedIso_cut)+"*((q_1*q_2)>0.0)"+"*"+self.decay_mode_reweight(channel)+"*"+self.ewkz_zll_stitchingweight()+"*"+zmm_cr_factor+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
								("noplot_" if not controlregions else "") + "ztt_ss_invertedEIso",
								nick_suffix=nick_suffix
						)
						Samples._add_input(
								config,
								self.files_ewkz_znn(channel),
								self.root_file_folder(channel),
								lumi,
								Samples.ztt_genmatch(channel)+"*"+self.get_weights_ztt(channel=channel,cut_type=cut_type,weight=weight,doStitching=False)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=qcd_invertedIso_cut)+"*((q_1*q_2)>0.0)"+"*"+self.decay_mode_reweight(channel)+"*"+self.ewkz_zll_stitchingweight()+"*"+zmm_cr_factor+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
								("noplot_" if not controlregions else "") + "ztt_ss_invertedEIso",
								nick_suffix=nick_suffix
						)
					Samples._add_input(
							config,
							self.files_zll(channel),
							self.root_file_folder(channel),
							lumi,
							mc_weight+"*"+weight+"*eventWeight*"+self.zll_stitchingweight()+"*"+Samples.zll_genmatch(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=qcd_invertedIso_cut)+"*((q_1*q_2)>0.0)"+"*zPtReweightWeight"+"*"+self.zll_zl_shape_weight(channel, cut_type)+"*"+zmm_cr_factor+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
							("noplot_" if not controlregions else "") + "zll_ss_invertedEIso",
							nick_suffix=nick_suffix
					)
					if not (kwargs.get("no_ewk_samples", False) or kwargs.get("no_ewkz_as_dy", False)):
						Samples._add_input(
								config,
								self.files_ewkz_zll(channel),
								self.root_file_folder(channel),
								lumi,
								mc_weight+"*"+weight+"*eventWeight*"+Samples.zll_genmatch(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=qcd_invertedIso_cut)+"*((q_1*q_2)>0.0)"+"*"+self.zll_zl_shape_weight(channel, cut_type)+"*"+self.ewkz_znn_stitchingweight()+"*"+zmm_cr_factor+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
								("noplot_" if not controlregions else "") + "zll_ss_invertedEIso",
								nick_suffix=nick_suffix
						)
						Samples._add_input(
								config,
								self.files_ewkz_znn(channel),
								self.root_file_folder(channel),
								lumi,
								mc_weight+"*"+weight+"*eventWeight*"+Samples.zll_genmatch(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=qcd_invertedIso_cut)+"*((q_1*q_2)>0.0)"+"*"+self.zll_zl_shape_weight(channel, cut_type)+"*"+self.ewkz_znn_stitchingweight()+"*"+zmm_cr_factor+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
								("noplot_" if not controlregions else "") + "zll_ss_invertedEIso",
								nick_suffix=nick_suffix
						)
					if not kwargs.get("no_ewk_samples", False) and kwargs.get("no_ewkz_as_dy", False):
						Samples._add_input(
								config,
								self.files_ewkz_zll(channel),
								self.root_file_folder(channel),
								lumi,
								mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=qcd_invertedIso_cut)+"*((q_1*q_2)>0.0)"+"*"+self.ewkz_zll_stitchingweight()+"*"+zmm_cr_factor,
								("noplot_" if not controlregions else "") + "ewkz_ss_invertedEIso",
								nick_suffix=nick_suffix
						)
						Samples._add_input(
								config,
								self.files_ewkz_znn(channel),
								self.root_file_folder(channel),
								lumi,
								mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=qcd_invertedIso_cut)+"*((q_1*q_2)>0.0)"+"*"+self.ewkz_znn_stitchingweight()+"*"+zmm_cr_factor,
								("noplot_" if not controlregions else "") + "ewkz_ss_invertedEIso",
								nick_suffix=nick_suffix
						)
					Samples._add_input(
							config,
							self.files_ttj(channel),
							self.root_file_folder(channel),
							lumi,
							mc_weight+"*"+weight+"*eventWeight*"+self.embedding_ttbarveto_weight(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=qcd_invertedIso_cut)+"*((q_1*q_2)>0.0)"+"*"+ "topPtReweightWeight"+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),			
							("noplot_" if not controlregions else "") + "ttj_ss_invertedEIso",
							nick_suffix=nick_suffix
					)
					Samples._add_input(
							config,
							self.files_vv(channel),
							self.root_file_folder(channel),
							lumi,
							mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=qcd_invertedIso_cut)+"*((q_1*q_2)>0.0)"+"*"+self.vv_stitchingweight()+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
							("noplot_" if not controlregions else "") + "vv_ss_invertedEIso",
							nick_suffix=nick_suffix
					)
					Samples._add_input(
							config,
							self.files_diboson(channel),
							self.root_file_folder(channel),
							lumi,
							mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=qcd_invertedIso_cut)+"*((q_1*q_2)>0.0)"+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
							("noplot_" if not controlregions else "") + "vv_ss_invertedEIso",
							nick_suffix=nick_suffix
					)
					Samples._add_input(
							config,
							self.files_wj(channel),
							self.root_file_folder(channel),
							lumi,
							mc_weight+"*"+qcd_shape_weight+"*eventWeight*"+self.wj_stitchingweight()+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=qcd_invertedIso_cut)+"*((q_1*q_2)>0.0)",
							("noplot_" if not controlregions else "") + "wj_ss_invertedEIso",
							nick_suffix=nick_suffix
					)
					Samples._add_input(
							config,
							self.files_data(channel),
							self.root_file_folder(channel),
							1.0,
							data_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os"] , cut_type=qcd_invertedIso_cut)+"*((q_1*q_2)>0.0)",
							("noplot_" if not controlregions else "") + "qcd_ss_invertedEIso",
							nick_suffix=nick_suffix
					)
					Samples._add_input(
							config,
							self.files_data(channel),
							self.root_file_folder(channel),
							1.0,
							data_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os"] , cut_type=qcd_invertedIso_cut)+"*((q_1*q_2)>0.0)",
							("noplot_" if not controlregions else "") + "data_ss_invertedEIso",
							nick_suffix=nick_suffix
					)
					if kwargs.get("ss_os_factor", 0.0) != 0.0:
						ss_os_factor = kwargs["ss_os_factor"]
					else:
						ss_os_factor = 1.0
						print "category", category
						if category != None:
							if channel == "et":
								ss_os_factor = 1.28 if "Boosted2D" in category else 1.0 if "Vbf2D" in category else 1.0 if "ZeroJet2D" in category else 1.0
							elif channel == "mt":
								ss_os_factor = 1.06 if "Boosted2D" in category else 1.0 if "Vbf2D" in category else 1.07 if "ZeroJet2D" in category else 1.0
					if not "EstimateWjetsAndQCD" in config.get("analysis_modules", []):
						config.setdefault("analysis_modules", []).append("EstimateWjetsAndQCD")
					if not "CalculateQcdOStoSSFactor" in config.get("analysis_modules", []):
						config.setdefault("analysis_modules", []).append("CalculateQcdOStoSSFactor")
					if channel == "et":
						config.setdefault("qcd_extrapolation_factors_ss_os", []).append(ss_os_factor)
					elif channel == "mt":
						config.setdefault("qcd_extrapolation_factors_ss_os", []).append(ss_os_factor)
					
					if controlregions:
						config.setdefault("qcd_shape_nicks", []).append("qcd"+nick_suffix)
						config.setdefault("qcd_yield_nicks", []).append("data_ss_lowmt"+nick_suffix)
						config.setdefault("qcd_extrapolate_ss_yield_nicks", []).append("data_ss_invertedEIso"+nick_suffix)
						config.setdefault("qcd_extrapolate_os_yield_nicks", []).append("data_os_invertedEIso"+nick_suffix)
						if not kwargs.get("no_ewk_samples", False) and kwargs.get("no_ewkz_as_dy", False):
							config.setdefault("qcd_yield_substract_nicks", []).append(" ".join([nick+nick_suffix for nick in "ztt_ss_lowmt zll_ss_lowmt ewkz_ss_lowmt ttj_ss_lowmt vv_ss_lowmt wj_ss_lowmt".split()]))
							config.setdefault("qcd_shape_substract_nicks", []).append(" ".join([nick+nick_suffix for nick in "noplot_ztt_shape_ss_qcd_control noplot_zll_shape_ss_qcd_control noplot_ewkz_shape_ss_qcd_control noplot_ttj_shape_ss_qcd_control noplot_vv_shape_ss_qcd_control noplot_wj_shape_ss_qcd_control".split()]))
							config.setdefault("qcd_shape_highmt_substract_nicks", []).append(" ".join([nick+nick_suffix for nick in "noplot_ztt_shape_ss_highmt noplot_zll_shape_ss_highmt noplot_ewkz_shape_ss_highmt noplot_ttj_shape_ss_highmt noplot_vv_shape_ss_highmt".split()]))
							config.setdefault("qcd_extrapolate_ss_substract_nicks", []).append(" ".join([nick+nick_suffix for nick in "ztt_ss_invertedEIso zll_ss_invertedEIso ewkz_ss_invertedEIso ttj_ss_invertedEIso vv_ss_invertedEIso wj_ss_invertedEIso".split()]))
							config.setdefault("qcd_extrapolate_os_substract_nicks", []).append(" ".join([nick+nick_suffix for nick in "ztt_os_invertedEIso zll_os_invertedEIso ewkz_os_invertedEIso ttj_os_invertedEIso vv_os_invertedEIso wj_os_invertedEIso".split()]))
						else:
							config.setdefault("qcd_yield_substract_nicks", []).append(" ".join([nick+nick_suffix for nick in "ztt_ss_lowmt zll_ss_lowmt ttj_ss_lowmt vv_ss_lowmt wj_ss_lowmt".split()]))
							config.setdefault("qcd_shape_substract_nicks", []).append(" ".join([nick+nick_suffix for nick in "noplot_ztt_shape_ss_qcd_control noplot_zll_shape_ss_qcd_control noplot_ttj_shape_ss_qcd_control noplot_vv_shape_ss_qcd_control noplot_wj_shape_ss_qcd_control".split()]))
							config.setdefault("qcd_shape_highmt_substract_nicks", []).append(" ".join([nick+nick_suffix for nick in "noplot_ztt_shape_ss_highmt noplot_zll_shape_ss_highmt noplot_ttj_shape_ss_highmt noplot_vv_shape_ss_highmt".split()]))
							config.setdefault("qcd_extrapolate_ss_substract_nicks", []).append(" ".join([nick+nick_suffix for nick in "ztt_ss_invertedEIso zll_ss_invertedEIso ttj_ss_invertedEIso vv_ss_invertedEIso wj_ss_invertedEIso".split()]))
							config.setdefault("qcd_extrapolate_os_substract_nicks", []).append(" ".join([nick+nick_suffix for nick in "ztt_os_invertedEIso zll_os_invertedEIso ttj_os_invertedEIso vv_os_invertedEIso wj_os_invertedEIso".split()]))
						config.setdefault("qcd_ss_highmt_shape_nicks", []).append("qcd_ss_highmt"+nick_suffix)
						config.setdefault("qcd_ss_lowmt_nicks", []).append("qcd_ss_lowmt"+nick_suffix)
						config.setdefault("qcd_os_highmt_nicks", []).append("qcd_os_highmt"+nick_suffix)
						config.setdefault("qcd_ss_invertedEIso_nicks", []).append("qcd_ss_invertedEIso"+nick_suffix)
						config.setdefault("qcd_os_invertedEIso_nicks", []).append("qcd_os_invertedEIso"+nick_suffix)
						
						if kwargs.get("wj_sf_shift", 0.0) != 0.0:
							config.setdefault("wjets_scale_factor_shifts", []).append(kwargs["wj_sf_shift"])

						for nick in ["ztt_ss_lowmt", "zll_ss_lowmt", "ttj_ss_lowmt", "vv_ss_lowmt", "wj_ss_lowmt","data_ss_lowmt", "qcd_ss_highmt", "qcd_os_highmt", "qcd_ss_lowmt"]+(["ewkz_ss_lowmt"] if (not kwargs.get("no_ewk_samples", False) and kwargs.get("no_ewkz_as_dy", False)) else []):
					
							if not kwargs.get("mssm", False):
								Samples._add_bin_corrections(config, nick, nick_suffix)
							Samples._add_plot(config, "bkg", "HIST", "F",  kwargs.get("color_label_key", nick), nick_suffix)
						
						
					else:
						config.setdefault("qcd_shape_nicks", []).append("qcd"+nick_suffix)
						config.setdefault("qcd_yield_nicks", []).append("noplot_data_ss_lowmt"+nick_suffix)
						config.setdefault("qcd_extrapolate_ss_yield_nicks", []).append("noplot_data_ss_invertedEIso"+nick_suffix)
						config.setdefault("qcd_extrapolate_os_yield_nicks", []).append("noplot_data_os_invertedEIso"+nick_suffix)
						if not kwargs.get("no_ewk_samples", False) and kwargs.get("no_ewkz_as_dy", False):
							config.setdefault("qcd_yield_substract_nicks", []).append(" ".join(["noplot_"+nick+nick_suffix for nick in "ztt_ss_lowmt zll_ss_lowmt ewkz_ss_lowmt ttj_ss_lowmt vv_ss_lowmt wj_ss_lowmt".split()]))
							config.setdefault("qcd_shape_substract_nicks", []).append(" ".join([nick+nick_suffix for nick in "noplot_ztt_shape_ss_qcd_control noplot_zll_shape_ss_qcd_control noplot_ewkz_shape_ss_qcd_control noplot_ttj_shape_ss_qcd_control noplot_vv_shape_ss_qcd_control noplot_wj_shape_ss_qcd_control".split()]))
							config.setdefault("qcd_shape_highmt_substract_nicks", []).append(" ".join([nick+nick_suffix for nick in "noplot_ztt_shape_ss_highmt noplot_zll_shape_ss_highmt noplot_ewkz_shape_ss_highmt noplot_ttj_shape_ss_highmt noplot_vv_shape_ss_highmt".split()]))
							config.setdefault("qcd_extrapolate_ss_substract_nicks", []).append(" ".join([nick+nick_suffix for nick in "noplot_ztt_ss_invertedEIso noplot_zll_ss_invertedEIso noplot_ewkz_ss_invertedEIso noplot_ttj_ss_invertedEIso noplot_vv_ss_invertedEIso noplot_wj_ss_invertedEIso".split()]))
							config.setdefault("qcd_extrapolate_os_substract_nicks", []).append(" ".join([nick+nick_suffix for nick in "noplot_ztt_os_invertedEIso noplot_zll_os_invertedEIso noplot_ewkz_os_invertedEIso noplot_ttj_os_invertedEIso noplot_vv_os_invertedEIso noplot_wj_os_invertedEIso".split()]))
						else:
							config.setdefault("qcd_yield_substract_nicks", []).append(" ".join(["noplot_"+nick+nick_suffix for nick in "ztt_ss_lowmt zll_ss_lowmt ttj_ss_lowmt vv_ss_lowmt wj_ss_lowmt".split()]))
							config.setdefault("qcd_shape_substract_nicks", []).append(" ".join([nick+nick_suffix for nick in "noplot_ztt_shape_ss_qcd_control noplot_zll_shape_ss_qcd_control noplot_ttj_shape_ss_qcd_control noplot_vv_shape_ss_qcd_control noplot_wj_shape_ss_qcd_control".split()]))
							config.setdefault("qcd_shape_highmt_substract_nicks", []).append(" ".join([nick+nick_suffix for nick in "noplot_ztt_shape_ss_highmt noplot_zll_shape_ss_highmt noplot_ttj_shape_ss_highmt noplot_vv_shape_ss_highmt".split()]))
							config.setdefault("qcd_extrapolate_ss_substract_nicks", []).append(" ".join([nick+nick_suffix for nick in "noplot_ztt_ss_invertedEIso noplot_zll_ss_invertedEIso noplot_ttj_ss_invertedEIso noplot_vv_ss_invertedEIso noplot_wj_ss_invertedEIso".split()]))
							config.setdefault("qcd_extrapolate_os_substract_nicks", []).append(" ".join([nick+nick_suffix for nick in "noplot_ztt_os_invertedEIso noplot_zll_os_invertedEIso noplot_ttj_os_invertedEIso noplot_vv_os_invertedEIso noplot_wj_os_invertedEIso".split()]))
						config.setdefault("qcd_ss_highmt_shape_nicks", []).append("noplot_qcd_ss_highmt"+nick_suffix)
						config.setdefault("qcd_ss_lowmt_nicks", []).append("noplot_qcd_ss_lowmt"+nick_suffix)
						config.setdefault("qcd_os_highmt_nicks", []).append("noplot_qcd_os_highmt"+nick_suffix)
						config.setdefault("qcd_ss_invertedEIso_nicks", []).append("noplot_qcd_ss_invertedEIso"+nick_suffix)
						config.setdefault("qcd_os_invertedEIso_nicks", []).append("noplot_qcd_os_invertedEIso"+nick_suffix)
						
						if kwargs.get("wj_sf_shift", 0.0) != 0.0:
							config.setdefault("wjets_scale_factor_shifts", []).append(kwargs["wj_sf_shift"])
				if channel == "em" or channel == "ttbar":
					for estimation_type in ["shape", "yield"]:
						qcd_weight = weight
						qcd_shape_cut = cut_type
						qcd_exclude_cuts = copy.deepcopy(exclude_cuts)+["os"]
						if category != None:
							if estimation_type == "shape" and ("ZeroJet2D" in category or "Boosted2D" in category):
								qcd_weight += "*(iso_1<0.3)*(iso_2>0.1)*(iso_2<0.3)"
								qcd_exclude_cuts += ["iso_1", "iso_2"]
							if estimation_type == "shape" and "Vbf2D" in category:
								qcd_weight += "*(iso_1<0.5)*(iso_2>0.2)*(iso_2<0.5)"
								qcd_exclude_cuts += ["iso_1", "iso_2"]
							if "newKIT" in estimationMethod and estimation_type == "shape": # take shape from full jet-bin
								qcd_shape_cut = qcd_shape_cut + ("relaxedETauMuTauWJ" if ("1jet" in category or "vbf" in category) else "")
								qcd_exclude_cuts.append("pzeta")
								qcd_weight = make_multiplication(Samples.get_jetbin(channel, category, weight))
						data_sample_weight = make_multiplication([data_weight,
											  qcd_weight,
											  "eventWeight",
											  self._cut_string(channel, exclude_cuts=qcd_exclude_cuts, cut_type=qcd_shape_cut),
											  "((q_1*q_2)>0.0)",
											  "emuQcdWeightNom"])
						mc_sample_weight = make_multiplication([  mc_weight,
											  qcd_weight,
											  "eventWeight",
											  self._cut_string(channel, exclude_cuts=qcd_exclude_cuts, cut_type=qcd_shape_cut),
											  "((q_1*q_2)>0.0)",
											  "emuQcdWeightNom"])
						Samples._add_input(
								config,
								self.files_wj(channel),
								self.root_file_folder(channel),
								lumi,
								mc_sample_weight+"*"+self.wj_stitchingweight()+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
								"noplot_wj_"+estimation_type,
								nick_suffix=nick_suffix
						)
						if (not kwargs.get("no_ewk_samples", False)):
							Samples._add_input(
									config,
									self.files_ewkwm(channel),
									self.root_file_folder(channel),
									lumi,
									mc_sample_weight+"*"+self.ewkwm_stitchingweight()+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
									"noplot_wj_"+estimation_type,
									nick_suffix=nick_suffix
							)
							Samples._add_input(
									config,
									self.files_ewkwp(channel),
									self.root_file_folder(channel),
									lumi,
									mc_sample_weight+"*"+self.ewkwp_stitchingweight()+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
									"noplot_wj_"+estimation_type,
									nick_suffix=nick_suffix
							)
						Samples._add_input(
								config,
								self.files_wgamma(channel),
								self.root_file_folder(channel),
								lumi,
								mc_sample_weight+"*"+self.wgamma_stitchingweight()+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
								"noplot_wj_"+estimation_type,
								nick_suffix=nick_suffix
						)
						Samples._add_input(
								config,
								self.files_wgamma_star(channel),
								self.root_file_folder(channel),
								lumi,
								mc_sample_weight+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
								"noplot_wj_"+estimation_type,
								nick_suffix=nick_suffix
						)
						Samples._add_input(
								config,
								self.files_data(channel),
								self.root_file_folder(channel),
								1.0,
								data_sample_weight,
								("qcd" if estimation_type=="shape" else "noplot_qcd_"+estimation_type),
								nick_suffix=nick_suffix
						)
						Samples._add_input(
								config,
								self.files_ztt(channel),
								self.root_file_folder(channel),
								lumi,
								Samples.ztt_genmatch(channel)+"*"+self.get_weights_ztt(channel=channel,cut_type=cut_type,mc_sample_weight=mc_sample_weight)+"*zPtReweightWeight"+"*"+zmm_cr_factor+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
								"noplot_ztt_"+estimation_type,
								nick_suffix=nick_suffix
						)
						if not (kwargs.get("no_ewk_samples", False) or kwargs.get("no_ewkz_as_dy", False)):
							Samples._add_input(
									config,
									self.files_ewkz_zll(channel),
									self.root_file_folder(channel),
									lumi,
									Samples.ztt_genmatch(channel)+"*"+self.get_weights_ztt(channel=channel,cut_type=cut_type,mc_sample_weight=mc_sample_weight, doStitching=False)+"*"+self.ewkz_zll_stitchingweight()+"*"+zmm_cr_factor+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
									"noplot_ztt_"+estimation_type,
									nick_suffix=nick_suffix
							)
							Samples._add_input(
									config,
									self.files_ewkz_znn(channel),
									self.root_file_folder(channel),
									lumi,
									Samples.ztt_genmatch(channel)+"*"+self.get_weights_ztt(channel=channel,cut_type=cut_type,mc_sample_weight=mc_sample_weight, doStitching=False)+"*"+self.ewkz_znn_stitchingweight()+"*"+zmm_cr_factor+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
									"noplot_ztt_"+estimation_type,
									nick_suffix=nick_suffix
							)
						Samples._add_input(
								config,
								self.files_zll(channel),
								self.root_file_folder(channel),
								lumi,
								self.zll_stitchingweight()+"*"+Samples.zll_genmatch(channel)+"*"+mc_sample_weight+"*zPtReweightWeight"+"*"+self.zll_zl_shape_weight(channel, cut_type)+"*"+zmm_cr_factor+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
								"noplot_zll_"+estimation_type,
								nick_suffix=nick_suffix
						)
						if not (kwargs.get("no_ewk_samples", False) or kwargs.get("no_ewkz_as_dy", False)):
							Samples._add_input(
									config,
									self.files_ewkz_zll(channel),
									self.root_file_folder(channel),
									lumi,
									Samples.zll_genmatch(channel)+"*"+mc_sample_weight+"*"+self.zll_zl_shape_weight(channel, cut_type)+"*"+self.ewkz_zll_stitchingweight()+"*"+zmm_cr_factor+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
									"noplot_zll_"+estimation_type,
									nick_suffix=nick_suffix
							)
							Samples._add_input(
									config,
									self.files_ewkz_znn(channel),
									self.root_file_folder(channel),
									lumi,
									Samples.zll_genmatch(channel)+"*"+mc_sample_weight+"*"+self.zll_zl_shape_weight(channel, cut_type)+"*"+self.ewkz_znn_stitchingweight()+"*"+zmm_cr_factor+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
									"noplot_zll_"+estimation_type,
									nick_suffix=nick_suffix
							)
						if not kwargs.get("no_ewk_samples", False) and kwargs.get("no_ewkz_as_dy", False):
							Samples._add_input(
									config,
									self.files_ewkz_zll(channel),
									self.root_file_folder(channel),
									lumi,
									mc_sample_weight+"*"+self.ewkz_zll_stitchingweight()+"*"+zmm_cr_factor+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
									"noplot_ewkz_"+estimation_type,
									nick_suffix=nick_suffix
							)
							Samples._add_input(
									config,
									self.files_ewkz_znn(channel),
									self.root_file_folder(channel),
									lumi,
									mc_sample_weight+"*"+self.ewkz_znn_stitchingweight()+"*"+zmm_cr_factor+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
									"noplot_ewkz_"+estimation_type,
									nick_suffix=nick_suffix
							)
						Samples._add_input(
								config,
								self.files_ttj(channel),
								self.root_file_folder(channel),
								lumi,
								mc_sample_weight+"*"+self.embedding_ttbarveto_weight(channel)+"*topPtReweightWeight"+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
								"noplot_ttj_"+estimation_type,
								nick_suffix=nick_suffix
						)
						Samples._add_input(
								config,
								self.files_vv(channel),
								self.root_file_folder(channel),
								lumi,
								mc_sample_weight+"*"+self.vv_stitchingweight()+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
								"noplot_vv_"+estimation_type,
								nick_suffix=nick_suffix
						)
						Samples._add_input(
								config,
								self.files_diboson(channel),
								self.root_file_folder(channel),
								lumi,
								mc_sample_weight+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
								"noplot_vv_"+estimation_type,
								nick_suffix=nick_suffix
						)
					if not "EstimateQcd" in config.get("analysis_modules", []):
						config.setdefault("analysis_modules", []).append("EstimateQcd")
					config.setdefault("qcd_shape_nicks", []).append("qcd"+nick_suffix)
					config.setdefault("qcd_yield_nicks", []).append("noplot_qcd_yield"+nick_suffix)
					if not kwargs.get("no_ewk_samples", False) and kwargs.get("no_ewkz_as_dy", False):
						config.setdefault("qcd_yield_subtract_nicks", []).append(" ".join(["noplot_"+nick+"_yield"+nick_suffix for nick in "ztt zll ewkz ttj vv wj".split()]))
						config.setdefault("qcd_shape_subtract_nicks", []).append(" ".join(["noplot_"+nick+"_shape"+nick_suffix for nick in "ztt zll ewkz ttj vv wj".split()]))
					else:
						config.setdefault("qcd_yield_subtract_nicks", []).append(" ".join(["noplot_"+nick+"_yield"+nick_suffix for nick in "ztt zll ttj vv wj".split()]))
						config.setdefault("qcd_shape_subtract_nicks", []).append(" ".join(["noplot_"+nick+"_shape"+nick_suffix for nick in "ztt zll ttj vv wj".split()]))
					if kwargs.get("ss_os_factor", 0.0) != 0.0:
						ss_os_factor = kwargs["ss_os_factor"]
					else:
						ss_os_factor = 2.22
						if category != None:
							ss_os_factor = 2.27 if "ZeroJet2D" in category else 2.26 if "Boosted2D" in category else 2.84 if "Vbf2D" in category else 2.22
					config.setdefault("qcd_extrapolation_factors_ss_os", []).append(ss_os_factor)
				if channel == "tt":
					if cut_type == "baseline2016":
						isolationDefinition = "((byMediumIsolationMVArun2v1DBoldDMwLT_1 > 0.5 && byLooseIsolationMVArun2v1DBoldDMwLT_2 > 0.5 && byTightIsolationMVArun2v1DBoldDMwLT_2 < 0.5) || (byMediumIsolationMVArun2v1DBoldDMwLT_2 > 0.5 && byLooseIsolationMVArun2v1DBoldDMwLT_1 > 0.5 && byTightIsolationMVArun2v1DBoldDMwLT_1 < 0.5))"
					elif cut_type == "smhtt2016":
						isolationDefinition = "((byMediumIsolationMVArun2v1DBoldDMwLT_1 > 0.5 && byLooseIsolationMVArun2v1DBoldDMwLT_2 > 0.5 && byTightIsolationMVArun2v1DBoldDMwLT_2 < 0.5) || (byMediumIsolationMVArun2v1DBoldDMwLT_2 > 0.5 && byLooseIsolationMVArun2v1DBoldDMwLT_1 > 0.5 && byTightIsolationMVArun2v1DBoldDMwLT_1 < 0.5))*((gen_match_1 == 5)*0.95 + (gen_match_1 != 5))*((gen_match_2 == 5)*0.95 + (gen_match_2 != 5))"
					else:
						isolationDefinition = "(byMediumIsolationMVArun2v1DBoldDMwLT_1 > 0.5 && byLooseIsolationMVArun2v1DBoldDMwLT_2 > 0.5 && byVTightIsolationMVArun2v1DBoldDMwLT_2 < 0.5)"
					data_selection_weights = {
						"qcd_shape" : data_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["iso_1", "iso_2"], cut_type=cut_type)+"*"+isolationDefinition,
						"qcd_signal_ss" : data_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=cut_type)+"*((q_1*q_2)>0.0)",
						"qcd_relaxed_ss" : data_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os", "iso_1", "iso_2"], cut_type=cut_type)+"*((q_1*q_2)>0.0)"+"*"+isolationDefinition
						}
					mc_selection_weights = {
						"qcd_shape" : mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["iso_1", "iso_2"], cut_type=cut_type)+"*"+isolationDefinition,
						"qcd_signal_ss" : mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=cut_type)+"*((q_1*q_2)>0.0)",
						"qcd_relaxed_ss" : mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os", "iso_1", "iso_2"], cut_type=cut_type)+"*((q_1*q_2)>0.0)"+"*"+isolationDefinition
						}
					for key in mc_selection_weights:
						Samples._add_input(
								config,
								self.files_wj(channel),
								self.root_file_folder(channel),
								lumi,
								self.wj_stitchingweight()+"*"+mc_selection_weights[key],
								"noplot_wj_"+key,
								nick_suffix=nick_suffix
						)
						if (not kwargs.get("no_ewk_samples", False)):
							Samples._add_input(
									config,
									self.files_ewkwm(channel),
									self.root_file_folder(channel),
									lumi,
									mc_selection_weights[key]+"*"+self.ewkwm_stitchingweight(),
									"noplot_wj_"+key,
									nick_suffix=nick_suffix
							)
							Samples._add_input(
									config,
									self.files_ewkwp(channel),
									self.root_file_folder(channel),
									lumi,
									mc_selection_weights[key]+"*"+self.ewkwp_stitchingweight(),
									"noplot_wj_"+key,
									nick_suffix=nick_suffix
							)
						Samples._add_input(
								config,
								self.files_data(channel),
								self.root_file_folder(channel),
								1.0,
								data_selection_weights[key],
								"qcd" if key == "qcd_shape" else "noplot_data_"+key,
								nick_suffix=nick_suffix
						)
						Samples._add_input(
								config,
								self.files_ztt(channel),
								self.root_file_folder(channel),
								lumi,
								Samples.ztt_genmatch(channel)+"*"+self.get_weights_ztt(channel=channel,cut_type=cut_type,mc_sample_weight=mc_selection_weights[key])+"*zPtReweightWeight"+"*"+zmm_cr_factor,
								"noplot_ztt_"+key,
								nick_suffix=nick_suffix
						)
						if not (kwargs.get("no_ewk_samples", False) or kwargs.get("no_ewkz_as_dy", False)):
							Samples._add_input(
									config,
									self.files_ewkz_zll(channel),
									self.root_file_folder(channel),
									lumi,
									Samples.ztt_genmatch(channel)+"*"+self.get_weights_ztt(channel=channel,cut_type=cut_type,mc_sample_weight=mc_selection_weights[key], doStitching=False)+"*"+self.ewkz_zll_stitchingweight()+"*"+zmm_cr_factor,
									"noplot_ztt_"+key,
									nick_suffix=nick_suffix
							)
							Samples._add_input(
									config,
									self.files_ewkz_znn(channel),
									self.root_file_folder(channel),
									lumi,
									Samples.ztt_genmatch(channel)+"*"+self.get_weights_ztt(channel=channel,cut_type=cut_type,mc_sample_weight=mc_selection_weights[key], doStitching=False)+"*"+self.ewkz_znn_stitchingweight()+"*"+zmm_cr_factor,
									"noplot_ztt_"+key,
									nick_suffix=nick_suffix
							)
						Samples._add_input(
								config,
								self.files_zll(channel),
								self.root_file_folder(channel),
								lumi,
								mc_selection_weights[key]+"*"+self.zll_stitchingweight()+"*"+Samples.zll_genmatch(channel)+"*"+"zPtReweightWeight"+"*"+self.zll_zl_shape_weight(channel, cut_type)+"*"+zmm_cr_factor,
								"noplot_zll_"+key,
								nick_suffix=nick_suffix
						)
						if not (kwargs.get("no_ewk_samples", False) or kwargs.get("no_ewkz_as_dy", False)):
							Samples._add_input(
									config,
									self.files_ewkz_zll(channel),
									self.root_file_folder(channel),
									lumi,
									mc_selection_weights[key]+"*"+Samples.zll_genmatch(channel)+"*"+self.zll_zl_shape_weight(channel, cut_type)+"*"+self.ewkz_zll_stitchingweight()+"*"+zmm_cr_factor,
									"noplot_zll_"+key,
									nick_suffix=nick_suffix
							)
							Samples._add_input(
									config,
									self.files_ewkz_znn(channel),
									self.root_file_folder(channel),
									lumi,
									mc_selection_weights[key]+"*"+Samples.zll_genmatch(channel)+"*"+self.zll_zl_shape_weight(channel, cut_type)+"*"+self.ewkz_znn_stitchingweight()+"*"+zmm_cr_factor,
									"noplot_zll_"+key,
									nick_suffix=nick_suffix
							)
						if not kwargs.get("no_ewk_samples", False) and kwargs.get("no_ewkz_as_dy", False):
							Samples._add_input(
									config,
									self.files_ewkz_zll(channel),
									self.root_file_folder(channel),
									lumi,
									mc_selection_weights[key]+"*"+self.ewkz_zll_stitchingweight()+"*"+zmm_cr_factor,
									"noplot_ewkz_"+key,
									nick_suffix=nick_suffix
							)
							Samples._add_input(
									config,
									self.files_ewkz_znn(channel),
									self.root_file_folder(channel),
									lumi,
									mc_selection_weights[key]+"*"+self.ewkz_znn_stitchingweight()+"*"+zmm_cr_factor,
									"noplot_ewkz_"+key,
									nick_suffix=nick_suffix
							)
						Samples._add_input(
								config,
								self.files_ttj(channel),
								self.root_file_folder(channel),
								lumi,
								mc_selection_weights[key]+"*"+self.embedding_ttbarveto_weight(channel)+"*topPtReweightWeight",
								"noplot_ttj_"+key,
								nick_suffix=nick_suffix
						)
						Samples._add_input(
								config,
								self.files_vv(channel),
								self.root_file_folder(channel),
								lumi,
								mc_selection_weights[key]+"*"+self.vv_stitchingweight(),
								"noplot_vv_"+key,
								nick_suffix=nick_suffix
						)
						Samples._add_input(
								config,
								self.files_diboson(channel),
								self.root_file_folder(channel),
								lumi,
								mc_selection_weights[key],
								"noplot_vv_"+key,
								nick_suffix=nick_suffix
						)
					if not "EstimateQcdTauHadTauHad" in config.get("analysis_modules", []):
						config.setdefault("analysis_modules", []).append("EstimateQcdTauHadTauHad")
					config.setdefault("qcd_data_shape_nicks", []).append("qcd"+nick_suffix)
					config.setdefault("qcd_data_signal_control_nicks", []).append("noplot_data_qcd_signal_ss"+nick_suffix)
					config.setdefault("qcd_data_relaxed_control_nicks", []).append("noplot_data_qcd_relaxed_ss"+nick_suffix)
					if not kwargs.get("no_ewk_samples", False) and kwargs.get("no_ewkz_as_dy", False):
						config.setdefault("qcd_data_subtract_nicks", []).append(" ".join([nick+nick_suffix for nick in "noplot_ztt_qcd_shape noplot_zll_qcd_shape noplot_ewkz_qcd_shape noplot_ttj_qcd_shape noplot_vv_qcd_shape noplot_wj_qcd_shape".split()]))
						config.setdefault("qcd_control_signal_subtract_nicks", []).append(" ".join([nick+nick_suffix for nick in "noplot_ztt_qcd_signal_ss noplot_zll_qcd_signal_ss noplot_ewkz_qcd_signal_ss noplot_ttj_qcd_signal_ss noplot_vv_qcd_signal_ss noplot_wj_qcd_signal_ss".split()]))
						config.setdefault("qcd_control_relaxed_subtract_nicks", []).append(" ".join([nick+nick_suffix for nick in "noplot_ztt_qcd_relaxed_ss noplot_zll_qcd_relaxed_ss noplot_ewkz_qcd_relaxed_ss noplot_ttj_qcd_relaxed_ss noplot_vv_qcd_relaxed_ss noplot_wj_qcd_relaxed_ss".split()]))
					else:
						config.setdefault("qcd_data_subtract_nicks", []).append(" ".join([nick+nick_suffix for nick in "noplot_ztt_qcd_shape noplot_zll_qcd_shape noplot_ttj_qcd_shape noplot_vv_qcd_shape noplot_wj_qcd_shape".split()]))
						config.setdefault("qcd_control_signal_subtract_nicks", []).append(" ".join([nick+nick_suffix for nick in "noplot_ztt_qcd_signal_ss noplot_zll_qcd_signal_ss noplot_ttj_qcd_signal_ss noplot_vv_qcd_signal_ss noplot_wj_qcd_signal_ss".split()]))
						config.setdefault("qcd_control_relaxed_subtract_nicks", []).append(" ".join([nick+nick_suffix for nick in "noplot_ztt_qcd_relaxed_ss noplot_zll_qcd_relaxed_ss noplot_ttj_qcd_relaxed_ss noplot_vv_qcd_relaxed_ss noplot_wj_qcd_relaxed_ss".split()]))
				elif channel in ["mm","ee"]:
					log.error("Sample config (QCD) currently not implemented for channel \"%s\"!" % channel)
		else:
			log.error("Sample config (QCD) currently not implemented for channel \"%s\"!" % channel)

		if not kwargs.get("no_plot", False):
			if not kwargs.get("mssm", False):
				Samples._add_bin_corrections(config, "qcd", nick_suffix)
			Samples._add_plot(config, "bkg", "HIST", "F", "qcd", nick_suffix)
		
		if controlregions:
			for nick in ["ztt_os_invertedEIso", "zll_os_invertedEIso", "ttj_os_invertedEIso", "vv_os_invertedEIso", "wj_os_invertedEIso", "qcd_os_invertedEIso","data_os_invertedEIso", "ztt_ss_invertedEIso", "zll_ss_invertedEIso", "ttj_ss_invertedEIso", "vv_ss_invertedEIso", "wj_ss_invertedEIso", "qcd_ss_invertedEIso","data_ss_invertedEIso"]+(["ewkz_os_invertedEIso","ewkz_ss_invertedEIso"] if (not kwargs.get("no_ewk_samples", False) and kwargs.get("no_ewkz_as_dy", False)) else []):
				if not kwargs.get("mssm", False):
					Samples._add_bin_corrections(config, nick, nick_suffix)
				Samples._add_plot(config, "bkg", "HIST", "F",  kwargs.get("color_label_key", nick), nick_suffix)
							
		return config
