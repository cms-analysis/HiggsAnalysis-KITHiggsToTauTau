#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import argparse
import os

import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gErrorIgnoreLevel = ROOT.kError

import HiggsAnalysis.KITHiggsToTauTau.treemerge as treemerge
import Artus.Utility.progressiterator as pi
import Artus.Utility.tools as tools

import glob

# Example usage for multiple nicknames:
# for x in /nfs/dust/cms/user/tmuller/htautau/artus/2015-02-10_17-33_svfitComputation/output/*; do echo $x; svfitCacheTreeMerge.py -i $x/*.root --input-trees `artusPipelines.py $x/*.root | sed -e 's@\$@/svfitCache@g'` -o `echo "HiggsAnalysis/KITHiggsToTauTau/auxiliaries/svfit/svfitCache_${x}.root" | sed -e 's@/nfs/dust/cms/user/tmuller/htautau/artus/2015-02-10_17-33_svfitComputation/output/@@g'`; done
def _call_command(command):
	log.debug(command)
	logger.subprocessCall(command.split())

def nick_from_dir(directory):
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
	parser.add_argument("--dcache", type=bool, default=False,
	                    help="Read&Write from and to desy dcache[Default: %(default)s]")
	
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

		merged_tree_name = treemerge.treemerge(
				input, input_trees,
				output, output_tree,
				match_input_tree_names=True
		)
		log.info("SVfit cache trees collected in \"%s\"." % merged_tree_name)
	else:
		input_dirs = args.input
		nick_names = {}
		for directory in input_dirs:
			nick_names[nick_from_dir(directory)] = directory
		for nick_name, input_dir in pi.ProgressIterator(nick_names.iteritems(),
		                                                   length=len(nick_names),
		                                                   description="Merging Svfit Caches"):
			tmp_filename = ("/tmp/" + nick_name+".root")
			out_filename = args.output + "/" + nick_name + ".root"
			in_files = " ".join(glob.glob(input_dir + "/*/*/*/*/*.root"))
			merge_commands.append("hadd -f %s %s" % (tmp_filename, in_files ))
			copy_commands.append("gfal-copy -f file:///%s %s" % (tmp_filename, out_filename ))
			config_file.append('"%s" : "%s",' % (nick_name, "dcap://dcache-cms-dcap.desy.de/pnfs/" + out_filename.split("pnfs")[1]))
		for index in range(len(merge_commands)):
			tools.parallelize(_call_command, [merge_commands[index]], 1)
			tools.parallelize(_call_command, [copy_commands[index]], 1)
		print "done. Artus SvfitCacheFile settings: "
		for entry in config_file: 
			print entry

if __name__ == "__main__":
	main()

