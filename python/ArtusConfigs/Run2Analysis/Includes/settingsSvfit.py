# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import re
import json
import Artus.Utility.jsonTools as jsonTools
import Kappa.Skimming.datasetsHelperTwopz as datasetsHelperTwopz
import copy

class Svfit(dict):
	def __init__(self, nickname):
		self["SvfitIntegrationMethod"] = "MarkovChain"
		self["GenerateSvfitInput"] = False
		self["UseFirstInputFileNameForSvfit"] = False
		self["SvfitCacheMissBehaviour"] = "recalculate"
		self["SvfitInputCutOff"] = 10000
		self["UpdateSvfitCache"] = True
		self["SvfitOutFile"] = "SvfitCache.root"

		self["SvfitCacheFile"] = self.__getsvfitCacheFile__(nickname)


	def __getsvfitCacheFile__(self, nickname):

		if (nickname == "DY1JetsToLLM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8"): 
 			return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/DY1JetsToLLM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8.root"

		elif (nickname == "DY2JetsToLLM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/DY2JetsToLLM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8.root"

		elif (nickname == "DY3JetsToLLM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/DY3JetsToLLM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8.root"

		elif (nickname == "DY4JetsToLLM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/DY4JetsToLLM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8.root"

		elif (nickname == "DYJetsToLLM10to50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/DYJetsToLLM10to50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8.root"

		elif (nickname == "DYJetsToLLM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext1"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/DYJetsToLLM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext1.root"

		elif (nickname == "DYJetsToLLM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext2"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/DYJetsToLLM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext2.root"

		elif (nickname == "DoubleEG_Run2016B_03Feb2017ver2v2_13TeV_MINIAOD"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/DoubleEG_Run2016B_03Feb2017ver2v2_13TeV_MINIAOD.root"

		elif (nickname == "DoubleEG_Run2016C_03Feb2017v1_13TeV_MINIAOD"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/DoubleEG_Run2016C_03Feb2017v1_13TeV_MINIAOD.root"

		elif (nickname == "DoubleEG_Run2016D_03Feb2017v1_13TeV_MINIAOD"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/DoubleEG_Run2016D_03Feb2017v1_13TeV_MINIAOD.root"

		elif (nickname == "DoubleEG_Run2016E_03Feb2017v1_13TeV_MINIAOD"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/DoubleEG_Run2016E_03Feb2017v1_13TeV_MINIAOD.root"

		elif (nickname == "DoubleEG_Run2016F_03Feb2017v1_13TeV_MINIAOD"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/DoubleEG_Run2016F_03Feb2017v1_13TeV_MINIAOD.root"

		elif (nickname == "DoubleEG_Run2016G_03Feb2017v1_13TeV_MINIAOD"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/DoubleEG_Run2016G_03Feb2017v1_13TeV_MINIAOD.root"

		elif (nickname == "DoubleEG_Run2016H_03Feb2017ver2v1_13TeV_MINIAOD"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/DoubleEG_Run2016H_03Feb2017ver2v1_13TeV_MINIAOD.root"

		elif (nickname == "DoubleEG_Run2016H_03Feb2017ver3v1_13TeV_MINIAOD"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/DoubleEG_Run2016H_03Feb2017ver3v1_13TeV_MINIAOD.root"

		elif (nickname == "DoubleMuon_Run2016B_03Feb2017ver2v2_13TeV_MINIAOD"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/DoubleMuon_Run2016B_03Feb2017ver2v2_13TeV_MINIAOD.root"

		elif (nickname == "DoubleMuon_Run2016C_03Feb2017v1_13TeV_MINIAOD"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/DoubleMuon_Run2016C_03Feb2017v1_13TeV_MINIAOD.root"

		elif (nickname == "DoubleMuon_Run2016D_03Feb2017v1_13TeV_MINIAOD"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/DoubleMuon_Run2016D_03Feb2017v1_13TeV_MINIAOD.root"

		elif (nickname == "DoubleMuon_Run2016E_03Feb2017v1_13TeV_MINIAOD"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/DoubleMuon_Run2016E_03Feb2017v1_13TeV_MINIAOD.root"

		elif (nickname == "DoubleMuon_Run2016F_03Feb2017v1_13TeV_MINIAOD"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/DoubleMuon_Run2016F_03Feb2017v1_13TeV_MINIAOD.root"

		elif (nickname == "DoubleMuon_Run2016G_03Feb2017v1_13TeV_MINIAOD"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/DoubleMuon_Run2016G_03Feb2017v1_13TeV_MINIAOD.root"

		elif (nickname == "DoubleMuon_Run2016H_03Feb2017ver2v1_13TeV_MINIAOD"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/DoubleMuon_Run2016H_03Feb2017ver2v1_13TeV_MINIAOD.root"

		elif (nickname == "DoubleMuon_Run2016H_03Feb2017ver3v1_13TeV_MINIAOD"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/DoubleMuon_Run2016H_03Feb2017ver3v1_13TeV_MINIAOD.root"

		elif (nickname == "EWKWMinus2JetsWToLNuM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/EWKWMinus2JetsWToLNuM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8.root"

		elif (nickname == "EWKWMinus2JetsWToLNuM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext1"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/EWKWMinus2JetsWToLNuM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext1.root"

		elif (nickname == "EWKWMinus2JetsWToLNuM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext2"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/EWKWMinus2JetsWToLNuM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext2.root"

		elif (nickname == "EWKWPlus2JetsWToLNuM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/EWKWPlus2JetsWToLNuM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8.root"

		elif (nickname == "EWKWPlus2JetsWToLNuM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext1"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/EWKWPlus2JetsWToLNuM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext1.root"

		elif (nickname == "EWKWPlus2JetsWToLNuM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext2"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/EWKWPlus2JetsWToLNuM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext2.root"

		elif (nickname == "EWKZ2JetsZToLLM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/EWKZ2JetsZToLLM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8.root"

		elif (nickname == "EWKZ2JetsZToLLM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext1"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/EWKZ2JetsZToLLM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext1.root"

		elif (nickname == "EWKZ2JetsZToLLM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext2"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/EWKZ2JetsZToLLM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext2.root"

		elif (nickname == "EWKZ2Jets_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/EWKZ2Jets_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8.root"

		elif (nickname == "EWKZ2Jets_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext1"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/EWKZ2Jets_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext1.root"

		elif (nickname == "EWKZ2Jets_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext2"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/EWKZ2Jets_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext2.root"

		elif (nickname == "GluGluHToTauTauM110_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/GluGluHToTauTauM110_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root"

		elif (nickname == "GluGluHToTauTauM120_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8_ext1"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/GluGluHToTauTauM120_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8_ext1.root"

		elif (nickname == "GluGluHToTauTauM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/GluGluHToTauTauM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root"

		elif (nickname == "GluGluHToTauTauM130_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8_ext1"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/GluGluHToTauTauM130_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8_ext1.root"

		elif (nickname == "GluGluHToTauTauM140_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/GluGluHToTauTauM140_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root"

		elif (nickname == "GluGluHToWWTo2L2NuM120_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/GluGluHToWWTo2L2NuM120_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root"

		elif (nickname == "GluGluHToWWTo2L2NuM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/GluGluHToWWTo2L2NuM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root"

		elif (nickname == "GluGluHToWWTo2L2NuM130_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/GluGluHToWWTo2L2NuM130_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root"

		elif (nickname == "MuonEG_Run2016B_03Feb2017ver2v2_13TeV_MINIAOD"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/MuonEG_Run2016B_03Feb2017ver2v2_13TeV_MINIAOD.root"

		elif (nickname == "MuonEG_Run2016C_03Feb2017v1_13TeV_MINIAOD"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/MuonEG_Run2016C_03Feb2017v1_13TeV_MINIAOD.root"

		elif (nickname == "MuonEG_Run2016D_03Feb2017v1_13TeV_MINIAOD"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/MuonEG_Run2016D_03Feb2017v1_13TeV_MINIAOD.root"

		elif (nickname == "MuonEG_Run2016E_03Feb2017v1_13TeV_MINIAOD"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/MuonEG_Run2016E_03Feb2017v1_13TeV_MINIAOD.root"

		elif (nickname == "MuonEG_Run2016F_03Feb2017v1_13TeV_MINIAOD"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/MuonEG_Run2016F_03Feb2017v1_13TeV_MINIAOD.root"

		elif (nickname == "MuonEG_Run2016G_03Feb2017v1_13TeV_MINIAOD"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/MuonEG_Run2016G_03Feb2017v1_13TeV_MINIAOD.root"

		elif (nickname == "MuonEG_Run2016H_03Feb2017ver2v1_13TeV_MINIAOD"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/MuonEG_Run2016H_03Feb2017ver2v1_13TeV_MINIAOD.root"

		elif (nickname == "MuonEG_Run2016H_03Feb2017ver3v1_13TeV_MINIAOD"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/MuonEG_Run2016H_03Feb2017ver3v1_13TeV_MINIAOD.root"

		elif (nickname == "STt-channelantitop4finclusiveDecays_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/STt-channelantitop4finclusiveDecays_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root"

		elif (nickname == "STt-channeltop4finclusiveDecays_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/STt-channeltop4finclusiveDecays_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root"

		elif (nickname == "STtWantitop5finclusiveDecays_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8_ext1"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/STtWantitop5finclusiveDecays_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8_ext1.root"

		elif (nickname == "STtWtop5finclusiveDecays_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8_ext1"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/STtWtop5finclusiveDecays_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8_ext1.root"

		elif (nickname == "SingleElectron_Run2016B_03Feb2017ver2v2_13TeV_MINIAOD"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/SingleElectron_Run2016B_03Feb2017ver2v2_13TeV_MINIAOD.root"

		elif (nickname == "SingleElectron_Run2016C_03Feb2017v1_13TeV_MINIAOD"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/SingleElectron_Run2016C_03Feb2017v1_13TeV_MINIAOD.root"

		elif (nickname == "SingleElectron_Run2016D_03Feb2017v1_13TeV_MINIAOD"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/SingleElectron_Run2016D_03Feb2017v1_13TeV_MINIAOD.root"

		elif (nickname == "SingleElectron_Run2016E_03Feb2017v1_13TeV_MINIAOD"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/SingleElectron_Run2016E_03Feb2017v1_13TeV_MINIAOD.root"

		elif (nickname == "SingleElectron_Run2016F_03Feb2017v1_13TeV_MINIAOD"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/SingleElectron_Run2016F_03Feb2017v1_13TeV_MINIAOD.root"

		elif (nickname == "SingleElectron_Run2016G_03Feb2017v1_13TeV_MINIAOD"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/SingleElectron_Run2016G_03Feb2017v1_13TeV_MINIAOD.root"

		elif (nickname == "SingleElectron_Run2016H_03Feb2017ver2v1_13TeV_MINIAOD"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/SingleElectron_Run2016H_03Feb2017ver2v1_13TeV_MINIAOD.root"

		elif (nickname == "SingleElectron_Run2016H_03Feb2017ver3v1_13TeV_MINIAOD"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/SingleElectron_Run2016H_03Feb2017ver3v1_13TeV_MINIAOD.root"

		elif (nickname == "SingleMuon_Run2016B_03Feb2017ver2v2_13TeV_MINIAOD"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/SingleMuon_Run2016B_03Feb2017ver2v2_13TeV_MINIAOD.root"

		elif (nickname == "SingleMuon_Run2016C_03Feb2017v1_13TeV_MINIAOD"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/SingleMuon_Run2016C_03Feb2017v1_13TeV_MINIAOD.root"

		elif (nickname == "SingleMuon_Run2016D_03Feb2017v1_13TeV_MINIAOD"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/SingleMuon_Run2016D_03Feb2017v1_13TeV_MINIAOD.root"

		elif (nickname == "SingleMuon_Run2016E_03Feb2017v1_13TeV_MINIAOD"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/SingleMuon_Run2016E_03Feb2017v1_13TeV_MINIAOD.root"

		elif (nickname == "SingleMuon_Run2016F_03Feb2017v1_13TeV_MINIAOD"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/SingleMuon_Run2016F_03Feb2017v1_13TeV_MINIAOD.root"

		elif (nickname == "SingleMuon_Run2016G_03Feb2017v1_13TeV_MINIAOD"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/SingleMuon_Run2016G_03Feb2017v1_13TeV_MINIAOD.root"

		elif (nickname == "SingleMuon_Run2016H_03Feb2017ver2v1_13TeV_MINIAOD"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/SingleMuon_Run2016H_03Feb2017ver2v1_13TeV_MINIAOD.root"

		elif (nickname == "SingleMuon_Run2016H_03Feb2017ver3v1_13TeV_MINIAOD"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/SingleMuon_Run2016H_03Feb2017ver3v1_13TeV_MINIAOD.root"

		elif (nickname == "TT_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/TT_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root"

		elif (nickname == "Tau_Run2016B_03Feb2017ver2v2_13TeV_MINIAOD"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/Tau_Run2016B_03Feb2017ver2v2_13TeV_MINIAOD.root"

		elif (nickname == "Tau_Run2016C_03Feb2017v1_13TeV_MINIAOD"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/Tau_Run2016C_03Feb2017v1_13TeV_MINIAOD.root"

		elif (nickname == "Tau_Run2016D_03Feb2017v1_13TeV_MINIAOD"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/Tau_Run2016D_03Feb2017v1_13TeV_MINIAOD.root"

		elif (nickname == "Tau_Run2016E_03Feb2017v1_13TeV_MINIAOD"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/Tau_Run2016E_03Feb2017v1_13TeV_MINIAOD.root"

		elif (nickname == "Tau_Run2016F_03Feb2017v1_13TeV_MINIAOD"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/Tau_Run2016F_03Feb2017v1_13TeV_MINIAOD.root"

		elif (nickname == "Tau_Run2016G_03Feb2017v1_13TeV_MINIAOD"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/Tau_Run2016G_03Feb2017v1_13TeV_MINIAOD.root"

		elif (nickname == "Tau_Run2016H_03Feb2017ver2v1_13TeV_MINIAOD"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/Tau_Run2016H_03Feb2017ver2v1_13TeV_MINIAOD.root"

		elif (nickname == "Tau_Run2016H_03Feb2017ver3v1_13TeV_MINIAOD"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/Tau_Run2016H_03Feb2017ver3v1_13TeV_MINIAOD.root"

		elif (nickname == "VBFHToTauTauM110_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/VBFHToTauTauM110_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root"

		elif (nickname == "VBFHToTauTauM120_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8_ext1"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/VBFHToTauTauM120_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8_ext1.root"

		elif (nickname == "VBFHToTauTauM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/VBFHToTauTauM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root"

		elif (nickname == "VBFHToTauTauM130_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8_ext1"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/VBFHToTauTauM130_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8_ext1.root"

		elif (nickname == "VBFHToTauTauM140_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/VBFHToTauTauM140_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root"

		elif (nickname == "VBFHToWWTo2L2NuM120_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/VBFHToWWTo2L2NuM120_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root"

		elif (nickname == "VBFHToWWTo2L2NuM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/VBFHToWWTo2L2NuM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root"

		elif (nickname == "VBFHToWWTo2L2NuM130_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/VBFHToWWTo2L2NuM130_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root"

		elif (nickname == "VVTo2L2Nu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_amcatnlo-pythia8"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/VVTo2L2Nu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_amcatnlo-pythia8.root"

		elif (nickname == "VVTo2L2Nu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_amcatnlo-pythia8_ext1"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/VVTo2L2Nu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_amcatnlo-pythia8_ext1.root"

		elif (nickname == "W1JetsToLNu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/W1JetsToLNu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8.root"

		elif (nickname == "W2JetsToLNu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/W2JetsToLNu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8.root"

		elif (nickname == "W2JetsToLNu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext1"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/W2JetsToLNu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext1.root"

		elif (nickname == "W3JetsToLNu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/W3JetsToLNu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8.root"

		elif (nickname == "W3JetsToLNu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext1"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/W3JetsToLNu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext1.root"

		elif (nickname == "W4JetsToLNu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/W4JetsToLNu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8.root"

		elif (nickname == "W4JetsToLNu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext1"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/W4JetsToLNu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext1.root"

		elif (nickname == "W4JetsToLNu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext2"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/W4JetsToLNu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext2.root"

		elif (nickname == "WGToLNuG_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_amcatnlo-pythia8_ext1"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/WGToLNuG_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_amcatnlo-pythia8_ext1.root"

		elif (nickname == "WGToLNuG_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_amcatnlo-pythia8_ext2"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/WGToLNuG_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_amcatnlo-pythia8_ext2.root"

		elif (nickname == "WGToLNuG_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_amcatnlo-pythia8_ext3"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/WGToLNuG_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_amcatnlo-pythia8_ext3.root"

		elif (nickname == "WGstarToLNuEE_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/WGstarToLNuEE_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph.root"

		elif (nickname == "WGstarToLNuMuMu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/WGstarToLNuMuMu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph.root"

		elif (nickname == "WJetsToLNu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/WJetsToLNu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8.root"

		elif (nickname == "WJetsToLNu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext2"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/WJetsToLNu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext2.root"

		elif (nickname == "WWTo1L1Nu2Q_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_amcatnlo-pythia8"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/WWTo1L1Nu2Q_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_amcatnlo-pythia8.root"

		elif (nickname == "WZJToLLLNu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_pythia8"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/WZJToLLLNu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_pythia8.root"

		elif (nickname == "WZTo1L1Nu2Q_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_amcatnlo-pythia8"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/WZTo1L1Nu2Q_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_amcatnlo-pythia8.root"

		elif (nickname == "WZTo1L3Nu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_amcatnlo-pythia8"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/WZTo1L3Nu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_amcatnlo-pythia8.root"

		elif (nickname == "WZTo2L2Q_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_amcatnlo-pythia8"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/WZTo2L2Q_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_amcatnlo-pythia8.root"

		elif (nickname == "WminusHToTauTauM110_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/WminusHToTauTauM110_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root"

		elif (nickname == "WminusHToTauTauM120_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/WminusHToTauTauM120_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root"

		elif (nickname == "WminusHToTauTauM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/WminusHToTauTauM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root"

		elif (nickname == "WminusHToTauTauM130_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/WminusHToTauTauM130_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root"

		elif (nickname == "WminusHToTauTauM140_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/WminusHToTauTauM140_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root"

		elif (nickname == "WplusHToTauTauM110_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/WplusHToTauTauM110_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root"

		elif (nickname == "WplusHToTauTauM120_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/WplusHToTauTauM120_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root"

		elif (nickname == "WplusHToTauTauM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/WplusHToTauTauM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root"

		elif (nickname == "WplusHToTauTauM130_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/WplusHToTauTauM130_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root"

		elif (nickname == "WplusHToTauTauM140_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/WplusHToTauTauM140_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root"

		elif (nickname == "ZHToTauTauM110_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/ZHToTauTauM110_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root"

		elif (nickname == "ZHToTauTauM120_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/ZHToTauTauM120_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root"

		elif (nickname == "ZHToTauTauM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/ZHToTauTauM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root"

		elif (nickname == "ZHToTauTauM130_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/ZHToTauTauM130_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root"

		elif (nickname == "ZHToTauTauM140_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/ZHToTauTauM140_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root"

		elif (nickname == "ZZTo2L2Q_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_amcatnlo-pythia8"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/ZZTo2L2Q_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_amcatnlo-pythia8.root"

		elif (nickname == "ZZTo4L_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_amcatnlo-pythia8_ext1"): 
  			 return "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2017-05-28_20-05/ZZTo4L_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_amcatnlo-pythia8_ext1.root"




