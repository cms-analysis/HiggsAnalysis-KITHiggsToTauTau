#include <boost/algorithm/string.hpp>

#include "Artus/Consumer/interface/LambdaNtupleConsumer.h"
#include "Artus/KappaAnalysis/interface/KappaTypes.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttEnumTypes.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Utility/CPQuantities.h"
#include "HiggsCPinTauDecays/ImpactParameter/interface/ImpactParameter.h"
#include "HiggsCPinTauDecays/IpCorrection/interface/IpCorrection.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/QuantileMappingProducer.h"
#include <TString.h>

#include <fstream>

std::string QuantileMappingProducer::GetProducerId() const
{
	return "QuantileMappingProducer";
}

void QuantileMappingProducer::Init(setting_type const& settings, metadata_type& metadata)
{
	ProducerBase<HttTypes>::Init(settings, metadata);
	m_isData = settings.GetInputIsData();
	m_isEmbedding = settings.GetInputIsEmbedding();

	m_year = std::to_string(settings.GetYear());

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
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "calibPhiStarCPHelrPVBS", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_calibPhiStarCPHelrPVBS;
	});
	// Combined Method
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "calibPhiStarCPCombHelrPVBS", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_calibPhiStarCPCombHelrPVBS;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "calibPhiStarCPCombMergedHelrPVBS", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_calibPhiStarCPCombMergedHelrPVBS;
	});

}

