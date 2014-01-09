import os
import sys

# Collection of functions used by checkout scripts
# Todo: Write output to logger, e.g. 'git config --list'
# Todo if possible: get rid of manualy entering "cmsenv"


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
# setup git-based cmssw area. Fork the cmssw before starting with that according to the manual on the following page
# https://wiki.physik.uzh.ch/cms/computing:git:basics


def setupCMSSW(args):
	commands = [
	'git init',
	'git config --global user.name ' + args.github_username,
	'git config --global user.email ' + args.mail,
	'git config --global core.editor ' + args.editor,
	'export CVSROOT=":ext:' + args.cern_username + '@lxplus5.cern.ch:/afs/cern.ch/user/c/cvscmssw/public/CMSSW"',
	'git clone git@github.com:fwyzard/cms-git-tools.git',
	'export PATH=$PWD/cms-git-tools:$PATH',
	'scram p ' + str(args.cmssw_version),
	]

	execCommands(commands)
	return
