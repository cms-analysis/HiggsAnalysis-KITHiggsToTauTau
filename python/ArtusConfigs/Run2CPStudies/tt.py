# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import re
import copy

import HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Run2CPStudies.CPQuantities as quantities
import HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Includes.processorOrdering as processorOrdering

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


class tt_ArtusConfig(dict):

	def __init__(self):
		pass	

	def build_config(self, nickname, *args, **kwargs):                #Maybe change this the arguments to process/year and DATA/MC
		
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
		self["TauLowerPtCuts"] = ["40.0"]  #in json with default
		self["TauUpperAbsEtaCuts"] = ["2.1"] #in json with default
		self["DiTauPairMinDeltaRCut"] = 0.5
		self["DiTauPairIsTauIsoMVA"] = True
		self["EventWeight"] = "eventWeight"
		self["RooWorkspace"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/scaleFactorWeights/htt_scalefactors_sm_moriond_v2.root"
		self["TauTauTriggerWeightWorkspace"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/scaleFactorWeights/htt_scalefactors_sm_moriond_v2.root"

		self["TauTauTriggerWeightWorkspaceWeightNames"] = ["0:triggerWeight", "1:triggerWeight"]
		self["TauTauTriggerWeightWorkspaceObjectNames"] = ["0:t_genuine_TightIso_tt_ratio,t_fake_TightIso_tt_ratio", "1:t_genuine_TightIso_tt_ratio,t_fake_TightIso_tt_ratio"]
		self["TauTauTriggerWeightWorkspaceObjectArguments"] = ["0:t_pt,t_dm","1:t_pt,t_dm"]
		self["EleTauFakeRateWeightFile"] = [
			"0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/scaleFactorWeights/antiElectronDiscrMVA6FakeRateWeights.root",
			"1:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/scaleFactorWeights/antiElectronDiscrMVA6FakeRateWeights.root"
		]
		
		self["TauTauRestFrameReco"] = "collinear_approximation"
		self["TriggerObjectLowerPtCut"] = 28.0
		self["InvalidateNonMatchingElectrons"] = False
		self["InvalidateNonMatchingMuons"] = False
		self["InvalidateNonMatchingTaus"] = True
		self["InvalidateNonMatchingJets"] = False
		self["UseUWGenMatching"] = "true"                   #TODO change this to boolean? or change the rest to string?
		self["DirectIso"] = True
		self["TopPtReweightingStrategy"] = "Run1"

		self["OSChargeLeptons"] = True
		self["SvfitKappaParameter"] = 5.0

		self["AddGenMatchedTaus"] = True
		self["AddGenMatchedTauJets"] = True
		self["BranchGenMatchedTaus"] = True

		self["Consumers"] = ["KappaLambdaNtupleConsumer",
			"cutflow_histogram",
			"SvfitCacheConsumer"]#,
			#"CutFlowTreeConsumer",
			#"KappaTausConsumer",
			#"KappaTaggedJetsConsumer",
			#"RunTimeConsumer",
			#"PrintEventsConsumer",
			#"PrintGenParticleDecayTreeConsumer"]

		if re.search("Embedding", nickname):
			self["NoHltFiltering"]= True
			self["DiTauPairNoHLT"]= True
		else:
			self["NoHltFiltering"]=False
			self["DiTauPairNoHLT"]= False	
		
		 #set it here and if it is something else then change it in the ifs below
		self["HltPaths"] = ["HLT_DoubleMediumIsoPFTau35_Trk1_eta2p1_Reg", "HLT_DoubleMediumCombinedIsoPFTau35_Trk1_eta2p1_Reg"]
		self["TauTriggerFilterNames"] = [
			"HLT_DoubleMediumIsoPFTau35_Trk1_eta2p1_Reg_v:hltDoublePFTau35TrackPt1MediumIsolationDz02Reg",   #here are : in string
			"HLT_DoubleMediumCombinedIsoPFTau35_Trk1_eta2p1_Reg_v:hltDoublePFTau35TrackPt1MediumCombinedIsolationDz02Reg"
		]

		if "Run2016" in nickname and not "Run2016H" in nickname:
			self["HltPaths"] = ["HLT_DoubleMediumIsoPFTau35_Trk1_eta2p1_Reg"]
			self["TauTriggerFilterNames"]=["HLT_DoubleMediumIsoPFTau35_Trk1_eta2p1_Reg_v:hltDoublePFTau35TrackPt1MediumIsolationDz02Reg"]


		elif "Run2016H" in nickname:
			self["HltPaths"] = ["HLT_DoubleMediumCombinedIsoPFTau35_Trk1_eta2p1_Reg"]
			self["TauTriggerFilterNames"] = ["HLT_DoubleMediumCombinedIsoPFTau35_Trk1_eta2p1_Reg_v:hltDoublePFTau35TrackPt1MediumCombinedIsolationDz02Reg"]

		elif "Fall15MiniAODv2" in nickname or "Run2015D" in nickname or "Embedding2015" in nickname:
			self["HltPaths"] = ["HLT_DoubleMediumIsoPFTau35_Trk1_eta2p1_Reg"]
			self["TauTriggerFilterNames"] = ["HLT_DoubleMediumIsoPFTau35_Trk1_eta2p1_Reg_v:hltDoublePFTau35TrackPt1MediumIsolationDz02Reg"]

		elif "Embedding2016" in nickname or "EmbeddingMC" in nickname:	 #TODO Ask thomas what it should be line 40 in json
			self["HltPaths"] = [""]

		#Quantities, this looks for tt em mt et very similar, check if it is the same and if so put it in baseconfig for all channels
		quantities_dict = quantities.quantities() 
		quantities_dict.build_quantities(nickname, channel = self["Channel"])

		#put rest of quantities in CPQuantities.py?

		quantities_dict["Quantities"] += [
						"nLooseElectrons", 
						"nLooseMuons",
						"nDiTauPairCandidates",
						 "nAllDiTauPairCandidates"
					]
		if re.search("(DY.?JetsToLL).*(?=(Spring16|Summer16))", nickname):
			quantities_dict["Quantities"] += quantities_dict.genQuantities()
			quantities_dict["Quantities"] += quantities_dict.lheWeightsDYQuantities()
			quantities_dict["Quantities"] += [
				"tauSpinnerValidOutputs",
				"tauSpinnerPolarisation",
			]
		elif re.search("(DY.?JetsToLL).*(?=Fall15)", nickname):
			quantities_dict["Quantities"] += [
				"tauSpinnerValidOutputs",
				"tauSpinnerPolarisation",
			]
		elif re.search("(DY.?JetsToLL).*(?=Fall15)", nickname):
			quantities_dict["Quantities"] += quantities_dict.genMatchedCPQuantities()
		elif re.search("Embedding2016", nickname):
			quantities_dict["Quantities"] += [
				"tauSpinnerValidOutputs",
				"tauSpinnerPolarisation",
			]
		
		self.update(copy.deepcopy(quantities_dict))

		#Producers and filters, TODO filter everything which is the same and use this as the startint list, then just add the other variables per sample

		self["Processors"] = [
				"producer:HltProducer",
				"filter:HltFilter",
				"producer:MetSelector",
				################## special for each channel in et mt tt em.
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
				##################
				"producer:Run2DecayChannelProducer",          
				"producer:TaggedJetCorrectionsProducer",
				"producer:ValidTaggedJetsProducer",
				"producer:ValidBTaggedJetsProducer",	
				"producer:TauTauRestFrameSelector",
				"producer:DiLeptonQuantitiesProducer",
				"producer:DiJetQuantitiesProducer",
				
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
				self["Processors"] += ["producer:TauCorrectionsProducer"]
				self["Processors"] += ["producer:TauTauTriggerWeightProducer"]
				self["Processors"] += ["producer:MetCorrector"]
				self["Processors"] += [
						"producer:SimpleEleTauFakeRateWeightProducer",
						"producer:SimpleMuTauFakeRateWeightProducer"
						]
			
				if re.search("(LFV).*(?=(Spring16|Summer16))", nickname):
					self["Processors"] += [
						"producer:ZPtReweightProducer"
						#"filter:MinimalPlotlevelFilter"
					]
					self["Processors"] += ["producer:GenMatchedTauCPProducer"]

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
						self["Processors"] += ["producer:GenMatchedPolarisationQuantitiesProducer"]
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
				self["Processors"] += [
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
		processorOrderingkey = processorOrdering.processors_ordered(channel = self["Channel"])
		ordered_processors = processorOrderingkey.order_processors(self["Processors"]) 
		self["Processors"] = copy.deepcopy(ordered_processors)
		#processorOrderingkey.get_demon_processor(self["Processors"])


