
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import os

import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(True)


def treemerge(input_file_names, input_tree_names,
              output_file_name, output_tree_name):

	input_tree = ROOT.TChain()
	for input_file_name in input_file_names:
		for input_tree_name in input_tree_names:
			input_tree.Add(os.path.join(input_file_name, input_tree_name))
	
	output_file = ROOT.TFile(output_file_name, "RECREATE")
	output_tree = input_tree.CloneTree()
	output_tree.SetName(output_tree_name)
	output_file.Write()
	output_file.Close()
	return os.path.join(output_file_name, output_tree_name)

