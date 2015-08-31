
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Consumers/TriggerTagAndProbeConsumers.h"


MMTriggerTagAndProbeConsumer::MMTriggerTagAndProbeConsumer() :
	TriggerTagAndProbeConsumerBase<KMuon, KMuon>(
			"mmTriggerTP",
			&HttTypes::product_type::m_triggerTagProbeMuonPairs,
			&HttTypes::product_type::m_triggerTagProbeMuonMatchedPairs
	)
{
}

std::string MMTriggerTagAndProbeConsumer::GetConsumerId() const
{
	return "MMTriggerTagAndProbeConsumer";
}


EETriggerTagAndProbeConsumer::EETriggerTagAndProbeConsumer() :
	TriggerTagAndProbeConsumerBase<KElectron, KElectron>(
			"eeTriggerTP",
			&HttTypes::product_type::m_triggerTagProbeElectronPairs,
			&HttTypes::product_type::m_triggerTagProbeElectronMatchedPairs
	)
{
}

std::string EETriggerTagAndProbeConsumer::GetConsumerId() const
{
	return "EETriggerTagAndProbeConsumer";
}


MTTriggerTagAndProbeConsumer::MTTriggerTagAndProbeConsumer() :
	TriggerTagAndProbeConsumerBase<KMuon, KTau>(
			"mtTriggerTP",
			&HttTypes::product_type::m_triggerTagProbeMuonTauPairs,
			&HttTypes::product_type::m_triggerTagProbeMuonTauMatchedPairs
	)
{
}

std::string MTTriggerTagAndProbeConsumer::GetConsumerId() const
{
	return "MTTriggerTagAndProbeConsumer";
}


ETTriggerTagAndProbeConsumer::ETTriggerTagAndProbeConsumer() :
	TriggerTagAndProbeConsumerBase<KElectron, KTau>(
			"etTriggerTP",
			&HttTypes::product_type::m_triggerTagProbeElectronTauPairs,
			&HttTypes::product_type::m_triggerTagProbeElectronTauMatchedPairs
	)
{
}

std::string ETTriggerTagAndProbeConsumer::GetConsumerId() const
{
	return "ETTriggerTagAndProbeConsumer";
}
