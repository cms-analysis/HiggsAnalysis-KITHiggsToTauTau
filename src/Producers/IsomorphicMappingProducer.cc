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
		m_emb = "_emb";
	}

	std::string ipHelrPV_r_prompt_str;
	std::string ipHelrPV_phi_prompt_str;
	std::string ipHelrPV_theta_prompt_str;
	std::string ipHelrPVBS_r_prompt_str;
	std::string ipHelrPVBS_phi_prompt_str;
	std::string ipHelrPVBS_theta_prompt_str;

	std::string ipHelrPV_r_muon_str;
	std::string ipHelrPV_phi_muon_str;
	std::string ipHelrPV_theta_muon_str;
	std::string ipHelrPVBS_r_muon_str;
	std::string ipHelrPVBS_phi_muon_str;
	std::string ipHelrPVBS_theta_muon_str;

	std::string ipHelrPV_r_pion_str;
	std::string ipHelrPV_phi_pion_str;
	std::string ipHelrPV_theta_pion_str;
	std::string ipHelrPVBS_r_pion_str;
	std::string ipHelrPVBS_phi_pion_str;
	std::string ipHelrPVBS_theta_pion_str;



	// Calibration Curves for prompt decays (calibration done in Z->mumu)
	ipHelrPV_r_prompt_str     = std::string("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/isomap/prompt/calib_zmm" + m_year + m_emb + "/ip_mag.root");
	ipHelrPV_phi_prompt_str   = std::string("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/isomap/prompt/calib_zmm" + m_year + m_emb + "/ip_phi.root");
	ipHelrPV_theta_prompt_str = std::string("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/isomap/prompt/calib_zmm" + m_year + m_emb + "/ip_theta.root");

	ipHelrPVBS_r_prompt_str     = std::string("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/isomap/prompt/calib_zmm" + m_year + m_emb + "/ip_bs_mag.root");
	ipHelrPVBS_phi_prompt_str   = std::string("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/isomap/prompt/calib_zmm" + m_year + m_emb + "/ip_bs_phi.root");
	ipHelrPVBS_theta_prompt_str = std::string("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/isomap/prompt/calib_zmm" + m_year + m_emb + "/ip_bs_theta.root");

	// Calibration curves for non prompt decays
	// tau->muon
	ipHelrPV_r_muon_str     = std::string("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/isomap/muon/calib" + m_year + m_emb + "/ip_mag.root");
	ipHelrPV_phi_muon_str   = std::string("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/isomap/muon/calib" + m_year + m_emb + "/ip_phi.root");
	ipHelrPV_theta_muon_str = std::string("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/isomap/muon/calib" + m_year + m_emb + "/ip_theta.root");
	ipHelrPVBS_r_muon_str     = std::string("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/isomap/muon/calib" + m_year + m_emb + "/ip_bs_mag.root");
	ipHelrPVBS_phi_muon_str   = std::string("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/isomap/muon/calib" + m_year + m_emb + "/ip_bs_phi.root");
	ipHelrPVBS_theta_muon_str = std::string("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/isomap/muon/calib" + m_year + m_emb + "/ip_bs_theta.root");
	// tau->pion
	ipHelrPV_r_pion_str     = std::string("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/isomap/pion/calib" + m_year + m_emb + "/ip_mag.root");
	ipHelrPV_phi_pion_str   = std::string("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/isomap/pion/calib" + m_year + m_emb + "/ip_phi.root");
	ipHelrPV_theta_pion_str = std::string("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/isomap/pion/calib" + m_year + m_emb + "/ip_theta.root");
	ipHelrPVBS_r_pion_str     = std::string("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/isomap/pion/calib" + m_year + m_emb + "/ip_bs_mag.root");
	ipHelrPVBS_phi_pion_str   = std::string("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/isomap/pion/calib" + m_year + m_emb + "/ip_bs_phi.root");
	ipHelrPVBS_theta_pion_str = std::string("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/isomap/pion/calib" + m_year + m_emb + "/ip_bs_theta.root");

	// Prompt Decays
	// refit PV
	TFile inputFile_ipHelrPV_prompt_r(ipHelrPV_r_prompt_str.c_str(), "READ");
	m_ipHelrPV_r_prompt_isomap = static_cast<TGraph*>(inputFile_ipHelrPV_prompt_r.Get("isomap"));
	inputFile_ipHelrPV_prompt_r.Close();

	TFile inputFile_ipHelrPV_prompt_theta(ipHelrPV_theta_prompt_str.c_str(), "READ");
	m_ipHelrPV_theta_prompt_isomap = static_cast<TGraph*>(inputFile_ipHelrPV_prompt_theta.Get("isomap"));
	inputFile_ipHelrPV_prompt_theta.Close();

	TFile inputFile_ipHelrPV_prompt_phi(ipHelrPV_phi_prompt_str.c_str(), "READ");
	m_ipHelrPV_phi_prompt_isomap = static_cast<TGraph*>(inputFile_ipHelrPV_prompt_phi.Get("isomap"));
	inputFile_ipHelrPV_prompt_phi.Close();
	// refit PV with BS
	TFile inputFile_ipHelrPVBS_prompt_r(ipHelrPVBS_r_prompt_str.c_str(), "READ");
	m_ipHelrPVBS_r_prompt_isomap = static_cast<TGraph*>(inputFile_ipHelrPVBS_prompt_r.Get("isomap"));
	inputFile_ipHelrPVBS_prompt_r.Close();

	TFile inputFile_ipHelrPVBS_prompt_theta(ipHelrPVBS_theta_prompt_str.c_str(), "READ");
	m_ipHelrPVBS_theta_prompt_isomap = static_cast<TGraph*>(inputFile_ipHelrPVBS_prompt_theta.Get("isomap"));
	inputFile_ipHelrPVBS_prompt_theta.Close();

	TFile inputFile_ipHelrPVBS_prompt_phi(ipHelrPVBS_phi_prompt_str.c_str(), "READ");
	m_ipHelrPVBS_phi_prompt_isomap = static_cast<TGraph*>(inputFile_ipHelrPVBS_prompt_phi.Get("isomap"));
	inputFile_ipHelrPVBS_prompt_phi.Close();

	// Nonprompt decays
	// tau->muon
	// refit PV
	TFile inputFile_ipHelrPV_muon_r(ipHelrPV_r_muon_str.c_str(), "READ");
	m_ipHelrPV_r_muon_isomap = static_cast<TGraph*>(inputFile_ipHelrPV_muon_r.Get("isomap"));
	inputFile_ipHelrPV_muon_r.Close();

	TFile inputFile_ipHelrPV_muon_theta(ipHelrPV_theta_muon_str.c_str(), "READ");
	m_ipHelrPV_theta_muon_isomap = static_cast<TGraph*>(inputFile_ipHelrPV_muon_theta.Get("isomap"));
	inputFile_ipHelrPV_muon_theta.Close();

	TFile inputFile_ipHelrPV_muon_phi(ipHelrPV_phi_muon_str.c_str(), "READ");
	m_ipHelrPV_phi_muon_isomap = static_cast<TGraph*>(inputFile_ipHelrPV_muon_phi.Get("isomap"));
	inputFile_ipHelrPV_muon_phi.Close();
	// refit PV with BS
	TFile inputFile_ipHelrPVBS_muon_r(ipHelrPVBS_r_muon_str.c_str(), "READ");
	m_ipHelrPVBS_r_muon_isomap = static_cast<TGraph*>(inputFile_ipHelrPVBS_muon_r.Get("isomap"));
	inputFile_ipHelrPVBS_muon_r.Close();

	TFile inputFile_ipHelrPVBS_muon_theta(ipHelrPVBS_theta_muon_str.c_str(), "READ");
	m_ipHelrPVBS_theta_muon_isomap = static_cast<TGraph*>(inputFile_ipHelrPVBS_muon_theta.Get("isomap"));
	inputFile_ipHelrPVBS_muon_theta.Close();

	TFile inputFile_ipHelrPVBS_muon_phi(ipHelrPVBS_phi_muon_str.c_str(), "READ");
	m_ipHelrPVBS_phi_muon_isomap = static_cast<TGraph*>(inputFile_ipHelrPVBS_muon_phi.Get("isomap"));
	inputFile_ipHelrPVBS_muon_phi.Close();
	// tau->pion
	// refit PV
	TFile inputFile_ipHelrPV_pion_r(ipHelrPV_r_pion_str.c_str(), "READ");
	m_ipHelrPV_r_pion_isomap = static_cast<TGraph*>(inputFile_ipHelrPV_pion_r.Get("isomap"));
	inputFile_ipHelrPV_pion_r.Close();

	TFile inputFile_ipHelrPV_pion_theta(ipHelrPV_theta_pion_str.c_str(), "READ");
	m_ipHelrPV_theta_pion_isomap = static_cast<TGraph*>(inputFile_ipHelrPV_pion_theta.Get("isomap"));
	inputFile_ipHelrPV_pion_theta.Close();

	TFile inputFile_ipHelrPV_pion_phi(ipHelrPV_phi_pion_str.c_str(), "READ");
	m_ipHelrPV_phi_pion_isomap = static_cast<TGraph*>(inputFile_ipHelrPV_pion_phi.Get("isomap"));
	inputFile_ipHelrPV_pion_phi.Close();
	// refit PV with BS
	TFile inputFile_ipHelrPVBS_pion_r(ipHelrPVBS_r_pion_str.c_str(), "READ");
	m_ipHelrPVBS_r_pion_isomap = static_cast<TGraph*>(inputFile_ipHelrPVBS_pion_r.Get("isomap"));
	inputFile_ipHelrPVBS_pion_r.Close();

	TFile inputFile_ipHelrPVBS_pion_theta(ipHelrPVBS_theta_pion_str.c_str(), "READ");
	m_ipHelrPVBS_theta_pion_isomap = static_cast<TGraph*>(inputFile_ipHelrPVBS_pion_theta.Get("isomap"));
	inputFile_ipHelrPVBS_pion_theta.Close();

	TFile inputFile_ipHelrPVBS_pion_phi(ipHelrPVBS_phi_pion_str.c_str(), "READ");
	m_ipHelrPVBS_phi_pion_isomap = static_cast<TGraph*>(inputFile_ipHelrPVBS_pion_phi.Get("isomap"));
	inputFile_ipHelrPVBS_pion_phi.Close();

	gDirectory = savedir;
	gFile = savefile;

	LambdaNtupleConsumer<HttTypes>::AddRMPointQuantity(metadata, "calibIPHelrPV_1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return (((product.m_calibIPHelrPV_1).x() != -999) ? RMPoint( (product.m_calibIPHelrPV_1).x(), (product.m_calibIPHelrPV_1).y(), (product.m_calibIPHelrPV_1).z() ) : DefaultValues::UndefinedRMPoint);
	});
	LambdaNtupleConsumer<HttTypes>::AddRMPointQuantity(metadata, "calibIPHelrPV_2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return (((product.m_calibIPHelrPV_2).x() != -999) ? RMPoint( (product.m_calibIPHelrPV_2).x(), (product.m_calibIPHelrPV_2).y(), (product.m_calibIPHelrPV_2).z() ) : DefaultValues::UndefinedRMPoint);
	});

	LambdaNtupleConsumer<HttTypes>::AddRMPointQuantity(metadata, "calibIPHelrPVBS_1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return (((product.m_calibIPHelrPVBS_1).x() != -999) ? RMPoint( (product.m_calibIPHelrPVBS_1).x(), (product.m_calibIPHelrPVBS_1).y(), (product.m_calibIPHelrPVBS_1).z() ) : DefaultValues::UndefinedRMPoint);
	});
	LambdaNtupleConsumer<HttTypes>::AddRMPointQuantity(metadata, "calibIPHelrPVBS_2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return (((product.m_calibIPHelrPVBS_2).x() != -999) ? RMPoint( (product.m_calibIPHelrPVBS_2).x(), (product.m_calibIPHelrPVBS_2).y(), (product.m_calibIPHelrPVBS_2).z() ) : DefaultValues::UndefinedRMPoint);
	});

	// CP-related quantities
	// IP-Method
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "calibPhiStarCPHelrPV", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_calibPhiStarCPHelrPV;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "calibPhiStarCPHelrPVBS", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_calibPhiStarCPHelrPVBS;
	});
	// Combined Method
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "calibPhiStarCPCombHelrPV", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_calibPhiStarCPCombHelrPV;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "calibPhiStarCPCombMergedHelrPV", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_calibPhiStarCPCombMergedHelrPV;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "calibPhiStarCPCombHelrPVBS", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_calibPhiStarCPCombHelrPVBS;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "calibPhiStarCPCombMergedHelrPVBS", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_calibPhiStarCPCombMergedHelrPVBS;
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

		product.m_calibIPHelrPV_1.SetXYZ(-999, -999, -999);
		product.m_calibIPHelrPV_2.SetXYZ(-999, -999, -999);
		product.m_calibIPHelrPVBS_1.SetXYZ(-999, -999, -999);
		product.m_calibIPHelrPVBS_2.SetXYZ(-999, -999, -999);

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
		int gen_match_2 = product.m_flavourOrderedGenMatch.at(0);

		// Defining CPQuantities object to use variables and functions of this class
		CPQuantities cpq;
		ImpactParameter ip;
		if (product.m_refitPV != nullptr){
			if ( product.m_decayChannel == HttEnumTypes::DecayChannel::MT ){
				product.m_calibIPHelrPV_1 = CalibrateIPHelrPV(product.m_recoIPHelrPV_1, gen_match_1, true);
				product.m_calibIPHelrPVBS_1 = CalibrateIPHelrPVBS(product.m_recoIPHelrPVBS_1, gen_match_1, true);
				if (recoTau2->decayMode == 0) {
					product.m_calibIPHelrPV_2 = CalibrateIPHelrPV(product.m_recoIPHelrPV_2, gen_match_2, false);
					product.m_calibIPHelrPVBS_2 = CalibrateIPHelrPVBS(product.m_recoIPHelrPVBS_2, gen_match_2, false);
				} else {
					product.m_calibIPHelrPV_2 = product.m_recoIPHelrPV_2;
					product.m_calibIPHelrPVBS_2 = product.m_recoIPHelrPVBS_2;
				}
			} else if ( product.m_decayChannel == HttEnumTypes::DecayChannel::TT ) {
				if (recoTau1->decayMode == 0) {
					product.m_calibIPHelrPV_1 = CalibrateIPHelrPV(product.m_recoIPHelrPV_1, gen_match_1, false);
					product.m_calibIPHelrPVBS_1 = CalibrateIPHelrPVBS(product.m_recoIPHelrPVBS_1, gen_match_1, false);
				} else {
					product.m_calibIPHelrPV_1 = product.m_recoIPHelrPV_1;
					product.m_calibIPHelrPVBS_1 = product.m_recoIPHelrPVBS_1;
				}
				if (recoTau2->decayMode == 0) {
					product.m_calibIPHelrPV_2 = CalibrateIPHelrPV(product.m_recoIPHelrPV_2, gen_match_2, false);
					product.m_calibIPHelrPVBS_2 = CalibrateIPHelrPVBS(product.m_recoIPHelrPVBS_2, gen_match_2, false);
				} else {
					product.m_calibIPHelrPV_2 = product.m_recoIPHelrPV_2;
					product.m_calibIPHelrPVBS_2 = product.m_recoIPHelrPVBS_2;
				}
			}

			if (recoParticle1->getHash() == chargedPart1->getHash()){
				IPPlusHelrPV  = product.m_calibIPHelrPV_1;
				IPMinusHelrPV = product.m_calibIPHelrPV_2;
				IPPlusHelrPVBS  = product.m_calibIPHelrPVBS_1;
				IPMinusHelrPVBS = product.m_calibIPHelrPVBS_2;
			} else {
				IPPlusHelrPV  = product.m_calibIPHelrPV_2;
				IPMinusHelrPV = product.m_calibIPHelrPV_1;
				IPPlusHelrPVBS  = product.m_calibIPHelrPVBS_2;
				IPMinusHelrPVBS = product.m_calibIPHelrPVBS_1;
			}
			product.m_calibPhiStarCPHelrPV = cpq.CalculatePhiStarCP(momentumP, momentumM, IPPlusHelrPV, IPMinusHelrPV, "reco");
			product.m_calibPhiStarCPHelrPVBS = cpq.CalculatePhiStarCP(momentumP, momentumM, IPPlusHelrPVBS, IPMinusHelrPVBS, "reco");

			// ---------
			// comb-method - with refitted PV
			// ---------
			if ( product.m_decayChannel == HttEnumTypes::DecayChannel::MT || product.m_decayChannel == HttEnumTypes::DecayChannel::ET || recoTau2->decayMode == 1){
				KTau* recoTau2 = static_cast<KTau*>(recoParticle2);

				product.m_calibPhiStarCPCombHelrPV   = cpq.CalculatePhiStarCPComb(product.m_calibIPHelrPV_1, recoParticle1->p4, recoTau2->chargedHadronCandidates.at(0).p4, recoTau2->piZeroMomentum(), recoParticle1->charge());
				product.m_calibPhiStarCPCombHelrPVBS = cpq.CalculatePhiStarCPComb(product.m_calibIPHelrPVBS_1, recoParticle1->p4, recoTau2->chargedHadronCandidates.at(0).p4, recoTau2->piZeroMomentum(), recoParticle1->charge());

				product.m_calibPhiStarCPCombMergedHelrPV   = cpq.MergePhiStarCPCombSemiLeptonic(product.m_calibPhiStarCPCombHelrPV, recoTau2, product.m_reco_posyTauL, product.m_reco_negyTauL);
				product.m_calibPhiStarCPCombMergedHelrPVBS = cpq.MergePhiStarCPCombSemiLeptonic(product.m_calibPhiStarCPCombHelrPVBS, recoTau2, product.m_reco_posyTauL, product.m_reco_negyTauL);
			}
			if ( product.m_decayChannel == HttEnumTypes::DecayChannel::TT ){
				// tau1->rho, tau2->a
				if (recoTau1->decayMode == 1 && recoTau2->decayMode != 1) {
					product.m_calibPhiStarCPCombHelrPV   = cpq.CalculatePhiStarCPComb(product.m_calibIPHelrPV_2, recoParticle2->p4, recoTau1->chargedHadronCandidates.at(0).p4, recoTau1->piZeroMomentum(), recoParticle2->charge());
					product.m_calibPhiStarCPCombHelrPVBS = cpq.CalculatePhiStarCPComb(product.m_calibIPHelrPVBS_2, recoParticle2->p4, recoTau1->chargedHadronCandidates.at(0).p4, recoTau1->piZeroMomentum(), recoParticle2->charge());

					product.m_calibPhiStarCPCombMergedHelrPV   = cpq.MergePhiStarCPCombFullyHadronic(product.m_calibPhiStarCPCombHelrPV, recoTau1, recoTau2, product.m_reco_posyTauL, product.m_reco_negyTauL);
					product.m_calibPhiStarCPCombMergedHelrPVBS = cpq.MergePhiStarCPCombFullyHadronic(product.m_calibPhiStarCPCombHelrPVBS, recoTau1, recoTau2, product.m_reco_posyTauL, product.m_reco_negyTauL);
				}
				// tau1->a, tau2->rho
				if (recoTau1->decayMode != 1 && recoTau2->decayMode ==1){
					product.m_calibPhiStarCPCombHelrPV   = cpq.CalculatePhiStarCPComb(product.m_calibIPHelrPV_1, recoParticle1->p4, recoTau2->chargedHadronCandidates.at(0).p4, recoTau2->piZeroMomentum(), recoParticle1->charge());
					product.m_calibPhiStarCPCombHelrPVBS = cpq.CalculatePhiStarCPComb(product.m_calibIPHelrPVBS_1, recoParticle1->p4, recoTau2->chargedHadronCandidates.at(0).p4, recoTau2->piZeroMomentum(), recoParticle1->charge());

					product.m_calibPhiStarCPCombMergedHelrPV   = cpq.MergePhiStarCPCombFullyHadronic(product.m_calibPhiStarCPCombHelrPV, recoTau1, recoTau2, product.m_reco_posyTauL, product.m_reco_negyTauL);
					product.m_calibPhiStarCPCombMergedHelrPVBS = cpq.MergePhiStarCPCombFullyHadronic(product.m_calibPhiStarCPCombHelrPVBS, recoTau1, recoTau2, product.m_reco_posyTauL, product.m_reco_negyTauL);
				}

			}  // if tt ch.
		} // if refitPV exists
	} // is not data
	else{
		product.m_calibIPHelrPV_1 = product.m_recoIPHelrPV_1;
		product.m_calibIPHelrPV_2 = product.m_recoIPHelrPV_2;
		product.m_calibIPHelrPVBS_1 = product.m_recoIPHelrPVBS_1;
		product.m_calibIPHelrPVBS_2 = product.m_recoIPHelrPVBS_2;

		product.m_calibPhiStarCPHelrPV             = product.m_recoPhiStarCPHelrPV;
		product.m_calibPhiStarCPHelrPVBS           = product.m_recoPhiStarCPHelrPVBS;
		product.m_calibPhiStarCPCombHelrPV         = product.m_recoPhiStarCPCombHelrPV;
		product.m_calibPhiStarCPCombMergedHelrPV   = product.m_recoPhiStarCPCombMergedHelrPV;
		product.m_calibPhiStarCPCombHelrPVBS       = product.m_recoPhiStarCPCombHelrPVBS;
		product.m_calibPhiStarCPCombMergedHelrPVBS = product.m_recoPhiStarCPCombMergedHelrPVBS;
	} // is data
}
