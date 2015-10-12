
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import copy


class SystematicsFactory(dict):
	def __init__(self):
		super(SystematicsFactory, self).__init__()
		
		self["nominal"] = Nominal
		self["CMS_scale_j_13TeV"] = JecUncSystematic
		
		for channel in ["mt", "et", "tt"]:
			self["CMS_scale_t_"+channel+"_13TeV"] = TauEsSystematic


class SystematicShiftBase(object):

	def __init__(self, plot_config):
		super(SystematicShiftBase, self).__init__()
		self.plot_config = plot_config
	
	def get_config(self, shift=0.0):
		plot_config = copy.deepcopy(self.plot_config)
		
		if shift != 0.0:
			if "FillEmptyHistograms" not in plot_config.get("analysis_modules", []):
				plot_config.setdefault("analysis_modules", []).append("FillEmptyHistograms")
			# TODO: maybe specify more settings
			# plot_config.setdefault("nicks_fill_empty_histograms", []).append(...)
			# plot_config["fill_empty_histograms_integral"] = 1e-5
		
		return plot_config


class Nominal(SystematicShiftBase):
	pass


class JecUncSystematic(SystematicShiftBase):
	
	def get_config(self, shift=0.0):
		plot_config = super(JecUncSystematic, self).get_config(shift=shift)
		
		if shift > 0.0:
			plot_config["folders"] = [folder.replace("jecUncNom", "jecUncUp") for folder in plot_config.get("folders", [])]
		elif shift < 0.0:
			plot_config["folders"] = [folder.replace("jecUncNom", "jecUncDown") for folder in plot_config.get("folders", [])]
		
		return plot_config


class TauEsSystematic(SystematicShiftBase):
	
	def get_config(self, shift=0.0):
		plot_config = super(TauEsSystematic, self).get_config(shift=shift)
		
		if shift > 0.0:
			plot_config["folders"] = [folder.replace("tauEsNom", "tauEsUp") for folder in plot_config.get("folders", [])]
		elif shift < 0.0:
			plot_config["folders"] = [folder.replace("tauEsNom", "tauEsDown") for folder in plot_config.get("folders", [])]
		
		return plot_config

