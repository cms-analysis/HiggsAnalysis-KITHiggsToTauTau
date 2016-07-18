
#include "Artus/Consumer/interface/LambdaNtupleConsumer.h"
#include "Artus/KappaAnalysis/interface/KappaTypes.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttEnumTypes.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Utility/CPQuantities.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/RecoTauCPProducer.h"


void RecoTauCPProducer::Init(setting_type const& settings)
{
	ProducerBase<HttTypes>::Init(settings);
	
	//adding possible quantities for the lambda ntuples consumers
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("recoPhiStarCP", [](event_type const& event, product_type const& product)
	{
		return product.m_recoPhiStarCP;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("recoPhiStar", [](event_type const& event, product_type const& product)
	{
		return product.m_recoPhiStar;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("recoChargedHadron1HiggsFrameEnergy", [](event_type const& event, product_type const& product)
	{
		return product.m_recoChargedHadronEnergies.first;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("recoChargedHadron2HiggsFrameEnergy", [](event_type const& event, product_type const& product)
	{
		return product.m_recoChargedHadronEnergies.second;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("recoImpactParameter1", [](event_type const& event, product_type const& product)
	{
		return product.m_recoIP1;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("recoImpactParameter2", [](event_type const& event, product_type const& product)
	{
		return product.m_recoIP2;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("recoTrackRefError1", [](event_type const& event, product_type const& product)
	{
		return product.m_recoTrackRefError1;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("recoTrackRefError2", [](event_type const& event, product_type const& product)
	{
		return product.m_recoTrackRefError2;
	});
}
void RecoTauCPProducer::Produce(event_type const& event, product_type& product, setting_type const& settings) const
{
	assert(event.m_vertexSummary);
	assert(product.m_flavourOrderedLeptons.size() >= 2);
	
	KTrack& track1 = product.m_flavourOrderedLeptons[0]->track;
	KTrack& track2 = product.m_flavourOrderedLeptons[1]->track;
	RMFLV& momentum1 = product.m_flavourOrderedLeptons[0]->p4;
	RMFLV& momentum2 = product.m_flavourOrderedLeptons[1]->p4;

	if ((product.m_decayChannel == HttEnumTypes::DecayChannel::TT) &&
	    (static_cast<KTau*>(product.m_flavourOrderedLeptons[0])->chargedHadronCandidates.size() > 0))
	{
		momentum1 = static_cast<KTau*>(product.m_flavourOrderedLeptons[0])->chargedHadronCandidates.at(0).p4;
	}
	if (((product.m_decayChannel == HttEnumTypes::DecayChannel::ET) ||
	     (product.m_decayChannel == HttEnumTypes::DecayChannel::MT) ||
	     (product.m_decayChannel == HttEnumTypes::DecayChannel::TT)) &&
	    (static_cast<KTau*>(product.m_flavourOrderedLeptons[1])->chargedHadronCandidates.size() > 0))
	{
		momentum2 = static_cast<KTau*>(product.m_flavourOrderedLeptons[1])->chargedHadronCandidates.at(0).p4;
	}
	

	// define which is the chargePlus particle and which is the chargeMinus particle
	KTrack& trackP = track1;
	KTrack& trackM = track2;
	RMFLV& momentumP = momentum1;
	RMFLV& momentumM = momentum2;

	if (product.m_flavourOrderedLeptons[0]->charge() == -1){   // reminder: track1 = product.m_flavourOrderedLeptons[0]->track
		trackP = track2;
		trackM = track1;
		momentumP = momentum2;
		momentumM = momentum1;
	}

	CPQuantities cpq;
	product.m_recoPhiStarCP = cpq.CalculatePhiStarCP(event.m_vertexSummary->pv, trackP, trackM, momentumP, momentumM);
	product.m_recoPhiStar = cpq.GetRecoPhiStar();
	product.m_recoIP1 = cpq.GetRecoIP1();
	product.m_recoIP2 = cpq.GetRecoIP2();
	product.m_recoChargedHadronEnergies.first = cpq.CalculateChargedHadronEnergy(product.m_diTauSystem, momentum1);
	product.m_recoChargedHadronEnergies.second = cpq.CalculateChargedHadronEnergy(product.m_diTauSystem, momentum2);
	product.m_recoTrackRefError1 = cpq.CalculateTrackReferenceError(track1);
	product.m_recoTrackRefError2 = cpq.CalculateTrackReferenceError(track2);
}
