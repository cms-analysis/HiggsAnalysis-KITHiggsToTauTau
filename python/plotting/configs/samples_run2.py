
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import copy

import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.samples as samples
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.cutstrings as cutstrings


default_lumi = 2155

class Samples(samples.SamplesBase):

	@staticmethod
	def cut_string(channel, exclude_cuts=None, cut_type="baseline"):
		if exclude_cuts is None:
			exclude_cuts = []
		
		cuts = cutstrings.CutStringsDict()._get_cutdict(channel, cut_type)
		cuts_list = [cut for (name, cut) in cuts.iteritems() if not name in exclude_cuts]
		if len(cuts_list) == 0:
			cuts_list.append("1.0")
		
		return "*".join(cuts_list)
	
	@staticmethod
	def ztt_genmatch(channel):
		if channel in ["mt", "et"]:
			return "(gen_match_2 == 5)*stitchWeightZTT*"
		elif channel == "em":
			return "(gen_match_1 > 2 && gen_match_2 > 3)*stitchWeightZTT*"
		elif channel == "mm":
			return "(gen_match_1 > 3 && gen_match_2 > 3)*stitchWeightZTT*"
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
		elif channel == "em":
			return "(gen_match_1 < 3 || gen_match_2 < 4)*stitchWeightZLL*"
		elif channel == "mm":
			return "(gen_match_1 < 4 || gen_match_2 < 4)*stitchWeightZLL"
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
					channel+"_jecUncNom_tauEsNom/ntuple",
					1.0,
					weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type),
					"data",
					nick_suffix=nick_suffix
			)
		elif channel == "et":
			Samples._add_input(
					config,
					"SingleElectron_Run2015?_*_13TeV_*AOD/*.root",
					channel+"_jecUncNom_tauEsNom/ntuple",
					1.0,
					weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type),
					"data",
					nick_suffix=nick_suffix
			)
		elif channel == "em":
			Samples._add_input(
					config,
					"MuonEG_Run2015?_*_13TeV_*AOD/*.root",
					channel+"_jecUncNom/ntuple",
					1.0,
					weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type),
					"data",
					nick_suffix=nick_suffix
			)
		elif channel == "mm":
			Samples._add_input(
					config,
					"SingleMuon_Run2015?_*_13TeV_*AOD/*.root",
					channel+"_jecUncNom/ntuple",
					1.0,
					weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type),
					"data",
					nick_suffix=nick_suffix
			)
		elif channel == "tt":
			Samples._add_input(
					config,
					"Tau_Run2015?_*_13TeV_*AOD/*.root",
					channel+"_jecUncNom_tauEsNom/ntuple",
					1.0,
					weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type),
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
		
		if channel in ["mt", "et", "tt", "em", "mm"]:
			Samples._add_input(
					config,
					"DY*JetsToLLM*_RunIIFall15*_*_13TeV_*AOD_*/*.root",
					channel+"_jecUncNom"+("_tauEsNom" if channel in ["mt", "et", "tt"] else "")+"/ntuple",
					lumi,
					weight+"*eventWeight*" + Samples.ztt_genmatch(channel) + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind"], cut_type=cut_type),
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
					channel+"_jecUncNom_tauEsNom/ntuple",
					lumi,
					weight+"*eventWeight*" + Samples.zl_genmatch(channel) + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind"], cut_type=cut_type),
					"zl",
					nick_suffix=nick_suffix
			)
		elif channel in ["em"]:
			pass
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
					channel+"_jecUncNom_tauEsNom/ntuple",
					lumi,
					weight+"*eventWeight*" + Samples.zj_genmatch(channel) + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind"], cut_type=cut_type),
					"zj",
					nick_suffix=nick_suffix
			)
		elif channel in ["em"]:
			pass
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
		
		if channel in ["mt", "et", "tt", "em", "mm"]:
			Samples._add_input(
					config,
					"DY*JetsToLLM10to50_RunIIFall15*_*_13TeV_*AOD_*/*.root DY*JetsToLLM50_RunIIFall15*_*_13TeV_*AOD_*/*.root",
					channel+"_jecUncNom"+("_tauEsNom" if channel in ["mt", "et", "tt"] else "")+"/ntuple",
					lumi,
					weight+"*eventWeight*" + Samples.zll_genmatch(channel) + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind"], cut_type=cut_type),
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
					channel+"_jecUncNom_tauEsNom/ntuple",
					lumi,
					weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind"], cut_type=cut_type),
					"ttj",
					nick_suffix=nick_suffix
			)
		elif channel == "mm":
			Samples._add_input(
					config,
					"TT_RunIIFall15*_*_13TeV_*AOD_powheg-pythia8/*.root",
					channel+"_jecUncNom/ntuple",
					lumi,
					weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind"], cut_type=cut_type),
					"ttj",
					nick_suffix=nick_suffix
			)
		elif channel == "em":
			Samples._add_input(
					config,
					"TT_RunIIFall15*_*_13TeV_*AOD_powheg-pythia8/*.root",
					channel+"_jecUncNom/ntuple",
					lumi,
					weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind"], cut_type=cut_type),
					"ttj",
					nick_suffix=nick_suffix
			)
			Samples._add_input(
					config,
					"MuonEG_Run2015?_*_13TeV_*AOD/*.root",
					channel+"_jecUncNom/ntuple",
					1.0,
					"eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "pzeta", "nobtag"], cut_type=cut_type) + "*(pZetaMissVis < -20.0)",
					"noplot_ttj_data_control",
					nick_suffix=nick_suffix
			)
			Samples._add_input(
					config,
					"DY*JetsToLLM*_RunIIFall15*_*_13TeV_*AOD_*/*.root",
					channel+"_jecUncNom/ntuple",
					lumi,
					"eventWeight*" + Samples.ztt_genmatch(channel) + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "pzeta", "nobtag"], cut_type=cut_type) + "*(pZetaMissVis < -20.0)",
					"noplot_ztt_mc_ttj_control",
					nick_suffix=nick_suffix
			)
			Samples._add_input(
					config,
					"DY*JetsToLLM10to50_RunIIFall15*_*_13TeV_*AOD_*/*.root DY*JetsToLLM50_RunIIFall15*_*_13TeV_*AOD_*/*.root",
					channel+"_jecUncNom/ntuple",
					lumi,
					"eventWeight*" + Samples.zll_genmatch(channel) + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "pzeta", "nobtag"], cut_type=cut_type) + "*(pZetaMissVis < -20.0)",
					"noplot_zll_ttj_control",
					nick_suffix=nick_suffix
			)
			Samples._add_input(
					config,
					"W*JetsToLNu_RunIIFall15*_*_13TeV_*AOD_*/*.root",
					channel+"_jecUncNom/ntuple",
					lumi,
					"eventWeight*stitchWeightWJ*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "pzeta", "nobtag"], cut_type=cut_type) + "*(pZetaMissVis < -20.0)",
					"noplot_wj_ttj_control",
					nick_suffix=nick_suffix
			)
			Samples._add_input(
					config,
					"ST*_RunIIFall15*_*_13TeV_*AOD_powheg-pythia8/*root WW*_RunIIFall15*_*_13TeV_*AOD_*/*.root WZ*_RunIIFall15*_*_13TeV_*AOD_*/*.root ZZ*_RunIIFall15*_*_13TeV_*AOD_*/*.root VV*_RunIIFall15*_*_13TeV_*AOD_*/*.root",
					channel+"_jecUncNom/ntuple",
					lumi,
					"eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "pzeta", "nobtag"], cut_type=cut_type) + "*(pZetaMissVis < -20.0)",
					"noplot_vv_ttj_control",
					nick_suffix=nick_suffix
			)
			Samples._add_input(
					config,
					"TT_RunIIFall15*_*_13TeV_*AOD_powheg-pythia8/*.root",
					channel+"_jecUncNom/ntuple",
					lumi,
					weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind"], cut_type=cut_type),
					"noplot_ttj_mc_signal",
					nick_suffix=nick_suffix
			)
			Samples._add_input(
					config,
					"TT_RunIIFall15*_*_13TeV_*AOD_powheg-pythia8/*.root",
					channel+"_jecUncNom/ntuple",
					lumi,
					"eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "pzeta", "nobtag"], cut_type=cut_type) + "*(pZetaMissVis < -20.0)",
					"noplot_ttj_mc_control",
					nick_suffix=nick_suffix
			)

			if not "EstimateTtbar" in config.get("analysis_modules", []):
				config.setdefault("analysis_modules", []).append("EstimateTtbar")
			config.setdefault("ttbar_from_mc", []).append(False)
			config.setdefault("ttbar_shape_nicks", []).append("ttj"+nick_suffix)
			config.setdefault("ttbar_data_control_nicks", []).append("noplot_ttj_data_control"+nick_suffix)
			config.setdefault("ttbar_data_substract_nicks", []).append(" ".join([nick+nick_suffix for nick in "noplot_ztt_mc_ttj_control noplot_zll_ttj_control noplot_wj_ttj_control noplot_vv_ttj_control".split()]))
			config.setdefault("ttbar_mc_signal_nicks", []).append("noplot_ttj_mc_signal"+nick_suffix)
			config.setdefault("ttbar_mc_control_nicks", []).append("noplot_ttj_mc_control"+nick_suffix)
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
		
		if channel in ["mt", "et", "em", "tt", "mm"]:
			Samples._add_input(
					config,
					"ST*_RunIIFall15*_*_13TeV_*AOD_powheg-pythia8/*root WW*_RunIIFall15*_*_13TeV_*AOD_*/*.root WZ*_RunIIFall15*_*_13TeV_*AOD_*/*.root ZZ*_RunIIFall15*_*_13TeV_*AOD_*/*.root VV*_RunIIFall15*_*_13TeV_*AOD_*/*.root",
					channel+"_jecUncNom"+("_tauEsNom" if channel in ["mt", "et", "tt"] else "")+"/ntuple",
					lumi,
					weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind"], cut_type=cut_type),
					"vv",
					nick_suffix=nick_suffix
			)
		else:
			log.error("Sample config (VV) currently not implemented for channel \"%s\"!" % channel)
		
		Samples._add_bin_corrections(config, "vv", nick_suffix)
		Samples._add_plot(config, "bkg", "HIST", "F", "vv", nick_suffix)
		return config
	
	def wj(self, config, channel, category, weight, nick_suffix, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", estimationMethod="classic", controlregions=False,**kwargs):
		if exclude_cuts is None:
			exclude_cuts = []
		
		scale_factor = lumi
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("WJets", 1.0)
		
		if channel in ["mt", "et"]:
			if estimationMethod == "new":
				Samples._add_input(
						config,
						"DY*JetsToLLM*_RunIIFall15*_*_13TeV_*AOD_*/*.root",
						channel+"_jecUncNom_tauEsNom/ntuple",
						lumi,
						weight+"*eventWeight*" + Samples.ztt_genmatch(channel) + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "mt"], cut_type=cut_type) + "*(mt_1>70.0)",
						("noplot_" if not controlregions else "") + "ztt_os_highmt",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						"DY*JetsToLLM10to50_RunIIFall15*_*_13TeV_*AOD_*/*.root DY*JetsToLLM50_RunIIFall15*_*_13TeV_*AOD_*/*.root",
						channel+"_jecUncNom_tauEsNom/ntuple",
						lumi,
						weight+"*eventWeight*" + Samples.zll_genmatch(channel) + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "mt"], cut_type=cut_type) + "*(mt_1>70.0)",
						("noplot_" if not controlregions else "") + "zll_os_highmt",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						"DY*JetsToLLM*_RunIIFall15*_*_13TeV_*AOD_*/*.root",
						channel+"_jecUncNom_tauEsNom/ntuple",
						lumi,
						weight+"*eventWeight*" + Samples.zl_genmatch(channel) + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "mt"], cut_type=cut_type) + "*(mt_1>70.0)",
						("noplot_" if not controlregions else "") + "zl_os_highmt",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						"DY*JetsToLLM*_RunIIFall15*_*_13TeV_*AOD_*/*.root",
						channel+"_jecUncNom_tauEsNom/ntuple",
						lumi,
						weight+"*eventWeight*" + Samples.zj_genmatch(channel) + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "mt"], cut_type=cut_type) + "*(mt_1>70.0)",
						("noplot_" if not controlregions else "") + "zj_os_highmt",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						"TT_RunIIFall15*_*_13TeV_*AOD_powheg-pythia8/*.root",
						channel+"_jecUncNom_tauEsNom/ntuple",
						lumi,
						weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "mt"], cut_type=cut_type) + "*(mt_1>70.0)",
						("noplot_" if not controlregions else "") + "ttj_os_highmt",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						"ST*_RunIIFall15*_*_13TeV_*AOD_powheg-pythia8/*root WW*_RunIIFall15*_*_13TeV_*AOD_*/*.root WZ*_RunIIFall15*_*_13TeV_*AOD_*/*.root ZZ*_RunIIFall15*_*_13TeV_*AOD_*/*.root VV*_RunIIFall15*_*_13TeV_*AOD_*/*.root",
						channel+"_jecUncNom_tauEsNom/ntuple",
						lumi,
						weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "mt"], cut_type=cut_type) + "*(mt_1>70.0)",
						("noplot_" if not controlregions else "") + "vv_os_highmt",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						"SingleMuon_Run2015?_*_13TeV_*AOD/*.root" if channel == "mt" else "SingleElectron_Run2015?_*_13TeV_*AOD/*root",
						channel+"_jecUncNom_tauEsNom/ntuple",
						1.0,
						weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "mt"], cut_type=cut_type) + "*(mt_1>70.0)",
						("noplot_" if not controlregions else "") + "data_os_highmt",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						"W*JetsToLNu_RunIIFall15*_*_13TeV_*AOD_*/*.root",
						channel+"_jecUncNom_tauEsNom/ntuple",
						lumi,
						weight+"*stitchWeightWJ*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "mt"], cut_type=cut_type) + "*(mt_1>70.0)",
						("noplot_" if not controlregions else "") + "wj_os_highmt",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						"DY*JetsToLLM*_RunIIFall15*_*_13TeV_*AOD_*/*.root",
						channel+"_jecUncNom_tauEsNom/ntuple",
						lumi,
						weight+"*eventWeight*" + Samples.ztt_genmatch(channel) + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "mt", "os"], cut_type=cut_type) + "*(mt_1>70.0)*((q_1*q_2)>0.0)",
						("noplot_" if not controlregions else "") + "ztt_ss_highmt",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						"DY*JetsToLLM10to50_RunIIFall15*_*_13TeV_*AOD_*/*.root DY*JetsToLLM50_RunIIFall15*_*_13TeV_*AOD_*/*.root",
						channel+"_jecUncNom_tauEsNom/ntuple",
						lumi,
						weight+"*eventWeight*" + Samples.zll_genmatch(channel) + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "mt", "os"], cut_type=cut_type) + "*(mt_1>70.0)*((q_1*q_2)>0.0)",
						("noplot_" if not controlregions else "") + "zll_ss_highmt",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						"DY*JetsToLLM10to50_RunIIFall15*_*_13TeV_*AOD_*/*.root DY*JetsToLLM50_RunIIFall15*_*_13TeV_*AOD_*/*.root",
						channel+"_jecUncNom_tauEsNom/ntuple",
						lumi,
						weight+"*eventWeight*" + Samples.zl_genmatch(channel) + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "mt", "os"], cut_type=cut_type) + "*(mt_1>70.0)*((q_1*q_2)>0.0)",
						("noplot_" if not controlregions else "") + "zl_ss_highmt",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						"DY*JetsToLLM10to50_RunIIFall15*_*_13TeV_*AOD_*/*.root DY*JetsToLLM50_RunIIFall15*_*_13TeV_*AOD_*/*.root",
						channel+"_jecUncNom_tauEsNom/ntuple",
						lumi,
						weight+"*eventWeight*" + Samples.zj_genmatch(channel) + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "mt", "os"], cut_type=cut_type) + "*(mt_1>70.0)*((q_1*q_2)>0.0)",
						("noplot_" if not controlregions else "") + "zj_ss_highmt",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						"TT_RunIIFall15*_*_13TeV_*AOD_powheg-pythia8/*.root",
						channel+"_jecUncNom_tauEsNom/ntuple",
						lumi,
						weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "mt", "os"], cut_type=cut_type) + "*(mt_1>70.0)*((q_1*q_2)>0.0)",
						("noplot_" if not controlregions else "") + "ttj_ss_highmt",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						"ST*_RunIIFall15*_*_13TeV_*AOD_powheg-pythia8/*root WW*_RunIIFall15*_*_13TeV_*AOD_*/*.root WZ*_RunIIFall15*_*_13TeV_*AOD_*/*.root ZZ*_RunIIFall15*_*_13TeV_*AOD_*/*.root VV*_RunIIFall15*_*_13TeV_*AOD_*/*.root",
						channel+"_jecUncNom_tauEsNom/ntuple",
						lumi,
						weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "mt", "os"], cut_type=cut_type) + "*(mt_1>70.0)*((q_1*q_2)>0.0)",
						("noplot_" if not controlregions else "") + "vv_ss_highmt",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						"SingleMuon_Run2015?_*_13TeV_*AOD/*.root" if channel == "mt" else "SingleElectron_Run2015?_*_13TeV_*AOD/*root",
						channel+"_jecUncNom_tauEsNom/ntuple",
						1.0,
						weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "mt", "os"], cut_type=cut_type) + "*(mt_1>70.0)*((q_1*q_2)>0.0)",
						("noplot_" if not controlregions else "") + "data_ss_highmt",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						"W*JetsToLNu_RunIIFall15*_*_13TeV_*AOD_*/*.root",
						channel+"_jecUncNom_tauEsNom/ntuple",
						lumi,
						weight+"*stitchWeightWJ*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "mt", "os"], cut_type=cut_type) + "*((q_1*q_2)>0.0)*(mt_1>70.0)",
						("noplot_" if not controlregions else "") + "wj_ss_highmt",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						"W*JetsToLNu_RunIIFall15*_*_13TeV_*AOD_*/*.root",
						channel+"_jecUncNom_tauEsNom/ntuple",
						lumi,
						weight+"*stitchWeightWJ*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind"], cut_type=cut_type),
						"wj",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						"W*JetsToLNu_RunIIFall15*_*_13TeV_*AOD_*/*.root",
						channel+"_jecUncNom_tauEsNom/ntuple",
						lumi,
						weight+"*stitchWeightWJ*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "mt"], cut_type=cut_type),
						"noplot_wj_mc_os_inclusive",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						"W*JetsToLNu_RunIIFall15*_*_13TeV_*AOD_*/*.root",
						channel+"_jecUncNom_tauEsNom/ntuple",
						lumi,
						weight+"*stitchWeightWJ*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "mt", "os"], cut_type=cut_type) + "*((q_1*q_2)>0.0)",
						"noplot_wj_mc_ss_inclusive",
						nick_suffix=nick_suffix
				)
				if not "EstimateWjetsAndQCD" in config.get("analysis_modules", []):
					config.setdefault("analysis_modules", []).append("EstimateWjetsAndQCD")
				if controlregions:
					config.setdefault("wjets_ss_substract_nicks", []).append(" ".join([nick+nick_suffix for nick in "ztt_ss_highmt zll_ss_highmt ttj_ss_highmt vv_ss_highmt".split()]))
					config.setdefault("wjets_ss_data_nicks", []).append("data_ss_highmt"+nick_suffix)
					config.setdefault("wjets_os_substract_nicks", []).append(" ".join([nick+nick_suffix for nick in "ztt_os_highmt zll_os_highmt ttj_os_highmt vv_os_highmt".split()]))
					config.setdefault("wjets_os_data_nicks", []).append("data_os_highmt"+nick_suffix)
					config.setdefault("wjets_shape_nicks", []).append("wj"+nick_suffix)
					config.setdefault("wjets_ss_mc_nicks", []).append("noplot_wj_mc_ss_inclusive"+nick_suffix)
					config.setdefault("wjets_ss_highmt_mc_nicks", []).append("wj_ss_highmt"+nick_suffix)
					config.setdefault("wjets_os_mc_nicks", []).append("noplot_wj_mc_os_inclusive"+nick_suffix)
					config.setdefault("wjets_os_highmt_mc_nicks", []).append("wj_os_highmt"+nick_suffix)
					config.setdefault("wjets_os_lowmt_mc_nicks", []).append("wj"+nick_suffix)
					for nick in ["ztt_os_highmt", "zll_os_highmt", "zl_os_highmt", "zj_os_highmt", "ttj_os_highmt", "vv_os_highmt", "data_os_highmt", "wj_os_highmt", "ztt_ss_highmt", "zll_ss_highmt", "zl_ss_highmt", "zj_ss_highmt", "ttj_ss_highmt", "vv_ss_highmt", "data_ss_highmt", "wj_ss_highmt"]:
						Samples._add_bin_corrections(config, nick, nick_suffix)
						Samples._add_plot(config, "bkg", "HIST", "F", nick, nick_suffix)
				else:
					config.setdefault("wjets_ss_substract_nicks", []).append(" ".join(["noplot_"+nick+nick_suffix for nick in "ztt_ss_highmt zll_ss_highmt ttj_ss_highmt vv_ss_highmt".split()]))
					config.setdefault("wjets_ss_data_nicks", []).append("noplot_data_ss_highmt"+nick_suffix)
					config.setdefault("wjets_os_substract_nicks", []).append(" ".join(["noplot_"+nick+nick_suffix for nick in "ztt_os_highmt zll_os_highmt ttj_os_highmt vv_os_highmt".split()]))
					config.setdefault("wjets_os_data_nicks", []).append("noplot_data_os_highmt"+nick_suffix)
					config.setdefault("wjets_shape_nicks", []).append("wj"+nick_suffix)
					config.setdefault("wjets_ss_mc_nicks", []).append("noplot_wj_mc_ss_inclusive"+nick_suffix)
					config.setdefault("wjets_ss_highmt_mc_nicks", []).append("noplot_wj_ss_highmt"+nick_suffix)
					config.setdefault("wjets_os_mc_nicks", []).append("noplot_wj_mc_os_inclusive"+nick_suffix)
					config.setdefault("wjets_os_highmt_mc_nicks", []).append("noplot_wj_os_highmt"+nick_suffix)
					config.setdefault("wjets_os_lowmt_mc_nicks", []).append("wj"+nick_suffix)

			if estimationMethod == "classic":
				shape_weight = weight+"*eventWeight*stitchWeightWJ*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind"], cut_type=cut_type)
				#if (not category is None) and (category != ""):
					## relaxed isolation
					#shape_weight = weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "iso_2"], cut_type=cut_type) + "*(byCombinedIsolationDeltaBetaCorrRaw3Hits_2<10.0)"
				
				Samples._add_input(
						config,
						"W*JetsToLNu_RunIIFall15*_*_13TeV_*AOD_*/*.root",
						channel+"_jecUncNom_tauEsNom/ntuple",
						lumi,
						shape_weight,
						"wj",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						"SingleMuon_Run2015?_*_13TeV_*AOD/*.root" if channel == "mt" else "SingleElectron_Run2015?_*_13TeV_*AOD/*root",
						channel+"_jecUncNom_tauEsNom/ntuple",
						1.0,
						"eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "mt"], cut_type=cut_type) + "*(mt_1>70.0)",
						"noplot_wj_data_control",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						"DY*JetsToLLM*_RunIIFall15*_*_13TeV_*AOD_*/*.root",
						channel+"_jecUncNom_tauEsNom/ntuple",
						lumi,
						"eventWeight*" + Samples.ztt_genmatch(channel) + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "mt"], cut_type=cut_type) + "*(mt_1>70.0)",
						"noplot_ztt_mc_wj_control",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						"DY*JetsToLLM10to50_RunIIFall15*_*_13TeV_*AOD_*/*.root DY*JetsToLLM50_RunIIFall15*_*_13TeV_*AOD_*/*.root",
						channel+"_jecUncNom_tauEsNom/ntuple",
						lumi,
						"eventWeight*" + Samples.zll_genmatch(channel) + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "mt"], cut_type=cut_type) + "*(mt_1>70.0)",
						"noplot_zll_wj_control",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						"TT_RunIIFall15*_*_13TeV_*AOD_powheg-pythia8/*.root",
						channel+"_jecUncNom_tauEsNom/ntuple",
						lumi,
						"eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "mt"], cut_type=cut_type) + "*(mt_1>70.0)",
						"noplot_ttj_wj_control",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						"ST*_RunIIFall15*_*_13TeV_*AOD_powheg-pythia8/*root WW*_RunIIFall15*_*_13TeV_*AOD_*/*.root WZ*_RunIIFall15*_*_13TeV_*AOD_*/*.root ZZ*_RunIIFall15*_*_13TeV_*AOD_*/*.root VV*_RunIIFall15*_*_13TeV_*AOD_*/*.root",
						channel+"_jecUncNom_tauEsNom/ntuple",
						lumi,
						"eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "mt"], cut_type=cut_type) + "*(mt_1>70.0)",
						"noplot_vv_wj_control",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						"W*JetsToLNu_RunIIFall15*_*_13TeV_*AOD_*/*.root",
						channel+"_jecUncNom_tauEsNom/ntuple",
						lumi,
						weight+"*eventWeight*stitchWeightWJ*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind"], cut_type=cut_type),
						"noplot_wj_mc_signal",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						"W*JetsToLNu_RunIIFall15*_*_13TeV_*AOD_*/*.root",
						channel+"_jecUncNom_tauEsNom/ntuple",
						lumi,
						"eventWeight*stitchWeightWJ*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "mt"], cut_type=cut_type) + "*(mt_1>70.0)",
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

		elif channel in ["em", "tt", "mm"]:
			Samples._add_input(
					config,
					"W*JetsToLNu_RunIIFall15*_*_13TeV_*AOD_*/*.root",
					channel+"_jecUncNom"+("_tauEsNom" if channel == "tt" else "")+"/ntuple",
					lumi,
					weight+"*eventWeight*stitchWeightWJ*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind"], cut_type=cut_type),
					"wj",
					nick_suffix=nick_suffix
			)
		else:	
			log.error("Sample config (WJets) currently not implemented for channel \"%s\"!" % channel)
		
		if not kwargs.get("no_plot", False):
			Samples._add_bin_corrections(config, "wj", nick_suffix)
			Samples._add_plot(config, "bkg", "HIST", "F", "wj", nick_suffix)
		return config

	def qcd(self, config, channel, category, weight, nick_suffix, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", estimationMethod="classic", controlregions=False,**kwargs):
		if exclude_cuts is None:
			exclude_cuts = []
		
		scale_factor = 1.0
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("QCD", 1.0)
		
		if channel in ["et", "mt", "em", "tt", "mm"]:
			if estimationMethod == "classic":
				# WJets for QCD estimate
				Samples._add_input(
						config,
						"W*JetsToLNu_RunIIFall15*_*_13TeV_*AOD_*/*.root",
						channel+"_jecUncNom"+("_tauEsNom" if channel in ["mt", "et", "tt"] else "")+"/ntuple",
						lumi,
						"eventWeight*stitchWeightWJ*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "os"], cut_type=cut_type) + "*((q_1*q_2)>0.0)",
						"noplot_wj_ss",
						nick_suffix=nick_suffix
				)
				
				if channel in ["mt", "et"]:
					Samples._add_input(
							config,
							"SingleMuon_Run2015?_*_13TeV_*AOD/*.root" if channel == "mt" else ("SingleElectron_Run2015?_*_13TeV_*AOD/*root" if channel == "et" else "MuonEG_Run2015?_*_13TeV_*AOD/*.root"),
							channel+"_jecUncNom_tauEsNom/ntuple",
							1.0,
							"eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "os", "mt"], cut_type=cut_type) + "*((q_1*q_2)>0.0)*(mt_1>70.0)",
							"noplot_wj_ss_data_control",
							nick_suffix=nick_suffix
					)
					Samples._add_input(
							config,
							"DY*JetsToLLM*_RunIIFall15*_*_13TeV_*AOD_*/*.root",
							channel+"_jecUncNom_tauEsNom/ntuple",
							lumi,
							"eventWeight*" + Samples.ztt_genmatch(channel) + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "os", "mt"], cut_type=cut_type) + "*((q_1*q_2)>0.0)*(mt_1>70.0)",
							"noplot_ztt_ss_mc_wj_control",
							nick_suffix=nick_suffix
					)
					Samples._add_input(
							config,
							"DY*JetsToLLM10to50_RunIIFall15*_*_13TeV_*AOD_*/*.root DY*JetsToLLM50_RunIIFall15*_*_13TeV_*AOD_*/*.root",
							channel+"_jecUncNom_tauEsNom/ntuple",
							lumi,
							"eventWeight*" + Samples.zll_genmatch(channel) + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "os", "mt"], cut_type=cut_type) + "*((q_1*q_2)>0.0)*(mt_1>70.0)",
							"noplot_zll_ss_wj_control",
							nick_suffix=nick_suffix
					)
					Samples._add_input(
							config,
							"TT_RunIIFall15*_*_13TeV_*AOD_powheg-pythia8/*.root",
							channel+"_jecUncNom_tauEsNom/ntuple",
							lumi,
							"eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "os", "mt"], cut_type=cut_type) + "*((q_1*q_2)>0.0)*(mt_1>70.0)",
							"noplot_ttj_ss_wj_control",
							nick_suffix=nick_suffix
					)
					Samples._add_input(
							config,
							"ST*_RunIIFall15*_*_13TeV_*AOD_powheg-pythia8/*root WW*_RunIIFall15*_*_13TeV_*AOD_*/*.root WZ*_RunIIFall15*_*_13TeV_*AOD_*/*.root ZZ*_RunIIFall15*_*_13TeV_*AOD_*/*.root VV*_RunIIFall15*_*_13TeV_*AOD_*/*.root",
							channel+"_jecUncNom_tauEsNom/ntuple",
							lumi,
							"eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "os", "mt"], cut_type=cut_type) + "*((q_1*q_2)>0.0)*(mt_1>70.0)",
							"noplot_vv_ss_wj_control",
							nick_suffix=nick_suffix
					)
					Samples._add_input(
							config,
							"W*JetsToLNu_RunIIFall15*_*_13TeV_*AOD_*/*.root",
							channel+"_jecUncNom_tauEsNom/ntuple",
							lumi,
							"stitchWeightWJ*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "os"], cut_type=cut_type) + "*((q_1*q_2)>0.0)",
							"noplot_wj_ss_mc_signal",
							nick_suffix=nick_suffix
					)
					Samples._add_input(
							config,
							"W*JetsToLNu_RunIIFall15*_*_13TeV_*AOD_*/*.root",
							channel+"_jecUncNom_tauEsNom/ntuple",
							lumi,
							"stitchWeightWJ*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "os", "mt"], cut_type=cut_type) + "*((q_1*q_2)>0.0)*(mt_1>70.0)",
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
				shape_weight = weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "os"], cut_type=cut_type) + "*((q_1*q_2)>0.0)"
				#if (not category is None) and (category != ""):
					## relaxed/inverted isolation
					#if channel in ["et", "mt"]:
						#shape_weight = weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "os", "iso_2"], cut_type=cut_type) + "*((q_1*q_2)>0.0)"+"*(byCombinedIsolationDeltaBetaCorrRaw3Hits_2<10.0)"
					#else:
						#shape_weight = weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "os", "iso_1", "iso_2"], cut_type=cut_type) + "*((q_1*q_2)>0.0)"
				
				Samples._add_input(
						config,
						"SingleMuon_Run2015?_*_13TeV_*AOD/*.root" if channel == "mt" else ("SingleElectron_Run2015?_*_13TeV_*AOD/*root" if channel == "et" else "MuonEG_Run2015?_*_13TeV_*AOD/*.root" if channel == "em" else "Tau_Run2015?_*_13TeV_*AOD/*.root"),
						channel+"_jecUncNom"+("_tauEsNom" if channel in ["mt", "et", "tt"] else "")+"/ntuple",
						1.0,
						shape_weight,
						"qcd",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						"SingleMuon_Run2015?_*_13TeV_*AOD/*.root" if channel == "mt" else ("SingleElectron_Run2015?_*_13TeV_*AOD/*root" if channel == "et" else "MuonEG_Run2015?_*_13TeV_*AOD/*.root" if channel == "em" else "Tau_Run2015?_*_13TeV_*AOD/*.root"),
						channel+"_jecUncNom"+("_tauEsNom" if channel in ["mt", "et", "tt"] else "")+"/ntuple",
						1.0,
						weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "os"], cut_type=cut_type) + "*((q_1*q_2)>0.0)",
						"noplot_data_qcd_yield",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						"SingleMuon_Run2015?_*_13TeV_*AOD/*.root" if channel == "mt" else ("SingleElectron_Run2015?_*_13TeV_*AOD/*root" if channel == "et" else "MuonEG_Run2015?_*_13TeV_*AOD/*.root" if channel == "em" else "Tau_Run2015?_*_13TeV_*AOD/*.root"),
						channel+"_jecUncNom"+("_tauEsNom" if channel in ["mt", "et", "tt"] else "")+"/ntuple",
						1.0,
						"eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "os"], cut_type=cut_type) + "*((q_1*q_2)>0.0)",
						"noplot_data_qcd_control",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						"DY*JetsToLLM*_RunIIFall15*_*_13TeV_*AOD_*/*.root",
						channel+"_jecUncNom"+("_tauEsNom" if channel in ["mt", "et", "tt"] else "")+"/ntuple",
						lumi,
						"eventWeight*" + Samples.ztt_genmatch(channel) + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "os"], cut_type=cut_type) + "*((q_1*q_2)>0.0)",
						"noplot_ztt_mc_qcd_control",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						"DY*JetsToLLM10to50_RunIIFall15*_*_13TeV_*AOD_*/*.root DY*JetsToLLM50_RunIIFall15*_*_13TeV_*AOD_*/*.root",
						channel+"_jecUncNom"+("_tauEsNom" if channel in ["mt", "et", "tt"] else "")+"/ntuple",
						lumi,
						"eventWeight*" + Samples.zll_genmatch(channel) + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "os"], cut_type=cut_type) + "*((q_1*q_2)>0.0)",
						"noplot_zll_qcd_control",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						"TT_RunIIFall15*_*_13TeV_*AOD_powheg-pythia8/*.root",
						channel+"_jecUncNom"+("_tauEsNom" if channel in ["mt", "et", "tt"] else "")+"/ntuple",
						lumi,
						"eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "os"], cut_type=cut_type) + "*((q_1*q_2)>0.0)",
						"noplot_ttj_qcd_control",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						"ST*_RunIIFall15*_*_13TeV_*AOD_powheg-pythia8/*root WW*_RunIIFall15*_*_13TeV_*AOD_*/*.root WZ*_RunIIFall15*_*_13TeV_*AOD_*/*.root ZZ*_RunIIFall15*_*_13TeV_*AOD_*/*.root VV*_RunIIFall15*_*_13TeV_*AOD_*/*.root",
						channel+"_jecUncNom"+("_tauEsNom" if channel in ["mt", "et", "tt"] else "")+"/ntuple",
						lumi,
						"eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "os"], cut_type=cut_type) + "*((q_1*q_2)>0.0)",
						"noplot_vv_qcd_control",
						nick_suffix=nick_suffix
				)
				
				if not "EstimateQcd" in config.get("analysis_modules", []):
					config.setdefault("analysis_modules", []).append("EstimateQcd")
				config.setdefault("qcd_data_shape_nicks", []).append("qcd"+nick_suffix)
				config.setdefault("qcd_data_yield_nicks", []).append("noplot_data_qcd_yield"+nick_suffix)
				config.setdefault("qcd_data_control_nicks", []).append("noplot_data_qcd_control"+nick_suffix)
				config.setdefault("qcd_data_substract_nicks", []).append(" ".join([nick+nick_suffix for nick in "noplot_ztt_mc_qcd_control noplot_zll_qcd_control noplot_ttj_qcd_control noplot_vv_qcd_control noplot_wj_ss".split()]))
				if channel == "em":
					config.setdefault("qcd_extrapolation_factors_ss_os", []).append(2.0 + (0.0 if not "os" in exclude_cuts else 1.0))
				elif channel == "et":
					config.setdefault("qcd_extrapolation_factors_ss_os", []).append(1.0 + (0.0 if not "os" in exclude_cuts else 1.0))
				elif channel == "mt":
					config.setdefault("qcd_extrapolation_factors_ss_os", []).append(1.17 + (0.0 if not "os" in exclude_cuts else 1.0))
				else:
					config.setdefault("qcd_extrapolation_factors_ss_os", []).append(1.06 + (0.0 if not "os" in exclude_cuts else 1.0))
				config.setdefault("qcd_subtract_shape", []).append(True)
			
			if estimationMethod == "new":
				Samples._add_input(
						config,
						"DY*JetsToLLM*_RunIIFall15*_*_13TeV_*AOD_*/*.root",
						channel+"_jecUncNom_tauEsNom/ntuple",
						lumi,
						weight+"*eventWeight*" + Samples.ztt_genmatch(channel) + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "os"], cut_type=cut_type) + "*((q_1*q_2)>0.0)",
						("noplot_" if not controlregions else "") + "ztt_ss_lowmt",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						"DY*JetsToLLM10to50_RunIIFall15*_*_13TeV_*AOD_*/*.root DY*JetsToLLM50_RunIIFall15*_*_13TeV_*AOD_*/*.root",
						channel+"_jecUncNom_tauEsNom/ntuple",
						lumi,
						weight+"*eventWeight*" + Samples.zll_genmatch(channel) + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "os"], cut_type=cut_type) + "*((q_1*q_2)>0.0)",
						("noplot_" if not controlregions else "") + "zll_ss_lowmt",
						nick_suffix=nick_suffix
				)
				if channel in ["et","mt"]:
					Samples._add_input(
							config,
							"DY*JetsToLLM10to50_RunIIFall15*_*_13TeV_*AOD_*/*.root DY*JetsToLLM50_RunIIFall15*_*_13TeV_*AOD_*/*.root",
							channel+"_jecUncNom_tauEsNom/ntuple",
							lumi,
							weight+"*eventWeight*" + Samples.zl_genmatch(channel) + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "os"], cut_type=cut_type) + "*((q_1*q_2)>0.0)",
							("noplot_" if not controlregions else "") + "zl_ss_lowmt",
							nick_suffix=nick_suffix
					)
					Samples._add_input(
							config,
							"DY*JetsToLLM10to50_RunIIFall15*_*_13TeV_*AOD_*/*.root DY*JetsToLLM50_RunIIFall15*_*_13TeV_*AOD_*/*.root",
							channel+"_jecUncNom_tauEsNom/ntuple",
							lumi,
							weight+"*eventWeight*" + Samples.zj_genmatch(channel) + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "os"], cut_type=cut_type) + "*((q_1*q_2)>0.0)",
							("noplot_" if not controlregions else "") + "zj_ss_lowmt",
							nick_suffix=nick_suffix
					)
				Samples._add_input(
						config,
						"TT_RunIIFall15*_*_13TeV_*AOD_powheg-pythia8/*.root",
						channel+"_jecUncNom_tauEsNom/ntuple",
						lumi,
						weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "os"], cut_type=cut_type) + "*((q_1*q_2)>0.0)",
						("noplot_" if not controlregions else "") + "ttj_ss_lowmt",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						"ST*_RunIIFall15*_*_13TeV_*AOD_powheg-pythia8/*root WW*_RunIIFall15*_*_13TeV_*AOD_*/*.root WZ*_RunIIFall15*_*_13TeV_*AOD_*/*.root ZZ*_RunIIFall15*_*_13TeV_*AOD_*/*.root VV*_RunIIFall15*_*_13TeV_*AOD_*/*.root",
						channel+"_jecUncNom_tauEsNom/ntuple",
						lumi,
						weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "os"], cut_type=cut_type) + "*((q_1*q_2)>0.0)",
						("noplot_" if not controlregions else "") + "vv_ss_lowmt",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						"W*JetsToLNu_RunIIFall15*_*_13TeV_*AOD_*/*.root",
						channel+"_jecUncNom_tauEsNom/ntuple",
						lumi,
						weight+"*stitchWeightWJ*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "os"], cut_type=cut_type) + "*((q_1*q_2)>0.0)",
						("noplot_" if not controlregions else "") + "wj_ss_lowmt",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						"SingleMuon_Run2015?_*_13TeV_*AOD/*.root" if channel == "mt" else ("SingleElectron_Run2015?_*_13TeV_*AOD/*root" if channel == "et" else "MuonEG_Run2015?_*_13TeV_*AOD/*.root"),
						channel+"_jecUncNom_tauEsNom/ntuple",
						1.0,
						weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "os"], cut_type=cut_type) + "*((q_1*q_2)>0.0)",
						("noplot_" if not controlregions else "") + "data_ss_lowmt",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						"DY*JetsToLLM*_RunIIFall15*_*_13TeV_*AOD_*/*.root",
						channel+"_jecUncNom_tauEsNom/ntuple",
						lumi,
						(weight+"*eventWeight*" + Samples.ztt_genmatch(channel) + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "os"], cut_type=cut_type) + "*((q_1*q_2)>0.0)").replace("nbtag","nloosebtag" if "_btag" in category else "nbtag"),
						"noplot_ztt_shape_ss_qcd_control",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						"DY*JetsToLLM10to50_RunIIFall15*_*_13TeV_*AOD_*/*.root DY*JetsToLLM50_RunIIFall15*_*_13TeV_*AOD_*/*.root",
						channel+"_jecUncNom_tauEsNom/ntuple",
						lumi,
						(weight+"*eventWeight*" + Samples.zll_genmatch(channel) + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "os"], cut_type=cut_type) + "*((q_1*q_2)>0.0)").replace("nbtag","nloosebtag" if "_btag" in category else "nbtag"),
						"noplot_zll_shape_ss_qcd_control",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						"TT_RunIIFall15*_*_13TeV_*AOD_powheg-pythia8/*.root",
						channel+"_jecUncNom_tauEsNom/ntuple",
						lumi,
						(weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "os"], cut_type=cut_type) + "*((q_1*q_2)>0.0)").replace("nbtag","nloosebtag" if "_btag" in category else "nbtag"),
						"noplot_ttj_shape_ss_qcd_control",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						"ST*_RunIIFall15*_*_13TeV_*AOD_powheg-pythia8/*root WW*_RunIIFall15*_*_13TeV_*AOD_*/*.root WZ*_RunIIFall15*_*_13TeV_*AOD_*/*.root ZZ*_RunIIFall15*_*_13TeV_*AOD_*/*.root VV*_RunIIFall15*_*_13TeV_*AOD_*/*.root",
						channel+"_jecUncNom_tauEsNom/ntuple",
						lumi,
						(weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "os"], cut_type=cut_type) + "*((q_1*q_2)>0.0)").replace("nbtag","nloosebtag" if "_btag" in category else "nbtag"),
						"noplot_vv_shape_ss_qcd_control",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						"W*JetsToLNu_RunIIFall15*_*_13TeV_*AOD_*/*.root",
						channel+"_jecUncNom_tauEsNom/ntuple",
						lumi,
						(weight+"*stitchWeightWJ*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "os"], cut_type=cut_type) + "*((q_1*q_2)>0.0)").replace("nbtag","nloosebtag" if "_btag" in category else "nbtag"),
						"noplot_wj_shape_ss_qcd_control",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						"SingleMuon_Run2015?_*_13TeV_*AOD/*.root" if channel == "mt" else ("SingleElectron_Run2015?_*_13TeV_*AOD/*root" if channel == "et" else "MuonEG_Run2015?_*_13TeV_*AOD/*.root"),
						channel+"_jecUncNom_tauEsNom/ntuple",
						1.0,
						weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "os", "mt"], cut_type=cut_type) + "*((q_1*q_2)>0.0)*(mt_1>70.0)",
						("noplot_" if not controlregions else "") + "qcd_ss_highmt",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						"DY*JetsToLLM*_RunIIFall15*_*_13TeV_*AOD_*/*.root",
						channel+"_jecUncNom_tauEsNom/ntuple",
						lumi,
						(weight+"*eventWeight*" + Samples.ztt_genmatch(channel) + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "os", "mt"], cut_type=cut_type) + "*((q_1*q_2)>0.0)*(mt_1>70.0)").replace("nbtag","nloosebtag" if "_btag" in category else "nbtag"),
						"noplot_ztt_shape_ss_highmt",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						"DY*JetsToLLM10to50_RunIIFall15*_*_13TeV_*AOD_*/*.root DY*JetsToLLM50_RunIIFall15*_*_13TeV_*AOD_*/*.root",
						channel+"_jecUncNom_tauEsNom/ntuple",
						lumi,
						(weight+"*eventWeight*" + Samples.zll_genmatch(channel) + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "os", "mt"], cut_type=cut_type) + "*((q_1*q_2)>0.0)*(mt_1>70.0)").replace("nbtag","nloosebtag" if "_btag" in category else "nbtag"),
						"noplot_zll_shape_ss_highmt",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						"TT_RunIIFall15*_*_13TeV_*AOD_powheg-pythia8/*.root",
						channel+"_jecUncNom_tauEsNom/ntuple",
						lumi,
						(weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "os", "mt"], cut_type=cut_type) + "*((q_1*q_2)>0.0)*(mt_1>70.0)").replace("nbtag","nloosebtag" if "_btag" in category else "nbtag"),
						"noplot_ttj_shape_ss_highmt",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						"ST*_RunIIFall15*_*_13TeV_*AOD_powheg-pythia8/*root WW*_RunIIFall15*_*_13TeV_*AOD_*/*.root WZ*_RunIIFall15*_*_13TeV_*AOD_*/*.root ZZ*_RunIIFall15*_*_13TeV_*AOD_*/*.root VV*_RunIIFall15*_*_13TeV_*AOD_*/*.root",
						channel+"_jecUncNom_tauEsNom/ntuple",
						lumi,
						(weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "os", "mt"], cut_type=cut_type) + "*((q_1*q_2)>0.0)*(mt_1>70.0)").replace("nbtag","nloosebtag" if "_btag" in category else "nbtag"),
						"noplot_vv_shape_ss_highmt",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						"SingleMuon_Run2015?_*_13TeV_*AOD/*.root" if channel == "mt" else ("SingleElectron_Run2015?_*_13TeV_*AOD/*root" if channel == "et" else "MuonEG_Run2015?_*_13TeV_*AOD/*.root"),
						channel+"_jecUncNom_tauEsNom/ntuple",
						1.0,
						weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "os", "mt"], cut_type=cut_type) + "*(mt_1>70.0)*((q_1*q_2)>0.0)",
						("noplot_" if not controlregions else "") + "qcd_os_highmt",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						"SingleMuon_Run2015?_*_13TeV_*AOD/*.root" if channel == "mt" else ("SingleElectron_Run2015?_*_13TeV_*AOD/*root" if channel == "et" else "MuonEG_Run2015?_*_13TeV_*AOD/*.root"),
						channel+"_jecUncNom_tauEsNom/ntuple",
						1.0,
						weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "os"], cut_type=cut_type) + "*((q_1*q_2)>0.0)",
						("noplot_" if not controlregions else "") + "qcd_ss_lowmt",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						"SingleMuon_Run2015?_*_13TeV_*AOD/*.root" if channel == "mt" else ("SingleElectron_Run2015?_*_13TeV_*AOD/*root" if channel == "et" else "MuonEG_Run2015?_*_13TeV_*AOD/*.root"),
						channel+"_jecUncNom_tauEsNom/ntuple",
						1.0,
						(weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "os"], cut_type=cut_type) + "*((q_1*q_2)>0.0)").replace("nbtag","nloosebtag" if "_btag" in category else "nbtag"),
						"qcd",
						nick_suffix=nick_suffix
				)
				if controlregions:
					if not "EstimateWjetsAndQCD" in config.get("analysis_modules", []):
						config.setdefault("analysis_modules", []).append("EstimateWjetsAndQCD")
					elif channel == "et":
						config.setdefault("qcd_extrapolation_factors_ss_os", []).append(1.0)
					elif channel == "mt":
						config.setdefault("qcd_extrapolation_factors_ss_os", []).append(1.17)
					config.setdefault("qcd_shape_nicks", []).append("qcd"+nick_suffix)
					config.setdefault("qcd_yield_nicks", []).append("data_ss_lowmt"+nick_suffix)
					config.setdefault("qcd_yield_substract_nicks", []).append(" ".join([nick+nick_suffix for nick in "ztt_ss_lowmt zll_ss_lowmt ttj_ss_lowmt vv_ss_lowmt wj_ss_lowmt".split()]))
					config.setdefault("qcd_shape_substract_nicks", []).append(" ".join([nick+nick_suffix for nick in "noplot_ztt_shape_ss_qcd_control noplot_zll_shape_ss_qcd_control noplot_ttj_shape_ss_qcd_control noplot_vv_shape_ss_qcd_control noplot_wj_shape_ss_qcd_control".split()]))
					config.setdefault("qcd_ss_highmt_shape_nicks", []).append("qcd_ss_highmt"+nick_suffix)
					config.setdefault("qcd_ss_lowmt_nicks", []).append("qcd_ss_lowmt"+nick_suffix)
					config.setdefault("qcd_os_highmt_nicks", []).append("qcd_os_highmt"+nick_suffix)
					config.setdefault("qcd_shape_highmt_substract_nicks", []).append(" ".join([nick+nick_suffix for nick in "noplot_ztt_shape_ss_highmt noplot_zll_shape_ss_highmt noplot_ttj_shape_ss_highmt noplot_vv_shape_ss_highmt".split()]))

					if channel in ["et","mt"]:
						for nick in ["ztt_ss_lowmt", "zll_ss_lowmt", "zl_ss_lowmt", "zj_ss_lowmt", "ttj_ss_lowmt", "vv_ss_lowmt", "wj_ss_lowmt","data_ss_lowmt", "qcd_ss_highmt", "qcd_os_highmt", "qcd_ss_lowmt"]:
							Samples._add_bin_corrections(config, nick, nick_suffix)
							Samples._add_plot(config, "bkg", "HIST", "F", nick, nick_suffix)
					else:
						for nick in ["ztt_ss_lowmt", "zll_ss_lowmt", "ttj_ss_lowmt", "vv_ss_lowmt", "wj_ss_lowmt","data_ss_lowmt", "qcd_ss_highmt", "qcd_os_highmt", "qcd_ss_lowmt"]:
							Samples._add_bin_corrections(config, nick, nick_suffix)
							Samples._add_plot(config, "bkg", "HIST", "F", nick, nick_suffix)

				else:
					if not "EstimateWjetsAndQCD" in config.get("analysis_modules", []):
						config.setdefault("analysis_modules", []).append("EstimateWjetsAndQCD")
					elif channel == "et":
						config.setdefault("qcd_extrapolation_factors_ss_os", []).append(1.0)
					elif channel == "mt":
						config.setdefault("qcd_extrapolation_factors_ss_os", []).append(1.17)
					config.setdefault("qcd_shape_nicks", []).append("qcd"+nick_suffix)
					config.setdefault("qcd_yield_nicks", []).append("noplot_data_ss_lowmt"+nick_suffix)
					config.setdefault("qcd_yield_substract_nicks", []).append(" ".join(["noplot_"+nick+nick_suffix for nick in "ztt_ss_lowmt zll_ss_lowmt ttj_ss_lowmt vv_ss_lowmt wj_ss_lowmt".split()]))
					config.setdefault("qcd_shape_substract_nicks", []).append(" ".join([nick+nick_suffix for nick in "noplot_ztt_shape_ss_qcd_control noplot_zll_shape_ss_qcd_control noplot_ttj_shape_ss_qcd_control noplot_vv_shape_ss_qcd_control noplot_wj_shape_ss_qcd_control".split()]))
					config.setdefault("qcd_ss_highmt_shape_nicks", []).append("noplot_qcd_ss_highmt"+nick_suffix)
					config.setdefault("qcd_ss_lowmt_nicks", []).append("noplot_qcd_ss_lowmt"+nick_suffix)
					config.setdefault("qcd_os_highmt_nicks", []).append("noplot_qcd_os_highmt"+nick_suffix)
					config.setdefault("qcd_shape_highmt_substract_nicks", []).append(" ".join([nick+nick_suffix for nick in "noplot_ztt_shape_ss_highmt noplot_zll_shape_ss_highmt noplot_ttj_shape_ss_highmt noplot_vv_shape_ss_highmt".split()]))
		else:
			log.error("Sample config (QCD) currently not implemented for channel \"%s\"!" % channel)
		
		if not kwargs.get("no_plot", False):
			Samples._add_bin_corrections(config, "qcd", nick_suffix)
			Samples._add_plot(config, "bkg", "HIST", "F", "qcd", nick_suffix)
		return config
	
	def htt(self, config, channel, category, weight, nick_suffix, higgs_masses, normalise_signal_to_one_pb=False, lumi=default_lumi, exclude_cuts=None, **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []
		
		config = self.ggh(config, channel, category, weight, nick_suffix+"_noplot", higgs_masses,
		                  normalise_signal_to_one_pb, lumi=lumi, exclude_cuts=exclude_cuts, no_plot=True, **kwargs)
		config = self.qqh(config, channel, category, weight, nick_suffix+"_noplot", higgs_masses,
		                  normalise_signal_to_one_pb, lumi=lumi, exclude_cuts=exclude_cuts, no_plot=True, **kwargs)
		config = self.vh(config, channel, category, weight, nick_suffix+"_noplot", higgs_masses,
		                 normalise_signal_to_one_pb, lumi=lumi, exclude_cuts=exclude_cuts, no_plot=True, **kwargs)
		
		for mass in higgs_masses:
			if not "AddHistograms" in config.get("analysis_modules", []):
				config.setdefault("analysis_modules", []).append("AddHistograms")
			config.setdefault("histogram_nicks", []).append(" ".join([sample+str(mass)+("_"+str(int(kwargs["scale_signal"])) if kwargs.get("scale_signal", 1.0) != 1.0 else "")+nick_suffix+"_noplot" for sample in ["ggh", "qqh", "vh"]]))
			config.setdefault("sum_result_nicks", []).append("htt"+str(mass)+nick_suffix)
			
			Samples._add_bin_corrections(
					config,
					"htt"+str(mass)+("_"+str(int(kwargs["scale_signal"])) if kwargs.get("scale_signal", 1.0) != 1.0 else ""),
					nick_suffix
			)
			Samples._add_plot(
					config,
					"bkg" if kwargs.get("stack_signal", False) else "htt",
					"LINE",
					"L",
					"htt"+str(mass)+("_"+str(int(kwargs["scale_signal"])) if kwargs.get("scale_signal", 1.0) != 1.0 else ""),
					nick_suffix
			)
		return config
	
	def bbh(self, config, channel, category, weight, nick_suffix, higgs_masses, normalise_signal_to_one_pb=False, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []
		
		scale_factor = lumi
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("bbh", 1.0)
		
		for mass in higgs_masses:
			if channel in ["tt", "et", "mt", "em"]:
				Samples._add_input(
						config,
						"SUSYGluGluToBBHToTauTauM{mass}_RunIIFall15*_*_13TeV_*AOD_pythia8/*.root".format(mass=str(mass)),
						channel+"_jecUncNom"+("_tauEsNom" if channel in ["mt", "et", "tt"] else "")+"/ntuple",
						lumi*kwargs.get("scale_signal", 1.0),
						weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind"], cut_type=cut_type),
						"bbH"+str(mass)+("_"+str(int(kwargs["scale_signal"])) if kwargs.get("scale_signal", 1.0) != 1.0 else ""),
						nick_suffix=nick_suffix
				)
			else:
				log.error("Sample config (bbH%s) currently not implemented for channel \"%s\"!" % (str(mass), channel))
			
			if not kwargs.get("no_plot", False):
				Samples._add_bin_corrections(
						config,
						"bbh"+str(mass)+("_"+str(int(kwargs["scale_signal"])) if kwargs.get("scale_signal", 1.0) != 1.0 else ""),
						nick_suffix
				)
				Samples._add_plot(
						config,
						"bbh",
						"LINE",
						"L",
						"bbh"+str(mass)+("_"+str(int(kwargs["scale_signal"])) if kwargs.get("scale_signal", 1.0) != 1.0 else ""),
						nick_suffix
				)
		return config

	def ggh(self, config, channel, category, weight, nick_suffix, higgs_masses, normalise_signal_to_one_pb=False, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", mssm=False, **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []
		
		scale_factor = lumi
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("ggh", 1.0)
		
		for mass in higgs_masses:
			if channel in ["tt", "et", "mt", "em", "mm"]:
				Samples._add_input(
						config,
						"GluGluHToTauTauM{mass}_RunIIFall15*_*_13TeV_*AOD_powheg*pythia8/*.root".format(mass=str(mass)) if not mssm else "SUSYGluGluToHToTauTauM{mass}_RunIIFall15*_*_13TeV_*AOD_pythia8/*.root".format(mass=str(mass)),
						channel+"_jecUncNom"+("_tauEsNom" if channel in ["mt", "et", "tt"] else "")+"/ntuple",
						lumi*kwargs.get("scale_signal", 1.0),
						weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind"], cut_type=cut_type),
						"ggh"+str(mass)+("_"+str(int(kwargs["scale_signal"])) if kwargs.get("scale_signal", 1.0) != 1.0 else ""),
						nick_suffix=nick_suffix
				)
			else:
				log.error("Sample config (ggH%s) currently not implemented for channel \"%s\"!" % (str(mass), channel))
			
			if not kwargs.get("no_plot", False):
				Samples._add_bin_corrections(
						config,
						"ggh"+str(mass)+("_"+str(int(kwargs["scale_signal"])) if kwargs.get("scale_signal", 1.0) != 1.0 else ""),
						nick_suffix
				)
				Samples._add_plot(
						config,
						"ggh",
						"LINE",
						"L",
						"ggh"+str(mass)+("_"+str(int(kwargs["scale_signal"])) if kwargs.get("scale_signal", 1.0) != 1.0 else ""),
						nick_suffix
				)
		return config
	
	def qqh(self, config, channel, category, weight, nick_suffix, higgs_masses, normalise_signal_to_one_pb=False, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []
		
		scale_factor = lumi
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("qqH", 1.0)
		
		for mass in higgs_masses:
			if channel in ["tt", "et", "mt", "em", "mm"]:
				Samples._add_input(
						config,
						"VBFHToTauTauM{mass}_RunIIFall15*_*_13TeV_*AOD_powheg*pythia8/*.root".format(mass=str(mass)),
						channel+"_jecUncNom"+("_tauEsNom" if channel in ["mt", "et", "tt"] else "")+"/ntuple",
						lumi*kwargs.get("scale_signal", 1.0),
						weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind"], cut_type=cut_type),
						"qqh"+str(mass)+("_"+str(int(kwargs["scale_signal"])) if kwargs.get("scale_signal", 1.0) != 1.0 else ""),
						nick_suffix=nick_suffix
			)
			else:
				log.error("Sample config (VBF%s) currently not implemented for channel \"%s\"!" % (str(mass), channel))
			
			if not kwargs.get("no_plot", False):
				Samples._add_bin_corrections(
						config,
						"qqh"+str(mass)+("_"+str(int(kwargs["scale_signal"])) if kwargs.get("scale_signal", 1.0) != 1.0 else ""),
						nick_suffix
				)
				Samples._add_plot(
						config,
						"qqh",
						"LINE",
						"L",
						"qqh"+str(mass)+("_"+str(int(kwargs["scale_signal"])) if kwargs.get("scale_signal", 1.0) != 1.0 else ""),
						nick_suffix
				)
		return config
	
	def vh(self, config, channel, category, weight, nick_suffix, higgs_masses, normalise_signal_to_one_pb=False, lumi=default_lumi, exclude_cuts=None, **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []
		
		no_plot_kwargs = copy.deepcopy(kwargs)
		no_plot_kwargs["no_plot"] = True
		config = self.wh(config, channel, category, weight, nick_suffix+"_noplot", higgs_masses,
		                 normalise_signal_to_one_pb, lumi=lumi, exclude_cuts=exclude_cuts, **no_plot_kwargs)
		config = self.zh(config, channel, category, weight, nick_suffix+"_noplot", higgs_masses,
		                 normalise_signal_to_one_pb, lumi=lumi, exclude_cuts=exclude_cuts, **no_plot_kwargs)
		
		for mass in higgs_masses:
			if not "AddHistograms" in config.get("analysis_modules", []):
				config.setdefault("analysis_modules", []).append("AddHistograms")
			config.setdefault("histogram_nicks", []).append(" ".join([sample+str(mass)+("_"+str(int(kwargs["scale_signal"])) if kwargs.get("scale_signal", 1.0) != 1.0 else "")+nick_suffix+"_noplot" for sample in ["wh", "zh"]]))
			config.setdefault("sum_result_nicks", []).append("vh"+str(mass)+("_"+str(int(kwargs["scale_signal"])) if kwargs.get("scale_signal", 1.0) != 1.0 else "")+nick_suffix)
			
			if not kwargs.get("no_plot", False):
				Samples._add_bin_corrections(
						config,
						"vh"+str(mass)+("_"+str(int(kwargs["scale_signal"])) if kwargs.get("scale_signal", 1.0) != 1.0 else ""),
						nick_suffix
				)
				Samples._add_plot(
						config,
						"vh",
						"LINE",
						"L",
						"vh"+str(mass)+("_"+str(int(kwargs["scale_signal"])) if kwargs.get("scale_signal", 1.0) != 1.0 else ""),
						nick_suffix
				)
		return config
	
	def wh(self, config, channel, category, weight, nick_suffix, higgs_masses, normalise_signal_to_one_pb=False, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []
		
		scale_factor = lumi
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("WH", 1.0)
		
		for mass in higgs_masses:
			if channel in ["tt", "et", "mt", "em", "mm"]:
				Samples._add_input(
						config,
						"WminusHToTauTauM{mass}_RunIIFall15*_*_13TeV_*AOD_powheg*pythia8/*.root".format(mass=str(mass)),
						channel+"_jecUncNom"+("_tauEsNom" if channel in ["mt", "et", "tt"] else "")+"/ntuple",
						lumi*kwargs.get("scale_signal", 1.0),
						weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind"], cut_type=cut_type),
						"wmh"+str(mass)+("_"+str(int(kwargs["scale_signal"])) if kwargs.get("scale_signal", 1.0) != 1.0 else ""),
						nick_suffix=nick_suffix+"_noplot"
				)
				Samples._add_input(
						config,
						"WplusHToTauTauM{mass}_RunIIFall15*_*_13TeV_*AOD_powheg*pythia8/*.root".format(mass=str(mass)),
						channel+"_jecUncNom"+("_tauEsNom" if channel in ["mt", "et", "tt"] else "")+"/ntuple",
						lumi*kwargs.get("scale_signal", 1.0),
						weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind"], cut_type=cut_type),
						"wph"+str(mass)+("_"+str(int(kwargs["scale_signal"])) if kwargs.get("scale_signal", 1.0) != 1.0 else ""),
						nick_suffix=nick_suffix+"_noplot"
				)
				
				if not "AddHistograms" in config.get("analysis_modules", []):
					config.setdefault("analysis_modules", []).append("AddHistograms")
				config.setdefault("histogram_nicks", []).append(" ".join([sample+str(mass)+("_"+str(int(kwargs["scale_signal"])) if kwargs.get("scale_signal", 1.0) != 1.0 else "")+nick_suffix+"_noplot" for sample in ["wmh", "wph"]]))
				config.setdefault("sum_result_nicks", []).append("wh"+str(mass)+("_"+str(int(kwargs["scale_signal"])) if kwargs.get("scale_signal", 1.0) != 1.0 else "")+nick_suffix)
			
			else:
				log.error("Sample config (WH%s) currently not implemented for channel \"%s\"!" % (str(mass), channel))
			
			if not kwargs.get("no_plot", False):
				Samples._add_bin_corrections(
						config,
						"wh"+str(mass)+("_"+str(int(kwargs["scale_signal"])) if kwargs.get("scale_signal", 1.0) != 1.0 else ""),
						nick_suffix
				)
				Samples._add_plot(
						config,
						"wh",
						"LINE",
						"L",
						"wh"+str(mass)+("_"+str(int(kwargs["scale_signal"])) if kwargs.get("scale_signal", 1.0) != 1.0 else ""),
						nick_suffix
				)
		return config
	
	def zh(self, config, channel, category, weight, nick_suffix, higgs_masses, normalise_signal_to_one_pb=False, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []
		
		scale_factor = lumi
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("ZH", 1.0)
		
		for mass in higgs_masses:
			if channel in ["tt", "et", "mt", "em", "mm"]:
				Samples._add_input(
						config,
						"ZHToTauTauM{mass}_RunIIFall15*_*_13TeV_*AOD_powheg*pythia8/*.root".format(mass=str(mass)),
						channel+"_jecUncNom"+("_tauEsNom" if channel in ["mt", "et", "tt"] else "")+"/ntuple",
						lumi*kwargs.get("scale_signal", 1.0),
						weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind"], cut_type=cut_type),
						"zh"+str(mass)+("_"+str(int(kwargs["scale_signal"])) if kwargs.get("scale_signal", 1.0) != 1.0 else ""),
						nick_suffix=nick_suffix
				)
			
			else:
				log.error("Sample config (ZH%s) currently not implemented for channel \"%s\"!" % (str(mass), channel))
			
			if not kwargs.get("no_plot", False):
				Samples._add_bin_corrections(
						config,
						"zh"+str(mass)+("_"+str(int(kwargs["scale_signal"])) if kwargs.get("scale_signal", 1.0) != 1.0 else ""),
						nick_suffix
				)
				Samples._add_plot(
						config,
						"zh",
						"LINE",
						"L",
						"zh"+str(mass)+("_"+str(int(kwargs["scale_signal"])) if kwargs.get("scale_signal", 1.0) != 1.0 else ""),
						nick_suffix
				)
		return config

