
#pragma once

#include <map>
#include <string>

#include "Artus/KappaAnalysis/interface/KappaProduct.h"

#include "Artus/Utility/interface/DefaultValues.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttEnumTypes.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Utility/SvfitTools.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Utility/DiTauPair.h"


class HttProduct : public KappaProduct
{
public:

	/// added by HttValidLooseElectronsProducer
	std::vector<KElectron*> m_validLooseElectrons;
	std::vector<KElectron*> m_invalidLooseElectrons;

	/// added by HttValidVetoElectronsProducer
	std::vector<KElectron*> m_validVetoElectrons;
	std::vector<KElectron*> m_invalidVetoElectrons;

	/// added by HttValidLooseMuonsProducer
	std::vector<KMuon*> m_validLooseMuons;
	std::vector<KMuon*> m_invalidLooseMuons;

	/// added by HttValidVetoMuonsProducer
	std::vector<KMuon*> m_validVetoMuons;
	std::vector<KMuon*> m_invalidVetoMuons;
	
	/// added by DiTauPairCandidatesProducers
	std::vector<DiTauPair> m_validDiTauPairCandidates;
	std::vector<DiTauPair> m_invalidDiTauPairCandidates;

	// filled by DecayChannelProducer
	bool m_extraElecVeto = false;
	bool m_extraMuonVeto = false;
	
	// filled by DiLeptonVetoProducers
	int m_nDiElectronVetoPairsOS = 0;
	int m_nDiElectronVetoPairsSS = 0;
	int m_nDiMuonVetoPairsOS = 0;
	int m_nDiMuonVetoPairsSS = 0;

	// filled by TTHTauPairProducer
	std::vector<KTau*> m_validTTHTaus;
	
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
	std::map<KTau*, double> m_tauEnergyScaleWeight;
	
	// filled by HttValid<Leptons>Producer
	std::map<KLepton*, double> m_leptonIsolation;
	std::map<KLepton*, double> m_leptonIsolationOverPt;
	std::map<KElectron*, double> m_electronIsolation;
	std::map<KElectron*, double> m_electronIsolationOverPt;
	std::map<KMuon*, double> m_muonIsolation;
	std::map<KMuon*, double> m_muonIsolationOverPt;
	std::map<KTau*, double> m_tauIsolation;
	std::map<KTau*, double> m_tauIsolationOverPt;
	
	// filled by the DiLeptonQuantitiesProducer
	RMFLV m_diLeptonSystem;
	RMFLV m_diLeptonPlusMetSystem;
	
	// filled by the DiLeptonQuantitiesProducer (collinear approximation)
	std::vector<RMFLV> m_flavourOrderedTauMomentaCA;
	RMFLV m_diTauSystemCA;
	bool m_validCollinearApproximation = false;
	
	double pZetaVis = 0.0;
	double pZetaMissVis = 0.0;
	double pZetaMissVisNoLep = 0.0;
	
	// filled by the SvfitProducer
	mutable SvfitEventKey m_svfitEventKey;
	mutable SvfitInputs m_svfitInputs;
	mutable SvfitResults m_svfitResults;
	bool m_svfitCalculated = false;
	
	// filled by the DiJetQuantitiesProducer
	RMDLV m_diJetSystem;
	bool m_diJetSystemAvailable = false;
	int m_nCentralJets20 = 0;
	int m_nCentralJets30 = 0;
	
	KMET* m_met = 0;
	
	// filled by the TauTauRestFrameProducer
	HttEnumTypes::TauTauRestFrameReco m_tauTauRestFrameReco = HttEnumTypes::TauTauRestFrameReco::NONE;
	std::vector<RMFLV> m_flavourOrderedTauMomenta;
	std::vector<ROOT::Math::Boost> m_boostsToTauRestFrames;
	bool m_tauMomentaReconstructed = false;
	RMFLV m_diTauSystem;
	ROOT::Math::Boost m_boostToDiTauRestFrame;
	bool m_diTauSystemReconstructed = false;

	// filled by GenTauCPProducer
	double m_genZMinus  = DefaultValues::UndefinedDouble;
	double m_genZPlus  = DefaultValues::UndefinedDouble;
	double m_genZs  = DefaultValues::UndefinedDouble;

	double m_genPhiCP  = DefaultValues::UndefinedDouble;
	double m_genOCP  = DefaultValues::UndefinedDouble;
	double m_genPhiStarCP  = DefaultValues::UndefinedDouble;
	double m_genOStarCP  = DefaultValues::UndefinedDouble;
	double m_genPhi  = DefaultValues::UndefinedDouble;
	double m_genPhiStar  = DefaultValues::UndefinedDouble;
	double m_genTauMinusDirX  = DefaultValues::UndefinedDouble;
	double m_genTauMinusDirY  = DefaultValues::UndefinedDouble;
	double m_genTauMinusDirZ  = DefaultValues::UndefinedDouble;
	double m_genPiMinusDirX  = DefaultValues::UndefinedDouble;
	double m_genPiMinusDirY  = DefaultValues::UndefinedDouble;
	double m_genPiMinusDirZ  = DefaultValues::UndefinedDouble;
	std::pair <double,double> m_genChargedProngEnergies = std::make_pair(DefaultValues::UndefinedDouble, DefaultValues::UndefinedDouble);
	double m_genThetaNuHadron  = DefaultValues::UndefinedDouble;
	double m_genAlphaTauNeutrinos  = DefaultValues::UndefinedDouble;
	KGenParticle* m_genOneProngCharged1 = 0;
	KGenParticle* m_genOneProngCharged2 = 0;

	// filled by RecoTauCPProducer
	double m_recoPhiStarCP  = DefaultValues::UndefinedDouble;
	double m_recoPhiStar = DefaultValues::UndefinedDouble;
	KGenParticle* m_recoChargedParticle1 = 0;
	KGenParticle* m_recoChargedParitcle2 = 0;
	std::pair <double,double> m_recoChargedHadronEnergies = std::make_pair(DefaultValues::UndefinedDouble, DefaultValues::UndefinedDouble);
	double m_recoIP1 = DefaultValues::UndefinedDouble;
	double m_recoIP2 = DefaultValues::UndefinedDouble;
	double m_recoTrackRefError1 = DefaultValues::UndefinedDouble;
	double m_recoTrackRefError2 = DefaultValues::UndefinedDouble;
	
	// MVA outputs
	std::vector<double> m_antiTtbarDiscriminators;

	// filled by HttValidGenTausProducer. Naming scheme like for the reco particles
	std::vector<KGenTau*> m_ptOrderedGenTaus;
	std::vector<KGenTau*> m_flavourOrderedGenTaus;
	std::vector<KGenTau*> m_chargeOrderedGenTaus;
	std::vector<KGenTau*> m_validGenTausToElectrons;
	std::vector<KGenTau*> m_validGenTausToMuons;
	std::vector<KGenTau*> m_validGenTausToTaus;

	// filled by TriggerTagAndProbeProducers
	std::vector<std::pair<KElectron*, KElectron*> > m_triggerTagProbeElectronPairs;
	std::vector<std::pair<KMuon*, KMuon*> > m_triggerTagProbeMuonPairs;
	
	std::vector<std::pair<bool, bool> > m_triggerTagProbeElectronMatchedPairs;
	std::vector<std::pair<bool, bool> > m_triggerTagProbeMuonMatchedPairs;
};
