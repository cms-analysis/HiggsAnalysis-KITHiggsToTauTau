import os
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras

#User interface. Specify the following paths:
#   the directory with the signal and background samples
#   the input json file from the controllplotter. this will be used to identify the relevant samples and their weights
#   the directory to use for storing/ loading the csv dataset, model, and additional files_labeled_with_weights
#   the version of execution in order not to overwrite previous files in the input/output directories
sample_directory = "/net/scratch_cms3b/krausse/public/new_ROOT/"
input_json = "/net/scratch_cms3b/krausse/public/input/m_vis.json"
output_directory = "/net/scratch_cms3b/krausse/public/output/"
version = "final_"

#list of used samples
label_str = ["zll", "ztt_emb", "ttj", "wj", "vv", "qcd", "zmt"]

#Argument parser
def parser():
    import argparse

    parser = argparse.ArgumentParser(description="Script for LFV Analysis 2017. This code classifies a set of signal-background samples using a dnn. The result of classification on the form of a dnn_score is then appended to the root files and can then be used for statistical analysis.", formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("--csv", action = "store_true", help="Create csv file as DNN input")
    parser.add_argument("--training", action = "store_true", help="Train the DNN")
    parser.add_argument("--results", action = "store_true", help="get DNN results by application to the whole dataset")
    parser.add_argument("--attach", action = "store_true", help="attach DNN score to ROOT files")
    return parser.parse_args()


##########   supporting definitions to use in the main parts of the code ##########


#read json file from controllplots and create list of used root files, labels and weights, that are being used for the analysis
def get_labeled_files_weights():
    import json
    import re
    #Read the json file, get, weights, labels, files and nicks
    with open(input_json, 'r') as myfile:
        data=myfile.read()
    obj = json.loads(data)
    weights = obj["weights"]
    labels = obj["labels"]
    files = obj["files"]
    nicks = obj["nicks"]

    #run through file-list to sort them together with weights and labels
    labeled_files=[]
    for i in range(len(files)):
        #check if file is used for plotting(nicks =! noplot...)
        for l in labels:
            if nicks[i]==l:
                #make list, that sorts every file with their weight and nick
                labeled_files.append([files[i].split(), weights[i], nicks[i]])

    for labfile in labeled_files:
        #weights are mix of numbers and vars from ROOT. Extract the var names in a list
        splitted_weights = re.split('[^a-zA-Z0-9_.]', labfile[1])
        ilist=[]
        for i in range(len(splitted_weights)):
            if len(splitted_weights[i])==0:
                ilist.append(i)
            elif splitted_weights[i][0].isalpha() == False:
                ilist.append(i)
            elif splitted_weights[i] == u'abs':
                ilist.append(i)

        while len(ilist)>0:
            del splitted_weights[ilist[-1]]
            del ilist[-1]

        #append list of ROOT-vars used in weights to the final output list
        labfile.append(splitted_weights)

    #format final output
    files_labeled_with_weights = []
    for i in range(len(labeled_files)):
        for j in range(len(labeled_files[i][0])):
            filename = labeled_files[i][0][j].split("/")[0] + "/" + labeled_files[i][0][j].split("/")[0] + ".root"
            files_labeled_with_weights.append([filename, labeled_files[i][1], labeled_files[i][2], labeled_files[i][3]])
    return files_labeled_with_weights


#preprocessing of the dataframe holding the events in order to make the variables ready for dnn training
def get_dnn_input(df):
    label_dict = {"zll":0,
                  "ztt_emb":1,
                  "ttj":2,
                  "wj":3,
                  "vv":4,
                  "qcd":5,
                  "zmt":6
                  }
    variables_skimmed = ["m_vis", "met", "mt_1", "mt_2", "mt_Z", "pt_1", "pt_2", "pt_ll", "ptvis","E_Z", "delta_phi_ll", "delta_phi_l1MET", "delta_phi_l2MET", "delta_phi_l1Z", "delta_phi_l2Z", "delta_Theta_ll", "abs_d0_1", "abs_d0_2"]
    variables_remove = ["collinearMass", "d0_1", "d0_2", "eta_1", "eta_2", "phi_1", "phi_2", "phi_met", "phi_Z", "theta_1", "theta_2"]

    df = df.drop(["weight"], axis=1)
    df = df.drop(variables_remove, axis=1)
    df = df.dropna()
    df["label"] = df["label"].map(label_dict)
    #scaling dnn input, so each input has variable in [0,1]
    for v in variables_skimmed:
        df[v] = (df[v] - df[v].mean())/df[v].std()
    label_list = df.pop("label").values
    x_test = df.values
    y_test = keras.utils.to_categorical(label_list, num_classes=7)
    return x_test, y_test


#Train the DNN
def DNN_training(even_or_odd):
    from sklearn.model_selection import train_test_split

    #vars
    label_dict = {"zll":0,
                  "ztt_emb":1,
                  "ttj":2,
                  "wj":3,
                  "vv":4,
                  "qcd":5,
                  "zmt":6
                  }
    variables = ["collinearMass", "d0_1", "d0_2", "eta_1", "eta_2", "m_vis", "met", "mt_1", "mt_2", "mt_Z", "pt_1", "pt_2", "pt_ll", "ptvis", "phi_1", "phi_2", "phi_met", "phi_Z", "theta_1", "theta_2","E_Z", "delta_phi_ll", "delta_phi_l1MET", "delta_phi_l2MET", "delta_phi_l1Z", "delta_phi_l2Z", "delta_Theta_ll", "abs_d0_1", "abs_d0_2"]
    variables_skimmed = ["m_vis", "met", "mt_1", "mt_2", "mt_Z", "pt_1", "pt_2", "pt_ll", "ptvis","E_Z", "delta_phi_ll", "delta_phi_l1MET", "delta_phi_l2MET", "delta_phi_l1Z", "delta_phi_l2Z", "delta_Theta_ll", "abs_d0_1", "abs_d0_2"]
    variables_remove = ["collinearMass", "d0_1", "d0_2", "eta_1", "eta_2", "phi_1", "phi_2", "phi_met", "phi_Z", "theta_1", "theta_2"]

    print("reading in dataset:\n")
    df = pd.read_csv(output_directory + "csv_" + version + even_or_odd + ".csv")
    print("starting data manipulation:\n")

    df = df.drop(["weight"], axis=1)
    df = df.drop(variables_remove, axis=1)
    df = df.dropna()

    df["label"] = df["label"].map(label_dict)
    #scaling dnn input, so each input has variable in [0,1]
    for v in variables_skimmed:
        df[v] = (df[v] - df[v].mean())/df[v].std()

    #Balance Dataset
    balanced_df = df.groupby("label")
    balanced_df = pd.DataFrame(balanced_df.apply(lambda x: x.sample(balanced_df.size().min()).reset_index(drop=True)))
    label_list = balanced_df.pop("label").values
    x = balanced_df.values
    y = keras.utils.to_categorical(label_list, num_classes=7)
    #create training, validation and testing dataset
    x_train, x_valid, y_train, y_valid = train_test_split(x, y, test_size=0.2, random_state=42)

    print("start training:\n")
    #define model
    model = tf.keras.Sequential()
    model.add(tf.keras.layers.Dense(32, input_dim=x.shape[1], activation="relu", kernel_initializer='random_normal'))
    model.add(tf.keras.layers.Dropout(0.2))
    model.add(tf.keras.layers.Dense(32,activation="relu",kernel_initializer='random_normal'))
    model.add(tf.keras.layers.Dense(y.shape[1], activation="softmax",kernel_initializer='random_normal'))

    #compiling the program by declaring the loss-function, the optimizer and the metrics
    model.compile(loss="categorical_crossentropy", optimizer=tf.keras.optimizers.Adam(lr=0.001), metrics=["accuracy"])
    history = model.fit(x_train,y_train,validation_data=(x_valid,y_valid),verbose=1,epochs=200)
    model.save(output_directory + "model_" + version + even_or_odd + ".h5")
    return model, history


#plot confusion matrix
def plot_confusion_matrix(confusion_matrix, even_or_odd):
    import seaborn

    seaborn.set(color_codes=True)
    plt.figure(1, figsize=(9, 6))
    plt.title(even_or_odd + " Model Confusion Matrix")
    seaborn.set(font_scale=1.)
    ax = seaborn.heatmap(confusion_matrix, annot=True, cmap="YlGnBu", cbar_kws={'label': 'Scale'}, fmt='g')
    ax.set_xticklabels(label_str)
    ax.set_yticklabels(label_str)
    ax.set(ylabel="True Label", xlabel="Predicted Label")
    plt.savefig(output_directory + "confusionmatrix_" + version + even_or_odd + ".png", bbox_inches='tight', dpi=300)
    plt.close()


#plot loss accuracy on training
def plot_acc_loss(history, even_or_odd):
    fig = plt.figure()
    ax1 = fig.add_subplot(211)
    ax2 = fig.add_subplot(212)

    ax1.plot(history.history['acc'])
    ax1.plot(history.history['val_acc'])
    ax1.set_title(even_or_odd + " Model")
    ax1.set_xlabel("epoch")
    ax1.set_ylabel("accuracy")
    ax1.legend()

    ax2.plot(history.history['loss'])
    ax2.plot(history.history['val_loss'])
    ax2.set_xlabel("epoch")
    ax2.set_ylabel("loss")
    ax2.legend()
    plt.savefig(output_directory + "loss_acc_" + version + even_or_odd + ".png")
    plt.close()


#plot dnn_score variable (currently unused, since the dnn score can be plotted just using harryPlotter after attaching it to the root files)
def plot_dnn_score(result_df):
    result_df["score"] = result_df.apply(lambda row: row.zmt - (row.zll + row.ztt_emb + row.ttj + row.vv + row.wj + row.qcd), axis=1)
    df_zll = pd.DataFrame(result_df[result_df["label"] == 0.], columns=["score"])
    df_ztt = pd.DataFrame(result_df[result_df["label"] == 1.], columns=["score"])
    df_ttj = pd.DataFrame(result_df[result_df["label"] == 2.], columns=["score"])
    df_vv = pd.DataFrame(result_df[result_df["label"] == 3.], columns=["score"])
    df_wj = pd.DataFrame(result_df[result_df["label"] == 4.], columns=["score"])
    df_qcd = pd.DataFrame(result_df[result_df["label"] == 5.], columns=["score"])
    df_zmt = pd.DataFrame(result_df[result_df["label"] == 6.], columns=["score"])

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.hist(df_zll.values, label="zll")
    ax.hist(df_ztt.values, label="ztt")
    ax.hist(df_ttj.values, label="ttj")
    ax.hist(df_vv.values, label="vv")
    ax.hist(df_wj.values, label="wj")
    ax.hist(df_qcd.values, label="qcd")
    ax.hist(df_zmt.values, label="zmt")
    ax.legend()
    plt.savefig(output_directory + "dnn_sore_" + version + ".png")


########## Main functionality of this code based on the previous defined supporting definitions ##########


#dnn input is created in form of csv files, dataset is split by even/odd event numbers to train two networks later
def get_csv():
    import ROOT
    from math import acos, cos, sin
    from tqdm import tqdm

    #defining variables, read in info from json file and open csv file
    filelist = get_labeled_files_weights()
    csv_even = open(output_directory + "csv_" + version + "even.csv", "w")
    csv_odd = open(output_directory + "csv_" + version + "odd.csv", "w")
    csv_even.write("collinearMass,d0_1,d0_2,eta_1,eta_2,m_vis,met,mt_1,mt_2,mt_Z,pt_1,pt_2,pt_ll,ptvis,phi_1,phi_2,phi_met,phi_Z,theta_1,theta_2,E_Z,delta_phi_ll,delta_phi_l1MET,delta_phi_l2MET,delta_phi_l1Z,delta_phi_l2Z,delta_Theta_ll,abs_d0_1,abs_d0_2,weight,label\n")
    csv_odd.write("collinearMass,d0_1,d0_2,eta_1,eta_2,m_vis,met,mt_1,mt_2,mt_Z,pt_1,pt_2,pt_ll,ptvis,phi_1,phi_2,phi_met,phi_Z,theta_1,theta_2,E_Z,delta_phi_ll,delta_phi_l1MET,delta_phi_l2MET,delta_phi_l1Z,delta_phi_l2Z,delta_Theta_ll,abs_d0_1,abs_d0_2,weight,label\n")

    counter = 0
    #encode unicode to utf-8
    for i in range(len(filelist)):
        filelist[i][0] = filelist[i][0].encode("utf-8")
        filelist[i][1] = filelist[i][1].encode("utf-8")
        filelist[i][2] = filelist[i][2].encode("utf-8")
        for j in range(len(filelist[i][3])):
            filelist[i][3][j] = filelist[i][3][j].encode("utf-8")

    #loop over all files
    print("running over {} ROOT-files:\n".format(len(filelist)))
    for f in filelist:
        counter+=1
        #read tree from rootfile
        rootFile = ROOT.TFile(sample_directory + f[0], "read")
        tree = rootFile.Get("mt_nominal/ntuple")
        entries = tree.GetEntries()

        #modify weight string to python readable (for evaluating later)
        f[1] = f[1].replace('&&', 'and')
        f[1] = f[1].replace('||', 'or')
        f[1] = f[1].replace('!', 'not')
        for var in list(dict.fromkeys(f[3])):
            newstring = 'tree.GetLeaf(\"' + var + '\").GetValue()'
            f[1] = f[1].replace(var, newstring)

        #loop over every entry in ROOT tree and get weight and sensitive vars
        for i in tqdm(range(entries), desc="{} out of {}".format(counter, len(filelist)), unit="events"):
            tree.GetEntry(i)
            weight = eval(f[1])
            if weight!=0:
                #reading in direct vars from tree
                collinearMass	= tree.GetLeaf("collinearMass").GetValue()
                d0_1  			= tree.GetLeaf("d0_1").GetValue()
                d0_2  			= tree.GetLeaf("d0_2").GetValue()
                eta_1  			= tree.GetLeaf("eta_1").GetValue()
                eta_2  			= tree.GetLeaf("eta_2").GetValue()
                m_vis  			= tree.GetLeaf("m_vis").GetValue()
                met  			= tree.GetLeaf("met").GetValue()
                mt_1  			= tree.GetLeaf("mt_1").GetValue()
                mt_2  			= tree.GetLeaf("mt_2").GetValue()
                mt_Z            = tree.diLepLV.Mt()
                pt_1			= tree.GetLeaf("pt_1").GetValue()
                pt_2			= tree.GetLeaf("pt_2").GetValue()
                pt_ll           = tree.diLepLV.Pt()
                ptvis  			= tree.GetLeaf("ptvis").GetValue()
                phi_1           = tree.GetLeaf("phi_1").GetValue()
                phi_2           = tree.GetLeaf("phi_2").GetValue()
                phi_met         = tree.GetLeaf("metphi").GetValue()
                phi_Z           = tree.diLepLV.Phi()
                theta_1         = tree.lep1LV.Theta()
                theta_2         = tree.lep2LV.Theta()
                E_Z             = tree.diLepLV.energy()
                event           = tree.GetLeaf("event").GetValue()

                #creating own sensitive vars
                delta_phi_ll    = acos(cos(phi_1)*cos(phi_2) + sin(phi_1)*sin(phi_2))
                delta_phi_l1MET = acos(cos(phi_1)*cos(phi_met) + sin(phi_1)*sin(phi_met))
                delta_phi_l2MET = acos(cos(phi_2)*cos(phi_met) + sin(phi_2)*sin(phi_met))
                delta_phi_l1Z   = acos(cos(phi_1)*cos(phi_Z) + sin(phi_1)*sin(phi_Z))
                delta_phi_l2Z   = acos(cos(phi_2)*cos(phi_Z) + sin(phi_2)*sin(phi_Z))
                delta_Theta_ll  = acos(cos(theta_1)*cos(theta_2) + sin(theta_1)*sin(theta_2))
                abs_d0_1        = abs(d0_1)
                abs_d0_2        = abs(d0_2)

                #write sensitive vars and label in csv file
                if event%2==0:
                    csv_even.write(str(collinearMass) + "," + str(d0_1) + "," + str(d0_2) + "," + str(eta_1) + "," + str(eta_2) + "," + str(m_vis) + "," + str(met) + "," + str(mt_1) + "," + str(mt_2) + "," + str(mt_Z) + "," + str(pt_1) + "," + str(pt_2) + "," + str(pt_ll) + "," + str(ptvis) + "," + str(phi_1) + "," + str(phi_2) + "," + str(phi_met) + "," + str(phi_Z) + "," + str(theta_1) + "," + str(theta_2) + "," + str(E_Z) + "," + str(delta_phi_ll) + "," + str(delta_phi_l1MET) + "," + str(delta_phi_l2MET) + "," + str(delta_phi_l1Z) + "," + str(delta_phi_l2Z) + "," + str(delta_Theta_ll) + "," + str(abs_d0_1) + "," + str(abs_d0_2) + "," + str(weight) + "," + str(f[2]) + "\n")
                else:
                    csv_odd.write(str(collinearMass) + "," + str(d0_1) + "," + str(d0_2) + "," + str(eta_1) + "," + str(eta_2) + "," + str(m_vis) + "," + str(met) + "," + str(mt_1) + "," + str(mt_2) + "," + str(mt_Z) + "," + str(pt_1) + "," + str(pt_2) + "," + str(pt_ll) + "," + str(ptvis) + "," + str(phi_1) + "," + str(phi_2) + "," + str(phi_met) + "," + str(phi_Z) + "," + str(theta_1) + "," + str(theta_2) + "," + str(E_Z) + "," + str(delta_phi_ll) + "," + str(delta_phi_l1MET) + "," + str(delta_phi_l2MET) + "," + str(delta_phi_l1Z) + "," + str(delta_phi_l2Z) + "," + str(delta_Theta_ll) + "," + str(abs_d0_1) + "," + str(abs_d0_2) + "," + str(weight) + "," + str(f[2]) + "\n")
    csv_even.close()
    csv_odd.close()


#call DNN training for even and odd dataset
def do_training():
    print("Train model 1 on even dataset")
    model_even, history_even = DNN_training("even")
    print("train model 2 on odd dataset")
    model_odd, history_odd = DNN_training("odd")
    print("plot loss and accuracy for both models")
    plot_acc_loss(history_even, "even")
    plot_acc_loss(history_odd, "odd")


#Get results on test dataset with confusion matrix and dnn_score-Plot
def get_results():
    import numpy as np
    from sklearn.metrics import confusion_matrix

    #load model
    model_even = keras.models.load_model(output_directory + "model_" + version + "even.h5")
    model_odd = keras.models.load_model(output_directory + "model_" + version + "odd.h5")
    #read in and shape test data
    df_even = pd.read_csv(output_directory + "csv_" + version + "even.csv")
    df_odd = pd.read_csv(output_directory + "csv_" + version + "odd.csv")
    x_even, y_even = get_dnn_input(df_even)
    x_odd, y_odd = get_dnn_input(df_odd)
    #testing on Test data
    test_loss_even, test_acc_even = model_even.evaluate(x_odd, y_odd, verbose=1)
    test_loss_odd, test_acc_odd = model_odd.evaluate(x_even, y_even, verbose=1)
    print("\nAccuracy on even model: {}".format(test_acc_even))
    print("\nAccuracy on odd model: {}".format(test_acc_odd))

    #calculating and plotting confusion matrix
    predictions_even = model_even.predict(x_odd)
    predictions_odd = model_odd.predict(x_even)

    pred_labels_even = np.argmax(predictions_even, axis=1)
    true_labels_even = np.argmax(y_odd, axis=1)
    cm_even = confusion_matrix(true_labels_even, pred_labels_even)
    cm_even = cm_even.astype("float") / cm_even.sum(axis=1)[:, np.newaxis]
    plot_confusion_matrix(cm_even, "even")

    pred_labels_odd = np.argmax(predictions_odd, axis=1)
    true_labels_odd = np.argmax(y_even, axis=1)
    cm_odd = confusion_matrix(true_labels_odd, pred_labels_odd)
    cm_odd = cm_odd.astype("float") / cm_odd.sum(axis=1)[:, np.newaxis]
    plot_confusion_matrix(cm_odd, "odd")


#Attach dnn_score to odd event Samples and write into new root file
def attach():
    import numpy as np
    import ROOT
    from math import acos, cos, sin
    from tqdm import tqdm
    import array
    import os

    print("Get scaling factors:\n")
    variables_skimmed = ["m_vis", "met", "mt_1", "mt_2", "mt_Z", "pt_1", "pt_2", "pt_ll", "ptvis","E_Z", "delta_phi_ll", "delta_phi_l1MET", "delta_phi_l2MET", "delta_phi_l1Z", "delta_phi_l2Z", "delta_Theta_ll", "abs_d0_1", "abs_d0_2"]

    df_even = pd.read_csv(output_directory + "csv_" + version + "even.csv")
    df_odd = pd.read_csv(output_directory + "csv_" + version + "odd.csv")

    mean_even=[]
    mean_odd=[]
    std_even=[]
    std_odd=[]
    for v in variables_skimmed:
        mean_even.append(df_even[v].mean())
        mean_odd.append(df_odd[v].mean())
        std_even.append(df_even[v].std())
        std_odd.append(df_odd[v].std())

    print("load dnn:\n")
    model_even = keras.models.load_model(output_directory + "model_" + version + "even.h5")
    model_odd = keras.models.load_model(output_directory + "model_" + version + "odd.h5")

    filelist = []
    for root, directories, files in os.walk(sample_directory):
        for name in files:
            filelist.append(str(os.path.join(root, name)))

    counter=0
    #loop over all files
    print("running over {} ROOT-files:\n".format(len(filelist[41:])))
    for f in filelist[41:]:
        print("updating file {}".format(f))
        counter+=1
        rootFile = ROOT.TFile(f, "UPDATE")
        tree = rootFile.Get("mt_nominal/ntuple")
        dnn_score       = array.array("f", [0])
        delta_phi_ll    = array.array("f", [0])
        delta_phi_l1MET = array.array("f", [0])
        delta_phi_l2MET = array.array("f", [0])
        delta_phi_l1Z   = array.array("f", [0])
        delta_phi_l2Z   = array.array("f", [0])
        delta_Theta_ll  = array.array("f", [0])
        abs_d0_1        = array.array("f", [0])
        abs_d0_2        = array.array("f", [0])
        branch_dnn_score       = tree.Branch("dnn_score", dnn_score, "dnn_score/F")
        branch_delta_phi_ll    = tree.Branch("delta_phi_ll", delta_phi_ll, "delta_phi_ll/F")
        branch_delta_phi_l1MET = tree.Branch("delta_phi_l1MET", delta_phi_l1MET, "delta_phi_l1MET/F")
        branch_delta_phi_l2MET = tree.Branch("delta_phi_l2MET", delta_phi_l2MET, "delta_phi_l2MET/F")
        branch_delta_phi_l1Z   = tree.Branch("delta_phi_l1Z", delta_phi_l1Z, "delta_phi_l1Z/F")
        branch_delta_phi_l2Z   = tree.Branch("delta_phi_l2Z", delta_phi_l2Z, "delta_phi_l2Z/F")
        branch_delta_Theta_ll  = tree.Branch("delta_Theta_ll", delta_Theta_ll, "delta_Theta_ll/F")
        branch_abs_d0_1        = tree.Branch("abs_d0_1", abs_d0_1, "abs_d0_1/F")
        branch_abs_d0_2        = tree.Branch("abs_d0_2", abs_d0_2, "abs_d0_1/F")

        entries = tree.GetEntries()
        #loop over every entry in ROOT tree and get weight and sensitive vars
        for i in tqdm(range(entries), desc="{} out of {}".format(counter, len(filelist[41:])), unit="events"):
            tree.GetEntry(i)

            #reading in direct vars from tree
            collinearMass_var	= tree.GetLeaf("collinearMass").GetValue()
            d0_1_var  			= tree.GetLeaf("d0_1").GetValue()
            d0_2_var  			= tree.GetLeaf("d0_2").GetValue()
            eta_1_var  			= tree.GetLeaf("eta_1").GetValue()
            eta_2_var  			= tree.GetLeaf("eta_2").GetValue()
            m_vis_var  			= tree.GetLeaf("m_vis").GetValue()
            met_var  			= tree.GetLeaf("met").GetValue()
            mt_1_var  			= tree.GetLeaf("mt_1").GetValue()
            mt_2_var  			= tree.GetLeaf("mt_2").GetValue()
            mt_Z_var            = tree.diLepLV.Mt()
            pt_1_var			= tree.GetLeaf("pt_1").GetValue()
            pt_2_var			= tree.GetLeaf("pt_2").GetValue()
            pt_ll_var           = tree.diLepLV.Pt()
            ptvis_var  			= tree.GetLeaf("ptvis").GetValue()
            phi_1_var           = tree.GetLeaf("phi_1").GetValue()
            phi_2_var           = tree.GetLeaf("phi_2").GetValue()
            phi_met_var         = tree.GetLeaf("metphi").GetValue()
            phi_Z_var           = tree.diLepLV.Phi()
            theta_1_var         = tree.lep1LV.Theta()
            theta_2_var         = tree.lep2LV.Theta()
            E_Z_var             = tree.diLepLV.energy()
            event_var           = tree.GetLeaf("event").GetValue()

            #creating own sensitive vars (with extra caution due to possible math errors in calculation)
            try:
                delta_phi_ll_var    = acos(cos(phi_1_var)*cos(phi_2_var) + sin(phi_1_var)*sin(phi_2_var))
            except:
                delta_phi_ll_var    = 0
                print("invalid angle")
            try:
                delta_phi_l1MET_var = acos(cos(phi_1_var)*cos(phi_met_var) + sin(phi_1_var)*sin(phi_met_var))
            except:
                delta_phi_l1MET_var = 0
                print("invalid angle")
            try:
                delta_phi_l2MET_var = acos(cos(phi_2_var)*cos(phi_met_var) + sin(phi_2_var)*sin(phi_met_var))
            except:
                delta_phi_l2MET_var = 0
                print("invalid angle")
            try:
                delta_phi_l1Z_var   = acos(cos(phi_1_var)*cos(phi_Z_var) + sin(phi_1_var)*sin(phi_Z_var))
            except:
                delta_phi_l1Z_var   = 0
                print("invalid angle")
            try:
                delta_phi_l2Z_var   = acos(cos(phi_2_var)*cos(phi_Z_var) + sin(phi_2_var)*sin(phi_Z_var))
            except:
                delta_phi_l2Z_var   = 0
                print("invalid angle")
            try:
                delta_Theta_ll_var  = acos(cos(theta_1_var)*cos(theta_2_var) + sin(theta_1_var)*sin(theta_2_var))
            except:
                delta_Theta_ll_var = 0
                print("invalid angle")
            abs_d0_1_var        = abs(d0_1_var)
            abs_d0_2_var        = abs(d0_2_var)

            dnn_input_raw = [m_vis_var, met_var, mt_1_var, mt_2_var, mt_Z_var, pt_1_var, pt_2_var, pt_ll_var, ptvis_var, E_Z_var, delta_phi_ll_var, delta_phi_l1MET_var, delta_phi_l2MET_var, delta_phi_l1Z_var, delta_phi_l2Z_var, delta_Theta_ll_var, abs_d0_1_var, abs_d0_2_var]
            dnn_input=[]
            if event_var%2==0:
                for index, var in enumerate(dnn_input_raw):
                    dnn_input.append((var - mean_even[index])/std_even[index])
                dnn_input=np.asarray([dnn_input])
                prediction = model_odd.predict(dnn_input)[0]
                dnn_score_var = prediction[6] - np.sum(prediction[:6])
            else:
                for index, var in enumerate(dnn_input_raw):
                    dnn_input.append((var - mean_odd[index])/std_odd[index])
                dnn_input=np.asarray([dnn_input])
                prediction = model_even.predict(dnn_input)[0]
                dnn_score_var = prediction[6] - np.sum(prediction[:6])

            dnn_score[0]       = dnn_score_var
            delta_phi_ll[0]    = delta_phi_ll_var
            delta_phi_l1MET[0] = delta_phi_l1MET_var
            delta_phi_l2MET[0] = delta_phi_l2MET_var
            delta_phi_l1Z[0]   = delta_phi_l1Z_var
            delta_phi_l2Z[0]   = delta_phi_l2Z_var
            delta_Theta_ll[0]  = delta_Theta_ll_var
            abs_d0_1[0]        = abs_d0_1_var
            abs_d0_2[0]        = abs_d0_1_var

            branch_dnn_score.Fill()
            branch_delta_phi_ll.Fill()
            branch_delta_phi_l1MET.Fill()
            branch_delta_phi_l2MET.Fill()
            branch_delta_phi_l1Z.Fill()
            branch_delta_phi_l2Z.Fill()
            branch_delta_Theta_ll.Fill()
            branch_abs_d0_1.Fill()
            branch_abs_d0_2.Fill()
        rootFile.cd("mt_nominal")
        tree.Write("", ROOT.TObject.kOverwrite)
        rootFile.Close()


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

if __name__ == "__main__":
    main()
