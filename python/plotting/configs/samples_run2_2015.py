
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import copy

import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.samples_run2_2016 as samples
from Kappa.Skimming.registerDatasetHelper import get_nick_list

# constants for all plots
energy = 13
class Samples(samples.Samples):

	data_format = "MINIAOD"
	mc_campaign = "RunIIFall15MiniAOD.*"

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

	def files_data(self, channel):
		query = {}
		expect_n_results = 1 # adjust in if-statements if different depending on channel
		if channel == "mt":
			query = { "process" : "SingleMuon" }
		elif channel == "et":
			query = { "process" : "SingleElectron" }
		elif channel == "em":
			query = { "process" : "MuonEG" }
		elif channel == "mm":
			query = { "process" : "DoubleMuon" }
		elif channel == "tt":
			query = { "process" : "Tau" }
		else:
			log.error("Sample config (Data) currently not implemented for channel \"%s\"!" % channel)
		query["scenario"] = "16Dec2015v1"
		query["data"] = True
		query["campaign"] = "Run2015D.*"
		return self.artus_file_names(query, expect_n_results),


	def files_ztt(self, channel):
		query = { "data" : False,
				"campaign" : self.mc_campaign,
				"generator" :  "madgraph\-pythia8",
				"process" : "(DYJetsToLLM150|DYJetsToLLM50|DY1JetsToLLM50|DY2JetsToLLM50|DY3JetsToLLM50|DY4JetsToLLM50)" }
		artus_files = self.artus_file_names(query , 6)

		query = { "data" : False,
				"campaign" : self.mc_campaign,
				"generator" :  "amcatnlo-pythia8",
				"process" : "DYJetsToLLM10to50"}
		artus_files = artus_files + " " + self.artus_file_names(query , 1)
		return artus_files


	def files_zll(self, channel):
		query = { "data" : False,
				"campaign" : self.mc_campaign,
				"generator" :  "madgraph\-pythia8",
				"process" : "(DYJetsToLLM50|DY1JetsToLLM50|DY2JetsToLLM50|DY3JetsToLLM50|DY4JetsToLLM50)" }
		artus_files = self.artus_file_names(query , 5)

		query = { "data" : False,
				"campaign" : self.mc_campaign,
				"generator" :  "amcatnlo-pythia8",
				"process" : "DYJetsToLLM10to50"}
		artus_files = artus_files + " " + self.artus_file_names(query , 1)
		return artus_files


	def files_ttj(self, channel):
		return super(Samples, self).files_ttj(channel)


	def files_vv(self, config):
		return self.artus_file_names({ "process" : "(STt-channelantitop4fleptonDecays|STt-channeltop4fleptonDecays|STtWantitop5finclusiveDecays|STtWtop5finclusiveDecays|"
		                                    + "WWTo1L1Nu2Q|"
		                                    + "WZJets|WZTo1L1Nu2Q|WZTo1L3Nu|WZTo2L2Q|" 
		                                    + "ZZTo2L2Q|ZZTo4L)",
		                      "data" : False, "campaign" : self.mc_campaign}, 11),


	def files_wj(self, channel):
		return super(Samples, self).files_wj(channel)

	def files_ggh(self, channel, mass=125):
		return super(Samples, self).files_ggh(channel)

	def files_susy_ggh(self, channel, mass=125):
		return super(Samples, self).files_susy_ggh(channel)

	def files_qqh(self, channel, mass=125):
		return super(Samples, self).files_qqh(channel)

	def files_wh_minus(self, channel, mass=125):
		return super(Samples, self).files_wh_minus(channel)

	def files_wh_plus(self, channel, mass=125):
		return super(Samples, self).files_wh_plus(channel)

	def files_zh(self, channel, mass=125):
		return super(Samples, self).files_zh(channel)

