#!/usr/bin/env python
# -*- coding: utf-8 -*-

# checkout script for cmssw53x for skimming
# todo: implement logger
# todo: make cmsenv/scramv work

import os
import sys
from optparse import OptionParser

from HiggsAnalysis.KITHiggsToTauTau.checkoutScriptsHelper import *

#################################################################################################################


def checkoutPackages(args):
	cmsswsrc = os.popen("echo $CMSSW_BASE").readline().replace("\n", "") + '/src/'
	subdir = cmsswsrc + "AnalysisTools/Code/TauSpiner/"
	commands = [
	"git clone https://github.com/inugent/AnalysisTools",
	"cd " + subdir,
	"wget http://lcgapp.cern.ch/project/simu/HepMC/download/HepMC-2.06.05.tar.gz",
	"tar -xzvf HepMC-2.06.05.tar.gz",
	"mkdir hepmc",
	"cd " + subdir + "hepmc/",
	"mkdir build install",
	"cd " + subdir,
	"tar -xzvf lhapdf-5.8.6.tgz",
	"wget http://service-spi.web.cern.ch/service-spi/external/MCGenerators/distribution/pythia8/pythia8-176-src.tgz",
	"tar -xzvf pythia8-176-src.tgz",
	"wget http://service-spi.web.cern.ch/service-spi/external/MCGenerators/distribution/tauola++/tauola++-1.1.4-src.tgz",
	"tar -xzvf tauola++-1.1.4-src.tgz",
	"wget http://service-spi.web.cern.ch/service-spi/external/MCGenerators/distribution/pythia8/pythia8-176-src.tgz",
	"tar -xzvf pythia8-176-src.tgz",
	"touch ../make.inc",
	"sed -i 's/1.1.3/1.1.4/g' " + subdir + "Makefile.standalone",  # standalone makefile might still be for tauola++1.1.3
	"gmake -f Makefile.standalone"
	]
	execCommands(commands)
	return
#################################################################################################################


def main():
	print sys.argv[0]
	parser = OptionParser()
	sysInformation = getSysInformation()

	(options, args) = parser.parse_args()
	checkoutPackages(args)

#################################################################################################################
if __name__ == "__main__":
	main()
