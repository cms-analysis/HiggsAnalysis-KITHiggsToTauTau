
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import copy


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
		self["CMS_mFakeTau_1prong_13TeV"] = MuonToTauOneProngFakeSystematic
		self["CMS_mFakeTau_1prong1pizero_13TeV"] = MuonToTauOneProngPiZerosFakeSystematic
		self["CMS_htt_jetToTauFake_13TeV"] = JetToTauFakeSystematic
		self["CMS_scale_met_clustered_13TeV"] = MetJetEnSystematic
		self["CMS_scale_met_unclustered_13TeV"] = MetUnclusteredEnSystematic
		self["CMS_tauDMReco_1prong_13TeV"] = TauDMRecoOneProngSystematic
		self["CMS_tauDMReco_1prong1pizero_13TeV"] = TauDMRecoOneProngPiZerosSystematic
		self["CMS_tauDMReco_3prong_13TeV"] = TauDMRecoThreeProngSystematic
		self["CMS_ZLShape_mt_1prong_13TeV"] = MuonFakeOneProngTauEnergyScaleSystematic
		self["CMS_ZLShape_mt_1prong1pizero_13TeV"] = MuonFakeOneProngPiZerosTauEnergyScaleSystematic
		self["CMS_ZLShape_et_1prong_13TeV"] = ElectronFakeOneProngTauEnergyScaleSystematic
		self["CMS_ZLShape_et_1prong1pizero_13TeV"] = ElectronFakeOneProngPiZerosTauEnergyScaleSystematic
		self["CMS_scale_gg_13TeV"] = GGHRenormalizationScaleSystematic
		self["CMS_scale_t_1prong_13TeV"] = TauESOneProngSystematic
		self["CMS_scale_t_1prong1pizero_13TeV"] = TauESOneProngPiZerosSystematic
		self["CMS_scale_t_3prong_13TeV"] = TauESThreeProngSystematic
		
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
			"Closure"
		]
		
		for jecUncert in jecUncertNames:
			self["CMS_scale_j_"+jecUncert+"_13TeV"] = JecUncSplitSystematic
		
		# these uncertainties currently need to be implemented in your datacards script
		self["WSFUncert_mt_0jet_13TeV"] = Nominal
		self["WSFUncert_et_0jet_13TeV"] = Nominal
		self["WSFUncert_mt_boosted_13TeV"] = Nominal
		self["WSFUncert_et_boosted_13TeV"] = Nominal
		self["WSFUncert_mt_vbf_13TeV"] = Nominal
		self["WSFUncert_et_vbf_13TeV"] = Nominal
		self["WSFUncert_lt_13TeV"] = Nominal
		self["CMS_htt_zmumuShape_VBF_13TeV"] = Nominal


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
			if not "Run201" in plot_config["files"][index]:
				if shift > 0.0:
					plot_config["weights"][index] = weight+"*"+w
				elif shift < 0.0:
					plot_config["weights"][index] = weight+"*(2-"+w+")"
		
		return plot_config


class Nominal(SystematicShiftBase):
	pass


class JecUncSystematic(SystematicShiftBase):
	
	def get_config(self, shift=0.0):
		plot_config = super(JecUncSystematic, self).get_config(shift=shift)
		
		for index, folder in enumerate(plot_config.get("folders", [])):
			if not "Run201" in plot_config["files"][index]:
				if shift > 0.0:
					plot_config["folders"][index] = folder.replace("nominal", "jecUncUp")
				elif shift < 0.0:
					plot_config["folders"][index] = folder.replace("nominal", "jecUncDown")
		
		return plot_config


