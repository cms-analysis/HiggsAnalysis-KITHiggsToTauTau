
#pragma once

#include "../HttTypes.h"


class EventWeightProducer: public HttProducerBase {
public:

	virtual std::string GetProducerId() const ARTUS_CPP11_OVERRIDE {
		return "event_weight";
	}
	
	virtual void InitGlobal(global_setting_type const& globalSettings)  ARTUS_CPP11_OVERRIDE
	{
		ProducerBase<HttTypes>::InitGlobal(globalSettings);
	}
	
	virtual void InitLocal(setting_type const& settings)  ARTUS_CPP11_OVERRIDE
	{
		ProducerBase<HttTypes>::InitLocal(settings);
	}

	virtual void ProduceLocal(HttEvent const& event, HttProduct& product,
	                          HttPipelineSettings const& settings) const ARTUS_CPP11_OVERRIDE;
};


