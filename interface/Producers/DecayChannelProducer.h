
#pragma once

#include "../HttTypes.h"


class DecayChannelProducer: public ProducerBase<HttTypes> {
public:

	typedef typename HttTypes::event_type event_type;
	typedef typename HttTypes::product_type product_type;
	typedef typename HttTypes::setting_type setting_type;

	virtual std::string GetProducerId() const ARTUS_CPP11_OVERRIDE {
		return "decay_channels";
	}
	
	virtual void Init(setting_type const& settings) ARTUS_CPP11_OVERRIDE;
	
	virtual void Produce(event_type const& event, product_type& product,
	                     setting_type const& settings) const ARTUS_CPP11_OVERRIDE;
};


