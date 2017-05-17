#!/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import argparse
import datetime
from httplib import HTTPException
from multiprocessing import Process
import os
import re
import shutil
import shlex
import string

from CRABAPI.RawCommand import crabCommand
from CRABClient.ClientExceptions import ClientException
import CRABClient.UserUtilities
from CRABClient.UserUtilities import getUsernameFromSiteDB

import Artus.Utility.tools as tools


def submit(config):
	try:
		crabCommand("submit", config=config)
	except HTTPException as hte:
		log.error("Failed submitting task: %s" % (hte.headers))
	except ClientException as cle:
		log.error("Failed submitting task: %s" % (cle))

def read_file(filename):
	content = ""
	with open(filename) as input_file:
		content = input_file.read()
	return content

def submission(base_path):

	today = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
	max_n_files_per_task = 8000
	filename_replacements = {
		"srm://grid-srm.physik.rwth-aachen.de:8443/srm/managerv2?SFN=/pnfs/physik.rwth-aachen.de/cms/store/user/" : "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/"
	}
	
	# retrieve and prepare input files
	stdout_directories, stderr_directories = tools.subprocessCall(shlex.split("gfal-ls " + args.base_path))
	for sample in stdout_directories.decode().strip().split("\n"):
		stdout_files, stderr_files = tools.subprocessCall(shlex.split("gfal-ls " + os.path.join(args.base_path, sample)))
		filenames = [filename for filename in stdout_files.decode().strip().split("\n") if (("SvfitCache" in filename) and filename.endswith(".root"))]
		if len(filenames) > 0:
			filenames = [os.path.join(args.base_path, sample, filename) for filename in filenames]
			pipelines_filenames = {}
			for filename in filenames:
				for src, dst in filename_replacements.iteritems():
					filename = filename.replace(src, dst)
				pipeline = re.search("SvfitCache(?P<pipeline>.*)\d+.root", filename).groupdict()["pipeline"]
				pipelines_filenames.setdefault(pipeline, []).append(filename)
			
			for pipeline, filenames in pipelines_filenames.iteritems():
				filenames_chunks = [filenames[index:index+max_n_files_per_task] for index in xrange(0, len(filenames), max_n_files_per_task)]
				for index, filenames_chunk in enumerate(filenames_chunks):
					
					# create job scripts
					jobfile_name = str("svfit_%s_%s_%s_%d.sh" % (today, sample, pipeline, index))
					with open(jobfile_name, "w+") as jobfile:
						jobfile.write(read_file(os.path.expandvars("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/templates/crab_userjob_prefix.sh")))
						
						svfit_code = string.Template(read_file(os.path.expandvars("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/templates/crab_svfit.sh")))
						jobfile.write(svfit_code.safe_substitute(
								input_files = "\n".join("arr[%d,0]=%s" % (i+1, f) for i, f in enumerate(filenames_chunk)),
								cwd=os.getcwd()
						))
						
						jobfile.close()
					
					# crab configuration
					config = CRABClient.UserUtilities.config()
					config.General.workArea = os.path.abspath(os.path.expandvars("$ARTUS_WORK_BASE/../svfit_caches/%s/" % (today)))
					config.General.transferOutputs = True
					config.General.transferLogs = True
					config.General.requestName = ("%s_%s_%d" % (sample, pipeline, index))[:100]
					log.info("Job name: " + config.General.requestName)
					config.Data.outputPrimaryDataset = "Svfit"
					config.Data.splitting = "EventBased"
					config.Data.unitsPerJob = 1
					config.Data.totalUnits = len(filenames_chunk)
					config.Data.publication = False
					config.Data.outputDatasetTag = config.General.requestName
					config.Data.outLFNDirBase = "/store/user/%s/higgs-kit/Svfit/%s/"%(getUsernameFromSiteDB(), today)
					log.info("Output directory: " + config.Data.outLFNDirBase)
					config.Data.publication = False
		
					config.User.voGroup = "dcms"
		
					config.JobType.pluginName = "PrivateMC"
					config.JobType.psetName = os.environ["CMSSW_BASE"]+"/src/CombineHarvester/CombineTools/scripts/do_nothing_cfg.py"
					# config.JobType.inputFiles = ["Kappa/lib/libKappa.so", os.environ["CMSSW_BASE"]+"/bin/"+os.environ["SCRAM_ARCH"]+"/ComputeSvfit", jobfile_name]
					config.JobType.inputFiles = [os.path.expandvars("$CMSSW_BASE/bin/$SCRAM_ARCH/ComputeSvfit"), jobfile_name]
					config.JobType.allowUndistributedCMSSW = True
					config.JobType.scriptExe = jobfile_name
					config.JobType.outputFiles = ["SvfitCache.tar"]
		
					config.Site.storageSite = "T2_DE_DESY"
					# config.Site.blacklist = ["T3_US_PuertoRico", "T2_ES_CIEMAT", "T2_DE_RWTH", "T3_US_Colorado", "T2_BR_UERJ", "T2_ES_IFCA", "T2_RU_JINR", "T2_UA_KIPT", "T2_EE_Estonia", "T2_FR_GRIF_LLR", "T2_CH_CERN", "T2_FR_GRIF_LLR", "T3_IT_Bologna", "T2_US_Nebraska", "T2_US_Nebraska", "T3_TW_NTU_HEP", "T2_US_Caltech", "T3_US_Cornell", "T2_IT_Legnaro", "T2_HU_Budapest", "T2_IT_Pisa", "T2_US_Florida", "T2_IT_Bari", "T2_FR_GRIF_IRFU", "T2_IT_Rome", "T2_FR_GRIF_IRFU", "T2_CH_CSCS", "T3_TW_NCU"]
					p = Process(target=submit, args=(config,))
					p.start()
					p.join()
					
					os.remove(jobfile_name)


if __name__ == "__main__":

	parser = argparse.ArgumentParser(description="crab submission script for standalone Svfit calculation.",
	                                 parents=[logger.loggingParser])
	
	parser.add_argument("base_path",
	                    help="/pnfs/[path to storage element with SvfitCache input files]")
	
	args = parser.parse_args()
	logger.initLogger(args)
	
	submission(args.base_path)

