
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/SimpleMuTauFakeRateWeightProducer.h"
#include "Artus/KappaAnalysis/interface/Utility/GeneratorInfo.h"

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
		KappaEnumTypes::GenMatchingCode genMatchingCode = KappaEnumTypes::GenMatchingCode::NONE;
		KLepton* originalLepton = product.m_originalLeptons.find(product.m_flavourOrderedLeptons[1]) != product.m_originalLeptons.end() ? const_cast<KLepton*>(product.m_originalLeptons.at(product.m_flavourOrderedLeptons[1])) : product.m_flavourOrderedLeptons[1];
		if (settings.GetUseUWGenMatching())
		{
			genMatchingCode = GeneratorInfo::GetGenMatchingCodeUW(event, originalLepton);
		}
		else
		{
			KGenParticle* genParticle = GeneratorInfo::GetGenMatchedParticle(originalLepton, product.m_genParticleMatchedLeptons, product.m_genTauMatchedLeptons);
			if (genParticle)
				genMatchingCode = GeneratorInfo::GetGenMatchingCode(genParticle);
			else
				genMatchingCode = KappaEnumTypes::GenMatchingCode::IS_FAKE;
		}
		KLepton* lepton = product.m_flavourOrderedLeptons[1];
		if ((genMatchingCode == KappaEnumTypes::GenMatchingCode::IS_MUON_PROMPT) || (genMatchingCode == KappaEnumTypes::GenMatchingCode::IS_MUON_FROM_TAU))
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
		KappaEnumTypes::GenMatchingCode genMatchingCode = KappaEnumTypes::GenMatchingCode::NONE;
		KLepton* originalLepton = product.m_originalLeptons.find(product.m_flavourOrderedLeptons[1]) != product.m_originalLeptons.end() ? const_cast<KLepton*>(product.m_originalLeptons.at(product.m_flavourOrderedLeptons[1])) : product.m_flavourOrderedLeptons[1];
		if (settings.GetUseUWGenMatching())
		{
			genMatchingCode = GeneratorInfo::GetGenMatchingCodeUW(event, originalLepton);
		}
		else
		{
			KGenParticle* genParticle = GeneratorInfo::GetGenMatchedParticle(originalLepton, product.m_genParticleMatchedLeptons, product.m_genTauMatchedLeptons);
			if (genParticle)
				genMatchingCode = GeneratorInfo::GetGenMatchingCode(genParticle);
			else
				genMatchingCode = KappaEnumTypes::GenMatchingCode::IS_FAKE;
		}
		KLepton* lepton = product.m_flavourOrderedLeptons[1];
		if ((genMatchingCode == KappaEnumTypes::GenMatchingCode::IS_MUON_PROMPT) || (genMatchingCode == KappaEnumTypes::GenMatchingCode::IS_MUON_FROM_TAU))
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
			KappaEnumTypes::GenMatchingCode genMatchingCode = KappaEnumTypes::GenMatchingCode::NONE;
			KLepton* originalLepton = product.m_originalLeptons.find(product.m_flavourOrderedLeptons[index]) != product.m_originalLeptons.end() ? const_cast<KLepton*>(product.m_originalLeptons.at(product.m_flavourOrderedLeptons[index])) : product.m_flavourOrderedLeptons[index];
			if (settings.GetUseUWGenMatching())
			{
				genMatchingCode = GeneratorInfo::GetGenMatchingCodeUW(event, originalLepton);
			}
			else
			{
				KGenParticle* genParticle = GeneratorInfo::GetGenMatchedParticle(originalLepton, product.m_genParticleMatchedLeptons, product.m_genTauMatchedLeptons);
				if (genParticle)
					genMatchingCode = GeneratorInfo::GetGenMatchingCode(genParticle);
				else
					genMatchingCode = KappaEnumTypes::GenMatchingCode::IS_FAKE;
			}
			KLepton* lepton = product.m_flavourOrderedLeptons[index];
			if ((genMatchingCode == KappaEnumTypes::GenMatchingCode::IS_MUON_PROMPT) || (genMatchingCode == KappaEnumTypes::GenMatchingCode::IS_MUON_FROM_TAU))
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
