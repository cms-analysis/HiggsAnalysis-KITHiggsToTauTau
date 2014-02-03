
#pragma once

#include "Artus/Core/interface/GlobalInclude.h"
#include "Artus/Configuration/interface/SettingsBase.h"
#include "Artus/Configuration/interface/SettingMacros.h"
#include "Artus/Configuration/interface/PropertyTreeSupport.h"

class HttPipelineSettings: public SettingsBase {
public:
	IMPL_SETTING_DEFAULT(std::string, Channel, "")

	IMPL_SETTING_DEFAULT(float, FilterPtLow, 0.0)
	IMPL_SETTING_DEFAULT(float, FilterPtHigh, 0.0)

	VarCache<stringvector> m_filter;
	stringvector GetFilter() const
	{
		RETURN_CACHED(m_filter, PropertyTreeSupport::GetAsStringList(GetPropTree(), "Pipelines." + GetName() + ".Filter"))
	}

	VarCache<stringvector> m_consumer;
	stringvector GetConsumer() const
	{
		RETURN_CACHED(m_consumer, PropertyTreeSupport::GetAsStringList(GetPropTree(), "Pipelines." + GetName() + ".Consumer"))
	}

	VarCache<stringvector> quantities;
	stringvector GetQuantities() const
	{
		RETURN_CACHED(quantities, PropertyTreeSupport::GetAsStringList(GetPropTree(), "Pipelines." + GetName() + ".Quantities"))
	}

};

class HttGlobalSettings: public GlobalSettingsBase {
public:

	IMPL_SETTING(float, ProducerPtCorrectionFactor)
	IMPL_SETTING(bool, InputIsData)

};
