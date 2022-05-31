
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import copy
import re

class SystematicsFactory(dict):
	def __init__(self):
		super(SystematicsFactory, self).__init__()
		
		self["nominal"] = Nominal
		self["CMS_scale_j_13TeV"] = JecUncSystematic
		self["CMS_scale_t_13TeV"] = TauEsSystematic
		self["CMS_ztt_scale_mFakeTau_13TeV"] = MuFakeTauEsSystematic
		self["CMS_ztt_scale_eFakeTau_13TeV"] = EleFakeTauEsSystematic
		self["CMS_htt_ttbarShape_13TeV"] = TTBarShapeSystematic
		self["CMS_htt_dyShape_13TeV"] = DYShapeSystematic
		self["CMS_ztt_jetFakeTau_qcd_Shape_13TeV"] = JetFakeTauQCDShapeSystematic
		self["CMS_ztt_jetFakeTau_w_Shape_13TeV"] = JetFakeTauWShapeSystematic
		self["CMS_ztt_jetFakeTau_tt_corr_Shape_13TeV"] = JetFakeTauTTcorrShapeSystematic
		self["CMS_ztt_jetFakeTau_tt_stat_Shape_13TeV"] = JetFakeTauTTstatShapeSystematic
		self["CMS_ztt_jetFakeTau_frac_qcd_Shape_13TeV"] = JetFakeTauFracQCDShapeSystematic
		self["CMS_ztt_jetFakeTau_frac_w_Shape_13TeV"] = JetFakeTauFracWShapeSystematic
		self["CMS_ztt_jetFakeTau_frac_tt_Shape_13TeV"] = JetFakeTauFracTTShapeSystematic
		self["CMS_ztt_jetFakeTau_frac_dy_Shape_13TeV"] = JetFakeTauFracDYShapeSystematic
		self["CMS_eff_b_13TeV"] = BTagSystematic
		self["CMS_mistag_b_13TeV"] = BMistagSystematic
		self["CMS_eFakeTau_1prong_13TeV"] = ElectronToTauOneProngFakeSystematic
		self["CMS_eFakeTau_1prong1pizero_13TeV"] = ElectronToTauOneProngPiZerosFakeSystematic
		self["CMS_eFakeTau_eta_13TeV"] = ElectronToTauFakeSystematic
		self["CMS_mFakeTau_1prong_13TeV"] = MuonToTauOneProngFakeSystematic
		self["CMS_mFakeTau_1prong1pizero_13TeV"] = MuonToTauOneProngPiZerosFakeSystematic
		self["CMS_mFakeTau_eta_13TeV"] = MuonToTauFakeSystematic
		self["CMS_htt_jetToTauFake_13TeV"] = JetToTauFakeSystematic
		self["CMS_htt_jetToTauFake_pi_13TeV"] = JetToTauFakeSystematic
		self["CMS_htt_jetToTauFake_rho_13TeV"] = JetToTauFakeSystematic
		self["CMS_htt_jetToTauFake_a1_13TeV"] = JetToTauFakeSystematic
		self["CMS_htt_jetToTauFake_pi_pi_13TeV"] = JetToTauFakeSystematic
		self["CMS_htt_jetToTauFake_rho_pi_13TeV"] = JetToTauFakeSystematic
		self["CMS_htt_jetToTauFake_rho_rho_13TeV"] = JetToTauFakeSystematic
		self["CMS_htt_jetToTauFake_a1_pi_13TeV"] = JetToTauFakeSystematic
		self["CMS_htt_jetToTauFake_a1_rho_13TeV"] = JetToTauFakeSystematic
		self["CMS_htt_jetToTauFake_a1_a1_13TeV"] = JetToTauFakeSystematic
		self["CMS_scale_met_clustered_13TeV"] = MetJetEnSystematic
		self["CMS_scale_met_unclustered_13TeV"] = MetUnclusteredEnSystematic
		self["CMS_tauIDvsJets_pt_13TeV"] = TauIDvsJetsSystematic
		self["CMS_tauTrigger_pt_13TeV"] = TauTriggerSystematic
		self["CMS_tauDMReco_1prong_13TeV"] = TauDMRecoOneProngSystematic
		self["CMS_tauDMReco_1prong1pizero_13TeV"] = TauDMRecoOneProngPiZerosSystematic
		self["CMS_tauDMReco_3prong_13TeV"] = TauDMRecoThreeProngSystematic
		self["CMS_recoTauDecayModeFake_pi_13TeV"] = RecoTauDecayModeFakePiSystematic
		self["CMS_recoTauDecayModeFake_rho_13TeV"] = RecoTauDecayModeFakeRhoSystematic
		self["CMS_recoTauDecayModeFake_a1_13TeV"] = RecoTauDecayModeFakeA1Systematic
#		self["CMS_genTauDecayModeFake_pi_13TeV"] = GenTauDecayModeFakePiSystematic
#		self["CMS_genTauDecayModeFake_rho_13TeV"] = GenTauDecayModeFakeRhoSystematic
#		self["CMS_genTauDecayModeFake_a1_13TeV"] = GenTauDecayModeFakeA1Systematic
		self["CMS_ZLShape_mt_1prong_13TeV"] = MuonFakeOneProngTauEnergyScaleSystematic
		self["CMS_ZLShape_mt_1prong1pizero_13TeV"] = MuonFakeOneProngPiZerosTauEnergyScaleSystematic
		self["CMS_ZLShape_et_1prong_13TeV"] = ElectronFakeOneProngTauEnergyScaleSystematic
		self["CMS_ZLShape_et_1prong1pizero_13TeV"] = ElectronFakeOneProngPiZerosTauEnergyScaleSystematic
		self["CMS_scale_gg_13TeV"] = GGHRenormalizationScaleSystematic
		self["CMS_scale_e_13TeV"] = EleEsSystematic
		self["CMS_scale_t_1prong_13TeV"] = TauESOneProngSystematic
		self["CMS_scale_t_1prong1pizero_13TeV"] = TauESOneProngPiZerosSystematic
		self["CMS_scale_t_3prong_13TeV"] = TauESThreeProngSystematic
		self["CMS_WSFUncert_mt_0jet_13TeV"] = WJetScaleFactor0JetSystematic
		self["CMS_WSFUncert_et_0jet_13TeV"] = WJetScaleFactor0JetSystematic
		self["CMS_WSFUncert_mt_boosted_13TeV"] = WJetScaleFactorBoostedSystematic
		self["CMS_WSFUncert_et_boosted_13TeV"] = WJetScaleFactorBoostedSystematic
		self["CMS_WSFUncert_mt_vbf_13TeV"] = WJetScaleFactorVbfSystematic
		self["CMS_WSFUncert_et_vbf_13TeV"] = WJetScaleFactorVbfSystematic
		self["WSFUncert_mt_0jet_13TeV"] = self["CMS_WSFUncert_mt_0jet_13TeV"]
		self["WSFUncert_et_0jet_13TeV"] = self["CMS_WSFUncert_et_0jet_13TeV"]
		self["WSFUncert_mt_boosted_13TeV"] = self["CMS_WSFUncert_mt_boosted_13TeV"]
		self["WSFUncert_et_boosted_13TeV"] = self["CMS_WSFUncert_et_boosted_13TeV"]
		self["WSFUncert_mt_vbf_13TeV"] = self["CMS_WSFUncert_mt_vbf_13TeV"]
		self["WSFUncert_et_vbf_13TeV"] = self["CMS_WSFUncert_et_vbf_13TeV"]
		self["CMS_ttbar_embeded_13TeV"] = EmbeddingTTBarContaminationSystematic

		self["CMS_FiniteQuarkMass_13TeV"] = CMS_FiniteQuarkMass_13TeV

		self["CMS_scale_j_eta0to5_corr_13TeV"] = CMS_scale_j_eta0to5_corr_13TeV
		self["CMS_scale_j_eta0to3_corr_13TeV"] = CMS_scale_j_eta0to3_corr_13TeV
		self["CMS_scale_j_eta3to5_corr_13TeV"] = CMS_scale_j_eta3to5_corr_13TeV

		self["CMS_scale_j_eta0to5_uncorr_13TeV"] = CMS_scale_j_eta0to5_uncorr_13TeV
		self["CMS_scale_j_eta0to3_uncorr_13TeV"] = CMS_scale_j_eta0to3_uncorr_13TeV
		self["CMS_scale_j_eta3to5_uncorr_13TeV"] = CMS_scale_j_eta3to5_uncorr_13TeV

		self["CMS_scale_j_RelativeBal_13TeV"] = CMS_scale_j_RelativeBal_13TeV
		self["CMS_scale_j_RelativeSample_13TeV"] = CMS_scale_j_RelativeSample_13TeV
		
		for channel in ["mt", "et", "tt"]:
			self["CMS_scale_t_"+channel+"_13TeV"] = TauEsSystematic

		for channel in ["em", "et"]:
			self["CMS_scale_e_"+channel+"_13TeV"] = EleEsSystematic

		for channel in ["em", "mt"]:
			self["CMS_scale_m_"+channel+"_13TeV"] = MuonEsSystematic

		for channel in ["em", "et", "mt", "tt"]:
			self["CMS_scale_met_"+channel+"_13TeV"] = MetResponseSystematic

		for channel in ["et"]:
			self["CMS_scale_probetau_"+channel+"_13TeV"] = ProbeTauEsSystematic

		for channel in ["et"]:
			self["CMS_scale_probeele_"+channel+"_13TeV"] = ProbeEleEsSystematic

		for channel in ["et"]:
			self["CMS_scale_tagele_"+channel+"_13TeV"] = TagEleEsSystematic

		for channel in ["et"]:
			self["CMS_scale_massRes_"+channel+"_13TeV"] = MassResSystematic

		for channel in ["et"]:
			self["CMS_scale_massResv2_"+channel+"_13TeV"] = MassResSystematicv2
		"""
		jecUncertNames = [
			"AbsoluteFlavMap",
			"AbsoluteMPFBias",
			"AbsoluteScale",
			"AbsoluteStat",
			"FlavorQCD",
			"Fragmentation",
			"PileUpDataMC",
			"PileUpPtBB",
			"PileUpPtEC1",
			"PileUpPtEC2",
			"PileUpPtHF",
			"PileUpPtRef",
			"RelativeBal",
			"RelativeFSR",
			"RelativeJEREC1",
			"RelativeJEREC2",
			"RelativeJERHF",
			"RelativePtBB",
			"RelativePtEC1",
			"RelativePtEC2",
			"RelativePtHF",
			"RelativeStatEC",
			"RelativeStatFSR",
			"RelativeStatHF",
			"SinglePionECAL",
			"SinglePionHCAL",
			"TimePtEta",
			"Total",
			"eta0to5",
			"eta0to3",
			"eta3to5",
			"Closure"
		]
		
		for jecUncert in jecUncertNames:
			self["CMS_scale_j_"+jecUncert+"_13TeV"] = JecUncSplitSystematic if jecUncert != "Total" else JecUncSystematic 
		"""
		fakeFactorUncertNames = [
		]

		for channel in ["mt", "et"]:
			fakeFactorUncertNames += [

			        "qcd_dm0_njet0_"+channel+"_stat", #et,mt

			        "qcd_dm0_njet1_"+channel+"_stat", #et,mt

			        "qcd_dm1_njet0_"+channel+"_stat", #et,mt

			        "qcd_dm1_njet1_"+channel+"_stat", #et,mt

				"w_dm0_njet0_"+channel+"_stat", #et,mt

				"w_dm0_njet1_"+channel+"_stat", #et,mt

				"w_dm1_njet0_"+channel+"_stat", #et,mt

				"w_dm1_njet1_"+channel+"_stat", #et,mt

				"tt_dm0_njet0_"+channel+"_stat", #et,mt

				"tt_dm0_njet1_"+channel+"_stat", #et,mt

				"tt_dm1_njet0_"+channel+"_stat", #et,mt

				"tt_dm1_njet1_"+channel+"_stat",  #et,mt

				"sub_syst_" + channel
			]
			fakeFactorUncertNames += ["w_syst"]
			
			fakeFactorUncertNames += ["qcd_"+channel+"_syst", "ff_sub_syst_"+channel]
		#only in next to next artus run, i forgot to add them in cpquantities
		for channel in ["tt"]:
			fakeFactorUncertNames += [
				"w_frac_syst",
				"tt_frac_syst",
				"tt_qcd_met_closure_syst_njets0",
				"tt_qcd_syst_njets0",
				"tt_qcd_met_closure_syst_njets1",
				"tt_qcd_syst_njets1",
				"tt_qcd_met_closure_syst_njets2",
				"tt_qcd_stat_unc1_njets0_mvadm0_sig_gt",
				"tt_qcd_stat_unc1_njets0_mvadm1",
				"tt_qcd_stat_unc1_njets0_mvadm10",
				"tt_qcd_stat_unc1_njets0_mvadm2",
				"tt_qcd_stat_unc1_njets1_mvadm0_sig_gt",
				"tt_qcd_stat_unc1_njets1_mvadm1",
				"tt_qcd_stat_unc1_njets1_mvadm10",
				"tt_qcd_stat_unc1_njets1_mvadm2",
				"tt_qcd_stat_unc1_njets2_mvadm0_sig_gt",
				"tt_qcd_stat_unc1_njets2_mvadm1",
				"tt_qcd_stat_unc1_njets2_mvadm10",
				"tt_qcd_stat_unc1_njets2_mvadm2",
				"tt_qcd_stat_unc2_njets0_mvadm0_sig_gt",
				"tt_qcd_stat_unc2_njets0_mvadm1",
				"tt_qcd_stat_unc2_njets0_mvadm10",
				"tt_qcd_stat_unc2_njets0_mvadm2",
				"tt_qcd_stat_unc2_njets1_mvadm0_sig_gt",
				"tt_qcd_stat_unc2_njets1_mvadm1",
				"tt_qcd_stat_unc2_njets1_mvadm10",
				"tt_qcd_stat_unc2_njets1_mvadm2",
				"tt_qcd_stat_unc2_njets2_mvadm0_sig_gt",
				"tt_qcd_stat_unc2_njets2_mvadm1",
				"tt_qcd_stat_unc2_njets2_mvadm10",
				"tt_qcd_stat_unc2_njets2_mvadm2",
				"tt_sub_syst",
			]


		#TODO: ff_sub_syst_et_0jet and more

		for fakeFactorUncertainty in fakeFactorUncertNames:
			self["ff_"+fakeFactorUncertainty ] = FakeFactorUncSystematic

		# these uncertainties currently need to be implemented in your datacards script
		self["WSFUncert_mt_dijet_boosted_13TeV"] = Nominal
		self["WSFUncert_mt_dijet2D_boosted_13TeV"] = Nominal
		self["WSFUncert_mt_dijet_lowboost_13TeV"] = Nominal
		self["WSFUncert_et_dijet_boosted_13TeV"] = Nominal	
		self["WSFUncert_et_dijet2D_boosted_13TeV"] = Nominal	
		self["WSFUncert_et_dijet_lowboost_13TeV"] = Nominal	
		self["WSFUncert_et_dijet_lowboost_13TeV"] = Nominal	
		self["WSFUncert_mt_dijet_lowM_13TeV"] = Nominal
		self["WSFUncert_et_dijet_lowM_13TeV"] = Nominal	
		self["WSFUncert_mt_dijet_highM_13TeV"] = Nominal
		self["WSFUncert_et_dijet_highM_13TeV"] = Nominal	
		self["WSFUncert_mt_dijet_lowMjj_13TeV"] = Nominal
		self["WSFUncert_et_dijet_lowMjj_13TeV"] = Nominal								
		self["WSFUncert_lt_13TeV"] = Nominal
		self["CMS_WSFUncert_lt_13TeV"] = Nominal
		self["CMS_htt_zmumuShape_VBF_13TeV"] = Nominal
		
		# TODO: Where are these systematics to be implemented?
		self["CMS_ggH_STXSVBF2j"] = Nominal
		self["CMS_ggH_STXSmig12"] = Nominal	
		
		# QCD systematics for the GGH CP analysis.
		self["CMS_em_QCD_0JetRate_13TeV"] = EmuQCDOsssRateSystematic
		self["CMS_em_QCD_1JetRate_13TeV"] = EmuQCDOsssRateSystematic
		self["CMS_em_QCD_0JetShape_13TeV"] = EmuQCDOsssShapeSystematic
		self["CMS_em_QCD_1JetShape_13TeV"] = EmuQCDOsssShapeSystematic
		self["CMS_em_QCD_IsoExtrap_13TeV"] = EmuQCDExtrapSystematic

	
	def get(self, key, default_value=None):
		value = super(SystematicsFactory, self).get(key, default_value)
		if value is None:
			log.error("Could not find implementation for shape systematic \"{syst}\" in SystematicsFactory! Continue with \"nominal\"".format(syst=key))
			value = super(SystematicsFactory, self).get("nominal")
		return value


