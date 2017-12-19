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

###Function for parser calls

def parser():
	
	parser = argparse.ArgumentParser(description = "Analysis and plotting beast (using harry.py the MVP) for LFV", formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument("-a", "--analysis", required = True,  action = "store", choices = range(4), type = int, help = "Your choice of specific analysis function. Use this key to get the your analysis function of desire: \n" "0: Make a controlplot \n" 
				"1: Make a cut effieciency plot\n"
				"2: Make a shape plot\n"
				"3: Do a cut optimization\n")
	parser.add_argument("-x", "--x_expression", required = True, choices = range(12), nargs="+", type = int, help = "Choice your parameter of desire. Multiple parameter keys could be given at once. Use this key to get the your paramter(s):\n"
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


###Function that stores and return information for the configs that will be written

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


def sumofhists_config():
	analysis_mod	=	"SumOfHistograms"
	sum_nicks	=	["zttnoplot zllnoplot ttjnoplot vvnoplot wjnoplot qcdnoplot"]
	result_nicks	=	["bkg_sum"]
	
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
	path = os.path.abspath(os.path.expandvars("$CMSSW_BASE/src/plots/FlavioOutput/CutOptimization/CutValues/"))
	file_name = "cut_values_onejet2.ini"
	if os.path.exists(path + "/" + file_name):
		os.remove(path + "/" + file_name)

	for index in range(5):
		for parameter in x:

			##For first itereration no cuts are used, then N-1 cuts are applied for the N th parameter you look at
			if(index != 0):
				cut_parameters = list(set(x).difference(set([parameter])))
				cut_strings = parameter_info.get_parameter_info(cut_parameters, 2)
				weight = parameter_info.weightaddition(cut_strings, [cut_values[str(cut)] for cut in cut_parameters])
				print weight
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
			cut_file = ROOT.TFile.Open(os.path.abspath(os.path.expandvars("$CMSSW_BASE/src/plots/FlavioOutput/CutOptimization/CutHistogram/")) + "/" +  parameter_info.get_parameter_info(parameter, 0)[-1] + ".root")
			histogram = cut_file.Get("sOverSqrtSB_" + str(parameter))	
			cut_values[str(parameter)] = histogram.GetXaxis().GetBinCenter(histogram.GetMaximumBin())
			
		
		##Write cut values from Iteration into cut config
		parameter_info.cutconfigwriter(path, file_name, "Iteration" + str(index), cut_values)

	sys.exit()



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
	higgsplot.HiggsPlotter(list_of_config_dicts=config_list, n_plots = len(config_list))
	

main()
