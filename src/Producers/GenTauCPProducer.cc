

#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/GenTauCPProducer.h"

#include "Artus/Utility/interface/DefaultValues.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/CPQuantities.h"


void GenTauCPProducer::ProduceGlobal(HttEvent const& event, HttProduct& product,
									 HttGlobalSettings const& globalSettings) const
{
	std::vector<KappaProduct::MotherDaughterBundle> higgs = product.m_genBoson;
	KGenParticle* selectedTau1 = higgs[0].Daughters[0].node;
	KGenParticle* selectedTau2 = higgs[0].Daughters[1].node;
	std::vector<KappaProduct::MotherDaughterBundle> selectedTauDaughters1 = higgs[0].Daughters[0].Daughters;
	std::vector<KappaProduct::MotherDaughterBundle> selectedTauDaughters2 = higgs[0].Daughters[1].Daughters;
	//Selection of the right channel

	if ((abs(selectedTau1->pdgId()) == 15) && (abs(selectedTau2->pdgId()) == 15) && (selectedTauDaughters1.size() == 2) && (selectedTauDaughters2.size() == 2))
	{
		std::pair<float, float> phiPsiStar;
		
		//Initialization of Pions
		KGenParticle* Pion1 = selectedTauDaughters1[0].node;
		KGenParticle* Pion2 = selectedTauDaughters2[0].node;
		for (unsigned int i = 0; i < selectedTauDaughters1.size(); i++)
		{
			if (abs(selectedTauDaughters1[i].node->pdgId()) == 211) Pion1 = selectedTauDaughters1[i].node;
		}
		for (unsigned int i = 0; i < selectedTauDaughters2.size(); i++)
		{
			if (abs(selectedTauDaughters2[i].node->pdgId()) == 211) Pion2 = selectedTauDaughters2[i].node;
		}

		if ((abs(Pion1->pdgId()) == 211) && (abs(Pion2->pdgId()) == 211)) //check for the right channel
		{
			LOG(DEBUG) << Pion1->pdgId() << "               " << Pion2->pdgId() << std::endl;

			//Calculation of Phi* and Psi*CP itself

			phiPsiStar = CPQuantities::CalculatePhiPsiStar(selectedTau1->p4, selectedTau2->p4, Pion1->p4, Pion2->p4);
			product.m_genPhiStar = phiPsiStar.first;
			product.m_genPsiStarCP = phiPsiStar.second;
			
			// Calculatiion of the angle Phi as angle betweeen normal vectors of Tau- -> Pi- and Tau+ -> Pi+ 
			// decay planes 
			product.m_genPhi = CPQuantities::CalculatePhi(higgs[0].node->p4, selectedTau1->p4, selectedTau2->p4, Pion1->p4, Pion2->p4);
 		}
		else
		{
			product.m_genPhiStar = DefaultValues::UndefinedDouble;	 // Default value in case of a wrong channel
			product.m_genPsiStarCP = DefaultValues::UndefinedDouble;
			product.m_genPhi = DefaultValues::UndefinedDouble;
		}
	}
	else
	{
		product.m_genPhiStar = DefaultValues::UndefinedDouble;
		product.m_genPsiStarCP = DefaultValues::UndefinedDouble;
		product.m_genPhi = DefaultValues::UndefinedDouble;
	}

}

