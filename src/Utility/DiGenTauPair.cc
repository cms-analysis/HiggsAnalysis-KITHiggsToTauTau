
#include <Math/VectorUtil.h>

#include "Artus/Utility/interface/Utility.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/Utility/DiGenTauPair.h"


DiGenTauPair::DiGenTauPair(KLV* lepton1, KLV* lepton2) :
	std::pair<KLV*, KLV*>(lepton1, lepton2)
{
}

double DiGenTauPair::GetDeltaR()
{
	return ROOT::Math::VectorUtil::DeltaR(first->p4, second->p4);
}
