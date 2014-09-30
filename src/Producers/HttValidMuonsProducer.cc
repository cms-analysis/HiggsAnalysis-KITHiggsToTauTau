
#include "Artus/Utility/interface/DefaultValues.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/HttValidMuonsProducer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Calculations/ParticleIsolation.h"


HttValidMuonsProducer::HttValidMuonsProducer(std::vector<KDataMuon*> product_type::*validMuons,
                                             std::vector<KDataMuon*> product_type::*invalidMuons,
                                             std::string (setting_type::*GetMuonID)(void) const,
                                             std::string (setting_type::*GetMuonIsoType)(void) const,
                                             std::string (setting_type::*GetMuonIso)(void) const,
                                             std::vector<std::string>& (setting_type::*GetLowerPtCuts)(void) const,
                                             std::vector<std::string>& (setting_type::*GetUpperAbsEtaCuts)(void) const,
                                             float (setting_type::*GetMuonChargedIsoVetoConeSize)(void) const,
                                             float (setting_type::*GetMuonNeutralIsoVetoConeSize)(void) const,
                                             float (setting_type::*GetMuonPhotonIsoVetoConeSize)(void) const,
                                             float (setting_type::*GetMuonDeltaBetaIsoVetoConeSize)(void) const,
                                             float (setting_type::*GetMuonChargedIsoPtThreshold)(void) const,
                                             float (setting_type::*GetMuonNeutralIsoPtThreshold)(void) const,
                                             float (setting_type::*GetMuonPhotonIsoPtThreshold)(void) const,
                                             float (setting_type::*GetMuonDeltaBetaIsoPtThreshold)(void) const,
                                             float (setting_type::*GetMuonIsoSignalConeSize)(void) const,
                                             float (setting_type::*GetMuonDeltaBetaCorrectionFactor)(void) const,
                                             float (setting_type::*GetMuonIsoPtSumOverPtThresholdEB)(void) const,
                                             float (setting_type::*GetMuonIsoPtSumOverPtThresholdEE)(void) const,
                                             float (setting_type::*GetMuonTrackDxyCut)(void) const,
                                             float (setting_type::*GetMuonTrackDzCut)(void) const) :
	ValidMuonsProducer(validMuons, invalidMuons,
	                   GetMuonID, GetMuonIsoType, GetMuonIso,
	                   GetLowerPtCuts, GetUpperAbsEtaCuts),
	GetMuonChargedIsoVetoConeSize(GetMuonChargedIsoVetoConeSize),
	GetMuonNeutralIsoVetoConeSize(GetMuonNeutralIsoVetoConeSize),
	GetMuonPhotonIsoVetoConeSize(GetMuonPhotonIsoVetoConeSize),
	GetMuonDeltaBetaIsoVetoConeSize(GetMuonDeltaBetaIsoVetoConeSize),
	GetMuonChargedIsoPtThreshold(GetMuonChargedIsoPtThreshold),
	GetMuonNeutralIsoPtThreshold(GetMuonNeutralIsoPtThreshold),
	GetMuonPhotonIsoPtThreshold(GetMuonPhotonIsoPtThreshold),
	GetMuonDeltaBetaIsoPtThreshold(GetMuonDeltaBetaIsoPtThreshold),
	GetMuonIsoSignalConeSize(GetMuonIsoSignalConeSize),
	GetMuonDeltaBetaCorrectionFactor(GetMuonDeltaBetaCorrectionFactor),
	GetMuonIsoPtSumOverPtThresholdEB(GetMuonIsoPtSumOverPtThresholdEB),
	GetMuonIsoPtSumOverPtThresholdEE(GetMuonIsoPtSumOverPtThresholdEE),
	GetMuonTrackDxyCut(GetMuonTrackDxyCut),
	GetMuonTrackDzCut(GetMuonTrackDzCut)
{
}


