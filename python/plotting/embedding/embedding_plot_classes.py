#!/usr/bin/env python

import Artus.Utility.jsonTools as jsonTools
import ROOT as r


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
		marker = "HISTO",
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
		name = None,
		num_file = None,
		den_file = None,
		num_folder = None,
		den_folder = None,
		num_tree = None,
		den_tree = None,
		stack = None,
		label = None,
		marker = None,
		color = None,
		legend_marker = None,
		scale_factor= None):

		cloned_plotline = single_plotline(
			name = self.name  if name is None else name,
			num_file = self.num_file if num_file is None else num_file,
			den_file = self.den_file if den_file is None else den_file,
			num_folder = self.num_folder if num_folder  is None else num_folder,
			den_folder = self.den_folder if den_folder  is None else den_folder,
			num_tree = self.num_tree if num_tree  is None else num_tree,
			den_tree = self.den_tree if den_tree  is None else den_tree,
			stack = self.stack if stack  is None else stack,
			label = self.label if label  is None else label,
			marker = self.marker if marker  is None else marker,
			color = self.color if color  is None else color,
			legend_marker= self.legend_marker if legend_marker is None else legend_marker,
			scale_factor= self.scale_factor if scale_factor is None else scale_factor)
		return cloned_plotline



class single_plot:
	def __init__(self,
		     name = "test",
		     title = None,
		     x_bins = None,
		     y_bins = None,
		     x_ticks = None,
		     x_tick_labels = None,
		     x_expression = "nPU",
		     y_expression = None,
		     y_lims = None,
		     z_lims = None,
		     z_label = None,
		     x_label = None,
		     legend = None,
		     formats =["png","pdf"],
		     wwwfolder ="plots",
		     y_label = "Events",
		     y_log = False,
		     weight = "1",
		     normalized_to_nevents = False,
		     normalized_to_unity = False,
		     normalized_to_hist1 = False,
		     profiled = False,
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
		self.y_bins = y_bins
		self.x_ticks = x_ticks
		self.x_tick_labels = x_tick_labels
		self.x_label = x_expression if x_label is None else x_label
		self.x_expression = x_expression
		self.y_expression = y_expression
		self.y_lims = y_lims
		self.z_lims = z_lims
		self.z_label = z_label
		self.legend = legend
		self.formats = formats
		self.wwwfolder = wwwfolder
		self.y_label = y_label
		self.y_log = y_log
		self.weight = weight
		self.normalized_to_nevents = normalized_to_nevents
		self.normalized_to_unity = normalized_to_unity
		self.normalized_to_hist1 = normalized_to_hist1
		self.profiled = profiled
		self.stacked = stacked
		self.plot_type = plot_type
		self.subplot_denominator = subplot_denominator
		self.subplot_numerators = subplot_numerators
		self.y_subplot_label = y_subplot_label
		self.y_subplot_lims = y_subplot_lims

		self.plotlines = plotlines
		self.out_json = jsonTools.JsonDict({})
	def clone(self,
		     name = None,
		     title = None,
		     x_bins = None,
		     y_bins = None,
		     x_ticks = None,
		     x_tick_labels = None,
		     x_expression = None,
		     y_expression = None,
		     y_lims = None,
		     z_lims = None,
		     z_label = None,
		     x_label = None,
		     legend = None,
		     formats = None,
		     wwwfolder = None,
		     y_label = None,
		     y_log = None,
		     weight = None,
		     normalized_to_nevents = None,
		     normalized_to_unity = None,
		     normalized_to_hist1 = None,
		     profiled = None,
		     stacked = None,
		     plot_type = None,
		     subplot_denominator = None,
		     subplot_numerators = None,
		     y_subplot_label = None,
		     y_subplot_lims = None,
		     plotlines = None):
	  
		cloned_plot = single_plot(
		     name = self.name if name is None else name,
		     title = self.title if title is None else title,
		     x_bins = self.x_bins if x_bins is None else x_bins,
		     y_bins = self.y_bins if y_bins is None else y_bins,
		     x_ticks = self.x_ticks if x_ticks is None else x_ticks,
		     x_tick_labels = self.x_tick_labels if x_tick_labels is None else x_tick_labels,
		     x_expression = self.x_expression if x_expression is None else x_expression,
		     y_expression = self.y_expression if y_expression is None else y_expression,
		     y_lims = self.y_lims if y_lims is None else y_lims,
		     z_lims = self.z_lims if z_lims is None else z_lims,
		     z_label = self.z_label if z_label is None else z_label,
		     x_label = self.x_label if x_label is None else x_label,
		     legend = self.legend if legend is None else legend,
		     formats = self.formats if formats is None else formats,
		     wwwfolder = self.wwwfolder if wwwfolder is None else wwwfolder,
		     y_label = self.y_label if y_label is None else y_label,
		     y_log = self.y_log if y_log is None else y_log,
		     weight = self.weight if weight is None else weight,
		     normalized_to_nevents = self.normalized_to_nevents if normalized_to_nevents is None else normalized_to_nevents,
		     normalized_to_unity = self.normalized_to_unity if normalized_to_unity is None else normalized_to_unity,
		     normalized_to_hist1 = self.normalized_to_hist1 if normalized_to_hist1 is None else normalized_to_hist1,
		     profiled = self.profiled if profiled is None else profiled,
		     stacked = self.stacked if stacked is None else stacked,
		     plot_type = self.plot_type if plot_type is None else plot_type,
		     subplot_denominator = self.subplot_denominator if subplot_denominator is None else subplot_denominator,
		     subplot_numerators = self.subplot_numerators if subplot_numerators is None else subplot_numerators,
		     y_subplot_label = self.y_subplot_label if y_subplot_label is None else y_subplot_label,
		     y_subplot_lims = self.y_subplot_lims if y_subplot_lims is None else y_subplot_lims,
		     plotlines = self.plotlines if plotlines is None else plotlines
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
		
		self.out_json["fill_styles"] = 0
		self.out_json["extra_text"] = "Work in Progress"
		self.out_json["cms"] = True 
		if self.profiled: self.out_json["tree_draw_options"] = "prof"
		
		self.out_json["filename"] = self.name + "_" + self.x_expression
		self.out_json["title"] = self.title
		self.out_json["y_scientific"] = True
		self.out_json["x_bins"] = self.x_bins
		if not self.x_ticks is None: self.out_json["x_ticks"] = self.x_ticks
		if not self.x_tick_labels is None: self.out_json["x_tick_labels"] = self.x_tick_labels
		self.out_json.setdefault("x_expressions", []).append(self.x_expression)
		if not self.y_expression is None: self.out_json.setdefault("y_expressions", []).append(self.y_expression)
		if not self.y_lims is None: self.out_json["y_lims"] = self.y_lims
		if not self.y_bins is None: self.out_json["y_bins"] = self.y_bins
		if not self.z_lims is None: self.out_json["z_lims"] = self.z_lims
		if not self.z_label is None: self.out_json["z_label"] = self.z_label
		self.out_json["x_label"] = self.x_label
		if not self.legend is None: self.out_json["legend"] = self.legend
		self.out_json["formats"] = self.formats
		if self.wwwfolder != "": self.out_json["www"] = self.wwwfolder
		self.out_json["y_label"] = self.y_label
		self.out_json["y_log"] = self.y_log
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
				if self.normalized_to_unity == True: self.safe_append_modules(modulename="NormalizeToUnity", moduletype="analysis")
				if self.normalized_to_hist1 == True: self.safe_append_modules(modulename="NormalizeToFirstHisto", moduletype="analysis")
			else:
				print "No proper plot type defined. Choose 'efficiency' or 'absolute'."
				sys.exit()

		# making a subplot with ratios, when denominator and numerators are given, both for 'efficiency' and 'absolute' plot type
		if self.subplot_denominator != None and len(self.subplot_numerators) != 0:
			self.out_json["y_subplot_label"] = self.y_subplot_label
			self.safe_append_modules(modulename="Divide", moduletype="analysis")
			self.create_subplot()
