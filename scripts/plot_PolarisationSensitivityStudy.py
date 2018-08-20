import argparse
import copy
import os
import sys
import re
import glob
from types import *
from subprocess import call


import ROOT

from CombineHarvester.ZTTPOL2016.zttpol2016_functions import *

#Colors
HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ MAIN ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~:
if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Create ROOT inputs and datacards for ZTT polarisation analysis.")

	parser.add_argument("-i", "--input-dir", required=False,
						help="Input directory of the Sensitivity study.")
	parser.add_argument("--channel", action="store_true", default = False,
						help = "Plot sensitivities per channel")
	parser.add_argument("--combination", action="store_true", default = False,
						help = "Plot sensitivities per combination")
	parser.add_argument("--binning", action="store_true", default = False,
						help = "Use for binning study")

	args = parser.parse_args()

#Get sensitivities from files
polarisation_values_combined, polarisation_values_individual, polarisation_values_channel = find_combination(args.input_dir)
	
colors = {'combined': 'kBlack', 'et': 'kGreen', 'tt':'kBlue', 'em':'kMagenta', 'mt':'kRed'}

if args.channel == True:
	print OKBLUE + "channel_dicts: " + ENDC, channel_dicts
	
	channel_dicts = {'em': {'Mvis':{},'Omega':{}},'mt': {'Mvis':{},'Omega':{}},'et': {'Mvis':{},'Omega':{}},'tt': {'Mvis':{},'Omega':{}}}
	for index, category in enumerate(sorted(polarisation_values_combined.keys())):
		channel_dicts[category.split("_")[0]][category.split("_")[-1]].update({category: [polarisation_values_combined[category][0], polarisation_values_combined[category][1], polarisation_values_combined[category][2]]})

	for channel in channel_dicts.keys():
		for variable in channel_dicts[channel].keys():
			x_values, ticks, y_values, y_errors_down, y_errors_up = zip(*[(index, category, polarisation_values_combined[category][0], polarisation_values_combined[category][1], polarisation_values_combined[category][2]) for index, category in enumerate(sorted(channel_dicts[channel][variable].keys() ))])
			command = "higgsplot.py --input-modules InputInteractive -m P -x \"{x_values}\" -y \"{y_values}\" --y-errors \"{y_errors_down}\" --y-errors-up \"{y_errors_up}\" --x-ticks \"{x_values}\" --x-tick-labels \"{ticks}\" --x-lims {min} {max} --y-lims {ymin} {ymax} --www SensitivityStudy/PerChannel --y-label 'Average Polarisation' --x-label '' -C {colors} --filename {filename}".format(x_values='" "'.join([str(x) for x in x_values]), y_values='" "'.join([str(y) for y in y_values]), y_errors_down='" "'.join([str(y) for y in y_errors_down]), y_errors_up='" "'.join([str(y) for y in y_errors_up]), ticks='" "'.join(ticks), min=min(x_values)-0.5, max=max(x_values)+0.5, filename = channel +"_"+ variable, ymin = min(y_values)-0.3, ymax = max(y_values)+0.3, colors = " ".join([colors[x.split("_")[0]] for x in ticks]))
			print OKGREEN + "executing command: " + ENDC, command
			os.system(command)
			
