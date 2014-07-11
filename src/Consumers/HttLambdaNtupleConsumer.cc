
#include <Math/VectorUtil.h>

#include "Artus/Utility/interface/SafeMap.h"
#include "Artus/Utility/interface/Utility.h"
#include "Artus/Utility/interface/DefaultValues.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/Consumers/HttLambdaNtupleConsumer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/DiJetQuantitiesProducer.h"


void HttLambdaNtupleConsumer::Init(Pipeline<HttTypes> * pipeline)
{

	// Lepton quantities
	LambdaNtupleConsumer<HttTypes>::Quantities["nElectrons"] = [](event_type const& event, product_type const& product) { 
		return product.m_validElectrons.size();
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["nMuons"] = [](event_type const& event, product_type const& product) {
		return product.m_validMuons.size();
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["nTaus"] = [](event_type const& event, product_type const& product) {
		return product.m_validTaus.size();
	};
	
	LambdaNtupleConsumer<HttTypes>::Quantities["leadingLepCharge"] = [](event_type const& event, product_type const& product) { return product.m_ptOrderedLeptons[0]->charge; };
	LambdaNtupleConsumer<HttTypes>::Quantities["leadingLepPt"] = [](event_type const& event, product_type const& product) { return product.m_ptOrderedLeptons[0]->p4.Pt(); };
	LambdaNtupleConsumer<HttTypes>::Quantities["leadingLepEta"] = [](event_type const& event, product_type const& product) { return product.m_ptOrderedLeptons[0]->p4.Eta(); };
	LambdaNtupleConsumer<HttTypes>::Quantities["leadingLepPhi"] = [](event_type const& event, product_type const& product) { return product.m_ptOrderedLeptons[0]->p4.Phi(); };
	LambdaNtupleConsumer<HttTypes>::Quantities["leadingLepMass"] = [](event_type const& event, product_type const& product) { return product.m_ptOrderedLeptons[0]->p4.mass(); };
	LambdaNtupleConsumer<HttTypes>::Quantities["leadingLepMt"] = [](event_type const& event, product_type const& product) { return product.m_ptOrderedLeptons[0]->p4.Mt(); };
	LambdaNtupleConsumer<HttTypes>::Quantities["leadingLepIso"] = [](event_type const& event, product_type const& product) {
		return SafeMap::GetWithDefault(product.m_leptonIsolation, product.m_ptOrderedLeptons[0], DefaultValues::UndefinedDouble);
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["leadingLepIsoOverPt"] = [](event_type const& event, product_type const& product) {
		return SafeMap::GetWithDefault(product.m_leptonIsolationOverPt, product.m_ptOrderedLeptons[0], DefaultValues::UndefinedDouble);
	};
	
	LambdaNtupleConsumer<HttTypes>::Quantities["lep1Charge"] = [](event_type const& event, product_type const& product) { return product.m_flavourOrderedLeptons[0]->charge; };
	LambdaNtupleConsumer<HttTypes>::Quantities["lep1Pt"] = [](event_type const& event, product_type const& product) { return product.m_flavourOrderedLeptons[0]->p4.Pt(); };
	LambdaNtupleConsumer<HttTypes>::Quantities["lep1Eta"] = [](event_type const& event, product_type const& product) { return product.m_flavourOrderedLeptons[0]->p4.Eta(); };
	LambdaNtupleConsumer<HttTypes>::Quantities["lep1Phi"] = [](event_type const& event, product_type const& product) { return product.m_flavourOrderedLeptons[0]->p4.Phi(); };
	LambdaNtupleConsumer<HttTypes>::Quantities["lep1Mass"] = [](event_type const& event, product_type const& product) { return product.m_flavourOrderedLeptons[0]->p4.mass(); };
	LambdaNtupleConsumer<HttTypes>::Quantities["lep1Mt"] = [](event_type const& event, product_type const& product) { return product.m_flavourOrderedLeptons[0]->p4.Mt(); };
	LambdaNtupleConsumer<HttTypes>::Quantities["lep1Iso"] = [](event_type const& event, product_type const& product) {
		return SafeMap::GetWithDefault(product.m_leptonIsolation, product.m_flavourOrderedLeptons[0], DefaultValues::UndefinedDouble);
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["lep1IsoOverPt"] = [](event_type const& event, product_type const& product) {
		return SafeMap::GetWithDefault(product.m_leptonIsolationOverPt, product.m_flavourOrderedLeptons[0], DefaultValues::UndefinedDouble);
	};
	
	LambdaNtupleConsumer<HttTypes>::Quantities["trailingLepCharge"] = [](event_type const& event, product_type const& product) { return product.m_ptOrderedLeptons[1]->charge; };
	LambdaNtupleConsumer<HttTypes>::Quantities["trailingLepPt"] = [](event_type const& event, product_type const& product) { return product.m_ptOrderedLeptons[1]->p4.Pt(); };
	LambdaNtupleConsumer<HttTypes>::Quantities["trailingLepEta"] = [](event_type const& event, product_type const& product) { return product.m_ptOrderedLeptons[1]->p4.Eta(); };
	LambdaNtupleConsumer<HttTypes>::Quantities["trailingLepPhi"] = [](event_type const& event, product_type const& product) { return product.m_ptOrderedLeptons[1]->p4.Phi(); };
	LambdaNtupleConsumer<HttTypes>::Quantities["trailingLepMass"] = [](event_type const& event, product_type const& product) { return product.m_ptOrderedLeptons[1]->p4.mass(); };
	LambdaNtupleConsumer<HttTypes>::Quantities["trailingLepMt"] = [](event_type const& event, product_type const& product) { return product.m_ptOrderedLeptons[1]->p4.Mt(); };
	LambdaNtupleConsumer<HttTypes>::Quantities["trailingLepIso"] = [](event_type const& event, product_type const& product) {
		return SafeMap::GetWithDefault(product.m_leptonIsolation, product.m_ptOrderedLeptons[1], DefaultValues::UndefinedDouble);
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["trailingLepIsoOverPt"] = [](event_type const& event, product_type const& product) {
		return SafeMap::GetWithDefault(product.m_leptonIsolationOverPt, product.m_ptOrderedLeptons[1], DefaultValues::UndefinedDouble);
	};
	
	LambdaNtupleConsumer<HttTypes>::Quantities["lep2Charge"] = [](event_type const& event, product_type const& product) { return product.m_flavourOrderedLeptons[1]->charge; };
	LambdaNtupleConsumer<HttTypes>::Quantities["lep2Pt"] = [](event_type const& event, product_type const& product) { return product.m_flavourOrderedLeptons[1]->p4.Pt(); };
	LambdaNtupleConsumer<HttTypes>::Quantities["lep2Eta"] = [](event_type const& event, product_type const& product) { return product.m_flavourOrderedLeptons[1]->p4.Eta(); };
	LambdaNtupleConsumer<HttTypes>::Quantities["lep2Phi"] = [](event_type const& event, product_type const& product) { return product.m_flavourOrderedLeptons[1]->p4.Phi(); };
	LambdaNtupleConsumer<HttTypes>::Quantities["lep2Mass"] = [](event_type const& event, product_type const& product) { return product.m_flavourOrderedLeptons[1]->p4.mass(); };
	LambdaNtupleConsumer<HttTypes>::Quantities["lep2Mt"] = [](event_type const& event, product_type const& product) { return product.m_flavourOrderedLeptons[1]->p4.Mt(); };
	LambdaNtupleConsumer<HttTypes>::Quantities["lep2Iso"] = [](event_type const& event, product_type const& product) {
		return SafeMap::GetWithDefault(product.m_leptonIsolation, product.m_flavourOrderedLeptons[1], DefaultValues::UndefinedDouble);
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["lep2IsoOverPt"] = [](event_type const& event, product_type const& product) {
		return SafeMap::GetWithDefault(product.m_leptonIsolationOverPt, product.m_flavourOrderedLeptons[1], DefaultValues::UndefinedDouble);
	};
	
	LambdaNtupleConsumer<HttTypes>::Quantities["diLepPt"] = [](event_type const& event, product_type const& product) {
		return product.m_diLeptonSystem.Pt();
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["diLepEta"] = [](event_type const& event, product_type const& product) {
		return product.m_diLeptonSystem.Eta();
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["diLepPhi"] = [](event_type const& event, product_type const& product) {
		return product.m_diLeptonSystem.Phi();
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["diLepMass"] = [](event_type const& event, product_type const& product) {
		return product.m_diLeptonSystem.mass();
	};
	
	LambdaNtupleConsumer<HttTypes>::Quantities["diTauPt"] = [](event_type const& event, product_type const& product) {
		return product.m_diTauSystem.Pt();
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["diTauEta"] = [](event_type const& event, product_type const& product) {
		return product.m_diTauSystem.Eta();
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["diTauPhi"] = [](event_type const& event, product_type const& product) {
		return product.m_diTauSystem.Phi();
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["diTauMass"] = [](event_type const& event, product_type const& product) {
		return product.m_diTauSystem.mass();
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["diTauSystemReconstructed"] = [](event_type const& event, product_type const& product) {
		return (product.m_diTauSystemReconstructed ? 1.0 : 0.0);
	};
	
	LambdaNtupleConsumer<HttTypes>::Quantities["decayChannelIndex"] = [](event_type const& event, product_type const& product) {
		return Utility::ToUnderlyingValue(product.m_decayChannel);
	};
	
	// Jet quantities
	LambdaNtupleConsumer<HttTypes>::Quantities["nJets"] = [](event_type const& event, product_type const& product) {
		return product.m_validJets.size();
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["rho"] = [](event_type const& event, product_type const& product) {
		return event.m_jetArea->median;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["leadingJetPt"] = [](event_type const& event, product_type const& product) {
		return product.m_validJets.size() >= 1 ? product.m_validJets.at(0)->p4.Pt() : DefaultValues::UndefinedDouble;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["leadingJetEta"] = [](event_type const& event, product_type const& product) {
		return product.m_validJets.size() >= 1 ? product.m_validJets.at(0)->p4.Eta() : DefaultValues::UndefinedDouble;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["leadingJetPhi"] = [](event_type const& event, product_type const& product) {
		return product.m_validJets.size() >= 1 ? product.m_validJets.at(0)->p4.Phi() : DefaultValues::UndefinedDouble;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["leadingJetCSV"] = [](event_type const& event, product_type const& product) {
		return product.m_validJets.size() >= 1 ? static_cast<KDataPFTaggedJet*>(product.m_validJets.at(0))->getTagger("CombinedSecondaryVertexBJetTags", event.m_taggerMetadata) : DefaultValues::UndefinedDouble;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["leadingJetTCHE"] = [](event_type const& event, product_type const& product) {
		return product.m_validJets.size() >= 1 ? static_cast<KDataPFTaggedJet*>(product.m_validJets.at(0))->getTagger("TrackCountingHighEffBJetTags", event.m_taggerMetadata) : DefaultValues::UndefinedDouble;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["trailingJetPt"] = [](event_type const& event, product_type const& product) {
		return product.m_validJets.size() >= 2 ? product.m_validJets.at(1)->p4.Pt() : DefaultValues::UndefinedDouble;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["trailingJetEta"] = [](event_type const& event, product_type const& product) {
		return product.m_validJets.size() >= 2 ? product.m_validJets.at(1)->p4.Eta() : DefaultValues::UndefinedDouble;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["trailingJetPhi"] = [](event_type const& event, product_type const& product) {
		return product.m_validJets.size() >= 2 ? product.m_validJets.at(1)->p4.Phi() : DefaultValues::UndefinedDouble;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["trailingJetCSV"] = [](event_type const& event, product_type const& product) {
		return product.m_validJets.size() >= 2 ? static_cast<KDataPFTaggedJet*>(product.m_validJets.at(1))->getTagger("CombinedSecondaryVertexBJetTags", event.m_taggerMetadata) : DefaultValues::UndefinedDouble;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["trailingJetTCHE"] = [](event_type const& event, product_type const& product) {
		return product.m_validJets.size() >= 2 ? static_cast<KDataPFTaggedJet*>(product.m_validJets.at(1))->getTagger("TrackCountingHighEffBJetTags", event.m_taggerMetadata) : DefaultValues::UndefinedDouble;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["nBTaggedJets"] = [](event_type const& event, product_type const& product) {
		return product.m_bTaggedJets.size();
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["bJetPt"] = [](event_type const& event, product_type const& product) {
		return product.m_bTaggedJets.size() >= 1 ? product.m_bTaggedJets.at(0)->p4.Pt() : DefaultValues::UndefinedDouble;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["bJetEta"] = [](event_type const& event, product_type const& product) {
		return product.m_bTaggedJets.size() >= 1 ? product.m_bTaggedJets.at(0)->p4.Eta() : DefaultValues::UndefinedDouble;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["bJetPhi"] = [](event_type const& event, product_type const& product) {
		return product.m_bTaggedJets.size() >= 1 ? product.m_bTaggedJets.at(0)->p4.Phi() : DefaultValues::UndefinedDouble;
	};
	
	LambdaNtupleConsumer<HttTypes>::Quantities["diJetMass"] = [](event_type const& event, product_type const& product) {
		return DiJetQuantitiesProducer::GetDiJetQuantity(product, [](RMLV diJetSystem) -> double { return diJetSystem.mass(); });
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["diJetDeltaPhi"] = [](event_type const& event, product_type const& product) {
		return product.m_diJetSystemAvailable ? ROOT::Math::VectorUtil::DeltaR(product.m_validJets[0]->p4, product.m_validJets[1]->p4) :
		                                        DefaultValues::UndefinedDouble;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["diJetAbsDeltaEta"] = [](event_type const& event, product_type const& product) {
		return product.m_diJetSystemAvailable ? std::abs(product.m_validJets[0]->p4.Eta() - product.m_validJets[1]->p4.Eta()) :
		                                        DefaultValues::UndefinedDouble;
	};
	
	// MET quantities
	LambdaNtupleConsumer<HttTypes>::Quantities["pfMetSumEt"] = [](event_type const& event, product_type const& product) { return event.m_met->sumEt; };
	LambdaNtupleConsumer<HttTypes>::Quantities["pfMetPt"] = [](event_type const& event, product_type const& product) { return event.m_met->p4.Pt(); };
	LambdaNtupleConsumer<HttTypes>::Quantities["pfMetPhi"] = [](event_type const& event, product_type const& product) { return event.m_met->p4.Phi(); };
	LambdaNtupleConsumer<HttTypes>::Quantities["pfMetCov00"] = [](event_type const& event, product_type const& product) { return event.m_met->significance.At(0, 0); };
	LambdaNtupleConsumer<HttTypes>::Quantities["pfMetCov01"] = [](event_type const& event, product_type const& product) { return event.m_met->significance.At(0, 1); };
	LambdaNtupleConsumer<HttTypes>::Quantities["pfMetCov10"] = [](event_type const& event, product_type const& product) { return event.m_met->significance.At(1, 0); };
	LambdaNtupleConsumer<HttTypes>::Quantities["pfMetCov11"] = [](event_type const& event, product_type const& product) { return event.m_met->significance.At(1, 1); };
	
	LambdaNtupleConsumer<HttTypes>::Quantities["mvaMetSumEt"] = [](event_type const& event, product_type const& product) { return product.m_met->sumEt; };
	LambdaNtupleConsumer<HttTypes>::Quantities["mvaMetPt"] = [](event_type const& event, product_type const& product) { return product.m_met->p4.Pt(); };
	LambdaNtupleConsumer<HttTypes>::Quantities["mvaMetPhi"] = [](event_type const& event, product_type const& product) { return product.m_met->p4.Phi(); };
	LambdaNtupleConsumer<HttTypes>::Quantities["mvaMetCov00"] = [](event_type const& event, product_type const& product) { return product.m_met->significance.At(0, 0); };
	LambdaNtupleConsumer<HttTypes>::Quantities["mvaMetCov01"] = [](event_type const& event, product_type const& product) { return product.m_met->significance.At(0, 1); };
	LambdaNtupleConsumer<HttTypes>::Quantities["mvaMetCov10"] = [](event_type const& event, product_type const& product) { return product.m_met->significance.At(1, 0); };
	LambdaNtupleConsumer<HttTypes>::Quantities["mvaMetCov11"] = [](event_type const& event, product_type const& product) { return product.m_met->significance.At(1, 1); };

	LambdaNtupleConsumer<HttTypes>::Quantities["TauSpinnerWeight"] = [](event_type const & event, product_type const & product)
	{
		return product.m_weights.at("tauSpinnerWeight");
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["genPhiStarCP"] = [](event_type const & event, product_type const & product)
	{
		return product.m_genPhiStarCP;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["recoPhiStarCP"] = [](event_type const & event, product_type const & product)
	{
		return product.m_recoPhiStarCP;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["MassRoundOff1"] = [](event_type const & event, product_type const & product)
	{
		return product.m_genMassRoundOff1;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["MassRoundOff2"] = [](event_type const & event, product_type const & product)
	{
		return product.m_genMassRoundOff2;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["genPhi"] = [](event_type const & event, product_type const & product)
	{
		return product.m_genPhi;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["TauMProngEnergy"] = [](event_type const & event, product_type const & product)
	{
		return product.m_genChargedProngEnergies.first;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["TauPProngEnergy"] = [](event_type const & event, product_type const & product)
	{
		return product.m_genChargedProngEnergies.second;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["genPhiDet"] = [](event_type const & event, product_type const & product)
	{
		return product.m_genPhiDet;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["genPhiStarCPDet"] = [](event_type const & event, product_type const & product)
	{
		return product.m_genPhiStarCPDet;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["ThetaNuHadron"] = [](event_type const & event, product_type const & product)
	{
		return product.m_genThetaNuHadron;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["AlphaTauNeutrinos"] = [](event_type const & event, product_type const & product)
	{
		return product.m_genAlphaTauNeutrinos;
	};
	//Boson
	LambdaNtupleConsumer<HttTypes>::Quantities["genBosonSize"] = [](event_type const & event, product_type const & product)
	{
		return product.m_genBoson.size() > 0 ? product.m_genBoson.size() : DefaultValues::UndefinedDouble;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["1genBosonPt"] = [](event_type const & event, product_type const & product)
	{
		return product.m_genBoson.size() > 0 ? product.m_genBoson[0].node->p4.Pt() : DefaultValues::UndefinedDouble;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["1genBosonPz"] = [](event_type const & event, product_type const & product)
	{
		return product.m_genBoson.size() > 0 ? product.m_genBoson[0].node->p4.Pz() : DefaultValues::UndefinedDouble;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["1genBosonEta"] = [](event_type const & event, product_type const & product)
	{
		return product.m_genBoson.size() > 0 ? product.m_genBoson[0].node->p4.Eta() : DefaultValues::UndefinedDouble;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["1genBosonPhi"] = [](event_type const & event, product_type const & product)
	{
		return product.m_genBoson.size() > 0 ? product.m_genBoson[0].node->p4.Phi() : DefaultValues::UndefinedDouble;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["1genBosonMass"] = [](event_type const & event, product_type const & product)
	{
		return product.m_genBoson.size() > 0 ? product.m_genBoson[0].node->p4.mass() : DefaultValues::UndefinedDouble;
	};
		LambdaNtupleConsumer<HttTypes>::Quantities["1genBosonEnergy"] = [](event_type const & event, product_type const & product)
	{
		return product.m_genBoson.size() > 0 ? product.m_genBoson[0].node->p4.E() : DefaultValues::UndefinedDouble;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["1genBosonPdgId"] = [](event_type const & event, product_type const & product)
	{
		return product.m_genBoson.size() > 0 ? product.m_genBoson[0].node->pdgId() : DefaultValues::UndefinedDouble;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["1genBosonStatus"] = [](event_type const & event, product_type const & product)
	{
		return product.m_genBoson.size() > 0 ? product.m_genBoson[0].node->status() : DefaultValues::UndefinedDouble;
	};




	// Boson daughters
	LambdaNtupleConsumer<HttTypes>::Quantities["1genBosonDaughterSize"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 0) ? product.m_genBoson[0].Daughters.size() : DefaultValues::UndefinedDouble;
	};

	// charged particles of a one-prong
	LambdaNtupleConsumer<HttTypes>::Quantities["Tau1OneProngsSize"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 0) && (product.m_genBoson[0].Daughters[0].finalStateOneProngs.size() > 0)? product.m_genBoson[0].Daughters[0].finalStateOneProngs.size() : DefaultValues::UndefinedDouble;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["Tau2OneProngsSize"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[1].finalStateOneProngs.size() > 0)? product.m_genBoson[0].Daughters[1].finalStateOneProngs.size() : DefaultValues::UndefinedDouble;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["OneProngChargedPart1PdgId"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[0].finalStateOneProngs.size() > 0) && (product.m_genBoson[0].Daughters[1].finalStateOneProngs.size() > 0)? product.m_genOneProngCharged1->pdgId() : DefaultValues::UndefinedDouble;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["OneProngChargedPart1Pt"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[0].finalStateOneProngs.size() > 0) && (product.m_genBoson[0].Daughters[1].finalStateOneProngs.size() > 0)? product.m_genOneProngCharged1->p4.Pt() : DefaultValues::UndefinedDouble;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["OneProngChargedPart1Pz"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[0].finalStateOneProngs.size() > 0) && (product.m_genBoson[0].Daughters[1].finalStateOneProngs.size() > 0)? product.m_genOneProngCharged1->p4.Pz() : DefaultValues::UndefinedDouble;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["OneProngChargedPart1Eta"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[0].finalStateOneProngs.size() > 0) && (product.m_genBoson[0].Daughters[1].finalStateOneProngs.size() > 0)? product.m_genOneProngCharged1->p4.Eta() : DefaultValues::UndefinedDouble;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["OneProngChargedPart1Phi"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[0].finalStateOneProngs.size() > 0) && (product.m_genBoson[0].Daughters[1].finalStateOneProngs.size() > 0)? product.m_genOneProngCharged1->p4.Phi() : DefaultValues::UndefinedDouble;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["OneProngChargedPart1Mass"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[0].finalStateOneProngs.size() > 0) && (product.m_genBoson[0].Daughters[1].finalStateOneProngs.size() > 0)? product.m_genOneProngCharged1->p4.mass() : DefaultValues::UndefinedDouble;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["OneProngChargedPart1Energy"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[0].finalStateOneProngs.size() > 0) && (product.m_genBoson[0].Daughters[1].finalStateOneProngs.size() > 0)? product.m_genOneProngCharged1->p4.E() : DefaultValues::UndefinedDouble;
	};

	LambdaNtupleConsumer<HttTypes>::Quantities["OneProngChargedPart2PdgId"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[1].finalStateOneProngs.size() > 0) && (product.m_genBoson[0].Daughters[0].finalStateOneProngs.size() > 0)? product.m_genOneProngCharged2->pdgId() : DefaultValues::UndefinedDouble;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["OneProngChargedPart2Pt"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[1].finalStateOneProngs.size() > 0) && (product.m_genBoson[0].Daughters[0].finalStateOneProngs.size() > 0)? product.m_genOneProngCharged2->p4.Pt() : DefaultValues::UndefinedDouble;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["OneProngChargedPart2Pz"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[1].finalStateOneProngs.size() > 0) && (product.m_genBoson[0].Daughters[0].finalStateOneProngs.size() > 0)? product.m_genOneProngCharged2->p4.Pz() : DefaultValues::UndefinedDouble;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["OneProngChargedPart2Eta"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[1].finalStateOneProngs.size() > 0) && (product.m_genBoson[0].Daughters[0].finalStateOneProngs.size() > 0)? product.m_genOneProngCharged2->p4.Eta() : DefaultValues::UndefinedDouble;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["OneProngChargedPart2Phi"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[1].finalStateOneProngs.size() > 0) && (product.m_genBoson[0].Daughters[0].finalStateOneProngs.size() > 0)? product.m_genOneProngCharged2->p4.Phi() : DefaultValues::UndefinedDouble;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["OneProngChargedPart2Mass"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[1].finalStateOneProngs.size() > 0) && (product.m_genBoson[0].Daughters[0].finalStateOneProngs.size() > 0)? product.m_genOneProngCharged2->p4.mass() : DefaultValues::UndefinedDouble;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["OneProngChargedPart2Energy"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[1].finalStateOneProngs.size() > 0) && (product.m_genBoson[0].Daughters[0].finalStateOneProngs.size() > 0)? product.m_genOneProngCharged2->p4.E() : DefaultValues::UndefinedDouble;
	};
	// first daughter
	
	LambdaNtupleConsumer<HttTypes>::Quantities["TauMinusParent"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 0) ? product.m_genBoson[0].Daughters[0].parent->node->pdgId() : DefaultValues::UndefinedDouble;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["1genBoson1DaughterPt"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 0) ? product.m_genBoson[0].Daughters[0].node->p4.Pt() : DefaultValues::UndefinedDouble;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["1genBoson1DaughterPz"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 0) ? product.m_genBoson[0].Daughters[0].node->p4.Pz() : DefaultValues::UndefinedDouble;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["1genBoson1DaughterEta"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 0) ? product.m_genBoson[0].Daughters[0].node->p4.Eta() : DefaultValues::UndefinedDouble;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["1genBoson1DaughterPhi"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 0) ? product.m_genBoson[0].Daughters[0].node->p4.Phi() : DefaultValues::UndefinedDouble;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["1genBoson1DaughterMass"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 0) ? product.m_genBoson[0].Daughters[0].node->p4.mass() : DefaultValues::UndefinedDouble;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["1genBoson1DaughterCharge"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 0) ? product.m_genBoson[0].Daughters[0].getCharge() : DefaultValues::UndefinedDouble;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["1genBoson1DaughterEnergy"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 0) ? product.m_genBoson[0].Daughters[0].node->p4.E() : DefaultValues::UndefinedDouble;
	};	
	LambdaNtupleConsumer<HttTypes>::Quantities["1genBoson1DaughterPdgId"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 0) ? product.m_genBoson[0].Daughters[0].node->pdgId() : DefaultValues::UndefinedDouble;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["1genBoson1DaughterStatus"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 0) ? product.m_genBoson[0].Daughters[0].node->status() : DefaultValues::UndefinedDouble;
	};

	// second daughter
	LambdaNtupleConsumer<HttTypes>::Quantities["TauPlusParent"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 1) ? product.m_genBoson[0].Daughters[1].parent->node->pdgId() : DefaultValues::UndefinedDouble;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["1genBoson2DaughterPt"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 1) ? product.m_genBoson[0].Daughters[1].node->p4.Pt() : DefaultValues::UndefinedDouble;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["1genBoson2DaughterPz"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 1) ? product.m_genBoson[0].Daughters[1].node->p4.Pz() : DefaultValues::UndefinedDouble;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["1genBoson2DaughterEta"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 1) ? product.m_genBoson[0].Daughters[1].node->p4.Eta() : DefaultValues::UndefinedDouble;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["1genBoson2DaughterPhi"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 1) ? product.m_genBoson[0].Daughters[1].node->p4.Phi() : DefaultValues::UndefinedDouble;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["1genBoson2DaughterMass"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 1) ? product.m_genBoson[0].Daughters[1].node->p4.mass() : DefaultValues::UndefinedDouble;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["1genBoson2DaughterEnergy"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 1) ? product.m_genBoson[0].Daughters[1].node->p4.E() : DefaultValues::UndefinedDouble;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["1genBoson2DaughterPdgId"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 1) ? product.m_genBoson[0].Daughters[1].node->pdgId() : DefaultValues::UndefinedDouble;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["1genBoson2DaughterStatus"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 1) ? product.m_genBoson[0].Daughters[1].node->status() : DefaultValues::UndefinedDouble;
	};


	// Boson granddaughters
	LambdaNtupleConsumer<HttTypes>::Quantities["1genBoson1DaughterGranddaughterSize"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 0) && (product.m_genBoson[0].Daughters[0].Daughters.size() > 0) ? product.m_genBoson[0].Daughters[0].Daughters.size() : DefaultValues::UndefinedDouble;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["1genBoson2DaughterGranddaughterSize"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[1].Daughters.size() > 0) ? product.m_genBoson[0].Daughters[1].Daughters.size() : DefaultValues::UndefinedDouble;
	};


	// first daughter daughters
	LambdaNtupleConsumer<HttTypes>::Quantities["1genBoson1Daughter1GranddaughterPt"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 0) && (product.m_genBoson[0].Daughters[0].Daughters.size() > 0) ? product.m_genBoson[0].Daughters[0].Daughters[0].node->p4.Pt() : DefaultValues::UndefinedDouble;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["1genBoson1Daughter1GranddaughterPz"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 0) && (product.m_genBoson[0].Daughters[0].Daughters.size() > 0) ? product.m_genBoson[0].Daughters[0].Daughters[0].node->p4.Pz() : DefaultValues::UndefinedDouble;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["1genBoson1Daughter1GranddaughterEta"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 0) && (product.m_genBoson[0].Daughters[0].Daughters.size() > 0) ? product.m_genBoson[0].Daughters[0].Daughters[0].node->p4.Eta() : DefaultValues::UndefinedDouble;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["1genBoson1Daughter1GranddaughterPhi"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 0) && (product.m_genBoson[0].Daughters[0].Daughters.size() > 0) ? product.m_genBoson[0].Daughters[0].Daughters[0].node->p4.Phi() : DefaultValues::UndefinedDouble;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["1genBoson1Daughter1GranddaughterMass"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 0) && (product.m_genBoson[0].Daughters[0].Daughters.size() > 0) ? product.m_genBoson[0].Daughters[0].Daughters[0].node->p4.mass() : DefaultValues::UndefinedDouble;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["1genBoson1Daughter1GranddaughterEnergy"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 0) && (product.m_genBoson[0].Daughters[0].Daughters.size() > 0) ? product.m_genBoson[0].Daughters[0].Daughters[0].node->p4.E() : DefaultValues::UndefinedDouble;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["1genBoson1Daughter1GranddaughterPdgId"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 0) && (product.m_genBoson[0].Daughters[0].Daughters.size() > 0) ? product.m_genBoson[0].Daughters[0].Daughters[0].node->pdgId() : DefaultValues::UndefinedDouble;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["1genBoson1Daughter1GranddaughterStatus"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 0) && (product.m_genBoson[0].Daughters[0].Daughters.size() > 0) ? product.m_genBoson[0].Daughters[0].Daughters[0].node->status() : DefaultValues::UndefinedDouble;
	};

	LambdaNtupleConsumer<HttTypes>::Quantities["1genBoson1Daughter2GranddaughterPt"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 0) && (product.m_genBoson[0].Daughters[0].Daughters.size() > 1) ? product.m_genBoson[0].Daughters[0].Daughters[1].node->p4.Pt() : DefaultValues::UndefinedDouble;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["1genBoson1Daughter2GranddaughterPz"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 0) && (product.m_genBoson[0].Daughters[0].Daughters.size() > 1) ? product.m_genBoson[0].Daughters[0].Daughters[1].node->p4.Pz() : DefaultValues::UndefinedDouble;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["1genBoson1Daughter2GranddaughterEta"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 0) && (product.m_genBoson[0].Daughters[0].Daughters.size() > 1) ? product.m_genBoson[0].Daughters[0].Daughters[1].node->p4.Eta() : DefaultValues::UndefinedDouble;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["1genBoson1Daughter2GranddaughterPhi"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 0) && (product.m_genBoson[0].Daughters[0].Daughters.size() > 1) ? product.m_genBoson[0].Daughters[0].Daughters[1].node->p4.Phi() : DefaultValues::UndefinedDouble;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["1genBoson1Daughter2GranddaughterMass"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 0) && (product.m_genBoson[0].Daughters[0].Daughters.size() > 1) ? product.m_genBoson[0].Daughters[0].Daughters[1].node->p4.mass() : DefaultValues::UndefinedDouble;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["1genBoson1Daughter2GranddaughterEnergy"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 0) && (product.m_genBoson[0].Daughters[0].Daughters.size() > 1) ? product.m_genBoson[0].Daughters[0].Daughters[1].node->p4.E() : DefaultValues::UndefinedDouble;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["1genBoson1Daughter2GranddaughterPdgId"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 0) && (product.m_genBoson[0].Daughters[0].Daughters.size() > 1) ? product.m_genBoson[0].Daughters[0].Daughters[1].node->pdgId() : DefaultValues::UndefinedDouble;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["1genBoson1Daughter2GranddaughterStatus"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 0) && (product.m_genBoson[0].Daughters[0].Daughters.size() > 1) ? product.m_genBoson[0].Daughters[0].Daughters[1].node->status() : DefaultValues::UndefinedDouble;
	};

	LambdaNtupleConsumer<HttTypes>::Quantities["1genBoson1Daughter3GranddaughterPt"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 0) && (product.m_genBoson[0].Daughters[0].Daughters.size() > 2) ? product.m_genBoson[0].Daughters[0].Daughters[2].node->p4.Pt() : DefaultValues::UndefinedDouble;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["1genBoson1Daughter3GranddaughterPz"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 0) && (product.m_genBoson[0].Daughters[0].Daughters.size() > 2) ? product.m_genBoson[0].Daughters[0].Daughters[2].node->p4.Pz() : DefaultValues::UndefinedDouble;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["1genBoson1Daughter3GranddaughterEta"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 0) && (product.m_genBoson[0].Daughters[0].Daughters.size() > 2) ? product.m_genBoson[0].Daughters[0].Daughters[2].node->p4.Eta() : DefaultValues::UndefinedDouble;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["1genBoson1Daughter3GranddaughterPhi"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 0) && (product.m_genBoson[0].Daughters[0].Daughters.size() > 2) ? product.m_genBoson[0].Daughters[0].Daughters[2].node->p4.Phi() : DefaultValues::UndefinedDouble;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["1genBoson1Daughter3GranddaughterMass"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 0) && (product.m_genBoson[0].Daughters[0].Daughters.size() > 2) ? product.m_genBoson[0].Daughters[0].Daughters[2].node->p4.mass() : DefaultValues::UndefinedDouble;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["1genBoson1Daughter3GranddaughterEnergy"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 0) && (product.m_genBoson[0].Daughters[0].Daughters.size() > 2) ? product.m_genBoson[0].Daughters[0].Daughters[2].node->p4.E() : DefaultValues::UndefinedDouble;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["1genBoson1Daughter3GranddaughterPdgId"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 0) && (product.m_genBoson[0].Daughters[0].Daughters.size() > 2) ? product.m_genBoson[0].Daughters[0].Daughters[2].node->pdgId() : DefaultValues::UndefinedDouble;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["1genBoson1Daughter3GranddaughterStatus"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 0) && (product.m_genBoson[0].Daughters[0].Daughters.size() > 2) ? product.m_genBoson[0].Daughters[0].Daughters[2].node->status() : DefaultValues::UndefinedDouble;
	};

	LambdaNtupleConsumer<HttTypes>::Quantities["1genBoson1Daughter4GranddaughterPt"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 0) && (product.m_genBoson[0].Daughters[0].Daughters.size() > 3) ? product.m_genBoson[0].Daughters[0].Daughters[3].node->p4.Pt() : DefaultValues::UndefinedDouble;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["1genBoson1Daughter4GranddaughterPz"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 0) && (product.m_genBoson[0].Daughters[0].Daughters.size() > 3) ? product.m_genBoson[0].Daughters[0].Daughters[3].node->p4.Pz() : DefaultValues::UndefinedDouble;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["1genBoson1Daughter4GranddaughterEta"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 0) && (product.m_genBoson[0].Daughters[0].Daughters.size() > 3) ? product.m_genBoson[0].Daughters[0].Daughters[3].node->p4.Eta() : DefaultValues::UndefinedDouble;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["1genBoson1Daughter4GranddaughterPhi"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 0) && (product.m_genBoson[0].Daughters[0].Daughters.size() > 3) ? product.m_genBoson[0].Daughters[0].Daughters[3].node->p4.Phi() : DefaultValues::UndefinedDouble;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["1genBoson1Daughter4GranddaughterMass"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 0) && (product.m_genBoson[0].Daughters[0].Daughters.size() > 3) ? product.m_genBoson[0].Daughters[0].Daughters[3].node->p4.mass() : DefaultValues::UndefinedDouble;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["1genBoson1Daughter4GranddaughterEnergy"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 0) && (product.m_genBoson[0].Daughters[0].Daughters.size() > 3) ? product.m_genBoson[0].Daughters[0].Daughters[3].node->p4.E() : DefaultValues::UndefinedDouble;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["1genBoson1Daughter4GranddaughterPdgId"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 0) && (product.m_genBoson[0].Daughters[0].Daughters.size() > 3) ? product.m_genBoson[0].Daughters[0].Daughters[3].node->pdgId() : DefaultValues::UndefinedDouble;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["1genBoson1Daughter4GranddaughterStatus"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 0) && (product.m_genBoson[0].Daughters[0].Daughters.size() > 3) ? product.m_genBoson[0].Daughters[0].Daughters[3].node->status() : DefaultValues::UndefinedDouble;
	};


	// second daughter daughters
	LambdaNtupleConsumer<HttTypes>::Quantities["1genBoson2Daughter1GranddaughterPt"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[1].Daughters.size() > 0) ? product.m_genBoson[0].Daughters[1].Daughters[0].node->p4.Pt() : DefaultValues::UndefinedDouble;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["1genBoson2Daughter1GranddaughterPz"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[1].Daughters.size() > 0) ? product.m_genBoson[0].Daughters[1].Daughters[0].node->p4.Pz() : DefaultValues::UndefinedDouble;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["1genBoson2Daughter1GranddaughterEta"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[1].Daughters.size() > 0) ? product.m_genBoson[0].Daughters[1].Daughters[0].node->p4.Eta() : DefaultValues::UndefinedDouble;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["1genBoson2Daughter1GranddaughterPhi"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[1].Daughters.size() > 0) ? product.m_genBoson[0].Daughters[1].Daughters[0].node->p4.Phi() : DefaultValues::UndefinedDouble;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["1genBoson2Daughter1GranddaughterMass"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[1].Daughters.size() > 0) ? product.m_genBoson[0].Daughters[1].Daughters[0].node->p4.mass() : DefaultValues::UndefinedDouble;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["1genBoson2Daughter1GranddaughterEnergy"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[1].Daughters.size() > 0) ? product.m_genBoson[0].Daughters[1].Daughters[0].node->p4.E() : DefaultValues::UndefinedDouble;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["1genBoson2Daughter1GranddaughterPdgId"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[1].Daughters.size() > 0) ? product.m_genBoson[0].Daughters[1].Daughters[0].node->pdgId() : DefaultValues::UndefinedDouble;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["1genBoson2Daughter1GranddaughterStatus"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[1].Daughters.size() > 0) ? product.m_genBoson[0].Daughters[1].Daughters[0].node->status() : DefaultValues::UndefinedDouble;
	};

	LambdaNtupleConsumer<HttTypes>::Quantities["1genBoson2Daughter2GranddaughterPt"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[1].Daughters.size() > 1) ? product.m_genBoson[0].Daughters[1].Daughters[1].node->p4.Pt() : DefaultValues::UndefinedDouble;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["1genBoson2Daughter2GranddaughterPz"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[1].Daughters.size() > 1) ? product.m_genBoson[0].Daughters[1].Daughters[1].node->p4.Pz() : DefaultValues::UndefinedDouble;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["1genBoson2Daughter2GranddaughterEta"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[1].Daughters.size() > 1) ? product.m_genBoson[0].Daughters[1].Daughters[1].node->p4.Eta() : DefaultValues::UndefinedDouble;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["1genBoson2Daughter2GranddaughterPhi"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[1].Daughters.size() > 1) ? product.m_genBoson[0].Daughters[1].Daughters[1].node->p4.Phi() : DefaultValues::UndefinedDouble;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["1genBoson2Daughter2GranddaughterMass"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[1].Daughters.size() > 1) ? product.m_genBoson[0].Daughters[1].Daughters[1].node->p4.mass() : DefaultValues::UndefinedDouble;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["1genBoson2Daughter2GranddaughterEnergy"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[1].Daughters.size() > 1) ? product.m_genBoson[0].Daughters[1].Daughters[1].node->p4.E() : DefaultValues::UndefinedDouble;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["1genBoson2Daughter2GranddaughterPdgId"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[1].Daughters.size() > 1) ? product.m_genBoson[0].Daughters[1].Daughters[1].node->pdgId() : DefaultValues::UndefinedDouble;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["1genBoson2Daughter2GranddaughterStatus"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[1].Daughters.size() > 1) ? product.m_genBoson[0].Daughters[1].Daughters[1].node->status() : DefaultValues::UndefinedDouble;
	};

	LambdaNtupleConsumer<HttTypes>::Quantities["1genBoson2Daughter3GranddaughterPt"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[1].Daughters.size() > 2) ? product.m_genBoson[0].Daughters[1].Daughters[2].node->p4.Pt() : DefaultValues::UndefinedDouble;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["1genBoson2Daughter3GranddaughterPz"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[1].Daughters.size() > 2) ? product.m_genBoson[0].Daughters[1].Daughters[2].node->p4.Pz() : DefaultValues::UndefinedDouble;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["1genBoson2Daughter3GranddaughterEta"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[1].Daughters.size() > 2) ? product.m_genBoson[0].Daughters[1].Daughters[2].node->p4.Eta() : DefaultValues::UndefinedDouble;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["1genBoson2Daughter3GranddaughterPhi"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[1].Daughters.size() > 2) ? product.m_genBoson[0].Daughters[1].Daughters[2].node->p4.Phi() : DefaultValues::UndefinedDouble;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["1genBoson2Daughter3GranddaughterMass"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[1].Daughters.size() > 2) ? product.m_genBoson[0].Daughters[1].Daughters[2].node->p4.mass() : DefaultValues::UndefinedDouble;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["1genBoson2Daughter3GranddaughterEnergy"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[1].Daughters.size() > 2) ? product.m_genBoson[0].Daughters[1].Daughters[2].node->p4.E() : DefaultValues::UndefinedDouble;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["1genBoson2Daughter3GranddaughterPdgId"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[1].Daughters.size() > 2) ? product.m_genBoson[0].Daughters[1].Daughters[2].node->pdgId() : DefaultValues::UndefinedDouble;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["1genBoson2Daughter3GranddaughterStatus"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[1].Daughters.size() > 2) ? product.m_genBoson[0].Daughters[1].Daughters[2].node->status() : DefaultValues::UndefinedDouble;
	};

	LambdaNtupleConsumer<HttTypes>::Quantities["1genBoson2Daughter4GranddaughterPt"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[1].Daughters.size() > 3) ? product.m_genBoson[0].Daughters[1].Daughters[3].node->p4.Pt() : DefaultValues::UndefinedDouble;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["1genBoson2Daughter4GranddaughterPz"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[1].Daughters.size() > 3) ? product.m_genBoson[0].Daughters[1].Daughters[3].node->p4.Pz() : DefaultValues::UndefinedDouble;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["1genBoson2Daughter4GranddaughterEta"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[1].Daughters.size() > 3) ? product.m_genBoson[0].Daughters[1].Daughters[3].node->p4.Eta() : DefaultValues::UndefinedDouble;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["1genBoson2Daughter4GranddaughterPhi"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[1].Daughters.size() > 3) ? product.m_genBoson[0].Daughters[1].Daughters[3].node->p4.Phi() : DefaultValues::UndefinedDouble;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["1genBoson2Daughter4GranddaughterMass"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[1].Daughters.size() > 3) ? product.m_genBoson[0].Daughters[1].Daughters[3].node->p4.mass() : DefaultValues::UndefinedDouble;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["1genBoson2Daughter4GranddaughterEnergy"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[1].Daughters.size() > 3) ? product.m_genBoson[0].Daughters[1].Daughters[3].node->p4.E() : DefaultValues::UndefinedDouble;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["1genBoson2Daughter4GranddaughterPdgId"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[1].Daughters.size() > 3) ? product.m_genBoson[0].Daughters[1].Daughters[3].node->pdgId() : DefaultValues::UndefinedDouble;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["1genBoson2Daughter4GranddaughterStatus"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[1].Daughters.size() > 3) ? product.m_genBoson[0].Daughters[1].Daughters[3].node->status() : DefaultValues::UndefinedDouble;
	};

	// Boson GrandGranddaughters: the only GrandGranddaughters we need are from 2nd Granddaughters
	LambdaNtupleConsumer<HttTypes>::Quantities["1genBoson1Daughter2GranddaughterGrandGranddaughterSize"] = [](event_type const & event, product_type const & product)
	{	
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 0) && (product.m_genBoson[0].Daughters[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[0].Daughters[1].Daughters.size() >0)? product.m_genBoson[0].Daughters[0].Daughters[1].Daughters.size() : DefaultValues::UndefinedDouble;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["1genBoson2Daughter2GranddaughterGrandGranddaughterSize"] = [](event_type const & event, product_type const & product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[1].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[1].Daughters[1].Daughters.size() >0)? product.m_genBoson[0].Daughters[1].Daughters[1].Daughters.size() : DefaultValues::UndefinedDouble;
	};


	
	LambdaNtupleConsumer<HttTypes>::Quantities["1genBoson1Daughter2Granddaughter1GrandGranddaughterPdgId"] = [](event_type const & event, product_type const & product)
	{	
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 0) && (product.m_genBoson[0].Daughters[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[0].Daughters[1].Daughters.size() >0)? product.m_genBoson[0].Daughters[0].Daughters[1].Daughters[0].node->pdgId() : DefaultValues::UndefinedDouble;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["1genBoson1Daughter2Granddaughter1GrandGranddaughterStatus"] = [](event_type const & event, product_type const & product)
	{	
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 0) && (product.m_genBoson[0].Daughters[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[0].Daughters[1].Daughters.size() >0)? product.m_genBoson[0].Daughters[0].Daughters[1].Daughters[0].node->status() : DefaultValues::UndefinedDouble;
	};

	LambdaNtupleConsumer<HttTypes>::Quantities["1genBoson1Daughter2Granddaughter2GrandGranddaughterPdgId"] = [](event_type const & event, product_type const & product)
	{	
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 0) && (product.m_genBoson[0].Daughters[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[0].Daughters[1].Daughters.size() >1)? product.m_genBoson[0].Daughters[0].Daughters[1].Daughters[1].node->pdgId() : DefaultValues::UndefinedDouble;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["1genBoson1Daughter2Granddaughter2GrandGranddaughterStatus"] = [](event_type const & event, product_type const & product)
	{	
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 0) && (product.m_genBoson[0].Daughters[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[0].Daughters[1].Daughters.size() >1)? product.m_genBoson[0].Daughters[0].Daughters[1].Daughters[1].node->status() : DefaultValues::UndefinedDouble;
	};

	LambdaNtupleConsumer<HttTypes>::Quantities["1genBoson1Daughter2Granddaughter3GrandGranddaughterPdgId"] = [](event_type const & event, product_type const & product)
	{	
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 0) && (product.m_genBoson[0].Daughters[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[0].Daughters[1].Daughters.size() >2)? product.m_genBoson[0].Daughters[0].Daughters[1].Daughters[2].node->pdgId() : DefaultValues::UndefinedDouble;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["1genBoson1Daughter2Granddaughter3GrandGranddaughterStatus"] = [](event_type const & event, product_type const & product)
	{	
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 0) && (product.m_genBoson[0].Daughters[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[0].Daughters[1].Daughters.size() >2)? product.m_genBoson[0].Daughters[0].Daughters[1].Daughters[2].node->status() : DefaultValues::UndefinedDouble;
	};
	
	LambdaNtupleConsumer<HttTypes>::Quantities["1genBoson1Daughter2Granddaughter4GrandGranddaughterPdgId"] = [](event_type const & event, product_type const & product)
	{	
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 0) && (product.m_genBoson[0].Daughters[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[0].Daughters[1].Daughters.size() >3)? product.m_genBoson[0].Daughters[0].Daughters[1].Daughters[3].node->pdgId() : DefaultValues::UndefinedDouble;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["1genBoson1Daughter2Granddaughter4GrandGranddaughterStatus"] = [](event_type const & event, product_type const & product)
	{	
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 0) && (product.m_genBoson[0].Daughters[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[0].Daughters[1].Daughters.size() >3)? product.m_genBoson[0].Daughters[0].Daughters[1].Daughters[3].node->status() : DefaultValues::UndefinedDouble;
	};	
	
	LambdaNtupleConsumer<HttTypes>::Quantities["1genBoson1Daughter2Granddaughter5GrandGranddaughterPdgId"] = [](event_type const & event, product_type const & product)
	{	
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 0) && (product.m_genBoson[0].Daughters[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[0].Daughters[1].Daughters.size() >4)? product.m_genBoson[0].Daughters[0].Daughters[1].Daughters[4].node->pdgId() : DefaultValues::UndefinedDouble;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["1genBoson1Daughter2Granddaughter5GrandGranddaughterStatus"] = [](event_type const & event, product_type const & product)
	{	
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 0) && (product.m_genBoson[0].Daughters[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[0].Daughters[1].Daughters.size() >4)? product.m_genBoson[0].Daughters[0].Daughters[1].Daughters[4].node->status() : DefaultValues::UndefinedDouble;
	};
	
	LambdaNtupleConsumer<HttTypes>::Quantities["1genBoson1Daughter2Granddaughter6GrandGranddaughterPdgId"] = [](event_type const & event, product_type const & product)
	{	
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 0) && (product.m_genBoson[0].Daughters[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[0].Daughters[1].Daughters.size() >5)? product.m_genBoson[0].Daughters[0].Daughters[1].Daughters[5].node->pdgId() : DefaultValues::UndefinedDouble;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["1genBoson1Daughter2Granddaughter6GrandGranddaughterStatus"] = [](event_type const & event, product_type const & product)
	{	
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 0) && (product.m_genBoson[0].Daughters[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[0].Daughters[1].Daughters.size() >5)? product.m_genBoson[0].Daughters[0].Daughters[1].Daughters[5].node->status() : DefaultValues::UndefinedDouble;
	};
	
	// settings for synch ntuples
	LambdaNtupleConsumer<HttTypes>::Quantities["evt"] = [](event_type const& event, product_type const& product) { return event.m_eventMetadata->nEvent; };
	LambdaNtupleConsumer<HttTypes>::Quantities["puweight"] = [](event_type const& event, product_type const& product) {
		return SafeMap::GetWithDefault(product.m_weights, std::string("puWeight"), 1.0);
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["trigweight_1"] = [](event_type const& event, product_type const& product) {
		return SafeMap::GetWithDefault(product.m_weights, std::string("triggerWeight1"), 1.0);
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["trigweight_2"] = [](event_type const& event, product_type const& product) {
		return SafeMap::GetWithDefault(product.m_weights, std::string("triggerWeight2"), 1.0);
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["weight"] = [pipeline](event_type const& event, product_type const& product) {
		return SafeMap::GetWithDefault(product.m_weights, pipeline->GetSettings().GetEventWeight(), 1.0);
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["mvis"] = LambdaNtupleConsumer<HttTypes>::Quantities["diLepMass"];
	LambdaNtupleConsumer<HttTypes>::Quantities["pt_1"] = LambdaNtupleConsumer<HttTypes>::Quantities["lep1Pt"];
	LambdaNtupleConsumer<HttTypes>::Quantities["eta_1"] = LambdaNtupleConsumer<HttTypes>::Quantities["lep1Eta"];
	LambdaNtupleConsumer<HttTypes>::Quantities["phi_1"] = LambdaNtupleConsumer<HttTypes>::Quantities["lep1Phi"];
	LambdaNtupleConsumer<HttTypes>::Quantities["m_1"] = LambdaNtupleConsumer<HttTypes>::Quantities["lep1Mass"];
	LambdaNtupleConsumer<HttTypes>::Quantities["q_1"] = LambdaNtupleConsumer<HttTypes>::Quantities["lep1Charge"];
	LambdaNtupleConsumer<HttTypes>::Quantities["iso_1"] = LambdaNtupleConsumer<HttTypes>::Quantities["lep1IsoOverPt"];
	LambdaNtupleConsumer<HttTypes>::Quantities["mt_1"] = LambdaNtupleConsumer<HttTypes>::Quantities["lep1Mt"];
	LambdaNtupleConsumer<HttTypes>::Quantities["pt_2"] = LambdaNtupleConsumer<HttTypes>::Quantities["lep2Pt"];
	LambdaNtupleConsumer<HttTypes>::Quantities["eta_2"] = LambdaNtupleConsumer<HttTypes>::Quantities["lep2Eta"];
	LambdaNtupleConsumer<HttTypes>::Quantities["phi_2"] = LambdaNtupleConsumer<HttTypes>::Quantities["lep2Phi"];
	LambdaNtupleConsumer<HttTypes>::Quantities["m_2"] = LambdaNtupleConsumer<HttTypes>::Quantities["lep2Mass"];
	LambdaNtupleConsumer<HttTypes>::Quantities["q_2"] = LambdaNtupleConsumer<HttTypes>::Quantities["lep2Charge"];
	LambdaNtupleConsumer<HttTypes>::Quantities["iso_2"] = LambdaNtupleConsumer<HttTypes>::Quantities["lep2IsoOverPt"];
	LambdaNtupleConsumer<HttTypes>::Quantities["mt_2"] = LambdaNtupleConsumer<HttTypes>::Quantities["lep2Mt"];
	LambdaNtupleConsumer<HttTypes>::Quantities["met"] = LambdaNtupleConsumer<HttTypes>::Quantities["pfMetPt"];
	LambdaNtupleConsumer<HttTypes>::Quantities["metphi"] = LambdaNtupleConsumer<HttTypes>::Quantities["pfMetPhi"];
	LambdaNtupleConsumer<HttTypes>::Quantities["metcov00"] = LambdaNtupleConsumer<HttTypes>::Quantities["pfMetCov00"];
	LambdaNtupleConsumer<HttTypes>::Quantities["metcov01"] = LambdaNtupleConsumer<HttTypes>::Quantities["pfMetCov01"];
	LambdaNtupleConsumer<HttTypes>::Quantities["metcov10"] = LambdaNtupleConsumer<HttTypes>::Quantities["pfMetCov10"];
	LambdaNtupleConsumer<HttTypes>::Quantities["metcov11"] = LambdaNtupleConsumer<HttTypes>::Quantities["pfMetCov11"];
	LambdaNtupleConsumer<HttTypes>::Quantities["mvamet"] = LambdaNtupleConsumer<HttTypes>::Quantities["mvaMetPt"];
	LambdaNtupleConsumer<HttTypes>::Quantities["mvametphi"] = LambdaNtupleConsumer<HttTypes>::Quantities["mvaMetPhi"];
	LambdaNtupleConsumer<HttTypes>::Quantities["mvacov00"] = LambdaNtupleConsumer<HttTypes>::Quantities["mvaMetCov00"];
	LambdaNtupleConsumer<HttTypes>::Quantities["mvacov01"] = LambdaNtupleConsumer<HttTypes>::Quantities["mvaMetCov01"];
	LambdaNtupleConsumer<HttTypes>::Quantities["mvacov10"] = LambdaNtupleConsumer<HttTypes>::Quantities["mvaMetCov10"];
	LambdaNtupleConsumer<HttTypes>::Quantities["mvacov11"] = LambdaNtupleConsumer<HttTypes>::Quantities["mvaMetCov11"];
	LambdaNtupleConsumer<HttTypes>::Quantities["jpt_1"] = LambdaNtupleConsumer<HttTypes>::Quantities["leadingJetPt"];
	LambdaNtupleConsumer<HttTypes>::Quantities["jeta_1"] = LambdaNtupleConsumer<HttTypes>::Quantities["leadingJetEta"];
	LambdaNtupleConsumer<HttTypes>::Quantities["jphi_1"] = LambdaNtupleConsumer<HttTypes>::Quantities["leadingJetPhi"];
	LambdaNtupleConsumer<HttTypes>::Quantities["jpt_2"] = LambdaNtupleConsumer<HttTypes>::Quantities["trailingJetPt"];
	LambdaNtupleConsumer<HttTypes>::Quantities["jeta_2"] = LambdaNtupleConsumer<HttTypes>::Quantities["trailingJetEta"];
	LambdaNtupleConsumer<HttTypes>::Quantities["jphi_2"] = LambdaNtupleConsumer<HttTypes>::Quantities["trailingJetPhi"];
	LambdaNtupleConsumer<HttTypes>::Quantities["mjj"] = LambdaNtupleConsumer<HttTypes>::Quantities["diJetMass"];
	LambdaNtupleConsumer<HttTypes>::Quantities["jdeta"] = LambdaNtupleConsumer<HttTypes>::Quantities["diJetAbsDeltaEta"];
	LambdaNtupleConsumer<HttTypes>::Quantities["njets"] = LambdaNtupleConsumer<HttTypes>::Quantities["nJets"];
	LambdaNtupleConsumer<HttTypes>::Quantities["pt_sv"] = LambdaNtupleConsumer<HttTypes>::Quantities["diTauPt"];
	LambdaNtupleConsumer<HttTypes>::Quantities["eta_sv"] = LambdaNtupleConsumer<HttTypes>::Quantities["diTauEta"];
	LambdaNtupleConsumer<HttTypes>::Quantities["phi_sv"] = LambdaNtupleConsumer<HttTypes>::Quantities["diTauPhi"];
	LambdaNtupleConsumer<HttTypes>::Quantities["m_sv"] = LambdaNtupleConsumer<HttTypes>::Quantities["diTauMass"];
	
	// need to be called at last
	KappaLambdaNtupleConsumer<HttTypes>::Init(pipeline);
}
