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
		
		"git clone https://github.com/cms-analysis/HiggsAnalysis-KITHiggsToTauTau.wiki.git HiggsAnalysis/KITHiggsToTauTau/doc/wiki",
		
		"svn co https://ekptrac.physik.uni-karlsruhe.de/svn/KITHiggsToTauTau-auxiliaries/trunk HiggsAnalysis/KITHiggsToTauTau/auxiliaries",
		
		# needed by the JetEnergyCorrectionProducer
		"git clone https://github.com/veelken/SVfit_standalone.git -b svFit_2015Apr03 TauAnalysis/SVfitStandalone",
		
		# needed for plotting and statistical inference
		"git clone https://github.com/cms-analysis/HiggsAnalysis-HiggsToTauTau.git HiggsAnalysis/HiggsToTauTau",
		"git clone https://github.com/cms-analysis/CombineHarvester.git CombineHarvester",
		"git clone https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git -b slc6-root5.34.17 HiggsAnalysis/CombinedLimit",
		"git clone https://github.com/roger-wolf/HiggsAnalysis-HiggsToTauTau-auxiliaries.git auxiliaries",
		
		# needed for error propagation e.g. in the background estimations
		"git clone https://github.com/lebigot/uncertainties.git -b 2.4.6.1 HiggsAnalysis/KITHiggsToTauTau/python/uncertainties",
		
		# needed for running the HHKinFit
		"git clone https://github.com/thomas-mueller/HHKinFit2.git",
	]
	checkoutpackages.execute_commands(commands, max_n_trials=max_n_trials)

