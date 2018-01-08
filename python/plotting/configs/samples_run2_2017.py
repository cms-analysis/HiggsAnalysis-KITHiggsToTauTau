
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)


import pprint
import copy
import sys

import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.samples_run2_2016 as samples
from Kappa.Skimming.registerDatasetHelper import get_nick_list


from Artus.Utility.tools import make_multiplication, split_multiplication, clean_multiplication
energy = 13
default_lumi =  42.0*1000.0

class Samples(samples.Samples):


	# constants for all plots
	data_format = "MINIAOD"
	mc_campaign = "RunIISummer17MiniAOD"

	#NOTES: zPtReweightWeight is used for 2016 values currently.

	# For 2017 v1 MC samples, remove the npartons=4 part since we don't have the sample yet, and also remove the highmass part in your return value if you have don't use the high mass sample!
	def ztt_stitchingweight(self):
		highmass = "((genbosonmass >= 150.0 && (npartons == 0 || npartons >= 5))*1.25469132e-3) + ((genbosonmass >= 150.0 && npartons == 1)*1.17290378e-3) + ((genbosonmass >= 150.0 && npartons == 2)*1.17845742e-3) + ((genbosonmass >= 150.0 && npartons == 3)*1.18139540e-3)+((genbosonmass >= 150.0 && npartons == 4)*1.15891212e-3)+"
		mediummass = "((genbosonmass >= 50.0 && genbosonmass < 150.0 && (npartons == 0 || npartons >= 5))*5.75970078e-5) + ((genbosonmass >= 50.0 && genbosonmass < 150.0 && npartons == 1)*1.36277241e-5) + ((genbosonmass >= 50.0 && genbosonmass < 150.0 && npartons == 2)*7.42888435e-6) + ((genbosonmass >= 50.0 && genbosonmass < 150.0 && npartons == 3)*1.62808443e-5)+ ((genbosonmass >= 50.0 && genbosonmass < 150.0 && npartons == 4)*5.75970078e-5)+"
		#mediummass = "((genbosonmass >= 50.0 && genbosonmass < 150.0 && (npartons == 0 || npartons >= 5))*5.75970078e-5) + ((genbosonmass >= 50.0 && genbosonmass < 150.0 && npartons == 1)*1.36277241e-5) + ((genbosonmass >= 50.0 && genbosonmass < 150.0 && npartons == 2)*7.42888435e-6) + ((genbosonmass >= 50.0 && genbosonmass < 150.0 && npartons == 3)*1.62808443e-5)+"
		lowmass = "((genbosonmass < 50.0)*numberGeneratedEventsWeight*crossSectionPerEventWeight)"
		normalization = "/(numberGeneratedEventsWeight*crossSectionPerEventWeight*sampleStitchingWeight)"
		return "("+highmass+mediummass+lowmass+")"+normalization
		#return "("+mediummass+lowmass+")"+normalization


	# DYJetsToLLM_150 sample currently only contains Z->tautau decays
	def zll_stitchingweight(self):
		mediummass = "((genbosonmass >= 50.0 && (npartons == 0 || npartons >= 5))*5.75970078e-5) + ((genbosonmass >= 50.0 && npartons == 1)*1.36277241e-5) + ((genbosonmass >= 50.0 && npartons == 2)*7.42888435e-6) + ((genbosonmass >= 50.0 && npartons == 3)*1.62808443e-5) + ((genbosonmass >= 50.0 && npartons == 4)*5.75970078e-5)+"
		lowmass = "((genbosonmass < 50.0)*numberGeneratedEventsWeight*crossSectionPerEventWeight)"
		normalization = "/(numberGeneratedEventsWeight*crossSectionPerEventWeight*sampleStitchingWeight)"
		return "("+mediummass+lowmass+")"+normalization

	def wj_stitchingweight(self):
		return "(((npartons == 0 || npartons >= 5)*2.36006270e-3) + ((npartons == 1)*2.34817764e-4) + ((npartons == 2)*1.31144867e-4) + ((npartons == 3)*1.39177532e-4) + ((npartons == 4)*6.46064804e-5))/(numberGeneratedEventsWeight*crossSectionPerEventWeight*sampleStitchingWeight)"


	def files_data(self, channel):
		query_rereco = {}
		query_promptreco = {}
		query_reminiaod = {}
		expect_n_results_rereco = 2 # adjust in if-statements if different depending on channel
		expect_n_results_promptreco = 3
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
		query_rereco["campaign"] = "Run2017(B|C)"
		query_rereco["scenario"] = "12Sep2017v(1|3)"
		query_promptreco["data"] = True
		query_promptreco["campaign"] = "Run2017(D|E|F)"
		query_promptreco["scenario"] = "PromptRecov(1|2)"
		query_reminiaod["data"] = True
		query_reminiaod["campaign"] = "Run2017(B|C|D|E|F|G|H)"
		query_reminiaod["scenario"] = "12Sep2017*"

		rereco_files = self.artus_file_names(query_rereco, expect_n_results_rereco)
		promptreco_files = self.artus_file_names(query_promptreco, expect_n_results_promptreco)
		reminiaod_files = self.artus_file_names(query_reminiaod, expect_n_results_reminiaod)
		return rereco_files + " " + promptreco_files
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


	def files_ztt(self, channel):
		return self.artus_file_names({"process" : "(DYJetsToLLM50|DYJetsToLLM50v1|DY1JetsToLLM50|DY2JetsToLLM50|DY3JetsToLLM50)", "data": False, "campaign" : self.mc_campaign, "generator" : "madgraph\-pythia8"}, 5)

	def files_zll(self, channel):
		return self.artus_file_names({"process" : "(DYJetsToLLM50|DYJetsToLLM50v1|DY1JetsToLLM50|DY2JetsToLLM50|DY3JetsToLLM50)", "data": False, "campaign" : self.mc_campaign, "generator" : "madgraph\-pythia8"},5)

	def files_ewkwm(self, channel):
		return None

	def files_ewkwp(self, channel):
		return None

	def files_ewkz_zll(self, channel):
		return None

	def files_ewkz_znn(self, channel):
		return None

	def files_ttj(self, channel):
		if self.ttbar_retuned:
			return self.artus_file_names({"process" : "TTTo.*", "data": False, "campaign" : self.mc_campaign}, 2)
		else:
			return self.artus_file_names({"process" : "TTv1_|TTv2_", "data": False, "campaign" : self.mc_campaign}, 2)

	def files_diboson(self, channel):

		artus_files = self.artus_file_names({ "process" :
		                                      "(WW|"
		                                    + "WZ|"
		                                    + "ZZ"
		                                    +  ")",
		                      "data" : False, "campaign" : self.mc_campaign, "generator" : "pythia8"}, 3)
		artus_files = artus_files + " " + self.artus_file_names({ "process" : "(STtWantitop5finclusiveDecays|STtWtop5finclusiveDecays)",
		                      "data" : False, "campaign" : self.mc_campaign}, 2)
		return artus_files

	def files_vv(self, channel):
		return None

	def files_wj(self, channel):
		artus_files = self.artus_file_names({"process" : "W.*JetsToLNu", "data" : False, "campaign" : self.mc_campaign, "generator" : "madgraph-pythia8"}, 5)
		return artus_files
