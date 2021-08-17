'''
HiggsCP_DNN: Python code for the analysis of the CP-properties of the Higgs-Boson
author = Alexander Fenger
version = 1.0
'''
import os
import copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix

#####################################################################################
#   Meta Data
#####################################################################################

# Input defining values
# version and input will define the name of output files
# version and input need to have the same name as csv file
version = "GG_VBF_tt_full_boost2_rotz_PtEtaPhi"
tag = "reco-1.1"

# use generator information for 4-vectors
# True: use generator level information
use_genmatched = False
# Global defined Variables
decay_channel = (10.0, 10.0)  # Tuple: (decayModeMVA_1,decayModeMVA_2)
select_mixing = "100"  # the selected mixing angle for binary classification
chain_results = True  # True: validate DNN directly after training

# DNN Settings
# Settings are defined global
epochs = 50
batch_size = 512
dropout_rate = 0.20
bc_nodes = 300
mc_nodes = 800
lr = 1e-3
layer = 6

# Switches for different DNN methods
# select DNN method, only one at a time
is_MixingAngle_Multiclassing = True
is_spinweight_Multiclassing = False
is_cp_binaryclassing = False

# directory settings
# sample directory should contain target csv file
# output directory will store all outputs generated
sample_directory = "/net/scratch_cms3b/fenger/artus/HiggsCP_DNN/input/"
output_directory = "/net/scratch_cms3b/fenger/artus/HiggsCP_DNN/output/" + version + "/"

# feature list settings:
# features are set per decay mode, IDs for features are found below
feat_d1d1 = [7, 8, 9, 10, 101]
feat_d10d1 = [1, 2, 3, 9, 10, 101]
feat_d10d10 = [1, 2, 3, 4, 5, 6, 101]
feat_d10d0 = [1, 2, 3, 4, 16, 101]

#####################################################################################
#   Preparations for code
#####################################################################################

# create sub directory for version
if not os.path.isdir(output_directory):
    os.mkdir(output_directory)

# create label for DNN methods and decay channels
decay_label = "d" + str(int(decay_channel[0])) + "d" + str(int(decay_channel[1]))
if is_MixingAngle_Multiclassing:
    method_label = "MixingAngle_Multiclassing" + "_" + decay_label
if is_spinweight_Multiclassing:
    method_label = "spinweight_Multiclassing" + "_" + decay_label
if is_cp_binaryclassing:
    method_label = "CP_Binary" + "_" + decay_label

# Dictionary containing all usable input values
genM_dict = {1: "genMatchedTau1ChargedHadronLV_1",
             2: "genMatchedTau1ChargedHadronLV_2",
             3: "genMatchedTau1ChargedHadronLV_3",
             4: "genMatchedTau2ChargedHadronLV_1",
             5: "genMatchedTau2ChargedHadronLV_2",
             6: "genMatchedTau2ChargedHadronLV_3",
             7: "genMatchedTau1SumChargedHadronsLV",
             8: "genMatchedTau1SumNeutralHadronsLV",
             9: "genMatchedTau2SumChargedHadronsLV",
             10: "genMatchedTau2SumNeutralHadronsLV",
             11: "genMatchedTau1NeutrinoLV",
             12: "genMatchedTau2NeutrinoLV",
             13: "genMatchedTau1LV",
             14: "genMatchedTau2LV",
             15: "genIP1",
             16: "genIP2",
             17: "genMatchedlep1LV",
             18: "genMatchedlep2LV",
             101: "genMatchedPhiStarCP"}

