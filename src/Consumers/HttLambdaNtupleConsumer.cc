
#include "Artus/Utility/interface/Utility.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/Consumers/HttLambdaNtupleConsumer.h"


HttLambdaNtupleConsumer::HttLambdaNtupleConsumer() : LambdaNtupleConsumerBase<HttTypes>()
{
	// event weight // TODO: loop over product.m_weights to write out all weights
	m_valueExtractorMap["eventWeight"] = [](HttEvent const& event, HttProduct const& product) {
		return Utility::GetWithDefault(product.m_weights, std::string("eventWeight"), 1.0);
	};

	// tests for lepton producers
	m_valueExtractorMap["hardLepPt"] = [](HttEvent const& event, HttProduct const& product) { return product.m_ptOrderedLeptons[0]->Pt(); };
	m_valueExtractorMap["hardLepEta"] = [](HttEvent const& event, HttProduct const& product) { return product.m_ptOrderedLeptons[0]->Eta(); };
	m_valueExtractorMap["softLepPt"] = [](HttEvent const& event, HttProduct const& product) { return product.m_ptOrderedLeptons[1]->Pt(); };
	m_valueExtractorMap["softLepEta"] = [](HttEvent const& event, HttProduct const& product) { return product.m_ptOrderedLeptons[1]->Eta(); };
	m_valueExtractorMap["diLepMass"] = [](HttEvent const& event, HttProduct const& product) { return (*(product.m_ptOrderedLeptons[0]) + *(product.m_ptOrderedLeptons[1])).mass(); };
	m_valueExtractorMap["decayChannelIndex"] = [](HttEvent const& event, HttProduct const& product) { return Utility::ToUnderlyingValue(product.m_decayChannel); };

}

