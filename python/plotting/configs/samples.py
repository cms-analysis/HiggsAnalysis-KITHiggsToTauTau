
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import copy

import Artus.Utility.jsonTools as jsonTools


class SamplesBase(object):

	def __init__(self):
		super(SamplesBase, self).__init__()
		
		self.config = jsonTools.JsonDict({})
		self.postfit_scales = None
	
	def get_config(self, samples, channel, category, nick_suffix="", postfit_scales=None, **kwargs):
		self.postfit_scales = postfit_scales
		
		config = copy.deepcopy(self.config)
		
		for sample in samples:
			config = sample(self, config, channel, category, nick_suffix, **kwargs)
		
		if not category is None:
			config["weights"] = [weight+("*(isCat%s>0)" % category) for weight in config.setdefault("weights", [])]
		
		config["nicks_blacklist"] = ["noplot"]
		#config["file_mode"] = "UPDATE"
		
		return config.doIncludes().doComments()
		
	@staticmethod
	def merge_configs(config1, config2, additional_keys = []):
		merged_config = copy.deepcopy(config1)
		
		for key in [
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
				"histogram_to_scale_nicks",
				"integral_histogram_nicks",
				"scale_by_inverse_integrals",
				"histogram_nicks",
				"sum_result_nicks",
				"stacks",
				"markers",
				"colors",
				"labels",
				"legend_markers"
		] + additional_keys:
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
	
	@staticmethod
	def _add_input(config, input_file, folder, scale_factor, weight, nick, nick_suffix=""):
		config.setdefault("files", []).append(input_file)
		config.setdefault("folders", []).append(folder)
		config.setdefault("scale_factors", []).append(scale_factor)
		config.setdefault("weights", []).append(weight)
		config.setdefault("nicks", []).append(nick+nick_suffix)
		return config
		
	@staticmethod
	def _add_plot(config, stack, marker, legend_marker, color_label_key, nick_suffix=""):
		config.setdefault("stacks", []).append(stack+nick_suffix)
		config.setdefault("markers", []).append(marker)
		config.setdefault("legend_markers", []).append(legend_marker)
		config.setdefault("colors", []).append(color_label_key)
		config.setdefault("labels", []).append(color_label_key)
		return config

