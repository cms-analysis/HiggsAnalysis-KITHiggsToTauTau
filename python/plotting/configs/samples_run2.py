
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import copy

import Artus.Utility.jsonTools as jsonTools


selectionCuts = "*((q_1*q_2)<0.0)*(againstElectronVLooseMVA5_2 > 0.5)*(againstMuonTight3_2 > 0.5)*(extraelec_veto < 0.5)"
#"*(iso_1 < 0.1)*(againstElectronLooseMVA5_2 > 0.5)*(againstMuonTight3_2 > 0.5)*(byCombinedIsolationDeltaBetaCorrRaw3Hits_2 < 1.5)*(extraelec_veto == 0)*(extramuon_veto == 0)*(mt_1 < 40)"

class Sample(object):

	def __init__(self):
		self.config = jsonTools.JsonDict({})
		self.postfit_scales = None
	
	def get_config(self, samples, channel, category, nick_suffix="", postfit_scales=None, **kwargs):
		self.postfit_scales = postfit_scales
		
		config = copy.deepcopy(self.config)
		
		for sample in samples:
			config = sample(self, config, channel, category, nick_suffix, **kwargs)
		
		if not category is None:
			config["weights"] = [weight+("*(isCat%s>0)" % category) for weight in config.setdefault("weights", [])]
		
		#config.setdefault("analysis_modules", []).append("@CorrectNegativeBinContents")
		config.setdefault("analysis_modules", []).append("PrintInfos")
		
		config["nicks_blacklist"] = ["noplot"]
		#config["file_mode"] = "UPDATE"
		
		return config.doIncludes().doComments()
		
	@staticmethod
	def merge_configs(config1, config2):
		merged_config = copy.deepcopy(config1)
		
		for key in [
				"nicks",
				"directories",
				"files",
				"folders",
				"x_expressions",
				"scale_factors",
				"weights",
				"x_bins",
				"y_bins",
				"z_bins",
				"histogram_to_scale_nicks",
				"integral_histogram_nicks",
				"scale_by_inverse_integrals",
				"histogram_nicks",
				"sum_result_nicks",
				"stacks",
				"markers",
				"colors",
				"labels",
		]:
			if key in merged_config or key in config2:
				merged_config.setdefault(key, []).extend(config2.get(key, []))
		
		for key in [
				"analysis_modules",
		]:
			for item in config2.get(key, []):
				if not item in merged_config.get(key, []):
					merged_config.setdefault(key, []).append(item)
		
		for key, value in config2.iteritems():
			if not key in merged_config:
				merged_config[key] = value
		
		return merged_config
	
	def data(self, config, channel, category, nick_suffix, **kwargs):
		scale_factor = 1.0
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("data_obs", 1.0)
		
		if channel == "mt":
			Sample._add_input(
					config,
					"SingleMuon_Run2015B_PromptRecov1_13TeV_MINIAOD/*.root",
					"mt_z/ntuple",
					1.0,
					"eventWeight" + selectionCuts,
					"data",
					nick_suffix=nick_suffix
			)
		else:
			log.error("Sample config (Data) currently not implemented for channel \"%s\"!" % channel)
		
		Sample._add_plot(config, "data", "E", "ELP", "data", nick_suffix)
		return config
	
	def ztt(self, config, channel, category, nick_suffix, lumi=5.59, **kwargs):
		scale_factor = 1.0
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("ZTT", 1.0)
		
		if channel in ["mt"]:
			Sample._add_input(
					config,
					"DYJetsToLLM50_RunIISpring15DR74_Asympt25ns_13TeV_MINIAODSIM/*.root",
					channel+"_ztt/ntuple",
					lumi,
					"crossSectionPerEventWeight*numberGeneratedEventsWeight" + selectionCuts,
					"ztt",
					nick_suffix=nick_suffix
			)
		else:
			log.error("Sample config (ZTT) currently not implemented for channel \"%s\"!" % channel)
		
		Sample._add_plot(config, "bkg", "HIST", "F", "ztt", nick_suffix)
		
		return config
	
	def zl(self, config, channel, category, nick_suffix, lumi=5.59, **kwargs):
		scale_factor = lumi
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("ZL", 1.0)
		
		if channel in ["mt"]:
			Sample._add_input(
					config,
					"DYJetsToLLM50_RunIISpring15DR74_Asympt25ns_13TeV_MINIAODSIM/*.root",
					channel+"_zl/ntuple",
					lumi,
					"crossSectionPerEventWeight*numberGeneratedEventsWeight" + selectionCuts,
					"zleplep",
					nick_suffix=nick_suffix
			)
		else:
			log.error("Sample config (ZL) currently not implemented for channel \"%s\"!" % channel)
		
		Sample._add_plot(config, "bkg", "HIST", "F", "zl", nick_suffix)
		return config


	def zj(self, config, channel, category, nick_suffix, lumi=5.59, **kwargs):
		scale_factor = lumi
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("ZJ", 1.0)
		
		if channel in ["mt"]:
			Sample._add_input(
					config,
					"DYJetsToLLM50_RunIISpring15DR74_Asympt25ns_13TeV_MINIAODSIM/*.root",
					channel+"_zj/ntuple",
					lumi,
					"crossSectionPerEventWeight*numberGeneratedEventsWeight" + selectionCuts,
					"zleplep"
			)
		else:
			log.error("Sample config (ZJ) currently not implemented for channel \"%s\"!" % channel)

		#Sample._add_plot(config, "bkg", "HIST", "F", "zj", nick_suffix)
		return config
	

	def ttj(self, config, channel, category, nick_suffix, lumi=5.59, **kwargs):
		scale_factor = lumi
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("TTJ", 1.0)
		
		if channel in ["mt"]:
			Sample._add_input(
					config,
					"TTJets_RunIISpring15DR74_Asympt25ns_13TeV_MINIAODSIM/*.root",
					channel+"_z/ntuple",
					lumi,
					"crossSectionPerEventWeight*numberGeneratedEventsWeight" + selectionCuts,
					"ttj",
					nick_suffix=nick_suffix
			)	
		else:
			log.error("Sample config (TTJ) currently not implemented for channel \"%s\"!" % channel)
		
		Sample._add_plot(config, "bkg", "HIST", "F", "ttj", nick_suffix)
		return config
	
	def wj(self, config, channel, category, nick_suffix, lumi=5.59, **kwargs):
		scale_factor = lumi
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("WJets", 1.0)
		
		if channel in ["mt"]:
			Sample._add_input(
					config,
					"WJetsToLNu_RunIISpring15DR74_Asympt25ns_13TeV_MINIAODSIM/*.root",
					channel+"_z/ntuple",
					lumi,
					"crossSectionPerEventWeight*numberGeneratedEventsWeight" + selectionCuts,
					"wj",
					nick_suffix=nick_suffix
			)
		else:	
			log.error("Sample config (WJets) currently not implemented for channel \"%s\"!" % channel)
		
		if not kwargs.get("no_plot", False):
			Sample._add_plot(config, "bkg", "HIST", "F", "wj", nick_suffix)
		return config

	@staticmethod
	def _add_input(config, input_file, folder, scale_factor, weight, nick, nick_suffix=""):
		config.setdefault("files", []).append(input_file)
		config.setdefault("folders", []).append(folder)
		config.setdefault("scale_factors", []).append(scale_factor)
		config.setdefault("weights", []).append(weight)
		config.setdefault("nicks", []).append(nick+nick_suffix)
		return config
		
	@staticmethod
	def _add_plot(config, stack, marker, legend_marker, color_label_key, nick_suffix=""):
		config.setdefault("stacks", []).append(stack+nick_suffix)
		config.setdefault("markers", []).append(marker)
		config.setdefault("legend_markers", []).append(legend_marker)
		config.setdefault("colors", []).append(color_label_key)
		config.setdefault("labels", []).append(color_label_key)
		return config

