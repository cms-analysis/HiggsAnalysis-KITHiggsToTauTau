
#pragma once

#include "Artus/KappaAnalysis/interface/Consumers/KappaLambdaNtupleConsumer.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"


/** Producer to split TTbar contribution by decay modes (fullhadronic, semileptonic, fullleptonic).
 */
class TTbarGenDecayModeProducer: public ProducerBase<HttTypes> {
public:

	typedef typename HttTypes::event_type event_type;
	typedef typename HttTypes::product_type product_type;
	typedef typename HttTypes::setting_type setting_type;

	virtual std::string GetProducerId() const override {
		return "TTbarGenDecayModeProducer";
	}
	
	virtual void Init(setting_type const& settings) override;
	
	virtual void Produce(event_type const& event, product_type& product,
	                     setting_type const& settings) const override;
};
