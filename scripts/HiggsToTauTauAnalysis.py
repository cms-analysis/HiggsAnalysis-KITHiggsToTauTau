#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from Artus.Configuration.artusWrapper import ArtusWrapper


if __name__ == "__main__":

	artusWrapper = ArtusWrapper("HiggsToTauTauAnalysis")
	sys.exit(artusWrapper.run())

