
#pragma once

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"


/** Producer that defines the decay channel.
 */
class DecayChannelProducer: public ProducerBase<HttTypes> {
public:

	typedef typename HttTypes::event_type event_type;
	typedef typename HttTypes::product_type product_type;
	typedef typename HttTypes::setting_type setting_type;

	virtual std::string GetProducerId() const ARTUS_CPP11_OVERRIDE {
		return "DecayChannelProducer";
	}
	
	virtual void Init(setting_type const& settings) ARTUS_CPP11_OVERRIDE;
	
	virtual void Produce(event_type const& event, product_type& product,
	                     setting_type const& settings) const ARTUS_CPP11_OVERRIDE;
};


/** Decay channel producer designed to accommodate the Higgs to tau decays
    where the Higgs is produced in association with a top pair (ttH).
 */
class TTHDecayChannelProducer: public DecayChannelProducer {
public:

	typedef typename HttTypes::event_type event_type;
	typedef typename HttTypes::product_type product_type;
	typedef typename HttTypes::setting_type setting_type;

	virtual std::string GetProducerId() const ARTUS_CPP11_OVERRIDE {
		return "TTHDecayChannelProducer";
	}
	
	virtual void Produce(event_type const& event, product_type& product,
	                     setting_type const& settings) const ARTUS_CPP11_OVERRIDE;
};

class Run2DecayChannelProducer : public DecayChannelProducer {
public:
	virtual std::string GetProducerId() const ARTUS_CPP11_OVERRIDE {
		return "Run2DecayChannelProducer";
	}
	virtual void Produce(event_type const& event, product_type& product,
	                     setting_type const& settings) const ARTUS_CPP11_OVERRIDE;
};

