
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import copy

import Artus.Utility.jsonTools as jsonTools

#TODO: pass this as a configuration parameter, if
# used more than for a few tests
cutStep = 5

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
					channel+"_z/ntuple",
					1.0,
					"1.0" + cut_string(channel, cutStep),
					"data",
					nick_suffix=nick_suffix
			)
		elif channel == "et":
			Sample._add_input(
					config,
					"SingleElectron_Run2015B_PromptRecov1_13TeV_MINIAOD/*.root",
					channel+"_z/ntuple",
					1.0,
					"1.0" + cut_string(channel, cutStep),
					"data",
					nick_suffix=nick_suffix
			)
		elif channel == "em":
			Sample._add_input(
					config,
					"MuonEG_Run2015B_PromptRecov1_13TeV_MINIAOD/*.root",
					channel+"/ntuple",
					1.0,
					"1.0" + cut_string(channel, cutStep),
					"data",
					nick_suffix=nick_suffix
			)
		else:
			log.error("Sample config (Data) currently not implemented for channel \"%s\"!" % channel)
		
		Sample._add_plot(config, "data", "E", "ELP", "data", nick_suffix)
		return config
	
	def ztt(self, config, channel, category, nick_suffix, lumi=40.03, **kwargs):
		scale_factor = 1.0
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("ZTT", 1.0)
		
		if channel in ["mt", "et"]:
			Sample._add_input(
					config,
					"DYJetsToLLM50_RunIISpring15DR74_Asympt25ns_13TeV_MINIAODSIM/*.root",
					channel+"_ztt/ntuple " + channel + "_zttlep/ntuple",
					lumi,
					"crossSectionPerEventWeight*numberGeneratedEventsWeight*generatorWeight" + cut_string(channel, cutStep),
					"ztt",
					nick_suffix=nick_suffix
			)
		elif channel == "em":
			Sample._add_input(
					config,
					"DYJetsToLLM50_RunIISpring15DR74_Asympt25ns_13TeV_MINIAODSIM/*.root",
					channel+"_tt/ntuple",
					lumi,
					"crossSectionPerEventWeight*numberGeneratedEventsWeight*generatorWeight" + cut_string(channel, cutStep),
					"ztt",
					nick_suffix=nick_suffix
			)
		else:
			log.error("Sample config (ZTT) currently not implemented for channel \"%s\"!" % channel)
		
		Sample._add_plot(config, "bkg", "HIST", "F", "ztt", nick_suffix)
		
		return config
	
	def zll(self, config, channel, category, nick_suffix, lumi=40.03, **kwargs):
		scale_factor = lumi
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("ZL", 1.0)
		
		if channel in ["mt", "et"]:
			Sample._add_input(
					config,
					"DYJetsToLLM50_RunIISpring15DR74_Asympt25ns_13TeV_MINIAODSIM/*.root",
					channel+"_zll/ntuple " + channel + "_zl/ntuple " + channel + "_zj/ntuple",
					lumi,
					"crossSectionPerEventWeight*numberGeneratedEventsWeight*generatorWeight" + cut_string(channel, cutStep),
					"zll",
					nick_suffix=nick_suffix
			)
		elif channel == "em":
			Sample._add_input(
					config,
					"DYJetsToLLM50_RunIISpring15DR74_Asympt25ns_13TeV_MINIAODSIM/*.root",
					channel+"_ee/ntuple " + channel + "_mm/ntuple",
					lumi,
					"crossSectionPerEventWeight*numberGeneratedEventsWeight*generatorWeight" + cut_string(channel, cutStep),
					"zll",
					nick_suffix=nick_suffix
			)
		else:
			log.error("Sample config (ZLL) currently not implemented for channel \"%s\"!" % channel)
		
		Sample._add_plot(config, "bkg", "HIST", "F", "zl", nick_suffix)
		return config
	

	def ttj(self, config, channel, category, nick_suffix, lumi=40.03, **kwargs):
		scale_factor = lumi
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("TTJ", 1.0)
		
		if channel in ["mt", "et"]:
			Sample._add_input(
					config,
					"TTJets_RunIISpring15DR74_Asympt25ns_13TeV_MINIAODSIM/*.root",
					channel+"_z/ntuple",
					lumi,
					"crossSectionPerEventWeight*numberGeneratedEventsWeight*generatorWeight" + cut_string(channel, cutStep),
					"ttj",
					nick_suffix=nick_suffix
			)

		elif channel == "em":
			Sample._add_input(
					config,
					"TTJets_RunIISpring15DR74_Asympt25ns_13TeV_MINIAODSIM/*.root",
					channel+"/ntuple",
					lumi,
					"crossSectionPerEventWeight*numberGeneratedEventsWeight*generatorWeight" + cut_string(channel, cutStep),
					"ttj",
					nick_suffix=nick_suffix
			)
		else:
			log.error("Sample config (TTJ) currently not implemented for channel \"%s\"!" % channel)
		
		Sample._add_plot(config, "bkg", "HIST", "F", "ttj", nick_suffix)
		return config
	
	def wj(self, config, channel, category, nick_suffix, lumi=40.03, **kwargs):
		scale_factor = lumi
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("WJets", 1.0)
		
		if channel in ["mt", "et"]:
			Sample._add_input(
					config,
					"WJetsToLNu_RunIISpring15DR74_Asympt25ns_13TeV_MINIAODSIM/*.root",
					channel+"_z/ntuple",
					lumi,
					"crossSectionPerEventWeight*numberGeneratedEventsWeight*generatorWeight" + cut_string(channel, cutStep),
					"wj",
					nick_suffix=nick_suffix
			)
			Sample._add_input(
					config,
					"SingleMuon_Run2015B_PromptRecov1_13TeV_MINIAOD/*.root" if channel == "mt" else "SingleElectron_Run2015B_PromptRecov1_13TeV_MINIAOD/*root",
					channel+"_z/ntuple",
					1.0,
					"crossSectionPerEventWeight*numberGeneratedEventsWeight*generatorWeight" + cut_string(channel, cutStep) + "*(mt_1>80.0)",
					"noplot_wj_data_control"
			)
			Sample._add_input(
					config,
					"DYJetsToLLM50_RunIISpring15DR74_Asympt25ns_13TeV_MINIAODSIM/*.root",
					channel+"_ztt/ntuple " + channel + "_zttlep/ntuple",
					lumi,
					"crossSectionPerEventWeight*numberGeneratedEventsWeight*generatorWeight" + cut_string(channel, cutStep) + "*(mt_1>80.0)",
					"noplot_ztt_mc_wj_control",
					nick_suffix=nick_suffix
			)
			Sample._add_input(
					config,
					"DYJetsToLLM50_RunIISpring15DR74_Asympt25ns_13TeV_MINIAODSIM/*.root",
					channel+"_zl/ntuple " + channel + "_zj/ntuple " + channel + "_zll/ntuple",
					lumi,
					"crossSectionPerEventWeight*numberGeneratedEventsWeight*generatorWeight" + cut_string(channel, cutStep) + "*(mt_1>80.0)",
					"noplot_zll_wj_control",
					nick_suffix=nick_suffix
			)
			Sample._add_input(
					config,
					"TTJets_RunIISpring15DR74_Asympt25ns_13TeV_MINIAODSIM/*.root",
					channel+"_z/ntuple",
					lumi,
					"crossSectionPerEventWeight*numberGeneratedEventsWeight*generatorWeight" + cut_string(channel, cutStep) + "*(mt_1>80.0)",
					"noplot_ttj_wj_control",
					nick_suffix=nick_suffix
			)
			Sample._add_input(
					config,
					"WJetsToLNu_RunIISpring15DR74_Asympt25ns_13TeV_MINIAODSIM/*.root",
					channel+"_z/ntuple",
					lumi,
					"crossSectionPerEventWeight*numberGeneratedEventsWeight*generatorWeight" + cut_string(channel, cutStep),
					"noplot_wj_mc_signal",
					nick_suffix=nick_suffix
			)
			Sample._add_input(
					config,
					"WJetsToLNu_RunIISpring15DR74_Asympt25ns_13TeV_MINIAODSIM/*.root",
					channel+"_z/ntuple",
					lumi,
					"crossSectionPerEventWeight*numberGeneratedEventsWeight*generatorWeight" + cut_string(channel, cutStep) + "*(mt_1>80.0)",
					"noplot_wj_mc_control",
					nick_suffix=nick_suffix
			)

			if not "EstimateWjets" in config.get("analysis_modules", []):
				config.setdefault("analysis_modules", []).append("EstimateWjets")
			config.setdefault("wjets_shape_nicks", []).append("wj"+nick_suffix)
			config.setdefault("wjets_data_control_nicks", []).append("noplot_wj_data_control"+nick_suffix)
			config.setdefault("wjets_data_substract_nicks", []).append(" ".join([nick+nick_suffix for nick in "noplot_ztt_mc_wj_control noplot_zll_wj_control noplot_ttj_wj_control".split()]))
			config.setdefault("wjets_mc_signal_nicks", []).append("noplot_wj_mc_signal"+nick_suffix)
			config.setdefault("wjets_mc_control_nicks", []).append("noplot_wj_mc_control"+nick_suffix)

		elif channel == "em":
			Sample._add_input(
					config,
					"WJetsToLNu_RunIISpring15DR74_Asympt25ns_13TeV_MINIAODSIM/*.root",
					channel+"/ntuple",
					lumi,
					"crossSectionPerEventWeight*numberGeneratedEventsWeight*generatorWeight" + cut_string(channel, cutStep),
					"wj",
					nick_suffix=nick_suffix
			)
		else:	
			log.error("Sample config (WJets) currently not implemented for channel \"%s\"!" % channel)
		
		if not kwargs.get("no_plot", False):
			Sample._add_plot(config, "bkg", "HIST", "F", "wj", nick_suffix)
		return config

	def qcd(self, config, channel, category, nick_suffix, lumi=40.03, **kwargs):
		scale_factor = 1.0
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("QCD", 1.0)
		
		if channel in ["et", "mt"]:

			# WJets for QCD estimate
			Sample._add_input(
					config,
					"WJetsToLNu_RunIISpring15DR74_Asympt25ns_13TeV_MINIAODSIM/*.root",
					channel+"_z/ntuple",
					lumi,
					"crossSectionPerEventWeight*numberGeneratedEventsWeight*generatorWeight*((q_1*q_2)>0.0)*(extraelec_veto < 0.5)*(extramuon_veto < 0.5)*(dilepton_veto < 0.5)*(iso_1 < 0.1)*(byCombinedIsolationDeltaBetaCorrRaw3Hits_2 < 1.5)" +
						("*(againstElectronVLooseMVA5_2 > 0.5)*(againstMuonTight3_2 > 0.5)" if channel == "mt" else
						 "*(againstElectronTightMVA5_2 > 0.5)*(againstMuonLoose3_2 > 0.5)"),
					"noplot_wj_ss",
					nick_suffix=nick_suffix
			)
			Sample._add_input(
					config,
					"SingleMuon_Run2015B_PromptRecov1_13TeV_MINIAOD/*.root" if channel == "mt" else "SingleElectron_Run2015B_PromptRecov1_13TeV_MINIAOD/*root",
					channel+"_z/ntuple",
					1.0,
					"crossSectionPerEventWeight*numberGeneratedEventsWeight*generatorWeight*((q_1*q_2)>0.0)*(extraelec_veto < 0.5)*(extramuon_veto < 0.5)*(dilepton_veto < 0.5)*(iso_1 < 0.1)*(byCombinedIsolationDeltaBetaCorrRaw3Hits_2 < 1.5)*(mt_1>80.0)" +
						("*(againstElectronVLooseMVA5_2 > 0.5)*(againstMuonTight3_2 > 0.5)" if channel == "mt" else
						 "*(againstElectronTightMVA5_2 > 0.5)*(againstMuonLoose3_2 > 0.5)"),
					"noplot_wj_ss_data_control",
					nick_suffix=nick_suffix
			)
			Sample._add_input(
					config,
					"DYJetsToLLM50_RunIISpring15DR74_Asympt25ns_13TeV_MINIAODSIM/*.root",
					channel+"_ztt/ntuple " + channel + "_zttlep/ntuple",
					lumi,
					"crossSectionPerEventWeight*numberGeneratedEventsWeight*generatorWeight*((q_1*q_2)>0.0)*(extraelec_veto < 0.5)*(extramuon_veto < 0.5)*(dilepton_veto < 0.5)*(iso_1 < 0.1)*(byCombinedIsolationDeltaBetaCorrRaw3Hits_2 < 1.5)*(mt_1>80.0)" +
						("*(againstElectronVLooseMVA5_2 > 0.5)*(againstMuonTight3_2 > 0.5)" if channel == "mt" else
						 "*(againstElectronTightMVA5_2 > 0.5)*(againstMuonLoose3_2 > 0.5)"),
					"noplot_ztt_ss_mc_wj_control",
					nick_suffix=nick_suffix
			)
			Sample._add_input(
					config,
					"DYJetsToLLM50_RunIISpring15DR74_Asympt25ns_13TeV_MINIAODSIM/*.root",
					channel+"_zl/ntuple " + channel + "_zj/ntuple " + channel + "_zll/ntuple",
					lumi,
					"crossSectionPerEventWeight*numberGeneratedEventsWeight*generatorWeight*((q_1*q_2)>0.0)*(extraelec_veto < 0.5)*(extramuon_veto < 0.5)*(dilepton_veto < 0.5)*(iso_1 < 0.1)*(byCombinedIsolationDeltaBetaCorrRaw3Hits_2 < 1.5)*(mt_1>80.0)" +
						("*(againstElectronVLooseMVA5_2 > 0.5)*(againstMuonTight3_2 > 0.5)" if channel == "mt" else
						 "*(againstElectronTightMVA5_2 > 0.5)*(againstMuonLoose3_2 > 0.5)"),
					"noplot_zll_ss_wj_control",
					nick_suffix=nick_suffix
			)
			Sample._add_input(
					config,
					"TTJets_RunIISpring15DR74_Asympt25ns_13TeV_MINIAODSIM/*.root",
					channel+"_z/ntuple",
					lumi,
					"crossSectionPerEventWeight*numberGeneratedEventsWeight*generatorWeight*((q_1*q_2)>0.0)*(extraelec_veto < 0.5)*(extramuon_veto < 0.5)*(dilepton_veto < 0.5)*(iso_1 < 0.1)*(byCombinedIsolationDeltaBetaCorrRaw3Hits_2 < 1.5)*(mt_1>80.0)" +
						("*(againstElectronVLooseMVA5_2 > 0.5)*(againstMuonTight3_2 > 0.5)" if channel == "mt" else
						 "*(againstElectronTightMVA5_2 > 0.5)*(againstMuonLoose3_2 > 0.5)"),
					"noplot_ttj_ss_wj_control",
					nick_suffix=nick_suffix
			)
			Sample._add_input(
					config,
					"WJetsToLNu_RunIISpring15DR74_Asympt25ns_13TeV_MINIAODSIM/*.root",
					channel+"_z/ntuple",
					lumi,
					"crossSectionPerEventWeight*numberGeneratedEventsWeight*generatorWeight*((q_1*q_2)>0.0)*(extraelec_veto < 0.5)*(extramuon_veto < 0.5)*(dilepton_veto < 0.5)*(iso_1 < 0.1)*(byCombinedIsolationDeltaBetaCorrRaw3Hits_2 < 1.5)" +
						("*(againstElectronVLooseMVA5_2 > 0.5)*(againstMuonTight3_2 > 0.5)" if channel == "mt" else
						 "*(againstElectronTightMVA5_2 > 0.5)*(againstMuonLoose3_2 > 0.5)"),
					"noplot_wj_ss_mc_signal",
					nick_suffix=nick_suffix
			)
			Sample._add_input(
					config,
					"WJetsToLNu_RunIISpring15DR74_Asympt25ns_13TeV_MINIAODSIM/*.root",
					channel+"_z/ntuple",
					lumi,
					"crossSectionPerEventWeight*numberGeneratedEventsWeight*generatorWeight*((q_1*q_2)>0.0)*(extraelec_veto < 0.5)*(extramuon_veto < 0.5)*(dilepton_veto < 0.5)*(iso_1 < 0.1)*(byCombinedIsolationDeltaBetaCorrRaw3Hits_2 < 1.5)*(mt_1>80.0)" +
						("*(againstElectronVLooseMVA5_2 > 0.5)*(againstMuonTight3_2 > 0.5)" if channel == "mt" else
						 "*(againstElectronTightMVA5_2 > 0.5)*(againstMuonLoose3_2 > 0.5)"),
					"noplot_wj_ss_mc_control",
					nick_suffix=nick_suffix
			)
			
			if not "EstimateWjets" in config.get("analysis_modules", []):
				config.setdefault("analysis_modules", []).append("EstimateWjets")
			config.setdefault("wjets_shape_nicks", []).append("noplot_wj_ss"+nick_suffix)
			config.setdefault("wjets_data_control_nicks", []).append("noplot_wj_ss_data_control"+nick_suffix)
			config.setdefault("wjets_data_substract_nicks", []).append(" ".join([nick+nick_suffix for nick in "noplot_ztt_ss_mc_wj_control noplot_zll_ss_wj_control noplot_ttj_ss_wj_control".split()]))
			config.setdefault("wjets_mc_signal_nicks", []).append("noplot_wj_ss_mc_signal"+nick_suffix)
			config.setdefault("wjets_mc_control_nicks", []).append("noplot_wj_ss_mc_control"+nick_suffix)

			# QCD
			Sample._add_input(
					config,
					"SingleMuon_Run2015B_PromptRecov1_13TeV_MINIAOD/*.root" if channel == "mt" else "SingleElectron_Run2015B_PromptRecov1_13TeV_MINIAOD/*root",
					channel+"_z/ntuple",
					1.0,
					"crossSectionPerEventWeight*numberGeneratedEventsWeight*generatorWeight*((q_1*q_2)>0.0)*(extraelec_veto < 0.5)*(extramuon_veto < 0.5)*(dilepton_veto < 0.5)*(iso_1 < 0.1)*(byCombinedIsolationDeltaBetaCorrRaw3Hits_2 < 1.5)" +
						("*(againstElectronVLooseMVA5_2 > 0.5)*(againstMuonTight3_2 > 0.5)" if channel == "mt" else
						 "*(againstElectronTightMVA5_2 > 0.5)*(againstMuonLoose3_2 > 0.5)"),
					"qcd",
					nick_suffix=nick_suffix
			)
			Sample._add_input(
					config,
					"DYJetsToLLM50_RunIISpring15DR74_Asympt25ns_13TeV_MINIAODSIM/*.root",
					channel+"_ztt/ntuple " + channel + "_zttlep/ntuple",
					lumi,
					"crossSectionPerEventWeight*numberGeneratedEventsWeight*generatorWeight*((q_1*q_2)>0.0)*(extraelec_veto < 0.5)*(extramuon_veto < 0.5)*(dilepton_veto < 0.5)*(iso_1 < 0.1)*(byCombinedIsolationDeltaBetaCorrRaw3Hits_2 < 1.5)" +
						("*(againstElectronVLooseMVA5_2 > 0.5)*(againstMuonTight3_2 > 0.5)" if channel == "mt" else
						 "*(againstElectronTightMVA5_2 > 0.5)*(againstMuonLoose3_2 > 0.5)"),
					"noplot_ztt_mc_qcd_control",
					nick_suffix=nick_suffix
			)
			Sample._add_input(
					config,
					"DYJetsToLLM50_RunIISpring15DR74_Asympt25ns_13TeV_MINIAODSIM/*.root",
					channel+"_zl/ntuple " + channel + "_zj/ntuple " + channel + "_zll/ntuple",
					lumi,
					"crossSectionPerEventWeight*numberGeneratedEventsWeight*generatorWeight*((q_1*q_2)>0.0)*(extraelec_veto < 0.5)*(extramuon_veto < 0.5)*(dilepton_veto < 0.5)*(iso_1 < 0.1)*(byCombinedIsolationDeltaBetaCorrRaw3Hits_2 < 1.5)" +
						("*(againstElectronVLooseMVA5_2 > 0.5)*(againstMuonTight3_2 > 0.5)" if channel == "mt" else
						 "*(againstElectronTightMVA5_2 > 0.5)*(againstMuonLoose3_2 > 0.5)"),
					"noplot_zll_qcd_control",
					nick_suffix=nick_suffix
			)
			Sample._add_input(
					config,
					"TTJets_RunIISpring15DR74_Asympt25ns_13TeV_MINIAODSIM/*.root",
					channel+"_z/ntuple",
					lumi,
					"crossSectionPerEventWeight*numberGeneratedEventsWeight*generatorWeight*((q_1*q_2)>0.0)*(extraelec_veto < 0.5)*(extramuon_veto < 0.5)*(dilepton_veto < 0.5)*(iso_1 < 0.1)*(byCombinedIsolationDeltaBetaCorrRaw3Hits_2 < 1.5)" +
						("*(againstElectronVLooseMVA5_2 > 0.5)*(againstMuonTight3_2 > 0.5)" if channel == "mt" else
						 "*(againstElectronTightMVA5_2 > 0.5)*(againstMuonLoose3_2 > 0.5)"),
					"noplot_ttj_qcd_control",
					nick_suffix=nick_suffix
			)
			
			if not "EstimateQcd" in config.get("analysis_modules", []):
				config.setdefault("analysis_modules", []).append("EstimateQcd")
			config.setdefault("qcd_data_control_nicks", []).append("qcd"+nick_suffix)
			config.setdefault("qcd_data_substract_nicks", []).append(" ".join([nick+nick_suffix for nick in "noplot_ztt_mc_qcd_control noplot_zll_qcd_control noplot_ttj_qcd_control noplot_wj_ss".split()]))
			config.setdefault("qcd_extrapolation_factors_ss_os", []).append(1.06)

		elif channel == "em":
			Sample._add_input(
					config,
					"MuEG_Run2012?_22Jan2013_8TeV/*.root",
					"em_dirIso/ntuple",
					1.0,
					"eventWeight*((q_1*q_2)>0.0)",
					"qcd",
					nick_suffix=nick_suffix
			)
		else:
			log.error("Sample config (QCD) currently not implemented for channel \"%s\"!" % channel)
		
		if not kwargs.get("no_plot", False):
			Sample._add_plot(config, "bkg", "HIST", "F", "qcd", nick_suffix)
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


