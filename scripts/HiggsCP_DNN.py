import os
import copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras

'''
# mt or tt: for simple or double hadronic decay mode
# Boost:
- 1: on full generator level: tau ( and potentially visible decay porducts) into higgs restframe
- 2: on full reconstruction level: visible decay products into combined restframe
- 3: on full reconstruction level: visible decay products into intermediate charged decay products restframe
# rot: align boosted 4vectors along z-axis

### implemented methods
mixing angle multiclassing classification
cp singleclass classification
cp raw singleclass classification                   // DNN used from 1608.02609 (No Keras)

'''
################################
version = "GG_VBF_tt_full_boost3_rot_sort"
################################
#   use a unique tag to mark different DNN settings (only for plot saving important)
tag = ""

#   Global variables defined by mode
mixing_labels = ["000", "010", "020", "030", "040", "050", "060", "070", "080", "090", "100", "110", "120", "130",
                 "140", "150", "160", "170", "180", "190", "200"]
chain_results = True  # True: validate DNN directly after training
use_genmatched = False  # True: use generator information for 4-vectors
decay_channel = (1.0, 1.0)  # Tuple: (decayModeMVA_1,decayModeMVA_2)
select_mixing = "100"  # the selected mixing angle for binary classification
decay_label = "d" + str(int(decay_channel[0])) + "d" + str(int(decay_channel[1]))

# Switches for different DNN methods
is_MixingAngle_Multiclassing = True
is_cp_binaryclassing = False
is_cpraw_binaryclassing = False

#   the directory with the signal samples
sample_directory = "/net/scratch_cms3b/fenger/artus/HiggsCP_DNN/input/"
#   the directory to use for storing/ loading the csv dataset, model, and additional files
output_directory = "/net/scratch_cms3b/fenger/artus/HiggsCP_DNN/output/" + version + "/"

#   create sub directory for version
if not os.path.isdir(output_directory):
    os.mkdir(output_directory)

# set label for DNN method:
if is_MixingAngle_Multiclassing:
    method_label = "MixingAngle_Multiclassing" + "_" + decay_label
if is_cp_binaryclassing:
    method_label = "CP_Binary" + "_" + decay_label
if is_cpraw_binaryclassing:
    method_label = "CPraw_Binary" + "_" + decay_label


