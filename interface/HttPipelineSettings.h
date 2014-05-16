
#pragma once

#include "Artus/KappaAnalysis/interface/KappaPipelineSettings.h"

/**
   \brief Reads settings for local parts of HttPipelineRunner from a prepared json configuration file. 

   Defines local settings that can be obtained from the json configuration file. These settings are
   then available as key value pairs of type:

   KappaGlobalSetting mysetting;
   mysetting.key = value

   for an implementation of type:

   IMPL_SETTING_DEFAULT(type_of_value, key, default_value);

   This class derives from KappaPipelineSeetings for local pipeline settings and adds a few more 
   parameters, which are used for testing at the moment.
*/

class HttPipelineSettings: public KappaPipelineSettings {
public:
	/// htt decay channel and event category
	IMPL_SETTING_DEFAULT(std::string, Channel, "");
	IMPL_SETTING_DEFAULT(std::string, Category, "");
	
	/// quantities to be processed by the main consumer
	VarCache<stringvector> quantities;
	stringvector GetQuantities() const
	{
		RETURN_CACHED(quantities, PropertyTreeSupport::GetAsStringList(GetPropTree(), "Pipelines." + GetName() + ".Quantities"))
	}
	
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
	
	IMPL_SETTING(float, LowerCutHardLepPt);
};

/**
   \brief Reads settings for global parts of HttPipelineRunner from a prepared json configuration file. 

   Defines global settings that can be obtained from the json configuration file. These settings are
   then available as key value pairs of type:

   KappaGlobalSetting mysetting;
   mysetting.key = value

   for an implementation of type:

   IMPL_SETTING_DEFAULT(type_of_value, key, default_value);

   This class derives from KappaPipelineSeetings for local pipeline settings and adds a few more 
   parameters, which are used for testing at the moment.
*/

class HttGlobalSettings: public KappaGlobalSettings {
public:

	/// names of MET collection in kappa tuple
	IMPL_SETTING_DEFAULT(std::string, MvaMetTT, "");
	IMPL_SETTING_DEFAULT(std::string, MvaMetMT, "");
	IMPL_SETTING_DEFAULT(std::string, MvaMetET, "");
	IMPL_SETTING_DEFAULT(std::string, MvaMetEM, "");
	
	/// htt decay channel and event category
	IMPL_SETTING_DEFAULT(std::string, Channel, "");
	IMPL_SETTING_DEFAULT(std::string, Category, "");

	/// detemine whether this is data or MC
	IMPL_SETTING(bool, InputIsData)
	/// Reading TauSpinnerSettings
	VarCache<stringvector> tauSpinnerSettings;
	stringvector GetTauSpinnerSettings() const
	{
		RETURN_CACHED(tauSpinnerSettings, PropertyTreeSupport::GetAsStringList(GetPropTree(), "TauSpinnerSettings"))
	}
	VarCache<stringvector> chosenTauDaughters;
	stringvector GetChosenTauDaughters() const
	{
		RETURN_CACHED(chosenTauDaughters, PropertyTreeSupport::GetAsStringList(GetPropTree(), "ChosenTauDaughters"))
	}
	
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
	
	IMPL_SETTING(float, LowerCutHardLepPt);
};
