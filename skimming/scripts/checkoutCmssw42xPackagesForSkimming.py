#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

from Kappa.SkimmingForKITHiggsToTauTau.logger import getLogger


os.chdir(os.path.expandvars("$CMSSW_BASE/src/"))

checkoutCommands = [
	# kappa patch needed
	"cd $CMSSW_BASE/src/",

	# patch needed
	"cvs co -r V00-03-04 -d CMGTools/External UserCode/CMG/CMGTools/External",
	"cvs co -r V00-03-23 CommonTools/RecoAlgos",
	"cvs co -r v1-2-3 -d QuarkGluonTagger/EightTeV UserCode/tomc/QuarkGluonTagger/EightTeV",

	"cvs co -r METPU_4_2_X_v4 JetMETCorrections/METPUSubtraction",
	"cd JetMETCorrections/METPUSubtraction/test/",
	"./setup42.sh",
	"cd ../../../",
]

for checkoutCommand in checkoutCommands:
	exitCode = 1
	nTrials = 0
	while success != 0:
		if nTrials > 3:
			logger.error("Last command could be executed successfully! Stop program!")
			sys.exit(1)

		logger.info("{CHECKOUT_COMMAND} (trial {N_TRIAL}):".formal(CHECKOUT_COMMAND=checkoutCommand,
	                                                           N_TRIAL=(nTrials+1))

		if checkoutCommand.startswith("cd"):
			exitCode = os.chdir(os.path.expandvars(checkoutCommand.replace("cd ", "")))
		else:
			exitCode = os.system(checkoutCommand)

		nTrials += 1