class JecUncSplitSystematic(SystematicShiftBase):
	
	def __init__(self, plot_config, jecUncertainty):
		super(JecUncSplitSystematic, self).__init__(plot_config)
		self.plot_config = plot_config
		self.jecUncertainty = jecUncertainty
	
	def get_config(self, shift=0.0):
		plot_config = super(JecUncSplitSystematic, self).get_config(shift=shift)
		
		for index, folder in enumerate(plot_config.get("folders", [])):
			if not "Run201" in plot_config["files"][index]:
				if shift > 0.0:
					plot_config["folders"][index] = folder.replace("nominal", "jecUncUp")
				elif shift < 0.0:
					plot_config["folders"][index] = folder.replace("nominal", "jecUncDown")
		
		for index, weight in enumerate(plot_config.get("weights", [])):
			if not "Run201" in plot_config["files"][index]:
				if shift > 0.0 or shift < 0.0:
					plot_config["weights"][index] = weight.replace("njetspt30", "njetspt30_"+self.jecUncertainty).replace("mjj", "mjj_"+self.jecUncertainty).replace("jdeta", "jdeta_"+self.jecUncertainty)
		
		return plot_config


class TTBarShapeSystematic(SystematicShiftBase):
	
	def get_config(self, shift=0.0):
		plot_config = super(TTBarShapeSystematic, self).get_config(shift=shift)
		
		for index, weight in enumerate(plot_config.get("weights", [])):
			if not "Run201" in plot_config["files"][index]:
				if shift > 0.0:
					plot_config["weights"][index] = weight.replace("topPtReweightWeight", "topPtReweightWeight*topPtReweightWeight")
				elif shift < 0.0:
					plot_config["weights"][index] = weight.replace("topPtReweightWeight", "(1.0)")
		
		return plot_config


class DYShapeSystematic(SystematicShiftBase):
	
	def get_config(self, shift=0.0):
		plot_config = super(DYShapeSystematic, self).get_config(shift=shift)
		
		for index, weight in enumerate(plot_config.get("weights", [])):
			if not "Run201" in plot_config["files"][index]:
				if shift > 0.0:
					plot_config["weights"][index] = weight.replace("zPtReweightWeight","zPtReweightWeight*zPtReweightWeight")
				elif shift < 0.0:
					plot_config["weights"][index] = weight.replace("zPtReweightWeight","(1.0)")
		
		return plot_config


class JetFakeTauQCDShapeSystematic(SystematicShiftBase):
	
	def get_config(self, shift=0.0):
		plot_config = super(JetFakeTauQCDShapeSystematic, self).get_config(shift=shift)
		
		for index, weight in enumerate(plot_config.get("weights", [])):
			if not "Run201" in plot_config["files"][index]:
				if shift > 0.0:
					plot_config["weights"][index] = weight.replace("jetToTauFakeWeight_comb", "jetToTauFakeWeight_qcd_up")
				elif shift < 0.0:
					plot_config["weights"][index] = weight.replace("jetToTauFakeWeight_comb", "jetToTauFakeWeight_qcd_down")
		
		return plot_config


class JetFakeTauWShapeSystematic(SystematicShiftBase):
	
	def get_config(self, shift=0.0):
		plot_config = super(JetFakeTauWShapeSystematic, self).get_config(shift=shift)
		
		for index, weight in enumerate(plot_config.get("weights", [])):
			if not "Run201" in plot_config["files"][index]:
				if shift > 0.0:
					plot_config["weights"][index] = weight.replace("jetToTauFakeWeight_comb", "jetToTauFakeWeight_w_up")
				elif shift < 0.0:
					plot_config["weights"][index] = weight.replace("jetToTauFakeWeight_comb", "jetToTauFakeWeight_w_down")
		
		return plot_config


class JetFakeTauTTcorrShapeSystematic(SystematicShiftBase):
	
	def get_config(self, shift=0.0):
		plot_config = super(JetFakeTauTTcorrShapeSystematic, self).get_config(shift=shift)
		
		for index, weight in enumerate(plot_config.get("weights", [])):
			if not "Run201" in plot_config["files"][index]:
				if shift > 0.0:
					plot_config["weights"][index] = weight.replace("jetToTauFakeWeight_comb", "jetToTauFakeWeight_tt_corr_up")
				elif shift < 0.0:
					plot_config["weights"][index] = weight.replace("jetToTauFakeWeight_comb", "jetToTauFakeWeight_tt_corr_down")
		
		return plot_config


