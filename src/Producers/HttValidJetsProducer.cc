
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/HttValidJetsProducer.h"


bool HttValidJetsProducer::AdditionalCriteria(KDataPFJet* jet,
                                              event_type const& event, product_type& product,
                                              setting_type const& settings) const
{
	bool validJet = ValidJetsProducer<HttTypes>::AdditionalCriteria(jet, event, product, settings);
	
	return validJet;
}


bool HttValidTaggedJetsProducer::AdditionalCriteria(KDataPFTaggedJet* jet,
                                                    event_type const& event, product_type& product,
                                                    setting_type const& settings) const
{
	bool validJet = ValidTaggedJetsProducer::AdditionalCriteria(jet, event, product, settings);

	// TODO: implement actual preselection (possibly channel-dependent)
	// the cuts below are just a temporary example to test the code
	validJet = validJet && jet->p4.pt() > 50.
                            && std::abs(jet->p4.eta()) < 4.;

	return validJet;
}
