# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import re
import copy
import os

from HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Run2CPStudies.quantities import Quantities

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

import HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Run2CPStudies.Includes.settingsTauPolarisationMva as sTPMVA

from HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Run2Analysis.Includes.idAndTriggerSF import IdAndTriggerSF
import Kappa.Skimming.datasetsHelperTwopz as datasetsHelperTwopz


class em_ArtusConfig(dict):

	def __init__(self):
		pass

	def addProcessors(self, nickname):
		self["Processors"] = [
				"producer:HltProducer",
				"filter:HltFilter",
				"producer:MetSelector",
				################## special for each channel in et mt tt em.
				"producer:ValidElectronsProducer",
				"filter:ValidElectronsFilter",
				"producer:ElectronTriggerMatchingProducer",
				"filter:MinElectronsCountFilter",
				"producer:ValidMuonsProducer",
				"filter:ValidMuonsFilter",
				"producer:MuonTriggerMatchingProducer",
				"filter:MinMuonsCountFilter",
				"producer:ValidTausProducer",
				"producer:ValidEMPairCandidatesProducer",
				"filter:ValidDiTauPairCandidatesFilter",
				"producer:HttValidLooseMuonsProducer",
				##################
				"producer:Run2DecayChannelProducer",          
				"producer:TaggedJetCorrectionsProducer",
				"producer:ValidTaggedJetsProducer",
				"producer:ValidBTaggedJetsProducer",	
				"producer:TauTauRestFrameSelector",
				"producer:DiLeptonQuantitiesProducer",
				"producer:DiJetQuantitiesProducer",
				"producer:HttValidLooseElectronsProducer"
				]

		if re.search("(Spring16|Summer16|Run2016)", nickname):
			self["Processors"] += ["producer:RefitVertexSelector"]
			self["Processors"] += ["producer:RecoTauCPProducer"]
			self["Processors"] += ["producer:PolarisationQuantitiesSvfitProducer"]
			self["Processors"] += ["producer:PolarisationQuantitiesSvfitM91Producer"]
			self["Processors"] += ["producer:PolarisationQuantitiesSimpleFitProducer"]
			self["Processors"] += ["producer:TaggedJetUncertaintyShiftProducer"]
			
			if re.search("Run2016", nickname):
				#self["Processors"] += ["producer:MVATestMethodsProducer"]
						
				self["Processors"] += ["producer:SimpleFitProducer"]
				self["Processors"] += ["producer:GenMatchedPolarisationQuantitiesProducer"]

				self["Processors"] += ["filter:MinimalPlotlevelFilter"]
				self["Processors"] += ["producer:SvfitProducer"]
				self["Processors"] += ["producer:SvfitM91Producer"]
				self["Processors"] += ["producer:SvfitM125Producer"]

				self["Processors"] += ["producer:MELAProducer"]
				self["Processors"] += ["producer:MELAM125Producer"]


				#self["Processors"] += ["producer:TauPolarisationTmvaReader"]

			else:
				#self["Processors"] += ["producer:TauCorrectionsProducer"]
				self["Processors"] += ["producer:ElectronCorrectionsProducer"] #channel dependent
				self["Processors"] += ["producer:TriggerWeightProducer"]
				self["Processors"] += ["producer:MetCorrector"]
				self["Processors"] += ["producer:RooWorkspaceWeightProducer"]
							
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
					self["Processors"] += ["producer:SvfitM91Producer"]
					self["Processors"] += ["producer:SvfitM125Producer"]

					self["Processors"] += ["producer:MELAProducer"]
					self["Processors"] += ["producer:MELAM125Producer"]

					if re.search("(DY.?JetsToLL).*(?=(Spring16|Summer16))", nickname):
						self["Processors"] += ["producer:ZPtReweightProducer"]			

						self["Processors"] += ["producer:SimpleFitProducer"]
						self["Processors"] += ["producer:GenMatchedTauCPProducer"]
						self["Processors"] += ["producer:GenMatchedPolarisationQuantitiesProducer"]

						#self["Processors"] += ["producer:TauPolarisationTmvaReader"]

					elif re.search("(HToTauTau|H2JetsToTauTau|Higgs).*(?=(Spring16|Summer16))", nickname):
						self["Processors"] += [
							"producer:TopPtReweightingProducer"
						] 
						#self["Processors"] += ["producer:MVATestMethodsProducer"]
						self["Processors"] += ["producer:GenMatchedTauCPProducer"]
						#self["Processors"] += ["producer:TauPolarisationTmvaReader"]
						#self["Processors"] += ["producer:MadGraphReweightingProducer"]
					else:
						self["Processors"] += [	"producer:TopPtReweightingProducer"] 
						#self["Processors"] += ["producer:MVATestMethodsProducer"]
						self["Processors"] += ["producer:SimpleFitProducer"]				
						self["Processors"] += ["producer:GenMatchedPolarisationQuantitiesProducer"]
				
						#self["Processors"] += ["producer:TauPolarisationTmvaReader"]

		elif re.search("(Fall15|Run2015)", nickname):
			#self["Processors"] += ["producer:RefitVertexSelector"]
			self["Processors"] += ["producer:RecoTauCPProducer"]
			self["Processors"] += ["producer:PolarisationQuantitiesSvfitProducer"]
			self["Processors"] += ["producer:PolarisationQuantitiesSvfitM91Producer"]
			self["Processors"] += ["producer:PolarisationQuantitiesSimpleFitProducer"]
			self["Processors"] += ["filter:MinimalPlotlevelFilter"]
			self["Processors"] += ["producer:MvaMetSelector"]

			
			if re.search("Run2015", nickname):
				pass
				#self["Processors"] += ["producer:SimpleFitProducer"]
			
				#self["Processors"] += ["producer:SvfitProducer"]
				#self["Processors"] += ["producer:SvfitM91Producer"]
				#self["Processors"] += ["producer:SvfitM125Producer"]

				#self["Processors"] += ["producer:MELAProducer"]
				#self["Processors"] += ["producer:MELAM125Producer"]
			else:
				self["Processors"] += ["producer:MvaMetCorrector"]
				self["Processors"] += ["producer:MetCorrector"]
				self["Processors"] += ["producer:RecoElectronGenParticleMatchingProducer"] #if you grep this, it is already in globalprocessors
				self["Processors"] += ["producer:RecoMuonGenParticleMatchingProducer"]
				self["Processors"] += ["producer:MatchedLeptonsProducer"]
				#self["Processors"] += ["producer:TauCorrectionsProducer"]
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

	def build_config(self, nickname, *args, **kwargs): #Maybe change this the arguments to process/year and DATA/MC


		datasetsHelper = datasetsHelperTwopz.datasetsHelperTwopz(os.path.expandvars("$CMSSW_BASE/src/Kappa/Skimming/data/datasets.json"))

		# define frequently used conditions
		isEmbedded = datasetsHelper.isEmbedded(nickname)
		isData = datasetsHelper.isData(nickname) and (not isEmbedded)

		ElectronID_config = sEID.Electron_ID(nickname)
		ElectronID_config.looseElectron_ID(nickname) 		#append the config for loose electron ID because it is used
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

		mplf = sMPlF.MinimalPlotlevelFilter(nickname=nickname, channel="EM", eTauFakeRate=False)
		self.update(mplf.minPlotLevelDict)

		MVATestMethods_config = sMVATM.MVATestMethods()
		self.update(MVATestMethods_config)

		self["Channel"] = "EM"
		self["MinNElectrons"] = 1
		self["MinNMuons"] = 1
		self["HltPaths_comment"] = "The first path must be one with the higher pt cut on the electron. The second and last path must be one with the higher pt cut on the muon. Corresponding Pt cuts are implemented in the Run2DecayChannelProducer."

		self["NoHltFiltering"] = False #*default
		self["DiTauPairLepton1LowerPtCuts"] = [								     # **default
			"HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v:24.0"
		]

		self["DiTauPairLepton2LowerPtCuts"] = [								# ***default
			"HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_v:24.0",
			"HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_v:24.0"
		]
		self["DiTauPairNoHLT"] = False
		
		if re.search("(Fall15MiniAODv2|Run2015D|Embedding2015)", nickname):
			self["HltPaths"] = [
				"HLT_Mu8_TrkIsoVVL_Ele17_CaloIdL_TrackIdL_IsoVL",
				"HLT_Mu17_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL"
			]
			self["DiTauPairLepton1LowerPtCuts"] = [							#**
				"HLT_Mu17_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v:18.0"
			]
			self["DiTauPairLepton2LowerPtCuts"] = [
				"HLT_Mu8_TrkIsoVVL_Ele17_CaloIdL_TrackIdL_IsoVL_v:18.0"
			]

		elif re.search("Run2016(B|C|D|E|F)|Spring16|Summer16", nickname):
			self["HltPaths"] = [
				"HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL",
				"HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL"
			]

		elif re.search("Run2016(G|H)", nickname):
			self["HltPaths"] = [
				"HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ",
				"HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ"
			]
			self["DiTauPairLepton1LowerPtCuts"] = [							#**
				"HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v:24.0"
			]

		elif re.search("Embedding(2016|MC)", nickname):
			self["HltPaths"] = []
			self["NoHltFiltering"] = True 								#*if "Embedding(2016|MC)"
			self["DiTauPairLepton1LowerPtCuts"] = [                                         	 #**
				"HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v:-1.0",
				"HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v:-1.0"
			]
			self["DiTauPairLepton2LowerPtCuts"] = [							#***
				"HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_v:-1.0",
				"HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_v:-1.0"
			]
			self["DiTauPairNoHLT"] = True
			self["LowerCutHardLepPt"] = 24.0
		
		self["ElectronLowerPtCuts"] = [
			"13.0"
		]
		self["ElectronUpperAbsEtaCuts"] = [
			"2.5"
		]
		self["MuonLowerPtCuts"] = [
			"10.0"
		]
		self["MuonUpperAbsEtaCuts"] = [
			"2.4"
		]
		self["DeltaRTriggerMatchingElectrons"] = 0.4
		self["DeltaRTriggerMatchingMuons"] = 0.4
		self["DiTauPairMinDeltaRCut"] = 0.3
		self["DiTauPairIsTauIsoMVA"] = True

		self["EventWeight"] = "eventWeight"
		self["RooWorkspace"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/scaleFactorWeights/htt_scalefactors_v16_5_1.root"
		self["RooWorkspaceWeightNames"] = [
			"0:idIsoWeight",
			"0:emuQcdOsssWeight",
			"0:emuQcdOsssRateUpWeight",
			"0:emuQcdOsssRateDownWeight",
			"0:emuQcdOsssShapeUpWeight",
			"0:emuQcdOsssShapeDownWeight",
			"0:emuQcdExtrapUpWeight",
			"0:emuQcdExtrapDownWeight",			
			"1:idIsoWeight",
			"1:emuQcdOsssWeight",
			"1:emuQcdOsssRateUpWeight",
			"1:emuQcdOsssRateDownWeight",
			"1:emuQcdOsssShapeUpWeight",
			"1:emuQcdOsssShapeDownWeight",
			"1:emuQcdExtrapUpWeight",
			"1:emuQcdExtrapDownWeight"							
		]
		self["RooWorkspaceObjectNames"] = [
			"0:e_idiso0p15_desy_ratio",
			"0:em_qcd_osss_binned",
			"0:em_qcd_osss_rateup_binned",
			"0:em_qcd_osss_ratedown_binned",
			"0:em_qcd_osss_shapeup_binned",
			"0:em_qcd_osss_shapedown_binned",
			"0:em_qcd_extrap_up",
			"0:em_qcd_extrap_down",			
			"1:m_idiso0p20_desy_ratio",
			"1:em_qcd_osss_binned",
			"1:em_qcd_osss_rateup_binned",
			"1:em_qcd_osss_ratedown_binned",
			"1:em_qcd_osss_shapeup_binned",
			"1:em_qcd_osss_shapedown_binned",
			"1:em_qcd_extrap_up",
			"1:em_qcd_extrap_down",				
		]
		self["RooWorkspaceObjectArguments"] = [
			"0:e_pt,e_eta",
			"0:njets,dR,e_pt,m_pt",
			"0:njets,dR,e_pt,m_pt",
			"0:njets,dR,e_pt,m_pt",
			"0:njets,dR,e_pt,m_pt",
			"0:njets,dR,e_pt,m_pt",
			"0:njets,dR,e_pt,m_pt",
			"0:njets,dR,e_pt,m_pt",
			"1:m_pt,m_eta",
			"1:njets,dR,e_pt,m_pt",
			"1:njets,dR,e_pt,m_pt",
			"1:njets,dR,e_pt,m_pt",
			"1:njets,dR,e_pt,m_pt",
			"1:njets,dR,e_pt,m_pt",
			"1:njets,dR,e_pt,m_pt",
			"1:njets,dR,e_pt,m_pt"
		]

		self.update(IdAndTriggerSF(nickname, channel="EM", dcach=False))

		self["TauTauRestFrameReco"] = "collinear_approximation"

		if re.search("(Fall15MiniAODv2|Run2015D|Embedding2015)", nickname):
			self["ElectronTriggerFilterNames"] = [
				"HLT_Mu17_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v:hltMu17TrkIsoVVLEle12CaloIdLTrackIdLIsoVLElectronlegTrackIsoFilter",
				"HLT_Mu8_TrkIsoVVL_Ele17_CaloIdL_TrackIdL_IsoVL_v:hltMu8TrkIsoVVLEle17CaloIdLTrackIdLIsoVLElectronlegTrackIsoFilter"
			]
			self["MuonTriggerFilterNames"] = [
				"HLT_Mu17_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v:hltMu17TrkIsoVVLEle12CaloIdLTrackIdLIsoVLMuonlegL3IsoFiltered17",
				"HLT_Mu8_TrkIsoVVL_Ele17_CaloIdL_TrackIdL_IsoVL_v:hltMu8TrkIsoVVLEle17CaloIdLTrackIdLIsoVLMuonlegL3IsoFiltered8"
			]

		elif re.search("Run2016(B|C|D|E|F)|Spring16|Summer16", nickname):
			self["ElectronTriggerFilterNames"] = [
				"HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v:hltMu23TrkIsoVVLEle12CaloIdLTrackIdLIsoVLElectronlegTrackIsoFilter",
				"HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_v:hltMu8TrkIsoVVLEle23CaloIdLTrackIdLIsoVLElectronlegTrackIsoFilter"
			]
			self["MuonTriggerFilterNames"] = [
				"HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v:hltMu23TrkIsoVVLEle12CaloIdLTrackIdLIsoVLMuonlegL3IsoFiltered23",
				"HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_v:hltMu8TrkIsoVVLEle23CaloIdLTrackIdLIsoVLMuonlegL3IsoFiltered8"
			]

		elif re.search("Run2016(G|H)", nickname):
			self["ElectronTriggerFilterNames"] = [
				"HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v:hltMu23TrkIsoVVLEle12CaloIdLTrackIdLIsoVLElectronlegTrackIsoFilter",
				"HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v:hltMu23TrkIsoVVLEle12CaloIdLTrackIdLIsoVLDZFilter",
				"HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_v:hltMu8TrkIsoVVLEle23CaloIdLTrackIdLIsoVLElectronlegTrackIsoFilter",
				"HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_v:hltMu8TrkIsoVVLEle23CaloIdLTrackIdLIsoVLDZFilter"
			]
			self["MuonTriggerFilterNames"] = [
				"HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v:hltMu23TrkIsoVVLEle12CaloIdLTrackIdLIsoVLMuonlegL3IsoFiltered23",
				"HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v:hltMu23TrkIsoVVLEle12CaloIdLTrackIdLIsoVLDZFilter",
				"HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_v:hltMu8TrkIsoVVLEle23CaloIdLTrackIdLIsoVLMuonlegL3IsoFiltered8",
				"HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_v:hltMu8TrkIsoVVLEle23CaloIdLTrackIdLIsoVLDZFilter"
			]

		self["InvalidateNonMatchingElectrons"] = True
		self["InvalidateNonMatchingMuons"] = True
		self["InvalidateNonMatchingTaus"] = False
		self["InvalidateNonMatchingJets"] = False
		self["DirectIso"] = True
	
		self["OSChargeLeptons"] = True
		self["SvfitKappaParameter"] = 3.0

		self["AddGenMatchedParticles"] = True
		self["BranchGenMatchedElectrons"] = True
		self["BranchGenMatchedMuons"] = True
		self["Consumers"] = [
			"KappaLambdaNtupleConsumer",
			"cutflow_histogram",
			"SvfitCacheConsumer",
			"#CutFlowTreeConsumer",
			"#KappaElectronsConsumer",
			"#KappaMuonsConsumer",
			"#KappaTaggedJetsConsumer",
			"#RunTimeConsumer",
			"#PrintEventsConsumer",
			"#PrintGenParticleDecayTreeConsumer"
		]

		quantities_set = Quantities()
		quantities_set.build_quantities(nickname, channel = self["Channel"])
		self["Quantities"] = list(quantities_set.quantities)

		self.addProcessors(nickname)
