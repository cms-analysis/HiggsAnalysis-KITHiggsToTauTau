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

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "metfilter_flag", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_metFilterFlag;
	});

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
	bool metFilterFlag = true;
	for (auto metfilter : m_metFilters)
	{
		LOG(DEBUG) << metfilter << std::endl;
		int filterid = event.m_triggerObjectMetadata->metFilterPos(metfilter);
        	bool result = event.m_triggerObjects->passesMetFilter(filterid);
		// check if the filter should be inverted
		if(std::find(m_invertedFilters.begin(),m_invertedFilters.end(), metfilter) != m_invertedFilters.end())
		{
			result = !result;
		}
		product.m_optionalWeights[metfilter] = result; //add option to look at each metfilter seperatly
		metFilterFlag = metFilterFlag && result;
		if(product.m_optionalWeights[metfilter] != 1.0){
			LOG(DEBUG) << "event.m_triggerObjectMetadata->metFilterPos(metfilter): " << event.m_triggerObjectMetadata->metFilterPos(metfilter);
			LOG(DEBUG) << "product.m_optionalWeights[metfilter]: " << product.m_optionalWeights[metfilter];
			LOG(DEBUG) << "metFilterFlag: " << metFilterFlag;
		}
	}
	product.m_optionalWeights["metFilterWeight"] = metFilterFlag;
	product.m_metFilterFlag = metFilterFlag;
	LOG(DEBUG) << "product.m_optionalWeights[\"metFilterWeight\"]: " << product.m_optionalWeights["metFilterWeight"];
	LOG(DEBUG) << "product.m_metFilterFlag: " << product.m_metFilterFlag;
}

