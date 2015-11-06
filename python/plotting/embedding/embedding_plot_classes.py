#!/usr/bin/env python

import Artus.Utility.jsonTools as jsonTools

## This class is built to create .json files for the Harryplotter module

class single_plotline:
	def __init__(self,
		name,
		num_file = None,
		den_file = None,
		num_folder = None,
		den_folder = None,
		num_tree = None,
		den_tree = None,
		stack = None,
		label = None,
		marker = "PE",
		color = "kBlack",
		legend_marker="L",
		scale_factor=1,
		weight="1"):

		self.name = name

		# num_* used for both line_types, den_* and eff_nick only for "efficiency"
		self.num_file = num_file
		self.den_file = num_file if den_file == None else den_file
		self.num_folder = num_folder
		self.den_folder = den_folder
		self.num_tree = num_tree
		self.den_tree = num_tree if den_tree == None else den_tree

		self.stack = stack
		self.label = label
		self.marker = marker
		self.color = color
		self.legend_marker = legend_marker
		self.scale_factor = scale_factor
		self.weight = weight

		# internally used nicknames
		self.nick = num_file.replace("/","_").replace(".root","") + "_" + num_folder + "_" + num_tree
		self.num_nick = "num_" + self.nick
		self.den_nick = "den_" + self.nick
		self.eff_nick = "eff_" + self.nick

_no_default = () ## dummy Sentinel object

class single_plot:
	def __init__(self,
		     name = "test",
		     title = None,
		     x_bins = None,
		     x_expression = "nPU",
		     x_label = _no_default,
		     legend =[0.25,0.15,0.55,0.45],
		     formats =["png","pdf"], 
		     wwwfolder ="plots",
		     y_label = "Events",
		     normalized = False, 
		     stacked = False,
		     plot_type = "efficiency",
		     plotlines = []):

		self.name = name
		self.title = title
		self.x_bins = x_bins
		self.x_label = x_expression if x_label == _no_default else x_label
		self.x_expression = x_expression
		self.legend = legend
		self.formats = formats
		self.wwwfolder = wwwfolder
		self.y_label = y_label

		self.normalized = normalized
		self.stacked = stacked
		self.plot_type = plot_type

		self.plotlines = plotlines
		self.out_json = jsonTools.JsonDict({})
	def clone(self,
		     name = _no_default,
		     title = _no_default,
		     x_bins = _no_default,
		     x_expression = _no_default,
		     x_label = _no_default,
		     legend = _no_default,
		     formats = _no_default, 
		     wwwfolder = _no_default,
		     y_label = _no_default,
		     normalized = _no_default, 
		     stacked = _no_default,
		     plot_type = _no_default,
		     plotlines = _no_default):
	  
		cloned_plot = single_plot(
		     name = self.name if name == _no_default else name,
		     title = self.title if title == _no_default else title,
		     x_bins = self.x_bins if x_bins == _no_default else x_bins,
		     x_expression = self.x_expression if x_expression == _no_default else x_expression,
		     x_label = self.x_label if x_label == _no_default else x_label,
		     legend = self.legend if legend == _no_default else legend,
		     formats =  self.formats if formats == _no_default else formats,
		     wwwfolder = self.wwwfolder if wwwfolder == _no_default else wwwfolder,
		     y_label = self.y_label if  y_label== _no_default else y_label,
		     normalized =  self.normalized if normalized == _no_default else normalized,
		     stacked = self.stacked if stacked == _no_default else stacked,
		     plot_type = self.plot_type if plot_type == _no_default else plot_type,
		     plotlines = self.plotlines if plotlines == _no_default else plotlines
		     )
		
		return cloned_plot

	def add_plotline(self, plotline):
		self.plotlines.append(plotline)
	def return_json_from_x_expressions(self, x_expressions=[]):
	    ret_json_list = []
	    for akt_x_expression in x_expressions:
	      akt_plot = self.clone(x_expression=akt_x_expression)
	      akt_plot.fill_single_json()
	      ret_json_list.append(akt_plot.out_json)
	    return ret_json_list

	def fill_single_json(self):

		self.out_json.setdefault("plot_modules", []).append("PlotRootHtt")

		self.out_json["filename"] = self.name + "_" + self.x_expression
		self.out_json["title"] = self.title
		self.out_json["x_bins"] = self.x_bins
		self.out_json.setdefault("x_expressions", []).append(self.x_expression)
		self.out_json["x_label"] = self.x_label
		self.out_json["legend"] = self.legend
		self.out_json["formats"] = self.formats
		self.out_json["www"] = self.wwwfolder
		self.out_json["y_label"] = self.y_label

		for akt_plotline in self.plotlines:

			if akt_plotline.num_file == None or akt_plotline.num_folder == None or akt_plotline.num_tree == None:
				print "Numerator is not properly set for line {LINE}. Need file, folder and tree".format(LINE=akt_plotline.name)
				sys.exit()

			self.out_json.setdefault("labels",[]).append(akt_plotline.label)
			self.out_json.setdefault("markers", []).append(akt_plotline.marker)
			self.out_json.setdefault("colors", []).append(akt_plotline.color)
			self.out_json.setdefault("legend_markers", []).append(akt_plotline.legend_marker)
			self.out_json.setdefault("scale_factors", []).append(akt_plotline.scale_factor)
			self.out_json.setdefault("weights", []).append(akt_plotline.weight)

			if self.stacked: self.out_json.setdefault("stacks",[]).append(akt_plotline.stack)

			if self.plot_type == "efficiency":
				if akt_plotline.den_file == None or akt_plotline.den_folder == None or akt_plotline.den_tree == None:
					print "Denominator is not properly set for line {LINE}. Need file, folder and tree".format(LINE=akt_plotline.name)
					sys.exit()

				self.out_json.setdefault("files", []).append(akt_plotline.num_file)
				self.out_json.setdefault("folders", []).append(akt_plotline.num_folder+"/"+akt_plotline.num_tree)
				self.out_json.setdefault("nicks", []).append(akt_plotline.num_nick)

				self.out_json.setdefault("files", []).append(akt_plotline.den_file)
				self.out_json.setdefault("folders", []).append(akt_plotline.den_folder+"/"+akt_plotline.den_tree)
				self.out_json.setdefault("nicks", []).append(akt_plotline.den_nick)

				try: self.out_json.get("analysis_modules").count("Efficiency")
				except: self.out_json.setdefault("analysis_modules", []).append("Efficiency")
				self.out_json.setdefault("efficiency_numerator_nicks", []).append(akt_plotline.num_nick)
				self.out_json.setdefault("efficiency_denominator_nicks", []).append(akt_plotline.den_nick)
				self.out_json.setdefault("efficiency_nicks", []).append(akt_plotline.eff_nick)
				self.out_json.setdefault("nicks_whitelist", []).append(akt_plotline.eff_nick)


			elif self.plot_type == "absolute":

				self.out_json.setdefault("files", []).append(akt_plotline.num_file)
				self.out_json.setdefault("folders", []).append(akt_plotline.num_folder+"/"+akt_plotline.num_tree)
				self.out_json.setdefault("nicks", []).append(akt_plotline.num_nick)

				if self.normalized:
					try: self.out_json.get("analysis_modules").count("NormalizeToUnity")
					except: self.out_json.setdefault("analysis_modules", []).append("NormalizeToUnity")

			else:
				print "No proper plot type defined. Choose 'efficiency' or 'absolute'."
				sys.exit()
