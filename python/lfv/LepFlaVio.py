#! /usr/bin/env python

import argparse
import os
import sys

import HiggsAnalysis.KITHiggsToTauTau.plotting.higgsplot as higgsplot
import HiggsAnalysis.KITHiggsToTauTau.lfv.ConfigMaster as configmaster
import HiggsAnalysis.KITHiggsToTauTau.lfv.ParameterMaster as parametermaster

import ROOT
import pprint

###Enumeration class for analysis functions of flavio

class Analysismodule():
	control_plot = 0
	effiency_plot = 1
	shape_plot = 2
	cut_optimization = 3
	bkg_reduction_plot = 4
	nminus1_plot = 5
	cutflow_plot = 6
	limit_plot = 7

class Weights():
	zero_jet = 0
	one_jet = 1
	zero_jet_optimized = 2
	one_jet_optimized = 3

###Function for parser calls

def parser():
	
	parser = argparse.ArgumentParser(description = "Analysis and plotting beast (using harry.py the MVP) for LFV", formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument("-a", "--analysis", required = True,  action = "store", choices = range(8), type = int, help = "Your choice of specific analysis function. Use this key to get the your analysis function of desire: \n" 					"0: Make a controlplot \n" 
				"1: Make a cut effieciency plot\n"
				"2: Make a shape plot\n"
				"3: Do a cut optimization\n"
				"4: Make a plot showing ratio of samples before and after cut optimazation\n"
				"5: Make a N-1 plot using results of optimized cuts\n"	
				"6: Make a cutflow plot with optmized cuts\n"			
				"7: Do a limit plot\n")
	parser.add_argument("-x", "--x_expression", choices = range(14), required = True, nargs="+", type = int, help = "Choice your parameter of desire. Multiple parameter keys could be given at once. Use this key to get the your paramter(s):\n"
				"0:  Visible Mass\n" 
				"1:  Transverse momenta of sum of all lepton momenta\n"
				"2:  Transverse mass of lepton 1\n"
				"3:  Transverse mass of lepton 2\n"
				"4:  Number of jets\n"			
				"5:  Missing tranverse energy\n"
				"6:  Difference of angular angle between the two leptons minus pi\n"
				"7:  Difference of angular angle between the two leptons in center of mass frame minus pi\n"
				"8:  Difference of jet transverse momenta and dilepton transverse momenta\n"
				"9:  Some crazy parameter I even dont know about\n"
				"10: Impact parameter of first lepton\n"
				"11: Impact parameter of second lepton\n"
				"12: Sum of impact parameter\n"
				"13: Limit option which must be used with analysis argument 4\n")
	parser.add_argument("-w", "--weight-options", action = "store", choices = range(4), type = int, help = "Option for appyling weights on histograms working the analysismodule 0-2. Use this key to get your wished weights:\n"
				"0: Zero jet weight\n"
				"1: One jet weight\n"
				"2: Optimized weights for zero jet category\n"
				"3: Optimized weights for one jet category\n")
	parser.add_argument("-c", "--channel", action = "store", required = True, choices = ["em", "et", "mt"], type = str, help = "Your choice of final state which should be analysed")

	return parser.parse_args()


###Function that stores and return information for the configs that will be written

def base_config(channel, parameter, parameter_info, weights, nick_suffix = "", no_plot = False):

	weight_path = os.path.abspath(os.path.expandvars("$CMSSW_BASE/src/plots/FlavioOutput/CutOptimization")) + "/cutvalues_"
	weights_libary = {
				None:					["1", ""],													
				Weights.zero_jet:			["(njetspt30==0)", "_zerojets"],
				Weights.one_jet:			["(njetspt30==1)", "_onejet"],
				Weights.zero_jet_optimized:		[parameter_info.weightmaster(weight_path + channel + "_zerojet.ini") + "*" + "(njetspt30==0)", "_zerojet_optimized"],
				Weights.one_jet_optimized:		[parameter_info.weightmaster(weight_path + channel + "_onejet.ini") + "*" + "(njetspt30==1)", "_onejet_optimized"]
	}


	x,bins,output = parameter_info.get_parameter_info(parameter, 0)

	input_dir 		= 	["/net/scratch_cms3b/croote/artus/2017-11-09_14-46_SM-control/merged/"]
	output_dir		=	os.path.abspath(os.path.expandvars("$CMSSW_BASE/src/plots/FlavioOutput/"))
	output_file		= 	output + weights_libary[weights][1] if weights in weights_libary else output
	format 			= 	["pdf", "png"]
	www			= 	channel + "/"
	www_nodate		=	True
	nick_suffix		=	nick_suffix
	x_expressions		=	x
	x_bins	 		=	[bins]
	
	sample_list		= 	["z" + channel, "ztt", "zll", "ttj", "vv", "wj", "qcd"]
	channel 		= 	channel
	category		= 	None
	no_plot			=	no_plot
	weights			=	weights_libary[weights][0] if type(weights) == int or weights == None else weights
	estimationMethod	=	"new"
	cut_type		= 	"lfv"


	base_values = [input_dir, output_dir, output_file, format, www, www_nodate, x_expressions, x_bins]
	samples_values = [sample_list, channel, category, no_plot, nick_suffix, weights, estimationMethod, cut_type]

	return base_values, samples_values	

def controlplot_config(channel, parameter, parameter_info):
	x_label			=	parameter_info.get_parameter_info(parameter, 1)
	title 			=	"Controlplot " + "(" + channel + ")"
	legend			=	[0.65, 0.65, 1.00, 0.88]
	lumis 			= 	[35.87]
	energies		=	[13]
	year			=	"2016"
	www 			=	"Controlplot"
	
	return [x_label, title, legend, lumis, energies, year, www]


def sumofhists_config(sum_nicks, result_nicks):
	analysis_mod		=	["SumOfHistograms"]
	sum_nicks		=	sum_nicks
	result_nicks		=	result_nicks
	
	return [analysis_mod, sum_nicks, result_nicks]

	
def efficiency_config(channel, parameter, parameter_info, lower_cut = "True", plot_modules = ["PlotRoot"]):
	output_dir		= 	"/CutOptimization/"
	analysis_mod		=  	"CutEfficiency"
	bkg_nicks 		=	["bkg_sum"]	
	sig_nicks		=	["z" + channel + "noplot"]
	cut_modes		=	["sOverSqrtSB"]
	cut_nicks		= 	["sOverSqrtSB_" + str(parameter)]
	whitelist		= 	["sOverSqrtSB_" + str(parameter)]
	markers			=	["L"]
	y_label 		= 	"S/#sqrt{S+B}"
	lower_cut 		= 	lower_cut
	plot_modules		= 	plot_modules

	x_label			=	parameter_info.get_parameter_info(parameter, 1)
	title 			=	"Cut efficiency " + "(" + channel + ")"
	legend			=	None
	lumis 			= 	[35.87]
	energies		=	[13]
	year			=	"2016"
	www 			=	"CutEfficiency"

	return [x_label, title, legend, lumis, energies, year, www], [analysis_mod, bkg_nicks, sig_nicks, cut_modes, cut_nicks, whitelist, markers, y_label, lower_cut, plot_modules, output_dir]

def shape_config(channel, parameter, parameter_info):
	y_label			=	"arb. units"
	analysis_mod		= 	"NormalizeToUnity"

	x_label			=	parameter_info.get_parameter_info(parameter, 1)
	title 			=	"Shapeplot " + "(" + channel + ")"
	legend			=	[0.65, 0.65, 1.00, 0.88]
	lumis 			= 	[35.87]
	energies		=	[13]
	year			=	"2016"
	www 			=	"Shapeplot"
	
	return [x_label, title, legend, lumis, energies, year, www], [y_label, analysis_mod]

def bkg_reduction_config(channel, parameter, parameter_info):
	result_nicks		=	["z" + channel, "ztt", "zll", "ttj", "vv", "wj", "qcd"] 
	numerator_nicks		=	["{sample}_noplot_before_cuts".format(sample = sample) for sample in result_nicks] 
	denominator_nicks	=	["{sample}_noplot_after_cuts".format(sample = sample) for sample in result_nicks] 
	no_errors		= 	True
	analysis_modules	=	"Divide"
	markers			= 	["LINE" for nick in result_nicks]
	y_lims			=	[0, 1]
	colors			=	["k{color}".format(color=color) for color in ["Magenta", "Yellow", "Blue", "Violet", "Green", "Orange", "Pink"][:len(result_nicks)]]
	labels			= 	result_nicks
    	legend			= 	[0.15, 0.65, 0.60, 0.88] 
    	legend_markers		=	["L" for label in result_nicks]
	y_label			= 	"Ratio"

	x_label			=	parameter_info.get_parameter_info(parameter, 1)
	title 			=	"Ratioplot " + "(" + channel + ")"
	legend			=	[0.20, 0.70, 0.65, 0.88]
	lumis 			= 	[35.87]
	energies		=	[13]
	year			=	"2016"
	www			= 	"BackgroundReduction"	

	return [x_label, title, legend, lumis, energies, year, www], [numerator_nicks, denominator_nicks, result_nicks, no_errors, analysis_modules, y_lims, markers, colors, labels, legend, legend_markers, y_label]

def nminus1_config(channel, parameter, parameter_info):
	x_label			=	parameter_info.get_parameter_info(parameter, 1)
	title 			=	"N-1 Plot " + "(" + channel + ")"
	legend			=	[0.67, 0.70, 0.92, 0.88]
	lumis 			= 	[35.87]
	energies		=	[13]
	year			=	"2016"
	www 			= 	"N1minusPlot"

	return [x_label, title, legend, lumis, energies, year, www]

def ratio_config(numerator, denominator):
	ratio_numerator_nicks	=	numerator
	ratio_denominator_nicks =	denominator
	ratio_result_nicks 	=	["ratio"]
	analysis_modules	=	["Ratio"]
	markers			=	["LINE"]
	stacks			=	["ratio"]

	return [ratio_numerator_nicks, ratio_denominator_nicks, ratio_result_nicks, analysis_modules, markers, stacks]

def cutflow_config(channel, parameter, parameter_info):
	files 			=	"cutflow_" + channel + ".root"
	nicks 			=	["z" + channel, "ztt", "zll", "ttj", "vv", "wj", "qcd"]
	markers			= 	["HIST" for background in nicks]
	x_tick_labels	 	= 	[]
	stacks			=	["bkg" for background in nicks]

	x_label			=	""
	title			= 	"Cutflow "  + "(" + channel + ")"
	legend			=	[0.75, 0.60, 1, 0.83]
	lumis 			= 	[35.87]
	energies		=	[13]
	year			=	"2016"
	www 			= 	"Cutflow"

	return [x_label, title, legend, lumis, energies, year, www], [files, markers, nicks, x_tick_labels, stacks]


def limit_config(channel, parameter, parameter_info):
	y_label 		=	""
	files 			=	"limit_" + channel + ".root"
	folders 		= 	["limit"]
	y_expressions		= 	["category"]
	markers			= 	["E5", "E5", "P", "P"]
	colors 			= 	["kYellow", "kGreen", "kBlack", "kBlack"]
	fill_styles 		= 	[3001]
	marker_styles 		= 	[20, 20, 20, 21]
	line_widths 		= 	[40, 40, 1, 1]
	tree_draw_options 	= 	["TGraphAsymmErrorsX", "TGraphAsymmErrorsX", "TGraph", "TGraph"]
	y_tick_labels	 	= 	[]
	nicks 			=	["95% excepted", "68% excepted", "Excepted", "Observed"]
	y_lims 			= 	[-0.5]
	x_lims			=	[-0.2, 10]

	

	x_label			=	parameter_info.get_parameter_info(parameter, 1)[0]
	print x_label
	title			= 	"Limits "  + "(" + channel + ")"
	legend			=	[0.65, 0.65, 0.95, 0.88]
	lumis 			= 	[35.87]
	energies		=	[13]
	year			=	"2016"
	www 			= 	"Limitplots"

	return [x_label, title, legend, lumis, energies, year, www], [y_label, files, folders, y_expressions, markers, colors, fill_styles, marker_styles, line_widths, tree_draw_options, y_tick_labels, nicks, x_lims, y_lims]
	

###Analysis function using the specific plotting modules

def controlplot(config_list, channel, x, parameter_info, weights):
	for index, parameter in enumerate(x):
		config = configmaster.ConfigMaster(*base_config(channel, parameter, parameter_info, weights))
		config.add_config_info(controlplot_config(channel, parameter, parameter_info), 0)
		config_list.append(config.return_config())

		config_list[index]["weights"][0] += "*50"

	return config_list

def efficiencyplot(config_list, channel, x, parameter_info, weights):
	for parameter in x:
		config = configmaster.ConfigMaster(*base_config(channel, parameter, parameter_info, weights, nick_suffix = "noplot", no_plot = True))
		config.add_config_info(sumofhists_config(), 1)
		config.add_config_info(efficiency_config(channel, parameter, parameter_info)[0], 0)
		config.add_config_info(efficiency_config(channel, parameter, parameter_info)[1], 2)
		config_list.append(config.return_config())
	
	return config_list

def shapeplot(config_list, channel, x, parameter_info, weights):
	for index, parameter in enumerate(x):
		config = configmaster.ConfigMaster(*base_config(channel, parameter, parameter_info, weights))
		config.add_config_info(shape_config(channel, parameter, parameter_info)[0], 0)
		config.add_config_info(shape_config(channel, parameter, parameter_info)[1], 3)
		config.pop(["stacks", "colors"])
		config_list.append(config.return_config())

		##Delete information not needed
		config_list[index]["markers"] = ["LINE" for value in config_list[index]["markers"]]
	
	return config_list

def cutoptimization(config_list, channel, x, parameter_info, weights):

	##Define information for the cut config output
	cut_values = {}
	path = os.path.abspath(os.path.expandvars("$CMSSW_BASE/src/plots/FlavioOutput/CutOptimization/"))

	file_name = "cutvalues_" + channel + "_onejet2.ini"
	if os.path.exists(path + "/" + file_name):
		os.remove(path + "/" + file_name)

	for index in range(4):	
		for parameter in x:
			##For first itereration no cuts are used, then N-1 cuts are applied for the N th parameter you look at
			if(index != 0):
				cut_parameters = list(set(x).difference(set([parameter])))
				cut_strings = parameter_info.get_parameter_info(cut_parameters, 2)
				weight = parameter_info.weightaddition(cut_strings, [cut_values[str(cut)] for cut in cut_parameters])
		
			##Fill harry plotter config to get S/sqrt(S+B) histograms 
			config = configmaster.ConfigMaster(*base_config(channel, parameter, parameter_info, nick_suffix = "noplot", no_plot = True, weights = "1" if index==0 else weight))
			config.add_config_info(sumofhists_config(["zttnoplot zllnoplot ttjnoplot vvnoplot wjnoplot qcdnoplot"], ["bkg_sum"]), 1)
			config.add_config_info(efficiency_config(channel, parameter, parameter_info, plot_modules = ["ExportRoot"])[1], 2)
			config.pop(["www", "www_nodate"])
			config.change_config_info("filename", "_" + channel)

			##Call harry.py the MVP to get your job done
			harry = higgsplot.HiggsPlotter(list_of_config_dicts=[config.return_config()], n_plots = 1)

			##Read out produced histogramm for the N th parameter and find best cut value
			cut_file = ROOT.TFile.Open(os.path.abspath(os.path.expandvars("$CMSSW_BASE/src/plots/FlavioOutput/CutOptimization/")) + "/" +  parameter_info.get_parameter_info(parameter, 0)[-1] + "_" + channel + ".root")
			histogram = cut_file.Get("sOverSqrtSB_" + str(parameter))	
			cut_values[str(parameter)] = histogram.GetXaxis().GetBinCenter(histogram.GetMaximumBin())

			##Clear up output directory to only have ini files
			os.remove(path + "/" + config.return_config()["filename"] + ".root")
			os.remove(path + "/" + config.return_config()["filename"] + ".json")
			
		##Write cut values from Iteration into cut config
		parameter_info.cutconfigwriter(path, file_name, "Iteration" + str(index), cut_values)
	
	sys.exit()


def bkgreductionplot(config_list, channel, x, parameter_info, weights):

	##Weights without and with cut optimation, which are stored in base_config() 
	weight_before_cuts = weights
	weight_after_cuts = weights - 2

	##Return directly a config before cuts are applied which will be merged with config which is return to harry
	config_before_cuts = configmaster.ConfigMaster(*base_config(channel, x[0], parameter_info, weight_before_cuts, nick_suffix = "_noplot_before_cuts", no_plot = True)).return_config()

	##List with keys to merge to configs
	keys = ["files", "folders", "nicks", "nicks_correct_negative_bins", "nicks_empty_bins", "scale_factors", "weights", "qcd_shape_nicks", "qcd_shape_subtract_nicks", "qcd_yield_nicks",  "qcd_yield_subtract_nicks"]
	
	##Main config, starting with weights for the cuts and in which the before the cut config will be merged
	config = configmaster.ConfigMaster(*base_config(channel, x[0], parameter_info, weight_after_cuts,nick_suffix = "_noplot_after_cuts", no_plot = True))
	config.merge_by_keys(config_before_cuts, keys)
	config.add_config_info(bkg_reduction_config(channel, x[0], parameter_info)[0], 0)
	config.add_config_info(bkg_reduction_config(channel, x[0], parameter_info)[1], 5)
	
	config_list.append(config.return_config())

	return config_list
	

def nminus1plot(config_list, channel, x, parameter_info, weights):

	##Get information about cuts from ParameterMaster
	weight_path = os.path.abspath(os.path.expandvars("$CMSSW_BASE/src/plots/FlavioOutput/CutOptimization")) + "/cutvalues_" + channel + "_zerojet.ini" if weights == 0 else "_onejet.ini"
	cut_parameter, cut_values = parameter_info.cutconfigreader(weight_path, "Iteration3")
	cut_strings = parameter_info.get_parameter_info(cut_parameter, 2)

	if x[0] not in cut_parameter:	
		raise ValueError("This parameter was not optimized, you fool! Harry Plotter is a magician, but he is not almighty. Try harder or optimize this parameter.")

	for index, parameter in enumerate(cut_parameter):
		##Construct weight for N-1 plot
		strings = cut_strings[:index] + cut_strings[index+1 :]
		values = cut_values[:index] + cut_values[index+1 :]	
		weight = parameter_info.weightaddition(strings, values)	+ "*" + "(njetspt30==0)" if weights == 0 else "(njetspt30==1)"	

		#Build config
		config = configmaster.ConfigMaster(*base_config(channel, parameter, parameter_info, weight))
		config.add_config_info(nminus1_config(channel, parameter, parameter_info), 0)

		config_list.append(config.return_config())

	return config_list
		
def cutflowplot(config_list, channel, x, parameter_info, weights):
	##Directories you need as inputs
	weight_path = os.path.abspath(os.path.expandvars("$CMSSW_BASE/src/plots/FlavioOutput/CutOptimization")) + "/cutvalues_" + channel + "_zerojet.ini" if weights == 0 else os.path.abspath(os.path.expandvars("$CMSSW_BASE/src/plots/FlavioOutput/CutOptimization")) + "/cutvalues_" + channel + "_onejet.ini"
	output_directory = os.path.abspath(os.path.expandvars("$CMSSW_BASE/src/plots/FlavioOutput/Cutflow"))
	root_file = "/cutflow_" + channel + ".root"

	##List of processes
	processes = ["z" + channel, "ztt", "zll", "ttj", "vv", "wj", "qcd"]

	##Construct list of weights = [no cut, cut1, cut1+cut2, ..., cut1+...+cutN]
	cut_parameter, cut_values = parameter_info.cutconfigreader(weight_path, "Iteration3")
	cut_strings = parameter_info.get_parameter_info(cut_parameter, 2)
	weight_list = ["(njetspt30==0)" if weights == 0 else "(njetspt30==1)"] + [parameter_info.weightaddition(cut_strings[0:index+1], cut_values[0:index+1]) + "*" + "(njetspt30==0)" if weights == 0 else "(njetspt30==1)" for index in range(len(cut_parameter))]
	
	##Using harry.py the magician to get root files, read out for each process the total number of events and save them in hists as list for each weight
	hists = []
	for weight in weight_list:
		config = configmaster.ConfigMaster(*base_config(channel, x[0], parameter_info, weight))
		config.change_config_info("plot_modules", "ExportRoot")
		config.pop(["www", "www_nodate", "legend_markers"])
		
		higgsplot.HiggsPlotter(list_of_config_dicts=[config.return_config()], n_plots = 1)	

		root = ROOT.TFile.Open(os.path.abspath(os.path.expandvars("$CMSSW_BASE/src/plots/FlavioOutput/")) + "/VisibleMass.root")
		hists.append([root.Get(process).Integral() for process in processes])

	for filetype in ["root", "json"]:
		os.remove(os.path.abspath(os.path.expandvars("$CMSSW_BASE/src/plots/FlavioOutput/")) + "/VisibleMass." + filetype)

	##Use ROOT to fill hists in a new root file in which each process is a hist with the Number of events for each weight applied
	if not os.path.exists(output_directory):
		os.mkdir(output_directory)

	if os.path.isfile(output_directory + root_file):
		os.remove(output_directory + root_file)

	for index1, process in enumerate(processes):	
		output = ROOT.TFile(output_directory + root_file, "UPDATE")
		root_hist = ROOT.TH1F(process, process, len(hists), 0, len(hists))
		for index2, hist in enumerate(hists):
			root_hist.SetBinContent(index2+1, hist[index1])

		output.Write()
		output.Close()
	
	##Write config for limit plots
	config = configmaster.ConfigMaster(base_config(channel, x[0], parameter_info, "1", no_plot = True)[0])
	config.add_config_info(cutflow_config(channel, x, parameter_info)[0], 0)
	config.add_config_info(cutflow_config(channel, x, parameter_info)[1], 6)
	config.add_config_info(sumofhists_config(["ztt zll ttj vv wj qcd"], ["bkg_sum_noplot"]), 1)
	config.print_config()
	config.add_config_info(ratio_config(["z" + channel], ["bkg_sum_noplot"]), 7)
	config.pop(["directories", "x_expressions", "x_bins"])
	config.change_config_info(["directories", "x_expressions", "x_tick_labels"], [os.path.abspath(output_directory), processes, ["no cuts"] + cut_strings])

	config_list.append(config.return_config())

	return config_list

def limitplot(config_list, channel, x, parameter_info, weights):

	##Read out limits and sigma bands from output of higgs combined and save them into lists
	directory = os.path.abspath(os.path.expandvars("$CMSSW_BASE/src/plots/LFV_datacards/datacards"))
	output_directory = os.path.abspath(os.path.expandvars("$CMSSW_BASE/src/plots/FlavioOutput/Limits"))
	root_file = "/limit_" + channel + ".root"

	categories = [     #Bin IDs of categories as higg combined saves it, defined in python/datacards/datacardsconfig.py
			["One Jet",		"/category/3002"],	
			["Zero Jet",		"/category/3001"],
			["Combined", 		"/combined/"	]
	]

	limits = []
	avaible_category_label = []
	category_id = []

	for (category_label, category_directory) in categories:
		if(os.path.exists(directory + category_directory)):
			limit_file = ROOT.TFile.Open(directory + category_directory + "/higgsCombine.Asymptotic.mH125.root")
			tree = limit_file.Get("limit")

			limit_subfolder = []
			for quantile in tree:
				limit_subfolder.append(tree.limit)

			limits.append(limit_subfolder)
			avaible_category_label.append(category_label)

			try:
				category_id.append(int(category_directory.split("/")[2]))

			except ValueError:
				category_id.append(3000)


	##Write information into new root file with tree limit and branch sigma2down, sigma1down, limit, sigma1up, sigma2up
	ROOT.gROOT.ProcessLine(
	"struct MyStruct {\
		Float_t		two_sigma_down;\
		Float_t		one_sigma_down;\
		Float_t		limit_exp;\
		Float_t		limit_obs;\
		Float_t		one_sigma_up;\
		Float_t		two_sigma_up;\
		Int_t		category;\
		Int_t		bin_id;\
	};");


	if not os.path.exists(output_directory):
		os.mkdir(output_directory)

	if os.path.isfile(output_directory + root_file):
		os.remove(output_directory + root_file)

	output = ROOT.TFile(output_directory + root_file, "NEW")
	output_tree = ROOT.TTree("limit", "tree with limit values for categories")

	limit_struct = ROOT.MyStruct()

	branch_name = ["two_sigma_down", "one_sigma_down", "limit_exp", "limit_obs", "one_sigma_up", "two_sigma_up", "categories", "bin_id"]
	branch_adress = ["two_sigma_down", "one_sigma_down", "limit_exp", "limit_obs", "one_sigma_up", "two_sigma_up", "category", "bin_id"]
	branch_parameter = ["two_sigma_down/F", "one_sigma_down/F", "limit_exp/F", "limit_obs/F", "one_sigma_up/F", "two_sigma_up/F", "category/I", "bin_id/I"]

	for name, adress, parameter in zip(branch_name, branch_adress, branch_parameter):
		output_tree.Branch(name, ROOT.AddressOf(limit_struct, adress), parameter)

	for index in range(len(limits)):
		limit_struct.two_sigma_down	= 	limits[index][0] 
		limit_struct.one_sigma_down 	= 	limits[index][1] 
		limit_struct.limit_exp		= 	limits[index][2]
		limit_struct.limit_obs 		= 	limits[index][5] 
		limit_struct.one_sigma_up 	= 	limits[index][3] 
		limit_struct.two_sigma_up 	= 	limits[index][4] 
		limit_struct.category 		= 	index
		limit_struct.bin_id 		= 	category_id[index]
	
		output_tree.Fill()

	output.Write()
	output.Close()

	##Write config for limit plots
	config = configmaster.ConfigMaster(base_config(channel, x[0], parameter_info, weights)[0])
	config.add_config_info(limit_config(channel, x, parameter_info)[0], 0)
	config.add_config_info(limit_config(channel, x, parameter_info)[1], 8)
	config.pop("directories")
	config.change_config_info(["directories", "y_tick_labels", "y_lims"], [os.path.abspath(output_directory), avaible_category_label, index + 0.5])

	config_list.append(config.return_config())

	##Supress plotting of observed limit
	del config_list[0]["tree_draw_options"][-1]
	del config_list[0]["x_expressions"][-1]
	del config_list[0]["nicks"][-1]

	return config_list
	

###Main Function

def main():

	###Call and get parser arguments
	args = parser()

	##Define libary with all analysis modules of flavio
	Analysismodule_libary = {
				Analysismodule.control_plot:		controlplot,
				Analysismodule.effiency_plot:		efficiencyplot,
				Analysismodule.shape_plot:		shapeplot,
				Analysismodule.cut_optimization:	cutoptimization,
				Analysismodule.bkg_reduction_plot:	bkgreductionplot,
				Analysismodule.nminus1_plot:		nminus1plot,
				Analysismodule.cutflow_plot:		cutflowplot,
				Analysismodule.limit_plot:		limitplot
	}

	##Create instance of class for parameter information
	parameter_info = parametermaster.ParameterMaster()

	###Write config using your desired analysis function
	config_list = []
	config_list = Analysismodule_libary[args.analysis](config_list, args.channel, args.x_expression, parameter_info, args.weight_options)
	
	#pprint.pprint(config_list[0])	

	###Call MVP harry.py to get your job done
	higgsplot.HiggsPlotter(list_of_config_dicts=config_list, n_plots = len(config_list))
	

main()
