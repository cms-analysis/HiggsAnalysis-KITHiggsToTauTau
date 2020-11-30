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
		#self["SvfitIntegrationMethod"] = "MarkovChain"
		self["GenerateSvfitInput"] = False
		self["UseFirstInputFileNameForSvfit"] = False
		self["SvfitCacheMissBehaviour"] = "recalculate"
		self["SvfitInputCutOff"] = 10000
		self["UpdateSvfitCache"] = True
		self["SvfitOutFile"] = "SvfitCache.root"

		self["#DiTauMassConstraint"] = 125.0

		self["SvfitCacheFile"] = self.__getsvfitCacheFile__(nickname)

		self["SvfitM91CacheFile"] = self.__getsvfitM91CacheFile__(nickname)

		self["SvfitM125CacheFile"] = self.__getsvfitM125CacheFile__(nickname)


	def __getsvfitCacheFile__(self, nickname):

		if (nickname == "DY1JetsToLLM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/DY1JetsToLLM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8.root"

		elif (nickname == "DY2JetsToLLM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/DY2JetsToLLM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8.root"

		elif (nickname == "DY3JetsToLLM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/DY3JetsToLLM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8.root"

		elif (nickname == "DY4JetsToLLM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/DY4JetsToLLM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8.root"

		elif (nickname == "DYJetsToLLM10to50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/DYJetsToLLM10to50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8.root"

		elif (nickname == "DYJetsToLLM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext1"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/DYJetsToLLM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext1.root"

		elif (nickname == "DYJetsToLLM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext2"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/DYJetsToLLM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext2.root"

		elif (nickname == "DoubleEG_Run2016B_03Feb2017ver2v2_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/DoubleEG_Run2016B_03Feb2017ver2v2_13TeV_MINIAOD.root"

		elif (nickname == "DoubleEG_Run2016C_03Feb2017v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/DoubleEG_Run2016C_03Feb2017v1_13TeV_MINIAOD.root"

		elif (nickname == "DoubleEG_Run2016D_03Feb2017v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/DoubleEG_Run2016D_03Feb2017v1_13TeV_MINIAOD.root"

		elif (nickname == "DoubleEG_Run2016E_03Feb2017v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/DoubleEG_Run2016E_03Feb2017v1_13TeV_MINIAOD.root"

		elif (nickname == "DoubleEG_Run2016F_03Feb2017v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/DoubleEG_Run2016F_03Feb2017v1_13TeV_MINIAOD.root"

		elif (nickname == "DoubleEG_Run2016G_03Feb2017v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/DoubleEG_Run2016G_03Feb2017v1_13TeV_MINIAOD.root"

		elif (nickname == "DoubleEG_Run2016H_03Feb2017ver2v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/DoubleEG_Run2016H_03Feb2017ver2v1_13TeV_MINIAOD.root"

		elif (nickname == "DoubleEG_Run2016H_03Feb2017ver3v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/DoubleEG_Run2016H_03Feb2017ver3v1_13TeV_MINIAOD.root"

		elif (nickname == "DoubleMuon_Run2016B_03Feb2017ver2v2_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/DoubleMuon_Run2016B_03Feb2017ver2v2_13TeV_MINIAOD.root"

		elif (nickname == "DoubleMuon_Run2016C_03Feb2017v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/DoubleMuon_Run2016C_03Feb2017v1_13TeV_MINIAOD.root"

		elif (nickname == "DoubleMuon_Run2016D_03Feb2017v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/DoubleMuon_Run2016D_03Feb2017v1_13TeV_MINIAOD.root"

		elif (nickname == "DoubleMuon_Run2016E_03Feb2017v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/DoubleMuon_Run2016E_03Feb2017v1_13TeV_MINIAOD.root"

		elif (nickname == "DoubleMuon_Run2016F_03Feb2017v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/DoubleMuon_Run2016F_03Feb2017v1_13TeV_MINIAOD.root"

		elif (nickname == "DoubleMuon_Run2016G_03Feb2017v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/DoubleMuon_Run2016G_03Feb2017v1_13TeV_MINIAOD.root"

		elif (nickname == "DoubleMuon_Run2016H_03Feb2017ver2v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/DoubleMuon_Run2016H_03Feb2017ver2v1_13TeV_MINIAOD.root"

		elif (nickname == "DoubleMuon_Run2016H_03Feb2017ver3v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/DoubleMuon_Run2016H_03Feb2017ver3v1_13TeV_MINIAOD.root"

		elif (nickname == "EWKWMinus2JetsWToLNuM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/EWKWMinus2JetsWToLNuM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8.root"

		elif (nickname == "EWKWMinus2JetsWToLNuM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext1"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/EWKWMinus2JetsWToLNuM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext1.root"

		elif (nickname == "EWKWMinus2JetsWToLNuM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext2"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/EWKWMinus2JetsWToLNuM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext2.root"

		elif (nickname == "EWKWPlus2JetsWToLNuM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/EWKWPlus2JetsWToLNuM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8.root"

		elif (nickname == "EWKWPlus2JetsWToLNuM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext1"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/EWKWPlus2JetsWToLNuM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext1.root"

		elif (nickname == "EWKWPlus2JetsWToLNuM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext2"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/EWKWPlus2JetsWToLNuM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext2.root"

		elif (nickname == "EWKZ2JetsZToLLM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/EWKZ2JetsZToLLM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8.root"

		elif (nickname == "EWKZ2JetsZToLLM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext1"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/EWKZ2JetsZToLLM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext1.root"

		elif (nickname == "EWKZ2JetsZToLLM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext2"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/EWKZ2JetsZToLLM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext2.root"

		elif (nickname == "EWKZ2Jets_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/EWKZ2Jets_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8.root"

		elif (nickname == "EWKZ2Jets_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext1"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/EWKZ2Jets_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext1.root"

		elif (nickname == "EWKZ2Jets_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext2"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/EWKZ2Jets_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext2.root"

		elif (nickname == "GluGluHToTauTauM110_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/GluGluHToTauTauM110_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root"

		elif (nickname == "GluGluHToTauTauM120_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8_ext1"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/GluGluHToTauTauM120_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8_ext1.root"

		elif (nickname == "GluGluHToTauTauM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/GluGluHToTauTauM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root"

		elif (nickname == "GluGluHToTauTauM130_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8_ext1"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/GluGluHToTauTauM130_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8_ext1.root"

		elif (nickname == "GluGluHToTauTauM140_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/GluGluHToTauTauM140_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root"

		elif (nickname == "GluGluHToWWTo2L2NuM120_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/GluGluHToWWTo2L2NuM120_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root"

		elif (nickname == "GluGluHToWWTo2L2NuM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/GluGluHToWWTo2L2NuM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root"

		elif (nickname == "GluGluHToWWTo2L2NuM130_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/GluGluHToWWTo2L2NuM130_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root"

		elif (nickname == "MuonEG_Run2016B_03Feb2017ver2v2_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/MuonEG_Run2016B_03Feb2017ver2v2_13TeV_MINIAOD.root"

		elif (nickname == "MuonEG_Run2016C_03Feb2017v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/MuonEG_Run2016C_03Feb2017v1_13TeV_MINIAOD.root"

		elif (nickname == "MuonEG_Run2016D_03Feb2017v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/MuonEG_Run2016D_03Feb2017v1_13TeV_MINIAOD.root"

		elif (nickname == "MuonEG_Run2016E_03Feb2017v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/MuonEG_Run2016E_03Feb2017v1_13TeV_MINIAOD.root"

		elif (nickname == "MuonEG_Run2016F_03Feb2017v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/MuonEG_Run2016F_03Feb2017v1_13TeV_MINIAOD.root"

		elif (nickname == "MuonEG_Run2016G_03Feb2017v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/MuonEG_Run2016G_03Feb2017v1_13TeV_MINIAOD.root"

		elif (nickname == "MuonEG_Run2016H_03Feb2017ver2v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/MuonEG_Run2016H_03Feb2017ver2v1_13TeV_MINIAOD.root"

		elif (nickname == "MuonEG_Run2016H_03Feb2017ver3v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/MuonEG_Run2016H_03Feb2017ver3v1_13TeV_MINIAOD.root"

		elif (nickname == "STt-channelantitop4finclusiveDecays_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/STt-channelantitop4finclusiveDecays_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root"

		elif (nickname == "STt-channeltop4finclusiveDecays_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/STt-channeltop4finclusiveDecays_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root"

		elif (nickname == "STtWantitop5finclusiveDecays_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8_ext1"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/STtWantitop5finclusiveDecays_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8_ext1.root"

		elif (nickname == "STtWtop5finclusiveDecays_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8_ext1"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/STtWtop5finclusiveDecays_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8_ext1.root"

		elif (nickname == "SingleElectron_Run2016B_03Feb2017ver2v2_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/SingleElectron_Run2016B_03Feb2017ver2v2_13TeV_MINIAOD.root"

		elif (nickname == "SingleElectron_Run2016C_03Feb2017v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/SingleElectron_Run2016C_03Feb2017v1_13TeV_MINIAOD.root"

		elif (nickname == "SingleElectron_Run2016D_03Feb2017v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/SingleElectron_Run2016D_03Feb2017v1_13TeV_MINIAOD.root"

		elif (nickname == "SingleElectron_Run2016E_03Feb2017v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/SingleElectron_Run2016E_03Feb2017v1_13TeV_MINIAOD.root"

		elif (nickname == "SingleElectron_Run2016F_03Feb2017v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/SingleElectron_Run2016F_03Feb2017v1_13TeV_MINIAOD.root"

		elif (nickname == "SingleElectron_Run2016G_03Feb2017v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/SingleElectron_Run2016G_03Feb2017v1_13TeV_MINIAOD.root"

		elif (nickname == "SingleElectron_Run2016H_03Feb2017ver2v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/SingleElectron_Run2016H_03Feb2017ver2v1_13TeV_MINIAOD.root"

		elif (nickname == "SingleElectron_Run2016H_03Feb2017ver3v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/SingleElectron_Run2016H_03Feb2017ver3v1_13TeV_MINIAOD.root"

		elif (nickname == "SingleMuon_Run2016B_03Feb2017ver2v2_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/SingleMuon_Run2016B_03Feb2017ver2v2_13TeV_MINIAOD.root"

		elif (nickname == "SingleMuon_Run2016C_03Feb2017v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/SingleMuon_Run2016C_03Feb2017v1_13TeV_MINIAOD.root"

		elif (nickname == "SingleMuon_Run2016D_03Feb2017v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/SingleMuon_Run2016D_03Feb2017v1_13TeV_MINIAOD.root"

		elif (nickname == "SingleMuon_Run2016E_03Feb2017v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/SingleMuon_Run2016E_03Feb2017v1_13TeV_MINIAOD.root"

		elif (nickname == "SingleMuon_Run2016F_03Feb2017v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/SingleMuon_Run2016F_03Feb2017v1_13TeV_MINIAOD.root"

		elif (nickname == "SingleMuon_Run2016G_03Feb2017v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/SingleMuon_Run2016G_03Feb2017v1_13TeV_MINIAOD.root"

		elif (nickname == "SingleMuon_Run2016H_03Feb2017ver2v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/SingleMuon_Run2016H_03Feb2017ver2v1_13TeV_MINIAOD.root"

		elif (nickname == "SingleMuon_Run2016H_03Feb2017ver3v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/SingleMuon_Run2016H_03Feb2017ver3v1_13TeV_MINIAOD.root"

		elif (nickname == "TT_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/TT_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root"

		elif (nickname == "Tau_Run2016B_03Feb2017ver2v2_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/Tau_Run2016B_03Feb2017ver2v2_13TeV_MINIAOD.root"

		elif (nickname == "Tau_Run2016C_03Feb2017v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/Tau_Run2016C_03Feb2017v1_13TeV_MINIAOD.root"

		elif (nickname == "Tau_Run2016D_03Feb2017v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/Tau_Run2016D_03Feb2017v1_13TeV_MINIAOD.root"

		elif (nickname == "Tau_Run2016E_03Feb2017v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/Tau_Run2016E_03Feb2017v1_13TeV_MINIAOD.root"

		elif (nickname == "Tau_Run2016F_03Feb2017v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/Tau_Run2016F_03Feb2017v1_13TeV_MINIAOD.root"

		elif (nickname == "Tau_Run2016G_03Feb2017v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/Tau_Run2016G_03Feb2017v1_13TeV_MINIAOD.root"

		elif (nickname == "Tau_Run2016H_03Feb2017ver2v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/Tau_Run2016H_03Feb2017ver2v1_13TeV_MINIAOD.root"

		elif (nickname == "Tau_Run2016H_03Feb2017ver3v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/Tau_Run2016H_03Feb2017ver3v1_13TeV_MINIAOD.root"

		elif (nickname == "VBFHToTauTauM110_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/VBFHToTauTauM110_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root"

		elif (nickname == "VBFHToTauTauM120_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8_ext1"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/VBFHToTauTauM120_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8_ext1.root"

		elif (nickname == "VBFHToTauTauM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/VBFHToTauTauM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root"

		elif (nickname == "VBFHToTauTauM130_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8_ext1"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/VBFHToTauTauM130_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8_ext1.root"

		elif (nickname == "VBFHToTauTauM140_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/VBFHToTauTauM140_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root"

		elif (nickname == "VBFHToWWTo2L2NuM120_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/VBFHToWWTo2L2NuM120_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root"

		elif (nickname == "VBFHToWWTo2L2NuM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/VBFHToWWTo2L2NuM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root"

		elif (nickname == "VBFHToWWTo2L2NuM130_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/VBFHToWWTo2L2NuM130_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root"

		elif (nickname == "VVTo2L2Nu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_amcatnlo-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/VVTo2L2Nu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_amcatnlo-pythia8.root"

		elif (nickname == "VVTo2L2Nu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_amcatnlo-pythia8_ext1"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/VVTo2L2Nu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_amcatnlo-pythia8_ext1.root"

		elif (nickname == "W1JetsToLNu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/W1JetsToLNu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8.root"

		elif (nickname == "W2JetsToLNu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/W2JetsToLNu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8.root"

		elif (nickname == "W2JetsToLNu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext1"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/W2JetsToLNu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext1.root"

		elif (nickname == "W3JetsToLNu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/W3JetsToLNu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8.root"

		elif (nickname == "W3JetsToLNu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext1"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/W3JetsToLNu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext1.root"

		elif (nickname == "W4JetsToLNu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/W4JetsToLNu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8.root"

		elif (nickname == "W4JetsToLNu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext1"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/W4JetsToLNu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext1.root"

		elif (nickname == "W4JetsToLNu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext2"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/W4JetsToLNu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext2.root"

		elif (nickname == "WGToLNuG_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_amcatnlo-pythia8_ext1"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/WGToLNuG_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_amcatnlo-pythia8_ext1.root"

		elif (nickname == "WGToLNuG_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_amcatnlo-pythia8_ext2"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/WGToLNuG_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_amcatnlo-pythia8_ext2.root"

		elif (nickname == "WGToLNuG_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_amcatnlo-pythia8_ext3"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/WGToLNuG_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_amcatnlo-pythia8_ext3.root"

		elif (nickname == "WGstarToLNuEE_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/WGstarToLNuEE_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph.root"

		elif (nickname == "WGstarToLNuMuMu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/WGstarToLNuMuMu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph.root"

		elif (nickname == "WJetsToLNu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/WJetsToLNu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8.root"

		elif (nickname == "WJetsToLNu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext2"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/WJetsToLNu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext2.root"

		elif (nickname == "WWTo1L1Nu2Q_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_amcatnlo-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/WWTo1L1Nu2Q_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_amcatnlo-pythia8.root"

		elif (nickname == "WZJToLLLNu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/WZJToLLLNu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_pythia8.root"

		elif (nickname == "WZTo1L1Nu2Q_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_amcatnlo-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/WZTo1L1Nu2Q_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_amcatnlo-pythia8.root"

		elif (nickname == "WZTo1L3Nu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_amcatnlo-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/WZTo1L3Nu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_amcatnlo-pythia8.root"

		elif (nickname == "WZTo2L2Q_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_amcatnlo-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/WZTo2L2Q_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_amcatnlo-pythia8.root"

		elif (nickname == "WminusHToTauTauM110_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/WminusHToTauTauM110_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root"

		elif (nickname == "WminusHToTauTauM120_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/WminusHToTauTauM120_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root"

		elif (nickname == "WminusHToTauTauM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/WminusHToTauTauM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root"

		elif (nickname == "WminusHToTauTauM130_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/WminusHToTauTauM130_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root"

		elif (nickname == "WminusHToTauTauM140_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/WminusHToTauTauM140_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root"

		elif (nickname == "WplusHToTauTauM110_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/WplusHToTauTauM110_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root"

		elif (nickname == "WplusHToTauTauM120_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/WplusHToTauTauM120_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root"

		elif (nickname == "WplusHToTauTauM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/WplusHToTauTauM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root"

		elif (nickname == "WplusHToTauTauM130_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/WplusHToTauTauM130_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root"

		elif (nickname == "WplusHToTauTauM140_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/WplusHToTauTauM140_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root"

		elif (nickname == "ZHToTauTauM110_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/ZHToTauTauM110_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root"

		elif (nickname == "ZHToTauTauM120_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/ZHToTauTauM120_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root"

		elif (nickname == "ZHToTauTauM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/ZHToTauTauM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root"

		elif (nickname == "ZHToTauTauM130_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/ZHToTauTauM130_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root"

		elif (nickname == "ZHToTauTauM140_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/ZHToTauTauM140_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root"

		elif (nickname == "ZZTo2L2Q_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_amcatnlo-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/ZZTo2L2Q_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_amcatnlo-pythia8.root"

		elif (nickname == "ZZTo4L_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_amcatnlo-pythia8_ext1"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-02-15_00-16_classivSvfit_inputs2017-12-26_noMassConstraint/ZZTo4L_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_amcatnlo-pythia8_ext1.root"

		else:
			log.warning("COULD NOT FIND THE SVFIT CACHE FILE")


	def __getsvfitM91CacheFile__(self, nickname):

		if (nickname == "DY1JetsToLLM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/DY1JetsToLLM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8.root"
		elif (nickname =="DY2JetsToLLM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/DY2JetsToLLM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8.root"
		elif (nickname =="DY3JetsToLLM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/DY3JetsToLLM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8.root"
		elif (nickname =="DY4JetsToLLM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/DY4JetsToLLM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8.root"
		elif (nickname =="DYJetsToLLM10to50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/DYJetsToLLM10to50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8.root"
		elif (nickname =="DYJetsToLLM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext1"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/DYJetsToLLM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext1.root"
		elif (nickname =="DYJetsToLLM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext2"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/DYJetsToLLM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext2.root"
		elif (nickname =="DoubleEG_Run2016B_03Feb2017ver2v2_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/DoubleEG_Run2016B_03Feb2017ver2v2_13TeV_MINIAOD.root"
		elif (nickname =="DoubleEG_Run2016C_03Feb2017v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/DoubleEG_Run2016C_03Feb2017v1_13TeV_MINIAOD.root"
		elif (nickname =="DoubleEG_Run2016D_03Feb2017v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/DoubleEG_Run2016D_03Feb2017v1_13TeV_MINIAOD.root"
		elif (nickname =="DoubleEG_Run2016E_03Feb2017v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/DoubleEG_Run2016E_03Feb2017v1_13TeV_MINIAOD.root"
		elif (nickname =="DoubleEG_Run2016F_03Feb2017v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/DoubleEG_Run2016F_03Feb2017v1_13TeV_MINIAOD.root"
		elif (nickname =="DoubleEG_Run2016G_03Feb2017v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/DoubleEG_Run2016G_03Feb2017v1_13TeV_MINIAOD.root"
		elif (nickname =="DoubleEG_Run2016H_03Feb2017ver2v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/DoubleEG_Run2016H_03Feb2017ver2v1_13TeV_MINIAOD.root"
		elif (nickname =="DoubleEG_Run2016H_03Feb2017ver3v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/DoubleEG_Run2016H_03Feb2017ver3v1_13TeV_MINIAOD.root"
		elif (nickname =="DoubleMuon_Run2016B_03Feb2017ver2v2_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/DoubleMuon_Run2016B_03Feb2017ver2v2_13TeV_MINIAOD.root"
		elif (nickname =="DoubleMuon_Run2016C_03Feb2017v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/DoubleMuon_Run2016C_03Feb2017v1_13TeV_MINIAOD.root"
		elif (nickname =="DoubleMuon_Run2016D_03Feb2017v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/DoubleMuon_Run2016D_03Feb2017v1_13TeV_MINIAOD.root"
		elif (nickname =="DoubleMuon_Run2016E_03Feb2017v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/DoubleMuon_Run2016E_03Feb2017v1_13TeV_MINIAOD.root"
		elif (nickname =="DoubleMuon_Run2016F_03Feb2017v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/DoubleMuon_Run2016F_03Feb2017v1_13TeV_MINIAOD.root"
		elif (nickname =="DoubleMuon_Run2016G_03Feb2017v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/DoubleMuon_Run2016G_03Feb2017v1_13TeV_MINIAOD.root"
		elif (nickname =="DoubleMuon_Run2016H_03Feb2017ver2v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/DoubleMuon_Run2016H_03Feb2017ver2v1_13TeV_MINIAOD.root"
		elif (nickname =="DoubleMuon_Run2016H_03Feb2017ver3v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/DoubleMuon_Run2016H_03Feb2017ver3v1_13TeV_MINIAOD.root"
		elif (nickname =="EWKWMinus2JetsWToLNuM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/EWKWMinus2JetsWToLNuM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8.root"
		elif (nickname =="EWKWMinus2JetsWToLNuM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext1"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/EWKWMinus2JetsWToLNuM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext1.root"
		elif (nickname =="EWKWMinus2JetsWToLNuM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext2"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/EWKWMinus2JetsWToLNuM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext2.root"
		elif (nickname =="EWKWPlus2JetsWToLNuM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/EWKWPlus2JetsWToLNuM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8.root"
		elif (nickname =="EWKWPlus2JetsWToLNuM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext1"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/EWKWPlus2JetsWToLNuM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext1.root"
		elif (nickname =="EWKWPlus2JetsWToLNuM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext2"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/EWKWPlus2JetsWToLNuM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext2.root"
		elif (nickname =="EWKZ2JetsZToLLM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/EWKZ2JetsZToLLM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8.root"
		elif (nickname =="EWKZ2JetsZToLLM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext1"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/EWKZ2JetsZToLLM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext1.root"
		elif (nickname =="EWKZ2JetsZToLLM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext2"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/EWKZ2JetsZToLLM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext2.root"
		elif (nickname =="EWKZ2Jets_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/EWKZ2Jets_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8.root"
		elif (nickname =="EWKZ2Jets_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext1"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/EWKZ2Jets_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext1.root"
		elif (nickname =="EWKZ2Jets_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext2"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/EWKZ2Jets_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext2.root"
		elif (nickname =="GluGluH2JetsToTauTauM125CPmixingmaxmixJHU_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_JHUgen"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/GluGluH2JetsToTauTauM125CPmixingmaxmixJHU_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_JHUgen.root"
		elif (nickname =="GluGluH2JetsToTauTauM125CPmixingpseudoscalarJHU_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_JHUgen"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/GluGluH2JetsToTauTauM125CPmixingpseudoscalarJHU_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_JHUgen.root"
		elif (nickname =="GluGluH2JetsToTauTauM125CPmixingsmJHU_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_JHUgen"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/GluGluH2JetsToTauTauM125CPmixingsmJHU_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_JHUgen.root"
		elif (nickname =="GluGluHToTauTauM120_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8_ext1"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/GluGluHToTauTauM120_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8_ext1.root"
		elif (nickname =="GluGluHToTauTauM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/GluGluHToTauTauM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root"
		elif (nickname =="GluGluHToTauTauM130_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8_ext1"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/GluGluHToTauTauM130_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8_ext1.root"
		elif (nickname =="GluGluHToTauTauM140_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/GluGluHToTauTauM140_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root"
		elif (nickname =="GluGluHToWWTo2L2NuM120_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/GluGluHToWWTo2L2NuM120_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root"
		elif (nickname =="GluGluHToWWTo2L2NuM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/GluGluHToWWTo2L2NuM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root"
		elif (nickname =="GluGluHToWWTo2L2NuM130_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/GluGluHToWWTo2L2NuM130_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root"
		elif (nickname =="GluGluToHToTauTauM125_RunIIFall15MiniAODv2_PU25nsData2015v1_13TeV_MINIAOD_amcatnlo-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/GluGluToHToTauTauM125_RunIIFall15MiniAODv2_PU25nsData2015v1_13TeV_MINIAOD_amcatnlo-pythia8.root"
		elif (nickname =="MuonEG_Run2016B_03Feb2017ver2v2_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/MuonEG_Run2016B_03Feb2017ver2v2_13TeV_MINIAOD.root"
		elif (nickname =="MuonEG_Run2016C_03Feb2017v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/MuonEG_Run2016C_03Feb2017v1_13TeV_MINIAOD.root"
		elif (nickname =="MuonEG_Run2016D_03Feb2017v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/MuonEG_Run2016D_03Feb2017v1_13TeV_MINIAOD.root"
		elif (nickname =="MuonEG_Run2016E_03Feb2017v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/MuonEG_Run2016E_03Feb2017v1_13TeV_MINIAOD.root"
		elif (nickname =="MuonEG_Run2016F_03Feb2017v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/MuonEG_Run2016F_03Feb2017v1_13TeV_MINIAOD.root"
		elif (nickname =="MuonEG_Run2016G_03Feb2017v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/MuonEG_Run2016G_03Feb2017v1_13TeV_MINIAOD.root"
		elif (nickname =="MuonEG_Run2016H_03Feb2017ver2v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/MuonEG_Run2016H_03Feb2017ver2v1_13TeV_MINIAOD.root"
		elif (nickname =="MuonEG_Run2016H_03Feb2017ver3v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/MuonEG_Run2016H_03Feb2017ver3v1_13TeV_MINIAOD.root"
		elif (nickname =="STt-channelantitop4finclusiveDecays_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/STt-channelantitop4finclusiveDecays_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root"
		elif (nickname =="STt-channeltop4finclusiveDecays_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/STt-channeltop4finclusiveDecays_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root"
		elif (nickname =="STtWantitop5finclusiveDecays_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8_ext1"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/STtWantitop5finclusiveDecays_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8_ext1.root"
		elif (nickname =="STtWtop5finclusiveDecays_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8_ext1"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/STtWtop5finclusiveDecays_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8_ext1.root"
		elif (nickname =="SUSYGluGluToBBHToTauTauM100_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/SUSYGluGluToBBHToTauTauM100_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_pythia8.root"
		elif (nickname =="SUSYGluGluToBBHToTauTauM110_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/SUSYGluGluToBBHToTauTauM110_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_pythia8.root"
		elif (nickname =="SUSYGluGluToBBHToTauTauM120_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/SUSYGluGluToBBHToTauTauM120_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_pythia8.root"
		elif (nickname =="SUSYGluGluToBBHToTauTauM130_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/SUSYGluGluToBBHToTauTauM130_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_pythia8.root"
		elif (nickname =="SUSYGluGluToBBHToTauTauM140_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/SUSYGluGluToBBHToTauTauM140_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_pythia8.root"
		elif (nickname =="SUSYGluGluToBBHToTauTauM160_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/SUSYGluGluToBBHToTauTauM160_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_pythia8.root"
		elif (nickname =="SUSYGluGluToBBHToTauTauM180_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/SUSYGluGluToBBHToTauTauM180_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_pythia8.root"
		elif (nickname =="SUSYGluGluToBBHToTauTauM200_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/SUSYGluGluToBBHToTauTauM200_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_pythia8.root"
		elif (nickname =="SUSYGluGluToBBHToTauTauM250_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/SUSYGluGluToBBHToTauTauM250_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_pythia8.root"
		elif (nickname =="SUSYGluGluToBBHToTauTauM300_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/SUSYGluGluToBBHToTauTauM300_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_pythia8.root"
		elif (nickname =="SUSYGluGluToBBHToTauTauM350_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/SUSYGluGluToBBHToTauTauM350_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_pythia8.root"
		elif (nickname =="SUSYGluGluToBBHToTauTauM80_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/SUSYGluGluToBBHToTauTauM80_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_pythia8.root"
		elif (nickname =="SUSYGluGluToBBHToTauTauM90_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/SUSYGluGluToBBHToTauTauM90_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_pythia8.root"
		elif (nickname =="SUSYGluGluToHToTauTauM100_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/SUSYGluGluToHToTauTauM100_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_pythia8.root"
		elif (nickname =="SUSYGluGluToHToTauTauM110_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/SUSYGluGluToHToTauTauM110_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_pythia8.root"
		elif (nickname =="SUSYGluGluToHToTauTauM120_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/SUSYGluGluToHToTauTauM120_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_pythia8.root"
		elif (nickname =="SUSYGluGluToHToTauTauM130_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/SUSYGluGluToHToTauTauM130_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_pythia8.root"
		elif (nickname =="SUSYGluGluToHToTauTauM140_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/SUSYGluGluToHToTauTauM140_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_pythia8.root"
		elif (nickname =="SUSYGluGluToHToTauTauM160_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/SUSYGluGluToHToTauTauM160_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_pythia8.root"
		elif (nickname =="SUSYGluGluToHToTauTauM180_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/SUSYGluGluToHToTauTauM180_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_pythia8.root"
		elif (nickname =="SUSYGluGluToHToTauTauM200_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/SUSYGluGluToHToTauTauM200_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_pythia8.root"
		elif (nickname =="SUSYGluGluToHToTauTauM250_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/SUSYGluGluToHToTauTauM250_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_pythia8.root"
		elif (nickname =="SUSYGluGluToHToTauTauM300_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/SUSYGluGluToHToTauTauM300_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_pythia8.root"
		elif (nickname =="SUSYGluGluToHToTauTauM350_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/SUSYGluGluToHToTauTauM350_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_pythia8.root"
		elif (nickname =="SUSYGluGluToHToTauTauM80_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/SUSYGluGluToHToTauTauM80_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_pythia8.root"
		elif (nickname =="SUSYGluGluToHToTauTauM90_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/SUSYGluGluToHToTauTauM90_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_pythia8.root"
		elif (nickname =="SingleElectron_Run2016B_03Feb2017ver2v2_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/SingleElectron_Run2016B_03Feb2017ver2v2_13TeV_MINIAOD.root"
		elif (nickname =="SingleElectron_Run2016C_03Feb2017v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/SingleElectron_Run2016C_03Feb2017v1_13TeV_MINIAOD.root"
		elif (nickname =="SingleElectron_Run2016D_03Feb2017v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/SingleElectron_Run2016D_03Feb2017v1_13TeV_MINIAOD.root"
		elif (nickname =="SingleElectron_Run2016E_03Feb2017v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/SingleElectron_Run2016E_03Feb2017v1_13TeV_MINIAOD.root"
		elif (nickname =="SingleElectron_Run2016F_03Feb2017v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/SingleElectron_Run2016F_03Feb2017v1_13TeV_MINIAOD.root"
		elif (nickname =="SingleElectron_Run2016G_03Feb2017v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/SingleElectron_Run2016G_03Feb2017v1_13TeV_MINIAOD.root"
		elif (nickname =="SingleElectron_Run2016H_03Feb2017ver2v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/SingleElectron_Run2016H_03Feb2017ver2v1_13TeV_MINIAOD.root"
		elif (nickname =="SingleElectron_Run2016H_03Feb2017ver3v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/SingleElectron_Run2016H_03Feb2017ver3v1_13TeV_MINIAOD.root"
		elif (nickname =="SingleMuon_Run2016B_03Feb2017ver2v2_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/SingleMuon_Run2016B_03Feb2017ver2v2_13TeV_MINIAOD.root"
		elif (nickname =="SingleMuon_Run2016C_03Feb2017v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/SingleMuon_Run2016C_03Feb2017v1_13TeV_MINIAOD.root"
		elif (nickname =="SingleMuon_Run2016D_03Feb2017v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/SingleMuon_Run2016D_03Feb2017v1_13TeV_MINIAOD.root"
		elif (nickname =="SingleMuon_Run2016E_03Feb2017v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/SingleMuon_Run2016E_03Feb2017v1_13TeV_MINIAOD.root"
		elif (nickname =="SingleMuon_Run2016F_03Feb2017v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/SingleMuon_Run2016F_03Feb2017v1_13TeV_MINIAOD.root"
		elif (nickname =="SingleMuon_Run2016G_03Feb2017v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/SingleMuon_Run2016G_03Feb2017v1_13TeV_MINIAOD.root"
		elif (nickname =="SingleMuon_Run2016H_03Feb2017ver2v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/SingleMuon_Run2016H_03Feb2017ver2v1_13TeV_MINIAOD.root"
		elif (nickname =="SingleMuon_Run2016H_03Feb2017ver3v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/SingleMuon_Run2016H_03Feb2017ver3v1_13TeV_MINIAOD.root"
		elif (nickname =="TT_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/TT_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root"
		elif (nickname =="Tau_Run2016B_03Feb2017ver2v2_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/Tau_Run2016B_03Feb2017ver2v2_13TeV_MINIAOD.root"
		elif (nickname =="Tau_Run2016C_03Feb2017v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/Tau_Run2016C_03Feb2017v1_13TeV_MINIAOD.root"
		elif (nickname =="Tau_Run2016D_03Feb2017v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/Tau_Run2016D_03Feb2017v1_13TeV_MINIAOD.root"
		elif (nickname =="Tau_Run2016E_03Feb2017v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/Tau_Run2016E_03Feb2017v1_13TeV_MINIAOD.root"
		elif (nickname =="Tau_Run2016F_03Feb2017v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/Tau_Run2016F_03Feb2017v1_13TeV_MINIAOD.root"
		elif (nickname =="Tau_Run2016G_03Feb2017v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/Tau_Run2016G_03Feb2017v1_13TeV_MINIAOD.root"
		elif (nickname =="Tau_Run2016H_03Feb2017ver2v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/Tau_Run2016H_03Feb2017ver2v1_13TeV_MINIAOD.root"
		elif (nickname =="Tau_Run2016H_03Feb2017ver3v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/Tau_Run2016H_03Feb2017ver3v1_13TeV_MINIAOD.root"
		elif (nickname =="VBFHToTauTauM110_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/VBFHToTauTauM110_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root"
		elif (nickname =="VBFHToTauTauM120_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8_ext1"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/VBFHToTauTauM120_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8_ext1.root"
		elif (nickname =="VBFHToTauTauM125_RunIIFall15MiniAODv2_PU25nsData2015v1_13TeV_MINIAOD_amcatnlo-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/VBFHToTauTauM125_RunIIFall15MiniAODv2_PU25nsData2015v1_13TeV_MINIAOD_amcatnlo-pythia8.root"
		elif (nickname =="VBFHToTauTauM125_RunIISpring16MiniAODv2reHLT_PUSpring16RAWAODSIM_13TeV_MINIAOD_amcatnlo-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/VBFHToTauTauM125_RunIISpring16MiniAODv2reHLT_PUSpring16RAWAODSIM_13TeV_MINIAOD_amcatnlo-pythia8.root"
		elif (nickname =="VBFHToTauTauM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/VBFHToTauTauM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root"
		elif (nickname =="VBFHToTauTauM130_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8_ext1"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/VBFHToTauTauM130_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8_ext1.root"
		elif (nickname =="VBFHToTauTauM140_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/VBFHToTauTauM140_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root"
		elif (nickname =="VBFHToWWTo2L2NuM120_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/VBFHToWWTo2L2NuM120_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root"
		elif (nickname =="VBFHToWWTo2L2NuM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/VBFHToWWTo2L2NuM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root"
		elif (nickname =="VBFHToWWTo2L2NuM130_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/VBFHToWWTo2L2NuM130_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root"
		elif (nickname =="VBFHiggs0L1M125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_JHUgenv6"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/VBFHiggs0L1M125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_JHUgenv6.root"
		elif (nickname =="VBFHiggs0L1f05ph0M125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_JHUgenv6"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/VBFHiggs0L1f05ph0M125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_JHUgenv6.root"
		elif (nickname =="VBFHiggs0MM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_JHUgenv6"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/VBFHiggs0MM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_JHUgenv6.root"
		elif (nickname =="VBFHiggs0Mf05ph0M125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_JHUgenv6"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/VBFHiggs0Mf05ph0M125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_JHUgenv6.root"
		elif (nickname =="VBFHiggs0PHM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_JHUgenv6"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/VBFHiggs0PHM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_JHUgenv6.root"
		elif (nickname =="VBFHiggs0PHf05ph0M125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_JHUgenv6"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/VBFHiggs0PHf05ph0M125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_JHUgenv6.root"
		elif (nickname =="VBFHiggs0PMM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_JHUgenv6"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/VBFHiggs0PMM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_JHUgenv6.root"
		elif (nickname =="VVTo2L2Nu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_amcatnlo-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/VVTo2L2Nu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_amcatnlo-pythia8.root"
		elif (nickname =="VVTo2L2Nu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_amcatnlo-pythia8_ext1"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/VVTo2L2Nu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_amcatnlo-pythia8_ext1.root"
		elif (nickname =="W1JetsToLNu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/W1JetsToLNu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8.root"
		elif (nickname =="W2JetsToLNu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/W2JetsToLNu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8.root"
		elif (nickname =="W2JetsToLNu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext1"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/W2JetsToLNu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext1.root"
		elif (nickname =="W3JetsToLNu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/W3JetsToLNu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8.root"
		elif (nickname =="W3JetsToLNu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext1"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/W3JetsToLNu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext1.root"
		elif (nickname =="W4JetsToLNu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/W4JetsToLNu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8.root"
		elif (nickname =="W4JetsToLNu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext1"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/W4JetsToLNu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext1.root"
		elif (nickname =="W4JetsToLNu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext2"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/W4JetsToLNu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext2.root"
		elif (nickname =="WGToLNuG_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_amcatnlo-pythia8_ext1"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/WGToLNuG_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_amcatnlo-pythia8_ext1.root"
		elif (nickname =="WGToLNuG_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_amcatnlo-pythia8_ext2"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/WGToLNuG_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_amcatnlo-pythia8_ext2.root"
		elif (nickname =="WGToLNuG_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_amcatnlo-pythia8_ext3"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/WGToLNuG_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_amcatnlo-pythia8_ext3.root"
		elif (nickname =="WGstarToLNuEE_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/WGstarToLNuEE_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph.root"
		elif (nickname =="WGstarToLNuMuMu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/WGstarToLNuMuMu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph.root"
		elif (nickname =="WHiggs0L1UndecayedM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_JHUgen"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/WHiggs0L1UndecayedM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_JHUgen.root"
		elif (nickname =="WHiggs0L1fWH05ph0UndecayedM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_JHUgen"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/WHiggs0L1fWH05ph0UndecayedM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_JHUgen.root"
		elif (nickname =="WHiggs0MUndecayedM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_JHUgen"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/WHiggs0MUndecayedM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_JHUgen.root"
		elif (nickname =="WHiggs0MfWH05ph0UndecayedM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_JHUgen"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/WHiggs0MfWH05ph0UndecayedM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_JHUgen.root"
		elif (nickname =="WHiggs0PHUndecayedM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_JHUgen"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/WHiggs0PHUndecayedM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_JHUgen.root"
		elif (nickname =="WHiggs0PHfWH05ph0UndecayedM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_JHUgen"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/WHiggs0PHfWH05ph0UndecayedM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_JHUgen.root"
		elif (nickname =="WHiggs0PMUndecayedM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_JHUgen"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/WHiggs0PMUndecayedM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_JHUgen.root"
		elif (nickname =="WJetsToLNu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/WJetsToLNu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8.root"
		elif (nickname =="WJetsToLNu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext2"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/WJetsToLNu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext2.root"
		elif (nickname =="WWTo1L1Nu2Q_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_amcatnlo-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/WWTo1L1Nu2Q_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_amcatnlo-pythia8.root"
		elif (nickname =="WZJToLLLNu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/WZJToLLLNu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_pythia8.root"
		elif (nickname =="WZTo1L1Nu2Q_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_amcatnlo-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/WZTo1L1Nu2Q_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_amcatnlo-pythia8.root"
		elif (nickname =="WZTo1L3Nu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_amcatnlo-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/WZTo1L3Nu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_amcatnlo-pythia8.root"
		elif (nickname =="WZTo2L2Q_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_amcatnlo-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/WZTo2L2Q_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_amcatnlo-pythia8.root"
		elif (nickname =="WminusHToTauTauM110_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/WminusHToTauTauM110_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root"
		elif (nickname =="WminusHToTauTauM120_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/WminusHToTauTauM120_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root"
		elif (nickname =="WminusHToTauTauM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/WminusHToTauTauM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root"
		elif (nickname =="WminusHToTauTauM130_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/WminusHToTauTauM130_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root"
		elif (nickname =="WminusHToTauTauM140_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/WminusHToTauTauM140_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root"
		elif (nickname =="WplusHToTauTauM110_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/WplusHToTauTauM110_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root"
		elif (nickname =="WplusHToTauTauM120_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/WplusHToTauTauM120_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root"
		elif (nickname =="WplusHToTauTauM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/WplusHToTauTauM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root"
		elif (nickname =="WplusHToTauTauM130_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/WplusHToTauTauM130_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root"
		elif (nickname =="WplusHToTauTauM140_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/WplusHToTauTauM140_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root"
		elif (nickname =="ZHToTauTauM110_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/ZHToTauTauM110_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root"
		elif (nickname =="ZHToTauTauM120_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/ZHToTauTauM120_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root"
		elif (nickname =="ZHToTauTauM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/ZHToTauTauM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root"
		elif (nickname =="ZHToTauTauM130_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/ZHToTauTauM130_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root"
		elif (nickname =="ZHToTauTauM140_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/ZHToTauTauM140_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root"
		elif (nickname =="ZHiggs0L1UndecayedM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_JHUgen"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/ZHiggs0L1UndecayedM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_JHUgen.root"
		elif (nickname =="ZHiggs0L1fZH05ph0UndecayedM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_JHUgen"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/ZHiggs0L1fZH05ph0UndecayedM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_JHUgen.root"
		elif (nickname =="ZHiggs0MUndecayedM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_JHUgen"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/ZHiggs0MUndecayedM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_JHUgen.root"
		elif (nickname =="ZHiggs0MfZH05ph0UndecayedM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_JHUgen"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/ZHiggs0MfZH05ph0UndecayedM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_JHUgen.root"
		elif (nickname =="ZHiggs0PHUndecayedM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_JHUgen"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/ZHiggs0PHUndecayedM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_JHUgen.root"
		elif (nickname =="ZHiggs0PHfZH05ph0UndecayedM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_JHUgen"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/ZHiggs0PHfZH05ph0UndecayedM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_JHUgen.root"
		elif (nickname =="ZHiggs0PMUndecayedM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_JHUgen"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/ZHiggs0PMUndecayedM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_JHUgen.root"
		elif (nickname =="ZZTo2L2Q_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_amcatnlo-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/ZZTo2L2Q_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_amcatnlo-pythia8.root"
		elif (nickname =="ZZTo4L_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_amcatnlo-pythia8_ext1"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/tmuller/higgs-kit/Svfit/MergedCaches/2018-03-16_09-44_classivSvfit_inputs2017-12-26_ZMassConstraint/ZZTo4L_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_amcatnlo-pythia8_ext1.root"

	def __getsvfitM125CacheFile__(self, nickname):
		if (nickname == "DY1JetsToLLM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/DY1JetsToLLM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8.root"
		elif (nickname =="DY2JetsToLLM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/DY2JetsToLLM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8.root"
		elif (nickname =="DY3JetsToLLM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/DY3JetsToLLM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8.root"
		elif (nickname =="DY4JetsToLLM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/DY4JetsToLLM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8.root"
		elif (nickname =="DYJetsToLLM10to50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/DYJetsToLLM10to50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8.root"
		elif (nickname =="DYJetsToLLM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext1"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/DYJetsToLLM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext1.root"
		elif (nickname =="DYJetsToLLM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext2"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/DYJetsToLLM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext2.root"
		elif (nickname =="DoubleEG_Run2016B_03Feb2017ver2v2_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/DoubleEG_Run2016B_03Feb2017ver2v2_13TeV_MINIAOD.root"
		elif (nickname =="DoubleEG_Run2016C_03Feb2017v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/DoubleEG_Run2016C_03Feb2017v1_13TeV_MINIAOD.root"
		elif (nickname =="DoubleEG_Run2016D_03Feb2017v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/DoubleEG_Run2016D_03Feb2017v1_13TeV_MINIAOD.root"
		elif (nickname =="DoubleEG_Run2016E_03Feb2017v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/DoubleEG_Run2016E_03Feb2017v1_13TeV_MINIAOD.root"
		elif (nickname =="DoubleEG_Run2016F_03Feb2017v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/DoubleEG_Run2016F_03Feb2017v1_13TeV_MINIAOD.root"
		elif (nickname =="DoubleEG_Run2016G_03Feb2017v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/DoubleEG_Run2016G_03Feb2017v1_13TeV_MINIAOD.root"
		elif (nickname =="DoubleEG_Run2016H_03Feb2017ver2v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/DoubleEG_Run2016H_03Feb2017ver2v1_13TeV_MINIAOD.root"
		elif (nickname =="DoubleEG_Run2016H_03Feb2017ver3v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/DoubleEG_Run2016H_03Feb2017ver3v1_13TeV_MINIAOD.root"
		elif (nickname =="DoubleMuon_Run2016B_03Feb2017ver2v2_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/DoubleMuon_Run2016B_03Feb2017ver2v2_13TeV_MINIAOD.root"
		elif (nickname =="DoubleMuon_Run2016C_03Feb2017v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/DoubleMuon_Run2016C_03Feb2017v1_13TeV_MINIAOD.root"
		elif (nickname =="DoubleMuon_Run2016D_03Feb2017v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/DoubleMuon_Run2016D_03Feb2017v1_13TeV_MINIAOD.root"
		elif (nickname =="DoubleMuon_Run2016E_03Feb2017v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/DoubleMuon_Run2016E_03Feb2017v1_13TeV_MINIAOD.root"
		elif (nickname =="DoubleMuon_Run2016F_03Feb2017v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/DoubleMuon_Run2016F_03Feb2017v1_13TeV_MINIAOD.root"
		elif (nickname =="DoubleMuon_Run2016G_03Feb2017v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/DoubleMuon_Run2016G_03Feb2017v1_13TeV_MINIAOD.root"
		elif (nickname =="DoubleMuon_Run2016H_03Feb2017ver2v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/DoubleMuon_Run2016H_03Feb2017ver2v1_13TeV_MINIAOD.root"
		elif (nickname =="DoubleMuon_Run2016H_03Feb2017ver3v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/DoubleMuon_Run2016H_03Feb2017ver3v1_13TeV_MINIAOD.root"
		elif (nickname =="EWKWMinus2JetsWToLNuM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/EWKWMinus2JetsWToLNuM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8.root"
		elif (nickname =="EWKWMinus2JetsWToLNuM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext1"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/EWKWMinus2JetsWToLNuM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext1.root"
		elif (nickname =="EWKWMinus2JetsWToLNuM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext2"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/EWKWMinus2JetsWToLNuM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext2.root"
		elif (nickname =="EWKWPlus2JetsWToLNuM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/EWKWPlus2JetsWToLNuM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8.root"
		elif (nickname =="EWKWPlus2JetsWToLNuM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext1"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/EWKWPlus2JetsWToLNuM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext1.root"
		elif (nickname =="EWKWPlus2JetsWToLNuM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext2"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/EWKWPlus2JetsWToLNuM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext2.root"
		elif (nickname =="EWKZ2JetsZToLLM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/EWKZ2JetsZToLLM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8.root"
		elif (nickname =="EWKZ2JetsZToLLM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext1"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/EWKZ2JetsZToLLM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext1.root"
		elif (nickname =="EWKZ2JetsZToLLM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext2"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/EWKZ2JetsZToLLM50_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext2.root"
		elif (nickname =="EWKZ2Jets_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/EWKZ2Jets_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8.root"
		elif (nickname =="EWKZ2Jets_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext1"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/EWKZ2Jets_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext1.root"
		elif (nickname =="EWKZ2Jets_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext2"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/EWKZ2Jets_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext2.root"
		elif (nickname =="GluGluH2JetsToTauTauM125CPmixingmaxmixJHU_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_JHUgen"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/GluGluH2JetsToTauTauM125CPmixingmaxmixJHU_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_JHUgen.root"
		elif (nickname =="GluGluH2JetsToTauTauM125CPmixingpseudoscalarJHU_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_JHUgen"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/GluGluH2JetsToTauTauM125CPmixingpseudoscalarJHU_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_JHUgen.root"
		elif (nickname =="GluGluH2JetsToTauTauM125CPmixingsmJHU_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_JHUgen"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/GluGluH2JetsToTauTauM125CPmixingsmJHU_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_JHUgen.root"
		elif (nickname =="GluGluHToTauTauM120_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8_ext1"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/GluGluHToTauTauM120_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8_ext1.root"
		elif (nickname =="GluGluHToTauTauM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/GluGluHToTauTauM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root"
		elif (nickname =="GluGluHToTauTauM130_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8_ext1"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/GluGluHToTauTauM130_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8_ext1.root"
		elif (nickname =="GluGluHToTauTauM140_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/GluGluHToTauTauM140_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root"
		elif (nickname =="GluGluHToWWTo2L2NuM120_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/GluGluHToWWTo2L2NuM120_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root"
		elif (nickname =="GluGluHToWWTo2L2NuM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/GluGluHToWWTo2L2NuM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root"
		elif (nickname =="GluGluHToWWTo2L2NuM130_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/GluGluHToWWTo2L2NuM130_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root"
		elif (nickname =="GluGluToHToTauTauM125_RunIIFall15MiniAODv2_PU25nsData2015v1_13TeV_MINIAOD_amcatnlo-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/GluGluToHToTauTauM125_RunIIFall15MiniAODv2_PU25nsData2015v1_13TeV_MINIAOD_amcatnlo-pythia8.root"
		elif (nickname =="MuonEG_Run2016B_03Feb2017ver2v2_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/MuonEG_Run2016B_03Feb2017ver2v2_13TeV_MINIAOD.root"
		elif (nickname =="MuonEG_Run2016C_03Feb2017v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/MuonEG_Run2016C_03Feb2017v1_13TeV_MINIAOD.root"
		elif (nickname =="MuonEG_Run2016D_03Feb2017v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/MuonEG_Run2016D_03Feb2017v1_13TeV_MINIAOD.root"
		elif (nickname =="MuonEG_Run2016E_03Feb2017v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/MuonEG_Run2016E_03Feb2017v1_13TeV_MINIAOD.root"
		elif (nickname =="MuonEG_Run2016F_03Feb2017v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/MuonEG_Run2016F_03Feb2017v1_13TeV_MINIAOD.root"
		elif (nickname =="MuonEG_Run2016G_03Feb2017v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/MuonEG_Run2016G_03Feb2017v1_13TeV_MINIAOD.root"
		elif (nickname =="MuonEG_Run2016H_03Feb2017ver2v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/MuonEG_Run2016H_03Feb2017ver2v1_13TeV_MINIAOD.root"
		elif (nickname =="MuonEG_Run2016H_03Feb2017ver3v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/MuonEG_Run2016H_03Feb2017ver3v1_13TeV_MINIAOD.root"
		elif (nickname =="STt-channelantitop4finclusiveDecays_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/STt-channelantitop4finclusiveDecays_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root"
		elif (nickname =="STt-channeltop4finclusiveDecays_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/STt-channeltop4finclusiveDecays_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root"
		elif (nickname =="STtWantitop5finclusiveDecays_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8_ext1"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/STtWantitop5finclusiveDecays_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8_ext1.root"
		elif (nickname =="STtWtop5finclusiveDecays_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8_ext1"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/STtWtop5finclusiveDecays_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8_ext1.root"
		elif (nickname =="SUSYGluGluToBBHToTauTauM100_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/SUSYGluGluToBBHToTauTauM100_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_pythia8.root"
		elif (nickname =="SUSYGluGluToBBHToTauTauM110_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/SUSYGluGluToBBHToTauTauM110_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_pythia8.root"
		elif (nickname =="SUSYGluGluToBBHToTauTauM120_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/SUSYGluGluToBBHToTauTauM120_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_pythia8.root"
		elif (nickname =="SUSYGluGluToBBHToTauTauM130_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/SUSYGluGluToBBHToTauTauM130_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_pythia8.root"
		elif (nickname =="SUSYGluGluToBBHToTauTauM140_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/SUSYGluGluToBBHToTauTauM140_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_pythia8.root"
		elif (nickname =="SUSYGluGluToBBHToTauTauM160_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/SUSYGluGluToBBHToTauTauM160_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_pythia8.root"
		elif (nickname =="SUSYGluGluToBBHToTauTauM180_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/SUSYGluGluToBBHToTauTauM180_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_pythia8.root"
		elif (nickname =="SUSYGluGluToBBHToTauTauM200_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/SUSYGluGluToBBHToTauTauM200_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_pythia8.root"
		elif (nickname =="SUSYGluGluToBBHToTauTauM250_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/SUSYGluGluToBBHToTauTauM250_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_pythia8.root"
		elif (nickname =="SUSYGluGluToBBHToTauTauM300_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/SUSYGluGluToBBHToTauTauM300_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_pythia8.root"
		elif (nickname =="SUSYGluGluToBBHToTauTauM350_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/SUSYGluGluToBBHToTauTauM350_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_pythia8.root"
		elif (nickname =="SUSYGluGluToBBHToTauTauM80_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/SUSYGluGluToBBHToTauTauM80_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_pythia8.root"
		elif (nickname =="SUSYGluGluToBBHToTauTauM90_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/SUSYGluGluToBBHToTauTauM90_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_pythia8.root"
		elif (nickname =="SUSYGluGluToHToTauTauM100_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/SUSYGluGluToHToTauTauM100_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_pythia8.root"
		elif (nickname =="SUSYGluGluToHToTauTauM110_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/SUSYGluGluToHToTauTauM110_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_pythia8.root"
		elif (nickname =="SUSYGluGluToHToTauTauM120_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/SUSYGluGluToHToTauTauM120_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_pythia8.root"
		elif (nickname =="SUSYGluGluToHToTauTauM130_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/SUSYGluGluToHToTauTauM130_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_pythia8.root"
		elif (nickname =="SUSYGluGluToHToTauTauM140_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/SUSYGluGluToHToTauTauM140_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_pythia8.root"
		elif (nickname =="SUSYGluGluToHToTauTauM160_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/SUSYGluGluToHToTauTauM160_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_pythia8.root"
		elif (nickname =="SUSYGluGluToHToTauTauM180_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/SUSYGluGluToHToTauTauM180_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_pythia8.root"
		elif (nickname =="SUSYGluGluToHToTauTauM200_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/SUSYGluGluToHToTauTauM200_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_pythia8.root"
		elif (nickname =="SUSYGluGluToHToTauTauM250_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/SUSYGluGluToHToTauTauM250_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_pythia8.root"
		elif (nickname =="SUSYGluGluToHToTauTauM300_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/SUSYGluGluToHToTauTauM300_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_pythia8.root"
		elif (nickname =="SUSYGluGluToHToTauTauM350_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/SUSYGluGluToHToTauTauM350_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_pythia8.root"
		elif (nickname =="SUSYGluGluToHToTauTauM80_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/SUSYGluGluToHToTauTauM80_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_pythia8.root"
		elif (nickname =="SUSYGluGluToHToTauTauM90_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/SUSYGluGluToHToTauTauM90_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_pythia8.root"
		elif (nickname =="SingleElectron_Run2016B_03Feb2017ver2v2_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/SingleElectron_Run2016B_03Feb2017ver2v2_13TeV_MINIAOD.root"
		elif (nickname =="SingleElectron_Run2016C_03Feb2017v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/SingleElectron_Run2016C_03Feb2017v1_13TeV_MINIAOD.root"
		elif (nickname =="SingleElectron_Run2016D_03Feb2017v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/SingleElectron_Run2016D_03Feb2017v1_13TeV_MINIAOD.root"
		elif (nickname =="SingleElectron_Run2016E_03Feb2017v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/SingleElectron_Run2016E_03Feb2017v1_13TeV_MINIAOD.root"
		elif (nickname =="SingleElectron_Run2016F_03Feb2017v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/SingleElectron_Run2016F_03Feb2017v1_13TeV_MINIAOD.root"
		elif (nickname =="SingleElectron_Run2016G_03Feb2017v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/SingleElectron_Run2016G_03Feb2017v1_13TeV_MINIAOD.root"
		elif (nickname =="SingleElectron_Run2016H_03Feb2017ver2v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/SingleElectron_Run2016H_03Feb2017ver2v1_13TeV_MINIAOD.root"
		elif (nickname =="SingleElectron_Run2016H_03Feb2017ver3v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/SingleElectron_Run2016H_03Feb2017ver3v1_13TeV_MINIAOD.root"
		elif (nickname =="SingleMuon_Run2016B_03Feb2017ver2v2_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/SingleMuon_Run2016B_03Feb2017ver2v2_13TeV_MINIAOD.root"
		elif (nickname =="SingleMuon_Run2016C_03Feb2017v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/SingleMuon_Run2016C_03Feb2017v1_13TeV_MINIAOD.root"
		elif (nickname =="SingleMuon_Run2016D_03Feb2017v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/SingleMuon_Run2016D_03Feb2017v1_13TeV_MINIAOD.root"
		elif (nickname =="SingleMuon_Run2016E_03Feb2017v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/SingleMuon_Run2016E_03Feb2017v1_13TeV_MINIAOD.root"
		elif (nickname =="SingleMuon_Run2016F_03Feb2017v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/SingleMuon_Run2016F_03Feb2017v1_13TeV_MINIAOD.root"
		elif (nickname =="SingleMuon_Run2016G_03Feb2017v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/SingleMuon_Run2016G_03Feb2017v1_13TeV_MINIAOD.root"
		elif (nickname =="SingleMuon_Run2016H_03Feb2017ver2v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/SingleMuon_Run2016H_03Feb2017ver2v1_13TeV_MINIAOD.root"
		elif (nickname =="SingleMuon_Run2016H_03Feb2017ver3v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/SingleMuon_Run2016H_03Feb2017ver3v1_13TeV_MINIAOD.root"
		elif (nickname =="TT_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/TT_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root"
		elif (nickname =="Tau_Run2016B_03Feb2017ver2v2_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/Tau_Run2016B_03Feb2017ver2v2_13TeV_MINIAOD.root"
		elif (nickname =="Tau_Run2016C_03Feb2017v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/Tau_Run2016C_03Feb2017v1_13TeV_MINIAOD.root"
		elif (nickname =="Tau_Run2016D_03Feb2017v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/Tau_Run2016D_03Feb2017v1_13TeV_MINIAOD.root"
		elif (nickname =="Tau_Run2016E_03Feb2017v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/Tau_Run2016E_03Feb2017v1_13TeV_MINIAOD.root"
		elif (nickname =="Tau_Run2016F_03Feb2017v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/Tau_Run2016F_03Feb2017v1_13TeV_MINIAOD.root"
		elif (nickname =="Tau_Run2016G_03Feb2017v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/Tau_Run2016G_03Feb2017v1_13TeV_MINIAOD.root"
		elif (nickname =="Tau_Run2016H_03Feb2017ver2v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/Tau_Run2016H_03Feb2017ver2v1_13TeV_MINIAOD.root"
		elif (nickname =="Tau_Run2016H_03Feb2017ver3v1_13TeV_MINIAOD"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/Tau_Run2016H_03Feb2017ver3v1_13TeV_MINIAOD.root"
		elif (nickname =="VBFHToTauTauM110_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/VBFHToTauTauM110_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root"
		elif (nickname =="VBFHToTauTauM120_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8_ext1"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/VBFHToTauTauM120_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8_ext1.root"
		elif (nickname =="VBFHToTauTauM125_RunIIFall15MiniAODv2_PU25nsData2015v1_13TeV_MINIAOD_amcatnlo-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/VBFHToTauTauM125_RunIIFall15MiniAODv2_PU25nsData2015v1_13TeV_MINIAOD_amcatnlo-pythia8.root"
		elif (nickname =="VBFHToTauTauM125_RunIISpring16MiniAODv2reHLT_PUSpring16RAWAODSIM_13TeV_MINIAOD_amcatnlo-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/VBFHToTauTauM125_RunIISpring16MiniAODv2reHLT_PUSpring16RAWAODSIM_13TeV_MINIAOD_amcatnlo-pythia8.root"
		elif (nickname =="VBFHToTauTauM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/VBFHToTauTauM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root"
		elif (nickname =="VBFHToTauTauM130_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8_ext1"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/VBFHToTauTauM130_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8_ext1.root"
		elif (nickname =="VBFHToTauTauM140_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/VBFHToTauTauM140_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root"
		elif (nickname =="VBFHToWWTo2L2NuM120_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/VBFHToWWTo2L2NuM120_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root"
		elif (nickname =="VBFHToWWTo2L2NuM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/VBFHToWWTo2L2NuM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root"
		elif (nickname =="VBFHToWWTo2L2NuM130_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/VBFHToWWTo2L2NuM130_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root"
		elif (nickname =="VBFHiggs0L1M125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_JHUgenv6"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/VBFHiggs0L1M125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_JHUgenv6.root"
		elif (nickname =="VBFHiggs0L1f05ph0M125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_JHUgenv6"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/VBFHiggs0L1f05ph0M125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_JHUgenv6.root"
		elif (nickname =="VBFHiggs0MM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_JHUgenv6"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/VBFHiggs0MM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_JHUgenv6.root"
		elif (nickname =="VBFHiggs0Mf05ph0M125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_JHUgenv6"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/VBFHiggs0Mf05ph0M125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_JHUgenv6.root"
		elif (nickname =="VBFHiggs0PHM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_JHUgenv6"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/VBFHiggs0PHM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_JHUgenv6.root"
		elif (nickname =="VBFHiggs0PHf05ph0M125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_JHUgenv6"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/VBFHiggs0PHf05ph0M125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_JHUgenv6.root"
		elif (nickname =="VBFHiggs0PMM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_JHUgenv6"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/VBFHiggs0PMM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_JHUgenv6.root"
		elif (nickname =="VVTo2L2Nu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_amcatnlo-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/VVTo2L2Nu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_amcatnlo-pythia8.root"
		elif (nickname =="VVTo2L2Nu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_amcatnlo-pythia8_ext1"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/VVTo2L2Nu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_amcatnlo-pythia8_ext1.root"
		elif (nickname =="W1JetsToLNu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/W1JetsToLNu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8.root"
		elif (nickname =="W2JetsToLNu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/W2JetsToLNu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8.root"
		elif (nickname =="W2JetsToLNu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext1"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/W2JetsToLNu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext1.root"
		elif (nickname =="W3JetsToLNu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/W3JetsToLNu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8.root"
		elif (nickname =="W3JetsToLNu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext1"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/W3JetsToLNu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext1.root"
		elif (nickname =="W4JetsToLNu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/W4JetsToLNu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8.root"
		elif (nickname =="W4JetsToLNu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext1"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/W4JetsToLNu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext1.root"
		elif (nickname =="W4JetsToLNu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext2"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/W4JetsToLNu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext2.root"
		elif (nickname =="WGToLNuG_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_amcatnlo-pythia8_ext1"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/WGToLNuG_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_amcatnlo-pythia8_ext1.root"
		elif (nickname =="WGToLNuG_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_amcatnlo-pythia8_ext2"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/WGToLNuG_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_amcatnlo-pythia8_ext2.root"
		elif (nickname =="WGToLNuG_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_amcatnlo-pythia8_ext3"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/WGToLNuG_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_amcatnlo-pythia8_ext3.root"
		elif (nickname =="WGstarToLNuEE_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/WGstarToLNuEE_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph.root"
		elif (nickname =="WGstarToLNuMuMu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/WGstarToLNuMuMu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph.root"
		elif (nickname =="WHiggs0L1UndecayedM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_JHUgen"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/WHiggs0L1UndecayedM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_JHUgen.root"
		elif (nickname =="WHiggs0L1fWH05ph0UndecayedM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_JHUgen"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/WHiggs0L1fWH05ph0UndecayedM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_JHUgen.root"
		elif (nickname =="WHiggs0MUndecayedM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_JHUgen"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/WHiggs0MUndecayedM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_JHUgen.root"
		elif (nickname =="WHiggs0MfWH05ph0UndecayedM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_JHUgen"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/WHiggs0MfWH05ph0UndecayedM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_JHUgen.root"
		elif (nickname =="WHiggs0PHUndecayedM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_JHUgen"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/WHiggs0PHUndecayedM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_JHUgen.root"
		elif (nickname =="WHiggs0PHfWH05ph0UndecayedM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_JHUgen"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/WHiggs0PHfWH05ph0UndecayedM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_JHUgen.root"
		elif (nickname =="WHiggs0PMUndecayedM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_JHUgen"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/WHiggs0PMUndecayedM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_JHUgen.root"
		elif (nickname =="WJetsToLNu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/WJetsToLNu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8.root"
		elif (nickname =="WJetsToLNu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext2"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/WJetsToLNu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_madgraph-pythia8_ext2.root"
		elif (nickname =="WWTo1L1Nu2Q_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_amcatnlo-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/WWTo1L1Nu2Q_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_amcatnlo-pythia8.root"
		elif (nickname =="WZJToLLLNu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/WZJToLLLNu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_pythia8.root"
		elif (nickname =="WZTo1L1Nu2Q_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_amcatnlo-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/WZTo1L1Nu2Q_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_amcatnlo-pythia8.root"
		elif (nickname =="WZTo1L3Nu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_amcatnlo-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/WZTo1L3Nu_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_amcatnlo-pythia8.root"
		elif (nickname =="WZTo2L2Q_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_amcatnlo-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/WZTo2L2Q_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_amcatnlo-pythia8.root"
		elif (nickname =="WminusHToTauTauM110_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/WminusHToTauTauM110_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root"
		elif (nickname =="WminusHToTauTauM120_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/WminusHToTauTauM120_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root"
		elif (nickname =="WminusHToTauTauM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/WminusHToTauTauM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root"
		elif (nickname =="WminusHToTauTauM130_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/WminusHToTauTauM130_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root"
		elif (nickname =="WminusHToTauTauM140_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/WminusHToTauTauM140_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root"
		elif (nickname =="WplusHToTauTauM110_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/WplusHToTauTauM110_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root"
		elif (nickname =="WplusHToTauTauM120_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/WplusHToTauTauM120_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root"
		elif (nickname =="WplusHToTauTauM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/WplusHToTauTauM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root"
		elif (nickname =="WplusHToTauTauM130_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/WplusHToTauTauM130_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root"
		elif (nickname =="WplusHToTauTauM140_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/WplusHToTauTauM140_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root"
		elif (nickname =="ZHToTauTauM110_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/ZHToTauTauM110_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root"
		elif (nickname =="ZHToTauTauM120_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/ZHToTauTauM120_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root"
		elif (nickname =="ZHToTauTauM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/ZHToTauTauM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root"
		elif (nickname =="ZHToTauTauM130_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/ZHToTauTauM130_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root"
		elif (nickname =="ZHToTauTauM140_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/ZHToTauTauM140_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_powheg-pythia8.root"
		elif (nickname =="ZHiggs0L1UndecayedM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_JHUgen"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/ZHiggs0L1UndecayedM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_JHUgen.root"
		elif (nickname =="ZHiggs0L1fZH05ph0UndecayedM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_JHUgen"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/ZHiggs0L1fZH05ph0UndecayedM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_JHUgen.root"
		elif (nickname =="ZHiggs0MUndecayedM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_JHUgen"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/ZHiggs0MUndecayedM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_JHUgen.root"
		elif (nickname =="ZHiggs0MfZH05ph0UndecayedM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_JHUgen"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/ZHiggs0MfZH05ph0UndecayedM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_JHUgen.root"
		elif (nickname =="ZHiggs0PHUndecayedM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_JHUgen"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/ZHiggs0PHUndecayedM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_JHUgen.root"
		elif (nickname =="ZHiggs0PHfZH05ph0UndecayedM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_JHUgen"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/ZHiggs0PHfZH05ph0UndecayedM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_JHUgen.root"
		elif (nickname =="ZHiggs0PMUndecayedM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_JHUgen"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/ZHiggs0PMUndecayedM125_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_JHUgen.root"
		elif (nickname =="ZZTo2L2Q_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_amcatnlo-pythia8"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/ZZTo2L2Q_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_amcatnlo-pythia8.root"
		elif (nickname =="ZZTo4L_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_amcatnlo-pythia8_ext1"):
			return "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/dwolfsch/higgs-kit/Svfit/MergedCaches/2018-02-19_15-29_clsssivSvfit_inputs2017-12-26_HiggsMassConstraint/ZZTo4L_RunIISummer16MiniAODv2_PUMoriond17_13TeV_MINIAOD_amcatnlo-pythia8_ext1.root"

