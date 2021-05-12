import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras

#User interface. Specify the following paths:
#   the directory with the signal and background samples
#   the input json file from the controllplotter. this will be used to identify the relevant samples and their weights
#   the directory to use for storing/ loading the csv dataset, model, and additional files_labeled_with_weights
#   the version of execution in order not to overwrite previous files in the input/output directories
sample_directory = "/net/scratch_cms3b/fenger/artus/2021_05_05/"
input_json = "/net/scratch_cms3b/krausse/public/input/m_vis.json"
output_directory = "/net/scratch_cms3b/fenger/artus/2021_07_05/"
version = "dummy_loop_mva12"

#Argument parser
def parser():
    import argparse

    parser = argparse.ArgumentParser(description="Script for LFV Analysis 2017. This code classifies a set of signal-background samples using a dnn. The result of classification on the form of a dnn_score is then appended to the root files and can then be used for statistical analysis.", formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("--csv", action = "store_true", help="Create csv file as DNN input")
    parser.add_argument("--training", action = "store_true", help="Train the DNN")
    parser.add_argument("--results", action = "store_true", help="get DNN results by application to the whole dataset")
    parser.add_argument("--attach", action = "store_true", help="attach DNN score to ROOT files")
    parser.add_argument("--debug", action = "store_true", help="debug code")
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

def get_DNN_input(df):
    var_skimmed = ["eta_1","eta_2","m_vis","met","mt_1","mt_2","pt_1","pt_2","ptvis","phi_1","phi_2"]
    mixing_labels = np.linspace(0,100,21,dtype = int)

    #input rescaling
    for v in var_skimmed:
        df[v] = (df[v] - df[v].mean())/df[v].std()

    #sample_weight_array = df.pop("tauSpinnerWeight").values
    mixing_array = df.pop("mixing").values

    x = df.values
    y = keras.utils.to_categorical(mixing_array/5, num_classes=21)

    x_valid = np.delete(x,-1,axis = 1)

    return x_valid,y


def DNN_training():
    from sklearn.model_selection import train_test_split

    mixing_labels = np.linspace(0,100,21,dtype = int)

    print("reading in dataset:\n")
    df= pd.read_csv(output_directory + "csv_" + version + "_train.csv")
    print("starting data manipulation:\n")

    #var_drop = ["eta_1","eta_2","m_vis","met","mt_1","mt_2","pt_1","pt_2","ptvis","phi_1","phi_2","decayModeMVA_2"]
    #df = df.drop(var_drop, axis=1)

    var_skimmed = df.columns.values.tolist()
    var_remove = ["mixing","tauSpinnerWeight"] #,"decayModeMVA_2"
    for i in var_remove:
        var_skimmed.remove(i)

    #input rescaling
    for v in var_skimmed:
        df[v] = (df[v] - df[v].mean())/df[v].std()

    #sample_weight_array = df.pop("tauSpinnerWeight").values
    mixing_array = df.pop("mixing").values
    df = df.drop("decayModeMVA_2",axis = 1)

    x = df.values
    y = keras.utils.to_categorical(mixing_array/5, num_classes=21)

    x_train_cache, x_valid_cache, y_train, y_valid = train_test_split(x, y, test_size=0.2, random_state=42)

    x_train_sample_weights = x_train_cache[:,-1]
    x_valid_sample_weights = x_valid_cache[:,-1]

    x_train = np.delete(x_train_cache,-1,axis = 1)
    x_valid = np.delete(x_valid_cache,-1,axis = 1)

    print("start training:\n")
    #define model
    print("shape input",x_train.shape[1])
    model = tf.keras.Sequential()
    model.add(tf.keras.layers.Dense(300, input_dim=x_train.shape[1], activation="relu"))
    model.add(tf.keras.layers.Dropout(0.2))
    model.add(tf.keras.layers.Dense(300,activation="relu"))
    model.add(tf.keras.layers.Dense(300,activation="relu"))
    model.add(tf.keras.layers.Dense(y_train.shape[1], activation="softmax"))

    #compiling the program by declaring the loss-function, the optimizer and the metrics
    model.compile(loss="categorical_crossentropy", optimizer=tf.keras.optimizers.Adam(lr=0.001), metrics=["accuracy"])
    history = model.fit(x_train,y_train ,validation_data=(x_valid,y_valid),verbose=1,epochs=50,class_weight = x_train_sample_weights,batch_size = 100) #
    model.save(output_directory + "model_" + version + ".h5")
    return model, history


#plot confusion matrix
def plot_confusion_matrix(confusion_matrix, even_or_odd):
    import seaborn

    label_str = ["000","005","010","015","020","025","030","035","040","045","050","055","060","065","070","075","080","085","090","095","100"]
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
def plot_acc_loss(history):
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
    plt.savefig(output_directory + "loss_acc_" + version + ".png")
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

def get_csv():
    import ROOT
    from math import acos, cos, sin
    from tqdm import tqdm

    # custom file and var list:
    filelist = ["GluGluHToTauTauUncorrelatedDecayFilteredM125_RunIIFall17MiniAODv2_PU2017_13TeV_MINIAOD_powheg-pythia8/GluGluHToTauTauUncorrelatedDecayFilteredM125_RunIIFall17MiniAODv2_PU2017_13TeV_MINIAOD_powheg-pythia8.root"]
    tauSpinnerWeight_steps = ["000","005","010","015","020","025","030","035","040","045","050","055","060","065","070","075","080","085","090","095","100"]
    vars_list = ["eta_1","eta_2","m_vis","met","mt_1","mt_2","pt_1","pt_2","ptvis","phi_1","phi_2"]
    counter = 0

    #Settings
    islooptauSpinnerWeights = False

    #defining variables, read in info from json file and open csv file
    csv_train = open(output_directory + "csv_" + version + "_train.csv", "w")
    csv_valid = open(output_directory + "csv_" + version + "_valid.csv", "w")

    csv_header_string = ""
    for v in vars_list:
        csv_header_string += v + ","

    csv_header_string += "PhiStarCP,decayModeMVA_2," #additional vars

    csv_train.write(csv_header_string + "tauSpinnerWeight,mixing"+ "\n")
    csv_valid.write(csv_header_string + "tauSpinnerWeight,mixing"+ "\n")

    for f in filelist:
        counter += 1
        rootFile = ROOT.TFile(sample_directory + f, "read")
        tree = rootFile.Get("mt_nominal/ntuple")
        entries = tree.GetEntries()

        for i in tqdm(range(100000), desc="{} out of {}".format(counter, len(filelist)), unit="events"):
            tree.GetEntry(i)

            decayModeMVA_2 = tree.GetLeaf("decayModeMVA_2").GetValue()

            if decayModeMVA_2 == 1:

                # reading in vars from tree
                csv_string = ""
                for vars in vars_list:
                    csv_string += str(tree.GetLeaf(vars).GetValue()) + ","

                #read additional vars
                csv_string += str(tree.GetLeaf("recoPhiStarCPCombMergedHelrPVBS").GetValue()) + ","
                csv_string += str(decayModeMVA_2) + ","

                #looping tauSpinnerWeight
                if islooptauSpinnerWeights == True:

                    for step in tauSpinnerWeight_steps:
                        tauSpinnerWeightxxx = tree.GetLeaf("tauSpinnerWeight"+step).GetValue()

                        #write into csv file and plit into train and validation data
                        if i%2 == 0:
                            csv_train.write(csv_string + str(tauSpinnerWeightxxx) + "," + step + "\n")
                        else:
                            csv_valid.write(csv_string + str(tauSpinnerWeightxxx) + "," + step + "\n")

                elif islooptauSpinnerWeights == False:
                    random_step = np.random.choice(tauSpinnerWeight_steps)
                    tauSpinnerWeightxxx = tree.GetLeaf("tauSpinnerWeight"+random_step).GetValue()

                    #write into csv file and plit into train and validation data
                    if i%2 == 0:
                        csv_train.write(csv_string + str(tauSpinnerWeightxxx) + "," + random_step + "\n")
                    else:
                        csv_valid.write(csv_string + str(tauSpinnerWeightxxx) + "," + random_step + "\n")


    csv_train.close()
    csv_valid.close()

#call DNN training for even and odd dataset
def do_training():
    print("Train model on dataset")
    model_train, history_train = DNN_training()
    print("plot loss and accuracy for both models")
    plot_acc_loss(history_train)

#Get results on test dataset with confusion matrix and dnn_score-Plot
def get_results():
    import numpy as np
    from sklearn.metrics import confusion_matrix

    #load model
    model_train = keras.models.load_model(output_directory + "model_" + version + ".h5")
    #read in and shape test data
    df_valid = pd.read_csv(output_directory + "csv_" + version + "_valid.csv")
    x_eval, y_eval = get_DNN_input(df_valid)

    #testing on Test data
    test_loss, test_acc = model_train.evaluate(x_eval, y_eval, verbose=1)
    print("\nAccuracy on model: {}".format(test_acc))

    #calculating and plotting confusion matrix
    predictions = model_train.predict(x_eval)

    pred_labels = np.argmax(predictions, axis=1)
    true_labels = np.argmax(y_eval, axis=1)
    cm = confusion_matrix(true_labels, pred_labels)
    cm = cm.astype("float") / cm.sum(axis=1)[:, np.newaxis]
    plot_confusion_matrix(cm, "evaluation")

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


################################################################################

def do_debug():
    data1 = pd.read_csv(output_directory + "csv_" + version + "_train.csv")
    print(data1.head())
    data2 = pd.read_csv(output_directory + "csv_" + version + "_valid.csv")
    print(data2.head())


#Calling the different ports of the main code according to the parser
def main():
    args = parser()

    if args.csv:
        et_csv()

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
