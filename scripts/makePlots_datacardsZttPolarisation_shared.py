#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

import argparse
import copy
import os
import sys
import re
import glob
from types import *

import ROOT

import CombineHarvester.CombineTools.ch as ch
import CombineHarvester.ZTTPOL2016.zttpol2016_datacards as zttdatacards

import CombineHarvester.ZTTPOL2016.tools as tools
from CombineHarvester.ZTTPOL2016.tools import _call_command

from CombineHarvester.ZTTPOL2016.zttpol2016_functions import *

import Artus.Utility.tools as tools
import Artus.Utility.jsonTools as jsonTools
import Artus.HarryPlotter.utility.plotconfigs as plotconfigs
import Artus.HarryPlotter
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import HiggsAnalysis.KITHiggsToTauTau.plotting.higgsplot as higgsplot
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.binnings as binnings
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.systematics_run2 as systematics
import HiggsAnalysis.KITHiggsToTauTau.datacards.datacardconfigs as datacardconfigs
import HiggsAnalysis.KITHiggsToTauTau.datacards.zttpolarisationdatacards as zttpolarisationdatacards

import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.samples_run2_2016 as samples


#Colors
HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

def create_input_root_files(datacards, args):
    ''' Configuring Harry plotter according to the samples and creating input root files according to the args.'''
    plot_configs = []
    output_files = []
    merged_output_files = []
    hadd_commands = []

    sample_settings = samples.Samples()
    binnings_settings = binnings.BinningsDict()
    systematics_factory = systematics.SystematicsFactory()

    for index, (channel, categories) in enumerate(zip(args.channel, args.categories)):

        for category in categories:
            datacards_per_channel_category = zttpolarisationdatacards.ZttPolarisationDatacards(cb=datacards.cb.cp().channel([channel]).bin([category]))
                        
            higgs_masses = [mass for mass in datacards_per_channel_category.cb.mass_set() if mass != "*"]

            output_file = os.path.join(args.output_dir,"input/{ANALYSIS}_{CHANNEL}_{BIN}_{ERA}.root".format(
                    ANALYSIS="ztt",
                    CHANNEL=channel,
                    BIN=category,
                    ERA="13TeV"
            ))
            output_files.append(output_file)
            tmp_output_files = []

            for shape_systematic, list_of_samples in datacards_per_channel_category.get_samples_per_shape_systematic().iteritems():
                nominal = (shape_systematic == "nominal")
                list_of_samples = [datacards.configs.process2sample(process) for process in list_of_samples]
                asimov_nicks = []
                if args.use_asimov_dataset:
                    asimov_nicks = [nick.replace("zttpospol", "zttpospol_noplot").replace("zttnegpol", "zttnegpol_noplot") for nick in list_of_samples]
                    if "data" in asimov_nicks:
                        asimov_nicks.remove("data")

                for shift_up in ([True] if nominal else [True, False]):
                    systematic = "nominal" if nominal else (shape_systematic + ("Up" if shift_up else "Down"))

                    log.debug("Create inputs for (samples, systematic) = ([\"{samples}\"], {systematic}), (channel, category) = ({channel}, {category}).".format(
                            samples="\", \"".join(list_of_samples),
                            channel=channel,
                            category=category,
                            systematic=systematic
                    ))

                    # prepare plotting configs for retrieving the input histograms
                    config = sample_settings.get_config(
                            samples=[getattr(samples.Samples, sample) for sample in list_of_samples],
                            channel=channel,
                            category="catZttPol13TeV_"+category,
                            weight=args.weight,
                            lumi = args.lumi * 1000,
                            higgs_masses=higgs_masses,
                            estimationMethod="new",
                            polarisation_bias_correction=True,
                            cut_type="low_mvis_smhtt2016",
                            no_ewk_samples = args.no_ewk_samples,
                            no_ewkz_as_dy = True,
                            asimov_nicks = asimov_nicks
                    )

                    systematics_settings = systematics_factory.get(shape_systematic)(config)
                    # TODO: evaluate shift from datacards_per_channel_category.cb
                    config = systematics_settings.get_config(shift=(0.0 if nominal else (1.0 if shift_up else -1.0)))

                    #config["qcd_subtract_shape"] =[args.qcd_subtract_shapes]

                    x_expression = args.quantity if args.quantity else ("testZttPol13TeV_"+category)
                    config["x_expressions"] = [("0" if (("gen_zttpospol" in nick) or ("gen_zttnegpol" in nick)) else x_expression) for nick in config["nicks"]]

                    binnings_key = "binningZttPol13TeV_"+category+(("_"+args.quantity) if args.quantity else "")
                    if binnings_key in binnings_settings.binnings_dict:
                        config["x_bins"] = [("1,-1,1" if (("gen_zttpospol" in nick) or ("gen_zttnegpol" in nick)) else binnings_key) for nick in config["nicks"]]

                    config["directories"] = [args.input_dir]

                    histogram_name_template = "${BIN}/${PROCESS}" if nominal else "${BIN}/${PROCESS}_${SYSTEMATIC}"
                    config["labels"] = [histogram_name_template.replace("$", "").format(
                            PROCESS=datacards.configs.sample2process(sample.replace("asimov", "data")),
                            BIN=category,
                            SYSTEMATIC=systematic
                    ) for sample in config["labels"]]

                    tmp_output_file = os.path.join(args.output_dir, "input/{ANALYSIS}_{CHANNEL}_{BIN}_{SYSTEMATIC}_{ERA}.root".format(
                            ANALYSIS="ztt",
                            CHANNEL=channel,
                            BIN=category,
                            SYSTEMATIC=systematic,
                            ERA="13TeV"
                    ))
                    tmp_output_files.append(tmp_output_file)
                    config["output_dir"] = os.path.dirname(tmp_output_file)
                    config["filename"] = os.path.splitext(os.path.basename(tmp_output_file))[0]

                    config["plot_modules"] = ["ExportRoot"]
                    config["file_mode"] = "UPDATE"

                    if "legend_markers" in config:
                        config.pop("legend_markers")
                        
                    plot_configs.append(config)

            hadd_commands.append("hadd -f {DST} {SRC} && rm {SRC}".format(
                    DST=output_file,
                    SRC=" ".join(tmp_output_files)
            ))
                
    tmp_output_files = list(set([os.path.join(config["output_dir"], config["filename"]+".root") for config in plot_configs[:args.n_plots[0]]]))
    for output_file in tmp_output_files:
        if os.path.exists(output_file):
            os.remove(output_file)
            log.debug("Removed file \""+output_file+"\" before it is recreated again.")
    output_files = list(set(output_files))

    higgsplot.HiggsPlotter(list_of_config_dicts=plot_configs, list_of_args_strings=[args.args], n_processes=args.n_processes, n_plots=args.n_plots[0], batch=args.batch)
    
    if args.n_plots[0] != 0:
        tools.parallelize(_call_command, hadd_commands, n_processes=args.n_processes)

    debug_plot_configs = []
    for output_file in (output_files):
        debug_plot_configs.extend(plotconfigs.PlotConfigs().all_histograms(output_file, plot_config_template={"markers":["E"], "colors":["#FF0000"]}))
    if args.www:
        for debug_plot_config in debug_plot_configs:
            debug_plot_config["www"] = debug_plot_config["output_dir"].replace(args.output_dir, args.www)
    higgsplot.HiggsPlotter(list_of_config_dicts=debug_plot_configs, list_of_args_strings=[args.args], n_processes=args.n_processes, n_plots=args.n_plots[0])

    return None

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ MAIN ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~:
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create ROOT inputs and datacards for ZTT polarisation analysis.",
                                     parents=[logger.loggingParser])

    parser.add_argument("-i", "--input-dir", required=True,
                        help="Input directory.")
    parser.add_argument("-c", "--channel", action = "append",
                        default=["mt", "et", "tt", "em"],
                       help="Channel. This agument can be set multiple times. [Default: %(default)s]")
    parser.add_argument("--categories", action="append", nargs="+",
                        default=[["all"]] * len(parser.get_default("channel")),
                       help="Categories per channel. This agument needs to be set as often as --channels. [Default: %(default)s]")
    parser.add_argument("--combinations", nargs="+",
                        default=["individual", "channel", "category", "combined"],
                        choices=["individual", "channel", "category", "combined"],
                        help="Combinations to perform. [Default: %(default)s]")
    parser.add_argument("--no-bbb-uncs", action="store_true", default=False,
                        help="Do not add bin-by-bin uncertainties. [Default: %(default)s]")
    parser.add_argument("--steps", nargs="+",
                        default=["maxlikelihoodfit", "totstatuncs", "prefitpostfitplots", "pulls"],
                        choices=["maxlikelihoodfit", "totstatuncs", "prefitpostfitplots", "pulls", "deltanll", "nuisanceimpacts"],
                        help="Steps to perform. [Default: %(default)s]")
    parser.add_argument("--auto-rebin", action="store_true", default=False,
                        help="Do auto rebinning [Default: %(default)s]")
    parser.add_argument("--lumi", type=float, default=samples.default_lumi/1000.0,
                        help="Luminosity for the given data in fb^(-1). [Default: %(default)s]")
    parser.add_argument("-x", "--quantity", default=None,
                        help="Quantity. [Default: testZttPol13TeV_<category>]")
    parser.add_argument("-w", "--weight", default="1.0",
                        help="Additional weight (cut) expression. [Default: %(default)s]")
    parser.add_argument("--analysis-modules", default=[], nargs="+",
                        help="Additional analysis Modules. [Default: %(default)s]")
    parser.add_argument("-r", "--ratio", default=False, action="store_true",
                        help="Add ratio subplot. [Default: %(default)s]")
    parser.add_argument("-a", "--args", default="",
                        help="Additional Arguments for HarryPlotter. [Default: %(default)s]")
    parser.add_argument("-n", "--n-processes", type=int, default=1,
                        help="Number of (parallel) processes. [Default: %(default)s]")
    parser.add_argument("-b", "--batch", default=None, const="rwthcondor", nargs="?",
                        help="Run with grid-control. Optionally select backend. [Default: %(default)s]")
    parser.add_argument("-f", "--n-plots", type=int, nargs=2, default=[None, None],
                        help="Number of plots for datacard inputs (1st arg) and for postfit plots (2nd arg). [Default: all]")
    parser.add_argument("-o", "--output-dir",
                        default="$CMSSW_BASE/src/plots/ztt_polarisation_datacards/",
                        help="Output directory. [Default: %(default)s]")
    parser.add_argument("--clear-output-dir", action="store_true", default=False,
                        help="Delete/clear output directory before running this script. [Default: %(default)s]")
    parser.add_argument("--lumi-projection", type=float, nargs="+", default=[],
                        help="Specify luminosi ty values in fb^(-1) for a projection. [Default: %(default)s]")
    parser.add_argument("--use-asimov-dataset", action="store_true", default=False,
                        help="Use s+b expectation as observation instead of real data. [Default: %(default)s]")
    parser.add_argument("--check-linearity", type=float, nargs="+", default=[],
                        help="Specify the polarisation values for which to check the linearity of the discriminator. [Default: %(default)s]")
    parser.add_argument("--no-ewk-samples", default=False, action="store_true",
                        help="Do not use EWK Z/W samples. [Default: %(default)s]")
    parser.add_argument("--no-ewkz-as-dy", default=False, action="store_true",
                        help="Do not include EWKZ samples in inputs for DY. [Default: %(default)s]")
    parser.add_argument("--no-shape-uncs", default=False, action="store_true",
                        help="Do not include shape-uncertainties. [Default: %(default)s]")
    parser.add_argument("--era", default="2016",
                        help="Era of samples to be used. [Default: %(default)s]")
    parser.add_argument("--www", nargs="?", default=None, const="datacards",
                        help="Publish plots. [Default: %(default)s]")

    args = parser.parse_args()
    logger.initLogger(args)

    if args.channel != parser.get_default("channel"):
        args.channel = args.channel[len(parser.get_default("channel")):]

    if args.categories != parser.get_default("categories"):
        args.categories = args.categories[len(parser.get_default("categories")):]
    args.categories = (args.categories * len(args.channel))[:len(args.channel)]



    #1.-----Create Datacards
    print WARNING + UNDERLINE + '-----      Creating datacard with processes and systematics...        -----' + ENDC
    datacards = CreateDatacard(args)
    datacards.configs = datacardconfigs.DatacardConfigs()
    
    if args.no_shape_uncs:
        print OKBLUE + "No shape uncs!" + ENDC
        datacards.cb.FilterSysts(lambda systematic : systematic.type() == "shape")

    print OKGREEN + 'Datacard channels:' + ENDC, datacards.cb.channel_set()
    print OKGREEN + 'Datacard categories :' + ENDC, datacards.cb.bin_set()
    print OKGREEN + 'Datacard systematics :' + ENDC, datacards.cb.syst_name_set()


    #2.-----Creating input root files
    print WARNING + '-----      Creating input root files...             -----' + ENDC
    create_input_root_files(datacards, args)
    
    #3.-----Extract shapes from input root files or from samples with HP
    print WARNING + '-----      Extracting histograms from input root files...             -----' + ENDC
    
    ExtractShapes(datacards, args.output_dir +"/input/")
    #datacards.cb.SetGroup("syst", [".*"])
    
    #4.-----Add BBB
    print WARNING + '-----      Merging bin errors and generating bbb uncertainties...     -----' + ENDC

    BinErrorsAndBBB(datacards, 0.1, 0.5, True)
    #datacards.cb.SetGroup("syst_plus_bbb", [".*"])

    #5.-----Write Cards
    print WARNING + '-----      Writing Datacards...                                       -----' + ENDC

    output_root_filename_template = "datacards/common/${ANALYSIS}.input_${ERA}.root"
    datacard_filename_templates = []
    if "individual" in args.combinations:
        datacard_filename_templates.append("datacards/individual/${CHANNEL}/${BINID}/${ANALYSIS}_${CHANNEL}_${BINID}_${ERA}.txt")
    if "channel" in args.combinations:
        datacard_filename_templates.append("datacards/channel/${CHANNEL}/${ANALYSIS}_${CHANNEL}_${ERA}.txt")
    if "category" in args.combinations:
        datacard_filename_templates.append("datacards/category/${BINID}/${ANALYSIS}_${BINID}_${ERA}.txt")
    if "combined" in args.combinations:
        datacard_filename_templates.append("datacards/combined/${ANALYSIS}_${ERA}.txt")

    datacards_cbs = {}
    for datacard_filename_template in datacard_filename_templates:
        datacards_cbs.update(WriteDatacard(
                datacards,
                datacard_filename_template.replace("{", "").replace("}", ""),
                output_root_filename_template.replace("{", "").replace("}", ""),
                args.output_dir
        ))
    
    # exit here and do the rest with combineTool.py
    import sys
    sys.exit(0)
    
    #6.-----Write Cards
    print WARNING + UNDERLINE  + '-----      Performing statistical analysis                            -----' + ENDC
    
    if args.use_asimov_dataset:
        print datacards
        datacards = use_asimov_dataset(datacards)
        print datacards
        print OKBLUE + "Using asimov dataset!" + ENDC
        
    #print OKBLUE + "datacards.cb.PrintAll()" + ENDC, datacards.cb.PrintAll()
    
    #7.-----text2workspace
    print WARNING + '-----      text2workspace                                             -----' + ENDC

    physicsmodel = "CombineHarvester.ZTTPOL2016.taupolarisationmodels:ztt_pol"
    datacards_workspaces = text2workspace(datacards, datacards_cbs, physicsmodel, "workspace")

