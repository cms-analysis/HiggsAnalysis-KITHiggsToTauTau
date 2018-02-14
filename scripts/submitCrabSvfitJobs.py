#!/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import argparse
import datetime
import glob
from httplib import HTTPException
from multiprocessing import Process
import os
import re
import shutil
import shlex
import string
import tempfile

from CRABAPI.RawCommand import crabCommand
from CRABClient.ClientExceptions import ClientException
import CRABClient.UserUtilities
from CRABClient.UserUtilities import getUsernameFromSiteDB

import Artus.Utility.tools as tools


def get_filenames(args):
	base_path, sample = args[0], args[1]

	filename_replacements = {
		"srm://grid-srm.physik.rwth-aachen.de:8443/srm/managerv2?SFN=/pnfs/physik.rwth-aachen.de/cms/store/user/" : "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/"
	}
	
	filenames_per_sample_per_pipeline = {}
	
	stdout, stderr = tools.subprocessCall(shlex.split("gfal-ls " + os.path.join(base_path, sample)))
	filenames = [filename for filename in stdout.decode().strip().split("\n") if (("SvfitCache" in filename) and filename.endswith(".root"))]
	if len(filenames) > 0:
		filenames = [os.path.join(base_path, sample, filename) for filename in filenames]
		for filename in filenames:
			for src, dst in filename_replacements.iteritems():
				filename = filename.replace(src, dst)
			pipeline = re.search("SvfitCache(?P<pipeline>.*)\d+.root", filename).groupdict()["pipeline"]
			filenames_per_sample_per_pipeline.setdefault(sample, {}).setdefault(pipeline, []).append(filename)
	
	return filenames_per_sample_per_pipeline

def build_configs(filenames_per_sample_per_pipeline, di_tau_mass_constraint, name):
	today = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
	max_n_files_per_task = 8000
	
	filenames = []
	for sample, filenames_per_pipeline in filenames_per_sample_per_pipeline.iteritems():
		for pipeline, tmp_filenames in filenames_per_pipeline.iteritems():
			filenames.extend(tmp_filenames)
	
	configs = []
	jobfiles = []
	filenames_chunks = [filenames[index:index+max_n_files_per_task] for index in xrange(0, len(filenames), max_n_files_per_task)]
	for index, filenames_chunk in enumerate(filenames_chunks):
		
		# create job scripts
		jobfiles.append(str("svfit_%s_%s_%d.sh" % (today, name, index)))
		with open(jobfiles[-1], "w+") as jobfile:
			jobfile.write(read_file(os.path.expandvars("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/templates/crab_userjob_prefix.sh")))
			
			svfit_code = string.Template(read_file(os.path.expandvars("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/templates/crab_svfit.sh")))
			jobfile.write(svfit_code.safe_substitute(
					input_files = "\n".join("arr[%d,0]=%s" % (i+1, f) for i, f in enumerate(filenames_chunk)),
					cwd=os.getcwd(),
					args="--massconstraint "+str(di_tau_mass_constraint)
			))
			
			jobfile.close()
		
		# crab configuration
		configs.append(CRABClient.UserUtilities.config())
		configs[-1].General.workArea = os.path.abspath(os.path.expandvars("$ARTUS_WORK_BASE/../svfit_caches/%s_%s/" % (today, name)))
		configs[-1].General.transferOutputs = True
		configs[-1].General.transferLogs = True
		configs[-1].General.requestName = ("svfit_%s_%s_%d" % (today, name, index))[:100]
		log.debug("Job name: " + configs[-1].General.requestName)
		configs[-1].Data.outputPrimaryDataset = "Svfit"
		configs[-1].Data.splitting = "EventBased"
		configs[-1].Data.unitsPerJob = 1
		configs[-1].Data.totalUnits = len(filenames_chunk)
		configs[-1].Data.publication = False
		configs[-1].Data.outputDatasetTag = configs[-1].General.requestName
		configs[-1].Data.outLFNDirBase = "/store/user/%s/higgs-kit/Svfit/%s_%s/"%(getUsernameFromSiteDB(), today, name)
		log.debug("Output directory: " + configs[-1].Data.outLFNDirBase)
		configs[-1].Data.publication = False
		configs[-1].User.voGroup = "dcms"
		configs[-1].JobType.pluginName = "PrivateMC"
		configs[-1].JobType.psetName = os.environ["CMSSW_BASE"]+"/src/CombineHarvester/CombineTools/scripts/do_nothing_cfg.py"
		configs[-1].JobType.inputFiles = [os.path.expandvars("$CMSSW_BASE/bin/$SCRAM_ARCH/ComputeSvfit"), jobfiles[-1]]
		configs[-1].JobType.allowUndistributedCMSSW = True
		configs[-1].JobType.scriptExe = jobfiles[-1]
		configs[-1].JobType.outputFiles = ["SvfitCache.tar"]
		configs[-1].Site.storageSite = "T2_DE_RWTH"
	
	return configs, jobfiles

def submit(args):
	config, jobfile = args[0], args[1]
	
	try:
		crabCommand("submit", config=config)
	except HTTPException as hte:
		log.error("Failed submitting task: %s" % (hte.headers))
	except ClientException as cle:
		log.error("Failed submitting task: %s" % (cle))
	
	os.remove(jobfile)

