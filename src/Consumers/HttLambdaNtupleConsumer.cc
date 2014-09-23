
#include <Math/VectorUtil.h>

#include "Artus/Utility/interface/SafeMap.h"
#include "Artus/Utility/interface/Utility.h"
#include "Artus/Utility/interface/DefaultValues.h"
#include "Artus/KappaAnalysis/interface/KappaTypes.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/Consumers/HttLambdaNtupleConsumer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/DiJetQuantitiesProducer.h"


void HttLambdaNtupleConsumer::Init(setting_type const& settings)
{
	// add possible quantities for the lambda ntuples consumers
	
	// settings for synch ntuples
	LambdaNtupleConsumer<KappaTypes>::AddQuantity("evt", [](KappaEvent const& event, KappaProduct const& product)
	{
		return event.m_eventMetadata->nEvent;
	});
	LambdaNtupleConsumer<KappaTypes>::AddQuantity("puweight", [](KappaEvent const& event, KappaProduct const& product) {
		return SafeMap::GetWithDefault(product.m_weights, std::string("puWeight"), 1.0);
	});
	LambdaNtupleConsumer<KappaTypes>::AddQuantity("trigweight_1", [](KappaEvent const& event, KappaProduct const& product) {
		return SafeMap::GetWithDefault(product.m_weights, std::string("triggerWeight1"), 1.0);
	});
	LambdaNtupleConsumer<KappaTypes>::AddQuantity("trigweight_2", [](KappaEvent const& event, KappaProduct const& product) {
		return SafeMap::GetWithDefault(product.m_weights, std::string("triggerWeight2"), 1.0);
	});
	LambdaNtupleConsumer<KappaTypes>::AddQuantity("weight", [settings](KappaEvent const& event, KappaProduct const& product) {
		return SafeMap::GetWithDefault(product.m_weights, settings.GetEventWeight(), 1.0);
	});
	LambdaNtupleConsumer<KappaTypes>::AddQuantity("mvis", LambdaNtupleConsumer<KappaTypes>::GetQuantities()["diLepMass"]);
	LambdaNtupleConsumer<KappaTypes>::AddQuantity("pt_1", LambdaNtupleConsumer<KappaTypes>::GetQuantities()["lep1Pt"]);
	LambdaNtupleConsumer<KappaTypes>::AddQuantity("eta_1", LambdaNtupleConsumer<KappaTypes>::GetQuantities()["lep1Eta"]);
	LambdaNtupleConsumer<KappaTypes>::AddQuantity("phi_1", LambdaNtupleConsumer<KappaTypes>::GetQuantities()["lep1Phi"]);
	LambdaNtupleConsumer<KappaTypes>::AddQuantity("m_1", LambdaNtupleConsumer<KappaTypes>::GetQuantities()["lep1Mass"]);
	LambdaNtupleConsumer<KappaTypes>::AddQuantity("q_1", LambdaNtupleConsumer<KappaTypes>::GetQuantities()["lep1Charge"]);
	LambdaNtupleConsumer<KappaTypes>::AddQuantity("iso_1", LambdaNtupleConsumer<KappaTypes>::GetQuantities()["lep1IsoOverPt"]);
	LambdaNtupleConsumer<KappaTypes>::AddQuantity("mt_1", LambdaNtupleConsumer<KappaTypes>::GetQuantities()["lep1Mt"]);
	LambdaNtupleConsumer<KappaTypes>::AddQuantity("pt_2", LambdaNtupleConsumer<KappaTypes>::GetQuantities()["lep2Pt"]);
	LambdaNtupleConsumer<KappaTypes>::AddQuantity("eta_2", LambdaNtupleConsumer<KappaTypes>::GetQuantities()["lep2Eta"]);
	LambdaNtupleConsumer<KappaTypes>::AddQuantity("phi_2", LambdaNtupleConsumer<KappaTypes>::GetQuantities()["lep2Phi"]);
	LambdaNtupleConsumer<KappaTypes>::AddQuantity("m_2", LambdaNtupleConsumer<KappaTypes>::GetQuantities()["lep2Mass"]);
	LambdaNtupleConsumer<KappaTypes>::AddQuantity("q_2", LambdaNtupleConsumer<KappaTypes>::GetQuantities()["lep2Charge"]);
	LambdaNtupleConsumer<KappaTypes>::AddQuantity("iso_2", LambdaNtupleConsumer<KappaTypes>::GetQuantities()["lep2IsoOverPt"]);
	LambdaNtupleConsumer<KappaTypes>::AddQuantity("mt_2", LambdaNtupleConsumer<KappaTypes>::GetQuantities()["lep2Mt"]);
	LambdaNtupleConsumer<KappaTypes>::AddQuantity("met", LambdaNtupleConsumer<KappaTypes>::GetQuantities()["pfMetPt"]);
	LambdaNtupleConsumer<KappaTypes>::AddQuantity("metphi", LambdaNtupleConsumer<KappaTypes>::GetQuantities()["pfMetPhi"]);
	LambdaNtupleConsumer<KappaTypes>::AddQuantity("metcov00", LambdaNtupleConsumer<KappaTypes>::GetQuantities()["pfMetCov00"]);
	LambdaNtupleConsumer<KappaTypes>::AddQuantity("metcov01", LambdaNtupleConsumer<KappaTypes>::GetQuantities()["pfMetCov01"]);
	LambdaNtupleConsumer<KappaTypes>::AddQuantity("metcov10", LambdaNtupleConsumer<KappaTypes>::GetQuantities()["pfMetCov10"]);
	LambdaNtupleConsumer<KappaTypes>::AddQuantity("metcov11", LambdaNtupleConsumer<KappaTypes>::GetQuantities()["pfMetCov11"]);
	LambdaNtupleConsumer<KappaTypes>::AddQuantity("mvamet", LambdaNtupleConsumer<KappaTypes>::GetQuantities()["mvaMetPt"]);
	LambdaNtupleConsumer<KappaTypes>::AddQuantity("mvametphi", LambdaNtupleConsumer<KappaTypes>::GetQuantities()["mvaMetPhi"]);
	LambdaNtupleConsumer<KappaTypes>::AddQuantity("mvacov00", LambdaNtupleConsumer<KappaTypes>::GetQuantities()["mvaMetCov00"]);
	LambdaNtupleConsumer<KappaTypes>::AddQuantity("mvacov01", LambdaNtupleConsumer<KappaTypes>::GetQuantities()["mvaMetCov01"]);
	LambdaNtupleConsumer<KappaTypes>::AddQuantity("mvacov10", LambdaNtupleConsumer<KappaTypes>::GetQuantities()["mvaMetCov10"]);
	LambdaNtupleConsumer<KappaTypes>::AddQuantity("mvacov11", LambdaNtupleConsumer<KappaTypes>::GetQuantities()["mvaMetCov11"]);
	LambdaNtupleConsumer<KappaTypes>::AddQuantity("jpt_1", LambdaNtupleConsumer<KappaTypes>::GetQuantities()["leadingJetPt"]);
	LambdaNtupleConsumer<KappaTypes>::AddQuantity("jeta_1", LambdaNtupleConsumer<KappaTypes>::GetQuantities()["leadingJetEta"]);
	LambdaNtupleConsumer<KappaTypes>::AddQuantity("jphi_1", LambdaNtupleConsumer<KappaTypes>::GetQuantities()["leadingJetPhi"]);
	LambdaNtupleConsumer<KappaTypes>::AddQuantity("jpt_2", LambdaNtupleConsumer<KappaTypes>::GetQuantities()["trailingJetPt"]);
	LambdaNtupleConsumer<KappaTypes>::AddQuantity("jeta_2", LambdaNtupleConsumer<KappaTypes>::GetQuantities()["trailingJetEta"]);
	LambdaNtupleConsumer<KappaTypes>::AddQuantity("jphi_2", LambdaNtupleConsumer<KappaTypes>::GetQuantities()["trailingJetPhi"]);
	LambdaNtupleConsumer<KappaTypes>::AddQuantity("mjj", LambdaNtupleConsumer<KappaTypes>::GetQuantities()["diJetMass"]);
	LambdaNtupleConsumer<KappaTypes>::AddQuantity("jdeta", LambdaNtupleConsumer<KappaTypes>::GetQuantities()["diJetAbsDeltaEta"]);
	LambdaNtupleConsumer<KappaTypes>::AddQuantity("njets", LambdaNtupleConsumer<KappaTypes>::GetQuantities()["nJets"]);
	LambdaNtupleConsumer<KappaTypes>::AddQuantity("pt_sv", LambdaNtupleConsumer<KappaTypes>::GetQuantities()["diTauPt"]);
	LambdaNtupleConsumer<KappaTypes>::AddQuantity("eta_sv", LambdaNtupleConsumer<KappaTypes>::GetQuantities()["diTauEta"]);
	LambdaNtupleConsumer<KappaTypes>::AddQuantity("phi_sv", LambdaNtupleConsumer<KappaTypes>::GetQuantities()["diTauPhi"]);
	LambdaNtupleConsumer<KappaTypes>::AddQuantity("m_sv", LambdaNtupleConsumer<KappaTypes>::GetQuantities()["diTauMass"]);
	
	// need to be called at last
	KappaLambdaNtupleConsumer::Init(settings);
}
