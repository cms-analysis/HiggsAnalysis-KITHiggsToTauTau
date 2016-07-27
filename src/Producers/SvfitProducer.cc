
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
		std::string svfitCacheFile = settings.GetSvfitCacheFile();
		// Check if we need to look in a subfolder
		if ( ! settings.GetSvfitCacheFileFolder().empty())
		{
			// modify the path to include the subfolder defined in the setting SvfitCacheFileFolder
			boost::filesystem::path inputFilePath(svfitCacheFile);
			boost::filesystem::path inputFileName = inputFilePath.filename();
			inputFilePath = inputFilePath.parent_path();
			inputFilePath /= boost::filesystem::path(settings.GetSvfitCacheFileFolder());
			inputFilePath /= inputFileName;
			svfitCacheFile = inputFilePath.string();
		}
		svfitTools.Init(std::vector<std::string>(1, svfitCacheFile),
		                               settings.GetSvfitCacheTree());
	}
	else if ( ! settings.GetSvfitCacheFilePrefix().empty())
	{
		std::vector<std::string> cacheFiles;
		for (auto file : settings.GetInputFiles()) {
			cacheFiles.push_back(settings.GetSvfitCacheFilePrefix()+boost::filesystem::basename(boost::filesystem::path(file))+std::string(".root"));
		}
		svfitTools.Init(cacheFiles, settings.GetSvfitCacheTree());
	}
	svfitCacheMissBehaviour = HttEnumTypes::ToSvfitCacheMissBehaviour(settings.GetSvfitCacheMissBehaviour());
	// add possible quantities for the lambda ntuples consumers
	LambdaNtupleConsumer<HttTypes>::AddBoolQuantity("svfitAvailable", [](event_type const& event, product_type const& product) {
		return (product.m_svfitResults.momentum ? true : false);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("svfitPt", [](event_type const& event, product_type const& product) {
		return (product.m_svfitResults.momentum ? product.m_svfitResults.momentum->Pt() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("svfitEta", [](event_type const& event, product_type const& product) {
		return (product.m_svfitResults.momentum ? product.m_svfitResults.momentum->Eta() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("svfitPhi", [](event_type const& event, product_type const& product) {
		return (product.m_svfitResults.momentum ? product.m_svfitResults.momentum->Phi() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("svfitMass", [](event_type const& event, product_type const& product) {
		return (product.m_svfitResults.momentum ? product.m_svfitResults.momentum->mass() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("svfitMet", [](event_type const& event, product_type const& product) {
		return (product.m_svfitResults.fittedMET ? product.m_svfitResults.fittedMET->Rho() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("svfitTransverseMass", [](event_type const& event, product_type const& product) {
		return (product.m_svfitResults.transverseMass ? static_cast<float>(*(product.m_svfitResults.transverseMass)) : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("svfitTransverseMassUnc", [](event_type const& event, product_type const& product) {
		return (product.m_svfitResults.transverseMassUnc ? static_cast<float>(*(product.m_svfitResults.transverseMassUnc)) : DefaultValues::UndefinedFloat);
	});
	
	LambdaNtupleConsumer<HttTypes>::AddBoolQuantity("svfitUncAvailable", [](event_type const& event, product_type const& product) {
		return (product.m_svfitResults.momentumUncertainty ? true : false);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("svfitUncPt", [](event_type const& event, product_type const& product) {
		return (product.m_svfitResults.momentumUncertainty ? product.m_svfitResults.momentumUncertainty->Pt() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("svfitUncEta", [](event_type const& event, product_type const& product) {
		return (product.m_svfitResults.momentumUncertainty ? product.m_svfitResults.momentumUncertainty->Eta() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("svfitUncPhi", [](event_type const& event, product_type const& product) {
		return (product.m_svfitResults.momentumUncertainty ? product.m_svfitResults.momentumUncertainty->Phi() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("svfitUncMass", [](event_type const& event, product_type const& product) {
		return (product.m_svfitResults.momentumUncertainty ? product.m_svfitResults.momentumUncertainty->mass() : DefaultValues::UndefinedFloat);
	});
}

void SvfitProducer::Produce(event_type const& event, product_type& product,
                            setting_type const& settings) const
{
	assert(event.m_eventInfo);
	assert(product.m_metUncorr);

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
		product.m_svfitResults = svfitTools.GetResults(product.m_svfitEventKey,
		                                                              product.m_svfitInputs,
	                                                                  product.m_svfitCalculated,
	                                                                  svfitCacheMissBehaviour);
		// apply systematic shifts
		if( product.m_svfitResults.momentum )
			product.m_svfitResults.momentum->SetM(product.m_svfitResults.momentum->M() * settings.GetSvfitMassShift());
	}
	
}

