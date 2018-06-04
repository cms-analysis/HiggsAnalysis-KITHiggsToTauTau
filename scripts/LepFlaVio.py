#! /usr/bin/env python

import argparse
import os
import sys
import yaml
import subprocess
from multiprocessing import Pool, cpu_count

import HiggsAnalysis.KITHiggsToTauTau.plotting.higgsplot as higgsplot
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.configmaster as configmaster

import ROOT

###Enumeration class for analysis functions of flavio

class Analysismodule():
	control_plot = 0
	effiency_plot = 1
	shape_plot = 2
	cut_optimization = 3
	nminus1_plot = 4
	cutflow_plot = 5
	limit_plot = 6

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
				"6: Do a limit plot					supports: None						x_expression use: If x= 30 is used, plot will be produces, only will be will created\n")
	parser.add_argument("-x", "--x_expression", choices = range(31), required = True, nargs="+", type = int, help = "Choice your parameter of desire. Multiple parameter keys could be given at once. Use this key to get the your paramter(s):\n"
				"0:  Visible Mass\n" 
				"1:  Transverse momenta of sum of all lepton momenta\n"
				"2:  Transverse mass of lepton 1\n"
				"3:  Transverse mass of lepton 2\n"
				"4:  Number of jets\n"			
				"5:  Missing tranverse energy\n"
				"6:  Difference of jet transverse momenta and dilepton transverse momenta\n"
				"7:  Some crazy parameter I even dont know about\n"
				"8:  Impact parameter of first lepton\n"
				"9:  Impact parameter of second lepton\n"
				"10  Trannverse momentum\n"
				####ADD NEW PARAMETER
				"30: Limit option which must be used with analysis argument 4\n")
	parser.add_argument("-c", "--channel", action = "store", required = True, choices = ["em", "et", "mt", "gen"], type = str, help = "Your choice of final state which should be analysed")
	parser.add_argument("--jet-number", action = "store", choices = range(2), type = int, help = "Optional argument for choosing a constraint on the number of jets. Use this key to get the your jet number:\n"
				"0: Only events with zero jets are choosen\n"
				"1: Only events with one jet are choosen\n")
	parser.add_argument("--category", action = "store", choices = range(2), type = int, help = "Optional argument for to apply cuts of a categorization. Notice a cut optimzation had to be done once. Use this key to get the your category:\n"
				"0: Zero jet category\n"
				"1: One jet category\n")
	parser.add_argument("--data", action="store_true", default=False, help = "Use real data") 
	parser.add_argument("--signal", action="store_true", default=True, help = "Use signal")  

	return parser.parse_args()

###Global constants/functions
def global_constants(args):
	global config_info, parameter_info, cut_info, sample_list, flavio_path, channel, x, weight, categories, weight_name, category_name, jet_number, data, signal

	##Inputs from parser
	data		=	args.data
	signal 		=	args.signal
	channel		=	args.channel
	x		=	args.x_expression
	jet_number 	= 	args.jet_number


	##File to read/write informations
	try:
		cut_info	=	yaml.load(open(os.environ["CMSSW_BASE"] + "/src/FlavioOutput/Configs/cuts.yaml", "r"))
	except IOError:
		cut_file 	= 	open(os.environ["CMSSW_BASE"] + "/src/FlavioOutput/Configs/cuts.yaml", "w")
		cut_file.close()

		cut_info 	= yaml.load(open(os.environ["CMSSW_BASE"] + "/src/FlavioOutput/Configs/cuts.yaml", "r"))
	
	config_info	=	yaml.load(open(os.environ["CMSSW_BASE"] + "/src/FlavioOutput/Configs/config_info.yaml", "r"))
	parameter_info  =	yaml.load(open(os.environ["CMSSW_BASE"] + "/src/FlavioOutput/Configs/parameter.yaml", "r"))
	
	##Output path
	flavio_path	= 	os.path.abspath(os.path.expandvars("$CMSSW_BASE/src/FlavioOutput/"))

	##samples
	if args.analysis != 4:	
		sample_list 	= 	["ztt", "zll", "ttj", "vv", "wj", "qcd"]  + (["z" + channel] if signal else []) + (["data"] if data else [])

	else: 	
		sample_list 	= 	["z" + channel] # ["ztt", "zll", "ttj", "vv", "wj", "qcd"] + (["z" + channel] if signal else [])	

	##weight and category
	weight 		= 	["(njetspt30==0)","(njetspt30==1)"][args.jet_number] if args.jet_number != None else "1"
	weight_name	=	["_zerojet", "_onejet"][args.jet_number] if args.jet_number != None else ""
	category_name	=	"_optimized" if args.category != None else ""


	if args.category == None:
		categories = "1"

	else:
		cut_strings = [parameter_info[param][4] for param in cut_info[0 if weight == "(njetspt30==0)" else 1][channel].keys()]
		cut_values, cut_side = [[entry[index] for entry in cut_info[0 if weight == "(njetspt30==0)" else 1][channel].values()] for index in [0,1]]
		categories = "*".join([cut_strings[index].format(side = side, cut = value) for index, (side, value) in enumerate(zip(cut_side, cut_values))])

