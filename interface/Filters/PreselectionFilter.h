
#pragma once

#include "Artus/Core/interface/Cpp11Support.h"

#include "../HttTypes.h"

class PreselectionFilter: public HttFilterBase {
public:

	virtual ~PreselectionFilter() {
	}

	virtual std::string GetFilterId() {
		return "filter_preselection";
	}

	virtual bool DoesEventPass(HttEvent const& event,
			HttProduct const& product,
            HttPipelineSettings const& settings ) {

		const std::string channel = settings.GetChannel();
		
		bool passPreselection = true;
		if(channel == "mm") {
			if(event.m_muons->size() < 2) passPreselection = false;
		}
		else {
			passPreselection = false;
		}

		return passPreselection;
	}
};


