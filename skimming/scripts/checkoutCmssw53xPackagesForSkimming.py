#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

from Kappa.SkimmingForKITHiggsToTauTau.logger import getLogger


"""
scram p CMSSW CMSSW_5_3_9
cd CMSSW_5_3_9/src
cmsenv
"""

checkoutCommands = [
	# kappa patch needed
	"cd $CMSSW_BASE/src/",

	# "cvs co -r V00-03-04 -d CMGTools/External UserCode/CMG/CMGTools/External", # patch needed
	"cvs co -r V00-03-23 CommonTools/RecoAlgos",
	"cvs co -r v1-2-3 -d QuarkGluonTagger/EightTeV UserCode/tomc/QuarkGluonTagger/EightTeV",

	# MuMu Twiki
	"addpkg RecoMET/METProducers V03-03-12-02",

	# PU Jet ID as used in TauTau and needed for MVA MET
	# https://twiki.cern.ch/twiki/bin/view/CMS/HiggsToTauTauWorkingSummer2013#MET_regression_MVA_residual_reco
	# https://twiki.cern.ch/twiki/bin/view/CMS/MVAMet
	"cvs co -r METPU_5_3_X_v10 JetMETCorrections/METPUSubtraction",
	"cd JetMETCorrections/METPUSubtraction/test/",
	"./setup.sh",
	"cd ../../../",

	# replace non working RecoTauTag from above by official version
	# https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuidePFTauID#CMSSW_5_3_12
	"rm -rf RecoTauTag",

	#HCP + new discriminants
	"cvs co -r V01-04-25 RecoTauTag/RecoTau",
	"cvs co -r V01-04-13 RecoTauTag/Configuration",
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

