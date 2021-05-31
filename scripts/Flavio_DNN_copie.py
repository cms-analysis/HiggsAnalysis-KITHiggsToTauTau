import os
import copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras

#User interface. Specify the following paths:


#   the version of execution in order not to overwrite previous files in the input/output directories
'''
# mt or tt: for simple or double hadronic decay mode
# decay channel: (1,2,10,11)
# Boost:
- 1: on full generator level: tau ( and potentially visible decay porducts) into higgs restframe
- 2: on full reconstruction level: visible decay products into combined restframe
- 3: on full reconstruction level: visible decay products into intermediate charged decay products restframe
# rot: align boosted 4vectors along z-axis

### implemented versions:
mva1_1_mva2_2

mixing_angle_multiclassing
ovr_binaryclassing
'''
################################
version = "tt_boost3_rot"
################################
#   use a unique tag to mark different DNN settings (only for plot saving important)
tag = "mixing_angle_multiclassing"

#   Global variables defined by mode
mixing_labels = ["000","010","020","030","040","050","060","070","080","090","100","110","120","130","140","150","160","170","180","190","200"]
chain_results = True # True: validate DNN directly after training
use_genmatched = False # True: use generator information for 4-vectors
decay_channel = (1,1) # Tuple: (decayModeMVA_1,decayModeMVA_2)
dnn_method = "mixing_angle_multiclassing"
select_mixing = "100" # the selected mixing angle for binary classification
threshhold_parameter = 0.5


#   the directory with the signal samples
sample_directory = "/net/scratch_cms3b/fenger/artus/2021_05_05/"
#   the directory to use for storing/ loading the csv dataset, model, and additional files
output_directory = "/net/scratch_cms3b/fenger/artus/2021_07_05/" + version + "/"


#   create sub directory for version
if os.path.isdir(output_directory) == False:
    os.mkdir(output_directory)


#    list of entry variables from root tree
tree_entry_list = ["svfitTau1LV",
                    "svfitTau2LV",
                    "lep1neutrinoLV",
                    "lep2neutrinoLV",
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
                    "lep2ChargedHadronLV_3",
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
                    "genMatchedTau2ChargedHadronLV_3"]


#   create variable list for DNN input
if decay_channel[0] == 1 and decay_channel[1] == 1:
    if use_genmatched == False:
        var_list = mixing_labels + ["PhiStarCP"]
        par_list = ["lep1neutrinoLV","lep2neutrinoLV","lep1SumChargedHadronsLV","lep1SumNeutralHadronsLV","lep2SumChargedHadronsLV","lep2SumNeutralHadronsLV"] #
    if use_genmatched == True:
        var_list = mixing_labels + ["PhiStarCP"]
        par_list = ["genMatchedTau1NeutrinoLV","genMatchedTau2NeutrinoLV","genMatchedTau1SumChargedHadronsLV","genMatchedTau1SumNeutralHadronsLV","genMatchedTau2SumChargedHadronsLV","genMatchedTau2SumNeutralHadronsLV"]
    for entry in par_list:
        var_list.append(entry + "E")
        var_list.append(entry + "Px")
        var_list.append(entry + "Py")
        var_list.append(entry + "Pz")


