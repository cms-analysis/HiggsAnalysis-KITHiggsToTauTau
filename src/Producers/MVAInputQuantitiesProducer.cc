#include "Artus/Consumer/interface/LambdaNtupleConsumer.h"
#include "Artus/Utility/interface/DefaultValues.h"
#include <TMath.h>
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/MVAInputQuantitiesProducer.h"
#include <assert.h>

void MVAInputQuantitiesProducer::Init(setting_type const& settings, metadata_type& metadata)
{
	ProducerBase<HttTypes>::Init(settings, metadata);
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
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("dmjj", [](event_type const& event, product_type const& product) {
		return product.m_diJetDeltaMass;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("diJetSymEta_1", [](event_type const& event, product_type const& product) {
		return product.m_validJets.size() >= 1 ? (std::abs(product.m_validJets[0]->p4.Eta())) : -1;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("diJetSymEta_2", [](event_type const& event, product_type const& product) {
		return product.m_diJetSymDeltaEta;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("diJetDeltaR", [](event_type const& event, product_type const& product) {
		return product.m_diJetDeltaR;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("diJetAbsDeltaPhi", [](event_type const& event, product_type const& product) {
		return product.m_diJetSystemAvailable ? std::abs(ROOT::Math::VectorUtil::DeltaPhi(product.m_validJets[0]->p4, product.m_validJets[1]->p4)) : -1;
	});
	//csv score ordered variables
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("diCJetDeltam", [](event_type const& event, product_type const& product) {
		return product.m_diCJetDeltaMass;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("diCJetSymEta_1", [](event_type const& event, product_type const& product) {
		return product.m_diCJetSymEta1;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("diCJetSymEta_2", [](event_type const& event, product_type const& product) {
		return product.m_diCJetSymDeltaEta;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("diCJetDeltaR", [](event_type const& event, product_type const& product) {
		return product.m_diCJetDeltaR;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("diCJetAbsDeltaPhi", [](event_type const& event, product_type const& product) {
		return product.m_diCJetAbsDeltaPhi;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("jccsv_1", [](event_type const& event, product_type const& product) {
		return product.m_jccsv1;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("jccsv_2", [](event_type const& event, product_type const& product) {
		return product.m_jccsv2;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("jccsv_3", [](event_type const& event, product_type const& product) {
		return product.m_jccsv3;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("jccsv_4", [](event_type const& event, product_type const& product) {
		return product.m_jccsv4;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("jcpt_1", [](event_type const& event, product_type const& product) {
		return product.m_csv1JetPt;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("jcpt_2", [](event_type const& event, product_type const& product) {
		return product.m_csv2JetPt;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("jcm_1", [](event_type const& event, product_type const& product) {
		return product.m_csv1JetMass;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("jcm_2", [](event_type const& event, product_type const& product) {
		return product.m_csv2JetMass;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("diCJetm", [](event_type const& event, product_type const& product) {
		return product.m_diCJetMass;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("pVecSumCSVJets", [](event_type const& event, product_type const& product) {
		return product.m_pVecSumCSVJets;
	});
}

void MVAInputQuantitiesProducer::Produce(event_type const& event, product_type& product,
                                      setting_type const& settings, metadata_type const& metadata) const
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
        //find jets with highest csv score
        int csvleading = -1;
        int csvtrailing = -1;
	int csv3 = -1;
	int csv4 = -1;
        switch (int(product.m_validJets.size())){
		case 0:
			break;
		case 1:
			csvleading = 0;
			break;
		case 2:
			if(static_cast<KJet*>(product.m_validJets.at(1))->getTag(settings.GetBTaggedJetCombinedSecondaryVertexName(), event.m_jetMetadata) > static_cast<KJet*>(product.m_validJets.at(0))->getTag(settings.GetBTaggedJetCombinedSecondaryVertexName(), event.m_jetMetadata)){
				csvleading = 1;
				csvtrailing = 0;
			}
			else{
				csvleading = 0;
				csvtrailing = 1;
			}
			break;
		default:
			double csv=-1000;
			for(int i=0; i < int(product.m_validJets.size()); i++){
				double probecsv = static_cast<KJet*>(product.m_validJets.at(i))->getTag(settings.GetBTaggedJetCombinedSecondaryVertexName(), event.m_jetMetadata);
				if (probecsv > csv){
					csvleading = i;
					csv = probecsv;
				}
			}
			csv=-1000;
			for(int i=0; i < int(product.m_validJets.size()); i++){
				double probecsv = static_cast<KJet*>(product.m_validJets.at(i))->getTag(settings.GetBTaggedJetCombinedSecondaryVertexName(), event.m_jetMetadata);
				if (i != csvleading && probecsv > csv){
					csvtrailing = i;
					csv = probecsv;
				}
			}
			csv=-1000;
			for(int i=0; i < int(product.m_validJets.size()); i++){
				double probecsv = static_cast<KJet*>(product.m_validJets.at(i))->getTag(settings.GetBTaggedJetCombinedSecondaryVertexName(), event.m_jetMetadata);
				if (i != csvleading && i != csvtrailing && probecsv > csv){
					csv3 = i;
					csv = probecsv;
				}
			}
			csv=-1000;
			for(int i=0; i < int(product.m_validJets.size()); i++){
				double probecsv = static_cast<KJet*>(product.m_validJets.at(i))->getTag(settings.GetBTaggedJetCombinedSecondaryVertexName(), event.m_jetMetadata);
				if (i != csvleading && i != csvtrailing && i != csv3 && probecsv > csv && csv4 == -1){
					csv4 = i;
					csv = probecsv;
				}
			}
	}
	assert(csvleading >= 0 or int(product.m_validJets.size())<1);
	assert(csvtrailing >= 0 or int(product.m_validJets.size())<2);
	assert(csv3 >= 0 or int(product.m_validJets.size())<3);
	assert(csv4 >= 0 or int(product.m_validJets.size())<4);
                
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
		double cjet1_eta = product.m_validJets[csvleading]->p4.Eta();
		double cjet2_eta = product.m_validJets[csvtrailing]->p4.Eta();
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
		//other diJetSystem variables
		double jm_1 = product.m_validJets[0]->p4.mass();
		double jm_2 = product.m_validJets[1]->p4.mass();
		product.m_diJetDeltaMass = jm_1-jm_2;
		product.m_diJetSymDeltaEta = (jet2_eta-jet1_eta)*(TMath::Sign(1.0, jet1_eta));
		product.m_diJetDeltaR = ROOT::Math::VectorUtil::DeltaR(product.m_validJets[0]->p4, product.m_validJets[1]->p4);
		//csv score ordered variables
		product.m_diCJetDeltaMass = product.m_validJets[csvleading]->p4.mass()-product.m_validJets[csvtrailing]->p4.mass();
		product.m_diCJetSymDeltaEta = (cjet2_eta-cjet1_eta)*(TMath::Sign(1.0, cjet1_eta));
		product.m_diCJetDeltaR = ROOT::Math::VectorUtil::DeltaR(product.m_validJets[csvleading]->p4, product.m_validJets[csvtrailing]->p4);
		product.m_diCJetAbsDeltaPhi = std::abs(ROOT::Math::VectorUtil::DeltaPhi(product.m_validJets[csvleading]->p4, product.m_validJets[csvtrailing]->p4));
		product.m_diCJetMass = (product.m_validJets[csvleading]->p4 + product.m_validJets[csvtrailing]->p4).mass();
		product.m_pVecSumCSVJets = (product.m_met.p4 + product.m_diLeptonSystem + product.m_validJets[csvleading]->p4 + product.m_validJets[csvtrailing]->p4).M();
	}
	if (KappaProduct::GetNJetsAbovePtThreshold(product.m_validJets, 30.0) >=1 and product.m_svfitResults.fittedHiggsLV)
	{
		double jet1_eta = product.m_validJets[0]->p4.Eta();
		double jet1_phi = product.m_validJets[0]->p4.Phi();
		double svfit_eta = product.m_svfitResults.fittedHiggsLV->Eta();
		double svfit_phi = product.m_svfitResults.fittedHiggsLV->Phi();
// 		double svfit_pt = product.m_svfitResults.fittedHiggsLV->Pt();
		product.m_diLepJet1DeltaR = TMath::Sqrt((svfit_eta-jet1_eta)*(svfit_eta-jet1_eta)+(svfit_phi-jet1_phi)*(svfit_phi-jet1_phi));
	}
	if (product.m_validJets.size() >= 1)
	{
		product.m_diCJetSymEta1 = std::abs(product.m_validJets[csvleading]->p4.Eta());
		product.m_jccsv1 = static_cast<KJet*>(product.m_validJets.at(csvleading))->getTag(settings.GetBTaggedJetCombinedSecondaryVertexName(), event.m_jetMetadata);
		product.m_csv1JetPt = product.m_validJets[csvleading]->p4.Pt();
		product.m_csv1JetMass = product.m_validJets[csvleading]->p4.mass();
	}
	if (product.m_validJets.size() >= 2)
	{
		product.m_jccsv2 = static_cast<KJet*>(product.m_validJets.at(csvtrailing))->getTag(settings.GetBTaggedJetCombinedSecondaryVertexName(), event.m_jetMetadata);
		product.m_csv2JetPt = product.m_validJets[csvtrailing]->p4.Pt();
		product.m_csv2JetMass = product.m_validJets[csvtrailing]->p4.mass();
	}
	if (product.m_validJets.size() >= 3)
	{
		product.m_jccsv3 = static_cast<KJet*>(product.m_validJets.at(csv3))->getTag(settings.GetBTaggedJetCombinedSecondaryVertexName(), event.m_jetMetadata);
	}
	if (product.m_validJets.size() >= 4)
	{
		product.m_jccsv4 = static_cast<KJet*>(product.m_validJets.at(csv4))->getTag(settings.GetBTaggedJetCombinedSecondaryVertexName(), event.m_jetMetadata);
	}
	if (product.m_svfitResults.fittedHiggsLV)
	{
		double svfit_eta = product.m_svfitResults.fittedHiggsLV->Eta();
// 		double svfit_phi = product.m_svfitResults.fittedHiggsLV->Phi();
		double svfit_pt = product.m_svfitResults.fittedHiggsLV->Pt();
		product.m_diLepBoost = svfit_pt*TMath::CosH(svfit_eta);
	}

}