###Function that stores and return information for the configs that will be written

def base_config(parameter, nick_suffix = "", no_plot = False, weight_input = "1"):
	input_dir, format, www_nodate, cms, text 		= config_info[-2]
	category, estimationMethod, cut_type			= config_info[-1]
	x_expressions,x_bins,output				= parameter_info[parameter][:3]
	output = output + weight_name + category_name
	
	title 							= {"em": "e#mu", "et": "e#tau_{h}", "mt": "#mu#tau_{h}"}[channel]
	weights							= weight + "*" + categories + "*" + weight_input 
	www							= channel + "/"	

	base_values		= [input_dir, flavio_path, format,  www_nodate, www, x_expressions, x_bins, output, title, cms, text]
	samples_values		= [sample_list, channel, category, estimationMethod, cut_type, nick_suffix, no_plot, weights]

	print samples_values

	return base_values, samples_values	

def controlplot_config(parameter):
	x_label							= parameter_info[parameter][3]
	legend, lumis, energies, year, www			= config_info[0]
	
	return [x_label, legend, lumis, energies, year, www]


def sumofhists_config(sum_nicks, result_nicks):
	analysis_mod	=	"SumOfHistograms"
	
	return analysis_mod, sum_nicks, result_nicks

def efficiency_config(parameter, bkg_nicks, lower_cut = True):
	analysis_mod, markers, y_label, cut_modes, cut_nicks, whitelist 	=	 config_info[1][:6]	
	legend, lumis, energies, year, www						= config_info[1][6:]
	x_label										= parameter_info[parameter][3]
	
	sig_nicks		=	["z" + channel + "noplot"]

	return [x_label, legend, lumis, energies, year, www], [analysis_mod, bkg_nicks, markers, y_label, cut_modes, sig_nicks, cut_nicks, whitelist, lower_cut]

def shape_config(parameter):
	y_label, analysis_mod			= config_info[2][:2]
	legend, lumis, energies, year, www	= config_info[2][2:]
	x_label					= parameter_info[parameter][3]
	
	return [x_label, legend, lumis, energies, year, www], [y_label, analysis_mod]

def nminus1_config(parameter):
	x_label					= parameter_info[parameter][3]
	legend, lumis, energies, year, www	= config_info[4]
	
	return [x_label, legend, lumis, energies, year, www]

def ratio_config(numerator, denominator):
	ratio_numerator_nicks	=	numerator
	ratio_denominator_nicks =	denominator
	ratio_result_nicks 	=	["ratio1", "ratio2"]
	analysis_modules	=	"Ratio"
	markers			=	["E", "E2"]
	stacks			=	["ratio1", "ratio2"]
	y_subplot_lims		= 	[.5, 1.5]

	return [ratio_numerator_nicks, ratio_denominator_nicks, ratio_result_nicks, analysis_modules, markers, stacks, y_subplot_lims]

