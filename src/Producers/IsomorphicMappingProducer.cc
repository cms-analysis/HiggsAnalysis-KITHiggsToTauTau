#include <boost/algorithm/string.hpp>

#include "Artus/Consumer/interface/LambdaNtupleConsumer.h"
#include "Artus/KappaAnalysis/interface/KappaTypes.h"
#include "Artus/Utility/interface/UnitConverter.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttEnumTypes.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Utility/CPQuantities.h"
#include "HiggsCPinTauDecays/ImpactParameter/interface/ImpactParameter.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/IsomorphicMappingProducer.h"

#include <fstream>

std::string IsomorphicMappingProducer::GetProducerId() const
{
	return "IsomorphicMappingProducer";
}

void IsomorphicMappingProducer::Init(setting_type const& settings, metadata_type& metadata)
{
	ProducerBase<HttTypes>::Init(settings, metadata);
	m_isData = settings.GetInputIsData();
	m_isEmbedding = settings.GetInputIsEmbedding();

	TDirectory *savedir(gDirectory);
	TFile *savefile(gFile);

	m_year = std::to_string(settings.GetYear());
	// m_decayChannel = boost::algorithm::to_lower_copy(settings.GetChannel());
	if (m_isEmbedding) {
		m_emb = "_emb";
	} else {
		m_emb = "";
	}

	std::string ipHelrPV_x_prompt_str;
	std::string ipHelrPV_y_prompt_str;
	std::string ipHelrPV_z_prompt_str;
	std::string ipHelrPVBS_x_prompt_str;
	std::string ipHelrPVBS_y_prompt_str;
	std::string ipHelrPVBS_z_prompt_str;

	std::string ipHelrPV_x_muon_str;
	std::string ipHelrPV_y_muon_str;
	std::string ipHelrPV_z_muon_str;
	std::string ipHelrPVBS_x_muon_str;
	std::string ipHelrPVBS_y_muon_str;
	std::string ipHelrPVBS_z_muon_str;

	std::string ipHelrPV_x_pion_str;
	std::string ipHelrPV_y_pion_str;
	std::string ipHelrPV_z_pion_str;
	std::string ipHelrPVBS_x_pion_str;
	std::string ipHelrPVBS_y_pion_str;
	std::string ipHelrPVBS_z_pion_str;



	// Calibration Curves for prompt decays (calibration done in Z->mumu)
	ipHelrPV_x_prompt_str     = std::string("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/isomap/prompt/calib_zmm" + m_year + m_emb + "/ip_nx.root");
	ipHelrPV_y_prompt_str   = std::string("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/isomap/prompt/calib_zmm" + m_year + m_emb + "/ip_ny.root");
	ipHelrPV_z_prompt_str = std::string("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/isomap/prompt/calib_zmm" + m_year + m_emb + "/ip_nz.root");

	ipHelrPVBS_x_prompt_str     = std::string("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/isomap/prompt/calib_zmm" + m_year + m_emb + "/ip_bs_nx.root");
	ipHelrPVBS_y_prompt_str   = std::string("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/isomap/prompt/calib_zmm" + m_year + m_emb + "/ip_bs_ny.root");
	ipHelrPVBS_z_prompt_str = std::string("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/isomap/prompt/calib_zmm" + m_year + m_emb + "/ip_bs_nz.root");

	// Calibration curves for non prompt decays
	// tau->muon
	ipHelrPV_x_muon_str     = std::string("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/isomap/muon/calib" + m_year + m_emb + "/ip_nx.root");
	ipHelrPV_y_muon_str   = std::string("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/isomap/muon/calib" + m_year + m_emb + "/ip_ny.root");
	ipHelrPV_z_muon_str = std::string("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/isomap/muon/calib" + m_year + m_emb + "/ip_nz.root");
	ipHelrPVBS_x_muon_str     = std::string("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/isomap/muon/calib" + m_year + m_emb + "/ip_bs_nx.root");
	ipHelrPVBS_y_muon_str   = std::string("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/isomap/muon/calib" + m_year + m_emb + "/ip_bs_ny.root");
	ipHelrPVBS_z_muon_str = std::string("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/isomap/muon/calib" + m_year + m_emb + "/ip_bs_nz.root");
	// tau->pion
	ipHelrPV_x_pion_str     = std::string("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/isomap/pion/calib" + m_year + m_emb + "/ip_nx.root");
	ipHelrPV_y_pion_str   = std::string("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/isomap/pion/calib" + m_year + m_emb + "/ip_ny.root");
	ipHelrPV_z_pion_str = std::string("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/isomap/pion/calib" + m_year + m_emb + "/ip_nz.root");
	ipHelrPVBS_x_pion_str     = std::string("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/isomap/pion/calib" + m_year + m_emb + "/ip_bs_nx.root");
	ipHelrPVBS_y_pion_str   = std::string("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/isomap/pion/calib" + m_year + m_emb + "/ip_bs_ny.root");
	ipHelrPVBS_z_pion_str = std::string("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/isomap/pion/calib" + m_year + m_emb + "/ip_bs_nz.root");

	// Prompt Decays
	// refit PV
	TFile inputFile_ipHelrPV_prompt_x(ipHelrPV_x_prompt_str.c_str(), "READ");
	m_ipHelrPV_x_prompt_isomap = static_cast<TGraph*>(inputFile_ipHelrPV_prompt_x.Get("isomap"));
	inputFile_ipHelrPV_prompt_x.Close();

	TFile inputFile_ipHelrPV_prompt_y(ipHelrPV_y_prompt_str.c_str(), "READ");
	m_ipHelrPV_y_prompt_isomap = static_cast<TGraph*>(inputFile_ipHelrPV_prompt_y.Get("isomap"));
	inputFile_ipHelrPV_prompt_y.Close();

	TFile inputFile_ipHelrPV_prompt_z(ipHelrPV_z_prompt_str.c_str(), "READ");
	m_ipHelrPV_z_prompt_isomap = static_cast<TGraph*>(inputFile_ipHelrPV_prompt_z.Get("isomap"));
	inputFile_ipHelrPV_prompt_z.Close();
	// refit PV with BS
	TFile inputFile_ipHelrPVBS_prompt_x(ipHelrPVBS_x_prompt_str.c_str(), "READ");
	m_ipHelrPVBS_x_prompt_isomap = static_cast<TGraph*>(inputFile_ipHelrPVBS_prompt_x.Get("isomap"));
	inputFile_ipHelrPVBS_prompt_x.Close();

	TFile inputFile_ipHelrPVBS_prompt_y(ipHelrPVBS_y_prompt_str.c_str(), "READ");
	m_ipHelrPVBS_y_prompt_isomap = static_cast<TGraph*>(inputFile_ipHelrPVBS_prompt_y.Get("isomap"));
	inputFile_ipHelrPVBS_prompt_y.Close();

	TFile inputFile_ipHelrPVBS_prompt_z(ipHelrPVBS_z_prompt_str.c_str(), "READ");
	m_ipHelrPVBS_z_prompt_isomap = static_cast<TGraph*>(inputFile_ipHelrPVBS_prompt_z.Get("isomap"));
	inputFile_ipHelrPVBS_prompt_z.Close();

	// Nonprompt decays
	// tau->muon
	// refit PV
	TFile inputFile_ipHelrPV_muon_x(ipHelrPV_x_muon_str.c_str(), "READ");
	m_ipHelrPV_x_muon_isomap = static_cast<TGraph*>(inputFile_ipHelrPV_muon_x.Get("isomap"));
	inputFile_ipHelrPV_muon_x.Close();

	TFile inputFile_ipHelrPV_muon_y(ipHelrPV_y_muon_str.c_str(), "READ");
	m_ipHelrPV_y_muon_isomap = static_cast<TGraph*>(inputFile_ipHelrPV_muon_y.Get("isomap"));
	inputFile_ipHelrPV_muon_y.Close();

	TFile inputFile_ipHelrPV_muon_z(ipHelrPV_z_muon_str.c_str(), "READ");
	m_ipHelrPV_z_muon_isomap = static_cast<TGraph*>(inputFile_ipHelrPV_muon_z.Get("isomap"));
	inputFile_ipHelrPV_muon_z.Close();
	// refit PV with BS
	TFile inputFile_ipHelrPVBS_muon_x(ipHelrPVBS_x_muon_str.c_str(), "READ");
	m_ipHelrPVBS_x_muon_isomap = static_cast<TGraph*>(inputFile_ipHelrPVBS_muon_x.Get("isomap"));
	inputFile_ipHelrPVBS_muon_x.Close();

	TFile inputFile_ipHelrPVBS_muon_y(ipHelrPVBS_y_muon_str.c_str(), "READ");
	m_ipHelrPVBS_y_muon_isomap = static_cast<TGraph*>(inputFile_ipHelrPVBS_muon_y.Get("isomap"));
	inputFile_ipHelrPVBS_muon_y.Close();

	TFile inputFile_ipHelrPVBS_muon_z(ipHelrPVBS_z_muon_str.c_str(), "READ");
	m_ipHelrPVBS_z_muon_isomap = static_cast<TGraph*>(inputFile_ipHelrPVBS_muon_z.Get("isomap"));
	inputFile_ipHelrPVBS_muon_z.Close();
	// tau->pion
	// refit PV
	TFile inputFile_ipHelrPV_pion_x(ipHelrPV_x_pion_str.c_str(), "READ");
	m_ipHelrPV_x_pion_isomap = static_cast<TGraph*>(inputFile_ipHelrPV_pion_x.Get("isomap"));
	inputFile_ipHelrPV_pion_x.Close();

	TFile inputFile_ipHelrPV_pion_y(ipHelrPV_y_pion_str.c_str(), "READ");
	m_ipHelrPV_y_pion_isomap = static_cast<TGraph*>(inputFile_ipHelrPV_pion_y.Get("isomap"));
	inputFile_ipHelrPV_pion_y.Close();

	TFile inputFile_ipHelrPV_pion_z(ipHelrPV_z_pion_str.c_str(), "READ");
	m_ipHelrPV_z_pion_isomap = static_cast<TGraph*>(inputFile_ipHelrPV_pion_z.Get("isomap"));
	inputFile_ipHelrPV_pion_z.Close();
	// refit PV with BS
	TFile inputFile_ipHelrPVBS_pion_x(ipHelrPVBS_x_pion_str.c_str(), "READ");
	m_ipHelrPVBS_x_pion_isomap = static_cast<TGraph*>(inputFile_ipHelrPVBS_pion_x.Get("isomap"));
	inputFile_ipHelrPVBS_pion_x.Close();

	TFile inputFile_ipHelrPVBS_pion_y(ipHelrPVBS_y_pion_str.c_str(), "READ");
	m_ipHelrPVBS_y_pion_isomap = static_cast<TGraph*>(inputFile_ipHelrPVBS_pion_y.Get("isomap"));
	inputFile_ipHelrPVBS_pion_y.Close();

	TFile inputFile_ipHelrPVBS_pion_z(ipHelrPVBS_z_pion_str.c_str(), "READ");
	m_ipHelrPVBS_z_pion_isomap = static_cast<TGraph*>(inputFile_ipHelrPVBS_pion_z.Get("isomap"));
	inputFile_ipHelrPVBS_pion_z.Close();

	gDirectory = savedir;
	gFile = savefile;

	LambdaNtupleConsumer<HttTypes>::AddRMPointQuantity(metadata, "isomapIPHelrPV_1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return (((product.m_isomapIPHelrPV_1).x() != -999) ? RMPoint( (product.m_isomapIPHelrPV_1).x(), (product.m_isomapIPHelrPV_1).y(), (product.m_isomapIPHelrPV_1).z() ) : DefaultValues::UndefinedRMPoint);
	});
	LambdaNtupleConsumer<HttTypes>::AddRMPointQuantity(metadata, "isomapIPHelrPV_2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return (((product.m_isomapIPHelrPV_2).x() != -999) ? RMPoint( (product.m_isomapIPHelrPV_2).x(), (product.m_isomapIPHelrPV_2).y(), (product.m_isomapIPHelrPV_2).z() ) : DefaultValues::UndefinedRMPoint);
	});

	LambdaNtupleConsumer<HttTypes>::AddRMPointQuantity(metadata, "isomapIPHelrPVBS_1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return (((product.m_isomapIPHelrPVBS_1).x() != -999) ? RMPoint( (product.m_isomapIPHelrPVBS_1).x(), (product.m_isomapIPHelrPVBS_1).y(), (product.m_isomapIPHelrPVBS_1).z() ) : DefaultValues::UndefinedRMPoint);
	});
	LambdaNtupleConsumer<HttTypes>::AddRMPointQuantity(metadata, "isomapIPHelrPVBS_2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return (((product.m_isomapIPHelrPVBS_2).x() != -999) ? RMPoint( (product.m_isomapIPHelrPVBS_2).x(), (product.m_isomapIPHelrPVBS_2).y(), (product.m_isomapIPHelrPVBS_2).z() ) : DefaultValues::UndefinedRMPoint);
	});

	// CP-related quantities
	// IP-Method
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "isomapPhiStarCPHelrPV", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_isomapPhiStarCPHelrPV;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "isomapPhiStarCPHelrPVBS", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_isomapPhiStarCPHelrPVBS;
	});
	// Combined Method
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "isomapPhiStarCPCombHelrPV", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_isomapPhiStarCPCombHelrPV;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "isomapPhiStarCPCombMergedHelrPV", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_isomapPhiStarCPCombMergedHelrPV;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "isomapPhiStarCPCombHelrPVBS", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_isomapPhiStarCPCombHelrPVBS;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "isomapPhiStarCPCombMergedHelrPVBS", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_isomapPhiStarCPCombMergedHelrPVBS;
	});


}

