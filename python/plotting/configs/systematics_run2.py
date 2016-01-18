
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
		
		for channel in ["em", "et"]:
			self["CMS_scale_e_"+channel+"_13TeV"] = EleEsSystematic


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
		
		for index, folder in enumerate(plot_config.get("folders", [])):
			if not "data" in plot_config["nicks"][index]:
				if shift > 0.0:
					plot_config["folders"][index] = folder.replace("jecUncNom", "jecUncUp")
				elif shift < 0.0:
					plot_config["folders"][index] = folder.replace("jecUncNom", "jecUncDown")
		
		return plot_config


class TauEsSystematic(SystematicShiftBase):
	
	def get_config(self, shift=0.0):
		plot_config = super(TauEsSystematic, self).get_config(shift=shift)
		
		for index, folder in enumerate(plot_config.get("folders", [])):
			if not "data" in plot_config["nicks"][index]:
				if shift > 0.0:
					plot_config["folders"][index] = folder.replace("tauEsNom", "tauEsUp")
				elif shift < 0.0:
					plot_config["folders"][index] = folder.replace("tauEsNom", "tauEsDown")
		
		return plot_config


class EleEsSystematic(SystematicShiftBase):
	
	def get_config(self, shift=0.0):
		plot_config = super(EleEsSystematic, self).get_config(shift=shift)
		
		for index, folder in enumerate(plot_config.get("folders", [])):
			if not "data" in plot_config["nicks"][index]:
				if shift > 0.0:
					plot_config["folders"][index] = folder.replace("eleUncNom", "eleUncUp")
				elif shift < 0.0:
					plot_config["folders"][index] = folder.replace("eleUncNom", "eleUncDown")
		
		return plot_config
