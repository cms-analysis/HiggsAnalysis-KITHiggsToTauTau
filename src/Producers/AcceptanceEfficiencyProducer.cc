#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/AcceptanceEfficiencyProducer.h"

void AcceptanceEfficiencyProducer::Init(setting_type const& settings)
{
	ProducerBase<HttTypes>::Init(settings);
}

void AcceptanceEfficiencyProducer::Produce(event_type const& event, product_type& product, setting_type const& settings) const
{
	//std::cout << "acceptance weight = " << event.m_genEventInfo->weight << " particles: ";
	for (KGenParticles::iterator part = event.m_genParticles->begin(); part != event.m_genParticles->end(); ++part)
	{
		if (part->pdgId == 15) product.m_accEffTauMinus = &(*part);
		else if (part->pdgId == -15) product.m_accEffTauPlus = &(*part);
		//std::cout << part->pdgId << " ";
	}
	std::cout << "| ";
	product.m_accEffDC = DetermineDecayChannel(event, product.m_accEffTauMinus, product.m_accEffTauPlus);
	std::cout << "Pt Tau Minus: " << product.m_accEffTauMinus->p4.Pt() << std::endl;
}

unsigned int AcceptanceEfficiencyProducer::DetermineDecayChannel(event_type const& event, KGenParticle* tau1, KGenParticle* tau2) const
{
	std::cout << "Pt's: "<< tau1->p4.Pt() << " " << tau2->p4.Pt() << " | ";
	unsigned int countMuons, countElectrons;
	countElectrons = 0;
	countMuons = 0;
	
	for (std::vector<unsigned int>::const_iterator daughter_ind = tau1->daughterIndices.begin(); daughter_ind != tau1->daughterIndices.end(); ++daughter_ind)
	{
		if (std::abs(event.m_genParticles->at(*daughter_ind).pdgId) == 11) ++countElectrons;
		else if (std::abs(event.m_genParticles->at(*daughter_ind).pdgId) == 13) ++countMuons;
	}
	
	for (std::vector<unsigned int>::const_iterator daughter_ind = tau2->daughterIndices.begin(); daughter_ind != tau2->daughterIndices.end(); ++daughter_ind)
	{
		if (std::abs(event.m_genParticles->at(*daughter_ind).pdgId) == 11) ++countElectrons;
		else if (std::abs(event.m_genParticles->at(*daughter_ind).pdgId) == 13) ++countMuons;
	}
	//std::cout << "muons: " << countMuons << " " << "electrons: " << countElectrons << std::endl;
	if (countElectrons == 2) return 1;
	else if (countMuons == 2) return 2;
	else if (countElectrons == 0 && countMuons == 0) return 3;
	else if (countElectrons == 1 && countMuons == 1) return 4;
	else if (countElectrons == 1 && countMuons == 0) return 5;
	else if (countElectrons == 0 && countMuons == 1) return 6;
	return 0;
}
