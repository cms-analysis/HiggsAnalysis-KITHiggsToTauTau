
#pragma once

#include <limits.h>

#include "Artus/KappaAnalysis/interface/KappaSettings.h"

/**
   \brief Reads settings for all parts of the KappaAnalysis code from a prepared
   json configuration file.

   Defines settings that can be obtained from the json configuration file.
*/

class HttSettings: public KappaSettings {
public:

	/// names of (old) MVA MET collection in kappa tuple
	IMPL_SETTING_DEFAULT(std::string, MvaMetTT, "");
	IMPL_SETTING_DEFAULT(std::string, MvaMetMT, "");
	IMPL_SETTING_DEFAULT(std::string, MvaMetET, "");
	IMPL_SETTING_DEFAULT(std::string, MvaMetEM, "");

	/// names of (new) MVA MET collection in kappa tuple
	IMPL_SETTING_DEFAULT(std::string, MvaMetsTT, "");
	IMPL_SETTING_DEFAULT(std::string, MvaMetsMT, "");
	IMPL_SETTING_DEFAULT(std::string, MvaMetsET, "");
	IMPL_SETTING_DEFAULT(std::string, MvaMetsEM, "");
	IMPL_SETTING_DEFAULT(std::string, MvaMets, "");

	/// htt decay channel and event category
	IMPL_SETTING_DEFAULT(std::string, Channel, "");
	IMPL_SETTING_DEFAULT(std::string, Category, "");

	IMPL_SETTING(bool, OSChargeLeptons);

	IMPL_SETTING(std::string, MetRecoilCorrectorFile);
	IMPL_SETTING(std::string, MvaMetRecoilCorrectorFile);
	IMPL_SETTING(std::string, MetShiftCorrectorFile);
	IMPL_SETTING(std::string, MvaMetShiftCorrectorFile);
	IMPL_SETTING_DEFAULT(std::string, MetCorrectionMethod, "quantileMapping");

	IMPL_SETTING_DEFAULT(bool, ChooseMvaMet, true);
	IMPL_SETTING_DEFAULT(bool, UpdateMetWithCorrectedLeptons, false);
	IMPL_SETTING_DEFAULT(int, MetSysType, 0);
	IMPL_SETTING_DEFAULT(int, MetSysShift, 0);

	IMPL_SETTING_DEFAULT(bool, MetUncertaintyShift, false);
	IMPL_SETTING_DEFAULT(std::string, MetUncertaintyType, "");

	IMPL_SETTING_STRINGLIST_DEFAULT(PlotlevelFilterExpressionQuantities, {});
	IMPL_SETTING_DEFAULT(std::string, PlotlevelFilterExpression, "");

	IMPL_SETTING_STRINGLIST_DEFAULT(TriggerEfficiencyData, {});
	IMPL_SETTING_STRINGLIST_DEFAULT(TriggerEfficiencyMc, {});
	IMPL_SETTING_DEFAULT(std::string, TriggerEfficiencyHistogram, "triggerEfficiency");
	IMPL_SETTING_DEFAULT(std::string, TriggerEfficiencyMode, "multiply_weights");

	IMPL_SETTING_STRINGLIST_DEFAULT(IdentificationEfficiencyData, {});
	IMPL_SETTING_STRINGLIST_DEFAULT(IdentificationEfficiencyMc, {});
	IMPL_SETTING_DEFAULT(std::string, IdentificationEfficiencyHistogram, "identificationEfficiency");
	IMPL_SETTING_DEFAULT(std::string, IdentificationEfficiencyMode, "multiply_weights");

	std::vector<std::string> EleTauFakeRateHistograms = {"antiEVLoose", "antiELoose", "antiEMedium", "antiETight", "antiEVTight"};
	IMPL_SETTING_STRINGLIST(EleTauFakeRateWeightFile);
	IMPL_SETTING_STRINGLIST_DEFAULT(EleTauFakeRateHistograms, EleTauFakeRateHistograms);
	IMPL_SETTING_STRINGLIST(MuonTauFakeRateWeightFile);
	IMPL_SETTING_STRINGLIST_DEFAULT(MuonTauFakeRateHistograms, {});