# TODO: move to separate file if needed
cutSequenceDict = {
	"mt" : ["((q_1*q_2)<0.0)",
		"(againstElectronVLooseMVA5_2 > 0.5)*(againstMuonTight3_2 > 0.5)",
		"(extraelec_veto < 0.5)*(extramuon_veto < 0.5)*(dilepton_veto < 0.5)",
		"(iso_1 < 0.1)",
		"(byCombinedIsolationDeltaBetaCorrRaw3Hits_2 < 1.5)"],
	"et" : ["((q_1*q_2)<0.0)",
		"(againstElectronTightMVA5_2 > 0.5)*(againstMuonLoose3_2 > 0.5)",
		"(extraelec_veto < 0.5)*(extramuon_veto < 0.5)*(dilepton_veto < 0.5)",
		"(iso_1 < 0.1)",
		"(byCombinedIsolationDeltaBetaCorrRaw3Hits_2 < 1.5)"],
	"em" : ["((q_1*q_2)<0.0)",
		"(extraelec_veto < 0.5)*(extramuon_veto < 0.5)",
		"(iso_1 < 0.15)",
		"(iso_2 < 0.15)",
		"1."]
}

def cut_string(channel, cut_step):

	if not isinstance(cut_step, int):
		raise TypeError("cut step must be an integer")
	if not channel in cutSequenceDict.keys():
		raise TypeError("no cut values implemented for channel %s" % channel)
	if (cut_step > len(cutSequenceDict[channel])):
		raise ValueError("no cut corresponding to step %d for channel %s" % (cut_step, channel))

	string = ""
	for icut in range(cut_step):
		string = string + "*" + cutSequenceDict[channel][icut]
	return string

