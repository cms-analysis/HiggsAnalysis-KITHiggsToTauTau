
#include "Artus/Utility/interface/EnumHelper.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/Consumers/HttLambdaNtupleConsumer.h"


HttLambdaNtupleConsumer::HttLambdaNtupleConsumer() : LambdaNtupleConsumerBase<HttTypes>()
{
	// tests for lepton producers
	m_valueExtractorMap["hardLepPt"] = [](HttEvent const& event, HttProduct const& product) { return product.m_ptOrderedLeptons[0]->Pt(); };
	m_valueExtractorMap["hardLepEta"] = [](HttEvent const& event, HttProduct const& product) { return product.m_ptOrderedLeptons[0]->Eta(); };
	m_valueExtractorMap["softLepPt"] = [](HttEvent const& event, HttProduct const& product) { return product.m_ptOrderedLeptons[1]->Pt(); };
	m_valueExtractorMap["softLepEta"] = [](HttEvent const& event, HttProduct const& product) { return product.m_ptOrderedLeptons[1]->Eta(); };
	m_valueExtractorMap["diLepMass"] = [](HttEvent const& event, HttProduct const& product) { return (*(product.m_ptOrderedLeptons[0]) + *(product.m_ptOrderedLeptons[1])).mass(); };
	m_valueExtractorMap["decayChannelIndex"] = [](HttEvent const& event, HttProduct const& product) { return EnumHelper::toUnderlyingValue(product.m_decayChannel); };

	// RW's own stuff for testing
	m_valueExtractorMap["genTauPt"] = [](HttEvent const& event, HttProduct const& product) { return product.m_genTauDecay.size() > 0 ? product.m_genTauDecay.at(0)->p4.Pt() : UNDEFINED_VALUE; };
	m_valueExtractorMap["genTauPdgId"] = [](HttEvent const& event, HttProduct const& product) { return product.m_genTauDecay.size() > 0 ? product.m_genTauDecay.at(0)->pdgId() : UNDEFINED_VALUE; };
	m_valueExtractorMap["genTauStatus"] = [](HttEvent const& event, HttProduct const& product) { return product.m_genTauDecay.size() > 0 ? product.m_genTauDecay.at(0)->status() : UNDEFINED_VALUE; };
	m_valueExtractorMap["genTauDirDaugs"] = [](HttEvent const& event, HttProduct const& product) { return product.m_genTauDecay.size() > 0 ? product.m_genTauDecay.at(0)->daughterIndices.size() : UNDEFINED_VALUE; };
	m_valueExtractorMap["genTauAllDaugs"] = [](HttEvent const& event, HttProduct const& product) { return product.m_genTauDecay.size() - 1.; };
}