	IMPL_SETTING(std::string, ElectronIDType);
	IMPL_SETTING_DEFAULT(std::string, ElectronIDName, "");
	IMPL_SETTING_STRINGLIST_DEFAULT(ElectronIDList, {});
	IMPL_SETTING_DEFAULT(float, ElectronMvaIDCutEB1, -1.0);
	IMPL_SETTING_DEFAULT(float, ElectronMvaIDCutEB2, -1.0);
	IMPL_SETTING_DEFAULT(float, ElectronMvaIDCutEE, -1.0);

	IMPL_SETTING_DEFAULT(float, ElectronChargedIsoVetoConeSizeEB, 0.0);
	IMPL_SETTING_DEFAULT(float, ElectronChargedIsoVetoConeSizeEE, 0.0);
	IMPL_SETTING_DEFAULT(float, ElectronNeutralIsoVetoConeSize, 0.0);
	IMPL_SETTING_DEFAULT(float, ElectronPhotonIsoVetoConeSizeEB, 0.0);
	IMPL_SETTING_DEFAULT(float, ElectronPhotonIsoVetoConeSizeEE, 0.0);
	IMPL_SETTING_DEFAULT(float, ElectronDeltaBetaIsoVetoConeSize, 0.0);

	IMPL_SETTING_DEFAULT(float, ElectronChargedIsoPtThreshold, 0.0);
	IMPL_SETTING_DEFAULT(float, ElectronNeutralIsoPtThreshold, 0.0);
	IMPL_SETTING_DEFAULT(float, ElectronPhotonIsoPtThreshold, 0.0);
	IMPL_SETTING_DEFAULT(float, ElectronDeltaBetaIsoPtThreshold, 0.0);

	IMPL_SETTING(float, ElectronIsoSignalConeSize);
	IMPL_SETTING(float, ElectronDeltaBetaCorrectionFactor);
	IMPL_SETTING_DEFAULT(float, ElectronIsoPtSumOverPtLowerThresholdEB, -1.0);
	IMPL_SETTING_DEFAULT(float, ElectronIsoPtSumOverPtLowerThresholdEE, -1.0);
	IMPL_SETTING_DEFAULT(float, ElectronIsoPtSumOverPtUpperThresholdEB, std::numeric_limits<float>::max());
	IMPL_SETTING_DEFAULT(float, ElectronIsoPtSumOverPtUpperThresholdEE, std::numeric_limits<float>::max());

	IMPL_SETTING_DEFAULT(float, MuonChargedIsoVetoConeSize, 0.0);
	IMPL_SETTING_DEFAULT(float, MuonNeutralIsoVetoConeSize, 0.0);
	IMPL_SETTING_DEFAULT(float, MuonPhotonIsoVetoConeSize, 0.0);
	IMPL_SETTING_DEFAULT(float, MuonDeltaBetaIsoVetoConeSize, 0.0);

	IMPL_SETTING_DEFAULT(float, MuonChargedIsoPtThreshold, 0.0);
	IMPL_SETTING_DEFAULT(float, MuonNeutralIsoPtThreshold, 0.0);
	IMPL_SETTING_DEFAULT(float, MuonPhotonIsoPtThreshold, 0.0);
	IMPL_SETTING_DEFAULT(float, MuonDeltaBetaIsoPtThreshold, 0.0);

	IMPL_SETTING(float, MuonIsoSignalConeSize);
	IMPL_SETTING(float, MuonDeltaBetaCorrectionFactor);
	IMPL_SETTING_DEFAULT(float, MuonIsoPtSumOverPtLowerThresholdEB, -1.0);
	IMPL_SETTING_DEFAULT(float, MuonIsoPtSumOverPtLowerThresholdEE, -1.0);
	IMPL_SETTING_DEFAULT(float, MuonIsoPtSumOverPtUpperThresholdEB, std::numeric_limits<float>::max());
	IMPL_SETTING_DEFAULT(float, MuonIsoPtSumOverPtUpperThresholdEE, std::numeric_limits<float>::max());

