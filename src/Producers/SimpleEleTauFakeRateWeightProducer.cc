
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/SimpleEleTauFakeRateWeightProducer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Utility/GeneratorInfo.h"

std::string SimpleEleTauFakeRateWeightProducer::GetProducerId() const
{
	return "SimpleEleTauFakeRateWeightProducer";
}

void SimpleEleTauFakeRateWeightProducer::Produce(event_type const& event, product_type& product,
                                                 setting_type const& settings) const
{
	
    float eTauFakeRateWeight = 1.0;
    if (product.m_decayChannel == HttEnumTypes::DecayChannel::ET)
    {
        KLepton* lepton = product.m_flavourOrderedLeptons[1];
        KGenParticle* genParticle = GeneratorInfo::GetGenMatchedParticle(lepton, product.m_genParticleMatchedLeptons, product.m_genTauMatchedTaus);

        if (genParticle && ((GeneratorInfo::GetGenMatchingCode(genParticle) == HttEnumTypes::GenMatchingCode::IS_ELE_PROMPT) || (GeneratorInfo::GetGenMatchingCode(genParticle) == HttEnumTypes::GenMatchingCode::IS_ELE_FROM_TAU)))
        {
            if(std::abs(lepton->p4.Eta()) < 1.5)
            {
                eTauFakeRateWeight = 1.8;
            }
            else
            {
                eTauFakeRateWeight = 1.3;
            }
        }
    }
    else if (product.m_decayChannel == HttEnumTypes::DecayChannel::MT)
    {
        KLepton* lepton = product.m_flavourOrderedLeptons[1];
        KGenParticle* genParticle = GeneratorInfo::GetGenMatchedParticle(lepton, product.m_genParticleMatchedLeptons, product.m_genTauMatchedTaus);

        if (genParticle && ((GeneratorInfo::GetGenMatchingCode(genParticle) == HttEnumTypes::GenMatchingCode::IS_ELE_PROMPT) || (GeneratorInfo::GetGenMatchingCode(genParticle) == HttEnumTypes::GenMatchingCode::IS_ELE_FROM_TAU)))
        {
            if(std::abs(lepton->p4.Eta()) < 1.5)
            {
                eTauFakeRateWeight = 1.02;
            }
            else
            {
                eTauFakeRateWeight = 1.11;
            }
        }
    }
    else if (product.m_decayChannel == HttEnumTypes::DecayChannel::TT)
    {
        for (int index = 0; index < 2; index++)
        {
            KLepton* lepton = product.m_flavourOrderedLeptons[index];
            KGenParticle* genParticle = GeneratorInfo::GetGenMatchedParticle(lepton, product.m_genParticleMatchedLeptons, product.m_genTauMatchedTaus);

            if (genParticle && ((GeneratorInfo::GetGenMatchingCode(genParticle) == HttEnumTypes::GenMatchingCode::IS_ELE_PROMPT) || (GeneratorInfo::GetGenMatchingCode(genParticle) == HttEnumTypes::GenMatchingCode::IS_ELE_FROM_TAU)))
            {
                if(std::abs(lepton->p4.Eta()) < 1.5)
                {
                    eTauFakeRateWeight *= 1.02;
                }
                else
                {
                    eTauFakeRateWeight *= 1.11;
                }
            }
        }
    }
    product.m_optionalWeights["eleTauFakeRateWeight"] = eTauFakeRateWeight;
	
}
