# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import os

import Artus.KappaAnalysis.kappaanalysiswrapper as kappaanalysiswrapper
import Artus.Utility.jsonTools as jsonTools

import HiggsAnalysis.KITHiggsToTauTau.tools as tools


class HiggsToTauTauAnalysisWrapper(kappaanalysiswrapper.KappaAnalysisWrapper):

	def __init__(self):
		super(HiggsToTauTauAnalysisWrapper, self).__init__("HiggsToTauTauAnalysis")

	def _initArgumentParser(self, userArgParsers=None):
		super(HiggsToTauTauAnalysisWrapper, self)._initArgumentParser(userArgParsers)
		self._parser.set_defaults(ld_library_paths=["$CMSSW_BASE/src/HiggsAnalysis/HiggsToTauTau/CombineHarvester/CombineTools/lib/"]+self._parser.get_default("ld_library_paths"))

	def modify_replacing_dict(self):
		self.replacingDict["areafiles"] += " auxiliaries/mva_weights"

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
					new_name = tools.find_common_httpipename(pipeline_renamings.get(pipeline1, pipeline1),
					                                         pipeline_renamings.get(pipeline2, pipeline2))
					pipeline_renamings[pipeline1] = new_name.strip("_").replace("__", "_")
		
		for pipeline in pipelines_to_remove:
			self._config["Pipelines"].pop(pipeline)
		
		for old_name, new_name in pipeline_renamings.iteritems():
			self._config["Pipelines"][new_name] = self._config["Pipelines"].pop(old_name)

	def run(self):
		symlinkBaseDir = os.path.expandvars("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/ArtusOutputs")
		if not os.path.exists(symlinkBaseDir):
			os.makedirs(symlinkBaseDir)
		
		if not self.projectPath is None:
			symlinkDir = os.path.join(symlinkBaseDir, "recent")
			if os.path.islink(symlinkDir):
				os.remove(symlinkDir)
			os.symlink(self.projectPath, symlinkDir)
		
		exitCode = super(HiggsToTauTauAnalysisWrapper, self).run()
		
		if not self.projectPath is None:
			symlinkDir = os.path.join(symlinkBaseDir, os.path.basename(self.projectPath))
			os.symlink(self.projectPath, symlinkDir)
		
		return exitCode
