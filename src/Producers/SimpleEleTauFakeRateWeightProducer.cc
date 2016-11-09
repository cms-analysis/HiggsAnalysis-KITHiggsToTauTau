
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/SimpleEleTauFakeRateWeightProducer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Utility/GeneratorInfo.h"

std::string SimpleEleTauFakeRateWeightProducer::GetProducerId() const
{
	return "SimpleEleTauFakeRateWeightProducer";
}

void SimpleEleTauFakeRateWeightProducer::Produce(event_type const& event, product_type& product,
                                                 setting_type const& settings) const
{
	// 04.11.2016: numbers taken from https://indico.cern.ch/event/563239/contributions/2279020/attachments/1325496/1989607/lepTauFR_tauIDmeeting_20160822.pdf
	//             as recommended in https://twiki.cern.ch/twiki/bin/viewauth/CMS/SMTauTau2016#e_tau_fake_rate
	
    float eTauFakeRateWeight = 1.0;
    if (product.m_decayChannel == HttEnumTypes::DecayChannel::ET)
    {
        KLepton* lepton = product.m_flavourOrderedLeptons[1];
        KGenParticle* genParticle = GeneratorInfo::GetGenMatchedParticle(lepton, product.m_genParticleMatchedLeptons, product.m_genTauMatchedTaus);

        if (genParticle && ((GeneratorInfo::GetGenMatchingCode(genParticle) == HttEnumTypes::GenMatchingCode::IS_ELE_PROMPT) || (GeneratorInfo::GetGenMatchingCode(genParticle) == HttEnumTypes::GenMatchingCode::IS_ELE_FROM_TAU)))
        {
            if(std::abs(lepton->p4.Eta()) < 1.460)
            {
                eTauFakeRateWeight = 1.505;
            }
            else if(std::abs(lepton->p4.Eta()) > 1.558)
            {
                eTauFakeRateWeight = 1.994;
            }
        }
    }
    else if (product.m_decayChannel == HttEnumTypes::DecayChannel::MT)
    {
        KLepton* lepton = product.m_flavourOrderedLeptons[1];
        KGenParticle* genParticle = GeneratorInfo::GetGenMatchedParticle(lepton, product.m_genParticleMatchedLeptons, product.m_genTauMatchedTaus);

        if (genParticle && ((GeneratorInfo::GetGenMatchingCode(genParticle) == HttEnumTypes::GenMatchingCode::IS_ELE_PROMPT) || (GeneratorInfo::GetGenMatchingCode(genParticle) == HttEnumTypes::GenMatchingCode::IS_ELE_FROM_TAU)))
        {
            if(std::abs(lepton->p4.Eta()) < 1.460)
            {
                eTauFakeRateWeight = 1.292;
            }
            else if(std::abs(lepton->p4.Eta()) > 1.558)
            {
                eTauFakeRateWeight = 1.536;
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
                if(std::abs(lepton->p4.Eta()) < 1.460)
                {
                    eTauFakeRateWeight *= 1.292;
                }
                else if(std::abs(lepton->p4.Eta()) > 1.558)
                {
                    eTauFakeRateWeight *= 1.536;
                }
            }
        }
    }
    product.m_optionalWeights["eleTauFakeRateWeight"] = eTauFakeRateWeight;
	
}
