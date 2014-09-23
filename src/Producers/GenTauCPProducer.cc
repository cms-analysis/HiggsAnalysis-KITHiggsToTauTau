

#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/GenTauCPProducer.h"

#include "Artus/Consumer/interface/LambdaNtupleConsumer.h"
#include "Artus/Utility/interface/DefaultValues.h"
#include "Artus/KappaAnalysis/interface/MotherDaughterBundle.h"
#include "Artus/KappaAnalysis/interface/KappaTypes.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/Calculations/CPQuantities.h"



void GenTauCPProducer::Init(setting_type const& settings)
{
	ProducerBase<HttTypes>::Init(settings);
	
	// add possible quantities for the lambda ntuples consumers
	LambdaNtupleConsumer<KappaTypes>::AddQuantity("genPhiStarCP", [](KappaEvent const& event, KappaProduct const& product)
	{
		return (static_cast<HttProduct const&>(product)).m_genPhiStarCP;
	});
	LambdaNtupleConsumer<KappaTypes>::AddQuantity("genPhiCP", [](KappaEvent const& event, KappaProduct const& product)
	{
		return (static_cast<HttProduct const&>(product)).m_genPhiCP;
	});
	LambdaNtupleConsumer<KappaTypes>::AddQuantity("genPhiStar", [](KappaEvent const& event, KappaProduct const& product)
	{
		return (static_cast<HttProduct const&>(product)).m_genPhiStar;
	});
	LambdaNtupleConsumer<KappaTypes>::AddQuantity("genPhi", [](KappaEvent const& event, KappaProduct const& product)
	{
		return (static_cast<HttProduct const&>(product)).m_genPhi;
	});
	LambdaNtupleConsumer<KappaTypes>::AddQuantity("TauMProngEnergy", [](KappaEvent const& event, KappaProduct const& product)
	{
		return (static_cast<HttProduct const&>(product)).m_genChargedProngEnergies.first;
	});
	LambdaNtupleConsumer<KappaTypes>::AddQuantity("TauPProngEnergy", [](KappaEvent const& event, KappaProduct const& product)
	{
		return (static_cast<HttProduct const&>(product)).m_genChargedProngEnergies.second;
	});
	LambdaNtupleConsumer<KappaTypes>::AddQuantity("ThetaNuHadron", [](KappaEvent const& event, KappaProduct const& product)
	{
		return (static_cast<HttProduct const&>(product)).m_genThetaNuHadron;
	});
	LambdaNtupleConsumer<KappaTypes>::AddQuantity("AlphaTauNeutrinos", [](KappaEvent const& event, KappaProduct const& product)
	{
		return (static_cast<HttProduct const&>(product)).m_genAlphaTauNeutrinos;
	});
	LambdaNtupleConsumer<KappaTypes>::AddQuantity("genImpactParameter1", [](KappaEvent const& event, KappaProduct const& product)
	{
		return (static_cast<HttProduct const&>(product)).m_genABS_n1;
	});
	LambdaNtupleConsumer<KappaTypes>::AddQuantity("genImpactParameter2", [](KappaEvent const& event, KappaProduct const& product)
	{
		return (static_cast<HttProduct const&>(product)).m_genABS_n2;
	});
	// charged particles of a one-prong
	LambdaNtupleConsumer<KappaTypes>::AddQuantity("Tau1OneProngsSize", [](KappaEvent const& event, KappaProduct const& product)
	{
		return ((static_cast<HttProduct const&>(product)).m_genBoson.size() > 0) && ((static_cast<HttProduct const&>(product)).m_genBoson[0].Daughters.size() > 0) && ((static_cast<HttProduct const&>(product)).m_genBoson[0].Daughters[0].finalStateOneProngs.size() > 0)? (static_cast<HttProduct const&>(product)).m_genBoson[0].Daughters[0].finalStateOneProngs.size() : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<KappaTypes>::AddQuantity("Tau2OneProngsSize", [](KappaEvent const& event, KappaProduct const& product)
	{
		return ((static_cast<HttProduct const&>(product)).m_genBoson.size() > 0) && ((static_cast<HttProduct const&>(product)).m_genBoson[0].Daughters.size() > 1) && ((static_cast<HttProduct const&>(product)).m_genBoson[0].Daughters[1].finalStateOneProngs.size() > 0)? (static_cast<HttProduct const&>(product)).m_genBoson[0].Daughters[1].finalStateOneProngs.size() : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<KappaTypes>::AddQuantity("OneProngChargedPart1PdgId", [](KappaEvent const& event, KappaProduct const& product)
	{
		return ((static_cast<HttProduct const&>(product)).m_genBoson.size() > 0) && ((static_cast<HttProduct const&>(product)).m_genBoson[0].Daughters.size() > 1) && ((static_cast<HttProduct const&>(product)).m_genBoson[0].Daughters[0].finalStateOneProngs.size() > 0) && ((static_cast<HttProduct const&>(product)).m_genBoson[0].Daughters[1].finalStateOneProngs.size() > 0)? (static_cast<HttProduct const&>(product)).m_genOneProngCharged1->pdgId() : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<KappaTypes>::AddQuantity("OneProngChargedPart1Pt", [](KappaEvent const& event, KappaProduct const& product)
	{
		return ((static_cast<HttProduct const&>(product)).m_genBoson.size() > 0) && ((static_cast<HttProduct const&>(product)).m_genBoson[0].Daughters.size() > 1) && ((static_cast<HttProduct const&>(product)).m_genBoson[0].Daughters[0].finalStateOneProngs.size() > 0) && ((static_cast<HttProduct const&>(product)).m_genBoson[0].Daughters[1].finalStateOneProngs.size() > 0)? (static_cast<HttProduct const&>(product)).m_genOneProngCharged1->p4.Pt() : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<KappaTypes>::AddQuantity("OneProngChargedPart1Pz", [](KappaEvent const& event, KappaProduct const& product)
	{
		return ((static_cast<HttProduct const&>(product)).m_genBoson.size() > 0) && ((static_cast<HttProduct const&>(product)).m_genBoson[0].Daughters.size() > 1) && ((static_cast<HttProduct const&>(product)).m_genBoson[0].Daughters[0].finalStateOneProngs.size() > 0) && ((static_cast<HttProduct const&>(product)).m_genBoson[0].Daughters[1].finalStateOneProngs.size() > 0)? (static_cast<HttProduct const&>(product)).m_genOneProngCharged1->p4.Pz() : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<KappaTypes>::AddQuantity("OneProngChargedPart1Eta", [](KappaEvent const& event, KappaProduct const& product)
	{
		return ((static_cast<HttProduct const&>(product)).m_genBoson.size() > 0) && ((static_cast<HttProduct const&>(product)).m_genBoson[0].Daughters.size() > 1) && ((static_cast<HttProduct const&>(product)).m_genBoson[0].Daughters[0].finalStateOneProngs.size() > 0) && ((static_cast<HttProduct const&>(product)).m_genBoson[0].Daughters[1].finalStateOneProngs.size() > 0)? (static_cast<HttProduct const&>(product)).m_genOneProngCharged1->p4.Eta() : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<KappaTypes>::AddQuantity("OneProngChargedPart1Phi", [](KappaEvent const& event, KappaProduct const& product)
	{
		return ((static_cast<HttProduct const&>(product)).m_genBoson.size() > 0) && ((static_cast<HttProduct const&>(product)).m_genBoson[0].Daughters.size() > 1) && ((static_cast<HttProduct const&>(product)).m_genBoson[0].Daughters[0].finalStateOneProngs.size() > 0) && ((static_cast<HttProduct const&>(product)).m_genBoson[0].Daughters[1].finalStateOneProngs.size() > 0)? (static_cast<HttProduct const&>(product)).m_genOneProngCharged1->p4.Phi() : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<KappaTypes>::AddQuantity("OneProngChargedPart1Mass", [](KappaEvent const& event, KappaProduct const& product)
	{
		return ((static_cast<HttProduct const&>(product)).m_genBoson.size() > 0) && ((static_cast<HttProduct const&>(product)).m_genBoson[0].Daughters.size() > 1) && ((static_cast<HttProduct const&>(product)).m_genBoson[0].Daughters[0].finalStateOneProngs.size() > 0) && ((static_cast<HttProduct const&>(product)).m_genBoson[0].Daughters[1].finalStateOneProngs.size() > 0)? (static_cast<HttProduct const&>(product)).m_genOneProngCharged1->p4.mass() : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<KappaTypes>::AddQuantity("OneProngChargedPart1Energy", [](KappaEvent const& event, KappaProduct const& product)
	{
		return ((static_cast<HttProduct const&>(product)).m_genBoson.size() > 0) && ((static_cast<HttProduct const&>(product)).m_genBoson[0].Daughters.size() > 1) && ((static_cast<HttProduct const&>(product)).m_genBoson[0].Daughters[0].finalStateOneProngs.size() > 0) && ((static_cast<HttProduct const&>(product)).m_genBoson[0].Daughters[1].finalStateOneProngs.size() > 0)? (static_cast<HttProduct const&>(product)).m_genOneProngCharged1->p4.E() : DefaultValues::UndefinedDouble;
	});

	LambdaNtupleConsumer<KappaTypes>::AddQuantity("OneProngChargedPart2PdgId", [](KappaEvent const& event, KappaProduct const& product)
	{
		return ((static_cast<HttProduct const&>(product)).m_genBoson.size() > 0) && ((static_cast<HttProduct const&>(product)).m_genBoson[0].Daughters.size() > 1) && ((static_cast<HttProduct const&>(product)).m_genBoson[0].Daughters[1].finalStateOneProngs.size() > 0) && ((static_cast<HttProduct const&>(product)).m_genBoson[0].Daughters[0].finalStateOneProngs.size() > 0)? (static_cast<HttProduct const&>(product)).m_genOneProngCharged2->pdgId() : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<KappaTypes>::AddQuantity("OneProngChargedPart2Pt", [](KappaEvent const& event, KappaProduct const& product)
	{
		return ((static_cast<HttProduct const&>(product)).m_genBoson.size() > 0) && ((static_cast<HttProduct const&>(product)).m_genBoson[0].Daughters.size() > 1) && ((static_cast<HttProduct const&>(product)).m_genBoson[0].Daughters[1].finalStateOneProngs.size() > 0) && ((static_cast<HttProduct const&>(product)).m_genBoson[0].Daughters[0].finalStateOneProngs.size() > 0)? (static_cast<HttProduct const&>(product)).m_genOneProngCharged2->p4.Pt() : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<KappaTypes>::AddQuantity("OneProngChargedPart2Pz", [](KappaEvent const& event, KappaProduct const& product)
	{
		return ((static_cast<HttProduct const&>(product)).m_genBoson.size() > 0) && ((static_cast<HttProduct const&>(product)).m_genBoson[0].Daughters.size() > 1) && ((static_cast<HttProduct const&>(product)).m_genBoson[0].Daughters[1].finalStateOneProngs.size() > 0) && ((static_cast<HttProduct const&>(product)).m_genBoson[0].Daughters[0].finalStateOneProngs.size() > 0)? (static_cast<HttProduct const&>(product)).m_genOneProngCharged2->p4.Pz() : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<KappaTypes>::AddQuantity("OneProngChargedPart2Eta", [](KappaEvent const& event, KappaProduct const& product)
	{
		return ((static_cast<HttProduct const&>(product)).m_genBoson.size() > 0) && ((static_cast<HttProduct const&>(product)).m_genBoson[0].Daughters.size() > 1) && ((static_cast<HttProduct const&>(product)).m_genBoson[0].Daughters[1].finalStateOneProngs.size() > 0) && ((static_cast<HttProduct const&>(product)).m_genBoson[0].Daughters[0].finalStateOneProngs.size() > 0)? (static_cast<HttProduct const&>(product)).m_genOneProngCharged2->p4.Eta() : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<KappaTypes>::AddQuantity("OneProngChargedPart2Phi", [](KappaEvent const& event, KappaProduct const& product)
	{
		return ((static_cast<HttProduct const&>(product)).m_genBoson.size() > 0) && ((static_cast<HttProduct const&>(product)).m_genBoson[0].Daughters.size() > 1) && ((static_cast<HttProduct const&>(product)).m_genBoson[0].Daughters[1].finalStateOneProngs.size() > 0) && ((static_cast<HttProduct const&>(product)).m_genBoson[0].Daughters[0].finalStateOneProngs.size() > 0)? (static_cast<HttProduct const&>(product)).m_genOneProngCharged2->p4.Phi() : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<KappaTypes>::AddQuantity("OneProngChargedPart2Mass", [](KappaEvent const& event, KappaProduct const& product)
	{
		return ((static_cast<HttProduct const&>(product)).m_genBoson.size() > 0) && ((static_cast<HttProduct const&>(product)).m_genBoson[0].Daughters.size() > 1) && ((static_cast<HttProduct const&>(product)).m_genBoson[0].Daughters[1].finalStateOneProngs.size() > 0) && ((static_cast<HttProduct const&>(product)).m_genBoson[0].Daughters[0].finalStateOneProngs.size() > 0)? (static_cast<HttProduct const&>(product)).m_genOneProngCharged2->p4.mass() : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<KappaTypes>::AddQuantity("OneProngChargedPart2Energy", [](KappaEvent const& event, KappaProduct const& product)
	{
		return ((static_cast<HttProduct const&>(product)).m_genBoson.size() > 0) && ((static_cast<HttProduct const&>(product)).m_genBoson[0].Daughters.size() > 1) && ((static_cast<HttProduct const&>(product)).m_genBoson[0].Daughters[1].finalStateOneProngs.size() > 0) && ((static_cast<HttProduct const&>(product)).m_genBoson[0].Daughters[0].finalStateOneProngs.size() > 0)? (static_cast<HttProduct const&>(product)).m_genOneProngCharged2->p4.E() : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<KappaTypes>::AddQuantity("genZPlus", [](KappaEvent const& event, KappaProduct const& product)
	{
		return (static_cast<HttProduct const&>(product)).m_genZPlus;
	});
	LambdaNtupleConsumer<KappaTypes>::AddQuantity("genZMinus", [](KappaEvent const& event, KappaProduct const& product)
	{
		return (static_cast<HttProduct const&>(product)).m_genZMinus;
	});
	LambdaNtupleConsumer<KappaTypes>::AddQuantity("genZs", [](KappaEvent const& event, KappaProduct const& product)
	{
		return (static_cast<HttProduct const&>(product)).m_genZs;
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
