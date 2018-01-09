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
	limit_plot = 4

###Function for parser calls

def parser():
	
	parser = argparse.ArgumentParser(description = "Analysis and plotting beast (using harry.py the MVP) for LFV", formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument("-a", "--analysis", required = True,  action = "store", choices = range(5), type = int, help = "Your choice of specific analysis function. Use this key to get the your analysis function of desire: \n" "0: Make a controlplot \n" 
				"1: Make a cut effieciency plot\n"
				"2: Make a shape plot\n"
				"3: Do a cut optimization\n"
				"4: Do a limit plot n")
	parser.add_argument("-x", "--x_expression", choices = range(13), required = True, nargs="+", type = int, help = "Choice your parameter of desire. Multiple parameter keys could be given at once. Use this key to get the your paramter(s):\n"
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
				"12: Limit option which must be used with analysis argument 4\n")
	parser.add_argument("-c", "--channel", action = "store", required = True, choices = ["em", "et", "mt"], type = str, help = "Your choice of final state which should be analysed")

	return parser.parse_args()


###Function that stores and return information for the configs that will be written

def base_config(channel, parameter, parameter_info, nick_suffix = "", no_plot = False, weights = "njetspt30==1"):

	x,bins,output = parameter_info.get_parameter_info(parameter, 0)

	input_dir 		= 	["/net/scratch_cms3b/croote/artus/2017-11-09_14-46_SM-control/merged/"]
	output_dir		=	os.path.abspath(os.path.expandvars("$CMSSW_BASE/src/plots/FlavioOutput/"))
	output_file		= 	output
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
	weights			=	weights

	base_values = [input_dir, output_dir, output_file, format, www, www_nodate, x_expressions, x_bins]
	samples_values = [sample_list, channel, category, no_plot, nick_suffix, weights]

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


def sumofhists_config():
	analysis_mod		=	"SumOfHistograms"
	sum_nicks		=	["zttnoplot zllnoplot ttjnoplot vvnoplot wjnoplot qcdnoplot"]
	result_nicks		=	["bkg_sum"]
	
	return [analysis_mod, sum_nicks, result_nicks]

	
def efficiency_config(channel, parameter, parameter_info, lower_cut = "True", plot_modules = ["PlotRoot"]):

	x_label			=	parameter_info.get_parameter_info(parameter, 1)
	output_dir		= 	"/CutOptimization/"
	analysis_mod		=  	"CutEfficiency"
	bkg_nicks 		=	["bkg_sum"]	
	sig_nicks		=	["z" + channel + "noplot"]
	cut_modes		=	["sOverSqrtSB"]
	cut_nicks		= 	["sOverSqrtSB_" + str(parameter)]
	whitelist		= 	["sOverSqrtSB_" + str(parameter)]
	markers			=	["E"]
	y_label 		= 	"S/#sqrt{S+B}"
	www 			=	"CutEfficiency"
	lower_cut 		= 	lower_cut
	plot_modules		= 	plot_modules

	return [analysis_mod, bkg_nicks, sig_nicks, cut_modes, cut_nicks, whitelist, markers, x_label, y_label, www, lower_cut, plot_modules, output_dir]

def shape_config(channel, parameter, parameter_info):

	x_label			=	parameter_info.get_parameter_info(parameter, 1)
	title 			=	"Shapeplot " + "(" + channel + ")"
	legend			=	[0.65, 0.65, 1.00, 0.88]
	lumis 			= 	[35.87]
	energies		=	[13]
	year			=	"2016"
	www 			=	"Shapeplot"
	y_label			=	"arb. units"
	analysis_mod		= 	"NormalizeToUnity"
	
	return [x_label, title, legend, lumis, energies, year, www, y_label, analysis_mod]

def limit_config(parameter, parameter_info):
	y_label 		=	""
	x_label 		= 	"95% CL Limit #frac{BR(Z#rightarrowLFV)}{BR(Z#rightarrowLFV)^{current}}"
	files 			=	"limit.root"
	folders 		= 	["limit"]
	y_expressions		= 	["category"]
	markers			= 	["E5", "E5", "P", "P"]
	colors 			= 	["kYellow", "kGreen", "kBlack", "kBlack"]
	fill_styles 		= 	[3001]
	marker_styles 		= 	[20, 20, 20, 21]
	line_widths 		= 	[40, 40, 1, 1]
	tree_draw_options 	= 	["TGraphAsymmErrorsX", "TGraphAsymmErrorsX", "TGraph", "TGraph"]
	y_tick_labels	 	= 	[]
	www 			= 	"Limitplots"
	title			= 	"Limits"
	lumis 			= 	[35.87]
	energies		=	[13]
	year			=	"2016"
	legend			=	[0.67, 0.70, 0.92, 0.88]
	nicks 			=	["95% excepted", "68% excepted", "Excepted", "Observed"]
	y_lims 			= 	[],
	x_lims			=	[-0.2, 1.3]

	return [x_label, y_label, files, folders, y_expressions, markers, colors, fill_styles, marker_styles, line_widths, tree_draw_options, y_tick_labels, www, title, lumis, energies, year, legend, nicks, x_lims, y_lims]
	

###Analysis function using the specific plotting modules

def controlplot(config_list, channel, x, parameter_info):
	for index, parameter in enumerate(x):
		config = configmaster.ConfigMaster(*base_config(channel, parameter, parameter_info))
		config.add_config_info(controlplot_config(channel, parameter, parameter_info), 0)
		config_list.append(config.return_config())
		
		##Scale signal to see it in the plot
		config_list[index]["weights"][0] += "*50"

	return config_list

def efficiencyplot(config_list, channel, x, parameter_info):
	for parameter in x:
		config = configmaster.ConfigMaster(*base_config(channel, parameter, parameter_info, nick_suffix = "noplot", no_plot = True))
		config.add_config_info(sumofhists_config(), 1)
		config.add_config_info(efficiency_config(channel, parameter, parameter_info), 2)
		config_list.append(config.return_config())
	
	return config_list

def shapeplot(config_list, channel, x, parameter_info):
	for index, parameter in enumerate(x):
		config = configmaster.ConfigMaster(*base_config(channel, parameter, parameter_info))
		config.add_config_info(shape_config(channel, parameter, parameter_info), 3)
		config_list.append(config.return_config())

		##Delete information not needed
		config_list[index].pop("stacks")
		config_list[index].pop("colors")
		config_list[index]["markers"] = ["LINE" for value in config_list[index]["markers"]]
	
	return config_list

def cutoptimization(config_list, channel, x, parameter_info):

	##Define information for the cut config output
	cut_values = {}
	path = os.path.abspath(os.path.expandvars("$CMSSW_BASE/src/plots/FlavioOutput/CutOptimization/"))
	file_name = "cutvalues_onejet.ini"
	if os.path.exists(path + "/" + file_name):
		os.remove(path + "/" + file_name)

	for index in range(5):
		for parameter in x:

			##For first itereration no cuts are used, then N-1 cuts are applied for the N th parameter you look at
			if(index != 0):
				cut_parameters = list(set(x).difference(set([parameter])))
				cut_strings = parameter_info.get_parameter_info(cut_parameters, 2)
				weight = parameter_info.weightaddition(cut_strings, [cut_values[str(cut)] for cut in cut_parameters])
			del config_list[:]	
		
			##Fill harry plotter config to get S/sqrt(S+B) histograms 
			config = configmaster.ConfigMaster(*base_config(channel, parameter, parameter_info, nick_suffix = "noplot", no_plot = True, weights = "1" if index==0 else weight))
			config.add_config_info(sumofhists_config(), 1)
			config.add_config_info(efficiency_config(channel, parameter, parameter_info, plot_modules = ["ExportRoot"]), 2)
			
			config_list.append(config.return_config())
	
			##Delete www option not need for the root histograms
			config_list[0].pop("www")
			config_list[0].pop("www_nodate")

			##Call harry.py the MVP to get your job done
			higgsplot.HiggsPlotter(list_of_config_dicts=config_list, n_plots = len(config_list))

			##Read out produced histogramm for the N th parameter and find best cut value
			cut_file = ROOT.TFile.Open(os.path.abspath(os.path.expandvars("$CMSSW_BASE/src/plots/FlavioOutput/CutOptimization/")) + "/" +  parameter_info.get_parameter_info(parameter, 0)[-1] + ".root")
			histogram = cut_file.Get("sOverSqrtSB_" + str(parameter))	
			cut_values[str(parameter)] = histogram.GetXaxis().GetBinCenter(histogram.GetMaximumBin())
			
		
		##Write cut values from Iteration into cut config
		parameter_info.cutconfigwriter(path, file_name, "Iteration" + str(index), cut_values)

	
	sys.exit()

def limitplot(config_list, channel, x, parameter_info):

	##Read out limits and sigma bands from output of higgs combined and save them into lists
	directory = os.path.abspath(os.path.expandvars("$CMSSW_BASE/src/plots/LFV_datacards/datacards/"))
	categories = [	
			["LFVOneJet",		"/category/3004"],     #Bin IDs of categories as higg combined saves it, defined in python/datacards/datacardsconfig.py
			["LFVOneJet_mt",	"/category/3003"],	
			["LFVZeroJet",		"/category/3002"],
			["LFVZeroJet_mt",	"/category/3001"],
			["Combined", 		"/combined/"	]
	]

	limits = []
	avaible_category_label = []


	for (category_label, category_directory) in categories:
		if(os.path.exists(directory + category_directory)):
			limit_file = ROOT.TFile.Open(directory + category_directory + "/higgsCombine.Asymptotic.mH125.root")
			tree = limit_file.Get("limit")

			limit_subfolder = []
			for quantile in tree:
				limit_subfolder.append(tree.limit)

			limits.append(limit_subfolder)
			avaible_category_label.append(category_label)

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
	};");


	if os.path.isfile("limit.root"):
		os.remove("limit.root")

	output = ROOT.TFile("limit.root", "NEW")
	output_tree = ROOT.TTree("limit", "tree with limit values for categories")

	limit_struct = ROOT.MyStruct()

	branch_name = ["two_sigma_down", "one_sigma_down", "limit_exp", "limit_obs", "one_sigma_up", "two_sigma_up", "categories"]
	branch_adress = ["two_sigma_down", "one_sigma_down", "limit_exp", "limit_obs", "one_sigma_up", "two_sigma_up", "category"]
	branch_parameter = ["two_sigma_down/F", "one_sigma_down/F", "limit_exp/F", "limit_obs/F", "one_sigma_up/F", "two_sigma_up/F", "category/I"]

	for name, adress, parameter in zip(branch_name, branch_adress, branch_parameter):
		output_tree.Branch(name, ROOT.AddressOf(limit_struct, adress), parameter)

	for index in range(len(limits)):
		limit_struct.two_sigma_down = limits[index][0] 
		limit_struct.one_sigma_down = limits[index][1] 
		limit_struct.limit_exp = limits[index][2]
		limit_struct.limit_obs = limits[index][5] 
		limit_struct.one_sigma_up = limits[index][3] 
		limit_struct.two_sigma_up = limits[index][4] 
		limit_struct.category = index
	
		output_tree.Fill()

	output.Write()
	output.Close()

	

	##Write config for limit plots
	config = configmaster.ConfigMaster(base_config(channel, x[0], parameter_info)[0])
	config.add_config_info(limit_config(x, parameter_info), 5)

	config_list.append(config.return_config())

	##Do specific config changes
	config_list[0]["directories"] = os.path.abspath(os.path.expandvars("$CMSSW_BASE/src/"))
	for index in range(len(avaible_category_label)):
		config_list[0]["y_tick_labels"].append(avaible_category_label[index])
	config_list[0]["y_lims"] = [-0.5, index + 0.5]

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
				Analysismodule.limit_plot:		limitplot
	}

	##Create instance of class for parameter information
	parameter_info = parametermaster.ParameterMaster()

	###Write config using your desired analysis function
	config_list = []
	config_list = Analysismodule_libary[args.analysis](config_list, args.channel, args.x_expression, parameter_info)
	
	pprint.pprint(config_list[0])	

	###Call MVP harry.py to get your job done
	higgsplot.HiggsPlotter(list_of_config_dicts=config_list, n_plots = len(config_list))
	

main()
