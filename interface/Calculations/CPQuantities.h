
#pragma once

#include <utility>

#include "Kappa/DataFormats/interface/Kappa.h"
#include "Artus/Utility/interface/ArtusLogging.h"

/**
   \brief Place to collect functions calculating CP quantities
   -Phi* : this is a variable, with which one can say, whether the considered boson is a scalar (CP even) or a pseudoscalar (CP odd)
   -Psi*CP : this is a variable, with which one can figure out, whether the have a CP-mixture or not
   -Zs : this is a variable, with which one can figure out, wether the considered boson is a scalar (CP even) or a pseudoscalar (CP odd)
*/

class CPQuantities
{
public:
	double CalculatePhiStarCP(RMDataLV tau1, RMDataLV tau2, RMDataLV chargPart1, RMDataLV chargPart2);
	double CalculatePhiStarCP(KDataVertex pv , KDataTrack track1, KDataTrack track2, RMDataLV chargPart1,RMDataLV chargPart2);
	double CalculateChargedHadronEnergy(RMDataLV diTauMomentum, RMDataLV chargHad);
	double CalculatePhiCP(RMDataLV boson, RMDataLV tau1, RMDataLV tau2, RMDataLV pion1, RMDataLV pion2);
	double CalculateChargedProngEnergy(RMDataLV tau, RMDataLV chargedProng);
	double CalculateChargedProngEnergyApprox(RMDataLV tau, RMDataLV chargedProng);
	double CalculateThetaNuHadron(RMDataLV tau, RMDataLV nuTau, RMDataLV hadron);
	double CalculateAlphaTauNeutrinos(RMDataLV tauM, RMDataLV nuTauM, RMDataLV tauP, RMDataLV nuTauP);
	double CalculateTrackReferenceError(KDataTrack track);
	double CalculateZPlusMinus(RMDataLV higgs, RMDataLV chargedPart);
	double CalculateZs(double zPlus, double zMinus);
	double PhiTransform(double phi);
	inline double GetGenPhiStar()
	{
		return genPhiStar;
	}
	inline double GetGenPhi()
	{
		return genPhi;
	}
	inline double GetRecoPhiStar()
	{
		return recoPhiStar;
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
	double genPhi;
	double recoPhiStar;
	double recoIP1;
	double recoIP2;
	//level: "gen", "reco" 
	double CalculatePhiStarCPSame(RMDataLV::BetaVector k1, RMDataLV::BetaVector k2, RMDataLV chargPart1, RMDataLV chargPart2, std::string level);
	inline void SetGenPhiStar(double genphistar)
	{
		genPhiStar = genphistar;
	}
	inline void SetGenPhi(double genphi)
	{
		genPhi = genphi;
	}
	inline void SetRecoPhiStar(double recophistar)
	{
		recoPhiStar = recophistar;
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