class JetFakeTauTTstatShapeSystematic(SystematicShiftBase):
	
	def get_config(self, shift=0.0):
		plot_config = super(JetFakeTauTTstatShapeSystematic, self).get_config(shift=shift)
		
		for index, weight in enumerate(plot_config.get("weights", [])):
			if not "Run201" in plot_config["files"][index]:
				if shift > 0.0:
					plot_config["weights"][index] = weight.replace("jetToTauFakeWeight_comb", "jetToTauFakeWeight_tt_stat_up")
				elif shift < 0.0:
					plot_config["weights"][index] = weight.replace("jetToTauFakeWeight_comb", "jetToTauFakeWeight_tt_stat_down")
		
		return plot_config


class JetFakeTauFracQCDShapeSystematic(SystematicShiftBase):
	
	def get_config(self, shift=0.0):
		plot_config = super(JetFakeTauFracQCDShapeSystematic, self).get_config(shift=shift)
		
		for index, weight in enumerate(plot_config.get("weights", [])):
			if not "Run201" in plot_config["files"][index]:
				if shift > 0.0:
					plot_config["weights"][index] = weight.replace("jetToTauFakeWeight_comb", "jetToTauFakeWeight_frac_qcd_up")
				elif shift < 0.0:
					plot_config["weights"][index] = weight.replace("jetToTauFakeWeight_comb", "jetToTauFakeWeight_frac_qcd_down")
		
		return plot_config


class JetFakeTauFracWShapeSystematic(SystematicShiftBase):
	
	def get_config(self, shift=0.0):
		plot_config = super(JetFakeTauFracWShapeSystematic, self).get_config(shift=shift)
		
		for index, weight in enumerate(plot_config.get("weights", [])):
			if not "Run201" in plot_config["files"][index]:
				if shift > 0.0:
					plot_config["weights"][index] = weight.replace("jetToTauFakeWeight_comb", "jetToTauFakeWeight_frac_w_up")
				elif shift < 0.0:
					plot_config["weights"][index] = weight.replace("jetToTauFakeWeight_comb", "jetToTauFakeWeight_frac_w_down")
		
		return plot_config


class JetFakeTauFracTTShapeSystematic(SystematicShiftBase):
	
	def get_config(self, shift=0.0):
		plot_config = super(JetFakeTauFracTTShapeSystematic, self).get_config(shift=shift)
		
		for index, weight in enumerate(plot_config.get("weights", [])):
			if not "Run201" in plot_config["files"][index]:
				if shift > 0.0:
					plot_config["weights"][index] = weight.replace("jetToTauFakeWeight_comb", "jetToTauFakeWeight_frac_tt_up")
				elif shift < 0.0:
					plot_config["weights"][index] = weight.replace("jetToTauFakeWeight_comb", "jetToTauFakeWeight_frac_tt_down")
		
		return plot_config


class JetFakeTauFracDYShapeSystematic(SystematicShiftBase):
	
	def get_config(self, shift=0.0):
		plot_config = super(JetFakeTauFracDYShapeSystematic, self).get_config(shift=shift)
		
		for index, weight in enumerate(plot_config.get("weights", [])):
			if not "Run201" in plot_config["files"][index]:
				if shift > 0.0:
					plot_config["weights"][index] = weight.replace("jetToTauFakeWeight_comb", "jetToTauFakeWeight_frac_dy_up")
				elif shift < 0.0:
					plot_config["weights"][index] = weight.replace("jetToTauFakeWeight_comb", "jetToTauFakeWeight_frac_dy_down")
		
		return plot_config


class MuFakeTauEsSystematic(SystematicShiftBase):
	
	def get_config(self, shift=0.0):
		plot_config = super(MuFakeTauEsSystematic, self).get_config(shift=shift)
		
		for index, folder in enumerate(plot_config.get("folders", [])):
			if not "Run201" in plot_config["files"][index]:
				if shift > 0.0:
					plot_config["folders"][index] = folder.replace("nominal", "muonEsUp")
				elif shift < 0.0:
					plot_config["folders"][index] = folder.replace("nominal", "muonEsDown")
		
		return plot_config


class EleFakeTauEsSystematic(SystematicShiftBase):
	
	def get_config(self, shift=0.0):
		plot_config = super(EleFakeTauEsSystematic, self).get_config(shift=shift)
		
		for index, folder in enumerate(plot_config.get("folders", [])):
			if not "Run201" in plot_config["files"][index]:
				if shift > 0.0:
					plot_config["folders"][index] = folder.replace("nominal", "eleEsUp")
				elif shift < 0.0:
					plot_config["folders"][index] = folder.replace("nominal", "eleEsDown")
		
		return plot_config


