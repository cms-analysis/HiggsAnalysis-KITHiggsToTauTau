
#include "Artus/Utility/interface/DefaultValues.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/HttValidElectronsProducer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Calculations/ParticleIsolation.h"


void HttValidElectronsProducer::InitGlobal(global_setting_type const& globalSettings)
{
	ValidElectronsProducer::InitGlobal(globalSettings);
	
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

void HttValidElectronsProducer::InitLocal(setting_type const& settings)
{
	ValidElectronsProducer::InitLocal(settings);
	
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

bool HttValidElectronsProducer::AdditionalCriteria(KDataElectron* electron,
                                                   event_type const& event,
                                                   product_type& product) const
{
	bool validElectron = ValidElectronsProducer::AdditionalCriteria(electron, event, product);
	
	if (validElectron && electronIsoType == ElectronIsoType::USER) {
		double isolationPtSum = ParticleIsolation::IsolationPtSum(
				electron->p4, event,
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
		
		if ((electron->p4.Eta() < DefaultValues::EtaBorderEB && isolationPtSum > isoPtSumThresholdEB) ||
		    (electron->p4.Eta() >= DefaultValues::EtaBorderEB && isolationPtSum > isoPtSumThresholdEE)) {
			validElectron = false;
		}
	}
	
	return validElectron;
}

