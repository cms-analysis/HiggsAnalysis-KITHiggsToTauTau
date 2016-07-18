
#include <Math/VectorUtil.h>

#include "Artus/Utility/interface/SafeMap.h"
#include "Artus/Utility/interface/Utility.h"
#include "Artus/Utility/interface/DefaultValues.h"
#include "Artus/KappaAnalysis/interface/KappaEnumTypes.h"
#include "Artus/KappaAnalysis/interface/KappaTypes.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/Consumers/HttLambdaNtupleConsumer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/DiJetQuantitiesProducer.h"


void HttLambdaNtupleConsumer::Init(setting_type const& settings)
{
	// add possible quantities for the lambda ntuples consumers

	// settings for synch ntuples
	LambdaNtupleConsumer<KappaTypes>::AddUInt64Quantity("evt", [](KappaEvent const& event, KappaProduct const& product)
	{
		return event.m_eventInfo->nEvent;
	});

	bool bInpData = settings.GetInputIsData();
	LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("npu", [bInpData](KappaEvent const& event, KappaProduct const& product)
	{
		if (bInpData)
			return DefaultValues::UndefinedFloat;
		return static_cast<KGenEventInfo*>(event.m_eventInfo)->nPUMean;
	});
	LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("puweight", [](KappaEvent const& event, KappaProduct const& product)
	{
		return SafeMap::GetWithDefault(product.m_weights, std::string("puWeight"), 1.0);
	});
	LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("trigweight_1", [](KappaEvent const& event, KappaProduct const& product)
	{
		return SafeMap::GetWithDefault(product.m_weights, std::string("triggerWeight_1"), 1.0);
	});
	LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("trigweight_2", [](KappaEvent const& event, KappaProduct const& product)
	{
		return SafeMap::GetWithDefault(product.m_weights, std::string("triggerWeight_2"), 1.0);
	});
	LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("idisoweight_1", [](KappaEvent const& event, KappaProduct const& product)
	{
		return SafeMap::GetWithDefault(product.m_weights, std::string("identificationWeight_1"), 1.0);
	});
	LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("idisoweight_2", [](KappaEvent const& event, KappaProduct const& product)
	{
		return SafeMap::GetWithDefault(product.m_weights, std::string("identificationWeight_2"), 1.0);
	});
	LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("weight", [settings](KappaEvent const& event, KappaProduct const& product)
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
		return sqrt(pow(SafeMap::Get(LambdaNtupleConsumer<KappaTypes>::GetFloatQuantities(),std::string("mt_tt"))(event,product),2)+pow(SafeMap::Get(LambdaNtupleConsumer<KappaTypes>::GetFloatQuantities(),std::string("lep1MetMt"))(event,product),2)+pow(SafeMap::Get(LambdaNtupleConsumer<KappaTypes>::GetFloatQuantities(),std::string("lep2MetMt"))(event,product),2));
	});

	LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("m_vis", LambdaNtupleConsumer<KappaTypes>::GetFloatQuantities()["diLepMass"]);
	LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("mvis", LambdaNtupleConsumer<KappaTypes>::GetFloatQuantities()["diLepMass"]);
	LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("ptvis", LambdaNtupleConsumer<KappaTypes>::GetFloatQuantities()["diLepPt"]);
	LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("H_pt", LambdaNtupleConsumer<KappaTypes>::GetFloatQuantities()["diLepMetPt"]);
	LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("H_mass", LambdaNtupleConsumer<KappaTypes>::GetFloatQuantities()["diLepMetMass"]);
	LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("pt_tt", LambdaNtupleConsumer<KappaTypes>::GetFloatQuantities()["diLepMetPt"]);
	LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("pt_1", LambdaNtupleConsumer<KappaTypes>::GetFloatQuantities()["lep1Pt"]);
	LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("eta_1", LambdaNtupleConsumer<KappaTypes>::GetFloatQuantities()["lep1Eta"]);
	LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("phi_1", LambdaNtupleConsumer<KappaTypes>::GetFloatQuantities()["lep1Phi"]);
	LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("m_1", LambdaNtupleConsumer<KappaTypes>::GetFloatQuantities()["lep1Mass"]);
	LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("q_1", LambdaNtupleConsumer<KappaTypes>::GetFloatQuantities()["lep1Charge"]);
	LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("dZ_1", LambdaNtupleConsumer<KappaTypes>::GetFloatQuantities()["lep1Dz"]);
	LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("d0_1", LambdaNtupleConsumer<KappaTypes>::GetFloatQuantities()["lep1D0"]);
	LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("iso_1", LambdaNtupleConsumer<KappaTypes>::GetFloatQuantities()["lep1IsoOverPt"]);
	LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("mt_1", LambdaNtupleConsumer<KappaTypes>::GetFloatQuantities()["lep1MetMt"]);
	LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("pt_2", LambdaNtupleConsumer<KappaTypes>::GetFloatQuantities()["lep2Pt"]);
	LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("eta_2", LambdaNtupleConsumer<KappaTypes>::GetFloatQuantities()["lep2Eta"]);
	LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("phi_2", LambdaNtupleConsumer<KappaTypes>::GetFloatQuantities()["lep2Phi"]);
	LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("m_2", LambdaNtupleConsumer<KappaTypes>::GetFloatQuantities()["lep2Mass"]);
	LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("q_2", LambdaNtupleConsumer<KappaTypes>::GetFloatQuantities()["lep2Charge"]);
	LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("dZ_2", LambdaNtupleConsumer<KappaTypes>::GetFloatQuantities()["lep2Dz"]);
	LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("d0_2", LambdaNtupleConsumer<KappaTypes>::GetFloatQuantities()["lep2D0"]);
	LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("iso_2", LambdaNtupleConsumer<KappaTypes>::GetFloatQuantities()["lep2IsoOverPt"]);
	LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("mt_2", LambdaNtupleConsumer<KappaTypes>::GetFloatQuantities()["lep2MetMt"]);
	LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("met", LambdaNtupleConsumer<KappaTypes>::GetFloatQuantities()["pfMetPt"]);
	LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("metphi", LambdaNtupleConsumer<KappaTypes>::GetFloatQuantities()["pfMetPhi"]);
	LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("metcov00", LambdaNtupleConsumer<KappaTypes>::GetFloatQuantities()["pfMetCov00"]);
	LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("metcov01", LambdaNtupleConsumer<KappaTypes>::GetFloatQuantities()["pfMetCov01"]);
	LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("metcov10", LambdaNtupleConsumer<KappaTypes>::GetFloatQuantities()["pfMetCov10"]);
	LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("metcov11", LambdaNtupleConsumer<KappaTypes>::GetFloatQuantities()["pfMetCov11"]);
	LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("mvamet", LambdaNtupleConsumer<KappaTypes>::GetFloatQuantities()["mvaMetPt"]);
	LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("mvametphi", LambdaNtupleConsumer<KappaTypes>::GetFloatQuantities()["mvaMetPhi"]);
	LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("mvacov00", LambdaNtupleConsumer<KappaTypes>::GetFloatQuantities()["mvaMetCov00"]);
	LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("mvacov01", LambdaNtupleConsumer<KappaTypes>::GetFloatQuantities()["mvaMetCov01"]);
	LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("mvacov10", LambdaNtupleConsumer<KappaTypes>::GetFloatQuantities()["mvaMetCov10"]);
	LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("mvacov11", LambdaNtupleConsumer<KappaTypes>::GetFloatQuantities()["mvaMetCov11"]);
	LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("pzetavis", LambdaNtupleConsumer<KappaTypes>::GetFloatQuantities()["pZetaVis"]);
	LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("pzetamiss", LambdaNtupleConsumer<KappaTypes>::GetFloatQuantities()["pZetaMiss"]);
	LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("jpt_1", LambdaNtupleConsumer<KappaTypes>::GetFloatQuantities()["leadingJetPt"]);
	LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("jeta_1", LambdaNtupleConsumer<KappaTypes>::GetFloatQuantities()["leadingJetEta"]);
	LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("jphi_1", LambdaNtupleConsumer<KappaTypes>::GetFloatQuantities()["leadingJetPhi"]);
	LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("jmva_1", LambdaNtupleConsumer<KappaTypes>::GetFloatQuantities()["leadingJetPuID"]);
	LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("jcsv_1", LambdaNtupleConsumer<KappaTypes>::GetFloatQuantities()["leadingJetCSV"]);
	LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("bpt_1", LambdaNtupleConsumer<KappaTypes>::GetFloatQuantities()["bJetPt"]);
	LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("beta_1", LambdaNtupleConsumer<KappaTypes>::GetFloatQuantities()["bJetEta"]);
	LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("bphi_1", LambdaNtupleConsumer<KappaTypes>::GetFloatQuantities()["bJetPhi"]);
	LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("bmva_1", LambdaNtupleConsumer<KappaTypes>::GetFloatQuantities()["leadingBJetPuID"]);
	LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("bcsv_1", LambdaNtupleConsumer<KappaTypes>::GetFloatQuantities()["leadingBJetCSV"]);

	LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("jpt_2", LambdaNtupleConsumer<KappaTypes>::GetFloatQuantities()["trailingJetPt"]);
	LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("jeta_2", LambdaNtupleConsumer<KappaTypes>::GetFloatQuantities()["trailingJetEta"]);
	LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("jphi_2", LambdaNtupleConsumer<KappaTypes>::GetFloatQuantities()["trailingJetPhi"]);

	LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("jpt_3", LambdaNtupleConsumer<KappaTypes>::GetFloatQuantities()["thirdJetPt"]);
	LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("jeta_3", LambdaNtupleConsumer<KappaTypes>::GetFloatQuantities()["thirdJetEta"]);
	LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("jphi_3", LambdaNtupleConsumer<KappaTypes>::GetFloatQuantities()["thirdJetPhi"]);
	LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("jpt_4", LambdaNtupleConsumer<KappaTypes>::GetFloatQuantities()["fourthJetPt"]);
	LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("jeta_4", LambdaNtupleConsumer<KappaTypes>::GetFloatQuantities()["fourthJetEta"]);
	LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("jphi_4", LambdaNtupleConsumer<KappaTypes>::GetFloatQuantities()["fourthJetPhi"]);
	LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("jpt_5", LambdaNtupleConsumer<KappaTypes>::GetFloatQuantities()["fifthJetPt"]);
	LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("jeta_5", LambdaNtupleConsumer<KappaTypes>::GetFloatQuantities()["fifthJetEta"]);
	LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("jphi_5", LambdaNtupleConsumer<KappaTypes>::GetFloatQuantities()["fifthJetPhi"]);
	LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("jpt_6", LambdaNtupleConsumer<KappaTypes>::GetFloatQuantities()["sixthJetPt"]);
	LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("jeta_6", LambdaNtupleConsumer<KappaTypes>::GetFloatQuantities()["sixthJetEta"]);
	LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("jphi_6", LambdaNtupleConsumer<KappaTypes>::GetFloatQuantities()["sixthJetPhi"]);

	LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("jmva_2", LambdaNtupleConsumer<KappaTypes>::GetFloatQuantities()["trailingJetPuID"]);
	LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("jcsv_2", LambdaNtupleConsumer<KappaTypes>::GetFloatQuantities()["trailingJetCSV"]);
	LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("bpt_2", LambdaNtupleConsumer<KappaTypes>::GetFloatQuantities()["bJet2Pt"]);
	LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("beta_2", LambdaNtupleConsumer<KappaTypes>::GetFloatQuantities()["bJet2Eta"]);
	LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("bphi_2", LambdaNtupleConsumer<KappaTypes>::GetFloatQuantities()["bJet2Phi"]);
	LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("bmva_2", LambdaNtupleConsumer<KappaTypes>::GetFloatQuantities()["trailingBJetPuID"]);
	LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("bcsv_2", LambdaNtupleConsumer<KappaTypes>::GetFloatQuantities()["trailingBJetCSV"]);

	LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("mjj", LambdaNtupleConsumer<KappaTypes>::GetFloatQuantities()["diJetMass"]);
	LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("jdeta", LambdaNtupleConsumer<KappaTypes>::GetFloatQuantities()["diJetAbsDeltaEta"]);
	LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("jdphi", LambdaNtupleConsumer<KappaTypes>::GetFloatQuantities()["diJetDeltaPhi"]);
	LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("dijetpt", LambdaNtupleConsumer<KappaTypes>::GetFloatQuantities()["diJetPt"]);
	LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("dijetphi", LambdaNtupleConsumer<KappaTypes>::GetFloatQuantities()["diJetPhi"]);
	LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("hdijetphi", LambdaNtupleConsumer<KappaTypes>::GetFloatQuantities()["diJetdiLepPhi"]);

	LambdaNtupleConsumer<KappaTypes>::AddIntQuantity("njets", LambdaNtupleConsumer<KappaTypes>::GetIntQuantities()["nJets30"]);
	LambdaNtupleConsumer<KappaTypes>::AddIntQuantity("njetspt30", LambdaNtupleConsumer<KappaTypes>::GetIntQuantities()["nJets30"]);
	LambdaNtupleConsumer<KappaTypes>::AddIntQuantity("njetspt20", LambdaNtupleConsumer<KappaTypes>::GetIntQuantities()["nJets20"]);
	LambdaNtupleConsumer<KappaTypes>::AddIntQuantity("nbtag", LambdaNtupleConsumer<KappaTypes>::GetIntQuantities()["nBJets20"]);
	LambdaNtupleConsumer<KappaTypes>::AddIntQuantity("njetingap", LambdaNtupleConsumer<KappaTypes>::GetIntQuantities()["nCentralJets30"]);
	LambdaNtupleConsumer<KappaTypes>::AddIntQuantity("njetingap30", LambdaNtupleConsumer<KappaTypes>::GetIntQuantities()["nCentralJets30"]);
	LambdaNtupleConsumer<KappaTypes>::AddIntQuantity("njetingap20", LambdaNtupleConsumer<KappaTypes>::GetIntQuantities()["nCentralJets20"]);

	LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("pt_sv", LambdaNtupleConsumer<KappaTypes>::GetFloatQuantities()["svfitPt"]);
	LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("eta_sv", LambdaNtupleConsumer<KappaTypes>::GetFloatQuantities()["svfitEta"]);
	LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("phi_sv", LambdaNtupleConsumer<KappaTypes>::GetFloatQuantities()["svfitPhi"]);
	LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("m_sv", LambdaNtupleConsumer<KappaTypes>::GetFloatQuantities()["svfitMass"]);
	LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("mt_sv", LambdaNtupleConsumer<KappaTypes>::GetFloatQuantities()["svfitTransverseMass"]);
	LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("met_sv", LambdaNtupleConsumer<KappaTypes>::GetFloatQuantities()["svfitMet"]);

	LambdaNtupleConsumer<KappaTypes>::AddBoolQuantity("NUP", [](KappaEvent const& event, KappaProduct const& product)
	{
		return product.m_genNPartons;
	});

	LambdaNtupleConsumer<KappaTypes>::AddIntQuantity("isFake", [](KappaEvent const& event, KappaProduct const& product)
	{
		return DefaultValues::UndefinedInt;
	});
	LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("visjeteta", [](KappaEvent const& event, KappaProduct const& product)
	{
		return DefaultValues::UndefinedFloat;
	});
