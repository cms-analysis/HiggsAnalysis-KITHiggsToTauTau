
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
	//if no "Category" tag is provided in the config, simply checks that the event belongs to at least one category
	if (m_eventCategory == HttEnumTypes::EventCategory::NONE) {
		return (product.m_exclusiveEventCategory != HttEnumTypes::EventCategory::NONE);
	}
	
	//else, require that the event belongs exactly to the category specified in the config
	else {
		return (product.m_exclusiveEventCategory == m_eventCategory);
	}
}
