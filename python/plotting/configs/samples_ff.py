# This file defines samples used for the Fake Factor datacards

import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.samples_run2_2015 as samples
default_lumi = 2.301*1000.0

class Samples(samples.Samples):

	def ewk(self, config, channel, category, weight, nick_suffix, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", fakefactor_method=None, **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []

		scale_factor = lumi
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("Dibosons", 1.0)

		data_weight = "(1.0)*"
		mc_weight = "(1.0)*"
		if kwargs.get("project_to_lumi", False):
			data_weight = "({projection})*".format(projection=kwargs["project_to_lumi"]) + data_weight
			mc_weight = "({projection})*".format(projection=kwargs["project_to_lumi"]) + mc_weight
		if kwargs.get("cut_mc_only", False):
			mc_weight = "({mc_cut})*".format(mc_cut=kwargs["cut_mc_only"]) + mc_weight
		if kwargs.get("scale_mc_only", False):
			mc_weight = "({mc_scale})*".format(mc_scale=kwargs["scale_mc_only"]) + mc_weight

		if channel in ["mt", "et"]:
			Samples._add_input(
					config,
					"TT_RunIIFall15*_*_13TeV_*AOD_powheg-pythia8/*.root ST*_RunIIFall15*_*_13TeV_*AOD_powheg-pythia8/*root WW*_RunIIFall15*_*_13TeV_*AOD_*/*.root WZ*_RunIIFall15*_*_13TeV_*AOD_*/*.root ZZ*_RunIIFall15*_*_13TeV_*AOD_*/*.root VV*_RunIIFall15*_*_13TeV_*AOD_*/*.root",
					channel+"_jecUncNom_tauEsNom/ntuple",
					lumi,
					mc_weight+weight+"*eventWeight*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind"], cut_type=cut_type),
					"ewk",
					nick_suffix=nick_suffix
			)
		else:
			log.error("Sample config (EWK) currently not implemented for channel \"%s\"!" % channel)
	
		if channel in ["mt", "et"] and fakefactor_method == "standard":
			config["weights"][config["nicks"].index("ewk")] = config["weights"][config["nicks"].index("ewk")]  + "*(gen_match_2 != 6)"
		if channel in ["mt", "et"] and fakefactor_method == "comparison":
			config["weights"][config["nicks"].index("ewk")] = config["weights"][config["nicks"].index("ewk")]  + "*(gen_match_2 == 6)"
	
		Samples._add_plot(config, "bkg", "HIST", "F", "ewk", nick_suffix)
		return config

	def vvt(self, config, channel, category, weight, nick_suffix, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", fakefactor_method=None, **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []

		scale_factor = lumi
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("Dibosons", 1.0)

		mc_weight = "(1.0)*"

		if channel in ["mt", "et"]:
			Samples._add_input(
					config,
					"ST*_RunIIFall15*_*_13TeV_*AOD_powheg-pythia8/*root WW*_RunIIFall15*_*_13TeV_*AOD_*/*.root WZ*_RunIIFall15*_*_13TeV_*AOD_*/*.root ZZ*_RunIIFall15*_*_13TeV_*AOD_*/*.root VV*_RunIIFall15*_*_13TeV_*AOD_*/*.root",
					channel+"_jecUncNom_tauEsNom/ntuple",
					lumi,
					mc_weight+weight+"*eventWeight*(gen_match_2 == 5)*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind"], cut_type=cut_type),
					"vvt",
					nick_suffix=nick_suffix
			)
		else:
			log.error("Sample config (vvt) currently not implemented for channel \"%s\"!" % channel)
	
		Samples._add_plot(config, "bkg", "HIST", "F", "vvt", nick_suffix)
		return config

	def ttjt(self, config, channel, category, weight, nick_suffix, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", fakefactor_method=None, **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []

		scale_factor = lumi
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("Dibosons", 1.0)

		mc_weight = "(1.0)*"

		if channel in ["mt", "et"]:
			Samples._add_input(
					config,
					"TT_RunIIFall15*_*_13TeV_*AOD_powheg-pythia8/*.root",
					channel+"_jecUncNom_tauEsNom/ntuple",
					lumi,
					mc_weight+weight+"*eventWeight*(gen_match_2 == 5)*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind"], cut_type=cut_type),
					"ttjt",
					nick_suffix=nick_suffix
			)
		else:
			log.error("Sample config (ttjt) currently not implemented for channel \"%s\"!" % channel)
	
		Samples._add_plot(config, "bkg", "HIST", "F", "ttjt", nick_suffix)
		return config

	def wjt(self, config, channel, category, weight, nick_suffix, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", fakefactor_method=None, **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []

		scale_factor = lumi
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("Dibosons", 1.0)

		mc_weight = "(1.0)*"

		if channel in ["mt", "et"]:
			Samples._add_input(
					config,
					"W*JetsToLNu_RunIIFall15*_*_13TeV_*AOD_*/*.root",
					channel+"_jecUncNom_tauEsNom/ntuple",
					lumi,
					mc_weight+weight+"*eventWeight*(gen_match_2 == 5)*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind"], cut_type=cut_type),
					"wjt",
					nick_suffix=nick_suffix
			)
		else:
			log.error("Sample config (wjt) currently not implemented for channel \"%s\"!" % channel)
	
		Samples._add_plot(config, "bkg", "HIST", "F", "wjt", nick_suffix)
		return config

	def vvl(self, config, channel, category, weight, nick_suffix, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", fakefactor_method=None, **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []

		scale_factor = lumi
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("Dibosons", 1.0)

		mc_weight = "(1.0)*"

		if channel in ["mt", "et"]:
			Samples._add_input(
					config,
					"ST*_RunIIFall15*_*_13TeV_*AOD_powheg-pythia8/*root WW*_RunIIFall15*_*_13TeV_*AOD_*/*.root WZ*_RunIIFall15*_*_13TeV_*AOD_*/*.root ZZ*_RunIIFall15*_*_13TeV_*AOD_*/*.root VV*_RunIIFall15*_*_13TeV_*AOD_*/*.root",
					channel+"_jecUncNom_tauEsNom/ntuple",
					lumi,
					mc_weight+weight+"*eventWeight*(gen_match_2 <= 4)*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind"], cut_type=cut_type),
					"vvl",
					nick_suffix=nick_suffix
			)
		else:
			log.error("Sample config (vvl) currently not implemented for channel \"%s\"!" % channel)
	
		Samples._add_plot(config, "bkg", "HIST", "F", "vvl", nick_suffix)
		return config

	def ttjl(self, config, channel, category, weight, nick_suffix, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", fakefactor_method=None, **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []

		scale_factor = lumi
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("Dibosons", 1.0)

		mc_weight = "(1.0)*"

		if channel in ["mt", "et"]:
			Samples._add_input(
					config,
					"TT_RunIIFall15*_*_13TeV_*AOD_powheg-pythia8/*.root",
					channel+"_jecUncNom_tauEsNom/ntuple",
					lumi,
					mc_weight+weight+"*eventWeight*(gen_match_2 <= 4)*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind"], cut_type=cut_type),
					"ttjl",
					nick_suffix=nick_suffix
			)
		else:
			log.error("Sample config (ttjl) currently not implemented for channel \"%s\"!" % channel)
	
		Samples._add_plot(config, "bkg", "HIST", "F", "ttjl", nick_suffix)
		return config

	def wjl(self, config, channel, category, weight, nick_suffix, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", fakefactor_method=None, **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []

		scale_factor = lumi
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("Dibosons", 1.0)

		mc_weight = "(1.0)*"

		if channel in ["mt", "et"]:
			Samples._add_input(
					config,
					"W*JetsToLNu_RunIIFall15*_*_13TeV_*AOD_*/*.root",
					channel+"_jecUncNom_tauEsNom/ntuple",
					lumi,
					mc_weight+weight+"*eventWeight*(gen_match_2 <= 4)*" + Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind"], cut_type=cut_type),
					"wjl",
					nick_suffix=nick_suffix
			)
		else:
			log.error("Sample config (wjl) currently not implemented for channel \"%s\"!" % channel)
	
		Samples._add_plot(config, "bkg", "HIST", "F", "wjl", nick_suffix)
		return config
