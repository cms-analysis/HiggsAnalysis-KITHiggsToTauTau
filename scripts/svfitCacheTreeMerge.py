#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import argparse
import os

import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(True)

import HiggsAnalysis.KITHiggsToTauTau.treemerge as treemerge


# Example usage for multiple nicknames:
# for x in /nfs/dust/cms/user/tmuller/htautau/artus/2015-02-10_17-33_svfitComputation/output/*; do echo $x; svfitCacheTreeMerge.py -i $x/*.root --input-trees `artusPipelines.py $x/*.root | sed -e 's@\$@/svfitCache@g'` -o `echo "HiggsAnalysis/KITHiggsToTauTau/auxiliaries/svfit/svfitCache_${x}.root" | sed -e 's@/nfs/dust/cms/user/tmuller/htautau/artus/2015-02-10_17-33_svfitComputation/output/@@g'`; done

def main():
	parser = argparse.ArgumentParser(description="Collect matching trees from input files into one output tree",
	                                 parents=[logger.loggingParser])

	parser.add_argument("-i", "--input", nargs="+", help="Input ROOT files.")
	parser.add_argument("-o", "--output", default="svfitCache.root",
	                    help="Output ROOT file. [Default: %(default)s]")
	
	parser.add_argument("--input-trees", nargs="+",
	                    default=["svfitCache",
	                             "ee/svfitCache", "em/svfitCache", "et/svfitCache",
	                             "mm/svfitCache", "mt/svfitCache", "tt/svfitCache"],
	                    help="Paths of input SVfit cache trees. [Default: %(default)s]")
	parser.add_argument("--output-tree", default="svfitCache",
	                    help="Name of output SVfit cache tree. [Default: %(default)s]")
	
	args = parser.parse_args()
	logger.initLogger(args)
	
	merged_tree_name = treemerge.treemerge(args.input, args.input_trees,
	                                       args.output, args.output_tree)
	log.info("SVfit cache trees collected in \"%s\"." % merged_tree_name)


if __name__ == "__main__":
	main()

