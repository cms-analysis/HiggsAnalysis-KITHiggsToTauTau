
#include <boost/algorithm/string.hpp>
#include <boost/algorithm/string/trim.hpp>

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttEnumTypes.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Filters/DecayChannelFilter.h"


void DecayChannelFilter::Init(setting_type const& settings)
{
	FilterBase<HttTypes>::Init(settings);
	
	m_decayChannel = HttEnumTypes::ToDecayChannel(boost::algorithm::to_lower_copy(boost::algorithm::trim_copy(settings.GetChannel())));
}

bool DecayChannelFilter::DoesEventPass(event_type const& event, product_type const& product,
                                       setting_type const& settings) const
{
	return (product.m_decayChannel == m_decayChannel);
}

