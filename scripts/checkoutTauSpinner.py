#!/usr/bin/env python
# -*- coding: utf-8 -*-

# checkout script for cmssw53x for skimming
# todo: implement logger
# todo: make cmsenv/scramv work

import os
import sys
from optparse import OptionParser

#################################################################################################################


def execCommands(commands):
	for command in commands:
		print ""
		print "command: " + command
		exitCode = 1
		nTrials = 0
		while exitCode != 0:
			if nTrials > 1:
				print "Last command could NOT be executed successfully! Stop program!"
				sys.exit(1)

				#logger.info("{CHECKOUT_COMMAND} (trial {N_TRIAL}):").formal(CHECKOUT_COMMAND = command, N_TRIAL = (nTrials+1))

			if command.startswith("cd"):
				os.chdir(os.path.expandvars(command.replace("cd ", "")))
				exitCode = int((os.path.expandvars(command.replace("cd ", "").strip("/")) != os.getcwd().strip("/")))
			else:
				exitCode = os.system(command)

			nTrials += 1

	return

#################################################################################################################


def getSysInformation():
	sysInformation = {
	"github_username": os.popen("git config user.name").readline().replace("\n", ""),
	"email": os.popen("git config user.email").readline().replace("\n", ""),
	"editor": os.popen("git config core.editor").readline().replace("\n", ""),
	"pwd": os.getcwd()
	}
	return sysInformation

#################################################################################################################


def checkoutPackages(args):
	cmsswsrc = os.popen("echo $CMSSW_BASE").readline().replace("\n", "") + '/src/'
	subdir = cmsswsrc + "AnalysisTools/Code/TauSpiner/"
	commands = [
	"git clone git://github.com/inugent/AnalysisTools",
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
	"wget http://service-spi.web.cern.ch/service-spi/external/MCGenerators/distribution/tauola++/tauola++-1.1.5-src.tgz",
	"tar -xzvf tauola++-1.1.5-src.tgz"
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
