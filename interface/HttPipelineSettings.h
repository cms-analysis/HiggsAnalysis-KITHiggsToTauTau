
#pragma once

#include "Artus/KappaAnalysis/interface/KappaPipelineSettings.h"

class HttPipelineSettings: public KappaPipelineSettings {
public:
	IMPL_SETTING_DEFAULT(std::string, Channel, "")
};

class HttGlobalSettings: public KappaGlobalSettings {
public:
	IMPL_SETTING(bool, InputIsData)

};
