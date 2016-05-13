
#include <boost/algorithm/string.hpp>
#include <boost/algorithm/string/trim.hpp>

#include "Artus/Utility/interface/SafeMap.h"
#include "Artus/Utility/interface/Utility.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttEnumTypes.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/HttMuonCorrectionsProducer.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/Utility/RoccoR.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Utility/rochcor2015.h"
#include "TLorentzVector.h"

void HttMuonCorrectionsProducer::Init(setting_type const& settings)
{
	MuonCorrectionsProducer::Init(settings);
	
	muonEnergyCorrection = ToMuonEnergyCorrection(boost::algorithm::to_lower_copy(boost::algorithm::trim_copy(static_cast<HttSettings const&>(settings).GetMuonEnergyCorrection())));
}

void HttMuonCorrectionsProducer::AdditionalCorrections(KMuon* muon, event_type const& event,
                                                       product_type& product, setting_type const& settings) const
{
	MuonCorrectionsProducer::AdditionalCorrections(muon, event, product, settings);
	
	if (muonEnergyCorrection == MuonEnergyCorrection::FALL2015)
	{
		muon->p4 = muon->p4 * (1.0);
	}
	else if (muonEnergyCorrection == MuonEnergyCorrection::ROCHCORR2015)
	{
		rochcor2015 *rmcor = new rochcor2015(static_cast<HttSettings const&>(settings).GetMuonRochesterCorrectionsFile());

		TLorentzVector mu;
		mu.SetPtEtaPhiM(muon->p4.Pt(),muon->p4.Eta(),muon->p4.Phi(),muon->p4.mass());

		float q = muon->charge();
		float qter = 1.0;

		if (static_cast<HttSettings const&>(settings).GetInputIsData())
		{
			rmcor->momcor_data(mu, q, 0, qter);
			RMFLV muon_corr(mu.X(),mu.Y(),mu.Z(),mu.T());
			muon->p4 = muon_corr;
		}
		else
		{
			int ntrk = muon->track.nPixelLayers + muon->track.nStripLayers; // TODO: this corresponds to reco::HitPattern::trackerLayersWithMeasurementOld(). update to "new" implementation also in Kappa
			rmcor->momcor_mc(mu, q, ntrk, qter);
			RMFLV muon_corr(mu.X(),mu.Y(),mu.Z(),mu.T());
			muon->p4 = muon_corr;
		}
	}
	else if (muonEnergyCorrection != MuonEnergyCorrection::NONE)
	{
		LOG(FATAL) << "Muon energy correction of type " << Utility::ToUnderlyingValue(muonEnergyCorrection) << " not yet implemented!";
	}
	
	float muonEnergyCorrectionShift = static_cast<HttSettings const&>(settings).GetMuonEnergyCorrectionShift();
	if (muonEnergyCorrectionShift != 1.0)
	{
		muon->p4 = muon->p4 * muonEnergyCorrectionShift;
	}
}

