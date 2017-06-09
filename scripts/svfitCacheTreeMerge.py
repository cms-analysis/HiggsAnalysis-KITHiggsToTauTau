#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import argparse
import glob
import os
import shlex

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
	
	tar_files = []
	for input_dir in args.input_dirs:
		tar_files.extend(glob.glob(os.path.join(input_dir, "*/results/*.tar")))
		tar_files.extend(glob.glob(os.path.join(input_dir, "results/*.tar")))
		
	tar_commands = ["tar -x -f "+tar_file+" -C "+args.output_dir+" --overwrite" for tar_file in tar_files]
	tools.parallelize(_call_command, tar_commands, args.n_processes, description="un-tar crab outputs")
	
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

