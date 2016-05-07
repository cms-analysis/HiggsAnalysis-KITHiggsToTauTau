

#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/GenTauCPProducer.h"

#include "Artus/Consumer/interface/LambdaNtupleConsumer.h"
#include "Artus/Utility/interface/DefaultValues.h"
#include "Artus/KappaAnalysis/interface/Utility/GenParticleDecayTree.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/Utility/CPQuantities.h"



void GenTauCPProducer::Init(setting_type const& settings)
{
	ProducerBase<HttTypes>::Init(settings);
	
	// add possible quantities for the lambda ntuples consumers
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("genPhiStarCP", [](event_type const& event, product_type const& product)
	{
		return product.m_genPhiStarCP;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("genOStarCP", [](event_type const& event, product_type const& product)
	{
		return product.m_genOStarCP;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("genPhiCP", [](event_type const& event, product_type const& product)
	{
		return product.m_genPhiCP;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("genOCP", [](event_type const& event, product_type const& product)
	{
		return product.m_genOCP; 
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("genPhiStar", [](event_type const& event, product_type const& product)
	{
		return product.m_genPhiStar;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("genPhi", [](event_type const& event, product_type const& product)
	{
		return product.m_genPhi;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("genTauMinusDirX", [](event_type const& event, product_type const& product)
	{
		return product.m_genTauMinusDirX; 
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("genTauMinusDirY", [](event_type const& event, product_type const& product)
	{
		return product.m_genTauMinusDirY;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("genTauMinusDirZ", [](event_type const& event, product_type const& product)
	{
		return product.m_genTauMinusDirZ;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("genPiMinusDirX", [](event_type const& event, product_type const& product)
	{
		return product.m_genPiMinusDirX; 
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("genPiMinusDirY", [](event_type const& event, product_type const& product)
	{
		return product.m_genPiMinusDirY;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("genPiMinusDirZ", [](event_type const& event, product_type const& product)
	{
		return product.m_genPiMinusDirZ;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("TauMProngEnergy", [](event_type const& event, product_type const& product)
	{
		return product.m_genChargedProngEnergies.first;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("TauPProngEnergy", [](event_type const& event, product_type const& product)
	{
		return product.m_genChargedProngEnergies.second;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("ThetaNuHadron", [](event_type const& event, product_type const& product)
	{
		return product.m_genThetaNuHadron;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("AlphaTauNeutrinos", [](event_type const& event, product_type const& product)
	{
		return product.m_genAlphaTauNeutrinos;
	});
	// charged particles of a one-prong
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("Tau1OneProngsSize", [](event_type const& event, product_type const& product)
	{
		return ((product.m_genBosonTree.m_daughters.size() > 0) && (product.m_genBosonTree.m_daughters[0].m_finalStateOneProngs.size() > 0))? product.m_genBosonTree.m_daughters[0].m_finalStateOneProngs.size() : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("Tau2OneProngsSize", [](event_type const& event, product_type const& product)
	{
		return ((product.m_genBosonTree.m_daughters.size() > 1) && (product.m_genBosonTree.m_daughters[1].m_finalStateOneProngs.size() > 0))? product.m_genBosonTree.m_daughters[1].m_finalStateOneProngs.size() : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("OneProngChargedPart1PdgId", [](event_type const& event, product_type const& product)
	{
		return ((product.m_genOneProngCharged1 != 0) && ((product.m_genBosonTree.m_daughters.size() > 1) && (product.m_genBosonTree.m_daughters[0].m_finalStateOneProngs.size() > 0) && (product.m_genBosonTree.m_daughters[1].m_finalStateOneProngs.size() > 0)))? product.m_genOneProngCharged1->pdgId : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("OneProngChargedPart1Pt", [](event_type const& event, product_type const& product)
	{
		return ((product.m_genOneProngCharged1 != 0) && ((product.m_genBosonTree.m_daughters.size() > 1) && (product.m_genBosonTree.m_daughters[0].m_finalStateOneProngs.size() > 0) && (product.m_genBosonTree.m_daughters[1].m_finalStateOneProngs.size() > 0)))? product.m_genOneProngCharged1->p4.Pt() : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("OneProngChargedPart1Pz", [](event_type const& event, product_type const& product)
	{
		return ((product.m_genOneProngCharged1 != 0) && ((product.m_genBosonTree.m_daughters.size() > 1) && (product.m_genBosonTree.m_daughters[0].m_finalStateOneProngs.size() > 0) && (product.m_genBosonTree.m_daughters[1].m_finalStateOneProngs.size() > 0)))? product.m_genOneProngCharged1->p4.Pz() : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("OneProngChargedPart1Eta", [](event_type const& event, product_type const& product)
	{
		return ((product.m_genOneProngCharged1 != 0) && ((product.m_genBosonTree.m_daughters.size() > 1) && (product.m_genBosonTree.m_daughters[0].m_finalStateOneProngs.size() > 0) && (product.m_genBosonTree.m_daughters[1].m_finalStateOneProngs.size() > 0)))? product.m_genOneProngCharged1->p4.Eta() : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("OneProngChargedPart1Phi", [](event_type const& event, product_type const& product)
	{
		return ((product.m_genOneProngCharged1 != 0) && ((product.m_genBosonTree.m_daughters.size() > 1) && (product.m_genBosonTree.m_daughters[0].m_finalStateOneProngs.size() > 0) && (product.m_genBosonTree.m_daughters[1].m_finalStateOneProngs.size() > 0)))? product.m_genOneProngCharged1->p4.Phi() : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("OneProngChargedPart1Mass", [](event_type const& event, product_type const& product)
	{
		return ((product.m_genOneProngCharged1 != 0) && ((product.m_genBosonTree.m_daughters.size() > 1) && (product.m_genBosonTree.m_daughters[0].m_finalStateOneProngs.size() > 0) && (product.m_genBosonTree.m_daughters[1].m_finalStateOneProngs.size() > 0)))? product.m_genOneProngCharged1->p4.mass() : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("OneProngChargedPart1Energy", [](event_type const& event, product_type const& product)
	{
		return ((product.m_genOneProngCharged1 != 0) && ((product.m_genBosonTree.m_daughters.size() > 1) && (product.m_genBosonTree.m_daughters[0].m_finalStateOneProngs.size() > 0) && (product.m_genBosonTree.m_daughters[1].m_finalStateOneProngs.size() > 0)))? product.m_genOneProngCharged1->p4.E() : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("OneProngChargedPart2PdgId", [](event_type const& event, product_type const& product)
	{
		return ((product.m_genOneProngCharged2 != 0) && ((product.m_genBosonTree.m_daughters.size() > 1) && (product.m_genBosonTree.m_daughters[1].m_finalStateOneProngs.size() > 0) && (product.m_genBosonTree.m_daughters[0].m_finalStateOneProngs.size() > 0)))? product.m_genOneProngCharged2->pdgId : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("OneProngChargedPart2Pt", [](event_type const& event, product_type const& product)
	{
		return ((product.m_genOneProngCharged2 != 0) && ((product.m_genBosonTree.m_daughters.size() > 1) && (product.m_genBosonTree.m_daughters[1].m_finalStateOneProngs.size() > 0) && (product.m_genBosonTree.m_daughters[0].m_finalStateOneProngs.size() > 0)))? product.m_genOneProngCharged2->p4.Pt() : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("OneProngChargedPart2Pz", [](event_type const& event, product_type const& product)
	{
		return ((product.m_genOneProngCharged2 != 0) && ((product.m_genBosonTree.m_daughters.size() > 1) && (product.m_genBosonTree.m_daughters[1].m_finalStateOneProngs.size() > 0) && (product.m_genBosonTree.m_daughters[0].m_finalStateOneProngs.size() > 0)))? product.m_genOneProngCharged2->p4.Pz() : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("OneProngChargedPart2Eta", [](event_type const& event, product_type const& product)
	{
		return ((product.m_genOneProngCharged2 != 0) && ((product.m_genBosonTree.m_daughters.size() > 1) && (product.m_genBosonTree.m_daughters[1].m_finalStateOneProngs.size() > 0) && (product.m_genBosonTree.m_daughters[0].m_finalStateOneProngs.size() > 0)))? product.m_genOneProngCharged2->p4.Eta() : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("OneProngChargedPart2Phi", [](event_type const& event, product_type const& product)
	{
		return ((product.m_genOneProngCharged2 != 0) && ((product.m_genBosonTree.m_daughters.size() > 1) && (product.m_genBosonTree.m_daughters[1].m_finalStateOneProngs.size() > 0) && (product.m_genBosonTree.m_daughters[0].m_finalStateOneProngs.size() > 0)))? product.m_genOneProngCharged2->p4.Phi() : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("OneProngChargedPart2Mass", [](event_type const& event, product_type const& product)
	{
		return ((product.m_genOneProngCharged2 != 0) && ((product.m_genBosonTree.m_daughters.size() > 1) && (product.m_genBosonTree.m_daughters[1].m_finalStateOneProngs.size() > 0) && (product.m_genBosonTree.m_daughters[0].m_finalStateOneProngs.size() > 0)))? product.m_genOneProngCharged2->p4.mass() : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("OneProngChargedPart2Energy", [](event_type const& event, product_type const& product)
	{
		return ((product.m_genOneProngCharged2 != 0) && ((product.m_genBosonTree.m_daughters.size() > 1) && (product.m_genBosonTree.m_daughters[1].m_finalStateOneProngs.size() > 0) && (product.m_genBosonTree.m_daughters[0].m_finalStateOneProngs.size() > 0)))? product.m_genOneProngCharged2->p4.E() : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("genZPlus", [](event_type const& event, product_type const& product)
	{
		return product.m_genZPlus;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("genZMinus", [](event_type const& event, product_type const& product)
	{
		return product.m_genZMinus;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("genZs", [](event_type const& event, product_type const& product)
	{
		return product.m_genZs;
	});
}

void GenTauCPProducer::Produce(event_type const& event, product_type& product,
	                           setting_type const& settings) const
{
	// A generator level boson and its decay products must exist
	// The boson is searched for by a GenBosonProducer
	// and the decay tree is built by the GenTauDecayProducer
	assert(product.m_genBosonTree.m_daughters.size() > 1);
	
	GenParticleDecayTree* higgs = &(product.m_genBosonTree);
	GenParticleDecayTree* selectedTau1 = &(higgs->m_daughters[0]);
	GenParticleDecayTree* selectedTau2 = &(higgs->m_daughters[1]);
	selectedTau1->CreateFinalStateProngs(selectedTau1);
	selectedTau2->CreateFinalStateProngs(selectedTau2);
	std::vector<GenParticleDecayTree*> selectedTau1OneProngs = selectedTau1->m_finalStateOneProngs;
	std::vector<GenParticleDecayTree*> selectedTau2OneProngs = selectedTau2->m_finalStateOneProngs;
	// Defining CPQuantities object to use variables and functions of this class
	CPQuantities cpq;
	//Selection of the right channel for phi, phi* and psi*CP
	if (abs(selectedTau1->m_genParticle->pdgId) == 15 && abs(selectedTau2->m_genParticle->pdgId) == 15 && selectedTau1OneProngs.size() != 0 && selectedTau2OneProngs.size() != 0)
	{
		//Initialization of charged particles
		KGenParticle* chargedPart1 = selectedTau1OneProngs[0]->m_genParticle;
		KGenParticle* chargedPart2 = selectedTau2OneProngs[0]->m_genParticle;
		for (unsigned int i = 0; i < selectedTau1OneProngs.size(); i++)
		{
			if (abs(selectedTau1OneProngs[i]->GetCharge()) == 1) chargedPart1 = selectedTau1OneProngs[i]->m_genParticle;
		}
		for (unsigned int i = 0; i < selectedTau2OneProngs.size(); i++)
		{
			if (abs(selectedTau2OneProngs[i]->GetCharge()) == 1) chargedPart2 = selectedTau2OneProngs[i]->m_genParticle;
		}
		// Saving the charged particles for  analysis
		product.m_genOneProngCharged1 = chargedPart1;
		product.m_genOneProngCharged2 = chargedPart2;
		// Saving Energies of charged particles in tau rest frames
		product.m_genChargedProngEnergies.first = cpq.CalculateChargedProngEnergy(selectedTau1->m_genParticle->p4, chargedPart1->p4);
		product.m_genChargedProngEnergies.second = cpq.CalculateChargedProngEnergy(selectedTau2->m_genParticle->p4, chargedPart2->p4);
		// Calculation of Phi* and Phi*CP itself
		double genPhiStarCP = cpq.CalculatePhiStarCP(selectedTau1->m_genParticle->p4, selectedTau2->m_genParticle->p4, chargedPart1->p4, chargedPart2->p4);
		product.m_genPhiStar = cpq.GetGenPhiStar();
		product.m_genOStarCP = cpq.CalculateOStarCP(selectedTau1->m_genParticle->p4, selectedTau2->m_genParticle->p4, chargedPart1->p4, chargedPart2->p4);
		// Calculation of the angle Phi as angle betweeen normal vectors of Tau- -> Pi- and Tau+ -> Pi+ 
		// decay planes 
		double genPhiCP = cpq.CalculatePhiCP(higgs->m_genParticle->p4, selectedTau1->m_genParticle->p4, selectedTau2->m_genParticle->p4, chargedPart1->p4, chargedPart2->p4);
		product.m_genPhi = cpq.GetGenPhi();
		product.m_genOCP = cpq.CalculateOCP(higgs->m_genParticle->p4, selectedTau1->m_genParticle->p4, selectedTau2->m_genParticle->p4, chargedPart1->p4, chargedPart2->p4);

		std::vector<float> tauDir = cpq.CalculateTauMinusDirection(higgs->m_genParticle->p4, selectedTau1->m_genParticle->p4);
		product.m_genTauMinusDirX = tauDir.at(0);
		product.m_genTauMinusDirY = tauDir.at(1);
		product.m_genTauMinusDirZ = tauDir.at(2);

		std::vector<float> piDir = cpq.CalculatePiMinusDirection(selectedTau1->m_genParticle->p4, chargedPart1->p4);
		product.m_genPiMinusDirX = piDir.at(0);
		product.m_genPiMinusDirY = piDir.at(1);
		product.m_genPiMinusDirZ = piDir.at(2);

		//CPTransformation for semileptonic case
		if (settings.GetPhiTransform() == true && (((chargedPart1->pdgId == DefaultValues::pdgIdElectron || chargedPart1->pdgId == DefaultValues::pdgIdMuon) && (chargedPart2->pdgId == 211)) || ((chargedPart2->pdgId == -DefaultValues::pdgIdElectron || chargedPart2->pdgId == -DefaultValues::pdgIdMuon) && (chargedPart1->pdgId == -211))))
		{	
			product.m_genPhiStarCP = cpq.PhiTransform(genPhiStarCP);
			product.m_genPhiCP = cpq.PhiTransform(genPhiCP);
		}
		else
		{
			product.m_genPhiStarCP = genPhiStarCP;
			product.m_genPhiCP = genPhiCP;
		}
		//ZPlusMinus calculation
		product.m_genZPlus = cpq.CalculateZPlusMinus(higgs->m_genParticle->p4, chargedPart1->p4);
		product.m_genZMinus = cpq.CalculateZPlusMinus(higgs->m_genParticle->p4, chargedPart2->p4);
		product.m_genZs = cpq.CalculateZs(product.m_genZPlus, product.m_genZMinus);
	}
	if(selectedTau1->m_daughters.size() == 2)
	{
		product.m_genThetaNuHadron = cpq.CalculateThetaNuHadron(selectedTau1->m_genParticle->p4, selectedTau1->m_daughters[0].m_genParticle->p4, selectedTau1->m_daughters[1].m_genParticle->p4);
	}
	
	if ((! selectedTau1->m_daughters.empty()) && (! selectedTau2->m_daughters.empty()))
	{
		product.m_genAlphaTauNeutrinos = cpq.CalculateAlphaTauNeutrinos(selectedTau1->m_genParticle->p4, selectedTau1->m_daughters[0].m_genParticle->p4, selectedTau2->m_genParticle->p4, selectedTau2->m_daughters[0].m_genParticle->p4);
	}

}
