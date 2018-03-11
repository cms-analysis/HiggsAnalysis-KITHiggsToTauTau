
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/HttValidJetsProducer.h"


bool HttValidJetsProducer::AdditionalCriteria(KBasicJet* jet,
                                              event_type const& event, product_type& product,
                                              setting_type const& settings, metadata_type const& metadata) const
{
	return HttValidJetsProducer::AdditionalCriteriaStatic(jet, event, product, settings, metadata);
}

bool HttValidJetsProducer::AdditionalCriteriaStatic(KBasicJet* jet,
                                                    event_type const& event, product_type& product,
                                                    setting_type const& settings, metadata_type const& metadata)
{
	bool validJet = ValidJetsProducer::AdditionalCriteriaStatic(jet, event, product, settings, metadata);
	
	return validJet;
}


bool HttValidTaggedJetsProducer::AdditionalCriteria(KJet* jet,
                                                    event_type const& event, product_type& product,
                                                    setting_type const& settings, metadata_type const& metadata) const
{
	return HttValidTaggedJetsProducer::AdditionalCriteriaStatic(jet,
	                                                            puJetIdsByIndex, puJetIdsByHltName,
	                                                            jetTaggerLowerCutsByTaggerName, jetTaggerUpperCutsByTaggerName,
	                                                            event, product, settings, metadata);
}

bool HttValidTaggedJetsProducer::AdditionalCriteriaStatic(KJet* jet,
	                                                      std::map<size_t, std::vector<std::string> > const& puJetIdsByIndex,
	                                                      std::map<std::string, std::vector<std::string> > const& puJetIdsByHltName,
	                                                      std::map<std::string, std::vector<float> > const& jetTaggerLowerCutsByTaggerName,
	                                                      std::map<std::string, std::vector<float> > const& jetTaggerUpperCutsByTaggerName,
	                                                      event_type const& event, product_type& product,
	                                                      setting_type const& settings, metadata_type const& metadata)
{
	bool validJet = ValidTaggedJetsProducer::AdditionalCriteriaStatic(jet,
	                                                                  puJetIdsByIndex, puJetIdsByHltName,
	                                                                  jetTaggerLowerCutsByTaggerName, jetTaggerUpperCutsByTaggerName,
	                                                                  event, product, settings, metadata);
	
	spec_setting_type const& specSettings = static_cast<spec_setting_type const&>(settings);
	spec_product_type const& specProduct = static_cast<spec_product_type const&>(product);
	
	// remove taus from list of jets via simple DeltaR isolation
	// (targeted at ttH analysis, harmless if m_validTTHTaus is not filled)
	for (std::vector<KTau*>::const_iterator tau = specProduct.m_validTTHTaus.begin();
	validJet && tau != specProduct.m_validTTHTaus.end(); ++tau)
	{
		validJet = validJet && ROOT::Math::VectorUtil::DeltaR(jet->p4, (*tau)->p4) > specSettings.GetJetTauLowerDeltaRCut();
	}

	return validJet;
}
