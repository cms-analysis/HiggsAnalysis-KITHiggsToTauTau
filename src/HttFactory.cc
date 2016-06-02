
#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttFactory.h"

// producers
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/ElectronEtaSelector.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/HttElectronCorrectionsProducer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/HttMuonCorrectionsProducer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/HttTauCorrectionsProducer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/HttValidElectronsProducer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/HttValidMuonsProducer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/HttValidTausProducer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/HttValidJetsProducer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/MetSelectors.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/MetCorrectors.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/TTHTauPairProducer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/DecayChannelProducer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/EventCategoryProducer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/DataMcScaleFactorProducers.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/DiLeptonQuantitiesProducer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/DiJetQuantitiesProducer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/SvfitProducer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/MetprojectionProducer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/TauTauRestFrameSelector.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/TauSpinnerProducer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/GenTauCPProducers.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/RecoTauCPProducer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/HttTmvaClassificationReaders.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/HttValidGenTausProducer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/HttTriggerSettingsProducer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/DiLeptonVetoProducers.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/ValidDiTauPairCandidatesProducers.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/GenDiTauPairCandidatesProducers.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/GenDiTauPairAcceptanceProducer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/TriggerTagAndProbeProducers.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/MVATestMethodsProducer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/HHKinFitProducer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/MVAInputQuantitiesProducer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/AcceptanceEfficiencyProducer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/TopPtReweightingProducer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/ZPtReweightProducer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/ScaleVariationProducer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/SimpleEleTauFakeRateWeightProducer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/JetToTauFakesProducer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/PolarisationQuantitiesProducer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/SimpleFitProducer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/EmuQcdWeightProducer.h"

// filters
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Filters/LooseObjectsCountFilters.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Filters/MaxLooseObjectsCountFilters.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Filters/DiLeptonVetoFilters.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Filters/RecoMuonInElectronConeVetoFilter.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Filters/DecayChannelFilter.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Filters/DiLeptonChargeFilter.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Filters/MinimalPlotlevelFilter.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Filters/EventCategoryFilter.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Filters/ZBosonVetoFilter.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Filters/HttObjectsCutFilters.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Filters/ValidDiTauPairCandidatesFilter.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Filters/GenDiTauPairFilters.h"

// consumers
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Consumers/HttLambdaNtupleConsumer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Consumers/SvfitCacheConsumer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Consumers/TriggerTagAndProbeConsumers.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Consumers/EventCountConsumer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Consumers/EmbeddingConsumer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Consumers/BTagEffConsumer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Consumers/AcceptanceEfficiencyConsumer.h"

