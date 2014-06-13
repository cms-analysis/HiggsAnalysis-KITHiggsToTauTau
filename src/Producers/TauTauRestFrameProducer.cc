
#include <boost/algorithm/string.hpp>
#include <boost/algorithm/string/trim.hpp>

#include "Artus/Utility/interface/Utility.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/TauTauRestFrameProducer.h"


void TauTauRestFrameProducer::Init(setting_type const& settings)
{
	tauTauRestFrameReco = ToTauTauRestFrameReco(boost::algorithm::to_lower_copy(boost::algorithm::trim_copy(settings.GetTauTauRestFrameReco())));
}

void TauTauRestFrameProducer::Produce(event_type const& event, product_type& product,
                                      setting_type const& settings) const
{
	std::vector<RMLV> tauTauMomenta;

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
	//else if (tauTauRestFrameReco == TauTauRestFrameReco::SVFIT)
	//{
	//	tauTauMomenta = ProduceSvfitRestFrame(event, product, settings);
	//}
	else
	{
		LOG(FATAL) << "TauTau restframe reconstruction of type " << Utility::ToUnderlyingValue(tauTauRestFrameReco) << " not yet implemented!";
	}
	
	// fill product
	if (tauTauMomenta.size() > 0)
	{
		product.m_tauTauMomenta = tauTauMomenta;
		product.m_tauTauMomentaReconstructed = true;
	}
	else
	{
		product.m_tauTauMomentaReconstructed = false;
	}
	
	size_t index = 0;
	for (std::vector<RMLV>::const_iterator tauMomentum = tauTauMomenta.begin();
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


std::vector<RMLV> TauTauRestFrameProducer::ProduceVisibleLeptonsRestFrame(event_type const& event,
                                                                          product_type& product,
                                                                          setting_type const& settings) const
{
	std::vector<RMLV> tauTauMomenta;
	
	for (std::vector<KLepton*>::const_iterator lepton = product.m_ptOrderedLeptons.begin();
	     lepton != product.m_ptOrderedLeptons.end(); ++lepton)
	{
		tauTauMomenta.push_back(RMLV((*lepton)->p4));
	}
	
	return tauTauMomenta;
}

std::vector<RMLV> TauTauRestFrameProducer::ProduceVisibleLeptonsMetRestFrame(event_type const& event,
                                                                             product_type& product,
                                                                             setting_type const& settings) const
{
	RMLV tauTauMomentum;
	
	for (std::vector<KLepton*>::const_iterator lepton = product.m_ptOrderedLeptons.begin();
	     lepton != product.m_ptOrderedLeptons.end(); ++lepton)
	{
		tauTauMomentum += (*lepton)->p4;
	}
	tauTauMomentum += product.m_met->p4;
	
	return std::vector<RMLV>(1, tauTauMomentum);
}

std::vector<RMLV> TauTauRestFrameProducer::ProduceCollinearApproximationRestFrame(event_type const& event,
                                                                                  product_type& product,
                                                                                  setting_type const& settings) const
{
	std::vector<RMLV> tauTauMomenta;
	
	// consider only the first two leptons
	assert(product.m_ptOrderedLeptons.size() >= 2);
	double p1x = product.m_ptOrderedLeptons[0]->p4.Px();
	double p1y = product.m_ptOrderedLeptons[0]->p4.Py();
	double p2x = product.m_ptOrderedLeptons[1]->p4.Px();
	double p2y = product.m_ptOrderedLeptons[1]->p4.Py();
	double pmx = product.m_met->p4.Px();
	double pmy = product.m_met->p4.Py();
	
	// reconstruct tau momenta assuming that the neutrinos fly collinear to the taus
	// HiggsAnalysis/KITHiggsToTauTau/doc/collinear_approximation.nb
	double ratioVisToTau1 = (p1y*p2x - p1x*p2y + p2y*pmx - p2x*pmy) / (p1y*p2x - p1x*p2y);
	double ratioVisToTau2 = (p1y*p2x - p1x*p2y - p1y*pmx + p1x*pmy) / (p1y*p2x - p1x*p2y);
	
	if (ratioVisToTau1 >= 0.0 && ratioVisToTau2 >= 0.0)
	{
		std::vector<RMLV> tauTauMomenta;
		tauTauMomenta.push_back(RMLV(product.m_ptOrderedLeptons[0]->p4 * ratioVisToTau1));
		tauTauMomenta.push_back(RMLV(product.m_ptOrderedLeptons[1]->p4 * ratioVisToTau2));
		return tauTauMomenta;
	}
	else
	{
		// fall back to visible decay products and MET in case of unphysical solutions
		return ProduceVisibleLeptonsMetRestFrame(event, product, settings);
	}
	
}

std::vector<RMLV> TauTauRestFrameProducer::ProduceSvfitRestFrame(event_type const& event,
                                                                 product_type& product,
                                                                 setting_type const& settings) const
{
	std::vector<RMLV> tauTauMomenta;
	
	// TODO
	
	return tauTauMomenta;
}
