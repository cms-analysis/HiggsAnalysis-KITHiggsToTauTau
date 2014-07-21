

#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/GenTauCPProducer.h"

#include "Artus/Consumer/interface/LambdaNtupleConsumer.h"
#include "Artus/Utility/interface/DefaultValues.h"
#include "Artus/KappaAnalysis/interface/MotherDaughterBundle.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Calculations/CPQuantities.h"



void GenTauCPProducer::Init(setting_type const& settings)
{
	ProducerBase<HttTypes>::Init(settings);
	
	// add possible quantities for the lambda ntuples consumers
	LambdaNtupleConsumer<HttTypes>::Quantities["genPhiStarCP"] = [](event_type const & event, product_type const & product)
	{
		return product.m_genPhiStarCP;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["recoPhiStarCP"] = [](event_type const & event, product_type const & product)
	{
		return product.m_recoPhiStarCP;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["genPhi"] = [](event_type const & event, product_type const & product)
	{
		return product.m_genPhi;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["TauMProngEnergy"] = [](event_type const & event, product_type const & product)
	{
		return product.m_genChargedProngEnergies.first;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["TauPProngEnergy"] = [](event_type const & event, product_type const & product)
	{
		return product.m_genChargedProngEnergies.second;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["genPhiDet"] = [](event_type const & event, product_type const & product)
	{
		return product.m_genPhiDet;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["genPhiStarCPDet"] = [](event_type const & event, product_type const & product)
	{
		return product.m_genPhiStarCPDet;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["ThetaNuHadron"] = [](event_type const & event, product_type const & product)
	{
		return product.m_genThetaNuHadron;
	};
	LambdaNtupleConsumer<HttTypes>::Quantities["AlphaTauNeutrinos"] = [](event_type const & event, product_type const & product)
	{
		return product.m_genAlphaTauNeutrinos;
	};
}

void GenTauCPProducer::Produce(event_type const& event, product_type& product,
	                           setting_type const& settings) const
{
	MotherDaughterBundle* higgs = &(product.m_genBoson[0]);	
	MotherDaughterBundle* selectedTau1 = &(higgs->Daughters[0]);
	MotherDaughterBundle* selectedTau2 = &(higgs->Daughters[1]);
	selectedTau1->createFinalStateProngs(selectedTau1);
	selectedTau2->createFinalStateProngs(selectedTau2);
	std::vector<MotherDaughterBundle*> selectedTau1OneProngs = selectedTau1->finalStateOneProngs;
	std::vector<MotherDaughterBundle*> selectedTau2OneProngs = selectedTau2->finalStateOneProngs;
	//Selection of the right channel for phi, phi* and psi*CP
	if (abs(selectedTau1->node->pdgId()) == 15 && abs(selectedTau2->node->pdgId()) == 15 && selectedTau1OneProngs.size() != 0 && selectedTau2OneProngs.size() != 0)
	{
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
		LOG_N_TIMES(20, DEBUG) << chargedPart1->pdgId() << "               " << chargedPart2->pdgId() << std::endl;
		// Saving the charged particles for  analysis
		product.m_genOneProngCharged1 = chargedPart1;
		product.m_genOneProngCharged2 = chargedPart2;
		
		// Saving Energies of charged particles in tau rest frames
		product.m_genChargedProngEnergies.first = CPQuantities::CalculateChargedProngEnergy(selectedTau1->node->p4, chargedPart1->p4);
		product.m_genChargedProngEnergies.second = CPQuantities::CalculateChargedProngEnergy(selectedTau2->node->p4, chargedPart2->p4);
		// Calculation of Phi* and Psi*CP itself

		product.m_genPhiStarCP = CPQuantities::CalculatePhiStarCP(selectedTau1->node->p4, selectedTau2->node->p4, chargedPart1->p4, chargedPart2->p4);
		// Calculatiion of the angle Phi as angle betweeen normal vectors of Tau- -> Pi- and Tau+ -> Pi+ 
		// decay planes 
		product.m_genPhi = CPQuantities::CalculatePhi(higgs->node->p4, selectedTau1->node->p4, selectedTau2->node->p4, chargedPart1->p4, chargedPart2->p4);
		
		//Cross check with neutral Pions
		RMDataLV summedMomentum1;
		RMDataLV summedMomentum2;
		for (unsigned int i = 0; i < selectedTau1OneProngs.size(); i++)
		{
			if (selectedTau1OneProngs[i]->isDetectable())
			{
				//std::cout << "  " << selectedTau1OneProngs[i]->node->pdgId();
				summedMomentum1 += selectedTau1OneProngs[i]->node->p4;
			}
		}
		for (unsigned int i = 0; i < selectedTau2OneProngs.size(); i++)
		{
			if (selectedTau2OneProngs[i]->isDetectable()) 
			{
				//std::cout << "  " << selectedTau2OneProngs[i]->node->pdgId();
				summedMomentum2 += selectedTau2OneProngs[i]->node->p4;
			}
		}
		product.m_genPhiDet = CPQuantities::CalculatePhi(higgs->node->p4, selectedTau1->node->p4, selectedTau2->node->p4, summedMomentum1, summedMomentum2);
		//product.m_genPhiStarCPDet = CPQuantities::CalculatePhiStarCP(selectedTau1->node->p4, selectedTau2->node->p4, summedMomentum1, summedMomentum2);
	}
	else
	{
		product.m_genPhiStarCPDet = DefaultValues::UndefinedDouble;
		product.m_genPhiDet = DefaultValues::UndefinedDouble;
		product.m_genPhiStarCP = DefaultValues::UndefinedDouble;
		product.m_genPhi = DefaultValues::UndefinedDouble;
	}
	if(selectedTau1->Daughters.size() == 2)
	{
		product.m_genThetaNuHadron = CPQuantities::CalculateThetaNuHadron(selectedTau1->node->p4, selectedTau1->Daughters[0].node->p4, selectedTau1->Daughters[1].node->p4);
	}
	else
	{
		product.m_genThetaNuHadron = DefaultValues::UndefinedDouble;
	}
	product.m_genAlphaTauNeutrinos = CPQuantities::CalculateAlphaTauNeutrinos(selectedTau1->node->p4, selectedTau1->Daughters[0].node->p4, selectedTau2->node->p4, selectedTau2->Daughters[0].node->p4);

}