# Argument parser
def parser():
    import argparse

    parser = argparse.ArgumentParser(
        description="Script for LFV Analysis 2017. This code classifies a set of signal-background samples using a dnn. The result of classification on the form of a dnn_score is then appended to the root files and can then be used for statistical analysis.",
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("--csv", action="store_true", help="Create csv file as DNN input")
    parser.add_argument("--training", action="store_true", help="Train the DNN")
    parser.add_argument("--results", action="store_true", help="get DNN results by application to the whole dataset")
    parser.add_argument("--attach", action="store_true", help="attach DNN score to ROOT files")
    parser.add_argument("--debug", action="store_true", help="debug code")
    return parser.parse_args()


############################################################################################################
#################    Settings for DNN input    #############################################################
############################################################################################################

var_list = []
par_list = []

# Decay Channel Rho - Rho
if decay_channel[0] == 1 and decay_channel[1] == 1:
    if not use_genmatched:
        var_list = mixing_labels + ["PhiStarCP",
                                    "reco_negyTauL",
                                    "reco_posyTauL",
                                    "q_1",
                                    "q_2"]
        par_list = ["lep1LV",
                    "lep2LV",
                    "lep1neutrinoLV",
                    "lep2neutrinoLV",
                    "lep1SumChargedHadronsLV",
                    "lep1SumNeutralHadronsLV",
                    "lep2SumChargedHadronsLV",
                    "lep2SumNeutralHadronsLV"]

    if use_genmatched:
        var_list = mixing_labels + ["genMatchedPhiStarCP"]
        par_list = ["genMatchedTau1LV",
                    "genMatchedTau2LV",
                    "genMatchedTau1NeutrinoLV",
                    "genMatchedTau2NeutrinoLV",
                    "genMatchedTau1SumChargedHadronsLV",
                    "genMatchedTau1SumNeutralHadronsLV",
                    "genMatchedTau2SumChargedHadronsLV",
                    "genMatchedTau2SumNeutralHadronsLV"]

# Decay Channel a1 - cPi
if (decay_channel[0] == 0 and decay_channel[1] == 10) or (decay_channel[0] == 10 and decay_channel[1] == 0):
    if not use_genmatched:
        var_list = mixing_labels + ["PhiStarCP",
                                    "reco_negyTauL",
                                    "reco_posyTauL",
                                    "q_1",
                                    "q_2"]
        par_list = ["lep1LV",
                    "lep2LV",
                    "lep1neutrinoLV",
                    "lep2neutrinoLV",
                    "lep1SumChargedHadronsLV",
                    "lep1SumNeutralHadronsLV",
                    "lep2SumChargedHadronsLV",
                    "lep2SumNeutralHadronsLV"]

    if use_genmatched:
        var_list = mixing_labels + ["genMatchedPhiStarCP"]
        par_list = ["genMatchedTau1LV",
                    "genMatchedTau2LV",
                    "genMatchedTau1NeutrinoLV",
                    "genMatchedTau2NeutrinoLV",
                    "genMatchedTau2LV",
                    "genMatchedTau1ChargedHadronLV_1",
                    "genMatchedTau1ChargedHadronLV_2",
                    "genMatchedTau1ChargedHadronLV_3"]

# Decay Channel a1 - rho
if (decay_channel[0] == 1 and decay_channel[1] == 10) or (decay_channel[0] == 10 and decay_channel[1] == 1):
    if not use_genmatched:
        var_list = mixing_labels + ["PhiStarCP",
                                    "reco_negyTauL",
                                    "reco_posyTauL",
                                    "q_1",
                                    "q_2"]
        par_list = ["lep1LV",
                    "lep2LV",
                    "lep1neutrinoLV",
                    "lep2neutrinoLV",
                    "lep1SumChargedHadronsLV",
                    "lep1SumNeutralHadronsLV",
                    "lep2SumChargedHadronsLV",
                    "lep2SumNeutralHadronsLV"]

    if use_genmatched:
        var_list = mixing_labels + ["genMatchedPhiStarCP"]
        par_list = ["genMatchedTau1LV",
                    "genMatchedTau2LV",
                    "genMatchedTau1NeutrinoLV",
                    "genMatchedTau2NeutrinoLV",
                    "genMatchedTau2SumChargedHadronsLV",
                    "genMatchedTau2SumNeutralHadronsLV",
                    "genMatchedTau1ChargedHadronLV_1",
                    "genMatchedTau1ChargedHadronLV_2",
                    "genMatchedTau1ChargedHadronLV_3"]

# Decay Channel a1 - a1
if decay_channel[0] == 10 and decay_channel[1] == 10:
    if not use_genmatched:
        var_list = mixing_labels + ["PhiStarCP",
                                    "reco_negyTauL",
                                    "reco_posyTauL",
                                    "q_1",
                                    "q_2"]
        par_list = ["lep1LV",
                    "lep2LV",
                    "lep1neutrinoLV",
                    "lep2neutrinoLV",
                    "lep1SumChargedHadronsLV",
                    "lep1SumNeutralHadronsLV",
                    "lep2SumChargedHadronsLV",
                    "lep2SumNeutralHadronsLV"]

    if use_genmatched:
        var_list = mixing_labels + ["genMatchedPhiStarCP"]
        par_list = ["genMatchedTau1LV",
                    "genMatchedTau2LV",
                    "genMatchedTau1NeutrinoLV",
                    "genMatchedTau2NeutrinoLV",
                    "genMatchedTau1ChargedHadronLV_1",
                    "genMatchedTau1ChargedHadronLV_2",
                    "genMatchedTau1ChargedHadronLV_3",
                    "genMatchedTau2ChargedHadronLV_1",
                    "genMatchedTau2ChargedHadronLV_2",
                    "genMatchedTau2ChargedHadronLV_3"]

for entry in par_list:
    var_list.append(entry + "Pt")
    var_list.append(entry + "Eta")
    var_list.append(entry + "Phi")
    var_list.append(entry + "E")


############################################################################################################
#################    CSV Iput    ###########################################################################
############################################################################################################


def get_csv_reco():
    import ROOT
    from math import acos, cos, sin
    from tqdm import tqdm

    # check for old csv file, if it exist its getting deleted
    if os.path.exists(output_directory + "csv_" + version + "_train.csv"):
        os.remove(output_directory + "csv_" + version + "_train.csv")
        os.remove(output_directory + "csv_" + version + "_valid.csv")
        print("removed old csv file")

    # Settings
    filelist = [
        "GluGluHToTauTauUncorrelatedDecayFilteredM125_RunIIFall17MiniAODv2_PU2017_13TeV_MINIAOD_powheg-pythia8.root",
        "VBFHToTauTauUncorrelatedDecayFilteredM125_RunIIFall17MiniAODv2_PU2017_13TeV_MINIAOD_powheg-pythia8.root"]

    #    list of entry variables from root tree
    rmlv_entry_list = ["svfitTau1LV",
                        "svfitTau2LV",
                        "simpleFitTau1LV",
                        "simpleFitTau2LV",
                        "svfitneutrino1LV",
                        "svfitneutrino2LV",
                        "simpleFitneutrino1LV",
                        "simpleFitneutrino2LV",
                        "lep1LV",
                        "lep2LV",
                        "lep1SumChargedHadronsLV",
                        "lep1SumNeutralHadronsLV",
                        "lep2SumChargedHadronsLV",
                        "lep2SumNeutralHadronsLV",
                        "lep1ChargedHadronLV_1",
                        "lep1ChargedHadronLV_2",
                        "lep1ChargedHadronLV_3",
                        "lep2ChargedHadronLV_1",
                        "lep2ChargedHadronLV_2",
                        "lep2ChargedHadronLV_3"]

    param_entry_list = ["decayModeMVA_1",
                        "decayModeMVA_2",
                        "simpleFitConverged",
                        "reco_negyTauL",
                        "reco_posyTauL",
                        "q_1",
                        "q_2",
                        "m2_1",
                        "m2_2"]

    # defining variables, read in info from json file and open csv file
    print("Creating CSV file: ",version)
    csv_train = open(output_directory + "csv_" + version + "_train.csv", "w")
    csv_valid = open(output_directory + "csv_" + version + "_valid.csv", "w")

    # write csv header
    csv_header_string = ""
    tauSpinnerWeight_steps = ["000", "010", "020", "030", "040", "050", "060", "070", "080", "090",
                              "100"]  # existing weights
    tauSpinnerWeight_addsteps = ["110", "120", "130", "140", "150", "160", "170", "180", "190",
                                 "200"]  # need to be calculated

    for step in tauSpinnerWeight_steps + tauSpinnerWeight_addsteps:
        csv_header_string += (str(step) + ",")
    for param in param_entry_list:
        csv_header_string += (str(param) + ",")
    # PhiStarCP gets added extra to not end on comma here
    csv_header_string += "PhiStarCP"
    for var in rmlv_entry_list:
        csv_header_string += "," + var + "Pt" + "," + var + "Eta" + "," + var + "Phi" + "," + var + "E"
    csv_train.write(csv_header_string + "\n")
    csv_valid.write(csv_header_string + "\n")

    counter = 0
    for f in filelist:
        counter += 1
        rootFile = ROOT.TFile(sample_directory + f, "read")
        tree = rootFile.Get("tt_nominal/ntuple")
        entries = tree.GetEntries()

        for i in tqdm(range(entries), desc="{} out of {}".format(counter, len(filelist)), unit="events"):
            tree.GetEntry(i)

            decayModeMVA_1 = tree.GetLeaf("decayModeMVA_1").GetValue()
            decayModeMVA_2 = tree.GetLeaf("decayModeMVA_2").GetValue()
            wt_000 = tree.GetLeaf("tauSpinnerWeight000").GetValue()
            wt_050 = tree.GetLeaf("tauSpinnerWeight050").GetValue()
            wt_100 = tree.GetLeaf("tauSpinnerWeight100").GetValue()

            # check weight and get CP sensitive variable
            weight = 0
            flipdecay = False

            # Decay channel: rho - rho
            if decayModeMVA_1 == 1 and decayModeMVA_2 == 1:
                PhiStarCP = tree.GetLeaf("recoPhiStarCPRhoMerged").GetValue()
                weight = 1

            # Decay channel: charged pion - a1
            if (decayModeMVA_1 == 0 and decayModeMVA_2 == 10) or (decayModeMVA_1 == 10 and decayModeMVA_2 == 0):
                PhiStarCP = tree.GetLeaf("recoPhiStarCPCombMergedHelrPVBS").GetValue()
                # sort decay channel by int size of decayModeMVA
                if decayModeMVA_1 < decayModeMVA_2:
                    flipdecay = True
                weight = 1

            # Decay channel: rho - a1
            if (decayModeMVA_1 == 1 and decayModeMVA_2 == 10) or (decayModeMVA_1 == 10 and decayModeMVA_2 == 1):
                PhiStarCP = 0
                # sort decay channel by int size of decayModeMVA
                if decayModeMVA_1 < decayModeMVA_2:
                    flipdecay = True
                weight = 1

            # Decay channel: a1 - a1
            if decayModeMVA_1 == 10 and decayModeMVA_2 == 10:
                PhiStarCP = 0
                weight = 1

            # filtering out entries only contraining ones
            if weight == 1 and wt_000 != 1 and PhiStarCP > -500:
                # prepare string
                csv_string = ""

                # looping tauSpinnerWeight
                for step in tauSpinnerWeight_steps:
                    tauSpinnerWeightxxx = tree.GetLeaf("tauSpinnerWeight" + step).GetValue()
                    csv_string += str(tauSpinnerWeightxxx) + ","

                # Generating additional weights for mixing range pi to 2*pi
                for addstep in tauSpinnerWeight_addsteps:
                    mixing_angle = float(addstep) / 100 * np.pi / 2
                    new_tauSpinnerWeightxxx = calc_tauSpinnerWeight(wt_000, wt_050, wt_100, mixing_angle)
                    csv_string += str(new_tauSpinnerWeightxxx) + ","

                if flipdecay:
                    # writing additional parameter
                    csv_string += str(tree.GetLeaf("decayModeMVA_2").GetValue()) + ","
                    csv_string += str(tree.GetLeaf("decayModeMVA_1").GetValue()) + ","
                    csv_string += str(tree.GetLeaf("simpleFitConverged").GetValue()) + ","
                    csv_string += str(tree.GetLeaf("reco_negyTauL").GetValue()) + ","
                    csv_string += str(tree.GetLeaf("reco_posyTauL").GetValue()) + ","
                    csv_string += str(tree.GetLeaf("q_2").GetValue()) + ","
                    csv_string += str(tree.GetLeaf("q_1").GetValue()) + ","
                    csv_string += str(tree.lep2LV.M2()) + ","
                    csv_string += str(tree.lep1LV.M2()) + ","
                    csv_string += str(PhiStarCP)  # dont end on comma here
                else:
                    # writing additional parameter
                    csv_string += str(tree.GetLeaf("decayModeMVA_1").GetValue()) + ","
                    csv_string += str(tree.GetLeaf("decayModeMVA_2").GetValue()) + ","
                    csv_string += str(tree.GetLeaf("simpleFitConverged").GetValue()) + ","
                    csv_string += str(tree.GetLeaf("reco_negyTauL").GetValue()) + ","
                    csv_string += str(tree.GetLeaf("reco_posyTauL").GetValue()) + ","
                    csv_string += str(tree.GetLeaf("q_1").GetValue()) + ","
                    csv_string += str(tree.GetLeaf("q_2").GetValue()) + ","
                    csv_string += str(tree.lep1LV.M2()) + ","
                    csv_string += str(tree.lep2LV.M2()) + ","
                    csv_string += str(PhiStarCP)  # dont end on comma here

                ### Reading in recontructed RMLV
                svfitTau1LV = tree.svfitTau1LV
                svfitTau2LV = tree.svfitTau2LV
                simpleFitTau1LV = tree.simpleFitTau1LV
                simpleFitTau2LV = tree.simpleFitTau2LV
                svfitneutrino1LV = tree.svfitTau1LV - tree.lep1LV
                svfitneutrino2LV = tree.svfitTau2LV - tree.lep2LV
                simpleFitneutrino1LV = tree.simpleFitTau1LV - tree.lep1LV
                simpleFitneutrino2LV = tree.simpleFitTau2LV - tree.lep2LV

                # Creating a boost M into the ZMF of the intermediate decay
                sum_of_LVs = tree.lep1SumChargedHadronsLV + tree.lep2SumChargedHadronsLV
                boostvec = sum_of_LVs.BoostToCM()
                M = ROOT.Math.Boost(boostvec.X(), boostvec.Y(), boostvec.Z())

                # boosting 4-vectors to the ZMF
                svfitTau1LV = M * svfitTau1LV
                svfitTau2LV = M * svfitTau2LV
                simpleFitTau1LV = M * simpleFitTau1LV
                simpleFitTau2LV = M * simpleFitTau2LV
                lep1LV = M * tree.lep1LV
                lep2LV = M * tree.lep2LV
                svfitneutrino1LV = M * svfitneutrino1LV
                svfitneutrino2LV = M * svfitneutrino2LV
                simpleFitneutrino1LV = M * simpleFitneutrino1LV
                simpleFitneutrino2LV = M * simpleFitneutrino2LV
                lep1SumChargedHadronsLV = M * tree.lep1SumChargedHadronsLV
                lep1SumNeutralHadronsLV = M * tree.lep1SumNeutralHadronsLV
                lep2SumChargedHadronsLV = M * tree.lep2SumChargedHadronsLV
                lep2SumNeutralHadronsLV = M * tree.lep2SumNeutralHadronsLV
                lep1ChargedHadronLV_1 = M * tree.lep1ChargedHadronLV_1
                lep1ChargedHadronLV_2 = M * tree.lep1ChargedHadronLV_2
                lep1ChargedHadronLV_3 = M * tree.lep1ChargedHadronLV_3
                lep2ChargedHadronLV_1 = M * tree.lep2ChargedHadronLV_1
                lep2ChargedHadronLV_2 = M * tree.lep2ChargedHadronLV_2
                lep2ChargedHadronLV_3 = M * tree.lep2ChargedHadronLV_3

                if flipdecay:
                    # creating list containing RMLVs
                    RMLV_list = [svfitTau2LV,
                                 svfitTau1LV,
                                 simpleFitTau2LV,
                                 simpleFitTau1LV,
                                 svfitneutrino2LV,
                                 svfitneutrino1LV,
                                 simpleFitneutrino2LV,
                                 simpleFitneutrino1LV,
                                 lep2LV,
                                 lep1LV,
                                 lep2SumChargedHadronsLV,
                                 lep2SumNeutralHadronsLV,
                                 lep1SumChargedHadronsLV,
                                 lep1SumNeutralHadronsLV,
                                 lep2ChargedHadronLV_1,
                                 lep2ChargedHadronLV_2,
                                 lep2ChargedHadronLV_3,
                                 lep1ChargedHadronLV_1,
                                 lep1ChargedHadronLV_2,
                                 lep1ChargedHadronLV_3]

                else:
                    # creating list containing RMLVs
                    RMLV_list = [svfitTau1LV,
                                 svfitTau2LV,
                                 simpleFitTau1LV,
                                 simpleFitTau2LV,
                                 svfitneutrino1LV,
                                 svfitneutrino2LV,
                                 simpleFitneutrino1LV,
                                 simpleFitneutrino2LV,
                                 lep1LV,
                                 lep2LV,
                                 lep1SumChargedHadronsLV,
                                 lep1SumNeutralHadronsLV,
                                 lep2SumChargedHadronsLV,
                                 lep2SumNeutralHadronsLV,
                                 lep1ChargedHadronLV_1,
                                 lep1ChargedHadronLV_2,
                                 lep1ChargedHadronLV_3,
                                 lep2ChargedHadronLV_1,
                                 lep2ChargedHadronLV_2,
                                 lep2ChargedHadronLV_3]


                # generate TVector3 for rotation
                rot_vec = copy.deepcopy(lep1SumChargedHadronsLV)
                TV3_list = []
                for rmlv in RMLV_list:
                    TV3 = ROOT.TVector3(rmlv.X(), rmlv.Y(), rmlv.Z())
                    TV3.RotateZ(0.5 * np.pi - rot_vec.Phi())
                    TV3.RotateX(rot_vec.Theta())
                    TV3_list.append(TV3)

                # write RMLV into csv with Pt Eta Phi
                for j in range(len(TV3_list)):
                    TV3 = TV3_list[j]
                    rmlv = RMLV_list[j]
                    new_rmlv = ROOT.Math.LorentzVector(ROOT.Math.PxPyPzM4D(float))(TV3.X(), TV3.Y(), TV3.Z(), rmlv.E())

                    csv_string += "," + str(new_rmlv.Pt())
                    csv_string += "," + str(new_rmlv.Eta())
                    csv_string += "," + str(new_rmlv.Phi())
                    csv_string += "," + str(new_rmlv.E())


                # write into csv file and split into train and validation data
                if i % 2 == 0:
                    csv_train.write(csv_string + "\n")
                else:
                    csv_valid.write(csv_string + "\n")

    csv_train.close()
    csv_valid.close()


def get_csv_genM():
    import ROOT
    from math import acos, cos, sin
    from tqdm import tqdm

    # check for old csv file, if it exist its getting deleted
    if os.path.exists(output_directory + "csv_" + version + "_train.csv"):
        os.remove(output_directory + "csv_" + version + "_train.csv")
        os.remove(output_directory + "csv_" + version + "_valid.csv")
        print("removed old csv file")

    # Settings
    filelist = [
        "GluGluHToTauTauUncorrelatedDecayFilteredM125_RunIIFall17MiniAODv2_PU2017_13TeV_MINIAOD_powheg-pythia8.root",
        "VBFHToTauTauUncorrelatedDecayFilteredM125_RunIIFall17MiniAODv2_PU2017_13TeV_MINIAOD_powheg-pythia8.root"]

    genMatched_rmlv_entry_list = ["genBosonLV",
                        "genMatchedTau1LV",
                        "genMatchedTau2LV",
                        "genMatchedTau1NeutrinoLV",
                        "genMatchedTau2NeutrinoLV",
                        "genMatchedLep1LV",
                        "genMatchedLep2LV",
                        "genMatchedTau1SumChargedHadronsLV",
                        "genMatchedTau1SumNeutralHadronsLV",
                        "genMatchedTau2SumChargedHadronsLV",
                        "genMatchedTau2SumNeutralHadronsLV",
                        "genMatchedTau1ChargedHadronLV_1",
                        "genMatchedTau1ChargedHadronLV_2",
                        "genMatchedTau1ChargedHadronLV_3",
                        "genMatchedTau2ChargedHadronLV_1",
                        "genMatchedTau2ChargedHadronLV_2",
                        "genMatchedTau2ChargedHadronLV_3",]

    genMatched_param_entry_list = ["decayModeMVA_1",
                                    "decayModeMVA_2",
                                    "genMacthed_negyTauL",
                                    "genMatched_posyTauL",
                                    "genQ_1",
                                    "genQ_2"]



    #defining variables, read in info from json file and open csv file
    print("Creating CSV file: ",version)
    csv_train = open(output_directory + "csv_" + version + "_train.csv", "w")
    csv_valid = open(output_directory + "csv_" + version + "_valid.csv", "w")

    # write csv header
    csv_header_string = ""
    tauSpinnerWeight_steps = ["000","010","020","030","040","050","060","070","080","090","100"] # existing weights
    tauSpinnerWeight_addsteps = ["110","120","130","140","150","160","170","180","190","200"] # need to be calculated
    for step in tauSpinnerWeight_steps + tauSpinnerWeight_addsteps:
        csv_header_string += (str(step) + ",")
    for param in genMatched_param_entry_list:
        csv_header_string += (str(param) + ",")
    # PhiStarCP gets added extra to not end on comma here
    csv_header_string += "genMatchedPhiStarCP"
    for var in genMatched_rmlv_entry_list:
        csv_header_string += "," + var + "Pt" + "," + var + "Eta" + "," + var + "Phi" + "," + var + "E"
    csv_train.write(csv_header_string + "\n")
    csv_valid.write(csv_header_string + "\n")

    counter = 0
    for f in filelist:
        counter += 1
        rootFile = ROOT.TFile(sample_directory + f, "read")
        tree = rootFile.Get("tt_nominal/ntuple")
        entries = tree.GetEntries()

        for i in tqdm(range(entries), desc="{} out of {}".format(counter, len(filelist)), unit="events"):
            tree.GetEntry(i)

            decayModeMVA_1 = tree.GetLeaf("decayModeMVA_1").GetValue()
            decayModeMVA_2 = tree.GetLeaf("decayModeMVA_2").GetValue()
            wt_000 = tree.GetLeaf("tauSpinnerWeight000").GetValue()
            wt_050 = tree.GetLeaf("tauSpinnerWeight050").GetValue()
            wt_100 = tree.GetLeaf("tauSpinnerWeight100").GetValue()

            # check weight and get CP sensitive variable
            # Scan decay for false entries
            weight = 0
            flipdecay = False

            # Decay channel: rho - rho
            if decayModeMVA_1 == 1 and decayModeMVA_2 == 1:
                PhiStarCP = tree.GetLeaf("genMatchedPhiStarCPRhoMerged").GetValue()
                weight = 1

            # Decay channel: charged pion - a1
            if (decayModeMVA_1 == 0 and decayModeMVA_2 == 10) or (decayModeMVA_1 == 10 and decayModeMVA_2 == 0):
                PhiStarCP = 0
                # sort decay channel by int size of decayModeMVA
                if decayModeMVA_1 < decayModeMVA_2:
                    flipdecay = True

                if tree.genMatchedLep1LV.E() < 9999.0 and tree.genMatchedLep2LV.E() < 9999.0 and tree.genMatchedTau1LV.E() < 9999.0 and tree.genMatchedTau2LV.E() < 9999.0 and tree.genMatchedTau2SumNeutralHadronsLV.E() == 0.0 and tree.genMatchedTau1SumNeutralHadronsLV.E() == 0.0:
                    if flipdecay:
                        if tree.genMatchedTau1ChargedHadronLV_1.E() < 9999.0:
                            weight = 1
                    if not flipdecay:
                        if tree.genMatchedTau2ChargedHadronLV_1.E() < 9999.0:
                            weight = 1

            # Decay channel: rho - a1
            if (decayModeMVA_1 == 1 and decayModeMVA_2 == 10) or (decayModeMVA_1 == 10 and decayModeMVA_2 == 1):
                PhiStarCP = 0
                # sort decay channel by int size of decayModeMVA
                if decayModeMVA_1 < decayModeMVA_2:
                    flipdecay = True

                if tree.genMatchedLep1LV.E() < 9999.0 and tree.genMatchedLep2LV.E() < 9999.0 and tree.genMatchedTau1LV.E() < 9999.0 and tree.genMatchedTau2LV.E() < 9999.0:
                    if flipdecay:
                        if tree.genMatchedTau2SumNeutralHadronsLV.E() == 0.0:
                            weight = 1
                    if not flipdecay:
                        if tree.genMatchedTau1SumNeutralHadronsLV.E() == 0.0:
                            weight = 1


            # Decay channel: a1 - a1
            if decayModeMVA_1 == 10 and decayModeMVA_2 == 10:
                PhiStarCP = 0

                if tree.genMatchedLep1LV.E() < 9999.0 and tree.genMatchedLep2LV.E() < 9999.0 and tree.genMatchedTau1SumNeutralHadronsLV.E() == 0.0 and tree.genMatchedTau2SumNeutralHadronsLV.E() == 0.0:
                    weight = 1

            #filtering out entries only contraining ones
            if weight == 1 and wt_000 != 1 and PhiStarCP > -500:

                ### Reading in recontructed RMLV
                # Creating a boost M into the ZMF of the intermediate decay
                sum_of_LVs = tree.genMatchedLep1LV + tree.genMatchedLep2LV
                boostvec = sum_of_LVs.BoostToCM()
                M = ROOT.Math.Boost(boostvec.X(),boostvec.Y(),boostvec.Z())

                # boosting 4-vectors to the ZMF
                genBosonLV = M * tree.genBosonLV
                genMatchedTau1LV = M * tree.genMatchedTau1LV
                genMatchedTau2LV = M * tree.genMatchedTau2LV
                genMatchedTau1NeutrinoLV = M * tree.genMatchedTau1NeutrinoLV
                genMatchedTau2NeutrinoLV = M * tree.genMatchedTau2NeutrinoLV
                genMatchedlep1LV = M * tree.genMatchedLep1LV
                genMatchedlep2LV = M * tree.genMatchedLep2LV
                genMatchedlep1SumChargedHadronsLV = M * tree.genMatchedTau1SumChargedHadronsLV
                genMatchedlep1SumNeutralHadronsLV = M * tree.genMatchedTau1SumNeutralHadronsLV
                genMatchedlep2SumChargedHadronsLV = M * tree.genMatchedTau2SumChargedHadronsLV
                genMatchedlep2SumNeutralHadronsLV = M * tree.genMatchedTau2SumNeutralHadronsLV
                genMatchedTau1ChargedHadronLV_1 = M * tree.genMatchedTau1ChargedHadronLV_1
                genMatchedTau1ChargedHadronLV_2 = M * tree.genMatchedTau1ChargedHadronLV_2
                genMatchedTau1ChargedHadronLV_3 = M * tree.genMatchedTau1ChargedHadronLV_3
                genMatchedTau2ChargedHadronLV_1 = M * tree.genMatchedTau2ChargedHadronLV_1
                genMatchedTau2ChargedHadronLV_2 = M * tree.genMatchedTau2ChargedHadronLV_2
                genMatchedTau2ChargedHadronLV_3 = M * tree.genMatchedTau2ChargedHadronLV_3

                if flipdecay:
                    # creating list containing RMLVs
                    RMLV_list = [genBosonLV,
                                genMatchedTau2LV,
                                genMatchedTau1LV,
                                genMatchedTau2NeutrinoLV,
                                genMatchedTau1NeutrinoLV,
                                genMatchedlep2LV,
                                genMatchedlep1LV,
                                genMatchedlep2SumChargedHadronsLV,
                                genMatchedlep2SumNeutralHadronsLV,
                                genMatchedlep1SumChargedHadronsLV,
                                genMatchedlep1SumNeutralHadronsLV,
                                genMatchedTau2ChargedHadronLV_1,
                                genMatchedTau2ChargedHadronLV_2,
                                genMatchedTau2ChargedHadronLV_3,
                                genMatchedTau1ChargedHadronLV_1,
                                genMatchedTau1ChargedHadronLV_2,
                                genMatchedTau1ChargedHadronLV_3]
                else:
                    # creating list containing RMLVs
                    RMLV_list = [genBosonLV,
                                genMatchedTau1LV,
                                genMatchedTau2LV,
                                genMatchedTau1NeutrinoLV,
                                genMatchedTau2NeutrinoLV,
                                genMatchedlep1LV,
                                genMatchedlep2LV,
                                genMatchedlep1SumChargedHadronsLV,
                                genMatchedlep1SumNeutralHadronsLV,
                                genMatchedlep2SumChargedHadronsLV,
                                genMatchedlep2SumNeutralHadronsLV,
                                genMatchedTau1ChargedHadronLV_1,
                                genMatchedTau1ChargedHadronLV_2,
                                genMatchedTau1ChargedHadronLV_3,
                                genMatchedTau2ChargedHadronLV_1,
                                genMatchedTau2ChargedHadronLV_2,
                                genMatchedTau2ChargedHadronLV_3]

                # generate TVector3 for rotation
                rot_vec = copy.deepcopy(genMatchedlep1LV)
                TV3_list = []
                for rmlv in RMLV_list:
                    TV3 = ROOT.TVector3(rmlv.X(),rmlv.Y(),rmlv.Z())
                    TV3.RotateZ(0.5*np.pi - rot_vec.Phi())
                    TV3.RotateX(rot_vec.Theta())
                    TV3_list.append(TV3)

                # prepare string
                csv_string = ""

                # looping tauSpinnerWeight
                for step in tauSpinnerWeight_steps:
                    tauSpinnerWeightxxx = tree.GetLeaf("tauSpinnerWeight"+step).GetValue()
                    csv_string += str(tauSpinnerWeightxxx) + ","

                # Generating additional weights for mixing range pi to 2*pi
                for addstep in tauSpinnerWeight_addsteps:
                    mixing_angle = float(addstep) / 100 * np.pi / 2
                    new_tauSpinnerWeightxxx = calc_tauSpinnerWeight(wt_000,wt_050,wt_100, mixing_angle)
                    csv_string += str(new_tauSpinnerWeightxxx) + ","

                if flipdecay:
                    # writing additional parameter
                    csv_string += str(tree.GetLeaf("decayModeMVA_2").GetValue()) + ","
                    csv_string += str(tree.GetLeaf("decayModeMVA_1").GetValue()) + ","
                    csv_string += str(tree.GetLeaf("genMatched_negyTauL").GetValue()) + ","
                    csv_string += str(tree.GetLeaf("genMatched_posyTauL").GetValue()) + ","
                    csv_string += str(tree.GetLeaf("genQ_2").GetValue()) + ","
                    csv_string += str(tree.GetLeaf("genQ_1").GetValue()) + ","
                    csv_string += str(PhiStarCP) # dont end on comma here
                else:
                    # writing additional parameter
                    csv_string += str(tree.GetLeaf("decayModeMVA_1").GetValue()) + ","
                    csv_string += str(tree.GetLeaf("decayModeMVA_2").GetValue()) + ","
                    csv_string += str(tree.GetLeaf("genMatched_negyTauL").GetValue()) + ","
                    csv_string += str(tree.GetLeaf("genMatched_posyTauL").GetValue()) + ","
                    csv_string += str(tree.GetLeaf("genQ_1").GetValue()) + ","
                    csv_string += str(tree.GetLeaf("genQ_2").GetValue()) + ","
                    csv_string += str(PhiStarCP) # dont end on comma here


                # write RMLV into csv with Pt Eta Phi
                for j in range(len(TV3_list)):
                    TV3 = TV3_list[j]
                    rmlv = RMLV_list[j]
                    new_rmlv = ROOT.Math.LorentzVector(ROOT.Math.PxPyPzM4D(float))(TV3.X(), TV3.Y(), TV3.Z(), rmlv.E())

                    csv_string += "," + str(new_rmlv.Pt())
                    csv_string += "," + str(new_rmlv.Eta())
                    csv_string += "," + str(new_rmlv.Phi())
                    csv_string += "," + str(new_rmlv.E())

                # write into csv file and split into train and validation data
                if i%2 == 0:
                    csv_train.write(csv_string + "\n")
                else:
                    csv_valid.write(csv_string + "\n")

    csv_train.close()
    csv_valid.close()



############################################################################################################
##########   input function converting dataframe to DNN input data       ###################################
############################################################################################################

def get_DNN_input(df):
    from keras.utils import to_categorical

    # filter out events with selected decay channel
    df = df.loc[((df["decayModeMVA_1"] == decay_channel[0]) & (df["decayModeMVA_2"] == decay_channel[1])) | (
            (df["decayModeMVA_1"] == decay_channel[1]) & (df["decayModeMVA_2"] == decay_channel[0]))]

    if is_MixingAngle_Multiclassing:
        # drop variables not used for DNN training
        var_skimmed = df.columns.values.tolist()
        var_drop = [item for item in var_skimmed if item not in var_list]
        df = df.drop(var_drop, axis=1)

        # remove entries with negative y_rho values
        # df = df.loc[(df["reco_negyTauL"] * df["reco_posyTauL"]) >= 0]

        # input rescaling
        var_skimmed = df.columns.values.tolist()
        var_remove = mixing_labels
        for i in var_remove:
            var_skimmed.remove(i)
        for v in var_skimmed:
            df[v] = (df[v] - df[v].mean()) / df[v].std()

        df = df.drop("200", axis=1)  # drop mixing angle 200

        # temporary
        if use_genmatched:
            df = df.drop("genMatchedPhiStarCP", axis=1)

        split_range = len(mixing_labels) - 1
        x = df.iloc[:, split_range:].values
        y = df.iloc[:, :split_range].values

        # one hot encode output layer
        y = np.argmax(y, axis=1)
        y = to_categorical(y, num_classes=20)

        return x, y

    if is_cp_binaryclassing:
        # drop variables not used for DNN training
        var_skimmed = df.columns.values.tolist()
        var_drop = [item for item in var_skimmed if item not in var_list]
        var_drop += [item for item in mixing_labels if item not in ["000", select_mixing]]
        df = df.drop(var_drop, axis=1)

        var_skimmed = df.columns.values.tolist()
        var_remove = ["000", select_mixing]
        for i in var_remove:
            var_skimmed.remove(i)
        for v in var_skimmed:
            df[v] = (df[v] - df[v].mean()) / df[v].std()

        split_range = 2
        x = df.iloc[:, split_range:].values
        y = df.iloc[:, :split_range].values

        # returns y with both weights
        return x, y

    if is_cpraw_binaryclassing:
        # drop variables not used for DNN training
        var_skimmed = df.columns.values.tolist()
        var_drop = [item for item in var_skimmed if item not in var_list]
        var_drop += [item for item in mixing_labels if item not in ["000", select_mixing]]
        df = df.drop(var_drop, axis=1)

        split_range = 2
        x = df.iloc[:, split_range:].values
        y = df.iloc[:, :split_range].values

        return x, y


############################################################################################################
##########   supporting definitions to use in the main parts of the code ###################################
############################################################################################################

# custom cross entropy loss function modelled after 1608.02609
def loss_loglikelihood(y_true, y_pred):
    import tensorflow.keras.backend as K
    return tf.reduce_mean(-(y_true * K.log(y_pred)))


def calc_tauSpinnerWeight(wt_000, wt_050, wt_100, angle):
    new_weight = wt_000 * (np.cos(angle) ** 2 - np.cos(angle) * np.sin(angle)) + wt_100 * (
            np.sin(angle) ** 2 - np.cos(angle) * np.sin(angle)) + wt_050 * (2 * np.cos(angle) * np.sin(angle))
    return new_weight


def fast_AUC_ROC_curve(y_pred, y_true, weighted=False, results=False):
    '''

    :param y_pred: Predicted probabilities of shape [n,2]
    :param y_true: True probabilities of shape [n,2]
    :param weighted: True: use y_pred as weights for AUC Score
    :param results: True: returns results: AUC Score
    :return:
    '''

    # defining variables needed for generating ROC curve
    score = []
    p = []
    weight = []

    # sort input array by possibilities
    full_array = np.zeros((len(y_pred), 4))
    full_array[:, 0:2] = y_pred
    full_array[:, 2:4] = y_true
    full_array = full_array[full_array[:, 0].argsort()]

    # bring data into necessary format
    if weighted:
        auc_label = "weightedAUC Score"

        for i in range(len(y_pred)):
            # model predicts X_i in A with probability p_i, contributes with weight wa
            score.append(1)
            p.append(full_array[i][0])
            weight.append(full_array[i][2])

            # model incorrectly predicts X_i in A with probability p_i, contributes with weight wb
            score.append(0)
            p.append(full_array[i][0])
            weight.append(full_array[i][3])

    else:
        auc_label = "AUC Score"

        for i in range(len(y_pred)):
            # simple classifier
            if full_array[i][2] >= 0.5:
                score.append(1)
            else:
                score.append(0)
            p.append(full_array[i][0])
            weight.append(1)

    fpr_list = []  # false-positive-rate
    tpr_list = []  # true-positive-rate
    tp = 0
    fp = 0
    tn = 0
    fn = 0

    # calculate initial fp and fp with lowest threshold possible (< min(p))
    # events can now only be classified as tp or fp
    for i in range(len(p)):
        if score[i] == 1:
            tp += weight[i]
        elif score[i] == 0:
            fp += weight[i]

    # tpr and fpr are in this case 1.0
    fpr_list.append(1.0)
    tpr_list.append(1.0)

    # iterate through given possibilities using each as ROC threshold
    # if initial result is 1, event changes from tp to fn
    # if initial result is 0, event changes from fp to tn

    for i in range(len(p)):
        if score[i] == 1:
            tp -= weight[i]
            fn += weight[i]
        elif score[i] == 0:
            fp -= weight[i]
            tn += weight[i]

        # catch exception of tpr,fpr = 0
        # and calculate tpr,fpr
        try:
            fpr = fp / (fp + tn)
        except ZeroDivisionError:
            fpr = 0
        try:
            tpr = tp / (tp + fn)
        except ZeroDivisionError:
            tpr = 0

        fpr_list.append(fpr)
        tpr_list.append(tpr)

    # calc area under ROC
    auc_score = 0
    for i in range(len(fpr_list) - 1):
        # Riemann-sum to calculate area under curve
        area = (fpr_list[i + 1] - fpr_list[i]) * tpr_list[i]
        # multiply result by -1, since x values are ordered from highest to lowest
        auc_score += area * (-1)

    if results:
        return auc_score
    else:
        print("Plotting ROC curve and {}...".format(auc_label))
        plt.figure()
        plt.title("ROC Curve | " + auc_label)
        plt.plot(fpr_list, tpr_list, color="red", label="{0:}: {1:.3f}".format(auc_label, auc_score))
        plt.plot([0, 1], [0, 1], color="black", ls="--")
        plt.xlim(0, 1)
        plt.ylim(0, 1)
        plt.xlabel("False Positive Rate")
        plt.ylabel("True Positive Rate")
        plt.legend()
        # plt.savefig(output_directory + version + "_" + method_label + "_" + tag + "_ROCCurve" + ".png")
        plt.show()


############################################################################################################
##########                          Plotting fuctions                    ###################################
############################################################################################################


# plot confusion matrix
def plot_confusion_matrix(confusion_matrix, even_or_odd):
    import seaborn

    label_str = ["0,", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17",
                 "18", "19"]
    seaborn.set(color_codes=True)
    plt.figure(1, figsize=(9, 6))
    plt.title(even_or_odd + " Model Confusion Matrix")
    seaborn.set(font_scale=1.)
    ax = seaborn.heatmap(confusion_matrix, cmap="YlGnBu", cbar_kws={'label': 'Scale'}, fmt='g')
    ax.set_xticklabels(label_str)
    ax.set_yticklabels(label_str)
    ax.set(ylabel="True Label", xlabel="Predicted Label")
    plt.savefig(output_directory + version + "_" + method_label + "_" + tag + "_confusionmatrix" + ".png",
                bbox_inches='tight',
                dpi=300)
    plt.close()


# plot loss accuracy on training
def plot_acc_loss(history):
    print("Plotting accuracy/loss ...")
    fig = plt.figure()
    ax1 = fig.add_subplot(211)
    ax2 = fig.add_subplot(212)

    ax1.plot(history.history['accuracy'], label="Training")
    ax1.plot(history.history['val_accuracy'], label="Validation")
    ax1.set_title(version)
    ax1.set_ylabel("accuracy")
    ax1.legend()

    ax2.plot(history.history['loss'], label="Training")
    ax2.plot(history.history['val_loss'], label="Validation")
    ax2.set_xlabel("epoch")
    ax2.set_ylabel("loss")
    ax2.legend()
    plt.savefig(output_directory + version + "_" + method_label + "_" + tag + "_accloss" + ".png")
    plt.close()


def plot_pred_diff(pred_labels, true_labels):
    print("Plotting class difference ...")

    class_diff = pred_labels - true_labels
    class_diff_mean = np.mean(class_diff)
    class_diff_std = np.std(class_diff)

    # Calculate class_diff with added symmetry (class 20 == class 0)
    class_diff_clipped = []
    for i in range(len(class_diff)):
        if abs(class_diff[i]) >= 10:
            diff = pred_labels[i] - true_labels[i]
            if diff > 0:
                class_diff_clipped.append(diff - 20)
            elif diff < 0:
                class_diff_clipped.append(diff + 20)
        else:
            class_diff_clipped.append(class_diff[i])

    class_diff_mean_clipped = np.mean(class_diff_clipped)
    class_diff_std_clipped = np.std(class_diff_clipped)

    bins = len(np.unique(class_diff))

    plt.figure()
    plt.hist(class_diff, histtype=u"step", bins=bins,
             label="mean [idx]: {:.3f}\nstd [idx]: {:.3f}\n{} [idx]: {:.3f}\n{} [idx]: {:.3f}".format(
                 class_diff_mean, class_diff_std, r"$mean_{sym}$", class_diff_mean_clipped, r"$std_{sym}$",
                 class_diff_std_clipped))
    plt.xlabel("$\Delta_{class}$")
    plt.xlim(min(class_diff), max(class_diff))
    plt.legend()
    plt.savefig(output_directory + version + "_" + method_label + "_" + tag + "_classdiff" + ".png")


def plot_pred_dist(pred_labels, true_labels):
    print("Plotting class distribution ...")

    acc_top1 = 0
    acc_top2 = 0
    acc_top3 = 0
    len_data = float(len(true_labels))
    for i in range(len(pred_labels)):
        if abs(pred_labels[i] - true_labels[i]) < 1:
            acc_top1 += 1
        if abs(pred_labels[i] - true_labels[i]) < 2:
            acc_top2 += 1
        if abs(pred_labels[i] - true_labels[i]) < 3:
            acc_top3 += 1

    plt.figure()
    plt.hist(pred_labels, histtype=u"step", bins=20, label="prediction", color="red")
    plt.hist(true_labels, histtype=u"step", bins=20, label="generation", color="black")
    plt.plot([], [], label="{}: {:.3f}\n{}: {:.3f}\n{}: {:.3f}".format(
        r"$\Delta_{class}^{0}$", acc_top1/len_data, r"$\Delta_{class}^{1}$", acc_top2/len_data, r"$\Delta_{class}^{2}$", acc_top3/len_data))
    plt.xlabel("$class index$")
    plt.legend()
    plt.savefig(output_directory + version + "_" + method_label + "_" + tag + "_classdist" + ".png")


############################################################################################################
##########                              DNN Methods                      ###################################
############################################################################################################


def run_DNN_mixingangle_multiclassing():
    from sklearn.model_selection import train_test_split

    print("reading in dataset...")
    df = pd.read_csv(output_directory + "csv_" + version + "_train.csv")
    print("starting data manipulation...")
    x, y = get_DNN_input(df)

    # control print
    print(x[1])
    print(y[1])

    # split samples into training and validation pool
    x_train, x_valid, y_train, y_valid = train_test_split(x, y, test_size=0.2, random_state=42)

    # define model
    print("start training:...")
    print("shape input: ", x_train.shape[1])

    # DNN Settings
    epochs = 50
    batch_size = 500
    dropout_rate = 0.15
    nodes = 800
    lr = 0.001

    model = tf.keras.Sequential()
    model.add(tf.keras.layers.Dense(nodes, input_dim=x_train.shape[1], activation="relu"))
    model.add(tf.keras.layers.Dropout(dropout_rate))

    model.add(tf.keras.layers.Dense(nodes, activation="relu"))
    model.add(tf.keras.layers.Dropout(dropout_rate))

    model.add(tf.keras.layers.Dense(nodes, activation="relu"))
    model.add(tf.keras.layers.Dropout(dropout_rate))

    model.add(tf.keras.layers.Dense(nodes, activation="relu"))
    model.add(tf.keras.layers.Dropout(dropout_rate))

    model.add(tf.keras.layers.Dense(nodes, activation="relu"))
    model.add(tf.keras.layers.Dropout(dropout_rate))

    model.add(tf.keras.layers.Dense(nodes, activation="relu"))
    model.add(tf.keras.layers.Dropout(dropout_rate))

    model.add(tf.keras.layers.Dense(y_train.shape[1], activation="softmax"))

    model.compile(loss="categorical_crossentropy", optimizer=tf.keras.optimizers.Adam(lr=lr),
                  metrics=["accuracy"])  #
    history = model.fit(x_train, y_train, validation_data=(x_valid, y_valid), verbose=1, epochs=epochs,
                        batch_size=batch_size)
    model.save(output_directory + version + "_" + method_label + "_" + tag + ".h5")
    return model, history


def run_DNN_spinweight_multiclassing():
    from sklearn.model_selection import train_test_split

    mixing_labels = ["000", "010", "020", "030", "040", "050", "060", "070", "080", "090", "100", "110", "120", "130",
                     "140", "150", "160", "170", "180", "190", "200"]

    print("reading in dataset:\n")
    df = pd.read_csv(output_directory + "csv_" + version + "_train.csv")
    print("starting data manipulation:\n")

    var_drop = ["decayModeMVA_2"]
    df = df.drop(var_drop, axis=1)

    # drop every unused variable before here
    var_skimmed = df.columns.values.tolist()
    var_remove = ["PhiStarCP"] + mixing_labels
    for i in var_remove:
        var_skimmed.remove(i)
    # input rescaling

    for v in var_skimmed:
        df[v] = (df[v] - df[v].mean()) / df[v].std()

    split_range = len(df.columns.values.tolist()) - len(mixing_labels)

    x = df.iloc[:, :split_range].values
    y = df.iloc[:, split_range:].values

    # apply Bayes probability
    for i in range(y.shape[0]):
        row_sum = np.sum(y[i, :])
        for j in range(y.shape[1]):
            y[i][j] = y[i][j] / row_sum

    x_train, x_valid, y_train, y_valid = train_test_split(x, y, test_size=0.2, random_state=42)

    print("start training:\n")
    # define model
    print("shape input", x_train.shape[1])
    model = tf.keras.Sequential()
    kernelinitializer = tf.keras.initializers.RandomNormal(mean=0., stddev=1.)
    model.add(
        tf.keras.layers.Dense(16, input_dim=x_train.shape[1], activation="relu", kernel_initializer=kernelinitializer))
    model.add(tf.keras.layers.Dropout(0.25))
    model.add(tf.keras.layers.Dense(32, activation="relu", kernel_initializer=kernelinitializer))
    model.add(tf.keras.layers.Dense(64, activation="relu", kernel_initializer=kernelinitializer))
    model.add(tf.keras.layers.Dense(y_train.shape[1], activation="softmax", kernel_initializer=kernelinitializer))

    # compiling the program by declaring the loss-function, the optimizer and the metrics
    model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])
    history = model.fit(x_train, y_train, validation_data=(x_valid, y_valid), verbose=1, epochs=10,
                        batch_size=100)  # ,batch_size = 100
    model.save(output_directory + version + "_" + method_label + "_" + tag + ".h5")
    return model, history