if args.combination == True:	
	print OKBLUE + "variable dicts: " + ENDC, variable_dicts

	variable_dicts = {'combined':{'Mvis':{}, 'Omega':{}},'single':{'Mvis':{}, 'Omega':{}},'inclusive':{'Mvis':{}, 'Omega':{}}}
	for index, category in enumerate(sorted(polarisation_values_combined.keys())):
		if category.split("_").count('combined') >= 1:
			variable_dicts['combined'][category.split("_")[-1]].update({category: [polarisation_values_combined[category][0], polarisation_values_combined[category][1], polarisation_values_combined[category][2]]})
		elif category.split("_").count('inclusive') >= 1:
			variable_dicts['inclusive'][category.split("_")[-1]].update({category: [polarisation_values_combined[category][0], polarisation_values_combined[category][1], polarisation_values_combined[category][2]]})
		else :
			variable_dicts['single'][category.split("_")[-1]].update({category: [polarisation_values_combined[category][0], polarisation_values_combined[category][1], polarisation_values_combined[category][2]]})

	
	for combination in variable_dicts.keys():
		for variable in variable_dicts[combination].keys():
			if len(variable_dicts[combination][variable].keys()) > 0:
				x_values, ticks, y_values, y_errors_down, y_errors_up = zip(*[(index, "_".join(category.split("_")[:-1]), polarisation_values_combined[category][0], polarisation_values_combined[category][1], polarisation_values_combined[category][2]) for index, category in enumerate(sorted(variable_dicts[combination][variable].keys() ))])
				command = "higgsplot.py --input-modules InputInteractive -m P -x \"{x_values}\" -y \"{y_values}\" --y-errors \"{y_errors_down}\" --y-errors-up \"{y_errors_up}\" --x-ticks \"{x_values}\" --x-tick-labels \"{ticks}\" --x-lims {min} {max} --y-lims {ymin} {ymax} --www SensitivityStudy/PerCombination --y-label 'Average Polarisation' --x-label '' -C {colors} --filename {filename}".format(x_values='" "'.join([str(x) for x in x_values]), y_values='" "'.join([str(y) for y in y_values]), y_errors_down='" "'.join([str(y) for y in y_errors_down]), y_errors_up='" "'.join([str(y) for y in y_errors_up]), ticks='" "'.join(ticks), min=min(x_values)-0.5, max=max(x_values)+0.5, filename = combination +"_"+ variable, ymin = min(y_values)-0.3, ymax = max(y_values)+0.3, colors = " ".join([colors[x.split("_")[0]] for x in ticks]))
				print OKGREEN + "executing command: " + ENDC, command
				os.system(command)

if args.binning == True:
	
	binning_dicts = {'em':{},'et':{},'mt':{},'tt':{}}
	for index, channel in enumerate(sorted(polarisation_values_channel.keys())):
		for binning in polarisation_values_channel[channel].keys(): 
			binning_dicts[channel].update({binning:[polarisation_values_channel[channel][binning][0],polarisation_values_channel[channel][binning][1],polarisation_values_channel[channel][binning][2]]})
	
	print OKBLUE, binning_dicts, ENDC
	
	for channel in binning_dicts.keys(): 
		print WARNING, channel, ENDC
		x_values, ticks, y_values, y_errors_down, y_errors_up = zip(*[(index, "".join(binning.split("_")[-1]), polarisation_values_channel[channel][binning][0], polarisation_values_channel[channel][binning][1], polarisation_values_channel[channel][binning][2]) for index, binning in enumerate(sorted(binning_dicts[channel].keys() ))])
		command = "higgsplot.py --input-modules InputInteractive -m P -x \"{x_values}\" -y \"{y_values}\" --y-errors \"{y_errors_down}\" --y-errors-up \"{y_errors_up}\" --x-ticks \"{x_values}\" --x-tick-labels \"{ticks}\" --x-lims {min} {max} --y-lims {ymin} {ymax} --www BinningStudy --y-label 'Average Polarisation' --x-label '' --filename {filename}".format(x_values='" "'.join([str(x) for x in x_values]), y_values='" "'.join([str(y) for y in y_values]), y_errors_down='" "'.join([str(y) for y in y_errors_down]), y_errors_up='" "'.join([str(y) for y in y_errors_up]), ticks='" "'.join(ticks), min=min(x_values)-0.5, max=max(x_values)+0.5, filename = "binning_"+channel, ymin = min(y_values)-max(y_errors_down)-0.01, ymax = max(y_values)+max(y_errors_down)+0.01)
		print OKGREEN + "executing command: " + ENDC, command
		os.system(command)
