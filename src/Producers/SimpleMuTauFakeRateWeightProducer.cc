
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/SimpleMuTauFakeRateWeightProducer.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Utility/GeneratorInfo.h"

SimpleMuTauFakeRateWeightProducer::SimpleMuTauFakeRateWeightProducer(
		std::vector<float>& (setting_type::*GetSimpleMuTauFakeRateWeightLoose)(void) const,
		std::vector<float>& (setting_type::*GetSimpleMuTauFakeRateWeightTight)(void) const
):
	GetSimpleMuTauFakeRateWeightLoose(GetSimpleMuTauFakeRateWeightLoose),
	GetSimpleMuTauFakeRateWeightTight(GetSimpleMuTauFakeRateWeightTight)
{
}

SimpleMuTauFakeRateWeightProducer::SimpleMuTauFakeRateWeightProducer():
		SimpleMuTauFakeRateWeightProducer(&setting_type::GetSimpleMuTauFakeRateWeightLoose,
										  &setting_type::GetSimpleMuTauFakeRateWeightTight)
{
}

void SimpleMuTauFakeRateWeightProducer::Init(setting_type const& settings)
{
	ProducerBase<HttTypes>::Init(settings);

	SimpleMuTauFakeRateWeightLoose = (settings.*GetSimpleMuTauFakeRateWeightLoose)();
	SimpleMuTauFakeRateWeightTight = (settings.*GetSimpleMuTauFakeRateWeightTight)();
}

std::string SimpleMuTauFakeRateWeightProducer::GetProducerId() const
{
	return "SimpleMuTauFakeRateWeightProducer";
}

void SimpleMuTauFakeRateWeightProducer::Produce(event_type const& event, product_type& product,
                                                 setting_type const& settings) const
{
	
	float muTauFakeRateWeight=1.0;

	assert(SimpleMuTauFakeRateWeightLoose.size() == 5);
	assert(SimpleMuTauFakeRateWeightTight.size() == 5);

	if (product.m_decayChannel == HttEnumTypes::DecayChannel::MT)
	{
		KLepton* lepton = product.m_flavourOrderedLeptons[1];
		KGenParticle* genParticle = GeneratorInfo::GetGenMatchedParticle(lepton, product.m_genParticleMatchedLeptons, product.m_genTauMatchedTaus);
		if (genParticle && ((GeneratorInfo::GetGenMatchingCode(genParticle) == HttEnumTypes::GenMatchingCode::IS_MUON_PROMPT) || (GeneratorInfo::GetGenMatchingCode(genParticle) == HttEnumTypes::GenMatchingCode::IS_MUON_FROM_TAU)))
		{
			if(std::abs(lepton->p4.Eta()) < 0.4)
			{
				muTauFakeRateWeight = SimpleMuTauFakeRateWeightTight.at(0);
			}
			else if(std::abs(lepton->p4.Eta()) < 0.8)
			{
				muTauFakeRateWeight = SimpleMuTauFakeRateWeightTight.at(1);
			}
			else if(std::abs(lepton->p4.Eta()) < 1.2)
			{
				muTauFakeRateWeight = SimpleMuTauFakeRateWeightTight.at(2);
			}
			else if(std::abs(lepton->p4.Eta()) < 1.7)
			{
				muTauFakeRateWeight = SimpleMuTauFakeRateWeightTight.at(3);
			}
			else if(std::abs(lepton->p4.Eta()) < 2.3)
			{
				muTauFakeRateWeight = SimpleMuTauFakeRateWeightTight.at(4);
			}
		}
	}
	else if (product.m_decayChannel == HttEnumTypes::DecayChannel::ET)
	{
		KLepton* lepton = product.m_flavourOrderedLeptons[1];
		KGenParticle* genParticle = GeneratorInfo::GetGenMatchedParticle(lepton, product.m_genParticleMatchedLeptons, product.m_genTauMatchedTaus);
		if (genParticle && ((GeneratorInfo::GetGenMatchingCode(genParticle) == HttEnumTypes::GenMatchingCode::IS_MUON_PROMPT) || (GeneratorInfo::GetGenMatchingCode(genParticle) == HttEnumTypes::GenMatchingCode::IS_MUON_FROM_TAU)))
		{
			if(std::abs(lepton->p4.Eta()) < 0.4)
			{
				muTauFakeRateWeight = SimpleMuTauFakeRateWeightLoose.at(0);
			}
			else if(std::abs(lepton->p4.Eta()) < 0.8)
			{
				muTauFakeRateWeight = SimpleMuTauFakeRateWeightLoose.at(1);
			}
			else if(std::abs(lepton->p4.Eta()) < 1.2)
			{
				muTauFakeRateWeight = SimpleMuTauFakeRateWeightLoose.at(2);
			}
			else if(std::abs(lepton->p4.Eta()) < 1.7)
			{
				muTauFakeRateWeight = SimpleMuTauFakeRateWeightLoose.at(3);
			}
			else if(std::abs(lepton->p4.Eta()) < 2.3)
			{
				muTauFakeRateWeight = SimpleMuTauFakeRateWeightLoose.at(4);
			}
		}
	}
	else if (product.m_decayChannel == HttEnumTypes::DecayChannel::TT)
	{
		for (int index = 0; index < 2; index++)
		{
			KLepton* lepton = product.m_flavourOrderedLeptons[index];
			KGenParticle* genParticle = GeneratorInfo::GetGenMatchedParticle(lepton, product.m_genParticleMatchedLeptons, product.m_genTauMatchedTaus);
			if (genParticle && ((GeneratorInfo::GetGenMatchingCode(genParticle) == HttEnumTypes::GenMatchingCode::IS_MUON_PROMPT) || (GeneratorInfo::GetGenMatchingCode(genParticle) == HttEnumTypes::GenMatchingCode::IS_MUON_FROM_TAU)))
			{
				if(std::abs(lepton->p4.Eta()) < 0.4)
				{
					muTauFakeRateWeight *= SimpleMuTauFakeRateWeightLoose.at(0);
				}
				else if(std::abs(lepton->p4.Eta()) < 0.8)
				{
					muTauFakeRateWeight *= SimpleMuTauFakeRateWeightLoose.at(1);
				}
				else if(std::abs(lepton->p4.Eta()) < 1.2)
				{
					muTauFakeRateWeight *= SimpleMuTauFakeRateWeightLoose.at(2);
				}
				else if(std::abs(lepton->p4.Eta()) < 1.7)
				{
					muTauFakeRateWeight *= SimpleMuTauFakeRateWeightLoose.at(3);
				}
				else if(std::abs(lepton->p4.Eta()) < 2.3)
				{
					muTauFakeRateWeight *= SimpleMuTauFakeRateWeightLoose.at(4);
				}
			}
		}
	}
	product.m_weights["muTauFakeRateWeight"] = muTauFakeRateWeight;
	
}
