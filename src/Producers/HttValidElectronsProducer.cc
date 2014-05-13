
#include "Artus/Utility/interface/DefaultValues.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/HttValidElectronsProducer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Calculations/ParticleIsolation.h"


void HttValidElectronsProducer::InitGlobal(global_setting_type const& globalSettings)
{
	ValidElectronsProducer::InitGlobal(globalSettings);
	
	chargedIsoVetoConeSizeEB = globalSettings.GetElectronChargedIsoVetoConeSizeEB();
	chargedIsoVetoConeSizeEE = globalSettings.GetElectronChargedIsoVetoConeSizeEE();
	neutralIsoVetoConeSize = globalSettings.GetElectronNeutralIsoVetoConeSize();
	photonIsoVetoConeSizeEB = globalSettings.GetElectronPhotonIsoVetoConeSizeEB();
	photonIsoVetoConeSizeEE = globalSettings.GetElectronPhotonIsoVetoConeSizeEE();
	deltaBetaIsoVetoConeSize = globalSettings.GetElectronDeltaBetaIsoVetoConeSize();
	
	chargedIsoPtThreshold = globalSettings.GetElectronChargedIsoPtThreshold();
	neutralIsoPtThreshold = globalSettings.GetElectronNeutralIsoPtThreshold();
	photonIsoPtThreshold = globalSettings.GetElectronPhotonIsoPtThreshold();
	deltaBetaIsoPtThreshold = globalSettings.GetElectronDeltaBetaIsoPtThreshold();
	
	isoSignalConeSize = globalSettings.GetIsoSignalConeSize();
	deltaBetaCorrectionFactor = globalSettings.GetDeltaBetaCorrectionFactor();
	isoPtSumThresholdEB = globalSettings.GetIsoPtSumThresholdEB();
	isoPtSumThresholdEE = globalSettings.GetIsoPtSumThresholdEE();
}

void HttValidElectronsProducer::InitLocal(setting_type const& settings)
{
	ValidElectronsProducer::InitLocal(settings);
	
	chargedIsoVetoConeSizeEB = settings.GetElectronChargedIsoVetoConeSizeEB();
	chargedIsoVetoConeSizeEE = settings.GetElectronChargedIsoVetoConeSizeEE();
	neutralIsoVetoConeSize = settings.GetElectronNeutralIsoVetoConeSize();
	photonIsoVetoConeSizeEB = settings.GetElectronPhotonIsoVetoConeSizeEB();
	photonIsoVetoConeSizeEE = settings.GetElectronPhotonIsoVetoConeSizeEE();
	deltaBetaIsoVetoConeSize = settings.GetElectronDeltaBetaIsoVetoConeSize();
	
	chargedIsoPtThreshold = settings.GetElectronChargedIsoPtThreshold();
	neutralIsoPtThreshold = settings.GetElectronNeutralIsoPtThreshold();
	photonIsoPtThreshold = settings.GetElectronPhotonIsoPtThreshold();
	deltaBetaIsoPtThreshold = settings.GetElectronDeltaBetaIsoPtThreshold();
	
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

