
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

	data_format = "MINIAOD"
	mc_campaign = "RunIIFall15MiniAOD.*"
		
	def __init__(self,embedding=False):
		super(Samples, self).__init__()
		self.embedding=embedding
	
	def ztt_stitchingweight(self):
		highmass = "((genbosonmass >= 150.0 && (npartons == 0 || npartons >= 5))*1.26276e-6) + ((genbosonmass >= 150.0 && npartons == 1)*1.18349e-6) + ((genbosonmass >= 150.0 && npartons == 2)*1.18854e-6) + ((genbosonmass >= 150.0 && npartons == 3)*1.19334e-6) + ((genbosonmass >= 150.0 && npartons == 4)*1.16985e-6)+"
		mediummass = "((genbosonmass >= 50.0 && genbosonmass < 150.0 && (npartons == 0 || npartons >= 5))*2.43669e-5) + ((genbosonmass >= 50.0 && genbosonmass < 150.0 && npartons == 1)*1.06292e-5) + ((genbosonmass >= 50.0 && genbosonmass < 150.0 && npartons == 2)*1.10505e-5) + ((genbosonmass >= 50.0 && genbosonmass < 150.0 && npartons == 3)*1.14799e-5) + ((genbosonmass >= 50.0 && genbosonmass < 150.0 && npartons == 4)*9.62135e-6)+"
		lowmass = "((genbosonmass < 50.0)*numberGeneratedEventsWeight*crossSectionPerEventWeight)"
		normalization = "/(numberGeneratedEventsWeight*crossSectionPerEventWeight*sampleStitchingWeight)"
		return "("+highmass+mediummass+lowmass+")"+normalization

	# DYJetsToLLM_150 sample currently only contains Z->tautau decays
	def zll_stitchingweight(self):
		mediummass = "((genbosonmass >= 50.0 && genbosonmass < 150.0 && (npartons == 0 || npartons >= 5))*2.43669e-5) + ((genbosonmass >= 50.0 && genbosonmass < 150.0 && npartons == 1)*1.06292e-5) + ((genbosonmass >= 50.0 && genbosonmass < 150.0 && npartons == 2)*1.10505e-5) + ((genbosonmass >= 50.0 && genbosonmass < 150.0 && npartons == 3)*1.14799e-5) + ((genbosonmass >= 50.0 && genbosonmass < 150.0 && npartons == 4)*9.62135e-6)+"
		lowmass = "((genbosonmass < 50.0)*numberGeneratedEventsWeight*crossSectionPerEventWeight)"
		normalization = "/(numberGeneratedEventsWeight*crossSectionPerEventWeight*sampleStitchingWeight)"
		return "("+mediummass+lowmass+")"+normalization

	def wj_stitchingweight(self):
		return "(((npartons == 0 || npartons >= 5)*1.3046006677e-3) + ((npartons == 1)*2.162338159e-4) + ((npartons == 2)*1.159006627e-4) + ((npartons == 3)*5.82002641e-5) + ((npartons == 4)*6.27558901e-05))/(numberGeneratedEventsWeight*crossSectionPerEventWeight*sampleStitchingWeight)"

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
		return self.artus_file_names(query, expect_n_results)

	def files_dy_m50(self, channel):
		return self.artus_file_names({"process" : "DYJetsToLLM50", "data": False, "campaign" : self.mc_campaign, "generator" : "madgraph\-pythia8"}, 1)

	def files_ztt(self, channel):
		if self.embedding:
			return self.artus_file_names({"process" : "Embedding2015D" , "campaign" : "MuTauFinalState" }, 1)
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
	
	def files_ewkz(self, channel):
		ewkz_query = { "data" : False,
						"campaign" : self.mc_campaign,
						"generator" : "madgraph-pythia8",
						"process" : "EWKZ2Jets.*"}
		artus_files = self.artus_file_names(ewkz_query, 2)
		return artus_files


	def files_ttj(self, channel):
		return self.artus_file_names({"process" : "TT", "data": False, "campaign" : self.mc_campaign+"2" }, 1)


	def files_vv(self, config):
		return self.artus_file_names({ "process" : "(STt-channelantitop4fleptonDecays|STt-channeltop4fleptonDecays|STtWantitop5finclusiveDecays|STtWtop5finclusiveDecays|"
		                                    + "WWTo1L1Nu2Q|"
		                                    + "WZJToLLLNu|WZTo1L1Nu2Q|WZTo1L3Nu|WZTo2L2Q|" 
		                                    + "ZZTo2L2Q|ZZTo4L|VVTo2L2Nu)",
		                      "data" : False, "campaign" : self.mc_campaign}, 12)


	def files_wj(self, channel):
		# W + N jets from MiniAODv2
		query = { "data" : False,
						"campaign" : self.mc_campaign,
						"generator" : "madgraph-pythia8",
						"process" : "(WJetsToLNu|W1JetsToLNu|W2JetsToLNu|W3JetsToLNu|W4JetsToLNu)"}
		artus_files = self.artus_file_names(query, 5)
		return artus_files

	def files_ggh(self, channel, mass=125):
		return self.artus_file_names({"process" : "GluGluHToTauTau_M"+str(mass), "data": False, "campaign" : self.mc_campaign }, 1)
	
	def files_bbh(self, channel, mass=125):
		return self.artus_file_names({"process" : "SUSYGluGluToBBHToTauTau_M"+str(mass), "data": False, "campaign" : self.mc_campaign }, 1)

	def files_susy_ggh(self, channel, mass=125):
		return self.artus_file_names({"process" : "SUSYGluGluToHToTauTauM"+str(mass), "data": False, "campaign" : self.mc_campaign}, 1)

	def files_qqh(self, channel, mass=125):
		return self.artus_file_names({"process" : "VBFHToTauTau_M"+str(mass), "data": False, "campaign" : self.mc_campaign}, 1)

	def files_wh_minus(self, channel, mass=125):
		return self.artus_file_names({"process" : "WminusHToTauTau_M"+str(mass), "data": False, "campaign" : self.mc_campaign}, 1)

	def files_wh_plus(self, channel, mass=125):
		return self.artus_file_names({"process" : "WplusHToTauTau_M"+str(mass), "data": False, "campaign" : self.mc_campaign}, 1)

	def files_zh(self, channel, mass=125):
		return self.artus_file_names({"process" : "ZHToTauTau_M"+str(mass), "data": False, "campaign" : self.mc_campaign}, 1)

