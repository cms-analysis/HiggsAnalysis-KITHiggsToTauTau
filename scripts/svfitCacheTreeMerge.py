#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import argparse
import os
import re
import shutil
import sys

import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gErrorIgnoreLevel = ROOT.kError

import HiggsAnalysis.KITHiggsToTauTau.treemerge as treemerge
import Artus.Utility.tools as tools
import Artus.Utility.jsonTools as jsonTools

import glob
import tempfile

def _call_command(command):
	log.debug(command)
	if logger.subprocessCall(command.split()) != 0:
		pass
		#log.critical("Could not execute command \""+command+"\"! Exit program!")
		#sys.exit(1)

def nick_from_dir(directory):
	directory = directory.rstrip("/")
	return directory[directory.rfind("/")+1:]

def srm(in_path):
	return "srm://dcache-se-cms.desy.de:8443/srm/managerv2?SFN=/%s"%(in_path)

def dcap(in_path):
	return "dcap://dcache-cms-dcap.desy.de%s" % (in_path)

def xrd(in_path):
	return "root://dcache-cms-xrootd.desy.de:1094/%s" % (in_path.replace("/pnfs/desy.de/cms/tier2", ""))

def main():
	parser = argparse.ArgumentParser(description="Collect matching trees from input files into one output tree",
	                                 parents=[logger.loggingParser])

	parser.add_argument("-i", "--input", help="Input directory with merged Artus outputs including Svit Cache files")
	parser.add_argument("-o", "--output", default="svfitCache.root",
	                    help="Output ROOT file. [Default: %(default)s]")
	
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
	
	merge_commands = []
	copy_commands = []
	config_file = []
	
	ls_command = "gfal-ls %s" %(srm(args.output))
	retCode = logger.subprocessCall(ls_command.split())
	if(retCode != 0):
		mkdir_command = "gfal-mkdir %s" %(srm(args.output))
		log.info("Creating " + srm(args.output))
		logger.subprocessCall(mkdir_command.split())
	tmpdir = tempfile.mkdtemp(suffix='', prefix='tmp', dir="/tmp") #dir=os.getcwd())
	
	if not args.dcache:
		if not args.no_run:
			for input in glob.glob(args.input + "/*/*.root"):
				output = tmpdir 
				input_trees = args.input_trees
				output_trees = args.output_tree
				config = jsonTools.JsonDict(input)
				pipelines = config.get("Pipelines", {}).keys()
				# extract names without the leading channel
				pipelines = ["_".join(pipeline.split("_")[1:]) for pipeline in pipelines]
				pipelines = list(set(pipelines))
				pipelines = [x for x in pipelines if x != '']
				merge_commands = []
				for pipeline in pipelines:
					out_filename = os.path.join(output, pipeline, "svfitCache_" + os.path.basename(input))
					if not os.path.exists(os.path.dirname(out_filename)):
						os.makedirs(os.path.dirname(out_filename))
					pipeline_input_trees = [pipeline+"/"+input_tree for input_tree in input_trees]
					merged_tree_name = treemerge.treemerge(
							[input],  pipeline_input_trees,
							out_filename, output_trees,
							match_input_tree_names=True
					)
					log.info("SVfit cache trees collected in \"%s\"." % merged_tree_name)
			
			if args.previous_cache: # check for all available files in previous_cache
				previous_caches = glob.glob(args.previous_cache + "*/*.root")
				previous_cachefiles = [ "/".join(cache.split("/")[-2:]) for cache in previous_caches ]
				for cachefile in previous_cachefiles:
					current = os.path.join(output, cachefile)
					previous = os.path.join(args.previous_cache, cachefile)
					if not os.path.exists(os.path.dirname(current)):
						os.makedirs(os.path.dirname(current))
					if os.path.exists(current):
						merge_commands.append("mv %s %s_tmp.root "%(current, current))
						merge_commands.append("hadd -f -f6 %s %s_tmp.root %s "%(current, current, previous))
						merge_commands.append("rm %s_tmp.root "%(current))
					else:
						merge_commands.append("hadd -f -f6 %s %s"%(current, previous))
				tools.parallelize(_call_command, merge_commands, args.n_processes, description="merging")
			
			# move to output-directory
			copy_command = "gfal-copy -r file:///%s %s" % (output, srm(args.output) )
			logger.subprocessCall(copy_command.split())
		
		# print c&p summary
		current_caches = glob.glob(args.output + "*/*.root")
		nicknames = list(set([ os.path.basename(cache).split(".")[0].replace("svfitCache_", "") for cache in current_caches ]))
		for nick in sorted(nicknames):
			config_file.append('\t\t\t"%s" : "%s",' % (nick, xrd(args.output) + "/svfitCache_" + nick + ".root"))
	
	else:
		input_dirs = glob.glob(args.input + "/*/*/*")
		untar_commands = ["tar xf %s -C %s"%(file,tmpdir) for input_dir in input_dirs for file in glob.glob(input_dir + "/*.tar*")]
		if not args.no_run:
			tools.parallelize(_call_command, untar_commands, args.n_processes, description="unpacking")
		regex=re.compile(".*/(.*)_job_[0-9]+_SvfitCache.._(.*?)[0-9]+.root")
		matches = [(regex.match(file).groups(),file) for file in glob.glob(tmpdir+"/*.root")]
		dirs = {}
		
		# go through matches and create nested dict {'sample' : {'Pipeline' : [files]}}
		for match in matches:
			if match[0][0] not in dirs:
				dirs[match[0][0]] = {}
			if match[0][1] not in dirs[match[0][0]]:
				dirs[match[0][0]][match[0][1]] = []
			dirs[match[0][0]][match[0][1]].append(match[1])
		
		for sample in dirs:
			for pipeline in dirs[sample]:
				# create folders as needed
				if not os.path.exists(tmpdir + "/" + pipeline):
					os.makedirs(tmpdir + "/" + pipeline)
				previous_cache_file = ""
				if args.previous_cache:
					if os.path.isfile(args.previous_cache + "/" + pipeline + "/svfitCache_" + sample + ".root"):
						previous_cache_file = args.previous_cache + "/" + pipeline + "/svfitCache_" + sample + ".root"
				tmp_filename = tmpdir + "/" + pipeline + "/svfitCache_" + sample + ".root"
				out_filename = args.output + "/" + pipeline + "/svfitCache_" + sample + ".root"
				merge_commands.append("hadd -f %s %s %s"%(tmp_filename, " ".join(dirs[sample][pipeline]), previous_cache_file))
				copy_commands.append("gfal-copy -f file:///%s %s" % (tmp_filename, srm(out_filename) ))
			config_file.append('"%s" : "%s",' % (sample, xrd(args.output) + "/svfitCache_" + sample + ".root"))
		
		if not args.no_run:
			tools.parallelize(_call_command, merge_commands, args.n_processes, description="merging")
			tools.parallelize(_call_command, copy_commands, args.n_processes, description="copying")
	
	shutil.rmtree(tmpdir)
	log.info("done. Artus SvfitCacheFile settings: ")
	
	for entry in config_file: 
		log.info(entry)

if __name__ == "__main__":
	main()

