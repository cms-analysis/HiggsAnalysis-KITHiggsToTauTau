
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Utility/Quantities.h"

#include <TMath.h>

// transverse mass in the H2Taus definition
// https://github.com/CERN-PH-CMG/cmg-cmssw/blob/CMGTools-from-CMSSW_7_2_3/CMGTools/H2TauTau/python/proto/physicsobjects/DiObject.py#L119
double Quantities::CalculateMtH2Tau(RMFLV const& vector1, RMFLV const& vector2)
{
	return sqrt(pow(vector1.Pt() + vector2.Pt(), 2) - pow(vector1.Px() + vector2.Px(), 2) - pow(vector1.Py() + vector2.Py(), 2));
}

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

double Quantities::cosptAngle(RMFLV const& vector1, RMFLV const& vector2)
{
	return ((vector1.X()*vector2.X())+(vector1.Y()*vector2.Y())+(vector1.Z()*vector2.Z()))/(vector1.P()*vector2.P());
}

double Quantities::MetChiSquare(TVector2 const& v, ROOT::Math::SMatrix<double, 2> matrix)
{
	TVector tmp(2);
	tmp(0) = v.X();
	tmp(1) = v.Y();
	TVector tmp2 = tmp;

	ROOT::Math::SMatrix<double, 2> invertedMatrix = matrix;
	invertedMatrix.Invert();
	TMatrixTSym<double> tmpM(2);
	tmpM(0, 0) = invertedMatrix(0,0);
	tmpM(1, 0) = invertedMatrix(1,0);
	tmpM(0, 1) = invertedMatrix(0,1);
	tmpM(1, 1) = invertedMatrix(1,1);
	tmp2 *= tmpM;
	return( tmp2 * tmp);
}
