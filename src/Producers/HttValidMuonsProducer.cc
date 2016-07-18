
#include "Artus/Utility/interface/DefaultValues.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/HttValidMuonsProducer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Utility/ParticleIsolation.h"


HttValidMuonsProducer::HttValidMuonsProducer(std::vector<KMuon*> product_type::*validMuons,
                                             std::vector<KMuon*> product_type::*invalidMuons,
                                             std::string (setting_type::*GetMuonID)(void) const,
                                             std::string (setting_type::*GetMuonIsoType)(void) const,
                                             std::string (setting_type::*GetMuonIsoTypeUserMode)(void) const,
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
                                             float (setting_type::*GetMuonIsoPtSumOverPtLowerThresholdEB)(void) const,
                                             float (setting_type::*GetMuonIsoPtSumOverPtLowerThresholdEE)(void) const,
                                             float (setting_type::*GetMuonIsoPtSumOverPtUpperThresholdEB)(void) const,
                                             float (setting_type::*GetMuonIsoPtSumOverPtUpperThresholdEE)(void) const,
                                             float (setting_type::*GetMuonTrackDxyCut)(void) const,
                                             float (setting_type::*GetMuonTrackDzCut)(void) const)
                                              :
	ValidMuonsProducer(validMuons, invalidMuons,
	                   GetMuonID, GetMuonIsoType, GetMuonIso,
	                   GetLowerPtCuts, GetUpperAbsEtaCuts),
    GetMuonIsoTypeUserMode(GetMuonIsoTypeUserMode),
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
	GetMuonIsoPtSumOverPtLowerThresholdEB(GetMuonIsoPtSumOverPtLowerThresholdEB),
	GetMuonIsoPtSumOverPtLowerThresholdEE(GetMuonIsoPtSumOverPtLowerThresholdEE),
	GetMuonIsoPtSumOverPtUpperThresholdEB(GetMuonIsoPtSumOverPtUpperThresholdEB),
	GetMuonIsoPtSumOverPtUpperThresholdEE(GetMuonIsoPtSumOverPtUpperThresholdEE),
	GetMuonTrackDxyCut(GetMuonTrackDxyCut),
	GetMuonTrackDzCut(GetMuonTrackDzCut)
{
}


