
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/ElectronEtaSelector.h"


void ElectronEtaSelector::Produce(event_type const& event, product_type& product,
	                              setting_type const& settings, metadata_type const& metadata) const
{
	assert(event.m_electrons);
	
	for (KElectrons::iterator electron = event.m_electrons->begin();
		 electron != event.m_electrons->end(); electron++)
	{
		// This modifies the const event, which is possible due to the const pointer
		// of the electrons vector but should be avoided in normal cases.
		electron->p4.SetEta(electron->superclusterPosition.Eta());
	}
}

