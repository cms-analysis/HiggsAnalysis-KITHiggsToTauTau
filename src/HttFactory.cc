
#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttFactory.h"

// producers
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/ElectronEtaSelector.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/HttTauCorrectionsProducer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/HttValidElectronsProducer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/HttValidMuonsProducer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/HttValidTausProducer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/HttValidJetsProducer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/MetSelectors.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/TTHTauPairProducer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/DecayChannelProducer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/EventCategoryProducer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/DataMcScaleFactorProducers.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/DiLeptonQuantitiesProducer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/DiJetQuantitiesProducer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/SvfitProducer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/TauTauRestFrameSelector.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/TauSpinnerProducer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/GenTauCPProducer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/RecoTauCPProducer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/HttTmvaClassificationReaders.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/HttValidGenTausProducer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/HttTriggerSettingsProducer.h"

// filters
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Filters/LooseObjectsCountFilters.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Filters/MaxLooseObjectsCountFilters.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Filters/DiLeptonVetoFilters.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Filters/RecoMuonInElectronConeVetoFilter.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Filters/DecayChannelFilter.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Filters/DiLeptonChargeFilter.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Filters/EventCategoryFilter.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Filters/ZBosonVetoFilter.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Filters/HttObjectsCutFilters.h"

// consumers
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Consumers/HttLambdaNtupleConsumer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Consumers/SvfitCacheConsumer.h"


ProducerBaseUntemplated * HttFactory::createProducer(std::string const& id)
{
	if(id == ElectronEtaSelector().GetProducerId())
		return new ElectronEtaSelector();
	else if(id == HttTauCorrectionsProducer().GetProducerId())
		return new HttTauCorrectionsProducer();
	else if(id == HttValidElectronsProducer().GetProducerId())
		return new HttValidElectronsProducer();
	else if(id == HttValidLooseElectronsProducer().GetProducerId())
		return new HttValidLooseElectronsProducer();
	else if(id == HttValidVetoElectronsProducer().GetProducerId())
		return new HttValidVetoElectronsProducer();
	else if(id == HttValidMuonsProducer().GetProducerId())
		return new HttValidMuonsProducer();
	else if(id == HttValidLooseMuonsProducer().GetProducerId())
		return new HttValidLooseMuonsProducer();
	else if(id == HttValidVetoMuonsProducer().GetProducerId())
		return new HttValidVetoMuonsProducer();
	else if(id == HttValidTausProducer().GetProducerId())
		return new HttValidTausProducer();
	else if(id == HttValidJetsProducer().GetProducerId())
		return new HttValidJetsProducer();
	else if(id == HttValidTaggedJetsProducer().GetProducerId())
		return new HttValidTaggedJetsProducer();
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
	else if(id == TTHTauPairProducer().GetProducerId())
		return new TTHTauPairProducer();
	else if(id == DecayChannelProducer().GetProducerId())
		return new DecayChannelProducer();
	else if(id == TTHDecayChannelProducer().GetProducerId())
		return new TTHDecayChannelProducer();
	else if(id == Run2DecayChannelProducer().GetProducerId())
		return new Run2DecayChannelProducer();
	else if(id == EventCategoryProducer().GetProducerId())
		return new EventCategoryProducer();
	else if(id == TTHEventCategoryProducer().GetProducerId())
		return new TTHEventCategoryProducer();
	else if(id == TriggerWeightProducer().GetProducerId())
		return new TriggerWeightProducer();
	else if(id == IdentificationWeightProducer().GetProducerId())
		return new IdentificationWeightProducer();
	if(id == TauSpinnerProducer().GetProducerId())
		return new TauSpinnerProducer();
	if(id == DiLeptonQuantitiesProducer().GetProducerId())
		return new DiLeptonQuantitiesProducer();
	if(id == DiJetQuantitiesProducer().GetProducerId())
		return new DiJetQuantitiesProducer();
	if(id == SvfitProducer().GetProducerId())
		return new SvfitProducer();
	if(id == TauTauRestFrameSelector().GetProducerId())
		return new TauTauRestFrameSelector();
	else if(id == GenTauCPProducer().GetProducerId())
		return new GenTauCPProducer();
	else if(id == RecoTauCPProducer().GetProducerId())
		return new RecoTauCPProducer();
	else if(id == AntiTtbarDiscriminatorTmvaReader().GetProducerId())
		return new AntiTtbarDiscriminatorTmvaReader();
	else if(id == HttValidGenTausProducer().GetProducerId())
		return new HttValidGenTausProducer();
	else if(id == HttTriggerSettingsProducer().GetProducerId())
		return new HttTriggerSettingsProducer();
	else
		return KappaFactory::createProducer( id );
}

FilterBaseUntemplated * HttFactory::createFilter(std::string const& id)
{
	if(id == LooseElectronsCountFilter().GetFilterId())
		return new LooseElectronsCountFilter();
	else if(id == LooseMuonsCountFilter().GetFilterId())
		return new LooseMuonsCountFilter();
	else if(id == MaxLooseElectronsCountFilter().GetFilterId())
		return new MaxLooseElectronsCountFilter();
	else if(id == MaxLooseMuonsCountFilter().GetFilterId())
		return new MaxLooseMuonsCountFilter();
	else if(id == DiVetoElectronVetoFilter().GetFilterId())
		return new DiVetoElectronVetoFilter();
	else if(id == DiVetoMuonVetoFilter().GetFilterId())
		return new DiVetoMuonVetoFilter();
	else if(id == RecoMuonInElectronConeVetoFilter().GetFilterId())
		return new RecoMuonInElectronConeVetoFilter();
	else if(id == DecayChannelFilter().GetFilterId())
		return new DecayChannelFilter();
	else if(id == DiLeptonChargeFilter().GetFilterId())
		return new DiLeptonChargeFilter();
	else if(id == EventCategoryFilter().GetFilterId())
		return new EventCategoryFilter();
	else if(id == ZBosonVetoFilter().GetFilterId())
		return new ZBosonVetoFilter();
	else if(id == MetLowerPtCutsFilter().GetFilterId())
		return new MetLowerPtCutsFilter();
	else if(id == MetUpperPtCutsFilter().GetFilterId())
		return new MetUpperPtCutsFilter();
	else
		return KappaFactory::createFilter( id );
}

ConsumerBaseUntemplated * HttFactory::createConsumer (std::string const& id)
{
	if(id == HttLambdaNtupleConsumer().GetConsumerId())
		return new HttLambdaNtupleConsumer();
	else if(id == SvfitCacheConsumer().GetConsumerId())
		return new SvfitCacheConsumer();
	else
		return KappaFactory::createConsumer( id );
}

