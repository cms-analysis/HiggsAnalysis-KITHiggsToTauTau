
#include <boost/algorithm/string.hpp>
#include <boost/algorithm/string/trim.hpp>

#include "Artus/Consumer/interface/LambdaNtupleConsumer.h"
#include "Artus/Utility/interface/Utility.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/TauTauRestFrameSelector.h"


void TauTauRestFrameSelector::Init(setting_type const& settings, metadata_type& metadata)
{
	ProducerBase<HttTypes>::Init(settings, metadata);
	
	tauTauRestFrameReco = HttEnumTypes::ToTauTauRestFrameReco(boost::algorithm::to_lower_copy(boost::algorithm::trim_copy(settings.GetTauTauRestFrameReco())));
	
	// add possible quantities for the lambda ntuples consumers
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "diTauPt", [](event_type const& event, product_type const& product) {
		return product.m_diTauSystem.Pt();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "diTauEta", [](event_type const& event, product_type const& product) {
		return product.m_diTauSystem.Eta();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "diTauPhi", [](event_type const& event, product_type const& product) {
		return product.m_diTauSystem.Phi();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "diTauMass", [](event_type const& event, product_type const& product) {
		return product.m_diTauSystem.mass();
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "diTauSystemReconstructed", [](event_type const& event, product_type const& product) {
		return (product.m_diTauSystemReconstructed ? 1.0 : 0.0);
	});
}

void TauTauRestFrameSelector::Produce(event_type const& event, product_type& product,
                                      setting_type const& settings, metadata_type const& metadata) const
{
	// consider only the first two leptons
	assert(product.m_flavourOrderedLeptons.size() >= 2);

	product.m_flavourOrderedTauMomenta.clear();

	// select the requested restframe reconstruction
	if (tauTauRestFrameReco == HttEnumTypes::TauTauRestFrameReco::VISIBLE_LEPTONS)
	{
		product.m_flavourOrderedTauMomenta.push_back(product.m_flavourOrderedLeptons[0]->p4);
		product.m_flavourOrderedTauMomenta.push_back(product.m_flavourOrderedLeptons[1]->p4);
		product.m_tauMomentaReconstructed = false;
		
		product.m_diTauSystem = product.m_diLeptonSystem;
		product.m_diTauSystemReconstructed = false;
	}
	if (tauTauRestFrameReco == HttEnumTypes::TauTauRestFrameReco::VISIBLE_LEPTONS_MET)
	{
		product.m_tauMomentaReconstructed = false;
		
		product.m_diTauSystem = product.m_diLeptonPlusMetSystem;
		product.m_diTauSystemReconstructed = false;
	}
	else if (tauTauRestFrameReco == HttEnumTypes::TauTauRestFrameReco::COLLINEAR_APPROXIMATION)
	{
		product.m_flavourOrderedTauMomenta = product.m_flavourOrderedTauMomentaCA;
		
		// fall back to VISIBLE_LEPTONS_MET system in case of non-physical CA solutions
		product.m_diTauSystem = (product.m_validCollinearApproximation ? product.m_diTauSystemCA : product.m_diLeptonPlusMetSystem);
		product.m_diTauSystemReconstructed = product.m_validCollinearApproximation;
	}
	else if (tauTauRestFrameReco == HttEnumTypes::TauTauRestFrameReco::SVFIT)
	{
		product.m_tauMomentaReconstructed = false;
		product.m_diTauSystem = *(product.m_svfitResults.fittedHiggsLV);
		product.m_diTauSystemReconstructed = (product.m_diTauSystem.mass() > 0.0); // TODO
	}
	else
	{
		LOG(FATAL) << "TauTau restframe reconstruction of type " << Utility::ToUnderlyingValue(tauTauRestFrameReco) << " not yet implemented!";
	}
	
	// calculate boosts
	for (std::vector<RMFLV>::const_iterator tauMomentum = product.m_flavourOrderedTauMomenta.begin();
	     tauMomentum != product.m_flavourOrderedTauMomenta.end(); ++tauMomentum)
	{
		product.m_boostsToTauRestFrames.push_back(ROOT::Math::Boost(tauMomentum->BoostToCM()));
	}
	
	product.m_boostToDiTauRestFrame = ROOT::Math::Boost(product.m_diTauSystem.BoostToCM());
	
	product.m_tauTauRestFrameReco = tauTauRestFrameReco;
}

