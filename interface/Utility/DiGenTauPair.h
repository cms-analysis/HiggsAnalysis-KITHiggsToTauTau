
#pragma once

#include "Kappa/DataFormats/interface/Kappa.h"


class DiGenTauPair : public std::pair<KLV*, KLV*>
{
public:
	DiGenTauPair(KLV* lepton1, KLV* lepton2);
	
	double GetDeltaR();
};
