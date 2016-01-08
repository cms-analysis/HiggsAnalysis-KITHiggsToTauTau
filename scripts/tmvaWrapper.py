#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import argparse
import os
import sys
import time
from fnmatch import fnmatch

import Artus.Utility.jsonTools as jsonTools

import ROOT
from ROOT import TCut, TString
ROOT.PyConfig.IgnoreCommandLineOptions = True

def tmva_Wrapper(args_from_script=None):
    """
    Perform TMVA classification training.
    
    http://root.cern.ch/svn/root/trunk/tmva/test/TMVAClassification.C
    http://root.cern.ch/root/htmldoc/TMVA__Factory.html
    http://root.cern.ch/root/htmldoc/TMVA_Index.html
    """

    parser = argparse.ArgumentParser(description="Perform TMVA classification training.",
                                    fromfile_prefix_chars="@", conflict_handler="resolve",
                                    parents=[logger.loggingParser])

    parser.add_argument("-o", "--output-file", default="tmvaClassification/output.root",
                        help="Output file. [Default: %(default)s]")
    parser.add_argument("-n", "--name", default="training",
                        help="Training name. [Default: %(default)s]")
    parser.add_argument("--factory-options", default="",
                        help="Options for TMVA.Factory constructor. [Default: %(default)s]")
    parser.add_argument("-v", "--variables", nargs="+", required=True, default=None,
                        help="Training variables. Multiple arguments for TMVA.Factory.AddVariable are split by semicolon.")
    parser.add_argument("--spectator-variables", nargs="+", default=[],
                        help="Spectator variables. Multiple arguments for TMVA.Factory.AddSpectator are split by semicolon. [Default: %(default)s]")
    
    parser.add_argument("-s", "--signal-trees", nargs="+", required=True, default=None,
                        help="Signal trees/Directories containing signal tree[s].")
    parser.add_argument("--signal-tree-weights", nargs="+", type=float, default=[1.0],
                        help="Weights for signal trees. Need same number of arguments as for --signal-trees or one.")
    parser.add_argument("--signal-event-weight", help="Signal event weight expression.")
    parser.add_argument("--signal-cuts", default="", help="Signal cut expression. [Default: %(default)s]")
    
    parser.add_argument("-b", "--background-trees", nargs="+", required=True, default=None,
                        help="Background trees/Directories containing Background tree[s].")
    parser.add_argument("--background-tree-weights", nargs="+", type=float, default=[1.0],
                        help="Weights for background trees. Need same number of arguments as for --background-trees or one.")
    parser.add_argument("--background-event-weight", help="Background event weight expression.")
    parser.add_argument("--background-cuts", default="", help="Background cut expression. [Default: %(default)s]")
    
    parser.add_argument("--preparation-trees-options", default="",
                        help="Options for preparation of inputs trees as passed to TMVA.Factory.PrepareTrainingAndTestTree. [Default: %(default)s]")
    
    parser.add_argument("-m", "--methods", nargs="+", required=True, default=None,
                        help="MVA methods. Multiple arguments for TMVA.Factory.BookMethod are split by semicolon. Format: name;title;options.")
    
    parser.add_argument("-f", "--folders", nargs="+", required=True, default=[],
                        help="folder names within ROOT-files e.g.: em_jecUnc_Nom em_jecUnc_Nom_tt.")
    parser.add_argument("-N", "--Ntuple-name", nargs="+", required=True, default=['ntuple'],
                        help="Name of the ntuples you want to read e.g.: ntuple   [Default: %(default)s")
    parser.add_argument("-S", "--Split", default=False, 
                        help="If set enables splitting into training and test tree, use value between 0 and 99 to split tree using variable TrainingSelectionValue")

    args = parser.parse_args(args_from_script.split() if args_from_script != None else None)
    logger.initLogger(args)
    
    # load the library
    ROOT.TMVA.Tools.Instance()
    cutTest = TCut("")
    cutTrain = TCut("")
    #check if split_cut is required
    if args.Split:
        cutTest = TCut("TrainingSelectionValue>=%i"%int(args.Split))
        cutTrain = TCut("TrainingSelectionValue<%i"%int(args.Split))
    
    # create output file
    if not os.path.exists(os.path.dirname(args.output_file)):
        os.makedirs(os.path.dirname(args.output_file))
    output_file = ROOT.TFile(args.output_file, "RECREATE")
    
    # create factory
    log.debug("TMVA.Factory(\"" + args.name + "\", TFile(\"" + args.output_file + "\", \"RECREATE\"), \"" + args.factory_options + "\")")
    tmva_factory = ROOT.TMVA.Factory(args.name, output_file, args.factory_options)
    
    # add training variables
    for variable in args.variables:
        log.debug("TMVA.Factory.AddVariable(" + ", ".join(["\"" + v + "\"" for v in variable.split(";")]) + ")")
        tmva_factory.AddVariable(*(variable.split(";")))
    
    # add spectator variables
    for spectator_variable in args.spectator_variables:
        log.debug("TMVA.Factory.AddSpectator(" + ", ".join(["\"" + v + "\"" for v in spectator_variable.split(";")]) + ")")
        tmva_factory.AddSpectator(*(spectator_variable.split(";")))
    
    # add signal
    if len(args.signal_tree_weights) != 1 and len(args.signal_tree_weights) != len(args.signal_trees):
        log.warning("Number of signal tree weights need to be 1 or " + len(args.signal_trees) + "!")
    args.signal_tree_weights = (args.signal_tree_weights * len(args.signal_trees))[:len(args.signal_trees)]
    
    for signal_tree_parameter, signal_tree_weight in zip(args.signal_trees, args.signal_tree_weights):
        log.debug("Evaluate signal parameter: " + signal_tree_parameter)
        pattern = "*.root"
        signal_files_list = []
        #find all root files in signal_folders
        if fnmatch(signal_tree_parameter, pattern):
            signal_files_list.append(signal_tree_parameter)
            log.debug("Add 1 RootFile: " + signal_tree_parameter)
        elif os.path.isdir(signal_tree_parameter) or os.path.islink(signal_tree_parameter):
            for path, subdirs, files in os.walk(signal_tree_parameter, followlinks=True):
                log.debug('check path: ' +path)
                log.debug('check subdirs:' +str(subdirs))
                log.debug('check files:' +str(files)) 
                for name in files:
                    if fnmatch(name, pattern):
                        signal_files_list.append(os.path.join(path, name))
                        log.debug("Add 1 RootFile: " + signal_tree_parameter)
        for root_file in signal_files_list:
            a = ROOT.TFile(root_file)
            for ntuple_folder in args.folders:
                last_dir = a.GetDirectory(ntuple_folder)
                if not last_dir == None:
                    for possible_ntuple in last_dir.GetListOfKeys():
                        if possible_ntuple.GetName() in args.Ntuple_name:
                            root_ntuple = os.path.join(root_file, ntuple_folder)
                            root_ntuple = os.path.join(root_ntuple, possible_ntuple.GetName())
                            signal_tree = ROOT.TChain()
                            signal_tree.Add(root_ntuple)
                            if args.Split:
                                tmva_factory.AddTree(signal_tree, "Signal", signal_tree_weight, cutTrain, "train")
                                tmva_factory.AddTree(signal_tree, "Signal", signal_tree_weight, cutTest, "test")
                                log.debug("TMVA.Factory.AddTree(%s, 'Signal', %s, %s/%s, 'train/test')"%(root_ntuple, signal_tree_weight, cutTrain, cutTest))
                            else:
                                tmva_factory.AddSignalTree(signal_tree, signal_tree_weight)
                                log.debug("TMVA.Factory.AddSignalTree(TChain.Add(\"" + root_ntuple + "\"), " + str(signal_tree_weight) + ")")
                            
    if args.signal_event_weight:
        log.debug("TMVA.Factory.SetSignalWeightExpression(\"" + args.signal_event_weight + "\")")
        tmva_factory.SetSignalWeightExpression(args.signal_event_weight)
    
    # add background
    if len(args.background_tree_weights) != 1 and len(args.background_tree_weights) != len(args.background_trees):
        log.warning("Number of background tree weights need to be 1 or " + len(args.background_trees) + "!")
    args.background_tree_weights = (args.background_tree_weights * len(args.background_trees))[:len(args.background_trees)]
    
    for background_tree_parameter, background_tree_weight in zip(args.background_trees, args.background_tree_weights):
        pattern = "*.root"
        background_files_list = []
        #find all root files in background_folders
        if fnmatch(background_tree_parameter, pattern):
            file_name = background_tree_parameter.strip('.root')
            background_files_list.append(background_tree_parameter)
        elif os.path.isdir(background_tree_parameter):
                for path, subdirs, files in os.walk(background_tree_parameter, followlinks=True):
                    for name in files:
                        if fnmatch(name, pattern):
                            background_files_list.append(os.path.join(path, name))
                            
        for root_file in background_files_list:
            a = ROOT.TFile(root_file)
            for ntuple_folder in args.folders:
                last_dir = a.GetDirectory(ntuple_folder)
                if not last_dir == None:
                    for possible_ntuple in last_dir.GetListOfKeys():
                        if possible_ntuple.GetName() in args.Ntuple_name:
                            root_ntuple = os.path.join(root_file, ntuple_folder)
                            root_ntuple = os.path.join(root_ntuple, possible_ntuple.GetName())
                            background_tree = ROOT.TChain()
                            background_tree.Add(root_ntuple)
                            if args.Split:
                                tmva_factory.AddTree(background_tree, "Background", background_tree_weight, cutTrain, "train")
                                tmva_factory.AddTree(background_tree, "Background", background_tree_weight, cutTest, "test")
                                log.debug("TMVA.Factory.AddTree(%s, 'Background', %s, %s/%s, 'train/test')"%(root_ntuple, background_tree_weight, cutTrain, cutTest))
                            else:
                                tmva_factory.AddBackgroundTree(background_tree, background_tree_weight)
                                log.debug("TMVA.Factory.AddBackgroundTree(TChain.Add(\"" + root_ntuple + "\"), " + str(background_tree_weight) + ")")
                                                
    if args.background_event_weight:
        log.debug("TMVA.Factory.SetBackgroundWeightExpression(\"" + args.background_event_weight + "\")")
        tmva_factory.SetBackgroundWeightExpression(args.background_event_weight)
    
    # prepare trees
    log.debug("TMVA.Factory.PrepareTrainingAndTestTree(\"" + args.signal_cuts + "\", \"" + args.background_cuts + "\", \"" + args.preparation_trees_options + "\")")
    tmva_factory.PrepareTrainingAndTestTree(ROOT.TCut(args.signal_cuts), ROOT.TCut(args.background_cuts),
                                            args.preparation_trees_options)
    
    # book methods
    #for method in args.methods:
        #tmva_factory.BookMethod(*(map(TString, method.split(';'))))
        #time.sleep(3)
    print ROOT.TMVA.Types.Instance().GetMethodType( "BDT" )
    try:
        tmva_factory.BookMethod(ROOT.TMVA.Types.Instance().GetMethodType( "BDT" ), TString("TestBDT"), TString("nCuts=1200:NTrees=150:MinNodeSize=0.25"))
    except:
        tmva_factory.BookMethod(TString("BDT"), TString("TestBDT"), TString("nCuts=1200:NTrees=150:MinNodeSize=0.25"))
        #log.debug("TMVA.Factory.BookMethod(" + ", ".join(["\"" + m + "\"" for m in method.split(";")]) + ")")
    
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
    
tmva_Wrapper()
#/nfs/dust/cms/user/mschmitt/analysis/CMSSW_7_1_5/src/HiggsAnalysis/KITHiggsToTauTau/scripts/tmvaWrapper.py -s Sig/ -b Bkg/ -f mt_jecUncNom_tauEsNom -N ntuple -m "BDT;SplitTest;nCuts=1200:NTrees=150:MinNodeSize=0.25" -v pt_1 pZetaVis pZetaMiss iso_1  nbtag njets pVecSum min_ll_jet_eta lep1_centrality lep2_centrality delta_lep_centrality -o all_plus/split_test.root -S 35

