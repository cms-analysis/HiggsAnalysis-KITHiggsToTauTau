
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


class SystematicShiftBase(object):

	def __init__(self, plot_config):
		super(SystematicShiftBase, self).__init__()
		self.plot_config = plot_config
	
	def get_config(self, shift=0.0):
		plot_config = copy.deepcopy(self.plot_config)
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