def cutflow_config(parameter):
	nicks 			=	sample_list + ["soverb"]
	files 			=	"cutflow_" + channel + ".root"
	markers			= 	["HIST" for background in sample_list] + ["LINE"]
	x_tick_labels	 	= 	[]
	stacks			=	["bkg" for background in sample_list] + ["soverb"]

	x_label					= parameter_info[parameter][3]
	sub_nicks, y_subplot_label		= config_info[5][:2]
	legend, lumis, energies, year, www	= config_info[5][2:]

	return [x_label, legend, lumis, energies, year, www], [sub_nicks, y_subplot_label, files, markers, nicks, x_tick_labels, stacks]

def limit_config(parameter):
	y_label, folders, y_expressions, markers, colors, marker_styles, line_widths, tree_draw_options, nicks, x_lims, y_lims, x_tick_labels				= config_info[6][:12]
	legend, lumis, energies, year, www																= config_info[6][12:]
	x_label																				= parameter_info[parameter][3]
	files 			= "limits.root"	

	return [x_label, legend, lumis, energies, year, www], [y_label, folders, y_expressions, markers, colors, marker_styles, line_widths, tree_draw_options, nicks, x_lims, y_lims, x_tick_labels, files]

def blind_config():
	analysis_modules = ["MaskHistograms"]	
	mask_nick = ["data", "ratio1"]
	mask_ref = "z" + channel
	mask_value = 100.0
	
	return [analysis_modules, mask_nick, mask_ref, mask_value]

	

###Analysis function using the specific plotting modules
def controlplot(config_list):
	for index, parameter in enumerate(x):
		if data:
			config = configmaster.ConfigMaster(*base_config(parameter))
			config.add_config_info(controlplot_config(parameter), 0)
			config.add_config_info(sumofhists_config([" ".join([nick for nick in sample_list[:-2]])], ["bkg_sum_noplot"]), 1)
			config.add_config_info(ratio_config(["data", "bkg_sum_noplot"], ["bkg_sum_noplot", "bkg_sum_noplot"]), 6)
			config.add_config_info(blind_config(), 8)

			
		else:
			config = configmaster.ConfigMaster(*base_config(parameter))
			config.add_config_info(controlplot_config(parameter), 0)
	
	
		config_list.append(config.return_config())
		config_list[index]["no_cache"] = True

		if signal:
			config_list[index]["weights"][-2 if data else -1] += "*(10)"
			config_list[index]["labels"][-2 if data else -1] = "Z #rightarrow " + {"em": "e#mu", "et": "e#tau", "mt": "#mu#tau"}[channel] + " (LFV) x 10"

	return config_list

def efficiencyplot(config_list):
	for parameter in x:
		config = configmaster.ConfigMaster(*base_config(parameter, nick_suffix = "noplot", no_plot = True))
		config.add_config_info(sumofhists_config(["zttnoplot zllnoplot ttjnoplot vvnoplot wjnoplot qcdnoplot"], ["bkg_sum"]), 1)
		config.add_config_info(efficiency_config(parameter, ["bkg_sum"])[0], 0)
		config.add_config_info(efficiency_config(parameter, ["bkg_sum"])[1], 2)
		config_list.append(config.return_config())
	
	return config_list


