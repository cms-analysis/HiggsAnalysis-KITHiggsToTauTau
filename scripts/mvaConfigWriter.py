#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import argparse
import copy
import os
import re
import Artus.Utility.jsonTools as jsonTools
import sys
import glob
import itertools

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Collect and Combine Correlation Information",
									 parents=[logger.loggingParser])
	parser.add_argument("-i", "--input-dir", required=True,
						help="Input directory. Use directory of ooutput from correlation_SampleProducer.py")
	parser.add_argument("-o", "--output-file",
							default="settingsMVATEstMethods.json",
							help="Output file. [Default: %(default)s]")
	parser.add_argument("-e", "--exclude-log", nargs="+",
						default=[],
						help="exclude training log files from collection. [Default: %(default)s]")
	parser.add_argument("-c", "--combine-log", nargs="+",
						default=["*_TrainingLog.json"],
						help="include training log files into collectionm [Default: %(default)s]")
	args = parser.parse_args()
	logger.initLogger(args)

	log_file_list = []
	log_exclude_list = []
	map(log_file_list.__iadd__, map(glob.glob, [os.path.join(args.input_dir, l) for l in args.combine_log]))
	map(log_exclude_list.__iadd__, map(glob.glob, [os.path.join(args.input_dir, l) for l in args.exclude_log]))
	for ex_log in log_exclude_list:
		if ex_log in log_file_list:
			log_file_list.pop(log_file_list.index(ex_log))
	settings_info = {
    "MVATestMethodsInputQuantities" : [
        ],
    "MVATestMethodsMethods" : [

    ],
    "MVATestMethodsNames" : [

    ],
	"MVATestMethodsNFolds" : [

    ],
    "MVATestMethodsWeights" : [
	]
	}
	settings_info["property"] = [
    ]
	quantities_index = -1
	for log_file in log_file_list:
		c_log = jsonTools.JsonDict(log_file)
		quantities = c_log["variables"]
		weight_path = os.path.join(args.input_dir, "weights")
		n_fold = c_log["N-Fold"]
		training_name = c_log["training_name"]
		methods = c_log["methods"]

		if quantities not in settings_info["MVATestMethodsInputQuantities"]:
			quantities_index += 1
			settings_info["MVATestMethodsInputQuantities"].append("%i;"%quantities_index + quantities)


		settings_info["MVATestMethodsNames"].append(training_name)
		settings_info["MVATestMethodsNFolds"].append(n_fold)
		for method in methods:
			method = method.split(";")[0]
			settings_info["property"].append(training_name)
			if n_fold == 1:
				settings_info["MVATestMethodsMethods"].append("%i;%s"%(quantities_index, method))
				settings_info["MVATestMethodsWeights"].append(weight_path+"/T%i_%s_%s.weights.xml"%(1,method,training_name))
			else:
				for i in range(1,n_fold+1):
					settings_info["MVATestMethodsMethods"].append("%i;%s"%(quantities_index, method))
					settings_info["MVATestMethodsWeights"].append(weight_path+"/T%i_%s_%s.weights.xml"%(i,method,training_name))
					settings_info["property"].append("T%i%s"%(i, training_name))
	jsonTools.JsonDict(settings_info).save(os.path.join(args.input_dir, args.output_file), indent = 4)