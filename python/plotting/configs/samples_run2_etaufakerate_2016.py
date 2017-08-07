
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import copy

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
	def ztt_genmatch(channel):
		if channel in ["mt", "et"]:
			return "(gen_match_2 == 5)*"
		elif channel == "tt":
			return "(gen_match_1 == 5 && gen_match_2 == 5)*"
		else:
			log.fatal("No ZTT selection implemented for channel \"%s\"!" % channel)
			sys.exit(1)
	
	@staticmethod
	def zl_genmatch(channel):
		if channel in ["mt", "et", "tt"]:
			return "(gen_match_2 < 5)*"
		else:
			log.fatal("No ZL selection implemented for channel \"%s\"!" % channel)
			sys.exit(1)
	
	@staticmethod
	def zj_genmatch(channel):
		if channel in ["mt", "et"]:
			return "(gen_match_2 == 6)*"
		elif channel == "tt":
			return "(gen_match_2 == 6 || gen_match_1 == 6)*"
		else:
			log.fatal("No ZJ selection implemented for channel \"%s\"!" % channel)
			sys.exit(1)
	
	@staticmethod
	def zll_genmatch(channel):
		if channel in ["mt", "et", "tt"]:
			return "(gen_match_2 < 5 || gen_match_2 == 6)*"
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


	def get_config(self, samples, channel, category, nick_suffix="", postfit_scales=None, blind_expression=None, **kwargs):
		config = super(Samples, self).get_config(samples, channel, category, nick_suffix=nick_suffix, postfit_scales=postfit_scales, **kwargs)
		
		# blinding (of data)
		config["weights"] = [weight.format(blind=self.expressions.replace_expressions("blind_"+str(blind_expression)) if "blind_"+str(blind_expression) in self.expressions.expressions_dict else "1.0") for weight in config["weights"]]
		
		# execute bin correction modules after possible background estimation modules
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
		
		if channel == "mt":
			Samples._add_input(
					config,
					"SingleMuon_Run2016?_*_13TeV_*AOD/*.root",
					channel+"_nominal/ntuple",
					1.0,
					weight+"*eventWeight*" + self.cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type),
					"data",
					nick_suffix=nick_suffix
			)
		elif channel == "et":
			Samples._add_input(
					config,
					"SingleElectron_Run2016?_*_13TeV_*AOD/*.root",
					channel+"_nominal/ntuple",
					1.0,
					weight+"*eventWeight*" + self.cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type),
					"data",
					nick_suffix=nick_suffix
			)
		elif channel == "tt":
			Samples._add_input(
					config,
					"Tau_Run2016?_*_13TeV_*AOD/*.root",
					channel+"_nominal/ntuple",
					1.0,
					weight+"*eventWeight*" + self.cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type),
					"data",
					nick_suffix=nick_suffix
			)
		else:
			log.error("Sample config (Data) currently not implemented for channel \"%s\"!" % channel)
		
		Samples._add_plot(config, "data", "E", "ELP", "data", nick_suffix)
		return config

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
		
		if channel in ["mt", "et", "tt"]:
			Samples._add_input(
					config,
					"DY*JetsToLLM*_RunIISummer16*_*_13TeV_*AOD_*/*.root",
					channel+"_tagEleEsNom_probeTauEsNom_probeEleEsNom/ntuple",
					lumi,
					weight+"*eventWeight*" + Samples.ztt_genmatch(channel) + self.cut_string(channel, exclude_cuts=exclude_cuts+["blind"], cut_type=cut_type),
					"ztt",
					nick_suffix=nick_suffix
			)
		else:
			log.error("Sample config (ZTT) currently not implemented for channel \"%s\"!" % channel)
		
		Samples._add_bin_corrections(config, "ztt", nick_suffix)
		Samples._add_plot(config, "bkg", "HIST", "F", "ztt", nick_suffix)
		
		return config
	
	def zl(self, config, channel, category, weight, nick_suffix, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []
		
		scale_factor = lumi
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("ZL", 1.0)
		
		if channel in ["mt", "et", "tt"]:
			Samples._add_input(
					config,
					"DY*JetsToLLM10to50_RunIISummer16*_*_13TeV_*AOD_*/*.root DY*JetsToLLM50_RunIISummer16*_*_13TeV_*AOD_*/*.root",
					channel+"_tagEleEsNom_probeTauEsNom_probeEleEsNom/ntuple",
					lumi,
					weight+"*eventWeight*" + Samples.zl_genmatch(channel) + self.cut_string(channel, exclude_cuts=exclude_cuts+["blind"], cut_type=cut_type),
					"zl",
					nick_suffix=nick_suffix
			)
		else:
			log.error("Sample config (ZL) currently not implemented for channel \"%s\"!" % channel)
		
		Samples._add_bin_corrections(config, "zl", nick_suffix)
		Samples._add_plot(config, "bkg", "HIST", "F", "zl", nick_suffix)
		return config
	
	def zj(self, config, channel, category, weight, nick_suffix, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []
		
		scale_factor = lumi
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("ZJ", 1.0)
		
		if channel in ["mt", "et", "tt"]:
			Samples._add_input(
					config,
					"DY*JetsToLLM10to50_RunIISummer16*_*_13TeV_*AOD_*/*.root DY*JetsToLLM50_RunIISummer16*_*_13TeV_*AOD_*/*.root",
					channel+"_tagEleEsNom_probeTauEsNom_probeEleEsNom/ntuple",
					lumi,
					weight+"*eventWeight*" + Samples.zj_genmatch(channel) + self.cut_string(channel, exclude_cuts=exclude_cuts+["blind"], cut_type=cut_type),
					"zj",
					nick_suffix=nick_suffix
			)
		else:
			log.error("Sample config (ZJ) currently not implemented for channel \"%s\"!" % channel)
		
		Samples._add_bin_corrections(config, "zj", nick_suffix)
		Samples._add_plot(config, "bkg", "HIST", "F", "zj", nick_suffix)
		return config
	
	def files_zll(self, channel):
		return self.artus_file_names({"process" : "(DYJetsToLLM10to50|DYJetsToLLM50|DY1JetsToLLM50|DY2JetsToLLM50|DY3JetsToLLM50|DY4JetsToLLM50)", "data": False, "campaign" : self.mc_campaign, "generator" : "madgraph\-pythia8"}, 7)

	def zll(self, config, channel, category, weight, nick_suffix, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []
		
		zmm_cr_factor = kwargs.get("zmm_cr_factor", "(1.0)")

		scale_factor = lumi
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("ZLL", 1.0)
		
		if channel in ["mt", "et", "tt"]:
			Samples._add_input(
					config,
					"DY*JetsToLLM10to50_RunIISummer16*_*_13TeV_*AOD_*/*.root DY*JetsToLLM50_RunIISummer16*_*_13TeV_*AOD_*/*.root",
					channel+"_tagEleEsNom_probeTauEsNom_probeEleEsNom/ntuple",
					lumi,
					weight+"*eventWeight*" + Samples.zll_genmatch(channel) + self.cut_string(channel, exclude_cuts=exclude_cuts+["blind"], cut_type=cut_type),
					"zll",
					nick_suffix=nick_suffix
			)
		else:
			log.error("Sample config (ZLL) currently not implemented for channel \"%s\"!" % channel)
		
		Samples._add_bin_corrections(config, "zll", nick_suffix)
		Samples._add_plot(config, "bkg", "HIST", "F", "zll", nick_suffix)
		return config

	def ttj(self, config, channel, category, weight, nick_suffix, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", estimationMethod="classic", fakefactor_method=None, **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []
		
		zmm_cr_factor = kwargs.get("zmm_cr_factor", "(1.0)")

		scale_factor = lumi
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("TTJ", 1.0)
		
		if channel in ["mt", "et", "tt"]:
			Samples._add_input(
					config,
					"TT_RunIISummer16*_*_13TeV_*AOD_powheg-pythia8/*.root",
					channel+"_nominal/ntuple",
					lumi,
					weight+"*eventWeight*" + self.cut_string(channel, exclude_cuts=exclude_cuts+["blind"], cut_type=cut_type),
					"ttj",
					nick_suffix=nick_suffix
			)
		else:
			log.error("Sample config (TTJ) currently not implemented for channel \"%s\"!" % channel)
		
		Samples._add_bin_corrections(config, "ttj", nick_suffix)
		Samples._add_plot(config, "bkg", "HIST", "F", "ttj", nick_suffix)
		return config

	def files_ttj(self, channel):
		if self.ttbar_retuned:
			return self.artus_file_names({"process" : "TTTo.*", "data": False, "campaign" : self.mc_campaign}, 2)
		else:
			return self.artus_file_names({"process" : "TT_", "data": False, "campaign" : self.mc_campaign}, 1)

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


	def vv(self, config, channel, category, weight, nick_suffix, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []
		
		scale_factor = lumi
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("Dibosons", 1.0)
		
		if channel in ["mt", "et", "tt"]:
			Samples._add_input(
					config,
					"ST*_RunIISummer16*_*_13TeV_*AOD_powheg-pythia8/*root WW*_RunIISummer16*_*_13TeV_*AOD_*/*.root WZ*_RunIISummer16*_*_13TeV_*AOD_*/*.root ZZ*_RunIISummer16*_*_13TeV_*AOD_*/*.root VV*_RunIISummer16*_*_13TeV_*AOD_*/*.root",
					channel+"_nominal/ntuple",
					lumi,
					weight+"*eventWeight*" + self.cut_string(channel, exclude_cuts=exclude_cuts+["blind"], cut_type=cut_type),
					"vv",
					nick_suffix=nick_suffix
			)
		else:
			log.error("Sample config (VV) currently not implemented for channel \"%s\"!" % channel)
		
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

	def wj(self, config, channel, category, weight, nick_suffix, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []
		
		scale_factor = lumi
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("WJets", 1.0)
		
		if channel in ["mt", "et"]:
			shape_weight = weight+"*eventWeight*" + self.cut_string(channel, exclude_cuts=exclude_cuts+["blind"], cut_type=cut_type)
			#if (not category is None) and (category != ""):
				## relaxed isolation
				#shape_weight = weight+"*eventWeight*" + self.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "iso_2"], cut_type=cut_type) + "*(byCombinedIsolationDeltaBetaCorrRaw3Hits_2<10.0)"
			
			Samples._add_input(
					config,
					"W*JetsToLNu_RunIISummer16*_*_13TeV_*AOD_*/*.root",
					channel+"_nominal/ntuple",
					lumi,
					shape_weight,
					"wj",
					nick_suffix=nick_suffix
			)
			Samples._add_input(
					config,
					"SingleMuon_Run2016?_*_13TeV_*AOD/*.root" if channel == "mt" else "SingleElectron_Run2016?_*_13TeV_*AOD/*root",
					channel+"_nominal/ntuple",
					1.0,
					"eventWeight*" + self.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "mt"], cut_type=cut_type) + "*(mt_1>70.0)",
					"noplot_wj_data_control"
			)
			Samples._add_input(
					config,
					"DY*JetsToLLM*_RunIISummer16*_*_13TeV_*AOD_*/*.root",
					channel+"_tagEleEsNom_probeTauEsNom_probeEleEsNom/ntuple",
					lumi,
					"eventWeight*" + Samples.ztt_genmatch(channel) + self.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "mt"], cut_type=cut_type) + "*(mt_1>70.0)",
					"noplot_ztt_mc_wj_control",
					nick_suffix=nick_suffix
			)
			Samples._add_input(
					config,
					"DY*JetsToLLM10to50_RunIISummer16*_*_13TeV_*AOD_*/*.root DY*JetsToLLM50_RunIISummer16*_*_13TeV_*AOD_*/*.root",
					channel+"_tagEleEsNom_probeTauEsNom_probeEleEsNom/ntuple",
					lumi,
					"eventWeight*" + Samples.zll_genmatch(channel) + self.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "mt"], cut_type=cut_type) + "*(mt_1>70.0)",
					"noplot_zll_wj_control",
					nick_suffix=nick_suffix
			)
			Samples._add_input(
					config,
					"TT_RunIISummer16*_*_13TeV_*AOD_powheg-pythia8/*.root",
					channel+"_nominal/ntuple",
					lumi,
					"eventWeight*" + self.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "mt"], cut_type=cut_type) + "*(mt_1>70.0)",
					"noplot_ttj_wj_control",
					nick_suffix=nick_suffix
			)
			Samples._add_input(
					config,
					"ST*_RunIISummer16*_*_13TeV_*AOD_powheg-pythia8/*root WW*_RunIISummer16*_*_13TeV_*AOD_*/*.root WZ*_RunIISummer16*_*_13TeV_*AOD_*/*.root ZZ*_RunIISummer16*_*_13TeV_*AOD_*/*.root VV*_RunIISummer16*_*_13TeV_*AOD_*/*.root",
					channel+"_nominal/ntuple",
					lumi,
					"eventWeight*" + self.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "mt"], cut_type=cut_type) + "*(mt_1>70.0)",
					"noplot_vv_wj_control",
					nick_suffix=nick_suffix
			)
			Samples._add_input(
					config,
					"W*JetsToLNu_RunIISummer16*_*_13TeV_*AOD_*/*.root",
					channel+"_nominal/ntuple",
					lumi,
					weight+"*eventWeight*" + self.cut_string(channel, exclude_cuts=exclude_cuts+["blind"], cut_type=cut_type),
					"noplot_wj_mc_signal",
					nick_suffix=nick_suffix
			)
			Samples._add_input(
					config,
					"W*JetsToLNu_RunIISummer16*_*_13TeV_*AOD_*/*.root",
					channel+"_nominal/ntuple",
					lumi,
					"eventWeight*" + self.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "mt"], cut_type=cut_type) + "*(mt_1>70.0)",
					"noplot_wj_mc_control",
					nick_suffix=nick_suffix
			)

			if not "EstimateWjets" in config.get("analysis_modules", []):
				config.setdefault("analysis_modules", []).append("EstimateWjets")
			config.setdefault("wjets_from_mc", []).append(False)
			config.setdefault("wjets_shape_nicks", []).append("wj"+nick_suffix)
			config.setdefault("wjets_data_control_nicks", []).append("noplot_wj_data_control"+nick_suffix)
			config.setdefault("wjets_data_substract_nicks", []).append(" ".join([nick+nick_suffix for nick in "noplot_ztt_mc_wj_control noplot_zll_wj_control noplot_ttj_wj_control noplot_vv_wj_control".split()]))
			config.setdefault("wjets_mc_signal_nicks", []).append("noplot_wj_mc_signal"+nick_suffix)
			config.setdefault("wjets_mc_control_nicks", []).append("noplot_wj_mc_control"+nick_suffix)

		elif channel in ["tt"]:
			Samples._add_input(
					config,
					"W*JetsToLNu_RunIISummer16*_*_13TeV_*AOD_*/*.root",
					channel+"_nominal/ntuple",
					lumi,
					weight+"*eventWeight*" + self.cut_string(channel, exclude_cuts=exclude_cuts+["blind"], cut_type=cut_type),
					"wj",
					nick_suffix=nick_suffix
			)
		else:	
			log.error("Sample config (WJets) currently not implemented for channel \"%s\"!" % channel)
		
		if not kwargs.get("no_plot", False):
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

		if channel in ["et", "mt", "tt"]:
			if "classic" in estimationMethod:
				# WJets for QCD estimate
				Samples._add_input(
						config,
						"W*JetsToLNu_RunIISummer16*_*_13TeV_*AOD_*/*.root",
						channel+"_nominal/ntuple",
						lumi,
						mc_weight+"*"+weight+"*eventWeight*" + self.wj_stitchingweight()+"*"+ self.cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=cut_type) + "*((q_1*q_2)>0.0)",
						"noplot_wj_ss",
						nick_suffix=nick_suffix
				)
			
				if channel in ["mt", "et"]:
					high_mt_ss_cut_type = cut_type + "highMtSSControlRegionWJ"
					exclude_cuts_high_mt = [cut for cut in exclude_cuts if cut not in ["mt"]]
					exclude_cuts_high_mt_ss = copy.deepcopy(exclude_cuts_high_mt)+["os"]
					
					Samples._add_input(
							config,
							"SingleMuon_Run2016?_*_13TeV_*AOD/*.root" if channel == "mt" else ("SingleElectron_Run2016?_*_13TeV_*AOD/*root" if channel == "et" else "MuonEG_Run2016?_*_13TeV_*AOD/*.root"),
							channel+"_nominal/ntuple",
							1.0,
							data_weight+"*"+weight+"*eventWeight*" + self.cut_string(channel, exclude_cuts=exclude_cuts_high_mt_ss, cut_type=high_mt_ss_cut_type),
							"noplot_wj_ss_data_control",
							nick_suffix=nick_suffix
					)
					Samples._add_input(
							config,
							"DY*JetsToLLM*_RunIISummer16*_*_13TeV_*AOD_*/*.root",
							channel+"_tagEleEsNom_probeTauEsNom_probeEleEsNom/ntuple",
							lumi,
							Samples.ztt_genmatch(channel)+"*"+self.get_weights_ztt(channel=channel,cut_type=cut_type,weight=weight)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_high_mt_ss, cut_type=high_mt_ss_cut_type)+"*zPtReweightWeight"+"*"+zmm_cr_factor,
							"noplot_ztt_ss_mc_wj_control",
							nick_suffix=nick_suffix
					)
					Samples._add_input(
							config,
							"DY*JetsToLLM10to50_RunIISummer16*_*_13TeV_*AOD_*/*.root DY*JetsToLLM50_RunIISummer16*_*_13TeV_*AOD_*/*.root",
							channel+"_tagEleEsNom_probeTauEsNom_probeEleEsNom/ntuple",
							lumi,
							mc_weight+"*"+weight+"*eventWeight*"+self.zll_stitchingweight()+"*"+Samples.zll_genmatch(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_high_mt_ss, cut_type=high_mt_ss_cut_type)+"*zPtReweightWeight"+"*"+self.zll_zl_shape_weight(channel, cut_type)+"*"+zmm_cr_factor,
							"noplot_zll_ss_wj_control",
							nick_suffix=nick_suffix
					)
					Samples._add_input(
							config,
							"TT_RunIISummer16*_*_13TeV_*AOD_powheg-pythia8/*.root",
							channel+"_nominal/ntuple",
							lumi,
							mc_weight+"*"+weight+"*eventWeight*"+self.embedding_ttbarveto_weight(channel)+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts_high_mt_ss, cut_type=high_mt_ss_cut_type)+"*topPtReweightWeight",
							"noplot_ttj_ss_wj_control",
							nick_suffix=nick_suffix
					)
					Samples._add_input(
							config,
							"ST*_RunIISummer16*_*_13TeV_*AOD_powheg-pythia8/*root WW*_RunIISummer16*_*_13TeV_*AOD_*/*.root WZ*_RunIISummer16*_*_13TeV_*AOD_*/*.root ZZ*_RunIISummer16*_*_13TeV_*AOD_*/*.root VV*_RunIISummer16*_*_13TeV_*AOD_*/*.root",
							channel+"_nominal/ntuple",
							lumi,
							mc_weight+"*"+weight+"*eventWeight*"+self._cut_string(channel, exclude_cuts=exclude_cuts_high_mt_ss, cut_type=high_mt_ss_cut_type),
							"noplot_vv_ss_wj_control",
							nick_suffix=nick_suffix
					)
					Samples._add_input(
							config,
							"W*JetsToLNu_RunIISummer16*_*_13TeV_*AOD_*/*.root",
							channel+"_nominal/ntuple",
							lumi,
							mc_weight+"*"+weight+"*eventWeight*"+self.wj_stitchingweight()+"*"+self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=cut_type)+"*((q_1*q_2)>0.0)",
							"noplot_wj_ss_mc_signal",
							nick_suffix=nick_suffix
					)
					Samples._add_input(
							config,
							"W*JetsToLNu_RunIISummer16*_*_13TeV_*AOD_*/*.root",
							channel+"_nominal/ntuple",
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
					config.setdefault("wjets_data_substract_nicks", []).append(" ".join([nick+nick_suffix for nick in "noplot_ztt_ss_mc_wj_control noplot_zll_ss_wj_control noplot_ttj_ss_wj_control noplot_vv_ss_wj_control".split()]))
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
					"SingleMuon_Run2016?_*_13TeV_*AOD/*.root" if channel == "mt" else ("SingleElectron_Run2016?_*_13TeV_*AOD/*root" if channel == "et" else "MuonEG_Run2016?_*_13TeV_*AOD/*.root" if channel == "em" else "Tau_Run2016?_*_13TeV_*AOD/*.root"),
					channel+"_nominal/ntuple",
					1.0,
					shape_weight,
					"qcd",
					nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						"SingleMuon_Run2016?_*_13TeV_*AOD/*.root" if channel == "mt" else ("SingleElectron_Run2016?_*_13TeV_*AOD/*root" if channel == "et" else "MuonEG_Run2016?_*_13TeV_*AOD/*.root" if channel == "em" else "Tau_Run2016?_*_13TeV_*AOD/*.root"),
						channel+"_nominal/ntuple",
						1.0,
						weight+"*eventWeight*" + self.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "os"], cut_type=cut_type) + "*((q_1*q_2)>0.0)",
						"noplot_data_qcd_yield",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						"SingleMuon_Run2016?_*_13TeV_*AOD/*.root" if channel == "mt" else ("SingleElectron_Run2016?_*_13TeV_*AOD/*root" if channel == "et" else "MuonEG_Run2016?_*_13TeV_*AOD/*.root" if channel == "em" else "Tau_Run2016?_*_13TeV_*AOD/*.root"),
						channel+"_nominal/ntuple",
						1.0,
						"eventWeight*" + self.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "os"], cut_type=cut_type) + "*((q_1*q_2)>0.0)",
						"noplot_data_qcd_control",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						"DY*JetsToLLM*_RunIISummer16*_*_13TeV_*AOD_*/*.root",
						channel+"_tagEleEsNom_probeTauEsNom_probeEleEsNom/ntuple",
						lumi,
						"eventWeight*" + Samples.ztt_genmatch(channel) + self.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "os"], cut_type=cut_type) + "*((q_1*q_2)>0.0)",
						"noplot_ztt_mc_qcd_control",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						"DY*JetsToLLM10to50_RunIISummer16*_*_13TeV_*AOD_*/*.root DY*JetsToLLM50_RunIISummer16*_*_13TeV_*AOD_*/*.root",
						channel+"_tagEleEsNom_probeTauEsNom_probeEleEsNom/ntuple",
						lumi,
						"eventWeight*" + Samples.zll_genmatch(channel) + self.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "os"], cut_type=cut_type) + "*((q_1*q_2)>0.0)",
						"noplot_zll_qcd_control",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						"TT_RunIISummer16*_*_13TeV_*AOD_powheg-pythia8/*.root",
						channel+"_nominal/ntuple",
						lumi,
						"eventWeight*" + self.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "os"], cut_type=cut_type) + "*((q_1*q_2)>0.0)",
						"noplot_ttj_qcd_control",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						"ST*_RunIISummer16*_*_13TeV_*AOD_powheg-pythia8/*root WW*_RunIISummer16*_*_13TeV_*AOD_*/*.root WZ*_RunIISummer16*_*_13TeV_*AOD_*/*.root ZZ*_RunIISummer16*_*_13TeV_*AOD_*/*.root VV*_RunIISummer16*_*_13TeV_*AOD_*/*.root",
						channel+"_nominal/ntuple",
						lumi,
						"eventWeight*" + self.cut_string(channel, exclude_cuts=exclude_cuts+["blind", "os"], cut_type=cut_type) + "*((q_1*q_2)>0.0)",
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
					if cut_type == "baseline2016" or cut_type == "baseline2016newTauId":
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
			Samples._add_bin_corrections(config, "qcd", nick_suffix)
			Samples._add_plot(config, "bkg", "HIST", "F", "qcd", nick_suffix)
		return config

