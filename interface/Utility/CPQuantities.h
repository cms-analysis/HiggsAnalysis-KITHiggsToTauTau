
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
	double CalculateD0sArea(double d0_1, double d0_2);
	double CalculateD0sDist(double d0_1, double d0_2);
	double PhiTransform(double phi);
	TVector3 CalculateShortestDistance(KGenParticle* genParticle, RMPoint* pv);
	TVector3 CalculateShortestDistance(KLepton* recoParticle, RMPoint pv);
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
	// get functions for azimuthal angle of tau decay planes - ip method
	inline double GetRecoPhiPlus_ipmeth(){ return recoPhiPlus_ipmeth; }
	inline double GetRecoPhiMinus_ipmeth(){ return recoPhiMinus_ipmeth; }
	inline double GetRecoPhiStarPlus_ipmeth(){ return recoPhiStarPlus_ipmeth; }
	inline double GetRecoPhiStarMinus_ipmeth(){ return recoPhiStarMinus_ipmeth; }
	// get functions for azimuthal angle of tau decay planes - comb method
	inline double GetRecoPhiPlus_combmeth(){ return recoPhiPlus_combmeth; }
	inline double GetRecoPhiMinus_combmeth(){ return recoPhiMinus_combmeth; }
	inline double GetRecoPhiStarPlus_combmeth(){ return recoPhiStarPlus_combmeth; }
	inline double GetRecoPhiStarMinus_combmeth(){ return recoPhiStarMinus_combmeth; }
	// get functions for azimuthal angle of tau decay planes - rho method
	inline double GetRecoPhiPlus_rhometh(){ return recoPhiPlus_rhometh; }
	inline double GetRecoPhiMinus_rhometh(){ return recoPhiMinus_rhometh; }
	inline double GetRecoPhiStarPlus_rhometh(){ return recoPhiStarPlus_rhometh; }
	inline double GetRecoPhiStarMinus_rhometh(){ return recoPhiStarMinus_rhometh; }
private:
	double genPhiStar;
	double genOStarCP;
	double genPhi;
	double genOCP;
	double recoPhiStar;
	double recoOStarCP;
	double recoIP1;
	double recoIP2;
	double recoPhiPlus_ipmeth;
	double recoPhiMinus_ipmeth;
	double recoPhiStarPlus_ipmeth;
	double recoPhiStarMinus_ipmeth;
	double recoPhiPlus_combmeth;
	double recoPhiMinus_combmeth;
	double recoPhiStarPlus_combmeth;
	double recoPhiStarMinus_combmeth;
	double recoPhiPlus_rhometh;
	double recoPhiMinus_rhometh;
	double recoPhiStarPlus_rhometh;
	double recoPhiStarMinus_rhometh;
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
	inline void SetRecoPhiPlus_ipmeth(double recophiplus_ipmeth){ recoPhiPlus_ipmeth = recophiplus_ipmeth; }
	inline void SetRecoPhiMinus_ipmeth(double recophiminus_ipmeth){ recoPhiMinus_ipmeth = recophiminus_ipmeth; }
	inline void SetRecoPhiStarPlus_ipmeth(double recophistarplus_ipmeth){ recoPhiStarPlus_ipmeth = recophistarplus_ipmeth; }
	inline void SetRecoPhiStarMinus_ipmeth(double recophistarminus_ipmeth){ recoPhiStarMinus_ipmeth = recophistarminus_ipmeth; }
	// set functions for azimuthal angle of tau decay planes - comb method
	inline void SetRecoPhiPlus_combmeth(double recophcomblus_combmeth){ recoPhiPlus_combmeth = recophcomblus_combmeth; }
	inline void SetRecoPhiMinus_combmeth(double recophiminus_combmeth){ recoPhiMinus_combmeth = recophiminus_combmeth; }
	inline void SetRecoPhiStarPlus_combmeth(double recophistarplus_combmeth){ recoPhiStarPlus_combmeth = recophistarplus_combmeth; }
	inline void SetRecoPhiStarMinus_combmeth(double recophistarminus_combmeth){ recoPhiStarMinus_combmeth = recophistarminus_combmeth; }
	// set functions for azimuthal angle of tau decay planes - rho method
	inline void SetRecoPhiPlus_rhometh(double recophrholus_rhometh){ recoPhiPlus_rhometh = recophrholus_rhometh; }
	inline void SetRecoPhiMinus_rhometh(double recophiminus_rhometh){ recoPhiMinus_rhometh = recophiminus_rhometh; }
	inline void SetRecoPhiStarPlus_rhometh(double recophistarplus_rhometh){ recoPhiStarPlus_rhometh = recophistarplus_rhometh; }
	inline void SetRecoPhiStarMinus_rhometh(double recophistarminus_rhometh){ recoPhiStarMinus_rhometh = recophistarminus_rhometh; }
};
