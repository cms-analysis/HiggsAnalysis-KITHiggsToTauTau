
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import copy

import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.samples as samples

#TODO: pass this as a configuration parameter, if
# used more than for a few tests
cutStep = 5


class Samples(samples.SamplesBase):

	def __init__(self):
		super(Samples, self).__init__()
	
	def get_config(self, samples, channel, category, nick_suffix="", postfit_scales=None, **kwargs):
		config = super(Samples, self).get_config(
				samples=samples,
				channel=channel,
				category=category,
				nick_suffix=nick_suffix,
				postfit_scales=postfit_scales,
				**kwargs
		)
		
		config.setdefault("analysis_modules", []).append("PrintInfos")
		if channel in ["mt", "et"]:
			config.setdefault("analysis_modules", []).append("CorrectNegativeBinContents")
			config.setdefault("nicks_correct_negative_bins", []).append("qcd"+nick_suffix)
		
		return config
	
	def data(self, config, channel, category, nick_suffix, **kwargs):
		scale_factor = 1.0
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("data_obs", 1.0)
		
		if channel == "mt":
			Samples._add_input(
					config,
					"SingleMuon_Run2015B_PromptRecov1_13TeV_MINIAOD/*.root",
					channel+"_z/ntuple",
					1.0,
					"eventWeight" + cut_string(channel, cutStep),
					"data",
					nick_suffix=nick_suffix
			)
		elif channel == "et":
			Samples._add_input(
					config,
					"SingleElectron_Run2015B_PromptRecov1_13TeV_MINIAOD/*.root",
					channel+"_z/ntuple",
					1.0,
					"eventWeight" + cut_string(channel, cutStep),
					"data",
					nick_suffix=nick_suffix
			)
		elif channel == "em":
			Samples._add_input(
					config,
					"MuonEG_Run2015B_PromptRecov1_13TeV_MINIAOD/*.root",
					channel+"/ntuple",
					1.0,
					"eventWeight" + cut_string(channel, cutStep),
					"data",
					nick_suffix=nick_suffix
			)
		else:
			log.error("Sample config (Data) currently not implemented for channel \"%s\"!" % channel)
		
		Samples._add_plot(config, "data", "E", "ELP", "data", nick_suffix)
		return config
	
	def ztt(self, config, channel, category, nick_suffix, lumi=40.03, **kwargs):
		scale_factor = 1.0
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("ZTT", 1.0)
		
		if channel in ["mt", "et"]:
			Samples._add_input(
					config,
					"DYJetsToLLM50_RunIISpring15DR74_Asympt25ns_13TeV_MINIAODSIM/*.root",
					channel+"_ztt/ntuple " + channel + "_zttlep/ntuple",
					lumi,
					"eventWeight" + cut_string(channel, cutStep),
					"ztt",
					nick_suffix=nick_suffix
			)
		elif channel == "em":
			Samples._add_input(
					config,
					"DYJetsToLLM50_RunIISpring15DR74_Asympt25ns_13TeV_MINIAODSIM/*.root",
					channel+"_tt/ntuple",
					lumi,
					"eventWeight" + cut_string(channel, cutStep),
					"ztt",
					nick_suffix=nick_suffix
			)
		else:
			log.error("Sample config (ZTT) currently not implemented for channel \"%s\"!" % channel)
		
		Samples._add_plot(config, "bkg", "HIST", "F", "ztt", nick_suffix)
		
		return config
	
	def zll(self, config, channel, category, nick_suffix, lumi=40.03, **kwargs):
		scale_factor = lumi
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("ZL", 1.0)
		
		if channel in ["mt", "et"]:
			Samples._add_input(
					config,
					"DYJetsToLLM50_RunIISpring15DR74_Asympt25ns_13TeV_MINIAODSIM/*.root",
					channel+"_zll/ntuple " + channel + "_zl/ntuple " + channel + "_zj/ntuple",
					lumi,
					"eventWeight" + cut_string(channel, cutStep),
					"zll",
					nick_suffix=nick_suffix
			)
		elif channel == "em":
			Samples._add_input(
					config,
					"DYJetsToLLM50_RunIISpring15DR74_Asympt25ns_13TeV_MINIAODSIM/*.root",
					channel+"_ee/ntuple " + channel + "_mm/ntuple",
					lumi,
					"eventWeight" + cut_string(channel, cutStep),
					"zll",
					nick_suffix=nick_suffix
			)
		else:
			log.error("Sample config (ZLL) currently not implemented for channel \"%s\"!" % channel)
		
		Samples._add_plot(config, "bkg", "HIST", "F", "zl", nick_suffix)
		return config
	

	def ttj(self, config, channel, category, nick_suffix, lumi=40.03, **kwargs):
		scale_factor = lumi
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("TTJ", 1.0)
		
		if channel in ["mt", "et"]:
			Samples._add_input(
					config,
					"TT_RunIISpring15DR74_Asympt25ns_13TeV_MINIAODSIM/*.root",
					channel+"_z/ntuple",
					lumi,
					"eventWeight" + cut_string(channel, cutStep),
					"ttj",
					nick_suffix=nick_suffix
			)

		elif channel == "em":
			Samples._add_input(
					config,
					"TT_RunIISpring15DR74_Asympt25ns_13TeV_MINIAODSIM/*.root",
					channel+"/ntuple",
					lumi,
					"eventWeight" + cut_string(channel, cutStep),
					"ttj",
					nick_suffix=nick_suffix
			)
		else:
			log.error("Sample config (TTJ) currently not implemented for channel \"%s\"!" % channel)
		
		Samples._add_plot(config, "bkg", "HIST", "F", "ttj", nick_suffix)
		return config

	def vv(self, config, channel, category, nick_suffix, lumi=40.03, **kwargs):
		scale_factor = lumi
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("Dibosons", 1.0)
		
		if channel in ["mt", "et", "em"]:
			Samples._add_input(
					config,
					"??To*_RunIISpring15DR74_Asympt25ns_13TeV_MINIAODSIM/*.root",
					channel+("_z" if channel in ["et", "mt"] else "") + "/ntuple",
					lumi,
					"eventWeight" + cut_string(channel, cutStep),
					"vv",
					nick_suffix=nick_suffix
			)
		else:
			log.error("Sample config (VV) currently not implemented for channel \"%s\"!" % channel)
		
		Samples._add_plot(config, "bkg", "HIST", "F", "vv", nick_suffix)
		return config
	
	def wj(self, config, channel, category, nick_suffix, lumi=40.03, **kwargs):
		scale_factor = lumi
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("WJets", 1.0)
		
		if channel in ["mt", "et"]:
			Samples._add_input(
					config,
					"WJetsToLNu_RunIISpring15DR74_Asympt25ns_13TeV_MINIAODSIM/*.root",
					channel+"_z/ntuple",
					lumi,
					"eventWeight" + cut_string(channel, cutStep),
					"wj",
					nick_suffix=nick_suffix
			)
			Samples._add_input(
					config,
					"SingleMuon_Run2015B_PromptRecov1_13TeV_MINIAOD/*.root" if channel == "mt" else "SingleElectron_Run2015B_PromptRecov1_13TeV_MINIAOD/*root",
					channel+"_z/ntuple",
					1.0,
					"eventWeight" + cut_string(channel, cutStep) + "*(mt_1>80.0)",
					"noplot_wj_data_control"
			)
			Samples._add_input(
					config,
					"DYJetsToLLM50_RunIISpring15DR74_Asympt25ns_13TeV_MINIAODSIM/*.root",
					channel+"_ztt/ntuple " + channel + "_zttlep/ntuple",
					lumi,
					"eventWeight" + cut_string(channel, cutStep) + "*(mt_1>80.0)",
					"noplot_ztt_mc_wj_control",
					nick_suffix=nick_suffix
			)
			Samples._add_input(
					config,
					"DYJetsToLLM50_RunIISpring15DR74_Asympt25ns_13TeV_MINIAODSIM/*.root",
					channel+"_zl/ntuple " + channel + "_zj/ntuple " + channel + "_zll/ntuple",
					lumi,
					"eventWeight" + cut_string(channel, cutStep) + "*(mt_1>80.0)",
					"noplot_zll_wj_control",
					nick_suffix=nick_suffix
			)
			Samples._add_input(
					config,
					"TT_RunIISpring15DR74_Asympt25ns_13TeV_MINIAODSIM/*.root",
					channel+"_z/ntuple",
					lumi,
					"eventWeight" + cut_string(channel, cutStep) + "*(mt_1>80.0)",
					"noplot_ttj_wj_control",
					nick_suffix=nick_suffix
			)
			Samples._add_input(
					config,
					"??To*_RunIISpring15DR74_Asympt25ns_13TeV_MINIAODSIM/*.root",
					channel+"_z/ntuple",
					lumi,
					"eventWeight" + cut_string(channel, cutStep) + "*(mt_1>80.0)",
					"noplot_vv_wj_control",
					nick_suffix=nick_suffix
			)
			Samples._add_input(
					config,
					"WJetsToLNu_RunIISpring15DR74_Asympt25ns_13TeV_MINIAODSIM/*.root",
					channel+"_z/ntuple",
					lumi,
					"eventWeight" + cut_string(channel, cutStep),
					"noplot_wj_mc_signal",
					nick_suffix=nick_suffix
			)
			Samples._add_input(
					config,
					"WJetsToLNu_RunIISpring15DR74_Asympt25ns_13TeV_MINIAODSIM/*.root",
					channel+"_z/ntuple",
					lumi,
					"eventWeight" + cut_string(channel, cutStep) + "*(mt_1>80.0)",
					"noplot_wj_mc_control",
					nick_suffix=nick_suffix
			)

			if not "EstimateWjets" in config.get("analysis_modules", []):
				config.setdefault("analysis_modules", []).append("EstimateWjets")
			config.setdefault("wjets_shape_nicks", []).append("wj"+nick_suffix)
			config.setdefault("wjets_data_control_nicks", []).append("noplot_wj_data_control"+nick_suffix)
			config.setdefault("wjets_data_substract_nicks", []).append(" ".join([nick+nick_suffix for nick in "noplot_ztt_mc_wj_control noplot_zll_wj_control noplot_ttj_wj_control noplot_vv_wj_control".split()]))
			config.setdefault("wjets_mc_signal_nicks", []).append("noplot_wj_mc_signal"+nick_suffix)
			config.setdefault("wjets_mc_control_nicks", []).append("noplot_wj_mc_control"+nick_suffix)

		elif channel == "em":
			Samples._add_input(
					config,
					"WJetsToLNu_RunIISpring15DR74_Asympt25ns_13TeV_MINIAODSIM/*.root",
					channel+"/ntuple",
					lumi,
					"eventWeight" + cut_string(channel, cutStep),
					"wj",
					nick_suffix=nick_suffix
			)
		else:	
			log.error("Sample config (WJets) currently not implemented for channel \"%s\"!" % channel)
		
		if not kwargs.get("no_plot", False):
			Samples._add_plot(config, "bkg", "HIST", "F", "wj", nick_suffix)
		return config

	def qcd(self, config, channel, category, nick_suffix, lumi=40.03, **kwargs):
		scale_factor = 1.0
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("QCD", 1.0)
		
		if channel in ["et", "mt"]:

			# WJets for QCD estimate
			Samples._add_input(
					config,
					"WJetsToLNu_RunIISpring15DR74_Asympt25ns_13TeV_MINIAODSIM/*.root",
					channel+"_z/ntuple",
					lumi,
					"eventWeight*((q_1*q_2)>0.0)*(extraelec_veto < 0.5)*(extramuon_veto < 0.5)*(dilepton_veto < 0.5)*(iso_1 < 0.1)*(byCombinedIsolationDeltaBetaCorrRaw3Hits_2 < 1.5)" +
						("*(againstElectronVLooseMVA5_2 > 0.5)*(againstMuonTight3_2 > 0.5)" if channel == "mt" else
						 "*(againstElectronTightMVA5_2 > 0.5)*(againstMuonLoose3_2 > 0.5)"),
					"noplot_wj_ss",
					nick_suffix=nick_suffix
			)
			Samples._add_input(
					config,
					"SingleMuon_Run2015B_PromptRecov1_13TeV_MINIAOD/*.root" if channel == "mt" else "SingleElectron_Run2015B_PromptRecov1_13TeV_MINIAOD/*root",
					channel+"_z/ntuple",
					1.0,
					"((q_1*q_2)>0.0)*(extraelec_veto < 0.5)*(extramuon_veto < 0.5)*(dilepton_veto < 0.5)*(iso_1 < 0.1)*(byCombinedIsolationDeltaBetaCorrRaw3Hits_2 < 1.5)*(mt_1>80.0)" +
						("*(againstElectronVLooseMVA5_2 > 0.5)*(againstMuonTight3_2 > 0.5)" if channel == "mt" else
						 "*(againstElectronTightMVA5_2 > 0.5)*(againstMuonLoose3_2 > 0.5)"),
					"noplot_wj_ss_data_control",
					nick_suffix=nick_suffix
			)
			Samples._add_input(
					config,
					"DYJetsToLLM50_RunIISpring15DR74_Asympt25ns_13TeV_MINIAODSIM/*.root",
					channel+"_ztt/ntuple " + channel + "_zttlep/ntuple",
					lumi,
					"eventWeight*((q_1*q_2)>0.0)*(extraelec_veto < 0.5)*(extramuon_veto < 0.5)*(dilepton_veto < 0.5)*(iso_1 < 0.1)*(byCombinedIsolationDeltaBetaCorrRaw3Hits_2 < 1.5)*(mt_1>80.0)" +
						("*(againstElectronVLooseMVA5_2 > 0.5)*(againstMuonTight3_2 > 0.5)" if channel == "mt" else
						 "*(againstElectronTightMVA5_2 > 0.5)*(againstMuonLoose3_2 > 0.5)"),
					"noplot_ztt_ss_mc_wj_control",
					nick_suffix=nick_suffix
			)
			Samples._add_input(
					config,
					"DYJetsToLLM50_RunIISpring15DR74_Asympt25ns_13TeV_MINIAODSIM/*.root",
					channel+"_zl/ntuple " + channel + "_zj/ntuple " + channel + "_zll/ntuple",
					lumi,
					"eventWeight*((q_1*q_2)>0.0)*(extraelec_veto < 0.5)*(extramuon_veto < 0.5)*(dilepton_veto < 0.5)*(iso_1 < 0.1)*(byCombinedIsolationDeltaBetaCorrRaw3Hits_2 < 1.5)*(mt_1>80.0)" +
						("*(againstElectronVLooseMVA5_2 > 0.5)*(againstMuonTight3_2 > 0.5)" if channel == "mt" else
						 "*(againstElectronTightMVA5_2 > 0.5)*(againstMuonLoose3_2 > 0.5)"),
					"noplot_zll_ss_wj_control",
					nick_suffix=nick_suffix
			)
			Samples._add_input(
					config,
					"TT_RunIISpring15DR74_Asympt25ns_13TeV_MINIAODSIM/*.root",
					channel+"_z/ntuple",
					lumi,
					"eventWeight*((q_1*q_2)>0.0)*(extraelec_veto < 0.5)*(extramuon_veto < 0.5)*(dilepton_veto < 0.5)*(iso_1 < 0.1)*(byCombinedIsolationDeltaBetaCorrRaw3Hits_2 < 1.5)*(mt_1>80.0)" +
						("*(againstElectronVLooseMVA5_2 > 0.5)*(againstMuonTight3_2 > 0.5)" if channel == "mt" else
						 "*(againstElectronTightMVA5_2 > 0.5)*(againstMuonLoose3_2 > 0.5)"),
					"noplot_ttj_ss_wj_control",
					nick_suffix=nick_suffix
			)
			Samples._add_input(
					config,
					"??To*_RunIISpring15DR74_Asympt25ns_13TeV_MINIAODSIM/*.root",
					channel+"_z/ntuple",
					lumi,
					"eventWeight*((q_1*q_2)>0.0)*(extraelec_veto < 0.5)*(extramuon_veto < 0.5)*(dilepton_veto < 0.5)*(iso_1 < 0.1)*(byCombinedIsolationDeltaBetaCorrRaw3Hits_2 < 1.5)*(mt_1>80.0)" +
						("*(againstElectronVLooseMVA5_2 > 0.5)*(againstMuonTight3_2 > 0.5)" if channel == "mt" else
						 "*(againstElectronTightMVA5_2 > 0.5)*(againstMuonLoose3_2 > 0.5)"),
					"noplot_vv_ss_wj_control",
					nick_suffix=nick_suffix
			)
			Samples._add_input(
					config,
					"WJetsToLNu_RunIISpring15DR74_Asympt25ns_13TeV_MINIAODSIM/*.root",
					channel+"_z/ntuple",
					lumi,
					"eventWeight*((q_1*q_2)>0.0)*(extraelec_veto < 0.5)*(extramuon_veto < 0.5)*(dilepton_veto < 0.5)*(iso_1 < 0.1)*(byCombinedIsolationDeltaBetaCorrRaw3Hits_2 < 1.5)" +
						("*(againstElectronVLooseMVA5_2 > 0.5)*(againstMuonTight3_2 > 0.5)" if channel == "mt" else
						 "*(againstElectronTightMVA5_2 > 0.5)*(againstMuonLoose3_2 > 0.5)"),
					"noplot_wj_ss_mc_signal",
					nick_suffix=nick_suffix
			)
			Samples._add_input(
					config,
					"WJetsToLNu_RunIISpring15DR74_Asympt25ns_13TeV_MINIAODSIM/*.root",
					channel+"_z/ntuple",
					lumi,
					"eventWeight*((q_1*q_2)>0.0)*(extraelec_veto < 0.5)*(extramuon_veto < 0.5)*(dilepton_veto < 0.5)*(iso_1 < 0.1)*(byCombinedIsolationDeltaBetaCorrRaw3Hits_2 < 1.5)*(mt_1>80.0)" +
						("*(againstElectronVLooseMVA5_2 > 0.5)*(againstMuonTight3_2 > 0.5)" if channel == "mt" else
						 "*(againstElectronTightMVA5_2 > 0.5)*(againstMuonLoose3_2 > 0.5)"),
					"noplot_wj_ss_mc_control",
					nick_suffix=nick_suffix
			)
			
			if not "EstimateWjets" in config.get("analysis_modules", []):
				config.setdefault("analysis_modules", []).append("EstimateWjets")
			config.setdefault("wjets_shape_nicks", []).append("noplot_wj_ss"+nick_suffix)
			config.setdefault("wjets_data_control_nicks", []).append("noplot_wj_ss_data_control"+nick_suffix)
			config.setdefault("wjets_data_substract_nicks", []).append(" ".join([nick+nick_suffix for nick in "noplot_ztt_ss_mc_wj_control noplot_zll_ss_wj_control noplot_ttj_ss_wj_control noplot_vv_ss_wj_control".split()]))
			config.setdefault("wjets_mc_signal_nicks", []).append("noplot_wj_ss_mc_signal"+nick_suffix)
			config.setdefault("wjets_mc_control_nicks", []).append("noplot_wj_ss_mc_control"+nick_suffix)

			# QCD
			Samples._add_input(
					config,
					"SingleMuon_Run2015B_PromptRecov1_13TeV_MINIAOD/*.root" if channel == "mt" else "SingleElectron_Run2015B_PromptRecov1_13TeV_MINIAOD/*root",
					channel+"_z/ntuple",
					1.0,
					"((q_1*q_2)>0.0)*(extraelec_veto < 0.5)*(extramuon_veto < 0.5)*(dilepton_veto < 0.5)*(iso_1 < 0.1)*(byCombinedIsolationDeltaBetaCorrRaw3Hits_2 < 1.5)" +
						("*(againstElectronVLooseMVA5_2 > 0.5)*(againstMuonTight3_2 > 0.5)" if channel == "mt" else
						 "*(againstElectronTightMVA5_2 > 0.5)*(againstMuonLoose3_2 > 0.5)"),
					"qcd",
					nick_suffix=nick_suffix
			)
			Samples._add_input(
					config,
					"DYJetsToLLM50_RunIISpring15DR74_Asympt25ns_13TeV_MINIAODSIM/*.root",
					channel+"_ztt/ntuple " + channel + "_zttlep/ntuple",
					lumi,
					"eventWeight*((q_1*q_2)>0.0)*(extraelec_veto < 0.5)*(extramuon_veto < 0.5)*(dilepton_veto < 0.5)*(iso_1 < 0.1)*(byCombinedIsolationDeltaBetaCorrRaw3Hits_2 < 1.5)" +
						("*(againstElectronVLooseMVA5_2 > 0.5)*(againstMuonTight3_2 > 0.5)" if channel == "mt" else
						 "*(againstElectronTightMVA5_2 > 0.5)*(againstMuonLoose3_2 > 0.5)"),
					"noplot_ztt_mc_qcd_control",
					nick_suffix=nick_suffix
			)
			Samples._add_input(
					config,
					"DYJetsToLLM50_RunIISpring15DR74_Asympt25ns_13TeV_MINIAODSIM/*.root",
					channel+"_zl/ntuple " + channel + "_zj/ntuple " + channel + "_zll/ntuple",
					lumi,
					"eventWeight*((q_1*q_2)>0.0)*(extraelec_veto < 0.5)*(extramuon_veto < 0.5)*(dilepton_veto < 0.5)*(iso_1 < 0.1)*(byCombinedIsolationDeltaBetaCorrRaw3Hits_2 < 1.5)" +
						("*(againstElectronVLooseMVA5_2 > 0.5)*(againstMuonTight3_2 > 0.5)" if channel == "mt" else
						 "*(againstElectronTightMVA5_2 > 0.5)*(againstMuonLoose3_2 > 0.5)"),
					"noplot_zll_qcd_control",
					nick_suffix=nick_suffix
			)
			Samples._add_input(
					config,
					"TT_RunIISpring15DR74_Asympt25ns_13TeV_MINIAODSIM/*.root",
					channel+"_z/ntuple",
					lumi,
					"eventWeight*((q_1*q_2)>0.0)*(extraelec_veto < 0.5)*(extramuon_veto < 0.5)*(dilepton_veto < 0.5)*(iso_1 < 0.1)*(byCombinedIsolationDeltaBetaCorrRaw3Hits_2 < 1.5)" +
						("*(againstElectronVLooseMVA5_2 > 0.5)*(againstMuonTight3_2 > 0.5)" if channel == "mt" else
						 "*(againstElectronTightMVA5_2 > 0.5)*(againstMuonLoose3_2 > 0.5)"),
					"noplot_ttj_qcd_control",
					nick_suffix=nick_suffix
			)
			Samples._add_input(
					config,
					"??To*_RunIISpring15DR74_Asympt25ns_13TeV_MINIAODSIM/*.root",
					channel+"_z/ntuple",
					lumi,
					"eventWeight*((q_1*q_2)>0.0)*(extraelec_veto < 0.5)*(extramuon_veto < 0.5)*(dilepton_veto < 0.5)*(iso_1 < 0.1)*(byCombinedIsolationDeltaBetaCorrRaw3Hits_2 < 1.5)" +
						("*(againstElectronVLooseMVA5_2 > 0.5)*(againstMuonTight3_2 > 0.5)" if channel == "mt" else
						 "*(againstElectronTightMVA5_2 > 0.5)*(againstMuonLoose3_2 > 0.5)"),
					"noplot_vv_qcd_control",
					nick_suffix=nick_suffix
			)
			
			if not "EstimateQcd" in config.get("analysis_modules", []):
				config.setdefault("analysis_modules", []).append("EstimateQcd")
			config.setdefault("qcd_data_control_nicks", []).append("qcd"+nick_suffix)
			config.setdefault("qcd_data_substract_nicks", []).append(" ".join([nick+nick_suffix for nick in "noplot_ztt_mc_qcd_control noplot_zll_qcd_control noplot_ttj_qcd_control noplot_vv_qcd_control noplot_wj_ss".split()]))
			config.setdefault("qcd_extrapolation_factors_ss_os", []).append(1.06)
			config.setdefault("qcd_subtract_shape", []).append(True)

		elif channel == "em":
			Samples._add_input(
					config,
					"MuonEG_Run2015B_PromptRecov1_13TeV_MINIAOD/*.root",
					channel+"/ntuple",
					1.0,
					"((q_1*q_2)>0.0)*(extraelec_veto < 0.5)*(extramuon_veto < 0.5)*(iso_1 < 0.15)*(iso_2 < 0.15)",
					"qcd",
					nick_suffix=nick_suffix
			)
		else:
			log.error("Sample config (QCD) currently not implemented for channel \"%s\"!" % channel)
		
		if not kwargs.get("no_plot", False):
			Samples._add_plot(config, "bkg", "HIST", "F", "qcd", nick_suffix)
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
		"1.0"]
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

