
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/HttValidTausProducer.h"


void HttValidTausProducer::InitGlobal(global_setting_type const& globalSettings)
{
	ValidTausProducer::InitGlobal(globalSettings);
}

void HttValidTausProducer::InitLocal(setting_type const& settings)
{
	ValidTausProducer::InitLocal(settings);
}

bool HttValidTausProducer::AdditionalCriteria(KDataPFTau* tau,
                                              event_type const& event,
                                              product_type& product) const
{
	bool validTau = ValidTausProducer::AdditionalCriteria(tau, event, product);
	
	return validTau;
}