bool HttValidMuonsProducer::AdditionalCriteria(KMuon* muon,
                                               event_type const& event, product_type& product,
                                               setting_type const& settings) const
{
	bool validMuon = ValidMuonsProducer<HttTypes>::AdditionalCriteria(muon, event, product, settings);

	double chargedIsolationPtSum = DefaultValues::UndefinedDouble;
	double neutralIsolationPtSum = DefaultValues::UndefinedDouble;
	double photonIsolationPtSum = DefaultValues::UndefinedDouble;
	double deltaBetaIsolationPtSum = DefaultValues::UndefinedDouble;

	double isolationPtSum = DefaultValues::UndefinedDouble;

	if (muonIsoTypeUserMode == MuonIsoTypeUserMode::FROMCMSSW)
	{
		chargedIsolationPtSum = muon->sumChargedHadronPt;
		neutralIsolationPtSum = muon->sumNeutralHadronEt;
		photonIsolationPtSum = muon->sumPhotonEt;
		deltaBetaIsolationPtSum = muon->sumPUPt;

		isolationPtSum = muon->pfIso((settings.*GetMuonDeltaBetaCorrectionFactor)());
	}
	else if (muonIsoTypeUserMode == MuonIsoTypeUserMode::FROMCMSSWR04)
	{
		chargedIsolationPtSum = muon->sumChargedHadronPtR04;
		neutralIsolationPtSum = muon->sumNeutralHadronEtR04;
		photonIsolationPtSum = muon->sumPhotonEtR04;
		deltaBetaIsolationPtSum = muon->sumPUPtR04;

		isolationPtSum = muon->pfIso((settings.*GetMuonDeltaBetaCorrectionFactor)());
	}
	else if (muonIsoTypeUserMode == MuonIsoTypeUserMode::CALCULATED)
	{
		chargedIsolationPtSum = ParticleIsolation::IsolationPtSumForParticleClass(
				muon->p4,
				event.m_pfChargedHadronsNoPileUp,
				(settings.*GetMuonIsoSignalConeSize)(),
				(settings.*GetMuonChargedIsoVetoConeSize)(),
				(settings.*GetMuonChargedIsoVetoConeSize)(),
				(settings.*GetMuonChargedIsoPtThreshold)()
		);
		neutralIsolationPtSum = ParticleIsolation::IsolationPtSumForParticleClass(
				muon->p4,
				event.m_pfNeutralHadronsNoPileUp,
				(settings.*GetMuonIsoSignalConeSize)(),
				(settings.*GetMuonNeutralIsoVetoConeSize)(),
				(settings.*GetMuonNeutralIsoVetoConeSize)(),
				(settings.*GetMuonNeutralIsoPtThreshold)()
		);
		photonIsolationPtSum = ParticleIsolation::IsolationPtSumForParticleClass(
				muon->p4,
				event.m_pfPhotonsNoPileUp,
				(settings.*GetMuonIsoSignalConeSize)(),
				(settings.*GetMuonPhotonIsoVetoConeSize)(),
				(settings.*GetMuonPhotonIsoVetoConeSize)(),
				(settings.*GetMuonPhotonIsoPtThreshold)()
		);
		deltaBetaIsolationPtSum = ParticleIsolation::IsolationPtSumForParticleClass(
				muon->p4,
				event.m_pfChargedHadronsPileUp,
				(settings.*GetMuonIsoSignalConeSize)(),
				(settings.*GetMuonDeltaBetaIsoVetoConeSize)(),
				(settings.*GetMuonDeltaBetaIsoVetoConeSize)(),
				(settings.*GetMuonDeltaBetaIsoPtThreshold)()
		);

		isolationPtSum = chargedIsolationPtSum + std::max(0.0,neutralIsolationPtSum + photonIsolationPtSum - (settings.*GetMuonDeltaBetaCorrectionFactor)() * deltaBetaIsolationPtSum);

	}

	product.m_leptonIsolation[muon] = isolationPtSum;
	product.m_muonIsolation[muon] = isolationPtSum;

	product.m_muonChargedIsolation[muon] = chargedIsolationPtSum;
	product.m_muonNeutralIsolation[muon] = neutralIsolationPtSum;
	product.m_muonPhotonIsolation[muon] = photonIsolationPtSum;
	product.m_muonDeltaBetaIsolation[muon] = deltaBetaIsolationPtSum;

	double isolationPtSumOverPt = isolationPtSum / muon->p4.Pt();

	product.m_leptonIsolationOverPt[muon] = isolationPtSumOverPt;
	product.m_muonIsolationOverPt[muon] = isolationPtSumOverPt;

	product.m_muonChargedIsolationOverPt[muon] = chargedIsolationPtSum / muon->p4.Pt();
	product.m_muonNeutralIsolationOverPt[muon] = neutralIsolationPtSum / muon->p4.Pt();
	product.m_muonPhotonIsolationOverPt[muon] = photonIsolationPtSum / muon->p4.Pt();
	product.m_muonDeltaBetaIsolationOverPt[muon] = deltaBetaIsolationPtSum / muon->p4.Pt();

	if (validMuon && muonIsoType == MuonIsoType::USER) {

		if (std::abs(muon->p4.Eta()) < DefaultValues::EtaBorderEB)
		{
			if ((isolationPtSumOverPt > (settings.*GetMuonIsoPtSumOverPtLowerThresholdEB)()) &&
			    (isolationPtSumOverPt < (settings.*GetMuonIsoPtSumOverPtUpperThresholdEB)()))
			{
				validMuon = settings.GetDirectIso();
			}
			else
			{
				validMuon = (! settings.GetDirectIso());
			}
		}
		else
		{
			if ((isolationPtSumOverPt > (settings.*GetMuonIsoPtSumOverPtLowerThresholdEE)()) &&
			    (isolationPtSumOverPt < (settings.*GetMuonIsoPtSumOverPtUpperThresholdEE)()))
			{
				validMuon = settings.GetDirectIso();
			}
			else
			{
				validMuon = (! settings.GetDirectIso());
			}
		}
	}
	
	// (tighter) cut on impact parameters of track
	validMuon = validMuon
	            && ((settings.*GetMuonTrackDxyCut)() <= 0.0 || std::abs(muon->dxy) < (settings.*GetMuonTrackDxyCut)())
	            && ((settings.*GetMuonTrackDzCut)() <= 0.0 || std::abs(muon->dz) < (settings.*GetMuonTrackDzCut)());

	return validMuon;
}


