

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttEnumTypes.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/RecoTauCPProducer.h"


void RecoTauCPProducer::Produce(event_type const& event, product_type& product, setting_type const& settings) const
{
	// Hadronic TauTau channel
	//std::cout << (product.m_validTaus[0])->signalNeutrHadrCands.size() << std::endl;
	if(product.m_decayChannel == HttProduct::DecayChannel::TT)
	{
		KDataVertex primevertex = event.m_vertexSummary->pv;
		KDataPFTau* tau1 = product.m_validTaus[0];
		KDataPFTau* tau2 = product.m_validTaus[1];
		if(tau1->signalChargedHadrCands.size()==1 && tau2->signalChargedHadrCands.size()==1)
		{
			KPFCandidate* chargePart1 = &(tau1->signalChargedHadrCands[0]);
			KPFCandidate* chargePart2 = &(tau2->signalChargedHadrCands[0]);
			product.m_recoPhiStarCP = CPQuantities::CalculatePhiStarCP(primevertex, tau1->track, tau2->track, chargePart1->p4, chargePart2->p4);
		}
		else product.m_recoPhiStarCP = DefaultValues::UndefinedDouble;
	}

	else if (product.m_decayChannel == HttProduct::DecayChannel::EE)
	{
		KDataVertex primevertex = event.m_vertexSummary->pv;
		KDataElectron* electron1 = product.m_validElectrons[0];
		KDataElectron* electron2 = product.m_validElectrons[1];
		product.m_recoPhiStarCP = CPQuantities::CalculatePhiStarCP(primevertex, electron1->track, electron2->track, electron1->p4, electron2->p4);
	}
	else if (product.m_decayChannel == HttProduct::DecayChannel::MM)
	{
		KDataVertex primevertex = event.m_vertexSummary->pv;
		KDataMuon* muon1 = product.m_validMuons[0];
		KDataMuon* muon2 = product.m_validMuons[1];
		product.m_recoPhiStarCP = CPQuantities::CalculatePhiStarCP(primevertex, muon1->track, muon2->track, muon1->p4, muon2->p4);
	}
	else if (product.m_decayChannel == HttProduct::DecayChannel::ET)
	{
		KDataVertex primevertex = event.m_vertexSummary->pv;
		KDataElectron* electron1 = product.m_validElectrons[0];
		KDataPFTau* tau1 = product.m_validTaus[0];
		if (tau1->signalChargedHadrCands.size()==1)
		{
			KPFCandidate* chargePart1 = &(tau1->signalChargedHadrCands[0]);
			product.m_recoPhiStarCP = CPQuantities::CalculatePhiStarCP(primevertex, electron1->track, tau1->track, electron1->p4, chargePart1->p4);
		}
		else product.m_recoPhiStarCP = DefaultValues::UndefinedDouble;
	}
	else if (product.m_decayChannel == HttProduct::DecayChannel::MT)
	{
		KDataVertex primevertex = event.m_vertexSummary->pv;
		KDataMuon* muon1 = product.m_validMuons[0];
		KDataPFTau* tau1 = product.m_validTaus[0];
		if (tau1->signalChargedHadrCands.size()==1
		{
			KPFCandidate* chargePart1 = &(tau1->signalChargedHadrCands[0]);
			product.m_recoPhiStarCP = CPQuantities::CalculatePhiStarCP(primevertex, muon1->track, tau1->track, muon1->p4, chargePart1->p4);
		}
		else product.m_recoPhiStarCP = DefaultValues::UndefinedDouble;
	}
	else if (product.m_decayChannel == HttProduct::DecayChannel::EM)
	{
		KDataVertex primevertex = event.m_vertexSummary->pv;
		KDataElectron* electron1 = product.m_validElectrons[0];
		KDataMuon* muon1 = product.m_validMuons[0];
		product.m_recoPhiStarCP = CPQuantities::CalculatePhiStarCP(primevertex, electron1->track, muon1->track, electron1->p4, muon1->p4);
	}
	else product.m_recoPhiStarCP = DefaultValues::UndefinedDouble;
}
