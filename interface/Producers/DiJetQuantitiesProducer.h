
#pragma once

#include "../HttTypes.h"


class DiJetQuantitiesProducer: public ProducerBase<HttTypes> {
public:

	typedef typename HttTypes::event_type event_type;
	typedef typename HttTypes::product_type product_type;
	typedef typename HttTypes::setting_type setting_type;
	
	typedef std::function<double(RMDLV const&)> dijet_extractor_lambda;
	
	static double GetDiJetQuantity(product_type const& product,
	                               dijet_extractor_lambda dijetQuantity);

	virtual std::string GetProducerId() const override {
		return "DiJetQuantitiesProducer";
	}
	
	virtual void Init(setting_type const& settings) override;

	virtual void Produce(event_type const& event, product_type& product,
	                     setting_type const& settings) const override;
};

