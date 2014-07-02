
#include <boost/algorithm/string.hpp>
#include <boost/algorithm/string/trim.hpp>

#include "TauAnalysis/SVfitStandalone/interface/SVfitStandaloneAlgorithm.h"

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
	
	for (std::vector<KLepton*>::const_iterator lepton = product.m_flavourOrderedLeptons.begin();
	     lepton != product.m_flavourOrderedLeptons.end(); ++lepton)
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
	
	for (std::vector<KLepton*>::const_iterator lepton = product.m_flavourOrderedLeptons.begin();
	     lepton != product.m_flavourOrderedLeptons.end(); ++lepton)
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
	std::vector<RMLV> tauMomenta;
	
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
		std::vector<RMLV> tauMomenta;
		tauMomenta.push_back(RMLV(product.m_flavourOrderedLeptons[0]->p4 / ratioVisToTau1));
		tauMomenta.push_back(RMLV(product.m_flavourOrderedLeptons[1]->p4 / ratioVisToTau2));
		return tauMomenta;
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
	
	std::vector<svFitStandalone::MeasuredTauLepton> measuredTauLeptons {
		svFitStandalone::MeasuredTauLepton(decayType1, svFitStandalone::LorentzVector(product.m_flavourOrderedLeptons[0]->p4)),
		svFitStandalone::MeasuredTauLepton(decayType2, svFitStandalone::LorentzVector(product.m_flavourOrderedLeptons[1]->p4))
	};
	
	TMatrixD metCovariance(2, 2);
	metCovariance[0][0] = product.m_met->significance.At(0, 0);
	metCovariance[1][0] = product.m_met->significance.At(1, 0);
	metCovariance[0][1] = product.m_met->significance.At(0, 1);
	metCovariance[1][1] = product.m_met->significance.At(1, 1);
	
	int verbosity = 0;
	
	SVfitStandaloneAlgorithm svfitAlgorithm(measuredTauLeptons,
	                                        svFitStandalone::Vector(product.m_met->p4.Vect()),
	                                        metCovariance,
	                                        verbosity);
	
	svfitAlgorithm.addLogM(false);
	
	if (settings.GetSvfitUseVegasInsteadOfMarkovChain())
	{
		svfitAlgorithm.integrateVEGAS();
	}
	else
	{
		svfitAlgorithm.integrateMarkovChain();
	}
	
	RMLV tauMomentum;
	tauMomentum.SetPt(svfitAlgorithm.pt());
	tauMomentum.SetEta(svfitAlgorithm.eta());
	tauMomentum.SetPhi(svfitAlgorithm.phi());
	tauMomentum.SetM(svfitAlgorithm.mass());
	
	/*
	if (! settings.GetSvfitUseVegasInsteadOfMarkovChain())
	{
		double diTauPtErr = svfitAlgorithm.getPtUncert();
		double diTauEtaErr = svfitAlgorithm.getEtaUncert();
		double diTauPhiErr = svfitAlgorithm.getPhiUncert();
		double diTauMassErr = svfitAlgorithm.getMassUncert();
	}
	*/
	
	return std::vector<RMLV>(1, tauMomentum);
}
