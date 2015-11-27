
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
	
	/// htt decay channel and event category
	IMPL_SETTING_DEFAULT(std::string, Channel, "");
	IMPL_SETTING_DEFAULT(std::string, Category, "");
	
	IMPL_SETTING(bool, OSChargeLeptons);
	
	IMPL_SETTING_STRINGLIST_DEFAULT(TriggerEfficiencyData, {});
	IMPL_SETTING_STRINGLIST_DEFAULT(TriggerEfficiencyMc, {});
	IMPL_SETTING_DEFAULT(std::string, TriggerEfficiencyHistogram, "triggerEfficiency");
	
	IMPL_SETTING_STRINGLIST_DEFAULT(IdentificationEfficiencyData, {});
	IMPL_SETTING_STRINGLIST_DEFAULT(IdentificationEfficiencyMc, {});
	IMPL_SETTING_DEFAULT(std::string, IdentificationEfficiencyHistogram, "identificationEfficiency");
	
	IMPL_SETTING(std::string, ElectronIDType);
	
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
	
	IMPL_SETTING(std::string, TauEnergyCorrection);
	IMPL_SETTING_DEFAULT(float, TauEnergyCorrectionShift, 1.0);
	
	IMPL_SETTING_DEFAULT(float, SvfitMassShift, 1.0);
	
	IMPL_SETTING(int, NLooseElectrons);
	IMPL_SETTING(int, NLooseMuons);
	
	IMPL_SETTING(int, MaxNLooseElectrons);
	IMPL_SETTING(int, MaxNLooseMuons);
	
	IMPL_SETTING(float, LowerCutHardLepPt);
	
	IMPL_SETTING_DEFAULT(float, DiTauPairMinDeltaRCut, -1.0);
	IMPL_SETTING_STRINGLIST_DEFAULT(DiTauPairLepton1LowerPtCuts, {});
	IMPL_SETTING_STRINGLIST_DEFAULT(DiTauPairLepton2LowerPtCuts, {});
	IMPL_SETTING_SORTED_STRINGLIST_DEFAULT(DiTauPairHltPathsWithoutCommonMatchRequired, {});
	
	IMPL_SETTING(std::string, SvfitIntegrationMethod);
	IMPL_SETTING_DEFAULT(std::string, SvfitCacheFile, "");
	IMPL_SETTING_DEFAULT(std::string, SvfitCacheTree, "svfitCache");
	IMPL_SETTING_DEFAULT(bool, SvfitCheckInputs, false);
	
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
	IMPL_SETTING(bool, TauSpinnerSettingsBoost);
	
	IMPL_SETTING_FLOATLIST_DEFAULT(TauSpinnerMixingAnglesOverPiHalf, {});
	IMPL_SETTING_DEFAULT(float, TauSpinnerMixingAnglesOverPiHalfSample, -1.0);

	IMPL_SETTING(bool, ChooseTauDaughter);
	IMPL_SETTING_STRINGLIST_DEFAULT(ChosenTauDaughters, {});

	IMPL_SETTING(int, BosonPdgId);

	IMPL_SETTING(bool, PhiTransform);

	// TMVA reader settings
    IMPL_SETTING_STRINGLIST_DEFAULT(AntiTtbarTmvaInputQuantities, {});
    IMPL_SETTING_STRINGLIST_DEFAULT(AntiTtbarTmvaMethods, {});
    IMPL_SETTING_STRINGLIST_DEFAULT(AntiTtbarTmvaWeights, {});
    
    //MVATestMethodsProducer settings
    IMPL_SETTING_STRINGLIST_DEFAULT(MVATestMethodsInputQuantities, {});
    IMPL_SETTING_STRINGLIST_DEFAULT(MVATestMethodsMethods, {});
    IMPL_SETTING_STRINGLIST_DEFAULT(MVATestMethodsWeights, {});
    
	// settings for TriggerTagAndProbeProducers
	IMPL_SETTING_STRINGLIST_DEFAULT(TagLeptonHltPaths, {});
	IMPL_SETTING_STRINGLIST_DEFAULT(ProbeLeptonHltPaths, {});
	
	IMPL_SETTING_STRINGLIST_DEFAULT(TagLeptonTriggerFilterNames, {});
	IMPL_SETTING_STRINGLIST_DEFAULT(ProbeLeptonTriggerFilterNames, {});
};
