
#pragma once

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"


/** Producer that defines the decay channel.
 */
class DecayChannelProducer: public ProducerBase<HttTypes> {
public:

	virtual std::string GetProducerId() const override {
		return "DecayChannelProducer";
	}
	
	virtual void Init(setting_type const& settings, metadata_type& metadata) override;
	
	virtual void Produce(event_type const& event, product_type& product,
	                     setting_type const& settings, metadata_type const& metadata) const override;

protected:
	HttEnumTypes::DecayChannel m_decayChannel;
	
	void FillGenLeptonCollections(product_type& product) const;
};


/** Decay channel producer designed to accommodate the Higgs to tau decays
    where the Higgs is produced in association with a top pair (ttH).
 */
class TTHDecayChannelProducer: public DecayChannelProducer {
public:

	virtual std::string GetProducerId() const override {
		return "TTHDecayChannelProducer";
	}
	
	virtual void Produce(event_type const& event, product_type& product,
	                     setting_type const& settings, metadata_type const& metadata) const override;
};

class Run2DecayChannelProducer : public DecayChannelProducer {
public:
	virtual std::string GetProducerId() const override {
		return "Run2DecayChannelProducer";
	}
	
	virtual void Init(setting_type const& settings, metadata_type& metadata) override;

	virtual void Produce(event_type const& event, product_type& product,
	                     setting_type const& settings, metadata_type const& metadata) const override;
};

