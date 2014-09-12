
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
	LambdaNtupleConsumer<KappaTypes>::Quantities["evt"] = [](KappaEvent const& event, KappaProduct const& product)
	{
		return event.m_eventMetadata->nEvent;
	};
	LambdaNtupleConsumer<KappaTypes>::Quantities["puweight"] = [](KappaEvent const& event, KappaProduct const& product) {
		return SafeMap::GetWithDefault(product.m_weights, std::string("puWeight"), 1.0);
	};
	LambdaNtupleConsumer<KappaTypes>::Quantities["trigweight_1"] = [](KappaEvent const& event, KappaProduct const& product) {
		return SafeMap::GetWithDefault(product.m_weights, std::string("triggerWeight1"), 1.0);
	};
	LambdaNtupleConsumer<KappaTypes>::Quantities["trigweight_2"] = [](KappaEvent const& event, KappaProduct const& product) {
		return SafeMap::GetWithDefault(product.m_weights, std::string("triggerWeight2"), 1.0);
	};
	LambdaNtupleConsumer<KappaTypes>::Quantities["weight"] = [settings](KappaEvent const& event, KappaProduct const& product) {
		return SafeMap::GetWithDefault(product.m_weights, settings.GetEventWeight(), 1.0);
	};
	LambdaNtupleConsumer<KappaTypes>::Quantities["mvis"] = LambdaNtupleConsumer<KappaTypes>::Quantities["diLepMass"];
	LambdaNtupleConsumer<KappaTypes>::Quantities["pt_1"] = LambdaNtupleConsumer<KappaTypes>::Quantities["lep1Pt"];
	LambdaNtupleConsumer<KappaTypes>::Quantities["eta_1"] = LambdaNtupleConsumer<KappaTypes>::Quantities["lep1Eta"];
	LambdaNtupleConsumer<KappaTypes>::Quantities["phi_1"] = LambdaNtupleConsumer<KappaTypes>::Quantities["lep1Phi"];
	LambdaNtupleConsumer<KappaTypes>::Quantities["m_1"] = LambdaNtupleConsumer<KappaTypes>::Quantities["lep1Mass"];
	LambdaNtupleConsumer<KappaTypes>::Quantities["q_1"] = LambdaNtupleConsumer<KappaTypes>::Quantities["lep1Charge"];
	LambdaNtupleConsumer<KappaTypes>::Quantities["iso_1"] = LambdaNtupleConsumer<KappaTypes>::Quantities["lep1IsoOverPt"];
	LambdaNtupleConsumer<KappaTypes>::Quantities["mt_1"] = LambdaNtupleConsumer<KappaTypes>::Quantities["lep1Mt"];
	LambdaNtupleConsumer<KappaTypes>::Quantities["pt_2"] = LambdaNtupleConsumer<KappaTypes>::Quantities["lep2Pt"];
	LambdaNtupleConsumer<KappaTypes>::Quantities["eta_2"] = LambdaNtupleConsumer<KappaTypes>::Quantities["lep2Eta"];
	LambdaNtupleConsumer<KappaTypes>::Quantities["phi_2"] = LambdaNtupleConsumer<KappaTypes>::Quantities["lep2Phi"];
	LambdaNtupleConsumer<KappaTypes>::Quantities["m_2"] = LambdaNtupleConsumer<KappaTypes>::Quantities["lep2Mass"];
	LambdaNtupleConsumer<KappaTypes>::Quantities["q_2"] = LambdaNtupleConsumer<KappaTypes>::Quantities["lep2Charge"];
	LambdaNtupleConsumer<KappaTypes>::Quantities["iso_2"] = LambdaNtupleConsumer<KappaTypes>::Quantities["lep2IsoOverPt"];
	LambdaNtupleConsumer<KappaTypes>::Quantities["mt_2"] = LambdaNtupleConsumer<KappaTypes>::Quantities["lep2Mt"];
	LambdaNtupleConsumer<KappaTypes>::Quantities["met"] = LambdaNtupleConsumer<KappaTypes>::Quantities["pfMetPt"];
	LambdaNtupleConsumer<KappaTypes>::Quantities["metphi"] = LambdaNtupleConsumer<KappaTypes>::Quantities["pfMetPhi"];
	LambdaNtupleConsumer<KappaTypes>::Quantities["metcov00"] = LambdaNtupleConsumer<KappaTypes>::Quantities["pfMetCov00"];
	LambdaNtupleConsumer<KappaTypes>::Quantities["metcov01"] = LambdaNtupleConsumer<KappaTypes>::Quantities["pfMetCov01"];
	LambdaNtupleConsumer<KappaTypes>::Quantities["metcov10"] = LambdaNtupleConsumer<KappaTypes>::Quantities["pfMetCov10"];
	LambdaNtupleConsumer<KappaTypes>::Quantities["metcov11"] = LambdaNtupleConsumer<KappaTypes>::Quantities["pfMetCov11"];
	LambdaNtupleConsumer<KappaTypes>::Quantities["mvamet"] = LambdaNtupleConsumer<KappaTypes>::Quantities["mvaMetPt"];
	LambdaNtupleConsumer<KappaTypes>::Quantities["mvametphi"] = LambdaNtupleConsumer<KappaTypes>::Quantities["mvaMetPhi"];
	LambdaNtupleConsumer<KappaTypes>::Quantities["mvacov00"] = LambdaNtupleConsumer<KappaTypes>::Quantities["mvaMetCov00"];
	LambdaNtupleConsumer<KappaTypes>::Quantities["mvacov01"] = LambdaNtupleConsumer<KappaTypes>::Quantities["mvaMetCov01"];
	LambdaNtupleConsumer<KappaTypes>::Quantities["mvacov10"] = LambdaNtupleConsumer<KappaTypes>::Quantities["mvaMetCov10"];
	LambdaNtupleConsumer<KappaTypes>::Quantities["mvacov11"] = LambdaNtupleConsumer<KappaTypes>::Quantities["mvaMetCov11"];
	LambdaNtupleConsumer<KappaTypes>::Quantities["jpt_1"] = LambdaNtupleConsumer<KappaTypes>::Quantities["leadingJetPt"];
	LambdaNtupleConsumer<KappaTypes>::Quantities["jeta_1"] = LambdaNtupleConsumer<KappaTypes>::Quantities["leadingJetEta"];
	LambdaNtupleConsumer<KappaTypes>::Quantities["jphi_1"] = LambdaNtupleConsumer<KappaTypes>::Quantities["leadingJetPhi"];
	LambdaNtupleConsumer<KappaTypes>::Quantities["jpt_2"] = LambdaNtupleConsumer<KappaTypes>::Quantities["trailingJetPt"];
	LambdaNtupleConsumer<KappaTypes>::Quantities["jeta_2"] = LambdaNtupleConsumer<KappaTypes>::Quantities["trailingJetEta"];
	LambdaNtupleConsumer<KappaTypes>::Quantities["jphi_2"] = LambdaNtupleConsumer<KappaTypes>::Quantities["trailingJetPhi"];
	LambdaNtupleConsumer<KappaTypes>::Quantities["mjj"] = LambdaNtupleConsumer<KappaTypes>::Quantities["diJetMass"];
	LambdaNtupleConsumer<KappaTypes>::Quantities["jdeta"] = LambdaNtupleConsumer<KappaTypes>::Quantities["diJetAbsDeltaEta"];
	LambdaNtupleConsumer<KappaTypes>::Quantities["njets"] = LambdaNtupleConsumer<KappaTypes>::Quantities["nJets"];
	LambdaNtupleConsumer<KappaTypes>::Quantities["pt_sv"] = LambdaNtupleConsumer<KappaTypes>::Quantities["diTauPt"];
	LambdaNtupleConsumer<KappaTypes>::Quantities["eta_sv"] = LambdaNtupleConsumer<KappaTypes>::Quantities["diTauEta"];
	LambdaNtupleConsumer<KappaTypes>::Quantities["phi_sv"] = LambdaNtupleConsumer<KappaTypes>::Quantities["diTauPhi"];
	LambdaNtupleConsumer<KappaTypes>::Quantities["m_sv"] = LambdaNtupleConsumer<KappaTypes>::Quantities["diTauMass"];
	
	// need to be called at last
	KappaLambdaNtupleConsumer::Init(settings);
}
