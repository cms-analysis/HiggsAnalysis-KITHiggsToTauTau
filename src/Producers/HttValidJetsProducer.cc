
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/HttValidJetsProducer.h"


bool HttValidJetsProducer::AdditionalCriteria(KBasicJet* jet,
                                              event_type const& event, product_type& product,
                                              setting_type const& settings, metadata_type const& metadata) const
{
	bool validJet = ValidJetsProducer::AdditionalCriteria(jet, event, product, settings, metadata);
	
	return validJet;
}


bool HttValidTaggedJetsProducer::AdditionalCriteria(KJet* jet,
                                                    event_type const& event, product_type& product,
                                                    setting_type const& settings, metadata_type const& metadata) const
{
	bool validJet = ValidTaggedJetsProducer::AdditionalCriteria(jet, event, product, settings, metadata);
	
	HttSettings const& specSettings = static_cast<HttSettings const&>(settings);
	HttProduct const& specProduct = static_cast<HttProduct const&>(product);
	
	// remove taus from list of jets via simple DeltaR isolation
	// (targeted at ttH analysis, harmless if m_validTTHTaus is not filled)
	for (std::vector<KTau*>::const_iterator tau = specProduct.m_validTTHTaus.begin();
		validJet && tau != specProduct.m_validTTHTaus.end(); ++tau)
		{
			validJet = validJet && ROOT::Math::VectorUtil::DeltaR(jet->p4, (*tau)->p4) > specSettings.GetJetTauLowerDeltaRCut();
		}

	return validJet;
}
