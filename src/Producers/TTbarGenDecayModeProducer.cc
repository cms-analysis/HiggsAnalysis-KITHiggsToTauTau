#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/TTbarGenDecayModeProducer.h"

void TTbarGenDecayModeProducer::Init(setting_type const& settings, metadata_type& metadata)
{
	ProducerBase<HttTypes>::Init(settings, metadata);
	LambdaNtupleConsumer<HttTypes>::AddIntQuantity(metadata, "TTbarGenDecayMode", [this](HttTypes::event_type const& event, HttTypes::product_type const& product, HttTypes::setting_type const& settings, HttTypes::metadata_type const& metadata) {
		return product.m_TTbarGenDecayMode;
	});
}

void TTbarGenDecayModeProducer::Produce(event_type const& event, product_type& product,
                                setting_type const& settings, metadata_type const& metadata) const
{
	// meaning: 0 - unspecified, 1 - fullhadronic, 2 - fullleptonic, 3 - semileptonic
	product.m_TTbarGenDecayMode = 0;
	unsigned int top_count = 0;
	unsigned int W_count = 0;
	unsigned int n_quarks = 0;
	unsigned int n_leptons = 0;
	for (unsigned int i=0; i<event.m_genParticles->size(); ++i)
	{
		if(abs(event.m_genParticles->at(i).pdgId) == 6 && event.m_genParticles->at(i).status() == 62)
		{
			top_count++;
		}
	}

	for (unsigned int i=0; i<event.m_genParticles->size(); ++i)
	{
		if(abs(event.m_genParticles->at(i).pdgId) == 24)
		{
			W_count++;
			KGenParticle* W = &(event.m_genParticles->at(i));
			for (unsigned int j=0; j<W->daughterIndices.size();j++)
			{
				if(abs(event.m_genParticles->at(W->daughterIndices.at(j)).pdgId) < 7 && abs(event.m_genParticles->at(W->daughterIndices.at(j)).pdgId) > 0)
				{
					n_quarks++;
				}
				else if(abs(event.m_genParticles->at(W->daughterIndices.at(j)).pdgId) < 17 && abs(event.m_genParticles->at(W->daughterIndices.at(j)).pdgId) > 10)
				{
					n_leptons++;
				}
			}
		}
	}

	if(top_count == 2)
	{
		if(n_quarks == 4 && n_leptons == 0) product.m_TTbarGenDecayMode = 1;
		else if(n_quarks == 0 && n_leptons == 4) product.m_TTbarGenDecayMode = 2;
		else if(n_quarks == 2 && n_leptons == 2) product.m_TTbarGenDecayMode = 3;
	}

	if(product.m_TTbarGenDecayMode == 0)
	{
	std::cout << std::endl << "Number of tops: " << top_count << std::endl;
	std::cout << "Number of W's: " << W_count << std::endl;
	std::cout << "Number of quarks from W's: " << n_quarks << std::endl;
	std::cout << "Number of leptons from W's: " << n_leptons << std::endl;
	}
}
