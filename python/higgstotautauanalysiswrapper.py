# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import Artus.KappaAnalysis.kappaanalysiswrapper as kappaanalysiswrapper


class HiggsToTauTauAnalysisWrapper(kappaanalysiswrapper.KappaAnalysisWrapper):

	def __init__(self):
		super(HiggsToTauTauAnalysisWrapper, self).__init__("HiggsToTauTauAnalysis")

	def _initArgumentParser(self, userArgParsers=None):
		super(HiggsToTauTauAnalysisWrapper, self)._initArgumentParser(userArgParsers)
		self._parser.set_defaults(gc_config_includes=["$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/gc/htt_includes.conf"])
		self._parser.set_defaults(ld_library_paths=["$CMSSW_BASE/src/HiggsAnalysis/HiggsToTauTau/CombineHarvester/CombineTools/lib/"]+self._parser.get_default("ld_library_paths"))

