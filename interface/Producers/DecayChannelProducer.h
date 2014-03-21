
#pragma once

#include "../HttTypes.h"


class DecayChannelProducer: public HttProducerBase {
public:

	virtual std::string GetProducerId() const ARTUS_CPP11_OVERRIDE {
		return "decay_channels";
	}
	
	DecayChannelProducer() : HttProducerBase() {};

	virtual void ProduceGlobal(HttEvent const& event, HttProduct& product,
	                           HttGlobalSettings const& globalSettings) const ARTUS_CPP11_OVERRIDE;
};


