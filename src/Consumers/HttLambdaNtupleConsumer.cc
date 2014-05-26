
#include "Artus/Utility/interface/SafeMap.h"
#include "Artus/Utility/interface/Utility.h"
#include "Artus/Utility/interface/DefaultValues.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/Consumers/HttLambdaNtupleConsumer.h"


void HttLambdaNtupleConsumer::Init(Pipeline<HttTypes> * pipeline)
{

	// Lepton quantities
	m_valueExtractorMap["nElectrons"] = [](event_type const& event, product_type const& product) { 
		return product.m_validElectrons.size();
	};
	m_valueExtractorMap["nMuons"] = [](event_type const& event, product_type const& product) {
		return product.m_validMuons.size();
	};
	m_valueExtractorMap["nTaus"] = [](event_type const& event, product_type const& product) {
		return product.m_validTaus.size();
	};
	
	m_valueExtractorMap["leadingLepPt"] = [](event_type const& event, product_type const& product) { return product.m_ptOrderedLeptons[0]->Pt(); };
	m_valueExtractorMap["leadingLepEta"] = [](event_type const& event, product_type const& product) { return product.m_ptOrderedLeptons[0]->Eta(); };
	m_valueExtractorMap["leadingLepPhi"] = [](event_type const& event, product_type const& product) { return product.m_ptOrderedLeptons[0]->Phi(); };
	m_valueExtractorMap["leadingLepMass"] = [](event_type const& event, product_type const& product) { return product.m_ptOrderedLeptons[0]->mass(); };
	m_valueExtractorMap["leadingLepMt"] = [](event_type const& event, product_type const& product) { return product.m_ptOrderedLeptons[0]->Mt(); };
	
	m_valueExtractorMap["leadingLepIso"] = [](event_type const& event, product_type const& product) { return product.m_isoValuePtOrderedLeptons[0]; };
	
	m_valueExtractorMap["trailingLepPt"] = [](event_type const& event, product_type const& product) { return product.m_ptOrderedLeptons[1]->Pt(); };
	m_valueExtractorMap["trailingLepEta"] = [](event_type const& event, product_type const& product) { return product.m_ptOrderedLeptons[1]->Eta(); };
	m_valueExtractorMap["trailingLepPhi"] = [](event_type const& event, product_type const& product) { return product.m_ptOrderedLeptons[1]->Phi(); };
	m_valueExtractorMap["trailingLepMass"] = [](event_type const& event, product_type const& product) { return product.m_ptOrderedLeptons[1]->mass(); };
	m_valueExtractorMap["trailingLepMt"] = [](event_type const& event, product_type const& product) { return product.m_ptOrderedLeptons[1]->Mt(); };
	
	m_valueExtractorMap["trailingLepIso"] = [](event_type const& event, product_type const& product) { return product.m_isoValuePtOrderedLeptons[1]; };
	
	m_valueExtractorMap["diLepMass"] = [](event_type const& event, product_type const& product) {
		return (*(product.m_ptOrderedLeptons[0]) + *(product.m_ptOrderedLeptons[1])).mass();
	};
	m_valueExtractorMap["decayChannelIndex"] = [](event_type const& event, product_type const& product) {
		return Utility::ToUnderlyingValue(product.m_decayChannel);
	};
	
	// Jet quantities
	m_valueExtractorMap["nJets"] = [](event_type const& event, product_type const& product) {
		return product.m_validJets.size();
	};
	m_valueExtractorMap["rho"] = [](event_type const& event, product_type const& product) {
		return event.m_jetArea->median;
	};
	m_valueExtractorMap["leadingJetPt"] = [](event_type const& event, product_type const& product) {
		return product.m_validJets.size() >= 1 ? product.m_validJets.at(0)->p4.Pt() : DefaultValues::UndefinedFloat;
	};
	m_valueExtractorMap["leadingJetEta"] = [](event_type const& event, product_type const& product) {
		return product.m_validJets.size() >= 1 ? product.m_validJets.at(0)->p4.Eta() : DefaultValues::UndefinedFloat;
	};
	m_valueExtractorMap["leadingJetPhi"] = [](event_type const& event, product_type const& product) {
		return product.m_validJets.size() >= 1 ? product.m_validJets.at(0)->p4.Phi() : DefaultValues::UndefinedFloat;
	};
	m_valueExtractorMap["leadingJetCSV"] = [](event_type const& event, product_type const& product) {
		return product.m_validJets.size() >= 1 ? static_cast<KDataPFTaggedJet*>(product.m_validJets.at(0))->getTagger("CombinedSecondaryVertexBJetTags", event.m_taggermetadata) : DefaultValues::UndefinedFloat;
	};
	m_valueExtractorMap["leadingJetTCHE"] = [](event_type const& event, product_type const& product) {
		return product.m_validJets.size() >= 1 ? static_cast<KDataPFTaggedJet*>(product.m_validJets.at(0))->getTagger("TrackCountingHighEffBJetTags", event.m_taggermetadata) : DefaultValues::UndefinedFloat;
	};
	m_valueExtractorMap["trailingJetPt"] = [](event_type const& event, product_type const& product) {
		return product.m_validJets.size() >= 2 ? product.m_validJets.at(1)->p4.Pt() : DefaultValues::UndefinedFloat;
	};
	m_valueExtractorMap["trailingJetEta"] = [](event_type const& event, product_type const& product) {
		return product.m_validJets.size() >= 2 ? product.m_validJets.at(1)->p4.Eta() : DefaultValues::UndefinedFloat;
	};
	m_valueExtractorMap["trailingJetPhi"] = [](event_type const& event, product_type const& product) {
		return product.m_validJets.size() >= 2 ? product.m_validJets.at(1)->p4.Phi() : DefaultValues::UndefinedFloat;
	};
	m_valueExtractorMap["trailingJetCSV"] = [](event_type const& event, product_type const& product) {
		return product.m_validJets.size() >= 2 ? static_cast<KDataPFTaggedJet*>(product.m_validJets.at(1))->getTagger("CombinedSecondaryVertexBJetTags", event.m_taggermetadata) : DefaultValues::UndefinedFloat;
	};
	m_valueExtractorMap["trailingJetTCHE"] = [](event_type const& event, product_type const& product) {
		return product.m_validJets.size() >= 2 ? static_cast<KDataPFTaggedJet*>(product.m_validJets.at(1))->getTagger("TrackCountingHighEffBJetTags", event.m_taggermetadata) : DefaultValues::UndefinedFloat;
	};
	m_valueExtractorMap["nBTaggedJets"] = [](event_type const& event, product_type const& product) {
		return product.m_BTaggedJets.size();
	};
	m_valueExtractorMap["bJetPt"] = [](event_type const& event, product_type const& product) {
		return product.m_BTaggedJets.size() >= 1 ? product.m_BTaggedJets.at(0)->p4.Pt() : DefaultValues::UndefinedFloat;
	};
	m_valueExtractorMap["bJetEta"] = [](event_type const& event, product_type const& product) {
		return product.m_BTaggedJets.size() >= 1 ? product.m_BTaggedJets.at(0)->p4.Eta() : DefaultValues::UndefinedFloat;
	};
	m_valueExtractorMap["bJetPhi"] = [](event_type const& event, product_type const& product) {
		return product.m_BTaggedJets.size() >= 1 ? product.m_BTaggedJets.at(0)->p4.Phi() : DefaultValues::UndefinedFloat;
	};
	
	// MET quantities
	m_valueExtractorMap["pfMETsumEt"] = [](event_type const& event, product_type const& product) { return event.m_met->sumEt; };
	m_valueExtractorMap["pfMETpt"] = [](event_type const& event, product_type const& product) { return event.m_met->p4.Pt(); };
	m_valueExtractorMap["pfMETphi"] = [](event_type const& event, product_type const& product) { return event.m_met->p4.Phi(); };
	
	m_valueExtractorMap["mvaMetSumEt"] = [](event_type const& event, product_type const& product) { return product.m_met->sumEt; };
	m_valueExtractorMap["mvaMetPt"] = [](event_type const& event, product_type const& product) { return product.m_met->p4.Pt(); };
	m_valueExtractorMap["mvaMetPhi"] = [](event_type const& event, product_type const& product) { return product.m_met->p4.Phi(); };
	
	m_valueExtractorMap["MvaMetTTsumEt"] = [](event_type const& event, product_type const& product) { return event.m_mvaMetTT->sumEt; };
	m_valueExtractorMap["MvaMetTTpt"] = [](event_type const& event, product_type const& product) { return event.m_mvaMetTT->p4.Pt(); };
	m_valueExtractorMap["MvaMetTTphi"] = [](event_type const& event, product_type const& product) { return event.m_mvaMetTT->p4.Phi(); };



	m_valueExtractorMap["TauSpinnerWeight"] = [](event_type const & event, product_type const & product)
	{
		return product.m_weights.at("tauspinnerweight");
	};
	m_valueExtractorMap["PhiStar"] = [](event_type const & event, product_type const & product)
	{
		return product.m_genPhiStar;
	};
	m_valueExtractorMap["PsiStarCP"] = [](event_type const & event, product_type const & product)
	{
		return product.m_genPsiStarCP;
	};
	m_valueExtractorMap["MassRoundOff1"] = [](event_type const & event, product_type const & product)
	{
		return product.m_genMassRoundOff1;
	};
	m_valueExtractorMap["MassRoundOff2"] = [](event_type const & event, product_type const & product)
	{
		return product.m_genMassRoundOff2;
	};
	m_valueExtractorMap["Phi"] = [](event_type const & event, product_type const & product)
	{
		return product.m_genPhi;
	};
	//Boson
	m_valueExtractorMap["genBosonSize"] = [](event_type const & event, product_type const & product)
	{
		return product.m_genBoson.size() > 0 ? product.m_genBoson.size() : DefaultValues::UndefinedFloat;
	};
	m_valueExtractorMap["1genBosonPt"] = [](event_type const & event, product_type const & product)
	{
		return product.m_genBoson.size() > 0 ? product.m_genBoson[0].node->p4.Pt() : DefaultValues::UndefinedFloat;
	};
	m_valueExtractorMap["1genBosonPz"] = [](event_type const & event, product_type const & product)
	{
		return product.m_genBoson.size() > 0 ? product.m_genBoson[0].node->p4.Pz() : DefaultValues::UndefinedFloat;
	};
	m_valueExtractorMap["1genBosonEta"] = [](event_type const & event, product_type const & product)
	{
		return product.m_genBoson.size() > 0 ? product.m_genBoson[0].node->p4.Eta() : DefaultValues::UndefinedFloat;
	};
	m_valueExtractorMap["1genBosonPhi"] = [](event_type const & event, product_type const & product)
	{
		return product.m_genBoson.size() > 0 ? product.m_genBoson[0].node->p4.Phi() : DefaultValues::UndefinedFloat;
	};
	m_valueExtractorMap["1genBosonMass"] = [](event_type const & event, product_type const & product)
	{
		return product.m_genBoson.size() > 0 ? product.m_genBoson[0].node->p4.mass() : DefaultValues::UndefinedFloat;
	};
		m_valueExtractorMap["1genBosonEnergy"] = [](event_type const & event, product_type const & product)
	{
		return product.m_genBoson.size() > 0 ? product.m_genBoson[0].node->p4.E() : DefaultValues::UndefinedFloat;
	};
	m_valueExtractorMap["1genBosonPdgId"] = [](event_type const & event, product_type const & product)
	{
		return product.m_genBoson.size() > 0 ? product.m_genBoson[0].node->pdgId() : DefaultValues::UndefinedFloat;
	};
	m_valueExtractorMap["1genBosonStatus"] = [](event_type const & event, product_type const & product)
	{
		return product.m_genBoson.size() > 0 ? product.m_genBoson[0].node->status() : DefaultValues::UndefinedFloat;
	};




	// Boson daughters
	m_valueExtractorMap["1genBosonDaughterSize"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 0) ? product.m_genBoson[0].Daughters.size() : DefaultValues::UndefinedFloat;
	};

	// charged particles of a one-prong
	m_valueExtractorMap["Tau1OneProngsSize"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 0) && (product.m_genBoson[0].Daughters[0].finalStateOneProngs.size() > 0)? product.m_genBoson[0].Daughters[0].finalStateOneProngs.size() : DefaultValues::UndefinedFloat;
	};
	m_valueExtractorMap["Tau2OneProngsSize"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[1].finalStateOneProngs.size() > 0)? product.m_genBoson[0].Daughters[1].finalStateOneProngs.size() : DefaultValues::UndefinedFloat;
	};
	m_valueExtractorMap["OneProngChargedPart1PdgId"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[0].finalStateOneProngs.size() > 0) && (product.m_genBoson[0].Daughters[1].finalStateOneProngs.size() > 0)? product.m_genOneProngCharged1->pdgId() : DefaultValues::UndefinedFloat;
	};
	m_valueExtractorMap["OneProngChargedPart2PdgId"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[1].finalStateOneProngs.size() > 0) && (product.m_genBoson[0].Daughters[0].finalStateOneProngs.size() > 0)? product.m_genOneProngCharged2->pdgId() : DefaultValues::UndefinedFloat;
	};
	// first daughter
	
	m_valueExtractorMap["TauMinusParent"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 0) ? product.m_genBoson[0].Daughters[0].parent->node->pdgId() : DefaultValues::UndefinedFloat;
	};
	m_valueExtractorMap["1genBoson1DaughterPt"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 0) ? product.m_genBoson[0].Daughters[0].node->p4.Pt() : DefaultValues::UndefinedFloat;
	};
	m_valueExtractorMap["1genBoson1DaughterPz"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 0) ? product.m_genBoson[0].Daughters[0].node->p4.Pz() : DefaultValues::UndefinedFloat;
	};
	m_valueExtractorMap["1genBoson1DaughterEta"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 0) ? product.m_genBoson[0].Daughters[0].node->p4.Eta() : DefaultValues::UndefinedFloat;
	};
	m_valueExtractorMap["1genBoson1DaughterPhi"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 0) ? product.m_genBoson[0].Daughters[0].node->p4.Phi() : DefaultValues::UndefinedFloat;
	};
	m_valueExtractorMap["1genBoson1DaughterMass"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 0) ? product.m_genBoson[0].Daughters[0].node->p4.mass() : DefaultValues::UndefinedFloat;
	};
	m_valueExtractorMap["1genBoson1DaughterCharge"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 0) ? product.m_genBoson[0].Daughters[0].getCharge() : DefaultValues::UndefinedFloat;
	};
	m_valueExtractorMap["1genBoson1DaughterEnergy"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 0) ? product.m_genBoson[0].Daughters[0].node->p4.E() : DefaultValues::UndefinedFloat;
	};	
	m_valueExtractorMap["1genBoson1DaughterPdgId"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 0) ? product.m_genBoson[0].Daughters[0].node->pdgId() : DefaultValues::UndefinedFloat;
	};
	m_valueExtractorMap["1genBoson1DaughterStatus"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 0) ? product.m_genBoson[0].Daughters[0].node->status() : DefaultValues::UndefinedFloat;
	};

	// second daughter
	m_valueExtractorMap["TauPlusParent"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 1) ? product.m_genBoson[0].Daughters[1].parent->node->pdgId() : DefaultValues::UndefinedFloat;
	};
	m_valueExtractorMap["1genBoson2DaughterPt"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 1) ? product.m_genBoson[0].Daughters[1].node->p4.Pt() : DefaultValues::UndefinedFloat;
	};
	m_valueExtractorMap["1genBoson2DaughterPz"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 1) ? product.m_genBoson[0].Daughters[1].node->p4.Pz() : DefaultValues::UndefinedFloat;
	};
	m_valueExtractorMap["1genBoson2DaughterEta"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 1) ? product.m_genBoson[0].Daughters[1].node->p4.Eta() : DefaultValues::UndefinedFloat;
	};
	m_valueExtractorMap["1genBoson2DaughterPhi"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 1) ? product.m_genBoson[0].Daughters[1].node->p4.Phi() : DefaultValues::UndefinedFloat;
	};
	m_valueExtractorMap["1genBoson2DaughterMass"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 1) ? product.m_genBoson[0].Daughters[1].node->p4.mass() : DefaultValues::UndefinedFloat;
	};
	m_valueExtractorMap["1genBoson2DaughterEnergy"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 1) ? product.m_genBoson[0].Daughters[1].node->p4.E() : DefaultValues::UndefinedFloat;
	};
	m_valueExtractorMap["1genBoson2DaughterPdgId"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 1) ? product.m_genBoson[0].Daughters[1].node->pdgId() : DefaultValues::UndefinedFloat;
	};
	m_valueExtractorMap["1genBoson2DaughterStatus"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 1) ? product.m_genBoson[0].Daughters[1].node->status() : DefaultValues::UndefinedFloat;
	};


	// Boson granddaughters
	m_valueExtractorMap["1genBoson1DaughterGranddaughterSize"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 0) && (product.m_genBoson[0].Daughters[0].Daughters.size() > 0) ? product.m_genBoson[0].Daughters[0].Daughters.size() : DefaultValues::UndefinedFloat;
	};
	m_valueExtractorMap["1genBoson2DaughterGranddaughterSize"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[1].Daughters.size() > 0) ? product.m_genBoson[0].Daughters[1].Daughters.size() : DefaultValues::UndefinedFloat;
	};


	// first daughter daughters
	m_valueExtractorMap["1genBoson1Daughter1GranddaughterPt"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 0) && (product.m_genBoson[0].Daughters[0].Daughters.size() > 0) ? product.m_genBoson[0].Daughters[0].Daughters[0].node->p4.Pt() : DefaultValues::UndefinedFloat;
	};
	m_valueExtractorMap["1genBoson1Daughter1GranddaughterPz"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 0) && (product.m_genBoson[0].Daughters[0].Daughters.size() > 0) ? product.m_genBoson[0].Daughters[0].Daughters[0].node->p4.Pz() : DefaultValues::UndefinedFloat;
	};
	m_valueExtractorMap["1genBoson1Daughter1GranddaughterEta"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 0) && (product.m_genBoson[0].Daughters[0].Daughters.size() > 0) ? product.m_genBoson[0].Daughters[0].Daughters[0].node->p4.Eta() : DefaultValues::UndefinedFloat;
	};
	m_valueExtractorMap["1genBoson1Daughter1GranddaughterPhi"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 0) && (product.m_genBoson[0].Daughters[0].Daughters.size() > 0) ? product.m_genBoson[0].Daughters[0].Daughters[0].node->p4.Phi() : DefaultValues::UndefinedFloat;
	};
	m_valueExtractorMap["1genBoson1Daughter1GranddaughterMass"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 0) && (product.m_genBoson[0].Daughters[0].Daughters.size() > 0) ? product.m_genBoson[0].Daughters[0].Daughters[0].node->p4.mass() : DefaultValues::UndefinedFloat;
	};
	m_valueExtractorMap["1genBoson1Daughter1GranddaughterEnergy"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 0) && (product.m_genBoson[0].Daughters[0].Daughters.size() > 0) ? product.m_genBoson[0].Daughters[0].Daughters[0].node->p4.E() : DefaultValues::UndefinedFloat;
	};
	m_valueExtractorMap["1genBoson1Daughter1GranddaughterPdgId"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 0) && (product.m_genBoson[0].Daughters[0].Daughters.size() > 0) ? product.m_genBoson[0].Daughters[0].Daughters[0].node->pdgId() : DefaultValues::UndefinedFloat;
	};
	m_valueExtractorMap["1genBoson1Daughter1GranddaughterStatus"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 0) && (product.m_genBoson[0].Daughters[0].Daughters.size() > 0) ? product.m_genBoson[0].Daughters[0].Daughters[0].node->status() : DefaultValues::UndefinedFloat;
	};

	m_valueExtractorMap["1genBoson1Daughter2GranddaughterPt"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 0) && (product.m_genBoson[0].Daughters[0].Daughters.size() > 1) ? product.m_genBoson[0].Daughters[0].Daughters[1].node->p4.Pt() : DefaultValues::UndefinedFloat;
	};
	m_valueExtractorMap["1genBoson1Daughter2GranddaughterPz"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 0) && (product.m_genBoson[0].Daughters[0].Daughters.size() > 1) ? product.m_genBoson[0].Daughters[0].Daughters[1].node->p4.Pz() : DefaultValues::UndefinedFloat;
	};
	m_valueExtractorMap["1genBoson1Daughter2GranddaughterEta"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 0) && (product.m_genBoson[0].Daughters[0].Daughters.size() > 1) ? product.m_genBoson[0].Daughters[0].Daughters[1].node->p4.Eta() : DefaultValues::UndefinedFloat;
	};
	m_valueExtractorMap["1genBoson1Daughter2GranddaughterPhi"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 0) && (product.m_genBoson[0].Daughters[0].Daughters.size() > 1) ? product.m_genBoson[0].Daughters[0].Daughters[1].node->p4.Phi() : DefaultValues::UndefinedFloat;
	};
	m_valueExtractorMap["1genBoson1Daughter2GranddaughterMass"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 0) && (product.m_genBoson[0].Daughters[0].Daughters.size() > 1) ? product.m_genBoson[0].Daughters[0].Daughters[1].node->p4.mass() : DefaultValues::UndefinedFloat;
	};
	m_valueExtractorMap["1genBoson1Daughter2GranddaughterEnergy"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 0) && (product.m_genBoson[0].Daughters[0].Daughters.size() > 1) ? product.m_genBoson[0].Daughters[0].Daughters[1].node->p4.E() : DefaultValues::UndefinedFloat;
	};
	m_valueExtractorMap["1genBoson1Daughter2GranddaughterPdgId"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 0) && (product.m_genBoson[0].Daughters[0].Daughters.size() > 1) ? product.m_genBoson[0].Daughters[0].Daughters[1].node->pdgId() : DefaultValues::UndefinedFloat;
	};
	m_valueExtractorMap["1genBoson1Daughter2GranddaughterStatus"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 0) && (product.m_genBoson[0].Daughters[0].Daughters.size() > 1) ? product.m_genBoson[0].Daughters[0].Daughters[1].node->status() : DefaultValues::UndefinedFloat;
	};

	m_valueExtractorMap["1genBoson1Daughter3GranddaughterPt"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 0) && (product.m_genBoson[0].Daughters[0].Daughters.size() > 2) ? product.m_genBoson[0].Daughters[0].Daughters[2].node->p4.Pt() : DefaultValues::UndefinedFloat;
	};
	m_valueExtractorMap["1genBoson1Daughter3GranddaughterPz"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 0) && (product.m_genBoson[0].Daughters[0].Daughters.size() > 2) ? product.m_genBoson[0].Daughters[0].Daughters[2].node->p4.Pz() : DefaultValues::UndefinedFloat;
	};
	m_valueExtractorMap["1genBoson1Daughter3GranddaughterEta"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 0) && (product.m_genBoson[0].Daughters[0].Daughters.size() > 2) ? product.m_genBoson[0].Daughters[0].Daughters[2].node->p4.Eta() : DefaultValues::UndefinedFloat;
	};
	m_valueExtractorMap["1genBoson1Daughter3GranddaughterPhi"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 0) && (product.m_genBoson[0].Daughters[0].Daughters.size() > 2) ? product.m_genBoson[0].Daughters[0].Daughters[2].node->p4.Phi() : DefaultValues::UndefinedFloat;
	};
	m_valueExtractorMap["1genBoson1Daughter3GranddaughterMass"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 0) && (product.m_genBoson[0].Daughters[0].Daughters.size() > 2) ? product.m_genBoson[0].Daughters[0].Daughters[2].node->p4.mass() : DefaultValues::UndefinedFloat;
	};
	m_valueExtractorMap["1genBoson1Daughter3GranddaughterEnergy"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 0) && (product.m_genBoson[0].Daughters[0].Daughters.size() > 2) ? product.m_genBoson[0].Daughters[0].Daughters[2].node->p4.E() : DefaultValues::UndefinedFloat;
	};
	m_valueExtractorMap["1genBoson1Daughter3GranddaughterPdgId"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 0) && (product.m_genBoson[0].Daughters[0].Daughters.size() > 2) ? product.m_genBoson[0].Daughters[0].Daughters[2].node->pdgId() : DefaultValues::UndefinedFloat;
	};
	m_valueExtractorMap["1genBoson1Daughter3GranddaughterStatus"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 0) && (product.m_genBoson[0].Daughters[0].Daughters.size() > 2) ? product.m_genBoson[0].Daughters[0].Daughters[2].node->status() : DefaultValues::UndefinedFloat;
	};

	m_valueExtractorMap["1genBoson1Daughter4GranddaughterPt"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 0) && (product.m_genBoson[0].Daughters[0].Daughters.size() > 3) ? product.m_genBoson[0].Daughters[0].Daughters[3].node->p4.Pt() : DefaultValues::UndefinedFloat;
	};
	m_valueExtractorMap["1genBoson1Daughter4GranddaughterPz"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 0) && (product.m_genBoson[0].Daughters[0].Daughters.size() > 3) ? product.m_genBoson[0].Daughters[0].Daughters[3].node->p4.Pz() : DefaultValues::UndefinedFloat;
	};
	m_valueExtractorMap["1genBoson1Daughter4GranddaughterEta"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 0) && (product.m_genBoson[0].Daughters[0].Daughters.size() > 3) ? product.m_genBoson[0].Daughters[0].Daughters[3].node->p4.Eta() : DefaultValues::UndefinedFloat;
	};
	m_valueExtractorMap["1genBoson1Daughter4GranddaughterPhi"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 0) && (product.m_genBoson[0].Daughters[0].Daughters.size() > 3) ? product.m_genBoson[0].Daughters[0].Daughters[3].node->p4.Phi() : DefaultValues::UndefinedFloat;
	};
	m_valueExtractorMap["1genBoson1Daughter4GranddaughterMass"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 0) && (product.m_genBoson[0].Daughters[0].Daughters.size() > 3) ? product.m_genBoson[0].Daughters[0].Daughters[3].node->p4.mass() : DefaultValues::UndefinedFloat;
	};
	m_valueExtractorMap["1genBoson1Daughter4GranddaughterEnergy"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 0) && (product.m_genBoson[0].Daughters[0].Daughters.size() > 3) ? product.m_genBoson[0].Daughters[0].Daughters[3].node->p4.E() : DefaultValues::UndefinedFloat;
	};
	m_valueExtractorMap["1genBoson1Daughter4GranddaughterPdgId"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 0) && (product.m_genBoson[0].Daughters[0].Daughters.size() > 3) ? product.m_genBoson[0].Daughters[0].Daughters[3].node->pdgId() : DefaultValues::UndefinedFloat;
	};
	m_valueExtractorMap["1genBoson1Daughter4GranddaughterStatus"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 0) && (product.m_genBoson[0].Daughters[0].Daughters.size() > 3) ? product.m_genBoson[0].Daughters[0].Daughters[3].node->status() : DefaultValues::UndefinedFloat;
	};


	// second daughter daughters
	m_valueExtractorMap["1genBoson2Daughter1GranddaughterPt"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[1].Daughters.size() > 0) ? product.m_genBoson[0].Daughters[1].Daughters[0].node->p4.Pt() : DefaultValues::UndefinedFloat;
	};
	m_valueExtractorMap["1genBoson2Daughter1GranddaughterPz"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[1].Daughters.size() > 0) ? product.m_genBoson[0].Daughters[1].Daughters[0].node->p4.Pz() : DefaultValues::UndefinedFloat;
	};
	m_valueExtractorMap["1genBoson2Daughter1GranddaughterEta"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[1].Daughters.size() > 0) ? product.m_genBoson[0].Daughters[1].Daughters[0].node->p4.Eta() : DefaultValues::UndefinedFloat;
	};
	m_valueExtractorMap["1genBoson2Daughter1GranddaughterPhi"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[1].Daughters.size() > 0) ? product.m_genBoson[0].Daughters[1].Daughters[0].node->p4.Phi() : DefaultValues::UndefinedFloat;
	};
	m_valueExtractorMap["1genBoson2Daughter1GranddaughterMass"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[1].Daughters.size() > 0) ? product.m_genBoson[0].Daughters[1].Daughters[0].node->p4.mass() : DefaultValues::UndefinedFloat;
	};
	m_valueExtractorMap["1genBoson2Daughter1GranddaughterEnergy"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[1].Daughters.size() > 0) ? product.m_genBoson[0].Daughters[1].Daughters[0].node->p4.E() : DefaultValues::UndefinedFloat;
	};
	m_valueExtractorMap["1genBoson2Daughter1GranddaughterPdgId"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[1].Daughters.size() > 0) ? product.m_genBoson[0].Daughters[1].Daughters[0].node->pdgId() : DefaultValues::UndefinedFloat;
	};
	m_valueExtractorMap["1genBoson2Daughter1GranddaughterStatus"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[1].Daughters.size() > 0) ? product.m_genBoson[0].Daughters[1].Daughters[0].node->status() : DefaultValues::UndefinedFloat;
	};

	m_valueExtractorMap["1genBoson2Daughter2GranddaughterPt"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[1].Daughters.size() > 1) ? product.m_genBoson[0].Daughters[1].Daughters[1].node->p4.Pt() : DefaultValues::UndefinedFloat;
	};
	m_valueExtractorMap["1genBoson2Daughter2GranddaughterPz"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[1].Daughters.size() > 1) ? product.m_genBoson[0].Daughters[1].Daughters[1].node->p4.Pz() : DefaultValues::UndefinedFloat;
	};
	m_valueExtractorMap["1genBoson2Daughter2GranddaughterEta"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[1].Daughters.size() > 1) ? product.m_genBoson[0].Daughters[1].Daughters[1].node->p4.Eta() : DefaultValues::UndefinedFloat;
	};
	m_valueExtractorMap["1genBoson2Daughter2GranddaughterPhi"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[1].Daughters.size() > 1) ? product.m_genBoson[0].Daughters[1].Daughters[1].node->p4.Phi() : DefaultValues::UndefinedFloat;
	};
	m_valueExtractorMap["1genBoson2Daughter2GranddaughterMass"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[1].Daughters.size() > 1) ? product.m_genBoson[0].Daughters[1].Daughters[1].node->p4.mass() : DefaultValues::UndefinedFloat;
	};
	m_valueExtractorMap["1genBoson2Daughter2GranddaughterEnergy"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[1].Daughters.size() > 1) ? product.m_genBoson[0].Daughters[1].Daughters[1].node->p4.E() : DefaultValues::UndefinedFloat;
	};
	m_valueExtractorMap["1genBoson2Daughter2GranddaughterPdgId"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[1].Daughters.size() > 1) ? product.m_genBoson[0].Daughters[1].Daughters[1].node->pdgId() : DefaultValues::UndefinedFloat;
	};
	m_valueExtractorMap["1genBoson2Daughter2GranddaughterStatus"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[1].Daughters.size() > 1) ? product.m_genBoson[0].Daughters[1].Daughters[1].node->status() : DefaultValues::UndefinedFloat;
	};

	m_valueExtractorMap["1genBoson2Daughter3GranddaughterPt"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[1].Daughters.size() > 2) ? product.m_genBoson[0].Daughters[1].Daughters[2].node->p4.Pt() : DefaultValues::UndefinedFloat;
	};
	m_valueExtractorMap["1genBoson2Daughter3GranddaughterPz"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[1].Daughters.size() > 2) ? product.m_genBoson[0].Daughters[1].Daughters[2].node->p4.Pz() : DefaultValues::UndefinedFloat;
	};
	m_valueExtractorMap["1genBoson2Daughter3GranddaughterEta"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[1].Daughters.size() > 2) ? product.m_genBoson[0].Daughters[1].Daughters[2].node->p4.Eta() : DefaultValues::UndefinedFloat;
	};
	m_valueExtractorMap["1genBoson2Daughter3GranddaughterPhi"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[1].Daughters.size() > 2) ? product.m_genBoson[0].Daughters[1].Daughters[2].node->p4.Phi() : DefaultValues::UndefinedFloat;
	};
	m_valueExtractorMap["1genBoson2Daughter3GranddaughterMass"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[1].Daughters.size() > 2) ? product.m_genBoson[0].Daughters[1].Daughters[2].node->p4.mass() : DefaultValues::UndefinedFloat;
	};
	m_valueExtractorMap["1genBoson2Daughter3GranddaughterEnergy"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[1].Daughters.size() > 2) ? product.m_genBoson[0].Daughters[1].Daughters[2].node->p4.E() : DefaultValues::UndefinedFloat;
	};
	m_valueExtractorMap["1genBoson2Daughter3GranddaughterPdgId"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[1].Daughters.size() > 2) ? product.m_genBoson[0].Daughters[1].Daughters[2].node->pdgId() : DefaultValues::UndefinedFloat;
	};
	m_valueExtractorMap["1genBoson2Daughter3GranddaughterStatus"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[1].Daughters.size() > 2) ? product.m_genBoson[0].Daughters[1].Daughters[2].node->status() : DefaultValues::UndefinedFloat;
	};

	m_valueExtractorMap["1genBoson2Daughter4GranddaughterPt"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[1].Daughters.size() > 3) ? product.m_genBoson[0].Daughters[1].Daughters[3].node->p4.Pt() : DefaultValues::UndefinedFloat;
	};
	m_valueExtractorMap["1genBoson2Daughter4GranddaughterPz"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[1].Daughters.size() > 3) ? product.m_genBoson[0].Daughters[1].Daughters[3].node->p4.Pz() : DefaultValues::UndefinedFloat;
	};
	m_valueExtractorMap["1genBoson2Daughter4GranddaughterEta"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[1].Daughters.size() > 3) ? product.m_genBoson[0].Daughters[1].Daughters[3].node->p4.Eta() : DefaultValues::UndefinedFloat;
	};
	m_valueExtractorMap["1genBoson2Daughter4GranddaughterPhi"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[1].Daughters.size() > 3) ? product.m_genBoson[0].Daughters[1].Daughters[3].node->p4.Phi() : DefaultValues::UndefinedFloat;
	};
	m_valueExtractorMap["1genBoson2Daughter4GranddaughterMass"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[1].Daughters.size() > 3) ? product.m_genBoson[0].Daughters[1].Daughters[3].node->p4.mass() : DefaultValues::UndefinedFloat;
	};
	m_valueExtractorMap["1genBoson2Daughter4GranddaughterEnergy"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[1].Daughters.size() > 3) ? product.m_genBoson[0].Daughters[1].Daughters[3].node->p4.E() : DefaultValues::UndefinedFloat;
	};
	m_valueExtractorMap["1genBoson2Daughter4GranddaughterPdgId"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[1].Daughters.size() > 3) ? product.m_genBoson[0].Daughters[1].Daughters[3].node->pdgId() : DefaultValues::UndefinedFloat;
	};
	m_valueExtractorMap["1genBoson2Daughter4GranddaughterStatus"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[1].Daughters.size() > 3) ? product.m_genBoson[0].Daughters[1].Daughters[3].node->status() : DefaultValues::UndefinedFloat;
	};

	// Boson GrandGranddaughters: the only GrandGranddaughters we need are from 2nd Granddaughters
	m_valueExtractorMap["1genBoson1Daughter2GranddaughterGrandGranddaughterSize"] = [](event_type const & event, product_type const & product)
	{	
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 0) && (product.m_genBoson[0].Daughters[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[0].Daughters[1].Daughters.size() >0)? product.m_genBoson[0].Daughters[0].Daughters[1].Daughters.size() : DefaultValues::UndefinedFloat;
	};
	m_valueExtractorMap["1genBoson2Daughter2GranddaughterGrandGranddaughterSize"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[1].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[1].Daughters[1].Daughters.size() >0)? product.m_genBoson[0].Daughters[1].Daughters[1].Daughters.size() : DefaultValues::UndefinedFloat;
	};


	
	m_valueExtractorMap["1genBoson1Daughter2Granddaughter1GrandGranddaughterPdgId"] = [](event_type const & event, product_type const & product)
	{	
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 0) && (product.m_genBoson[0].Daughters[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[0].Daughters[1].Daughters.size() >0)? product.m_genBoson[0].Daughters[0].Daughters[1].Daughters[0].node->pdgId() : DefaultValues::UndefinedFloat;
	};
	m_valueExtractorMap["1genBoson1Daughter2Granddaughter1GrandGranddaughterStatus"] = [](event_type const & event, product_type const & product)
	{	
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 0) && (product.m_genBoson[0].Daughters[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[0].Daughters[1].Daughters.size() >0)? product.m_genBoson[0].Daughters[0].Daughters[1].Daughters[0].node->status() : DefaultValues::UndefinedFloat;
	};

	m_valueExtractorMap["1genBoson1Daughter2Granddaughter2GrandGranddaughterPdgId"] = [](event_type const & event, product_type const & product)
	{	
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 0) && (product.m_genBoson[0].Daughters[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[0].Daughters[1].Daughters.size() >1)? product.m_genBoson[0].Daughters[0].Daughters[1].Daughters[1].node->pdgId() : DefaultValues::UndefinedFloat;
	};
	m_valueExtractorMap["1genBoson1Daughter2Granddaughter2GrandGranddaughterStatus"] = [](event_type const & event, product_type const & product)
	{	
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 0) && (product.m_genBoson[0].Daughters[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[0].Daughters[1].Daughters.size() >1)? product.m_genBoson[0].Daughters[0].Daughters[1].Daughters[1].node->status() : DefaultValues::UndefinedFloat;
	};

	m_valueExtractorMap["1genBoson1Daughter2Granddaughter3GrandGranddaughterPdgId"] = [](event_type const & event, product_type const & product)
	{	
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 0) && (product.m_genBoson[0].Daughters[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[0].Daughters[1].Daughters.size() >2)? product.m_genBoson[0].Daughters[0].Daughters[1].Daughters[2].node->pdgId() : DefaultValues::UndefinedFloat;
	};
	m_valueExtractorMap["1genBoson1Daughter2Granddaughter3GrandGranddaughterStatus"] = [](event_type const & event, product_type const & product)
	{	
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 0) && (product.m_genBoson[0].Daughters[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[0].Daughters[1].Daughters.size() >2)? product.m_genBoson[0].Daughters[0].Daughters[1].Daughters[2].node->status() : DefaultValues::UndefinedFloat;
	};
	
	m_valueExtractorMap["1genBoson1Daughter2Granddaughter4GrandGranddaughterPdgId"] = [](event_type const & event, product_type const & product)
	{	
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 0) && (product.m_genBoson[0].Daughters[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[0].Daughters[1].Daughters.size() >3)? product.m_genBoson[0].Daughters[0].Daughters[1].Daughters[3].node->pdgId() : DefaultValues::UndefinedFloat;
	};
	m_valueExtractorMap["1genBoson1Daughter2Granddaughter4GrandGranddaughterStatus"] = [](event_type const & event, product_type const & product)
	{	
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 0) && (product.m_genBoson[0].Daughters[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[0].Daughters[1].Daughters.size() >3)? product.m_genBoson[0].Daughters[0].Daughters[1].Daughters[3].node->status() : DefaultValues::UndefinedFloat;
	};	
	
	m_valueExtractorMap["1genBoson1Daughter2Granddaughter5GrandGranddaughterPdgId"] = [](event_type const & event, product_type const & product)
	{	
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 0) && (product.m_genBoson[0].Daughters[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[0].Daughters[1].Daughters.size() >4)? product.m_genBoson[0].Daughters[0].Daughters[1].Daughters[4].node->pdgId() : DefaultValues::UndefinedFloat;
	};
	m_valueExtractorMap["1genBoson1Daughter2Granddaughter5GrandGranddaughterStatus"] = [](event_type const & event, product_type const & product)
	{	
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 0) && (product.m_genBoson[0].Daughters[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[0].Daughters[1].Daughters.size() >4)? product.m_genBoson[0].Daughters[0].Daughters[1].Daughters[4].node->status() : DefaultValues::UndefinedFloat;
	};
	
	m_valueExtractorMap["1genBoson1Daughter2Granddaughter6GrandGranddaughterPdgId"] = [](event_type const & event, product_type const & product)
	{	
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 0) && (product.m_genBoson[0].Daughters[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[0].Daughters[1].Daughters.size() >5)? product.m_genBoson[0].Daughters[0].Daughters[1].Daughters[5].node->pdgId() : DefaultValues::UndefinedFloat;
	};
	m_valueExtractorMap["1genBoson1Daughter2Granddaughter6GrandGranddaughterStatus"] = [](event_type const & event, product_type const & product)
	{	
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 0) && (product.m_genBoson[0].Daughters[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[0].Daughters[1].Daughters.size() >5)? product.m_genBoson[0].Daughters[0].Daughters[1].Daughters[5].node->status() : DefaultValues::UndefinedFloat;
	};
	
	// settings for synch ntuples
	m_valueExtractorMap["evt"] = [](event_type const& event, product_type const& product) { return event.m_eventMetadata->nEvent; };
	m_valueExtractorMap["puweight"] = [](event_type const& event, product_type const& product) { return product.m_weights.at("puWeight"); };
	m_valueExtractorMap["weight"] = [pipeline](event_type const& event, product_type const& product) {
		return product.m_weights.at(pipeline->GetSettings().GetEventWeight());
	};
	m_valueExtractorMap["mvis"] = m_valueExtractorMap["diLepMass"];
	m_valueExtractorMap["pt_1"] = m_valueExtractorMap["leadingLepPt"];
	m_valueExtractorMap["eta_1"] = m_valueExtractorMap["leadingLepEta"];
	m_valueExtractorMap["phi_1"] = m_valueExtractorMap["leadingLepPhi"];
	m_valueExtractorMap["m_1"] = m_valueExtractorMap["leadingLepMass"];
	m_valueExtractorMap["iso_1"] = m_valueExtractorMap["leadingLepIso"];
	m_valueExtractorMap["mt_1"] = m_valueExtractorMap["leadingLepMt"];
	m_valueExtractorMap["pt_2"] = m_valueExtractorMap["trailingLepPt"];
	m_valueExtractorMap["eta_2"] = m_valueExtractorMap["trailingLepEta"];
	m_valueExtractorMap["phi_2"] = m_valueExtractorMap["trailingLepPhi"];
	m_valueExtractorMap["m_2"] = m_valueExtractorMap["trailingLepMass"];
	m_valueExtractorMap["iso_2"] = m_valueExtractorMap["trailingLepIso"];
	m_valueExtractorMap["mt_2"] = m_valueExtractorMap["trailingLepMt"];
	m_valueExtractorMap["met"] = m_valueExtractorMap["mvaMetPt"];
	
	// need to be called at last
	KappaLambdaNtupleConsumer<HttTypes>::Init(pipeline);
}