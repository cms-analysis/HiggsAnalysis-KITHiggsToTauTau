#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import argparse
import os
import re
import shutil

import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gErrorIgnoreLevel = ROOT.kError

import HiggsAnalysis.KITHiggsToTauTau.treemerge as treemerge
import Artus.Utility.progressiterator as pi
import Artus.Utility.tools as tools
import Artus.Utility.jsonTools as jsonTools

import glob
import tempfile

# Example usage for multiple nicknames:
# for x in /nfs/dust/cms/user/tmuller/htautau/artus/2015-02-10_17-33_svfitComputation/output/*; do echo $x; svfitCacheTreeMerge.py -i $x/*.root --input-trees `artusPipelines.py $x/*.root | sed -e 's@\$@/svfitCache@g'` -o `echo "HiggsAnalysis/KITHiggsToTauTau/auxiliaries/svfit/svfitCache_${x}.root" | sed -e 's@/nfs/dust/cms/user/tmuller/htautau/artus/2015-02-10_17-33_svfitComputation/output/@@g'`; done
def _call_command(command):
	log.debug(command)
	logger.subprocessCall(command.split())

def nick_from_dir(directory):
	directory = directory.rstrip("/")
	return directory[directory.rfind("/")+1:]

def main():
	parser = argparse.ArgumentParser(description="Collect matching trees from input files into one output tree",
	                                 parents=[logger.loggingParser])

	parser.add_argument("-i", "--input", nargs="+", help="Input ROOT files.")
	parser.add_argument("-o", "--output", default="svfitCache.root",
	                    help="Output ROOT file. [Default: %(default)s]")
	
	parser.add_argument("--input-trees", nargs="+", default=["svfitCache"],
	                    help="Paths of input SVfit cache trees. [Default: %(default)s]")
	parser.add_argument("--output-tree", default="svfitCache",
	                    help="Name of output SVfit cache tree. [Default: %(default)s]")
	parser.add_argument("--previous-cache", default="",
	                    help="Path to a previous cache which will be merged. [Default: %(default)s]")
	parser.add_argument("--use-pipelines", default=False, action="store_true",
	                    help="Write caches into one chache per pipeline[Default: %(default)s]")
	parser.add_argument("--dcache", type=bool, default=False,
	                    help="Read&Write from and to desy dcache[Default: %(default)s]")
	parser.add_argument("--no-run", default=False, action="store_true",
	                    help="Do not run but only print dict  [Default: %(default)s]")
	
	merge_commands = []
	copy_commands = []
	config_file = []
	args = parser.parse_args()
	logger.initLogger(args)
	if not args.dcache:
		input = args.input
		output = args.output
		input_trees = args.input_trees
		output_trees = args.output_tree
		if args.use_pipelines:
			config = jsonTools.JsonDict(input[0])
			pipelines = config.get("Pipelines", {}).keys()
			# extract names without the leading channel
			pipelines = ["_".join(pipeline.split("_")[1:]) for pipeline in pipelines]
			pipelines = list(set(pipelines))
			for pipeline in pipelines:
				if not os.path.exists(pipeline):
					os.makedirs(pipeline)
				merged_tree_name = treemerge.treemerge(
						input, [pipeline+"/"+input_tree for input_tree in input_trees],
						pipeline+"/"+output, output_trees,
						match_input_tree_names=True
				)
				log.info("SVfit cache trees collected in \"%s\"." % merged_tree_name)
		else:
			merged_tree_name = treemerge.treemerge(
					input, input_trees,
					output, output_trees,
					match_input_tree_names=True
			)
			log.info("SVfit cache trees collected in \"%s\"." % merged_tree_name)
	else:
		input_dirs = args.input
		ls_command = "gfal-ls %s" %(args.output)
		retCode = logger.subprocessCall(ls_command.split())
		if(retCode != 0):
			mkdir_command = "gfal-mkdir %s" %(args.output)
			print "Creating " + args.output
			logger.subprocessCall(mkdir_command.split())
		tmpdir = tempfile.mkdtemp(suffix='', prefix='tmp', dir="/tmp")
		untar_commands = ["tar xvf %s -C %s"%(file,tmpdir) for input_dir in input_dirs for file in glob.glob(input_dir + "/*.tar*")]
		if not args.no_run:
			for index in range(len(untar_commands)):
				tools.parallelize(_call_command, [untar_commands[index]], 1)
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
				copy_commands.append("gfal-copy -f file:///%s %s" % (tmp_filename, out_filename ))
			config_file.append('"%s" : "%s",' % (sample, "dcap://dcache-cms-dcap.desy.de/pnfs/" + args.output + "/svfitCache_" + sample + ".root"))
		if not args.no_run:
			for index in range(len(merge_commands)):
				tools.parallelize(_call_command, [merge_commands[index]], 1)
				tools.parallelize(_call_command, [copy_commands[index]], 1)
		shutil.rmtree(tmpdir)
		print "done. Artus SvfitCacheFile settings: "
		for entry in config_file: 
			print entry

if __name__ == "__main__":
	main()

