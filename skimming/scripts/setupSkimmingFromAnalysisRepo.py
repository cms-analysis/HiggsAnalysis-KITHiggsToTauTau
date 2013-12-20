#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import logging
import sys
import os
sys.path.append("/portal/ekpcms5/home/friese/devel/analysis/CMSSW_6_1_1/src/KITHiggsToTauTau/python/")
from logger import getLogger


def main():
	parser = argparse.ArgumentParser(description="Create symbolic links of skimming files in the skimming CMSSW versions.")

	parser.add_argument("skimming_cmssw_base", help="Path to skimming CMSSW base.")

	logger = getLogger(parser, sys.argv[0])
	args = parser.parse_args()

	if not os.path.exists(args.skimming_cmssw_base):
		logger.critical("Skimming CMSSW base " + args.skimming_cmssw_base + " does not exist!")
		sys.exit(1)

	kappaDir = os.path.join(os.path.abspath(args.skimming_cmssw_base), "src/Kappa/")
	if not os.path.exists(kappaDir):
		logger.critical("Skimming CMSSW base " + kappaDir + " does not exist!")
		sys.exit(1)

	skimmingDir = os.path.join(kappaDir, "SkimmingForKITHiggsToTauTau")
	os.system("rsync -avSzh --delete {V} $CMSSW_BASE/src/KITHiggsToTauTau/skimming/ {SKIMMING_DIR}/".format(
			SKIMMING_DIR=skimmingDir,
			V="--progress" if logger.isEnabledFor(logging.INFO) else ""))
	os.system("rsync -avSzh --delete {V} $CMSSW_BASE/src/KITHiggsToTauTau/python/logger.py {SKIMMING_DIR}/python/".format(
			SKIMMING_DIR=skimmingDir,
			V="--progress" if logger.isEnabledFor(logging.INFO) else ""))

if __name__ == "__main__":
	main()
