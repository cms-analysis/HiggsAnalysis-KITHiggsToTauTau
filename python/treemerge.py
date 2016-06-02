
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import copy
import os
import re

import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(True)

import Artus.HarryPlotter.utility.roottools as roottools
import Artus.Utility.tfilecontextmanager as tfilecontextmanager


def treemerge(input_file_names, input_tree_names,
              output_file_name, output_tree_name,
              match_input_tree_names = False):

	input_tree = ROOT.TChain()
	for input_file_name in input_file_names:
		tmp_input_tree_names = []
		
		if match_input_tree_names:
			tree_names = None
			with tfilecontextmanager.TFileContextManager(input_file_name, "READ") as root_file:
				tree_names = [path for key, path in roottools.RootTools.walk_root_directory(root_file) if key.GetClassName().startswith("TTree")]
			for input_tree_name in input_tree_names:
				tmp_input_tree_names.extend([tree_name for tree_name in tree_names if re.search(input_tree_name, tree_name)])
			tmp_input_tree_names = list(set(tmp_input_tree_names))
		else:
			tmp_input_tree_names = copy.deepcopy(input_tree_names)
		
		for input_tree_name in tmp_input_tree_names:
			log.debug("Found \"{0}/{1}\" to be merged.".format(input_file_name, input_tree_name))
			input_tree.Add(os.path.join(input_file_name, input_tree_name))
	
	output_file = ROOT.TFile(output_file_name, "RECREATE")
	output_tree = input_tree.CloneTree()
	output_tree.SetName(output_tree_name)
	output_file.Write()
	output_file.Close()
	return os.path.join(output_file_name, output_tree_name)

