# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import re
import copy
import os

from HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Run2CPStudies.quantities import Quantities
from HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Includes.processorOrdering import ProcessorsOrdered

import HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Run2Analysis.Includes.settingsElectronID as sEID
import HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Run2Analysis.Includes.settingsMuonID as sMID
import HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Run2Analysis.Includes.settingsTauID as sTID
import HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Run2Analysis.Includes.settingsJetID as sJID
import HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Run2Analysis.Includes.settingsBTaggedJetID as sBTJID
import HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Run2Analysis.Includes.settingsSvfit as sSvfit
import HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Run2Analysis.Includes.settingsMinimalPlotlevelFilter as sMPlF
import HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Run2Analysis.Includes.settingsJEC as sJEC
import HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Run2Analysis.Includes.settingsJECUncertaintySplit as sJECUS

import HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Includes.settingsMVATestMethods as sMVATM

from HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Run2Analysis.Includes.idAndTriggerSF import IdAndTriggerSF
import Kappa.Skimming.datasetsHelperTwopz as datasetsHelperTwopz

class mm_ArtusConfig(dict):

	def __init__(self):
		pass

	def addProcessors(self, nickname, legacy):
		if re.search("(DY.?JetsToLL|EWKZ2Jets).*(?=(Spring16|Summer16))",nickname):
			self["Processors"] = [
				"producer:HltProducer",
				"filter:HltFilter",
				"producer:MetSelector",
				"producer:MuonCorrectionsProducer",
				"producer:ValidMuonsProducer",
				"filter:ValidMuonsFilter",
				"producer:MuonTriggerMatchingProducer",
				"filter:MinMuonsCountFilter",
				"producer:ValidElectronsProducer",
				"producer:ValidTausProducer",
				"producer:ValidMMPairCandidatesProducer",
				"filter:ValidDiTauPairCandidatesFilter",
				"producer:HttValidLooseElectronsProducer",
				"producer:HttValidLooseMuonsProducer",
				"producer:Run2DecayChannelProducer",
				"producer:TaggedJetCorrectionsProducer",
				"producer:ValidTaggedJetsProducer",
				"producer:ValidBTaggedJetsProducer",
				"producer:TaggedJetUncertaintyShiftProducer",
				"producer:MetCorrector",
				"producer:DiLeptonQuantitiesProducer",
				"producer:TauTauRestFrameSelector",
				"producer:DiJetQuantitiesProducer",
				"producer:ZPtReweightProducer",
				"filter:MinimalPlotlevelFilter"
			]
			self["Processors"] += ["#producer:MVATestMethodsProducer"]
			self["Processors"] += ["#producer:SvfitProducer"]
			self["Processors"] += ["producer:MELAProducer"]
			self["Processors"] += ["producer:MELAM125Producer"]
			self["Processors"] += ["#producer:TriggerWeightProducer"]
			self["Processors"] += ["producer:IdentificationWeightProducer"]
			self["Processors"] += ["#producer:RooWorkspaceWeightProducer"]
			self["Processors"] += ["producer:MuMuTriggerWeightProducer"]
			self["Processors"] += ["producer:GenMatchedTauCPProducer"]
			self["Processors"] += ["producer:RefitVertexSelector"]
			self["Processors"] += ["producer:RecoTauCPProducer"]
			self["Processors"] += ["producer:EventWeightProducer"]

		elif re.search("^((?!(DY.?JetsToLL|EWKZ2Jets)).)*Fall15", nickname):
			self["Processors"] = [
				"producer:HltProducer",
				"filter:HltFilter",
				"producer:MetSelector",
				"producer:MuonCorrectionsProducer",
				"producer:ValidMuonsProducer",
				"filter:ValidMuonsFilter",
				"producer:MuonTriggerMatchingProducer",
				"filter:MinMuonsCountFilter",
				"producer:ValidElectronsProducer",
				"producer:ValidTausProducer",
				"producer:ValidMMPairCandidatesProducer",
				"filter:ValidDiTauPairCandidatesFilter",
				"producer:HttValidLooseElectronsProducer",
				"producer:HttValidLooseMuonsProducer",
				"producer:Run2DecayChannelProducer",
				"producer:MvaMetSelector",
				"producer:TaggedJetCorrectionsProducer",
				"producer:ValidTaggedJetsProducer",
				"producer:ValidBTaggedJetsProducer",
				"#producer:TaggedJetUncertaintyShiftProducer",
				"producer:MetCorrector",
				"producer:MvaMetCorrector",
				"producer:TauTauRestFrameSelector",
				"producer:DiLeptonQuantitiesProducer",
				"producer:DiJetQuantitiesProducer",
				"filter:MinimalPlotlevelFilter"
			]
			self["Processors"] += ["#producer:MVATestMethodsProducer"]
			self["Processors"] += ["#producer:SvfitProducer"]
			self["Processors"] += ["producer:MELAProducer"]
			self["Processors"] += ["producer:MELAM125Producer"]
			self["Processors"] += ["producer:RefitVertexSelector"]
			self["Processors"] += ["producer:RecoTauCPProducer"]
			self["Processors"] += ["producer:TriggerWeightProducer"]
			self["Processors"] += ["producer:IdentificationWeightProducer"]
			self["Processors"] += ["producer:EventWeightProducer"]

		elif re.search("(DY.?JetsToLL|EWKZ2Jets).*(?=Fall15)", nickname):
			self["Processors"] = [
				"producer:HltProducer",
				"filter:HltFilter",
				"producer:MetSelector",
				"producer:MuonCorrectionsProducer",
				"producer:ValidMuonsProducer",
				"filter:ValidMuonsFilter",
				"producer:MuonTriggerMatchingProducer",
				"filter:MinMuonsCountFilter",
				"producer:ValidElectronsProducer",
				"producer:ValidTausProducer",
				"producer:ValidMMPairCandidatesProducer",
				"filter:ValidDiTauPairCandidatesFilter",
				"producer:HttValidLooseElectronsProducer",
				"producer:HttValidLooseMuonsProducer",
				"producer:Run2DecayChannelProducer",
				"producer:MvaMetSelector",
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
				"filter:MinimalPlotlevelFilter"
			]
			self["Processors"] += ["#producer:MVATestMethodsProducer"]
			self["Processors"] += ["#producer:SvfitProducer"]
			self["Processors"] += ["producer:TriggerWeightProducer"]
			self["Processors"] += ["producer:IdentificationWeightProducer"]
			self["Processors"] += ["producer:EventWeightProducer"]

		elif re.search("Run2016", nickname):
			self["Processors"] = [
				"producer:HltProducer",
				"filter:HltFilter",
				"producer:MetSelector",
				"producer:MuonCorrectionsProducer",
				"producer:ValidMuonsProducer",
				"filter:ValidMuonsFilter",
				"producer:MuonTriggerMatchingProducer",
				"filter:MinMuonsCountFilter",
				"producer:ValidElectronsProducer",
				"producer:ValidTausProducer",
				"producer:ValidMMPairCandidatesProducer",
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
				"filter:MinimalPlotlevelFilter"
			]
			self["Processors"] += ["#producer:MVATestMethodsProducer"]
			self["Processors"] += ["#producer:SvfitProducer"]
			self["Processors"] += ["producer:MELAProducer"]
			self["Processors"] += ["producer:MELAM125Producer"]

			self["Processors"] += ["producer:RefitVertexSelector"]
			self["Processors"] += ["producer:RecoTauCPProducer"]
			self["Processors"] += ["producer:EventWeightProducer"]

		elif re.search("Run2015", nickname):
			self["Processors"] = [
				"producer:HltProducer",
				"filter:HltFilter",
				"producer:MetSelector",
				"producer:MuonCorrectionsProducer",
				"producer:ValidMuonsProducer",
				"filter:ValidMuonsFilter",
				"producer:MuonTriggerMatchingProducer",
				"filter:MinMuonsCountFilter",
				"producer:ValidElectronsProducer",
				"producer:ValidTausProducer",
				"producer:ValidMMPairCandidatesProducer",
				"filter:ValidDiTauPairCandidatesFilter",
				"producer:HttValidLooseElectronsProducer",
				"producer:HttValidLooseMuonsProducer",
				"producer:Run2DecayChannelProducer",
				"producer:MvaMetSelector",
				"producer:TaggedJetCorrectionsProducer",
				"producer:ValidTaggedJetsProducer",
				"producer:ValidBTaggedJetsProducer",
				"#producer:TaggedJetUncertaintyShiftProducer",
				"producer:TauTauRestFrameSelector",
				"producer:DiLeptonQuantitiesProducer",
				"producer:DiJetQuantitiesProducer",
				"filter:MinimalPlotlevelFilter"
			]
			self["Processors"] += ["#producer:MVATestMethodsProducer"]
			self["Processors"] += ["#producer:SvfitProducer"]
			self["Processors"] += ["producer:EventWeightProducer"]

		elif re.search("(LFV).*(?=(Spring16|Summer16))", nickname):
			self["Processors"] = [
				"producer:HltProducer",
				"filter:HltFilter",
				"producer:MetSelector",
				"producer:MuonCorrectionsProducer",
				"producer:ValidMuonsProducer",
				"filter:ValidMuonsFilter",
				"producer:MuonTriggerMatchingProducer",
				"filter:MinMuonsCountFilter",
				"producer:ValidElectronsProducer",
				"producer:ValidTausProducer",
				"producer:ValidMMPairCandidatesProducer",
				"filter:ValidDiTauPairCandidatesFilter",
				"producer:HttValidLooseElectronsProducer",
				"producer:HttValidLooseMuonsProducer",
				"producer:Run2DecayChannelProducer",
				"producer:TaggedJetCorrectionsProducer",
				"producer:ValidTaggedJetsProducer",
				"producer:ValidBTaggedJetsProducer",
				"producer:TaggedJetUncertaintyShiftProducer",
				"producer:MetCorrector",
				"producer:DiLeptonQuantitiesProducer",
				"producer:TauTauRestFrameSelector",
				"producer:DiJetQuantitiesProducer",
				"producer:ZPtReweightProducer",
				"#filter:MinimalPlotlevelFilter"
			]
			self["Processors"] += ["#producer:MVATestMethodsProducer"]
			self["Processors"] += ["#producer:SvfitProducer"]
			self["Processors"] += ["#producer:TriggerWeightProducer"]
			self["Processors"] += ["producer:IdentificationWeightProducer"]
			self["Processors"] += ["#producer:RooWorkspaceWeightProducer"]
			self["Processors"] += ["producer:MuMuTriggerWeightProducer"]
			self["Processors"] += ["producer:EventWeightProducer"]

		elif re.search("Run2017|Summer17|Fall17|Embedding2017", nickname):
			self["Processors"] = [
				"producer:HltProducer",
				"producer:MetSelector",
				"producer:MetSelectorPuppi",
				"producer:ValidMuonsProducer",
				"filter:ValidMuonsFilter",
				"producer:MuonTriggerMatchingProducer",
				"filter:MinMuonsCountFilter",
				"producer:ValidElectronsProducer",
				"producer:ValidTausProducer",
				"producer:NewValidMMPairCandidatesProducer",
				"filter:ValidDiTauPairCandidatesFilter",
				"producer:HttValidLooseElectronsProducer",
				"producer:HttValidLooseMuonsProducer",
				"producer:Run2DecayChannelProducer",
				"producer:TaggedJetCorrectionsProducer",
				"producer:ValidTaggedJetsProducer",
				"producer:ValidBTaggedJetsProducer",
				"producer:TauTauRestFrameSelector",
				"producer:DiLeptonQuantitiesProducer",
				"producer:DiJetQuantitiesProducer",
				"producer:TopPtReweightingProducer",
				"filter:MinimalPlotlevelFilter"
			]

			if re.search("Summer17|Fall17", nickname):
				self["Processors"] += ["producer:MetCorrector"]
				self["Processors"] += ["producer:PuppiMetCorrector"]
				self["Processors"] += ["producer:GenMatchedTauCPProducer"]
			self["Processors"] += ["producer:GroupedJetUncertaintyShiftProducer"]
			self["Processors"] += ["producer:SvfitProducer"]
			self["Processors"] += ["producer:LegacyWeightProducer"]
			self["Processors"] += ["producer:RefitVertexSelector"]
			self["Processors"] += ["producer:RecoTauCPProducer"]
			self["Processors"] += ["producer:EventWeightProducer"]
			self["Processors"] += ["producer:CPInitialStateQuantitiesProducer"] #only DoLhenpNLO for IC samples
			self["Processors"] += ["producer:MetFilterProducer"]


		else:
			self["Processors"] = [
				"producer:HltProducer",
				"filter:HltFilter",
				"producer:MetSelector",
				"producer:MuonCorrectionsProducer",
				"producer:ValidMuonsProducer",
				"filter:ValidMuonsFilter",
				"producer:MuonTriggerMatchingProducer",
				"filter:MinMuonsCountFilter",
				"producer:ValidElectronsProducer",
				"producer:ValidTausProducer",
				"producer:ValidMMPairCandidatesProducer",
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
				"producer:TopPtReweightingProducer",
				"filter:MinimalPlotlevelFilter"
			]
			self["Processors"] += ["#producer:MVATestMethodsProducer"]
			self["Processors"] += ["#producer:SvfitProducer"]
			self["Processors"] += ["producer:MELAProducer"]
			self["Processors"] += ["producer:MELAM125Producer"]
			self["Processors"] += ["#producer:TriggerWeightProducer"]
			self["Processors"] += ["producer:IdentificationWeightProducer"]
			self["Processors"] += ["#producer:RooWorkspaceWeightProducer"]
			self["Processors"] += ["producer:MuMuTriggerWeightProducer"]
			self["Processors"] += ["producer:RefitVertexSelector"]
			self["Processors"] += ["producer:RecoTauCPProducer"]
			self["Processors"] += ["producer:EventWeightProducer"]

			self["Processors"] = list(set(self["Processors"]))
			processorOrderingkey = ProcessorsOrdered(channel = self["Channel"])
			ordered_processors = processorOrderingkey.order_processors(self["Processors"])

			self["Processors"] = copy.deepcopy(ordered_processors)

	def build_config(self, nickname, *args, **kwargs):                #Maybe change this the arguments to process/year and DATA/MC
		datasetsHelper = datasetsHelperTwopz.datasetsHelperTwopz(os.path.expandvars("$CMSSW_BASE/src/Kappa/Skimming/data/datasets.json"))

		isLegacy = kwargs.get("legacy", False)
		isEmbedded = datasetsHelper.isEmbedded(nickname)
		isData = datasetsHelper.isData(nickname) and (not isEmbedded)

		ElectronID_config = sEID.Electron_ID(nickname)
		ElectronID_config.looseElectron_ID(nickname) 		#append the config for loose electron ID because it is used
		self.update(ElectronID_config)

		MuonID_config = sMID.Muon_ID(nickname)
		MuonID_config.looseMuon_ID(nickname) 		#append the config for loose Muon ID because it is used
		# MuonID_config.vetoMuon_ID(nickname)
		self.update(MuonID_config)

		TauID_config = sTID.Tau_ID(nickname)			#here loose is not appended since loose tau ID is not used
		self.update(TauID_config)

		JEC_config = sJEC.JEC(nickname)  #Is allready in baseconfig, for now leave it in; possibly remove it
		self.update(JEC_config)

		# JECUncertaintySplit_config = sJECUS.JECUncertaintySplit(nickname)
		# self.update(JECUncertaintySplit_config)

		JetID_config = sJID.Jet_ID(nickname)
		self.update(JetID_config)

		BTaggedJet_config = sBTJID.BTaggedJet_ID(nickname)
		self.update(BTaggedJet_config)

		Svfit_config = sSvfit.Svfit(nickname)
		self.update(Svfit_config)

		mplf = sMPlF.MinimalPlotlevelFilter(nickname=nickname, channel="MM", eTauFakeRate=False)
		self.update(mplf.minPlotLevelDict)

		MVATestMethods_config = sMVATM.MVATestMethods()
		self.update(MVATestMethods_config)

		self["Channel"] = "MM"
		self["MinNMuons"] = 2
		self["HltPaths_comment"] = "The first path must be the single lepton trigger. A corresponding Pt cut is implemented in the Run2DecayChannelProducer."

		self["HltPaths"] = [
			"HLT_IsoMu24",
			"HLT_IsoTkMu24"
		]
		self["NoHltFiltering"] = False

		self["DiTauPairLepton1LowerPtCuts"] = [
			"HLT_IsoMu24_v:25.0",
			"HLT_IsoTkMu24_v:25.0"
		]

		if re.search("(Fall15MiniAODv2|Run2015D|Embedding2015)", nickname):
			self["HltPaths"] =[
				"HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ",
				"HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ"
			]
			self["DiTauPairLepton1LowerPtCuts"] = [
					"HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_v:20.0",
					"HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ_v:20.0"
				]

			self["DiTauPairLepton2LowerPtCuts"] =  [
					"HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_v:10.0",
					"HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ_v:10.0"
				]

		elif re.search("Embedding(2016|MC)", nickname):
			self["HltPaths"] = [""]
			self["NoHltFiltering"] = True


		self["TauID"] = "TauIDRecommendation13TeV"
		self["TauUseOldDMs"] = False
		self["MuonLowerPtCuts"] = [
			"10.0"
		]
		self["MuonUpperAbsEtaCuts"] = [
			"2.4"
		]
		self["DiTauPairMinDeltaRCut"] = 0.3
		self["DeltaRTriggerMatchingMuons"] = 0.1

		if re.search("Run2016|Spring16|Summer16", nickname):
			self["DiTauPairHltPathsWithoutCommonMatchRequired"] = [
				"HLT_IsoMu24_v",
				"HLT_IsoTkMu24_v"
			]

		self["DiTauPairNoHLT"] = False

		self["EventWeight"] = "eventWeight"
		# self["RooWorkspace"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/scaleFactorWeights/htt_scalefactors_sm_moriond_v2.root"
		# self["RooWorkspaceWeightNames"] = [
		# 	"0:idIsoWeight",
		# 	"1:idIsoWeight"
		# ]
		# self["RooWorkspaceObjectNames"] = [
		# 	"0:m_idiso0p15_desy_ratio",
		# 	"1:m_idiso0p15_desy_ratio"
		# ]
		# self["RooWorkspaceObjectArguments"] = [
		# 	"0:m_pt,m_eta",
		# 	"1:m_pt,m_eta"
		# ]
		# self["MuMuTriggerWeightWorkspace"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/scaleFactorWeights/htt_scalefactors_sm_moriond_v2.root"
		# self["MuMuTriggerWeightWorkspaceWeightNames"] = [
		# 	"0:triggerWeight",
		# 	"1:triggerWeight"
		# ]
		# self["MuMuTriggerWeightWorkspaceObjectNames"] = [
		# 	"0:m_trgIsoMu24orTkIsoMu24_desy_ratio",
		# 	"1:m_trgIsoMu24orTkIsoMu24_desy_ratio"
		# ]
		# self["MuMuTriggerWeightWorkspaceObjectArguments"] = [
		# 	"0:m_pt,m_eta",
		# 	"1:m_pt,m_eta"
		# ]

		self.update(IdAndTriggerSF(nickname, channel="MM", dcach=False))

		self["TriggerEfficiencyMode"] = "correlate_triggers"

		self["IdentificationEfficiencyMode"] = "multiply_weights"
		self["TauTauRestFrameReco"] = "collinear_approximation"

		if re.search("Run2016|Spring16|Summer16", nickname):
			self["MuonTriggerFilterNames"] = [
				"HLT_IsoMu24_v:hltL3crIsoL1sMu22L1f0L2f10QL3f24QL3trkIsoFiltered0p09",
				"HLT_IsoTkMu24_v:hltL3fL1sMu22L1f0Tkf24QL3trkIsoFiltered0p09"
			]

		if re.search("(Fall15MiniAODv2|Run2015D|Embedding2015)", nickname):
			self["MuonTriggerFilterNames"] = [
				"HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_v:hltDiMuonGlb17Glb8RelTrkIsoFiltered0p4DzFiltered0p2",
				"HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ_v:hltDiMuonGlb17Trk8RelTrkIsoFiltered0p4DzFiltered0p2"
			]

		self["InvalidateNonMatchingElectrons"] = False
		self["InvalidateNonMatchingMuons"] = True
		self["InvalidateNonMatchingTaus"] = True
		self["InvalidateNonMatchingJets"] = False
		self["DirectIso"] = True

		self["AddGenMatchedParticles"] = True
		self["BranchGenMatchedMuons"] = True
		self["Consumers"] = [
			"KappaLambdaNtupleConsumer",
			"cutflow_histogram",
			"#PrintHltConsumer",
			"#SvfitCacheConsumer",
			"#CutFlowTreeConsumer",
			"#KappaMuonsConsumer",
			"#KappaTausConsumer",
			"#KappaTaggedJetsConsumer",
			"#RunTimeConsumer",
			"#PrintEventsConsumer"
		]

		self["OSChargeLeptons"] = True
		if re.search("(Fall15MiniAODv2|Run2015)", nickname):
			self["MuonEnergyCorrection"] = "rochcorr2015"
			self["MuonRochesterCorrectionsFile"] = "$CMSSW_BASE/src/Artus/KappaAnalysis/data/rochcorr/RoccoR_13tev_2015.txt"

		else:
			self["MuonEnergyCorrection"] = "rochcorr2016"
			self["MuonRochesterCorrectionsFile"] = "$CMSSW_BASE/src/Artus/KappaAnalysis/data/rochcorr2016"

		quantities_set = Quantities()
		quantities_set.build_quantities(nickname, channel = self["Channel"])
		self["Quantities"] = list(quantities_set.quantities)

		self.addProcessors(nickname, isLegacy)
