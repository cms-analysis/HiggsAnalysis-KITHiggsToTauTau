
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

	virtual bool DoesEventPassLocal(HttEvent const& event,
	                                HttProduct const& product,
	                                HttPipelineSettings const& settings) const ARTUS_CPP11_OVERRIDE;
};


