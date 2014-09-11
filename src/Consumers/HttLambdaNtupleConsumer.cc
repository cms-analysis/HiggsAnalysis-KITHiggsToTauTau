
#include <Math/VectorUtil.h>

#include "Artus/Utility/interface/SafeMap.h"
#include "Artus/Utility/interface/Utility.h"
#include "Artus/Utility/interface/DefaultValues.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/Consumers/HttLambdaNtupleConsumer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/DiJetQuantitiesProducer.h"


void HttLambdaNtupleConsumer::Init(setting_type const& settings)
{
	// add possible quantities for the lambda ntuples consumers
	
	// settings for synch ntuples
	LambdaNtupleConsumer<HttTypes>::Quantities["evt"] = [](event_type const& event, product_type const& product)
	{
		return event.m_eventMetadata->nEvent;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["puweight"] = [](event_type const& event, product_type const& product) {
		return SafeMap::GetWithDefault(product.m_weights, std::string("puWeight"), 1.0);
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["trigweight_1"] = [](event_type const& event, product_type const& product) {
		return SafeMap::GetWithDefault(product.m_weights, std::string("triggerWeight1"), 1.0);
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["trigweight_2"] = [](event_type const& event, product_type const& product) {
		return SafeMap::GetWithDefault(product.m_weights, std::string("triggerWeight2"), 1.0);
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["weight"] = [settings](event_type const& event, product_type const& product) {
		return SafeMap::GetWithDefault(product.m_weights, settings.GetEventWeight(), 1.0);
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
	KappaLambdaNtupleConsumer::Init(settings);
}
