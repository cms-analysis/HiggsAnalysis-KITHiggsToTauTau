# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import re
import copy
import os

from HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Run2CPFinalStateStudies.quantities import Quantities

# Use mm CP Initial State config as baseline
import HiggsAnalysis.KITHiggsToTauTau.ArtusConfigs.Run2CPStudies.mm as mmbaseconfig

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


class mm_ArtusConfig(mmbaseconfig.mm_ArtusConfig):

	def __init__(self):
		pass

	def addProcessors(self, nickname, legacy):
		super(mm_ArtusConfig, self).addProcessors(nickname, legacy)
		if re.search("Run2017|Summer17|Fall17|Embedding2017", nickname):
			self["Processors"] += ["producer:IsomorphicMappingProducer"]
			self["Processors"] += ["producer:QuantileMappingProducer"]

			if re.search("(DY.?JetsToLL).*(?=(Summer17|Fall17))", nickname):
				self["Processors"] += ["producer:RooWorkspaceWeightProducer"]

	def build_config(self, nickname, *args, **kwargs):

		super(mm_ArtusConfig, self).build_config(nickname, *args, **kwargs)

		datasetsHelper = datasetsHelperTwopz.datasetsHelperTwopz(os.path.expandvars("$CMSSW_BASE/src/Kappa/Skimming/data/datasets.json"))

		isLegacy = kwargs.get("legacy", False)
		isEmbedded = datasetsHelper.isEmbedded(nickname)
		isData = datasetsHelper.isData(nickname) and (not isEmbedded)

		self["UseUWGenMatching"] =  True

		if re.search("Run2017|Summer17|Fall17|Embedding2017", nickname):
			self["HltPaths"] = [
				"HLT_IsoMu24",
				"HLT_IsoMu27",
			]
			self["MuonLowerPtCuts"] = ["21.0"]
			self["HLTBranchNames"] = [
				"trg_singlemuon_24:HLT_IsoMu24_v",
				"trg_singlemuon_27:HLT_IsoMu27_v",
			]

			if isEmbedded:
				self["MuonTriggerFilterNames"] = [
					"HLT_IsoMu24_v:hltL3crIsoL1sSingleMu22L1f0L2f10QL3f24QL3trkIsoFiltered0p07",
					"HLT_IsoMu27_v:hltL3crIsoL1sMu22Or25L1f0L2f10QL3f27QL3trkIsoFiltered0p07",
				]
				self["RequireFiredHlt"] = False
			else:
				self["MuonTriggerFilterNames"] = [
					"HLT_IsoMu24_v:hltL3crIsoL1sSingleMu22L1f0L2f10QL3f24QL3trkIsoFiltered0p07",
					"HLT_IsoMu27_v:hltL3crIsoL1sMu22Or25L1f0L2f10QL3f27QL3trkIsoFiltered0p07",
				]

			self["CheckLepton1TriggerMatch"] = [
				"trg_singlemuon_24",
				"trg_singlemuon_27",
			]

		self["EventWeight"] = "eventWeight"

		if re.search("(Run2017|Summer17|Fall17|Embedding2017)", nickname):
			if isLegacy:
				self["SaveLegacyWeightAsOptionalOnly"] = True
				self["LegacyWeightWorkspace"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/scaleFactorWeights/htt_scalefactors_legacy_2017_IC.root"
				self["LegacyWeightWorkspaceWeightNames"] = [
					"0:trackWeight",
					"0:idisoWeight",
					"0:triggerEfficiency_singletrigger_MCEmb",
					"0:triggerEfficiency_singletrigger_data",
					"1:trackWeight",
					"1:idisoWeight",
				]
				self["LegacyWeightWorkspaceObjectNames"] = [
					"0:m_trk_ratio",
					"0:m_idiso_ic_ratio",
					"0:m_trg_ic_mc",
					"0:m_trg_ic_data",
					"1:m_trk_ratio",
					"1:m_idiso_ic_ratio",
				]
				self["LegacyWeightWorkspaceObjectArguments"] = [
					"0:m_eta",
					"0:m_pt,m_eta",
					"0:m_pt,m_eta",
					"0:m_pt,m_eta",
					"1:m_eta",
					"1:m_pt,m_eta",
				]
				if re.search("(DY.?JetsToLL).*(?=(Summer17|Fall17))", nickname):
					self["RooWorkspace"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/scaleFactorWeights/htt_scalefactors_legacy_2017.root"
					self["RooWorkspaceWeightNames"] = ["0:zPtReweightWeight"]
					self["RooWorkspaceObjectNames"] = ["0:zptmass_weight_nom"]
					self["RooWorkspaceObjectArguments"] = ["0:z_gen_mass,z_gen_pt"]




		quantities_set = Quantities()
		quantities_set.build_quantities(nickname, channel = self["Channel"], legacy=isLegacy)
		quantities_set.quantities.update(self["Quantities"])
		self["Quantities"] = list(quantities_set.quantities)

		self.addProcessors(nickname, isLegacy)
