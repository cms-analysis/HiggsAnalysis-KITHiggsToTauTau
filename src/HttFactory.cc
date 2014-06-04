
#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttFactory.h"

// producers
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/HttValidElectronsProducer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/HttValidMuonsProducer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/HttValidTausProducer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/MetSelectors.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/HttValidJetsProducer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/HttValidBTaggedJetsProducer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/DecayChannelProducer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/TauSpinnerProducer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/GenTauCPProducer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/RecoTauCPProducer.h"

// filters
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Filters/PreselectionFilter.h"

// consumers
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Consumers/HttLambdaNtupleConsumer.h"


HttProducerBase * HttFactory::createProducer ( std::string const& id )
{
	if(id == HttValidElectronsProducer().GetProducerId())
		return new HttValidElectronsProducer();
	else if(id == HttValidMuonsProducer().GetProducerId())
		return new HttValidMuonsProducer();
	else if(id == HttValidTausProducer().GetProducerId())
		return new HttValidTausProducer();
	else if(id == MetSelector().GetProducerId())
		return new MetSelector();
	else if(id == MvaMetTTSelector().GetProducerId())
		return new MvaMetTTSelector();
	else if(id == MvaMetMTSelector().GetProducerId())
		return new MvaMetMTSelector();
	else if(id == MvaMetETSelector().GetProducerId())
		return new MvaMetETSelector();
	else if(id == MvaMetEMSelector().GetProducerId())
		return new MvaMetEMSelector();
	else if(id == HttValidJetsProducer().GetProducerId())
		return new HttValidJetsProducer();
	else if(id == HttValidTaggedJetsProducer().GetProducerId())
		return new HttValidTaggedJetsProducer();
	else if(id == HttValidBTaggedJetsProducer().GetProducerId())
		return new HttValidBTaggedJetsProducer();
	else if(id == DecayChannelProducer().GetProducerId())
  		return new DecayChannelProducer();
    if(id == TauSpinnerProducer().GetProducerId())
        return new TauSpinnerProducer();
	else if(id == GenTauCPProducer().GetProducerId())
		return new GenTauCPProducer();
	else if(id == RecoTauCPProducer().GetProducerId())
		return new RecoTauCPProducer();
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
