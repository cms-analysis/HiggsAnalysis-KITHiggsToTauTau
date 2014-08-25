
#pragma once

#include "Artus/KappaAnalysis/interface/Producers/TmvaClassificationReaderBase.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"


/**
   \brief Producer for discriminator agains TTbar (as used in the EM channel)
   
   Required config tags:
   - AntiTtbarTmvaInputQuantities
   - AntiTtbarTmvaMethods
   - AntiTtbarTmvaWeights (same length as for AntiTtbarTmvaMethods required)
*/
class AntiTtbarDiscriminatorTmvaReader: public TmvaClassificationReaderBase<HttTypes>
{
public:

	typedef typename HttTypes::event_type event_type;
	typedef typename HttTypes::product_type product_type;
	typedef typename HttTypes::setting_type setting_type;

	virtual std::string GetProducerId() const ARTUS_CPP11_OVERRIDE
	{
		return "AntiTtbarDiscriminatorTmvaReader";
	}
	
	AntiTtbarDiscriminatorTmvaReader();

};

