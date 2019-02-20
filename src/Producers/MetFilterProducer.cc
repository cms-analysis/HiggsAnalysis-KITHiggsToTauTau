#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/MetFilterProducer.h"



MetFilterProducer::~MetFilterProducer()
{
}

std::string MetFilterProducer::GetProducerId() const
{
	return "MetFilterProducer";
}

void MetFilterProducer::Init(setting_type const& settings, metadata_type& metadata)
{
	ProducerBase<HttTypes>::Init(settings, metadata);

	std::vector<std::string> tmpMetFilters = settings.GetMetFilter();
	for(auto filter: tmpMetFilters)
	{
		//std::cout << "FilterName:\t\t" << filter << std::endl;
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

void MetFilterProducer::Produce(event_type const& event, product_type& product,
                                    setting_type const& settings, metadata_type const& metadata) const
{
	bool validEvent = true;
	for (auto metfilter : m_metFilters)
	{
		//std::cout<< metfilter << std::endl;
		int filterid = event.m_triggerObjectMetadata->metFilterPos(metfilter);                                  
        	bool result = event.m_triggerObjects->passesMetFilter(filterid);
		// check if the filter should be inverted
		if(std::find(m_invertedFilters.begin(),m_invertedFilters.end(), metfilter) != m_invertedFilters.end())
		{
			result = !result;
		}
		product.m_optionalWeights[metfilter] = result; //add option to look at each metfilter seperatly
		validEvent = validEvent && result;
	}
	product.m_optionalWeights["metFilterWeight"] = validEvent;
}

