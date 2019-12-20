#pragma once

#include "Artus/Core/interface/ProducerBase.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"
#include "TFile.h"
#include "TGraphAsymmErrors.h"
#include "TauAnalysisTools/TauTriggerSFs/interface/SFProvider.h"

/**
   \brief DeepTauTriggerScaleFactorProducer
   Config tags:
   - Fill me with something meaningful
*/

// class tau_trigger::SFProvider;

class DeepTauTriggerScaleFactorProducer: public ProducerBase<HttTypes> {
public:

	virtual std::string GetProducerId() const override;

	virtual void Init(setting_type const& settings, metadata_type& metadata) override;

	virtual void Produce(event_type const& event, product_type& product,
						 setting_type const& settings, metadata_type const& metadata) const override;

private:
	std::vector<std::shared_ptr<tau_trigger::SFProvider> > TauSFs;
};
