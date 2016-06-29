#include "Artus/Consumer/interface/LambdaNtupleConsumer.h"
#include "Artus/Utility/interface/DefaultValues.h"
#include <TMath.h>
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/MVAInputQuantitiesProducer.h"


void MVAInputQuantitiesProducer::Init(setting_type const& settings)
{
	ProducerBase<HttTypes>::Init(settings);
	LambdaNtupleConsumer<HttTypes>::AddIntQuantity("TrainingSelectionValue", [](event_type const& event, product_type const& product) {
		return (event.m_eventInfo->nEvent)%100;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("pVecSum", [](event_type const& event, product_type const& product) {
		return product.m_pVecSum;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("pScalSum", [](event_type const& event, product_type const& product) {
		return product.m_pScalSum;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("min_ll_jet_eta", [](event_type const& event, product_type const& product) {
		return product.m_MinLLJetEta;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("abs_min_ll_jet_eta", [](event_type const& event, product_type const& product) {
		return std::abs(product.m_MinLLJetEta);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("lep1_centrality", [](event_type const& event, product_type const& product) {
		return product.m_Lep1Centrality;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("lep2_centrality", [](event_type const& event, product_type const& product) {
		return product.m_Lep2Centrality;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("product_lep_centrality", [](event_type const& event, product_type const& product) {
		return KappaProduct::GetNJetsAbovePtThreshold(product.m_validJets, 30.0) >=1 ? (product.m_Lep1Centrality*product.m_Lep2Centrality) : -1;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("diLep_centrality", [](event_type const& event, product_type const& product) {
		return std::abs(product.m_DiLepCentrality);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("diLep_diJet_deltaR", [](event_type const& event, product_type const& product) {
		return std::abs(product.m_DiLepDiJetDeltaR);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("diLepBoost", [](event_type const& event, product_type const& product) {
		return std::abs(product.m_diLepBoost);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("diLepJet1DeltaR", [](event_type const& event, product_type const& product) {
		return std::abs(product.m_diLepJet1DeltaR);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("diLepDeltaR", [](event_type const& event, product_type const& product) {
		return std::abs(product.m_diLepDeltaR);
	});

}

void MVAInputQuantitiesProducer::Produce(event_type const& event, product_type& product,
                                      setting_type const& settings) const
{   //tsValue production
//     int evt_number = event.m_eventInfo->nEvent, lumi = event.m_eventInfo->nLumi, rndm = 0;
//     unsigned char *evt_char = reinterpret_cast<unsigned char *>(&evt_number);
//     unsigned char *lumi_char = reinterpret_cast<unsigned char *>(&lumi);
//     unsigned char *random_selector = reinterpret_cast<unsigned char *>(&rndm);
//     *random_selector = *evt_char ^ *lumi_char;
// //     rndm = evt_number ^ lumi;
//     product.tsValue = rndm%100;
	//pVecSum production vectorial sum of missing E_t DiLepton und DiJet
	product.m_pVecSum = (product.m_met.p4 + product.m_diLeptonSystem + product.m_diJetSystem).M();
	//pScalSum production scalar sum of missing E_t DiLepton und DiJet
	product.m_pScalSum = (product.m_met.p4).M() + product.m_diLeptonSystem.M() + product.m_diJetSystem.M();
	double lep1_phi = product.m_flavourOrderedLeptons[0]->p4.Phi();
	double lep2_phi = product.m_flavourOrderedLeptons[1]->p4.Phi();
	double lep1_eta = product.m_flavourOrderedLeptons[0]->p4.Eta();
	double lep2_eta = product.m_flavourOrderedLeptons[1]->p4.Eta();
	product.m_diLepDeltaR = TMath::Sqrt((lep1_phi-lep2_phi)*(lep1_phi-lep2_phi)+(lep1_eta-lep2_eta)*(lep1_eta-lep2_eta));
//    if (KappaProduct::GetNJetsAbovePtThreshold(product.m_validJets, 20.0) >= 1)
//     {
//         product.m_MinLLJetEta = product.m_diLeptonSystem.Eta() + product.m_validJets[0]->p4.Eta();
//     }
//     else
//     {
//         product.m_MinLLJetEta = product.m_diLeptonSystem.Eta();
//     }
    //min_ll_jet_eta production
	if(product.m_diJetSystemAvailable)
	{
		double jet1_eta = product.m_validJets[0]->p4.Eta();
		double jet2_eta = product.m_validJets[1]->p4.Eta();
		product.m_MinLLJetEta = std::min(product.m_diLeptonSystem.Eta() + jet1_eta, product.m_diLeptonSystem.Eta() + jet2_eta);
		product.m_DiLepDiJetDeltaR = ROOT::Math::VectorUtil::DeltaR(product.m_diLeptonSystem, product.m_diJetSystem);
		//object_centrality production
		double eta = 0.0;
		eta = product.m_flavourOrderedLeptons[0]->p4.Eta();
		product.m_Lep1Centrality = TMath::Exp(-4.0/(jet1_eta-jet2_eta)/(jet1_eta-jet2_eta)*(eta-(jet1_eta+jet2_eta)/2.0)*(eta-(jet1_eta+jet2_eta)/2.0));
		eta = product.m_flavourOrderedLeptons[1]->p4.Eta();
		product.m_Lep2Centrality = TMath::Exp(-4.0/(jet1_eta-jet2_eta)/(jet1_eta-jet2_eta)*(eta-(jet1_eta+jet2_eta)/2.0)*(eta-(jet1_eta+jet2_eta)/2.0));
		eta = product.m_diLeptonSystem.Eta();
		product.m_DiLepCentrality = TMath::Exp(-4.0/(jet1_eta-jet2_eta)/(jet1_eta-jet2_eta)*(eta-(jet1_eta+jet2_eta)/2.0)*(eta-(jet1_eta+jet2_eta)/2.0));
	}
	if (KappaProduct::GetNJetsAbovePtThreshold(product.m_validJets, 30.0) >=1 and product.m_svfitResults.momentum)
	{
		double jet1_eta = product.m_validJets[0]->p4.Eta();
		double jet1_phi = product.m_validJets[0]->p4.Phi();
		double svfit_eta = product.m_svfitResults.momentum->Eta();
		double svfit_phi = product.m_svfitResults.momentum->Phi();
// 		double svfit_pt = product.m_svfitResults.momentum->Pt();
		product.m_diLepJet1DeltaR = TMath::Sqrt((svfit_eta-jet1_eta)*(svfit_eta-jet1_eta)+(svfit_phi-jet1_phi)*(svfit_phi-jet1_phi));
	}
	if (product.m_svfitResults.momentum)
	{
		double svfit_eta = product.m_svfitResults.momentum->Eta();
// 		double svfit_phi = product.m_svfitResults.momentum->Phi();
		double svfit_pt = product.m_svfitResults.momentum->Pt();
		product.m_diLepBoost = svfit_pt*TMath::CosH(svfit_eta);
	}

}
