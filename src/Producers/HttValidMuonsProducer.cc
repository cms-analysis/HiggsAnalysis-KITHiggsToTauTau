
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/HttValidMuonsProducer.h"


void HttValidMuonsProducer::InitGlobal(global_setting_type const& globalSettings)
{
	ValidMuonsProducer::InitGlobal(globalSettings);
	
	decayChannel = HttProduct::ToDecayChannel(globalSettings.GetChannel());
}

void HttValidMuonsProducer::InitLocal(setting_type const& settings)
{
	ValidMuonsProducer::InitLocal(settings);
	
	decayChannel = HttProduct::ToDecayChannel(settings.GetChannel());
}

bool HttValidMuonsProducer::AdditionalCriteria(KDataMuon* muon,
                                               event_type const& event,
                                               product_type& product) const
{
	bool validMuon = ValidMuonsProducer::AdditionalCriteria(muon, event, product);
	
	return validMuon;
}

