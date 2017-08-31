
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Filters/DiLeptonChargeFilter.h"


bool DiLeptonChargeFilter::DoesEventPass(event_type const& event, product_type const& product,
                                       setting_type const& settings, metadata_type const& metadata) const
{
	assert(product.m_flavourOrderedLeptons.size() >= 2);
	return ((int(product.m_flavourOrderedLeptons[0]->charge()) * int(product.m_flavourOrderedLeptons[1]->charge()) < 0)
	        ==
	        settings.GetOSChargeLeptons());
}

