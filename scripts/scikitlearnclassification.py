#!/usr/bin/env python
# -*- coding: utf-8 -*-


####################################################################################
# This script needs scikit-learn and root_numpy modules and requieres the	   #
# following versions: Python >=2.6 or >=3.3, Numpy >=1.6.1, Scipy >=0.9 and	   #
# ROOT >=5.32.                							   #
####################################################################################


import numpy as np

from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier  
from sklearn.metrics import classification_report, roc_auc_score

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import argparse
import os

import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True


def scikit_classification(args_from_script=None):
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
	                    help="Training variables.")
	parser.add_argument("--splitting", nargs="+", default="0.3 0.1 0.6",
	                    help="Set relative size of training, test and evaluation subsample (sum has to be 1). [Default: %(default)s]")
	parser.add_argument("-m", "--methods", nargs="+", required=True, default=None,
	                    help="MVA methods.")
	parser.add_argument("-o", "--output-file", default="sklearnClassification/output.root",
	                    help="Output file. [Default: %(default)s]")
	parser.add_argument("--optimize", default=False,
	                    help="Optimize the model for a fixed hyperparameter space. [Default: %(default)s]")

	args = parser.parse_args(args_from_script.split() if args_from_script != None else None)
	logger.initLogger(args)

	# create output file
	if not os.path.exists(os.path.dirname(args.output_file)):
		os.makedirs(os.path.dirname(args.output_file))
	output_file = ROOT.TFile(args.output_file, "RECREATE")

	
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
	bdt = AdaBoostClassifier(args.methods)
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
		clf.fit(X_train, y_train)

		print "Best parameter set found on development set:"
		print
		print clf.best_estimator_

	# finish
	output_file.Close()
	log.info("Training output is written to \"" + args.output_file + "\".")
	
	
	#testing
	y_predicted = bdt.predict(X_test)
	y_predicted.dtype = [('score', np.float64)]
	array2root(y_predicted, args.output, "BDTtest")

	print classification_report(y_test, y_predicted, target_names=["background", "signal"])
	print "Area under ROC curve: %.4f"%(roc_auc_score(y_test, bdt.decision_function(X_test)))

	#evaluation
	y_eval = bdt.predict(X_eval)
	y_eval.dtype = [('score', np.float64)]
	array2root(y_eval, args.output, "BDTeval")

if __name__ == "__main__" and len(sys.argv) > 1:
	scikit_classification()
		
		
