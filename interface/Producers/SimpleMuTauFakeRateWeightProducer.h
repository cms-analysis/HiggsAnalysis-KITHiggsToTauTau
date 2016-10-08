
#pragma once

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"

/**
   \brief SimpleEleTauFakeRateWeightProducer
   Config tags:
   - Fill me with something meaningful

*/

class SimpleMuTauFakeRateWeightProducer : public ProducerBase<HttTypes> {
public:

	typedef typename HttTypes::event_type event_type;
	typedef typename HttTypes::product_type product_type;
	typedef typename HttTypes::setting_type setting_type;

	std::string GetProducerId() const override;

	void Produce(event_type const& event, product_type& product,
	             setting_type const& settings) const override;

};
