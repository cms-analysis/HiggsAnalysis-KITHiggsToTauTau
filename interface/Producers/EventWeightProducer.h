
#pragma once

#include "../HttTypes.h"


class EventWeightProducer: public HttProducerBase {
public:

	virtual std::string GetProducerId() const ARTUS_CPP11_OVERRIDE {
		return "event_weight";
	}
	
	EventWeightProducer() : HttProducerBase() {};

	virtual void ProduceLocal(HttEvent const& event, HttProduct& product,
	                          HttPipelineSettings const& settings) const ARTUS_CPP11_OVERRIDE;
};


