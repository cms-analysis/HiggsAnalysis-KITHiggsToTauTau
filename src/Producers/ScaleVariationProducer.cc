
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/ScaleVariationProducer.h"
#include "Artus/Utility/interface/SafeMap.h"
#include "Artus/Utility/interface/Utility.h"


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
		if (Utility::Contains(genEventInfoMetadataMap, lheWeightName))
		{
			weightNames.push_back(SafeMap::Get(genEventInfoMetadataMap, lheWeightName).at(0));
			LOG(DEBUG) << "Found LHE weight " << lheWeightName << " (" << weightNames.back() << ")";
		}
		else
		{
			weightNames.push_back(lheWeightName);
			LOG(WARNING) << "LHE weight " << lheWeightName << " not found. It will be ommitted.";
		}
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
