
#pragma once

#include "../HttTypes.h"


class DecayChannelProducer: public HttProducerBase {
public:

	virtual std::string GetProducerId() const ARTUS_CPP11_OVERRIDE {
		return "decay_channels";
	}
	
	virtual void InitGlobal(global_setting_type const& globalSettings)  ARTUS_CPP11_OVERRIDE
	{
		ProducerBase<HttTypes>::InitGlobal(globalSettings);
	}
	
	virtual void InitLocal(setting_type const& settings)  ARTUS_CPP11_OVERRIDE
	{
		ProducerBase<HttTypes>::InitLocal(settings);
	}

	virtual void ProduceGlobal(event_type const& event,
	                           product_type& product,
	                           global_setting_type const& globalSettings) const ARTUS_CPP11_OVERRIDE
	{
		Produce(event, product);
	}

	virtual void ProduceLocal(event_type const& event,
	                          product_type& product,
	                          setting_type const& settings) const ARTUS_CPP11_OVERRIDE
	{
		Produce(event, product);
	}

protected:

	// function that lets this producer work as both a global and a local producer
	virtual void Produce(event_type const& event, product_type& product) const;
};


