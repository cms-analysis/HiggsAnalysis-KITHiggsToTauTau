
#pragma once

// #include "Artus/Core/interface/FilterBase.h"
#include "Artus/Core/interface/ProducerBase.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"
// #include "HiggsAnalysis/KITHiggsToTauTau/interface/HttEnumTypes.h"
#include "Artus/Consumer/interface/LambdaNtupleConsumer.h"
// #include "Artus/Utility/interface/DefaultValues.h"

/** producer for the met-filtering.
 *  Required config tag:
 *  - MetFilter
 */

class MetFilterProducer : public ProducerBase<HttTypes> {
public:

	virtual ~MetFilterProducer();
	
	virtual std::string GetProducerId() const override;

	virtual void Init(setting_type const& settings, metadata_type& metadata) override;

	virtual void Produce(event_type const& event, product_type& product,
                 setting_type const& settings, metadata_type const& metadata) const override;

private:
    std::vector<std::string> m_metFilters;
    std::vector<std::string> m_invertedFilters;

protected:

};

