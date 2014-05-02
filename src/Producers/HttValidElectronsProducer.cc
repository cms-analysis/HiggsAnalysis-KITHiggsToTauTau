
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/HttValidElectronsProducer.h"


void HttValidElectronsProducer::InitGlobal(global_setting_type const& globalSettings)
{
	ValidElectronsProducer::InitGlobal(globalSettings);
}

void HttValidElectronsProducer::InitLocal(setting_type const& settings)
{
	ValidElectronsProducer::InitLocal(settings);
}

bool HttValidElectronsProducer::AdditionalCriteria(KDataElectron* electron,
                                                   event_type const& event,
                                                   product_type& product) const
{
	bool validElectron = ValidElectronsProducer::AdditionalCriteria(electron, event, product);
	
	return validElectron;
}

