
#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttFactory.h"

// producers
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/DecayChannelProducer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/EventWeightProducer.h"

// filters
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Filters/PreselectionFilter.h"

// consumers
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Consumers/HttLambdaNtupleConsumer.h"


HttProducerBase * HttFactory::createProducer ( std::string const& id )
{
	if(id == DecayChannelProducer().GetProducerId())
		return new DecayChannelProducer();
	else if(id == EventWeightProducer().GetProducerId())
		return new EventWeightProducer();
	else
		return KappaFactory<HttTypes>::createProducer( id );	
}

HttFilterBase * HttFactory::createFilter ( std::string const& id )
{
	if(id == PreselectionFilter().GetFilterId())
		return new PreselectionFilter();
	else
		return KappaFactory<HttTypes>::createFilter( id );
}

HttConsumerBase * HttFactory::createConsumer ( std::string const& id )
{
	if(id == HttLambdaNtupleConsumer().GetConsumerId())
		return new HttLambdaNtupleConsumer();
	else
		return KappaFactory<HttTypes>::createConsumer( id );
}
