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
import HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Run2Analysis.Includes.settingsTauES as sTES
import HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Run2Analysis.Includes.settingsJEC as sJEC
import HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Run2Analysis.Includes.settingsJECUncertaintySplit as sJECUS
import HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Run2Analysis.Includes.settingsJER as sJER
import HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Run2Analysis.Includes.settingsSimpleFits as sSimpleFits

import HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Includes.settingsMVATestMethods as sMVATM
import HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Run2CPStudies.Includes.settingsTauPolarisationMva as sTPMVA

from HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Run2Analysis.Includes.idAndTriggerSF import IdAndTriggerSF
import Kappa.Skimming.datasetsHelperTwopz as datasetsHelperTwopz


class tt_ArtusConfig(dict):

	def __init__(self):
		pass

	def addProcessors(self, nickname, legacy):
		self["Processors"] = [
				"producer:HltProducer",
				#"filter:HltFilter",
				"producer:MetSelector",
				"producer:MetSelectorPuppi",
				################## special for each channel in et mt tt em.
				"producer:ValidTausProducer",
				"filter:ValidTausFilter",
				"producer:ValidMuonsProducer",
				"producer:ValidElectronsProducer",
				"producer:TauTriggerMatchingProducer",
				"filter:MinTausCountFilter",
				#"producer:ValidTTPairCandidatesProducer",
				"filter:ValidDiTauPairCandidatesFilter",
				"producer:HttValidLooseElectronsProducer",
				"producer:HttValidLooseMuonsProducer",
				##################
				"producer:Run2DecayChannelProducer",
				"producer:ValidTaggedJetsProducer",
				"producer:ValidBTaggedJetsProducer",
				"producer:TauTauRestFrameSelector",
				"producer:DiLeptonQuantitiesProducer",
				"producer:DiJetQuantitiesProducer",
				]

		if re.search("(Spring16|Summer16|Run2016|Embedding2016|Summer17|Fall17|Run2017|Embedding2017|Autumn18|Run2018|Embedding2018)", nickname):
			self["Processors"] += ["producer:CPInitialStateQuantitiesProducer"] #only DoLhenpNLO for IC samples
			self["Processors"] += ["producer:RefitVertexSelector"]
			self["Processors"] += ["producer:RecoTauCPProducer"]
			self["Processors"] += ["producer:PolarisationQuantitiesSvfitProducer"]
			self["Processors"] += ["producer:PolarisationQuantitiesSvfitM91Producer"]
			self["Processors"] += ["producer:PolarisationQuantitiesSimpleFitProducer"]
			self["Processors"] += ["producer:SimpleFitProducer"]
			self["Processors"] += ["producer:SimpleFitThreeProngThreeProngProducer"]

			self["Processors"] += ["filter:MinimalPlotlevelFilter"]

			# self["Processors"] += ["producer:TaggedJetCorrectionsProducer"]
			self["Processors"] += ["producer:GroupedJetUncertaintyShiftProducer"]
			self["Processors"] += ["producer:SmearedTaggedJetProducer"]

			self["Processors"] += ["producer:HttEventClassifierTmvaReader"]

			if legacy:
				self["Processors"] += ["producer:LegacyJetToTauFakesProducer"]
			else:
				self["Processors"] += ["producer:JetToTauFakesProducer"]

			if re.search("Summer1(6|7)|Fall17|Run201(6|7|8)|Embedding201(6|7|8)|Autumn18", nickname):
				self["Processors"] += ["producer:NewValidTTPairCandidatesProducer"]
				self["Processors"] += ["producer:MetFilterProducer"]
			else:
				self["Processors"] += ["producer:ValidTTPairCandidatesProducer"]

			if re.search("Run201(6|7|8)|Embedding201(6|7|8)", nickname):
				# self["Processors"] += ["producer:MVATestMethodsProducer"]
				# self["Processors"] += ["producer:TauPolarisationTmvaReader"]

				self["Processors"] += ["producer:GenMatchedPolarisationQuantitiesProducer"]

				self["Processors"] += ["producer:SvfitProducer"]
				self["Processors"] += ["producer:FastMttProducer"]
				self["Processors"] += ["producer:SvfitM91Producer"]
				self["Processors"] += ["producer:SvfitM125Producer"]

				# self["Processors"] += ["producer:MELAProducer"]
				# self["Processors"] += ["producer:MELAM125Producer"]

				if re.search("Embedding201(6|7|8)", nickname):
					if legacy:
						self["Processors"] += ["producer:LegacyWeightProducer"]
					else:
						self["Processors"] += ["producer:EmbeddingWeightProducer"]
					self["Processors"] += ["producer:TauCorrectionsProducer"]
					self["Processors"] += ["producer:GenMatchedTauCPProducer"]
					self["Processors"] += ["producer:GenMatchedPolarisationQuantitiesProducer"]

			else:
				self["Processors"] += ["producer:TauCorrectionsProducer"]
				self["Processors"] += ["producer:MetCorrector"]
				self["Processors"] += ["producer:PuppiMetCorrector"]
				self["Processors"] += ["producer:GenMatchedTauCPProducer"]
				self["Processors"] += ["producer:GenMatchedPolarisationQuantitiesProducer"]
				self["Processors"] += ["producer:PileUpJetIDScaleFactorWeightProducer"]
				self["Processors"] += ["producer:TopPtReweightingProducer"]

				# self["Processors"] += [
				# 		"producer:SimpleEleTauFakeRateWeightProducer",
				# 		"producer:SimpleMuTauFakeRateWeightProducer"
				# 		]

				if re.search("Summer17|Fall17", nickname):
					self["Processors"] += ["producer:PrefiringWeightProducer"]
					if legacy:
						self["Processors"] += ["producer:LegacyWeightProducer"]
					else:
						self["Processors"] += ["producer:TauTriggerEfficiency2017Producer"]
						self["Processors"] += ["producer:LeptonTauTrigger2017WeightProducer"]
					# self["Processors"] += ["producer:TriggerWeightProducer"]
					# self["Processors"] += ["producer:IdentificationWeightProducer"]
				else:
					if legacy:
						self["Processors"] += ["producer:LegacyWeightProducer"]
					else:
						self["Processors"] += ["producer:TauTauTriggerWeightProducer"]

				if re.search("(LFV).*(?=(Spring16|Summer16))", nickname):
					self["Processors"] += [
						"producer:ZPtReweightProducer"
						#"filter:MinimalPlotlevelFilter"
					]
					self["Processors"] += ["producer:GenMatchedTauCPProducer"]

				else:
					self["Processors"] += ["producer:SvfitProducer"]
					self["Processors"] += ["producer:FastMttProducer"]
					self["Processors"] += ["producer:SvfitM91Producer"]
					self["Processors"] += ["producer:SvfitM125Producer"]

					# self["Processors"] += ["producer:MELAProducer"]
					# self["Processors"] += ["producer:MELAM125Producer"]

					if re.search("(DY.?JetsToLL).*(?=(Spring16|Summer16|Summer17|Fall17|Autumn18))", nickname):
						if re.search("Summer17|Fall17|Autumn18", nickname) == None:
							self["Processors"] += ["producer:ZPtReweightProducer"]

						self["Processors"] += ["producer:GenSimpleFitProducer"]
						self["Processors"] += ["producer:GenMatchedTauCPProducer"]
						self["Processors"] += ["producer:GenMatchedPolarisationQuantitiesProducer"]
						#self["Processors"] += ["producer:TauPolarisationTmvaReader"]

					elif re.search("(HTo.*TauTau|H2JetsToTauTau|Higgs).*(?=(Spring16|Summer16|Summer17|Fall17|Autumn18))", nickname):
						self["Processors"] += ["producer:GenSimpleFitProducer"]
						#self["Processors"] += ["producer:MVATestMethodsProducer"]
						self["Processors"] += ["producer:GenMatchedTauCPProducer"]
						self["Processors"] += ["producer:GenMatchedPolarisationQuantitiesProducer"]
						#self["Processors"] += ["producer:TauPolarisationTmvaReader"]
						#self["Processors"] += ["producer:MadGraphReweightingProducer"]
					else:
						#self["Processors"] += ["producer:MVATestMethodsProducer"]
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
			self["Processors"] += ["producer:TaggedJetCorrectionsProducer"]

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
				self["Processors"] += ["producer:EleTauFakeRateWeightProducer"]

				if re.search("(DY.?JetsToLL).*(?=Fall15)", nickname):

					self["Processors"] += ["producer:ZPtReweightProducer"]
					#self["Processors"] += ["producer:SimpleFitProducer"]
					self["Processors"] += ["producer:GenMatchedTauCPProducer"]
					self["Processors"] += ["producer:GenMatchedPolarisationQuantitiesProducer"]

				elif re.search("(HTo.*TauTau|H2JetsToTauTau|Higgs).*(?=Fall15)",nickname):
					self["Processors"] += ["producer:SvfitProducer"]
					self["Processors"] += ["producer:FastMttProducer"]
					self["Processors"] += ["producer:SvfitM91Producer"]
					self["Processors"] += ["producer:SvfitM125Producer"]

					# self["Processors"] += ["producer:MELAProducer"]
					# self["Processors"] += ["producer:MELAM125Producer"]

				elif re.search("^((?!(DY.?JetsToLL|HTo.*TauTau|H2JetsToTauTau|Higgs)).)*Fall15", nickname):
					self["Processors"] += ["producer:SvfitProducer"]
					self["Processors"] += ["producer:FastMttProducer"]
					self["Processors"] += ["producer:SvfitM91Producer"]
					self["Processors"] += ["producer:SvfitM125Producer"]

					# self["Processors"] += ["producer:MELAProducer"]
					# self["Processors"] += ["producer:MELAM125Producer"]

		self["Processors"] += ["producer:EventWeightProducer"]

	def build_config(self, nickname, *args, **kwargs):                #Maybe change this the arguments to process/year and DATA/MC

		datasetsHelper = datasetsHelperTwopz.datasetsHelperTwopz(os.path.expandvars("$CMSSW_BASE/src/Kappa/Skimming/data/datasets.json"))

		# define frequently used conditions
		isLegacy = kwargs.get("legacy", False)
		isEmbedded = datasetsHelper.isEmbedded(nickname)
		isData = datasetsHelper.isData(nickname) and (not isEmbedded)

		ElectronID_config = sEID.Electron_ID(nickname, legacy=isLegacy)
		ElectronID_config.looseElectron_ID(nickname) 		#append the config for loose electron ID because it is used
		self.update(ElectronID_config)

		MuonID_config = sMID.Muon_ID(nickname)
		MuonID_config.looseMuon_ID(nickname) 		#append the config for loose Muon ID because it is used
		self.update(MuonID_config)

		TauID_config = sTID.Tau_ID(nickname, legacy=isLegacy)			#here loose is not appended since loose tau ID is not used
		self.update(TauID_config)

		JEC_config = sJEC.JEC(nickname)  #Is allready in baseconfig, for now leave it in; possibly remove it
		self.update(JEC_config)

		JECUncertaintySplit_config = sJECUS.JECUncertaintySplit(nickname)
		self.update(JECUncertaintySplit_config)

		JER_config = sJER.JER(nickname)
		self.update(JER_config)

		JetID_config = sJID.Jet_ID(nickname)
		self.update(JetID_config)

		BTaggedJet_config = sBTJID.BTaggedJet_ID(nickname)
		self.update(BTaggedJet_config)

		Svfit_config = sSvfit.Svfit(nickname)
		self.update(Svfit_config)

		SimpleFits_config = sSimpleFits.SimpleFits(nickname)
		self.update(SimpleFits_config)

		if re.search("VBFHToTauTauM125_RunIIFall17MiniAODv2_PU2017(|newpmx)_13TeV_MINIAOD_powheg-pythia8",nickname) or kwargs.get("sync", False): # synchronization sample
			mplf = sMPlF.MinimalPlotlevelFilter(nickname=nickname, channel="TT", eTauFakeRate=False, sync=True, legacy=isLegacy)
		else:
			mplf = sMPlF.MinimalPlotlevelFilter(nickname=nickname, channel="TT", eTauFakeRate=False, sync=False, legacy=isLegacy)
		self.update(mplf.minPlotLevelDict)

		MVATestMethods_config = sMVATM.MVATestMethods()
		self.update(MVATestMethods_config)

		TauES_config = sTES.TauES(nickname, legacy=isLegacy)
		self.update(TauES_config)

		TauPolarisationMva_config = sTPMVA.TauPolarisationMva()
		self.update(TauPolarisationMva_config)

		self.update(IdAndTriggerSF(nickname, channel="TT", dcach=False))

		self["TauPolarisationTmvaWeights"] = ["/afs/cern.ch/user/m/mfackeld/public/weights_tmva/training.weights.xml",
						"/afs/cern.ch/user/m/mfackeld/public/weights_sklearn/training_tt.weights.xml"]

		self["Channel"] = "TT"
		self["MinNTaus"] = 2

		self["TauLowerPtCuts"] = ["40.0"]
		self["TauUpperAbsEtaCuts"] = ["2.1"]
		self["DiTauPairMinDeltaRCut"] = 0.5
		self["DiTauPairIsTauIsoMVA"] = True
		self["EventWeight"] = "eventWeight"

		if isLegacy:
			if re.search("(Run2016|Summer16|Embedding2016)", nickname):
				self["LegacyWeightWorkspace"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/scaleFactorWeights/htt_scalefactors_legacy_2016_IC.root"
			elif re.search("(Run2017|Summer17|Fall17|Embedding2017)", nickname):
				self["LegacyWeightWorkspace"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/scaleFactorWeights/htt_scalefactors_legacy_2017_IC.root"
			elif re.search("(Run2018|Autumn18|Embedding2018)", nickname):
				self["LegacyWeightWorkspace"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/scaleFactorWeights/htt_scalefactors_legacy_2018_IC.root"

			self["SaveAllLegacyWeightsAsOptionalOnly"] = True
			# self["SaveLegacyWeightAsOptionalOnly"] = True

			if isEmbedded:
				self["LegacyWeightWorkspaceWeightNames"] = [
					"0:weightTauId",
					"1:weightTauId",
					"0:weightTriggerEfficiency_crosstrigger_MCEmb",
					"0:weightTriggerEfficiency_crosstrigger_data",
					"1:weightTriggerEfficiency_crosstrigger_MCEmb",
					"1:weightTriggerEfficiency_crosstrigger_data",
					"0:weightScaleFactor_deepTauVsMuVLoose",
					"1:weightScaleFactor_deepTauVsMuVLoose",
					"0:weightScaleFactor_deepTauVsEleVVLoose",
					"1:weightScaleFactor_deepTauVsEleVVLoose",
				]
				self["LegacyWeightWorkspaceObjectNames"] = [
					"0:t_deeptauid_dm_embed_medium",
					"1:t_deeptauid_dm_embed_medium",
					"0:t_trg_mediumDeepTau_ditau_embed",
					"0:t_trg_mediumDeepTau_ditau_data",
					"1:t_trg_mediumDeepTau_ditau_embed",
					"1:t_trg_mediumDeepTau_ditau_data",
					"0:t_id_vs_mu_eta_vloose",
					"1:t_id_vs_mu_eta_vloose",
					"0:t_id_vs_e_eta_vvloose",
					"1:t_id_vs_e_eta_vvloose",
				]
				self["LegacyWeightWorkspaceObjectArguments"] = [
					"0:t_dm",
					"1:t_dm",
					"0:t_pt,t_eta,t_phi,t_dm",
					"0:t_pt,t_eta,t_phi,t_dm",
					"1:t_pt,t_eta,t_phi,t_dm",
					"1:t_pt,t_eta,t_phi,t_dm",
					"0:t_eta",
					"1:t_eta",
					"0:t_eta",
					"1:t_eta",
				]
				# Add RooWorkspace function for systematics. Triples previous lists and appends nothing (for the nominmal weights), "up" and "down" to each third element
				self["LegacyWeightWorkspaceWeightNames"] += [weight+sys for sys in ["_up", "_down"] for weight in self["LegacyWeightWorkspaceWeightNames"]]
				self["LegacyWeightWorkspaceObjectNames"] += [weight+sys for sys in ["_up", "_down"] for weight in self["LegacyWeightWorkspaceObjectNames"]]
				self["LegacyWeightWorkspaceObjectArguments"] += [weight for sys in ["_up", "_down"] for weight in self["LegacyWeightWorkspaceObjectArguments"]]

				self["LegacyWeightWorkspaceWeightNames"] += [
					"0:weightEmbeddingSelection_id",
					"1:weightEmbeddingSelection_id",
					"0:weightEmbeddingSelection_trigger",
				]
				self["LegacyWeightWorkspaceObjectNames"] += [
					"0:m_sel_id_ic_ratio",
					"1:m_sel_id_ic_ratio",
					"0:m_sel_trg_ic_ratio",
				]
				self["LegacyWeightWorkspaceObjectArguments"] += [
					"0:gt_pt,gt_eta",
					"1:gt_pt,gt_eta",
					"0:gt1_pt,gt1_eta,gt2_pt,gt2_eta",
				]

			else:
				self["LegacyWeightWorkspaceWeightNames"] = [
					"0:weightTauId",
					"1:weightTauId",
					"0:weightTriggerEfficiency_crosstrigger_MCEmb",
					"0:weightTriggerEfficiency_crosstrigger_data",
					"1:weightTriggerEfficiency_crosstrigger_MCEmb",
					"1:weightTriggerEfficiency_crosstrigger_data",
					"0:weightScaleFactor_deepTauVsMuVLoose",
					"1:weightScaleFactor_deepTauVsMuVLoose",
					"0:weightScaleFactor_deepTauVsEleVVLoose",
					"1:weightScaleFactor_deepTauVsEleVVLoose",
				]
				self["LegacyWeightWorkspaceObjectNames"] = [
					"0:t_deeptauid_dm_medium",
					"1:t_deeptauid_dm_medium",
					"0:t_trg_pog_deeptau_medium_ditau_mc",
					"0:t_trg_pog_deeptau_medium_ditau_data",
					"1:t_trg_pog_deeptau_medium_ditau_mc",
					"1:t_trg_pog_deeptau_medium_ditau_data",
					"0:t_id_vs_mu_eta_vloose",
					"1:t_id_vs_mu_eta_vloose",
					"0:t_id_vs_e_eta_vvloose",
					"1:t_id_vs_e_eta_vvloose",
				]
				self["LegacyWeightWorkspaceObjectArguments"] = [
					"0:t_dm",
					"1:t_dm",
					"0:t_pt,t_dm",
					"0:t_pt,t_dm",
					"1:t_pt,t_dm",
					"1:t_pt,t_dm",
					"0:t_eta",
					"1:t_eta",
					"0:t_eta",
					"1:t_eta",
				]
				# Add RooWorkspace function for systematics. Triples previous lists and appends nothing (for the nominmal weights), "up" and "down" to each third element
				self["LegacyWeightWorkspaceWeightNames"] += [weight+sys for sys in ["_up", "_down"] for weight in self["LegacyWeightWorkspaceWeightNames"]]
				self["LegacyWeightWorkspaceObjectNames"] += [weight+sys for sys in ["_up", "_down"] for weight in self["LegacyWeightWorkspaceObjectNames"]]
				self["LegacyWeightWorkspaceObjectArguments"] += [weight for sys in ["_up", "_down"] for weight in self["LegacyWeightWorkspaceObjectArguments"]]

				if re.search("DY.?JetsToLL", nickname):
					self["LegacyWeightWorkspaceWeightNames"].append("0:zPtReweightWeight")
					self["LegacyWeightWorkspaceObjectNames"].append("0:zptmass_weight_nom")
					self["LegacyWeightWorkspaceObjectArguments"].append("0:z_gen_mass,z_gen_pt")

		else:
			if re.search("(Run2017|Summer17|Fall17|Embedding2017)", nickname):
				if isEmbedded:
					self["SaveEmbeddingWeightAsOptionalOnly"] = "true"
					self["EmbeddingWeightWorkspace"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/scaleFactorWeights/htt_scalefactors_v17_6.root"
					self["EmbeddingWeightWorkspaceWeightNames"] = [
						"0:triggerWeight_doublemu",
						"0:idweight_doublemu",
						"1:idweight_doublemu",
						"0:triggerWeight_tau",
						"1:triggerWeight_tau",
					]
					self["EmbeddingWeightWorkspaceObjectNames"] = [
						"0:m_sel_trg_ratio",
						"0:m_sel_idEmb_ratio",
						"1:m_sel_idEmb_ratio",
						"0:tt_emb_PFTau35OR40_tight_kit_ratio",
						"1:tt_emb_PFTau35OR40_tight_kit_ratio",
					]
					self["EmbeddingWeightWorkspaceObjectArguments"] = [
						"0:gt1_pt,gt1_eta,gt2_pt,gt2_eta",
						"0:gt_pt,gt_eta",
						"1:gt_pt,gt_eta",
						"0:t_pt",
						"1:t_pt",
					]

			elif re.search("(Spring16|Summer16|Run2016|Embedding2016)", nickname):
				if isEmbedded:
					self["EmbeddingWeightWorkspace"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/scaleFactorWeights/htt_scalefactors_v16_11_embedded.root"

					self["EmbeddingWeightWorkspaceWeightNames"] = [
						"0:triggerWeight_doublemu",
						"0:triggerWeight_tau",
						"1:triggerWeight_tau"
					]
					self["EmbeddingWeightWorkspaceObjectNames"] = [
						"0:m_sel_trg_ratio",
						"0:t_TightIso_tt_emb_ratio",
						"1:t_TightIso_tt_emb_ratio"
					]
					self["EmbeddingWeightWorkspaceObjectArguments"] = [
						"0:gt1_pt,gt1_eta,gt2_pt,gt2_eta",
						"0:t_pt,t_dm",
						"1:t_pt,t_dm"
					]
				else:
					self["TauTauTriggerWeightWorkspace"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/scaleFactorWeights/htt_scalefactors_sm_moriond_v2.root"

					self["TauTauTriggerWeightWorkspaceWeightNames"] = [
						"0:triggerWeight",
						"1:triggerWeight"
					]
					self["TauTauTriggerWeightWorkspaceObjectNames"] = [
						"0:t_genuine_TightIso_tt_ratio,t_fake_TightIso_tt_ratio",
						"1:t_genuine_TightIso_tt_ratio,t_fake_TightIso_tt_ratio"
					]
					self["TauTauTriggerWeightWorkspaceObjectArguments"] = [
						"0:t_pt,t_dm",
						"1:t_pt,t_dm"
					]
				self["EleTauFakeRateWeightFile"] = [
					"0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/scaleFactorWeights/antiElectronDiscrMVA6FakeRateWeights.root",
					"1:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/scaleFactorWeights/antiElectronDiscrMVA6FakeRateWeights.root"
				]

		if re.search("Run2016|Spring16|Summer16|Embedding2016", nickname):
			#settings for jetstotaufakesproducer
			self["FakeFaktorFile"] = "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/jdegens/higgs-kit/ff/2016/tt/fakeFactors_tt_inclusive.root"
			self["FakeFactorMethod"] = "cp2016"
			self["FakeFactorFractionsRooWorkspaceFile"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/fakeFactorWeights/rooworkspacefractions/ff_fracs_new_2016.root"

		elif re.search("(Run2017|Summer17|Fall17|Embedding2017)", nickname):
			self["FakeFaktorFile"] = "root://grid-cms-xrootd.physik.rwth-aachen.de:1094//store/user/azotz/higgs-kit/ff/2017/tt/fakeFactors.root"
			self["FakeFactorMethod"] = "cp2017"
			self["FakeFactorFractionsRooWorkspaceFile"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/fakeFactorWeights/rooworkspacefractions/ff_fracs_pt_2017.root"

		self["FakeFactorRooWorkspaceFunction"] = [ # valid for both 2016 and 2017
			"w_fracs_1:w_tt_fracs_1",
			"qcd_fracs_1:qcd_tt_fracs_1",
			"ttbar_fracs_1:ttbar_tt_fracs_1",
			"dy_fracs_1:dy_tt_fracs_1",
			"w_fracs_2:w_tt_fracs_2",
			"qcd_fracs_2:qcd_tt_fracs_2",
			"ttbar_fracs_2:ttbar_tt_fracs_2",
			"dy_fracs_2:dy_tt_fracs_2"
		]

		self["TauTauRestFrameReco"] = "collinear_approximation"
		self["TriggerObjectLowerPtCut"] = 28.0
		self["InvalidateNonMatchingElectrons"] = False
		self["InvalidateNonMatchingMuons"] = False
		self["InvalidateNonMatchingTaus"] = True
		self["InvalidateNonMatchingJets"] = False
		self["UseUWGenMatching"] = "true"
		self["DirectIso"] = True
		self["TopPtReweightingStrategy"] = "Run2"

		self["OSChargeLeptons"] = True
		self["SvfitKappaParameter"] = 5.0

		self["AddGenMatchedTaus"] = True
		self["AddGenMatchedTauJets"] = True
		self["BranchGenMatchedTaus"] = True

		self["Consumers"] = [
			"#PrintHltConsumer",
			"KappaLambdaNtupleConsumer",
			"cutflow_histogram",
			"SvfitCacheConsumer"]#,
			#"CutFlowTreeConsumer",
			#"KappaTausConsumer",
			#"KappaTaggedJetsConsumer",
			#"RunTimeConsumer",
			#"PrintEventsConsumer",
			#"PrintGenParticleDecayTreeConsumer"]

		# if re.search("Embedding", nickname):
		# 	self["NoHltFiltering"]= True
		# 	self["DiTauPairNoHLT"]= True
		# else:
		# 	self["NoHltFiltering"]= False
		# 	self["DiTauPairNoHLT"]= True

		 #set it here and if it is something else then change it in the ifs below
		self["HltPaths"] = ["HLT_DoubleMediumIsoPFTau35_Trk1_eta2p1_Reg", "HLT_DoubleMediumCombinedIsoPFTau35_Trk1_eta2p1_Reg"]
		self["TauTriggerFilterNames"] = [
			"HLT_DoubleMediumIsoPFTau35_Trk1_eta2p1_Reg_v:hltDoublePFTau35TrackPt1MediumIsolationDz02Reg",
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

		elif "Embedding2016" in nickname or "EmbeddingMC" in nickname:
			self["HltPaths"] = ["HLT_DoubleMediumIsoPFTau35_Trk1_eta2p1_Reg_v"]
			self["TauTriggerFilterNames"] = ["HLT_DoubleMediumIsoPFTau35_Trk1_eta2p1_Reg_v:hltDoublePFTau35Reg"]

		elif re.search("Run2017|Summer17|Fall17|Embedding2017", nickname):
			self["HltPaths"] = ["HLT_DoubleTightChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg", "HLT_DoubleMediumChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg", "HLT_DoubleTightChargedIsoPFTau40_Trk1_eta2p1_Reg"]
			if isEmbedded:
				self["TauTriggerFilterNames"] = [
					"HLT_DoubleTightChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg_v:hltDoubleL2IsoTau26eta2p2",
					"HLT_DoubleMediumChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg_v:hltDoubleL2IsoTau26eta2p2",
					"HLT_DoubleTightChargedIsoPFTau40_Trk1_eta2p1_Reg_v:hltDoubleL2IsoTau26eta2p2"
				]
				self["RequireFiredHlt"] = False
			else:
				self["TauTriggerFilterNames"] = [
					"HLT_DoubleTightChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg_v:hltDoublePFTau35TrackPt1TightChargedIsolationAndTightOOSCPhotonsDz02Reg", #here are : in string
					"HLT_DoubleMediumChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg_v:hltDoublePFTau40TrackPt1MediumChargedIsolationAndTightOOSCPhotonsDz02Reg",
					"HLT_DoubleTightChargedIsoPFTau40_Trk1_eta2p1_Reg_v:hltDoublePFTau40TrackPt1TightChargedIsolationDz02Reg"
				]

			self["TauTriggerCheckL1Match"] = [
				"HLT_DoubleTightChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg_v",
				"HLT_DoubleMediumChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg_v",
				"HLT_DoubleTightChargedIsoPFTau40_Trk1_eta2p1_Reg_v"
			]

			self["HLTBranchNames"] = [
				"trg_doubletau_35_tightiso_tightid:HLT_DoubleTightChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg",
				"trg_doubletau_40_mediso_tightid:HLT_DoubleMediumChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg",
				"trg_doubletau_40_tightiso:HLT_DoubleTightChargedIsoPFTau40_Trk1_eta2p1_Reg"
			]

			self["CheckL1MatchForDiTauPairLepton1"] = True
			self["CheckL1MatchForDiTauPairLepton2"] = True

			self["DiTauPairLepton1LowerPtCuts"] = [
				# "HLT_DoubleMediumChargedIsoPFTau35_Trk1_eta2p1_Reg_v:40.0",
				"HLT_DoubleTightChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg_v:40.0",
				"HLT_DoubleMediumChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg_v:45.0",
				"HLT_DoubleTightChargedIsoPFTau40_Trk1_eta2p1_Reg_v:45.0",
				]

			self["DiTauPairLepton2LowerPtCuts"] = [
				# "HLT_DoubleMediumChargedIsoPFTau35_Trk1_eta2p1_Reg_v:40.0",
				"HLT_DoubleTightChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg_v:40.0",
				"HLT_DoubleMediumChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg_v:45.0",
				"HLT_DoubleTightChargedIsoPFTau40_Trk1_eta2p1_Reg_v:45.0",
				]

			self["CheckLepton1TriggerMatch"] = [
				"trg_doubletau_35_tightiso_tightid",
				"trg_doubletau_40_mediso_tightid",
				"trg_doubletau_40_tightiso",
				]

			self["CheckLepton2TriggerMatch"] = [
				"trg_doubletau_35_tightiso_tightid",
				"trg_doubletau_40_mediso_tightid",
				"trg_doubletau_40_tightiso",
				]

		elif re.search("Run2018|Autumn18|Embedding2018", nickname):
			self["HltPaths"] = [
				"HLT_DoubleMediumChargedIsoPFTauHPS35_Trk1_eta2p1_Reg"
				]
			self["HLTBranchNames"] = [
				"trg_doubletau_35_mediso:HLT_DoubleMediumChargedIsoPFTauHPS35_Trk1_eta2p1_Reg"
			]
			if re.search("Run2018|Autumn18", nickname):
				self["TauTriggerFilterNames"] = [
					"HLT_DoubleMediumChargedIsoPFTauHPS35_Trk1_eta2p1_Reg_v:hltHpsDoublePFTau35TrackPt1MediumChargedIsolationDz02Reg"
				]
				if re.search("Run2018", nickname):
					self["HltPaths"] += [
						"HLT_DoubleTightChargedIsoPFTau40_Trk1_eta2p1_Reg",
						"HLT_DoubleMediumChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg",
						"HLT_DoubleTightChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg",
						]
					self["HLTBranchNames"] += [
						"trg_doubletau_40_tightiso:HLT_DoubleTightChargedIsoPFTau40_Trk1_eta2p1_Reg",
						"trg_doubletau_40_mediso_tightid:HLT_DoubleMediumChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg",
						"trg_doubletau_35_tightiso_tightid:HLT_DoubleTightChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg",
					]
					self["TauTriggerFilterNames"] += [
						"HLT_DoubleTightChargedIsoPFTau40_Trk1_eta2p1_Reg_v:hltDoublePFTau40TrackPt1TightChargedIsolationDz02Reg",
						"HLT_DoubleMediumChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg_v:hltDoublePFTau40TrackPt1MediumChargedIsolationAndTightOOSCPhotonsDz02Reg",
						"HLT_DoubleTightChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg_v:hltDoublePFTau35TrackPt1TightChargedIsolationAndTightOOSCPhotonsDz02Reg",
					]

					self["DiTauPairLepton1LowerRunNumberCuts"] = [
						"hltHpsDoublePFTau35TrackPt1MediumChargedIsolationDz02Reg:317509",
					]
					self["DiTauPairLepton1UpperRunNumberCuts"] = [
						"hltDoublePFTau40TrackPt1TightChargedIsolationDz02Reg:317509",
						"hltDoublePFTau40TrackPt1MediumChargedIsolationAndTightOOSCPhotonsDz02Reg:317509",
						"hltDoublePFTau35TrackPt1TightChargedIsolationAndTightOOSCPhotonsDz02Reg:317509",
					]
					self["DiTauPairLepton2LowerRunNumberCuts"] = [
						"hltHpsDoublePFTau35TrackPt1MediumChargedIsolationDz02Reg:317509",
					]
					self["DiTauPairLepton2UpperRunNumberCuts"] = [
						"hltDoublePFTau40TrackPt1TightChargedIsolationDz02Reg:317509",
						"hltDoublePFTau40TrackPt1MediumChargedIsolationAndTightOOSCPhotonsDz02Reg:317509",
						"hltDoublePFTau35TrackPt1TightChargedIsolationAndTightOOSCPhotonsDz02Reg:317509",
					]

			elif re.search("Embedding2018", nickname):
				self["TauTriggerFilterNames"] = [
					"HLT_DoubleMediumChargedIsoPFTauHPS35_Trk1_eta2p1_Reg_v:hltDoubleL2IsoTau26eta2p2"
				]
				self["RequireFiredHlt"] = False

			self["DiTauPairLepton1LowerPtCuts"] = [
				"HLT_DoubleTightChargedIsoPFTau40_Trk1_eta2p1_Reg_v:45.0",
				"HLT_DoubleMediumChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg_v:45.0",
				"HLT_DoubleTightChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg_v:40.0",
				"HLT_DoubleMediumChargedIsoPFTauHPS35_Trk1_eta2p1_Reg_v:40.0",
			]
			self["DiTauPairLepton2LowerPtCuts"] = [
				"HLT_DoubleTightChargedIsoPFTau40_Trk1_eta2p1_Reg_v:45.0",
				"HLT_DoubleMediumChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg_v:45.0",
				"HLT_DoubleTightChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg_v:40.0",
				"HLT_DoubleMediumChargedIsoPFTauHPS35_Trk1_eta2p1_Reg_v:40.0",
			]

			self["CheckLepton1TriggerMatch"] = [
				"trg_doubletau_35_tightiso_tightid",
				"trg_doubletau_40_mediso_tightid",
				"trg_doubletau_40_tightiso",
				"trg_doubletau_35_mediso"
				]
			self["CheckLepton2TriggerMatch"] = [
				"trg_doubletau_35_tightiso_tightid",
				"trg_doubletau_40_mediso_tightid",
				"trg_doubletau_40_tightiso",
				"trg_doubletau_35_mediso"
				]

			self["CheckL1MatchForDiTauPairLepton1"] = True
			self["CheckL1MatchForDiTauPairLepton2"] = True

		quantities_set = Quantities()
		quantities_set.build_quantities(nickname, channel = self["Channel"], legacy=isLegacy)
		self["Quantities"] = list(quantities_set.quantities)

		self.addProcessors(nickname, isLegacy)
