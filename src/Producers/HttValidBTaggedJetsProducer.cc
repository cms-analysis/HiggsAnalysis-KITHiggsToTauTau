
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/HttValidBTaggedJetsProducer.h"


void HttValidBTaggedJetsProducer::InitGlobal(global_setting_type const& globalSettings)
	{
		HttValidTaggedJetsProducer::InitGlobal(globalSettings);

		combinedSecondaryVertexMediumWP = globalSettings.GetBTaggedJetCombinedSecondaryVertexMediumWP();
		absEtaCut = globalSettings.GetBTaggedJetAbsEtaCut();
	}

void HttValidBTaggedJetsProducer::InitLocal(setting_type const& settings)
	{
		HttValidTaggedJetsProducer::InitLocal(settings);

		combinedSecondaryVertexMediumWP = settings.GetBTaggedJetCombinedSecondaryVertexMediumWP();
		absEtaCut = settings.GetBTaggedJetAbsEtaCut();
	}

void HttValidBTaggedJetsProducer::Produce(event_type const& event, product_type& product) const
{
	for (std::vector<KDataPFJet*>::iterator jet = product.m_validJets.begin();
		     jet != product.m_validJets.end(); ++jet)
		{
			bool validBJet = true;

			float combinedSecondaryVertex = static_cast<KDataPFTaggedJet*>(*jet)->getTagger("CombinedSecondaryVertexBJetTags", event.m_taggermetadata);

			if (combinedSecondaryVertex < combinedSecondaryVertexMediumWP ||
			    std::abs(static_cast<KDataPFTaggedJet*>(*jet)->p4.eta()) > absEtaCut) {
				validBJet = false;
			}

			validBJet = validBJet && HttValidBTaggedJetsProducer::AdditionalCriteria(static_cast<KDataPFTaggedJet*>(*jet), event, product);

			if (validBJet)
				product.m_validBTaggedJets.push_back(static_cast<KDataPFTaggedJet*>(*jet));
			else
				product.m_invalidBTaggedJets.push_back(static_cast<KDataPFTaggedJet*>(*jet));
		}
}

bool HttValidBTaggedJetsProducer::AdditionalCriteria(KDataPFTaggedJet* jet,
                                                     event_type const& event,
                                                     product_type& product) const
{
	bool validBJet = true;

	return validBJet;
}
