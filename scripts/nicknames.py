#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import argparse
import os
import re


if __name__ == "__main__":

	parser = argparse.ArgumentParser(description="Check nicknames of all available samples.",
	                                 parents=[logger.loggingParser])

	parser.add_argument("--match-py", help="Python-type regular expression to be checked.")
	parser.add_argument("--match-sh", help="Bash expression with wildcards to be checked.")
	
	args = parser.parse_args()
	logger.initLogger(args)
	
	file_lists = os.listdir(os.path.join(os.path.expandvars("$CMSSW_BASE"),
	                                     "src/HiggsAnalysis/KITHiggsToTauTau/data/Samples"))
	file_lists = [file_list for file_list in file_lists if file_list.endswith("recent.txt") and "_sample_" in file_list]
	
	nick_names = [re.match("\S*_sample_(?P<nick>.*)_recent.txt", file_list).groupdict().get("nick") for file_list in file_lists]
	nick_names = list(set(nick_names))
	nick_names = sorted([nick_name for nick_name in nick_names if nick_name != None])
	
	if args.match_py == None and args.match_sh == None:
		print "Available nick names:\n\t%s" % "\n\t".join(nick_names)
	
	else:
		if args.match_py != None:
			nick_names_py = [nick_name for nick_name in nick_names if re.search(args.match_py, nick_name) != None]
			print "Matching nick names (python-type):\n\t%s" % "\n\t".join(nick_names_py)
		
		if args.match_sh != None:
			import fnmatch
			nick_names_sh = [nick_name for nick_name in nick_names if fnmatch.fnmatch(nick_name, args.match_sh)]
			print "Matching nick names (bash-type):\n\t%s" % "\n\t".join(nick_names_sh)

