
#pragma once

#include <utility>

#include "Kappa/DataFormats/interface/Kappa.h"
#include "Artus/Utility/interface/ArtusLogging.h"

#include "TVector3.h"


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
	double CalculatePhiStarCP_rho(RMFLV chargedPiP, RMFLV chargedPiM, RMFLV piZeroP, RMFLV piZeroM);
	double CalculatePhiStarCPComb(TVector3 ipvec, RMFLV daughter, RMFLV pion, RMFLV pizero, int daughterCharge);
	double CalculateChargedHadronEnergy(RMFLV diTauMomentum, RMFLV chargHad);
	double CalculatePhiCP(RMFLV boson, RMFLV tau1, RMFLV tau2, RMFLV pion1, RMFLV pion2);
	double CalculatePhiCPLab(RMFLV chargPart1, TVector3 ipvec1, TVector3 ipvec2);
	double CalculateChargedProngEnergy(RMFLV tau, RMFLV chargedProng);
	double CalculateChargedProngEnergyApprox(RMFLV tau, RMFLV chargedProng);
	double CalculateSpinAnalysingDiscriminant_rho(RMFLV tau1, RMFLV tau2, RMFLV pionP, RMFLV pionM, RMFLV pi0P, RMFLV pi0M);
	double CalculateSpinAnalysingDiscriminant_rho(RMFLV chargedPion, RMFLV pi0);
	double CalculateTrackReferenceError(KTrack track);
	double CalculateZPlusMinus(RMFLV higgs, RMFLV chargedPart);
	double CalculateZs(double zPlus, double zMinus);
	double PhiTransform(double phi);
	TVector3 CalculateIPVector(KGenParticle* genParticle, RMPoint* pv);
	TVector3 CalculateIPVector(KLepton* recoParticle, KVertex* pv);
	double CalculateCosPsi(RMFLV recoPart, TVector3 ipvec);
	std::vector<double> CalculateIPErrors(KLepton* lepton, KVertex* pv, TVector3* ipvec);
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
private:
	double genPhiStar;
	double genOStarCP;
	double genPhi;
	double genOCP;
	double recoPhiStar;
	double recoOStarCP;
	double recoIP1;
	double recoIP2;
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
};
