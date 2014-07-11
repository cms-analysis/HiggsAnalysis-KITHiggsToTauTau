
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

	typedef typename HttTypes::event_type event_type;
	typedef typename HttTypes::product_type product_type;
	typedef typename HttTypes::setting_type setting_type;
	
	virtual std::string GetFilterId() const ARTUS_CPP11_OVERRIDE {
            return "decay_channel";
    }
    
    virtual void Init(setting_type const& settings) ARTUS_CPP11_OVERRIDE;

	virtual bool DoesEventPass(event_type const& event, product_type const& product,
	                           setting_type const& settings) const ARTUS_CPP11_OVERRIDE;


private:
	HttEnumTypes::DecayChannel m_decayChannel;

};


