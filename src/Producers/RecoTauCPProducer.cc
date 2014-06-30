

#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/RecoTauCPProducer.h"

void RecoTauCPProducer::Produce(event_type const& event, product_type& product, setting_type const& settings) const
{
	// Hadronic TauTau channel
	if(product.m_decayChannel == HttProduct::DecayChannel::TT  && product.m_tauTauMomentaReconstructed)
	{
		KDataPFTau* tau1 = product.m_validTaus[0];
		KDataPFTau* tau2 = product.m_validTaus[1];
		RMDataLV Tau1Mom = static_cast<RMDataLV>(product.m_tauTauMomenta[0]);
		RMDataLV Tau2Mom = static_cast<RMDataLV>(product.m_tauTauMomenta[1]);
		if(tau1->signalChargedHadrCands.size()==1 && tau2->signalChargedHadrCands.size()==1)
		{
			//std::cout << "Taus: " << tau1->p4 << "       " << tau2->p4 << std::endl;
			KPFCandidate* chargePart1 = &(tau1->signalChargedHadrCands[0]);
			KPFCandidate* chargePart2 = &(tau2->signalChargedHadrCands[0]);
			//std::cout << "Hadrons: " << chargePart1->p4 << "       " << chargePart2->p4 << std::endl;
			product.RecoPhiStar = (CPQuantities::CalculatePhiPsiStar(Tau1Mom, Tau2Mom, chargePart1->p4, chargePart2->p4) ).first;
			if (abs(product.RecoPhiStar - ROOT::Math::Pi()/2.0)<0.01)
			{
				//std::cout << "Difference of Tau1 and chargePart1 Pt: " << Tau1Mom.Pt()-chargePart1->p4.Pt() << std::endl;
				std::cout << "Mass DiTau System: " << (Tau1Mom+Tau2Mom).mass() << std::endl;
			}
		}
		else product.RecoPhiStar = DefaultValues::UndefinedDouble;
	}
	else product.RecoPhiStar = DefaultValues::UndefinedDouble;
}
