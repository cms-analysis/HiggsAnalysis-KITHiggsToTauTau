

#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/RecoTauCPProducer.h"

void RecoTauCPProducer::Produce(event_type const& event, product_type& product, setting_type const& settings) const
{
	// Hadronic TauTau channel
	if(product.m_decayChannel == HttProduct::DecayChannel::TT)
	{
		KDataPFTau* tau1 = static_cast<KDataPFTau*>(product.m_flavourOrderedLeptons[0]);
		KDataPFTau* tau2 = static_cast<KDataPFTau*>(product.m_flavourOrderedLeptons[1]);
		if(tau1->signalChargedHadrCands.size()==1 && tau2->signalChargedHadrCands.size()==1)
		{
			KPFCandidate* chargePart1 = &(tau1->signalChargedHadrCands[0]);
			KPFCandidate* chargePart2 = &(tau2->signalChargedHadrCands[0]);
			product.RecoPhiStar = (CPQuantities::CalculatePhiPsiStar(tau1->p4, tau2->p4, chargePart1->p4, chargePart2->p4) ).first;
		}
		else product.RecoPhiStar = DefaultValues::UndefinedDouble;
	}
	else product.RecoPhiStar = DefaultValues::UndefinedDouble;
}