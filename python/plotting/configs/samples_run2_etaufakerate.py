
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import copy

import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.samples as samples


default_lumi = 2245

class Samples(samples.SamplesBase):
	
	@staticmethod
	def ztt_genmatch(channel):
		if channel in ["mt", "et"]:
			return "(gen_match_2 == 5)*stitchWeightZTT*"
		elif channel == "tt":
			return "(gen_match_1 == 5 && gen_match_2 == 5)*stitchWeightZTT*"
		else:
			log.fatal("No ZTT selection implemented for channel \"%s\"!" % channel)
			sys.exit(1)
	
	@staticmethod
	def zl_genmatch(channel):
		if channel in ["mt", "et", "tt"]:
			return "(gen_match_2 < 5)*stitchWeightZLL*"
		else:
			log.fatal("No ZL selection implemented for channel \"%s\"!" % channel)
			sys.exit(1)
	
	@staticmethod
	def zj_genmatch(channel):
		if channel in ["mt", "et"]:
			return "(gen_match_2 == 6)*stitchWeightZLL*"
		elif channel == "tt":
			return "(gen_match_2 == 6 || gen_match_1 == 6)*stitchWeightZLL*"
		else:
			log.fatal("No ZJ selection implemented for channel \"%s\"!" % channel)
			sys.exit(1)
	
	@staticmethod
	def zll_genmatch(channel):
		if channel in ["mt", "et", "tt"]:
			return "(gen_match_2 < 5 || gen_match_2 == 6)*stitchWeightZLL*"
		else:
			log.fatal("No ZLL selection implemented for channel \"%s\"!" % channel)
			sys.exit(1)

	def __init__(self):
		super(Samples, self).__init__()
		
		self.period = "run2"
	
	def get_config(self, samples, channel, category, nick_suffix="", postfit_scales=None, blind_expression=None, **kwargs):
		config = super(Samples, self).get_config(samples, channel, category, nick_suffix=nick_suffix, postfit_scales=postfit_scales, **kwargs)
		
		# blinding (of data)
		config["weights"] = [weight.format(blind=self.expressions.replace_expressions("blind_"+str(blind_expression)) if "blind_"+str(blind_expression) in self.expressions.expressions_dict else "1.0") for weight in config["weights"]]
		
		# execute bin correction modules after possible background estimation modules
		config.setdefault("analysis_modules", []).sort(key=lambda module: module in ["BinErrorsOfEmptyBins", "CorrectNegativeBinContents"])
		
		return config
	
	def data(self, config, channel, category, weight, nick_suffix, exclude_cuts=None, cut_type="baseline", **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []
		
		scale_factor = 1.0
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("data_obs", 1.0)
		
		if channel == "mt":
			Samples._add_input(
					config,
					"SingleMuon_Run2015?_*_13TeV_*AOD/*.root",
					channel+"_tagEleEsNom_probeTauEsNom_probeEleEsNom/ntuple",
					1.0,
					weight+"*eventWeight*" + self.cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type),
					"data",
					nick_suffix=nick_suffix
			)
		elif channel == "et":
			Samples._add_input(
					config,
					"SingleElectron_Run2015?_*_13TeV_*AOD/*.root",
					channel+"_tagEleEsNom_probeTauEsNom_probeEleEsNom/ntuple",
					1.0,
					weight+"*eventWeight*" + self.cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type),
					"data",
					nick_suffix=nick_suffix
			)
		elif channel == "tt":
			Samples._add_input(
					config,
					"Tau_Run2015?_*_13TeV_*AOD/*.root",
					channel+"_tagEleEsNom_probeTauEsNom_probeEleEsNom/ntuple",
					1.0,
					weight+"*eventWeight*" + self.cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type),
					"data",
					nick_suffix=nick_suffix
			)
		else:
			log.error("Sample config (Data) currently not implemented for channel \"%s\"!" % channel)
		
		Samples._add_plot(config, "data", "E", "ELP", "data", nick_suffix)
		return config
	
	def ztt(self, config, channel, category, weight, nick_suffix, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []
		
		scale_factor = 1.0
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("ZTT", 1.0)
		
		if channel in ["mt", "et", "tt"]:
			Samples._add_input(
					config,
					"DY*JetsToLLM*_RunIIFall15*_*_13TeV_*AOD_*/*.root",
					channel+"_tagEleEsNom_probeTauEsNom_probeEleEsNom/ntuple",
					lumi,
					weight+"*eventWeight*" + Samples.ztt_genmatch(channel) + self.cut_string(channel, exclude_cuts=exclude_cuts+["blind"], cut_type=cut_type),
					"ztt",
					nick_suffix=nick_suffix
			)
		else:
			log.error("Sample config (ZTT) currently not implemented for channel \"%s\"!" % channel)
		
		Samples._add_bin_corrections(config, "ztt", nick_suffix)
		Samples._add_plot(config, "bkg", "HIST", "F", "ztt", nick_suffix)
		
		return config
	
	def zl(self, config, channel, category, weight, nick_suffix, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []
		
		scale_factor = lumi
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("ZL", 1.0)
		
		if channel in ["mt", "et", "tt"]:
			Samples._add_input(
					config,
					"DY*JetsToLLM10to50_RunIIFall15*_*_13TeV_*AOD_*/*.root DY*JetsToLLM50_RunIIFall15*_*_13TeV_*AOD_*/*.root",
					channel+"_tagEleEsNom_probeTauEsNom_probeEleEsNom/ntuple",
					lumi,
					weight+"*eventWeight*" + Samples.zl_genmatch(channel) + self.cut_string(channel, exclude_cuts=exclude_cuts+["blind"], cut_type=cut_type),
					"zl",
					nick_suffix=nick_suffix
			)
		else:
			log.error("Sample config (ZL) currently not implemented for channel \"%s\"!" % channel)
		
		Samples._add_bin_corrections(config, "zl", nick_suffix)
		Samples._add_plot(config, "bkg", "HIST", "F", "zl", nick_suffix)
		return config
	
	def zj(self, config, channel, category, weight, nick_suffix, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []
		
		scale_factor = lumi
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("ZJ", 1.0)
		
		if channel in ["mt", "et", "tt"]:
			Samples._add_input(
					config,
					"DY*JetsToLLM10to50_RunIIFall15*_*_13TeV_*AOD_*/*.root DY*JetsToLLM50_RunIIFall15*_*_13TeV_*AOD_*/*.root",
					channel+"_tagEleEsNom_probeTauEsNom_probeEleEsNom/ntuple",
					lumi,
					weight+"*eventWeight*" + Samples.zj_genmatch(channel) + self.cut_string(channel, exclude_cuts=exclude_cuts+["blind"], cut_type=cut_type),
					"zj",
					nick_suffix=nick_suffix
			)
		else:
			log.error("Sample config (ZJ) currently not implemented for channel \"%s\"!" % channel)
		
		Samples._add_bin_corrections(config, "zj", nick_suffix)
		Samples._add_plot(config, "bkg", "HIST", "F", "zj", nick_suffix)
		return config
	
	def zll(self, config, channel, category, weight, nick_suffix, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []
		
		scale_factor = lumi
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("ZLL", 1.0)
		
		if channel in ["mt", "et", "tt"]:
			Samples._add_input(
					config,
					"DY*JetsToLLM10to50_RunIIFall15*_*_13TeV_*AOD_*/*.root DY*JetsToLLM50_RunIIFall15*_*_13TeV_*AOD_*/*.root",
					channel+"_tagEleEsNom_probeTauEsNom_probeEleEsNom/ntuple",
					lumi,
					weight+"*eventWeight*" + Samples.zll_genmatch(channel) + self.cut_string(channel, exclude_cuts=exclude_cuts+["blind"], cut_type=cut_type),
					"zll",
					nick_suffix=nick_suffix
			)
		else:
			log.error("Sample config (ZLL) currently not implemented for channel \"%s\"!" % channel)
		
		Samples._add_bin_corrections(config, "zll", nick_suffix)
		Samples._add_plot(config, "bkg", "HIST", "F", "zll", nick_suffix)
		return config

	def ttj(self, config, channel, category, weight, nick_suffix, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []
		
		scale_factor = lumi
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("TTJ", 1.0)
		
		if channel in ["mt", "et", "tt"]:
			Samples._add_input(
					config,
					"TT_RunIIFall15*_*_13TeV_*AOD_powheg-pythia8/*.root",
					channel+"_tagEleEsNom_probeTauEsNom_probeEleEsNom/ntuple",
					lumi,
					weight+"*eventWeight*" + self.cut_string(channel, exclude_cuts=exclude_cuts+["blind"], cut_type=cut_type),
					"ttj",
					nick_suffix=nick_suffix
			)
		else:
			log.error("Sample config (TTJ) currently not implemented for channel \"%s\"!" % channel)
		
		Samples._add_bin_corrections(config, "ttj", nick_suffix)
		Samples._add_plot(config, "bkg", "HIST", "F", "ttj", nick_suffix)
		return config

	def vv(self, config, channel, category, weight, nick_suffix, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []
		
		scale_factor = lumi
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("Dibosons", 1.0)
		
		if channel in ["mt", "et", "tt"]:
			Samples._add_input(
					config,
					"ST*_RunIIFall15*_*_13TeV_*AOD_powheg-pythia8/*root WW*_RunIIFall15*_*_13TeV_*AOD_*/*.root WZ*_RunIIFall15*_*_13TeV_*AOD_*/*.root ZZ*_RunIIFall15*_*_13TeV_*AOD_*/*.root VV*_RunIIFall15*_*_13TeV_*AOD_*/*.root",
					channel+"_tagEleEsNom_probeTauEsNom_probeEleEsNom/ntuple",
					lumi,
					weight+"*eventWeight*" + self.cut_string(channel, exclude_cuts=exclude_cuts+["blind"], cut_type=cut_type),
					"vv",
					nick_suffix=nick_suffix
			)
		else:
			log.error("Sample config (VV) currently not implemented for channel \"%s\"!" % channel)
		
		Samples._add_bin_corrections(config, "vv", nick_suffix)
		Samples._add_plot(config, "bkg", "HIST", "F", "vv", nick_suffix)
		return config
	
	def wj(self, config, channel, category, weight, nick_suffix, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []
		
		scale_factor = lumi
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("WJets", 1.0)
		
		if channel in ["mt", "et"]:
			shape_weight = weight+"*stitchWeightWJ*eventWeight*" + self.cut_string(channel, exclude_cuts=exclude_cuts+["blind"], cut_type=cut_type)
			#if (not category is None) and (category != ""):
				## relaxed isolation
				#shape_weight = weight+"*eventWeight*" + self.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "iso_2"], cut_type=cut_type) + "*(byCombinedIsolationDeltaBetaCorrRaw3Hits_2<10.0)"
			
			Samples._add_input(
					config,
					"W*JetsToLNu_RunIIFall15*_*_13TeV_*AOD_*/*.root",
					channel+"_tagEleEsNom_probeTauEsNom_probeEleEsNom/ntuple",
					lumi,
					shape_weight,
					"wj",
					nick_suffix=nick_suffix
			)
			Samples._add_input(
					config,
					"SingleMuon_Run2015?_*_13TeV_*AOD/*.root" if channel == "mt" else "SingleElectron_Run2015?_*_13TeV_*AOD/*root",
					channel+"_tagEleEsNom_probeTauEsNom_probeEleEsNom/ntuple",
					1.0,
					"eventWeight*" + self.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "mt"], cut_type=cut_type) + "*(mt_1>70.0)",
					"noplot_wj_data_control"
			)
			Samples._add_input(
					config,
					"DY*JetsToLLM*_RunIIFall15*_*_13TeV_*AOD_*/*.root",
					channel+"_tagEleEsNom_probeTauEsNom_probeEleEsNom/ntuple",
					lumi,
					"eventWeight*" + Samples.ztt_genmatch(channel) + self.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "mt"], cut_type=cut_type) + "*(mt_1>70.0)",
					"noplot_ztt_mc_wj_control",
					nick_suffix=nick_suffix
			)
			Samples._add_input(
					config,
					"DY*JetsToLLM10to50_RunIIFall15*_*_13TeV_*AOD_*/*.root DY*JetsToLLM50_RunIIFall15*_*_13TeV_*AOD_*/*.root",
					channel+"_tagEleEsNom_probeTauEsNom_probeEleEsNom/ntuple",
					lumi,
					"eventWeight*" + Samples.zll_genmatch(channel) + self.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "mt"], cut_type=cut_type) + "*(mt_1>70.0)",
					"noplot_zll_wj_control",
					nick_suffix=nick_suffix
			)
			Samples._add_input(
					config,
					"TT_RunIIFall15*_*_13TeV_*AOD_powheg-pythia8/*.root",
					channel+"_tagEleEsNom_probeTauEsNom_probeEleEsNom/ntuple",
					lumi,
					"eventWeight*" + self.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "mt"], cut_type=cut_type) + "*(mt_1>70.0)",
					"noplot_ttj_wj_control",
					nick_suffix=nick_suffix
			)
			Samples._add_input(
					config,
					"ST*_RunIIFall15*_*_13TeV_*AOD_powheg-pythia8/*root WW*_RunIIFall15*_*_13TeV_*AOD_*/*.root WZ*_RunIIFall15*_*_13TeV_*AOD_*/*.root ZZ*_RunIIFall15*_*_13TeV_*AOD_*/*.root VV*_RunIIFall15*_*_13TeV_*AOD_*/*.root",
					channel+"_tagEleEsNom_probeTauEsNom_probeEleEsNom/ntuple",
					lumi,
					"eventWeight*" + self.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "mt"], cut_type=cut_type) + "*(mt_1>70.0)",
					"noplot_vv_wj_control",
					nick_suffix=nick_suffix
			)
			Samples._add_input(
					config,
					"W*JetsToLNu_RunIIFall15*_*_13TeV_*AOD_*/*.root",
					channel+"_tagEleEsNom_probeTauEsNom_probeEleEsNom/ntuple",
					lumi,
					weight+"*stitchWeightWJ*eventWeight*" + self.cut_string(channel, exclude_cuts=exclude_cuts+["blind"], cut_type=cut_type),
					"noplot_wj_mc_signal",
					nick_suffix=nick_suffix
			)
			Samples._add_input(
					config,
					"W*JetsToLNu_RunIIFall15*_*_13TeV_*AOD_*/*.root",
					channel+"_tagEleEsNom_probeTauEsNom_probeEleEsNom/ntuple",
					lumi,
					"stitchWeightWJ*eventWeight*" + self.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "mt"], cut_type=cut_type) + "*(mt_1>70.0)",
					"noplot_wj_mc_control",
					nick_suffix=nick_suffix
			)

			if not "EstimateWjets" in config.get("analysis_modules", []):
				config.setdefault("analysis_modules", []).append("EstimateWjets")
			config.setdefault("wjets_from_mc", []).append(False)
			config.setdefault("wjets_shape_nicks", []).append("wj"+nick_suffix)
			config.setdefault("wjets_data_control_nicks", []).append("noplot_wj_data_control"+nick_suffix)
			config.setdefault("wjets_data_substract_nicks", []).append(" ".join([nick+nick_suffix for nick in "noplot_ztt_mc_wj_control noplot_zll_wj_control noplot_ttj_wj_control noplot_vv_wj_control".split()]))
			config.setdefault("wjets_mc_signal_nicks", []).append("noplot_wj_mc_signal"+nick_suffix)
			config.setdefault("wjets_mc_control_nicks", []).append("noplot_wj_mc_control"+nick_suffix)

		elif channel in ["tt"]:
			Samples._add_input(
					config,
					"W*JetsToLNu_RunIIFall15*_*_13TeV_*AOD_*/*.root",
					channel+"_tagEleEsNom_probeTauEsNom_probeEleEsNom/ntuple",
					lumi,
					weight+"*stitchWeightWJ*eventWeight*" + self.cut_string(channel, exclude_cuts=exclude_cuts+["blind"], cut_type=cut_type),
					"wj",
					nick_suffix=nick_suffix
			)
		else:	
			log.error("Sample config (WJets) currently not implemented for channel \"%s\"!" % channel)
		
		if not kwargs.get("no_plot", False):
			Samples._add_bin_corrections(config, "wj", nick_suffix)
			Samples._add_plot(config, "bkg", "HIST", "F", "wj", nick_suffix)
		return config

	def qcd(self, config, channel, category, weight, nick_suffix, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []
		
		scale_factor = 1.0
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("QCD", 1.0)
		
		if channel in ["et", "mt", "tt"]:

			# WJets for QCD estimate
			Samples._add_input(
					config,
					"W*JetsToLNu_RunIIFall15*_*_13TeV_*AOD_*/*.root",
					channel+"_tagEleEsNom_probeTauEsNom_probeEleEsNom/ntuple",
					lumi,
					"stitchWeightWJ*eventWeight*" + self.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "os"], cut_type=cut_type) + "*((q_1*q_2)>0.0)",
					"noplot_wj_ss",
					nick_suffix=nick_suffix
			)
			
			if channel in ["mt", "et"]:
				Samples._add_input(
						config,
						"SingleMuon_Run2015?_*_13TeV_*AOD/*.root" if channel == "mt" else ("SingleElectron_Run2015?_*_13TeV_*AOD/*root" if channel == "et" else "MuonEG_Run2015?_*_13TeV_*AOD/*.root"),
						channel+"_tagEleEsNom_probeTauEsNom_probeEleEsNom/ntuple",
						1.0,
						"eventWeight*" + self.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "os", "mt"], cut_type=cut_type) + "*((q_1*q_2)>0.0)*(mt_1>70.0)",
						"noplot_wj_ss_data_control",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						"DY*JetsToLLM*_RunIIFall15*_*_13TeV_*AOD_*/*.root",
						channel+"_tagEleEsNom_probeTauEsNom_probeEleEsNom/ntuple",
						lumi,
						"eventWeight*" + Samples.ztt_genmatch(channel) + self.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "os", "mt"], cut_type=cut_type) + "*((q_1*q_2)>0.0)*(mt_1>70.0)",
						"noplot_ztt_ss_mc_wj_control",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						"DY*JetsToLLM10to50_RunIIFall15*_*_13TeV_*AOD_*/*.root DY*JetsToLLM50_RunIIFall15*_*_13TeV_*AOD_*/*.root",
						channel+"_tagEleEsNom_probeTauEsNom_probeEleEsNom/ntuple",
						lumi,
						"eventWeight*" + Samples.zll_genmatch(channel) + self.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "os", "mt"], cut_type=cut_type) + "*((q_1*q_2)>0.0)*(mt_1>70.0)",
						"noplot_zll_ss_wj_control",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						"TT_RunIIFall15*_*_13TeV_*AOD_powheg-pythia8/*.root",
						channel+"_tagEleEsNom_probeTauEsNom_probeEleEsNom/ntuple",
						lumi,
						"eventWeight*" + self.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "os", "mt"], cut_type=cut_type) + "*((q_1*q_2)>0.0)*(mt_1>70.0)",
						"noplot_ttj_ss_wj_control",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						"ST*_RunIIFall15*_*_13TeV_*AOD_powheg-pythia8/*root WW*_RunIIFall15*_*_13TeV_*AOD_*/*.root WZ*_RunIIFall15*_*_13TeV_*AOD_*/*.root ZZ*_RunIIFall15*_*_13TeV_*AOD_*/*.root VV*_RunIIFall15*_*_13TeV_*AOD_*/*.root",
						channel+"_tagEleEsNom_probeTauEsNom_probeEleEsNom/ntuple",
						lumi,
						"eventWeight*" + self.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "os", "mt"], cut_type=cut_type) + "*((q_1*q_2)>0.0)*(mt_1>70.0)",
						"noplot_vv_ss_wj_control",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						"W*JetsToLNu_RunIIFall15*_*_13TeV_*AOD_*/*.root",
						channel+"_tagEleEsNom_probeTauEsNom_probeEleEsNom/ntuple",
						lumi,
						"stitchWeightWJ*eventWeight*" + self.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "os"], cut_type=cut_type) + "*((q_1*q_2)>0.0)",
						"noplot_wj_ss_mc_signal",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						"W*JetsToLNu_RunIIFall15*_*_13TeV_*AOD_*/*.root",
						channel+"_tagEleEsNom_probeTauEsNom_probeEleEsNom/ntuple",
						lumi,
						"stitchWeightWJ*eventWeight*" + self.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "os", "mt"], cut_type=cut_type) + "*((q_1*q_2)>0.0)*(mt_1>70.0)",
						"noplot_wj_ss_mc_control",
						nick_suffix=nick_suffix
				)
			
				if not "EstimateWjets" in config.get("analysis_modules", []):
					config.setdefault("analysis_modules", []).append("EstimateWjets")
				config.setdefault("wjets_from_mc", []).append(False)
				config.setdefault("wjets_shape_nicks", []).append("noplot_wj_ss"+nick_suffix)
				config.setdefault("wjets_data_control_nicks", []).append("noplot_wj_ss_data_control"+nick_suffix)
				config.setdefault("wjets_data_substract_nicks", []).append(" ".join([nick+nick_suffix for nick in "noplot_ztt_ss_mc_wj_control noplot_zll_ss_wj_control noplot_ttj_ss_wj_control noplot_vv_ss_wj_control".split()]))
				config.setdefault("wjets_mc_signal_nicks", []).append("noplot_wj_ss_mc_signal"+nick_suffix)
				config.setdefault("wjets_mc_control_nicks", []).append("noplot_wj_ss_mc_control"+nick_suffix)
			
			# QCD
			shape_weight = weight+"*eventWeight*" + self.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "os"], cut_type=cut_type) + "*((q_1*q_2)>0.0)"
			#if (not category is None) and (category != ""):
				## relaxed/inverted isolation
				#if channel in ["et", "mt"]:
					#shape_weight = weight+"*eventWeight*" + self.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "os", "iso_2"], cut_type=cut_type) + "*((q_1*q_2)>0.0)"+"*(byCombinedIsolationDeltaBetaCorrRaw3Hits_2<10.0)"
				#else:
					#shape_weight = weight+"*eventWeight*" + self.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "os", "iso_1", "iso_2"], cut_type=cut_type) + "*((q_1*q_2)>0.0)"
			
			Samples._add_input(
					config,
					"SingleMuon_Run2015?_*_13TeV_*AOD/*.root" if channel == "mt" else ("SingleElectron_Run2015?_*_13TeV_*AOD/*root" if channel == "et" else "MuonEG_Run2015?_*_13TeV_*AOD/*.root" if channel == "em" else "Tau_Run2015?_*_13TeV_*AOD/*.root"),
					channel+"_tagEleEsNom_probeTauEsNom_probeEleEsNom/ntuple",
					1.0,
					shape_weight,
					"qcd",
					nick_suffix=nick_suffix
			)
			Samples._add_input(
					config,
					"SingleMuon_Run2015?_*_13TeV_*AOD/*.root" if channel == "mt" else ("SingleElectron_Run2015?_*_13TeV_*AOD/*root" if channel == "et" else "MuonEG_Run2015?_*_13TeV_*AOD/*.root" if channel == "em" else "Tau_Run2015?_*_13TeV_*AOD/*.root"),
					channel+"_tagEleEsNom_probeTauEsNom_probeEleEsNom/ntuple",
					1.0,
					weight+"*eventWeight*" + self.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "os"], cut_type=cut_type) + "*((q_1*q_2)>0.0)",
					"noplot_data_qcd_yield",
					nick_suffix=nick_suffix
			)
			Samples._add_input(
					config,
					"SingleMuon_Run2015?_*_13TeV_*AOD/*.root" if channel == "mt" else ("SingleElectron_Run2015?_*_13TeV_*AOD/*root" if channel == "et" else "MuonEG_Run2015?_*_13TeV_*AOD/*.root" if channel == "em" else "Tau_Run2015?_*_13TeV_*AOD/*.root"),
					channel+"_tagEleEsNom_probeTauEsNom_probeEleEsNom/ntuple",
					1.0,
					"eventWeight*" + self.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "os"], cut_type=cut_type) + "*((q_1*q_2)>0.0)",
					"noplot_data_qcd_control",
					nick_suffix=nick_suffix
			)
			Samples._add_input(
					config,
					"DY*JetsToLLM*_RunIIFall15*_*_13TeV_*AOD_*/*.root",
					channel+"_tagEleEsNom_probeTauEsNom_probeEleEsNom/ntuple",
					lumi,
					"eventWeight*" + Samples.ztt_genmatch(channel) + self.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "os"], cut_type=cut_type) + "*((q_1*q_2)>0.0)",
					"noplot_ztt_mc_qcd_control",
					nick_suffix=nick_suffix
			)
			Samples._add_input(
					config,
					"DY*JetsToLLM10to50_RunIIFall15*_*_13TeV_*AOD_*/*.root DY*JetsToLLM50_RunIIFall15*_*_13TeV_*AOD_*/*.root",
					channel+"_tagEleEsNom_probeTauEsNom_probeEleEsNom/ntuple",
					lumi,
					"eventWeight*" + Samples.zll_genmatch(channel) + self.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "os"], cut_type=cut_type) + "*((q_1*q_2)>0.0)",
					"noplot_zll_qcd_control",
					nick_suffix=nick_suffix
			)
			Samples._add_input(
					config,
					"TT_RunIIFall15*_*_13TeV_*AOD_powheg-pythia8/*.root",
					channel+"_tagEleEsNom_probeTauEsNom_probeEleEsNom/ntuple",
					lumi,
					"eventWeight*" + self.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "os"], cut_type=cut_type) + "*((q_1*q_2)>0.0)",
					"noplot_ttj_qcd_control",
					nick_suffix=nick_suffix
			)
			Samples._add_input(
					config,
					"ST*_RunIIFall15*_*_13TeV_*AOD_powheg-pythia8/*root WW*_RunIIFall15*_*_13TeV_*AOD_*/*.root WZ*_RunIIFall15*_*_13TeV_*AOD_*/*.root ZZ*_RunIIFall15*_*_13TeV_*AOD_*/*.root VV*_RunIIFall15*_*_13TeV_*AOD_*/*.root",
					channel+"_tagEleEsNom_probeTauEsNom_probeEleEsNom/ntuple",
					lumi,
					"eventWeight*" + self.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "os"], cut_type=cut_type) + "*((q_1*q_2)>0.0)",
					"noplot_vv_qcd_control",
					nick_suffix=nick_suffix
			)
			
			if not "EstimateQcd" in config.get("analysis_modules", []):
				config.setdefault("analysis_modules", []).append("EstimateQcd")
			config.setdefault("qcd_data_shape_nicks", []).append("qcd"+nick_suffix)
			config.setdefault("qcd_data_yield_nicks", []).append("noplot_data_qcd_yield"+nick_suffix)
			config.setdefault("qcd_data_control_nicks", []).append("noplot_data_qcd_control"+nick_suffix)
			config.setdefault("qcd_data_substract_nicks", []).append(" ".join([nick+nick_suffix for nick in "noplot_ztt_mc_qcd_control noplot_zll_qcd_control noplot_ttj_qcd_control noplot_vv_qcd_control noplot_wj_ss".split()]))
			if channel == "et":
				config.setdefault("qcd_extrapolation_factors_ss_os", []).append(1.0 + (0.0 if not "os" in exclude_cuts else 1.0))
			elif channel == "mt":
				config.setdefault("qcd_extrapolation_factors_ss_os", []).append(1.17 + (0.0 if not "os" in exclude_cuts else 1.0))
			else:
				config.setdefault("qcd_extrapolation_factors_ss_os", []).append(1.06 + (0.0 if not "os" in exclude_cuts else 1.0))
			config.setdefault("qcd_subtract_shape", []).append(True)
		else:
			log.error("Sample config (QCD) currently not implemented for channel \"%s\"!" % channel)
		
		if not kwargs.get("no_plot", False):
			Samples._add_bin_corrections(config, "qcd", nick_suffix)
			Samples._add_plot(config, "bkg", "HIST", "F", "qcd", nick_suffix)
		return config
