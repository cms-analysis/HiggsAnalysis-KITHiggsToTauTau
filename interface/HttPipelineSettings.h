
#pragma once

#include <limits.h>

#include "Artus/KappaAnalysis/interface/KappaPipelineSettings.h"

/**
   \brief Reads settings for all parts of the KappaAnalysis code from a prepared
   json configuration file. 

   Defines settings that can be obtained from the json configuration file.
*/

class HttPipelineSettings: public KappaPipelineSettings {
public:

	/// names of MET collection in kappa tuple
	IMPL_SETTING_DEFAULT(std::string, MvaMetTT, "");
	IMPL_SETTING_DEFAULT(std::string, MvaMetMT, "");
	IMPL_SETTING_DEFAULT(std::string, MvaMetET, "");
	IMPL_SETTING_DEFAULT(std::string, MvaMetEM, "");
	
	/// htt decay channel and event category
	IMPL_SETTING_DEFAULT(std::string, Channel, "");
	IMPL_SETTING_DEFAULT(std::string, Category, "");
	
	IMPL_SETTING_DOUBLELIST(ElectronTriggerTurnOnParamtersData);
	IMPL_SETTING_DOUBLELIST(ElectronTriggerTurnOnParamtersMc);
	IMPL_SETTING_DOUBLELIST(MuonTriggerTurnOnParamtersData);
	IMPL_SETTING_DOUBLELIST(MuonTriggerTurnOnParamtersMc);
	IMPL_SETTING_DOUBLELIST(TauTriggerTurnOnParamtersData);
	IMPL_SETTING_DOUBLELIST(TauTriggerTurnOnParamtersMc);
	
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
	
	IMPL_SETTING_DEFAULT(float, MuonChargedIsoVetoConeSize, 0.0);
	IMPL_SETTING_DEFAULT(float, MuonNeutralIsoVetoConeSize, 0.0);
	IMPL_SETTING_DEFAULT(float, MuonPhotonIsoVetoConeSize, 0.0);
	IMPL_SETTING_DEFAULT(float, MuonDeltaBetaIsoVetoConeSize, 0.0);
	
	IMPL_SETTING_DEFAULT(float, MuonChargedIsoPtThreshold, 0.0);
	IMPL_SETTING_DEFAULT(float, MuonNeutralIsoPtThreshold, 0.0);
	IMPL_SETTING_DEFAULT(float, MuonPhotonIsoPtThreshold, 0.0);
	IMPL_SETTING_DEFAULT(float, MuonDeltaBetaIsoPtThreshold, 0.0);
	
	IMPL_SETTING_DEFAULT(float, BTaggedJetCombinedSecondaryVertexMediumWP, 0.0);
	IMPL_SETTING_DEFAULT(float, BTaggedJetAbsEtaCut, 0.0);

	IMPL_SETTING(float, IsoSignalConeSize);
	IMPL_SETTING(float, DeltaBetaCorrectionFactor);
	IMPL_SETTING(float, IsoPtSumOverPtThresholdEB);
	IMPL_SETTING(float, IsoPtSumOverPtThresholdEE);
	
	IMPL_SETTING(float, ElectronTrackDxyCut);
	IMPL_SETTING(float, ElectronTrackDzCut);
	IMPL_SETTING(float, MuonTrackDxyCut);
	IMPL_SETTING(float, MuonTrackDzCut);
	
	IMPL_SETTING_DEFAULT(float, TauDiscriminatorIsolationCut, std::numeric_limits<float>::max());
	IMPL_SETTING_FLOATLIST(TauDiscriminatorAntiElectronMvaCuts);
	IMPL_SETTING_INTLIST(TauDiscriminatorAntiElectronMvaCutsLeptonIndices);
	
	IMPL_SETTING(float, LowerCutHardLepPt);
	
	IMPL_SETTING_STRINGLIST(TauSpinnerSettings);
	IMPL_SETTING_STRINGLIST(ChosenTauDaughters);

};
