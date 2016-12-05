
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
		self["CMS_htt_ttbarShape_13TeV"] = TTBarShapeSystematic
		self["CMS_htt_dyShape_13TeV"] = DyShapeSystematic
		self["CMS_eff_b_13TeV"] = BTagSystematic
		self["CMS_mistag_b_13TeV"] = BMistagSystematic
		
		for channel in ["et", "mt"]:
			self["CMS_ztt_ff_qcd_syst_"+channel+"_13TeV"] = JetFakeTauQCDsystShapeSystematic
			self["CMS_ztt_ff_qcd_stat_"+channel+"_13TeV"] = JetFakeTauQCDstatShapeSystematic
			self["CMS_ztt_ff_w_syst_"+channel+"_13TeV"] = JetFakeTauWsystShapeSystematic
			self["CMS_ztt_ff_w_stat_"+channel+"_13TeV"] = JetFakeTauWstatShapeSystematic
			self["CMS_ztt_ff_tt_syst_"+channel+"_13TeV"] = JetFakeTauTTsystShapeSystematic
			self["CMS_ztt_ff_tt_stat_"+channel+"_13TeV"] = JetFakeTauTTstatShapeSystematic
			
			# exact copies of the above
			for category in ["inclusive", "0jet", "1jet_low", "1jet_medium", "1jet_high", "2jet_vbf", "1bjet", "2bjet"]:
				self["CMS_ztt_ff_qcd_syst_"+channel+"_"+category+"_13TeV"] = JetFakeTauQCDsystShapeSystematic
				self["CMS_ztt_ff_qcd_stat_"+channel+"_"+category+"_13TeV"] = JetFakeTauQCDstatShapeSystematic
				self["CMS_ztt_ff_w_syst_"+channel+"_"+category+"_13TeV"] = JetFakeTauWsystShapeSystematic
				self["CMS_ztt_ff_w_stat_"+channel+"_"+category+"_13TeV"] = JetFakeTauWstatShapeSystematic
				self["CMS_ztt_ff_tt_syst_"+channel+"_"+category+"_13TeV"] = JetFakeTauTTsystShapeSystematic
				self["CMS_ztt_ff_tt_stat_"+channel+"_"+category+"_13TeV"] = JetFakeTauTTstatShapeSystematic
		
		for channel in ["mt", "et", "tt"]:
			self["CMS_scale_t_"+channel+"_13TeV"] = TauEsSystematic
		
		for channel in ["em", "et"]:
			self["CMS_scale_e_"+channel+"_13TeV"] = EleEsSystematic
		
		for channel in ["em", "mt"]:
			self["CMS_scale_m_"+channel+"_13TeV"] = MuonEsSystematic
		
		for channel in ["em", "et", "mt", "tt"]:
			self["CMS_scale_met_corr_"+channel+"_13TeV"] = MetResponseSystematic
		
		for channel in ["em", "et", "mt", "tt"]:
			self["CMS_scale_met_corr_13TeV"] = MetResponseSystematic # exact copy of the above
		
		for channel in ["em", "et", "mt", "tt"]:
			self["CMS_res_met_corr_"+channel+"_13TeV"] = MetResolutionSystematic
		
		for channel in ["em", "et", "mt", "tt"]:
			self["CMS_res_met_corr_13TeV"] = MetResolutionSystematic # exact copy of the above
		
		for channel in ["et"]:
			self["CMS_scale_probetau_"+channel+"_13TeV"] = ProbeTauEsSystematic
		
		for channel in ["et"]:
			self["CMS_scale_probeele_"+channel+"_13TeV"] = ProbeEleEsSystematic
		
		for channel in ["et"]:
			self["CMS_scale_tagele_"+channel+"_13TeV"] = TagEleEsSystematic
		
		for channel in ["et"]:
			self["CMS_scale_massRes_"+channel+"_13TeV"] = MassResSystematic


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


class Nominal(SystematicShiftBase):
	pass


class JecUncSystematic(SystematicShiftBase):
	
	def get_config(self, shift=0.0):
		plot_config = super(JecUncSystematic, self).get_config(shift=shift)
		
		for index, folder in enumerate(plot_config.get("folders", [])):
			if not "Run201" in plot_config["files"][index]:
				if shift > 0.0:
					plot_config["folders"][index] = folder.replace("jecUncNom", "jecUncUp")
				elif shift < 0.0:
					plot_config["folders"][index] = folder.replace("jecUncNom", "jecUncDown")
		
		return plot_config


