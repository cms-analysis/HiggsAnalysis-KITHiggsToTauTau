
#pragma once

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"


class DiJetQuantitiesProducer: public ProducerBase<HttTypes> {
public:

	typedef std::function<double(RMDLV const&)> dijet_extractor_lambda;
	
	static double GetDiJetQuantity(product_type const& product,
	                               dijet_extractor_lambda dijetQuantity);

	virtual std::string GetProducerId() const override {
		return "DiJetQuantitiesProducer";
	}
	
	virtual void Init(setting_type const& settings, metadata_type& metadata) override;

	virtual void Produce(event_type const& event, product_type& product,
	                     setting_type const& settings, metadata_type const& metadata) const override;
};

