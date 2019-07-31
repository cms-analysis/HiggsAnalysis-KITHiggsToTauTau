
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)


import pprint
import copy
import sys

import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.samples_run2_2016 as samples
from Kappa.Skimming.registerDatasetHelper import get_nick_list

from functools import wraps, partial


from Artus.Utility.tools import make_multiplication, split_multiplication, clean_multiplication
energy = 13
default_lumi =  41.53*1000.0
#41.37

class partialmethod(partial):
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return partial(self.func, instance,
                       *(self.args or ()), **(self.keywords or {}))



class Samples(samples.Samples):
	# constants for all plots
	data_format = "MINIAOD"
	mc_campaign = "RunIIFall17MiniAODv2"
	
	# For 2017 v2 MC samples, the npartons=4 part is removedfor now since the skimming is not completed, and also the highmass part in your return value is removed since we don't have it yet.
	def ztt_stitchingweight(self):
		highmass = "((genbosonmass >= 150.0 && (npartons == 0 || npartons >= 5))*1.25469132e-3) + (((genbosonmass >= 150.0) && (npartons == 1))*1.17290378e-3) + (((genbosonmass >= 150.0) && (npartons == 2))*1.17845742e-3) + (((genbosonmass >= 150.0) && (npartons == 3))*1.18139540e-3)+((genbosonmass >= 150.0 && npartons == 4)*1.15891212e-3)"

		mediummass = "((genbosonmass >= 50.0 && (npartons == 0 || npartons >= 5))*(6.36539901e-05)) + ((genbosonmass >= 50.0 && npartons == 1)*(1.11088685e-05)) + ((genbosonmass >= 50.0 && npartons == 2)*(2.30871136e-05)) + ((genbosonmass >= 50.0 && npartons == 3)*(1.45336607e-05)) +((genbosonmass >= 50.0 && genbosonmass < 150.0 && npartons == 4)*(6.36539901e-05))" #+((genbosonmass >= 50.0 && genbosonmass < 150.0 && npartons == 4)*(1.17409282e-05))"

		lowmass = "((genbosonmass < 50.0)*numberGeneratedEventsWeight*crossSectionPerEventWeight) +"
		normalization = "/(numberGeneratedEventsWeight*crossSectionPerEventWeight*sampleStitchingWeight)"
		#return "("+ highmass + " + " + mediummass+ " + " + lowmass +")"+normalization
		return "("+lowmass+mediummass+")"+normalization

	# DYJetsToLLM_150 sample currently only contains Z->tautau decays  5.94801691-05

	def zll_stitchingweight(self):
		mediummass = "((genbosonmass >= 50.0 && (npartons == 0 || npartons >= 5))*(6.36539901e-05)) + ((genbosonmass >= 50.0 && npartons == 1)*(1.11088685e-05)) + ((genbosonmass >= 50.0 && npartons == 2)*(2.30871136e-05)) + ((genbosonmass >= 50.0 && npartons == 3)*(1.45336607e-05)) +((genbosonmass >= 50.0 && genbosonmass < 150.0 && npartons == 4)*(6.36539901e-05))" #+((genbosonmass >= 50.0 && genbosonmass < 150.0 && npartons == 4)*(1.17409282e-05))"

		lowmass = "((genbosonmass < 50.0)*numberGeneratedEventsWeight*crossSectionPerEventWeight) +"
		normalization = "/(numberGeneratedEventsWeight*crossSectionPerEventWeight*sampleStitchingWeight)"
		#return "("+mediummass+ " + " + lowmass+")"+normalization
		return "("+lowmass+mediummass+")"+normalization

	def wj_stitchingweight(self, use_ext_sample=True):
		# return "(((npartons == 0 || npartons >= 5)*(1.37088105e-03)) + ((npartons == 1)*(1.54354730e-04)) + ((npartons == 2)*(3.62872916e-04)) + ((npartons == 3)*(5.61528581e-05)) + ((npartons == 4)*(5.36308423e-05)))/(numberGeneratedEventsWeight*crossSectionPerEventWeight*sampleStitchingWeight)"
		if use_ext_sample:
			return "(((npartons == 0 || npartons >= 5)*(8.602609716e-04)) + ((npartons == 1)*(1.446850624e-04)) + ((npartons == 2)*(3.219452396e-04)) + ((npartons == 3)*(5.482001534e-05)) + ((npartons == 4)*(5.241373841e-05)))/(numberGeneratedEventsWeight*crossSectionPerEventWeight*sampleStitchingWeight)"
		else:
			return "(((npartons == 0 || npartons >= 5)*(2.28776768e-03)) + ((npartons == 1)*(1.61649265e-04)) + ((npartons == 2)*(4.20029057e-04)) + ((npartons == 3)*(5.70900669e-05)) + ((npartons == 4)*(5.44851148e-05)))/(numberGeneratedEventsWeight*crossSectionPerEventWeight*sampleStitchingWeight)"

	#no stitching weights since no extensions
	def ewkz_zll_stitchingweight(self):
		return "(1.0)"

	def ewkz_znn_stitchingweight(self):
		return "(1.0)"

	def ewkwm_stitchingweight(self):
		return "(1.0)"

	def ewkwp_stitchingweight(self):
		return "(1.0)"
	
	def wgamma_stitchingweight(self):
		return "(1.0)"
	
	def vv_stitchingweight(self):
		return "(1.0)"

	def ttbar_stitchingweight(self):
		return "(1.0)"

	def wwtolnuqq_stitchingweight(self):
		return "(5.32574493e-8)/(numberGeneratedEventsWeight)" # (5.32574493e-8) = 1/(8782525+9994191)

	def zzto4l_stitchingweight(self):
		return "(9.51876639e-9)/(numberGeneratedEventsWeight)" # (9.51876639e-9) = 1/(98091559+6964071)

	def ggh_stitchingweight(self, cp=None, channel=None):
		if channel=="et":
			if cp == None:
				log.warning("you want to add stitching weight but did not define cp state, returning 1")
				return "(1)"
			elif cp == "sm":
				return "((npartons<2)+((npartons>=2)*(1.30458e-08*3.045966)*(1/(numberGeneratedEventsWeight*generatorWeight*crossSectionPerEventWeight))))"
			elif cp == "mm":
				return "((npartons<2)+((npartons>=2)*(9.98162e-09*3.045966)*(1/(numberGeneratedEventsWeight*crossSectionPerEventWeight))))"
			elif cp == "ps":
				return "((npartons<2)+((npartons>=2)*(9.87958e-09*3.045966)*(1/(numberGeneratedEventsWeight*crossSectionPerEventWeight))))"
			else:
				log.warning("you want to add stitching weight but did define a wrongly configured cp state, returning 1")
				return "(1)"
		else:	
			if cp == None:
				log.warning("you want to add stitching weight but did not define cp state, returning 1")
				return "(1)"
			elif cp == "sm":
				return "((lhenpNLO<2)+((lhenpNLO==2)*(1.30458e-08*3.045966)*(1/(numberGeneratedEventsWeight*generatorWeight*crossSectionPerEventWeight))))"
			elif cp == "mm":
				return "((lhenpNLO<2)+((lhenpNLO==2)*(9.98162e-09*3.045966)*(1/(numberGeneratedEventsWeight*crossSectionPerEventWeight))))"
			elif cp == "ps":
				return "((lhenpNLO<2)+((lhenpNLO==2)*(9.87958e-09*3.045966)*(1/(numberGeneratedEventsWeight*crossSectionPerEventWeight))))"
			else:
				log.warning("you want to add stitching weight but did define a wrongly configured cp state, returning 1")
				return "(1)"

	def files_data(self, channel):
		query_rereco = {}
		query_promptreco = {}
		query_reminiaod = {}
		expect_n_results_rereco = 5 # adjust in if-statements if different depending on channel
		#expect_n_results_promptreco = 1
		expect_n_results_promptreco = 0
		#expect_n_results_reminiaod = 8
		expect_n_results_reminiaod = 0
		if channel == "mt":
			query_rereco = { "process" : "SingleMuon" }
			query_promptreco = { "process" : "SingleMuon" }
			query_reminiaod = { "process" : "SingleMuon" }
		elif channel == "et":
			query_rereco = { "process" : "SingleElectron" }
			query_promptreco = { "process" : "SingleElectron" }
			query_reminiaod = { "process" : "SingleElectron" }
		elif channel == "em" or channel == "ttbar":
			query_rereco = { "process" : "MuonEG" }
			query_promptreco = { "process" : "MuonEG" }
			query_reminiaod = { "process" : "MuonEG" }
		elif channel == "mm":
			query_rereco = { "process" : "SingleMuon" }
			query_promptreco = { "process" : "SingleMuon" }
			query_reminiaod = { "process" : "SingleMuon" }
		elif channel == "ee":
			query_rereco = { "process" : "SingleElectron" }
			query_promptreco = { "process" : "SingleElectron" }
			query_reminiaod = { "process" : "SingleElectron" }
		elif channel == "tt":
			query_rereco = { "process" : "Tau" }
			query_promptreco = { "process" : "Tau" }
			query_reminiaod = { "process" : "Tau" }
		else:
			log.error("Sample config (Data) currently not implemented for channel \"%s\"!" % channel)

		query_rereco["data"] = True
		query_rereco["campaign"] = "Run2017(B|C|D|E|F)"
		query_rereco["scenario"] = "31Mar2018v1"
		query_promptreco["data"] = True
		query_promptreco["campaign"] = "Run2017(E)"
		query_promptreco["scenario"] = "PromptRecov(1|2)"
		query_reminiaod["data"] = True
		query_reminiaod["campaign"] = "Run2017(B|C|D|E|F)"
		query_reminiaod["scenario"] = "12Sep2017*"

		rereco_files = self.artus_file_names(query_rereco, expect_n_results_rereco)
		promptreco_files = self.artus_file_names(query_promptreco, expect_n_results_promptreco)
		reminiaod_files = self.artus_file_names(query_reminiaod, expect_n_results_reminiaod)
		return rereco_files 
		#return reminiaod_files

	def data(self, config, channel, category, weight, nick_suffix, exclude_cuts=None, cut_type="baseline", **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []

		scale_factor = 1.0
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("data_obs", 1.0)
		data_weight = "(1.0)"
		if kwargs.get("project_to_lumi", False):
			data_weight = "({projection})*".format(projection=kwargs["project_to_lumi"]) + data_weight

		Samples._add_input(
				config,
				self.files_data(channel),
				self.root_file_folder(channel),
				1.0,
				make_multiplication([data_weight, weight, "eventWeight", self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)]),
				"data",
				nick_suffix=nick_suffix
		)

		Samples._add_plot(config, "data", "E", "ELP", "data", nick_suffix)
		return config


	def files_ztt(self, channel, embedding=False):
		#artus_files = self.artus_file_names({"process" : "(DYJetsToLLM50|DY1JetsToLLM50|DY2JetsToLLM50|DY3JetsToLLM50)", "data": False, "campaign" : self.mc_campaign, "generator" : "madgraph\-pythia8"}, 7) #8 mit norm DY3 jets und DY4jets		TOO many not used samples in samples run 2 so i did it the fast and dirty way
		if embedding:
			if channel=='mt':
				return self.artus_file_names({"process" : "Embedding2017.*" , "campaign" : "MuTauFinalState" , "scenario" : ".*v2"}, 5)
			elif channel=='et':
				return self.artus_file_names({"process" : "Embedding2017.*" , "campaign" : "ElTauFinalState" , "scenario" : ".*v2"}, 5)
			elif channel=='tt':
				return self.artus_file_names({"process" : "Embedding2017.*" , "campaign" : "TauTauFinalState" , "scenario" : ".*v2"}, 5)
			elif channel=='em':
				return self.artus_file_names({"process" : "Embedding2017.*" , "campaign" : "ElMuFinalState" , "scenario" : ".*v2"}, 5)
		else:
			artus_files = "DY1JetsToLLM50_RunIIFall17MiniAODv2_PU2017_13TeV_MINIAOD_madgraph-pythia8/*.root DY1JetsToLLM50_RunIIFall17MiniAODv2_PU2017_13TeV_MINIAOD_madgraph-pythia8_ext1/*.root DY2JetsToLLM50_RunIIFall17MiniAODv2_PU2017_13TeV_MINIAOD_madgraph-pythia8/*.root DY2JetsToLLM50_RunIIFall17MiniAODv2_PU2017_13TeV_MINIAOD_madgraph-pythia8_ext1/*.root DY3JetsToLLM50_RunIIFall17MiniAODv2_PU2017_13TeV_MINIAOD_madgraph-pythia8/*.root DY3JetsToLLM50_RunIIFall17MiniAODv2_PU2017_13TeV_MINIAOD_madgraph-pythia8_ext1/*.root DYJetsToLLM10to50_RunIIFall17MiniAODv2_PU2017_13TeV_MINIAOD_madgraph-pythia8/*.root DYJetsToLLM50_RunIIFall17MiniAODv2_PU2017RECOSIMstep_13TeV_MINIAOD_madgraph-pythia8/*.root DYJetsToLLM50_RunIIFall17MiniAODv2_PU2017RECOSIMstep_13TeV_MINIAOD_madgraph-pythia8_ext1/*.root"
			return artus_files

	def files_zll(self, channel):
		#artus_files = self.artus_file_names({"process" : "(DYJetsToLLM50|DY1JetsToLLM50|DY2JetsToLLM50|DY3JetsToLLM50)", "data": False, "campaign" : self.mc_campaign, "generator" : "madgraph\-pythia8"}, 7) #8 mit norm DY3 jets und DY4jets		TOO many not used samples in samples run 2 so i did it the fast and dirty way
		artus_files = "DY1JetsToLLM50_RunIIFall17MiniAODv2_PU2017_13TeV_MINIAOD_madgraph-pythia8/*.root DY1JetsToLLM50_RunIIFall17MiniAODv2_PU2017_13TeV_MINIAOD_madgraph-pythia8_ext1/*.root DY2JetsToLLM50_RunIIFall17MiniAODv2_PU2017_13TeV_MINIAOD_madgraph-pythia8/*.root DY2JetsToLLM50_RunIIFall17MiniAODv2_PU2017_13TeV_MINIAOD_madgraph-pythia8_ext1/*.root DY3JetsToLLM50_RunIIFall17MiniAODv2_PU2017_13TeV_MINIAOD_madgraph-pythia8/*.root DY3JetsToLLM50_RunIIFall17MiniAODv2_PU2017_13TeV_MINIAOD_madgraph-pythia8_ext1/*.root DYJetsToLLM10to50_RunIIFall17MiniAODv2_PU2017_13TeV_MINIAOD_madgraph-pythia8/*.root DYJetsToLLM50_RunIIFall17MiniAODv2_PU2017RECOSIMstep_13TeV_MINIAOD_madgraph-pythia8/*.root DYJetsToLLM50_RunIIFall17MiniAODv2_PU2017RECOSIMstep_13TeV_MINIAOD_madgraph-pythia8_ext1/*.root"
		return artus_files

	def files_ewkwm(self, channel):
		ewkw_query = { "data" : False,
						"campaign" : self.mc_campaign,
						"generator" : "madgraph-pythia8",
						"process" : "EWKWMinus2Jets_WToLNuM50"}
		artus_files = self.artus_file_names(ewkw_query, 1)
		return artus_files

	def files_ewkwp(self, channel):
		ewkw_query = { "data" : False,
						"campaign" : self.mc_campaign,
						"generator" : "madgraph-pythia8",
						"process" : "EWKWPlus2Jets_WToLNuM50"}
		artus_files = self.artus_file_names(ewkw_query, 1)
		return artus_files

	def files_ewkz_zll(self, channel):
		ewkz_query = { "data" : False,
						"campaign" : self.mc_campaign,
						"generator" : "madgraph-pythia8",
						"process" : "EWKZ2Jets_ZToLL_M50"}
		artus_files = self.artus_file_names(ewkz_query, 1)
		return artus_files

	def files_ewkz_znn(self, channel):
		ewkz_query = { "data" : False,
						"campaign" : self.mc_campaign,
						"generator" : "madgraph-pythia8",
						"process" : "EWKZ2Jets"}
		artus_files = self.artus_file_names(ewkz_query, 1)
		return artus_files

	def ewkz(self, config, channel, category, weight, nick_suffix, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", fakefactor_method=None, **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []
		
		zmm_cr_factor = kwargs.get("zmm_cr_factor", "(1.0)")

		scale_factor = lumi
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("EWKZ", 1.0)

		data_weight, mc_weight = self.projection(kwargs)
		add_input = partialmethod(Samples._add_input, config=config, folder=self.root_file_folder(channel), scale_factor=lumi, nick_suffix=nick_suffix)	
		if channel in ["mt", "et", "em", "tt", "mm", "ee", "ttbar"]:
			add_input(
					input_file=self.files_ewkz_zll(channel),
					weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+zmm_cr_factor+"*"+self.ewkz_zll_stitchingweight()+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
					nick="ewkz"
			)
			add_input(
					input_file=self.files_ewkz_znn(channel),
					weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+zmm_cr_factor+"*"+self.ewkz_znn_stitchingweight()+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
					nick="ewkz"
			)
		else:
			log.error("Sample config (EWKZ) currently not implemented for channel \"%s\"!" % channel)
		if not kwargs.get("mssm", False):
			Samples._add_bin_corrections(config, "ewkz", nick_suffix)
		
		if not kwargs.get("no_plot", False):
			Samples._add_plot(config, "bkg", "HIST", "F", kwargs.get("color_label_key", "ewkz"), nick_suffix)
		return config

	def files_ttj(self, channel):
		if self.ttbar_retuned:
			return self.artus_file_names({"process" : "TTTo.*", "data": False, "campaign" : self.mc_campaign}, 3)
		else:
			return self.artus_file_names({"process" : "TTTo.*", "data": False, "campaign" : self.mc_campaign}, 3)


	########### W+NJETS FILES ################
	def files_wj(self, channel, use_ext_sample=True):
		if use_ext_sample:
			artus_files = self.artus_file_names({"process" : "W.*JetsToLNu", "data" : False, "campaign" : self.mc_campaign, "generator" : "madgraph-pythia8"}, 6)
			return artus_files
		else:
			artus_files = self.artus_file_names({"process" : "W.*JetsToLNu", "data" : False, "campaign" : self.mc_campaign, "generator" : "madgraph-pythia8", "extension" : ""}, 5)
			return artus_files


	############ DIBOSON FILES ###############
	def files_wwtolnuqq(self, channel):
		artus_files = self.artus_file_names({ "process" : "WWToLNuQQ","data" : False, "campaign" : self.mc_campaign, "generator" : "powheg-pythia8"}, 2)
		return artus_files

	def files_wwto4q(self, channel):
		artus_files = self.artus_file_names({ "process" : "WWTo4Q", "data" : False, "campaign" : self.mc_campaign, "generator" : "powheg-pythia8"}, 1)
		return artus_files

	def files_wzto1l3nu(self, channel):
		artus_files = self.artus_file_names({ "process" : "WZTo1L3Nu", "data" : False, "campaign" : self.mc_campaign, "generator" : "amcatnlo-pythia8"}, 1)
		return artus_files

	def files_wzto3lnu(self, channel):
		artus_files = self.artus_file_names({ "process" : "WZTo3LNu", "data" : False, "campaign" : self.mc_campaign, "generator" : "amcatnlo-pythia8"}, 1)
		return artus_files

	def files_zzto2l2nu(self, channel):
		artus_files = self.artus_file_names({ "process" : "ZZTo2L2Nu", "data" : False, "campaign" : self.mc_campaign, "generator" : "powheg-pythia8"}, 1)
		return artus_files

	def files_zzto4l(self, channel):
		artus_files = self.artus_file_names({ "process" : "ZZTo4L", "data" : False, "campaign" : self.mc_campaign, "generator" : "powheg-pythia8"}, 2)
		return artus_files

	def files_singletop(self, channel):
		artus_files = self.artus_file_names({ "process" : "(STtWantitop5finclusiveDecaysTuneCP5|STtWtop5finclusiveDecaysTuneCP5)",
							"data" : False, "campaign" : self.mc_campaign}, 2)
		artus_files = artus_files + " " + self.artus_file_names({ "process" : "(STt-channelantitop4finclusiveDecaysTuneCP5|STt-channeltop4finclusiveDecaysTuneCP5)",
		                      "data" : False, "campaign" : self.mc_campaign}, 2)
		return artus_files


	#wwtolnuqq_stitchingweight
	#zzto4l_stitchingweight

	def vvt(self, config, channel, category, weight, nick_suffix, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", fakefactor_method=False, **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []

		scale_factor = lumi
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("Dibosons", 1.0)

		data_weight, mc_weight = self.projection(kwargs)
		add_input = partialmethod(Samples._add_input, config=config, folder=self.root_file_folder(channel), scale_factor=lumi, nick_suffix=nick_suffix)
		if channel in ["mt", "et", "tt"]:
			add_input(
					input_file=self.files_wwtolnuqq(channel),
					weight=mc_weight+"*"+weight+"*eventWeight*"+Samples.ttt_genmatch(channel,kwargs)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+self.embedding_ttbarveto_weight(channel)+"*"+self.nojetsfakefactor_weight(channel, fakefactor_method=fakefactor_method)+"*"+self.wwtolnuqq_stitchingweight(),
					nick="vvt"
			)
			add_input(
					input_file=self.files_wwto4q(channel),
					weight=mc_weight+"*"+weight+"*eventWeight*"+Samples.ttt_genmatch(channel,kwargs)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+self.embedding_ttbarveto_weight(channel)+"*"+self.nojetsfakefactor_weight(channel, fakefactor_method=fakefactor_method),
					nick="vvt"
			)
			add_input(
					input_file=self.files_wzto1l3nu(channel),
					weight=mc_weight+"*"+weight+"*eventWeight*"+Samples.ttt_genmatch(channel,kwargs)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+self.embedding_ttbarveto_weight(channel)+"*"+self.nojetsfakefactor_weight(channel, fakefactor_method=fakefactor_method),
					nick="vvt"
			)
			add_input(
					input_file=self.files_wzto3lnu(channel),
					weight=mc_weight+"*"+weight+"*eventWeight*"+Samples.ttt_genmatch(channel,kwargs)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+self.embedding_ttbarveto_weight(channel)+"*"+self.nojetsfakefactor_weight(channel, fakefactor_method=fakefactor_method),
					nick="vvt"
			)
			add_input(
					input_file=self.files_zzto2l2nu(channel),
					weight=mc_weight+"*"+weight+"*eventWeight*"+Samples.ttt_genmatch(channel,kwargs)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+self.embedding_ttbarveto_weight(channel)+"*"+self.nojetsfakefactor_weight(channel, fakefactor_method=fakefactor_method),
					nick="vvt"
			)
			add_input(
					input_file=self.files_zzto4l(channel),
					weight=mc_weight+"*"+weight+"*eventWeight*"+Samples.ttt_genmatch(channel,kwargs)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+self.embedding_ttbarveto_weight(channel)+"*"+self.nojetsfakefactor_weight(channel, fakefactor_method=fakefactor_method)+"*"+self.zzto4l_stitchingweight(),
					nick="vvt"
			)
			add_input(
					input_file=self.files_singletop(channel),
					weight=mc_weight+"*"+weight+"*eventWeight*"+Samples.ttj_genmatch(channel,kwargs)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type),
					nick="vvt"
			)
		else:
			log.error("Sample config (VVT) currently not implemented for channel \"%s\"!" % channel)
		if not kwargs.get("mssm", False):
			Samples._add_bin_corrections(config, "vvt", nick_suffix)

		if not kwargs.get("no_plot", False):
			Samples._add_plot(config, "bkg", "HIST", "F", kwargs.get("color_label_key", "vvt"), nick_suffix)
		return config

	def vvj(self, config, channel, category, weight, nick_suffix, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", fakefactor_method=False, **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []

		scale_factor = lumi
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("Dibosons", 1.0)

		data_weight, mc_weight = self.projection(kwargs)
		add_input = partialmethod(Samples._add_input, config=config, folder=self.root_file_folder(channel), scale_factor=lumi, nick_suffix=nick_suffix)
		if channel in ["mt", "et", "tt"]:
			add_input(
					input_file=self.files_wwtolnuqq(channel),
					weight=mc_weight+"*"+weight+"*eventWeight*"+Samples.ttj_genmatch(channel,kwargs)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+self.embedding_ttbarveto_weight(channel)+"*"+self.wwtolnuqq_stitchingweight(),
					nick="vvj"
			)
			add_input(
					input_file=self.files_wwto4q(channel),
					weight=mc_weight+"*"+weight+"*eventWeight*"+Samples.ttj_genmatch(channel,kwargs)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+self.embedding_ttbarveto_weight(channel),
					nick="vvj"
			)
			add_input(
					input_file=self.files_wzto1l3nu(channel),
					weight=mc_weight+"*"+weight+"*eventWeight*"+Samples.ttj_genmatch(channel,kwargs)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+self.embedding_ttbarveto_weight(channel),
					nick="vvj"
			)
			add_input(
					input_file=self.files_wzto3lnu(channel),
					weight=mc_weight+"*"+weight+"*eventWeight*"+Samples.ttj_genmatch(channel,kwargs)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+self.embedding_ttbarveto_weight(channel),
					nick="vvj"
			)
			add_input(
					input_file=self.files_zzto2l2nu(channel),
					weight=mc_weight+"*"+weight+"*eventWeight*"+Samples.ttj_genmatch(channel,kwargs)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+self.embedding_ttbarveto_weight(channel),
					nick="vvj"
			)
			add_input(
					input_file=self.files_zzto4l(channel),
					weight=mc_weight+"*"+weight+"*eventWeight*"+Samples.ttj_genmatch(channel,kwargs)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+self.embedding_ttbarveto_weight(channel)+"*"+self.zzto4l_stitchingweight(),
					nick="vvj"
			)
			add_input(
					input_file=self.files_singletop(channel),
					weight=mc_weight+"*"+weight+"*eventWeight*"+Samples.ttj_genmatch(channel,kwargs)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type),
					nick="vvj"
			)
		else:
			log.error("Sample config (VVJ) currently not implemented for channel \"%s\"!" % channel)
		if not kwargs.get("mssm", False):
			Samples._add_bin_corrections(config, "vvt", nick_suffix)

		if not kwargs.get("no_plot", False):
			Samples._add_plot(config, "bkg", "HIST", "F", kwargs.get("color_label_key", "vvt"), nick_suffix)
		return config

	def vv(self, config, channel, category, weight, nick_suffix, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", fakefactor_method=False, **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []

		scale_factor = lumi
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("Dibosons", 1.0)

		data_weight, mc_weight = self.projection(kwargs)
		add_input = partialmethod(Samples._add_input, config=config, folder=self.root_file_folder(channel), scale_factor=lumi, nick_suffix=nick_suffix)
		if channel in ["mt", "et", "tt"]:
			add_input(
					input_file=self.files_wwtolnuqq(channel),
					weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+self.embedding_ttbarveto_weight(channel)+"*"+self.wwtolnuqq_stitchingweight(),
					nick="vv"
			)
			add_input(
					input_file=self.files_wwto4q(channel),
					weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+self.embedding_ttbarveto_weight(channel),
					nick="vv"
			)
			add_input(
					input_file=self.files_wzto1l3nu(channel),
					weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+self.embedding_ttbarveto_weight(channel),
					nick="vv"
			)
			add_input(
					input_file=self.files_wzto3lnu(channel),
					weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+self.embedding_ttbarveto_weight(channel),
					nick="vv"
			)
			add_input(
					input_file=self.files_zzto2l2nu(channel),
					weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+self.embedding_ttbarveto_weight(channel),
					nick="vv"
			)
			add_input(
					input_file=self.files_zzto4l(channel),
					weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+self.embedding_ttbarveto_weight(channel)+"*"+self.zzto4l_stitchingweight(),
					nick="vv"
			)
			add_input(
					input_file=self.files_singletop(channel),
					weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type),
					nick="vv"
			)
		else:
			log.error("Sample config (VV) currently not implemented for channel \"%s\"!" % channel)
		if not kwargs.get("mssm", False):
			Samples._add_bin_corrections(config, "vvt", nick_suffix)

		if not kwargs.get("no_plot", False):
			Samples._add_plot(config, "bkg", "HIST", "F", kwargs.get("color_label_key", "vvt"), nick_suffix)
		return config

	################higgs files###########################
	def files_qqh(self, channel, mass=125, **kwargs):
		cp = kwargs.get("cp", None)
		if cp is None or  cp =="cpeven":
			#CAUTION: If necessary the mc-generator nick might need to be updated from time to time. added v2 to this, if mc_campaign changes change this as well
			return self.artus_file_names({"process" : "VBFHToTauTau_M"+str(mass), "data": False, "campaign" : self.mc_campaign, "generator" : "powheg-pythia8"}, 1)  

		#TODO add the 2017 samples cp samples if they are ready		
		"""
		elif "jhu" in cp: #TODO add the 2017 samples
			
			if "sm" in cp:
				return "VBFHiggs0PMM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_JHUgenv6//*.root"		
			if "ps" in cp:
				return "VBFHiggs0MM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_JHUgenv6/*.root"
			if "mm" in cp:
				return "VBFHiggs0Mf05ph0M125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_JHUgenv6/*.root"
		elif cp in ["sm", "mm", "ps"]:
			return "VBFHToTauTauM125_RunIISpring16MiniAODv2reHLT_PUSpring16RAWAODSIM_13TeV_MINIAOD_amcatnlo-pythia8/*.root"
		"""

	def files_ggh(self, channel, mass=125, **kwargs):
		cp = kwargs.get("cp", None)
		generator = kwargs.get("generator", "madgraph")
		if generator == "madgraph":
			if "sm" in cp:
				return "GluGluToHToTauTauM125_RunIIFall17MiniAODv2_PU2017_13TeV_MINIAOD_amcatnlo-pythia8/*.root GluGluToHToTauTauPlusTwoJetsM125_RunIIFall17MiniAODv2_PU2017_13TeV_MINIAOD_amcatnlo-pythia8/*.root" #FIXME change to total sm		
			if "ps" in cp:
				return "GluGluToPseudoscalarHToTauTauM125_dwinterb_RunIIFall17MiniAODv2_GluGluToPseudoscalarHToTauTau_13TeV_USER_amcatnlo-pythia8/*.root GluGluToPseudoscalarHToTauTauPlusTwoJetsM125_RunIIFall17MiniAODv2_PU2017_13TeV_MINIAOD_amcatnlo-pythia8/*.root"
			if "mm" in cp:
				return "GluGluToMaxmixHToTauTauM125_dwinterb_RunIIFall17MiniAODv2_GluGluToMaxmixHToTauTau_13TeV_USER_amcatnlo-pythia8/*.root GluGluToMaxmixHToTauTauPlusTwoJetsM125_RunIIFall17MiniAODv2_PU2017_13TeV_MINIAOD_amcatnlo-pythia8/*.root"

		elif generator == "jhu":
			#CAUTION: If necessary the mc-generator nick might need to be updated from time to time.
			if "sm" in cp:
				return "JJHiggs0PMToTauTauPseudoscalarDecayM125_RunIIFall17MiniAODv2_PU2017_13TeV_MINIAOD_JHUgen-pythia8/*.root" #FIXME change to total sm		
			if "ps" in cp:
				return "JJHiggs0MToTauTauM125_RunIIFall17MiniAODv2_PU2017_13TeV_MINIAOD_JHUgen-pythia8/*.root"
			if "mm" in cp:
				return "JJHiggs0Mf05ph0ToTauTauM125_RunIIFall17MiniAODv2_PU2017_13TeV_MINIAOD_JHUgen-pythia8/*.root"
		else:
			if cp in ["sm", "mm", "ps"]:
				return "GluGluToHToTauTauM125_RunIIFall15MiniAODv2_PU25nsData2015v1_13TeV_MINIAOD_amcatnlo-pythia8/*.root"
			else:
				return self.artus_file_names({"process" : "GluGluHToTauTau_M"+str(mass), "data": False, "campaign" : self.mc_campaign, "generator" : "powheg-pythia8"}, 1)

	def files_vv(self, channel):
		return None
	
	def qcd(self, config, channel, category, weight, nick_suffix, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", estimationMethod="classic", controlregions=False,**kwargs):

		if channel== "mt":
			ss_os_factor = 1.218 #TODO for 2017
		elif channel == "et":
			ss_os_factor = 1.361 #TODO for 2017
		else:
			ss_os_factor = 0.0
		
		#Call the function as in samples_run2_2016 with the kwarg ss_os_factor as defined above 

		return super(Samples, self).qcd(config, channel, category, weight, nick_suffix, lumi=default_lumi, exclude_cuts=exclude_cuts, cut_type=cut_type, estimationMethod=estimationMethod, controlregions=controlregions, ss_os_factor=ss_os_factor)

	def wj(self, config, channel, category, weight, nick_suffix, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", fakefactor_method=None, estimationMethod="classic", controlregions=False,**kwargs):
		
		if channel== "mt":
			ss_os_factor = 1.29 #TODO for 2017
		elif channel == "et":
			ss_os_factor = 1.56 #TODO for 2017
		else:
			ss_os_factor = 0.0



		return super(Samples, self).wj(config, channel, category, weight, nick_suffix, lumi=default_lumi, exclude_cuts=exclude_cuts, cut_type=cut_type, fakefactor_method=fakefactor_method, estimationMethod=estimationMethod, controlregions=controlregions, ss_os_factor=ss_os_factor, **kwargs)


	def ff(self, config, channel, category, weight, nick_suffix, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", fake_factor_name_1="fakefactorWeight_comb_inclusive_1", fake_factor_name_2="fakefactorWeight_comb_inclusive_2",fakefactor_method=True, **kwargs):

		data_weight, mc_weight = self.projection(kwargs)
		zmm_cr_factor = kwargs.get("zmm_cr_factor", "(1.0)")
		cut_type_emb = cut_type + "emb" if self.embedding else cut_type

		if exclude_cuts is None:
			exclude_cuts = []
		exclude_cuts_ff = []
		if channel in ["mt","et"]:
			exclude_cuts_ff += ["iso_2"]
			ff_weight_2 = "((" + fake_factor_name_2 + ")*(byVLooseIsolationMVArun2017v2DBoldDMwLT2017_2>0.5)*(byTightIsolationMVArun2017v2DBoldDMwLT2017_2<0.5))"

		if channel == "tt":
			exclude_cuts_ff += ["iso_1", "iso_2"]
			ff_weight_1 = "((" + fake_factor_name_1 + ")*(byVLooseIsolationMVArun2017v2DBoldDMwLT2017_1>0.5)*(byVLooseIsolationMVArun2017v2DBoldDMwLT2017_1<0.5)*(byTightIsolationMVArun2017v2DBoldDMwLT2017_2>0.5))"   #factor 1/2 for tt already aplied in producer
			ff_weight_2 = "((" + fake_factor_name_2 + ")*(byVLooseIsolationMVArun2017v2DBoldDMwLT2017_2>0.5)*(byTightIsolationMVArun2017v2DBoldDMwLT2017_2<0.5)*(byTightIsolationMVArun2017v2DBoldDMwLT2017_1>0.5))"

		if channel =="tt":
			weight_ff = weight + "*(" + ff_weight_1 + "+" + ff_weight_2 + ")"
		elif channel in ["mt","et"]:
			weight_ff = weight + "*(" + ff_weight_2 + ")"

		weight_tau_id="(zPtReweightWeight)*(gen_match_2 < 6)*((gen_match_2 == 5)*0.97 + (gen_match_2 != 5))" if self.embedding else "(zPtReweightWeight)*(gen_match_2 < 6)*((gen_match_2 == 5)*0.89 + (gen_match_2 != 5))"

		add_input = partialmethod(Samples._add_input, config=config, folder=self.root_file_folder(channel), scale_factor=lumi, nick_suffix=nick_suffix)

		#Samples._add_plot(config, "bkg", "HIST", "F", "jetFakes", "jetFakes")
		#TODO, ff_weight is always 1 in current artus output, set it manually to 1/3 for testing
		#return config
		#if sum of shapes for wj qcd and ttbar sum up to 1,
		if channel in ["mt","et", "tt"]:
			#full data jetfakes"
			add_input(
				input_file=self.files_data(channel),
				scale_factor=1.0,
				weight=data_weight+"*"+weight_ff+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts+exclude_cuts_ff, cut_type=cut_type),
				nick="noplot_jetFakes_raw"
			)

			add_input(
				input_file=self.files_ztt(channel, embedding=self.embedding),
				weight=mc_weight+"*"+self.get_weights_ztt(channel=channel,cut_type=cut_type_emb,weight=weight_ff,embedding=self.embedding)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts+exclude_cuts_ff, cut_type=cut_type_emb)+"*"+self.decay_mode_reweight(channel, cut_type_emb)+"*"+weight_tau_id,
				scale_factor = 1.0 if self.embedding else lumi,
				nick="noplot_ff_realtaus_subtract"
			)
			"""
			add_input(
				input_file=self.files_zll(channel),
				weight=self.get_weights_zll(channel=channel,cut_type=cut_type,weight=weight_ff)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts+exclude_cuts_ff, cut_type=cut_type)+"*zPtReweightWeight*(gen_match_2 < 6)",
				nick="noplot_ff_realtaus_subtract"
			)"""

			add_input(
				input_file=self.files_zll(channel),
				weight=mc_weight+"*"+weight_ff+"*eventWeight*"+self.zll_stitchingweight()+"*"+Samples.zll_genmatch(channel)+"*"+self._cut_string(channel, exclude_cuts= exclude_cuts+exclude_cuts_ff, cut_type=cut_type)+"*(gen_match_2 < 6)"+"*"+self.zll_zl_shape_weight(channel, cut_type)+"*"+zmm_cr_factor+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type)+"*((gen_match_2 == 5)*0.89 + (gen_match_2 != 5))*(zPtReweightWeight)",
				nick="noplot_ff_realtaus_subtract"
				)

			add_input(
				input_file=self.files_ttj(channel),
				weight=mc_weight+"*"+weight_ff+"*"+self.embedding_ttbarveto_weight(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts+exclude_cuts_ff, cut_type=cut_type)+"*eventWeight*(gen_match_2 < 6)*((gen_match_2 == 5)*0.89 + (gen_match_2 != 5))",
				nick="noplot_ff_realtaus_subtract"
			)
			add_input(
					input_file=self.files_wwtolnuqq(channel),
					weight=mc_weight+"*"+weight_ff+"*"+weight+"*eventWeight*"+Samples.ttt_genmatch(channel,kwargs)+"*"+self.embedding_ttbarveto_weight(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+self.nojetsfakefactor_weight(channel, fakefactor_method=fakefactor_method)+"*"+self.wwtolnuqq_stitchingweight()+"*eventWeight*(gen_match_2 < 6)*((gen_match_2 == 5)*0.89 + (gen_match_2 != 5))",
					nick="noplot_ff_realtaus_subtract"
			)
			add_input(
					input_file=self.files_wwto4q(channel),
					weight=mc_weight+"*"+weight_ff+"*"+weight+"*eventWeight*"+Samples.ttt_genmatch(channel,kwargs)+"*"+self.embedding_ttbarveto_weight(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+self.nojetsfakefactor_weight(channel, fakefactor_method=fakefactor_method)+"*eventWeight*(gen_match_2 < 6)*((gen_match_2 == 5)*0.89 + (gen_match_2 != 5))",
					nick="noplot_ff_realtaus_subtract"
			)
			add_input(
					input_file=self.files_wzto1l3nu(channel),
					weight=mc_weight+"*"+weight_ff+"*"+weight+"*eventWeight*"+Samples.ttt_genmatch(channel,kwargs)+"*"+self.embedding_ttbarveto_weight(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+self.nojetsfakefactor_weight(channel, fakefactor_method=fakefactor_method)+"*eventWeight*(gen_match_2 < 6)*((gen_match_2 == 5)*0.89 + (gen_match_2 != 5))",
					nick="noplot_ff_realtaus_subtract"
			)
			add_input(
					input_file=self.files_wzto3lnu(channel),
					weight=mc_weight+"*"+weight_ff+"*"+weight+"*eventWeight*"+Samples.ttt_genmatch(channel,kwargs)+"*"+self.embedding_ttbarveto_weight(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+self.nojetsfakefactor_weight(channel, fakefactor_method=fakefactor_method)+"*eventWeight*(gen_match_2 < 6)*((gen_match_2 == 5)*0.89 + (gen_match_2 != 5))",
					nick="noplot_ff_realtaus_subtract"
			)
			add_input(
					input_file=self.files_zzto2l2nu(channel),
					weight=mc_weight+"*"+weight_ff+"*"+weight+"*eventWeight*"+Samples.ttt_genmatch(channel,kwargs)+"*"+self.embedding_ttbarveto_weight(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+self.nojetsfakefactor_weight(channel, fakefactor_method=fakefactor_method)+"*eventWeight*(gen_match_2 < 6)*((gen_match_2 == 5)*0.89 + (gen_match_2 != 5))",
					nick="noplot_ff_realtaus_subtract"
			)
			add_input(
					input_file=self.files_zzto4l(channel),
					weight=mc_weight+"*"+weight_ff+"*"+weight+"*eventWeight*"+Samples.ttt_genmatch(channel,kwargs)+"*"+self.embedding_ttbarveto_weight(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+self.nojetsfakefactor_weight(channel, fakefactor_method=fakefactor_method)+"*"+self.zzto4l_stitchingweight()+"*eventWeight*(gen_match_2 < 6)*((gen_match_2 == 5)*0.89 + (gen_match_2 != 5))",
					nick="noplot_ff_realtaus_subtract"
			)
			add_input(
					input_file=self.files_singletop(channel),
					weight=mc_weight+"*"+weight_ff+"*"+weight+"*eventWeight*"+Samples.ttj_genmatch(channel,kwargs)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*eventWeight*(gen_match_2 < 6)*((gen_match_2 == 5)*0.89 + (gen_match_2 != 5))",
					nick="noplot_ff_realtaus_subtract"
			)
			if not "AddHistograms" in config.get("analysis_modules", []):
				config.setdefault("analysis_modules", []).append("AddHistograms")


			config.setdefault("add_nicks", []).append("noplot_jetFakes_raw noplot_ff_realtaus_subtract") #TODO

			config.setdefault("add_scale_factors", []).append("1. -1.")#TODO ff_weight is always 1 in current artus output, set it manually to 1/3 for testing should be 1 

			config.setdefault("add_result_nicks", []).append("ff")

		else:
			log.error("Sample config (FakeFactor) currently not implemented for channel \"%s\"!" % channel)

		Samples._add_plot(config, "bkg", "HIST", "F", "ff", nick_suffix)
		return config

	

