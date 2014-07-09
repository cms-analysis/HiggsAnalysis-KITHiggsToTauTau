
#pragma once

#include <map>
#include <string>

#include "Artus/KappaAnalysis/interface/KappaProduct.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttEnumTypes.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttComputedObjects.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Utility/SvfitTools.h"


class HttProduct : public KappaProduct
{
public:

	HttEnumTypes::DecayChannel m_decayChannel;
	std::vector<HttEnumTypes::EventCategory> m_eventCategories;
	
	// TODO: To be set by producers that apply shifts
	HttEnumTypes::SystematicShift m_systematicShift = HttEnumTypes::SystematicShift::CENTRAL;
	float m_systematicShiftSigma = 0.0;
	
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
	mutable SvfitEventKey m_svfitEventKey;
	mutable SvfitInputs m_svfitInputs;
	mutable SvfitResults m_svfitResults;
	bool m_svfitCalculated = false;
	
	// filled by the DiJetQuantitiesProducer
	RMLV m_diJetSystem;
	bool m_diJetSystemAvailable = false;
	
	KDataPFMET* m_met = 0;
	
	// filled by the TauTauRestFrameProducer
	HttEnumTypes::TauTauRestFrameReco m_tauTauRestFrameReco = HttEnumTypes::TauTauRestFrameReco::NONE;
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
