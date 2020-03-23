
#pragma once

#include "Kappa/DataFormats/interface/Kappa.h"
#include "Artus/Utility/interface/ArtusLogging.h"
#include "TVector2.h"
#include "TVector.h"
#include "TMatrixTSym.h"

/**
   \brief Place to collect functions calculating generic physical quantities
   -Mt: transverse mass, under the approximation of massless objects
*/
	
typedef ROOT::Math::DisplacementVector3D<ROOT::Math::Cartesian3D<float>,ROOT::Math::DefaultCoordinateSystemTag> RMDataV;


class Quantities {

public:
	static double CalculateMtH2Tau(RMFLV const& vector1, RMFLV const& vector2);
	static double CalculateMt(RMFLV const& vector1, RMFLV const& vector2);
	static double CalculateMtVar(RMFLV const& vector1, RMFLV const& vector2);

	static RMDataV Zeta(RMFLV const& lepton1, RMFLV const& lepton2);
	static double PZetaVis(RMFLV const& lepton1, RMFLV const& lepton2);
	static double PZetaMissVis(RMFLV const& lepton1, RMFLV const& lepton2,
	                           RMFLV const& met, float alpha=0.85);

	static double MetChiSquare(TVector2 const& v, ROOT::Math::SMatrix<double, 2> matrix);
private:
	Quantities() {  };
};
