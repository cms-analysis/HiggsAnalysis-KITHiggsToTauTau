
#include <boost/algorithm/string.hpp>
#include <boost/algorithm/string/trim.hpp>

#include "TauAnalysis/SVfitStandalone/interface/SVfitStandaloneAlgorithm.h"

#include "Artus/Utility/interface/RootFileHelper.h"
#include "Artus/Utility/interface/Utility.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/Utility/SvfitTools.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/TauTauRestFrameProducer.h"


SvfitTools TauTauRestFrameProducer::svfitTools = SvfitTools();

TauTauRestFrameProducer::~TauTauRestFrameProducer()
{
}

void TauTauRestFrameProducer::Init(setting_type const& settings)
{
	tauTauRestFrameReco = ToTauTauRestFrameReco(boost::algorithm::to_lower_copy(boost::algorithm::trim_copy(settings.GetTauTauRestFrameReco())));
	
	if (! settings.GetSvfitCacheFile().empty())
	{
		TauTauRestFrameProducer::svfitTools.Init(std::vector<std::string>(1, settings.GetSvfitCacheFile()),
		                                         settings.GetSvfitCacheTree());
	}
}

void TauTauRestFrameProducer::Produce(event_type const& event, product_type& product,
                                      setting_type const& settings) const
{
	std::vector<RMDataLV> tauTauMomenta;

	// perform requested restframe reconstruction
	if (tauTauRestFrameReco == TauTauRestFrameReco::VISIBLE_LEPTONS)
	{
		tauTauMomenta = ProduceVisibleLeptonsRestFrame(event, product, settings);
	}
	else if (tauTauRestFrameReco == TauTauRestFrameReco::VISIBLE_LEPTONS_MET)
	{
		tauTauMomenta = ProduceVisibleLeptonsMetRestFrame(event, product, settings);
	}
	else if (tauTauRestFrameReco == TauTauRestFrameReco::VISIBLE_LEPTONS_MET)
	{
		tauTauMomenta = ProduceVisibleLeptonsMetRestFrame(event, product, settings);
	}
	else if (tauTauRestFrameReco == TauTauRestFrameReco::COLLINEAR_APPROXIMATION)
	{
		tauTauMomenta = ProduceCollinearApproximationRestFrame(event, product, settings);
	}
	else if (tauTauRestFrameReco == TauTauRestFrameReco::SVFIT)
	{
		tauTauMomenta = ProduceSvfitRestFrame(event, product, settings);
	}
	else
	{
		LOG(FATAL) << "TauTau restframe reconstruction of type " << Utility::ToUnderlyingValue(tauTauRestFrameReco) << " not yet implemented!";
	}
	
	// fill product
	if (tauTauMomenta.size() > 1)
	{
		product.m_flavourOrderedTauTauMomenta = tauTauMomenta;
		product.m_tauTauMomentaReconstructed = true;
	}
	else
	{
		product.m_tauTauMomentaReconstructed = false;
	}
	
	size_t index = 0;
	for (std::vector<RMDataLV>::const_iterator tauMomentum = tauTauMomenta.begin();
	     tauMomentum != tauTauMomenta.end(); ++tauMomentum)
	{
		if (index == 0)
		{
			product.m_tauTauMomentum = *tauMomentum;
		}
		else
		{
			product.m_tauTauMomentum += *tauMomentum;
		}
		
		product.m_boostToTauRestFrames.push_back(ROOT::Math::Boost(tauMomentum->BoostToCM()));
		
		++index;
	}
	
	product.m_boostToTauTauRestFrame = ROOT::Math::Boost(product.m_tauTauMomentum.BoostToCM());
}


std::vector<RMDataLV> TauTauRestFrameProducer::ProduceVisibleLeptonsRestFrame(event_type const& event,
                                                                          product_type& product,
                                                                          setting_type const& settings) const
{
	std::vector<RMDataLV> tauTauMomenta;
	
	for (std::vector<KLepton*>::const_iterator lepton = product.m_flavourOrderedLeptons.begin();
	     lepton != product.m_flavourOrderedLeptons.end(); ++lepton)
	{
		tauTauMomenta.push_back(RMDataLV((*lepton)->p4));
	}
	
	return tauTauMomenta;
}

