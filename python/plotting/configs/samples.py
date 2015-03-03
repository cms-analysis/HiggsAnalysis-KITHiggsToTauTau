
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import copy

import Artus.Utility.jsonTools as jsonTools



class Sample(object):

	def __init__(self):
		self.config = jsonTools.JsonDict({})
	
	def get_config(self, samples, channel, category, **kwargs):
		config = copy.deepcopy(self.config)
		
		for sample in samples:
			config = sample(config, channel, category, **kwargs)
		
		if not category is None:
			config["weights"] = [weight+("*(isCat%s>0)" % category) for weight in config.setdefault("weights", [])]
		
		config.setdefault("analysis_modules", []).append("@CorrectNegativeBinContents")
		config.setdefault("analysis_modules", []).append("PrintInfos")
		
		config["nicks_blacklist"] = ["noplot"]
		config["legend"] = [0.75, 0.55]
		config["file_mode"] = "UPDATE"
		
		return config.doIncludes().doComments()
	
	@staticmethod
	def data(config, channel, category, **kwargs):
		if (channel == "et") or (channel == "mt"):
			Sample._add_input(
					config,
					"Tau*_Run2012?_22Jan2013_8TeV/*.root",
					channel+"_dirIso_z_tauEs/ntuple",
					1.0,
					"eventWeight*((q_1*q_2)<0.0)*(pt_2>30.0)*(lep1MetMt<30.0)",
					"data"
			)
		elif channel == "em":
			Sample._add_input(
					config,
					"MuEG_Run2012?_22Jan2013_8TeV/*.root",
					"em_dirIso/ntuple",
					1.0,
					"eventWeight*((q_1*q_2)<0.0)",
					"data"
			)
		else:
			log.error("Sample config currently not implemented for channel \"%s\"!" % channel)
		
		Sample._add_plot(config, "data", "#000000", "Data")
		return config
	
	@staticmethod
	def ztt(config, channel, category, lumi=19712.0, **kwargs):
		if (channel == "et") or (channel == "mt") or (channel == "em"):
			Sample._add_input(
					config,
					"*_PFembedded_Run2012?_22Jan2013_"+channel+"_8TeV/*.root",
					"em_dirIso/ntuple" if channel == "em" else channel+"_dirIso_z_tauEs/ntuple",
					1.0,
					"eventWeight*((q_1*q_2)<0.0)" + ("" if channel == "em" else "*(pt_2>30.0)*(lep1MetMt<30.0)"),
					"ztt"
			)
			Sample._add_input(
					config,
					"*_PFembedded_Run2012?_22Jan2013_"+channel+"_8TeV/*.root",
					"em_dirIso/ntuple" if channel == "em" else channel+"_dirIso_z_tauEs/ntuple",
					1.0,
					"eventWeight*((q_1*q_2)<0.0)" + ("" if channel == "em" else "*(pt_2>30.0)*(lep1MetMt<30.0)"),
					"noplot_ztt_emb_inc"
			)
			Sample._add_input(
					config,
					"DYJetsToLL_M_50_madgraph_8TeV/*.root",
					"em_dirIso_tt/ntuple" if channel == "em" else channel+"_dirIso_ztt_tauEsNom/ntuple",
					lumi,
					"eventWeight*((q_1*q_2)<0.0)" + ("" if channel == "em" else "*(pt_2>30.0)*(lep1MetMt<30.0)"),
					"noplot_ztt_mc_inc"
			)
			Sample._add_input(
					config,
					"DYJetsToLL_M_50_madgraph_8TeV/*.root",
					"em_dirIso_tt/ntuple" if channel == "em" else channel+"_dirIso_ztt_tauEsNom/ntuple",
					lumi,
					"eventWeight*((q_1*q_2)<0.0)" + ("" if channel == "em" else "*(pt_2>30.0)*(lep1MetMt<30.0)"),
					"noplot_ztt_mc"
			)
			config.setdefault("analysis_modules", []).append("EstimateZtt")
		else:
			log.error("Sample config currently not implemented for channel \"%s\"!" % channel)
		
		Sample._add_plot(config, "bkg", "#FFCC66", "ZTT")
		
		return config
	
	@staticmethod
	def zl(config, channel, category, lumi=19712.0, **kwargs):
		if (channel == "et") or (channel == "mt") or (channel == "em"):
			Sample._add_input(
					config,
					"DYJetsToLL_M_50_madgraph_8TeV/*.root",
					"em_dirIso_ee/ntuple em_dirIso_mm/ntuple" if channel == "em" else channel+"_dirIso_zl_tauEsNom/ntuple",
					lumi,
					"eventWeight*((q_1*q_2)<0.0)" + ("" if channel == "em" else "*(pt_2>30.0)*(lep1MetMt<30.0)"),
					"zl"
			)
		else:
			log.error("Sample config currently not implemented for channel \"%s\"!" % channel)
		
		Sample._add_plot(config, "bkg", "#4496C8", "ZL")
		return config
	
	@staticmethod
	def zj(config, channel, category, lumi=19712.0, **kwargs):
		if (channel == "et") or (channel == "mt"):
			Sample._add_input(
					config,
					"DYJetsToLL_M_50_madgraph_8TeV/*.root",
					channel+"_dirIso_zj_tauEsNom/ntuple",
					lumi,
					"eventWeight*((q_1*q_2)<0.0)*(pt_2>30.0)*(lep1MetMt<30.0)",
					"zj"
			)
			Sample._add_plot(config, "bkg", "#64B6E8", "ZJ")
		elif channel == "em":
			pass
		else:
			log.error("Sample config currently not implemented for channel \"%s\"!" % channel)
		
		return config
	
	@staticmethod
	def ttj(config, channel, category, lumi=19712.0, **kwargs):
		if (channel == "et") or (channel == "mt"):
			Sample._add_input(
					config,
					"TTJets*_madgraph_tauola_8TeV/*.root",
					channel+"_dirIso_z_tauEs/ntuple",
					lumi,
					"eventWeight*((q_1*q_2)<0.0)*(pt_2>30.0)*(lep1MetMt<30.0)",
					"ttj"
			)
		elif channel == "em":
			Sample._add_input(
					config,
					"TTJetsTo*_madgraph_tauola_8TeV/*.root",
					"em_dirIso/ntuple",
					lumi,
					"eventWeight*((q_1*q_2)<0.0)",
					"ttj"
			)
			Sample._add_input(
					config,
					"T*_powheg_tauola_8TeV/*.root",
					"em_dirIso/ntuple",
					lumi,
					"eventWeight*((q_1*q_2)<0.0)",
					"ttj"
			)
		else:
			log.error("Sample config currently not implemented for channel \"%s\"!" % channel)
		
		Sample._add_plot(config, "bkg", "#9999CC", "TTJ")
		return config
	
	@staticmethod
	def vv(config, channel, category, lumi=19712.0, **kwargs):
		if (channel == "et") or (channel == "mt"):
			Sample._add_input(
					config,
					"??_pythia_tauola_8TeV/*.root",
					channel+"_dirIso_z_tauEs/ntuple",
					lumi,
					"eventWeight*((q_1*q_2)<0.0)*(pt_2>30.0)*(lep1MetMt<30.0)",
					"diboson"
			)
		elif channel == "em":
			Sample._add_input(
					config,
					"??JetsTo*_madgraph_tauola_8TeV/*.root",
					"em_dirIso/ntuple",
					lumi,
					"eventWeight*((q_1*q_2)<0.0)",
					"diboson"
			)
		else:
			log.error("Sample config currently not implemented for channel \"%s\"!" % channel)
		
		Sample._add_plot(config, "bkg", "#DE5A6A", "VV")
		return config
	
	@staticmethod
	def wj(config, channel, category, lumi=19712.0, **kwargs):
		if (channel == "et") or (channel == "mt"):
			Sample._add_input(
					config,
					"WJetsToLN_madgraph_8TeV/*.root",
					channel+"_dirIso_z_tauEs/ntuple",
					lumi,
					"eventWeight*((q_1*q_2)<0.0)*(pt_2>30.0)*(lep1MetMt<30.0)",
					"wjets"
			)
			Sample._add_input(
					config,
					"Tau*_Run2012?_22Jan2013_8TeV/*.root",
					channel+"_dirIso_z_tauEs/ntuple",
					1.0,
					"eventWeight*((q_1*q_2)<0.0)*(pt_2>30.0)*(lep1MetMt>70.0)",
					"noplot_wjets_data_control"
			)
			Sample._add_input(
					config,
					"DYJetsToLL_M_50_madgraph_8TeV/*.root",
					channel+"_dirIso_ztt_tauEsNom/ntuple",
					lumi,
					"eventWeight*((q_1*q_2)<0.0)*(pt_2>30.0)*(lep1MetMt>70.0)",
					"noplot_ztt_mc_wjet_control"
			)
			Sample._add_input(
					config,
					"DYJetsToLL_M_50_madgraph_8TeV/*.root",
					channel+"_dirIso_zl_tauEsNom/ntuple "+channel+"_dirIso_zj_tauEsNom/ntuple",
					lumi,
					"eventWeight*((q_1*q_2)<0.0)*(pt_2>30.0)*(lep1MetMt>70.0)",
					"noplot_zll_wjet_control"
			)
			Sample._add_input(
					config,
					"TTJets*_madgraph_tauola_8TeV/*.root",
					channel+"_dirIso_z_tauEs/ntuple",
					lumi,
					"eventWeight*((q_1*q_2)<0.0)*(pt_2>30.0)*(lep1MetMt>70.0)",
					"noplot_ttj_wjet_control"
			)
			Sample._add_input(
					config,
					"??_pythia_tauola_8TeV/*.root",
					channel+"_dirIso_z_tauEs/ntuple",
					lumi,
					"eventWeight*((q_1*q_2)<0.0)*(pt_2>30.0)*(lep1MetMt>70.0)",
					"noplot_diboson_wjet_control"
			)
			Sample._add_input(
					config,
					"WJetsToLN_madgraph_8TeV/*.root",
					channel+"_dirIso_z_tauEs/ntuple",
					lumi,
					"eventWeight*((q_1*q_2)<0.0)*(pt_2>30.0)*(lep1MetMt<30.0)",
					"noplot_wjets_mc_signal"
			)
			Sample._add_input(
					config,
					"WJetsToLN_madgraph_8TeV/*.root",
					channel+"_dirIso_z_tauEs/ntuple",
					lumi,
					"eventWeight*((q_1*q_2)<0.0)*(pt_2>30.0)*(lep1MetMt>70.0)",
					"noplot_wjets_mc_control"
			)
			config.setdefault("analysis_modules", []).append("EstimateWjets")
		elif channel == "em":
			Sample._add_input(
					config,
					"WJetsToLN_madgraph_8TeV/*.root",
					"em_dirIso/ntuple",
					lumi,
					"eventWeight*((q_1*q_2)<0.0)",
					"wjets"
			)
		else:
			log.error("Sample config currently not implemented for channel \"%s\"!" % channel)
		
		Sample._add_plot(config, "bkg", "#FE7A8A", "WJets")
		return config
	
	@staticmethod
	def qcd(config, channel, category, lumi=19712.0, **kwargs):
		if (channel == "et") or (channel == "mt"):
			Sample._add_input(
					config,
					"WJetsToLN_madgraph_8TeV/*.root",
					channel+"_dirIso_z_tauEs/ntuple",
					lumi,
					"eventWeight*((q_1*q_2)>0.0)*(pt_2>30.0)*(lep1MetMt<30.0)",
					"noplot_wjets_ss"
			)
			Sample._add_input(
					config,
					"Tau*_Run2012?_22Jan2013_8TeV/*.root",
					channel+"_dirIso_z_tauEs/ntuple",
					1.0,
					"eventWeight*((q_1*q_2)>0.0)*(pt_2>30.0)*(lep1MetMt>70.0)",
					"noplot_wjets_ss_data_control"
			)
			Sample._add_input(
					config,
					"DYJetsToLL_M_50_madgraph_8TeV/*.root",
					channel+"_dirIso_ztt_tauEsNom/ntuple",
					lumi,
					"eventWeight*((q_1*q_2)>0.0)*(pt_2>30.0)*(lep1MetMt>70.0)",
					"noplot_ztt_ss_mc_wjet_control"
			)
			Sample._add_input(
					config,
					"DYJetsToLL_M_50_madgraph_8TeV/*.root",
					channel+"_dirIso_zl_tauEsNom/ntuple "+channel+"_dirIso_zj_tauEsNom/ntuple",
					lumi,
					"eventWeight*((q_1*q_2)>0.0)*(pt_2>30.0)*(lep1MetMt>70.0)",
					"noplot_zll_ss_wjet_control"
			)
			Sample._add_input(
					config,
					"TTJets*_madgraph_tauola_8TeV/*.root",
					channel+"_dirIso_z_tauEs/ntuple",
					lumi,
					"eventWeight*((q_1*q_2)>0.0)*(pt_2>30.0)*(lep1MetMt>70.0)",
					"noplot_ttj_ss_wjet_control"
			)
			Sample._add_input(
					config,
					"??_pythia_tauola_8TeV/*.root",
					channel+"_dirIso_z_tauEs/ntuple",
					lumi,
					"eventWeight*((q_1*q_2)>0.0)*(pt_2>30.0)*(lep1MetMt>70.0)",
					"noplot_diboson_ss_wjet_control"
			)
			Sample._add_input(
					config,
					"WJetsToLN_madgraph_8TeV/*.root",
					channel+"_dirIso_z_tauEs/ntuple",
					lumi,
					"eventWeight*((q_1*q_2)>0.0)*(pt_2>30.0)*(lep1MetMt<30.0)",
					"noplot_wjets_ss_mc_signal"
			)
			Sample._add_input(
					config,
					"WJetsToLN_madgraph_8TeV/*.root",
					channel+"_dirIso_z_tauEs/ntuple",
					lumi,
					"eventWeight*((q_1*q_2)>0.0)*(pt_2>30.0)*(lep1MetMt>70.0)",
					"noplot_wjets_ss_mc_control"
			)
		
			# QCD
			Sample._add_input(
					config,
					"Tau*_Run2012?_22Jan2013_8TeV/*.root",
					channel+"_dirIso_z_tauEs/ntuple",
					1.0,
					"eventWeight*((q_1*q_2)>0.0)*(pt_2>30.0)*(lep1MetMt<30.0)",
					"qcd"
			)
			Sample._add_input(
					config,
					"DYJetsToLL_M_50_madgraph_8TeV/*.root",
					channel+"_dirIso_ztt_tauEsNom/ntuple",
					lumi,
					"eventWeight*((q_1*q_2)>0.0)*(pt_2>30.0)*(lep1MetMt<30.0)",
					"noplot_ztt_mc_qcd_control"
			)
			Sample._add_input(
					config,
					"DYJetsToLL_M_50_madgraph_8TeV/*.root",
					channel+"_dirIso_zl_tauEsNom/ntuple "+channel+"_dirIso_zj_tauEsNom/ntuple",
					lumi,
					"eventWeight*((q_1*q_2)>0.0)*(pt_2>30.0)*(lep1MetMt<30.0)",
					"noplot_zll_qcd_control"
			)
			Sample._add_input(
					config,
					"TTJets*_madgraph_tauola_8TeV/*.root",
					channel+"_dirIso_z_tauEs/ntuple",
					lumi,
					"eventWeight*((q_1*q_2)>0.0)*(pt_2>30.0)*(lep1MetMt<30.0)",
					"noplot_ttj_qcd_control"
			)
			Sample._add_input(
					config,
					"??_pythia_tauola_8TeV/*.root",
					channel+"_dirIso_z_tauEs/ntuple",
					lumi,
					"eventWeight*((q_1*q_2)>0.0)*(pt_2>30.0)*(lep1MetMt<30.0)",
					"noplot_diboson_qcd_control"
			)
			config.setdefault("analysis_modules", []).append("EstimateQcd")
		elif channel == "em":
			Sample._add_input(
					config,
					"MuEG_Run2012?_22Jan2013_8TeV/*.root",
					"em_dirIso/ntuple",
					1.0,
					"eventWeight*((q_1*q_2)>0.0)",
					"qcd"
			)
		else:
			log.error("Sample config currently not implemented for channel \"%s\"!" % channel)
		
		Sample._add_plot(config, "bkg", "#FFCCFF", "QCD")
		return config
	
	@staticmethod
	def ggh(config, channel, category, higgs_masses, normalise_signal_to_one_pb=False, lumi=19712.0, **kwargs):
		for mass in higgs_masses:
			if (channel == "et") or (channel == "mt") or (channel == "em"):
				Sample._add_input(
						config,
						"SM_GluGluToHToTauTau_M_%s_powheg_pythia_8TeV/*.root" % str(mass),
						"em_dirIso/ntuple" if channel == "em" else channel+"_dirIso_z_tauEsNom/ntuple",
						lumi,
						"eventWeight*((q_1*q_2)<0.0)" + ("" if channel == "em" else "*(pt_2>30.0)*(lep1MetMt<30.0)") + ("/crossSectionPerEventWeight" if normalise_signal_to_one_pb else ""),
						"ggH%s" % str(mass)
				)
			else:
				log.error("Sample config currently not implemented for channel \"%s\"!" % channel)
			
			Sample._add_plot(config, "sig", "#000000", "ggH%s" % str(mass))
		return config
	
	@staticmethod
	def qqh(config, channel, category, higgs_masses, normalise_signal_to_one_pb=False, lumi=19712.0, **kwargs):
		for mass in higgs_masses:
			if (channel == "et") or (channel == "mt") or (channel == "em"):
				Sample._add_input(
						config,
						"SM_VBFHToTauTau_M_%s_powheg_pythia_8TeV/*.root" % str(mass),
						"em_dirIso/ntuple" if channel == "em" else channel+"_dirIso_z_tauEsNom/ntuple",
						lumi,
						"eventWeight*((q_1*q_2)<0.0)" + ("" if channel == "em" else "*(pt_2>30.0)*(lep1MetMt<30.0)") + ("/crossSectionPerEventWeight" if normalise_signal_to_one_pb else ""),
						"VBF%s" % str(mass)
			)
			else:
				log.error("Sample config currently not implemented for channel \"%s\"!" % channel)
			
			Sample._add_plot(config, "sig", "#000000", "VBF%s" % str(mass))
		return config
	
	@staticmethod
	def vh(config, channel, category, higgs_masses, normalise_signal_to_one_pb=False, lumi=19712.0, **kwargs):
		for mass in higgs_masses:
			if (channel == "et") or (channel == "mt") or (channel == "em"):
				Sample._add_input(
						config,
						"SM_WH_ZH_TTH_HToTauTau_M_%s_powheg_pythia_8TeV/*.root" % str(mass),
						"em_dirIso/ntuple" if channel == "em" else channel+"_dirIso_z_tauEsNom/ntuple",
						lumi / 2.0,
						"eventWeight*((q_1*q_2)<0.0)" + ("" if channel == "em" else "*(pt_2>30.0)*(lep1MetMt<30.0)") + ("/crossSectionPerEventWeight" if normalise_signal_to_one_pb else ""),
						"WH%s" % str(mass)
				)
				Sample._add_input(
						config,
						"SM_WH_ZH_TTH_HToTauTau_M_%s_powheg_pythia_8TeV/*.root" % str(mass),
						"em_dirIso/ntuple" if channel == "em" else channel+"_dirIso_z_tauEsNom/ntuple",
						lumi / 2.0,
						"eventWeight*((q_1*q_2)<0.0)" + ("" if channel == "em" else "*(pt_2>30.0)*(lep1MetMt<30.0)") + ("/crossSectionPerEventWeight" if normalise_signal_to_one_pb else ""),
						"ZH%s" % str(mass)
				)
			else:
				log.error("Sample config currently not implemented for channel \"%s\"!" % channel)
			
			Sample._add_plot(config, "sig", "#000000", "WH%s" % str(mass))
			Sample._add_plot(config, "sig", "#000000", "ZH%s" % str(mass))
		return config
	
	@staticmethod
	def _add_input(config, file, folder, scale_factor, weight, nick):
		config.setdefault("files", []).append(file)
		config.setdefault("folders", []).append(folder)
		config.setdefault("scale_factors", []).append(scale_factor)
		config.setdefault("weights", []).append(weight)
		config.setdefault("nicks", []).append(nick)
		return config
		
	@staticmethod
	def _add_plot(config, stack, color, label):
		config.setdefault("stacks", []).append(stack)
		config.setdefault("colors", []).append(color)
		config.setdefault("labels", []).append(label)
		return config

