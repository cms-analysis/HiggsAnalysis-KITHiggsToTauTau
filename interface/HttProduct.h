
#pragma once

#include <map>
#include <string>

#include "Artus/KappaAnalysis/interface/KappaProduct.h"

#include "Artus/Utility/interface/DefaultValues.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttEnumTypes.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Utility/SvfitTools.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Utility/DiTauPair.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Utility/DiGenTauPair.h"
#include "TVector2.h"
#include "TVector3.h"

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

	/// added by GenDiTauPairCandidatesProducers and GenDiTauPairAcceptanceProducer
	std::vector<DiGenTauPair> m_genDiTauPairCandidates;
	std::vector<DiGenTauPair> m_genDiTauPairInAcceptance;

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

	// TODO: To be set by producers that apply shifts
	HttEnumTypes::SystematicShift m_systematicShift = HttEnumTypes::SystematicShift::CENTRAL;
	float m_systematicShiftSigma = 0.0;

	// filled by DecayChannelProducer
	std::vector<KLepton*> m_ptOrderedLeptons; // highest pt leptons first
	std::vector<KLepton*> m_flavourOrderedLeptons; // according to channel definition
	std::vector<KLepton*> m_chargeOrderedLeptons; // positively charged leptons first

	std::vector<KGenParticle*> m_ptOrderedGenLeptons; // same ordering as reco collection
	std::vector<KGenParticle*> m_flavourOrderedGenLeptons; // same ordering as reco collection
	std::vector<KGenParticle*> m_chargeOrderedGenLeptons; // same ordering as reco collection

	std::vector<RMFLV*> m_ptOrderedGenLeptonVisibleLVs; // same ordering as reco collection
	std::vector<RMFLV*> m_flavourOrderedGenLeptonVisibleLVs; // same ordering as reco collection
	std::vector<RMFLV*> m_chargeOrderedGenLeptonVisibleLVs; // same ordering as reco collection

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

	std::vector<std::string> m_triggersmatched;

	// individual isolation components needed for embedding studies (also filled by HttValidMuonsProducer)
	std::map<KMuon*, double> m_muonChargedIsolation;
	std::map<KMuon*, double> m_muonNeutralIsolation;
	std::map<KMuon*, double> m_muonPhotonIsolation;
	std::map<KMuon*, double> m_muonDeltaBetaIsolation;

	std::map<KMuon*, double> m_muonChargedIsolationOverPt;
	std::map<KMuon*, double> m_muonNeutralIsolationOverPt;
	std::map<KMuon*, double> m_muonPhotonIsolationOverPt;
	std::map<KMuon*, double> m_muonDeltaBetaIsolationOverPt;

	// filled by the DiLeptonQuantitiesProducer
	RMFLV m_diLeptonSystem;
	RMFLV m_diLeptonPlusMetSystem;
	RMFLV m_diLeptonGenSystem;
	bool m_diLeptonGenSystemFound = false;
	RMFLV m_diTauGenSystem;
	bool m_diTauGenSystemFound = false;
	double m_col;

	// filled by the TauSpinnerProducer
	bool m_tauSpinnerValidOutputs = false;
	double m_tauSpinnerPolarisation = DefaultValues::UndefinedDouble;
	double m_tauSpinnerPdgIdTau_1 = DefaultValues::UndefinedInt;
	double m_tauSpinnerPdgIdTau_2 = DefaultValues::UndefinedInt;
	double m_tauSpinnerETau_1 = DefaultValues::UndefinedDouble;
	double m_tauSpinnerETau_2 = DefaultValues::UndefinedDouble;
	double m_tauSpinnerEPi_1 = DefaultValues::UndefinedDouble;
	double m_tauSpinnerEPi_2 = DefaultValues::UndefinedDouble;

	// filled by the PolarisationQuantitiesProducer
	std::map<KLepton*, float> m_polarisationOmegasGenMatched;
	std::map<KLepton*, float> m_polarisationOmegasSvfit;
	std::map<KLepton*, float> m_polarisationOmegasSvfitM91;
	std::map<KLepton*, float> m_polarisationOmegasSimpleFit;
	//std::map<KLepton*, float> m_polarisationOmegasHHKinFit;
	std::map<KGenTau*, float> m_polarisationOmegasGen;

	std::map<KLepton*, float> m_polarisationOmegaBarsGenMatched;
	std::map<KLepton*, float> m_polarisationOmegaBarsSvfit;
	std::map<KLepton*, float> m_polarisationOmegaBarsSvfitM91;
	std::map<KLepton*, float> m_polarisationOmegaBarsSimpleFit;
	//std::map<KLepton*, float> m_polarisationOmegaBarsHHKinFit;
	std::map<KGenTau*, float> m_polarisationOmegaBarsGen;

	std::map<KLepton*, float> m_polarisationOmegaVisiblesGenMatched;
	std::map<KLepton*, float> m_polarisationOmegaVisiblesSvfit;
	std::map<KLepton*, float> m_polarisationOmegaVisiblesSvfitM91;
	std::map<KLepton*, float> m_polarisationOmegaVisiblesSimpleFit;
	//std::map<KLepton*, float> m_polarisationOmegaVisiblesHHKinFit;
	std::map<KGenTau*, float> m_polarisationOmegaVisiblesGen;

	float m_polarisationCombinedOmegaGenMatched = DefaultValues::UndefinedFloat;
	float m_polarisationCombinedOmegaSvfit = DefaultValues::UndefinedFloat;
	float m_polarisationCombinedOmegaSvfitM91 = DefaultValues::UndefinedFloat;
	float m_polarisationCombinedOmegaSimpleFit = DefaultValues::UndefinedFloat;
	//float m_polarisationCombinedOmegaHHKinFit = DefaultValues::UndefinedFloat;
	float m_polarisationCombinedOmegaGen = DefaultValues::UndefinedFloat;

	float m_polarisationCombinedOmegaBarGenMatched = DefaultValues::UndefinedFloat;
	float m_polarisationCombinedOmegaBarSvfit = DefaultValues::UndefinedFloat;
	float m_polarisationCombinedOmegaBarSvfitM91 = DefaultValues::UndefinedFloat;
	float m_polarisationCombinedOmegaBarSimpleFit = DefaultValues::UndefinedFloat;
	//float m_polarisationCombinedOmegaBarHHKinFit = DefaultValues::UndefinedFloat;
	float m_polarisationCombinedOmegaBarGen = DefaultValues::UndefinedFloat;

	float m_polarisationCombinedOmegaVisibleGenMatched = DefaultValues::UndefinedFloat;
	float m_polarisationCombinedOmegaVisibleSvfit = DefaultValues::UndefinedFloat;
	float m_polarisationCombinedOmegaVisibleSvfitM91 = DefaultValues::UndefinedFloat;
	float m_polarisationCombinedOmegaVisibleSimpleFit = DefaultValues::UndefinedFloat;
	//float m_polarisationCombinedOmegaVisibleHHKinFit = DefaultValues::UndefinedFloat;
	float m_polarisationCombinedOmegaVisibleGen = DefaultValues::UndefinedFloat;

	// filled by the MetprojectionProducer
	TVector2 m_recoMetOnGenMetProjection;
	TVector2 m_metPull;
	TVector2 m_recoMetOnBoson;
	TVector2 m_recoilOnBoson;
	double m_chiSquare;
	TVector2 m_recoPfMetOnGenMetProjection;
	TVector2 m_pfmetPull;
	TVector2 m_recoPfMetOnBoson;
	TVector2 m_pfrecoilOnBoson;
	double m_chiSquarePf;
	double m_metPlusVisLepsOnGenBosonPtOverGenBosonPt;
	double m_pfmetPlusVisLepsOnGenBosonPtOverGenBosonPt;
	double m_genBosonPt;
	double m_genBosonPhi;

	// filled by the DiLeptonQuantitiesProducer (collinear approximation)
	std::vector<RMFLV> m_flavourOrderedTauMomentaCA;
	RMFLV m_diTauSystemCA;
	bool m_validCollinearApproximation = false;

	double pZetaVis = 0.0;
	double pZetaMiss = 0.0;
	double pZetaMissVis = 0.0;

	// filled by the SvfitProducer
	mutable SvfitEventKey m_svfitEventKey;
	mutable SvfitEventKey m_svfitM91EventKey;
	mutable SvfitEventKey m_svfitM125EventKey;
	mutable SvfitInputs m_svfitInputs;
	mutable SvfitResults m_svfitResults;
	mutable SvfitResults m_svfitM91Results;
	mutable SvfitResults m_svfitM125Results;
	std::map<KLepton*, RMFLV> m_svfitTaus;
	std::map<KLepton*, RMFLV> m_svfitM91Taus;
	std::map<KLepton*, RMFLV> m_svfitM125Taus;

	// filled by the HHKinFitProducer
	//std::map<KLepton*, RMFLV> m_hhKinFitTaus;

	// filled by the SimpleFitProducer
	std::map<KLepton*, RMFLV> m_simpleFitTaus;
	RMFLV m_diTauSystemSimpleFit = DefaultValues::UndefinedRMFLV;

	// filled by the DiJetQuantitiesProducer
	RMDLV m_diJetSystem;
	bool m_diJetSystemAvailable = false;
	int m_nCentralJets20 = 0;
	int m_nCentralJets30 = 0;

	// filled by the DiGenJetQuantitiesProducer
	RMDLV m_diGenJetSystem;
	bool m_diGenJetSystemAvailable = false;

	// filled by TaggedJetUncertaintyShiftProducer
	std::map<HttEnumTypes::JetEnergyUncertaintyShiftName, std::vector<KJet>> m_correctedJetsBySplitUncertaintyUp;
	std::map<HttEnumTypes::JetEnergyUncertaintyShiftName, std::vector<KJet>> m_correctedJetsBySplitUncertaintyDown;
	std::vector<KJet> m_correctedJetsBySplitUncertainty;
	std::map<HttEnumTypes::JetEnergyUncertaintyShiftName, std::vector<KJet>> m_correctedBTaggedJetsBySplitUncertaintyUp;
	std::map<HttEnumTypes::JetEnergyUncertaintyShiftName, std::vector<KJet>> m_correctedBTaggedJetsBySplitUncertaintyDown;
	std::vector<KJet> m_correctedBTaggedJetsBySplitUncertainty;

	KMET m_MET_shift;

	KMET* m_metUncorr = 0;
	KMET* m_puppiMetUncorr = 0;
	KMET* m_pfmetUncorr = 0;
	KMET* m_mvametUncorr = 0;



	// filled by the MetCorrectors
	std::vector<float> m_mvametCorrections;
	std::vector<float> m_pfmetCorrections;
	KMET m_met;
	KMET m_pfmet;
	KMET m_mvamet;

	// filled by the TauTauRestFrameProducer
	HttEnumTypes::TauTauRestFrameReco m_tauTauRestFrameReco = HttEnumTypes::TauTauRestFrameReco::NONE;
	std::vector<RMFLV> m_flavourOrderedTauMomenta;
	std::vector<ROOT::Math::Boost> m_boostsToTauRestFrames;
	bool m_tauMomentaReconstructed = false;
	RMFLV m_diTauSystem;
	ROOT::Math::Boost m_boostToDiTauRestFrame;
	bool m_diTauSystemReconstructed = false;

	// filled by the BoostRestFrameProducer
	std::map<KLepton*, RMFLV> m_leptonsBoostToDiLeptonSystem;
	std::map<KLepton*, RMFLV> m_leptonsBoostToDiTauSystem;
	std::map<RMFLV*, RMFLV> m_tausBoostToDiTauSystem;
	std::map<KGenTau*, RMFLV> m_genVisTausBoostToGenDiLeptonSystem;
	std::map<KGenTau*, RMFLV> m_genTausBoostToGenDiLeptonSystem;
	std::map<KGenTau*, RMFLV> m_genTausBoostToGenDiTauSystem;


	// filled by RefitVertexSelector
	KRefitVertex* m_refitPV = 0;
	KRefitVertex* m_refitPVBS = 0;
	RMPoint* m_refP1 = 0;
	RMPoint* m_refP2 = 0;
	RMFLV* m_track1p4 = 0;
	RMFLV* m_track2p4 = 0;

	float m_d3DnewPV1 = DefaultValues::UndefinedFloat;    // IP vector mag calculated with IPTools method
	float m_err3DnewPV1 = DefaultValues::UndefinedFloat;  // and corresponding error
	float m_d2DnewPV1 = DefaultValues::UndefinedFloat;
	float m_err2DnewPV1 = DefaultValues::UndefinedFloat;
	float m_d3DnewPV2 = DefaultValues::UndefinedFloat;
	float m_err3DnewPV2 = DefaultValues::UndefinedFloat;
	float m_d2DnewPV2 = DefaultValues::UndefinedFloat;
	float m_err2DnewPV2 = DefaultValues::UndefinedFloat;


	// filled by GenTauCPProducer
	RMPoint* m_genPV = 0;
	double m_genZMinus = DefaultValues::UndefinedDouble;
	double m_genZPlus  = DefaultValues::UndefinedDouble;
	double m_genZs  = DefaultValues::UndefinedDouble;

	double m_d0_1 = DefaultValues::UndefinedDouble;
	double m_d0_2 = DefaultValues::UndefinedDouble;
	double m_d0s_area  = DefaultValues::UndefinedDouble;
	double m_d0s_dist  = DefaultValues::UndefinedDouble;

	double m_genPhiCP = DefaultValues::UndefinedDouble;
	double m_genPhiStarCP  = DefaultValues::UndefinedDouble;
	double m_genPhiStar  = DefaultValues::UndefinedDouble;
	double m_genOStarCP  = DefaultValues::UndefinedDouble;
	double m_genPhi  = DefaultValues::UndefinedDouble;
	double m_genOCP  = DefaultValues::UndefinedDouble;
	double m_genPhiCPLab  = DefaultValues::UndefinedDouble;
	double m_genPhiStarCPComb = DefaultValues::UndefinedDouble;

	double m_genPhiCP_rho  = DefaultValues::UndefinedDouble;
	double m_genPhiStarCP_rho  = DefaultValues::UndefinedDouble;
	double m_genPhi_rho  = DefaultValues::UndefinedDouble;
	double m_genPhiStar_rho  = DefaultValues::UndefinedDouble;
	double m_gen_yTau  = DefaultValues::UndefinedDouble;
	double m_gen_posyTauL  = DefaultValues::UndefinedDouble;
	double m_gen_negyTauL  = DefaultValues::UndefinedDouble;

	std::pair <double,double> m_genChargedProngEnergies = std::make_pair(DefaultValues::UndefinedDouble, DefaultValues::UndefinedDouble);
	KGenParticle* m_genOneProngCharged1 = 0;
	KGenParticle* m_genOneProngCharged2 = 0;
	unsigned int m_genTau1ProngsSize = DefaultValues::UndefinedInt;
	unsigned int m_genTau2ProngsSize = DefaultValues::UndefinedInt;
	int m_genTau1DecayMode = DefaultValues::UndefinedInt;
	int m_genTau2DecayMode = DefaultValues::UndefinedInt;
	int m_genTauTree1DecayMode = DefaultValues::UndefinedInt;
	int m_genTauTree2DecayMode = DefaultValues::UndefinedInt;


	// filled by GenMatchedTauCPProducer
	RMPoint* m_genSV1 = 0; // vertex of production of tau daughter 1
	RMPoint* m_genSV2 = 0; // vertex of production of tau daughter 2
	double m_genD01 = DefaultValues::UndefinedDouble;
	double m_genD02 = DefaultValues::UndefinedDouble;
	TVector3 m_genIP1;
	TVector3 m_genIP2;
	double m_genCosPsiPlus  = DefaultValues::UndefinedDouble;
	double m_genCosPsiMinus = DefaultValues::UndefinedDouble;


	// filled by RecoTauCPProducer

	TVector3 m_recoIP1; // IPvec wrt original PV
	TVector3 m_recoIP2; // IPvec wrt original PV
	TVector3 m_recoIP1_refitPV; // IPvec wrt refitted PV
	TVector3 m_recoIP2_refitPV; // IPvec wrt refitted PV
	TVector3 m_track1FromBS; // distance between track1 and BS center
	TVector3 m_track2FromBS; // distance between track2 and BS center

	double m_pca1DiffInSigma = DefaultValues::UndefinedDouble; //Distance of Point of closest approach(PCA) from the primary vertex (PV) in units of sigma
	double m_pca2DiffInSigma = DefaultValues::UndefinedDouble; //Distance of Point of closest approach(PCA) from the primary vertex (PV) in units of sigma
	double m_pca1proj = DefaultValues::UndefinedDouble; //Projection of Point of closest approach(PCA) to the primary vertex (PV) 1 sigma ellipsoid
	double m_pca2proj = DefaultValues::UndefinedDouble; //Projection of Point of closest approach(PCA) to the primary vertex (PV) 1 sigma ellipsoid

	double m_cosPsiPlus  = DefaultValues::UndefinedDouble;
	double m_cosPsiMinus = DefaultValues::UndefinedDouble;

	std::vector<double> m_errorIP1vec {DefaultValues::UndefinedDouble, DefaultValues::UndefinedDouble, DefaultValues::UndefinedDouble};
	std::vector<double> m_errorIP2vec {DefaultValues::UndefinedDouble, DefaultValues::UndefinedDouble, DefaultValues::UndefinedDouble};

	std::vector<double> m_errorIP1vec_refitPV {DefaultValues::UndefinedDouble, DefaultValues::UndefinedDouble, DefaultValues::UndefinedDouble};
	std::vector<double> m_errorIP2vec_refitPV {DefaultValues::UndefinedDouble, DefaultValues::UndefinedDouble, DefaultValues::UndefinedDouble};

	// comparison genIP-recoIP

	// wrt original PV

	double m_deltaEtaGenRecoIP1  = DefaultValues::UndefinedDouble;
	double m_deltaEtaGenRecoIP2  = DefaultValues::UndefinedDouble;
	double m_deltaPhiGenRecoIP1  = DefaultValues::UndefinedDouble;
	double m_deltaPhiGenRecoIP2  = DefaultValues::UndefinedDouble;
	double m_deltaRGenRecoIP1  = DefaultValues::UndefinedDouble;
	double m_deltaRGenRecoIP2  = DefaultValues::UndefinedDouble;
	double m_deltaGenRecoIP1  = DefaultValues::UndefinedDouble;
	double m_deltaGenRecoIP2  = DefaultValues::UndefinedDouble;
	// wrt refitPV
	double m_deltaEtaGenRecoIP1_refitPV  = DefaultValues::UndefinedDouble;
	double m_deltaEtaGenRecoIP2_refitPV  = DefaultValues::UndefinedDouble;
	double m_deltaPhiGenRecoIP1_refitPV  = DefaultValues::UndefinedDouble;
	double m_deltaPhiGenRecoIP2_refitPV  = DefaultValues::UndefinedDouble;
	double m_deltaRGenRecoIP1_refitPV  = DefaultValues::UndefinedDouble;
	double m_deltaRGenRecoIP2_refitPV  = DefaultValues::UndefinedDouble;
	double m_deltaGenRecoIP1_refitPV  = DefaultValues::UndefinedDouble;
	double m_deltaGenRecoIP2_refitPV  = DefaultValues::UndefinedDouble;




	// comparison between recoIP(original PV) and recoIP(refitPV)

	double m_deltaRrecoIP1s  = DefaultValues::UndefinedDouble;
	double m_deltaRrecoIP2s  = DefaultValues::UndefinedDouble;

	// CP-sensitive observable
	double m_recoPhiStarCP  = DefaultValues::UndefinedDouble;
	double m_recoPhiStarCPrPV  = DefaultValues::UndefinedDouble;
	double m_recoPhiStarCPrPV2  = DefaultValues::UndefinedDouble;
	double m_recoPhiStarCPrPVbs  = DefaultValues::UndefinedDouble;
	double m_recoPhiStarCPComb  = DefaultValues::UndefinedDouble;
	double m_recoPhiStarCPCombMerged  = DefaultValues::UndefinedDouble;

	double m_recoPhiStarCP_rho  = DefaultValues::UndefinedDouble;
	double m_recoPhiStarCP_rho_merged  = DefaultValues::UndefinedDouble;
	double m_recoPhiStarCPrPV_rho  = DefaultValues::UndefinedDouble;
	double m_recoPhiStarCPrPVbs_rho  = DefaultValues::UndefinedDouble;

	double m_reco_posyTauL = DefaultValues::UndefinedDouble;
	double m_reco_negyTauL = DefaultValues::UndefinedDouble;
	double m_recoPhiStar = DefaultValues::UndefinedDouble;
	double m_recoPhiStar_rho = DefaultValues::UndefinedDouble;



	// azimuthal angles of the tau decay planes
	// ip method
	double m_recoPhiPlus_ipmeth = DefaultValues::UndefinedDouble;
	double m_recoPhiMinus_ipmeth = DefaultValues::UndefinedDouble;
	double m_recoPhiStarPlus_ipmeth = DefaultValues::UndefinedDouble;
	double m_recoPhiStarMinus_ipmeth = DefaultValues::UndefinedDouble;
	// comb method
	double m_recoPhiPlus_combmeth = DefaultValues::UndefinedDouble;
	double m_recoPhiMinus_combmeth = DefaultValues::UndefinedDouble;
	double m_recoPhiStarPlus_combmeth = DefaultValues::UndefinedDouble;
	double m_recoPhiStarMinus_combmeth = DefaultValues::UndefinedDouble;
	// rho method
	double m_recoPhiPlus_rhometh = DefaultValues::UndefinedDouble;
	double m_recoPhiMinus_rhometh = DefaultValues::UndefinedDouble;
	double m_recoPhiStarPlus_rhometh = DefaultValues::UndefinedDouble;
	double m_recoPhiStarMinus_rhometh = DefaultValues::UndefinedDouble;

	double m_recoChargedPiPlus_rho_pt = DefaultValues::UndefinedDouble;
	double m_recoChargedPiMinus_pt = DefaultValues::UndefinedDouble;
	double m_recoPiZeroPlus_pt = DefaultValues::UndefinedDouble;
	double m_recoPiZeroMinus_pt = DefaultValues::UndefinedDouble;
	double m_recoChargedPiPlus_eta = DefaultValues::UndefinedDouble;
	double m_recoChargedPiMinus_eta = DefaultValues::UndefinedDouble;
	double m_recoPiZeroPlus_eta = DefaultValues::UndefinedDouble;
	double m_recoPiZeroMinus_eta = DefaultValues::UndefinedDouble;

	KGenParticle* m_recoChargedParticle1 = 0;
	KGenParticle* m_recoChargedParitcle2 = 0;
	std::pair <double,double> m_recoChargedHadronEnergies = std::make_pair(DefaultValues::UndefinedDouble, DefaultValues::UndefinedDouble);
	//double m_recoIP1 = DefaultValues::UndefinedDouble;
	//double m_recoIP2 = DefaultValues::UndefinedDouble;
	double m_recoTrackRefError1 = DefaultValues::UndefinedDouble;
	double m_recoTrackRefError2 = DefaultValues::UndefinedDouble;

	// MVA outputs
	std::vector<double> m_antiTtbarDiscriminators;
	std::vector<double> m_tauPolarisationDiscriminators;

	//MVATestMethods
	std::vector<double> m_MVATestMethodsDiscriminators;

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
	std::vector<std::pair<KMuon*, KTau*> > m_triggerTagProbeMuonTauPairs;
	std::vector<std::pair<KElectron*, KTau*> > m_triggerTagProbeElectronTauPairs;

	std::vector<std::pair<bool, bool> > m_triggerTagProbeElectronMatchedPairs;
	std::vector<std::pair<bool, bool> > m_triggerTagProbeMuonMatchedPairs;
	std::vector<std::pair<bool, bool> > m_triggerTagProbeMuonTauMatchedPairs;
	std::vector<std::pair<bool, bool> > m_triggerTagProbeElectronTauMatchedPairs;

	std::vector<double> m_tautriggerefficienciesMC;
	std::vector<double> m_tautriggerefficienciesData;

	// filled by MVAInputQuantitiesProducer