std::vector<RMDataLV> TauTauRestFrameProducer::ProduceVisibleLeptonsMetRestFrame(event_type const& event,
                                                                             product_type& product,
                                                                             setting_type const& settings) const
{
	RMDataLV tauTauMomentum;
	
	for (std::vector<KLepton*>::const_iterator lepton = product.m_flavourOrderedLeptons.begin();
	     lepton != product.m_flavourOrderedLeptons.end(); ++lepton)
	{
		tauTauMomentum += (*lepton)->p4;
	}
	tauTauMomentum += product.m_met->p4;
	
	return std::vector<RMDataLV>(1, tauTauMomentum);
}

std::vector<RMDataLV> TauTauRestFrameProducer::ProduceCollinearApproximationRestFrame(event_type const& event,
                                                                                  product_type& product,
                                                                                  setting_type const& settings) const
{
	std::vector<RMDataLV> tauMomenta;
	
	// consider only the first two leptons
	assert(product.m_flavourOrderedLeptons.size() >= 2);
	double p1x = product.m_flavourOrderedLeptons[0]->p4.Px();
	double p1y = product.m_flavourOrderedLeptons[0]->p4.Py();
	double p2x = product.m_flavourOrderedLeptons[1]->p4.Px();
	double p2y = product.m_flavourOrderedLeptons[1]->p4.Py();
	double pmx = product.m_met->p4.Px();
	double pmy = product.m_met->p4.Py();
	
	// reconstruct tau momenta assuming that the neutrinos fly collinear to the taus
	// HiggsAnalysis/KITHiggsToTauTau/doc/collinear_approximation.nb
	double ratioVisToTau1 = (p1y*p2x - p1x*p2y + p2y*pmx - p2x*pmy) / (p1y*p2x - p1x*p2y);
	double ratioVisToTau2 = (p1y*p2x - p1x*p2y - p1y*pmx + p1x*pmy) / (p1y*p2x - p1x*p2y);
	
	if (ratioVisToTau1 >= 0.0 && ratioVisToTau2 >= 0.0)
	{
		std::vector<RMDataLV> tauMomenta;
		tauMomenta.push_back(RMDataLV(product.m_flavourOrderedLeptons[0]->p4 / ratioVisToTau1));
		tauMomenta.push_back(RMDataLV(product.m_flavourOrderedLeptons[1]->p4 / ratioVisToTau2));
		return tauMomenta;
	}
	else
	{
		// fall back to visible decay products and MET in case of unphysical solutions
		return ProduceVisibleLeptonsMetRestFrame(event, product, settings);
	}
	
}

std::vector<RMDataLV> TauTauRestFrameProducer::ProduceSvfitRestFrame(event_type const& event,
                                                                 product_type& product,
                                                                 setting_type const& settings) const
{
	// consider only the first two leptons
	assert(product.m_flavourOrderedLeptons.size() >= 2);
	
	// construct decay types
	svFitStandalone::kDecayType decayType1 = svFitStandalone::kTauToHadDecay;
	if (product.m_decayChannel == HttProduct::DecayChannel::MT || product.m_decayChannel == HttProduct::DecayChannel::MM)
	{
		decayType1 = svFitStandalone::kTauToMuDecay;
	}
	else if (product.m_decayChannel == HttProduct::DecayChannel::ET || product.m_decayChannel == HttProduct::DecayChannel::EE)
	{
		decayType1 = svFitStandalone::kTauToElecDecay;
	}
	
	svFitStandalone::kDecayType decayType2 = svFitStandalone::kTauToHadDecay;
	if (product.m_decayChannel == HttProduct::DecayChannel::MM)
	{
		decayType2 = svFitStandalone::kTauToMuDecay;
	}
	else if (product.m_decayChannel == HttProduct::DecayChannel::EE)
	{
		decayType2 = svFitStandalone::kTauToElecDecay;
	}
	
	// construct run, lumi, event
	product.m_runLumiEvent.Set(event.m_eventMetadata->nRun,
	                           event.m_eventMetadata->nLumi,
	                           event.m_eventMetadata->nEvent);
	
	// construct inputs
	product.m_svfitInputs.Set(decayType1, decayType2,
	                          product.m_flavourOrderedLeptons[0]->p4, product.m_flavourOrderedLeptons[1]->p4,
	                          product.m_met->p4.Vect(), product.m_met->significance);
	
	// calculate results
	product.m_svfitResults = TauTauRestFrameProducer::svfitTools.GetResults(product.m_runLumiEvent,
	                                                                        product.m_svfitInputs,
	                                                                        product.m_svfitCalculated);
	
	return std::vector<RMDataLV>(1, *(product.m_svfitResults.momentum));
}