HttValidLooseMuonsProducer::HttValidLooseMuonsProducer(
		std::vector<KMuon*> product_type::*validMuons,
		std::vector<KMuon*> product_type::*invalidMuons,
		std::string (setting_type::*GetMuonID)(void) const,
		std::string (setting_type::*GetMuonIsoType)(void) const,
		std::string (setting_type::*GetMuonIsoTypeUserMode)(void) const,
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
		float (setting_type::*GetMuonIsoPtSumOverPtLowerThresholdEB)(void) const,
		float (setting_type::*GetMuonIsoPtSumOverPtLowerThresholdEE)(void) const,
		float (setting_type::*GetMuonIsoPtSumOverPtUpperThresholdEB)(void) const,
		float (setting_type::*GetMuonIsoPtSumOverPtUpperThresholdEE)(void) const,
		float (setting_type::*GetMuonTrackDxyCut)(void) const,
		float (setting_type::*GetMuonTrackDzCut)(void) const
) :
	HttValidMuonsProducer(validMuons,
	                      invalidMuons,
	                      GetMuonID,
	                      GetMuonIsoType,
	                      GetMuonIsoTypeUserMode,
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
	                      GetMuonIsoPtSumOverPtLowerThresholdEB,
	                      GetMuonIsoPtSumOverPtLowerThresholdEE,
	                      GetMuonIsoPtSumOverPtUpperThresholdEB,
	                      GetMuonIsoPtSumOverPtUpperThresholdEE,
	                      GetMuonTrackDxyCut,
	                      GetMuonTrackDzCut)
{
}


HttValidVetoMuonsProducer::HttValidVetoMuonsProducer(
		std::vector<KMuon*> product_type::*validMuons,
		std::vector<KMuon*> product_type::*invalidMuons,
		std::string (setting_type::*GetMuonID)(void) const,
		std::string (setting_type::*GetMuonIsoType)(void) const,
		std::string (setting_type::*GetMuonIsoTypeUserMode)(void) const,
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
		float (setting_type::*GetMuonIsoPtSumOverPtLowerThresholdEB)(void) const,
		float (setting_type::*GetMuonIsoPtSumOverPtLowerThresholdEE)(void) const,
		float (setting_type::*GetMuonIsoPtSumOverPtUpperThresholdEB)(void) const,
		float (setting_type::*GetMuonIsoPtSumOverPtUpperThresholdEE)(void) const,
		float (setting_type::*GetMuonTrackDxyCut)(void) const,
		float (setting_type::*GetMuonTrackDzCut)(void) const
) :
	HttValidMuonsProducer(validMuons,
	                      invalidMuons,
	                      GetMuonID,
	                      GetMuonIsoType,
	                      GetMuonIsoTypeUserMode,
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
	                      GetMuonIsoPtSumOverPtLowerThresholdEB,
	                      GetMuonIsoPtSumOverPtLowerThresholdEE,
	                      GetMuonIsoPtSumOverPtUpperThresholdEB,
	                      GetMuonIsoPtSumOverPtUpperThresholdEE,
	                      GetMuonTrackDxyCut,
	                      GetMuonTrackDzCut)
{
}

