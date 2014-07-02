# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import os
import sys

import Artus.KappaAnalysis.checkoutpackages as checkoutpackages


def checkout_packages(max_n_trials=2):
	commands = [
		"cd $CMSSW_BASE/src",
		
		# needed by the JetEnergyCorrectionProducer
		"git clone https://github.com/veelken/SVfit_standalone.git TauAnalysis/SVfitStandalone",
	]
	checkoutpackages.execute_commands(commands, max_n_trials=max_n_trials)

