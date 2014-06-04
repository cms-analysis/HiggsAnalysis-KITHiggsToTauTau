

#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/RecoTauCPProducer.h"

void RecoTauCPProducer::Produce(event_type const& event, product_type& product) const
{
	// Hadronic TauTau channel
	if(product.m_decayChannel == HttProduct::DecayChannel::TT)
	{
		
	}
}