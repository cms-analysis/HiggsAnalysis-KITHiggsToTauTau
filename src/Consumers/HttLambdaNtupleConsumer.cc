
#include <Math/VectorUtil.h>

#include "Artus/Utility/interface/SafeMap.h"
#include "Artus/Utility/interface/Utility.h"
#include "Artus/Utility/interface/DefaultValues.h"
#include "Artus/KappaAnalysis/interface/KappaEnumTypes.h"
#include "Artus/KappaAnalysis/interface/KappaTypes.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/Consumers/HttLambdaNtupleConsumer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/DiJetQuantitiesProducer.h"


void HttLambdaNtupleConsumer::Init(setting_type const& settings, metadata_type& metadata)
{
	// add possible quantities for the lambda ntuples consumers

	// settings for synch ntuples
	LambdaNtupleConsumer<HttTypes>::AddUInt64Quantity("evt", [](event_type const& event, product_type const& product)
	{
		return event.m_eventInfo->nEvent;
	});

	bool bInpData = settings.GetInputIsData();
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("npu", [bInpData](event_type const& event, product_type const& product)
	{
		if (bInpData)
			return DefaultValues::UndefinedFloat;
		return static_cast<KGenEventInfo*>(event.m_eventInfo)->nPUMean;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("puweight", [](event_type const& event, product_type const& product)
	{
		return SafeMap::GetWithDefault(product.m_weights, std::string("puWeight"), 1.0);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("trigweight_1", [](event_type const& event, product_type const& product)
	{
		return SafeMap::GetWithDefault(product.m_weights, std::string("triggerWeight_1"), 1.0);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("trigweight_2", [](event_type const& event, product_type const& product)
	{
		return SafeMap::GetWithDefault(product.m_weights, std::string("triggerWeight_2"), 1.0);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("idisoweight_1", [](event_type const& event, product_type const& product)
	{
		return SafeMap::GetWithDefault(product.m_weights, std::string("identificationWeight_1"), 1.0);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("idisoweight_2", [](event_type const& event, product_type const& product)
	{
		return SafeMap::GetWithDefault(product.m_weights, std::string("identificationWeight_2"), 1.0);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("weight", [settings](event_type const& event, product_type const& product)
	{
		return SafeMap::GetWithDefault(product.m_weights, settings.GetEventWeight(), 1.0);
	});

	LambdaNtupleConsumer<HttTypes>::AddIntQuantity("nDiLeptonVetoPairsOS", [](event_type const& event, product_type const& product)
	{
		return product.m_nDiElectronVetoPairsOS + product.m_nDiMuonVetoPairsOS;
	});
	LambdaNtupleConsumer<HttTypes>::AddIntQuantity("nDiLeptonVetoPairsSS", [](event_type const& event, product_type const& product)
	{
		return product.m_nDiElectronVetoPairsSS + product.m_nDiMuonVetoPairsSS;
	});
	LambdaNtupleConsumer<HttTypes>::AddIntQuantity("dilepton_veto", [](event_type const& event, product_type const& product)
	{
		return ((product.m_nDiElectronVetoPairsOS + product.m_nDiMuonVetoPairsOS) >= 1) ? 1 : 0;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("mt_tot", [](event_type const& event, product_type const& product)
	{
		return sqrt(pow(SafeMap::Get(LambdaNtupleConsumer<HttTypes>::GetFloatQuantities(),std::string("mt_tt"))(event,product),2)+pow(SafeMap::Get(LambdaNtupleConsumer<HttTypes>::GetFloatQuantities(),std::string("lep1MetMt"))(event,product),2)+pow(SafeMap::Get(LambdaNtupleConsumer<HttTypes>::GetFloatQuantities(),std::string("lep2MetMt"))(event,product),2));
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("m_vis", LambdaNtupleConsumer<HttTypes>::GetFloatQuantities()["diLepMass"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("mvis", LambdaNtupleConsumer<HttTypes>::GetFloatQuantities()["diLepMass"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("ptvis", LambdaNtupleConsumer<HttTypes>::GetFloatQuantities()["diLepPt"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("H_pt", LambdaNtupleConsumer<HttTypes>::GetFloatQuantities()["diLepMetPt"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("H_mass", LambdaNtupleConsumer<HttTypes>::GetFloatQuantities()["diLepMetMass"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("pt_tt", LambdaNtupleConsumer<HttTypes>::GetFloatQuantities()["diLepMetPt"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("pt_1", LambdaNtupleConsumer<HttTypes>::GetFloatQuantities()["lep1Pt"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("eta_1", LambdaNtupleConsumer<HttTypes>::GetFloatQuantities()["lep1Eta"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("phi_1", LambdaNtupleConsumer<HttTypes>::GetFloatQuantities()["lep1Phi"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("m_1", LambdaNtupleConsumer<HttTypes>::GetFloatQuantities()["lep1Mass"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("q_1", LambdaNtupleConsumer<HttTypes>::GetFloatQuantities()["lep1Charge"]);

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("dZ_1", LambdaNtupleConsumer<HttTypes>::GetFloatQuantities()["lep1Dz"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("d0_1", LambdaNtupleConsumer<HttTypes>::GetFloatQuantities()["lep1D0"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("errDZ_1", LambdaNtupleConsumer<HttTypes>::GetFloatQuantities()["lep1ErrDz"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("errD0_1", LambdaNtupleConsumer<HttTypes>::GetFloatQuantities()["lep1ErrD0"]);

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("iso_1", LambdaNtupleConsumer<HttTypes>::GetFloatQuantities()["lep1IsoOverPt"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("mt_1", LambdaNtupleConsumer<HttTypes>::GetFloatQuantities()["lep1MetMt"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("pt_2", LambdaNtupleConsumer<HttTypes>::GetFloatQuantities()["lep2Pt"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("eta_2", LambdaNtupleConsumer<HttTypes>::GetFloatQuantities()["lep2Eta"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("phi_2", LambdaNtupleConsumer<HttTypes>::GetFloatQuantities()["lep2Phi"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("m_2", LambdaNtupleConsumer<HttTypes>::GetFloatQuantities()["lep2Mass"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("q_2", LambdaNtupleConsumer<HttTypes>::GetFloatQuantities()["lep2Charge"]);

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("dZ_2", LambdaNtupleConsumer<HttTypes>::GetFloatQuantities()["lep2Dz"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("d0_2", LambdaNtupleConsumer<HttTypes>::GetFloatQuantities()["lep2D0"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("errDZ_2", LambdaNtupleConsumer<HttTypes>::GetFloatQuantities()["lep2ErrDz"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("errD0_2", LambdaNtupleConsumer<HttTypes>::GetFloatQuantities()["lep2ErrD0"]);

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("iso_2", LambdaNtupleConsumer<HttTypes>::GetFloatQuantities()["lep2IsoOverPt"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("mt_2", LambdaNtupleConsumer<HttTypes>::GetFloatQuantities()["lep2MetMt"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("met", LambdaNtupleConsumer<HttTypes>::GetFloatQuantities()["metPt"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("metphi", LambdaNtupleConsumer<HttTypes>::GetFloatQuantities()["metPhi"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("metcov00", LambdaNtupleConsumer<HttTypes>::GetFloatQuantities()["metCov00"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("metcov01", LambdaNtupleConsumer<HttTypes>::GetFloatQuantities()["metCov01"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("metcov10", LambdaNtupleConsumer<HttTypes>::GetFloatQuantities()["metCov10"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("metcov11", LambdaNtupleConsumer<HttTypes>::GetFloatQuantities()["metCov11"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("pfmet", LambdaNtupleConsumer<HttTypes>::GetFloatQuantities()["pfMetPt"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("pfmetphi", LambdaNtupleConsumer<HttTypes>::GetFloatQuantities()["pfMetPhi"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("pfmetcov00", LambdaNtupleConsumer<HttTypes>::GetFloatQuantities()["pfMetCov00"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("pfmetcov01", LambdaNtupleConsumer<HttTypes>::GetFloatQuantities()["pfMetCov01"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("pfmetcov10", LambdaNtupleConsumer<HttTypes>::GetFloatQuantities()["pfMetCov10"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("pfmetcov11", LambdaNtupleConsumer<HttTypes>::GetFloatQuantities()["pfMetCov11"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("mvamet", LambdaNtupleConsumer<HttTypes>::GetFloatQuantities()["mvaMetPt"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("mvametphi", LambdaNtupleConsumer<HttTypes>::GetFloatQuantities()["mvaMetPhi"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("mvacov00", LambdaNtupleConsumer<HttTypes>::GetFloatQuantities()["mvaMetCov00"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("mvacov01", LambdaNtupleConsumer<HttTypes>::GetFloatQuantities()["mvaMetCov01"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("mvacov10", LambdaNtupleConsumer<HttTypes>::GetFloatQuantities()["mvaMetCov10"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("mvacov11", LambdaNtupleConsumer<HttTypes>::GetFloatQuantities()["mvaMetCov11"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("pzetavis", LambdaNtupleConsumer<HttTypes>::GetFloatQuantities()["pZetaVis"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("pzetamiss", LambdaNtupleConsumer<HttTypes>::GetFloatQuantities()["pZetaMiss"]);
	
	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity("jlv_1", LambdaNtupleConsumer<HttTypes>::GetRMFLVQuantities()["leadingJetLV"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("jpt_1", LambdaNtupleConsumer<HttTypes>::GetFloatQuantities()["leadingJetPt"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("jeta_1", LambdaNtupleConsumer<HttTypes>::GetFloatQuantities()["leadingJetEta"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("jphi_1", LambdaNtupleConsumer<HttTypes>::GetFloatQuantities()["leadingJetPhi"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("jm_1", LambdaNtupleConsumer<HttTypes>::GetFloatQuantities()["leadingJetMass"]);

	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity("jlv_2", LambdaNtupleConsumer<HttTypes>::GetRMFLVQuantities()["trailingJetLV"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("jpt_2", LambdaNtupleConsumer<HttTypes>::GetFloatQuantities()["trailingJetPt"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("jeta_2", LambdaNtupleConsumer<HttTypes>::GetFloatQuantities()["trailingJetEta"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("jphi_2", LambdaNtupleConsumer<HttTypes>::GetFloatQuantities()["trailingJetPhi"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("jm_2", LambdaNtupleConsumer<HttTypes>::GetFloatQuantities()["trailingJetMass"]);

	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity("jlv_3", LambdaNtupleConsumer<HttTypes>::GetRMFLVQuantities()["thirdJetLV"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("jpt_3", LambdaNtupleConsumer<HttTypes>::GetFloatQuantities()["thirdJetPt"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("jeta_3", LambdaNtupleConsumer<HttTypes>::GetFloatQuantities()["thirdJetEta"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("jphi_3", LambdaNtupleConsumer<HttTypes>::GetFloatQuantities()["thirdJetPhi"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("jm_3", LambdaNtupleConsumer<HttTypes>::GetFloatQuantities()["thirdJetMass"]);
	
	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity("jlv_4", LambdaNtupleConsumer<HttTypes>::GetRMFLVQuantities()["fourthJetLV"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("jpt_4", LambdaNtupleConsumer<HttTypes>::GetFloatQuantities()["fourthJetPt"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("jeta_4", LambdaNtupleConsumer<HttTypes>::GetFloatQuantities()["fourthJetEta"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("jphi_4", LambdaNtupleConsumer<HttTypes>::GetFloatQuantities()["fourthJetPhi"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("jm_4", LambdaNtupleConsumer<HttTypes>::GetFloatQuantities()["fourthJetMass"]);
	
	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity("jlv_5", LambdaNtupleConsumer<HttTypes>::GetRMFLVQuantities()["fifthJetLV"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("jpt_5", LambdaNtupleConsumer<HttTypes>::GetFloatQuantities()["fifthJetPt"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("jeta_5", LambdaNtupleConsumer<HttTypes>::GetFloatQuantities()["fifthJetEta"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("jphi_5", LambdaNtupleConsumer<HttTypes>::GetFloatQuantities()["fifthJetPhi"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("jm_5", LambdaNtupleConsumer<HttTypes>::GetFloatQuantities()["fifthJetMass"]);
	
	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity("jlv_6", LambdaNtupleConsumer<HttTypes>::GetRMFLVQuantities()["sixthJetLV"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("jpt_6", LambdaNtupleConsumer<HttTypes>::GetFloatQuantities()["sixthJetPt"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("jeta_6", LambdaNtupleConsumer<HttTypes>::GetFloatQuantities()["sixthJetEta"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("jphi_6", LambdaNtupleConsumer<HttTypes>::GetFloatQuantities()["sixthJetPhi"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("jm_6", LambdaNtupleConsumer<HttTypes>::GetFloatQuantities()["sixthJetMass"]);
	
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("jmva_1", LambdaNtupleConsumer<HttTypes>::GetFloatQuantities()["leadingJetPuID"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("jcsv_1", LambdaNtupleConsumer<HttTypes>::GetFloatQuantities()["leadingJetCSV"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("bpt_1", LambdaNtupleConsumer<HttTypes>::GetFloatQuantities()["bJetPt"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("beta_1", LambdaNtupleConsumer<HttTypes>::GetFloatQuantities()["bJetEta"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("bphi_1", LambdaNtupleConsumer<HttTypes>::GetFloatQuantities()["bJetPhi"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("bmva_1", LambdaNtupleConsumer<HttTypes>::GetFloatQuantities()["leadingBJetPuID"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("bcsv_1", LambdaNtupleConsumer<HttTypes>::GetFloatQuantities()["leadingBJetCSV"]);
	
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("jmva_2", LambdaNtupleConsumer<HttTypes>::GetFloatQuantities()["trailingJetPuID"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("jcsv_2", LambdaNtupleConsumer<HttTypes>::GetFloatQuantities()["trailingJetCSV"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("bpt_2", LambdaNtupleConsumer<HttTypes>::GetFloatQuantities()["bJet2Pt"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("beta_2", LambdaNtupleConsumer<HttTypes>::GetFloatQuantities()["bJet2Eta"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("bphi_2", LambdaNtupleConsumer<HttTypes>::GetFloatQuantities()["bJet2Phi"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("bmva_2", LambdaNtupleConsumer<HttTypes>::GetFloatQuantities()["trailingBJetPuID"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("bcsv_2", LambdaNtupleConsumer<HttTypes>::GetFloatQuantities()["trailingBJetCSV"]);
	
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("jcsv_3", LambdaNtupleConsumer<HttTypes>::GetFloatQuantities()["thirdJetCSV"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("jcsv_4", LambdaNtupleConsumer<HttTypes>::GetFloatQuantities()["fourthJetCSV"]);

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("mjj", LambdaNtupleConsumer<HttTypes>::GetFloatQuantities()["diJetMass"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("jdeta", LambdaNtupleConsumer<HttTypes>::GetFloatQuantities()["diJetAbsDeltaEta"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("jdphi", LambdaNtupleConsumer<HttTypes>::GetFloatQuantities()["diJetDeltaPhi"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("dijetpt", LambdaNtupleConsumer<HttTypes>::GetFloatQuantities()["diJetPt"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("dijetphi", LambdaNtupleConsumer<HttTypes>::GetFloatQuantities()["diJetPhi"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("hdijetphi", LambdaNtupleConsumer<HttTypes>::GetFloatQuantities()["diJetdiLepPhi"]);

	LambdaNtupleConsumer<HttTypes>::AddIntQuantity("njets", LambdaNtupleConsumer<HttTypes>::GetIntQuantities()["nJets30"]);
	LambdaNtupleConsumer<HttTypes>::AddIntQuantity("njetspt30", LambdaNtupleConsumer<HttTypes>::GetIntQuantities()["nJets30"]);
	LambdaNtupleConsumer<HttTypes>::AddIntQuantity("njetspt20", LambdaNtupleConsumer<HttTypes>::GetIntQuantities()["nJets20"]);
	LambdaNtupleConsumer<HttTypes>::AddIntQuantity("njetspt20eta2p4", LambdaNtupleConsumer<HttTypes>::GetIntQuantities()["nJets20Eta2p4"]);
	LambdaNtupleConsumer<HttTypes>::AddIntQuantity("nbtag", LambdaNtupleConsumer<HttTypes>::GetIntQuantities()["nBJets20"]);
	LambdaNtupleConsumer<HttTypes>::AddIntQuantity("njetingap", LambdaNtupleConsumer<HttTypes>::GetIntQuantities()["nCentralJets30"]);
	LambdaNtupleConsumer<HttTypes>::AddIntQuantity("njetingap30", LambdaNtupleConsumer<HttTypes>::GetIntQuantities()["nCentralJets30"]);
	LambdaNtupleConsumer<HttTypes>::AddIntQuantity("njetingap20", LambdaNtupleConsumer<HttTypes>::GetIntQuantities()["nCentralJets20"]);

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("pt_sv", LambdaNtupleConsumer<HttTypes>::GetFloatQuantities()["svfitPt"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("eta_sv", LambdaNtupleConsumer<HttTypes>::GetFloatQuantities()["svfitEta"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("phi_sv", LambdaNtupleConsumer<HttTypes>::GetFloatQuantities()["svfitPhi"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("m_sv", LambdaNtupleConsumer<HttTypes>::GetFloatQuantities()["svfitMass"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("mt_sv", LambdaNtupleConsumer<HttTypes>::GetFloatQuantities()["svfitTransverseMass"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("met_sv", LambdaNtupleConsumer<HttTypes>::GetFloatQuantities()["svfitMet"]);

	LambdaNtupleConsumer<HttTypes>::AddIntQuantity("npartons", [](event_type const& event, product_type const& product)
	{
		return event.m_genEventInfo ? event.m_genEventInfo->lheNOutPartons : DefaultValues::UndefinedInt;
	});
	LambdaNtupleConsumer<HttTypes>::AddIntQuantity("NUP", LambdaNtupleConsumer<HttTypes>::GetIntQuantities()["npartons"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("genbosonmass", [](event_type const& event, product_type const& product)
	{
		return LambdaNtupleConsumer<HttTypes>::GetFloatQuantities().count("genBosonMass") >= 1 ? LambdaNtupleConsumer<HttTypes>::GetFloatQuantities()["genBosonMass"](event, product) : DefaultValues::UndefinedFloat;
	});


	LambdaNtupleConsumer<HttTypes>::AddIntQuantity("isFake", [](event_type const& event, product_type const& product)
	{
		return DefaultValues::UndefinedInt;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("visjeteta", [](event_type const& event, product_type const& product)
	{
		return DefaultValues::UndefinedFloat;
	});
// 	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("ptvis", [](event_type const& event, product_type const& product)
// 	{
// 		return DefaultValues::UndefinedFloat;
// 	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("jrawf_1", [](event_type const& event, product_type const& product)
	{
		return DefaultValues::UndefinedFloat;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("jrawf_2", [](event_type const& event, product_type const& product)
	{
		return DefaultValues::UndefinedFloat;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("jpfid_1", [](event_type const& event, product_type const& product)
	{
		return DefaultValues::UndefinedFloat;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("jpfid_2", [](event_type const& event, product_type const& product)
	{
		return DefaultValues::UndefinedFloat;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("jpuid_1", [](event_type const& event, product_type const& product)
	{
		return DefaultValues::UndefinedFloat;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("jpuid_2", [](event_type const& event, product_type const& product)
	{
		return DefaultValues::UndefinedFloat;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("brawf_1", [](event_type const& event, product_type const& product)
	{
		return DefaultValues::UndefinedFloat;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("bpfid_1", [](event_type const& event, product_type const& product)
	{
		return DefaultValues::UndefinedFloat;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("bpuid_1", [](event_type const& event, product_type const& product)
	{
		return DefaultValues::UndefinedFloat;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("brawf_2", [](event_type const& event, product_type const& product)
	{
		return DefaultValues::UndefinedFloat;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("bpfid_2", [](event_type const& event, product_type const& product)
	{
		return DefaultValues::UndefinedFloat;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("bpuid_2", [](event_type const& event, product_type const& product)
	{
		return DefaultValues::UndefinedFloat;
	});

	// need to be called at last
	KappaLambdaNtupleConsumer::Init(settings, metadata);
}
