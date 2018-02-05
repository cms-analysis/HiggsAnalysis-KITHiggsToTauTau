
#include <boost/algorithm/string.hpp>
#include <boost/algorithm/string/trim.hpp>
#include <boost/filesystem/convenience.hpp>
#include "boost/functional/hash.hpp"

#include "TauAnalysis/SVfitStandalone/interface/SVfitStandaloneAlgorithm.h"

#include "Artus/Consumer/interface/LambdaNtupleConsumer.h"
#include "Artus/Utility/interface/DefaultValues.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttEnumTypes.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/SvfitProducer.h"


void SvfitProducer::Init(setting_type const& settings, metadata_type& metadata)
{
	ProducerBase<HttTypes>::Init(settings, metadata);
	
	if (! settings.GetSvfitCacheFile().empty())
	{
		svfitTools.Init(
				settings.GetSvfitCacheFile(),
				boost::algorithm::to_lower_copy(settings.GetChannel())+"_"+settings.GetSvfitCacheFileFolder()+"/"+settings.GetSvfitCacheTree()
		);
	}
	
	svfitCacheMissBehaviour = HttEnumTypes::ToSvfitCacheMissBehaviour(settings.GetSvfitCacheMissBehaviour());
	// add possible quantities for the lambda ntuples consumers
	LambdaNtupleConsumer<HttTypes>::AddBoolQuantity(metadata, "svfitAvailable", [](event_type const& event, product_type const& product) {
		return (product.m_svfitResults.fittedHiggsLV ? true : false);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "svfitPt", [](event_type const& event, product_type const& product) {
		return (product.m_svfitResults.fittedHiggsLV ? product.m_svfitResults.fittedHiggsLV->Pt() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "svfitEta", [](event_type const& event, product_type const& product) {
		return (product.m_svfitResults.fittedHiggsLV ? product.m_svfitResults.fittedHiggsLV->Eta() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "svfitPhi", [](event_type const& event, product_type const& product) {
		return (product.m_svfitResults.fittedHiggsLV ? product.m_svfitResults.fittedHiggsLV->Phi() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "svfitMass", [](event_type const& event, product_type const& product) {
		return (product.m_svfitResults.fittedHiggsLV ? product.m_svfitResults.fittedHiggsLV->mass() : DefaultValues::UndefinedFloat);
	});

	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity(metadata, "svfitLV", [](event_type const& event, product_type const& product) {
		return (product.m_svfitResults.fittedHiggsLV ? *(product.m_svfitResults.fittedHiggsLV) : DefaultValues::UndefinedRMFLV);
	});
	
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "svfitTransverseMass", [](event_type const& event, product_type const& product) {
		return (product.m_svfitResults.fittedTransverseMass ? static_cast<float>(product.m_svfitResults.fittedTransverseMass) : DefaultValues::UndefinedFloat);
	});
	
	LambdaNtupleConsumer<HttTypes>::AddBoolQuantity(metadata, "svfitTau1Available", [](event_type const& event, product_type const& product) {
		return (product.m_svfitResults.fittedTau1LV ? true : false);
	});
	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity(metadata, "svfitTau1LV", [](event_type const& event, product_type const& product) {
		return (product.m_svfitResults.fittedTau1LV ? *(product.m_svfitResults.fittedTau1LV) : DefaultValues::UndefinedRMFLV);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "svfitTau1ERatio", [](event_type const& event, product_type const& product) {
		return product.m_svfitResults.fittedTau1ERatio;
	});
	
	LambdaNtupleConsumer<HttTypes>::AddBoolQuantity(metadata, "svfitTau2Available", [](event_type const& event, product_type const& product) {
		return (product.m_svfitResults.fittedTau2LV ? true : false);
	});
	LambdaNtupleConsumer<HttTypes>::AddRMFLVQuantity(metadata, "svfitTau2LV", [](event_type const& event, product_type const& product) {
		return (product.m_svfitResults.fittedTau2LV ? *(product.m_svfitResults.fittedTau2LV) : DefaultValues::UndefinedRMFLV);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "svfitTau2ERatio", [](event_type const& event, product_type const& product) {
		return product.m_svfitResults.fittedTau2ERatio;
	});
}

void SvfitProducer::Produce(event_type const& event, product_type& product,
                            setting_type const& settings, metadata_type const& metadata) const
{
	assert(event.m_eventInfo);

	// consider only the first two leptons
	assert(product.m_flavourOrderedLeptons.size() >= 2);
	KLepton* lepton1 = product.m_flavourOrderedLeptons[0];
	KLepton* lepton2 = product.m_flavourOrderedLeptons[1];
	
	// construct decay types/modes
	classic_svFit::MeasuredTauLepton::kDecayType decayType1 = classic_svFit::MeasuredTauLepton::kTauToHadDecay;
	int decayMode1 = -1;
	if (lepton1->flavour() == KLeptonFlavour::ELECTRON)
	{
		decayType1 = classic_svFit::MeasuredTauLepton::kTauToElecDecay;
		decayMode1 = -1;
	}
	else if (lepton1->flavour() == KLeptonFlavour::MUON)
	{
		decayType1 = classic_svFit::MeasuredTauLepton::kTauToMuDecay;
		decayMode1 = -1;
	}
	else if (lepton1->flavour() == KLeptonFlavour::TAU)
	{
		decayType1 = classic_svFit::MeasuredTauLepton::kTauToHadDecay;
		decayMode1 = static_cast<KTau*>(lepton1)->decayMode;
	}
	
	classic_svFit::MeasuredTauLepton::kDecayType decayType2 = classic_svFit::MeasuredTauLepton::kTauToHadDecay;
	int decayMode2 = -1;
	if (lepton2->flavour() == KLeptonFlavour::ELECTRON)
	{
		decayType2 = classic_svFit::MeasuredTauLepton::kTauToElecDecay;
		decayMode2 = -1;
	}
	else if (lepton2->flavour() == KLeptonFlavour::MUON)
	{
		decayType2 = classic_svFit::MeasuredTauLepton::kTauToMuDecay;
		decayMode2 = -1;
	}
	else if (lepton2->flavour() == KLeptonFlavour::TAU)
	{
		decayType2 = classic_svFit::MeasuredTauLepton::kTauToHadDecay;
		decayMode2 = static_cast<KTau*>(lepton2)->decayMode;
	}
	
	// construct inputs
	product.m_svfitInputs.Set(lepton1->p4, lepton2->p4,
	                          product.m_met.p4.Vect(), product.m_met.significance);
	
	// construct event key
	size_t runLumiEvent = 0;
	boost::hash_combine(runLumiEvent, event.m_eventInfo->nRun);
	boost::hash_combine(runLumiEvent, event.m_eventInfo->nLumi);
	boost::hash_combine(runLumiEvent, event.m_eventInfo->nEvent);

	product.m_svfitEventKey.Set(runLumiEvent, decayType1, decayType2, decayMode1, decayMode2,
	                            product.m_systematicShift, product.m_systematicShiftSigma,
	                            settings.GetDiTauMassConstraint());


	// calculate results
	product.m_svfitResults = svfitTools.GetResults(
			product.m_svfitEventKey,
			product.m_svfitInputs,
			product.m_svfitCalculated,
			svfitCacheMissBehaviour,
			settings.GetSvfitKappaParameter()
	);
	
	if (product.m_svfitResults.fittedTau1LV)
	{
		product.m_svfitTaus[lepton1] = *(product.m_svfitResults.fittedTau1LV);
	}
	if (product.m_svfitResults.fittedTau2LV)
	{
		product.m_svfitTaus[lepton2] = *(product.m_svfitResults.fittedTau2LV);
	}
	
	// apply systematic shifts
	if(product.m_svfitResults.fittedHiggsLV)
	{
		product.m_svfitResults.fittedHiggsLV->SetM(product.m_svfitResults.fittedHiggsLV->M() * settings.GetSvfitMassShift());
	}
}