class TauEsSystematic(SystematicShiftBase):
	
	def get_config(self, shift=0.0):
		plot_config = super(TauEsSystematic, self).get_config(shift=shift)
		
		for index, folder in enumerate(plot_config.get("folders", [])):
			if not "Run201" in plot_config["files"][index]:
				if shift > 0.0:
					plot_config["folders"][index] = folder.replace("nominal", "tauEsUp")
				elif shift < 0.0:
					plot_config["folders"][index] = folder.replace("nominal", "tauEsDown")
		
		return plot_config


class EleEsSystematic(SystematicShiftBase):
	
	def get_config(self, shift=0.0):
		plot_config = super(EleEsSystematic, self).get_config(shift=shift)
		
		for index, folder in enumerate(plot_config.get("folders", [])):
			if not "Run201" in plot_config["files"][index]:
				if shift > 0.0:
					plot_config["folders"][index] = folder.replace("nominal", "eleEsUp")
				elif shift < 0.0:
					plot_config["folders"][index] = folder.replace("nominal", "eleEsDown")
		
		return plot_config


class MuonEsSystematic(SystematicShiftBase):
	
	def get_config(self, shift=0.0):
		plot_config = super(MuonEsSystematic, self).get_config(shift=shift)
		
		for index, folder in enumerate(plot_config.get("folders", [])):
			if not "Run201" in plot_config["files"][index]:
				if shift > 0.0:
					plot_config["folders"][index] = folder.replace("nominal", "muonEsUp")
				elif shift < 0.0:
					plot_config["folders"][index] = folder.replace("nominal", "muonEsDown")
		
		return plot_config


class MetResponseSystematic(SystematicShiftBase):
	
	def get_config(self, shift=0.0):
		plot_config = super(MetResponseSystematic, self).get_config(shift=shift)
		
		for index, folder in enumerate(plot_config.get("folders", [])):
			if not "Run201" in plot_config["files"][index]:
				if shift > 0.0:
					plot_config["folders"][index] = folder.replace("nominal", "metResponseUp")
				elif shift < 0.0:
					plot_config["folders"][index] = folder.replace("nominal", "metResponseDown")
		
		return plot_config


class TagEleEsSystematic(SystematicShiftBase):
	
	def get_config(self, shift=0.0):
		plot_config = super(TagEleEsSystematic, self).get_config(shift=shift)
		
		for index, folder in enumerate(plot_config.get("folders", [])):
			if not "Run201" in plot_config["files"][index]:
				if shift > 0.0:
					plot_config["folders"][index] = folder.replace("tagEleEsNom", "tagEleEsUp")
				elif shift < 0.0:
					plot_config["folders"][index] = folder.replace("tagEleEsNom", "tagEleEsDown")
		
		return plot_config


class ProbeTauEsSystematic(SystematicShiftBase):
	
	def get_config(self, shift=0.0):
		plot_config = super(ProbeTauEsSystematic, self).get_config(shift=shift)
		
		for index, folder in enumerate(plot_config.get("folders", [])):
			if not "Run201" in plot_config["files"][index]:
				if shift > 0.0:
					plot_config["folders"][index] = folder.replace("probeTauEsNom", "probeTauEsUp")
				elif shift < 0.0:
					plot_config["folders"][index] = folder.replace("probeTauEsNom", "probeTauEsDown")
		
		return plot_config


class ProbeEleEsSystematic(SystematicShiftBase):
	
	def get_config(self, shift=0.0):
		plot_config = super(ProbeEleEsSystematic, self).get_config(shift=shift)
		
		for index, folder in enumerate(plot_config.get("folders", [])):
			if not "Run201" in plot_config["files"][index]:
				if shift > 0.0:
					plot_config["folders"][index] = folder.replace("probeEleEsNom", "probeEleEsUp")
				elif shift < 0.0:
					plot_config["folders"][index] = folder.replace("probeEleEsNom", "probeEleEsDown")
		
		return plot_config


