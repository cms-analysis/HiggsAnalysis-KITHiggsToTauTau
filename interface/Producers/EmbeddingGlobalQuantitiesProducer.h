#pragma once

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttEnumTypes.h"
#include "Artus/Consumer/interface/LambdaNtupleConsumer.h"

/**
   \brief Producer, that is calculating quantities describing the full event in embedding.
   Need follwoing Producers to be executed for this (attention to order!):
   - PFCandidatesProducer
   - ZProducer
*/

class EmbeddingGlobalQuantitiesProducer : public ProducerBase<HttTypes> {
public:

	virtual std::string GetProducerId() const override {
		return "EmbeddingGlobalQuantitiesProducer";
	}
	
	virtual void Init(setting_type const& settings, metadata_type& metadata) override;
	virtual void Produce(event_type const& event, product_type& product,
	                     setting_type const& settings, metadata_type const& metadata) const override;
};
