
#pragma once

#include "Kappa/DataFormats/interface/Kappa.h"
#include "Artus/Utility/interface/SafeMap.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttEnumTypes.h"

/**
   \brief Place to collect functions of general use
*/
	


class GeneratorInfo {

public:
	static HttEnumTypes::GenMatchingCode GetGenMatchingCode(const KGenParticle* genParticle);
	
	static const KGenParticle* GetGenMatchedParticle(
			KLepton* lepton,
			const std::map<KLepton*, const KGenParticle*> leptonGenParticleMap,
			const std::map<KTau*, KGenTau*> tauGenTauMap
	);

private:
	GeneratorInfo() {  };
};
