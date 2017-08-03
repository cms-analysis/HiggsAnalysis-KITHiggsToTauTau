
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/ScaleVariationProducer.h"
#include "Artus/Utility/interface/SafeMap.h"

#include "Artus/Utility/interface/Utility.h"

#include <algorithm>


std::string ScaleVariationProducer::GetProducerId() const
{
	return "ScaleVariationProducer";
}

void ScaleVariationProducer::Init(setting_type const& settings)
{
	ProducerBase<HttTypes>::Init(settings);
	
	m_pdfLheWeights = Utility::ParseVectorToMap(settings.GetPdfLheWeights());
	m_alphaSLheWeights = Utility::ParseVectorToMap(settings.GetAlphaSLheWeights());
	m_scaleLheWeights = Utility::ParseVectorToMap(settings.GetScaleLheWeights());
}

void ScaleVariationProducer::OnLumi(event_type const& event, setting_type const& settings)
{
	assert(event.m_genEventInfoMetadata);

	m_pdfLheWeightNamesIndices.clear();
	m_alphaSLheWeightNamesIndices.clear();
	m_scaleLheWeightNamesIndices.clear();
	
	for (unsigned int lheWeightIndex = 0; lheWeightIndex < event.m_genEventInfoMetadata->lheWeightNames.size(); ++lheWeightIndex)
	{
		std::string lheWeightName = event.m_genEventInfoMetadata->lheWeightNames[lheWeightIndex];
		if (Utility::Contains(m_pdfLheWeights, lheWeightName))
		{
			m_pdfLheWeightNamesIndices.push_back(std::pair<std::string, unsigned int>(SafeMap::Get(m_pdfLheWeights, lheWeightName).at(0), lheWeightIndex));
			LOG(DEBUG) << "Found PDF variation LHE weight " << lheWeightName << " (" << m_pdfLheWeightNamesIndices.end()->first << ")";
		}
		else if (Utility::Contains(m_alphaSLheWeights, lheWeightName))
		{
			m_alphaSLheWeightNamesIndices.push_back(std::pair<std::string, unsigned int>(SafeMap::Get(m_alphaSLheWeights, lheWeightName).at(0), lheWeightIndex));
			LOG(DEBUG) << "Found alphaS variation LHE weight " << lheWeightName << " (" << m_alphaSLheWeightNamesIndices.end()->first << ")";
		}
		else if (Utility::Contains(m_scaleLheWeights, lheWeightName))
		{
			m_scaleLheWeightNamesIndices.push_back(std::pair<std::string, unsigned int>(SafeMap::Get(m_scaleLheWeights, lheWeightName).at(0), lheWeightIndex));
			LOG(DEBUG) << "Found muF/muR scale variation LHE weight " << lheWeightName << " (" << m_scaleLheWeightNamesIndices.end()->first << ")";
		}
	}
}

void ScaleVariationProducer::Produce(event_type const& event, product_type & product, 
                                     setting_type const& settings) const
{
	assert(event.m_genEventInfo);
	
	// PDF variations
	float meanPdfVariationWeight = 0.0;
	for(std::vector<std::pair<std::string, unsigned int> >::const_iterator lheWeightNameIndex = m_pdfLheWeightNamesIndices.begin();
	    lheWeightNameIndex != m_pdfLheWeightNamesIndices.end(); ++lheWeightNameIndex)
	{
		product.m_optionalWeights[lheWeightNameIndex->first] = event.m_genEventInfo->lheWeights[lheWeightNameIndex->second];
		meanPdfVariationWeight += std::pow(1.0-lheWeightNameIndex->second, 2);
	}
	meanPdfVariationWeight = std::sqrt(meanPdfVariationWeight);
	product.m_optionalWeights["meanPdfVariationWeight"] = meanPdfVariationWeight;
	
	// alphaS variations
	for(std::vector<std::pair<std::string, unsigned int> >::const_iterator lheWeightNameIndex = m_alphaSLheWeightNamesIndices.begin();
	    lheWeightNameIndex != m_alphaSLheWeightNamesIndices.end(); ++lheWeightNameIndex)
	{
		product.m_optionalWeights[lheWeightNameIndex->first] = event.m_genEventInfo->lheWeights[lheWeightNameIndex->second];
	}
	
	// muF/muR scale variations
	std::vector<float> scaleVariationWeights;
	for(std::vector<std::pair<std::string, unsigned int> >::const_iterator lheWeightNameIndex = m_scaleLheWeightNamesIndices.begin();
	    lheWeightNameIndex != m_scaleLheWeightNamesIndices.end(); ++lheWeightNameIndex)
	{
		product.m_optionalWeights[lheWeightNameIndex->first] = event.m_genEventInfo->lheWeights[lheWeightNameIndex->second];
		scaleVariationWeights.push_back(event.m_genEventInfo->lheWeights[lheWeightNameIndex->second]);
	}
	product.m_optionalWeights["meanScaleVariationWeight"] = ((*std::max_element(scaleVariationWeights.begin(), scaleVariationWeights.end())) - (*std::min_element(scaleVariationWeights.begin(), scaleVariationWeights.end()))) / 2.0;
}
