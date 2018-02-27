#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import argparse
import glob
import os
import re
import shlex
import tempfile

import Artus.Utility.tools as tools

filename_replacements = {
	"srm://grid-srm.physik.rwth-aachen.de:8443/srm/managerv2?SFN=/pnfs/physik.rwth-aachen.de/cms/store/user/" : "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/"
}

def _call_command(command):
	log.debug(command)
	if logger.subprocessCall(shlex.split(command)) != 0:
		pass
		#log.critical("Could not execute command \""+command+"\"! Exit program!")
		#sys.exit(1)

def _get_crab_outputs(args):
	crab_dir = args[0]
	jobids = args[1]
	stdout, stderr = tools.subprocessCall(shlex.split("crab getoutput --dump --jobids {jobids} -d {crab_dir}".format(crab_dir=crab_dir, jobids=jobids)))
	return re.findall("PFN:\s*(?P<path>.*)\s", stdout)

def _download_untar(args):
	tar_file = args[0]
	output_dir = args[1]
	downloaded_tar_file = os.path.join(tempfile.mkdtemp(), os.path.basename(tar_file))
	tools.subprocessCall(shlex.split("gfal-copy {tar_file} {downloaded_tar_file}".format(tar_file=tar_file, downloaded_tar_file=downloaded_tar_file)))
	tools.subprocessCall(shlex.split("tar -x -f {downloaded_tar_file} -C {output_dir} --overwrite".format(downloaded_tar_file=downloaded_tar_file, output_dir=output_dir)))
	tools.subprocessCall(shlex.split("rm -rf {temp_dir}".format(temp_dir=os.path.dirname(downloaded_tar_file))))

def main():
	parser = argparse.ArgumentParser(description="Collect matching trees from input files into one output tree",
	                                 parents=[logger.loggingParser])

	parser.add_argument("-i", "--input-dirs", help="Input directories = crab project directories containing the subdirectories with crab tasks", nargs="+")
	parser.add_argument("-o", "--output-dir", default=None,
	                    help="Local output directory. [Default: subdir \"results\" in first input directory]")
	parser.add_argument("-d", "--dcache-target", default=None,
	                    help="Directory on dCache (srm) where the files should be copied to. [Default: %(default)s]")
	
	parser.add_argument("--input-trees", nargs="+", default=["svfitCache"],
	                    help="Paths of input SVfit cache trees. [Default: %(default)s]")
	parser.add_argument("--output-tree", default="svfitCache",
	                    help="Name of output SVfit cache tree. [Default: %(default)s]")
	parser.add_argument("--previous-cache", default="",
	                    help="Path to a previous cache which will be merged. [Default: %(default)s]")
	parser.add_argument("--dcache", type=bool, default=False,
	                    help="Read&Write from and to desy dcache[Default: %(default)s]")
	parser.add_argument("--no-run", default=False, action="store_true",
	                    help="Do not run but only print dict  [Default: %(default)s]")
	parser.add_argument("-n", "--n-processes", type=int, default=1,
	                    help="Number of (parallel) processes. [Default: %(default)s]")
	
	args = parser.parse_args()
	logger.initLogger(args)
	
	if args.output_dir is None:
		args.output_dir = os.path.join(args.input_dirs[0], "results")
	
	# get paths to crab outputs
	max_n_jobs = 8000
	max_n_retrieve = 500
	get_crab_outputs_args = []
	for input_dir in args.input_dirs:
		for jobid_start in xrange(1, max_n_jobs, max_n_retrieve):
			jobid_end = jobid_start + max_n_retrieve - 1
			get_crab_outputs_args.append([input_dir, "{jobid_start}-{jobid_end}".format(jobid_start=jobid_start, jobid_end=jobid_end)])
	
	tar_files = tools.parallelize(_get_crab_outputs, get_crab_outputs_args, args.n_processes, description="crab getoutput --dump")
	tar_files = tools.flattenList(tar_files)
	
	# download and un-tar
	download_untar_args = [[tar_file, args.output_dir] for tar_file in tar_files]
	tools.parallelize(_download_untar, download_untar_args, args.n_processes, description="download and un-tar crab outputs")
	
	root_files = glob.glob(os.path.join(args.output_dir, "*.root"))
	# TODO: maybe add more root files from -i arguments, that did not need to be un-tared
	
	root_files_per_sample_nick = {}
	for root_file in root_files:
		basename = os.path.basename(root_file)
		sample_nick = basename[:basename.index("_job_")]
		root_files_per_sample_nick.setdefault(sample_nick, []).append(root_file)
	
	merged_output_dir = os.path.join(args.output_dir, "merged")
	if not os.path.exists(merged_output_dir):
		os.makedirs(merged_output_dir)
	hadd_commands = ["hadd.py "+(" ".join(tmp_root_files))+" -t "+os.path.join(merged_output_dir, sample_nick+".root")+" -a \" -f -v 0\"" for sample_nick, tmp_root_files in root_files_per_sample_nick.iteritems()]
	tools.parallelize(_call_command, hadd_commands, args.n_processes, description="merging")
	
	if args.dcache_target:
		dcache_copy_commands = ["gfal-copy -f -r "+merged_output_dir+" "+args.dcache_target]
		tools.parallelize(_call_command, dcache_copy_commands, args.n_processes, description="copying to dCache")
	
	rm_commands = ["rm "+root_file for root_file in root_files]
	if args.dcache_target:
		rm_commands.extend(["rm "+os.path.join(merged_output_dir, sample_nick+".root") for sample_nick in root_files_per_sample_nick.keys()])
	tools.parallelize(_call_command, rm_commands, args.n_processes, description="deleting temporary files")
	
	log.info("\nJSON configuration for Artus:\n")
	config_output_dir = args.dcache_target if args.dcache_target else merged_output_dir
	for src, dst in filename_replacements.iteritems():
		config_output_dir = config_output_dir.replace(src, dst)
	for sample_nick in sorted(root_files_per_sample_nick.keys()):
		log.info("\""+sample_nick+"\" : \""+os.path.join(config_output_dir, sample_nick+".root")+"\",")

if __name__ == "__main__":
	main()

