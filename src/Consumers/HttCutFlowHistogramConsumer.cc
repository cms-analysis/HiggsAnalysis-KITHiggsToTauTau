
#include "Artus/Utility/interface/SafeMap.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/Consumers/HttCutFlowHistogramConsumer.h"


void HttCutFlowHistogramConsumer::Init(HttPipeline * pipeline)
{
	CutFlowHistogramConsumer<HttTypes>::Init(pipeline);
	
	weightExtractor = [](HttEvent const& event, HttProduct const& product) -> float {
		return SafeMap::GetWithDefault(product.m_weights, std::string("eventWeight"), 1.0);
	};
	
	m_addWeightedCutFlow = true;
}
