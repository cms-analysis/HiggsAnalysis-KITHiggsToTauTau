
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Calculations/Quantities.h"

// transverse mass in the approximation of massless objects
double Quantities::CalculateMt(RMFLV const& vector1, RMFLV const& vector2)
{
	return sqrt(2 * vector1.Pt() * vector2.Pt() * (1. - cos(vector1.Phi() - vector2.Phi())));
}

RMDataV Quantities::Zeta(RMFLV const& lepton1, RMFLV const& lepton2)
{
	RMDataV v1 = lepton1.Vect().Unit();
	RMDataV v2 = lepton2.Vect().Unit();
	v1.SetZ(0.0);
	v2.SetZ(0.0);
	v1 = v1.Unit();
	v2 = v2.Unit();
	return (v1 + v2).Unit();
}

double Quantities::PZetaVis(RMFLV const& lepton1, RMFLV const& lepton2)
{
	RMDataV diLeptonV = lepton1.Vect() + lepton2.Vect();
	diLeptonV.SetZ(0.0);
	return diLeptonV.Dot(Quantities::Zeta(lepton1, lepton2));
}

double Quantities::PZetaMissVis(RMFLV const& lepton1, RMFLV const& lepton2,
                                RMFLV const& met, float alpha)
{
	RMDataV metV = met.Vect();
	metV.SetZ(0.0);
	return (metV.Dot(Quantities::Zeta(lepton1, lepton2)) - (alpha * Quantities::PZetaVis(lepton1, lepton2)));
}
