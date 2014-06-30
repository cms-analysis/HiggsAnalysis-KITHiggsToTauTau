

#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/RecoTauCPProducer.h"

void RecoTauCPProducer::Produce(event_type const& event, product_type& product, setting_type const& settings) const
{
	// Hadronic TauTau channel
	//std::cout << (product.m_validTaus[0])->signalNeutrHadrCands.size() << std::endl;
	if(product.m_decayChannel == HttProduct::DecayChannel::TT  && product.m_tauTauMomentaReconstructed)
	{
		KDataPFTau* tau1 = product.m_validTaus[0];
		KDataPFTau* tau2 = product.m_validTaus[1];
		RMDataLV Tau1Mom = static_cast<RMDataLV>(product.m_flavourOrderedTauTauMomenta[0]);
		RMDataLV Tau2Mom = static_cast<RMDataLV>(product.m_flavourOrderedTauTauMomenta[1]);
		// Decays, which are compatible with collinear approximatiom, e.g. there are detectable neutral particles
		if(tau1->signalChargedHadrCands.size()==1 && tau2->signalChargedHadrCands.size()==1 /*&& tau1->signalNeutrHadrCands.size()!=0 && tau2->signalNeutrHadrCands.size()!=0*/)
		{
			//std::cout << "Taus: " << tau1->p4 << "       " << tau2->p4 << std::endl;
			KPFCandidate* chargePart1 = &(tau1->signalChargedHadrCands[0]);
			KPFCandidate* chargePart2 = &(tau2->signalChargedHadrCands[0]);
			//std::cout << "Hadrons: " << chargePart1->p4 << "       " << chargePart2->p4 << std::endl;
			product.RecoPhiStar = (CPQuantities::CalculatePhiPsiStar(Tau1Mom, Tau2Mom, chargePart1->p4, chargePart2->p4) ).first;

				//std::cout << "Difference of Tau1 and chargePart1 Pt: " << Tau1Mom.Pt()-chargePart1->p4.Pt() << std::endl;
				//std::cout << "Mass DiTau System: " << (Tau1Mom+Tau2Mom).mass() << std::endl;
		}
		else product.RecoPhiStar = DefaultValues::UndefinedDouble;
	}
	else if (product.m_decayChannel == HttProduct::DecayChannel::EE  && product.m_tauTauMomentaReconstructed)
	{
		KDataElectron* electron1 = product.m_validElectrons[0];
		KDataElectron* electron2 = product.m_validElectrons[1];
		RMDataLV Tau1Mom = static_cast<RMDataLV>(product.m_flavourOrderedTauTauMomenta[0]);
		RMDataLV Tau2Mom = static_cast<RMDataLV>(product.m_flavourOrderedTauTauMomenta[1]);
		product.RecoPhiStar = (CPQuantities::CalculatePhiPsiStar(Tau1Mom, Tau2Mom, electron1->p4, electron2->p4) ).first;
	}
	else if (product.m_decayChannel == HttProduct::DecayChannel::MM  && product.m_tauTauMomentaReconstructed)
	{
		KDataMuon* muon1 = product.m_validMuons[0];
		KDataMuon* muon2 = product.m_validMuons[1];
		RMDataLV Tau1Mom = static_cast<RMDataLV>(product.m_flavourOrderedTauTauMomenta[0]);
		RMDataLV Tau2Mom = static_cast<RMDataLV>(product.m_flavourOrderedTauTauMomenta[1]);
		product.RecoPhiStar = (CPQuantities::CalculatePhiPsiStar(Tau1Mom, Tau2Mom, muon1->p4, muon2->p4) ).first;
	}
	else if (product.m_decayChannel == HttProduct::DecayChannel::ET  && product.m_tauTauMomentaReconstructed)
	{
		KDataElectron* electron1 = product.m_validElectrons[0];
		KDataPFTau* tau1 = product.m_validTaus[0];
		RMDataLV Tau1Mom = static_cast<RMDataLV>(product.m_flavourOrderedTauTauMomenta[0]);
		RMDataLV Tau2Mom = static_cast<RMDataLV>(product.m_flavourOrderedTauTauMomenta[1]);
		if (tau1->signalChargedHadrCands.size()==1 /* && tau1->signalNeutrHadrCands.size()!=0 */)
		{
			KPFCandidate* chargePart1 = &(tau1->signalChargedHadrCands[0]);
			product.RecoPhiStar = (CPQuantities::CalculatePhiPsiStar(Tau1Mom, Tau2Mom, electron1->p4, chargePart1->p4) ).first;
		}
		else product.RecoPhiStar = DefaultValues::UndefinedDouble;
	}
	else if (product.m_decayChannel == HttProduct::DecayChannel::MT  && product.m_tauTauMomentaReconstructed)
	{
		KDataMuon* muon1 = product.m_validMuons[0];
		KDataPFTau* tau1 = product.m_validTaus[0];
		RMDataLV Tau1Mom = static_cast<RMDataLV>(product.m_flavourOrderedTauTauMomenta[0]);
		RMDataLV Tau2Mom = static_cast<RMDataLV>(product.m_flavourOrderedTauTauMomenta[1]);
		if (tau1->signalChargedHadrCands.size()==1 /* && tau1->signalNeutrHadrCands.size()!=0 */)
		{
			KPFCandidate* chargePart1 = &(tau1->signalChargedHadrCands[0]);
			product.RecoPhiStar = (CPQuantities::CalculatePhiPsiStar(Tau1Mom, Tau2Mom, muon1->p4, chargePart1->p4) ).first;
		}
		else product.RecoPhiStar = DefaultValues::UndefinedDouble;
	}
	else if (product.m_decayChannel == HttProduct::DecayChannel::EM  && product.m_tauTauMomentaReconstructed)
	{
		KDataElectron* electron1 = product.m_validElectrons[0];
		KDataMuon* muon1 = product.m_validMuons[0];
		RMDataLV Tau1Mom = static_cast<RMDataLV>(product.m_flavourOrderedTauTauMomenta[0]);
		RMDataLV Tau2Mom = static_cast<RMDataLV>(product.m_flavourOrderedTauTauMomenta[1]);
		product.RecoPhiStar = (CPQuantities::CalculatePhiPsiStar(Tau1Mom, Tau2Mom, electron1->p4, muon1->p4) ).first;
	}
	else product.RecoPhiStar = DefaultValues::UndefinedDouble;
}
