
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import sys
from pprint import pprint

class CutStringsDict:
	
	@staticmethod
	def baseline(channel, cut_type):
		cuts = {}
		if channel == "gen":
			cuts ={}
		else:
			cuts["blind"] = "{blind}"
			cuts["os"] = "((q_1*q_2)<0.0)"

		if channel == "mm":
			if "mssm" in cut_type:
				cuts["trg"] = "(trg_singlemuon == 1)"

			elif "smhtt2016" in cut_type or "cp2016" in cut_type or "cpggh2016" in cut_type:
				cuts["pt_1"] = "(pt_1 > 25.0)"
				cuts["pt_2"] = "(pt_2 > 25.0)"
				cuts["eta_1"] = "(abs(eta_1) < 2.1)"
				cuts["eta_2"] = "(abs(eta_2) < 2.1)"
			cuts["extra_lepton_veto"] = "(extraelec_veto < 0.5)*(extramuon_veto < 0.5)"
			cuts["iso_1"] = "(iso_1 < 0.15)"
			cuts["iso_2"] = "(iso_2 < 0.15)"
			cuts["m_vis"] = "(m_vis > 70.0)*(m_vis < 110.0)"

		elif channel == "ee":
			if "mssm" in cut_type:
				cuts["trg"] = "(trg_singleelectron == 1)"
			cuts["extra_lepton_veto"] = "(extraelec_veto < 0.5)*(extramuon_veto < 0.5)"
			cuts["iso_1"] = "(iso_1 < 0.1)"
			cuts["iso_2"] = "(iso_2 < 0.1)"
			cuts["m_vis"] = "(m_vis > 60.0)*(m_vis < 120.0)"

		elif channel == "em" or channel == "ttbar":
			if "mssm" in cut_type:
				cuts["trg"] = "(trg_muonelectron == 1)"

			elif ("smhtt2016" in cut_type or "cp2016" in cut_type or "cpggh2016" in cut_type) and channel == "em":
				cuts["bveto"] = "(nbtag == 0)"
				cuts["pt_1"] = "(pt_1 > 13.0)"
				cuts["pt_2"] = "(pt_2 > 10.0)"
				# used to remove overlap with H->WW->emu analysis
				cuts["diLepMetMt"] = "(diLepMetMt < 60.0)"
			cuts["pzeta"] = "(pZetaMissVis > -35.0)" if "2016" in cut_type and not "mssm" in cut_type else "(pZetaMissVis > -40.0)"
			if "mssm" in cut_type:
				cuts["pzeta"] = "(pZetaMissVis > -50.0)"
			cuts["extra_lepton_veto"] = "(extraelec_veto < 0.5)*(extramuon_veto < 0.5)"
			cuts["iso_1"] = "(iso_1 < 0.15)"
			cuts["iso_2"] = "(iso_2 < 0.2)" if "2016" in cut_type else "(iso_2 < 0.15)"

		elif channel == "mt":
			if "mssm" in cut_type:
				cuts["trg"] = "(trg_singlemuon == 1)"

			elif "smhtt2016" in cut_type or "cp2016" in cut_type or "cpggh2016" in cut_type:
				# trigger weights are saved as optional weights, and thus need to be applied here
				cuts["trg"] = "((trg_mutaucross == 1)*(triggerWeight_muTauCross_1)*(triggerWeight_muTauCross_2)*(pt_1 <= 23)+(trg_singlemuon == 1)*(triggerWeight_singleMu_1)*(pt_1 > 23))"
				cuts["pt_1"] = "(pt_1 > 20.0)"
				cuts["pt_2"] = "(pt_2 > 30.0)"


			cuts["mt"] = "(mt_1<40.0)" if "mssm2016" in cut_type else "(mt_1<30.0)" if "mssm" in cut_type else "(mt_1<50.0)" if "2016" in cut_type else "(mt_1<40.0)" #TODO 2017
			cuts["anti_e_tau_discriminators"] = "(againstElectronVLooseMVA6_2 > 0.5)"
			cuts["anti_mu_tau_discriminators"] = "(againstMuonTight3_2 > 0.5)"
			cuts["extra_lepton_veto"] = "(extraelec_veto < 0.5)*(extramuon_veto < 0.5)"
			cuts["dilepton_veto"] = "(dilepton_veto < 0.5)"
			cuts["iso_1"] = "(iso_1 < 0.15)" if "2016" in cut_type else "(iso_1 < 0.1)"    #TODO 2017

			if "2017" in cut_type:
				cuts["trigger"] = "((trg_singlemuon_24>0.5)||(trg_singlemuon_27>0.5)||(trg_crossmuon_mu20tau27>0.5))"
				cuts["iso_1"] = "(iso_1 < 0.15)"
				cuts["iso_2"] = "(byTightIsolationMVArun2017v2DBoldDMwLT2017_2 > 0.5)*((gen_match_2 == 5)*0.87 + (gen_match_2 != 5))" 
				cuts["pt_1"] = "(pt_1 > 25.0)"
				cuts["pt_2"] = "(pt_2 > 30.0)"
				cuts["mt"] = "(mt_1<50.0)"
			else:
				cuts["iso_2"] = "(byMediumIsolationMVArun2v1DBoldDMwLT_2 > 0.5)*((gen_match_2 == 5)*0.97 + (gen_match_2 != 5))" if "mssm2016" in cut_type else "(byTightIsolationMVArun2v1DBoldDMwLT_2 > 0.5)*((gen_match_2 == 5)*0.95 + (gen_match_2 != 5))" if "2016" in cut_type else "(byTightIsolationMVArun2v1DBoldDMwLT_2 > 0.5)"

		elif channel == "et":
			if "mssm" in cut_type:
				cuts["trg"] = "(trg_singleelectron == 1)"

			elif "smhtt2016" in cut_type or "cp2016" in cut_type or "cpggh2016" in cut_type:
				cuts["pt_1"] = "(pt_1 > 25.0)"
				cuts["pt_2"] = "(pt_2 > 30.0)"
			elif "smhtt2017" in cut_type or "cp2017" in cut_type or "cpggh2017" in cut_type:  #TODO pt_1 set to 37 might change, pt_2 at 25 might change
				cuts["pt_1"] = "(pt_1 > 25.0)"
				cuts["pt_2"] = "(pt_2 > 25.0)"  
			cuts["mt"] = "(mt_1<50.0)" if "2016" in cut_type else "(mt_1<40.0)"
			cuts["anti_e_tau_discriminators"] = "(againstElectronTightMVA6_2 > 0.5)"
			cuts["anti_mu_tau_discriminators"] = "(againstMuonLoose3_2 > 0.5)"
			cuts["extra_lepton_veto"] = "(extraelec_veto < 0.5)*(extramuon_veto < 0.5)"
			cuts["dilepton_veto"] = "(dilepton_veto < 0.5)"
			cuts["iso_1"] = "(iso_1 < 0.1)"
			if "2017" in cut_type:
				cuts["trigger"] = "(((trg_singleelectron_35>0.5)*(pt_1>36))||((trg_crosselectron_ele24tau30>0.5)*(pt_1>25)*(pt_2>35))||((trg_singleelectron_27>0.5)*(pt_1>28))||((trg_singleelectron_32>0.5)*(pt_1>33))|| ((trg_singleelectron_32_fallback>0.5)*(pt_1>33)))"
				cuts["iso_2"] = "(byTightIsolationMVArun2017v2DBoldDMwLT2017_2 > 0.5)*((gen_match_2 == 5)*0.87 + (gen_match_2 != 5))" #TODO add byTightIsolationMVArun2v1DBoldDMwLT_2, 0.87 = tauid sf tight
				cuts["mt"] = "(mt_1<50.0)"
			else:
				cuts["iso_2"] = "(byMediumIsolationMVArun2v1DBoldDMwLT_2 > 0.5)*((gen_match_2 == 5)*0.97 + (gen_match_2 != 5))" if "mssm2016" in cut_type else "(byTightIsolationMVArun2v1DBoldDMwLT_2 > 0.5)*((gen_match_2 == 5)*0.95 + (gen_match_2 != 5))" if "2016" in cut_type else "(byTightIsolationMVArun2v1DBoldDMwLT_2 > 0.5)"

		elif channel == "tt":
			if "mssm" in cut_type:
				cuts["trg"] = "(trg_doubletau == 1)"

			elif "smhtt2016" in cut_type or "cp2016" in cut_type or "cpggh2016" in cut_type:  #TODO 2017
				cuts["pt_1"] = "(pt_1 > 50.0)"
				cuts["pt_2"] = "(pt_2 > 40.0)"
			cuts["extra_lepton_veto"] = "(extraelec_veto < 0.5)*(extramuon_veto < 0.5)"
			cuts["anti_e_tau_discriminators"] = "(againstElectronVLooseMVA6_1 > 0.5)*(againstElectronVLooseMVA6_2 > 0.5)"
			cuts["anti_mu_tau_discriminators"] = "(againstMuonLoose3_1 > 0.5)*(againstMuonLoose3_2 > 0.5)"
			if "2017" in cut_type:
				cuts["iso_1"] = "(byTightIsolationMVArun2017v2DBoldDMwLT2017_1 > 0.5)*((gen_match_1 == 5)*0.89 + (gen_match_1 != 5))"
				cuts["iso_2"] = "(byTightIsolationMVArun2017v2DBoldDMwLT2017_2 > 0.5)*((gen_match_2 == 5)*0.89 + (gen_match_2 != 5))"
			else:
				cuts["iso_1"] = "(byTightIsolationMVArun2v1DBoldDMwLT_1 > 0.5)*((gen_match_1 == 5)*0.95 + (gen_match_1 != 5))" if "2016" in cut_type else "(byVTightIsolationMVArun2v1DBoldDMwLT_2 > 0.5)"  #TODO 2017
				cuts["iso_2"] = "(byTightIsolationMVArun2v1DBoldDMwLT_2 > 0.5)*((gen_match_2 == 5)*0.95 + (gen_match_2 != 5))" if "2016" in cut_type else "(byVTightIsolationMVArun2v1DBoldDMwLT_2 > 0.5)"  #TODO 2017
		else:
			log.fatal("No cut values implemented for channel \"%s\" in \"%s\"" % (channel, cut_type))
			sys.exit(1)
		return cuts
	
	@staticmethod
	def mssm2016(channel, cut_type):
		cuts = CutStringsDict.baseline(channel, cut_type)
		if channel == "mt":
			iso_2_cut = ""
			if cut_type == "mssm2016fflooseiso":
				iso_2_cut = "(byTightIsolationMVArun2v1DBoldDMwLT_2 < 0.5)*(byMediumIsolationMVArun2v1DBoldDMwLT_2 > 0.5)*((gen_match_2 == 5)*0.97 + (gen_match_2 != 5))"
			elif cut_type == "mssm2016fffull":
				iso_2_cut = "(byMediumIsolationMVArun2v1DBoldDMwLT_2 > 0.5)*((gen_match_2 == 5)*0.97 + (gen_match_2 != 5))"
			elif cut_type == "mssm2016looseiso":
				iso_2_cut = "(byTightIsolationMVArun2v1DBoldDMwLT_2 < 0.5)*(byLooseIsolationMVArun2v1DBoldDMwLT_2 > 0.5)*((gen_match_2 == 5)*0.99 + (gen_match_2 != 5))"
			elif cut_type in ["mssm2016loosemt", "mssm2016tight"]:
				iso_2_cut = "(byTightIsolationMVArun2v1DBoldDMwLT_2 > 0.5)*((gen_match_2 == 5)*0.95 + (gen_match_2 != 5))"
			else:
				iso_2_cut = "(byLooseIsolationMVArun2v1DBoldDMwLT_2 > 0.5)*((gen_match_2 == 5)*0.99 + (gen_match_2 != 5))"
			cuts["mt"] = "(mt_1<40.0)" if cut_type == "mssm2016tight" else "(mt_1>40.0)*(mt_1<70.0)" if cut_type == "mssm2016loosemt" else "(mt_1<70.0)"
			cuts["iso_2"] = iso_2_cut 
		elif channel == "et":
			iso_2_cut = ""
			if cut_type == "mssm2016fflooseiso":
				iso_2_cut = "(byTightIsolationMVArun2v1DBoldDMwLT_2 < 0.5)*(byMediumIsolationMVArun2v1DBoldDMwLT_2 > 0.5)*((gen_match_2 == 5)*0.97 + (gen_match_2 != 5))"
			elif cut_type == "mssm2016fffull":
				iso_2_cut = "(byMediumIsolationMVArun2v1DBoldDMwLT_2 > 0.5)*((gen_match_2 == 5)*0.97 + (gen_match_2 != 5))"
			elif cut_type == "mssm2016looseiso":
				iso_2_cut = "(byTightIsolationMVArun2v1DBoldDMwLT_2 < 0.5)*(byLooseIsolationMVArun2v1DBoldDMwLT_2 > 0.5)*((gen_match_2 == 5)*0.99 + (gen_match_2 != 5))"
			elif cut_type in ["mssm2016loosemt", "mssm2016tight"]:
				iso_2_cut = "(byTightIsolationMVArun2v1DBoldDMwLT_2 > 0.5)*((gen_match_2 == 5)*0.95 + (gen_match_2 != 5))"
			else:
				iso_2_cut = "(byLooseIsolationMVArun2v1DBoldDMwLT_2 > 0.5)*((gen_match_2 == 5)*0.99 + (gen_match_2 != 5))"
			cuts["mt"] = "(mt_1<40.0)" if cut_type == "mssm2016tight" else "(mt_1>40.0)*(mt_1<70.0)" if cut_type == "mssm2016loosemt" else "(mt_1<70.0)"
			cuts["iso_2"] = iso_2_cut
		return cuts
	
	@staticmethod
	def cpggh2016(channel, cut_type):
		cuts = CutStringsDict.baseline(channel, cut_type)
		if channel == "mm":		
			cuts["pt_1"] = "(pt_1 > 25.0)"
			cuts["pt_2"] = "(pt_2 > 25.0)"
			cuts["eta_1"] = "(abs(eta_1) < 2.1)"
			cuts["eta_2"] = "(abs(eta_2) < 2.1)"					
		elif channel == "em":
			cuts["bveto"] = "(nbtag == 0)"
			cuts["pt_1"] = "(pt_1 > 13.0)"
			cuts["pt_2"] = "(pt_2 > 10.0)"
			# used to remove overlap with H->WW->emu analysis
			cuts["diLepMetMt"] = "(diLepMetMt < 60.0)"
		elif channel == "mt":
			cuts["trg"] = "((trg_mutaucross == 1)*(triggerWeight_muTauCross_1)*(triggerWeight_muTauCross_2)*(pt_1 <= 23)+(trg_singlemuon == 1)*(triggerWeight_singleMu_1)*(pt_1 > 23))"
			cuts["pt_1"] = "(pt_1 > 20.0)"
			cuts["pt_2"] = "(pt_2 > 30.0)"
			cuts["mt"] = "(mt_1<50.0)"					
			cuts["iso_1"] = "(iso_1 < 0.15)"
			cuts["iso_2"] = "(byTightIsolationMVArun2v1DBoldDMwLT_2 > 0.5)*((gen_match_2 == 5)*0.95 + (gen_match_2 != 5))"
		elif channel == "et":
			cuts["pt_1"] = "(pt_1 > 25.0)"
			cuts["pt_2"] = "(pt_2 > 30.0)"	
			cuts["mt"] = "(mt_1<50.0)"	
			cuts["iso_1"] = "(iso_1 < 0.1)"
			cuts["iso_2"] = "(byTightIsolationMVArun2v1DBoldDMwLT_2 > 0.5)*((gen_match_2 == 5)*0.95 + (gen_match_2 != 5))"
		elif channel == "tt":
			cuts["pt_1"] = "(pt_1 > 50.0)"
			cuts["pt_2"] = "(pt_2 > 40.0)"
			cuts["iso_1"] = "(byTightIsolationMVArun2v1DBoldDMwLT_1 > 0.5)*((gen_match_1 == 5)*0.95 + (gen_match_1 != 5))"									
			cuts["iso_2"] = "(byTightIsolationMVArun2v1DBoldDMwLT_2 > 0.5)*((gen_match_2 == 5)*0.95 + (gen_match_2 != 5))"
		return cuts

	@staticmethod
	def cpggh2017(channel, cut_type):
		cuts = CutStringsDict.baseline(channel, cut_type)
		if channel == "mm":		
			cuts["pt_1"] = "(pt_1 > 25.0)"
			cuts["pt_2"] = "(pt_2 > 25.0)"
			cuts["eta_1"] = "(abs(eta_1) < 2.1)"
			cuts["eta_2"] = "(abs(eta_2) < 2.1)"					
		elif channel == "em":
			cuts["bveto"] = "(nbtag == 0)"
			cuts["pt_1"] = "(pt_1 > 13.0)"
			cuts["pt_2"] = "(pt_2 > 10.0)"
			# used to remove overlap with H->WW->emu analysis
			cuts["diLepMetMt"] = "(diLepMetMt < 60.0)"
		elif channel == "mt":
			#cuts["trigger"] = "((trg_singlemuon_24>0.5)||(trg_singlemuon_27>0.5)||(trg_crossmuon_mu20tau27>0.5))"
			cuts["pt_1"] = "(pt_1 > 20.0)"
			cuts["pt_2"] = "(pt_2 > 30.0)"
			cuts["mt"] = "(mt_1<50.0)"					
			cuts["iso_1"] = "(iso_1 < 0.15)"
			cuts["iso_2"] = "(byTightIsolationMVArun2017v2DBoldDMwLT2017_2 > 0.5)*((gen_match_2 == 5)*0.87 + (gen_match_2 != 5))"
		elif channel == "et":
			cuts["pt_1"] = "(pt_1 > 25.0)"
			cuts["pt_2"] = "(pt_2 > 30.0)"	
			cuts["mt"] = "(mt_1<50.0)"	
			cuts["iso_1"] = "(iso_1 < 0.1)"
			cuts["iso_2"] = "(byTightIsolationMVArun2017v2DBoldDMwLT2017_2 > 0.5)*((gen_match_2 == 5)*0.87 + (gen_match_2 != 5))"
		elif channel == "tt":
			cuts["pt_1"] = "(pt_1 > 50.0)"
			cuts["pt_2"] = "(pt_2 > 40.0)"
			cuts["iso_1"] = "(byTightIsolationMVArun2v1DBoldDMwLT_1 > 0.5)*((gen_match_1 == 5)*0.95 + (gen_match_1 != 5))"									
			cuts["iso_2"] = "(byTightIsolationMVArun2v1DBoldDMwLT_2 > 0.5)*((gen_match_2 == 5)*0.95 + (gen_match_2 != 5))"
		cuts["generatorweight"] = "(1/generatorWeight)" #TODO
		return cuts


	@staticmethod
	def lfv(channel, cut_type):
		cuts = CutStringsDict.baseline(channel, cut_type)
		#cuts["nbtag"] = "nbtag==0"
		#cuts["mt"] = ""
			
		return cuts
			
	
	@staticmethod
	def antievloosepass(channel, cut_type):
		if channel == "et":
			cuts = CutStringsDict.baseline(channel, cut_type)
			cuts["mt"] = "(mt_1 < 30.0)"
			cuts["iso_2"] = "(byTightIsolationMVArun2017v2DBoldDMwLT2017_2 > 0.5)*((gen_match_2 == 5)*0.85 + (gen_match_2 != 5))"  if "2017" in cut_type else  "(byTightIsolationMVArun2v1DBoldDMwLT_2 > 0.5)"
			cuts["discriminator"] = "(againstElectronVLooseMVA6_2 > 0.5)"
		else:
			log.fatal("No cut values implemented for channel \"%s\" in \"%s\"" % (channel, cut_type))
			sys.exit(1)
		return cuts
	
	@staticmethod
	def antievloosefail(channel, cut_type):
		if channel == "et":
			cuts = CutStringsDict.baseline(channel, cut_type)
			cuts["mt"] = "(mt_1 < 30.0)"
			cuts["iso_2"] = "(byTightIsolationMVArun2017v2DBoldDMwLT2017_2 > 0.5)*((gen_match_2 == 5)*0.85 + (gen_match_2 != 5))"  if "2017" in cut_type  else  "(byTightIsolationMVArun2v1DBoldDMwLT_2 > 0.5)"
			cuts["discriminator"] = "(againstElectronVLooseMVA6_2 < 0.5)"
		else:
			log.fatal("No cut values implemented for channel \"%s\" in \"%s\"" % (channel, cut_type))
			sys.exit(1)
		return cuts
	
	@staticmethod
	def antieloosepass(channel, cut_type):
		if channel == "et":
			cuts = CutStringsDict.baseline(channel, cut_type)
			cuts["mt"] = "(mt_1 < 30.0)"
			cuts["iso_2"] = "(byTightIsolationMVArun2017v2DBoldDMwLT2017_2 > 0.5)*((gen_match_2 == 5)*0.89 + (gen_match_2 != 5))"  if "2017" in cut_type  else  "(byTightIsolationMVArun2v1DBoldDMwLT_2 > 0.5)"
			cuts["discriminator"] = "(againstElectronLooseMVA6_2 > 0.5)"
		else:
			log.fatal("No cut values implemented for channel \"%s\" in \"%s\"" % (channel, cut_type))
			sys.exit(1)
		return cuts
	
	@staticmethod
	def antieloosefail(channel, cut_type):
		if channel == "et":
			cuts = CutStringsDict.baseline(channel, cut_type)
			cuts["mt"] = "(mt_1 < 30.0)"
			cuts["iso_2"] = "(byTightIsolationMVArun2017v2DBoldDMwLT2017_2 > 0.5)*((gen_match_2 == 5)*0.89 + (gen_match_2 != 5))"  if "2017" in cut_type  else  "(byTightIsolationMVArun2v1DBoldDMwLT_2 > 0.5)"
			cuts["discriminator"] = "(againstElectronLooseMVA6_2 < 0.5)"
		else:
			log.fatal("No cut values implemented for channel \"%s\" in \"%s\"" % (channel, cut_type))
			sys.exit(1)
		return cuts
	
	@staticmethod
	def antiemediumpass(channel, cut_type):
		if channel == "et":
			cuts = CutStringsDict.baseline(channel, cut_type)
			cuts["mt"] = "(mt_1 < 30.0)"
			cuts["iso_2"] = "(byTightIsolationMVArun2017v2DBoldDMwLT2017_2 > 0.5)*((gen_match_2 == 5)*0.89 + (gen_match_2 != 5))"  if "2017" in cut_type  else  "(byTightIsolationMVArun2v1DBoldDMwLT_2 > 0.5)"
			cuts["discriminator"] = "(againstElectronMediumMVA6_2 > 0.5)"
		else:
			log.fatal("No cut values implemented for channel \"%s\" in \"%s\"" % (channel, cut_type))
			sys.exit(1)
		return cuts
	
	@staticmethod
	def antiemediumfail(channel, cut_type):
		if channel == "et":
			cuts = CutStringsDict.baseline(channel, cut_type)
			cuts["mt"] = "(mt_1 < 30.0)"
			cuts["iso_2"] = "(byTightIsolationMVArun2017v2DBoldDMwLT2017_2 > 0.5)*((gen_match_2 == 5)*0.89 + (gen_match_2 != 5))"  if "2017" in cut_type  else  "(byTightIsolationMVArun2v1DBoldDMwLT_2 > 0.5)"
			cuts["discriminator"] = "(againstElectronMediumMVA6_2 < 0.5)"
		else:
			log.fatal("No cut values implemented for channel \"%s\" in \"%s\"" % (channel, cut_type))
			sys.exit(1)
		return cuts
	
	@staticmethod
	def antietightpass(channel, cut_type):
		if channel == "et":
			cuts = CutStringsDict.baseline(channel, cut_type)
			cuts["mt"] = "(mt_1 < 30.0)"
			cuts["iso_2"] = "(byTightIsolationMVArun2017v2DBoldDMwLT2017_2 > 0.5)*((gen_match_2 == 5)*0.87 + (gen_match_2 != 5))"  if "2017" in cut_type  else  "(byTightIsolationMVArun2v1DBoldDMwLT_2 > 0.5)"
			cuts["discriminator"] = "(againstElectronTightMVA6_2 > 0.5)"
		else:
			log.fatal("No cut values implemented for channel \"%s\" in \"%s\"" % (channel, cut_type))
			sys.exit(1)
		return cuts
	
	@staticmethod
	def antietightfail(channel, cut_type):
		if channel == "et":
			cuts = CutStringsDict.baseline(channel, cut_type)
			cuts["mt"] = "(mt_1 < 30.0)"
			cuts["iso_2"] = "(byTightIsolationMVArun2017v2DBoldDMwLT2017_2 > 0.5)*((gen_match_2 == 5)*0.87 + (gen_match_2 != 5))"  if "2017" in cut_type  else  "(byTightIsolationMVArun2v1DBoldDMwLT_2 > 0.5)"
			cuts["discriminator"] = "(againstElectronTightMVA6_2 < 0.5)"
		else:
			log.fatal("No cut values implemented for channel \"%s\" in \"%s\"" % (channel, cut_type))
			sys.exit(1)
		return cuts
	
	@staticmethod
	def antievtightpass(channel, cut_type):
		if channel == "et":
			cuts = CutStringsDict.baseline(channel, cut_type)
			cuts["mt"] = "(mt_1 < 30.0)"
			cuts["iso_2"] = "(byTightIsolationMVArun2017v2DBoldDMwLT2017_2 > 0.5)*((gen_match_2 == 5)*0.85 + (gen_match_2 != 5))"  if "2017" in cut_type else  "(byTightIsolationMVArun2v1DBoldDMwLT_2 > 0.5)"
			cuts["discriminator"] = "(againstElectronVTightMVA6_2 > 0.5)"
		else:
			log.fatal("No cut values implemented for channel \"%s\" in \"%s\"" % (channel, cut_type))
			sys.exit(1)
		return cuts
	
	@staticmethod
	def antievtightfail(channel, cut_type):
		if channel == "et":
			cuts = CutStringsDict.baseline(channel, cut_type)
			cuts["mt"] = "(mt_1 < 30.0)"
			cuts["iso_2"] = "(byTightIsolationMVArun2017v2DBoldDMwLT2017_2 > 0.5)*((gen_match_2 == 5)*0.85 + (gen_match_2 != 5))"  if "2017" in cut_type else  "(byTightIsolationMVArun2v1DBoldDMwLT_2 > 0.5)"
			cuts["discriminator"] = "(againstElectronVTightMVA6_2 < 0.5)"
		else:
			log.fatal("No cut values implemented for channel \"%s\" in \"%s\"" % (channel, cut_type))
			sys.exit(1)
		return cuts

	@staticmethod
	def antieinclusive(channel, cut_type):
		if channel == "et":
			cuts = CutStringsDict.baseline(channel, cut_type)
			cuts["mt"] = "(mt_1 < 30.0)"
			cuts["iso_2"] = "(byTightIsolationMVArun2017v2DBoldDMwLT2017_2 > 0.5)" if "2017" in cut_type else  "(byTightIsolationMVArun2v1DBoldDMwLT_2 > 0.5)"
		else:
			log.fatal("No cut values implemented for channel \"%s\" in \"%s\"" % (channel, cut_type))
			sys.exit(1)
		return cuts
	
	@staticmethod
	def antimuloosepass(channel, cut_type):
		if channel == "mt":
			cuts = CutStringsDict.baseline(channel, cut_type)
			cuts["pzeta"] = "(pZetaMissVis > -20.0)"
			cuts["discriminator"] = "(againstMuonLoose3_2 > 0.5)"
		else:
			log.fatal("No cut values implemented for channel \"%s\" in \"%s\"" % (channel, cut_type))
			sys.exit(1)
		return cuts
	
	@staticmethod
	def antimuloosefail(channel, cut_type):
		if channel == "mt":
			cuts = CutStringsDict.baseline(channel, cut_type)
			#cuts["pzeta"] = "(pZetaMissVis > -20.0)"
			cuts["discriminator"] = "(againstMuonLoose3_2 < 0.5)"
		else:
			log.fatal("No cut values implemented for channel \"%s\" in \"%s\"" % (channel, cut_type))
			sys.exit(1)
		return cuts
	
	@staticmethod
	def antimutightpass(channel, cut_type):
		if channel == "mt":
			cuts = CutStringsDict.baseline(channel, cut_type)
			#cuts["pzeta"] = "(pZetaMissVis > -20.0)"
			cuts["discriminator"] = "(againstMuonTight3_2 > 0.5)"
		else:
			log.fatal("No cut values implemented for channel \"%s\" in \"%s\"" % (channel, cut_type))
			sys.exit(1)
		return cuts
	
	@staticmethod
	def antimutightfail(channel, cut_type):
		if channel == "mt":
			cuts = CutStringsDict.baseline(channel, cut_type)
			#cuts["pzeta"] = "(pZetaMissVis > -20.0)"
			cuts["discriminator"] = "(againstMuonTight3_2 < 0.5)"
		else:
			log.fatal("No cut values implemented for channel \"%s\" in \"%s\"" % (channel, cut_type))
			sys.exit(1)
		return cuts
	
	@staticmethod
	def tauidloosepass(channel, cut_type):
		if channel in ["mt", "et"]:
			cuts = CutStringsDict.baseline(channel, cut_type)
			cuts["pzeta"] = "(pZetaMissVis > -25.0)"
			cuts["bveto"] = "(nbtag == 0)"
			cuts["discriminator"] = "(byLooseIsolationMVArun2v1DBoldDMwLT_2 > 0.5)"
		else:
			log.fatal("No cut values implemented for channel \"%s\" in \"%s\"" % (channel, cut_type))
			sys.exit(1)
		return cuts
	
	@staticmethod
	def tauidloosefail(channel, cut_type):
		if channel in ["mt", "et"]:
			cuts = CutStringsDict.baseline(channel, cut_type)
			cuts["pzeta"] = "(pZetaMissVis > -25.0)"
			cuts["bveto"] = "(nbtag == 0)"
			cuts["discriminator"] = "(byLooseIsolationMVArun2v1DBoldDMwLT_2 < 0.5)"
		else:
			log.fatal("No cut values implemented for channel \"%s\" in \"%s\"" % (channel, cut_type))
			sys.exit(1)
		return cuts
	
	@staticmethod
	def tauidmediumpass(channel, cut_type):
		if channel in ["mt", "et"]:
			cuts = CutStringsDict.baseline(channel, cut_type)
			cuts["pzeta"] = "(pZetaMissVis > -25.0)"
			cuts["bveto"] = "(nbtag == 0)"
			cuts["discriminator"] = "(byMediumIsolationMVArun2v1DBoldDMwLT_2 > 0.5)"
		else:
			log.fatal("No cut values implemented for channel \"%s\" in \"%s\"" % (channel, cut_type))
			sys.exit(1)
		return cuts
	
	@staticmethod
	def tauidmediumfail(channel, cut_type):
		if channel in ["mt", "et"]:
			cuts = CutStringsDict.baseline(channel, cut_type)
			cuts["pzeta"] = "(pZetaMissVis > -25.0)"
			cuts["bveto"] = "(nbtag == 0)"
			cuts["discriminator"] = "(byMediumIsolationMVArun2v1DBoldDMwLT_2 < 0.5)"
		else:
			log.fatal("No cut values implemented for channel \"%s\" in \"%s\"" % (channel, cut_type))
			sys.exit(1)
		return cuts
	
	@staticmethod
	def tauidtightpass(channel, cut_type):
		if channel in ["mt", "et"]:
			cuts = CutStringsDict.baseline(channel, cut_type)
			cuts["pzeta"] = "(pZetaMissVis > -25.0)"
			cuts["bveto"] = "(nbtag == 0)"
			cuts["discriminator"] = "(byTightIsolationMVArun2v1DBoldDMwLT_2 > 0.5)"
		else:
			log.fatal("No cut values implemented for channel \"%s\" in \"%s\"" % (channel, cut_type))
			sys.exit(1)
		return cuts
	
	@staticmethod
	def tauidtightfail(channel, cut_type):
		if channel in ["mt", "et"]:
			cuts = CutStringsDict.baseline(channel, cut_type)
			cuts["pzeta"] = "(pZetaMissVis > -25.0)"
			cuts["bveto"] = "(nbtag == 0)"
			cuts["discriminator"] = "(byTightIsolationMVArun2v1DBoldDMwLT_2 < 0.5)"
		else:
			log.fatal("No cut values implemented for channel \"%s\" in \"%s\"" % (channel, cut_type))
			sys.exit(1)
		return cuts
	
	@staticmethod
	def tauidvtightpass(channel, cut_type):
		if channel in ["mt", "et"]:
			cuts = CutStringsDict.baseline(channel, cut_type)
			cuts["pzeta"] = "(pZetaMissVis > -25.0)"
			cuts["bveto"] = "(nbtag == 0)"
			cuts["discriminator"] = "(byVTightIsolationMVArun2v1DBoldDMwLT_2 > 0.5)"
		else:
			log.fatal("No cut values implemented for channel \"%s\" in \"%s\"" % (channel, cut_type))
			sys.exit(1)
		return cuts
	
	@staticmethod
	def tauidvtightfail(channel, cut_type):
		if channel in ["mt", "et"]:
			cuts = CutStringsDict.baseline(channel, cut_type)
			cuts["pzeta"] = "(pZetaMissVis > -25.0)"
			cuts["bveto"] = "(nbtag == 0)"
			cuts["discriminator"] = "(byVTightIsolationMVArun2v1DBoldDMwLT_2 < 0.5)"
		else:
			log.fatal("No cut values implemented for channel \"%s\" in \"%s\"" % (channel, cut_type))
			sys.exit(1)
		return cuts
	
	@staticmethod
	def tauescuts(channel, cut_type):
		if channel in ["mt", "et"]:
			cuts = CutStringsDict.baseline(channel, cut_type)
			if "2016" in cut_type:
				cuts["mt"] = "(mt_1<30.0)"
				cuts["iso_2"] = "(byVTightIsolationMVArun2v1DBoldDMwLT_2 > 0.5)*((gen_match_2 == 5)*0.95 + (gen_match_2 != 5))"
				if channel == "mt":
					cuts["trg"] = "((trg_singlemuon22 == 1)*(triggerWeight_singleMu22_1)*(pt_1 > 23)*(abs(eta_1) < 2.1) + (trg_singlemuon24 == 1)*(triggerWeight_singleMu24_1)*(pt_1 > 25)*(abs(eta_1) > 2.1))"
			if not "2016" in cut_type:
				# the cuts below lead to W+jets being estimated to zero
				# with new background estimation technique
				cuts["pzeta"] = "(pZetaMissVis > -25.0)"
				cuts["bveto"] = "(nbtag == 0)"
		else:
			log.fatal("No cut values implemented for channel \"%s\" in \"%s\"" % (channel, cut_type))
			sys.exit(1)
		return cuts

	@staticmethod
	def relaxedETauMuTauWJ(channel, cut_type):
		if channel in ["mt", "et"]:
			cuts = CutStringsDict._get_cutdict(channel, cut_type.replace("relaxedETauMuTauWJ",""))
			cuts["iso_1"] = "(iso_1 < 0.3)"
			cuts["iso_2"] = "(byMediumIsolationMVArun2v1DBoldDMwLT_2 > 0.5)*((gen_match_2 == 5)*0.95 + (gen_match_2 != 5))" if "smhtt2016" in cut_type else "(byMediumIsolationMVArun2v1DBoldDMwLT_2 > 0.5)*((gen_match_2 == 5)*0.97 + (gen_match_2 != 5))" if "2016" in cut_type else "(byLooseIsolationMVArun2017v2DBoldDMwLT2017_2 > 0.5)"
		elif channel in ["em", "ttbar"]:
			cuts = CutStringsDict.baseline(channel, cut_type)
			cuts["iso_1"] = "(iso_1 < 0.3)"
			cuts["iso_2"] = "(iso_2 < 0.3)"
		else:
			log.fatal("No cut values implemented for channel \"%s\" in \"%s\"" % (channel, cut_type))
			sys.exit(1)
		return cuts

	@staticmethod
	def antiIsolationRegionQCD(channel, cut_type):
		if channel in ["mt", "et"]:
			cuts = CutStringsDict._get_cutdict(channel, cut_type.replace("relaxedETauMuTauWJ",""))
			cuts["iso_1"] = " ".join("(iso_1 < 0.3)*(iso_1>0.1)" if channel == "mt" else "(iso_1 < 0.3)*(iso_1>0.15)")
		else:
			log.fatal("No cut values implemented for channel \"%s\" in \"%s\"" % (channel, cut_type))
			sys.exit(1)
		return cuts

	def antiIsolationSSRegionQCD(channel, cut_type):
		if channel in ["mt", "et"]:
			cuts = CutStringsDict.antiIsolationRegionQCD(channel, cut_type)
			cuts["ss"] = "((q_1*q_2)>0.0)"
		else:
			log.fatal("No cut values implemented for channel \"%s\" in \"%s\"" % (channel, cut_type))
			sys.exit(1)
		return cuts

	@staticmethod
	def SameSignRegion(channel, cut_type):
		cuts = CutStringsDict._get_cutdict(channel, cut_type.replace("highMtControlRegionWJ","").replace("highMtSSControlRegionWJ","").replace("SameSignRegion",""))
		cuts["ss"] = "((q_1*q_2)>0.0)"
		return cuts
	
	@staticmethod
	def highMtControlRegionWJ(channel, cut_type):
		if channel in ["mt", "et"]:
			print "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
			print cut_type
			cuts = CutStringsDict._get_cutdict(channel, cut_type.replace("highMtControlRegionWJ","").replace("highMtSSControlRegionWJ","").replace("SameSignRegion",""))
			#cuts.pop("mt")
			cuts["mt_wj"] = "(mt_1>70.0)" if ("mssm" in cut_type or "cpggh" in cut_type or "2016" not in cut_type) else "(mt_1>80.0)"
			pprint(cuts)
		else:
			log.fatal("No cut values implemented for channel \"%s\" in \"%s\"" % (channel, cut_type))
			sys.exit(1)
		return cuts
	
	@staticmethod
	def highMtSSControlRegionWJ(channel, cut_type):
		if channel in ["mt", "et"]:
			cuts = CutStringsDict.highMtControlRegionWJ(channel, cut_type)
			cuts["ss"] = "((q_1*q_2)>0.0)"
		else:
			log.fatal("No cut values implemented for channel \"%s\" in \"%s\"" % (channel, cut_type))
			sys.exit(1)
		return cuts

	@staticmethod
	def invertedLeptonIsolation(channel, cut_type):
		if channel in ["mt", "et"]:
			cuts = CutStringsDict._get_cutdict(channel, cut_type.replace("invertedLeptonIsolation",""))
			cuts["iso_1"] = "((iso_1)>0.1)"
		else:
			log.fatal("No cut values implemented for channel \"%s\" in \"%s\"" % (channel, cut_type))
			sys.exit(1)
		return cuts

	@staticmethod
	def baseline_low_mvis(channel, cut_type):
		if channel== "gen":
			cuts = {}
		else:
			cuts = CutStringsDict.baseline(channel, cut_type)
			cuts["m_vis"] = "((m_vis > 40.0) * (m_vis < 85.0))"

		return cuts

	# cp final state cuts
	@staticmethod
	def cp2016(channel, cut_type):
		if channel == "mt":
			cuts = CutStringsDict.baseline(channel, cut_type)
			cuts["pt_1"] = "(pt_1 > 20.0)"
			cuts["pt_2"] = "(pt_2 > 20.0)"
		elif channel == "et":
			cuts = CutStringsDict.baseline(channel, cut_type)
			cuts["pt_1"] = "(pt_1 > 26.0)"
			cuts["pt_2"] = "(pt_2 > 20.0)"
		elif channel == "tt":
			cuts = CutStringsDict.baseline(channel, cut_type)
			cuts["pt_1"] = "(pt_1 > 40.0)"
			cuts["pt_2"] = "(pt_2 > 40.0)"
		elif channel == "mm":
			cuts = CutStringsDict.baseline(channel, cut_type)
			cuts["pt_1"] = "(pt_1 > 10.0)"
			cuts["pt_2"] = "(pt_2 > 10.0)"
		elif channel == "em" or channel == "ttbar":
			cuts = CutStringsDict.baseline(channel, cut_type)
			cuts["pt_1"] = "(pt_1 > 13.0)"
			cuts["pt_2"] = "(pt_2 > 10.0)"
		else:
			log.fatal("No cut values implemented for channel \"%s\" in \"%s\"" % (channel, cut_type))
			sys.exit(1)
		return cuts
	
	def cprho2016(channel, cut_type):
		if channel == "tt":
			cuts = CutStringsDict.cp2016(channel, cut_type)
			cuts["rhodecay"] = "(decayMode_1 == 1)*(decayMode_2 == 1)"

	def cpcomb2016(channel, cut_type):
		if channel == "mt":
			cuts = CutStringsDict.cp2016(channel, cut_type)
			cuts["rhodecay"] = "(decayMode_2 == 1)"
		if channel == "et":
			cuts = CutStringsDict.cp2016(channel, cut_type)
			cuts["rhodecay"] = "(decayMode_2 == 1)"
		if channel == "tt":
			cuts = CutStringsDict.cp2016(channel, cut_type)
			cuts["rhodecay"] = "((decayMode_1 == 1)*(decayMode_2 != 1))+((decayMode_1 != 1)*(decayMode_2 == 1))"

	@staticmethod
	def ztt2015cs(channel, cut_type):
		cuts = {}
		cuts["blind"] = "{blind}"
		cuts["os"] = "((q_1*q_2)<0.0)"
		
		if channel == "mm":
			cuts["trigger_threshold"] = "(pt_1 > 20.0 || pt_2 > 20.0)" #new
			cuts["extra_lepton_veto"] = "(extraelec_veto < 0.5)*(extramuon_veto < 0.5)"
			cuts["iso_1"] = "(iso_1 < 0.15)"
			cuts["iso_2"] = "(iso_2 < 0.15)"
			#cuts["m_vis"] = "(m_vis > 60.0)*(m_vis < 120.0)"
		elif channel == "ee":
			pass
		elif channel == "em":
			cuts["trigger_threshold"] = "(pt_1 > 24.0 || pt_2 > 24.0)" if "2016" in cut_type else "(1.0)"
			cuts["pzeta"] = "(pZetaMissVis > -20.0)"
			cuts["extra_lepton_veto"] = "(extraelec_veto < 0.5)*(extramuon_veto < 0.5)"#?
			cuts["iso_1"] = "(iso_1 < 0.15)"
			cuts["iso_2"] = "(iso_2 < 0.15)"
		elif channel == "mt":
			cuts["mt"] = "(mt_1<30.0)"#changed
			cuts["anti_e_tau_discriminators"] = "(againstElectronVLooseMVA6_2 > 0.5)"
			cuts["anti_mu_tau_discriminators"] = "(againstMuonTight3_2 > 0.5)"
			cuts["extra_muon_veto"] = "(extramuon_veto < 0.5)"#?is this the same? no extra electron veto
			cuts["iso_1"] = "(iso_1 < 0.1)"

			cuts["dilepton_veto"] = "(dilepton_veto < 0.5)"# shouldnt be there
			cuts["iso_2"] = "(byTightIsolationMVArun2v1DBoldDMwLT_2 > 0.5)"# shouldnt be there
			#if not "mssm" in cut_type: cuts["bveto"] = "(nbtag == 0)"
		elif channel == "et":
			cuts["iso_1"] = "(iso_1 < 0.1)"
			cuts["mt"] = "(mt_1<30.0)"#changed
			cuts["anti_e_tau_discriminators"] = "(againstElectronTightMVA6_2 > 0.5)"#strange in paper
			cuts["anti_mu_tau_discriminators"] = "(againstMuonLoose3_2 > 0.5)"

			cuts["extra_lepton_veto"] = "(extraelec_veto < 0.5)"# was "(extraelec_veto < 0.5)*(extramuon_veto < 0.5)" shouldnt be there

			cuts["dilepton_veto"] = "(dilepton_veto < 0.5)"# shouldnt be there
			cuts["iso_2"] = "(byTightIsolationMVArun2v1DBoldDMwLT_2 > 0.5)"# shouldnt be there
		elif channel == "tt":
			cuts["iso_1"] = "(byVTightIsolationMVArun2v1DBoldDMwLT_2 > 0.5)"
			cuts["iso_2"] = "(byVTightIsolationMVArun2v1DBoldDMwLT_2 > 0.5)"
			cuts["anti_e_tau_discriminators"] = "(againstElectronVLooseMVA6_1 > 0.5)*(againstElectronVLooseMVA6_2 > 0.5)"
			cuts["anti_mu_tau_discriminators"] = "(againstMuonLoose3_1 > 0.5)*(againstMuonLoose3_2 > 0.5)"
			
			cuts["extra_lepton_veto"] = "(extraelec_veto < 0.5)*(extramuon_veto < 0.5)"# shouldnt be there
		else:
			log.fatal("No cut values implemented for channel \"%s\" in \"%s\"" % (channel, cut_type))
			sys.exit(1)
		return cuts

	@staticmethod
	def _get_cutdict(channel, cut_type):
		cuts = {}
		if cut_type=="baseline":
			cuts = CutStringsDict.baseline(channel, cut_type)
		elif cut_type=="baseline2016":
			cuts = CutStringsDict.baseline(channel, cut_type)
		elif cut_type=="baseline2017":
			cuts = CutStringsDict.baseline(channel, cut_type)
		elif cut_type=="smhtt2016":
			cuts = CutStringsDict.baseline(channel, cut_type)
		elif cut_type=="cpggh2016":
			cuts = CutStringsDict.cpggh2016(channel, cut_type)	
		elif cut_type=="cpggh2017":
			cuts = CutStringsDict.cpggh2017(channel, cut_type)			
		elif cut_type=="mssm":
			cuts = CutStringsDict.baseline(channel, cut_type)
		elif cut_type=="mssm2016":
			cuts = CutStringsDict.baseline(channel, cut_type)
		elif cut_type=="mssm2016full":
			cuts = CutStringsDict.mssm2016(channel, cut_type)
		elif cut_type=="mssm2016tight":
			cuts = CutStringsDict.mssm2016(channel, cut_type)
		elif cut_type=="mssm2016loosemt":
			cuts = CutStringsDict.mssm2016(channel, cut_type)
		elif cut_type=="mssm2016looseiso":
			cuts = CutStringsDict.mssm2016(channel, cut_type)
		elif cut_type=="mssm2016fffull":
			cuts = CutStringsDict.mssm2016(channel, cut_type)
		elif cut_type=="mssm2016fflooseiso":
			cuts = CutStringsDict.mssm2016(channel, cut_type)

		elif cut_type=="antievloosepass2016" or cut_type=="antievloosepass2017":
			cuts = CutStringsDict.antievloosepass(channel, cut_type)
		elif cut_type=="antievloosefail2016" or cut_type=="antievloosefail2017":
			cuts = CutStringsDict.antievloosefail(channel, cut_type)
		elif cut_type=="antieloosepass2016" or cut_type=="antieloosepass2017":
			cuts = CutStringsDict.antieloosepass(channel, cut_type)
		elif cut_type=="antieloosefail2016" or cut_type=="antieloosefail2017":
			cuts = CutStringsDict.antieloosefail(channel, cut_type)
		elif cut_type=="antiemediumpass2016" or cut_type=="antiemediumpass2017":
			cuts = CutStringsDict.antiemediumpass(channel, cut_type)
		elif cut_type=="antiemediumfail2016" or cut_type=="antiemediumfail2017":
			cuts = CutStringsDict.antiemediumfail(channel, cut_type)
		elif cut_type=="antietightpass2016" or cut_type=="antietightpass2017":
			cuts = CutStringsDict.antietightpass(channel, cut_type)
		elif cut_type=="antietightfail2016" or cut_type=="antietightfail2017":
			cuts = CutStringsDict.antietightfail(channel, cut_type)
		elif cut_type=="antievtightpass2016" or cut_type=="antievtightpass2017":
			cuts = CutStringsDict.antievtightpass(channel, cut_type)
		elif cut_type=="antievtightfail2016" or cut_type=="antievtightfail2017":
			cuts = CutStringsDict.antievtightfail(channel, cut_type)
		elif cut_type=="antieinclusive2017":
			cuts = CutStringsDict.antieinclusive(channel, cut_type)
		
		elif cut_type=="antimuloosepass":
			cuts = CutStringsDict.antimuloosepass(channel, cut_type)
		elif cut_type=="antimuloosefail":
			cuts = CutStringsDict.antimuloosefail(channel, cut_type)
		elif cut_type=="antimutightpass":
			cuts = CutStringsDict.antimutightpass(channel, cut_type)
		elif cut_type=="antimutightfail":
			cuts = CutStringsDict.antimutightfail(channel, cut_type)
		
		elif cut_type=="tauidloosepass":
			cuts = CutStringsDict.tauidloosepass(channel, cut_type)
		elif cut_type=="tauidloosefail":
			cuts = CutStringsDict.tauidloosefail(channel, cut_type)
		elif cut_type=="tauidmediumpass":
			cuts = CutStringsDict.tauidmediumpass(channel, cut_type)
		elif cut_type=="tauidmediumfail":
			cuts = CutStringsDict.tauidmediumfail(channel, cut_type)
		elif cut_type=="tauidtightpass":
			cuts = CutStringsDict.tauidtightpass(channel, cut_type)
		elif cut_type=="tauidtightfail":
			cuts = CutStringsDict.tauidtightfail(channel, cut_type)
		elif cut_type=="tauidvtightpass":
			cuts = CutStringsDict.tauidvtightpass(channel, cut_type)
		elif cut_type=="tauidvtightfail":
			cuts = CutStringsDict.tauidvtightfail(channel, cut_type)
		
		elif cut_type=="tauescuts":
			cuts = CutStringsDict.tauescuts(channel, cut_type)
		elif cut_type=="tauescuts2016":
			cuts = CutStringsDict.tauescuts(channel, cut_type)
		elif "relaxedETauMuTauWJ" in cut_type:
			cuts = CutStringsDict.relaxedETauMuTauWJ(channel, cut_type)
		elif "highMtControlRegionWJ" in cut_type:
			cuts = CutStringsDict.highMtControlRegionWJ(channel, cut_type)
		elif "highMtSSControlRegionWJ" in cut_type:
			cuts = CutStringsDict.highMtSSControlRegionWJ(channel, cut_type)
		elif "SameSignRegion" in cut_type:
			cuts = CutStringsDict.SameSignRegion(channel, cut_type)
		elif "invertedLeptonIsolation" in cut_type:
			cuts = CutStringsDict.invertedLeptonIsolation(channel, cut_type)

		elif "low_mvis_smhtt" in cut_type:
			cuts = CutStringsDict.baseline_low_mvis(channel, cut_type)
		
		elif cut_type=="cp2016":
			cuts = CutStringsDict.cp2016(channel, cut_type)

		elif cut_type=="ztt2015cs":
			cuts = CutStringsDict.ztt2015cs(channel, cut_type)

		elif cut_type=="lfv":
			cuts = CutStringsDict.lfv(channel, cut_type)

		else:
			log.fatal("No cut dictionary implemented for \"%s\"!" % cut_type)
			sys.exit(1)
		return cuts
