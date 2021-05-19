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
version = "dummy_mva12"

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

# custom cross entropy loss function modelled after 2001.00455
def custom_crossentropy(y_true,y_pred):
    return K.sum(-1 * y_pred * K.log(y_true))


def get_DNN_input(df):
    from keras.utils import to_categorical

    mixing_labels = ["000","010","020","030","040","050","060","070","080","090","100","110","120","130","140","150","160","170","180","190","200"]
    var_drop = ["decayModeMVA_2","eta_1","eta_2","m_vis","met","mt_1","mt_2","pt_1","pt_2","ptvis","phi_1","phi_2"]
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

    y = np.argmax(y,axis=1)
    y = to_categorical(y,num_classes = 21)

    return x,y

def DNN_mixingangle_multiclassing():
    from sklearn.model_selection import train_test_split
    from keras.utils import to_categorical
    from sklearn.utils import class_weight

    mixing_labels = ["000","010","020","030","040","050","060","070","080","090","100","110","120","130","140","150","160","170","180","190","200"]

    print("reading in dataset:\n")
    df= pd.read_csv(output_directory + "csv_" + version + "_train.csv")
    print("starting data manipulation:\n")

    var_drop = ["decayModeMVA_2","eta_1","eta_2","m_vis","met","mt_1","mt_2","pt_1","pt_2","ptvis","phi_1","phi_2"]
    df = df.drop(var_drop, axis=1)

    # drop every unused variable before here
    var_skimmed = df.columns.values.tolist()
    var_remove =  ["PhiStarCP"] + mixing_labels #
    for i in var_remove:
        var_skimmed.remove(i)

    #input rescaling
    for v in var_skimmed:
        df[v] = (df[v] - df[v].mean())/df[v].std()

    split_range = len(df.columns.values.tolist()) - len(mixing_labels)
    x = df.iloc[:,:split_range].values
    y = df.iloc[:,split_range:].values

    y = np.argmax(y,axis=1)
    y = to_categorical(y,num_classes = 21)

    print(x[1])
    print(y[1])

    x_train, x_valid, y_train, y_valid = train_test_split(x, y, test_size=0.2, random_state=42)

    print("start training:\n")
    #define model
    print("shape input",x_train.shape[1])

    #define model
    model = tf.keras.Sequential()
    model.add(tf.keras.layers.Dense(32, input_dim=x_train.shape[1], activation = "relu",kernel_initializer="random_normal"))
    model.add(tf.keras.layers.Dropout(0.2))
    model.add(tf.keras.layers.Dense(32, activation = "relu",kernel_initializer="random_normal"))
    model.add(tf.keras.layers.Dense(y_train.shape[1], activation="softmax",kernel_initializer="random_normal"))

    model.compile(loss="categorical_crossentropy", optimizer=tf.keras.optimizers.Adam(lr=0.0001), metrics=["accuracy"])
    history = model.fit(x_train,y_train,validation_data=(x_valid,y_valid),verbose=1,epochs=200) #,batch_size = 256
    model.save(output_directory + "model_" + version + ".h5")
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
    model.compile(loss=custom_crossentropy, optimizer="adam", metrics=["accuracy"])
    history = model.fit(x_train,y_train ,validation_data=(x_valid,y_valid),verbose=1,epochs=10,batch_size = 100) #,batch_size = 100
    model.save(output_directory + "model_" + version + ".h5")
    return model, history


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

def plot_pred_diff(pred_labels,true_labels):
    class_diff = pred_labels - true_labels
    class_diff_mean = np.mean(class_diff)
    class_diff_std = np.std(class_diff)

    plt.figure()
    plt.hist(class_diff,histtype = u"step",bins = 9,label = "mean [idx]: {}\nstd [idx]: {}".format(class_diff_mean,class_diff_std))
    plt.xlabel("$\Delta_{class}$")
    plt.legend()
    plt.savefig(output_directory + "classdiff_" + version + ".png")

def plot_pred_dist(pred_labels,true_labels):
    plt.figure()
    plt.hist(pred_labels,histtype = u"step",bins = 20,label = "prediction",color="red")
    plt.hist(true_labels,histtype = u"step",bins = 20,label = "generation",color="black")
    plt.xlabel("$class index$")
    plt.legend()
    plt.savefig(output_directory + "classdist_" + version + ".png")

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

