
#include <boost/algorithm/string.hpp>
#include <boost/algorithm/string/trim.hpp>

#include "TauAnalysis/SVfitStandalone/interface/SVfitStandaloneAlgorithm.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttEnumTypes.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/SvfitProducer.h"


SvfitTools SvfitProducer::svfitTools = SvfitTools();

void SvfitProducer::Init(setting_type const& settings)
{
	integrationMethod = SvfitEventKey::ToIntegrationMethod(
			boost::algorithm::to_lower_copy(boost::algorithm::trim_copy(settings.GetSvfitIntegrationMethod()))
	);
	
	if (! settings.GetSvfitCacheFile().empty())
	{
		SvfitProducer::svfitTools.Init(std::vector<std::string>(1, settings.GetSvfitCacheFile()),
		                               settings.GetSvfitCacheTree());
	}
}

void SvfitProducer::Produce(event_type const& event, product_type& product,
                            setting_type const& settings) const
{
	assert(event.m_eventInfo);
	assert(product.m_met);

	// consider only the first two leptons
	assert(product.m_flavourOrderedLeptons.size() >= 2);
	
	// construct decay types
	svFitStandalone::kDecayType decayType1 = svFitStandalone::kTauToHadDecay;
	if (product.m_decayChannel == HttEnumTypes::DecayChannel::MT || product.m_decayChannel == HttEnumTypes::DecayChannel::MM)
	{
		decayType1 = svFitStandalone::kTauToMuDecay;
	}
	else if (product.m_decayChannel == HttEnumTypes::DecayChannel::ET || product.m_decayChannel == HttEnumTypes::DecayChannel::EE)
	{
		decayType1 = svFitStandalone::kTauToElecDecay;
	}
	
	svFitStandalone::kDecayType decayType2 = svFitStandalone::kTauToHadDecay;
	if (product.m_decayChannel == HttEnumTypes::DecayChannel::MM)
	{
		decayType2 = svFitStandalone::kTauToMuDecay;
	}
	else if (product.m_decayChannel == HttEnumTypes::DecayChannel::EE)
	{
		decayType2 = svFitStandalone::kTauToElecDecay;
	}
	
	// construct event key
	product.m_svfitEventKey.Set(event.m_eventInfo->nRun, event.m_eventInfo->nLumi, event.m_eventInfo->nEvent,
	                            product.m_systematicShift, product.m_systematicShiftSigma, integrationMethod);
	
	// construct inputs
	product.m_svfitInputs.Set(decayType1, decayType2,
	                          product.m_flavourOrderedLeptons[0]->p4, product.m_flavourOrderedLeptons[1]->p4,
	                          product.m_met->p4.Vect(), product.m_met->significance);
	
	// calculate results
	product.m_svfitResults = SvfitProducer::svfitTools.GetResults(product.m_svfitEventKey,
	                                                              product.m_svfitInputs,
	                                                              product.m_svfitCalculated);
}

