
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/ElectronEtaSelector.h"


void ElectronEtaSelector::Produce(event_type const& event, product_type& product) const
{
	for (KDataElectrons::iterator electron = event.m_electrons->begin();
		 electron != event.m_electrons->end(); electron++)
	{
		// This modifies the const event, which is possible due to the const pointer
		// of the electrons vector but should be avoided in normal cases.
		electron->p4.SetEta(electron->superclusterposition.Eta());
	}
}

