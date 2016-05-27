
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/SimpleEleTauFakeRateWeightProducer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Utility/GeneratorInfo.h"

std::string SimpleEleTauFakeRateWeightProducer::GetProducerId() const
{
	return "SimpleEleTauFakeRateWeightProducer";
}

void SimpleEleTauFakeRateWeightProducer::Produce(event_type const& event, product_type& product,
                                                 setting_type const& settings) const
{
	
	float eTauFakeRateWeight;
	KLepton* lepton = product.m_flavourOrderedLeptons[1];
	const KGenParticle* genParticle = GeneratorInfo::GetGenMatchedParticle(lepton, product.m_genParticleMatchedLeptons, product.m_genTauMatchedTaus);

	if((GeneratorInfo::GetGenMatchingCode(genParticle) == HttEnumTypes::GenMatchingCode::IS_ELE_PROMPT) || (GeneratorInfo::GetGenMatchingCode(genParticle) == HttEnumTypes::GenMatchingCode::IS_ELE_FROM_TAU))
	{
		if(lepton->p4.Eta() < 1.5)
		{
			eTauFakeRateWeight = 1.8;
		}
		else
		{
			eTauFakeRateWeight = 1.3;
		}
	}
	else
	{
		eTauFakeRateWeight = 1.0;
	}
	product.m_optionalWeights["eleTauFakeRateWeight"] = eTauFakeRateWeight;
	
}
