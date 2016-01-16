#!/usr/bin/env python

import Artus.Utility.jsonTools as jsonTools
import ROOT as r


## This class is built to create .json files for the Harryplotter module
_no_default = () ## dummy Sentinel object


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
		scale_factor=1):

		self.name = name
		# num_* used for both line_types, den_* and eff_nick only for "efficiency"
		self.num_file = num_file
		self.den_file = num_file if den_file == None else den_file
		self.num_folder = num_folder
		self.den_folder = num_folder if den_folder == None else den_folder
		self.num_tree = num_tree
		self.den_tree = num_tree if den_tree == None else den_tree

		self.stack = stack
		self.label = label
		self.marker = marker
		self.color = color
		self.legend_marker = legend_marker
		self.scale_factor = scale_factor

		# internally used nicknames
		self.nick = num_file.replace("/","_").replace(".root","") + "_" + num_folder + "_" + num_tree
		self.num_nick = "num" + self.nick
		self.den_nick = "den" + self.nick
		self.eff_nick = "eff" + self.nick
	def calculate_nevents_scalefactor(self):
		f = r.TFile(self.num_file, "READ")
		nevents= f.Get(self.num_folder).Get("ntuple").GetEntries()
		return 1./nevents

	def clone(self,
		name = _no_default,
		num_file = _no_default,
		den_file = _no_default,
		num_folder = _no_default,
		den_folder = _no_default,
		num_tree = _no_default,
		den_tree = _no_default,
		stack = _no_default,
		label = _no_default,
		marker = _no_default,
		color = _no_default,
		legend_marker = _no_default,
		scale_factor= _no_default):

		cloned_plotline = single_plotline(
			name = self.name  if name  == _no_default else name,
			num_file = self.num_file  if num_file  == _no_default else num_file,
			den_file = self.den_file  if den_file  == _no_default else den_file,
			num_folder = self.num_folder  if num_folder  == _no_default else num_folder,
			den_folder = self.den_folder  if den_folder  == _no_default else den_folder,
			num_tree = self.num_tree  if num_tree  == _no_default else num_tree,
			den_tree = self.den_tree  if den_tree  == _no_default else den_tree,
			stack = self.stack  if stack  == _no_default else stack,
			label = self.label  if label  == _no_default else label,
			marker = self.marker  if marker  == _no_default else marker,
			color = self.color  if color  == _no_default else color,
			legend_marker= self.legend_marker if legend_marker == _no_default else legend_marker,
			scale_factor= self.scale_factor if scale_factor == _no_default else scale_factor)
		return cloned_plotline



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
		     weight = "1",
		     normalized_to_nevents = False,
		     stacked = False,
		     plot_type = "efficiency",
		     subplot_denominator = None,
		     subplot_numerators = [],
		     y_subplot_label = "ratio",
		     y_subplot_lims =[0.5,2],
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
		self.weight = weight
		self.normalized_to_nevents = normalized_to_nevents
		self.stacked = stacked
		self.plot_type = plot_type
		self.subplot_denominator = subplot_denominator
		self.subplot_numerators = subplot_numerators
		self.y_subplot_label = y_subplot_label
		self.y_subplot_lims = y_subplot_lims

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
		     weight = _no_default,
		     normalized_to_nevents = _no_default,
		     stacked = _no_default,
		     plot_type = _no_default,
		     subplot_denominator = _no_default,
		     subplot_numerators = _no_default,
		     y_subplot_label = _no_default,
		     y_subplot_lims = _no_default,
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
		     weight = self.weight if weight == _no_default else weight,
		     normalized_to_nevents =  self.normalized_to_nevents if normalized_to_nevents == _no_default else normalized_to_nevents,
		     stacked = self.stacked if stacked == _no_default else stacked,
		     plot_type = self.plot_type if plot_type == _no_default else plot_type,
		     subplot_denominator = self.subplot_denominator if subplot_denominator == _no_default else subplot_denominator,
		     subplot_numerators = self.subplot_numerators if subplot_numerators == _no_default else subplot_numerators,
		     y_subplot_label = self.y_subplot_label if y_subplot_label == _no_default else y_subplot_label,
		     y_subplot_lims = self.y_subplot_lims if y_subplot_lims == _no_default else y_subplot_lims,
		     plotlines = self.plotlines if plotlines == _no_default else plotlines
		     )
		
		return cloned_plot

	def add_plotline(self, plotline):
		self.plotlines.append(plotline)
	def return_json_with_changed_x_and_weight(self, x_expressions=[], weights = []):
		ret_json_list = []
		if len(x_expressions) == len(weights):
			for i in range(len(x_expressions)):
				akt_plot = self.clone(x_expression=x_expressions[i], weight=weights[i])
				akt_plot.fill_single_json()
				ret_json_list.append(akt_plot.out_json)
		elif weights == []:
			for akt_x_expression in x_expressions:
				akt_plot = self.clone(x_expression=akt_x_expression)
				akt_plot.fill_single_json()
				ret_json_list.append(akt_plot.out_json)
		else:
			print "Choose for x_expressions and weights lists the same length or only x_expressions!"
			sys.exit()
		return ret_json_list
	#function to avoid errors, when no module of a certain type is appended yet. Appends a module only once.
	def safe_append_modules(self, modulename, moduletype):
		try:
			count = self.out_json.get(moduletype+"_modules").count(modulename)
			if count == 0:
				self.out_json.setdefault(moduletype+"_modules", []).append(modulename)
		except: self.out_json.setdefault(moduletype+"_modules", []).append(modulename)
	
	#function for creating a subplot
	def create_subplot(self):
		sub_den_nick = ""
		if self.plot_type == "efficiency": sub_den_nick = self.plotlines[self.subplot_denominator].eff_nick
		elif self.plot_type == "absolute": sub_den_nick = self.plotlines[self.subplot_denominator].num_nick
		else:
			print "No proper plot type defined. Choose 'efficiency' or 'absolute'."
			sys.exit()
		self.out_json.setdefault("divide_denominator_nicks",[]).append(sub_den_nick)
		for index in self.subplot_numerators:
			sub_num_nick = ""
			if self.plot_type == "efficiency": sub_num_nick = self.plotlines[index].eff_nick
			elif self.plot_type == "absolute": sub_num_nick = self.plotlines[index].num_nick
			else:
				print "No proper plot type defined. Choose 'efficiency' or 'absolute'."
				sys.exit()

			self.out_json["y_subplot_lims"] = self.y_subplot_lims

			self.out_json.setdefault("divide_numerator_nicks",[]).append(sub_num_nick)
			self.out_json.setdefault("divide_result_nicks",[]).append("div_"+sub_num_nick)
			self.out_json.setdefault("subplot_nicks",[]).append("div_"+sub_num_nick)

			self.out_json.setdefault("colors",[]).append(self.plotlines[index].color)
			self.out_json.setdefault("labels",[]).append(self.plotlines[index].label)
			self.out_json.setdefault("markers",[]).append(self.plotlines[index].marker)
			self.out_json.setdefault("legend_markers",[]).append(self.plotlines[index].legend_marker)

	def fill_single_json(self):
		self.out_json.setdefault("plot_modules", []).append("PlotRootHtt")

		self.out_json["filename"] = self.name + "_" + self.x_expression
		self.out_json["title"] = self.title
		self.out_json["y_scientific"] = True
		self.out_json["x_bins"] = self.x_bins
		self.out_json.setdefault("x_expressions", []).append(self.x_expression)
		self.out_json["x_label"] = self.x_label
		self.out_json["legend"] = self.legend
		self.out_json["formats"] = self.formats
		if self.wwwfolder != "": self.out_json["www"] = self.wwwfolder
		self.out_json["y_label"] = self.y_label
		self.out_json.setdefault("weights",[]).append(self.weight)

		# making the plot out of available files both for efficiency and absolute plot type 
		for akt_plotline in self.plotlines:

			if akt_plotline.num_file == None or akt_plotline.num_folder == None or akt_plotline.num_tree == None:
				print "Numerator is not properly set for line {LINE}. Need file, folder and tree".format(LINE=akt_plotline.name)
				sys.exit()

			self.out_json.setdefault("labels",[]).append(akt_plotline.label)
			self.out_json.setdefault("markers", []).append(akt_plotline.marker)
			self.out_json.setdefault("colors", []).append(akt_plotline.color)
			self.out_json.setdefault("legend_markers", []).append(akt_plotline.legend_marker)

			if self.stacked: self.out_json.setdefault("stacks",[]).append(akt_plotline.stack)

			if self.plot_type == "efficiency":
				if akt_plotline.den_file == None or akt_plotline.den_folder == None or akt_plotline.den_tree == None:
					print "Denominator is not properly set for line {LINE}. Need file, folder and tree".format(LINE=akt_plotline.name)
					sys.exit()

				self.out_json.setdefault("scale_factors", []).append(akt_plotline.scale_factor)
				self.out_json.setdefault("files", []).append(akt_plotline.num_file)
				ntree = "/" + akt_plotline.num_tree if not akt_plotline.num_tree == "" else ""
				self.out_json.setdefault("folders", []).append(akt_plotline.num_folder+ntree)
				self.out_json.setdefault("nicks", []).append(akt_plotline.num_nick)
				self.out_json.setdefault("nicks_blacklist",[]).append(akt_plotline.num_nick)

				self.out_json.setdefault("files", []).append(akt_plotline.den_file)
				dtree = "/" + akt_plotline.den_tree if not akt_plotline.den_tree == "" else ""
				self.out_json.setdefault("folders", []).append(akt_plotline.den_folder+dtree)
				self.out_json.setdefault("nicks", []).append(akt_plotline.den_nick)
				self.out_json.setdefault("nicks_blacklist",[]).append(akt_plotline.den_nick)

				self.safe_append_modules(modulename="Efficiency", moduletype="analysis")
				self.out_json.setdefault("efficiency_numerator_nicks", []).append(akt_plotline.num_nick)
				self.out_json.setdefault("efficiency_denominator_nicks", []).append(akt_plotline.den_nick)
				self.out_json.setdefault("efficiency_nicks", []).append(akt_plotline.eff_nick)

			elif self.plot_type == "absolute":
				if self.normalized_to_nevents == True: self.out_json.setdefault("scale_factors", []).append(akt_plotline.calculate_nevents_scalefactor())
				else: self.out_json.setdefault("scale_factors", []).append(akt_plotline.scale_factor)
				self.out_json.setdefault("files", []).append(akt_plotline.num_file)
				ntree = "/" + akt_plotline.num_tree if not akt_plotline.num_tree == "" else ""
				self.out_json.setdefault("folders", []).append(akt_plotline.num_folder+ntree)
				self.out_json.setdefault("nicks", []).append(akt_plotline.num_nick)
			else:
				print "No proper plot type defined. Choose 'efficiency' or 'absolute'."
				sys.exit()

		# making a subplot with ratios, when denominator and numerators are given, both for 'efficiency' and 'absolute' plot type
		if self.subplot_denominator != None and len(self.subplot_numerators) != 0:
			self.out_json["y_subplot_label"] = self.y_subplot_label
			self.safe_append_modules(modulename="Divide", moduletype="analysis")
			self.create_subplot()
