
#pragma once

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"


/** Check that the generator-level di-tau pair passes acceptance
 *  requirements on pseudorapidity and transverse momentum
 */
class GenDiTauPairAcceptanceProducer: public ProducerBase<HttTypes>
{
public:

	virtual std::string GetProducerId() const override {
		return "GenDiTauPairAcceptanceProducer";
	}
	
	virtual void Init(setting_type const& settings, metadata_type& metadata) override;
	
	virtual void Produce(event_type const& event, product_type& product,
	                     setting_type const& settings, metadata_type const& metadata) const override;

};
