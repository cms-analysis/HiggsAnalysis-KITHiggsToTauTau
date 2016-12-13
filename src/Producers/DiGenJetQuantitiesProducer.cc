
#include "Artus/Consumer/interface/LambdaNtupleConsumer.h"
#include "Artus/Utility/interface/DefaultValues.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/DiGenJetQuantitiesProducer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/DiJetQuantitiesProducer.h"


std::string DiGenJetQuantitiesProducer::GetProducerId() const
{
	return "DiGenJetQuantitiesProducer";
}

void DiGenJetQuantitiesProducer::Init(setting_type const& settings)
{
	ProducerBase<HttTypes>::Init(settings);

	// add possible quantities for the lambda ntuples consumers
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("diGenJetMass", [this](event_type const& event, product_type const& product) {
		return DiJetQuantitiesProducer::GetDiJetQuantity(product, [](RMDLV diGenJetSystem) -> double
	{
		return diGenJetSystem.mass(); });
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("diGenJetPt", [this](event_type const& event, product_type const& product) {
		return DiJetQuantitiesProducer::GetDiJetQuantity(product, [](RMDLV diGenJetSystem) -> double
	{
		return diGenJetSystem.Pt(); });
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("diGenJetPhi", [this](event_type const& event, product_type const& product) {
		return DiJetQuantitiesProducer::GetDiJetQuantity(product, [](RMDLV diGenJetSystem) -> double
	{
		return diGenJetSystem.Phi(); });
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("diGenJetDeltaPhi", [](event_type const& event, product_type const& product) {
		return product.m_diGenJetSystemAvailable ? ROOT::Math::VectorUtil::DeltaPhi(product.m_validJets[0]->p4, product.m_validJets[1]->p4) :
		                                           DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("diGenJetAbsDeltaEta", [](event_type const& event, product_type const& product) {
		return product.m_diGenJetSystemAvailable ? std::abs(product.m_validJets[0]->p4.Eta() - product.m_validJets[1]->p4.Eta()) :
		                                           DefaultValues::UndefinedFloat;
	});
}

void DiGenJetQuantitiesProducer::Produce(event_type const& event, product_type& product,
	                                  setting_type const& settings) const
{
	if (product.m_validGenJets.size() >= 2)
	{
		product.m_diGenJetSystem = (product.m_validGenJets[0]->p4 + product.m_validGenJets[1]->p4);
		product.m_diGenJetSystemAvailable = true;
	}
	else
	{
		product.m_diGenJetSystemAvailable = false;
	}
}
