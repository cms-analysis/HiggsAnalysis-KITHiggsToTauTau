
#pragma once


#include "Kappa/DataFormats/interface/Kappa.h"

#include "Artus/Core/interface/FilterBase.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"


/** Filter the events where the dilepton pair is likely to come from a Z boson decay
 */
class ZBosonVetoFilter: public FilterBase<HttTypes> {
public:
	
	virtual std::string GetFilterId() const ARTUS_CPP11_OVERRIDE {
			return "ZBosonVetoFilter";
	}

	virtual bool DoesEventPass(event_type const& event, product_type const& product,
							   setting_type const& settings) const ARTUS_CPP11_OVERRIDE;

};