class MassResSystematic(SystematicShiftBase):
	
	def get_config(self, shift=0.0):
		plot_config = super(MassResSystematic, self).get_config(shift=shift)
		
		for index, expression in enumerate(plot_config.get("x_expressions", [])):
			if not "Run201" in plot_config["files"][index]:
				if shift > 0.0:
					plot_config["x_expressions"][index] = expression.replace("m_vis", "diLepMassSmearUp")
				elif shift < 0.0:
					plot_config["x_expressions"][index] = expression.replace("m_vis", "diLepMassSmearDown")
		
		return plot_config


class BTagSystematic(SystematicShiftBase):
	
	def get_config(self, shift=0.0):
		plot_config = super(BTagSystematic, self).get_config(shift=shift)
		
		for index, folder in enumerate(plot_config.get("folders", [])):
			if not "Run201" in plot_config["files"][index]:
				if shift > 0.0:
					plot_config["folders"][index] = folder.replace("nominal", "bTagUp")
				elif shift < 0.0:
					plot_config["folders"][index] = folder.replace("nominal", "bTagDown")
		
		return plot_config


class BMistagSystematic(SystematicShiftBase):
	
	def get_config(self, shift=0.0):
		plot_config = super(BMistagSystematic, self).get_config(shift=shift)
		
		for index, folder in enumerate(plot_config.get("folders", [])):
			if not "Run201" in plot_config["files"][index]:
				if shift > 0.0:
					plot_config["folders"][index] = folder.replace("nominal", "bMistagUp")
				elif shift < 0.0:
					plot_config["folders"][index] = folder.replace("nominal", "bMistagDown")
		
		return plot_config


class ElectronToTauOneProngFakeSystematic(SystematicShiftBase):
	
	def get_config(self, shift=0.0):
		plot_config = super(ElectronToTauOneProngFakeSystematic, self).get_config(shift=shift)
		
		for index, weight in enumerate(plot_config.get("weights", [])):
			if not "Run201" in plot_config["files"][index]:
				if shift > 0.0:
					plot_config["weights"][index] = weight.replace("(((decayMode_2 == 0)*0.98) + ((decayMode_2 == 1 || decayMode_2 == 2)*1.2) + ((decayMode_2 == 10)*1.0))", "(((decayMode_2 == 0)*0.98*1.12) + ((decayMode_2 == 1 || decayMode_2 == 2)*1.2) + ((decayMode_2 == 10)*1.0))")
				elif shift < 0.0:
					plot_config["weights"][index] = weight.replace("(((decayMode_2 == 0)*0.98) + ((decayMode_2 == 1 || decayMode_2 == 2)*1.2) + ((decayMode_2 == 10)*1.0))", "(((decayMode_2 == 0)*0.98*0.88) + ((decayMode_2 == 1 || decayMode_2 == 2)*1.2) + ((decayMode_2 == 10)*1.0))")
		
		return plot_config


class ElectronToTauOneProngPiZerosFakeSystematic(SystematicShiftBase):
	
	def get_config(self, shift=0.0):
		plot_config = super(ElectronToTauOneProngPiZerosFakeSystematic, self).get_config(shift=shift)
		
		for index, weight in enumerate(plot_config.get("weights", [])):
			if not "Run201" in plot_config["files"][index]:
				if shift > 0.0:
					plot_config["weights"][index] = weight.replace("(((decayMode_2 == 0)*0.98) + ((decayMode_2 == 1 || decayMode_2 == 2)*1.2) + ((decayMode_2 == 10)*1.0))", "(((decayMode_2 == 0)*0.98) + ((decayMode_2 == 1 || decayMode_2 == 2)*1.2*1.12) + ((decayMode_2 == 10)*1.0))")
				elif shift < 0.0:
					plot_config["weights"][index] = weight.replace("(((decayMode_2 == 0)*0.98) + ((decayMode_2 == 1 || decayMode_2 == 2)*1.2) + ((decayMode_2 == 10)*1.0))", "(((decayMode_2 == 0)*0.98) + ((decayMode_2 == 1 || decayMode_2 == 2)*1.2*0.88) + ((decayMode_2 == 10)*1.0))")
		
		return plot_config


