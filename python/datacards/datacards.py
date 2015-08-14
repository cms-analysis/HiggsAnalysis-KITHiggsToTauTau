# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import copy
import os

# http://cms-analysis.github.io/HiggsAnalysis-HiggsToTauTau/python-interface.html
import combineharvester as ch

import HiggsAnalysis.KITHiggsToTauTau.datacards.datacardconfigs as datacardconfigs


class Datacards(object):
	def __init__(self, cb=None):
		super(Datacards, self).__init__()
		
		self.cb = cb
		if self.cb is None:
			self.cb = ch.CombineHarvester()
		if log.isEnabledFor(logging.DEBUG):
			self.cb.SetVerbosity(1)
		
		self.configs = datacardconfigs.DatacardConfigs()
		
		self.lumi_syst_args = [
			"lumi_$ERA",
			"lnN",
			ch.SystMap("era")
				( ["7TeV"], 1.026)
				( ["8TeV"], 1.026)
				(["13TeV"], 1.026)
		]
	
	def add_processes(self, channel, categories, bkg_processes, sig_processes=["ztt"], *args, **kwargs):
		bin = [(self.configs.category2binid(category), category) for category in categories]
		
		for key in ["channel", "procs", "bin", "signal"]:
			if key in kwargs:
				kwargs.pop(key)
		
		non_sig_kwargs = copy.deepcopy(kwargs)
		if "mass" in non_sig_kwargs:
			non_sig_kwargs.pop("mass")
		
		self.cb.AddObservations(channel=[channel], mass=["*"], bin=bin, *args, **non_sig_kwargs)
		self.cb.AddProcesses(channel=[channel], mass=["*"], procs=bkg_processes, bin=bin, signal=False, *args, **non_sig_kwargs)
		self.cb.AddProcesses(channel=[channel], mass=["90"], procs=sig_processes, bin=bin, signal=True, *args, **kwargs)
	
	def extract_shapes(self, root_filename_template, histogram_name_template, syst_histogram_name_template):
		for analysis in self.cb.analysis_set():
			for era in self.cb.cp().analysis([analysis]).era_set():
				for channel in self.cb.cp().analysis([analysis]).era([era]).channel_set():
					root_filename = root_filename_template.format(
							ANALYSIS=analysis,
							CHANNEL=channel,
							ERA=era
					)
					self.cb.cp().analysis([analysis]).era([era]).channel([channel]).ExtractShapes(root_filename, histogram_name_template, syst_histogram_name_template)
		
		if log.isEnabledFor(logging.DEBUG):
			self.cb.PrintAll()
	
	def write_datacards(self, datacard_filename_template, root_filename_template, output_directory="."):
		writer = ch.CardWriter(os.path.join(output_directory, datacard_filename_template),
		                       os.path.join(output_directory, root_filename_template))
		if log.isEnabledFor(logging.DEBUG):
			writer.PrintAll()
		
		# TODO: writer.WriteCards seems to ignore output_directory, therefore it is added to ch.CardWriter
		writer.WriteCards(output_directory, self.cb)

