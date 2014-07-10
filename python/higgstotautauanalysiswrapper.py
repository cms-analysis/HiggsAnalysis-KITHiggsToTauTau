# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import Artus.Configuration.artusWrapper as artusWrapper


class HiggsToTauTauAnalysisWrapper(artusWrapper.ArtusWrapper):

	def __init__(self):
		super(HiggsToTauTauAnalysisWrapper, self).__init__("HiggsToTauTauAnalysis")

	def _initArgumentParser(self, userArgParsers=None):
		super(HiggsToTauTauAnalysisWrapper, self)._initArgumentParser(userArgParsers)
		self._parser.set_defaults(gc_config_includes=["$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/gc/htt_includes.conf"])

