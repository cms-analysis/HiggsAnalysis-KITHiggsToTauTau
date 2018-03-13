
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/GenTauCPProducers.h"

#include "Artus/Consumer/interface/LambdaNtupleConsumer.h"
#include "Artus/Utility/interface/DefaultValues.h"
#include "Artus/KappaAnalysis/interface/Utility/GenParticleDecayTree.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/Utility/CPQuantities.h"


void GenTauCPProducerBase::Init(setting_type const& settings, metadata_type& metadata)
{
	ProducerBase<HttTypes>::Init(settings, metadata);

	// add possible quantities for the lambda ntuples consumers

	// MC-truth PV coordinates
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genPVx", [](event_type const& event, product_type const& product)
	{
		return ((product.m_genPV != nullptr) ? (product.m_genPV)->x() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genPVy", [](event_type const& event, product_type const& product)
	{
		return ((product.m_genPV != nullptr) ? (product.m_genPV)->y() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genPVz", [](event_type const& event, product_type const& product)
	{
		return ((product.m_genPV != nullptr) ? (product.m_genPV)->z() : DefaultValues::UndefinedFloat);
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genPhiStarCP", [](event_type const& event, product_type const& product)
	{
		return product.m_genPhiStarCP;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genPhiStarCP_rho", [](event_type const& event, product_type const& product)
	{
		return product.m_genPhiStarCP_rho;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genPhiStarCPComb", [](event_type const& event, product_type const& product)
	{
		return product.m_genPhiStarCPComb;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "gen_posyTauL", [](event_type const& event, product_type const& product)
	{
		return product.m_gen_posyTauL;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "gen_negyTauL", [](event_type const& event, product_type const& product)
	{
		return product.m_gen_negyTauL;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "gen_yTau", [](event_type const& event, product_type const& product)
	{
		return product.m_gen_yTau;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genPhiCP", [](event_type const& event, product_type const& product)
	{
		return product.m_genPhiCP;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genPhiCPLab", [](event_type const& event, product_type const& product)
	{
		return product.m_genPhiCPLab;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genPhiCP_rho", [](event_type const& event, product_type const& product)
	{
		return product.m_genPhiCP_rho;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genPhiStar", [](event_type const& event, product_type const& product)
	{
		return product.m_genPhiStar;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genOStarCP", [](event_type const& event, product_type const& product)
	{
		return product.m_genOStarCP;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genPhiStar_rho", [](event_type const& event, product_type const& product)
	{
		return product.m_genPhiStar_rho;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genPhi", [](event_type const& event, product_type const& product)
	{
		return product.m_genPhi;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genOCP", [](event_type const& event, product_type const& product)
	{
		return product.m_genOCP;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genPhi_rho", [](event_type const& event, product_type const& product)
	{
		return product.m_genPhi_rho;
	});

	// energy of the charged prong particles in the tau rest frame
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "TauPProngEnergy", [](event_type const& event, product_type const& product)
	{
		return product.m_genChargedProngEnergies.first;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "TauMProngEnergy", [](event_type const& event, product_type const& product)
	{
		return product.m_genChargedProngEnergies.second;
	});

	// charged particles of a one-prong tau
	// FIXME these two variables could be removed ???
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "Tau1OneProngsSize", [](event_type const& event, product_type const& product)
	{
		return product.m_genTau1ProngsSize;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "Tau2OneProngsSize", [](event_type const& event, product_type const& product)
	{
		return product.m_genTau2ProngsSize;
	});

	// decay mode of the taus from KGenTau
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "Tau1DecayMode", [](event_type const& event, product_type const& product)
	{
		return product.m_genTau1DecayMode;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "Tau2DecayMode", [](event_type const& event, product_type const& product)
	{
		return product.m_genTau2DecayMode;
	});
	// decay mode of the taus from GenParticleDecayTree
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "TauTree1DecayMode", [](event_type const& event, product_type const& product)
	{
		return product.m_genTauTree1DecayMode;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "TauTree2DecayMode", [](event_type const& event, product_type const& product)
	{
		return product.m_genTauTree2DecayMode;
	});
	
	// MC-truth IP vectors
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genIP1mag", [](event_type const& event, product_type const& product)
	{
		return (((product.m_genIP1).x() != -999) ? ( sqrt( (product.m_genIP1).x()*(product.m_genIP1).x() + (product.m_genIP1).y()*(product.m_genIP1).y() + (product.m_genIP1).z()*(product.m_genIP1).z() ) ) : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genIP1x", [](event_type const& event, product_type const& product)
	{
		return ((&product.m_genIP1 != nullptr) ? (product.m_genIP1).x() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genIP1y", [](event_type const& event, product_type const& product)
	{
		return ((&product.m_genIP1 != nullptr) ? (product.m_genIP1).y() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genIP1z", [](event_type const& event, product_type const& product)
	{
		return ((&product.m_genIP1 != nullptr) ? (product.m_genIP1).z() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genIP2mag", [](event_type const& event, product_type const& product)
	{
		return (((product.m_genIP2).x() != -999) ? ( sqrt( (product.m_genIP2).x()*(product.m_genIP2).x() + (product.m_genIP2).y()*(product.m_genIP2).y() + (product.m_genIP2).z()*(product.m_genIP2).z() ) ) : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genIP2x", [](event_type const& event, product_type const& product)
	{
		return ((&product.m_genIP2 != nullptr) ? (product.m_genIP2).x() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genIP2y", [](event_type const& event, product_type const& product)
	{
		return ((&product.m_genIP2 != nullptr) ? (product.m_genIP2).y() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genIP2z", [](event_type const& event, product_type const& product)
	{
		return ((&product.m_genIP2 != nullptr) ? (product.m_genIP2).z() : DefaultValues::UndefinedFloat);
	});

	// cosPsi
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genCosPsiPlus", [](event_type const& event, product_type const& product)
	{
		return product.m_genCosPsiPlus;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genCosPsiMinus", [](event_type const& event, product_type const& product)
	{
		return product.m_genCosPsiMinus;
	});

	// properties of the charged particles from tau decays
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "OneProngChargedPart1PdgId", [](event_type const& event, product_type const& product)
	{
		return product.m_genOneProngCharged1 != nullptr ? product.m_genOneProngCharged1->pdgId : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "OneProngChargedPart1Pt", [](event_type const& event, product_type const& product)
	{
		return product.m_genOneProngCharged1 != nullptr ? product.m_genOneProngCharged1->p4.Pt() : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "OneProngChargedPart1Pz", [](event_type const& event, product_type const& product)
	{
		return product.m_genOneProngCharged1 != nullptr ? product.m_genOneProngCharged1->p4.Pz() : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "OneProngChargedPart1Eta", [](event_type const& event, product_type const& product)
	{
		return product.m_genOneProngCharged1 != nullptr ? product.m_genOneProngCharged1->p4.Eta() : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "OneProngChargedPart1Phi", [](event_type const& event, product_type const& product)
	{
		return product.m_genOneProngCharged1 != nullptr ? product.m_genOneProngCharged1->p4.Phi() : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "OneProngChargedPart1Mass", [](event_type const& event, product_type const& product)
	{
		return product.m_genOneProngCharged1 != nullptr ? product.m_genOneProngCharged1->p4.mass() : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "OneProngChargedPart1Energy", [](event_type const& event, product_type const& product)
	{
		return product.m_genOneProngCharged1 != nullptr ? product.m_genOneProngCharged1->p4.E() : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "OneProngChargedPart2PdgId", [](event_type const& event, product_type const& product)
	{
		return product.m_genOneProngCharged2 != nullptr ? product.m_genOneProngCharged2->pdgId : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "OneProngChargedPart2Pt", [](event_type const& event, product_type const& product)
	{
		return product.m_genOneProngCharged2 != nullptr ? product.m_genOneProngCharged2->p4.Pt() : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "OneProngChargedPart2Pz", [](event_type const& event, product_type const& product)
	{
		return product.m_genOneProngCharged2 != nullptr ? product.m_genOneProngCharged2->p4.Pz() : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "OneProngChargedPart2Eta", [](event_type const& event, product_type const& product)
	{
		return product.m_genOneProngCharged2 != nullptr ? product.m_genOneProngCharged2->p4.Eta() : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "OneProngChargedPart2Phi", [](event_type const& event, product_type const& product)
	{
		return product.m_genOneProngCharged2 != nullptr ? product.m_genOneProngCharged2->p4.Phi() : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "OneProngChargedPart2Mass", [](event_type const& event, product_type const& product)
	{
		return product.m_genOneProngCharged2 != nullptr ? product.m_genOneProngCharged2->p4.mass() : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "OneProngChargedPart2Energy", [](event_type const& event, product_type const& product)
	{
		return product.m_genOneProngCharged2 != nullptr ? product.m_genOneProngCharged2->p4.E() : DefaultValues::UndefinedDouble;
	});

	// longitudinal spin correlations
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genZPlus", [](event_type const& event, product_type const& product)
	{
		return product.m_genZPlus;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genZMinus", [](event_type const& event, product_type const& product)
	{
		return product.m_genZMinus;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genZs", [](event_type const& event, product_type const& product)
	{
		return product.m_genZs;
	});
}

void GenTauCPProducerBase::Produce(event_type const& event, product_type& product,
                                   setting_type const& settings, metadata_type const& metadata) const
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
					product.m_gen_posyTauL = cpq.CalculateSpinAnalysingDiscriminant_rho(PionP, Pi0P);
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
					product.m_gen_negyTauL = cpq.CalculateSpinAnalysingDiscriminant_rho(PionM, Pi0M);
				}
			}

			////////////////
			// rho method //
			////////////////
			
			if (genTau1->genDecayMode() == 1 && genTau2->genDecayMode() == 1){
				if (PionP.X()!=-999 && PionM.X()!=-999 && Pi0P.X()!=-999 && Pi0M.X()!=-999){

					product.m_genPhiStarCP_rho = cpq.CalculatePhiStarCP_rho(PionP, PionM, Pi0P, Pi0M);
					product.m_gen_yTau = cpq.CalculateSpinAnalysingDiscriminant_rho(genTauDecayTree1->m_genParticle->p4, genTauDecayTree2->m_genParticle->p4, PionP, PionM, Pi0P, Pi0M);
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
				product.m_genIP1 = cpq.CalculateShortestDistance(chargedPart1, product.m_genPV);
				product.m_genIP2 = cpq.CalculateShortestDistance(chargedPart2, product.m_genPV);

				// calculate cosPsi
				product.m_genCosPsiPlus  = cpq.CalculateCosPsi(chargedPart1->p4, product.m_genIP1);
				product.m_genCosPsiMinus = cpq.CalculateCosPsi(chargedPart2->p4, product.m_genIP2);

				// Calculation of Phi* and Phi*CP
				product.m_genPhiStarCP = cpq.CalculatePhiStarCP(chargedPart1->p4, chargedPart2->p4, product.m_genIP1, product.m_genIP2, "gen");
				product.m_genPhiStar = cpq.GetGenPhiStar();
				product.m_genOStarCP = cpq.GetGenOStarCP();

				// Calculate phiCP in the lab frame
				product.m_genPhiCPLab = cpq.CalculatePhiCPLab(chargedPart1->p4, product.m_genIP1, product.m_genIP2);


				/////////////////////
				// IP + rho method //
				/////////////////////
				
				// the tau1 decays into a rho
				if (genTau1->genDecayMode()==1 && genTau2->genDecayMode()!=1)
					product.m_genPhiStarCPComb = cpq.CalculatePhiStarCPComb(product.m_genIP2, chargedPart2->p4, PionP, Pi0P, (int)chargedPart2->charge());

				// the tau2 decays into a rho
				if (genTau1->genDecayMode()!=1 && genTau2->genDecayMode()==1)
					product.m_genPhiStarCPComb = cpq.CalculatePhiStarCPComb(product.m_genIP1, chargedPart1->p4, PionM, Pi0M, (int)chargedPart1->charge());

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

void GenTauCPProducer::Init(setting_type const& settings, metadata_type& metadata)
{
	GenTauCPProducerBase::Init(settings, metadata);
}

void GenTauCPProducer::Produce(event_type const& event, product_type& product,
                               setting_type const& settings, metadata_type const& metadata) const
{
	GenTauCPProducerBase::Produce(event, product, settings, metadata);
}


std::string GenMatchedTauCPProducer::GetProducerId() const
{
	return "GenMatchedTauCPProducer";
}

void GenMatchedTauCPProducer::Init(setting_type const& settings, metadata_type& metadata)
{
	GenTauCPProducerBase::Init(settings, metadata);

	// add possible quantities for the lambda ntuples consumers

	// MC-truth SV vertex, obtained by tau daughter 1
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genSV1x", [](event_type const& event, product_type const& product)
	{
		return ((product.m_genSV1 != nullptr) ? (product.m_genSV1)->x() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genSV1y", [](event_type const& event, product_type const& product)
	{
		return ((product.m_genSV1 != nullptr) ? (product.m_genSV1)->y() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genSV1z", [](event_type const& event, product_type const& product)
	{
		return ((product.m_genSV1 != nullptr) ? (product.m_genSV1)->z() : DefaultValues::UndefinedFloat);
	});

	// MC-truth SV vertex, obtained by tau daughter 2
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genSV2x", [](event_type const& event, product_type const& product)
	{
		return ((product.m_genSV2 != nullptr) ? (product.m_genSV2)->x() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genSV2y", [](event_type const& event, product_type const& product)
	{
		return ((product.m_genSV2 != nullptr) ? (product.m_genSV2)->y() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genSV2z", [](event_type const& event, product_type const& product)
	{
		return ((product.m_genSV2 != nullptr) ? (product.m_genSV2)->z() : DefaultValues::UndefinedFloat);
	});

	// transverse impact parameter d0
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genD01", [](event_type const& event, product_type const& product)
	{
		return product.m_genD01;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genD02", [](event_type const& event, product_type const& product)
	{
		return product.m_genD02;
	});
	
	// charge of leptons
	LambdaNtupleConsumer<HttTypes>::AddIntQuantity(metadata, "genQ_1", [](event_type const& event, product_type const& product)
	{
		return product.m_flavourOrderedGenLeptons.at(0) ? static_cast<int>(product.m_flavourOrderedGenLeptons.at(0)->charge()) : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddIntQuantity(metadata, "genQ_2", [](event_type const& event, product_type const& product)
	{
		return product.m_flavourOrderedGenLeptons.at(1) ? static_cast<int>(product.m_flavourOrderedGenLeptons.at(1)->charge()) : DefaultValues::UndefinedDouble;
	});
	

}

void GenMatchedTauCPProducer::Produce(event_type const& event, product_type& product,
                                      setting_type const& settings, metadata_type const& metadata) const
{

	if(product.m_genBosonLVFound && product.m_genBosonTree.m_daughters.size() > 1){

		// initialization
		KGenParticle* genParticle1 = nullptr;
		KGenParticle* genParticle2 = nullptr;
		GenParticleDecayTree* genTauDecayTree1 = nullptr; // necessary to access the tau prongs
		GenParticleDecayTree* genTauDecayTree2 = nullptr; // necessary to access the tau prongs
		KGenTau* genTau1 = nullptr; // necessary to access the tau decay mode
		KGenTau* genTau2 = nullptr; // necessary to access the tau decay mode
		product.m_genIP1.SetXYZ(-999,-999,-999);
		product.m_genIP2.SetXYZ(-999,-999,-999);
		// object for rho method
		RMFLV pi1, pi01, pi2, pi02;
		std::vector<RMFLV> rho1DecayPhotons, rho2DecayPhotons;
		pi1.SetXYZT(-999,-999,-999,-999);
		pi01.SetXYZT(-999,-999,-999,-999);
		pi2.SetXYZT(-999,-999,-999,-999);
		pi02.SetXYZT(-999,-999,-999,-999);
		double genY1L = DefaultValues::UndefinedDouble;
		double genY2L = DefaultValues::UndefinedDouble;
		// auxiliary variables: charged ordered
		// chargedPart1 = +, chargedPart2 = -
		KGenParticle* chargedPart1 = nullptr;
		KGenParticle* chargedPart2 = nullptr;
		TVector3 IPPlus, IPMinus;
		IPPlus.SetXYZ(-999,-999,-999);
		IPMinus.SetXYZ(-999,-999,-999);

		// defining object of type CPQuantities to access variables and functions of this class
		CPQuantities cpq;

		// access vectors of gen leptons matched to reco leptons
		if (product.m_flavourOrderedGenLeptons.at(0) and product.m_flavourOrderedGenLeptons.at(1)){
			genParticle1 = product.m_flavourOrderedGenLeptons.at(0);
			genParticle2 = product.m_flavourOrderedGenLeptons.at(1);

			// full decay tree of the taus
			genTauDecayTree1 = &(product.m_genBosonTree.m_daughters.at(0));
			genTauDecayTree2 = &(product.m_genBosonTree.m_daughters.at(1));
			genTau1 = SafeMap::GetWithDefault(product.m_validGenTausMap, genTauDecayTree1->m_genParticle, static_cast<KGenTau*>(nullptr));
			genTau2 = SafeMap::GetWithDefault(product.m_validGenTausMap, genTauDecayTree2->m_genParticle, static_cast<KGenTau*>(nullptr));

			// if the genLepton is a hadronic tau, we want to take its hadronic daughter
			// for the calculation of the IP vector
			if (std::abs(genParticle1->pdgId) == DefaultValues::pdgIdTau){
				GenParticleDecayTree* gentautree = nullptr;
				KGenTau* gentau = nullptr;
				if (genParticle1->pdgId == genTauDecayTree1->m_genParticle->pdgId){
					gentautree = genTauDecayTree1;
					gentau = genTau1;
				} else {
					gentautree = genTauDecayTree2;
					gentau = genTau2;
				}
				int decaymode = gentau->genDecayMode();
				product.m_genTau1DecayMode = decaymode;
				product.m_genTauTree1DecayMode = (int)gentautree->m_decayMode;
			
				std::vector<GenParticleDecayTree*> prongs = gentautree->m_finalStates;
				product.m_genTau1ProngsSize = prongs.size();

				// hadronic decay mode
				if (decaymode >= 0){
					for (unsigned int i=0; i<prongs.size(); ++i){
						if (std::abs(prongs.at(i)->GetCharge())==1){
							genParticle1 = prongs.at(i)->m_genParticle;
							break;
						}
					} // loop over tau prongs

						if (decaymode == 1){
							// consider only case tau->rho nu-> pi gamma gamma nu
							if (prongs.size() == 4){
								for (unsigned int i=0; i<prongs.size(); ++i){
									if (std::abs(prongs.at(i)->m_genParticle->pdgId) == DefaultValues::pdgIdPiPlus)
										pi1 = prongs.at(i)->m_genParticle->p4;
									if (std::abs(prongs.at(i)->m_genParticle->pdgId) == DefaultValues::pdgIdGamma)
										rho1DecayPhotons.push_back(prongs.at(i)->m_genParticle->p4);
								} // loop over tau prongs
								pi01 = rho1DecayPhotons.at(0) + rho1DecayPhotons.at(1);
								genY1L = cpq.CalculateSpinAnalysingDiscriminant_rho(pi1, pi01);
							}
						} // rho decay

				} // if hadronic decay mode
			}  // if genParticle1 is a tau

			if (std::abs(genParticle2->pdgId) == DefaultValues::pdgIdTau){
				GenParticleDecayTree* gentautree = nullptr;
				KGenTau* gentau = nullptr;
				if (genParticle2->pdgId == genTauDecayTree1->m_genParticle->pdgId){
					gentautree = genTauDecayTree1;
					gentau = genTau1;
				} else {
					gentautree = genTauDecayTree2;
					gentau = genTau2;
				}
				int decaymode = gentau->genDecayMode();
				product.m_genTau2DecayMode = decaymode;
				product.m_genTauTree2DecayMode = (int)gentautree->m_decayMode;
			
				std::vector<GenParticleDecayTree*> prongs = gentautree->m_finalStates;
				product.m_genTau2ProngsSize = prongs.size();

				// hadronic decay mode
				if (decaymode >= 0){
					for (unsigned int i=0; i<prongs.size(); ++i){
						if (std::abs(prongs.at(i)->GetCharge())==1){
							genParticle2 = prongs.at(i)->m_genParticle;
							break;
						}
					} // loop over tau prongs

						if (decaymode == 1){
							// consider only case tau->rho nu-> pi gamma gamma nu
							if (prongs.size() == 4){
								for (unsigned int i=0; i<prongs.size(); ++i){
									if (std::abs(prongs.at(i)->m_genParticle->pdgId) == DefaultValues::pdgIdPiPlus)
										pi2 = prongs.at(i)->m_genParticle->p4;
									if (std::abs(prongs.at(i)->m_genParticle->pdgId) == DefaultValues::pdgIdGamma)
										rho2DecayPhotons.push_back(prongs.at(i)->m_genParticle->p4);
								} // loop over tau prongs
								pi02 = rho2DecayPhotons.at(0) + rho2DecayPhotons.at(1);
								genY2L = cpq.CalculateSpinAnalysingDiscriminant_rho(pi2, pi02);
							}
						} // rho decay

				} // if hadronic decay mode
			}  // if genParticle2 is a tau
			
			// ==================
			// === rho method ===
			// ==================
			if (genTau1 != nullptr && genTau2 != nullptr){
				if (genParticle1->charge() > 0){
					product.m_gen_posyTauL = genY1L;
					product.m_gen_negyTauL = genY2L;

					if (genTau1->genDecayMode()==1 && genTau2->genDecayMode()==1){
						if (pi1.X()!=-999 && pi01.X()!=-999 && pi2.X()!=-999 && pi02.X()!=-999)
							product.m_genPhiStarCP_rho = cpq.CalculatePhiStarCP_rho(pi1, pi2, pi01, pi02);
					}
				} else {
					product.m_gen_posyTauL = genY2L;
					product.m_gen_negyTauL = genY1L;
					if (genTau1->genDecayMode()==1 && genTau2->genDecayMode()==1){
						if (pi1.X()!=-999 && pi01.X()!=-999 && pi2.X()!=-999 && pi02.X()!=-999)
							product.m_genPhiStarCP_rho = cpq.CalculatePhiStarCP_rho(pi2, pi1, pi02, pi01);
					}
				}
			}
			///////////////////////////// rho method
			
			// =================
			// === ip method ===
			// =================
			product.m_genSV1 = &genParticle1->vertex;
			product.m_genSV2 = &genParticle2->vertex;
	
			if (product.m_genPV != nullptr){

				product.m_genD01 = (1 / genParticle1->p4.Pt()) 
									* ( -( (product.m_genSV1)->x() - (product.m_genPV)->x() )*genParticle1->p4.Py()
									+ ( (product.m_genSV1)->y() - (product.m_genPV)->y() )*genParticle1->p4.Px() );
				product.m_genD02 = (1 / genParticle2->p4.Pt()) 
									* ( -( (product.m_genSV2)->x() - (product.m_genPV)->x() )*genParticle2->p4.Py()
									+ ( (product.m_genSV2)->y() - (product.m_genPV)->y() )*genParticle2->p4.Px() );

				product.m_genIP1 = cpq.CalculateShortestDistance(genParticle1, product.m_genPV);
				product.m_genIP2 = cpq.CalculateShortestDistance(genParticle2, product.m_genPV);
				
				// calculate phi*cp
				if (genParticle1->charge() > 0){
					IPPlus = product.m_genIP1;
					IPMinus = product.m_genIP2;
					chargedPart1 = genParticle1;
					chargedPart2 = genParticle2;
				} else {
					IPPlus = product.m_genIP2;
					IPMinus = product.m_genIP1;
					chargedPart1 = genParticle2;
					chargedPart2 = genParticle1;
				}

				product.m_genCosPsiPlus = cpq.CalculateCosPsi(chargedPart1->p4, IPPlus);
				product.m_genCosPsiMinus = cpq.CalculateCosPsi(chargedPart2->p4, IPMinus);

				product.m_genPhiStarCP = cpq.CalculatePhiStarCP(chargedPart1->p4, chargedPart2->p4, IPPlus, IPMinus, "gen");
				///////////////////////////// ip method
				

				// ===================
				// === comb method ===
				// ===================
				if (genTau1 != nullptr && genTau2 != nullptr){
					if (genTau1->genDecayMode()==1 && genTau2->genDecayMode()!=1)
						product.m_genPhiStarCPComb = cpq.CalculatePhiStarCPComb(product.m_genIP2, genParticle2->p4, pi1, pi01, genParticle2->charge());
					if (genTau1->genDecayMode()!=1 && genTau2->genDecayMode()==1)
						product.m_genPhiStarCPComb = cpq.CalculatePhiStarCPComb(product.m_genIP1, genParticle1->p4, pi2, pi02, genParticle1->charge());
				}
			///////////////////////////// comb method

			} // if genPV != nullptr


		} // if flavourOrderedGenLeptons is a non-empty vector

	} // if product.m_genBosonLVFound && product.m_genBosonTree.m_daughters.size() > 1

}