reco_dict = {1: "lep1ChargedHadronLV_1",
             2: "lep1ChargedHadronLV_2",
             3: "lep1ChargedHadronLV_3",
             4: "lep2ChargedHadronLV_1",
             5: "lep2ChargedHadronLV_2",
             6: "lep2ChargedHadronLV_3",
             7: "lep1SumChargedHadronsLV",
             8: "lep1SumNeutralHadronsLV",
             9: "lep2SumChargedHadronsLV",
             10: "lep2SumNeutralHadronsLV",
             11: "lep1NeutrinoLV",
             12: "lep2NeutrinoLV",
             13: "simpleFitTau1LV",
             14: "simpleFitTau2LV",
             15: "IP_1",
             16: "IP_2",
             17: "lep1LV",
             18: "lep2LV",
             19: "svfitTau1LV",
             20: "svfitTau2LV",
             101: "PhiStarCP",
             102: "reco_negyTauL",
             103: "reco_posyTauL",
             104: "q_1",
             105: "q_2",
             106: "m2_1",
             107: "m2_2",
             108: "alpha_1",
             109: "alpha_2",
             110: "emiss_x",
             111: "emiss_y",
             112: "neutrino1_Pt",
             113: "neutrino1_Pz",
             114: "neutrino1_E",
             115: "neutrino1_Phi",
             116: "neutrino2_Pt",
             117: "neutrino2_Pz",
             118: "neutrino2_E",
             119: "neutrino2_Phi",
             120: "PhiStarCP_polvec",
             121: "polvec_c0",
             122: "polvec_c1",
             123: "polvec_c2",
             124: "polvec_angleTT",
             21: "polVecTau1Tau2PiSSFromRhoSimpleFit_1",
             22: "polVecTau1Tau2PiSSFromRhoSimpleFit_2",
             23: "polVecTau1Tau2PiHighPtSimpleFit_1",
             24: "polVecTau1Tau2PiHighPtSimpleFit_2",
             25: "polVecTau1VisTau2PiSSFromRhoSimpleFit_1",
             26: "polVecTau1VisTau2PiSSFromRhoSimpleFit_2",
             27: "polVecTau1VisTau2PiHighPtSimpleFit_1",
             28: "polVecTau1VisTau2PiHighPtSimpleFit_2"
             }

mixing_labels = ["000", "010", "020", "030", "040", "050", "060", "070", "080", "090", "100", "110", "120", "130",
                 "140", "150", "160", "170", "180", "190", "200"]

# generate LV list and parameter list
var_list = []
par_list = []
# Decay Channel Rho - Rho
if decay_channel[0] == 1 and decay_channel[1] == 1:
    # filter features based on datatype
    # RMLV < 100
    # Observable > 100
    var_list = [num for num in feat_d1d1 if num < 100]
    par_list = [num for num in feat_d1d1 if num > 100]

    # Map list content
    if use_genmatched:
        var_list = list(map(genM_dict.get, var_list))
        par_list = list(map(genM_dict.get, par_list))
    else:
        var_list = list(map(reco_dict.get, var_list))
        par_list = list(map(reco_dict.get, par_list))

# Decay Channel a1 - Rho
if decay_channel[0] == 10 and decay_channel[1] == 1:
    # filter features based on datatype
    # RMLV < 100
    # Observable > 100
    var_list = [num for num in feat_d10d1 if num < 100]
    par_list = [num for num in feat_d10d1 if num > 100]

    # Map list content
    if use_genmatched:
        var_list = list(map(genM_dict.get, var_list))
        par_list = list(map(genM_dict.get, par_list))
    else:
        var_list = list(map(reco_dict.get, var_list))
        par_list = list(map(reco_dict.get, par_list))

# Decay Channel a1 - a1
if decay_channel[0] == 10 and decay_channel[1] == 10:
    # filter features based on datatype
    # RMLV < 100
    # Observable > 100
    var_list = [num for num in feat_d10d10 if num < 100]
    par_list = [num for num in feat_d10d10 if num > 100]

    # Map list content
    if use_genmatched:
        var_list = list(map(genM_dict.get, var_list))
        par_list = list(map(genM_dict.get, par_list))
    else:
        var_list = list(map(reco_dict.get, var_list))
        par_list = list(map(reco_dict.get, par_list))