class TTBarShapeSystematic(SystematicShiftBase):
	
	def get_config(self, shift=0.0):
		plot_config = super(TTBarShapeSystematic, self).get_config(shift=shift)
		
		for index, weight in enumerate(plot_config.get("weights", [])):
			if not "data" in plot_config["nicks"][index]:
				if shift > 0.0:
					plot_config["weights"][index] = weight.replace("topPtReweightWeight", "topPtReweightWeight*topPtReweightWeight")
				elif shift < 0.0:
					plot_config["weights"][index] = weight.replace("topPtReweightWeight", "(1.0)")
		
		return plot_config

class DyShapeSystematic(SystematicShiftBase):
	
	def get_config(self, shift=0.0):
		plot_config = super(DyShapeSystematic, self).get_config(shift=shift)
		
		for index, weight in enumerate(plot_config.get("weights", [])):
			if not "data" in plot_config["nicks"][index]:
				if shift > 0.0:
					plot_config["weights"][index] = weight.replace("zReweightingWeight", "zReweightingWeight*zReweightingWeight")
				elif shift < 0.0:
					plot_config["weights"][index] = weight.replace("zReweightingWeight", "(1.0)")
		
		return plot_config

class JetFakeTauQCDsystShapeSystematic(SystematicShiftBase):
	
	def get_config(self, shift=0.0):
		plot_config = super(JetFakeTauQCDsystShapeSystematic, self).get_config(shift=shift)
		
		for index, weight in enumerate(plot_config.get("weights", [])):
			if not "data" in plot_config["nicks"][index]:
				pieces = [e+'_comb' if not e.startswith("_") else e for e in weight.split('_comb')]
				pieces_split = pieces[1].split("*",1)
				if shift > 0.0:
					plot_config["weights"][index] = pieces[0] + pieces_split[0] + '_qcd_syst_up*' + pieces_split[1] 
				elif shift < 0.0:
					plot_config["weights"][index] = pieces[0] + pieces_split[0] + '_qcd_syst_down*' + pieces_split[1] 
		
		return plot_config


class JetFakeTauQCDstatShapeSystematic(SystematicShiftBase):

        def get_config(self, shift=0.0):
                plot_config = super(JetFakeTauQCDstatShapeSystematic, self).get_config(shift=shift)

                for index, weight in enumerate(plot_config.get("weights", [])):
                        if not "data" in plot_config["nicks"][index]:
				pieces = [e+'_comb' if not e.startswith("_") else e for e in weight.split('_comb')]
				pieces_split = pieces[1].split("*",1)
                                if shift > 0.0:
                                        plot_config["weights"][index] =  pieces[0] + pieces_split[0] + '_qcd_stat_up*' + pieces_split[1] 
                                elif shift < 0.0:
                                        plot_config["weights"][index] = pieces[0] + pieces_split[0] + '_qcd_stat_down*' + pieces_split[1] 

                return plot_config


class JetFakeTauWsystShapeSystematic(SystematicShiftBase):
	
	def get_config(self, shift=0.0):
		plot_config = super(JetFakeTauWsystShapeSystematic, self).get_config(shift=shift)
		
		for index, weight in enumerate(plot_config.get("weights", [])):
			if not "data" in plot_config["nicks"][index]:
				pieces = [e+'_comb' if not e.startswith("_") else e for e in weight.split('_comb')]
                                pieces_split = pieces[1].split("*",1)
				if shift > 0.0:
					plot_config["weights"][index] =  pieces[0] + pieces_split[0] + '_w_syst_up*' + pieces_split[1]
				elif shift < 0.0:
					plot_config["weights"][index] =  pieces[0] + pieces_split[0] + '_w_syst_down*' + pieces_split[1]
		
		return plot_config