void IsomorphicMappingProducer::Produce(event_type const& event, product_type& product, setting_type const& settings, metadata_type const& metadata) const
{
	if (!m_isData){
		assert(event.m_vertexSummary);
		assert(product.m_flavourOrderedLeptons.size() >= 2);

		// initialization of TVector3 objects
		//FIXME These Vectors are only needed for the helical approach
		TVector3 IPPlusHelrPV;
		TVector3 IPMinusHelrPV;
		TVector3 IPPlusHelrPVBS;
		TVector3 IPMinusHelrPVBS;

		IPPlusHelrPV.SetXYZ(-999,-999,-999);
		IPMinusHelrPV.SetXYZ(-999,-999,-999);
		IPPlusHelrPVBS.SetXYZ(-999,-999,-999);
		IPMinusHelrPVBS.SetXYZ(-999,-999,-999);

		product.m_isomapIPHelrPV_1.SetXYZ(-999, -999, -999);
		product.m_isomapIPHelrPV_2.SetXYZ(-999, -999, -999);
		product.m_isomapIPHelrPVBS_1.SetXYZ(-999, -999, -999);
		product.m_isomapIPHelrPVBS_2.SetXYZ(-999, -999, -999);

		// reconstructed leptons
		KLepton* recoParticle1 = product.m_flavourOrderedLeptons.at(0);
		KLepton* recoParticle2 = product.m_flavourOrderedLeptons.at(1);
		KTau* recoTau1 = static_cast<KTau*>(recoParticle1);
		KTau* recoTau2 = static_cast<KTau*>(recoParticle2);
		KLepton* chargedPart1  = product.m_chargeOrderedLeptons.at(0);
		KLepton* chargedPart2  = product.m_chargeOrderedLeptons.at(1);
		KTrack trackP = chargedPart1->track; // in case of tau_h, the track of the lead. prong is saved in the KTau track member
		KTrack trackM = chargedPart2->track;
		RMFLV momentumP = ((chargedPart1->flavour() == KLeptonFlavour::TAU) ? static_cast<KTau*>(chargedPart1)->chargedHadronCandidates.at(0).p4 : chargedPart1->p4);
		RMFLV momentumM = ((chargedPart2->flavour() == KLeptonFlavour::TAU) ? static_cast<KTau*>(chargedPart2)->chargedHadronCandidates.at(0).p4 : chargedPart2->p4);

		int gen_match_1 = product.m_flavourOrderedGenMatch.at(0);
		int gen_match_2 = product.m_flavourOrderedGenMatch.at(1);

		// Defining CPQuantities object to use variables and functions of this class
		CPQuantities cpq;
		ImpactParameter ip;
		if (product.m_refitPV != nullptr){
			if ( product.m_decayChannel == HttEnumTypes::DecayChannel::MT ){
				product.m_isomapIPHelrPV_1 = CalibrateIPHelrPV(product.m_recoIPHelrPV_1, gen_match_1, true);
				product.m_isomapIPHelrPVBS_1 = CalibrateIPHelrPVBS(product.m_recoIPHelrPVBS_1, gen_match_1, true);
				if (recoTau2->decayMode == 0) {
					product.m_isomapIPHelrPV_2 = CalibrateIPHelrPV(product.m_recoIPHelrPV_2, gen_match_2, false);
					product.m_isomapIPHelrPVBS_2 = CalibrateIPHelrPVBS(product.m_recoIPHelrPVBS_2, gen_match_2, false);
				} else {
					product.m_isomapIPHelrPV_2 = product.m_recoIPHelrPV_2;
					product.m_isomapIPHelrPVBS_2 = product.m_recoIPHelrPVBS_2;
				}
			} else if ( product.m_decayChannel == HttEnumTypes::DecayChannel::TT ) {
				if (recoTau1->decayMode == 0) {
					product.m_isomapIPHelrPV_1 = CalibrateIPHelrPV(product.m_recoIPHelrPV_1, gen_match_1, false);
					product.m_isomapIPHelrPVBS_1 = CalibrateIPHelrPVBS(product.m_recoIPHelrPVBS_1, gen_match_1, false);
				} else {
					product.m_isomapIPHelrPV_1 = product.m_recoIPHelrPV_1;
					product.m_isomapIPHelrPVBS_1 = product.m_recoIPHelrPVBS_1;
				}
				if (recoTau2->decayMode == 0) {
					product.m_isomapIPHelrPV_2 = CalibrateIPHelrPV(product.m_recoIPHelrPV_2, gen_match_2, false);
					product.m_isomapIPHelrPVBS_2 = CalibrateIPHelrPVBS(product.m_recoIPHelrPVBS_2, gen_match_2, false);
				} else {
					product.m_isomapIPHelrPV_2 = product.m_recoIPHelrPV_2;
					product.m_isomapIPHelrPVBS_2 = product.m_recoIPHelrPVBS_2;
				}
			}

			if (recoParticle1->getHash() == chargedPart1->getHash()){
				IPPlusHelrPV  = product.m_isomapIPHelrPV_1;
				IPMinusHelrPV = product.m_isomapIPHelrPV_2;
				IPPlusHelrPVBS  = product.m_isomapIPHelrPVBS_1;
				IPMinusHelrPVBS = product.m_isomapIPHelrPVBS_2;
			} else {
				IPPlusHelrPV  = product.m_isomapIPHelrPV_2;
				IPMinusHelrPV = product.m_isomapIPHelrPV_1;
				IPPlusHelrPVBS  = product.m_isomapIPHelrPVBS_2;
				IPMinusHelrPVBS = product.m_isomapIPHelrPVBS_1;
			}
			product.m_isomapPhiStarCPHelrPV = cpq.CalculatePhiStarCP(momentumP, momentumM, IPPlusHelrPV, IPMinusHelrPV, "reco");
			product.m_isomapPhiStarCPHelrPVBS = cpq.CalculatePhiStarCP(momentumP, momentumM, IPPlusHelrPVBS, IPMinusHelrPVBS, "reco");

			// ---------
			// comb-method - with refitted PV
			// ---------
			if ( (product.m_decayChannel == HttEnumTypes::DecayChannel::MT || product.m_decayChannel == HttEnumTypes::DecayChannel::ET) && recoTau2->decayMode == 1){
				KTau* recoTau2 = static_cast<KTau*>(recoParticle2);

				product.m_isomapPhiStarCPCombHelrPV   = cpq.CalculatePhiStarCPComb(product.m_isomapIPHelrPV_1, recoParticle1->p4, recoTau2->chargedHadronCandidates.at(0).p4, recoTau2->piZeroMomentum(), recoParticle1->charge());
				product.m_isomapPhiStarCPCombHelrPVBS = cpq.CalculatePhiStarCPComb(product.m_isomapIPHelrPVBS_1, recoParticle1->p4, recoTau2->chargedHadronCandidates.at(0).p4, recoTau2->piZeroMomentum(), recoParticle1->charge());

				product.m_isomapPhiStarCPCombMergedHelrPV   = cpq.MergePhiStarCPCombSemiLeptonic(product.m_isomapPhiStarCPCombHelrPV, recoTau2, product.m_reco_posyTauL, product.m_reco_negyTauL);
				product.m_isomapPhiStarCPCombMergedHelrPVBS = cpq.MergePhiStarCPCombSemiLeptonic(product.m_isomapPhiStarCPCombHelrPVBS, recoTau2, product.m_reco_posyTauL, product.m_reco_negyTauL);
			}
			if ( product.m_decayChannel == HttEnumTypes::DecayChannel::TT ){
				// tau1->rho, tau2->a
				if (recoTau1->decayMode == 1 && recoTau2->decayMode != 1) {
					product.m_isomapPhiStarCPCombHelrPV   = cpq.CalculatePhiStarCPComb(product.m_isomapIPHelrPV_2, recoParticle2->p4, recoTau1->chargedHadronCandidates.at(0).p4, recoTau1->piZeroMomentum(), recoParticle2->charge());
					product.m_isomapPhiStarCPCombHelrPVBS = cpq.CalculatePhiStarCPComb(product.m_isomapIPHelrPVBS_2, recoParticle2->p4, recoTau1->chargedHadronCandidates.at(0).p4, recoTau1->piZeroMomentum(), recoParticle2->charge());

					product.m_isomapPhiStarCPCombMergedHelrPV   = cpq.MergePhiStarCPCombFullyHadronic(product.m_isomapPhiStarCPCombHelrPV, recoTau1, recoTau2, product.m_reco_posyTauL, product.m_reco_negyTauL);
					product.m_isomapPhiStarCPCombMergedHelrPVBS = cpq.MergePhiStarCPCombFullyHadronic(product.m_isomapPhiStarCPCombHelrPVBS, recoTau1, recoTau2, product.m_reco_posyTauL, product.m_reco_negyTauL);
				}
				// tau1->a, tau2->rho
				if (recoTau1->decayMode != 1 && recoTau2->decayMode ==1){
					product.m_isomapPhiStarCPCombHelrPV   = cpq.CalculatePhiStarCPComb(product.m_isomapIPHelrPV_1, recoParticle1->p4, recoTau2->chargedHadronCandidates.at(0).p4, recoTau2->piZeroMomentum(), recoParticle1->charge());
					product.m_isomapPhiStarCPCombHelrPVBS = cpq.CalculatePhiStarCPComb(product.m_isomapIPHelrPVBS_1, recoParticle1->p4, recoTau2->chargedHadronCandidates.at(0).p4, recoTau2->piZeroMomentum(), recoParticle1->charge());

					product.m_isomapPhiStarCPCombMergedHelrPV   = cpq.MergePhiStarCPCombFullyHadronic(product.m_isomapPhiStarCPCombHelrPV, recoTau1, recoTau2, product.m_reco_posyTauL, product.m_reco_negyTauL);
					product.m_isomapPhiStarCPCombMergedHelrPVBS = cpq.MergePhiStarCPCombFullyHadronic(product.m_isomapPhiStarCPCombHelrPVBS, recoTau1, recoTau2, product.m_reco_posyTauL, product.m_reco_negyTauL);
				}

			}  // if tt ch.
		} // if refitPV exists
	} // is not data
	else{
		product.m_isomapIPHelrPV_1 = product.m_recoIPHelrPV_1;
		product.m_isomapIPHelrPV_2 = product.m_recoIPHelrPV_2;
		product.m_isomapIPHelrPVBS_1 = product.m_recoIPHelrPVBS_1;
		product.m_isomapIPHelrPVBS_2 = product.m_recoIPHelrPVBS_2;

		product.m_isomapPhiStarCPHelrPV             = product.m_recoPhiStarCPHelrPV;
		product.m_isomapPhiStarCPHelrPVBS           = product.m_recoPhiStarCPHelrPVBS;
		product.m_isomapPhiStarCPCombHelrPV         = product.m_recoPhiStarCPCombHelrPV;
		product.m_isomapPhiStarCPCombMergedHelrPV   = product.m_recoPhiStarCPCombMergedHelrPV;
		product.m_isomapPhiStarCPCombHelrPVBS       = product.m_recoPhiStarCPCombHelrPVBS;
		product.m_isomapPhiStarCPCombMergedHelrPVBS = product.m_recoPhiStarCPCombMergedHelrPVBS;
	} // is data
}
