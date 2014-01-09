#!/usr/bin/env python
# -*- coding: utf-8 -*-

# checkout script for cmssw53x for skimming
# todo: implement logger
# todo: make cmsenv/scramv work

import os
import sys
import argparse

sys.path.append(os.path.abspath(os.path.dirname(sys.argv[0])) + "/../python/")
sys.path.append(os.path.abspath(os.path.dirname(sys.argv[0])) + "/../../python/")

from logger import getLogger
from checkoutScriptsHelper import *


#################################################################################################################


def checkoutPackages(args):
	cmsswsrc = os.popen("echo $CMSSW_BASE").readline().replace("\n", "") + '/src/'

	commands = [
		'cd ' + cmsswsrc,
		# do the git cms-addpkg before starting with checking out cvs repositories

		#PAT
		"git cms-addpkg DataFormats/PatCandidates",
		"git cms-addpkg PhysicsTools/PatAlgos",
		"git cms-addpkg FWCore/GuiBrowsers",

		#Electrons
		"git cms-addpkg EgammaAnalysis/ElectronTools",
		"cd " + cmsswsrc + "EgammaAnalysis/ElectronTools/data/",
		"cat download.url | xargs wget",
		'cd ' + cmsswsrc,

		# MuMu Twiki
		"git cms-addpkg RecoMET/METProducers",

		# "cvs co -r V00-03-04 -d CMGTools/External UserCode/CMG/CMGTools/External", # patch needed
		"git cms-cvs-history import V00-03-23 CommonTools/RecoAlgos",

		# https://twiki.cern.ch/twiki/bin/view/CMS/GluonTag
		"git clone git@github.com:amarini/QuarkGluonTagger.git",
		"cd " + cmsswsrc + "QuarkGluonTagger",
		"git checkout v1-2-3",
		'cd ' + cmsswsrc,

		# PU Jet ID as used in TauTau and needed for MVA MET # does not work with git cms-cvs-history and does not compile with cvs co
		# https://twiki.cern.ch/twiki/bin/view/CMS/HiggsToTauTauWorkingSummer2013#MET_regression_MVA_residual_reco
		# https://twiki.cern.ch/twiki/bin/view/CMS/MVAMet
#		"cvs co -r METPU_5_3_X_v10 JetMETCorrections/METPUSubtraction",
#		"cd " + cmsswsrc + "JetMETCorrections/METPUSubtraction/test"
#		"./setup.sh",
#		'cd ' + cmsswsrc,

		# replace non working RecoTauTag from above by official version
		# https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuidePFTauID#CMSSW_5_3_12
#		"rm -rf RecoTauTag",

		#HCP + new discriminants
		"git cms-cvs-history import V01-04-25 RecoTauTag/RecoTau",
		"git cms-cvs-history import V01-04-13 RecoTauTag/Configuration",

		#Check out Kappa
		"git clone https://ekptrac.physik.uni-karlsruhe.de/git/Kappa",
		"scram b -j 4"
	]
	execCommands(commands)
	return
#################################################################################################################


def main():
	parser = argparse.ArgumentParser(description="Create symbolic links of skimming files in the skimming CMSSW versions.")
	sysInformation = getSysInformation()

	parser.add_argument("--github_username", help="your name as in github. Default: " + sysInformation["github_username"], default=sysInformation["github_username"], nargs='?')
	parser.add_argument("--mail", help="your email. Default: " + sysInformation["email"], default=sysInformation["email"], nargs='?')
	parser.add_argument("--editor", help="your favorite editor (ex. emacs). Default: " + sysInformation["editor"], default=sysInformation["editor"], nargs='?')
	parser.add_argument("--cern_username", help="Your CERN username", default="", nargs='?')
	parser.add_argument("--cmssw_version", help="the CMSSW Version to checko out. Default: CMSSW_5_3_13_patch3", default="CMSSW_5_3_13_patch3", nargs='?')
	parser.add_argument("--no_cmssw_setup", help="Do not set up CMSSW environement", action='store_false')
	parser.add_argument("--no_packages_checkout", help="Do not check out additional packages", action='store_false')

	logger = getLogger(parser, sys.argv[0])
	args = parser.parse_args()

	if args.no_cmssw_setup:
		setupCMSSW(args)
	if args.no_packages_checkout:
		checkoutPackages(args)

#################################################################################################################
if __name__ == "__main__":
	main()
