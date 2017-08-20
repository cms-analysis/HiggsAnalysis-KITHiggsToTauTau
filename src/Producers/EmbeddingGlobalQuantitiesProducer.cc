#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/EmbeddingGlobalQuantitiesProducer.h"

void EmbeddingGlobalQuantitiesProducer::Init(setting_type const& settings, metadata_type& metadata)
{
	ProducerBase<HttTypes>::Init(settings, metadata);
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("PFSumHt", [](event_type const& event, product_type const& product)
	{
		return product.m_pfSumHt;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("PFSumPt", [](event_type const& event, product_type const& product)
	{
		return product.m_pfSumP4.Pt();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("PFSumHtWithoutZMuMu", [](event_type const& event, product_type const& product)
	{
		return product.m_pfSumHtWithoutZMuMu;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("PFSumPtWithoutZMuMu", [](event_type const& event, product_type const& product)
	{
		return product.m_pfSumP4WithoutZMuMu.Pt();
	});
}

void EmbeddingGlobalQuantitiesProducer::Produce(event_type const& event, product_type& product, setting_type const& settings, metadata_type const& metadata) const
{
	product.m_pfSumP4.SetPxPyPzE(0.,0.,0.,0.);
	product.m_pfSumP4WithoutZMuMu.SetPxPyPzE(0.,0.,0.,0.);
	for (KPFCandidates::const_iterator pfCandidate = event.m_packedPFCandidates->begin();
		pfCandidate != event.m_packedPFCandidates->end(); ++pfCandidate)
	{
		product.m_pfSumHt += pfCandidate->p4.Pt();
		product.m_pfSumP4 += pfCandidate->p4;
	}
	product.m_pfSumHtWithoutZMuMu = product.m_pfSumHt;
	product.m_pfSumP4WithoutZMuMu = product.m_pfSumP4;
	if(product.m_zValid)
	{
		product.m_pfSumHtWithoutZMuMu -= (product.m_zPFLeptonsMatched.first->p4.Pt() + product.m_zPFLeptonsMatched.second->p4.Pt());
		product.m_pfSumP4WithoutZMuMu -= (product.m_zPFLeptonsMatched.first->p4 + product.m_zPFLeptonsMatched.second->p4);
	}
}