	IMPL_SETTING_DEFAULT(float, ElectronTrackDxyCut, -1.0);
	IMPL_SETTING_DEFAULT(float, ElectronTrackDzCut, -1.0);
	IMPL_SETTING_DEFAULT(float, MuonTrackDxyCut, -1.0);
	IMPL_SETTING_DEFAULT(float, MuonTrackDzCut, -1.0);
	IMPL_SETTING_DEFAULT(float, TauTrackDzCut, -1.0);

	IMPL_SETTING(std::string, LooseElectronID);
	IMPL_SETTING(std::string, LooseElectronIDType);
	IMPL_SETTING_DEFAULT(std::string, LooseElectronIDName, "");
	IMPL_SETTING_DEFAULT(float, LooseElectronMvaIDCutEB1, -1.0);
	IMPL_SETTING_DEFAULT(float, LooseElectronMvaIDCutEB2, -1.0);
	IMPL_SETTING_DEFAULT(float, LooseElectronMvaIDCutEE, -1.0);
	IMPL_SETTING(std::string, LooseElectronReco);
	IMPL_SETTING(std::string, LooseMuonID);

	IMPL_SETTING(std::string, LooseElectronIsoType);
	IMPL_SETTING(std::string, LooseElectronIso);
	IMPL_SETTING_DEFAULT(float, LooseElectronIsoPtSumOverPtLowerThresholdEB, -1.0);
	IMPL_SETTING_DEFAULT(float, LooseElectronIsoPtSumOverPtLowerThresholdEE, -1.0);
	IMPL_SETTING_DEFAULT(float, LooseElectronIsoPtSumOverPtUpperThresholdEB, std::numeric_limits<float>::max());
	IMPL_SETTING_DEFAULT(float, LooseElectronIsoPtSumOverPtUpperThresholdEE, std::numeric_limits<float>::max());
	IMPL_SETTING(std::string, LooseMuonIsoType);
	IMPL_SETTING(std::string, LooseMuonIso);
	IMPL_SETTING_DEFAULT(float, LooseMuonIsoPtSumOverPtLowerThresholdEB, -1.0);
	IMPL_SETTING_DEFAULT(float, LooseMuonIsoPtSumOverPtLowerThresholdEE, -1.0);
	IMPL_SETTING_DEFAULT(float, LooseMuonIsoPtSumOverPtUpperThresholdEB, std::numeric_limits<float>::max());
	IMPL_SETTING_DEFAULT(float, LooseMuonIsoPtSumOverPtUpperThresholdEE, std::numeric_limits<float>::max());

	IMPL_SETTING_DEFAULT(std::string, MuonIsoTypeUserMode, "fromcmssw");

	IMPL_SETTING_DEFAULT(float, LooseElectronTrackDxyCut, -1.0);
	IMPL_SETTING_DEFAULT(float, LooseElectronTrackDzCut, -1.0);
	IMPL_SETTING_DEFAULT(float, LooseMuonTrackDxyCut, -1.0);
	IMPL_SETTING_DEFAULT(float, LooseMuonTrackDzCut, -1.0);

	IMPL_SETTING_STRINGLIST_DEFAULT(LooseElectronLowerPtCuts, {});
	IMPL_SETTING_STRINGLIST_DEFAULT(LooseMuonLowerPtCuts, {});
	IMPL_SETTING_STRINGLIST_DEFAULT(LooseElectronUpperAbsEtaCuts, {});
	IMPL_SETTING_STRINGLIST_DEFAULT(LooseMuonUpperAbsEtaCuts, {});

