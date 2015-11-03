#!/usr/bin/env python

import Artus.Utility.jsonTools as jsonTools
import HiggsAnalysis.KITHiggsToTauTau.plotting.higgsplot as higgsplot


## This class is built to create .json files for the Harryplotter module


class single_pipeline:
	def __init__(self, file, folder, nick):
		self.file = file
		self.folder = folder
		self.nick = nick

class single_efficiency:
	def __init__(self, effnum, effden, effnick):
		self.effnum = effnum
		self.effden = effden
		self.effnick = effnick

class single_base:
	def __init__(self, x_expression, marker="PE", color="kBlack", legend_marker="L", scale_factor=1, weight="1"):
		self.x_expression = x_expression
		self.marker = marker
		self.color = color
		self.legend_marker = legend_marker
		self.scale_factor = scale_factor
		self.weight = weight

class single_plot:
	def __init__(self, name):
		self.name = name
		self.pipelines = []
		self.efficiencies = []
		self.bases = []
		self.quantities = None
		self.out_json = jsonTools.JsonDict({})
	def add_pipeline(self,pipeline):
		self.pipelines.append(pipeline)
	def add_efficiency(self,efficiency):
		self.efficiencies.append(efficiency)
	def add_base(self, base):
		self.bases.append(base)
	def fill_single_json(self):
		self.out_json["filename"] = self.name
		for akt_pipeline in self.pipelines:
			self.out_json.setdefault("files", []).append(akt_pipeline.file)
			self.out_json.setdefault("folders", []).append(akt_pipeline.folder)
			self.out_json.setdefault("nicks", []).append(akt_pipeline.nick)
		for akt_base in self.bases:
			self.out_json.setdefault("x_expressions", []).append(akt_base.x_expression)
			self.out_json.setdefault("markers", []).append(akt_base.marker)
			self.out_json.setdefault("colors", []).append(akt_base.color)
			self.out_json.setdefault("legend_markers", []).append(akt_base.legend_marker)
			self.out_json.setdefault("scale_factors", []).append(akt_base.scale_factor)
			self.out_json.setdefault("weights", []).append(akt_base.weight)
		if not len(self.efficiencies) == 0:
			for akt_eff in self.efficiencies:
				self.out_json.setdefault("efficiency_numerator_nicks",[]).append(akt_eff.effnum)
				self.out_json.setdefault("efficiency_denominator_nicks",[]).append(akt_eff.effden)
				self.out_json.setdefault("efficiency_nicks",[]).append(akt_eff.effnick)


if __name__ == "__main__":

	import sys
	import argparse

	parser = argparse.ArgumentParser(description="Make Htautau plots with central sample estimation.")

	parser.add_argument("-plt", "--plotname", default="test", help="Name of the plot. [Default: %(default)s]")
	parser.add_argument("-plt-fld", "--plotfolder", default="plots", help="Name of the folder, where the plot is saved. [Default: %(default)s]")

	parser.add_argument("-a", "--args", default="",help="Additional Arguments for HarryPlotter. [Default: %(default)s]")
	parser.add_argument("-var","--variable", default="nPU", help="Variable, which should be plotted. [Default: %(default)s]")
	parser.add_argument("-eff", "--efficiency", action="store_true", default=False, help="Decision, whether efficiencies or absolute values should be plotted. [Default: %(default)s]")

	parser.add_argument("-pipes", "--pipelines", default="Mu_Full;genMatched;muon_full;gen_matched", help="Pipelines chosen for plotting. Number of pipelines should correspond to the number of files. Separated by a semicolon. [Default: %(default)s]")
	parser.add_argument("-files", "--files", default="2**/nfs/dust/cms/user/swayand/embedd_save/muonembed/ar_muonembed_K2Skim_FullReco.root;2**/nfs/dust/cms/user/swayand/DATA_NMSSM/artus_prod/MC_ZMUMU/MC_ZMUMU_merged.root", help="Files chosen for plotting. Number of files should correspond to the number of pipelines. Different files are separated by semicolon. If a file should appear multiple times, then use the appropriate count factor in front of the path. E.g.: 2**filepath. [Default: %(default)s]")
	parser.add_argument("-lnames", "--legend-names", default="Mu_Full;genMatched;muon_full;gen_matched", help="Uniquely chosen names for the plotted categories, which consist of a file and a pipeline chosen. These could be in some cases the same, so they need to be distinguished by the names in the legend. Numer of names should correspond to the number of files. Separated by a semicolon. [Default: %(default)s]")

	parser.add_argument("-eff-num", "--efficiency-numerators", default="Mu_Full;muon_full", help="Numerators for efficiency plotting. Separated by a semicolon. The names used here must correspond to the ones used in 'legend_names'. [Default: %(default)s]")
	parser.add_argument("-eff-den", "--efficiency-denominators", default="genMatched;gen_matched", help="Denominators for efficiency plotting. Separated by a semicolon. The names used here must correspond to the ones used in 'legend_names' [Default: %(default)s]")
	parser.add_argument("-eff-nick", "--efficiency-nicknames", default="CMSSW_7_0_7;CMSSW_7_4_12p4", help="Efficiency names for efficiency plotting. Separated by a semicolon. [Default: %(default)s]")
	args = parser.parse_args()

	args.args += " --plot-modules PlotRootHtt --legend {POSITION} --www {PLOTFOLDER} -o {PLOTFOLDER} --y-label {YLABEL} --formats 'png' 'pdf' {MODULE} ".format(MODULE="--analysis-modules 'Efficiency'" if args.efficiency else "--y-log", POSITION="0.25 0.15 0.55 0.45", YLABEL="Efficiency" if args.efficiency else "Events", PLOTFOLDER=args.plotfolder)

	color_list = ["kGray+3","kRed+2","kOrange+7", "kBlue+2", "kGreen+3", "kViolet-1"]
	nick_list = args.legend_names.split(";")
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

	eff_num_list = args.efficiency_numerators.split(";")
	eff_den_list = args.efficiency_denominators.split(";")
	eff_nick_list = args.efficiency_nicknames.split(";")

	if not (len(eff_den_list) == len(eff_den_list) and len(eff_nick_list) == len(eff_den_list)):
		print "Choose same number of efficiency inputs!"
		sys.exit()

	plot = single_plot(args.plotname)


	for i in range(len(file_list)):
		one_pipeline = single_pipeline(file=file_list[i], folder=folder_list[i], nick=nick_list[i])
		plot.add_pipeline(one_pipeline)

	if args.efficiency:
		for i in range(len(eff_num_list)):
			one_efficiency = single_efficiency(effnum=eff_num_list[i], effden=eff_den_list[i],effnick=eff_nick_list[i])
			plot.add_efficiency(one_efficiency)
			one_base = single_base(x_expression=args.variable, color=color_list[i])
			plot.add_base(one_base)
			plot.out_json.setdefault("nicks_whitelist", eff_nick_list)
	else:
		for i in range(len(file_list)):
			one_base = single_base(x_expression=args.variable, color=color_list[i])
			plot.add_base(one_base)

	plot.fill_single_json()

	configs = []

	configs.append(plot.out_json)

	higgs_plotter = higgsplot.HiggsPlotter(list_of_config_dicts=configs, list_of_args_strings=[args.args])

