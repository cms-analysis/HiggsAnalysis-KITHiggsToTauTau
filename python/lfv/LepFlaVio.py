#! /usr/bin/env python

import argparse
import os
import sys
import yaml
import subprocess

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

###Function for parser calls

def parser():
	
	parser = argparse.ArgumentParser(description = "Analysis and plotting beast (using harry.py the MVP) for LFV", formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument("-a", "--analysis", required = True,  action = "store", choices = range(8), type = int, help = "Your choice of specific analysis function. Number of jets and category option can be choosen. Use this key to get the your analysis function of desire: \n" 					
				"0: Make a controlplot					supports: Number of jets/category			x_expression use: Choose one or more you want to plot)\n" 
				"1: Make a cut effieciency plot				supports: Number of jets/category			x_expression use: Choose one or more you want to plot)\n"			
				"2: Make a shape plot					supports: Number of jets/category			x_expression use: Choose one or more you want to plot)\n"
				"3: Do a cut optimization				Needs:    Number of jets No supporting: category	x_expression use: Choose set to be optimized as cut\n"					
				"4: Make a N-1 plot using results of optimized cuts	Needs:    Number of jets No supporting: category	x_expression use: Does not matter\n"         	
				"5: Make a cutflow plot with optmized cuts		Needs:    Number of jets No supporting: category	x_expression use: Choose one to see how optimized cuts would work\n"
				"6: Do a limit plot					supports: None						x_expression use: Only comtibable with option 10\n")
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
				"11: Impact parameter of second lepton\n")
	parser.add_argument("-c", "--channel", required = True, action = "store", choices = ["em", "et", "mt"], type = str, help = "Your choice of final state which should be analysed")

	return parser.parse_args()

###Global constants/functions
def global_constants(args):
	global config_info, parameter_info, cut_info, sample_list, flavio_path, channel, x, weight, categories, weight_name, category_name, jet_number

	##Inputs from parser
	channel		=	args.channel
	x		=	args.x_expression
	jet_number 	= 	args.jet_number

	##File to read/write informations
	try:
		cut_info	=	yaml.load(open(os.path.abspath(os.path.expandvars("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/python/lfv/cuts.yaml")), "r"))
	except IOError:
		cut_file 	= 	open(os.path.abspath(os.path.expandvars("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/python/lfv/cuts.yaml")), "w")
		cut_file.close()

		cut_info 	= yaml.load(open(os.path.abspath(os.path.expandvars("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/python/lfv/cuts.yaml")), "r"))
	
	config_info	=	yaml.load(open(os.path.abspath(os.path.expandvars("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/python/lfv/config_info.yaml")), "r"))
	parameter_info  =	yaml.load(open(os.path.abspath(os.path.expandvars("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/python/lfv/parameter.yaml")), "r"))
	
	##Output path
	flavio_path	= 	os.path.abspath(os.path.expandvars("$CMSSW_BASE/src/plots/FlavioOutput/"))

	##samples	
	sample_list 	=	["z" + channel, "ztt", "zll", "ttj", "vv", "wj", "qcd"]

	##weight and category
	weight 		= 	["(njetspt30==0)","(njetspt30==1)"][args.jet_number] if args.jet_number != None else "1"
	weight_name	=	["_zerojet", "_onejet"][args.jet_number] if args.jet_number != None else ""
	category_name	=	"_optimized" if args.category != None else ""

def base_config(channel, parameter, parameter_info, nick_suffix = "", no_plot = False, weights = "njetspt30==1"):

	x,bins,output = parameter_info.get_parameter_info(parameter, 0)

	input_dir 	= 	["/net/scratch_cms3b/croote/artus/2017-11-09_14-46_SM-control/merged/"]
	output_dir	=	os.path.abspath(os.path.expandvars("$CMSSW_BASE/src/plots/FlavioOutput/"))
	output_file	= 	output
	format 		= 	["pdf", "png"]
	www		= 	channel + "/"
	www_nodate	=	True
	nick_suffix	=	nick_suffix

	sample_list	= 	["z" + channel, "ztt", "zll", "ttj", "vv", "wj", "qcd"]
	channel 	= 	channel
	category	= 	None
	no_plot		=	no_plot
	weights		=	weights

	x_expressions	=	[x]
	x_bins	 	=	[bins]
	
	base_values = [input_dir, output_dir, output_file, format, www, www_nodate, x_expressions, x_bins]
	samples_values = [sample_list, channel, category, no_plot, nick_suffix, weights]

	return base_values, samples_values	

