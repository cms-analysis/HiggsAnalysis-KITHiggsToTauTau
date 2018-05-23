# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.categories as Categories
import HiggsAnalysis.KITHiggsToTauTau.datacards.datacards as datacards
import HiggsAnalysis.KITHiggsToTauTau.datacards.smhttdatacards as smhttdatacards
import CombineHarvester.CombineTools.ch as ch

class FinalStateCPStudiesDatacards(smhttdatacards.SMHttDatacards):
                 
	def __init__(self, higgs_masses=["125"], ttbarFit=False, mmFit=False, year="", noJECuncSplit=False, cb=None, cp_study="rhometh"):
		
		signal_processes = {
			"rhometh" : ["smHcpeven", "susyHcpodd_ALT"],
			"combmeth" : [], # TODO
			"ipmeth" : [], # TODO
		}
		
		super(FinalStateCPStudiesDatacards, self).__init__(
				higgs_masses=higgs_masses,
				ttbarFit=ttbarFit,
				mmFit=mmFit,
				year=year,
				noJECuncSplit=noJECuncSplit,
				cb=cb,
				signal_processes=signal_processes.get(cp_study, []),
		)
		
#		def remove_redundant_signal(obj):
#			if not obj.signal():
#				return False
#			else:
#				if (cp_study == "rhometh") and (obj.process() == "ggH"):
#					return True
#				if (cp_study == "rhometh") and (obj.process() == "qqH"):
#					return True
#				if (cp_study == "rhometh") and (obj.process() == "WH"):
#					return True
#				if (cp_study == "rhometh") and (obj.process() == "ZH"):
#					return True
#				else:
#					return False
#
#				#if any([key in obj.bin().lower() for key in ["twojet", "vbf"]]):
#				#	if (cp_study == "ggh") and (obj.process() == "ggH"):
#				#		return True
#				#	elif (cp_study == "vbf") and (obj.process() == "qqH"):
#				#		return True
#				#	elif cp_study == "final":
#				#		return False # TODO
#				#	else:
#				#		return False
#				#else:
#				#	if any([obj.process() == key for key in cp_signal_processes.get("analysis", [])]):
#				#		return True
#				#	else:
#				#		return False
#		
#		self.cb.FilterProcs(remove_redundant_signal)
#		self.cb.FilterSysts(remove_redundant_signal)
#
#		self.cb.PrintProcs()
