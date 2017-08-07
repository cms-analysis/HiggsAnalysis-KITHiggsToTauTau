
#include <boost/algorithm/string.hpp>
#include <boost/algorithm/string/trim.hpp>
#include <boost/filesystem/convenience.hpp>
#include "boost/functional/hash.hpp"

#include "TauAnalysis/SVfitStandalone/interface/SVfitStandaloneAlgorithm.h"

#include "Artus/Consumer/interface/LambdaNtupleConsumer.h"
#include "Artus/Utility/interface/DefaultValues.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttEnumTypes.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/SvfitProducer.h"


void SvfitProducer::Init(setting_type const& settings)
{
	ProducerBase<HttTypes>::Init(settings);
	
	integrationMethod = SvfitEventKey::ToIntegrationMethod(
			boost::algorithm::to_lower_copy(boost::algorithm::trim_copy(settings.GetSvfitIntegrationMethod()))
	);
	
	if (! settings.GetSvfitCacheFile().empty())
	{
		svfitTools.Init(
				settings.GetSvfitCacheFile(),
				boost::algorithm::to_lower_copy(settings.GetChannel())+"_"+settings.GetSvfitCacheFileFolder()+"/"+settings.GetSvfitCacheTree()
		);
	}
	
	svfitCacheMissBehaviour = HttEnumTypes::ToSvfitCacheMissBehaviour(settings.GetSvfitCacheMissBehaviour());
	// add possible quantities for the lambda ntuples consumers
	LambdaNtupleConsumer<HttTypes>::AddBoolQuantity("svfitAvailable", [](event_type const& event, product_type const& product) {
		return (product.m_svfitResults.fittedHiggsLV ? true : false);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("svfitPt", [](event_type const& event, product_type const& product) {
		return (product.m_svfitResults.fittedHiggsLV ? product.m_svfitResults.fittedHiggsLV->Pt() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("svfitEta", [](event_type const& event, product_type const& product) {
		return (product.m_svfitResults.fittedHiggsLV ? product.m_svfitResults.fittedHiggsLV->Eta() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("svfitPhi", [](event_type const& event, product_type const& product) {
		return (product.m_svfitResults.fittedHiggsLV ? product.m_svfitResults.fittedHiggsLV->Phi() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("svfitMass", [](event_type const& event, product_type const& product) {
		return (product.m_svfitResults.fittedHiggsLV ? product.m_svfitResults.fittedHiggsLV->mass() : DefaultValues::UndefinedFloat);
	});

	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity("svfitLV", [](event_type const& event, product_type const& product) {
		return (product.m_svfitResults.fittedHiggsLV ? *(product.m_svfitResults.fittedHiggsLV) : DefaultValues::UndefinedRMFLV);
	});
	
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("svfitTransverseMass", [](event_type const& event, product_type const& product) {
		return (product.m_svfitResults.fittedTransverseMass ? static_cast<float>(product.m_svfitResults.fittedTransverseMass) : DefaultValues::UndefinedFloat);
	});
	
	LambdaNtupleConsumer<HttTypes>::AddBoolQuantity("svfitTau1Available", [](event_type const& event, product_type const& product) {
		return (product.m_svfitResults.fittedTau1LV ? true : false);
	});
	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity("svfitTau1LV", [](event_type const& event, product_type const& product) {
		return (product.m_svfitResults.fittedTau1LV ? *(product.m_svfitResults.fittedTau1LV) : DefaultValues::UndefinedRMFLV);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("svfitTau1ERatio", [](event_type const& event, product_type const& product) {
		return product.m_svfitResults.fittedTau1ERatio;
	});
	
	LambdaNtupleConsumer<HttTypes>::AddBoolQuantity("svfitTau2Available", [](event_type const& event, product_type const& product) {
		return (product.m_svfitResults.fittedTau2LV ? true : false);
	});
	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity("svfitTau2LV", [](event_type const& event, product_type const& product) {
		return (product.m_svfitResults.fittedTau2LV ? *(product.m_svfitResults.fittedTau2LV) : DefaultValues::UndefinedRMFLV);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("svfitTau2ERatio", [](event_type const& event, product_type const& product) {
		return product.m_svfitResults.fittedTau2ERatio;
	});
}

void SvfitProducer::Produce(event_type const& event, product_type& product,
                            setting_type const& settings) const
{
	assert(event.m_eventInfo);

	// consider only the first two leptons
	assert(product.m_flavourOrderedLeptons.size() >= 2);
	
	// construct decay types
	svFitStandalone::kDecayType decayType1 = svFitStandalone::kTauToHadDecay;
	if (product.m_decayChannel == HttEnumTypes::DecayChannel::MT || product.m_decayChannel == HttEnumTypes::DecayChannel::MM)
	{
		decayType1 = svFitStandalone::kTauToMuDecay;
	}
	else if (product.m_decayChannel == HttEnumTypes::DecayChannel::ET || product.m_decayChannel == HttEnumTypes::DecayChannel::EM || product.m_decayChannel == HttEnumTypes::DecayChannel::EE)
	{
		decayType1 = svFitStandalone::kTauToElecDecay;
	}
	
	svFitStandalone::kDecayType decayType2 = svFitStandalone::kTauToHadDecay;
	if (product.m_decayChannel == HttEnumTypes::DecayChannel::MM || product.m_decayChannel == HttEnumTypes::DecayChannel::EM)
	{
		decayType2 = svFitStandalone::kTauToMuDecay;
	}
	else if (product.m_decayChannel == HttEnumTypes::DecayChannel::EE)
	{
		decayType2 = svFitStandalone::kTauToElecDecay;
	}

	// set decayModes. For hadronic taus use the one from the decayModeFinding (OldDMs). Else set it to -1 (this is the default)
	int decayMode1, decayMode2;
	if (decayType1 == svFitStandalone::kTauToHadDecay)
	{
		KLepton* lepton = product.m_flavourOrderedLeptons[0];
		if (lepton->flavour() == KLeptonFlavour::TAU)
		{
			decayMode1 = static_cast<KTau*>(lepton)->decayMode;
		}
		else
		{
			decayMode1 = -1;
		}
	}
	else
	{
		decayMode1 = -1;
	}
	if (decayType2 == svFitStandalone::kTauToHadDecay)
	{
		KLepton* lepton = product.m_flavourOrderedLeptons[1];
		if (lepton->flavour() == KLeptonFlavour::TAU)
		{
			decayMode2 = static_cast<KTau*>(lepton)->decayMode;
		}
		else
		{
			decayMode2 = -1;
		}
	}
	else
	{
		decayMode2 = -1;
	}
	// construct inputs
	product.m_svfitInputs.Set(product.m_flavourOrderedLeptons[0]->p4, product.m_flavourOrderedLeptons[1]->p4,
	                          product.m_met.p4.Vect(), product.m_met.significance, decayMode1, decayMode2);
	
	// construct event key
	size_t runLumiEvent = 0;
	boost::hash_combine(runLumiEvent, event.m_eventInfo->nRun);
	boost::hash_combine(runLumiEvent, event.m_eventInfo->nLumi);
	boost::hash_combine(runLumiEvent, event.m_eventInfo->nEvent);

	product.m_svfitEventKey.Set(runLumiEvent, decayType1, decayType2,
	                            product.m_systematicShift, product.m_systematicShiftSigma, integrationMethod, product.m_met.leptonSelectionHash);

//	if (settings.GetGenerateSvfitInput())
//	{
//		// set dummy result
//		product.m_svfitResults = SvfitResults();
//		product.m_svfitCalculated = true;
//	}
//	else
	{
		// calculate results
		product.m_svfitResults = svfitTools.GetResults(
				product.m_svfitEventKey,
				product.m_svfitInputs,
				product.m_svfitCalculated,
				svfitCacheMissBehaviour
		);
		
		// apply systematic shifts
		if(product.m_svfitResults.fittedHiggsLV)
		{
			product.m_svfitResults.fittedHiggsLV->SetM(product.m_svfitResults.fittedHiggsLV->M() * settings.GetSvfitMassShift());
		}
	}
	
}

