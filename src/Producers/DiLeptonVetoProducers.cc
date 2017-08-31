
#include "Artus/Consumer/interface/LambdaNtupleConsumer.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/DiLeptonVetoProducers.h"


std::string DiVetoElectronVetoProducer::GetProducerId() const
{
	return "DiVetoElectronVetoProducer";
}

DiVetoElectronVetoProducer::DiVetoElectronVetoProducer() :
	DiLeptonVetoProducerBase<KElectron>(&product_type::m_validVetoElectrons,
	                                    &setting_type::GetDiVetoElectronMinDeltaRCut,
	                                    &product_type::m_nDiElectronVetoPairsOS,
	                                    &product_type::m_nDiElectronVetoPairsSS)
{
}

void DiVetoElectronVetoProducer::Init(setting_type const& settings, metadata_type& metadata)
{
	DiLeptonVetoProducerBase<KElectron>::Init(settings, metadata);

	LambdaNtupleConsumer<HttTypes>::AddIntQuantity(metadata, "nDiElectronVetoPairsOS", [](event_type const& event, product_type const& product)
	{
		return product.m_nDiElectronVetoPairsOS;
	});
	LambdaNtupleConsumer<HttTypes>::AddIntQuantity(metadata, "nDiElectronVetoPairsSS", [](event_type const& event, product_type const& product)
	{
		return product.m_nDiElectronVetoPairsSS;
	});
}

std::string DiVetoMuonVetoProducer::GetProducerId() const
{
	return "DiVetoMuonVetoProducer";
}

DiVetoMuonVetoProducer::DiVetoMuonVetoProducer() :
	DiLeptonVetoProducerBase<KMuon>(&product_type::m_validVetoMuons,
	                                &setting_type::GetDiVetoMuonMinDeltaRCut,
	                                &product_type::m_nDiMuonVetoPairsOS,
	                                &product_type::m_nDiMuonVetoPairsSS)
{
}

void DiVetoMuonVetoProducer::Init(setting_type const& settings, metadata_type& metadata)
{
	DiLeptonVetoProducerBase<KMuon>::Init(settings, metadata);

	LambdaNtupleConsumer<HttTypes>::AddIntQuantity(metadata, "nDiMuonVetoPairsOS", [](event_type const& event, product_type const& product)
	{
		return product.m_nDiMuonVetoPairsOS;
	});
	LambdaNtupleConsumer<HttTypes>::AddIntQuantity(metadata, "nDiMuonVetoPairsSS", [](event_type const& event, product_type const& product)
	{
		return product.m_nDiMuonVetoPairsSS;
	});
}

