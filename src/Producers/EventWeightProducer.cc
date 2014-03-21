
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/EventWeightProducer.h"


void EventWeightProducer::ProduceLocal(HttEvent const& event, HttProduct& product,
                                       HttPipelineSettings const& settings) const
{
	double eventWeight = 1.0;
	
	// loop over all previously calculated weights and multiply them
	for(std::map<std::string, double>::const_iterator weight = product.m_weights.begin();
	    weight != product.m_weights.end(); ++weight)
	{
		eventWeight *= weight->second;
	}
	
	product.m_weights["eventWeight"] = eventWeight;
}
