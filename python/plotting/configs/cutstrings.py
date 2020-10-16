
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import sys
from pprint import pprint

class CutStringsDict:

	@staticmethod
	def baseline(channel, cut_type, **kwargs):
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
				cuts["iso_2"] = "(byTightIsolationMVArun2017v2DBoldDMwLT2017_2 > 0.5)*((gen_match_2 == 5)*0.89 + (gen_match_2 != 5))"
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
				cuts["trigger"] = "(((trg_singleelectron_35>0.5)*(pt_1>36))||((trg_crosselectron_ele24tau30>0.5)*(pt_1>25)*(pt_1<28)*(abs(eta_2)<2.1)*(pt_2>35))||((trg_singleelectron_27>0.5)*(pt_1>28))||((trg_singleelectron_32>0.5)*(pt_1>33))||((trg_singleelectron_32_fallback>0.5)*(pt_1>33)))"
				cuts["iso_1"] = "(iso_1 < 0.15)"
				cuts["iso_2"] = "(byTightIsolationMVArun2017v2DBoldDMwLT2017_2 > 0.5)*((gen_match_2 == 5)*0.89 + (gen_match_2 != 5))" #only for MC; TODO add byTightIsolationMVArun2v1DBoldDMwLT_2, 0.87 = tauid sf tight
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
	def mssm2016(channel, cut_type, **kwargs):
		cuts = CutStringsDict.baseline(channel, cut_type, **kwargs)
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
	def cpggh2016(channel, cut_type, **kwargs):
		cuts = CutStringsDict.baseline(channel, cut_type, **kwargs)
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
			cuts["pt_1"] = "(pt_1 > 20.0)"
			cuts["pt_2"] = "(pt_2 > 30.0)"
			cuts["mt"] = "(mt_1<50.0)"
			cuts["iso_1"] = "(iso_1 < 0.15)"
			cuts["iso_2"] = "(byTightIsolationMVArun2v1DBoldDMwLT_2 > 0.5)*((gen_match_2 == 5)*0.95 + (gen_match_2 != 5))"
			if "emb" in cut_type:
				cuts["iso_2"] = "(byTightIsolationMVArun2v1DBoldDMwLT_2 > 0.5)*((gen_match_2 == 5)*1.02 + (gen_match_2 != 5))"
				cuts["trg"] = "(((trg_mutaucross == 1)*(triggerWeight_muTauCross_1)*(pt_1 <= 23))+((trg_singlemuon == 1)*(triggerWeight_singleMu_1)*(pt_1 > 23)))*(triggerWeight_doublemu_1)"
			else:
				cuts["trg"] = "(((trg_mutaucross == 1)*(triggerWeight_muTauCross_1)*(triggerWeight_muTauCross_2)*(pt_1 <= 23))+((trg_singlemuon == 1)*(triggerWeight_singleMu_1)*(pt_1 > 23)))"
		elif channel == "et":
			cuts["pt_1"] = "(pt_1 > 25.0)"
			cuts["pt_2"] = "(pt_2 > 30.0)"
			cuts["mt"] = "(mt_1<50.0)"
			cuts["iso_1"] = "(iso_1 < 0.1)"
			cuts["iso_2"] = "(byTightIsolationMVArun2v1DBoldDMwLT_2 > 0.5)*((gen_match_2 == 5)*0.95 + (gen_match_2 != 5))"
			if "emb" in cut_type:
				cuts["iso_2"] = "(byTightIsolationMVArun2v1DBoldDMwLT_2 > 0.5)*((gen_match_2 == 5)*1.02 + (gen_match_2 != 5))"
				cuts["trg"] = "(triggerWeight_singleE_1*triggerWeight_doublemu_1)"
		elif channel == "tt":
			cuts["pt_1"] = "(pt_1 > 50.0)"
			cuts["pt_2"] = "(pt_2 > 40.0)"
			cuts["iso_1"] = "(byTightIsolationMVArun2v1DBoldDMwLT_1 > 0.5)*((gen_match_1 == 5)*0.95 + (gen_match_1 != 5))"
			cuts["iso_2"] = "(byTightIsolationMVArun2v1DBoldDMwLT_2 > 0.5)*((gen_match_2 == 5)*0.95 + (gen_match_2 != 5))"
			if "emb" in cut_type:
				cuts["iso_1"] = "(byTightIsolationMVArun2v1DBoldDMwLT_1 > 0.5)*((gen_match_1 == 5)*1.02 + (gen_match_1 != 5))"
				cuts["iso_2"] = "(byTightIsolationMVArun2v1DBoldDMwLT_2 > 0.5)*((gen_match_2 == 5)*1.02 + (gen_match_2 != 5))"
				cuts["trg"] = "(triggerWeight_tau_1*triggerWeight_tau_2*triggerWeight_doublemu_1)"
		return cuts

	@staticmethod
	def cpggh2017(channel, cut_type, **kwargs):
		cuts = CutStringsDict.baseline(channel, cut_type, **kwargs)
		cuts["bveto"] = "(nbtag == 0)"
		cuts["prefiringWeight"] = "(1.0)" if "emb" in cut_type else "(prefiringWeight)"
		if channel == "mm":  #TODO
			cuts["pt_1"] = "(pt_1 > 25.0)"
			cuts["pt_2"] = "(pt_2 > 25.0)"
			cuts["eta_1"] = "(abs(eta_1) < 2.1)"
			cuts["eta_2"] = "(abs(eta_2) < 2.1)"
		elif channel == "em": #TODO
			cuts["bveto"] = "(nbtag == 0)"
			cuts["pt_1"] = "(pt_1 > 13.0)"
			cuts["pt_2"] = "(pt_2 > 10.0)"
			# used to remove overlap with H->WW->emu analysis
			cuts["diLepMetMt"] = "(diLepMetMt < 60.0)"
		elif channel == "mt":
			cuts["trigger"] = "(((pt_1 >= 25.0)*(trg_singlemuon_24>0.5))||((pt_1 >= 28.0)*(trg_singlemuon_27>0.5))||((pt_1 < 25.0)*(pt_2 > 32.0)*(abs(eta_2) < 2.1)*(trg_crossmuon_mu20tau27>0.5)))"
			cuts["pt_1"] = "(pt_1 > 21.0)"
			cuts["pt_2"] = "(pt_2 > 30.0)"
			cuts["mt"] = "(mt_1<50.0)"
			cuts["iso_1"] = "(iso_1 < 0.15)"
			cuts["iso_2"] = "(byTightIsolationMVArun2017v2DBoldDMwLT2017_2 > 0.5)*((gen_match_2 == 5)*0.89 + (gen_match_2 != 5))"
			cuts["eta_2"] = "(abs(eta_2) < 2.1)"
			if "emb" in cut_type:
				# cuts["trigger"] = "((((pt_1 >= 25.0)*(trg_singlemuon_24>0.5))||(trg_crossmuon_mu20tau27>0.5)||((pt_1 >= 28.0)*(trg_singlemuon_27>0.5)))*triggerWeight_mu_1 + ((pt_1 < 25.0)*(pt_2 > 32.0)*(abs(eta_2) < 2.1)*((trg_crossmuon_mu20tau27>0.5)||(trg_singlemuon_27>0.5)||(trg_singlemuon_24>0.5))))"
				cuts["trigger"] = "((((pt_1 >= 25.0)*(trg_singlemuon_24>0.5))||((pt_1 >= 28.0)*(trg_singlemuon_27>0.5)))*triggerWeight_mu_1 + ((pt_1 < 25.0)*(pt_2 > 32.0)*(abs(eta_2) < 2.1)*(trg_crossmuon_mu20tau27>0.5)))"
				# cuts["trigger"] = "(((trg_singlemuon_24>0.5)||(trg_singlemuon_27>0.5))||(trg_crossmuon_mu20tau27>0.5))*triggerWeight_mu_1*triggerWeight_mutaucross_1*triggerWeight_mutaucross_2"
				# cuts["trigger"] = "((((trg_singlemuon_24>0.5))||((trg_singlemuon_27>0.5)))*triggerWeight_mu_1 + ((trg_crossmuon_mu20tau27>0.5)*triggerWeight_mutaucross_1*triggerWeight_mutaucross_2))"
				# cuts["trigger"] = "((((pt_1 >= 25.0)*(trg_singlemuon_24>0.5))||((pt_1 >= 28.0)*(trg_singlemuon_27>0.5)))*triggerWeight_mu_1 + ((pt_1 < 25.0)*(pt_2 > 32.0)*(abs(eta_2) < 2.1)*(trg_crossmuon_mu20tau27>0.5)*triggerWeight_mutaucross_1*triggerWeight_mutaucross_2))"
				# cuts["trigger"] = "((((pt_1 >= 25.0)*(trg_singlemuon_24>0.5))||((pt_1 >= 28.0)*(trg_singlemuon_27>0.5)))*triggerWeight_mu_1 + ((pt_1 < 25.0)*(pt_2 > 32.0)*(abs(eta_2) < 2.1)*(trg_crossmuon_mu20tau27>0.5)*triggerWeight_mutaucross_2))"
				cuts["trigger"] += "*(triggerWeight_doublemu_1)"
				cuts["iso_2"] = "(byTightIsolationMVArun2017v2DBoldDMwLT2017_2 > 0.5)*((gen_match_2 == 5)*0.97 + (gen_match_2 != 5))"
		elif channel == "et":
			if "emb" in cut_type:
				cuts["trigger"] = "( (abs(eta_1) <= 1.479) * ( (((trg_singleelectron_27>0.5)*(pt_1 >= 28.0)) || (((trg_singleelectron_32>0.5)||(trg_singleelectron_32_fallback>0.5))*(pt_1>33)) || ((trg_singleelectron_35>0.5)*(pt_1>36))) * triggerWeight_trg27_trg32_trg35_embed_1 + ((trg_crosselectron_ele24tau30>0.5)*(pt_1 < 28.0)*(pt_2 > 35.0)*(abs(eta_2) < 2.1))*triggerWeight_tauLeg_2*triggerWeight_trg_EleTau_Ele24Leg_embed_1 ) + (abs(eta_1) > 1.479) * (triggerWeight_trg27_trg32_trg35_data_1*(pt_1>28.0) + tautriggerefficiencyData*triggerWeight_trg_EleTau_Ele24Leg_data_1*(pt_1 < 28.0)*(pt_2 > 35.0)*(abs(eta_2) < 2.1)) )"
				# cuts["trigger"] = "( (abs(eta_1) <= 1.479) * ( (((trg_singleelectron_27>0.5)*(pt_1 >= 28.0)) || (((trg_singleelectron_32>0.5)||(trg_singleelectron_32_fallback>0.5))*(pt_1>33)) || ((trg_singleelectron_35>0.5)*(pt_1>36))) * triggerWeight_trg27_trg32_trg35_embed_1 + ((trg_crosselectron_ele24tau30>0.5)*(pt_1 < 28.0)*(pt_2 > 35.0))*triggerWeight_tauLeg_2*triggerWeight_trg_EleTau_Ele24Leg_embed_1 ) + (abs(eta_1) > 1.479) * (triggerWeight_trg27_trg32_trg35_data_1*(pt_1>28.0) + tautriggerefficiencyData*triggerWeight_trg_EleTau_Ele24Leg_data_1*(pt_1 < 28.0)) )"
				# cuts["trigger"] = "( (abs(eta_1) <= 1.479) * ( (((trg_singleelectron_27>0.5)*(pt_1 >= 28.0)) || (((trg_singleelectron_32>0.5)||(trg_singleelectron_32_fallback>0.5))*(pt_1>33)) || ((trg_singleelectron_35>0.5)*(pt_1>36))) * triggerWeight_trg27_trg32_trg35_embed_1 + ((trg_crosselectron_ele24tau30>0.5)*(pt_1 < 28.0)*(pt_2 > 35.0))*triggerWeight_tauLeg_2*triggerWeight_trg_EleTau_Ele24Leg_embed_1 ) + (abs(eta_1) > 1.479) * ((((trg_singleelectron_27>0.5)*(pt_1 >= 28.0)) || (((trg_singleelectron_32>0.5)||(trg_singleelectron_32_fallback>0.5))*(pt_1>33)) || ((trg_singleelectron_35>0.5)*(pt_1>36)))*triggerWeight_trg27_trg32_trg35_data_1 + tautriggerefficiencyData*triggerWeight_trg_EleTau_Ele24Leg_data_1*((trg_crosselectron_ele24tau30>0.5)*(pt_1 < 28.0)*(pt_2 > 35.0))) )"
				# cuts["trigger"] = "( (abs(eta_1) <= 1.479) * ( (((trg_singleelectron_27>0.5)) || (((trg_singleelectron_32>0.5)||(trg_singleelectron_32_fallback>0.5))) || ((trg_singleelectron_35>0.5))) * triggerWeight_trg27_trg32_trg35_embed_1 + ((trg_crosselectron_ele24tau30>0.5))*triggerWeight_tauLeg_2*triggerWeight_trg_EleTau_Ele24Leg_embed_1 ) + (abs(eta_1) > 1.479) * (triggerWeight_trg27_trg32_trg35_data_1 + tautriggerefficiencyData*triggerWeight_trg_EleTau_Ele24Leg_data_1) )"
				cuts["trigger"] += "*(triggerWeight_doublemu_1)"
			cuts["pt_1"] = "(pt_1 > 25.0)"
			cuts["pt_2"] = "(pt_2 > 30.0)"
			cuts["mt"] = "(mt_1<50.0)"
			cuts["iso_1"] = "(iso_1 < 0.1)"
			cuts["iso_2"] = "(byTightIsolationMVArun2017v2DBoldDMwLT2017_2 > 0.5)*((gen_match_2 == 5)*0.89 + (gen_match_2 != 5))"
			cuts["eta_2"] = "(abs(eta_2) < 2.1)"
			if "emb" in cut_type:
				cuts["iso_2"] = "(byTightIsolationMVArun2017v2DBoldDMwLT2017_2 > 0.5)*((gen_match_2 == 5)*0.97 + (gen_match_2 != 5))"
		elif channel == "tt": #TODO
			cuts["pt_1"] = "(pt_1 > 50.0)"
			cuts["pt_2"] = "(pt_2 > 40.0)"
			cuts["iso_1"] = "(byTightIsolationMVArun2017v2DBoldDMwLT2017_1 > 0.5)*((gen_match_1 == 5)*0.95 + (gen_match_1 != 5))"
			cuts["iso_2"] = "(byTightIsolationMVArun2017v2DBoldDMwLT2017_2 > 0.5)*((gen_match_2 == 5)*0.95 + (gen_match_2 != 5))"
		#cuts["generatorweight"] = "(1/generatorWeight)" #TODO
		return cuts


	@staticmethod
	def cptautau2017(channel, cut_type, **kwargs):
		data = kwargs.get("data", False)
		embedding = kwargs.get("embedding", False)
		cuts = CutStringsDict.baseline(channel, cut_type, **kwargs)
		# cuts["bveto"] = "(nbtag == 0)"
		cuts["prefiringWeight"] = "(1.0)" if "emb" in cut_type else "(prefiringWeight)"

		if channel == "mt":
			# cuts["trigger"] = "(((pt_1 >= 25.0)*(trg_singlemuon_24>0.5))||((pt_1 >= 28.0)*(trg_singlemuon_27>0.5))||((pt_1 < 25.0)*(pt_2 > 32.0)*(abs(eta_2) < 2.1)*(trg_crossmuon_mu20tau27>0.5)))"
			if data :
				cuts["trigger"] = "((((pt_1 >= 25.0)*(trg_singlemuon_24>0.5))||((pt_1 >= 28.0)*(trg_singlemuon_27>0.5))) + ((pt_1 < 25.0)*(pt_2 > 32.0)*(abs(eta_2) < 2.1)*(trg_crossmuon_mu20tau27>0.5)))"
			else:
				# tauidtriggersf_2 = "((byVLooseIsolationMVArun2017v2DBoldDMwLT2017_2 > 0.5)*(byLooseIsolationMVArun2017v2DBoldDMwLT2017_2 < 0.5)*tautriggerefficiencyData_2_vloose/tautriggerefficiencyMC_2_vloose + (byLooseIsolationMVArun2017v2DBoldDMwLT2017_2 > 0.5)*(byMediumIsolationMVArun2017v2DBoldDMwLT2017_2 < 0.5)*tautriggerefficiencyData_2_loose/tautriggerefficiencyMC_2_loose + (byMediumIsolationMVArun2017v2DBoldDMwLT2017_2 > 0.5)*(byTightIsolationMVArun2017v2DBoldDMwLT2017_2 < 0.5)*tautriggerefficiencyData_2_medium/tautriggerefficiencyMC_2_medium + (byTightIsolationMVArun2017v2DBoldDMwLT2017_2 > 0.5)*(byVTightIsolationMVArun2017v2DBoldDMwLT2017_2 < 0.5)*tautriggerefficiencyData_2_tight/tautriggerefficiencyMC_2_tight + (byVTightIsolationMVArun2017v2DBoldDMwLT2017_2 > 0.5)*(byVVTightIsolationMVArun2017v2DBoldDMwLT2017_2 < 0.5)*tautriggerefficiencyData_2_vtight/tautriggerefficiencyMC_2_vtight + (byVVTightIsolationMVArun2017v2DBoldDMwLT2017_2 > 0.5)*tautriggerefficiencyData_2_vvtight/tautriggerefficiencyMC_2_vvtight)"
				# tauidtriggersf_2 = "((byVLooseIsolationMVArun2017v2DBoldDMwLT2017_2 > 0.5)*(byLooseIsolationMVArun2017v2DBoldDMwLT2017_2 < 0.5)*tautriggerefficiencyData_2_vloose/((tautriggerefficiencyMC_2_vloose > 0)*tautriggerefficiencyMC_2_vloose + (tautriggerefficiencyMC_2_vloose == 0)*1.0) + (byLooseIsolationMVArun2017v2DBoldDMwLT2017_2 > 0.5)*(byMediumIsolationMVArun2017v2DBoldDMwLT2017_2 < 0.5)*tautriggerefficiencyData_2_loose/((tautriggerefficiencyMC_2_loose > 0)*tautriggerefficiencyMC_2_loose + (tautriggerefficiencyMC_2_loose == 0)*1.0) + (byMediumIsolationMVArun2017v2DBoldDMwLT2017_2 > 0.5)*(byTightIsolationMVArun2017v2DBoldDMwLT2017_2 < 0.5)*tautriggerefficiencyData_2_medium/((tautriggerefficiencyMC_2_medium > 0)*tautriggerefficiencyMC_2_medium + (tautriggerefficiencyMC_2_medium == 0)*1.0) + (byTightIsolationMVArun2017v2DBoldDMwLT2017_2 > 0.5)*(byVTightIsolationMVArun2017v2DBoldDMwLT2017_2 < 0.5)*tautriggerefficiencyData_2_tight/((tautriggerefficiencyMC_2_tight > 0)*tautriggerefficiencyMC_2_tight + (tautriggerefficiencyMC_2_tight == 0)*1.0) + (byVTightIsolationMVArun2017v2DBoldDMwLT2017_2 > 0.5)*(byVVTightIsolationMVArun2017v2DBoldDMwLT2017_2 < 0.5)*tautriggerefficiencyData_2_vtight/((tautriggerefficiencyMC_2_vtight > 0)*tautriggerefficiencyMC_2_vtight + (tautriggerefficiencyMC_2_vtight == 0)*1.0) + (byVVTightIsolationMVArun2017v2DBoldDMwLT2017_2 > 0.5)*tautriggerefficiencyData_2_vvtight/((tautriggerefficiencyMC_2_vvtight > 0)*tautriggerefficiencyMC_2_vvtight + (tautriggerefficiencyMC_2_vvtight == 0)*1.0))"
				#"((byVLooseIsolationMVArun2017v2DBoldDMwLT2017_2 > 0.5)*(byLooseIsolationMVArun2017v2DBoldDMwLT2017_2 < 0.5)*((tautriggerefficiencyMC_2_vloose > 0)*tautriggerefficiencyData_2_vloose/tautriggerefficiencyMC_2_vloose + (tautriggerefficiencyMC_2_vloose <= 0)) + (byLooseIsolationMVArun2017v2DBoldDMwLT2017_2 > 0.5)*(byMediumIsolationMVArun2017v2DBoldDMwLT2017_2 < 0.5)*((tautriggerefficiencyMC_2_loose > 0)*tautriggerefficiencyData_2_loose/tautriggerefficiencyMC_2_loose + (tautriggerefficiencyMC_2_loose <= 0)) + (byMediumIsolationMVArun2017v2DBoldDMwLT2017_2 > 0.5)*(byTightIsolationMVArun2017v2DBoldDMwLT2017_2 < 0.5)*((tautriggerefficiencyMC_2_medium > 0)*tautriggerefficiencyData_2_medium/tautriggerefficiencyMC_2_medium + (tautriggerefficiencyMC_2_medium <= 0)) + (byTightIsolationMVArun2017v2DBoldDMwLT2017_2 > 0.5)*(byVTightIsolationMVArun2017v2DBoldDMwLT2017_2 < 0.5)*((tautriggerefficiencyMC_2_tight > 0)*tautriggerefficiencyData_2_tight/tautriggerefficiencyMC_2_tight + (tautriggerefficiencyMC_2_tight <= 0)) + (byVTightIsolationMVArun2017v2DBoldDMwLT2017_2 > 0.5)*(byVVTightIsolationMVArun2017v2DBoldDMwLT2017_2 < 0.5)*((tautriggerefficiencyMC_2_vtight > 0)*tautriggerefficiencyData_2_vtight/tautriggerefficiencyMC_2_vtight + (byVVTightIsolationMVArun2017v2DBoldDMwLT2017_2 > 0.5)*(tautriggerefficiencyMC_2_vvtight > 0)*tautriggerefficiencyData_2_vvtight/tautriggerefficiencyMC_2_vvtight + (tautriggerefficiencyMC_2_vtight <= 0)))"
				tauidtriggersf_2 = "triggerWeight_mutaucross_2"
				cuts["trigger"] = "((((pt_1 >= 25.0)*(trg_singlemuon_24>0.5))||((pt_1 >= 28.0)*(trg_singlemuon_27>0.5)))*triggerWeight_mu_1 + ((pt_1 < 25.0)*(pt_2 > 32.0)*(abs(eta_2) < 2.1)*(trg_crossmuon_mu20tau27>0.5)*triggerWeight_mutaucross_1*" + tauidtriggersf_2 + "))"
			cuts["pt_1"] = "(pt_1 > 21.0)"
			cuts["pt_2"] = "(pt_2 > 30.0)"
			cuts["eta_1"] = "(abs(eta_1) < 2.1)"
			cuts["eta_2"] = "(abs(eta_2) < 2.1)"
			cuts["mt"] = "(mt_1<50.0)"
			cuts["iso_1"] = "(iso_1 < 0.15)"
			cuts["iso_2"] = "(byTightIsolationMVArun2017v2DBoldDMwLT2017_2 > 0.5)"
			if "emb" in cut_type:
				# cuts["trigger"] = "((((pt_1 >= 25.0)*(trg_singlemuon_24>0.5))||(trg_crossmuon_mu20tau27>0.5)||((pt_1 >= 28.0)*(trg_singlemuon_27>0.5)))*triggerWeight_mu_1 + ((pt_1 < 25.0)*(pt_2 > 32.0)*(abs(eta_2) < 2.1)*((trg_crossmuon_mu20tau27>0.5)||(trg_singlemuon_27>0.5)||(trg_singlemuon_24>0.5))))"
				# cuts["trigger"] = "((((pt_1 >= 25.0)*(trg_singlemuon_24>0.5))||((pt_1 >= 28.0)*(trg_singlemuon_27>0.5)))*triggerWeight_mu_1 + ((pt_1 < 25.0)*(pt_2 > 32.0)*(abs(eta_2) < 2.1)*(trg_crossmuon_mu20tau27>0.5)*triggerWeight_mutaucross_1*triggerWeight_mutaucross_2))"
				# cuts["trigger"] = "(((trg_singlemuon_24>0.5)||(trg_singlemuon_27>0.5))||(trg_crossmuon_mu20tau27>0.5))*triggerWeight_mu_1*triggerWeight_mutaucross_1*triggerWeight_mutaucross_2"
				# cuts["trigger"] = "((((trg_singlemuon_24>0.5))||((trg_singlemuon_27>0.5)))*triggerWeight_mu_1 + ((trg_crossmuon_mu20tau27>0.5)*triggerWeight_mutaucross_1*triggerWeight_mutaucross_2))"
				cuts["trigger"] = "((((pt_1 >= 25.0)*(trg_singlemuon_24>0.5))||((pt_1 >= 28.0)*(trg_singlemuon_27>0.5)))*triggerWeight_mu_1 + ((pt_1 < 25.0)*(pt_2 > 32.0)*(abs(eta_2) < 2.1)*(trg_crossmuon_mu20tau27>0.5)*triggerWeight_mutaucross_1*triggerWeight_mutaucross_2))"
				cuts["trigger"] += "*(triggerWeight_doublemu_1)"

		elif channel == "et":
			if data :
				cuts["trigger"] = "( ( (((trg_singleelectron_27>0.5)*(pt_1 >= 28.0)) || (((trg_singleelectron_32>0.5)||(trg_singleelectron_32_fallback>0.5))*(pt_1>33)) || ((trg_singleelectron_35>0.5)*(pt_1>36))) + ((trg_crosselectron_ele24tau30>0.5)*(pt_1 < 28.0)*(pt_2 > 35.0)*(abs(eta_2) < 2.1)) ))"
			else:
				# tauidtriggersf_2 = "((byVLooseIsolationMVArun2017v2DBoldDMwLT2017_2 > 0.5)*(byLooseIsolationMVArun2017v2DBoldDMwLT2017_2 < 0.5)*tautriggerefficiencyData_2_vloose/((tautriggerefficiencyMC_2_vloose > 0)*tautriggerefficiencyMC_2_vloose + (tautriggerefficiencyMC_2_vloose == 0)*1.0) + (byLooseIsolationMVArun2017v2DBoldDMwLT2017_2 > 0.5)*(byMediumIsolationMVArun2017v2DBoldDMwLT2017_2 < 0.5)*tautriggerefficiencyData_2_loose/((tautriggerefficiencyMC_2_loose > 0)*tautriggerefficiencyMC_2_loose + (tautriggerefficiencyMC_2_loose == 0)*1.0) + (byMediumIsolationMVArun2017v2DBoldDMwLT2017_2 > 0.5)*(byTightIsolationMVArun2017v2DBoldDMwLT2017_2 < 0.5)*tautriggerefficiencyData_2_medium/((tautriggerefficiencyMC_2_medium > 0)*tautriggerefficiencyMC_2_medium + (tautriggerefficiencyMC_2_medium == 0)*1.0) + (byTightIsolationMVArun2017v2DBoldDMwLT2017_2 > 0.5)*(byVTightIsolationMVArun2017v2DBoldDMwLT2017_2 < 0.5)*tautriggerefficiencyData_2_tight/((tautriggerefficiencyMC_2_tight > 0)*tautriggerefficiencyMC_2_tight + (tautriggerefficiencyMC_2_tight == 0)*1.0) + (byVTightIsolationMVArun2017v2DBoldDMwLT2017_2 > 0.5)*(byVVTightIsolationMVArun2017v2DBoldDMwLT2017_2 < 0.5)*tautriggerefficiencyData_2_vtight/((tautriggerefficiencyMC_2_vtight > 0)*tautriggerefficiencyMC_2_vtight + (tautriggerefficiencyMC_2_vtight == 0)*1.0) + (byVVTightIsolationMVArun2017v2DBoldDMwLT2017_2 > 0.5)*tautriggerefficiencyData_2_vvtight/((tautriggerefficiencyMC_2_vvtight > 0)*tautriggerefficiencyMC_2_vvtight + (tautriggerefficiencyMC_2_vvtight == 0)*1.0))"
				tauidtriggersf_2 = "triggerWeight_etaucross_2"
				cuts["trigger"] = "( ( (((trg_singleelectron_27>0.5)*(pt_1 >= 28.0)) || (((trg_singleelectron_32>0.5)||(trg_singleelectron_32_fallback>0.5))*(pt_1>33)) || ((trg_singleelectron_35>0.5)*(pt_1>36))) * triggerWeight_singleE_1 + ((trg_crosselectron_ele24tau30>0.5)*(pt_1 < 28.0)*(pt_2 > 35.0)*(abs(eta_2) < 2.1))*triggerWeight_etaucross_1*" + tauidtriggersf_2 + " ))"
			if "emb" in cut_type:
				cuts["trigger"] = "( (abs(eta_1) <= 1.479) * ( (((trg_singleelectron_27>0.5)*(pt_1 >= 28.0)) || (((trg_singleelectron_32>0.5)||(trg_singleelectron_32_fallback>0.5))*(pt_1>33)) || ((trg_singleelectron_35>0.5)*(pt_1>36))) * triggerWeight_trg27_trg32_trg35_embed_1 + ((trg_crosselectron_ele24tau30>0.5)*(pt_1 < 28.0)*(pt_2 > 35.0)*(abs(eta_2) < 2.1))*triggerWeight_tauLeg_2*triggerWeight_trg_EleTau_Ele24Leg_embed_1 ) + (abs(eta_1) > 1.479) * (triggerWeight_trg27_trg32_trg35_data_1*(pt_1>28.0) + tautriggerefficiencyData_2*triggerWeight_trg_EleTau_Ele24Leg_data_1*(pt_1 < 28.0)*(pt_2 > 35.0)*(abs(eta_2) < 2.1)) )"
				# cuts["trigger"] = "( (abs(eta_1) <= 1.479) * ( (((trg_singleelectron_27>0.5)*(pt_1 >= 28.0)) || (((trg_singleelectron_32>0.5)||(trg_singleelectron_32_fallback>0.5))*(pt_1>33)) || ((trg_singleelectron_35>0.5)*(pt_1>36))) * triggerWeight_trg27_trg32_trg35_embed_1 + ((trg_crosselectron_ele24tau30>0.5)*(pt_1 < 28.0)*(pt_2 > 35.0))*triggerWeight_tauLeg_2*triggerWeight_trg_EleTau_Ele24Leg_embed_1 ) + (abs(eta_1) > 1.479) * (triggerWeight_trg27_trg32_trg35_data_1*(pt_1>28.0) + tautriggerefficiencyData*triggerWeight_trg_EleTau_Ele24Leg_data_1*(pt_1 < 28.0)) )"
				# cuts["trigger"] = "( (abs(eta_1) <= 1.479) * ( (((trg_singleelectron_27>0.5)*(pt_1 >= 28.0)) || (((trg_singleelectron_32>0.5)||(trg_singleelectron_32_fallback>0.5))*(pt_1>33)) || ((trg_singleelectron_35>0.5)*(pt_1>36))) * triggerWeight_trg27_trg32_trg35_embed_1 + ((trg_crosselectron_ele24tau30>0.5)*(pt_1 < 28.0)*(pt_2 > 35.0))*triggerWeight_tauLeg_2*triggerWeight_trg_EleTau_Ele24Leg_embed_1 ) + (abs(eta_1) > 1.479) * ((((trg_singleelectron_27>0.5)*(pt_1 >= 28.0)) || (((trg_singleelectron_32>0.5)||(trg_singleelectron_32_fallback>0.5))*(pt_1>33)) || ((trg_singleelectron_35>0.5)*(pt_1>36)))*triggerWeight_trg27_trg32_trg35_data_1 + tautriggerefficiencyData*triggerWeight_trg_EleTau_Ele24Leg_data_1*((trg_crosselectron_ele24tau30>0.5)*(pt_1 < 28.0)*(pt_2 > 35.0))) )"
				# cuts["trigger"] = "( (abs(eta_1) <= 1.479) * ( (((trg_singleelectron_27>0.5)) || (((trg_singleelectron_32>0.5)||(trg_singleelectron_32_fallback>0.5))) || ((trg_singleelectron_35>0.5))) * triggerWeight_trg27_trg32_trg35_embed_1 + ((trg_crosselectron_ele24tau30>0.5))*triggerWeight_tauLeg_2*triggerWeight_trg_EleTau_Ele24Leg_embed_1 ) + (abs(eta_1) > 1.479) * (triggerWeight_trg27_trg32_trg35_data_1 + tautriggerefficiencyData*triggerWeight_trg_EleTau_Ele24Leg_data_1) )"
				cuts["trigger"] += "*(triggerWeight_doublemu_1)"
			cuts["pt_1"] = "(pt_1 > 25.0)"
			cuts["pt_2"] = "(pt_2 > 30.0)"
			cuts["eta_1"] = "(abs(eta_1) < 2.1)"
			cuts["eta_2"] = "(abs(eta_2) < 2.1)"
			cuts["mt"] = "(mt_1<50.0)"
			cuts["iso_1"] = "(iso_1 < 0.15)"
			cuts["iso_2"] = "(byTightIsolationMVArun2017v2DBoldDMwLT2017_2 > 0.5)"

		elif channel == "tt":
			cuts["trigger"] = "( ((HLT_DoubleTightChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg > 0.5) * (pt_1 > 40) * (pt_2 > 40)) || ((HLT_DoubleMediumChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg > 0.5) * (pt_1 > 45) * (pt_2 > 45)) || ((HLT_DoubleTightChargedIsoPFTau40_Trk1_eta2p1_Reg > 0.5) * (pt_1 > 45) * (pt_2 > 45) ) )"
			if not data and not ("emb" in cut_type):
				# tauidtriggersf_1 = "((byVLooseIsolationMVArun2017v2DBoldDMwLT2017_1 > 0.5)*(byLooseIsolationMVArun2017v2DBoldDMwLT2017_1 < 0.5)*tautriggerefficiencyData_1_vloose/((tautriggerefficiencyMC_1_vloose > 0)*tautriggerefficiencyMC_1_vloose + (tautriggerefficiencyMC_1_vloose == 0)*1.0) + (byLooseIsolationMVArun2017v2DBoldDMwLT2017_1 > 0.5)*(byMediumIsolationMVArun2017v2DBoldDMwLT2017_1 < 0.5)*tautriggerefficiencyData_1_loose/((tautriggerefficiencyMC_1_loose > 0)*tautriggerefficiencyMC_1_loose + (tautriggerefficiencyMC_1_loose == 0)*1.0) + (byMediumIsolationMVArun2017v2DBoldDMwLT2017_1 > 0.5)*(byTightIsolationMVArun2017v2DBoldDMwLT2017_1 < 0.5)*tautriggerefficiencyData_1_medium/((tautriggerefficiencyMC_1_medium > 0)*tautriggerefficiencyMC_1_medium + (tautriggerefficiencyMC_1_medium == 0)*1.0) + (byTightIsolationMVArun2017v2DBoldDMwLT2017_1 > 0.5)*(byVTightIsolationMVArun2017v2DBoldDMwLT2017_1 < 0.5)*tautriggerefficiencyData_1_tight/((tautriggerefficiencyMC_1_tight > 0)*tautriggerefficiencyMC_1_tight + (tautriggerefficiencyMC_1_tight == 0)*1.0) + (byVTightIsolationMVArun2017v2DBoldDMwLT2017_1 > 0.5)*(byVVTightIsolationMVArun2017v2DBoldDMwLT2017_1 < 0.5)*tautriggerefficiencyData_1_vtight/((tautriggerefficiencyMC_1_vtight > 0)*tautriggerefficiencyMC_1_vtight + (tautriggerefficiencyMC_1_vtight == 0)*1.0) + (byVVTightIsolationMVArun2017v2DBoldDMwLT2017_1 > 0.5)*tautriggerefficiencyData_1_vvtight/((tautriggerefficiencyMC_1_vvtight > 0)*tautriggerefficiencyMC_1_vvtight + (tautriggerefficiencyMC_1_vvtight == 0)*1.0))"
				# tauidtriggersf_2 = "((byVLooseIsolationMVArun2017v2DBoldDMwLT2017_2 > 0.5)*(byLooseIsolationMVArun2017v2DBoldDMwLT2017_2 < 0.5)*tautriggerefficiencyData_2_vloose/((tautriggerefficiencyMC_2_vloose > 0)*tautriggerefficiencyMC_2_vloose + (tautriggerefficiencyMC_2_vloose == 0)*1.0) + (byLooseIsolationMVArun2017v2DBoldDMwLT2017_2 > 0.5)*(byMediumIsolationMVArun2017v2DBoldDMwLT2017_2 < 0.5)*tautriggerefficiencyData_2_loose/((tautriggerefficiencyMC_2_loose > 0)*tautriggerefficiencyMC_2_loose + (tautriggerefficiencyMC_2_loose == 0)*1.0) + (byMediumIsolationMVArun2017v2DBoldDMwLT2017_2 > 0.5)*(byTightIsolationMVArun2017v2DBoldDMwLT2017_2 < 0.5)*tautriggerefficiencyData_2_medium/((tautriggerefficiencyMC_2_medium > 0)*tautriggerefficiencyMC_2_medium + (tautriggerefficiencyMC_2_medium == 0)*1.0) + (byTightIsolationMVArun2017v2DBoldDMwLT2017_2 > 0.5)*(byVTightIsolationMVArun2017v2DBoldDMwLT2017_2 < 0.5)*tautriggerefficiencyData_2_tight/((tautriggerefficiencyMC_2_tight > 0)*tautriggerefficiencyMC_2_tight + (tautriggerefficiencyMC_2_tight == 0)*1.0) + (byVTightIsolationMVArun2017v2DBoldDMwLT2017_2 > 0.5)*(byVVTightIsolationMVArun2017v2DBoldDMwLT2017_2 < 0.5)*tautriggerefficiencyData_2_vtight/((tautriggerefficiencyMC_2_vtight > 0)*tautriggerefficiencyMC_2_vtight + (tautriggerefficiencyMC_2_vtight == 0)*1.0) + (byVVTightIsolationMVArun2017v2DBoldDMwLT2017_2 > 0.5)*tautriggerefficiencyData_2_vvtight/((tautriggerefficiencyMC_2_vvtight > 0)*tautriggerefficiencyMC_2_vvtight + (tautriggerefficiencyMC_2_vvtight == 0)*1.0))"
				tauidtriggersf_1 = "triggerWeight_tautaucross_1"
				tauidtriggersf_2 = "triggerWeight_tautaucross_2"
				cuts["trigger"] += "*" + tauidtriggersf_1 + "*" + tauidtriggersf_2
			elif "emb" in cut_type:
				cuts["trigger"] += "*triggerWeight_tau_1*triggerWeight_tau_2"
				cuts["trigger"] += "*triggerWeight_doublemu_1"
			cuts["pt_1"] = "(pt_1 > 50.0)"
			cuts["pt_2"] = "(pt_2 > 40.0)"
			cuts["eta_1"] = "(abs(eta_1) < 2.1)"
			cuts["eta_2"] = "(abs(eta_2) < 2.1)"
			cuts["iso_1"] = "(byTightIsolationMVArun2017v2DBoldDMwLT2017_1 > 0.5)"
			cuts["iso_2"] = "(byTightIsolationMVArun2017v2DBoldDMwLT2017_2 > 0.5)"

		return cuts

	@staticmethod
	def cptautau2017legacy(channel, cut_type, **kwargs):
		data = kwargs.get("data", False)
		embedding = kwargs.get("embedding", False)
		cuts = CutStringsDict.baseline(channel, cut_type, **kwargs)
		cuts["bveto"] = "(nbtag == 0)"
		cuts["prefiringWeight"] = "(1.0)" if "emb" in cut_type else "(prefiringWeight)"

		if channel == "mt":
			# if data :
				# cuts["trigger"] = "((((pt_1 >= 25.0)*(trg_singlemuon_24>0.5))||((pt_1 >= 28.0)*(trg_singlemuon_27>0.5))) + ((pt_1 < 25.0)*(pt_2 > 32.0)*(abs(eta_2) < 2.1)*(trg_crossmuon_mu20tau27>0.5)))"
			# else:
				# cuts["trigger"] = "((((pt_1 >= 25.0)*(trg_singlemuon_24>0.5))||((pt_1 >= 28.0)*(trg_singlemuon_27>0.5)))*triggerWeight_single_1 + ((pt_1 < 25.0)*(pt_2 > 32.0)*(abs(eta_2) < 2.1)*(trg_crossmuon_mu20tau27>0.5)*triggerWeight_cross_1*triggerWeight_cross_2))"
			cuts["trigger"] = "( ((pt_1 > 25.0)*(trg_singlemuon_24>0.5)) || ((pt_1 > 28.0)*(trg_singlemuon_27>0.5)) || ((pt_1 < 25.0)*(pt_2 > 32.0)*(trg_crossmuon_mu20tau27>0.5)) )"
			if not data:
				cuts["trigger"] += "*triggerWeight_comb"
			# cuts["pujetIDweight"] = "pileupJetIDScaleFactorWeight"
			cuts["pt_1"] = "(pt_1 > 21.0)"
			cuts["pt_2"] = "(pt_2 > 30.0)"
			cuts["eta_1"] = "(abs(eta_1) < 2.1)"
			cuts["eta_2"] = "(abs(eta_2) < 2.3)"
			cuts["mt"] = "(mt_1<50.0)"
			cuts["iso_1"] = "(iso_1 < 0.15)"
			cuts["anti_e_tau_discriminators"] = "(byVVLooseDeepTau2017v2p1VSe_2 > 0.5)"
			cuts["anti_mu_tau_discriminators"] = "(byTightDeepTau2017v2p1VSmu_2 > 0.5)"
			cuts["iso_2"] = "(byMediumDeepTau2017v2p1VSjet_2 > 0.5)"
			# cuts["decay_mode_reweight"] = "(0.99/0.97)*((decayModeMVA_2==0)*0.975 + (decayModeMVA_2==1)*0.975*1.051 + (decayModeMVA_2==10)*pow(0.975,3) + (decayModeMVA_2==11)*pow(0.975,3)*1.051)/(((decayMode_2==0)*0.975 + (decayMode_2==1)*0.975*1.051 + (decayMode_2==10)*pow(0.975,3))||(1.0))"
			# cuts["decay_mode_reweight"] = "(0.99/0.97)*((decayMode_2==11)*pow(0.975,3)*1.051 + (decayMode_2!=11))"

		elif channel == "et":
			if data :
				cuts["trigger"] = "( ( (((trg_singleelectron_27>0.5)*(pt_1 >= 28.0)) || (((trg_singleelectron_32>0.5)||(trg_singleelectron_32_fallback>0.5))*(pt_1>33)) || ((trg_singleelectron_35>0.5)*(pt_1>36))) + ((trg_crosselectron_ele24tau30>0.5)*(pt_1 < 28.0)*(pt_2 > 35.0)*(abs(eta_2) < 2.1)) ))"
			else:
				cuts["trigger"] = "( ( (((trg_singleelectron_27>0.5)*(pt_1 >= 28.0)) || (((trg_singleelectron_32>0.5)||(trg_singleelectron_32_fallback>0.5))*(pt_1>33)) || ((trg_singleelectron_35>0.5)*(pt_1>36))) * triggerWeight_single_1 + ((trg_crosselectron_ele24tau30>0.5)*(pt_1 < 28.0)*(pt_2 > 35.0)*(abs(eta_2) < 2.1))*triggerWeight_cross_1*triggerWeight_cross_2))"
			cuts["pt_1"] = "(pt_1 > 25.0)"
			cuts["pt_2"] = "(pt_2 > 30.0)"
			cuts["eta_1"] = "(abs(eta_1) < 2.1)"
			cuts["eta_2"] = "(abs(eta_2) < 2.1)"
			cuts["mt"] = "(mt_1<50.0)"
			cuts["iso_1"] = "(iso_1 < 0.15)"
			cuts["iso_2"] = "(byMediumDeepTau2017v2p1VSjet_2 > 0.5)"
			cuts["anti_e_tau_discriminators"] = "(byTightDeepTau2017v2p1VSe_2 > 0.5)"
			cuts["anti_mu_tau_discriminators"] = "(byVlooseDeepTau2017v2p1VSmu_2 > 0.5)"

		elif channel == "tt":
			cuts["trigger"] = "( ((HLT_DoubleTightChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg > 0.5) * (pt_1 > 40) * (pt_2 > 40)) || ((HLT_DoubleMediumChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg > 0.5) * (pt_1 > 45) * (pt_2 > 45)) || ((HLT_DoubleTightChargedIsoPFTau40_Trk1_eta2p1_Reg > 0.5) * (pt_1 > 45) * (pt_2 > 45) ) )"
			if not data:
				tauidtriggersf_1 = "triggerWeight_cross_1"
				tauidtriggersf_2 = "triggerWeight_cross_2"
				cuts["trigger"] += "*" + tauidtriggersf_1 + "*" + tauidtriggersf_2
			cuts["pt_1"] = "(pt_1 > 40.0)"
			cuts["pt_2"] = "(pt_2 > 40.0)"
			cuts["eta_1"] = "(abs(eta_1) < 2.1)"
			cuts["eta_2"] = "(abs(eta_2) < 2.1)"
			cuts["iso_1"] = "(byMediumDeepTau2017v2p1VSjet_1 > 0.5)"
			cuts["iso_2"] = "(byMediumDeepTau2017v2p1VSjet_2 > 0.5)"
			cuts["anti_e_tau_discriminators_1"] = "(byVVLooseDeepTau2017v2p1VSe_1 > 0.5)"
			cuts["anti_e_tau_discriminators_2"] = "(byVVLooseDeepTau2017v2p1VSe_2 > 0.5)"
			cuts["anti_mu_tau_discriminators_1"] = "(byVLooseDeepTau2017v2p1VSmu_1 > 0.5)"
			cuts["anti_mu_tau_discriminators_2"] = "(byVLooseDeepTau2017v2p1VSmu_2 > 0.5)"

		elif channel == "mm":
			cuts["trigger"] = "(((pt_1 >= 25.0)*(trg_singlemuon_24>0.5))||((pt_1 >= 28.0)*(trg_singlemuon_27>0.5)))"
			cuts["pt_1"] = "(pt_1 > 21.0)"
			cuts["pt_2"] = "(pt_2 > 21.0)"
			cuts["eta_1"] = "(abs(eta_1) < 2.1)"
			cuts["eta_2"] = "(abs(eta_2) < 2.1)"
			cuts["iso_1"] = "(iso_1 < 0.15)"
			cuts["iso_2"] = "(iso_2 < 0.15)"
			if not data:
				cuts["trigger"] += "*(triggerWeight_single_1)"
		return cuts

	@staticmethod
	def lfv(channel, cut_type, **kwargs):
		cuts = CutStringsDict.baseline(channel, cut_type, **kwargs)
		#cuts["nbtag"] = "nbtag==0"
		#cuts["mt"] = ""

		return cuts

	@staticmethod
        def baseline2017legacy(channel, cut_type, **kwargs):
                cuts = CutStringsDict.baseline(channel, cut_type, **kwargs)
                return cuts

	@staticmethod
	def antievloosepass(channel, cut_type, **kwargs):
		if channel == "et":
			cuts = CutStringsDict.baseline(channel, cut_type, **kwargs)
			cuts["mt"] = "(mt_1 < 30.0)"
			cuts["iso_2"] = "(byTightIsolationMVArun2017v2DBoldDMwLT2017_2 > 0.5)*((gen_match_2 == 5)*0.85 + (gen_match_2 != 5))"  if "2017" in cut_type else  "(byTightIsolationMVArun2v1DBoldDMwLT_2 > 0.5)"
			cuts["discriminator"] = "(againstElectronVLooseMVA6_2 > 0.5)"
		else:
			log.fatal("No cut values implemented for channel \"%s\" in \"%s\"" % (channel, cut_type))
			sys.exit(1)
		return cuts

	@staticmethod
	def antievloosefail(channel, cut_type, **kwargs):
		if channel == "et":
			cuts = CutStringsDict.baseline(channel, cut_type, **kwargs)
			cuts["mt"] = "(mt_1 < 30.0)"
			cuts["iso_2"] = "(byTightIsolationMVArun2017v2DBoldDMwLT2017_2 > 0.5)*((gen_match_2 == 5)*0.85 + (gen_match_2 != 5))"  if "2017" in cut_type  else  "(byTightIsolationMVArun2v1DBoldDMwLT_2 > 0.5)"
			cuts["discriminator"] = "(againstElectronVLooseMVA6_2 < 0.5)"
		else:
			log.fatal("No cut values implemented for channel \"%s\" in \"%s\"" % (channel, cut_type))
			sys.exit(1)
		return cuts

	@staticmethod
	def antieloosepass(channel, cut_type, **kwargs):
		if channel == "et":
			cuts = CutStringsDict.baseline(channel, cut_type, **kwargs)
			cuts["mt"] = "(mt_1 < 30.0)"
			cuts["iso_2"] = "(byTightIsolationMVArun2017v2DBoldDMwLT2017_2 > 0.5)*((gen_match_2 == 5)*0.89 + (gen_match_2 != 5))"  if "2017" in cut_type  else  "(byTightIsolationMVArun2v1DBoldDMwLT_2 > 0.5)"
			cuts["discriminator"] = "(againstElectronLooseMVA6_2 > 0.5)"
		else:
			log.fatal("No cut values implemented for channel \"%s\" in \"%s\"" % (channel, cut_type))
			sys.exit(1)
		return cuts

	@staticmethod
	def antieloosefail(channel, cut_type, **kwargs):
		if channel == "et":
			cuts = CutStringsDict.baseline(channel, cut_type, **kwargs)
			cuts["mt"] = "(mt_1 < 30.0)"
			cuts["iso_2"] = "(byTightIsolationMVArun2017v2DBoldDMwLT2017_2 > 0.5)*((gen_match_2 == 5)*0.89 + (gen_match_2 != 5))"  if "2017" in cut_type  else  "(byTightIsolationMVArun2v1DBoldDMwLT_2 > 0.5)"
			cuts["discriminator"] = "(againstElectronLooseMVA6_2 < 0.5)"
		else:
			log.fatal("No cut values implemented for channel \"%s\" in \"%s\"" % (channel, cut_type))
			sys.exit(1)
		return cuts

	@staticmethod
	def antiemediumpass(channel, cut_type, **kwargs):
		if channel == "et":
			cuts = CutStringsDict.baseline(channel, cut_type, **kwargs)
			cuts["mt"] = "(mt_1 < 30.0)"
			cuts["iso_2"] = "(byTightIsolationMVArun2017v2DBoldDMwLT2017_2 > 0.5)*((gen_match_2 == 5)*0.89 + (gen_match_2 != 5))"  if "2017" in cut_type  else  "(byTightIsolationMVArun2v1DBoldDMwLT_2 > 0.5)"
			cuts["discriminator"] = "(againstElectronMediumMVA6_2 > 0.5)"
		else:
			log.fatal("No cut values implemented for channel \"%s\" in \"%s\"" % (channel, cut_type))
			sys.exit(1)
		return cuts

	@staticmethod
	def antiemediumfail(channel, cut_type, **kwargs):
		if channel == "et":
			cuts = CutStringsDict.baseline(channel, cut_type, **kwargs)
			cuts["mt"] = "(mt_1 < 30.0)"
			cuts["iso_2"] = "(byTightIsolationMVArun2017v2DBoldDMwLT2017_2 > 0.5)*((gen_match_2 == 5)*0.89 + (gen_match_2 != 5))"  if "2017" in cut_type  else  "(byTightIsolationMVArun2v1DBoldDMwLT_2 > 0.5)"
			cuts["discriminator"] = "(againstElectronMediumMVA6_2 < 0.5)"
		else:
			log.fatal("No cut values implemented for channel \"%s\" in \"%s\"" % (channel, cut_type))
			sys.exit(1)
		return cuts

	@staticmethod
	def antietightpass(channel, cut_type, **kwargs):
		if channel == "et":
			cuts = CutStringsDict.baseline(channel, cut_type, **kwargs)
			cuts["mt"] = "(mt_1 < 30.0)"
			cuts["iso_2"] = "(byTightIsolationMVArun2017v2DBoldDMwLT2017_2 > 0.5)*((gen_match_2 == 5)*0.87 + (gen_match_2 != 5))"  if "2017" in cut_type  else  "(byTightIsolationMVArun2v1DBoldDMwLT_2 > 0.5)"
			cuts["discriminator"] = "(againstElectronTightMVA6_2 > 0.5)"
		else:
			log.fatal("No cut values implemented for channel \"%s\" in \"%s\"" % (channel, cut_type))
			sys.exit(1)
		return cuts

	@staticmethod
	def antietightfail(channel, cut_type, **kwargs):
		if channel == "et":
			cuts = CutStringsDict.baseline(channel, cut_type, **kwargs)
			cuts["mt"] = "(mt_1 < 30.0)"
			cuts["iso_2"] = "(byTightIsolationMVArun2017v2DBoldDMwLT2017_2 > 0.5)*((gen_match_2 == 5)*0.87 + (gen_match_2 != 5))"  if "2017" in cut_type  else  "(byTightIsolationMVArun2v1DBoldDMwLT_2 > 0.5)"
			cuts["discriminator"] = "(againstElectronTightMVA6_2 < 0.5)"
		else:
			log.fatal("No cut values implemented for channel \"%s\" in \"%s\"" % (channel, cut_type))
			sys.exit(1)
		return cuts

	@staticmethod
	def antievtightpass(channel, cut_type, **kwargs):
		if channel == "et":
			cuts = CutStringsDict.baseline(channel, cut_type, **kwargs)
			cuts["mt"] = "(mt_1 < 30.0)"
			cuts["iso_2"] = "(byTightIsolationMVArun2017v2DBoldDMwLT2017_2 > 0.5)*((gen_match_2 == 5)*0.85 + (gen_match_2 != 5))"  if "2017" in cut_type else  "(byTightIsolationMVArun2v1DBoldDMwLT_2 > 0.5)"
			cuts["discriminator"] = "(againstElectronVTightMVA6_2 > 0.5)"
		else:
			log.fatal("No cut values implemented for channel \"%s\" in \"%s\"" % (channel, cut_type))
			sys.exit(1)
		return cuts

	@staticmethod
	def antievtightfail(channel, cut_type, **kwargs):
		if channel == "et":
			cuts = CutStringsDict.baseline(channel, cut_type, **kwargs)
			cuts["mt"] = "(mt_1 < 30.0)"
			cuts["iso_2"] = "(byTightIsolationMVArun2017v2DBoldDMwLT2017_2 > 0.5)*((gen_match_2 == 5)*0.85 + (gen_match_2 != 5))"  if "2017" in cut_type else  "(byTightIsolationMVArun2v1DBoldDMwLT_2 > 0.5)"
			cuts["discriminator"] = "(againstElectronVTightMVA6_2 < 0.5)"
		else:
			log.fatal("No cut values implemented for channel \"%s\" in \"%s\"" % (channel, cut_type))
			sys.exit(1)
		return cuts

	@staticmethod
	def antieinclusive(channel, cut_type, **kwargs):
		if channel == "et":
			cuts = CutStringsDict.baseline(channel, cut_type, **kwargs)
			cuts["mt"] = "(mt_1 < 30.0)"
			cuts["iso_2"] = "(byTightIsolationMVArun2017v2DBoldDMwLT2017_2 > 0.5)" if "2017" in cut_type else  "(byTightIsolationMVArun2v1DBoldDMwLT_2 > 0.5)"
		else:
			log.fatal("No cut values implemented for channel \"%s\" in \"%s\"" % (channel, cut_type))
			sys.exit(1)
		return cuts

	@staticmethod
	def antimuloosepass(channel, cut_type, **kwargs):
		if channel == "mt":
			cuts = CutStringsDict.baseline(channel, cut_type, **kwargs)
			cuts["pzeta"] = "(pZetaMissVis > -20.0)"
			cuts["discriminator"] = "(againstMuonLoose3_2 > 0.5)"
		else:
			log.fatal("No cut values implemented for channel \"%s\" in \"%s\"" % (channel, cut_type))
			sys.exit(1)
		return cuts

	@staticmethod
	def antimuloosefail(channel, cut_type, **kwargs):
		if channel == "mt":
			cuts = CutStringsDict.baseline(channel, cut_type, **kwargs)
			#cuts["pzeta"] = "(pZetaMissVis > -20.0)"
			cuts["discriminator"] = "(againstMuonLoose3_2 < 0.5)"
		else:
			log.fatal("No cut values implemented for channel \"%s\" in \"%s\"" % (channel, cut_type))
			sys.exit(1)
		return cuts

	@staticmethod
	def antimutightpass(channel, cut_type, **kwargs):
		if channel == "mt":
			cuts = CutStringsDict.baseline(channel, cut_type, **kwargs)
			#cuts["pzeta"] = "(pZetaMissVis > -20.0)"
			cuts["discriminator"] = "(againstMuonTight3_2 > 0.5)"
		else:
			log.fatal("No cut values implemented for channel \"%s\" in \"%s\"" % (channel, cut_type))
			sys.exit(1)
		return cuts

	@staticmethod
	def antimutightfail(channel, cut_type, **kwargs):
		if channel == "mt":
			cuts = CutStringsDict.baseline(channel, cut_type, **kwargs)
			#cuts["pzeta"] = "(pZetaMissVis > -20.0)"
			cuts["discriminator"] = "(againstMuonTight3_2 < 0.5)"
		else:
			log.fatal("No cut values implemented for channel \"%s\" in \"%s\"" % (channel, cut_type))
			sys.exit(1)
		return cuts

	@staticmethod
	def tauidloosepass(channel, cut_type, **kwargs):
		if channel in ["mt", "et"]:
			cuts = CutStringsDict.baseline(channel, cut_type, **kwargs)
			cuts["pzeta"] = "(pZetaMissVis > -25.0)"
			cuts["bveto"] = "(nbtag == 0)"
			cuts["discriminator"] = "(byLooseIsolationMVArun2v1DBoldDMwLT_2 > 0.5)"
		else:
			log.fatal("No cut values implemented for channel \"%s\" in \"%s\"" % (channel, cut_type))
			sys.exit(1)
		return cuts

	@staticmethod
	def tauidloosefail(channel, cut_type, **kwargs):
		if channel in ["mt", "et"]:
			cuts = CutStringsDict.baseline(channel, cut_type, **kwargs)
			cuts["pzeta"] = "(pZetaMissVis > -25.0)"
			cuts["bveto"] = "(nbtag == 0)"
			cuts["discriminator"] = "(byLooseIsolationMVArun2v1DBoldDMwLT_2 < 0.5)"
		else:
			log.fatal("No cut values implemented for channel \"%s\" in \"%s\"" % (channel, cut_type))
			sys.exit(1)
		return cuts

	@staticmethod
	def tauidmediumpass(channel, cut_type, **kwargs):
		if channel in ["mt", "et"]:
			cuts = CutStringsDict.baseline(channel, cut_type, **kwargs)
			cuts["pzeta"] = "(pZetaMissVis > -25.0)"
			cuts["bveto"] = "(nbtag == 0)"
			cuts["discriminator"] = "(byMediumIsolationMVArun2v1DBoldDMwLT_2 > 0.5)"
		else:
			log.fatal("No cut values implemented for channel \"%s\" in \"%s\"" % (channel, cut_type))
			sys.exit(1)
		return cuts

	@staticmethod
	def tauidmediumfail(channel, cut_type, **kwargs):
		if channel in ["mt", "et"]:
			cuts = CutStringsDict.baseline(channel, cut_type, **kwargs)
			cuts["pzeta"] = "(pZetaMissVis > -25.0)"
			cuts["bveto"] = "(nbtag == 0)"
			cuts["discriminator"] = "(byMediumIsolationMVArun2v1DBoldDMwLT_2 < 0.5)"
		else:
			log.fatal("No cut values implemented for channel \"%s\" in \"%s\"" % (channel, cut_type))
			sys.exit(1)
		return cuts

	@staticmethod
	def tauidtightpass(channel, cut_type, **kwargs):
		if channel in ["mt", "et"]:
			cuts = CutStringsDict.baseline(channel, cut_type, **kwargs)
			cuts["pzeta"] = "(pZetaMissVis > -25.0)"
			cuts["bveto"] = "(nbtag == 0)"
			cuts["discriminator"] = "(byTightIsolationMVArun2v1DBoldDMwLT_2 > 0.5)"
		else:
			log.fatal("No cut values implemented for channel \"%s\" in \"%s\"" % (channel, cut_type))
			sys.exit(1)
		return cuts

	@staticmethod
	def tauidtightfail(channel, cut_type, **kwargs):
		if channel in ["mt", "et"]:
			cuts = CutStringsDict.baseline(channel, cut_type, **kwargs)
			cuts["pzeta"] = "(pZetaMissVis > -25.0)"
			cuts["bveto"] = "(nbtag == 0)"
			cuts["discriminator"] = "(byTightIsolationMVArun2v1DBoldDMwLT_2 < 0.5)"
		else:
			log.fatal("No cut values implemented for channel \"%s\" in \"%s\"" % (channel, cut_type))
			sys.exit(1)
		return cuts

	@staticmethod
	def tauidvtightpass(channel, cut_type, **kwargs):
		if channel in ["mt", "et"]:
			cuts = CutStringsDict.baseline(channel, cut_type, **kwargs)
			cuts["pzeta"] = "(pZetaMissVis > -25.0)"
			cuts["bveto"] = "(nbtag == 0)"
			cuts["discriminator"] = "(byVTightIsolationMVArun2v1DBoldDMwLT_2 > 0.5)"
		else:
			log.fatal("No cut values implemented for channel \"%s\" in \"%s\"" % (channel, cut_type))
			sys.exit(1)
		return cuts

	@staticmethod
	def tauidvtightfail(channel, cut_type, **kwargs):
		if channel in ["mt", "et"]:
			cuts = CutStringsDict.baseline(channel, cut_type, **kwargs)
			cuts["pzeta"] = "(pZetaMissVis > -25.0)"
			cuts["bveto"] = "(nbtag == 0)"
			cuts["discriminator"] = "(byVTightIsolationMVArun2v1DBoldDMwLT_2 < 0.5)"
		else:
			log.fatal("No cut values implemented for channel \"%s\" in \"%s\"" % (channel, cut_type))
			sys.exit(1)
		return cuts

	@staticmethod
	def tauescuts(channel, cut_type, **kwargs):
		if channel in ["mt", "et"]:
			cuts = CutStringsDict.baseline(channel, cut_type, **kwargs)
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
	def relaxedETauMuTauWJ(channel, cut_type, **kwargs):
		if channel in ["mt", "et"]:
			cuts = CutStringsDict._get_cutdict(channel, cut_type.replace("relaxedETauMuTauWJ",""), **kwargs)
			cuts["iso_1"] = "(iso_1 < 0.3)"
			cuts["iso_2"] = "(byMediumIsolationMVArun2v1DBoldDMwLT_2 > 0.5)*((gen_match_2 == 5)*0.95 + (gen_match_2 != 5))" if "smhtt2016" in cut_type else "(byMediumIsolationMVArun2v1DBoldDMwLT_2 > 0.5)*((gen_match_2 == 5)*0.97 + (gen_match_2 != 5))" if "2016" in cut_type else "(byLooseIsolationMVArun2017v2DBoldDMwLT2017_2 > 0.5)"
		elif channel in ["em", "ttbar"]:
			cuts = CutStringsDict.baseline(channel, cut_type, **kwargs)
			cuts["iso_1"] = "(iso_1 < 0.3)"
			cuts["iso_2"] = "(iso_2 < 0.3)"
		else:
			log.fatal("No cut values implemented for channel \"%s\" in \"%s\"" % (channel, cut_type))
			sys.exit(1)
		return cuts

	@staticmethod
	def antiIsolationRegionQCD(channel, cut_type, **kwargs):
		if channel in ["mt", "et"]:
			cuts = CutStringsDict._get_cutdict(channel, cut_type.replace("relaxedETauMuTauWJ",""), **kwargs)
			cuts["iso_1"] = " ".join("(iso_1 < 0.3)*(iso_1>0.1)" if channel == "mt" else "(iso_1 < 0.3)*(iso_1>0.15)")
		else:
			log.fatal("No cut values implemented for channel \"%s\" in \"%s\"" % (channel, cut_type))
			sys.exit(1)
		return cuts

	def antiIsolationSSRegionQCD(channel, cut_type, **kwargs):
		if channel in ["mt", "et"]:
			cuts = CutStringsDict.antiIsolationRegionQCD(channel, cut_type, **kwargs)
			cuts["ss"] = "((q_1*q_2)>0.0)"
		else:
			log.fatal("No cut values implemented for channel \"%s\" in \"%s\"" % (channel, cut_type))
			sys.exit(1)
		return cuts

	@staticmethod
	def SameSignRegion(channel, cut_type, **kwargs):
		cuts = CutStringsDict._get_cutdict(channel, cut_type.replace("highMtControlRegionWJ","").replace("highMtSSControlRegionWJ","").replace("SameSignRegion",""), **kwargs)
		cuts["ss"] = "((q_1*q_2)>0.0)"
		return cuts

	@staticmethod
	def highMtControlRegionWJ(channel, cut_type, **kwargs):
		if channel in ["mt", "et"]:
			cuts = CutStringsDict._get_cutdict(channel, cut_type.replace("highMtControlRegionWJ","").replace("highMtSSControlRegionWJ","").replace("SameSignRegion",""), **kwargs)
			cuts["mt"] = "(mt_1>70.0)" if ("mssm" in cut_type or "cpggh" in cut_type or "cptautau" in cut_type or "2016" not in cut_type) else "(mt_1>80.0)"
		else:
			log.fatal("No cut values implemented for channel \"%s\" in \"%s\"" % (channel, cut_type))
			sys.exit(1)
		return cuts

	@staticmethod
	def highMtSSControlRegionWJ(channel, cut_type, **kwargs):
		if channel in ["mt", "et"]:
			cuts = CutStringsDict.highMtControlRegionWJ(channel, cut_type, **kwargs)
			cuts["ss"] = "((q_1*q_2)>0.0)"
		else:
			log.fatal("No cut values implemented for channel \"%s\" in \"%s\"" % (channel, cut_type))
			sys.exit(1)
		return cuts

	@staticmethod
	def invertedLeptonIsolation(channel, cut_type, **kwargs):
		if channel in ["mt", "et"]:
			cuts = CutStringsDict._get_cutdict(channel, cut_type.replace("invertedLeptonIsolation",""), **kwargs)
			cuts["iso_1"] = "((iso_1)>0.1)"
		else:
			log.fatal("No cut values implemented for channel \"%s\" in \"%s\"" % (channel, cut_type))
			sys.exit(1)
		return cuts

	@staticmethod
	def invertedTauIsolationFF(channel, cuts, cut_type, **kwargs):
		if channel in ["mt", "et"]:
			cuts["iso_2"] = "((byVLooseIsolationMVArun2017v2DBoldDMwLT2017_2>0.5)*(byTightIsolationMVArun2017v2DBoldDMwLT2017_2<0.5))"
		elif channel in ["tt"]:
			if "invertedTauIsolationFF_1" in cut_type:
				cuts["iso_1"] = "((byVLooseIsolationMVArun2017v2DBoldDMwLT2017_1>0.5)*(byTightIsolationMVArun2017v2DBoldDMwLT2017_1<0.5))"
			elif "invertedTauIsolationFF_2" in cut_type:
				cuts["iso_2"] = "((byVLooseIsolationMVArun2017v2DBoldDMwLT2017_2>0.5)*(byTightIsolationMVArun2017v2DBoldDMwLT2017_2<0.5))"
		else:
			log.fatal("No cut values implemented for channel \"%s\" in \"%s\"" % (channel, cut_type))
			sys.exit(1)
		return cuts

	@staticmethod
	def highMtControlRegionWJFF(channel, cuts, cut_type, **kwargs):
		if channel in ["mt", "et"]:
			cuts["mt"] = "(mt_1>70.0)" if ("mssm" in cut_type or "cpggh" in cut_type or "2016" not in cut_type) else "(mt_1>80.0)"
		else:
			log.fatal("No cut values implemented for channel \"%s\" in \"%s\"" % (channel, cut_type))
			sys.exit(1)
		return cuts

	@staticmethod
	def lowMtZPeakControlRegionDY(channel, cut_type, **kwargs):
		cuts = CutStringsDict._get_cutdict(channel, cut_type.replace("lowMtZPeakControlRegionDY",""), **kwargs)
		cuts["m_sv"] = "(m_sv > 80.0) * (m_sv < 100.0)"
		return cuts


	@staticmethod
	def baseline_low_mvis(channel, cut_type, **kwargs):
		if channel== "gen":
			cuts = {}
		else:
			cuts = CutStringsDict.baseline(channel, cut_type, **kwargs)
			cuts["m_vis"] = "((m_vis > 40.0) * (m_vis < 85.0))"

		return cuts

	# cp final state cuts
	@staticmethod
	def cp2016(channel, cut_type, **kwargs):
		if channel == "mt":
			cuts = CutStringsDict.baseline(channel, cut_type, **kwargs)
			cuts["pt_1"] = "(pt_1 > 20.0)"
			cuts["pt_2"] = "(pt_2 > 20.0)"
		elif channel == "et":
			cuts = CutStringsDict.baseline(channel, cut_type, **kwargs)
			cuts["pt_1"] = "(pt_1 > 26.0)"
			cuts["pt_2"] = "(pt_2 > 20.0)"
		elif channel == "tt":
			cuts = CutStringsDict.baseline(channel, cut_type, **kwargs)
			cuts["pt_1"] = "(pt_1 > 40.0)"
			cuts["pt_2"] = "(pt_2 > 40.0)"
		elif channel == "mm":
			cuts = CutStringsDict.baseline(channel, cut_type, **kwargs)
			cuts["pt_1"] = "(pt_1 > 10.0)"
			cuts["pt_2"] = "(pt_2 > 10.0)"
		elif channel == "em" or channel == "ttbar":
			cuts = CutStringsDict.baseline(channel, cut_type, **kwargs)
			cuts["pt_1"] = "(pt_1 > 13.0)"
			cuts["pt_2"] = "(pt_2 > 10.0)"
		else:
			log.fatal("No cut values implemented for channel \"%s\" in \"%s\"" % (channel, cut_type))
			sys.exit(1)
		return cuts

	def cprho2016(channel, cut_type, **kwargs):
		if channel == "tt":
			cuts = CutStringsDict.cp2016(channel, cut_type, **kwargs)
			cuts["rhodecay"] = "(decayMode_1 == 1)*(decayMode_2 == 1)"

	def cpcomb2016(channel, cut_type, **kwargs):
		if channel == "mt":
			cuts = CutStringsDict.cp2016(channel, cut_type, **kwargs)
			cuts["rhodecay"] = "(decayMode_2 == 1)"
		if channel == "et":
			cuts = CutStringsDict.cp2016(channel, cut_type, **kwargs)
			cuts["rhodecay"] = "(decayMode_2 == 1)"
		if channel == "tt":
			cuts = CutStringsDict.cp2016(channel, cut_type, **kwargs)
			cuts["rhodecay"] = "((decayMode_1 == 1)*(decayMode_2 != 1))+((decayMode_1 != 1)*(decayMode_2 == 1))"

	@staticmethod
	def ztt2015cs(channel, cut_type, **kwargs):
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
	def _get_cutdict(channel, cut_type, **kwargs):
		cuts = {}
		if cut_type=="baseline":
			cuts = CutStringsDict.baseline(channel, cut_type, **kwargs)
		elif cut_type=="baseline2016":
			cuts = CutStringsDict.baseline(channel, cut_type, **kwargs)
		elif cut_type=="baseline2017":
			cuts = CutStringsDict.baseline(channel, cut_type, **kwargs)
		elif cut_type=="smhtt2016":
			cuts = CutStringsDict.baseline(channel, cut_type, **kwargs)
		elif cut_type == "cpggh2016" or cut_type == "cpggh2016_emb":
			cuts = CutStringsDict.cpggh2016(channel, cut_type, **kwargs)
		elif cut_type == "cpggh2017" or cut_type == "cpggh2017_emb":
			cuts = CutStringsDict.cpggh2017(channel, cut_type, **kwargs)
		elif cut_type == "cptautau2017" or cut_type == "cptautau2017_emb":
			cuts = CutStringsDict.cptautau2017(channel, cut_type, **kwargs)
		elif cut_type == "cptautau2017legacy" or cut_type == "cptautau2017legacy_emb":
			cuts = CutStringsDict.cptautau2017legacy(channel, cut_type, **kwargs)
		elif cut_type=="mssm":
			cuts = CutStringsDict.baseline(channel, cut_type, **kwargs)
		elif cut_type=="mssm2016":
			cuts = CutStringsDict.baseline(channel, cut_type, **kwargs)
		elif cut_type=="mssm2016full":
			cuts = CutStringsDict.mssm2016(channel, cut_type, **kwargs)
		elif cut_type=="mssm2016tight":
			cuts = CutStringsDict.mssm2016(channel, cut_type, **kwargs)
		elif cut_type=="mssm2016loosemt":
			cuts = CutStringsDict.mssm2016(channel, cut_type, **kwargs)
		elif cut_type=="mssm2016looseiso":
			cuts = CutStringsDict.mssm2016(channel, cut_type, **kwargs)
		elif cut_type=="mssm2016fffull":
			cuts = CutStringsDict.mssm2016(channel, cut_type, **kwargs)
		elif cut_type=="mssm2016fflooseiso":
			cuts = CutStringsDict.mssm2016(channel, cut_type, **kwargs)

		elif cut_type=="antievloosepass2016" or cut_type=="antievloosepass2017":
			cuts = CutStringsDict.antievloosepass(channel, cut_type, **kwargs)
		elif cut_type=="antievloosefail2016" or cut_type=="antievloosefail2017":
			cuts = CutStringsDict.antievloosefail(channel, cut_type, **kwargs)
		elif cut_type=="antieloosepass2016" or cut_type=="antieloosepass2017":
			cuts = CutStringsDict.antieloosepass(channel, cut_type, **kwargs)
		elif cut_type=="antieloosefail2016" or cut_type=="antieloosefail2017":
			cuts = CutStringsDict.antieloosefail(channel, cut_type, **kwargs)
		elif cut_type=="antiemediumpass2016" or cut_type=="antiemediumpass2017":
			cuts = CutStringsDict.antiemediumpass(channel, cut_type, **kwargs)
		elif cut_type=="antiemediumfail2016" or cut_type=="antiemediumfail2017":
			cuts = CutStringsDict.antiemediumfail(channel, cut_type, **kwargs)
		elif cut_type=="antietightpass2016" or cut_type=="antietightpass2017":
			cuts = CutStringsDict.antietightpass(channel, cut_type, **kwargs)
		elif cut_type=="antietightfail2016" or cut_type=="antietightfail2017":
			cuts = CutStringsDict.antietightfail(channel, cut_type, **kwargs)
		elif cut_type=="antievtightpass2016" or cut_type=="antievtightpass2017":
			cuts = CutStringsDict.antievtightpass(channel, cut_type, **kwargs)
		elif cut_type=="antievtightfail2016" or cut_type=="antievtightfail2017":
			cuts = CutStringsDict.antievtightfail(channel, cut_type, **kwargs)
		elif cut_type=="antieinclusive2017":
			cuts = CutStringsDict.antieinclusive(channel, cut_type, **kwargs)

		elif cut_type=="antimuloosepass":
			cuts = CutStringsDict.antimuloosepass(channel, cut_type, **kwargs)
		elif cut_type=="antimuloosefail":
			cuts = CutStringsDict.antimuloosefail(channel, cut_type, **kwargs)
		elif cut_type=="antimutightpass":
			cuts = CutStringsDict.antimutightpass(channel, cut_type, **kwargs)
		elif cut_type=="antimutightfail":
			cuts = CutStringsDict.antimutightfail(channel, cut_type, **kwargs)

		elif cut_type=="tauidloosepass":
			cuts = CutStringsDict.tauidloosepass(channel, cut_type, **kwargs)
		elif cut_type=="tauidloosefail":
			cuts = CutStringsDict.tauidloosefail(channel, cut_type, **kwargs)
		elif cut_type=="tauidmediumpass":
			cuts = CutStringsDict.tauidmediumpass(channel, cut_type, **kwargs)
		elif cut_type=="tauidmediumfail":
			cuts = CutStringsDict.tauidmediumfail(channel, cut_type, **kwargs)
		elif cut_type=="tauidtightpass":
			cuts = CutStringsDict.tauidtightpass(channel, cut_type, **kwargs)
		elif cut_type=="tauidtightfail":
			cuts = CutStringsDict.tauidtightfail(channel, cut_type, **kwargs)
		elif cut_type=="tauidvtightpass":
			cuts = CutStringsDict.tauidvtightpass(channel, cut_type, **kwargs)
		elif cut_type=="tauidvtightfail":
			cuts = CutStringsDict.tauidvtightfail(channel, cut_type, **kwargs)

		elif "lowMtZPeakControlRegionDY" in cut_type:
			cuts = CutStringsDict.lowMtZPeakControlRegionDY(channel, cut_type, **kwargs)

		elif cut_type=="tauescuts":
			cuts = CutStringsDict.tauescuts(channel, cut_type, **kwargs)
		elif cut_type=="tauescuts2016":
			cuts = CutStringsDict.tauescuts(channel, cut_type, **kwargs)
		elif "relaxedETauMuTauWJ" in cut_type:
			cuts = CutStringsDict.relaxedETauMuTauWJ(channel, cut_type, **kwargs)
		elif "highMtControlRegionWJ" in cut_type:
			cuts = CutStringsDict.highMtControlRegionWJ(channel, cut_type, **kwargs)
		elif "highMtSSControlRegionWJ" in cut_type:
			cuts = CutStringsDict.highMtSSControlRegionWJ(channel, cut_type, **kwargs)
		elif "SameSignRegion" in cut_type:
			cuts = CutStringsDict.SameSignRegion(channel, cut_type, **kwargs)
		elif "invertedLeptonIsolation" in cut_type:
			cuts = CutStringsDict.invertedLeptonIsolation(channel, cut_type, **kwargs)

		elif "low_mvis_smhtt" in cut_type:
			cuts = CutStringsDict.baseline_low_mvis(channel, cut_type, **kwargs)

		elif cut_type=="cp2016":
			cuts = CutStringsDict.cp2016(channel, cut_type, **kwargs)

		elif cut_type=="ztt2015cs":
			cuts = CutStringsDict.ztt2015cs(channel, cut_type, **kwargs)

		elif cut_type=="lfv":
			cuts = CutStringsDict.lfv(channel, cut_type, **kwargs)

		elif cut_type=="baseline2017legacy":
                        cuts = CutStringsDict.baseline2017legacy(channel, cut_type, **kwargs)

		else:
			log.fatal("No cut dictionary implemented for \"%s\"!" % cut_type)
			sys.exit(1)
		return cuts
