#include "Artus/Utility/interface/SafeMap.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/CPInitialStateQuantitiesProducer.h"

#include "Artus/Consumer/interface/LambdaNtupleConsumer.h"

CPInitialStateQuantitiesProducer::~CPInitialStateQuantitiesProducer()
{
}

std::string CPInitialStateQuantitiesProducer::GetProducerId() const
{
	return "CPInitialStateQuantitiesProducer";
}

void CPInitialStateQuantitiesProducer::Init(setting_type const& settings, metadata_type& metadata)
{
	ProducerBase<HttTypes>::Init(settings, metadata);

	LambdaNtupleConsumer<HttTypes>::AddIntQuantity(metadata, "lhenpNLO", [](event_type const& event, product_type const& product)
	{
		return product.m_lhenpNLO;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "etaSep", [](event_type const& event, product_type const& product) {
		return product.m_diJetSystemAvailable ? std::min(std::abs(product.m_svfitResults.fittedHiggsLV->Eta() - product.m_validJets[0]->p4.Eta()),std::abs(product.m_svfitResults.fittedHiggsLV->Eta() - product.m_validJets[1]->p4.Eta())) : DefaultValues::UndefinedDouble;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "etaH_cut", [](event_type const& event, product_type const& product) {
		return product.m_diJetSystemAvailable ? (((product.m_validJets[0]->p4.Eta() < product.m_svfitResults.fittedHiggsLV->Eta()) && (product.m_validJets[1]->p4.Eta() > product.m_svfitResults.fittedHiggsLV->Eta())) || ((product.m_validJets[1]->p4.Eta() < product.m_svfitResults.fittedHiggsLV->Eta()) && (product.m_validJets[0]->p4.Eta() > product.m_svfitResults.fittedHiggsLV->Eta()))) : false;
	});
}

void CPInitialStateQuantitiesProducer::Produce(event_type const& event, product_type& product,
                                    setting_type const& settings, metadata_type const& metadata) const
{
	int lhenpNLO = 0;
	if (settings.GetDoLhenpNLO()) //not in all skims yet, but quantities above I want to have in skim
	{
		lhenpNLO = (event.m_genEventInfo)->lhenpNLO;
	}
	product.m_lhenpNLO = lhenpNLO;
}