class MuonToTauOneProngFakeSystematic(SystematicShiftBase):
	
	def get_config(self, shift=0.0):
		plot_config = super(MuonToTauOneProngFakeSystematic, self).get_config(shift=shift)
		
		for index, weight in enumerate(plot_config.get("weights", [])):
			if not "Run201" in plot_config["files"][index]:
				if shift > 0.0:
					plot_config["weights"][index] = weight.replace("(((decayMode_2 == 0)*0.75) + ((decayMode_2 == 1 || decayMode_2 == 2)*1.0) + ((decayMode_2 == 10)*1.0))", "(((decayMode_2 == 0)*0.75*1.25) + ((decayMode_2 == 1 || decayMode_2 == 2)*1.0) + ((decayMode_2 == 10)*1.0))")
				elif shift < 0.0:
					plot_config["weights"][index] = weight.replace("(((decayMode_2 == 0)*0.75) + ((decayMode_2 == 1 || decayMode_2 == 2)*1.0) + ((decayMode_2 == 10)*1.0))", "(((decayMode_2 == 0)*0.75*0.75) + ((decayMode_2 == 1 || decayMode_2 == 2)*1.0) + ((decayMode_2 == 10)*1.0))")
		
		return plot_config


class MuonToTauOneProngPiZerosFakeSystematic(SystematicShiftBase):
	
	def get_config(self, shift=0.0):
		plot_config = super(MuonToTauOneProngPiZerosFakeSystematic, self).get_config(shift=shift)
		
		for index, weight in enumerate(plot_config.get("weights", [])):
			if not "Run201" in plot_config["files"][index]:
				if shift > 0.0:
					plot_config["weights"][index] = weight.replace("(((decayMode_2 == 0)*0.75) + ((decayMode_2 == 1 || decayMode_2 == 2)*1.0) + ((decayMode_2 == 10)*1.0))", "(((decayMode_2 == 0)*0.75) + ((decayMode_2 == 1 || decayMode_2 == 2)*1.25) + ((decayMode_2 == 10)*1.0))")
				elif shift < 0.0:
					plot_config["weights"][index] = weight.replace("(((decayMode_2 == 0)*0.75) + ((decayMode_2 == 1 || decayMode_2 == 2)*1.0) + ((decayMode_2 == 10)*1.0))", "(((decayMode_2 == 0)*0.75) + ((decayMode_2 == 1 || decayMode_2 == 2)*0.75) + ((decayMode_2 == 10)*1.0))")
		
		return plot_config


class JetToTauFakeSystematic(SystematicShiftBase):
	
	def get_config(self, shift=0.0):
		plot_config = super(JetToTauFakeSystematic, self).get_config(shift=shift)
		
		for index, folder in enumerate(plot_config.get("folders", [])):
			if not "Run201" in plot_config["files"][index]:
				if shift > 0.0:
					plot_config["folders"][index] = folder.replace("nominal", "tauJetFakeEsUp")
				elif shift < 0.0:
					plot_config["folders"][index] = folder.replace("nominal", "tauJetFakeEsDown")
		
		return plot_config


class MetJetEnSystematic(SystematicShiftBase):
	
	def get_config(self, shift=0.0):
		plot_config = super(MetJetEnSystematic, self).get_config(shift=shift)
		
		for index, folder in enumerate(plot_config.get("folders", [])):
			if not "Run201" in plot_config["files"][index]:
				if shift > 0.0:
					plot_config["folders"][index] = folder.replace("nominal", "metJetEnUp")
				elif shift < 0.0:
					plot_config["folders"][index] = folder.replace("nominal", "metJetEnDown")
		
		return plot_config


class MetUnclusteredEnSystematic(SystematicShiftBase):
	
	def get_config(self, shift=0.0):
		plot_config = super(MetUnclusteredEnSystematic, self).get_config(shift=shift)
		
		for index, folder in enumerate(plot_config.get("folders", [])):
			if not "Run201" in plot_config["files"][index]:
				if shift > 0.0:
					plot_config["folders"][index] = folder.replace("nominal", "metUnclusteredEnUp")
				elif shift < 0.0:
					plot_config["folders"][index] = folder.replace("nominal", "metUnclusteredEnDown")
		
		return plot_config


