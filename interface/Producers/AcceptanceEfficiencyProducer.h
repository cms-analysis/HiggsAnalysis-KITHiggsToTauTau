#pragma once

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttEnumTypes.h"
#include "Artus/Consumer/interface/LambdaNtupleConsumer.h"

class AcceptanceEfficiencyProducer: public ProducerBase<HttTypes> {
public:

	typedef typename HttTypes::event_type event_type;
	typedef typename HttTypes::product_type product_type;
	typedef typename HttTypes::setting_type setting_type;

	virtual std::string GetProducerId() const override {
		return "AcceptanceEfficiencyProducer";
	}
	
	virtual void Init(setting_type const& settings) override;
	
	
	/* Numbers for decay channels:
		0 for Undefined
		1 for ElEl
		2 for MuMu
		3 for HadHad
		4 for ElMu
		5 for ElHad
		6 for MuHad
	*/
	virtual unsigned int DetermineDecayChannel(event_type const& event, KGenParticle* tau1, KGenParticle* tau2) const;
	virtual void Produce(event_type const& event, product_type& product,
	                     setting_type const& settings) const override;
};
