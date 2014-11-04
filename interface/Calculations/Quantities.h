
#pragma once

#include "Kappa/DataFormats/interface/Kappa.h"

/**
   \brief Place to collect functions calculating generic physical quantities
   -Mt: transverse mass, under the approximation of massless objects
*/

class Quantities {

public:
	static double CalculateMt(const RMDataLV vector1, const RMDataLV vector2);

private:
	Quantities() {  };
};
