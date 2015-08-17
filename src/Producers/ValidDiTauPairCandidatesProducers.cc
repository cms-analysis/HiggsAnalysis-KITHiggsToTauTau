
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/ValidDiTauPairCandidatesProducers.h"


ValidTTPairCandidatesProducer::ValidTTPairCandidatesProducer() :
	ValidDiTauPairCandidatesProducerBase<KTau, KTau>(
			&HttTypes::product_type::m_validTaus,
			&HttTypes::product_type::m_validTaus
	)
{
}

std::string ValidTTPairCandidatesProducer::GetProducerId() const
{
	return "ValidTTPairCandidatesProducer";
}


ValidMTPairCandidatesProducer::ValidMTPairCandidatesProducer() :
	ValidDiTauPairCandidatesProducerBase<KMuon, KTau>(
			&HttTypes::product_type::m_validMuons,
			&HttTypes::product_type::m_validTaus
	)
{
}

std::string ValidMTPairCandidatesProducer::GetProducerId() const
{
	return "ValidMTPairCandidatesProducer";
}


ValidETPairCandidatesProducer::ValidETPairCandidatesProducer() :
	ValidDiTauPairCandidatesProducerBase<KElectron, KTau>(
			&HttTypes::product_type::m_validElectrons,
			&HttTypes::product_type::m_validTaus
	)
{
}

std::string ValidETPairCandidatesProducer::GetProducerId() const
{
	return "ValidETPairCandidatesProducer";
}


ValidEMPairCandidatesProducer::ValidEMPairCandidatesProducer() :
	ValidDiTauPairCandidatesProducerBase<KMuon, KElectron>(
			&HttTypes::product_type::m_validMuons,
			&HttTypes::product_type::m_validElectrons
	)
{
}

std::string ValidEMPairCandidatesProducer::GetProducerId() const
{
	return "ValidEMPairCandidatesProducer";
}


ValidMMPairCandidatesProducer::ValidMMPairCandidatesProducer() :
	ValidDiTauPairCandidatesProducerBase<KMuon, KMuon>(
			&HttTypes::product_type::m_validMuons,
			&HttTypes::product_type::m_validMuons
	)
{
}

std::string ValidMMPairCandidatesProducer::GetProducerId() const
{
	return "ValidMMPairCandidatesProducer";
}


ValidEEPairCandidatesProducer::ValidEEPairCandidatesProducer() :
	ValidDiTauPairCandidatesProducerBase<KElectron, KElectron>(
			&HttTypes::product_type::m_validElectrons,
			&HttTypes::product_type::m_validElectrons
	)
{
}

std::string ValidEEPairCandidatesProducer::GetProducerId() const
{
	return "ValidEEPairCandidatesProducer";
}

