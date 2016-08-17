#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import Artus.Utility.logger as logger
import Artus.Utility.tools as aTools
log = logging.getLogger(__name__)
import sys
import os
import ROOT
import array
import Artus.Utility.jsonTools as jsonTools
ROOT.PyConfig.IgnoreCommandLineOptions = True

def append_MVAbranch(filenames, ntuple_strings, training_logs, branch_names="same as training", calcTrainBDT=False):
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
		splits = [ROOT.TFormula("%s%i"%(method,temp), split.replace("event", "x")) for split in log["splits"]]
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
		
		if calcTrainBDT:
			splits2 = [ROOT.TFormula("%s%i"%(method,temp), "1.0-" + split.replace("event", "x")) for split in log["splits"]]
			handling = {"variables":variables_list,
					"training_name": training_name + "_TrainingSet",
					"NFolds": NFolds,
					"weight_files": weight_files,
					"splits":splits2,
					"methods": methods,
					"reader": reader
					}
			tmva_handling_list.append(handling)	
	if calcTrainBDT:
		branch_count = 2*branch_count

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
						if split.Eval(event.__getattr__("event")):
							new_branches[counter][0] = handl["reader"].EvaluateMVA(method)
							real_branches[counter].Fill()
							break
			tree.Write("", ROOT.TObject.kOverwrite)
		del c_file

def file_wrapper(args):
	if args[2] in ["ee", "em", "mm"]:
		ntuple_strings = [args[2]+"_jecUncNom/ntuple"]#, args[2]+"_jecUncDown/ntuple", args[2]+"_jecUncUp/ntuple"]
	else:
		ntuple_strings = [args[2]+"_jecUncNom_tauEsNom/ntuple"]
		if not "Run20" in os.path.basename(args[0]):
			ntuple_strings.append(channel+"_jecUncDown_tauEsNom/ntuple")
			ntuple_strings.append(channel+"_jecUncUp_tauEsNom/ntuple")
		if "DY" in args[0] or "HToTauTau" in os.path.basename(args[0]):
			ntuple_strings.append(channel+"_jecUncNom_tauEsUp/ntuple")
			ntuple_strings.append(channel+"_jecUncNom_tauEsDown/ntuple")
	append_MVAbranch(filenames=[args[0]], ntuple_strings=ntuple_strings, training_logs=args[1], calcTrainBDT=args[3])


if __name__ == "__main__":
	import argparse
	import glob
	parser = argparse.ArgumentParser(description="Plot overlapping signal events.",
									 parents=[logger.loggingParser])
	parser.add_argument("-i", "--input-files", nargs="+", required=True,
						help="Path to ArtusOutput merged or rootfiles")
	parser.add_argument("-l", "--training-logs", nargs="+", default=[],
						help="Path to TrainingLog.json")
	parser.add_argument("-j", "--j", default = 1,
						help="number of parallel processes [Default: %(default)s]")
	parser.add_argument("-c", "--channels", nargs="*",
						default=["tt", "mt", "et", "em", "mm", "ee"],
						help="Channels. [Default: %(default)s]")
	parser.add_argument("--calc-Training-BDT", default = False, action="store_true",
						help="Calculate BDT scores for the training set as well [Default: %(default)s]")
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
	args = parser.parse_args()
	
	#clean argument input-files
	inputs = []
	for entry in args.input_files:
		inputs.append(entry.strip(',').strip('"'))
	if len(inputs)>1:
		filenames = inputs
	else:
		if os.path.isdir(inputs[0]):
			filenames = glob.glob(os.path.join(inputs[0], "*", "*.root"))
		else:
			filenames = inputs
	#ntuple_strings = ["mt_jecUncDown_tauEsNom/ntuple","mt_jecUncNom_tauEsDown/ntuple","mt_jecUncNom_tauEsNom/ntuple","mt_jecUncNom_tauEsUp/ntuple","mt_jecUncUp_tauEsNom/ntuple"]
	#training_logs = [jsonTools.JsonDict("TrainingLog.json")]
	training_logs = []
	for element in args.training_logs:
		training_logs.append(jsonTools.JsonDict(element))
	
	for channel in args.channels:
		args_list = []
		for element in filenames:
			args_list.append([element, training_logs, channel, args.calc_Training_BDT])
		aTools.parallelize(file_wrapper, args_list, args.j)