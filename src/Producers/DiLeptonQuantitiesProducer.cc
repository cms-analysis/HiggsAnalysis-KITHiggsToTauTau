
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/DiLeptonQuantitiesProducer.h"


void DiLeptonQuantitiesProducer::Produce(event_type const& event, product_type& product,
	                                     setting_type const& settings) const
{
	product.m_diLeptonSystem = (product.m_ptOrderedLeptons[0]->p4 + product.m_ptOrderedLeptons[1]->p4);
}
