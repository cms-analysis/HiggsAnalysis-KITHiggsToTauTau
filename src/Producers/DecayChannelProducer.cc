
#include "Artus/Consumer/interface/LambdaNtupleConsumer.h"
#include "Artus/Utility/interface/DefaultValues.h"
#include "Artus/Utility/interface/Utility.h"
#include "Artus/KappaAnalysis/interface/KappaTypes.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttEnumTypes.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/DecayChannelProducer.h"


void DecayChannelProducer::Init(setting_type const& settings)
{
	ProducerBase<HttTypes>::Init(settings);
	
	// add possible quantities for the lambda ntuples consumers
	LambdaNtupleConsumer<KappaTypes>::AddQuantity("decayChannelIndex", [](KappaEvent const& event, KappaProduct const& product) {
		return Utility::ToUnderlyingValue((static_cast<HttProduct const&>(product)).m_decayChannel);
	});
	
	LambdaNtupleConsumer<KappaTypes>::AddQuantity("leadingLepCharge", [](KappaEvent const& event, KappaProduct const& product)
	{
		return (static_cast<HttProduct const&>(product)).m_ptOrderedLeptons[0]->charge;
	});
	LambdaNtupleConsumer<KappaTypes>::AddQuantity("leadingLepPt", [](KappaEvent const& event, KappaProduct const& product)
	{
		return (static_cast<HttProduct const&>(product)).m_ptOrderedLeptons[0]->p4.Pt();
	});
	LambdaNtupleConsumer<KappaTypes>::AddQuantity("leadingLepEta", [](KappaEvent const& event, KappaProduct const& product)
	{
		return (static_cast<HttProduct const&>(product)).m_ptOrderedLeptons[0]->p4.Eta();
	});
	LambdaNtupleConsumer<KappaTypes>::AddQuantity("leadingLepPhi", [](KappaEvent const& event, KappaProduct const& product)
	{
		return (static_cast<HttProduct const&>(product)).m_ptOrderedLeptons[0]->p4.Phi();
	});
	LambdaNtupleConsumer<KappaTypes>::AddQuantity("leadingLepMass", [](KappaEvent const& event, KappaProduct const& product)
	{
		return (static_cast<HttProduct const&>(product)).m_ptOrderedLeptons[0]->p4.mass();
	});
	LambdaNtupleConsumer<KappaTypes>::AddQuantity("leadingLepMt", [](KappaEvent const& event, KappaProduct const& product)
	{
		return (static_cast<HttProduct const&>(product)).m_ptOrderedLeptons[0]->p4.Mt();
	});
	LambdaNtupleConsumer<KappaTypes>::AddQuantity("leadingLepIso", [](KappaEvent const& event, KappaProduct const& product) {
		return SafeMap::GetWithDefault((static_cast<HttProduct const&>(product)).m_leptonIsolation, (static_cast<HttProduct const&>(product)).m_ptOrderedLeptons[0], DefaultValues::UndefinedDouble);
	});
	LambdaNtupleConsumer<KappaTypes>::AddQuantity("leadingLepIsoOverPt", [](KappaEvent const& event, KappaProduct const& product) {
		return SafeMap::GetWithDefault((static_cast<HttProduct const&>(product)).m_leptonIsolationOverPt, (static_cast<HttProduct const&>(product)).m_ptOrderedLeptons[0], DefaultValues::UndefinedDouble);
	});
	
	LambdaNtupleConsumer<KappaTypes>::AddQuantity("lep1Charge", [](KappaEvent const& event, KappaProduct const& product)
	{
		return (static_cast<HttProduct const&>(product)).m_flavourOrderedLeptons[0]->charge;
	});
	LambdaNtupleConsumer<KappaTypes>::AddQuantity("lep1Pt", [](KappaEvent const& event, KappaProduct const& product)
	{
		return (static_cast<HttProduct const&>(product)).m_flavourOrderedLeptons[0]->p4.Pt();
	});
	LambdaNtupleConsumer<KappaTypes>::AddQuantity("lep1Eta", [](KappaEvent const& event, KappaProduct const& product)
	{
		return (static_cast<HttProduct const&>(product)).m_flavourOrderedLeptons[0]->p4.Eta();
	});
	LambdaNtupleConsumer<KappaTypes>::AddQuantity("lep1Phi", [](KappaEvent const& event, KappaProduct const& product)
	{
		return (static_cast<HttProduct const&>(product)).m_flavourOrderedLeptons[0]->p4.Phi();
	});
	LambdaNtupleConsumer<KappaTypes>::AddQuantity("lep1Mass", [](KappaEvent const& event, KappaProduct const& product)
	{
		return (static_cast<HttProduct const&>(product)).m_flavourOrderedLeptons[0]->p4.mass();
	});
	LambdaNtupleConsumer<KappaTypes>::AddQuantity("lep1Mt", [](KappaEvent const& event, KappaProduct const& product)
	{
		return (static_cast<HttProduct const&>(product)).m_flavourOrderedLeptons[0]->p4.Mt();
	});
	LambdaNtupleConsumer<KappaTypes>::AddQuantity("lep1Iso", [](KappaEvent const& event, KappaProduct const& product) {
		return SafeMap::GetWithDefault((static_cast<HttProduct const&>(product)).m_leptonIsolation, (static_cast<HttProduct const&>(product)).m_flavourOrderedLeptons[0], DefaultValues::UndefinedDouble);
	});
	LambdaNtupleConsumer<KappaTypes>::AddQuantity("lep1IsoOverPt", [](KappaEvent const& event, KappaProduct const& product) {
		return SafeMap::GetWithDefault((static_cast<HttProduct const&>(product)).m_leptonIsolationOverPt, (static_cast<HttProduct const&>(product)).m_flavourOrderedLeptons[0], DefaultValues::UndefinedDouble);
	});
	
	LambdaNtupleConsumer<KappaTypes>::AddQuantity("trailingLepCharge", [](KappaEvent const& event, KappaProduct const& product)
	{
		return (static_cast<HttProduct const&>(product)).m_ptOrderedLeptons[1]->charge;
	});
	LambdaNtupleConsumer<KappaTypes>::AddQuantity("trailingLepPt", [](KappaEvent const& event, KappaProduct const& product)
	{
		return (static_cast<HttProduct const&>(product)).m_ptOrderedLeptons[1]->p4.Pt();
	});
	LambdaNtupleConsumer<KappaTypes>::AddQuantity("trailingLepEta", [](KappaEvent const& event, KappaProduct const& product)
	{
		return (static_cast<HttProduct const&>(product)).m_ptOrderedLeptons[1]->p4.Eta();
	});
	LambdaNtupleConsumer<KappaTypes>::AddQuantity("trailingLepPhi", [](KappaEvent const& event, KappaProduct const& product)
	{
		return (static_cast<HttProduct const&>(product)).m_ptOrderedLeptons[1]->p4.Phi();
	});
	LambdaNtupleConsumer<KappaTypes>::AddQuantity("trailingLepMass", [](KappaEvent const& event, KappaProduct const& product)
	{
		return (static_cast<HttProduct const&>(product)).m_ptOrderedLeptons[1]->p4.mass();
	});
	LambdaNtupleConsumer<KappaTypes>::AddQuantity("trailingLepMt", [](KappaEvent const& event, KappaProduct const& product)
	{
		return (static_cast<HttProduct const&>(product)).m_ptOrderedLeptons[1]->p4.Mt();
	});
	LambdaNtupleConsumer<KappaTypes>::AddQuantity("trailingLepIso", [](KappaEvent const& event, KappaProduct const& product) {
		return SafeMap::GetWithDefault((static_cast<HttProduct const&>(product)).m_leptonIsolation, (static_cast<HttProduct const&>(product)).m_ptOrderedLeptons[1], DefaultValues::UndefinedDouble);
	});
	LambdaNtupleConsumer<KappaTypes>::AddQuantity("trailingLepIsoOverPt", [](KappaEvent const& event, KappaProduct const& product) {
		return SafeMap::GetWithDefault((static_cast<HttProduct const&>(product)).m_leptonIsolationOverPt, (static_cast<HttProduct const&>(product)).m_ptOrderedLeptons[1], DefaultValues::UndefinedDouble);
	});
	
	LambdaNtupleConsumer<KappaTypes>::AddQuantity("lep2Charge", [](KappaEvent const& event, KappaProduct const& product)
	{
		return (static_cast<HttProduct const&>(product)).m_flavourOrderedLeptons[1]->charge;
	});
	LambdaNtupleConsumer<KappaTypes>::AddQuantity("lep2Pt", [](KappaEvent const& event, KappaProduct const& product)
	{
		return (static_cast<HttProduct const&>(product)).m_flavourOrderedLeptons[1]->p4.Pt();
	});
	LambdaNtupleConsumer<KappaTypes>::AddQuantity("lep2Eta", [](KappaEvent const& event, KappaProduct const& product)
	{
		return (static_cast<HttProduct const&>(product)).m_flavourOrderedLeptons[1]->p4.Eta();
	});
	LambdaNtupleConsumer<KappaTypes>::AddQuantity("lep2Phi", [](KappaEvent const& event, KappaProduct const& product)
	{
		return (static_cast<HttProduct const&>(product)).m_flavourOrderedLeptons[1]->p4.Phi();
	});
	LambdaNtupleConsumer<KappaTypes>::AddQuantity("lep2Mass", [](KappaEvent const& event, KappaProduct const& product)
	{
		return (static_cast<HttProduct const&>(product)).m_flavourOrderedLeptons[1]->p4.mass();
	});
	LambdaNtupleConsumer<KappaTypes>::AddQuantity("lep2Mt", [](KappaEvent const& event, KappaProduct const& product)
	{
		return (static_cast<HttProduct const&>(product)).m_flavourOrderedLeptons[1]->p4.Mt();
	});
	LambdaNtupleConsumer<KappaTypes>::AddQuantity("lep2Iso", [](KappaEvent const& event, KappaProduct const& product) {
		return SafeMap::GetWithDefault((static_cast<HttProduct const&>(product)).m_leptonIsolation, (static_cast<HttProduct const&>(product)).m_flavourOrderedLeptons[1], DefaultValues::UndefinedDouble);
	});
	LambdaNtupleConsumer<KappaTypes>::AddQuantity("lep2IsoOverPt", [](KappaEvent const& event, KappaProduct const& product) {
		return SafeMap::GetWithDefault((static_cast<HttProduct const&>(product)).m_leptonIsolationOverPt, (static_cast<HttProduct const&>(product)).m_flavourOrderedLeptons[1], DefaultValues::UndefinedDouble);
	});
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

			// require that in the EM channel at least one of the leptons has a pT > 20 GeV
			if (lepton1->p4.Pt() > 20. || lepton2->p4.Pt() > 20.) {
				product.m_decayChannel = HttEnumTypes::DecayChannel::EM;
			}
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
