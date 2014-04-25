
#pragma once

#include "Artus/Utility/interface/Utility.h"

#include "TauSpinner/SimpleParticle.h"
#include "TauSpinner/tau_reweight_lib.h"

#include "../HttTypes.h"

/**
   \brief GlobalProducer, for tau decays on generator level. Following quantities are calculated:
   
   -This producer has the product of the GenTauDecayProducer as input and calculates the TauSpinnerWeight 
   for these particles, where tau is the daughter of Higgs

*/

class TauSpinnerProducer: public HttProducerBase {
public:
	
	virtual std::string GetProducerId() const ARTUS_CPP11_OVERRIDE {
		return "tauspinner";
	}
	
	TauSpinnerProducer() : HttProducerBase() {};

	void InitGlobal(global_setting_type const& globalSettings) ARTUS_CPP11_OVERRIDE;
	

	virtual void ProduceGlobal(HttEvent const& event, HttProduct& product,
	                           HttGlobalSettings const& globalSettings) const ARTUS_CPP11_OVERRIDE;
	
};


