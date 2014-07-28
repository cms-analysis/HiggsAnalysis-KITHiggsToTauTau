
#include <boost/algorithm/string.hpp>
#include <boost/algorithm/string/trim.hpp>

#include "DataFormats/TauReco/interface/PFTau.h"

#include "Artus/Utility/interface/SafeMap.h"
#include "Artus/Utility/interface/Utility.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/HttTauCorrectionsProducer.h"

	
void HttTauCorrectionsProducer::Init(setting_type const& settings)
{
	TauCorrectionsProducer<HttTypes>::Init(settings);
	
	tauEnergyCorrection = ToTauEnergyCorrection(boost::algorithm::to_lower_copy(boost::algorithm::trim_copy(settings.GetTauEnergyCorrection())));
}

void HttTauCorrectionsProducer::AdditionalCorrections(KDataPFTau* tau, event_type const& event,
                                                      product_type& product, setting_type const& settings) const
{
	TauCorrectionsProducer<HttTypes>::AdditionalCorrections(tau, event, product, settings);
	
	double normalisationFactor = 1.0;
	
	// https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsToTauTauWorkingSummer2013#TauES_and_decay_mode_scale_facto
	if (tauEnergyCorrection == TauEnergyCorrection::SUMMER2013)
	{
		// http://cmslxr.fnal.gov/lxr/source/DataFormats/TauReco/interface/PFTau.h#035
		if (tau->hpsDecayMode == reco::PFTau::hadronicDecayMode::kOneProng0PiZero)
		{
			normalisationFactor = 0.88;
		}
		else if (tau->hpsDecayMode == reco::PFTau::hadronicDecayMode::kOneProng1PiZero || tau->hpsDecayMode == reco::PFTau::hadronicDecayMode::kOneProng2PiZero)
		{
			tau->p4 = tau->p4 * (1.012);
// 			tau->p4 = tau->p4 * (1.015 + 0.001 * std::min(std::max(tau->p4.Pt() - 45.0, 0.0), 10.0));
		}
		else if (tau->hpsDecayMode == reco::PFTau::hadronicDecayMode::kThreeProng0PiZero)
		{
			tau->p4 = tau->p4 * (1.012);
// 			tau->p4 = tau->p4 * (1.012 + 0.001 * std::min(std::max(tau->p4.Pt() - 32.0, 0.0), 18.0));
		}
	}
	else if (tauEnergyCorrection != TauEnergyCorrection::NONE)
	{
		LOG(FATAL) << "Tau energy correction of type " << Utility::ToUnderlyingValue(tauEnergyCorrection) << " not yet implemented!";
	}
	
	product.m_tauEnergyScaleWeight[tau] = normalisationFactor;
}