def shapeplot(config_list):
	for index, parameter in enumerate(x):
		config = configmaster.ConfigMaster(*base_config(parameter))
		config.add_config_info(shape_config(parameter)[0], 0)
		config.add_config_info(shape_config(parameter)[1], 3)
		config.pop(["stacks", "colors"])
		config_list.append(config.return_config())

		##Delete information not needed
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
			config.pop(["www", "www_nodate", "cms", "extra_text"])
			config.change_config_info(["filename", "plot_modules"], ["_" + channel, "ExportRoot"])
		
			##Create config in zero iteration to check on which side the cut should be applied
			if(index1 == 0):
				config2 = config.copy()
				config2.replace("select_lower_values", False)
				config2.change_config_info("filename", "_2")
		
			##Harry.py the MVP
			higgsplot.HiggsPlotter(list_of_config_dicts=[config.return_config()] if index1 != 0  else [config.return_config(), config2.return_config()], n_plots = 2 if index1==0 else 1)
			
			##Readout best cut value
			cut_file = ROOT.TFile.Open(flavio_path + "/" +  config.return_config()["filename"] + ".root")
			histogram = cut_file.Get("sOverSqrtSB")	
			cut_values[index2] = (histogram.GetXaxis().GetBinCenter(histogram.GetMaximumBin()))

			for filetype in [".json", ".root"]:
				os.remove(flavio_path + "/" +  config.return_config()["filename"] + filetype)
			
			##Choose which side to cut on in zero iteration
			if index1==0:
				cut_file2 = ROOT.TFile.Open(flavio_path + "/" +  config2.return_config()["filename"] + ".root")
				histogram2 = cut_file2.Get("sOverSqrtSB")	
				
				if histogram.GetMaximum() < histogram2.GetMaximum():
					cut_values[index2] = histogram2.GetXaxis().GetBinCenter(histogram2.GetMaximumBin())
					cut_side[index2] = ">"

				for filetype in [".json", ".root"]:
					os.remove(flavio_path + "/" +  config2.return_config()["filename"] + filetype)
		
		##print progress
		if index1 == 0:
			print "Cut sides which are choosen: {sides}".format(sides = cut_side)
		print "Cut values for iteration {index}: {values}".format(index = index1, values = cut_values)

	##Save data in cut.yaml
	cut_info 	= yaml.load(open(os.path.abspath(os.path.expandvars("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/python/lfv/cuts.yaml")), "r"))
	if cut_info == None:
		for category in [0 if weight == "(njetspt30==0)" else 1]:
			cut_info = {category: {channel: {}}}
			for (cut, side, parameter) in zip(cut_values, cut_side, x):
				cut_info[category][channel][parameter] = [cut, side]

	else:
		for category in [0 if weight == "(njetspt30==0)" else 1]:
			try:
				cut_info[category][channel] = {}
			except KeyError:
				cut_info[category] = {channel: {}}
			for (cut, side, parameter) in zip(cut_values, cut_side, x):
				cut_info[category][channel][parameter] = [cut, side]

	yaml.dump(cut_info, open(os.path.abspath(os.path.expandvars("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/python/lfv/cuts.yaml")), "w"), default_flow_style=False)
	
	sys.exit()