class TauDMRecoOneProngSystematic(SystematicShiftBase):
	
	def get_config(self, shift=0.0):
		plot_config = super(TauDMRecoOneProngSystematic, self).get_config(shift=shift)
		
		for index, weight in enumerate(plot_config.get("weights", [])):
			if not "Run201" in plot_config["files"][index]:
				if shift > 0.0:
					plot_config["weights"][index] = weight.replace("(((decayMode_2 == 0)*1.0) + ((decayMode_2 == 1 || decayMode_2 == 2)*1.0) + ((decayMode_2 == 10)*1.0))", "(((decayMode_2 == 0)*1.03) + ((decayMode_2 == 1 || decayMode_2 == 2)*1.0) + ((decayMode_2 == 10)*1.0))")
				elif shift < 0.0:
					plot_config["weights"][index] = weight.replace("(((decayMode_2 == 0)*1.0) + ((decayMode_2 == 1 || decayMode_2 == 2)*1.0) + ((decayMode_2 == 10)*1.0))", "(((decayMode_2 == 0)*0.97) + ((decayMode_2 == 1 || decayMode_2 == 2)*1.0) + ((decayMode_2 == 10)*1.0))")
		
		return plot_config


class TauDMRecoOneProngPiZerosSystematic(SystematicShiftBase):
	
	def get_config(self, shift=0.0):
		plot_config = super(TauDMRecoOneProngPiZerosSystematic, self).get_config(shift=shift)
		
		for index, weight in enumerate(plot_config.get("weights", [])):
			if not "Run201" in plot_config["files"][index]:
				if shift > 0.0:
					plot_config["weights"][index] = weight.replace("(((decayMode_2 == 0)*1.0) + ((decayMode_2 == 1 || decayMode_2 == 2)*1.0) + ((decayMode_2 == 10)*1.0))", "(((decayMode_2 == 0)*1.0) + ((decayMode_2 == 1 || decayMode_2 == 2)*1.03) + ((decayMode_2 == 10)*1.0))")
				elif shift < 0.0:
					plot_config["weights"][index] = weight.replace("(((decayMode_2 == 0)*1.0) + ((decayMode_2 == 1 || decayMode_2 == 2)*1.0) + ((decayMode_2 == 10)*1.0))", "(((decayMode_2 == 0)*1.0) + ((decayMode_2 == 1 || decayMode_2 == 2)*0.97) + ((decayMode_2 == 10)*1.0))")
		
		return plot_config


class TauDMRecoThreeProngSystematic(SystematicShiftBase):
	
	def get_config(self, shift=0.0):
		plot_config = super(TauDMRecoThreeProngSystematic, self).get_config(shift=shift)
		
		for index, weight in enumerate(plot_config.get("weights", [])):
			if not "Run201" in plot_config["files"][index]:
				if shift > 0.0:
					plot_config["weights"][index] = weight.replace("(((decayMode_2 == 0)*1.0) + ((decayMode_2 == 1 || decayMode_2 == 2)*1.0) + ((decayMode_2 == 10)*1.0))", "(((decayMode_2 == 0)*1.0) + ((decayMode_2 == 1 || decayMode_2 == 2)*1.0) + ((decayMode_2 == 10)*1.03))")
				elif shift < 0.0:
					plot_config["weights"][index] = weight.replace("(((decayMode_2 == 0)*1.0) + ((decayMode_2 == 1 || decayMode_2 == 2)*1.0) + ((decayMode_2 == 10)*1.0))", "(((decayMode_2 == 0)*1.0) + ((decayMode_2 == 1 || decayMode_2 == 2)*1.0) + ((decayMode_2 == 10)*0.97))")
		
		return plot_config


class ElectronFakeOneProngTauEnergyScaleSystematic(SystematicShiftBase):
	
	def get_config(self, shift=0.0):
		plot_config = super(ElectronFakeOneProngTauEnergyScaleSystematic, self).get_config(shift=shift)
		
		for index, folder in enumerate(plot_config.get("folders", [])):
			if not "Run201" in plot_config["files"][index]:
				if shift > 0.0:
					plot_config["folders"][index] = folder.replace("nominal", "tauEleFakeEsOneProngUp")
				elif shift < 0.0:
					plot_config["folders"][index] = folder.replace("nominal", "tauEleFakeEsOneProngDown")
		
		return plot_config


