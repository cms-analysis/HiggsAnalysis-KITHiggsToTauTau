
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import copy

import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.samples as samples


default_lumi = 71.52

class Samples(samples.SamplesBase):

	@staticmethod
	def cut_string(channel, exclude_cuts=None):
		if exclude_cuts is None:
			exclude_cuts = []
		
		cuts = {}
		cuts["blind"] = "{blind}"
		cuts["os"] = "((q_1*q_2)<0.0)"
		cuts["nobtag"] = "((nbtag<1)||(njetspt30<1))"
		
		if channel == "mt":
			cuts["mt"] = "(mt_1<30.0)"
			cuts["anti_lepton_tau_discriminators"] = "(againstElectronVLooseMVA5_2 > 0.5)*(againstMuonTight3_2 > 0.5)"
			cuts["extra_lepton_veto"] = "(extraelec_veto < 0.5)*(extramuon_veto < 0.5)*(dilepton_veto < 0.5)"
			cuts["iso_1"] = "(iso_1 < 0.1)"
			cuts["iso_2"] = "(byCombinedIsolationDeltaBetaCorrRaw3Hits_2 < 1.5)"
		elif channel == "et":
			cuts["mt"] = "(mt_1<30.0)"
			cuts["anti_lepton_tau_discriminators"] = "(againstElectronTightMVA5_2 > 0.5)*(againstMuonLoose3_2 > 0.5)"
			cuts["extra_lepton_veto"] = "(extraelec_veto < 0.5)*(extramuon_veto < 0.5)*(dilepton_veto < 0.5)"
			cuts["iso_1"] = "(iso_1 < 0.1)"
			cuts["iso_2"] = "(byCombinedIsolationDeltaBetaCorrRaw3Hits_2 < 1.5)"
		elif channel == "em":
			cuts["pzeta"] = "(pZetaMissVis > -20.0)"
			cuts["extra_lepton_veto"] = "(extraelec_veto < 0.5)*(extramuon_veto < 0.5)"
			cuts["iso_1"] = "(iso_1 < 0.15)"
			cuts["iso_2"] = "(iso_2 < 0.15)"
		elif channel == "tt":
			cuts["extra_lepton_veto"] = "(extraelec_veto < 0.5)*(extramuon_veto < 0.5)"
			cuts["iso_1"] = "(byCombinedIsolationDeltaBetaCorrRaw3Hits_1 < 1.5)"
			cuts["iso_2"] = "(byCombinedIsolationDeltaBetaCorrRaw3Hits_2 < 1.5)"
		else:
			log.fatal("No cut values implemented for channel \"%s\"!" % channel)
			sys.exit(1)
		
		cuts_list = [cut for (name, cut) in cuts.iteritems() if not name in exclude_cuts]
		if len(cuts_list) == 0:
			cuts_list.append("1.0")
		
		return "*".join(cuts_list)

	def __init__(self):
		super(Samples, self).__init__()
		
		self.period = "run2"
	
	def get_config(self, samples, channel, category, nick_suffix="", postfit_scales=None, blind_expression=None, **kwargs):
		config = super(Samples, self).get_config(samples, channel, category, nick_suffix=nick_suffix, postfit_scales=postfit_scales, **kwargs)
		
		# blinding (of data)
		config["weights"] = [weight.format(blind=self.expressions.replace_expressions("blind_"+str(blind_expression)) if "blind_"+str(blind_expression) in self.expressions.expressions_dict else "1.0") for weight in config["weights"]]
		
		# execute bin correction modules after possible background estimation modules
		config.setdefault("analysis_modules", []).sort(key=lambda module: module in ["BinErrorsOfEmptyBins", "CorrectNegativeBinContents"])
		
		return config
	
	def data(self, config, channel, category, weight, nick_suffix, exclude_cuts=None, **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []
		
		scale_factor = 1.0
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("data_obs", 1.0)
		
		if channel == "mt":
			Samples._add_input(
					config,
					"SingleMuon_Run2015?_*_13TeV_*AOD/*.root",
					channel+"_jecUnc_z_tauEs/ntuple",
					1.0,
					weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts),
					"data",
					nick_suffix=nick_suffix
			)
		elif channel == "et":
			Samples._add_input(
					config,
					"SingleElectron_Run2015?_*_13TeV_*AOD/*.root",
					channel+"_jecUnc_z_tauEs/ntuple",
					1.0,
					weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts),
					"data",
					nick_suffix=nick_suffix
			)
		elif channel == "em":
			Samples._add_input(
					config,
					"MuonEG_Run2015?_*_13TeV_*AOD/*.root",
					channel+"_jecUnc/ntuple",
					1.0,
					weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts),
					"data",
					nick_suffix=nick_suffix
			)
		elif channel == "tt":
			Samples._add_input(
					config,
					"Tau_Run2015?_*_13TeV_*AOD/*.root",
					channel+"_jecUnc_tauEs/ntuple",
					1.0,
					weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts),
					"data",
					nick_suffix=nick_suffix
			)
		else:
			log.error("Sample config (Data) currently not implemented for channel \"%s\"!" % channel)
		
		Samples._add_plot(config, "data", "E", "ELP", "data", nick_suffix)
		return config
	
	def ztt(self, config, channel, category, weight, nick_suffix, lumi=default_lumi, exclude_cuts=None, **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []
		
		scale_factor = 1.0
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("ZTT", 1.0)
		
		if channel in ["mt", "et", "tt", "em"]:
			Samples._add_input(
					config,
					"DYJetsToLL*_RunIISpring15*_*_13TeV_*AOD_amcatnlo*-pythia8/*.root",
					" ".join([channel+"_jecUncNom_"+dy+("_tauEsNom" if channel in ["mt", "et", "tt"] else "")+"/ntuple" for dy in (["ztt", "zttlep"] if channel in ["et", "mt"] else ["tt"])]),
					lumi,
					weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind"]),
					"ztt",
					nick_suffix=nick_suffix
			)
		else:
			log.error("Sample config (ZTT) currently not implemented for channel \"%s\"!" % channel)
		
		Samples._add_bin_corrections(config, "ztt", nick_suffix)
		Samples._add_plot(config, "bkg", "HIST", "F", "ztt", nick_suffix)
		
		return config
	
	def zll(self, config, channel, category, weight, nick_suffix, lumi=default_lumi, exclude_cuts=None, **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []
		
		scale_factor = lumi
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("ZL", 1.0)
		
		if channel in ["mt", "et", "tt", "em"]:
			Samples._add_input(
					config,
					"DYJetsToLL*_RunIISpring15*_*_13TeV_*AOD_amcatnlo*-pythia8/*.root",
					" ".join([channel+"_jecUncNom_"+dy+("_tauEsNom" if channel in ["mt", "et", "tt"] else "")+"/ntuple" for dy in (["zl", "zj", "zll"] if channel in ["et", "mt"] else ["ee", "mm"])]),
					lumi,
					weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind"]),
					"zll",
					nick_suffix=nick_suffix
			)
		else:
			log.error("Sample config (ZLL) currently not implemented for channel \"%s\"!" % channel)
		
		Samples._add_bin_corrections(config, "zll", nick_suffix)
		Samples._add_plot(config, "bkg", "HIST", "F", "zll", nick_suffix)
		return config
	

	def ttj(self, config, channel, category, weight, nick_suffix, lumi=default_lumi, exclude_cuts=None, **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []
		
		scale_factor = lumi
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("TTJ", 1.0)
		
		if channel in ["mt", "et", "tt"]:
			Samples._add_input(
					config,
					"TT_RunIISpring15*_*_13TeV_*AOD_powheg-pythia8/*.root",
					channel+"_jecUncNom"+("_z" if channel in ["mt", "et"] else "")+"_tauEs/ntuple",
					lumi,
					weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind"]),
					"ttj",
					nick_suffix=nick_suffix
			)
		elif channel == "em":
			Samples._add_input(
					config,
					"TT_RunIISpring15*_*_13TeV_*AOD_powheg-pythia8/*.root",
					channel+"_jecUncNom/ntuple",
					lumi,
					weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind"]),
					"ttj",
					nick_suffix=nick_suffix
			)
			Samples._add_input(
					config,
					"MuonEG_Run2015?_*_13TeV_*AOD/*.root",
					channel+"_jecUnc/ntuple",
					1.0,
					"eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "pzeta", "nobtag"]) + "*(pZetaMissVis < -20.0)",
					"noplot_ttj_data_control"
			)
			Samples._add_input(
					config,
					"DYJetsToLL*_RunIISpring15*_*_13TeV_*AOD_amcatnlo*-pythia8/*.root",
					channel+"_jecUncNom_tt/ntuple",
					lumi,
					"eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "pzeta", "nobtag"]) + "*(pZetaMissVis < -20.0)",
					"noplot_ztt_mc_ttj_control",
					nick_suffix=nick_suffix
			)
			Samples._add_input(
					config,
					"DYJetsToLL*_RunIISpring15*_*_13TeV_*AOD_amcatnlo*-pythia8/*.root",
					channel+"_jecUncNom_ee/ntuple " + channel+"_jecUncNom_mm/ntuple",
					lumi,
					"eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "pzeta", "nobtag"]) + "*(pZetaMissVis < -20.0)",
					"noplot_zll_ttj_control",
					nick_suffix=nick_suffix
			)
			Samples._add_input(
					config,
					"WJetsToLNu_RunIISpring15*_*_13TeV_*AOD_amcatnlo*-pythia8/*.root",
					channel+"_jecUncNom/ntuple",
					lumi,
					"eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "pzeta", "nobtag"]) + "*(pZetaMissVis < -20.0)",
					"noplot_wj_ttj_control",
					nick_suffix=nick_suffix
			)
			Samples._add_input(
					config,
					"WWTo*_RunIISpring15*_*_13TeV_*AOD_powheg/*.root WZTo?L*2Q_RunIISpring15*_*_13TeV_*AOD_amcatnlo*pythia8/*.root WZTo3LNu_RunIISpring15*_*_13TeV_*AOD_powheg-pythia8/*.root ZZTo*_RunIISpring15*_*_13TeV_*AOD_amcatnlo*pythia8/*.root ZZTo2L2Nu_RunIISpring15*_*_13TeV_*AOD_powheg*pythia8/*.root",
					channel+"_jecUncNom/ntuple",
					lumi,
					"eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "pzeta", "nobtag"]) + "*(pZetaMissVis < -20.0)",
					"noplot_vv_ttj_control",
					nick_suffix=nick_suffix
			)
			Samples._add_input(
					config,
					"TT_RunIISpring15*_*_13TeV_*AOD_powheg-pythia8/*.root",
					channel+"_jecUncNom/ntuple",
					lumi,
					weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind"]),
					"noplot_ttj_mc_signal",
					nick_suffix=nick_suffix
			)
			Samples._add_input(
					config,
					"TT_RunIISpring15*_*_13TeV_*AOD_powheg-pythia8/*.root",
					channel+"_jecUncNom/ntuple",
					lumi,
					"eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "pzeta", "nobtag"]) + "*(pZetaMissVis < -20.0)",
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
		else:
			log.error("Sample config (TTJ) currently not implemented for channel \"%s\"!" % channel)
		
		Samples._add_bin_corrections(config, "ttj", nick_suffix)
		Samples._add_plot(config, "bkg", "HIST", "F", "ttj", nick_suffix)
		return config

	def vv(self, config, channel, category, weight, nick_suffix, lumi=default_lumi, exclude_cuts=None, **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []
		
		scale_factor = lumi
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("Dibosons", 1.0)
		
		if channel in ["mt", "et", "em", "tt"]:
			Samples._add_input(
					config,
					"WWTo*_RunIISpring15*_*_13TeV_*AOD_powheg/*.root WZTo?L*2Q_RunIISpring15*_*_13TeV_*AOD_amcatnlo*pythia8/*.root WZTo3LNu_RunIISpring15*_*_13TeV_*AOD_powheg-pythia8/*.root ZZTo*_RunIISpring15*_*_13TeV_*AOD_amcatnlo*pythia8/*.root ZZTo2L2Nu_RunIISpring15*_*_13TeV_*AOD_powheg*pythia8/*.root",
					channel+"_jecUncNom"+("_z" if channel in ["et", "mt"] else "")+("_tauEs" if channel in ["mt", "et", "tt"] else "")+"/ntuple",
					lumi,
					weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind"]),
					"vv",
					nick_suffix=nick_suffix
			)
		else:
			log.error("Sample config (VV) currently not implemented for channel \"%s\"!" % channel)
		
		Samples._add_bin_corrections(config, "vv", nick_suffix)
		Samples._add_plot(config, "bkg", "HIST", "F", "vv", nick_suffix)
		return config
	
	def wj(self, config, channel, category, weight, nick_suffix, lumi=default_lumi, exclude_cuts=None, **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []
		
		scale_factor = lumi
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("WJets", 1.0)
		
		if channel in ["mt", "et"]:
			shape_weight = weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind"])
			if (not category is None) and (category != ""):
				# relaxed isolation
				shape_weight = weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "iso_2"]) + "*(byCombinedIsolationDeltaBetaCorrRaw3Hits_2<10.0)"
			
			Samples._add_input(
					config,
					"WJetsToLNu_RunIISpring15*_*_13TeV_*AOD_amcatnlo*-pythia8/*.root",
					channel+"_jecUncNom_z_tauEs/ntuple",
					lumi,
					shape_weight,
					"wj",
					nick_suffix=nick_suffix
			)
			Samples._add_input(
					config,
					"SingleMuon_Run2015?_*_13TeV_*AOD/*.root" if channel == "mt" else "SingleElectron_Run2015?_*_13TeV_*AOD/*root",
					channel+"_jecUnc_z_tauEs/ntuple",
					1.0,
					"eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "mt"]) + "*(mt_1>70.0)",
					"noplot_wj_data_control"
			)
			Samples._add_input(
					config,
					"DYJetsToLL*_RunIISpring15*_*_13TeV_*AOD_amcatnlo*-pythia8/*.root",
					channel+"_jecUncNom_ztt_tauEsNom/ntuple " + channel + "_jecUncNom_zttlep_tauEsNom/ntuple",
					lumi,
					"eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "mt"]) + "*(mt_1>70.0)",
					"noplot_ztt_mc_wj_control",
					nick_suffix=nick_suffix
			)
			Samples._add_input(
					config,
					"DYJetsToLL*_RunIISpring15*_*_13TeV_*AOD_amcatnlo*-pythia8/*.root",
					channel+"_jecUncNom_zl_tauEsNom/ntuple " + channel+"_jecUncNom_zj_tauEsNom/ntuple " + channel+"_jecUncNom_zll_tauEsNom/ntuple",
					lumi,
					"eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "mt"]) + "*(mt_1>70.0)",
					"noplot_zll_wj_control",
					nick_suffix=nick_suffix
			)
			Samples._add_input(
					config,
					"TT_RunIISpring15*_*_13TeV_*AOD_powheg-pythia8/*.root",
					channel+"_jecUncNom_z_tauEs/ntuple",
					lumi,
					"eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "mt"]) + "*(mt_1>70.0)",
					"noplot_ttj_wj_control",
					nick_suffix=nick_suffix
			)
			Samples._add_input(
					config,
					"WWTo*_RunIISpring15*_*_13TeV_*AOD_powheg/*.root WZTo?L*2Q_RunIISpring15*_*_13TeV_*AOD_amcatnlo*pythia8/*.root WZTo3LNu_RunIISpring15*_*_13TeV_*AOD_powheg-pythia8/*.root ZZTo*_RunIISpring15*_*_13TeV_*AOD_amcatnlo*pythia8/*.root ZZTo2L2Nu_RunIISpring15*_*_13TeV_*AOD_powheg*pythia8/*.root",
					channel+"_jecUncNom_z_tauEs/ntuple",
					lumi,
					"eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "mt"]) + "*(mt_1>70.0)",
					"noplot_vv_wj_control",
					nick_suffix=nick_suffix
			)
			Samples._add_input(
					config,
					"WJetsToLNu_RunIISpring15*_*_13TeV_*AOD_amcatnlo*-pythia8/*.root",
					channel+"_jecUncNom_z_tauEs/ntuple",
					lumi,
					weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind"]),
					"noplot_wj_mc_signal",
					nick_suffix=nick_suffix
			)
			Samples._add_input(
					config,
					"WJetsToLNu_RunIISpring15*_*_13TeV_*AOD_amcatnlo*-pythia8/*.root",
					channel+"_jecUncNom_z_tauEs/ntuple",
					lumi,
					"eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "mt"]) + "*(mt_1>70.0)",
					"noplot_wj_mc_control",
					nick_suffix=nick_suffix
			)

			if not "EstimateWjets" in config.get("analysis_modules", []):
				config.setdefault("analysis_modules", []).append("EstimateWjets")
			config.setdefault("wjets_from_mc", []).append(False)
			config.setdefault("wjets_shape_nicks", []).append("wj"+nick_suffix)
			config.setdefault("wjets_data_control_nicks", []).append("noplot_wj_data_control"+nick_suffix)
			config.setdefault("wjets_data_substract_nicks", []).append(" ".join([nick+nick_suffix for nick in "noplot_ztt_mc_wj_control noplot_zll_wj_control noplot_ttj_wj_control noplot_vv_wj_control".split()]))
			config.setdefault("wjets_mc_signal_nicks", []).append("noplot_wj_mc_signal"+nick_suffix)
			config.setdefault("wjets_mc_control_nicks", []).append("noplot_wj_mc_control"+nick_suffix)

		elif channel in ["em", "tt"]:
			Samples._add_input(
					config,
					"WJetsToLNu_RunIISpring15*_*_13TeV_*AOD_amcatnlo*-pythia8/*.root",
					channel+"_jecUncNom"+("_tauEs" if channel == "tt" else "")+"/ntuple",
					lumi,
					weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind"]),
					"wj",
					nick_suffix=nick_suffix
			)
		else:	
			log.error("Sample config (WJets) currently not implemented for channel \"%s\"!" % channel)
		
		if not kwargs.get("no_plot", False):
			Samples._add_bin_corrections(config, "wj", nick_suffix)
			Samples._add_plot(config, "bkg", "HIST", "F", "wj", nick_suffix)
		return config

	def qcd(self, config, channel, category, weight, nick_suffix, lumi=default_lumi, exclude_cuts=None, **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []
		
		scale_factor = 1.0
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("QCD", 1.0)
		
		if channel in ["et", "mt", "em"]:

			# WJets for QCD estimate
			Samples._add_input(
					config,
					"WJetsToLNu_RunIISpring15*_*_13TeV_*AOD_amcatnlo*-pythia8/*.root",
					channel+"_jecUncNom"+("_z" if channel in ["et", "mt"] else "")+("_tauEs" if channel in ["mt", "et", "tt"] else "")+"/ntuple",
					lumi,
					"eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "os"]) + "*((q_1*q_2)>0.0)",
					"noplot_wj_ss",
					nick_suffix=nick_suffix
			)
			
			if channel in ["mt", "et"]:
				Samples._add_input(
						config,
						"SingleMuon_Run2015?_*_13TeV_*AOD/*.root" if channel == "mt" else ("SingleElectron_Run2015?_*_13TeV_*AOD/*root" if channel == "et" else "MuonEG_Run2015?_*_13TeV_*AOD/*.root"),
						channel+"_jecUnc"+("_z" if channel in ["et", "mt"] else "")+"_tauEs/ntuple",
						1.0,
						"eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "os", "mt"]) + "*((q_1*q_2)>0.0)*(mt_1>70.0)",
						"noplot_wj_ss_data_control",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						"DYJetsToLL*_RunIISpring15*_*_13TeV_*AOD_amcatnlo*-pythia8/*.root",
						" ".join([channel+"_jecUncNom_"+dy+"_tauEsNom/ntuple" for dy in (["ztt", "zttlep"] if channel in ["et", "mt"] else ["tt"])]),
						lumi,
						"eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "os", "mt"]) + "*((q_1*q_2)>0.0)*(mt_1>70.0)",
						"noplot_ztt_ss_mc_wj_control",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						"DYJetsToLL*_RunIISpring15*_*_13TeV_*AOD_amcatnlo*-pythia8/*.root",
						" ".join([channel+"_jecUncNom_"+dy+"_tauEsNom/ntuple" for dy in (["zl", "zj", "zll"] if channel in ["et", "mt"] else ["ee", "mm"])]),
						lumi,
						"eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "os", "mt"]) + "*((q_1*q_2)>0.0)*(mt_1>70.0)",
						"noplot_zll_ss_wj_control",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						"TT_RunIISpring15*_*_13TeV_*AOD_powheg-pythia8/*.root",
						channel+"_jecUncNom"+("_z" if channel in ["et", "mt"] else "")+"_tauEs/ntuple",
						lumi,
						"eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "os", "mt"]) + "*((q_1*q_2)>0.0)*(mt_1>70.0)",
						"noplot_ttj_ss_wj_control",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						"WWTo*_RunIISpring15*_*_13TeV_*AOD_powheg/*.root WZTo?L*2Q_RunIISpring15*_*_13TeV_*AOD_amcatnlo*pythia8/*.root WZTo3LNu_RunIISpring15*_*_13TeV_*AOD_powheg-pythia8/*.root ZZTo*_RunIISpring15*_*_13TeV_*AOD_amcatnlo*pythia8/*.root ZZTo2L2Nu_RunIISpring15*_*_13TeV_*AOD_powheg*pythia8/*.root",
						channel+"_jecUncNom"+("_z" if channel in ["et", "mt"] else "")+"_tauEs/ntuple",
						lumi,
						"eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "os", "mt"]) + "*((q_1*q_2)>0.0)*(mt_1>70.0)",
						"noplot_vv_ss_wj_control",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						"WJetsToLNu_RunIISpring15*_*_13TeV_*AOD_amcatnlo*-pythia8/*.root",
						channel+"_jecUncNom"+("_z" if channel in ["et", "mt"] else "")+"_tauEs/ntuple",
						lumi,
						"eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "os"]) + "*((q_1*q_2)>0.0)",
						"noplot_wj_ss_mc_signal",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						"WJetsToLNu_RunIISpring15*_*_13TeV_*AOD_amcatnlo*-pythia8/*.root",
						channel+"_jecUncNom"+("_z" if channel in ["et", "mt"] else "")+"_tauEs/ntuple",
						lumi,
						"eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "os", "mt"]) + "*((q_1*q_2)>0.0)*(mt_1>70.0)",
						"noplot_wj_ss_mc_control",
						nick_suffix=nick_suffix
				)
			
				if not "EstimateWjets" in config.get("analysis_modules", []):
					config.setdefault("analysis_modules", []).append("EstimateWjets")
				config.setdefault("wjets_from_mc", []).append(False)
				config.setdefault("wjets_shape_nicks", []).append("noplot_wj_ss"+nick_suffix)
				config.setdefault("wjets_data_control_nicks", []).append("noplot_wj_ss_data_control"+nick_suffix)
				config.setdefault("wjets_data_substract_nicks", []).append(" ".join([nick+nick_suffix for nick in "noplot_ztt_ss_mc_wj_control noplot_zll_ss_wj_control noplot_ttj_ss_wj_control noplot_vv_ss_wj_control".split()]))
				config.setdefault("wjets_mc_signal_nicks", []).append("noplot_wj_ss_mc_signal"+nick_suffix)
				config.setdefault("wjets_mc_control_nicks", []).append("noplot_wj_ss_mc_control"+nick_suffix)
			
			# QCD
			shape_weight = weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "os"]) + "*((q_1*q_2)>0.0)"
			if (not category is None) and (category != ""):
				# relaxed/inverted isolation
				if channel in ["et", "mt"]:
					shape_weight = weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "os", "iso_2"]) + "*((q_1*q_2)>0.0)"+"*(byCombinedIsolationDeltaBetaCorrRaw3Hits_2<10.0)"
				else:
					shape_weight = weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "os", "iso_1", "iso_2"]) + "*((q_1*q_2)>0.0)"
			
			Samples._add_input(
					config,
					"SingleMuon_Run2015?_*_13TeV_*AOD/*.root" if channel == "mt" else ("SingleElectron_Run2015?_*_13TeV_*AOD/*root" if channel == "et" else "MuonEG_Run2015?_*_13TeV_*AOD/*.root"),
					channel+"_jecUnc"+("_z" if channel in ["et", "mt"] else "")+("_tauEs" if channel in ["mt", "et"] else "")+"/ntuple",
					1.0,
					shape_weight,
					"qcd",
					nick_suffix=nick_suffix
			)
			Samples._add_input(
					config,
					"SingleMuon_Run2015?_*_13TeV_*AOD/*.root" if channel == "mt" else ("SingleElectron_Run2015?_*_13TeV_*AOD/*root" if channel == "et" else "MuonEG_Run2015?_*_13TeV_*AOD/*.root"),
					channel+"_jecUnc"+("_z" if channel in ["et", "mt"] else "")+("_tauEs" if channel in ["mt", "et"] else "")+"/ntuple",
					1.0,
					weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "os"]) + "*((q_1*q_2)>0.0)",
					"noplot_data_qcd_yield",
					nick_suffix=nick_suffix
			)
			Samples._add_input(
					config,
					"SingleMuon_Run2015?_*_13TeV_*AOD/*.root" if channel == "mt" else ("SingleElectron_Run2015?_*_13TeV_*AOD/*root" if channel == "et" else "MuonEG_Run2015?_*_13TeV_*AOD/*.root"),
					channel+"_jecUnc"+("_z" if channel in ["et", "mt"] else "")+("_tauEs" if channel in ["mt", "et"] else "")+"/ntuple",
					1.0,
					"eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "os"]) + "*((q_1*q_2)>0.0)",
					"noplot_data_qcd_control",
					nick_suffix=nick_suffix
			)
			Samples._add_input(
					config,
					"DYJetsToLL*_RunIISpring15*_*_13TeV_*AOD_amcatnlo*-pythia8/*.root",
					" ".join([channel+"_jecUncNom_"+dy+("_tauEsNom" if channel in ["mt", "et"] else "")+"/ntuple" for dy in (["ztt", "zttlep"] if channel in ["et", "mt"] else ["tt"])]),
					lumi,
					"eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "os"]) + "*((q_1*q_2)>0.0)",
					"noplot_ztt_mc_qcd_control",
					nick_suffix=nick_suffix
			)
			Samples._add_input(
					config,
					"DYJetsToLL*_RunIISpring15*_*_13TeV_*AOD_amcatnlo*-pythia8/*.root",
					" ".join([channel+"_jecUncNom_"+dy+("_tauEsNom" if channel in ["mt", "et"] else "")+"/ntuple" for dy in (["zl", "zj", "zll"] if channel in ["et", "mt"] else ["ee", "mm"])]),
					lumi,
					"eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "os"]) + "*((q_1*q_2)>0.0)",
					"noplot_zll_qcd_control",
					nick_suffix=nick_suffix
			)
			Samples._add_input(
					config,
					"TT_RunIISpring15*_*_13TeV_*AOD_powheg-pythia8/*.root",
					channel+"_jecUncNom"+("_z" if channel in ["et", "mt"] else "")+("_tauEs" if channel in ["mt", "et"] else "")+"/ntuple",
					lumi,
					"eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "os"]) + "*((q_1*q_2)>0.0)",
					"noplot_ttj_qcd_control",
					nick_suffix=nick_suffix
			)
			Samples._add_input(
					config,
					"WWTo*_RunIISpring15*_*_13TeV_*AOD_powheg/*.root WZTo?L*2Q_RunIISpring15*_*_13TeV_*AOD_amcatnlo*pythia8/*.root WZTo3LNu_RunIISpring15*_*_13TeV_*AOD_powheg-pythia8/*.root ZZTo*_RunIISpring15*_*_13TeV_*AOD_amcatnlo*pythia8/*.root ZZTo2L2Nu_RunIISpring15*_*_13TeV_*AOD_powheg*pythia8/*.root",
					channel+"_jecUncNom"+("_z" if channel in ["et", "mt"] else "")+("_tauEs" if channel in ["mt", "et"] else "")+"/ntuple",
					lumi,
					"eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "os"]) + "*((q_1*q_2)>0.0)",
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
		
		elif channel == "tt":
			Samples._add_input(
					config,
					"Tau_Run2015?_*_13TeV_*AOD/*.root",
					channel+"_jecUnc_tauEs/ntuple",
					1.0,
					weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "os"]) + "*((q_1*q_2)>0.0)",
					"qcd",
					nick_suffix=nick_suffix
			)
		else:
			log.error("Sample config (QCD) currently not implemented for channel \"%s\"!" % channel)
		
		if not kwargs.get("no_plot", False):
			Samples._add_bin_corrections(config, "qcd", nick_suffix)
			Samples._add_plot(config, "bkg", "HIST", "F", "qcd", nick_suffix)
		return config
	
	def htt(self, config, channel, category, weight, nick_suffix, higgs_masses, normalise_signal_to_one_pb=False, lumi=default_lumi, exclude_cuts=None, **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []
		
		config = self.ggh(config, channel, category, weight, nick_suffix+"_noplot", higgs_masses,
		                  normalise_signal_to_one_pb, lumi=lumi, exclude_cuts=exclude_cuts, no_plot=True, **kwargs)
		config = self.qqh(config, channel, category, weight, nick_suffix+"_noplot", higgs_masses,
		                  normalise_signal_to_one_pb, lumi=lumi, exclude_cuts=exclude_cuts, no_plot=True, **kwargs)
		config = self.vh(config, channel, category, weight, nick_suffix+"_noplot", higgs_masses,
		                 normalise_signal_to_one_pb, lumi=lumi, exclude_cuts=exclude_cuts, no_plot=True, **kwargs)
		
		for mass in higgs_masses:
			if not "AddHistograms" in config.get("analysis_modules", []):
				config.setdefault("analysis_modules", []).append("AddHistograms")
			config.setdefault("histogram_nicks", []).append(" ".join([sample+str(mass)+nick_suffix+"_noplot" for sample in ["ggh", "qqh", "vh"]]))
			config.setdefault("sum_result_nicks", []).append("htt"+str(mass)+nick_suffix)
			
			Samples._add_bin_corrections(config, "htt"+str(mass), nick_suffix)
			Samples._add_plot(config, "sig", "LINE", "L", "htt"+str(mass), nick_suffix)
		return config
	
	def ggh(self, config, channel, category, weight, nick_suffix, higgs_masses, normalise_signal_to_one_pb=False, lumi=default_lumi, exclude_cuts=None, **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []
		
		scale_factor = lumi
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("ggh", 1.0)
		
		for mass in higgs_masses:
			if channel in ["tt", "et", "mt", "em", "mm"]:
				Samples._add_input(
						config,
						"GluGluHToTauTauM{mass}_RunIISpring15DR74_Asympt25ns_13TeV_*AOD_powhegpythia8/*.root".format(mass=str(mass)),
						channel+"_jecUncNom"+("_z" if channel in ["et", "mt"] else "")+("_tauEsNom" if channel in ["mt", "et", "tt"] else "")+"/ntuple",
						lumi,
						weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind"]),
						"ggh%s" % str(mass),
						nick_suffix=nick_suffix
				)
			else:
				log.error("Sample config (ggH%s) currently not implemented for channel \"%s\"!" % (str(mass), channel))
			
			if not kwargs.get("no_plot", False):
				Samples._add_bin_corrections(config, "ggh"+str(mass), nick_suffix)
				Samples._add_plot(config, "sig", "LINE", "L", "ggh"+str(mass), nick_suffix)
		return config
	
	def qqh(self, config, channel, category, weight, nick_suffix, higgs_masses, normalise_signal_to_one_pb=False, lumi=default_lumi, exclude_cuts=None, **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []
		
		scale_factor = lumi
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("qqH", 1.0)
		
		for mass in higgs_masses:
			if channel in ["tt", "et", "mt", "em", "mm"]:
				Samples._add_input(
						config,
						"VBFHToTauTauM{mass}_RunIISpring15DR74_Asympt25ns_13TeV_*AOD_powhegpythia8/*.root".format(mass=str(mass)),
						channel+"_jecUncNom"+("_z" if channel in ["et", "mt"] else "")+("_tauEsNom" if channel in ["mt", "et", "tt"] else "")+"/ntuple",
						lumi,
						weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind"]),
						"qqh%s" % str(mass),
						nick_suffix=nick_suffix
			)
			else:
				log.error("Sample config (VBF%s) currently not implemented for channel \"%s\"!" % (str(mass), channel))
			
			if not kwargs.get("no_plot", False):
				Samples._add_bin_corrections(config, "qqh"+str(mass), nick_suffix)
				Samples._add_plot(config, "sig", "LINE", "L", "qqh"+str(mass), nick_suffix)
		return config
	
	def vh(self, config, channel, category, weight, nick_suffix, higgs_masses, normalise_signal_to_one_pb=False, lumi=default_lumi, exclude_cuts=None, **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []
		
		config = self.wh(config, channel, category, weight, nick_suffix+"_noplot", higgs_masses,
		                 normalise_signal_to_one_pb, lumi=lumi, exclude_cuts=exclude_cuts, no_plot=True, **kwargs)
		config = self.zh(config, channel, category, weight, nick_suffix+"_noplot", higgs_masses,
		                 normalise_signal_to_one_pb, lumi=lumi, exclude_cuts=exclude_cuts, no_plot=True, **kwargs)
		
		for mass in higgs_masses:
			if not "AddHistograms" in config.get("analysis_modules", []):
				config.setdefault("analysis_modules", []).append("AddHistograms")
			config.setdefault("histogram_nicks", []).append(" ".join([sample+str(mass)+nick_suffix+"_noplot" for sample in ["wh", "zh"]]))
			config.setdefault("sum_result_nicks", []).append("vh"+str(mass)+nick_suffix)
			
			Samples._add_bin_corrections(config, "vh"+str(mass), nick_suffix)
			Samples._add_plot(config, "sig", "LINE", "L", "vh"+str(mass), nick_suffix)
		return config
	
	def wh(self, config, channel, category, weight, nick_suffix, higgs_masses, normalise_signal_to_one_pb=False, lumi=default_lumi, exclude_cuts=None, **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []
		
		scale_factor = lumi
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("WH", 1.0)
		
		for mass in higgs_masses:
			if channel in ["tt", "et", "mt", "em", "mm"]:
				Samples._add_input(
						config,
						"WminusHToTauTauM{mass}_RunIISpring15DR74_Asympt25ns_13TeV_*AOD_powhegpythia8/*.root".format(mass=str(mass)),
						channel+"_jecUncNom"+("_z" if channel in ["et", "mt"] else "")+("_tauEsNom" if channel in ["mt", "et", "tt"] else "")+"/ntuple",
						lumi,
						weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind"]),
						"wmh%s" % str(mass),
						nick_suffix=nick_suffix+"_noplot"
				)
				Samples._add_input(
						config,
						"WplusHToTauTauM{mass}_RunIISpring15DR74_Asympt25ns_13TeV_*AOD_powhegpythia8/*.root".format(mass=str(mass)),
						channel+"_jecUncNom"+("_z" if channel in ["et", "mt"] else "")+("_tauEsNom" if channel in ["mt", "et", "tt"] else "")+"/ntuple",
						lumi,
						weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind"]),
						"wph%s" % str(mass),
						nick_suffix=nick_suffix+"_noplot"
				)
				
				if not "AddHistograms" in config.get("analysis_modules", []):
					config.setdefault("analysis_modules", []).append("AddHistograms")
				config.setdefault("histogram_nicks", []).append(" ".join([sample+str(mass)+nick_suffix+"_noplot" for sample in ["wmh", "wph"]]))
				config.setdefault("sum_result_nicks", []).append("wh"+str(mass)+nick_suffix)
			
			else:
				log.error("Sample config (WH%s) currently not implemented for channel \"%s\"!" % (str(mass), channel))
			
			if not kwargs.get("no_plot", False):
				Samples._add_bin_corrections(config, "wh"+str(mass), nick_suffix)
				Samples._add_plot(config, "sig", "LINE", "L", "wh"+str(mass), nick_suffix)
		return config
	
	def zh(self, config, channel, category, weight, nick_suffix, higgs_masses, normalise_signal_to_one_pb=False, lumi=default_lumi, exclude_cuts=None, **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []
		
		scale_factor = lumi
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("ZH", 1.0)
		
		for mass in higgs_masses:
			if channel in ["tt", "et", "mt", "em", "mm"]:
				Samples._add_input(
						config,
						"ZHToTauTauM{mass}_RunIISpring15DR74_Asympt25ns_13TeV_*AOD_powhegpythia8/*.root".format(mass=str(mass)),
						channel+"_jecUncNom"+("_z" if channel in ["et", "mt"] else "")+("_tauEsNom" if channel in ["mt", "et", "tt"] else "")+"/ntuple",
						lumi,
						weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind"]),
						"zh%s" % str(mass),
						nick_suffix=nick_suffix
				)
			
			else:
				log.error("Sample config (ZH%s) currently not implemented for channel \"%s\"!" % (str(mass), channel))
			
			if not kwargs.get("no_plot", False):
				Samples._add_bin_corrections(config, "zh"+str(mass), nick_suffix)
				Samples._add_plot(config, "sig", "LINE", "L", "zh"+str(mass), nick_suffix)
		return config

