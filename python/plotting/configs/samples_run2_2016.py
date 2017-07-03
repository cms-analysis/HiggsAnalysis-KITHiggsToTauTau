
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import copy
import sys
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.samples as samples
from Kappa.Skimming.registerDatasetHelper import get_nick_list
from Artus.Utility.tools import make_multiplication, split_multiplication, clean_multiplication
energy = 13
default_lumi =  35.87*1000.0
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
		return "!"+Samples.ttt_genmatch(channel,kwargs)

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
			return "(gen_match_1 < 6 && gen_match_2 < 6 && !(gen_match_1 == 5 && gen_match_2 == 5))"
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
			return "((gen_match_1 < 6 && gen_match_2 < 6 && !(gen_match_1 == 5 && gen_match_2 == 5)) || gen_match_2 == 6 || gen_match_1 == 6)"
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
				return "!((gen_match_1 == 4) && (gen_match_2 == 5))"
			elif channel == "et":
				return "!((gen_match_1 == 3) && (gen_match_2 == 5))"
			elif channel == "tt":
				return "!((gen_match_1 == 5) && (gen_match_2 == 5))"
			elif channel == "em":
				return "!((gen_match_1 == 3) && (gen_match_2 == 4))"
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
		return"(4.200367267668e-6)/(numberGeneratedEventsWeight*crossSectionPerEventWeight)"

	def ewkwp_stitchingweight(self):
		return"(5.190747826298e-6)/(numberGeneratedEventsWeight*crossSectionPerEventWeight)"
	
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
			return "("+self.zl_genmatch(channel)+"*"+self.zl_shape_weight(channel, cut_type)+" + "+self.zj_genmatch(channel)+")"
		else:
			return "(1.0)"
	
	# decay mode reweighting (currently no default reweighting but only used as workaround for shape systematics)
	def decay_mode_reweight(self, channel):
		if channel in ["et", "mt"]:
			return "(((decayMode_2 == 0)*1.0) + ((decayMode_2 == 1 || decayMode_2 == 2)*1.0) + ((decayMode_2 == 10)*1.0))"
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
		if channel in ['gen']:
			Samples._add_input(
					config,
					self.files_ztt(channel),
					self.root_file_folder(channel),
					lumi,
					Samples.ztt_genchannelmatch(channel, category)+"*"+self.get_weights_ztt(channel=channel,cut_type=cut_type,weight=weight)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type),
					"ztt",
					nick_suffix=nick_suffix
		)
		elif channel in ["mt", "et", "tt", "em", "mm", "ee", "ttbar"]:
			Samples._add_input(
					config,
					self.files_ztt(channel),
					self.root_file_folder(channel),
					lumi,
					Samples.ztt_genmatch(channel)+"*"+self.get_weights_ztt(channel=channel,cut_type=cut_type,weight=weight)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*zPtReweightWeight"+"*"+self.decay_mode_reweight(channel)+"*"+zmm_cr_factor,
					"ztt",
					nick_suffix=nick_suffix
			)
			if not (kwargs.get("no_ewk_samples", False) or kwargs.get("no_ewkz_as_dy", False)):
				Samples._add_input(
						config,
						self.files_ewkz_zll(channel),
						self.root_file_folder(channel),
						lumi,
						Samples.ztt_genmatch(channel)+"*"+self.get_weights_ztt(channel=channel,cut_type=cut_type,weight=weight,doStitching=False)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+self.decay_mode_reweight(channel)+"*"+self.ewkz_zll_stitchingweight()+"*"+zmm_cr_factor,
						"ztt",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						self.files_ewkz_znn(channel),
						self.root_file_folder(channel),
						lumi,
						Samples.ztt_genmatch(channel)+"*"+self.get_weights_ztt(channel=channel,cut_type=cut_type,weight=weight,doStitching=False)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+self.decay_mode_reweight(channel)+"*"+self.ewkz_znn_stitchingweight()+"*"+zmm_cr_factor,
						"ztt",
						nick_suffix=nick_suffix
				)
		else:
			log.error("Sample config (ZTT) currently not implemented for channel \"%s\"!" % channel)
		if not kwargs.get("mssm", False):
			Samples._add_bin_corrections(config, "ztt", nick_suffix)
		
		if not kwargs.get("no_plot", False):
			Samples._add_plot(config, "bkg", "HIST", "F", kwargs.get("color_label_key", "ztt"), nick_suffix)

		return config

	def zttpospol(self, config, channel, category, weight, nick_suffix, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", **kwargs):
		polarisation_weight = "tauSpinnerPolarisation>=0.0"
		config = self.ztt(config, channel, category, "(%s)*(%s)" % (polarisation_weight, weight), "pospol"+nick_suffix, lumi=lumi, exclude_cuts=exclude_cuts, cut_type=cut_type, color_label_key="zttpospol", label="zttpospol", **kwargs)
		
		polarisation_bias_correction = kwargs.get("polarisation_bias_correction", False)
		polarisation_gen_ztt_plots = kwargs.get("polarisation_gen_ztt_plots", False)
		
		if polarisation_bias_correction or polarisation_gen_ztt_plots:
			Samples._add_input(
					config,
					self.files_dy_m50(channel),
					"gen/ntuple",
					1.0,
					"isZTT*(%s)" % polarisation_weight,
					"zttpospol_gen"+("" if polarisation_gen_ztt_plots else "_noplot")+nick_suffix,
					nick_suffix=nick_suffix
			)
		
		if polarisation_bias_correction:
			if not "NormalizeForPolarisation" in config.get("analysis_modules", []):
				config.setdefault("analysis_modules", []).append("NormalizeForPolarisation")
			config.setdefault("ztt_pos_pol_gen_nicks", []).extend(["zttpospol_gen"+("" if polarisation_gen_ztt_plots else "_noplot")+nick_suffix] * 2),
			config.setdefault("ztt_pos_pol_reco_nicks", []).extend(["zttpospol"+nick_suffix, "zttpospol_gen"+("" if polarisation_gen_ztt_plots else "_noplot")+nick_suffix])
		
		if polarisation_gen_ztt_plots:
			Samples._add_plot(config, "bkg", "HIST", "F", "zttpospol", nick_suffix)
		
		return config
	
	def zttnegpol(self, config, channel, category, weight, nick_suffix, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", **kwargs):
		polarisation_weight = "tauSpinnerPolarisation<0.0"
		config = self.ztt(config, channel, category, "(%s)*(%s)" % (polarisation_weight, weight), "negpol"+nick_suffix, lumi=lumi, exclude_cuts=exclude_cuts, cut_type=cut_type, color_label_key="zttnegpol", label="zttnegpol", **kwargs)
		
		polarisation_bias_correction = kwargs.get("polarisation_bias_correction", False)
		polarisation_gen_ztt_plots = kwargs.get("polarisation_gen_ztt_plots", False)
		
		if polarisation_bias_correction or polarisation_gen_ztt_plots:
			Samples._add_input(
					config,
					self.files_dy_m50(channel),
					"gen/ntuple",
					1.0,
					"isZTT*(%s)" % polarisation_weight,
					"zttnegpol_gen"+("" if polarisation_gen_ztt_plots else "_noplot")+nick_suffix,
					nick_suffix=nick_suffix
			)
		
		if polarisation_bias_correction:
			if not "NormalizeForPolarisation" in config.get("analysis_modules", []):
				config.setdefault("analysis_modules", []).append("NormalizeForPolarisation")
			config.setdefault("ztt_neg_pol_gen_nicks", []).extend(["zttnegpol_gen"+("" if polarisation_gen_ztt_plots else "_noplot")+nick_suffix] * 2),
			config.setdefault("ztt_neg_pol_reco_nicks", []).extend(["zttnegpol"+nick_suffix, "zttnegpol_gen"+("" if polarisation_gen_ztt_plots else "_noplot")+nick_suffix])
		
		if polarisation_gen_ztt_plots:
			Samples._add_plot(config, "bkg", "HIST", "F", "zttnegpol", nick_suffix)
		
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

		if channel in ["mt", "et", "tt", "em", "mm", "ee", "ttbar"]:
			Samples._add_input(
					config,
					self.files_zll(channel),
					self.root_file_folder(channel),
					lumi,
					mc_weight+"*"+weight+"*eventWeight*"+self.zll_stitchingweight()+"*"+Samples.zll_genmatch(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*zPtReweightWeight"+"*"+self.zll_zl_shape_weight(channel, cut_type)+"*"+zmm_cr_factor,
					"zll",
					nick_suffix=nick_suffix
			)
			if not (kwargs.get("no_ewk_samples", False) or kwargs.get("no_ewkz_as_dy", False)):
				Samples._add_input(
						config,
						self.files_ewkz_zll(channel),
						self.root_file_folder(channel),
						lumi,
						mc_weight+"*"+weight+"*eventWeight*"+Samples.zll_genmatch(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+self.zll_zl_shape_weight(channel, cut_type)+"*"+self.ewkz_zll_stitchingweight()+"*"+zmm_cr_factor,
						"zll",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						self.files_ewkz_znn(channel),
						self.root_file_folder(channel),
						lumi,
						mc_weight+"*"+weight+"*eventWeight*"+Samples.zll_genmatch(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+self.zll_zl_shape_weight(channel, cut_type)+"*"+self.ewkz_znn_stitchingweight()+"*"+zmm_cr_factor,
						"zll",
						nick_suffix=nick_suffix
				)
		else:
			log.error("Sample config (ZLL) currently not implemented for channel \"%s\"!" % channel)
		if not kwargs.get("mssm", False):
			Samples._add_bin_corrections(config, "zll", nick_suffix)
		
		
		Samples._add_plot(config, "bkg", "HIST", "F", "zll", nick_suffix)
		return config

	def zl(self, config, channel, category, weight, nick_suffix, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []
		
		zmm_cr_factor = kwargs.get("zmm_cr_factor", "(1.0)")

		scale_factor = lumi
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("ZL", 1.0)

		data_weight, mc_weight = self.projection(kwargs)

		if channel in ["mt", "et", "tt"]:
			Samples._add_input(
					config,
					self.files_zll(channel),
					self.root_file_folder(channel),
					lumi,
					mc_weight+"*"+weight+"*eventWeight*"+self.zll_stitchingweight()+"*"+Samples.zl_genmatch(channel)+"*"+Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind"], cut_type=cut_type)+"*zPtReweightWeight"+"*"+self.zl_shape_weight(channel, cut_type)+"*"+zmm_cr_factor,
					"zl",
					nick_suffix=nick_suffix
			)
			if not (kwargs.get("no_ewk_samples", False) or kwargs.get("no_ewkz_as_dy", False)):
				Samples._add_input(
						config,
						self.files_ewkz_zll(channel),
						self.root_file_folder(channel),
						lumi,
						mc_weight+"*"+weight+"*eventWeight*"+Samples.zl_genmatch(channel)+"*"+Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind"], cut_type=cut_type)+"*"+self.zl_shape_weight(channel, cut_type)+"*"+self.ewkz_zll_stitchingweight()+"*"+zmm_cr_factor,
						"zl",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						self.files_ewkz_znn(channel),
						self.root_file_folder(channel),
						lumi,
						mc_weight+"*"+weight+"*eventWeight*"+Samples.zl_genmatch(channel)+"*"+Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind"], cut_type=cut_type)+"*"+self.zl_shape_weight(channel, cut_type)+"*"+self.ewkz_znn_stitchingweight()+"*"+zmm_cr_factor,
						"zl",
						nick_suffix=nick_suffix
				)
		elif channel in ["em", "ttbar"]:
			pass
		else:
			log.error("Sample config (ZL) currently not implemented for channel \"%s\"!" % channel)
		if not kwargs.get("mssm", False):
			Samples._add_bin_corrections(config, "zl", nick_suffix)
		Samples._add_plot(config, "bkg", "HIST", "F", "zl", nick_suffix)
		return config

	def zj(self, config, channel, category, weight, nick_suffix, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []
		
		zmm_cr_factor = kwargs.get("zmm_cr_factor", "(1.0)")

		scale_factor = lumi
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("ZJ", 1.0)

		data_weight, mc_weight = self.projection(kwargs)

		if channel in ["mt", "et", "tt"]:
			Samples._add_input(
					config,
					self.files_zll(channel),
					self.root_file_folder(channel),
					lumi,
					mc_weight+"*"+weight+"*eventWeight*"+self.zll_stitchingweight()+"*"+Samples.zj_genmatch(channel)+"*"+Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind"], cut_type=cut_type)+"*zPtReweightWeight"+"*"+zmm_cr_factor,
					"zj",
					nick_suffix=nick_suffix
			)
			if not (kwargs.get("no_ewk_samples", False) or kwargs.get("no_ewkz_as_dy", False)):
				Samples._add_input(
						config,
						self.files_ewkz_zll(channel),
						self.root_file_folder(channel),
						lumi,
						mc_weight+"*"+weight+"*eventWeight*"+Samples.zj_genmatch(channel)+"*"+Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind"], cut_type=cut_type)+"*"+self.ewkz_zll_stitchingweight()+"*"+zmm_cr_factor,
						"zj",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						self.files_ewkz_znn(channel),
						self.root_file_folder(channel),
						lumi,
						mc_weight+"*"+weight+"*eventWeight*"+Samples.zj_genmatch(channel)+"*"+Samples.cut_string(channel, exclude_cuts=exclude_cuts+["blind"], cut_type=cut_type)+"*"+self.ewkz_znn_stitchingweight()+"*"+zmm_cr_factor,
						"zj",
						nick_suffix=nick_suffix
				)
		elif channel in ["em", "ttbar"]:
			pass
		else:
			log.error("Sample config (ZJ) currently not implemented for channel \"%s\"!" % channel)
		if not kwargs.get("mssm", False):
			Samples._add_bin_corrections(config, "zj", nick_suffix)
		Samples._add_plot(config, "bkg", "HIST", "F", "zj", nick_suffix)
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

		Samples._add_input(
				config,
				self.files_ttj(channel),
				self.root_file_folder(channel),
				lumi,
				mc_weight+"*"+weight+"*eventWeight*"+self.embedding_ttbarveto_weight(channel)+"*"+Samples.ttt_genmatch(channel,kwargs)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*topPtReweightWeight",
				"ttt",
				nick_suffix=nick_suffix
		)
		if channel not in ["et", "mt", "tt"]:
			log.error("Sample config (TTT) currently not implemented for channel \"%s\"!" % channel)
		if not kwargs.get("mssm", False):
			Samples._add_bin_corrections(config, "ttt", nick_suffix)
		
		Samples._add_plot(config, "bkg", "HIST", "F", "ttt", nick_suffix)
		return config

	def ttjj(self, config, channel, category, weight, nick_suffix, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", fakefactor_method=None, **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []

		scale_factor = lumi
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("TTJ", 1.0)

		data_weight, mc_weight = self.projection(kwargs)

		Samples._add_input(
				config,
				self.files_ttj(channel),
				self.root_file_folder(channel),
				lumi,
				mc_weight+"*"+weight+"*eventWeight*"+self.embedding_ttbarveto_weight(channel)+"*"+Samples.ttj_genmatch(channel,kwargs)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*topPtReweightWeight",
				"ttjj",
				nick_suffix=nick_suffix
		)
		if channel not in ["et", "mt", "tt"]:
			log.error("Sample config (TTJ) currently not implemented for channel \"%s\"!" % channel)
		if not kwargs.get("mssm", False):
			Samples._add_bin_corrections(config, "ttjj", nick_suffix)
		
		Samples._add_plot(config, "bkg", "HIST", "F", "ttjj", nick_suffix)
		return config

	def tttautau(self, config, channel, category, weight, nick_suffix, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", estimationMethod="classic", fakefactor_method=None, **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []

		scale_factor = lumi
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("TTTAUTAU", 1.0)
		data_weight, mc_weight = self.projection(kwargs)
		Samples._add_input(
				config,
				self.files_ttj(channel),
				self.root_file_folder(channel),
				lumi,
				make_multiplication([mc_weight, weight, "eventWeight",self.tttautau_genmatch(channel), self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type), "topPtReweightWeight"]),
				"tttautau",
				nick_suffix=nick_suffix
		)
		if channel not in ["em", "et", "mt", "tt", "mm", "ee", "ttbar"]:
			log.error("Sample config (TTTAUTAU) currently not implemented for channel \"%s\"!" % channel)
		if not kwargs.get("mssm", False):
			Samples._add_bin_corrections(config, "tttautau", nick_suffix)		
		Samples._add_plot(config, "bkg", "HIST", "F", "tttautau", nick_suffix)
		return config

	def ttj(self, config, channel, category, weight, nick_suffix, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", estimationMethod="classic", fakefactor_method=None, **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []
		
		zmm_cr_factor = kwargs.get("zmm_cr_factor", "(1.0)")

		scale_factor = lumi
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("TTJ", 1.0)
		data_weight, mc_weight = self.projection(kwargs)
		Samples._add_input(
				config,
				self.files_ttj(channel),
				self.root_file_folder(channel),
				lumi,
				make_multiplication([mc_weight, weight, "eventWeight",self.embedding_ttbarveto_weight(channel), self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type), "topPtReweightWeight"]),
				"ttj",
				nick_suffix=nick_suffix
		)
		if (channel == "em") and ("newKIT" in estimationMethod):
			channel_weight = Samples.get_jetbin(channel, category, weight)
			
			ttbar_data_weight = make_multiplication(["(pZetaMissVis < -70.0)", channel_weight] )   # get data / mc factor from inclusive

			Samples._add_input(
					config,
					self.files_data(channel),
					self.root_file_folder(channel),
					1.0,
					make_multiplication([data_weight, ttbar_data_weight, "eventWeight", self._cut_string(channel, exclude_cuts=exclude_cuts+["pzeta", "nobtag"], cut_type=cut_type) ]),
					"noplot_ttj_data_control",
					nick_suffix=nick_suffix
			)
			Samples._add_input(
					config,
					self.files_ztt(channel),
					self.root_file_folder(channel),
					lumi,
					make_multiplication([Samples.ztt_genmatch(channel), ttbar_data_weight, self.get_weights_ztt(channel=channel,cut_type=cut_type,weight=weight), self._cut_string(channel, exclude_cuts=exclude_cuts+["pzeta", "nobtag"], cut_type=cut_type) ],"zPtReweightWeight", zmm_cr_factor),
					"noplot_ztt_mc_ttj_control",
					nick_suffix=nick_suffix
			)
			if not (kwargs.get("no_ewk_samples", False) or kwargs.get("no_ewkz_as_dy", False)):
				Samples._add_input(
						config,
						self.files_ewkz_zll(channel),
						self.root_file_folder(channel),
						lumi,
						make_multiplication([Samples.ztt_genmatch(channel), ttbar_data_weight, self.get_weights_ztt(channel=channel,cut_type=cut_type,weight=weight,doStitching=False), self._cut_string(channel, exclude_cuts=exclude_cuts+["pzeta", "nobtag"], cut_type=cut_type), zmm_cr_factor, self.ewkz_zll_stitchingweight()]),
						"noplot_ztt_mc_ttj_control",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						self.files_ewkz_znn(channel),
						self.root_file_folder(channel),
						lumi,
						make_multiplication([Samples.ztt_genmatch(channel), ttbar_data_weight, self.get_weights_ztt(channel=channel,cut_type=cut_type,weight=weight,doStitching=False), self._cut_string(channel, exclude_cuts=exclude_cuts+["pzeta", "nobtag"], cut_type=cut_type), zmm_cr_factor, self.ewkz_znn_stitchingweight()]),
						"noplot_ztt_mc_ttj_control",
						nick_suffix=nick_suffix
				)
			Samples._add_input(
					config,
					self.files_zll(channel),
					self.root_file_folder(channel),
					lumi,
					make_multiplication([mc_weight, ttbar_data_weight, "eventWeight", self.zll_stitchingweight(), Samples.zll_genmatch(channel), self._cut_string(channel, exclude_cuts=exclude_cuts+["pzeta", "nobtag"], cut_type=cut_type)],"zPtReweightWeight",self.zll_zl_shape_weight(channel, cut_type), zmm_cr_factor),
					"noplot_zll_ttj_control",
					nick_suffix=nick_suffix
			)
			if not (kwargs.get("no_ewk_samples", False) or kwargs.get("no_ewkz_as_dy", False)):
				Samples._add_input(
						config,
						self.files_ewkz_zll(channel),
						self.root_file_folder(channel),
						lumi,
						make_multiplication([mc_weight, ttbar_data_weight, "eventWeight", Samples.zll_genmatch(channel), self._cut_string(channel, exclude_cuts=exclude_cuts+["pzeta", "nobtag"], cut_type=cut_type)],self.zll_zl_shape_weight(channel, cut_type), zmm_cr_factor, self.ewkz_zll_stitchingweight()),
						"noplot_zll_ttj_control",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						self.files_ewkz_znn(channel),
						self.root_file_folder(channel),
						lumi,
						make_multiplication([mc_weight, ttbar_data_weight, "eventWeight", Samples.zll_genmatch(channel), self._cut_string(channel, exclude_cuts=exclude_cuts+["pzeta", "nobtag"], cut_type=cut_type)],self.zll_zl_shape_weight(channel, cut_type), zmm_cr_factor, self.ewkz_znn_stitchingweight()),
						"noplot_zll_ttj_control",
						nick_suffix=nick_suffix
				)
			if not kwargs.get("no_ewk_samples", False) and kwargs.get("no_ewkz_as_dy", False):
				Samples._add_input(
						config,
						self.files_ewkz_zll(channel),
						self.root_file_folder(channel),
						lumi,
						make_multiplication([mc_weight, ttbar_data_weight, "eventWeight", self._cut_string(channel, exclude_cuts=exclude_cuts+["pzeta", "nobtag"], cut_type=cut_type)], zmm_cr_factor, self.ewkz_zll_stitchingweight()),
						"noplot_ewkz_ttj_control",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						self.files_ewkz_znn(channel),
						self.root_file_folder(channel),
						lumi,
						make_multiplication([mc_weight, ttbar_data_weight, "eventWeight", self._cut_string(channel, exclude_cuts=exclude_cuts+["pzeta", "nobtag"], cut_type=cut_type)], zmm_cr_factor, self.ewkz_znn_stitchingweight()),
						"noplot_ewkz_ttj_control",
						nick_suffix=nick_suffix
				)
			Samples._add_input(
					config,
					self.files_wj(channel),
					self.root_file_folder(channel),
					lumi,
					make_multiplication([mc_weight, ttbar_data_weight, "eventWeight", self._cut_string(channel, exclude_cuts=exclude_cuts+["pzeta", "nobtag"], cut_type=cut_type)]),
					"noplot_wj_ttj_control",
					nick_suffix=nick_suffix
			)
			Samples._add_input(
					config,
					self.files_vv(channel),
					self.root_file_folder(channel),
					lumi,
					make_multiplication([mc_weight, ttbar_data_weight, "eventWeight", self._cut_string(channel, exclude_cuts=exclude_cuts+["pzeta", "nobtag"], cut_type=cut_type)]),
					"noplot_vv_ttj_control",
					nick_suffix=nick_suffix
			)
			Samples._add_input(
					config,
					self.files_ttj(channel),
					self.root_file_folder(channel),
					lumi,
					make_multiplication([mc_weight, weight, "eventWeight",self.embedding_ttbarveto_weight(channel), self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type), "topPtReweightWeight"]),
					"noplot_ttj_mc_signal",
					nick_suffix=nick_suffix
			)
			Samples._add_input(
					config,
					self.files_ttj(channel),
					self.root_file_folder(channel),
					lumi,
					make_multiplication([mc_weight, ttbar_data_weight, "eventWeight",self.embedding_ttbarveto_weight(channel), self._cut_string(channel, exclude_cuts=exclude_cuts+["pzeta", "nobtag"], cut_type=cut_type)+"*topPtReweightWeight"]),
					"noplot_ttj_mc_control",
					nick_suffix=nick_suffix
			)
			if not "EstimateTtbar" in config.get("analysis_modules", []):
				config.setdefault("analysis_modules", []).append("EstimateTtbar")
			config.setdefault("ttbar_shape_nicks", []).append("ttj"+nick_suffix)
			config.setdefault("ttbar_data_control_nicks", []).append("noplot_ttj_data_control"+nick_suffix)
			if not kwargs.get("no_ewk_samples", False) and kwargs.get("no_ewkz_as_dy", False):
				config.setdefault("ttbar_data_subtract_nicks", []).append(" ".join([nick+nick_suffix for nick in "noplot_ztt_mc_ttj_control noplot_zll_ttj_control noplot_ewkz_ttj_control noplot_wj_ttj_control noplot_vv_ttj_control".split()]))
			else:
				config.setdefault("ttbar_data_subtract_nicks", []).append(" ".join([nick+nick_suffix for nick in "noplot_ztt_mc_ttj_control noplot_zll_ttj_control noplot_wj_ttj_control noplot_vv_ttj_control".split()]))
			config.setdefault("ttbar_mc_signal_nicks", []).append("noplot_ttj_mc_signal"+nick_suffix)
			config.setdefault("ttbar_mc_control_nicks", []).append("noplot_ttj_mc_control"+nick_suffix)
		if channel not in ["em", "et", "mt", "tt", "mm", "ee", "ttbar"]:
			log.error("Sample config (TTJ) currently not implemented for channel \"%s\"!" % channel)
		if not kwargs.get("mssm", False):
			Samples._add_bin_corrections(config, "ttj", nick_suffix)
		
		
		Samples._add_plot(config, "bkg", "HIST", "F", "ttj", nick_suffix)
		return config

	def files_vv(self, config):
		artus_files = self.artus_file_names({ "process" : 
		                                      "(WWTo1L1Nu2Q|"
		                                    + "WZTo1L1Nu2Q|"
		                                    + "WZTo1L3Nu|"
		                                    + "WZTo2L2Q|" 
		                                    + "ZZTo2L2Q"
		                                    +  ")",
		                      "extension" : "",
		                      "data" : False, "campaign" : self.mc_campaign, "generator" : "amcatnlo-pythia8"}, 5)

		artus_files = artus_files + " " + self.artus_file_names({ "process" : "VVTo2L2Nu|ZZTo4L", "extension" : "ext1",
		                      "data" : False, "campaign" : self.mc_campaign, "generator" : "amcatnlo-pythia8"}, 2)

		artus_files = artus_files + " " + self.artus_file_names({ "process" : "WZJToLLLNu",
		                      "data" : False, "campaign" : self.mc_campaign, "generator" : "pythia8"}, 1)

		artus_files = artus_files + " " + self.artus_file_names({ "process" : "(STt-channelantitop4finclusiveDecays|STt-channeltop4finclusiveDecays|STtWantitop5finclusiveDecays|STtWtop5finclusiveDecays)",
		                      "data" : False, "campaign" : self.mc_campaign}, 4)
		return artus_files

	def files_hww_gg(self, channel, mass=125):
		return self.artus_file_names({"process" : "GluGluHToWWTo2L2Nu_M"+str(mass), "data": False, "campaign" : self.mc_campaign}, 1)
	
	def hww_gg(self, config, channel, category, weight, nick_suffix, higgs_masses, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []
		
		data_weight, mc_weight = self.projection(kwargs)
		
		for mass in higgs_masses:
			if channel in ["mt", "et", "em", "tt", "mm", "ee", "ttbar"]:
				Samples._add_input(
					config,
					self.files_hww_gg(channel, mass),
					self.root_file_folder(channel),
					lumi,
					mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type),
					"hww_gg"+str(mass),
					nick_suffix=nick_suffix
				)
			else:
				log.error("Sample config (HWW_gg) currently not implemented for channel \"%s\"!" % channel)
			if not kwargs.get("mssm", False):
				Samples._add_bin_corrections(config, "hww_gg"+str(mass), nick_suffix)
		
			Samples._add_plot(config, "bkg", "HIST", "F", "hww_gg"+str(mass), nick_suffix)
		
		return config

	def hww_gg125(self, config, channel, category, weight, nick_suffix, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []
		
		data_weight, mc_weight = self.projection(kwargs)
		
		if channel in ["mt", "et", "em", "tt", "mm", "ee", "ttbar"]:
			Samples._add_input(
				config,
				self.files_hww_gg(channel, 125),
				self.root_file_folder(channel),
				lumi,
				mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type),
				"hww_gg125",
				nick_suffix=nick_suffix
			)
		else:
			log.error("Sample config (HWW_gg125) currently not implemented for channel \"%s\"!" % channel)
		if not kwargs.get("mssm", False):
			Samples._add_bin_corrections(config, "hww_gg125", nick_suffix)
		
		Samples._add_plot(config, "bkg", "HIST", "F", "hww_gg125", nick_suffix)
		
		return config

	def files_hww_qq(self, channel, mass=125):
		return self.artus_file_names({"process" : "VBFHToWWTo2L2Nu_M"+str(mass), "data": False, "campaign" : self.mc_campaign}, 1)

	def hww_qq(self, config, channel, category, weight, nick_suffix, higgs_masses, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []
		
		data_weight, mc_weight = self.projection(kwargs)
		
		for mass in higgs_masses:
			if channel in ["mt", "et", "em", "tt", "mm", "ee", "ttbar"]:
				Samples._add_input(
					config,
					self.files_hww_qq(channel, mass),
					self.root_file_folder(channel),
					lumi,
					mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type),
					"hww_qq"+str(mass),
					nick_suffix=nick_suffix
				)
			else:
				log.error("Sample config (HWW_qq) currently not implemented for channel \"%s\"!" % channel)
			if not kwargs.get("mssm", False):
				Samples._add_bin_corrections(config, "hww_qq"+str(mass), nick_suffix)
			
			Samples._add_plot(config, "bkg", "HIST", "F", "hww_qq"+str(mass), nick_suffix)
		
		return config

	def hww_qq125(self, config, channel, category, weight, nick_suffix, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []
		
		data_weight, mc_weight = self.projection(kwargs)
		
		if channel in ["mt", "et", "em", "tt", "mm", "ee", "ttbar"]:
			Samples._add_input(
				config,
				self.files_hww_qq(channel, 125),
				self.root_file_folder(channel),
				lumi,
				mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type),
				"hww_qq125",
				nick_suffix=nick_suffix
			)
		else:
			log.error("Sample config (HWW_qq125) currently not implemented for channel \"%s\"!" % channel)
		if not kwargs.get("mssm", False):
			Samples._add_bin_corrections(config, "hww_qq125", nick_suffix)
		
		Samples._add_plot(config, "bkg", "HIST", "F", "hww_qq125", nick_suffix)
		
		return config

	def hww(self, config, channel, category, weight, nick_suffix, higgs_masses, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []

		data_weight, mc_weight = self.projection(kwargs)

		for mass in higgs_masses:
			if channel == "em" or channel == "ttbar":
				Samples._add_input(
					config,
					self.files_hww_gg(channel, mass),
					self.root_file_folder(channel),
					lumi,
					mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type),
					"hww"+str(mass),
					nick_suffix=nick_suffix
				)
				Samples._add_input(
					config,
					self.files_hww_qq(channel, mass),
					self.root_file_folder(channel),
					lumi,
					mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type),
					"hww"+str(mass),
					nick_suffix=nick_suffix
				)
			else:
				log.error("Sample config (HWW) currently not implemented for channel \"%s\"!" % channel)
			if not kwargs.get("mssm", False):
				Samples._add_bin_corrections(config, "hww"+str(mass), nick_suffix)

			Samples._add_plot(config, "bkg", "HIST", "F", "hww"+str(mass), nick_suffix)
		return config

	def vvt(self, config, channel, category, weight, nick_suffix, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", fakefactor_method=None, **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []

		scale_factor = lumi
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("Dibosons", 1.0)

		data_weight, mc_weight = self.projection(kwargs)

		if channel in ["mt", "et", "tt"]:
			Samples._add_input(
					config,
					self.files_vv(channel),
					self.root_file_folder(channel),
					lumi,
					mc_weight+"*"+weight+"*eventWeight*"+Samples.ttt_genmatch(channel,kwargs)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type),
					"vvt",
					nick_suffix=nick_suffix
			)
		else:
			log.error("Sample config (VVT) currently not implemented for channel \"%s\"!" % channel)
		if not kwargs.get("mssm", False):
			Samples._add_bin_corrections(config, "vvt", nick_suffix)
		
		Samples._add_plot(config, "bkg", "HIST", "F", "vvt", nick_suffix)
		return config

	def vvj(self, config, channel, category, weight, nick_suffix, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", fakefactor_method=None, **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []

		scale_factor = lumi
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("Dibosons", 1.0)

		data_weight, mc_weight = self.projection(kwargs)

		if channel in ["mt", "et", "tt"]:
			Samples._add_input(
					config,
					self.files_vv(channel),
					self.root_file_folder(channel),
					lumi,
					mc_weight+"*"+weight+"*eventWeight*"+Samples.ttj_genmatch(channel,kwargs)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type),
					"vvj",
					nick_suffix=nick_suffix
			)
		else:
			log.error("Sample config (VVJ) currently not implemented for channel \"%s\"!" % channel)
		if not kwargs.get("mssm", False):
			Samples._add_bin_corrections(config, "vvj", nick_suffix)
		
		Samples._add_plot(config, "bkg", "HIST", "F", "vvj", nick_suffix)
		return config

	def vv(self, config, channel, category, weight, nick_suffix, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", fakefactor_method=None, **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []

		scale_factor = lumi
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("Dibosons", 1.0)

		data_weight, mc_weight = self.projection(kwargs)

		if channel in ["mt", "et", "em", "tt", "mm", "ee", "ttbar"]:
			Samples._add_input(
					config,
					self.files_vv(channel),
					self.root_file_folder(channel),
					lumi,
					mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type),
					"vv",
					nick_suffix=nick_suffix
			)
		else:
			log.error("Sample config (VV) currently not implemented for channel \"%s\"!" % channel)
		if not kwargs.get("mssm", False):
			Samples._add_bin_corrections(config, "vv", nick_suffix)
		
		
		Samples._add_plot(config, "bkg", "HIST", "F", "vv", nick_suffix)
		return config

	def files_wj(self, channel):
		artus_files = self.artus_file_names({"process" : "W.*JetsToLNu", "data" : False, "campaign" : self.mc_campaign, "generator" : "madgraph-pythia8"}, 10)
		return artus_files
	
	def files_wgamma(self, channel):
		artus_files = self.artus_file_names({"process" : "WGToLNuG", "data" : False, "campaign" : self.mc_campaign, "generator" : "amcatnlo-pythia8", "extension" : "ext3"}, 1)
		artus_files = artus_files + " " + self.artus_file_names({"process" : "WGstarToLNuEE|WGstarToLNuMuMu", "data" : False, "campaign" : self.mc_campaign, "generator" : "madgraph"}, 2)
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

		if channel in ["mt", "et", "em", "tt", "mm", "ee", "ttbar"]:
			Samples._add_input(
					config,
					self.files_ewkz_zll(channel),
					self.root_file_folder(channel),
					lumi,
					mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+zmm_cr_factor+"*"+self.ewkz_zll_stitchingweight(),
					"ewkz",
					nick_suffix=nick_suffix
			)
			Samples._add_input(
					config,
					self.files_ewkz_znn(channel),
					self.root_file_folder(channel),
					lumi,
					mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+zmm_cr_factor+"*"+self.ewkz_znn_stitchingweight(),
					"ewkz",
					nick_suffix=nick_suffix
			)
		else:
			log.error("Sample config (EWKZ) currently not implemented for channel \"%s\"!" % channel)
		if not kwargs.get("mssm", False):
			Samples._add_bin_corrections(config, "ewkz", nick_suffix)
		
		
		Samples._add_plot(config, "bkg", "HIST", "F", "ewkz", nick_suffix)
		return config

	def wj(self, config, channel, category, weight, nick_suffix, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", fakefactor_method=None, estimationMethod="classic", controlregions=False,**kwargs):
		if exclude_cuts is None:
			exclude_cuts = []
		
		zmm_cr_factor = kwargs.get("zmm_cr_factor", "(1.0)")

		scale_factor = lumi
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("WJets", 1.0)

		data_weight, mc_weight = self.projection(kwargs)

		if channel in ["mt", "et"]:
			high_mt_cut_type = cut_type + "highMtControlRegionWJ"
			high_mt_ss_cut_type = cut_type + "highMtSSControlRegionWJ"
			wj_shape_cut_type = cut_type
			wj_highmt_shape_cut_type = high_mt_cut_type
			
			exclude_cuts_high_mt = [cut for cut in exclude_cuts if cut not in ["mt"]]
			exclude_cuts_high_mt_ss = copy.deepcopy(exclude_cuts_high_mt)+["os"]
			exclude_cuts_inclusive = copy.deepcopy(exclude_cuts)+["mt"]
			exclude_cuts_inclusive_ss = copy.deepcopy(exclude_cuts_inclusive)+["os"]
			exclude_cuts_relaxed = []
			
			if category != None:
				wj_highmt_shape_cut_type = wj_highmt_shape_cut_type + ("relaxedETauMuTauWJ" if ("1jet" in category or "vbf" in category or "Boosted2D" in category or "Vbf2D" in category) else "")
				wj_shape_cut_type = wj_shape_cut_type + ("relaxedETauMuTauWJ" if ("1jet" in category or "vbf" in category or "Boosted2D" in category or "Vbf2D" in category) else "")
				exclude_cuts_relaxed = ["iso_1", "iso_2"] if ("1jet" in category or "vbf" in category or "Boosted2D" in category or "Vbf2D" in category) else []
			
			# wj shape and highmt to lowmt extrapolation
			wj_shape_weight = weight   # replace only category part
			if "newKIT" in estimationMethod:
				wj_shape_weight = make_multiplication(Samples.get_jetbin(category, channel, weight))
			
			if "new" in estimationMethod:
				wj_weight = weight
				if "newKIT" in estimationMethod:
					wj_weight = split_multiplication(weight)[-1] # remove category selection for yield estimation
		
				# noplot_xx_os_highmt: for the w+jets os high-mt yield
				Samples._add_input(
						config,
						self.files_ztt(channel),
						self.root_file_folder(channel),
						lumi,
						Samples.ztt_genmatch(channel)+"*"+self.get_weights_ztt(channel=channel,cut_type=cut_type,weight=wj_weight)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_high_mt, cut_type=high_mt_cut_type)+"*zPtReweightWeight"+"*"+zmm_cr_factor,
						("noplot_" if not controlregions else "") + "ztt_os_highmt",
						nick_suffix=nick_suffix
				)
				if not (kwargs.get("no_ewk_samples", False) or kwargs.get("no_ewkz_as_dy", False)):
					Samples._add_input(
							config,
							self.files_ewkz_zll(channel),
							self.root_file_folder(channel),
							lumi,
							Samples.ztt_genmatch(channel)+"*"+self.get_weights_ztt(channel=channel,cut_type=cut_type,weight=wj_weight,doStitching=False)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_high_mt, cut_type=high_mt_cut_type)+"*"+self.ewkz_zll_stitchingweight()+"*"+zmm_cr_factor,
							("noplot_" if not controlregions else "") + "ztt_os_highmt",
							nick_suffix=nick_suffix
					)
					Samples._add_input(
							config,
							self.files_ewkz_znn(channel),
							self.root_file_folder(channel),
							lumi,
							Samples.ztt_genmatch(channel)+"*"+self.get_weights_ztt(channel=channel,cut_type=cut_type,weight=wj_weight,doStitching=False)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_high_mt, cut_type=high_mt_cut_type)+"*"+self.ewkz_znn_stitchingweight()+"*"+zmm_cr_factor,
							("noplot_" if not controlregions else "") + "ztt_os_highmt",
							nick_suffix=nick_suffix
					)
				Samples._add_input(
						config,
						self.files_zll(channel),
						self.root_file_folder(channel),
						lumi,
						mc_weight+"*"+wj_weight+"*eventWeight*"+self.zll_stitchingweight()+"*"+Samples.zll_genmatch(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_high_mt, cut_type=high_mt_cut_type)+"*zPtReweightWeight"+"*"+self.zll_zl_shape_weight(channel, cut_type)+"*"+zmm_cr_factor,
						("noplot_" if not controlregions else "") + "zll_os_highmt",
						nick_suffix=nick_suffix
				)
				if not (kwargs.get("no_ewk_samples", False) or kwargs.get("no_ewkz_as_dy", False)):
					Samples._add_input(
							config,
							self.files_ewkz_zll(channel),
							self.root_file_folder(channel),
							lumi,
							mc_weight+"*"+wj_weight+"*eventWeight*"+Samples.zll_genmatch(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_high_mt, cut_type=high_mt_cut_type)+"*"+self.zll_zl_shape_weight(channel, cut_type)+"*"+self.ewkz_zll_stitchingweight()+"*"+zmm_cr_factor,
							("noplot_" if not controlregions else "") + "zll_os_highmt",
							nick_suffix=nick_suffix
					)
					Samples._add_input(
							config,
							self.files_ewkz_znn(channel),
							self.root_file_folder(channel),
							lumi,
							mc_weight+"*"+wj_weight+"*eventWeight*"+Samples.zll_genmatch(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_high_mt, cut_type=high_mt_cut_type)+"*"+self.zll_zl_shape_weight(channel, cut_type)+"*"+self.ewkz_znn_stitchingweight()+"*"+zmm_cr_factor,
							("noplot_" if not controlregions else "") + "zll_os_highmt",
							nick_suffix=nick_suffix
					)
				Samples._add_input(
						config,
						self.files_zll(channel),
						self.root_file_folder(channel),
						lumi,
						mc_weight+"*"+wj_weight+"*eventWeight*"+self.zll_stitchingweight()+"*"+Samples.zl_genmatch(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_high_mt, cut_type=high_mt_cut_type)+"*zPtReweightWeight"+"*"+self.zl_shape_weight(channel, cut_type)+"*"+zmm_cr_factor,
						("noplot_" if not controlregions else "") + "zl_os_highmt",
						nick_suffix=nick_suffix
				)
				if not (kwargs.get("no_ewk_samples", False) or kwargs.get("no_ewkz_as_dy", False)):
					Samples._add_input(
							config,
							self.files_ewkz_zll(channel),
							self.root_file_folder(channel),
							lumi,
							mc_weight+"*"+wj_weight+"*eventWeight*"+Samples.zl_genmatch(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_high_mt, cut_type=high_mt_cut_type)+"*"+self.zl_shape_weight(channel, cut_type)+"*"+self.ewkz_zll_stitchingweight()+"*"+zmm_cr_factor,
							("noplot_" if not controlregions else "") + "zl_os_highmt",
							nick_suffix=nick_suffix
					)
					Samples._add_input(
							config,
							self.files_ewkz_znn(channel),
							self.root_file_folder(channel),
							lumi,
							mc_weight+"*"+wj_weight+"*eventWeight*"+Samples.zl_genmatch(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_high_mt, cut_type=high_mt_cut_type)+"*"+self.zl_shape_weight(channel, cut_type)+"*"+self.ewkz_znn_stitchingweight()+"*"+zmm_cr_factor,
							("noplot_" if not controlregions else "") + "zl_os_highmt",
							nick_suffix=nick_suffix
					)
				Samples._add_input(
						config,
						self.files_zll(channel),
						self.root_file_folder(channel),
						lumi,
						mc_weight+"*"+wj_weight+"*eventWeight*"+self.zll_stitchingweight()+"*"+Samples.zj_genmatch(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_high_mt, cut_type=high_mt_cut_type)+"*zPtReweightWeight"+"*"+zmm_cr_factor,
						("noplot_" if not controlregions else "") + "zj_os_highmt",
						nick_suffix=nick_suffix
				)
				if not (kwargs.get("no_ewk_samples", False) or kwargs.get("no_ewkz_as_dy", False)):
					Samples._add_input(
							config,
							self.files_ewkz_zll(channel),
							self.root_file_folder(channel),
							lumi,
							mc_weight+"*"+wj_weight+"*eventWeight*"+Samples.zj_genmatch(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_high_mt, cut_type=high_mt_cut_type)+"*"+self.ewkz_zll_stitchingweight()+"*"+zmm_cr_factor,
							("noplot_" if not controlregions else "") + "zj_os_highmt",
							nick_suffix=nick_suffix
					)
					Samples._add_input(
							config,
							self.files_ewkz_znn(channel),
							self.root_file_folder(channel),
							lumi,
							mc_weight+"*"+wj_weight+"*eventWeight*"+Samples.zj_genmatch(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_high_mt, cut_type=high_mt_cut_type)+"*"+self.ewkz_znn_stitchingweight()+"*"+zmm_cr_factor,
							("noplot_" if not controlregions else "") + "zj_os_highmt",
							nick_suffix=nick_suffix
					)
				if not kwargs.get("no_ewk_samples", False) and kwargs.get("no_ewkz_as_dy", False):
					Samples._add_input(
							config,
							self.files_ewkz_zll(channel),
							self.root_file_folder(channel),
							lumi,
							mc_weight+"*"+wj_weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_high_mt, cut_type=high_mt_cut_type)+"*"+self.ewkz_zll_stitchingweight()+"*"+zmm_cr_factor,
							("noplot_" if not controlregions else "") + "ewkz_os_highmt",
							nick_suffix=nick_suffix
					)
					Samples._add_input(
							config,
							self.files_ewkz_znn(channel),
							self.root_file_folder(channel),
							lumi,
							mc_weight+"*"+wj_weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_high_mt, cut_type=high_mt_cut_type)+"*"+self.ewkz_znn_stitchingweight()+"*"+zmm_cr_factor,
							("noplot_" if not controlregions else "") + "ewkz_os_highmt",
							nick_suffix=nick_suffix
					)
				Samples._add_input(
						config,
						self.files_ttj(channel),
						self.root_file_folder(channel),
						lumi,
						mc_weight+"*"+wj_weight+"*eventWeight*"+self.embedding_ttbarveto_weight(channel)+"*"+Samples.ttt_genmatch(channel,kwargs)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_high_mt, cut_type=high_mt_cut_type)+"*topPtReweightWeight",
						("noplot_" if not controlregions else "") + "ttt_os_highmt",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						self.files_ttj(channel),
						self.root_file_folder(channel),
						lumi,
						mc_weight+"*"+wj_weight+"*eventWeight*"+self.embedding_ttbarveto_weight(channel)+"*"+Samples.ttj_genmatch(channel,kwargs)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_high_mt, cut_type=high_mt_cut_type)+"*topPtReweightWeight",
						("noplot_" if not controlregions else "") + "ttjj_os_highmt",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						self.files_ttj(channel),
						self.root_file_folder(channel),
						lumi,
						mc_weight+"*"+wj_weight+"*eventWeight*"+self.embedding_ttbarveto_weight(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_high_mt, cut_type=high_mt_cut_type)+"*topPtReweightWeight",
						("noplot_" if not controlregions else "") + "ttj_os_highmt",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						self.files_vv(channel),
						self.root_file_folder(channel),
						lumi,
						mc_weight+"*"+wj_weight+"*eventWeight*"+Samples.ttt_genmatch(channel,kwargs)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_high_mt, cut_type=high_mt_cut_type),
						("noplot_" if not controlregions else "") + "vvt_os_highmt",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						self.files_vv(channel),
						self.root_file_folder(channel),
						lumi,
						mc_weight+"*"+wj_weight+"*eventWeight*"+Samples.ttj_genmatch(channel,kwargs)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_high_mt, cut_type=high_mt_cut_type),
						("noplot_" if not controlregions else "") + "vvj_os_highmt",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						self.files_vv(channel),
						self.root_file_folder(channel),
						lumi,
						mc_weight+"*"+wj_weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_high_mt, cut_type=high_mt_cut_type),
						("noplot_" if not controlregions else "") + "vv_os_highmt",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						self.files_data(channel),
						self.root_file_folder(channel),
						1.0,
						data_weight+"*"+wj_weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_high_mt, cut_type=high_mt_cut_type),
						("noplot_" if not controlregions else "") + "data_os_highmt",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						self.files_wj(channel),
						self.root_file_folder(channel),
						lumi,
						mc_weight+"*"+wj_weight+"*eventWeight*"+self.wj_stitchingweight()+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_high_mt, cut_type=high_mt_cut_type),
						("noplot_" if not controlregions else "") + "wj_os_highmt",
						nick_suffix=nick_suffix
				)
				if (not kwargs.get("no_ewk_samples", False)):
					Samples._add_input(
							config,
							self.files_ewkwm(channel),
							self.root_file_folder(channel),
							lumi,
							mc_weight+"*"+wj_weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_high_mt, cut_type=high_mt_cut_type)+"*"+self.ewkwm_stitchingweight(),
							("noplot_" if not controlregions else "") + "wj_os_highmt",
							nick_suffix=nick_suffix
					)
					Samples._add_input(
							config,
							self.files_ewkwp(channel),
							self.root_file_folder(channel),
							lumi,
							mc_weight+"*"+wj_weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_high_mt, cut_type=high_mt_cut_type)+"*"+self.ewkwp_stitchingweight(),
							("noplot_" if not controlregions else "") + "wj_os_highmt",
							nick_suffix=nick_suffix
					)
				# noplot_xx_ss_highmt: for the w+jets ss high-mt yield
				Samples._add_input(
						config,
						self.files_ztt(channel),
						self.root_file_folder(channel),
						lumi,
						Samples.ztt_genmatch(channel)+"*"+self.get_weights_ztt(channel=channel,cut_type=cut_type,weight=wj_weight)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_high_mt_ss, cut_type=high_mt_ss_cut_type)+"*zPtReweightWeight"+"*"+zmm_cr_factor,
						("noplot_" if not controlregions else "") + "ztt_ss_highmt",
						nick_suffix=nick_suffix
				)
				if not (kwargs.get("no_ewk_samples", False) or kwargs.get("no_ewkz_as_dy", False)):
					Samples._add_input(
							config,
							self.files_ewkz_zll(channel),
							self.root_file_folder(channel),
							lumi,
							Samples.ztt_genmatch(channel)+"*"+self.get_weights_ztt(channel=channel,cut_type=cut_type,weight=wj_weight,doStitching=False)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_high_mt_ss, cut_type=high_mt_ss_cut_type)+"*"+self.ewkz_zll_stitchingweight()+"*"+zmm_cr_factor,
							("noplot_" if not controlregions else "") + "ztt_ss_highmt",
							nick_suffix=nick_suffix
					)
					Samples._add_input(
							config,
							self.files_ewkz_znn(channel),
							self.root_file_folder(channel),
							lumi,
							Samples.ztt_genmatch(channel)+"*"+self.get_weights_ztt(channel=channel,cut_type=cut_type,weight=wj_weight,doStitching=False)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_high_mt_ss, cut_type=high_mt_ss_cut_type)+"*"+self.ewkz_znn_stitchingweight()+"*"+zmm_cr_factor,
							("noplot_" if not controlregions else "") + "ztt_ss_highmt",
							nick_suffix=nick_suffix
					)
				Samples._add_input(
						config,
						self.files_zll(channel),
						self.root_file_folder(channel),
						lumi,
						mc_weight+"*"+wj_weight+"*eventWeight*"+self.zll_stitchingweight()+"*"+Samples.zll_genmatch(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_high_mt_ss, cut_type=high_mt_ss_cut_type)+"*zPtReweightWeight"+"*"+self.zll_zl_shape_weight(channel, cut_type)+"*"+zmm_cr_factor,
						("noplot_" if not controlregions else "") + "zll_ss_highmt",
						nick_suffix=nick_suffix
				)
				if not (kwargs.get("no_ewk_samples", False) or kwargs.get("no_ewkz_as_dy", False)):
					Samples._add_input(
							config,
							self.files_ewkz_zll(channel),
							self.root_file_folder(channel),
							lumi,
							mc_weight+"*"+wj_weight+"*eventWeight*"+Samples.zll_genmatch(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_high_mt_ss, cut_type=high_mt_ss_cut_type)+"*"+self.zll_zl_shape_weight(channel, cut_type)+"*"+self.ewkz_zll_stitchingweight()+"*"+zmm_cr_factor,
							("noplot_" if not controlregions else "") + "zll_ss_highmt",
							nick_suffix=nick_suffix
					)
					Samples._add_input(
							config,
							self.files_ewkz_znn(channel),
							self.root_file_folder(channel),
							lumi,
							mc_weight+"*"+wj_weight+"*eventWeight*"+Samples.zll_genmatch(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_high_mt_ss, cut_type=high_mt_ss_cut_type)+"*"+self.zll_zl_shape_weight(channel, cut_type)+"*"+self.ewkz_znn_stitchingweight()+"*"+zmm_cr_factor,
							("noplot_" if not controlregions else "") + "zll_ss_highmt",
							nick_suffix=nick_suffix
					)
				Samples._add_input(
						config,
						self.files_zll(channel),
						self.root_file_folder(channel),
						lumi,
						mc_weight+"*"+wj_weight+"*eventWeight*"+self.zll_stitchingweight()+"*"+Samples.zl_genmatch(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_high_mt_ss, cut_type=high_mt_ss_cut_type)+"*zPtReweightWeight"+"*"+self.zl_shape_weight(channel, cut_type)+"*"+zmm_cr_factor,
						("noplot_" if not controlregions else "") + "zl_ss_highmt",
						nick_suffix=nick_suffix
				)
				if not (kwargs.get("no_ewk_samples", False) or kwargs.get("no_ewkz_as_dy", False)):
					Samples._add_input(
							config,
							self.files_ewkz_zll(channel),
							self.root_file_folder(channel),
							lumi,
							mc_weight+"*"+wj_weight+"*eventWeight*"+Samples.zl_genmatch(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_high_mt_ss, cut_type=high_mt_ss_cut_type)+"*"+self.zl_shape_weight(channel, cut_type)+"*"+self.ewkz_zll_stitchingweight()+"*"+zmm_cr_factor,
							("noplot_" if not controlregions else "") + "zl_ss_highmt",
							nick_suffix=nick_suffix
					)
					Samples._add_input(
							config,
							self.files_ewkz_znn(channel),
							self.root_file_folder(channel),
							lumi,
							mc_weight+"*"+wj_weight+"*eventWeight*"+Samples.zl_genmatch(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_high_mt_ss, cut_type=high_mt_ss_cut_type)+"*"+self.zl_shape_weight(channel, cut_type)+"*"+self.ewkz_znn_stitchingweight()+"*"+zmm_cr_factor,
							("noplot_" if not controlregions else "") + "zl_ss_highmt",
							nick_suffix=nick_suffix
					)
				Samples._add_input(
						config,
						self.files_zll(channel),
						self.root_file_folder(channel),
						lumi,
						mc_weight+"*"+wj_weight+"*eventWeight*"+self.zll_stitchingweight()+"*"+Samples.zj_genmatch(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_high_mt_ss, cut_type=high_mt_ss_cut_type)+"*zPtReweightWeight"+"*"+zmm_cr_factor,
						("noplot_" if not controlregions else "") + "zj_ss_highmt",
						nick_suffix=nick_suffix
				)
				if not (kwargs.get("no_ewk_samples", False) or kwargs.get("no_ewkz_as_dy", False)):
					Samples._add_input(
							config,
							self.files_ewkz_zll(channel),
							self.root_file_folder(channel),
							lumi,
							mc_weight+"*"+wj_weight+"*eventWeight*"+Samples.zj_genmatch(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_high_mt_ss, cut_type=high_mt_ss_cut_type)+"*"+self.ewkz_zll_stitchingweight()+"*"+zmm_cr_factor,
							("noplot_" if not controlregions else "") + "zj_ss_highmt",
							nick_suffix=nick_suffix
					)
					Samples._add_input(
							config,
							self.files_ewkz_znn(channel),
							self.root_file_folder(channel),
							lumi,
							mc_weight+"*"+wj_weight+"*eventWeight*"+Samples.zj_genmatch(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_high_mt_ss, cut_type=high_mt_ss_cut_type)+"*"+self.ewkz_znn_stitchingweight()+"*"+zmm_cr_factor,
							("noplot_" if not controlregions else "") + "zj_ss_highmt",
							nick_suffix=nick_suffix
					)
				if not kwargs.get("no_ewk_samples", False) and kwargs.get("no_ewkz_as_dy", False):
					Samples._add_input(
							config,
							self.files_ewkz_zll(channel),
							self.root_file_folder(channel),
							lumi,
							mc_weight+"*"+wj_weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_high_mt_ss, cut_type=high_mt_ss_cut_type)+"*"+self.ewkz_zll_stitchingweight()+"*"+zmm_cr_factor,
							("noplot_" if not controlregions else "") + "ewkz_ss_highmt",
							nick_suffix=nick_suffix
					)
					Samples._add_input(
							config,
							self.files_ewkz_znn(channel),
							self.root_file_folder(channel),
							lumi,
							mc_weight+"*"+wj_weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_high_mt_ss, cut_type=high_mt_ss_cut_type)+"*"+self.ewkz_znn_stitchingweight()+"*"+zmm_cr_factor,
							("noplot_" if not controlregions else "") + "ewkz_ss_highmt",
							nick_suffix=nick_suffix
					)
				Samples._add_input(
						config,
						self.files_ttj(channel),
						self.root_file_folder(channel),
						lumi,
						mc_weight+"*"+wj_weight+"*eventWeight*"+self.embedding_ttbarveto_weight(channel)+"*"+Samples.ttt_genmatch(channel,kwargs)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_high_mt_ss, cut_type=high_mt_ss_cut_type)+"*topPtReweightWeight",
						("noplot_" if not controlregions else "") + "ttt_ss_highmt",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						self.files_ttj(channel),
						self.root_file_folder(channel),
						lumi,
						mc_weight+"*"+wj_weight+"*eventWeight*"+self.embedding_ttbarveto_weight(channel)+"*"+Samples.ttj_genmatch(channel,kwargs)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_high_mt_ss, cut_type=high_mt_ss_cut_type)+"*topPtReweightWeight",
						("noplot_" if not controlregions else "") + "ttjj_ss_highmt",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						self.files_ttj(channel),
						self.root_file_folder(channel),
						lumi,
						mc_weight+"*"+wj_weight+"*eventWeight*"+self.embedding_ttbarveto_weight(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_high_mt_ss, cut_type=high_mt_ss_cut_type)+"*topPtReweightWeight",
						("noplot_" if not controlregions else "") + "ttj_ss_highmt",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						self.files_vv(channel),
						self.root_file_folder(channel),
						lumi,
						mc_weight+"*"+wj_weight+"*eventWeight*"+Samples.ttt_genmatch(channel,kwargs)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_high_mt_ss, cut_type=high_mt_ss_cut_type),
						("noplot_" if not controlregions else "") + "vvt_ss_highmt",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						self.files_vv(channel),
						self.root_file_folder(channel),
						lumi,
						mc_weight+"*"+wj_weight+"*eventWeight*"+Samples.ttj_genmatch(channel,kwargs)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_high_mt_ss, cut_type=high_mt_ss_cut_type),
						("noplot_" if not controlregions else "") + "vvj_ss_highmt",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						self.files_vv(channel),
						self.root_file_folder(channel),
						lumi,
						mc_weight+"*"+wj_weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_high_mt_ss, cut_type=high_mt_ss_cut_type),
						("noplot_" if not controlregions else "") + "vv_ss_highmt",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						self.files_data(channel),
						self.root_file_folder(channel),
						1.0,
						data_weight+"*"+wj_weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_high_mt_ss, cut_type=high_mt_ss_cut_type),
						("noplot_" if not controlregions else "") + "data_ss_highmt",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						self.files_wj(channel),
						self.root_file_folder(channel),
						lumi,
						mc_weight+"*"+wj_weight+"*eventWeight*"+self.wj_stitchingweight()+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_high_mt_ss, cut_type=high_mt_ss_cut_type),
						("noplot_" if not controlregions else "") + "wj_ss_highmt",
						nick_suffix=nick_suffix
				)
				if (not kwargs.get("no_ewk_samples", False)):
					Samples._add_input(
							config,
							self.files_ewkwm(channel),
							self.root_file_folder(channel),
							lumi,
							mc_weight+"*"+wj_weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_high_mt_ss, cut_type=high_mt_ss_cut_type)+"*"+self.ewkwm_stitchingweight(),
							("noplot_" if not controlregions else "") + "wj_ss_highmt",
							nick_suffix=nick_suffix
					)
					Samples._add_input(
							config,
							self.files_ewkwp(channel),
							self.root_file_folder(channel),
							lumi,
							mc_weight+"*"+wj_weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_high_mt_ss, cut_type=high_mt_ss_cut_type)+"*"+self.ewkwp_stitchingweight(),
							("noplot_" if not controlregions else "") + "wj_ss_highmt",
							nick_suffix=nick_suffix
					)
				Samples._add_input(
						config,
						self.files_wj(channel),
						self.root_file_folder(channel),
						lumi,
						mc_weight+"*"+wj_shape_weight+"*eventWeight*"+self.wj_stitchingweight()+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=wj_shape_cut_type),
						"wj",
						nick_suffix=nick_suffix
				)
				if (not kwargs.get("no_ewk_samples", False)):
					Samples._add_input(
							config,
							self.files_ewkwm(channel),
							self.root_file_folder(channel),
							lumi,
							mc_weight+"*"+wj_shape_weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=wj_shape_cut_type)+"*"+self.ewkwm_stitchingweight(),
							"wj",
							nick_suffix=nick_suffix
					)
					Samples._add_input(
							config,
							self.files_ewkwp(channel),
							self.root_file_folder(channel),
							lumi,
							mc_weight+"*"+wj_shape_weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=wj_shape_cut_type)+"*"+self.ewkwp_stitchingweight(),
							"wj",
							nick_suffix=nick_suffix
					)
				# exact wj selection on MC
				if "newKIT" in estimationMethod:
					Samples._add_input(
							config,
							self.files_wj(channel),
							self.root_file_folder(channel),
							lumi,
							mc_weight+"*"+weight+"*eventWeight*"+self.wj_stitchingweight()+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type),
							"noplot_wj_final_selection",
							nick_suffix=nick_suffix
					)
					if (not kwargs.get("no_ewk_samples", False)):
						Samples._add_input(
								config,
								self.files_ewkwm(channel),
								self.root_file_folder(channel),
								lumi,
								mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+self.ewkwm_stitchingweight(),
								"noplot_wj_final_selection",
								nick_suffix=nick_suffix
						)
						Samples._add_input(
								config,
								self.files_ewkwp(channel),
								self.root_file_folder(channel),
								lumi,
								mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+self.ewkwp_stitchingweight(),
								"noplot_wj_final_selection",
								nick_suffix=nick_suffix
						)
				Samples._add_input(
						config,
						self.files_wj(channel),
						self.root_file_folder(channel),
						lumi,
						mc_weight+"*"+wj_weight+"*eventWeight*"+self.wj_stitchingweight()+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_high_mt+exclude_cuts_relaxed, cut_type=wj_highmt_shape_cut_type),
						"noplot_wj_relaxed_os_highmt",
						nick_suffix=nick_suffix
				)
				if (not kwargs.get("no_ewk_samples", False)):
					Samples._add_input(
							config,
							self.files_ewkwm(channel),
							self.root_file_folder(channel),
							lumi,
							mc_weight+"*"+wj_weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_high_mt+exclude_cuts_relaxed, cut_type=wj_highmt_shape_cut_type)+"*"+self.ewkwm_stitchingweight(),
							"noplot_wj_relaxed_os_highmt",
							nick_suffix=nick_suffix
					)
					Samples._add_input(
							config,
							self.files_ewkwp(channel),
							self.root_file_folder(channel),
							lumi,
							mc_weight+"*"+wj_weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_high_mt+exclude_cuts_relaxed, cut_type=wj_highmt_shape_cut_type)+"*"+self.ewkwp_stitchingweight(),
							"noplot_wj_relaxed_os_highmt",
							nick_suffix=nick_suffix
					)
				Samples._add_input(
						config,
						self.files_wj(channel),
						self.root_file_folder(channel),
						lumi,
						mc_weight+"*"+wj_weight+"*eventWeight*"+self.wj_stitchingweight()+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts+exclude_cuts_relaxed, cut_type=wj_shape_cut_type),
						"noplot_wj_relaxed_os_lowmt",
						nick_suffix=nick_suffix
				)
				if (not kwargs.get("no_ewk_samples", False)):
					Samples._add_input(
							config,
							self.files_ewkwm(channel),
							self.root_file_folder(channel),
							lumi,
							mc_weight+"*"+wj_weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts+exclude_cuts_relaxed, cut_type=wj_shape_cut_type)+"*"+self.ewkwm_stitchingweight(),
							"noplot_wj_relaxed_os_lowmt",
							nick_suffix=nick_suffix
					)
					Samples._add_input(
							config,
							self.files_ewkwp(channel),
							self.root_file_folder(channel),
							lumi,
							mc_weight+"*"+wj_weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts+exclude_cuts_relaxed, cut_type=wj_shape_cut_type)+"*"+self.ewkwp_stitchingweight(),
							"noplot_wj_relaxed_os_lowmt",
							nick_suffix=nick_suffix
					)
				if not "EstimateWjetsAndQCD" in config.get("analysis_modules", []):
					config.setdefault("analysis_modules", []).append("EstimateWjetsAndQCD")
				if controlregions:
					if not kwargs.get("no_ewk_samples", False) and kwargs.get("no_ewkz_as_dy", False):
						config.setdefault("wjets_ss_substract_nicks", []).append(" ".join([nick+nick_suffix for nick in "ztt_ss_highmt zll_ss_highmt ewkz_ss_highmt ttj_ss_highmt vv_ss_highmt".split()]))
						config.setdefault("wjets_os_substract_nicks", []).append(" ".join([nick+nick_suffix for nick in "ztt_os_highmt zll_os_highmt ewkz_os_highmt ttj_os_highmt vv_os_highmt".split()]))
					else:
						config.setdefault("wjets_ss_substract_nicks", []).append(" ".join([nick+nick_suffix for nick in "ztt_ss_highmt zll_ss_highmt ttj_ss_highmt vv_ss_highmt".split()]))
						config.setdefault("wjets_os_substract_nicks", []).append(" ".join([nick+nick_suffix for nick in "ztt_os_highmt zll_os_highmt ttj_os_highmt vv_os_highmt".split()]))
					config.setdefault("wjets_ss_data_nicks", []).append("data_ss_highmt"+nick_suffix)
					config.setdefault("wjets_os_data_nicks", []).append("data_os_highmt"+nick_suffix)
					config.setdefault("wjets_shape_nicks", []).append("wj"+nick_suffix)
					config.setdefault("wjets_ss_highmt_mc_nicks", []).append("wj_ss_highmt"+nick_suffix)
					config.setdefault("wjets_os_highmt_mc_nicks", []).append("wj_os_highmt"+nick_suffix)
					config.setdefault("wjets_wj_final_selection", []).append(("noplot_wj_final_selection"+nick_suffix) if "newKIT" in estimationMethod else None)
					config.setdefault("wjets_relaxed_os_highmt_nicks", []).append("noplot_wj_relaxed_os_highmt"+nick_suffix)
					config.setdefault("wjets_relaxed_os_lowmt_nicks", []).append("noplot_wj_relaxed_os_lowmt"+nick_suffix)
					for nick in ["ztt_os_highmt", "zll_os_highmt", "zl_os_highmt", "zj_os_highmt", "ttt_os_highmt", "ttjj_os_highmt", "ttj_os_highmt", "vvt_os_highmt", "vvj_os_highmt", "vv_os_highmt", "data_os_highmt", "wj_os_highmt", "ztt_ss_highmt", "zll_ss_highmt", "zl_ss_highmt", "zj_ss_highmt", "ttt_ss_highmt", "ttjj_ss_highmt", "ttj_ss_highmt", "vvt_ss_highmt", "vvj_ss_highmt", "vv_ss_highmt", "data_ss_highmt", "wj_ss_highmt"]+(["ewkz_os_highmt", "ewkz_ss_highmt"] if (not kwargs.get("no_ewk_samples", False) and kwargs.get("no_ewkz_as_dy", False)) else []):
						if not kwargs.get("mssm", False):
							Samples._add_bin_corrections(config, nick, nick_suffix)
						Samples._add_plot(config, "bkg", "HIST", "F", nick, nick_suffix)
				else:
					if not kwargs.get("no_ewk_samples", False) and kwargs.get("no_ewkz_as_dy", False):
						config.setdefault("wjets_ss_substract_nicks", []).append(" ".join(["noplot_"+nick+nick_suffix for nick in "ztt_ss_highmt zll_ss_highmt ewkz_ss_highmt ttj_ss_highmt vv_ss_highmt".split()]))
						config.setdefault("wjets_os_substract_nicks", []).append(" ".join(["noplot_"+nick+nick_suffix for nick in "ztt_os_highmt zll_os_highmt ewkz_os_highmt ttj_os_highmt vv_os_highmt".split()]))
					else:
						config.setdefault("wjets_ss_substract_nicks", []).append(" ".join(["noplot_"+nick+nick_suffix for nick in "ztt_ss_highmt zll_ss_highmt ttj_ss_highmt vv_ss_highmt".split()]))
						config.setdefault("wjets_os_substract_nicks", []).append(" ".join(["noplot_"+nick+nick_suffix for nick in "ztt_os_highmt zll_os_highmt ttj_os_highmt vv_os_highmt".split()]))
					config.setdefault("wjets_ss_data_nicks", []).append("noplot_data_ss_highmt"+nick_suffix)
					config.setdefault("wjets_os_data_nicks", []).append("noplot_data_os_highmt"+nick_suffix)
					config.setdefault("wjets_shape_nicks", []).append("wj"+nick_suffix)
					config.setdefault("wjets_ss_highmt_mc_nicks", []).append("noplot_wj_ss_highmt"+nick_suffix)
					config.setdefault("wjets_os_highmt_mc_nicks", []).append("noplot_wj_os_highmt"+nick_suffix)
					config.setdefault("wjets_wj_final_selection", []).append(("noplot_wj_final_selection"+nick_suffix) if "newKIT" in estimationMethod else None)
					config.setdefault("wjets_relaxed_os_highmt_nicks", []).append("noplot_wj_relaxed_os_highmt"+nick_suffix)
					config.setdefault("wjets_relaxed_os_lowmt_nicks", []).append("noplot_wj_relaxed_os_lowmt"+nick_suffix)

			if "classic" in estimationMethod:
				shape_weight = mc_weight+"*"+weight+"*eventWeight*"+self.wj_stitchingweight()+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)
				#if (not category is None) and (category != ""):
					## relaxed isolation
					#shape_weight = weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["blind", "iso_2"], cut_type=cut_type)+"*(byCombinedIsolationDeltaBetaCorrRaw3Hits_2<10.0)"

				Samples._add_input(
						config,
						self.files_wj(channel),
						self.root_file_folder(channel),
						lumi,
						shape_weight,
						"wj",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						self.files_data(channel),
						self.root_file_folder(channel),
						1.0,
						data_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_high_mt, cut_type=high_mt_cut_type),
						"noplot_wj_data_control",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						self.files_ztt(channel),
						self.root_file_folder(channel),
						lumi,
						Samples.ztt_genmatch(channel)+"*"+self.get_weights_ztt(channel=channel,cut_type=cut_type,weight=weight)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_high_mt, cut_type=high_mt_cut_type)+"*zPtReweightWeight"+"*"+zmm_cr_factor,
						"noplot_ztt_mc_wj_control",
						nick_suffix=nick_suffix
				)
				if not (kwargs.get("no_ewk_samples", False) or kwargs.get("no_ewkz_as_dy", False)):
					Samples._add_input(
							config,
							self.files_ewkz_zll(channel),
							self.root_file_folder(channel),
							lumi,
							Samples.ztt_genmatch(channel)+"*"+self.get_weights_ztt(channel=channel,cut_type=cut_type,weight=weight,doStitching=False)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_high_mt, cut_type=high_mt_cut_type)+"*"+self.ewkz_zll_stitchingweight()+"*"+zmm_cr_factor,
							"noplot_ztt_mc_wj_control",
							nick_suffix=nick_suffix
					)
					Samples._add_input(
							config,
							self.files_ewkz_znn(channel),
							self.root_file_folder(channel),
							lumi,
							Samples.ztt_genmatch(channel)+"*"+self.get_weights_ztt(channel=channel,cut_type=cut_type,weight=weight,doStitching=False)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_high_mt, cut_type=high_mt_cut_type)+"*"+self.ewkz_znn_stitchingweight()+"*"+zmm_cr_factor,
							"noplot_ztt_mc_wj_control",
							nick_suffix=nick_suffix
					)
				Samples._add_input(
						config,
						self.files_zll(channel),
						self.root_file_folder(channel),
						lumi,
						mc_weight+"*"+weight+"*eventWeight*"+self.zll_stitchingweight()+"*"+Samples.zll_genmatch(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_high_mt, cut_type=high_mt_cut_type)+"*zPtReweightWeight"+"*"+self.zll_zl_shape_weight(channel, cut_type)+"*"+zmm_cr_factor,
						"noplot_zll_wj_control",
						nick_suffix=nick_suffix
				)
				if not (kwargs.get("no_ewk_samples", False) or kwargs.get("no_ewkz_as_dy", False)):
					Samples._add_input(
							config,
							self.files_ewkz_zll(channel),
							self.root_file_folder(channel),
							lumi,
							mc_weight+"*"+weight+"*eventWeight*"+Samples.zll_genmatch(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_high_mt, cut_type=high_mt_cut_type)+"*"+self.zll_zl_shape_weight(channel, cut_type)+"*"+self.ewkz_zll_stitchingweight()+"*"+zmm_cr_factor,
							"noplot_zll_wj_control",
							nick_suffix=nick_suffix
					)
					Samples._add_input(
							config,
							self.files_ewkz_znn(channel),
							self.root_file_folder(channel),
							lumi,
							mc_weight+"*"+weight+"*eventWeight*"+Samples.zll_genmatch(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_high_mt, cut_type=high_mt_cut_type)+"*"+self.zll_zl_shape_weight(channel, cut_type)+"*"+self.ewkz_znn_stitchingweight()+"*"+zmm_cr_factor,
							"noplot_zll_wj_control",
							nick_suffix=nick_suffix
					)
				if not kwargs.get("no_ewk_samples", False) and kwargs.get("no_ewkz_as_dy", False):
					Samples._add_input(
							config,
							self.files_ewkz_zll(channel),
							self.root_file_folder(channel),
							lumi,
							mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_high_mt, cut_type=high_mt_cut_type)+"*"+self.ewkz_zll_stitchingweight()+"*"+zmm_cr_factor,
							"noplot_ewkz_wj_control",
							nick_suffix=nick_suffix
					)
					Samples._add_input(
							config,
							self.files_ewkz_znn(channel),
							self.root_file_folder(channel),
							lumi,
							mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_high_mt, cut_type=high_mt_cut_type)+"*"+self.ewkz_znn_stitchingweight()+"*"+zmm_cr_factor,
							"noplot_ewkz_wj_control",
							nick_suffix=nick_suffix
					)
				Samples._add_input(
						config,
						self.files_ttj(channel),
						self.root_file_folder(channel),
						lumi,
						mc_weight+"*"+weight+"*eventWeight*"+self.embedding_ttbarveto_weight(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_high_mt, cut_type=high_mt_cut_type)+"*topPtReweightWeight",
						"noplot_ttj_wj_control",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						self.files_vv(channel),
						self.root_file_folder(channel),
						lumi,
						mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_high_mt, cut_type=high_mt_cut_type),
						"noplot_vv_wj_control",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						self.files_wj(channel),
						self.root_file_folder(channel),
						lumi,
						mc_weight+"*"+weight+"*eventWeight*"+self.wj_stitchingweight()+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type),
						"noplot_wj_mc_signal",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						self.files_wj(channel),
						self.root_file_folder(channel),
						lumi,
						mc_weight+"*"+weight+"*eventWeight*"+self.wj_stitchingweight()+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_high_mt, cut_type=high_mt_cut_type),
						"noplot_wj_mc_control",
						nick_suffix=nick_suffix
				)

				if not "EstimateWjets" in config.get("analysis_modules", []):
					config.setdefault("analysis_modules", []).append("EstimateWjets")
				# if fakefactor_method is None:
					# config.setdefault("wjets_from_mc", []).append(False)
				config.setdefault("wjets_shape_nicks", []).append("wj"+nick_suffix)
				config.setdefault("wjets_data_control_nicks", []).append("noplot_wj_data_control"+nick_suffix)
				if not kwargs.get("no_ewk_samples", False) and kwargs.get("no_ewkz_as_dy", False):
					config.setdefault("wjets_data_substract_nicks", []).append(" ".join([nick+nick_suffix for nick in "noplot_ztt_mc_wj_control noplot_zll_wj_control noplot_ewkz_wj_control noplot_ttj_wj_control noplot_vv_wj_control".split()]))
				else:
					config.setdefault("wjets_data_substract_nicks", []).append(" ".join([nick+nick_suffix for nick in "noplot_ztt_mc_wj_control noplot_zll_wj_control noplot_ttj_wj_control noplot_vv_wj_control".split()]))
				config.setdefault("wjets_mc_signal_nicks", []).append("noplot_wj_mc_signal"+nick_suffix)
				config.setdefault("wjets_mc_control_nicks", []).append("noplot_wj_mc_control"+nick_suffix)

		elif channel in ["em", "tt", "mm", "ee", "ttbar"]:
			Samples._add_input(
					config,
					self.files_wj(channel),
					self.root_file_folder(channel),
					lumi,
					weight+"*eventWeight*"+self.wj_stitchingweight()+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type),
					"wj",
					nick_suffix=nick_suffix
			)
			if (not kwargs.get("no_ewk_samples", False)):
				Samples._add_input(
						config,
						self.files_ewkwm(channel),
						self.root_file_folder(channel),
						lumi,
						weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+self.ewkwm_stitchingweight(),
						"wj",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						self.files_ewkwp(channel),
						self.root_file_folder(channel),
						lumi,
						weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)+"*"+self.ewkwp_stitchingweight(),
						"wj",
						nick_suffix=nick_suffix
				)
			if channel == "em" or channel == "ttbar":
				Samples._add_input(
						config,
						self.files_wgamma(channel),
						self.root_file_folder(channel),
						lumi,
						weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type),
						"wj",
						nick_suffix=nick_suffix
				)
		else:
			log.error("Sample config (WJets) currently not implemented for channel \"%s\"!" % channel)

		if not kwargs.get("no_plot", False):
			if not kwargs.get("mssm", False):
				Samples._add_bin_corrections(config, "wj", nick_suffix)
			Samples._add_plot(config, "bkg", "HIST", "F", "wj", nick_suffix)
		return config

	def qcd(self, config, channel, category, weight, nick_suffix, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", estimationMethod="classic", controlregions=False,**kwargs):
		if exclude_cuts is None:
			exclude_cuts = []
		
		zmm_cr_factor = kwargs.get("zmm_cr_factor", "(1.0)")

		scale_factor = 1.0
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("QCD", 1.0)

		data_weight, mc_weight = self.projection(kwargs)

		if channel in ["et", "mt", "em", "tt", "mm", "ee", "ttbar"]:
			if "classic" in estimationMethod:
				# WJets for QCD estimate
				Samples._add_input(
						config,
						self.files_wj(channel),
						self.root_file_folder(channel),
						lumi,
						mc_weight+"*"+weight+"*eventWeight*"+self.wj_stitchingweight()+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=cut_type)+"*((q_1*q_2)>0.0)",
						"noplot_wj_ss",
						nick_suffix=nick_suffix
				)

				if channel in ["mt", "et"]:
					high_mt_ss_cut_type = cut_type + "highMtSSControlRegionWJ"
					exclude_cuts_high_mt = [cut for cut in exclude_cuts if cut not in ["mt"]]
					exclude_cuts_high_mt_ss = copy.deepcopy(exclude_cuts_high_mt)+["os"]

					Samples._add_input(
							config,
							self.files_data(channel),
							self.root_file_folder(channel),
							1.0,
							data_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_high_mt_ss, cut_type=high_mt_ss_cut_type),
							"noplot_wj_ss_data_control",
							nick_suffix=nick_suffix
					)
					Samples._add_input(
							config,
							self.files_ztt(channel),
							self.root_file_folder(channel),
							lumi,
							Samples.ztt_genmatch(channel)+"*"+self.get_weights_ztt(channel=channel,cut_type=cut_type,weight=weight)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_high_mt_ss, cut_type=high_mt_ss_cut_type)+"*zPtReweightWeight"+"*"+zmm_cr_factor,
							"noplot_ztt_ss_mc_wj_control",
							nick_suffix=nick_suffix
					)
					if not (kwargs.get("no_ewk_samples", False) or kwargs.get("no_ewkz_as_dy", False)):
						Samples._add_input(
								config,
								self.files_ewkz_zll(channel),
								self.root_file_folder(channel),
								lumi,
								Samples.ztt_genmatch(channel)+"*"+self.get_weights_ztt(channel=channel,cut_type=cut_type,weight=weight,doStitching=False)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_high_mt_ss, cut_type=high_mt_ss_cut_type)+"*"+self.ewkz_zll_stitchingweight()+"*"+zmm_cr_factor,
								"noplot_ztt_ss_mc_wj_control",
								nick_suffix=nick_suffix
						)
						Samples._add_input(
								config,
								self.files_ewkz_znn(channel),
								self.root_file_folder(channel),
								lumi,
								Samples.ztt_genmatch(channel)+"*"+self.get_weights_ztt(channel=channel,cut_type=cut_type,weight=weight,doStitching=False)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_high_mt_ss, cut_type=high_mt_ss_cut_type)+"*"+self.ewkz_znn_stitchingweight()+"*"+zmm_cr_factor,
								"noplot_ztt_ss_mc_wj_control",
								nick_suffix=nick_suffix
						)
					Samples._add_input(
							config,
							self.files_zll(channel),
							self.root_file_folder(channel),
							lumi,
							mc_weight+"*"+weight+"*eventWeight*"+self.zll_stitchingweight()+"*"+Samples.zll_genmatch(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_high_mt_ss, cut_type=high_mt_ss_cut_type)+"*zPtReweightWeight"+"*"+self.zll_zl_shape_weight(channel, cut_type)+"*"+zmm_cr_factor,
							"noplot_zll_ss_wj_control",
							nick_suffix=nick_suffix
					)
					if not (kwargs.get("no_ewk_samples", False) or kwargs.get("no_ewkz_as_dy", False)):
						Samples._add_input(
								config,
								self.files_ewkz_zll(channel),
								self.root_file_folder(channel),
								lumi,
								mc_weight+"*"+weight+"*eventWeight*"+Samples.zll_genmatch(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_high_mt_ss, cut_type=high_mt_ss_cut_type)+"*"+self.zll_zl_shape_weight(channel, cut_type)+"*"+self.ewkz_zll_stitchingweight()+"*"+zmm_cr_factor,
								"noplot_zll_ss_wj_control",
								nick_suffix=nick_suffix
						)
						Samples._add_input(
								config,
								self.files_ewkz_znn(channel),
								self.root_file_folder(channel),
								lumi,
								mc_weight+"*"+weight+"*eventWeight*"+Samples.zll_genmatch(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_high_mt_ss, cut_type=high_mt_ss_cut_type)+"*"+self.zll_zl_shape_weight(channel, cut_type)+"*"+self.ewkz_znn_stitchingweight()+"*"+zmm_cr_factor,
								"noplot_zll_ss_wj_control",
								nick_suffix=nick_suffix
						)
					if not kwargs.get("no_ewk_samples", False) and kwargs.get("no_ewkz_as_dy", False):
						Samples._add_input(
								config,
								self.files_ewkz_zll(channel),
								self.root_file_folder(channel),
								lumi,
								mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_high_mt_ss, cut_type=high_mt_ss_cut_type)+"*"+self.ewkz_zll_stitchingweight()+"*"+zmm_cr_factor,
								"noplot_ewkz_ss_wj_control",
								nick_suffix=nick_suffix
						)
						Samples._add_input(
								config,
								self.files_ewkz_znn(channel),
								self.root_file_folder(channel),
								lumi,
								mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_high_mt_ss, cut_type=high_mt_ss_cut_type)+"*"+self.ewkz_znn_stitchingweight()+"*"+zmm_cr_factor,
								"noplot_ewkz_ss_wj_control",
								nick_suffix=nick_suffix
						)
					Samples._add_input(
							config,
							self.files_ttj(channel),
							self.root_file_folder(channel),
							lumi,
							mc_weight+"*"+weight+"*eventWeight*"+self.embedding_ttbarveto_weight(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_high_mt_ss, cut_type=high_mt_ss_cut_type)+"*topPtReweightWeight",
							"noplot_ttj_ss_wj_control",
							nick_suffix=nick_suffix
					)
					Samples._add_input(
							config,
							self.files_vv(channel),
							self.root_file_folder(channel),
							lumi,
							mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_high_mt_ss, cut_type=high_mt_ss_cut_type),
							"noplot_vv_ss_wj_control",
							nick_suffix=nick_suffix
					)
					Samples._add_input(
							config,
							self.files_wj(channel),
							self.root_file_folder(channel),
							lumi,
							mc_weight+"*"+weight+"*eventWeight*"+self.wj_stitchingweight()+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=cut_type)+"*((q_1*q_2)>0.0)",
							"noplot_wj_ss_mc_signal",
							nick_suffix=nick_suffix
					)
					Samples._add_input(
							config,
							self.files_wj(channel),
							self.root_file_folder(channel),
							lumi,
							mc_weight+"*"+weight+"*eventWeight*"+self.wj_stitchingweight()+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_high_mt_ss, cut_type=high_mt_ss_cut_type),
							"noplot_wj_ss_mc_control",
							nick_suffix=nick_suffix
					)

					if not "EstimateWjets" in config.get("analysis_modules", []):
						config.setdefault("analysis_modules", []).append("EstimateWjets")
					config.setdefault("wjets_from_mc", []).append(False)
					config.setdefault("wjets_shape_nicks", []).append("noplot_wj_ss"+nick_suffix)
					config.setdefault("wjets_data_control_nicks", []).append("noplot_wj_ss_data_control"+nick_suffix)
					if not kwargs.get("no_ewk_samples", False) and kwargs.get("no_ewkz_as_dy", False):
						config.setdefault("wjets_data_substract_nicks", []).append(" ".join([nick+nick_suffix for nick in "noplot_ztt_ss_mc_wj_control noplot_zll_ss_wj_control noplot_ttj_ss_wj_control noplot_vv_ss_wj_control".split()]))
					else:
						config.setdefault("wjets_data_substract_nicks", []).append(" ".join([nick+nick_suffix for nick in "noplot_ztt_ss_mc_wj_control noplot_zll_ss_wj_control noplot_ewkz_ss_wj_control noplot_ttj_ss_wj_control noplot_vv_ss_wj_control".split()]))
					config.setdefault("wjets_mc_signal_nicks", []).append("noplot_wj_ss_mc_signal"+nick_suffix)
					config.setdefault("wjets_mc_control_nicks", []).append("noplot_wj_ss_mc_control"+nick_suffix)

				# QCD
				shape_weight = data_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=cut_type)+"*((q_1*q_2)>0.0)"
				#if (not category is None) and (category != ""):
					## relaxed/inverted isolation
					#if channel in ["et", "mt"]:
						#shape_weight = weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["blind", "os", "iso_2"], cut_type=cut_type)+"*((q_1*q_2)>0.0)"+"*(byCombinedIsolationDeltaBetaCorrRaw3Hits_2<10.0)"
					#else:
						#shape_weight = weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["blind", "os", "iso_1", "iso_2"], cut_type=cut_type)+"*((q_1*q_2)>0.0)"

				Samples._add_input(
						config,
						self.files_data(channel),
						self.root_file_folder(channel),
						1.0,
						shape_weight,
						"qcd",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						self.files_data(channel),
						self.root_file_folder(channel),
						1.0,
						data_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=cut_type)+"*((q_1*q_2)>0.0)",
						"noplot_data_qcd_yield",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						self.files_data(channel),
						self.root_file_folder(channel),
						1.0,
						data_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=cut_type)+"*((q_1*q_2)>0.0)",
						"noplot_data_qcd_control",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						self.files_ztt(channel),
						self.root_file_folder(channel),
						lumi,
						Samples.ztt_genmatch(channel)+"*"+self.get_weights_ztt(channel=channel,cut_type=cut_type,weight=weight)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=cut_type)+"*((q_1*q_2)>0.0)"+"*zPtReweightWeight"+"*"+zmm_cr_factor,
						"noplot_ztt_mc_qcd_control",
						nick_suffix=nick_suffix
				)
				if not (kwargs.get("no_ewk_samples", False) or kwargs.get("no_ewkz_as_dy", False)):
					Samples._add_input(
							config,
							self.files_ewkz_zll(channel),
							self.root_file_folder(channel),
							lumi,
							Samples.ztt_genmatch(channel)+"*"+self.get_weights_ztt(channel=channel,cut_type=cut_type,weight=weight,doStitching=False)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=cut_type)+"*((q_1*q_2)>0.0)"+"*"+self.ewkz_zll_stitchingweight()+"*"+zmm_cr_factor,
							"noplot_ztt_mc_qcd_control",
							nick_suffix=nick_suffix
					)
					Samples._add_input(
							config,
							self.files_ewkz_znn(channel),
							self.root_file_folder(channel),
							lumi,
							Samples.ztt_genmatch(channel)+"*"+self.get_weights_ztt(channel=channel,cut_type=cut_type,weight=weight,doStitching=False)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=cut_type)+"*((q_1*q_2)>0.0)"+"*"+self.ewkz_znn_stitchingweight()+"*"+zmm_cr_factor,
							"noplot_ztt_mc_qcd_control",
							nick_suffix=nick_suffix
					)
				Samples._add_input(
						config,
						self.files_zll(channel),
						self.root_file_folder(channel),
						lumi,
						mc_weight+"*"+weight+"*eventWeight*"+self.zll_stitchingweight()+"*"+Samples.zll_genmatch(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=cut_type)+"*((q_1*q_2)>0.0)"+"*zPtReweightWeight"+"*"+self.zll_zl_shape_weight(channel, cut_type)+"*"+zmm_cr_factor,
						"noplot_zll_qcd_control",
						nick_suffix=nick_suffix
				)
				if not (kwargs.get("no_ewk_samples", False) or kwargs.get("no_ewkz_as_dy", False)):
					Samples._add_input(
							config,
							self.files_ewkz_zll(channel),
							self.root_file_folder(channel),
							lumi,
							mc_weight+"*"+weight+"*eventWeight*"+Samples.zll_genmatch(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=cut_type)+"*((q_1*q_2)>0.0)"+"*"+self.zll_zl_shape_weight(channel, cut_type)+"*"+self.ewkz_zll_stitchingweight()+"*"+zmm_cr_factor,
							"noplot_zll_qcd_control",
							nick_suffix=nick_suffix
					)
					Samples._add_input(
							config,
							self.files_ewkz_znn(channel),
							self.root_file_folder(channel),
							lumi,
							mc_weight+"*"+weight+"*eventWeight*"+Samples.zll_genmatch(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=cut_type)+"*((q_1*q_2)>0.0)"+"*"+self.zll_zl_shape_weight(channel, cut_type)+"*"+self.ewkz_znn_stitchingweight()+"*"+zmm_cr_factor,
							"noplot_zll_qcd_control",
							nick_suffix=nick_suffix
					)
				if not kwargs.get("no_ewk_samples", False) and kwargs.get("no_ewkz_as_dy", False):
					Samples._add_input(
							config,
							self.files_ewkz_zll(channel),
							self.root_file_folder(channel),
							lumi,
							mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=cut_type)+"*((q_1*q_2)>0.0)"+"*"+self.ewkz_zll_stitchingweight()+"*"+zmm_cr_factor,
							"noplot_ewkz_qcd_control",
							nick_suffix=nick_suffix
					)
					Samples._add_input(
							config,
							self.files_ewkz_znn(channel),
							self.root_file_folder(channel),
							lumi,
							mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=cut_type)+"*((q_1*q_2)>0.0)"+"*"+self.ewkz_znn_stitchingweight()+"*"+zmm_cr_factor,
							"noplot_ewkz_qcd_control",
							nick_suffix=nick_suffix
					)
				Samples._add_input(
						config,
						self.files_ttj(channel),
						self.root_file_folder(channel),
						lumi,
						mc_weight+"*"+weight+"*eventWeight*"+self.embedding_ttbarveto_weight(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=cut_type)+"*((q_1*q_2)>0.0)*topPtReweightWeight",
						"noplot_ttj_qcd_control",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						self.files_vv(channel),
						self.root_file_folder(channel),
						lumi,
						mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=cut_type)+"*((q_1*q_2)>0.0)",
						"noplot_vv_qcd_control",
						nick_suffix=nick_suffix
				)

				if not "EstimateQcd" in config.get("analysis_modules", []):
					config.setdefault("analysis_modules", []).append("EstimateQcd")
				config.setdefault("qcd_shape_nicks", []).append("qcd"+nick_suffix)
				config.setdefault("qcd_yield_nicks", []).append("noplot_data_qcd_yield"+nick_suffix)
				if not kwargs.get("no_ewk_samples", False) and kwargs.get("no_ewkz_as_dy", False):
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

			if "new" in estimationMethod:
				if channel in ["et","mt"]:
					high_mt_ss_cut_type = cut_type + "highMtSSControlRegionWJ"
					qcd_shape_cut = cut_type
					exclude_cuts_high_mt = [cut for cut in exclude_cuts if cut not in ["mt"]]
					exclude_cuts_high_mt_ss = copy.deepcopy(exclude_cuts_high_mt)+["os"]
					exclude_cuts_relaxed = []
					
					if category != None:
						qcd_shape_cut = qcd_shape_cut + ("relaxedETauMuTauWJ" if ("1jet" in category or "vbf" in category or "Boosted2D" in category or "Vbf2D" in category) else "")
						exclude_cuts_relaxed = ["iso_1", "iso_2"] if ("1jet" in category or "vbf" in category or "Boosted2D" in category or "Vbf2D" in category) else []
					
					qcd_shape_weight = weight
					if "newKIT" in estimationMethod:
						qcd_shape_weight = make_multiplication(Samples.get_jetbin(channel, category, weight))
					
					Samples._add_input(
							config,
							self.files_ztt(channel),
							self.root_file_folder(channel),
							lumi,
							Samples.ztt_genmatch(channel)+"*"+self.get_weights_ztt(channel=channel,cut_type=cut_type,weight=weight)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=cut_type)+"*((q_1*q_2)>0.0)"+"*zPtReweightWeight"+"*"+zmm_cr_factor,
							("noplot_" if not controlregions else "") + "ztt_ss_lowmt",
							nick_suffix=nick_suffix
					)
					if not (kwargs.get("no_ewk_samples", False) or kwargs.get("no_ewkz_as_dy", False)):
						Samples._add_input(
								config,
								self.files_ewkz_zll(channel),
								self.root_file_folder(channel),
								lumi,
								Samples.ztt_genmatch(channel)+"*"+self.get_weights_ztt(channel=channel,cut_type=cut_type,weight=weight,doStitching=False)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=cut_type)+"*((q_1*q_2)>0.0)"+"*"+self.ewkz_zll_stitchingweight()+"*"+zmm_cr_factor,
								("noplot_" if not controlregions else "") + "ztt_ss_lowmt",
								nick_suffix=nick_suffix
						)
						Samples._add_input(
								config,
								self.files_ewkz_znn(channel),
								self.root_file_folder(channel),
								lumi,
								Samples.ztt_genmatch(channel)+"*"+self.get_weights_ztt(channel=channel,cut_type=cut_type,weight=weight,doStitching=False)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=cut_type)+"*((q_1*q_2)>0.0)"+"*"+self.ewkz_znn_stitchingweight()+"*"+zmm_cr_factor,
								("noplot_" if not controlregions else "") + "ztt_ss_lowmt",
								nick_suffix=nick_suffix
						)
					Samples._add_input(
							config,
							self.files_zll(channel),
							self.root_file_folder(channel),
							lumi,
							mc_weight+"*"+weight+"*eventWeight*"+self.zll_stitchingweight()+"*"+Samples.zll_genmatch(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=cut_type)+"*((q_1*q_2)>0.0)"+"*zPtReweightWeight"+"*"+self.zll_zl_shape_weight(channel, cut_type)+"*"+zmm_cr_factor,
							("noplot_" if not controlregions else "") + "zll_ss_lowmt",
							nick_suffix=nick_suffix
					)
					if not (kwargs.get("no_ewk_samples", False) or kwargs.get("no_ewkz_as_dy", False)):
						Samples._add_input(
								config,
								self.files_ewkz_zll(channel),
								self.root_file_folder(channel),
								lumi,
								mc_weight+"*"+weight+"*eventWeight*"+Samples.zll_genmatch(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=cut_type)+"*((q_1*q_2)>0.0)"+"*"+self.zll_zl_shape_weight(channel, cut_type)+"*"+self.ewkz_zll_stitchingweight()+"*"+zmm_cr_factor,
								("noplot_" if not controlregions else "") + "zll_ss_lowmt",
								nick_suffix=nick_suffix
						)
						Samples._add_input(
								config,
								self.files_ewkz_znn(channel),
								self.root_file_folder(channel),
								lumi,
								mc_weight+"*"+weight+"*eventWeight*"+Samples.zll_genmatch(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=cut_type)+"*((q_1*q_2)>0.0)"+"*"+self.zll_zl_shape_weight(channel, cut_type)+"*"+self.ewkz_znn_stitchingweight()+"*"+zmm_cr_factor,
								("noplot_" if not controlregions else "") + "zll_ss_lowmt",
								nick_suffix=nick_suffix
						)
					Samples._add_input(
							config,
							self.files_zll(channel),
							self.root_file_folder(channel),
							lumi,
							mc_weight+"*"+weight+"*eventWeight*"+self.zll_stitchingweight()+"*"+Samples.zl_genmatch(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=cut_type)+"*((q_1*q_2)>0.0)"+"*zPtReweightWeight"+"*"+self.zl_shape_weight(channel, cut_type)+"*"+zmm_cr_factor,
							("noplot_" if not controlregions else "") + "zl_ss_lowmt",
							nick_suffix=nick_suffix
					)
					if not (kwargs.get("no_ewk_samples", False) or kwargs.get("no_ewkz_as_dy", False)):
						Samples._add_input(
								config,
								self.files_ewkz_zll(channel),
								self.root_file_folder(channel),
								lumi,
								mc_weight+"*"+weight+"*eventWeight*"+Samples.zl_genmatch(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=cut_type)+"*((q_1*q_2)>0.0)"+"*"+self.zl_shape_weight(channel, cut_type)+"*"+self.ewkz_zll_stitchingweight()+"*"+zmm_cr_factor,
								("noplot_" if not controlregions else "") + "zl_ss_lowmt",
								nick_suffix=nick_suffix
						)
						Samples._add_input(
								config,
								self.files_ewkz_znn(channel),
								self.root_file_folder(channel),
								lumi,
								mc_weight+"*"+weight+"*eventWeight*"+Samples.zl_genmatch(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=cut_type)+"*((q_1*q_2)>0.0)"+"*"+self.zl_shape_weight(channel, cut_type)+"*"+self.ewkz_znn_stitchingweight()+"*"+zmm_cr_factor,
								("noplot_" if not controlregions else "") + "zl_ss_lowmt",
								nick_suffix=nick_suffix
						)
					Samples._add_input(
							config,
							self.files_zll(channel),
							self.root_file_folder(channel),
							lumi,
							mc_weight+"*"+weight+"*eventWeight*"+self.zll_stitchingweight()+"*"+Samples.zj_genmatch(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=cut_type)+"*((q_1*q_2)>0.0)"+"*zPtReweightWeight"+"*"+zmm_cr_factor,
							("noplot_" if not controlregions else "") + "zj_ss_lowmt",
							nick_suffix=nick_suffix
					)
					if not (kwargs.get("no_ewk_samples", False) or kwargs.get("no_ewkz_as_dy", False)):
						Samples._add_input(
								config,
								self.files_ewkz_zll(channel),
								self.root_file_folder(channel),
								lumi,
								mc_weight+"*"+weight+"*eventWeight*"+Samples.zj_genmatch(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=cut_type)+"*((q_1*q_2)>0.0)"+"*"+self.ewkz_zll_stitchingweight()+"*"+zmm_cr_factor,
								("noplot_" if not controlregions else "") + "zj_ss_lowmt",
								nick_suffix=nick_suffix
						)
						Samples._add_input(
								config,
								self.files_ewkz_znn(channel),
								self.root_file_folder(channel),
								lumi,
								mc_weight+"*"+weight+"*eventWeight*"+Samples.zj_genmatch(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=cut_type)+"*((q_1*q_2)>0.0)"+"*"+self.ewkz_znn_stitchingweight()+"*"+zmm_cr_factor,
								("noplot_" if not controlregions else "") + "zj_ss_lowmt",
								nick_suffix=nick_suffix
						)
					if not kwargs.get("no_ewk_samples", False) and kwargs.get("no_ewkz_as_dy", False):
						Samples._add_input(
								config,
								self.files_ewkz_zll(channel),
								self.root_file_folder(channel),
								lumi,
								mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=cut_type)+"*((q_1*q_2)>0.0)"+"*"+self.ewkz_zll_stitchingweight()+"*"+zmm_cr_factor,
								("noplot_" if not controlregions else "") + "ewkz_ss_lowmt",
								nick_suffix=nick_suffix
						)
						Samples._add_input(
								config,
								self.files_ewkz_znn(channel),
								self.root_file_folder(channel),
								lumi,
								mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=cut_type)+"*((q_1*q_2)>0.0)"+"*"+self.ewkz_znn_stitchingweight()+"*"+zmm_cr_factor,
								("noplot_" if not controlregions else "") + "ewkz_ss_lowmt",
								nick_suffix=nick_suffix
						)
					Samples._add_input(
							config,
							self.files_ttj(channel),
							self.root_file_folder(channel),
							lumi,
							mc_weight+"*"+weight+"*eventWeight*"+self.embedding_ttbarveto_weight(channel)+"*"+Samples.ttt_genmatch(channel,kwargs)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=cut_type)+"*((q_1*q_2)>0.0)*topPtReweightWeight",
							("noplot_" if not controlregions else "") + "ttt_ss_lowmt",
							nick_suffix=nick_suffix
					)
					Samples._add_input(
							config,
							self.files_ttj(channel),
							self.root_file_folder(channel),
							lumi,
							mc_weight+"*"+weight+"*eventWeight*"+self.embedding_ttbarveto_weight(channel)+"*"+Samples.ttj_genmatch(channel,kwargs)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=cut_type)+"*((q_1*q_2)>0.0)*topPtReweightWeight",
							("noplot_" if not controlregions else "") + "ttjj_ss_lowmt",
							nick_suffix=nick_suffix
					)
					Samples._add_input(
							config,
							self.files_ttj(channel),
							self.root_file_folder(channel),
							lumi,
							mc_weight+"*"+weight+"*eventWeight*"+self.embedding_ttbarveto_weight(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=cut_type)+"*((q_1*q_2)>0.0)*topPtReweightWeight",
							("noplot_" if not controlregions else "") + "ttj_ss_lowmt",
							nick_suffix=nick_suffix
					)
					Samples._add_input(
							config,
							self.files_vv(channel),
							self.root_file_folder(channel),
							lumi,
							mc_weight+"*"+weight+"*eventWeight*"+Samples.ttt_genmatch(channel,kwargs)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=cut_type)+"*((q_1*q_2)>0.0)",
							("noplot_" if not controlregions else "") + "vvt_ss_lowmt",
							nick_suffix=nick_suffix
					)
					Samples._add_input(
							config,
							self.files_vv(channel),
							self.root_file_folder(channel),
							lumi,
							mc_weight+"*"+weight+"*eventWeight*"+Samples.ttj_genmatch(channel,kwargs)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=cut_type)+"*((q_1*q_2)>0.0)",
							("noplot_" if not controlregions else "") + "vvj_ss_lowmt",
							nick_suffix=nick_suffix
					)
					Samples._add_input(
							config,
							self.files_vv(channel),
							self.root_file_folder(channel),
							lumi,
							mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=cut_type)+"*((q_1*q_2)>0.0)",
							("noplot_" if not controlregions else "") + "vv_ss_lowmt",
							nick_suffix=nick_suffix
					)
					Samples._add_input(
							config,
							self.files_wj(channel),
							self.root_file_folder(channel),
							lumi,
							mc_weight+"*"+weight+"*eventWeight*"+self.wj_stitchingweight()+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=cut_type)+"*((q_1*q_2)>0.0)",
							("noplot_" if not controlregions else "") + "wj_ss_lowmt",
							nick_suffix=nick_suffix
					)
					if (not kwargs.get("no_ewk_samples", False)):
						Samples._add_input(
								config,
								self.files_ewkwm(channel),
								self.root_file_folder(channel),
								lumi,
								mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=cut_type)+"*((q_1*q_2)>0.0)"+"*"+self.ewkwm_stitchingweight(),
								("noplot_" if not controlregions else "") + "wj_ss_lowmt",
								nick_suffix=nick_suffix
						)
						Samples._add_input(
								config,
								self.files_ewkwp(channel),
								self.root_file_folder(channel),
								lumi,
								mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=cut_type)+"*((q_1*q_2)>0.0)"+"*"+self.ewkwp_stitchingweight(),
								("noplot_" if not controlregions else "") + "wj_ss_lowmt",
								nick_suffix=nick_suffix
						)
					Samples._add_input(
							config,
							self.files_data(channel),
							self.root_file_folder(channel),
							1.0,
							data_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=cut_type)+"*((q_1*q_2)>0.0)",
							("noplot_" if not controlregions else "") + "data_ss_lowmt",
							nick_suffix=nick_suffix
					)
					Samples._add_input(
							config,
							self.files_ztt(channel),
							self.root_file_folder(channel),
							lumi,
							Samples.ztt_genmatch(channel)+"*"+self.get_weights_ztt(channel=channel,cut_type=cut_type,weight=qcd_shape_weight)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os"]+exclude_cuts_relaxed, cut_type=qcd_shape_cut)+"*((q_1*q_2)>0.0)"+"*zPtReweightWeight"+"*"+zmm_cr_factor,
							"noplot_ztt_shape_ss_qcd_control",
							nick_suffix=nick_suffix
					)
					if not (kwargs.get("no_ewk_samples", False) or kwargs.get("no_ewkz_as_dy", False)):
						Samples._add_input(
								config,
								self.files_ewkz_zll(channel),
								self.root_file_folder(channel),
								lumi,
								Samples.ztt_genmatch(channel)+"*"+self.get_weights_ztt(channel=channel,cut_type=cut_type,weight=qcd_shape_weight,doStitching=False)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os"]+exclude_cuts_relaxed, cut_type=qcd_shape_cut)+"*((q_1*q_2)>0.0)"+"*"+self.ewkz_zll_stitchingweight()+"*"+zmm_cr_factor,
								"noplot_ztt_shape_ss_qcd_control",
								nick_suffix=nick_suffix
						)
						Samples._add_input(
								config,
								self.files_ewkz_znn(channel),
								self.root_file_folder(channel),
								lumi,
								Samples.ztt_genmatch(channel)+"*"+self.get_weights_ztt(channel=channel,cut_type=cut_type,weight=qcd_shape_weight,doStitching=False)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os"]+exclude_cuts_relaxed, cut_type=qcd_shape_cut)+"*((q_1*q_2)>0.0)"+"*"+self.ewkz_znn_stitchingweight()+"*"+zmm_cr_factor,
								"noplot_ztt_shape_ss_qcd_control",
								nick_suffix=nick_suffix
						)
					Samples._add_input(
							config,
							self.files_zll(channel),
							self.root_file_folder(channel),
							lumi,
							mc_weight+"*"+qcd_shape_weight+"*eventWeight*"+self.zll_stitchingweight()+"*"+Samples.zll_genmatch(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os"]+exclude_cuts_relaxed, cut_type=qcd_shape_cut)+"*((q_1*q_2)>0.0)"+"*zPtReweightWeight"+"*"+self.zll_zl_shape_weight(channel, cut_type)+"*"+zmm_cr_factor,
							"noplot_zll_shape_ss_qcd_control",
							nick_suffix=nick_suffix
					)
					if not (kwargs.get("no_ewk_samples", False) or kwargs.get("no_ewkz_as_dy", False)):
						Samples._add_input(
								config,
								self.files_ewkz_zll(channel),
								self.root_file_folder(channel),
								lumi,
								mc_weight+"*"+qcd_shape_weight+"*eventWeight*"+Samples.zll_genmatch(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os"]+exclude_cuts_relaxed, cut_type=qcd_shape_cut)+"*((q_1*q_2)>0.0)"+"*"+self.zll_zl_shape_weight(channel, cut_type)+"*"+self.ewkz_zll_stitchingweight()+"*"+zmm_cr_factor,
								"noplot_zll_shape_ss_qcd_control",
								nick_suffix=nick_suffix
						)
						Samples._add_input(
								config,
								self.files_ewkz_znn(channel),
								self.root_file_folder(channel),
								lumi,
								mc_weight+"*"+qcd_shape_weight+"*eventWeight*"+Samples.zll_genmatch(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os"]+exclude_cuts_relaxed, cut_type=qcd_shape_cut)+"*((q_1*q_2)>0.0)"+"*"+self.zll_zl_shape_weight(channel, cut_type)+"*"+self.ewkz_znn_stitchingweight()+"*"+zmm_cr_factor,
								"noplot_zll_shape_ss_qcd_control",
								nick_suffix=nick_suffix
						)
					if not kwargs.get("no_ewk_samples", False) and kwargs.get("no_ewkz_as_dy", False):
						Samples._add_input(
								config,
								self.files_ewkz_zll(channel),
								self.root_file_folder(channel),
								lumi,
								mc_weight+"*"+qcd_shape_weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os"]+exclude_cuts_relaxed, cut_type=qcd_shape_cut)+"*((q_1*q_2)>0.0)"+"*"+self.ewkz_zll_stitchingweight()+"*"+zmm_cr_factor,
								"noplot_ewkz_shape_ss_qcd_control",
								nick_suffix=nick_suffix
						)
						Samples._add_input(
								config,
								self.files_ewkz_znn(channel),
								self.root_file_folder(channel),
								lumi,
								mc_weight+"*"+qcd_shape_weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os"]+exclude_cuts_relaxed, cut_type=qcd_shape_cut)+"*((q_1*q_2)>0.0)"+"*"+self.ewkz_znn_stitchingweight()+"*"+zmm_cr_factor,
								"noplot_ewkz_shape_ss_qcd_control",
								nick_suffix=nick_suffix
						)
					Samples._add_input(
							config,
							self.files_ttj(channel),
							self.root_file_folder(channel),
							lumi,
							mc_weight+"*"+qcd_shape_weight+"*eventWeight*"+self.embedding_ttbarveto_weight(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os"]+exclude_cuts_relaxed, cut_type=qcd_shape_cut)+"*((q_1*q_2)>0.0)*topPtReweightWeight",
							"noplot_ttj_shape_ss_qcd_control",
							nick_suffix=nick_suffix
					)
					Samples._add_input(
							config,
							self.files_vv(channel),
							self.root_file_folder(channel),
							lumi,
							mc_weight+"*"+qcd_shape_weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os"]+exclude_cuts_relaxed, cut_type=qcd_shape_cut)+"*((q_1*q_2)>0.0)",
							"noplot_vv_shape_ss_qcd_control",
							nick_suffix=nick_suffix
					)
					Samples._add_input(
							config,
							self.files_wj(channel),
							self.root_file_folder(channel),
							lumi,
							mc_weight+"*"+qcd_shape_weight+"*eventWeight*"+self.wj_stitchingweight()+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os"]+exclude_cuts_relaxed, cut_type=qcd_shape_cut)+"*((q_1*q_2)>0.0)",
							"noplot_wj_shape_ss_qcd_control",
							nick_suffix=nick_suffix
					)
					if (not kwargs.get("no_ewk_samples", False)):
						Samples._add_input(
								config,
								self.files_ewkwm(channel),
								self.root_file_folder(channel),
								lumi,
								mc_weight+"*"+qcd_shape_weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os"]+exclude_cuts_relaxed, cut_type=qcd_shape_cut)+"*((q_1*q_2)>0.0)"+"*"+self.ewkwm_stitchingweight(),
								"noplot_wj_shape_ss_qcd_control",
								nick_suffix=nick_suffix
						)
						Samples._add_input(
								config,
								self.files_ewkwp(channel),
								self.root_file_folder(channel),
								lumi,
								mc_weight+"*"+qcd_shape_weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os"]+exclude_cuts_relaxed, cut_type=qcd_shape_cut)+"*((q_1*q_2)>0.0)"+"*"+self.ewkwp_stitchingweight(),
								"noplot_wj_shape_ss_qcd_control",
								nick_suffix=nick_suffix
						)
					Samples._add_input(
							config,
							self.files_data(channel),
							self.root_file_folder(channel),
							1.0,
							data_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_high_mt_ss, cut_type=high_mt_ss_cut_type),
							("noplot_" if not controlregions else "") + "qcd_ss_highmt",
							nick_suffix=nick_suffix
					)
					Samples._add_input(
							config,
							self.files_ztt(channel),
							self.root_file_folder(channel),
							lumi,
							Samples.ztt_genmatch(channel)+"*"+self.get_weights_ztt(channel=channel,cut_type=cut_type,weight=weight)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_high_mt_ss, cut_type=high_mt_ss_cut_type)+"*zPtReweightWeight"+"*"+zmm_cr_factor,
							"noplot_ztt_shape_ss_highmt",
							nick_suffix=nick_suffix
					)
					if not (kwargs.get("no_ewk_samples", False) or kwargs.get("no_ewkz_as_dy", False)):
						Samples._add_input(
								config,
								self.files_ewkz_zll(channel),
								self.root_file_folder(channel),
								lumi,
								Samples.ztt_genmatch(channel)+"*"+self.get_weights_ztt(channel=channel,cut_type=cut_type,weight=weight,doStitching=False)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_high_mt_ss, cut_type=high_mt_ss_cut_type)+"*"+self.ewkz_zll_stitchingweight()+"*"+zmm_cr_factor,
								"noplot_ztt_shape_ss_highmt",
								nick_suffix=nick_suffix
						)
						Samples._add_input(
								config,
								self.files_ewkz_znn(channel),
								self.root_file_folder(channel),
								lumi,
								Samples.ztt_genmatch(channel)+"*"+self.get_weights_ztt(channel=channel,cut_type=cut_type,weight=weight,doStitching=False)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_high_mt_ss, cut_type=high_mt_ss_cut_type)+"*"+self.ewkz_znn_stitchingweight()+"*"+zmm_cr_factor,
								"noplot_ztt_shape_ss_highmt",
								nick_suffix=nick_suffix
						)
					Samples._add_input(
							config,
							self.files_zll(channel),
							self.root_file_folder(channel),
							lumi,
							mc_weight+"*"+weight+"*eventWeight*"+self.zll_stitchingweight()+"*"+Samples.zll_genmatch(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_high_mt_ss, cut_type=high_mt_ss_cut_type)+"*zPtReweightWeight"+"*"+self.zll_zl_shape_weight(channel, cut_type)+"*"+zmm_cr_factor,
							"noplot_zll_shape_ss_highmt",
							nick_suffix=nick_suffix
					)
					if not (kwargs.get("no_ewk_samples", False) or kwargs.get("no_ewkz_as_dy", False)):
						Samples._add_input(
								config,
								self.files_ewkz_zll(channel),
								self.root_file_folder(channel),
								lumi,
								mc_weight+"*"+weight+"*eventWeight*"+Samples.zll_genmatch(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_high_mt_ss, cut_type=high_mt_ss_cut_type)+"*"+self.zll_zl_shape_weight(channel, cut_type)+"*"+self.ewkz_zll_stitchingweight()+"*"+zmm_cr_factor,
								"noplot_zll_shape_ss_highmt",
								nick_suffix=nick_suffix
						)
						Samples._add_input(
								config,
								self.files_ewkz_znn(channel),
								self.root_file_folder(channel),
								lumi,
								mc_weight+"*"+weight+"*eventWeight*"+Samples.zll_genmatch(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_high_mt_ss, cut_type=high_mt_ss_cut_type)+"*"+self.zll_zl_shape_weight(channel, cut_type)+"*"+self.ewkz_znn_stitchingweight()+"*"+zmm_cr_factor,
								"noplot_zll_shape_ss_highmt",
								nick_suffix=nick_suffix
						)
					if not kwargs.get("no_ewk_samples", False) and kwargs.get("no_ewkz_as_dy", False):
						Samples._add_input(
								config,
								self.files_ewkz_zll(channel),
								self.root_file_folder(channel),
								lumi,
								mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_high_mt_ss, cut_type=high_mt_ss_cut_type)+"*"+self.ewkz_zll_stitchingweight()+"*"+zmm_cr_factor,
								"noplot_ewkz_shape_ss_highmt",
								nick_suffix=nick_suffix
						)
						Samples._add_input(
								config,
								self.files_ewkz_znn(channel),
								self.root_file_folder(channel),
								lumi,
								mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_high_mt_ss, cut_type=high_mt_ss_cut_type)+"*"+self.ewkz_znn_stitchingweight()+"*"+zmm_cr_factor,
								"noplot_ewkz_shape_ss_highmt",
								nick_suffix=nick_suffix
						)
					Samples._add_input(
							config,
							self.files_ttj(channel),
							self.root_file_folder(channel),
							lumi,
							mc_weight+"*"+weight+"*eventWeight*"+self.embedding_ttbarveto_weight(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_high_mt_ss, cut_type=high_mt_ss_cut_type)+"*topPtReweightWeight",
							"noplot_ttj_shape_ss_highmt",
							nick_suffix=nick_suffix
					)
					Samples._add_input(
							config,
							self.files_vv(channel),
							self.root_file_folder(channel),
							lumi,
							mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_high_mt_ss, cut_type=high_mt_ss_cut_type),
							"noplot_vv_shape_ss_highmt",
							nick_suffix=nick_suffix
					)
					Samples._add_input(
							config,
							self.files_data(channel),
							self.root_file_folder(channel),
							1.0,
							data_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_high_mt_ss, cut_type=high_mt_ss_cut_type),
							("noplot_" if not controlregions else "") + "qcd_os_highmt",
							nick_suffix=nick_suffix
					)
					Samples._add_input(
							config,
							self.files_data(channel),
							self.root_file_folder(channel),
							1.0,
							data_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=cut_type)+"*((q_1*q_2)>0.0)",
							("noplot_" if not controlregions else "") + "qcd_ss_lowmt",
							nick_suffix=nick_suffix
					)
					Samples._add_input(
							config,
							self.files_data(channel),
							self.root_file_folder(channel),
							1.0,
							data_weight+"*"+qcd_shape_weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os"]+exclude_cuts_relaxed, cut_type=qcd_shape_cut)+"*((q_1*q_2)>0.0)",
							"qcd",
							nick_suffix=nick_suffix
					)
					if kwargs.get("ss_os_factor", 0.0) != 0.0:
						ss_os_factor = kwargs["ss_os_factor"]
					else:
						ss_os_factor = 1.0
						if category != None:
							if channel == "et":
								ss_os_factor = 1.28 if "Boosted2D" in category else 1.0 if "Vbf2D" in category else 1.0 if "ZeroJet2D" in category else 1.0
							elif channel == "mt":
								ss_os_factor = 1.06 if "Boosted2D" in category else 1.0 if "Vbf2D" in category else 1.07 if "ZeroJet2D" in category else 1.0
					if not "EstimateWjetsAndQCD" in config.get("analysis_modules", []):
						config.setdefault("analysis_modules", []).append("EstimateWjetsAndQCD")
					elif channel == "et":
						config.setdefault("qcd_extrapolation_factors_ss_os", []).append(ss_os_factor)
					elif channel == "mt":
						config.setdefault("qcd_extrapolation_factors_ss_os", []).append(ss_os_factor)
					if controlregions:
						config.setdefault("qcd_shape_nicks", []).append("qcd"+nick_suffix)
						config.setdefault("qcd_yield_nicks", []).append("data_ss_lowmt"+nick_suffix)
						if not kwargs.get("no_ewk_samples", False) and kwargs.get("no_ewkz_as_dy", False):
							config.setdefault("qcd_yield_substract_nicks", []).append(" ".join([nick+nick_suffix for nick in "ztt_ss_lowmt zll_ss_lowmt ewkz_ss_lowmt ttj_ss_lowmt vv_ss_lowmt wj_ss_lowmt".split()]))
							config.setdefault("qcd_shape_substract_nicks", []).append(" ".join([nick+nick_suffix for nick in "noplot_ztt_shape_ss_qcd_control noplot_zll_shape_ss_qcd_control noplot_ewkz_shape_ss_qcd_control noplot_ttj_shape_ss_qcd_control noplot_vv_shape_ss_qcd_control noplot_wj_shape_ss_qcd_control".split()]))
							config.setdefault("qcd_shape_highmt_substract_nicks", []).append(" ".join([nick+nick_suffix for nick in "noplot_ztt_shape_ss_highmt noplot_zll_shape_ss_highmt noplot_ewkz_shape_ss_highmt noplot_ttj_shape_ss_highmt noplot_vv_shape_ss_highmt".split()]))
						else:
							config.setdefault("qcd_yield_substract_nicks", []).append(" ".join([nick+nick_suffix for nick in "ztt_ss_lowmt zll_ss_lowmt ttj_ss_lowmt vv_ss_lowmt wj_ss_lowmt".split()]))
							config.setdefault("qcd_shape_substract_nicks", []).append(" ".join([nick+nick_suffix for nick in "noplot_ztt_shape_ss_qcd_control noplot_zll_shape_ss_qcd_control noplot_ttj_shape_ss_qcd_control noplot_vv_shape_ss_qcd_control noplot_wj_shape_ss_qcd_control".split()]))
							config.setdefault("qcd_shape_highmt_substract_nicks", []).append(" ".join([nick+nick_suffix for nick in "noplot_ztt_shape_ss_highmt noplot_zll_shape_ss_highmt noplot_ttj_shape_ss_highmt noplot_vv_shape_ss_highmt".split()]))
						config.setdefault("qcd_ss_highmt_shape_nicks", []).append("qcd_ss_highmt"+nick_suffix)
						config.setdefault("qcd_ss_lowmt_nicks", []).append("qcd_ss_lowmt"+nick_suffix)
						config.setdefault("qcd_os_highmt_nicks", []).append("qcd_os_highmt"+nick_suffix)
						if kwargs.get("wj_sf_shift", 0.0) != 0.0:
							config.setdefault("wjets_scale_factor_shifts", []).append(kwargs["wj_sf_shift"])

						for nick in ["ztt_ss_lowmt", "zll_ss_lowmt", "zl_ss_lowmt", "zj_ss_lowmt", "ttt_ss_lowmt", "ttjj_ss_lowmt", "ttj_ss_lowmt", "vvt_ss_lowmt", "vvj_ss_lowmt", "vv_ss_lowmt", "wj_ss_lowmt","data_ss_lowmt", "qcd_ss_highmt", "qcd_os_highmt", "qcd_ss_lowmt"]+(["ewkz_ss_lowmt"] if (not kwargs.get("no_ewk_samples", False) and kwargs.get("no_ewkz_as_dy", False)) else []):
							if not kwargs.get("mssm", False):
								Samples._add_bin_corrections(config, nick, nick_suffix)
							Samples._add_plot(config, "bkg", "HIST", "F", nick, nick_suffix)
					else:
						config.setdefault("qcd_shape_nicks", []).append("qcd"+nick_suffix)
						config.setdefault("qcd_yield_nicks", []).append("noplot_data_ss_lowmt"+nick_suffix)
						if not kwargs.get("no_ewk_samples", False) and kwargs.get("no_ewkz_as_dy", False):
							config.setdefault("qcd_yield_substract_nicks", []).append(" ".join(["noplot_"+nick+nick_suffix for nick in "ztt_ss_lowmt zll_ss_lowmt ewkz_ss_lowmt ttj_ss_lowmt vv_ss_lowmt wj_ss_lowmt".split()]))
							config.setdefault("qcd_shape_substract_nicks", []).append(" ".join([nick+nick_suffix for nick in "noplot_ztt_shape_ss_qcd_control noplot_zll_shape_ss_qcd_control noplot_ewkz_shape_ss_qcd_control noplot_ttj_shape_ss_qcd_control noplot_vv_shape_ss_qcd_control noplot_wj_shape_ss_qcd_control".split()]))
							config.setdefault("qcd_shape_highmt_substract_nicks", []).append(" ".join([nick+nick_suffix for nick in "noplot_ztt_shape_ss_highmt noplot_zll_shape_ss_highmt noplot_ewkz_shape_ss_highmt noplot_ttj_shape_ss_highmt noplot_vv_shape_ss_highmt".split()]))
						else:
							config.setdefault("qcd_yield_substract_nicks", []).append(" ".join(["noplot_"+nick+nick_suffix for nick in "ztt_ss_lowmt zll_ss_lowmt ttj_ss_lowmt vv_ss_lowmt wj_ss_lowmt".split()]))
							config.setdefault("qcd_shape_substract_nicks", []).append(" ".join([nick+nick_suffix for nick in "noplot_ztt_shape_ss_qcd_control noplot_zll_shape_ss_qcd_control noplot_ttj_shape_ss_qcd_control noplot_vv_shape_ss_qcd_control noplot_wj_shape_ss_qcd_control".split()]))
							config.setdefault("qcd_shape_highmt_substract_nicks", []).append(" ".join([nick+nick_suffix for nick in "noplot_ztt_shape_ss_highmt noplot_zll_shape_ss_highmt noplot_ttj_shape_ss_highmt noplot_vv_shape_ss_highmt".split()]))
						config.setdefault("qcd_ss_highmt_shape_nicks", []).append("noplot_qcd_ss_highmt"+nick_suffix)
						config.setdefault("qcd_ss_lowmt_nicks", []).append("noplot_qcd_ss_lowmt"+nick_suffix)
						config.setdefault("qcd_os_highmt_nicks", []).append("noplot_qcd_os_highmt"+nick_suffix)
						if kwargs.get("wj_sf_shift", 0.0) != 0.0:
							config.setdefault("wjets_scale_factor_shifts", []).append(kwargs["wj_sf_shift"])
				if channel == "em" or channel == "ttbar":
					for estimation_type in ["shape", "yield"]:
						qcd_weight = weight
						qcd_shape_cut = cut_type
						qcd_exclude_cuts = copy.deepcopy(exclude_cuts)+["os"]
						if category != None:
							if estimation_type == "shape" and ("ZeroJet2D" in category or "Boosted2D" in category):
								qcd_weight += "*(iso_1<0.3)*(iso_2>0.1)*(iso_2<0.3)"
								qcd_exclude_cuts += ["iso_1", "iso_2"]
							if estimation_type == "shape" and "Vbf2D" in category:
								qcd_weight += "*(iso_1<0.5)*(iso_2>0.2)*(iso_2<0.5)"
								qcd_exclude_cuts += ["iso_1", "iso_2"]
							if "newKIT" in estimationMethod and estimation_type == "shape": # take shape from full jet-bin
								qcd_shape_cut = qcd_shape_cut + ("relaxedETauMuTauWJ" if ("1jet" in category or "vbf" in category) else "")
								qcd_exclude_cuts.append("pzeta")
								qcd_weight = make_multiplication(Samples.get_jetbin(channel, category, weight))
						data_sample_weight = make_multiplication([data_weight, 
											  qcd_weight,
											  "eventWeight",
											  self._cut_string(channel, exclude_cuts=qcd_exclude_cuts, cut_type=qcd_shape_cut),
											  "((q_1*q_2)>0.0)",
											  "emuQcdWeightNom"])
						mc_sample_weight = make_multiplication([  mc_weight,
											  qcd_weight,
											  "eventWeight",
											  self._cut_string(channel, exclude_cuts=qcd_exclude_cuts, cut_type=qcd_shape_cut),
											  "((q_1*q_2)>0.0)",
											  "emuQcdWeightNom"])
						Samples._add_input(
								config,
								self.files_wj(channel),
								self.root_file_folder(channel),
								lumi,
								mc_sample_weight+"*"+self.wj_stitchingweight(),
								"noplot_wj_"+estimation_type,
								nick_suffix=nick_suffix
						)
						if (not kwargs.get("no_ewk_samples", False)):
							Samples._add_input(
									config,
									self.files_ewkwm(channel),
									self.root_file_folder(channel),
									lumi,
									mc_sample_weight+"*"+self.ewkwm_stitchingweight(),
									"noplot_wj_"+estimation_type,
									nick_suffix=nick_suffix
							)
							Samples._add_input(
									config,
									self.files_ewkwp(channel),
									self.root_file_folder(channel),
									lumi,
									mc_sample_weight+"*"+self.ewkwp_stitchingweight(),
									"noplot_wj_"+estimation_type,
									nick_suffix=nick_suffix
							)
						Samples._add_input(
								config,
								self.files_wgamma(channel),
								self.root_file_folder(channel),
								lumi,
								mc_sample_weight,
								"noplot_wj_"+estimation_type,
								nick_suffix=nick_suffix
						)
						Samples._add_input(
								config,
								self.files_data(channel),
								self.root_file_folder(channel),
								1.0,
								data_sample_weight,
								("qcd" if estimation_type=="shape" else "noplot_qcd_"+estimation_type),
								nick_suffix=nick_suffix
						)
						Samples._add_input(
								config,
								self.files_ztt(channel),
								self.root_file_folder(channel),
								lumi,
								Samples.ztt_genmatch(channel)+"*"+self.get_weights_ztt(channel=channel,cut_type=cut_type,mc_sample_weight=mc_sample_weight)+"*zPtReweightWeight"+"*"+zmm_cr_factor,
								"noplot_ztt_"+estimation_type,
								nick_suffix=nick_suffix
						)
						if not (kwargs.get("no_ewk_samples", False) or kwargs.get("no_ewkz_as_dy", False)):
							Samples._add_input(
									config,
									self.files_ewkz_zll(channel),
									self.root_file_folder(channel),
									lumi,
									Samples.ztt_genmatch(channel)+"*"+self.get_weights_ztt(channel=channel,cut_type=cut_type,mc_sample_weight=mc_sample_weight, doStitching=False)+"*"+self.ewkz_zll_stitchingweight()+"*"+zmm_cr_factor,
									"noplot_ztt_"+estimation_type,
									nick_suffix=nick_suffix
							)
							Samples._add_input(
									config,
									self.files_ewkz_znn(channel),
									self.root_file_folder(channel),
									lumi,
									Samples.ztt_genmatch(channel)+"*"+self.get_weights_ztt(channel=channel,cut_type=cut_type,mc_sample_weight=mc_sample_weight, doStitching=False)+"*"+self.ewkz_znn_stitchingweight()+"*"+zmm_cr_factor,
									"noplot_ztt_"+estimation_type,
									nick_suffix=nick_suffix
							)
						Samples._add_input(
								config,
								self.files_zll(channel),
								self.root_file_folder(channel),
								lumi,
								self.zll_stitchingweight()+"*"+Samples.zll_genmatch(channel)+"*"+mc_sample_weight+"*zPtReweightWeight"+"*"+self.zll_zl_shape_weight(channel, cut_type)+"*"+zmm_cr_factor,
								"noplot_zll_"+estimation_type,
								nick_suffix=nick_suffix
						)
						if not (kwargs.get("no_ewk_samples", False) or kwargs.get("no_ewkz_as_dy", False)):
							Samples._add_input(
									config,
									self.files_ewkz_zll(channel),
									self.root_file_folder(channel),
									lumi,
									Samples.zll_genmatch(channel)+"*"+mc_sample_weight+"*"+self.zll_zl_shape_weight(channel, cut_type)+"*"+self.ewkz_zll_stitchingweight()+"*"+zmm_cr_factor,
									"noplot_zll_"+estimation_type,
									nick_suffix=nick_suffix
							)
							Samples._add_input(
									config,
									self.files_ewkz_znn(channel),
									self.root_file_folder(channel),
									lumi,
									Samples.zll_genmatch(channel)+"*"+mc_sample_weight+"*"+self.zll_zl_shape_weight(channel, cut_type)+"*"+self.ewkz_znn_stitchingweight()+"*"+zmm_cr_factor,
									"noplot_zll_"+estimation_type,
									nick_suffix=nick_suffix
							)
						if not kwargs.get("no_ewk_samples", False) and kwargs.get("no_ewkz_as_dy", False):
							Samples._add_input(
									config,
									self.files_ewkz_zll(channel),
									self.root_file_folder(channel),
									lumi,
									mc_sample_weight+"*"+self.ewkz_zll_stitchingweight()+"*"+zmm_cr_factor,
									"noplot_ewkz_"+estimation_type,
									nick_suffix=nick_suffix
							)
							Samples._add_input(
									config,
									self.files_ewkz_znn(channel),
									self.root_file_folder(channel),
									lumi,
									mc_sample_weight+"*"+self.ewkz_znn_stitchingweight()+"*"+zmm_cr_factor,
									"noplot_ewkz_"+estimation_type,
									nick_suffix=nick_suffix
							)
						Samples._add_input(
								config,
								self.files_ttj(channel),
								self.root_file_folder(channel),
								lumi,
								mc_sample_weight+"*"+self.embedding_ttbarveto_weight(channel)+"*topPtReweightWeight",
								"noplot_ttj_"+estimation_type,
								nick_suffix=nick_suffix
						)
						Samples._add_input(
								config,
								self.files_vv(channel),
								self.root_file_folder(channel),
								lumi,
								mc_sample_weight,
								"noplot_vv_"+estimation_type,
								nick_suffix=nick_suffix
						)
					if not "EstimateQcd" in config.get("analysis_modules", []):
						config.setdefault("analysis_modules", []).append("EstimateQcd")
					config.setdefault("qcd_shape_nicks", []).append("qcd"+nick_suffix)
					config.setdefault("qcd_yield_nicks", []).append("noplot_qcd_yield"+nick_suffix)
					if not kwargs.get("no_ewk_samples", False) and kwargs.get("no_ewkz_as_dy", False):
						config.setdefault("qcd_yield_subtract_nicks", []).append(" ".join(["noplot_"+nick+"_yield"+nick_suffix for nick in "ztt zll ewkz ttj vv wj".split()]))
						config.setdefault("qcd_shape_subtract_nicks", []).append(" ".join(["noplot_"+nick+"_shape"+nick_suffix for nick in "ztt zll ewkz ttj vv wj".split()]))
					else:
						config.setdefault("qcd_yield_subtract_nicks", []).append(" ".join(["noplot_"+nick+"_yield"+nick_suffix for nick in "ztt zll ttj vv wj".split()]))
						config.setdefault("qcd_shape_subtract_nicks", []).append(" ".join(["noplot_"+nick+"_shape"+nick_suffix for nick in "ztt zll ttj vv wj".split()]))
					if kwargs.get("ss_os_factor", 0.0) != 0.0:
						ss_os_factor = kwargs["ss_os_factor"]
					else:
						ss_os_factor = 1.0
						if category != None:
							ss_os_factor = 1.8 if "ZeroJet2D" in category else 1.89 if "Boosted2D" in category else 1.74 if "Vbf2D" in category else 1.0
					config.setdefault("qcd_extrapolation_factors_ss_os", []).append(ss_os_factor)
				if channel == "tt":
					if cut_type == "baseline2016":
						isolationDefinition = "((byMediumIsolationMVArun2v1DBoldDMwLT_1 > 0.5 && byLooseIsolationMVArun2v1DBoldDMwLT_2 > 0.5 && byTightIsolationMVArun2v1DBoldDMwLT_2 < 0.5) || (byMediumIsolationMVArun2v1DBoldDMwLT_2 > 0.5 && byLooseIsolationMVArun2v1DBoldDMwLT_1 > 0.5 && byTightIsolationMVArun2v1DBoldDMwLT_1 < 0.5))"
					elif cut_type == "smhtt2016" or cut_type == "smhtt2016newTauId":
						isolationDefinition = "((byMediumIsolationMVArun2v1DBoldDMwLT_1 > 0.5 && byLooseIsolationMVArun2v1DBoldDMwLT_2 > 0.5 && byTightIsolationMVArun2v1DBoldDMwLT_2 < 0.5) || (byMediumIsolationMVArun2v1DBoldDMwLT_2 > 0.5 && byLooseIsolationMVArun2v1DBoldDMwLT_1 > 0.5 && byTightIsolationMVArun2v1DBoldDMwLT_1 < 0.5))*((gen_match_1 == 5)*0.95 + (gen_match_1 != 5))*((gen_match_2 == 5)*0.95 + (gen_match_2 != 5))"
					else:
						isolationDefinition = "(byMediumIsolationMVArun2v1DBoldDMwLT_1 > 0.5 && byLooseIsolationMVArun2v1DBoldDMwLT_2 > 0.5 && byVTightIsolationMVArun2v1DBoldDMwLT_2 < 0.5)"
					data_selection_weights = {
						"qcd_shape" : data_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["iso_1", "iso_2"], cut_type=cut_type)+"*"+isolationDefinition,
						"qcd_signal_ss" : data_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=cut_type)+"*((q_1*q_2)>0.0)",
						"qcd_relaxed_ss" : data_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os", "iso_1", "iso_2"], cut_type=cut_type)+"*((q_1*q_2)>0.0)"+"*"+isolationDefinition
						}
					mc_selection_weights = {
						"qcd_shape" : mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["iso_1", "iso_2"], cut_type=cut_type)+"*"+isolationDefinition,
						"qcd_signal_ss" : mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=cut_type)+"*((q_1*q_2)>0.0)",
						"qcd_relaxed_ss" : mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os", "iso_1", "iso_2"], cut_type=cut_type)+"*((q_1*q_2)>0.0)"+"*"+isolationDefinition
						}
					for key in mc_selection_weights:
						Samples._add_input(
								config,
								self.files_wj(channel),
								self.root_file_folder(channel),
								lumi,
								self.wj_stitchingweight()+"*"+mc_selection_weights[key],
								"noplot_wj_"+key,
								nick_suffix=nick_suffix
						)
						if (not kwargs.get("no_ewk_samples", False)):
							Samples._add_input(
									config,
									self.files_ewkwm(channel),
									self.root_file_folder(channel),
									lumi,
									mc_selection_weights[key]+"*"+self.ewkwm_stitchingweight(),
									"noplot_wj_"+key,
									nick_suffix=nick_suffix
							)
							Samples._add_input(
									config,
									self.files_ewkwp(channel),
									self.root_file_folder(channel),
									lumi,
									mc_selection_weights[key]+"*"+self.ewkwp_stitchingweight(),
									"noplot_wj_"+key,
									nick_suffix=nick_suffix
							)
						Samples._add_input(
								config,
								self.files_data(channel),
								self.root_file_folder(channel),
								1.0,
								data_selection_weights[key],
								"qcd" if key == "qcd_shape" else "noplot_data_"+key,
								nick_suffix=nick_suffix
						)
						Samples._add_input(
								config,
								self.files_ztt(channel),
								self.root_file_folder(channel),
								lumi,
								Samples.ztt_genmatch(channel)+"*"+self.get_weights_ztt(channel=channel,cut_type=cut_type,mc_sample_weight=mc_selection_weights[key])+"*zPtReweightWeight"+"*"+zmm_cr_factor,
								"noplot_ztt_"+key,
								nick_suffix=nick_suffix
						)
						if not (kwargs.get("no_ewk_samples", False) or kwargs.get("no_ewkz_as_dy", False)):
							Samples._add_input(
									config,
									self.files_ewkz_zll(channel),
									self.root_file_folder(channel),
									lumi,
									Samples.ztt_genmatch(channel)+"*"+self.get_weights_ztt(channel=channel,cut_type=cut_type,mc_sample_weight=mc_selection_weights[key], doStitching=False)+"*"+self.ewkz_zll_stitchingweight()+"*"+zmm_cr_factor,
									"noplot_ztt_"+key,
									nick_suffix=nick_suffix
							)
							Samples._add_input(
									config,
									self.files_ewkz_znn(channel),
									self.root_file_folder(channel),
									lumi,
									Samples.ztt_genmatch(channel)+"*"+self.get_weights_ztt(channel=channel,cut_type=cut_type,mc_sample_weight=mc_selection_weights[key], doStitching=False)+"*"+self.ewkz_znn_stitchingweight()+"*"+zmm_cr_factor,
									"noplot_ztt_"+key,
									nick_suffix=nick_suffix
							)
						Samples._add_input(
								config,
								self.files_zll(channel),
								self.root_file_folder(channel),
								lumi,
								mc_selection_weights[key]+"*"+self.zll_stitchingweight()+"*"+Samples.zll_genmatch(channel)+"*"+"zPtReweightWeight"+"*"+self.zll_zl_shape_weight(channel, cut_type)+"*"+zmm_cr_factor,
								"noplot_zll_"+key,
								nick_suffix=nick_suffix
						)
						if not (kwargs.get("no_ewk_samples", False) or kwargs.get("no_ewkz_as_dy", False)):
							Samples._add_input(
									config,
									self.files_ewkz_zll(channel),
									self.root_file_folder(channel),
									lumi,
									mc_selection_weights[key]+"*"+Samples.zll_genmatch(channel)+"*"+self.zll_zl_shape_weight(channel, cut_type)+"*"+self.ewkz_zll_stitchingweight()+"*"+zmm_cr_factor,
									"noplot_zll_"+key,
									nick_suffix=nick_suffix
							)
							Samples._add_input(
									config,
									self.files_ewkz_znn(channel),
									self.root_file_folder(channel),
									lumi,
									mc_selection_weights[key]+"*"+Samples.zll_genmatch(channel)+"*"+self.zll_zl_shape_weight(channel, cut_type)+"*"+self.ewkz_znn_stitchingweight()+"*"+zmm_cr_factor,
									"noplot_zll_"+key,
									nick_suffix=nick_suffix
							)
						if not kwargs.get("no_ewk_samples", False) and kwargs.get("no_ewkz_as_dy", False):
							Samples._add_input(
									config,
									self.files_ewkz_zll(channel),
									self.root_file_folder(channel),
									lumi,
									mc_selection_weights[key]+"*"+self.ewkz_zll_stitchingweight()+"*"+zmm_cr_factor,
									"noplot_ewkz_"+key,
									nick_suffix=nick_suffix
							)
							Samples._add_input(
									config,
									self.files_ewkz_znn(channel),
									self.root_file_folder(channel),
									lumi,
									mc_selection_weights[key]+"*"+self.ewkz_znn_stitchingweight()+"*"+zmm_cr_factor,
									"noplot_ewkz_"+key,
									nick_suffix=nick_suffix
							)
						Samples._add_input(
								config,
								self.files_ttj(channel),
								self.root_file_folder(channel),
								lumi,
								mc_selection_weights[key]+"*"+self.embedding_ttbarveto_weight(channel)+"*topPtReweightWeight",
								"noplot_ttj_"+key,
								nick_suffix=nick_suffix
						)
						Samples._add_input(
								config,
								self.files_vv(channel),
								self.root_file_folder(channel),
								lumi,
								mc_selection_weights[key],
								"noplot_vv_"+key,
								nick_suffix=nick_suffix
						)
					if not "EstimateQcdTauHadTauHad" in config.get("analysis_modules", []):
						config.setdefault("analysis_modules", []).append("EstimateQcdTauHadTauHad")
					config.setdefault("qcd_data_shape_nicks", []).append("qcd"+nick_suffix)
					config.setdefault("qcd_data_signal_control_nicks", []).append("noplot_data_qcd_signal_ss"+nick_suffix)
					config.setdefault("qcd_data_relaxed_control_nicks", []).append("noplot_data_qcd_relaxed_ss"+nick_suffix)
					if not kwargs.get("no_ewk_samples", False) and kwargs.get("no_ewkz_as_dy", False):
						config.setdefault("qcd_data_subtract_nicks", []).append(" ".join([nick+nick_suffix for nick in "noplot_ztt_qcd_shape noplot_zll_qcd_shape noplot_ewkz_qcd_shape noplot_ttj_qcd_shape noplot_vv_qcd_shape noplot_wj_qcd_shape".split()]))
						config.setdefault("qcd_control_signal_subtract_nicks", []).append(" ".join([nick+nick_suffix for nick in "noplot_ztt_qcd_signal_ss noplot_zll_qcd_signal_ss noplot_ewkz_qcd_signal_ss noplot_ttj_qcd_signal_ss noplot_vv_qcd_signal_ss noplot_wj_qcd_signal_ss".split()]))
						config.setdefault("qcd_control_relaxed_subtract_nicks", []).append(" ".join([nick+nick_suffix for nick in "noplot_ztt_qcd_relaxed_ss noplot_zll_qcd_relaxed_ss noplot_ewkz_qcd_relaxed_ss noplot_ttj_qcd_relaxed_ss noplot_vv_qcd_relaxed_ss noplot_wj_qcd_relaxed_ss".split()]))
					else:
						config.setdefault("qcd_data_subtract_nicks", []).append(" ".join([nick+nick_suffix for nick in "noplot_ztt_qcd_shape noplot_zll_qcd_shape noplot_ttj_qcd_shape noplot_vv_qcd_shape noplot_wj_qcd_shape".split()]))
						config.setdefault("qcd_control_signal_subtract_nicks", []).append(" ".join([nick+nick_suffix for nick in "noplot_ztt_qcd_signal_ss noplot_zll_qcd_signal_ss noplot_ttj_qcd_signal_ss noplot_vv_qcd_signal_ss noplot_wj_qcd_signal_ss".split()]))
						config.setdefault("qcd_control_relaxed_subtract_nicks", []).append(" ".join([nick+nick_suffix for nick in "noplot_ztt_qcd_relaxed_ss noplot_zll_qcd_relaxed_ss noplot_ttj_qcd_relaxed_ss noplot_vv_qcd_relaxed_ss noplot_wj_qcd_relaxed_ss".split()]))
				elif channel in ["mm","ee"]:
					log.error("Sample config (QCD) currently not implemented for channel \"%s\"!" % channel)
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
			return tmp_sample+str(tmp_mass)+("_"+str(int(kwargs["scale_signal"])) if kwargs.get("scale_signal", 1.0) != 1.0 else "")+(nick_suffix if add_nick_suffix else "")

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

	def files_bbh(self, channel, mass=125):
		return self.artus_file_names({"process" : "SUSYGluGluToBBHToTauTau_M"+str(mass), "data": False, "campaign" : self.mc_campaign}, 1)

	def bbh(self, config, channel, category, weight, nick_suffix, higgs_masses, normalise_signal_to_one_pb=False, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []

		scale_factor = lumi
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("bbh", 1.0)

		data_weight, mc_weight = self.projection(kwargs)

		for mass in higgs_masses:
			if channel in ["tt", "et", "mt", "em", "ttbar"]:
				Samples._add_input(
						config,
						self.files_bbh(channel, mass),
						self.root_file_folder(channel),
						lumi*kwargs.get("scale_signal", 1.0),
						mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type),
						"bbh"+str(mass)+("_"+str(int(kwargs["scale_signal"])) if kwargs.get("scale_signal", 1.0) != 1.0 else ""),
						nick_suffix=nick_suffix
				)
			else:
				log.error("Sample config (bbH%s) currently not implemented for channel \"%s\"!" % (str(mass), channel))

			if not kwargs.get("no_plot", False):
				if not kwargs.get("mssm", False):
					Samples._add_bin_corrections(
							config,
							"bbh"+str(mass)+("_"+str(int(kwargs["scale_signal"])) if kwargs.get("scale_signal", 1.0) != 1.0 else ""),
							nick_suffix
					)
				Samples._add_plot(
						config,
						"bbh",
						"LINE",
						"L",
						"bbh"+str(mass)+("_"+str(int(kwargs["scale_signal"])) if kwargs.get("scale_signal", 1.0) != 1.0 else ""),
						nick_suffix
				)
		return config

	def files_ggh(self, channel, mass=125, **kwargs):
		cp=kwargs.get("cp", None)
		if cp in ["sm", "mm", "ps"]:
			return "GluGluToHToTauTauM125_RunIIFall15MiniAODv2_PU25nsData2015v1_13TeV_MINIAOD_amcatnlo-pythia8/*.root"
		else:
			#CAUTION: If necessary the mc-generator nick might need to be updated from time to time.
			return self.artus_file_names({"process" : "GluGluHToTauTau_M"+str(mass), "data": False, "campaign" : self.mc_campaign, "generator" : "powheg-pythia8"}, 1)

	def files_susy_ggh(self, channel, mass=125):
		return self.artus_file_names({"process" : "SUSYGluGluToHToTauTauM"+str(mass), "data": False, "campaign" : self.mc_campaign}, 1)

	def ggh(self, config, channel, category, weight, nick_suffix, higgs_masses, normalise_signal_to_one_pb=False, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", mssm=False, **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []
		
		scale_factor = lumi
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("ggh", 1.0)

		data_weight, mc_weight = self.projection(kwargs)
		if (kwargs.get("cp", "sm") == "sm"):
			matrix_weight = ""
		elif(kwargs.get("cp", "sm") == "mm"):
			matrix_weight = "madGraphWeight050/madGraphWeight000*"
		elif(kwargs.get("cp", "sm") == "ps"):
			matrix_weight = "madGraphWeight100/madGraphWeight000*"
		
		for mass in higgs_masses:
			if channel in ["tt", "et", "mt", "em", "mm", "ee", "ttbar"]:
				Samples._add_input(
						config,
						self.files_ggh(channel, mass, cp=kwargs.get("cp", None)) if not mssm else self.files_susy_ggh(channel, mass),
						self.root_file_folder(channel),
						lumi*kwargs.get("scale_signal", 1.0),
						matrix_weight+mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type),
						"ggh"+str(kwargs.get("cp", ""))+str(mass)+("_"+str(int(kwargs["scale_signal"])) if kwargs.get("scale_signal", 1.0) != 1.0 else ""),
						nick_suffix=nick_suffix
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
						kwargs.get("stacks", "ggh"),
						"LINE",
						"L",
						"ggh"+str(kwargs.get("cp", ""))+str(mass)+("_"+str(int(kwargs["scale_signal"])) if kwargs.get("scale_signal", 1.0) != 1.0 else ""),
						str(kwargs.get("cp", ""))+nick_suffix
				)
		return config 

	def gghsm(self, config, channel, category, weight, nick_suffix, higgs_masses, normalise_signal_to_one_pb=False, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", mssm=False, **kwargs):
		config = self.ggh( config, channel, category, weight, "sm"+nick_suffix, higgs_masses, normalise_signal_to_one_pb=normalise_signal_to_one_pb, lumi=lumi, exclude_cuts=exclude_cuts, cut_type=cut_type, mssm=mssm, cp="sm", stacks="gghsm", **kwargs)
		return config

	def gghmm(self, config, channel, category, weight, nick_suffix, higgs_masses, normalise_signal_to_one_pb=False, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", mssm=False, **kwargs):
		config = self.ggh(config, channel, category, weight, "mm"+nick_suffix, higgs_masses, normalise_signal_to_one_pb=normalise_signal_to_one_pb, lumi=lumi, exclude_cuts=exclude_cuts, cut_type=cut_type, mssm=mssm, cp="mm", stacks="gghmm", **kwargs)
		return config

	def gghps(self, config, channel, category, weight, nick_suffix, higgs_masses, normalise_signal_to_one_pb=False, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", mssm=False, **kwargs):
		config = self.ggh(config, channel, category, weight, "ps"+nick_suffix, higgs_masses, normalise_signal_to_one_pb=normalise_signal_to_one_pb, lumi=lumi, exclude_cuts=exclude_cuts, cut_type=cut_type, mssm=mssm, cp="ps", stacks="gghps", **kwargs)
		return config



	def files_qqh(self, channel, mass=125):
		return self.artus_file_names({"process" : "VBFHToTauTau_M"+str(mass), "data": False, "campaign" : self.mc_campaign}, 1)
	
	def qqh(self, config, channel, category, weight, nick_suffix, higgs_masses, normalise_signal_to_one_pb=False, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []

		scale_factor = lumi
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("qqH", 1.0)

		data_weight, mc_weight = self.projection(kwargs)

		for mass in higgs_masses:
			if channel in ["tt", "et", "mt", "em", "mm", "ee", "ttbar"]:
				Samples._add_input(
						config,
						self.files_qqh(channel, mass),
						self.root_file_folder(channel),
						lumi*kwargs.get("scale_signal", 1.0),
						mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type),
						"qqh"+str(mass)+("_"+str(int(kwargs["scale_signal"])) if kwargs.get("scale_signal", 1.0) != 1.0 else ""),
						nick_suffix=nick_suffix
			)
			else:
				log.error("Sample config (VBF%s) currently not implemented for channel \"%s\"!" % (str(mass), channel))

			if not kwargs.get("no_plot", False):
				if not kwargs.get("mssm", False):
					Samples._add_bin_corrections(
							config,
							"qqh"+str(mass)+("_"+str(int(kwargs["scale_signal"])) if kwargs.get("scale_signal", 1.0) != 1.0 else ""),
							nick_suffix
					)
				Samples._add_plot(
						config,
						"qqh",
						"LINE",
						"L",
						"qqh"+str(mass)+("_"+str(int(kwargs["scale_signal"])) if kwargs.get("scale_signal", 1.0) != 1.0 else ""),
						nick_suffix
				)
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
			config.setdefault("add_nicks", []).append(" ".join([sample+str(mass)+("_"+str(int(kwargs["scale_signal"])) if kwargs.get("scale_signal", 1.0) != 1.0 else "")+nick_suffix+"_noplot" for sample in ["wh", "zh"]]))
			config.setdefault("add_result_nicks", []).append("vh"+str(mass)+("_"+str(int(kwargs["scale_signal"])) if kwargs.get("scale_signal", 1.0) != 1.0 else "")+nick_suffix)

			if not kwargs.get("no_plot", False):
				if not kwargs.get("mssm", False):
					Samples._add_bin_corrections(
							config,
							"vh"+str(mass)+("_"+str(int(kwargs["scale_signal"])) if kwargs.get("scale_signal", 1.0) != 1.0 else ""),
							nick_suffix
					)
				Samples._add_plot(
						config,
						"vh",
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

		for mass in higgs_masses:
			if channel in ["tt", "et", "mt", "em", "mm", "ee", "ttbar"]:
				Samples._add_input(
						config,
						self.files_wh_minus(channel, mass),
						self.root_file_folder(channel),
						lumi*kwargs.get("scale_signal", 1.0),
						mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type),
						"wmh"+str(mass)+("_"+str(int(kwargs["scale_signal"])) if kwargs.get("scale_signal", 1.0) != 1.0 else ""),
						nick_suffix=nick_suffix+"_noplot"
				)
				Samples._add_input(
						config,
						self.files_wh_plus(channel, mass),
						self.root_file_folder(channel),
						lumi*kwargs.get("scale_signal", 1.0),
						mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type),
						"wph"+str(mass)+("_"+str(int(kwargs["scale_signal"])) if kwargs.get("scale_signal", 1.0) != 1.0 else ""),
						nick_suffix=nick_suffix+"_noplot"
				)

				if not "AddHistograms" in config.get("analysis_modules", []):
					config.setdefault("analysis_modules", []).append("AddHistograms")
				config.setdefault("add_nicks", []).append(" ".join([sample+str(mass)+("_"+str(int(kwargs["scale_signal"])) if kwargs.get("scale_signal", 1.0) != 1.0 else "")+nick_suffix+"_noplot" for sample in ["wmh", "wph"]]))
				config.setdefault("add_result_nicks", []).append("wh"+str(mass)+("_"+str(int(kwargs["scale_signal"])) if kwargs.get("scale_signal", 1.0) != 1.0 else "")+nick_suffix)

			else:
				log.error("Sample config (WH%s) currently not implemented for channel \"%s\"!" % (str(mass), channel))

			if not kwargs.get("no_plot", False):
				if not kwargs.get("mssm", False):
					Samples._add_bin_corrections(
							config,
							"wh"+str(mass)+("_"+str(int(kwargs["scale_signal"])) if kwargs.get("scale_signal", 1.0) != 1.0 else ""),
							nick_suffix
					)
				Samples._add_plot(
						config,
						"wh",
						"LINE",
						"L",
						"wh"+str(mass)+("_"+str(int(kwargs["scale_signal"])) if kwargs.get("scale_signal", 1.0) != 1.0 else ""),
						nick_suffix
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

		for mass in higgs_masses:
			if channel in ["tt", "et", "mt", "em", "mm", "ee", "ttbar"]:
				Samples._add_input(
						config,
						self.files_zh(channel, mass),
						self.root_file_folder(channel),
						lumi*kwargs.get("scale_signal", 1.0),
						mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type),
						"zh"+str(mass)+("_"+str(int(kwargs["scale_signal"])) if kwargs.get("scale_signal", 1.0) != 1.0 else ""),
						nick_suffix=nick_suffix
				)

			else:
				log.error("Sample config (ZH%s) currently not implemented for channel \"%s\"!" % (str(mass), channel))

			if not kwargs.get("no_plot", False):
				if not kwargs.get("mssm", False):
					Samples._add_bin_corrections(
							config,
							"zh"+str(mass)+("_"+str(int(kwargs["scale_signal"])) if kwargs.get("scale_signal", 1.0) != 1.0 else ""),
							nick_suffix
					)
				Samples._add_plot(
						config,
						"zh",
						"LINE",
						"L",
						"zh"+str(mass)+("_"+str(int(kwargs["scale_signal"])) if kwargs.get("scale_signal", 1.0) != 1.0 else ""),
						nick_suffix
				)
		return config


	def ff(self, config, channel, category, weight, nick_suffix, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []

		if channel in ["mt","et"]:
			Samples._add_input(
					config,
					self.files_data(channel),
					self.root_file_folder(channel),
					1.0,
					weight+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["iso_2"], cut_type=cut_type)+"*eventWeight*jetToTauFakeWeight_comb",
					"ff",
					nick_suffix=nick_suffix
			)

			Samples._add_input(
					config,
					self.files_ztt(channel),
					self.root_file_folder(channel),
					lumi,
					self.get_weights_ztt(channel=channel,cut_type=cut_type,weight=weight)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["iso_2"], cut_type=cut_type)+"*zPtReweightWeight*(gen_match_2 < 6)*jetToTauFakeWeight_comb",
					"noplot_dy_ff_control",
					nick_suffix=nick_suffix
			)
			Samples._add_input(
					config,
					self.files_ttj(channel),
					self.root_file_folder(channel),
					lumi,
					weight+"*"+self.embedding_ttbarveto_weight(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["iso_2"], cut_type=cut_type)+"*topPtReweightWeight*eventWeight*(gen_match_2 < 6)*jetToTauFakeWeight_comb",
					"noplot_tt_ff_control",
					nick_suffix=nick_suffix
			)
			Samples._add_input(
					config,
					self.files_vv(channel),
					self.root_file_folder(channel),
					lumi,
					weight+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["iso_2"], cut_type=cut_type)+"*eventWeight*(gen_match_2 < 6)*jetToTauFakeWeight_comb",
					"noplot_vv_ff_control",
					nick_suffix=nick_suffix
			)
			Samples._add_input(
					config,
					self.files_data(channel),
					self.root_file_folder(channel),
					1.0,
					weight+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["iso_2"], cut_type=cut_type)+"*eventWeight*jetToTauFakeWeight_comb",
					"noplot_ff_norm",
					nick_suffix=nick_suffix
			)

			Samples._add_input(
					config,
					self.files_ztt(channel),
					self.root_file_folder(channel),
					lumi,
					self.get_weights_ztt(channel=channel,cut_type=cut_type,weight=weight)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["iso_2"], cut_type=cut_type)+"*zPtReweightWeight*(gen_match_2 < 6)*jetToTauFakeWeight_comb",
					"noplot_dy_ff_norm",
					nick_suffix=nick_suffix
			)
			Samples._add_input(
					config,
					self.files_ttj(channel),
					self.root_file_folder(channel),
					lumi,
					weight+"*"+self.embedding_ttbarveto_weight(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["iso_2"], cut_type=cut_type)+"*topPtReweightWeight*eventWeight*(gen_match_2 < 6)*jetToTauFakeWeight_comb",
					"noplot_tt_ff_norm",
					nick_suffix=nick_suffix
			)
			Samples._add_input(
					config,
					self.files_vv(channel),
					self.root_file_folder(channel),
					lumi,
					weight+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["iso_2"], cut_type=cut_type)+"*eventWeight*(gen_match_2 < 6)*jetToTauFakeWeight_comb",
					"noplot_vv_ff_norm",
					nick_suffix=nick_suffix
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

		if channel in ["mt", "et"]:
			Samples._add_input(
					config,
					self.files_ttj(channel) + " " + self.files_wj(channel) + " " + self.files_vv(channel),
					self.root_file_folder(channel),
					lumi,
					mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type),
					"ewk",
					nick_suffix=nick_suffix
			)
		else:
			log.error("Sample config (EWK) currently not implemented for channel \"%s\"!" % channel)
		
		if channel in ["mt", "et"] and fakefactor_method == "standard":
			config["weights"][config["nicks"].index("ewk")] = config["weights"][config["nicks"].index("ewk")]+"*(gen_match_2 != 6)"
		if channel in ["mt", "et"] and fakefactor_method == "comparison":
			config["weights"][config["nicks"].index("ewk")] = config["weights"][config["nicks"].index("ewk")]+"*(gen_match_2 == 6)"
		
		Samples._add_plot(config, "bkg", "HIST", "F", "ewk", nick_suffix)
		return config
