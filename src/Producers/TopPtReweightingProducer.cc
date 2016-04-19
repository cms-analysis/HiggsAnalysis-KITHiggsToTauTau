
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/TopPtReweightingProducer.h"

std::string TopPtReweightingProducer::GetProducerId() const
{
	return "TopPtReweightingProducer";
}

void TopPtReweightingProducer::Produce( KappaEvent const& event,
			KappaProduct & product,
			KappaSettings const& settings) const
{
	assert(event.m_genEventInfo != nullptr);
	std::vector<KGenParticle> tops;
	for (auto particle : *(event.m_genParticles))
	//for (KGenParticles::iterator part = event.m_genParticles->begin(); part != event.m_genParticles->end(); ++part)
	{
		if(std::abs(particle.pdgId) == 6 && particle.isLastCopy()) tops.push_back(particle);
	}
	
	float topPtWeight;
	std::cout << tops.size() << std::endl;
	assert(tops.size() == 2);
	if ((tops.at(0).p4.Pt() > 400.0) && (tops.at(1).p4.Pt() > 400.0))
	{
		topPtWeight = sqrt(exp(0.156-0.00137*400.0)*exp(0.156-0.00137*400.0));
	}
	else if (tops.at(0).p4.Pt() > 400.0)
	{
		topPtWeight = sqrt(exp(0.156-0.00137*400.0)*exp(0.156-0.00137*tops.at(1).p4.Pt()));
	}
	else if (tops.at(1).p4.Pt() > 400.0)
	{
		topPtWeight = sqrt(exp(0.156-0.00137*400.0)*exp(0.156-0.00137*tops.at(0).p4.Pt()));
	}
	else
	{
		topPtWeight = sqrt(exp(0.156-0.00137*tops.at(0).p4.Pt())*exp(0.156-0.00137*tops.at(1).p4.Pt()));
	}
	product.m_optionalWeights["topPtReweightWeight"] = topPtWeight;
	
}
