
#include "Artus/Consumer/interface/LambdaNtupleConsumer.h"
#include "Artus/Utility/interface/DefaultValues.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/DiJetQuantitiesProducer.h"


double DiJetQuantitiesProducer::GetDiJetQuantity(product_type const& product,
                                                 dijet_extractor_lambda dijetQuantity)
{
	return ((static_cast<HttProduct const&>(product)).m_diJetSystemAvailable ? dijetQuantity((static_cast<HttProduct const&>(product)).m_diJetSystem) : -11);
}

void DiJetQuantitiesProducer::Init(setting_type const& settings, metadata_type& metadata)
{
	ProducerBase<HttTypes>::Init(settings, metadata);

	// add possible quantities for the lambda ntuples consumers
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "diJetPt", [this](event_type const& event, product_type const& product) {
		return DiJetQuantitiesProducer::GetDiJetQuantity(product, [](RMDLV diJetSystem) -> double
	{
		return diJetSystem.Pt(); });
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "diJetEta", [this](event_type const& event, product_type const& product) {
		return DiJetQuantitiesProducer::GetDiJetQuantity(product, [](RMDLV diJetSystem) -> double
	{
		return diJetSystem.Eta(); });
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "diJetPhi", [this](event_type const& event, product_type const& product) {
		return DiJetQuantitiesProducer::GetDiJetQuantity(product, [](RMDLV diJetSystem) -> double
	{
		return diJetSystem.Phi(); });
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "diJetMass", [this](event_type const& event, product_type const& product) {
		return DiJetQuantitiesProducer::GetDiJetQuantity(product, [](RMDLV diJetSystem) -> double
	{
		return diJetSystem.mass(); });
	});
	
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "diJetDeltaPhi", [](event_type const& event, product_type const& product) {
		return product.m_diJetSystemAvailable ? ROOT::Math::VectorUtil::DeltaPhi(product.m_validJets[0]->p4, product.m_validJets[1]->p4) :
		                                        DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "diJetAbsDeltaEta", [](event_type const& event, product_type const& product) {
		return product.m_diJetSystemAvailable ? std::abs(product.m_validJets[0]->p4.Eta() - product.m_validJets[1]->p4.Eta()) :
		                                        -1;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "diJetdiLepPhi", [](event_type const& event, product_type const& product) {
		return product.m_diJetSystemAvailable ? (product.m_diJetSystem + product.m_diLeptonSystem).Phi() :
		                                        DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddBoolQuantity(metadata, "centralJet30Exists", [](event_type const& event, product_type const& product) {
		return (product.m_nCentralJets30 > 0 ? true : false);
	});
	LambdaNtupleConsumer<HttTypes>::AddIntQuantity(metadata, "nCentralJets20", [](event_type const& event, product_type const& product) {
		return product.m_nCentralJets20;
	});
	LambdaNtupleConsumer<HttTypes>::AddIntQuantity(metadata, "nCentralJets30", [](event_type const& event, product_type const& product) {
		return product.m_nCentralJets30;
	});
}

void DiJetQuantitiesProducer::Produce(event_type const& event, product_type& product,
	                                  setting_type const& settings, metadata_type const& metadata) const
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
