/*
#include "HHKinFit2/HHKinFit2/interface/HHKinFitMasterSingleHiggs.h"

#include "Artus/Consumer/interface/LambdaNtupleConsumer.h"
#include "Artus/Utility/interface/DefaultValues.h"
#include "Artus/Utility/interface/Utility.h"
#include "Artus/Utility/interface/SafeMap.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/HHKinFitProducer.h"

std::string HHKinFitProducer::GetProducerId() const
{
	return "HHKinFitProducer";
}

void HHKinFitProducer::Init(setting_type const& settings, metadata_type& metadata)
{
	ProducerBase<HttTypes>::Init(settings, metadata);
	
	// add possible quantities for the lambda ntuples consumers
	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity(metadata, "hhKinFitTau1LV", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
		if ((product.m_flavourOrderedLeptons.size() > 0) && Utility::Contains(product.m_hhKinFitTaus, product.m_flavourOrderedLeptons[0]))
		{
			return SafeMap::Get(product.m_hhKinFitTaus, product.m_flavourOrderedLeptons[0]);
		}
		else
		{
			return DefaultValues::UndefinedRMFLV;
		}
	});
	
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "hhKinFitTau1Pt", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
		if ((product.m_flavourOrderedLeptons.size() > 0) && Utility::Contains(product.m_hhKinFitTaus, product.m_flavourOrderedLeptons[0]))
		{
			return SafeMap::Get(product.m_hhKinFitTaus, product.m_flavourOrderedLeptons[0]).Pt();
		}
		else
		{
			return DefaultValues::UndefinedFloat;
		}
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "hhKinFitTau1Eta", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
		if ((product.m_flavourOrderedLeptons.size() > 0) && Utility::Contains(product.m_hhKinFitTaus, product.m_flavourOrderedLeptons[0]))
		{
			return SafeMap::Get(product.m_hhKinFitTaus, product.m_flavourOrderedLeptons[0]).Eta();
		}
		else
		{
			return DefaultValues::UndefinedFloat;
		}
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "hhKinFitTau1Phi", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
		if ((product.m_flavourOrderedLeptons.size() > 0) && Utility::Contains(product.m_hhKinFitTaus, product.m_flavourOrderedLeptons[0]))
		{
			return SafeMap::Get(product.m_hhKinFitTaus, product.m_flavourOrderedLeptons[0]).Phi();
		}
		else
		{
			return DefaultValues::UndefinedFloat;
		}
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "hhKinFitTau1Mass", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
		if ((product.m_flavourOrderedLeptons.size() > 0) && Utility::Contains(product.m_hhKinFitTaus, product.m_flavourOrderedLeptons[0]))
		{
			return SafeMap::Get(product.m_hhKinFitTaus, product.m_flavourOrderedLeptons[0]).mass();
		}
		else
		{
			return DefaultValues::UndefinedFloat;
		}
	});
		
	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity(metadata, "hhKinFitTau2LV", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
		if ((product.m_flavourOrderedLeptons.size() > 1) && Utility::Contains(product.m_hhKinFitTaus, product.m_flavourOrderedLeptons[1]))
		{
			return SafeMap::Get(product.m_hhKinFitTaus, product.m_flavourOrderedLeptons[1]);
		}
		else
		{
			return DefaultValues::UndefinedRMFLV;
		}
	});
	
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "hhKinFitTau2Pt", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
		if ((product.m_flavourOrderedLeptons.size() > 1) && Utility::Contains(product.m_hhKinFitTaus, product.m_flavourOrderedLeptons[1]))
		{
			return SafeMap::Get(product.m_hhKinFitTaus, product.m_flavourOrderedLeptons[1]).Pt();
		}
		else
		{
			return DefaultValues::UndefinedFloat;
		}
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "hhKinFitTau2Eta", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
		if ((product.m_flavourOrderedLeptons.size() > 1) && Utility::Contains(product.m_hhKinFitTaus, product.m_flavourOrderedLeptons[1]))
		{
			return SafeMap::Get(product.m_hhKinFitTaus, product.m_flavourOrderedLeptons[1]).Eta();
		}
		else
		{
			return DefaultValues::UndefinedFloat;
		}
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "hhKinFitTau2Phi", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
		if ((product.m_flavourOrderedLeptons.size() > 1) && Utility::Contains(product.m_hhKinFitTaus, product.m_flavourOrderedLeptons[1]))
		{
			return SafeMap::Get(product.m_hhKinFitTaus, product.m_flavourOrderedLeptons[1]).Phi();
		}
		else
		{
			return DefaultValues::UndefinedFloat;
		}
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "hhKinFitTau2Mass", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata) {
		if ((product.m_flavourOrderedLeptons.size() > 1) && Utility::Contains(product.m_hhKinFitTaus, product.m_flavourOrderedLeptons[1]))
		{
			return SafeMap::Get(product.m_hhKinFitTaus, product.m_flavourOrderedLeptons[1]).mass();
		}
		else
		{
			return DefaultValues::UndefinedFloat;
		}
	});
}

void HHKinFitProducer::Produce(event_type const& event, product_type& product,
                            setting_type const& settings, metadata_type const& metadata) const
{
	// consider only the first two leptons
	assert(product.m_flavourOrderedLeptons.size() >= 2);
	
	TLorentzVector visibleTau1 = Utility::ConvertPtEtaPhiMLorentzVector<RMFLV, TLorentzVector>(product.m_flavourOrderedLeptons[0]->p4);
	TLorentzVector visibleTau2 = Utility::ConvertPtEtaPhiMLorentzVector<RMFLV, TLorentzVector>(product.m_flavourOrderedLeptons[1]->p4);
	TVector2 met = Utility::ConvertPxPyVector<RMFLV, TVector2>(product.m_met.p4);
	TMatrixD metCov = Utility::ConvertMatrixSym<ROOT::Math::SMatrix<double, 2, 2, ROOT::Math::MatRepSym<double, 2> >>(product.m_met.significance, 2, 4);
	
	HHKinFit2::HHKinFitMasterSingleHiggs hhKinFit(visibleTau1, visibleTau2, met, metCov);
	hhKinFit.addHypo(90); // TODO: make configurable
	
	try
	{
		hhKinFit.fit();
		HHKinFit2::HHFitHypothesisSingleHiggs hhKinFitHypothesis = hhKinFit.getBestHypothesis();
	
		product.m_hhKinFitTaus[product.m_flavourOrderedLeptons[0]] = Utility::ConvertPtEtaPhiMLorentzVector<TLorentzVector>(hhKinFit.getFittedTau1(hhKinFitHypothesis));
		product.m_hhKinFitTaus[product.m_flavourOrderedLeptons[1]] = Utility::ConvertPtEtaPhiMLorentzVector<TLorentzVector>(hhKinFit.getFittedTau2(hhKinFitHypothesis));
	}
	catch (...)
	{
	}
}
*/
