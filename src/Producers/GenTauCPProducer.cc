

#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/GenTauCPProducer.h"

#include "Artus/Utility/interface/DefaultValues.h"
#include "Artus/KappaAnalysis/interface/MotherDaughterBundle.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Calculations/CPQuantities.h"


void GenTauCPProducer::ProduceGlobal(HttEvent const& event, HttProduct& product,
									 HttGlobalSettings const& globalSettings) const
{
	MotherDaughterBundle* higgs = &(product.m_genBoson[0]);	
	MotherDaughterBundle* selectedTau1 = &(higgs->Daughters[0]);
	MotherDaughterBundle* selectedTau2 = &(higgs->Daughters[1]);
	selectedTau1->createFinalStateProngs(selectedTau1);
	selectedTau2->createFinalStateProngs(selectedTau2);
	std::vector<MotherDaughterBundle*> selectedTau1OneProngs = selectedTau1->finalStateOneProngs;
	std::vector<MotherDaughterBundle*> selectedTau2OneProngs = selectedTau2->finalStateOneProngs;
	//Selection of the right channel
	if (abs(selectedTau1->node->pdgId()) == 15 && abs(selectedTau2->node->pdgId()) == 15 && selectedTau1OneProngs.size() != 0 && selectedTau2OneProngs.size() != 0)
	{
		std::pair<float, float> phiPsiStar;
		//Initialization of charged particles
		KGenParticle* chargedPart1 = selectedTau1OneProngs[0]->node;
		KGenParticle* chargedPart2 = selectedTau2OneProngs[0]->node;
		for (unsigned int i = 0; i < selectedTau1OneProngs.size(); i++)
		{
			if (abs(selectedTau1OneProngs[i]->getCharge()) == 1) chargedPart1 = selectedTau1OneProngs[i]->node;
		}
		for (unsigned int i = 0; i < selectedTau2OneProngs.size(); i++)
		{
			if (abs(selectedTau2OneProngs[i]->getCharge()) == 1) chargedPart2 = selectedTau2OneProngs[i]->node;
		}
		LOG(DEBUG) << chargedPart1->pdgId() << "               " << chargedPart2->pdgId() << std::endl;
		// Saving the charged particles for  analysis
		product.m_genOneProngCharged1 = chargedPart1;
		product.m_genOneProngCharged2 = chargedPart2;
		// Calculation of Phi* and Psi*CP itself

		phiPsiStar = CPQuantities::CalculatePhiPsiStar(selectedTau1->node->p4, selectedTau2->node->p4, chargedPart1->p4, chargedPart2->p4);
		product.m_genPhiStar = phiPsiStar.first;
		product.m_genPsiStarCP = phiPsiStar.second;

		// Calculatiion of the angle Phi as angle betweeen normal vectors of Tau- -> Pi- and Tau+ -> Pi+ 
		// decay planes 
		product.m_genPhi = CPQuantities::CalculatePhi(higgs->node->p4, selectedTau1->node->p4, selectedTau2->node->p4, chargedPart1->p4, chargedPart2->p4);
		
		//Cross check for neutral Pions
		RMDataLV summedMomentum1;
		RMDataLV summedMomentum2;
		for (unsigned int i = 0; i < selectedTau1OneProngs.size(); i++)
		{
			if (selectedTau1OneProngs[i]->isDetectable()) summedMomentum1 += selectedTau1OneProngs[i]->node->p4;
		}
		for (unsigned int i = 0; i < selectedTau2OneProngs.size(); i++)
		{
			if (selectedTau2OneProngs[i]->isDetectable()) summedMomentum2 += selectedTau2OneProngs[i]->node->p4;
		}
		product.PhiDet = CPQuantities::CalculatePhi(higgs->node->p4, selectedTau1->node->p4, selectedTau2->node->p4, summedMomentum1, summedMomentum2);
	}
	else
	{
		product.PhiDet = DefaultValues::UndefinedDouble;
		product.m_genPhiStar = DefaultValues::UndefinedDouble;
		product.m_genPsiStarCP = DefaultValues::UndefinedDouble;
		product.m_genPhi = DefaultValues::UndefinedDouble;
	}

}

