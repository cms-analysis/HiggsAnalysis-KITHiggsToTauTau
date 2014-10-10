
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
	static double CalculateChargedHadronEnergy(RMDataLV diTauMomentum, RMDataLV chargHad);
	double CalculatePhiCP(RMDataLV boson, RMDataLV tau1, RMDataLV tau2, RMDataLV pion1, RMDataLV pion2);
	static double CalculateChargedProngEnergy(RMDataLV tau, RMDataLV chargedProng);
	static double CalculateChargedProngEnergyApprox(RMDataLV tau, RMDataLV chargedProng);
	static double CalculateThetaNuHadron(RMDataLV tau, RMDataLV nuTau, RMDataLV hadron);
	static double CalculateAlphaTauNeutrinos(RMDataLV tauM, RMDataLV nuTauM, RMDataLV tauP, RMDataLV nuTauP);
	static double CalculateTrackReferenceError(KDataTrack track);
	static double CalculateZPlusMinus(RMDataLV higgs, RMDataLV chargedPart);
	static double CalculateZs(double zPlus, double zMinus);
	static double PhiTransform(double phi);
	double GetgenPhiStar()
	{
		return genPhiStar;
	}
	double GetgenPhi()
	{
		return genPhi;
	}
	double GetrecoPhiStar()
	{
		return recoPhiStar;
	}
	double GetrecoIP1()
	{
		return recoIP1;
	}
	double GetrecoIP2()
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
	void SetgenPhiStar(double genphistar)
	{
		genPhiStar = genphistar;
	}
	void SetgenPhi(double genphi)
	{
		genPhi = genphi;
	}
	void SetrecoPhiStar(double recophistar)
	{
		recoPhiStar = recophistar;
	}
	void SetrecoIP1(double recoip1)
	{
		recoIP1 = recoip1;
	}
	void SetrecoIP2(double recoip2)
	{
		recoIP2 = recoip2;
	}
};
