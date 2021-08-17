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
'''

version = "GG_VBF_tt_full_boost4_rotz_PtEtaPhi_genM_Test"
use_genmatched = True  # True: use generator information for 4-vectors

#   Global variables defined by mode
mixing_labels = ["000", "010", "020", "030", "040", "050", "060", "070", "080", "090", "100", "110", "120", "130",
                 "140", "150", "160", "170", "180", "190", "200"]

#   the directory with the signal samples
sample_directory = "/net/scratch_cms3b/fenger/artus/HiggsCP_DNN/input/"
#   the directory to use for storing/ loading the csv dataset, model, and additional files
output_directory = "/net/scratch_cms3b/fenger/artus/HiggsCP_DNN/output/" + version + "/"

#   create sub directory for version
if not os.path.isdir(output_directory):
    os.mkdir(output_directory)

# calculate additional spinweights
def calc_tauSpinnerWeight(wt_000, wt_050, wt_100, angle):
    new_weight = wt_000 * (np.cos(angle) ** 2 - np.cos(angle) * np.sin(angle)) + wt_100 * (
            np.sin(angle) ** 2 - np.cos(angle) * np.sin(angle)) + wt_050 * (2 * np.cos(angle) * np.sin(angle))
    return new_weight

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

    # features used for correlated samples
    is_cutstring = True

    filelist = [
        "GluGluHToTauTauM125_RunIIFall17MiniAODv2_PU2017newpmx_13TeV_MINIAOD_powheg-pythia8.root",
        "VBFHToTauTauM125_RunIIFall17MiniAODv2_PU2017newpmx_13TeV_MINIAOD_powheg-pythia8.root"]

    '''
    # Settings
    filelist = [
        "GluGluHToTauTauUncorrelatedDecayFilteredM125_RunIIFall17MiniAODv2_PU2017_13TeV_MINIAOD_powheg-pythia8.root",
        "VBFHToTauTauUncorrelatedDecayFilteredM125_RunIIFall17MiniAODv2_PU2017_13TeV_MINIAOD_powheg-pythia8.root"]
    '''

    #   Full list of all features in the csv file
    rmlv_entry_list = ["svfitTau1LV",
                        "simpleFitTau1LV",
                        "lep1LV",
                        "lep1SumChargedHadronsLV",
                        "lep1SumNeutralHadronsLV",
                        "lep1ChargedHadronLV_1",
                        "lep1ChargedHadronLV_2",
                        "lep1ChargedHadronLV_3",
                        "IP_1",
                        "polarimetricVectorsTauOneProngTauA1SimpleFit_1",
                        "polarimetricVectorsOneProngA1SimpleFit_1",
                        "svfitTau2LV",
                        "simpleFitTau2LV",
                        "lep2LV",
                        "lep2SumChargedHadronsLV",
                        "lep2SumNeutralHadronsLV",
                        "lep2ChargedHadronLV_1",
                        "lep2ChargedHadronLV_2",
                        "lep2ChargedHadronLV_3",
                        "IP_2",
                        "polarimetricVectorsTauOneProngTauA1SimpleFit_2",
                        "polarimetricVectorsOneProngA1SimpleFit_2"]

    param_entry_list = ["decayModeMVA_1",
                        "decayModeMVA_2",
                        "simpleFitConverged",
                        "reco_negyTauL",
                        "reco_posyTauL",
                        "q_1",
                        "q_2",
                        "m2_1",
                        "m2_2",
                        "approx_neutrino",
                        "alpha_1",
                        "alpha_2",
                        "emiss_x",
                        "emiss_y",
                        "neutrino1_Pt",
                        "neutrino1_Pz",
                        "neutrino1_E",
                        "neutrino1_Phi",
                        "neutrino2_Pt",
                        "neutrino2_Pz",
                        "neutrino2_E",
                        "neutrino2_Phi",
                        "PhiStarCP_PolVec"]

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

            # Event selection through cuts
            # check weight and get CP sensitive variable
            # set decay Mode to a1 decay in first slot
            weight = 0
            cut_weight = 1
            flipdecay = False
            approx_neutrino = False

            # check cut string is one is unused
            if is_cutstring:
                cutstring = '(byVVLooseDeepTau2017v2p1VSe_2 > 0.5)*(byVVLooseDeepTau2017v2p1VSe_1 > 0.5)*(byVLooseDeepTau2017v2p1VSmu_2 > 0.5)*(byVLooseDeepTau2017v2p1VSmu_1 > 0.5)*(nbtag == 0)*(pt_1 > 40.0)*(pt_2 > 40.0)*( ((trg_doubletau_35_tightiso_tightid > 0.5) * (pt_1 > 40) * (pt_2 > 40)) || ((trg_doubletau_40_mediso_tightid > 0.5) * (pt_1 > 45) * (pt_2 > 45)) || ((trg_doubletau_40_tightiso > 0.5) * (pt_1 > 45) * (pt_2 > 45) ) )*(abs(eta_1) < 2.1)*(byMediumDeepTau2017v2p1VSjet_2 > 0.5)*(byMediumDeepTau2017v2p1VSjet_1 > 0.5)*((q_1*q_2)<0.0)*(abs(eta_2) < 2.1)'

                byVVLooseDeepTau2017v2p1VSe_2 = tree.GetLeaf("byVVLooseDeepTau2017v2p1VSe_2").GetValue()
                byVVLooseDeepTau2017v2p1VSe_1 = tree.GetLeaf("byVVLooseDeepTau2017v2p1VSe_1").GetValue()
                byVLooseDeepTau2017v2p1VSmu_2 = tree.GetLeaf("byVLooseDeepTau2017v2p1VSmu_2").GetValue()
                byVLooseDeepTau2017v2p1VSmu_1 = tree.GetLeaf("byVLooseDeepTau2017v2p1VSmu_1").GetValue()
                nbtag = tree.GetLeaf("nbtag").GetValue()
                pt_1 = tree.GetLeaf("pt_1").GetValue()
                pt_2 = tree.GetLeaf("pt_2").GetValue()
                trg_doubletau_35_tightiso_tightid = tree.GetLeaf("trg_doubletau_35_tightiso_tightid").GetValue()
                trg_doubletau_40_mediso_tightid = tree.GetLeaf("trg_doubletau_40_mediso_tightid").GetValue()
                trg_doubletau_40_tightiso = tree.GetLeaf("trg_doubletau_40_tightiso").GetValue()
                byMediumDeepTau2017v2p1VSjet_2 = tree.GetLeaf("byMediumDeepTau2017v2p1VSjet_2").GetValue()
                byMediumDeepTau2017v2p1VSjet_1 = tree.GetLeaf("byMediumDeepTau2017v2p1VSjet_1").GetValue()
                eta_1 = tree.GetLeaf("eta_1").GetValue()
                eta_2 = tree.GetLeaf("eta_2").GetValue()
                q_1 = tree.GetLeaf("q_1").GetValue()
                q_2 = tree.GetLeaf("q_2").GetValue()

                cutstring = cutstring.replace('&&', 'and')
                cutstring = cutstring.replace('||', 'or')
                cutstring = cutstring.replace('!', 'not')

                cut_weight = eval(cutstring)

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
                PhiStarCP = tree.GetLeaf("recoPhiStarCPCombMergedHelrPVBS").GetValue()
                # sort decay channel by int size of decayModeMVA
                if decayModeMVA_1 < decayModeMVA_2:
                    flipdecay = True
                weight = 1

            # Decay channel: a1 - a1
            if decayModeMVA_1 == 10 and decayModeMVA_2 == 10:
                PhiStarCP = tree.GetLeaf("recoPhiStarCPCombMergedHelrPVBS").GetValue()
                weight = 1

            # filtering out entries only contraining ones
            if weight == 1 and wt_000 != 1 and PhiStarCP > -500:


                ### Reading in recontructed RMLV
                svfitTau1LV = tree.svfitTau1LV
                svfitTau2LV = tree.svfitTau2LV
                simpleFitTau1LV = tree.simpleFitTau1LV
                simpleFitTau2LV = tree.simpleFitTau2LV

                # create 4vector of impact parameter vectors
                IP_1_ref = ROOT.Math.LorentzVector(ROOT.Math.PxPyPzM4D(float))(tree.IP_1.X(), tree.IP_1.Y(), tree.IP_1.Z(), 0)
                IP_2_ref = ROOT.Math.LorentzVector(ROOT.Math.PxPyPzM4D(float))(tree.IP_2.X(), tree.IP_2.Y(), tree.IP_2.Z(), 0)

                IP_1 = ROOT.Math.LorentzVector(ROOT.Math.PtEtaPhiM4D(float))(IP_1_ref.Pt(), IP_1_ref.Eta(), IP_1_ref.Phi(), 0)
                IP_2 = ROOT.Math.LorentzVector(ROOT.Math.PtEtaPhiM4D(float))(IP_2_ref.Pt(), IP_2_ref.Eta(), IP_2_ref.Phi(), 0)

                # approximating neutrino momenta - Part 1
                # calculating helpful parameters for later analysis

                # calculating missing transverse momentum
                met = tree.GetLeaf("met").GetValue()
                metphi = tree.GetLeaf("metphi").GetValue()

                emiss_x = met * np.cos(metphi)
                emiss_y = met * np.sin(metphi)

                p_had1_x = tree.lep1LV.X()
                p_had1_y = tree.lep1LV.Y()
                p_had2_x = tree.lep2LV.X()
                p_had2_y = tree.lep2LV.Y()

                alpha_2 = (emiss_y * p_had1_x - emiss_x * p_had1_y) / (p_had2_y * p_had1_x - p_had2_x * p_had1_y)
                alpha_1 = (emiss_x - alpha_2 * p_had2_x) / p_had1_x

                # Boost:
                # 1: on full generator level: tau ( and potentially visible decay porducts) into higgs restframe
                # 2: on full reconstruction level: visible decay products into combined restframe
                # 3: on full reconstruction level: visible decay products into intermediate charged decay products restframe
                # Creating a boost M into the ZMF of the intermediate decay
                sum_of_LVs = tree.lep1LV + tree.lep2LV
                boostvec = sum_of_LVs.BoostToCM()
                M = ROOT.Math.Boost(boostvec.X(), boostvec.Y(), boostvec.Z())

                # boosting 4-vectors to the ZMF
                svfitTau1LV = M * svfitTau1LV
                svfitTau2LV = M * svfitTau2LV
                simpleFitTau1LV = M * simpleFitTau1LV
                simpleFitTau2LV = M * simpleFitTau2LV
                genMatchedTau1NeutrinoLV = M * tree.genMatchedTau1NeutrinoLV
                genMatchedTau2NeutrinoLV = M * tree.genMatchedTau2NeutrinoLV
                lep1LV = M * tree.lep1LV
                lep2LV = M * tree.lep2LV
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
                IP_1 = M * IP_1
                IP_2 = M * IP_2

                # polarimetric vectors
                polarimetricVectorsTauOneProngTauA1SimpleFit_1_ref = ROOT.Math.LorentzVector(ROOT.Math.PxPyPzM4D(float))(tree.polarimetricVectorsTauOneProngTauA1SimpleFit_1.X(), tree.polarimetricVectorsTauOneProngTauA1SimpleFit_1.Y(), tree.polarimetricVectorsTauOneProngTauA1SimpleFit_1.Z(), 0)
                polarimetricVectorsTauOneProngTauA1SimpleFit_1 = ROOT.Math.LorentzVector(ROOT.Math.PtEtaPhiM4D(float))(polarimetricVectorsTauOneProngTauA1SimpleFit_1_ref.Pt(), polarimetricVectorsTauOneProngTauA1SimpleFit_1_ref.Eta(), polarimetricVectorsTauOneProngTauA1SimpleFit_1_ref.Phi(), 0)

                polarimetricVectorsTauOneProngTauA1SimpleFit_2_ref = ROOT.Math.LorentzVector(ROOT.Math.PxPyPzM4D(float))(tree.polarimetricVectorsTauOneProngTauA1SimpleFit_2.X(), tree.polarimetricVectorsTauOneProngTauA1SimpleFit_2.Y(), tree.polarimetricVectorsTauOneProngTauA1SimpleFit_2.Z(), 0)
                polarimetricVectorsTauOneProngTauA1SimpleFit_2 = ROOT.Math.LorentzVector(ROOT.Math.PtEtaPhiM4D(float))(polarimetricVectorsTauOneProngTauA1SimpleFit_2_ref.Pt(), polarimetricVectorsTauOneProngTauA1SimpleFit_2_ref.Eta(), polarimetricVectorsTauOneProngTauA1SimpleFit_2_ref.Phi(), 0)

                polarimetricVectorsOneProngA1SimpleFit_1_ref = ROOT.Math.LorentzVector(ROOT.Math.PxPyPzM4D(float))(tree.polarimetricVectorsOneProngA1SimpleFit_1.X(), tree.polarimetricVectorsOneProngA1SimpleFit_1.Y(), tree.polarimetricVectorsOneProngA1SimpleFit_1.Z(), 0)
                polarimetricVectorsOneProngA1SimpleFit_1 = ROOT.Math.LorentzVector(ROOT.Math.PtEtaPhiM4D(float))(polarimetricVectorsOneProngA1SimpleFit_1_ref.Pt(), polarimetricVectorsOneProngA1SimpleFit_1_ref.Eta(), polarimetricVectorsOneProngA1SimpleFit_1_ref.Phi(), 0)

                polarimetricVectorsOneProngA1SimpleFit_2_ref = ROOT.Math.LorentzVector(ROOT.Math.PxPyPzM4D(float))(tree.polarimetricVectorsOneProngA1SimpleFit_2.X(), tree.polarimetricVectorsOneProngA1SimpleFit_2.Y(), tree.polarimetricVectorsOneProngA1SimpleFit_2.Z(), 0)
                polarimetricVectorsOneProngA1SimpleFit_2 = ROOT.Math.LorentzVector(ROOT.Math.PtEtaPhiM4D(float))(polarimetricVectorsOneProngA1SimpleFit_2_ref.Pt(), polarimetricVectorsOneProngA1SimpleFit_2_ref.Eta(), polarimetricVectorsOneProngA1SimpleFit_2_ref.Phi(), 0)

                # creating list containing 1st decay
                RMLV_tau1 = [svfitTau1LV,
                             simpleFitTau1LV,
                             lep1LV,
                             lep1SumChargedHadronsLV,
                             lep1SumNeutralHadronsLV,
                             lep1ChargedHadronLV_1,
                             lep1ChargedHadronLV_2,
                             lep1ChargedHadronLV_3,
                             IP_1,
                             polarimetricVectorsTauOneProngTauA1SimpleFit_1,
                             polarimetricVectorsOneProngA1SimpleFit_1]


                # creating list containing 2nd decay
                RMLV_tau2 = [svfitTau2LV,
                             simpleFitTau2LV,
                             lep2LV,
                             lep2SumChargedHadronsLV,
                             lep2SumNeutralHadronsLV,
                             lep2ChargedHadronLV_1,
                             lep2ChargedHadronLV_2,
                             lep2ChargedHadronLV_3,
                             IP_2,
                             polarimetricVectorsTauOneProngTauA1SimpleFit_2,
                             polarimetricVectorsOneProngA1SimpleFit_2]


                # generate TVector3 for rotation
                # vector for rotation
                rot_vec = copy.deepcopy(lep1LV)

                TV3_tau1 = []
                for rmlv in RMLV_tau1:
                    TV3 = ROOT.TVector3(rmlv.X(), rmlv.Y(), rmlv.Z())
                    TV3.RotateZ(0.5 * np.pi - rot_vec.Phi())
                    TV3.RotateX(rot_vec.Theta())
                    TV3_tau1.append(TV3)

                TV3_tau2 = []
                for rmlv in RMLV_tau2:
                    TV3 = ROOT.TVector3(rmlv.X(), rmlv.Y(), rmlv.Z())
                    TV3.RotateZ(0.5 * np.pi - rot_vec.Phi())
                    TV3.RotateX(rot_vec.Theta())
                    TV3_tau2.append(TV3)

                # approximating neutrino momenta - Part 2
                # now in boost frame
                m2_tau1 = tree.genMatchedTau1LV.M2()
                m2_tau2 = tree.genMatchedTau2LV.M2()
                e_had1 = RMLV_tau1[2].E()
                e_had2 = RMLV_tau2[2].E()
                pz_had1 = TV3_tau1[2].Z()
                pz_had2 = TV3_tau2[2].Z()

                # approx. pz_neutrino
                pz_neutrino1 = alpha_1 * pz_had1
                pz_neutrino2 = alpha_2 * pz_had2

                e_neutrino1 = (m2_tau1 - e_had1**2 + pz_had1**2 + 2 * pz_neutrino1 * pz_had1) / ( 2 * e_had1)
                e_neutrino2 = (m2_tau2 - e_had2**2 + pz_had2**2 + 2 * pz_neutrino2 * pz_had2) / ( 2 * e_had2)

                # use of absolute value to avoid negative root
                # needs exception case
                pt_neutrino1 = np.sqrt(abs(e_neutrino1**2 - pz_neutrino1**2))
                pt_neutrino2 = np.sqrt(abs(e_neutrino2**2 - pz_neutrino2**2))

                # exception cases, to validate approximation success
                if alpha_1 > 0 and alpha_2 > 0 and e_neutrino1 > 0 and e_neutrino2 > 0:
                    approx_neutrino = True

                # set negative transverse mommenta to 0
                if pt_neutrino1 < 0:
                    pt_neutrino1 = 0.0
                if pt_neutrino2 < 0:
                    pt_neutrino2 = 0.0

                ### PLACEHOLDER FOR NEUTRINO AZIMUTHAL ANGLE APPROXIMATION
                phi_neutrino1 = 0
                phi_neutrino2 = 0

                # Write results into csv file
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
                    # low level observables
                    csv_string += str(tree.GetLeaf("decayModeMVA_2").GetValue()) + ","
                    csv_string += str(tree.GetLeaf("decayModeMVA_1").GetValue()) + ","
                    csv_string += str(tree.GetLeaf("simpleFitConverged").GetValue()) + ","
                    csv_string += str(tree.GetLeaf("reco_negyTauL").GetValue()) + ","
                    csv_string += str(tree.GetLeaf("reco_posyTauL").GetValue()) + ","
                    csv_string += str(tree.GetLeaf("q_2").GetValue()) + ","
                    csv_string += str(tree.GetLeaf("q_1").GetValue()) + ","
                    csv_string += str(tree.lep2LV.M2()) + ","
                    csv_string += str(tree.lep1LV.M2()) + ","
                    # neutrino approximation
                    csv_string += str(approx_neutrino) + ","
                    csv_string += str(alpha_1) + ","
                    csv_string += str(alpha_2) + ","
                    csv_string += str(emiss_x) + ","
                    csv_string += str(emiss_y) + ","
                    csv_string += str(pt_neutrino2) + ","
                    csv_string += str(pz_neutrino2) + ","
                    csv_string += str(e_neutrino2) + ","
                    csv_string += str(phi_neutrino2) + ","
                    csv_string += str(pt_neutrino1) + ","
                    csv_string += str(pz_neutrino1) + ","
                    csv_string += str(e_neutrino1) + ","
                    csv_string += str(phi_neutrino1) + ","
                    # CP sensitive Observables
                    csv_string += str(tree.GetLeaf("recoPhiStarCPPolVecCombOneProngTauA1HelrPVBS").GetValue()) + ","
                    csv_string += str(PhiStarCP)  # dont end on comma here
                else:
                    # writing additional parameter
                    # low level observables
                    csv_string += str(tree.GetLeaf("decayModeMVA_1").GetValue()) + ","
                    csv_string += str(tree.GetLeaf("decayModeMVA_2").GetValue()) + ","
                    csv_string += str(tree.GetLeaf("simpleFitConverged").GetValue()) + ","
                    csv_string += str(tree.GetLeaf("reco_negyTauL").GetValue()) + ","
                    csv_string += str(tree.GetLeaf("reco_posyTauL").GetValue()) + ","
                    csv_string += str(tree.GetLeaf("q_1").GetValue()) + ","
                    csv_string += str(tree.GetLeaf("q_2").GetValue()) + ","
                    csv_string += str(tree.lep1LV.M2()) + ","
                    csv_string += str(tree.lep2LV.M2()) + ","
                    # neutrino approximation
                    csv_string += str(approx_neutrino) + ","
                    csv_string += str(alpha_1) + ","
                    csv_string += str(alpha_2) + ","
                    csv_string += str(emiss_x) + ","
                    csv_string += str(emiss_y) + ","
                    csv_string += str(pt_neutrino1) + ","
                    csv_string += str(pz_neutrino1) + ","
                    csv_string += str(e_neutrino1) + ","
                    csv_string += str(phi_neutrino1) + ","
                    csv_string += str(pt_neutrino2) + ","
                    csv_string += str(pz_neutrino2) + ","
                    csv_string += str(e_neutrino2) + ","
                    csv_string += str(phi_neutrino2) + ","
                    # CP sensitive Observables
                    csv_string += str(tree.GetLeaf("recoPhiStarCPPolVecCombOneProngTauA1HelrPVBS").GetValue()) + ","
                    csv_string += str(PhiStarCP)  # dont end on comma here


                # write RMLV into csv with Pt Eta Phi
                if flipdecay:
                    for j in range(len(TV3_tau2)):
                        TV3 = TV3_tau2[j]
                        rmlv = RMLV_tau2[j]
                        new_rmlv = ROOT.Math.LorentzVector(ROOT.Math.PxPyPzM4D(float))(TV3.X(), TV3.Y(), TV3.Z(), rmlv.E())

                        csv_string += "," + str(new_rmlv.Pt())
                        csv_string += "," + str(new_rmlv.Eta())
                        csv_string += "," + str(new_rmlv.Phi())
                        csv_string += "," + str(new_rmlv.E())

                    for j in range(len(TV3_tau1)):
                        TV3 = TV3_tau1[j]
                        rmlv = RMLV_tau1[j]
                        new_rmlv = ROOT.Math.LorentzVector(ROOT.Math.PxPyPzM4D(float))(TV3.X(), TV3.Y(), TV3.Z(), rmlv.E())

                        csv_string += "," + str(new_rmlv.Pt())
                        csv_string += "," + str(new_rmlv.Eta())
                        csv_string += "," + str(new_rmlv.Phi())
                        csv_string += "," + str(new_rmlv.E())

                else:
                    for j in range(len(TV3_tau1)):
                        TV3 = TV3_tau1[j]
                        rmlv = RMLV_tau1[j]
                        new_rmlv = ROOT.Math.LorentzVector(ROOT.Math.PxPyPzM4D(float))(TV3.X(), TV3.Y(), TV3.Z(), rmlv.E())

                        csv_string += "," + str(new_rmlv.Pt())
                        csv_string += "," + str(new_rmlv.Eta())
                        csv_string += "," + str(new_rmlv.Phi())
                        csv_string += "," + str(new_rmlv.E())

                    for j in range(len(TV3_tau2)):
                        TV3 = TV3_tau2[j]
                        rmlv = RMLV_tau2[j]
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


    # features used for correlated samples
    is_cutstring = False
    '''
    filelist = [
        "GluGluHToTauTauM125_RunIIFall17MiniAODv2_PU2017newpmx_13TeV_MINIAOD_powheg-pythia8.root",
        "VBFHToTauTauM125_RunIIFall17MiniAODv2_PU2017newpmx_13TeV_MINIAOD_powheg-pythia8.root"]

    '''

    # Settings
    filelist = [
        "GluGluHToTauTauUncorrelatedDecayFilteredM125_RunIIFall17MiniAODv2_PU2017_13TeV_MINIAOD_powheg-pythia8.root",
        "VBFHToTauTauUncorrelatedDecayFilteredM125_RunIIFall17MiniAODv2_PU2017_13TeV_MINIAOD_powheg-pythia8.root"]


    genMatched_rmlv_entry_list = [
                        "genMatchedTau1LV",
                        "genMatchedTau1NeutrinoLV",
                        "genMatchedLep1LV",
                        "genMatchedTau1SumChargedHadronsLV",
                        "genMatchedTau1SumNeutralHadronsLV",
                        "genMatchedTau1ChargedHadronLV_1",
                        "genMatchedTau1ChargedHadronLV_2",
                        "genMatchedTau1ChargedHadronLV_3",
                        "genIP1",
                        "genMatchedTau2LV",
                        "genMatchedTau2NeutrinoLV",
                        "genMatchedLep2LV",
                        "genMatchedTau2SumChargedHadronsLV",
                        "genMatchedTau2SumNeutralHadronsLV",
                        "genMatchedTau2ChargedHadronLV_1",
                        "genMatchedTau2ChargedHadronLV_2",
                        "genMatchedTau2ChargedHadronLV_3",
                        "genIP2"]

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
            # Scan decay for false entries
            weight = 0
            cut_weight = 1
            flipdecay = False
            approx_neutrino = False

            # check cut string is one is unused
            if is_cutstring:
                cutstring = '(byVVLooseDeepTau2017v2p1VSe_2 > 0.5)*(byVVLooseDeepTau2017v2p1VSe_1 > 0.5)*(byVLooseDeepTau2017v2p1VSmu_2 > 0.5)*(byVLooseDeepTau2017v2p1VSmu_1 > 0.5)*(nbtag == 0)*(pt_1 > 40.0)*(pt_2 > 40.0)*( ((trg_doubletau_35_tightiso_tightid > 0.5) * (pt_1 > 40) * (pt_2 > 40)) || ((trg_doubletau_40_mediso_tightid > 0.5) * (pt_1 > 45) * (pt_2 > 45)) || ((trg_doubletau_40_tightiso > 0.5) * (pt_1 > 45) * (pt_2 > 45) ) )*(abs(eta_1) < 2.1)*(byMediumDeepTau2017v2p1VSjet_2 > 0.5)*(byMediumDeepTau2017v2p1VSjet_1 > 0.5)*((q_1*q_2)<0.0)*(abs(eta_2) < 2.1)'

                byVVLooseDeepTau2017v2p1VSe_2 = tree.GetLeaf("byVVLooseDeepTau2017v2p1VSe_2").GetValue()
                byVVLooseDeepTau2017v2p1VSe_1 = tree.GetLeaf("byVVLooseDeepTau2017v2p1VSe_1").GetValue()
                byVLooseDeepTau2017v2p1VSmu_2 = tree.GetLeaf("byVLooseDeepTau2017v2p1VSmu_2").GetValue()
                byVLooseDeepTau2017v2p1VSmu_1 = tree.GetLeaf("byVLooseDeepTau2017v2p1VSmu_1").GetValue()
                nbtag = tree.GetLeaf("nbtag").GetValue()
                pt_1 = tree.GetLeaf("pt_1").GetValue()
                pt_2 = tree.GetLeaf("pt_2").GetValue()
                trg_doubletau_35_tightiso_tightid = tree.GetLeaf("trg_doubletau_35_tightiso_tightid").GetValue()
                trg_doubletau_40_mediso_tightid = tree.GetLeaf("trg_doubletau_40_mediso_tightid").GetValue()
                trg_doubletau_40_tightiso = tree.GetLeaf("trg_doubletau_40_tightiso").GetValue()
                byMediumDeepTau2017v2p1VSjet_2 = tree.GetLeaf("byMediumDeepTau2017v2p1VSjet_2").GetValue()
                byMediumDeepTau2017v2p1VSjet_1 = tree.GetLeaf("byMediumDeepTau2017v2p1VSjet_1").GetValue()
                eta_1 = tree.GetLeaf("eta_1").GetValue()
                eta_2 = tree.GetLeaf("eta_2").GetValue()
                q_1 = tree.GetLeaf("q_1").GetValue()
                q_2 = tree.GetLeaf("q_2").GetValue()

                cutstring = cutstring.replace('&&', 'and')
                cutstring = cutstring.replace('||', 'or')
                cutstring = cutstring.replace('!', 'not')

                cut_weight = eval(cutstring)

            # Decay channel: rho - rho
            if decayModeMVA_1 == 1 and decayModeMVA_2 == 1:
                PhiStarCP = tree.GetLeaf("genMatchedPhiStarCPRhoMerged").GetValue()
                # check for unlogical events
                if tree.genMatchedLep1LV.E() < 9999.0 and tree.genMatchedLep2LV.E() < 9999.0 and tree.genMatchedTau1LV.E() < 9999.0 and tree.genMatchedTau2LV.E() < 9999.0:
                    # check for standard value in PhiStarCP
                    if  PhiStarCP - np.pi/2.0 != 0:
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
            if weight*cut_weight != 0 and wt_000 != 1 and PhiStarCP > -500:

                ### Reading in recontructed RMLV
                # Creating a boost M into the ZMF of the intermediate decay
                sum_of_LVs = tree.genMatchedLep1LV + tree.genMatchedLep2LV
                boostvec = sum_of_LVs.BoostToCM()
                M = ROOT.Math.Boost(boostvec.X(),boostvec.Y(),boostvec.Z())

                # create 4vector of impact parameter vectors
                genIP1_ref = ROOT.Math.LorentzVector(ROOT.Math.PxPyPzM4D(float))(tree.genIP1.X(), tree.genIP1.Y(), tree.genIP1.Z(), 0)
                genIP2_ref = ROOT.Math.LorentzVector(ROOT.Math.PxPyPzM4D(float))(tree.genIP2.X(), tree.genIP2.Y(), tree.genIP2.Z(), 0)

                genIP1 = ROOT.Math.LorentzVector(ROOT.Math.PtEtaPhiM4D(float))(genIP1_ref.Pt(), genIP1_ref.Eta(), genIP1_ref.Phi(), 0)
                genIP2 = ROOT.Math.LorentzVector(ROOT.Math.PtEtaPhiM4D(float))(genIP2_ref.Pt(), genIP2_ref.Eta(), genIP2_ref.Phi(), 0)

                # boosting 4-vectors to the ZMF
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
                genIP1 = M * genIP1
                genIP2 = M * genIP2

                # creating list containing RMLVs
                RMLV_tau1 = [
                            genMatchedTau1LV,
                            genMatchedTau1NeutrinoLV,
                            genMatchedlep1LV,
                            genMatchedlep1SumChargedHadronsLV,
                            genMatchedlep1SumNeutralHadronsLV,
                            genMatchedTau1ChargedHadronLV_1,
                            genMatchedTau1ChargedHadronLV_2,
                            genMatchedTau1ChargedHadronLV_3,
                            genIP1]

                # creating list containing RMLVs
                RMLV_tau2 = [
                            genMatchedTau2LV,
                            genMatchedTau2NeutrinoLV,
                            genMatchedlep2LV,
                            genMatchedlep2SumChargedHadronsLV,
                            genMatchedlep2SumNeutralHadronsLV,
                            genMatchedTau2ChargedHadronLV_1,
                            genMatchedTau2ChargedHadronLV_2,
                            genMatchedTau2ChargedHadronLV_3,
                            genIP2]

                # generate TVector3 for rotation
                rot_vec = copy.deepcopy(genMatchedlep1LV)
                TV3_tau1 = []
                for rmlv in RMLV_tau1:
                    TV3 = ROOT.TVector3(rmlv.X(),rmlv.Y(),rmlv.Z())
                    TV3.RotateZ(0.5 * np.pi - rot_vec.Phi())
                    TV3.RotateX(rot_vec.Theta())
                    TV3_tau1.append(TV3)

                TV3_tau2 = []
                for rmlv in RMLV_tau2:
                    TV3 = ROOT.TVector3(rmlv.X(),rmlv.Y(),rmlv.Z())
                    TV3.RotateZ(0.5 * np.pi - rot_vec.Phi())
                    TV3.RotateX(rot_vec.Theta())
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


                # write RMLV into csv with Pt Eta Phi
                if flipdecay:
                    for j in range(len(TV3_tau2)):
                        TV3 = TV3_tau2[j]
                        rmlv = RMLV_tau2[j]
                        new_rmlv = ROOT.Math.LorentzVector(ROOT.Math.PxPyPzM4D(float))(TV3.X(), TV3.Y(), TV3.Z(), rmlv.E())

                        csv_string += "," + str(new_rmlv.Pt())
                        csv_string += "," + str(new_rmlv.Eta())
                        csv_string += "," + str(new_rmlv.Phi())
                        csv_string += "," + str(new_rmlv.E())

                    for j in range(len(TV3_tau1)):
                        TV3 = TV3_tau1[j]
                        rmlv = RMLV_tau1[j]
                        new_rmlv = ROOT.Math.LorentzVector(ROOT.Math.PxPyPzM4D(float))(TV3.X(), TV3.Y(), TV3.Z(), rmlv.E())

                        csv_string += "," + str(new_rmlv.Pt())
                        csv_string += "," + str(new_rmlv.Eta())
                        csv_string += "," + str(new_rmlv.Phi())
                        csv_string += "," + str(new_rmlv.E())

                else:
                    for j in range(len(TV3_tau1)):
                        TV3 = TV3_tau1[j]
                        rmlv = RMLV_tau1[j]
                        new_rmlv = ROOT.Math.LorentzVector(ROOT.Math.PxPyPzM4D(float))(TV3.X(), TV3.Y(), TV3.Z(), rmlv.E())

                        csv_string += "," + str(new_rmlv.Pt())
                        csv_string += "," + str(new_rmlv.Eta())
                        csv_string += "," + str(new_rmlv.Phi())
                        csv_string += "," + str(new_rmlv.E())

                    for j in range(len(TV3_tau2)):
                        TV3 = TV3_tau2[j]
                        rmlv = RMLV_tau2[j]
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

################################################################################
if __name__ == "__main__":
    if use_genmatched:
        get_csv_genM()
    elif not use_genmatched:
        get_csv_reco()
