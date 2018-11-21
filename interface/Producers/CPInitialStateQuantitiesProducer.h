
#pragma once

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"
#include "Artus/KappaAnalysis/interface/KappaProducerBase.h"

#include "Artus/KappaAnalysis/interface/Utility/ValidPhysicsObjectTools.h"


class CPInitialStateQuantitiesProducer : public ProducerBase<HttTypes> {
public:

	virtual ~CPInitialStateQuantitiesProducer();
	
	virtual std::string GetProducerId() const override;

	virtual void Init(setting_type const& settings, metadata_type& metadata) override;

	void Produce(event_type const& event, product_type& product,
                 setting_type const& settings, metadata_type const& metadata) const override;
};
