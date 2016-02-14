
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/GenDiTauPairCandidatesProducers.h"


GenTTPairCandidatesProducer::GenTTPairCandidatesProducer() :
	GenDiTauPairCandidatesProducerBase<KGenJet, KGenJet>(
			&HttTypes::product_type::m_genTauJets,
			&HttTypes::product_type::m_genTauJets
	)
{
}

std::string GenTTPairCandidatesProducer::GetProducerId() const
{
	return "GenTTPairCandidatesProducer";
}


GenMTPairCandidatesProducer::GenMTPairCandidatesProducer() :
	GenDiTauPairCandidatesProducerBase<KGenParticle, KGenJet>(
			&HttTypes::product_type::m_genMuons,
			&HttTypes::product_type::m_genTauJets
	)
{
}

std::string GenMTPairCandidatesProducer::GetProducerId() const
{
	return "GenMTPairCandidatesProducer";
}


GenETPairCandidatesProducer::GenETPairCandidatesProducer() :
	GenDiTauPairCandidatesProducerBase<KGenParticle, KGenJet>(
			&HttTypes::product_type::m_genElectrons,
			&HttTypes::product_type::m_genTauJets
	)
{
}

std::string GenETPairCandidatesProducer::GetProducerId() const
{
	return "GenETPairCandidatesProducer";
}


GenEMPairCandidatesProducer::GenEMPairCandidatesProducer() :
	GenDiTauPairCandidatesProducerBase<KGenParticle, KGenParticle>(
			&HttTypes::product_type::m_genElectrons,
			&HttTypes::product_type::m_genMuons
	)
{
}

std::string GenEMPairCandidatesProducer::GetProducerId() const
{
	return "GenEMPairCandidatesProducer";
}


GenMMPairCandidatesProducer::GenMMPairCandidatesProducer() :
	GenDiTauPairCandidatesProducerBase<KGenParticle, KGenParticle>(
			&HttTypes::product_type::m_genMuons,
			&HttTypes::product_type::m_genMuons
	)
{
}

std::string GenMMPairCandidatesProducer::GetProducerId() const
{
	return "GenMMPairCandidatesProducer";
}


GenEEPairCandidatesProducer::GenEEPairCandidatesProducer() :
	GenDiTauPairCandidatesProducerBase<KGenParticle, KGenParticle>(
			&HttTypes::product_type::m_genElectrons,
			&HttTypes::product_type::m_genElectrons
	)
{
}

std::string GenEEPairCandidatesProducer::GetProducerId() const
{
	return "GenEEPairCandidatesProducer";
}

