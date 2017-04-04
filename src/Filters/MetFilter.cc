
#include <boost/algorithm/string.hpp>
#include <boost/algorithm/string/trim.hpp>

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttEnumTypes.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Filters/MetFilter.h"


void MetFilter::Init(setting_type const& settings)
{
	FilterBase<HttTypes>::Init(settings);
	
	m_metFilters = settings.GetMetFilter();
}

bool MetFilter::DoesEventPass(event_type const& event, product_type const& product,
                                       setting_type const& settings) const
{
    bool validEvent = true;
    for (auto metfilter : m_metFilters)
    {
        int filterid = event.m_triggerObjectMetadata->metFilterPos(metfilter);                                     
        validEvent = validEvent && event.m_triggerObjects->passesMetFilter(filterid);
    }
	return validEvent;
}

