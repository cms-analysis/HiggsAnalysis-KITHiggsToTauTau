#pragma once

#include "Artus/Utility/interface/Utility.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Calculations/CPQuantities.h"
#include "Artus/Utility/interface/DefaultValues.h"

/**
   \brief
*/

class RecoTauCPProducer : public HttProducerBase {
public:
	
	virtual std::string GetProducerId() const ARTUS_CPP11_OVERRIDE {
		return "reco_cp";
	}
	
	virtual void InitGlobal(global_setting_type const& globalSettings)  ARTUS_CPP11_OVERRIDE
	{
		ProducerBase<HttTypes>::InitGlobal(globalSettings);
	}
	
	virtual void InitLocal(setting_type const& settings)  ARTUS_CPP11_OVERRIDE
	{
		ProducerBase<HttTypes>::InitLocal(settings);
	}

	virtual void ProduceGlobal(HttEvent const& event, HttProduct& product,
	                           HttGlobalSettings const& globalSettings) const ARTUS_CPP11_OVERRIDE;
};