	IMPL_SETTING(std::string, VetoElectronID);
	IMPL_SETTING(std::string, VetoElectronIDType);
	IMPL_SETTING_DEFAULT(std::string, VetoElectronIDName, "");
	IMPL_SETTING_DEFAULT(float, VetoElectronMvaIDCutEB1, -1.0);
	IMPL_SETTING_DEFAULT(float, VetoElectronMvaIDCutEB2, -1.0);
	IMPL_SETTING_DEFAULT(float, VetoElectronMvaIDCutEE, -1.0);
	IMPL_SETTING(std::string, VetoElectronReco);
	IMPL_SETTING(std::string, VetoMuonID);

	IMPL_SETTING(std::string, VetoElectronIsoType);
	IMPL_SETTING(std::string, VetoElectronIso);
	IMPL_SETTING_DEFAULT(float, VetoElectronIsoPtSumOverPtLowerThresholdEB, -1.0);
	IMPL_SETTING_DEFAULT(float, VetoElectronIsoPtSumOverPtLowerThresholdEE, -1.0);
	IMPL_SETTING_DEFAULT(float, VetoElectronIsoPtSumOverPtUpperThresholdEB, std::numeric_limits<float>::max());
	IMPL_SETTING_DEFAULT(float, VetoElectronIsoPtSumOverPtUpperThresholdEE, std::numeric_limits<float>::max());
	IMPL_SETTING(std::string, VetoMuonIsoType);
	IMPL_SETTING(std::string, VetoMuonIso);
	IMPL_SETTING_DEFAULT(float, VetoMuonIsoPtSumOverPtLowerThresholdEB, -1.0);
	IMPL_SETTING_DEFAULT(float, VetoMuonIsoPtSumOverPtLowerThresholdEE, -1.0);
	IMPL_SETTING_DEFAULT(float, VetoMuonIsoPtSumOverPtUpperThresholdEB, std::numeric_limits<float>::max());
	IMPL_SETTING_DEFAULT(float, VetoMuonIsoPtSumOverPtUpperThresholdEE, std::numeric_limits<float>::max());

	IMPL_SETTING_STRINGLIST_DEFAULT(VetoElectronLowerPtCuts, {});
	IMPL_SETTING_STRINGLIST_DEFAULT(VetoMuonLowerPtCuts, {});
	IMPL_SETTING_STRINGLIST_DEFAULT(VetoElectronUpperAbsEtaCuts, {});
	IMPL_SETTING_STRINGLIST_DEFAULT(VetoMuonUpperAbsEtaCuts, {});

	IMPL_SETTING(std::string, DiVetoElectronVetoMode);
	IMPL_SETTING_DEFAULT(float, DiVetoElectronMinDeltaRCut, -1.0);

	IMPL_SETTING(std::string, DiVetoMuonVetoMode);
	IMPL_SETTING_DEFAULT(float, DiVetoMuonMinDeltaRCut, -1.0);

