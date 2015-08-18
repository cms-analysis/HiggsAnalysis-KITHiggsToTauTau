# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import os

import Artus.KappaAnalysis.kappaanalysiswrapper as kappaanalysiswrapper


class HiggsToTauTauAnalysisWrapper(kappaanalysiswrapper.KappaAnalysisWrapper):

	def __init__(self):
		super(HiggsToTauTauAnalysisWrapper, self).__init__("HiggsToTauTauAnalysis")

	def _initArgumentParser(self, userArgParsers=None):
		super(HiggsToTauTauAnalysisWrapper, self)._initArgumentParser(userArgParsers)
		self._parser.set_defaults(ld_library_paths=["$CMSSW_BASE/src/HiggsAnalysis/HiggsToTauTau/CombineHarvester/CombineTools/lib/"]+self._parser.get_default("ld_library_paths"))

	def modify_replacing_dict(self):
		self.replacingDict["areafiles"] += " auxiliaries/mva_weights"

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