# Decay Channel a1 - cPi
if decay_channel[0] == 10 and decay_channel[1] == 0:
    # filter features based on datatype
    # RMLV < 100
    # Observable > 100
    var_list = [num for num in feat_d10d0 if num < 100]
    par_list = [num for num in feat_d10d0 if num > 100]

    # Map list content
    if use_genmatched:
        var_list = list(map(genM_dict.get, var_list))
        par_list = list(map(genM_dict.get, par_list))
    else:
        var_list = list(map(reco_dict.get, var_list))
        par_list = list(map(reco_dict.get, par_list))

for entry in var_list:
    par_list.append(entry + "Pt")
    par_list.append(entry + "Eta")
    par_list.append(entry + "Phi")
    par_list.append(entry + "E")
par_list = par_list + mixing_labels


# par_list contains all feature labels

#####################################################################################
#   input function converting dataframe to DNN input data
#####################################################################################

def get_DNN_input(df, return_weights=False):
    '''

    :param df: raw pandas dataframe
    :return: x,y: input features as numpy array
    '''
    # filter out events with selected decay channel
    df = df.loc[((df["decayModeMVA_1"] == decay_channel[0]) & (df["decayModeMVA_2"] == decay_channel[1])) | (
            (df["decayModeMVA_1"] == decay_channel[1]) & (df["decayModeMVA_2"] == decay_channel[0]))]

    # only pass events with successful neutrino approximation
    # df = df.loc[df["approx_neutrino"] == True]

    # data parser for classification: mixing angle and spinweights
    if is_MixingAngle_Multiclassing or is_spinweight_Multiclassing:
        # Drop every row containing NaN entries
        df = df.dropna(axis=0, how="any")

        # drop variables not used for DNN training
        par_skimmed = df.columns.values.tolist()
        par_drop = [item for item in par_skimmed if item not in par_list]
        df = df.drop(par_drop, axis=1)

        # input rescaling
        par_skimmed = df.columns.values.tolist()
        par_remove = mixing_labels  # exclude spinweights
        for i in par_remove:
            par_skimmed.remove(i)
        for v in par_skimmed:
            df[v] = (df[v] - df[v].mean()) / df[v].std()

        # drop mixing angle 200 from dataframe
        df = df.drop("200", axis=1)

        # split dataframe according to number of classes selected
        split_range = len(mixing_labels) - 1
        x = df.iloc[:, split_range:].values
        y = df.iloc[:, :split_range].values

        if return_weights:
            return x, y

        if is_MixingAngle_Multiclassing:
            # one hot encode output layer
            y = np.argmax(y, axis=1)
            y = to_categorical(y, num_classes=20)

        if is_spinweight_Multiclassing:
            # apply Bayes probability
            for i in range(y.shape[0]):
                row_sum = np.sum(y[i, :])
                for j in range(y.shape[1]):
                    y[i][j] = y[i][j] / row_sum

        return x, y

    if is_cp_binaryclassing:
        # Drop every row containing NaN entries
        df = df.dropna(axis=0, how="any")

        # drop variables not used for DNN training
        par_skimmed = df.columns.values.tolist()
        par_drop = [item for item in par_skimmed if item not in par_list]
        par_drop += [item for item in mixing_labels if item not in ["000", select_mixing]]
        df = df.drop(par_drop, axis=1)

        par_skimmed = df.columns.values.tolist()
        par_remove = ["000", select_mixing]
        for i in par_remove:
            par_skimmed.remove(i)
        for v in par_skimmed:
            df[v] = (df[v] - df[v].mean()) / df[v].std()

        split_range = 2
        x = df.iloc[:, split_range:].values
        y = df.iloc[:, :split_range].values

        # returns y with both weights
        return x, y


#####################################################################################
#    supporting definitions to use in the main parts of the code
#####################################################################################

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
        print("Writing ROC results into txt file")
        file = open(output_directory + version + "_" + method_label + "_" + tag + "_ROC.txt", "w")
        for i in range(len(fpr_list)):
            file_string = str(fpr_list[i]) + ";" + str(tpr_list[i])
            file.write(file_string + "\n")
        file.close()

    return auc_score