bool HttValidMuonsProducer::AdditionalCriteria(KDataMuon* muon,
                                               event_type const& event, product_type& product,
                                               setting_type const& settings) const
{
	bool validMuon = ValidMuonsProducer<HttTypes>::AdditionalCriteria(muon, event, product, settings);
	double isolationPtSum = DefaultValues::UndefinedDouble;

	if (validMuon && muonIsoType == MuonIsoType::USER) {
		isolationPtSum = ParticleIsolation::IsolationPtSum(
				muon->p4, event,
				(settings.*GetMuonIsoSignalConeSize)(),
				(settings.*GetMuonDeltaBetaCorrectionFactor)(),
				(settings.*GetMuonChargedIsoVetoConeSize)(),
				(settings.*GetMuonChargedIsoVetoConeSize)(),
				(settings.*GetMuonNeutralIsoVetoConeSize)(),
				(settings.*GetMuonPhotonIsoVetoConeSize)(),
				(settings.*GetMuonPhotonIsoVetoConeSize)(),
				(settings.*GetMuonDeltaBetaIsoVetoConeSize)(),
				(settings.*GetMuonChargedIsoPtThreshold)(),
				(settings.*GetMuonNeutralIsoPtThreshold)(),
				(settings.*GetMuonPhotonIsoPtThreshold)(),
				(settings.*GetMuonDeltaBetaIsoPtThreshold)()
		);
		
		double isolationPtSumOverPt = isolationPtSum / muon->p4.Pt();
		
		product.m_leptonIsolation[muon] = isolationPtSum;
		product.m_leptonIsolationOverPt[muon] = isolationPtSumOverPt;
		
		if ((std::abs(muon->p4.Eta()) < DefaultValues::EtaBorderEB && ((isolationPtSumOverPt >= (settings.*GetMuonIsoPtSumOverPtThresholdEB)()) ? settings.GetDirectIso() : (!settings.GetDirectIso()))) ||
		    (std::abs(muon->p4.Eta()) >= DefaultValues::EtaBorderEB && ((isolationPtSumOverPt >= (settings.*GetMuonIsoPtSumOverPtThresholdEE)()) ? settings.GetDirectIso() : (!settings.GetDirectIso())))) {
			validMuon = false;
		}
	}
	
	// (tighter) cut on impact parameters of track
	validMuon = validMuon
	            && ((settings.*GetMuonTrackDxyCut)() <= 0.0 || std::abs(muon->bestTrack.getDxy(&event.m_vertexSummary->pv)) < (settings.*GetMuonTrackDxyCut)())
	            && ((settings.*GetMuonTrackDzCut)() <= 0.0 || std::abs(muon->bestTrack.getDz(&event.m_vertexSummary->pv)) < (settings.*GetMuonTrackDzCut)());

	return validMuon;
}


HttValidLooseMuonsProducer::HttValidLooseMuonsProducer(
		std::vector<KDataMuon*> product_type::*validMuons,
		std::vector<KDataMuon*> product_type::*invalidMuons,
		std::string (setting_type::*GetMuonID)(void) const,
		std::string (setting_type::*GetMuonIsoType)(void) const,
		std::string (setting_type::*GetMuonIso)(void) const,
		std::vector<std::string>& (setting_type::*GetLowerPtCuts)(void) const,
		std::vector<std::string>& (setting_type::*GetUpperAbsEtaCuts)(void) const,
		float (setting_type::*GetMuonChargedIsoVetoConeSize)(void) const,
		float (setting_type::*GetMuonNeutralIsoVetoConeSize)(void) const,
		float (setting_type::*GetMuonPhotonIsoVetoConeSize)(void) const,
		float (setting_type::*GetMuonDeltaBetaIsoVetoConeSize)(void) const,
		float (setting_type::*GetMuonChargedIsoPtThreshold)(void) const,
		float (setting_type::*GetMuonNeutralIsoPtThreshold)(void) const,
		float (setting_type::*GetMuonPhotonIsoPtThreshold)(void) const,
		float (setting_type::*GetMuonDeltaBetaIsoPtThreshold)(void) const,
		float (setting_type::*GetMuonIsoSignalConeSize)(void) const,
		float (setting_type::*GetMuonDeltaBetaCorrectionFactor)(void) const,
		float (setting_type::*GetMuonIsoPtSumOverPtThresholdEB)(void) const,
		float (setting_type::*GetMuonIsoPtSumOverPtThresholdEE)(void) const,
		float (setting_type::*GetMuonTrackDxyCut)(void) const,
		float (setting_type::*GetMuonTrackDzCut)(void) const
) :
	HttValidMuonsProducer(validMuons,
	                      invalidMuons,
	                      GetMuonID,
	                      GetMuonIsoType,
	                      GetMuonIso,
	                      GetLowerPtCuts,
	                      GetUpperAbsEtaCuts,
	                      GetMuonChargedIsoVetoConeSize,
	                      GetMuonNeutralIsoVetoConeSize,
	                      GetMuonPhotonIsoVetoConeSize,
	                      GetMuonDeltaBetaIsoVetoConeSize,
	                      GetMuonChargedIsoPtThreshold,
	                      GetMuonNeutralIsoPtThreshold,
	                      GetMuonPhotonIsoPtThreshold,
	                      GetMuonDeltaBetaIsoPtThreshold,
	                      GetMuonIsoSignalConeSize,
	                      GetMuonDeltaBetaCorrectionFactor,
	                      GetMuonIsoPtSumOverPtThresholdEB,
	                      GetMuonIsoPtSumOverPtThresholdEE,
	                      GetMuonTrackDxyCut,
	                      GetMuonTrackDzCut)
{
}


