#!/usr/bin/env python

import Artus.Utility.jsonTools as jsonTools
import HiggsAnalysis.KITHiggsToTauTau.plotting.higgsplot as higgsplot


## This class is built to create .json files for the Harryplotter module


class single_file:
    def __init__(self, afile):
        self.file = afile
        self.folder = None 
        self.marker = None
        self.color = None
        self.stack = None
        self.legend_name = None
        self.legend_marker = None
        self.scale_factor = 1
        self.weight = "1"
        self.x_expressions = None

class single_plot:
    def __init__(self, name):
        self.name = name
        self.files = []
        self.quantities = None
        self.out_json = jsonTools.JsonDict({})
    def add_file(self,a_file):
        self.files.append(a_file)
    def fill_single_json(self):
        self.out_json["filename"] = self.name
        for akt_file in self.files:
            self.out_json.setdefault("files", []).append(akt_file.file)
            self.out_json.setdefault("folders", []).append(akt_file.folder)
            self.out_json.setdefault("markers", []).append(akt_file.marker)
            self.out_json.setdefault("colors", []).append(akt_file.color)
            self.out_json.setdefault("nicks", []).append(akt_file.legend_name)
            self.out_json.setdefault("legend_markers", []).append(akt_file.legend_marker)
            self.out_json.setdefault("scale_factors", []).append(akt_file.scale_factor)
            self.out_json.setdefault("weights", []).append(akt_file.weight)
            self.out_json.setdefault("x_expressions", []).append(akt_file.x_expressions)


if __name__ == "__main__":

	import sys
	import argparse

	parser = argparse.ArgumentParser(description="Make Htautau plots with central sample estimation.")
	parser.add_argument("-a", "--args", default="",help="Additional Arguments for HarryPlotter. [Default: %(default)s]")
	parser.add_argument("-var","--variable", default="nPU", help="Variable, which should be plotted. [Default: %(default)s]")
	parser.add_argument("-pipes", "--pipelines", default="Mu_NoIso;Mu_Full;genMatched", help="Pipelines chosen for plotting. Number of pipelines should correspond to the number of files. Pipelines are separated by a semicolon. [Default: %(default)s]")
	parser.add_argument("-files", "--files", default="3**/nfs/dust/cms/user/aakhmets/CMSSW_7_4_12_patch4/src/tast_skim_embedded_merged.root", help="Files chosen for plotting. Number of files should correspond to the number of pipelines. Different files are separated by semicolon. If a file should appear multiple times, then use the appropriate count factor in front of the path. E.g.: 2^filepath. [Default: %(default)s]")
	args = parser.parse_args()

	args.args += " --plot-modules PlotRootHtt"

	color_list = ["kGray+3","kRed+2","kOrange+7", "kBlue+2", "kGreen+3", "kViolet-1"]
	legend_name_list = args.pipelines.split(";")
	folder_list = (args.pipelines+"/ntuple").replace(";","/ntuple;").split(";")
	file_list = []
	different_files = args.files.split(";")
	for f in different_files:
		if f.find("**") > -1:
			same_files = f.split("**")
			try:
				same = int(same_files[0])
				for i in range(same):
					file_list.append(same_files[1])
			except:
				print "No count factor"
		else: file_list.append(f)
	if not len(file_list) == len(folder_list):
		print "Choose same number of files and pipelines!"
		sys.exit()
	plot = single_plot("test")

	for i in range(len(file_list)):
		one_file = single_file(file_list[i])
		one_file.folder = folder_list[i]
		one_file.marker = "LINE"
		one_file.color = color_list[i]
		one_file.stack = "first_stack"
		one_file.legend_name = legend_name_list[i]
		one_file.legend_marker = "LINE"
		one_file.scale_factor = 1
		one_file.weight = "1"
		one_file.x_expressions = args.variable

		plot.add_file(one_file)

	plot.fill_single_json()

	configs = []

	configs.append(plot.out_json)

	higgs_plotter = higgsplot.HiggsPlotter(list_of_config_dicts=configs, list_of_args_strings=[args.args])

