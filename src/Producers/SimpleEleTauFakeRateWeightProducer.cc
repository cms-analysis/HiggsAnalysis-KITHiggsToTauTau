
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/SimpleEleTauFakeRateWeightProducer.h"
#include "Artus/KappaAnalysis/interface/Utility/GeneratorInfo.h"

SimpleEleTauFakeRateWeightProducer::SimpleEleTauFakeRateWeightProducer(
		std::vector<float>& (setting_type::*GetSimpleEleTauFakeRateWeightVLoose)(void) const,
		std::vector<float>& (setting_type::*GetSimpleEleTauFakeRateWeightTight)(void) const
):
	GetSimpleEleTauFakeRateWeightVLoose(GetSimpleEleTauFakeRateWeightVLoose),
	GetSimpleEleTauFakeRateWeightTight(GetSimpleEleTauFakeRateWeightTight)
{
}

SimpleEleTauFakeRateWeightProducer::SimpleEleTauFakeRateWeightProducer():
		SimpleEleTauFakeRateWeightProducer(&setting_type::GetSimpleEleTauFakeRateWeightVLoose,
										  &setting_type::GetSimpleEleTauFakeRateWeightTight)
{
}

void SimpleEleTauFakeRateWeightProducer::Init(setting_type const& settings)
{
	ProducerBase<HttTypes>::Init(settings);

	SimpleEleTauFakeRateWeightVLoose = (settings.*GetSimpleEleTauFakeRateWeightVLoose)();
	SimpleEleTauFakeRateWeightTight = (settings.*GetSimpleEleTauFakeRateWeightTight)();
}

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

	assert(SimpleEleTauFakeRateWeightVLoose.size() == 2);
	assert(SimpleEleTauFakeRateWeightTight.size() == 2);

	if (product.m_decayChannel == HttEnumTypes::DecayChannel::ET)
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
		if ((genMatchingCode == KappaEnumTypes::GenMatchingCode::IS_ELE_PROMPT) || (genMatchingCode == KappaEnumTypes::GenMatchingCode::IS_ELE_FROM_TAU))
		{
			if(std::abs(lepton->p4.Eta()) < 1.460)
			{
				eTauFakeRateWeight = SimpleEleTauFakeRateWeightTight.at(0);
			}
			else if(std::abs(lepton->p4.Eta()) > 1.558)
			{
				eTauFakeRateWeight = SimpleEleTauFakeRateWeightTight.at(1);
			}
		}
	}
	else if (product.m_decayChannel == HttEnumTypes::DecayChannel::MT)
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
		if ((genMatchingCode == KappaEnumTypes::GenMatchingCode::IS_ELE_PROMPT) || (genMatchingCode == KappaEnumTypes::GenMatchingCode::IS_ELE_FROM_TAU))
		{
			if(std::abs(lepton->p4.Eta()) < 1.460)
			{
				eTauFakeRateWeight = SimpleEleTauFakeRateWeightVLoose.at(0);
			}
			else if(std::abs(lepton->p4.Eta()) > 1.558)
			{
				eTauFakeRateWeight = SimpleEleTauFakeRateWeightVLoose.at(1);
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
			if ((genMatchingCode == KappaEnumTypes::GenMatchingCode::IS_ELE_PROMPT) || (genMatchingCode == KappaEnumTypes::GenMatchingCode::IS_ELE_FROM_TAU))
			{
				if(std::abs(lepton->p4.Eta()) < 1.460)
				{
					eTauFakeRateWeight *= SimpleEleTauFakeRateWeightVLoose.at(0);
				}
				else if(std::abs(lepton->p4.Eta()) > 1.558)
				{
					eTauFakeRateWeight *= SimpleEleTauFakeRateWeightVLoose.at(1);
				}
			}
		}
	}
	product.m_weights["eleTauFakeRateWeight"] = eTauFakeRateWeight;
	
}
