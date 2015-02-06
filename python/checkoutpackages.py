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
		
		"svn co https://ekptrac.physik.uni-karlsruhe.de/svn/KITHiggsToTauTau-auxiliaries/trunk HiggsAnalysis/KITHiggsToTauTau/auxiliaries",
		
		# needed by the JetEnergyCorrectionProducer
		"git clone https://github.com/veelken/SVfit_standalone.git TauAnalysis/SVfitStandalone",
		
		# needed for plotting and statistical inference
		"git clone https://github.com/cms-analysis/HiggsAnalysis-HiggsToTauTau.git -d development HiggsAnalysis/HiggsToTauTau",
		"git clone https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit",
		"git clone https://github.com/roger-wolf/HiggsAnalysis-HiggsToTauTau-auxiliaries.git auxiliaries",
	]
	checkoutpackages.execute_commands(commands, max_n_trials=max_n_trials)

