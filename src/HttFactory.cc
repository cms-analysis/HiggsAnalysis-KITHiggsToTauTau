
#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttFactory.h"

// producers
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/HttValidElectronsProducer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/HttValidMuonsProducer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/HttValidTausProducer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/HttValidMetProducer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/DecayChannelProducer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/TauSpinnerProducer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/EventWeightProducer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/GenTauCPProducer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/TauDiscriminatorsProducer.h"

// filters
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Filters/PreselectionFilter.h"

// consumers
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Consumers/HttLambdaNtupleConsumer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Consumers/HttCutFlowHistogramConsumer.h"


HttProducerBase * HttFactory::createProducer ( std::string const& id )
{
	if(id == HttValidElectronsProducer().GetProducerId())
		return new HttValidElectronsProducer();
	else if(id == HttValidMuonsProducer().GetProducerId())
		return new HttValidMuonsProducer();
	else if(id == HttValidTausProducer().GetProducerId())
		return new HttValidTausProducer();
	else if(id == HttValidMvaMetTTProducer().GetProducerId())
		return new HttValidMvaMetTTProducer();
	else if(id == HttValidMvaMetMTProducer().GetProducerId())
		return new HttValidMvaMetMTProducer();
	else if(id == HttValidMvaMetETProducer().GetProducerId())
		return new HttValidMvaMetETProducer();
	else if(id == HttValidMvaMetEMProducer().GetProducerId())
		return new HttValidMvaMetEMProducer();
	else if(id == DecayChannelProducer().GetProducerId())
  		return new DecayChannelProducer();
    if(id == TauSpinnerProducer().GetProducerId())
        return new TauSpinnerProducer();
	else if(id == EventWeightProducer().GetProducerId())
		return new EventWeightProducer();
	else if(id == GenTauCPProducer().GetProducerId())
		return new GenTauCPProducer();
	else if(id == TauDiscriminatorsProducer().GetProducerId())
		return new TauDiscriminatorsProducer();
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
	else if(id == HttCutFlowHistogramConsumer().GetConsumerId())
		return new HttCutFlowHistogramConsumer();
	else
		return KappaFactory<HttTypes>::createConsumer( id );
}
