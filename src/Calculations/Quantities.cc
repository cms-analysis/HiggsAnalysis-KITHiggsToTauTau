
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Calculations/Quantities.h"

// transverse mass in the approximation of massless objects
double Quantities::CalculateMt(const RMDataLV vector1, const RMDataLV vector2)
{
	return sqrt(2 * vector1.Pt() * vector2.Pt() * (1. - cos(vector1.Phi() - vector2.Phi())));
}