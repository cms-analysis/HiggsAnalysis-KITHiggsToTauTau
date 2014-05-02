
#pragma once

#include "Artus/Core/interface/Cpp11Support.h"

#include "../HttTypes.h"

class PreselectionFilter: public HttFilterBase {
public:

	virtual ~PreselectionFilter() {
	}

	virtual std::string GetFilterId() const ARTUS_CPP11_OVERRIDE {
		return "preselection";
	}
	
	virtual void InitGlobal(global_setting_type const& globalSettings)  ARTUS_CPP11_OVERRIDE
	{
		FilterBase<HttTypes>::InitGlobal(globalSettings);
	}
	
	virtual void InitLocal(setting_type const& settings)  ARTUS_CPP11_OVERRIDE
	{
		FilterBase<HttTypes>::InitLocal(settings);
	}

	virtual bool DoesEventPassLocal(HttEvent const& event,
	                                HttProduct const& product,
	                                HttPipelineSettings const& settings) const ARTUS_CPP11_OVERRIDE;
};


