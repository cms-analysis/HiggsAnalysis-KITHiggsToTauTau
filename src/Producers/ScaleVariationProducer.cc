
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
	
	DetermineWeights(event, product, settings, m_pdfLheWeightNamesIndices, "Pdf");
	DetermineWeights(event, product, settings, m_alphaSLheWeightNamesIndices, "AlphaS");
	DetermineWeights(event, product, settings, m_scaleLheWeightNamesIndices, "Scale");
}

void ScaleVariationProducer::DetermineWeights(event_type const& event, product_type & product, setting_type const& settings,
                                              std::map<std::string, unsigned int> const& lheWeightNamesIndices, std::string const& variationName) const
{
	if (lheWeightNamesIndices.size() > 0)
	{
		std::map<std::string, float> lheWeights = event.m_genEventInfo->getLheWeights(lheWeightNamesIndices);
		
		int nWeightsUp = 0;
		float sumOfLheWeightsUp = 0.0;
		float sumOfQuadraticDifferencesUp = 0.0;
		
		int nWeightsDown = 0;
		float sumOfLheWeightsDown = 0.0;
		float sumOfQuadraticDifferencesDown = 0.0;
		
		for (std::map<std::string, float>::iterator lheWeight = lheWeights.begin(); lheWeight != lheWeights.end(); ++lheWeight)
		{
			product.m_optionalWeights[lheWeight->first] = lheWeight->second;
			
			if (lheWeight->second > 1.0)
			{
				++nWeightsUp;
				sumOfLheWeightsUp += lheWeight->second;
				sumOfQuadraticDifferencesUp += std::pow(lheWeight->second - 1.0, 2);
			}
			else if (lheWeight->second < 1.0)
			{
				++nWeightsDown;
				sumOfLheWeightsDown += lheWeight->second;
				sumOfQuadraticDifferencesDown += std::pow(lheWeight->second - 1.0, 2);
			}
		}
		
		std::pair<std::map<std::string, float>::const_iterator, std::map<std::string, float>::const_iterator> minmaxPdfLheWeight = std::minmax_element(
				lheWeights.begin(), lheWeights.end(),
				[](std::pair<std::string, float> const& a, std::pair<std::string, float> const& b) { return a.second < b.second; }
		);
		float sumOfLheWeights = std::accumulate(
				lheWeights.begin(), lheWeights.end(), 0.0,
				[](float const& a, std::pair<std::string, float> const& b) { return a + b.second; }
		);
		float sumOfQuadraticDifferences = std::sqrt(std::accumulate(
				lheWeights.begin(), lheWeights.end(), 0.0,
				[](float const& a, std::pair<std::string, float> const& b) { return a + std::pow(b.second - 1.0, 2); }
		));
		
		product.m_optionalWeights["min"+variationName+"LheWeight"] = minmaxPdfLheWeight.first->second;
		product.m_optionalWeights["max"+variationName+"LheWeight"] = minmaxPdfLheWeight.second->second;
		product.m_optionalWeights["mean"+variationName+"LheWeight"] = sumOfLheWeights / lheWeights.size();
		product.m_optionalWeights["stdev"+variationName+"LheWeight"] = (sumOfQuadraticDifferences / lheWeights.size()) + 1.0;
		
		if (nWeightsUp != 0)
		{
			product.m_optionalWeights["mean"+variationName+"LheWeightUp"] = sumOfLheWeightsUp / nWeightsUp;
			product.m_optionalWeights["stdev"+variationName+"LheWeightUp"] = (sumOfQuadraticDifferencesUp / nWeightsUp) + 1.0;
		}
		
		if (nWeightsDown != 0)
		{
			product.m_optionalWeights["mean"+variationName+"LheWeightDown"] = sumOfLheWeightsDown / nWeightsDown;
			product.m_optionalWeights["stdev"+variationName+"LheWeightDown"] = 1.0 - (sumOfQuadraticDifferencesDown / nWeightsDown);
		}
	}
}

