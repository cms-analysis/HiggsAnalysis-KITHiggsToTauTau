
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import copy



class SystematicShiftBase(object):

	def __init__(self, plot_config, name=""):
		self.plot_config = plot_config
		self.name = name
	
	def get_config(self, shift=0.0):
		plot_config = copy.deepcopy(self.plot_config)
		
		if shift > 0.0:
			plot_config["labels"] = ["%s_%sUp" % (label, self.name) for label in plot_config.setdefault("labels", [])]
		elif shift < 0.0:
			plot_config["labels"] = ["%s_%sDown" % (label, self.name) for label in plot_config.setdefault("labels", [])]
		
		return plot_config
	
	@staticmethod
	def add_data():
		return False
	
	@staticmethod
	def add_ztt():
		return False
	
	@staticmethod
	def add_zl():
		return False
	
	@staticmethod
	def add_zj():
		return False
	
	@staticmethod
	def add_ttj():
		return False
	
	@staticmethod
	def add_vv():
		return False
	
	@staticmethod
	def add_wj():
		return False
	
	@staticmethod
	def add_qcd():
		return False
	
	@staticmethod
	def add_ggh():
		return False
	
	@staticmethod
	def add_qqh():
		return False
	
	@staticmethod
	def add_vh():
		return False


class Nominal(SystematicShiftBase):

	def __init__(self, plot_config, name=None): # name argument is ignored
		super(Nominal, self).__init__(plot_config, name=None)
	
	@staticmethod
	def add_data():
		return True
	
	@staticmethod
	def add_ztt():
		return True
	
	@staticmethod
	def add_zl():
		return True
	
	@staticmethod
	def add_zj():
		return True
	
	@staticmethod
	def add_ttj():
		return True
	
	@staticmethod
	def add_vv():
		return True
	
	@staticmethod
	def add_wj():
		return True
	
	@staticmethod
	def add_qcd():
		return True
	
	@staticmethod
	def add_ggh():
		return True
	
	@staticmethod
	def add_qqh():
		return True
	
	@staticmethod
	def add_vh():
		return True

