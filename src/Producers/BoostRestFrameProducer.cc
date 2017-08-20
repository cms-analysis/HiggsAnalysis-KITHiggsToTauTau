
#include "Artus/Consumer/interface/LambdaNtupleConsumer.h"
#include "Artus/Utility/interface/DefaultValues.h"
#include "Artus/Utility/interface/SafeMap.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/BoostRestFrameProducer.h"


std::string BoostRestFrameProducer::GetProducerId() const
{
	return "BoostRestFrameProducer";
}

void BoostRestFrameProducer::Init(setting_type const& settings, metadata_type& metadata)
{
	ProducerBase<HttTypes>::Init(settings, metadata);
	
	for (size_t leptonIndex = 0; leptonIndex < 2; ++leptonIndex)
	{
		std::string leptonIndexString = std::to_string(leptonIndex+1);
		
		LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity("lep"+leptonIndexString+"LVBoostToDiLeptonSystem", [leptonIndex](event_type const& event, product_type const& product)
		{
			return SafeMap::GetWithDefault(product.m_leptonsBoostToDiLeptonSystem, product.m_flavourOrderedLeptons.at(leptonIndex), DefaultValues::UndefinedRMFLV);
		});
		LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity("lep"+leptonIndexString+"LVBoostToDiTauSystem", [leptonIndex](event_type const& event, product_type const& product)
		{
			return SafeMap::GetWithDefault(product.m_leptonsBoostToDiTauSystem, product.m_flavourOrderedLeptons.at(leptonIndex), DefaultValues::UndefinedRMFLV);
		});
		LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity("tau"+leptonIndexString+"LVBoostToDiTauSystem", [leptonIndex](event_type const& event, product_type const& product)
		{
			KLepton* lepton = product.m_flavourOrderedLeptons.at(leptonIndex);
			RMFLV* tau = (Utility::Contains(product.m_hhKinFitTaus, lepton) ? const_cast<RMFLV*>(&SafeMap::Get(product.m_hhKinFitTaus, lepton)) : nullptr);
			return (tau ? SafeMap::GetWithDefault(product.m_tausBoostToDiTauSystem, tau, DefaultValues::UndefinedRMFLV) : DefaultValues::UndefinedRMFLV);
		});
		
		LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity("genMatchedTau"+leptonIndexString+"VisibleLVBoostToGenDiLeptonSystem", [leptonIndex](event_type const& event, product_type const& product)
		{
			KGenTau* genTau = SafeMap::GetWithDefault(product.m_genTauMatchedLeptons, product.m_flavourOrderedLeptons.at(leptonIndex), static_cast<KGenTau*>(nullptr));
			return (genTau ? SafeMap::GetWithDefault(product.m_genVisTausBoostToGenDiLeptonSystem, genTau, DefaultValues::UndefinedRMFLV) : DefaultValues::UndefinedRMFLV);
		});
		LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity("genMatchedTau"+leptonIndexString+"LVBoostToGenDiLeptonSystem", [leptonIndex](event_type const& event, product_type const& product)
		{
			KGenTau* genTau = SafeMap::GetWithDefault(product.m_genTauMatchedLeptons, product.m_flavourOrderedLeptons.at(leptonIndex), static_cast<KGenTau*>(nullptr));
			return (genTau ? SafeMap::GetWithDefault(product.m_genTausBoostToGenDiLeptonSystem, genTau, DefaultValues::UndefinedRMFLV) : DefaultValues::UndefinedRMFLV);
		});
		LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity("genMatchedTau"+leptonIndexString+"LVBoostToGenDiTauSystem", [leptonIndex](event_type const& event, product_type const& product)
		{
			KGenTau* genTau = SafeMap::GetWithDefault(product.m_genTauMatchedLeptons, product.m_flavourOrderedLeptons.at(leptonIndex), static_cast<KGenTau*>(nullptr));
			return (genTau ? SafeMap::GetWithDefault(product.m_genTausBoostToGenDiTauSystem, genTau, DefaultValues::UndefinedRMFLV) : DefaultValues::UndefinedRMFLV);
		});
	}
}

void BoostRestFrameProducer::Produce(event_type const& event, product_type& product,
                                     setting_type const& settings, metadata_type const& metadata) const
{
	// built systems of multiple particles
	RMFLV leptonSystem;
	RMFLV tauSystem;
	RMFLV genLeptonSystem;
	RMFLV genTauSystem;
	
	for (std::vector<KLepton*>::iterator lepton = product.m_flavourOrderedLeptons.begin();
	     lepton != product.m_flavourOrderedLeptons.end(); ++lepton)
	{
		leptonSystem += (*lepton)->p4;
		
		if (Utility::Contains(product.m_hhKinFitTaus, *lepton))
		{
			tauSystem += SafeMap::Get(product.m_hhKinFitTaus, *lepton);
		}
		
		KGenTau* genTau = SafeMap::GetWithDefault(product.m_genTauMatchedLeptons, *lepton, static_cast<KGenTau*>(nullptr));
		if (genTau)
		{
			genLeptonSystem += genTau->visible.p4;
			genTauSystem += genTau->p4;
		}
	}
	
	// get boosts into these systems
	ROOT::Math::Boost leptonSystemBoost(leptonSystem.BoostToCM());
	ROOT::Math::Boost tauSystemBoost(tauSystem.BoostToCM());
	ROOT::Math::Boost genLeptonSystemBoost(genLeptonSystem.BoostToCM());
	ROOT::Math::Boost genTauSystemBoost(genTauSystem.BoostToCM());
	
	// boost particles to rest frames of these systems
	for (std::vector<KLepton*>::iterator lepton = product.m_flavourOrderedLeptons.begin();
	     lepton != product.m_flavourOrderedLeptons.end(); ++lepton)
	{
		product.m_leptonsBoostToDiLeptonSystem[*lepton] = leptonSystemBoost * (*lepton)->p4;
		product.m_leptonsBoostToDiTauSystem[*lepton] = tauSystemBoost * (*lepton)->p4;
		
		if (Utility::Contains(product.m_hhKinFitTaus, *lepton))
		{
			RMFLV* tau = &SafeMap::Get(product.m_hhKinFitTaus, *lepton);
			product.m_tausBoostToDiTauSystem[tau] = tauSystemBoost * (*tau);
		}
		
		KGenTau* genTau = SafeMap::GetWithDefault(product.m_genTauMatchedLeptons, *lepton, static_cast<KGenTau*>(nullptr));
		if (genTau)
		{
			product.m_genVisTausBoostToGenDiLeptonSystem[genTau] = genLeptonSystemBoost * genTau->visible.p4;
			product.m_genTausBoostToGenDiLeptonSystem[genTau] = genTauSystemBoost * genTau->visible.p4;
			product.m_genTausBoostToGenDiTauSystem[genTau] = genTauSystemBoost * genTau->p4;
		}
	}
}
