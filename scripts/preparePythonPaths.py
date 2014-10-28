#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
# crate symlinks necessary for import statements in kitHiggsTauTauTauCheckoutPackages.py script
if os.environ["CMSSW_BASE"] == "":
	print "Environment variable $CMSSW_BASE not set. Try 'cmsenv' before using this script."
	os.exit(1)
if not os.path.exists(os.path.expandvars("$CMSSW_BASE/python/Artus")):
	os.makedirs(os.path.expandvars("$CMSSW_BASE/python/Artus"))
	initfile = open(os.path.expandvars("$CMSSW_BASE/python/Artus/__init__.py"),'w')
	initfile.write("__path__.append('" + os.path.expandvars("$CMSSW_RELEASE_BASE") + "/python/Artus')\n")
	initfile.close()
	os.symlink(os.path.expandvars("$CMSSW_BASE/src/Artus/KappaAnalysis/python/"), 
	           os.path.expandvars("$CMSSW_BASE/python/Artus/KappaAnalysis"))
	os.symlink(os.path.expandvars("../../src/Artus/Utility/python/"), 
	           os.path.expandvars("$CMSSW_BASE/python/Artus/Utility"))

	os.makedirs(os.path.expandvars("$CMSSW_BASE/python/HiggsAnalysis"))
	os.symlink(os.path.expandvars("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/python"), 
	           os.path.expandvars("$CMSSW_BASE/python/HiggsAnalysis/KITHiggsToTauTau"))
	initfile = open(os.path.expandvars("$CMSSW_BASE/python/HiggsAnalysis/__init__.py"), 'w')
	initfile.write("__path__.append('" + os.path.expandvars("$CMSSW_RELEASE_BASE") + "/python/Higgsanalysis')\n")
	initfile.close()
	open(os.path.expandvars("$CMSSW_BASE/python/__init__.py"), 'w').close()
	open(os.path.expandvars("$CMSSW_BASE/python/Artus/KappaAnalysis/__init__.py"), 'w').close()
	open(os.path.expandvars("$CMSSW_BASE/python/Artus/Utility/__init__.py"), 'w').close()
	open(os.path.expandvars("$CMSSW_BASE/python/HiggsAnalysis/KITHiggsToTauTau/__init__.py"), 'w').close()
	print "...Done!"
