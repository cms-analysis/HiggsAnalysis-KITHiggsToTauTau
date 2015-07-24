
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/DiTauPairCandidatesProducers.h"


TTPairCandidatesProducer::TTPairCandidatesProducer() :
	DiTauPairCandidatesProducerBase<KTau, KTau>(
			&HttTypes::product_type::m_validTaus,
			&HttTypes::product_type::m_validTaus
	)
{
}

std::string TTPairCandidatesProducer::GetProducerId() const
{
	return "TTPairCandidatesProducer";
}


MTPairCandidatesProducer::MTPairCandidatesProducer() :
	DiTauPairCandidatesProducerBase<KMuon, KTau>(
			&HttTypes::product_type::m_validMuons,
			&HttTypes::product_type::m_validTaus
	)
{
}

std::string MTPairCandidatesProducer::GetProducerId() const
{
	return "MTPairCandidatesProducer";
}


ETPairCandidatesProducer::ETPairCandidatesProducer() :
	DiTauPairCandidatesProducerBase<KElectron, KTau>(
			&HttTypes::product_type::m_validElectrons,
			&HttTypes::product_type::m_validTaus
	)
{
}

std::string ETPairCandidatesProducer::GetProducerId() const
{
	return "ETPairCandidatesProducer";
}


EMPairCandidatesProducer::EMPairCandidatesProducer() :
	DiTauPairCandidatesProducerBase<KMuon, KElectron>(
			&HttTypes::product_type::m_validMuons,
			&HttTypes::product_type::m_validElectrons
	)
{
}

std::string EMPairCandidatesProducer::GetProducerId() const
{
	return "EMPairCandidatesProducer";
}


MMPairCandidatesProducer::MMPairCandidatesProducer() :
	DiTauPairCandidatesProducerBase<KMuon, KMuon>(
			&HttTypes::product_type::m_validMuons,
			&HttTypes::product_type::m_validMuons
	)
{
}

std::string MMPairCandidatesProducer::GetProducerId() const
{
	return "MMPairCandidatesProducer";
}


EEPairCandidatesProducer::EEPairCandidatesProducer() :
	DiTauPairCandidatesProducerBase<KElectron, KElectron>(
			&HttTypes::product_type::m_validElectrons,
			&HttTypes::product_type::m_validElectrons
	)
{
}

std::string EEPairCandidatesProducer::GetProducerId() const
{
	return "EEPairCandidatesProducer";
}

