#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import argparse
import glob
import os
from string import Template

import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gErrorIgnoreLevel = ROOT.kError

import Artus.Utility.tools as tools
import Artus.Utility.progressiterator as pi


def _call_command(command):
	log.debug(command)
	logger.subprocessCall(command.split())


def main():
	
	parser = argparse.ArgumentParser(description="Computes Svfit values on local batch system via grid-control", parents=[logger.loggingParser])

	parser.add_argument("project_dir", help="Artus Project directory containing the files \"output/*/*.root\" to calculate Svfit values for")
	args = parser.parse_args()
	logger.initLogger(args)
	output_dirs = glob.glob(os.path.join(args.project_dir, "output/*"))
	nick_names_wo_shifts = [nick for nick in [output_dir[output_dir.rfind("/")+1:] for output_dir in output_dirs] if not ".tar.gz" in nick]
	shifts = ["jecUncUp_tauEsNom", "jecUncNom_tauEsNom", "jecUncDown_tauEsNom", "jecUncNom_tauEsUp", "jecUncNom_tauEsDown"]
	outputs_per_nick = {}
	for shift in shifts:
		outputs_per_nick.update({nick+"_"+shift : glob.glob(os.path.join(args.project_dir, "output", nick, "*" + shift + "*.root")) for nick in nick_names_wo_shifts})
	# drop potentially existing SvfitCaches from the filelist
	for nick, files in outputs_per_nick.iteritems():
		outputs_per_nick[nick] = [file for file in files if ("SvfitCache" in file)]
	outputs_per_nick = {nick : files for nick, files in outputs_per_nick.iteritems() if len(files) > 0}

	svfit_dir = os.path.join(args.project_dir, "SvfitCache")
	svfit_work_dir = os.path.join(args.project_dir, "SvfitCacheWorkDir")
	if not os.path.exists(svfit_work_dir):
		os.makedirs(svfit_work_dir)

	#import pprint
	#pprint.pprint(outputs_per_nick) 
	dbs_file_path = os.path.join(svfit_work_dir, "SvfitCache.dbs")
	dbs_file = open(dbs_file_path, "w")

	for nick_name, output_files in outputs_per_nick.iteritems():
		dbs_file.write("\n[" + nick_name + "]\n")
		dbs_file.write("nickname = " + nick_name+"\n")
		for output_file in output_files:
			dbs_file.write("file:///" + output_file + " = 1\n")
	dbs_file.close()

	gcConfigFilePath = os.path.expandvars("$CMSSW_BASE/src/Artus/Configuration/data/grid-control_base_config.conf")
	gcConfigFile = open(gcConfigFilePath,"r")
	tmpGcConfigFileBasename = "grid-control_base_config_.conf"
	tmpGcConfigFileBasepath = os.path.join(svfit_work_dir, tmpGcConfigFileBasename)
	tmpGcConfigFile = open(tmpGcConfigFileBasepath,"w")
	gcConfigFileContent = gcConfigFile.readlines()
	epilogArguments = ""
	epilogArguments += "-i $FILE_NAMES "
	epilogArguments += "-o SvFitCache.root "
##	epilogArguments += "-l " + os.path.expandvars("$CMSSW_BASE/src/Kappa/lib/libKappa.so")
		
	sepath = "se path = " + svfit_dir 
	workdir = "workdir = " + svfit_work_dir 
	backend = open(os.path.expandvars("$CMSSW_BASE/src/Artus/Configuration/data/grid-control_backend_" + "naf" + ".conf"), 'r').read()
	replacingDict = dict(
				include = (""),
				epilogexecutable = "epilog executable = $CMSSW_BASE/bin/" + os.path.join(os.path.expandvars("$SCRAM_ARCH"), os.path.basename("ComputeSvfit")),
				sepath = sepath,
				workdir = workdir,
				jobs = "",
				inputfiles = "",# "input files = \n\t" + self._configFilename,
				filesperjob = "files per job = 1",
				areafiles = "",
				walltime = "wall time = 23:00",
				memory = "memory = 4000",
				cmdargs = "cmdargs = -cG -m 3",
				dataset = "dataset = \n\t:ListProvider:" + dbs_file_path,
				epilogarguments = "epilog arguments = " + epilogArguments,
				seoutputfiles = "se output files = *.root",
				backend = backend
		)


	replaceLines(gcConfigFileContent, replacingDict)
	for index, line in enumerate(gcConfigFileContent):
		gcConfigFileContent[index] = line.replace("$CMSSW_BASE", os.environ.get("CMSSW_BASE", ""))

	# save it
	for line in gcConfigFileContent:
		tmpGcConfigFile.write(line)
	tmpGcConfigFile.close()

	exitCode = 0
	command = "go.py " + tmpGcConfigFileBasepath
	log.info("Execute \"%s\"." % command)
	exitCode = logger.subprocessCall(command.split())
		
	log.info("Output is written to directory \"%s\"" % tmpGcConfigFileBasepath)

def replaceLines(inputList, replacingDict):
	for line in range(len(inputList)):
		inputList[line] = Template(inputList[line]).safe_substitute(replacingDict)


if __name__ == "__main__":
	main()

