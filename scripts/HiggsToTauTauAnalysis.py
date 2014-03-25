#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import sys
from Artus.Configuration.artusWrapper import ArtusWrapper


if __name__ == "__main__":

	artusWrapper = ArtusWrapper("HiggsToTauTauAnalysis")
	sys.exit(artusWrapper.run())

