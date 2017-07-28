
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/ScaleVariationProducer.h"
#include "Artus/Utility/interface/SafeMap.h"

std::string ScaleVariationProducer::GetProducerId() const
{
	return "ScaleVariationProducer";
}

void ScaleVariationProducer::Init(setting_type const& settings)
{
	ProducerBase<HttTypes>::Init(settings);
	
	genEventInfoMetadataMap = Utility::ParseVectorToMap(settings.GetGenEventInfoMetadataNames());
}

void ScaleVariationProducer::OnLumi(event_type const& event, setting_type const& settings)
{
	weightNames.clear();
	for (std::string lheWeightName : event.m_genEventInfoMetadata->lheWeightNames)
	{
		std::string humanReadableWeightName = SafeMap::GetWithDefault(genEventInfoMetadataMap, lheWeightName, {lheWeightName}).at(0);
		if (humanReadableWeightName.compare(lheWeightName) == 0)
		{
			LOG(DEBUG) << "ScaleVariationProducer::Init: Not found LHE weight " << lheWeightName << " (ommited)";
			continue;
		}
		weightNames.push_back(humanReadableWeightName);
		LOG(DEBUG) << "ScaleVariationProducer::Init: Found LHE weight " << lheWeightName << " (" << humanReadableWeightName << ")";
	}
}

void ScaleVariationProducer::Produce(event_type const& event, product_type & product, 
	                 setting_type const& settings) const
{
	size_t index = 0;
	for(std::string weightName : weightNames)
	{
		product.m_optionalWeights[weightName] = event.m_genEventInfo->lheWeight[index];
		++index;
	}
}
