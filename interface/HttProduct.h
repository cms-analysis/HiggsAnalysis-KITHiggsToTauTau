
#pragma once

#include <map>
#include <string>

#include "Artus/KappaAnalysis/interface/KappaProduct.h"

#include "Artus/Utility/interface/DefaultValues.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttEnumTypes.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Utility/SvfitTools.h"


class HttProduct : public KappaProduct
{
public:

	/// added by HttValidLooseElectronsProducer
	std::vector<KDataElectron*> m_validLooseElectrons;
	std::vector<KDataElectron*> m_invalidLooseElectrons;

	/// added by HttValidVetoElectronsProducer
	std::vector<KDataElectron*> m_validVetoElectrons;
	std::vector<KDataElectron*> m_invalidVetoElectrons;

	/// added by HttValidLooseMuonsProducer
	std::vector<KDataMuon*> m_validLooseMuons;
	std::vector<KDataMuon*> m_invalidLooseMuons;

	/// added by HttValidVetoMuonsProducer
	std::vector<KDataMuon*> m_validVetoMuons;
	std::vector<KDataMuon*> m_invalidVetoMuons;

	// filled by DecayChannelProducer
	HttEnumTypes::DecayChannel m_decayChannel;
	
	// filled by EventCategoryProducer
	std::vector<HttEnumTypes::EventCategory> m_eventCategories;
	HttEnumTypes::EventCategory m_exclusiveEventCategory;
	
	// TODO: To be set by producers that apply shifts
	HttEnumTypes::SystematicShift m_systematicShift = HttEnumTypes::SystematicShift::CENTRAL;
	float m_systematicShiftSigma = 0.0;
	
	// filled by DecayChannelProducer
	std::vector<KLepton*> m_ptOrderedLeptons; // highest pt leptons first
	std::vector<KLepton*> m_flavourOrderedLeptons; // according to channel definition
	std::vector<KLepton*> m_chargeOrderedLeptons; // positively charged leptons first
	
	// filled by HttTauEnergyCorrectionProducer
	std::map<KDataPFTau*, double> m_tauEnergyScaleWeight;
	
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

	// filled by TauSpinnerProducer
	bool m_tauSpinnerWeight;


	// filled by GenTauCPProducer
	double m_genPhiCP;
	double m_genPhiStarCP;
	std::pair <double,double> m_genChargedProngEnergies;
	double m_genThetaNuHadron;
	double m_genAlphaTauNeutrinos;
	double m_genPhiDet;
	double m_genPhiStarCPDet;
	KGenParticle* m_genOneProngCharged1 = 0;
	KGenParticle* m_genOneProngCharged2 = 0;
	float m_genABS_n1 = DefaultValues::UndefinedDouble;
	float m_genABS_n2 = DefaultValues::UndefinedDouble;

	// filled by RecoTauCPProducer
	double m_recoPhiStarCP;
	KGenParticle* m_recoChargedParticle1 = 0;
	KGenParticle* m_recoChargedParitcle2 = 0;
	std::pair <double,double> m_recoChargedHadronEnergies;
	float m_recoAbs_n1 = DefaultValues::UndefinedDouble;
	float m_recoAbs_n2 = DefaultValues::UndefinedDouble;
	float m_recoTrackRefError1 = DefaultValues::UndefinedDouble;
	float m_recoTrackRefError2 = DefaultValues::UndefinedDouble;
	
	// MVA outputs
	std::vector<double> m_antiTtbarDiscriminators;

	// filled by HttValidGenTausProducer. Naming scheme like for the reco particles
	std::vector<KDataGenTau*> m_ptOrderedGenTaus;
	std::vector<KDataGenTau*> m_flavourOrderedGenTaus;
	std::vector<KDataGenTau*> m_chargeOrderedGenTaus;
	std::vector<KDataGenTau*> m_validGenTausToElectrons;
	std::vector<KDataGenTau*> m_validGenTausToMuons;
	std::vector<KDataGenTau*> m_validGenTausToTaus;

};
