#!/usr/bin/env python
# -*- coding: utf-8 -*-

# checkout script for cmssw53x for skimming
# todo: implement logger
# todo: make cmsenv/scramv work

import os
import sys
from optparse import OptionParser

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

		#Electrons
		"git cms-addpkg EgammaAnalysis/ElectronTools",
		"cd " + cmsswsrc + "EgammaAnalysis/ElectronTools/data/",
		"cat download.url | xargs wget",
		'cd ' + cmsswsrc,

		# https://twiki.cern.ch/twiki/bin/view/CMS/GluonTag
		"git clone git@github.com:amarini/QuarkGluonTagger.git",
		"cd " + cmsswsrc + "QuarkGluonTagger",
		"git checkout v1-2-3",
		'cd ' + cmsswsrc,
		
		# PU Jet ID as used in TauTau and needed for MVA MET (does not work with git cms-cvs-history and does not compile with cvs co)
		# https://twiki.cern.ch/twiki/bin/view/CMS/SWGuideCMSDataAnalysisSchoolJetMetAnalysis#MET_Recipe
		# https://twiki.cern.ch/twiki/bin/view/CMS/MVAMet

		"git cms-addpkg PhysicsTools/PatAlgos",
		"git cms-merge-topic -u TaiSakuma:53X-met-131120-01",
		"git cms-merge-topic -u cms-analysis-tools:5_3_14-updateSelectorUtils",
		"git cms-merge-topic -u cms-analysis-tools:5_3_13_patch2-testNewTau",
		"git cms-merge-topic -u cms-met:53X-MVaNoPuMET-20131217-01",

		"git clone https://github.com/ajaykumar649/Jets_Short.git",
		"cp -r Jets_Short/* " + cmsswsrc,
		"rm -rf Jets_Short",

		#Check out Kappa
		"git clone https://ekptrac.physik.uni-karlsruhe.de/git/Kappa",
		#"scram b -j 4"
	]
	execCommands(commands)
	return
#################################################################################################################


def main():
	parser = OptionParser()
	sysInformation = getSysInformation()

	parser.add_option("--github_username", help="your name as in github. Default: " + sysInformation["github_username"], default=sysInformation["github_username"], nargs='?')
	parser.add_option("--mail", help="your email. Default: " + sysInformation["email"], default=sysInformation["email"], nargs='?')
	parser.add_option("--editor", help="your favorite editor (ex. emacs). Default: " + sysInformation["editor"], default=sysInformation["editor"], nargs='?')
	parser.add_option("--cmssw_version", help="the CMSSW Version to checko out. Default: CMSSW_5_3_13_patch3", default="CMSSW_5_3_13_patch3", nargs='?')

	logger = getLogger()
	#args = parser.parse_args()
	(options, args) = parser.parse_args()
	checkoutPackages(args)

#################################################################################################################
if __name__ == "__main__":
	main()