def controlplot_config(channel, parameter, parameter_info):

	x_label		=	parameter_info.get_parameter_info(parameter, 1)
	title 		=	"Controlplot " + "(" + channel + ")"
	legend		=	[0.65, 0.65, 1.00, 0.88]
	lumis 		= 	[35.87]
	energies	=	[13]
	year		=	"2016"
	www 		=	"Controlplot"

	controlplot_values = [x_label, title, legend, lumis, energies, year, www]
	
	return controlplot_values

def efficiency_config(parameter, bkg_nicks, lower_cut = True):
	analysis_mod, markers, y_label, cut_modes, cut_nicks, whitelist 	=	 config_info[1][:6]	
	legend, lumis, energies, year, www						= config_info[1][6:]
	x_label										= parameter_info[parameter][3]
	
	title 			=	"Efficiencyplot " + "(" + channel + ")"
	sig_nicks		=	["z" + channel + "noplot"]

	return [x_label, title, legend, lumis, energies, year, www], [analysis_mod, bkg_nicks, markers, y_label, cut_modes, sig_nicks, cut_nicks, whitelist, lower_cut]

def shape_config(parameter):
	y_label, analysis_mod			= config_info[2][:2]
	legend, lumis, energies, year, www	= config_info[2][2:]
	x_label					= parameter_info[parameter][3]
	
	sumofhists_values = [analysis_mod, sum_nicks, result_nicks]
	
	return sumofhists_values

	
def efficiency_config(channel, parameter, parameter_info, lower_cut = "True", plot_modules = ["PlotRoot"]):

	x_label		=	parameter_info.get_parameter_info(parameter, 1)
	output_dir	= 	"/CutOptimization/CutHistogram/"
	analysis_mod	=  	"CutEfficiency"
	bkg_nicks 	=	["bkg_sum"]	
	sig_nicks	=	["z" + channel + "noplot"]
	cut_modes	=	["sOverSqrtSB"]
	cut_nicks	= 	["sOverSqrtSB_" + str(parameter)]
	whitelist	= 	["sOverSqrtSB_" + str(parameter)]
	markers		=	["E"]
	y_label 	= 	"S/#sqrt{S+B}"
	www 		=	"CutEfficiency"
	lower_cut 	= 	lower_cut
	plot_modules	= 	plot_modules

	efficiency_values = [analysis_mod, bkg_nicks, sig_nicks, cut_modes, cut_nicks, whitelist, markers, x_label, y_label, www, lower_cut, plot_modules, output_dir]

	return efficiency_values

def shape_config(channel, parameter, parameter_info):

	x_label		=	parameter_info.get_parameter_info(parameter, 1)
	title 		=	"Shapeplot " + "(" + channel + ")"
	legend		=	[0.65, 0.65, 1.00, 0.88]
	lumis 		= 	[35.87]
	energies	=	[13]
	year		=	"2016"
	www 		=	"Shapeplot"
	y_label		=	"arb. units"
	analysis_mod	= 	"NormalizeToUnity"
	
	shape_values = [x_label, title, legend, lumis, energies, year, www, y_label, analysis_mod]
	
	return shape_values

###Analysis function using the specific plotting modules

def controlplot(config_list, channel, x, parameter_info):
	for index, parameter in enumerate(x):
		config = configmaster.ConfigMaster(*base_config(channel, parameter, parameter_info))
		config.add_config_info(controlplot_config(channel, parameter, parameter_info), 0)
		config_list.append(config.return_config())
		
		config_list[index]["weights"][0] += "*50"

	return config_list

def efficiencyplot(config_list, channel, x, parameter_info):
	for parameter in x:
		config = configmaster.ConfigMaster(*base_config(parameter, nick_suffix = "noplot", no_plot = True))
		config.add_config_info(sumofhists_config(["zttnoplot zllnoplot ttjnoplot vvnoplot wjnoplot qcdnoplot"], ["bkg_sum"]), 1)
		config.add_config_info(efficiency_config(parameter, ["bkg_sum"])[0], 0)
		config.add_config_info(efficiency_config(parameter, ["bkg_sum"])[1], 2)
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

