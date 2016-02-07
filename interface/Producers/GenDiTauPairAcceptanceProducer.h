
#pragma once

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"


/** Check that the generator-level di-tau pair passes acceptance
 *  requirements on pseudorapidity and transverse momentum
 */
class GenDiTauPairAcceptanceProducer: public ProducerBase<HttTypes>
{
public:

	typedef typename HttTypes::event_type event_type;
	typedef typename HttTypes::product_type product_type;
	typedef typename HttTypes::setting_type setting_type;
	
	virtual std::string GetProducerId() const override {
		return "GenDiTauPairAcceptanceProducer";
	}
	
	virtual void Init(setting_type const& settings) override;
	
	virtual void Produce(event_type const& event, product_type& product,
	                     setting_type const& settings) const override;

};
