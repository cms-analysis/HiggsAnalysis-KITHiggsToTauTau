#!/usr/bin/env python
# -*- coding: utf-8 -*-

# checkout script for cmssw53x for skimming
# todo: implement logger
# todo: replace absoulte cms5 path by useful generic path
# todo: check if cmsenv works

import os
import sys
import argparse
import subprocess

sys.path.append("/portal/ekpcms5/home/friese/devel/analysis/CMSSW_6_1_1/src/KITHiggsToTauTau/python/")
from logger import getLogger
from checkoutScriptsHelper import *

#################################################################################################################


def checkoutPackages(args):
	cmsswsrc = args.skimming_cmssw_base + "/" + args.cmssw_version + '/src'
	commands = [
		# kappa patch needed
		'cd ' + cmsswsrc,

		# "cvs co -r V00-03-04 -d CMGTools/External UserCode/CMG/CMGTools/External", # patch needed
#!		"git cms-addpkg CommonTools/RecoAlgos", #V00-03-23
#!		"git cms-addpkg QuarkGluonTagger/EightTeV",#"cvs co -r v1-2-3 QuarkGluonTagger/EightTeV UserCode/tomc/QuarkGluonTagger/EightTeV",
#!		"git cms-addpkg UserCode/tomc/QuarkGluonTagger/EightTeV",

		# MuMu Twiki  #V03-03-12-02
		"git cms-addpkg RecoMET/METProducers",

		# PU Jet ID as used in TauTau and needed for MVA MET
		# https://twiki.cern.ch/twiki/bin/view/CMS/HiggsToTauTauWorkingSummer2013#MET_regression_MVA_residual_reco
		# https://twiki.cern.ch/twiki/bin/view/CMS/MVAMet
#!		"git cms-addpkg JetMETCorrections/METPUSubtraction", # METPU_5_3_X_v10
#!		"cd JetMETCorrections/METPUSubtraction/test/",
#!		"./setup.sh",
		'cd ' + cmsswsrc,

		# replace non working RecoTauTag from above by official version
		# https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuidePFTauID#CMSSW_5_3_12
		"rm -rf RecoTauTag",

		#HCP + new discriminants
		"git cms-addpkg RecoTauTag/RecoTau",  #V01-04-25
		"git cms-addpkg RecoTauTag/Configuration",  #V01-04-13
		"pwd",
		#PAT
		"git cms-addpkg DataFormats/PatCandidates",
		"git cms-addpkg PhysicsTools/PatAlgos",
		"git cms-addpkg FWCore/GuiBrowsers",

		#Electrons
		"git cms-addpkg EgammaAnalysis/ElectronTools",
		"cat EgammaAnalysis/ElectronTools/data/download.url | xargs wget -P EgammaAnalysis/ElectronTools/data/",

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
	parser.add_argument("--skimming_cmssw_base", help="Path to skimming CMSSW base. Default: " + sysInformation["pwd"], nargs='?', default=sysInformation["pwd"])
	parser.add_argument("--username", help="your name as in github. Default: " + sysInformation["username"], default=sysInformation["username"], nargs='?')
	parser.add_argument("--mail", help="your email. Default: " + sysInformation["email"], default=sysInformation["username"], nargs='?')
	parser.add_argument("--editor", help="your favorite editor (ex. emacs). Default: " + sysInformation["editor"], default=sysInformation["editor"], nargs='?')
	parser.add_argument("--cmssw_version", help="the CMSSW Version to checko out. Default: CMSSW_5_3_13_patch3", default="CMSSW_5_3_13_patch3", nargs='?')
	parser.add_argument("--no_cmssw_setup", help="setup CMSSW environement", action='store_false')

	logger = getLogger(parser, sys.argv[0])
	args = parser.parse_args()
	print args.no_cmssw_setup
	if args.no_cmssw_setup:
		setupCMSSW(args)
	checkoutPackages(args)

#################################################################################################################
if __name__ == "__main__":
	main()
