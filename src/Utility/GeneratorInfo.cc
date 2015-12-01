
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Utility/GeneratorInfo.h"

int GeneratorInfo::GetGenMatchingCode(const KGenParticle* genParticle)
{
	int pdgId = std::abs(genParticle->pdgId());
	
	if (pdgId == 11 && genParticle->p4.Pt() > 8. && genParticle->isPrompt())
	{
		return static_cast<int>(GenMatchingCode::isElePrompt);
	}
	else if (pdgId == 13 && genParticle->p4.Pt() > 8. && genParticle->isPrompt())
	{
		return static_cast<int>(GenMatchingCode::isMuonPrompt);
	}
	else if (pdgId == 11 && genParticle->p4.Pt() > 8. && genParticle->isDirectPromptTauDecayProduct())
	{
		return static_cast<int>(GenMatchingCode::isEleFromTau);
	}
	else if (pdgId == 13 && genParticle->p4.Pt() > 8. && genParticle->isDirectPromptTauDecayProductFinalState())
	{
		return static_cast<int>(GenMatchingCode::isMuonFromTau);
	}
	else if (pdgId == 15 && genParticle->p4.Pt() > 15.)
	{
		return static_cast<int>(GenMatchingCode::isTauHadDecay);
	}
	else
	{
		return static_cast<int>(GenMatchingCode::isFake);
	}
}