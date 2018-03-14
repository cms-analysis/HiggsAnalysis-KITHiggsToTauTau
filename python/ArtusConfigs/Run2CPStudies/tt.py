# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import re
import json
import Artus.Utility.jsonTools as jsonTools
import Kappa.Skimming.datasetsHelperTwopz as datasetsHelperTwopz
import copy

import HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Run2Analysis.Includes.Run2Quantities as r2q
import HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Run2CPStudies.Includes.Run2CPQuantities as r2cpq


import HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Run2Analysis.Includes.settingsElectronID as sEID
import HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Run2Analysis.Includes.settingsMuonID as sMID
import HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Run2Analysis.Includes.settingsTauID as sTID
import HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Run2Analysis.Includes.settingsJetID as sJID 
import HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Run2Analysis.Includes.settingsBTaggedJetID as sBTJID
import HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Run2Analysis.Includes.settingsSvfit as sSvfit
import HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Run2Analysis.Includes.settingsMinimalPlotlevelFilter as sMPlF
import HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Run2Analysis.Includes.settingsTauES as sTES
import HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Run2Analysis.Includes.settingsJEC as sJEC
import HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Run2Analysis.Includes.settingsJECUncertaintySplit as sJECUS

import HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Includes.settingsMVATestMethods as sMVATM

import HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Includes.Run2CPStudies.Includes.settingsTauPolarisationMva as sTPMVA


