import ROOT
import sys
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.samples_run2_2016 as samples
from pprint import pprint
import glob
import subprocess


##Define constants
sample_dir = "/net/scratch_cms3b/brunner/artus/AllSamples/merged/"
tree_name = "{channel}_nominal/ntuple"
output_root = "$CMSSW_BASE/src/plots/FlavioOutput/{channel}_MVA.root"

sig_list = ["zem"]
bkg_list = ["ztt", "zll", "ttj", "vv", "wj"]
parameter = ["pt_1", "pt_2", "d0_refitPV_1", "d0_refitPV_2", "diLepLV.Pt()", "met", "pZetaMissVis", "phi_1 - phi_2", "m_vis"]


def get_input_files(channel):
	sample_settings = samples.Samples()
	mc_list = []

	for sample_list in [sig_list, bkg_list]:
		mc_set = set()
		config = sample_settings.get_config(samples=[getattr(samples.Samples, sample) for sample in sample_list], channel = channel, category = None, cut_type = "lfv")
		mc_set.update([glob.glob(sample_dir + mc_name)[0] for mc_name in [file_name for file_list in [config_string.split(" ") for config_string in config["files"]] for file_name in file_list]])
		mc_list.append(list(mc_set))

	return mc_list

def MVA(channel, mc_list):
	output = ROOT.TFile(output_root.format(channel=channel), "RECREATE")
	factory = ROOT.TMVA.Factory(channel, output)

	sig_trees = ROOT.TChain(tree_name.format(channel = channel))
	bkg_trees = ROOT.TChain(tree_name.format(channel = channel))

	for sig_file in mc_list[0]:
		sig_trees.Add(sig_file)

	for bkg_file in mc_list[1]:
		bkg_trees.Add(bkg_file)			
	
	for param in parameter:
		factory.AddVariable(param)

	
	factory.AddSignalTree(sig_trees)
	factory.AddBackgroundTree(bkg_trees)

	n_option = ROOT.TString("nTrain_Signal=4500:nTest_Signal=4500:nTrain_Background=4500:nTest_Background=4500:SplitMode=Random",)

	factory.PrepareTrainingAndTestTree(ROOT.TCut("d0_refitPV_2 > -900 && d0_refitPV_1 > -900"), ROOT.TCut("d0_refitPV_2 > -900 && d0_refitPV_1 > -900"), n_option)
	factory.BookMethod(ROOT.TMVA.Types.kBDT, "BDT", "!H:!V:NTrees=850:MinNodeSize=2.5%:MaxDepth=3:BoostType=AdaBoost:AdaBoostBeta=0.5:UseBaggedBoost:BaggedSampleFraction=0.5:SeparationType=GiniIndex:nCuts=20")

	factory.TrainAllMethods()
	factory.TestAllMethods()
	factory.EvaluateAllMethods()
	output.Close()


def main():

	mc_list = get_input_files("et")	
	MVA("et", mc_list)
	ROOT.TMVA.TMVAGui("$CMSSW_BASE/src/plots/FlavioOutput/{channel}_MVA.root".format(channel="et"))
	raw_input("Press Enter to exit")
		
main()
