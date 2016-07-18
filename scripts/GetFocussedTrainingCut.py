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
	log.info("Generate BDThistograms.root with Double precision")
	tree = ""
	#create histogram
        BDThistSG = ROOT.TH1D("BDT-Sig", "Signal BDT-Scores", nbins, -1, 1)
	BDThistBG = ROOT.TH1D("BDT-Bcg", "Background BDT-Scores", nbins, -1, 1)
	
	log.debug("Fill signal histogram")
	for file in signalfiles:
		f = ROOT.TFile.Open(file, "read")
		tree = f.Get("SplitTree")
		for event in tree:
			#print event.BDTScore1
			if not hasattr(event, leaftocut):
				raise AttributeError("event has no attribute '%s'"%(leaftocut,))
			BDThistSG.Fill(getattr(event, leaftocut), event.eventWeight)
		f.Close()
	log.debug("Fill background histogram")
	for file in backgroundfiles:
                f = ROOT.TFile.Open(file, "read") 
                tree = f.Get("SplitTree")
                for event in tree:
                        #print event.BDTScore1
                        if not hasattr(event, leaftocut):
                                raise AttributeError("event has no attribute '%s'"%(leaftocut,))
			BDThistBG.Fill(getattr(event, leaftocut), event.eventWeight)
                f.Close()

	store_file = ROOT.TFile(os.path.join(outputdir, "BDThistograms.root"), "RECREATE")
     
	#calculate histogram integrals for normalization
	integralSG = BDThistSG.Integral()
	integralBG = BDThistBG.Integral()
	#create cumulated histograms
	BDThistCUMSG = ROOT.TH1D("Sig-Eff", "Signal-Efficiency", nbins-1, -1.0+1.0/nbins, 1.0-1.0/nbins)
	BDThistCUMBG = ROOT.TH1D("Bcg-Rjc", "Background-Rejection", nbins-1, -1, 1)
	sigeff = 1.
	bcgrej = 0.
	log.debug("Fill cumulated histograms")
	for i in range(1,nbins):
		sigeff -= BDThistSG.GetBinContent(i)/integralSG
		bcgrej += BDThistBG.GetBinContent(i)/integralBG		
		BDThistCUMSG.SetBinContent(i, sigeff)
		BDThistCUMBG.SetBinContent(i, bcgrej)

	BDThistSG.Write()
	BDThistBG.Write()
	BDThistCUMSG.Write()
	BDThistCUMBG.Write()
	
	log.debug("Find cut. Cut method: " + method + "; Parameter: " + str(parameter))
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
	if method == "backgroundrej":	#parameter = desired background rejection
		cutbin = 1
		#find optimal BDT score to cut
		for i in range (2,nbins):
			if abs(parameter-BDThistCUMBG.GetBinContent(i)) <= abs(parameter-BDThistCUMBG.GetBinContent(cutbin)):
				cutbin = i
			else:
				break
	if method == "bargaining":	#parameter = what percentage of background rejection is one percent of signal efficiency worth?
		cutbin = 1
		profit = parameter*BDThistCUMSG.GetBinContent(cutbin)+BDThistCUMBG.GetBinContent(cutbin)
		#find optimal BDT score to cut
		for i in range (2,nbins):
			if parameter*BDThistCUMSG.GetBinContent(i)+BDThistCUMBG.GetBinContent(i) > profit:
				cutbin = i
				profit = parameter*BDThistCUMSG.GetBinContent(i)+BDThistCUMBG.GetBinContent(i)
	#end of metric definitions 
	cutSGeff = BDThistCUMSG.GetBinContent(cutbin)
	cutBGrej = BDThistCUMBG.GetBinContent(cutbin)
	if cutbin == 0:
		raise StandardError("Was not able to find cut value! Check whether you have chosen a proper cut method.")
	else:
		cutvalue =  BDThistCUMSG.GetBinCenter(cutbin)
		log.info("Signal efficiency of chosen cut at BDT score " + str(cutvalue) + ": " + str(cutSGeff))
		log.info("Background rejection of chosen cut at BDT score " + str(cutvalue) + ": " + str(cutBGrej))
	store_file.Close()
	return cutvalue, cutSGeff, cutBGrej
  
if __name__ == "__main__":
	files1 = ["Bargaining2/Loop1/storage/L1_vbfggh_vs_default_storage_qqh_split1.root", "Bargaining2/Loop1/storage/L1_vbfggh_vs_default_storage_qqh_split2.root", "Bargaining2/Loop1/storage/L1_vbfggh_vs_default_storage_ggh_split1.root", "Bargaining2/Loop1/storage/L1_vbfggh_vs_default_storage_ggh_split2.root"]
	files2 = ["Bargaining2/Loop1/storage/L1_vbfggh_vs_default_storage_ggh_split1.root", "Bargaining2/Loop1/storage/L1_vbfggh_vs_default_storage_ggh_split2.root"]
	print get_cut("./", files1, files2, "BDTScore1", "signaleff", 0.5)
