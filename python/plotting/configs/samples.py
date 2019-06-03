
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import copy

import Artus.Utility.jsonTools as jsonTools

import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.cutstrings as cutstrings
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.expressions as expressions


class SamplesBase(object):

	def __init__(self):
		super(SamplesBase, self).__init__()
		
		self.config = jsonTools.JsonDict({})
		self.postfit_scales = None
		self.expressions = expressions.ExpressionsDict()
		
		self.exclude_cuts = []
		self.period = "run"
		
	
	def get_config(self, samples, channel, category, nick_suffix="", postfit_scales=None, **kwargs):
		self.postfit_scales = postfit_scales
		
		config = copy.deepcopy(self.config)
		
		weights = []
		if not category is None:
			weights.append("({category})".format(category=self.expressions.replace_expressions(category)))
		if "weight" in kwargs:
			weights.append("({weight})".format(weight=kwargs.pop("weight")))
		weight = "(1.0)"
		if len(weights) > 0:
			weight = "(" + ("*".join(weights)) + ")"
		for sample in samples:
			config = sample(self, config, channel, category, weight, nick_suffix, **kwargs)
		
		config["nicks_blacklist"] = ["noplot"]
		#config["file_mode"] = "UPDATE"
		
		return config.doIncludes().doComments()
		
	@staticmethod
	def merge_configs(config1, config2, additional_keys = []):
		""" 
		Merge two configs to one config by appending the second config to the 
		first config.
		"""
		merged_config = copy.deepcopy(config1)
		
		for key in list(set([
				"nicks",
				"directories",
				"files",
				"folders",
				"x_expressions",
				"scale_factors",
				"weights",
				"x_bins",
				"y_bins",
				"z_bins",
				"proxy",
				"proxy_prefixes",
				"histogram_to_scale_nicks",
				"integral_histogram_nicks",
				"scale_by_inverse_integrals",
				"add_nicks",
				"add_result_nicks",
				"sum_nicks",
				"sum_result_nicks",
				"stacks",
				"markers",
				"colors",
				"labels",
				"legend_markers",
				"shape_nicks",
				"yield_nicks",
				"shape_yield_nicks"
		] + additional_keys)):
			if key in merged_config or key in config2:
				merged_config.setdefault(key, []).extend(config2.get(key, []))
		
		for key in [
				"analysis_modules",
		]:
			for item in config2.get(key, []):
				if not item in merged_config.get(key, []):
					merged_config.setdefault(key, []).append(item)
		
		for key, value in config2.iteritems():
			if not key in merged_config:
				merged_config[key] = value
		
		return merged_config

	def _cut_string(self, channel, exclude_cuts=None, cut_type="baseline"):
		if exclude_cuts is None:
			exclude_cuts = []
		for self_exclude_cut in self.exclude_cuts:
			if not self_exclude_cut in exclude_cuts:
				exclude_cuts += self.exclude_cuts
		return self.cut_string(channel, exclude_cuts, cut_type)

	@staticmethod
	def cut_string(channel, exclude_cuts=None, cut_type="baseline"):
		if exclude_cuts is None:
			exclude_cuts = []
		cuts = cutstrings.CutStringsDict._get_cutdict(channel, cut_type)
		cuts_list = [cut for (name, cut) in cuts.iteritems() if not name in exclude_cuts]
		if len(cuts_list) == 0:
			cuts_list.append("1.0")

		return "*".join(cuts_list)
	
	@staticmethod
	def _add_input(config, input_file, folder, scale_factor, weight, nick, nick_suffix="", proxy_prefix=""):
		"""
		Method used to fill the config for a sample with the
		1. input .root-file
		2. the folder in the input root file 
		3. the scaling for the sample
		4. Additional weights 
		5. A nick name 
		"""
		config.setdefault("files", []).append(input_file)
		config.setdefault("folders", []).append(folder)
		config.setdefault("scale_factors", []).append(scale_factor)
		config.setdefault("weights", []).append(weight)
		config.setdefault("nicks", []).append(nick+nick_suffix)
		config.setdefault("tree_draw_options", []).append("proxy" if len(proxy_prefix)>0 else "")
		config.setdefault("proxy_prefixes", []).append(proxy_prefix)
		
		return config
	
	@staticmethod
	def _add_bin_corrections(config, nick, nick_suffix=""):
		if not "BinErrorsOfEmptyBins" in config.get("analysis_modules", []):
			config.setdefault("analysis_modules", []).append("BinErrorsOfEmptyBins")
		config.setdefault("nicks_empty_bins", []).append(nick+nick_suffix)
		
		if not "CorrectNegativeBinContents" in config.get("analysis_modules", []):
			config.setdefault("analysis_modules", []).append("CorrectNegativeBinContents")
		config.setdefault("nicks_correct_negative_bins", []).append(nick+nick_suffix)
		
		return config
		
	@staticmethod
	def _add_plot(config, stack, marker, legend_marker, color_label_key, nick_suffix=""):
		config.setdefault("stacks", []).append(stack)
		config.setdefault("markers", []).append(marker)
		config.setdefault("legend_markers", []).append(legend_marker)
		config.setdefault("colors", []).append(color_label_key)
		config.setdefault("labels", []).append(color_label_key)
		return config