HttValidVetoMuonsProducer::HttValidVetoMuonsProducer(
		std::vector<KDataMuon*> product_type::*validMuons,
		std::vector<KDataMuon*> product_type::*invalidMuons,
		std::string (setting_type::*GetMuonID)(void) const,
		std::string (setting_type::*GetMuonIsoType)(void) const,
		std::string (setting_type::*GetMuonIso)(void) const,
		std::vector<std::string>& (setting_type::*GetLowerPtCuts)(void) const,
		std::vector<std::string>& (setting_type::*GetUpperAbsEtaCuts)(void) const,
		float (setting_type::*GetMuonChargedIsoVetoConeSize)(void) const,
		float (setting_type::*GetMuonNeutralIsoVetoConeSize)(void) const,
		float (setting_type::*GetMuonPhotonIsoVetoConeSize)(void) const,
		float (setting_type::*GetMuonDeltaBetaIsoVetoConeSize)(void) const,
		float (setting_type::*GetMuonChargedIsoPtThreshold)(void) const,
		float (setting_type::*GetMuonNeutralIsoPtThreshold)(void) const,
		float (setting_type::*GetMuonPhotonIsoPtThreshold)(void) const,
		float (setting_type::*GetMuonDeltaBetaIsoPtThreshold)(void) const,
		float (setting_type::*GetMuonIsoSignalConeSize)(void) const,
		float (setting_type::*GetMuonDeltaBetaCorrectionFactor)(void) const,
		float (setting_type::*GetMuonIsoPtSumOverPtThresholdEB)(void) const,
		float (setting_type::*GetMuonIsoPtSumOverPtThresholdEE)(void) const,
		float (setting_type::*GetMuonTrackDxyCut)(void) const,
		float (setting_type::*GetMuonTrackDzCut)(void) const
) :
	HttValidMuonsProducer(validMuons,
	                      invalidMuons,
	                      GetMuonID,
	                      GetMuonIsoType,
	                      GetMuonIso,
	                      GetLowerPtCuts,
	                      GetUpperAbsEtaCuts,
	                      GetMuonChargedIsoVetoConeSize,
	                      GetMuonNeutralIsoVetoConeSize,
	                      GetMuonPhotonIsoVetoConeSize,
	                      GetMuonDeltaBetaIsoVetoConeSize,
	                      GetMuonChargedIsoPtThreshold,
	                      GetMuonNeutralIsoPtThreshold,
	                      GetMuonPhotonIsoPtThreshold,
	                      GetMuonDeltaBetaIsoPtThreshold,
	                      GetMuonIsoSignalConeSize,
	                      GetMuonDeltaBetaCorrectionFactor,
	                      GetMuonIsoPtSumOverPtThresholdEB,
	                      GetMuonIsoPtSumOverPtThresholdEE,
	                      GetMuonTrackDxyCut,
	                      GetMuonTrackDzCut)
{
}

