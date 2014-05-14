
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
	isoPtSumOverPtThresholdEB = globalSettings.GetIsoPtSumOverPtThresholdEB();
	isoPtSumOverPtThresholdEE = globalSettings.GetIsoPtSumOverPtThresholdEE();
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
	isoPtSumOverPtThresholdEB = settings.GetIsoPtSumOverPtThresholdEB();
	isoPtSumOverPtThresholdEE = settings.GetIsoPtSumOverPtThresholdEE();
}

bool HttValidElectronsProducer::AdditionalCriteria(KDataElectron* electron,
                                                   event_type const& event,
                                                   product_type& product) const
{
	bool validElectron = ValidElectronsProducer::AdditionalCriteria(electron, event, product);
	double isolationPtSum = DefaultValues::UndefinedDouble;

	if (validElectron && electronIsoType == ElectronIsoType::USER) {
		isolationPtSum = ParticleIsolation::IsolationPtSum(
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
		
		double isolationPtSumOverPt = isolationPtSum / electron->p4.Pt();
		
		if ((electron->p4.Eta() < DefaultValues::EtaBorderEB && isolationPtSumOverPt > isoPtSumOverPtThresholdEB) ||
		    (electron->p4.Eta() >= DefaultValues::EtaBorderEB && isolationPtSumOverPt > isoPtSumOverPtThresholdEE)) {
			validElectron = false;
		}
	}

	if (validElectron) {
		product.m_isoValueElectrons.push_back(isolationPtSum);
	}

	return validElectron;
}

