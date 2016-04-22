
#include "Artus/Consumer/interface/LambdaNtupleConsumer.h"
#include "Artus/Utility/interface/DefaultValues.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/DiJetQuantitiesProducer.h"


double DiJetQuantitiesProducer::GetDiJetQuantity(product_type const& product,
                                                 dijet_extractor_lambda dijetQuantity)
{
	return ((static_cast<HttProduct const&>(product)).m_diJetSystemAvailable ? dijetQuantity((static_cast<HttProduct const&>(product)).m_diJetSystem) : -1);
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
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("diJetPt", [this](event_type const& event, product_type const& product) {
		return DiJetQuantitiesProducer::GetDiJetQuantity(product, [](RMDLV diJetSystem) -> double
	{
		return diJetSystem.Pt(); });
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("diJetPhi", [this](event_type const& event, product_type const& product) {
		return DiJetQuantitiesProducer::GetDiJetQuantity(product, [](RMDLV diJetSystem) -> double
	{
		return diJetSystem.Phi(); });
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("diJetDeltaPhi", [](event_type const& event, product_type const& product) {
		return product.m_diJetSystemAvailable ? ROOT::Math::VectorUtil::DeltaR(product.m_validJets[0]->p4, product.m_validJets[1]->p4) :
		                                        DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("diJetAbsDeltaEta", [](event_type const& event, product_type const& product) {
		return product.m_diJetSystemAvailable ? std::abs(product.m_validJets[0]->p4.Eta() - product.m_validJets[1]->p4.Eta()) :
		                                        -1;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("diJetdiLepPhi", [](event_type const& event, product_type const& product) {
		return product.m_diJetSystemAvailable ? (product.m_diJetSystem + product.m_diLeptonSystem).Phi() :
		                                        DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddBoolQuantity("centralJet30Exists", [](event_type const& event, product_type const& product) {
		return (product.m_nCentralJets30 > 0 ? true : false);
	});
	LambdaNtupleConsumer<HttTypes>::AddIntQuantity("nCentralJets20", [](event_type const& event, product_type const& product) {
		return product.m_nCentralJets20;
	});
	LambdaNtupleConsumer<HttTypes>::AddIntQuantity("nCentralJets30", [](event_type const& event, product_type const& product) {
		return product.m_nCentralJets30;
	});
}

void DiJetQuantitiesProducer::Produce(event_type const& event, product_type& product,
	                                  setting_type const& settings) const
{
	// central jet veto
	product.m_nCentralJets30 = 0;
	if (KappaProduct::GetNJetsAbovePtThreshold(product.m_validJets, 30.0) >= 2)
	{
		float minJetEta = std::min(product.m_validJets[0]->p4.Eta(), product.m_validJets[1]->p4.Eta());
		float maxJetEta = std::max(product.m_validJets[0]->p4.Eta(), product.m_validJets[1]->p4.Eta());
		for (std::vector<KBasicJet*>::const_iterator jet = product.m_validJets.begin();
		     jet != product.m_validJets.end(); ++jet)
		{
			// skip first two jets
			if ((*jet) == product.m_validJets[0]) continue;
			if ((*jet) == product.m_validJets[1]) continue;

			if ((minJetEta < (*jet)->p4.Eta()) && ((*jet)->p4.Eta() < maxJetEta))
			{
				if ((*jet)->p4.Pt() > 20.0)
					product.m_nCentralJets20++;

				if ((*jet)->p4.Pt() > 30.0)
					product.m_nCentralJets30++;
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
