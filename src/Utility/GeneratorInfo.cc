
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Utility/GeneratorInfo.h"

HttEnumTypes::GenMatchingCode GeneratorInfo::GetGenMatchingCode(const KGenParticle* genParticle)
{
	int pdgId = std::abs(genParticle->pdgId);
	
	if (pdgId == 11 && genParticle->p4.Pt() > 8. && genParticle->isPrompt())
	{
		return HttEnumTypes::GenMatchingCode::IS_ELE_PROMPT;
	}
	else if (pdgId == 13 && genParticle->p4.Pt() > 8. && genParticle->isPrompt())
	{
		return HttEnumTypes::GenMatchingCode::IS_MUON_PROMPT;
	}
	else if (pdgId == 11 && genParticle->p4.Pt() > 8. && genParticle->isDirectPromptTauDecayProduct())
	{
		return HttEnumTypes::GenMatchingCode::IS_ELE_FROM_TAU;
	}
	else if (pdgId == 13 && genParticle->p4.Pt() > 8. && genParticle->isDirectPromptTauDecayProduct())
	{
		return HttEnumTypes::GenMatchingCode::IS_MUON_FROM_TAU;
	}
	else if (pdgId == 15 && genParticle->p4.Pt() > 15.)
	{
		return HttEnumTypes::GenMatchingCode::IS_TAU_HAD_DECAY;
	}
	else
	{
		return HttEnumTypes::GenMatchingCode::IS_FAKE;
	}
}

KGenParticle* GeneratorInfo::GetGenMatchedParticle(
		KLepton* lepton,
		std::map<KLepton*, KGenParticle*> const& leptonGenParticleMap,
		std::map<KTau*, KGenTau*> const& tauGenTauMap
)
{
	// TODO: the pointer new KGenParticle() is a possible memory leak
	KGenParticle* genParticle = SafeMap::GetWithDefault(leptonGenParticleMap, lepton, new KGenParticle());
	
	if (lepton->flavour() == KLeptonFlavour::TAU)
	{
		KGenTau* genTau = SafeMap::GetWithDefault(tauGenTauMap, static_cast<KTau*>(lepton), new KGenTau());
		
		float deltaRTauGenTau = ROOT::Math::VectorUtil::DeltaR(lepton->p4, genTau->visible.p4);
		float deltaRTauGenParticle = ROOT::Math::VectorUtil::DeltaR(lepton->p4, genParticle->p4);
		
		if (deltaRTauGenParticle < deltaRTauGenTau)
		{
			return genParticle;
		}
		else
		{
			return genTau;
		}
	}
	else
	{
		return genParticle;
	}
}