def run_DNN_cp_binaryclassing():
    from sklearn.model_selection import train_test_split
    from tensorflow.keras.utils import to_categorical

    print("reading in dataset...")
    df = pd.read_csv(output_directory + "csv_" + version + "_train.csv")
    print("starting data manipulation...")
    x, y = get_DNN_input(df)

    # test print for validation
    # print(x[1])
    # print(y[1])

    # apply Bayes probability
    for i in range(y.shape[0]):
        row_sum = np.sum(y[i, :])
        for j in range(y.shape[1]):
            y[i][j] = y[i][j] / row_sum

    # split samples into training and validation pool
    x_train, x_valid, y_train, y_valid = train_test_split(x, y, test_size=0.2, random_state=42)

    # define model
    print("start training...")
    print("shape input: ", x_train.shape[1])

    # DNN Settings
    epochs = 20
    batch_size = 100
    dropout_rate = 0.05
    nodes = 300
    lr = 0.001

    model = tf.keras.Sequential()
    model.add(tf.keras.layers.Dense(nodes, input_dim=x_train.shape[1], activation="relu"))
    model.add(tf.keras.layers.Dropout(dropout_rate))

    model.add(tf.keras.layers.Dense(nodes, activation="relu"))
    model.add(tf.keras.layers.Dropout(dropout_rate))

    model.add(tf.keras.layers.Dense(nodes, activation="relu"))
    model.add(tf.keras.layers.Dropout(dropout_rate))

    model.add(tf.keras.layers.Dense(nodes, activation="relu"))
    model.add(tf.keras.layers.Dropout(dropout_rate))

    model.add(tf.keras.layers.Dense(nodes, activation="relu"))
    model.add(tf.keras.layers.Dropout(dropout_rate))

    model.add(tf.keras.layers.Dense(nodes, activation="relu"))
    model.add(tf.keras.layers.Dropout(dropout_rate))

    model.add(tf.keras.layers.Dense(2, activation="softmax"))

    model.compile(loss="categorical_crossentropy", optimizer=tf.keras.optimizers.Adam(lr=lr), metrics=["mse"])
    history = model.fit(x_train, y_train, validation_data=(x_valid, y_valid), verbose=1, epochs=epochs,
                        batch_size=batch_size)
    model.save(output_directory + version + "_" + method_label + "_" + tag + ".h5")
    return model, history