class SystematicShiftBase(object):

	def __init__(self, plot_config):
		super(SystematicShiftBase, self).__init__()
		self.plot_config = plot_config
	
	def get_config(self, shift=0.0):
		plot_config = copy.deepcopy(self.plot_config)
		
		if shift != 0.0:
			if "FillEmptyHistograms" not in plot_config.get("analysis_modules", []):
				plot_config.setdefault("analysis_modules", []).append("FillEmptyHistograms")
			# TODO: maybe specify more settings
			# plot_config.setdefault("nicks_fill_empty_histograms", []).append(...)
			# plot_config["fill_empty_histograms_integral"] = 1e-5
		
		return plot_config


# w+jets scale factor shifts for different categories
# same uncertainties as used for WHighMTtoLowMT_$BIN_13TeV implented in systematics_libary.py
class WJetScaleFactor0JetSystematic(SystematicShiftBase):
	def get_config(self, shift=0.0):
		plot_config = super(WJetScaleFactor0JetSystematic, self).get_config(shift=shift)	
		
		if shift > 0.0:
			plot_config.setdefault("wjets_scale_factor_shifts", []).append(1.0 + 0.1)
		elif shift < 0.0:
			plot_config.setdefault("wjets_scale_factor_shifts", []).append(1.0 - 0.1)

		return plot_config


class WJetScaleFactorBoostedSystematic(SystematicShiftBase):
	def get_config(self, shift=0.0):
		plot_config = super(WJetScaleFactorBoostedSystematic, self).get_config(shift=shift)	
		
		if shift > 0.0:
			plot_config.setdefault("wjets_scale_factor_shifts", []).append(1.0 + 0.05)
		elif shift < 0.0:
			plot_config.setdefault("wjets_scale_factor_shifts", []).append(1.0 - 0.05)

		return plot_config
		

class WJetScaleFactorVbfSystematic(SystematicShiftBase):
	def get_config(self, shift=0.0):
		plot_config = super(WJetScaleFactorVbfSystematic, self).get_config(shift=shift)	
		
		if shift > 0.0:
			plot_config.setdefault("wjets_scale_factor_shifts", []).append(1.0 + 0.1)
		elif shift < 0.0:
			plot_config.setdefault("wjets_scale_factor_shifts", []).append(1.0 - 0.1)

		return plot_config


class GGHRenormalizationScaleSystematic(SystematicShiftBase):
	
	def __init__(self, plot_config, category):
		super(GGHRenormalizationScaleSystematic, self).__init__(plot_config)
		self.plot_config = plot_config
		self.channel = category.split("_")[0]
		self.category = category.split("_")[1]
	
	def get_config(self, shift=0.0):
		plot_config = super(GGHRenormalizationScaleSystematic, self).get_config(shift=shift)
		
		w = "(1.0)"
		if self.category == "ZeroJet2D":
			if self.channel == "mt":
				w = "(0.929+0.0001702*pt_2)"
			elif self.channel == "et":
				w = "(0.973+0.0003405*pt_2)"
			elif self.channel == "em":
				w = "(0.942-0.0000170*pt_1)"
			elif self.channel == "tt":
				w = "(0.814+0.0027094*pt_1)"
		elif self.category == "Boosted2D":
			if self.channel == "mt":
				w = "(0.919+0.0010055*H_pt)"
			elif self.channel == "et":
				w = "(0.986-0.0000278*H_pt)"
			elif self.channel == "em":
				w = "(0.936+0.0008871*H_pt)"
			elif self.channel == "tt":
				w = "(0.973+0.0008596*H_pt)"
		elif self.category == "Vbf2D":
			if self.channel == "mt":
				w = "(1.026+0.000066*mjj)"
			elif self.channel == "et":
				w = "(0.971+0.0000327*mjj)"
			elif self.channel == "em":
				w = "(1.032+0.000102*mjj)"
			elif self.channel == "tt":
				w = "(1.094+0.0000545*mjj)"
	
		for index, weight in enumerate(plot_config.get("weights", [])):
			if (shift != 0.0) and (not "Run201" in plot_config["files"][index]) and (not "gen_ztt" in plot_config["nicks"][index]):
				if shift > 0.0:
					plot_config["weights"][index] = weight+"*"+w
				else:
					plot_config["weights"][index] = weight+"*(2-"+w+")"
		
		return plot_config


class Nominal(SystematicShiftBase):
	pass

