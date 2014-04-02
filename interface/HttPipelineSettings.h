
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
	IMPL_SETTING_DEFAULT(std::string, Channel, "")
	IMPL_SETTING_DEFAULT(std::string, Category, "")
	
	/// quantities to be processed by the main consumer
	VarCache<stringvector> quantities;
	stringvector GetQuantities() const
	{
		RETURN_CACHED(quantities, PropertyTreeSupport::GetAsStringList(GetPropTree(), "Pipelines." + GetName() + ".Quantities"))
	}

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
        /// this is not really used I guess
	IMPL_SETTING(float, ProducerPtCorrectionFactor)
	/// detemine whether this is data or MC
	IMPL_SETTING(bool, InputIsData)
	/// Reading TauSpinnerSettings
	VarCache<stringvector> tauSpinnerSettings;
	stringvector GetTauSpinnerSettings() const
	{
		RETURN_CACHED(tauSpinnerSettings, PropertyTreeSupport::GetAsStringList(GetPropTree(), "TauSpinnerSettings"))
	}
};
