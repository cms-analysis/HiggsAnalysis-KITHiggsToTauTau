# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import pprint
import copy
import sys
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.samples as samples
from Kappa.Skimming.registerDatasetHelper import get_nick_list
from Artus.Utility.tools import make_multiplication, split_multiplication, clean_multiplication
from functools import wraps, partial
energy = 13
default_lumi =  35.87*1000.0

class partialmethod(partial):
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return partial(self.func, instance,
                       *(self.args or ()), **(self.keywords or {}))


class Samples(samples.SamplesBase):


	# constants for all plots
	data_format = "MINIAOD"
	mc_campaign = "RunIISummer16MiniAODv2"
	
	
	@staticmethod 
	def root_file_folder(channel):
		if channel == "inclusive":
			return "inclusive/ntuple"
		elif channel == "gen":
			return "gen/ntuple"
		elif channel == "ttbar":
			return "em_nominal/ntuple"
		else:
			return channel+"_nominal/ntuple"

	@staticmethod
	def artus_file_names( query, expect_n_results = 1):
		query["energy"] = energy
		found_file_names = []
		for nick in get_nick_list ( query, expect_n_results = expect_n_results):
			found_file_names.append(nick + "/*.root")
		return " ".join(found_file_names) # convert it to a HP-readable format

	@staticmethod
	def ttt_genmatch(channel, kwargs):
		if channel in ["mt", "et"]:
			if kwargs.get("mssm", False):
				return "(gen_match_2 < 6)"
			else:
				return "(gen_match_2 == 5)"
		elif channel == "tt":
			return "(gen_match_1 == 5 && gen_match_2 == 5)"
		else:
			log.fatal("No TTT/TTJ selection implemented for channel \"%s\"!" % channel)
			sys.exit(1)

	@staticmethod
	def ttj_genmatch(channel, kwargs):
		return "(!("+Samples.ttt_genmatch(channel,kwargs)+"))"

	# In order to specify the channels in gen-level info, one also needs the category as a parameter of the matching function!
		#(In the so-called "gen" channel, the categories are considered as tt,mt,et... channels for now,
		# it will be adapted later considering the decay products of tau's)
	@staticmethod
	def ztt_genchannelmatch(channel, category):
		category = category.split("_")[-1]
		if channel in ["gen"]:
			if category == "tt":
				return "genTauTauDecayMode == 1"
			elif category == "mt":
				return "genTauTauDecayMode == 2"
			elif category == "et":
				return "genTauTauDecayMode == 3"
			elif category == "mm":
				return "genTauTauDecayMode == 4"
			elif category == "em" or category == "ttbar":
				return "genTauTauDecayMode == 5"
			elif category == "ee":
				return "genTauTauDecayMode == 6"
		else:
			log.fatal("No ZTT selection implemented for channel \"%s\"!" % channel)
			sys.exit(1)

	@staticmethod
	def ztt_genmatch(channel):
		if channel in ["mt", "et"]:
			return "(gen_match_2 == 5)"
		elif channel == "em" or channel == "ttbar":
			return "(gen_match_1 > 2 && gen_match_2 > 3)"
		elif channel == "mm":
			return "(gen_match_1 > 3 && gen_match_2 > 3)"
		elif channel == "ee":
			return "(gen_match_1 > 3 && gen_match_2 > 3)"
		elif channel == "tt":
			return "(gen_match_1 == 5 && gen_match_2 == 5)"
		else:
			log.fatal("No ZTT selection implemented for channel \"%s\"!" % channel)
			sys.exit(1)

	@staticmethod
	def zl_genmatch(channel):
		if channel in ["mt", "et"]:
			return "(gen_match_2 < 5)"
		elif channel == "tt":
			return "(gen_match_1 < 6 && gen_match_2 < 6 && (!(gen_match_1 == 5 && gen_match_2 == 5)))"
		else:
			log.fatal("No ZL selection implemented for channel \"%s\"!" % channel)
			sys.exit(1)

	@staticmethod
	def zj_genmatch(channel):
		if channel in ["mt", "et"]:
			return "(gen_match_2 == 6)"
		elif channel == "tt":
			return "(gen_match_2 == 6 || gen_match_1 == 6)"
		else:
			log.fatal("No ZJ selection implemented for channel \"%s\"!" % channel)
			sys.exit(1)

	@staticmethod
	def zll_genmatch(channel):
		if channel in ["mt", "et"]:
			return "(gen_match_2 < 5 || gen_match_2 == 6)"
		elif channel == "em" or channel == "ttbar":
			return "(gen_match_1 < 3 || gen_match_2 < 4)"
		elif channel == "mm":
			return "(gen_match_1 < 4 || gen_match_2 < 4)"
		elif channel == "ee":
			return "(gen_match_1 < 4 || gen_match_2 < 4)"
		elif channel == "tt":
			return "((gen_match_1 < 6 && gen_match_2 < 6 && (!(gen_match_1 == 5 && gen_match_2 == 5))) || gen_match_2 == 6 || gen_match_1 == 6)"
		else:
			log.fatal("No ZLL selection implemented for channel \"%s\"!" % channel)
			sys.exit(1)

	@staticmethod
	def get_jetbin(channel, category, weight):
		if category == None:
			return [weight]
		addition = split_multiplication(weight)[1]
		if("x") in category:
			if "1jet" in category:
				return ["(njetspt30==1)", addition]
			if "vbf" in category:
				return ["(njetspt30==1)", addition]
		else:
			if "1jet" in category:
				return ["(njetspt30==1)", addition]
			if "vbf" in category:
				return ["(njetspt30>1)", addition]
			return [weight]

	def ztt_stitchingweight(self):
		highmass = "((genbosonmass >= 150.0 && (npartons == 0 || npartons >= 5))*3.95423374e-5) + ((genbosonmass >= 150.0 && npartons == 1)*1.27486147e-5) + ((genbosonmass >= 150.0 && npartons == 2)*1.3012785e-5) + ((genbosonmass >= 150.0 && npartons == 3)*1.33802133e-5) + ((genbosonmass >= 150.0 && npartons == 4)*1.09698723e-5)+"
		mediummass = "((genbosonmass >= 50.0 && genbosonmass < 150.0 && (npartons == 0 || npartons >= 5))*3.95423374e-5) + ((genbosonmass >= 50.0 && genbosonmass < 150.0 && npartons == 1)*1.27486147e-5) + ((genbosonmass >= 50.0 && genbosonmass < 150.0 && npartons == 2)*1.3012785e-5) + ((genbosonmass >= 50.0 && genbosonmass < 150.0 && npartons == 3)*1.33802133e-5) + ((genbosonmass >= 50.0 && genbosonmass < 150.0 && npartons == 4)*1.09698723e-5)+"
		lowmass = "((genbosonmass < 50.0)*numberGeneratedEventsWeight*crossSectionPerEventWeight)"
		normalization = "/(numberGeneratedEventsWeight*crossSectionPerEventWeight*sampleStitchingWeight)"
		return "("+highmass+mediummass+lowmass+")"+normalization

	def embedding_ttbarveto_weight(self,channel):
		if self.embedding:
			if channel == "mt":
				return "(!((gen_match_1 == 4) && (gen_match_2 == 5)))"
			elif channel == "et":
				return "(!((gen_match_1 == 3) && (gen_match_2 == 5)))"
			elif channel == "tt":
				return "(!((gen_match_1 == 5) && (gen_match_2 == 5)))"
			elif channel == "em":
				return "(!((gen_match_1 == 3) && (gen_match_2 == 4)))"
			else:
				log.error("Embedding currently not implemented for channel \"%s\"!" % channel)
		else:
			return "(1.0)"	
	
	def tttautau_genmatch(self,channel):
		if channel == "mt":
			return "((gen_match_1 == 4) && (gen_match_2 == 5))"
		elif channel == "et":
			return "((gen_match_1 == 3) && (gen_match_2 == 5))"
		elif channel == "tt":
			return "((gen_match_1 == 5) && (gen_match_2 == 5))"
		elif channel == "em":
			return "((gen_match_1 == 3) && (gen_match_2 == 4))"
		else:
			log.error("TTTAUTAU currently not implemented for channel \"%s\"!" % channel)

	def embedding_stitchingweight(self,channel):
		if channel=='mt':
			runB = "((run >= 272007) && (run < 275657))*3768958.+"
			runC = "((run >= 275657) && (run < 276315))*1583897.+"
			runD = "((run >= 276315) && (run < 276831))*2570815.+"
			runE = "((run >= 276831) && (run < 277772))*2514506.+"
			runF = "((run >= 277772) && (run < 278820))*1879819.+"
			runG = "((run >= 278820) && (run < 280919))*5008746.+"
			runH = "((run >= 280919) && (run < 284045))*6325743."
			totalevents = "3768958.+1583897.+2570815.+2514506.+1879819.+5008746.+6325743."
			return "("+runB+runC+runD+runE+runF+runG+runH+")/("+totalevents+")"
		elif channel=='et':
			runB = "((run >= 272007) && (run < 275657))*3570181.+"
			runC = "((run >= 275657) && (run < 276315))*1543340.+"
			runD = "((run >= 276315) && (run < 276831))*2614984.+"
			runE = "((run >= 276831) && (run < 277772))*2387033.+"
			runF = "((run >= 277772) && (run < 278820))*1733082.+"
			runG = "((run >= 278820) && (run < 280919))*4700036.+"
			runH = "((run >= 280919) && (run < 284045))*5830114."
			totalevents = "3570181.+1543340.+2614984.+2387033.+1733082.+4700036.+5830114."
			return "("+runB+runC+runD+runE+runF+runG+runH+")/("+totalevents+")"
		elif channel=='tt':
			runB = "((run >= 272007) && (run < 275657))*1331777.+"
			runC = "((run >= 275657) && (run < 276315))*577219.+"
			runD = "((run >= 276315) && (run < 276831))*984751.+"
			runE = "((run >= 276831) && (run < 277772))*813524.+"
			runF = "((run >= 277772) && (run < 278820))*665461.+"
			runG = "((run >= 278820) && (run < 280919))*1773204."
			totalevents = "1331777.+577219.+984751.+813524.+665461.+1773204."
			return "("+runB+runC+runD+runE+runF+runG+")/("+totalevents+")"
		elif channel=='em':
			runB = "((run >= 272007) && (run < 275657))*4475455.+"
			runC = "((run >= 275657) && (run < 276315))*1961248.+"
			runD = "((run >= 276315) && (run < 276831))*3356220.+"
			runE = "((run >= 276831) && (run < 277772))*3055567.+"
			runF = "((run >= 277772) && (run < 278820))*2280011.+"
			runG = "((run >= 278820) && (run < 280919))*5993673."
			totalevents = "4475455.+1961248.+3356220.+3055567.+2280011.+5993673."
			return "("+runB+runC+runD+runE+runF+runG+")/("+totalevents+")"
		else:
			log.error("Embedding currently not implemented for channel \"%s\"!" % channel)
		

	# DYJetsToLLM_150 sample currently only contains Z->tautau decays
	def zll_stitchingweight(self):
		mediummass = "((genbosonmass >= 50.0 && (npartons == 0 || npartons >= 5))*3.95423374e-5) + ((genbosonmass >= 50.0 && npartons == 1)*1.27486147e-5) + ((genbosonmass >= 50.0 && npartons == 2)*1.3012785e-5) + ((genbosonmass >= 50.0 && npartons == 3)*1.33802133e-5) + ((genbosonmass >= 50.0 && npartons == 4)*1.09698723e-5)+"
		lowmass = "((genbosonmass < 50.0)*numberGeneratedEventsWeight*crossSectionPerEventWeight)"
		normalization = "/(numberGeneratedEventsWeight*crossSectionPerEventWeight*sampleStitchingWeight)"
		return "("+mediummass+lowmass+")"+normalization

	def wj_stitchingweight(self):
		return "(((npartons == 0 || npartons >= 5)*7.09390278348407e-4) + ((npartons == 1)*1.90063898596475e-4) + ((npartons == 2)*5.8529964471165e-5) + ((npartons == 3)*1.9206444928444e-5) + ((npartons == 4)*1.923548021385e-5))/(numberGeneratedEventsWeight*crossSectionPerEventWeight*sampleStitchingWeight)"

	def ewkz_zll_stitchingweight(self):
		return "(3.989190065346e-6)/(numberGeneratedEventsWeight*crossSectionPerEventWeight)"

	def ewkz_znn_stitchingweight(self):
		return "(3.35561920393e-6)/(numberGeneratedEventsWeight*crossSectionPerEventWeight)"

	def ewkwm_stitchingweight(self):
		return "(4.200367267668e-6)/(numberGeneratedEventsWeight*crossSectionPerEventWeight)"

	def ewkwp_stitchingweight(self):
		return "(5.190747826298e-6)/(numberGeneratedEventsWeight*crossSectionPerEventWeight)"
	
	def wgamma_stitchingweight(self):
		return "(1.7829004749953e-5)/(numberGeneratedEventsWeight*crossSectionPerEventWeight)"
	
	def vv_stitchingweight(self):
		return "(1.22671436926e-6)/(numberGeneratedEventsWeight*crossSectionPerEventWeight)"
	
	# reweighting of l->tau fakes in ZL as done in SM HTT 2016 
	def zl_shape_weight(self, channel, cut_type):
		if "smhtt2016" in cut_type:
			if channel == "mt":
				return "(((decayMode_2 == 0)*0.75) + ((decayMode_2 == 1 || decayMode_2 == 2)*1.0) + ((decayMode_2 == 10)*1.0))"
			elif channel == "et":
				return "(((decayMode_2 == 0)*0.98) + ((decayMode_2 == 1 || decayMode_2 == 2)*1.2) + ((decayMode_2 == 10)*1.0))"
			else:
				return "(1.0)"
		else:
			return "(1.0)"
	
	# reweighting of l->tau fakes in ZL as done in SM HTT 2016
	# this function is needed since background methods for W+jets and QCD
	# use zll instead of zl+zj separately
	def zll_zl_shape_weight(self, channel, cut_type):
		if "smhtt2016" in cut_type and channel in ["mt", "et"]:
			return "(("+self.zl_genmatch(channel)+"*"+self.zl_shape_weight(channel, cut_type)+") + "+self.zj_genmatch(channel)+")"
		else:
			return "(1.0)"
	
	# decay mode reweighting (currently no default reweighting but only used as workaround for shape systematics)
	def decay_mode_reweight(self, channel):
		if channel in ["et", "mt"]:
			return "(((decayMode_2 == 0)*1.0) + ((decayMode_2 == 1 || decayMode_2 == 2)*1.0) + ((decayMode_2 == 10)*1.0))"
		else:
			return "(1.0)"
	
	# lumi-weighted average to account for EM cross trigger with DZ filter used only in data for periods G-H
	def em_triggerweight_dz_filter(self, channel, cut_type):
		if channel in ["em", "ttbar"] and "2016" in cut_type:
			return "(0.979)"
		else:
			return "(1.0)"

	def __init__(self,embedding=False,ttbar_retuned=False,embedding_weight="(1.0)"):
		super(Samples, self).__init__()
		self.exclude_cuts = ["blind"]
		self.period = "run2"
		self.embedding = embedding
		self.ttbar_retuned = ttbar_retuned
		self.embedding_weight = embedding_weight

	def get_config(self, samples, channel, category, nick_suffix="", postfit_scales=None, **kwargs):
		config = super(Samples, self).get_config(samples, channel, category, nick_suffix=nick_suffix, postfit_scales=postfit_scales, **kwargs)

		# execute bin correction modules after possible background estimation modules
		if not kwargs.get("mssm", False):
			config.setdefault("analysis_modules", []).sort(key=lambda module: module in ["BinErrorsOfEmptyBins", "CorrectNegativeBinContents"])
		return config

	def projection(self, kwargs):
		data_weight = "(1.0)"
		mc_weight = "(1.0)"
		if kwargs.get("project_to_lumi", False):
			data_weight = "({projection})*".format(projection=kwargs["project_to_lumi"]) + data_weight
			mc_weight = "({projection})*".format(projection=kwargs["project_to_lumi"]) + mc_weight
		if kwargs.get("cut_mc_only", False):
			mc_weight = "({mc_cut})*".format(mc_cut=kwargs["cut_mc_only"]) + mc_weight
		if kwargs.get("scale_mc_only", False):
			mc_weight = "({mc_scale})*".format(mc_scale=kwargs["scale_mc_only"]) + mc_weight
		return clean_multiplication(data_weight), clean_multiplication(mc_weight)

	def get_weights_ztt(self,channel, cut_type, weight="(1.0)", mc_sample_weight="(1.0)", doStitching=True,**kwargs):
		data_weight, mc_weight = self.projection(kwargs)
		if self.embedding:
			if channel == "et":
				if not 'eventWeight' in mc_sample_weight:
					return make_multiplication([mc_sample_weight, self.embedding_stitchingweight(channel), "(eventWeight)*(eventWeight<1.0)",self.embedding_weight[1]])
				return make_multiplication([mc_sample_weight, self.embedding_stitchingweight(channel), "(eventWeight<1.0)",self.embedding_weight[1]])			
			elif channel == "mt":
				if not 'eventWeight' in mc_sample_weight:
					return make_multiplication([mc_sample_weight, self.embedding_stitchingweight(channel), "(eventWeight)*(eventWeight<1.0)",self.embedding_weight[0]])
				return make_multiplication([mc_sample_weight, self.embedding_stitchingweight(channel), "(eventWeight<1.0)",self.embedding_weight[0]])			
			elif channel == "tt":
				if not 'eventWeight' in mc_sample_weight:
					return make_multiplication([mc_sample_weight, self.embedding_stitchingweight(channel), "(eventWeight)*(eventWeight<1.0)",self.embedding_weight[3]])
				return make_multiplication([mc_sample_weight, self.embedding_stitchingweight(channel), "(eventWeight<1.0)",self.embedding_weight[3]])
			elif channel == "em" or channel == "ttbar":
				if not 'eventWeight' in mc_sample_weight:
					return make_multiplication([mc_sample_weight, self.embedding_stitchingweight(channel), "(eventWeight)*(eventWeight<1.0)",self.embedding_weight[2]])
				return make_multiplication([mc_sample_weight, self.embedding_stitchingweight(channel), "(eventWeight<1.0)",self.embedding_weight[2]])
			else:
				log.error("Embedding currently not implemented for channel \"%s\"!" % channel)
		elif mc_sample_weight != "(1.0)":
			if doStitching:
				return make_multiplication([self.ztt_stitchingweight(), mc_sample_weight])
			else:
				return mc_sample_weight
		else:
			if doStitching:
				if channel == "gen":
					return  mc_weight  # TODO this needs to be studied further!
				else:
					return make_multiplication([mc_weight, weight, "eventWeight", self.ztt_stitchingweight()])
			else:
				if channel == "gen":
					return  mc_weight  # TODO this needs to be studied further!
				else:
					return make_multiplication([mc_weight, weight, "eventWeight"])

	def files_data(self, channel):
		query_rereco = {}
		query_promptreco = {}
		query_reminiaod = {}
		expect_n_results_rereco = 6 # adjust in if-statements if different depending on channel
		expect_n_results_promptreco = 2
		expect_n_results_reminiaod = 8
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
		query_rereco["campaign"] = "Run2016(B|C|D|E|F|G)"
		query_rereco["scenario"] = "23Sep2016v(1|3)"
		query_promptreco["data"] = True
		query_promptreco["campaign"] = "Run2016H"
		query_promptreco["scenario"] = "PromptRecov(2|3)"
		query_reminiaod["data"] = True
		query_reminiaod["campaign"] = "Run2016(B|C|D|E|F|G|H)"
		query_reminiaod["scenario"] = "03Feb2017.*"

		rereco_files = self.artus_file_names(query_rereco, expect_n_results_rereco)
		promptreco_files = self.artus_file_names(query_promptreco, expect_n_results_promptreco)
		reminiaod_files = self.artus_file_names(query_reminiaod, expect_n_results_reminiaod)
		#~ return rereco_files + " " + promptreco_files
		return reminiaod_files

	def data(self, config, channel, category, weight, nick_suffix, exclude_cuts=None, cut_type="baseline", **kwargs):

		asimov_nicks = kwargs.get("asimov_nicks", [])
		if len(asimov_nicks) == 0:
			if exclude_cuts is None:
				exclude_cuts = []

			scale_factor = 1.0
			if not self.postfit_scales is None:
				scale_factor *= self.postfit_scales.get("data_obs", 1.0)
			data_weight = "(1.0)"
			if kwargs.get("project_to_lumi", False):
				data_weight = "({projection})*".format(projection=kwargs["project_to_lumi"]) + data_weight
			
			add_input = partialmethod(Samples._add_input, config=config, folder=self.root_file_folder(channel), nick_suffix=nick_suffix)
			add_input(
					input_file=self.files_data(channel),
					scale_factor=1.0,
					weight=make_multiplication([data_weight, weight, "eventWeight", self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)]),
					nick="data"					
			)
		else:
			if not "AddHistograms" in config.get("analysis_modules", []):
				config.setdefault("analysis_modules", []).append("AddHistograms")
			config.setdefault("add_nicks", []).append(" ".join(asimov_nicks))
			config.setdefault("add_result_nicks", []).append("data"+nick_suffix)
			config.setdefault("nicks_whitelist", []).extend(["^((?!(data|noplot)).)*$", "data"])

		if not kwargs.get("no_plot", False):
			Samples._add_plot(config, "data", "E", "ELP", "data" if len(asimov_nicks) == 0 else "asimov", nick_suffix)

		return config

	def files_dy_m50(self, channel):
		return self.artus_file_names({"process" : "DYJetsToLLM50", "data": False, "campaign" : self.mc_campaign, "generator" : "madgraph\-pythia8"}, 2)

	def files_ztt(self, channel):
		if self.embedding:
			if channel=='mt':
				return self.artus_file_names({"process" : "Embedding2016.*" , "campaign" : "MuTauFinalState","scenario": ".*v2" }, 7)
			elif channel=='et':
				return self.artus_file_names({"process" : "Embedding2016.*" , "campaign" : "ElTauFinalState","scenario": ".*v2" }, 7)
			elif channel=='tt':
				return self.artus_file_names({"process" : "Embedding2016.*" , "campaign" : "TauTauFinalState","scenario": "imputSep16DoubleMu_mirror_miniAODv2" }, 6)				
			elif channel=='em':
				return self.artus_file_names({"process" : "Embedding2016.*" , "campaign" : "ElMuFinalState","scenario": "imputSep16DoubleMu_mirror_miniAODv2" }, 6)
			else:
				log.error("Embedding currently not implemented for channel \"%s\"!" % channel)
								
		return self.artus_file_names({"process" : "(DYJetsToLLM10to50|DYJetsToLLM50|DY1JetsToLLM50|DY2JetsToLLM50|DY3JetsToLLM50|DY4JetsToLLM50)", "data": False, "campaign" : self.mc_campaign, "generator" : "madgraph\-pythia8"}, 7)

	def ztt(self, config, channel, category, weight, nick_suffix, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []
		
		zmm_cr_factor = kwargs.get("zmm_cr_factor", "(1.0)")

		scale_factor = 1.0
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("ZTT", 1.0)
			
		add_input = partialmethod(Samples._add_input, config=config, folder=self.root_file_folder(channel), scale_factor=lumi, nick_suffix=nick_suffix)		
		if channel in ['gen']:
			add_input(
					input_file=self.files_ztt(channel),
					weight=Samples.ztt_genchannelmatch(channel, category)+"*"+self.get_weights_ztt(channel=channel,cut_type=cut_type,weight=weight)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type),
					nick="ztt"
		)
		elif channel in ["mt", "et", "tt", "em", "mm", "ee", "ttbar"]:
			add_input(
					input_file=self.files_ztt(channel),
					weight=Samples.ztt_genmatch(channel)+"*"+self.get_weights_ztt(channel=channel,cut_type=cut_type,weight=weight)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*zPtReweightWeight"+"*"+self.decay_mode_reweight(channel)+"*"+zmm_cr_factor+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
					nick="ztt"
			)
			if not (kwargs.get("no_ewk_samples", False) or kwargs.get("no_ewkz_as_dy", False)):
				add_input(
						input_file=self.files_ewkz_zll(channel),
						weight=Samples.ztt_genmatch(channel)+"*"+self.get_weights_ztt(channel=channel,cut_type=cut_type,weight=weight,doStitching=False)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+self.decay_mode_reweight(channel)+"*"+self.ewkz_zll_stitchingweight()+"*"+zmm_cr_factor+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
						nick="ztt"
				)
				add_input(
						input_file=self.files_ewkz_znn(channel),
						weight=Samples.ztt_genmatch(channel)+"*"+self.get_weights_ztt(channel=channel,cut_type=cut_type,weight=weight,doStitching=False)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+self.decay_mode_reweight(channel)+"*"+self.ewkz_znn_stitchingweight()+"*"+zmm_cr_factor+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
						nick="ztt"
				)
		else:
			log.error("Sample config (ZTT) currently not implemented for channel \"%s\"!" % channel)
		if not kwargs.get("mssm", False):
			Samples._add_bin_corrections(config, "ztt", nick_suffix)
		
		if not kwargs.get("no_plot", False):
			Samples._add_plot(config, "bkg", "HIST", "F", kwargs.get("color_label_key", "ztt"), nick_suffix)

		return config

	def zttpospol(self, config, channel, category, weight, nick_suffix, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", **kwargs):
		polarisation_bias_correction = kwargs.get("polarisation_bias_correction", False)
		polarisation_gen_ztt_plots = kwargs.get("polarisation_gen_ztt_plots", False)
		
		name = "pospol"+("_noplot" if polarisation_bias_correction else "")
		polarisation_weight = "tauSpinnerPolarisation>=0.0"
		config = self.ztt(config, channel, category, "(%s)*(%s)" % (polarisation_weight, weight), name+nick_suffix, lumi=lumi, exclude_cuts=exclude_cuts, cut_type=cut_type, color_label_key="zttpospol", label="zttpospol", **kwargs)
		add_input = partialmethod(Samples._add_input, config=config, scale_factor=1.0, nick_suffix=nick_suffix)	
		if polarisation_bias_correction or polarisation_gen_ztt_plots:
			add_input(
					input_file=self.files_dy_m50(channel),
					folder="gen/ntuple",
					weight="isZTT*(%s)" % polarisation_weight,
					nick="gen_ztt"+name+("" if polarisation_gen_ztt_plots else "_noplot")
			)
		
		if polarisation_bias_correction:
			if not "NormalizeForPolarisation" in config.get("analysis_modules", []):
				config.setdefault("analysis_modules", []).append("NormalizeForPolarisation")
			config.setdefault("ztt_pos_pol_gen_nicks", []).extend(["gen_ztt"+name+("" if polarisation_gen_ztt_plots else "_noplot")+nick_suffix] * 2),
			config.setdefault("ztt_pos_pol_reco_nicks", []).extend(["ztt"+name+nick_suffix, "gen_ztt"+name+("" if polarisation_gen_ztt_plots else "_noplot")+nick_suffix])
			config.setdefault("ztt_pos_pol_reco_result_nicks", []).extend(["zttpospol"+nick_suffix, "gen_zttpospol"+("" if polarisation_gen_ztt_plots else "_noplot")+nick_suffix])
		
		if polarisation_gen_ztt_plots:
			Samples._add_plot(config, "gen", "HIST", "F", "zttpospol", nick_suffix)
		
		return config
	
	def zttnegpol(self, config, channel, category, weight, nick_suffix, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", **kwargs):
		polarisation_bias_correction = kwargs.get("polarisation_bias_correction", False)
		polarisation_gen_ztt_plots = kwargs.get("polarisation_gen_ztt_plots", False)
		
		name = "negpol"+("_noplot" if polarisation_bias_correction else "")
		polarisation_weight = "tauSpinnerPolarisation<0.0"
		config = self.ztt(config, channel, category, "(%s)*(%s)" % (polarisation_weight, weight), name+nick_suffix, lumi=lumi, exclude_cuts=exclude_cuts, cut_type=cut_type, color_label_key="zttnegpol", label="zttnegpol", **kwargs)
		add_input = partialmethod(Samples._add_input, config=config, scale_factor=1.0, nick_suffix=nick_suffix)	

		if polarisation_bias_correction or polarisation_gen_ztt_plots:
			add_input(
					input_file=self.files_dy_m50(channel),
					folder="gen/ntuple",
					weight="isZTT*(%s)" % polarisation_weight,
					nick="gen_ztt"+name+("" if polarisation_gen_ztt_plots else "_noplot")
			)
		
		if polarisation_bias_correction:
			if not "NormalizeForPolarisation" in config.get("analysis_modules", []):
				config.setdefault("analysis_modules", []).append("NormalizeForPolarisation")
			config.setdefault("ztt_neg_pol_gen_nicks", []).extend(["gen_ztt"+name+("" if polarisation_gen_ztt_plots else "_noplot")+nick_suffix] * 2),
			config.setdefault("ztt_neg_pol_reco_nicks", []).extend(["ztt"+name+nick_suffix, "gen_ztt"+name+("" if polarisation_gen_ztt_plots else "_noplot")+nick_suffix])
			config.setdefault("ztt_neg_pol_reco_result_nicks", []).extend(["zttnegpol"+nick_suffix, "gen_zttnegpol"+("" if polarisation_gen_ztt_plots else "_noplot")+nick_suffix])
		
		if polarisation_gen_ztt_plots:
			Samples._add_plot(config, "gen", "HIST", "F", "zttnegpol", nick_suffix)
		
		return config

	def zttposcp(self, config, channel, category, weight, nick_suffix, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", **kwargs):
		cp_weight = "( ((q_2>0)*(cosPsiPlus<(sqrt(2)/2))) + ((q_2<0)*(cosPsiMinus<(sqrt(2)/2))) )"
		config = self.ztt(config, channel, category, "(%s)*(%s)" % (cp_weight, weight), "poscp"+nick_suffix, lumi=lumi, exclude_cuts=exclude_cuts, cut_type=cut_type, color_label_key="zttposcp", label="zttposcp", **kwargs)
		return config

	def zttnegcp(self, config, channel, category, weight, nick_suffix, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", **kwargs):
		cp_weight = "( ((q_2>0)*(cosPsiPlus>(sqrt(2)/2))) + ((q_2<0)*(cosPsiMinus>(sqrt(2)/2))) )"
		config = self.ztt(config, channel, category, "(%s)*(%s)" % (cp_weight, weight), "negcp"+nick_suffix, lumi=lumi, exclude_cuts=exclude_cuts, cut_type=cut_type, color_label_key="zttnegcp", label="zttnegcp", **kwargs)
		return config

	def files_zll(self, channel):
		return self.artus_file_names({"process" : "(DYJetsToLLM10to50|DYJetsToLLM50|DY1JetsToLLM50|DY2JetsToLLM50|DY3JetsToLLM50|DY4JetsToLLM50)", "data": False, "campaign" : self.mc_campaign, "generator" : "madgraph\-pythia8"}, 7)

	def zll(self, config, channel, category, weight, nick_suffix, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", fakefactor_method=None, **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []
		
		zmm_cr_factor = kwargs.get("zmm_cr_factor", "(1.0)")

		scale_factor = lumi
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("ZLL", 1.0)

		data_weight, mc_weight = self.projection(kwargs)
		add_input = partialmethod(Samples._add_input, config=config, folder=self.root_file_folder(channel), scale_factor=lumi, nick_suffix=nick_suffix)	
		if channel in ["mt", "et", "tt", "em", "mm", "ee", "ttbar"]:
			add_input(
					input_file=self.files_zll(channel),
					weight=mc_weight+"*"+weight+"*eventWeight*"+self.zll_stitchingweight()+"*"+Samples.zll_genmatch(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*zPtReweightWeight"+"*"+self.zll_zl_shape_weight(channel, cut_type)+"*"+zmm_cr_factor+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
					nick="zll"
			)
			if not (kwargs.get("no_ewk_samples", False) or kwargs.get("no_ewkz_as_dy", False)):
				add_input(
						input_file=self.files_ewkz_zll(channel),
						weight=mc_weight+"*"+weight+"*eventWeight*"+Samples.zll_genmatch(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+self.zll_zl_shape_weight(channel, cut_type)+"*"+self.ewkz_zll_stitchingweight()+"*"+zmm_cr_factor+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
						nick="zll"
				)
				add_input(
						input_file=self.files_ewkz_znn(channel),
						weight=mc_weight+"*"+weight+"*eventWeight*"+Samples.zll_genmatch(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+self.zll_zl_shape_weight(channel, cut_type)+"*"+self.ewkz_znn_stitchingweight()+"*"+zmm_cr_factor+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
						nick="zll"
				)
		else:
			log.error("Sample config (ZLL) currently not implemented for channel \"%s\"!" % channel)
		if not kwargs.get("mssm", False):
			Samples._add_bin_corrections(config, "zll", nick_suffix)
		
		if not kwargs.get("no_plot", False):
			Samples._add_plot(config, "bkg", "HIST", "F", kwargs.get("color_label_key", "zll"), nick_suffix)
		
		return config

	def zl(self, config, channel, category, weight, nick_suffix, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []
		
		zmm_cr_factor = kwargs.get("zmm_cr_factor", "(1.0)")

		scale_factor = lumi
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("ZL", 1.0)

		data_weight, mc_weight = self.projection(kwargs)
		
		add_input = partialmethod(Samples._add_input, config=config, folder=self.root_file_folder(channel), scale_factor=lumi, nick_suffix=nick_suffix)	
		if channel in ["mt", "et", "tt"]:
			add_input(
					input_file=self.files_zll(channel),
					weight=mc_weight+"*"+weight+"*eventWeight*"+self.zll_stitchingweight()+"*"+Samples.zl_genmatch(channel)+"*"+Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind"], cut_type=cut_type)+"*zPtReweightWeight"+"*"+self.zl_shape_weight(channel, cut_type)+"*"+zmm_cr_factor+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
					nick="zl",
			)
			if not (kwargs.get("no_ewk_samples", False) or kwargs.get("no_ewkz_as_dy", False)):
				add_input(
						input_file=self.files_ewkz_zll(channel),
						weight=mc_weight+"*"+weight+"*eventWeight*"+Samples.zl_genmatch(channel)+"*"+Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind"], cut_type=cut_type)+"*"+self.zl_shape_weight(channel, cut_type)+"*"+self.ewkz_zll_stitchingweight()+"*"+zmm_cr_factor+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
						nick="zl"
				)
				add_input(
						input_file=self.files_ewkz_znn(channel),
						weight=mc_weight+"*"+weight+"*eventWeight*"+Samples.zl_genmatch(channel)+"*"+Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind"], cut_type=cut_type)+"*"+self.zl_shape_weight(channel, cut_type)+"*"+self.ewkz_znn_stitchingweight()+"*"+zmm_cr_factor+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
						nick="zl",
				)
		elif channel in ["em", "ttbar"]:
			pass
		else:
			log.error("Sample config (ZL) currently not implemented for channel \"%s\"!" % channel)
		if not kwargs.get("mssm", False):
			Samples._add_bin_corrections(config, "zl", nick_suffix)
	
		if not kwargs.get("no_plot", False):
			Samples._add_plot(config, "bkg", "HIST", "F", kwargs.get("color_label_key", "zl"), nick_suffix)
		return config

	def zj(self, config, channel, category, weight, nick_suffix, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []
		
		zmm_cr_factor = kwargs.get("zmm_cr_factor", "(1.0)")

		scale_factor = lumi
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("ZJ", 1.0)

		data_weight, mc_weight = self.projection(kwargs)
		add_input = partialmethod(Samples._add_input, config=config, folder=self.root_file_folder(channel), scale_factor=lumi, nick_suffix=nick_suffix)	
		if channel in ["mt", "et", "tt"]:
			add_input(
					input_file=self.files_zll(channel),
					weight=mc_weight+"*"+weight+"*eventWeight*"+self.zll_stitchingweight()+"*"+Samples.zj_genmatch(channel)+"*"+Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind"], cut_type=cut_type)+"*zPtReweightWeight"+"*"+zmm_cr_factor+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
					nick="zj"
			)
			if not (kwargs.get("no_ewk_samples", False) or kwargs.get("no_ewkz_as_dy", False)):
				add_input(
						input_file=self.files_ewkz_zll(channel),
						weight=mc_weight+"*"+weight+"*eventWeight*"+Samples.zj_genmatch(channel)+"*"+Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind"], cut_type=cut_type)+"*"+self.ewkz_zll_stitchingweight()+"*"+zmm_cr_factor+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
						nick="zj"
				)
				add_input(
						input_file=self.files_ewkz_znn(channel),
						weight=mc_weight+"*"+weight+"*eventWeight*"+Samples.zj_genmatch(channel)+"*"+Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind"], cut_type=cut_type)+"*"+self.ewkz_znn_stitchingweight()+"*"+zmm_cr_factor+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
						nick="zj"
				)
		elif channel in ["em", "ttbar"]:
			pass
		else:
			log.error("Sample config (ZJ) currently not implemented for channel \"%s\"!" % channel)
		if not kwargs.get("mssm", False):
			Samples._add_bin_corrections(config, "zj", nick_suffix)

		if not kwargs.get("no_plot", False):
			Samples._add_plot(config, "bkg", "HIST", "F", kwargs.get("color_label_key", "zj"), nick_suffix)

		return config
		
	def files_ttj(self, channel):
		if self.ttbar_retuned:
			return self.artus_file_names({"process" : "TTTo.*", "data": False, "campaign" : self.mc_campaign}, 2)
		else:
			return self.artus_file_names({"process" : "TT_", "data": False, "campaign" : self.mc_campaign}, 1)

	def ttt(self, config, channel, category, weight, nick_suffix, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", fakefactor_method=None, **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []

		scale_factor = lumi
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("TTJ", 1.0)

		data_weight, mc_weight = self.projection(kwargs)
		add_input = partialmethod(Samples._add_input, config=config, folder=self.root_file_folder(channel), scale_factor=lumi, nick_suffix=nick_suffix)	
		add_input(
				input_file=self.files_ttj(channel),
				weight=mc_weight+"*"+weight+"*eventWeight*"+self.embedding_ttbarveto_weight(channel)+"*"+Samples.ttt_genmatch(channel,kwargs)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*topPtReweightWeight"+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
				nick="ttt"
		)
		if channel not in ["et", "mt", "tt"]:
			log.error("Sample config (TTT) currently not implemented for channel \"%s\"!" % channel)
		if not kwargs.get("mssm", False):
			Samples._add_bin_corrections(config, "ttt", nick_suffix)
		
		if not kwargs.get("no_plot", False):
			Samples._add_plot(config, "bkg", "HIST", "F", kwargs.get("color_label_key", "ttt"), nick_suffix)

		return config

	def files_lfv(self, channel):
		return self.artus_file_names({"process" : "LFV*", "data": False, "croote" : self.mc_campaign}, 10)




	def zmt(self, config, channel, category, weight, nick_suffix, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", fakefactor_method=None, **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []

		scale_factor = lumi

		branching_ratio = "1.2e-5" #"(0.03363)*0.66*0.17*2" 				
		jet_integral_weight = "1/1.05"							
		files_weight = "1/10.0"
		cross_section_weight = "3.0" # "(0.03363+0.03366+0.0337)/(0.0337)"
	
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("TTJ", 1.0)

		data_weight, mc_weight = self.projection(kwargs)
		add_input = partialmethod(Samples._add_input, config=config, folder=self.root_file_folder(channel), scale_factor=lumi, nick_suffix=nick_suffix)	
		add_input(
				input_file=self.files_lfv(channel),
				weight=mc_weight+"*"+weight+"*eventWeight*"+Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind"], cut_type=cut_type)+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type)+"*"+"(lheZtoMT > 0.5)"+"*"+branching_ratio+"*"+files_weight+"*"+jet_integral_weight+"*"+cross_section_weight+"*jetCorrectionWeight",			
				nick="zmt"														
		)

		Samples._add_bin_corrections(config, "zmt", nick_suffix)			
		
		if not kwargs.get("no_plot", False):
			Samples._add_plot(config, "sig", "LINE", "F", kwargs.get("color_label_key", "zmt"), nick_suffix)				
		
		return config

	def zet(self, config, channel, category, weight, nick_suffix, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", fakefactor_method=None, **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []

		scale_factor = lumi

		branching_ratio = "9.8e-6" #"(0.03363)*0.66*0.17*2"
		jet_integral_weight = "1/1.06"
		files_weight = "1/10.0"
		cross_section_weight = "3.0" # "(0.03363+0.03366+0.0337)/(0.0337)"
	
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("TTJ", 1.0)

		data_weight, mc_weight = self.projection(kwargs)
		add_input = partialmethod(Samples._add_input, config=config, folder=self.root_file_folder(channel), scale_factor=lumi, nick_suffix=nick_suffix)	
		add_input(
				input_file=self.files_lfv(channel),
				weight=mc_weight+"*"+weight+"*eventWeight*"+Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind"], cut_type=cut_type)+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type)+"*"+"(lheZtoET > 0.5)"+"*"+branching_ratio+"*"+files_weight+"*"+jet_integral_weight+"*"+cross_section_weight+"*jetCorrectionWeight",
				nick="zet"
		)
				
		Samples._add_bin_corrections(config, "zet", nick_suffix)		

		if not kwargs.get("no_plot", False):
			Samples._add_plot(config, "sig", "LINE", "F", kwargs.get("color_label_key", "zet"), nick_suffix)

		return config

	def zem(self, config, channel, category, weight, nick_suffix, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", fakefactor_method=None, **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []

		scale_factor = lumi

		branching_ratio = "7.3e-7" #"1.2e-5" #"9.8e-6"  # "(0.03363+0.03366+0.0337)*0.1741*0.1783*2"			
		jet_integral_weight = "1/1.03"											
		files_weight = "1/10.0"
		cross_section_weight = "3.0" #"(0.03363+0.03366+0.0337)/(0.0337)"

		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("TTJ", 1.0)

		data_weight, mc_weight = self.projection(kwargs)
		add_input = partialmethod(Samples._add_input, config=config, folder=self.root_file_folder(channel), scale_factor=lumi, nick_suffix=nick_suffix)	
		add_input(
				input_file=self.files_lfv(channel),
				weight=mc_weight+"*"+weight+"*eventWeight*"+Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind"], cut_type=cut_type)+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type)+"*"+"(lheZtoEM > 0.5)"+"*"+ branching_ratio+"*"+files_weight+"*"+jet_integral_weight+"*"+cross_section_weight+"*jetCorrectionWeight",			
				nick="zem"											
		)

		Samples._add_bin_corrections(config, "zem", nick_suffix)							

		if not kwargs.get("no_plot", False):
			Samples._add_plot(config, "sig", "LINE", "F", kwargs.get("color_label_key", "zem"), nick_suffix)	
		
		return config





	def zetm(self, config, channel, category, weight, nick_suffix, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", fakefactor_method=None, **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []

		scale_factor = lumi
		branching_ratio = "9.8e-6" #"(0.03363)*0.66*0.17*2"
		jet_integral_weight = "1/1.05"
		files_weight = "1/10.0"
		cross_section_weight = "3.0" # "(0.03363+0.03366+0.0337)/(0.0337)"
	
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("TTJ", 1.0)

		data_weight, mc_weight = self.projection(kwargs)
		add_input = partialmethod(Samples._add_input, config=config, folder=self.root_file_folder(channel), scale_factor=lumi, nick_suffix=nick_suffix)	
		add_input(
				input_file=self.files_lfv(channel),
				weight=mc_weight+"*"+weight+"*eventWeight*"+Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind"], cut_type=cut_type)+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type)+"*"+"(lheZtoET > 0.5)"+"*"+branching_ratio+"*"+files_weight+"*"+jet_integral_weight+"*"+cross_section_weight+"*jetCorrectionWeight",
				nick="zetm"
		)

		Samples._add_bin_corrections(config, "zetm", nick_suffix)
		
		if not kwargs.get("no_plot", False):
			Samples._add_plot(config, "sig", "LINE", "F", kwargs.get("color_label_key", "zetm"), nick_suffix)
		
		return config



	def zmte(self, config, channel, category, weight, nick_suffix, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", fakefactor_method=None, **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []

		scale_factor = lumi
		branching_ratio = "1.2e-5" #"(0.03363)*0.66*0.17*2"
		jet_integral_weight = "1/1.05"
		files_weight = "1/10.0"
		cross_section_weight = "3.0" # "(0.03363+0.03366+0.0337)/(0.0337)"
	
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("TTJ", 1.0)

		data_weight, mc_weight = self.projection(kwargs)
		add_input = partialmethod(Samples._add_input, config=config, folder=self.root_file_folder(channel), scale_factor=lumi, nick_suffix=nick_suffix)	
		add_input(
				input_file=self.files_lfv(channel),
				weight=mc_weight+"*"+weight+"*eventWeight*"+Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind"], cut_type=cut_type)+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type)+"*"+"(lheZtoMT > 0.5)"+"*"+branching_ratio+"*"+files_weight+"*"+jet_integral_weight+"*"+cross_section_weight+"*jetCorrectionWeight",
				nick="zmte"
		)

		Samples._add_bin_corrections(config, "zmte", nick_suffix)
		
		if not kwargs.get("no_plot", False):
			Samples._add_plot(config, "sig", "LINE", "F", kwargs.get("color_label_key", "zmte"), nick_suffix)
		
		return config




	def ttjj(self, config, channel, category, weight, nick_suffix, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", fakefactor_method=None, **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []

		scale_factor = lumi
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("TTJ", 1.0)

		data_weight, mc_weight = self.projection(kwargs)
		add_input = partialmethod(Samples._add_input, config=config, folder=self.root_file_folder(channel), scale_factor=lumi, nick_suffix=nick_suffix)	
		add_input(
				input_file=self.files_ttj(channel),
				weight=mc_weight+"*"+weight+"*eventWeight*"+self.embedding_ttbarveto_weight(channel)+"*"+Samples.ttj_genmatch(channel,kwargs)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*topPtReweightWeight"+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
				nick="ttjj"
		)
		if channel not in ["et", "mt", "tt"]:
			log.error("Sample config (TTJ) currently not implemented for channel \"%s\"!" % channel)
		if not kwargs.get("mssm", False):
			Samples._add_bin_corrections(config, "ttjj", nick_suffix)

		if not kwargs.get("no_plot", False):
			Samples._add_plot(config, "bkg", "HIST", "F", kwargs.get("color_label_key", "ttjj"), nick_suffix)
	
		return config

	def tttautau(self, config, channel, category, weight, nick_suffix, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", estimationMethod="classic", fakefactor_method=None, **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []

		scale_factor = lumi
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("TTTAUTAU", 1.0)
		data_weight, mc_weight = self.projection(kwargs)
		
		add_input = partialmethod(Samples._add_input, config=config, folder=self.root_file_folder(channel), scale_factor=lumi, nick_suffix=nick_suffix)	
		add_input(
				input_file=self.files_ttj(channel),
				weight=make_multiplication([mc_weight, weight, "eventWeight",self.tttautau_genmatch(channel), self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type), "topPtReweightWeight"])+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
				nick="tttautau"
		)
		if channel not in ["em", "et", "mt", "tt", "mm", "ee", "ttbar"]:
			log.error("Sample config (TTTAUTAU) currently not implemented for channel \"%s\"!" % channel)
		if not kwargs.get("mssm", False):
			Samples._add_bin_corrections(config, "tttautau", nick_suffix)	
		
		if not kwargs.get("no_plot", False):
			Samples._add_plot(config, "bkg", "HIST", "F", kwargs.get("color_label_key", "tttautau"), nick_suffix)
		return config

	def ttj(self, config, channel, category, weight, nick_suffix, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", estimationMethod="classic", fakefactor_method=None, **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []
		
		zmm_cr_factor = kwargs.get("zmm_cr_factor", "(1.0)")

		scale_factor = lumi
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("TTJ", 1.0)
		data_weight, mc_weight = self.projection(kwargs)
		add_input = partialmethod(Samples._add_input, config=config, folder=self.root_file_folder(channel), scale_factor=lumi, nick_suffix=nick_suffix)	
		add_input(
				input_file=self.files_ttj(channel),
				weight=make_multiplication([mc_weight, weight, "eventWeight",self.embedding_ttbarveto_weight(channel), self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type), "topPtReweightWeight"])+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
				nick="ttj"
		)
		if channel not in ["em", "et", "mt", "tt", "mm", "ee", "ttbar"]:
			log.error("Sample config (TTJ) currently not implemented for channel \"%s\"!" % channel)
		if not kwargs.get("mssm", False):
			Samples._add_bin_corrections(config, "ttj", nick_suffix)
		
		if not kwargs.get("no_plot", False):
			Samples._add_plot(config, "bkg", "HIST", "F", kwargs.get("color_label_key", "ttj"), nick_suffix)

		return config

	def files_diboson(self, channel):
		artus_files = self.artus_file_names({ "process" : 
		                                      "(WWTo1L1Nu2Q|"
		                                    + "WZTo1L1Nu2Q|"
		                                    + "WZTo1L3Nu|"
		                                    + "WZTo2L2Q|" 
		                                    + "ZZTo2L2Q"
		                                    +  ")",
		                      "data" : False, "campaign" : self.mc_campaign, "generator" : "amcatnlo-pythia8"}, 5)

		artus_files = artus_files + " " + self.artus_file_names({ "process" : "ZZTo4L", "extension" : "ext1",
		                      "data" : False, "campaign" : self.mc_campaign, "generator" : "amcatnlo-pythia8"}, 1)

		artus_files = artus_files + " " + self.artus_file_names({ "process" : "WZJToLLLNu",
		                      "data" : False, "campaign" : self.mc_campaign, "generator" : "pythia8"}, 1)

		artus_files = artus_files + " " + self.artus_file_names({ "process" : "(STt-channelantitop4finclusiveDecays|STt-channeltop4finclusiveDecays|STtWantitop5finclusiveDecays|STtWtop5finclusiveDecays)",
		                      "data" : False, "campaign" : self.mc_campaign}, 4)
		return artus_files
	
	def files_vv(self, channel):
		artus_files = self.artus_file_names({ "process" : "VVTo2L2Nu", "data" : False, "campaign" : self.mc_campaign, "generator" : "amcatnlo-pythia8"}, 2)
		return artus_files

	def files_hww_gg(self, channel, mass=125):
		return self.artus_file_names({"process" : "GluGluHToWWTo2L2Nu_M"+str(mass), "data": False, "campaign" : self.mc_campaign, "generator" : "powheg-pythia8"}, 1)
	
	def hww_gg(self, config, channel, category, weight, nick_suffix, higgs_masses, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []
		
		data_weight, mc_weight = self.projection(kwargs)
		add_input = partialmethod(Samples._add_input, config=config, folder=self.root_file_folder(channel), scale_factor=lumi, nick_suffix=nick_suffix)	
		
		for mass in higgs_masses:
			if channel in ["mt", "et", "em", "tt", "mm", "ee", "ttbar"]:
				add_input(
					input_file=self.files_hww_gg(channel, mass),
					weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
					nick="hww_gg"+str(mass)
				)
			else:
				log.error("Sample config (HWW_gg) currently not implemented for channel \"%s\"!" % channel)
			if not kwargs.get("mssm", False):
				Samples._add_bin_corrections(config, "hww_gg"+str(mass), nick_suffix)
		
			if not kwargs.get("no_plot", False):
				Samples._add_plot(config, "bkg", "HIST", "F", "hww_gg"+str(mass), nick_suffix)
		
		return config

	def hww_gg125(self, config, channel, category, weight, nick_suffix, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []
		
		data_weight, mc_weight = self.projection(kwargs)
		add_input = partialmethod(Samples._add_input, config=config, folder=self.root_file_folder(channel), scale_factor=lumi, nick_suffix=nick_suffix)	
		if channel in ["mt", "et", "em", "tt", "mm", "ee", "ttbar"]:
			add_input(
				input_file=self.files_hww_gg(channel, 125),
				weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
				nick="hww_gg125"
			)
		else:
			log.error("Sample config (HWW_gg125) currently not implemented for channel \"%s\"!" % channel)
		if not kwargs.get("mssm", False):
			Samples._add_bin_corrections(config, "hww_gg125", nick_suffix)
		
		if not kwargs.get("no_plot", False):
			Samples._add_plot(config, "bkg", "HIST", "F", "hww_gg125", nick_suffix)
		
		return config

	def files_hww_qq(self, channel, mass=125):
		return self.artus_file_names({"process" : "VBFHToWWTo2L2Nu_M"+str(mass), "data": False, "campaign" : self.mc_campaign, "generator" : "powheg-pythia8"}, 1)

	def hww_qq(self, config, channel, category, weight, nick_suffix, higgs_masses, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []
		
		data_weight, mc_weight = self.projection(kwargs)
		add_input = partialmethod(Samples._add_input, config=config, folder=self.root_file_folder(channel), scale_factor=lumi, nick_suffix=nick_suffix)	
		for mass in higgs_masses:
			if channel in ["mt", "et", "em", "tt", "mm", "ee", "ttbar"]:
				add_input(
					input_file=self.files_hww_qq(channel, mass),
					weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
					nick="hww_qq"+str(mass)
				)
			else:
				log.error("Sample config (HWW_qq) currently not implemented for channel \"%s\"!" % channel)
			if not kwargs.get("mssm", False):
				Samples._add_bin_corrections(config, "hww_qq"+str(mass), nick_suffix)
			
			if not kwargs.get("no_plot", False):
				Samples._add_plot(config, "bkg", "HIST", "F", "hww_qq"+str(mass), nick_suffix)
		
		return config

	def hww_qq125(self, config, channel, category, weight, nick_suffix, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []
		
		data_weight, mc_weight = self.projection(kwargs)
		add_input = partialmethod(Samples._add_input, config=config, folder=self.root_file_folder(channel), scale_factor=lumi, nick_suffix=nick_suffix)			
		if channel in ["mt", "et", "em", "tt", "mm", "ee", "ttbar"]:
			add_input(
				input_file=self.files_hww_qq(channel, 125),
				weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
				nick="hww_qq125"
			)
		else:
			log.error("Sample config (HWW_qq125) currently not implemented for channel \"%s\"!" % channel)
		if not kwargs.get("mssm", False):
			Samples._add_bin_corrections(config, "hww_qq125", nick_suffix)
		if not kwargs.get("no_plot", False):
			Samples._add_plot(config, "bkg", "HIST", "F", "hww_qq125", nick_suffix)
		
		return config

	def hww(self, config, channel, category, weight, nick_suffix, higgs_masses, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []

		data_weight, mc_weight = self.projection(kwargs)
		add_input = partialmethod(Samples._add_input, config=config, folder=self.root_file_folder(channel), scale_factor=lumi, nick_suffix=nick_suffix)	
		for mass in higgs_masses:
			if channel == "em" or channel == "ttbar":
				add_input(
					input_file=self.files_hww_gg(channel, mass),
					weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
					nick="hww"+str(mass)
				)
				add_input(
					input_file=self.files_hww_qq(channel, mass),
					weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
					nick="hww"+str(mass)
				)
			else:
				log.error("Sample config (HWW) currently not implemented for channel \"%s\"!" % channel)
			if not kwargs.get("mssm", False):
				Samples._add_bin_corrections(config, "hww"+str(mass), nick_suffix)
			if not kwargs.get("no_plot", False):
				Samples._add_plot(config, "bkg", "HIST", "F", "hww"+str(mass), nick_suffix)
		return config

	def vvt(self, config, channel, category, weight, nick_suffix, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", fakefactor_method=None, **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []

		scale_factor = lumi
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("Dibosons", 1.0)

		data_weight, mc_weight = self.projection(kwargs)
		add_input = partialmethod(Samples._add_input, config=config, folder=self.root_file_folder(channel), scale_factor=lumi, nick_suffix=nick_suffix)	
		if channel in ["mt", "et", "tt"]:
			add_input(
					input_file=self.files_vv(channel),
					weight=mc_weight+"*"+weight+"*eventWeight*"+Samples.ttt_genmatch(channel,kwargs)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+self.vv_stitchingweight()+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
					nick="vvt"
			)
			add_input(
					input_file=self.files_diboson(channel),
					weight=mc_weight+"*"+weight+"*eventWeight*"+Samples.ttt_genmatch(channel,kwargs)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
					nick="vvt"
			)
		else:
			log.error("Sample config (VVT) currently not implemented for channel \"%s\"!" % channel)
		if not kwargs.get("mssm", False):
			Samples._add_bin_corrections(config, "vvt", nick_suffix)

		if not kwargs.get("no_plot", False):
			Samples._add_plot(config, "bkg", "HIST", "F", kwargs.get("color_label_key", "vvt"), nick_suffix)
		return config

	def vvj(self, config, channel, category, weight, nick_suffix, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", fakefactor_method=None, **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []

		scale_factor = lumi
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("Dibosons", 1.0)

		data_weight, mc_weight = self.projection(kwargs)
		add_input = partialmethod(Samples._add_input, config=config, folder=self.root_file_folder(channel), scale_factor=lumi, nick_suffix=nick_suffix)	
		if channel in ["mt", "et", "tt"]:
			add_input(
					input_file=self.files_vv(channel),
					weight=mc_weight+"*"+weight+"*eventWeight*"+Samples.ttj_genmatch(channel,kwargs)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+self.vv_stitchingweight()+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
					nick="vvj"
			)
			add_input(
					input_file=self.files_diboson(channel),
					weight=mc_weight+"*"+weight+"*eventWeight*"+Samples.ttj_genmatch(channel,kwargs)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
					nick="vvj"
			)
		else:
			log.error("Sample config (VVJ) currently not implemented for channel \"%s\"!" % channel)

		if not kwargs.get("no_plot", False):
			Samples._add_plot(config, "bkg", "HIST", "F", kwargs.get("color_label_key", "vvj"), nick_suffix)

		if not kwargs.get("mssm", False):
			Samples._add_bin_corrections(config, "vvj", nick_suffix)
		return config

	def vv(self, config, channel, category, weight, nick_suffix, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", fakefactor_method=None, **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []

		scale_factor = lumi
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("Dibosons", 1.0)

		data_weight, mc_weight = self.projection(kwargs)
		add_input = partialmethod(Samples._add_input, config=config, folder=self.root_file_folder(channel), scale_factor=lumi, nick_suffix=nick_suffix)	
		if channel in ["mt", "et", "em", "tt", "mm", "ee", "ttbar"]:
			add_input(
					input_file=self.files_vv(channel),
					weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+self.vv_stitchingweight()+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
					nick="vv"
			)
			add_input(
					input_file=self.files_diboson(channel),
					weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
					nick="vv"
			)
		else:
			log.error("Sample config (VV) currently not implemented for channel \"%s\"!" % channel)
		if not kwargs.get("mssm", False):
			Samples._add_bin_corrections(config, "vv", nick_suffix)
		

		if not kwargs.get("no_plot", False):
			Samples._add_plot(config, "bkg", "HIST", "F", kwargs.get("color_label_key", "vv"), nick_suffix)
		
		return config

	def files_wj(self, channel):
		artus_files = self.artus_file_names({"process" : "W.*JetsToLNu", "data" : False, "campaign" : self.mc_campaign, "generator" : "madgraph-pythia8"}, 10)
		return artus_files
	
	def files_wgamma(self, channel):
		artus_files = self.artus_file_names({"process" : "WGToLNuG", "data" : False, "campaign" : self.mc_campaign, "generator" : "amcatnlo-pythia8"}, 3)
		return artus_files
	
	def files_wgamma_star(self, channel):
		artus_files = self.artus_file_names({"process" : "WGstarToLNuEE|WGstarToLNuMuMu", "data" : False, "campaign" : self.mc_campaign, "generator" : "madgraph"}, 2)
		return artus_files

	def files_ewkwm(self, channel):
		ewkw_query = { "data" : False,
						"campaign" : self.mc_campaign,
						"generator" : "madgraph-pythia8",
						"process" : "EWKWMinus2Jets_WToLNuM50"}
		artus_files = self.artus_file_names(ewkw_query, 3)
		return artus_files

	def files_ewkwp(self, channel):
		ewkw_query = { "data" : False,
						"campaign" : self.mc_campaign,
						"generator" : "madgraph-pythia8",
						"process" : "EWKWPlus2Jets_WToLNuM50"}
		artus_files = self.artus_file_names(ewkw_query, 3)
		return artus_files

	def files_ewkz_zll(self, channel):
		ewkz_query = { "data" : False,
						"campaign" : self.mc_campaign,
						"generator" : "madgraph-pythia8",
						"process" : "EWKZ2Jets_ZToLL_M50"}
		artus_files = self.artus_file_names(ewkz_query, 3)
		return artus_files

	def files_ewkz_znn(self, channel):
		ewkz_query = { "data" : False,
						"campaign" : self.mc_campaign,
						"generator" : "madgraph-pythia8",
						"process" : "EWKZ2Jets"}
		artus_files = self.artus_file_names(ewkz_query, 3)
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
	
	def wj_mc_ss(self, config, channel, category, weight, nick_suffix, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", fakefactor_method=None, estimationMethod="classic", controlregions=False,**kwargs):
		if exclude_cuts is None:
			exclude_cuts = []

		scale_factor = lumi
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("WJets", 1.0)

		data_weight, mc_weight = self.projection(kwargs)
		add_input = partialmethod(Samples._add_input, config=config, folder=self.root_file_folder(channel), scale_factor=lumi, nick_suffix=nick_suffix)	
		
		cut_type_B = cut_type + "SameSignRegion" 
		exclude_cuts_B = copy.deepcopy(exclude_cuts)+["os"]
		add_input(
				input_file=self.files_wj(channel),
				weight=mc_weight+"*"+weight+"*eventWeight*"+self.wj_stitchingweight()+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_B, cut_type=cut_type_B)+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
				nick="wj_mc_ss"
		)
		if (not kwargs.get("no_ewk_samples", False)):
			add_input(
					input_file=self.files_ewkwm(channel),
					weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_B, cut_type=cut_type_B)+"*"+self.ewkwm_stitchingweight(),
					nick="wj_mc_ss"
			)
			add_input(
					input_file=self.files_ewkwp(channel),
					weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_B, cut_type=cut_type_B)+"*"+self.ewkwp_stitchingweight(),
					nick="wj_mc_ss"
			)		
		if not kwargs.get("no_plot", False):
			if not kwargs.get("mssm", False):
				Samples._add_bin_corrections(config, "wj", nick_suffix)
			Samples._add_plot(config, "bkg", "HIST", "F", "wj", nick_suffix)
		return config

	
	
	def wj(self, config, channel, category, weight, nick_suffix, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", fakefactor_method=None, estimationMethod="classic", controlregions=False,**kwargs):
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
		exclude_cuts_D = [cut for cut in exclude_cuts if cut not in ["mt"]] + ["mt"]
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
						input_file=self.files_ztt(channel),
						weight=Samples.ztt_genmatch(channel)+"*"+self.get_weights_ztt(channel=channel,cut_type=cut_type,weight=weight)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_C, cut_type=cut_type_C)+"*zPtReweightWeight"+"*"+zmm_cr_factor,
						nick=("noplot_" if not controlregions else "") + "ztt_ss_highmt"
				)
				if not (kwargs.get("no_ewk_samples", False) or kwargs.get("no_ewkz_as_dy", False)):
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
				add_input(
						input_file=self.files_vv(channel),
						weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_C, cut_type=cut_type_C)+"*"+self.vv_stitchingweight(),
						nick=("noplot_" if not controlregions else "") + "vv_ss_highmt"
				)
				add_input(
						input_file=self.files_diboson(channel),
						weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_C, cut_type=cut_type_C),
						nick=("noplot_" if not controlregions else "") + "vv_ss_highmt"
				)
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
						input_file=self.files_ztt(channel),
						weight=Samples.ztt_genmatch(channel)+"*"+self.get_weights_ztt(channel=channel,cut_type=cut_type,weight=weight)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_D, cut_type=cut_type_D)+"*zPtReweightWeight"+"*"+zmm_cr_factor,
						nick=("noplot_" if not controlregions else "") + "ztt_os_highmt"
				)
				if not (kwargs.get("no_ewk_samples", False) or kwargs.get("no_ewkz_as_dy", False)):
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
				add_input(
						input_file=self.files_vv(channel),
						weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_D, cut_type=cut_type_D)+"*"+self.vv_stitchingweight(),
						nick=("noplot_" if not controlregions else "") + "vv_os_highmt"
				)
				add_input(
						input_file=self.files_diboson(channel),
						weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_D, cut_type=cut_type_D),
						nick=("noplot_" if not controlregions else "") + "vv_os_highmt"
				)
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
						weight=data_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_D, cut_type=cut_type_D),
						nick="noplot_wj_data_control"
				)
				add_input(
						input_file=self.files_ztt(channel),
						weight=Samples.ztt_genmatch(channel)+"*"+self.get_weights_ztt(channel=channel,cut_type=cut_type,weight=weight)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_D, cut_type=cut_type_D)+"*zPtReweightWeight"+"*"+zmm_cr_factor,
						nick="noplot_ztt_mc_wj_control"
				)
				if not (kwargs.get("no_ewk_samples", False) or kwargs.get("no_ewkz_as_dy", False)):
					add_input(
							input_file=self.files_ewkz_zll(channel),
							weight=Samples.ztt_genmatch(channel)+"*"+self.get_weights_ztt(channel=channel,cut_type=cut_type,weight=weight,doStitching=False)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_D, cut_type=cut_type_D)+"*"+self.ewkz_zll_stitchingweight()+"*"+zmm_cr_factor,
							nick="noplot_ztt_mc_wj_control"
					)
					add_input(
							input_file=self.files_ewkz_znn(channel),
							weight=Samples.ztt_genmatch(channel)+"*"+self.get_weights_ztt(channel=channel,cut_type=cut_type,weight=weight,doStitching=False)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_D, cut_type=cut_type_D)+"*"+self.ewkz_znn_stitchingweight()+"*"+zmm_cr_factor,
							nick="noplot_ztt_mc_wj_control"
					)
				add_input(
						input_file=self.files_zll(channel),
						weight=mc_weight+"*"+weight+"*eventWeight*"+self.zll_stitchingweight()+"*"+Samples.zll_genmatch(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_D, cut_type=cut_type_D)+"*zPtReweightWeight"+"*"+self.zll_zl_shape_weight(channel, cut_type)+"*"+zmm_cr_factor,
						nick="noplot_zll_wj_control"
				)
				if not (kwargs.get("no_ewk_samples", False) or kwargs.get("no_ewkz_as_dy", False)):
					add_input(
							input_file=self.files_ewkz_zll(channel),
							weight=mc_weight+"*"+weight+"*eventWeight*"+Samples.zll_genmatch(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_D, cut_type=cut_type_D)+"*"+self.zll_zl_shape_weight(channel, cut_type)+"*"+self.ewkz_zll_stitchingweight()+"*"+zmm_cr_factor,
							nick="noplot_zll_wj_control"
					)
					add_input(
							input_file=self.files_ewkz_znn(channel),
							weight=mc_weight+"*"+weight+"*eventWeight*"+Samples.zll_genmatch(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_D, cut_type=cut_type_D)+"*"+self.zll_zl_shape_weight(channel, cut_type)+"*"+self.ewkz_znn_stitchingweight()+"*"+zmm_cr_factor,
							nick="noplot_zll_wj_control"
					)
				if (not kwargs.get("no_ewk_samples", False)) and kwargs.get("no_ewkz_as_dy", False):
					add_input(
							input_file=self.files_ewkz_zll(channel),
							weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_D, cut_type=cut_type_D)+"*"+self.ewkz_zll_stitchingweight()+"*"+zmm_cr_factor,
							nick="noplot_ewkz_wj_control"
					)
					add_input(
							input_file=self.files_ewkz_znn(channel),
							weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_D, cut_type=cut_type_D)+"*"+self.ewkz_znn_stitchingweight()+"*"+zmm_cr_factor,
							nick="noplot_ewkz_wj_control"
					)
				add_input(
						input_file=self.files_ttj(channel),
						weight=mc_weight+"*"+weight+"*eventWeight*"+self.embedding_ttbarveto_weight(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_D, cut_type=cut_type_D)+"*topPtReweightWeight",
						nick="noplot_ttj_wj_control"
				)
				add_input(
						input_file=self.files_vv(channel),
						weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_D, cut_type=cut_type_D)+"*"+self.vv_stitchingweight(),
						nick="noplot_vv_wj_control"
				)
				add_input(
						input_file=self.files_diboson(channel),
						weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_D, cut_type=cut_type_D),
						nick="noplot_vv_wj_control"
				)
				add_input(
						input_file=self.files_wj(channel),
						weight=mc_weight+"*"+weight+"*eventWeight*"+self.wj_stitchingweight()+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type),
						nick="noplot_wj_mc_signal"
				)
				add_input(
						input_file=self.files_wj(channel),
						weight=mc_weight+"*"+weight+"*eventWeight*"+self.wj_stitchingweight()+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_D, cut_type=cut_type_D),
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
					input_file=self.files_ztt(channel),
					weight=Samples.ztt_genmatch(channel)+"*"+self.get_weights_ztt(channel=channel,cut_type=cut_type,weight=weight)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_B, cut_type=cut_type_B)+"*zPtReweightWeight"+"*"+zmm_cr_factor+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
					nick="noplot_ztt_mc_qcd_control"
			)
			if not (kwargs.get("no_ewk_samples", False) or kwargs.get("no_ewkz_as_dy", False)):
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
			add_input(
					input_file=self.files_vv(channel),
					weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_B, cut_type=cut_type_B)+"*"+self.vv_stitchingweight()+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
					nick="noplot_vv_qcd_control"
			)
		 	add_input(
					input_file=self.files_diboson(channel),
					weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_B, cut_type=cut_type_B)+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
					nick="noplot_vv_qcd_control"
			)

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
		exclude_cuts_D = copy.deepcopy(exclude_cuts)+["mt"]
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
						input_file=self.files_ztt(channel),
						weight=Samples.ztt_genmatch(channel)+"*"+self.get_weights_ztt(channel=channel,cut_type=cut_type,weight=weight)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_B, cut_type=cut_type_B)+"*zPtReweightWeight"+"*"+zmm_cr_factor+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
						nick=("noplot_" if not controlregions else "") + "ztt_ss_qcd"
				)
				if not (kwargs.get("no_ewk_samples", False) or kwargs.get("no_ewkz_as_dy", False)):
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
				add_input(
						input_file=self.files_vv(channel),
						weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_B, cut_type=cut_type_B)+"*"+self.vv_stitchingweight()+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
						nick=("noplot_" if not controlregions else "") + "vv_ss_qcd",
				)
				add_input(
						input_file=self.files_diboson(channel),
						weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel,exclude_cuts=exclude_cuts_B, cut_type=cut_type_B)+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
						nick=("noplot_" if not controlregions else "") + "vv_ss_qcd",
				)
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
								ss_os_factor = 1.76 if "BoostedCP" in category else 1.2 if "ZeroJetCP" in category else 2.00 if "dijet2D" in category else 1.0
							elif channel == "mt":
								ss_os_factor = 1.19 if "BoostedCP" in category else 1.15 if "ZeroJetCP" in category else 1.3 if "dijet2D_boosted" in category else 1.47 if "dijet2D_lowboost" in category else 1.0
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
						mc_sample_weight = make_multiplication([  mc_weight,
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
								input_file=self.files_ztt(channel),
								weight=Samples.ztt_genmatch(channel)+"*"+self.get_weights_ztt(channel=channel,cut_type=cut_type,mc_sample_weight=mc_sample_weight)+"*zPtReweightWeight"+"*"+zmm_cr_factor+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
								nick="noplot_ztt_"+estimation_type
						)
						if not (kwargs.get("no_ewk_samples", False) or kwargs.get("no_ewkz_as_dy", False)):
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
						add_input(
								input_file=self.files_vv(channel),
								weight=mc_sample_weight+"*"+self.vv_stitchingweight()+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
								nick="noplot_vv_"+estimation_type
						)
						add_input(
								input_file=self.files_diboson(channel),
								weight=mc_sample_weight+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
								nick="noplot_vv_"+estimation_type
						)
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
					if cut_type == "baseline2016":
						isolationDefinition = "((byMediumIsolationMVArun2v1DBoldDMwLT_1 > 0.5 && byLooseIsolationMVArun2v1DBoldDMwLT_2 > 0.5 && byTightIsolationMVArun2v1DBoldDMwLT_2 < 0.5) || (byMediumIsolationMVArun2v1DBoldDMwLT_2 > 0.5 && byLooseIsolationMVArun2v1DBoldDMwLT_1 > 0.5 && byTightIsolationMVArun2v1DBoldDMwLT_1 < 0.5))"
					elif cut_type == "smhtt2016":
						isolationDefinition = "((byMediumIsolationMVArun2v1DBoldDMwLT_1 > 0.5 && byLooseIsolationMVArun2v1DBoldDMwLT_2 > 0.5 && byTightIsolationMVArun2v1DBoldDMwLT_2 < 0.5) || (byMediumIsolationMVArun2v1DBoldDMwLT_2 > 0.5 && byLooseIsolationMVArun2v1DBoldDMwLT_1 > 0.5 && byTightIsolationMVArun2v1DBoldDMwLT_1 < 0.5))*((gen_match_1 == 5)*0.95 + (gen_match_1 != 5))*((gen_match_2 == 5)*0.95 + (gen_match_2 != 5))"
					elif cut_type == "cpggh2016":
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
								input_file=self.files_ztt(channel),
								weight=Samples.ztt_genmatch(channel)+"*"+self.get_weights_ztt(channel=channel,cut_type=cut_type,mc_sample_weight=mc_selection_weights[key])+"*zPtReweightWeight"+"*"+zmm_cr_factor,
								nick="noplot_ztt_"+key
						)
						if not (kwargs.get("no_ewk_samples", False) or kwargs.get("no_ewkz_as_dy", False)):
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
						add_input(
								input_file=self.files_vv(channel),
								weight=mc_selection_weights[key]+"*"+self.vv_stitchingweight(),
								nick="noplot_vv_"+key
						)
						add_input(
								input_file=self.files_diboson(channel),
								weight=mc_selection_weights[key],
								nick="noplot_vv_"+key
						)
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
							input_file=self.files_ztt(channel),
							weight=Samples.ztt_genmatch(channel)+"*"+self.get_weights_ztt(channel=channel,cut_type=cut_type,weight=weight)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_C, cut_type=cut_type_C)+"*zPtReweightWeight"+"*"+zmm_cr_factor,
							nick="noplot_ztt_ss_mc_wj_control"
					)
					if not (kwargs.get("no_ewk_samples", False) or kwargs.get("no_ewkz_as_dy", False)):
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
					add_input(
							input_file=self.files_vv(channel),
							weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_C, cut_type=cut_type_C)+"*"+self.vv_stitchingweight(),
							nick="noplot_vv_ss_wj_control"
					)
					add_input(
							input_file=self.files_diboson(channel),
							weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_C, cut_type=cut_type_C),
							nick="noplot_vv_ss_wj_control"
					)
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
						input_file=self.files_ztt(channel),
						weight=Samples.ztt_genmatch(channel)+"*"+self.get_weights_ztt(channel=channel,cut_type=cut_type,weight=weight)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_B , cut_type=cut_type_B)+"*zPtReweightWeight"+"*"+zmm_cr_factor+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
						nick="noplot_ztt_mc_qcd_control"
				)
				if not (kwargs.get("no_ewk_samples", False) or kwargs.get("no_ewkz_as_dy", False)):
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
				add_input(
						input_file=self.files_vv(channel),
						weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_B, cut_type=cut_type_B)+"*"+self.vv_stitchingweight()+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
						nick="noplot_vv_qcd_control"
				)
				add_input(
						input_file=self.files_diboson(channel),
						weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_B, cut_type=cut_type_B)+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
						nick="noplot_vv_qcd_control"
				)

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

	def htt(self, config, channel, category, weight, nick_suffix, higgs_masses, normalise_signal_to_one_pb=False, lumi=default_lumi, exclude_cuts=None, additional_higgs_masses_for_shape=[], mssm=False, normalise_to_sm_xsec=False, **kwargs):
		
		if exclude_cuts is None:
			exclude_cuts = []

		# gluon fusion (SM/MSSM)
		config = self.ggh(config, channel, category, weight, nick_suffix+"_noplot", higgs_masses+additional_higgs_masses_for_shape,
		                  normalise_signal_to_one_pb, lumi=lumi, exclude_cuts=exclude_cuts, no_plot=True, mssm=mssm, **kwargs)
		if mssm and  normalise_to_sm_xsec:
			config = self.ggh(config, channel, category, weight, nick_suffix+"_sm_noplot", higgs_masses,
			                  normalise_signal_to_one_pb, lumi=lumi, exclude_cuts=exclude_cuts, no_plot=True, mssm=False, **kwargs)
		
		# vector boson fusion (SM)
		if (not mssm) or normalise_to_sm_xsec:
			config = self.qqh(config, channel, category, weight, nick_suffix+("_sm" if mssm else "")+"_noplot", higgs_masses+([] if mssm else additional_higgs_masses_for_shape),
			                  normalise_signal_to_one_pb, lumi=lumi, exclude_cuts=exclude_cuts, no_plot=True, **kwargs)
		
		# Higgs strahlung (SM)
		if (not mssm) or normalise_to_sm_xsec:
			config = self.vh(config, channel, category, weight, nick_suffix+("_sm" if mssm else "")+"_noplot", higgs_masses+([] if mssm else additional_higgs_masses_for_shape),
			                 normalise_signal_to_one_pb, lumi=lumi, exclude_cuts=exclude_cuts, no_plot=True, **kwargs)

		# production in association with b-quarks (MSSM)
		if mssm:
			config = self.bbh(config, channel, category, weight, nick_suffix+"_noplot", higgs_masses+additional_higgs_masses_for_shape,
			                  normalise_signal_to_one_pb, lumi=lumi, exclude_cuts=exclude_cuts, no_plot=True, **kwargs)
			
		def final_nick(tmp_sample, tmp_mass, add_nick_suffix=True):
			return tmp_sample+str(kwargs.get("cp", ""))+str(tmp_mass)+("_"+str(int(kwargs["scale_signal"])) if kwargs.get("scale_signal", 1.0) != 1.0 else "")+(nick_suffix if add_nick_suffix else "")

		for index, mass in enumerate(additional_higgs_masses_for_shape+higgs_masses):
			is_additional_mass = (index < len(additional_higgs_masses_for_shape))
			
			if not "AddHistograms" in config.get("analysis_modules", []):
				config.setdefault("analysis_modules", []).append("AddHistograms")
			config.setdefault("add_nicks", []).append(" ".join([final_nick(sample, mass)+"_noplot" for sample in ["ggh"]+(["bbh"] if mssm else ["qqh", "vh"])]))
			config.setdefault("add_result_nicks", []).append(final_nick("htt", mass)+"_noplot")
			
			if not is_additional_mass:
				config.setdefault("add_nicks", []).append(" ".join([final_nick("htt", m)+"_noplot" for m in [mass]+additional_higgs_masses_for_shape]))
				config.setdefault("add_result_nicks", []).append(final_nick("htt", mass)+"_noplot_shape")
				
				if mssm and normalise_to_sm_xsec:
					config.setdefault("add_nicks", []).append(" ".join([final_nick(sample, mass)+"_sm_noplot" for sample in ["ggh", "qqh", "vh"]]))
					config.setdefault("add_result_nicks", []).append(final_nick("htt", mass)+"_sm_noplot")
				
				if not "ShapeYieldMerge" in config.get("analysis_modules", []):
					config.setdefault("analysis_modules", []).append("ShapeYieldMerge")
				config.setdefault("shape_nicks", []).append(final_nick("htt", mass)+"_noplot_shape")
				config.setdefault("yield_nicks", []).append(final_nick("htt", mass)+("_sm" if mssm and normalise_to_sm_xsec else "")+"_noplot")
				config.setdefault("shape_yield_nicks", []).append(final_nick("htt", mass))
			
			if (not kwargs.get("no_plot", False)) and (not is_additional_mass):
				if not mssm:
					Samples._add_bin_corrections(
							config,
							final_nick("htt", mass),
							nick_suffix
					)
				Samples._add_plot(
						config,
						"bkg" if kwargs.get("stack_signal", False) else "htt",
						"LINE",
						"L",
						final_nick("htt", mass, False),
						nick_suffix
				)
		return config

	# samples which merge susy_ggh and bbh
	# susy ssamples to be used with SM analysis (mssm = False)
	def susy(self, config, channel, category, weight, nick_suffix, higgs_masses, normalise_signal_to_one_pb=False, lumi=default_lumi, exclude_cuts=None, additional_higgs_masses_for_shape=[], mssm=False, normalise_to_sm_xsec=False, **kwargs):
		
		if exclude_cuts is None:
			exclude_cuts = []

		# lumi multiplied by a factor of 1.9 to correctly normalize samples to SM samples
		# susy ggh
		config = self.susy_ggh(config, channel, category, weight, nick_suffix+"_noplot", higgs_masses+additional_higgs_masses_for_shape,
		                  normalise_signal_to_one_pb, lumi=lumi*1.9, exclude_cuts=exclude_cuts, no_plot=True, mssm=mssm, **kwargs)
		# bbh
		config = self.bbh(config, channel, category, weight, nick_suffix+"_noplot", higgs_masses+additional_higgs_masses_for_shape,
		                  normalise_signal_to_one_pb, lumi=lumi*1.9, exclude_cuts=exclude_cuts, no_plot=True, mssm=mssm, **kwargs)
		
		def final_nick(tmp_sample, tmp_mass, add_nick_suffix=True):
			return tmp_sample+str(kwargs.get("cp", ""))+str(tmp_mass)+("_"+str(int(kwargs["scale_signal"])) if kwargs.get("scale_signal", 1.0) != 1.0 else "")+(nick_suffix if add_nick_suffix else "")

		for index, mass in enumerate(additional_higgs_masses_for_shape+higgs_masses):
			is_additional_mass = (index < len(additional_higgs_masses_for_shape))
			
			if not "AddHistograms" in config.get("analysis_modules", []):
				config.setdefault("analysis_modules", []).append("AddHistograms")
			config.setdefault("add_nicks", []).append(" ".join([final_nick(sample, mass)+"_noplot" for sample in ["susy_ggh"]+["bbh"] ]))
			config.setdefault("add_result_nicks", []).append(final_nick("susy", mass)+"_noplot")
			
			if not is_additional_mass:
				config.setdefault("add_nicks", []).append(" ".join([final_nick("susy", m)+"_noplot" for m in [mass]+additional_higgs_masses_for_shape]))
				config.setdefault("add_result_nicks", []).append(final_nick("susy", mass)+"_noplot_shape")
				
				if not "ShapeYieldMerge" in config.get("analysis_modules", []):
					config.setdefault("analysis_modules", []).append("ShapeYieldMerge")
				config.setdefault("shape_nicks", []).append(final_nick("susy", mass)+"_noplot_shape")
				config.setdefault("yield_nicks", []).append(final_nick("susy", mass)+("_sm" if mssm and normalise_to_sm_xsec else "")+"_noplot")
				config.setdefault("shape_yield_nicks", []).append(final_nick("susy", mass))
			
			if (not kwargs.get("no_plot", False)) and (not is_additional_mass):
				if not mssm:
					Samples._add_bin_corrections(
							config,
							final_nick("susy", mass),
							nick_suffix
					)
				Samples._add_plot(
						config,
						"bkg" if kwargs.get("stack_signal", False) else "susy",
						"LINE",
						"L",
						final_nick("susy", mass, False),
						nick_suffix
				)
		return config

	# signal samples for CP studies in the final state
	# cp-even state
	def httcpeven(self, config, channel, category, weight, nick_suffix, higgs_masses, normalise_signal_to_one_pb=False, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", mssm=False, normalise_to_sm_xsec=True, **kwargs):
		config = self.htt( config, channel, category, weight, "cpeven"+nick_suffix, higgs_masses, normalise_signal_to_one_pb=normalise_signal_to_one_pb, lumi=lumi, exclude_cuts=exclude_cuts, cut_type=cut_type, mssm=mssm, normalise_to_sm_xsec=normalise_to_sm_xsec, cp="cpeven", stacks="httcpeven", **kwargs)
		return config
	
	# cp-odd state from SM samples %FIXME 
	def httcpodd(self, config, channel, category, weight, nick_suffix, higgs_masses, normalise_signal_to_one_pb=False, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", mssm=False, **kwargs):
		config = self.htt( config, channel, category, weight, "cpodd"+nick_suffix, higgs_masses, normalise_signal_to_one_pb=normalise_signal_to_one_pb, lumi=lumi, exclude_cuts=exclude_cuts, cut_type=cut_type, mssm=mssm, cp="cpodd", stacks="httcpodd", **kwargs)
		return config

	# cp-odd state from SUSY samples
	def susycpodd(self, config, channel, category, weight, nick_suffix, higgs_masses, normalise_signal_to_one_pb=False, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", mssm=False, normalise_to_sm_xsec=True, **kwargs):
		config = self.susy( config, channel, category, weight, "cpodd"+nick_suffix, higgs_masses, normalise_signal_to_one_pb=normalise_signal_to_one_pb, lumi=lumi, exclude_cuts=exclude_cuts, cut_type=cut_type, mssm=mssm, normalise_to_sm_xsec=normalise_to_sm_xsec, cp="cpodd", stacks="susycpodd", **kwargs)
		return config

	# cp-mix state from SM samples
	def httcpmix(self, config, channel, category, weight, nick_suffix, higgs_masses, normalise_signal_to_one_pb=False, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", mssm=False, **kwargs):
		config = self.htt( config, channel, category, weight, "cpmix"+nick_suffix, higgs_masses, normalise_signal_to_one_pb=normalise_signal_to_one_pb, lumi=lumi, exclude_cuts=exclude_cuts, cut_type=cut_type, mssm=mssm, cp="cpmix", stacks="httcpmix", **kwargs)
		return config


	def files_bbh(self, channel, mass=125):
		return self.artus_file_names({"process" : "SUSYGluGluToBBHToTauTau_M"+str(mass), "data": False, "campaign" : self.mc_campaign}, 1)

	def bbh(self, config, channel, category, weight, nick_suffix, higgs_masses, normalise_signal_to_one_pb=False, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []

		scale_factor = lumi
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("bbh", 1.0)

		data_weight, mc_weight = self.projection(kwargs)
		add_input = partialmethod(Samples._add_input, config=config, folder=self.root_file_folder(channel), scale_factor=lumi, nick_suffix=nick_suffix)

		for mass in higgs_masses:
			if channel in ["tt", "et", "mt", "em", "ttbar"]:
				add_input(
						input_file=self.files_bbh(channel, str(int(mass)-5)) if int(mass)==125 else self.files_bbh(channel, mass),
						scale_factor=lumi*kwargs.get("scale_signal", 1.0),
						weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
						nick="bbh"+str(kwargs.get("cp", ""))+str(mass)+("_"+str(int(kwargs["scale_signal"])) if kwargs.get("scale_signal", 1.0) != 1.0 else "")
				)
			else:
				log.error("Sample config (bbH%s) currently not implemented for channel \"%s\"!" % (str(mass), channel))

			if not kwargs.get("no_plot", False):
				if not kwargs.get("mssm", False):
					Samples._add_bin_corrections(
							config,
							"bbh"+str(kwargs.get("cp", ""))+str(mass)+("_"+str(int(kwargs["scale_signal"])) if kwargs.get("scale_signal", 1.0) != 1.0 else ""),
							str(kwargs.get("cp", ""))+nick_suffix
					)
				Samples._add_plot(
						config,
						"bkg" if kwargs.get("stack_signal", False) else "bbh",
						"LINE",
						"L",
						"bbh"+str(kwargs.get("cp", ""))+str(mass)+("_"+str(int(kwargs["scale_signal"])) if kwargs.get("scale_signal", 1.0) != 1.0 else ""),
						str(kwargs.get("cp", ""))+nick_suffix
				)
		return config

	def files_ggh(self, channel, mass=125, **kwargs):
		cp = kwargs.get("cp", None)
		if cp is None or cp == "cpeven":
			#CAUTION: If necessary the mc-generator nick might need to be updated from time to time.
			return self.artus_file_names({"process" : "GluGluHToTauTau_M"+str(mass), "data": False, "campaign" : self.mc_campaign, "generator" : "powheg-pythia8"}, 1)
		
		elif "jhu" in cp:
			if "sm" in cp:
				return "GluGluH2JetsToTauTauM125CPmixingsmJHU_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_JHUgen/*.root"		
			if "ps" in cp:
				return "GluGluH2JetsToTauTauM125CPmixingpseudoscalarJHU_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_JHUgen/*.root"
			if "mm" in cp:
				return "GluGluH2JetsToTauTauM125CPmixingmaxmixJHU_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_JHUgen/*.root"
		elif cp in ["sm", "mm", "ps"]:
			return "GluGluToHToTauTauM125_RunIIFall15MiniAODv2_PU25nsData2015v1_13TeV_MINIAOD_amcatnlo-pythia8/*.root"
	
	def files_susy_ggh(self, channel, mass=125):
		return self.artus_file_names({"process" : "SUSYGluGluToHToTauTauM"+str(mass), "data": False, "campaign" : self.mc_campaign}, 1)

	def susy_ggh(self, config, channel, category, weight, nick_suffix, higgs_masses, normalise_signal_to_one_pb=False, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", mssm=False, **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []
		
		scale_factor = lumi
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("susy_ggh", 1.0)

		data_weight, mc_weight = self.projection(kwargs)
		add_input = partialmethod(Samples._add_input, config=config, folder=self.root_file_folder(channel), scale_factor=lumi, nick_suffix=nick_suffix)

		for mass in higgs_masses:
			if channel in ["tt", "et", "mt", "em", "mm", "ee", "ttbar"]:
				add_input(
						input_file=self.files_susy_ggh(channel, str(int(mass)-5)) if int(mass)==125 else self.files_susy_ggh(channel, mass),
						scale_factor=lumi*kwargs.get("scale_signal", 1.0),
						weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
						nick="susy_ggh"+str(kwargs.get("cp", ""))+str(mass)+("_"+str(int(kwargs["scale_signal"])) if kwargs.get("scale_signal", 1.0) != 1.0 else "")
				)
			else:
				log.error("Sample config (ggH%s) currently not implemented for channel \"%s\"!" % (str(mass), channel))

			if not kwargs.get("no_plot", False):
				if not mssm:
					Samples._add_bin_corrections(
							config,
							"susy_ggh"+str(kwargs.get("cp", ""))+str(mass)+("_"+str(int(kwargs["scale_signal"])) if kwargs.get("scale_signal", 1.0) != 1.0 else ""),
							str(kwargs.get("cp", ""))+nick_suffix
					)
				Samples._add_plot(
						config,
						"bkg" if kwargs.get("stack_signal", False) else kwargs.get("stacks", "susy_ggh"),
						"LINE",
						"L",
						"susy_ggh"+str(kwargs.get("cp", ""))+str(mass)+("_"+str(int(kwargs["scale_signal"])) if kwargs.get("scale_signal", 1.0) != 1.0 else ""),
						str(kwargs.get("cp", ""))+nick_suffix
				)
		return config
		
	def ggh(self, config, channel, category, weight, nick_suffix, higgs_masses, normalise_signal_to_one_pb=False, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", mssm=False, **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []
		
		scale_factor = lumi
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("ggh", 1.0)

		data_weight, mc_weight = self.projection(kwargs)
		add_input = partialmethod(Samples._add_input, config=config, folder=self.root_file_folder(channel), scale_factor=lumi, nick_suffix=nick_suffix)
		
		matrix_weight = "(1.0)*"
		if (kwargs.get("cp", None) == "sm"):
			matrix_weight = "(madGraphWeightSample>-899)*"
		elif(kwargs.get("cp", None) == "mm"):
			matrix_weight = "(madGraphWeight050/madGraphWeightSample)*(madGraphWeight000>-899)*(madGraphWeightSample>-899)*"
		elif(kwargs.get("cp", None) == "ps"):
			matrix_weight = "(madGraphWeight100/madGraphWeightSample)*(madGraphWeight000>-899)*(madGraphWeightSample>-899)*"

		# tauSpinner weight for CP study in the final state
		tauSpinner_weight = "(1.0)"
		#if (kwargs.get("cp", None) == "cpeven"):
		#	tauSpinner_weight = "(tauSpinnerWeightInvSample)*(tauSpinnerWeight000)"
		#if (kwargs.get("cp", None) == "cpmix"):
		#	tauSpinner_weight = "(tauSpinnerWeightInvSample)*(tauSpinnerWeight050)"
		#if (kwargs.get("cp", None) == "cpodd"):
		#	tauSpinner_weight = "(tauSpinnerWeightInvSample)*(tauSpinnerWeight100)"

		for mass in higgs_masses:
			if channel in ["tt", "et", "mt", "em", "mm", "ee", "ttbar"]:

				add_input(
						input_file=self.files_ggh(channel, mass, cp=kwargs.get('cp', None)) if not mssm else self.files_susy_ggh(channel, mass),
						scale_factor=lumi*kwargs.get("scale_signal", 1.0),
						weight=tauSpinner_weight+"*"+matrix_weight+mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
						nick="ggh"+str(kwargs.get("cp", ""))+str(mass)+("_"+str(int(kwargs["scale_signal"])) if kwargs.get("scale_signal", 1.0) != 1.0 else "")
				)
			else:
				log.error("Sample config (ggH%s) currently not implemented for channel \"%s\"!" % (str(mass), channel))

			if not kwargs.get("no_plot", False):
				if not mssm:
					Samples._add_bin_corrections(
							config,
							"ggh"+str(kwargs.get("cp", ""))+str(mass)+("_"+str(int(kwargs["scale_signal"])) if kwargs.get("scale_signal", 1.0) != 1.0 else ""),
							str(kwargs.get("cp", ""))+nick_suffix
					)
				Samples._add_plot(
						config,
						"bkg" if kwargs.get("stack_signal", False) else kwargs.get("stacks", "ggh"),
						"LINE",
						"L",
						"ggh"+str(kwargs.get("cp", ""))+str(mass)+("_"+str(int(kwargs["scale_signal"])) if kwargs.get("scale_signal", 1.0) != 1.0 else ""),
						str(kwargs.get("cp", ""))+nick_suffix
				)
		return config

	def gghsm(self, config, channel, category, weight, nick_suffix, higgs_masses, normalise_signal_to_one_pb=False, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", mssm=False, **kwargs):
		config = self.ggh( config, channel, category, weight, "sm"+nick_suffix, higgs_masses, normalise_signal_to_one_pb=normalise_signal_to_one_pb, lumi=lumi, exclude_cuts=exclude_cuts, cut_type=cut_type, mssm=mssm, cp="sm", stacks="gghsm", **kwargs)
		return config
	
	def gghjhusm(self, config, channel, category, weight, nick_suffix, higgs_masses, normalise_signal_to_one_pb=False, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", mssm=False, **kwargs):
		config = self.ggh( config, channel, category, weight, "jhusm"+nick_suffix, higgs_masses, normalise_signal_to_one_pb=normalise_signal_to_one_pb, lumi=lumi, exclude_cuts=exclude_cuts, cut_type=cut_type, mssm=mssm, cp="jhusm", stacks="gghjhusm", **kwargs)
		return config	

	def gghmm(self, config, channel, category, weight, nick_suffix, higgs_masses, normalise_signal_to_one_pb=False, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", mssm=False, **kwargs):
		config = self.ggh(config, channel, category, weight, "mm"+nick_suffix, higgs_masses, normalise_signal_to_one_pb=normalise_signal_to_one_pb, lumi=lumi, exclude_cuts=exclude_cuts, cut_type=cut_type, mssm=mssm, cp="mm", stacks="gghmm", **kwargs)
		return config

	def gghjhumm(self, config, channel, category, weight, nick_suffix, higgs_masses, normalise_signal_to_one_pb=False, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", mssm=False, **kwargs):
		config = self.ggh(config, channel, category, weight, "jhumm"+nick_suffix, higgs_masses, normalise_signal_to_one_pb=normalise_signal_to_one_pb, lumi=lumi, exclude_cuts=exclude_cuts, cut_type=cut_type, mssm=mssm, cp="jhumm", stacks="gghjhumm", **kwargs)
		return config
	
	def gghps(self, config, channel, category, weight, nick_suffix, higgs_masses, normalise_signal_to_one_pb=False, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", mssm=False, **kwargs):
		config = self.ggh(config, channel, category, weight, "ps"+nick_suffix, higgs_masses, normalise_signal_to_one_pb=normalise_signal_to_one_pb, lumi=lumi, exclude_cuts=exclude_cuts, cut_type=cut_type, mssm=mssm, cp="ps", stacks="gghps", **kwargs)
		return config
	 
	def gghjhups(self, config, channel, category, weight, nick_suffix, higgs_masses, normalise_signal_to_one_pb=False, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", mssm=False, **kwargs):
		config = self.ggh(config, channel, category, weight, "jhups"+nick_suffix, higgs_masses, normalise_signal_to_one_pb=normalise_signal_to_one_pb, lumi=lumi, exclude_cuts=exclude_cuts, cut_type=cut_type, mssm=mssm, cp="jhups", stacks="gghjhups", **kwargs)
		return config
	
	def files_qqh(self, channel, mass=125, **kwargs):
		cp = kwargs.get("cp", None)
		
		if cp is None or  cp =="cpeven":
			#CAUTION: If necessary the mc-generator nick might need to be updated from time to time.
			return self.artus_file_names({"process" : "VBFHToTauTauM"+str(mass), "data": False, "campaign" : self.mc_campaign, "generator" : "powheg-pythia8"}, 1)
		
		elif "jhu" in cp:
			if "sm" in cp:
				return "VBFHiggs0PMM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_JHUgenv6//*.root"		
			if "ps" in cp:
				return "VBFHiggs0MM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_JHUgenv6/*.root"
			if "mm" in cp:
				return "VBFHiggs0Mf05ph0M125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_JHUgenv6/*.root"
		elif cp in ["sm", "mm", "ps"]:
			return "VBFHToTauTauM125_RunIISpring16MiniAODv2reHLT_PUSpring16RAWAODSIM_13TeV_MINIAOD_amcatnlo-pythia8/*.root"
	
	def qqh(self, config, channel, category, weight, nick_suffix, higgs_masses, normalise_signal_to_one_pb=False, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []

		scale_factor = lumi
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("qqH", 1.0)

		data_weight, mc_weight = self.projection(kwargs)
		matrix_weight = "(1.0)*"
		if (kwargs.get("cp", None) == "sm"):
			matrix_weight = "(madGraphWeight000/madGraphWeightSample)*(madGraphWeight000>-899)*(madGraphWeightSample>-899)*"
		elif(kwargs.get("cp", None) == "mm"):
			matrix_weight = "(madGraphWeight050/madGraphWeightSample)*(madGraphWeight000>-899)*(madGraphWeightSample>-899)*"
		elif(kwargs.get("cp", None) == "ps"):
			matrix_weight = "(madGraphWeight100/madGraphWeightSample)*(madGraphWeight000>-899)*(madGraphWeightSample>-899)*"

		# tauSpinner weight for CP study in the final state
		tauSpinner_weight = "(1.0)"
		#if (kwargs.get("cp", None) == "cpeven"):
		#	tauSpinner_weight = "(tauSpinnerWeightInvSample)*(tauSpinnerWeight000)"
		#if (kwargs.get("cp", None) == "cpmix"):
		#	tauSpinner_weight = "(tauSpinnerWeightInvSample)*(tauSpinnerWeight050)"
		#if (kwargs.get("cp", None) == "cpodd"):
		#	tauSpinner_weight = "(tauSpinnerWeightInvSample)*(tauSpinnerWeight100)"

		data_weight, mc_weight = self.projection(kwargs)
		add_input = partialmethod(Samples._add_input, config=config, folder=self.root_file_folder(channel), scale_factor=lumi, nick_suffix=nick_suffix)

		for mass in higgs_masses:
			if channel in ["tt", "et", "mt", "em", "mm", "ee", "ttbar"]:
				add_input(
						input_file=self.files_qqh(channel, mass, cp=kwargs.get("cp", None)),
						scale_factor=lumi,
						weight=tauSpinner_weight+"*"+matrix_weight+mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
						nick="qqh"+str(kwargs.get("cp", ""))+str(mass)
			)
			else:
				log.error("Sample config (VBF%s) currently not implemented for channel \"%s\"!" % (str(mass), channel))

			if not kwargs.get("no_plot", False):
				if not kwargs.get("mssm", False):
					Samples._add_bin_corrections(
							config,
							"qqh"+str(kwargs.get("cp", ""))+str(mass),
							str(kwargs.get("cp", ""))+nick_suffix
					)
				Samples._add_plot(
						config,
						"bkg",# if kwargs.get("stack_signal", False) else kwargs.get("stacks", "qqh"),
						"HIST",
						"F",
						"qqh"+str(kwargs.get("cp", ""))+str(mass),
						str(kwargs.get("cp", ""))+nick_suffix
				)
		return config

	def qqhsm(self, config, channel, category, weight, nick_suffix, higgs_masses, normalise_signal_to_one_pb=False, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", mssm=False, **kwargs):
		config = self.qqh( config, channel, category, weight, "sm"+nick_suffix, higgs_masses, normalise_signal_to_one_pb=normalise_signal_to_one_pb, lumi=lumi, exclude_cuts=exclude_cuts, cut_type=cut_type, mssm=mssm, cp="sm", stacks="qqhsm", **kwargs)
		return config

	def qqhmm(self, config, channel, category, weight, nick_suffix, higgs_masses, normalise_signal_to_one_pb=False, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", mssm=False, **kwargs):
		config = self.qqh(config, channel, category, weight, "mm"+nick_suffix, higgs_masses, normalise_signal_to_one_pb=normalise_signal_to_one_pb, lumi=lumi, exclude_cuts=exclude_cuts, cut_type=cut_type, mssm=mssm, cp="mm", stacks="qqhmm", **kwargs)
		return config

	def qqhps(self, config, channel, category, weight, nick_suffix, higgs_masses, normalise_signal_to_one_pb=False, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", mssm=False, **kwargs):
		config = self.qqh(config, channel, category, weight, "ps"+nick_suffix, higgs_masses, normalise_signal_to_one_pb=normalise_signal_to_one_pb, lumi=lumi, exclude_cuts=exclude_cuts, cut_type=cut_type, mssm=mssm, cp="ps", stacks="qqhps", **kwargs)
		return config	

	def qqhjhusm(self, config, channel, category, weight, nick_suffix, higgs_masses, normalise_signal_to_one_pb=False, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", mssm=False, **kwargs):
		config = self.qqh( config, channel, category, weight, "jhusm"+nick_suffix, higgs_masses, normalise_signal_to_one_pb=normalise_signal_to_one_pb, lumi=lumi, exclude_cuts=exclude_cuts, cut_type=cut_type, mssm=mssm, cp="jhusm", stacks="qqhjhusm", **kwargs)
		return config

	def qqhjhumm(self, config, channel, category, weight, nick_suffix, higgs_masses, normalise_signal_to_one_pb=False, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", mssm=False, **kwargs):
		config = self.qqh(config, channel, category, weight, "jhumm"+nick_suffix, higgs_masses, normalise_signal_to_one_pb=normalise_signal_to_one_pb, lumi=lumi, exclude_cuts=exclude_cuts, cut_type=cut_type, mssm=mssm, cp="jhumm", stacks="qqhjhumm", **kwargs)
		return config

	def qqhjhups(self, config, channel, category, weight, nick_suffix, higgs_masses, normalise_signal_to_one_pb=False, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", mssm=False, **kwargs):
		config = self.qqh(config, channel, category, weight, "jhups"+nick_suffix, higgs_masses, normalise_signal_to_one_pb=normalise_signal_to_one_pb, lumi=lumi, exclude_cuts=exclude_cuts, cut_type=cut_type, mssm=mssm, cp="jhups", stacks="qqhjhups", **kwargs)
		return config	
	
	def vh(self, config, channel, category, weight, nick_suffix, higgs_masses, normalise_signal_to_one_pb=False, lumi=default_lumi, exclude_cuts=None, **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []

		no_plot_kwargs = copy.deepcopy(kwargs)
		no_plot_kwargs["no_plot"] = True
		config = self.wh(config, channel, category, weight, nick_suffix+"_noplot", higgs_masses,
		                 normalise_signal_to_one_pb, lumi=lumi, exclude_cuts=exclude_cuts, **no_plot_kwargs)
		config = self.zh(config, channel, category, weight, nick_suffix+"_noplot", higgs_masses,
		                 normalise_signal_to_one_pb, lumi=lumi, exclude_cuts=exclude_cuts, **no_plot_kwargs)
		for mass in higgs_masses:
			if not "AddHistograms" in config.get("analysis_modules", []):
				config.setdefault("analysis_modules", []).append("AddHistograms")
			config.setdefault("add_nicks", []).append(" ".join([sample+str(kwargs.get("cp", ""))+str(mass)+("_"+str(int(kwargs["scale_signal"])) if kwargs.get("scale_signal", 1.0) != 1.0 else "")+nick_suffix+"_noplot" for sample in ["wh", "zh"]]))
			config.setdefault("add_result_nicks", []).append("vh"+str(kwargs.get("cp", ""))+str(mass)+("_"+str(int(kwargs["scale_signal"])) if kwargs.get("scale_signal", 1.0) != 1.0 else "")+nick_suffix)

			if not kwargs.get("no_plot", False):
				if not kwargs.get("mssm", False):
					Samples._add_bin_corrections(
							config,
							"vh"+str(mass)+("_"+str(int(kwargs["scale_signal"])) if kwargs.get("scale_signal", 1.0) != 1.0 else ""),
							nick_suffix
					)
				Samples._add_plot(
						config,
						"bkg" if kwargs.get("stack_signal", False) else "vh",
						"LINE",
						"L",
						"vh"+str(mass)+("_"+str(int(kwargs["scale_signal"])) if kwargs.get("scale_signal", 1.0) != 1.0 else ""),
						nick_suffix
				)
		return config

	def files_wh_minus(self, channel, mass=125):
		return self.artus_file_names({"process" : "WminusHToTauTau_M"+str(mass), "data": False, "campaign" : self.mc_campaign}, 1)

	def files_wh_plus(self, channel, mass=125):
		return self.artus_file_names({"process" : "WplusHToTauTau_M"+str(mass), "data": False, "campaign" : self.mc_campaign}, 1)

	def wh(self, config, channel, category, weight, nick_suffix, higgs_masses, normalise_signal_to_one_pb=False, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []

		scale_factor = lumi
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("WH", 1.0)

		data_weight, mc_weight = self.projection(kwargs)
		add_input = partialmethod(Samples._add_input, config=config, folder=self.root_file_folder(channel), scale_factor=lumi, nick_suffix=nick_suffix)

		# tauSpinner weight for CP study in the final state
		tauSpinner_weight = "(1.0)"
		#if (kwargs.get("cp", None) == "cpeven"):
		#	tauSpinner_weight = "(tauSpinnerWeightInvSample)*(tauSpinnerWeight000)"
		#if (kwargs.get("cp", None) == "cpmix"):
		#	tauSpinner_weight = "(tauSpinnerWeightInvSample)*(tauSpinnerWeight050)"
		#if (kwargs.get("cp", None) == "cpodd"):
		#	tauSpinner_weight = "(tauSpinnerWeightInvSample)*(tauSpinnerWeight100)"

		for mass in higgs_masses:
			if channel in ["tt", "et", "mt", "em", "mm", "ee", "ttbar"]:
				add_input(
						input_file=self.files_wh_minus(channel, mass),
						scale_factor=lumi*kwargs.get("scale_signal", 1.0),
						weight=tauSpinner_weight+"*"+mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
						nick="wmh"+str(kwargs.get("cp", ""))+str(mass)+("_"+str(int(kwargs["scale_signal"])) if kwargs.get("scale_signal", 1.0) != 1.0 else ""),
						nick_suffix=nick_suffix+"_noplot"
				)
				add_input(
						input_file=self.files_wh_plus(channel, mass),
						scale_factor=lumi*kwargs.get("scale_signal", 1.0),
						weight=tauSpinner_weight+"*"+mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
						nick="wph"+str(kwargs.get("cp", ""))+str(mass)+("_"+str(int(kwargs["scale_signal"])) if kwargs.get("scale_signal", 1.0) != 1.0 else ""),
						nick_suffix=nick_suffix+"_noplot"
				)

				if not "AddHistograms" in config.get("analysis_modules", []):
					config.setdefault("analysis_modules", []).append("AddHistograms")
				config.setdefault("add_nicks", []).append(" ".join([sample+str(kwargs.get("cp", ""))+str(mass)+("_"+str(int(kwargs["scale_signal"])) if kwargs.get("scale_signal", 1.0) != 1.0 else "")+nick_suffix+"_noplot" for sample in ["wmh", "wph"]]))
				config.setdefault("add_result_nicks", []).append("wh"+str(kwargs.get("cp", ""))+str(mass)+("_"+str(int(kwargs["scale_signal"])) if kwargs.get("scale_signal", 1.0) != 1.0 else "")+nick_suffix)

			else:
				log.error("Sample config (WH%s) currently not implemented for channel \"%s\"!" % (str(mass), channel))

			if not kwargs.get("no_plot", False):
				if not kwargs.get("mssm", False):
					Samples._add_bin_corrections(
							config,
							"wh"+str(kwargs.get("cp", ""))+str(mass)+("_"+str(int(kwargs["scale_signal"])) if kwargs.get("scale_signal", 1.0) != 1.0 else ""),
							str(kwargs.get("cp", ""))+nick_suffix
					)
				Samples._add_plot(
						config,
						"wh",
						"LINE",
						"L",
						"wh"+str(kwargs.get("cp", ""))+str(mass)+("_"+str(int(kwargs["scale_signal"])) if kwargs.get("scale_signal", 1.0) != 1.0 else ""),
						str(kwargs.get("cp", ""))+nick_suffix
				)
		return config

	def files_zh(self, channel, mass=125):
		return self.artus_file_names({"process" : "ZHToTauTau_M"+str(mass), "data": False, "campaign" : self.mc_campaign}, 1)

	def zh(self, config, channel, category, weight, nick_suffix, higgs_masses, normalise_signal_to_one_pb=False, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []

		scale_factor = lumi
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("ZH", 1.0)

		data_weight, mc_weight = self.projection(kwargs)
		add_input = partialmethod(Samples._add_input, config=config, folder=self.root_file_folder(channel), scale_factor=lumi, nick_suffix=nick_suffix)

		# tauSpinner weight for CP study in the final state
		tauSpinner_weight = "(1.0)"
		#if (kwargs.get("cp", None) == "cpeven"):
		#	tauSpinner_weight = "(tauSpinnerWeightInvSample)*(tauSpinnerWeight000)"
		#if (kwargs.get("cp", None) == "cpmix"):
		#	tauSpinner_weight = "(tauSpinnerWeightInvSample)*(tauSpinnerWeight050)"
		#if (kwargs.get("cp", None) == "cpodd"):
		#	tauSpinner_weight = "(tauSpinnerWeightInvSample)*(tauSpinnerWeight100)"

		for mass in higgs_masses:
			if channel in ["tt", "et", "mt", "em", "mm", "ee", "ttbar"]:
				add_input(
						input_file=self.files_zh(channel, mass),
						scale_factor=lumi*kwargs.get("scale_signal", 1.0),
						weight=tauSpinner_weight+"*"+mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+self.em_triggerweight_dz_filter(channel, cut_type=cut_type),
						nick="zh"+str(kwargs.get("cp", ""))+str(mass)+("_"+str(int(kwargs["scale_signal"])) if kwargs.get("scale_signal", 1.0) != 1.0 else "")
				)

			else:
				log.error("Sample config (ZH%s) currently not implemented for channel \"%s\"!" % (str(mass), channel))

			if not kwargs.get("no_plot", False):
				if not kwargs.get("mssm", False):
					Samples._add_bin_corrections(
							config,
							"zh"+str(kwargs.get("cp", ""))+str(mass)+("_"+str(int(kwargs["scale_signal"])) if kwargs.get("scale_signal", 1.0) != 1.0 else ""),
							str(kwargs.get("cp", ""))+nick_suffix
					)
				Samples._add_plot(
						config,
						"zh",
						"LINE",
						"L",
						"zh"+str(kwargs.get("cp", ""))+str(mass)+("_"+str(int(kwargs["scale_signal"])) if kwargs.get("scale_signal", 1.0) != 1.0 else ""),
						str(kwargs.get("cp", ""))+nick_suffix
				)
		return config


	def ff(self, config, channel, category, weight, nick_suffix, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []
			
		add_input = partialmethod(Samples._add_input, config=config, folder=self.root_file_folder(channel), scale_factor=lumi, nick_suffix=nick_suffix)

		if channel in ["mt","et"]:
			add_input(
					input_file=self.files_data(channel),
					scale_factor=1.0,
					weight=weight+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["iso_2"], cut_type=cut_type)+"*eventWeight*jetToTauFakeWeight_comb",
					nick="ff"
			)

			add_input(
					input_file=self.files_ztt(channel),
					weight=self.get_weights_ztt(channel=channel,cut_type=cut_type,weight=weight)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["iso_2"], cut_type=cut_type)+"*zPtReweightWeight*(gen_match_2 < 6)*jetToTauFakeWeight_comb",
					nick="noplot_dy_ff_control"
			)
			add_input(
					input_file=self.files_ttj(channel),
					weight=weight+"*"+self.embedding_ttbarveto_weight(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["iso_2"], cut_type=cut_type)+"*topPtReweightWeight*eventWeight*(gen_match_2 < 6)*jetToTauFakeWeight_comb",
					nick="noplot_tt_ff_control"
			)
			add_input(
					input_file=self.files_vv(channel),
					weight=weight+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["iso_2"], cut_type=cut_type)+"*eventWeight*(gen_match_2 < 6)*jetToTauFakeWeight_comb"+"*"+self.vv_stitchingweight(),
					nick="noplot_vv_ff_control"
			)
			add_input(
					input_file=self.files_diboson(channel),
					weight=weight+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["iso_2"], cut_type=cut_type)+"*eventWeight*(gen_match_2 < 6)*jetToTauFakeWeight_comb",
					nick="noplot_vv_ff_control"
			)
			add_input(
					input_file=self.files_data(channel),
					scale_factor=1.0,
					weight=weight+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["iso_2"], cut_type=cut_type)+"*eventWeight*jetToTauFakeWeight_comb",
					nick="noplot_ff_norm"
			)

			add_input(
					input_file=self.files_ztt(channel),
					weight=self.get_weights_ztt(channel=channel,cut_type=cut_type,weight=weight)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["iso_2"], cut_type=cut_type)+"*zPtReweightWeight*(gen_match_2 < 6)*jetToTauFakeWeight_comb",
					nick="noplot_dy_ff_norm"
			)
			add_input(
					input_file=self.files_ttj(channel),
					weight=weight+"*"+self.embedding_ttbarveto_weight(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["iso_2"], cut_type=cut_type)+"*topPtReweightWeight*eventWeight*(gen_match_2 < 6)*jetToTauFakeWeight_comb",
					nick="noplot_tt_ff_norm"
			)
			add_input(
					input_file=self.files_vv(channel),
					weight=weight+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["iso_2"], cut_type=cut_type)+"*eventWeight*(gen_match_2 < 6)*jetToTauFakeWeight_comb"+"*"+self.vv_stitchingweight(),
					nick="noplot_vv_ff_norm"
			)
			add_input(
					input_file=self.files_diboson(channel),
					weight=weight+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["iso_2"], cut_type=cut_type)+"*eventWeight*(gen_match_2 < 6)*jetToTauFakeWeight_comb",
					nick="noplot_vv_ff_norm"
			)
			if not "EstimateFF" in config.get("analysis_modules", []):
				config.setdefault("analysis_modules", []).append("EstimateFF")
			config.setdefault("ff_data_nicks", []).append("ff"+nick_suffix)
			config.setdefault("ff_mc_subtract_nicks", []).append(" ".join([nick+nick_suffix for nick in "noplot_dy_ff_control noplot_tt_ff_control noplot_vv_ff_control".split()]))
			config.setdefault("ff_norm_data_nicks", []).append("noplot_ff_norm"+nick_suffix)
			config.setdefault("ff_norm_mc_subtract_nicks", []).append(" ".join([nick+"_norm"+nick_suffix for nick in "noplot_dy_ff noplot_tt_ff noplot_vv_ff".split()]))

		else:
			log.error("Sample config (FakeFactor) currently not implemented for channel \"%s\"!" % channel)
		Samples._add_plot(config, "bkg", "HIST", "F", "ff", nick_suffix)
		return config


	def ewk(self, config, channel, category, weight, nick_suffix, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", fakefactor_method=None, **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []

		scale_factor = lumi
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("Dibosons", 1.0)

		data_weight, mc_weight = self.projection(kwargs)
		add_input = partialmethod(Samples._add_input, config=config, folder=self.root_file_folder(channel), scale_factor=lumi, nick_suffix=nick_suffix)

		if channel in ["mt", "et"]:
			add_input(
					input_file=self.files_ttj(channel) + " " + self.files_diboson(channel),
					folder=self.root_file_folder(channel),
					weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type),
					nick="ewk"
			)
			add_input(
					input_file=self.files_wj(channel),
					weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+self.wj_stitchingweight(),
					nick="ewk"
			)
			add_input(
					input_file=self.files_vv(channel),
					weight=mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+self.vv_stitchingweight(),
					nick="ewk"
			)
		else:
			log.error("Sample config (EWK) currently not implemented for channel \"%s\"!" % channel)
		
		if channel in ["mt", "et"] and fakefactor_method == "standard":
			config["weights"][config["nicks"].index("ewk")] = config["weights"][config["nicks"].index("ewk")]+"*(gen_match_2 != 6)"
		if channel in ["mt", "et"] and fakefactor_method == "comparison":
			config["weights"][config["nicks"].index("ewk")] = config["weights"][config["nicks"].index("ewk")]+"*(gen_match_2 == 6)"
		
		Samples._add_plot(config, "bkg", "HIST", "F", "ewk", nick_suffix)
		return config
