
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/HttValidBTaggedJetsProducer.h"


void HttValidBTaggedJetsProducer::Produce(event_type const& event, product_type& product,
	                                      setting_type const& settings) const
{
	for (std::vector<KDataPFJet*>::iterator jet = product.m_validJets.begin();
		     jet != product.m_validJets.end(); ++jet)
		{
			bool validBJet = true;

			float combinedSecondaryVertex = static_cast<KDataPFTaggedJet*>(*jet)->getTagger("CombinedSecondaryVertexBJetTags", event.m_taggermetadata);

			if (combinedSecondaryVertex < settings.GetBTaggedJetCombinedSecondaryVertexMediumWP() ||
			    std::abs(static_cast<KDataPFTaggedJet*>(*jet)->p4.eta()) > settings.GetBTaggedJetAbsEtaCut()) {
				validBJet = false;
			}

			validBJet = validBJet && HttValidBTaggedJetsProducer::AdditionalCriteria(static_cast<KDataPFTaggedJet*>(*jet),
			                                                                         event, product, settings);

			if (validBJet)
				product.m_BTaggedJets.push_back(static_cast<KDataPFTaggedJet*>(*jet));
			else
				product.m_notBTaggedJets.push_back(static_cast<KDataPFTaggedJet*>(*jet));
		}
}

bool HttValidBTaggedJetsProducer::AdditionalCriteria(KDataPFTaggedJet* jet,
                                                     event_type const& event, product_type& product,
                                                     setting_type const& settings) const
{
	bool validBJet = true;

	return validBJet;
}