def calc_tauSpinnerWeight(wt_000,wt_050,wt_100,angle):
    new_weight = wt_000 * (np.cos(angle)**2 - np.cos(angle) * np.sin(angle)) + wt_100 * (np.sin(angle)**2 - np.cos(angle) * np.sin(angle)) + wt_050 * (2*np.cos(angle) * np.sin(angle))
    return new_weight

########## Main functionality of this code based on the previous defined supporting definitions ##########

def get_csv():
    import ROOT
    from math import acos, cos, sin
    from tqdm import tqdm

    # check for old csv file, if it exist its getting deleted
    if os.path.exists(output_directory + "csv_" + version + "_train.csv"):
        os.remove(output_directory + "csv_" + version + "_train.csv")
        os.remove(output_directory + "csv_" + version + "_valid.csv")
        print("removed old csv file")

    # custom file and var list:
    filelist = ["GluGluHToTauTauUncorrelatedDecayFilteredM125_RunIIFall17MiniAODv2_PU2017_13TeV_MINIAOD_powheg-pythia8/GluGluHToTauTauUncorrelatedDecayFilteredM125_RunIIFall17MiniAODv2_PU2017_13TeV_MINIAOD_powheg-pythia8.root"]
    vars_list = ["eta_1","eta_2","m_vis","met","mt_1","mt_2","pt_1","pt_2","ptvis","phi_1","phi_2"]
    vars_extra = ["Tau1E","Tau1Px","Tau1Py","Tau1Pz","Tau2E","Tau2Px","Tau2Py","Tau2Pz"]
    counter = 0

    #Settings
    tauSpinnerWeight_steps = ["000","010","020","030","040","050","060","070","080","090","100"]
    tauSpinnerWeight_addsteps = ["110","120","130","140","150","160","170","180","190","200"]

    #defining variables, read in info from json file and open csv file
    csv_train = open(output_directory + "csv_" + version + "_train.csv", "w")
    csv_valid = open(output_directory + "csv_" + version + "_valid.csv", "w")

    csv_header_string = ""
    for v in vars_list+vars_extra:
        csv_header_string += v + ","

    csv_header_string += "PhiStarCP,decayModeMVA_2" #dont end on comma here

    for i in tauSpinnerWeight_steps+tauSpinnerWeight_addsteps:
        csv_header_string += "," + str(i)

    csv_train.write(csv_header_string + "\n")
    csv_valid.write(csv_header_string + "\n")

    for f in filelist:
        counter += 1
        rootFile = ROOT.TFile(sample_directory + f, "read")
        tree = rootFile.Get("mt_nominal/ntuple")
        entries = tree.GetEntries()

        for i in tqdm(range(200000), desc="{} out of {}".format(counter, len(filelist)), unit="events"):
            tree.GetEntry(i)

            decayModeMVA_2 = tree.GetLeaf("decayModeMVA_2").GetValue()
            wt_000 = tree.GetLeaf("tauSpinnerWeight000").GetValue()
            wt_050 = tree.GetLeaf("tauSpinnerWeight050").GetValue()
            wt_100 = tree.GetLeaf("tauSpinnerWeight100").GetValue()

            if decayModeMVA_2 == 1 and wt_000-wt_050 !=0:

                #read vars from tree
                csv_string = ""
                for vars in vars_list:
                    csv_string += str(tree.GetLeaf(vars).GetValue()) + ","

                #read reconstructed vars
                csv_string += str(tree.svfitTau1LV.E()) + ","
                csv_string += str(tree.svfitTau1LV.Px()) + ","
                csv_string += str(tree.svfitTau1LV.Py()) + ","
                csv_string += str(tree.svfitTau1LV.Pz()) + ","
                csv_string += str(tree.svfitTau2LV.E()) + ","
                csv_string += str(tree.svfitTau2LV.Px()) + ","
                csv_string += str(tree.svfitTau2LV.Py()) + ","
                csv_string += str(tree.svfitTau2LV.Pz()) + ","
                csv_string += str(tree.GetLeaf("recoPhiStarCPCombMergedHelrPVBS").GetValue()) + ","
                csv_string += str(decayModeMVA_2) # dont end on comma here

                #looping tauSpinnerWeight
                for step in tauSpinnerWeight_steps:
                    tauSpinnerWeightxxx = tree.GetLeaf("tauSpinnerWeight"+step).GetValue()
                    csv_string += "," + str(tauSpinnerWeightxxx)

                #Generating additional weights for mixing range pi to 2*pi
                for addstep in tauSpinnerWeight_addsteps:
                    mixing_angle = float(addstep) / 100 * np.pi / 2
                    new_tauSpinnerWeightxxx = calc_tauSpinnerWeight(wt_000,wt_050,wt_100, mixing_angle)
                    csv_string += "," + str(new_tauSpinnerWeightxxx)

                #write into csv file and plit into train and validation data
                if i%2 == 0:
                    csv_train.write(csv_string + "\n")
                else:
                    csv_valid.write(csv_string + "\n")

    csv_train.close()
    csv_valid.close()

