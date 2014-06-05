
#include "Artus/Utility/interface/DefaultValues.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/DecayChannelProducer.h"


void DecayChannelProducer::Produce(event_type const& event, product_type& product,
	                               setting_type const& settings) const
{
	
	product.m_decayChannel = HttProduct::DecayChannel::NONE;
	
	KLepton* lepton1 = 0;
	KLepton* lepton2 = 0;
	
	size_t nElectrons = product.m_validElectrons.size();
	size_t nMuons = product.m_validMuons.size();
	size_t nTaus = product.m_validTaus.size();
	
	if (nElectrons == 2)
	{
		lepton1 = product.m_validElectrons[0];
		lepton2 = product.m_validElectrons[1];
		product.m_decayChannel = HttProduct::DecayChannel::EE;
	}
	else if (nElectrons == 1)
	{
		if (nMuons == 1)
		{
			lepton1 = product.m_validElectrons[0];
			lepton2 = product.m_validMuons[0];
			product.m_decayChannel = HttProduct::DecayChannel::EM;
		}
		else if (nTaus >= 1)
		{
			lepton1 = product.m_validElectrons[0];
			lepton2 = product.m_validTaus[0];
			product.m_decayChannel = HttProduct::DecayChannel::ET;
		}
	}
	else if (nElectrons == 0)
	{
		if (nMuons == 2)
		{
			lepton1 = product.m_validMuons[0];
			lepton2 = product.m_validMuons[1];
			product.m_decayChannel = HttProduct::DecayChannel::MM;
		}
		else if (nMuons == 1 && nTaus >= 1)
		{
			lepton1 = product.m_validMuons[0];
			lepton2 = product.m_validTaus[0];
			product.m_decayChannel = HttProduct::DecayChannel::MT;
		}
		else if (nTaus >= 2)
		{
			lepton1 = product.m_validTaus[0];
			lepton2 = product.m_validTaus[1];
			product.m_decayChannel = HttProduct::DecayChannel::TT;
		}
	}

	if(product.m_decayChannel != HttProduct::DecayChannel::NONE) {
		
		// fill p4 pointers ordered by pt
		if(lepton1->p4.Pt() >= lepton2->p4.Pt()) {
			product.m_ptOrderedLeptons.push_back(lepton1);
			product.m_ptOrderedLeptons.push_back(lepton2);
		}
		else {
			product.m_ptOrderedLeptons.push_back(lepton2);
			product.m_ptOrderedLeptons.push_back(lepton1);
		}
		
		// fill p4 pointers ordered by flavour (according to channel name)
		product.m_flavourOrderedLeptons.push_back(lepton1);
		product.m_flavourOrderedLeptons.push_back(lepton2);
	}
}
