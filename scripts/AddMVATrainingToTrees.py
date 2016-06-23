#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)
import sys
import os
import ROOT
import array
import Artus.Utility.jsonTools as jsonTools
ROOT.PyConfig.IgnoreCommandLineOptions = True

def append_MVAbranch(filenames, ntuple_strings, training_logs, branch_names="same as training"):
	#Setup of all the readers/methods etc. for value calculation
	ROOT.TMVA.Tools.Instance()
	tmva_handling_list = []
	all_variables = {}
	branch_count = 0
	for i, log in enumerate(training_logs):
		variables_list = [x.split(";")[0] for x in log["quantities"]]
		for var in variables_list:
			if not var in all_variables:
				all_variables[var] = array.array('f', [0])
		training_name = log["training_name"]
		if not isinstance(branch_names, str):
			training_name = branch_names[i]
		NFolds = int(log["N-Fold"])
		weight_file_path, weight_file_name = os.path.split(log["output_file"])
		temp_method = [m.split(";")[0] for m in log["methods"]]
		if len(temp_method) > 1:
			log.error("Only one MVA method per call, exception for NFold training!")
			sys.exit()
		branch_count += len(temp_method)
		weight_files = [ROOT.TString(os.path.join(weight_file_path, "T{number}_{method}_{name}.weights.xml".format(number=num, method=meth, name=weight_file_name))) for meth in temp_method for num in range(1,NFolds+1)]
		methods = []
		for method in temp_method:
			for temp in range(1,NFolds+1):
				methods.append(ROOT.TString(method+"_"+str(temp)+'_'+training_name))
		splits = [ROOT.TFormula("%s%i"%(method,temp), split.replace("TrainingSelectionValue", "x")) for split in log["splits"]]
		reader = ROOT.TMVA.Reader()
		for var_name in variables_list:
			reader.AddVariable(ROOT.TString(var_name), all_variables[var_name])
		for count, (method, weight_f) in enumerate(zip(methods, weight_files)):
			reader.BookMVA(method, weight_f)
		handling = {"variables":variables_list,
					"training_name": training_name,
					"NFolds": NFolds,
					"weight_files": weight_files,
					"splits":splits,
					"methods": methods,
					"reader": reader
					}
		tmva_handling_list.append(handling)

	new_branches = [array.array('f', [x]) for x in range(branch_count)]
	#looping over all files -> ntuples -> events -> branches to be added
	for filename in filenames:
		c_file = ROOT.TFile(filename, "update")
		for ntuple in ntuple_strings:
			ROOT.gDirectory.cd("/")
			if "/" in ntuple:
				ROOT.gDirectory.cd(ntuple.split("/")[0])
				tree = ROOT.gDirectory.Get(ntuple.split("/")[1])
			else:
				tree = ROOT.gDirectory.Get(ntuple)
			real_branches = []
			for key in all_variables:
				tree.SetBranchAddress(str(key), all_variables[key])
			for count, handl in enumerate(tmva_handling_list):
				real_branches.append(tree.Branch(str(handl['training_name']), new_branches[count], str(method)+"/F"))
			for event in tree:
				for counter, handl in enumerate(tmva_handling_list):
					temp_vars = array.array('f', [all_variables[var_name][0] for var_name in handl["variables"]])
					for (method, split) in zip(handl["methods"], handl["splits"]):
						#import pdb
						#pdb.set_trace()
						if split.Eval(event.__getattr__("TrainingSelectionValue")):
							new_branches[counter][0] = handl["reader"].EvaluateMVA(method)
							real_branches[counter].Fill()
							break
			tree.Write("", ROOT.TObject.kOverwrite)
		del c_file
if __name__ == "__main__":
	#import argparse
	#parser = argparse.ArgumentParser(description="Plot overlapping signal events.",
									 #parents=[logger.loggingParser])
	#parser.add_argument("-i", "--input-dir",
						#help="Path to ArtusOutput")
	#parser.add_argument("-m", "--higgs-masses",nargs="+", default = ["125"],
						#help="higgs mass [Default: %(default)s]")
	#parser.add_argument("-a", "--args", default="--plot-modules PlotRootHtt",
	                    #help="Additional Arguments for HarryPlotter. [Default: %(default)s]")
	#parser.add_argument("-f", "--first-category", nargs="+", default=[],
	                    #help="First Categories, can be specified multiple times. Several categories specified at once will be concatenated with or [Default: %(default)s]")
	#parser.add_argument("-s", "--second-category", nargs="+", default=[],
						#help="Second Categories, can be specified multiple times. Several categories specified at once will be concatenated with or[Default: %(default)s]")
	#parser.add_argument("-S", "--Samples", nargs="+", default=["ggh", "qqh"],
	                    #help="Samples to be compared [Default: %(default)s]")
	#parser.add_argument("-o", "--output-dir",
						#default="./",
						#help="path to output file. [Default: %(default)s]")

	filenames = ["TestTree.root"]
	ntuple_strings = ["mt_jecUncDown_tauEsNom/ntuple","mt_jecUncNom_tauEsDown/ntuple","mt_jecUncNom_tauEsNom/ntuple","mt_jecUncNom_tauEsUp/ntuple","mt_jecUncUp_tauEsNom/ntuple"]
	training_logs = [jsonTools.JsonDict("TrainingLog.json")]
	append_MVAbranch(filenames, ntuple_strings, training_logs)
