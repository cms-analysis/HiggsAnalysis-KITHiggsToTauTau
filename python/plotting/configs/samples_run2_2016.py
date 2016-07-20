
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import copy

import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.samples as samples
from Kappa.Skimming.registerDatasetHelper import get_nick_list

energy = 13
default_lumi = 6.26*1000.0

class Samples(samples.SamplesBase):

	
	# constants for all plots
	data_format = "MINIAOD"
	mc_campaign = "RunIISpring16MiniAODv.*"

	@staticmethod 
	def root_file_folder(channel):
		return channel+"_jecUncNom"+("_tauEsNom" if "t" in channel else "")+"/ntuple"

	@staticmethod
	def artus_file_names( query, expect_n_results = 1):
		query["energy"] = energy
		found_file_names = []
		for nick in get_nick_list ( query, expect_n_results = expect_n_results):
			found_file_names.append(nick  + "/*.root")
		return " ".join(found_file_names) # convert it to a HP-readable format

	@staticmethod
	def ztt_genmatch(channel):
		if channel in ["mt", "et"]:
			return "(gen_match_2 == 5)*"
		elif channel == "em":
			return "(gen_match_1 > 2 && gen_match_2 > 3)*"
		elif channel == "mm":
			return "(gen_match_1 > 3 && gen_match_2 > 3)*"
		elif channel == "tt":
			return "(gen_match_1 == 5 && gen_match_2 == 5)*"
		else:
			log.fatal("No ZTT selection implemented for channel \"%s\"!" % channel)
			sys.exit(1)

	@staticmethod
	def zl_genmatch(channel):
		if channel in ["mt", "et"]:
			return "(gen_match_2 < 5)*"
		elif channel == "tt":
			return "(gen_match_1 < 6 && gen_match_2 < 6 && !(gen_match_1 == 5 && gen_match_2 == 5))*"
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
		if channel in ["mt", "et"]:
			return "(gen_match_2 < 5 || gen_match_2 == 6)*"
		elif channel == "em":
			return "(gen_match_1 < 3 || gen_match_2 < 4)*"
		elif channel == "mm":
			return "(gen_match_1 < 4 || gen_match_2 < 4)*"
		elif channel == "tt":
			return "((gen_match_1 < 6 && gen_match_2 < 6 && !(gen_match_1 == 5 && gen_match_2 == 5)) || gen_match_2 == 6 || gen_match_1 == 6)*"
		else:
			log.fatal("No ZLL selection implemented for channel \"%s\"!" % channel)
			sys.exit(1)

	def __init__(self):
		super(Samples, self).__init__()
		self.exclude_cuts = ["blind"]
		self.period = "run2"

	def get_config(self, samples, channel, category, nick_suffix="", postfit_scales=None, **kwargs):
		config = super(Samples, self).get_config(samples, channel, category, nick_suffix=nick_suffix, postfit_scales=postfit_scales, **kwargs)

		# execute bin correction modules after possible background estimation modules
		if not kwargs.get("mssm", False):
			config.setdefault("analysis_modules", []).sort(key=lambda module: module in ["BinErrorsOfEmptyBins", "CorrectNegativeBinContents"])
		
		return config

	def projection(self, kwargs):
		data_weight = "(1.0)*"
		mc_weight = "(1.0)*"
		if kwargs.get("project_to_lumi", False):
			data_weight = "({projection})*".format(projection=kwargs["project_to_lumi"]) + data_weight
			mc_weight = "({projection})*".format(projection=kwargs["project_to_lumi"]) + mc_weight
		if kwargs.get("cut_mc_only", False):
			mc_weight = "({mc_cut})*".format(mc_cut=kwargs["cut_mc_only"]) + mc_weight
		if kwargs.get("scale_mc_only", False):
			mc_weight = "({mc_scale})*".format(mc_scale=kwargs["scale_mc_only"]) + mc_weight
		return data_weight, mc_weight

	def files_data(self, channel):
		query = {}
		expect_n_results = 3 # adjust in if-statements if different depending on channel
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

		query["data"] = True
		query["campaign"] = "Run2016.*"
		return self.artus_file_names(query, expect_n_results),

	def data(self, config, channel, category, weight, nick_suffix, exclude_cuts=None, cut_type="baseline", **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []

		scale_factor = 1.0
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("data_obs", 1.0)
		data_weight = "(1.0)*"
		if kwargs.get("project_to_lumi", False):
			data_weight = "({projection})*".format(projection=kwargs["project_to_lumi"]) + data_weight

		Samples._add_input(
				config,
				self.files_data(channel),
				self.root_file_folder(channel),
				1.0,
				data_weight+weight+"*eventWeight*" + self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type),
				"data",
				nick_suffix=nick_suffix
		)

		Samples._add_plot(config, "data", "E", "ELP", "data", nick_suffix)
		return config

	def files_ztt(self, channel):
		return self.artus_file_names({"process" : "(DYJetsToLLM10to50|DYJetsToLLM50|DYJetsToLLM150|DY1JetsToLLM50|DY2JetsToLLM50|DY3JetsToLLM50|DY4JetsToLLM50)", "data": False, "campaign" : "RunIISpring16MiniAODv2", "generator" : "madgraph\-pythia8"}, 7)

	def ztt(self, config, channel, category, weight, nick_suffix, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []

		scale_factor = 1.0
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("ZTT", 1.0)

		data_weight, mc_weight = self.projection(kwargs) 


		self.root_file_folder(channel),
		if channel in ["mt", "et", "tt", "em", "mm"]:
			Samples._add_input(
					config,
					self.files_ztt(channel),
					self.root_file_folder(channel),
					lumi,
					mc_weight+weight+"*eventWeight*" + Samples.ztt_genmatch(channel) + self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type),
					"ztt",
					nick_suffix=nick_suffix
			)
		else:
			log.error("Sample config (ZTT) currently not implemented for channel \"%s\"!" % channel)
		if not kwargs.get("mssm", False):
			Samples._add_bin_corrections(config, "ztt", nick_suffix)
		Samples._add_plot(config, "bkg", "HIST", "F", "ztt", nick_suffix)

		return config

	def files_zll(self, channel):
		return self.artus_file_names({"process" : "(DYJetsToLLM10to50|DYJetsToLLM50|DY1JetsToLLM50|DY2JetsToLLM50|DY3JetsToLLM50|DY4JetsToLLM50)", "data": False, "campaign" : "RunIISpring16MiniAODv2", "generator" : "madgraph\-pythia8"}, 6)

	def zll(self, config, channel, category, weight, nick_suffix, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", fakefactor_method=None, **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []

		scale_factor = lumi
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("ZLL", 1.0)

		data_weight, mc_weight = self.projection(kwargs) 

		if channel in ["mt", "et", "tt", "em", "mm"]:
			Samples._add_input(
					config,
					self.files_zll(channel),
					self.root_file_folder(channel),
					lumi,
					mc_weight+weight+"*eventWeight*" + Samples.zll_genmatch(channel) + self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type),
					"zll",
					nick_suffix=nick_suffix
			)
		else:
			log.error("Sample config (ZLL) currently not implemented for channel \"%s\"!" % channel)
		if not kwargs.get("mssm", False):
			Samples._add_bin_corrections(config, "zll", nick_suffix)
		
		if channel in ["mt", "et"] and fakefactor_method == "standard":
			config["weights"][config["nicks"].index("zll")] = config["weights"][config["nicks"].index("zll")]  + "*(gen_match_2 != 6)"
		if channel in ["mt", "et"] and fakefactor_method == "comparison":
			config["weights"][config["nicks"].index("zll")] = config["weights"][config["nicks"].index("zll")]  + "*(gen_match_2 == 6)"
		
		Samples._add_plot(config, "bkg", "HIST", "F", "zll", nick_suffix)
		return config

	def files_ttj(self, channel):
		return self.artus_file_names({"process" : "TT", "data": False, "campaign" : "RunIISpring16MiniAODv2"}, 1)

	def ttj(self, config, channel, category, weight, nick_suffix, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", fakefactor_method=None, **kwargs):
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
				mc_weight+weight+"*eventWeight*" + self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type),
				"ttj",
				nick_suffix=nick_suffix
		)
		if channel == "em": # handle later as result from other member function
			Samples._add_input(
					config,
					self.files_data(channel),
					self.root_file_folder(channel),
					1.0,
					data_weight+"eventWeight*" + self._cut_string(channel, exclude_cuts=exclude_cuts+["pzeta", "nobtag"], cut_type=cut_type) + "*(pZetaMissVis < -20.0)",
					"noplot_ttj_data_control",
					nick_suffix=nick_suffix
			)
			Samples._add_input(
					config,
					self.files_ztt(channel),
					self.root_file_folder(channel),
					lumi,
					mc_weight+"eventWeight*" + Samples.ztt_genmatch(channel) + self._cut_string(channel, exclude_cuts=exclude_cuts+["pzeta", "nobtag"], cut_type=cut_type) + "*(pZetaMissVis < -20.0)",
					"noplot_ztt_mc_ttj_control",
					nick_suffix=nick_suffix
			)
			Samples._add_input(
					config,
					self.files_zll(channel),
					self.root_file_folder(channel),
					lumi,
					mc_weight+"eventWeight*" + Samples.zll_genmatch(channel) + self._cut_string(channel, exclude_cuts=exclude_cuts+["pzeta", "nobtag"], cut_type=cut_type) + "*(pZetaMissVis < -20.0)",
					"noplot_zll_ttj_control",
					nick_suffix=nick_suffix
			)
			Samples._add_input(
					config,
					self.files_wj(channel),
					self.root_file_folder(channel),
					lumi,
					mc_weight+"eventWeight*" + self._cut_string(channel, exclude_cuts=exclude_cuts+["pzeta", "nobtag"], cut_type=cut_type) + "*(pZetaMissVis < -20.0)",
					"noplot_wj_ttj_control",
					nick_suffix=nick_suffix
			)
			Samples._add_input(
					config,
					self.files_vv(channel),
					self.root_file_folder(channel),
					lumi,
					mc_weight+"eventWeight*" + self._cut_string(channel, exclude_cuts=exclude_cuts+["pzeta", "nobtag"], cut_type=cut_type) + "*(pZetaMissVis < -20.0)",
					"noplot_vv_ttj_control",
					nick_suffix=nick_suffix
			)
			Samples._add_input(
					config,
					self.files_ttj(channel),
					self.root_file_folder(channel),
					lumi,
					mc_weight+weight+"*eventWeight*" + self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type),
					"noplot_ttj_mc_signal",
					nick_suffix=nick_suffix
			)
			Samples._add_input(
					config,
					self.files_ttj(channel),
					self.root_file_folder(channel),
					lumi,
					mc_weight+"eventWeight*" + self._cut_string(channel, exclude_cuts=exclude_cuts+["pzeta", "nobtag"], cut_type=cut_type) + "*(pZetaMissVis < -20.0)",
					"noplot_ttj_mc_control",
					nick_suffix=nick_suffix
			)

			if not "EstimateTtbar" in config.get("analysis_modules", []):
				config.setdefault("analysis_modules", []).append("EstimateTtbar")
			config.setdefault("ttbar_from_mc", []).append(True)
			config.setdefault("ttbar_shape_nicks", []).append("ttj"+nick_suffix)
			config.setdefault("ttbar_data_control_nicks", []).append("noplot_ttj_data_control"+nick_suffix)
			config.setdefault("ttbar_data_substract_nicks", []).append(" ".join([nick+nick_suffix for nick in "noplot_ztt_mc_ttj_control noplot_zll_ttj_control noplot_wj_ttj_control noplot_vv_ttj_control".split()]))
			config.setdefault("ttbar_mc_signal_nicks", []).append("noplot_ttj_mc_signal"+nick_suffix)
			config.setdefault("ttbar_mc_control_nicks", []).append("noplot_ttj_mc_control"+nick_suffix)
		if channel not in ["em", "et", "mt", "tt", "mm"]:
			log.error("Sample config (TTJ) currently not implemented for channel \"%s\"!" % channel)
		if not kwargs.get("mssm", False):
			Samples._add_bin_corrections(config, "ttj", nick_suffix)
		
		if channel in ["mt", "et"] and fakefactor_method == "standard":
			config["weights"][config["nicks"].index("ttj")] = config["weights"][config["nicks"].index("ttj")]  + "*(gen_match_2 != 6)"
		if channel in ["mt", "et"] and fakefactor_method == "comparison":
			config["weights"][config["nicks"].index("ttj")] = config["weights"][config["nicks"].index("ttj")]  + "*(gen_match_2 == 6)"
		
		Samples._add_plot(config, "bkg", "HIST", "F", "ttj", nick_suffix)
		return config

	def files_vv(self, config):
		artus_files = self.artus_file_names({ "process" : 
		                                      "(WWTo1L1Nu2Q|"
		                                    + "WZJets|WZTo1L1Nu2Q|WZTo1L3Nu|WZTo2L2Q|" 
		                                    + "ZZTo2L2Q|ZZTo4L|VVTo2L2Nu)",
		                      "data" : False, "campaign" : "RunIISpring16MiniAODv2", "generator" : "amcatnlo-pythia8"}, 6)

		artus_files = artus_files + " " + self.artus_file_names({ "process" : "(STt-channelantitop4fleptonDecays|STt-channeltop4fleptonDecays|STtWantitop5finclusiveDecays|STtWtop5finclusiveDecays)",
		                      "data" : False, "campaign" : "RunIISpring16MiniAODv2" }, 4),
		return artus_files

	def vv(self, config, channel, category, weight, nick_suffix, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", fakefactor_method=None, **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []

		scale_factor = lumi
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("Dibosons", 1.0)

		data_weight, mc_weight = self.projection(kwargs) 

		if channel in ["mt", "et", "em", "tt", "mm"]:
			Samples._add_input(
					config,
					self.files_vv(channel),
					self.root_file_folder(channel),
					lumi,
					mc_weight+weight+"*eventWeight*" + self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type),
					"vv",
					nick_suffix=nick_suffix
			)
		else:
			log.error("Sample config (VV) currently not implemented for channel \"%s\"!" % channel)
		if not kwargs.get("mssm", False):
			Samples._add_bin_corrections(config, "vv", nick_suffix)
		
		if channel in ["mt", "et"] and fakefactor_method == "standard":
			config["weights"][config["nicks"].index("vv")] = config["weights"][config["nicks"].index("vv")]  + "*(gen_match_2 != 6)"
		if channel in ["mt", "et"] and fakefactor_method == "comparison":
			config["weights"][config["nicks"].index("vv")] = config["weights"][config["nicks"].index("vv")]  + "*(gen_match_2 == 6)"
		
		Samples._add_plot(config, "bkg", "HIST", "F", "vv", nick_suffix)
		return config

	def files_wj(self, channel):
		# W + N jets from MiniAODv2
		query = { "data" : False,
						"campaign" : self.mc_campaign + "2",
						"generator" : "madgraph-pythia8",
						"process" : "(W1JetsToLNu|W2JetsToLNu|W3JetsToLNu|W4JetsToLNu)"}
		artus_files = self.artus_file_names(query, 4)
		# inclusive W+jets sample from MiniAODv1
		query["process"] = "WJetsToLNu"
		query["campaign"] = self.mc_campaign + "1"
		artus_files = artus_files + " " + self.artus_file_names(query, 1)
		return artus_files

	def wj(self, config, channel, category, weight, nick_suffix, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", fakefactor_method=None, estimationMethod="classic", controlregions=False,**kwargs):
		if exclude_cuts is None:
			exclude_cuts = []

		scale_factor = lumi
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("WJets", 1.0)

		data_weight, mc_weight = self.projection(kwargs) 

		if channel in ["mt", "et"]:
			if estimationMethod == "new":
				Samples._add_input(
						config,
						self.files_ztt(channel),
						self.root_file_folder(channel),
						lumi,
						mc_weight+weight+"*eventWeight*" + Samples.ztt_genmatch(channel) + self._cut_string(channel, exclude_cuts=exclude_cuts+["mt"], cut_type=cut_type) + "*(mt_1>70.0)",
						("noplot_" if not controlregions else "") + "ztt_os_highmt",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						self.files_zll(channel),
						self.root_file_folder(channel),
						lumi,
						mc_weight+weight+"*eventWeight*" + Samples.zll_genmatch(channel) + self._cut_string(channel, exclude_cuts=exclude_cuts+["mt"], cut_type=cut_type) + "*(mt_1>70.0)",
						("noplot_" if not controlregions else "") + "zll_os_highmt",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						self.files_ztt(channel),
						self.root_file_folder(channel),
						lumi,
						mc_weight+weight+"*eventWeight*" + Samples.zl_genmatch(channel) + self._cut_string(channel, exclude_cuts=exclude_cuts+["mt"], cut_type=cut_type) + "*(mt_1>70.0)",
						("noplot_" if not controlregions else "") + "zl_os_highmt",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						self.files_ztt(channel),
						self.root_file_folder(channel),
						lumi,
						mc_weight+weight+"*eventWeight*" + Samples.zj_genmatch(channel) + self._cut_string(channel, exclude_cuts=exclude_cuts+["mt"], cut_type=cut_type) + "*(mt_1>70.0)",
						("noplot_" if not controlregions else "") + "zj_os_highmt",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						self.files_ttj(channel),
						self.root_file_folder(channel),
						lumi,
						mc_weight+weight+"*eventWeight*" + self._cut_string(channel, exclude_cuts=exclude_cuts+["mt"], cut_type=cut_type) + "*(mt_1>70.0)",
						("noplot_" if not controlregions else "") + "ttj_os_highmt",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						self.files_vv(channel),
						self.root_file_folder(channel),
						lumi,
						mc_weight+weight+"*eventWeight*" + self._cut_string(channel, exclude_cuts=exclude_cuts+["mt"], cut_type=cut_type) + "*(mt_1>70.0)",
						("noplot_" if not controlregions else "") + "vv_os_highmt",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						self.files_data(channel),
						self.root_file_folder(channel),
						1.0,
						data_weight+weight+"*eventWeight*" + self._cut_string(channel, exclude_cuts=exclude_cuts+["mt"], cut_type=cut_type) + "*(mt_1>70.0)",
						("noplot_" if not controlregions else "") + "data_os_highmt",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						self.files_wj(channel),
						self.root_file_folder(channel),
						lumi,
						mc_weight+weight+"*eventWeight*" + self._cut_string(channel, exclude_cuts=exclude_cuts+["mt"], cut_type=cut_type) + "*(mt_1>70.0)",
						("noplot_" if not controlregions else "") + "wj_os_highmt",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						self.files_ztt(channel),
						self.root_file_folder(channel),
						lumi,
						mc_weight+weight+"*eventWeight*" + Samples.ztt_genmatch(channel) + self._cut_string(channel, exclude_cuts=exclude_cuts+["mt", "os"], cut_type=cut_type) + "*(mt_1>70.0)*((q_1*q_2)>0.0)",
						("noplot_" if not controlregions else "") + "ztt_ss_highmt",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						self.files_zll(channel),
						self.root_file_folder(channel),
						lumi,
						mc_weight+weight+"*eventWeight*" + Samples.zll_genmatch(channel) + self._cut_string(channel, exclude_cuts=exclude_cuts+["mt", "os"], cut_type=cut_type) + "*(mt_1>70.0)*((q_1*q_2)>0.0)",
						("noplot_" if not controlregions else "") + "zll_ss_highmt",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						self.files_zll(channel),
						self.root_file_folder(channel),
						lumi,
						mc_weight+weight+"*eventWeight*" + Samples.zl_genmatch(channel) + self._cut_string(channel, exclude_cuts=exclude_cuts+["mt", "os"], cut_type=cut_type) + "*(mt_1>70.0)*((q_1*q_2)>0.0)",
						("noplot_" if not controlregions else "") + "zl_ss_highmt",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						self.files_zll(channel),
						self.root_file_folder(channel),
						lumi,
						mc_weight+weight+"*eventWeight*" + Samples.zj_genmatch(channel) + self._cut_string(channel, exclude_cuts=exclude_cuts+["mt", "os"], cut_type=cut_type) + "*(mt_1>70.0)*((q_1*q_2)>0.0)",
						("noplot_" if not controlregions else "") + "zj_ss_highmt",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						self.files_ttj(channel),
						self.root_file_folder(channel),
						lumi,
						mc_weight+weight+"*eventWeight*" + self._cut_string(channel, exclude_cuts=exclude_cuts+["mt", "os"], cut_type=cut_type) + "*(mt_1>70.0)*((q_1*q_2)>0.0)",
						("noplot_" if not controlregions else "") + "ttj_ss_highmt",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						self.files_vv(channel),
						self.root_file_folder(channel),
						lumi,
						mc_weight+weight+"*eventWeight*" + self._cut_string(channel, exclude_cuts=exclude_cuts+["mt", "os"], cut_type=cut_type) + "*(mt_1>70.0)*((q_1*q_2)>0.0)",
						("noplot_" if not controlregions else "") + "vv_ss_highmt",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						self.files_data(channel),
						self.root_file_folder(channel),
						1.0,
						data_weight+weight+"*eventWeight*" + self._cut_string(channel, exclude_cuts=exclude_cuts+["mt", "os"], cut_type=cut_type) + "*(mt_1>70.0)*((q_1*q_2)>0.0)",
						("noplot_" if not controlregions else "") + "data_ss_highmt",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						self.files_wj(channel),
						self.root_file_folder(channel),
						lumi,
						mc_weight+weight+"*eventWeight*" + self._cut_string(channel, exclude_cuts=exclude_cuts+["mt", "os"], cut_type=cut_type) + "*((q_1*q_2)>0.0)*(mt_1>70.0)",
						("noplot_" if not controlregions else "") + "wj_ss_highmt",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						self.files_wj(channel),
						self.root_file_folder(channel),
						lumi,
						mc_weight+weight+"*eventWeight*" + self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type),
						"wj",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						self.files_wj(channel),
						self.root_file_folder(channel),
						lumi,
						mc_weight+weight+"*eventWeight*" + self._cut_string(channel, exclude_cuts=exclude_cuts+["mt"], cut_type=cut_type),
						"noplot_wj_mc_os_inclusive",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						self.files_wj(channel),
						self.root_file_folder(channel),
						lumi,
						mc_weight+weight+"*eventWeight*" + self._cut_string(channel, exclude_cuts=exclude_cuts+["mt", "os"], cut_type=cut_type) + "*((q_1*q_2)>0.0)",
						"noplot_wj_mc_ss_inclusive",
						nick_suffix=nick_suffix
				)
				if not "EstimateWjetsAndQCD" in config.get("analysis_modules", []):
					config.setdefault("analysis_modules", []).append("EstimateWjetsAndQCD")
				if controlregions:
					config.setdefault("wjets_ss_substract_nicks", []).append(" ".join([nick+nick_suffix for nick in "ztt_ss_highmt zll_ss_highmt ttj_ss_highmt vv_ss_highmt".split()]))
					config.setdefault("wjets_ss_data_nicks", []).append("data_ss_highmt"+nick_suffix)
					config.setdefault("wjets_os_substract_nicks", []).append(" ".join([nick+nick_suffix for nick in "ztt_os_highmt zll_os_highmt ttj_os_highmt vv_os_highmt".split()]))
					config.setdefault("wjets_os_data_nicks", []).append("data_os_highmt"+nick_suffix)
					config.setdefault("wjets_shape_nicks", []).append("wj"+nick_suffix)
					config.setdefault("wjets_ss_mc_nicks", []).append("noplot_wj_mc_ss_inclusive"+nick_suffix)
					config.setdefault("wjets_ss_highmt_mc_nicks", []).append("wj_ss_highmt"+nick_suffix)
					config.setdefault("wjets_os_mc_nicks", []).append("noplot_wj_mc_os_inclusive"+nick_suffix)
					config.setdefault("wjets_os_highmt_mc_nicks", []).append("wj_os_highmt"+nick_suffix)
					config.setdefault("wjets_os_lowmt_mc_nicks", []).append("wj"+nick_suffix)
					for nick in ["ztt_os_highmt", "zll_os_highmt", "zl_os_highmt", "zj_os_highmt", "ttj_os_highmt", "vv_os_highmt", "data_os_highmt", "wj_os_highmt", "ztt_ss_highmt", "zll_ss_highmt", "zl_ss_highmt", "zj_ss_highmt", "ttj_ss_highmt", "vv_ss_highmt", "data_ss_highmt", "wj_ss_highmt"]:
						if not kwargs.get("mssm", False):
							Samples._add_bin_corrections(config, nick, nick_suffix)
						Samples._add_plot(config, "bkg", "HIST", "F", nick, nick_suffix)
				else:
					config.setdefault("wjets_ss_substract_nicks", []).append(" ".join(["noplot_"+nick+nick_suffix for nick in "ztt_ss_highmt zll_ss_highmt ttj_ss_highmt vv_ss_highmt".split()]))
					config.setdefault("wjets_ss_data_nicks", []).append("noplot_data_ss_highmt"+nick_suffix)
					config.setdefault("wjets_os_substract_nicks", []).append(" ".join(["noplot_"+nick+nick_suffix for nick in "ztt_os_highmt zll_os_highmt ttj_os_highmt vv_os_highmt".split()]))
					config.setdefault("wjets_os_data_nicks", []).append("noplot_data_os_highmt"+nick_suffix)
					config.setdefault("wjets_shape_nicks", []).append("wj"+nick_suffix)
					config.setdefault("wjets_ss_mc_nicks", []).append("noplot_wj_mc_ss_inclusive"+nick_suffix)
					config.setdefault("wjets_ss_highmt_mc_nicks", []).append("noplot_wj_ss_highmt"+nick_suffix)
					config.setdefault("wjets_os_mc_nicks", []).append("noplot_wj_mc_os_inclusive"+nick_suffix)
					config.setdefault("wjets_os_highmt_mc_nicks", []).append("noplot_wj_os_highmt"+nick_suffix)
					config.setdefault("wjets_os_lowmt_mc_nicks", []).append("wj"+nick_suffix)

			if estimationMethod == "classic":
				shape_weight = mc_weight+weight+"*eventWeight*" + self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)
				#if (not category is None) and (category != ""):
					## relaxed isolation
					#shape_weight = weight+"*eventWeight*" + self._cut_string(channel, exclude_cuts=exclude_cuts+["blind", "iso_2"], cut_type=cut_type) + "*(byCombinedIsolationDeltaBetaCorrRaw3Hits_2<10.0)"

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
						data_weight+"eventWeight*" + self._cut_string(channel, exclude_cuts=exclude_cuts+["mt"], cut_type=cut_type) + "*(mt_1>70.0)",
						"noplot_wj_data_control",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						self.files_ztt(channel),
						self.root_file_folder(channel),
						lumi,
						mc_weight+"eventWeight*" + Samples.ztt_genmatch(channel) + self._cut_string(channel, exclude_cuts=exclude_cuts+["mt"], cut_type=cut_type) + "*(mt_1>70.0)",
						"noplot_ztt_mc_wj_control",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						self.files_zll(channel),
						self.root_file_folder(channel),
						lumi,
						mc_weight+"eventWeight*" + Samples.zll_genmatch(channel) + self._cut_string(channel, exclude_cuts=exclude_cuts+["mt"], cut_type=cut_type) + "*(mt_1>70.0)",
						"noplot_zll_wj_control",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						self.files_ttj(channel),
						self.root_file_folder(channel),
						lumi,
						mc_weight+"eventWeight*" + self._cut_string(channel, exclude_cuts=exclude_cuts+["mt"], cut_type=cut_type) + "*(mt_1>70.0)",
						"noplot_ttj_wj_control",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						self.files_vv(channel),
						self.root_file_folder(channel),
						lumi,
						mc_weight+"eventWeight*" + self._cut_string(channel, exclude_cuts=exclude_cuts+["mt"], cut_type=cut_type) + "*(mt_1>70.0)",
						"noplot_vv_wj_control",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						self.files_wj(channel),
						self.root_file_folder(channel),
						lumi,
						mc_weight+weight+"*eventWeight*" + self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type),
						"noplot_wj_mc_signal",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						self.files_wj(channel),
						self.root_file_folder(channel),
						lumi,
						mc_weight+"eventWeight*" + self._cut_string(channel, exclude_cuts=exclude_cuts+["mt"], cut_type=cut_type) + "*(mt_1>70.0)",
						"noplot_wj_mc_control",
						nick_suffix=nick_suffix
				)

				if not "EstimateWjets" in config.get("analysis_modules", []):
					config.setdefault("analysis_modules", []).append("EstimateWjets")
				if channel in ["mt", "et"] and fakefactor_method == "standard":
					config["weights"][config["nicks"].index("wj")] = config["weights"][config["nicks"].index("wj")]  + "*(gen_match_2 != 6)"
					config.setdefault("wjets_from_mc", []).append(True)
				if channel in ["mt", "et"] and fakefactor_method == "comparison":
					config["weights"][config["nicks"].index("wj")] = config["weights"][config["nicks"].index("wj")]  + "*(gen_match_2 == 6)"
					config.setdefault("wjets_from_mc", []).append(False)
				if fakefactor_method is None:
					config.setdefault("wjets_from_mc", []).append(False)
				config.setdefault("wjets_shape_nicks", []).append("wj"+nick_suffix)
				config.setdefault("wjets_data_control_nicks", []).append("noplot_wj_data_control"+nick_suffix)
				config.setdefault("wjets_data_substract_nicks", []).append(" ".join([nick+nick_suffix for nick in "noplot_ztt_mc_wj_control noplot_zll_wj_control noplot_ttj_wj_control noplot_vv_wj_control".split()]))
				config.setdefault("wjets_mc_signal_nicks", []).append("noplot_wj_mc_signal"+nick_suffix)
				config.setdefault("wjets_mc_control_nicks", []).append("noplot_wj_mc_control"+nick_suffix)

		elif channel in ["em", "tt", "mm"]:
			Samples._add_input(
					config,
					self.files_wj(channel),
					self.root_file_folder(channel),
					lumi,
					weight+"*eventWeight*" + self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type),
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

		scale_factor = 1.0
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("QCD", 1.0)

		data_weight, mc_weight = self.projection(kwargs) 

		if channel in ["et", "mt", "em", "tt", "mm"]:
			if estimationMethod == "classic":
				# WJets for QCD estimate
				Samples._add_input(
						config,
						self.files_wj(channel),
						self.root_file_folder(channel),
						lumi,
						mc_weight+"eventWeight*" + self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=cut_type) + "*((q_1*q_2)>0.0)",
						"noplot_wj_ss",
						nick_suffix=nick_suffix
				)

				if channel in ["mt", "et"]:
					Samples._add_input(
							config,
							self.files_data(channel),
							self.root_file_folder(channel),
							1.0,
							data_weight+"eventWeight*" + self._cut_string(channel, exclude_cuts=exclude_cuts+["os", "mt"], cut_type=cut_type) + "*((q_1*q_2)>0.0)*(mt_1>70.0)",
							"noplot_wj_ss_data_control",
							nick_suffix=nick_suffix
					)
					Samples._add_input(
							config,
							self.files_ztt(channel),
							self.root_file_folder(channel),
							lumi,
							mc_weight+"eventWeight*" + Samples.ztt_genmatch(channel) + self._cut_string(channel, exclude_cuts=exclude_cuts+["os", "mt"], cut_type=cut_type) + "*((q_1*q_2)>0.0)*(mt_1>70.0)",
							"noplot_ztt_ss_mc_wj_control",
							nick_suffix=nick_suffix
					)
					Samples._add_input(
							config,
							self.files_zll(channel),
							self.root_file_folder(channel),
							lumi,
							mc_weight+"eventWeight*" + Samples.zll_genmatch(channel) + self._cut_string(channel, exclude_cuts=exclude_cuts+["os", "mt"], cut_type=cut_type) + "*((q_1*q_2)>0.0)*(mt_1>70.0)",
							"noplot_zll_ss_wj_control",
							nick_suffix=nick_suffix
					)
					Samples._add_input(
							config,
							self.files_ttj(channel),
							self.root_file_folder(channel),
							lumi,
							mc_weight+"eventWeight*" + self._cut_string(channel, exclude_cuts=exclude_cuts+["os", "mt"], cut_type=cut_type) + "*((q_1*q_2)>0.0)*(mt_1>70.0)",
							"noplot_ttj_ss_wj_control",
							nick_suffix=nick_suffix
					)
					Samples._add_input(
							config,
							self.files_vv(channel),
							self.root_file_folder(channel),
							lumi,
							mc_weight+"eventWeight*" + self._cut_string(channel, exclude_cuts=exclude_cuts+["os", "mt"], cut_type=cut_type) + "*((q_1*q_2)>0.0)*(mt_1>70.0)",
							"noplot_vv_ss_wj_control",
							nick_suffix=nick_suffix
					)
					Samples._add_input(
							config,
							self.files_wj(channel),
							self.root_file_folder(channel),
							lumi,
							mc_weight+"eventWeight*" + self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=cut_type) + "*((q_1*q_2)>0.0)",
							"noplot_wj_ss_mc_signal",
							nick_suffix=nick_suffix
					)
					Samples._add_input(
							config,
							self.files_wj(channel),
							self.root_file_folder(channel),
							lumi,
							mc_weight+"eventWeight*" + self._cut_string(channel, exclude_cuts=exclude_cuts+["os", "mt"], cut_type=cut_type) + "*((q_1*q_2)>0.0)*(mt_1>70.0)",
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
				shape_weight = data_weight+weight+"*eventWeight*" + self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=cut_type) + "*((q_1*q_2)>0.0)"
				#if (not category is None) and (category != ""):
					## relaxed/inverted isolation
					#if channel in ["et", "mt"]:
						#shape_weight = weight+"*eventWeight*" + self._cut_string(channel, exclude_cuts=exclude_cuts+["blind", "os", "iso_2"], cut_type=cut_type) + "*((q_1*q_2)>0.0)"+"*(byCombinedIsolationDeltaBetaCorrRaw3Hits_2<10.0)"
					#else:
						#shape_weight = weight+"*eventWeight*" + self._cut_string(channel, exclude_cuts=exclude_cuts+["blind", "os", "iso_1", "iso_2"], cut_type=cut_type) + "*((q_1*q_2)>0.0)"

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
						data_weight+weight+"*eventWeight*" + self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=cut_type) + "*((q_1*q_2)>0.0)",
						"noplot_data_qcd_yield",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						self.files_data(channel),
						self.root_file_folder(channel),
						1.0,
						data_weight+"eventWeight*" + self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=cut_type) + "*((q_1*q_2)>0.0)",
						"noplot_data_qcd_control",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						self.files_ztt(channel),
						self.root_file_folder(channel),
						lumi,
						mc_weight+"eventWeight*" + Samples.ztt_genmatch(channel) + self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=cut_type) + "*((q_1*q_2)>0.0)",
						"noplot_ztt_mc_qcd_control",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						self.files_zll(channel),
						self.root_file_folder(channel),
						lumi,
						mc_weight+"eventWeight*" + Samples.zll_genmatch(channel) + self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=cut_type) + "*((q_1*q_2)>0.0)",
						"noplot_zll_qcd_control",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						self.files_ttj(channel),
						self.root_file_folder(channel),
						lumi,
						mc_weight+"eventWeight*" + self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=cut_type) + "*((q_1*q_2)>0.0)",
						"noplot_ttj_qcd_control",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						self.files_vv(channel),
						self.root_file_folder(channel),
						lumi,
						mc_weight+"eventWeight*" + self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=cut_type) + "*((q_1*q_2)>0.0)",
						"noplot_vv_qcd_control",
						nick_suffix=nick_suffix
				)

				if not "EstimateQcd" in config.get("analysis_modules", []):
					config.setdefault("analysis_modules", []).append("EstimateQcd")
				config.setdefault("qcd_data_shape_nicks", []).append("qcd"+nick_suffix)
				config.setdefault("qcd_data_yield_nicks", []).append("noplot_data_qcd_yield"+nick_suffix)
				config.setdefault("qcd_data_control_nicks", []).append("noplot_data_qcd_control"+nick_suffix)
				config.setdefault("qcd_data_substract_nicks", []).append(" ".join([nick+nick_suffix for nick in "noplot_ztt_mc_qcd_control noplot_zll_qcd_control noplot_ttj_qcd_control noplot_vv_qcd_control noplot_wj_ss".split()]))
				if channel == "em":
					config.setdefault("qcd_extrapolation_factors_ss_os", []).append(2.0 + (0.0 if not "os" in exclude_cuts else 1.0))
				elif channel == "et":
					config.setdefault("qcd_extrapolation_factors_ss_os", []).append(1.0 + (0.0 if not "os" in exclude_cuts else 1.0))
				elif channel == "mt":
					config.setdefault("qcd_extrapolation_factors_ss_os", []).append(1.17 + (0.0 if not "os" in exclude_cuts else 1.0))
				else:
					config.setdefault("qcd_extrapolation_factors_ss_os", []).append(1.06 + (0.0 if not "os" in exclude_cuts else 1.0))
				config.setdefault("qcd_subtract_shape", []).append(True)

			if estimationMethod == "new":
				Samples._add_input(
						config,
						self.files_ztt(channel),
						self.root_file_folder(channel),
						lumi,
						mc_weight+weight+"*eventWeight*" + Samples.ztt_genmatch(channel) + self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=cut_type) + "*((q_1*q_2)>0.0)",
						("noplot_" if not controlregions else "") + "ztt_ss_lowmt",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						self.files_zll(channel),
						self.root_file_folder(channel),
						lumi,
						mc_weight+weight+"*eventWeight*" + Samples.zll_genmatch(channel) + self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=cut_type) + "*((q_1*q_2)>0.0)",
						("noplot_" if not controlregions else "") + "zll_ss_lowmt",
						nick_suffix=nick_suffix
				)
				if channel in ["et","mt"]:
					Samples._add_input(
							config,
							self.files_zll(channel),
							self.root_file_folder(channel),
							lumi,
							mc_weight+weight+"*eventWeight*" + Samples.zl_genmatch(channel) + self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=cut_type) + "*((q_1*q_2)>0.0)",
							("noplot_" if not controlregions else "") + "zl_ss_lowmt",
							nick_suffix=nick_suffix
					)
					Samples._add_input(
							config,
							self.files_zll(channel),
							self.root_file_folder(channel),
							lumi,
							mc_weight+weight+"*eventWeight*" + Samples.zj_genmatch(channel) + self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=cut_type) + "*((q_1*q_2)>0.0)",
							("noplot_" if not controlregions else "") + "zj_ss_lowmt",
							nick_suffix=nick_suffix
					)
				Samples._add_input(
						config,
						self.files_ttj(channel),
						self.root_file_folder(channel),
						lumi,
						mc_weight+weight+"*eventWeight*" + self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=cut_type) + "*((q_1*q_2)>0.0)",
						("noplot_" if not controlregions else "") + "ttj_ss_lowmt",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						self.files_vv(channel),
						self.root_file_folder(channel),
						lumi,
						mc_weight+weight+"*eventWeight*" + self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=cut_type) + "*((q_1*q_2)>0.0)",
						("noplot_" if not controlregions else "") + "vv_ss_lowmt",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						self.files_wj(channel),
						self.root_file_folder(channel),
						lumi,
						mc_weight+weight+"*eventWeight*" + self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=cut_type) + "*((q_1*q_2)>0.0)",
						("noplot_" if not controlregions else "") + "wj_ss_lowmt",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						self.files_data(channel),
						self.root_file_folder(channel),
						1.0,
						data_weight+weight+"*eventWeight*" + self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=cut_type) + "*((q_1*q_2)>0.0)",
						("noplot_" if not controlregions else "") + "data_ss_lowmt",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						self.files_ztt(channel),
						self.root_file_folder(channel),
						lumi,
						(mc_weight+weight+"*eventWeight*" + Samples.ztt_genmatch(channel) + self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=cut_type) + "*((q_1*q_2)>0.0)").replace("nbtag","nloosebtag" if "_btag" in category else "nbtag"),
						"noplot_ztt_shape_ss_qcd_control",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						self.files_zll(channel),
						self.root_file_folder(channel),
						lumi,
						(mc_weight+weight+"*eventWeight*" + Samples.zll_genmatch(channel) + self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=cut_type) + "*((q_1*q_2)>0.0)").replace("nbtag","nloosebtag" if "_btag" in category else "nbtag"),
						"noplot_zll_shape_ss_qcd_control",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						self.files_ttj(channel),
						self.root_file_folder(channel),
						lumi,
						(mc_weight+weight+"*eventWeight*" + self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=cut_type) + "*((q_1*q_2)>0.0)").replace("nbtag","nloosebtag" if "_btag" in category else "nbtag"),
						"noplot_ttj_shape_ss_qcd_control",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						self.files_vv(channel),
						self.root_file_folder(channel),
						lumi,
						(mc_weight+weight+"*eventWeight*" + self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=cut_type) + "*((q_1*q_2)>0.0)").replace("nbtag","nloosebtag" if "_btag" in category else "nbtag"),
						"noplot_vv_shape_ss_qcd_control",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						self.files_wj(channel),
						self.root_file_folder(channel),
						lumi,
						(mc_weight+weight+"*eventWeight*" + self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=cut_type) + "*((q_1*q_2)>0.0)").replace("nbtag","nloosebtag" if "_btag" in category else "nbtag"),
						"noplot_wj_shape_ss_qcd_control",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						self.files_data(channel),
						self.root_file_folder(channel),
						1.0,
						data_weight+weight+"*eventWeight*" + self._cut_string(channel, exclude_cuts=exclude_cuts+["os", "mt"], cut_type=cut_type) + "*((q_1*q_2)>0.0)*(mt_1>70.0)",
						("noplot_" if not controlregions else "") + "qcd_ss_highmt",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						self.files_ztt(channel),
						self.root_file_folder(channel),
						lumi,
						(mc_weight+weight+"*eventWeight*" + Samples.ztt_genmatch(channel) + self._cut_string(channel, exclude_cuts=exclude_cuts+["os", "mt"], cut_type=cut_type) + "*((q_1*q_2)>0.0)*(mt_1>70.0)").replace("nbtag","nloosebtag" if "_btag" in category else "nbtag"),
						"noplot_ztt_shape_ss_highmt",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						self.files_zll(channel),
						self.root_file_folder(channel),
						lumi,
						(mc_weight+weight+"*eventWeight*" + Samples.zll_genmatch(channel) + self._cut_string(channel, exclude_cuts=exclude_cuts+["os", "mt"], cut_type=cut_type) + "*((q_1*q_2)>0.0)*(mt_1>70.0)").replace("nbtag","nloosebtag" if "_btag" in category else "nbtag"),
						"noplot_zll_shape_ss_highmt",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						self.files_ttj(channel),
						self.root_file_folder(channel),
						lumi,
						(mc_weight+weight+"*eventWeight*" + self._cut_string(channel, exclude_cuts=exclude_cuts+["os", "mt"], cut_type=cut_type) + "*((q_1*q_2)>0.0)*(mt_1>70.0)").replace("nbtag","nloosebtag" if "_btag" in category else "nbtag"),
						"noplot_ttj_shape_ss_highmt",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						self.files_vv(channel),
						self.root_file_folder(channel),
						lumi,
						(mc_weight+weight+"*eventWeight*" + self._cut_string(channel, exclude_cuts=exclude_cuts+["os", "mt"], cut_type=cut_type) + "*((q_1*q_2)>0.0)*(mt_1>70.0)").replace("nbtag","nloosebtag" if "_btag" in category else "nbtag"),
						"noplot_vv_shape_ss_highmt",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						self.files_data(channel),
						self.root_file_folder(channel),
						1.0,
						data_weight+weight+"*eventWeight*" + self._cut_string(channel, exclude_cuts=exclude_cuts+["os", "mt"], cut_type=cut_type) + "*(mt_1>70.0)*((q_1*q_2)>0.0)",
						("noplot_" if not controlregions else "") + "qcd_os_highmt",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						self.files_data(channel),
						self.root_file_folder(channel),
						1.0,
						data_weight+weight+"*eventWeight*" + self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=cut_type) + "*((q_1*q_2)>0.0)",
						("noplot_" if not controlregions else "") + "qcd_ss_lowmt",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						self.files_data(channel),
						self.root_file_folder(channel),
						1.0,
						(data_weight+weight+"*eventWeight*" + self._cut_string(channel, exclude_cuts=exclude_cuts+["os"], cut_type=cut_type) + "*((q_1*q_2)>0.0)").replace("nbtag","nloosebtag" if "_btag" in category else "nbtag"),
						"qcd",
						nick_suffix=nick_suffix
				)
				if controlregions:
					if not "EstimateWjetsAndQCD" in config.get("analysis_modules", []):
						config.setdefault("analysis_modules", []).append("EstimateWjetsAndQCD")
					elif channel == "et":
						config.setdefault("qcd_extrapolation_factors_ss_os", []).append(1.0)
					elif channel == "mt":
						config.setdefault("qcd_extrapolation_factors_ss_os", []).append(1.17)
					config.setdefault("qcd_shape_nicks", []).append("qcd"+nick_suffix)
					config.setdefault("qcd_yield_nicks", []).append("data_ss_lowmt"+nick_suffix)
					config.setdefault("qcd_yield_substract_nicks", []).append(" ".join([nick+nick_suffix for nick in "ztt_ss_lowmt zll_ss_lowmt ttj_ss_lowmt vv_ss_lowmt wj_ss_lowmt".split()]))
					config.setdefault("qcd_shape_substract_nicks", []).append(" ".join([nick+nick_suffix for nick in "noplot_ztt_shape_ss_qcd_control noplot_zll_shape_ss_qcd_control noplot_ttj_shape_ss_qcd_control noplot_vv_shape_ss_qcd_control noplot_wj_shape_ss_qcd_control".split()]))
					config.setdefault("qcd_ss_highmt_shape_nicks", []).append("qcd_ss_highmt"+nick_suffix)
					config.setdefault("qcd_ss_lowmt_nicks", []).append("qcd_ss_lowmt"+nick_suffix)
					config.setdefault("qcd_os_highmt_nicks", []).append("qcd_os_highmt"+nick_suffix)
					config.setdefault("qcd_shape_highmt_substract_nicks", []).append(" ".join([nick+nick_suffix for nick in "noplot_ztt_shape_ss_highmt noplot_zll_shape_ss_highmt noplot_ttj_shape_ss_highmt noplot_vv_shape_ss_highmt".split()]))

					if channel in ["et","mt"]:
						for nick in ["ztt_ss_lowmt", "zll_ss_lowmt", "zl_ss_lowmt", "zj_ss_lowmt", "ttj_ss_lowmt", "vv_ss_lowmt", "wj_ss_lowmt","data_ss_lowmt", "qcd_ss_highmt", "qcd_os_highmt", "qcd_ss_lowmt"]:
							if not kwargs.get("mssm", False):
								Samples._add_bin_corrections(config, nick, nick_suffix)
							Samples._add_plot(config, "bkg", "HIST", "F", nick, nick_suffix)
					else:
						for nick in ["ztt_ss_lowmt", "zll_ss_lowmt", "ttj_ss_lowmt", "vv_ss_lowmt", "wj_ss_lowmt","data_ss_lowmt", "qcd_ss_highmt", "qcd_os_highmt", "qcd_ss_lowmt"]:
							if not kwargs.get("mssm", False):
								Samples._add_bin_corrections(config, nick, nick_suffix)
							Samples._add_plot(config, "bkg", "HIST", "F", nick, nick_suffix)

				else:
					if not "EstimateWjetsAndQCD" in config.get("analysis_modules", []):
						config.setdefault("analysis_modules", []).append("EstimateWjetsAndQCD")
					elif channel == "et":
						config.setdefault("qcd_extrapolation_factors_ss_os", []).append(1.0)
					elif channel == "mt":
						config.setdefault("qcd_extrapolation_factors_ss_os", []).append(1.17)
					config.setdefault("qcd_shape_nicks", []).append("qcd"+nick_suffix)
					config.setdefault("qcd_yield_nicks", []).append("noplot_data_ss_lowmt"+nick_suffix)
					config.setdefault("qcd_yield_substract_nicks", []).append(" ".join(["noplot_"+nick+nick_suffix for nick in "ztt_ss_lowmt zll_ss_lowmt ttj_ss_lowmt vv_ss_lowmt wj_ss_lowmt".split()]))
					config.setdefault("qcd_shape_substract_nicks", []).append(" ".join([nick+nick_suffix for nick in "noplot_ztt_shape_ss_qcd_control noplot_zll_shape_ss_qcd_control noplot_ttj_shape_ss_qcd_control noplot_vv_shape_ss_qcd_control noplot_wj_shape_ss_qcd_control".split()]))
					config.setdefault("qcd_ss_highmt_shape_nicks", []).append("noplot_qcd_ss_highmt"+nick_suffix)
					config.setdefault("qcd_ss_lowmt_nicks", []).append("noplot_qcd_ss_lowmt"+nick_suffix)
					config.setdefault("qcd_os_highmt_nicks", []).append("noplot_qcd_os_highmt"+nick_suffix)
					config.setdefault("qcd_shape_highmt_substract_nicks", []).append(" ".join([nick+nick_suffix for nick in "noplot_ztt_shape_ss_highmt noplot_zll_shape_ss_highmt noplot_ttj_shape_ss_highmt noplot_vv_shape_ss_highmt".split()]))
		else:
			log.error("Sample config (QCD) currently not implemented for channel \"%s\"!" % channel)

		if not kwargs.get("no_plot", False):
			if not kwargs.get("mssm", False):
				Samples._add_bin_corrections(config, "qcd", nick_suffix)
			Samples._add_plot(config, "bkg", "HIST", "F", "qcd", nick_suffix)
		return config

	def htt(self, config, channel, category, weight, nick_suffix, higgs_masses, normalise_signal_to_one_pb=False,
	        lumi=default_lumi, exclude_cuts=None, additional_higgs_masses_for_shape=[], mssm=False, normalise_to_sm_xsec=False, **kwargs):
		
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

	def bbh(self, config, channel, category, weight, nick_suffix, higgs_masses, normalise_signal_to_one_pb=False, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []

		scale_factor = lumi
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("bbh", 1.0)

		data_weight, mc_weight = self.projection(kwargs) 

		for mass in higgs_masses:
			if channel in ["tt", "et", "mt", "em"]:
				Samples._add_input(
						config,
						"SUSYGluGluToBBHToTauTauM{mass}_RunIISpring16*_*_13TeV_*AOD_pythia8/*.root".format(mass=str(mass)),
						self.root_file_folder(channel),
						lumi*kwargs.get("scale_signal", 1.0),
						mc_weight+weight+"*eventWeight*" + self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type),
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

	def files_ggh(self, channel, mass=125):
		return self.artus_file_names({"process" : "GluGluHToTauTau_M"+str(mass), "data": False, "campaign" : "RunIISpring16MiniAODv2"}, 1)

	def files_susy_ggh(self, channel, mass=125):
		return self.artus_file_names({"process" : "SUSYGluGluHToTauTau_M"+str(mass), "data": False, "campaign" : self.mc_campaign}, 1)

	def ggh(self, config, channel, category, weight, nick_suffix, higgs_masses, normalise_signal_to_one_pb=False, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", mssm=False, **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []

		scale_factor = lumi
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("ggh", 1.0)

		data_weight, mc_weight = self.projection(kwargs) 

		for mass in higgs_masses:
			if channel in ["tt", "et", "mt", "em", "mm"]:
				Samples._add_input(
						config,
						self.files_ggh(channel) if not mssm else self.files_susy_ggh(channel),
						self.root_file_folder(channel),
						lumi*kwargs.get("scale_signal", 1.0),
						mc_weight+weight+"*eventWeight*" + self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type),
						"ggh"+str(mass)+("_"+str(int(kwargs["scale_signal"])) if kwargs.get("scale_signal", 1.0) != 1.0 else ""),
						nick_suffix=nick_suffix
				)
			else:
				log.error("Sample config (ggH%s) currently not implemented for channel \"%s\"!" % (str(mass), channel))

			if not kwargs.get("no_plot", False):
				if not mssm:
					Samples._add_bin_corrections(
							config,
							"ggh"+str(mass)+("_"+str(int(kwargs["scale_signal"])) if kwargs.get("scale_signal", 1.0) != 1.0 else ""),
							nick_suffix
					)
				Samples._add_plot(
						config,
						"ggh",
						"LINE",
						"L",
						"ggh"+str(mass)+("_"+str(int(kwargs["scale_signal"])) if kwargs.get("scale_signal", 1.0) != 1.0 else ""),
						nick_suffix
				)
		return config

	def files_qqh(self, channel, mass=125):
		return self.artus_file_names({"process" : "VBFHToTauTau_M"+str(mass), "data": False, "campaign" : "RunIISpring16MiniAODv2"}, 1)

	def qqh(self, config, channel, category, weight, nick_suffix, higgs_masses, normalise_signal_to_one_pb=False, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", **kwargs):
		if exclude_cuts is None:
			exclude_cuts = []

		scale_factor = lumi
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("qqH", 1.0)

		data_weight, mc_weight = self.projection(kwargs) 

		for mass in higgs_masses:
			if channel in ["tt", "et", "mt", "em", "mm"]:
				Samples._add_input(
						config,
						self.files_qqh(channel),
						self.root_file_folder(channel),
						lumi*kwargs.get("scale_signal", 1.0),
						mc_weight+weight+"*eventWeight*" + self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type),
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
			if channel in ["tt", "et", "mt", "em", "mm"]:
				Samples._add_input(
						config,
						self.files_wh_minus(channel),
						self.root_file_folder(channel),
						lumi*kwargs.get("scale_signal", 1.0),
						mc_weight+weight+"*eventWeight*" + self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type),
						"wmh"+str(mass)+("_"+str(int(kwargs["scale_signal"])) if kwargs.get("scale_signal", 1.0) != 1.0 else ""),
						nick_suffix=nick_suffix+"_noplot"
				)
				Samples._add_input(
						config,
						self.files_wh_plus(channel),
						self.root_file_folder(channel),
						lumi*kwargs.get("scale_signal", 1.0),
						mc_weight+weight+"*eventWeight*" + self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type),
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
			if channel in ["tt", "et", "mt", "em", "mm"]:
				Samples._add_input(
						config,
						self.files_zh(channel),
						self.root_file_folder(channel),
						lumi*kwargs.get("scale_signal", 1.0),
						mc_weight+weight+"*eventWeight*" + self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type),
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

		data_weight = "(1.0)*"
		
		if channel == "mt":
			Samples._add_input(
					config,
					self.files_data(channel),
					self.root_file_folder(channel),
					1.0,
					data_weight+weight+"*eventWeight*jetToTauFakeWeight_comb*" + self._cut_string(channel, exclude_cuts=exclude_cuts+["iso_2"], cut_type=cut_type)+"*(byTightIsolationMVArun2v1DBoldDMwLT_2 < 0.5)",
					"ff",
					nick_suffix=nick_suffix
			)
		elif channel == "et":
			Samples._add_input(
					config,
					self.files_data(channel),
					self.root_file_folder(channel),
					1.0,
					data_weight+weight+"*eventWeight*jetToTauFakeWeight_comb*" + self._cut_string(channel, exclude_cuts=exclude_cuts+["iso_2"], cut_type=cut_type)+"*(byTightIsolationMVArun2v1DBoldDMwLT_2 < 0.5)",
					"ff",
					nick_suffix=nick_suffix
			)
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
					mc_weight+weight+"*eventWeight*" + self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type),
					"ewk",
					nick_suffix=nick_suffix
			)
		else:
			log.error("Sample config (EWK) currently not implemented for channel \"%s\"!" % channel)
		
		if channel in ["mt", "et"] and fakefactor_method == "standard":
			config["weights"][config["nicks"].index("ewk")] = config["weights"][config["nicks"].index("ewk")]  + "*(gen_match_2 != 6)"
		if channel in ["mt", "et"] and fakefactor_method == "comparison":
			config["weights"][config["nicks"].index("ewk")] = config["weights"][config["nicks"].index("ewk")]  + "*(gen_match_2 == 6)"
		
		Samples._add_plot(config, "bkg", "HIST", "F", "ewk", nick_suffix)
		return config
