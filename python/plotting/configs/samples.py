
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import copy

import Artus.Utility.jsonTools as jsonTools


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
		
		config.setdefault("analysis_modules", []).append("@CorrectNegativeBinContents")
		config.setdefault("analysis_modules", []).append("@PrintInfos")
		
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
		
		if (channel == "et") or (channel == "mt"):
			Sample._add_input(
					config,
					"Tau*_Run2012?_22Jan2013_8TeV/*.root",
					channel+"_dirIso_z_tauEs/ntuple",
					1.0,
					"eventWeight*((q_1*q_2)<0.0)*(pt_2>30.0)*(lep1MetMt<30.0)",
					"data",
					nick_suffix=nick_suffix
			)
		elif channel == "em":
			Sample._add_input(
					config,
					"MuEG_Run2012?_22Jan2013_8TeV/*.root",
					"em_dirIso/ntuple",
					1.0,
					"eventWeight*((q_1*q_2)<0.0)",
					"data",
					nick_suffix=nick_suffix
			)
		elif channel == "mm":
			Sample._add_input(
					config,
					"DoubleMu*_Run2012?_22Jan2013_8TeV/*.root",
					"mm_dirIso/ntuple",
					1.0,
					"eventWeight*((q_1*q_2)<0.0)",
					"data",
					nick_suffix=nick_suffix
			)
		else:
			log.error("Sample config (Data) currently not implemented for channel \"%s\"!" % channel)
		
		Sample._add_plot(config, "data", "E", "ELP", "data", nick_suffix)
		return config
	
	def ztt(self, config, channel, category, nick_suffix, lumi=19712.0, **kwargs):
		scale_factor = 1.0
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("ZTT", 1.0)
		
		if (channel == "et") or (channel == "mt") or (channel == "em") or (channel == "mm"):
			Sample._add_input(
					config,
					"*_PFembedded_Run2012?_22Jan2013_"+channel+"_8TeV/*.root",
					channel+"_dirIso/ntuple" if (channel == "em") or (channel == "mm") else channel+"_dirIso_z_tauEs/ntuple",
					1.0,
					"eventWeight*((q_1*q_2)<0.0)" + ("" if (channel == "em") or (channel == "mm") else "*(pt_2>30.0)*(lep1MetMt<30.0)"),
					"ztt",
					nick_suffix=nick_suffix
			)
			Sample._add_input(
					config,
					"*_PFembedded_Run2012?_22Jan2013_"+channel+"_8TeV/*.root",
					channel+"_dirIso/ntuple" if (channel == "em") or (channel == "mm") else channel+"_dirIso_z_tauEs/ntuple",
					1.0,
					"eventWeight*((q_1*q_2)<0.0)" + ("" if (channel == "em") or (channel == "mm") else "*(pt_2>30.0)*(lep1MetMt<30.0)"),
					"noplot_ztt_emb_inc",
					nick_suffix=nick_suffix
			)
			Sample._add_input(
					config,
					"DYJetsToLL_M_50_madgraph_8TeV/*.root",
					channel+"_dirIso_tt/ntuple" if (channel == "em") or (channel == "mm") else channel+"_dirIso_ztt_tauEsNom/ntuple",
					lumi,
					"eventWeight*((q_1*q_2)<0.0)" + ("" if (channel == "em") or (channel == "mm") else "*(pt_2>30.0)*(lep1MetMt<30.0)"),
					"noplot_ztt_mc_inc",
					nick_suffix=nick_suffix
			)
			Sample._add_input(
					config,
					"DYJetsToLL_M_50_madgraph_8TeV/*.root",
					channel+"_dirIso_tt/ntuple" if (channel == "em") or (channel == "mm") else channel+"_dirIso_ztt_tauEsNom/ntuple",
					lumi,
					"eventWeight*((q_1*q_2)<0.0)" + ("" if (channel == "em") or (channel == "mm") else "*(pt_2>30.0)*(lep1MetMt<30.0)"),
					"noplot_ztt_mc",
					nick_suffix=nick_suffix
			)
			config.setdefault("analysis_modules", []).append("EstimateZtt")
		else:
			log.error("Sample config (ZTT) currently not implemented for channel \"%s\"!" % channel)
		
		Sample._add_plot(config, "bkg", "HIST", "F", "ztt", nick_suffix)
		
		return config
	
	def zl(self, config, channel, category, nick_suffix, lumi=19712.0, **kwargs):
		scale_factor = lumi
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("ZL", 1.0)
		
		if (channel == "et") or (channel == "mt") or (channel == "em") or (channel == "mm"):
			Sample._add_input(
					config,
					"DYJetsToLL_M_50_madgraph_8TeV/*.root",
					channel+"_dirIso_ee/ntuple "+channel+"_dirIso_mm/ntuple" if (channel == "em") or (channel == "mm") else channel+"_dirIso_zl_tauEsNom/ntuple",
					lumi,
					"eventWeight*((q_1*q_2)<0.0)" + ("" if (channel == "em") or (channel == "mm") else "*(pt_2>30.0)*(lep1MetMt<30.0)"),
					"zl",
					nick_suffix=nick_suffix
			)
		else:
			log.error("Sample config (ZL) currently not implemented for channel \"%s\"!" % channel)
		
		Sample._add_plot(config, "bkg", "HIST", "F", "zl", nick_suffix)
		return config
	
	def zj(self, config, channel, category, nick_suffix, lumi=19712.0, **kwargs):
		scale_factor = lumi
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("ZJ", 1.0)
		
		if (channel == "et") or (channel == "mt"):
			Sample._add_input(
					config,
					"DYJetsToLL_M_50_madgraph_8TeV/*.root",
					channel+"_dirIso_zj_tauEsNom/ntuple",
					lumi,
					"eventWeight*((q_1*q_2)<0.0)*(pt_2>30.0)*(lep1MetMt<30.0)",
					"zj"
			)
			
			Sample._add_plot(config, "bkg", "HIST", "F", "zj", nick_suffix)
		elif (channel == "em") or (channel == "mm"):
			pass
		else:
			log.error("Sample config (ZJ) currently not implemented for channel \"%s\"!" % channel)
		
		return config
	
	def ttj(self, config, channel, category, nick_suffix, lumi=19712.0, **kwargs):
		scale_factor = lumi
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("TTJ", 1.0)
		
		if (channel == "et") or (channel == "mt"):
			Sample._add_input(
					config,
					"TTJets*_madgraph_tauola_8TeV/*.root",
					channel+"_dirIso_z_tauEs/ntuple",
					lumi,
					"eventWeight*((q_1*q_2)<0.0)*(pt_2>30.0)*(lep1MetMt<30.0)",
					"ttj",
					nick_suffix=nick_suffix
			)
		elif channel == "em":
			Sample._add_input(
					config,
					"TTJetsTo*_madgraph_tauola_8TeV/*.root",
					"em_dirIso/ntuple",
					lumi,
					"eventWeight*((q_1*q_2)<0.0)",
					"ttj",
					nick_suffix=nick_suffix
			)
			Sample._add_input(
					config,
					"T*_powheg_tauola_8TeV/*.root",
					"em_dirIso/ntuple",
					lumi,
					"eventWeight*((q_1*q_2)<0.0)",
					"ttj",
					nick_suffix=nick_suffix
			)
		elif channel == "mm":
			Sample._add_input(
					config,
					"TTJetsTo*_madgraph_tauola_8TeV/*.root",
					"mm_dirIso/ntuple",
					lumi,
					"eventWeight*((q_1*q_2)<0.0)",
					"ttj",
					nick_suffix=nick_suffix
			)
		else:
			log.error("Sample config (TTJ) currently not implemented for channel \"%s\"!" % channel)
		
		Sample._add_plot(config, "bkg", "HIST", "F", "ttj", nick_suffix)
		return config
	
	def vv(self, config, channel, category, nick_suffix, lumi=19712.0, **kwargs):
		scale_factor = lumi
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("Dibosons", 1.0)
		
		if (channel == "et") or (channel == "mt"):
			Sample._add_input(
					config,
					"??_pythia_tauola_8TeV/*.root",
					channel+"_dirIso_z_tauEs/ntuple",
					lumi,
					"eventWeight*((q_1*q_2)<0.0)*(pt_2>30.0)*(lep1MetMt<30.0)",
					"vv",
					nick_suffix=nick_suffix
			)
		elif channel == "em":
			Sample._add_input(
					config,
					"??JetsTo*_madgraph_tauola_8TeV/*.root",
					"em_dirIso/ntuple",
					lumi,
					"eventWeight*((q_1*q_2)<0.0)",
					"vv",
					nick_suffix=nick_suffix
			)
		elif channel == "mm":
			Sample._add_input(
					config,
					"??_pythia_tauola_8TeV/*.root",
					channel+"_dirIso/ntuple",
					lumi,
					"eventWeight*((q_1*q_2)<0.0)",
					"vv",
					nick_suffix=nick_suffix
			)
		else:
			log.error("Sample config (VV) currently not implemented for channel \"%s\"!" % channel)
		
		Sample._add_plot(config, "bkg", "HIST", "F", "vv", nick_suffix)
		return config
	
	def wj(self, config, channel, category, nick_suffix, lumi=19712.0, **kwargs):
		scale_factor = lumi
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("WJets", 1.0)
		
		if (channel == "et") or (channel == "mt"):
			Sample._add_input(
					config,
					"WJetsToLN_madgraph_8TeV/*.root",
					channel+"_dirIso_z_tauEs/ntuple",
					lumi,
					"eventWeight*((q_1*q_2)<0.0)*(pt_2>30.0)*(lep1MetMt<30.0)",
					"wj",
					nick_suffix=nick_suffix
			)
			Sample._add_input(
					config,
					"Tau*_Run2012?_22Jan2013_8TeV/*.root",
					channel+"_dirIso_z_tauEs/ntuple",
					1.0,
					"eventWeight*((q_1*q_2)<0.0)*(pt_2>30.0)*(lep1MetMt>70.0)",
					"noplot_wj_data_control"
			)
			Sample._add_input(
					config,
					"DYJetsToLL_M_50_madgraph_8TeV/*.root",
					channel+"_dirIso_ztt_tauEsNom/ntuple",
					lumi,
					"eventWeight*((q_1*q_2)<0.0)*(pt_2>30.0)*(lep1MetMt>70.0)",
					"noplot_ztt_mc_wj_control",
					nick_suffix=nick_suffix
			)
			Sample._add_input(
					config,
					"DYJetsToLL_M_50_madgraph_8TeV/*.root",
					channel+"_dirIso_zl_tauEsNom/ntuple "+channel+"_dirIso_zj_tauEsNom/ntuple",
					lumi,
					"eventWeight*((q_1*q_2)<0.0)*(pt_2>30.0)*(lep1MetMt>70.0)",
					"noplot_zll_wj_control",
					nick_suffix=nick_suffix
			)
			Sample._add_input(
					config,
					"TTJets*_madgraph_tauola_8TeV/*.root",
					channel+"_dirIso_z_tauEs/ntuple",
					lumi,
					"eventWeight*((q_1*q_2)<0.0)*(pt_2>30.0)*(lep1MetMt>70.0)",
					"noplot_ttj_wj_control",
					nick_suffix=nick_suffix
			)
			Sample._add_input(
					config,
					"??_pythia_tauola_8TeV/*.root",
					channel+"_dirIso_z_tauEs/ntuple",
					lumi,
					"eventWeight*((q_1*q_2)<0.0)*(pt_2>30.0)*(lep1MetMt>70.0)",
					"noplot_vv_wj_control",
					nick_suffix=nick_suffix
			)
			Sample._add_input(
					config,
					"WJetsToLN_madgraph_8TeV/*.root",
					channel+"_dirIso_z_tauEs/ntuple",
					lumi,
					"eventWeight*((q_1*q_2)<0.0)*(pt_2>30.0)*(lep1MetMt<30.0)",
					"noplot_wj_mc_signal",
					nick_suffix=nick_suffix
			)
			Sample._add_input(
					config,
					"WJetsToLN_madgraph_8TeV/*.root",
					channel+"_dirIso_z_tauEs/ntuple",
					lumi,
					"eventWeight*((q_1*q_2)<0.0)*(pt_2>30.0)*(lep1MetMt>70.0)",
					"noplot_wj_mc_control",
					nick_suffix=nick_suffix
			)
			config.setdefault("analysis_modules", []).append("EstimateWjets")
		elif (channel == "em") or (channel == "mm"):
			Sample._add_input(
					config,
					"WJetsToLN_madgraph_8TeV/*.root",
					channel+"_dirIso/ntuple",
					lumi,
					"eventWeight*((q_1*q_2)<0.0)",
					"wj",
					nick_suffix=nick_suffix
			)
		else:
			log.error("Sample config (WJets) currently not implemented for channel \"%s\"!" % channel)
		
		if not kwargs.get("no_plot", False):
			Sample._add_plot(config, "bkg", "HIST", "F", "wj", nick_suffix)
		return config
	
	def qcd(self, config, channel, category, nick_suffix, lumi=19712.0, **kwargs):
		scale_factor = 1.0
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("QCD", 1.0)
		
		if (channel == "et") or (channel == "mt"):
			Sample._add_input(
					config,
					"WJetsToLN_madgraph_8TeV/*.root",
					channel+"_dirIso_z_tauEs/ntuple",
					lumi,
					"eventWeight*((q_1*q_2)>0.0)*(pt_2>30.0)*(lep1MetMt<30.0)",
					"noplot_wj_ss",
					nick_suffix=nick_suffix
			)
			Sample._add_input(
					config,
					"Tau*_Run2012?_22Jan2013_8TeV/*.root",
					channel+"_dirIso_z_tauEs/ntuple",
					1.0,
					"eventWeight*((q_1*q_2)>0.0)*(pt_2>30.0)*(lep1MetMt>70.0)",
					"noplot_wj_ss_data_control",
					nick_suffix=nick_suffix
			)
			Sample._add_input(
					config,
					"DYJetsToLL_M_50_madgraph_8TeV/*.root",
					channel+"_dirIso_ztt_tauEsNom/ntuple",
					lumi,
					"eventWeight*((q_1*q_2)>0.0)*(pt_2>30.0)*(lep1MetMt>70.0)",
					"noplot_ztt_ss_mc_wj_control",
					nick_suffix=nick_suffix
			)
			Sample._add_input(
					config,
					"DYJetsToLL_M_50_madgraph_8TeV/*.root",
					channel+"_dirIso_zl_tauEsNom/ntuple "+channel+"_dirIso_zj_tauEsNom/ntuple",
					lumi,
					"eventWeight*((q_1*q_2)>0.0)*(pt_2>30.0)*(lep1MetMt>70.0)",
					"noplot_zll_ss_wj_control",
					nick_suffix=nick_suffix
			)
			Sample._add_input(
					config,
					"TTJets*_madgraph_tauola_8TeV/*.root",
					channel+"_dirIso_z_tauEs/ntuple",
					lumi,
					"eventWeight*((q_1*q_2)>0.0)*(pt_2>30.0)*(lep1MetMt>70.0)",
					"noplot_ttj_ss_wj_control",
					nick_suffix=nick_suffix
			)
			Sample._add_input(
					config,
					"??_pythia_tauola_8TeV/*.root",
					channel+"_dirIso_z_tauEs/ntuple",
					lumi,
					"eventWeight*((q_1*q_2)>0.0)*(pt_2>30.0)*(lep1MetMt>70.0)",
					"noplot_vv_ss_wj_control",
					nick_suffix=nick_suffix
			)
			Sample._add_input(
					config,
					"WJetsToLN_madgraph_8TeV/*.root",
					channel+"_dirIso_z_tauEs/ntuple",
					lumi,
					"eventWeight*((q_1*q_2)>0.0)*(pt_2>30.0)*(lep1MetMt<30.0)",
					"noplot_wj_ss_mc_signal",
					nick_suffix=nick_suffix
			)
			Sample._add_input(
					config,
					"WJetsToLN_madgraph_8TeV/*.root",
					channel+"_dirIso_z_tauEs/ntuple",
					lumi,
					"eventWeight*((q_1*q_2)>0.0)*(pt_2>30.0)*(lep1MetMt>70.0)",
					"noplot_wj_ss_mc_control",
					nick_suffix=nick_suffix
			)
		
			# QCD
			Sample._add_input(
					config,
					"Tau*_Run2012?_22Jan2013_8TeV/*.root",
					channel+"_dirIso_z_tauEs/ntuple",
					1.0,
					"eventWeight*((q_1*q_2)>0.0)*(pt_2>30.0)*(lep1MetMt<30.0)",
					"qcd",
					nick_suffix=nick_suffix
			)
			Sample._add_input(
					config,
					"DYJetsToLL_M_50_madgraph_8TeV/*.root",
					channel+"_dirIso_ztt_tauEsNom/ntuple",
					lumi,
					"eventWeight*((q_1*q_2)>0.0)*(pt_2>30.0)*(lep1MetMt<30.0)",
					"noplot_ztt_mc_qcd_control",
					nick_suffix=nick_suffix
			)
			Sample._add_input(
					config,
					"DYJetsToLL_M_50_madgraph_8TeV/*.root",
					channel+"_dirIso_zl_tauEsNom/ntuple "+channel+"_dirIso_zj_tauEsNom/ntuple",
					lumi,
					"eventWeight*((q_1*q_2)>0.0)*(pt_2>30.0)*(lep1MetMt<30.0)",
					"noplot_zll_qcd_control",
					nick_suffix=nick_suffix
			)
			Sample._add_input(
					config,
					"TTJets*_madgraph_tauola_8TeV/*.root",
					channel+"_dirIso_z_tauEs/ntuple",
					lumi,
					"eventWeight*((q_1*q_2)>0.0)*(pt_2>30.0)*(lep1MetMt<30.0)",
					"noplot_ttj_qcd_control",
					nick_suffix=nick_suffix
			)
			Sample._add_input(
					config,
					"??_pythia_tauola_8TeV/*.root",
					channel+"_dirIso_z_tauEs/ntuple",
					lumi,
					"eventWeight*((q_1*q_2)>0.0)*(pt_2>30.0)*(lep1MetMt<30.0)",
					"noplot_vv_qcd_control",
					nick_suffix=nick_suffix
			)
			config.setdefault("analysis_modules", []).append("EstimateQcd")
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
		elif channel == "mm":
			Sample._add_input(
					config,
					"DoubleMu*_Run2012?_22Jan2013_8TeV/*.root",
					"mm_dirIso/ntuple",
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
	
	def qcdwj(self, config, channel, category, nick_suffix, lumi=19712.0, **kwargs):
		config = self.qcd(config, channel, category, nick_suffix+"_noplot", lumi, no_plot=True, **kwargs)
		config = self.wj(config, channel, category, nick_suffix+"_noplot", lumi, no_plot=True, **kwargs)
		if not "AddHistograms" in config.get("analysis_modules", []):
			config.setdefault("analysis_modules", []).append("AddHistograms")
		config.setdefault("histogram_nicks", []).append(" ".join([sample+nick_suffix+"_noplot" for sample in ["qcd", "wj"]]))
		config.setdefault("sum_result_nicks", []).append("qcdwj"+nick_suffix)
		
		Sample._add_plot(config, "bkg", "HIST", "F", "qcdwj", nick_suffix)
		return config
	
	def htt(self, config, channel, category, nick_suffix, higgs_masses, normalise_signal_to_one_pb=False, lumi=19712.0, **kwargs):
		config = self.ggh(config, channel, category, nick_suffix+"_noplot", higgs_masses, normalise_signal_to_one_pb, lumi, no_plot=True, **kwargs)
		config = self.qqh(config, channel, category, nick_suffix+"_noplot", higgs_masses, normalise_signal_to_one_pb, lumi, no_plot=True, **kwargs)
		config = self.vh(config, channel, category, nick_suffix+"_noplot", higgs_masses, normalise_signal_to_one_pb, lumi, no_plot=True, **kwargs)
		
		for mass in higgs_masses:
			if not "AddHistograms" in config.get("analysis_modules", []):
				config.setdefault("analysis_modules", []).append("AddHistograms")
			config.setdefault("histogram_nicks", []).append(" ".join([sample+str(mass)+nick_suffix+"_noplot" for sample in ["ggh", "qqh", "vh"]]))
			config.setdefault("sum_result_nicks", []).append("htt"+str(mass)+nick_suffix)
			
			Sample._add_plot(config, "sig", "LINE", "L", "htt"+str(mass), nick_suffix)
		return config
	
	def ggh(self, config, channel, category, nick_suffix, higgs_masses, normalise_signal_to_one_pb=False, lumi=19712.0, **kwargs):
		scale_factor = lumi
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("ggH", 1.0)
		
		for mass in higgs_masses:
			if (channel == "et") or (channel == "mt") or (channel == "em") or (channel == "mm"):
				Sample._add_input(
						config,
						"SM_GluGluToHToTauTau_M_{mass}_powheg_pythia_8TeV/*.root".format(mass=str(mass)),
						channel+"_dirIso/ntuple" if (channel == "em") or (channel == "mm") else channel+"_dirIso_z_tauEsNom/ntuple",
						lumi,
						"eventWeight*((q_1*q_2)<0.0)" + ("" if (channel == "em") or (channel == "mm") else "*(pt_2>30.0)*(lep1MetMt<30.0)") + ("/crossSectionPerEventWeight" if normalise_signal_to_one_pb else ""),
						"ggH%s" % str(mass),
						nick_suffix=nick_suffix
				)
			else:
				log.error("Sample config (ggH%s) currently not implemented for channel \"%s\"!" % (str(mass), channel))
			
			if not kwargs.get("no_plot", False):
				Sample._add_plot(config, "sig", "LINE", "L", "htt"+str(mass), nick_suffix)
		return config
	
	def qqh(self, config, channel, category, nick_suffix, higgs_masses, normalise_signal_to_one_pb=False, lumi=19712.0, **kwargs):
		scale_factor = lumi
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("qqH", 1.0)
		
		for mass in higgs_masses:
			if (channel == "et") or (channel == "mt") or (channel == "em") or (channel == "mm"):
				Sample._add_input(
						config,
						"SM_VBFHToTauTau_M_{mass}_powheg_pythia_8TeV/*.root".format(mass=str(mass)),
						channel+"_dirIso/ntuple" if (channel == "em") or (channel == "mm") else channel+"_dirIso_z_tauEsNom/ntuple",
						lumi,
						"eventWeight*((q_1*q_2)<0.0)" + ("" if (channel == "em") or (channel == "mm") else "*(pt_2>30.0)*(lep1MetMt<30.0)") + ("/crossSectionPerEventWeight" if normalise_signal_to_one_pb else ""),
						"VBF%s" % str(mass),
						nick_suffix=nick_suffix
			)
			else:
				log.error("Sample config (VBF%s) currently not implemented for channel \"%s\"!" % (str(mass), channel))
			
			if not kwargs.get("no_plot", False):
				Sample._add_plot(config, "sig", "LINE", "L", "htt"+str(mass), nick_suffix)
		return config
	
	def vh(self, config, channel, category, nick_suffix, higgs_masses, normalise_signal_to_one_pb=False, lumi=19712.0, **kwargs):
		scale_factor = lumi
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("VH", 1.0)
		
		for mass in higgs_masses:
			if (channel == "et") or (channel == "mt") or (channel == "em") or (channel == "mm"):
				Sample._add_input(
						config,
						"SM_WH_ZH_TTH_HToTauTau_M_{mass}_powheg_pythia_8TeV/*.root".format(mass=str(mass)),
						channel+"_dirIso/ntuple" if (channel == "em") or (channel == "mm") else channel+"_dirIso_z_tauEsNom/ntuple",
						lumi / 2.0,
						"eventWeight*((q_1*q_2)<0.0)" + ("" if (channel == "em") or (channel == "mm") else "*(pt_2>30.0)*(lep1MetMt<30.0)") + ("/crossSectionPerEventWeight" if normalise_signal_to_one_pb else ""),
						"WH%s" % str(mass),
						nick_suffix=nick_suffix
				)
				Sample._add_input(
						config,
						"SM_WH_ZH_TTH_HToTauTau_M_{mass}_powheg_pythia_8TeV/*.root".format(mass=str(mass)),
						"em_dirIso/ntuple" if (channel == "em") or (channel == "mm") else channel+"_dirIso_z_tauEsNom/ntuple",
						lumi / 2.0,
						"eventWeight*((q_1*q_2)<0.0)" + ("" if (channel == "em") or (channel == "mm") else "*(pt_2>30.0)*(lep1MetMt<30.0)") + ("/crossSectionPerEventWeight" if normalise_signal_to_one_pb else ""),
						"ZH%s" % str(mass),
						nick_suffix=nick_suffix
				)
			else:
				log.error("Sample config (VH%s) currently not implemented for channel \"%s\"!" % (str(mass), channel))
			
			if not kwargs.get("no_plot", False):
				Sample._add_plot(config, "sig", "LINE", "L", "htt"+str(mass), nick_suffix)
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

