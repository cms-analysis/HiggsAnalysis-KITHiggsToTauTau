
#pragma once

#include "Artus/Core/interface/FilterBase.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttEnumTypes.h"


/** Filter for the decay channel.
 *  Required config tag:
 *  - Channel
 */
class DecayChannelFilter: public FilterBase<HttTypes> {
public:

	virtual std::string GetFilterId() const override {
            return "DecayChannelFilter";
    }

    virtual void Init(setting_type const& settings, metadata_type& metadata) override;

	virtual bool DoesEventPass(event_type const& event, product_type const& product,
	                           setting_type const& settings, metadata_type const& metadata) const override;


private:
	HttEnumTypes::DecayChannel m_decayChannel;

};
