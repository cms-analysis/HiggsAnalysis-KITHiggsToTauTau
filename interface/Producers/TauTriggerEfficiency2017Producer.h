#pragma once

#include "Artus/Core/interface/ProducerBase.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"
#include "TFile.h"
#include "TGraphAsymmErrors.h"
#include "TauAnalysisTools/TauTriggerSFs/interface/TauTriggerSFs2017.h"

/**
   \brief TauTrigger2017EfficiencyProducer
   Config tags:
   - Fill me with something meaningful
*/

class TauTriggerEfficiency2017Producer: public ProducerBase<HttTypes> {
public:

	virtual std::string GetProducerId() const override;

	virtual void Init(setting_type const& settings, metadata_type& metadata) override;

	virtual void Produce(event_type const& event, product_type& product,
						 setting_type const& settings, metadata_type const& metadata) const override;

private:
        TauTriggerSFs2017* TauSFs;
};
