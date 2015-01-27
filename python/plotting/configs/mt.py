
# -*- coding: utf-8 -*-

import Artus.Utility.jsonTools as jsonTools

class MT(object):
	def __init__(self):
		self.config = jsonTools.JsonDict({})
		
		# Data
		self.add_input("Tau*_Run2012?_22Jan2013_8TeV/*.root", "mt_os_dirIso_z_tauEs/ntuple", 1.0, "eventWeight*(pt_2>30.0)*(lep1MetMt<30.0)", "data")
		
		# DY->tautau
		self.add_input("*_PFembedded_Run2012?_22Jan2013_mt_8TeV/*.root", "mt_os_dirIso_z_tauEs/ntuple", 1.0, "eventWeight*(pt_2>30.0)*(lep1MetMt<30.0)", "ztt")
		self.add_input("*_PFembedded_Run2012?_22Jan2013_mt_8TeV/*.root", "mt_os_dirIso_z_tauEs/ntuple", 1.0, "eventWeight*(pt_2>30.0)*(lep1MetMt<30.0)", "noplot_ztt_emb_inc")
		self.add_input("DYJetsToLL_M_50_madgraph_8TeV/*.root", "mt_os_dirIso_ztt_tauEsNom/ntuple", 19712.0, "eventWeight*(pt_2>30.0)*(lep1MetMt<30.0)", "noplot_ztt_mc_inc")
		self.add_input("DYJetsToLL_M_50_madgraph_8TeV/*.root", "mt_os_dirIso_ztt_tauEsNom/ntuple", 19712.0, "eventWeight*(pt_2>30.0)*(lep1MetMt<30.0)", "noplot_ztt_mc")
		
		# ZL
		self.add_input("DYJetsToLL_M_50_madgraph_8TeV/*.root", "mt_os_dirIso_zl_tauEsNom/ntuple", 19712.0, "eventWeight*(pt_2>30.0)*(lep1MetMt<30.0)", "zl")
		
		# ZJ
		self.add_input("DYJetsToLL_M_50_madgraph_8TeV/*.root", "mt_os_dirIso_zj_tauEsNom/ntuple", 19712.0, "eventWeight*(pt_2>30.0)*(lep1MetMt<30.0)", "zj")
		
		# TTJets
		self.add_input("TTJets*_madgraph_tauola_8TeV/*.root", "mt_os_dirIso_z_tauEs/ntuple", 19712.0, "eventWeight*(pt_2>30.0)*(lep1MetMt<30.0)", "ttj")
		
		# Dibosons
		self.add_input("??_pythia_tauola_8TeV/*.root", "mt_os_dirIso_z_tauEs/ntuple", 19712.0, "eventWeight*(pt_2>30.0)*(lep1MetMt<30.0)", "diboson")
		
		# WJets
		self.add_input("WJetsToLN_madgraph_8TeV/*.root", "mt_os_dirIso_z_tauEs/ntuple", 19712.0, "eventWeight*(pt_2>30.0)*(lep1MetMt<30.0)", "wjets")
		self.add_input("Tau*_Run2012?_22Jan2013_8TeV/*.root", "mt_os_dirIso_z_tauEs/ntuple", 1.0, "eventWeight*(pt_2>30.0)*(lep1MetMt>70.0)", "noplot_wjets_data_control")
		self.add_input("DYJetsToLL_M_50_madgraph_8TeV/*.root", "mt_os_dirIso_ztt_tauEsNom/ntuple", 19712.0, "eventWeight*(pt_2>30.0)*(lep1MetMt>70.0)", "noplot_ztt_mc_wjet_control")
		self.add_input("DYJetsToLL_M_50_madgraph_8TeV/*.root", "mt_os_dirIso_zl_tauEsNom/ntuple mt_os_dirIso_zj_tauEsNom/ntuple", 19712.0, "eventWeight*(pt_2>30.0)*(lep1MetMt>70.0)", "noplot_zll_wjet_control")
		self.add_input("TTJets*_madgraph_tauola_8TeV/*.root", "mt_os_dirIso_z_tauEs/ntuple", 19712.0, "eventWeight*(pt_2>30.0)*(lep1MetMt>70.0)", "noplot_ttj_wjet_control")
		self.add_input("??_pythia_tauola_8TeV/*.root", "mt_os_dirIso_z_tauEs/ntuple", 19712.0, "eventWeight*(pt_2>30.0)*(lep1MetMt>70.0)", "noplot_diboson_wjet_control")
		self.add_input("WJetsToLN_madgraph_8TeV/*.root", "mt_os_dirIso_z_tauEs/ntuple", 19712.0, "eventWeight*(pt_2>30.0)*(lep1MetMt<30.0)", "noplot_wjets_mc_signal")
		self.add_input("WJetsToLN_madgraph_8TeV/*.root", "mt_os_dirIso_z_tauEs/ntuple", 19712.0, "eventWeight*(pt_2>30.0)*(lep1MetMt>70.0)", "noplot_wjets_mc_control")
		
		# WJets (SS, for substraction in QCD estimation)
		self.add_input("WJetsToLN_madgraph_8TeV/*.root", "mt_ss_dirIso_z_tauEs/ntuple", 19712.0, "eventWeight*(pt_2>30.0)*(lep1MetMt<30.0)", "noplot_wjets_ss")
		self.add_input("Tau*_Run2012?_22Jan2013_8TeV/*.root", "mt_ss_dirIso_z_tauEs/ntuple", 1.0, "eventWeight*(pt_2>30.0)*(lep1MetMt>70.0)", "noplot_wjets_ss_data_control")
		self.add_input("DYJetsToLL_M_50_madgraph_8TeV/*.root", "mt_ss_dirIso_ztt_tauEsNom/ntuple", 19712.0, "eventWeight*(pt_2>30.0)*(lep1MetMt>70.0)", "noplot_ztt_ss_mc_wjet_control")
		self.add_input("DYJetsToLL_M_50_madgraph_8TeV/*.root", "mt_ss_dirIso_zl_tauEsNom/ntuple mt_ss_dirIso_zj_tauEsNom/ntuple", 19712.0, "eventWeight*(pt_2>30.0)*(lep1MetMt>70.0)", "noplot_zll_ss_wjet_control")
		self.add_input("TTJets*_madgraph_tauola_8TeV/*.root", "mt_ss_dirIso_z_tauEs/ntuple", 19712.0, "eventWeight*(pt_2>30.0)*(lep1MetMt>70.0)", "noplot_ttj_ss_wjet_control")
		self.add_input("??_pythia_tauola_8TeV/*.root", "mt_ss_dirIso_z_tauEs/ntuple", 19712.0, "eventWeight*(pt_2>30.0)*(lep1MetMt>70.0)", "noplot_diboson_ss_wjet_control")
		self.add_input("WJetsToLN_madgraph_8TeV/*.root", "mt_ss_dirIso_z_tauEs/ntuple", 19712.0, "eventWeight*(pt_2>30.0)*(lep1MetMt<30.0)", "noplot_wjets_ss_mc_signal")
		self.add_input("WJetsToLN_madgraph_8TeV/*.root", "mt_ss_dirIso_z_tauEs/ntuple", 19712.0, "eventWeight*(pt_2>30.0)*(lep1MetMt>70.0)", "noplot_wjets_ss_mc_control")
		
		# QCD
		self.add_input("Tau*_Run2012?_22Jan2013_8TeV/*.root", "mt_ss_dirIso_z_tauEs/ntuple", 1.0, "eventWeight*(pt_2>30.0)*(lep1MetMt<30.0)", "qcd")
		self.add_input("DYJetsToLL_M_50_madgraph_8TeV/*.root", "mt_ss_dirIso_ztt_tauEsNom/ntuple", 19712.0, "eventWeight*(pt_2>30.0)*(lep1MetMt<30.0)", "noplot_ztt_mc_qcd_control")
		self.add_input("DYJetsToLL_M_50_madgraph_8TeV/*.root", "mt_ss_dirIso_zl_tauEsNom/ntuple mt_ss_dirIso_zj_tauEsNom/ntuple", 19712.0, "eventWeight*(pt_2>30.0)*(lep1MetMt<30.0)", "noplot_zll_qcd_control")
		self.add_input("TTJets*_madgraph_tauola_8TeV/*.root", "mt_ss_dirIso_z_tauEs/ntuple", 19712.0, "eventWeight*(pt_2>30.0)*(lep1MetMt<30.0)", "noplot_ttj_qcd_control")
		self.add_input("??_pythia_tauola_8TeV/*.root", "mt_ss_dirIso_z_tauEs/ntuple", 19712.0, "eventWeight*(pt_2>30.0)*(lep1MetMt<30.0)", "noplot_diboson_qcd_control")
		
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

