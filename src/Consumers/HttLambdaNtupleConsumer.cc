
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
	LambdaNtupleConsumer<HttTypes>::AddUInt64Quantity(metadata, "evt", [](event_type const& event, product_type const& product)
	{
		return event.m_eventInfo->nEvent;
	});

	bool bInpData = settings.GetInputIsData();
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "npu", [bInpData](event_type const& event, product_type const& product)
	{
		if (bInpData)
			return DefaultValues::UndefinedFloat;
		return static_cast<KGenEventInfo*>(event.m_eventInfo)->nPUMean;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "puweight", [](event_type const& event, product_type const& product)
	{
		return SafeMap::GetWithDefault(product.m_weights, std::string("puWeight"), 1.0);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "trigweight_1", [](event_type const& event, product_type const& product)
	{
		return SafeMap::GetWithDefault(product.m_weights, std::string("triggerWeight_1"), 1.0);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "trigweight_2", [](event_type const& event, product_type const& product)
	{
		return SafeMap::GetWithDefault(product.m_weights, std::string("triggerWeight_2"), 1.0);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "idisoweight_1", [](event_type const& event, product_type const& product)
	{
		return SafeMap::GetWithDefault(product.m_weights, std::string("identificationWeight_1"), 1.0);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "idisoweight_2", [](event_type const& event, product_type const& product)
	{
		return SafeMap::GetWithDefault(product.m_weights, std::string("identificationWeight_2"), 1.0);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "weight", [settings](event_type const& event, product_type const& product)
	{
		return SafeMap::GetWithDefault(product.m_weights, settings.GetEventWeight(), 1.0);
	});

	LambdaNtupleConsumer<HttTypes>::AddIntQuantity(metadata, "nDiLeptonVetoPairsOS", [](event_type const& event, product_type const& product)
	{
		return product.m_nDiElectronVetoPairsOS + product.m_nDiMuonVetoPairsOS;
	});
	LambdaNtupleConsumer<HttTypes>::AddIntQuantity(metadata, "nDiLeptonVetoPairsSS", [](event_type const& event, product_type const& product)
	{
		return product.m_nDiElectronVetoPairsSS + product.m_nDiMuonVetoPairsSS;
	});
	LambdaNtupleConsumer<HttTypes>::AddIntQuantity(metadata, "dilepton_veto", [](event_type const& event, product_type const& product)
	{
		return ((product.m_nDiElectronVetoPairsOS + product.m_nDiMuonVetoPairsOS) >= 1) ? 1 : 0;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "mt_tot", [metadata](event_type const& event, product_type const& product)
	{
		return sqrt(pow(SafeMap::Get(metadata.m_commonFloatQuantities,std::string("mt_tt"))(event,product),2)+pow(SafeMap::Get(metadata.m_commonFloatQuantities,std::string("lep1MetMt"))(event,product),2)+pow(SafeMap::Get(metadata.m_commonFloatQuantities,std::string("lep2MetMt"))(event,product),2));
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "m_vis", metadata.m_commonFloatQuantities["diLepMass"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "mvis", metadata.m_commonFloatQuantities["diLepMass"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "ptvis", metadata.m_commonFloatQuantities["diLepPt"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "H_pt", metadata.m_commonFloatQuantities["diLepMetPt"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "H_mass", metadata.m_commonFloatQuantities["diLepMetMass"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "pt_tt", metadata.m_commonFloatQuantities["diLepMetPt"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "pt_1", metadata.m_commonFloatQuantities["lep1Pt"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "eta_1", metadata.m_commonFloatQuantities["lep1Eta"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "phi_1", metadata.m_commonFloatQuantities["lep1Phi"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "m_1", metadata.m_commonFloatQuantities["lep1Mass"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "q_1", metadata.m_commonFloatQuantities["lep1Charge"]);

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "dZ_1", metadata.m_commonFloatQuantities["lep1Dz"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "d0_1", metadata.m_commonFloatQuantities["lep1D0"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "errDZ_1", metadata.m_commonFloatQuantities["lep1ErrDz"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "errD0_1", metadata.m_commonFloatQuantities["lep1ErrD0"]);

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "iso_1", metadata.m_commonFloatQuantities["lep1IsoOverPt"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "mt_1", metadata.m_commonFloatQuantities["lep1MetMt"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "pt_2", metadata.m_commonFloatQuantities["lep2Pt"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "eta_2", metadata.m_commonFloatQuantities["lep2Eta"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "phi_2", metadata.m_commonFloatQuantities["lep2Phi"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "m_2", metadata.m_commonFloatQuantities["lep2Mass"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "q_2", metadata.m_commonFloatQuantities["lep2Charge"]);

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "dZ_2", metadata.m_commonFloatQuantities["lep2Dz"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "d0_2", metadata.m_commonFloatQuantities["lep2D0"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "errDZ_2", metadata.m_commonFloatQuantities["lep2ErrDz"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "errD0_2", metadata.m_commonFloatQuantities["lep2ErrD0"]);

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "iso_2", metadata.m_commonFloatQuantities["lep2IsoOverPt"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "mt_2", metadata.m_commonFloatQuantities["lep2MetMt"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "met", metadata.m_commonFloatQuantities["metPt"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "metphi", metadata.m_commonFloatQuantities["metPhi"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "metcov00", metadata.m_commonFloatQuantities["metCov00"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "metcov01", metadata.m_commonFloatQuantities["metCov01"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "metcov10", metadata.m_commonFloatQuantities["metCov10"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "metcov11", metadata.m_commonFloatQuantities["metCov11"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "pfmet", metadata.m_commonFloatQuantities["pfMetPt"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "pfmetphi", metadata.m_commonFloatQuantities["pfMetPhi"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "pfmetcov00", metadata.m_commonFloatQuantities["pfMetCov00"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "pfmetcov01", metadata.m_commonFloatQuantities["pfMetCov01"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "pfmetcov10", metadata.m_commonFloatQuantities["pfMetCov10"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "pfmetcov11", metadata.m_commonFloatQuantities["pfMetCov11"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "mvamet", metadata.m_commonFloatQuantities["mvaMetPt"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "mvametphi", metadata.m_commonFloatQuantities["mvaMetPhi"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "mvacov00", metadata.m_commonFloatQuantities["mvaMetCov00"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "mvacov01", metadata.m_commonFloatQuantities["mvaMetCov01"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "mvacov10", metadata.m_commonFloatQuantities["mvaMetCov10"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "mvacov11", metadata.m_commonFloatQuantities["mvaMetCov11"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "pzetavis", metadata.m_commonFloatQuantities["pZetaVis"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "pzetamiss", metadata.m_commonFloatQuantities["pZetaMiss"]);
	
	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity(metadata, "jlv_1", metadata.m_commonRMFLVQuantities["leadingJetLV"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "jpt_1", metadata.m_commonFloatQuantities["leadingJetPt"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "jeta_1", metadata.m_commonFloatQuantities["leadingJetEta"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "jphi_1", metadata.m_commonFloatQuantities["leadingJetPhi"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "jm_1", metadata.m_commonFloatQuantities["leadingJetMass"]);

	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity(metadata, "jlv_2", metadata.m_commonRMFLVQuantities["trailingJetLV"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "jpt_2", metadata.m_commonFloatQuantities["trailingJetPt"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "jeta_2", metadata.m_commonFloatQuantities["trailingJetEta"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "jphi_2", metadata.m_commonFloatQuantities["trailingJetPhi"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "jm_2", metadata.m_commonFloatQuantities["trailingJetMass"]);

	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity(metadata, "jlv_3", metadata.m_commonRMFLVQuantities["thirdJetLV"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "jpt_3", metadata.m_commonFloatQuantities["thirdJetPt"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "jeta_3", metadata.m_commonFloatQuantities["thirdJetEta"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "jphi_3", metadata.m_commonFloatQuantities["thirdJetPhi"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "jm_3", metadata.m_commonFloatQuantities["thirdJetMass"]);
	
	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity(metadata, "jlv_4", metadata.m_commonRMFLVQuantities["fourthJetLV"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "jpt_4", metadata.m_commonFloatQuantities["fourthJetPt"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "jeta_4", metadata.m_commonFloatQuantities["fourthJetEta"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "jphi_4", metadata.m_commonFloatQuantities["fourthJetPhi"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "jm_4", metadata.m_commonFloatQuantities["fourthJetMass"]);
	
	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity(metadata, "jlv_5", metadata.m_commonRMFLVQuantities["fifthJetLV"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "jpt_5", metadata.m_commonFloatQuantities["fifthJetPt"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "jeta_5", metadata.m_commonFloatQuantities["fifthJetEta"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "jphi_5", metadata.m_commonFloatQuantities["fifthJetPhi"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "jm_5", metadata.m_commonFloatQuantities["fifthJetMass"]);
	
	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity(metadata, "jlv_6", metadata.m_commonRMFLVQuantities["sixthJetLV"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "jpt_6", metadata.m_commonFloatQuantities["sixthJetPt"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "jeta_6", metadata.m_commonFloatQuantities["sixthJetEta"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "jphi_6", metadata.m_commonFloatQuantities["sixthJetPhi"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "jm_6", metadata.m_commonFloatQuantities["sixthJetMass"]);
	
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "jmva_1", metadata.m_commonFloatQuantities["leadingJetPuID"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "jcsv_1", metadata.m_commonFloatQuantities["leadingJetCSV"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "bpt_1", metadata.m_commonFloatQuantities["bJetPt"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "beta_1", metadata.m_commonFloatQuantities["bJetEta"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "bphi_1", metadata.m_commonFloatQuantities["bJetPhi"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "bmva_1", metadata.m_commonFloatQuantities["leadingBJetPuID"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "bcsv_1", metadata.m_commonFloatQuantities["leadingBJetCSV"]);
	
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "jmva_2", metadata.m_commonFloatQuantities["trailingJetPuID"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "jcsv_2", metadata.m_commonFloatQuantities["trailingJetCSV"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "bpt_2", metadata.m_commonFloatQuantities["bJet2Pt"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "beta_2", metadata.m_commonFloatQuantities["bJet2Eta"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "bphi_2", metadata.m_commonFloatQuantities["bJet2Phi"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "bmva_2", metadata.m_commonFloatQuantities["trailingBJetPuID"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "bcsv_2", metadata.m_commonFloatQuantities["trailingBJetCSV"]);
	
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "jcsv_3", metadata.m_commonFloatQuantities["thirdJetCSV"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "jcsv_4", metadata.m_commonFloatQuantities["fourthJetCSV"]);

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "mjj", metadata.m_commonFloatQuantities["diJetMass"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "jdeta", metadata.m_commonFloatQuantities["diJetAbsDeltaEta"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "jdphi", metadata.m_commonFloatQuantities["diJetDeltaPhi"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "dijetpt", metadata.m_commonFloatQuantities["diJetPt"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "dijetphi", metadata.m_commonFloatQuantities["diJetPhi"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "hdijetphi", metadata.m_commonFloatQuantities["diJetdiLepPhi"]);

	LambdaNtupleConsumer<HttTypes>::AddIntQuantity(metadata, "njets", metadata.m_commonIntQuantities["nJets30"]);
	LambdaNtupleConsumer<HttTypes>::AddIntQuantity(metadata, "njetspt30", metadata.m_commonIntQuantities["nJets30"]);
	LambdaNtupleConsumer<HttTypes>::AddIntQuantity(metadata, "njetspt20", metadata.m_commonIntQuantities["nJets20"]);
	LambdaNtupleConsumer<HttTypes>::AddIntQuantity(metadata, "njetspt20eta2p4", metadata.m_commonIntQuantities["nJets20Eta2p4"]);
	LambdaNtupleConsumer<HttTypes>::AddIntQuantity(metadata, "nbtag", metadata.m_commonIntQuantities["nBJets20"]);
	LambdaNtupleConsumer<HttTypes>::AddIntQuantity(metadata, "njetingap", metadata.m_commonIntQuantities["nCentralJets30"]);
	LambdaNtupleConsumer<HttTypes>::AddIntQuantity(metadata, "njetingap30", metadata.m_commonIntQuantities["nCentralJets30"]);
	LambdaNtupleConsumer<HttTypes>::AddIntQuantity(metadata, "njetingap20", metadata.m_commonIntQuantities["nCentralJets20"]);

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "pt_sv", metadata.m_commonFloatQuantities["svfitPt"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "eta_sv", metadata.m_commonFloatQuantities["svfitEta"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "phi_sv", metadata.m_commonFloatQuantities["svfitPhi"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "m_sv", metadata.m_commonFloatQuantities["svfitMass"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "mt_sv", metadata.m_commonFloatQuantities["svfitTransverseMass"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "met_sv", metadata.m_commonFloatQuantities["svfitMet"]);

	LambdaNtupleConsumer<HttTypes>::AddIntQuantity(metadata, "npartons", [](event_type const& event, product_type const& product)
	{
		return event.m_genEventInfo ? event.m_genEventInfo->lheNOutPartons : DefaultValues::UndefinedInt;
	});
	LambdaNtupleConsumer<HttTypes>::AddIntQuantity(metadata, "NUP", metadata.m_commonIntQuantities["npartons"]);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genbosonmass", [metadata](event_type const& event, product_type const& product)
	{
		return Utility::Contains(metadata.m_commonFloatQuantities, std::string("genBosonMass")) ? SafeMap::Get(metadata.m_commonFloatQuantities, std::string("genBosonMass"))(event, product) : DefaultValues::UndefinedFloat;
	});


	LambdaNtupleConsumer<HttTypes>::AddIntQuantity(metadata, "isFake", [](event_type const& event, product_type const& product)
	{
		return DefaultValues::UndefinedInt;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "visjeteta", [](event_type const& event, product_type const& product)
	{
		return DefaultValues::UndefinedFloat;
	});
// 	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "ptvis", [](event_type const& event, product_type const& product)
// 	{
// 		return DefaultValues::UndefinedFloat;
// 	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "jrawf_1", [](event_type const& event, product_type const& product)
	{
		return DefaultValues::UndefinedFloat;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "jrawf_2", [](event_type const& event, product_type const& product)
	{
		return DefaultValues::UndefinedFloat;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "jpfid_1", [](event_type const& event, product_type const& product)
	{
		return DefaultValues::UndefinedFloat;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "jpfid_2", [](event_type const& event, product_type const& product)
	{
		return DefaultValues::UndefinedFloat;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "jpuid_1", [](event_type const& event, product_type const& product)
	{
		return DefaultValues::UndefinedFloat;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "jpuid_2", [](event_type const& event, product_type const& product)
	{
		return DefaultValues::UndefinedFloat;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "brawf_1", [](event_type const& event, product_type const& product)
	{
		return DefaultValues::UndefinedFloat;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "bpfid_1", [](event_type const& event, product_type const& product)
	{
		return DefaultValues::UndefinedFloat;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "bpuid_1", [](event_type const& event, product_type const& product)
	{
		return DefaultValues::UndefinedFloat;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "brawf_2", [](event_type const& event, product_type const& product)
	{
		return DefaultValues::UndefinedFloat;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "bpfid_2", [](event_type const& event, product_type const& product)
	{
		return DefaultValues::UndefinedFloat;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "bpuid_2", [](event_type const& event, product_type const& product)
	{
		return DefaultValues::UndefinedFloat;
	});

	// need to be called at last
	KappaLambdaNtupleConsumer::Init(settings, metadata);
}
