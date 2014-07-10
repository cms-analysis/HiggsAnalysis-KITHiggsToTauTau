#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import sys

import HiggsAnalysis.KITHiggsToTauTau.higgstotautauanalysiswrapper as higgstotautauanalysiswrapper


if __name__ == "__main__":

	higgsToTauTauAnalysisWrapper = higgstotautauanalysiswrapper.HiggsToTauTauAnalysisWrapper()
	sys.exit(higgsToTauTauAnalysisWrapper.run())

