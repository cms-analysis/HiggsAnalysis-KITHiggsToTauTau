
# -*- coding: utf-8 -*-

import copy

import Artus.Utility.jsonTools as jsonTools



class MT(object):

	def __init__(self, add_data=True, add_ztt=True, add_zl=True, add_zj=True, add_ttj=True, add_diboson=True, add_wjets=True, add_qcd=True,
	             add_ggh_signal=[], add_vbf_signal=[], add_vh_signal=[]):
		self.config = jsonTools.JsonDict({})
		
		# Data
		if add_data:
			self.add_input("Tau*_Run2012?_22Jan2013_8TeV/*.root", "mt_dirIso_z_tauEs/ntuple", 1.0, "eventWeight*((q_1*q_2)<0.0)*(pt_2>30.0)*(lep1MetMt<30.0)", "data")
			
			self.add_plot("data", "#000000", "Data")
		
		# DY->tautau
		if add_ztt:
			self.add_input("*_PFembedded_Run2012?_22Jan2013_mt_8TeV/*.root", "mt_dirIso_z_tauEs/ntuple", 1.0, "eventWeight*((q_1*q_2)<0.0)*(pt_2>30.0)*(lep1MetMt<30.0)", "ztt")
			self.add_input("*_PFembedded_Run2012?_22Jan2013_mt_8TeV/*.root", "mt_dirIso_z_tauEs/ntuple", 1.0, "eventWeight*((q_1*q_2)<0.0)*(pt_2>30.0)*(lep1MetMt<30.0)", "noplot_ztt_emb_inc")
			self.add_input("DYJetsToLL_M_50_madgraph_8TeV/*.root", "mt_dirIso_ztt_tauEsNom/ntuple", 19712.0, "eventWeight*((q_1*q_2)<0.0)*(pt_2>30.0)*(lep1MetMt<30.0)", "noplot_ztt_mc_inc")
			self.add_input("DYJetsToLL_M_50_madgraph_8TeV/*.root", "mt_dirIso_ztt_tauEsNom/ntuple", 19712.0, "eventWeight*((q_1*q_2)<0.0)*(pt_2>30.0)*(lep1MetMt<30.0)", "noplot_ztt_mc")
			
			self.add_plot("bkg", "#FFCC66", "ZTT")
		
		# ZL
		if add_zl:
			self.add_input("DYJetsToLL_M_50_madgraph_8TeV/*.root", "mt_dirIso_zl_tauEsNom/ntuple", 19712.0, "eventWeight*((q_1*q_2)<0.0)*(pt_2>30.0)*(lep1MetMt<30.0)", "zl")
			
			self.add_plot("bkg", "#4496C8", "ZL")
		
		# ZJ
		if add_zj:
			self.add_input("DYJetsToLL_M_50_madgraph_8TeV/*.root", "mt_dirIso_zj_tauEsNom/ntuple", 19712.0, "eventWeight*((q_1*q_2)<0.0)*(pt_2>30.0)*(lep1MetMt<30.0)", "zj")
			
			self.add_plot("bkg", "#64B6E8", "ZJ")
		
		# TTJets
		if add_ttj:
			self.add_input("TTJets*_madgraph_tauola_8TeV/*.root", "mt_dirIso_z_tauEs/ntuple", 19712.0, "eventWeight*((q_1*q_2)<0.0)*(pt_2>30.0)*(lep1MetMt<30.0)", "ttj")
			
			self.add_plot("bkg", "#9999CC", "TTJ")
		
		# Dibosons
		if add_diboson:
			self.add_input("??_pythia_tauola_8TeV/*.root", "mt_dirIso_z_tauEs/ntuple", 19712.0, "eventWeight*((q_1*q_2)<0.0)*(pt_2>30.0)*(lep1MetMt<30.0)", "diboson")
			
			self.add_plot("bkg", "#DE5A6A", "VV")
		
		# WJets
		if add_wjets:
			self.add_input("WJetsToLN_madgraph_8TeV/*.root", "mt_dirIso_z_tauEs/ntuple", 19712.0, "eventWeight*((q_1*q_2)<0.0)*(pt_2>30.0)*(lep1MetMt<30.0)", "wjets")
			self.add_input("Tau*_Run2012?_22Jan2013_8TeV/*.root", "mt_dirIso_z_tauEs/ntuple", 1.0, "eventWeight*((q_1*q_2)<0.0)*(pt_2>30.0)*(lep1MetMt>70.0)", "noplot_wjets_data_control")
			self.add_input("DYJetsToLL_M_50_madgraph_8TeV/*.root", "mt_dirIso_ztt_tauEsNom/ntuple", 19712.0, "eventWeight*((q_1*q_2)<0.0)*(pt_2>30.0)*(lep1MetMt>70.0)", "noplot_ztt_mc_wjet_control")
			self.add_input("DYJetsToLL_M_50_madgraph_8TeV/*.root", "mt_dirIso_zl_tauEsNom/ntuple mt_dirIso_zj_tauEsNom/ntuple", 19712.0, "eventWeight*((q_1*q_2)<0.0)*(pt_2>30.0)*(lep1MetMt>70.0)", "noplot_zll_wjet_control")
			self.add_input("TTJets*_madgraph_tauola_8TeV/*.root", "mt_dirIso_z_tauEs/ntuple", 19712.0, "eventWeight*((q_1*q_2)<0.0)*(pt_2>30.0)*(lep1MetMt>70.0)", "noplot_ttj_wjet_control")
			self.add_input("??_pythia_tauola_8TeV/*.root", "mt_dirIso_z_tauEs/ntuple", 19712.0, "eventWeight*((q_1*q_2)<0.0)*(pt_2>30.0)*(lep1MetMt>70.0)", "noplot_diboson_wjet_control")
			self.add_input("WJetsToLN_madgraph_8TeV/*.root", "mt_dirIso_z_tauEs/ntuple", 19712.0, "eventWeight*((q_1*q_2)<0.0)*(pt_2>30.0)*(lep1MetMt<30.0)", "noplot_wjets_mc_signal")
			self.add_input("WJetsToLN_madgraph_8TeV/*.root", "mt_dirIso_z_tauEs/ntuple", 19712.0, "eventWeight*((q_1*q_2)<0.0)*(pt_2>30.0)*(lep1MetMt>70.0)", "noplot_wjets_mc_control")
			
			self.add_plot("bkg", "#FE7A8A", "WJets")
		
		if add_qcd:
			# WJets (SS, for substraction in QCD estimation)
			self.add_input("WJetsToLN_madgraph_8TeV/*.root", "mt_dirIso_z_tauEs/ntuple", 19712.0, "eventWeight*((q_1*q_2)>0.0)*(pt_2>30.0)*(lep1MetMt<30.0)", "noplot_wjets_ss")
			self.add_input("Tau*_Run2012?_22Jan2013_8TeV/*.root", "mt_dirIso_z_tauEs/ntuple", 1.0, "eventWeight*((q_1*q_2)>0.0)*(pt_2>30.0)*(lep1MetMt>70.0)", "noplot_wjets_ss_data_control")
			self.add_input("DYJetsToLL_M_50_madgraph_8TeV/*.root", "mt_dirIso_ztt_tauEsNom/ntuple", 19712.0, "eventWeight*((q_1*q_2)>0.0)*(pt_2>30.0)*(lep1MetMt>70.0)", "noplot_ztt_ss_mc_wjet_control")
			self.add_input("DYJetsToLL_M_50_madgraph_8TeV/*.root", "mt_dirIso_zl_tauEsNom/ntuple mt_dirIso_zj_tauEsNom/ntuple", 19712.0, "eventWeight*((q_1*q_2)>0.0)*(pt_2>30.0)*(lep1MetMt>70.0)", "noplot_zll_ss_wjet_control")
			self.add_input("TTJets*_madgraph_tauola_8TeV/*.root", "mt_dirIso_z_tauEs/ntuple", 19712.0, "eventWeight*((q_1*q_2)>0.0)*(pt_2>30.0)*(lep1MetMt>70.0)", "noplot_ttj_ss_wjet_control")
			self.add_input("??_pythia_tauola_8TeV/*.root", "mt_dirIso_z_tauEs/ntuple", 19712.0, "eventWeight*((q_1*q_2)>0.0)*(pt_2>30.0)*(lep1MetMt>70.0)", "noplot_diboson_ss_wjet_control")
			self.add_input("WJetsToLN_madgraph_8TeV/*.root", "mt_dirIso_z_tauEs/ntuple", 19712.0, "eventWeight*((q_1*q_2)>0.0)*(pt_2>30.0)*(lep1MetMt<30.0)", "noplot_wjets_ss_mc_signal")
			self.add_input("WJetsToLN_madgraph_8TeV/*.root", "mt_dirIso_z_tauEs/ntuple", 19712.0, "eventWeight*((q_1*q_2)>0.0)*(pt_2>30.0)*(lep1MetMt>70.0)", "noplot_wjets_ss_mc_control")
		
			# QCD
			self.add_input("Tau*_Run2012?_22Jan2013_8TeV/*.root", "mt_dirIso_z_tauEs/ntuple", 1.0, "eventWeight*((q_1*q_2)>0.0)*(pt_2>30.0)*(lep1MetMt<30.0)", "qcd")
			self.add_input("DYJetsToLL_M_50_madgraph_8TeV/*.root", "mt_dirIso_ztt_tauEsNom/ntuple", 19712.0, "eventWeight*((q_1*q_2)>0.0)*(pt_2>30.0)*(lep1MetMt<30.0)", "noplot_ztt_mc_qcd_control")
			self.add_input("DYJetsToLL_M_50_madgraph_8TeV/*.root", "mt_dirIso_zl_tauEsNom/ntuple mt_dirIso_zj_tauEsNom/ntuple", 19712.0, "eventWeight*((q_1*q_2)>0.0)*(pt_2>30.0)*(lep1MetMt<30.0)", "noplot_zll_qcd_control")
			self.add_input("TTJets*_madgraph_tauola_8TeV/*.root", "mt_dirIso_z_tauEs/ntuple", 19712.0, "eventWeight*((q_1*q_2)>0.0)*(pt_2>30.0)*(lep1MetMt<30.0)", "noplot_ttj_qcd_control")
			self.add_input("??_pythia_tauola_8TeV/*.root", "mt_dirIso_z_tauEs/ntuple", 19712.0, "eventWeight*((q_1*q_2)>0.0)*(pt_2>30.0)*(lep1MetMt<30.0)", "noplot_diboson_qcd_control")
			
			self.add_plot("bkg", "#FFCCFF", "QCD")
		
		for higgs_mass in add_ggh_signal:
			self.add_input("SM_GluGluToHToTauTau_M_%s_powheg_pythia_8TeV/*.root" % str(higgs_mass), "mt_dirIso_z_tauEsNom/ntuple", 19712.0, "eventWeight*((q_1*q_2)<0.0)*(pt_2>30.0)*(lep1MetMt<30.0)", "ggH%s" % str(higgs_mass))
			
			self.add_plot("sig", "#000000", "ggH%s" % str(higgs_mass))
		
		for higgs_mass in add_vbf_signal:
			self.add_input("SM_VBFHToTauTau_M_%s_powheg_pythia_8TeV/*.root" % str(higgs_mass), "mt_dirIso_z_tauEsNom/ntuple", 19712.0, "eventWeight*((q_1*q_2)<0.0)*(pt_2>30.0)*(lep1MetMt<30.0)", "VBF%s" % str(higgs_mass))
			
			self.add_plot("sig", "#000000", "VBF%s" % str(higgs_mass))
		
		for higgs_mass in add_vh_signal:
			self.add_input("SM_WH_ZH_TTH_HToTauTau_M_%s_powheg_pythia_8TeV/*.root" % str(higgs_mass), "mt_dirIso_z_tauEsNom/ntuple", 19712.0, "eventWeight*((q_1*q_2)<0.0)*(pt_2>30.0)*(lep1MetMt<30.0)", "VH%s" % str(higgs_mass))
			
			self.add_plot("sig", "#000000", "VH%s" % str(higgs_mass))
		
		# additional settings
		self.config.setdefault("analysis_modules", []).append("@CorrectNegativeBinContents")
		if add_ztt:
			self.config.setdefault("analysis_modules", []).append("EstimateZtt")
		if add_wjets:
			self.config.setdefault("analysis_modules", []).append("EstimateWjets")
		if add_qcd:
			self.config.setdefault("analysis_modules", []).append("EstimateQcd")
		self.config.setdefault("analysis_modules", []).append("PrintInfos")
		
		self.config["nicks_blacklist"] = [
			"noplot"
		]
		self.config["legend"] = [
			0.75,
			0.55
		]
		self.config["file_mode"] = "UPDATE"
		
		# finish baseline config
		self.config = self.config.doIncludes().doComments()
		
	def add_input(self, file, folder, scale_factor, weight, nick):
		self.config.setdefault("files", []).append(file)
		self.config.setdefault("folders", []).append(folder)
		self.config.setdefault("scale_factors", []).append(scale_factor)
		self.config.setdefault("weights", []).append(weight)
		self.config.setdefault("nicks", []).append(nick)
		
	def add_plot(self, stack, color, label):
		self.config.setdefault("stack", []).append(stack)
		self.config.setdefault("colors", []).append(color)
		self.config.setdefault("labels", []).append(label)
	
	def get_config(self, category=None, tau_es_shift="Nom"):
		config = copy.deepcopy(self.config)
		
		# categories
		if category is None:
			return config
		else:
			config["weights"] = [weight+("*(isCat%s>0)" % category) for weight in config.setdefault("weights", [])]
			return config