ProducerBaseUntemplated * HttFactory::createProducer(std::string const& id)
{
	if(id == ElectronEtaSelector().GetProducerId())
		return new ElectronEtaSelector();
	else if(id == HttElectronCorrectionsProducer().GetProducerId())
		return new HttElectronCorrectionsProducer();
	else if(id == HttMuonCorrectionsProducer().GetProducerId())
		return new HttMuonCorrectionsProducer();
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
	else if(id == MetSelectorPuppi().GetProducerId())
		return new MetSelectorPuppi();
	else if(id == MvaMetTTSelector().GetProducerId())
		return new MvaMetTTSelector();
	else if(id == MvaMetMTSelector().GetProducerId())
		return new MvaMetMTSelector();
	else if(id == MvaMetETSelector().GetProducerId())
		return new MvaMetETSelector();
	else if(id == MvaMetEMSelector().GetProducerId())
		return new MvaMetEMSelector();
	else if(id == MvaMetSelector().GetProducerId())
		return new MvaMetSelector();
	else if(id == MetCorrector().GetProducerId())
		return new MetCorrector();
	else if(id == MvaMetCorrector().GetProducerId())
		return new MvaMetCorrector();
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
	else if(id == EleTauFakeRateWeightProducer().GetProducerId())
		return new EleTauFakeRateWeightProducer();
	else if(id == MuonTauFakeRateWeightProducer().GetProducerId())
		return new MuonTauFakeRateWeightProducer();
	else if(id == TauSpinnerProducer().GetProducerId())
		return new TauSpinnerProducer();
	else if(id == DiLeptonQuantitiesProducer().GetProducerId())
		return new DiLeptonQuantitiesProducer();
	else if(id == DiJetQuantitiesProducer().GetProducerId())
		return new DiJetQuantitiesProducer();
	else if(id == SvfitProducer().GetProducerId())
		return new SvfitProducer();
	else if(id == MetprojectionProducer().GetProducerId())
		return new MetprojectionProducer();
	else if(id == TauTauRestFrameSelector().GetProducerId())
		return new TauTauRestFrameSelector();
	else if(id == GenTauCPProducer().GetProducerId())
		return new GenTauCPProducer();
	else if(id == GenMatchedTauCPProducer().GetProducerId())
		return new GenMatchedTauCPProducer();
	else if(id == RecoTauCPProducer().GetProducerId())
		return new RecoTauCPProducer();
	else if(id == AntiTtbarDiscriminatorTmvaReader().GetProducerId())
		return new AntiTtbarDiscriminatorTmvaReader();
	else if(id == HttValidGenTausProducer().GetProducerId())
		return new HttValidGenTausProducer();
	else if(id == HttTriggerSettingsProducer().GetProducerId())
		return new HttTriggerSettingsProducer();
	else if(id == DiVetoElectronVetoProducer().GetProducerId())
		return new DiVetoElectronVetoProducer();
	else if(id == DiVetoMuonVetoProducer().GetProducerId())
		return new DiVetoMuonVetoProducer();
	else if(id == ValidTTPairCandidatesProducer().GetProducerId())
		return new ValidTTPairCandidatesProducer();
	else if(id == ValidMTPairCandidatesProducer().GetProducerId())
		return new ValidMTPairCandidatesProducer();
	else if(id == ValidETPairCandidatesProducer().GetProducerId())
		return new ValidETPairCandidatesProducer();
	else if(id == ValidEMPairCandidatesProducer().GetProducerId())
		return new ValidEMPairCandidatesProducer();
	else if(id == ValidMMPairCandidatesProducer().GetProducerId())
		return new ValidMMPairCandidatesProducer();
	else if(id == ValidEEPairCandidatesProducer().GetProducerId())
		return new ValidEEPairCandidatesProducer();
	else if(id == GenTTPairCandidatesProducer().GetProducerId())
		return new GenTTPairCandidatesProducer();
	else if(id == GenMTPairCandidatesProducer().GetProducerId())
		return new GenMTPairCandidatesProducer();
	else if(id == GenETPairCandidatesProducer().GetProducerId())
		return new GenETPairCandidatesProducer();
	else if(id == GenEMPairCandidatesProducer().GetProducerId())
		return new GenEMPairCandidatesProducer();
	else if(id == GenMMPairCandidatesProducer().GetProducerId())
		return new GenMMPairCandidatesProducer();
	else if(id == GenEEPairCandidatesProducer().GetProducerId())
		return new GenEEPairCandidatesProducer();
	else if(id == GenDiTauPairAcceptanceProducer().GetProducerId())
		return new GenDiTauPairAcceptanceProducer();
	else if(id == EETriggerTagAndProbeProducer().GetProducerId())
		return new EETriggerTagAndProbeProducer();
	else if(id == MMTriggerTagAndProbeProducer().GetProducerId())
		return new MMTriggerTagAndProbeProducer();
	else if(id == MTTriggerTagAndProbeProducer().GetProducerId())
		return new MTTriggerTagAndProbeProducer();
	else if(id == ETTriggerTagAndProbeProducer().GetProducerId())
		return new ETTriggerTagAndProbeProducer();
	else if(id == MVATestMethodsProducer().GetProducerId())
		return new MVATestMethodsProducer();
	else if(id == HHKinFitProducer().GetProducerId())
		return new HHKinFitProducer();
	else if(id == MVAInputQuantitiesProducer().GetProducerId())
		return new MVAInputQuantitiesProducer();
	else if(id == AcceptanceEfficiencyProducer().GetProducerId())
		return new AcceptanceEfficiencyProducer();
	else if(id == TopPtReweightingProducer().GetProducerId())
		return new TopPtReweightingProducer();
	else if(id == ZPtReweightProducer().GetProducerId())
		return new ZPtReweightProducer();
	else if(id == SimpleEleTauFakeRateWeightProducer().GetProducerId())
		return new SimpleEleTauFakeRateWeightProducer();
	else if(id == JetToTauFakesProducer().GetProducerId())
		return new JetToTauFakesProducer();
	else if(id == PolarisationQuantitiesProducer().GetProducerId())
		return new PolarisationQuantitiesProducer();
	else if(id == SimpleFitProducer().GetProducerId())
		return new SimpleFitProducer();
	else if(id == ScaleVariationProducer().GetProducerId())
		return new ScaleVariationProducer();
    else if(id == EmuQcdWeightProducer().GetProducerId())
        return new EmuQcdWeightProducer();
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
	else if(id == MinimalPlotlevelFilter().GetFilterId())
		return new MinimalPlotlevelFilter();
	else if(id == EventCategoryFilter().GetFilterId())
		return new EventCategoryFilter();
	else if(id == ZBosonVetoFilter().GetFilterId())
		return new ZBosonVetoFilter();
	else if(id == MetLowerPtCutsFilter().GetFilterId())
		return new MetLowerPtCutsFilter();
	else if(id == MetUpperPtCutsFilter().GetFilterId())
		return new MetUpperPtCutsFilter();
	else if(id == ValidDiTauPairCandidatesFilter().GetFilterId())
		return new ValidDiTauPairCandidatesFilter();
	else if(id == GenDiTauPairCandidatesFilter().GetFilterId())
		return new GenDiTauPairCandidatesFilter();
	else if(id == GenDiTauPairAcceptanceFilter().GetFilterId())
		return new GenDiTauPairAcceptanceFilter();
	else
		return KappaFactory::createFilter( id );
}

ConsumerBaseUntemplated * HttFactory::createConsumer (std::string const& id)
{
	if(id == HttLambdaNtupleConsumer().GetConsumerId())
		return new HttLambdaNtupleConsumer();
	else if(id == SvfitCacheConsumer().GetConsumerId())
		return new SvfitCacheConsumer();
	else if(id == EETriggerTagAndProbeConsumer().GetConsumerId())
		return new EETriggerTagAndProbeConsumer();
	else if(id == MMTriggerTagAndProbeConsumer().GetConsumerId())
		return new MMTriggerTagAndProbeConsumer();
	else if(id == MTTriggerTagAndProbeConsumer().GetConsumerId())
		return new MTTriggerTagAndProbeConsumer();
	else if(id == ETTriggerTagAndProbeConsumer().GetConsumerId())
		return new ETTriggerTagAndProbeConsumer();
	else if(id == EventCountConsumer().GetConsumerId())
		return new EventCountConsumer();
	else if(id == EmbeddingConsumer().GetConsumerId())
		return new EmbeddingConsumer();
	else if(id == BTagEffConsumer().GetConsumerId())
		return new BTagEffConsumer();
	else if (id == AcceptanceEfficiencyConsumer().GetConsumerId())
		return new AcceptanceEfficiencyConsumer();
	else
		return KappaFactory::createConsumer( id );
}