def run_DNN_cpraw_binaryclassing():
    '''
    Empty, not used anymore
    '''


############################################################################################################
########## Main functionality of this code based on the previous defined supporting definitions   ##########
############################################################################################################


def do_training():
    # set DNN method here
    print("Train model on dataset")
    if is_MixingAngle_Multiclassing:
        model_train, history_train = run_DNN_mixingangle_multiclassing()
        print("plot loss and accuracy for both models")
        plot_acc_loss(history_train)

    if is_cp_binaryclassing:
        model_train, history_train = run_DNN_cp_binaryclassing()
    if is_cpraw_binaryclassing:
        run_DNN_cpraw_binaryclassing()
        return

    if chain_results:
        get_results()


def get_results():
    import numpy as np
    from sklearn.metrics import confusion_matrix
    from sklearn.metrics import roc_auc_score

    # load model and read in and shape test data
    model_train = keras.models.load_model(output_directory + version + "_" + method_label + "_" + tag + ".h5")
    df_valid = pd.read_csv(output_directory + "csv_" + version + "_valid.csv")
    x_valid, y_valid = get_DNN_input(df_valid)

    if is_MixingAngle_Multiclassing == True:
        # testing on Test data
        predictions = model_train.predict(x_valid)
        test_loss, test_acc = model_train.evaluate(x_valid, y_valid, verbose=1)
        print("\nAccuracy on model: {}".format(test_acc))

        # calculating and plotting confusion matrix
        pred_labels = np.argmax(predictions, axis=1)
        true_labels = np.argmax(y_valid, axis=1)

        plot_pred_diff(pred_labels, true_labels)
        plot_pred_dist(pred_labels, true_labels)

        cm = confusion_matrix(true_labels, pred_labels)
        cm = cm.astype("float") / cm.sum(axis=1)[:, np.newaxis]
        plot_confusion_matrix(cm, "evaluation")

    if is_cp_binaryclassing:
        # testing on Test data
        y_pred = model_train.predict(x_valid)

        # apply Bayes probability
        y_valid_bayes = y_valid
        for i in range(y_valid_bayes.shape[0]):
            row_sum = np.sum(y_valid_bayes[i, :])
            for j in range(y_valid_bayes.shape[1]):
                y_valid_bayes[i][j] = y_valid_bayes[i][j] / row_sum

        print("\nPred: | True:")
        for i in range(20):
            print("{y_pred[i, 0]:.3f}|{y_valid_bayes[i, 0]:.3f}")
        print("")

        oracle_prediction = fast_AUC_ROC_curve(y_valid_bayes, y_valid, weighted=True, results=True)
        weighted_auc_score = fast_AUC_ROC_curve(y_pred, y_valid, weighted=True, results=True)

        print("Oracle Prediction: {:.3f}".format(oracle_prediction))
        print("weightedAUC Score: {:.3f}".format(weighted_auc_score))