#####################################################################################
#    result generating function
#####################################################################################

def get_results():
    # load model and read in and shape test data
    model_train = keras.models.load_model(output_directory + version + "_" + method_label + "_" + tag + ".h5")

    df_valid = pd.read_csv(output_directory + "csv_" + version + "_valid.csv")
    x_valid, y_valid = get_DNN_input(df_valid, return_weights=True)

    # evaluating validation data
    y_pred = model_train.predict(x_valid)

    if is_MixingAngle_Multiclassing or is_spinweight_Multiclassing:
        # calculating and plotting confusion matrix
        pred_labels = np.argmax(y_pred, axis=1)
        true_labels = np.argmax(y_valid, axis=1)

        # calculating class difference results ith added symmetry (class 20 == class 0)
        class_diff = []
        n_class = y_pred.shape[1]
        for i in range(y_pred.shape[0]):
            idp = np.argmax(y_pred[i, :])
            idc = np.argmax(y_valid[i, :])

            delta_class = [abs(idp - idc), ((n_class - 1) - abs(idp - idc))]
            if abs(idp - idc) != 0:
                delta_class_sign_1 = (idp - idc) / abs(idp - idc)
            else:
                delta_class_sign_1 = 1
            if abs(idc - idp) != 0:
                delta_class_sign_2 = (idc - idp) / abs(idc - idp)
            else:
                delta_class_sign_2 = 1

            if delta_class[0] < delta_class[1]:
                class_diff.append(min(delta_class) * delta_class_sign_1)
            else:
                class_diff.append(min(delta_class) * delta_class_sign_2)

        class_diff_mean = np.mean(class_diff)
        class_diff_std = np.std(class_diff)

        print("##########\n")
        print("Class Difference Results: {:.3f} +- {:.3f}".format(class_diff_mean, class_diff_std))
        print("\n##########")
        # PLOTTING class diff distribution

    if is_cp_binaryclassing:
        # apply Bayes probability
        y_valid_bayes = copy.deepcopy(y_valid)
        for i in range(y_valid_bayes.shape[0]):
            row_sum = np.sum(y_valid_bayes[i, :])
            for j in range(y_valid_bayes.shape[1]):
                y_valid_bayes[i][j] = y_valid_bayes[i][j] / row_sum

        oracle_prediction = fast_AUC_ROC_curve(y_valid_bayes, y_valid, weighted=True)
        weighted_auc_score = fast_AUC_ROC_curve(y_pred, y_valid, weighted=True, results=True)
        print("##########\n")
        print("Oracle Prediction: {:.3f}".format(oracle_prediction))
        print("weightedAUC Score: {:.3f}".format(weighted_auc_score))
        print("\n##########")

    # Writing results into txt file
    print("Writing results into txt file")
    file = open(output_directory + version + "_" + method_label + "_" + tag + "_results.txt", "w")
    for i in range(y_valid.shape[0]):
        file_string = ""
        for j in range(y_valid.shape[1]):
            file_string += str(y_valid[i][j]) + ";"

        for j in range(y_pred.shape[1]):
            file_string += str(y_pred[i][j]) + ";"
        file.write(file_string + "\n")
    file.close()


#####################################################################################
#    DNN defining and training functions
#####################################################################################

