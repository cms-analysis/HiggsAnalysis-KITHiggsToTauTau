
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

from HiggsAnalysis.KITHiggsToTauTau.plotting.configs.systematics import *



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

