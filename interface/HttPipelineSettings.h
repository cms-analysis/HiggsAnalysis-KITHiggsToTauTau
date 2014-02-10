
#pragma once

#include "Artus/KappaLeptonAnalysis/interface/KappaLeptonPipelineSettings.h"

class HttPipelineSettings: public KappaLeptonPipelineSettings {
public:
	IMPL_SETTING_DEFAULT(std::string, Channel, "")

	IMPL_SETTING_DEFAULT(float, FilterPtLow, 0.0)
	IMPL_SETTING_DEFAULT(float, FilterPtHigh, 0.0)

	VarCache<stringvector> quantities;
	stringvector GetQuantities() const
	{
		RETURN_CACHED(quantities, PropertyTreeSupport::GetAsStringList(GetPropTree(), "Pipelines." + GetName() + ".Quantities"))
	}

};

class HttGlobalSettings: public KappaLeptonGlobalSettings {
public:

	IMPL_SETTING(float, ProducerPtCorrectionFactor)
	IMPL_SETTING(bool, InputIsData)

};
