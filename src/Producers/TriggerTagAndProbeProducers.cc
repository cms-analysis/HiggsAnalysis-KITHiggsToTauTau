
#include "Artus/Consumer/interface/LambdaNtupleConsumer.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/TriggerTagAndProbeProducers.h"


LeptonTriggerTagAndProbeProducer::LeptonTriggerTagAndProbeProducer() :
	TriggerTagAndProbeProducerBase<KLepton>(
			&HttTypes::product_type::m_ptOrderedLeptons,
			&HttTypes::product_type::m_detailedTriggerMatchedLeptons,
			&HttTypes::setting_type::GetTagLeptonHltPaths,
			&HttTypes::setting_type::GetProbeLeptonHltPaths,
			//&HttTypes::setting_type::GetTagLeptonTriggerFilterNames,
			//&HttTypes::setting_type::GetProbeLeptonTriggerFilterNames,
			&HttTypes::product_type::m_triggerTagLeptonAvailable,
			&HttTypes::product_type::m_triggerProbeLeptonAvailable
	)
{
}

std::string LeptonTriggerTagAndProbeProducer::GetProducerId() const
{
	return "LeptonTriggerTagAndProbeProducer";
}

void LeptonTriggerTagAndProbeProducer::Init(setting_type const& settings)
{
	TriggerTagAndProbeProducerBase<KLepton>::Init(settings);
	
	// add possible quantities for the lambda ntuples consumers
	LambdaNtupleConsumer<HttTypes>::AddBoolQuantity("triggerTagLeptonAvailable", [](event_type const& event, product_type const& product)
	{
		return product.m_triggerTagLeptonAvailable;
	});
	LambdaNtupleConsumer<HttTypes>::AddBoolQuantity("triggerProbeLeptonAvailable", [](event_type const& event, product_type const& product)
	{
		return product.m_triggerProbeLeptonAvailable;
	});
}