def cutoptimization(config_list):
	##Information to create weight string for harry plotter
	cut_side    = ["<" for parameter in x]
	cut_values  = range(len(cut_side))
	cut_strings = [parameter_info[parameter][4] for parameter in x]

	for index1 in range(3):
		for index2, parameter in enumerate(x):
			##Create N-1 weight for Nth parameter if not zero Iteration
			if index1 != 0:
				weights = "*".join([cut_strings[index3].format(side = side, cut = value) for index3, (side, value) in enumerate(zip(cut_side, cut_values)) if index2 != index3])

			##Create harry plotter config
			config = configmaster.ConfigMaster(*base_config(parameter, nick_suffix = "noplot", no_plot = True, weight_input = "1" if index1 == 0 else weights))
			config.add_config_info(sumofhists_config(["zttnoplot zllnoplot ttjnoplot vvnoplot wjnoplot qcdnoplot"], ["bkg_sum"]), 1)
			config.add_config_info(efficiency_config(parameter, ["bkg_sum"], lower_cut = True if cut_side[index2] == "<" else False)[1], 2)
			config.pop(["www", "www_nodate"])
			config.change_config_info(["filename", "plot_modules"], ["_" + channel, "ExportRoot"])
		
			##Create config in zero iteration to check on which side the cut should be applied
			if(index1 == 0):
				config2 = config.copy()
				config2.replace("select_lower_values", False)
				config2.change_config_info("filename", "_2")
		
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

	for index1, parameter in enumerate(cut_info[0 if weight == "(njetspt30==0)" else 1][channel].keys()):
		##Construct weight for N-1 plot	
		weights = "*".join([cut_strings[index2].format(side = side, cut = value) for index2, (side, value) in enumerate(zip(cut_side, cut_values)) if index1 != index2])

		#Build config
		config = configmaster.ConfigMaster(*base_config(parameter, weight_input = weights))
		config.add_config_info(nminus1_config(parameter), 0)
		config.change_config_info("vertical_lines", [cut_values[index1]])

		config_list.append(config.return_config())

	return config_list
		
def cutflowplot(config_list):
	##Import math for s/sqrt(s+b) 
	from math import sqrt

	##Name of output root file
	root_file = "/cutflow_" + channel + ".root"

	##Construct list of weights = [no cut, cut1, cut1+cut2, ..., cut1+...+cutN]
	cut_strings = [parameter_info[param][4] for param in cut_info[0 if weight == "(njetspt30==0)" else 1][channel].keys()]
	cut_values, cut_side = [[entry[index] for entry in cut_info[0 if weight == "(njetspt30==0)" else 1][channel].values()] for index in [0,1]]
	weight_list = ["1"] + ["*".join(cut_strings[index].format(cut = cut, side = side) for index, (cut, side) in enumerate(zip(cut_values[:1 + index2], cut_side[:1 + index2]))) for index2 in range(len(cut_strings))]

	##Using harry.py the magician to get root files, read out for each process the total number of events and save them in hists as list for each weight
	hists = []
	configs = []
	for index, weights in enumerate(weight_list):
		config = configmaster.ConfigMaster(*base_config(x[0], weight_input = weights))
		config.change_config_info("plot_modules", "ExportRoot")
		config.pop(["www", "www_nodate", "legend_markers"])
		config.change_config_info("filename", str(index))
		configs.append(config.return_config())

	higgsplot.HiggsPlotter(list_of_config_dicts=configs, n_plots = len(configs), batch = "rwthcondor")	

	for index in range(len(weight_list)):
		root = ROOT.TFile.Open(flavio_path + "/VisibleMass"  + weight_name + str(index) + ".root")
		hists.append([root.Get(process).Integral() for process in sample_list])
		hists[index].append(hists[index][0]/sqrt(hists[index][0] + sum(hists[index][1:])))

	for filetype in [".root", ".json"]:
		for index in range(len(weight_list)):
			os.remove(flavio_path + "/VisibleMass" + weight_name + str(index) + filetype)

	##Use ROOT to fill hists in a new root file in which each process is a hist with the Number of events for each weight applied
	if not os.path.exists(flavio_path):
		os.mkdir(flavio_path)

	if os.path.isfile(flavio_path + root_file):
		os.remove(flavio_path + root_file)

	for index1, process in enumerate(sample_list + ["soverb"]):	
		output = ROOT.TFile(flavio_path + root_file, "UPDATE")
		root_hist = ROOT.TH1F(process, process, len(hists), 0, len(hists))
		for index2, hist in enumerate(hists):
			root_hist.SetBinContent(index2+1, hist[index1])

		output.Write()
		output.Close()

	##Write config for cutflow plots
	config = configmaster.ConfigMaster(base_config(x[0], no_plot = True)[0])
	config.add_config_info(cutflow_config(x[0])[0], 0)
	config.add_config_info(cutflow_config(x[0])[1], 5)
	config.pop(["directories", "x_expressions", "x_bins"])
	config.change_config_info(["directories", "x_expressions", "x_tick_labels"], [flavio_path, sample_list + ["soverb"], ["no cuts"] + cut_strings])
	config.print_config()

	config_list.append(config.return_config())

	return config_list

