
#include "Artus/Consumer/interface/LambdaNtupleConsumer.h"
#include "Artus/KappaAnalysis/interface/KappaTypes.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttEnumTypes.h"
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

	// Defining CPQuantities object to use variables and functions of this class
	CPQuantities cpq;
	if(product.m_decayChannel == HttEnumTypes::DecayChannel::TT)
	{
		KVertex primevertex = event.m_vertexSummary->pv;
		KTau* tau1 = product.m_validTaus[0];
		KTau* tau2 = product.m_validTaus[1];
		if(tau1->chargedHadronCandidates.size()==1 && tau2->chargedHadronCandidates.size()==1)
		{
			KPFCandidate* chargePart1 = &(tau1->chargedHadronCandidates[0]);
			KPFCandidate* chargePart2 = &(tau2->chargedHadronCandidates[0]);
			product.m_recoPhiStarCP = cpq.CalculatePhiStarCP(primevertex, tau1->track, tau2->track, chargePart1->p4, chargePart2->p4);
			product.m_recoPhiStar = cpq.GetRecoPhiStar();
			product.m_recoIP1 = cpq.GetRecoIP1();
			product.m_recoIP2 = cpq.GetRecoIP2();
			product.m_recoChargedHadronEnergies.first = cpq.CalculateChargedHadronEnergy(product.m_diTauSystem, chargePart1->p4);
			product.m_recoChargedHadronEnergies.second = cpq.CalculateChargedHadronEnergy(product.m_diTauSystem, chargePart2->p4);
			product.m_recoTrackRefError1 = cpq.CalculateTrackReferenceError(tau1->track);
			product.m_recoTrackRefError2 = cpq.CalculateTrackReferenceError(tau2->track);
		}
	}

	else if (product.m_decayChannel == HttEnumTypes::DecayChannel::EE)
	{
		KVertex primevertex = event.m_vertexSummary->pv;
		KElectron* electron1 = product.m_validElectrons[0];
		KElectron* electron2 = product.m_validElectrons[1];
		product.m_recoPhiStarCP = cpq.CalculatePhiStarCP(primevertex, electron1->track, electron2->track, electron1->p4, electron2->p4);
		product.m_recoPhiStar = cpq.GetRecoPhiStar();
		product.m_recoIP1 = cpq.GetRecoIP1();
		product.m_recoIP2 = cpq.GetRecoIP2();
		product.m_recoTrackRefError1 = cpq.CalculateTrackReferenceError(electron1->track);
		product.m_recoTrackRefError2 = cpq.CalculateTrackReferenceError(electron2->track);
	}
	else if (product.m_decayChannel == HttEnumTypes::DecayChannel::MM)
	{
		KVertex primevertex = event.m_vertexSummary->pv;
		KMuon* muon1 = product.m_validMuons[0];
		KMuon* muon2 = product.m_validMuons[1];
		product.m_recoPhiStarCP = cpq.CalculatePhiStarCP(primevertex, muon1->track, muon2->track, muon1->p4, muon2->p4);
		product.m_recoPhiStar = cpq.GetRecoPhiStar();
		product.m_recoIP1 = cpq.GetRecoIP1();
		product.m_recoIP2 = cpq.GetRecoIP2();
		product.m_recoTrackRefError1 = cpq.CalculateTrackReferenceError(muon1->track);
		product.m_recoTrackRefError2 = cpq.CalculateTrackReferenceError(muon2->track);
	}
	else if (product.m_decayChannel == HttEnumTypes::DecayChannel::ET)
	{
		KVertex primevertex = event.m_vertexSummary->pv;
		KElectron* electron1 = product.m_validElectrons[0];
		KTau* tau1 = product.m_validTaus[0];
		if (tau1->chargedHadronCandidates.size()==1)
		{
			KPFCandidate* chargePart1 = &(tau1->chargedHadronCandidates[0]);
			product.m_recoPhiStarCP = cpq.CalculatePhiStarCP(primevertex, electron1->track, tau1->track, electron1->p4, chargePart1->p4);
			product.m_recoPhiStar = cpq.GetRecoPhiStar();
			product.m_recoIP1 = cpq.GetRecoIP1();
			product.m_recoIP2 = cpq.GetRecoIP2();
			product.m_recoChargedHadronEnergies.first = cpq.CalculateChargedHadronEnergy(product.m_diTauSystem, chargePart1->p4);
			product.m_recoTrackRefError1 = cpq.CalculateTrackReferenceError(electron1->track);
			product.m_recoTrackRefError2 = cpq.CalculateTrackReferenceError(tau1->track);
		}
	}
	else if (product.m_decayChannel == HttEnumTypes::DecayChannel::MT)
	{
		KVertex primevertex = event.m_vertexSummary->pv;
		KMuon* muon1 = product.m_validMuons[0];
		KTau* tau1 = product.m_validTaus[0];
		if (tau1->chargedHadronCandidates.size()==1)
		{
			KPFCandidate* chargePart1 = &(tau1->chargedHadronCandidates[0]);
			product.m_recoPhiStarCP = cpq.CalculatePhiStarCP(primevertex, muon1->track, tau1->track, muon1->p4, chargePart1->p4);
			product.m_recoPhiStar = cpq.GetRecoPhiStar();
			product.m_recoIP1 = cpq.GetRecoIP1();
			product.m_recoIP2 = cpq.GetRecoIP2();
			product.m_recoChargedHadronEnergies.first = cpq.CalculateChargedHadronEnergy(product.m_diTauSystem, chargePart1->p4);
			product.m_recoTrackRefError1 = cpq.CalculateTrackReferenceError(muon1->track);
			product.m_recoTrackRefError2 = cpq.CalculateTrackReferenceError(tau1->track);
		}
	}
	else if (product.m_decayChannel == HttEnumTypes::DecayChannel::EM)
	{
		KVertex primevertex = event.m_vertexSummary->pv;
		KElectron* electron1 = product.m_validElectrons[0];
		KMuon* muon1 = product.m_validMuons[0];
		product.m_recoPhiStarCP = cpq.CalculatePhiStarCP(primevertex, electron1->track, muon1->track, electron1->p4, muon1->p4);
		product.m_recoPhiStar = cpq.GetRecoPhiStar();
		product.m_recoIP1 = cpq.GetRecoIP1();
		product.m_recoIP2 = cpq.GetRecoIP2();
		product.m_recoTrackRefError1 = cpq.CalculateTrackReferenceError(electron1->track);
		product.m_recoTrackRefError2 = cpq.CalculateTrackReferenceError(muon1->track);
	}
}
