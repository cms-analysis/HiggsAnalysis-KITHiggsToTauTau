#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

from multiprocessing import Pool,  cpu_count
import argparse
import copy
import os
import sys
import shutil
import yaml

import Artus.Utility.tools as tools
import Artus.HarryPlotter.utility.plotconfigs as plotconfigs

import HiggsAnalysis.KITHiggsToTauTau.plotting.higgsplot as higgsplot
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.samples_run2_2016 as samples
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.systematics_run2 as systematics
import HiggsAnalysis.KITHiggsToTauTau.datacards.lfvdatacards as lfvdatacards
import HiggsAnalysis.KITHiggsToTauTau.lfv.ConfigMaster as configmaster

def _call_command(command):
	log.debug(command)
	logger.subprocessCall(command, shell=True)

def harry_do_your_job(config):
	higgsplot.HiggsPlotter(list_of_config_dicts=[config], n_plots = 1)

if __name__ == "__main__":

	parser = argparse.ArgumentParser(description="Create ROOT inputs and datacards for LFV analysis.",
	                                 parents=[logger.loggingParser])
	parser.add_argument("-i", "--input-dir", default = "/net/scratch_cms3b/brunner/artus/AllSamples/merged/",
	                    help="Input directory.")
	parser.add_argument("-c", "--channel", nargs="+",
	                    help="Channel. This agument can be set multiple times. [Default: %(default)s]")
	parser.add_argument("-s", "--signal", nargs="+",
	                    help="Channel. This agument can be set multiple times. [Default: %(default)s]")
	parser.add_argument("-x", "--quantity", default="m_vis",
	                    help="Quantity. [Default: %(default)s]")
	parser.add_argument("--categories", nargs="+",
	                    default=["ZeroJet_LFV", "OneJet_LFV"],
	                    help="Categories per channel. This agument needs to be set as often as --channels. [Default: %(default)s]")
	parser.add_argument("-o", "--output-dir",
	                    default="$CMSSW_BASE/src/plots/LFV_datacards/",
	                    help="Output directory. [Default: %(default)s]")
	parser.add_argument("-f", "--n-plots", type=int, nargs=2, default=[None, None],
	                    help="Number of plots for datacard inputs (1st arg) and for postfit plots (2nd arg). [Default: all]")
	parser.add_argument("--shape-uncs", default= True, action="store_true",
						help="Do not include shape uncertainties. [Default: %(default)s]")
	parser.add_argument("--lnN-uncs", default= True, action="store_true",
						help="Do not include shape uncertainties. [Default: %(default)s]")
	parser.add_argument("--use-rateParam", action="store_true", default=False,
						help="Use rate parameter to estimate ZTT normalization from ZMM. [Default: %(default)s]")
	parser.add_argument("--use-asimov-dataset", action="store_true", default=True,
	                    help="Use s+b expectation as observation instead of real data. [Default: %(default)s]")
	parser.add_argument("--use-BDT-as-cut", action = "store_true", default = False, help = "Use BDT score as cut")
	parser.add_argument("--batch", action = "store_true", default = False, help = "Use BDT score as cut")


	args = parser.parse_args()
	logger.initLogger(args)
	args.output_dir = os.path.abspath(os.path.expandvars(args.output_dir))

	##Delete old datacards
	if os.path.exists(args.output_dir + "/datacards"):
		shutil.rmtree(args.output_dir + "/datacards")

	#Instances of classes needed for filling the config
	systematics_factory = systematics.SystematicsFactory()
	
	plot_configs = []
	output_files = []
	merged_output_files = []
	hadd_commands = []
	
	# Prepare name templates
	tmp_input_root_filename_template = "input/${ANALYSIS}_${CHANNEL}_${BIN}_${SYSTEMATIC}_${ERA}"
	input_root_filename_template = "input/${ANALYSIS}_${CHANNEL}_${BIN}_${ERA}.root"
	bkg_histogram_name_template = "${BIN}/${PROCESS}"
	sig_histogram_name_template = "${BIN}/${PROCESS}"
	bkg_syst_histogram_name_template = "${BIN}/${PROCESS}_${SYSTEMATIC}"
	sig_syst_histogram_name_template = "${BIN}/${PROCESS}_${SYSTEMATIC}"
	datacard_filename_templates =  [
			"datacards/individual/${BIN}/${ANALYSIS}_${CHANNEL}_${BINID}_${ERA}.txt",
			"datacards/channel/${CHANNEL}/${ANALYSIS}_${CHANNEL}_${ERA}.txt",
			"datacards/category/${BINID}/${ANALYSIS}_${BINID}_${ERA}.txt",
			"datacards/combined/${ANALYSIS}_${ERA}.txt",]
	output_root_filename_template = "datacards/common/${ANALYSIS}.input_${ERA}.root"

	##Dictionary for categories with list of [path of file with optimized cuts, weight for numbers of jets]
	categories = {
			"ZeroJet_LFV":	 [0, "(njetspt30==0)"],
			"OneJet_LFV":	 [1, "(njetspt30==1)"],
	}

	##Dictionary with control region with list of [process, weight]
	control_regions = {
			#"TT_CR_LFV":	["TT", "nbtag==0"]
	}

	#datacard initialization
	datacards = lfvdatacards.LFVDatacards(args.channel, args.signal, args.categories, control_regions, lnN_syst_enable = args.lnN_uncs, shape_syst_enable = args.shape_uncs, rate_param_enable = False)
	#datacards.cb.PrintAll()

	##Information about parameter and cuts for harry.py config
	cut_info 	= yaml.load(open(os.path.abspath(os.path.expandvars("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/python/lfv/cuts.yaml")), "r"))
	parameter_info  = yaml.load(open(os.path.abspath(os.path.expandvars("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/python/lfv/parameter.yaml")), "r"))

	#Loop over all channel/categories
	for channel in args.channel:
		list_of_samples_for_syst = datacards.get_samples_per_shape_systematic()
	
		for category in args.categories + control_regions.keys():
			tmp_output_files = []

			#Weight for the category saved in cut ini files
			if not "CR" in category and args.quantity == "m_vis":
				if not args.use_BDT_as_cut:
					cut_strings = [parameter_info[param][4] for param in cut_info[categories[category][0]][channel].keys()]
					cut_values, cut_side = [[entry[index] for entry in cut_info[categories[category][0]][channel].values()] for index in [0,1]]
					weight = "*".join([cut_strings[index].format(side = side, cut = value) for index, (side, value) in enumerate(zip(cut_side, cut_values))] + [categories[category][1]])
				
				else:
					weight = "BDT2_score > 0.0"

			##Weight if BDT score is used for stastical anaylsis
			elif args.quantity == "BDT3_score":
				weight = categories[category][1]

			##Weight for control region
			else:
				weight = control_regions[category][1]

			category = channel + "_" + category

			for shape_systematic in [shape for shape in datacards.cb.cp().syst_type(["shape"]).syst_name_set()] + ["nominal"]:
				nominal = (shape_systematic == "nominal")

				##Samples for control region
				if nominal and "CR" in category:
					samples = ["data"] + [datacards.configs.process2sample(control_regions[category[3:]][0])]

				##Sample for signal region
				else:
					samples = (["data"] if nominal else []) + [datacards.configs.process2sample(process) for process in list(list_of_samples_for_syst[shape_systematic])] + (["qcd"] if "W" in list_of_samples_for_syst[shape_systematic] and "QCD" not in list_of_samples_for_syst[shape_systematic] else []) + (["wj"] if "QCD" in list_of_samples_for_syst[shape_systematic] and "W" not in list_of_samples_for_syst[shape_systematic] else [])

				print samples


				for shift_up in ([True] if nominal else [True, False]):
					systematic = "nominal" if nominal else (shape_systematic + ("Up" if shift_up else "Down"))
					histogram_name_template = bkg_histogram_name_template if nominal else bkg_syst_histogram_name_template			
	
					##Define values to fill Harry Plotter config
					base_values = [
							[args.input_dir], 
							args.output_dir, 
							["png"],
							True,
							"",
							[args.quantity],
							["30,40,130"] if args.quantity == "m_vis" else ["20,0,0.2"], #Binning for m_vis or BDT_score
							tmp_input_root_filename_template.replace("$", "").format(ANALYSIS="LFV", CHANNEL = channel, BIN= category,SYSTEMATIC=systematic, ERA="13TeV"),		
							"",
							False,
							""
					]

					sample_values  = [
							samples,
							channel,
							None,
							"new",
							"lfv",
							"",
							False,
							weight,
					]

					datacard_values = [
							[histogram_name_template.replace("$", "").format(PROCESS=datacards.configs.sample2process(sample), CHANNEL = channel, BIN=category, SYSTEMATIC=systematic) for sample in samples],
							["ExportRoot"],
							"UPDATE"
					]

		
					##Fill config with ConfigMaster and SystematicFactory
					config = configmaster.ConfigMaster(base_values, sample_values)
					config.add_config_info(datacard_values, 4)
					config.pop(["www", "legend_markers", "cms", "extra_text", "title"])
					config = config.return_config()

					systematics_settings = systematics_factory.get(shape_systematic)(config)
					config = systematics_settings.get_config(shift=(0.0 if nominal else (1.0 if shift_up else -1.0)))				

					##Do specific config change
					config["labels"] = config["labels"][-1]
					plot_configs.append(config)

					##File list with tmp output files
					tmp_output_file = os.path.join(args.output_dir, tmp_input_root_filename_template.replace("$", "").format(ANALYSIS="LFV", CHANNEL = channel,BIN= category,SYSTEMATIC=systematic, ERA="13TeV") + ".root")	
					tmp_output_files.append(tmp_output_file)

			##File list with merged outputs
			output_file = os.path.join(args.output_dir, input_root_filename_template.replace("$", "").format(ANALYSIS="LFV", CHANNEL = channel, BIN= category, ERA="13TeV"))
			output_files.append(output_file)
			
			##Hadd command for merging the tmp output files
			hadd_commands.append("hadd -f {DST} {SRC} && rm {SRC}".format(DST=output_file, SRC=" ".join(tmp_output_files)))	

	# delete existing output files
	for output_file_iterator in tmp_output_files:
		if os.path.exists(output_file_iterator):
			os.remove(output_file_iterator)
	output_files = list(set(output_files))

	
	# create input histograms with HarryPlotter
	if not args.batch:
		pool = Pool(cpu_count())

		for config in plot_configs:
			pool.apply_async(harry_do_your_job, args = (config,))

		pool.close()
		pool.join()
		
	else:
		# create input histograms with HarryPlotter
		higgsplot.HiggsPlotter(list_of_config_dicts=plot_configs, n_processes= 1, n_plots=len(plot_configs), batch = "rwthcondor")

	tools.parallelize(_call_command, hadd_commands, n_processes=1)
	
	datacards.extract_shapes(os.path.join(args.output_dir, input_root_filename_template.replace("$", "")), bkg_histogram_name_template, sig_histogram_name_template, bkg_syst_histogram_name_template, sig_syst_histogram_name_template, update_systematics=True)

	"""
	datacards.add_bin_by_bin_uncertainties(
				processes=datacards.cb.cp().backgrounds().process_set(),
				add_threshold=0.05, merge_threshold=0.8, fix_norm=False

		)
	"""
	# use asimov dataset for s+b
	if args.use_asimov_dataset:
		datacards.replace_observation_by_asimov_dataset()

	#Writing datacards and produce libary for them
	datacards_cbs = {}
	for datacard_filename_template in datacard_filename_templates:
		datacards_cbs.update(datacards.write_datacards(datacard_filename_template.replace("{", "").replace("}", ""), output_root_filename_template.replace("{", "").replace("}", ""), args.output_dir))

	datacards_poi_ranges = {}
	for datacard, cb in datacards_cbs.iteritems():
		channels = cb.channel_set()
		categories = cb.bin_set()
		if len(channels) == 1:
			if len(categories) == 1:
				datacards_poi_ranges[datacard] = [0.0, 2.0]
				datacards_poi_ranges[datacard] = [0, 2.0]
			else:
				datacards_poi_ranges[datacard] = [0., 2.0]
		else:
			if len(categories) == 1:
				datacards_poi_ranges[datacard] = [0.0, 2.0]
			else:
				datacards_poi_ranges[datacard] = [0.0, 2.0]
	
	#write the datacards
	datacards_workspaces = datacards.text2workspace(datacards_cbs, n_processes=1)

	# Max. likelihood fit

	#datacards.combine(datacards_cbs, datacards_workspaces, datacards_poi_ranges, 1, "-M MaxLikelihoodFit "+datacards.stable_options+" -n \"\"")
	datacards.combine(datacards_cbs, datacards_workspaces, None, 1, "--expectSignal=1 -t -1 -M AsymptoticLimits -n \"\"")

	

