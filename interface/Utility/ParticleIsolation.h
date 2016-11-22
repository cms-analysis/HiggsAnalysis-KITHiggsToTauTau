
#pragma once

#include "Artus/Utility/interface/ArtusLogging.h"

#include <Math/VectorUtil.h>

#include "Kappa/DataFormats/interface/Kappa.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"


/**
   \brief Calculate isolation quantities for particles
*/

class ParticleIsolation {

public:

	static double IsolationPtSum(RMFLV const& particle, HttProduct const& product,
	                             float const& isoSignalConeSize = 0.4,
	                             float const& deltaBetaCorrectionFactor = 0.5,
	                             float const& chargedIsoVetoConeSizeEB = -1.0,
	                             float const& chargedIsoVetoConeSizeEE = -1.0,
	                             float const& neutralIsoVetoConeSize = -1.0,
	                             float const& photonIsoVetoConeSizeEB = -1.0,
	                             float const& photonIsoVetoConeSizeEE = -1.0,
	                             float const& deltaBetaIsoVetoConeSize = -1.0,
	                             float const& chargedIsoPtThreshold = 0.0,
	                             float const& neutralIsoPtThreshold = 0.0,
	                             float const& photonIsoPtThreshold = 0.0,
	                             float const& deltaBetaIsoPtThreshold = 0.0);

	static double IsolationPtSumForParticleClass(RMFLV const& particle, std::vector<const KPFCandidate*> pfCandidates,
	                                             float const& isoSignalConeSize = 0.4,
	                                             float const& isoVetoConeSizeEB = -1.0,
	                                             float const& isoVetoConeSizeEE = -1.0,
	                                             float const& isoPtThreshold = 0.0);

private:
	ParticleIsolation() {  };
};
