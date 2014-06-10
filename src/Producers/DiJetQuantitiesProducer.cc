
#include "Artus/Utility/interface/DefaultValues.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/DiJetQuantitiesProducer.h"


double DiJetQuantitiesProducer::GetDiJetQuantity(product_type const& product,
                                                 dijet_extractor_lambda dijetQuantity)
{
	return (product.m_diJetSystemAvailable ? dijetQuantity(product.m_diJetSystem) : DefaultValues::UndefinedDouble);
}

void DiJetQuantitiesProducer::Produce(event_type const& event, product_type& product,
	                                  setting_type const& settings) const
{
	if (product.m_validJets.size() >= 2)
	{
		product.m_diJetSystem = (product.m_validJets[0]->p4 + product.m_validJets[1]->p4);
		product.m_diJetSystemAvailable = true;
	}
	else
	{
		product.m_diJetSystemAvailable = false;
	}
}
