

#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/RecoTauCPProducer.h"

void RecoTauCPProducer::ProduceGlobal(HttEvent const& event, HttProduct& product,
									 HttGlobalSettings const& globalSettings) const
{
	for(unsigned int i=0;i<product.m_validElectrons.size();i++)
	{
		std::cout << product.m_validElectrons[i]->p4 << "   " << std::endl;
	}
	std::cout << std::endl;
}