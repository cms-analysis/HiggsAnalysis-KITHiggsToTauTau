
#pragma once

#include "Artus/Core/interface/Cpp11Support.h"

#include "../HttTypes.h"

class PreselectionFilter: public HttFilterBase {
public:

	virtual ~PreselectionFilter() {
	}

	virtual std::string GetFilterId() const ARTUS_CPP11_OVERRIDE {
		return "filter_preselection";
	}

	virtual bool DoesEventPassLocal(HttEvent const& event, HttProduct const& product,
            HttPipelineSettings const& settings) const ARTUS_CPP11_OVERRIDE
	{
		std::string decayChannelString = settings.GetChannel();
		
		// TODO: is there a more elegant way of mapping?
		DecayChannel decayChannel = DecayChannel::NONE;
		if(decayChannelString == "TT") decayChannel = DecayChannel::TT;
		else if(decayChannelString == "MT") decayChannel = DecayChannel::MT;
		else if(decayChannelString == "ET") decayChannel = DecayChannel::ET;
		else if(decayChannelString == "EM") decayChannel = DecayChannel::EM;
		else if(decayChannelString == "MM") decayChannel = DecayChannel::MM;
		else if(decayChannelString == "EE") decayChannel = DecayChannel::EE;
		
		return (product.m_decayChannel == decayChannel);
	}
};