class FakeFactorUncSystematic(SystematicShiftBase):
	
	def __init__(self, plot_config, fakeFactorUncertainty):
		super(FakeFactorUncSystematic, self).__init__(plot_config)
		self.plot_config = plot_config
		self.fakeFactorUncertainty = fakeFactorUncertainty

		"""
		"qcd_dm0_njet0_"+channel+"_stat", #et,mt

		"qcd_dm0_njet1_"+channel+"_stat", #et,mt

	        "qcd_dm1_njet0_"+channel+"_stat", #et,mt

	        "qcd_dm1_njet1_"+channel+"_stat", #et,mt

		"w_dm0_njet0_"+channel+"_stat", #et,mt

		"w_dm0_njet1_"+channel+"_stat", #et,mt

		"w_dm1_njet0_"+channel+"_stat", #et,mt

		"w_dm1_njet1_"+channel+"_stat", #et,mt

		"tt_dm0_njet0_"+channel+"_stat", #et,mt

		"tt_dm0_njet1_"+channel+"_stat", #et,mt

		"tt_dm1_njet0_"+channel+"_stat", #et,mt

		"tt_dm1_njet1_"+channel+"_stat",  #et,mt

		"sub_syst_" + channel

		"w_syst"
			
		"qcd_"+channel+"_syst", "ff_sub_syst_"+channel
		"""


		self.fakefactordict = {}
		for channel in ["mt", "et"]:
			self.fakefactordict["ff_qcd_dm0_njet0_"+channel+"_stat"] = "fakefactorWeight_qcd_dm0_njet0_stat_"
			self.fakefactordict["ff_qcd_dm0_njet1_"+channel+"_stat"] = "fakefactorWeight_qcd_dm0_njet1_stat_"
			self.fakefactordict["ff_qcd_dm1_njet0_"+channel+"_stat"] = "fakefactorWeight_qcd_dm1_njet0_stat_"
			self.fakefactordict["ff_qcd_dm1_njet1_"+channel+"_stat"] = "fakefactorWeight_qcd_dm1_njet1_stat_"

			self.fakefactordict["ff_w_dm0_njet0_"+channel+"_stat"]   = "fakefactorWeight_w_dm0_njet0_stat_"
			self.fakefactordict["ff_w_dm0_njet1_"+channel+"_stat"]   = "fakefactorWeight_w_dm0_njet1_stat_"
			self.fakefactordict["ff_w_dm1_njet0_"+channel+"_stat"]   = "fakefactorWeight_w_dm1_njet0_stat_"
			self.fakefactordict["ff_w_dm1_njet1_"+channel+"_stat"]   = "fakefactorWeight_w_dm1_njet1_stat_"

			self.fakefactordict["ff_tt_dm0_njet0_"+channel+"_stat"]  = "fakefactorWeight_tt_dm0_njet0_stat_"
			self.fakefactordict["ff_tt_dm0_njet1_"+channel+"_stat"]  = "fakefactorWeight_tt_dm0_njet1_stat_"
			self.fakefactordict["ff_tt_dm1_njet0_"+channel+"_stat"]  = "fakefactorWeight_tt_dm1_njet0_stat_"
			self.fakefactordict["ff_tt_dm1_njet1_"+channel+"_stat"]  = "fakefactorWeight_tt_dm1_njet1_stat_"

			self.fakefactordict["ff_qcd_"+channel+"_syst"] = "fakefactorWeight_qcd_syst_"

		self.fakefactordict["ff_tt_qcd_met_closure_syst_njets0"] = ["ffWeight_medium_mvadmbins_qcd_met_", "ffWeight_medium_mvadmbins_qcd_met_*(njets==0)+ffWeight_medium_mvadmbins_1*(njets!=0)"]
		self.fakefactordict["ff_tt_qcd_syst_njets0"] 			 = ["ffWeight_medium_mvadmbins_qcd_syst_", "ffWeight_medium_mvadmbins_qcd_syst_*(njets==0)+ffWeight_medium_mvadmbins_1*(njets!=0)"]
		self.fakefactordict["ff_tt_qcd_met_closure_syst_njets1"] = ["ffWeight_medium_mvadmbins_qcd_met_", "ffWeight_medium_mvadmbins_qcd_met_*(njets==1)+ffWeight_medium_mvadmbins_1*(njets!=1)"]
		self.fakefactordict["ff_tt_qcd_syst_njets1"]			 = ["ffWeight_medium_mvadmbins_qcd_syst_", "ffWeight_medium_mvadmbins_qcd_syst_*(njets==1)+ffWeight_medium_mvadmbins_1*(njets!=1)"]
		self.fakefactordict["ff_tt_qcd_met_closure_syst_njets2"] = ["ffWeight_medium_mvadmbins_qcd_met_", "ffWeight_medium_mvadmbins_qcd_met_*(njets>=2)+ffWeight_medium_mvadmbins_1*(njets<2)"]

		self.fakefactordict["ff_tt_qcd_stat_unc1_njets0_mvadm0_sig_gt"] = ["ffWeight_medium_mvadmbins_qcd_stat_unc1_njet0_mvadm0_sig_gt3_", "ffWeight_medium_mvadmbins_qcd_stat_unc1_njet0_mvadm0_sig_gt3_"]
		self.fakefactordict["ff_tt_qcd_stat_unc1_njets0_mvadm1"] 		= ["ffWeight_medium_mvadmbins_qcd_stat_unc1_njet0_mvadm1_", "ffWeight_medium_mvadmbins_qcd_stat_unc1_njet0_mvadm1_"]
		self.fakefactordict["ff_tt_qcd_stat_unc1_njets0_mvadm10"] 		= ["ffWeight_medium_mvadmbins_qcd_stat_unc1_njet0_mvadm10_", "ffWeight_medium_mvadmbins_qcd_stat_unc1_njet0_mvadm10_"]
		self.fakefactordict["ff_tt_qcd_stat_unc1_njets0_mvadm2"] 		= ["ffWeight_medium_mvadmbins_qcd_stat_unc1_njet0_mvadm2_", "ffWeight_medium_mvadmbins_qcd_stat_unc1_njet0_mvadm2_"]
		self.fakefactordict["ff_tt_qcd_stat_unc1_njets1_mvadm0_sig_gt"] = ["ffWeight_medium_mvadmbins_qcd_stat_unc1_njet1_mvadm0_sig_gt3_", "ffWeight_medium_mvadmbins_qcd_stat_unc1_njet1_mvadm0_sig_gt3_"]
		self.fakefactordict["ff_tt_qcd_stat_unc1_njets1_mvadm1"] 		= ["ffWeight_medium_mvadmbins_qcd_stat_unc1_njet1_mvadm1_", "ffWeight_medium_mvadmbins_qcd_stat_unc1_njet1_mvadm1_"]
		self.fakefactordict["ff_tt_qcd_stat_unc1_njets1_mvadm10"] 		= ["ffWeight_medium_mvadmbins_qcd_stat_unc1_njet1_mvadm10_", "ffWeight_medium_mvadmbins_qcd_stat_unc1_njet1_mvadm10_"]
		self.fakefactordict["ff_tt_qcd_stat_unc1_njets1_mvadm2"] 		= ["ffWeight_medium_mvadmbins_qcd_stat_unc1_njet1_mvadm2_", "ffWeight_medium_mvadmbins_qcd_stat_unc1_njet1_mvadm2_"]
		self.fakefactordict["ff_tt_qcd_stat_unc1_njets2_mvadm0_sig_gt"] = ["ffWeight_medium_mvadmbins_qcd_stat_unc1_njet2_mvadm0_sig_gt3_", "ffWeight_medium_mvadmbins_qcd_stat_unc1_njet2_mvadm0_sig_gt3_"]
		self.fakefactordict["ff_tt_qcd_stat_unc1_njets2_mvadm1"] 		= ["ffWeight_medium_mvadmbins_qcd_stat_unc1_njet2_mvadm1_", "ffWeight_medium_mvadmbins_qcd_stat_unc1_njet2_mvadm1_"]
		self.fakefactordict["ff_tt_qcd_stat_unc1_njets2_mvadm10"]		= ["ffWeight_medium_mvadmbins_qcd_stat_unc1_njet2_mvadm10_", "ffWeight_medium_mvadmbins_qcd_stat_unc1_njet2_mvadm10_"]
		self.fakefactordict["ff_tt_qcd_stat_unc1_njets2_mvadm2"] 		= ["ffWeight_medium_mvadmbins_qcd_stat_unc1_njet2_mvadm2_", "ffWeight_medium_mvadmbins_qcd_stat_unc1_njet2_mvadm2_"]
		self.fakefactordict["ff_tt_qcd_stat_unc2_njets0_mvadm0_sig_gt"] = ["ffWeight_medium_mvadmbins_qcd_stat_unc2_njet0_mvadm0_sig_gt3_", "ffWeight_medium_mvadmbins_qcd_stat_unc2_njet0_mvadm0_sig_gt3_"]
		self.fakefactordict["ff_tt_qcd_stat_unc2_njets0_mvadm1"] 		= ["ffWeight_medium_mvadmbins_qcd_stat_unc2_njet0_mvadm1_", "ffWeight_medium_mvadmbins_qcd_stat_unc2_njet0_mvadm1_"]
		self.fakefactordict["ff_tt_qcd_stat_unc2_njets0_mvadm10"] 		= ["ffWeight_medium_mvadmbins_qcd_stat_unc2_njet0_mvadm10_", "ffWeight_medium_mvadmbins_qcd_stat_unc2_njet0_mvadm10_"]
		self.fakefactordict["ff_tt_qcd_stat_unc2_njets0_mvadm2"]		= ["ffWeight_medium_mvadmbins_qcd_stat_unc2_njet0_mvadm2_", "ffWeight_medium_mvadmbins_qcd_stat_unc2_njet0_mvadm2_"]
		self.fakefactordict["ff_tt_qcd_stat_unc2_njets1_mvadm0_sig_gt"] = ["ffWeight_medium_mvadmbins_qcd_stat_unc2_njet1_mvadm0_sig_gt3_", "ffWeight_medium_mvadmbins_qcd_stat_unc2_njet1_mvadm0_sig_gt3_"]
		self.fakefactordict["ff_tt_qcd_stat_unc2_njets1_mvadm1"]		= ["ffWeight_medium_mvadmbins_qcd_stat_unc2_njet1_mvadm1_", "ffWeight_medium_mvadmbins_qcd_stat_unc2_njet1_mvadm1_"]
		self.fakefactordict["ff_tt_qcd_stat_unc2_njets1_mvadm10"] 		= ["ffWeight_medium_mvadmbins_qcd_stat_unc2_njet1_mvadm10_", "ffWeight_medium_mvadmbins_qcd_stat_unc2_njet1_mvadm10_"]
		self.fakefactordict["ff_tt_qcd_stat_unc2_njets1_mvadm2"] 		= ["ffWeight_medium_mvadmbins_qcd_stat_unc2_njet1_mvadm2_", "ffWeight_medium_mvadmbins_qcd_stat_unc2_njet1_mvadm2_"]
		self.fakefactordict["ff_tt_qcd_stat_unc2_njets2_mvadm0_sig_gt"] = ["ffWeight_medium_mvadmbins_qcd_stat_unc2_njet2_mvadm0_sig_gt3_", "ffWeight_medium_mvadmbins_qcd_stat_unc2_njet2_mvadm0_sig_gt3_"]
		self.fakefactordict["ff_tt_qcd_stat_unc2_njets2_mvadm1"] 		= ["ffWeight_medium_mvadmbins_qcd_stat_unc2_njet2_mvadm1_", "ffWeight_medium_mvadmbins_qcd_stat_unc2_njet2_mvadm1_"]
		self.fakefactordict["ff_tt_qcd_stat_unc2_njets2_mvadm10"] 		= ["ffWeight_medium_mvadmbins_qcd_stat_unc2_njet2_mvadm10_", "ffWeight_medium_mvadmbins_qcd_stat_unc2_njet2_mvadm10_"]
		self.fakefactordict["ff_tt_qcd_stat_unc2_njets2_mvadm2"] 		= ["ffWeight_medium_mvadmbins_qcd_stat_unc2_njet2_mvadm2_", "ffWeight_medium_mvadmbins_qcd_stat_unc2_njet2_mvadm2_"]

		self.fakefactordict["ff_w_syst"] = "fakefactorWeight_w_syst_"
		
	def get_config(self, shift=0.0):
		plot_config = super(FakeFactorUncSystematic, self).get_config(shift=shift)
		
		for index, weight in enumerate(plot_config.get("weights", [])):

			# if "ff_sub_syst" in self.fakeFactorUncertainty:
			# if re.search("ff_("+plot_config["channel"]+"|)_sub_syst",self.fakeFactorUncertainty):
			if re.search("ff.*sub_syst",self.fakeFactorUncertainty):
				if shift > 0.0:
					plot_config["add_scale_factors"] = ["1 -1.1"]
				elif shift < 0.0:
					plot_config["add_scale_factors"] = ["1 -0.9"]
			else:
				if (shift != 0.0) and (not "data" in plot_config["nicks"][index]) and (not "gen_ztt" in plot_config["nicks"][index]):
					if shift > 0.0 or shift < 0.0:
						shift_string = "up" if shift > 0.0 else "down"
						# plot_config["weights"][index] = weight.replace("fakefactorWeight_comb_inclusive_2", self.fakefactordict[self.fakeFactorUncertainty] + shift_string + "_inclusive_2")
						plot_config["weights"][index] = weight.replace("ffWeight_medium_mvadmbins_1", self.fakefactordict[self.fakeFactorUncertainty][1]).replace(self.fakefactordict[self.fakeFactorUncertainty][0], self.fakefactordict[self.fakeFactorUncertainty][0] + shift_string)
		return plot_config

