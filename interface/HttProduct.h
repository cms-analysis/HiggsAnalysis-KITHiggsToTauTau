
#pragma once

#include <map>
#include <string>

#include "Artus/KappaAnalysis/interface/KappaProduct.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttComputedObjects.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Utility/SvfitTools.h"


class HttProduct : public KappaProduct
{
public:

	enum class DecayChannel : int
	{
		NONE = -1,
		TT   = 0,
		MT   = 1,
		ET   = 2,
		EM   = 3,
		MM   = 4,
		EE   = 5
	};
	static DecayChannel ToDecayChannel(std::string const& decayChannelString)
	{
		if (decayChannelString == "TT") return DecayChannel::TT;
		else if (decayChannelString == "MT") return DecayChannel::MT;
		else if (decayChannelString == "ET") return DecayChannel::ET;
		else if (decayChannelString == "EM") return DecayChannel::EM;
		else if (decayChannelString == "MM") return DecayChannel::MM;
		else if (decayChannelString == "EE") return DecayChannel::EE;
		return DecayChannel::NONE;
	}

	// TODO: to be extended
	enum class EventCategory : int
	{
		NONE      = -1,
		INCLUSIVE = 0,
		ZERO_JET  = 1,
		BOOST     = 2,
		VBF       = 3
	};
	static EventCategory ToEventCategory(std::string const& eventCategoryString)
	{
		if (eventCategoryString == "INCLUSIVE") return EventCategory::INCLUSIVE;
		else if (eventCategoryString == "ZERO_JET") return EventCategory::ZERO_JET;
		else if (eventCategoryString == "BOOST") return EventCategory::BOOST;
		else if (eventCategoryString == "VBF") return EventCategory::VBF;
		return EventCategory::NONE;
	}

	DecayChannel m_decayChannel;
	std::vector<EventCategory> m_eventCategories;
	
	// filled by DecayChannelProducer
	std::vector<KLepton*> m_ptOrderedLeptons; // highest pt leptons first
	std::vector<KLepton*> m_flavourOrderedLeptons; // according to channel definition
	std::vector<KLepton*> m_chargeOrderedLeptons; // positively charged leptons first

	// filled by HttValid<Leptons>Producer
	std::map<KLepton*, double> m_leptonIsolation;
	std::map<KLepton*, double> m_leptonIsolationOverPt;
	
	// filled by the DiLeptonQuantitiesProducer
	RMDataLV m_diLeptonSystem;
	RMDataLV m_diLeptonPlusMetSystem;
	
	// filled by the DiLeptonQuantitiesProducer (collinear approximation)
	std::vector<RMDataLV> m_flavourOrderedTauMomentaCA;
	RMDataLV m_diTauSystemCA;
	bool m_validCollinearApproximation = false;
	
	// filled by the SvfitProducer
	mutable RunLumiEvent m_runLumiEvent;
	mutable SvfitInputs m_svfitInputs;
	mutable SvfitResults m_svfitResults;
	bool m_svfitCalculated = false;
	
	// filled by the DiJetQuantitiesProducer
	RMLV m_diJetSystem;
	bool m_diJetSystemAvailable = false;
	
	KDataPFMET* m_met = 0;
	
	// filled by the TauTauRestFrameProducer
	std::vector<RMDataLV> m_flavourOrderedTauMomenta;
	std::vector<ROOT::Math::Boost> m_boostsToTauRestFrames;
	bool m_tauMomentaReconstructed = false;
	RMDataLV m_diTauSystem;
	ROOT::Math::Boost m_boostToDiTauRestFrame;
	bool m_diTauSystemReconstructed = false;

	double m_genMassRoundOff1;
	double m_genMassRoundOff2;

	// filled by GenTauCPProducer
	double m_genPhi;
	double m_genPhiStarCP;
	std::pair <double,double> m_genChargedProngEnergies;
	std::pair <double,double> m_genChargedPionEnergiesApprox;
	double m_genThetaNuHadron;
	double m_genAlphaTauNeutrinos;
	double m_genPhiDet;
	double m_genPhiStarCPDet;

	// filled by RecoTauCPProducer
	double m_recoPhiStarCP;

	KGenParticle* m_genOneProngCharged1 = 0;
	KGenParticle* m_genOneProngCharged2 = 0;

};
