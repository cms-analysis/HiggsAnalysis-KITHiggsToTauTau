#pragma once

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"


class MVAInputQuantitiesProducer: public ProducerBase<HttTypes> {
public:

    virtual std::string GetProducerId() const override {
        return "MVAInputQuantitiesProducer";
    }
    
    virtual void Init(setting_type const& settings, metadata_type& metadata) override;

    virtual void Produce(event_type const& event, product_type& product,
                         setting_type const& settings, metadata_type const& metadata) const override;
};