def nminus1plot(config_list):
	##Get information about cuts from parameter_info
	cut_strings = [parameter_info[param][4] for param in cut_info[0 if weight == "(njetspt30==0)" else 1][channel].keys()]
	cut_values, cut_side = [[entry[index] for entry in cut_info[0 if weight == "(njetspt30==0)" else 1][channel].values()] for index in [0,1]]


	for index1, parameter in enumerate(cut_info[0 if weight == "(njetspt30==0)" else 1][channel].keys()):
		##Construct weight for N-1 plot	
		weights = "*".join([cut_strings[index2].format(side = side, cut = value) for index2, (side, value) in enumerate(zip(cut_side, cut_values)) if index1 != index2])

		#Build config
		config = configmaster.ConfigMaster(*base_config(parameter, weight_input = weights))
		config.add_config_info(nminus1_config(parameter), 0)
		config.change_config_info("vertical_lines", [cut_values[index1]])

		if signal:
			config = config.return_config()
			config["stacks"][-1] = "sig"
			config["markers"][-1] = "LINE"
			config["weights"][-1] += "*(500)"
			config["labels"][-1] = "Z #rightarrow " + {"em": "e#mu", "et": "e#tau", "mt": "#mu#tau"}[channel] + " (LFV) x 500"

		config_list.append(config if signal else config.return_config())

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
	import array

	directory = os.path.abspath(os.path.expandvars("$CMSSW_BASE/src/FlavioOutput/Limits/{channel}".format(channel=channel)))

	if not x[0]==30:	

		old_limits = {
				"em":		7.3e-7,
				"et":		9.8e-6,
				"mt":		1.2e-5
		}	

		#for method in ["cut_based", "BDT_cut", "BDT"]:
		#	os.system("python HiggsAnalysis/KITHiggsToTauTau/scripts/FlavioLimits.py --channel {channel} --method {method}".format(channel=channel, method=method))
	
		root_file = "/limits.root"
		output = ROOT.TFile(directory + root_file, "RECREATE")


		for method in ["cut_based", "cut_BDT", "BDT"]:
			output.mkdir(method)
			output_tree = ROOT.TTree("limit", "tree with limit values for categories")	

			branch_names = [("two_sigma_down", "/F"), ("one_sigma_down", "/F"), ("limit_exp", "/F"), ("one_sigma_up", "/F"), ("two_sigma_up", "/F"), ("limit_obs", "/F"), ("limit_old", "/F"), ("categories", "/I")]
			branch_adresses = [array.array("f", [0]) for branch in branch_names[:-1]] + [array.array("i", [0])]
			branches = [output_tree.Branch(branch_name, branch_adress, branch_name + branch_type) for (branch_name, branch_type), branch_adress in zip(branch_names, branch_adresses)]


			for index2, category in enumerate(["OneJet", "ZeroJet", "combined"]):
				limit_file = ROOT.TFile.Open(directory + "/limit_{cat}_{method}.root".format(cat=category, method = method))
				tree = limit_file.Get("limit")

				for index, event in enumerate(tree):
					branch_adresses[index][0] = event.limit*old_limits[channel]
						
				if index2 == 2:
					branch_adresses[index+1][0] = old_limits[channel]					
				else:
					branch_adresses[index+1][0] = 0 
				
				branch_adresses[index+2][0] = index2


				output_tree.Fill()
				limit_file.Close()
				
			output.cd(method)
			output_tree.Write()
		output.Close()
		sys.exit(0)

	else:	
		for index, analysis in enumerate(["cut_based", "BDT", "cut_BDT"]):
			##Write config for limit plots
			config = configmaster.ConfigMaster(base_config(x[0])[0])
			config.add_config_info(limit_config(x[0])[0], 0)
			config.add_config_info(limit_config(x[0])[1], 7)
			config.replace(["directories", "folders", "filename", "y_lims"], [directory, [analysis + "/limit"], "Limit_" + analysis, {"em": [0.0, 2.5e-6], "et": [0., 2.5e-4], "mt": [0., 2.5e-4]}[channel]])

			config_list.append(config.return_config())
			config_list[index]["nicks"] = config_list[index]["nicks"][:-1]
			config_list[index]["y_expressions"] = config_list[index]["y_expressions"][:-1]		

	return config_list


def harry_do_your_job(config):
	higgsplot.HiggsPlotter(list_of_config_dicts=[config])


###Main Function

def main():
	###Call and get parser arguments
	args = parser()

	###Define global constants
	global_constants(args)

	##Define libary with all analysis modules of flavio
	Analysismodule_libary = {
				Analysismodule.control_plot:		controlplot,
				Analysismodule.effiency_plot:		efficiencyplot,
			 	Analysismodule.shape_plot:		shapeplot,
				Analysismodule.cut_optimization:	cutoptimization,
				Analysismodule.nminus1_plot:		nminus1plot,
				Analysismodule.cutflow_plot:		cutflowplot,
				Analysismodule.limit_plot:		limitplot
	}

	###Write config using your desired analysis function
	config_list = []
	config_list = Analysismodule_libary[args.analysis](config_list)

	###Call MVP harry.py to get your job done
	pool = Pool(cpu_count())

	for config in config_list:
		pool.apply_async(harry_do_your_job, args = (config,))

	pool.close()
	pool.join()

if __name__ == "__main__":
	main()
