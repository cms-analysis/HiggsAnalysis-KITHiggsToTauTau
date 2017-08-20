
#pragma once

#include "Artus/KappaAnalysis/interface/Consumers/KappaLambdaNtupleConsumer.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"


/** Producer to split TTbar contribution by decay modes (fullhadronic, semileptonic, fullleptonic).
 */
class TTbarGenDecayModeProducer: public ProducerBase<HttTypes> {
public:

	virtual std::string GetProducerId() const override {
		return "TTbarGenDecayModeProducer";
	}
	
	virtual void Init(setting_type const& settings, metadata_type& metadata) override;
	
	virtual void Produce(event_type const& event, product_type& product,
	                     setting_type const& settings, metadata_type const& metadata) const override;
};
