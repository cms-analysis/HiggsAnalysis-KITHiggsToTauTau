
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/TriggerTagAndProbeProducers.h"


EETriggerTagAndProbeProducer::EETriggerTagAndProbeProducer() :
	TriggerTagAndProbeProducerBase<KElectron, KElectron>(
			&HttTypes::product_type::m_validElectrons,
			&HttTypes::product_type::m_validElectrons,
			&HttTypes::product_type::m_detailedTriggerMatchedElectrons,
			&HttTypes::product_type::m_detailedTriggerMatchedElectrons,
			&HttTypes::setting_type::GetTagLeptonHltPaths,
			&HttTypes::setting_type::GetProbeLeptonHltPaths,
			//&HttTypes::setting_type::GetTagLeptonTriggerFilterNames,
			//&HttTypes::setting_type::GetProbeLeptonTriggerFilterNames,
			&HttTypes::product_type::m_triggerTagProbeElectronPairs,
			&HttTypes::product_type::m_triggerTagProbeElectronMatchedPairs
	)
{
}

std::string EETriggerTagAndProbeProducer::GetProducerId() const
{
	return "EETriggerTagAndProbeProducer";
}


MMTriggerTagAndProbeProducer::MMTriggerTagAndProbeProducer() :
	TriggerTagAndProbeProducerBase<KMuon, KMuon>(
			&HttTypes::product_type::m_validMuons,
			&HttTypes::product_type::m_validMuons,
			&HttTypes::product_type::m_detailedTriggerMatchedMuons,
			&HttTypes::product_type::m_detailedTriggerMatchedMuons,
			&HttTypes::setting_type::GetTagLeptonHltPaths,
			&HttTypes::setting_type::GetProbeLeptonHltPaths,
			//&HttTypes::setting_type::GetTagLeptonTriggerFilterNames,
			//&HttTypes::setting_type::GetProbeLeptonTriggerFilterNames,
			&HttTypes::product_type::m_triggerTagProbeMuonPairs,
			&HttTypes::product_type::m_triggerTagProbeMuonMatchedPairs
	)
{
}

std::string MMTriggerTagAndProbeProducer::GetProducerId() const
{
	return "MMTriggerTagAndProbeProducer";
}


MTTriggerTagAndProbeProducer::MTTriggerTagAndProbeProducer() :
	TriggerTagAndProbeProducerBase<KMuon, KTau>(
			&HttTypes::product_type::m_validMuons,
			&HttTypes::product_type::m_validTaus,
			&HttTypes::product_type::m_detailedTriggerMatchedMuons,
			&HttTypes::product_type::m_detailedTriggerMatchedTaus,
			&HttTypes::setting_type::GetTagLeptonHltPaths,
			&HttTypes::setting_type::GetProbeLeptonHltPaths,
			//&HttTypes::setting_type::GetTagLeptonTriggerFilterNames,
			//&HttTypes::setting_type::GetProbeLeptonTriggerFilterNames,
			&HttTypes::product_type::m_triggerTagProbeMuonTauPairs,
			&HttTypes::product_type::m_triggerTagProbeMuonTauMatchedPairs
	)
{
}

std::string MTTriggerTagAndProbeProducer::GetProducerId() const
{
	return "MTTriggerTagAndProbeProducer";
}


ETTriggerTagAndProbeProducer::ETTriggerTagAndProbeProducer() :
	TriggerTagAndProbeProducerBase<KElectron, KTau>(
			&HttTypes::product_type::m_validElectrons,
			&HttTypes::product_type::m_validTaus,
			&HttTypes::product_type::m_detailedTriggerMatchedElectrons,
			&HttTypes::product_type::m_detailedTriggerMatchedTaus,
			&HttTypes::setting_type::GetTagLeptonHltPaths,
			&HttTypes::setting_type::GetProbeLeptonHltPaths,
			//&HttTypes::setting_type::GetTagLeptonTriggerFilterNames,
			//&HttTypes::setting_type::GetProbeLeptonTriggerFilterNames,
			&HttTypes::product_type::m_triggerTagProbeElectronTauPairs,
			&HttTypes::product_type::m_triggerTagProbeElectronTauMatchedPairs
	)
{
}

std::string ETTriggerTagAndProbeProducer::GetProducerId() const
{
	return "ETTriggerTagAndProbeProducer";
}

