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


class et_ArtusConfig(dict):

	def __init__(self):
		pass

	def addProcessors(self, nickname):
		self["Processors"] = [
				"producer:HltProducer",
				#"filter:HltFilter",
				"producer:MetSelector",
				################## special for each channel in et mt tt em.
				"producer:ValidElectronsProducer",
				"filter:ValidElectronsFilter",
				"producer:ElectronTriggerMatchingProducer",
				"filter:MinElectronsCountFilter",
				"producer:ValidMuonsProducer",
				"producer:ValidTausProducer",
				"filter:ValidTausFilter",
				"producer:TauTriggerMatchingProducer",
				"filter:MinTausCountFilter",
				"filter:ValidDiTauPairCandidatesFilter",
				"producer:HttValidVetoElectronsProducer",
				"producer:HttValidLooseElectronsProducer",
				"producer:HttValidLooseMuonsProducer",
				"producer:DiVetoElectronVetoProducer",
				##################
				"producer:Run2DecayChannelProducer",
				"producer:ValidTaggedJetsProducer",
				"producer:ValidBTaggedJetsProducer",
				"producer:TauTauRestFrameSelector",
				"producer:DiLeptonQuantitiesProducer",
				"producer:DiJetQuantitiesProducer",
				################## always the last one
				"producer:EventWeightProducer"
			]

		if re.search("(Spring16|Summer16|Run2016|Run2017|Summer17|Fall17|Embedding(2016|2017))", nickname):
			#'#producer:TauPolarisationTmvaReader', '#producer:MVATestMethodsProducer'
			self["Processors"] += ["producer:CPInitialStateQuantitiesProducer"] #only DoLhenpNLO for IC samples
			self["Processors"] += [
				"producer:RefitVertexSelector",
				"producer:RecoTauCPProducer",
				"producer:PolarisationQuantitiesSvfitProducer",
				#"producer:PolarisationQuantitiesSvfitM91Producer",
				"producer:PolarisationQuantitiesSimpleFitProducer",
				"producer:GenMatchedPolarisationQuantitiesProducer"
			]

			self["Processors"] += ["producer:TaggedJetCorrectionsProducer"]
			self["Processors"] += ["producer:GroupedJetUncertaintyShiftProducer"] #TaggedJetUncertaintyShiftProducer is old

			if not re.search("(LFV).*(?=(Spring16|Summer16))", nickname): self["Processors"] += ["producer:MELAProducer"]

			if re.search("(Run2017|Summer17|Fall17|Embedding2017)", nickname):
				self["Processors"] += ["producer:NewValidETPairCandidatesProducer"]
				self["Processors"] += ["producer:MetFilterProducer"]
			else:
				self["Processors"] += ["producer:ValidETPairCandidatesProducer"]
				#self["Processors"] += ["producer:TaggedJetUncertaintyShiftProducer"]
				self["Processors"] += ["producer:GenMatchedPolarisationQuantitiesProducer"]


			if re.search("Run2016|Run2017|Embedding(2016|2017)", nickname):
				#self["Processors"] += ["producer:TauPolarisationTmvaReader"]
				self["Processors"] += [
					"producer:SimpleFitProducer",
					"filter:MinimalPlotlevelFilter",
					"producer:SvfitProducer"
					#"producer:SvfitM91Producer",
					#"producer:SvfitM125Producer",
					#"producer:MELAM125Producer"
				]
				self["Processors"] += ["producer:JetToTauFakesProducer"] #TODO check if only needed in data

				if re.search("Embedding(2016|2017)", nickname):
					#self["Processors"] += ["producer:GenMatchedTauCPProducer"]
					#self["Processors"] += ["producer:GenMatchedPolarisationQuantitiesProducer"]
					#self["Processors"] += ["producer:RooWorkspaceWeightProducer"]
					self["Processors"] += ["producer:EmbeddingWeightProducer"]
					self["Processors"] += ["producer:TauCorrectionsProducer"]
					#self["Processors"] += ["producer:GenMatchedTauCPProducer"]
					#self["Processors"] += ["producer:GenMatchedPolarisationQuantitiesProducer"]
					if re.search("Embedding2017", nickname):
						self["Processors"] += ["producer:TauTriggerEfficiency2017Producer"]
						self["Processors"] += ["producer:ElectronCorrectionsProducer"]

			else: #(Spring16|Summer16|Summer17|Fall17)
				self["Processors"] += [
					"producer:GenMatchedTauCPProducer",
					"producer:TauCorrectionsProducer",
					"producer:ElectronCorrectionsProducer",
					"producer:SimpleEleTauFakeRateWeightProducer",
					"producer:SimpleMuTauFakeRateWeightProducer"
				]
				self["Processors"] += [
						"producer:MetCorrector" 
					]
				if re.search("Summer17|Fall17", nickname):
					self["Processors"] += ["producer:PrefiringWeightProducer"]
					self["Processors"] += ["producer:LeptonTauTrigger2017WeightProducer", "producer:TauTriggerEfficiency2017Producer"]
					#self["Processors"] += ["producer:IdentificationWeightProducer"]
					self["Processors"] += ["producer:RooWorkspaceWeightProducer"]  #changes from file to file
				else:
					self["Processors"] += ["producer:RooWorkspaceWeightProducer"]  #changes from file to file
					

				if re.search("(LFV).*(?=(Spring16|Summer16))", nickname):
					#"filter:MinimalPlotlevelFilter", '#producer:SvfitProducer', '#producer:SvfitM91Producer', '#producer:SvfitM125Producer'
					self["Processors"] += [
						"producer:ZPtReweightProducer",
						"producer:LFVJetCorrection2016Producer"
					]
				else:
					#self["Processors"] += ["producer:TauPolarisationTmvaReader"]
					#if re.search("VBFHToTauTauM125_RunIIFall17MiniAODv2_PU2017_13TeV_MINIAOD_powheg-pythia8",nickname) == None: 
					self["Processors"] += ["filter:MinimalPlotlevelFilter"]
					self["Processors"] += [
						"producer:SvfitProducer"
						#"producer:SvfitM91Producer",
						#"producer:SvfitM125Producer",
						#"producer:MELAM125Producer"
					]

					if re.search("(DY.?JetsToLL).*(?=(Spring16|Summer16|Summer17|Fall17))", nickname):
						self["Processors"] += ["producer:JetToTauFakesProducer"]
						self["Processors"] += [
							"producer:SimpleFitProducer"
						]
						if re.search("Summer17|Fall17", nickname) == None: #I dont want to do polarisation
							self["Processors"] += ["producer:GenMatchedTauCPProducer"]
							self["Processors"] += ["producer:GenMatchedPolarisationQuantitiesProducer"]
							self["Processors"] +=["producer:ZPtReweightProducer"] #done via rooworkspace in 2017
						#if re.search("(DY.?JetsToLL).*(?=(Spring16|Summer16))", nickname):
						

					elif re.search("(HToTauTau|H2JetsToTauTau|Higgs|JJHiggs).*(?=(Spring16|Summer16|Summer17|Fall17))", nickname):
						#self["Processors"] += ["producer:MadGraphReweightingProducer"]
						self["Processors"] += ["producer:TopPtReweightingProducer"]
						if re.search("amcatnlo",nickname):
							self["DoLhenpNLO"] = True	#NEEDED for stitching

					else: # what samples this correspond to? why no "producer:GenMatchedTauCPProducer"?
						#self["Processors"] += ["producer:MVATestMethodsProducer"]
						self["Processors"] += ["producer:JetToTauFakesProducer"] #TODO check if only needed in data
						self["Processors"] += [
							"producer:SimpleFitProducer"
						]
						if re.search("Summer17|Fall17|Embedding2017", nickname) == None: #I dont want to do polarisation
							#self["Processors"] += ["producer:GenMatchedTauCPProducer"]
							self["Processors"] += ["producer:GenMatchedPolarisationQuantitiesProducer"]
						self["Processors"] += ["producer:TopPtReweightingProducer"] #FIXME only tt?

		elif re.search("(Fall15|Run2015)", nickname):
			#"producer:RefitVertexSelector"], '#producer:TaggedJetUncertaintyShiftProducer',  '#producer:SimpleFitProducer',  '#producer:TauPolarisationTmvaReader', '#producer:MVATestMethodsProducer'
			self["Processors"] += [
				"producer:RecoTauCPProducer",
				"producer:PolarisationQuantitiesSvfitProducer",
				"producer:PolarisationQuantitiesSvfitM91Producer",
				"producer:PolarisationQuantitiesSimpleFitProducer",
				"filter:MinimalPlotlevelFilter",
				"producer:ValidETPairCandidatesProducer",
				"producer:MvaMetSelector"
			]
			self["Processors"] += ["producer:TaggedJetCorrectionsProducer"]

			if re.search("Run2015", nickname):
				#self["Processors"] += ["#producer:SimpleFitProducer", "#producer:SvfitProducer", "#producer:SvfitM91Producer", "#producer:SvfitM125Producer", "#producer:MELAProducer", "#producer:MELAM125Producer"]
				self["Processors"] += ["producer:GenMatchedPolarisationQuantitiesProducer"]

			else:
				#self["Processors"] += ['#producer:MVATestMethodsProducer', '#producer:RefitVertexSelector']
				self["Processors"] += [
					"producer:TriggerWeightProducer",
					"producer:IdentificationWeightProducer",
					"producer:MvaMetCorrector",
					"producer:MetCorrector",
					"producer:TauCorrectionsProducer",
					"producer:EleTauFakeRateWeightProducer"
				]

				if re.search("(DY.?JetsToLL).*(?=Fall15)", nickname):
					#self["Processors"] += ["#producer:SimpleFitProducer", '#producer:SvfitProducer', '#producer:SvfitM91Producer', '#producer:SvfitM125Producer', '#producer:MELAProducer', '#producer:MELAM125Producer']
					self["Processors"] += [
						"producer:ZPtReweightProducer",
						"producer:GenMatchedTauCPProducer",
						"producer:GenMatchedPolarisationQuantitiesProducer"
					]

				elif re.search("(HToTauTau|H2JetsToTauTau|Higgs).*(?=Fall15)",nickname):
					self["Processors"] += [
						'producer:TopPtReweightingProducer',
						'producer:GenMatchedTauCPProducer',
						'producer:MadGraphReweightingProducer',
						"producer:SvfitProducer",
						"producer:SvfitM91Producer",
						"producer:SvfitM125Producer",
						"producer:MELAProducer",
						"producer:MELAM125Producer"
					]

				elif re.search("^((?!(DY.?JetsToLL|HToTauTau|H2JetsToTauTau|Higgs)).)*Fall15", nickname):
					# self["Processors"] += ["#producer:SvfitProducer"], "#producer:MELAProducer"], "#producer:MELAM125Producer"]
					self["Processors"] += [
						"producer:SvfitM91Producer",
						"producer:SvfitM125Producer",
						'producer:TopPtReweightingProducer',
						'producer:GenMatchedPolarisationQuantitiesProducer'
					]

		else:
			# "#producer:TauPolarisationTmvaReader"
			self["Processors"] += ["producer:TauCorrectionsProducer",
				"producer:TaggedJetUncertaintyShiftProducer",
				"producer:MetCorrector",
				"producer:SvfitProducer",
				"producer:SvfitM91Producer",
				"producer:SvfitM125Producer",
				"producer:MELAProducer",
				"producer:MELAM125Producer",
				"producer:SimpleFitProducer",
				"producer:RooWorkspaceWeightProducer",
				"producer:RefitVertexSelector",
				"producer:RecoTauCPProducer",
				"producer:GenMatchedPolarisationQuantitiesProducer",
				"producer:PolarisationQuantitiesSvfitProducer",
				"producer:PolarisationQuantitiesSvfitM91Producer",
				"producer:PolarisationQuantitiesSimpleFitProducer",
			]

		# self["Processors"] += ["producer:EventWeightProducer"]

		self["Processors"] = list(set(self["Processors"]))
		processorOrderingkey = ProcessorsOrdered(channel = self["Channel"])
		ordered_processors = processorOrderingkey.order_processors(self["Processors"])
		self["Processors"] = copy.deepcopy(ordered_processors)

	def build_config(self, nickname): #Maybe change this the arguments to process/year and DATA/MC
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

		datasetsHelper = datasetsHelperTwopz.datasetsHelperTwopz(os.path.expandvars("$CMSSW_BASE/src/Kappa/Skimming/data/datasets.json"))

		# define frequently used conditions
		isEmbedded = datasetsHelper.isEmbedded(nickname)
		isData = datasetsHelper.isData(nickname) and (not isEmbedded)

		ElectronID_config = sEID.Electron_ID(nickname, iso=False, wp=90)
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

		#JECUncertaintySplit_config = sJECUS.JECUncertaintySplit(nickname)
		#self.update(JECUncertaintySplit_config)

		JetID_config = sJID.Jet_ID(nickname)
		self.update(JetID_config)

		BTaggedJet_config = sBTJID.BTaggedJet_ID(nickname)
		self.update(BTaggedJet_config)

		Svfit_config = sSvfit.Svfit(nickname)
		self.update(Svfit_config)

		if re.search("VBFHToTauTauM125_RunIIFall17MiniAODv2_PU2017_13TeV_MINIAOD_powheg-pythia8",nickname):
			mplf = sMPlF.MinimalPlotlevelFilter(nickname=nickname, channel="ET", eTauFakeRate=False, sync=True)
		else:
			mplf = sMPlF.MinimalPlotlevelFilter(nickname=nickname, channel="ET", eTauFakeRate=False, sync=False)
		self.update(mplf.minPlotLevelDict)
		
		MVATestMethods_config = sMVATM.MVATestMethods()
		self.update(MVATestMethods_config)

		TauES_config = sTES.TauES(nickname)
		self.update(TauES_config)

		TauPolarisationMva_config = sTPMVA.TauPolarisationMva()
		self.update(TauPolarisationMva_config)

		self.update(IdAndTriggerSF(nickname, channel="ET", dcach=False))


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

		self["ElectronLowerPtCuts"] = ["26.0"]  #default: !=2015
		self["DiTauPairLepton1LowerPtCuts"] = ["HLT_Ele25_eta2p1_WPTight_Gsf_v:26.0"]  #default: !=2015 or !=2017

		if re.search("(Fall15MiniAODv2|Run2015D|Embedding2015)", nickname):
			self["HltPaths"] = ["HLT_Ele23_WPLoose_Gsf"]
			self["ElectronLowerPtCuts"] = ["24.0"]           #2015
			self["DiTauPairLepton1LowerPtCuts"] = ["HLT_Ele23_WPLoose_Gsf_v:24.0"]  #2015
			self["DiTauPairHltPathsWithoutCommonMatchRequired"] = ["HLT_Ele23_WPLoose_Gsf_v"]

		elif re.search("Run2016|Spring16|Summer16", nickname):          #spring16 self["NoHltFiltering"] = True for cp config False for RUN2 set to false here
			self["HltPaths"] = ["HLT_Ele25_eta2p1_WPTight_Gsf"]
			self["DiTauPairHltPathsWithoutCommonMatchRequired"] = ["HLT_Ele25_eta2p1_WPTight_Gsf_v"]
			if re.search("Spring16", nickname):
				self["DiTauPairNoHLT" ] = True
				self["NoHltFiltering"] = True

		elif re.search("Embedding(2016|MC)", nickname):
			self["HltPaths"] =[""]
			self["NoHltFiltering"] = True               #else: self["NoHltFiltering"] = True
			self["DiTauPairNoHLT" ] = True

			self["DiTauPairHltPathsWithoutCommonMatchRequired"] = ["HLT_Ele25_eta2p1_WPTight_Gsf_v"]

		# elif re.search("Embedding2017", nickname):
		# 	self["NoHltFiltering"] = True

		elif re.search("Run2017|Summer17|Fall17|Embedding2017", nickname):
			#from https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsToTauTauWorking2017#Trigger_Information
			self["HltPaths"] = [
					"HLT_Ele27_WPTight_Gsf",
					"HLT_Ele32_WPTight_Gsf",
					"HLT_Ele32_WPTight_Gsf_L1DoubleEG",
					"HLT_Ele35_WPTight_Gsf",
					"HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTau30_eta2p1_CrossL1"
				]
			self["ElectronTriggerFilterNames"] = [#[] if isEmbedded else []
					"HLT_Ele27_WPTight_Gsf_v:hltEle27WPTightGsfTrackIsoFilter",
					"HLT_Ele32_WPTight_Gsf_v:hltEle32WPTightGsfTrackIsoFilter",
					"HLT_Ele32_WPTight_Gsf_L1DoubleEG_v:hltEle32L1DoubleEGWPTightGsfTrackIsoFilter",
					"HLT_Ele32_WPTight_Gsf_L1DoubleEG_v:hltEGL1SingleEGOrFilter",
					"HLT_Ele35_WPTight_Gsf_v:hltEle35noerWPTightGsfTrackIsoFilter"
				]
			if isEmbedded:
				self["ElectronTriggerFilterNames"] += [
					# "HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTau30_eta2p1_CrossL1_v:hltL1sBigORLooseIsoEGXXerIsoTauYYerdRMin0p3",
					"HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTau30_eta2p1_CrossL1_v:hltEle24erWPTightGsfTrackIsoFilterForTau"
				]
				self["RequireFiredHlt"] = False
			else:
				self["ElectronTriggerFilterNames"] += [
					"HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTau30_eta2p1_CrossL1_v:hltEle24erWPTightGsfTrackIsoFilterForTau",
					"HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTau30_eta2p1_CrossL1_v:hltOverlapFilterIsoEle24WPTightGsfLooseIsoPFTau30"
				]

			self["TauTriggerFilterNames"] = [
					"HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTau30_eta2p1_CrossL1_v:hltL1sBigORLooseIsoEGXXerIsoTauYYerdRMin0p3"
				] if isEmbedded else [
					"HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTau30_eta2p1_CrossL1_v:hltSelectedPFTau30LooseChargedIsolationL1HLTMatched",
					"HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTau30_eta2p1_CrossL1_v:hltOverlapFilterIsoEle24WPTightGsfLooseIsoPFTau30"
				]

			self["HLTBranchNames"] = [
				"trg_singleelectron_27:HLT_Ele27_WPTight_Gsf_v",
				"trg_singleelectron_32:HLT_Ele32_WPTight_Gsf_v",
				"trg_singleelectron_32_fallback:HLT_Ele32_WPTight_Gsf_L1DoubleEG_v",
				"trg_singleelectron_35:HLT_Ele35_WPTight_Gsf_v",
				"trg_crosselectron_ele24tau30:HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTau30_eta2p1_CrossL1_v"
			]

			self["ElectronLowerPtCuts"] = [	"25.0"]
			self["DiTauPairLepton1LowerPtCuts"] = [
					"HLT_Ele27_WPTight_Gsf_v:28.0",
					"HLT_Ele32_WPTight_Gsf_v:33.0",
					"HLT_Ele32_WPTight_Gsf_L1DoubleEG_v:33.0",
					"HLT_Ele35_WPTight_Gsf_v:36.0",
					"HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTau30_eta2p1_CrossL1_v:25.0"
				]
			self["DiTauPairLepton2LowerPtCuts"] = ["HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTau30_eta2p1_CrossL1_v:35.0"]
			self["DiTauPairHltPathsWithoutCommonMatchRequired"] = [
					"HLT_Ele35_WPTight_Gsf_v",
					"HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTau30_eta2p1_CrossL1_v",
					"HLT_Ele32_WPTight_Gsf_v",
					"HLT_Ele32_WPTight_Gsf_L1DoubleEG_v",
					"HLT_Ele27_WPTight_Gsf_v"
				]

			self["CheckLepton1TriggerMatch"] = [
				"trg_singleelectron_27",
      				"trg_singleelectron_32",
      				"trg_singleelectron_32_fallback",
				"trg_crossele_ele24tau30",
				"trg_singleelectron_35"
			  ]
			self["CheckLepton2TriggerMatch"] = [
				"trg_crosselectron_ele24tau30"
				]
			if re.search("Fall17", nickname):
				self["GlobalWeight"] = 0.991


		self["TauID"] =  "TauIDRecommendation13TeV"
		self["TauUseOldDMs"] =  True

		self["ElectronUpperAbsEtaCuts"] = ["2.1"]
		self["TauLowerPtCuts"] = ["20.0"]
		self["TauUpperAbsEtaCuts"] = ["2.3"]
		self["TriggerObjectLowerPtCut"] = -1.0

		self["DiTauPairMinDeltaRCut"] = 0.5
		self["DiTauPairIsTauIsoMVA"] = True

		self["EventWeight"] =  "eventWeight"

		if re.search("(Run2017|Summer17|Fall17|Embedding2017)", nickname):
			if isEmbedded:
				self["SaveEmbeddingWeightAsOptionalOnly"] = "true"
				self["EmbeddingWeightWorkspace"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/scaleFactorWeights/htt_scalefactors_v17_6.root"
				self["EmbeddingWeightWorkspaceWeightNames"] = [
					"0:triggerWeight_doublemu",
					"0:idweight_doublemu",
					"1:idweight_doublemu",
					"0:isoweight",
					"0:idweight",
					"0:triggerWeight_trg27_trg32_trg35_embed",
					"0:triggerWeight_trg_EleTau_Ele24Leg_embed",
					"1:triggerWeight_tauLeg",
					"0:triggerWeight_trg27_trg32_trg35_data",
					"0:triggerWeight_trg_EleTau_Ele24Leg_data"
				]
				self["EmbeddingWeightWorkspaceObjectNames"] = [
					"0:m_sel_trg_ratio",
					"0:m_sel_idEmb_ratio",
					"1:m_sel_idEmb_ratio",
					"0:e_iso_binned_embed_kit_ratio",
					"0:e_id90_embed_kit_ratio",
					"0:e_trg27_trg32_trg35_embed_kit_ratio",
					"0:e_trg_EleTau_Ele24Leg_kit_ratio_embed",
					"1:et_emb_LooseChargedIsoPFTau30_kit_ratio",
					"0:e_trg27_trg32_trg35_kit_data",
					"0:e_trg_EleTau_Ele24Leg_desy_data"
				]
				self["EmbeddingWeightWorkspaceObjectArguments"] = [
					"0:gt1_pt,gt1_eta,gt2_pt,gt2_eta",
					"0:gt_pt,gt_eta",
					"1:gt_pt,gt_eta",
					"0:e_pt,e_eta,e_iso",
					"0:e_pt,e_eta",
					"0:e_pt,e_eta",
					"0:e_pt",
					"1:t_pt",
					"0:e_pt,e_eta",
					"0:e_pt,e_eta"
				]
			else:
				#self["RooWorkspace"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/scaleFactorWeights/htt_scalefactors_v17_1.root"
				self["RooWorkspace"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/scaleFactorWeights/htt_scalefactors_2017_v3.root"
				self["RooWorkspaceWeightNames"] = [
					#"0:crossTriggerMCEfficiencyWeight",
					#"0:crossTriggerDataEfficiencyWeight",
					#"0:singleTriggerMCEfficiencyWeight",
					#"0:singleTriggerDataEfficiencyWeight",
					#"0:singleTriggerMCEfficiencyWeightKIT",
					#"0:singleTriggerDataEfficiencyWeightKIT",

					"0:idWeight",
					"0:isoWeight",
					"0:trackWeight"
				    ]
				self["RooWorkspaceObjectNames"] = [
					#"0:e_trg_EleTau_Ele24Leg_desy_mc",
					#"0:e_trg_EleTau_Ele24Leg_desy_data",
					#"0:e_trg_SingleEle_Ele32OREle35_desy_mc",
					#"0:e_trg_SingleEle_Ele32OREle35_desy_data",
					#"0:e_trg32or35_mc",
					#"0:e_trg32or35_data",
					"0:e_id90_kit_ratio",
					"0:e_iso_kit_ratio",
					"0:e_trk_ratio"
				]
				#for embedding use e_id_embed_ratio and e_iso_binned_embed_ratio

				self["RooWorkspaceObjectArguments"] = [
					#"0:e_pt,e_eta",
					#"0:e_pt,e_eta",
					#"0:e_pt,e_eta",
					#"0:e_pt,e_eta",
					#"0:e_pt,e_eta",
					#"0:e_pt,e_eta",

					"0:e_pt,e_eta",
					"0:e_pt,e_eta",
					"0:e_pt,e_eta"
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
						"0:e_triggerEffSingle_mc",
						"0:e_triggerEffCross_mc",
						"0:e_triggerEffSingle_data",
						"0:e_triggerEffCross_data"
					]
					self["LeptonTauTrigger2017WeightWorkspaceObjectNames"] = [
						"0:e_trg_binned_mc",
						"0:e_trg24_fromDoubleE_mc",
						"0:e_trg_binned_data",
						"0:e_trg24_fromDoubleE_data"
					]
					self["LeptonTauTrigger2017WeightWorkspaceObjectArguments"] = [
						"0:e_pt,e_eta,e_iso",
						"0:e_pt,e_eta",
						"0:e_pt,e_eta,e_iso",
						"0:e_pt,e_eta"
					]
				elif self["TriggerEfficiencyMode"] == "no_overlap_triggers":
					self["LeptonTauTrigger2017WeightWorkspace"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/scaleFactorWeights/htt_scalefactors_2017_v3.root"
					self["SaveLeptonTauTrigger2017WeightAsOptionalOnly"] = "true"
					self["LeptonTauTrigger2017WeightWorkspaceWeightNames"] = [
						"0:triggerWeight_singleE",
						"0:triggerWeight_etaucross",
					]
					self["LeptonTauTrigger2017WeightWorkspaceObjectNames"] = [
						"0:e_trg_27_32_35_ratio",
						"0:e_trg_EleTau_Ele24Leg_desy_ratio",
					]
					self["LeptonTauTrigger2017WeightWorkspaceObjectArguments"] = [
						"0:e_pt,e_eta",
						"0:e_pt,e_eta",
					]

		elif re.search("(Spring16|Summer16|Run2016|Embedding2016)", nickname):
			self["RooWorkspace"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/scaleFactorWeights/htt_scalefactors_v16_11_embedded.root" if isEmbedded else "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/scaleFactorWeights/htt_scalefactors_sm_moriond_v2.root"
			self["RooWorkspaceWeightNames"] = [
				"0:triggerWeight",
				"0:idIsoWeight"
			] if not isEmbedded else [ #TODO: Use Embedding weight rooworkspace producer instead
				"0:triggerWeight_doublemu",
				"0:isoweight",
				"0:idweight",
				"0:triggerWeight_singleE"
			]
			self["RooWorkspaceObjectNames"] = [
				"0:e_trgEle25eta2p1WPTight_desy_ratio",
				"0:e_idiso0p1_desy_ratio"
			] if not isEmbedded else [
				"0:m_sel_trg_ratio",
				"0:e_iso_ratio",
				"0:e_id_ratio",
				"0:e_trg_ratio"
			]
			self["RooWorkspaceObjectArguments"] = [
				"0:e_pt,e_eta",
				"0:e_pt,e_eta"
			] if not isEmbedded else [
				"0:gt1_pt,gt1_eta,gt2_pt,gt2_eta",
				"0:e_pt,e_eta",
				"0:e_pt,e_eta",
				"0:e_pt,e_eta"
			]

		if re.search("(Fall15MiniAODv2|Run2015D|Embedding2015)", nickname):
			self["TriggerEfficiencyData"] = [ "0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_Run2015_Electron_Ele23_fall15.root" ]
			self["TriggerEfficiencyMc"] = [ "0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_MC_Electron_Ele23_fall15.root"]

			self["IdentificationEfficiencyData"] = ["0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/identificationWeights/identificationEfficiency_Run2015_Electron_IdIso0p1_fall15.root"]
			self["IdentificationEfficiencyMc"] = ["0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/identificationWeights/identificationEfficiency_MC_Electron_IdIso0p1_fall15.root"]

		elif re.search("Run2017|Summer17|Fall17|Embedding2017", nickname):
			self["TriggerEfficiencyData"] = ["0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_Run2017_Electron_Ele32orEle35.root"]
			self["TriggerEfficiencyMc"] = ["0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_MCFall2017_Electron_Ele32orEle35.root"]

			self["IdentificationEfficiencyData"] = ["0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/identificationWeights/identificationEfficiency_Run2017_Electron_IdIso_IsoLt0.10_eff_RerecoFall17.root"]
			self["IdentificationEfficiencyMc"] = ["0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/identificationWeights/identificationEfficiency_MCFall2017_Electron_IdIso_IsoLt0.10_eff_RerecoFall17.root"]

		else:
			self["TriggerEfficiencyData"] = ["0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_Run2016_Electron_Ele25WPTight_eff.root" ]
			self["TriggerEfficiencyMc"] = ["0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_MC_Electron_Ele25WPTight_eff.root" ]

			self["IdentificationEfficiencyData"] = ["0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/identificationWeights/identificationEfficiency_Run2016_Electron_IdIso_IsoLt0p1_eff.root"]
			self["IdentificationEfficiencyMc"] = ["0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/identificationWeights/identificationEfficiency_MC_Electron_IdIso_IsoLt0p1_eff.root"]



		if re.search("Run2017|Summer17|Fall17|Embedding2017", nickname): #same as for 2016?
			pass
			#self["EleTauFakeRateWeightFile"] = ["1:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/scaleFactorWeights/antiElectronDiscrMVA6FakeRateWeights.root"]  TODO is not yet provided
		else:
			self["EleTauFakeRateWeightFile"] = ["1:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/scaleFactorWeights/antiElectronDiscrMVA6FakeRateWeights.root"]

		self["TauTauRestFrameReco"] = "collinear_approximation"


		if re.search("(Fall15MiniAODv2|Run2015D|Embedding2015)", nickname):
			self["ElectronTriggerFilterNames"] = ["HLT_Ele23_WPLoose_Gsf_v:hltEle23WPLooseGsfTrackIsoFilter"]

		elif re.search("Run2016|Spring16|Summer16|Embedding(2016|MC)", nickname):
			self["ElectronTriggerFilterNames"] = ["HLT_Ele25_eta2p1_WPTight_Gsf_v:hltEle25erWPTightGsfTrackIsoFilter"]


		self["FakeFactorRooWorkspaceFunction"] = [
			"w_fracs:w_et_fracs",
			"qcd_fracs:qcd_et_fracs",
			"ttbar_fracs:ttbar_et_fracs"
		]

		if re.search("Run2016|Spring16|Summer16", nickname):
			#settings for jetstotaufakesproducer
			self["FakeFaktorFile"] = "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/jdegens/higgs-kit/ff/2016/et/fakeFactors_20180831_tight.root"
			self["FakeFactorMethod"] = "cp2016"
			self["FakeFactorFractionsRooWorkspaceFile"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/fakeFactorWeights/rooworkspacefractions/ff_fracs_new_2016.root"

		elif re.search("Run2017|Summer17|Fall17|Embedding2017", nickname):
			self["FakeFaktorFile"] = "root://grid-vo-cms.physik.rwth-aachen.de:1094//store/user/jdegens/higgs-kit/ff/2017_2/et/fakeFactors.root" #TODO
			self["FakeFactorMethod"] = "cp2017"
			self["FakeFactorFractionsRooWorkspaceFile"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/fakeFactorWeights/rooworkspacefractions/ff_fracs_pt_2017.root"


		self["InvalidateNonMatchingElectrons"] = True
		self["InvalidateNonMatchingMuons"] = False
		self["InvalidateNonMatchingTaus"] = True
		self["InvalidateNonMatchingJets"] = False
		self["UseUWGenMatching"] = "true"
		self["DirectIso"] = True

		self["OSChargeLeptons"] = True
		self["SvfitKappaParameter"] = 4.0

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

		quantities_set = Quantities()
		quantities_set.build_quantities(nickname, channel = self["Channel"])
		self["Quantities"] = list(quantities_set.quantities)

		self.addProcessors(nickname)
