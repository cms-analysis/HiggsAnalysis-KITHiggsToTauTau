
#pragma once

#include "Kappa/DataFormats/interface/Kappa.h"

/**
   \brief Place to collect functions calculating generic physical quantities
   -Mt: transverse mass, under the approximation of massless objects
*/
	
typedef ROOT::Math::DisplacementVector3D<ROOT::Math::Cartesian3D<float>,ROOT::Math::DefaultCoordinateSystemTag> RMDataV;


class Quantities {

public:
	
	static double CalculateMt(RMDataLV const& vector1, RMDataLV const& vector2);
	
	static RMDataV Zeta(RMDataLV const& lepton1, RMDataLV const& lepton2);
	static double PZetaVis(RMDataLV const& lepton1, RMDataLV const& lepton2);
	static double PZetaMissVis(RMDataLV const& lepton1, RMDataLV const& lepton2,
	                           RMDataLV const& met, float alpha=0.85);

private:
	Quantities() {  };
};