#A  rgument parser
def parser():
    import argparse

    parser = argparse.ArgumentParser(description="Script for LFV Analysis 2017. This code classifies a set of signal-background samples using a dnn. The result of classification on the form of a dnn_score is then appended to the root files and can then be used for statistical analysis.", formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("--csv", action = "store_true", help="Create csv file as DNN input")
    parser.add_argument("--training", action = "store_true", help="Train the DNN")
    parser.add_argument("--results", action = "store_true", help="get DNN results by application to the whole dataset")
    parser.add_argument("--attach", action = "store_true", help="attach DNN score to ROOT files")
    parser.add_argument("--debug", action = "store_true", help="debug code")
    return parser.parse_args()


#################    CSV Iput    ###########################################################################

def get_csv():
    import ROOT
    from math import acos, cos, sin
    from tqdm import tqdm

    # check for old csv file, if it exist its getting deleted
    if os.path.exists(output_directory + "csv_" + version + "_train.csv"):
        os.remove(output_directory + "csv_" + version + "_train.csv")
        os.remove(output_directory + "csv_" + version + "_valid.csv")
        print("removed old csv file")

    #Settings
    filelist = ["GluGluHToTauTauUncorrelatedDecayFilteredM125_RunIIFall17MiniAODv2_PU2017_13TeV_MINIAOD_powheg-pythia8.root"]
    tauSpinnerWeight_steps = ["000","010","020","030","040","050","060","070","080","090","100"] # existing weights
    tauSpinnerWeight_addsteps = ["110","120","130","140","150","160","170","180","190","200"] # need to be calculated

    #defining variables, read in info from json file and open csv file
    csv_train = open(output_directory + "csv_" + version + "_train.csv", "w")
    csv_valid = open(output_directory + "csv_" + version + "_valid.csv", "w")

    # write csv header
    csv_header_string = ""
    for step in tauSpinnerWeight_steps + tauSpinnerWeight_addsteps:
        csv_header_string += (str(step) + ",")
    csv_header_string += "decayModeMVA_1,decayModeMVA_2,PhiStarCP,genMatchedPhiStarCP" #do not end on comma here
    for var in tree_entry_list:
        csv_header_string += "," + var + "E" + "," + var + "Px" + "," + var + "Py" + "," + var + "Pz"
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
            # prepare string
            csv_string = ""

            decayModeMVA_1 = tree.GetLeaf("decayModeMVA_1").GetValue()
            decayModeMVA_2 = tree.GetLeaf("decayModeMVA_2").GetValue()
            wt_000 = tree.GetLeaf("tauSpinnerWeight000").GetValue()
            wt_050 = tree.GetLeaf("tauSpinnerWeight050").GetValue()
            wt_100 = tree.GetLeaf("tauSpinnerWeight100").GetValue()

            # check weight and get CP sensitive variable
            weight = 0
            if decay_channel[0] == 1 and decay_channel[1] == 1:
                PhiStarCP = tree.GetLeaf("recoPhiStarCPRhoMerged").GetValue()
                genMatchedPhiStarCP = tree.GetLeaf("genMatchedPhiStarCPRho").GetValue()
                weight = 1

            #filtering out entries only contraining ones
            if weight == 1 and wt_000 != 1 and PhiStarCP > -500:

                #looping tauSpinnerWeight
                for step in tauSpinnerWeight_steps:
                    tauSpinnerWeightxxx = tree.GetLeaf("tauSpinnerWeight"+step).GetValue()
                    csv_string += str(tauSpinnerWeightxxx) + ","

                #Generating additional weights for mixing range pi to 2*pi
                for addstep in tauSpinnerWeight_addsteps:
                    mixing_angle = float(addstep) / 100 * np.pi / 2
                    new_tauSpinnerWeightxxx = calc_tauSpinnerWeight(wt_000,wt_050,wt_100, mixing_angle)
                    csv_string += str(new_tauSpinnerWeightxxx) + ","

                # write CP sensitive variable and decay mode
                csv_string += str(tree.GetLeaf("decayModeMVA_1").GetValue()) + ","
                csv_string += str(tree.GetLeaf("decayModeMVA_2").GetValue()) + ","
                csv_string += str(PhiStarCP) + ","
                csv_string += str(genMatchedPhiStarCP) # dont end on comma here

                '''
                # defining 4-vector for impact parameter vector
                IP_1_ref = ROOT.Math.LorentzVector(ROOT.Math.PxPyPzM4D(float))(tree.IPHelrPVBS_1.X(), tree.IPHelrPVBS_1.Y(), tree.IPHelrPVBS_1.Z(), 0)
                IP_1 = ROOT.Math.LorentzVector(ROOT.Math.PtEtaPhiM4D(float))(IP_1_ref.Pt(), IP_1_ref.Eta(), IP_1_ref.Phi(), 0)
                '''
                ### Reading in recontructed RMLV
                # creating neutrino 4-vectos
                svfitTau1LV = tree.svfitTau1LV
                svfitTau2LV = tree.svfitTau2LV
                lep1neutrinoLV = tree.svfitTau1LV - tree.lep1LV
                lep2neutrinoLV = tree.svfitTau2LV - tree.lep2LV

                # Creating a boost M into the ZMF of the (charged1, charged2) decay
                sum_of_LVs = tree.lep1LV + tree.lep2LV
                boostvec = sum_of_LVs.BoostToCM()
                M = ROOT.Math.Boost(boostvec.X(),boostvec.Y(),boostvec.Z())

                # boosting 4-vectors to the ZMF
                svfitTau1LV = M * svfitTau1LV
                svfitTau2LV = M * svfitTau2LV
                lep1neutrinoLV = M * lep1neutrinoLV
                lep2neutrinoLV = M * lep2neutrinoLV
                lep1LV = M * tree.lep1LV
                lep2LV = M * tree.lep2LV
                lep1SumChargedHadronsLV = M * tree.lep1SumChargedHadronsLV
                lep1SumNeutralHadronsLV = M * tree.lep1SumNeutralHadronsLV
                lep2SumChargedHadronsLV = M * tree.lep2SumChargedHadronsLV
                lep2SumNeutralHadronsLV = M * tree.lep2SumNeutralHadronsLV

                # creating list containing RMLVs
                RMLV_list = [svfitTau1LV,svfitTau2LV,lep1neutrinoLV,lep2neutrinoLV,lep1LV,lep2LV,lep1SumChargedHadronsLV,lep1SumNeutralHadronsLV,lep2SumChargedHadronsLV,lep2SumNeutralHadronsLV]

                # generate TVector3 for rotation
                rot_vec = copy.deepcopy(lep1LV)
                TV3_list = []
                for rmlv in RMLV_list:
                    TV3 = ROOT.TVector3(rmlv.X(),rmlv.Y(),rmlv.Z())
                    TV3.RotateZ(0.5*np.pi - rot_vec.Phi())
                    TV3.RotateX(rot_vec.Theta())
                    TV3_list.append(TV3)

                # write 4-vectors into csv
                for j in range(len(TV3_list)):
                    rmlv = RMLV_list[j]
                    TV3 = TV3_list[j]

                    csv_string += "," + str(TV3.Px())
                    csv_string += "," + str(TV3.Py())
                    csv_string += "," + str(TV3.Pz())
                    csv_string += "," + str(rmlv.E())

                ### Reading in genMatched RMLV
                # creating neutrino 4-vectos
                genMatchedTau1LV = tree.genMatchedTau1LV
                genMatchedTau2LV = tree.genMatchedTau2LV
                lep1neutrinoLV = tree.genMatchedTau1LV - tree.genMatchedLep1LV
                lep2neutrinoLV = tree.genMatchedTau2LV - tree.genMatchedLep2LV

                # Creating a boost M into the ZMF of the (charged1, charged2) decay
                sum_of_LVs =  tree.genMatchedLep1LV + tree.genMatchedLep2LV
                boostvec = sum_of_LVs.BoostToCM()
                M = ROOT.Math.Boost(boostvec.X(),boostvec.Y(),boostvec.Z())

                # boosting 4-vectors to the ZMF
                svfitTau1LV = M * genMatchedTau1LV
                svfitTau2LV = M * genMatchedTau2LV
                lep1neutrinoLV = M * lep1neutrinoLV
                lep2neutrinoLV = M * lep2neutrinoLV
                lep1LV = M * tree.genMatchedLep1LV
                lep2LV = M * tree.genMatchedLep2LV
                lep1SumChargedHadronsLV = M * tree.genMatchedTau1SumChargedHadronsLV
                lep1SumNeutralHadronsLV = M * tree.genMatchedTau1SumNeutralHadronsLV
                lep2SumChargedHadronsLV = M * tree.genMatchedTau2SumChargedHadronsLV
                lep2SumNeutralHadronsLV = M * tree.genMatchedTau2SumNeutralHadronsLV

                # creating list containing RMLVs
                RMLV_list = [svfitTau1LV,svfitTau2LV,lep1neutrinoLV,lep2neutrinoLV,lep1LV,lep2LV,lep1SumChargedHadronsLV,lep1SumNeutralHadronsLV,lep2SumChargedHadronsLV,lep2SumNeutralHadronsLV]

                # generate TVector3 for rotation
                rot_vec = copy.deepcopy(lep1LV)
                TV3_list = []
                for rmlv in RMLV_list:
                    TV3 = ROOT.TVector3(rmlv.X(),rmlv.Y(),rmlv.Z())
                    TV3.RotateZ(0.5*np.pi - rot_vec.Phi())
                    TV3.RotateX(rot_vec.Theta())
                    TV3_list.append(TV3)

                # write 4-vectors into csv
                for j in range(len(TV3_list)):
                    rmlv = RMLV_list[j]
                    TV3 = TV3_list[j]

                    csv_string += "," + str(TV3.Px())
                    csv_string += "," + str(TV3.Py())
                    csv_string += "," + str(TV3.Pz())
                    csv_string += "," + str(rmlv.E())

                # write into csv file and split into train and validation data
                if i%2 == 0:
                    csv_train.write(csv_string + "\n")
                else:
                    csv_valid.write(csv_string + "\n")

    csv_train.close()
    csv_valid.close()



##########   supporting definitions to use in the main parts of the code ###################################

# custom cross entropy loss function modelled after 1608.02609
def loss_loglikelihood(y_true,y_pred):
    import keras.backend as K
    return -( (y_true * K.log(y_pred)) + ((1-y_true)*K.log(1-y_pred)) )


def calc_tauSpinnerWeight(wt_000,wt_050,wt_100,angle):
    new_weight = wt_000 * (np.cos(angle)**2 - np.cos(angle) * np.sin(angle)) + wt_100 * (np.sin(angle)**2 - np.cos(angle) * np.sin(angle)) + wt_050 * (2*np.cos(angle) * np.sin(angle))
    return new_weight


def get_DNN_input(df):
    from keras.utils import to_categorical

    if dnn_method == "mixing_angle_multiclassing":
        # drop variables not used for DNN training
        var_skimmed = df.columns.values.tolist()
        var_drop = [item for item in var_skimmed if item not in var_list]
        df = df.drop(var_drop, axis=1)

        '''
        #input rescaling
        var_skimmed = df.columns.values.tolist()
        var_remove =  ["PhiStarCP"] + mixing_labels
        for i in var_remove:
            var_skimmed.remove(i)

        for v in var_skimmed:
            df[v] = (df[v] - df[v].mean())/df[v].std()
        '''

        split_range = len(mixing_labels)
        x = df.iloc[:,split_range:].values
        y = df.iloc[:,:split_range].values

        # one hot encode output layer
        y = np.argmax(y,axis=1)
        y = to_categorical(y,num_classes = 21)

    if dnn_method == "ovr_binaryclassing":
        # drop variables not used for DNN training
        var_skimmed = df.columns.values.tolist()
        var_drop = [item for item in var_skimmed if item not in var_list]
        var_drop += [item for item in mixing_labels if item not in ["000",select_mixing]]
        df = df.drop(var_drop, axis=1)

        for v in df.columns.values.tolist():
            df[v] = (df[v] - df[v].mean())/df[v].std()

        mixing_index = mixing_labels.index(select_mixing)

        split_range = 2
        x = df.iloc[:,split_range:].values
        y = df.iloc[:,:split_range].values

        # apply Bayes probability
        for i in range(y.shape[0]):
            row_sum = np.sum(y[i,:])
            for j in range(y.shape[1]):
                y[i][j] = y[i][j] / row_sum

        # returns y with both probabilities

    return x,y


#plot confusion matrix
def plot_confusion_matrix(confusion_matrix, even_or_odd):
    import seaborn

    label_str = ["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21"]
    seaborn.set(color_codes=True)
    plt.figure(1, figsize=(9, 6))
    plt.title(even_or_odd + " Model Confusion Matrix")
    seaborn.set(font_scale=1.)
    ax = seaborn.heatmap(confusion_matrix, cmap="YlGnBu", cbar_kws={'label': 'Scale'}, fmt='g')
    ax.set_xticklabels(label_str)
    ax.set_yticklabels(label_str)
    ax.set(ylabel="True Label", xlabel="Predicted Label")
    plt.savefig(output_directory + "confusionmatrix_" + version + even_or_odd + "_" + tag +  ".png", bbox_inches='tight', dpi=300)
    plt.close()


#plot loss accuracy on training
def plot_acc_loss(history):
    print("Plotting accuracy/loss ...")
    fig = plt.figure()
    ax1 = fig.add_subplot(211)
    ax2 = fig.add_subplot(212)

    ax1.plot(history.history['acc'])
    ax1.plot(history.history['val_acc'])
    ax1.set_title(" Model")
    ax1.set_xlabel("epoch")
    ax1.set_ylabel("accuracy")
    ax1.legend()

    ax2.plot(history.history['loss'])
    ax2.plot(history.history['val_loss'])
    ax2.set_xlabel("epoch")
    ax2.set_ylabel("loss")
    ax2.legend()
    plt.savefig(output_directory + "loss_acc_" + version + "_" + tag +  ".png")
    plt.close()

def plot_pred_diff(pred_labels,true_labels):
    print("Plotting class difference ...")

    class_diff = pred_labels - true_labels
    class_diff_mean = np.mean(class_diff)
    class_diff_std = np.std(class_diff)

    plt.figure()
    plt.hist(class_diff,histtype = u"step",bins = 21,label = "mean [idx]: {}\nstd [idx]: {}".format(class_diff_mean,class_diff_std))
    plt.xlabel("$\Delta_{class}$")
    plt.legend()
    plt.savefig(output_directory + "classdiff_" + version + "_" + tag +  ".png")

def plot_pred_dist(pred_labels,true_labels):
    print("Plotting class distribution ...")
    plt.figure()
    plt.hist(pred_labels,histtype = u"step",bins = 21,label = "prediction",color="red")
    plt.hist(true_labels,histtype = u"step",bins = 21,label = "generation",color="black")
    plt.xlabel("$class index$")
    plt.legend()
    plt.savefig(output_directory + "classdist_" + version + "_" + tag +  ".png")

def plot_ROC_curve(y_valid,y_pred):
    print("Plotting ROC curve ...")
    len_y = len(y_valid)

    neg_roc = [] # false-positive-rate
    pos_roc = [] # true-positive-rate

    pos = 0
    neg = 0

    for i in range(len(y_valid)):
        # evaluating results
        if y_valid[i] == 1:
            if int(y_pred[i][0]) > threshhold_parameter:
                pos += 1
            elif int(y_pred[i][0]) < threshhold_parameter:
                neg += 1
        if y_valid[i] == 0:
            if int(y_pred[i][0]) < threshhold_parameter:
                pos += 1
            elif int(y_pred[i][0]) > threshhold_parameter:
                neg += 1

        neg_roc.append(neg)
        pos_roc.append(pos)

    neg_roc_array = np.array(neg_roc)
    pos_roc_array = np.array(pos_roc)

    plt.figure()
    plt.plot(neg_roc_array,pos_roc_array,color="red")
    plt.plot([0,neg],[0,pos],color="black",ls="--")
    #plt.xlim(0,1)
    #plt.ylim(0,1)
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.savefig(output_directory + "roc_curve_" + version + "_" + tag +  ".png")


###################### definitions for DNN building##############################


def run_DNN_mixingangle_multiclassing():
    from sklearn.model_selection import train_test_split
    from keras.utils import to_categorical
    from sklearn.utils import class_weight

    print("reading in dataset:\n")
    df= pd.read_csv(output_directory + "csv_" + version + "_train.csv")
    print("starting data manipulation:\n")

    x,y = get_DNN_input(df)
    print(x[1])
    print(y[1])

    # split samples into training and validation pool
    x_train, x_valid, y_train, y_valid = train_test_split(x, y, test_size=0.2, random_state=42)

    #define model
    print("start training:\n")
    print("shape input",x_train.shape[1])
    dropout_rate = 0.05
    nodes = 500

    model = tf.keras.Sequential()
    model.add(tf.keras.layers.Dense(nodes, input_dim=x_train.shape[1],activation="relu"))
    model.add(tf.keras.layers.Dropout(dropout_rate))

    model.add(tf.keras.layers.Dense(nodes,activation="relu"))
    model.add(tf.keras.layers.Dropout(dropout_rate))

    model.add(tf.keras.layers.Dense(nodes,activation="relu"))
    model.add(tf.keras.layers.Dropout(dropout_rate))

    model.add(tf.keras.layers.Dense(nodes,activation="relu"))
    model.add(tf.keras.layers.Dropout(dropout_rate))

    model.add(tf.keras.layers.Dense(nodes,activation="relu"))
    model.add(tf.keras.layers.Dropout(dropout_rate))

    model.add(tf.keras.layers.Dense(nodes,activation="relu"))
    model.add(tf.keras.layers.Dropout(dropout_rate))

    model.add(tf.keras.layers.Dense(y_train.shape[1], activation="softmax"))

    model.compile(loss="categorical_crossentropy", optimizer=tf.keras.optimizers.Adam(lr=0.001), metrics=["accuracy"])
    history = model.fit(x_train,y_train,validation_data=(x_valid,y_valid),verbose=1,epochs=20,batch_size = 500) #,batch_size = 5000
    model.save(output_directory + "model_" + version + "_" + tag + ".h5")
    return model, history


def DNN_spinweight_multiclassing():
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import roc_auc_score
    import keras.backend as K

    mixing_labels = ["000","010","020","030","040","050","060","070","080","090","100","110","120","130","140","150","160","170","180","190","200"]

    print("reading in dataset:\n")
    df= pd.read_csv(output_directory + "csv_" + version + "_train.csv")
    print("starting data manipulation:\n")

    var_drop = ["decayModeMVA_2"]
    df = df.drop(var_drop, axis=1)

    # drop every unused variable before here
    var_skimmed = df.columns.values.tolist()
    var_remove = ["PhiStarCP"] + mixing_labels
    for i in var_remove:
        var_skimmed.remove(i)
    #input rescaling

    for v in var_skimmed:
        df[v] = (df[v] - df[v].mean())/df[v].std()

    split_range = len(df.columns.values.tolist()) - len(mixing_labels)

    x = df.iloc[:,:split_range].values
    y = df.iloc[:,split_range:].values

    # apply Bayes probability
    for i in range(y.shape[0]):
        row_sum = np.sum(y[i,:])
        for j in range(y.shape[1]):
            y[i][j] = y[i][j] / row_sum

    x_train, x_valid, y_train, y_valid = train_test_split(x, y, test_size=0.2, random_state=42)

    print("start training:\n")
    #define model
    print("shape input",x_train.shape[1])
    model = tf.keras.Sequential()
    kernelinitializer = tf.keras.initializers.RandomNormal(mean = 0.,stddev = 1.)
    model.add(tf.keras.layers.Dense(16, input_dim=x_train.shape[1], activation="relu",kernel_initializer = kernelinitializer))
    model.add(tf.keras.layers.Dropout(0.25))
    model.add(tf.keras.layers.Dense(32,activation="relu",kernel_initializer = kernelinitializer))
    model.add(tf.keras.layers.Dense(64,activation="relu",kernel_initializer = kernelinitializer))
    model.add(tf.keras.layers.Dense(y_train.shape[1], activation="softmax",kernel_initializer = kernelinitializer))

    #compiling the program by declaring the loss-function, the optimizer and the metrics
    model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])
    history = model.fit(x_train,y_train ,validation_data=(x_valid,y_valid),verbose=1,epochs=10,batch_size = 100) #,batch_size = 100
    model.save(output_directory + "model_" + version + ".h5")
    return model, history


