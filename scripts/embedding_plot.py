#!/usr/bin/env python

import Artus.Utility.jsonTools as jsonTools
import HiggsAnalysis.KITHiggsToTauTau.plotting.higgsplot as higgsplot


## This class is built to create .json files for the Harryplotter module

class single_plotobject:
	def __init__(self, plot_type = "efficiency", num_file = None, den_file = None, num_folder = None, den_folder = None, num_nick = None, den_nick = None, eff_nick = None, x_expression = "nPU", marker = "PE", color = "kBlack", legend_marker="L", scale_factor=1, weight="1"):

		# possible values: "efficiency" and "absolute"
		self.plot_type = plot_type

		# num_* used for both plot_types, den_* and eff_nick only for "efficiency"
		self.num_file = num_file
		self.den_file = den_file
		self.num_folder = num_folder
		self.den_folder = den_folder
		self.num_nick = num_nick
		self.den_nick = den_nick
		self.eff_nick = eff_nick

		self.x_expression = x_expression
		self.marker = marker
		self.color = color
		self.legend_marker = legend_marker
		self.scale_factor = scale_factor
		self.weight = weight

class single_plot:
	def __init__(self, name, title, legend=[0.25,0.15,0.55,0.45], normalized=False, wwwfolder="plots", formats=["png","pdf"]):
		self.name = name
		self.title = title
		self.legend = legend
		self.formats = formats
		self.normalized = normalized
		self.wwwfolder = wwwfolder
		self.plotobjects = []
		self.out_json = jsonTools.JsonDict({})
	def add_plotobject(self, plotobject):
		self.plotobjects.append(plotobject)
	def fill_single_json(self):

		self.out_json.setdefault("plot_modules", []).append("PlotRootHtt")

		self.out_json["filename"] = self.name
		self.out_json["legend"] = self.legend
		self.out_json["title"] = self.title
		self.out_json["formats"] = self.formats
		self.out_json["www"] = self.wwwfolder
		for akt_plotobject in self.plotobjects:

			self.out_json.setdefault("x_expressions", []).append(akt_plotobject.x_expression)
			self.out_json.setdefault("markers", []).append(akt_plotobject.marker)
			self.out_json.setdefault("colors", []).append(akt_plotobject.color)
			self.out_json.setdefault("legend_markers", []).append(akt_plotobject.legend_marker)
			self.out_json.setdefault("scale_factors", []).append(akt_plotobject.scale_factor)
			self.out_json.setdefault("weights", []).append(akt_plotobject.weight)

			if akt_plotobject.plot_type == "efficiency":

				self.out_json.setdefault("files", []).append(akt_plotobject.num_file)
				self.out_json.setdefault("folders", []).append(akt_plotobject.num_folder)
				self.out_json.setdefault("nicks", []).append(akt_plotobject.num_nick)

				self.out_json.setdefault("files", []).append(akt_plotobject.den_file)
				self.out_json.setdefault("folders", []).append(akt_plotobject.den_folder)
				self.out_json.setdefault("nicks", []).append(akt_plotobject.den_nick)

				try: self.out_json.get("analysis_modules").count("Efficiency")
				except: self.out_json.setdefault("analysis_modules", []).append("Efficiency")
				self.out_json.setdefault("efficiency_numerator_nicks", []).append(akt_plotobject.num_nick)
				self.out_json.setdefault("efficiency_denominator_nicks", []).append(akt_plotobject.den_nick)
				self.out_json.setdefault("efficiency_nicks", []).append(akt_plotobject.eff_nick)
				self.out_json.setdefault("nicks_whitelist", []).append(akt_plotobject.eff_nick)

				self.out_json["y_label"] = "efficiency"
				self.out_json["x_bins"] = "1 5 9 13 17 21 25 29 33 38 43 50 61"

			elif akt_plotobject.plot_type == "absolute":

				self.out_json.setdefault("files", []).append(akt_plotobject.num_file)
				self.out_json.setdefault("folders", []).append(akt_plotobject.num_folder)
				self.out_json.setdefault("nicks", []).append(akt_plotobject.num_nick)

				if self.normalized:
					try: self.out_json.get("analysis_modules").count("NormalizeToUnity")
					except: self.out_json.setdefault("analysis_modules", []).append("NormalizeToUnity")
					self.out_json["y_label"] = "normalized distribution"
				else:
					self.out_json["y_label"] = "number of events"

			else:
				print "No proper plot type of the object defined. Choose 'efficiency' or 'absolute'."
				sys.exit()

