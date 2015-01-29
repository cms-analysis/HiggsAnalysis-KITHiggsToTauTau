
# -*- coding: utf-8 -*-

import Artus.Utility.jsonTools as jsonTools

class MT(object):
	def __init__(self, add_data=True, add_ztt=True, add_zl=True, add_zj=True, add_ttj=True, add_diboson=True, add_wjets=True, add_qcd=True):
		self.config = jsonTools.JsonDict({})
		
		# Data
		if add_data:
			self.add_input("Tau*_Run2012?_22Jan2013_8TeV/*.root", "mt_dirIso_z_tauEs/ntuple", 1.0, "eventWeight*((q_1*q_2)<0.0)*(pt_2>30.0)*(lep1MetMt<30.0)", "data")
		
		# DY->tautau
		if add_ztt:
			self.add_input("*_PFembedded_Run2012?_22Jan2013_mt_8TeV/*.root", "mt_dirIso_z_tauEs/ntuple", 1.0, "eventWeight*((q_1*q_2)<0.0)*(pt_2>30.0)*(lep1MetMt<30.0)", "ztt")
			self.add_input("*_PFembedded_Run2012?_22Jan2013_mt_8TeV/*.root", "mt_dirIso_z_tauEs/ntuple", 1.0, "eventWeight*((q_1*q_2)<0.0)*(pt_2>30.0)*(lep1MetMt<30.0)", "noplot_ztt_emb_inc")
			self.add_input("DYJetsToLL_M_50_madgraph_8TeV/*.root", "mt_dirIso_ztt_tauEsNom/ntuple", 19712.0, "eventWeight*((q_1*q_2)<0.0)*(pt_2>30.0)*(lep1MetMt<30.0)", "noplot_ztt_mc_inc")
			self.add_input("DYJetsToLL_M_50_madgraph_8TeV/*.root", "mt_dirIso_ztt_tauEsNom/ntuple", 19712.0, "eventWeight*((q_1*q_2)<0.0)*(pt_2>30.0)*(lep1MetMt<30.0)", "noplot_ztt_mc")
		
		# ZL
		if add_zl:
			self.add_input("DYJetsToLL_M_50_madgraph_8TeV/*.root", "mt_dirIso_zl_tauEsNom/ntuple", 19712.0, "eventWeight*((q_1*q_2)<0.0)*(pt_2>30.0)*(lep1MetMt<30.0)", "zl")
		
		# ZJ
		if add_zj:
			self.add_input("DYJetsToLL_M_50_madgraph_8TeV/*.root", "mt_dirIso_zj_tauEsNom/ntuple", 19712.0, "eventWeight*((q_1*q_2)<0.0)*(pt_2>30.0)*(lep1MetMt<30.0)", "zj")
		
		# TTJets
		if add_ttj:
			self.add_input("TTJets*_madgraph_tauola_8TeV/*.root", "mt_dirIso_z_tauEs/ntuple", 19712.0, "eventWeight*((q_1*q_2)<0.0)*(pt_2>30.0)*(lep1MetMt<30.0)", "ttj")
		
		# Dibosons
		if add_diboson:
			self.add_input("??_pythia_tauola_8TeV/*.root", "mt_dirIso_z_tauEs/ntuple", 19712.0, "eventWeight*((q_1*q_2)<0.0)*(pt_2>30.0)*(lep1MetMt<30.0)", "diboson")
		
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
		
		# additional settings
		self.config["analysis_modules"] = [
			"@CorrectNegativeBinContents",
			"EstimateZtt",
			"EstimateWjets",
			"EstimateQcd",
			"PrintInfos"
		]
		self.config["nicks_blacklist"] = [
			"noplot"
		]
		self.config["stack"] = [
			"data",
			"bkg",
			"bkg",
			"bkg",
			"bkg",
			"bkg",
			"bkg",
			"bkg"
		]
		self.config["colors"] = [
			"#000000",
			"#FFCC66",
			"#4496C8",
			"#64B6E8",
			"#9999CC",
			"#DE5A6A",
			"#FE7A8A",
			"#FFCCFF"
		]
		self.config["labels"] = [
			"Data",
			"ZTT",
			"ZL",
			"ZJ",
			"TTJ",
			"VV",
			"WJ",
			"QCD"
		]
		self.config["legloc"] = [
			0.75,
			0.55
		]
		
	def add_input(self, file, folder, scale_factor, weight, nick):
		self.config.setdefault("files", []).append(file)
		self.config.setdefault("folders", []).append(folder)
		self.config.setdefault("scale_factors", []).append(scale_factor)
		self.config.setdefault("weights", []).append(weight)
		self.config.setdefault("nicks", []).append(nick)
	
	def get_config(self):
		return self.config.doIncludes().doComments()