class ElectronFakeOneProngPiZerosTauEnergyScaleSystematic(SystematicShiftBase):
	
	def get_config(self, shift=0.0):
		plot_config = super(ElectronFakeOneProngPiZerosTauEnergyScaleSystematic, self).get_config(shift=shift)
		
		for index, folder in enumerate(plot_config.get("folders", [])):
			if not "Run201" in plot_config["files"][index]:
				if shift > 0.0:
					plot_config["folders"][index] = folder.replace("nominal", "tauEleFakeEsOneProngPiZerosUp")
				elif shift < 0.0:
					plot_config["folders"][index] = folder.replace("nominal", "tauEleFakeEsOneProngPiZerosDown")
		
		return plot_config


class MuonFakeOneProngTauEnergyScaleSystematic(SystematicShiftBase):
	
	def get_config(self, shift=0.0):
		plot_config = super(MuonFakeOneProngTauEnergyScaleSystematic, self).get_config(shift=shift)
		
		for index, folder in enumerate(plot_config.get("folders", [])):
			if not "Run201" in plot_config["files"][index]:
				if shift > 0.0:
					plot_config["folders"][index] = folder.replace("nominal", "tauMuFakeEsOneProngUp")
				elif shift < 0.0:
					plot_config["folders"][index] = folder.replace("nominal", "tauMuFakeEsOneProngDown")
		
		return plot_config


class MuonFakeOneProngPiZerosTauEnergyScaleSystematic(SystematicShiftBase):
	
	def get_config(self, shift=0.0):
		plot_config = super(MuonFakeOneProngPiZerosTauEnergyScaleSystematic, self).get_config(shift=shift)
		
		for index, folder in enumerate(plot_config.get("folders", [])):
			if not "Run201" in plot_config["files"][index]:
				if shift > 0.0:
					plot_config["folders"][index] = folder.replace("nominal", "tauMuFakeEsOneProngPiZerosUp")
				elif shift < 0.0:
					plot_config["folders"][index] = folder.replace("nominal", "tauMuFakeEsOneProngPiZerosDown")
		
		return plot_config


class TauESOneProngSystematic(SystematicShiftBase):
	
	def get_config(self, shift=0.0):
		plot_config = super(TauESOneProngSystematic, self).get_config(shift=shift)
		
		for index, folder in enumerate(plot_config.get("folders", [])):
			if not "Run201" in plot_config["files"][index]:
				if shift > 0.0:
					plot_config["folders"][index] = folder.replace("nominal", "tauEsOneProngUp")
				elif shift < 0.0:
					plot_config["folders"][index] = folder.replace("nominal", "tauEsOneProngDown")
		
		return plot_config


class TauESOneProngPiZerosSystematic(SystematicShiftBase):
	
	def get_config(self, shift=0.0):
		plot_config = super(TauESOneProngPiZerosSystematic, self).get_config(shift=shift)
		
		for index, folder in enumerate(plot_config.get("folders", [])):
			if not "Run201" in plot_config["files"][index]:
				if shift > 0.0:
					plot_config["folders"][index] = folder.replace("nominal", "tauEsOneProngPiZerosUp")
				elif shift < 0.0:
					plot_config["folders"][index] = folder.replace("nominal", "tauEsOneProngPiZerosDown")
		
		return plot_config


class TauESThreeProngSystematic(SystematicShiftBase):
	
	def get_config(self, shift=0.0):
		plot_config = super(TauESThreeProngSystematic, self).get_config(shift=shift)
		
		for index, folder in enumerate(plot_config.get("folders", [])):
			if not "Run201" in plot_config["files"][index]:
				if shift > 0.0:
					plot_config["folders"][index] = folder.replace("nominal", "tauEsThreeProngUp")
				elif shift < 0.0:
					plot_config["folders"][index] = folder.replace("nominal", "tauEsThreeProngDown")
		
		return plot_config
