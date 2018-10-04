
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

		mediummass = "((genbosonmass >= 50.0 && (npartons == 0 || npartons >= 5))*(5.89503542e-05)) + ((genbosonmass >= 50.0 && npartons == 1)*(2.14832024e-05)) + ((genbosonmass >= 50.0 && npartons == 2)*(2.36744541e-05)) + ((genbosonmass >= 50.0 && npartons == 3)*(3.74962884e-05))" #+((genbosonmass >= 50.0 && genbosonmass < 150.0 && npartons == 4)*(1.17409282e-05))"

		lowmass = "((genbosonmass < 50.0)*numberGeneratedEventsWeight*crossSectionPerEventWeight) +"
		normalization = "/(numberGeneratedEventsWeight*crossSectionPerEventWeight*sampleStitchingWeight)"
		#return "("+ highmass + " + " + mediummass+ " + " + lowmass +")"+normalization
		return "("+lowmass+mediummass+")"+normalization

	# DYJetsToLLM_150 sample currently only contains Z->tautau decays  5.94801691-05

	def zll_stitchingweight(self):
		mediummass = "((genbosonmass >= 50.0 && (npartons == 0 || npartons >= 5))*(5.89503542e-05)) + ((genbosonmass >= 50.0 && npartons == 1)*(2.14832024e-05)) + ((genbosonmass >= 50.0 && npartons == 2)*(2.36744541e-05)) + ((genbosonmass >= 50.0 && npartons == 3)*(3.74962884e-05))" #+((genbosonmass >= 50.0 && genbosonmass < 150.0 && npartons == 4)*(1.17409282e-05))"

		lowmass = "((genbosonmass < 50.0)*numberGeneratedEventsWeight*crossSectionPerEventWeight) +"
		normalization = "/(numberGeneratedEventsWeight*crossSectionPerEventWeight*sampleStitchingWeight)"
		#return "("+mediummass+ " + " + lowmass+")"+normalization
		return "("+lowmass+mediummass+")"+normalization

	def wj_stitchingweight(self):
		return "(((npartons == 0 || npartons >= 5)*1.37088105e-03) + ((npartons == 1)*1.37088105e-03) + ((npartons == 2)*4.09458756e-04) + ((npartons == 3)*5.67393385e-05) + ((npartons == 4)*5.04028071e-05))/(numberGeneratedEventsWeight*crossSectionPerEventWeight*sampleStitchingWeight)"

	#no stitching weights since no extensions
	def ewkz_zll_stitchingweight(self):
		return "(1)"

	def ewkz_znn_stitchingweight(self):
		return "(1)"

	def ewkwm_stitchingweight(self):
		return "(1)"

	def ewkwp_stitchingweight(self):
		return "(1)"
	
	def wgamma_stitchingweight(self):
		return "(1)"
	
	def vv_stitchingweight(self):
		return "(1)"

	def ttbar_stitchingweight(self):
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


	def files_ztt(self, channel):
		#artus_files = self.artus_file_names({"process" : "(DYJetsToLLM50|DY1JetsToLLM50|DY2JetsToLLM50|DY3JetsToLLM50)", "data": False, "campaign" : self.mc_campaign, "generator" : "madgraph\-pythia8"}, 7) #8 mit norm DY3 jets und DY4jets
		artus_files = "DY1JetsToLLM50_RunIIFall17MiniAODv2_PU2017_13TeV_MINIAOD_madgraph-pythia8_ext1/*.root DY2JetsToLLM50_RunIIFall17MiniAODv2_PU2017_13TeV_MINIAOD_madgraph-pythia8/*.root DY2JetsToLLM50_RunIIFall17MiniAODv2_PU2017_13TeV_MINIAOD_madgraph-pythia8_ext1/*.root DY3JetsToLLM50_RunIIFall17MiniAODv2_PU2017_13TeV_MINIAOD_madgraph-pythia8_ext1/*.root DYJetsToLLM10to50_RunIIFall17MiniAOD_94X_13TeV_MINIAOD_madgraph-pythia8/*.root DYJetsToLLM50_RunIIFall17MiniAODv2_PU2017RECOSIMstep_13TeV_MINIAOD_madgraph-pythia8/*.root DYJetsToLLM50_RunIIFall17MiniAODv2_PU2017RECOSIMstep_13TeV_MINIAOD_madgraph-pythia8_ext1/*.root"
		return artus_files

	def files_zll(self, channel):
		#artus_files = self.artus_file_names({"process" : "(DYJetsToLLM50|DY1JetsToLLM50|DY2JetsToLLM50|DY3JetsToLLM50)", "data": False, "campaign" : self.mc_campaign, "generator" : "madgraph\-pythia8"}, 7) #8 mit norm DY3 jets und DY4jets
		artus_files = "DY1JetsToLLM50_RunIIFall17MiniAODv2_PU2017_13TeV_MINIAOD_madgraph-pythia8_ext1/*.root DY2JetsToLLM50_RunIIFall17MiniAODv2_PU2017_13TeV_MINIAOD_madgraph-pythia8/*.root DY2JetsToLLM50_RunIIFall17MiniAODv2_PU2017_13TeV_MINIAOD_madgraph-pythia8_ext1/*.root DY3JetsToLLM50_RunIIFall17MiniAODv2_PU2017_13TeV_MINIAOD_madgraph-pythia8_ext1/*.root DYJetsToLLM10to50_RunIIFall17MiniAOD_94X_13TeV_MINIAOD_madgraph-pythia8/*.root DYJetsToLLM50_RunIIFall17MiniAODv2_PU2017RECOSIMstep_13TeV_MINIAOD_madgraph-pythia8/*.root DYJetsToLLM50_RunIIFall17MiniAODv2_PU2017RECOSIMstep_13TeV_MINIAOD_madgraph-pythia8_ext1/*.root"
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


	def files_diboson(self, channel):

		artus_files = self.artus_file_names({ "process" :
		                                      "(WW|"
		                                    + "WZ|"
		                                    + "ZZ"
		                                    +  ")",
		                      "data" : False, "campaign" : self.mc_campaign, "generator" : "pythia8"}, 3)
		artus_files = artus_files + " " + self.artus_file_names({ "process" : "(STtWantitop5finclusiveDecaysTuneCP5|STtWtop5finclusiveDecaysTuneCP5)",
							"data" : False, "campaign" : self.mc_campaign}, 2)
		artus_files = artus_files + " " + self.artus_file_names({ "process" : "(STt-channelantitop4finclusiveDecaysTuneCP5|STt-channeltop4finclusiveDecaysTuneCP5)",
		                      "data" : False, "campaign" : self.mc_campaign}, 2)
		return artus_files

	#TODO do something similar for ggh like files_qqh if needed

	def files_qqh(self, channel, mass=125, **kwargs):
		cp = kwargs.get("cp", None)
		print "this is VBF"
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
		if cp is None or cp == "cpeven":
			#CAUTION: If necessary the mc-generator nick might need to be updated from time to time.
			return self.artus_file_names({"process" : "GluGluHToTauTau_M"+str(mass), "data": False, "campaign" : self.mc_campaign, "generator" : "powheg-pythia8"}, 1)
		
		elif "jhu" in cp:
			if "sm" in cp:
				return "JJHiggs0PMToTauTauPseudoscalarDecayM125_RunIIFall17MiniAODv2_PU2017_13TeV_MINIAOD_JHUgen-pythia8/*.root" #FIXME change to total sm		
			if "ps" in cp:
				return "JJHiggs0MToTauTauM125_RunIIFall17MiniAODv2_PU2017_13TeV_MINIAOD_JHUgen-pythia8/*.root"
			if "mm" in cp:
				return "JJHiggs0Mf05ph0ToTauTauM125_RunIIFall17MiniAODv2_PU2017_13TeV_MINIAOD_JHUgen-pythia8/*.root"
		elif cp in ["sm", "mm", "ps"]:
			return "GluGluToHToTauTauM125_RunIIFall15MiniAODv2_PU25nsData2015v1_13TeV_MINIAOD_amcatnlo-pythia8/*.root"

	def files_vv(self, channel):
		return None

	#missing w1jets in das
	def files_wj(self, channel):
		artus_files = self.artus_file_names({"process" : "W.*JetsToLNu", "data" : False, "campaign" : self.mc_campaign, "generator" : "madgraph-pythia8"}, 4)
		return artus_files


	
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
			ss_os_factor = 1.218 #TODO for 2017
		elif channel == "et":
			ss_os_factor = 1.361 #TODO for 2017
		else:
			ss_os_factor = 0.0



		return super(Samples, self).wj(config, channel, category, weight, nick_suffix, lumi=default_lumi, exclude_cuts=exclude_cuts, cut_type=cut_type, fakefactor_method=fakefactor_method, estimationMethod=estimationMethod, controlregions=controlregions, ss_os_factor=ss_os_factor, **kwargs)

	