def limitplot(config_list):
	##Read out limits and sigma bands from output of higgs combined and save them into lists
	directory = os.path.abspath(os.path.expandvars("$CMSSW_BASE/src/plots/LFV_datacards/datacards"))
	root_file = "/limit_" + channel + ".root"

	categories = [     #Bin IDs of categories as higg combined saves it, defined in python/datacards/datacardsconfig.py
			["One Jet",		"/category/3002"],	
			["Zero Jet",		"/category/3001"],
			["Combined", 		"/combined/"	]
	]
	old_limits = {
			"em":		7.3e-7,
			"et":		9.8e-6,
			"mt":		1.2e-5
	}		

	limits = []
	avaible_category_label = []
	category_id = []

	for (category_label, category_directory) in categories:
		if(os.path.exists(directory + category_directory)):
			limit_file = ROOT.TFile.Open(directory + category_directory + "/higgsCombine.AsymptoticLimits.mH125.root")
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

	if os.path.isfile(flavio_path + root_file):
		os.remove(flavio_path + root_file)

	output = ROOT.TFile(flavio_path + root_file, "NEW")
	output_tree = ROOT.TTree("limit", "tree with limit values for categories")

	limit_struct = ROOT.MyStruct()

	branch_name = ["two_sigma_down", "one_sigma_down", "limit_exp", "limit_obs", "one_sigma_up", "two_sigma_up", "categories", "bin_id"]
	branch_adress = ["two_sigma_down", "one_sigma_down", "limit_exp", "limit_obs", "one_sigma_up", "two_sigma_up", "category", "bin_id"]
	branch_parameter = ["two_sigma_down/F", "one_sigma_down/F", "limit_exp/F", "limit_obs/F", "one_sigma_up/F", "two_sigma_up/F", "category/I", "bin_id/I"]

	for name, adress, parameter in zip(branch_name, branch_adress, branch_parameter):
		output_tree.Branch(name, ROOT.AddressOf(limit_struct, adress), parameter)

	for index in range(len(limits)):
		limit_struct.two_sigma_down	= 	limits[index][0]*old_limits[channel]
		limit_struct.one_sigma_down 	= 	limits[index][1]*old_limits[channel]
		limit_struct.limit_exp		= 	limits[index][2]*old_limits[channel]
		limit_struct.limit_obs 		= 	limits[index][5]*old_limits[channel] 
		limit_struct.one_sigma_up 	= 	limits[index][3]*old_limits[channel] 
		limit_struct.two_sigma_up 	= 	limits[index][4]*old_limits[channel] 
		limit_struct.category 		= 	index
		limit_struct.bin_id 		= 	category_id[index]
	
		output_tree.Fill()

	output.Write()
	output.Close()

	##Write config for limit plots
	config = configmaster.ConfigMaster(base_config(x[0])[0])
	config.add_config_info(limit_config(x[0])[0], 0)
	config.add_config_info(limit_config(x[0])[1], 7)
	config.pop("directories")
	config.change_config_info(["directories", "y_tick_labels", "y_lims"], [os.path.abspath(flavio_path), avaible_category_label, len(limits) -1 + 0.5])
	config.print_config()

	config_list.append(config.return_config())
	
	##Supress plotting of observed limit
	del config_list[0]["tree_draw_options"][-1]
	del config_list[0]["x_expressions"][-1]
	del config_list[0]["nicks"][-1]



###Main Function

def main():

	###Call and get parser arguments
	args = parser()

	##Define libary with all analysis modules of flavio
	Analysismodule_libary = {
				Analysismodule.control_plot:		controlplot,
				Analysismodule.effiency_plot:		efficiencyplot,
				Analysismodule.shape_plot:		shapeplot,
				Analysismodule.cut_optimization:	cutoptimization
	}

	##Create instance of class for parameter information
	parameter_info = parametermaster.ParameterMaster()

	###Write config using your desired analysis function
	config_list = []
	config_list = Analysismodule_libary[args.analysis](config_list, args.channel, args.x_expression, parameter_info)
	
	#pprint.pprint(config_list[0])	

	###Call MVP harry.py to get your job done

	higgsplot.HiggsPlotter(list_of_config_dicts=config_list, n_plots = len(config_list), batch = "rwthcondor" if len(config_list) != 1 else None)
	if len(config_list) != 1: subprocess.Popen("cd $CMSSW_BASE/src/websync/; webplot.py {channel} -r -c".format(channel = channel), shell = True)

main()