def run_DNN():
    # Define Global Variables for settings
    global epochs
    global batch_size
    global dropout_rate
    global bc_nodes
    global mc_nodes
    global lr
    global layer
    nodes = 0
    initializer = tf.keras.initializers.random_normal()
    regularizer = tf.keras.regularizers.l1_l2()
    activity = tf.keras.regularizers.l1(0.0001)

    print("Reading in dataset")
    df = pd.read_csv(output_directory + "csv_" + version + "_train.csv")
    print("Starting data manipulation")
    x, y = get_DNN_input(df)

    # method defining DNN settings
    if is_spinweight_Multiclassing:
        loss_function = "kullback_leibler_divergence"
        nodes = mc_nodes
    if is_MixingAngle_Multiclassing:
        loss_function = "categorical_crossentropy"
        nodes = mc_nodes
    if is_cp_binaryclassing:
        loss_function = "categorical_crossentropy"
        nodes = bc_nodes

        # apply Bayes probability
        for i in range(y.shape[0]):
            row_sum = np.sum(y[i, :])
            for j in range(y.shape[1]):
                y[i][j] = y[i][j] / row_sum

    # split samples into training and validation pool
    x_train, x_valid, y_train, y_valid = train_test_split(x, y, test_size=0.2, random_state=42)

    # define model
    print("Start training")
    print("shape input: ", x_train.shape[1])

    # build DNN model
    model = tf.keras.Sequential()
    model.add(
        tf.keras.layers.Dense(nodes, input_dim=x_train.shape[1], activation="relu", kernel_initializer=initializer))
    model.add(tf.keras.layers.Dropout(dropout_rate))
    for i in range(layer - 1):
        model.add(tf.keras.layers.Dense(nodes, activation="relu", kernel_initializer=initializer))
        model.add(tf.keras.layers.Dropout(dropout_rate))
    model.add(tf.keras.layers.Dense(y_train.shape[1], activation="softmax", kernel_initializer=initializer))
    model.compile(loss=loss_function, optimizer=tf.keras.optimizers.Adam(lr=lr), metrics=["mse"])
    history = model.fit(x_train, y_train, validation_data=(x_valid, y_valid), verbose=1, epochs=epochs,
                        batch_size=batch_size)
    model.save(output_directory + version + "_" + method_label + "_" + tag + ".h5")
    return model, history


def do_training():
    # print DNN settings
    print("Train model on dataset: {}".format(version))
    print("Tag: {}".format(tag))
    print("Decay Channel: ({},{})".format(decay_channel[0], decay_channel[1]))
    print("Method: {}".format(method_label))
    if use_genmatched:
        print("Generator Level")
    else:
        print("Reco level")

    model_train, history_train = run_DNN()
    loss = history_train.history['loss']
    val_loss = history_train.history['val_loss']
    mse = history_train.history["mse"]
    val_mse = history_train.history["val_mse"]

    # Writing results into txt file
    print("Writing results into txt file")
    file = open(output_directory + version + "_" + method_label + "_" + tag + "_history.txt", "w")
    for i in range(len(loss)):
        file_string = str(loss[i]) + ";" + str(val_loss[i]) + ";" + str(mse[i]) + ";" + str(val_mse[i])
        file.write(file_string + "\n")
    file.close()

    if chain_results:
        get_results()


#####################################################################################
#    Scripts for advanced analysis and automated processes
#####################################################################################

def script_run_correlated():
    # read in data sample and DNN model
    model_train = keras.models.load_model(output_directory + version + "_" + method_label + "_" + tag + ".h5")
    df1 = pd.read_csv(output_directory + "csv_" + version + "_correlated" + "_train.csv")
    df2 = pd.read_csv(output_directory + "csv_" + version + "_correlated" + "_valid.csv")
    df_valid = pd.concat([df1, df2], axis=0, ignore_index=True)
    x_valid, y_valid = get_DNN_input(df_valid)

    # evaluating validation data
    y_pred = model_train.predict(x_valid)

    # Writing results into txt file
    print("Writing correlated results into txt file")
    file = open(output_directory + version + "_" + method_label + "_" + tag + "_correlated_results.txt", "w")
    for i in range(y_valid.shape[0]):
        file_string = ""
        for j in range(y_valid.shape[1]):
            file_string += str(y_valid[i][j]) + ";"

        for j in range(y_pred.shape[1]):
            file_string += str(y_pred[i][j]) + ";"
        file.write(file_string + "\n")
    file.close()


