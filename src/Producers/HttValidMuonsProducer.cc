
#include "Artus/Utility/interface/DefaultValues.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/HttValidMuonsProducer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Calculations/ParticleIsolation.h"


void HttValidMuonsProducer::InitGlobal(global_setting_type const& globalSettings)
{
	ValidMuonsProducer::InitGlobal(globalSettings);
	
	chargedIsoVetoConeSizeEB = globalSettings.GetChargedIsoVetoConeSizeEB();
	chargedIsoVetoConeSizeEE = globalSettings.GetChargedIsoVetoConeSizeEE();
	neutralIsoVetoConeSize = globalSettings.GetNeutralIsoVetoConeSize();
	photonIsoVetoConeSizeEB = globalSettings.GetPhotonIsoVetoConeSizeEB();
	photonIsoVetoConeSizeEE = globalSettings.GetPhotonIsoVetoConeSizeEE();
	deltaBetaIsoVetoConeSize = globalSettings.GetDeltaBetaIsoVetoConeSize();
	
	chargedIsoPtThreshold = globalSettings.GetChargedIsoPtThreshold();
	neutralIsoPtThreshold = globalSettings.GetNeutralIsoPtThreshold();
	photonIsoPtThreshold = globalSettings.GetPhotonIsoPtThreshold();
	deltaBetaIsoPtThreshold = globalSettings.GetDeltaBetaIsoPtThreshold();
	
	isoSignalConeSize = globalSettings.GetIsoSignalConeSize();
	deltaBetaCorrectionFactor = globalSettings.GetDeltaBetaCorrectionFactor();
	isoPtSumThresholdEB = globalSettings.GetIsoPtSumThresholdEB();
	isoPtSumThresholdEE = globalSettings.GetIsoPtSumThresholdEE();
}

void HttValidMuonsProducer::InitLocal(setting_type const& settings)
{
	ValidMuonsProducer::InitLocal(settings);
	
	chargedIsoVetoConeSizeEB = settings.GetChargedIsoVetoConeSizeEB();
	chargedIsoVetoConeSizeEE = settings.GetChargedIsoVetoConeSizeEE();
	neutralIsoVetoConeSize = settings.GetNeutralIsoVetoConeSize();
	photonIsoVetoConeSizeEB = settings.GetPhotonIsoVetoConeSizeEB();
	photonIsoVetoConeSizeEE = settings.GetPhotonIsoVetoConeSizeEE();
	deltaBetaIsoVetoConeSize = settings.GetDeltaBetaIsoVetoConeSize();
	
	chargedIsoPtThreshold = settings.GetChargedIsoPtThreshold();
	neutralIsoPtThreshold = settings.GetNeutralIsoPtThreshold();
	photonIsoPtThreshold = settings.GetPhotonIsoPtThreshold();
	deltaBetaIsoPtThreshold = settings.GetDeltaBetaIsoPtThreshold();
	
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
	
	if (validMuon && muonIsoType == MuonIsoType::USER) {
		double isolationPtSum = ParticleIsolation::IsolationPtSum(
				muon->p4, event,
				isoSignalConeSize,
				deltaBetaCorrectionFactor,
				chargedIsoVetoConeSizeEB,
				chargedIsoVetoConeSizeEE,
				neutralIsoVetoConeSize,
				photonIsoVetoConeSizeEB,
				photonIsoVetoConeSizeEE,
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
	
	return validMuon;
}

