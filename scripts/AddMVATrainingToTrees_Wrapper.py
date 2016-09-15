# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import argparse
import glob
import os
import sys
import tempfile
import hashlib
import json
import subprocess
import re
from string import Template
from datetime import datetime

import Artus.Utility.tools as tools
import Artus.Utility.jsonTools as jsonTools

def setInputFilenames(filelist, filedict):
	for entry in filelist:
		if "*" in entry:
			setInputFilenames(glob.glob(entry), filedict)
		else:
			if os.path.isdir(entry):
				setInputFilenames(glob.glob(os.path.join(entry, "*")), filedict)
			elif entry.endswith(".root"):
				nick = os.path.basename(entry).replace(".root","")
				if "_job" in nick:
					nick = nick.split("_job")[0]
				filedict.setdefault(nick, []).append(entry + " = 1")
			else:
				log.warning("Found file in input search path that is not further considered: " + entry + "\n")
			
if __name__ == "__main__":
	parser = argparse.ArgumentParser(parents=[logger.loggingParser],
		                                       description="Wrapper for AddMVATrainingToTrees.py used on the batch system. Parents are liable for their children!")
	fileOptionsGroup = parser.add_argument_group("File options")
	fileOptionsGroup.add_argument("-i", "--input-files", nargs="+", required=False,
						help="Input root files or folders.")
	fileOptionsGroup.add_argument("-l", "--training-logs", nargs="+", default=[],
						help="Path to TrainingLog.json")
	fileOptionsGroup.add_argument("-w", "--work", default="$ARTUS_WORK_BASE",
						help="Work directory base. [Default: %(default)s]")
	
	configOptionsGroup = parser.add_argument_group("Config options")
	configOptionsGroup.add_argument("-c", "--channels", nargs="*",
						default=["tt", "mt", "et", "em", "mm", "ee"],
						help="Channels. [Default: %(default)s]")
	configOptionsGroup.add_argument("--calc-Training-BDT", default = False, action="store_true",
						help="Calculate BDT scores for the training set as well [Default: %(default)s]")
	configOptionsGroup.add_argument("--gc-config", default="$CMSSW_BASE/src/Artus/Configuration/data/grid-control_base_config.conf",
		                                help="Path to grid-control base config that is replace by the wrapper. [Default: %(default)s]")
	configOptionsGroup.add_argument("--gc-config-includes", nargs="+",
						help="Path to grid-control configs to include in the base config.")
	runningOptionsGroup = parser.add_argument_group("Running options")
	runningOptionsGroup.add_argument("--no-run", default=False, action="store_true",
						help="Exit before running Artus to only check the configs.")
	#runningOptionsGroup.add_argument("--ld-library-paths", nargs="+",
	#					help="Add paths to environment variable LD_LIBRARY_PATH.")
	runningOptionsGroup.add_argument("--files-per-job", type=int, default=1,
						help="Files per batch job. [Default: %(default)s]")
	runningOptionsGroup.add_argument("--wall-time", default="24:00:00",
						help="Wall time of batch jobs. [Default: %(default)s]")
	runningOptionsGroup.add_argument("--memory", type=int, default=3000,
						help="Memory (in MB) for batch jobs. [Default: %(default)s]")
	runningOptionsGroup.add_argument("--cmdargs", default="-cG -m 3",
						help="Command line arguments for go.py. [Default: %(default)s]")
	#runningOptionsGroup.add_argument("--log-to-se", default=False, action="store_true",
	#					help="Write logfile in batch mode directly to SE. Does not work with remote batch system")
	
	args = parser.parse_args()
	
	ProjectPath = os.path.expandvars(args.work)
	if not ProjectPath.startswith("/"):
		ProjectPath = os.path.join(os.getcwd(), ProjectPath)
	if not os.path.exists(ProjectPath):
		os.makedirs(ProjectPath)
	#write dbs file
	gridControlInputFiles = {}
	setInputFilenames(args.input_files, gridControlInputFiles)
	dbsFileContent = tools.write_dbsfile(gridControlInputFiles)
	dbsFileBasename = "datasets.dbs"
	dbsFileBasepath = os.path.join(ProjectPath, dbsFileBasename)
	with open(dbsFileBasepath, "w") as dbsFile:
		dbsFile.write(dbsFileContent)
		
	#read gc base config
	gcConfigFilePath = os.path.expandvars(args.gc_config)
	gcConfigFile = open(gcConfigFilePath,"r")
	gcConfigFileContent = gcConfigFile.readlines()
	gcConfigFile.close()
	
	tmpGcConfigFileBasename = "grid-control_config.conf"
	tmpGcConfigFileBasepath = os.path.join(ProjectPath, tmpGcConfigFileBasename)
	tmpGcConfigFile = open(tmpGcConfigFileBasepath,"w")
	
	sepathRaw = os.path.join(ProjectPath, "output")

	epilogArguments  = r"epilog arguments ="
	#epilogArguments += r" --log-level " + args.log_level
	#if args.log_to_se:
	#	epilogArguments += r" --log-files" + os.path.join(sepathRaw, "${DATASETNICK}", "${DATASETNICK}_job_${MY_JOBID}_log.log")
	#else:
	#	epilogArguments += r" --log-files log.log --log-stream stdout"
	#epilogArguments += " --nick $DATASETNICK"
	epilogArguments += " -i $FILE_NAMES"
	epilogArguments += " -c"
	for entry in args.channels:
		epilogArguments += " " + entry
	if args.calc_Training_BDT:
		epilogArguments += " --calc-Training-BDT"
	epilogArguments += " -l"
	for entry in args.training_logs:
		epilogArguments += " " + entry
	#if not self._args.ld_library_paths is None:
		#epilogArguments += ("--ld-library-paths %s" % " ".join(self._args.ld_library_paths))

	workdir = "workdir = " + os.path.join(ProjectPath)
	backend = open(os.path.expandvars("$CMSSW_BASE/src/Artus/Configuration/data/grid-control_backend_naf.conf"), 'r').read()
	replacingDict = dict(
			include = ("include = " + " ".join(args.gc_config_includes) if args.gc_config_includes else ""),
			epilogexecutable = "epilog executable = AddMVATrainingToTrees.py",
			sepath = "se path = " + sepathRaw,
			workdir = workdir,
			jobs = "",
			inputfiles = "input files = \n\t" + os.path.expandvars(os.path.join("$CMSSW_BASE/bin/$SCRAM_ARCH", "AddMVATrainingToTrees.py")),
			filesperjob = "files per job = " + str(args.files_per_job),
			areafiles = "",
			walltime = "wall time = " + args.wall_time,
			memory = "memory = " + str(args.memory),
			cmdargs = "cmdargs = " + args.cmdargs,
			dataset = "dataset = \n\t:ListProvider:" + dbsFileBasepath,
			epilogarguments = epilogArguments,
			
			seoutputfiles = "",#"se output files = " if args.log_to_se else "se output files = *.log",
			backend = backend,
			partitionlfnmodifier = "partition lfn modifier = "
	)
	for line in range(len(gcConfigFileContent)):
		gcConfigFileContent[line] = Template(gcConfigFileContent[line]).safe_substitute(replacingDict)
	for index, line in enumerate(gcConfigFileContent):
		gcConfigFileContent[index] = line.replace("$CMSSW_BASE", os.environ.get("CMSSW_BASE", ""))
		gcConfigFileContent[index] = line.replace("$X509_USER_PROXY", os.environ.get("X509_USER_PROXY", ""))

	# save it
	for line in gcConfigFileContent:
		tmpGcConfigFile.write(line)
	tmpGcConfigFile.close()

	exitCode = 0
	command = "go.py " + tmpGcConfigFileBasepath
	log.info("Execute \"%s\"." % command)
	if not args.no_run:
		#logger.initLogger()
		exitCode = subprocess.call(command.split())#logger.subprocessCall(command.split())

	log.info("Log files are written to directory \"%s\"" % sepathRaw)

	if exitCode != 0:
		log.error("Exit with code %s.\n\n" % exitCode)