class JetFakeTauWstatShapeSystematic(SystematicShiftBase):

        def get_config(self, shift=0.0):
                plot_config = super(JetFakeTauWstatShapeSystematic, self).get_config(shift=shift)

                for index, weight in enumerate(plot_config.get("weights", [])):
                        if not "data" in plot_config["nicks"][index]:
                                pieces = [e+'_comb' if not e.startswith("_") else e for e in weight.split('_comb')]
                                pieces_split = pieces[1].split("*",1)
                                if shift > 0.0:
                                        plot_config["weights"][index] =  pieces[0] + pieces_split[0] + '_w_stat_up*' + pieces_split[1]
                                elif shift < 0.0:
                                        plot_config["weights"][index] =  pieces[0] + pieces_split[0] + '_w_stat_down*' + pieces_split[1]

                return plot_config


class JetFakeTauTTsystShapeSystematic(SystematicShiftBase):

        def get_config(self, shift=0.0):
                plot_config = super(JetFakeTauTTsystShapeSystematic, self).get_config(shift=shift)

                for index, weight in enumerate(plot_config.get("weights", [])):
                        if not "data" in plot_config["nicks"][index]:
                                pieces = [e+'_comb' if not e.startswith("_") else e for e in weight.split('_comb')]
                                pieces_split = pieces[1].split("*",1)
                                if shift > 0.0:
                                        plot_config["weights"][index] =  pieces[0] + pieces_split[0] + '_tt_syst_up*' + pieces_split[1]
                                elif shift < 0.0:
                                        plot_config["weights"][index] =  pieces[0] + pieces_split[0] + '_tt_syst_down*' + pieces_split[1]

                return plot_config


class JetFakeTauTTstatShapeSystematic(SystematicShiftBase):

        def get_config(self, shift=0.0):
                plot_config = super(JetFakeTauTTstatShapeSystematic, self).get_config(shift=shift)

                for index, weight in enumerate(plot_config.get("weights", [])):
                        if not "data" in plot_config["nicks"][index]:
                                pieces = [e+'_comb' if not e.startswith("_") else e for e in weight.split('_comb')]
                                pieces_split = pieces[1].split("*",1)
                                if shift > 0.0:
                                        plot_config["weights"][index] =  pieces[0] + pieces_split[0] + '_tt_stat_up*' + pieces_split[1]
                                elif shift < 0.0:
                                        plot_config["weights"][index] =  pieces[0] + pieces_split[0] + '_tt_stat_down*' + pieces_split[1]

                return plot_config


class MuFakeTauEsSystematic(SystematicShiftBase):
	
	def get_config(self, shift=0.0):
		plot_config = super(MuFakeTauEsSystematic, self).get_config(shift=shift)
		
		for index, folder in enumerate(plot_config.get("folders", [])):
			if not "data" in plot_config["nicks"][index]:
				if shift > 0.0:
					plot_config["folders"][index] = folder.split("/")[0] + "_muonEsUp/ntuple"
				elif shift < 0.0:
					plot_config["folders"][index] = folder.split("/")[0] + "_muonEsDown/ntuple"
		
		return plot_config


class TauEsSystematic(SystematicShiftBase):
	
	def get_config(self, shift=0.0):
		plot_config = super(TauEsSystematic, self).get_config(shift=shift)
		
		for index, folder in enumerate(plot_config.get("folders", [])):
			if not "data" in plot_config["nicks"][index]:
				if shift > 0.0:
					plot_config["folders"][index] = folder.replace("tauEsNom", "tauEsUp")
				elif shift < 0.0:
					plot_config["folders"][index] = folder.replace("tauEsNom", "tauEsDown")
		
		return plot_config


class EleEsSystematic(SystematicShiftBase):
	
	def get_config(self, shift=0.0):
		plot_config = super(EleEsSystematic, self).get_config(shift=shift)
		
		for index, folder in enumerate(plot_config.get("folders", [])):
			if not "data" in plot_config["nicks"][index]:
				if shift > 0.0:
					plot_config["folders"][index] = folder.split("/")[0] + "_eleEsUp/ntuple"
				elif shift < 0.0:
					plot_config["folders"][index] = folder.split("/")[0] + "_eleEsDown/ntuple"
		
		return plot_config


class MuonEsSystematic(SystematicShiftBase):
	
	def get_config(self, shift=0.0):
		plot_config = super(MuonEsSystematic, self).get_config(shift=shift)
		
		for index, folder in enumerate(plot_config.get("folders", [])):
			if not "data" in plot_config["nicks"][index]:
				if shift > 0.0:
					plot_config["folders"][index] = folder.split("/")[0] + "_muonEsUp/ntuple"
				elif shift < 0.0:
					plot_config["folders"][index] = folder.split("/")[0] + "_muonEsDown/ntuple"
		
		return plot_config


