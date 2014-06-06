
#include "Artus/Utility/interface/DefaultValues.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/HttValidMuonsProducer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Calculations/ParticleIsolation.h"


bool HttValidMuonsProducer::AdditionalCriteria(KDataMuon* muon,
                                               event_type const& event, product_type& product,
                                               setting_type const& settings) const
{
	bool validMuon = ValidMuonsProducer<HttTypes>::AdditionalCriteria(muon, event, product, settings);
	double isolationPtSum = DefaultValues::UndefinedDouble;

	if (validMuon && muonIsoType == MuonIsoType::USER) {
		isolationPtSum = ParticleIsolation::IsolationPtSum(
				muon->p4, event,
				settings.GetIsoSignalConeSize(),
				settings.GetDeltaBetaCorrectionFactor(),
				settings.GetMuonChargedIsoVetoConeSize(),
				settings.GetMuonChargedIsoVetoConeSize(),
				settings.GetMuonNeutralIsoVetoConeSize(),
				settings.GetMuonPhotonIsoVetoConeSize(),
				settings.GetMuonPhotonIsoVetoConeSize(),
				settings.GetMuonDeltaBetaIsoVetoConeSize(),
				settings.GetMuonChargedIsoPtThreshold(),
				settings.GetMuonNeutralIsoPtThreshold(),
				settings.GetMuonPhotonIsoPtThreshold(),
				settings.GetMuonDeltaBetaIsoPtThreshold()
		);
		
		double isolationPtSumOverPt = isolationPtSum / muon->p4.Pt();
		
		product.m_leptonIsolation[muon] = isolationPtSum;
		product.m_leptonIsolationOverPt[muon] = isolationPtSumOverPt;
		
		if ((muon->p4.Eta() < DefaultValues::EtaBorderEB && isolationPtSumOverPt > settings.GetIsoPtSumOverPtThresholdEB()) ||
		    (muon->p4.Eta() >= DefaultValues::EtaBorderEB && isolationPtSumOverPt > settings.GetIsoPtSumOverPtThresholdEE())) {
			validMuon = false;
		}
	}
	
	// (tighter) cut on impact parameters of track
	validMuon = validMuon
	            && (settings.GetMuonTrackDxyCut() <= 0.0 || std::abs(muon->bestTrack.getDxy(&event.m_vertexSummary->pv)) < settings.GetMuonTrackDxyCut())
	            && (settings.GetMuonTrackDzCut() <= 0.0 || std::abs(muon->bestTrack.getDz(&event.m_vertexSummary->pv)) < settings.GetMuonTrackDzCut());

	return validMuon;
}

