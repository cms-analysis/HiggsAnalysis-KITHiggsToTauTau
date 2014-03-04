
#pragma once

#include "Artus/Core/interface/Cpp11Support.h"

#include "Artus/KappaAnalysis/interface/KappaFactory.h"

#include "HttTypes.h"

// producer
#include "Producers/DecayChannelProducer.h"

// filter
#include "Filters/PreselectionFilter.h"

// consumer
#include "Consumers/HttLambdaNtupleConsumer.h"


class HttFactory: public KappaFactory<HttTypes> {
public:

	HttFactory() : KappaFactory<HttTypes>() {
	}

	virtual ~HttFactory() {}

	virtual ProducerBase<HttTypes> * createProducer ( std::string const& id )
		ARTUS_CPP11_OVERRIDE
	{
		if(id == DecayChannelProducer().GetProducerId())
	  		return new DecayChannelProducer();
		else
			return KappaFactory<HttTypes>::createProducer( id );	
	}

	virtual FilterBase<HttTypes> * createFilter ( std::string const& id )
		ARTUS_CPP11_OVERRIDE
	{
		if(id == PreselectionFilter().GetFilterId())
	  		return new PreselectionFilter();
		else
			return KappaFactory<HttTypes>::createFilter( id );
	}

	virtual ConsumerBase<HttTypes> * createConsumer ( std::string const& id )
		ARTUS_CPP11_OVERRIDE
	{
		if(id == HttLambdaNtupleConsumer().GetConsumerId())
			return new HttLambdaNtupleConsumer();
		else
			return KappaFactory<HttTypes>::createConsumer( id );
	}

};
