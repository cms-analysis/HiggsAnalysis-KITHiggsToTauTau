
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import copy

import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.samples as samples


class Samples(samples.SamplesBase):

	@staticmethod
	def cut_string(channel, exclude_cuts=None):
		if exclude_cuts is None:
			exclude_cuts = []
		
		cuts = {}
		cuts["os"] = "((q_1*q_2)<0.0)"
		cuts["nobtag"] = "((nBJets30<1)||(nJets30<1))"
		
		if channel == "mt":
			cuts["mt"] = "(mt_1<30.0)"
			cuts["pt2"] = "(pt_2>30.0)"
		elif channel == "et":
			cuts["mt"] = "(mt_1<30.0)"
			cuts["pt2"] = "(pt_2>30.0)"
		elif channel == "em":
			cuts["pzeta"] = "(pZetaMissVis > -20.0)"
		elif channel == "tt":
			pass
		elif channel == "mm":
			pass
		elif channel == "ee":
			pass
		else:
			log.fatal("No cut values implemented for channel \"%s\"!" % channel)
			sys.exit(1)
		
		cuts_list = [cut for (name, cut) in cuts.iteritems() if not name in exclude_cuts]
		if len(cuts_list) == 0:
			cuts_list.append("1.0")
		
		return "*".join(cuts_list)

	def __init__(self):
		super(Samples, self).__init__()
		
		self.period = "run1"
	
	def data(self, config, channel, category, weight, nick_suffix, exclude_cuts=None, **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []
		
		scale_factor = 1.0
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("data_obs", 1.0)
		
		if channel == "tt":
			Samples._add_input(
					config,
					"Tau*_Run2012?_22Jan2013_8TeV/*.root",
					"tt_dirIso_jecUncNom_tauEs/ntuple",
					1.0,
					weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts),
					"data",
					nick_suffix=nick_suffix
			)
		elif channel in ["et", "mt"]:
			Samples._add_input(
					config,
					"Tau*_Run2012?_22Jan2013_8TeV/*.root",
					channel+"_dirIso_z_jecUncNom_tauEs/ntuple",
					1.0,
					weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts),
					"data",
					nick_suffix=nick_suffix
			)
		elif channel == "em":
			Samples._add_input(
					config,
					"MuEG_Run2012?_22Jan2013_8TeV/*.root",
					"em_dirIso_jecUnc/ntuple",
					1.0,
					weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts),
					"data",
					nick_suffix=nick_suffix
			)
		elif channel == "mm":
			Samples._add_input(
					config,
					"DoubleMu*_Run2012?_22Jan2013_8TeV/*.root",
					"mm_dirIso_jecUnc/ntuple",
					1.0,
					weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts),
					"data",
					nick_suffix=nick_suffix
			)
		else:
			log.error("Sample config (Data) currently not implemented for channel \"%s\"!" % channel)
		
		Samples._add_plot(config, "data", "E", "ELP", "data", nick_suffix)
		return config
	
	def ztt(self, config, channel, category, weight, nick_suffix, lumi=19712.0, ztt_from_mc=False, exclude_cuts=None, **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []
		
		scale_factor = 1.0
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("ZTT", 1.0)
		
		if channel in ["tt", "et", "mt", "em", "mm"]:
			if ztt_from_mc:
				Samples._add_input(
						config,
						"DYJetsToLL_M_50_madgraph_8TeV/*.root",
						channel+"_dirIso" + ("_tt" if channel in ["tt", "em", "mm"] else "_ztt") + "_jecUncNom" + ("_tauEsNom" if channel in ["tt", "et", "mt"] else "") + "/ntuple",
						lumi,
						weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts),
						"ztt",
						nick_suffix=nick_suffix
				)
			else:
				Samples._add_input(
						config,
						"*_PFembedded_Run2012?_22Jan2013_"+channel+"_8TeV/*.root",
						channel+"_dirIso" + ("_z" if channel in ["et", "mt"] else "") + "_jecUncNom" + ("_tauEs" if channel in ["tt", "et", "mt"] else "") + "/ntuple",
						1.0,
						weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts),
						"ztt",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						"*_PFembedded_Run2012?_22Jan2013_"+channel+"_8TeV/*.root",
						channel+"_dirIso" + ("_z" if channel in ["et", "mt"] else "") + "_jecUncNom" + ("_tauEs" if channel in ["tt", "et", "mt"] else "") + "/ntuple",
						1.0,
						weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts),
						"noplot_ztt_emb_inc",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						"DYJetsToLL_M_50_madgraph_8TeV/*.root",
						channel+"_dirIso" + ("_tt" if channel in ["tt", "em", "mm"] else "_ztt") + "_jecUncNom" + ("_tauEs" if channel in ["tt", "et", "mt"] else "") + "/ntuple",
						lumi,
						weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts),
						"noplot_ztt_mc_inc",
						nick_suffix=nick_suffix
				)
			
			if not "EstimateZtt" in config.get("analysis_modules", []):
				config.setdefault("analysis_modules", []).append("EstimateZtt")
			config.setdefault("ztt_from_mc", []).append(ztt_from_mc)
			config.setdefault("ztt_plot_nicks", []).append("ztt"+nick_suffix)
			config.setdefault("ztt_mc_inc_nicks", []).append("noplot_ztt_mc_inc"+nick_suffix)
			config.setdefault("ztt_emb_inc_nicks", []).append("noplot_ztt_emb_inc"+nick_suffix)
			
		else:
			log.error("Sample config (ZTT) currently not implemented for channel \"%s\"!" % channel)
		
		Samples._add_plot(config, "bkg", "HIST", "F", "ztt", nick_suffix)
		
		return config
	
	def zl(self, config, channel, category, weight, nick_suffix, lumi=19712.0, exclude_cuts=None, **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []
		
		scale_factor = lumi
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("ZL", 1.0)
		
		if channel in ["tt", "et", "mt", "em", "mm"]:
			Samples._add_input(
					config,
					"DYJetsToLL_M_50_madgraph_8TeV/*.root",
					(channel+"_dirIso_ee_jecUncNom" + ("_tauEsNom" if channel == "tt" else "") + "/ntuple "+channel+"_dirIso_mm_jecUncNom" + ("_tauEsNom" if channel == "tt" else "") + "/ntuple") if channel in ["tt", "em", "mm"] else channel+"_dirIso_zl_jecUncNom_tauEsNom/ntuple",
					lumi,
					weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts),
					"zl",
					nick_suffix=nick_suffix
			)
		else:
			log.error("Sample config (ZL) currently not implemented for channel \"%s\"!" % channel)
		
		Samples._add_plot(config, "bkg", "HIST", "F", "zl", nick_suffix)
		return config
	
	def zj(self, config, channel, category, weight, nick_suffix, lumi=19712.0, exclude_cuts=None, **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []
		
		scale_factor = lumi
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("ZJ", 1.0)
		
		if channel in ["et", "mt"]:
			Samples._add_input(
					config,
					"DYJetsToLL_M_50_madgraph_8TeV/*.root",
					channel+"_dirIso_zj_jecUncNom_tauEsNom/ntuple",
					lumi,
					weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts),
					"zj"
			)
			
			Samples._add_plot(config, "bkg", "HIST", "F", "zj", nick_suffix)
		elif channel in ["tt", "em", "mm"]:
			pass
		else:
			log.error("Sample config (ZJ) currently not implemented for channel \"%s\"!" % channel)
		
		return config
	
	def ttj(self, config, channel, category, weight, nick_suffix, lumi=19712.0, exclude_cuts=None, **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []
		
		scale_factor = lumi
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("TTJ", 1.0)
		
		if channel in ["et", "mt"]:
			Samples._add_input(
					config,
					"TTJets*_madgraph_tauola_8TeV/*.root",
					channel+"_dirIso_z_jecUncNom_tauEs/ntuple",
					lumi,
					weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts),
					"ttj",
					nick_suffix=nick_suffix
			)
		elif channel == "em":
			Samples._add_input(
					config,
					"TTJetsTo*_madgraph_tauola_8TeV/*.root",
					"em_dirIso_jecUncNom/ntuple",
					lumi,
					weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts),
					"ttj",
					nick_suffix=nick_suffix
			)
			Samples._add_input(
					config,
					"T*_powheg_tauola_8TeV/*.root",
					"em_dirIso_jecUncNom/ntuple",
					lumi,
					weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts),
					"ttj",
					nick_suffix=nick_suffix
			)
			
			Samples._add_input(
					config,
					"MuEG_Run2012?_22Jan2013_8TeV/*.root",
					"em_dirIso_jecUnc/ntuple",
					1.0,
					"eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["pzeta", "nobtag"]) + "*(pZetaMissVis < -20.0)",
					"noplot_ttj_data_control"
			)
			Samples._add_input(
					config,
					"DYJetsToLL_M_50_madgraph_8TeV/*.root",
					channel+"_dirIso_tt_jecUncNom/ntuple",
					lumi,
					"eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["pzeta", "nobtag"]) + "*(pZetaMissVis < -20.0)",
					"noplot_ztt_mc_ttj_control",
					nick_suffix=nick_suffix
			)
			Samples._add_input(
					config,
					"DYJetsToLL_M_50_madgraph_8TeV/*.root",
					channel+"_dirIso_ee_jecUncNom/ntuple "+channel+"_dirIso_mm_jecUncNom/ntuple",
					lumi,
					"eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["pzeta", "nobtag"]) + "*(pZetaMissVis < -20.0)",
					"noplot_zll_ttj_control",
					nick_suffix=nick_suffix
			)
			Samples._add_input(
					config,
					"WJetsToLN_madgraph_8TeV/*.root",
					channel+"_dirIso_jecUncNom/ntuple",
					lumi,
					"eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["pzeta", "nobtag"]) + "*(pZetaMissVis < -20.0)",
					"noplot_wj_ttj_control",
					nick_suffix=nick_suffix
			)
			Samples._add_input(
					config,
					"??JetsToLL??*_madgraph_tauola_8TeV/*.root",
					channel+"_dirIso_jecUncNom/ntuple",
					lumi,
					"eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["pzeta", "nobtag"]) + "*(pZetaMissVis < -20.0)",
					"noplot_vv_ttj_control",
					nick_suffix=nick_suffix
			)
			Samples._add_input(
					config,
					"TTJetsTo*_madgraph_tauola_8TeV/*.root",
					"em_dirIso_jecUncNom/ntuple",
					lumi,
					weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind"]),
					"noplot_ttj_mc_signal",
					nick_suffix=nick_suffix
			)
			Samples._add_input(
					config,
					"T*_powheg_tauola_8TeV/*.root",
					"em_dirIso_jecUncNom/ntuple",
					lumi,
					weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind"]),
					"noplot_ttj_mc_signal",
					nick_suffix=nick_suffix
			)
			Samples._add_input(
					config,
					"TTJetsTo*_madgraph_tauola_8TeV/*.root",
					"em_dirIso_jecUncNom/ntuple",
					lumi,
					"eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["pzeta", "nobtag"]) + "*(pZetaMissVis < -20.0)",
					"noplot_ttj_mc_control",
					nick_suffix=nick_suffix
			)
			Samples._add_input(
					config,
					"T*_powheg_tauola_8TeV/*.root",
					"em_dirIso_jecUncNom/ntuple",
					lumi,
					"eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["pzeta", "nobtag"]) + "*(pZetaMissVis < -20.0)",
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
			
		elif channel in ["tt", "mm"]:
			Samples._add_input(
					config,
					"TTJetsTo*_madgraph_tauola_8TeV/*.root",
					channel+"_dirIso" + ("_jecUncNom_tauEs" if channel == "tt" else "") + "/ntuple",
					lumi,
					weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts),
					"ttj",
					nick_suffix=nick_suffix
			)
		else:
			log.error("Sample config (TTJ) currently not implemented for channel \"%s\"!" % channel)
		
		Samples._add_plot(config, "bkg", "HIST", "F", "ttj", nick_suffix)
		return config
	
	def vv(self, config, channel, category, weight, nick_suffix, lumi=19712.0, exclude_cuts=None, **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []
		
		scale_factor = lumi
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("Dibosons", 1.0)
		
		if channel in ["tt", "et", "mt", "em"]:
			Samples._add_input(
					config,
					"??JetsToLL??*_madgraph_tauola_8TeV/*.root",
					channel+"_dirIso" + ("_z" if channel in ["et", "mt"] else "") + "_jecUncNom" + ("_tauEs" if channel in ["tt", "et", "mt"] else "") + "/ntuple",
					lumi,
					weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts),
					"vv",
					nick_suffix=nick_suffix
			)
		elif channel == "mm":
			Samples._add_input(
					config,
					"??_pythia_tauola_8TeV/*.root",
					channel+"_dirIso_jecUncNom/ntuple",
					lumi,
					weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts),
					"vv",
					nick_suffix=nick_suffix
			)
		else:
			log.error("Sample config (VV) currently not implemented for channel \"%s\"!" % channel)
		
		Samples._add_plot(config, "bkg", "HIST", "F", "vv", nick_suffix)
		return config
	
	def wj(self, config, channel, category, weight, nick_suffix, lumi=19712.0, exclude_cuts=None, **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []
		
		scale_factor = lumi
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("WJets", 1.0)
		
		if channel == "tt":
			Samples._add_input(
					config,
					"WJetsToLN_madgraph_8TeV/*.root",
					"tt_dirIso_jecUncNom_tauEs/ntuple",
					lumi,
					weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts),
					"wj",
					nick_suffix=nick_suffix
			)
		elif channel in ["et", "mt"]:
			Samples._add_input(
					config,
					"WJetsToLN_madgraph_8TeV/*.root",
					channel+"_dirIso_z_jecUncNom_tauEs/ntuple",
					lumi,
					"eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts),
					"wj",
					nick_suffix=nick_suffix
			)
			Samples._add_input(
					config,
					"Tau*_Run2012?_22Jan2013_8TeV/*.root",
					channel+"_dirIso_z_jecUncNom_tauEs/ntuple",
					1.0,
					"eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["mt"]) + "*(lep1MetMt>70.0)",
					"noplot_wj_data_control"
			)
			Samples._add_input(
					config,
					"DYJetsToLL_M_50_madgraph_8TeV/*.root",
					channel+"_dirIso_ztt_jecUncNom_tauEsNom/ntuple",
					lumi,
					"eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["mt"]) + "*(lep1MetMt>70.0)",
					"noplot_ztt_mc_wj_control",
					nick_suffix=nick_suffix
			)
			Samples._add_input(
					config,
					"DYJetsToLL_M_50_madgraph_8TeV/*.root",
					channel+"_dirIso_zl_jecUncNom_tauEsNom/ntuple "+channel+"_dirIso_zj_jecUncNom_tauEsNom/ntuple",
					lumi,
					"eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["mt"]) + "*(lep1MetMt>70.0)",
					"noplot_zll_wj_control",
					nick_suffix=nick_suffix
			)
			Samples._add_input(
					config,
					"TTJets*_madgraph_tauola_8TeV/*.root",
					channel+"_dirIso_z_jecUncNom_tauEs/ntuple",
					lumi,
					"eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["mt"]) + "*(lep1MetMt>70.0)",
					"noplot_ttj_wj_control",
					nick_suffix=nick_suffix
			)
			Samples._add_input(
					config,
					"??JetsToLL??*_madgraph_tauola_8TeV/*.root",
					channel+"_dirIso_z_jecUncNom_tauEs/ntuple",
					lumi,
					"eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["mt"]) + "*(lep1MetMt>70.0)",
					"noplot_vv_wj_control",
					nick_suffix=nick_suffix
			)
			Samples._add_input(
					config,
					"WJetsToLN_madgraph_8TeV/*.root",
					channel+"_dirIso_z_jecUncNom_tauEs/ntuple",
					lumi,
					weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts),
					"noplot_wj_mc_signal",
					nick_suffix=nick_suffix
			)
			Samples._add_input(
					config,
					"WJetsToLN_madgraph_8TeV/*.root",
					channel+"_dirIso_z_jecUncNom_tauEs/ntuple",
					lumi,
					"eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["mt"]) + "*(lep1MetMt>70.0)",
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
			
		elif channel in ["em", "mm"]:
			Samples._add_input(
					config,
					"WJetsToLN_madgraph_8TeV/*.root",
					channel+"_dirIso_jecUncNom/ntuple",
					lumi,
					weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts),
					"wj",
					nick_suffix=nick_suffix
			)
		else:
			log.error("Sample config (WJets) currently not implemented for channel \"%s\"!" % channel)
		
		if not kwargs.get("no_plot", False):
			Samples._add_plot(config, "bkg", "HIST", "F", "wj", nick_suffix)
		return config
	
	def qcd(self, config, channel, category, weight, nick_suffix, lumi=19712.0, exclude_cuts=None, **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []
		
		scale_factor = 1.0
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("QCD", 1.0)
		
		if channel == "tt":
			Samples._add_input(
					config,
					"Tau*_Run2012?_22Jan2013_8TeV/*.root",
					"tt_dirIso_jecUncNom_tauEs/ntuple",
					1.0,
					weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["os"]) + "*((q_1*q_2)>0.0)",
					"qcd",
					nick_suffix=nick_suffix
			)
			Samples._add_input(
					config,
					"DYJetsToLL_M_50_madgraph_8TeV/*.root",
					"tt_dirIso_tt_jecUncNom_tauEsNom/ntuple",
					-lumi,
					weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["os"]) + "*((q_1*q_2)>0.0)",
					"qcd",
					nick_suffix=nick_suffix
			)
			Samples._add_input(
					config,
					"DYJetsToLL_M_50_madgraph_8TeV/*.root",
					"tt_dirIso_ee_jecUncNom_tauEsNom/ntuple tt_dirIso_mm_jecUncNom_tauEsNom/ntuple",
					-lumi,
					weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["os"]) + "*((q_1*q_2)>0.0)",
					"qcd",
					nick_suffix=nick_suffix
			)
			Samples._add_input(
					config,
					"TTJets*_madgraph_tauola_8TeV/*.root",
					"tt_dirIso_jecUncNom_tauEs/ntuple",
					-lumi,
					weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["os"]) + "*((q_1*q_2)>0.0)",
					"qcd",
					nick_suffix=nick_suffix
			)
			Samples._add_input(
					config,
					"??JetsToLL??*_madgraph_tauola_8TeV/*.root",
					"tt_dirIso_jecUncNom_tauEs/ntuple",
					-lumi,
					weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["os"]) + "*((q_1*q_2)>0.0)",
					"qcd",
					nick_suffix=nick_suffix
			)
			Samples._add_input(
					config,
					"WJetsToLN_madgraph_8TeV/*.root",
					"tt_dirIso_jecUncNom_tauEs/ntuple",
					-lumi,
					weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["os"]) + "*((q_1*q_2)>0.0)",
					"qcd",
					nick_suffix=nick_suffix
			)

		elif channel in ["et", "mt", "em"]:
			Samples._add_input(
					config,
					"WJetsToLN_madgraph_8TeV/*.root",
					channel+"_dirIso" + ("_z" if channel in ["et", "mt"] else "") + "_jecUncNom" + ("_tauEs" if channel in ["et", "mt"] else "") + "/ntuple",
					lumi,
					"eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["os"]) + "*((q_1*q_2)>0.0)",
					"noplot_wj_ss",
					nick_suffix=nick_suffix
			)
			
			if channel in ["et", "mt"]:
				Samples._add_input(
						config,
						"Tau*_Run2012?_22Jan2013_8TeV/*.root",
						channel+"_dirIso_z_jecUncNom_tauEs/ntuple",
						1.0,
						"eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["os", "mt"]) + "*((q_1*q_2)>0.0)*(lep1MetMt>70.0)",
						"noplot_wj_ss_data_control",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						"DYJetsToLL_M_50_madgraph_8TeV/*.root",
						channel+"_dirIso_ztt_jecUncNom_tauEsNom/ntuple",
						lumi,
						"eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["os", "mt"]) + "*((q_1*q_2)>0.0)*(lep1MetMt>70.0)",
						"noplot_ztt_ss_mc_wj_control",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						"DYJetsToLL_M_50_madgraph_8TeV/*.root",
						channel+"_dirIso_zl_jecUncNom_tauEsNom/ntuple "+channel+"_dirIso_zj_jecUncNom_tauEsNom/ntuple",
						lumi,
						"eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["os", "mt"]) + "*((q_1*q_2)>0.0)*(lep1MetMt>70.0)",
						"noplot_zll_ss_wj_control",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						"TTJets*_madgraph_tauola_8TeV/*.root",
						channel+"_dirIso_z_jecUncNom_tauEs/ntuple",
						lumi,
						"eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["os", "mt"]) + "*((q_1*q_2)>0.0)*(lep1MetMt>70.0)",
						"noplot_ttj_ss_wj_control",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						"??JetsToLL??*_madgraph_tauola_8TeV/*.root",
						channel+"_dirIso_z_jecUncNom_tauEs/ntuple",
						lumi,
						"eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["os", "mt"]) + "*((q_1*q_2)>0.0)*(lep1MetMt>70.0)",
						"noplot_vv_ss_wj_control",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						"WJetsToLN_madgraph_8TeV/*.root",
						channel+"_dirIso_z_jecUncNom_tauEs/ntuple",
						lumi,
						"eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["os"]) + "*((q_1*q_2)>0.0)",
						"noplot_wj_ss_mc_signal",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						"WJetsToLN_madgraph_8TeV/*.root",
						channel+"_dirIso_z_jecUncNom_tauEs/ntuple",
						lumi,
						"eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["os", "mt"]) + "*((q_1*q_2)>0.0)*(lep1MetMt>70.0)",
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
			if channel in ["et", "mt"]:
				Samples._add_input(
						config,
						"Tau*_Run2012?_22Jan2013_8TeV/*.root",
						channel+"_dirIso" + ("_z" if channel in ["et", "mt"] else "") + "_jecUncNom" + ("_tauEs" if channel in ["et", "mt"] else "") + "/ntuple",
						1.0,
						weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["os"]) + "*((q_1*q_2)>0.0)",
						"qcd",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						"Tau*_Run2012?_22Jan2013_8TeV/*.root",
						channel+"_dirIso" + ("_z" if channel in ["et", "mt"] else "") + "_jecUncNom" + ("_tauEs" if channel in ["et", "mt"] else "") + "/ntuple",
						1.0,
						weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["os"]) + "*((q_1*q_2)>0.0)",
						"noplot_data_qcd_yield",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						"Tau*_Run2012?_22Jan2013_8TeV/*.root",
						channel+"_dirIso" + ("_z" if channel in ["et", "mt"] else "") + "_jecUncNom" + ("_tauEs" if channel in ["et", "mt"] else "") + "/ntuple",
						1.0,
						"eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["os"]) + "*((q_1*q_2)>0.0)",
						"noplot_data_qcd_control",
						nick_suffix=nick_suffix
				)
			else:
				Samples._add_input(
						config,
						"MuEG_Run2012?_22Jan2013_8TeV/*.root",
						"em_dirIso_jecUnc/ntuple",
						1.0,
						weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["os"]) + "*((q_1*q_2)>0.0)",
						"qcd",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						"MuEG_Run2012?_22Jan2013_8TeV/*.root",
						"em_dirIso_jecUnc/ntuple",
						1.0,
						weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["os"]) + "*((q_1*q_2)>0.0)",
						"noplot_data_qcd_yield",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						"MuEG_Run2012?_22Jan2013_8TeV/*.root",
						"em_dirIso_jecUnc/ntuple",
						1.0,
						"eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["os"]) + "*((q_1*q_2)>0.0)",
						"noplot_data_qcd_control",
						nick_suffix=nick_suffix
				)
			
			Samples._add_input(
					config,
					"DYJetsToLL_M_50_madgraph_8TeV/*.root",
					(channel+"_dirIso_tt_jecUncNom/ntuple") if channel == "em" else (channel+"_dirIso_ztt_jecUncNom_tauEsNom/ntuple"),
					lumi,
					"eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["os"]) + "*((q_1*q_2)>0.0)",
					"noplot_ztt_mc_qcd_control",
					nick_suffix=nick_suffix
			)
			Samples._add_input(
					config,
					"DYJetsToLL_M_50_madgraph_8TeV/*.root",
					(channel+"_dirIso_ee_jecUncNom/ntuple "+channel+"_dirIso_mm_jecUncNom/ntuple") if channel == "em" else (channel+"_dirIso_zl_jecUncNom_tauEsNom/ntuple "+channel+"_dirIso_zj_jecUncNom_tauEsNom/ntuple"),
					lumi,
					"eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["os"]) + "*((q_1*q_2)>0.0)",
					"noplot_zll_qcd_control",
					nick_suffix=nick_suffix
			)
			Samples._add_input(
					config,
					"TTJets*_madgraph_tauola_8TeV/*.root",
					channel+"_dirIso" + ("_z" if channel in ["et", "mt"] else "") + "_jecUncNom" + ("_tauEs" if channel in ["et", "mt"] else "") + "/ntuple",
					lumi,
					"eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["os"]) + "*((q_1*q_2)>0.0)",
					"noplot_ttj_qcd_control",
					nick_suffix=nick_suffix
			)
			Samples._add_input(
					config,
					"??JetsToLL??*_madgraph_tauola_8TeV/*.root",
					channel+"_dirIso" + ("_z" if channel in ["et", "mt"] else "") + "_jecUncNom" + ("_tauEs" if channel in ["et", "mt"] else "") + "/ntuple",
					lumi,
					"eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["os"]) + "*((q_1*q_2)>0.0)",
					"noplot_vv_qcd_control",
					nick_suffix=nick_suffix
			)
			
			if not "EstimateQcd" in config.get("analysis_modules", []):
				config.setdefault("analysis_modules", []).append("EstimateQcd")
			config.setdefault("qcd_data_shape_nicks", []).append("qcd"+nick_suffix)
			config.setdefault("qcd_data_yield_nicks", []).append("noplot_data_qcd_yield"+nick_suffix)
			config.setdefault("qcd_data_control_nicks", []).append("noplot_data_qcd_control"+nick_suffix)
			config.setdefault("qcd_data_substract_nicks", []).append(" ".join([nick+nick_suffix for nick in "noplot_ztt_mc_qcd_control noplot_zll_qcd_control noplot_ttj_qcd_control noplot_vv_qcd_control noplot_wj_ss".split()]))
			config.setdefault("qcd_extrapolation_factors_ss_os", []).append(1.06 + (0.0 if not "os" in exclude_cuts else 1.0))
			config.setdefault("qcd_subtract_shape", []).append(False) # True currently not supported
			
		elif channel == "em":
			Samples._add_input(
					config,
					"MuEG_Run2012?_22Jan2013_8TeV/*.root",
					"em_dirIso_jecUnc/ntuple",
					1.0,
					weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["os"]) + "*((q_1*q_2)>0.0)",
					"qcd",
					nick_suffix=nick_suffix
			)
		elif channel == "mm":
			Samples._add_input(
					config,
					"DoubleMu*_Run2012?_22Jan2013_8TeV/*.root",
					"mm_dirIso_jecUnc/ntuple",
					1.0,
					weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["os"]) + "*((q_1*q_2)>0.0)",
					"qcd",
					nick_suffix=nick_suffix
			)
		else:
			log.error("Sample config (QCD) currently not implemented for channel \"%s\"!" % channel)
		
		if not kwargs.get("no_plot", False):
			Samples._add_plot(config, "bkg", "HIST", "F", "qcd", nick_suffix)
		return config
	
	def qcdwj(self, config, channel, category, weight, nick_suffix, lumi=19712.0, exclude_cuts=None, **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []
		
		config = self.qcd(config, channel, category, weight, nick_suffix+"_noplot", lumi, exclude_cuts=exclude_cuts, no_plot=True, **kwargs)
		config = self.wj(config, channel, category, weight, nick_suffix+"_noplot", lumi, exclude_cuts=exclude_cuts, no_plot=True, **kwargs)
		if not "AddHistograms" in config.get("analysis_modules", []):
			config.setdefault("analysis_modules", []).append("AddHistograms")
		config.setdefault("histogram_nicks", []).append(" ".join([sample+nick_suffix+"_noplot" for sample in ["qcd", "wj"]]))
		config.setdefault("sum_result_nicks", []).append("qcdwj"+nick_suffix)
		
		Samples._add_plot(config, "bkg", "HIST", "F", "qcdwj", nick_suffix)
		return config
	
	def htt(self, config, channel, category, weight, nick_suffix, higgs_masses, normalise_signal_to_one_pb=False, lumi=19712.0, exclude_cuts=None, **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []
		
		config = self.ggh(config, channel, category, weight, nick_suffix+"_noplot", higgs_masses,
		                  normalise_signal_to_one_pb, lumi, exclude_cuts=exclude_cuts, no_plot=True, **kwargs)
		config = self.qqh(config, channel, category, weight, nick_suffix+"_noplot", higgs_masses,
		                  normalise_signal_to_one_pb, lumi, exclude_cuts=exclude_cuts, no_plot=True, **kwargs)
		config = self.vh(config, channel, category, weight, nick_suffix+"_noplot", higgs_masses,
		                 normalise_signal_to_one_pb, lumi, exclude_cuts=exclude_cuts, no_plot=True, **kwargs)
		
		for mass in higgs_masses:
			if not "AddHistograms" in config.get("analysis_modules", []):
				config.setdefault("analysis_modules", []).append("AddHistograms")
			config.setdefault("histogram_nicks", []).append(" ".join([sample+str(mass)+nick_suffix+"_noplot" for sample in ["ggh", "qqh", "wh", "zh"]]))
			config.setdefault("sum_result_nicks", []).append("htt"+str(mass)+nick_suffix)
			
			Samples._add_plot(config, "sig", "LINE", "L", "htt"+str(mass), nick_suffix)
		return config
	
	def ggh(self, config, channel, category, weight, nick_suffix, higgs_masses, normalise_signal_to_one_pb=False, lumi=19712.0, exclude_cuts=None, **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []
		
		scale_factor = lumi
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("ggH", 1.0)
		
		for mass in higgs_masses:
			if channel in ["tt", "et", "mt", "em", "mm"]:
				Samples._add_input(
						config,
						"SM_GluGluToHToTauTau_M_{mass}_powheg_pythia_8TeV/*.root".format(mass=str(mass)),
						channel+"_dirIso" + ("_z" if channel in ["et", "mt"] else "") + "_jecUncNom" + ("_tauEsNom" if channel in ["tt", "et", "mt"] else "") + "/ntuple",
						lumi,
						weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts) + ("/crossSectionPerEventWeight" if normalise_signal_to_one_pb else ""),
						"ggh%s" % str(mass),
						nick_suffix=nick_suffix
				)
			else:
				log.error("Sample config (ggH%s) currently not implemented for channel \"%s\"!" % (str(mass), channel))
			
			if not kwargs.get("no_plot", False):
				Samples._add_plot(config, "sig", "LINE", "L", "ggh"+str(mass), nick_suffix)
		return config
	
	def qqh(self, config, channel, category, weight, nick_suffix, higgs_masses, normalise_signal_to_one_pb=False, lumi=19712.0, exclude_cuts=None, **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []
		
		scale_factor = lumi
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("qqH", 1.0)
		
		for mass in higgs_masses:
			if channel in ["tt", "et", "mt", "em", "mm"]:
				Samples._add_input(
						config,
						"SM_VBFHToTauTau_M_{mass}_powheg_pythia_8TeV/*.root".format(mass=str(mass)),
						channel+"_dirIso" + ("_z" if channel in ["et", "mt"] else "") + "_jecUncNom" + ("_tauEsNom" if channel in ["tt", "et", "mt"] else "") + "/ntuple",
						lumi,
						weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts) + ("/crossSectionPerEventWeight" if normalise_signal_to_one_pb else ""),
						"qqh%s" % str(mass),
						nick_suffix=nick_suffix
			)
			else:
				log.error("Sample config (VBF%s) currently not implemented for channel \"%s\"!" % (str(mass), channel))
			
			if not kwargs.get("no_plot", False):
				Samples._add_plot(config, "sig", "LINE", "L", "qqh"+str(mass), nick_suffix)
		return config
	
	def vh(self, config, channel, category, weight, nick_suffix, higgs_masses, normalise_signal_to_one_pb=False, lumi=19712.0, exclude_cuts=None, **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []
		
		scale_factor = lumi
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("VH", 1.0)
		
		for mass in higgs_masses:
			if channel in ["tt", "et", "mt", "em", "mm"]:
				Samples._add_input(
						config,
						"SM_WH_ZH_TTH_HToTauTau_M_{mass}_powheg_pythia_8TeV/*.root".format(mass=str(mass)),
						channel+"_dirIso" + ("_z" if channel in ["et", "mt"] else "") + "_jecUncNom" + ("_tauEsNom" if channel in ["tt", "et", "mt"] else "") + "/ntuple",
						lumi / 2.0,
						weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts) + ("/crossSectionPerEventWeight" if normalise_signal_to_one_pb else ""),
						"vh%s" % str(mass),
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						"SM_WH_ZH_TTH_HToTauTau_M_{mass}_powheg_pythia_8TeV/*.root".format(mass=str(mass)),
						channel+"_dirIso" + ("_z" if channel in ["et", "mt"] else "") + "_jecUncNom" + ("_tauEsNom" if channel in ["tt", "et", "mt"] else "") + "/ntuple",
						lumi / 2.0,
						weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts) + ("/crossSectionPerEventWeight" if normalise_signal_to_one_pb else ""),
						"vh%s" % str(mass),
						nick_suffix=nick_suffix
				)
			else:
				log.error("Sample config (VH%s) currently not implemented for channel \"%s\"!" % (str(mass), channel))
			
			if not kwargs.get("no_plot", False):
				Samples._add_plot(config, "sig", "LINE", "L", "vh"+str(mass), nick_suffix)
		return config