############################################################################################################
##########               Scripts for advanced analysis for automated process                      ##########
############################################################################################################

def script_runBinaryAll():
    '''
    Script to automatically run binary classification on all mixing angles and create plots for the finishing
    results

    :return:
    '''
    import copy

    # define global variables
    global select_mixing
    global tag
    global is_MixingAngle_Multiclassing
    global is_cp_binaryclassing
    global is_cpraw_binaryclassing
    global chain_results

    # Set correct DNN method
    is_MixingAngle_Multiclassing = False
    is_cpraw_binaryclassing = False
    is_cp_binaryclassing = True
    chain_results = False

    mixing_labels = ["010", "020", "030", "040", "050", "060", "070", "080", "090", "100", "110", "120", "130",
                     "140", "150", "160", "170", "180", "190", "200"]

    oracle_predictions = [0.5]
    weightedAUC_scores = [0.5]

    x_values = np.linspace(0.0, 2.0, 21)

    for mixing_angle in mixing_labels:
        print("\n### Run DNN Binary Classification for {} mixing label ###\n".format(mixing_angle))

        # Set tags for running mixing angle
        select_mixing = mixing_angle
        tag = "mixing" + mixing_angle

        # Execute the learning process
        do_training()

        # load model and read in and shape test data
        model_train = keras.models.load_model(output_directory + version + "_" + method_label + "_" + tag + ".h5")
        df_valid = pd.read_csv(output_directory + "csv_" + version + "_valid.csv")
        x_valid, y_valid = get_DNN_input(df_valid)

        # predict training data on model
        y_pred = model_train.predict(x_valid)

        # apply Bayes probability
        y_valid_bayes = copy.deepcopy(y_valid)
        for i in range(y_valid_bayes.shape[0]):
            row_sum = np.sum(y_valid_bayes[i, :])
            for j in range(y_valid_bayes.shape[1]):
                y_valid_bayes[i][j] = y_valid_bayes[i][j] / row_sum

        # evaluate score
        oracle_prediction = fast_AUC_ROC_curve(y_valid_bayes, y_valid, weighted=True, results=True)
        weightedAUC_score = fast_AUC_ROC_curve(y_pred, y_valid, weighted=True, results=True)

        oracle_predictions.append(oracle_prediction)
        weightedAUC_scores.append(weightedAUC_score)

        print("\nValidation of mixing angle ", mixing_angle)
        print("Oracle Prediction: {:.3f}".format(oracle_prediction))
        print("weightedAUC Score: {:.3f}".format(weightedAUC_score))

    plt.figure()
    plt.xlabel(r"$\alpha^{CP}$ in units of $\pi$")
    plt.ylabel(r"weightedAUC vs $\alpha^{CP} = 0.0$")
    plt.plot(x_values, oracle_predictions, ".", color="black", label="oracle predictions")
    plt.plot(x_values, weightedAUC_scores, ".", color="red", label="weightedAUC Score")
    plt.legend()
    plt.savefig(output_directory + version + "_" + "BinaryOracleCurve" + ".png")