def run_DNN_ovr_binaryclassing():
    from sklearn.model_selection import train_test_split
    from keras.utils import to_categorical
    from sklearn.utils import class_weight

    print("reading in dataset:\n")
    df= pd.read_csv(output_directory + "csv_" + version + "_train.csv")
    print("starting data manipulation:\n")

    x,y = get_DNN_input(df)
    # test print for validation
    print(x[1])
    print(y[1])

    # convert bayes probabilities to one hot encoded vector
    y = y[:,0]

    # split samples into training and validation pool
    x_train, x_valid, y_train, y_valid = train_test_split(x, y, test_size=0.2, random_state=42)

    #define model
    print("start training:\n")
    print("shape input",x_train.shape[1])
    dropout_rate = 0.05
    nodes = 300

    model = tf.keras.Sequential()
    model.add(tf.keras.layers.Dense(nodes, input_dim=x_train.shape[1],activation="relu"))
    model.add(tf.keras.layers.Dropout(dropout_rate))

    model.add(tf.keras.layers.Dense(nodes,activation="relu"))
    model.add(tf.keras.layers.Dropout(dropout_rate))

    model.add(tf.keras.layers.Dense(nodes,activation="relu"))
    model.add(tf.keras.layers.Dropout(dropout_rate))

    model.add(tf.keras.layers.Dense(nodes,activation="relu"))
    model.add(tf.keras.layers.Dropout(dropout_rate))

    model.add(tf.keras.layers.Dense(nodes,activation="relu"))
    model.add(tf.keras.layers.Dropout(dropout_rate))

    model.add(tf.keras.layers.Dense(nodes,activation="relu"))
    model.add(tf.keras.layers.Dropout(dropout_rate))

    model.add(tf.keras.layers.Dense(1, activation="sigmoid"))

    model.compile(loss=loss_loglikelihood, optimizer=tf.keras.optimizers.Adam(lr=0.001), metrics=["accuracy"])
    history = model.fit(x_train,y_train,validation_data=(x_valid,y_valid),verbose=1,epochs=20,batch_size = 500) #,batch_size = 5000
    model.save(output_directory + "model_" + version + "_" + tag + ".h5")
    return model, history


