
#include "Artus/Consumer/interface/LambdaNtupleConsumer.h"
#include "Artus/Utility/interface/DefaultValues.h"
#include "Artus/Utility/interface/Utility.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttEnumTypes.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/DecayChannelProducer.h"


void DecayChannelProducer::Init(setting_type const& settings)
{
	ProducerBase<HttTypes>::Init(settings);
	
	// add possible quantities for the lambda ntuples consumers
	LambdaNtupleConsumer<HttTypes>::Quantities["decayChannelIndex"] = [](event_type const& event, product_type const& product) {
		return Utility::ToUnderlyingValue(product.m_decayChannel);
	};
	
	LambdaNtupleConsumer<HttTypes>::Quantities["leadingLepCharge"] = [](event_type const& event, product_type const& product)
	{
		return product.m_ptOrderedLeptons[0]->charge;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["leadingLepPt"] = [](event_type const& event, product_type const& product)
	{
		return product.m_ptOrderedLeptons[0]->p4.Pt();
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["leadingLepEta"] = [](event_type const& event, product_type const& product)
	{
		return product.m_ptOrderedLeptons[0]->p4.Eta();
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["leadingLepPhi"] = [](event_type const& event, product_type const& product)
	{
		return product.m_ptOrderedLeptons[0]->p4.Phi();
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["leadingLepMass"] = [](event_type const& event, product_type const& product)
	{
		return product.m_ptOrderedLeptons[0]->p4.mass();
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["leadingLepMt"] = [](event_type const& event, product_type const& product)
	{
		return product.m_ptOrderedLeptons[0]->p4.Mt();
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["leadingLepIso"] = [](event_type const& event, product_type const& product) {
		return SafeMap::GetWithDefault(product.m_leptonIsolation, product.m_ptOrderedLeptons[0], DefaultValues::UndefinedDouble);
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["leadingLepIsoOverPt"] = [](event_type const& event, product_type const& product) {
		return SafeMap::GetWithDefault(product.m_leptonIsolationOverPt, product.m_ptOrderedLeptons[0], DefaultValues::UndefinedDouble);
	};
	
	LambdaNtupleConsumer<HttTypes>::Quantities["lep1Charge"] = [](event_type const& event, product_type const& product)
	{
		return product.m_flavourOrderedLeptons[0]->charge;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["lep1Pt"] = [](event_type const& event, product_type const& product)
	{
		return product.m_flavourOrderedLeptons[0]->p4.Pt();
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["lep1Eta"] = [](event_type const& event, product_type const& product)
	{
		return product.m_flavourOrderedLeptons[0]->p4.Eta();
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["lep1Phi"] = [](event_type const& event, product_type const& product)
	{
		return product.m_flavourOrderedLeptons[0]->p4.Phi();
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["lep1Mass"] = [](event_type const& event, product_type const& product)
	{
		return product.m_flavourOrderedLeptons[0]->p4.mass();
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["lep1Mt"] = [](event_type const& event, product_type const& product)
	{
		return product.m_flavourOrderedLeptons[0]->p4.Mt();
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["lep1Iso"] = [](event_type const& event, product_type const& product) {
		return SafeMap::GetWithDefault(product.m_leptonIsolation, product.m_flavourOrderedLeptons[0], DefaultValues::UndefinedDouble);
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["lep1IsoOverPt"] = [](event_type const& event, product_type const& product) {
		return SafeMap::GetWithDefault(product.m_leptonIsolationOverPt, product.m_flavourOrderedLeptons[0], DefaultValues::UndefinedDouble);
	};
	
	LambdaNtupleConsumer<HttTypes>::Quantities["trailingLepCharge"] = [](event_type const& event, product_type const& product)
	{
		return product.m_ptOrderedLeptons[1]->charge;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["trailingLepPt"] = [](event_type const& event, product_type const& product)
	{
		return product.m_ptOrderedLeptons[1]->p4.Pt();
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["trailingLepEta"] = [](event_type const& event, product_type const& product)
	{
		return product.m_ptOrderedLeptons[1]->p4.Eta();
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["trailingLepPhi"] = [](event_type const& event, product_type const& product)
	{
		return product.m_ptOrderedLeptons[1]->p4.Phi();
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["trailingLepMass"] = [](event_type const& event, product_type const& product)
	{
		return product.m_ptOrderedLeptons[1]->p4.mass();
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["trailingLepMt"] = [](event_type const& event, product_type const& product)
	{
		return product.m_ptOrderedLeptons[1]->p4.Mt();
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["trailingLepIso"] = [](event_type const& event, product_type const& product) {
		return SafeMap::GetWithDefault(product.m_leptonIsolation, product.m_ptOrderedLeptons[1], DefaultValues::UndefinedDouble);
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["trailingLepIsoOverPt"] = [](event_type const& event, product_type const& product) {
		return SafeMap::GetWithDefault(product.m_leptonIsolationOverPt, product.m_ptOrderedLeptons[1], DefaultValues::UndefinedDouble);
	};
	
	LambdaNtupleConsumer<HttTypes>::Quantities["lep2Charge"] = [](event_type const& event, product_type const& product)
	{
		return product.m_flavourOrderedLeptons[1]->charge;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["lep2Pt"] = [](event_type const& event, product_type const& product)
	{
		return product.m_flavourOrderedLeptons[1]->p4.Pt();
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["lep2Eta"] = [](event_type const& event, product_type const& product)
	{
		return product.m_flavourOrderedLeptons[1]->p4.Eta();
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["lep2Phi"] = [](event_type const& event, product_type const& product)
	{
		return product.m_flavourOrderedLeptons[1]->p4.Phi();
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["lep2Mass"] = [](event_type const& event, product_type const& product)
	{
		return product.m_flavourOrderedLeptons[1]->p4.mass();
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["lep2Mt"] = [](event_type const& event, product_type const& product)
	{
		return product.m_flavourOrderedLeptons[1]->p4.Mt();
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["lep2Iso"] = [](event_type const& event, product_type const& product) {
		return SafeMap::GetWithDefault(product.m_leptonIsolation, product.m_flavourOrderedLeptons[1], DefaultValues::UndefinedDouble);
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["lep2IsoOverPt"] = [](event_type const& event, product_type const& product) {
		return SafeMap::GetWithDefault(product.m_leptonIsolationOverPt, product.m_flavourOrderedLeptons[1], DefaultValues::UndefinedDouble);
	};
}

void DecayChannelProducer::Produce(event_type const& event, product_type& product,
	                               setting_type const& settings) const
{
	
	product.m_decayChannel = HttEnumTypes::DecayChannel::NONE;
	
	KLepton* lepton1 = 0;
	KLepton* lepton2 = 0;
	
	size_t nElectrons = product.m_validElectrons.size();
	size_t nMuons = product.m_validMuons.size();
	size_t nTaus = product.m_validTaus.size();
	
	if (nElectrons == 2)
	{
		lepton1 = product.m_validElectrons[0];
		lepton2 = product.m_validElectrons[1];
		product.m_decayChannel = HttEnumTypes::DecayChannel::EE;
	}
	else if (nElectrons == 1)
	{
		if (nMuons == 1)
		{
			lepton1 = product.m_validElectrons[0];
			lepton2 = product.m_validMuons[0];
			product.m_decayChannel = HttEnumTypes::DecayChannel::EM;
		}
		else if (nTaus >= 1)
		{
			lepton1 = product.m_validElectrons[0];
			lepton2 = product.m_validTaus[0];
			product.m_decayChannel = HttEnumTypes::DecayChannel::ET;
		}
	}
	else if (nElectrons == 0)
	{
		if (nMuons == 2)
		{
			lepton1 = product.m_validMuons[0];
			lepton2 = product.m_validMuons[1];
			product.m_decayChannel = HttEnumTypes::DecayChannel::MM;
		}
		else if (nMuons == 1 && nTaus >= 1)
		{
			lepton1 = product.m_validMuons[0];
			lepton2 = product.m_validTaus[0];
			product.m_decayChannel = HttEnumTypes::DecayChannel::MT;
		}
		else if (nTaus >= 2)
		{
			lepton1 = product.m_validTaus[0];
			lepton2 = product.m_validTaus[1];
			product.m_decayChannel = HttEnumTypes::DecayChannel::TT;
		}
	}
	
	// fill tau energy scale weights
	if (! product.m_tauEnergyScaleWeight.empty())
	{
		if ((product.m_decayChannel == HttEnumTypes::DecayChannel::ET) ||
			(product.m_decayChannel == HttEnumTypes::DecayChannel::MT) ||
			(product.m_decayChannel == HttEnumTypes::DecayChannel::TT))
		{
			product.m_weights["tauEnergyScaleWeight"] = SafeMap::Get(product.m_tauEnergyScaleWeight, static_cast<KDataPFTau*>(lepton2));
			if (product.m_decayChannel == HttEnumTypes::DecayChannel::TT)
			{
				product.m_weights["tauEnergyScaleWeight"] *= SafeMap::Get(product.m_tauEnergyScaleWeight, static_cast<KDataPFTau*>(lepton1));
			}
		}
	}

	if (product.m_decayChannel != HttEnumTypes::DecayChannel::NONE)
	{
		
		// fill leptons ordered by pt (high pt first)
		if (lepton1->p4.Pt() >= lepton2->p4.Pt())
		{
			product.m_ptOrderedLeptons.push_back(lepton1);
			product.m_ptOrderedLeptons.push_back(lepton2);
		}
		else
		{
			product.m_ptOrderedLeptons.push_back(lepton2);
			product.m_ptOrderedLeptons.push_back(lepton1);
		}
		
		// fill leptons ordered by flavour (according to channel definition)
		product.m_flavourOrderedLeptons.push_back(lepton1);
		product.m_flavourOrderedLeptons.push_back(lepton2);
		
		// fill leptons ordered by charge (positive charges first)
		if (lepton1->charge >= lepton2->charge)
		{
			product.m_chargeOrderedLeptons.push_back(lepton1);
			product.m_chargeOrderedLeptons.push_back(lepton2);
		}
		else
		{
			product.m_chargeOrderedLeptons.push_back(lepton2);
			product.m_chargeOrderedLeptons.push_back(lepton1);
		}
	}
}
