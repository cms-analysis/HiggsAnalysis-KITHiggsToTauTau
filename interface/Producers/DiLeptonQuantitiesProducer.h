
#pragma once

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"


/** Producer for simple di-lepton/di-tau quantities.
 */
class DiLeptonQuantitiesProducer: public ProducerBase<HttTypes> {
public:

	virtual std::string GetProducerId() const override {
		return "DiLeptonQuantitiesProducer";
	}
	
	virtual void Init(setting_type const& settings, metadata_type& metadata) override;

	virtual void Produce(event_type const& event, product_type& product,
	                     setting_type const& settings, metadata_type const& metadata) const override;
};

