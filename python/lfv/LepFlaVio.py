#! /usr/bin/env python

import argparse
import os
import sys
import ConfigParser

import HiggsAnalysis.KITHiggsToTauTau.plotting.higgsplot as higgsplot
import HiggsAnalysis.KITHiggsToTauTau.lfv.ConfigMaster as configmaster

import ROOT

import pprint

###Enumeration classes for analysis functions of flavio

class Analysismodule():
	control_plot = 0
	effiency_plot = 1
	shape_plot = 2
	cut_optimization = 3

class Parameter():
	m_vis = 0
	ptofsumdilep = 1
	mt_1 = 2
	mt_2 = 3
	number_jets = 4
	met = 5
	delta_phi = 6
	delta_phi_CM = 7
	delta_pt_jetdilep = 8
	pzeta = 9
	impact_1 = 10	
	impact_2 = 11
	

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

def base_config(channel, parameter, nick_suffix = "", no_plot = False, weights = "njetspt30==1"):

	x,bins,output = parameter_values(parameter)

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

def controlplot_config(channel, parameter):
	
	label = parameter_labels(parameter)

	x_label		=	label
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

	
def efficiency_config(channel, parameter, lower_cut = "True", plot_modules = ["PlotRoot"]):

	label = parameter_labels(parameter)

	x_label		=	label
	output_dir	= 	"/CutOptimization/CutHistogram/"
	analysis_mod	=  	"CutEfficiency"
	bkg_nicks 	=	["bkg_sum"]	
	sig_nicks	=	["z" + channel + "noplot"]
	cut_modes	=	["sOverSqrtSB"]
	cut_nicks	= 	["sOverSqrtSB_" + str(parameter)]
	whitelist	= 	["sOverSqrtSB_" + str(parameter)]
	markers		=	["E"]
	x_label		=	label
	y_label 	= 	"S/#sqrt{S+B}"
	www 		=	"CutEfficiency"
	lower_cut 	= 	lower_cut
	plot_modules	= 	plot_modules

	efficiency_values = [analysis_mod, bkg_nicks, sig_nicks, cut_modes, cut_nicks, whitelist, markers, x_label, y_label, www, lower_cut, plot_modules, output_dir]

	return efficiency_values

def shape_config(channel, parameter):
	label = parameter_labels(parameter)

	x_label		=	label
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
	

###Function saving values for specific pameters

def parameter_values(parameter):
	parameter_values = {
				Parameter.m_vis:		["m_vis", "100,0,170", "VisibleMass"],
				Parameter.ptofsumdilep:		["diLepLV.Pt()", "100,0,200", "PtOfMomentaSumDiLep"],
				Parameter.mt_1:			["mt_1", "100,0,200", "TransverseMass1"],
				Parameter.mt_2:			["mt_2", "100,0,200", "TransverseMass2"],
				Parameter.number_jets:		["njetspt30", "4,0,4", "NumberOfJets"], 
				Parameter.met:			["met", "100,0,140", "MissingTranverseEnergy"],
				Parameter.delta_phi:		["abs(abs(phi_1 - phi_2) - 3.14)", "100,0,3", "DeltaPhi"],
				Parameter.delta_phi_CM:		["abs(abs(lep1LV.BoostToCM().phi() - lep2LV.BoostToCM().phi()) - 3.14)", "100,0,3", "DeltaPhiCM"],
				Parameter.delta_pt_jetdilep:	["abs(diLepLV.Pt() -  leadingJetLV.Pt())", "100,0,200", "DeltaPtJetDilep"],
				Parameter.pzeta:		["pZetaMissVis", "100,-130,130", "PZeta"],
				Parameter.impact_1:		["abs(d0_1)", "100,0,0.03", "ImpactParameter1"],
				Parameter.impact_2:		["abs(d0_2)", "100,0,0.03", "ImpactParameter2"]
	}

	return parameter_values[parameter]

def parameter_labels(parameter):		

	parameter_labels = {
				Parameter.m_vis:		"m_{vis}",
				Parameter.ptofsumdilep:		"(#sump^{#mu})_{T}",
				Parameter.mt_1:			"m_{T}",
				Parameter.mt_2:			"m_{T}",
				Parameter.number_jets:		"Number of jets",
				Parameter.met:			"#slash{E}_{T}",
				Parameter.delta_phi:		"||#Delta#phi| - #pi|",
				Parameter.delta_phi_CM:		"||#Delta#phi_{CM}| - #pi|",
				Parameter.delta_pt_jetdilep:	"|p_{T}(jet) - (#sump^{#mu})_{T}|",
				Parameter.pzeta:		"#left(p^{miss}_{#zeta} #minus 0.85 p^{vis}_{#zeta}#right)",
				Parameter.impact_1:		"|d_{0}|",
				Parameter.impact_2:		"|d_{0}|"
	}
	
	return parameter_labels[parameter]