class JecUncSystematic(SystematicShiftBase):
	
	def __init__(self, plot_config, jecUncertainty):
		super(JecUncSystematic, self).__init__(plot_config)
		self.plot_config = plot_config
		self.jecUncertainty = jecUncertainty
	
	def get_config(self, shift=0.0):
		plot_config = super(JecUncSystematic, self).get_config(shift=shift)
		
		for index, folder in enumerate(plot_config.get("folders", [])):
			if (shift != 0.0) and (not "Run201" in plot_config["files"][index]) and (not "gen_ztt" in plot_config["nicks"][index]):
				if shift > 0.0:
					plot_config["folders"][index] = folder.replace("nominal", "jecUncUp")
				else:
					plot_config["folders"][index] = folder.replace("nominal", "jecUncDown")
		
		return plot_config


class CMS_scale_j_eta0to5_corr_13TeV(SystematicShiftBase):
	
	def __init__(self, plot_config):
		super(CMS_scale_j_eta0to5_corr_13TeV, self).__init__(plot_config)
		self.plot_config = plot_config
		#self.jecUncertainty = jecUncertainty	
	
	def get_config(self, shift=0.0):
		plot_config = super(CMS_scale_j_eta0to5_corr_13TeV, self).get_config(shift=shift)
		
		for index, folder in enumerate(plot_config.get("folders", [])):
			if (shift != 0.0) and (not "Run201" in plot_config["files"][index]) and (not "gen_ztt" in plot_config["nicks"][index]):
				if shift > 0.0:
					plot_config["folders"][index] = folder.replace("nominal", "eta0to5CorrelatedUp")
				else:
					plot_config["folders"][index] = folder.replace("nominal", "eta0to5CorrelatedDown")
		
		return plot_config

class CMS_scale_j_eta0to3_corr_13TeV(SystematicShiftBase):
	
	def __init__(self, plot_config):
		super(CMS_scale_j_eta0to3_corr_13TeV, self).__init__(plot_config)
		self.plot_config = plot_config
		#self.jecUncertainty = jecUncertainty	
	
	def get_config(self, shift=0.0):
		plot_config = super(CMS_scale_j_eta0to3_corr_13TeV, self).get_config(shift=shift)
		
		for index, folder in enumerate(plot_config.get("folders", [])):
			if (shift != 0.0) and (not "Run201" in plot_config["files"][index]) and (not "gen_ztt" in plot_config["nicks"][index]):
				if shift > 0.0:
					plot_config["folders"][index] = folder.replace("nominal", "eta0to3CorrelatedUp")
				else:
					plot_config["folders"][index] = folder.replace("nominal", "eta0to3CorrelatedDown")
		
		return plot_config


class CMS_scale_j_eta3to5_corr_13TeV(SystematicShiftBase):
	
	def __init__(self, plot_config):
		super(CMS_scale_j_eta3to5_corr_13TeV, self).__init__(plot_config)
		self.plot_config = plot_config
		#self.jecUncertainty = jecUncertainty	
	
	def get_config(self, shift=0.0):
		plot_config = super(CMS_scale_j_eta3to5_corr_13TeV, self).get_config(shift=shift)
		
		for index, folder in enumerate(plot_config.get("folders", [])):
			if (shift != 0.0) and (not "Run201" in plot_config["files"][index]) and (not "gen_ztt" in plot_config["nicks"][index]):
				if shift > 0.0:
					plot_config["folders"][index] = folder.replace("nominal", "eta3to5CorrelatedUp")
				else:
					plot_config["folders"][index] = folder.replace("nominal", "eta3to5CorrelatedDown")
		
		return plot_config



class CMS_scale_j_eta0to5_uncorr_13TeV(SystematicShiftBase):
	
	def __init__(self, plot_config):
		super(CMS_scale_j_eta0to5_uncorr_13TeV, self).__init__(plot_config)
		self.plot_config = plot_config
		#self.jecUncertainty = jecUncertainty	
	
	def get_config(self, shift=0.0):
		plot_config = super(CMS_scale_j_eta0to5_uncorr_13TeV, self).get_config(shift=shift)
		
		for index, folder in enumerate(plot_config.get("folders", [])):
			if (shift != 0.0) and (not "Run201" in plot_config["files"][index]) and (not "gen_ztt" in plot_config["nicks"][index]):
				if shift > 0.0:
					plot_config["folders"][index] = folder.replace("nominal", "eta0to5UncorrelatedUp")
				else:
					plot_config["folders"][index] = folder.replace("nominal", "eta0to5UncorrelatedDown")
		
		return plot_config

class CMS_scale_j_eta0to3_uncorr_13TeV(SystematicShiftBase):
	
	def __init__(self, plot_config):
		super(CMS_scale_j_eta0to3_uncorr_13TeV, self).__init__(plot_config)
		self.plot_config = plot_config
		#self.jecUncertainty = jecUncertainty	
	
	def get_config(self, shift=0.0):
		plot_config = super(CMS_scale_j_eta0to3_uncorr_13TeV, self).get_config(shift=shift)
		
		for index, folder in enumerate(plot_config.get("folders", [])):
			if (shift != 0.0) and (not "Run201" in plot_config["files"][index]) and (not "gen_ztt" in plot_config["nicks"][index]):
				if shift > 0.0:
					plot_config["folders"][index] = folder.replace("nominal", "eta0to3UncorrelatedUp")
				else:
					plot_config["folders"][index] = folder.replace("nominal", "eta0to3UncorrelatedDown")
		
		return plot_config


class CMS_scale_j_eta3to5_uncorr_13TeV(SystematicShiftBase):
	
	def __init__(self, plot_config):
		super(CMS_scale_j_eta3to5_uncorr_13TeV, self).__init__(plot_config)
		self.plot_config = plot_config
		#self.jecUncertainty = jecUncertainty	
	
	def get_config(self, shift=0.0):
		plot_config = super(CMS_scale_j_eta3to5_uncorr_13TeV, self).get_config(shift=shift)
		
		for index, folder in enumerate(plot_config.get("folders", [])):
			if (shift != 0.0) and (not "Run201" in plot_config["files"][index]) and (not "gen_ztt" in plot_config["nicks"][index]):
				if shift > 0.0:
					plot_config["folders"][index] = folder.replace("nominal", "eta3to5UncorrelatedUp")
				else:
					plot_config["folders"][index] = folder.replace("nominal", "eta3to5UncorrelatedDown")
		
		return plot_config

class CMS_scale_j_RelativeBal_13TeV(SystematicShiftBase):
	
	def __init__(self, plot_config):
		super(CMS_scale_j_RelativeBal_13TeV, self).__init__(plot_config)
		self.plot_config = plot_config
		#self.jecUncertainty = jecUncertainty	
	
	def get_config(self, shift=0.0):
		plot_config = super(CMS_scale_j_RelativeBal_13TeV, self).get_config(shift=shift)
		
		for index, folder in enumerate(plot_config.get("folders", [])):
			if (shift != 0.0) and (not "Run201" in plot_config["files"][index]) and (not "gen_ztt" in plot_config["nicks"][index]):
				if shift > 0.0:
					plot_config["folders"][index] = folder.replace("nominal", "relativeBalUp")
				else:
					plot_config["folders"][index] = folder.replace("nominal", "relativeBalDown")
		
		return plot_config

class CMS_scale_j_RelativeSample_13TeV(SystematicShiftBase):
	
	def __init__(self, plot_config):
		super(CMS_scale_j_RelativeSample_13TeV, self).__init__(plot_config)
		self.plot_config = plot_config
		#self.jecUncertainty = jecUncertainty	
	
	def get_config(self, shift=0.0):
		plot_config = super(CMS_scale_j_RelativeSample_13TeV, self).get_config(shift=shift)
		
		for index, folder in enumerate(plot_config.get("folders", [])):
			if (shift != 0.0) and (not "Run201" in plot_config["files"][index]) and (not "gen_ztt" in plot_config["nicks"][index]):
				if shift > 0.0:
					plot_config["folders"][index] = folder.replace("nominal", "relativeSampleUp")
				else:
					plot_config["folders"][index] = folder.replace("nominal", "relativeSampleDown")
		
		return plot_config