// 	int tsValue = 0;
	double m_pVecSum = -1;
	double m_pScalSum = -1;
	double m_MinLLJetEta = 10;
	double m_Lep1Centrality = -1.5;
	double m_Lep2Centrality = -1;
	double m_DiLepCentrality = -1;
	double m_DiLepDiJetDeltaR = -1;
	double m_diLepBoost = -10;
	double m_diLepJet1DeltaR = -10;
	double m_diLepDeltaR = -10;
	double m_diJetDeltaMass = -10;
	double m_diJetSymDeltaEta = -30;
	double m_diJetDeltaR = -1;
	double m_diCJetDeltaMass = -10;
	double m_diCJetSymDeltaEta = -30;
	double m_diCJetDeltaR = -1;
	double m_diCJetAbsDeltaPhi = -1;
	double m_diCJetSymEta1 = -1;
	double m_jccsv1 = -1;
	double m_jccsv2 = -1;
	double m_jccsv3 = -1;
	double m_jccsv4 = -1;
	double m_csv1JetPt = -10;
	double m_csv2JetPt = -10;
	double m_csv1JetMass = -10;
	double m_csv2JetMass = -10;
	double m_diCJetMass = -10;
	double m_pVecSumCSVJets = -1;

	// filled by EmbeddingGlobalQuantitiesProducer
	double m_pfSumHt = 0.;
	RMFLV m_pfSumP4;
	double m_pfSumHtWithoutZMuMu = 0.;
	RMFLV m_pfSumP4WithoutZMuMu;

	//filled by TagAndProbeMuonPairProducer
	std::vector<std::pair<KMuon*,KMuon*>> m_TagAndProbeMuonPairs;
	//filled by TagAndProbeElectronPairProducer
	std::vector<std::pair<KElectron*,KElectron*>> m_TagAndProbeElectronPairs;
	//filled by TagAndProbeGenLeptonProducer
	std::vector<KElectron*> m_TagAndProbeGenElectrons;
	std::vector<KMuon*> m_TagAndProbeGenMuons;
	std::vector<KTau*> m_TagAndProbeGenTaus;

	//filled by TTbarGenDecayModeProducer
	unsigned int m_TTbarGenDecayMode = 0;

	//filled by GenHiggsCPProducer
	std::vector<KLHEParticle*> m_lheParticlesIn;
	std::vector<KLHEParticle*> m_lheParticlesOut;
	std::vector<KLHEParticle*> m_lheParticlesBoson;

	//filled by MadGraphReweightingProducer
	std::vector<KLHEParticle*> m_lheParticlesSortedForMadGraph;

	//filled by MadGraphReweightingProducer
	float m_melaProbCPEvenGGH = DefaultValues::UndefinedFloat;
	float m_melaProbCPOddGGH = DefaultValues::UndefinedFloat;
	float m_melaProbCPMixGGH = DefaultValues::UndefinedFloat;
	float m_melaDiscriminatorD0MinusGGH = DefaultValues::UndefinedFloat;
	float m_melaDiscriminatorDCPGGH = DefaultValues::UndefinedFloat;

	float m_melaProbCPEvenVBF = DefaultValues::UndefinedFloat;
	float m_melaProbCPOddVBF = DefaultValues::UndefinedFloat;
	float m_melaProbCPMixVBF = DefaultValues::UndefinedFloat;
	float m_melaDiscriminatorD0MinusVBF = DefaultValues::UndefinedFloat;
	float m_melaDiscriminatorDCPVBF = DefaultValues::UndefinedFloat;

	//filled by LFVJetCorrection2016Producer
	float lfvjetcorr;

	/*
	float m_melaProbCPEvenWlepH = DefaultValues::UndefinedFloat;
	float m_melaProbCPOddWlepH = DefaultValues::UndefinedFloat;
	float m_melaProbCPMixWlepH = DefaultValues::UndefinedFloat;
	float m_melaDiscriminatorD0MinusWlepH = DefaultValues::UndefinedFloat;
	float m_melaDiscriminatorDCPWlepH = DefaultValues::UndefinedFloat;

	float m_melaProbCPEvenWhadH = DefaultValues::UndefinedFloat;
	float m_melaProbCPOddWhadH = DefaultValues::UndefinedFloat;
	float m_melaProbCPMixWhadH = DefaultValues::UndefinedFloat;
	float m_melaDiscriminatorD0MinusWhadH = DefaultValues::UndefinedFloat;
	float m_melaDiscriminatorDCPWhadH = DefaultValues::UndefinedFloat;

	float m_melaProbCPEvenZlepH = DefaultValues::UndefinedFloat;
	float m_melaProbCPOddZlepH = DefaultValues::UndefinedFloat;
	float m_melaProbCPMixZlepH = DefaultValues::UndefinedFloat;
	float m_melaDiscriminatorD0MinusZlepH = DefaultValues::UndefinedFloat;
	float m_melaDiscriminatorDCPZlepH = DefaultValues::UndefinedFloat;

	float m_melaProbCPEvenZhadH = DefaultValues::UndefinedFloat;
	float m_melaProbCPOddZhadH = DefaultValues::UndefinedFloat;
	float m_melaProbCPMixZhadH = DefaultValues::UndefinedFloat;
	float m_melaDiscriminatorD0MinusZhadH = DefaultValues::UndefinedFloat;
	float m_melaDiscriminatorDCPZhadH = DefaultValues::UndefinedFloat;
	*/

	float m_melaM125ProbCPEvenGGH = DefaultValues::UndefinedFloat;
	float m_melaM125ProbCPOddGGH = DefaultValues::UndefinedFloat;
	float m_melaM125ProbCPMixGGH = DefaultValues::UndefinedFloat;
	float m_melaM125DiscriminatorD0MinusGGH = DefaultValues::UndefinedFloat;
	float m_melaM125DiscriminatorDCPGGH = DefaultValues::UndefinedFloat;

	float m_melaM125ProbCPEvenVBF = DefaultValues::UndefinedFloat;
	float m_melaM125ProbCPOddVBF = DefaultValues::UndefinedFloat;
	float m_melaM125ProbCPMixVBF = DefaultValues::UndefinedFloat;
	float m_melaM125DiscriminatorD0MinusVBF = DefaultValues::UndefinedFloat;
	float m_melaM125DiscriminatorDCPVBF = DefaultValues::UndefinedFloat;

	/*
	float m_melaM125ProbCPEvenWlepH = DefaultValues::UndefinedFloat;
	float m_melaM125ProbCPOddWlepH = DefaultValues::UndefinedFloat;
	float m_melaM125ProbCPMixWlepH = DefaultValues::UndefinedFloat;
	float m_melaM125DiscriminatorD0MinusWlepH = DefaultValues::UndefinedFloat;
	float m_melaM125DiscriminatorDCPWlepH = DefaultValues::UndefinedFloat;

	float m_melaM125ProbCPEvenWhadH = DefaultValues::UndefinedFloat;
	float m_melaM125ProbCPOddWhadH = DefaultValues::UndefinedFloat;
	float m_melaM125ProbCPMixWhadH = DefaultValues::UndefinedFloat;
	float m_melaM125DiscriminatorD0MinusWhadH = DefaultValues::UndefinedFloat;
	float m_melaM125DiscriminatorDCPWhadH = DefaultValues::UndefinedFloat;

	float m_melaM125ProbCPEvenZlepH = DefaultValues::UndefinedFloat;
	float m_melaM125ProbCPOddZlepH = DefaultValues::UndefinedFloat;
	float m_melaM125ProbCPMixZlepH = DefaultValues::UndefinedFloat;
	float m_melaM125DiscriminatorD0MinusZlepH = DefaultValues::UndefinedFloat;
	float m_melaM125DiscriminatorDCPZlepH = DefaultValues::UndefinedFloat;

	float m_melaM125ProbCPEvenZhadH = DefaultValues::UndefinedFloat;
	float m_melaM125ProbCPOddZhadH = DefaultValues::UndefinedFloat;
	float m_melaM125ProbCPMixZhadH = DefaultValues::UndefinedFloat;
	float m_melaM125DiscriminatorD0MinusZhadH = DefaultValues::UndefinedFloat;
	float m_melaM125DiscriminatorDCPZhadH = DefaultValues::UndefinedFloat;
	*/

	int m_lhenpNLO = 0;
	RMDLV m_diJetSystem_CP1;
	RMDLV m_diJetSystem_CP2;
	bool m_etaH_cut = false;
	RMDLV m_jet_higher_CP1;
	RMDLV m_jet_lower_CP1;
	RMDLV m_jet_higher_CP2;
	RMDLV m_jet_lower_CP2;
	float m_etasep_1 = DefaultValues::UndefinedFloat;
	float m_etasep_2 = DefaultValues::UndefinedFloat;

};