	IMPL_SETTING_DEFAULT(std::string, ElectronEnergyCorrection, "none");
	IMPL_SETTING_DEFAULT(float, ElectronEnergyCorrectionShift, 1.0);
	IMPL_SETTING_DEFAULT(float, ElectronEnergyCorrectionShiftEB, 1.0);
	IMPL_SETTING_DEFAULT(float, ElectronEnergyCorrectionShiftEE, 1.0);
	IMPL_SETTING_DEFAULT(float, MuonEnergyCorrectionShift, 1.0);
	IMPL_SETTING_DEFAULT(float, RandomMuonEnergySmearing, 0.0);
	IMPL_SETTING_DEFAULT(float, RandomTauEnergySmearing, 0.0);
	IMPL_SETTING_DEFAULT(std::string, TauEnergyCorrection, "none");
	IMPL_SETTING_DEFAULT(float, TauEnergyCorrectionOneProng, 1.0);
	IMPL_SETTING_DEFAULT(float, TauEnergyCorrectionOneProngPiZeros, 1.0);
	IMPL_SETTING_DEFAULT(float, TauEnergyCorrectionThreeProng, 1.0);
	IMPL_SETTING_DEFAULT(float, TauEnergyCorrectionShift, 1.0);
	IMPL_SETTING_DEFAULT(float, TauEnergyCorrectionOneProngShift, 1.0);
	IMPL_SETTING_DEFAULT(float, TauEnergyCorrectionOneProngPiZerosShift, 1.0);
	IMPL_SETTING_DEFAULT(float, TauEnergyCorrectionThreeProngShift, 1.0);
	IMPL_SETTING_DEFAULT(float, TauElectronFakeEnergyCorrectionOneProng, 1.0);
	IMPL_SETTING_DEFAULT(float, TauElectronFakeEnergyCorrectionOneProngPiZeros, 1.0);
	IMPL_SETTING_DEFAULT(float, TauElectronFakeEnergyCorrectionThreeProng, 1.0);
	IMPL_SETTING_DEFAULT(float, TauElectronFakeEnergyCorrectionShift, 1.0);
	IMPL_SETTING_DEFAULT(float, TauElectronFakeEnergyCorrectionOneProngShift, 1.0);
	IMPL_SETTING_DEFAULT(float, TauElectronFakeEnergyCorrectionOneProngPiZerosShift, 1.0);
	IMPL_SETTING_DEFAULT(float, TauElectronFakeEnergyCorrectionThreeProngShift, 1.0);
	IMPL_SETTING_DEFAULT(float, TauMuonFakeEnergyCorrectionOneProng, 1.0);
	IMPL_SETTING_DEFAULT(float, TauMuonFakeEnergyCorrectionOneProngPiZeros, 1.0);
	IMPL_SETTING_DEFAULT(float, TauMuonFakeEnergyCorrectionThreeProng, 1.0);
	IMPL_SETTING_DEFAULT(float, TauMuonFakeEnergyCorrectionShift, 1.0);
	IMPL_SETTING_DEFAULT(float, TauMuonFakeEnergyCorrectionOneProngShift, 1.0);
	IMPL_SETTING_DEFAULT(float, TauMuonFakeEnergyCorrectionOneProngPiZerosShift, 1.0);
	IMPL_SETTING_DEFAULT(float, TauMuonFakeEnergyCorrectionThreeProngShift, 1.0);
	IMPL_SETTING_DEFAULT(float, TauJetFakeEnergyCorrection, 0.0);

	IMPL_SETTING(float, RecoMuonInElectronConeLowerPtCut);
	IMPL_SETTING(float, RecoMuonInElectronConeUpperAbsEtaCut);
	IMPL_SETTING(float, RecoMuonInElectronConeSize);

	IMPL_SETTING(std::string, ZBosonVetoType);
	IMPL_SETTING(float, MetLowerPtCuts);
	IMPL_SETTING(float, MetUpperPtCuts);

	IMPL_SETTING_DEFAULT(std::string, TauDiscriminatorIsolationName, "hpsPFTauDiscriminationByRawCombinedIsolationDBSumPtCorr3Hits");
	IMPL_SETTING_DEFAULT(float, TauDiscriminatorIsolationCut, std::numeric_limits<float>::max());
	IMPL_SETTING_STRINGLIST_DEFAULT(TauDiscriminatorMvaIsolation, {});
	IMPL_SETTING_FLOATLIST_DEFAULT(TauDiscriminatorAntiElectronMvaCuts, {});
	IMPL_SETTING_INTLIST_DEFAULT(TauDiscriminatorAntiElectronMvaCutsLeptonIndices, {});

	IMPL_SETTING_DEFAULT(float, TauLowerZImpactCut, std::numeric_limits<float>::max());
	IMPL_SETTING_DEFAULT(float, TauUpperZImpactCut, std::numeric_limits<float>::max());

	IMPL_SETTING_DEFAULT(float, TauLeadingTrackPtCut, -1.0);
	IMPL_SETTING_DEFAULT(float, TauTrackMultiplicityCut, -1.0);

	IMPL_SETTING_DEFAULT(float, SvfitMassShift, 1.0);

	IMPL_SETTING(int, NLooseElectrons);
	IMPL_SETTING(int, NLooseMuons);

	IMPL_SETTING(int, MaxNLooseElectrons);
	IMPL_SETTING(int, MaxNLooseMuons);

