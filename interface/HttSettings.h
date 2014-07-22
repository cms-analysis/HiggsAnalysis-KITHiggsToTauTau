
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

	/// names of MET collection in kappa tuple
	IMPL_SETTING_DEFAULT(std::string, MvaMetTT, "");
	IMPL_SETTING_DEFAULT(std::string, MvaMetMT, "");
	IMPL_SETTING_DEFAULT(std::string, MvaMetET, "");
	IMPL_SETTING_DEFAULT(std::string, MvaMetEM, "");
	
	/// htt decay channel and event category
	IMPL_SETTING_DEFAULT(std::string, Channel, "");
	IMPL_SETTING_DEFAULT(std::string, Category, "");
	
	IMPL_SETTING_STRINGLIST(TriggerEfficiencyData);
	IMPL_SETTING_STRINGLIST(TriggerEfficiencyMc);
	
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
	IMPL_SETTING(float, ElectronIsoPtSumOverPtThresholdEB);
	IMPL_SETTING(float, ElectronIsoPtSumOverPtThresholdEE);
	
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
	IMPL_SETTING(float, MuonIsoPtSumOverPtThresholdEB);
	IMPL_SETTING(float, MuonIsoPtSumOverPtThresholdEE);
	
	IMPL_SETTING(float, ElectronTrackDxyCut);
	IMPL_SETTING(float, ElectronTrackDzCut);
	IMPL_SETTING(float, MuonTrackDxyCut);
	IMPL_SETTING(float, MuonTrackDzCut);
	
	IMPL_SETTING(std::string, LooseElectronID);
	IMPL_SETTING(std::string, LooseElectronIDType);
	IMPL_SETTING(std::string, LooseElectronReco);
	IMPL_SETTING(std::string, LooseMuonID);
	
	IMPL_SETTING(std::string, LooseElectronIsoType);
	IMPL_SETTING(std::string, LooseElectronIso);
	IMPL_SETTING(float, LooseElectronIsoPtSumOverPtThresholdEB);
	IMPL_SETTING(float, LooseElectronIsoPtSumOverPtThresholdEE);
	IMPL_SETTING(std::string, LooseMuonIsoType);
	IMPL_SETTING(std::string, LooseMuonIso);
	IMPL_SETTING(float, LooseMuonIsoPtSumOverPtThresholdEB);
	IMPL_SETTING(float, LooseMuonIsoPtSumOverPtThresholdEE);
	
	IMPL_SETTING_STRINGLIST(LooseElectronLowerPtCuts);
	IMPL_SETTING_STRINGLIST(LooseMuonLowerPtCuts);
	IMPL_SETTING_STRINGLIST(LooseElectronUpperAbsEtaCuts);
	IMPL_SETTING_STRINGLIST(LooseMuonUpperAbsEtaCuts);
	
	IMPL_SETTING_DEFAULT(float, TauDiscriminatorIsolationCut, std::numeric_limits<float>::max());
	IMPL_SETTING_FLOATLIST(TauDiscriminatorAntiElectronMvaCuts);
	IMPL_SETTING_INTLIST(TauDiscriminatorAntiElectronMvaCutsLeptonIndices);
	
	IMPL_SETTING(std::string, TauEnergyCorrection);
	
	IMPL_SETTING(int, NLooseElectrons);
	IMPL_SETTING(int, NLooseMuons);
	
	IMPL_SETTING(int, MaxNLooseElectrons);
	IMPL_SETTING(int, MaxNLooseMuons);
	
	IMPL_SETTING(float, LowerCutHardLepPt);
	
	IMPL_SETTING(std::string, SvfitIntegrationMethod);
	IMPL_GLOBAL_SETTING_DEFAULT(std::string, SvfitCacheFile, "");
	IMPL_GLOBAL_SETTING_DEFAULT(std::string, SvfitCacheTree, "svfitCache");
	
	IMPL_SETTING(std::string, TauTauRestFrameReco);

	IMPL_SETTING_DEFAULT(float, TauElectronLowerDeltaRCut, 0.5);
	IMPL_SETTING_DEFAULT(float, TauMuonLowerDeltaRCut, 0.5);

	IMPL_SETTING(std::string, TauSpinnerSettingsPDF);
	IMPL_SETTING(float, TauSpinnerSettingsCmsEnergy);
	IMPL_SETTING(bool, TauSpinnerSettingsIpp);
	IMPL_SETTING(int, TauSpinnerSettingsIpol);
	IMPL_SETTING(int, TauSpinnerSettingsNonSM2);
	IMPL_SETTING(int, TauSpinnerSettingsNonSMN);
	IMPL_SETTING(bool, TauSpinnerSettingsBoost);

	IMPL_SETTING(bool, ChooseTauDaughter);
	IMPL_SETTING_STRINGLIST(ChosenTauDaughters);

	IMPL_SETTING(int, BosonPdgId);

	// TMVA reader settings
	IMPL_SETTING_STRINGLIST(AntiTtbarTmvaInputQuantities);
	IMPL_SETTING_STRINGLIST(AntiTtbarTmvaMethods);
	IMPL_SETTING_STRINGLIST(AntiTtbarTmvaWeights);
};
