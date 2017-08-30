
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/GenTauCPProducers.h"

#include "Artus/Consumer/interface/LambdaNtupleConsumer.h"
#include "Artus/Utility/interface/DefaultValues.h"
#include "Artus/KappaAnalysis/interface/Utility/GenParticleDecayTree.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/Utility/CPQuantities.h"


void GenTauCPProducerBase::Init(setting_type const& settings)
{
	ProducerBase<HttTypes>::Init(settings);

	// add possible quantities for the lambda ntuples consumers

	// MC-truth PV coordinates
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("genPVx", [](event_type const& event, product_type const& product)
	{
		return ((product.m_genPV != nullptr) ? (product.m_genPV)->x() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("genPVy", [](event_type const& event, product_type const& product)
	{
		return ((product.m_genPV != nullptr) ? (product.m_genPV)->y() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("genPVz", [](event_type const& event, product_type const& product)
	{
		return ((product.m_genPV != nullptr) ? (product.m_genPV)->z() : DefaultValues::UndefinedFloat);
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("genPhiStarCP", [](event_type const& event, product_type const& product)
	{
		return product.m_genPhiStarCP;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("genPhiStarCP_rho", [](event_type const& event, product_type const& product)
	{
		return product.m_genPhiStarCP_rho;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("gen_posyTauL", [](event_type const& event, product_type const& product)
	{
		return product.m_gen_posyTauL;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("gen_negyTauL", [](event_type const& event, product_type const& product)
	{
		return product.m_gen_negyTauL;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("gen_yTau", [](event_type const& event, product_type const& product)
	{
		return product.m_gen_yTau;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("genPhiCP", [](event_type const& event, product_type const& product)
	{
		return product.m_genPhiCP;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("genPhiCPLab", [](event_type const& event, product_type const& product)
	{
		return product.m_genPhiCPLab;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("genPhiCP_rho", [](event_type const& event, product_type const& product)
	{
		return product.m_genPhiCP_rho;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("genPhiStar", [](event_type const& event, product_type const& product)
	{
		return product.m_genPhiStar;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("genOStarCP", [](event_type const& event, product_type const& product)
	{
		return product.m_genOStarCP;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("genPhiStar_rho", [](event_type const& event, product_type const& product)
	{
		return product.m_genPhiStar_rho;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("genPhi", [](event_type const& event, product_type const& product)
	{
		return product.m_genPhi;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("genOCP", [](event_type const& event, product_type const& product)
	{
		return product.m_genOCP;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("genPhi_rho", [](event_type const& event, product_type const& product)
	{
		return product.m_genPhi_rho;
	});

	// energy of the charged prong particles in the tau rest frame
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("TauPProngEnergy", [](event_type const& event, product_type const& product)
	{
		return product.m_genChargedProngEnergies.first;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("TauMProngEnergy", [](event_type const& event, product_type const& product)
	{
		return product.m_genChargedProngEnergies.second;
	});

	// charged particles of a one-prong tau
	// FIXME these two variables could be removed ???
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("Tau1OneProngsSize", [](event_type const& event, product_type const& product)
	{
		return product.m_genTau1ProngsSize;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("Tau2OneProngsSize", [](event_type const& event, product_type const& product)
	{
		return product.m_genTau2ProngsSize;
	});

	// decay mode of the taus from KGenTau
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("Tau1DecayMode", [](event_type const& event, product_type const& product)
	{
		return product.m_genTau1DecayMode;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("Tau2DecayMode", [](event_type const& event, product_type const& product)
	{
		return product.m_genTau2DecayMode;
	});
	// decay mode of the taus from GenParticleDecayTree
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("TauTree1DecayMode", [](event_type const& event, product_type const& product)
	{
		return product.m_genTauTree1DecayMode;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("TauTree2DecayMode", [](event_type const& event, product_type const& product)
	{
		return product.m_genTauTree2DecayMode;
	});
	
	// MC-truth IP vectors
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("genIP1x", [](event_type const& event, product_type const& product)
	{
		return ((&product.m_genIP1 != nullptr) ? (product.m_genIP1).x() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("genIP1y", [](event_type const& event, product_type const& product)
	{
		return ((&product.m_genIP1 != nullptr) ? (product.m_genIP1).y() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("genIP1z", [](event_type const& event, product_type const& product)
	{
		return ((&product.m_genIP1 != nullptr) ? (product.m_genIP1).z() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("genIP2x", [](event_type const& event, product_type const& product)
	{
		return ((&product.m_genIP2 != nullptr) ? (product.m_genIP2).x() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("genIP2y", [](event_type const& event, product_type const& product)
	{
		return ((&product.m_genIP2 != nullptr) ? (product.m_genIP2).y() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("genIP2z", [](event_type const& event, product_type const& product)
	{
		return ((&product.m_genIP2 != nullptr) ? (product.m_genIP2).z() : DefaultValues::UndefinedFloat);
	});

	// cosPsi
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("genCosPsiPlus", [](event_type const& event, product_type const& product)
	{
		return product.m_genCosPsiPlus;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("genCosPsiMinus", [](event_type const& event, product_type const& product)
	{
		return product.m_genCosPsiMinus;
	});

	// properties of the charged particles from tau decays
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("OneProngChargedPart1PdgId", [](event_type const& event, product_type const& product)
	{
		return product.m_genOneProngCharged1 != nullptr ? product.m_genOneProngCharged1->pdgId : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("OneProngChargedPart1Pt", [](event_type const& event, product_type const& product)
	{
		return product.m_genOneProngCharged1 != nullptr ? product.m_genOneProngCharged1->p4.Pt() : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("OneProngChargedPart1Pz", [](event_type const& event, product_type const& product)
	{
		return product.m_genOneProngCharged1 != nullptr ? product.m_genOneProngCharged1->p4.Pz() : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("OneProngChargedPart1Eta", [](event_type const& event, product_type const& product)
	{
		return product.m_genOneProngCharged1 != nullptr ? product.m_genOneProngCharged1->p4.Eta() : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("OneProngChargedPart1Phi", [](event_type const& event, product_type const& product)
	{
		return product.m_genOneProngCharged1 != nullptr ? product.m_genOneProngCharged1->p4.Phi() : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("OneProngChargedPart1Mass", [](event_type const& event, product_type const& product)
	{
		return product.m_genOneProngCharged1 != nullptr ? product.m_genOneProngCharged1->p4.mass() : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("OneProngChargedPart1Energy", [](event_type const& event, product_type const& product)
	{
		return product.m_genOneProngCharged1 != nullptr ? product.m_genOneProngCharged1->p4.E() : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("OneProngChargedPart2PdgId", [](event_type const& event, product_type const& product)
	{
		return product.m_genOneProngCharged2 != nullptr ? product.m_genOneProngCharged2->pdgId : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("OneProngChargedPart2Pt", [](event_type const& event, product_type const& product)
	{
		return product.m_genOneProngCharged2 != nullptr ? product.m_genOneProngCharged2->p4.Pt() : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("OneProngChargedPart2Pz", [](event_type const& event, product_type const& product)
	{
		return product.m_genOneProngCharged2 != nullptr ? product.m_genOneProngCharged2->p4.Pz() : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("OneProngChargedPart2Eta", [](event_type const& event, product_type const& product)
	{
		return product.m_genOneProngCharged2 != nullptr ? product.m_genOneProngCharged2->p4.Eta() : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("OneProngChargedPart2Phi", [](event_type const& event, product_type const& product)
	{
		return product.m_genOneProngCharged2 != nullptr ? product.m_genOneProngCharged2->p4.Phi() : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("OneProngChargedPart2Mass", [](event_type const& event, product_type const& product)
	{
		return product.m_genOneProngCharged2 != nullptr ? product.m_genOneProngCharged2->p4.mass() : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("OneProngChargedPart2Energy", [](event_type const& event, product_type const& product)
	{
		return product.m_genOneProngCharged2 != nullptr ? product.m_genOneProngCharged2->p4.E() : DefaultValues::UndefinedDouble;
	});

	// longitudinal spin correlations
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

void GenTauCPProducerBase::Produce(event_type const& event, product_type& product,
                                   setting_type const& settings) const
{

	// A generator level boson and its decay products must exist
	// The boson is searched for by a GenBosonProducer
	// and the decay tree is built by the GenTauDecayProducer
	//if ( product.m_genBosonLVFound && (product.m_genBosonTree.m_daughters.size() > 1 ) )
	if ( product.m_genBosonLVFound && product.m_genLeptonsFromBosonDecay.size() > 1
		&& (std::abs(product.m_genLeptonsFromBosonDecay.at(0)->pdgId) == DefaultValues::pdgIdTau)
		&& (std::abs(product.m_genLeptonsFromBosonDecay.at(1)->pdgId) == DefaultValues::pdgIdTau) )
	{

		// save MC-truth PV
		for (unsigned int i=0; i<event.m_genParticles->size(); ++i){
			if (event.m_genParticles->at(i).pdgId == 23 || event.m_genParticles->at(i).pdgId == 25 || event.m_genParticles->at(i).pdgId == 36){
				product.m_genPV = &event.m_genParticles->at(i).vertex;
			}
		}
	
		// initialization of TVector3 objects
		product.m_genIP1.SetXYZ(-999,-999,-999);
		product.m_genIP2.SetXYZ(-999,-999,-999);

		// genTauDecayTree1 is the positevely charged genBosonDaughter
		GenParticleDecayTree* genTauDecayTree1 = nullptr;
		GenParticleDecayTree* genTauDecayTree2 = nullptr;
		KGenTau* genTau1 = nullptr;
		KGenTau* genTau2 = nullptr;
		if (product.m_genBosonTree.m_daughters.at(0).m_genParticle->charge() == +1){
			genTauDecayTree1 = &(product.m_genBosonTree.m_daughters.at(0));
			genTauDecayTree2 = &(product.m_genBosonTree.m_daughters.at(1));
		}
		else {
			genTauDecayTree1 = &(product.m_genBosonTree.m_daughters.at(1));
			genTauDecayTree2 = &(product.m_genBosonTree.m_daughters.at(0));
		}
		genTau1 = SafeMap::GetWithDefault(product.m_validGenTausMap, genTauDecayTree1->m_genParticle, static_cast<KGenTau*>(nullptr));
		genTau2 = SafeMap::GetWithDefault(product.m_validGenTausMap, genTauDecayTree2->m_genParticle, static_cast<KGenTau*>(nullptr));
		product.m_genTau1DecayMode = genTau1->genDecayMode();
		product.m_genTau2DecayMode = genTau2->genDecayMode();

		// get the full decay tree of the taus
		genTauDecayTree1->DetermineDecayMode(genTauDecayTree1);
		genTauDecayTree2->DetermineDecayMode(genTauDecayTree2);
		product.m_genTauTree1DecayMode = (int)genTauDecayTree1->m_decayMode;
		product.m_genTauTree2DecayMode = (int)genTauDecayTree2->m_decayMode;

		genTauDecayTree1->CreateFinalStateProngs(genTauDecayTree1);
		genTauDecayTree2->CreateFinalStateProngs(genTauDecayTree2);
		std::vector<GenParticleDecayTree*> genTauDecayTree1OneProngs = genTauDecayTree1->m_finalStates;
		std::vector<GenParticleDecayTree*> genTauDecayTree2OneProngs = genTauDecayTree2->m_finalStates;
		product.m_genTau1ProngsSize = genTauDecayTree1OneProngs.size();
		product.m_genTau2ProngsSize = genTauDecayTree2OneProngs.size();


		// Defining CPQuantities object to use variables and functions of this class
		CPQuantities cpq;

		// Selection of the right channel for phi and phi*
		if (//(std::abs(genTauDecayTree1->m_genParticle->pdgId) == DefaultValues::pdgIdTau) &&
		    //(std::abs(genTauDecayTree2->m_genParticle->pdgId) == DefaultValues::pdgIdTau) &&
		    (genTauDecayTree1OneProngs.size() != 0) &&
		    (genTauDecayTree2OneProngs.size() != 0))
		{
			// Initialization of charged particles
			KGenParticle* chargedPart1 = genTauDecayTree1OneProngs.at(0)->m_genParticle;
			KGenParticle* chargedPart2 = genTauDecayTree2OneProngs.at(0)->m_genParticle;
			for (unsigned int i = 0; i < genTauDecayTree1OneProngs.size(); ++i)
			{
				if (genTauDecayTree1OneProngs.at(i)->GetCharge() == 1) chargedPart1 = genTauDecayTree1OneProngs.at(i)->m_genParticle;
			}
			for (unsigned int i = 0; i < genTauDecayTree2OneProngs.size(); ++i)
			{
				if (genTauDecayTree2OneProngs.at(i)->GetCharge() == -1) chargedPart2 = genTauDecayTree2OneProngs.at(i)->m_genParticle;
			}

			// Saving the charged particles for  analysis
			// charged1 is the positevely charged tau-daughter
			product.m_genOneProngCharged1 = chargedPart1;
			product.m_genOneProngCharged2 = chargedPart2;
			// Saving Energies of charged particles in tau rest frames
			product.m_genChargedProngEnergies.first = cpq.CalculateChargedProngEnergy(genTauDecayTree1->m_genParticle->p4, chargedPart1->p4);
			product.m_genChargedProngEnergies.second = cpq.CalculateChargedProngEnergy(genTauDecayTree2->m_genParticle->p4, chargedPart2->p4);

			
			// objects to save LVs of charged and neutral pions from rho decays
			RMFLV PionP, Pi0P;
			RMFLV PionM, Pi0M;
			std::vector<RMFLV> rhoP_decay_photons;
			std::vector<RMFLV> rhoM_decay_photons;

			// initialize LVs
			PionP.SetXYZT(-999,-999,-999,-999);
			PionM.SetXYZT(-999,-999,-999,-999);
			Pi0P.SetXYZT(-999,-999,-999,-999);
			Pi0M.SetXYZT(-999,-999,-999,-999);

			// tau1 decaying to rho
			if (genTau1->genDecayMode() == 1){
				// select decays with only 2 final state photons for simplicity
				if (genTauDecayTree1OneProngs.size() == 4){
					for (unsigned int i = 0; i < genTauDecayTree1OneProngs.size(); ++i){
						if(std::abs(genTauDecayTree1OneProngs.at(i)->m_genParticle->pdgId) == DefaultValues::pdgIdPiPlus)
							PionP = genTauDecayTree1OneProngs.at(i)->m_genParticle->p4;

						if(std::abs(genTauDecayTree1OneProngs.at(i)->m_genParticle->pdgId) == DefaultValues::pdgIdGamma)
							rhoP_decay_photons.push_back(genTauDecayTree1OneProngs.at(i)->m_genParticle->p4);
					} // loop over genTau1 prongs
					
					Pi0P = rhoP_decay_photons.at(0) + rhoP_decay_photons.at(1);
				}
			}

			// tau2 decaying to rho
			if (genTau2->genDecayMode() == 1){
				// select decays with only 2 final state photons for simplicity
				if (genTauDecayTree2OneProngs.size() == 4){
					for (unsigned int i = 0; i < genTauDecayTree2OneProngs.size(); ++i){
						if(std::abs(genTauDecayTree2OneProngs.at(i)->m_genParticle->pdgId) == DefaultValues::pdgIdPiPlus)
							PionM = genTauDecayTree2OneProngs.at(i)->m_genParticle->p4;

						if(std::abs(genTauDecayTree2OneProngs.at(i)->m_genParticle->pdgId) == DefaultValues::pdgIdGamma)
							rhoM_decay_photons.push_back(genTauDecayTree2OneProngs.at(i)->m_genParticle->p4);
					} // loop over genTau1 prongs
					
					Pi0M = rhoM_decay_photons.at(0) + rhoM_decay_photons.at(1);
				}
			}

			////////////////
			// rho method //
			////////////////
			
			if (genTau1->genDecayMode() == 1 && genTau2->genDecayMode() == 1){
				if (PionP.X()!=-999 && PionM.X()!=-999 && Pi0P.X()!=-999 && Pi0M.X()!=-999){

					product.m_genPhiStarCP_rho = cpq.CalculatePhiStarCP_rho(PionP, PionM, Pi0P, Pi0M);
					product.m_gen_yTau = cpq.CalculateSpinAnalysingDiscriminant_rho(genTauDecayTree1->m_genParticle->p4, genTauDecayTree2->m_genParticle->p4, PionP, PionM, Pi0P, Pi0M);
					product.m_gen_posyTauL = cpq.CalculateSpinAnalysingDiscriminant_rho(PionP, Pi0P);
					product.m_gen_negyTauL = cpq.CalculateSpinAnalysingDiscriminant_rho(PionM, Pi0M);

				}
			} // tautau --> rhorho channel

			//////////////// rho method



			////////////////
			// IP method //
			////////////////

			// Calculation of Phi and PhiCP
			product.m_genPhiCP = cpq.CalculatePhiCP(product.m_genBosonLV, genTauDecayTree1->m_genParticle->p4, genTauDecayTree2->m_genParticle->p4, chargedPart1->p4, chargedPart2->p4);
			product.m_genPhi = cpq.GetGenPhi();
			product.m_genOCP = cpq.GetGenOCP();
	
			if (product.m_genPV != nullptr){
				// calculate IP vectors of tau daughters
				product.m_genIP1 = cpq.CalculateIPVector(chargedPart1, product.m_genPV);
				product.m_genIP2 = cpq.CalculateIPVector(chargedPart2, product.m_genPV);

				// calculate cosPsi
				product.m_genCosPsiPlus  = cpq.CalculateCosPsi(chargedPart1->p4, product.m_genIP1);
				product.m_genCosPsiMinus = cpq.CalculateCosPsi(chargedPart2->p4, product.m_genIP2);

				// Calculation of Phi* and Phi*CP
				product.m_genPhiStarCP = cpq.CalculatePhiStarCP(chargedPart1->p4, chargedPart2->p4, product.m_genIP1, product.m_genIP2);
				product.m_genPhiStar = cpq.GetGenPhiStar();
				product.m_genOStarCP = cpq.GetGenOStarCP();

				// Calculate phiCP in the lab frame
				product.m_genPhiCPLab = cpq.CalculatePhiCPLab(chargedPart1->p4, product.m_genIP1, product.m_genIP2);


				/////////////////////
				// IP + rho method //
				/////////////////////
				
				// the tau1 decays into a rho
				//if (genTau1->genDecayMode() == 1){

				//	product.m_genPhiStarCPComb = cpq.CalculatePhiStarCPComb(product.genIP2, chargedPart2->p4, 

				//}

				///////////////////// IP+rho method


			} // if genPV exists

			//////////////// IP method





			// Longitudinal correlations studies
			product.m_genZPlus = cpq.CalculateZPlusMinus(product.m_genBosonLV, chargedPart1->p4);
			product.m_genZMinus = cpq.CalculateZPlusMinus(product.m_genBosonLV, chargedPart2->p4);
			product.m_genZs = cpq.CalculateZs(product.m_genZPlus, product.m_genZMinus);
		}
	}
}


std::string GenTauCPProducer::GetProducerId() const
{
	return "GenTauCPProducer";
}

void GenTauCPProducer::Init(setting_type const& settings)
{
	GenTauCPProducerBase::Init(settings);
}

void GenTauCPProducer::Produce(event_type const& event, product_type& product,
                               setting_type const& settings) const
{
	GenTauCPProducerBase::Produce(event, product, settings);
}


std::string GenMatchedTauCPProducer::GetProducerId() const
{
	return "GenMatchedTauCPProducer";
}

void GenMatchedTauCPProducer::Init(setting_type const& settings)
{
	GenTauCPProducerBase::Init(settings);

	// add possible quantities for the lambda ntuples consumers

	// MC-truth SV vertex, obtained by tau daughter 1
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("genSV1x", [](event_type const& event, product_type const& product)
	{
		return ((product.m_genSV1 != nullptr) ? (product.m_genSV1)->x() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("genSV1y", [](event_type const& event, product_type const& product)
	{
		return ((product.m_genSV1 != nullptr) ? (product.m_genSV1)->y() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("genSV1z", [](event_type const& event, product_type const& product)
	{
		return ((product.m_genSV1 != nullptr) ? (product.m_genSV1)->z() : DefaultValues::UndefinedFloat);
	});

	// MC-truth SV vertex, obtained by tau daughter 2
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("genSV2x", [](event_type const& event, product_type const& product)
	{
		return ((product.m_genSV2 != nullptr) ? (product.m_genSV2)->x() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("genSV2y", [](event_type const& event, product_type const& product)
	{
		return ((product.m_genSV2 != nullptr) ? (product.m_genSV2)->y() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("genSV2z", [](event_type const& event, product_type const& product)
	{
		return ((product.m_genSV2 != nullptr) ? (product.m_genSV2)->z() : DefaultValues::UndefinedFloat);
	});

	// charge of leptons
	LambdaNtupleConsumer<HttTypes>::AddIntQuantity("genQ_1", [](event_type const& event, product_type const& product)
	{
		return product.m_flavourOrderedGenLeptons.at(0) ? static_cast<int>(product.m_flavourOrderedGenLeptons.at(0)->charge()) : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddIntQuantity("genQ_2", [](event_type const& event, product_type const& product)
	{
		return product.m_flavourOrderedGenLeptons.at(1) ? static_cast<int>(product.m_flavourOrderedGenLeptons.at(1)->charge()) : DefaultValues::UndefinedDouble;
	});
	

}

void GenMatchedTauCPProducer::Produce(event_type const& event, product_type& product,
                                      setting_type const& settings) const
{

	if(product.m_genBosonLVFound && product.m_genBosonTree.m_daughters.size() > 1){

		GenParticleDecayTree* genTau1;
		GenParticleDecayTree* genTau2;
		genTau1 = &(product.m_genBosonTree.m_daughters.at(0));
		genTau2 = &(product.m_genBosonTree.m_daughters.at(1));
		
		// get the full decay tree and decay mode of the genTaus
		genTau1->CreateFinalStateProngs(genTau1);
		genTau2->CreateFinalStateProngs(genTau2);
		genTau1->DetermineDecayMode(genTau1);
		genTau2->DetermineDecayMode(genTau2);
	
		// initialization of TVector3 objects
		product.m_genIP1.SetXYZ(-999,-999,-999);
		product.m_genIP2.SetXYZ(-999,-999,-999);
	
	
		if (product.m_chargeOrderedGenLeptons.at(0) and product.m_chargeOrderedGenLeptons.at(1)){
			
			KGenParticle* genParticle1 = product.m_flavourOrderedGenLeptons.at(0);
			KGenParticle* genParticle2 = product.m_flavourOrderedGenLeptons.at(1);

			// Defining CPQuantities object to use variables and functions of this class
			CPQuantities cpq;
				

			// if the genLepton is a hadronic tau, we want to take its hadronic daughter
			// for the calculation of the IP vector
			if (std::abs(genParticle1->pdgId) == DefaultValues::pdgIdTau){

				GenParticleDecayTree* genTauTree;
				if (genParticle1->pdgId == genTau1->m_genParticle->pdgId) genTauTree = genTau1;
				else genTauTree = genTau2;
			
				std::vector<GenParticleDecayTree*> prongs = genTauTree->m_finalStates;
				int decayMode = (int)genTauTree->m_decayMode;

				if (decayMode == 4 or decayMode == 7){
					for (unsigned int i=0; i<prongs.size(); ++i){
						if (std::abs(prongs.at(i)->GetCharge()) == 1){
							genParticle1 = prongs.at(i)->m_genParticle;
							break;
						}
					}  // loop over the prongs
				}  // if 1-prong decay mode
				
			}  // if genParticle1 is a tau

			if (std::abs(genParticle2->pdgId) == DefaultValues::pdgIdTau){

				GenParticleDecayTree* genTauTree;
				if (genParticle2->pdgId == genTau1->m_genParticle->pdgId) genTauTree = genTau1;
				else genTauTree = genTau2;
			
				std::vector<GenParticleDecayTree*> prongs = genTauTree->m_finalStates;
				int decayMode = (int)genTauTree->m_decayMode;

				if (decayMode == 4 or decayMode == 7){
					for (unsigned int i=0; i<prongs.size(); ++i){
						if (std::abs(prongs.at(i)->GetCharge()) == 1){
							genParticle2 = prongs.at(i)->m_genParticle;
							break;
						}
					}  // loop over the prongs
				}  // if 1-prong decay mode
				
			}  // if genParticle2 is a tau


			product.m_genSV1 = &genParticle1->vertex;
			product.m_genSV2 = &genParticle2->vertex;
	
			if (product.m_genPV != nullptr){

				product.m_genIP1 = cpq.CalculateIPVector(genParticle1, product.m_genPV);
				product.m_genIP2 = cpq.CalculateIPVector(genParticle2, product.m_genPV);
				
				// calculate phi*cp
				if (genParticle1->charge() > 0){
					product.m_genCosPsiPlus  = cpq.CalculateCosPsi(genParticle1->p4, product.m_genIP1);
					product.m_genCosPsiMinus = cpq.CalculateCosPsi(genParticle2->p4, product.m_genIP2);
					product.m_genPhiStarCP = cpq.CalculatePhiStarCP(genParticle1->p4, genParticle2->p4, product.m_genIP1, product.m_genIP2);
				} else {
					product.m_genCosPsiPlus  = cpq.CalculateCosPsi(genParticle2->p4, product.m_genIP2);
					product.m_genCosPsiMinus = cpq.CalculateCosPsi(genParticle1->p4, product.m_genIP1);
					product.m_genPhiStarCP = cpq.CalculatePhiStarCP(genParticle2->p4, genParticle1->p4, product.m_genIP2, product.m_genIP1);
				}
					
			}
	
		} // if chargeOrderedGenLeptons is a non-empty vector


	} // if product.m_genBosonLVFound && product.m_genBosonTree.m_daughters.size() > 1

}
