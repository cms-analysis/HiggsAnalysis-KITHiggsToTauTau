
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Consumers/TriggerTagAndProbeConsumers.h"


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