void QuantileMappingProducer::Produce(event_type const& event, product_type& product, setting_type const& settings, metadata_type const& metadata) const
{
	if (!m_isData){
		assert(event.m_vertexSummary);
		assert(product.m_flavourOrderedLeptons.size() >= 2);

		// initialization of TVector3 objects
		TVector3 IPPlusHelrPVBS;
		TVector3 IPMinusHelrPVBS;
		IPPlusHelrPVBS.SetXYZ(-999,-999,-999);
		IPMinusHelrPVBS.SetXYZ(-999,-999,-999);

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
		int gen_match_2 = product.m_flavourOrderedGenMatch.at(1);

		// Defining CPQuantities object to use variables and functions of this class
		CPQuantities cpq;
		ImpactParameter ip;
		TDirectory *savedir(gDirectory);
		TFile *savefile(gFile);
		IpCorrection ipCorrector("$CMSSW_BASE/src/HiggsCPinTauDecays/IpCorrection/data/ip_" + TString(m_year) + ".root");
		gDirectory = savedir;
		gFile = savefile;
		if (product.m_refitPV != nullptr){

			double ipx_corr = ipCorrector.correctIp(IpCorrection::Coordinate::Ipx, product.m_recoIPHelrPVBS_1.X(), product.m_genIP1.X(), recoTau1->p4.Eta());
			double ipy_corr = ipCorrector.correctIp(IpCorrection::Coordinate::Ipy, product.m_recoIPHelrPVBS_1.Y(), product.m_genIP1.Y(), recoTau1->p4.Eta());
			double ipz_corr = ipCorrector.correctIp(IpCorrection::Coordinate::Ipz, product.m_recoIPHelrPVBS_1.Z(), product.m_genIP1.Z(), recoTau1->p4.Eta());
			product.m_calibIPHelrPVBS_1.SetXYZ(ipx_corr, ipy_corr, ipz_corr);

			ipx_corr = ipCorrector.correctIp(IpCorrection::Coordinate::Ipx, product.m_recoIPHelrPVBS_2.X(), product.m_genIP2.X(), recoTau2->p4.Eta());
			ipy_corr = ipCorrector.correctIp(IpCorrection::Coordinate::Ipy, product.m_recoIPHelrPVBS_2.Y(), product.m_genIP2.Y(), recoTau2->p4.Eta());
			ipz_corr = ipCorrector.correctIp(IpCorrection::Coordinate::Ipz, product.m_recoIPHelrPVBS_2.Z(), product.m_genIP2.Z(), recoTau2->p4.Eta());
			product.m_calibIPHelrPVBS_2.SetXYZ(ipx_corr, ipy_corr, ipz_corr);


			if (recoParticle1->getHash() == chargedPart1->getHash()){
				IPPlusHelrPVBS  = product.m_calibIPHelrPVBS_1;
				IPMinusHelrPVBS = product.m_calibIPHelrPVBS_2;
			} else {
				IPPlusHelrPVBS  = product.m_calibIPHelrPVBS_2;
				IPMinusHelrPVBS = product.m_calibIPHelrPVBS_1;
			}
			product.m_calibPhiStarCPHelrPVBS = cpq.CalculatePhiStarCP(momentumP, momentumM, IPPlusHelrPVBS, IPMinusHelrPVBS, "reco");

			// ---------
			// comb-method - with refitted PV
			// ---------
			if ( product.m_decayChannel == HttEnumTypes::DecayChannel::MT || product.m_decayChannel == HttEnumTypes::DecayChannel::ET || recoTau2->decayMode == 1){
				KTau* recoTau2 = static_cast<KTau*>(recoParticle2);

				product.m_calibPhiStarCPCombHelrPVBS = cpq.CalculatePhiStarCPComb(product.m_calibIPHelrPVBS_1, recoParticle1->p4, recoTau2->chargedHadronCandidates.at(0).p4, recoTau2->piZeroMomentum(), recoParticle1->charge());
				product.m_calibPhiStarCPCombMergedHelrPVBS = cpq.MergePhiStarCPCombSemiLeptonic(product.m_calibPhiStarCPCombHelrPVBS, recoTau2, product.m_reco_posyTauL, product.m_reco_negyTauL);
			} // if mt ch.
			if ( product.m_decayChannel == HttEnumTypes::DecayChannel::TT ){
				// tau1->rho, tau2->a
				if (recoTau1->decayMode == 1 && recoTau2->decayMode != 1) {
					product.m_calibPhiStarCPCombHelrPVBS = cpq.CalculatePhiStarCPComb(product.m_calibIPHelrPVBS_2, recoParticle2->p4, recoTau1->chargedHadronCandidates.at(0).p4, recoTau1->piZeroMomentum(), recoParticle2->charge());
					product.m_calibPhiStarCPCombMergedHelrPVBS = cpq.MergePhiStarCPCombFullyHadronic(product.m_calibPhiStarCPCombHelrPVBS, recoTau1, recoTau2, product.m_reco_posyTauL, product.m_reco_negyTauL);
				}
				// tau1->a, tau2->rho
				if (recoTau1->decayMode != 1 && recoTau2->decayMode ==1){
					product.m_calibPhiStarCPCombHelrPVBS = cpq.CalculatePhiStarCPComb(product.m_calibIPHelrPVBS_1, recoParticle1->p4, recoTau2->chargedHadronCandidates.at(0).p4, recoTau2->piZeroMomentum(), recoParticle1->charge());
					product.m_calibPhiStarCPCombMergedHelrPVBS = cpq.MergePhiStarCPCombFullyHadronic(product.m_calibPhiStarCPCombHelrPVBS, recoTau1, recoTau2, product.m_reco_posyTauL, product.m_reco_negyTauL);
				}

			}  // if tt ch.
		} // if refitPV exists
	} // is not data
	else{
		product.m_calibIPHelrPVBS_1 = product.m_recoIPHelrPVBS_1;
		product.m_calibIPHelrPVBS_2 = product.m_recoIPHelrPVBS_2;
		product.m_calibPhiStarCPHelrPVBS           = product.m_recoPhiStarCPHelrPVBS;
		product.m_calibPhiStarCPCombHelrPVBS       = product.m_recoPhiStarCPCombHelrPVBS;
		product.m_calibPhiStarCPCombMergedHelrPVBS = product.m_recoPhiStarCPCombMergedHelrPVBS;
	} // is data
}
