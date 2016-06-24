import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)
import sys
import os
import ROOT
import array
import Artus.Utility.jsonTools as jsonTools
ROOT.PyConfig.IgnoreCommandLineOptions = True

def get_cut(outputdir, signalfiles, backgroundfiles, leaftocut, method, parameter, nbins=100):
	#store_file = ROOT.TFile("BDTHisto.root", "RECREATE")
	#tree_list = ROOT.TList()
	tree = ""
	#create histogram
        BDThistSG = ROOT.TH1F("BDT-Sig", "Signal BDT-Scores", nbins, -1, 1)
	BDThistBG = ROOT.TH1F("BDT-Bcg", "Background BDT-Scores", nbins, -1, 1)
	 
	for file in signalfiles:
		f = ROOT.TFile.Open(file, "read")
		tree = f.Get("SplitTree")
		for event in tree:
			#print event.BDTScore1
			if not hasattr(event, leaftocut):
				raise AttributeError("event has no attribute '%s'"%(leaftocut,))
			BDThistSG.Fill(getattr(event, leaftocut), event.eventWeight)
		f.Close()
	for file in backgroundfiles:
                f = ROOT.TFile.Open(file, "read") 
                tree = f.Get("SplitTree")
                for event in tree:
                        #print event.BDTScore1
                        if not hasattr(event, leaftocut):
                                raise AttributeError("event has no attribute '%s'"%(leaftocut,))
			BDThistBG.Fill(getattr(event, leaftocut), event.eventWeight)
                f.Close()
	#create histogram
	#BDThist = ROOT.TH1F("BDT-Score", "weighted number of events", 100, -1, 1)
	#bincontent = BDThist.GetBinContent(1...100)
	store_file = ROOT.TFile(os.path.join(outputdir, "BDThistograms.root"), "RECREATE")
     
	#calculate histogram integrals for normalization
	integralSG = BDThistSG.Integral()
	integralBG = 1.#BDThistBG.ComputeIntegral()
	#create cumulated histograms
	BDThistCUMSG = ROOT.TH1F("Sig-Eff", "Signal-Efficiency", nbins-1, -1.0+1.0/nbins, 1.0-1.0/nbins)
	BDThistCUMBG = ROOT.TH1F("Bcg-Rjc", "Background-Rejection", nbins-1, -1, 1)
	sigeff = 1.
	bcgrej = 0.
	for i in range(1,nbins):
		sigeff -= BDThistSG.GetBinContent(i)/integralSG
		bcgrej += BDThistBG.GetBinContent(i)/integralBG		
		BDThistCUMSG.SetBinContent(i, sigeff)
		BDThistCUMBG.SetBinContent(i, bcgrej)

	BDThistSG.Write()
	BDThistBG.Write()
	BDThistCUMSG.Write()
	BDThistCUMBG.Write()
	
	cutbin = 0
	#Available metrics for cut determination:
	if method == "signaleff":	#parameter = desired signal efficiency
		cutbin = 1
		#find optimal BDT score to cut
		for i in range (2,nbins):
			if abs(parameter-BDThistCUMSG.GetBinContent(i)) <= abs(parameter-BDThistCUMSG.GetBinContent(cutbin)):
				cutbin = i
			else:
				break
	
	#end of metric definitions 
	if cutbin == 0:
		raise StandardError("Was not able to find cut value!")
	else:
		cutvalue =  BDThistCUMSG.GetBinCenter(cutbin)
	store_file.Close()
	return cutvalue
  
if __name__ == "__main__":
	files1 = ["test6/Loop1/storage/vbf_vs_ggh_storage_qqh_split1.root", "test6/Loop1/storage/vbf_vs_ggh_storage_qqh_split2.root"]
	files2 = ["test6/Loop1/storage/vbf_vs_ggh_storage_ggh_split1.root", "test6/Loop1/storage/vbf_vs_ggh_storage_ggh_split2.root"]
	print get_cut("test6/Loop1", files1, files2, "BDTScore1", "signaleff", 0.5)