def script_run_oracle_curve():
    '''
    Script to automatically run binary classification on all mixing angles and create plots for the finishing
    results

    :return:
    '''
    import copy

    # define global variables
    global tag
    tag_base = copy.deepcopy(tag)
    global select_mixing
    global chain_results

    chain_results = False

    mixing_labels = ["010", "020", "030", "040", "050", "060", "070", "080", "090", "100", "110", "120", "130",
                     "140", "150", "160", "170", "180", "190", "200"]

    oracle_predictions = [0.5]
    weightedAUC_scores = [0.5]

    for mixing_angle in mixing_labels:
        print("\n### Run DNN Binary Classification for {} mixing label ###\n".format(mixing_angle))

        # Set tags for running mixing angle
        select_mixing = mixing_angle
        tag = tag_base + "_mixing" + mixing_angle

        # Execute the learning process
        do_training()

        # load model and read in and shape test data
        model_train = keras.models.load_model(output_directory + version + "_" + method_label + "_" + tag + ".h5")
        df_valid = pd.read_csv(output_directory + "csv_" + version + "_valid.csv")
        x_valid, y_valid = get_DNN_input(df_valid, return_weights=True)

        # evaluating validation data
        y_pred = model_train.predict(x_valid)

        # apply Bayes probability
        y_valid_bayes = copy.deepcopy(y_valid)
        for i in range(y_valid_bayes.shape[0]):
            row_sum = np.sum(y_valid_bayes[i, :])
            for j in range(y_valid_bayes.shape[1]):
                y_valid_bayes[i][j] = y_valid_bayes[i][j] / row_sum

        # evaluate score
        oracle_prediction = fast_AUC_ROC_curve(y_valid_bayes, y_valid, weighted=True, results=False)
        weightedAUC_score = fast_AUC_ROC_curve(y_pred, y_valid, weighted=True, results=False)

        oracle_predictions.append(oracle_prediction)
        weightedAUC_scores.append(weightedAUC_score)

        print("\nValidation of mixing angle ", mixing_angle)
        print("Oracle Prediction: {:.3f}".format(oracle_prediction))
        print("weightedAUC Score: {:.3f}".format(weightedAUC_score))

    # Writing results into txt file
    print("Writing oracle curve results into txt file")
    file = open(output_directory + version + "_" + method_label + "_" + tag + "_oracle_curve.txt", "w")
    for i in range(len(oracle_predictions)):
        file_string = ""
        file_string += str(oracle_predictions[i]) + ";" + str(weightedAUC_scores[i])
        file.write(file_string + "\n")
    file.close()


#####################################################################################
#    Example code for evaluation
#####################################################################################

# calculate additional spinweights
def calc_tauSpinnerWeight(wt_000, wt_050, wt_100, angle):
    new_weight = wt_000 * (np.cos(angle) ** 2 - np.cos(angle) * np.sin(angle)) + wt_100 * (
            np.sin(angle) ** 2 - np.cos(angle) * np.sin(angle)) + wt_050 * (2 * np.cos(angle) * np.sin(angle))
    return new_weight

# read in generated .txt outputs and return array
def read_txt_input(filename):
    # convert txt file to numpy array
    file = open(output_directory + filename, 'r').read().split('\n')
    cut_column = False

    array_as_list = []
    for line in file:
        array_as_list.append(line.split(";"))

    array_shape_x = len(array_as_list) - 1  # compensate empty line at the end
    array_shape_y = len(array_as_list[0])

    y = np.zeros((array_shape_x, array_shape_y))
    for i in range(array_shape_x):
        for j in range(array_shape_y):
            string_value = array_as_list[i][j].replace("'", "")
            if string_value == "":
                cut_column = True
                continue
            y[i][j] = float(string_value)

    if cut_column:
        y = y[:, :-1]
    return y


#####################################################################################
#    End Matter
#####################################################################################

def do_debug():
    # debug function, has dataframe ready
    df = pd.read_csv(output_directory + "csv_" + version + "_train.csv")


if __name__ == "__main__":
    do_training()