class JecUncSplitSystematic(SystematicShiftBase):
	
	def __init__(self, plot_config, jecUncertainty):
		super(JecUncSplitSystematic, self).__init__(plot_config)
		self.plot_config = plot_config
		self.jecUncertainty = jecUncertainty
	
	def get_config(self, shift=0.0):
		plot_config = super(JecUncSplitSystematic, self).get_config(shift=shift)

		for key in ["x_expressions", "y_expressions", "z_expressions", "weights"]:
			for index, value in enumerate(plot_config.get(key, [])):
				if (shift != 0.0) and (not "Run201" in plot_config["files"][index]) and (not "gen_ztt" in plot_config["nicks"][index]):
					if shift > 0.0 or shift < 0.0:
						shift_string = "Up" if shift > 0.0 else "Down"
						plot_config[key][index] = value.replace("njetspt30", "njetspt30_"+self.jecUncertainty+shift_string).replace("mjj", "mjj_"+self.jecUncertainty+shift_string).replace("jdeta", "jdeta_"+self.jecUncertainty+shift_string).replace("jdphi", "jdphi_"+self.jecUncertainty+shift_string)
		
		return plot_config


class TTBarShapeSystematic(SystematicShiftBase):
	
	def get_config(self, shift=0.0):
		plot_config = super(TTBarShapeSystematic, self).get_config(shift=shift)
		
		for index, weight in enumerate(plot_config.get("weights", [])):
			if (shift != 0.0) and (not "Run201" in plot_config["files"][index]) and (not "gen_ztt" in plot_config["nicks"][index]):
				if shift > 0.0:
					plot_config["weights"][index] = weight.replace("topPtReweightWeight", "topPtReweightWeight*topPtReweightWeight")
				else:
					plot_config["weights"][index] = weight.replace("topPtReweightWeight", "(1.0)")
		
		return plot_config


class DYShapeSystematic(SystematicShiftBase):
	
	def get_config(self, shift=0.0):
		plot_config = super(DYShapeSystematic, self).get_config(shift=shift)
		
		for index, weight in enumerate(plot_config.get("weights", [])):
			if (shift != 0.0) and (not "Run201" in plot_config["files"][index]) and (not "gen_ztt" in plot_config["nicks"][index]):
				if shift > 0.0:
					plot_config["weights"][index] = weight.replace("zPtReweightWeight","zPtReweightWeight*zPtReweightWeight")
				else:
					plot_config["weights"][index] = weight.replace("zPtReweightWeight","(1.0)")
		
		return plot_config

class EmuQCDOsssShapeSystematic(SystematicShiftBase):
	
	def get_config(self, shift=0.0):
		plot_config = super(EmuQCDOsssShapeSystematic, self).get_config(shift=shift)
		
		for index, weight in enumerate(plot_config.get("weights", [])):
			if (shift != 0.0) and (not "Run201" in plot_config["files"][index]) and (not "gen_ztt" in plot_config["nicks"][index]):
				if shift > 0.0:
					plot_config["weights"][index] = weight.replace("emuQcdOsssWeight","emuQcdOsssShapeUpWeight")
				else:
					plot_config["weights"][index] = weight.replace("emuQcdOsssWeight","emuQcdOsssShapeDownWeight")
		
		return plot_config

class EmuQCDOsssRateSystematic(SystematicShiftBase):
	
	def get_config(self, shift=0.0):
		plot_config = super(EmuQCDOsssRateSystematic, self).get_config(shift=shift)
		
		for index, weight in enumerate(plot_config.get("weights", [])):
			if (shift != 0.0) and (not "Run201" in plot_config["files"][index]) and (not "gen_ztt" in plot_config["nicks"][index]):
				if shift > 0.0:
					plot_config["weights"][index] = weight.replace("emuQcdOsssWeight","emuQcdOsssRateUpWeight")
				else:
					plot_config["weights"][index] = weight.replace("emuQcdOsssWeight","emuQcdOsssRateDownWeight")
		
		return plot_config

class EmuQCDExtrapSystematic(SystematicShiftBase):

	def get_config(self, shift=0.0):
		plot_config = super(EmuQCDExtrapSystematic, self).get_config(shift=shift)

		for index, weight in enumerate(plot_config.get("weights", [])):
			if (shift != 0.0) and (not "Run201" in plot_config["files"][index]) and (not "gen_ztt" in plot_config["nicks"][index]):
				if shift > 0.0:
					plot_config["weights"][index] = weight.replace("emuQcdOsssWeight","emuQcdExtrapUpWeight")
				else:
					plot_config["weights"][index] = weight.replace("emuQcdOsssWeight","emuQcdExtrapDownWeight")
		
		return plot_config


class JetFakeTauQCDShapeSystematic(SystematicShiftBase):
	
	def get_config(self, shift=0.0):
		plot_config = super(JetFakeTauQCDShapeSystematic, self).get_config(shift=shift)
		
		for index, weight in enumerate(plot_config.get("weights", [])):
			if (shift != 0.0) and (not "Run201" in plot_config["files"][index]) and (not "gen_ztt" in plot_config["nicks"][index]):
				if shift > 0.0:
					plot_config["weights"][index] = weight.replace("jetToTauFakeWeight_comb", "jetToTauFakeWeight_qcd_up")
				else:
					plot_config["weights"][index] = weight.replace("jetToTauFakeWeight_comb", "jetToTauFakeWeight_qcd_down")
		
		return plot_config


class JetFakeTauWShapeSystematic(SystematicShiftBase):
	
	def get_config(self, shift=0.0):
		plot_config = super(JetFakeTauWShapeSystematic, self).get_config(shift=shift)
		
		for index, weight in enumerate(plot_config.get("weights", [])):
			if (shift != 0.0) and (not "Run201" in plot_config["files"][index]) and (not "gen_ztt" in plot_config["nicks"][index]):
				if shift > 0.0:
					plot_config["weights"][index] = weight.replace("jetToTauFakeWeight_comb", "jetToTauFakeWeight_w_up")
				else:
					plot_config["weights"][index] = weight.replace("jetToTauFakeWeight_comb", "jetToTauFakeWeight_w_down")
		
		return plot_config


class JetFakeTauTTcorrShapeSystematic(SystematicShiftBase):
	
	def get_config(self, shift=0.0):
		plot_config = super(JetFakeTauTTcorrShapeSystematic, self).get_config(shift=shift)
		
		for index, weight in enumerate(plot_config.get("weights", [])):
			if (shift != 0.0) and (not "Run201" in plot_config["files"][index]) and (not "gen_ztt" in plot_config["nicks"][index]):
				if shift > 0.0:
					plot_config["weights"][index] = weight.replace("jetToTauFakeWeight_comb", "jetToTauFakeWeight_tt_corr_up")
				else:
					plot_config["weights"][index] = weight.replace("jetToTauFakeWeight_comb", "jetToTauFakeWeight_tt_corr_down")
		
		return plot_config


class JetFakeTauTTstatShapeSystematic(SystematicShiftBase):
	
	def get_config(self, shift=0.0):
		plot_config = super(JetFakeTauTTstatShapeSystematic, self).get_config(shift=shift)
		
		for index, weight in enumerate(plot_config.get("weights", [])):
			if (shift != 0.0) and (not "Run201" in plot_config["files"][index]) and (not "gen_ztt" in plot_config["nicks"][index]):
				if shift > 0.0:
					plot_config["weights"][index] = weight.replace("jetToTauFakeWeight_comb", "jetToTauFakeWeight_tt_stat_up")
				else:
					plot_config["weights"][index] = weight.replace("jetToTauFakeWeight_comb", "jetToTauFakeWeight_tt_stat_down")
		
		return plot_config


class JetFakeTauFracQCDShapeSystematic(SystematicShiftBase):
	
	def get_config(self, shift=0.0):
		plot_config = super(JetFakeTauFracQCDShapeSystematic, self).get_config(shift=shift)
		
		for index, weight in enumerate(plot_config.get("weights", [])):
			if (shift != 0.0) and (not "Run201" in plot_config["files"][index]) and (not "gen_ztt" in plot_config["nicks"][index]):
				if shift > 0.0:
					plot_config["weights"][index] = weight.replace("jetToTauFakeWeight_comb", "jetToTauFakeWeight_frac_qcd_up")
				else:
					plot_config["weights"][index] = weight.replace("jetToTauFakeWeight_comb", "jetToTauFakeWeight_frac_qcd_down")
		
		return plot_config


class JetFakeTauFracWShapeSystematic(SystematicShiftBase):
	
	def get_config(self, shift=0.0):
		plot_config = super(JetFakeTauFracWShapeSystematic, self).get_config(shift=shift)
		
		for index, weight in enumerate(plot_config.get("weights", [])):
			if (shift != 0.0) and (not "Run201" in plot_config["files"][index]) and (not "gen_ztt" in plot_config["nicks"][index]):
				if shift > 0.0:
					plot_config["weights"][index] = weight.replace("jetToTauFakeWeight_comb", "jetToTauFakeWeight_frac_w_up")
				else:
					plot_config["weights"][index] = weight.replace("jetToTauFakeWeight_comb", "jetToTauFakeWeight_frac_w_down")
		
		return plot_config


class JetFakeTauFracTTShapeSystematic(SystematicShiftBase):
	
	def get_config(self, shift=0.0):
		plot_config = super(JetFakeTauFracTTShapeSystematic, self).get_config(shift=shift)
		
		for index, weight in enumerate(plot_config.get("weights", [])):
			if (shift != 0.0) and (not "Run201" in plot_config["files"][index]) and (not "gen_ztt" in plot_config["nicks"][index]):
				if shift > 0.0:
					plot_config["weights"][index] = weight.replace("jetToTauFakeWeight_comb", "jetToTauFakeWeight_frac_tt_up")
				else:
					plot_config["weights"][index] = weight.replace("jetToTauFakeWeight_comb", "jetToTauFakeWeight_frac_tt_down")
		
		return plot_config


class JetFakeTauFracDYShapeSystematic(SystematicShiftBase):
	
	def get_config(self, shift=0.0):
		plot_config = super(JetFakeTauFracDYShapeSystematic, self).get_config(shift=shift)
		
		for index, weight in enumerate(plot_config.get("weights", [])):
			if (shift != 0.0) and (not "Run201" in plot_config["files"][index]) and (not "gen_ztt" in plot_config["nicks"][index]):
				if shift > 0.0:
					plot_config["weights"][index] = weight.replace("jetToTauFakeWeight_comb", "jetToTauFakeWeight_frac_dy_up")
				else:
					plot_config["weights"][index] = weight.replace("jetToTauFakeWeight_comb", "jetToTauFakeWeight_frac_dy_down")
		
		return plot_config


class MuFakeTauEsSystematic(SystematicShiftBase):
	
	def get_config(self, shift=0.0):
		plot_config = super(MuFakeTauEsSystematic, self).get_config(shift=shift)
		
		for index, folder in enumerate(plot_config.get("folders", [])):
			if (shift != 0.0) and (not "Run201" in plot_config["files"][index]) and (not "gen_ztt" in plot_config["nicks"][index]):
				if shift > 0.0:
					plot_config["folders"][index] = folder.replace("nominal", "muonEsUp")
				else:
					plot_config["folders"][index] = folder.replace("nominal", "muonEsDown")
		
		return plot_config


