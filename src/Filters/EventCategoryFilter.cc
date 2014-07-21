
#include <boost/algorithm/string.hpp>
#include <boost/algorithm/string/trim.hpp>

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttEnumTypes.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Filters/EventCategoryFilter.h"


void EventCategoryFilter::Init(setting_type const& settings)
{
	FilterBase<HttTypes>::Init(settings);
	
	m_eventCategory = HttEnumTypes::ToEventCategory(boost::algorithm::to_lower_copy(boost::algorithm::trim_copy(settings.GetCategory())));
}

bool EventCategoryFilter::DoesEventPass(event_type const& event, product_type const& product,
                                       setting_type const& settings) const
{
	return (product.m_exclusiveEventCategory == m_eventCategory);
}