def parameter_weights(parameter):
	parameter_weights = {
				Parameter.ptofsumdilep:		"(diLepLV.Pt()<{cut})",
				Parameter.mt_1:			"(mt_1<{cut})",
				Parameter.mt_2:			"(mt_2<{cut})",
				Parameter.delta_phi:		"(abs(abs(phi_1 - phi_2) - 3.14)<{cut})",
				Parameter.met:			"(met<{cut})",
				Parameter.delta_phi_CM:		"(abs(abs(lep1LV.BoostToCM().phi() - lep2LV.BoostToCM().phi()) - 3.14)<{cut})",
				Parameter.delta_pt_jetdilep:	"(abs(diLepLV.Pt() -  leadingJetLV.Pt())<{cut})",
				Parameter.impact_1:		"(abs(d0_1)<{cut})",
				Parameter.impact_2:		"(abs(d0_2)<{cut})",
				Parameter.pzeta:		"(pZetaMissVis<{cut})"
				
	}
		
	return parameter_weights[parameter]


###Additional help function not using harry.py
def weightaddition(cut_parameter, cut_values):
	weight = ""
	for index, cut in enumerate(cut_parameter):
		if index == 0:
			weight = parameter_weights(cut).format(cut = cut_values[index])

		else:
			weight = weight + "*" + parameter_weights(cut).format(cut = cut_values[index])

	return weight

def cutconfigwriter(path, filename, section, dictionary):
	if not os.path.exists(path):
		os.mkdir(path)

	ini_config = ConfigParser.ConfigParser()
	if os.path.exists(path + "/" + filename):
		ini_config.read(path + "/" + filename)
	ini_config.add_section(section)

	for (key, value) in dictionary.iteritems():
		ini_config.set(section, key, value)

	ini_file = open(path + "/" + filename, "w")
	ini_config.write(ini_file)
	ini_file.close()

	print "The cut information have been saved in " + filename + " under the section " + section + "."


def cutconfigreader(filename):
	cut_config = ConfigParser.ConfigParser()
	cut_config.read(filename)
	
	
###Analysis function using the specific plotting modules

def controlplot(config_list, channel, x):

	for index, parameter in enumerate(x):
		config = configmaster.ConfigMaster(*base_config(channel, parameter))
		config.add_config_info(controlplot_config(channel, parameter), 0)
		config_list.append(config.return_config())
		
		config_list[index]["weights"][0] += "*50"


	return config_list

def efficiencyplot(config_list, channel, x):
	for parameter in x:
		config = configmaster.ConfigMaster(*base_config(channel, parameter, nick_suffix = "noplot", no_plot = True))
		config.add_config_info(sumofhists_config(), 1)
		config.add_config_info(efficiency_config(channel, parameter), 2)
		config_list.append(config.return_config())
	
	return config_list

def shapeplot(config_list, channel, x):
	for index, parameter in enumerate(x):
		config = configmaster.ConfigMaster(*base_config(channel, parameter))
		config.add_config_info(shape_config(channel, parameter), 3)
		config_list.append(config.return_config())

		config_list[index].pop("stacks")
		config_list[index].pop("colors")
		config_list[index]["markers"] = ["LINE" for value in config_list[index]["markers"]]
	
	return config_list

def cutoptimization(config_list, channel, x):

	cut_values = {}
	path = os.path.abspath(os.path.expandvars("$CMSSW_BASE/src/plots/FlavioOutput/CutOptimization/CutValues/"))
	file_name = "cut_values_onejet2.ini"
	if  os.path.exists(path + "/" + file_name):
		os.remove(path + "/" + file_name)

	for index in range(5):
		for parameter in x:
			if(index != 0):
				cut_parameters = list(set(x).difference(set([parameter])))
				weight = weightaddition(cut_parameters, [cut_values[str(cut)] for cut in cut_parameters])
			del config_list[:]	
		
			config = configmaster.ConfigMaster(*base_config(channel, parameter, nick_suffix = "noplot", no_plot = True, weights = "1" if index==0 else weight))
			config.add_config_info(sumofhists_config(), 1)
			config.add_config_info(efficiency_config(channel, parameter, plot_modules = ["ExportRoot"]), 2)
			config_list.append(config.return_config())
	
			config_list[0].pop("www")
			config_list[0].pop("www_nodate")

			higgsplot.HiggsPlotter(list_of_config_dicts=config_list, n_plots = len(config_list))
			
			cut_file = ROOT.TFile.Open(os.path.abspath(os.path.expandvars("$CMSSW_BASE/src/plots/FlavioOutput/CutOptimization/CutHistogram/")) + "/" + parameter_values(parameter)[-1] + ".root")
			histogram = cut_file.Get("sOverSqrtSB_" + str(parameter))	
			cut_values[str(parameter)] = histogram.GetXaxis().GetBinCenter(histogram.GetMaximumBin())
			
		cutconfigwriter(path, file_name, "Iteration" + str(index), cut_values)

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

	###Write config using your desired analysis function
	config_list = []
	config_list = Analysismodule_libary[args.analysis](config_list, args.channel, args.x_expression)
	
	#pprint.pprint(config_list[0])	

	###Call MVP harry.py to get your job done
	higgsplot.HiggsPlotter(list_of_config_dicts=config_list, n_plots = len(config_list))
	

main()
