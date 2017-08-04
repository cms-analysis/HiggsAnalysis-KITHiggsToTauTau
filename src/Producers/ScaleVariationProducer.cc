
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/ScaleVariationProducer.h"

#include "Artus/Utility/interface/SafeMap.h"
#include "Artus/Utility/interface/Utility.h"
#include "Artus/Consumer/interface/LambdaNtupleConsumer.h"

#include <algorithm>


std::string ScaleVariationProducer::GetProducerId() const
{
	return "ScaleVariationProducer";
}

void ScaleVariationProducer::Init(setting_type const& settings)
{
	ProducerBase<HttTypes>::Init(settings);
	
	for (std::vector<std::string>::const_iterator lheWeight = settings.GetPdfLheWeights().begin(); lheWeight != settings.GetPdfLheWeights().end(); ++lheWeight)
	{
		std::string lheWeightStr = *lheWeight;
		LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(lheWeightStr, [lheWeightStr](event_type const& event, product_type const& product)
		{
			return SafeMap::GetWithDefault(product.m_optionalWeights, lheWeightStr, 1.0);
		});
	}
	
	for (std::vector<std::string>::const_iterator lheWeight = settings.GetAlphaSLheWeights().begin(); lheWeight != settings.GetAlphaSLheWeights().end(); ++lheWeight)
	{
		std::string lheWeightStr = *lheWeight;
		LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(lheWeightStr, [lheWeightStr](event_type const& event, product_type const& product)
		{
			return SafeMap::GetWithDefault(product.m_optionalWeights, lheWeightStr, 1.0);
		});
	}
	
	for (std::vector<std::string>::const_iterator lheWeight = settings.GetScaleLheWeights().begin(); lheWeight != settings.GetScaleLheWeights().end(); ++lheWeight)
	{
		std::string lheWeightStr = *lheWeight;
		LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(lheWeightStr, [lheWeightStr](event_type const& event, product_type const& product)
		{
			return SafeMap::GetWithDefault(product.m_optionalWeights, lheWeightStr, 1.0);
		});
	}
}

void ScaleVariationProducer::OnLumi(event_type const& event, setting_type const& settings)
{
	assert(event.m_genEventInfoMetadata);
	assert(event.m_genRunInfo);

	m_pdfLheWeightNamesIndices = event.m_genEventInfoMetadata->getLheWeightNamesMap(settings.GetPdfLheWeights(), event.m_genRunInfo->lheWeightNamesMap);
	m_alphaSLheWeightNamesIndices = event.m_genEventInfoMetadata->getLheWeightNamesMap(settings.GetAlphaSLheWeights(), event.m_genRunInfo->lheWeightNamesMap);
	m_scaleLheWeightNamesIndices = event.m_genEventInfoMetadata->getLheWeightNamesMap(settings.GetScaleLheWeights(), event.m_genRunInfo->lheWeightNamesMap);
}

void ScaleVariationProducer::Produce(event_type const& event, product_type & product, 
                                     setting_type const& settings) const
{
	assert(event.m_genEventInfo);
	
	// PDF variations
	if (m_pdfLheWeightNamesIndices.size() > 0)
	{
		std::map<std::string, float> pdfLheWeights = event.m_genEventInfo->getLheWeights(m_pdfLheWeightNamesIndices);
		for (std::map<std::string, float>::iterator lheWeight = pdfLheWeights.begin(); lheWeight != pdfLheWeights.end(); ++lheWeight)
		{
			product.m_optionalWeights[lheWeight->first] = lheWeight->second;
		}
		float minPdfLheWeight = std::min_element(
				pdfLheWeights.begin(), pdfLheWeights.end(),
				[](std::pair<std::string, float> const& a, std::pair<std::string, float> const& b) { return a.second < b.second; }
		)->second;
		float maxPdfLheWeight = std::max_element(
				pdfLheWeights.begin(), pdfLheWeights.end(),
				[](std::pair<std::string, float> const& a, std::pair<std::string, float> const& b) { return a.second < b.second; }
		)->second;
		LOG(INFO) << "PDF:    " << minPdfLheWeight << " - " << maxPdfLheWeight;
	}
	
	// alphaS variations
	if (m_alphaSLheWeightNamesIndices.size() > 0)
	{
		std::map<std::string, float> alphaSLheWeights = event.m_genEventInfo->getLheWeights(m_alphaSLheWeightNamesIndices);
		for (std::map<std::string, float>::iterator lheWeight = alphaSLheWeights.begin(); lheWeight != alphaSLheWeights.end(); ++lheWeight)
		{
			product.m_optionalWeights[lheWeight->first] = lheWeight->second;
		}
		float minAlphaSLheWeight = std::min_element(
				alphaSLheWeights.begin(), alphaSLheWeights.end(),
				[](std::pair<std::string, float> const& a, std::pair<std::string, float> const& b) { return a.second < b.second; }
		)->second;
		float maxAlphaSLheWeight = std::max_element(
				alphaSLheWeights.begin(), alphaSLheWeights.end(),
				[](std::pair<std::string, float> const& a, std::pair<std::string, float> const& b) { return a.second < b.second; }
		)->second;
		LOG(INFO) << "AlphaS: " << minAlphaSLheWeight << " - " << maxAlphaSLheWeight;
	}
	
	// muF/muR scale variations
	if (m_scaleLheWeightNamesIndices.size() > 0)
	{
		std::map<std::string, float> scaleLheWeights = event.m_genEventInfo->getLheWeights(m_scaleLheWeightNamesIndices);
		for (std::map<std::string, float>::iterator lheWeight = scaleLheWeights.begin(); lheWeight != scaleLheWeights.end(); ++lheWeight)
		{
			product.m_optionalWeights[lheWeight->first] = lheWeight->second;
		}
		float minScaleLheWeight = std::min_element(
				scaleLheWeights.begin(), scaleLheWeights.end(),
				[](std::pair<std::string, float> const& a, std::pair<std::string, float> const& b) { return a.second < b.second; }
		)->second;
		float maxScaleLheWeight = std::max_element(
				scaleLheWeights.begin(), scaleLheWeights.end(),
				[](std::pair<std::string, float> const& a, std::pair<std::string, float> const& b) { return a.second < b.second; }
		)->second;
		LOG(INFO) << "Scale:  " << minScaleLheWeight << " - " << maxScaleLheWeight;
	}
}
