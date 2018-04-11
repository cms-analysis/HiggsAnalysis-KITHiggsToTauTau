#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import array
import argparse
import os
import math

import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gErrorIgnoreLevel = ROOT.kError
import Artus.HarryPlotter.utility.roottools as roottools
import Artus.Utility.tfilecontextmanager as tfilecontextmanager


eta_string_to_float = {
	"EtaLt1p48"    : 0.5,
	"EtaGt1p48"    : 2.0,
	"Eta1p48to2p1" : 2.0,
	"EtaGt2p1"     : 2.2,
	"EtaLt0p9"     : 0.5,
	"EtaGt0p9"     : 1.0,
	"Eta0p9to1p2"  : 1.0,
	"Eta0p9to2p1"  : 1.0,
	"EtaGt1p2"     : 2.0,
	"Eta1p2to2p1"  : 1.5,
	"EtaGt2p1"     : 2.2
}

if __name__ == "__main__":

	parser = argparse.ArgumentParser(description="Convert efficiencies ROOT files from DESY-like format to ROOT inputs usable by Artus)", parents=[logger.loggingParser])

	parser.add_argument("-i", "--input-dir", required=True,
	                    help="Input directory (for example $CMSSW_BASE/src/LeptonEfficiencies).")
	parser.add_argument("-o", "--output", default="$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/",
	                    help="Output folder. [Default: %(default)s]")

	args = parser.parse_args()
	logger.initLogger(args)
	
	input_dir = os.path.join(args.input_dir)
	for directory in os.listdir(input_dir):

		# skip README files and git folders
		if (os.path.isfile(os.path.join(input_dir, directory)) or directory == ".git"):
			continue
		
		log.info("Producing ROOT files for object \"%s\"" % directory)
		file_dir = os.path.join(args.input_dir, directory)
		print "file", file_dir
		for file_name in os.listdir(file_dir):
			outFolderName = "identificationWeights" if ("IdIso" in file_name) else "triggerWeights"
			outFolderPath = os.path.join(args.output, outFolderName)
			
			log.info("\tConverting file \"%s\"" % file_name)
			f = ROOT.TFile(os.path.join(file_dir, file_name), "READ")
			etaBinsHisto = f.Get("etaBinsH")
			eta_labels = []
			for eta_bin in range(1, etaBinsHisto.GetNbinsX()+1):
				eta_labels.append(etaBinsHisto.GetXaxis().GetBinLabel(eta_bin))
			
			firstGraph = f.Get("ZMass"+eta_labels[0]+"_Data")
			if directory == "Electron":
				yBinslist = [-2.5, -2.1, -1.48, 0.0, 1.48, 2.1, 2.5]
			elif directory == "Muon":
				yBinslist = [-2.5, -2.1, -1.2, -0.9, 0.0, 0.9, 1.2, 2.1, 2.5]
			
			xBinslist = []
			xBinslist.append(0)
			
			for ipoint in range(0, firstGraph.GetN() - 1):
				x, y = ROOT.Double(0), ROOT.Double(0)
				firstGraph.GetPoint(ipoint, x, y)
				xErrHigh = firstGraph.GetErrorXhigh(ipoint)
				
				xBinslist.append(x + xErrHigh)
			
			pt_bins = array.array("d", xBinslist)
			eta_bins = array.array("d", yBinslist)
			
			for datatype in ["Data","MC"]:
				typelabel = "Run2017" if datatype == "Data" else "MCFall2017"
				effHistoName = "identificationEfficiency" if ("IdIso" in file_name) else "triggerEfficiency"
				outFileName = effHistoName+'_'+typelabel+'_'+file_name
				
				outFile = ROOT.TFile(os.path.join(outFolderPath, outFileName), "RECREATE")
				effHisto = ROOT.TH2F(effHistoName, effHistoName, len(pt_bins)-1, pt_bins, len(eta_bins)-1, eta_bins)
				
				for ieta in range(len(eta_labels)):
					graphName = "ZMass"+eta_labels[ieta]+"_"+datatype
					graph = f.Get("ZMass"+eta_labels[ieta]+"_"+datatype)
					eta = eta_string_to_float[eta_labels[ieta]]
					
					for ipoint in range(0, graph.GetN()):
						pt, eff = ROOT.Double(0), ROOT.Double(0)
						graph.GetPoint(ipoint, pt, eff)
						effError = graph.GetErrorY(ipoint)
						
						ptBin = effHisto.GetXaxis().FindBin(pt)
						etaBin = effHisto.GetYaxis().FindBin(eta)
						effHisto.SetBinContent(ptBin, etaBin, eff)
						effHisto.SetBinError(ptBin, etaBin, effError)
						
						etaBin = effHisto.GetYaxis().FindBin(-1.0 * eta)
						effHisto.SetBinContent(ptBin, etaBin, eff)
						effHisto.SetBinError(ptBin, etaBin, effError)
			
				effHisto.Write()
				outFile.Close()
				log.info("\tConverted %s file in \"%s\"" % (datatype, os.path.join(outFolderPath, outFileName)))
			
			f.Close()