	IMPL_SETTING_DEFAULT(float, LowerCutHardLepPt, -1.0);

	IMPL_SETTING_DEFAULT(float, DiTauPairMinDeltaRCut, -1.0);
	IMPL_SETTING_STRINGLIST_DEFAULT(DiTauPairLepton1LowerPtCuts, {});
	IMPL_SETTING_STRINGLIST_DEFAULT(DiTauPairLepton2LowerPtCuts, {});
	IMPL_SETTING_SORTED_STRINGLIST_DEFAULT(DiTauPairHltPathsWithoutCommonMatchRequired, {});
	IMPL_SETTING_DEFAULT(bool, DiTauPairIsTauIsoMVA, false);
	IMPL_SETTING_DEFAULT(bool, DiTauPairNoHLT, false);
	IMPL_SETTING_DEFAULT(bool, RequireFirstTriggering, false);
	IMPL_SETTING_STRINGLIST_DEFAULT(HLTBranchNames, {});
	IMPL_SETTING_DEFAULT(bool, DiTauPairHLTLast, false);

	IMPL_SETTING_DEFAULT(float, SvfitKappaParameter, 6.0);
	IMPL_SETTING_DEFAULT(float, DiTauMassConstraint, -1.0);
	IMPL_SETTING_DEFAULT(std::string, SvfitCacheFile, "");
	IMPL_SETTING_DEFAULT(std::string, SvfitCacheTree, "svfitCache");
	IMPL_SETTING_DEFAULT(std::string, SvfitCacheFileFolder, "");
	IMPL_SETTING_DEFAULT(bool, UseFirstInputFileNameForSvfit, false);
	IMPL_SETTING_DEFAULT(std::string, SvfitCacheMissBehaviour, "assert");
	IMPL_SETTING_DEFAULT(std::string, SvfitOutFile, "");
	IMPL_SETTING_DEFAULT(bool, GenerateSvfitInput, false);
	IMPL_SETTING_DEFAULT(int, SvfitInputCutOff, 5000)
	IMPL_SETTING_DEFAULT(bool, UpdateSvfitCache, false)

	IMPL_SETTING(std::string, TauTauRestFrameReco);

	IMPL_SETTING_DEFAULT(float, TauElectronLowerDeltaRCut, 0.5);
	IMPL_SETTING_DEFAULT(float, TauMuonLowerDeltaRCut, 0.5);
	IMPL_SETTING_DEFAULT(float, TauTauLowerDeltaRCut, 0.5);
	IMPL_SETTING_DEFAULT(float, JetTauLowerDeltaRCut, 0.5);

	IMPL_SETTING(std::string, TauSpinnerSettingsPDF);
	IMPL_SETTING(float, TauSpinnerSettingsCmsEnergy);
	IMPL_SETTING(bool, TauSpinnerSettingsIpp);
	IMPL_SETTING(int, TauSpinnerSettingsIpol);
	IMPL_SETTING(int, TauSpinnerSettingsNonSM2);
	IMPL_SETTING(int, TauSpinnerSettingsNonSMN);

	IMPL_SETTING_FLOATLIST_DEFAULT(TauSpinnerMixingAnglesOverPiHalf, {});
	IMPL_SETTING_DEFAULT(float, TauSpinnerMixingAnglesOverPiHalfSample, -1.0);

	IMPL_SETTING(int, BosonPdgId);

	// GenTauCPProducer settings
	IMPL_SETTING_DEFAULT(bool, PhiTransform, false);

	// TMVA reader settings
	IMPL_SETTING_STRINGLIST_DEFAULT(AntiTtbarTmvaInputQuantities, {});
	IMPL_SETTING_STRINGLIST_DEFAULT(AntiTtbarTmvaMethods, {});
	IMPL_SETTING_STRINGLIST_DEFAULT(AntiTtbarTmvaWeights, {});

