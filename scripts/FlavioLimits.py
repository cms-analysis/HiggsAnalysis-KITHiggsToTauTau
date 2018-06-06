import CombineHarvester.CombineTools.ch as ch
import os
import glob
import copy
import yaml
import argparse
from multiprocessing import Pool,  cpu_count

import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.samples_run2_2016 as samples
import HiggsAnalysis.KITHiggsToTauTau.plotting.higgsplot as higgsplot
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.systematics_libary as SystLib
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.systematics_run2 as systematics

##Argument parser
parser = argparse.ArgumentParser(description = "Script for calculating limits in LFV analysis", formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("--channel", action = "store", required = True, choices = ["em", "et", "mt"] , help = "Channel which should be analyzed")
parser.add_argument("--method", action = "store", required = True, choices = ["cut_based", "cut_BDT", "BDT"],  help = "Analysis method")

output_dir = os.environ["CMSSW_BASE"] + "/src/FlavioOutput/Limits/"
channel = parser.parse_args().channel
method = parser.parse_args().method

##Cleaning up
if not os.path.exists(os.environ["CMSSW_BASE"] + "/src/FlavioOutput/"):
	os.mkdir(os.environ["CMSSW_BASE"] + "/src/FlavioOutput/")
	os.mkdir(output_dir)

if not os.path.exists(output_dir):
	os.mkdir(output_dir)

if os.path.exists(output_dir + channel + "/input_{method}.root".format(method=method)):
	for f in glob.glob(output_dir + channel + "/*json"):
    		os.remove(f)

	for f in glob.glob(output_dir + channel + "/input_" + method + "*root"):
		os.remove(f)


##Harry plotter <-> Combine Harvester process names
data = {"data_obs": "data"}
signals = {"ZEM": "zem", "ZET": "zet", "ZMT": "zmt"}
backgrounds = {"ZTT" : "ztt", "VV" : "vv", "W" : "wj", "QCD" : "qcd"}
backgrounds.update({"TT": "ttj", "ZLL": "zll"} if channel == "em" else {"TTT" : "ttt", "TTJJ": "ttjj", "ZL":"zl", "ZJ" : "zj"})

#categories
categories = [(0, "ZeroJet"), (1, "OneJet")]

#control regions
controlregions = 

#Instance for extracting histograms
sample_settings = samples.Samples()	
config_list = []

##Combine harvester instance
cb = ch.CombineHarvester()

##weights
cut_info 	= yaml.load(open(os.environ["CMSSW_BASE"] + "/src/FlavioOutput/Configs/cuts.yaml", "r"))
parameter_info  = yaml.load(open(os.environ["CMSSW_BASE"] + "/src/FlavioOutput/Configs/parameter.yaml", "r"))

weights = []

for index, category in enumerate(["(njetspt30==0)", "(njetspt30==1)"]):
	cut_strings = [parameter_info[param][4] for param in cut_info[index][channel].keys()]
	cut_values, cut_side = [[entry[index2] for entry in cut_info[index][channel].values()] for index2 in [0,1]]
	
	weights.append({"cut_based":	"*".join([cut_strings[index2].format(side = side, cut = value) for index2, (side, value) in enumerate(zip(cut_side, cut_values))] + [category]),
			"cut_BDT": 	"(BDT_forcut_score>0.0)*" + category,
			"BDT":		category
	})

print weights[1][method]
	
##Fill combine harvester with categories/processes
for category in categories:
	##Add data/signal
	cb.AddObservations(["*"], ["lfv"], ["13TeV"], [channel], [category])
	cb.AddProcesses(["*"], ["lfv"], ["13TeV"], [channel], ["Z" + channel.upper()], [category], True)	

	##Config for each category
	config = sample_settings.get_config([getattr(samples.Samples, sample) for sample in data.values() + ["z"+channel] + backgrounds.values()], channel, None, estimationMethod = "new", weight = weights[category[0]][method])
	config.pop("legend_markers")
	config += {"filename": "input_" + method + "_nominal_" + category[1], "plot_modules": ["ExportRoot"], "file_mode": "UPDATE", "directories": os.environ["MCPATH"], "x_expressions": "BDT_score" if method == "BDT" else "m_vis", "x_bins": ["30,0.0,0.5"] if method == "BDT" else ["30,30,140"], "output_dir": output_dir + channel}
	config["labels"] = [category[1] + "/" + process for process in data.keys() + ["Z" + channel.upper()] + backgrounds.keys()]
	config_list.append(config)

	for process in backgrounds.keys():
		##Add background
		cb.AddProcesses(["*"], ["lfv"], ["13TeV"], [channel], [process], [category], False)

##Fill combine harvester with systematics
systematics_list = SystLib.SystematicLibary()
systematics_factory = systematics.SystematicsFactory()

for (systematic, process, category) in systematics_list.get_LFV_systs(channel, lnN = True) + systematics_list.get_LFV_systs(channel, shape = True):
	cb.cp().channel([channel]).process(process).AddSyst(cb, *systematic)
	
	if "W" in process and "QCD" not in process:
		process.append("QCD")

	if "QCD" in process and "W" not in process:
		process.append("W")
	
	if systematic[1] == "shape":
		##Config for each systematic shift:
		for category in categories:
			for shift in ["Down", "Up"]:
				config = sample_settings.get_config([getattr(samples.Samples, dict(signals, **backgrounds)[sample]) for sample in process], channel, None, estimationMethod = "new", weight = weights[category[0]][method])
				config.pop("legend_markers")
				config += {"filename": "input_" + method + "_" + systematic[0].replace("$ERA", "13TeV").replace("$CHANNEL", channel) + shift + "_" + category[1], "plot_modules": ["ExportRoot"], "file_mode": "UPDATE", "directories": os.environ["MCPATH"], "x_expressions": "BDT_score" if method == "BDT" else "m_vis", "x_bins": ["30,0.0,0.5"] if method == "BDT" else ["30,30,140"], "output_dir": output_dir + channel}
				config["labels"] = [category[1] + "/" + proc + "_" + systematic[0].replace("$ERA", "13TeV").replace("$CHANNEL", channel) + shift for proc in process]
				systematics_settings = systematics_factory.get(systematic[0].replace("$ERA", "13TeV").replace("$CHANNEL", channel))(config)
				config = systematics_settings.get_config(1 if shift == "Up" else -1)			
				config_list.append(config)


def harry_do_your_job(config):
	higgsplot.HiggsPlotter(list_of_config_dicts=[config])


pool = Pool(cpu_count())
for config in config_list:
	pool.apply_async(harry_do_your_job, args = (config,))

pool.close()
pool.join()

os.system("hadd {target}.root {root_files}*.root".format(target=output_dir + channel +"/input_" + method, root_files = output_dir + channel +"/input_" + method))

##Fill combine harvester with the shapes which were extracted before from harry.py
cb.cp().backgrounds().ExtractShapes(output_dir + channel +"/input_" + method + ".root", "$BIN/$PROCESS", "$BIN/$PROCESS_$SYSTEMATIC");
cb.cp().signals().ExtractShapes(output_dir + channel +"/input_" + method + ".root", "$BIN/$PROCESS", "$BIN/$PROCESS_$SYSTEMATIC");


#Write datacard and call combine
cb.WriteDatacard(output_dir + channel + "/combined_" + method + ".txt", output_dir + channel + "/combined_datacard_" + method + ".root")
os.system("combine -m 0 -M AsymptoticLimits {datacard}.txt".format(datacard = output_dir + channel + "/" + "combined" + "_" + method))
os.system("combine -m 0 -M FitDiagnostics {datacard}.txt".format(datacard = output_dir + channel + "/" + "combined" + "_" + method))
os.system("PostFitShapes -d {datacard}.txt -o {output}.root -f fitDiagnostics.root:fit_s --postfit".format(datacard = output_dir + channel + "/" + "combined" + "_" + method, output= output_dir + channel + "/" + "postfit_" + method))
os.system("mv higgsCombineTest.AsymptoticLimits.mH0.root {filename}.root".format(filename = output_dir + channel + "/" + "limit_combined" + "_" + method))


for category in categories:
	cb_copy = cb.cp()
	cb_copy.FilterAll(lambda obj: obj.bin() != category[1])
	cb_copy.WriteDatacard(output_dir + channel + "/" + category[1] + "_" + method + ".txt", output_dir + channel + "/" + category[1] + "_datacard_" + method + ".root")

	os.system("combine -m 0 -M AsymptoticLimits {datacard}.txt -t -1".format(datacard = output_dir + channel + "/" + category[1] + "_" + method))
	#os.system("text2workspace.py -m 0 {datacard}.txt".format(datacard = output_dir + channel + "/" + category[1] + "_" + method))
	#os.system("combineTool.py -M Impacts -d {workspace}.root -m 0 --doInitialFit --robustFit 1".format(workspace = output_dir + channel + "/" + category[1] + "_" + method))
	#os.system("combineTool.py -M Impacts -d {workspace}.root -m 0 --robustFit 1 --doFits --parallel 4".format(workspace = output_dir + channel + "/" + category[1] + "_" + method))
	#os.system("combineTool.py -M Impacts -d {workspace}.root -m 0 --robustFit 1 -o impacts.json".format(workspace = output_dir + channel + "/" + category[1] + "_" + method))
	#os.system("plotImpacts.py -i impacts.json -o {output}".format(output= "pullplot_" + category[1] + "_" + method))
	os.system("mv higgsCombineTest.AsymptoticLimits.mH0.root {filename}.root".format(filename = output_dir + channel + "/" + "limit_" + category[1] + "_" + method))
	#os.system("mv pullplot*pdf {output}".format(output=output_dir + channel))
	

##Plot postfit shapes
config_list = []
for category in categories:
	for shape in ["_prefit", "_postfit"]:
		config = {	"files": output_dir + channel + "/" + "postfit_" + method + ".root", "folders": category[1] + shape, 
				"x_expressions": sorted(backgrounds.keys(), reverse=True) + ["TotalBkg"] + data.keys() + ["Z" + channel.upper()], 
				"stacks": ["bkg" for bkg in backgrounds.keys()] +  ["unc", "data", "sig", "ratio1", "ratio2"], 
				"markers": ["HIST" for hist in backgrounds.keys()] + ["E2", "E", "LINE", "E", "E2"], "formats": ["png", "pdf"], 
				"nicks": sorted(backgrounds.values(), reverse=True) + ["Uncertainty"] + data.values() + ["z" + channel], 
				"colors": sorted(backgrounds.values(), reverse=True) + ["kBlack"] + data.values() + ["z" + channel, "kBlack", "kBlack"], 
				"legend": [0.65, 0.5, 0.95, 0.85], "y_subplot_lims": [0.5, 1.5],
				"analysis_modules": ["Ratio", "MaskHistograms"],
				"mask_histogram_nicks":	["data", "ratio1"], "mask_above_reference_nick": "z" + channel, "mask_above_reference_value": 50 if category[0] == 0 else 10,
				"ratio_denominator_nicks": ["Uncertainty", "Uncertainty"], "ratio_numerator_nicks": ["data", "Uncertainty"], "ratio_result_nicks": ["ratio1", "ratio2"], 
				"x_label": "BDT score" if method == "BDT" else "m_{vis}", 
				"filename": method + "_" + category[1] + shape,
				"lumis": [35.87], "energies": [13], "year": "2016",
				"scale_factors": ["1" for proc in backgrounds.keys() + data.keys()] + ["1", "10"],
				"title": {"em": "e#mu", "et": "e#tau", "mt": "#mu#tau"}[channel],
				"www": channel + "/Limits", "www_nodate": True,
		}
		config_list.append(config)

higgsplot.HiggsPlotter(list_of_config_dicts=config_list)

##Cleaning up again
for f in glob.glob(output_dir + channel + "/*json"):
    	os.remove(f)

for f in glob.glob(output_dir + channel + "/input_" + method + "_*root"):
	os.remove(f)

for f in glob.glob("*json"):
    	os.remove(f)

for f in glob.glob("*root"):
	os.remove(f)

