
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
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("diJetMass", [this](event_type const& event, product_type const& product) {
		return DiJetQuantitiesProducer::GetDiJetQuantity(product, [](RMDLV diJetSystem) -> double
	{
		return diJetSystem.mass(); });
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("diJetDeltaPhi", [](event_type const& event, product_type const& product) {
		return product.m_diJetSystemAvailable ? ROOT::Math::VectorUtil::DeltaR(product.m_validJets[0]->p4, product.m_validJets[1]->p4) :
		                                        DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("diJetAbsDeltaEta", [](event_type const& event, product_type const& product) {
		return product.m_diJetSystemAvailable ? std::abs(product.m_validJets[0]->p4.Eta() - product.m_validJets[1]->p4.Eta()) :
		                                        DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddBoolQuantity("centralJet30Exists", [](event_type const& event, product_type const& product) {
		return product.m_centralJet30Exists;
	});
}

void DiJetQuantitiesProducer::Produce(event_type const& event, product_type& product,
	                                  setting_type const& settings) const
{
	// central jet veto
	product.m_centralJet30Exists = false;
	if (KappaProduct::GetNJetsAbovePtThreshold(product.m_validJets, 30.0) >= 2)
	{
		float minJetEta = std::min(product.m_validJets[0]->p4.Eta(), product.m_validJets[1]->p4.Eta());
		float maxJetEta = std::max(product.m_validJets[0]->p4.Eta(), product.m_validJets[1]->p4.Eta());
		for (std::vector<KBasicJet*>::const_iterator jet = product.m_validJets.begin();
		     ((jet != product.m_validJets.end()) && ((*jet)->p4.Pt() > 30.0) && (! product.m_centralJet30Exists)); ++jet)
		{
			// skip first two jets
			if ((*jet) == product.m_validJets[0]) continue;
			if ((*jet) == product.m_validJets[1]) continue;
			
			if ((minJetEta < (*jet)->p4.Eta()) && ((*jet)->p4.Eta() < maxJetEta))
			{
				product.m_centralJet30Exists = true;
			}
		}
	}

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