def read_file(filename):
	content = ""
	with open(filename) as input_file:
		content = input_file.read()
	return content

def submission(base_paths, di_tau_mass_constraint, name, n_processes=1):
	
	# retrieve and prepare input files
	filenames_per_sample_per_pipeline = {}
	for base_path in base_paths:
		stdout_directories, stderr_directories = tools.subprocessCall(shlex.split("gfal-ls " + base_path))
		tmp_filenames_per_sample_per_pipeline = tools.parallelize(
				get_filenames,
				[[base_path, sample] for sample in stdout_directories.decode().strip().split("\n")],
				n_processes=n_processes,
				description="Retrieving inputs"
		)
		for item in tmp_filenames_per_sample_per_pipeline:
			for sample, filenames_per_pipeline in item.iteritems():
				for pipeline, tmp_filenames in filenames_per_pipeline.iteritems():
					filenames_per_sample_per_pipeline.setdefault(sample, {}).setdefault("pipeline", []).extend(tmp_filenames)
	configs, jobfiles = build_configs(filenames_per_sample_per_pipeline, di_tau_mass_constraint, name)
	
	# submit tasks
	submit_args = []
	for config, jobfile in zip(configs, jobfiles):
		submit_args.append([config, jobfile])
	tools.parallelize(submit, submit_args, n_processes=1, description="Submitting crab tasks")


def clear_environment():
	candidates_to_keep = ["TauAnalysis", "Kappa", "Artus", "HiggsAnalysis", "CombineHarvester", "grid-control"]
	candidates_to_move = glob.glob(os.path.expandvars("$CMSSW_BASE/src/*"))
	objects_to_move = sorted([candidate for candidate in candidates_to_move if not any([keep in candidate for keep in candidates_to_keep])])
	
	tmp_path = tempfile.mkdtemp(prefix="submitCrabSvfitJobs_"+datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")+"_")
	for object_to_move in objects_to_move:
		if os.path.isdir(object_to_move):
			cwd = os.getcwd()
			os.chdir(object_to_move)
			logger.subprocessCall("scram b clean", shell=True)
			os.chdir(cwd)
		
		log.info("Temporarily move {src} to {dst} ...".format(src=object_to_move, dst=tmp_path))
		shutil.move(object_to_move, tmp_path)
	
	symlinks_map = {}
	libs = sorted(glob.glob(os.path.expandvars("$CMSSW_BASE/lib/$SCRAM_ARCH/*")))
	for lib in libs:
		if not os.path.exists(lib):
			symlinks_map[lib] = os.readlink(lib)
			log.info("Remove temporarily broken symlink {src} ...".format(src=lib))
			os.remove(lib)
	
	return tmp_path, symlinks_map


def restore_environment(tmp_path, symlinks_map):
	objects_to_move = sorted(glob.glob(os.path.join(tmp_path, "*")))
	for object_to_move in objects_to_move:
		log.info("Move {src} to {dst} ...".format(src=object_to_move, dst="$CMSSW_BASE/src/"))
		shutil.move(object_to_move, os.path.expandvars("$CMSSW_BASE/src/"))
	log.info("Remove {src} ...".format(src=tmp_path))
	os.rmdir(tmp_path) # only remove if empty (for safety reasons)
	
	for link_name, src in symlinks_map.iteritems():
		log.info("Recreate symlink {link_name} to {src} ...".format(link_name=link_name, src=src))
		os.symlink(src, link_name)


if __name__ == "__main__":

	parser = argparse.ArgumentParser(description="crab submission script for standalone Svfit calculation.",
	                                 parents=[logger.loggingParser])
	
	parser.add_argument("base_paths", nargs="+",
	                    help="/pnfs/[path(s) to storage element(s) with SvfitCache input files]")
	parser.add_argument("-m", "--di-tau-mass-constraint", type=float, default=-1.0,
	                    help="Di-tau mass constraint. Suggestions: -1.0 (no constraint), 91.1876 (Z), 125.0 (H). [Default: %(default)s]")
	parser.add_argument("--name", default="svfit_caches",
	                    help="Project name to be put in output path. [Default: %(default)s]")
	parser.add_argument("-n", "--n-processes", type=int, default=1,
	                    help="Number of (parallel) processes. [Default: %(default)s]")
	parser.add_argument("--smaller-input-sandbox", default=False, action="store_true",
	                    help="Clear CMSSW environment before submitting by moving non-needed packages to a temporary directory in order to ensure sufficiently small crab input sandbox. In each of these packages \"scram b clean\" is called. After submission, the environment is restored. It is recommended to compile the complete CMSSW environment after submission. [Default: %(default)s]")
	
	args = parser.parse_args()
	logger.initLogger(args)
	
	# to keep crab input sandbox tarball small
	if args.smaller_input_sandbox:
		tmp_path, symlinks_map = clear_environment()
	
	submission(args.base_paths, args.di_tau_mass_constraint, args.name, args.n_processes)
	
	if args.smaller_input_sandbox:
		restore_environment(tmp_path, symlinks_map)

