
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

void DiVetoElectronVetoProducer::Init(setting_type const& settings)
{
	DiLeptonVetoProducerBase<KElectron>::Init(settings);

	LambdaNtupleConsumer<HttTypes>::AddIntQuantity("nDiElectronVetoPairsOS", [](event_type const& event, product_type const& product)
	{
		return product.m_nDiElectronVetoPairsOS;
	});
	LambdaNtupleConsumer<HttTypes>::AddIntQuantity("nDiElectronVetoPairsSS", [](event_type const& event, product_type const& product)
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

void DiVetoMuonVetoProducer::Init(setting_type const& settings)
{
	DiLeptonVetoProducerBase<KMuon>::Init(settings);

	LambdaNtupleConsumer<HttTypes>::AddIntQuantity("nDiMuonVetoPairsOS", [](event_type const& event, product_type const& product)
	{
		return product.m_nDiMuonVetoPairsOS;
	});
	LambdaNtupleConsumer<HttTypes>::AddIntQuantity("nDiMuonVetoPairsSS", [](event_type const& event, product_type const& product)
	{
		return product.m_nDiMuonVetoPairsSS;
	});
}

