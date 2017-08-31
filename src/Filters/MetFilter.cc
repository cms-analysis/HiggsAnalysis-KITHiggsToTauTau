
#include <boost/algorithm/string.hpp>
#include <boost/algorithm/string/trim.hpp>

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttEnumTypes.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Filters/MetFilter.h"


void MetFilter::Init(setting_type const& settings, metadata_type& metadata)
{
	FilterBase<HttTypes>::Init(settings, metadata);
	
    std::vector<std::string> tmpMetFilters = settings.GetMetFilter();
	for(auto filter: tmpMetFilters)
    {
	    if(filter.at(0) == '!')
        {
            std::string filterName = filter.substr(1);
            m_invertedFilters.push_back(filterName);
            m_metFilters.push_back(filterName);
        }
        else
        {
            m_metFilters.push_back(filter);
        }

    }
}

bool MetFilter::DoesEventPass(event_type const& event, product_type const& product,
                                       setting_type const& settings, metadata_type const& metadata) const
{
    bool validEvent = true;
    for (auto metfilter : m_metFilters)
    {
        int filterid = event.m_triggerObjectMetadata->metFilterPos(metfilter);                                     
        bool result = event.m_triggerObjects->passesMetFilter(filterid);
        // check if the filter should be inverted
        if(std::find(m_invertedFilters.begin(),m_invertedFilters.end(), metfilter) != m_invertedFilters.end())
        {
            result = !result;
        }
        validEvent = validEvent && result;
    }
	return validEvent;
}

