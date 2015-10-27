
#include <Math/VectorUtil.h>

#include "Artus/Utility/interface/SafeMap.h"
#include "Artus/Utility/interface/Utility.h"
#include "Artus/Utility/interface/DefaultValues.h"
#include "Artus/KappaAnalysis/interface/KappaTypes.h"

#include "Artus/KappaAnalysis/interface/Producers/GenTauDecayModeProducer.h"

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

	LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("puweight", [](KappaEvent const& event, KappaProduct const& product)
	{
		return SafeMap::GetWithDefault(product.m_weights, std::string("puWeight"), 1.0);
	});
	LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("trigweight_1", [](KappaEvent const& event, KappaProduct const& product)
	{
		return SafeMap::GetWithDefault(product.m_weights, std::string("triggerWeight1"), 1.0);
	});
	LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("trigweight_2", [](KappaEvent const& event, KappaProduct const& product)
	{
		return SafeMap::GetWithDefault(product.m_weights, std::string("triggerWeight2"), 1.0);
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
	
	LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("m_vis", LambdaNtupleConsumer<KappaTypes>::GetFloatQuantities()["diLepMass"]);
	LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("mvis", LambdaNtupleConsumer<KappaTypes>::GetFloatQuantities()["diLepMass"]);
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
	LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("met_sv", LambdaNtupleConsumer<KappaTypes>::GetFloatQuantities()["svfitMet"]);
	
	LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("isZEE", [](KappaEvent const& event, KappaProduct const& product)
	{
		return (product.m_genDiLeptonDecayMode == KappaEnumTypes::DiLeptonDecayMode::EE);
	});
	LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("isZMM", [](KappaEvent const& event, KappaProduct const& product)
	{
		return (product.m_genDiLeptonDecayMode == KappaEnumTypes::DiLeptonDecayMode::MM);
	});
	LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("isZLL", [](KappaEvent const& event, KappaProduct const& product)
	{
		return (product.m_genDiLeptonDecayMode == KappaEnumTypes::DiLeptonDecayMode::MM || product.m_genDiLeptonDecayMode == KappaEnumTypes::DiLeptonDecayMode::EE);
	});
	LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("isZtt", [](KappaEvent const& event, KappaProduct const& product)
	{
		return (product.m_genTauDecayMode == (int) GenTauDecayModeProducer::GenTauDecayMode::TT);
	});
	LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("isZmt", [](KappaEvent const& event, KappaProduct const& product)
	{
		return (product.m_genTauDecayMode == (int) GenTauDecayModeProducer::GenTauDecayMode::MT);
	});
	LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("isZet", [](KappaEvent const& event, KappaProduct const& product)
	{
		return (product.m_genTauDecayMode == (int) GenTauDecayModeProducer::GenTauDecayMode::ET);
	});
	LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("isZee", [](KappaEvent const& event, KappaProduct const& product)
	{
		return (product.m_genTauDecayMode == (int) GenTauDecayModeProducer::GenTauDecayMode::EE);
	});
	LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("isZmm", [](KappaEvent const& event, KappaProduct const& product)
	{
		return (product.m_genTauDecayMode == (int) GenTauDecayModeProducer::GenTauDecayMode::MM);
	});
	LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("isZem", [](KappaEvent const& event, KappaProduct const& product)
	{
		return (product.m_genTauDecayMode == (int) GenTauDecayModeProducer::GenTauDecayMode::EM);
	});
	LambdaNtupleConsumer<KappaTypes>::AddIntQuantity("NUP", [](KappaEvent const& event, KappaProduct const& product)
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
	LambdaNtupleConsumer<KappaTypes>::AddFloatQuantity("ptvis", [](KappaEvent const& event, KappaProduct const& product)
	{
		return DefaultValues::UndefinedFloat;
	});
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
	LambdaNtupleConsumer<KappaTypes>::AddIntQuantity("extraelec_veto", [](KappaEvent const& event, KappaProduct const& product)
	{
		return static_cast<HttProduct const&>(product).m_extraElecVeto;
	});
	LambdaNtupleConsumer<KappaTypes>::AddIntQuantity("extramuon_veto", [](KappaEvent const& event, KappaProduct const& product)
	{
		return static_cast<HttProduct const&>(product).m_extraMuonVeto;
	});

	// need to be called at last
	KappaLambdaNtupleConsumer::Init(settings);
}
