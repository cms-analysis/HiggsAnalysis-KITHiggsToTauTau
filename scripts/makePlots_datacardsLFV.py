#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import argparse
import copy
import os
import sys
import pprint

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

if __name__ == "__main__":

	parser = argparse.ArgumentParser(description="Create ROOT inputs and datacards for LFV analysis.",
	                                 parents=[logger.loggingParser])
	parser.add_argument("-i", "--input-dir", required=True,
	                    help="Input directory.")
	parser.add_argument("-c", "--channel", action="append",
	                    default=["et"],
	                    help="Channel. This agument can be set multiple times. [Default: %(default)s]")
	parser.add_argument("-s", "--signal", action="append",
	                    default=["zet"],
	                    help="Channel. This agument can be set multiple times. [Default: %(default)s]")
	parser.add_argument("-x", "--quantity", default="m_vis",
	                    help="Quantity. [Default: %(default)s]")
	parser.add_argument("--categories", nargs="+", action = "append",
	                    default=["LFVZeroJet", "LFVJet"],
	                    help="Categories per channel. This agument needs to be set as often as --channels. [Default: %(default)s]")
	parser.add_argument("-o", "--output-dir",
	                    default="$CMSSW_BASE/src/plots/LFV_datacards/",
	                    help="Output directory. [Default: %(default)s]")
	parser.add_argument("-f", "--n-plots", type=int, nargs=2, default=[None, None],
	                    help="Number of plots for datacard inputs (1st arg) and for postfit plots (2nd arg). [Default: all]")
	parser.add_argument("--shape-uncs", default= False, action="store_true",
						help="Do not include shape uncertainties. [Default: %(default)s]")
	parser.add_argument("--lnN-uncs", default= False, action="store_true",
						help="Do not include shape uncertainties. [Default: %(default)s]")
	parser.add_argument("--use-rateParam", action="store_true", default=False,
						help="Use rate parameter to estimate ZTT normalization from ZMM. [Default: %(default)s]")
	parser.add_argument("--use-asimov-dataset", action="store_true", default=False,
	                    help="Use s+b expectation as observation instead of real data. [Default: %(default)s]")


	args = parser.parse_args()
	args.output_dir = os.path.abspath(os.path.expandvars(args.output_dir))

	# initialisations for plotting
	systematics_factory = systematics.SystematicsFactory()
	
	plot_configs = []
	output_files = []
	merged_output_files = []
	hadd_commands = []

	#Set up informations if not default values are used
	if args.signal != parser.get_default("signal"):
		args.signal = args.signal[len(parser.get_default("signal")):]

	if args.channel != parser.get_default("channel"):
		args.channel = args.channel[len(parser.get_default("channel")):]

	if args.categories != parser.get_default("categories"):
		args.categories = args.categories[1:]

	#datacard initialization
	datacards = lfvdatacards.LFVDatacards(channel_list = args.channel, signal_list=args.signal, category_list = args.categories, lnN_syst_enable = args.lnN_uncs, shape_syst_enable = args.shape_uncs) 
	
	# Prepare name templates
	tmp_input_root_filename_template = "input/${ANALYSIS}_${CHANNEL}_${BIN}_${SYSTEMATIC}_${ERA}"
	input_root_filename_template = "input/${ANALYSIS}_${CHANNEL}_${BIN}_${ERA}.root"
	bkg_histogram_name_template = "${BIN}/${PROCESS}"
	sig_histogram_name_template = "${BIN}/${PROCESS}"
	bkg_syst_histogram_name_template = "${CHANNEL}_${BIN}/${PROCESS}_${SYSTEMATIC}"
	sig_syst_histogram_name_template = "${CHANNEL}_${BIN}/${PROCESS}_${SYSTEMATIC}"
	datacard_filename_templates =  [
			"datacards/individual/${BIN}/${ANALYSIS}_${CHANNEL}_${BINID}_${ERA}.txt",
			"datacards/channel/${CHANNEL}/${ANALYSIS}_${CHANNEL}_${ERA}.txt",
			"datacards/category/${BINID}/${ANALYSIS}_${BINID}_${ERA}.txt",
			"datacards/combined/${ANALYSIS}_${ERA}.txt",]
	output_root_filename_template = "datacards/common/${ANALYSIS}.input_${ERA}.root"

	#Loop over all channel/categories
	for channel in args.channel:
		list_of_samples = datacards.cb.process_set()

		for category in [args.categories[0]]:
			tmp_output_files = []
			category = channel + "_" + category
			
			for shape_systematic in ["nominal"] + [shape for shape in datacards.cb.cp().syst_type(["shape"]).syst_name_set()]:
				nominal = (shape_systematic == "nominal")
				list_of_samples = (["data"] if nominal else []) + [datacards.configs.process2sample(process) for process in list_of_samples]

				for shift_up in ([True] if nominal else [True, False]):
					systematic = "nominal" if nominal else (shape_systematic + ("Up" if shift_up else "Down"))
					histogram_name_template = bkg_histogram_name_template if nominal else bkg_syst_histogram_name_template				
	
					##Define values to fill Harry Plotter config
					base_values = [
							[args.input_dir], 
							args.output_dir, 
							tmp_input_root_filename_template.replace("$", "").format(ANALYSIS="LFV", CHANNEL = channel, BIN= category,SYSTEMATIC=systematic, ERA="13TeV"),
							["png"],
							"",
							True,
							[args.quantity],
							["25,0,200"]
					]

					sample_values  = [
							list_of_samples,
							channel,
							"catLFV13TeV_" + category,
							False,
							"",	
							"1"
					]
	
					datacard_values = [
							[histogram_name_template.replace("$", "").format(PROCESS=datacards.configs.sample2process(sample), CHANNEL = channel, BIN=category, SYSTEMATIC=systematic) for sample in list_of_samples],
							["ExportRoot"],
							"UPDATE"
					]
			
		
				##Fill config with ConfigMaster and SystematicFactory
				config = configmaster.ConfigMaster(base_values, sample_values)
				config.add_config_info(datacard_values, 4)
				config = config.return_config()

				systematics_settings = systematics_factory.get(shape_systematic)(config)
				config = systematics_settings.get_config(shift=(0.0 if nominal else (1.0 if shift_up else -1.0)))				

				##Delete options not needed
				config.pop("www")
				config.pop("legend_markers")
				config["labels"] = config["labels"][-1]

				plot_configs.append(config)

				##File list with tmp output files
				tmp_output_file = os.path.join(args.output_dir, tmp_input_root_filename_template.replace("$", "").format(ANALYSIS="LFV", CHANNEL = channel,BIN= category,SYSTEMATIC=systematic, ERA="13TeV") + ".root")
				tmp_output_files.append(tmp_output_file)

		##File list with merged outputs
		output_file = os.path.join(args.output_dir, input_root_filename_template.replace("$", "").format(ANALYSIS="LFV", CHANNEL = channel, BIN= category, ERA="13TeV"))
		merged_output_files.append(output_file)
		output_files.append(output_file)

		##Hadd command for merging the tmp output files
		hadd_commands.append("hadd -f {DST} {SRC} && rm {SRC}".format(DST=output_file, SRC=" ".join(tmp_output_files)))
	

	# delete existing output files
	for output_file_iterator in tmp_output_files:
		if os.path.exists(output_file_iterator):
			os.remove(output_file_iterator)
	output_files = list(set(output_files))

	#pprint.pprint(plot_configs[0])

	# create input histograms with HarryPlotter
	higgsplot.HiggsPlotter(list_of_config_dicts=plot_configs, n_processes= 1, n_plots=args.n_plots[0])
	if args.n_plots[0] != 0:
		tools.parallelize(_call_command, hadd_commands, n_processes=1)

	
	datacards.extract_shapes(os.path.join(args.output_dir, input_root_filename_template.replace("$", "")), bkg_histogram_name_template, sig_histogram_name_template, bkg_syst_histogram_name_template, sig_syst_histogram_name_template, update_systematics=True)

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
	datacards.combine(datacards_cbs, datacards_workspaces, datacards_poi_ranges, 1, "-M MaxLikelihoodFit "+datacards.stable_options+" -n \"\"")
	datacards.combine(datacards_cbs, datacards_workspaces, None, 1, "--expectSignal=1 -t -1 -M Asymptotic -n \"\"")

	"""datacards_postfit_shapes = datacards.postfit_shapes_fromworkspace(datacards_cbs, datacards_workspaces, False, args.n_processes, "--sampling" + (" --print" if args.n_processes <= 1 else ""))
	datacards.pull_plots(datacards_postfit_shapes, s_fit_only=False, plotting_args={"fit_poi" : ["x"], "formats" : ["pdf", "png"]}, n_processes=args.n_processes)
	datacards.print_pulls(datacards_cbs, args.n_processes, "-A -p {POI}".format(POI="x") )"""



	

