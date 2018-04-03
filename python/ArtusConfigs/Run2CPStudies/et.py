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
import HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Includes.SingleTauQuantities as stq

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

import HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Run2CPStudies.Includes.settingsTauPolarisationMva as sTPMVA

class et_ArtusConfig(dict):

	def __init__(self):
		self.base_copy = copy.deepcopy(self)
		self.datasetsHelper = datasetsHelperTwopz.datasetsHelperTwopz("Kappa/Skimming/data/datasets.json") 

	def build_config(self, nickname): 
               #Maybe change this the arguments to process/year and DATA/MC
		"""
		"include" : [
			"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/ArtusConfigs/Run2Analysis/Includes/settingsLooseElectronID.json",
			"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/ArtusConfigs/Run2Analysis/Includes/settingsLooseMuonID.json",
			"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/ArtusConfigs/Run2Analysis/Includes/settingsElectronID.json",
			"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/ArtusConfigs/Run2Analysis/Includes/settingsVetoElectronID.json",
			"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/ArtusConfigs/Run2Analysis/Includes/settingsMuonID.json",
			"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/ArtusConfigs/Run2Analysis/Includes/settingsTauID.json",
			"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/ArtusConfigs/Run2Analysis/Includes/settingsJEC.json",
			"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/ArtusConfigs/Run2Analysis/Includes/settingsJECUncertaintySplit.json",
			"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/ArtusConfigs/Run2Analysis/Includes/settingsJetID.json",
			"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/ArtusConfigs/Run2Analysis/Includes/settingsBTaggedJetID.json",
			"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/ArtusConfigs/Run2Analysis/Includes/settingsSvfit.json",
			"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/ArtusConfigs/Run2Analysis/Includes/settingsMinimalPlotlevelFilter_et.json",
			"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/ArtusConfigs/Includes/settingsMVATestMethods.json",
			"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/ArtusConfigs/Run2Analysis/Includes/settingsTauES.json",
			"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/ArtusConfigs/Run2CPStudies/Includes/settingsTauPolarisationMva.json"
		],
		"""
		ElectronID_config = sEID.Electron_ID(nickname)
		ElectronID_config.looseElectron_ID(nickname) 		#append the config for loose electron ID because it is used
		ElectronID_config.vetoElectron_ID(nickname) 		
		self.update(ElectronID_config)	

		MuonID_config = sMID.Muon_ID(nickname)
		MuonID_config.looseMuon_ID(nickname) 		#append the config for loose Muon ID because it is used

		self.update(MuonID_config)	

		TauID_config = sTID.Tau_ID(nickname)			#here loose is not appended since loose tau ID is not used
		self.update(TauID_config)

		JEC_config = sJEC.JEC(nickname)  #Is allready in baseconfig, for now leave it in; possibly remove it 
		self.update(JEC_config)

		JECUncertaintySplit_config = sJECUS.JECUncertaintySplit(nickname)
		self.update(JECUncertaintySplit_config)

		JetID_config = sJID.Jet_ID(nickname)
		self.update(JetID_config)

		BTaggedJet_config = sBTJID.BTaggedJet_ID(nickname)
		self.update(BTaggedJet_config)

		Svfit_config = sSvfit.Svfit(nickname)
		self.update(Svfit_config)

		MinimalPlotlevelFilter_config = sMPlF.MinimalPlotlevelFilter()
		MinimalPlotlevelFilter_config.et()
		self.update(MinimalPlotlevelFilter_config)
		
		MVATestMethods_config = sMVATM.MVATestMethods()
		self.update(MVATestMethods_config)

		TauES_config = sTES.TauES(nickname)
		self.update(TauES_config)

		TauPolarisationMva_config = sTPMVA.TauPolarisationMva()
		self.update(TauPolarisationMva_config)





		self["TauPolarisationTmvaWeights"] = [
			"/afs/cern.ch/user/m/mfackeld/public/weights_tmva/training.weights.xml",
			"/afs/cern.ch/user/m/mfackeld/public/weights_sklearn/training_et.weights.xml"
		]
		self["Channel"] =  "ET"
		self["MinNElectrons"] =  1
		self["MinNTaus"] =  1
		self["HltPaths_comment"] =  "The first path must be the single lepton trigger. A corresponding Pt cut is implemented in the Run2DecayChannelProducer."

		self["NoHltFiltering"] = False  #else
		self["DiTauPairNoHLT" ] = False		

		self["ElectronLowerPtCuts"] = "24.0"  #default: !=2015
		self["DiTauPairLepton1LowerPtCuts"] = ["HLT_Ele25_eta2p1_WPTight_Gsf_v:26.0"]  #default: !=2015
		
		if re.search("(Fall15MiniAODv2|Run2015D|Embedding2015)", nickname):
			self["HltPaths"] = ["HLT_Ele23_WPLoose_Gsf"]
			self["ElectronLowerPtCuts"] = "24.0"           #2015
			self["DiTauPairLepton1LowerPtCuts"] = ["HLT_Ele23_WPLoose_Gsf_v:24.0"]  #2015

			self["DiTauPairHltPathsWithoutCommonMatchRequired"] = ["HLT_Ele23_WPLoose_Gsf_v"]


		elif re.search("Run2016|Spring16|Summer16", nickname):          #spring16 self["NoHltFiltering"] = True for cp config False for RUN2 set to false here
			self["HltPaths"] = ["HLT_Ele25_eta2p1_WPTight_Gsf"]
			self["DiTauPairHltPathsWithoutCommonMatchRequired"] = ["HLT_Ele25_eta2p1_WPTight_Gsf_v"]

		elif re.search("Embedding(2016|MC)", nickname):
			self["HltPaths"] =[""]
 			self["NoHltFiltering"] = True               #else: self["NoHltFiltering"] = True
			self["DiTauPairNoHLT" ] = False

			self["DiTauPairHltPathsWithoutCommonMatchRequired"] = ["HLT_Ele25_eta2p1_WPTight_Gsf_v"]



	
		self["TauID"] =  "TauIDRecommendation13TeV"
		self["TauUseOldDMs"] =  True
	
		self["ElectronUpperAbsEtaCuts"] = ["2.1"]
		self["TauLowerPtCuts"] = ["20.0"]
		self["TauUpperAbsEtaCuts"] = ["2.3"]
		self["TriggerObjectLowerPtCut"] = -1.0
		
		self["DiTauPairMinDeltaRCut"] = 0.5
		self["DiTauPairIsTauIsoMVA"] = True
		
		
		self["EventWeight"] =  "eventWeight"
		self["RooWorkspace"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/scaleFactorWeights/htt_scalefactors_sm_moriond_v2.root"
		self["RooWorkspaceWeightNames"] = [
			"0:triggerWeight",
			"0:idIsoWeight"
		]
		self["RooWorkspaceObjectNames"] = [
			"0:e_trgEle25eta2p1WPTight_desy_ratio",
			"0:e_idiso0p1_desy_ratio"

		]
		self["RooWorkspaceObjectArguments"] = [
			"0:e_pt,e_eta",
			"0:e_pt,e_eta"
		]



		if re.search("(Fall15MiniAODv2|Run2015D|Embedding2015)", nickname):
			self["TriggerEfficiencyData"] = [ "0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_Run2015_Electron_Ele23_fall15.root" ]
			self["TriggerEfficiencyMc"] = [ "0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_MC_Electron_Ele23_fall15.root"]

			self["IdentificationEfficiencyData"] = ["0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/identificationWeights/identificationEfficiency_Run2015_Electron_IdIso0p1_fall15.root"]
			self["IdentificationEfficiencyMc"] = ["0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/identificationWeights/identificationEfficiency_MC_Electron_IdIso0p1_fall15.root"]

			

		else:
			self["TriggerEfficiencyData"] = ["0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_Run2016_Electron_Ele25WPTight_eff.root" ]
			self["TriggerEfficiencyMc"] = ["0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_MC_Electron_Ele25WPTight_eff.root" ]
			
			self["IdentificationEfficiencyData"] = ["0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/identificationWeights/identificationEfficiency_Run2016_Electron_IdIso_IsoLt0p1_eff.root"]
			self["IdentificationEfficiencyMc"] = ["0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/identificationWeights/identificationEfficiency_MC_Electron_IdIso_IsoLt0p1_eff.root"]
		


		self["TriggerEfficiencyMode"] = "multiply_weights"
		self["IdentificationEfficiencyMode"] = "multiply_weights"
		self["EleTauFakeRateWeightFile"] = [
			"1:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/scaleFactorWeights/antiElectronDiscrMVA6FakeRateWeights.root"
		]
		self["TauTauRestFrameReco"] = "collinear_approximation"
		

		if re.search("(Fall15MiniAODv2|Run2015D|Embedding2015)", nickname):
			self["ElectronTriggerFilterNames"] = ["HLT_Ele23_WPLoose_Gsf_v:hltEle23WPLooseGsfTrackIsoFilter"]

		elif re.search("Run2016|Spring16|Summer16|Embedding(2016|MC)", nickname):
			self["ElectronTriggerFilterNames"] = ["HLT_Ele25_eta2p1_WPTight_Gsf_v:hltEle25erWPTightGsfTrackIsoFilter"]

	
		self["InvalidateNonMatchingElectrons"] = True
		self["InvalidateNonMatchingMuons"] = False
		self["InvalidateNonMatchingTaus"] = True
		self["InvalidateNonMatchingJets"] = False
		self["UseUWGenMatching"] = "true"
		self["DirectIso"] = True

		self["OSChargeLeptons"] = True

		self["AddGenMatchedParticles"] = True
		self["AddGenMatchedTaus"] = True
		self["AddGenMatchedTauJets"] = True
		self["BranchGenMatchedElectrons"] = True
		self["BranchGenMatchedTaus"] = True
		self["Consumers"] = [
			"KappaLambdaNtupleConsumer",
			"cutflow_histogram",
			"SvfitCacheConsumer",
			"#CutFlowTreeConsumer",
			"#KappaElectronsConsumer",
			"#KappaTausConsumer",
			"#KappaTaggedJetsConsumer",
			"#RunTimeConsumer",
			"#PrintEventsConsumer",
			"#PrintGenParticleDecayTreeConsumer"
		]

		self["Quantities"]=[]

		if re.search("Run2015", nickname):  					#the same as tt
			self["Quantities"] += r2q.fourVectorQuantities()
			self["Quantities"] += r2q.syncQuantities()
			self["Quantities"] += r2cpq.weightQuantities()
			self["Quantities"] += r2cpq.recoPolarisationQuantities() 	#until here
			self["Quantities"] += ["nVetoElectrons",
					"nLooseElectrons",
					"nLooseMuons",
					"nDiTauPairCandidates",
					"nAllDiTauPairCandidates"]

		elif re.search("(DY.?JetsToLL).*(?=(Spring16|Summer16))", nickname):	 #the same as tt
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
			self["Quantities"] += stq.SingleTauQuantities()
			self["Quantities"] += ["nVetoElectrons",
					"nLooseElectrons",
					"nLooseMuons",
					"nDiTauPairCandidates",
					"nAllDiTauPairCandidates",
					"tauSpinnerPolarisation"]

		elif re.search("(HToTauTau|H2JetsToTauTau|Higgs).*(?=(Spring16|Summer16))", nickname):
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
			self["Quantities"] += ["#tauPolarisationTMVA",
					"#tauPolarisationSKLEARN",
					"nVetoElectrons",
					"nLooseElectrons",
					"nLooseMuons",
					"nDiTauPairCandidates",
					"nAllDiTauPairCandidates"
					]

		elif re.search("^((?!(DY.?JetsToLL|HToTauTau|H2JetsToTauTau|Higgs)).)*Fall15", nickname):
			self["Quantities"] += r2q.fourVectorQuantities()
			self["Quantities"] += r2q.syncQuantities()
			self["Quantities"] += r2cpq.weightQuantities()
			self["Quantities"] += r2cpq.recoPolarisationQuantities()
			self["Quantities"] += ["nVetoElectrons",
					"nLooseElectrons",
					"nLooseMuons",
					"nDiTauPairCandidates",
					"nAllDiTauPairCandidates"]

		elif re.search("(DY.?JetsToLL).*(?=Fall15)", nickname):
			self["Quantities"] += r2q.fourVectorQuantities()
			self["Quantities"] += r2q.syncQuantities()
			self["Quantities"] += r2cpq.genQuantities()			
			self["Quantities"] += r2cpq.weightQuantities()
			self["Quantities"] += r2cpq.genMatchedCPQuantities()
			self["Quantities"] += r2cpq.recoPolarisationQuantities()
			self["Quantities"] += ["nVetoElectrons",
					"nLooseElectrons",
					"nLooseMuons",
					"nDiTauPairCandidates",
					"nAllDiTauPairCandidates",
					"tauSpinnerPolarisation"]

		elif re.search("(HToTauTau|H2JetsToTauTau|Higgs).*(?=Fall15)",nickname): 
			self["Quantities"] += r2q.fourVectorQuantities()
			self["Quantities"] += r2q.syncQuantities()
			self["Quantities"] += r2q.svfitSyncQuantities()
			self["Quantities"] += r2cpq.genQuantities()
			self["Quantities"] += r2cpq.genHiggsQuantities()
			self["Quantities"] += r2cpq.weightQuantities()
			self["Quantities"] += r2cpq.genMatchedCPQuantities()
			self["Quantities"] += r2cpq.recoCPQuantities()
			self["Quantities"] += r2cpq.melaQuantities()
			self["Quantities"] += ["#tauPolarisationTMVA",
					"#tauPolarisationSKLEARN",
					"nVetoElectrons",
					"nLooseElectrons",
					"nLooseMuons",
					"nDiTauPairCandidates",
					"nAllDiTauPairCandidates"]

		elif re.search("Embedding2016", nickname):
			self["Quantities"] += r2q.fourVectorQuantities()
			self["Quantities"] += r2q.syncQuantities()
			self["Quantities"] += r2q.splitJecUncertaintyQuantities()
			self["Quantities"] += r2cpq.genQuantities()
			self["Quantities"] += r2cpq.weightQuantities()			
			self["Quantities"] += r2cpq.recoPolarisationQuantities()
			self["Quantities"] += ["nLooseElectrons",
					"nLooseMuons",
					"nDiTauPairCandidates",
					"nAllDiTauPairCandidates",
					"tauSpinnerPolarisation"]

		elif re.search("(LFV).*(?=(Spring16|Summer16))", nickname):
			self["Quantities"] += r2q.fourVectorQuantities()
			self["Quantities"] += r2q.syncQuantities()
			self["Quantities"] += r2q.splitJecUncertaintyQuantities()
			self["Quantities"] += r2cpq.genQuantities()
			self["Quantities"] += r2cpq.weightQuantities()			
			self["Quantities"] += r2cpq.recoPolarisationQuantities()
			self["Quantities"] += ["nVetoElectrons",
					"nLooseElectrons",
					"nLooseMuons",
					"nDiTauPairCandidates",
					"nAllDiTauPairCandidates"]

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
			self["Quantities"] += ["nVetoElectrons",
					"nLooseElectrons",
					"nLooseMuons",
					"nDiTauPairCandidates",
					"nAllDiTauPairCandidates"]


		self["Quantities"]=list(set(self["Quantities"])) #removes dublicates from list by making it a set and then again a list, dont know if it should be a list or can be left as a set

		if re.search("(DY.?JetsToLL).*(?=(Spring16|Summer16))", nickname):
			self["Processors"] = [
					"producer:HltProducer",
					"filter:HltFilter",
					"producer:MetSelector",
					"producer:ValidElectronsProducer",
					"filter:ValidElectronsFilter",
					"producer:ElectronTriggerMatchingProducer",
					"filter:MinElectronsCountFilter",
					"producer:ValidMuonsProducer",
					"producer:TauCorrectionsProducer",
					"producer:ValidTausProducer",
					"filter:ValidTausFilter",
					"producer:TauTriggerMatchingProducer",
					"filter:MinTausCountFilter",
					"producer:ValidETPairCandidatesProducer",
					"filter:ValidDiTauPairCandidatesFilter",
					"producer:HttValidVetoElectronsProducer",
					"producer:HttValidLooseElectronsProducer",
					"producer:HttValidLooseMuonsProducer",
					"producer:Run2DecayChannelProducer",
					"producer:DiVetoElectronVetoProducer",
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
					"#producer:MVATestMethodsProducer",
					"producer:SvfitProducer",
					"producer:MELAProducer",
					"producer:SimpleFitProducer",
					"producer:RooWorkspaceWeightProducer",
					"producer:GenMatchedTauCPProducer",
					"producer:RefitVertexSelector",
					"producer:RecoTauCPProducer",
					"producer:PolarisationQuantitiesSvfitProducer",
					"producer:PolarisationQuantitiesSimpleFitProducer",
					"#producer:TauPolarisationTmvaReader",
					"producer:EventWeightProducer"
				]
		
		elif re.search("^((?!(DY.?JetsToLL|HToTauTau|H2JetsToTauTau|Higgs)).)*Fall15", nickname):
			self["Processors"] = [
					"producer:HltProducer",
					"filter:HltFilter",
					"producer:MetSelector",
					"producer:ValidElectronsProducer",
					"filter:ValidElectronsFilter",
					"producer:ElectronTriggerMatchingProducer",
					"filter:MinElectronsCountFilter",
					"producer:ValidMuonsProducer",
					"producer:TauCorrectionsProducer",
					"producer:ValidTausProducer",
					"filter:ValidTausFilter",
					"producer:TauTriggerMatchingProducer",
					"filter:MinTausCountFilter",
					"producer:ValidETPairCandidatesProducer",
					"filter:ValidDiTauPairCandidatesFilter",
					"producer:HttValidVetoElectronsProducer",
					"producer:HttValidLooseElectronsProducer",
					"producer:HttValidLooseMuonsProducer",
					"producer:Run2DecayChannelProducer",
					"producer:MvaMetSelector",
					"producer:DiVetoElectronVetoProducer",
					"producer:TaggedJetCorrectionsProducer",
					"producer:ValidTaggedJetsProducer",
					"producer:ValidBTaggedJetsProducer",
					"#producer:TaggedJetUncertaintyShiftProducer",
					"producer:MetCorrector",
					"producer:MvaMetCorrector",
					"producer:TauTauRestFrameSelector",
					"producer:DiLeptonQuantitiesProducer",
					"producer:DiJetQuantitiesProducer",
					"producer:TopPtReweightingProducer",
					"filter:MinimalPlotlevelFilter",
					"#producer:MVATestMethodsProducer",
					"#producer:SvfitProducer",
					"#producer:MELAProducer",
					"#producer:SimpleFitProducer",
					"producer:TriggerWeightProducer",
					"producer:IdentificationWeightProducer",
					"#producer:RefitVertexSelector",
					"producer:RecoTauCPProducer",
					"producer:PolarisationQuantitiesSvfitProducer",
					"producer:PolarisationQuantitiesSimpleFitProducer",
					"#producer:TauPolarisationTmvaReader",
					"producer:EventWeightProducer"
				]
		elif re.search("(DY.?JetsToLL).*(?=Fall15)", nickname):
			self["Processors"] = [
					"producer:HltProducer",
					"filter:HltFilter",
					"producer:MetSelector",
					"producer:ValidElectronsProducer",
					"filter:ValidElectronsFilter",
					"producer:ElectronTriggerMatchingProducer",
					"filter:MinElectronsCountFilter",
					"producer:ValidMuonsProducer",
					"producer:TauCorrectionsProducer",
					"producer:ValidTausProducer",
					"filter:ValidTausFilter",
					"producer:TauTriggerMatchingProducer",
					"filter:MinTausCountFilter",
					"producer:ValidETPairCandidatesProducer",
					"filter:ValidDiTauPairCandidatesFilter",
					"producer:HttValidVetoElectronsProducer",
					"producer:HttValidLooseElectronsProducer",
					"producer:HttValidLooseMuonsProducer",
					"producer:Run2DecayChannelProducer",
					"producer:MvaMetSelector",
					"producer:DiVetoElectronVetoProducer",
					"producer:TaggedJetCorrectionsProducer",
					"producer:ValidTaggedJetsProducer",
					"producer:ValidBTaggedJetsProducer",
					"#producer:TaggedJetUncertaintyShiftProducer",
					"producer:MetCorrector",
					"producer:MvaMetCorrector",
					"producer:TauTauRestFrameSelector",
					"producer:DiLeptonQuantitiesProducer",
					"producer:DiJetQuantitiesProducer",
					"producer:ZPtReweightProducer",
					"filter:MinimalPlotlevelFilter",
					"#producer:MVATestMethodsProducer",
					"#producer:SvfitProducer",
					"#producer:MELAProducer",
					"#producer:SimpleFitProducer",
					"producer:TriggerWeightProducer",
					"producer:IdentificationWeightProducer",
					"producer:EleTauFakeRateWeightProducer",
					"producer:GenMatchedTauCPProducer",
					"#producer:RefitVertexSelector",
					"producer:RecoTauCPProducer",
					"producer:PolarisationQuantitiesSvfitProducer",
					"producer:PolarisationQuantitiesSimpleFitProducer",
					"#producer:TauPolarisationTmvaReader",
					"producer:EventWeightProducer"
				]

		elif re.search("Run2016", nickname):
			self["Processors"] = [
					"producer:HltProducer",
					"filter:HltFilter",
					"producer:MetSelector",
					"producer:ValidElectronsProducer",
					"filter:ValidElectronsFilter",
					"producer:ElectronTriggerMatchingProducer",
					"filter:MinElectronsCountFilter",
					"producer:ValidMuonsProducer",
					"producer:ValidTausProducer",
					"filter:ValidTausFilter",
					"producer:TauTriggerMatchingProducer",
					"filter:MinTausCountFilter",
					"producer:ValidETPairCandidatesProducer",
					"filter:ValidDiTauPairCandidatesFilter",
					"producer:HttValidVetoElectronsProducer",
					"producer:HttValidLooseElectronsProducer",
					"producer:HttValidLooseMuonsProducer",
					"producer:Run2DecayChannelProducer",
					"producer:DiVetoElectronVetoProducer",
					"producer:TaggedJetCorrectionsProducer",
					"producer:ValidTaggedJetsProducer",
					"producer:ValidBTaggedJetsProducer",
					"producer:TaggedJetUncertaintyShiftProducer",
					"producer:TauTauRestFrameSelector",
					"producer:DiLeptonQuantitiesProducer",
					"producer:DiJetQuantitiesProducer",
					"filter:MinimalPlotlevelFilter",
					"#producer:MVATestMethodsProducer",
					"producer:SvfitProducer",
					"producer:MELAProducer",
					"producer:SimpleFitProducer",
					"producer:RefitVertexSelector",
					"producer:RecoTauCPProducer",
					"producer:PolarisationQuantitiesSvfitProducer",
					"producer:PolarisationQuantitiesSimpleFitProducer",
					"#producer:TauPolarisationTmvaReader",
					"producer:EventWeightProducer"
				]
		elif re.search("Run2015", nickname):
			self["Processors"] = [
					"producer:HltProducer",
					"filter:HltFilter",
					"producer:MetSelector",
					"producer:ValidElectronsProducer",
					"filter:ValidElectronsFilter",
					"producer:ElectronTriggerMatchingProducer",
					"filter:MinElectronsCountFilter",
					"producer:ValidMuonsProducer",
					"producer:ValidTausProducer",
					"filter:ValidTausFilter",
					"producer:TauTriggerMatchingProducer",
					"filter:MinTausCountFilter",
					"producer:ValidETPairCandidatesProducer",
					"filter:ValidDiTauPairCandidatesFilter",
					"producer:HttValidVetoElectronsProducer",
					"producer:HttValidLooseElectronsProducer",
					"producer:HttValidLooseMuonsProducer",
					"producer:Run2DecayChannelProducer",
					"producer:MvaMetSelector",
					"producer:DiVetoElectronVetoProducer",
					"producer:TaggedJetCorrectionsProducer",
					"producer:ValidTaggedJetsProducer",
					"producer:ValidBTaggedJetsProducer",
					"#producer:TaggedJetUncertaintyShiftProducer",
					"producer:TauTauRestFrameSelector",
					"producer:DiLeptonQuantitiesProducer",
					"producer:DiJetQuantitiesProducer",
					"filter:MinimalPlotlevelFilter",
					"#producer:MVATestMethodsProducer",
					"#producer:SvfitProducer",
					"#producer:MELAProducer",
					"#producer:SimpleFitProducer",
					"#producer:RefitVertexSelector",
					"producer:RecoTauCPProducer",
					"producer:PolarisationQuantitiesSvfitProducer",
					"producer:PolarisationQuantitiesSimpleFitProducer",
					"#producer:TauPolarisationTmvaReader",
					"producer:EventWeightProducer"
				]


		elif re.search("(HToTauTau|H2JetsToTauTau|Higgs).*(?=(Spring16|Summer16))", nickname):
			self["Processors"] = [
					"producer:HltProducer",
					"filter:HltFilter",
					"producer:MetSelector",
					"producer:ValidElectronsProducer",
					"filter:ValidElectronsFilter",
					"producer:ElectronTriggerMatchingProducer",
					"filter:MinElectronsCountFilter",
					"producer:ValidMuonsProducer",
					"producer:TauCorrectionsProducer",
					"producer:ValidTausProducer",
					"filter:ValidTausFilter",
					"producer:TauTriggerMatchingProducer",
					"filter:MinTausCountFilter",
					"producer:ValidETPairCandidatesProducer",
					"filter:ValidDiTauPairCandidatesFilter",
					"producer:HttValidVetoElectronsProducer",
					"producer:HttValidLooseElectronsProducer",
					"producer:HttValidLooseMuonsProducer",
					"producer:Run2DecayChannelProducer",
					"producer:DiVetoElectronVetoProducer",
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
					"#producer:MVATestMethodsProducer",
					"producer:SvfitProducer",
					"producer:MELAProducer",
					"producer:RooWorkspaceWeightProducer",
					"producer:GenMatchedTauCPProducer",
					"producer:RefitVertexSelector",
					"producer:RecoTauCPProducer",
					"producer:PolarisationQuantitiesSvfitProducer",
					"producer:PolarisationQuantitiesSimpleFitProducer",
					"#producer:TauPolarisationTmvaReader",
					"#producer:MadGraphReweightingProducer",
					"producer:EventWeightProducer"
				]

		elif re.search("(HToTauTau|H2JetsToTauTau|Higgs).*(?=Fall15)",nickname):
			self["Processors"] = [
					"producer:HltProducer",
					"filter:HltFilter",
					"producer:MetSelector",
					"producer:ValidElectronsProducer",
					"filter:ValidElectronsFilter",
					"producer:ElectronTriggerMatchingProducer",
					"filter:MinElectronsCountFilter",
					"producer:ValidMuonsProducer",
					"producer:TauCorrectionsProducer",
					"producer:ValidTausProducer",
					"filter:ValidTausFilter",
					"producer:TauTriggerMatchingProducer",
					"filter:MinTausCountFilter",
					"producer:ValidETPairCandidatesProducer",
					"filter:ValidDiTauPairCandidatesFilter",
					"producer:HttValidVetoElectronsProducer",
					"producer:HttValidLooseElectronsProducer",
					"producer:HttValidLooseMuonsProducer",
					"producer:Run2DecayChannelProducer",
					"producer:MvaMetSelector",
					"producer:DiVetoElectronVetoProducer",
					"producer:TaggedJetCorrectionsProducer",
					"producer:ValidTaggedJetsProducer",
					"producer:ValidBTaggedJetsProducer",
					"#producer:TaggedJetUncertaintyShiftProducer",
					"producer:MetCorrector",
					"producer:MvaMetCorrector",
					"producer:TauTauRestFrameSelector",
					"producer:DiLeptonQuantitiesProducer",
					"producer:DiJetQuantitiesProducer",
					"producer:TopPtReweightingProducer",
					"filter:MinimalPlotlevelFilter",
					"#producer:MVATestMethodsProducer",
					"producer:SvfitProducer",
					"producer:MELAProducer",
					"#producer:SimpleFitProducer",
					"producer:TriggerWeightProducer",
					"producer:IdentificationWeightProducer",
					"producer:EleTauFakeRateWeightProducer",
					"producer:GenMatchedTauCPProducer",
					"#producer:RefitVertexSelector",
					"producer:RecoTauCPProducer",
					"producer:PolarisationQuantitiesSvfitProducer",
					"producer:PolarisationQuantitiesSimpleFitProducer",
					"#producer:TauPolarisationTmvaReader",
					"producer:MadGraphReweightingProducer",
					"producer:EventWeightProducer"
				]

		elif re.search("(LFV).*(?=(Spring16|Summer16))", nickname):
			 self["Processors"] = [
					"producer:HltProducer",
					"filter:HltFilter",
					"producer:MetSelector",
					"producer:ValidElectronsProducer",
					"filter:ValidElectronsFilter",
					"producer:ElectronTriggerMatchingProducer",
					"filter:MinElectronsCountFilter",
					"producer:ValidMuonsProducer",
					"producer:TauCorrectionsProducer",
					"producer:ValidTausProducer",
					"filter:ValidTausFilter",
					"producer:TauTriggerMatchingProducer",
					"filter:MinTausCountFilter",
					"producer:ValidETPairCandidatesProducer",
					"filter:ValidDiTauPairCandidatesFilter",
					"producer:HttValidVetoElectronsProducer",
					"producer:HttValidLooseElectronsProducer",
					"producer:HttValidLooseMuonsProducer",
					"producer:Run2DecayChannelProducer",
					"producer:DiVetoElectronVetoProducer",
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
					"#filter:MinimalPlotlevelFilter",
					"#producer:MVATestMethodsProducer",
					"#producer:SvfitProducer",
					"producer:RooWorkspaceWeightProducer",
					"producer:GenMatchedTauCPProducer",
					"producer:RefitVertexSelector",
					"producer:RecoTauCPProducer",
					"producer:PolarisationQuantitiesSvfitProducer",
					"producer:PolarisationQuantitiesSimpleFitProducer",
					"#producer:TauPolarisationTmvaReader",
					"producer:EventWeightProducer"
				]

		else:
			self["Processors"] = [
					"producer:HltProducer",
					"filter:HltFilter",
					"producer:MetSelector",
					"producer:ValidElectronsProducer",
					"filter:ValidElectronsFilter",
					"producer:ElectronTriggerMatchingProducer",
					"filter:MinElectronsCountFilter",
					"producer:ValidMuonsProducer",
					"producer:TauCorrectionsProducer",
					"producer:ValidTausProducer",
					"filter:ValidTausFilter",
					"producer:TauTriggerMatchingProducer",
					"filter:MinTausCountFilter",
					"producer:ValidETPairCandidatesProducer",
					"filter:ValidDiTauPairCandidatesFilter",
					"producer:HttValidVetoElectronsProducer",
					"producer:HttValidLooseElectronsProducer",
					"producer:HttValidLooseMuonsProducer",
					"producer:Run2DecayChannelProducer",
					"producer:DiVetoElectronVetoProducer",
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
					"#producer:MVATestMethodsProducer",
					"producer:SvfitProducer",
					"producer:MELAProducer",
					"producer:SimpleFitProducer",
					"producer:RooWorkspaceWeightProducer",
					"producer:RefitVertexSelector",
					"producer:RecoTauCPProducer",
					"producer:PolarisationQuantitiesSvfitProducer",
					"producer:PolarisationQuantitiesSimpleFitProducer",
					"#producer:TauPolarisationTmvaReader",
					"producer:EventWeightProducer"
				]


		








		
