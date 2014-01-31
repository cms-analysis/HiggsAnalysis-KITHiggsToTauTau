
#pragma once

#include "Artus/Core/interface/Cpp11Support.h"

#include "HttTypes.h"

class PtFilter: public HttFilterBase {
public:

	virtual ~PtFilter() {
	}

	virtual std::string GetFilterId() {
		return "filter_pt";
	}

	virtual bool DoesEventPass(HttEvent const& event,
			HttProduct const& product,
            HttPipelineSettings const& settings ) {

		const float lowCut = settings.GetFilterPtLow();
		const float highCut = settings.GetFilterPtHigh();

		assert(lowCut <= highCut);

		return ((lowCut <= event.m_floatPtSim) && (highCut > event.m_floatPtSim));
	}
};