class EleFakeTauEsSystematic(SystematicShiftBase):
	
	def get_config(self, shift=0.0):
		plot_config = super(EleFakeTauEsSystematic, self).get_config(shift=shift)
		
		for index, folder in enumerate(plot_config.get("folders", [])):
			if (shift != 0.0) and (not "Run201" in plot_config["files"][index]) and (not "gen_ztt" in plot_config["nicks"][index]):
				if shift > 0.0:
					plot_config["folders"][index] = folder.replace("nominal", "eleEsUp")
				else:
					plot_config["folders"][index] = folder.replace("nominal", "eleEsDown")
		
		return plot_config


class TauEsSystematic(SystematicShiftBase):
	
	def get_config(self, shift=0.0):
		plot_config = super(TauEsSystematic, self).get_config(shift=shift)
		
		for index, folder in enumerate(plot_config.get("folders", [])):
			if (shift != 0.0) and (not "Run201" in plot_config["files"][index]) and (not "gen_ztt" in plot_config["nicks"][index]):
				if shift > 0.0:
					plot_config["folders"][index] = folder.replace("nominal", "tauEsUp")
				else:
					plot_config["folders"][index] = folder.replace("nominal", "tauEsDown")
		
		return plot_config


class EleEsSystematic(SystematicShiftBase):
	
	def get_config(self, shift=0.0):
		plot_config = super(EleEsSystematic, self).get_config(shift=shift)
		
		for index, folder in enumerate(plot_config.get("folders", [])):
			if (shift != 0.0) and (not "Run201" in plot_config["files"][index]) and (not "gen_ztt" in plot_config["nicks"][index]):
				if shift > 0.0:
					plot_config["folders"][index] = folder.replace("nominal", "eleEsUp")
				else:
					plot_config["folders"][index] = folder.replace("nominal", "eleEsDown")
		
		return plot_config


class MuonEsSystematic(SystematicShiftBase):
	
	def get_config(self, shift=0.0):
		plot_config = super(MuonEsSystematic, self).get_config(shift=shift)
		
		for index, folder in enumerate(plot_config.get("folders", [])):
			if (shift != 0.0) and (not "Run201" in plot_config["files"][index]) and (not "gen_ztt" in plot_config["nicks"][index]):
				if shift > 0.0:
					plot_config["folders"][index] = folder.replace("nominal", "muonEsUp")
				else:
					plot_config["folders"][index] = folder.replace("nominal", "muonEsDown")
		
		return plot_config


class MetResponseSystematic(SystematicShiftBase):
	
	def get_config(self, shift=0.0):
		plot_config = super(MetResponseSystematic, self).get_config(shift=shift)
		
		for index, folder in enumerate(plot_config.get("folders", [])):
			if (shift != 0.0) and (not "Run201" in plot_config["files"][index]) and (not "gen_ztt" in plot_config["nicks"][index]):
				if shift > 0.0:
					plot_config["folders"][index] = folder.replace("nominal", "metResponseUp")
				else:
					plot_config["folders"][index] = folder.replace("nominal", "metResponseDown")
		
		return plot_config


class TagEleEsSystematic(SystematicShiftBase):
	
	def get_config(self, shift=0.0):
		plot_config = super(TagEleEsSystematic, self).get_config(shift=shift)
		
		for index, folder in enumerate(plot_config.get("folders", [])):
			if (shift != 0.0) and (not "Run201" in plot_config["files"][index]) and (not "gen_ztt" in plot_config["nicks"][index]):
				if shift > 0.0:
					plot_config["folders"][index] = folder.replace("tagEleEsNom", "tagEleEsUp")
				else:
					plot_config["folders"][index] = folder.replace("tagEleEsNom", "tagEleEsDown")
		
		return plot_config


class ProbeTauEsSystematic(SystematicShiftBase):
	
	def get_config(self, shift=0.0):
		plot_config = super(ProbeTauEsSystematic, self).get_config(shift=shift)
		
		for index, folder in enumerate(plot_config.get("folders", [])):
			if (shift != 0.0) and (not "Run201" in plot_config["files"][index]) and (not "gen_ztt" in plot_config["nicks"][index]):
				if shift > 0.0:
					plot_config["folders"][index] = folder.replace("probeTauEsNom", "probeTauEsUp")
				else:
					plot_config["folders"][index] = folder.replace("probeTauEsNom", "probeTauEsDown")
		
		return plot_config


class ProbeEleEsSystematic(SystematicShiftBase):
	
	def get_config(self, shift=0.0):
		plot_config = super(ProbeEleEsSystematic, self).get_config(shift=shift)
		
		for index, folder in enumerate(plot_config.get("folders", [])):
			if (shift != 0.0) and (not "Run201" in plot_config["files"][index]) and (not "gen_ztt" in plot_config["nicks"][index]):
				if shift > 0.0:
					plot_config["folders"][index] = folder.replace("probeEleEsNom", "probeEleEsUp")
				else:
					plot_config["folders"][index] = folder.replace("probeEleEsNom", "probeEleEsDown")
		
		return plot_config


class MassResSystematic(SystematicShiftBase):
	
	def get_config(self, shift=0.0):
		plot_config = super(MassResSystematic, self).get_config(shift=shift)
		
		for index, expression in enumerate(plot_config.get("x_expressions", [])):
			if (shift != 0.0) and (not "Run201" in plot_config["files"][index]) and (not "gen_ztt" in plot_config["nicks"][index]):
				if shift > 0.0:
					plot_config["x_expressions"][index] = expression.replace("m_vis", "diLepMassSmearUp")
				else:
					plot_config["x_expressions"][index] = expression.replace("m_vis", "diLepMassSmearDown")
		
		return plot_config

class MassResSystematicv2(SystematicShiftBase):

	def get_config(self, shift=0.0):
		plot_config = super(MassResSystematicv2, self).get_config(shift=shift)

		for index, expression in enumerate(plot_config.get("x_expressions", [])):
			if not "Run201" in plot_config["files"][index]:
				if shift > 0.0:
					plot_config["x_expressions"][index] = expression.replace("m_vis", "diLepMassSmearUp_wPeakFit")
				elif shift < 0.0:
					plot_config["x_expressions"][index] = expression.replace("m_vis", "diLepMassSmearDown_wPeakFit")

		return plot_config


class BTagSystematic(SystematicShiftBase):
	
	def get_config(self, shift=0.0):
		plot_config = super(BTagSystematic, self).get_config(shift=shift)
		
		for index, folder in enumerate(plot_config.get("folders", [])):
			if (shift != 0.0) and (not "Run201" in plot_config["files"][index]) and (not "gen_ztt" in plot_config["nicks"][index]):
				if shift > 0.0:
					plot_config["folders"][index] = folder.replace("nominal", "bTagUp")
				else:
					plot_config["folders"][index] = folder.replace("nominal", "bTagDown")
		
		return plot_config


class BMistagSystematic(SystematicShiftBase):
	
	def get_config(self, shift=0.0):
		plot_config = super(BMistagSystematic, self).get_config(shift=shift)
		
		for index, folder in enumerate(plot_config.get("folders", [])):
			if (shift != 0.0) and (not "Run201" in plot_config["files"][index]) and (not "gen_ztt" in plot_config["nicks"][index]):
				if shift > 0.0:
					plot_config["folders"][index] = folder.replace("nominal", "bMistagUp")
				else:
					plot_config["folders"][index] = folder.replace("nominal", "bMistagDown")
		
		return plot_config


class ElectronToTauOneProngFakeSystematic(SystematicShiftBase):

	def get_config(self, shift=0.0):
		plot_config = super(ElectronToTauOneProngFakeSystematic, self).get_config(shift=shift)
		
		for index, weight in enumerate(plot_config.get("weights", [])):
			if (shift != 0.0) and (not "Run201" in plot_config["files"][index]) and (not "gen_ztt" in plot_config["nicks"][index]):
				if shift > 0.0:
					plot_config["weights"][index] = weight.replace("(((decayMode_2 == 0)*0.98) + ((decayMode_2 == 1 || decayMode_2 == 2)*1.2) + ((decayMode_2 == 10)*1.0))", "(((decayMode_2 == 0)*0.98*1.12) + ((decayMode_2 == 1 || decayMode_2 == 2)*1.2) + ((decayMode_2 == 10)*1.0))")
				else:
					plot_config["weights"][index] = weight.replace("(((decayMode_2 == 0)*0.98) + ((decayMode_2 == 1 || decayMode_2 == 2)*1.2) + ((decayMode_2 == 10)*1.0))", "(((decayMode_2 == 0)*0.98*0.88) + ((decayMode_2 == 1 || decayMode_2 == 2)*1.2) + ((decayMode_2 == 10)*1.0))")
		
		return plot_config


class ElectronToTauOneProngPiZerosFakeSystematic(SystematicShiftBase):
	
	def get_config(self, shift=0.0):
		plot_config = super(ElectronToTauOneProngPiZerosFakeSystematic, self).get_config(shift=shift)
		
		for index, weight in enumerate(plot_config.get("weights", [])):
			if (shift != 0.0) and (not "Run201" in plot_config["files"][index]) and (not "gen_ztt" in plot_config["nicks"][index]):
				if shift > 0.0:
					plot_config["weights"][index] = weight.replace("(((decayMode_2 == 0)*0.98) + ((decayMode_2 == 1 || decayMode_2 == 2)*1.2) + ((decayMode_2 == 10)*1.0))", "(((decayMode_2 == 0)*0.98) + ((decayMode_2 == 1 || decayMode_2 == 2)*1.2*1.12) + ((decayMode_2 == 10)*1.0))")
				else:
					plot_config["weights"][index] = weight.replace("(((decayMode_2 == 0)*0.98) + ((decayMode_2 == 1 || decayMode_2 == 2)*1.2) + ((decayMode_2 == 10)*1.0))", "(((decayMode_2 == 0)*0.98) + ((decayMode_2 == 1 || decayMode_2 == 2)*1.2*0.88) + ((decayMode_2 == 10)*1.0))")
		
		return plot_config

class ElectronToTauFakeSystematic(SystematicShiftBase):
        
        def get_config(self, shift=0.0):
                plot_config = super(ElectronToTauFakeSystematic, self).get_config(shift=shift)

                for index, weight in enumerate(plot_config.get("weights", [])):
                        if (shift != 0.0) and (not "Run201" in plot_config["files"][index]) and (not "gen_ztt" in plot_config["nicks"][index]):
                                if shift > 0.0:
                                        plot_config["weights"][index] = ("({weight})*(1/tauidWeight_deepTauVsEleVVLoose_2)*(tauidWeight_deepTauVsEleVVLoose_up_2)").format(
                                                weight=weight
                                        )
                                else:
                                        plot_config["weights"][index] = ("({weight})*(1/tauidWeight_deepTauVsEleVVLoose_2)*(tauidWeight_deepTauVsEleVVLoose_down_2)").format(
                                                weight=weight
                                        )
                return plot_config

