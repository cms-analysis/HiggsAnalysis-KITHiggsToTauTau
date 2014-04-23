
#pragma once

#include "Kappa/DataFormats/interface/Kappa.h"

#include "Artus/Core/interface/GlobalInclude.h"

#include "../HttTypes.h"

/**
Producer to check the tau discriminators

Runs equally as global and local producer and takes a list of strings in the tag
"TauDiscriminators" as configuration. These are the names of the tau discriminators
that have to have fired. One can specify pt-dependent lists of discriminators by
putting the index (int) before the discriminator name separated by ":" (example
<index>:<discriminator>). This producer modifies the lists of (in-) valid taus.
*/

class TauDiscriminatorsProducer: public HttProducerBase
{

public:

	typedef typename HttTypes::event_type event_type;
	typedef typename HttTypes::product_type product_type;
	typedef typename HttTypes::global_setting_type global_setting_type;
	typedef typename HttTypes::setting_type setting_type;

	virtual std::string GetProducerId() const ARTUS_CPP11_OVERRIDE {
		return "tau_discriminators";
	}

	virtual void ProduceGlobal(event_type const& event,
	                           product_type& product,
	                           global_setting_type const& globalSettings) const ARTUS_CPP11_OVERRIDE;

	virtual void ProduceLocal(event_type const& event,
	                          product_type& product,
	                          setting_type const& settings) const ARTUS_CPP11_OVERRIDE;


private:

	// function that lets this producer work as both a global and a local producer
	void Produce(event_type const& event, product_type& product, stringvector discriminatorNames) const;
};