#call DNN training for even and odd dataset
def do_training():
    print("Train model on dataset")
    model_train, history_train = DNN_mixingangle_multiclassing()
    print("plot loss and accuracy for both models")
    plot_acc_loss(history_train)

#Get results on test dataset with confusion matrix and dnn_score-Plot
def get_results():
    import numpy as np
    from sklearn.metrics import confusion_matrix
    from sklearn.metrics import roc_auc_score
    from sklearn.metrics import log_loss

    #load model
    model_train = keras.models.load_model(output_directory + "model_" + version + ".h5")
    #read in and shape test data
    df_valid = pd.read_csv(output_directory + "csv_" + version + "_valid.csv")
    x_eval, y_eval = get_DNN_input(df_valid)

    #testing on Test data
    predictions = model_train.predict(x_eval)

    test_loss, test_acc = model_train.evaluate(x_eval, y_eval, verbose=1)
    print("\nAccuracy on model: {}".format(test_acc))

    print(predictions[1])
    print(y_eval[1])


    #calculating and plotting confusion matrix
    pred_labels = np.argmax(predictions, axis=1)
    true_labels = np.argmax(y_eval, axis=1)

    plot_pred_diff(pred_labels,true_labels)
    plot_pred_dist(pred_labels,true_labels)

    cm = confusion_matrix(true_labels, pred_labels)
    cm = cm.astype("float") / cm.sum(axis=1)[:, np.newaxis]
    plot_confusion_matrix(cm, "evaluation")



################################################################################

def do_debug():

    df1 = pd.read_csv(output_directory + "csv_" + version + "_train.csv")
    print(df1.head())
    df2 = pd.read_csv(output_directory + "csv_" + version + "_valid.csv")
    print(df2.head())

    x, y = get_DNN_input(df2)
    print(x[1])
    print(y[1])

    #x_val = df1.pop("PhiStarCP").values
    #y_val = df1.pop("000").values

    def plot_spinweight(phicp,y):
        x = np.linspace(0,200,21)
        plt.figure()
        plt.xlabel("mixing angle in %")
        plt.ylabel("spinweight wt")
        plt.plot(x,y,label = phicp)
        plt.legend()
        plt.savefig(output_directory + "spinweight_" + version + ".png")
    #plot_spinweight(x[0][-1],y[1])

    def plot_phicpdist(x_array,x_weights):
        plt.figure()
        plt.xlabel("Phi CP")
        plt.hist(x_array,weights = x_weights,histtype = u"step",bins = 20,color="red")
        plt.hist(x_array,histtype = u"step",bins = 20,color="black")
        plt.savefig(output_directory + "phicpdist_" + version + ".png")

    #plot_phicpdist(x_val,y_val)

    df = pd.concat([df1,df2],axis =0,ignore_index = True)

    mixing_labels = ["000","010","020","030","040","050","060","070","080","090","100","110","120","130","140","150","160","170","180","190","200"]
    var_drop = ["decayModeMVA_2","eta_1","eta_2","m_vis","met","mt_1","mt_2","pt_1","pt_2","ptvis","phi_1","phi_2"] + ["Tau1E","Tau1Px","Tau1Py","Tau1Pz","Tau2E","Tau2Px","Tau2Py","Tau2Pz"]
    df = df.drop(var_drop, axis=1)

    split_range = len(df.columns.values.tolist()) - len(mixing_labels)
    x = df.iloc[:,:split_range].values
    y = df.iloc[:,split_range:].values

    x_var = df.pop("PhiStarCP").values
    y_var = np.argmax(y,axis=1)

    plt.figure()
    plt.xlabel("class index")
    plt.ylabel("PhiStarCP")
    plt.plot(y_var,x_var,".",color="blue")
    plt.savefig(output_directory + "datapoints_" + version + ".png")

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
