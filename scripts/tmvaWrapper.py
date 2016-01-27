#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import argparse
import copy
import os

import Artus.Utility.jsonTools as jsonTools
import sys
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.samples_run2 as samples
import ROOT
import glob
from ROOT import TCut, TString
ROOT.PyConfig.IgnoreCommandLineOptions = True

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Make Data-MC control plots.",
                                     parents=[logger.loggingParser])

    parser.add_argument("-i", "--input-dir", required=True,
                        help="Input directory.")
    parser.add_argument("-s", "--signal_samples", nargs="+",
                        default=["ggh", "qqh", "vh"],
                        choices=["ggh", "qqh", "vh"], 
                        help="Signal-Samples. [Default: %(default)s]")
    parser.add_argument("-b", "--bkg_samples", nargs="+",
                        default=["ztt", "zll", "ttj", "vv", "wj"],
                        choices=["ztt", "zll", "ttj", "vv", "wj", "qcd"], 
                        help="Bkg-Samples. [Default: %(default)s]")
    parser.add_argument("-c", "--channels", nargs="*",
                        default=["tt", "mt", "et", "em", "mm", "ee"],
                        help="Channels. [Default: %(default)s]")
    parser.add_argument("-x", "--quantities", nargs="*",
                        default=["pVecSum", "pt_1", "mt_1", "pt_2", "mt_2", "met", 
                                "mvamet", "pZetaMissVis", "pZetaMiss", 
                                "pZetaVis","njets", "nbtag", 
                                "min_ll_jet_eta","lep1_centrality", 
                                "lep2_centrality", 
                                "delta_lep_centrality", "m_vis"],
                        help="Quantities to train on. [Default: %(default)s]")
    parser.add_argument("--lumi", type=float, default=2.155,
                        help="""Luminosity for the given data in fb^(-1). 
                                [Default: %(default)s]""")
    parser.add_argument("-w", "--weight", default="1.0",
                        help="""Additional weight (cut) expression.
                        [Default: %(default)s]""")
    parser.add_argument("-e", "--exclude-cuts", nargs="+", default=["pZetaMiss", "pZetaVis", "iso_1", "iso_2", "mt_1", "mt_2"],
                        help="""Exclude (default) selection cuts. 
                        [Default: %(default)s]""")
    parser.add_argument("--higgs-masses", nargs="+", default=["125"],
                        help="Higgs masses. [Default: %(default)s]")
    parser.add_argument("-S", "--Split", default='60', 
                        help="""If set enables splitting into training and test
                        tree, use value between 0 and 99 to split tree using
                        variable TrainingSelectionValue. [Default: %(default)s]""")
    parser.add_argument("-o", "--output-file",required=True,
                        default="tmvaClassification/output.root",
                        help="Output file. [Default: %(default)s]")
    parser.add_argument("--factory-options", default="",
                        help="Options for TMVA.Factory constructor. [Default: %(default)s]")
    parser.add_argument("-n", "--name", default="training",
                        help="Training name. [Default: %(default)s]")
    parser.add_argument("-m", "--methods", nargs="+", required=True, default=['BDT;nCuts=1200:NTrees=150:MinNodeSize=0.25;BoosType=Grad;Shrinkage=0.2'],
                        help="MVA methods. Multiple arguments for TMVA.Factory.BookMethod are split by semicolon. Format: name;options. [Default: %(default)s]")
    parser.add_argument("--preparation-trees-options", default="",
                        help="Options for preparation of inputs trees as passed to TMVA.Factory.PrepareTrainingAndTestTree. [Default: %(default)s]")
    args = parser.parse_args()
    logger.initLogger(args)
    
    if args.signal_samples == parser.get_default("signal_samples"):
        args.signal_samples = [sample for sample in args.signal_samples 
                        if hasattr(samples.Samples, sample)]
    if args.bkg_samples == parser.get_default("bkg_samples"):
        args.bkg_samples = [sample for sample in args.bkg_samples 
                        if hasattr(samples.Samples, sample)]
    if "qcd" in (args.bkg_samples+args.signal_samples):
        log.error("qcd not possible for training")
        sys.exit()
    list_of_samples = [getattr(samples.Samples, sample) for sample in 
                        (args.bkg_samples+args.signal_samples)]
    sample_settings = samples.Samples()
    #getting config
    plot_configs = []
    for channel in args.channels:
        category = None
        quantity = "pt_1"
        config = sample_settings.get_config(
                samples=list_of_samples,
                channel=channel,
                category=category,
                higgs_masses=args.higgs_masses,
                normalise_signal_to_one_pb=False,
                ztt_from_mc=False,
                weight="",
                lumi = args.lumi * 1000,
                exclude_cuts=args.exclude_cuts,
                blind_expression=channel+"_"+quantity,
                stack_signal=False,
                scale_signal=1.0,
                mssm=False
                )
        plot_configs.append(config)
    #extract important information from config
    scale_input = []
    file_names = []
    cuts = []
    s_b_extension = []
    nicks = []
    folder = []
    for config in plot_configs:
        for i,nick in enumerate(config["nicks"]):
            if nick in args.bkg_samples:
                for f in config["files"][i].split(' '):
                    nicks.append(nick)
                    scale_input.append(config["scale_factors"][i])
                    file_names.append(f)
                    cuts.append(config["weights"][i][17:])
                    folder.append(config["folders"][i])
                    s_b_extension.append("Background")
            elif ("ggh" in nick and "ggh" in args.signal_samples) or ("qqh"
                in nick and "qqh" in args.signal_samples):
                for f in config["files"][i].split(' '):
                    nicks.append(nick)
                    scale_input.append(config["scale_factors"][i])
                    file_names.append(f)
                    cuts.append(config["weights"][i][17:])
                    folder.append(config["folders"][i])
                    s_b_extension.append("Signal")
            elif "vh" in args.signal_samples and ("wmh" in nick or
                                                  "wph" in nick or
                                                  "zh" in nick):
                for f in config["files"][i].split(' '):
                    nicks.append(nick)
                    scale_input.append(config["scale_factors"][i])
                    file_names.append(f)
                    cuts.append(config["weights"][i][17:])
                    folder.append(config["folders"][i])
                    s_b_extension.append("Signal")
                    
    #TMVA Stuff
    ROOT.TMVA.Tools.Instance()
    if args.Split:
        cutTest = "(TrainingSelectionValue>=%i)*"%int(args.Split)
        cutTrain = "(TrainingSelectionValue<%i)*"%int(args.Split)
        
    # create output file
    dir_path, filename = os.path.split(args.output_file)
    storage_name_extension = filename.replace(".root", "") + "_storage"
    if dir_path is None:
        pass
    elif not os.path.exists(dir_path):
        os.makedirs(dir_path)
    output_file = ROOT.TFile(args.output_file, "RECREATE")
    
    # create factory
    log.debug("TMVA.Factory(\"" + args.name + "\", TFile(\"" + args.output_file +
              "\", \"RECREATE\"), \"" + args.factory_options + "\")")
    tmva_factory = ROOT.TMVA.Factory(args.name, output_file,
                                     args.factory_options)
    # add training variables
    for variable in args.quantities:
        log.debug("TMVA.Factory.AddVariable(" +
                    ", ".join(["\"" + v + "\""
                               for v in variable.split(";")]) + ")")
        tmva_factory.AddVariable(*(variable.split(";")))
    #add trees
    open_trees = []
    tree_list = []
    for i, nick in enumerate(nicks):
        root_file_name = glob.glob(args.input_dir+file_names[i])[0]
        if (root_file_name) in open_trees:
            c_tree = tree_list[open_trees.index(
                root_file_name)]
        else:
            open_trees.append(root_file_name)
            tree_list.append(ROOT.TChain())
            root_file_name = root_file_name + '/' + folder[i]
            tree_list[-1].Add(root_file_name)
            c_tree = tree_list[-1]
        store_file = ROOT.TFile("%s_%s.root"%(storage_name_extension, nick), "RECREATE")
        storage_tree_train = c_tree.CopyTree(cutTrain+cuts[i], "training")
        storage_tree_train.SetName("Training")
        storage_tree_test = c_tree.CopyTree(cutTest+cuts[i], "testing")
        storage_tree_test.SetName("Testing")
        store_file.Write()
        store_file.Close()
        training_tree = ROOT.TChain()
        training_tree.Add("%s_%s.root/Training"%(storage_name_extension, nick))
        testing_tree = ROOT.TChain()
        testing_tree.Add("%s_%s.root/Testing"%(storage_name_extension, nick))
        
        tmva_factory.AddTree(testing_tree, s_b_extension[i],
                             scale_input[i],
                             TCut(""), "test")
        tmva_factory.AddTree(training_tree, s_b_extension[i],
                             scale_input[i],
                             TCut(""), "train")
        log.debug("tmva_factory.AddTree(%s,%s,%s,TCut(''), train/test)" %(
            nick, s_b_extension[i], cuts[i]))
    tmva_factory.SetBackgroundWeightExpression('eventWeight')
    tmva_factory.SetSignalWeightExpression('eventWeight')
    for tree in tree_list:
        tree.~TTree()
    #prepare trees
    if args.Split:
        tmva_factory.PrepareTrainingAndTestTree(ROOT.TCut(''),
                                                ROOT.TCut(''),
                                                "NormMode=None:!V")
    else:
        tmva_factory.PrepareTrainingAndTestTree(ROOT.TCut(''),
                                            ROOT.TCut(''),
                                            args.preparation_trees_options)
    log.debug("TMVA.Factory.PrepareTrainingAndTestTree(\"" +
              "\", \"" + args.preparation_trees_options + "\")")
    
     # book methods
    for method in args.methods:
        method, options = method.split(';')
        name = method + '_' + filename
        tmva_factory.BookMethod(method, name, options)
        log.debug("TMVA.Factory.BookMethod(" + ", ".join(
            ["\"" + m + "\"" for m in (method, name, options)]) + ")")
    # perform full training
    log.debug("TMVA.Factory.TrainAllMethods()")
    tmva_factory.TrainAllMethods()
    
    log.debug("TMVA.Factory.TestAllMethods()")
    tmva_factory.TestAllMethods()
    
    log.debug("TMVA.Factory.EvaluateAllMethods()")
    tmva_factory.EvaluateAllMethods()
    
    # finish
    output_file.Close()
    log.info("Training output is written to \"" + args.output_file + "\".")
    