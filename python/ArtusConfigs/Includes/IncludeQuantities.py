# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

#this are functions that return python list, the lists are the same as in the json quantities files. Idea is that one can add the list to the quantities to be read in.


def SingleTauQuantities():
	return [
		"run",
		"lumi",
		"evt",
		"npv",
		"npu",
		"rho",
		"nLooseElectrons",
		"nLooseMuons",
		"nElectrons",
		"nMuons",
		"nTaus",
		"leadingElePt",
		"leadingEleEta",
		"leadingEleIso",
		"leadingEleIsoOverPt",
		"leadingMuonPt",
		"leadingMuonEta",
		"leadingMuonIso",
		"leadingMuonIsoOverPt",
		"leadingTauPt",
		"leadingTauEta",
		"leadingTauIso",
		"leadingTauIsoOverPt",
		"trailingTauPt",
		"trailingTauEta",
		"trailingTauIso",
		"trailingTauIsoOverPt",
		"diTauPt",
		"diTauEta",
		"diTauPhi",
		"diTauMass",
		"diTauSystemReconstructed",
		"weight",
		"collinearMass"
	]

def weightQuantities():
	return [
		"hltWeight",
		"triggerWeight_1",
		"triggerWeight_2",
		"identificationWeight_1",
		"identificationWeight_2",
		"puWeight",
		"tauEnergyScaleWeight",
		"generatorWeight",
		"crossSectionPerEventWeight",
		"numberGeneratedEventsWeight",
		"embeddingWeight",
		"eventWeight",
		"sampleStitchingWeight",
		"antiEVLooseSFWeight_1",
		"antiELooseSFWeight_1",
		"antiEMediumSFWeight_1",
		"antiETightSFWeight_1",
		"antiEVTightSFWeight_1",
		"antiEVLooseSFWeight_2",
		"antiELooseSFWeight_2",
		"antiEMediumSFWeight_2",
		"antiETightSFWeight_2",
		"antiEVTightSFWeight_2",
		"emuQcdWeightUp",
		"emuQcdWeightNom",
		"emuQcdWeightDown",
		"emuQcdOsssWeight",
		"emuQcdOsssRateUpWeight",
		"emuQcdOsssRateDownWeight",
		"emuQcdOsssShapeUpWeight",
		"emuQcdOsssShapeDownWeight"
		"topPtReweightWeight",
		"topPtReweightWeightRun1",
		"topPtReweightWeightRun2",
		"zPtReweightWeight",
		"eleTauFakeRateWeight",
		"muTauFakeRateWeight"
	]