def run_DNN_customBinary():
    from sklearn.model_selection import train_test_split
    from sklearn.utils import class_weight
    from sklearn.metrics import roc_auc_score

    # function to prep data for roc_auc_score input
    def prep_auc_score(pred, y_label):
    score = []
    p = []
    weight = []

    for i in range(len(pred)):
        # case (1,p_i,w_a)
        score.append(1)
        p.append(pred[i])
        weight.append(y_label[i][0])
        # case (0,p_i,w_b)
        score.append(0)
        p.append(pred[i])
        weight.append(y_label[i][1])
    return score, p, weight

    # Data preprocessing
    print("reading in dataset:\n")
    df = pd.read_csv(output_directory + "csv_" + version + "_train.csv")
    print("starting data manipulation:\n")
    x_train, y_train = get_DNN_input(df)

    # y_train is 2-dim with weight for 000 and selected mxining angle
    # test print for validation
    print(x_train[1])
    print(y_train[1])

    class NeuralNetwork(object):
        def __init__(self, num_features, batch_size, num_layers=6, size=300, lr=1e-3):
            # Each input x is represented by a given number of features
            # and corresponding weights for target distributions A and B.
            self.x = x = tf.compat.v1.placeholder(tf.float32, [batch_size, num_features])
            self.wa = wa = tf.compat.v1.placeholder(tf.float32, [batch_size])
            self.wb = wb = tf.compat.v1.placeholder(tf.float32, [batch_size])
            # The model will predict a single number, which is a probability of input x
            # belonging to class A. That probability is equal to wa / (wa + wb).
            y = wa / (wa + wb)
            y = tf.reshape(y, [-1, 1])

            # We apply multiple layers of transformations where each layer consists of
            # linearly transforming the features, followed by batch normalization (described above)
            # and ReLU nonlinearity (which is an elementwise operation: x -> max(x, 0))
            for i in range(num_layers):
                x = tf.nn.relu(batch_norm(linear(x, "linear_%d" % i, size), "bn_%d" % i))

            # Finally, the output is tranformed into a single number.
            # After applying sigmoid non-linearity (x -> 1 / (1 + exp(-x))) we’ll interpret that number
            # as a probability of x belonging to class A.
            x = linear(x, "regression", 1)
            self.p = tf.nn.sigmoid(x)

            # The objective to optimize is negative log likelihood under Bernoulli distribution:
            # loss = - (p(y==A) * log p(y==A|x) + p(y==B) * log p(y==B|x))
            self.loss = loss = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(logits=x, labels=y))
            # The model parameters are optimized using gradient-based Adam optimizer
            # (https://arxiv.org/abs/1412.6980) to minimize the loss on the training data.
            self.train_op = tf.compat.v1.train.AdamOptimizer(lr).minimize(loss)

            # initialize variables
            self.init_ops = tf.compat.v1.global_variables_initializer()

    # DNN settings :
    epochs = 10
    batch_size = 100 # Number of Samples per learning Batch
    num_layers = 6  # Number of Layers in Network
    size = 300  # Numbers of Nodes per Layer
    lr = 1e-3  # Learn rate for AdamOptimizer
    total_batch = int(len(y_train) / batch_size)  # Number of Batches per Input Data
    num_features = x_train.shape[1]  # Input Dimension

    # select input data in batches
    def get_batch(x_data, y_data, batch_size):
        idxs = np.random.randint(0, len(y_data), batch_size)
        return x_data[idxs, :], y_data[idxs, :]

    # Linearly transforms X of shape [batch_size, size1] into [batch_size, size].
    # Applies X -> XW + b, where W and b are trainable parameters.
    def linear(x, name, size, bias=True):
        w = tf.compat.v1.get_variable(name + "/W", [x.get_shape()[1], size], trainable=True)
        b = tf.compat.v1.get_variable(name + "/b", [1, size],
                                      initializer=tf.zeros_initializer, trainable=True)
        return tf.matmul(x, w) + b

    # Applies batch normalization trick from https://arxiv.org/abs/1502.03167
    # by normalizing each feature in a batch.
    def batch_norm(x, name):
        mean, var = tf.nn.moments(x, [0])
        normalized_x = (x - mean) * tf.compat.v1.rsqrt(var + 1e-8)
        gamma = tf.compat.v1.get_variable(name + "/gamma", [x.get_shape()[-1]],
                                          initializer=tf.constant_initializer(1.0))
        beta = tf.compat.v1.get_variable(name + "/beta", [x.get_shape()[-1]])
        return gamma * normalized_x + beta

    # Network Training
    tf.compat.v1.disable_eager_execution()
    sess = tf.compat.v1.Session()
    DNN = NeuralNetwork(num_features=num_features, batch_size=batch_size, num_layers=num_layers, size=size, lr=lr)

    sess.run(DNN.init_ops)
    for epoch in range(epochs):
        avg_loss = 0
        avg_auc = 0
        for i in range(total_batch):
            # select a batch of random events from the sample
            batch_x, batch_y = get_batch(x_train, y_train, batch_size=batch_size)

            # create dictionary to feed
            feed_dict = {DNN.x: batch_x, DNN.wa: batch_y[:, 0], DNN.wb: batch_y[:, 1]}

            # calculate loss and update the network
            loss = sess.run(DNN.loss, feed_dict=feed_dict)
            p = sess.run(DNN.p, feed_dict=feed_dict)
            sess.run(DNN.train_op, feed_dict=feed_dict)

            score, p_pred, weight = prep_auc_score(p, batch_y)

            auc = roc_auc_score(score, p_pred, sample_weight=weight)
            avg_loss += loss / total_batch
            avg_auc += auc / total_batch

        test_acc = 0
        print(f"Epoch: {epoch + 1}, loss={avg_loss:.3f}, auc={avg_auc:.3f}")
    print("\nTraining complete!")

    # Validate Trained Network
    # Reading in validation data and passing them through the network
    print("Validate Data")
    print("reading in dataset:")
    df = pd.read_csv(output_directory + "csv_" + version + "_valid.csv")
    print("starting data manipulation:")
    x_valid, y_valid = get_DNN_input(df)

    y_pred = []
    total_batch = int(len(y_valid) / batch_size)
    for i in range(total_batch):
        batch_x = x_valid[i:i + batch_size, :]
        batch_y = y_valid[i:i + batch_size, :]
        feed_dict = {DNN.x: batch_x, DNN.wa: batch_y[:, 0], DNN.wb: batch_y[:, 1]}
        p = sess.run(DNN.p, feed_dict=feed_dict)
        y_pred += p.tolist()

   # plot_ROC_curve(y_valid[:, 0], y_pred)
    score, p_pred, weight = prep_auc_score(y_pred, y_valid)
    final_auc_score = roc_auc_score(score, p_pred, sample_weight=weight)
    print("Final AUC Score: ", final_auc_score)
    sess.close()


