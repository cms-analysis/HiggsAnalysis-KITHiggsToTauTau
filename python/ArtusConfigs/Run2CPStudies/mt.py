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
import HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Run2Analysis.Includes.settingsTauES as sTES
import HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Run2Analysis.Includes.settingsJEC as sJEC
import HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Run2Analysis.Includes.settingsJECUncertaintySplit as sJECUS

import HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Includes.settingsMVATestMethods as sMVATM
import HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Run2CPStudies.Includes.settingsTauPolarisationMva as sTPMVA

from HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Run2Analysis.Includes.idAndTriggerSF import IdAndTriggerSF
import Kappa.Skimming.datasetsHelperTwopz as datasetsHelperTwopz


class mt_ArtusConfig(dict):

	def __init__(self):
		pass

	def addProcessors(self, nickname):
		self["Processors"] = [
				"producer:HltProducer",
				#"filter:HltFilter",
				"producer:MetSelector",
				################## special for each channel in et mt tt em.
				"producer:ValidMuonsProducer",
				"filter:ValidMuonsFilter",
				"producer:MuonTriggerMatchingProducer",
				"filter:MinMuonsCountFilter",
				"producer:ValidElectronsProducer",
				"producer:ValidTausProducer",
				"filter:ValidTausFilter",
				"producer:TauTriggerMatchingProducer",
				"filter:MinTausCountFilter",
				"filter:ValidDiTauPairCandidatesFilter",
				"producer:HttValidVetoMuonsProducer",
				"producer:HttValidLooseElectronsProducer",
				"producer:HttValidLooseMuonsProducer",
				##################
				"producer:Run2DecayChannelProducer",
				"producer:DiVetoMuonVetoProducer",
				"producer:ValidTaggedJetsProducer",
				"producer:ValidBTaggedJetsProducer",
				"producer:TauTauRestFrameSelector",
				"producer:DiLeptonQuantitiesProducer",
				"producer:DiJetQuantitiesProducer",

				]

		if re.search("(Spring16|Summer16|Run2016|Run2017|Summer17|Fall17|Embedding(2016|2017))", nickname):
			self["Processors"] += ["producer:CPInitialStateQuantitiesProducer"] #only DoLhenpNLO for IC samples
			self["Processors"] += ["producer:RefitVertexSelector"]
			self["Processors"] += ["producer:RecoTauCPProducer"]
			self["Processors"] += ["producer:PolarisationQuantitiesSvfitProducer"]
			self["Processors"] += ["producer:PolarisationQuantitiesSvfitM91Producer"]
			self["Processors"] += ["producer:PolarisationQuantitiesSimpleFitProducer"]
			if re.search("(Run2017|Summer17|Fall17|Embedding2017)", nickname):
				self["Processors"] += ["producer:NewValidMTPairCandidatesProducer"]
			else:
				self["Processors"] += ["producer:ValidMTPairCandidatesProducer"]
			self["Processors"] += ["producer:GroupedJetUncertaintyShiftProducer"]
			#if re.search("(Spring16|Summer16|Run2016|Embedding2016)",nickname):
			self["Processors"] += ["producer:TaggedJetCorrectionsProducer"] #already applied in kappa for 2017 i believe TODO in next skim

			if re.search("(Run2016|Run2017|Embedding(2016|2017))", nickname):
				#self["Processors"] += ["producer:MVATestMethodsProducer"]
				self["Processors"] += ["producer:SimpleFitProducer"]

				self["Processors"] += ["filter:MinimalPlotlevelFilter"]
				self["Processors"] += ["producer:SvfitProducer"]
				#self["Processors"] += ["producer:SvfitM91Producer"]
				#self["Processors"] += ["producer:SvfitM125Producer"]

				self["Processors"] += ["producer:MELAProducer"]
				#self["Processors"] += ["producer:MELAM125Producer"]

				self["Processors"] += ["producer:JetToTauFakesProducer"] #TODO check if only needed in data
				if re.search("Run2016", nickname):
					self["Processors"] += ["producer:GenMatchedPolarisationQuantitiesProducer"]
				#self["Processors"] += ["producer:TauPolarisationTmvaReader"]

				if re.search("Embedding(2016|2017)", nickname):
					self["Processors"] += ["producer:GenMatchedPolarisationQuantitiesProducer"]
					#self["Processors"] += ["producer:RooWorkspaceWeightProducer"]
					self["Processors"] += ["producer:EmbeddingWeightProducer"]
					#self["Processors"] += ["producer:MuTauTriggerWeightProducer"]
					self["Processors"] += ["producer:TauCorrectionsProducer"]

			else:
				self["Processors"] += [
						"producer:SimpleEleTauFakeRateWeightProducer",
						"producer:SimpleMuTauFakeRateWeightProducer"
						]
				self["Processors"] += ["producer:TauCorrectionsProducer"]
				self["Processors"] += ["producer:MetCorrector"]
				self["Processors"] += ["producer:GenMatchedTauCPProducer"]
				self["Processors"] += ["producer:GenMatchedPolarisationQuantitiesProducer"]
				if re.search("Summer17|Fall17", nickname):
					self["Processors"] += ["producer:PrefiringWeightProducer"]
					self["Processors"] += ["producer:TauTriggerEfficiency2017Producer"]
					#"producer:TriggerWeightProducer"
					self["Processors"] += ["producer:LeptonTauTrigger2017WeightProducer"] #is a rooworkspace

					#self["Processors"] += ["producer:IdentificationWeightProducer"]
					self["Processors"] += ["producer:RooWorkspaceWeightProducer"]
				else:
					self["Processors"] += ["producer:RooWorkspaceWeightProducer"]
					self["Processors"] += ["producer:MuTauTriggerWeightProducer"] #is a rooworkspace file

				if re.search("(LFV).*(?=(Spring16|Summer16))", nickname):
					self["Processors"] += [
						"producer:ZPtReweightProducer"
						#"filter:MinimalPlotlevelFilter"
					]
					self["Processors"] += ["producer:GenMatchedTauCPProducer"]
					self["Processors"] += ["producer:LFVJetCorrection2016Producer"]

				else:
					self["Processors"] += ["filter:MinimalPlotlevelFilter"]
					self["Processors"] += ["producer:SvfitProducer"]
					#self["Processors"] += ["producer:SvfitM91Producer"]
					#self["Processors"] += ["producer:SvfitM125Producer"]

					self["Processors"] += ["producer:MELAProducer"]
					#self["Processors"] += ["producer:MELAM125Producer"]

					if re.search("(DY.?JetsToLL).*(?=(Spring16|Summer16|Summer17|Fall17))", nickname):
						self["Processors"] += ["producer:JetToTauFakesProducer"]
						#if re.search("Summer17|Fall17", nickname) == None:


						self["Processors"] += ["producer:SimpleFitProducer"]
						if re.search("Summer17|Fall17", nickname) == None: #I dont want to do polarisation
							self["Processors"] += ["producer:GenMatchedTauCPProducer"]
							self["Processors"] += ["producer:GenMatchedPolarisationQuantitiesProducer"]
							self["Processors"] += ["producer:ZPtReweightProducer"]

						#self["Processors"] += ["producer:TauPolarisationTmvaReader"]

					elif re.search("(HToTauTau|H2JetsToTauTau|Higgs|JJHiggs).*(?=(Spring16|Summer16|Summer17|Fall17))", nickname):
						self["Processors"] += [
							"producer:TopPtReweightingProducer" #FIXME only ttbar?
						]
						if re.search("amcatnlo",nickname):
							self["DoLhenpNLO"] = True	#NEEDED for stitching
						#TODO lhe npo weight added
						#self["Processors"] += ["producer:MVATestMethodsProducer"]
						if re.search("Summer17|Fall17", nickname) == None: #I dont want to do polarisation
							self["Processors"] += ["producer:GenMatchedTauCPProducer"]
							self["Processors"] += ["producer:GenMatchedPolarisationQuantitiesProducer"] # I put this on in to create the same config as json but i dont think it is needed
						#self["Processors"] += ["producer:TauPolarisationTmvaReader"]
						#self["Processors"] += ["producer:MadGraphReweightingProducer"]
					else:
						self["Processors"] += ["producer:JetToTauFakesProducer"] #TODO check if only needed in data
						#if re.search("Summer17|Fall17", nickname) == None:
						self["Processors"] += [	"producer:TopPtReweightingProducer"]  #FIXME only ttbar?
						#self["Processors"] += ["producer:MVATestMethodsProducer"]
						self["Processors"] += ["producer:SimpleFitProducer"] #FIXME Needed?
						if re.search("Summer17|Fall17", nickname) == None: #I dont want to do polarisation
							self["Processors"] += ["producer:GenMatchedPolarisationQuantitiesProducer"]

						#self["Processors"] += ["producer:TauPolarisationTmvaReader"]

		elif re.search("(Fall15|Run2015)", nickname):
			#self["Processors"] += ["producer:RefitVertexSelector"]
			self["Processors"] += ["producer:ValidMTPairCandidatesProducer"]
			self["Processors"] += ["producer:RecoTauCPProducer"]
			self["Processors"] += ["producer:PolarisationQuantitiesSvfitProducer"]
			self["Processors"] += ["producer:PolarisationQuantitiesSvfitM91Producer"]
			self["Processors"] += ["producer:PolarisationQuantitiesSimpleFitProducer"]
			self["Processors"] += ["filter:MinimalPlotlevelFilter"]
			self["Processors"] += ["producer:TaggedJetCorrectionsProducer", "producer:MvaMetSelector"]


			if re.search("Run2015", nickname):
				#self["Processors"] += ["producer:SimpleFitProducer"]
				self["Processors"] += ["producer:GenMatchedPolarisationQuantitiesProducer"]

				#self["Processors"] += ["producer:SvfitProducer"]
				#self["Processors"] += ["producer:SvfitM91Producer"]
				#self["Processors"] += ["producer:SvfitM125Producer"]

				#self["Processors"] += ["producer:MELAProducer"]
				#self["Processors"] += ["producer:MELAM125Producer"]

			else:
				self["Processors"] += ["producer:MvaMetCorrector"]
				self["Processors"] += ["producer:MetCorrector"]
				self["Processors"] += ["producer:TauCorrectionsProducer"]
				self["Processors"] += ["producer:TriggerWeightProducer",
					"producer:IdentificationWeightProducer",
					"producer:EleTauFakeRateWeightProducer"
				]

				if re.search("(DY.?JetsToLL).*(?=Fall15)", nickname):

					self["Processors"] += ["producer:ZPtReweightProducer"]
					#self["Processors"] += ["producer:SimpleFitProducer"]
					self["Processors"] += ["producer:GenMatchedTauCPProducer"]
					self["Processors"] += ["producer:GenMatchedPolarisationQuantitiesProducer"]

				elif re.search("(HToTauTau|H2JetsToTauTau|Higgs).*(?=Fall15)",nickname):
					self["Processors"] += ["producer:SvfitProducer"]
					self["Processors"] += ["producer:SvfitM91Producer"]
					self["Processors"] += ["producer:SvfitM125Producer"]

					self["Processors"] += ["producer:MELAProducer"]
					self["Processors"] += ["producer:MELAM125Producer"]



				elif re.search("^((?!(DY.?JetsToLL|HToTauTau|H2JetsToTauTau|Higgs)).)*Fall15", nickname):
					self["Processors"] += ["producer:SvfitProducer"]
					self["Processors"] += ["producer:SvfitM91Producer"]
					self["Processors"] += ["producer:SvfitM125Producer"]

					self["Processors"] += ["producer:MELAProducer"]
					self["Processors"] += ["producer:MELAM125Producer"]

		self["Processors"] += ["producer:EventWeightProducer"]
		self["Processors"] = list(set(self["Processors"]))
		processorOrderingkey = ProcessorsOrdered(channel = self["Channel"])
		ordered_processors = processorOrderingkey.order_processors(self["Processors"])

		self["Processors"] = copy.deepcopy(ordered_processors)

	def build_config(self, nickname, *args, **kwargs):                #Maybe change this the arguments to process/year and DATA/MC
		"""
		"include" : [
			"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/ArtusConfigs/Run2Analysis/Includes/settingsLooseElectronID.json",
			"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/ArtusConfigs/Run2Analysis/Includes/settingsLooseMuonID.json",
			"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/ArtusConfigs/Run2Analysis/Includes/settingsElectronID.json",
			"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/ArtusConfigs/Run2Analysis/Includes/settingsVetoMuonID.json",
			"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/ArtusConfigs/Run2Analysis/Includes/settingsMuonID.json",
			"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/ArtusConfigs/Run2Analysis/Includes/settingsTauID.json",
			"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/ArtusConfigs/Run2Analysis/Includes/settingsJEC.json",
			"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/ArtusConfigs/Run2Analysis/Includes/settingsJECUncertaintySplit.json",
			"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/ArtusConfigs/Run2Analysis/Includes/settingsJetID.json",
			"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/ArtusConfigs/Run2Analysis/Includes/settingsBTaggedJetID.json",
			"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/ArtusConfigs/Run2Analysis/Includes/settingsSvfit.json",
			"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/ArtusConfigs/Run2Analysis/Includes/settingsMinimalPlotlevelFilter_mt.json",
			"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/ArtusConfigs/Includes/settingsMVATestMethods.json",
			"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/ArtusConfigs/Run2Analysis/Includes/settingsTauES.json",
			"$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/ArtusConfigs/Run2CPStudies/Includes/settingsTauPolarisationMva.json"
		],
		"""

		datasetsHelper = datasetsHelperTwopz.datasetsHelperTwopz(os.path.expandvars("$CMSSW_BASE/src/Kappa/Skimming/data/datasets.json"))

		# define frequently used conditions
		isEmbedded = datasetsHelper.isEmbedded(nickname)
		isData = datasetsHelper.isData(nickname) and (not isEmbedded)

		ElectronID_config = sEID.Electron_ID(nickname)
		ElectronID_config.looseElectron_ID(nickname) 		#append the config for loose electron ID because it is used
		self.update(ElectronID_config)

		MuonID_config = sMID.Muon_ID(nickname)
		MuonID_config.looseMuon_ID(nickname) 		#append the config for loose Muon ID because it is used
		MuonID_config.vetoMuon_ID(nickname)
		self.update(MuonID_config)

		TauID_config = sTID.Tau_ID(nickname)			#here loose is not appended since loose tau ID is not used
		self.update(TauID_config)

		JEC_config = sJEC.JEC(nickname)  #Is allready in baseconfig, for now leave it in; possibly remove it
		self.update(JEC_config)

		#JECUncertaintySplit_config = sJECUS.JECUncertaintySplit(nickname)
		#self.update(JECUncertaintySplit_config)

		JetID_config = sJID.Jet_ID(nickname)
		self.update(JetID_config)

		BTaggedJet_config = sBTJID.BTaggedJet_ID(nickname)
		self.update(BTaggedJet_config)

		Svfit_config = sSvfit.Svfit(nickname)
		self.update(Svfit_config)
		if re.search("VBFHToTauTauM125_RunIIFall17MiniAODv2_PU2017_13TeV_MINIAOD_powheg-pythia8",nickname):
			mplf = sMPlF.MinimalPlotlevelFilter(nickname=nickname, channel="MT", eTauFakeRate=False, sync=True)
		else:
			mplf = sMPlF.MinimalPlotlevelFilter(nickname=nickname, channel="MT", eTauFakeRate=False, sync=False)
		self.update(mplf.minPlotLevelDict)


		MVATestMethods_config = sMVATM.MVATestMethods()
		self.update(MVATestMethods_config)

		TauES_config = sTES.TauES(nickname)
		self.update(TauES_config)

		TauPolarisationMva_config = sTPMVA.TauPolarisationMva()
		self.update(TauPolarisationMva_config)
		
		self.update(IdAndTriggerSF(nickname, channel="MT", dcach=False))

		self["TauPolarisationTmvaWeights"] = [
			"/afs/cern.ch/user/m/mfackeld/public/weights_tmva/training.weights.xml",
			"/afs/cern.ch/user/m/mfackeld/public/weights_sklearn/training_mt.weights.xml"
		]
		self["Channel"] = "MT"
		self["MinNMuons"] = 1
		self["MinNTaus"] = 1
		self["HltPaths_comment"] = "The first path must be the single lepton trigger. A corresponding Pt cut is implemented in the Run2DecayChannelProducer."
		self["NoHltFiltering"] = False
		self["DiTauPairNoHLT"] = False

		if re.search("(Fall15MiniAODv2|Run2015D|Embedding2015)", nickname):
			self["HltPaths"] = ["HLT_IsoMu18"]
			self["NoHltFiltering"] = False
			self["DiTauPairNoHLT"] = False

		elif re.search("Run2016|Spring16|Summer16|Embedding(2016|MC)", nickname):
			self["HltPaths"] = [
				"HLT_IsoMu22",
				"HLT_IsoTkMu22",
				"HLT_IsoMu22_eta2p1",
				"HLT_IsoTkMu22_eta2p1",
				"HLT_IsoMu19_eta2p1_LooseIsoPFTau20",
				"HLT_IsoMu19_eta2p1_LooseIsoPFTau20_SingleL1"
			]
			self["NoHltFiltering"] = True if isEmbedded else False
			self["DiTauPairNoHLT"] = False

		# elif re.search("Embedding(2016|MC)", nickname):
		# 	self["HltPaths"] = []
		# 	self["NoHltFiltering"] = True
		# 	self["DiTauPairNoHLT"] = True

		self["TauID"] = "TauIDRecommendation13TeV"
		self["TauUseOldDMs"] = True

		self["MuonLowerPtCuts"] = ["20.0"]
		if re.search("(Fall15MiniAODv2|Run2015D|Embedding2015)", nickname):
			self["MuonLowerPtCuts"] = ["19.0"]

		self["MuonUpperAbsEtaCuts"] = ["2.1"]
		self["TauLowerPtCuts"] = ["20.0"]
		self["TauUpperAbsEtaCuts"] = ["2.3"]
		self["TriggerObjectLowerPtCut"] = -1.0
		self["DiTauPairMinDeltaRCut"] = 0.5
		self["DiTauPairIsTauIsoMVA"] = True

		if re.search("(Fall15MiniAODv2|Run2015D|Embedding2015)", nickname):
			self["DiTauPairLepton1LowerPtCuts"] = ["HLT_IsoMu18_v:19.0"]
			self["DiTauPairHltPathsWithoutCommonMatchRequired"] = ["HLT_IsoMu18_v"]

		elif re.search("Run2016|Spring16|Summer16|Embedding(2016|MC)", nickname):
			self["DiTauPairLepton1LowerPtCuts"] = [
				"HLT_IsoMu24_v:25.0",
				"HLT_IsoTkMu24_v:25.0"
			]
			self["DiTauPairHltPathsWithoutCommonMatchRequired"] = [
				"HLT_IsoMu22_v",
				"HLT_IsoTkMu22_v",
				"HLT_IsoMu22_eta2p1_v",
				"HLT_IsoTkMu22_eta2p1_v",
				"HLT_IsoMu19_eta2p1_LooseIsoPFTau20_v",
				"HLT_IsoMu19_eta2p1_LooseIsoPFTau20_SingleL1_v"
			]

		else:                                         #I believe "Run2016|Spring16|Summer16|Embedding(2016|MC)" is everything else but for safety i did it here, 2017 not included yet
			self["DiTauPairLepton1LowerPtCuts"] = [
				"HLT_IsoMu24_v:25.0",
				"HLT_IsoTkMu24_v:25.0"
			]


		self["DiTauPairHLTLast"] = False
		if re.search("Spring16", nickname): self["DiTauPairHLTLast"] = True

		if re.search("Run2016|Spring16|Summer16|Embedding(2016|MC)", nickname):
			self["DiTauPairHLTLast"] = True
			self["HLTBranchNames"] = [
				"trg_singlemuon:HLT_IsoMu22_v",
				"trg_singlemuon:HLT_IsoTkMu22_v",
				"trg_singlemuon:HLT_IsoMu22_eta2p1_v",
				"trg_singlemuon:HLT_IsoTkMu22_eta2p1_v",
				"trg_mutaucross:HLT_IsoMu19_eta2p1_LooseIsoPFTau20_v",
				"trg_mutaucross:HLT_IsoMu19_eta2p1_LooseIsoPFTau20_SingleL1_v"
			]

			self["MuonTriggerFilterNames"] = [
				"HLT_IsoMu22_v:hltL3crIsoL1sMu20L1f0L2f10QL3f22QL3trkIsoFiltered0p09",
				"HLT_IsoTkMu22_v:hltL3fL1sMu20L1f0Tkf22QL3trkIsoFiltered0p09",
				"HLT_IsoMu22_eta2p1_v:hltL3crIsoL1sSingleMu20erL1f0L2f10QL3f22QL3trkIsoFiltered0p09",
				"HLT_IsoTkMu22_eta2p1_v:hltL3fL1sMu20erL1f0Tkf22QL3trkIsoFiltered0p09",
				"HLT_IsoMu19_eta2p1_LooseIsoPFTau20_v:hltL3crIsoL1sMu18erTauJet20erL1f0L2f10QL3f19QL3trkIsoFiltered0p09",
				"HLT_IsoMu19_eta2p1_LooseIsoPFTau20_v:hltOverlapFilterIsoMu19LooseIsoPFTau20",
				"HLT_IsoMu19_eta2p1_LooseIsoPFTau20_SingleL1_v:hltL3crIsoL1sSingleMu18erIorSingleMu20erL1f0L2f10QL3f19QL3trkIsoFiltered0p09",
				"HLT_IsoMu19_eta2p1_LooseIsoPFTau20_SingleL1_v:hltOverlapFilterSingleIsoMu19LooseIsoPFTau20"
			]

			self["TauTriggerFilterNames"] = [
				"HLT_IsoMu19_eta2p1_LooseIsoPFTau20_v:hltL1sMu18erTau20er",
				#"HLT_IsoMu19_eta2p1_LooseIsoPFTau20_v:hltOverlapFilterIsoMu19LooseIsoPFTau20",
				"HLT_IsoMu19_eta2p1_LooseIsoPFTau20_SingleL1_v:hltL1sSingleMu18erIorSingleMu20er",
				#"HLT_IsoMu19_eta2p1_LooseIsoPFTau20_SingleL1_v:hltPFTau20TrackLooseIsoAgainstMuon",
				#"HLT_IsoMu19_eta2p1_LooseIsoPFTau20_SingleL1_v:hltOverlapFilterSingleIsoMu19LooseIsoPFTau20"
			]


		elif re.search("(Fall15MiniAODv2|Run2015D|Embedding2015)", nickname):
			self["MuonTriggerFilterNames"] = ["HLT_IsoMu18_v:hltL3crIsoL1sMu16L1f0L2f10QL3f18QL3trkIsoFiltered0p09"]


		elif re.search("Run2017|Summer17|Fall17|Embedding2017", nickname):
			self["HltPaths"] = [
				"HLT_IsoMu24",
				"HLT_IsoMu27",
				"HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1"
			]
			self["MuonLowerPtCuts"] = [21]
			self["TauLowerPtCuts"] = ["20.0"]
			self["HLTBranchNames"] = [
			      "trg_singlemuon_24:HLT_IsoMu24_v",
			      "trg_singlemuon_27:HLT_IsoMu27_v",
			      "trg_crossmuon_mu20tau27:HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1_v"
			]

			self["DiTauPairLepton1LowerPtCuts"] = [
				"HLT_IsoMu24_v:25.0",
				"HLT_IsoMu27_v:28.0",
				"HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1_v:21.0"
			]
			self["DiTauPairLepton2LowerPtCuts"] = ["HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1_v:32.0"]

			self["DiTauPairHltPathsWithoutCommonMatchRequired"] = [
				"HLT_IsoMu24_v",
				"HLT_IsoMu27_v",
				"HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1_v"
			]
			self["MuonTriggerFilterNames"] = [
				"HLT_IsoMu24_v:hltL3crIsoL1sSingleMu22L1f0L2f10QL3f24QL3trkIsoFiltered0p07",
				"HLT_IsoMu27_v:hltL3crIsoL1sMu22Or25L1f0L2f10QL3f27QL3trkIsoFiltered0p07",
				"HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1:hltL3crIsoL1sMu18erTau24erIorMu20erTau24erL1f0L2f10QL3f20QL3trkIsoFiltered0p07",
				"HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1:hltOverlapFilterIsoMu20LooseChargedIsoPFTau27L1Seeded"
			]
			if isEmbedded:
				self["TauTriggerFilterNames"] = [
					"HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1:hltL1sMu18erTau24erIorMu20erTau24er"
				]
			else:
				self["TauTriggerFilterNames"] = [
					"HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1:hltSelectedPFTau27LooseChargedIsolationAgainstMuonL1HLTMatched",
					"HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1:hltOverlapFilterIsoMu20LooseChargedIsoPFTau27L1Seeded",
				]


			self["CheckLepton1TriggerMatch"] = [
				"trg_singlemuon_24",
				"trg_singlemuon_27",
				"trg_crossmuon_mu20tau27",
				"trg_crossele_ele24tau30",
				"trg_doubletau_35_tightiso_tightid",
				"trg_doubletau_40_mediso_tightid",
				"trg_doubletau_40_tightiso",
				"trg_muonelectron_mu12ele23",
				"trg_muonelectron_mu23ele12",
				"trg_muonelectron_mu8ele23"
			  ]
			self["CheckLepton2TriggerMatch"] = [
				"trg_singletau_trailing",
				"trg_crossmuon_mu20tau27",
				"trg_crossele_ele24tau30",
				"trg_doubletau_35_tightiso_tightid",
				"trg_doubletau_40_mediso_tightid",
				"trg_doubletau_40_tightiso",
				"trg_muonelectron_mu12ele23",
				"trg_muonelectron_mu23ele12",
				"trg_muonelectron_mu8ele23"
				]

		self["EventWeight"] = "eventWeight"

		if re.search("(Run2017|Summer17|Fall17|Embedding2017)", nickname):
			if isEmbedded:
				self["SaveEmbeddingWeightAsOptionalOnly"] = "true"
				self["EmbeddingWeightWorkspace"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/scaleFactorWeights/htt_scalefactors_v17_5.root"
				self["EmbeddingWeightWorkspaceWeightNames"] = [
					"0:triggerWeight_doublemu",
					"0:idweight_doublemu",
					"1:idweight_doublemu",
					"0:isoweight",
					"0:idweight",
					"0:triggerWeight_mu",
					"0:triggerWeight_mutaucross",
					"1:triggerWeight_mutaucross"
				]
				self["EmbeddingWeightWorkspaceObjectNames"] = [
					"0:m_sel_trg_ratio",
					"0:m_sel_idEmb_ratio",
					"1:m_sel_idEmb_ratio",
					"0:m_iso_binned_embed_kit_ratio",
					"0:m_id_embed_kit_ratio",
					"0:m_trg24_27_embed_kit_ratio",
					"0:m_trg_MuTau_Mu20Leg_kit_ratio_embed",
					"1:mt_emb_LooseChargedIsoPFTau27_kit_ratio"
				]
				self["EmbeddingWeightWorkspaceObjectArguments"] = [
					"0:gt1_pt,gt1_eta,gt2_pt,gt2_eta",
					"0:gt_pt,gt_eta",
					"1:gt_pt,gt_eta",
					"0:m_pt,m_eta,m_iso",
					"0:m_pt,m_eta",
					"0:m_pt,m_eta",
					"0:m_pt",
					"1:t_pt"
				]
			else:
				self["RooWorkspace"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/scaleFactorWeights/htt_scalefactors_2017_v2.root"
				self["RooWorkspaceWeightNames"] = [
					#"0:crossTriggerMCEfficiencyWeight",
					#"0:crossTriggerDataEfficiencyWeight",
					#"0:singleTriggerMCEfficiencyWeight",
					#"0:singleTriggerDataEfficiencyWeight",
					#"0:singleTriggerMCEfficiencyWeightKIT",
					#"0:singleTriggerDataEfficiencyWeightKIT",

					"0:idIsoWeight",
					#"0:idWeight",
					"0:trackWeight"
					]
				self["RooWorkspaceObjectNames"] = [
					#"0:m_trg_MuTau_Mu20Leg_desy_mc",
					#"0:m_trg_MuTau_Mu20Leg_desy_data",
					#"0:m_trg_SingleMu_Mu24ORMu27_desy_mc",
					#"0:m_trg_SingleMu_Mu24ORMu27_desy_data",
					#"0:m_trg24or27_mc",
					#"0:m_trg24or27_data",

					"0:m_idiso_binned_ratio",
					#"0:m_id_ratio",
					"0:m_trk_ratio"
					]
				self["RooWorkspaceObjectArguments"] = [
					#"0:m_pt,m_eta",
					#"0:m_pt,m_eta",
					#"0:m_pt,m_eta",
					#"0:m_pt,m_eta",
					#"0:m_pt,m_eta",
					#"0:m_pt,m_eta",

					"0:m_pt,m_eta",
					#"0:m_pt,m_eta",
					"0:m_eta"
					]
				if re.search("HToTauTau", nickname):
					self["RooWorkspaceWeightNames"] += ["0:quarkmassWeight", "0:quarkmassUpWeight", "0:quarkmassDownWeight"]
					self["RooWorkspaceObjectNames"] += ["0:ggH_quarkmass_corr", "0:ggH_quarkmass_corr_up", "0:ggH_quarkmass_corr_down"]
					self["RooWorkspaceObjectArguments"] += ["0:HpT", "0:HpT", "0:HpT"] #gen Higgs pt
				if re.search("(DY.?JetsToLL).*(?=(Summer17|Fall17))", nickname):
					self["RooWorkspaceWeightNames"] += ["0:zPtReweightWeight"]
					self["RooWorkspaceObjectNames"] += ["0:zpt_weight_nom"]
					self["RooWorkspaceObjectArguments"] += ["0:z_gen_pt"]

				if self["TriggerEfficiencyMode"] == "cross_triggers":
					self["LeptonTauTrigger2017WeightWorkspace"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/scaleFactorWeights/htt_scalefactors_2017_v2.root"
					self["LeptonTauTrigger2017WeightWorkspaceWeightNames"] = [
						"0:m_triggerEffSingle_mc",
						"0:m_triggerEffCross_mc",
						"0:m_triggerEffSingle_data",
						"0:m_triggerEffCross_data"
					]
					self["LeptonTauTrigger2017WeightWorkspaceObjectNames"] = [
						"0:m_trg_binned_mc",
						"0:m_trg20_mc",
						"0:m_trg_binned_data",
						"0:m_trg20_data"

					]
					self["LeptonTauTrigger2017WeightWorkspaceObjectArguments"] = [
						"0:m_pt,m_eta,m_iso",
						"0:m_pt,m_eta",
						"0:m_pt,m_eta,m_iso",
						"0:m_pt,m_eta"
					]
				elif self["TriggerEfficiencyMode"] == "no_overlap_triggers":
					self["LeptonTauTrigger2017WeightWorkspace"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/scaleFactorWeights/htt_scalefactors_2017_v3.root"
					self["SaveLeptonTauTrigger2017WeightAsOptionalOnly"] = "true"
					self["LeptonTauTrigger2017WeightWorkspaceWeightNames"] = [
						"0:triggerWeight_mutaucross",
						"0:triggerWeight_mu",
					]
					self["LeptonTauTrigger2017WeightWorkspaceObjectNames"] = [
						"0:m_trg20_ratio",
						"0:m_trg24_27_kit_ratio",
					]
					self["LeptonTauTrigger2017WeightWorkspaceObjectArguments"] = [
						"0:m_pt,m_eta",
						"0:m_pt,m_eta",
					]

		elif re.search("(Spring16|Summer16|Run2016|Embedding2016)", nickname):
			self["SaveRooWorkspaceTriggerWeightAsOptionalOnly"] = "true"
			if isEmbedded:
				self["EmbeddingWeightWorkspace"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/scaleFactorWeights/htt_scalefactors_v16_11_embedded.root"
				self["EmbeddingWeightWorkspaceWeightNames"] = [
					"0:triggerWeight_doublemu",
					"0:isoweight",
					"0:idweight",
					"0:triggerWeight_singleMu",
					"1:MuTau_TauLeg_EmbeddedEfficiencyWeight",
					"1:MuTau_TauLeg_DataEfficiencyWeight"
				]
				self["EmbeddingWeightWorkspaceObjectNames"] = [
					"0:m_sel_trg_ratio",
					"0:m_iso_ratio",
					"0:m_id_ratio",
					"0:m_trg_ratio",

					"1:t_TightIso_mt_emb",
					"1:t_genuine_TightIso_mt_data,t_fake_TightIso_mt_data"
				]
				self["EmbeddingWeightWorkspaceObjectArguments"] = [
					"0:gt1_pt,gt1_eta,gt2_pt,gt2_eta",
					"0:m_pt,m_eta",
					"0:m_pt,m_eta",
					"0:m_pt,m_eta",

					"1:t_pt,t_eta",
					"1:t_pt,t_eta"
				]
			else:
				self["RooWorkspace"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/scaleFactorWeights/htt_scalefactors_sm_moriond_v2.root"
				self["RooWorkspaceWeightNames"] = [
					"0:triggerWeight_singleMu",
					"0:idIsoWeight"
				]
				self["RooWorkspaceObjectNames"] = [
					"0:m_trgMu22OR_eta2p1_desy_ratio",
					"0:m_idiso0p15_desy_ratio"
				]
				self["RooWorkspaceObjectArguments"] = [
					"0:m_pt,m_eta",
					"0:m_pt,m_eta"
				]
				self["SaveMuTauTriggerWeightAsOptionalOnly"] = "true"
				self["MuTauTriggerWeightWorkspace"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/scaleFactorWeights/htt_scalefactors_sm_moriond_v2.root"
				self["MuTauTriggerWeightWorkspaceWeightNames"] = [
					"0:triggerWeight_muTauCross",
					"1:triggerWeight_muTauCross"
				]
				self["MuTauTriggerWeightWorkspaceObjectNames"] = [
					"0:m_trgMu19leg_eta2p1_desy_ratio",
					"1:t_genuine_TightIso_mt_ratio,t_fake_TightIso_mt_ratio"
				]
				self["MuTauTriggerWeightWorkspaceObjectArguments"] = [
					"0:m_pt,m_eta",
					"1:t_pt,t_eta"
				]

		if re.search("Run2017|Summer17|Fall17", nickname):
			self["EleTauFakeRateWeightFile"] = ["1:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/scaleFactorWeights/antiElectronDiscrMVA6FakeRateWeights.root"]
		else:
			self["EleTauFakeRateWeightFile"] = ["1:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/scaleFactorWeights/antiElectronDiscrMVA6FakeRateWeights.root"]
		self["TauTauRestFrameReco"] =  "collinear_approximation"
		self["InvalidateNonMatchingElectrons"] =  False
		self["InvalidateNonMatchingMuons"] =  True
		self["InvalidateNonMatchingTaus"] =  True
		self["InvalidateNonMatchingJets"] =  False
		self["UseUWGenMatching"] =  "true"
		self["DirectIso"] =  True
		self["OSChargeLeptons"] = True
		self["SvfitKappaParameter"] = 4.0

		self["AddGenMatchedParticles"] = True
		self["AddGenMatchedTaus"] = True
		self["AddGenMatchedTauJets"] = True
		self["BranchGenMatchedMuons"] = True
		self["BranchGenMatchedTaus"] = True

		self["FakeFactorRooWorkspaceFunction"] = [
			"w_fracs:w_mt_fracs",
			"qcd_fracs:qcd_mt_fracs",
			"ttbar_fracs:ttbar_mt_fracs"
		]

		if re.search("Run2016|Spring16|Summer16|Embedding2016", nickname):
			#settings for jetstotaufakesproducer
			self["FakeFaktorFile"] = "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/jdegens/higgs-kit/ff/2016/mt/fakeFactors_20180831_tight.root"
			self["FakeFactorMethod"] = "cp2016"
			self["FakeFactorFractionsRooWorkspaceFile"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/fakeFactorWeights/rooworkspacefractions/ff_fracs_new_2016.root"


		elif re.search("Run2017|Summer17|Fall17|Embedding2017", nickname):
			self["FakeFaktorFile"] = "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/jdegens/higgs-kit/ff/2017_2/mt/fakeFactors.root" #TODO
			self["FakeFactorMethod"] = "cp2017"
			self["FakeFactorFractionsRooWorkspaceFile"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/fakeFactorWeights/rooworkspacefractions/ff_fracs_pt_2017.root"


		self["Consumers"] = [
			"KappaLambdaNtupleConsumer",
			"cutflow_histogram",
			"SvfitCacheConsumer",
			"#CutFlowTreeConsumer",
			"#KappaMuonsConsumer",
			"#KappaTausConsumer",
			"#KappaTaggedJetsConsumer",
			"#RunTimeConsumer",
			"#PrintEventsConsumer",
			"#PrintGenParticleDecayTreeConsumer"
		]

		quantities_set = Quantities()
		quantities_set.build_quantities(nickname, channel = self["Channel"])
		self["Quantities"] = list(quantities_set.quantities)

		self.addProcessors(nickname)
