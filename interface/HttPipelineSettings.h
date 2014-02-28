
#pragma once

#include "Artus/KappaAnalysis/interface/KappaPipelineSettings.h"

class HttPipelineSettings: public KappaPipelineSettings {
public:
	IMPL_SETTING_DEFAULT(std::string, Channel, "")

	IMPL_SETTING_DEFAULT(float, FilterPtLow, 0.0)
	IMPL_SETTING_DEFAULT(float, FilterPtHigh, 0.0)

};

class HttGlobalSettings: public KappaGlobalSettings {
public:

	IMPL_SETTING(float, ProducerPtCorrectionFactor)
	IMPL_SETTING(bool, InputIsData)

};
