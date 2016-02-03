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

    parser = argparse.ArgumentParser(description="Train BDTs using TMVA interface.",
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
    parser.add_argument("-m", "--methods", nargs="+", default=['BDT;nCuts=1200:NTrees=150:MinNodeSize=0.25:BoostType=Grad:Shrinkage=0.2'],
                        help="MVA methods. Multiple arguments for TMVA.Factory.BookMethod are split by semicolon. Format: name;options. [Default: %(default)s]")
    parser.add_argument("--preparation-trees-options", default="",
                        help="Options for preparation of inputs trees as passed to TMVA.Factory.PrepareTrainingAndTestTree. [Default: %(default)s]")
    parser.add_argument("-n", "--n-fold", type=int, default=0,
                        help="number of splits for n-fold training. 0 is regular splitting according to --Split, 1 is one split,which results in 2 parts...[Default: %(default)s]")
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
                    
    splits_list = []
    stored_files_list = []
    #TMVA Stuff
    ROOT.TMVA.Tools.Instance()
    if args.Split and args.n_fold == 0:
        splits_list.append("(TrainingSelectionValue>=%i)*"%int(args.Split))
        splits_list.append("(TrainingSelectionValue<%i)*"%int(args.Split))
    elif args.n_fold:
        part_size = 100/(args.n_fold+1)
        for i in range(args.n_fold+1):
            splits_list.append("(TrainingSelectionValue>=%i)*(TrainingSelectionValue<%i)*"%(i*part_size,(i+1)*part_size))
        
    # create output file
    dir_path, filename = os.path.split(args.output_file)
    filename = filename.replace(".root", "")
    storage_name_extension = filename + "_storage"
    if dir_path is None:
        pass
    elif not os.path.exists(dir_path):
        os.makedirs(dir_path)
    
    #produce trees
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
        stored_files_list.append("%s_%s_"%(storage_name_extension, nick))
        log.debug("Prepare Sample %s "%stored_files_list[-1])
        for j,split in enumerate(splits_list):
            store_file = ROOT.TFile("%s_%s_%s.root"%(storage_name_extension, nick, "split%i"%j), "RECREATE")
            storage_tree= c_tree.CopyTree(split+cuts[i], "tree%i"%j)
            storage_tree.SetName("SplitTree")
            store_file.Write()
            store_file.Close()
        
    for ifac in range(args.n_fold+1):
        iteration = args.n_fold+1
        output = ROOT.TFile(os.path.join(dir_path, filename+"T%i.root"%i), "RECREATE")
        # create factory
        log.debug("TMVA.Factory(\"T%i"%ifac + "\", TFile(\"" + args.output_file +
                "\", \"RECREATE\"), \"" + args.factory_options + "\")")
        factory=ROOT.TMVA.Factory("T%i"%ifac, output,
                                    args.factory_options)
        # add training variables
        for variable in args.quantities:
            log.debug("TMVA.Factory.AddVariable(" +
                        ", ".join(["\"" + v + "\""
                                for v in variable.split(";")]) + ")")
            factory.AddVariable(*(variable.split(";")))
        #add trees to factories
        skip = False
        if args.n_fold == 0:
            iteration += 1;
        for j,stored_file in enumerate(stored_files_list):
            for i in range(iteration):
                tree = ROOT.TChain()
                tree.Add(stored_file+"split%i.root/SplitTree"%(i))
                if i == ifac:
                    factory.AddTree(tree, s_b_extension[j],
                                                    scale_input[j],
                                                    TCut(""), "test")
                    log.debug("Add to Factory_%i sample %s as TestSample"%(ifac, stored_file+"split%i.root/SplitTree"%(i)))
                else:
                    
                    factory.AddTree(tree, s_b_extension[j],
                                                    scale_input[j],
                                                    TCut(""), "train")
                    log.debug("Add to Factory_%i sample %s as TrainingsSample"%(ifac, stored_file+"split%i.root/SplitTree"%(i)))
            log.debug("factory.AddTree(%s,%s,%s,TCut(''), train/test)" %(
                nick, s_b_extension[j], cuts[j]))
        
        factory.SetBackgroundWeightExpression('eventWeight')
        factory.SetSignalWeightExpression('eventWeight')
        factory.PrepareTrainingAndTestTree(ROOT.TCut(''),
                                                ROOT.TCut(''),
                                                "NormMode=None:!V")
        # book methods
        for method in args.methods:
            method, options = method.split(';')
            name = method + '_' + filename
            factory.BookMethod(method, name, options)
            log.debug("TMVA.Factory.BookMethod(" + ", ".join(
                ["\"" + m + "\"" for m in (method, name, options)]) + ")")
        
        # perform full training
        log.debug("TMVA.Factory.TrainAllMethods()")
        factory.TrainAllMethods()
        
        log.debug("TMVA.Factory.TestAllMethods()")
        factory.TestAllMethods()
        
        log.debug("TMVA.Factory.EvaluateAllMethods()")
        factory.EvaluateAllMethods()
        
        # finish
        output.Close()
        del factory
        log.info("Training output is written to \"" + os.path.join(dir_path, filename+"T%i.root"%ifac) + "\".")