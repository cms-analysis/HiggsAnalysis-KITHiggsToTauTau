#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import argparse


if __name__ == "__main__":

	parser = argparse.ArgumentParser(description="Print commands for statistical inference studies of SMLegacyDatacards datacards.",
	                                 parents=[logger.loggingParser])
	
	args = parser.parse_args()
	logger.initLogger(args)
	
	commands = [
		"SMLegacyDatacards",
		"limit.py --stable-new --max-likelihood output/sm_cards/*/",
		"submit.py --stable-new --multidim-fit --physics-model cV-cF output/sm_cards/125/ --lxq --queue=\"-l h_vmem=4000M -l h_rt=00:30:00 -l distro=sld6\"",
		"submit.py --stable-new --multidim-fit --physics-model cV-cF output/sm_cards/125/ --lxq --queue=\"-l h_vmem=4000M -l h_rt=00:30:00 -l distro=sld6\" --collect",
		"limit.py --stable-new --multidim-fit --physics-model cV-cF output/sm_cards/125/ --algo grid",
	]
	log.info("\n".join(commands))

