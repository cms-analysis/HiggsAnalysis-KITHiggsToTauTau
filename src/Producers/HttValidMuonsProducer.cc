
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
	isoPtSumThresholdEB = globalSettings.GetIsoPtSumThresholdEB();
	isoPtSumThresholdEE = globalSettings.GetIsoPtSumThresholdEE();
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
	isoPtSumThresholdEB = settings.GetIsoPtSumThresholdEB();
	isoPtSumThresholdEE = settings.GetIsoPtSumThresholdEE();
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
		
		if ((muon->p4.Eta() < DefaultValues::EtaBorderEB && isolationPtSum > isoPtSumThresholdEB) ||
		    (muon->p4.Eta() >= DefaultValues::EtaBorderEB && isolationPtSum > isoPtSumThresholdEE)) {
			validMuon = false;
		}
	}

	if (validMuon) {
		product.m_isoValueMuons.push_back(isolationPtSum);
	}

	return validMuon;
}

