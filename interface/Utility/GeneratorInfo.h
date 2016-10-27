
#pragma once

#include "Kappa/DataFormats/interface/Kappa.h"
#include "Artus/Utility/interface/SafeMap.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttEnumTypes.h"

/**
   \brief Place to collect functions of general use
*/
	


class GeneratorInfo {

public:
	static HttEnumTypes::GenMatchingCode GetGenMatchingCode(KGenParticle* genParticle);
	static RMFLV* GetVisibleLV(KGenParticle* genParticle);
	
	static KGenParticle* GetGenMatchedParticle(
			KLepton* lepton,
			std::map<KLepton*, KGenParticle*> const& leptonGenParticleMap,
			std::map<KTau*, KGenTau*> const& tauGenTauMap
	);

private:
	GeneratorInfo() {  };
};
