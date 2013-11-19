#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import logging
import sys
import os


def main():
	parser = argparse.ArgumentParser(description="Create symbolic links of skimming files in the skimming CMSSW versions.")

	parser.add_argument("skimming_cmssw_base", help="Path to skimming CMSSW base.")
	parser.add_argument("--log-level", default="debug", choices=["debug", "info", "warning", "error", "critical"], help="Log level. [Default: debug]")

	args = parser.parse_args()

	logging.basicConfig(level=getattr(logging, args.log_level.upper(), "DEBUG"),
	                    format="%(levelname)s: %(message)s")
	logger = logging.getLogger(sys.argv[0])

	if not os.path.exists(args.skimming_cmssw_base):
		logger.critical("Skimming CMSSW base " + args.skimming_cmssw_base + " does not exist!")
		sys.exit(1)

	destPythonDir = os.path.join(os.path.abspath(args.skimming_cmssw_base), "src/Kappa/Skimming/python/")
	if not os.path.exists(destPythonDir):
		os.makedirs(destPythonDir)

	os.system("rm -rf{V} {DEST_DIR}/*".format(DEST_DIR=destPythonDir,
	                                          V="v" if logger.isEnabledFor(logging.INFO) else ""))
	os.system("ln -s{V} $CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/python/skimming/* {DEST_DIR}".format(
			DEST_DIR=destPythonDir,
			V="v" if logger.isEnabledFor(logging.INFO) else ""))

if __name__ == "__main__":
	main()
