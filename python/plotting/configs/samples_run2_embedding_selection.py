# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import copy

import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.samples_run2_2016 as samples
from Kappa.Skimming.registerDatasetHelper import get_nick_list

# constants for all plots
energy = 13
default_lumi = 2.301*1000.0

class Samples(samples.Samples):

	### General settings
	data_format = "MINIAOD"
	mc_campaign = "RunIIFall15MiniAOD.*"

	@staticmethod 
	def root_file_folder(channel):
		return channel + "/ntuple"

	# needs to be overwritten since extentions have not been available in Fall15 nicks
	@staticmethod
	def artus_file_names( query, expect_n_results = 1):
		query["energy"] = energy
		found_file_names = []
		for nick in get_nick_list ( query, expect_n_results = expect_n_results):
			if("ext") in nick:
				nick = nick[0:nick.rfind("_")]
			found_file_names.append(nick  + "/*.root")
		return " ".join(found_file_names) # convert it to a HP-readable format

	### Data (Double Muon) settings
	def files_data(self, channel):
		query = {}
		if channel == "zmumu_selection_for_embedding":
			query = { "process" : "DoubleMuon" }
		else:
			log.error("Sample config (Data) currently not implemented for channel \"%s\"!" % channel)
		query["scenario"] = "16Dec2015v1"
		query["data"] = True
		query["campaign"] = "Run2015D.*"
		return self.artus_file_names(query, 1)

	def data(self, config, channel, category, weight, nick_suffix, exclude_cuts=None, cut_type="baseline", **kwargs):

		Samples._add_input(
				config,
				self.files_data(channel),
				self.root_file_folder(channel),
				1.0,
				"eventWeight*(ZMass>50)",
				"data",
				nick_suffix=nick_suffix
		)

		Samples._add_plot(config, "data", "E", "ELP", "data", nick_suffix)
		return config

	### DYJetsToLL settings
	def files_zll(self, channel):
		query = { "data" : False,
				"campaign" : self.mc_campaign,
				"generator" :  "amcatnlo-pythia8",
				"process" : "DYJetsToLLM50" }
		artus_files = self.artus_file_names(query , 1)

		query = { "data" : False,
				"campaign" : self.mc_campaign,
				"generator" :  "amcatnlo-pythia8",
				"process" : "DYJetsToLLM10to50"}
		artus_files = artus_files + " " + self.artus_file_names(query , 1)
		return artus_files

	def zll(self, config, channel, category, weight, nick_suffix, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", fakefactor_method=None, **kwargs):

		data_weight, mc_weight = self.projection(kwargs) 

		if channel == "zmumu_selection_for_embedding":
			Samples._add_input(
					config,
					self.files_zll(channel),
					self.root_file_folder(channel),
					lumi,
					"eventWeight*(ZMass>50)",
					"zll",
					nick_suffix=nick_suffix
			)
		else:
			log.error("Sample config (ZLL) currently not implemented for channel \"%s\"!" % channel)
		
		Samples._add_plot(config, "bkg", "HIST", "F", "zll", nick_suffix)
		return config

	### TTbar settings
	def files_ttj(self, channel):
		return self.artus_file_names({"process" : "TT", "data": False, "campaign" : self.mc_campaign+"2" }, 1)

	def ttj(self, config, channel, category, weight, nick_suffix, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", fakefactor_method=None, **kwargs):

		if channel == "zmumu_selection_for_embedding":
			Samples._add_input(
					config,
					self.files_ttj(channel),
					self.root_file_folder(channel),
					lumi,
					"eventWeight*(ZMass>50)",
					"ttj",
					nick_suffix=nick_suffix
			)
		else:
			log.error("Sample config (TTJ) currently not implemented for channel \"%s\"!" % channel)
		
		Samples._add_plot(config, "bkg", "HIST", "F", "ttj", nick_suffix)
		return config

	### DiBoson settings
	def files_vv(self, config):
		return self.artus_file_names({ "process" : "(STt-channelantitop4fleptonDecays|STt-channeltop4fleptonDecays|STtWantitop5finclusiveDecays|STtWtop5finclusiveDecays|"
												 + "WWTo1L1Nu2Q|"
												 + "WZJToLLLNu|WZTo1L1Nu2Q|WZTo1L3Nu|WZTo2L2Q|"
												 + "ZZTo2L2Q|ZZTo4L|VVTo2L2Nu)",
		                      "data" : False, "campaign" : self.mc_campaign}, 12)

	def vv(self, config, channel, category, weight, nick_suffix, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", fakefactor_method=None, **kwargs):

		if channel == "zmumu_selection_for_embedding":
			Samples._add_input(
					config,
					self.files_vv(channel),
					self.root_file_folder(channel),
					lumi,
					"eventWeight*(ZMass>50)",
					"vv",
					nick_suffix=nick_suffix
			)
		else:
			log.error("Sample config (VV) currently not implemented for channel \"%s\"!" % channel)

		Samples._add_plot(config, "bkg", "HIST", "F", "vv", nick_suffix)
		return config

	### W+Jets settings
	def files_wj(self, channel):
		query = { "data" : False,
						"campaign" : self.mc_campaign,
						"generator" : "amcatnlo-pythia8",
						"process" : "WJetsToLNu"}
		artus_files = self.artus_file_names(query, 1)
		return artus_files

	def wj(self, config, channel, category, weight, nick_suffix, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", fakefactor_method=None, estimationMethod="classic", controlregions=False,**kwargs):

		if channel == "zmumu_selection_for_embedding":
			Samples._add_input(
					config,
					self.files_wj(channel),
					self.root_file_folder(channel),
					lumi,
					"eventWeight*(ZMass>50)",
					"wj",
					nick_suffix=nick_suffix
			)
		else:
			log.error("Sample config (WJets) currently not implemented for channel \"%s\"!" % channel)

		Samples._add_plot(config, "bkg", "HIST", "F", "wj", nick_suffix)
		return config
		
