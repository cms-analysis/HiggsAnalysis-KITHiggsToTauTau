# -*- coding: utf-8 -*-

import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import GradientBoostingClassifier  
from sklearn.metrics import classification_report, roc_auc_score

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import argparse
import os

import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True


def tmva_classification(args_from_script=None):
	"""
	Perform scikit learn classification training.
	
	"""

	parser = argparse.ArgumentParser(description="Perform scikit learn classification training.",
	                                 fromfile_prefix_chars="@", conflict_handler="resolve",
	                                 parents=[logger.loggingParser])

	parser.add_argument("-s", "--signal", nargs="+", required=True, default=None,
	                    help="Signal file. Format same as for TChain.Add: path/to/file.root.")
	parser.add_argument("-b", "--background", nargs="+", required=True, default=None,
	                    help="Background file. Format same as for TChain.Add: path/to/file.root.")
	parser.add_argument("-f", "--folder", default=None, required=True,
	                    help="Tree in signal & background file. [Default: %(default)s]")
	parser.add_argument("-v", "--variables", nargs="+", required=True, default=None,
	                    help="Training variables. Multiple arguments for TMVA.Factory.AddVariable are split by semicolon.")
	parser.add_argument("--splitting", nargs="+", default="0.3 0.1 0.6",
	                    help="Set relative size of training, test and evaluation subsample. [Default: %(default)s]")
	parser.add_argument("-m", "--methods", nargs="+", required=True, default=None,
	                    help="MVA methods.")
	parser.add_argument("-o", "--output-file", default="sklearnClassification/output.root",
	                    help="Output file. [Default: %(default)s]")
	parser.add_argument("--optimize", default=False,
	                    help="Optimize the model for a fixed hyperparameter space. [Default: %(default)s]")

	args = parser.parse_args(args_from_script.split() if args_from_script != None else None)
	logger.initLogger(args)

	
	#training variables	
	list_of_variables = [variable for variable in args.variables.split(";")]

	#train,text,evaluation split
	splitting = args.splitting.split()
		
	from root_numpy import root2array, rec2array, array2root
	signal = root2array(args.signal,
			    args.folder,
			    list_of_variables)
	signal = rec2array(signal)

	backgr = root2array(args.background,
			    args.folder,
			    list_of_variables)
	backgr = rec2array(backgr)
	
	#sklearn needs 2D dataformat
	X = np.concatenate((signal, backgr))
	y = np.concatenate((np.ones(signal.shape[0]),
		            np.zeros(backgr.shape[0])))
	
	#sample splitting
	X_train, X_eval, y_train, y_eval = train_test_split(X, y, test_size=splitting[2], random_state=1)
	X_train, X_test, y_train, y_test = train_test_split(X_train, y_train, test_size=splitting[1], random_state=1)
    	
	#model and training
	bdt = GradientBoostingClassifier(args.methods)
	bdt.fit(X_train,y_train)


	#optimization of hyper parameter
	if args.optimize:

		from sklearn import grid_search


		# Perform grid search over all combinations
		# of these hyper-parameters
		param_grid = {"n_estimators": [50,200,400,1000],
			      "max_depth": [1, 3, 8],
			      'learning_rate': [0.1, 0.2, 1.]}

		clf = grid_search.GridSearchCV(gbt,
				               param_grid,
				               cv=3,
				               scoring='roc_auc',
				               n_jobs=8)
		_ = clf.fit(X_train, y_train)

		print "Best parameter set found on development set:"
		print
		print clf.best_estimator_	
	
	#testing
	y_predicted = bdt.predict(X_test)
	y_predicted.dtype = [('score', np.float64)]
	array2root(y_predicted, args.output, "BDTtest")

	log.debug(classification_report(y_test, y_predicted, target_names=["background", "signal"])
	log.debug("Area under ROC curve: %.4f"%(roc_auc_score(y_test, bdt.decision_function(X_test))))

	#Roc curve TODO!!!!
	"""
	plot_configs = []
		
	config_CutEff = {
    	"analysis_modules": [
		"CutEfficiency"
	],
	"markers": [
		"LP"
    	],
	"x_expressions": [
		"BDTscore"
    	], 
    	"x_label": "bkg_rej", 
    	"y_label": "sig_eff",
	"legend": [0.25, 0.25, 0.45, 0.45],
	"legend_cols": 1,
	"legend_markers": ["LP"],
	"weights": [
		"classID<0.5", 
		"classID>0.5"
    	]
	}
	
	plot_configs.append(config_CutEff)

	if log.isEnabledFor(logging.DEBUG):
		import pprint
		pprint.pprint(plot_configs)
	
	higgsplot.HiggsPlotter(list_of_config_dicts=plot_configs, list_of_args_strings=[args.args], n_processes=args.n_processes, n_plots=args.n_plots)
	"""

	#Evaluation
	from Artus.Utility.helpers.root.tree import TreeExtender

	with TreeExtender(args.output, BDTevaluation) as extender:
	    variables = list_of_variables
	    extender.addBranch("myDiscriminator/D", unpack=variables)

	    for entry in extender:
		values = [getattr(entry, v)[0] for v in variables]
		entry.myDiscriminator[0] = bdt.predict(X_eval, y_eval)




	
		

	
			
	

