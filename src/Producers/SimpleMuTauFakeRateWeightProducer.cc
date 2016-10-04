
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/SimpleMuTauFakeRateWeightProducer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Utility/GeneratorInfo.h"

std::string SimpleMuTauFakeRateWeightProducer::GetProducerId() const
{
	return "SimpleMuTauFakeRateWeightProducer";
}

void SimpleMuTauFakeRateWeightProducer::Produce(event_type const& event, product_type& product,
                                                 setting_type const& settings) const
{
	
    float muTauFakeRateWeight=1.0;

    if (product.m_decayChannel == HttEnumTypes::DecayChannel::MT)
    {
        KLepton* lepton = product.m_flavourOrderedLeptons[1];
        const KGenParticle* genParticle = GeneratorInfo::GetGenMatchedParticle(lepton, product.m_genParticleMatchedLeptons, product.m_genTauMatchedTaus);
        if (genParticle && ((GeneratorInfo::GetGenMatchingCode(genParticle) == HttEnumTypes::GenMatchingCode::IS_MUON_PROMPT) || (GeneratorInfo::GetGenMatchingCode(genParticle) == HttEnumTypes::GenMatchingCode::IS_MUON_FROM_TAU)))
        {
            if(std::abs(lepton->p4.Eta()) < 0.4)
            {
                muTauFakeRateWeight = 1.5;
            }
            else if(std::abs(lepton->p4.Eta()) < 0.8)
            {
                muTauFakeRateWeight = 1.4;
            }
            else if(std::abs(lepton->p4.Eta()) < 1.2)
            {
                muTauFakeRateWeight = 1.21;
            }
            else if(std::abs(lepton->p4.Eta()) < 1.7)
            {
                muTauFakeRateWeight = 2.6;
            }
            else if(std::abs(lepton->p4.Eta()) < 2.3)
            {
                muTauFakeRateWeight = 2.1;
            }
        }
    }
    else if (product.m_decayChannel == HttEnumTypes::DecayChannel::ET)
    {
        KLepton* lepton = product.m_flavourOrderedLeptons[1];
        const KGenParticle* genParticle = GeneratorInfo::GetGenMatchedParticle(lepton, product.m_genParticleMatchedLeptons, product.m_genTauMatchedTaus);
        if (genParticle && ((GeneratorInfo::GetGenMatchingCode(genParticle) == HttEnumTypes::GenMatchingCode::IS_MUON_PROMPT) || (GeneratorInfo::GetGenMatchingCode(genParticle) == HttEnumTypes::GenMatchingCode::IS_MUON_FROM_TAU)))
        {
            if(std::abs(lepton->p4.Eta()) < 0.4)
            {
                muTauFakeRateWeight = 1.15;
            }
            else if(std::abs(lepton->p4.Eta()) < 0.8)
            {
                muTauFakeRateWeight = 1.15;
            }
            else if(std::abs(lepton->p4.Eta()) < 1.2)
            {
                muTauFakeRateWeight = 1.18;
            }
            else if(std::abs(lepton->p4.Eta()) < 1.7)
            {
                muTauFakeRateWeight = 1.2;
            }
            else if(std::abs(lepton->p4.Eta()) < 2.3)
            {
                muTauFakeRateWeight = 1.3;
            }
        }
    }
    else if (product.m_decayChannel == HttEnumTypes::DecayChannel::TT)
    {
        for (int index = 0; index < 2; index++)
        {
            KLepton* lepton = product.m_flavourOrderedLeptons[index];
            const KGenParticle* genParticle = GeneratorInfo::GetGenMatchedParticle(lepton, product.m_genParticleMatchedLeptons, product.m_genTauMatchedTaus);
            if (genParticle && ((GeneratorInfo::GetGenMatchingCode(genParticle) == HttEnumTypes::GenMatchingCode::IS_MUON_PROMPT) || (GeneratorInfo::GetGenMatchingCode(genParticle) == HttEnumTypes::GenMatchingCode::IS_MUON_FROM_TAU)))
            {
                if(std::abs(lepton->p4.Eta()) < 0.4)
                {
                    muTauFakeRateWeight *= 1.15;
                }
                else if(std::abs(lepton->p4.Eta()) < 0.8)
                {
                    muTauFakeRateWeight *= 1.15;
                }
                else if(std::abs(lepton->p4.Eta()) < 1.2)
                {
                    muTauFakeRateWeight *= 1.18;
                }
                else if(std::abs(lepton->p4.Eta()) < 1.7)
                {
                    muTauFakeRateWeight *= 1.2;
                }
                else if(std::abs(lepton->p4.Eta()) < 2.3)
                {
                    muTauFakeRateWeight *= 1.3;
                }
            }
        }
    }
	product.m_optionalWeights["muTauFakeRateWeight"] = muTauFakeRateWeight;
	
}
