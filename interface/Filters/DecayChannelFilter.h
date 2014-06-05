
#pragma once

#include "Artus/Core/interface/Cpp11Support.h"

#include "../HttTypes.h"

class DecayChannelFilter: public HttFilterBase {
public:
	
	virtual std::string GetFilterId() const ARTUS_CPP11_OVERRIDE {
            return "decay_channel";
    }

	virtual bool DoesEventPass(HttEvent const& event, HttProduct const& product,
	                           HttPipelineSettings const& settings) const ARTUS_CPP11_OVERRIDE;
};