	IMPL_SETTING_STRINGLIST_DEFAULT(TauPolarisationTmvaInputQuantities, {});
	IMPL_SETTING_STRINGLIST_DEFAULT(TauPolarisationTmvaMethods, {});
	IMPL_SETTING_STRINGLIST_DEFAULT(TauPolarisationTmvaWeights, {});

	//MVATestMethodsProducer settings
	IMPL_SETTING_STRINGLIST_DEFAULT(MVATestMethodsInputQuantities, {});
	IMPL_SETTING_STRINGLIST_DEFAULT(MVATestMethodsMethods, {});
	IMPL_SETTING_STRINGLIST_DEFAULT(MVATestMethodsNames, {});
	IMPL_SETTING_STRINGLIST_DEFAULT(MVACustomWeights, {});
	IMPL_SETTING_INTLIST_DEFAULT(MVATestMethodsNFolds, {});
	IMPL_SETTING_STRINGLIST_DEFAULT(MVATestMethodsWeights, {});

	// settings for TriggerTagAndProbeProducers
	IMPL_SETTING_STRINGLIST_DEFAULT(TagLeptonHltPaths, {});
	IMPL_SETTING_STRINGLIST_DEFAULT(ProbeLeptonHltPaths, {});

	IMPL_SETTING_STRINGLIST_DEFAULT(TagLeptonTriggerFilterNames, {});
	IMPL_SETTING_STRINGLIST_DEFAULT(ProbeLeptonTriggerFilterNames, {});

	// settings for RooWorkspaceWeightProducer
	IMPL_SETTING_DEFAULT(bool, SaveRooWorkspaceTriggerWeightAsOptionalOnly, false);
	IMPL_SETTING_DEFAULT(std::string, RooWorkspace, "");
	IMPL_SETTING_STRINGLIST_DEFAULT(RooWorkspaceWeightNames, {});
	IMPL_SETTING_STRINGLIST_DEFAULT(RooWorkspaceObjectNames, {});
	IMPL_SETTING_STRINGLIST_DEFAULT(RooWorkspaceObjectArguments, {});

	// settings for EETriggerWeightProducer
	IMPL_SETTING_DEFAULT(bool, SaveEETriggerWeightAsOptionalOnly, false);
	IMPL_SETTING_DEFAULT(std::string, EETriggerWeightWorkspace, "");
	IMPL_SETTING_STRINGLIST_DEFAULT(EETriggerWeightWorkspaceWeightNames, {});
	IMPL_SETTING_STRINGLIST_DEFAULT(EETriggerWeightWorkspaceObjectNames, {});
	IMPL_SETTING_STRINGLIST_DEFAULT(EETriggerWeightWorkspaceObjectArguments, {});

	// settings for MuMuTriggerWeightProducer
	IMPL_SETTING_DEFAULT(bool, SaveMuMuTriggerWeightAsOptionalOnly, false);
	IMPL_SETTING_DEFAULT(std::string, MuMuTriggerWeightWorkspace, "");
	IMPL_SETTING_STRINGLIST_DEFAULT(MuMuTriggerWeightWorkspaceWeightNames, {});
	IMPL_SETTING_STRINGLIST_DEFAULT(MuMuTriggerWeightWorkspaceObjectNames, {});
	IMPL_SETTING_STRINGLIST_DEFAULT(MuMuTriggerWeightWorkspaceObjectArguments, {});

	// settings for TauTauTriggerWeightProducer
	IMPL_SETTING_DEFAULT(bool, SaveTauTauTriggerWeightAsOptionalOnly, false);
	IMPL_SETTING_DEFAULT(std::string, TauTauTriggerWeightWorkspace, "");
	IMPL_SETTING_STRINGLIST_DEFAULT(TauTauTriggerWeightWorkspaceWeightNames, {});
	IMPL_SETTING_STRINGLIST_DEFAULT(TauTauTriggerWeightWorkspaceObjectNames, {});
	IMPL_SETTING_STRINGLIST_DEFAULT(TauTauTriggerWeightWorkspaceObjectArguments, {});

