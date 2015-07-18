
#pragma once

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"


/** Producer that defines the decay channel.
 */
class DecayChannelProducer: public ProducerBase<HttTypes> {
public:

	typedef typename HttTypes::event_type event_type;
	typedef typename HttTypes::product_type product_type;
	typedef typename HttTypes::setting_type setting_type;

	virtual std::string GetProducerId() const override {
		return "DecayChannelProducer";
	}
	
	virtual void Init(setting_type const& settings) override;
	
	virtual void Produce(event_type const& event, product_type& product,
	                     setting_type const& settings) const override;
};


/** Decay channel producer designed to accommodate the Higgs to tau decays
    where the Higgs is produced in association with a top pair (ttH).
 */
class TTHDecayChannelProducer: public DecayChannelProducer {
public:

	typedef typename HttTypes::event_type event_type;
	typedef typename HttTypes::product_type product_type;
	typedef typename HttTypes::setting_type setting_type;

	virtual std::string GetProducerId() const override {
		return "TTHDecayChannelProducer";
	}
	
	virtual void Produce(event_type const& event, product_type& product,
	                     setting_type const& settings) const override;
};

class Run2DecayChannelProducer : public DecayChannelProducer {
public:
	virtual std::string GetProducerId() const override {
		return "Run2DecayChannelProducer";
	}
	virtual void Produce(event_type const& event, product_type& product,
	                     setting_type const& settings) const override;
};