def script_runOraclePrediction_DecayChannel():
    import copy
    '''
    Calculates the Oracle Prediction Curve for all available Decay Channels

    :return:
    '''

    decay_channel_list = [(1, 1), (0, 10), (1, 10), (10, 10)]
    decay_channel_label = ["Rho-Rho", "cPi-a1", "Rho-a1", "a1-a1"]

    # define global variables
    global select_mixing
    global tag
    global is_MixingAngle_Multiclassing
    global is_cp_binaryclassing
    global is_cpraw_binaryclassing
    global chain_results
    global decay_channel

    # Set correct DNN method
    is_MixingAngle_Multiclassing = False
    is_cpraw_binaryclassing = False
    is_cp_binaryclassing = True
    chain_results = False

    mixing_labels = ["010", "020", "030", "040", "050", "060", "070", "080", "090", "100", "110", "120", "130",
                     "140", "150", "160", "170", "180", "190", "200"]
    oracle_predictions_list = []
    x_values = np.linspace(0.0, 2.0, 21)

    for i in range(len(decay_channel_list)):
        print("\n### Run Oracle Prediction for {} decay channel ###\n".format(decay_channel_label[i]))

        oracle_predictions = [0.5]
        decay_channel = decay_channel_list[i]

        df = pd.read_csv(output_directory + "csv_" + version + "_train.csv")
        for mixing in mixing_labels:
            print("calculate oracle prediction for mixing label ", mixing)
            select_mixing = mixing
            x, y = get_DNN_input(df)

            # apply Bayes probability
            y_valid_bayes = copy.deepcopy(y)
            for i in range(y_valid_bayes.shape[0]):
                row_sum = np.sum(y_valid_bayes[i, :])
                for j in range(y_valid_bayes.shape[1]):
                    y_valid_bayes[i][j] = y_valid_bayes[i][j] / row_sum

            oracle_prediction = fast_AUC_ROC_curve(y_valid_bayes, y, weighted=True, results=True)
            oracle_predictions.append(oracle_prediction)

        oracle_predictions_list.append(oracle_predictions)

    plt.figure()
    plt.title(version)
    plt.xlabel(r"$\alpha^{CP}$ in units of $\pi$")
    plt.ylabel(r"Oracle vs $\alpha^{CP} = 0.0$")
    for j in range(len(decay_channel_list)):
        plt.plot(x_values, oracle_predictions_list[j], ".", label=decay_channel_label[j])
    plt.legend()
    plt.savefig(output_directory + version + "_" + "DecayChannelOracleCurve" + ".png")