	// settings for MuTauTriggerWeightProducer
	IMPL_SETTING_DEFAULT(bool, SaveMuTauTriggerWeightAsOptionalOnly, false);
	IMPL_SETTING_DEFAULT(std::string, MuTauTriggerWeightWorkspace, "");
	IMPL_SETTING_STRINGLIST_DEFAULT(MuTauTriggerWeightWorkspaceWeightNames, {});
	IMPL_SETTING_STRINGLIST_DEFAULT(MuTauTriggerWeightWorkspaceObjectNames, {});
	IMPL_SETTING_STRINGLIST_DEFAULT(MuTauTriggerWeightWorkspaceObjectArguments, {});

	// settings for the EmbeddingConsumer
	IMPL_SETTING_DEFAULT(int, DeltaRBinning, 100);
	IMPL_SETTING_DEFAULT(float, DeltaRMaximum, 0.4);
	IMPL_SETTING_DEFAULT(int, IsoPtSumBinning, 200);
	IMPL_SETTING_DEFAULT(float, IsoPtSumMaximum, 50);
	IMPL_SETTING_DEFAULT(float, IsoPtSumOverPtMaximum, 0.4);
	IMPL_SETTING_DEFAULT(bool, RandomMuon, false);

	// setting for mass smearing applied in DiLeptonQuantitiesProducer
	IMPL_SETTING_DEFAULT(float, MassSmearing, 0.10);

	// settings for the acceptance cuts in GenAcceptanceProducer
	IMPL_SETTING_DEFAULT(float, Lepton1AcceptancePtCut, -1.0);
	IMPL_SETTING_DEFAULT(float, Lepton2AcceptancePtCut, -1.0);
	IMPL_SETTING_DEFAULT(float, Lepton1AcceptanceEtaCut, std::numeric_limits<float>::max());
	IMPL_SETTING_DEFAULT(float, Lepton2AcceptanceEtaCut, std::numeric_limits<float>::max());

	// settings for the ScaleVariationProducer
	IMPL_SETTING_STRINGLIST(PdfLheWeights);
	IMPL_SETTING_STRINGLIST(AlphaSLheWeights);
	IMPL_SETTING_STRINGLIST(ScaleLheWeights);

	// settings for SimpleMuTauFakeRateWeightProducer
	IMPL_SETTING_FLOATLIST(SimpleMuTauFakeRateWeightLoose);
	IMPL_SETTING_FLOATLIST(SimpleMuTauFakeRateWeightTight);

	// settings for SimpleEleTauFakeRateWeightProducer
	IMPL_SETTING_FLOATLIST(SimpleEleTauFakeRateWeightVLoose);
	IMPL_SETTING_FLOATLIST(SimpleEleTauFakeRateWeightTight);

	// settings for MetFilter
	IMPL_SETTING_STRINGLIST_DEFAULT(MetFilter, {});

	// settings for ZPtReweightProducer
	IMPL_SETTING(std::string, ZptReweightProducerWeights);

	// settings for JetToTauFakesProducer
	IMPL_SETTING_STRINGLIST_DEFAULT(FakeFaktorFiles, {});

	// settings for MadGraphReweightingProducer
	IMPL_SETTING_FLOATLIST_DEFAULT(MadGraphMixingAnglesOverPiHalf, {});
	IMPL_SETTING_DEFAULT(float, MadGraphMixingAnglesOverPiHalfSample, -1.0);
	IMPL_SETTING(std::string, MadGraphParamCard);
	IMPL_SETTING(std::string, MadGraphParamCardSample);
	IMPL_SETTING_DEFAULT(bool, UseMadGraph2p5, false);
	IMPL_SETTING(std::string, MadGraph2p6ProcessDirectory);
	IMPL_SETTING_STRINGLIST(MadGraph2p5ProcessDirectories);
	IMPL_SETTING(bool, MadGraphSortingHeavyBQuark);
	
	IMPL_SETTING(std::string, MELAHiggsProductionMode);
	
	// settting for TopPtReweightingProducer
	IMPL_SETTING(std::string, TopPtReweightingStrategy)
};