class tt_ArtusConfig(dict):

	def __init__(self):
		self.base_copy = copy.deepcopy(self)
		self.datasetsHelper = datasetsHelperTwopz.datasetsHelperTwopz("Kappa/Skimming/data/datasets.json") 
			

	def build_config(self, nickname):                #Maybe change this the arguments to process/year and DATA/MC
		isData = self.datasetsHelper.isData(nickname)
		isSignal = self.datasetsHelper.isSignal(nickname)
		isEmbedding = self.datasetsHelper.isEmbedded(nickname)
		isTTbar = re.match("TT(To|_|Jets)", nickname)
		isDY = re.match("DY.?JetsToLLM(50|150)", nickname)
		isWjets = re.match("W.?JetsToLNu", nickname)
		isLFV = ("LFV" in nickname)
		is2015 = re.match("(Run2015|Fall15|Embedding15)*?",nickname) #I am not 100% sure if this is exclusive
		is2016 = re.match("(Run2016|Sprint16|Summer16|Fall16|Embedding16)*?",nickname) #I am not 100% sure if this is exclusive	
		is2017 = re.match("(Run2017|Summer17|Embedding17)*?",nickname) #I am not 100% sure if this is exclusive		
		
		#Change this json config files as well?
		"""
		if hasattr(self, "include") == False:
			self["include"] = []
		self["include"] += ["$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/ArtusConfigs/Run2Analysis/Includes/settingsLooseElectronID.json",  #Done
				"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/ArtusConfigs/Run2Analysis/Includes/settingsLooseMuonID.json", #Done
				"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/ArtusConfigs/Run2Analysis/Includes/settingsElectronID.json",  #Done
				"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/ArtusConfigs/Run2Analysis/Includes/settingsMuonID.json", #Done
				"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/ArtusConfigs/Run2Analysis/Includes/settingsTauID.json", #Done
				"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/ArtusConfigs/Run2Analysis/Includes/settingsJEC.json", #Done
				"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/ArtusConfigs/Run2Analysis/Includes/settingsJECUncertaintySplit.json", #Done
				"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/ArtusConfigs/Run2Analysis/Includes/settingsJetID.json",  #Done
				"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/ArtusConfigs/Run2Analysis/Includes/settingsBTaggedJetID.json", #Done
				"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/ArtusConfigs/Run2Analysis/Includes/settingsSvfit.json", #Done
				"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/ArtusConfigs/Run2Analysis/Includes/settingsMinimalPlotlevelFilter_tt.json", #Done
				"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/ArtusConfigs/Includes/settingsMVATestMethods.json",  #Done
				"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/ArtusConfigs/Run2Analysis/Includes/settingsTauES.json", #Done
				"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/ArtusConfigs/Run2CPStudies/Includes/settingsTauPolarisationMva.json"] #Done 
		"""


		ElectronID_config = sEID.Electron_ID(nickname)
		ElectronID_config.looseElectron_ID(nickname) 		#append the config for loose electron ID because it is used
		self.update(ElectronID_config)	

		MuonID_config = sMID.Muon_ID(nickname)
		ElectronID_config.looseMuon_ID(nickname) 		#append the config for loose Muon ID because it is used
		self.update(MuonID_config)	

		TauID_config = sTID.Tau_ID(nickname)			#here loose is not appended since loose tau ID is not used
		self.update(TauID_config)

		JEC_config = sJEC.JEC(nickname)
		self.update(JEC_config)

		JECUncertaintySplit_config = sJECUS.JECUncertaintySplit
		self.update(JECUncertaintySplit_config)

		JetID_config = sJID.Jet_ID(nickname)
		self.update(JetID_config)

		BTaggedJet_config = sBTJID.BTaggedJet_ID(nickname)
		self.update(BTaggedJet_config)

		Svfit_config = sSvfit.Svfit(nickname)
		self.update(Svfit_config)

		MinimalPlotlevelFilter_config = sMPlF.MinimalPlotlevelFilter()
		MinimalPlotlevelFilter_config.tt()
		self.update(MinimalPlotlevelFilter_config)
		
		MVATestMethods_config = sMVATM.MVATestMethods()
		self.update(MVATestMethods_config)

		TauES_config = sTES.TauES(nickname)
		self.update(TauES_config)
		
		TauPolarisationMva_config = sTPMVA.TauPolarisationMva()
		self.update(TauPolarisationMva_config)
	



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
		self["RooWorkspace"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/scaleFactorWeights/htt_scalefactors_sm_moriond_v2.root"
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
		self["UseUWGenMatching"] = True                   #TODO change this to boolean? or change the rest to string?
		self["DirectIso"] = True
		self["TopPtReweightingStrategy"] = "Run1"


		self["NoHltFiltering"]= False
		self["DiTauPairNoHLT"]= True		

		self["OSChargeLeptons"] = True

		self["AddGenMatchedTaus"] = True,
		self["AddGenMatchedTauJets"] = True,
		self["BranchGenMatchedTaus"] = True,

		self["Consumers"] = ["KappaLambdaNtupleConsumer",
			"cutflow_histogram",
			"SvfitCacheConsumer"]#,
			#"CutFlowTreeConsumer",
			#"KappaTausConsumer",
			#"KappaTaggedJetsConsumer",
			#"RunTimeConsumer",
			#"PrintEventsConsumer",
			#"PrintGenParticleDecayTreeConsumer"]

		if isEmbedding or "Spring16" in nickname:
			self["NoHltFiltering"]= True
			self["DiTauPairNoHLT"]= True
		else:
			self["NoHltFiltering"]=False
			self["DiTauPairNoHLT"]= False	
		

		 #set it here and if it is something else then change it in the ifs below
		self["HltPaths"] = ["HLT_DoubleMediumIsoPFTau35_Trk1_eta2p1_Reg", "HLT_DoubleMediumCombinedIsoPFTau35_Trk1_eta2p1_Reg"]     
		self["TauTriggerFilterNames"] = ["HLT_DoubleMediumIsoPFTau35_Trk1_eta2p1_Reg_v:hltDoublePFTau35TrackPt1MediumIsolationDz02Reg",   #here are : in string
						"HLT_DoubleMediumCombinedIsoPFTau35_Trk1_eta2p1_Reg_v:hltDoublePFTau35TrackPt1MediumCombinedIsolationDz02Reg"]

		if "Run2016" in nickname and not "Run2016H" in nickname:
			self["HltPaths"] = ["HLT_DoubleMediumIsoPFTau35_Trk1_eta2p1_Reg"]
			self["TauTriggerFilterNames"]=["HLT_DoubleMediumIsoPFTau35_Trk1_eta2p1_Reg_v:hltDoublePFTau35TrackPt1MediumIsolationDz02Reg"]


		elif "Run2016H" in nickname:
			self["HltPaths"] = ["HLT_DoubleMediumCombinedIsoPFTau35_Trk1_eta2p1_Reg"]
			self["TauTriggerFilterNames"] = ["HLT_DoubleMediumCombinedIsoPFTau35_Trk1_eta2p1_Reg_v:hltDoublePFTau35TrackPt1MediumCombinedIsolationDz02Reg"]

		elif "Fall15MiniAODv2" in nickname or "Run2015D" in nickname or "Embedding2015" in nickname:
			self["HltPaths"] = ["HLT_DoubleMediumIsoPFTau35_Trk1_eta2p1_Reg"]
			self["TauTriggerFilterNames"] = ["HLT_DoubleMediumIsoPFTau35_Trk1_eta2p1_Reg_v:hltDoublePFTau35TrackPt1MediumIsolationDz02Reg"]

		elif "Spring16" in nickname or "Embedding2016" in nickname or "EmbeddingMC" in nickname:	 #TODO Ask thomas what it should be line 40 in json
			self["HltPaths"] = [""]

		#Quantities, this looks for tt em mt et very similar, check if it is the same and if so put it in baseconfig for all channels
		self["Quantities"]=[]
		if isData and is2015:
			self["Quantities"] += r2q.fourVectorQuantities()
			self["Quantities"] += r2q.syncQuantities()
			self["Quantities"] += r2cpq.weightQuantities()
			self["Quantities"] += r2cpq.recoPolarisationQuantities()
			self["Quantities"] += ["nLooseElectrons", "nLooseMuons", "nDiTauPairCandidates", "nAllDiTauPairCandidates"] #Check if they are used everywhere if so make this the start list
		elif isDY and is2016:
			self["Quantities"] += r2q.fourVectorQuantities()
			self["Quantities"] += r2q.syncQuantities()
			self["Quantities"] += r2q.svfitSyncQuantities()
			self["Quantities"] += r2q.splitJecUncertaintyQuantities()
			self["Quantities"] += r2cpq.genQuantities()
			self["Quantities"] += r2cpq.weightQuantities()
			self["Quantities"] += r2cpq.genMatchedCPQuantities()
			self["Quantities"] += r2cpq.recoCPQuantities()
			self["Quantities"] += r2cpq.melaQuantities()
			self["Quantities"] += r2cpq.recoPolarisationQuantities()
			self["Quantities"] += r2cpq.recoPolarisationQuantitiesSvfit()
			self["Quantities"] += [] #TODO "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/ArtusConfigs/Includes/SingleTauQuantities.json"
			self["Quantities"] += ["nLooseElectrons", "nLooseMuons", "nDiTauPairCandidates", "nAllDiTauPairCandidates"] #Check if they are used everywhere if so make this the start list
			self["Quantities"] += ["tauSpinnerPolarisation"]
		elif isSignal and is2016:
			self["Quantities"] += r2q.fourVectorQuantities()
			self["Quantities"] += r2q.syncQuantities()
			self["Quantities"] += r2q.svfitSyncQuantities()
			self["Quantities"] += r2q.splitJecUncertaintyQuantities()
			self["Quantities"] += r2cpq.genQuantities()
			self["Quantities"] += r2cpq.genHiggsQuantities()
			self["Quantities"] += r2cpq.weightQuantities()
			self["Quantities"] += r2cpq.genMatchedCPQuantities()
			self["Quantities"] += r2cpq.recoCPQuantities()
			self["Quantities"] += r2cpq.melaQuantities()
			self["Quantities"] += ["nLooseElectrons", "nLooseMuons", "nDiTauPairCandidates", "nAllDiTauPairCandidates"] #Check if they are used everywhere if so make this the start list
		elif not (isDY or isSignal) and is2015:
			self["Quantities"] += r2q.fourVectorQuantities()
			self["Quantities"] += r2q.syncQuantities()
			self["Quantities"] += r2cpq.weightQuantities()
			self["Quantities"] += r2cpq.recoPolarisationQuantities()
			self["Quantities"] += ["nLooseElectrons", "nLooseMuons", "nDiTauPairCandidates", "nAllDiTauPairCandidates"] #Check if they are used everywhere if so make this the start list
		elif isDY and is2015:
			self["Quantities"] += r2q.fourVectorQuantities()
			self["Quantities"] += r2q.syncQuantities()
			self["Quantities"] += r2cpq.genQuantities()			
			self["Quantities"] += r2cpq.weightQuantities()
			self["Quantities"] += r2cpq.genMatchedCPQuantities()
			self["Quantities"] += r2cpq.recoPolarisationQuantities()
			self["Quantities"] += ["nLooseElectrons", "nLooseMuons", "nDiTauPairCandidates", "nAllDiTauPairCandidates"] #Check if they are used everywhere if so make this the start list			
		elif isSignal and is2015:    #almost the same as 2016 signal, no splitJecUncertaintyQuantities()
			self["Quantities"] += r2q.fourVectorQuantities()
			self["Quantities"] += r2q.syncQuantities()
			self["Quantities"] += r2q.svfitSyncQuantities()
			self["Quantities"] += r2cpq.genQuantities()
			self["Quantities"] += r2cpq.genHiggsQuantities()
			self["Quantities"] += r2cpq.weightQuantities()
			self["Quantities"] += r2cpq.genMatchedCPQuantities()
			self["Quantities"] += r2cpq.recoCPQuantities()
			self["Quantities"] += r2cpq.melaQuantities()
			self["Quantities"] += ["nLooseElectrons", "nLooseMuons", "nDiTauPairCandidates", "nAllDiTauPairCandidates"]
		elif isEmbedding and is2016:
			self["Quantities"] += r2q.fourVectorQuantities()
			self["Quantities"] += r2q.syncQuantities()
			self["Quantities"] += r2q.splitJecUncertaintyQuantities()
			self["Quantities"] += r2cpq.genQuantities()
			self["Quantities"] += r2cpq.weightQuantities()			
			self["Quantities"] += r2cpq.recoPolarisationQuantities()
			self["Quantities"] += ["nLooseElectrons", "nLooseMuons", "nDiTauPairCandidates", "nAllDiTauPairCandidates"] #Check if they are used everywhere if so make this the start list
			self["Quantities"] += ["tauSpinnerPolarisation"]
		elif isLFV and is2016:
			self["Quantities"] += r2q.fourVectorQuantities()
			self["Quantities"] += r2q.syncQuantities()
			self["Quantities"] += r2q.splitJecUncertaintyQuantities()
			self["Quantities"] += r2cpq.genQuantities()
			self["Quantities"] += r2cpq.weightQuantities()
		else:
			self["Quantities"] += r2q.fourVectorQuantities()
			self["Quantities"] += r2q.syncQuantities()
			self["Quantities"] += r2q.svfitSyncQuantities()
			self["Quantities"] += r2q.splitJecUncertaintyQuantities()
			self["Quantities"] += r2cpq.weightQuantities()
			self["Quantities"] += r2cpq.recoCPQuantities()
			self["Quantities"] += r2cpq.melaQuantities()
			self["Quantities"] += r2cpq.recoPolarisationQuantities()			
			self["Quantities"] += r2cpq.recoPolarisationQuantitiesSvfit()
			self["Quantities"] += ["nLooseElectrons", "nLooseMuons", "nDiTauPairCandidates", "nAllDiTauPairCandidates"] #Check if they are used everywhere if so make this the start list

		self["Quantities"]=list(set(self["Quantities"])) #removes dublicates from list by making it a set and then again a list, dont know if it should be a list or can be left as a set
		
		#Producers and filters, TODO filter everything which is the same and use this as the startint list, then just add the other variables per sample
		self["Processors"]=[]
		if isDY and is2016:
			self["Processors"] = ["producer:HltProducer",
					"filter:HltFilter",
					"producer:MetSelector",
					"producer:TauCorrectionsProducer",
					"producer:ValidTausProducer",
					"filter:ValidTausFilter",
					"producer:TauTriggerMatchingProducer",
					"filter:MinTausCountFilter",
					"producer:ValidElectronsProducer",
					"producer:ValidMuonsProducer",
					"producer:ValidTTPairCandidatesProducer",
					"filter:ValidDiTauPairCandidatesFilter",
					"producer:HttValidLooseElectronsProducer",
					"producer:HttValidLooseMuonsProducer",
					"producer:Run2DecayChannelProducer",
					"producer:TaggedJetCorrectionsProducer",
					"producer:ValidTaggedJetsProducer",
					"producer:ValidBTaggedJetsProducer",
					"producer:TaggedJetUncertaintyShiftProducer",
					"producer:MetCorrector",
					"producer:TauTauRestFrameSelector",
					"producer:DiLeptonQuantitiesProducer",
					"producer:DiJetQuantitiesProducer",
					"producer:SimpleEleTauFakeRateWeightProducer",
					"producer:SimpleMuTauFakeRateWeightProducer",
					"producer:ZPtReweightProducer",
					"filter:MinimalPlotlevelFilter",
					#"producer:MVATestMethodsProducer",
					"producer:SvfitProducer",
					"producer:MELAProducer",
					"producer:SimpleFitProducer",
					"producer:TauTauTriggerWeightProducer",
					"producer:GenMatchedTauCPProducer",
					"producer:RefitVertexSelector",
					"producer:RecoTauCPProducer",
					"producer:PolarisationQuantitiesSvfitProducer",
					"producer:PolarisationQuantitiesSimpleFitProducer",
					#"producer:TauPolarisationTmvaReader",
					"producer:EventWeightProducer"]

		elif not (isDY or isSignal) and is2015:
			self["Processors"] = ["producer:HltProducer",
					"filter:HltFilter",
					"producer:MetSelector",
					"producer:TauCorrectionsProducer",
					"producer:ValidTausProducer",
					"filter:ValidTausFilter",
					"producer:TauTriggerMatchingProducer",
					"filter:MinTausCountFilter",
					"producer:ValidElectronsProducer",
					"producer:ValidMuonsProducer",
					"producer:ValidTTPairCandidatesProducer",
					"filter:ValidDiTauPairCandidatesFilter",
					"producer:HttValidLooseElectronsProducer",
					"producer:HttValidLooseMuonsProducer",
					"producer:Run2DecayChannelProducer",
					"producer:MvaMetSelector",
					"producer:TaggedJetCorrectionsProducer",
					"producer:ValidTaggedJetsProducer",
					"producer:ValidBTaggedJetsProducer",
					#"producer:TaggedJetUncertaintyShiftProducer",
					"producer:MetCorrector",
					"producer:MvaMetCorrector",
					"producer:TauTauRestFrameSelector",
					"producer:DiLeptonQuantitiesProducer",
					"producer:DiJetQuantitiesProducer",
					"producer:TopPtReweightingProducer",
					"filter:MinimalPlotlevelFilter",
					#"producer:MVATestMethodsProducer",
					#"producer:SvfitProducer",
					#"producer:MELAProducer",
					#"producer:SimpleFitProducer",
					#"producer:RefitVertexSelector",
					"producer:RecoTauCPProducer",
					"producer:PolarisationQuantitiesSvfitProducer",
					"producer:PolarisationQuantitiesSimpleFitProducer",
					#"producer:TauPolarisationTmvaReader",
					"producer:EventWeightProducer"]
		
		elif isDY and is2015:
			self["Processors"] = ["producer:HltProducer",
					"filter:HltFilter",
					"producer:MetSelector",
					"producer:TauCorrectionsProducer",
					"producer:ValidTausProducer",
					"filter:ValidTausFilter",
					"producer:TauTriggerMatchingProducer",
					"filter:MinTausCountFilter",
					"producer:ValidElectronsProducer",
					"producer:ValidMuonsProducer",
					"producer:ValidTTPairCandidatesProducer",
					"filter:ValidDiTauPairCandidatesFilter",
					"producer:HttValidLooseElectronsProducer",
					"producer:HttValidLooseMuonsProducer",
					"producer:Run2DecayChannelProducer",
					"producer:MvaMetSelector",
					"producer:TaggedJetCorrectionsProducer",
					"producer:ValidTaggedJetsProducer",
					"producer:ValidBTaggedJetsProducer",
					#"producer:TaggedJetUncertaintyShiftProducer",
					"producer:MetCorrector",
					"producer:MvaMetCorrector",
					"producer:TauTauRestFrameSelector",
					"producer:DiLeptonQuantitiesProducer",
					"producer:DiJetQuantitiesProducer",
					"producer:ZPtReweightProducer",
					"filter:MinimalPlotlevelFilter",
					#"producer:MVATestMethodsProducer",
					#"producer:SvfitProducer",
					#"producer:MELAProducer",
					#"producer:SimpleFitProducer",
					"producer:EleTauFakeRateWeightProducer",
					"producer:GenMatchedTauCPProducer",
					#"producer:RefitVertexSelector",
					"producer:RecoTauCPProducer",
					"producer:PolarisationQuantitiesSvfitProducer",
					"producer:PolarisationQuantitiesSimpleFitProducer",
					#"producer:TauPolarisationTmvaReader",
					"producer:EventWeightProducer"]
		elif isData and is2016:
			self["Processors"] = ["producer:HltProducer",
					"filter:HltFilter",
					"producer:MetSelector",
					"producer:ValidTausProducer",
					"filter:ValidTausFilter",
					"producer:TauTriggerMatchingProducer",
					"filter:MinTausCountFilter",
					"producer:ValidElectronsProducer",
					"producer:ValidMuonsProducer",
					"producer:ValidTTPairCandidatesProducer",
					"filter:ValidDiTauPairCandidatesFilter",
					"producer:HttValidLooseElectronsProducer",
					"producer:HttValidLooseMuonsProducer",
					"producer:Run2DecayChannelProducer",
					"producer:TaggedJetCorrectionsProducer",
					"producer:ValidTaggedJetsProducer",
					"producer:ValidBTaggedJetsProducer",
					"producer:TaggedJetUncertaintyShiftProducer",
					"producer:TauTauRestFrameSelector",
					"producer:DiLeptonQuantitiesProducer",
					"producer:DiJetQuantitiesProducer",
					"filter:MinimalPlotlevelFilter",
					#"producer:MVATestMethodsProducer",
					"producer:SvfitProducer",
					"producer:MELAProducer",
					"producer:SimpleFitProducer",
					"producer:RefitVertexSelector",
					"producer:RecoTauCPProducer",
					"producer:PolarisationQuantitiesSvfitProducer",
					"producer:PolarisationQuantitiesSimpleFitProducer",
					#"producer:TauPolarisationTmvaReader",
					"producer:EventWeightProducer"]
		
		elif isData and is2015:
			self["Processors"] = ["producer:HltProducer",
					"filter:HltFilter",
					"producer:MetSelector",
					"producer:ValidTausProducer",
					"filter:ValidTausFilter",
					"producer:TauTriggerMatchingProducer",
					"filter:MinTausCountFilter",
					"producer:ValidElectronsProducer",
					"producer:ValidMuonsProducer",
					"producer:ValidTTPairCandidatesProducer",
					"filter:ValidDiTauPairCandidatesFilter",
					"producer:HttValidLooseElectronsProducer",
					"producer:HttValidLooseMuonsProducer",
					"producer:Run2DecayChannelProducer",
					"producer:MvaMetSelector",
					"producer:TaggedJetCorrectionsProducer",
					"producer:ValidTaggedJetsProducer",
					"producer:ValidBTaggedJetsProducer",
					#"producer:TaggedJetUncertaintyShiftProducer",
					"producer:TauTauRestFrameSelector",
					"producer:DiLeptonQuantitiesProducer",
					"producer:DiJetQuantitiesProducer",
					"filter:MinimalPlotlevelFilter",
					#"producer:MVATestMethodsProducer",
					#"producer:SvfitProducer",
					#"producer:MELAProducer",
					#"producer:SimpleFitProducer",
					#"producer:RefitVertexSelector",
					"producer:RecoTauCPProducer",
					"producer:PolarisationQuantitiesSvfitProducer",
					"producer:PolarisationQuantitiesSimpleFitProducer",
					#"producer:TauPolarisationTmvaReader",
					"producer:EventWeightProducer"]
		elif isSignal and is2016:
			self["Processors"] = ["producer:HltProducer",
					"filter:HltFilter",
					"producer:MetSelector",
					"producer:TauCorrectionsProducer",
					"producer:ValidTausProducer",
					"filter:ValidTausFilter",
					"producer:TauTriggerMatchingProducer",
					"filter:MinTausCountFilter",
					"producer:ValidElectronsProducer",
					"producer:ValidMuonsProducer",
					"producer:ValidTTPairCandidatesProducer",
					"filter:ValidDiTauPairCandidatesFilter",
					"producer:HttValidLooseElectronsProducer",
					"producer:HttValidLooseMuonsProducer",
					"producer:Run2DecayChannelProducer",
					"producer:TaggedJetCorrectionsProducer",
					"producer:ValidTaggedJetsProducer",
					"producer:ValidBTaggedJetsProducer",
					"producer:TaggedJetUncertaintyShiftProducer",
					"producer:MetCorrector",
					"producer:TauTauRestFrameSelector",
					"producer:DiLeptonQuantitiesProducer",
					"producer:DiJetQuantitiesProducer",
					"producer:SimpleEleTauFakeRateWeightProducer",
					"producer:SimpleMuTauFakeRateWeightProducer",
					"producer:TopPtReweightingProducer",
					"filter:MinimalPlotlevelFilter",
					#"producer:MVATestMethodsProducer",
					"producer:SvfitProducer",
					"producer:MELAProducer",
					"producer:TauTauTriggerWeightProducer",
					"producer:GenMatchedTauCPProducer",
					"producer:RefitVertexSelector",
					"producer:RecoTauCPProducer",
					"producer:PolarisationQuantitiesSvfitProducer",
					"producer:PolarisationQuantitiesSimpleFitProducer",
					#"producer:MadGraphReweightingProducer",
					#"producer:TauPolarisationTmvaReader",
					"producer:EventWeightProducer"]
		elif isSignal and is2015: 
			self["Processors"] = ["producer:HltProducer",
					"filter:HltFilter",
					"producer:MetSelector",
					"producer:TauCorrectionsProducer",
					"producer:ValidTausProducer",
					"filter:ValidTausFilter",
					"producer:TauTriggerMatchingProducer",
					"filter:MinTausCountFilter",
					"producer:ValidElectronsProducer",
					"producer:ValidMuonsProducer",
					"producer:ValidTTPairCandidatesProducer",
					"filter:ValidDiTauPairCandidatesFilter",
					"producer:HttValidLooseElectronsProducer",
					"producer:HttValidLooseMuonsProducer",
					"producer:Run2DecayChannelProducer",
					"producer:MvaMetSelector",
					"producer:TaggedJetCorrectionsProducer",
					"producer:ValidTaggedJetsProducer",
					"producer:ValidBTaggedJetsProducer",
					#"producer:TaggedJetUncertaintyShiftProducer",
					"producer:MetCorrector",
					"producer:MvaMetCorrector",
					"producer:TauTauRestFrameSelector",
					"producer:DiLeptonQuantitiesProducer",
					"producer:DiJetQuantitiesProducer",
					"producer:TopPtReweightingProducer",
					"filter:MinimalPlotlevelFilter",
					#"producer:MVATestMethodsProducer",
					"producer:SvfitProducer",
					"producer:MELAProducer",
					#"producer:SimpleFitProducer",
					"producer:EleTauFakeRateWeightProducer",
					"producer:GenMatchedTauCPProducer",
					#"producer:RefitVertexSelector",
					"producer:RecoTauCPProducer",
					"producer:PolarisationQuantitiesSvfitProducer",
					"producer:PolarisationQuantitiesSimpleFitProducer",
					"producer:MadGraphReweightingProducer",
					#"producer:TauPolarisationTmvaReader",
					"producer:EventWeightProducer"]
		elif isLFV and is2016:
			self["Processors"] = ["producer:HltProducer",
					"filter:HltFilter",
					"producer:MetSelector",
					"producer:TauCorrectionsProducer",
					"producer:ValidTausProducer",
					"filter:ValidTausFilter",
					"producer:TauTriggerMatchingProducer",
					"filter:MinTausCountFilter",
					"producer:ValidElectronsProducer",
					"producer:ValidMuonsProducer",
					"producer:ValidTTPairCandidatesProducer",
					"filter:ValidDiTauPairCandidatesFilter",
					"producer:HttValidLooseElectronsProducer",
					"producer:HttValidLooseMuonsProducer",
					"producer:Run2DecayChannelProducer",
					"producer:TaggedJetCorrectionsProducer",
					"producer:ValidTaggedJetsProducer",
					"producer:ValidBTaggedJetsProducer",
					"producer:TaggedJetUncertaintyShiftProducer",
					"producer:MetCorrector",
					"producer:TauTauRestFrameSelector",
					"producer:DiLeptonQuantitiesProducer",
					"producer:DiJetQuantitiesProducer",
					"producer:SimpleEleTauFakeRateWeightProducer",
					"producer:SimpleMuTauFakeRateWeightProducer",
					"producer:ZPtReweightProducer",
					#"filter:MinimalPlotlevelFilter",
					#"producer:MVATestMethodsProducer",
					#"producer:SvfitProducer",
					"producer:TauTauTriggerWeightProducer",
					"producer:GenMatchedTauCPProducer",
					"producer:RefitVertexSelector",
					"producer:RecoTauCPProducer",
					"producer:PolarisationQuantitiesSvfitProducer",
					"producer:PolarisationQuantitiesSimpleFitProducer",
					#"producer:TauPolarisationTmvaReader",
					"producer:EventWeightProducer"]
		
		else:
			self["Processors"] = ["producer:HltProducer",
					"filter:HltFilter",
					"producer:MetSelector",
					"producer:TauCorrectionsProducer",
					"producer:ValidTausProducer",
					"filter:ValidTausFilter",
					"producer:TauTriggerMatchingProducer",
					"filter:MinTausCountFilter",
					"producer:ValidElectronsProducer",
					"producer:ValidMuonsProducer",
					"producer:ValidTTPairCandidatesProducer",
					"filter:ValidDiTauPairCandidatesFilter",
					"producer:HttValidLooseElectronsProducer",
					"producer:HttValidLooseMuonsProducer",
					"producer:Run2DecayChannelProducer",
					"producer:TaggedJetCorrectionsProducer",
					"producer:ValidTaggedJetsProducer",
					"producer:ValidBTaggedJetsProducer",
					"producer:TaggedJetUncertaintyShiftProducer",
					"producer:MetCorrector",
					"producer:TauTauRestFrameSelector",
					"producer:DiLeptonQuantitiesProducer",
					"producer:DiJetQuantitiesProducer",
					"producer:SimpleEleTauFakeRateWeightProducer",
					"producer:SimpleMuTauFakeRateWeightProducer",
					"producer:TopPtReweightingProducer",
					"filter:MinimalPlotlevelFilter",
					#"producer:MVATestMethodsProducer",
					"producer:SvfitProducer",
					"producer:MELAProducer",
					"producer:SimpleFitProducer",
					"producer:TauTauTriggerWeightProducer",
					"producer:RefitVertexSelector",
					"producer:RecoTauCPProducer",
					"producer:PolarisationQuantitiesSvfitProducer",
					"producer:PolarisationQuantitiesSimpleFitProducer",
					#"producer:TauPolarisationTmvaReader",
					"producer:EventWeightProducer"]

		self["Processors"]=list(set(self["Processors"])) #removes dublicates from list by making it a set and then again a list, dont know if it should be a list or can be left as a set
		 



	def clear_config(self):
		self = self.base_copy







