
#include "Artus/Consumer/interface/LambdaNtupleConsumer.h"
#include "Artus/Utility/interface/DefaultValues.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/DiJetQuantitiesProducer.h"


double DiJetQuantitiesProducer::GetDiJetQuantity(product_type const& product,
                                                 dijet_extractor_lambda dijetQuantity)
{
	return ((static_cast<HttProduct const&>(product)).m_diJetSystemAvailable ? dijetQuantity((static_cast<HttProduct const&>(product)).m_diJetSystem) : DefaultValues::UndefinedDouble);
}

void DiJetQuantitiesProducer::Init(setting_type const& settings)
{
	ProducerBase<HttTypes>::Init(settings);
	
	// add possible quantities for the lambda ntuples consumers
	LambdaNtupleConsumer<HttTypes>::AddQuantity("diJetMass", [this](event_type const& event, product_type const& product) {
		return DiJetQuantitiesProducer::GetDiJetQuantity(product, [](RMLV diJetSystem) -> double
	{
		return diJetSystem.mass(); });
	});
	LambdaNtupleConsumer<HttTypes>::AddQuantity("diJetDeltaPhi", [](event_type const& event, product_type const& product) {
		return product.m_diJetSystemAvailable ? ROOT::Math::VectorUtil::DeltaR(product.m_validJets[0]->p4, product.m_validJets[1]->p4) :
		                                        DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddQuantity("diJetAbsDeltaEta", [](event_type const& event, product_type const& product) {
		return product.m_diJetSystemAvailable ? std::abs(product.m_validJets[0]->p4.Eta() - product.m_validJets[1]->p4.Eta()) :
		                                        DefaultValues::UndefinedDouble;
	});
}

void DiJetQuantitiesProducer::Produce(event_type const& event, product_type& product,
	                                  setting_type const& settings) const
{
	if (KappaProduct::GetNJetsAbovePtThreshold(product.m_validJets, 20.0) >= 2)
	{
		product.m_diJetSystem = (product.m_validJets[0]->p4 + product.m_validJets[1]->p4);
		product.m_diJetSystemAvailable = true;
	}
	else
	{
		product.m_diJetSystemAvailable = false;
	}
}
