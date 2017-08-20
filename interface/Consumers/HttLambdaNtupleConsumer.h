
#pragma once

#include "Artus/KappaAnalysis/interface/Consumers/KappaLambdaNtupleConsumer.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"


class HttLambdaNtupleConsumer: public KappaLambdaNtupleConsumer<HttTypes> {
public:

	virtual void Init(setting_type const& settings, metadata_type& metadata) override;
};