if __name__ == "__main__":

	import sys
	import argparse

	parser = argparse.ArgumentParser(description="Make Htautau plots with central sample estimation.")

	parser.add_argument("-a", "--args", default="",help="Additional Arguments for HarryPlotter. [Default: %(default)s]")
	parser.add_argument("-plt", "--plot-name", default="test", help="Name of the plot. [Default: %(default)s]")
	parser.add_argument("-plt-fld", "--plot-folder", default="plots", help="Name of the folder, where the plot is saved. [Default: %(default)s]")
	parser.add_argument("-plt-type", "--plot-type", default="efficiency", help="[Default: %(default)s]")
	parser.add_argument("-plt-t", "--plot-title", default="", help="[Default: %(default)s]")

	parser.add_argument("-var","--variable", default="nPU", help="Variable, which should be plotted. [Default: %(default)s]")
	parser.add_argument("-nfile", "--num-files", default="/nfs/dust/cms/user/swayand/embedd_save/muonembed/ar_muonembed_K2Skim_FullReco.root;/nfs/dust/cms/user/swayand/DATA_NMSSM/artus_prod/MC_ZMUMU/MC_ZMUMU_merged.root", help="[Default: %(default)s]")
	parser.add_argument("-nfold", "--num-folders", default="Mu_Full;muon_full", help="[Default: %(default)s]")
	parser.add_argument("-nnick", "--num-nicks", default="Mu_Full;muon_full", help="[Default: %(default)s]")

	parser.add_argument("-dfile", "--den-files", default="/nfs/dust/cms/user/swayand/embedd_save/muonembed/ar_muonembed_K2Skim_FullReco.root;/nfs/dust/cms/user/swayand/DATA_NMSSM/artus_prod/MC_ZMUMU/MC_ZMUMU_merged.root", help="[Default: %(default)s]")
	parser.add_argument("-dfold", "--den-folders", default="genMatched;gen_matched", help="[Default: %(default)s]")
	parser.add_argument("-dnick", "--den-nicks", default="genMatched;gen_matched", help="[Default: %(default)s]")

	parser.add_argument("-enick", "--eff-nicks", default="CMSSW_7_0_7;CMSSW_7_4_12p4", help="Efficiency names for efficiency plotting. Separated by a semicolon. [Default: %(default)s]")
	args = parser.parse_args()

	color_list = ["kGray+3","kRed+2","kOrange+7", "kBlue+2", "kGreen+3", "kViolet-1"]

	num_nick_list = args.num_nicks.split(";")
	num_folder_list = (args.num_folders+"/ntuple").replace(";","/ntuple;").split(";")
	num_file_list = args.num_files.split(";")

	den_nick_list = args.den_nicks.split(";")
	den_folder_list = (args.den_folders+"/ntuple").replace(";","/ntuple;").split(";")
	den_file_list = args.den_files.split(";")

	eff_nick_list = args.eff_nicks.split(";")

	plot = single_plot(name=args.plot_name, title=args.plot_title, wwwfolder=args.plot_folder)

	for i in range(len(num_nick_list)):
		one_plotobject = single_plotobject(plot_type = args.plot_type, x_expression = args.variable, color = color_list[i], num_file = num_file_list[i], num_folder = num_folder_list[i], num_nick = num_nick_list[i], den_file = den_file_list[i], den_folder = den_folder_list[i], den_nick = den_nick_list[i], eff_nick=eff_nick_list[i])
		plot.add_plotobject(one_plotobject)


	plot.fill_single_json()

	configs = []

	configs.append(plot.out_json)

	higgs_plotter = higgsplot.HiggsPlotter(list_of_config_dicts=configs, list_of_args_strings=[args.args])

