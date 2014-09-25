

#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/GenTauCPProducer.h"

#include "Artus/Consumer/interface/LambdaNtupleConsumer.h"
#include "Artus/Utility/interface/DefaultValues.h"
#include "Artus/KappaAnalysis/interface/MotherDaughterBundle.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/Calculations/CPQuantities.h"



void GenTauCPProducer::Init(setting_type const& settings)
{
	ProducerBase<HttTypes>::Init(settings);
	
	// add possible quantities for the lambda ntuples consumers
	LambdaNtupleConsumer<HttTypes>::AddQuantity("genPhiStarCP", [](event_type const& event, product_type const& product)
	{
		return product.m_genPhiStarCP;
	});
	LambdaNtupleConsumer<HttTypes>::AddQuantity("genPhiCP", [](event_type const& event, product_type const& product)
	{
		return product.m_genPhiCP;
	});
	LambdaNtupleConsumer<HttTypes>::AddQuantity("genPhiStar", [](event_type const& event, product_type const& product)
	{
		return product.m_genPhiStar;
	});
	LambdaNtupleConsumer<HttTypes>::AddQuantity("genPhi", [](event_type const& event, product_type const& product)
	{
		return product.m_genPhi;
	});
	LambdaNtupleConsumer<HttTypes>::AddQuantity("TauMProngEnergy", [](event_type const& event, product_type const& product)
	{
		return product.m_genChargedProngEnergies.first;
	});
	LambdaNtupleConsumer<HttTypes>::AddQuantity("TauPProngEnergy", [](event_type const& event, product_type const& product)
	{
		return product.m_genChargedProngEnergies.second;
	});
	LambdaNtupleConsumer<HttTypes>::AddQuantity("ThetaNuHadron", [](event_type const& event, product_type const& product)
	{
		return product.m_genThetaNuHadron;
	});
	LambdaNtupleConsumer<HttTypes>::AddQuantity("AlphaTauNeutrinos", [](event_type const& event, product_type const& product)
	{
		return product.m_genAlphaTauNeutrinos;
	});
	LambdaNtupleConsumer<HttTypes>::AddQuantity("genImpactParameter1", [](event_type const& event, product_type const& product)
	{
		return product.m_genABS_n1;
	});
	LambdaNtupleConsumer<HttTypes>::AddQuantity("genImpactParameter2", [](event_type const& event, product_type const& product)
	{
		return product.m_genABS_n2;
	});
	// charged particles of a one-prong
	LambdaNtupleConsumer<HttTypes>::AddQuantity("Tau1OneProngsSize", [](event_type const& event, product_type const& product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 0) && (product.m_genBoson[0].Daughters[0].finalStateOneProngs.size() > 0)? product.m_genBoson[0].Daughters[0].finalStateOneProngs.size() : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddQuantity("Tau2OneProngsSize", [](event_type const& event, product_type const& product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[1].finalStateOneProngs.size() > 0)? product.m_genBoson[0].Daughters[1].finalStateOneProngs.size() : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddQuantity("OneProngChargedPart1PdgId", [](event_type const& event, product_type const& product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[0].finalStateOneProngs.size() > 0) && (product.m_genBoson[0].Daughters[1].finalStateOneProngs.size() > 0)? product.m_genOneProngCharged1->pdgId() : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddQuantity("OneProngChargedPart1Pt", [](event_type const& event, product_type const& product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[0].finalStateOneProngs.size() > 0) && (product.m_genBoson[0].Daughters[1].finalStateOneProngs.size() > 0)? product.m_genOneProngCharged1->p4.Pt() : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddQuantity("OneProngChargedPart1Pz", [](event_type const& event, product_type const& product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[0].finalStateOneProngs.size() > 0) && (product.m_genBoson[0].Daughters[1].finalStateOneProngs.size() > 0)? product.m_genOneProngCharged1->p4.Pz() : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddQuantity("OneProngChargedPart1Eta", [](event_type const& event, product_type const& product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[0].finalStateOneProngs.size() > 0) && (product.m_genBoson[0].Daughters[1].finalStateOneProngs.size() > 0)? product.m_genOneProngCharged1->p4.Eta() : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddQuantity("OneProngChargedPart1Phi", [](event_type const& event, product_type const& product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[0].finalStateOneProngs.size() > 0) && (product.m_genBoson[0].Daughters[1].finalStateOneProngs.size() > 0)? product.m_genOneProngCharged1->p4.Phi() : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddQuantity("OneProngChargedPart1Mass", [](event_type const& event, product_type const& product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[0].finalStateOneProngs.size() > 0) && (product.m_genBoson[0].Daughters[1].finalStateOneProngs.size() > 0)? product.m_genOneProngCharged1->p4.mass() : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddQuantity("OneProngChargedPart1Energy", [](event_type const& event, product_type const& product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[0].finalStateOneProngs.size() > 0) && (product.m_genBoson[0].Daughters[1].finalStateOneProngs.size() > 0)? product.m_genOneProngCharged1->p4.E() : DefaultValues::UndefinedDouble;
	});

	LambdaNtupleConsumer<HttTypes>::AddQuantity("OneProngChargedPart2PdgId", [](event_type const& event, product_type const& product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[1].finalStateOneProngs.size() > 0) && (product.m_genBoson[0].Daughters[0].finalStateOneProngs.size() > 0)? product.m_genOneProngCharged2->pdgId() : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddQuantity("OneProngChargedPart2Pt", [](event_type const& event, product_type const& product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[1].finalStateOneProngs.size() > 0) && (product.m_genBoson[0].Daughters[0].finalStateOneProngs.size() > 0)? product.m_genOneProngCharged2->p4.Pt() : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddQuantity("OneProngChargedPart2Pz", [](event_type const& event, product_type const& product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[1].finalStateOneProngs.size() > 0) && (product.m_genBoson[0].Daughters[0].finalStateOneProngs.size() > 0)? product.m_genOneProngCharged2->p4.Pz() : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddQuantity("OneProngChargedPart2Eta", [](event_type const& event, product_type const& product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[1].finalStateOneProngs.size() > 0) && (product.m_genBoson[0].Daughters[0].finalStateOneProngs.size() > 0)? product.m_genOneProngCharged2->p4.Eta() : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddQuantity("OneProngChargedPart2Phi", [](event_type const& event, product_type const& product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[1].finalStateOneProngs.size() > 0) && (product.m_genBoson[0].Daughters[0].finalStateOneProngs.size() > 0)? product.m_genOneProngCharged2->p4.Phi() : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddQuantity("OneProngChargedPart2Mass", [](event_type const& event, product_type const& product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[1].finalStateOneProngs.size() > 0) && (product.m_genBoson[0].Daughters[0].finalStateOneProngs.size() > 0)? product.m_genOneProngCharged2->p4.mass() : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddQuantity("OneProngChargedPart2Energy", [](event_type const& event, product_type const& product)
	{
		return (product.m_genBoson.size() > 0) && (product.m_genBoson[0].Daughters.size() > 1) && (product.m_genBoson[0].Daughters[1].finalStateOneProngs.size() > 0) && (product.m_genBoson[0].Daughters[0].finalStateOneProngs.size() > 0)? product.m_genOneProngCharged2->p4.E() : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddQuantity("genZPlus", [](event_type const& event, product_type const& product)
	{
		return product.m_genZPlus;
	});
	LambdaNtupleConsumer<HttTypes>::AddQuantity("genZMinus", [](event_type const& event, product_type const& product)
	{
		return product.m_genZMinus;
	});
	LambdaNtupleConsumer<HttTypes>::AddQuantity("genZs", [](event_type const& event, product_type const& product)
	{
		return product.m_genZs;
	});
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
		float genPhiStarCP = CPQuantities::CalculatePhiStarCP(selectedTau1->node->p4, selectedTau2->node->p4, chargedPart1->p4, chargedPart2->p4, product.m_genABS_n1, product.m_genABS_n2, product.m_genPhiStar);
		// Calculatiion of the angle Phi as angle betweeen normal vectors of Tau- -> Pi- and Tau+ -> Pi+ 
		// decay planes 
		float genPhiCP = CPQuantities::CalculatePhiCP(higgs->node->p4, selectedTau1->node->p4, selectedTau2->node->p4, chargedPart1->p4, chargedPart2->p4, product.m_genPhi);
		
		//CPTransformation for semileptonic case
		if (settings.GetPhiTransform() == true && (((chargedPart1->pdgId() == DefaultValues::pdgIdElectron || chargedPart1->pdgId() == DefaultValues::pdgIdMuon) && (chargedPart2->pdgId() == 211)) || ((chargedPart2->pdgId() == -DefaultValues::pdgIdElectron || chargedPart2->pdgId() == -DefaultValues::pdgIdMuon) && (chargedPart1->pdgId() == -211))))
		{	
			product.m_genPhiStarCP = CPQuantities::PhiTransform(genPhiStarCP);
			product.m_genPhiCP = CPQuantities::PhiTransform(genPhiCP);
		}
		else
		{
			product.m_genPhiStarCP = genPhiStarCP;
			product.m_genPhiCP = genPhiCP;
		}
		//ZPlusMinus calculation
		product.m_genZPlus = CPQuantities::CalculateZPlusMinus(higgs->node->p4, chargedPart1->p4);
		product.m_genZMinus = CPQuantities::CalculateZPlusMinus(higgs->node->p4, chargedPart2->p4);
		product.m_genZs = CPQuantities::CalculateZs(product.m_genZPlus, product.m_genZMinus);
	}
	else
	{
		product.m_genPhiStarCP = DefaultValues::UndefinedDouble;
		product.m_genPhiCP = DefaultValues::UndefinedDouble;
		product.m_genChargedProngEnergies.first = DefaultValues::UndefinedDouble;
		product.m_genChargedProngEnergies.second = DefaultValues::UndefinedDouble;

		product.m_genZMinus = DefaultValues::UndefinedDouble;
		product.m_genZPlus = DefaultValues::UndefinedDouble;
		product.m_genZs = DefaultValues::UndefinedDouble;
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
