# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import os

import Artus.KappaAnalysis.kappaanalysiswrapper as kappaanalysiswrapper
import Artus.Utility.jsonTools as jsonTools
import Artus.Utility.tools as tools

import sys

class HiggsToTauTauAnalysisWrapper(kappaanalysiswrapper.KappaAnalysisWrapper):

	def __init__(self):
		super(HiggsToTauTauAnalysisWrapper, self).__init__("HiggsToTauTauAnalysis")

	def _initArgumentParser(self, userArgParsers=None):
		super(HiggsToTauTauAnalysisWrapper, self)._initArgumentParser(userArgParsers)

	def modify_replacing_dict(self):
		self.replacingDict["areafiles"] += " -data/Samples auxiliaries/mva_weights ZZMatrixElement/MELA"

	def remove_pipeline_copies(self):
		pipelines = self._config.get("Pipelines", {}).keys()
		pipelines_to_remove = []
		pipeline_renamings = {}
		for index1, pipeline1 in enumerate(pipelines):
			if pipeline1 in pipelines_to_remove:
				continue

			for pipeline2 in pipelines[index1+1:]:
				if pipeline2 in pipelines_to_remove:
					continue

				difference = jsonTools.JsonDict.deepdiff(self._config["Pipelines"][pipeline1],
				                                         self._config["Pipelines"][pipeline2])
				if len(difference[0]) == 0 and len(difference[1]) == 0:
					pipelines_to_remove.append(pipeline2)
					new_name = tools.find_common_string(pipeline_renamings.get(pipeline1, pipeline1),
					                                    pipeline_renamings.get(pipeline2, pipeline2))
					# Needed for systematic shifts that are only applied to certain samples.
					# In that case we do not want an extra pipeline with the same configuration
					# as the nominal one.
					if "Down" not in new_name or "Up" not in new_name:
						new_name = new_name.replace(new_name.split("_")[-1], "")
					# Add "nominal" to pipelines without systematic shifts
					if new_name.endswith("_"):
						new_name += "nominal"
					elif "_" not in new_name:
						new_name += "_nominal"
					pipeline_renamings[pipeline1] = new_name.strip("_").replace("__", "_")

		for pipeline in pipelines_to_remove:
			self._config["Pipelines"].pop(pipeline)

		for old_name, new_name in pipeline_renamings.iteritems():
			self._config["Pipelines"][new_name] = self._config["Pipelines"].pop(old_name)

	def readInExternals(self):
		if not "NumberGeneratedEvents" in self._config or (int(self._config["NumberGeneratedEvents"]) < 0):
			from Kappa.Skimming.registerDatasetHelper import get_n_generated_events_from_nick
			from Kappa.Skimming.datasetsHelper2015 import isData
			n_events_from_db = get_n_generated_events_from_nick(self._config["Nickname"])
			if(n_events_from_db > 0):
				self._config["NumberGeneratedEvents"] = n_events_from_db
			elif not isData(self._config["Nickname"]):
				log.fatal("Number of Generated Events not set! Check your datasets.json for nick " + self._config["Nickname"])
				sys.exit(1)

		if not ("CrossSection" in self._config) or (self._config["CrossSection"] < 0):
			from Kappa.Skimming.registerDatasetHelper import get_xsec
			from Kappa.Skimming.datasetsHelper2015 import isData
			xsec = get_xsec(self._config["Nickname"])
			if(xsec > 0):
				self._config["CrossSection"] = xsec
			elif not isData(self._config["Nickname"]):
				log.fatal("Cross section for " + self._config["Nickname"] + " not set! Check your datasets.json")
				sys.exit(1)

		if not ("GeneratorWeight" in self._config):
			from Kappa.Skimming.registerDatasetHelper import get_generator_weight
			from Kappa.Skimming.datasetsHelper2015 import isData
			generator_weight = get_generator_weight(self._config["Nickname"])
			if(generator_weight > 0 and generator_weight <= 1.0):
				self._config["GeneratorWeight"] = generator_weight


	def run(self):
		#symlinkBaseDir = os.path.expandvars("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/ArtusOutputs")
		#if not os.path.exists(symlinkBaseDir):
		#	os.makedirs(symlinkBaseDir)
		
		#if not self.projectPath is None:
		#	symlinkDir = os.path.join(symlinkBaseDir, "recent")
		#	if os.path.islink(symlinkDir):
		#		os.remove(symlinkDir)
		#	os.symlink(self.projectPath, symlinkDir)
		
		exitCode = super(HiggsToTauTauAnalysisWrapper, self).run()
		
		#if not self.projectPath is None:
		#	symlinkDir = os.path.join(symlinkBaseDir, os.path.basename(self.projectPath))
		#	os.symlink(self.projectPath, symlinkDir)
		
		return exitCode