class MuonToTauOneProngFakeSystematic(SystematicShiftBase):
	
	def get_config(self, shift=0.0):
		plot_config = super(MuonToTauOneProngFakeSystematic, self).get_config(shift=shift)
		
		for index, weight in enumerate(plot_config.get("weights", [])):
			if (shift != 0.0) and (not "Run201" in plot_config["files"][index]) and (not "gen_ztt" in plot_config["nicks"][index]):
				if shift > 0.0:
					plot_config["weights"][index] = weight.replace("(((decayMode_2 == 0)*0.75) + ((decayMode_2 == 1 || decayMode_2 == 2)*1.0) + ((decayMode_2 == 10)*1.0))", "(((decayMode_2 == 0)*0.75*1.25) + ((decayMode_2 == 1 || decayMode_2 == 2)*1.0) + ((decayMode_2 == 10)*1.0))")
				else:
					plot_config["weights"][index] = weight.replace("(((decayMode_2 == 0)*0.75) + ((decayMode_2 == 1 || decayMode_2 == 2)*1.0) + ((decayMode_2 == 10)*1.0))", "(((decayMode_2 == 0)*0.75*0.75) + ((decayMode_2 == 1 || decayMode_2 == 2)*1.0) + ((decayMode_2 == 10)*1.0))")
		
		return plot_config


class MuonToTauOneProngPiZerosFakeSystematic(SystematicShiftBase):
	
	def get_config(self, shift=0.0):
		plot_config = super(MuonToTauOneProngPiZerosFakeSystematic, self).get_config(shift=shift)
		
		for index, weight in enumerate(plot_config.get("weights", [])):
			if (shift != 0.0) and (not "Run201" in plot_config["files"][index]) and (not "gen_ztt" in plot_config["nicks"][index]):
				if shift > 0.0:
					plot_config["weights"][index] = weight.replace("(((decayMode_2 == 0)*0.75) + ((decayMode_2 == 1 || decayMode_2 == 2)*1.0) + ((decayMode_2 == 10)*1.0))", "(((decayMode_2 == 0)*0.75) + ((decayMode_2 == 1 || decayMode_2 == 2)*1.25) + ((decayMode_2 == 10)*1.0))")
				else:
					plot_config["weights"][index] = weight.replace("(((decayMode_2 == 0)*0.75) + ((decayMode_2 == 1 || decayMode_2 == 2)*1.0) + ((decayMode_2 == 10)*1.0))", "(((decayMode_2 == 0)*0.75) + ((decayMode_2 == 1 || decayMode_2 == 2)*0.75) + ((decayMode_2 == 10)*1.0))")
		
		return plot_config

class MuonToTauFakeSystematic(SystematicShiftBase):

        def get_config(self, shift=0.0):
                plot_config = super(MuonToTauFakeSystematic, self).get_config(shift=shift)

                for index, weight in enumerate(plot_config.get("weights", [])):
                        if (shift != 0.0) and (not "Run201" in plot_config["files"][index]) and (not "gen_ztt" in plot_config["nicks"][index]):
                                if shift > 0.0:
                                        plot_config["weights"][index] = ("({weight})*(1/tauidWeight_deepTauVsMuTight_2)*(tauidWeight_deepTauVsMuTight_up_2)").format(
                                                weight=weight
                                        )
                                else:
                                        plot_config["weights"][index] = ("({weight})*(1/tauidWeight_deepTauVsMuTight_2)*(tauidWeight_deepTauVsMuTight_down_2)").format(
                                                weight=weight
                                        )
                return plot_config

class JetToTauFakeSystematic(SystematicShiftBase):
	
	def get_config(self, shift=0.0):
		plot_config = super(JetToTauFakeSystematic, self).get_config(shift=shift)
		
		for index, folder in enumerate(plot_config.get("folders", [])):
			if (shift != 0.0) and (not "Run201" in plot_config["files"][index]) and (not "gen_ztt" in plot_config["nicks"][index]):
				if shift > 0.0:
					plot_config["folders"][index] = folder.replace("nominal", "tauJetFakeEsUp")
				else:
					plot_config["folders"][index] = folder.replace("nominal", "tauJetFakeEsDown")
		
		return plot_config


class MetJetEnSystematic(SystematicShiftBase):
	
	def get_config(self, shift=0.0):
		plot_config = super(MetJetEnSystematic, self).get_config(shift=shift)
		
		for index, folder in enumerate(plot_config.get("folders", [])):
			if (shift != 0.0) and (not "Run201" in plot_config["files"][index]) and (not "gen_ztt" in plot_config["nicks"][index]):
				if shift > 0.0:
					plot_config["folders"][index] = folder.replace("nominal", "metJetEnUp")
				else:
					plot_config["folders"][index] = folder.replace("nominal", "metJetEnDown")
		
		return plot_config


class MetUnclusteredEnSystematic(SystematicShiftBase):
	
	def get_config(self, shift=0.0):
		plot_config = super(MetUnclusteredEnSystematic, self).get_config(shift=shift)
		
		for index, folder in enumerate(plot_config.get("folders", [])):
			if (shift != 0.0) and (not "Run201" in plot_config["files"][index]) and (not "gen_ztt" in plot_config["nicks"][index]):
				if shift > 0.0:
					plot_config["folders"][index] = folder.replace("nominal", "metUnclusteredEnUp")
				else:
					plot_config["folders"][index] = folder.replace("nominal", "metUnclusteredEnDown")
		
		return plot_config

class TauIDvsJetsSystematic(SystematicShiftBase):

      def get_config(self, shift=0.0):
               plot_config = super(TauIDvsJetsSystematic, self).get_config(shift=shift)

               for index, weight in enumerate(plot_config.get("weights", [])):
                       if (shift != 0.0) and (not "Run201" in plot_config["files"][index]) and (not "gen_ztt" in plot_config["nicks"][index]):
                               if shift > 0.0:
                                       plot_config["weights"][index] = ("({weight})*(1/tauidWeight_deepTauVsJetMedium_2)*(tauidWeight_deepTauVsJetMedium_up_2)").format(
                                                       weight=weight
                                       )
                               else:
                                       plot_config["weights"][index] = ("({weight})*(1/tauidWeight_deepTauVsJetMedium_2)*(tauidWeight_deepTauVsJetMedium_down_2)").format(
                                                       weight=weight
                                       )
               return plot_config

class TauTriggerSystematic(SystematicShiftBase):

      def get_config(self, shift=0.0):
               plot_config = super(TauTriggerSystematic, self).get_config(shift=shift)

               for index, weight in enumerate(plot_config.get("weights", [])):
                       if (shift != 0.0) and (not "Run201" in plot_config["files"][index]) and (not "gen_ztt" in plot_config["nicks"][index]):
                               if shift > 0.0:
                                       plot_config["weights"][index] = ("({weight})*(1/triggerWeight_comb)*(triggerWeight_comb_up)").format(
                                                       weight=weight
                                       )
                               else:
                                       plot_config["weights"][index] = ("({weight})*(1/triggerWeight_comb)*(triggerWeight_comb_down)").format(
                                                       weight=weight
                                       )
               return plot_config

class TauDMRecoOneProngSystematic(SystematicShiftBase):
	
	def get_config(self, shift=0.0):
		plot_config = super(TauDMRecoOneProngSystematic, self).get_config(shift=shift)
		
		for index, weight in enumerate(plot_config.get("weights", [])):
			if (shift != 0.0) and (not "Run201" in plot_config["files"][index]) and (not "gen_ztt" in plot_config["nicks"][index]):
				if shift > 0.0:
					plot_config["weights"][index] = ("({weight})*(((decayMode_2 == 0)*1.03) + ((decayMode_2 == 1 || decayMode_2 == 2)*1.0) + ((decayMode_2 == 10)*1.0))").format(
							weight=weight
					)
				else:
					plot_config["weights"][index] = ("({weight})*(((decayMode_2 == 0)*0.97) + ((decayMode_2 == 1 || decayMode_2 == 2)*1.0) + ((decayMode_2 == 10)*1.0))").format(
							weight=weight
					)
		
		return plot_config


class TauDMRecoOneProngPiZerosSystematic(SystematicShiftBase):
	
	def get_config(self, shift=0.0):
		plot_config = super(TauDMRecoOneProngPiZerosSystematic, self).get_config(shift=shift)
		
		for index, weight in enumerate(plot_config.get("weights", [])):
			if (shift != 0.0) and (not "Run201" in plot_config["files"][index]) and (not "gen_ztt" in plot_config["nicks"][index]):
				if shift > 0.0:
					plot_config["weights"][index] = ("({weight})*(((decayMode_2 == 0)*1.0) + ((decayMode_2 == 1 || decayMode_2 == 2)*1.03) + ((decayMode_2 == 10)*1.0))").format(
							weight=weight
					)
				else:
					plot_config["weights"][index] = ("({weight})*(((decayMode_2 == 0)*1.0) + ((decayMode_2 == 1 || decayMode_2 == 2)*0.97) + ((decayMode_2 == 10)*1.0))").format(
							weight=weight
					)
		
		return plot_config


class TauDMRecoThreeProngSystematic(SystematicShiftBase):
	
	def get_config(self, shift=0.0):
		plot_config = super(TauDMRecoThreeProngSystematic, self).get_config(shift=shift)
		
		for index, weight in enumerate(plot_config.get("weights", [])):
			if (shift != 0.0) and (not "Run201" in plot_config["files"][index]) and (not "gen_ztt" in plot_config["nicks"][index]):
				if shift > 0.0:
					plot_config["weights"][index] = ("({weight})*(((decayMode_2 == 0)*1.0) + ((decayMode_2 == 1 || decayMode_2 == 2)*1.0) + ((decayMode_2 == 10)*1.03))").format(
							weight=weight
					)
				else:
					plot_config["weights"][index] = ("({weight})*(((decayMode_2 == 0)*1.0) + ((decayMode_2 == 1 || decayMode_2 == 2)*1.0) + ((decayMode_2 == 10)*0.97))").format(
							weight=weight
					)
		
		return plot_config


