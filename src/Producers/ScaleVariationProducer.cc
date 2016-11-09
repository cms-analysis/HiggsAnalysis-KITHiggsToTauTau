
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/ScaleVariationProducer.h"

std::string ScaleVariationProducer::GetProducerId() const
{
	return "ScaleVariationProducer";
}

void ScaleVariationProducer::Init(setting_type const& settings)
{
	genEventInfoMetadataMap = Utility::ParseVectorToMap(settings.GetGenEventInfoMetadataNames());
}

void ScaleVariationProducer::OnLumi(event_type const& event, setting_type const& settings)
{
	size_t index = 0;
	for(auto weight_to_store: genEventInfoMetadataMap)
	{
		// make sure it's properly configured
		assert(weight_to_store.second.size() == 1);
		for(auto weight_to_find : event.m_genEventInfoMetadata->lheWeightNames)
		{
			if(weight_to_store.first.compare(weight_to_find) == 0)
			{
				LOG(DEBUG) << "ScaleVariationProducer::Init: Inserting " << weight_to_store.first << " as " << weight_to_store.second.at(0) << " on index " << index << " to weightIndicesMap with size" << weightIndicesMap.size() << std::endl;
				//weightIndicesMap.insert(std::pair<size_t, std::string>(index, weight_to_store.second.at(0)));
				weightIndicesMap[index] = weight_to_store.second.at(0);
				break;
			}
		}
	index++;
	}
	// check wheter all specified names have been found. Stop execution otherwise
	assert(genEventInfoMetadataMap.size() == weightIndicesMap.size());
}

void ScaleVariationProducer::Produce(event_type const& event, product_type & product, 
	                 setting_type const& settings) const
{
	for(auto weight: weightIndicesMap)
	{
		product.m_optionalWeights[weight.second] = event.m_genEventInfo->lheWeight[weight.first];
	}
}