class MetResponseSystematic(SystematicShiftBase):
	
	def get_config(self, shift=0.0):
		plot_config = super(MetResponseSystematic, self).get_config(shift=shift)
		
		for index, folder in enumerate(plot_config.get("folders", [])):
			if not "data" in plot_config["nicks"][index]:
				if shift > 0.0:
					plot_config["folders"][index] = folder.split("/")[0] + "_metResponseUp/ntuple"
				elif shift < 0.0:
					plot_config["folders"][index] = folder.split("/")[0] + "_metResponseDown/ntuple"
		
		return plot_config


class MetResolutionSystematic(SystematicShiftBase):
	
	def get_config(self, shift=0.0):
		plot_config = super(MetResolutionSystematic, self).get_config(shift=shift)
		
		for index, folder in enumerate(plot_config.get("folders", [])):
			if not "data" in plot_config["nicks"][index]:
				if shift > 0.0:
					plot_config["folders"][index] = folder.split("/")[0] + "_metResolutionUp/ntuple"
				elif shift < 0.0:
					plot_config["folders"][index] = folder.split("/")[0] + "_metResolutionDown/ntuple"
		
		return plot_config


class TagEleEsSystematic(SystematicShiftBase):
	
	def get_config(self, shift=0.0):
		plot_config = super(TagEleEsSystematic, self).get_config(shift=shift)
		
		for index, folder in enumerate(plot_config.get("folders", [])):
			if not "data" in plot_config["nicks"][index]:
				if shift > 0.0:
					plot_config["folders"][index] = folder.replace("tagEleEsNom", "tagEleEsUp")
				elif shift < 0.0:
					plot_config["folders"][index] = folder.replace("tagEleEsNom", "tagEleEsDown")
		
		return plot_config


class ProbeTauEsSystematic(SystematicShiftBase):
	
	def get_config(self, shift=0.0):
		plot_config = super(ProbeTauEsSystematic, self).get_config(shift=shift)
		
		for index, folder in enumerate(plot_config.get("folders", [])):
			if not "data" in plot_config["nicks"][index]:
				if shift > 0.0:
					plot_config["folders"][index] = folder.replace("probeTauEsNom", "probeTauEsUp")
				elif shift < 0.0:
					plot_config["folders"][index] = folder.replace("probeTauEsNom", "probeTauEsDown")
		
		return plot_config


class ProbeEleEsSystematic(SystematicShiftBase):
	
	def get_config(self, shift=0.0):
		plot_config = super(ProbeEleEsSystematic, self).get_config(shift=shift)
		
		for index, folder in enumerate(plot_config.get("folders", [])):
			if not "data" in plot_config["nicks"][index]:
				if shift > 0.0:
					plot_config["folders"][index] = folder.replace("probeEleEsNom", "probeEleEsUp")
				elif shift < 0.0:
					plot_config["folders"][index] = folder.replace("probeEleEsNom", "probeEleEsDown")
		
		return plot_config


class MassResSystematic(SystematicShiftBase):
	
	def get_config(self, shift=0.0):
		plot_config = super(MassResSystematic, self).get_config(shift=shift)
		
		for index, expression in enumerate(plot_config.get("x_expressions", [])):
			if not "data" in plot_config["nicks"][index]:
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
					plot_config["folders"][index] = folder[0:3] + "bTagUp/ntuple"
				elif shift < 0.0:
					plot_config["folders"][index] = folder[0:3] + "bTagDown/ntuple"
		
		return plot_config

class BMistagSystematic(SystematicShiftBase):
	
	def get_config(self, shift=0.0):
		plot_config = super(BMistagSystematic, self).get_config(shift=shift)
		
		for index, folder in enumerate(plot_config.get("folders", [])):
			if not "Run201" in plot_config["files"][index]:
				if shift > 0.0:
					plot_config["folders"][index] = folder[0:3] + "bMistagUp/ntuple"
				elif shift < 0.0:
					plot_config["folders"][index] = folder[0:3] + "bMistagDown/ntuple"
		
		return plot_config
