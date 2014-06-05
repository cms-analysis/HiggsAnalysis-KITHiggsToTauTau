
#pragma once

#include "../HttTypes.h"


class DecayChannelProducer: public HttProducerBase {
public:

	virtual std::string GetProducerId() const ARTUS_CPP11_OVERRIDE {
		return "decay_channels";
	}

	virtual void Produce(event_type const& event, product_type& product,
	                     setting_type const& settings) const ARTUS_CPP11_OVERRIDE;
};


