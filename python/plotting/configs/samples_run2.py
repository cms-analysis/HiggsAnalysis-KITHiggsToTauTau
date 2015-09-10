
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import copy

import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.samples as samples

#TODO: pass this as a configuration parameter, if
# used more than for a few tests
cut_step = 5


class Samples(samples.SamplesBase):

	@staticmethod
	def cut_string(channel, exclude_cuts=None):
		if exclude_cuts is None:
			exclude_cuts = []
		
		cuts = {}
		if channel == "mt":
			cuts["mt"] = "(mt_1<30.0)"
			cuts["anti_lepton_tau_discriminators"] = "(againstElectronVLooseMVA5_2 > 0.5)*(againstMuonTight3_2 > 0.5)"
			cuts["extra_lepton_veto"] = "(extraelec_veto < 0.5)*(extramuon_veto < 0.5)*(dilepton_veto < 0.5)"
			cuts["iso_1"] = "(iso_1 < 0.1)"
			cuts["iso_2"] = "(byCombinedIsolationDeltaBetaCorrRaw3Hits_2 < 1.5)"
		elif channel == "et":
			cuts["mt"] = "(mt_1<30.0)"
			cuts["anti_lepton_tau_discriminators"] = "(againstElectronTightMVA5_2 > 0.5)*(againstMuonLoose3_2 > 0.5)"
			cuts["extra_lepton_veto"] = "(extraelec_veto < 0.5)*(extramuon_veto < 0.5)*(dilepton_veto < 0.5)"
			cuts["iso_1"] = "(iso_1 < 0.1)"
			cuts["iso_2"] = "(byCombinedIsolationDeltaBetaCorrRaw3Hits_2 < 1.5)"
		elif channel == "em":
			cuts["mt"] = "(mt_1<30.0)"
			cuts["extra_lepton_veto"] = "(extraelec_veto < 0.5)*(extramuon_veto < 0.5)"
			cuts["iso_1"] = "(iso_1 < 0.15)"
			cuts["iso_2"] = "(iso_2 < 0.15)"
		elif channel == "tt":
			cuts["mt"] = "(mt_1<30.0)"
			cuts["extra_lepton_veto"] = "(extraelec_veto < 0.5)*(extramuon_veto < 0.5)"
			cuts["iso_1"] = "(iso_1 < 0.15)"
			cuts["iso_2"] = "(iso_2 < 0.15)"
		else:
			log.fatal("No cut values implemented for channel \"%s\"!" % channel)
			sys.exit(1)
		
		cuts_list = [cut for (name, cut) in cuts.iteritems() if not name in exclude_cuts]
		if len(cuts_list) == 0:
			cuts_list.append("1.0")
		
		return "*".join(cuts_list)

	def __init__(self):
		super(Samples, self).__init__()
		
		self.period = "run2"
	
	def data(self, config, channel, weight, nick_suffix, exclude_cuts=None, **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []
		
		scale_factor = 1.0
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("data_obs", 1.0)
		
		if channel == "mt":
			Samples._add_input(
					config,
					"SingleMuon_Run2015B_PromptRecov1_13TeV_MINIAOD/*.root",
					channel+"_jecUnc_z/ntuple",
					1.0,
					weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts) + "*((q_1*q_2)<0.0)",
					"data",
					nick_suffix=nick_suffix
			)
		elif channel == "et":
			Samples._add_input(
					config,
					"SingleElectron_Run2015B_PromptRecov1_13TeV_MINIAOD/*.root",
					channel+"_jecUnc_z/ntuple",
					1.0,
					weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts) + "*((q_1*q_2)<0.0)",
					"data",
					nick_suffix=nick_suffix
			)
		elif channel == "em":
			Samples._add_input(
					config,
					"MuonEG_Run2015B_PromptRecov1_13TeV_MINIAOD/*.root",
					channel+"_jecUnc/ntuple",
					1.0,
					weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts) + "*((q_1*q_2)<0.0)",
					"data",
					nick_suffix=nick_suffix
			)
		elif channel == "tt":
			Samples._add_input(
					config,
					"Tau_Run2015B_PromptRecov1_13TeV_MINIAOD/*.root",
					channel+"_jecUnc/ntuple",
					1.0,
					weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts) + "*((q_1*q_2)<0.0)",
					"data",
					nick_suffix=nick_suffix
			)
		else:
			log.error("Sample config (Data) currently not implemented for channel \"%s\"!" % channel)
		
		Samples._add_plot(config, "data", "E", "ELP", "data", nick_suffix)
		return config
	
	def ztt(self, config, channel, weight, nick_suffix, lumi=40.03, exclude_cuts=None, **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []
		
		scale_factor = 1.0
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("ZTT", 1.0)
		
		if channel in ["mt", "et"]:
			Samples._add_input(
					config,
					"DYJetsToLLM50_RunIISpring15DR74_Asympt25ns_13TeV_MINIAOD*/*.root",
					channel+"_jecUncNom_ztt/ntuple " + channel+"_jecUncNom_zttlep/ntuple",
					lumi,
					weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts) + "*((q_1*q_2)<0.0)",
					"ztt",
					nick_suffix=nick_suffix
			)
		elif channel in ["em", "tt"]:
			Samples._add_input(
					config,
					"DYJetsToLLM50_RunIISpring15DR74_Asympt25ns_13TeV_MINIAOD*/*.root",
					channel+"_jecUncNom_tt/ntuple",
					lumi,
					weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts) + "*((q_1*q_2)<0.0)",
					"ztt",
					nick_suffix=nick_suffix
			)
		else:
			log.error("Sample config (ZTT) currently not implemented for channel \"%s\"!" % channel)
		
		Samples._add_plot(config, "bkg", "HIST", "F", "ztt", nick_suffix)
		
		return config
	
	def zll(self, config, channel, weight, nick_suffix, lumi=40.03, exclude_cuts=None, **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []
		
		scale_factor = lumi
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("ZL", 1.0)
		
		if channel in ["mt", "et"]:
			Samples._add_input(
					config,
					"DYJetsToLLM50_RunIISpring15DR74_Asympt25ns_13TeV_MINIAOD*/*.root",
					channel+"_jecUncNom_zll/ntuple " + channel+"_jecUncNom_zl/ntuple " + channel+"_jecUncNom_zj/ntuple",
					lumi,
					weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts) + "*((q_1*q_2)<0.0)",
					"zll",
					nick_suffix=nick_suffix
			)
		elif channel in ["em", "tt"]:
			Samples._add_input(
					config,
					"DYJetsToLLM50_RunIISpring15DR74_Asympt25ns_13TeV_MINIAOD*/*.root",
					channel+"_jecUncNom_ee/ntuple " + channel+"_jecUncNom_mm/ntuple",
					lumi,
					weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts) + "*((q_1*q_2)<0.0)",
					"zll",
					nick_suffix=nick_suffix
			)
		else:
			log.error("Sample config (ZLL) currently not implemented for channel \"%s\"!" % channel)
		
		Samples._add_plot(config, "bkg", "HIST", "F", "zl", nick_suffix)
		return config
	

	def ttj(self, config, channel, weight, nick_suffix, lumi=40.03, exclude_cuts=None, **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []
		
		scale_factor = lumi
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("TTJ", 1.0)
		
		if channel in ["mt", "et"]:
			Samples._add_input(
					config,
					"TT_RunIISpring15DR74_Asympt25ns_13TeV_MINIAOD*/*.root",
					channel+"_jecUncNom_z/ntuple",
					lumi,
					weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts) + "*((q_1*q_2)<0.0)",
					"ttj",
					nick_suffix=nick_suffix
			)

		elif channel in ["em", "tt"]:
			Samples._add_input(
					config,
					"TT_RunIISpring15DR74_Asympt25ns_13TeV_MINIAOD*/*.root",
					channel+"_jecUncNom/ntuple",
					lumi,
					weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts) + "*((q_1*q_2)<0.0)",
					"ttj",
					nick_suffix=nick_suffix
			)
		else:
			log.error("Sample config (TTJ) currently not implemented for channel \"%s\"!" % channel)
		
		Samples._add_plot(config, "bkg", "HIST", "F", "ttj", nick_suffix)
		return config

	def vv(self, config, channel, weight, nick_suffix, lumi=40.03, exclude_cuts=None, **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []
		
		scale_factor = lumi
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("Dibosons", 1.0)
		
		if channel in ["mt", "et", "em", "tt"]:
			Samples._add_input(
					config,
					"??To*_RunIISpring15DR74_Asympt25ns_13TeV_MINIAOD*/*.root",
					channel+"_jecUncNom"+("_z" if channel in ["et", "mt"] else "")+"/ntuple",
					lumi,
					weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts) + "*((q_1*q_2)<0.0)",
					"vv",
					nick_suffix=nick_suffix
			)
		else:
			log.error("Sample config (VV) currently not implemented for channel \"%s\"!" % channel)
		
		Samples._add_plot(config, "bkg", "HIST", "F", "vv", nick_suffix)
		return config
	
	def wj(self, config, channel, weight, nick_suffix, lumi=40.03, exclude_cuts=None, **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []
		
		scale_factor = lumi
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("WJets", 1.0)
		
		if channel in ["mt", "et"]:
			Samples._add_input(
					config,
					"WJetsToLNu_RunIISpring15DR74_Asympt25ns_13TeV_MINIAOD*/*.root",
					channel+"_jecUncNom_z/ntuple",
					lumi,
					weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts) + "*((q_1*q_2)<0.0)",
					"wj",
					nick_suffix=nick_suffix
			)
			Samples._add_input(
					config,
					"SingleMuon_Run2015B_PromptRecov1_13TeV_MINIAOD/*.root" if channel == "mt" else "SingleElectron_Run2015B_PromptRecov1_13TeV_MINIAOD/*root",
					channel+"_jecUnc_z/ntuple",
					1.0,
					"eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["mt"]) + "*((q_1*q_2)<0.0)*(mt_1>80.0)",
					"noplot_wj_data_control"
			)
			Samples._add_input(
					config,
					"DYJetsToLLM50_RunIISpring15DR74_Asympt25ns_13TeV_MINIAOD*/*.root",
					channel+"_jecUncNom_ztt/ntuple " + channel + "_jecUncNom_zttlep/ntuple",
					lumi,
					"eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["mt"]) + "*((q_1*q_2)<0.0)*(mt_1>80.0)",
					"noplot_ztt_mc_wj_control",
					nick_suffix=nick_suffix
			)
			Samples._add_input(
					config,
					"DYJetsToLLM50_RunIISpring15DR74_Asympt25ns_13TeV_MINIAOD*/*.root",
					channel+"_jecUncNom_zl/ntuple " + channel+"_jecUncNom_zj/ntuple " + channel+"_jecUncNom_zll/ntuple",
					lumi,
					"eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["mt"]) + "*((q_1*q_2)<0.0)*(mt_1>80.0)",
					"noplot_zll_wj_control",
					nick_suffix=nick_suffix
			)
			Samples._add_input(
					config,
					"TT_RunIISpring15DR74_Asympt25ns_13TeV_MINIAOD*/*.root",
					channel+"_jecUncNom_z/ntuple",
					lumi,
					"eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["mt"]) + "*((q_1*q_2)<0.0)*(mt_1>80.0)",
					"noplot_ttj_wj_control",
					nick_suffix=nick_suffix
			)
			Samples._add_input(
					config,
					"??To*_RunIISpring15DR74_Asympt25ns_13TeV_MINIAOD*/*.root",
					channel+"_jecUncNom_z/ntuple",
					lumi,
					"eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["mt"]) + "*((q_1*q_2)<0.0)*(mt_1>80.0)",
					"noplot_vv_wj_control",
					nick_suffix=nick_suffix
			)
			Samples._add_input(
					config,
					"WJetsToLNu_RunIISpring15DR74_Asympt25ns_13TeV_MINIAOD*/*.root",
					channel+"_jecUncNom_z/ntuple",
					lumi,
					weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts) + "*((q_1*q_2)<0.0)",
					"noplot_wj_mc_signal",
					nick_suffix=nick_suffix
			)
			Samples._add_input(
					config,
					"WJetsToLNu_RunIISpring15DR74_Asympt25ns_13TeV_MINIAOD*/*.root",
					channel+"_jecUncNom_z/ntuple",
					lumi,
					"eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["mt"]) + "*((q_1*q_2)<0.0)*(mt_1>80.0)",
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

		elif channel in ["em", "tt"]:
			Samples._add_input(
					config,
					"WJetsToLNu_RunIISpring15DR74_Asympt25ns_13TeV_MINIAOD*/*.root",
					channel+"_jecUncNom/ntuple",
					lumi,
					weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts) + "*((q_1*q_2)<0.0)",
					"wj",
					nick_suffix=nick_suffix
			)
		else:	
			log.error("Sample config (WJets) currently not implemented for channel \"%s\"!" % channel)
		
		if not kwargs.get("no_plot", False):
			Samples._add_plot(config, "bkg", "HIST", "F", "wj", nick_suffix)
		return config

	def qcd(self, config, channel, weight, nick_suffix, lumi=40.03, exclude_cuts=None, **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []
		
		scale_factor = 1.0
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("QCD", 1.0)
		
		if channel in ["et", "mt"]:

			# WJets for QCD estimate
			Samples._add_input(
					config,
					"WJetsToLNu_RunIISpring15DR74_Asympt25ns_13TeV_MINIAOD*/*.root",
					channel+"_jecUncNom_z/ntuple",
					lumi,
					weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts) + "*((q_1*q_2)>0.0)",
					"noplot_wj_ss",
					nick_suffix=nick_suffix
			)
			Samples._add_input(
					config,
					"SingleMuon_Run2015B_PromptRecov1_13TeV_MINIAOD/*.root" if channel == "mt" else "SingleElectron_Run2015B_PromptRecov1_13TeV_MINIAOD/*root",
					channel+"_jecUnc_z/ntuple",
					1.0,
					weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["mt"]) + "*((q_1*q_2)>0.0)*(mt_1>80.0)",
					"noplot_wj_ss_data_control",
					nick_suffix=nick_suffix
			)
			Samples._add_input(
					config,
					"DYJetsToLLM50_RunIISpring15DR74_Asympt25ns_13TeV_MINIAOD*/*.root",
					channel+"_jecUncNom_ztt/ntuple " + channel+"_jecUncNom_zttlep/ntuple",
					lumi,
					weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["mt"]) + "*((q_1*q_2)>0.0)*(mt_1>80.0)",
					"noplot_ztt_ss_mc_wj_control",
					nick_suffix=nick_suffix
			)
			Samples._add_input(
					config,
					"DYJetsToLLM50_RunIISpring15DR74_Asympt25ns_13TeV_MINIAOD*/*.root",
					channel+"_jecUncNom_zl/ntuple " + channel+"_jecUncNom_zj/ntuple " + channel+"_jecUncNom_zll/ntuple",
					lumi,
					weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["mt"]) + "*((q_1*q_2)>0.0)*(mt_1>80.0)",
					"noplot_zll_ss_wj_control",
					nick_suffix=nick_suffix
			)
			Samples._add_input(
					config,
					"TT_RunIISpring15DR74_Asympt25ns_13TeV_MINIAOD*/*.root",
					channel+"_jecUncNom_z/ntuple",
					lumi,
					weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["mt"]) + "*((q_1*q_2)>0.0)*(mt_1>80.0)",
					"noplot_ttj_ss_wj_control",
					nick_suffix=nick_suffix
			)
			Samples._add_input(
					config,
					"??To*_RunIISpring15DR74_Asympt25ns_13TeV_MINIAOD*/*.root",
					channel+"_jecUncNom_z/ntuple",
					lumi,
					weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["mt"]) + "*((q_1*q_2)>0.0)*(mt_1>80.0)",
					"noplot_vv_ss_wj_control",
					nick_suffix=nick_suffix
			)
			Samples._add_input(
					config,
					"WJetsToLNu_RunIISpring15DR74_Asympt25ns_13TeV_MINIAOD*/*.root",
					channel+"_jecUncNom_z/ntuple",
					lumi,
					"eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts) + "*((q_1*q_2)>0.0)",
					"noplot_wj_ss_mc_signal",
					nick_suffix=nick_suffix
			)
			Samples._add_input(
					config,
					"WJetsToLNu_RunIISpring15DR74_Asympt25ns_13TeV_MINIAOD*/*.root",
					channel+"_jecUncNom_z/ntuple",
					lumi,
					"eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["mt"]) + "*((q_1*q_2)>0.0)*(mt_1>80.0)",
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
					channel+"_jecUnc_z/ntuple",
					1.0,
					weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts) + "*((q_1*q_2)>0.0)",
					"qcd",
					nick_suffix=nick_suffix
			)
			Samples._add_input(
					config,
					"DYJetsToLLM50_RunIISpring15DR74_Asympt25ns_13TeV_MINIAOD*/*.root",
					channel+"_jecUncNom_ztt/ntuple " + channel+"_jecUncNom_zttlep/ntuple",
					lumi,
					weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts) + "*((q_1*q_2)>0.0)",
					"noplot_ztt_mc_qcd_control",
					nick_suffix=nick_suffix
			)
			Samples._add_input(
					config,
					"DYJetsToLLM50_RunIISpring15DR74_Asympt25ns_13TeV_MINIAOD*/*.root",
					channel+"_jecUncNom_zl/ntuple " + channel+"_jecUncNom_zj/ntuple " + channel+"_jecUncNom_zll/ntuple",
					lumi,
					weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts) + "*((q_1*q_2)>0.0)",
					"noplot_zll_qcd_control",
					nick_suffix=nick_suffix
			)
			Samples._add_input(
					config,
					"TT_RunIISpring15DR74_Asympt25ns_13TeV_MINIAOD*/*.root",
					channel+"_jecUncNom_z/ntuple",
					lumi,
					weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts) + "*((q_1*q_2)>0.0)",
					"noplot_ttj_qcd_control",
					nick_suffix=nick_suffix
			)
			Samples._add_input(
					config,
					"??To*_RunIISpring15DR74_Asympt25ns_13TeV_MINIAOD*/*.root",
					channel+"_jecUncNom_z/ntuple",
					lumi,
					weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts) + "*((q_1*q_2)>0.0)",
					"noplot_vv_qcd_control",
					nick_suffix=nick_suffix
			)
			
			if not "EstimateQcdRun2" in config.get("analysis_modules", []):
				config.setdefault("analysis_modules", []).append("EstimateQcdRun2")
			config.setdefault("qcd_data_control_nicks", []).append("qcd"+nick_suffix)
			config.setdefault("qcd_data_substract_nicks", []).append(" ".join([nick+nick_suffix for nick in "noplot_ztt_mc_qcd_control noplot_zll_qcd_control noplot_ttj_qcd_control noplot_vv_qcd_control noplot_wj_ss".split()]))
			config.setdefault("qcd_extrapolation_factors_ss_os", []).append(1.06)
			config.setdefault("qcd_subtract_shape", []).append(True)

			if channel in ["mt", "et"]:
				if not "CorrectNegativeBinContents" in config.get("analysis_modules", []):
					config.setdefault("analysis_modules", []).append("CorrectNegativeBinContents")
				config.setdefault("nicks_correct_negative_bins", []).append("qcd"+nick_suffix)

		elif channel == "em":
			Samples._add_input(
					config,
					"MuonEG_Run2015B_PromptRecov1_13TeV_MINIAOD/*.root",
					channel+"_jecUnc/ntuple",
					1.0,
					weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts) + "*((q_1*q_2)>0.0)",
					"qcd",
					nick_suffix=nick_suffix
			)
		elif channel == "tt":
			Samples._add_input(
					config,
					"Tau_Run2015B_PromptRecov1_13TeV_MINIAOD/*.root",
					channel+"_jecUnc/ntuple",
					1.0,
					weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts) + "*((q_1*q_2)>0.0)",
					"qcd",
					nick_suffix=nick_suffix
			)
		else:
			log.error("Sample config (QCD) currently not implemented for channel \"%s\"!" % channel)
		
		if not kwargs.get("no_plot", False):
			Samples._add_plot(config, "bkg", "HIST", "F", "qcd", nick_suffix)
		return config
	
	def htt(self, config, channel, weight, nick_suffix, higgs_masses, normalise_signal_to_one_pb=False, lumi=40.03, exclude_cuts=None, **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []
		
		config = self.ggh(config, channel, weight, nick_suffix+"_noplot", higgs_masses, normalise_signal_to_one_pb,
		                  lumi=lumi, exclude_cuts=exclude_cuts, no_plot=True, **kwargs)
		config = self.qqh(config, channel, weight, nick_suffix+"_noplot", higgs_masses, normalise_signal_to_one_pb,
		                  lumi=lumi, exclude_cuts=exclude_cuts, no_plot=True, **kwargs)
		config = self.vh(config, channel, weight, nick_suffix+"_noplot", higgs_masses, normalise_signal_to_one_pb,
		                 lumi=lumi, exclude_cuts=exclude_cuts, no_plot=True, **kwargs)
		
		for mass in higgs_masses:
			if not "AddHistograms" in config.get("analysis_modules", []):
				config.setdefault("analysis_modules", []).append("AddHistograms")
			config.setdefault("histogram_nicks", []).append(" ".join([sample+str(mass)+nick_suffix+"_noplot" for sample in ["ggh", "qqh", "vh"]]))
			config.setdefault("sum_result_nicks", []).append("htt"+str(mass)+nick_suffix)
			
			Samples._add_plot(config, "sig", "LINE", "L", "htt"+str(mass), nick_suffix)
		return config
	
	def ggh(self, config, channel, weight, nick_suffix, higgs_masses, normalise_signal_to_one_pb=False, lumi=40.03, exclude_cuts=None, **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []
		
		scale_factor = lumi
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("ggh", 1.0)
		
		for mass in higgs_masses:
			if channel in ["tt", "et", "mt", "em", "mm"]:
				Samples._add_input(
						config,
						"GluGluHToTauTauM{mass}_RunIISpring15DR74_Asympt25ns_13TeV_MINIAOD_powhegpythia8/*.root".format(mass=str(mass)),
						channel+"_jecUncNom"+("_z" if channel in ["et", "mt"] else "")+"/ntuple",
						lumi,
						weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts) + "*((q_1*q_2)<0.0)",
						"ggh%s" % str(mass),
						nick_suffix=nick_suffix
				)
			else:
				log.error("Sample config (ggH%s) currently not implemented for channel \"%s\"!" % (str(mass), channel))
			
			if not kwargs.get("no_plot", False):
				Samples._add_plot(config, "sig", "LINE", "L", "ggh"+str(mass), nick_suffix)
		return config
	
	def qqh(self, config, channel, weight, nick_suffix, higgs_masses, normalise_signal_to_one_pb=False, lumi=40.03, exclude_cuts=None, **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []
		
		scale_factor = lumi
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("qqH", 1.0)
		
		for mass in higgs_masses:
			if channel in ["tt", "et", "mt", "em", "mm"]:
				Samples._add_input(
						config,
						"VBFHToTauTauM{mass}_RunIISpring15DR74_Asympt25ns_13TeV_MINIAOD_powhegpythia8/*.root".format(mass=str(mass)),
						channel+"_jecUncNom"+("_z" if channel in ["et", "mt"] else "")+"/ntuple",
						lumi,
						weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts) + "*((q_1*q_2)<0.0)",
						"qqh%s" % str(mass),
						nick_suffix=nick_suffix
			)
			else:
				log.error("Sample config (VBF%s) currently not implemented for channel \"%s\"!" % (str(mass), channel))
			
			if not kwargs.get("no_plot", False):
				Samples._add_plot(config, "sig", "LINE", "L", "qqh"+str(mass), nick_suffix)
		return config
	
	def vh(self, config, channel, weight, nick_suffix, higgs_masses, normalise_signal_to_one_pb=False, lumi=40.03, exclude_cuts=None, **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []
		
		scale_factor = lumi
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("VH", 1.0)
		
		for mass in higgs_masses:
			if channel in ["tt", "et", "mt", "em", "mm"]:
				Samples._add_input(
						config,
						"WminusHToTauTauM{mass}_RunIISpring15DR74_Asympt25ns_13TeV_MINIAOD_powhegpythia8/*.root".format(mass=str(mass)),
						channel+"_jecUncNom"+("_z" if channel in ["et", "mt"] else "")+"/ntuple",
						lumi,
						weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts) + "*((q_1*q_2)<0.0)",
						"wmh%s" % str(mass),
						nick_suffix=nick_suffix+"_noplot"
				)
				Samples._add_input(
						config,
						"WplusHToTauTauM{mass}_RunIISpring15DR74_Asympt25ns_13TeV_MINIAOD_powhegpythia8/*.root".format(mass=str(mass)),
						channel+"_jecUncNom"+("_z" if channel in ["et", "mt"] else "")+"/ntuple",
						lumi,
						weight+"*eventWeight" + Samples.cut_string(channel, exclude_cuts=exclude_cuts) + "*((q_1*q_2)<0.0)",
						"wph%s" % str(mass),
						nick_suffix=nick_suffix+"_noplot"
				)
				Samples._add_input(
						config,
						"ZHToTauTauM{mass}_RunIISpring15DR74_Asympt25ns_13TeV_MINIAOD_powhegpythia8/*.root".format(mass=str(mass)),
						channel+"_jecUncNom"+("_z" if channel in ["et", "mt"] else "")+"/ntuple",
						lumi,
						weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts) + "*((q_1*q_2)<0.0)",
						"zh%s" % str(mass),
						nick_suffix=nick_suffix+"_noplot"
				)
				
				if not "AddHistograms" in config.get("analysis_modules", []):
					config.setdefault("analysis_modules", []).append("AddHistograms")
				config.setdefault("histogram_nicks", []).append(" ".join([sample+str(mass)+nick_suffix+"_noplot" for sample in ["wmh", "wph", "zh"]]))
				config.setdefault("sum_result_nicks", []).append("vh"+str(mass)+nick_suffix)
			
			else:
				log.error("Sample config (VH%s) currently not implemented for channel \"%s\"!" % (str(mass), channel))
			
			if not kwargs.get("no_plot", False):
				Samples._add_plot(config, "sig", "LINE", "L", "vh"+str(mass), nick_suffix)
		return config

