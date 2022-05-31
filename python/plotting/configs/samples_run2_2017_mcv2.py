# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import pprint
import copy
import sys
import os

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

		if self.legacy:
			mediummass = "((genbosonmass >= 50.0 && (npartons == 0 || npartons >= 5))*(6.21386672e-05)) + ((genbosonmass >= 50.0 && npartons == 1)*(1.70966124e-05)) + ((genbosonmass >= 50.0 && npartons == 2)*(2.21803680e-05)) + ((genbosonmass >= 50.0 && npartons == 3)*(1.41876778e-05)) +((genbosonmass >= 50.0 && genbosonmass < 150.0 && npartons == 4)*(6.21386672e-05))" #+((genbosonmass >= 50.0 && genbosonmass < 150.0 && npartons == 4)*(1.17409282e-05))"
		else:
			mediummass = "((genbosonmass >= 50.0 && (npartons == 0 || npartons >= 5))*(6.36539901e-05)) + ((genbosonmass >= 50.0 && npartons == 1)*(1.11088685e-05)) + ((genbosonmass >= 50.0 && npartons == 2)*(2.30871136e-05)) + ((genbosonmass >= 50.0 && npartons == 3)*(1.45336607e-05)) +((genbosonmass >= 50.0 && genbosonmass < 150.0 && npartons == 4)*(6.36539901e-05))" #+((genbosonmass >= 50.0 && genbosonmass < 150.0 && npartons == 4)*(1.17409282e-05))"

		lowmass = "((genbosonmass < 50.0)*numberGeneratedEventsWeight*crossSectionPerEventWeight) +"
		normalization = "/(numberGeneratedEventsWeight*crossSectionPerEventWeight*sampleStitchingWeight)"
		#return "("+ highmass + " + " + mediummass+ " + " + lowmass +")"+normalization
		return "("+lowmass+mediummass+")"+normalization

	# DYJetsToLLM_150 sample currently only contains Z->tautau decays  5.94801691-05

	def zll_stitchingweight(self):
		if self.legacy:
			mediummass = "((genbosonmass >= 50.0 && (npartons == 0 || npartons >= 5))*(6.21386672e-05)) + ((genbosonmass >= 50.0 && npartons == 1)*(1.70966124e-05)) + ((genbosonmass >= 50.0 && npartons == 2)*(2.21803680e-05)) + ((genbosonmass >= 50.0 && npartons == 3)*(1.41876778e-05)) +((genbosonmass >= 50.0 && genbosonmass < 150.0 && npartons == 4)*(6.21386672e-05))" #+((genbosonmass >= 50.0 && genbosonmass < 150.0 && npartons == 4)*(1.17409282e-05))"
		else:
			mediummass = "((genbosonmass >= 50.0 && (npartons == 0 || npartons >= 5))*(6.36539901e-05)) + ((genbosonmass >= 50.0 && npartons == 1)*(1.11088685e-05)) + ((genbosonmass >= 50.0 && npartons == 2)*(2.30871136e-05)) + ((genbosonmass >= 50.0 && npartons == 3)*(1.45336607e-05)) +((genbosonmass >= 50.0 && genbosonmass < 150.0 && npartons == 4)*(6.36539901e-05))" #+((genbosonmass >= 50.0 && genbosonmass < 150.0 && npartons == 4)*(1.17409282e-05))"

		lowmass = "((genbosonmass < 50.0)*numberGeneratedEventsWeight*crossSectionPerEventWeight) +"
		normalization = "/(numberGeneratedEventsWeight*crossSectionPerEventWeight*sampleStitchingWeight)"
		#return "("+mediummass+ " + " + lowmass+")"+normalization
		return "("+lowmass+mediummass+")"+normalization

	def wj_stitchingweight(self, use_ext_sample=True):
		# return "(((npartons == 0 || npartons >= 5)*(1.37088105e-03)) + ((npartons == 1)*(1.54354730e-04)) + ((npartons == 2)*(3.62872916e-04)) + ((npartons == 3)*(5.61528581e-05)) + ((npartons == 4)*(5.36308423e-05)))/(numberGeneratedEventsWeight*crossSectionPerEventWeight*sampleStitchingWeight)"
		if self.legacy:
			return "(((npartons == 0 || npartons >= 5)*(1.37088105e-03)) + ((npartons == 1)*(1.52257926e-04)) + ((npartons == 2)*(3.62872916e-04)) + ((npartons == 3)*(5.61528581e-05)) + ((npartons == 4)*(5.46975115e-05)))/(numberGeneratedEventsWeight*crossSectionPerEventWeight*sampleStitchingWeight)"
		else:
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

	def lfv_stitchingweight(self):
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

	# def data(self, config, channel, category, weight, nick_suffix, exclude_cuts=None, cut_type="baseline", **kwargs):
	# 	if exclude_cuts is None:
	# 		exclude_cuts = []
	#
	# 	scale_factor = 1.0
	# 	if not self.postfit_scales is None:
	# 		scale_factor *= self.postfit_scales.get("data_obs", 1.0)
	# 	data_weight = "(1.0)"
	# 	if kwargs.get("project_to_lumi", False):
	# 		data_weight = "({projection})*".format(projection=kwargs["project_to_lumi"]) + data_weight
	#
	# 	Samples._add_input(
	# 			config,
	# 			self.files_data(channel),
	# 			self.root_file_folder(channel),
	# 			1.0,
	# 			make_multiplication([data_weight, weight, "eventWeight", self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type, data=True)]),
	# 			"data",
	# 			nick_suffix=nick_suffix
	# 	)
	#
	# 	Samples._add_plot(config, "data", "E", "ELP", "data", nick_suffix)
	# 	return config


	def files_lfv(self, channel):
		return self.artus_file_names({"process" : "LFV*", "data": False, "scenario" : "RunIIFall17"}, 1)


	def zmt(self, config, channel, category, weight, nick_suffix, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", fakefactor_method=False, **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []

		scale_factor = lumi

		branching_ratio = "1.2e-5" #"(0.03363)*0.66*0.17*2"
		cross_section_weight = "3.0" # "(0.03363+0.03366+0.0337)/(0.0337)"
		scale_factor = "50"

		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("TTJ", 1.0)

		data_weight, mc_weight = self.projection(kwargs)
		add_input = partialmethod(Samples._add_input, config=config, folder=self.root_file_folder(channel), scale_factor=lumi, nick_suffix=nick_suffix)
		add_input(
				input_file=self.files_lfv(channel),
				weight=scale_factor+"*"+mc_weight+"*"+weight+"*eventWeight*"+Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind"], cut_type=cut_type)+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type)+"*"+"(1.0)"+"*"+branching_ratio+"*"+cross_section_weight,
				nick="zmt"
		)

		Samples._add_bin_corrections(config, "zmt", nick_suffix)

		if not kwargs.get("no_plot", False):
			Samples._add_plot(config, "sig", "LINE", "F", kwargs.get("color_label_key", "zmt"), nick_suffix)

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
			if self.legacy:
				artus_files = "DY1JetsToLLM50_RunIIFall17MiniAODv2_PU2017_13TeV_MINIAOD_madgraph-pythia8/*.root DY1JetsToLLM50_RunIIFall17MiniAODv2_PU2017_13TeV_MINIAOD_madgraph-pythia8_ext1/*.root DY2JetsToLLM50_RunIIFall17MiniAODv2_PU2017newpmx_13TeV_MINIAOD_madgraph-pythia8_ext1/*.root DY3JetsToLLM50_RunIIFall17MiniAODv2_PU2017_13TeV_MINIAOD_madgraph-pythia8/*.root DY3JetsToLLM50_RunIIFall17MiniAODv2_PU2017_13TeV_MINIAOD_madgraph-pythia8_ext1/*.root DYJetsToLLM10to50_RunIIFall17MiniAODv2_PU2017_13TeV_MINIAOD_madgraph-pythia8/*.root DYJetsToLLM50_RunIIFall17MiniAODv2_PU2017RECOSIMstep_13TeV_MINIAOD_madgraph-pythia8/*.root DYJetsToLLM50_RunIIFall17MiniAODv2_PU2017RECOSIMstep_13TeV_MINIAOD_madgraph-pythia8_ext1/*.root"
			else:
				artus_files = "DY1JetsToLLM50_RunIIFall17MiniAODv2_PU2017_13TeV_MINIAOD_madgraph-pythia8/*.root DY1JetsToLLM50_RunIIFall17MiniAODv2_PU2017_13TeV_MINIAOD_madgraph-pythia8_ext1/*.root DY2JetsToLLM50_RunIIFall17MiniAODv2_PU2017_13TeV_MINIAOD_madgraph-pythia8/*.root DY2JetsToLLM50_RunIIFall17MiniAODv2_PU2017_13TeV_MINIAOD_madgraph-pythia8_ext1/*.root DY3JetsToLLM50_RunIIFall17MiniAODv2_PU2017_13TeV_MINIAOD_madgraph-pythia8/*.root DY3JetsToLLM50_RunIIFall17MiniAODv2_PU2017_13TeV_MINIAOD_madgraph-pythia8_ext1/*.root DYJetsToLLM10to50_RunIIFall17MiniAODv2_PU2017_13TeV_MINIAOD_madgraph-pythia8/*.root DYJetsToLLM50_RunIIFall17MiniAODv2_PU2017RECOSIMstep_13TeV_MINIAOD_madgraph-pythia8/*.root DYJetsToLLM50_RunIIFall17MiniAODv2_PU2017RECOSIMstep_13TeV_MINIAOD_madgraph-pythia8_ext1/*.root"
			return artus_files

	def files_zll(self, channel):
		#artus_files = self.artus_file_names({"process" : "(DYJetsToLLM50|DY1JetsToLLM50|DY2JetsToLLM50|DY3JetsToLLM50)", "data": False, "campaign" : self.mc_campaign, "generator" : "madgraph\-pythia8"}, 7) #8 mit norm DY3 jets und DY4jets		TOO many not used samples in samples run 2 so i did it the fast and dirty way
		if self.legacy:
			artus_files = "DY1JetsToLLM50_RunIIFall17MiniAODv2_PU2017_13TeV_MINIAOD_madgraph-pythia8/*.root DY1JetsToLLM50_RunIIFall17MiniAODv2_PU2017_13TeV_MINIAOD_madgraph-pythia8_ext1/*.root DY2JetsToLLM50_RunIIFall17MiniAODv2_PU2017newpmx_13TeV_MINIAOD_madgraph-pythia8_ext1/*.root DY3JetsToLLM50_RunIIFall17MiniAODv2_PU2017_13TeV_MINIAOD_madgraph-pythia8/*.root DY3JetsToLLM50_RunIIFall17MiniAODv2_PU2017_13TeV_MINIAOD_madgraph-pythia8_ext1/*.root DYJetsToLLM10to50_RunIIFall17MiniAODv2_PU2017_13TeV_MINIAOD_madgraph-pythia8/*.root DYJetsToLLM50_RunIIFall17MiniAODv2_PU2017RECOSIMstep_13TeV_MINIAOD_madgraph-pythia8/*.root DYJetsToLLM50_RunIIFall17MiniAODv2_PU2017RECOSIMstep_13TeV_MINIAOD_madgraph-pythia8_ext1/*.root"
		else:
			artus_files = "DY1JetsToLLM50_RunIIFall17MiniAODv2_PU2017_13TeV_MINIAOD_madgraph-pythia8/*.root DY1JetsToLLM50_RunIIFall17MiniAODv2_PU2017_13TeV_MINIAOD_madgraph-pythia8_ext1/*.root DY2JetsToLLM50_RunIIFall17MiniAODv2_PU2017_13TeV_MINIAOD_madgraph-pythia8/*.root DY2JetsToLLM50_RunIIFall17MiniAODv2_PU2017_13TeV_MINIAOD_madgraph-pythia8_ext1/*.root DY3JetsToLLM50_RunIIFall17MiniAODv2_PU2017_13TeV_MINIAOD_madgraph-pythia8/*.root DY3JetsToLLM50_RunIIFall17MiniAODv2_PU2017_13TeV_MINIAOD_madgraph-pythia8_ext1/*.root DYJetsToLLM10to50_RunIIFall17MiniAODv2_PU2017_13TeV_MINIAOD_madgraph-pythia8/*.root DYJetsToLLM50_RunIIFall17MiniAODv2_PU2017RECOSIMstep_13TeV_MINIAOD_madgraph-pythia8/*.root DYJetsToLLM50_RunIIFall17MiniAODv2_PU2017RECOSIMstep_13TeV_MINIAOD_madgraph-pythia8_ext1/*.root"
		return artus_files

	def files_ewkwm(self, channel):
		ewkw_query = { "data" : False,
						"campaign" : self.mc_campaign,
						"generator" : "madgraph-pythia8",
						"process" : "EWKWMinus2Jets_WToLNuM50",
						"scenario" : "PU2017" + "_new_pmx" if self.legacy else ""}
		artus_files = self.artus_file_names(ewkw_query, 1)
		return artus_files

	def files_ewkwp(self, channel):
		ewkw_query = { "data" : False,
						"campaign" : self.mc_campaign,
						"generator" : "madgraph-pythia8",
						"process" : "EWKWPlus2Jets_WToLNuM50",
						"scenario" : "PU2017" + "_new_pmx" if self.legacy else ""}
		artus_files = self.artus_file_names(ewkw_query, 1)
		return artus_files

	def files_ewkz_zll(self, channel):
		ewkz_query = { "data" : False,
						"campaign" : self.mc_campaign,
						"generator" : "madgraph-pythia8",
						"process" : "EWKZ2Jets_ZToLL_M50",
						"scenario" : "PU2017" + "_new_pmx" if self.legacy else ""}
		artus_files = self.artus_file_names(ewkz_query, 1)
		return artus_files

	def files_ewkz_znn(self, channel):
		ewkz_query = { "data" : False,
						"campaign" : self.mc_campaign,
						"generator" : "madgraph-pythia8",
						"process" : "EWKZ2Jets",
						"scenario" : "PU2017" + "_new_pmx" if self.legacy else ""}
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
			artus_files = self.artus_file_names({"process" : "W(|1|2|3)JetsToLNu", "data" : False, "campaign" : self.mc_campaign, "generator" : "madgraph-pythia8"}, 5)
			artus_files = artus_files + " " + self.artus_file_names({"process" : "W4JetsToLNu", "data" : False, "campaign" : self.mc_campaign, "generator" : "madgraph-pythia8", "extension" : "", "scenario" : "PU2017" + "_new_pmx" if self.legacy else ""}, 1)
			return artus_files
		else:
			artus_files = self.artus_file_names({"process" : "W(|1|2|3)JetsToLNu", "data" : False, "campaign" : self.mc_campaign, "generator" : "madgraph-pythia8", "extension" : ""}, 4)
			artus_files = artus_files + " " + self.artus_file_names({"process" : "W4JetsToLNu", "data" : False, "campaign" : self.mc_campaign, "generator" : "madgraph-pythia8", "extension" : "", "scenario" : "PU2017" + "_new_pmx" if self.legacy else ""}, 1)
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

	def files_ww(self, channel):
		artus_files = self.artus_file_names({ "process" : "WW", "data" : False, "campaign" : self.mc_campaign, "generator" : "pythia8", "scenario" : "PU2017"}, 1)
		return artus_files

	def files_wz(self, channel):
		artus_files = self.artus_file_names({ "process" : "WZ", "data" : False, "campaign" : self.mc_campaign, "generator" : "pythia8", "scenario" : "PU2017"}, 1)
		return artus_files

	def files_zz(self, channel):
		artus_files = self.artus_file_names({ "process" : "ZZ", "data" : False, "campaign" : self.mc_campaign, "generator" : "pythia8", "scenario" : "PU2017_new_pmx"}, 1)
		return artus_files

	def files_singletop(self, channel):
		artus_files = self.artus_file_names({
			"process" : "(STtWantitop5finclusiveDecaysTuneCP5|STtWtop5finclusiveDecaysTuneCP5)",
			"data" : False,
			"campaign" : self.mc_campaign,
			"scenario" : "PU2017"},
			2)
		artus_files = artus_files + " " + self.artus_file_names({
			"process" : "STt-channelantitop4finclusiveDecaysTuneCP5",
			"data" : False,
			"campaign" : self.mc_campaign,
			"scenario" : "PU2017"},
			1)
		artus_files = artus_files + " " + self.artus_file_names({
			"process" : "STt-channeltop4finclusiveDecaysTuneCP5",
			"data" : False,
			"campaign" : self.mc_campaign,
			"scenario" : "PU2017" + "_new_pmx" if self.legacy else ""},
			1)
		return artus_files

	def files_diboson(self, channel):
		artus_files = self.files_wwtolnuqq(channel) + self.files_wwto4q(channel) + self.files_wzto1l3nu(channel) + self.files_wzto3lnu(channel) + self.files_zzto2l2nu(channel) + self.files_zzto4l(channel) + self.files_singletop(channel)
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
			if self.legacy:
				add_input(
						input_file=self.files_ww(channel),
						weight=mc_weight+"*"+weight+"*eventWeight*"+Samples.ttt_genmatch(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+self.embedding_ttbarveto_weight(channel)+"*"+self.nojetsfakefactor_weight(channel, fakefactor_method=fakefactor_method),
						nick="vvt"
				)
				add_input(
						input_file=self.files_wz(channel),
						weight=mc_weight+"*"+weight+"*eventWeight*"+Samples.ttt_genmatch(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+self.embedding_ttbarveto_weight(channel)+"*"+self.nojetsfakefactor_weight(channel, fakefactor_method=fakefactor_method),
						nick="vvt"
				)
				add_input(
						input_file=self.files_zz(channel),
						weight=mc_weight+"*"+weight+"*eventWeight*"+Samples.ttt_genmatch(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+self.embedding_ttbarveto_weight(channel)+"*"+self.nojetsfakefactor_weight(channel, fakefactor_method=fakefactor_method),
						nick="vvt"
				)
			else:
				add_input(
						input_file=self.files_wwtolnuqq(channel),
						weight=mc_weight+"*"+weight+"*eventWeight*"+Samples.ttt_genmatch(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+self.embedding_ttbarveto_weight(channel)+"*"+self.nojetsfakefactor_weight(channel, fakefactor_method=fakefactor_method)+"*"+self.wwtolnuqq_stitchingweight(),
						nick="vvt"
				)
				add_input(
						input_file=self.files_wwto4q(channel),
						weight=mc_weight+"*"+weight+"*eventWeight*"+Samples.ttt_genmatch(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+self.embedding_ttbarveto_weight(channel)+"*"+self.nojetsfakefactor_weight(channel, fakefactor_method=fakefactor_method),
						nick="vvt"
				)
				add_input(
						input_file=self.files_wzto1l3nu(channel),
						weight=mc_weight+"*"+weight+"*eventWeight*"+Samples.ttt_genmatch(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+self.embedding_ttbarveto_weight(channel)+"*"+self.nojetsfakefactor_weight(channel, fakefactor_method=fakefactor_method),
						nick="vvt"
				)
				add_input(
						input_file=self.files_wzto3lnu(channel),
						weight=mc_weight+"*"+weight+"*eventWeight*"+Samples.ttt_genmatch(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+self.embedding_ttbarveto_weight(channel)+"*"+self.nojetsfakefactor_weight(channel, fakefactor_method=fakefactor_method),
						nick="vvt"
				)
				add_input(
						input_file=self.files_zzto2l2nu(channel),
						weight=mc_weight+"*"+weight+"*eventWeight*"+Samples.ttt_genmatch(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+self.embedding_ttbarveto_weight(channel)+"*"+self.nojetsfakefactor_weight(channel, fakefactor_method=fakefactor_method),
						nick="vvt"
				)
				add_input(
						input_file=self.files_zzto4l(channel),
						weight=mc_weight+"*"+weight+"*eventWeight*"+Samples.ttt_genmatch(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+self.embedding_ttbarveto_weight(channel)+"*"+self.nojetsfakefactor_weight(channel, fakefactor_method=fakefactor_method)+"*"+self.zzto4l_stitchingweight(),
						nick="vvt"
				)
			add_input(
					input_file=self.files_singletop(channel),
					weight=mc_weight+"*"+weight+"*eventWeight*"+Samples.ttt_genmatch(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type),
					nick="vvt"
			)
		else:
			log.error("Sample config (VVT) currently not implemented for channel \"%s\"!" % channel)
		if not kwargs.get("mssm", False):
			Samples._add_bin_corrections(config, "vvt", nick_suffix)

		if not kwargs.get("no_plot", False):
			Samples._add_plot(config, "bkg", "HIST", "F", kwargs.get("color_label_key", "vvt"), nick_suffix)
		return config

	def vvl(self, config, channel, category, weight, nick_suffix, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", fakefactor_method=False, **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []

		scale_factor = lumi
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("Dibosons", 1.0)

		data_weight, mc_weight = self.projection(kwargs)
		add_input = partialmethod(Samples._add_input, config=config, folder=self.root_file_folder(channel), scale_factor=lumi, nick_suffix=nick_suffix)
		if channel in ["mt", "et", "tt"]:
			if self.legacy:
				add_input(
						input_file=self.files_ww(channel),
						weight=mc_weight+"*"+weight+"*eventWeight*"+Samples.ttl_genmatch(channel,fakefactor_method=fakefactor_method)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+self.embedding_ttbarveto_weight(channel)+"*"+self.nojetsfakefactor_weight(channel, fakefactor_method=fakefactor_method),
						nick="vvl"
				)
				add_input(
						input_file=self.files_wz(channel),
						weight=mc_weight+"*"+weight+"*eventWeight*"+Samples.ttl_genmatch(channel,fakefactor_method=fakefactor_method)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+self.embedding_ttbarveto_weight(channel)+"*"+self.nojetsfakefactor_weight(channel, fakefactor_method=fakefactor_method),
						nick="vvl"
				)
				add_input(
						input_file=self.files_zz(channel),
						weight=mc_weight+"*"+weight+"*eventWeight*"+Samples.ttl_genmatch(channel,fakefactor_method=fakefactor_method)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+self.embedding_ttbarveto_weight(channel)+"*"+self.nojetsfakefactor_weight(channel, fakefactor_method=fakefactor_method),
						nick="vvl"
				)
			else:
				add_input(
						input_file=self.files_wwtolnuqq(channel),
						weight=mc_weight+"*"+weight+"*eventWeight*"+Samples.ttl_genmatch(channel,fakefactor_method=fakefactor_method)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+self.embedding_ttbarveto_weight(channel)+"*"+self.nojetsfakefactor_weight(channel, fakefactor_method=fakefactor_method)+"*"+self.wwtolnuqq_stitchingweight(),
						nick="vvl"
				)
				add_input(
						input_file=self.files_wwto4q(channel),
						weight=mc_weight+"*"+weight+"*eventWeight*"+Samples.ttl_genmatch(channel,fakefactor_method=fakefactor_method)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+self.embedding_ttbarveto_weight(channel)+"*"+self.nojetsfakefactor_weight(channel, fakefactor_method=fakefactor_method),
						nick="vvl"
				)
				add_input(
						input_file=self.files_wzto1l3nu(channel),
						weight=mc_weight+"*"+weight+"*eventWeight*"+Samples.ttl_genmatch(channel,fakefactor_method=fakefactor_method)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+self.embedding_ttbarveto_weight(channel)+"*"+self.nojetsfakefactor_weight(channel, fakefactor_method=fakefactor_method),
						nick="vvl"
				)
				add_input(
						input_file=self.files_wzto3lnu(channel),
						weight=mc_weight+"*"+weight+"*eventWeight*"+Samples.ttl_genmatch(channel,fakefactor_method=fakefactor_method)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+self.embedding_ttbarveto_weight(channel)+"*"+self.nojetsfakefactor_weight(channel, fakefactor_method=fakefactor_method),
						nick="vvl"
				)
				add_input(
						input_file=self.files_zzto2l2nu(channel),
						weight=mc_weight+"*"+weight+"*eventWeight*"+Samples.ttl_genmatch(channel,fakefactor_method=fakefactor_method)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+self.embedding_ttbarveto_weight(channel)+"*"+self.nojetsfakefactor_weight(channel, fakefactor_method=fakefactor_method),
						nick="vvl"
				)
				add_input(
						input_file=self.files_zzto4l(channel),
						weight=mc_weight+"*"+weight+"*eventWeight*"+Samples.ttl_genmatch(channel,fakefactor_method=fakefactor_method)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+self.embedding_ttbarveto_weight(channel)+"*"+self.nojetsfakefactor_weight(channel, fakefactor_method=fakefactor_method)+"*"+self.zzto4l_stitchingweight(),
						nick="vvl"
				)
				add_input(
						input_file=self.files_singletop(channel),
						weight=mc_weight+"*"+weight+"*eventWeight*"+Samples.ttl_genmatch(channel,fakefactor_method=fakefactor_method)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type),
						nick="vvl"
				)
		else:
			log.error("Sample config (VVL) currently not implemented for channel \"%s\"!" % channel)
		if not kwargs.get("mssm", False):
			Samples._add_bin_corrections(config, "vvl", nick_suffix)

		if not kwargs.get("no_plot", False):
			Samples._add_plot(config, "bkg", "HIST", "F", kwargs.get("color_label_key", "vvl"), nick_suffix)
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
			if self.legacy:
				add_input(
						input_file=self.files_ww(channel),
						weight=mc_weight+"*"+weight+"*eventWeight*"+Samples.ttj_genmatch(channel,fakefactor_method=fakefactor_method)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+self.embedding_ttbarveto_weight(channel),
						nick="vvj"
				)
				add_input(
						input_file=self.files_wz(channel),
						weight=mc_weight+"*"+weight+"*eventWeight*"+Samples.ttj_genmatch(channel,fakefactor_method=fakefactor_method)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+self.embedding_ttbarveto_weight(channel),
						nick="vvj"
				)
				add_input(
						input_file=self.files_zz(channel),
						weight=mc_weight+"*"+weight+"*eventWeight*"+Samples.ttj_genmatch(channel,fakefactor_method=fakefactor_method)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+self.embedding_ttbarveto_weight(channel),
						nick="vvj"
				)
			else:
				add_input(
						input_file=self.files_wwtolnuqq(channel),
						weight=mc_weight+"*"+weight+"*eventWeight*"+Samples.ttj_genmatch(channel,fakefactor_method=fakefactor_method)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+self.embedding_ttbarveto_weight(channel)+"*"+self.wwtolnuqq_stitchingweight(),
						nick="vvj"
				)
				add_input(
						input_file=self.files_wwto4q(channel),
						weight=mc_weight+"*"+weight+"*eventWeight*"+Samples.ttj_genmatch(channel,fakefactor_method=fakefactor_method)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+self.embedding_ttbarveto_weight(channel),
						nick="vvj"
				)
				add_input(
						input_file=self.files_wzto1l3nu(channel),
						weight=mc_weight+"*"+weight+"*eventWeight*"+Samples.ttj_genmatch(channel,fakefactor_method=fakefactor_method)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+self.embedding_ttbarveto_weight(channel),
						nick="vvj"
				)
				add_input(
						input_file=self.files_wzto3lnu(channel),
						weight=mc_weight+"*"+weight+"*eventWeight*"+Samples.ttj_genmatch(channel,fakefactor_method=fakefactor_method)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+self.embedding_ttbarveto_weight(channel),
						nick="vvj"
				)
				add_input(
						input_file=self.files_zzto2l2nu(channel),
						weight=mc_weight+"*"+weight+"*eventWeight*"+Samples.ttj_genmatch(channel,fakefactor_method=fakefactor_method)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+self.embedding_ttbarveto_weight(channel),
						nick="vvj"
				)
				add_input(
						input_file=self.files_zzto4l(channel),
						weight=mc_weight+"*"+weight+"*eventWeight*"+Samples.ttj_genmatch(channel,fakefactor_method=fakefactor_method)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+self.embedding_ttbarveto_weight(channel)+"*"+self.zzto4l_stitchingweight(),
						nick="vvj"
				)
			add_input(
					input_file=self.files_singletop(channel),
					weight=mc_weight+"*"+weight+"*eventWeight*"+Samples.ttj_genmatch(channel,fakefactor_method=fakefactor_method)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type),
					nick="vvj"
			)
		else:
			log.error("Sample config (VVJ) currently not implemented for channel \"%s\"!" % channel)
		if not kwargs.get("mssm", False):
			Samples._add_bin_corrections(config, "vvj", nick_suffix)

		if not kwargs.get("no_plot", False):
			Samples._add_plot(config, "bkg", "HIST", "F", kwargs.get("color_label_key", "vvj"), nick_suffix)
		return config

	def vv(self, config, channel, category, weight, nick_suffix, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", fakefactor_method=False, **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []

		scale_factor = lumi
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("Dibosons", 1.0)

		data_weight, mc_weight = self.projection(kwargs)
		add_input = partialmethod(Samples._add_input, config=config, folder=self.root_file_folder(channel), scale_factor=lumi, nick_suffix=nick_suffix)
		if channel in ["mt", "et", "tt", "mm"]:
			if self.legacy:
				add_input(
						input_file=self.files_ww(channel),
						weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+self.embedding_ttbarveto_weight(channel),
						nick="vv"
				)
				add_input(
						input_file=self.files_wz(channel),
						weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+self.embedding_ttbarveto_weight(channel),
						nick="vv"
				)
				add_input(
						input_file=self.files_zz(channel),
						weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+self.embedding_ttbarveto_weight(channel),
						nick="vv"
				)
			else:
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
			Samples._add_bin_corrections(config, "vv", nick_suffix)

		if not kwargs.get("no_plot", False):
			Samples._add_plot(config, "bkg", "HIST", "F", kwargs.get("color_label_key", "vv"), nick_suffix)
		return config

	################higgs files###########################
	def files_qqh(self, channel, mass=125, **kwargs):
		cp = kwargs.get("cp", None)
		state = kwargs.get("state", None)
		if state == "initialState":
			if cp is None or cp =="cpeven":
				#CAUTION: If necessary the mc-generator nick might need to be updated from time to time. added v2 to this, if mc_campaign changes change this as well
				return self.artus_file_names({"process" : "VBFHToTauTau_M"+str(mass), "data": False, "campaign" : self.mc_campaign, "generator" : "powheg-pythia8", "scenario": "PU2017_new_pmx"}, 1)
		elif state == "finalState":
			# return "VBFHToMaxmixTauTauM125_adow_RunIIFall17MiniAODv2_VBFHToTauTauNoSpin_13TeV_USER_powheg-pythia8/*.root"
			return "VBFHToTauTauUncorrelatedDecayFilteredM125_RunIIFall17MiniAODv2_PU2017_13TeV_MINIAOD_powheg-pythia8/*.root"
		else:
			return self.artus_file_names({"process" : "VBFHToTauTau_M"+str(mass), "data": False, "campaign" : self.mc_campaign, "generator" : "powheg-pythia8", "scenario": "PU2017_new_pmx"}, 1)
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

	def files_wh(self, channel, mass=125, **kwargs):
		return "W*HToTauTauUncorrelatedDecayFilteredM125_RunIIFall17MiniAODv2_PU2017_13TeV_MINIAOD_powheg-pythia8/*.root"

	def files_zh(self, channel, mass=125, **kwargs):
		return "ZHToTauTauUncorrelatedDecayFilteredM125_RunIIFall17MiniAODv2_PU2017_13TeV_MINIAOD_powheg-pythia8/*.root"

	def files_ggh(self, channel, mass=125, **kwargs):
		cp = kwargs.get("cp", None)
		generator = kwargs.get("generator", "madgraph")
		state = kwargs.get("state", None);
		if state == "initialState":
			if generator == "madgraph":
				if "sm" in cp:
					return "GluGluToHToTauTauM125_RunIIFall17MiniAODv2_PU2017_13TeV_MINIAOD_amcatnlo-pythia8/*.root GluGluToHToTauTauPlusTwoJetsM125_RunIIFall17MiniAODv2_PU2017_13TeV_MINIAOD_amcatnlo-pythia8/*.root" #FIXME change to total sm
				if "ps" in cp:
					return "GluGluToPseudoscalarHToTauTauM125_dwinterb_RunIIFall17MiniAODv2_GluGluToPseudoscalarHToTauTau_13TeV_USER_amcatnlo-pythia8/*.root GluGluToPseudoscalarHToTauTauPlusTwoJetsM125_RunIIFall17MiniAODv2_PU2017_13TeV_MINIAOD_amcatnlo-pythia8/*.root"
				if "mm" in cp:
					return "GluGluToMaxmixHToTauTauM125_dwinterb_RunIIFall17MiniAODv2_GluGluToMaxmixHToTauTau_13TeV_USER_amcatnlo-pythia8/*.root GluGluToMaxmixHToTauTauPlusTwoJetsM125_RunIIFall17MiniAODv2_PU2017_13TeV_MINIAOD_amcatnlo-pythia8/*.root"
		elif state == "finalState":
			# return "GluGluHToPseudoscalarTauTauM125_adow_RunIIFall17MiniAODv2_GluGluToHToTauTauNoSpin_13TeV_USER_powheg-pythia8/*.root"
			return "GluGluHToTauTauUncorrelatedDecayFilteredM125_RunIIFall17MiniAODv2_PU2017_13TeV_MINIAOD_powheg-pythia8/*.root"

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
				return self.artus_file_names({"process" : "GluGluHToTauTau_M"+str(mass), "data": False, "campaign" : self.mc_campaign, "generator" : "powheg-pythia8", "scenario": "PU2017_new_pmx"}, 1)

	def files_vv(self, channel):
		return None

	def qcd_prefit(self, config, channel, category, weight, nick_suffix, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", estimationMethod="classic", controlregions=False,**kwargs):
		if exclude_cuts is None:
			exclude_cuts = []

		zmm_cr_factor = kwargs.get("zmm_cr_factor", "(1.0)")

		scale_factor = 1.0
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("QCD", 1.0)

		data_weight, mc_weight = self.projection(kwargs)

		cut_type_B = cut_type + "SameSignRegion"
		exclude_cuts_B = copy.deepcopy(exclude_cuts)+["os"]

		shape_weight = data_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_B, cut_type=cut_type_B)
		add_input = partialmethod(Samples._add_input, config=config, folder=self.root_file_folder(channel), scale_factor=lumi, nick_suffix=nick_suffix)
		if channel in ["et", "mt"]:
			add_input(
					input_file=self.files_data(channel),
					scale_factor=1.0,
					weight=shape_weight,
					nick="qcd_prefit"
			)
			add_input(
					input_file=self.files_data(channel),
					scale_factor=1.0,
					weight=shape_weight,
					nick="noplot_data_qcd_yield"
			)
			add_input(
					input_file=self.files_data(channel),
					scale_factor=1.0,
					weight=shape_weight,
					nick="noplot_data_qcd_control"
			)
			add_input(
					input_file=self.files_wj(channel),
					weight=mc_weight+"*"+weight+"*eventWeight*"+self.wj_stitchingweight()+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_B, cut_type=cut_type_B)+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
					nick="noplot_wj_mc_qcd_control"
			)
			if (not kwargs.get("no_ewk_samples", False)):
				add_input(
						input_file=self.files_ewkwm(channel),
						weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_B, cut_type=cut_type_B)+"*"+self.ewkwm_stitchingweight(),
						nick="noplot_wj_mc_qcd_control"
				)
				add_input(
						input_file=self.files_ewkwp(channel),
						weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_B, cut_type=cut_type_B)+"*"+self.ewkwp_stitchingweight(),
						nick="noplot_wj_mc_qcd_control"
				)
			add_input(
					input_file=self.files_ztt(channel, embedding=self.embedding),
					weight=Samples.ztt_genmatch(channel, embedding=self.embedding)+"*"+self.get_weights_ztt(channel=channel,cut_type=cut_type,weight=weight,embedding=self.embedding)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_B, cut_type=cut_type_B)+"*zPtReweightWeight"+"*"+zmm_cr_factor+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
					scale_factor = 1.0 if self.embedding else lumi,
					nick="noplot_ztt_mc_qcd_control"
			)
			if not (kwargs.get("no_ewk_samples", False) or kwargs.get("no_ewkz_as_dy", False) or self.embedding):
				add_input(
						input_file=self.files_ewkz_zll(channel),
						weight=Samples.ztt_genmatch(channel)+"*"+self.get_weights_ztt(channel=channel,cut_type=cut_type,weight=weight,doStitching=False)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_B, cut_type=cut_type_B)+"*"+self.ewkz_zll_stitchingweight()+"*"+zmm_cr_factor+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
						nick="noplot_ztt_mc_qcd_control"
				)
				add_input(
						input_file=self.files_ewkz_znn(channel),
						weight=Samples.ztt_genmatch(channel)+"*"+self.get_weights_ztt(channel=channel,cut_type=cut_type,weight=weight,doStitching=False)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_B, cut_type=cut_type_B)+"*"+self.ewkz_znn_stitchingweight()+"*"+zmm_cr_factor+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
						nick="noplot_ztt_mc_qcd_control"
				)
			add_input(
					input_file=self.files_zll(channel),
					weight=mc_weight+"*"+weight+"*eventWeight*"+self.zll_stitchingweight()+"*"+Samples.zll_genmatch(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_B, cut_type=cut_type_B)+"*zPtReweightWeight"+"*"+self.zll_zl_shape_weight(channel, cut_type)+"*"+zmm_cr_factor+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
					nick="noplot_zll_qcd_control"
			)
			if not (kwargs.get("no_ewk_samples", False) or kwargs.get("no_ewkz_as_dy", False)):
				add_input(
						input_file=self.files_ewkz_zll(channel),
						weight=mc_weight+"*"+weight+"*eventWeight*"+Samples.zll_genmatch(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_B, cut_type=cut_type_B)+"*"+self.zll_zl_shape_weight(channel, cut_type)+"*"+self.ewkz_zll_stitchingweight()+"*"+zmm_cr_factor+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
						nick="noplot_zll_qcd_control"
				)
				add_input(
						input_file=self.files_ewkz_znn(channel),
						weight=mc_weight+"*"+weight+"*eventWeight*"+Samples.zll_genmatch(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_B, cut_type=cut_type_B)+"*"+self.zll_zl_shape_weight(channel, cut_type)+"*"+self.ewkz_znn_stitchingweight()+"*"+zmm_cr_factor+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
						nick="noplot_zll_qcd_control",
				)
			if (not kwargs.get("no_ewk_samples", False)) and kwargs.get("no_ewkz_as_dy", False):
				add_input(
						input_file=self.files_ewkz_zll(channel),
						weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_B, cut_type=cut_type_B)+"*"+self.ewkz_zll_stitchingweight()+"*"+zmm_cr_factor+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
						nick="noplot_ewkz_qcd_control"
				)
				add_input(
						input_file=self.files_ewkz_znn(channel),
						weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_B, cut_type=cut_type_B)+"*"+self.ewkz_znn_stitchingweight()+"*"+zmm_cr_factor+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
						nick="noplot_ewkz_qcd_control"
				)

			add_input(
					input_file=self.files_ttj(channel),
					weight=mc_weight+"*"+weight+"*eventWeight*"+self.embedding_ttbarveto_weight(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_B, cut_type=cut_type_B)+"*topPtReweightWeight"+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
					nick="noplot_ttj_qcd_control"
			)
			if self.legacy:
				add_input(
						input_file=self.files_ww(channel),
						weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_B, cut_type=cut_type_B)+"*"+self.embedding_ttbarveto_weight(channel),
						nick="noplot_vv_qcd_control"
				)
				add_input(
						input_file=self.files_wz(channel),
						weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_B, cut_type=cut_type_B)+"*"+self.embedding_ttbarveto_weight(channel),
						nick="noplot_vv_qcd_control"
				)
				add_input(
						input_file=self.files_zz(channel),
						weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_B, cut_type=cut_type_B)+"*"+self.embedding_ttbarveto_weight(channel),
						nick="noplot_vv_qcd_control"
				)
			else:
				add_input(
						input_file=self.files_wwtolnuqq(channel),
						weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_B, cut_type=cut_type_B)+"*"+self.embedding_ttbarveto_weight(channel)+"*"+self.wwtolnuqq_stitchingweight(),
						nick="noplot_vv_qcd_control"
				)
				add_input(
						input_file=self.files_wwto4q(channel),
						weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_B, cut_type=cut_type_B)+"*"+self.embedding_ttbarveto_weight(channel),
						nick="noplot_vv_qcd_control"
				)
				add_input(
						input_file=self.files_wzto1l3nu(channel),
						weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_B, cut_type=cut_type_B)+"*"+self.embedding_ttbarveto_weight(channel),
						nick="noplot_vv_qcd_control"
				)
				add_input(
						input_file=self.files_wzto3lnu(channel),
						weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_B, cut_type=cut_type_B)+"*"+self.embedding_ttbarveto_weight(channel),
						nick="noplot_vv_qcd_control"
				)
				add_input(
						input_file=self.files_zzto2l2nu(channel),
						weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_B, cut_type=cut_type_B)+"*"+self.embedding_ttbarveto_weight(channel),
						nick="noplot_vv_qcd_control"
				)
				add_input(
						input_file=self.files_zzto4l(channel),
						weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_B, cut_type=cut_type_B)+"*"+self.embedding_ttbarveto_weight(channel)+"*"+self.zzto4l_stitchingweight(),
						nick="noplot_vv_qcd_control"
				)
				add_input(
						input_file=self.files_singletop(channel),
						weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_B, cut_type=cut_type_B),
						nick="noplot_vv_qcd_control"
			)
			# add_input(
			# 		input_file=self.files_vv(channel),
			# 		weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_B, cut_type=cut_type_B)+"*"+self.vv_stitchingweight()+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
			# 		nick="noplot_vv_qcd_control"
			# )
			# add_input(
			# 		input_file=self.files_diboson(channel),
			# 		weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_B, cut_type=cut_type_B)+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
			# 		nick="noplot_vv_qcd_control"
			# )

			if not "EstimateQcdPrefit" in config.get("analysis_modules", []):
				config.setdefault("analysis_modules", []).append("EstimateQcdPrefit")
			config.setdefault("qcd_shape_nicks", []).append("qcd_prefit"+nick_suffix)
			config.setdefault("qcd_yield_nicks", []).append("noplot_data_qcd_yield"+nick_suffix)
			if (not kwargs.get("no_ewk_samples", False)) and kwargs.get("no_ewkz_as_dy", False):
				config.setdefault("qcd_yield_subtract_nicks", []).append(" ".join([nick+nick_suffix for nick in "noplot_ztt_mc_qcd_control noplot_zll_qcd_control noplot_ewkz_qcd_control noplot_ttj_qcd_control noplot_vv_qcd_control noplot_wj_mc_qcd_control".split()]))
				config.setdefault("qcd_shape_subtract_nicks", []).append(" ".join([nick+nick_suffix for nick in "noplot_ztt_mc_qcd_control noplot_zll_qcd_control noplot_ewkz_qcd_control noplot_ttj_qcd_control noplot_vv_qcd_control noplot_wj_mc_qcd_control".split()]))
			else:
				config.setdefault("qcd_yield_subtract_nicks", []).append(" ".join([nick+nick_suffix for nick in "noplot_ztt_mc_qcd_control noplot_zll_qcd_control noplot_ttj_qcd_control noplot_vv_qcd_control noplot_wj_mc_qcd_control".split()]))
				config.setdefault("qcd_shape_subtract_nicks", []).append(" ".join([nick+nick_suffix for nick in "noplot_ztt_mc_qcd_control noplot_zll_qcd_control noplot_ttj_qcd_control noplot_vv_qcd_control noplot_wj_mc_qcd_control".split()]))
			if channel == "em" or channel == "ttbar":
				config.setdefault("qcd_extrapolation_factors_ss_os", []).append(1.0)
			elif channel == "et":
				config.setdefault("qcd_extrapolation_factors_ss_os", []).append(1.0)
			elif channel == "mt":
				config.setdefault("qcd_extrapolation_factors_ss_os", []).append(1.0)
			else:
				config.setdefault("qcd_extrapolation_factors_ss_os", []).append(1.0)

		else:
			log.error("Sample config (QCD) currently not implemented for channel \"%s\"!" % channel)

		if not kwargs.get("no_plot", False):
			if not kwargs.get("mssm", False):
				Samples._add_bin_corrections(config, "qcd_prefit", nick_suffix)
			Samples._add_plot(config, "bkg", "HIST", "F", "qcd_prefit", nick_suffix)
		return config

	def qcd(self, config, channel, category, weight, nick_suffix, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", estimationMethod="classic", controlregions=False,**kwargs):

		if channel== "mt":
			ss_os_factor = 1.218 #TODO for 2017
		elif channel == "et":
			ss_os_factor = 1.361 #TODO for 2017
		else:
			ss_os_factor = 0.0

		"""
		Using ABCD method in background-method types 'new' and 'simeqn'
		A := Signal region / os+low_mt
		B := SS Control region / ss+low_mt
		C := High mt SS region / ss+high_mt
		D := High mt OS region / ss+low_mt
		As this method is entangled with the wj function some nicks will be defined there and taken from there.
		See the analysis modules for details.
		"""
		if exclude_cuts is None:
			exclude_cuts = []

		zmm_cr_factor = kwargs.get("zmm_cr_factor", "(1.0)")

		scale_factor = 1.0
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("QCD", 1.0)

		data_weight, mc_weight = self.projection(kwargs)
		add_input = partialmethod(Samples._add_input, config=config, folder=self.root_file_folder(channel), scale_factor=lumi, nick_suffix=nick_suffix)

		# Same-sign region cut type
		cut_type_A = cut_type
		cut_type_B = cut_type + "SameSignRegion"
		cut_type_C = cut_type + "highMtSSControlRegionWJ"
		cut_type_D = cut_type + "highMtControlRegionWJ"

		exclude_cuts_A = exclude_cuts
		exclude_cuts_B = copy.deepcopy(exclude_cuts)+["os"]
		exclude_cuts_D = copy.deepcopy(exclude_cuts)#+["mt"]
		exclude_cuts_C = copy.deepcopy(exclude_cuts_D)+["os"]
		exclude_cuts_inclusive = copy.deepcopy(exclude_cuts)+["mt"]
		exclude_cuts_inclusive_ss = copy.deepcopy(exclude_cuts_inclusive)+["os"]

		if channel in ["et", "mt", "em", "tt", "mm", "ee", "ttbar"]:
			# background estimation in et/mt
			if ("new" in estimationMethod or "simeqn" in estimationMethod) and channel in  ["et", "mt"]:
				shape_weight = data_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_A, cut_type=cut_type_A)
				# qcd shape nick
				add_input(
					input_file=self.files_data(channel),
					scale_factor=1.0,
					weight=data_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_B , cut_type=cut_type_B),
					nick="qcd"
				)
				# qcd data yield nick (for subtraction)
				add_input(
						input_file=self.files_data(channel),
						scale_factor=1.0,
						weight=data_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_B, cut_type=cut_type_B),
						nick=("noplot_" if not controlregions else "") + "data_qcd_yield",
				)
				add_input(
						input_file=self.files_data(channel),
						scale_factor=1.0,
						weight=data_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_B, cut_type=cut_type_B),
						nick=("noplot_" if not controlregions else "") + "qcd_ss_lowmt",
				)
				add_input(
						input_file=self.files_data(channel),
						scale_factor=1.0,
						weight=data_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_D, cut_type=cut_type_D),
						nick=("noplot_" if not controlregions else "") + "qcd_os_highmt",
				)
				# background subtraction nicks in region B
				add_input(
						input_file=self.files_ztt(channel, embedding=self.embedding),
						weight=Samples.ztt_genmatch(channel, embedding=self.embedding)+"*"+self.get_weights_ztt(channel=channel,cut_type=cut_type + ("_emb" if self.embedding else ""),weight=weight,embedding=self.embedding)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_B, cut_type=cut_type_B + ("_emb" if self.embedding else ""))+"*zPtReweightWeight"+"*"+zmm_cr_factor+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type + ("_emb" if self.embedding else "")),
						scale_factor = 1.0 if self.embedding else lumi,
						nick=("noplot_" if not controlregions else "") + "ztt_ss_qcd"
				)
				if not (kwargs.get("no_ewk_samples", False) or kwargs.get("no_ewkz_as_dy", False) or self.embedding):
					add_input(
							input_file=self.files_ewkz_zll(channel),
							weight=Samples.ztt_genmatch(channel)+"*"+self.get_weights_ztt(channel=channel,cut_type=cut_type,weight=weight,doStitching=False)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_B, cut_type=cut_type_B)+"*"+self.ewkz_zll_stitchingweight()+"*"+zmm_cr_factor+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
							nick=("noplot_" if not controlregions else "") + "ztt_ss_qcd",
					)
					add_input(
							input_file=self.files_ewkz_znn(channel),
							weight=Samples.ztt_genmatch(channel)+"*"+self.get_weights_ztt(channel=channel,cut_type=cut_type,weight=weight,doStitching=False)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_B, cut_type=cut_type_B)+"*"+self.ewkz_znn_stitchingweight()+"*"+zmm_cr_factor+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
							nick=("noplot_" if not controlregions else "") + "ztt_ss_qcd",
					)
				add_input(
						input_file=self.files_zll(channel),
						weight=mc_weight+"*"+weight+"*eventWeight*"+self.zll_stitchingweight()+"*"+Samples.zll_genmatch(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_B, cut_type=cut_type_B)+"*zPtReweightWeight"+"*"+self.zll_zl_shape_weight(channel, cut_type)+"*"+zmm_cr_factor+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
						nick=("noplot_" if not controlregions else "") + "zll_ss_qcd",
				)
				if not (kwargs.get("no_ewk_samples", False)):
					add_input(
							input_file=self.files_ewkz_zll(channel),
							weight=mc_weight+"*"+weight+"*eventWeight*"+Samples.zll_genmatch(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_B, cut_type=cut_type_B)+"*"+self.zll_zl_shape_weight(channel, cut_type)+"*"+self.ewkz_zll_stitchingweight()+"*"+zmm_cr_factor+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
							nick=("noplot_" if not controlregions else "") + "zll_ss_qcd",
					)
					add_input(
							input_file=self.files_ewkz_znn(channel),
							weight=mc_weight+"*"+weight+"*eventWeight*"+Samples.zll_genmatch(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_B, cut_type=cut_type_B)+"*"+self.zll_zl_shape_weight(channel, cut_type)+"*"+self.ewkz_znn_stitchingweight()+"*"+zmm_cr_factor+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
							nick=("noplot_" if not controlregions else "") + "zll_ss_qcd",
					)
				if (not kwargs.get("no_ewk_samples", False)) and kwargs.get("no_ewkz_as_dy", False):
					add_input(
							input_file=self.files_ewkz_zll(channel),
							weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_B, cut_type=cut_type_B)+"*"+self.ewkz_zll_stitchingweight()+"*"+zmm_cr_factor+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
							nick=("noplot_" if not controlregions else "") + "ewkz_ss_qcd"
					)
					add_input(
							input_file=self.files_ewkz_znn(channel),
							weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_B, cut_type=cut_type_B)+"*"+self.ewkz_znn_stitchingweight()+"*"+zmm_cr_factor+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
							nick=("noplot_" if not controlregions else "") + "ewkz_ss_qcd"
					)
				add_input(
						input_file=self.files_ttj(channel),
						weight=mc_weight+"*"+weight+"*eventWeight*"+self.embedding_ttbarveto_weight(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_B, cut_type=cut_type_B)+"*topPtReweightWeight"+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
						nick=("noplot_" if not controlregions else "") + "ttj_ss_qcd",
				)
				if self.legacy:
					add_input(
							input_file=self.files_ww(channel),
							weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_B, cut_type=cut_type_B)+"*"+self.embedding_ttbarveto_weight(channel),
							nick=("noplot_" if not controlregions else "") + "vv_ss_qcd"
					)
					add_input(
							input_file=self.files_wz(channel),
							weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_B, cut_type=cut_type_B)+"*"+self.embedding_ttbarveto_weight(channel),
							nick=("noplot_" if not controlregions else "") + "vv_ss_qcd"
					)
					add_input(
							input_file=self.files_zz(channel),
							weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_B, cut_type=cut_type_B)+"*"+self.embedding_ttbarveto_weight(channel),
							nick=("noplot_" if not controlregions else "") + "vv_ss_qcd"
					)
				else:
					add_input(
							input_file=self.files_wwtolnuqq(channel),
							weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_B, cut_type=cut_type_B)+"*"+self.embedding_ttbarveto_weight(channel)+"*"+self.wwtolnuqq_stitchingweight(),
							nick=("noplot_" if not controlregions else "") + "vv_ss_qcd"
					)
					add_input(
							input_file=self.files_wwto4q(channel),
							weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_B, cut_type=cut_type_B)+"*"+self.embedding_ttbarveto_weight(channel),
							nick=("noplot_" if not controlregions else "") + "vv_ss_qcd"
					)
					add_input(
							input_file=self.files_wzto1l3nu(channel),
							weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_B, cut_type=cut_type_B)+"*"+self.embedding_ttbarveto_weight(channel),
							nick=("noplot_" if not controlregions else "") + "vv_ss_qcd"
					)
					add_input(
							input_file=self.files_wzto3lnu(channel),
							weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_B, cut_type=cut_type_B)+"*"+self.embedding_ttbarveto_weight(channel),
							nick=("noplot_" if not controlregions else "") + "vv_ss_qcd"
					)
					add_input(
							input_file=self.files_zzto2l2nu(channel),
							weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_B, cut_type=cut_type_B)+"*"+self.embedding_ttbarveto_weight(channel),
							nick=("noplot_" if not controlregions else "") + "vv_ss_qcd"
					)
					add_input(
							input_file=self.files_zzto4l(channel),
							weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_B, cut_type=cut_type_B)+"*"+self.embedding_ttbarveto_weight(channel)+"*"+self.zzto4l_stitchingweight(),
							nick=("noplot_" if not controlregions else "") + "vv_ss_qcd"
					)
				add_input(
						input_file=self.files_singletop(channel),
						weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_B, cut_type=cut_type_B),
						nick=("noplot_" if not controlregions else "") + "vv_ss_qcd"
				)
				# add_input(
				# 		input_file=self.files_vv(channel),
				# 		weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_B, cut_type=cut_type_B)+"*"+self.vv_stitchingweight()+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
				# 		nick=("noplot_" if not controlregions else "") + "vv_ss_qcd",
				# )
				# add_input(
				# 		input_file=self.files_diboson(channel),
				# 		weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel,exclude_cuts=exclude_cuts_B, cut_type=cut_type_B)+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
				# 		nick=("noplot_" if not controlregions else "") + "vv_ss_qcd",
				# )
				add_input(
						input_file=self.files_data(channel),
						scale_factor=1.0,
						weight=data_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_C, cut_type=cut_type_C),
						nick=("noplot_" if not controlregions else "") + "qcd_ss_highmt"
				)
				if "new" in estimationMethod:
					if kwargs.get("useRelaxedIsolationForQCD", False):
						cut_type_A = cut_type_A + "relaxedETauMuTauWJ"
					elif category != None:
						cut_type_A = cut_type_A + ("relaxedETauMuTauWJ" if ("1jet" in category or "vbf" in category or "Boosted2D" in category or "Vbf2D" in category or "dijet" in category) else "")
					add_input(
						input_file=self.files_wj(channel),
						weight=mc_weight+"*"+weight+"*eventWeight*"+self.wj_stitchingweight()+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_B , cut_type=cut_type_B),
						nick=("noplot_" if not controlregions else "") + "wj_ss_qcd"
					)
					if (not kwargs.get("no_ewk_samples", False)):
						add_input(
							input_file=self.files_ewkwm(channel),
							weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_B , cut_type=cut_type_B)+"*"+self.ewkwm_stitchingweight(),
							nick=("noplot_" if not controlregions else "") + "wj_ss_qcd"
						)
						add_input(
							input_file=self.files_ewkwp(channel),
							weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_B , cut_type=cut_type_B)+"*"+self.ewkwp_stitchingweight(),
							nick=("noplot_" if not controlregions else "") + "wj_ss_qcd"
						)
					if kwargs.get("ss_os_factor", 0.0) != 0.0:
						ss_os_factor = kwargs["ss_os_factor"]
					else:
						ss_os_factor = 1.00
						if category != None:
							if channel == "et":
								ss_os_factor =  1.28 if "Boosted2D" in category else 1.0 if "Vbf2D" in category else 1.0 if "ZeroJet2D" in category else 1.00
							elif channel == "mt":
								ss_os_factor =  1.06 if "Boosted2D" in category else 1.0 if "Vbf2D" in category else 1.07 if "ZeroJet2D" in category else 1.00
					if not "EstimateWjetsAndQCD" in config.get("analysis_modules", []):
						config.setdefault("analysis_modules", []).append("EstimateWjetsAndQCD")
						config.setdefault("qcd_extrapolation_factors_ss_os", []).append(ss_os_factor)

					if controlregions:
						config.setdefault("qcd_shape_nicks", []).append("qcd"+nick_suffix)
						config.setdefault("qcd_yield_nicks", []).append("data_qcd_yield"+nick_suffix)
						if (not kwargs.get("no_ewk_samples", False)) and kwargs.get("no_ewkz_as_dy", False):
							config.setdefault("B_substract_nicks", []).append(" ".join([nick+nick_suffix for nick in "ztt_ss_qcd zll_ss_qcd ewkz_ss_qcd ttj_ss_qcd vv_ss_qcd wj_ss_qcd".split()]))
						else:
							config.setdefault("B_substract_nicks", []).append(" ".join([nick+nick_suffix for nick in "ztt_ss_qcd zll_ss_qcd ttj_ss_qcd vv_ss_qcd wj_ss_qcd".split()]))
						config.setdefault("qcd_ss_highmt_shape_nicks", []).append("qcd_ss_highmt"+nick_suffix)
						config.setdefault("qcd_ss_lowmt_nicks", []).append("qcd_ss_lowmt"+nick_suffix)
						config.setdefault("qcd_os_highmt_nicks", []).append("qcd_os_highmt"+nick_suffix)
						if kwargs.get("wj_sf_shift", 0.0) != 0.0:
							config.setdefault("wjets_scale_factor_shifts", []).append(kwargs["wj_sf_shift"])
						for nick in ["ztt_ss_lowmt", "zll_ss_lowmt", "ttj_ss_lowmt", "vv_ss_lowmt", "wj_ss_lowmt","data_ss_lowmt", "qcd_ss_highmt", "qcd_os_highmt", "qcd_ss_lowmt"]+(["ewkz_ss_lowmt"] if (not kwargs.get("no_ewk_samples", False) and kwargs.get("no_ewkz_as_dy", False)) else []):
							if not kwargs.get("mssm", False):
								Samples._add_bin_corrections(config, nick, nick_suffix)
							Samples._add_plot(config, "bkg", "HIST", "F", nick, nick_suffix)
					else:
						config.setdefault("qcd_shape_nicks", []).append("qcd"+nick_suffix)
						config.setdefault("qcd_yield_nicks", []).append("noplot_data_qcd_yield"+nick_suffix)
						if (not kwargs.get("no_ewk_samples", False)) and kwargs.get("no_ewkz_as_dy", False):
							config.setdefault("B_substract_nicks", []).append(" ".join([nick+nick_suffix for nick in "noplot_ztt_ss_qcd noplot_zll_ss_qcd noplot_ewkz_ss_qcd noplot_ttj_ss_qcd noplot_vv_ss_qcd noplot_wj_ss_qcd".split()]))
						else:
							config.setdefault("B_substract_nicks", []).append(" ".join([nick+nick_suffix for nick in "noplot_ztt_ss_qcd noplot_zll_ss_qcd noplot_ttj_ss_qcd noplot_vv_ss_qcd noplot_wj_ss_qcd".split()]))
						config.setdefault("qcd_ss_highmt_shape_nicks", []).append("noplot_qcd_ss_highmt"+nick_suffix)
						config.setdefault("qcd_ss_lowmt_nicks", []).append("noplot_qcd_ss_lowmt"+nick_suffix)
						config.setdefault("qcd_os_highmt_nicks", []).append("noplot_qcd_os_highmt"+nick_suffix)
						if kwargs.get("wj_sf_shift", 0.0) != 0.0:
							config.setdefault("wjets_scale_factor_shifts", []).append(kwargs["wj_sf_shift"])
				if "simeqn" in estimationMethod:
					if kwargs.get("ss_os_factor", 0.0) != 0.0:
						ss_os_factor = kwargs["ss_os_factor"]
					else:
						ss_os_factor = 1.0
						if category != None:
							if channel == "et":
								ss_os_factor = 1.61 if "BoostedCP" in category else 0.97 if "ZeroJetCP" in category else 1.82 if "dijet2D" in category else 1.0
							elif channel == "mt":
								ss_os_factor = 1.18 if "BoostedCP" in category else 1.15 if "ZeroJetCP" in category else 1.24 if "dijet2D" in category else 1.0
					use_inclusive_wjets_mc = False
					if category != None:
						use_inclusive_wjets_mc = True if "dijet2D" in category else False

					if not "EstimateWjetsAndQCDSimEquationMethod" in config.get("analysis_modules", []):
						config.setdefault("analysis_modules", []).append("EstimateWjetsAndQCDSimEquationMethod")
					config.setdefault("qcd_extrapolation_factors_ss_os", []).append(ss_os_factor)
					config.setdefault("use_inclusive_wjets_mc", []).append(use_inclusive_wjets_mc)

					if controlregions:
						config.setdefault("B_subtract_nicks", []).append(" ".join([nick+nick_suffix for nick in "ztt_ss_qcd zll_ss_qcd ttj_ss_qcd vv_ss_qcd".split()]))
						config.setdefault("qcd_os_highmt_nicks", []).append("qcd_os_highmt"+nick_suffix)
						config.setdefault("qcd_ss_highmt_nicks", []).append("qcd_ss_highmt"+nick_suffix)
						config.setdefault("qcd_ss_lowmt_nicks", []).append("qcd_ss_lowmt"+nick_suffix)
						config.setdefault("qcd_ss_data_nicks", []).append("data_qcd_yield"+nick_suffix)
						config.setdefault("qcd_shape_nicks", []).append("qcd"+nick_suffix)
						for nick in ["ztt_ss_qcd", "zll_ss_qcd", "ttj_ss_qcd", "vv_ss_qcd", "qcd_ss_highmt", "qcd_ss_lowmt"]:
							if not kwargs.get("mssm", False):
								Samples._add_bin_corrections(config, nick, nick_suffix)
							Samples._add_plot(config, "bkg", "HIST", "F", nick, nick_suffix)
						for nick in ["data_qcd_yield"]:
							if not kwargs.get("mssm", False):
								Samples._add_bin_corrections(config, nick, nick_suffix)
							Samples._add_plot(config, "data", "E", "ELP", nick, nick_suffix)
					else:
						config.setdefault("qcd_shape_nicks", []).append("qcd"+nick_suffix)
						config.setdefault("qcd_ss_data_nicks", []).append("noplot_data_qcd_yield"+nick_suffix)
						config.setdefault("qcd_ss_lowmt_nicks", []).append("noplot_qcd_ss_lowmt"+nick_suffix)
						config.setdefault("qcd_os_highmt_nicks", []).append("noplot_qcd_os_highmt"+nick_suffix)
						config.setdefault("qcd_ss_highmt_nicks", []).append("noplot_qcd_ss_highmt"+nick_suffix)
						config.setdefault("B_subtract_nicks", []).append(" ".join(["noplot_"+nick+nick_suffix for nick in "ztt_ss_qcd zll_ss_qcd ttj_ss_qcd vv_ss_qcd ".split()]))
			elif ("new" in estimationMethod or "simeqn" in estimationMethod) and channel not in  ["et", "mt"]:
				if channel == "em" or channel == "ttbar":
					# in the em channel QCD is estimated from SS events in data
					# in the SM analysis a constant QCD OSSS factor is measured in anti-isolated lepton events.
					# in the CP analysis event weights in bins of njets, dR and pt where determined.
					if kwargs.get("ss_os_factor", 0.0) != 0.0:
						ss_os_factor = kwargs["ss_os_factor"]
					else:
						ss_os_factor = 2.22
						if category != None:
							ss_os_factor = 2.27 if "ZeroJet2D" in category else 2.26 if "Boosted2D" in category else 2.84 if "Vbf2D" in category else 2.22

					# determine the weight to be used
					em_qcd_event_weight = "emuQcdWeightNom" # if not any(CP_category in category for CP_category in ["ZeroJetCP", "BoostedCP", "dijet2D_lowboost", "dijet2D_boosted"]) else "emuQcdOsssWeight"
					for estimation_type in ["shape", "yield"]:
						qcd_weight = weight
						qcd_exclude_cuts = copy.deepcopy(exclude_cuts)+["os"]
						if category != None:
							if estimation_type == "shape" and ("ZeroJet2D" in category or "Boosted2D" in category):
								qcd_weight += "*(iso_1<0.3)*(iso_2>0.1)*(iso_2<0.3)"
								qcd_exclude_cuts += ["iso_1", "iso_2"]
							if estimation_type == "shape" and ("Vbf2D" in category):
								qcd_weight += "*(iso_1<0.5)*(iso_2>0.2)*(iso_2<0.5)"
								qcd_exclude_cuts += ["iso_1", "iso_2"]
						data_sample_weight = make_multiplication([data_weight,
												qcd_weight,
												"eventWeight",
												self._cut_string(channel, exclude_cuts=qcd_exclude_cuts, cut_type=cut_type_B),
												"((q_1*q_2)>0.0)",
												em_qcd_event_weight])
						mc_sample_weight = make_multiplication([mc_weight,
												qcd_weight,
												"eventWeight",
												self._cut_string(channel, exclude_cuts=qcd_exclude_cuts, cut_type=cut_type_B),
												"((q_1*q_2)>0.0)",
												em_qcd_event_weight])
						add_input(
								input_file=self.files_wj(channel),
								weight=mc_sample_weight+"*"+self.wj_stitchingweight()+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
								nick="noplot_wj_"+estimation_type
						)
						if (not kwargs.get("no_ewk_samples", False)):
							add_input(
									input_file=self.files_ewkwm(channel),
									weight=mc_sample_weight+"*"+self.ewkwm_stitchingweight()+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
									nick="noplot_wj_"+estimation_type
							)
							add_input(
									input_file=self.files_ewkwp(channel),
									weight=mc_sample_weight+"*"+self.ewkwp_stitchingweight()+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
									nick="noplot_wj_"+estimation_type
							)
						add_input(
								input_file=self.files_wgamma(channel),
								weight=mc_sample_weight+"*"+self.wgamma_stitchingweight()+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
								nick="noplot_wj_"+estimation_type
						)
						add_input(
								input_file=self.files_wgamma_star(channel),
								weight=mc_sample_weight+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
								nick="noplot_wj_"+estimation_type
						)
						add_input(
								input_file=self.files_data(channel),
								scale_factor=1.0,
								weight=data_sample_weight,
								nick=("qcd" if estimation_type=="shape" else "noplot_qcd_"+estimation_type)
						)
						add_input(
								input_file=self.files_ztt(channel, embedding=self.embedding),
								weight=Samples.ztt_genmatch(channel, embedding=self.embedding)+"*"+self.get_weights_ztt(channel=channel,cut_type=cut_type + ("_emb" if self.embedding else ""),mc_sample_weight=mc_sample_weight,embedding=self.embedding)+"*zPtReweightWeight"+"*"+zmm_cr_factor+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type + ("_emb" if self.embedding else "")),
								scale_factor = 1.0 if self.embedding else lumi,
								nick="noplot_ztt_"+estimation_type
						)
						if not (kwargs.get("no_ewk_samples", False) or kwargs.get("no_ewkz_as_dy", False) or self.embedding):
							add_input(
									input_file=self.files_ewkz_zll(channel),
									weight=Samples.ztt_genmatch(channel)+"*"+self.get_weights_ztt(channel=channel,cut_type=cut_type,mc_sample_weight=mc_sample_weight, doStitching=False)+"*"+self.ewkz_zll_stitchingweight()+"*"+zmm_cr_factor+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
									nick="noplot_ztt_"+estimation_type
							)
							add_input(
									input_file=self.files_ewkz_znn(channel),
									weight=Samples.ztt_genmatch(channel)+"*"+self.get_weights_ztt(channel=channel,cut_type=cut_type,mc_sample_weight=mc_sample_weight, doStitching=False)+"*"+self.ewkz_znn_stitchingweight()+"*"+zmm_cr_factor+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
									nick="noplot_ztt_"+estimation_type
							)
						add_input(
								input_file=self.files_zll(channel),
								weight=self.zll_stitchingweight()+"*"+Samples.zll_genmatch(channel)+"*"+mc_sample_weight+"*zPtReweightWeight"+"*"+self.zll_zl_shape_weight(channel, cut_type)+"*"+zmm_cr_factor+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
								nick="noplot_zll_"+estimation_type
						)
						if not (kwargs.get("no_ewk_samples", False) or kwargs.get("no_ewkz_as_dy", False)):
							add_input(
									input_file=self.files_ewkz_zll(channel),
									weight=Samples.zll_genmatch(channel)+"*"+mc_sample_weight+"*"+self.zll_zl_shape_weight(channel, cut_type)+"*"+self.ewkz_zll_stitchingweight()+"*"+zmm_cr_factor+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
									nick="noplot_zll_"+estimation_type
							)
							add_input(
									input_file=self.files_ewkz_znn(channel),
									weight=Samples.zll_genmatch(channel)+"*"+mc_sample_weight+"*"+self.zll_zl_shape_weight(channel, cut_type)+"*"+self.ewkz_znn_stitchingweight()+"*"+zmm_cr_factor+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
									nick="noplot_zll_"+estimation_type
							)
						if (not kwargs.get("no_ewk_samples", False)) and kwargs.get("no_ewkz_as_dy", False):
							add_input(
									input_file=self.files_ewkz_zll(channel),
									weight=mc_sample_weight+"*"+self.ewkz_zll_stitchingweight()+"*"+zmm_cr_factor+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
									nick="noplot_ewkz_"+estimation_type
							)
							add_input(
									input_file=self.files_ewkz_znn(channel),
									weight=mc_sample_weight+"*"+self.ewkz_znn_stitchingweight()+"*"+zmm_cr_factor+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
									nick="noplot_ewkz_"+estimation_type
							)
						add_input(
								input_file=self.files_ttj(channel),
								weight=mc_sample_weight+"*"+self.embedding_ttbarveto_weight(channel)+"*topPtReweightWeight"+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
								nick="noplot_ttj_"+estimation_type
						)
						if self.legacy:
							add_input(
									input_file=self.files_ww(channel),
									weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+self.embedding_ttbarveto_weight(channel),
									nick="noplot_vv_"+estimation_type
							)
							add_input(
									input_file=self.files_wz(channel),
									weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+self.embedding_ttbarveto_weight(channel),
									nick="noplot_vv_"+estimation_type
							)
							add_input(
									input_file=self.files_zz(channel),
									weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+self.embedding_ttbarveto_weight(channel),
									nick="noplot_vv_"+estimation_type
							)
						else:
							add_input(
									input_file=self.files_wwtolnuqq(channel),
									weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+self.embedding_ttbarveto_weight(channel)+"*"+self.wwtolnuqq_stitchingweight(),
									nick="noplot_vv_"+estimation_type
							)
							add_input(
									input_file=self.files_wwto4q(channel),
									weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+self.embedding_ttbarveto_weight(channel),
									nick="noplot_vv_"+estimation_type
							)
							add_input(
									input_file=self.files_wzto1l3nu(channel),
									weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+self.embedding_ttbarveto_weight(channel),
									nick="noplot_vv_"+estimation_type
							)
							add_input(
									input_file=self.files_wzto3lnu(channel),
									weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+self.embedding_ttbarveto_weight(channel),
									nick="noplot_vv_"+estimation_type
							)
							add_input(
									input_file=self.files_zzto2l2nu(channel),
									weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+self.embedding_ttbarveto_weight(channel),
									nick="noplot_vv_"+estimation_type
							)
							add_input(
									input_file=self.files_zzto4l(channel),
									weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+self.embedding_ttbarveto_weight(channel)+"*"+self.zzto4l_stitchingweight(),
									nick="noplot_vv_"+estimation_type
							)
						add_input(
								input_file=self.files_singletop(channel),
								weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type),
								nick="noplot_vv_"+estimation_type
						)
						# add_input(
						# 		input_file=self.files_vv(channel),
						# 		weight=mc_sample_weight+"*"+self.vv_stitchingweight()+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
						# 		nick="noplot_vv_"+estimation_type
						# )
						# add_input(
						# 		input_file=self.files_diboson(channel),
						# 		weight=mc_sample_weight+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
						# 		nick="noplot_vv_"+estimation_type
						# )
					if not "EstimateQcd" in config.get("analysis_modules", []):
						config.setdefault("analysis_modules", []).append("EstimateQcd")
					config.setdefault("qcd_shape_nicks", []).append("qcd"+nick_suffix)
					config.setdefault("qcd_yield_nicks", []).append("noplot_qcd_yield"+nick_suffix)
					if (not kwargs.get("no_ewk_samples", False)) and kwargs.get("no_ewkz_as_dy", False):
						config.setdefault("qcd_yield_subtract_nicks", []).append(" ".join(["noplot_"+nick+"_yield"+nick_suffix for nick in "ztt zll ewkz ttj vv wj".split()]))
						config.setdefault("qcd_shape_subtract_nicks", []).append(" ".join(["noplot_"+nick+"_shape"+nick_suffix for nick in "ztt zll ewkz ttj vv wj".split()]))
					else:
						config.setdefault("qcd_yield_subtract_nicks", []).append(" ".join(["noplot_"+nick+"_yield"+nick_suffix for nick in "ztt zll ttj vv wj".split()]))
						config.setdefault("qcd_shape_subtract_nicks", []).append(" ".join(["noplot_"+nick+"_shape"+nick_suffix for nick in "ztt zll ttj vv wj".split()]))
					config.setdefault("qcd_extrapolation_factors_ss_os", []).append(ss_os_factor)
				if channel == "tt":
					if cut_type == "cptautau2017legacy":
						isolationDefinition = "((byLooseDeepTau2017v2p1VSjet_1 > 0.5 && byVVLooseDeepTau2017v2p1VSjet_2 > 0.5 && byMediumDeepTau2017v2p1VSjet_2 < 0.5) || (byLooseDeepTau2017v2p1VSjet_2 > 0.5 && byVVLooseDeepTau2017v2p1VSjet_1 > 0.5 && byMediumDeepTau2017v2p1VSjet_1 < 0.5))"
					elif cut_type == "baseline2016":
						isolationDefinition = "((byMediumIsolationMVArun2v1DBoldDMwLT_1 > 0.5 && byLooseIsolationMVArun2v1DBoldDMwLT_2 > 0.5 && byTightIsolationMVArun2v1DBoldDMwLT_2 < 0.5) || (byMediumIsolationMVArun2v1DBoldDMwLT_2 > 0.5 && byLooseIsolationMVArun2v1DBoldDMwLT_1 > 0.5 && byTightIsolationMVArun2v1DBoldDMwLT_1 < 0.5))"
					elif cut_type == "smhtt2016":  #TODO or cut_type == "cpggh2016"?
						isolationDefinition = "((byMediumIsolationMVArun2v1DBoldDMwLT_1 > 0.5 && byLooseIsolationMVArun2v1DBoldDMwLT_2 > 0.5 && byTightIsolationMVArun2v1DBoldDMwLT_2 < 0.5) || (byMediumIsolationMVArun2v1DBoldDMwLT_2 > 0.5 && byLooseIsolationMVArun2v1DBoldDMwLT_1 > 0.5 && byTightIsolationMVArun2v1DBoldDMwLT_1 < 0.5))*((gen_match_1 == 5)*0.95 + (gen_match_1 != 5))*((gen_match_2 == 5)*0.95 + (gen_match_2 != 5))"
					else:
						isolationDefinition = "(byMediumIsolationMVArun2v1DBoldDMwLT_1 > 0.5 && byLooseIsolationMVArun2v1DBoldDMwLT_2 > 0.5 && byVTightIsolationMVArun2v1DBoldDMwLT_2 < 0.5)"
					data_selection_weights = {
						"qcd_shape" : data_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["iso_1", "iso_2"], cut_type=cut_type)+"*"+isolationDefinition,
						"qcd_signal_ss" : data_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_B , cut_type=cut_type)+"*((q_1*q_2)>0.0)",
						"qcd_relaxed_ss" : data_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os", "iso_1", "iso_2"], cut_type=cut_type)+"*((q_1*q_2)>0.0)"+"*"+isolationDefinition
						}
					mc_selection_weights = {
						"qcd_shape" : mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["iso_1", "iso_2"], cut_type=cut_type)+"*"+isolationDefinition,
						"qcd_signal_ss" : mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_B , cut_type=cut_type)+"*((q_1*q_2)>0.0)",
						"qcd_relaxed_ss" : mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os", "iso_1", "iso_2"], cut_type=cut_type)+"*((q_1*q_2)>0.0)"+"*"+isolationDefinition
						}
					emb_selection_weights = {
						"qcd_shape" : mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["iso_1", "iso_2"], cut_type=cut_type + "_emb")+"*"+isolationDefinition,
						"qcd_signal_ss" : mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_B , cut_type=cut_type + "_emb")+"*((q_1*q_2)>0.0)",
						"qcd_relaxed_ss" : mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os", "iso_1", "iso_2"], cut_type=cut_type + "_emb")+"*((q_1*q_2)>0.0)"+"*"+isolationDefinition
						}
					for key in mc_selection_weights:
						add_input(
								input_file=self.files_wj(channel),
								weight=self.wj_stitchingweight()+"*"+mc_selection_weights[key],
								nick="noplot_wj_"+key
						)
						if (not kwargs.get("no_ewk_samples", False)):
							add_input(
									input_file=self.files_ewkwm(channel),
									weight=mc_selection_weights[key]+"*"+self.ewkwm_stitchingweight(),
									nick="noplot_wj_"+key
							)
							add_input(
									input_file=self.files_ewkwp(channel),
									weight=mc_selection_weights[key]+"*"+self.ewkwp_stitchingweight(),
									nick="noplot_wj_"+key
							)
						add_input(
								input_file=self.files_data(channel),
								scale_factor=1.0,
								weight=data_selection_weights[key],
								nick="qcd" if key == "qcd_shape" else "noplot_data_"+key
						)
						add_input(
								input_file=self.files_ztt(channel, embedding=self.embedding),
								weight=Samples.ztt_genmatch(channel, embedding=self.embedding)+"*"+self.get_weights_ztt(channel=channel,cut_type=cut_type + ("_emb" if self.embedding else ""),mc_sample_weight=emb_selection_weights[key] if self.embedding else mc_selection_weights[key],embedding=self.embedding)+"*zPtReweightWeight"+"*"+zmm_cr_factor,
								scale_factor = 1.0 if self.embedding else lumi,
								nick="noplot_ztt_"+key
						)
						if not (kwargs.get("no_ewk_samples", False) or kwargs.get("no_ewkz_as_dy", False) or self.embedding):
							add_input(
									input_file=self.files_ewkz_zll(channel),
									weight=Samples.ztt_genmatch(channel)+"*"+self.get_weights_ztt(channel=channel,cut_type=cut_type,mc_sample_weight=mc_selection_weights[key], doStitching=False)+"*"+self.ewkz_zll_stitchingweight()+"*"+zmm_cr_factor,
									nick="noplot_ztt_"+key
							)
							add_input(
									input_file=self.files_ewkz_znn(channel),
									weight=Samples.ztt_genmatch(channel)+"*"+self.get_weights_ztt(channel=channel,cut_type=cut_type,mc_sample_weight=mc_selection_weights[key], doStitching=False)+"*"+self.ewkz_znn_stitchingweight()+"*"+zmm_cr_factor,
									nick="noplot_ztt_"+key
							)
						add_input(
								input_file=self.files_zll(channel),
								weight=mc_selection_weights[key]+"*"+self.zll_stitchingweight()+"*"+Samples.zll_genmatch(channel)+"*"+"zPtReweightWeight"+"*"+self.zll_zl_shape_weight(channel, cut_type)+"*"+zmm_cr_factor,
								nick="noplot_zll_"+key
						)
						if not (kwargs.get("no_ewk_samples", False) or kwargs.get("no_ewkz_as_dy", False)):
							add_input(
									input_file=self.files_ewkz_zll(channel),
									weight=mc_selection_weights[key]+"*"+Samples.zll_genmatch(channel)+"*"+self.zll_zl_shape_weight(channel, cut_type)+"*"+self.ewkz_zll_stitchingweight()+"*"+zmm_cr_factor,
									nick="noplot_zll_"+key
							)
							add_input(
									input_file=self.files_ewkz_znn(channel),
									weight=mc_selection_weights[key]+"*"+Samples.zll_genmatch(channel)+"*"+self.zll_zl_shape_weight(channel, cut_type)+"*"+self.ewkz_znn_stitchingweight()+"*"+zmm_cr_factor,
									nick="noplot_zll_"+key
							)
						if (not kwargs.get("no_ewk_samples", False)) and kwargs.get("no_ewkz_as_dy", False):
							add_input(
									input_file=self.files_ewkz_zll(channel),
									weight=mc_selection_weights[key]+"*"+self.ewkz_zll_stitchingweight()+"*"+zmm_cr_factor,
									nick="noplot_ewkz_"+key
							)
							add_input(
									input_file=self.files_ewkz_znn(channel),
									weight=mc_selection_weights[key]+"*"+self.ewkz_znn_stitchingweight()+"*"+zmm_cr_factor,
									nick="noplot_ewkz_"+key
							)
						add_input(
								input_file=self.files_ttj(channel),
								weight=mc_selection_weights[key]+"*"+self.embedding_ttbarveto_weight(channel)+"*topPtReweightWeight",
								nick="noplot_ttj_"+key
						)
						if self.legacy:
							add_input(
									input_file=self.files_ww(channel),
									weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+self.embedding_ttbarveto_weight(channel),
									nick="noplot_vv_"+key
							)
							add_input(
									input_file=self.files_wz(channel),
									weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+self.embedding_ttbarveto_weight(channel),
									nick="noplot_vv_"+key
							)
							add_input(
									input_file=self.files_zz(channel),
									weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+self.embedding_ttbarveto_weight(channel),
									nick="noplot_vv_"+key
							)
						else:
							add_input(
									input_file=self.files_wwtolnuqq(channel),
									weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+self.embedding_ttbarveto_weight(channel)+"*"+self.wwtolnuqq_stitchingweight(),
									nick="noplot_vv_"+key
							)
							add_input(
									input_file=self.files_wwto4q(channel),
									weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+self.embedding_ttbarveto_weight(channel),
									nick="noplot_vv_"+key
							)
							add_input(
									input_file=self.files_wzto1l3nu(channel),
									weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+self.embedding_ttbarveto_weight(channel),
									nick="noplot_vv_"+key
							)
							add_input(
									input_file=self.files_wzto3lnu(channel),
									weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+self.embedding_ttbarveto_weight(channel),
									nick="noplot_vv_"+key
							)
							add_input(
									input_file=self.files_zzto2l2nu(channel),
									weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+self.embedding_ttbarveto_weight(channel),
									nick="noplot_vv_"+key
							)
							add_input(
									input_file=self.files_zzto4l(channel),
									weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+self.embedding_ttbarveto_weight(channel)+"*"+self.zzto4l_stitchingweight(),
									nick="noplot_vv_"+key
							)
						add_input(
								input_file=self.files_singletop(channel),
								weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type),
								nick="noplot_vv_"+key
						)
						# add_input(
						# 		input_file=self.files_vv(channel),
						# 		weight=mc_selection_weights[key]+"*"+self.vv_stitchingweight(),
						# 		nick="noplot_vv_"+key
						# )
						# add_input(
						# 		input_file=self.files_diboson(channel),
						# 		weight=mc_selection_weights[key],
						# 		nick="noplot_vv_"+key
						# )
					if not "EstimateQcdTauHadTauHad" in config.get("analysis_modules", []):
						config.setdefault("analysis_modules", []).append("EstimateQcdTauHadTauHad")
					config.setdefault("qcd_data_shape_nicks", []).append("qcd"+nick_suffix)
					config.setdefault("qcd_data_signal_control_nicks", []).append("noplot_data_qcd_signal_ss"+nick_suffix)
					config.setdefault("qcd_data_relaxed_control_nicks", []).append("noplot_data_qcd_relaxed_ss"+nick_suffix)
					if (not kwargs.get("no_ewk_samples", False)) and kwargs.get("no_ewkz_as_dy", False):
						config.setdefault("qcd_data_subtract_nicks", []).append(" ".join([nick+nick_suffix for nick in "noplot_ztt_qcd_shape noplot_zll_qcd_shape noplot_ewkz_qcd_shape noplot_ttj_qcd_shape noplot_vv_qcd_shape noplot_wj_qcd_shape".split()]))
						config.setdefault("qcd_control_signal_subtract_nicks", []).append(" ".join([nick+nick_suffix for nick in "noplot_ztt_qcd_signal_ss noplot_zll_qcd_signal_ss noplot_ewkz_qcd_signal_ss noplot_ttj_qcd_signal_ss noplot_vv_qcd_signal_ss noplot_wj_qcd_signal_ss".split()]))
						config.setdefault("qcd_control_relaxed_subtract_nicks", []).append(" ".join([nick+nick_suffix for nick in "noplot_ztt_qcd_relaxed_ss noplot_zll_qcd_relaxed_ss noplot_ewkz_qcd_relaxed_ss noplot_ttj_qcd_relaxed_ss noplot_vv_qcd_relaxed_ss noplot_wj_qcd_relaxed_ss".split()]))
					else:
						config.setdefault("qcd_data_subtract_nicks", []).append(" ".join([nick+nick_suffix for nick in "noplot_ztt_qcd_shape noplot_zll_qcd_shape noplot_ttj_qcd_shape noplot_vv_qcd_shape noplot_wj_qcd_shape".split()]))
						config.setdefault("qcd_control_signal_subtract_nicks", []).append(" ".join([nick+nick_suffix for nick in "noplot_ztt_qcd_signal_ss noplot_zll_qcd_signal_ss noplot_ttj_qcd_signal_ss noplot_vv_qcd_signal_ss noplot_wj_qcd_signal_ss".split()]))
						config.setdefault("qcd_control_relaxed_subtract_nicks", []).append(" ".join([nick+nick_suffix for nick in "noplot_ztt_qcd_relaxed_ss noplot_zll_qcd_relaxed_ss noplot_ttj_qcd_relaxed_ss noplot_vv_qcd_relaxed_ss noplot_wj_qcd_relaxed_ss".split()]))
				elif channel in ["mm","ee"]:
					log.error("Sample config (QCD) currently not implemented for channel \"%s\"!" % channel)

			if "classic" in estimationMethod or "mc" in estimationMethod:
				# WJets for QCD estimate
				add_input(
						input_file=self.files_wj(channel),
						weight=mc_weight+"*"+weight+"*eventWeight*"+self.wj_stitchingweight()+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_B , cut_type=cut_type_B)+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
						nick="noplot_wj_ss"
				)

				if channel in ["mt", "et"]:

					add_input(
							input_file=self.files_data(channel),
							scale_factor=1.0,
							weight=data_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_C, cut_type=cut_type_C),
							nick="noplot_wj_ss_data_control"
					)
					add_input(
							input_file=self.files_ztt(channel, embedding=self.embedding),
							weight=Samples.ztt_genmatch(channel, embedding=self.embedding)+"*"+self.get_weights_ztt(channel=channel,cut_type=cut_type + ("_emb" if self.embedding else ""),weight=weight,embedding=self.embedding)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_C, cut_type=cut_type_C + ("_emb" if self.embedding else ""))+"*zPtReweightWeight"+"*"+zmm_cr_factor,
							scale_factor = 1.0 if self.embedding else lumi,
							nick="noplot_ztt_ss_mc_wj_control"
					)
					if not (kwargs.get("no_ewk_samples", False) or kwargs.get("no_ewkz_as_dy", False) or self.embedding):
						add_input(
								input_file=self.files_ewkz_zll(channel),
								weight=Samples.ztt_genmatch(channel)+"*"+self.get_weights_ztt(channel=channel,cut_type=cut_type,weight=weight,doStitching=False)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_C, cut_type=cut_type_C)+"*"+self.ewkz_zll_stitchingweight()+"*"+zmm_cr_factor,
								nick="noplot_ztt_ss_mc_wj_control"
						)
						add_input(
								input_file=self.files_ewkz_znn(channel),
								weight=Samples.ztt_genmatch(channel)+"*"+self.get_weights_ztt(channel=channel,cut_type=cut_type,weight=weight,doStitching=False)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_C, cut_type=cut_type_C)+"*"+self.ewkz_znn_stitchingweight()+"*"+zmm_cr_factor,
								nick="noplot_ztt_ss_mc_wj_control"
						)
					add_input(
							input_file=self.files_zll(channel),
							weight=mc_weight+"*"+weight+"*eventWeight*"+self.zll_stitchingweight()+"*"+Samples.zll_genmatch(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_C, cut_type=cut_type_C)+"*zPtReweightWeight"+"*"+self.zll_zl_shape_weight(channel, cut_type)+"*"+zmm_cr_factor,
							nick="noplot_zll_ss_wj_control"
					)
					if not (kwargs.get("no_ewk_samples", False) or kwargs.get("no_ewkz_as_dy", False)):
						add_input(
								input_file=self.files_ewkz_zll(channel),
								weight=mc_weight+"*"+weight+"*eventWeight*"+Samples.zll_genmatch(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_C, cut_type=cut_type_C)+"*"+self.zll_zl_shape_weight(channel, cut_type)+"*"+self.ewkz_zll_stitchingweight()+"*"+zmm_cr_factor,
								nick="noplot_zll_ss_wj_control"
						)
						add_input(
								input_file=self.files_ewkz_znn(channel),
								weight=mc_weight+"*"+weight+"*eventWeight*"+Samples.zll_genmatch(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_C, cut_type=cut_type_C)+"*"+self.zll_zl_shape_weight(channel, cut_type)+"*"+self.ewkz_znn_stitchingweight()+"*"+zmm_cr_factor,
								nick="noplot_zll_ss_wj_control"
						)
					if (not kwargs.get("no_ewk_samples", False)) and kwargs.get("no_ewkz_as_dy", False):
						add_input(
								input_file=self.files_ewkz_zll(channel),
								weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_C, cut_type=cut_type_C)+"*"+self.ewkz_zll_stitchingweight()+"*"+zmm_cr_factor,
								nick="noplot_ewkz_ss_wj_control"
						)
						add_input(
								input_file=self.files_ewkz_znn(channel),
								weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_C, cut_type=cut_type_C)+"*"+self.ewkz_znn_stitchingweight()+"*"+zmm_cr_factor,
								nick="noplot_ewkz_ss_wj_control"
						)
					add_input(
							input_file=self.files_ttj(channel),
							weight=mc_weight+"*"+weight+"*eventWeight*"+self.embedding_ttbarveto_weight(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_C, cut_type=cut_type_C)+"*topPtReweightWeight",
							nick="noplot_ttj_ss_wj_control"
					)
					if self.legacy:
						add_input(
								input_file=self.files_ww(channel),
								weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_C, cut_type=cut_type_C)+"*"+self.embedding_ttbarveto_weight(channel),
								nick="noplot_vv_ss_wj_control"
						)
						add_input(
								input_file=self.files_wz(channel),
								weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_C, cut_type=cut_type_C)+"*"+self.embedding_ttbarveto_weight(channel),
								nick="noplot_vv_ss_wj_control"
						)
						add_input(
								input_file=self.files_zz(channel),
								weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_C, cut_type=cut_type_C)+"*"+self.embedding_ttbarveto_weight(channel),
								nick="noplot_vv_ss_wj_control"
						)
					else:
						add_input(
								input_file=self.files_wwtolnuqq(channel),
								weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_C, cut_type=cut_type_C)+"*"+self.embedding_ttbarveto_weight(channel)+"*"+self.wwtolnuqq_stitchingweight(),
								nick="noplot_vv_ss_wj_control"
						)
						add_input(
								input_file=self.files_wwto4q(channel),
								weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_C, cut_type=cut_type_C)+"*"+self.embedding_ttbarveto_weight(channel),
								nick="noplot_vv_ss_wj_control"
						)
						add_input(
								input_file=self.files_wzto1l3nu(channel),
								weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_C, cut_type=cut_type_C)+"*"+self.embedding_ttbarveto_weight(channel),
								nick="noplot_vv_ss_wj_control"
						)
						add_input(
								input_file=self.files_wzto3lnu(channel),
								weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_C, cut_type=cut_type_C)+"*"+self.embedding_ttbarveto_weight(channel),
								nick="noplot_vv_ss_wj_control"
						)
						add_input(
								input_file=self.files_zzto2l2nu(channel),
								weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_C, cut_type=cut_type_C)+"*"+self.embedding_ttbarveto_weight(channel),
								nick="noplot_vv_ss_wj_control"
						)
						add_input(
								input_file=self.files_zzto4l(channel),
								weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_C, cut_type=cut_type_C)+"*"+self.embedding_ttbarveto_weight(channel)+"*"+self.zzto4l_stitchingweight(),
								nick="noplot_vv_ss_wj_control"
						)
					add_input(
							input_file=self.files_singletop(channel),
							weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_C, cut_type=cut_type_C),
							nick="noplot_vv_ss_wj_control"
					)
					# add_input(
					# 		input_file=self.files_vv(channel),
					# 		weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_C, cut_type=cut_type_C)+"*"+self.vv_stitchingweight(),
					# 		nick="noplot_vv_ss_wj_control"
					# )
					# add_input(
					# 		input_file=self.files_diboson(channel),
					# 		weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_C, cut_type=cut_type_C),
					# 		nick="noplot_vv_ss_wj_control"
					# )
					add_input(
							input_file=self.files_wj(channel),
							weight=mc_weight+"*"+weight+"*eventWeight*"+self.wj_stitchingweight()+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_B , cut_type=cut_type_B),
							nick="noplot_wj_ss_mc_signal"
					)
					add_input(
							input_file=self.files_wj(channel),
							weight=mc_weight+"*"+weight+"*eventWeight*"+self.wj_stitchingweight()+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_C, cut_type=cut_type_C),
							nick="noplot_wj_ss_mc_control"
					)

					if not "EstimateWjets" in config.get("analysis_modules", []):
						config.setdefault("analysis_modules", []).append("EstimateWjets")
					config.setdefault("wjets_from_mc", []).append(False)
					config.setdefault("wjets_shape_nicks", []).append("noplot_wj_ss"+nick_suffix)
					config.setdefault("wjets_data_control_nicks", []).append("noplot_wj_ss_data_control"+nick_suffix)
					if (not kwargs.get("no_ewk_samples", False)) and kwargs.get("no_ewkz_as_dy", False):
						config.setdefault("wjets_data_substract_nicks", []).append(" ".join([nick+nick_suffix for nick in "noplot_ztt_ss_mc_wj_control noplot_zll_ss_wj_control noplot_ewkz_ss_wj_control noplot_ttj_ss_wj_control noplot_vv_ss_wj_control".split()]))
					else:
						config.setdefault("wjets_data_substract_nicks", []).append(" ".join([nick+nick_suffix for nick in "noplot_ztt_ss_mc_wj_control noplot_zll_ss_wj_control noplot_ttj_ss_wj_control noplot_vv_ss_wj_control".split()]))
					config.setdefault("wjets_mc_signal_nicks", []).append("noplot_wj_ss_mc_signal"+nick_suffix)
					config.setdefault("wjets_mc_control_nicks", []).append("noplot_wj_ss_mc_control"+nick_suffix)

				# QCD
				shape_weight = data_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_B , cut_type=cut_type_B)
				#if (not category is None) and (category != ""):
					## relaxed/inverted isolation
					#if channel in ["et", "mt"]:
						#shape_weight = weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["blind", "os", "iso_2"], cut_type=cut_type)+"*((q_1*q_2)>0.0)"+"*(byCombinedIsolationDeltaBetaCorrRaw3Hits_2<10.0)"
					#else:
						#shape_weight = weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["blind", "os", "iso_1", "iso_2"], cut_type=cut_type)+"*((q_1*q_2)>0.0)"

				add_input(
						input_file=self.files_data(channel),
						scale_factor=1.0,
						weight=shape_weight,
						nick="qcd"
				)
				add_input(
						input_file=self.files_data(channel),
						scale_factor=1.0,
						weight=data_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_B , cut_type=cut_type_B),
						nick="noplot_data_qcd_yield"
				)
				add_input(
						input_file=self.files_data(channel),
						scale_factor=1.0,
						weight=data_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_B , cut_type=cut_type_B),
						nick="noplot_data_qcd_control"
				)
				add_input(
						input_file=self.files_ztt(channel, embedding=self.embedding),
						weight=Samples.ztt_genmatch(channel, embedding=self.embedding)+"*"+self.get_weights_ztt(channel=channel,cut_type=cut_type + ("_emb" if self.embedding else ""),weight=weight,embedding=self.embedding)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_B , cut_type=cut_type_B + ("_emb" if self.embedding else ""))+"*zPtReweightWeight"+"*"+zmm_cr_factor+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type + ("_emb" if self.embedding else "")),
						scale_factor = 1.0 if self.embedding else lumi,
						nick="noplot_ztt_mc_qcd_control"
				)
				if not (kwargs.get("no_ewk_samples", False) or kwargs.get("no_ewkz_as_dy", False) or self.embedding):
					add_input(
							input_file=self.files_ewkz_zll(channel),
							weight=Samples.ztt_genmatch(channel)+"*"+self.get_weights_ztt(channel=channel,cut_type=cut_type,weight=weight,doStitching=False)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_B , cut_type=cut_type_B)+"*"+self.ewkz_zll_stitchingweight()+"*"+zmm_cr_factor+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
							nick="noplot_ztt_mc_qcd_control"
					)
					add_input(
							input_file=self.files_ewkz_znn(channel),
							weight=Samples.ztt_genmatch(channel)+"*"+self.get_weights_ztt(channel=channel,cut_type=cut_type,weight=weight,doStitching=False)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_B , cut_type=cut_type_B)+"*"+self.ewkz_znn_stitchingweight()+"*"+zmm_cr_factor+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
							nick="noplot_ztt_mc_qcd_control"
					)
				add_input(
						input_file=self.files_zll(channel),
						weight=mc_weight+"*"+weight+"*eventWeight*"+self.zll_stitchingweight()+"*"+Samples.zll_genmatch(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_B , cut_type=cut_type_B)+"*zPtReweightWeight"+"*"+self.zll_zl_shape_weight(channel, cut_type)+"*"+zmm_cr_factor+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
						nick="noplot_zll_qcd_control"
				)
				if not (kwargs.get("no_ewk_samples", False) or kwargs.get("no_ewkz_as_dy", False)):
					add_input(
							input_file=self.files_ewkz_zll(channel),
							weight=mc_weight+"*"+weight+"*eventWeight*"+Samples.zll_genmatch(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_B , cut_type=cut_type_B)+"*"+self.zll_zl_shape_weight(channel, cut_type)+"*"+self.ewkz_zll_stitchingweight()+"*"+zmm_cr_factor+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
							nick="noplot_zll_qcd_control"
					)
					add_input(
							input_file=self.files_ewkz_znn(channel),
							weight=mc_weight+"*"+weight+"*eventWeight*"+Samples.zll_genmatch(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_B , cut_type=cut_type_B)+"*"+self.zll_zl_shape_weight(channel, cut_type)+"*"+self.ewkz_znn_stitchingweight()+"*"+zmm_cr_factor+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
							nick="noplot_zll_qcd_control"
					)
				if (not kwargs.get("no_ewk_samples", False)) and kwargs.get("no_ewkz_as_dy", False):
					add_input(
							input_file=self.files_ewkz_zll(channel),
							weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_B , cut_type=cut_type_B)+"*"+self.ewkz_zll_stitchingweight()+"*"+zmm_cr_factor+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
							nick="noplot_ewkz_qcd_control"
					)
					add_input(
							input_file=self.files_ewkz_znn(channel),
							weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_B , cut_type=cut_type_B)+"*"+self.ewkz_znn_stitchingweight()+"*"+zmm_cr_factor+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
							nick="noplot_ewkz_qcd_control"
					)
				add_input(
						input_file=self.files_ttj(channel),
						weight=mc_weight+"*"+weight+"*eventWeight*"+self.embedding_ttbarveto_weight(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_B , cut_type=cut_type_B)+"*topPtReweightWeight"+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
						nick="noplot_ttj_qcd_control"
				)
				if self.legacy:
					add_input(
							input_file=self.files_ww(channel),
							weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_B, cut_type=cut_type_B)+"*"+self.embedding_ttbarveto_weight(channel),
							nick="noplot_vv_qcd_control"
					)
					add_input(
							input_file=self.files_wz(channel),
							weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_B, cut_type=cut_type_B)+"*"+self.embedding_ttbarveto_weight(channel),
							nick="noplot_vv_qcd_control"
					)
					add_input(
							input_file=self.files_zz(channel),
							weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_B, cut_type=cut_type_B)+"*"+self.embedding_ttbarveto_weight(channel),
							nick="noplot_vv_qcd_control"
					)
				else:
					add_input(
							input_file=self.files_wwtolnuqq(channel),
							weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_B, cut_type=cut_type_B)+"*"+self.embedding_ttbarveto_weight(channel)+"*"+self.wwtolnuqq_stitchingweight(),
							nick="noplot_vv_qcd_control"
					)
					add_input(
							input_file=self.files_wwto4q(channel),
							weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_B, cut_type=cut_type_B)+"*"+self.embedding_ttbarveto_weight(channel),
							nick="noplot_vv_qcd_control"
					)
					add_input(
							input_file=self.files_wzto1l3nu(channel),
							weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_B, cut_type=cut_type_B)+"*"+self.embedding_ttbarveto_weight(channel),
							nick="noplot_vv_qcd_control"
					)
					add_input(
							input_file=self.files_wzto3lnu(channel),
							weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_B, cut_type=cut_type_B)+"*"+self.embedding_ttbarveto_weight(channel),
							nick="noplot_vv_qcd_control"
					)
					add_input(
							input_file=self.files_zzto2l2nu(channel),
							weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_B, cut_type=cut_type_B)+"*"+self.embedding_ttbarveto_weight(channel),
							nick="noplot_vv_qcd_control"
					)
					add_input(
							input_file=self.files_zzto4l(channel),
							weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_B, cut_type=cut_type_B)+"*"+self.embedding_ttbarveto_weight(channel)+"*"+self.zzto4l_stitchingweight(),
							nick="noplot_vv_qcd_control"
					)
				add_input(
						input_file=self.files_singletop(channel),
						weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_B, cut_type=cut_type_B),
						nick="noplot_vv_qcd_control"
				)
				# add_input(
				# 		input_file=self.files_vv(channel),
				# 		weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_B, cut_type=cut_type_B)+"*"+self.vv_stitchingweight()+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
				# 		nick="noplot_vv_qcd_control"
				# )
				# add_input(
				# 		input_file=self.files_diboson(channel),
				# 		weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_B, cut_type=cut_type_B)+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
				# 		nick="noplot_vv_qcd_control"
				# )

				if not "EstimateQcd" in config.get("analysis_modules", []):
					config.setdefault("analysis_modules", []).append("EstimateQcd")
				config.setdefault("qcd_shape_nicks", []).append("qcd"+nick_suffix)
				config.setdefault("qcd_yield_nicks", []).append("noplot_data_qcd_yield"+nick_suffix)
				if (not kwargs.get("no_ewk_samples", False)) and kwargs.get("no_ewkz_as_dy", False):
					config.setdefault("qcd_yield_subtract_nicks", []).append(" ".join([nick+nick_suffix for nick in "noplot_ztt_mc_qcd_control noplot_zll_qcd_control noplot_ewkz_qcd_control noplot_ttj_qcd_control noplot_vv_qcd_control noplot_wj_ss".split()]))
					config.setdefault("qcd_shape_subtract_nicks", []).append(" ".join([nick+nick_suffix for nick in "noplot_ztt_mc_qcd_control noplot_zll_qcd_control noplot_ewkz_qcd_control noplot_ttj_qcd_control noplot_vv_qcd_control noplot_wj_ss".split()]))
				else:
					config.setdefault("qcd_yield_subtract_nicks", []).append(" ".join([nick+nick_suffix for nick in "noplot_ztt_mc_qcd_control noplot_zll_qcd_control noplot_ttj_qcd_control noplot_vv_qcd_control noplot_wj_ss".split()]))
					config.setdefault("qcd_shape_subtract_nicks", []).append(" ".join([nick+nick_suffix for nick in "noplot_ztt_mc_qcd_control noplot_zll_qcd_control noplot_ttj_qcd_control noplot_vv_qcd_control noplot_wj_ss".split()]))
				if channel == "em" or channel == "ttbar":
					config.setdefault("qcd_extrapolation_factors_ss_os", []).append(2.0 + (0.0 if not "os" in exclude_cuts else 1.0))
				elif channel == "et":
					config.setdefault("qcd_extrapolation_factors_ss_os", []).append(1.0 + (0.0 if not "os" in exclude_cuts else 1.0))
				elif channel == "mt":
					config.setdefault("qcd_extrapolation_factors_ss_os", []).append(1.0 + (0.0 if not "os" in exclude_cuts else 1.0))
				else:
					config.setdefault("qcd_extrapolation_factors_ss_os", []).append(1.06 + (0.0 if not "os" in exclude_cuts else 1.0))

		else:
			log.error("Sample config (QCD) currently not implemented for channel \"%s\"!" % channel)

		if not kwargs.get("no_plot", False):
			if not kwargs.get("mssm", False):
				Samples._add_bin_corrections(config, "qcd", nick_suffix)
			Samples._add_plot(config, "bkg", "HIST", "F", "qcd", nick_suffix)
		return config

	def wj(self, config, channel, category, weight, nick_suffix, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", fakefactor_method=None, estimationMethod="classic", controlregions=False,**kwargs):

		if channel== "mt":
			ss_os_factor = 1.29 #TODO for 2017
		elif channel == "et":
			ss_os_factor = 1.56 #TODO for 2017
		else:
			ss_os_factor = 0.0

		"""
		Using ABCD method in background-method types 'new' and 'simeqn'
		A := Signal region / os+low_mt
		B := SS Control region / ss+low_mt
		C := High mt SS region / ss+high_mt
		D := High mt OS region / ss+low_mt
		As this method is entangled with the qcd function some nicks will be defined there and taken from there.
		See the analysis modules for details.
		"""

		if exclude_cuts is None:
			exclude_cuts = []

		zmm_cr_factor = kwargs.get("zmm_cr_factor", "(1.0)")

		scale_factor = lumi
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("WJets", 1.0)

		data_weight, mc_weight = self.projection(kwargs)
		add_input = partialmethod(Samples._add_input, config=config, folder=self.root_file_folder(channel), scale_factor=lumi, nick_suffix=nick_suffix)

		# Definition of the 4 regions of phase space used for the ABCD method
		cut_type_A = cut_type
		cut_type_B = cut_type + "SameSignRegion"
		cut_type_C = cut_type + "highMtSSControlRegionWJ"
		cut_type_D = cut_type + "highMtControlRegionWJ"

		exclude_cuts_A = exclude_cuts
		# This structure is needed to avoid that some cuts appear twice in the list of cuts to exclude.
		exclude_cuts_B = [cut for cut in exclude_cuts if cut not in ["os"]] + ["os"]
		exclude_cuts_D = [cut for cut in exclude_cuts] #if cut not in ["mt"]] + ["mt"]
		exclude_cuts_C = [cut for cut in exclude_cuts_D if cut not in ["os"]] + ["os"]
		exclude_cuts_inclusive = copy.deepcopy(exclude_cuts)+["mt"]
		exclude_cuts_inclusive_ss = copy.deepcopy(exclude_cuts_inclusive)+["os"]

		if channel in ["mt", "et"]:
			if kwargs.get("useRelaxedIsolationForW", False):
				cut_type_A = cut_type_A + "relaxedETauMuTauWJ"
				cut_type_C = cut_type_C + "relaxedETauMuTauWJ"
			elif category != None:
				cut_type_A = cut_type_A + ("relaxedETauMuTauWJ" if ("1jet" in category or "vbf" in category or "Boosted2D" in category or "Vbf2D" in category or "dijet" in category) else "")
				cut_type_C = cut_type_C + ("relaxedETauMuTauWJ" if ("1jet" in category or "vbf" in category or "Boosted2D" in category or "Vbf2D" in category or "dijet" in category) else "")

			# wj shape and highmt to lowmt extrapolation
			if "mc" in estimationMethod:
				# Determine W+jets from Monte Carlo
				add_input(
					input_file=self.files_wj(channel),
					weight=mc_weight+"*"+weight+"*eventWeight*"+self.wj_stitchingweight()+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
					nick="wj"
				)
				if (not kwargs.get("no_ewk_samples", False)):
					add_input(
							input_file=self.files_ewkwm(channel),
							weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+self.ewkwm_stitchingweight(),
							nick="wj"
					)
					add_input(
							input_file=self.files_ewkwp(channel),
							weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+self.ewkwp_stitchingweight(),
							nick="wj"
					)

			if "simeqn" in estimationMethod or "new" in estimationMethod:
				"""
				Inputs shared by both method can by found below ordered by the ABCD region they are applied to.
				"""
				# Type A inputs
				# wj shape nick
				add_input(
						input_file=self.files_wj(channel),
						weight=mc_weight+"*"+weight+"*eventWeight*"+self.wj_stitchingweight()+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type_A),
						nick="wj"
				)
				if (not kwargs.get("no_ewk_samples", False)):
					add_input(
							input_file=self.files_ewkwm(channel),
							weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type_A)+"*"+self.ewkwm_stitchingweight(),
							nick="wj"
					)
					add_input(
							input_file=self.files_ewkwp(channel),
							weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type_A)+"*"+self.ewkwp_stitchingweight(),
							nick="wj"
					)
				# Type C inputs
				# noplot_xx_ss_highmt: for the w+jets ss high-mt yield subtract nicks
				add_input(
						input_file=self.files_data(channel),
						scale_factor=1.0,
						weight=data_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_C, cut_type=cut_type_C),
						nick=("noplot_" if not controlregions else "") + "data_ss_highmt",
				)

				# Type C subtract nicks - nick type xx_ss_highmt
				add_input(
						input_file=self.files_ztt(channel, embedding=self.embedding),
						weight=Samples.ztt_genmatch(channel, embedding=self.embedding)+"*"+self.get_weights_ztt(channel=channel,cut_type=cut_type,weight=weight,embedding=self.embedding)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_C, cut_type=cut_type_C + ("_emb" if self.embedding else ""))+"*zPtReweightWeight"+"*"+zmm_cr_factor,
						scale_factor = 1.0 if self.embedding else lumi,
						nick=("noplot_" if not controlregions else "") + "ztt_ss_highmt"
				)
				if not (kwargs.get("no_ewk_samples", False) or kwargs.get("no_ewkz_as_dy", False) or self.embedding):
					add_input(
							input_file=self.files_ewkz_zll(channel),
							weight=Samples.ztt_genmatch(channel)+"*"+self.get_weights_ztt(channel=channel,cut_type=cut_type,weight=weight,doStitching=False)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_C, cut_type=cut_type_C)+"*"+self.ewkz_zll_stitchingweight()+"*"+zmm_cr_factor,
							nick=("noplot_" if not controlregions else "") + "ztt_ss_highmt"
					)
					add_input(
							input_file=self.files_ewkz_znn(channel),
							weight=Samples.ztt_genmatch(channel)+"*"+self.get_weights_ztt(channel=channel,cut_type=cut_type,weight=weight,doStitching=False)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_C, cut_type=cut_type_C)+"*"+self.ewkz_znn_stitchingweight()+"*"+zmm_cr_factor,
							nick=("noplot_" if not controlregions else "") + "ztt_ss_highmt"
					)
				add_input(
						input_file=self.files_zll(channel),
						weight=mc_weight+"*"+weight+"*eventWeight*"+self.zll_stitchingweight()+"*"+Samples.zll_genmatch(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_C, cut_type=cut_type_C)+"*zPtReweightWeight"+"*"+self.zll_zl_shape_weight(channel, cut_type)+"*"+zmm_cr_factor,
						nick=("noplot_" if not controlregions else "") + "zll_ss_highmt"
				)
				if not (kwargs.get("no_ewk_samples", False) or kwargs.get("no_ewkz_as_dy", False)):
					add_input(
							input_file=self.files_ewkz_zll(channel),
							weight=mc_weight+"*"+weight+"*eventWeight*"+Samples.zll_genmatch(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_C, cut_type=cut_type_C)+"*"+self.zll_zl_shape_weight(channel, cut_type)+"*"+self.ewkz_zll_stitchingweight()+"*"+zmm_cr_factor,
							nick=("noplot_" if not controlregions else "") + "zll_ss_highmt"
					)
					add_input(
							input_file=self.files_ewkz_znn(channel),
							weight=mc_weight+"*"+weight+"*eventWeight*"+Samples.zll_genmatch(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_C, cut_type=cut_type_C)+"*"+self.zll_zl_shape_weight(channel, cut_type)+"*"+self.ewkz_znn_stitchingweight()+"*"+zmm_cr_factor,
							nick=("noplot_" if not controlregions else "") + "zll_ss_highmt"
					)
				if (not kwargs.get("no_ewk_samples", False)) and kwargs.get("no_ewkz_as_dy", False):
					add_input(
						input_file=self.files_ewkz_zll(channel),
						weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_C, cut_type=cut_type_C)+"*"+self.ewkz_zll_stitchingweight()+"*"+zmm_cr_factor,
						nick=("noplot_" if not controlregions else "") + "ewkz_ss_highmt"
						)
					add_input(
						input_file=self.files_ewkz_znn(channel),
						weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_C, cut_type=cut_type_C)+"*"+self.ewkz_znn_stitchingweight()+"*"+zmm_cr_factor,
						nick=("noplot_" if not controlregions else "") + "ewkz_ss_highmt"
					)
				add_input(
						input_file=self.files_ttj(channel),
						weight=mc_weight+"*"+weight+"*eventWeight*"+self.embedding_ttbarveto_weight(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_C, cut_type=cut_type_C)+"*topPtReweightWeight",
						nick=("noplot_" if not controlregions else "") + "ttj_ss_highmt"
				)
				if self.legacy:
					add_input(
							input_file=self.files_ww(channel),
							weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_C, cut_type=cut_type_C)+"*"+self.embedding_ttbarveto_weight(channel),
							nick=("noplot_" if not controlregions else "") + "vv_ss_highmt"
					)
					add_input(
							input_file=self.files_wz(channel),
							weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_C, cut_type=cut_type_C)+"*"+self.embedding_ttbarveto_weight(channel),
							nick=("noplot_" if not controlregions else "") + "vv_ss_highmt"
					)
					add_input(
							input_file=self.files_zz(channel),
							weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_C, cut_type=cut_type_C)+"*"+self.embedding_ttbarveto_weight(channel),
							nick=("noplot_" if not controlregions else "") + "vv_ss_highmt"
					)
				else:
					add_input(
							input_file=self.files_wwtolnuqq(channel),
							weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_C, cut_type=cut_type_C)+"*"+self.embedding_ttbarveto_weight(channel)+"*"+self.wwtolnuqq_stitchingweight(),
							nick=("noplot_" if not controlregions else "") + "vv_ss_highmt"
					)
					add_input(
							input_file=self.files_wwto4q(channel),
							weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_C, cut_type=cut_type_C)+"*"+self.embedding_ttbarveto_weight(channel),
							nick=("noplot_" if not controlregions else "") + "vv_ss_highmt"
					)
					add_input(
							input_file=self.files_wzto1l3nu(channel),
							weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_C, cut_type=cut_type_C)+"*"+self.embedding_ttbarveto_weight(channel),
							nick=("noplot_" if not controlregions else "") + "vv_ss_highmt"
					)
					add_input(
							input_file=self.files_wzto3lnu(channel),
							weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_C, cut_type=cut_type_C)+"*"+self.embedding_ttbarveto_weight(channel),
							nick=("noplot_" if not controlregions else "") + "vv_ss_highmt"
					)
					add_input(
							input_file=self.files_zzto2l2nu(channel),
							weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_C, cut_type=cut_type_C)+"*"+self.embedding_ttbarveto_weight(channel),
							nick=("noplot_" if not controlregions else "") + "vv_ss_highmt"
					)
					add_input(
							input_file=self.files_zzto4l(channel),
							weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_C, cut_type=cut_type_C)+"*"+self.embedding_ttbarveto_weight(channel)+"*"+self.zzto4l_stitchingweight(),
							nick=("noplot_" if not controlregions else "") + "vv_ss_highmt"
					)
				add_input(
						input_file=self.files_singletop(channel),
						weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_C, cut_type=cut_type_C),
						nick=("noplot_" if not controlregions else "") + "vv_ss_highmt"
				)
				# add_input(
				# 		input_file=self.files_vv(channel),
				# 		weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_C, cut_type=cut_type_C)+"*"+self.vv_stitchingweight(),
				# 		nick=("noplot_" if not controlregions else "") + "vv_ss_highmt"
				# )
				# add_input(
				# 		input_file=self.files_diboson(channel),
				# 		weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_C, cut_type=cut_type_C),
				# 		nick=("noplot_" if not controlregions else "") + "vv_ss_highmt"
				# )
				# C Wj Monte Carlo nicks
				add_input(
						input_file=self.files_wj(channel),
						weight=mc_weight+"*"+weight+"*eventWeight*"+self.wj_stitchingweight()+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_C, cut_type=cut_type_C),
						nick=("noplot_" if not controlregions else "") + "wj_mc_ss_highmt"
				)
				if (not kwargs.get("no_ewk_samples", False)):
					add_input(
							input_file=self.files_ewkwm(channel),
							weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_C, cut_type=cut_type_C)+"*"+self.ewkwm_stitchingweight(),
							nick=("noplot_" if not controlregions else "") + "wj_mc_ss_highmt"
					)
					add_input(
							input_file=self.files_ewkwp(channel),
							weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_C, cut_type=cut_type_C)+"*"+self.ewkwp_stitchingweight(),
							nick=("noplot_" if not controlregions else "") + "wj_mc_ss_highmt"
					)
				# Type D inputs
				# data yield in os highmt
				add_input(
						input_file=self.files_data(channel),
						scale_factor=1.0,
						weight=data_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_D, cut_type=cut_type_D),
						nick=("noplot_" if not controlregions else "") + "data_os_highmt",
				)
				# wjets os highmt subtract nicks
				add_input(
						input_file=self.files_ztt(channel, embedding=self.embedding),
						weight=Samples.ztt_genmatch(channel, embedding=self.embedding)+"*"+self.get_weights_ztt(channel=channel,cut_type=cut_type,weight=weight,embedding=self.embedding)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_D, cut_type=cut_type_D + ("_emb" if self.embedding else ""))+"*zPtReweightWeight"+"*"+zmm_cr_factor,
						scale_factor = 1.0 if self.embedding else lumi,
						nick=("noplot_" if not controlregions else "") + "ztt_os_highmt"
				)
				if not (kwargs.get("no_ewk_samples", False) or kwargs.get("no_ewkz_as_dy", False) or self.embedding):
					add_input(
							input_file=self.files_ewkz_zll(channel),
							weight=Samples.ztt_genmatch(channel)+"*"+self.get_weights_ztt(channel=channel,cut_type=cut_type,weight=weight,doStitching=False)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_D, cut_type=cut_type_D)+"*"+self.ewkz_zll_stitchingweight()+"*"+zmm_cr_factor,
							nick=("noplot_" if not controlregions else "") + "ztt_os_highmt"
					)
					add_input(
							input_file=self.files_ewkz_znn(channel),
							weight=Samples.ztt_genmatch(channel)+"*"+self.get_weights_ztt(channel=channel,cut_type=cut_type,weight=weight,doStitching=False)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_D, cut_type=cut_type_D)+"*"+self.ewkz_znn_stitchingweight()+"*"+zmm_cr_factor,
							nick=("noplot_" if not controlregions else "") + "ztt_os_highmt"
					)
				add_input(
						input_file=self.files_zll(channel),
						weight=mc_weight+"*"+weight+"*eventWeight*"+self.zll_stitchingweight()+"*"+Samples.zll_genmatch(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_D, cut_type=cut_type_D)+"*zPtReweightWeight"+"*"+self.zll_zl_shape_weight(channel, cut_type)+"*"+zmm_cr_factor,
						nick=("noplot_" if not controlregions else "") + "zll_os_highmt"
				)
				if (not kwargs.get("no_ewk_samples", False)) and kwargs.get("no_ewkz_as_dy", False):
					add_input(
							input_file=self.files_ewkz_zll(channel),
							weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_D, cut_type=cut_type_D)+"*"+self.ewkz_zll_stitchingweight()+"*"+zmm_cr_factor,
							nick=("noplot_" if not controlregions else "") + "ewkz_os_highmt"
					)
					add_input(
							input_file=self.files_ewkz_znn(channel),
							weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_D, cut_type=cut_type_D)+"*"+self.ewkz_znn_stitchingweight()+"*"+zmm_cr_factor,
							nick=("noplot_" if not controlregions else "") + "ewkz_os_highmt"
					)
				if not (kwargs.get("no_ewk_samples", False)):
					add_input(
							input_file=self.files_ewkz_zll(channel),
							weight=mc_weight+"*"+weight+"*eventWeight*"+Samples.zll_genmatch(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_D, cut_type=cut_type_D)+"*"+self.zll_zl_shape_weight(channel, cut_type)+"*"+self.ewkz_zll_stitchingweight()+"*"+zmm_cr_factor,
							nick=("noplot_" if not controlregions else "") + "zll_os_highmt"
					)
					add_input(
							input_file=self.files_ewkz_znn(channel),
							weight=mc_weight+"*"+weight+"*eventWeight*"+Samples.zll_genmatch(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_D, cut_type=cut_type_D)+"*"+self.zll_zl_shape_weight(channel, cut_type)+"*"+self.ewkz_znn_stitchingweight()+"*"+zmm_cr_factor,
							nick=("noplot_" if not controlregions else "") + "zll_os_highmt"
					)
				add_input(
						input_file=self.files_ttj(channel),
						weight=mc_weight+"*"+weight+"*eventWeight*"+self.embedding_ttbarveto_weight(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_D, cut_type=cut_type_D)+"*topPtReweightWeight",
						nick=("noplot_" if not controlregions else "") + "ttj_os_highmt"
				)
				if self.legacy:
					add_input(
							input_file=self.files_ww(channel),
							weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_D, cut_type=cut_type_D)+"*"+self.embedding_ttbarveto_weight(channel),
							nick=("noplot_" if not controlregions else "") + "vv_os_highmt"
					)
					add_input(
							input_file=self.files_wz(channel),
							weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_D, cut_type=cut_type_D)+"*"+self.embedding_ttbarveto_weight(channel),
							nick=("noplot_" if not controlregions else "") + "vv_os_highmt"
					)
					add_input(
							input_file=self.files_zz(channel),
							weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_D, cut_type=cut_type_D)+"*"+self.embedding_ttbarveto_weight(channel),
							nick=("noplot_" if not controlregions else "") + "vv_os_highmt"
					)
				else:
					add_input(
							input_file=self.files_wwtolnuqq(channel),
							weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_D, cut_type=cut_type_D)+"*"+self.embedding_ttbarveto_weight(channel)+"*"+self.wwtolnuqq_stitchingweight(),
							nick=("noplot_" if not controlregions else "") + "vv_os_highmt"
					)
					add_input(
							input_file=self.files_wwto4q(channel),
							weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_D, cut_type=cut_type_D)+"*"+self.embedding_ttbarveto_weight(channel),
							nick=("noplot_" if not controlregions else "") + "vv_os_highmt"
					)
					add_input(
							input_file=self.files_wzto1l3nu(channel),
							weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_D, cut_type=cut_type_D)+"*"+self.embedding_ttbarveto_weight(channel),
							nick=("noplot_" if not controlregions else "") + "vv_os_highmt"
					)
					add_input(
							input_file=self.files_wzto3lnu(channel),
							weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_D, cut_type=cut_type_D)+"*"+self.embedding_ttbarveto_weight(channel),
							nick=("noplot_" if not controlregions else "") + "vv_os_highmt"
					)
					add_input(
							input_file=self.files_zzto2l2nu(channel),
							weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_D, cut_type=cut_type_D)+"*"+self.embedding_ttbarveto_weight(channel),
							nick=("noplot_" if not controlregions else "") + "vv_os_highmt"
					)
					add_input(
							input_file=self.files_zzto4l(channel),
							weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_D, cut_type=cut_type_D)+"*"+self.embedding_ttbarveto_weight(channel)+"*"+self.zzto4l_stitchingweight(),
							nick=("noplot_" if not controlregions else "") + "vv_os_highmt"
					)
				add_input(
						input_file=self.files_singletop(channel),
						weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_D, cut_type=cut_type_D),
						nick=("noplot_" if not controlregions else "") + "vv_os_highmt"
				)
				# add_input(
				# 		input_file=self.files_vv(channel),
				# 		weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_D, cut_type=cut_type_D)+"*"+self.vv_stitchingweight(),
				# 		nick=("noplot_" if not controlregions else "") + "vv_os_highmt"
				# )
				# add_input(
				# 		input_file=self.files_diboson(channel),
				# 		weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_D, cut_type=cut_type_D),
				# 		nick=("noplot_" if not controlregions else "") + "vv_os_highmt"
				# )
				# D Wj Monte Carlo nicks
				add_input(
						input_file=self.files_wj(channel),
						weight=mc_weight+"*"+weight+"*eventWeight*"+self.wj_stitchingweight()+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_D, cut_type=cut_type_D),
						nick=("noplot_" if not controlregions else "") + "wj_mc_os_highmt"
				)
				if (not kwargs.get("no_ewk_samples", False)):
					add_input(
							input_file=self.files_ewkwm(channel),
							weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_D, cut_type=cut_type_D)+"*"+self.ewkwm_stitchingweight(),
							nick=("noplot_" if not controlregions else "") + "wj_mc_os_highmt"
					)
					add_input(
							input_file=self.files_ewkwp(channel),
							weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_D, cut_type=cut_type_D)+"*"+self.ewkwp_stitchingweight(),
							nick=("noplot_" if not controlregions else "") + "wj_mc_os_highmt"
					)
			if "simeqn" in estimationMethod:
				"""
				Inputs only needed by simeqn method.
				"""
				# add inclusive Wjets MC samples in OS and SS for W SS/OS determination
				# Inclusive W os/ss factor determination
				add_input(
					input_file=self.files_wj(channel),
					weight=mc_weight+"*"+weight+"*eventWeight*"+self.wj_stitchingweight()+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_inclusive_ss, cut_type=cut_type_B)+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
					nick=("noplot_" if not controlregions else "") + "wj_mc_ss_inclusive"
				)
				if (not kwargs.get("no_ewk_samples", False)):
					add_input(
							input_file=self.files_ewkwm(channel),
							weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_inclusive_ss, cut_type=cut_type_B)+"*"+self.ewkwm_stitchingweight(),
							nick=("noplot_" if not controlregions else "") + "wj_mc_ss_inclusive"
					)
					add_input(
							input_file=self.files_ewkwp(channel),
							weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_inclusive_ss, cut_type=cut_type_B)+"*"+self.ewkwp_stitchingweight(),
							nick=("noplot_" if not controlregions else "") + "wj_mc_ss_inclusive"
					)
				add_input(
					input_file=self.files_wj(channel),
					weight=mc_weight+"*"+weight+"*eventWeight*"+self.wj_stitchingweight()+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_inclusive, cut_type=cut_type)+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
					nick=("noplot_" if not controlregions else "") + "wj_mc_os_inclusive"
				)
				if (not kwargs.get("no_ewk_samples", False)):
					add_input(
							input_file=self.files_ewkwm(channel),
							weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_inclusive, cut_type=cut_type)+"*"+self.ewkwm_stitchingweight(),
							nick=("noplot_" if not controlregions else "") + "wj_mc_os_inclusive"
					)
					add_input(
							input_file=self.files_ewkwp(channel),
							weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_inclusive, cut_type=cut_type)+"*"+self.ewkwp_stitchingweight(),
							nick=("noplot_" if not controlregions else "") + "wj_mc_os_inclusive"
					)
				add_input(
					input_file=self.files_wj(channel),
					weight=mc_weight+"*"+weight+"*eventWeight*"+self.wj_stitchingweight()+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_B, cut_type=cut_type_B)+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
					nick=("noplot_" if not controlregions else "") + "wj_mc_ss_lowmt"
				)
				if (not kwargs.get("no_ewk_samples", False)):
					add_input(
							input_file=self.files_ewkwm(channel),
							weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_B, cut_type=cut_type_B)+"*"+self.ewkwm_stitchingweight(),
							nick=("noplot_" if not controlregions else "") + "wj_mc_ss_lowmt"
					)
					add_input(
							input_file=self.files_ewkwp(channel),
							weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_B, cut_type=cut_type_B)+"*"+self.ewkwp_stitchingweight(),
							nick=("noplot_" if not controlregions else "") + "wj_mc_ss_lowmt"
					)
				add_input(
					input_file=self.files_wj(channel),
					weight=mc_weight+"*"+weight+"*eventWeight*"+self.wj_stitchingweight()+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
					nick=("noplot_" if not controlregions else "") + "wj_mc_os_lowmt"
				)
				if (not kwargs.get("no_ewk_samples", False)):
					add_input(
							input_file=self.files_ewkwm(channel),
							weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+self.ewkwm_stitchingweight(),
							nick=("noplot_" if not controlregions else "") + "wj_mc_os_lowmt"
					)
					add_input(
							input_file=self.files_ewkwp(channel),
							weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+self.ewkwp_stitchingweight(),
							nick=("noplot_" if not controlregions else "") + "wj_mc_os_lowmt"
					)
				# Step 5 - Estimate highmt ss yield
				# data yield in ss highmt
				# shape nicks for the later usable histograms
				add_input(
						input_file=self.files_wj(channel),
						weight=mc_weight+"*"+weight+"*eventWeight*"+self.wj_stitchingweight()+"*"+self._cut_string(channel,  exclude_cuts=exclude_cuts_C, cut_type=cut_type_C),
						nick=("noplot_" if not controlregions else "") + "wj_ss_highmt"
				)
				if (not kwargs.get("no_ewk_samples", False)):
					add_input(
							input_file=self.files_ewkwm(channel),
							weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel,  exclude_cuts=exclude_cuts_C, cut_type=cut_type_C)+"*"+self.ewkwm_stitchingweight(),
							nick=("noplot_" if not controlregions else "") + "wj_ss_highmt"
					)
					add_input(
							input_file=self.files_ewkwp(channel),
							weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel,  exclude_cuts=exclude_cuts_C, cut_type=cut_type_C)+"*"+self.ewkwp_stitchingweight(),
							nick=("noplot_" if not controlregions else "") + "wj_ss_highmt"
					)
				# Step 6 - Estimate lowmt shapes both os and ss
				add_input(
						input_file=self.files_wj(channel),
						weight=mc_weight+"*"+weight+"*eventWeight*"+self.wj_stitchingweight()+"*"+self._cut_string(channel,  exclude_cuts=exclude_cuts_B, cut_type=cut_type_B),
						nick=("noplot_" if not controlregions else "") + "wj_ss_lowmt"
				)
				if (not kwargs.get("no_ewk_samples", False)):
					add_input(
							input_file=self.files_ewkwm(channel),
							weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel,  exclude_cuts=exclude_cuts_B, cut_type=cut_type_B)+"*"+self.ewkwm_stitchingweight(),
							nick=("noplot_" if not controlregions else "") + "wj_ss_lowmt"
					)
					add_input(
							input_file=self.files_ewkwp(channel),
							weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel,  exclude_cuts=exclude_cuts_B, cut_type=cut_type_B)+"*"+self.ewkwp_stitchingweight(),
							nick=("noplot_" if not controlregions else "") + "wj_ss_lowmt"
					)
				add_input(
						input_file=self.files_wj(channel),
						weight=mc_weight+"*"+weight+"*eventWeight*"+self.wj_stitchingweight()+"*"+self._cut_string(channel,  exclude_cuts=exclude_cuts_D, cut_type=cut_type_D),
						nick=("noplot_" if not controlregions else "") + "wj_os_highmt"
				)
				if (not kwargs.get("no_ewk_samples", False)):
					add_input(
							input_file=self.files_ewkwm(channel),
							weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel,  exclude_cuts=exclude_cuts_D, cut_type=cut_type_D)+"*"+self.ewkwm_stitchingweight(),
							nick=("noplot_" if not controlregions else "") + "wj_os_highmt"
					)
					add_input(
							input_file=self.files_ewkwp(channel),
							weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel,  exclude_cuts=exclude_cuts_D, cut_type=cut_type_D)+"*"+self.ewkwp_stitchingweight(),
							nick=("noplot_" if not controlregions else "") + "wj_os_highmt"
					)
			if "new" in estimationMethod:
				"""
				Inputs only needed by 'new' method.
				"""
				# relaxed selections
				add_input(
						input_file=self.files_wj(channel),
						weight=mc_weight+"*"+weight+"*eventWeight*"+self.wj_stitchingweight()+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_D, cut_type=cut_type_D),
						nick=("noplot_" if not controlregions else "") + "wj_relaxed_os_highmt"
				)
				if (not kwargs.get("no_ewk_samples", False)):
					add_input(
							input_file=self.files_ewkwm(channel),
							weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_C, cut_type=cut_type_D)+"*"+self.ewkwm_stitchingweight(),
							nick=("noplot_" if not controlregions else "") + "wj_relaxed_os_highmt"
					)
					add_input(
							input_file=self.files_ewkwp(channel),
							weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_C, cut_type=cut_type_C)+"*"+self.ewkwp_stitchingweight(),
							nick=("noplot_" if not controlregions else "") + "wj_relaxed_os_highmt"
					)
				add_input(
						input_file=self.files_wj(channel),
						weight=mc_weight+"*"+weight+"*eventWeight*"+self.wj_stitchingweight()+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type_A),
						nick=("noplot_" if not controlregions else "") + "wj_relaxed_os_lowmt"
				)
				if (not kwargs.get("no_ewk_samples", False)):
					add_input(
							input_file=self.files_ewkwm(channel),
							weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type_A)+"*"+self.ewkwm_stitchingweight(),
							nick=("noplot_" if not controlregions else "") + "wj_relaxed_os_lowmt"
					)
					add_input(
							input_file=self.files_ewkwp(channel),
							weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type_A)+"*"+self.ewkwp_stitchingweight(),
							nick=("noplot_" if not controlregions else "") + "wj_relaxed_os_lowmt"
					)
				if not "EstimateWjetsAndQCD" in config.get("analysis_modules", []):
					config.setdefault("analysis_modules", []).append("EstimateWjetsAndQCD")
				if controlregions:
					if (not kwargs.get("no_ewk_samples", False)) and kwargs.get("no_ewkz_as_dy", False):
						config.setdefault("C_substract_nicks", []).append(" ".join([nick+nick_suffix for nick in "ztt_ss_highmt zll_ss_highmt ewkz_ss_highmt ttj_ss_highmt vv_ss_highmt".split()]))
						config.setdefault("D_substract_nicks", []).append(" ".join([nick+nick_suffix for nick in "ztt_os_highmt zll_os_highmt ewkz_os_highmt ttj_os_highmt vv_os_highmt".split()]))
					else:
						config.setdefault("C_substract_nicks", []).append(" ".join([nick+nick_suffix for nick in "ztt_ss_highmt zll_ss_highmt ttj_ss_highmt vv_ss_highmt".split()]))
						config.setdefault("D_substract_nicks", []).append(" ".join([nick+nick_suffix for nick in "ztt_os_highmt zll_os_highmt ttj_os_highmt vv_os_highmt".split()]))
					config.setdefault("wjets_C_data_nicks", []).append("data_ss_highmt"+nick_suffix)
					config.setdefault("wjets_D_data_nicks", []).append("data_os_highmt"+nick_suffix)
					config.setdefault("wjets_A_shape_nicks", []).append("wj"+nick_suffix)
					config.setdefault("wjets_C_mc_nicks", []).append("wj_mc_ss_highmt"+nick_suffix)
					config.setdefault("wjets_D_mc_nicks", []).append("wj_mc_os_highmt"+nick_suffix)
					config.setdefault("wjets_wj_final_selection", []).append(None)
					config.setdefault("wjets_relaxed_os_highmt_nicks", []).append("noplot_wj_relaxed_os_highmt"+nick_suffix)
					config.setdefault("wjets_relaxed_os_lowmt_nicks", []).append("noplot_wj_relaxed_os_lowmt"+nick_suffix)
					for nick in ["ztt_os_highmt", "zll_os_highmt", "ttj_os_highmt", "vv_os_highmt", "data_os_highmt", "wj_os_highmt", "ztt_ss_highmt", "zll_ss_highmt", "ttj_ss_highmt", "vv_ss_highmt", "data_ss_highmt", "wj_ss_highmt"]+(["ewkz_os_highmt", "ewkz_ss_highmt"] if (not kwargs.get("no_ewk_samples", False) and kwargs.get("no_ewkz_as_dy", False)) else []):
						if not kwargs.get("mssm", False):
							Samples._add_bin_corrections(config, nick, nick_suffix)
						Samples._add_plot(config, "bkg", "HIST", "F", nick, nick_suffix)
				else:
					if (not kwargs.get("no_ewk_samples", False)) and kwargs.get("no_ewkz_as_dy", False):
						config.setdefault("C_substract_nicks", []).append(" ".join(["noplot_"+nick+nick_suffix for nick in "ztt_ss_highmt zll_ss_highmt ewkz_ss_highmt ttj_ss_highmt vv_ss_highmt".split()]))
						config.setdefault("D_substract_nicks", []).append(" ".join(["noplot_"+nick+nick_suffix for nick in "ztt_os_highmt zll_os_highmt ewkz_os_highmt ttj_os_highmt vv_os_highmt".split()]))
					else:
						config.setdefault("C_substract_nicks", []).append(" ".join(["noplot_"+nick+nick_suffix for nick in "ztt_ss_highmt zll_ss_highmt ttj_ss_highmt vv_ss_highmt".split()]))
						config.setdefault("D_substract_nicks", []).append(" ".join(["noplot_"+nick+nick_suffix for nick in "ztt_os_highmt zll_os_highmt ttj_os_highmt vv_os_highmt".split()]))
					config.setdefault("wjets_C_data_nicks", []).append("noplot_data_ss_highmt"+nick_suffix)
					config.setdefault("wjets_D_data_nicks", []).append("noplot_data_os_highmt"+nick_suffix)
					config.setdefault("wjets_C_mc_nicks", []).append("noplot_wj_mc_ss_highmt"+nick_suffix)
					config.setdefault("wjets_D_mc_nicks", []).append("noplot_wj_mc_os_highmt"+nick_suffix)
					config.setdefault("wjets_wj_final_selection", []).append(None)
					config.setdefault("wjets_relaxed_os_highmt_nicks", []).append("noplot_wj_relaxed_os_highmt"+nick_suffix)
					config.setdefault("wjets_relaxed_os_lowmt_nicks", []).append("noplot_wj_relaxed_os_lowmt"+nick_suffix)
					config.setdefault("wjets_A_shape_nicks", []).append("wj"+nick_suffix)
			elif "simeqn" in estimationMethod:
				if not "EstimateWjetsAndQCDSimEquationMethod" in config.get("analysis_modules", []):
					config.setdefault("analysis_modules", []).append("EstimateWjetsAndQCDSimEquationMethod")
				if controlregions:
					# Step 1
					config.setdefault("wjets_ss_mc_nicks", []).append("wj_mc_ss_inclusive"+nick_suffix)
					config.setdefault("wjets_os_mc_nicks", []).append("wj_mc_os_inclusive"+nick_suffix)
					# Step 2
					config.setdefault("wjets_C_mc_nicks", []).append("wj_mc_ss_highmt"+nick_suffix)
					config.setdefault("wjets_B_mc_nicks", []).append("wj_mc_ss_lowmt"+nick_suffix)
					# Step 3
					config.setdefault("wjets_D_mc_nicks", []).append("wj_mc_os_highmt"+nick_suffix)
					config.setdefault("wjets_A_mc_nicks", []).append("wj_mc_os_lowmt"+nick_suffix)
					# Step 4
					# To be added in the qcd method.
					# Step 5
					config.setdefault("wjets_C_data_nicks", []).append("data_ss_highmt"+nick_suffix)
					config.setdefault("wjets_D_data_nicks", []).append("data_os_highmt"+nick_suffix)

					config.setdefault("C_subtract_nicks", []).append(" ".join([nick+nick_suffix for nick in "ztt_ss_highmt zll_ss_highmt ttj_ss_highmt vv_ss_highmt".split()]))
					config.setdefault("D_subtract_nicks", []).append(" ".join([nick+nick_suffix for nick in "ztt_os_highmt zll_os_highmt ttj_os_highmt vv_os_highmt".split()]))
					config.setdefault("wjets_C_shape_nicks", []).append("wj_ss_highmt"+nick_suffix)
					# Step 6
					config.setdefault("wjets_B_shape_nicks", []).append("wj_ss_lowmt"+nick_suffix)
					config.setdefault("wjets_A_shape_nicks", []).append("wj"+nick_suffix)
					config.setdefault("wjets_D_shape_nicks", []).append("wj_os_highmt"+nick_suffix)
					for nick in ["wj_mc_ss_inclusive", "wj_mc_os_inclusive", "wj_mc_ss_highmt", "wj_mc_ss_lowmt", "wj_mc_os_highmt", "wj_mc_os_lowmt", "ztt_ss_highmt", "zll_ss_highmt", "ttj_ss_highmt", "vv_ss_highmt", "ztt_os_highmt", "zll_os_highmt", "ttj_os_highmt", "vv_os_highmt", "wj_ss_highmt", "wj_ss_lowmt"]:
						if not kwargs.get("mssm", False):
							Samples._add_bin_corrections(config, nick, nick_suffix)
						Samples._add_plot(config, "bkg", "HIST", "F", nick, nick_suffix)
					for nick in ["data_ss_highmt", "data_os_highmt", "data_os_lowmt"]:
						if not kwargs.get("mssm", False):
							Samples._add_bin_corrections(config, nick, nick_suffix)
						Samples._add_plot(config, "data", "E", "ELP", nick, nick_suffix)
				else:
					# Step 1
					config.setdefault("wjets_ss_mc_nicks", []).append("noplot_wj_mc_ss_inclusive"+nick_suffix)
					config.setdefault("wjets_os_mc_nicks", []).append("noplot_wj_mc_os_inclusive"+nick_suffix)
					# Step 2
					config.setdefault("wjets_C_mc_nicks", []).append("noplot_wj_mc_ss_highmt"+nick_suffix)
					config.setdefault("wjets_B_mc_nicks", []).append("noplot_wj_mc_ss_lowmt"+nick_suffix)
					# Step 3
					config.setdefault("wjets_D_mc_nicks", []).append("noplot_wj_mc_os_highmt"+nick_suffix)
					config.setdefault("wjets_A_mc_nicks", []).append("noplot_wj_mc_os_lowmt"+nick_suffix)
					# Step 4
					# To be added in the qcd method.
					# Step 5
					config.setdefault("wjets_C_data_nicks", []).append("noplot_data_ss_highmt"+nick_suffix)
					config.setdefault("wjets_D_data_nicks", []).append("noplot_data_os_highmt"+nick_suffix)
					config.setdefault("C_subtract_nicks", []).append(" ".join(["noplot_"+nick+nick_suffix for nick in "ztt_ss_highmt zll_ss_highmt ttj_ss_highmt vv_ss_highmt".split()]))
					config.setdefault("D_subtract_nicks", []).append(" ".join(["noplot_"+nick+nick_suffix for nick in "ztt_os_highmt zll_os_highmt ttj_os_highmt vv_os_highmt".split()]))
					config.setdefault("wjets_C_shape_nicks", []).append("noplot_wj_ss_highmt"+nick_suffix)
					# Step 6
					config.setdefault("wjets_B_shape_nicks", []).append("noplot_wj_ss_lowmt"+nick_suffix)
					config.setdefault("wjets_A_shape_nicks", []).append("wj"+nick_suffix)
					config.setdefault("wjets_D_shape_nicks", []).append("noplot_wj_os_highmt"+nick_suffix)

			if "classic" in estimationMethod:
				shape_weight = mc_weight+"*"+weight+"*eventWeight*"+self.wj_stitchingweight()+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)
				#if (not category is None) and (category != ""):
					## relaxed isolation
					#shape_weight = weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["blind", "iso_2"], cut_type=cut_type)+"*(byCombinedIsolationDeltaBetaCorrRaw3Hits_2<10.0)"

				add_input(
						input_file=self.files_wj(channel),
						weight=shape_weight,
						nick="wj"
				)
				add_input(
						input_file=self.files_data(channel),
						scale_factor=1.0,
						weight=data_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type_D, data=True),
						nick="noplot_wj_data_control"
				)
				add_input(
						input_file=self.files_ztt(channel, embedding=self.embedding),
						weight=Samples.ztt_genmatch(channel, embedding=self.embedding)+"*"+self.get_weights_ztt(channel=channel,cut_type=cut_type_D + ("_emb" if self.embedding else ""),weight=weight,embedding=self.embedding)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type_D + ("_emb" if self.embedding else ""))+"*zPtReweightWeight"+"*"+self.decay_mode_reweight(channel, cut_type_D + ("_emb" if self.embedding else ""))+"*"+zmm_cr_factor+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type + ("_emb" if self.embedding else "")),
						scale_factor = 1.0 if self.embedding else lumi,
						nick="noplot_ztt_mc_wj_control"
				)
				if not (kwargs.get("no_ewk_samples", False) or kwargs.get("no_ewkz_as_dy", False) or self.embedding):
					add_input(
							input_file=self.files_ewkz_zll(channel),
							weight=Samples.ztt_genmatch(channel)+"*"+self.get_weights_ztt(channel=channel,cut_type=cut_type_D,weight=weight,doStitching=False)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type_D)+"*"+self.ewkz_zll_stitchingweight()+"*"+zmm_cr_factor,
							nick="noplot_ztt_mc_wj_control"
					)
					add_input(
							input_file=self.files_ewkz_znn(channel),
							weight=Samples.ztt_genmatch(channel)+"*"+self.get_weights_ztt(channel=channel,cut_type=cut_type_D,weight=weight,doStitching=False)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type_D)+"*"+self.ewkz_znn_stitchingweight()+"*"+zmm_cr_factor,
							nick="noplot_ztt_mc_wj_control"
					)
				add_input(
						input_file=self.files_zll(channel),
						weight=mc_weight+"*"+weight+"*eventWeight*"+self.zll_stitchingweight()+"*"+Samples.zll_genmatch(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type_D)+"*zPtReweightWeight"+"*"+self.zll_zl_shape_weight(channel, cut_type)+"*"+zmm_cr_factor,
						nick="noplot_zll_wj_control"
				)
				if not (kwargs.get("no_ewk_samples", False) or kwargs.get("no_ewkz_as_dy", False)):
					add_input(
							input_file=self.files_ewkz_zll(channel),
							weight=mc_weight+"*"+weight+"*eventWeight*"+Samples.zll_genmatch(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type_D)+"*"+self.zll_zl_shape_weight(channel, cut_type)+"*"+self.ewkz_zll_stitchingweight()+"*"+zmm_cr_factor,
							nick="noplot_zll_wj_control"
					)
					add_input(
							input_file=self.files_ewkz_znn(channel),
							weight=mc_weight+"*"+weight+"*eventWeight*"+Samples.zll_genmatch(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type_D)+"*"+self.zll_zl_shape_weight(channel, cut_type)+"*"+self.ewkz_znn_stitchingweight()+"*"+zmm_cr_factor,
							nick="noplot_zll_wj_control"
					)
				if (not kwargs.get("no_ewk_samples", False)) and kwargs.get("no_ewkz_as_dy", False):
					add_input(
							input_file=self.files_ewkz_zll(channel),
							weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type_D)+"*"+self.ewkz_zll_stitchingweight()+"*"+zmm_cr_factor,
							nick="noplot_ewkz_wj_control"
					)
					add_input(
							input_file=self.files_ewkz_znn(channel),
							weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type_D)+"*"+self.ewkz_znn_stitchingweight()+"*"+zmm_cr_factor,
							nick="noplot_ewkz_wj_control"
					)
				add_input(
						input_file=self.files_ttj(channel),
						weight=mc_weight+"*"+weight+"*eventWeight*"+self.embedding_ttbarveto_weight(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type_D)+"*topPtReweightWeight",
						nick="noplot_ttj_wj_control"
				)
				if self.legacy:
					add_input(
							input_file=self.files_ww(channel),
							weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type_D)+"*"+self.embedding_ttbarveto_weight(channel),
							nick="noplot_vv_wj_control"
					)
					add_input(
							input_file=self.files_wz(channel),
							weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type_D)+"*"+self.embedding_ttbarveto_weight(channel),
							nick="noplot_vv_wj_control"
					)
					add_input(
							input_file=self.files_zz(channel),
							weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type_D)+"*"+self.embedding_ttbarveto_weight(channel),
							nick="noplot_vv_wj_control"
					)
				else:
					add_input(
							input_file=self.files_wwtolnuqq(channel),
							weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type_D)+"*"+self.embedding_ttbarveto_weight(channel)+"*"+self.wwtolnuqq_stitchingweight(),
							nick="noplot_vv_wj_control"
					)
					add_input(
							input_file=self.files_wwto4q(channel),
							weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type_D)+"*"+self.embedding_ttbarveto_weight(channel),
							nick="noplot_vv_wj_control"
					)
					add_input(
							input_file=self.files_wzto1l3nu(channel),
							weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type_D)+"*"+self.embedding_ttbarveto_weight(channel),
							nick="noplot_vv_wj_control"
					)
					add_input(
							input_file=self.files_wzto3lnu(channel),
							weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type_D)+"*"+self.embedding_ttbarveto_weight(channel),
							nick="noplot_vv_wj_control"
					)
					add_input(
							input_file=self.files_zzto2l2nu(channel),
							weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type_D)+"*"+self.embedding_ttbarveto_weight(channel),
							nick="noplot_vv_wj_control"
					)
					add_input(
							input_file=self.files_zzto4l(channel),
							weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type_D)+"*"+self.embedding_ttbarveto_weight(channel)+"*"+self.zzto4l_stitchingweight(),
							nick="noplot_vv_wj_control"
					)
				add_input(
						input_file=self.files_singletop(channel),
						weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type_D),
						nick="noplot_vv_wj_control"
				)
				# add_input(
				# 		input_file=self.files_vv(channel),
				# 		weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type_D)+"*"+self.vv_stitchingweight(),
				# 		nick="noplot_vv_wj_control"
				# )
				# add_input(
				# 		input_file=self.files_diboson(channel),
				# 		weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type_D),
				# 		nick="noplot_vv_wj_control"
				# )
				add_input(
						input_file=self.files_wj(channel),
						weight=mc_weight+"*"+weight+"*eventWeight*"+self.wj_stitchingweight()+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type),
						nick="noplot_wj_mc_signal"
				)
				add_input(
						input_file=self.files_wj(channel),
						weight=mc_weight+"*"+weight+"*eventWeight*"+self.wj_stitchingweight()+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type_D),
						nick="noplot_wj_mc_control"
				)

				if not "EstimateWjets" in config.get("analysis_modules", []):
					config.setdefault("analysis_modules", []).append("EstimateWjets")
				# if fakefactor_method is None:
					# config.setdefault("wjets_from_mc", []).append(False)
				config.setdefault("wjets_shape_nicks", []).append("wj"+nick_suffix)
				config.setdefault("wjets_data_control_nicks", []).append("noplot_wj_data_control"+nick_suffix)
				if (not kwargs.get("no_ewk_samples", False)) and kwargs.get("no_ewkz_as_dy", False):
					config.setdefault("wjets_data_substract_nicks", []).append(" ".join([nick+nick_suffix for nick in "noplot_ztt_mc_wj_control noplot_zll_wj_control noplot_ewkz_wj_control noplot_ttj_wj_control noplot_vv_wj_control".split()]))
				else:
					config.setdefault("wjets_data_substract_nicks", []).append(" ".join([nick+nick_suffix for nick in "noplot_ztt_mc_wj_control noplot_zll_wj_control noplot_ttj_wj_control noplot_vv_wj_control".split()]))
				config.setdefault("wjets_mc_signal_nicks", []).append("noplot_wj_mc_signal"+nick_suffix)
				config.setdefault("wjets_mc_control_nicks", []).append("noplot_wj_mc_control"+nick_suffix)

		elif channel in ["em", "tt", "mm", "ee", "ttbar"]:
			add_input(
					input_file=self.files_wj(channel),
					weight=weight+"*eventWeight*"+self.wj_stitchingweight()+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
					nick="wj"
			)
			if (not kwargs.get("no_ewk_samples", False)):
				add_input(
						input_file=self.files_ewkwm(channel),
						weight=weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+self.ewkwm_stitchingweight()+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
						nick="wj"
				)
				add_input(
						input_file=self.files_ewkwp(channel),
						weight=weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+self.ewkwp_stitchingweight()+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
						nick="wj"
				)
			if channel == "em" or channel == "ttbar":
				add_input(
						input_file=self.files_wgamma(channel),
						weight=weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+self.wgamma_stitchingweight()+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
						nick="wj"
				)
				add_input(
						input_file=self.files_wgamma_star(channel),
						weight=weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
						nick="wj"
				)
		else:
			log.error("Sample config (WJets) currently not implemented for channel \"%s\"!" % channel)

		if not kwargs.get("no_plot", False):
			if not kwargs.get("mssm", False):
				Samples._add_bin_corrections(config, "wj", nick_suffix)
			Samples._add_plot(config, "bkg", "HIST", "F", "wj", nick_suffix)
		return config



	def ff(self, config, channel, category, weight, nick_suffix, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", fake_factor_name_1="fakefactorWeight_comb_inclusive_1", fake_factor_name_2="fakefactorWeight_comb_inclusive_2", fakefactor_method=True, **kwargs):

		data_weight, mc_weight = self.projection(kwargs)
		zmm_cr_factor = kwargs.get("zmm_cr_factor", "(1.0)")
		cut_type_emb = cut_type + "_emb" if self.embedding else cut_type

		if exclude_cuts is None:
			exclude_cuts = []
		exclude_cuts_ff = []

		proxy_fakefactors = kwargs.get("proxy_fakefactors", False)

		if proxy_fakefactors:
			if channel in ["mt", "et"]:
				proxy_fakefactor_weight_2 = "fakefactor_"+channel+"_HASH_NAME.GetScaleFactor(0, pt_1, pt_2, iso_1, decayMode_1, decayMode_2, m_vis, mt_1, njetspt30)"
			if channel == "tt":
				proxy_fakefactor_weight_1 = "fakefactor_"+channel+"_HASH_NAME.GetScaleFactor(0, pt_1, pt_2, iso_1, decayMode_1, decayMode_2, m_vis, mt_1, njetspt30)"
				proxy_fakefactor_weight_2 = "fakefactor_"+channel+"_HASH_NAME.GetScaleFactor(1, pt_1, pt_2, iso_1, decayMode_1, decayMode_2, m_vis, mt_1, njetspt30)"
			# proxy_prefix = os.path.expandvars("#include <HiggsAnalysis/KITHiggsToTauTau/interface/Utility/FakeFactorProxy.h>\nFakeFactorProxy fakefactor_"+channel+"_HASH_NAME(\"$CMSSW_BASE/src/plots/FF_fractions/FF_fractions_workspace_decayMode_pt_njets.root\", \"decayMode,njets,pt\", \""+channel+"\");")
			proxy_prefix = os.path.expandvars("#include <HiggsAnalysis/KITHiggsToTauTau/interface/Utility/FakeFactorProxy.h>\nFakeFactorProxy fakefactor_"+channel+"_HASH_NAME(\"$CMSSW_BASE/src/plots/FF_fractions/FF_fractions_workspace_m_vis_njetsexlude_os_exlude_blind.root\", \"njets,m_vis\", \""+channel+"\");")

		sub_channels = [channel] # needed for splitting of taus in tt, does nothing in all other channels

		if channel in ["mt", "et"]:
			exclude_cuts_ff += ["iso_2"]
			# ff_weight_2 = "(" + (proxy_fakefactor_weight_2 if proxy_fakefactors else fake_factor_name_2) + ")"
			ff_weight_2 = "(1.0)" if "iso_2" in exclude_cuts else "(" + (proxy_fakefactor_weight_2 if proxy_fakefactors else "(isnan("+fake_factor_name_2+")?0:"+fake_factor_name_2) + "))"
			if self.legacy:
				ff_iso_weight_2 = "((byVVVLooseDeepTau2017v2p1VSjet_2>0.5)*(byMediumDeepTau2017v2p1VSjet_2<0.5))"
			else:
				ff_iso_weight_2 = "((byVLooseIsolationMVArun2017v2DBoldDMwLT2017_2>0.5)*(byTightIsolationMVArun2017v2DBoldDMwLT2017_2<0.5))"

		if channel == "tt":
			exclude_cuts_ff += ["iso_1", "iso_2"]
			ff_weight_1 = "(" + (proxy_fakefactor_weight_1 if proxy_fakefactors else fake_factor_name_1) + ")" #factor 1/2 for tt already aplied in producer
			ff_iso_weight_1 = "((byVLooseIsolationMVArun2017v2DBoldDMwLT2017_1>0.5)*(byTightIsolationMVArun2017v2DBoldDMwLT2017_1<0.5)*(byTightIsolationMVArun2017v2DBoldDMwLT2017_2>0.5))"
			ff_weight_2 = "(" + (proxy_fakefactor_weight_2 if proxy_fakefactors else fake_factor_name_2) + ")"
			ff_iso_weight_2 = "((byVLooseIsolationMVArun2017v2DBoldDMwLT2017_2>0.5)*(byTightIsolationMVArun2017v2DBoldDMwLT2017_2<0.5)*(byTightIsolationMVArun2017v2DBoldDMwLT2017_1>0.5))"
			sub_channels = ["tt_1", "tt_2"]

		if channel == "tt":
			weight_ff = weight + "*(" + ff_weight_1 + "+" + ff_weight_2 + ")" # not used, overwritten in the subchannel loop
			weight_tau_id = "((gen_match_1 < 6) && (gen_match_2 < 6))"

		elif channel in ["mt", "et"]:
			weight_ff = weight + "*(" + ff_weight_2 + ")"
			weight_tau_id = "(gen_match_2 < 6)"


		if proxy_fakefactors:
			add_input = partialmethod(Samples._add_input, config=config, folder=self.root_file_folder(channel), scale_factor=lumi, nick_suffix=nick_suffix, proxy_prefix=proxy_prefix)
		else:
			add_input = partialmethod(Samples._add_input, config=config, folder=self.root_file_folder(channel), scale_factor=lumi, nick_suffix=nick_suffix)

		if channel in ["mt", "et", "tt"]:
			for sub_channel in sub_channels:
				weight_ff = weight + "*(" + ff_weight_1 + ")" if sub_channel == "tt_1" else weight + "*(" + ff_weight_2 + ")"
				weight_ff_iso = ff_iso_weight_1 if sub_channel == "tt_1" else ff_iso_weight_2
				# full data jetfakes
				add_input(
					input_file=self.files_data(channel),
					scale_factor=1.0,
					weight=data_weight+"*"+weight_ff+"*"+weight_ff_iso+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts+exclude_cuts_ff, cut_type=cut_type, data=True),
					nick="noplot_jetFakes_raw" + sub_channel.replace(channel,"")
				)

				add_input(
					input_file=self.files_ztt(channel, embedding=self.embedding),
					weight=mc_weight+"*"+self.ztt_genmatch(channel, embedding=self.embedding)+"*"+self.get_weights_ztt(channel=channel,cut_type=cut_type_emb,weight=weight_ff+"*"+weight_ff_iso+"*"+weight_tau_id,embedding=self.embedding)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts+exclude_cuts_ff, cut_type=cut_type_emb, embedding=self.embedding)+"*"+self.decay_mode_reweight(channel, cut_type_emb),
					scale_factor = 1.0 if self.embedding else lumi,
					nick="noplot_ff_realtaus_subtract" + sub_channel.replace(channel,"")
				)
				"""
				add_input(
					input_file=self.files_zll(channel),
					weight=self.get_weights_zll(channel=channel,cut_type=cut_type,weight=weight_ff)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts+exclude_cuts_ff, cut_type=cut_type)+"*zPtReweightWeight*(gen_match_2 < 6)",
					nick="noplot_ff_realtaus_subtract" + sub_channel.replace(channel,"")
				)"""

				add_input(
					input_file=self.files_zll(channel),
					weight=mc_weight+"*eventWeight*"+weight_ff+"*"+weight_ff_iso+"*"+weight_tau_id+"*(zPtReweightWeight)*"+self.zll_stitchingweight()+"*"+Samples.zl_genmatch(channel)+"*"+self._cut_string(channel, exclude_cuts= exclude_cuts+exclude_cuts_ff, cut_type=cut_type)+"*"+self.zll_zl_shape_weight(channel, cut_type)+"*"+zmm_cr_factor+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
					nick="noplot_ff_realtaus_subtract" + sub_channel.replace(channel,"")
					)
				add_input(
					input_file=self.files_ttj(channel),
					weight=mc_weight+"*eventWeight*"+weight_ff+"*"+weight_ff_iso+"*"+weight_tau_id+"*"+self.embedding_ttbarveto_weight(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts+exclude_cuts_ff, cut_type=cut_type),
					nick="noplot_ff_realtaus_subtract" + sub_channel.replace(channel,"")
				)
				if self.legacy:
					add_input(
							input_file=self.files_ww(channel),
							weight=mc_weight+"*eventWeight*"+weight_ff+"*"+weight_ff_iso+"*"+weight_tau_id+"*"+self.embedding_ttbarveto_weight(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts+exclude_cuts_ff, cut_type=cut_type),
							nick="noplot_ff_realtaus_subtract" + sub_channel.replace(channel,"")
					)
					add_input(
							input_file=self.files_wz(channel),
							weight=mc_weight+"*eventWeight*"+weight_ff+"*"+weight_ff_iso+"*"+weight_tau_id+"*"+self.embedding_ttbarveto_weight(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts+exclude_cuts_ff, cut_type=cut_type),
							nick="noplot_ff_realtaus_subtract" + sub_channel.replace(channel,"")
					)
					add_input(
							input_file=self.files_zz(channel),
							weight=mc_weight+"*eventWeight*"+weight_ff+"*"+weight_ff_iso+"*"+weight_tau_id+"*"+self.embedding_ttbarveto_weight(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts+exclude_cuts_ff, cut_type=cut_type),
							nick="noplot_ff_realtaus_subtract" + sub_channel.replace(channel,"")
					)
				else:
					add_input(
						input_file=self.files_wwtolnuqq(channel),
						weight=mc_weight+"*eventWeight*"+weight_ff+"*"+weight_ff_iso+"*"+weight_tau_id+"*"+self.embedding_ttbarveto_weight(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts+exclude_cuts_ff, cut_type=cut_type)+"*"+self.wwtolnuqq_stitchingweight(),
						nick="noplot_ff_realtaus_subtract" + sub_channel.replace(channel,"")
					)
					add_input(
						input_file=self.files_wwto4q(channel),
						weight=mc_weight+"*eventWeight*"+weight_ff+"*"+weight_ff_iso+"*"+weight_tau_id+"*"+self.embedding_ttbarveto_weight(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts+exclude_cuts_ff, cut_type=cut_type),
						nick="noplot_ff_realtaus_subtract" + sub_channel.replace(channel,"")
					)
					add_input(
						input_file=self.files_wzto1l3nu(channel),
						weight=mc_weight+"*eventWeight*"+weight_ff+"*"+weight_ff_iso+"*"+weight_tau_id+"*"+self.embedding_ttbarveto_weight(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts+exclude_cuts_ff, cut_type=cut_type),
						nick="noplot_ff_realtaus_subtract" + sub_channel.replace(channel,"")
					)
					add_input(
						input_file=self.files_wzto3lnu(channel),
						weight=mc_weight+"*eventWeight*"+weight_ff+"*"+weight_ff_iso+"*"+weight_tau_id+"*"+self.embedding_ttbarveto_weight(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts+exclude_cuts_ff, cut_type=cut_type),
						nick="noplot_ff_realtaus_subtract" + sub_channel.replace(channel,"")
					)
					add_input(
						input_file=self.files_zzto2l2nu(channel),
						weight=mc_weight+"*eventWeight*"+weight_ff+"*"+weight_ff_iso+"*"+weight_tau_id+"*"+self.embedding_ttbarveto_weight(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts+exclude_cuts_ff, cut_type=cut_type),
						nick="noplot_ff_realtaus_subtract" + sub_channel.replace(channel,"")
					)
					add_input(
						input_file=self.files_zzto4l(channel),
						weight=mc_weight+"*eventWeight*"+weight_ff+"*"+weight_ff_iso+"*"+weight_tau_id+"*"+self.embedding_ttbarveto_weight(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts+exclude_cuts_ff, cut_type=cut_type)+"*"+self.zzto4l_stitchingweight(),
						nick="noplot_ff_realtaus_subtract" + sub_channel.replace(channel,"")
					)
				add_input(
					input_file=self.files_singletop(channel),
					weight=mc_weight+"*eventWeight*"+weight_ff+"*"+weight_ff_iso+"*"+weight_tau_id+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts+exclude_cuts_ff, cut_type=cut_type),
					nick="noplot_ff_realtaus_subtract" + sub_channel.replace(channel,"")
				)
			if not "AddHistograms" in config.get("analysis_modules", []):
				config.setdefault("analysis_modules", []).append("AddHistograms")

			if channel == "tt":
				config.setdefault("add_nicks", []).append("noplot_jetFakes_raw_1 noplot_jetFakes_raw_2 noplot_ff_realtaus_subtract_1 noplot_ff_realtaus_subtract_2")
				config.setdefault("add_scale_factors", []).append("1. 1. -1. -1.")
			elif channel in ["mt","et"]:
				config.setdefault("add_nicks", []).append("noplot_jetFakes_raw noplot_ff_realtaus_subtract")
				config.setdefault("add_scale_factors", []).append("1. -1.")

			config.setdefault("add_result_nicks", []).append("ff")

		else:
			log.error("Sample config (FakeFactor) currently not implemented for channel \"%s\"!" % channel)

		Samples._add_plot(config, "bkg", "HIST", "F", "ff", nick_suffix)
		return config

	def wh(self, config, channel, category, weight, nick_suffix, higgs_masses, normalise_signal_to_one_pb=False, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", mssm=False, **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []

		scale_factor = lumi
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("WH", 1.0)

		data_weight, mc_weight = self.projection(kwargs)
		add_input = partialmethod(Samples._add_input, config=config, folder=self.root_file_folder(channel), scale_factor=lumi, nick_suffix=nick_suffix)

		# tauSpinner weight for CP study in the final state
		tauSpinner_weight = "(1.0)"
		if (kwargs.get("state", None) == "finalState"):
			if (kwargs.get("cp", None) == "sm"):
				tauSpinner_weight = "(tauSpinnerWeightInvSample)*(tauSpinnerWeight000)"
			if (kwargs.get("cp", None) == "mm"):
				tauSpinner_weight = "(tauSpinnerWeightInvSample)*(tauSpinnerWeight050)"
			if (kwargs.get("cp", None) == "ps"):
				tauSpinner_weight = "(tauSpinnerWeightInvSample)*(tauSpinnerWeight100)"

		wh_stitching_weight = "(1.0)"

		matrix_weight = "(1.0)"
		if kwargs.get("generator",None) =="madgraph":
			wh_stitching_weight = self.wh_stitchingweight(cp=kwargs.get("cp",None), channel=channel)
			matrix_weight = "(quarkmassWeight)*" #accounts for infinite top mass reweighting

		filter_efficiency_weight = self.cp_filterefficiency(process="wh", state=kwargs.get("state",None))

		for mass in higgs_masses:
			if channel in ["tt", "et", "mt", "em", "mm", "ee", "ttbar"]:

				add_input(
						input_file=self.files_wh(channel, mass, cp=kwargs.get("cp", None), generator=kwargs.get("generator", None), state=kwargs.get("state", None)) if not mssm else self.files_susy_wh(channel, mass),
						scale_factor=lumi*kwargs.get("scale_signal", 1.0),
						weight=tauSpinner_weight+"*"+matrix_weight+mc_weight+"*"+wh_stitching_weight+"*"+filter_efficiency_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
						nick="wh"+str(kwargs.get("generator", ""))+str(kwargs.get("cp", ""))+str(mass)+("_"+str(int(kwargs["scale_signal"])) if kwargs.get("scale_signal", 1.0) != 1.0 else "")
				)
			else:
				log.error("Sample config (wh%s) currently not implemented for channel \"%s\"!" % (str(mass), channel))

			if not kwargs.get("no_plot", False):
				if not mssm:
					Samples._add_bin_corrections(
							config,
							"wh"+str(kwargs.get("generator", ""))+str(kwargs.get("cp", ""))+str(mass)+("_"+str(int(kwargs["scale_signal"])) if kwargs.get("scale_signal", 1.0) != 1.0 else ""),
							str(kwargs.get("cp", ""))+nick_suffix
					)
				Samples._add_plot(
						config,
						"bkg" if kwargs.get("stack_signal", False) else kwargs.get("stacks", "wh"),
						"LINE",
						"L",
						"wh"+str(kwargs.get("cp", ""))+str(mass)+("_"+str(int(kwargs["scale_signal"])) if kwargs.get("scale_signal", 1.0) != 1.0 else ""),
						str(kwargs.get("cp", ""))+nick_suffix
				)
		return config

	def whsm(self, config, channel, category, weight, nick_suffix, higgs_masses, normalise_signal_to_one_pb=False, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", mssm=False, **kwargs):
		config = self.wh(config, channel, category, weight, nick_suffix, higgs_masses, normalise_signal_to_one_pb=normalise_signal_to_one_pb, lumi=lumi, exclude_cuts=exclude_cuts, cut_type=cut_type, mssm=mssm, cp="sm", state="finalState", generator="", domatrixweight=True, stacks="whsm") #TODO OLD NOT TESTED
		return config

	def whmm(self, config, channel, category, weight, nick_suffix, higgs_masses, normalise_signal_to_one_pb=False, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", mssm=False, **kwargs):
		config = self.wh(config, channel, category, weight, nick_suffix, higgs_masses, normalise_signal_to_one_pb=normalise_signal_to_one_pb, lumi=lumi, exclude_cuts=exclude_cuts, cut_type=cut_type, mssm=mssm, cp="mm", state="finalState", generator="", domatrixweight=True, stacks="whmm") #TODO OLD NOT TESTED
		return config



	def whps(self, config, channel, category, weight, nick_suffix, higgs_masses, normalise_signal_to_one_pb=False, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", mssm=False, **kwargs):
		config = self.wh(config, channel, category, weight, nick_suffix, higgs_masses, normalise_signal_to_one_pb=normalise_signal_to_one_pb, lumi=lumi, exclude_cuts=exclude_cuts, cut_type=cut_type, mssm=mssm, cp="ps", state="finalState", generator="", domatrixweight=True, stacks="whps") #TODO OLD NOT TESTED
		return config
	def zh(self, config, channel, category, weight, nick_suffix, higgs_masses, normalise_signal_to_one_pb=False, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", mssm=False, **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []

		scale_factor = lumi
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("zh", 1.0)

		data_weight, mc_weight = self.projection(kwargs)
		add_input = partialmethod(Samples._add_input, config=config, folder=self.root_file_folder(channel), scale_factor=lumi, nick_suffix=nick_suffix)

		# tauSpinner weight for CP study in the final state
		tauSpinner_weight = "(1.0)"
		if (kwargs.get("state", None) == "finalState"):
			if (kwargs.get("cp", None) == "sm"):
				tauSpinner_weight = "(tauSpinnerWeightInvSample)*(tauSpinnerWeight000)"
			if (kwargs.get("cp", None) == "mm"):
				tauSpinner_weight = "(tauSpinnerWeightInvSample)*(tauSpinnerWeight050)"
			if (kwargs.get("cp", None) == "ps"):
				tauSpinner_weight = "(tauSpinnerWeightInvSample)*(tauSpinnerWeight100)"

		zh_stitching_weight = "(1.0)"

		matrix_weight = "(1.0)"
		if kwargs.get("generator",None) =="madgraph":
			zh_stitching_weight = self.zh_stitchingweight(cp=kwargs.get("cp",None), channel=channel)
			matrix_weight = "(quarkmassWeight)*" #accounts for infinite top mass reweighting

		filter_efficiency_weight = self.cp_filterefficiency(process="zh", state=kwargs.get("state",None))

		for mass in higgs_masses:
			if channel in ["tt", "et", "mt", "em", "mm", "ee", "ttbar"]:

				add_input(
						input_file=self.files_zh(channel, mass, cp=kwargs.get("cp", None), generator=kwargs.get("generator", None), state=kwargs.get("state", None)) if not mssm else self.files_susy_zh(channel, mass),
						scale_factor=lumi*kwargs.get("scale_signal", 1.0),
						weight=tauSpinner_weight+"*"+matrix_weight+mc_weight+"*"+zh_stitching_weight+"*"+filter_efficiency_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
						nick="zh"+str(kwargs.get("generator", ""))+str(kwargs.get("cp", ""))+str(mass)+("_"+str(int(kwargs["scale_signal"])) if kwargs.get("scale_signal", 1.0) != 1.0 else "")
				)
			else:
				log.error("Sample config (zh%s) currently not implemented for channel \"%s\"!" % (str(mass), channel))

			if not kwargs.get("no_plot", False):
				if not mssm:
					Samples._add_bin_corrections(
							config,
							"zh"+str(kwargs.get("generator", ""))+str(kwargs.get("cp", ""))+str(mass)+("_"+str(int(kwargs["scale_signal"])) if kwargs.get("scale_signal", 1.0) != 1.0 else ""),
							str(kwargs.get("cp", ""))+nick_suffix
					)
				Samples._add_plot(
						config,
						"bkg" if kwargs.get("stack_signal", False) else kwargs.get("stacks", "zh"),
						"LINE",
						"L",
						"zh"+str(kwargs.get("cp", ""))+str(mass)+("_"+str(int(kwargs["scale_signal"])) if kwargs.get("scale_signal", 1.0) != 1.0 else ""),
						str(kwargs.get("cp", ""))+nick_suffix
				)
		return config

	def zhsm(self, config, channel, category, weight, nick_suffix, higgs_masses, normalise_signal_to_one_pb=False, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", mssm=False, **kwargs):
		config = self.zh(config, channel, category, weight, nick_suffix, higgs_masses, normalise_signal_to_one_pb=normalise_signal_to_one_pb, lumi=lumi, exclude_cuts=exclude_cuts, cut_type=cut_type, mssm=mssm, cp="sm", state="finalState", generator="", domatrixweight=True, stacks="zhsm") #TODO OLD NOT TESTED
		return config

	def zhmm(self, config, channel, category, weight, nick_suffix, higgs_masses, normalise_signal_to_one_pb=False, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", mssm=False, **kwargs):
		config = self.zh(config, channel, category, weight, nick_suffix, higgs_masses, normalise_signal_to_one_pb=normalise_signal_to_one_pb, lumi=lumi, exclude_cuts=exclude_cuts, cut_type=cut_type, mssm=mssm, cp="mm", state="finalState", generator="", domatrixweight=True, stacks="zhmm") #TODO OLD NOT TESTED
		return config



	def zhps(self, config, channel, category, weight, nick_suffix, higgs_masses, normalise_signal_to_one_pb=False, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", mssm=False, **kwargs):
		config = self.zh(config, channel, category, weight, nick_suffix, higgs_masses, normalise_signal_to_one_pb=normalise_signal_to_one_pb, lumi=lumi, exclude_cuts=exclude_cuts, cut_type=cut_type, mssm=mssm, cp="ps", state="finalState", generator="", domatrixweight=True, stacks="zhps") #TODO OLD NOT TESTED
		return config