class RecoTauDecayModeFakePiSystematic(SystematicShiftBase):
	
	def get_config(self, shift=0.0):
		plot_config = super(RecoTauDecayModeFakePiSystematic, self).get_config(shift=shift)
		
		for index, weight in enumerate(plot_config.get("weights", [])):
			if (shift != 0.0) and (not "Run201" in plot_config["files"][index]) and (not "gen_ztt" in plot_config["nicks"][index]):
				plot_config["weights"][index] = ("({weight})*({syst})").format(
						weight=weight,
						syst=(
								"((1.0)+"+
								 "((decayMode_1==0)*(genMatchedTau1DecayMode==0)*(1.13-1.0))+"+
								 "((decayMode_1==0)*(genMatchedTau1DecayMode==1)*(0.69-1.0)))*"+
								"((1.0)+"+
								 "((decayMode_2==0)*(genMatchedTau2DecayMode==0)*(1.13-1.0))+"+
								 "((decayMode_2==0)*(genMatchedTau2DecayMode==1)*(0.69-1.0)))"
						) if shift > 0.0 else (
								"((1.0)+"+
								 "((decayMode_1==0)*(genMatchedTau1DecayMode==0)*(0.88-1.0))+"+
								 "((decayMode_1==0)*(genMatchedTau1DecayMode==1)*(1.30-1.0)))*"+
								"((1.0)+"+
								 "((decayMode_2==0)*(genMatchedTau2DecayMode==0)*(0.88-1.0))+"+
								 "((decayMode_2==0)*(genMatchedTau2DecayMode==1)*(1.30-1.0)))"
						)
				)
		
		return plot_config


class RecoTauDecayModeFakeRhoSystematic(SystematicShiftBase):
	
	def get_config(self, shift=0.0):
		plot_config = super(RecoTauDecayModeFakeRhoSystematic, self).get_config(shift=shift)
		
		for index, weight in enumerate(plot_config.get("weights", [])):
			if (shift != 0.0) and (not "Run201" in plot_config["files"][index]) and (not "gen_ztt" in plot_config["nicks"][index]):
				plot_config["weights"][index] = ("({weight})*({syst})").format(
						weight=weight,
						syst=(
								"((1.0)+"+
								 "((decayMode_1==1)*(genMatchedTau1DecayMode==1)*(1.02-1.0))+"+
								 "((decayMode_1==1)*(genMatchedTau1DecayMode>1)*(genMatchedTau1DecayMode<5)*(0.96-1.0)))*"+
								"((1.0)+"+
								 "((decayMode_2==1)*(genMatchedTau2DecayMode==1)*(1.02-1.0))+"+
								 "((decayMode_2==1)*(genMatchedTau2DecayMode>1)*(genMatchedTau2DecayMode<5)*(0.96-1.0)))"
						) if shift > 0.0 else (
								"((1.0)+"+
								 "((decayMode_1==1)*(genMatchedTau1DecayMode==1)*(0.98-1.0))+"+
								 "((decayMode_1==1)*(genMatchedTau1DecayMode>1)*(genMatchedTau1DecayMode<5)*(1.04-1.0)))*"+
								"((1.0)+"+
								 "((decayMode_2==1)*(genMatchedTau2DecayMode==1)*(0.98-1.0))+"+
								 "((decayMode_2==1)*(genMatchedTau2DecayMode>1)*(genMatchedTau2DecayMode<5)*(1.04-1.0)))"
						)
				)
		
		return plot_config


class RecoTauDecayModeFakeA1Systematic(SystematicShiftBase):
	
	def get_config(self, shift=0.0):
		plot_config = super(RecoTauDecayModeFakeA1Systematic, self).get_config(shift=shift)
		
		for index, weight in enumerate(plot_config.get("weights", [])):
			if (shift != 0.0) and (not "Run201" in plot_config["files"][index]) and (not "gen_ztt" in plot_config["nicks"][index]):
				plot_config["weights"][index] = ("({weight})*({syst})").format(
						weight=weight,
						syst=(
								"((1.0)+"+
								 "((decayMode_1==10)*(genMatchedTau1DecayMode==10)*(1.05-1.0))+"+
								 "((decayMode_1==10)*(genMatchedTau1DecayMode>10)*(genMatchedTau1DecayMode<15)*(0.76-1.0)))*"+
								"((1.0)+"+
								 "((decayMode_2==10)*(genMatchedTau2DecayMode==10)*(1.05-1.0))+"+
								 "((decayMode_2==10)*(genMatchedTau2DecayMode>10)*(genMatchedTau2DecayMode<15)*(0.76-1.0)))"
						) if shift > 0.0 else (
								"((1.0)+"+
								 "((decayMode_1==10)*(genMatchedTau1DecayMode==10)*(0.96-1.0))+"+
								 "((decayMode_1==10)*(genMatchedTau1DecayMode>10)*(genMatchedTau1DecayMode<15)*(1.23-1.0)))*"+
								"((1.0)+"+
								 "((decayMode_2==10)*(genMatchedTau2DecayMode==10)*(0.96-1.0))+"+
								 "((decayMode_2==10)*(genMatchedTau2DecayMode>10)*(genMatchedTau2DecayMode<15)*(1.23-1.0)))"
						)
				)

		return plot_config


class ElectronFakeOneProngTauEnergyScaleSystematic(SystematicShiftBase):

	def get_config(self, shift=0.0):
		plot_config = super(ElectronFakeOneProngTauEnergyScaleSystematic, self).get_config(shift=shift)

		for index, folder in enumerate(plot_config.get("folders", [])):
			if (shift != 0.0) and (not "Run201" in plot_config["files"][index]) and (not "gen_ztt" in plot_config["nicks"][index]):
				if shift > 0.0:
					plot_config["folders"][index] = folder.replace("nominal", "tauEleFakeEsOneProngUp")
				else:
					plot_config["folders"][index] = folder.replace("nominal", "tauEleFakeEsOneProngDown")

		return plot_config


class ElectronFakeOneProngPiZerosTauEnergyScaleSystematic(SystematicShiftBase):

	def get_config(self, shift=0.0):
		plot_config = super(ElectronFakeOneProngPiZerosTauEnergyScaleSystematic, self).get_config(shift=shift)

		for index, folder in enumerate(plot_config.get("folders", [])):
			if (shift != 0.0) and (not "Run201" in plot_config["files"][index]) and (not "gen_ztt" in plot_config["nicks"][index]):
				if shift > 0.0:
					plot_config["folders"][index] = folder.replace("nominal", "tauEleFakeEsOneProngPiZerosUp")
				else:
					plot_config["folders"][index] = folder.replace("nominal", "tauEleFakeEsOneProngPiZerosDown")

		return plot_config


class MuonFakeOneProngTauEnergyScaleSystematic(SystematicShiftBase):

	def get_config(self, shift=0.0):
		plot_config = super(MuonFakeOneProngTauEnergyScaleSystematic, self).get_config(shift=shift)

		for index, folder in enumerate(plot_config.get("folders", [])):
			if (shift != 0.0) and (not "Run201" in plot_config["files"][index]) and (not "gen_ztt" in plot_config["nicks"][index]):
				if shift > 0.0:
					plot_config["folders"][index] = folder.replace("nominal", "tauMuFakeEsOneProngUp")
				else:
					plot_config["folders"][index] = folder.replace("nominal", "tauMuFakeEsOneProngDown")

		return plot_config


class MuonFakeOneProngPiZerosTauEnergyScaleSystematic(SystematicShiftBase):

	def get_config(self, shift=0.0):
		plot_config = super(MuonFakeOneProngPiZerosTauEnergyScaleSystematic, self).get_config(shift=shift)

		for index, folder in enumerate(plot_config.get("folders", [])):
			if (shift != 0.0) and (not "Run201" in plot_config["files"][index]) and (not "gen_ztt" in plot_config["nicks"][index]):
				if shift > 0.0:
					plot_config["folders"][index] = folder.replace("nominal", "tauMuFakeEsOneProngPiZerosUp")
				else:
					plot_config["folders"][index] = folder.replace("nominal", "tauMuFakeEsOneProngPiZerosDown")

		return plot_config


class TauESOneProngSystematic(SystematicShiftBase):

	def get_config(self, shift=0.0):
		plot_config = super(TauESOneProngSystematic, self).get_config(shift=shift)

		for index, folder in enumerate(plot_config.get("folders", [])):
			if (shift != 0.0) and (not "Run201" in plot_config["files"][index]) and (not "gen_ztt" in plot_config["nicks"][index]):
				if shift > 0.0:
					plot_config["folders"][index] = folder.replace("nominal", "tauEsOneProngUp")
				else:
					plot_config["folders"][index] = folder.replace("nominal", "tauEsOneProngDown")

		return plot_config


class TauESOneProngPiZerosSystematic(SystematicShiftBase):

	def get_config(self, shift=0.0):
		plot_config = super(TauESOneProngPiZerosSystematic, self).get_config(shift=shift)

		for index, folder in enumerate(plot_config.get("folders", [])):
			if (shift != 0.0) and (not "Run201" in plot_config["files"][index]) and (not "gen_ztt" in plot_config["nicks"][index]):
				if shift > 0.0:
					plot_config["folders"][index] = folder.replace("nominal", "tauEsOneProngPiZerosUp")
				else:
					plot_config["folders"][index] = folder.replace("nominal", "tauEsOneProngPiZerosDown")

		return plot_config


class TauESThreeProngSystematic(SystematicShiftBase):

	def get_config(self, shift=0.0):
		plot_config = super(TauESThreeProngSystematic, self).get_config(shift=shift)

		for index, folder in enumerate(plot_config.get("folders", [])):
			if (shift != 0.0) and (not "Run201" in plot_config["files"][index]) and (not "gen_ztt" in plot_config["nicks"][index]):
				if shift > 0.0:
					plot_config["folders"][index] = folder.replace("nominal", "tauEsThreeProngUp")
				else:
					plot_config["folders"][index] = folder.replace("nominal", "tauEsThreeProngDown")

		return plot_config

class EmbeddingTTBarContaminationSystematic(SystematicShiftBase):

	def get_config(self, shift=0.0):
		plot_config = super(EmbeddingTTBarContaminationSystematic, self).get_config(shift=shift)

		for index, folder in enumerate(plot_config.get("folders", [])):
			if (shift != 0.0):
				if not "AddHistograms" in plot_config.get("analysis_modules", []):
					plot_config.setdefault("analysis_modules", []).append("AddHistograms")
				plot_config.setdefault("add_nicks", []).append("ztt_emb vvt ttt")
				plot_config.setdefault("add_result_nicks", []).append("ztt_emb")
				if shift > 0.0:
					plot_config.setdefault("add_scale_factors", []).append("1.0 0.1 0.1")
				else:
					plot_config.setdefault("add_scale_factors", []).append("1.0 -0.1 -0.1")

		return plot_config

class CMS_FiniteQuarkMass_13TeV(SystematicShiftBase):
	
	def get_config(self, shift=0.0):
		plot_config = super(CMS_FiniteQuarkMass_13TeV, self).get_config(shift=shift)
		
		for index, weight in enumerate(plot_config.get("weights", [])):
			if (shift != 0.0) and (not "Run201" in plot_config["files"][index]) and (not "gen_ztt" in plot_config["nicks"][index]):
				if shift < 0.0:
					plot_config["weights"][index] = weight.replace("quarkmassWeight","(quarkmassWeight*0.999)")
				else:
					plot_config["weights"][index] = weight.replace("quarkmassWeight","(1.0)")
		
		return plot_config
