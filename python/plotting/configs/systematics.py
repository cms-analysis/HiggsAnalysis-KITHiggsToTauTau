
# -*- coding: utf-8 -*-

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
	def add_wjets():
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
	def add_wjets():
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


class TauEsSystematic(SystematicShiftBase):
	
	def get_config(self, shift=0.0):
		plot_config = super(TauEsSystematic, self).get_config(shift=shift)
		
		if shift > 0.0:
			plot_config["files"] = [input_file.replace("tauEsNom", "tauEsUp") for input_file in plot_config.setdefault("files", [])]
		elif shift < 0.0:
			plot_config["files"] = [input_file.replace("tauEsNom", "tauEsDown") for input_file in plot_config.setdefault("files", [])]
		
		return plot_config
	
	@staticmethod
	def add_ztt():
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


class SvfitMassSystematic(SystematicShiftBase):
	
	def get_config(self, shift=0.0):
		plot_config = super(SvfitMassSystematic, self).get_config(shift=shift)
		
		plot_config["x_expressions"] = ["((%s) * %f)" % (x, 1.0+0.02*shift) if x == "m_sv" else x for x in plot_config.setdefault("x_expressions", [])]
		
		return plot_config
	
	@staticmethod
	def add_zl():
		return True

