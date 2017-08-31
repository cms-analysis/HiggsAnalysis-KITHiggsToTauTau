
#pragma once

#include "Artus/Core/interface/FilterBase.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"


/** Filter for OS/SS leptons
 *  Required config tag:
 *  - OSChargeLeptons
 */
class DiLeptonChargeFilter: public FilterBase<HttTypes> {
public:

	virtual std::string GetFilterId() const override {
            return "DiLeptonChargeFilter";
    }
    
	virtual bool DoesEventPass(event_type const& event, product_type const& product,
	                           setting_type const& settings, metadata_type const& metadata) const override;

};