########## Main functionality of this code based on the previous defined supporting definitions ##########

#call DNN training for even and odd dataset
def do_training():
    # set DNN method here
    print("Train model on dataset")
    if dnn_method == "mixing_angle_multiclassing":
        model_train, history_train = run_DNN_mixingangle_multiclassing()
    if dnn_method == "ovr_binaryclassing":
        model_train, history_train = run_DNN_ovr_binaryclassing()
    print("plot loss and accuracy for both models")
    plot_acc_loss(history_train)

    if chain_results == True:
        get_results()

#Get results on test dataset with confusion matrix and dnn_score-Plot
def get_results():
    import numpy as np
    from sklearn.metrics import confusion_matrix
    from sklearn.metrics import roc_auc_score
    from sklearn.metrics import log_loss

    #load model and read in and shape test data
    model_train = keras.models.load_model(output_directory + "model_" + version + "_" + tag + ".h5")
    df_valid = pd.read_csv(output_directory + "csv_" + version + "_valid.csv")
    x_valid, y_valid = get_DNN_input(df_valid)

    if dnn_method == "mixing_angle_multiclassing":
        #testing on Test data
        predictions = model_train.predict(x_valid)
        test_loss, test_acc = model_train.evaluate(x_valid, y_valid, verbose=1)
        print("\nAccuracy on model: {}".format(test_acc))

        #calculating and plotting confusion matrix
        pred_labels = np.argmax(predictions, axis=1)
        true_labels = np.argmax(y_valid, axis=1)

        plot_pred_diff(pred_labels,true_labels)
        plot_pred_dist(pred_labels,true_labels)

        cm = confusion_matrix(true_labels, pred_labels)
        cm = cm.astype("float") / cm.sum(axis=1)[:, np.newaxis]
        plot_confusion_matrix(cm, "evaluation")

    if dnn_method == "ovr_binaryclassing":
        y_bayes = copy.deepcopy(y_valid)

        #testing on Test data
        y_pred = model_train.predict(x_valid)

        y_bayes_wa = y_bayes[:,0]
        y_bayes_wb = y_bayes[:,1]

        plot_ROC_curve(y_valid,y_pred)

