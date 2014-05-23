
#include "Artus/Utility/interface/DefaultValues.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/HttValidMuonsProducer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Calculations/ParticleIsolation.h"


void HttValidMuonsProducer::InitGlobal(global_setting_type const& globalSettings)
{
	ValidMuonsProducer::InitGlobal(globalSettings);
	
	chargedIsoVetoConeSize = globalSettings.GetMuonChargedIsoVetoConeSize();
	neutralIsoVetoConeSize = globalSettings.GetMuonNeutralIsoVetoConeSize();
	photonIsoVetoConeSize = globalSettings.GetMuonPhotonIsoVetoConeSize();
	deltaBetaIsoVetoConeSize = globalSettings.GetMuonDeltaBetaIsoVetoConeSize();
	
	chargedIsoPtThreshold = globalSettings.GetMuonChargedIsoPtThreshold();
	neutralIsoPtThreshold = globalSettings.GetMuonNeutralIsoPtThreshold();
	photonIsoPtThreshold = globalSettings.GetMuonPhotonIsoPtThreshold();
	deltaBetaIsoPtThreshold = globalSettings.GetMuonDeltaBetaIsoPtThreshold();
	
	isoSignalConeSize = globalSettings.GetIsoSignalConeSize();
	deltaBetaCorrectionFactor = globalSettings.GetDeltaBetaCorrectionFactor();
	isoPtSumOverPtThresholdEB = globalSettings.GetIsoPtSumOverPtThresholdEB();
	isoPtSumOverPtThresholdEE = globalSettings.GetIsoPtSumOverPtThresholdEE();
	
	trackDxyCut = globalSettings.GetMuonTrackDxyCut();
	trackDzCut = globalSettings.GetMuonTrackDzCut();
}

void HttValidMuonsProducer::InitLocal(setting_type const& settings)
{
	ValidMuonsProducer::InitLocal(settings);
	
	chargedIsoVetoConeSize = settings.GetMuonChargedIsoVetoConeSize();
	neutralIsoVetoConeSize = settings.GetMuonNeutralIsoVetoConeSize();
	photonIsoVetoConeSize = settings.GetMuonPhotonIsoVetoConeSize();
	deltaBetaIsoVetoConeSize = settings.GetMuonDeltaBetaIsoVetoConeSize();
	
	chargedIsoPtThreshold = settings.GetMuonChargedIsoPtThreshold();
	neutralIsoPtThreshold = settings.GetMuonNeutralIsoPtThreshold();
	photonIsoPtThreshold = settings.GetMuonPhotonIsoPtThreshold();
	deltaBetaIsoPtThreshold = settings.GetMuonDeltaBetaIsoPtThreshold();
	
	isoSignalConeSize = settings.GetIsoSignalConeSize();
	deltaBetaCorrectionFactor = settings.GetDeltaBetaCorrectionFactor();
	isoPtSumOverPtThresholdEB = settings.GetIsoPtSumOverPtThresholdEB();
	isoPtSumOverPtThresholdEE = settings.GetIsoPtSumOverPtThresholdEE();
	
	trackDxyCut = settings.GetMuonTrackDxyCut();
	trackDzCut = settings.GetMuonTrackDzCut();
}

bool HttValidMuonsProducer::AdditionalCriteria(KDataMuon* muon,
                                               event_type const& event,
                                               product_type& product) const
{
	bool validMuon = ValidMuonsProducer::AdditionalCriteria(muon, event, product);
	double isolationPtSum = DefaultValues::UndefinedDouble;

	if (validMuon && muonIsoType == MuonIsoType::USER) {
		isolationPtSum = ParticleIsolation::IsolationPtSum(
				muon->p4, event,
				isoSignalConeSize,
				deltaBetaCorrectionFactor,
				chargedIsoVetoConeSize,
				chargedIsoVetoConeSize,
				neutralIsoVetoConeSize,
				photonIsoVetoConeSize,
				photonIsoVetoConeSize,
				deltaBetaIsoVetoConeSize,
				chargedIsoPtThreshold,
				neutralIsoPtThreshold,
				photonIsoPtThreshold,
				deltaBetaIsoPtThreshold
		);
		
		double isolationPtSumOverPt = isolationPtSum / muon->p4.Pt();
		
		if ((muon->p4.Eta() < DefaultValues::EtaBorderEB && isolationPtSumOverPt > isoPtSumOverPtThresholdEB) ||
		    (muon->p4.Eta() >= DefaultValues::EtaBorderEB && isolationPtSumOverPt > isoPtSumOverPtThresholdEE)) {
			validMuon = false;
		}
	}
	
	// (tighter) cut on impact parameters of track
	validMuon = validMuon
	            && (trackDxyCut <= 0.0 || std::abs(muon->bestTrack.getDxy(&event.m_vertexSummary->pv)) < trackDxyCut)
	            && (trackDzCut <= 0.0 || std::abs(muon->bestTrack.getDz(&event.m_vertexSummary->pv)) < trackDzCut);

	if (validMuon) {
		product.m_validComputedMuons[muon].isolationValue = isolationPtSum / muon->p4.Pt();
	}

	return validMuon;
}

