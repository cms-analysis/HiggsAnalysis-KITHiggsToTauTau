
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/HttValidJetsProducer.h"


bool HttValidJetsProducer::AdditionalCriteria(KDataPFJet* jet,
                                              event_type const& event, product_type& product,
                                              setting_type const& settings) const
{
	bool validJet = ValidJetsProducer::AdditionalCriteria(jet, event, product, settings);
	
	return validJet;
}


bool HttValidTaggedJetsProducer::AdditionalCriteria(KDataPFTaggedJet* jet,
                                                    event_type const& event, product_type& product,
                                                    setting_type const& settings) const
{
	bool validJet = ValidTaggedJetsProducer::AdditionalCriteria(jet, event, product, settings);

	return validJet;
}