// 	LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("ptvis", [](KappaEvent const& event, KappaProduct const& product)
// 	{
// 		return DefaultValues::UndefinedFloat;
// 	});
	LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("jrawf_1", [](KappaEvent const& event, KappaProduct const& product)
	{
		return DefaultValues::UndefinedFloat;
	});
	LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("jrawf_2", [](KappaEvent const& event, KappaProduct const& product)
	{
		return DefaultValues::UndefinedFloat;
	});
	LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("jpfid_1", [](KappaEvent const& event, KappaProduct const& product)
	{
		return DefaultValues::UndefinedFloat;
	});
	LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("jpfid_2", [](KappaEvent const& event, KappaProduct const& product)
	{
		return DefaultValues::UndefinedFloat;
	});
	LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("jpuid_1", [](KappaEvent const& event, KappaProduct const& product)
	{
		return DefaultValues::UndefinedFloat;
	});
	LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("jpuid_2", [](KappaEvent const& event, KappaProduct const& product)
	{
		return DefaultValues::UndefinedFloat;
	});
	LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("brawf_1", [](KappaEvent const& event, KappaProduct const& product)
	{
		return DefaultValues::UndefinedFloat;
	});
	LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("bpfid_1", [](KappaEvent const& event, KappaProduct const& product)
	{
		return DefaultValues::UndefinedFloat;
	});
	LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("bpuid_1", [](KappaEvent const& event, KappaProduct const& product)
	{
		return DefaultValues::UndefinedFloat;
	});
	LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("brawf_2", [](KappaEvent const& event, KappaProduct const& product)
	{
		return DefaultValues::UndefinedFloat;
	});
	LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("bpfid_2", [](KappaEvent const& event, KappaProduct const& product)
	{
		return DefaultValues::UndefinedFloat;
	});
	LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("bpuid_2", [](KappaEvent const& event, KappaProduct const& product)
	{
		return DefaultValues::UndefinedFloat;
	});

	// need to be called at last
	KappaLambdaNtupleConsumer::Init(settings);
}
