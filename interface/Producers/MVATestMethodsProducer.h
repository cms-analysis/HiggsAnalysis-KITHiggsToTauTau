
#pragma once

#include "Artus/KappaAnalysis/interface/Producers/TmvaClassificationMultiReaderBase.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"


/**
   \brief Producer for discriminator agains TTbar (as used in the EM channel)
   
   Required config tags:
   - MVATestMethodsInputQuantities
   - MVATestMethodsMethods
   - MVATestMethodsWeights (same length as for MVATestMethodsMethods required)
*/
class MVATestMethodsProducer: public TmvaClassificationMultiReaderBase<HttTypes>
{
public:

	typedef KappaEvent event_type;
	typedef KappaProduct product_type;
	typedef KappaSettings setting_type;
	typedef typename HttTypes::event_type spec_event_type;
	typedef typename HttTypes::product_type spec_product_type;
	typedef typename HttTypes::setting_type spec_setting_type;

	
	virtual std::string GetProducerId() const override
	{
		return "MVATestMethodsProducer";
	}
//	 MVATestMethodsProducer();
	MVATestMethodsProducer();

	virtual void Init(spec_setting_type const& settings) override;
	
	virtual void Produce(spec_event_type const& event, spec_product_type& product,
						 spec_setting_type const& settings) const override;
};

