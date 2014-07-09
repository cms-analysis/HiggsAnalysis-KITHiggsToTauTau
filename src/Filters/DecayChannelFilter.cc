
#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttEnumTypes.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Filters/DecayChannelFilter.h"


bool DecayChannelFilter::DoesEventPass(event_type const& event, product_type const& product,
                                       setting_type const& settings) const
{
	return (product.m_decayChannel == HttEnumTypes::ToDecayChannel(settings.GetChannel()));
}