################################################################################
def do_debug():


    import ROOT
    from math import acos, cos, sin
    from tqdm import tqdm

    # check for old csv file, if it exist its getting deleted
    if os.path.exists(output_directory + "csv_" + version + "_train.csv"):
        os.remove(output_directory + "csv_" + version + "_train.csv")
        os.remove(output_directory + "csv_" + version + "_valid.csv")
        print("removed old csv file")

    # Content
    filelist = ["GluGluHToTauTauUncorrelatedDecayFilteredM125_RunIIFall17MiniAODv2_PU2017_13TeV_MINIAOD_powheg-pythia8.root"]

    genMatched_rmlv_entry_list = [
                        "genMatchedTau1LV",
                        "genMatchedTau1NeutrinoLV",
                        "genMatchedLep1LV",
                        "genMatchedTau1SumChargedHadronsLV",
                        "genMatchedTau1SumNeutralHadronsLV",
                        "genMatchedTau1ChargedHadronLV_1",
                        "genMatchedTau1ChargedHadronLV_2",
                        "genMatchedTau1ChargedHadronLV_3",
                        "genMatchedTau2LV",
                        "genMatchedTau2NeutrinoLV",
                        "genMatchedLep2LV",
                        "genMatchedTau2SumChargedHadronsLV",
                        "genMatchedTau2SumNeutralHadronsLV",
                        "genMatchedTau2ChargedHadronLV_1",
                        "genMatchedTau2ChargedHadronLV_2",
                        "genMatchedTau2ChargedHadronLV_3",]

    genMatched_param_entry_list = ["decayModeMVA_1",
                                    "decayModeMVA_2"]



    #defining variables, read in info from json file and open csv file
    print("Creating CSV file: ",version)
    csv_train = open(output_directory + "csv_" + version + "_train.csv", "w")
    csv_valid = open(output_directory + "csv_" + version + "_valid.csv", "w")

    # write csv header
    csv_header_string = ""
    tauSpinnerWeight_steps = ["000","010","020","030","040","050","060","070","080","090","100"] # existing weights
    tauSpinnerWeight_addsteps = ["110","120","130","140","150","160","170","180","190","200"] # need to be calculated
    for step in tauSpinnerWeight_steps + tauSpinnerWeight_addsteps:
        csv_header_string += (str(step) + ",")
    for param in genMatched_param_entry_list:
        csv_header_string += (str(param) + ",")
    # PhiStarCP gets added extra to not end on comma here
    csv_header_string += "genMatchedPhiStarCP"
    for var in genMatched_rmlv_entry_list:
        csv_header_string += "," + var + "Pt" + "," + var + "Eta" + "," + var + "Phi" + "," + var + "E"
    csv_train.write(csv_header_string + "\n")
    csv_valid.write(csv_header_string + "\n")

    counter = 0
    for f in filelist:
        counter += 1
        rootFile = ROOT.TFile(sample_directory + f, "read")
        tree = rootFile.Get("tt_nominal/ntuple")
        entries = tree.GetEntries()

        for i in tqdm(range(entries), desc="{} out of {}".format(counter, len(filelist)), unit="events"):
            tree.GetEntry(i)

            decayModeMVA_1 = tree.GetLeaf("decayModeMVA_1").GetValue()
            decayModeMVA_2 = tree.GetLeaf("decayModeMVA_2").GetValue()
            wt_000 = tree.GetLeaf("tauSpinnerWeight000").GetValue()
            wt_050 = tree.GetLeaf("tauSpinnerWeight050").GetValue()
            wt_100 = tree.GetLeaf("tauSpinnerWeight100").GetValue()

            # check weight and get CP sensitive variable
            weight = 0
            flipdecay = False

            # Decay channel: charged pion - a1
            if (decayModeMVA_1 == 0 and decayModeMVA_2 == 10) or (decayModeMVA_1 == 10 and decayModeMVA_2 == 0):
                PhiStarCP = 0
                simpleFitConverged = tree.GetLeaf("simpleFitConverged").GetValue()
                # sort decay channel by int size of decayModeMVA
                if decayModeMVA_1 < decayModeMVA_2:
                    flipdecay = True
                weight = 1

            #filtering out entries only contraining ones
            if weight == 1 and wt_000 != 1 and PhiStarCP > -500 and simpleFitConverged == True:

                ### Reading in recontructed RMLV
                # Creating a boost M into the ZMF of the intermediate decay
                sum_of_LVs = tree.genMatchedLep1LV + tree.genMatchedLep2LV
                boostvec = sum_of_LVs.BoostToCM()
                M = ROOT.Math.Boost(boostvec.X(),boostvec.Y(),boostvec.Z())

                # boosting 4-vectors to the ZMF
                genMatchedTau1LV = M * tree.simpleFitTau1LV
                genMatchedTau2LV = M * tree.simpleFitTau2LV
                genMatchedTau1NeutrinoLV = M * tree.genMatchedTau1NeutrinoLV
                genMatchedTau2NeutrinoLV = M * tree.genMatchedTau2NeutrinoLV
                genMatchedlep1LV = M * tree.genMatchedLep1LV
                genMatchedlep2LV = M * tree.genMatchedLep2LV
                genMatchedTau1SumChargedHadronsLV = M * tree.genMatchedTau1SumChargedHadronsLV
                genMatchedTau1SumNeutralHadronsLV = M * tree.genMatchedTau1SumNeutralHadronsLV
                genMatchedTau2SumChargedHadronsLV = M * tree.genMatchedTau2SumChargedHadronsLV
                genMatchedTau2SumNeutralHadronsLV = M * tree.genMatchedTau2SumNeutralHadronsLV
                genMatchedTau1ChargedHadronLV_1 = M * tree.genMatchedTau1ChargedHadronLV_1
                genMatchedTau1ChargedHadronLV_2 = M * tree.genMatchedTau1ChargedHadronLV_2
                genMatchedTau1ChargedHadronLV_3 = M * tree.genMatchedTau1ChargedHadronLV_3
                genMatchedTau2ChargedHadronLV_1 = M * tree.genMatchedTau2ChargedHadronLV_1
                genMatchedTau2ChargedHadronLV_2 = M * tree.genMatchedTau2ChargedHadronLV_2
                genMatchedTau2ChargedHadronLV_3 = M * tree.genMatchedTau2ChargedHadronLV_3

                RMLV_tau1 = [genMatchedTau1LV,
                            genMatchedTau1NeutrinoLV,
                            genMatchedlep1LV,
                            genMatchedTau1SumChargedHadronsLV,
                            genMatchedTau1SumNeutralHadronsLV,
                            genMatchedTau1ChargedHadronLV_1,
                            genMatchedTau1ChargedHadronLV_2,
                            genMatchedTau1ChargedHadronLV_3]

                RMLV_tau2 = [genMatchedTau2LV,
                            genMatchedTau2NeutrinoLV,
                            genMatchedlep2LV,
                            genMatchedTau2SumChargedHadronsLV,
                            genMatchedTau2SumNeutralHadronsLV,
                            genMatchedTau2ChargedHadronLV_1,
                            genMatchedTau2ChargedHadronLV_2,
                            genMatchedTau2ChargedHadronLV_3]

                # Align ZMF along the z - axis
                # decay channels get rotated individually
                rot_vec = copy.deepcopy(genMatchedTau1LV)
                TV3_tau1 = []
                for rmlv in RMLV_tau1:
                    TV3 = ROOT.TVector3(rmlv.X(),rmlv.Y(),rmlv.Z())
                    TV3.RotateZ(0.5*np.pi - rot_vec.Phi())
                    TV3.RotateX(rot_vec.Theta())
                    TV3_tau1.append(TV3)

                rot_vec = copy.deepcopy(genMatchedTau2LV)
                TV3_tau2 = []
                for rmlv in RMLV_tau2:
                    TV3 = ROOT.TVector3(rmlv.X(),rmlv.Y(),rmlv.Z())
                    TV3.RotateZ(1.5*np.pi - rot_vec.Phi())
                    TV3.RotateX((rot_vec.Theta()-np.pi) * (-1))
                    TV3_tau2.append(TV3)

                # prepare string
                csv_string = ""

                # looping tauSpinnerWeight
                for step in tauSpinnerWeight_steps:
                    tauSpinnerWeightxxx = tree.GetLeaf("tauSpinnerWeight"+step).GetValue()
                    csv_string += str(tauSpinnerWeightxxx) + ","

                # Generating additional weights for mixing range pi to 2*pi
                for addstep in tauSpinnerWeight_addsteps:
                    mixing_angle = float(addstep) / 100 * np.pi / 2
                    new_tauSpinnerWeightxxx = calc_tauSpinnerWeight(wt_000,wt_050,wt_100, mixing_angle)
                    csv_string += str(new_tauSpinnerWeightxxx) + ","

                if flipdecay:
                    # writing additional parameter
                    csv_string += str(tree.GetLeaf("decayModeMVA_2").GetValue()) + ","
                    csv_string += str(tree.GetLeaf("decayModeMVA_1").GetValue()) + ","
                    csv_string += str(PhiStarCP) # dont end on comma here
                else:
                    # writing additional parameter
                    csv_string += str(tree.GetLeaf("decayModeMVA_1").GetValue()) + ","
                    csv_string += str(tree.GetLeaf("decayModeMVA_2").GetValue()) + ","
                    csv_string += str(PhiStarCP) # dont end on comma here

                if flipdecay:
                    # write RMLV into csv with (Pt, Eta, Phi, E)
                    for j in range(len(TV3_tau2)):
                        TV3 = TV3_tau2[j]
                        rmlv = RMLV_tau2[j]
                        new_rmlv = ROOT.Math.LorentzVector(ROOT.Math.PxPyPzM4D(float))(TV3.X(), TV3.Y(), TV3.Z(), rmlv.E())

                        csv_string += "," + str(new_rmlv.X())
                        csv_string += "," + str(new_rmlv.Y())
                        csv_string += "," + str(new_rmlv.Z())
                        csv_string += "," + str(new_rmlv.E())

                    # write RMLV into csv with (Pt, Eta, Phi, E)
                    for j in range(len(TV3_tau1)):
                        TV3 = TV3_tau1[j]
                        rmlv = RMLV_tau1[j]
                        new_rmlv = ROOT.Math.LorentzVector(ROOT.Math.PxPyPzM4D(float))(TV3.X(), TV3.Y(), TV3.Z(), rmlv.E())

                        csv_string += "," + str(new_rmlv.X())
                        csv_string += "," + str(new_rmlv.Y())
                        csv_string += "," + str(new_rmlv.Z())
                        csv_string += "," + str(new_rmlv.E())

                else:
                    # write RMLV into csv with (Pt, Eta, Phi, E)
                    for j in range(len(TV3_tau1)):
                        TV3 = TV3_tau1[j]
                        rmlv = RMLV_tau1[j]
                        new_rmlv = ROOT.Math.LorentzVector(ROOT.Math.PxPyPzM4D(float))(TV3.X(), TV3.Y(), TV3.Z(), rmlv.E())

                        csv_string += "," + str(new_rmlv.X())
                        csv_string += "," + str(new_rmlv.Y())
                        csv_string += "," + str(new_rmlv.Z())
                        csv_string += "," + str(new_rmlv.E())

                    # write RMLV into csv with (Pt, Eta, Phi, E)
                    for j in range(len(TV3_tau2)):
                        TV3 = TV3_tau2[j]
                        rmlv = RMLV_tau2[j]
                        new_rmlv = ROOT.Math.LorentzVector(ROOT.Math.PxPyPzM4D(float))(TV3.X(), TV3.Y(), TV3.Z(), rmlv.E())

                        csv_string += "," + str(new_rmlv.X())
                        csv_string += "," + str(new_rmlv.Y())
                        csv_string += "," + str(new_rmlv.Z())
                        csv_string += "," + str(new_rmlv.E())




                # write into csv file and split into train and validation data
                if i%2 == 0:
                    csv_train.write(csv_string + "\n")
                else:
                    csv_valid.write(csv_string + "\n")

    csv_train.close()
    csv_valid.close()


# Calling the different ports of the main code according to the parser
def main():
    args = parser()

    if args.csv:
        if use_genmatched:
            get_csv_genM()
        elif not use_genmatched:
            get_csv_reco()

    if args.training:
        do_training()

    if args.results:
        get_results()

    if args.debug:
        do_debug()


if __name__ == "__main__":
    main()
