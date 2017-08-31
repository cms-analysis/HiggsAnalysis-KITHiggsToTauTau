
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

	virtual std::string GetProducerId() const override
	{
		return "AntiTtbarDiscriminatorTmvaReader";
	}
	
	AntiTtbarDiscriminatorTmvaReader();
	
	virtual void Init(setting_type const& settings, metadata_type& metadata) override;
	
	virtual void Produce(event_type const& event, product_type& product,
	                     setting_type const& settings, metadata_type const& metadata) const override;

};

class TauPolarisationTmvaReader: public TmvaClassificationReaderBase<HttTypes>
{
public:

	virtual std::string GetProducerId() const override
	{
		return "TauPolarisationTmvaReader";
	}
	
	TauPolarisationTmvaReader();
	
	virtual void Init(setting_type const& settings, metadata_type& metadata) override;
	
	virtual void Produce(event_type const& event, product_type& product,
	                     setting_type const& settings, metadata_type const& metadata) const override;

};

