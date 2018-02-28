# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import re
import json
import Artus.Utility.jsonTools as jsonTools
import Kappa.Skimming.datasetsHelperTwopz as datasetsHelperTwopz

class tt_ArtusConfig(dict)




	def __init__(self, nick, **kwargs):                #Maybe change this the arguments to process/year and DATA/MC
		import HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2Analysis.Includes.Run2Quantities as r2q
		"""
		#KIT is using this, not a bad idea. If done add year and runnumber as wel
		datasetsHelper = datasetsHelperTwopz.datasetsHelperTwopz("Kappa/Skimming/data/datasets.json") 
		isData = datasetsHelper.isData(nick)
		isEmbedding = datasetsHelper.isEmbedding(nick)
		isTTbar = re.match("TT(To|_|Jets)", nick)
		isDY = re.match("DY.?JetsToLLM(50|150)", nick)
		isWjets = re.match("W.?JetsToLNu", nick)
		"""
		#Change this json config files as well?
		self["include"] = ["$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/ArtusConfigs/Run2Analysis/Includes/settingsLooseElectronID.json", 
				"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/ArtusConfigs/Run2Analysis/Includes/settingsLooseMuonID.json",
				"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/ArtusConfigs/Run2Analysis/Includes/settingsElectronID.json",
				"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/ArtusConfigs/Run2Analysis/Includes/settingsMuonID.json",
				"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/ArtusConfigs/Run2Analysis/Includes/settingsTauID.json",
				"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/ArtusConfigs/Run2Analysis/Includes/settingsJEC.json",
				"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/ArtusConfigs/Run2Analysis/Includes/settingsJECUncertaintySplit.json",
				"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/ArtusConfigs/Run2Analysis/Includes/settingsJetID.json",
				"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/ArtusConfigs/Run2Analysis/Includes/settingsBTaggedJetID.json",
				"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/ArtusConfigs/Run2Analysis/Includes/settingsSvfit.json",
				"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/ArtusConfigs/Run2Analysis/Includes/settingsMinimalPlotlevelFilter_tt.json",
				"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/ArtusConfigs/Includes/settingsMVATestMethods.json",
				"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/ArtusConfigs/Run2Analysis/Includes/settingsTauES.json",
				"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/ArtusConfigs/Run2CPStudies/Includes/settingsTauPolarisationMva.json"]

		self["TauPolarisationTmvaWeights"] = ["/afs/cern.ch/user/m/mfackeld/public/weights_tmva/training.weights.xml",
						"/afs/cern.ch/user/m/mfackeld/public/weights_sklearn/training_tt.weights.xml"]

		self["Channel"] = "TT"
		self["MinNTaus"] = 2	
		self["TauID"] = "TauIDRecommendation13TeV"
		self["TauUseOldDMs"] = True
		self["TauLowerPtCuts"] = ["40"]  #in json with default
		self["TauUpperAbsEtaCuts"] = ["2.1"] #in json with default
		self["DiTauPairMinDeltaRCut"] = 0.5
		self["DiTauPairIsTauIsoMVA"] = True
		self["EventWeight"] = "eventWeight"
		self["RooWorkspace" = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/scaleFactorWeights/htt_scalefactors_sm_moriond_v2.root"
		self["TauTauTriggerWeightWorkspace"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/scaleFactorWeights/htt_scalefactors_sm_moriond_v2.root"

		self["TauTauTriggerWeightWorkspaceWeightNames"] = ["0:triggerWeight", "1:triggerWeight"] 
		self["TauTauTriggerWeightWorkspaceObjectNames"] = ["0:t_genuine_TightIso_tt_ratio,t_fake_TightIso_tt_ratio", "1:t_genuine_TightIso_tt_ratio,t_fake_TightIso_tt_ratio"]
		self["TauTauTriggerWeightWorkspaceObjectArguments"] = ["0:t_pt,t_dm","1:t_pt,t_dm"]
		self["EleTauFakeRateWeightFile"] = ["0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/scaleFactorWeights/antiElectronDiscrMVA6FakeRateWeights.root",
						"1:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/scaleFactorWeights/antiElectronDiscrMVA6FakeRateWeights.root"]
		
		self["TauTauRestFrameReco"] = "collinear_approximation"
		self["TriggerObjectLowerPtCut"] = 28.0
		self["InvalidateNonMatchingElectrons"] = False
		self["InvalidateNonMatchingMuons"] = False
		self["InvalidateNonMatchingTaus"] = True
		self["InvalidateNonMatchingJets"] = False
		self["UseUWGenMatching"] = "true"                   #TODO change this to boolean? or change the rest to string?
		self["DirectIso"] = True
		self["TopPtReweightingStrategy"] = "Run1"


		self["NoHltFiltering"]=False
		self["DiTauPairNoHLT"]= True		




		if "Embedding" in nick:
			self["NoHltFiltering"]= True
			self["DiTauPairNoHLT"]= True
		else:
			self["NoHltFiltering"]=False
			self["DiTauPairNoHLT"]= True	
		

		 #set it here and if it is something else then change it in the ifs below
		self["HltPaths"] = ["HLT_DoubleMediumIsoPFTau35_Trk1_eta2p1_Reg", "HLT_DoubleMediumCombinedIsoPFTau35_Trk1_eta2p1_Reg"]     
		self["TauTriggerFilterNames"] = ["HLT_DoubleMediumIsoPFTau35_Trk1_eta2p1_Reg_v:hltDoublePFTau35TrackPt1MediumIsolationDz02Reg",   #here are : in string
						"HLT_DoubleMediumCombinedIsoPFTau35_Trk1_eta2p1_Reg_v:hltDoublePFTau35TrackPt1MediumCombinedIsolationDz02Reg"]

		if "Run2016" in nick and not "Run2016H" in nick:
			self["HltPaths"] = ["HLT_DoubleMediumIsoPFTau35_Trk1_eta2p1_Reg"]
			self["TauTriggerFilterNames"]=["HLT_DoubleMediumIsoPFTau35_Trk1_eta2p1_Reg_v:hltDoublePFTau35TrackPt1MediumIsolationDz02Reg"]


		elif "Run2016H" in nick:
			self["HltPaths"] = ["HLT_DoubleMediumCombinedIsoPFTau35_Trk1_eta2p1_Reg"]
			self["TauTriggerFilterNames"] = ["HLT_DoubleMediumCombinedIsoPFTau35_Trk1_eta2p1_Reg_v:hltDoublePFTau35TrackPt1MediumCombinedIsolationDz02Reg"]

		elif "Fall15MiniAODv2" in nick or "Run2015D" in nick or "Embedding2015" in nick:
			self["HltPaths"] = ["HLT_DoubleMediumIsoPFTau35_Trk1_eta2p1_Reg"]
			self["TauTriggerFilterNames"] = ["HLT_DoubleMediumIsoPFTau35_Trk1_eta2p1_Reg_v:hltDoublePFTau35TrackPt1MediumIsolationDz02Reg"]

		elif "Spring16" in nick or "Embedding2016" in nick or "EmbeddingMC" in nick:	 #TODO Ask thomas what it should be line 40 in json
			self["HltPaths"] = [""]


		self["Quantities"]=[]
		if "Run2015" in nick:
			self["Quantities"] += r2q.fourVectorQuantities()
			self["Quantities"] += r2q.syncQuantities()
			self["Quantities"] += r2q.svfitSyncQuantities()
			self["Quantities"] += r2q.splitJecUncertaintyQuantities()
			self["Quantities"] += ["nLooseElectrons", "nLooseMuons", "nDiTauPairCandidates", "nAllDiTauPairCandidates"] #Check if they are used everywhere if so make this the start list
		else:
			self["Quantities"]+=r2q.fourVectorQuantities()
			self["Quantities"]+=r2q.syncQuantities()
			self["Quantities"]+=r2q.svfitSyncQuantities()
			self["Quantities"]+=r2q.splitJecUncertaintyQuantities() #TODO cp quantities to python file
			