################################################################################

def do_debug():
    import ROOT
    from math import acos, cos, sin
    from tqdm import tqdm

    df1 = pd.read_csv(output_directory + "csv_" + version + "_train.csv")
    #print(df1.head())
    df2 = pd.read_csv(output_directory + "csv_" + version + "_valid.csv")
    #print(df2.head())

    print("from {} events, {} are predicted after theory ({} %)".format(len(y_true),counter_true,counter_true/len(y_true)*100))

    '''
    f = "GluGluHToTauTauUncorrelatedDecayFilteredM125_RunIIFall17MiniAODv2_PU2017_13TeV_MINIAOD_powheg-pythia8.root"
    rootFile = ROOT.TFile(sample_directory + f, "read")
    tree = rootFile.Get("tt_nominal/ntuple")
    entries = tree.GetEntries()

    for i in tqdm(range(500000), unit="events"):
        tree.GetEntry(i)

        decayModeMVA_1 = tree.GetLeaf("decayModeMVA_1").GetValue()
        decayModeMVA_2 = tree.GetLeaf("decayModeMVA_2").GetValue()
        wt_000 = tree.GetLeaf("tauSpinnerWeight000").GetValue()
        wt_050 = tree.GetLeaf("tauSpinnerWeight050").GetValue()
        wt_100 = tree.GetLeaf("tauSpinnerWeight100").GetValue()

        # Get CP sensitive variable
        if decay_channel == "mva1_1_mva2_2":
            PhiStarCP = tree.GetLeaf("recoPhiStarCPRhoMerged").GetValue()

        csv_string = ""

        #filtering out entries only contraining ones
        if decayModeMVA_1 == 1 and decayModeMVA_2 == 1 and wt_000 != 1 and PhiStarCP > -500:

            # calculate neutrino 4 vector
            svfitTau1LV = tree.svfitTau1LV
            svfitTau2LV = tree.svfitTau2LV

            lep1neutrinoLV = tree.svfitTau1LV - tree.lep1LV
            lep2neutrinoLV = tree.svfitTau2LV - tree.lep2LV

            lep1LV = tree.lep1LV
            lep2LV = tree.lep2LV
            lep1SumChargedHadronsLV = tree.lep1SumChargedHadronsLV
            lep2SumChargedHadronsLV = tree.lep2SumChargedHadronsLV
            lep1SumNeutralHadronsLV = tree.lep1SumNeutralHadronsLV
            lep2SumNeutralHadronsLV = tree.lep2SumNeutralHadronsLV

            break
    lep1neutrinoLV.SetM(0)
    print("")
    for particle in [svfitTau1LV,lep1LV,lep1neutrinoLV]:
        print("Entry: ",particle.E(),particle.M(),particle.Px(),particle.Py(),particle.Pz())

    sum_of_LVs = svfitTau1LV
    boostvec = sum_of_LVs.BoostToCM()
    M = ROOT.Math.Boost(boostvec.X(),boostvec.Y(),boostvec.Z())

    svfitTau1LV = M * svfitTau1LV
    lep1LV = M * lep1LV
    lep1neutrinoLV = M * lep1neutrinoLV

    print("")
    for particle in [svfitTau1LV,lep1LV,lep1neutrinoLV]:
        print("Entry: ",particle.E(),particle.M(),particle.Px(),particle.Py(),particle.Pz())
    '''

#Calling the different ports of the main code according to the parser
def main():
    args = parser()

    if args.csv:
        get_csv()

    if args.training:
        do_training()

    if args.results:
        get_results()

    if args.attach:
        attach()

    if args.debug:
        do_debug()

if __name__ == "__main__":
    main()
