
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/HttValidMuonsProducer.h"


void HttValidMuonsProducer::InitGlobal(global_setting_type const& globalSettings)
{
	ValidMuonsProducer::InitGlobal(globalSettings);
}

void HttValidMuonsProducer::InitLocal(setting_type const& settings)
{
	ValidMuonsProducer::InitLocal(settings);
}

bool HttValidMuonsProducer::AdditionalCriteria(KDataMuon* muon,
                                                   event_type const& event,
                                                   product_type& product) const
{
	bool validMuon = ValidMuonsProducer::AdditionalCriteria(muon, event, product);
	
	return validMuon;
}

