
#pragma once

#include <utility>

#include "Kappa/DataFormats/interface/Kappa.h"
#include "Artus/Utility/interface/ArtusLogging.h"

#include "TVector3.h"
#include "TMatrix.h"


/**
   \brief Place to collect functions calculating CP quantities
   -Phi* : this is a variable, with which one can say, whether the considered boson is a CP even state or a CP odd state
   -Phi*CP : this is a variable, with which one can figure out, whether the Higgs is a CP mixture or not
   -Zs : this is a variable, with which one can figure out, wether the considered boson has spin 1 (Z) or 0 (Higgs)
*/

class CPQuantities
{
public:
	double CalculatePhiStarCP(RMFLV tau1, RMFLV tau2, RMFLV chargPart1, RMFLV chargPart2);
	double CalculatePhiStarCP(KVertex* pv, KTrack track1, KTrack track2, RMFLV chargPart1, RMFLV chargPart2);
	double CalculatePhiStarCP(KRefitVertex* pv, KTrack track1, KTrack track2, RMFLV chargPart1, RMFLV chargPart2);
	double CalculatePhiStarCP(RMFLV chargPart1, RMFLV chargPart2, TVector3 ipvec1, TVector3 ipvec2, std::string level);
	double CalculatePhiStarCPRho(RMFLV chargedPiP, RMFLV chargedPiM, RMFLV piZeroP, RMFLV piZeroM);
	double CalculatePhiStarCPComb(TVector3 ipvec, RMFLV daughter, RMFLV pion, RMFLV pizero, int daughterCharge);
	double CalculateChargedHadronEnergy(RMFLV diTauMomentum, RMFLV chargHad);
	double CalculatePhiCP(RMFLV boson, RMFLV tau1, RMFLV tau2, RMFLV pion1, RMFLV pion2);
	double CalculatePhiCPLab(RMFLV chargPart1, TVector3 ipvec1, TVector3 ipvec2);
	double CalculateChargedProngEnergy(RMFLV tau, RMFLV chargedProng);
	double CalculateChargedProngEnergyApprox(RMFLV tau, RMFLV chargedProng);
	double CalculateSpinAnalysingDiscriminantRho(RMFLV tau1, RMFLV tau2, RMFLV pionP, RMFLV pionM, RMFLV pi0P, RMFLV pi0M);
	double CalculateSpinAnalysingDiscriminantRho(RMFLV chargedPion, RMFLV pi0);
	double CalculateTrackReferenceError(KTrack track);
	double CalculateZPlusMinus(RMFLV higgs, RMFLV chargedPart);
	double CalculateZs(double zPlus, double zMinus);
	double CalculateD0sArea(double d0_1, double d0_2);
	double CalculateD0sDist(double d0_1, double d0_2);
	double CalculatePCADifferece(SMatrixSym3D cov, TVector3 DeltaPCA);
	TVector3 CalculatePCA(double B, short charge, std::vector<float> h_param,	ROOT::Math::SMatrix<float,5,5, ROOT::Math::MatRepSym<float,5>> cov, RMPoint ref, RMPoint PrV, bool write, double* return_scalar_product, KLepton* recoParticle, double* xBest);
	ROOT::Math::SMatrix<float,3,3, ROOT::Math::MatRepStd< float, 3, 3 >> CalculatePCACovariance(double B, short charge, std::vector<float> h_param, ROOT::Math::SMatrix<float,5,5, ROOT::Math::MatRepSym<float,5>> cov, RMPoint ref, RMPoint PrV, SMatrixSym3D SigmaPrV, double xBest);
	double PhiTransform(double phi);
	TVector3 CalculateShortestDistance(KGenParticle* genParticle, RMPoint* pv);
	TVector3 CalculateShortestDistance(KLepton* recoParticle, RMPoint pv);
	double CalculateCosPsi(RMFLV recoPart, TVector3 ipvec);
	std::vector<double> CalculateIPErrors(KLepton* lepton, KVertex* pv, TVector3* ipvec);
	double MergePhiStarCPCombSemiLeptonic(double phiStarCP, KTau* recoTau2, double reco_posyTauL, double reco_negyTauL);
	double MergePhiStarCPCombFullyHadronic(double phiStarCP, KTau* recoTau1, KTau* recoTau2, double reco_posyTauL, double reco_negyTauL);
	inline double GetGenPhiStar()
	{
		return genPhiStar;
	}
	inline double GetGenOStarCP()
	{
		return genOStarCP;
	}
	inline double GetGenPhi()
	{
		return genPhi;
	}
	inline double GetGenOCP()
	{
		return genOCP;
	}
	inline double GetRecoPhiStar()
	{
		return recoPhiStar;
	}
	inline double GetRecoOStarCP()
	{
		return recoOStarCP;
	}
	inline double GetRecoIP1()
	{
		return recoIP1;
	}
	inline double GetRecoIP2()
	{
		return recoIP2;
	}
	// get functions for azimuthal angle of tau decay planes - ip method
	inline double GetRecoPhiPlusIPMeth(){ return recoPhiPlusIPMeth; }
	inline double GetRecoPhiMinusIPMeth(){ return recoPhiMinusIPMeth; }
	inline double GetRecoPhiStarPlusIPMeth(){ return recoPhiStarPlusIPMeth; }
	inline double GetRecoPhiStarMinusIPMeth(){ return recoPhiStarMinusIPMeth; }
	// get functions for azimuthal angle of tau decay planes - comb method
	inline double GetRecoPhiPlusCombMeth(){ return recoPhiPlusCombMeth; }
	inline double GetRecoPhiMinusCombMeth(){ return recoPhiMinusCombMeth; }
	inline double GetRecoPhiStarPlusCombMeth(){ return recoPhiStarPlusCombMeth; }
	inline double GetRecoPhiStarMinusCombMeth(){ return recoPhiStarMinusCombMeth; }
	// get functions for azimuthal angle of tau decay planes - rho method
	inline double GetRecoPhiPlusRhoMeth(){ return recoPhiPlusRhoMeth; }
	inline double GetRecoPhiMinusRhoMeth(){ return recoPhiMinusRhoMeth; }
	inline double GetRecoPhiStarPlusRhoMeth(){ return recoPhiStarPlusRhoMeth; }
	inline double GetRecoPhiStarMinusRhoMeth(){ return recoPhiStarMinusRhoMeth; }
private:
	double genPhiStar;
	double genOStarCP;
	double genPhi;
	double genOCP;
	double recoPhiStar;
	double recoOStarCP;
	double recoIP1;
	double recoIP2;
	double recoPhiPlusIPMeth;
	double recoPhiMinusIPMeth;
	double recoPhiStarPlusIPMeth;
	double recoPhiStarMinusIPMeth;
	double recoPhiPlusCombMeth;
	double recoPhiMinusCombMeth;
	double recoPhiStarPlusCombMeth;
	double recoPhiStarMinusCombMeth;
	double recoPhiPlusRhoMeth;
	double recoPhiMinusRhoMeth;
	double recoPhiStarPlusRhoMeth;
	double recoPhiStarMinusRhoMeth;
	//level: "gen", "reco"
	double CalculatePhiStarCPSame(RMFLV::BetaVector k1, RMFLV::BetaVector k2, RMFLV chargPart1, RMFLV chargPart2, std::string level);
	inline void SetGenPhiStar(double genphistar)
	{
		genPhiStar = genphistar;
	}
	inline void SetGenOStarCP(double genostarcp)
	{
		genOStarCP = genostarcp;
	}
	inline void SetGenPhi(double genphi)
	{
		genPhi = genphi;
	}
	inline void SetGenOCP(double genocp)
	{
		genOCP = genocp;
	}
	inline void SetRecoPhiStar(double recophistar)
	{
		recoPhiStar = recophistar;
	}
	inline void SetRecoOStarCP(double recoostarcp)
	{
		recoOStarCP = recoostarcp;
	}
	inline void SetRecoIP1(double recoip1)
	{
		recoIP1 = recoip1;
	}
	inline void SetRecoIP2(double recoip2)
	{
		recoIP2 = recoip2;
	}
	// set functions for azimuthal angle of tau decay planes - ip method
	inline void SetRecoPhiPlusIPMeth(double recophiplusIPMeth){ recoPhiPlusIPMeth = recophiplusIPMeth; }
	inline void SetRecoPhiMinusIPMeth(double recophiminusIPMeth){ recoPhiMinusIPMeth = recophiminusIPMeth; }
	inline void SetRecoPhiStarPlusIPMeth(double recophistarplusIPMeth){ recoPhiStarPlusIPMeth = recophistarplusIPMeth; }
	inline void SetRecoPhiStarMinusIPMeth(double recophistarminusIPMeth){ recoPhiStarMinusIPMeth = recophistarminusIPMeth; }
	// set functions for azimuthal angle of tau decay planes - comb method
	inline void SetRecoPhiPlusCombMeth(double recophcomblusCombMeth){ recoPhiPlusCombMeth = recophcomblusCombMeth; }
	inline void SetRecoPhiMinusCombMeth(double recophiminusCombMeth){ recoPhiMinusCombMeth = recophiminusCombMeth; }
	inline void SetRecoPhiStarPlusCombMeth(double recophistarplusCombMeth){ recoPhiStarPlusCombMeth = recophistarplusCombMeth; }
	inline void SetRecoPhiStarMinusCombMeth(double recophistarminusCombMeth){ recoPhiStarMinusCombMeth = recophistarminusCombMeth; }
	// set functions for azimuthal angle of tau decay planes - rho method
	inline void SetRecoPhiPlusRhoMeth(double recophrholusRhoMeth){ recoPhiPlusRhoMeth = recophrholusRhoMeth; }
	inline void SetRecoPhiMinusRhoMeth(double recophiminusRhoMeth){ recoPhiMinusRhoMeth = recophiminusRhoMeth; }
	inline void SetRecoPhiStarPlusRhoMeth(double recophistarplusRhoMeth){ recoPhiStarPlusRhoMeth = recophistarplusRhoMeth; }
	inline void SetRecoPhiStarMinusRhoMeth(double recophistarminusRhoMeth){ recoPhiStarMinusRhoMeth = recophistarminusRhoMeth; }
};
