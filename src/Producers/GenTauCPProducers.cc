
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/GenTauCPProducers.h"

#include "Artus/Consumer/interface/LambdaNtupleConsumer.h"
#include "Artus/Utility/interface/DefaultValues.h"
#include "Artus/KappaAnalysis/interface/Utility/GenParticleDecayTree.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Utility/CPQuantities.h"
#include "TauPolSoftware/TauDecaysInterface/interface/SCalculator.h"

GenTauCPProducerBase::GenTauCPProducerBase(
		std::string name
) :
	m_name(name)
{
}

void GenTauCPProducerBase::Init(setting_type const& settings, metadata_type& metadata)
{
	ProducerBase<HttTypes>::Init(settings, metadata);

	// add possible quantities for the lambda ntuples consumers

	// MC-truth PV coordinates
	LambdaNtupleConsumer<HttTypes>::AddRMPointQuantity(metadata, "genPV", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return ((product.m_genPV != nullptr) ? *product.m_genPV : DefaultValues::UndefinedRMPoint);
		return event.m_vertexSummary->pv.position;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, m_name+"PhiStarCP", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_genPhiStarCP;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, m_name+"PhiStarCPRho", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_genPhiStarCPRho;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, m_name+"PhiStarCPComb", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_genPhiStarCPComb;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, m_name+"PhiStarCPCombMerged", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_genPhiStarCPCombMerged;
	});


	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, m_name+"_posyTauL", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_gen_posyTauL;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, m_name+"_negyTauL", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_gen_negyTauL;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, m_name+"_yTau", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_gen_yTau;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, m_name+"PhiCP", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_genPhiCP;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, m_name+"PhiCPLab", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_genPhiCPLab;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, m_name+"PhiCPRho", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_genPhiCPRho;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, m_name+"PhiStar", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_genPhiStar;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, m_name+"OStarCP", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_genOStarCP;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, m_name+"PhiStarRho", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_genPhiStarRho;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, m_name+"Phi", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_genPhi;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, m_name+"OCP", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_genOCP;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, m_name+"PhiRho", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_genPhiRho;
	});

	// energy of the charged prong particles in the tau rest frame
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genTauPProngEnergy", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_genChargedProngEnergies.first;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genTauMProngEnergy", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_genChargedProngEnergies.second;
	});

	// charged particles of a one-prong tau
	// FIXME these two variables could be removed ???
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genTau1OneProngsSize", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_genTau1ProngsSize;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genTau2OneProngsSize", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_genTau2ProngsSize;
	});

	// decay mode of the taus from KGenTau
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genTau1DecayMode", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_genTau1DecayMode;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genTau2DecayMode", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_genTau2DecayMode;
	});
	// decay mode of the taus from GenParticleDecayTree
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genTauTree1DecayMode", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_genTauTree1DecayMode;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genTauTree2DecayMode", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_genTauTree2DecayMode;
	});

	// MC-truth IP vectors
	LambdaNtupleConsumer<HttTypes>::AddRMPointQuantity(metadata, "genIP1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return ((&product.m_genIP1 != nullptr) ? RMPoint( (product.m_genIP1).x(), (product.m_genIP1).y(), (product.m_genIP1).z() ) : DefaultValues::UndefinedRMPoint);
	});
	LambdaNtupleConsumer<HttTypes>::AddRMPointQuantity(metadata, "genIP2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return ((&product.m_genIP2 != nullptr) ? RMPoint( (product.m_genIP2).x(), (product.m_genIP2).y(), (product.m_genIP2).z() ) : DefaultValues::UndefinedRMPoint);
	});

	// cosPsi
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, m_name+"CosPsiPlus", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_genCosPsiPlus;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, m_name+"CosPsiMinus", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_genCosPsiMinus;
	});

	// properties of the charged particles from tau decays
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genOneProngChargedPart1PdgId", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_genOneProngCharged1 != nullptr ? product.m_genOneProngCharged1->pdgId : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genOneProngChargedPart1Pt", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_genOneProngCharged1 != nullptr ? product.m_genOneProngCharged1->p4.Pt() : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genOneProngChargedPart1Pz", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_genOneProngCharged1 != nullptr ? product.m_genOneProngCharged1->p4.Pz() : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genOneProngChargedPart1Eta", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_genOneProngCharged1 != nullptr ? product.m_genOneProngCharged1->p4.Eta() : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genOneProngChargedPart1Phi", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_genOneProngCharged1 != nullptr ? product.m_genOneProngCharged1->p4.Phi() : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genOneProngChargedPart1Mass", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_genOneProngCharged1 != nullptr ? product.m_genOneProngCharged1->p4.mass() : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genOneProngChargedPart1Energy", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_genOneProngCharged1 != nullptr ? product.m_genOneProngCharged1->p4.E() : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genOneProngChargedPart2PdgId", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_genOneProngCharged2 != nullptr ? product.m_genOneProngCharged2->pdgId : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genOneProngChargedPart2Pt", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_genOneProngCharged2 != nullptr ? product.m_genOneProngCharged2->p4.Pt() : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genOneProngChargedPart2Pz", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_genOneProngCharged2 != nullptr ? product.m_genOneProngCharged2->p4.Pz() : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genOneProngChargedPart2Eta", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_genOneProngCharged2 != nullptr ? product.m_genOneProngCharged2->p4.Eta() : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genOneProngChargedPart2Phi", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_genOneProngCharged2 != nullptr ? product.m_genOneProngCharged2->p4.Phi() : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genOneProngChargedPart2Mass", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_genOneProngCharged2 != nullptr ? product.m_genOneProngCharged2->p4.mass() : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genOneProngChargedPart2Energy", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_genOneProngCharged2 != nullptr ? product.m_genOneProngCharged2->p4.E() : DefaultValues::UndefinedDouble;
	});

	// longitudinal spin correlations
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genZPlus", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_genZPlus;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genZMinus", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_genZMinus;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genZs", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
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
					product.m_gen_posyTauL = cpq.CalculateSpinAnalysingDiscriminantRho(PionP, Pi0P);
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
					product.m_gen_negyTauL = cpq.CalculateSpinAnalysingDiscriminantRho(PionM, Pi0M);
				}
			}

			////////////////
			// rho method //
			////////////////

			if (genTau1->genDecayMode() == 1 && genTau2->genDecayMode() == 1){
				if (PionP.X()!=-999 && PionM.X()!=-999 && Pi0P.X()!=-999 && Pi0M.X()!=-999){

					product.m_genPhiStarCPRho = cpq.CalculatePhiStarCPRho(PionP, PionM, Pi0P, Pi0M);
					product.m_gen_yTau = cpq.CalculateSpinAnalysingDiscriminantRho(genTauDecayTree1->m_genParticle->p4, genTauDecayTree2->m_genParticle->p4, PionP, PionM, Pi0P, Pi0M);
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

GenTauCPProducer::GenTauCPProducer() :
	GenTauCPProducerBase(
			"gen"
	)
{
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


GenMatchedTauCPProducer::GenMatchedTauCPProducer() :
	GenTauCPProducerBase(
			"genMatched"
	)
{
}

std::string GenMatchedTauCPProducer::GetProducerId() const
{
	return "GenMatchedTauCPProducer";
}

void GenMatchedTauCPProducer::Init(setting_type const& settings, metadata_type& metadata)
{
	GenTauCPProducerBase::Init(settings, metadata);
	m_useMVADecayModes = settings.GetGEFUseMVADecayModes();
	// add possible quantities for the lambda ntuples consumers

	// MC-truth SV vertex, obtained by tau daughter 1
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genSV1x", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return ((product.m_genSV1 != nullptr) ? (product.m_genSV1)->x() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genSV1y", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return ((product.m_genSV1 != nullptr) ? (product.m_genSV1)->y() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genSV1z", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return ((product.m_genSV1 != nullptr) ? (product.m_genSV1)->z() : DefaultValues::UndefinedFloat);
	});

	// MC-truth SV vertex, obtained by tau daughter 2
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genSV2x", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return ((product.m_genSV2 != nullptr) ? (product.m_genSV2)->x() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genSV2y", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return ((product.m_genSV2 != nullptr) ? (product.m_genSV2)->y() : DefaultValues::UndefinedFloat);
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genSV2z", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return ((product.m_genSV2 != nullptr) ? (product.m_genSV2)->z() : DefaultValues::UndefinedFloat);
	});

	// transverse impact parameter d0
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genD01", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_genD01;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genD02", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_genD02;
	});

	// charge of leptons
	LambdaNtupleConsumer<HttTypes>::AddIntQuantity(metadata, "genQ_1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_flavourOrderedGenLeptons.at(0) ? static_cast<int>(product.m_flavourOrderedGenLeptons.at(0)->charge()) : DefaultValues::UndefinedDouble;
	});
	LambdaNtupleConsumer<HttTypes>::AddIntQuantity(metadata, "genQ_2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_flavourOrderedGenLeptons.at(1) ? static_cast<int>(product.m_flavourOrderedGenLeptons.at(1)->charge()) : DefaultValues::UndefinedDouble;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genMatchedPhiStarCPPolVecTau1Tau2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_genMatchedPhiStarCPPolVecTau1Tau2;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genMatchedPhiStarCPPolVecTau1VisTau2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_genMatchedPhiStarCPPolVecTau1VisTau2;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genMatchedPhiStarCPPolVecTau1Tau2Vis", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_genMatchedPhiStarCPPolVecTau1Tau2Vis;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genMatchedPhiStarCPPolVecTau1VisTau2Vis", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_genMatchedPhiStarCPPolVecTau1VisTau2Vis;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genMatchedPhiStarCPPolVecTau1Tau2PiSSFromRho", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_genMatchedPhiStarCPPolVecTau1Tau2PiSSFromRho;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genMatchedPhiStarCPPolVecTau1Tau2PiHighPt", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_genMatchedPhiStarCPPolVecTau1Tau2PiHighPt;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genMatchedPhiStarCPPolVecTau1VisTau2PiSSFromRho", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_genMatchedPhiStarCPPolVecTau1VisTau2PiSSFromRho;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genMatchedPhiStarCPPolVecTau1VisTau2PiHighPt", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_genMatchedPhiStarCPPolVecTau1VisTau2PiHighPt;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genMatchedPhiStarCPPolVecCombTau1Tau2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_genMatchedPhiStarCPPolVecCombTau1Tau2;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genMatchedPhiStarCPPolVecCombTau1VisTau2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_genMatchedPhiStarCPPolVecCombTau1VisTau2;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genMatchedPhiStarCPPolVecCombTau1Tau2Vis", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_genMatchedPhiStarCPPolVecCombTau1Tau2Vis;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genMatchedPhiStarCPPolVecCombTau1VisTau2Vis", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_genMatchedPhiStarCPPolVecCombTau1VisTau2Vis;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genMatchedPhiStarCPPolVecCombTau1Tau2PiSSFromRho", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_genMatchedPhiStarCPPolVecCombTau1Tau2PiSSFromRho;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genMatchedPhiStarCPPolVecCombTau1Tau2PiHighPt", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_genMatchedPhiStarCPPolVecCombTau1Tau2PiHighPt;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genMatchedPhiStarCPPolVecCombTau1VisTau2PiSSFromRho", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_genMatchedPhiStarCPPolVecCombTau1VisTau2PiSSFromRho;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genMatchedPhiStarCPPolVecCombTau1VisTau2PiHighPt", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_genMatchedPhiStarCPPolVecCombTau1VisTau2PiHighPt;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genMatchedPhiStarCPPolVecTauOneProngTauA1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_genMatchedPhiStarCPPolVecTauOneProngTauA1;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genMatchedPhiStarCPPolVecOneProngTauA1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_genMatchedPhiStarCPPolVecOneProngTauA1;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genMatchedPhiStarCPPolVecTauOneProngA1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_genMatchedPhiStarCPPolVecTauOneProngA1;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genMatchedPhiStarCPPolVecOneProngA1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_genMatchedPhiStarCPPolVecOneProngA1;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genMatchedPhiStarCPPolVecTauOneProngA1PiSSFromRho", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_genMatchedPhiStarCPPolVecTauOneProngA1PiSSFromRho;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genMatchedPhiStarCPPolVecTauOneProngA1PiHighPt", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_genMatchedPhiStarCPPolVecTauOneProngA1PiHighPt;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genMatchedPhiStarCPPolVecOneProngA1PiSSFromRho", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_genMatchedPhiStarCPPolVecOneProngA1PiSSFromRho;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genMatchedPhiStarCPPolVecOneProngA1PiHighPt", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_genMatchedPhiStarCPPolVecOneProngA1PiHighPt;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genMatchedPhiStarCPPolVecCombTauOneProngTauA1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_genMatchedPhiStarCPPolVecCombTauOneProngTauA1;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genMatchedPhiStarCPPolVecCombOneProngTauA1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_genMatchedPhiStarCPPolVecCombOneProngTauA1;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genMatchedPhiStarCPPolVecCombTauOneProngA1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_genMatchedPhiStarCPPolVecCombTauOneProngA1;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genMatchedPhiStarCPPolVecCombOneProngA1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_genMatchedPhiStarCPPolVecCombOneProngA1;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genMatchedPhiStarCPPolVecCombTauOneProngA1PiSSFromRho", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_genMatchedPhiStarCPPolVecCombTauOneProngA1PiSSFromRho;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genMatchedPhiStarCPPolVecCombTauOneProngA1PiHighPt", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_genMatchedPhiStarCPPolVecCombTauOneProngA1PiHighPt;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genMatchedPhiStarCPPolVecCombOneProngA1PiSSFromRho", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_genMatchedPhiStarCPPolVecCombOneProngA1PiSSFromRho;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genMatchedPhiStarCPPolVecCombOneProngA1PiHighPt", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_genMatchedPhiStarCPPolVecCombOneProngA1PiHighPt;
	});

	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "genMatchedPhiStarCPCombMerged", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_genMatchedPhiStarCPCombMerged;
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
								genY1L = cpq.CalculateSpinAnalysingDiscriminantRho(pi1, pi01);
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
				int decaymode = -999;
				if( gentau != nullptr ){
					decaymode = gentau->genDecayMode();
				}
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
								genY2L = cpq.CalculateSpinAnalysingDiscriminantRho(pi2, pi02);
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
							product.m_genPhiStarCPRho = cpq.CalculatePhiStarCPRho(pi1, pi2, pi01, pi02);
					}
				} else {
					product.m_gen_posyTauL = genY2L;
					product.m_gen_negyTauL = genY1L;
					if (genTau1->genDecayMode()==1 && genTau2->genDecayMode()==1){
						if (pi1.X()!=-999 && pi01.X()!=-999 && pi2.X()!=-999 && pi02.X()!=-999)
							product.m_genPhiStarCPRho = cpq.CalculatePhiStarCPRho(pi2, pi1, pi02, pi01);
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

				product.m_genTauMatchedIPs[product.m_flavourOrderedLeptons.at(0)] = product.m_genIP1;
				product.m_genTauMatchedIPs[product.m_flavourOrderedLeptons.at(1)] = product.m_genIP2;

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
					{
						product.m_genPhiStarCPComb = cpq.CalculatePhiStarCPComb(product.m_genIP2, genParticle2->p4, pi1, pi01, genParticle2->charge());
						product.m_genPhiStarCPCombMerged = cpq.CalculatePhiStarCPComb(product.m_genIP2, genParticle2->p4, pi1, pi01, genParticle2->charge(), true);
					}
					if (genTau1->genDecayMode()!=1 && genTau2->genDecayMode()==1)
					{
						product.m_genPhiStarCPComb = cpq.CalculatePhiStarCPComb(product.m_genIP1, genParticle1->p4, pi2, pi02, genParticle1->charge());
						product.m_genPhiStarCPCombMerged = cpq.CalculatePhiStarCPComb(product.m_genIP1, genParticle1->p4, pi2, pi02, genParticle1->charge(), true);
					}
				}
			///////////////////////////// comb method

			} // if genPV != nullptr

		} // if flavourOrderedGenLeptons is a non-empty vector

	} // if product.m_genBosonLVFound && product.m_genBosonTree.m_daughters.size() > 1

	if (product.m_genTauMatchedLeptons.size() > 1)
	{
		KLepton* oneProng = nullptr;
		KTau* a1 = nullptr;
		RMFLV genIPLVOneProng;

		for (std::vector<KLepton*>::iterator leptonIt = product.m_flavourOrderedLeptons.begin();
		     leptonIt != product.m_flavourOrderedLeptons.end(); ++leptonIt)
		{
			if ((*leptonIt)->flavour() == KLeptonFlavour::TAU)
			{
				KTau* tau = static_cast<KTau*>(*leptonIt);
				int decaymode = m_useMVADecayModes ? (int)tau->getDiscriminator("MVADM2017v1", event.m_tauMetadata) : tau->decayMode;
				if ((! a1) &&
				    (decaymode == reco::PFTau::hadronicDecayMode::kThreeProng0PiZero) &&
				    (tau->chargedHadronCandidates.size() > 2) &&
				    tau->sv.valid)
				{
					a1 = tau;
				}
				else if ((! oneProng) &&
				         ((decaymode == reco::PFTau::hadronicDecayMode::kOneProng0PiZero)
				         ||(decaymode == reco::PFTau::hadronicDecayMode::kOneProng1PiZero)))
				{
					oneProng = *leptonIt;
					TVector3 IPOneProng = product.m_genTauMatchedIPs[*leptonIt];
					genIPLVOneProng.SetXYZT(IPOneProng.X(), IPOneProng.Y(), IPOneProng.Z(), 0);
				}
			}
			else if (! oneProng)
			{
				oneProng = *leptonIt;
				TVector3 IPOneProng = product.m_genTauMatchedIPs[*leptonIt];
				genIPLVOneProng.SetXYZT(IPOneProng.X(), IPOneProng.Y(), IPOneProng.Z(), 0);
			}
		}

		CPQuantities cpq;
		KGenTau* genTau1 = SafeMap::GetWithDefault(product.m_genTauMatchedLeptons, product.m_flavourOrderedLeptons.at(0), static_cast<KGenTau*>(nullptr));
		KGenTau* genTau2 = SafeMap::GetWithDefault(product.m_genTauMatchedLeptons, product.m_flavourOrderedLeptons.at(1), static_cast<KGenTau*>(nullptr));

		KGenTau* genTauA1 = SafeMap::GetWithDefault(product.m_genTauMatchedLeptons, static_cast<KLepton*>(a1), static_cast<KGenTau*>(nullptr));
		KGenTau* genTauOneProng = SafeMap::GetWithDefault(product.m_genTauMatchedLeptons, oneProng, static_cast<KGenTau*>(nullptr));

		if (genTauA1 != nullptr && genTauOneProng != nullptr)
		{
			RMFLV genPiSSFromRho1(0,0,0,0);
			RMFLV genPiOS1(0,0,0,0);
			RMFLV genPiSSHighPt1(0,0,0,0);
			RMFLV genPiSSFromRho2(0,0,0,0);
			RMFLV genPiOS2(0,0,0,0);
			RMFLV genPiSSHighPt2(0,0,0,0);

			RMFLV genA1PiSSFromRho(0,0,0,0);
			RMFLV genA1PiOS(0,0,0,0);
			RMFLV genA1PiSSHighPt(0,0,0,0);

			int genDecayType1(0);
			int genDecayType2(0);
			int genTauDecaymode_1 = genTau1->genDecayMode();
			int genTauDecaymode_2 = genTau2->genDecayMode();

			RMFLV genIP1;
			genIP1.SetXYZT((product.m_genIP1.X()), (product.m_genIP1.Y()), (product.m_genIP1.Z()), 0);
			RMFLV genIP2;
			genIP2.SetXYZT((product.m_genIP2.X()), (product.m_genIP2.Y()), (product.m_genIP2.Z()), 0);

			if (genTauDecaymode_1 > 0)
			{
				if (genTauDecaymode_1 == 1 || genTauDecaymode_1 == 2)
				genDecayType1 = 1;
				else if(genTauDecaymode_1 == 10 || genTauDecaymode_1 == 11)
				genDecayType1 = 2;
			}

			if (genTauDecaymode_2 > 0)
			{
				if (genTauDecaymode_2 == 1 || genTauDecaymode_2 == 2)
				genDecayType2 = 1;
				else if(genTauDecaymode_2 == 10 || genTauDecaymode_2 == 11)
				genDecayType2 = 2;
			}

			genPionsFromRho3Prongs(product, product.m_flavourOrderedLeptons.at(0), genPiSSFromRho1, genPiOS1, genPiSSHighPt1);
			genPionsFromRho3Prongs(product, product.m_flavourOrderedLeptons.at(1), genPiSSFromRho2, genPiOS2, genPiSSHighPt2);

			RMFLV genTau1Tau2ZMF = genTau1->p4 + genTau2->p4;
			RMFLV genTau1VisTau2ZMF = genTau1->visible.p4 + genTau2->p4;
			RMFLV genTau1Tau2VisZMF = genTau1->p4 + genTau2->visible.p4;
			RMFLV genTau1VisTau2VisZMF = genTau1->visible.p4 + genTau2->visible.p4;

			RMFLV genTau1Tau2PiSSFromRhoZMF, genTau1Tau2PiHighPtZMF, genTau1VisTau2PiSSFromRhoZMF, genTau1VisTau2PiHighPtZMF;

			RMFLV genTauOneProngTauA1ZMF = genTauA1->p4 + genTauOneProng->p4;
			RMFLV genOneProngTauA1ZMF = genTauOneProng->visible.p4 + genTauA1->p4;
			RMFLV genTauOneProngA1ZMF = genTauOneProng->p4 + genTauA1->visible.p4;
			RMFLV genOneProngA1ZMF = genTauOneProng->visible.p4 + genTauA1->visible.p4;

			RMFLV genTauOneProngA1PiSSFromRhoZMF, genTauOneProngA1PiHighPtZMF, genOneProngA1PiSSFromRhoZMF, genOneProngA1PiHighPtZMF;

			if (genTauDecaymode_2 == 10)
			{
				genTau1Tau2PiSSFromRhoZMF = genTau1->p4 + genPiSSFromRho2;
				genTau1Tau2PiHighPtZMF = genTau1->p4 + genPiSSHighPt2;
				genTau1VisTau2PiSSFromRhoZMF = genTau1->visible.p4 + genPiSSFromRho2;
				genTau1VisTau2PiHighPtZMF = genTau1->visible.p4 + genPiSSHighPt2;

				genA1PiSSHighPt = genPiSSHighPt2;
				genA1PiSSFromRho = genPiSSFromRho2;
				genA1PiOS = genPiOS2;
			}
			else if (genTauDecaymode_1 == 10)
			{
				genTau1Tau2PiSSFromRhoZMF = genTau2->p4 + genPiSSFromRho1;
				genTau1Tau2PiHighPtZMF = genTau2->p4 + genPiSSHighPt1;
				genTau1VisTau2PiSSFromRhoZMF = genTau2->visible.p4 + genPiSSFromRho1;
				genTau1VisTau2PiHighPtZMF = genTau2->visible.p4 + genPiSSHighPt1;

				genA1PiSSHighPt = genPiSSHighPt1;
				genA1PiSSFromRho = genPiSSFromRho1;
				genA1PiOS = genPiOS1;
			}
			genTauOneProngA1PiSSFromRhoZMF = genTauOneProng->p4 + genA1PiSSFromRho;
			genTauOneProngA1PiHighPtZMF = genTauOneProng->p4 + genA1PiSSHighPt;
			genOneProngA1PiSSFromRhoZMF = genTauOneProng->visible.p4 + genA1PiSSFromRho;
			genOneProngA1PiHighPtZMF = genTauOneProng->visible.p4 + genA1PiSSHighPt;

			for (std::vector<KLepton*>::iterator lepton = product.m_flavourOrderedLeptons.begin();
			lepton != product.m_flavourOrderedLeptons.end(); ++lepton)

			{
				std::vector<TLorentzVector> inputs;
				std::string type = "";
				int charge(-999);

				KGenTau* genTau = SafeMap::GetWithDefault(product.m_genTauMatchedLeptons, *lepton, static_cast<KGenTau*>(nullptr));
				int genTauDecayMode = genTau ? genTau->genDecayMode() : -999;

				if (((*lepton)->flavour() == KLeptonFlavour::ELECTRON) || ((*lepton)->flavour() == KLeptonFlavour::MUON))
				{
					type = "lepton";
				}
				else if ((*lepton)->flavour() == KLeptonFlavour::TAU)
				{
					if (genTauDecayMode == 10)
					{
						inputs = GetInputA1(product, *lepton);
						type = "a1";
						charge = (*lepton)->charge();
					}
					else if (genTauDecayMode == 1)
					{
						inputs = GetInputRho(product, *lepton);
						type = "rho";
						charge = (*lepton)->charge();
					}
					// else if (dm_tau == 0)
					else if (genTauDecayMode == 0)
					{
						inputs = GetInputPion(product, *lepton);
						type = "pion";
						charge = (*lepton)->charge();
					}
				}
				if (inputs.size() > 0 && type != "lepton")
				{
					SCalculator GenSpinCalculatorInterfaceTau1Tau2(type);
					GenSpinCalculatorInterfaceTau1Tau2.Configure(inputs, Utility::ConvertPtEtaPhiMLorentzVector<RMFLV, TLorentzVector>(genTau1Tau2ZMF), charge);
					product.m_polarimetricVectorsTau1Tau2GenMatchedTaus[*lepton] = Utility::ConvertPxPyPzVector<TVector3, RMFLV::BetaVector>(GenSpinCalculatorInterfaceTau1Tau2.pv());

					SCalculator GenSpinCalculatorInterfaceTau1VisTau2(type);
					GenSpinCalculatorInterfaceTau1VisTau2.Configure(inputs, Utility::ConvertPtEtaPhiMLorentzVector<RMFLV, TLorentzVector>(genTau1VisTau2ZMF), charge);
					product.m_polarimetricVectorsTau1VisTau2GenMatchedTaus[*lepton] = Utility::ConvertPxPyPzVector<TVector3, RMFLV::BetaVector>(GenSpinCalculatorInterfaceTau1VisTau2.pv());

					SCalculator GenSpinCalculatorInterfaceTau1Tau2Vis(type);
					GenSpinCalculatorInterfaceTau1Tau2Vis.Configure(inputs, Utility::ConvertPtEtaPhiMLorentzVector<RMFLV, TLorentzVector>(genTau1Tau2VisZMF), charge);
					product.m_polarimetricVectorsTau1Tau2VisGenMatchedTaus[*lepton] = Utility::ConvertPxPyPzVector<TVector3, RMFLV::BetaVector>(GenSpinCalculatorInterfaceTau1Tau2Vis.pv());

					SCalculator GenSpinCalculatorInterfaceTau1VisTau2Vis(type);
					GenSpinCalculatorInterfaceTau1VisTau2Vis.Configure(inputs, Utility::ConvertPtEtaPhiMLorentzVector<RMFLV, TLorentzVector>(genTau1VisTau2VisZMF), charge);
					product.m_polarimetricVectorsTau1VisTau2VisGenMatchedTaus[*lepton] = Utility::ConvertPxPyPzVector<TVector3, RMFLV::BetaVector>(GenSpinCalculatorInterfaceTau1VisTau2Vis.pv());


					SCalculator GenSpinCalculatorInterfaceTauOneProngTauA1(type);
					GenSpinCalculatorInterfaceTauOneProngTauA1.Configure(inputs, Utility::ConvertPtEtaPhiMLorentzVector<RMFLV, TLorentzVector>(genTauOneProngTauA1ZMF), charge);
					product.m_polarimetricVectorsTauOneProngTauA1GenMatchedTaus[*lepton] = Utility::ConvertPxPyPzVector<TVector3, RMFLV::BetaVector>(GenSpinCalculatorInterfaceTauOneProngTauA1.pv());

					SCalculator GenSpinCalculatorInterfaceOneProngTauA1(type);
					GenSpinCalculatorInterfaceOneProngTauA1.Configure(inputs, Utility::ConvertPtEtaPhiMLorentzVector<RMFLV, TLorentzVector>(genOneProngTauA1ZMF), charge);
					product.m_polarimetricVectorsOneProngTauA1GenMatchedTaus[*lepton] = Utility::ConvertPxPyPzVector<TVector3, RMFLV::BetaVector>(GenSpinCalculatorInterfaceOneProngTauA1.pv());

					SCalculator GenSpinCalculatorInterfaceTauOneProngA1(type);
					GenSpinCalculatorInterfaceTauOneProngA1.Configure(inputs, Utility::ConvertPtEtaPhiMLorentzVector<RMFLV, TLorentzVector>(genTauOneProngA1ZMF), charge);
					product.m_polarimetricVectorsTauOneProngA1GenMatchedTaus[*lepton] = Utility::ConvertPxPyPzVector<TVector3, RMFLV::BetaVector>(GenSpinCalculatorInterfaceTauOneProngA1.pv());

					SCalculator GenSpinCalculatorInterfaceOneProngA1(type);
					GenSpinCalculatorInterfaceOneProngA1.Configure(inputs, Utility::ConvertPtEtaPhiMLorentzVector<RMFLV, TLorentzVector>(genOneProngA1ZMF), charge);
					product.m_polarimetricVectorsOneProngA1GenMatchedTaus[*lepton] = Utility::ConvertPxPyPzVector<TVector3, RMFLV::BetaVector>(GenSpinCalculatorInterfaceOneProngA1.pv());

					if (genTauDecaymode_1 == 10 || genTauDecaymode_2 == 10)
					{
						SCalculator GenSpinCalculatorInterfaceTau1Tau2PiSSFromRho(type);
						GenSpinCalculatorInterfaceTau1Tau2PiSSFromRho.Configure(inputs, Utility::ConvertPtEtaPhiMLorentzVector<RMFLV, TLorentzVector>(genTau1Tau2PiSSFromRhoZMF), charge);
						product.m_polarimetricVectorsTau1Tau2PiSSFromRhoGenMatchedTaus[*lepton] = Utility::ConvertPxPyPzVector<TVector3, RMFLV::BetaVector>(GenSpinCalculatorInterfaceTau1Tau2PiSSFromRho.pv());

						SCalculator GenSpinCalculatorInterfaceTau1Tau2PiHighPt(type);
						GenSpinCalculatorInterfaceTau1Tau2PiHighPt.Configure(inputs, Utility::ConvertPtEtaPhiMLorentzVector<RMFLV, TLorentzVector>(genTau1Tau2PiHighPtZMF), charge);
						product.m_polarimetricVectorsTau1Tau2PiHighPtGenMatchedTaus[*lepton] = Utility::ConvertPxPyPzVector<TVector3, RMFLV::BetaVector>(GenSpinCalculatorInterfaceTau1Tau2PiHighPt.pv());

						SCalculator GenSpinCalculatorInterfaceTau1VisTau2PiSSFromRho(type);
						GenSpinCalculatorInterfaceTau1VisTau2PiSSFromRho.Configure(inputs, Utility::ConvertPtEtaPhiMLorentzVector<RMFLV, TLorentzVector>(genTau1VisTau2PiSSFromRhoZMF), charge);
						product.m_polarimetricVectorsTau1VisTau2PiSSFromRhoGenMatchedTaus[*lepton] = Utility::ConvertPxPyPzVector<TVector3, RMFLV::BetaVector>(GenSpinCalculatorInterfaceTau1VisTau2PiSSFromRho.pv());

						SCalculator GenSpinCalculatorInterfaceTau1VisTau2PiHighPt(type);
						GenSpinCalculatorInterfaceTau1VisTau2PiHighPt.Configure(inputs, Utility::ConvertPtEtaPhiMLorentzVector<RMFLV, TLorentzVector>(genTau1VisTau2PiHighPtZMF), charge);
						product.m_polarimetricVectorsTau1VisTau2PiHighPtGenMatchedTaus[*lepton] = Utility::ConvertPxPyPzVector<TVector3, RMFLV::BetaVector>(GenSpinCalculatorInterfaceTau1VisTau2PiHighPt.pv());


						SCalculator GenSpinCalculatorInterfaceTauOneProngA1PiSSFromRho(type);
						GenSpinCalculatorInterfaceTauOneProngA1PiSSFromRho.Configure(inputs, Utility::ConvertPtEtaPhiMLorentzVector<RMFLV, TLorentzVector>(genTauOneProngA1PiSSFromRhoZMF), charge);
						product.m_polarimetricVectorsTauOneProngA1PiSSFromRhoGenMatchedTaus[*lepton] = Utility::ConvertPxPyPzVector<TVector3, RMFLV::BetaVector>(GenSpinCalculatorInterfaceTauOneProngA1PiSSFromRho.pv());

						SCalculator GenSpinCalculatorInterfaceTauOneProngA1PiHighPt(type);
						GenSpinCalculatorInterfaceTauOneProngA1PiHighPt.Configure(inputs, Utility::ConvertPtEtaPhiMLorentzVector<RMFLV, TLorentzVector>(genTauOneProngA1PiHighPtZMF), charge);
						product.m_polarimetricVectorsTauOneProngA1PiHighPtGenMatchedTaus[*lepton] = Utility::ConvertPxPyPzVector<TVector3, RMFLV::BetaVector>(GenSpinCalculatorInterfaceTauOneProngA1PiHighPt.pv());

						SCalculator GenSpinCalculatorInterfaceOneProngA1PiSSFromRho(type);
						GenSpinCalculatorInterfaceOneProngA1PiSSFromRho.Configure(inputs, Utility::ConvertPtEtaPhiMLorentzVector<RMFLV, TLorentzVector>(genOneProngA1PiSSFromRhoZMF), charge);
						product.m_polarimetricVectorsOneProngA1PiSSFromRhoGenMatchedTaus[*lepton] = Utility::ConvertPxPyPzVector<TVector3, RMFLV::BetaVector>(GenSpinCalculatorInterfaceOneProngA1PiSSFromRho.pv());

						SCalculator GenSpinCalculatorInterfaceOneProngA1PiHighPt(type);
						GenSpinCalculatorInterfaceOneProngA1PiHighPt.Configure(inputs, Utility::ConvertPtEtaPhiMLorentzVector<RMFLV, TLorentzVector>(genOneProngA1PiHighPtZMF), charge);
						product.m_polarimetricVectorsOneProngA1PiHighPtGenMatchedTaus[*lepton] = Utility::ConvertPxPyPzVector<TVector3, RMFLV::BetaVector>(GenSpinCalculatorInterfaceOneProngA1PiHighPt.pv());
					}
				}
			}
			if ( (product.m_decayChannel == HttEnumTypes::DecayChannel::MT || product.m_decayChannel == HttEnumTypes::DecayChannel::ET) ) {

				// l+rho/a1(1-prong)
				// if (genDecayType2 == 1) {
				// 	product.m_genMatchedPhiStarCPCombMerged = cpq.CalculatePhiStarCPComb(product.m_genIP1, recoParticle1->p4, recoTau2->chargedHadronCandidates.at(0).p4, piZero2, recoParticle1->charge(), true);
				// }
				// l+3-prongs
				if (genDecayType2 == 2) {
					product.m_genMatchedPhiStarCPCombMerged = cpq.CalculatePhiStarCPComb(product.m_genIP1, genTau2->visible.p4, genPiSSFromRho2, genPiOS2, genTau1->charge(), true);
				}

				if (genTauDecaymode_2 == 10)
				{
					bool genFirstNegative = genTau2->charge() < 0;
					if(product.m_polarimetricVectorsTau1Tau2GenMatchedTaus.size() > 0)
					{
						RMFLV::BetaVector polVecTau1Tau2_2 = product.m_polarimetricVectorsTau1Tau2GenMatchedTaus[product.m_flavourOrderedLeptons.at(1)];
						product.m_genMatchedPhiStarCPPolVecCombTau1Tau2 = cpq.CalculatePhiStarCPPolVecComb(genTau2->p4, genTau1->p4, polVecTau1Tau2_2, genIP1, genFirstNegative);
					}
					if(product.m_polarimetricVectorsTau1VisTau2GenMatchedTaus.size() > 0)
					{
						RMFLV::BetaVector polVecTau1VisTau2_2 = product.m_polarimetricVectorsTau1VisTau2GenMatchedTaus[product.m_flavourOrderedLeptons.at(1)];
						product.m_genMatchedPhiStarCPPolVecCombTau1VisTau2 = cpq.CalculatePhiStarCPPolVecComb(genTau2->p4, genTau1->visible.p4, polVecTau1VisTau2_2, genIP1, genFirstNegative);
					}
					if(product.m_polarimetricVectorsTau1Tau2VisGenMatchedTaus.size() > 0)
					{
						RMFLV::BetaVector polVecTau1Tau2Vis_2 = product.m_polarimetricVectorsTau1Tau2VisGenMatchedTaus[product.m_flavourOrderedLeptons.at(1)];
						product.m_genMatchedPhiStarCPPolVecCombTau1Tau2Vis = cpq.CalculatePhiStarCPPolVecComb(genTau2->visible.p4, genTau1->p4, polVecTau1Tau2Vis_2, genIP1, genFirstNegative);
					}
					if(product.m_polarimetricVectorsTau1VisTau2VisGenMatchedTaus.size() > 0)
					{
						RMFLV::BetaVector polVecTau1VisTau2Vis_2 = product.m_polarimetricVectorsTau1VisTau2VisGenMatchedTaus[product.m_flavourOrderedLeptons.at(1)];
						product.m_genMatchedPhiStarCPPolVecCombTau1VisTau2Vis = cpq.CalculatePhiStarCPPolVecComb(genTau2->visible.p4, genTau1->visible.p4, polVecTau1VisTau2Vis_2, genIP1, genFirstNegative);
					}
					if(product.m_polarimetricVectorsTau1Tau2PiSSFromRhoGenMatchedTaus.size() > 0)
					{
						RMFLV::BetaVector polVecTau1Tau2PiSSFromRho_2 = product.m_polarimetricVectorsTau1Tau2PiSSFromRhoGenMatchedTaus[product.m_flavourOrderedLeptons.at(1)];
						product.m_genMatchedPhiStarCPPolVecCombTau1Tau2PiSSFromRho = cpq.CalculatePhiStarCPPolVecComb(genPiSSFromRho2, genTau1->p4, polVecTau1Tau2PiSSFromRho_2, genIP1, genFirstNegative);
					}
					if(product.m_polarimetricVectorsTau1Tau2PiHighPtGenMatchedTaus.size() > 0)
					{
						RMFLV::BetaVector polVecTau1Tau2PiHighPt_2 = product.m_polarimetricVectorsTau1Tau2PiHighPtGenMatchedTaus[product.m_flavourOrderedLeptons.at(1)];
						product.m_genMatchedPhiStarCPPolVecCombTau1Tau2PiHighPt = cpq.CalculatePhiStarCPPolVecComb(genPiSSHighPt2, genTau1->p4, polVecTau1Tau2PiHighPt_2, genIP1, genFirstNegative);
					}
					if(product.m_polarimetricVectorsTau1VisTau2PiSSFromRhoGenMatchedTaus.size() > 0)
					{
						RMFLV::BetaVector polVecTau1VisTau2PiSSFromRho_2 = product.m_polarimetricVectorsTau1VisTau2PiSSFromRhoGenMatchedTaus[product.m_flavourOrderedLeptons.at(1)];
						product.m_genMatchedPhiStarCPPolVecCombTau1VisTau2PiSSFromRho = cpq.CalculatePhiStarCPPolVecComb(genPiSSFromRho2, genTau1->visible.p4, polVecTau1VisTau2PiSSFromRho_2, genIP1, genFirstNegative);
					}
					if(product.m_polarimetricVectorsTau1VisTau2PiHighPtGenMatchedTaus.size() > 0)
					{
						RMFLV::BetaVector polVecTau1VisTau2PiHighPt_2 = product.m_polarimetricVectorsTau1VisTau2PiHighPtGenMatchedTaus[product.m_flavourOrderedLeptons.at(1)];
						product.m_genMatchedPhiStarCPPolVecCombTau1VisTau2PiHighPt = cpq.CalculatePhiStarCPPolVecComb(genPiSSHighPt2, genTau1->visible.p4, polVecTau1VisTau2PiHighPt_2, genIP1, genFirstNegative);
					}
				}
			} // if et or mt ch.
			if ( product.m_decayChannel == HttEnumTypes::DecayChannel::TT ) {
				// rho/a1(1-prong)+pi
				// if (genDecayType1 == 1 && genDecayType2 == 0) {
				// 	product.m_genMatchedPhiStarCPCombMerged = cpq.CalculatePhiStarCPComb(product.m_genIP2, genTau2->visible.p4, recoTau1->chargedHadronCandidates.at(0).p4, piZero1, genTau2->charge(), true);
				// }
				// 3-prongs+pi
				if (genDecayType1 == 2 && genDecayType2 == 0) {
					product.m_genMatchedPhiStarCPCombMerged = cpq.CalculatePhiStarCPComb(product.m_genIP2, genTau2->visible.p4, genPiSSFromRho1, genPiOS1, genTau2->charge(), true);
				}
				// // pi+rho/a1(1-prong)
				// else if (genDecayType1 == 0 && genDecayType2 == 1) {
					// 	product.m_genMatchedPhiStarCPCombMerged = cpq.CalculatePhiStarCPComb(product.m_genIP1, genTau1->visible.p4, genTau2->visible.p4, piZero2, genTau1->charge(), true);
					// }
					// pi+3-prongs
				else if (genDecayType1 == 0 && genDecayType2 == 2) {
					// product.m_recoPhiStarCPCombMergedHelrPVBS = cpq.CalculatePhiStarCPComb(product.m_recoIPHelrPVBS_1, recoTau1->chargedHadronCandidates.at(0).p4, piSSFromRho2, piOS2, recoTau1->charge(), true);
					product.m_genMatchedPhiStarCPCombMerged = cpq.CalculatePhiStarCPComb(product.m_genIP1, genTau1->visible.p4, genPiSSFromRho2, genPiOS2, genTau1->charge(), true);
				}

				if (genTauDecaymode_1 == 10 && genTauDecaymode_2 == 0)
				{
					bool genFirstNegative = genTau1->charge() < 0;
					if(product.m_polarimetricVectorsTau1Tau2GenMatchedTaus.size() > 0)
					{
						RMFLV::BetaVector polVecTau1Tau2_1 = product.m_polarimetricVectorsTau1Tau2GenMatchedTaus[product.m_flavourOrderedLeptons.at(0)];
						RMFLV::BetaVector polVecTau1Tau2_2 = product.m_polarimetricVectorsTau1Tau2GenMatchedTaus[product.m_flavourOrderedLeptons.at(1)];
						product.m_genMatchedPhiStarCPPolVecTau1Tau2 = cpq.CalculatePhiStarCPPolVec(genTau1->p4, genTau2->p4, polVecTau1Tau2_1, polVecTau1Tau2_2, genFirstNegative);
						product.m_genMatchedPhiStarCPPolVecCombTau1Tau2 = cpq.CalculatePhiStarCPPolVecComb(genTau1->p4, genTau2->p4, polVecTau1Tau2_1, genIP2, genFirstNegative);
					}
					if(product.m_polarimetricVectorsTau1VisTau2GenMatchedTaus.size() > 0)
					{
						RMFLV::BetaVector polVecTau1VisTau2_1 = product.m_polarimetricVectorsTau1VisTau2GenMatchedTaus[product.m_flavourOrderedLeptons.at(0)];
						RMFLV::BetaVector polVecTau1VisTau2_2 = product.m_polarimetricVectorsTau1VisTau2GenMatchedTaus[product.m_flavourOrderedLeptons.at(1)];
						product.m_genMatchedPhiStarCPPolVecTau1VisTau2 = cpq.CalculatePhiStarCPPolVec(genTau1->p4, genTau2->visible.p4, polVecTau1VisTau2_1, polVecTau1VisTau2_2, genFirstNegative);
						product.m_genMatchedPhiStarCPPolVecCombTau1VisTau2 = cpq.CalculatePhiStarCPPolVecComb(genTau1->p4, genTau2->visible.p4, polVecTau1VisTau2_1, genIP2, genFirstNegative);
					}
					if(product.m_polarimetricVectorsTau1Tau2VisGenMatchedTaus.size() > 0)
					{
						RMFLV::BetaVector polVecTau1Tau2Vis_1 = product.m_polarimetricVectorsTau1Tau2VisGenMatchedTaus[product.m_flavourOrderedLeptons.at(0)];
						RMFLV::BetaVector polVecTau1Tau2Vis_2 = product.m_polarimetricVectorsTau1Tau2VisGenMatchedTaus[product.m_flavourOrderedLeptons.at(1)];
						product.m_genMatchedPhiStarCPPolVecTau1Tau2Vis = cpq.CalculatePhiStarCPPolVec(genTau1->visible.p4, genTau2->p4, polVecTau1Tau2Vis_1, polVecTau1Tau2Vis_2, genFirstNegative);
						product.m_genMatchedPhiStarCPPolVecCombTau1Tau2Vis = cpq.CalculatePhiStarCPPolVecComb(genTau1->visible.p4, genTau2->p4, polVecTau1Tau2Vis_1, genIP2, genFirstNegative);
					}
					if(product.m_polarimetricVectorsTau1VisTau2VisGenMatchedTaus.size() > 0)
					{
						RMFLV::BetaVector polVecTau1VisTau2Vis_1 = product.m_polarimetricVectorsTau1VisTau2VisGenMatchedTaus[product.m_flavourOrderedLeptons.at(0)];
						RMFLV::BetaVector polVecTau1VisTau2Vis_2 = product.m_polarimetricVectorsTau1VisTau2VisGenMatchedTaus[product.m_flavourOrderedLeptons.at(1)];
						product.m_genMatchedPhiStarCPPolVecTau1VisTau2Vis = cpq.CalculatePhiStarCPPolVec(genTau1->visible.p4,  genTau2->visible.p4, polVecTau1VisTau2Vis_1, polVecTau1VisTau2Vis_2, genFirstNegative);
						product.m_genMatchedPhiStarCPPolVecCombTau1VisTau2Vis = cpq.CalculatePhiStarCPPolVecComb(genTau1->visible.p4,  genTau2->visible.p4, polVecTau1VisTau2Vis_1, genIP2, genFirstNegative);
					}
					if(product.m_polarimetricVectorsTau1Tau2PiSSFromRhoGenMatchedTaus.size() > 0)
					{
						RMFLV::BetaVector polVecTau1Tau2PiSSFromRho_1 = product.m_polarimetricVectorsTau1Tau2PiSSFromRhoGenMatchedTaus[product.m_flavourOrderedLeptons.at(0)];
						RMFLV::BetaVector polVecTau1Tau2PiSSFromRho_2 = product.m_polarimetricVectorsTau1Tau2PiSSFromRhoGenMatchedTaus[product.m_flavourOrderedLeptons.at(1)];
						product.m_genMatchedPhiStarCPPolVecTau1Tau2PiSSFromRho = cpq.CalculatePhiStarCPPolVec(genPiSSFromRho1, genTau2->p4, polVecTau1Tau2PiSSFromRho_1, polVecTau1Tau2PiSSFromRho_2, genFirstNegative);
						product.m_genMatchedPhiStarCPPolVecCombTau1Tau2PiSSFromRho = cpq.CalculatePhiStarCPPolVecComb(genPiSSFromRho1, genTau2->p4, polVecTau1Tau2PiSSFromRho_1, genIP2, genFirstNegative);
					}
					if(product.m_polarimetricVectorsTau1Tau2PiHighPtGenMatchedTaus.size() > 0)
					{
						RMFLV::BetaVector polVecTau1Tau2PiHighPt_1 = product.m_polarimetricVectorsTau1Tau2PiHighPtGenMatchedTaus[product.m_flavourOrderedLeptons.at(0)];
						RMFLV::BetaVector polVecTau1Tau2PiHighPt_2 = product.m_polarimetricVectorsTau1Tau2PiHighPtGenMatchedTaus[product.m_flavourOrderedLeptons.at(1)];
						product.m_genMatchedPhiStarCPPolVecTau1Tau2PiHighPt = cpq.CalculatePhiStarCPPolVec(genPiSSHighPt1, genTau2->p4, polVecTau1Tau2PiHighPt_1, polVecTau1Tau2PiHighPt_2, genFirstNegative);
						product.m_genMatchedPhiStarCPPolVecCombTau1Tau2PiHighPt = cpq.CalculatePhiStarCPPolVecComb(genPiSSHighPt1, genTau2->p4, polVecTau1Tau2PiHighPt_1, genIP2, genFirstNegative);
					}
					if(product.m_polarimetricVectorsTau1VisTau2PiSSFromRhoGenMatchedTaus.size() > 0)
					{
						RMFLV::BetaVector polVecTau1VisTau2PiSSFromRho_1 = product.m_polarimetricVectorsTau1VisTau2PiSSFromRhoGenMatchedTaus[product.m_flavourOrderedLeptons.at(0)];
						RMFLV::BetaVector polVecTau1VisTau2PiSSFromRho_2 = product.m_polarimetricVectorsTau1VisTau2PiSSFromRhoGenMatchedTaus[product.m_flavourOrderedLeptons.at(1)];
						product.m_genMatchedPhiStarCPPolVecTau1VisTau2PiSSFromRho = cpq.CalculatePhiStarCPPolVec(genPiSSFromRho1, genTau2->visible.p4, polVecTau1VisTau2PiSSFromRho_1, polVecTau1VisTau2PiSSFromRho_2, genFirstNegative);
						product.m_genMatchedPhiStarCPPolVecCombTau1VisTau2PiSSFromRho = cpq.CalculatePhiStarCPPolVecComb(genPiSSFromRho1, genTau2->visible.p4, polVecTau1VisTau2PiSSFromRho_1, genIP2, genFirstNegative);
					}
					if(product.m_polarimetricVectorsTau1VisTau2PiHighPtGenMatchedTaus.size() > 0)
					{
						RMFLV::BetaVector polVecTau1VisTau2PiHighPt_1 = product.m_polarimetricVectorsTau1VisTau2PiHighPtGenMatchedTaus[product.m_flavourOrderedLeptons.at(0)];
						RMFLV::BetaVector polVecTau1VisTau2PiHighPt_2 = product.m_polarimetricVectorsTau1VisTau2PiHighPtGenMatchedTaus[product.m_flavourOrderedLeptons.at(1)];
						product.m_genMatchedPhiStarCPPolVecTau1VisTau2PiHighPt = cpq.CalculatePhiStarCPPolVec(genPiSSHighPt1, genTau2->visible.p4, polVecTau1VisTau2PiHighPt_1, polVecTau1VisTau2PiHighPt_2, genFirstNegative);
						product.m_genMatchedPhiStarCPPolVecCombTau1VisTau2PiHighPt = cpq.CalculatePhiStarCPPolVecComb(genPiSSHighPt1, genTau2->visible.p4, polVecTau1VisTau2PiHighPt_1, genIP2, genFirstNegative);
					}
				}
				if (genTauDecaymode_1 == 0 && genTauDecaymode_2 == 10)
				{
					bool genFirstNegative = genTau2->charge() < 0;
					if(product.m_polarimetricVectorsTau1Tau2GenMatchedTaus.size() > 0)
					{
						RMFLV::BetaVector polVecTau1Tau2_1 = product.m_polarimetricVectorsTau1Tau2GenMatchedTaus[product.m_flavourOrderedLeptons.at(0)];
						RMFLV::BetaVector polVecTau1Tau2_2 = product.m_polarimetricVectorsTau1Tau2GenMatchedTaus[product.m_flavourOrderedLeptons.at(1)];
						product.m_genMatchedPhiStarCPPolVecTau1Tau2 = cpq.CalculatePhiStarCPPolVec(genTau2->p4, genTau1->p4, polVecTau1Tau2_2, polVecTau1Tau2_1, genFirstNegative);
						product.m_genMatchedPhiStarCPPolVecCombTau1Tau2 = cpq.CalculatePhiStarCPPolVecComb(genTau2->p4, genTau1->p4, polVecTau1Tau2_2, genIP1, genFirstNegative);
					}
					if(product.m_polarimetricVectorsTau1VisTau2GenMatchedTaus.size() > 0)
					{
						RMFLV::BetaVector polVecTau1VisTau2_1 = product.m_polarimetricVectorsTau1VisTau2GenMatchedTaus[product.m_flavourOrderedLeptons.at(0)];
						RMFLV::BetaVector polVecTau1VisTau2_2 = product.m_polarimetricVectorsTau1VisTau2GenMatchedTaus[product.m_flavourOrderedLeptons.at(1)];
						product.m_genMatchedPhiStarCPPolVecTau1VisTau2 = cpq.CalculatePhiStarCPPolVec(genTau2->p4, genTau1->visible.p4, polVecTau1VisTau2_2, polVecTau1VisTau2_1, genFirstNegative);
						product.m_genMatchedPhiStarCPPolVecCombTau1VisTau2 = cpq.CalculatePhiStarCPPolVecComb(genTau2->p4, genTau1->visible.p4, polVecTau1VisTau2_2, genIP1, genFirstNegative);
					}
					if(product.m_polarimetricVectorsTau1Tau2VisGenMatchedTaus.size() > 0)
					{
						RMFLV::BetaVector polVecTau1Tau2Vis_1 = product.m_polarimetricVectorsTau1Tau2VisGenMatchedTaus[product.m_flavourOrderedLeptons.at(0)];
						RMFLV::BetaVector polVecTau1Tau2Vis_2 = product.m_polarimetricVectorsTau1Tau2VisGenMatchedTaus[product.m_flavourOrderedLeptons.at(1)];
						product.m_genMatchedPhiStarCPPolVecTau1Tau2Vis = cpq.CalculatePhiStarCPPolVec(genTau2->visible.p4, genTau1->p4, polVecTau1Tau2Vis_2, polVecTau1Tau2Vis_1, genFirstNegative);
						product.m_genMatchedPhiStarCPPolVecCombTau1Tau2Vis = cpq.CalculatePhiStarCPPolVecComb(genTau2->visible.p4, genTau1->p4, polVecTau1Tau2Vis_2, genIP1, genFirstNegative);
					}
					if(product.m_polarimetricVectorsTau1VisTau2VisGenMatchedTaus.size() > 0)
					{
						RMFLV::BetaVector polVecTau1VisTau2Vis_1 = product.m_polarimetricVectorsTau1VisTau2VisGenMatchedTaus[product.m_flavourOrderedLeptons.at(0)];
						RMFLV::BetaVector polVecTau1VisTau2Vis_2 = product.m_polarimetricVectorsTau1VisTau2VisGenMatchedTaus[product.m_flavourOrderedLeptons.at(1)];
						product.m_genMatchedPhiStarCPPolVecTau1VisTau2Vis = cpq.CalculatePhiStarCPPolVec(genTau2->visible.p4, genTau1->visible.p4, polVecTau1VisTau2Vis_2, polVecTau1VisTau2Vis_1, genFirstNegative);
						product.m_genMatchedPhiStarCPPolVecCombTau1VisTau2Vis = cpq.CalculatePhiStarCPPolVecComb(genTau2->visible.p4, genTau1->visible.p4, polVecTau1VisTau2Vis_2, genIP1, genFirstNegative);
					}
					if(product.m_polarimetricVectorsTau1Tau2PiSSFromRhoGenMatchedTaus.size() > 0)
					{
						RMFLV::BetaVector polVecTau1Tau2PiSSFromRho_1 = product.m_polarimetricVectorsTau1Tau2PiSSFromRhoGenMatchedTaus[product.m_flavourOrderedLeptons.at(0)];
						RMFLV::BetaVector polVecTau1Tau2PiSSFromRho_2 = product.m_polarimetricVectorsTau1Tau2PiSSFromRhoGenMatchedTaus[product.m_flavourOrderedLeptons.at(1)];
						product.m_genMatchedPhiStarCPPolVecTau1Tau2PiSSFromRho = cpq.CalculatePhiStarCPPolVec(genPiSSFromRho2, genTau1->p4, polVecTau1Tau2PiSSFromRho_2, polVecTau1Tau2PiSSFromRho_1, genFirstNegative);
						product.m_genMatchedPhiStarCPPolVecCombTau1Tau2PiSSFromRho = cpq.CalculatePhiStarCPPolVecComb(genPiSSFromRho2, genTau1->p4, polVecTau1Tau2PiSSFromRho_2, genIP1, genFirstNegative);
					}
					if(product.m_polarimetricVectorsTau1Tau2PiHighPtGenMatchedTaus.size() > 0)
					{
						RMFLV::BetaVector polVecTau1Tau2PiHighPt_1 = product.m_polarimetricVectorsTau1Tau2PiHighPtGenMatchedTaus[product.m_flavourOrderedLeptons.at(0)];
						RMFLV::BetaVector polVecTau1Tau2PiHighPt_2 = product.m_polarimetricVectorsTau1Tau2PiHighPtGenMatchedTaus[product.m_flavourOrderedLeptons.at(1)];
						product.m_genMatchedPhiStarCPPolVecTau1Tau2PiHighPt = cpq.CalculatePhiStarCPPolVec(genPiSSHighPt2, genTau1->p4, polVecTau1Tau2PiHighPt_2, polVecTau1Tau2PiHighPt_1, genFirstNegative);
						product.m_genMatchedPhiStarCPPolVecCombTau1Tau2PiHighPt = cpq.CalculatePhiStarCPPolVecComb(genPiSSHighPt2, genTau1->p4, polVecTau1Tau2PiHighPt_2, genIP1, genFirstNegative);
					}
					if(product.m_polarimetricVectorsTau1VisTau2PiSSFromRhoGenMatchedTaus.size() > 0)
					{
						RMFLV::BetaVector polVecTau1VisTau2PiSSFromRho_1 = product.m_polarimetricVectorsTau1VisTau2PiSSFromRhoGenMatchedTaus[product.m_flavourOrderedLeptons.at(0)];
						RMFLV::BetaVector polVecTau1VisTau2PiSSFromRho_2 = product.m_polarimetricVectorsTau1VisTau2PiSSFromRhoGenMatchedTaus[product.m_flavourOrderedLeptons.at(1)];
						product.m_genMatchedPhiStarCPPolVecTau1VisTau2PiSSFromRho = cpq.CalculatePhiStarCPPolVec(genPiSSFromRho2, genTau1->visible.p4, polVecTau1VisTau2PiSSFromRho_2, polVecTau1VisTau2PiSSFromRho_1, genFirstNegative);
						product.m_genMatchedPhiStarCPPolVecCombTau1VisTau2PiSSFromRho = cpq.CalculatePhiStarCPPolVecComb(genPiSSFromRho2, genTau1->visible.p4, polVecTau1VisTau2PiSSFromRho_2, genIP1, genFirstNegative);
					}
					if(product.m_polarimetricVectorsTau1VisTau2PiHighPtGenMatchedTaus.size() > 0)
					{
						RMFLV::BetaVector polVecTau1VisTau2PiHighPt_1 = product.m_polarimetricVectorsTau1VisTau2PiHighPtGenMatchedTaus[product.m_flavourOrderedLeptons.at(0)];
						RMFLV::BetaVector polVecTau1VisTau2PiHighPt_2 = product.m_polarimetricVectorsTau1VisTau2PiHighPtGenMatchedTaus[product.m_flavourOrderedLeptons.at(1)];
						product.m_genMatchedPhiStarCPPolVecTau1VisTau2PiHighPt = cpq.CalculatePhiStarCPPolVec(genPiSSHighPt2, genTau1->visible.p4, polVecTau1VisTau2PiHighPt_2, polVecTau1VisTau2PiHighPt_1, genFirstNegative);
						product.m_genMatchedPhiStarCPPolVecCombTau1VisTau2PiHighPt = cpq.CalculatePhiStarCPPolVecComb(genPiSSHighPt2, genTau1->visible.p4, polVecTau1VisTau2PiHighPt_2, genIP1, genFirstNegative);
					}
				}
			}  // if tt ch.

			// first particle is always a1
			bool firstNegative = genTauA1->charge() < 0;
			if(product.m_polarimetricVectorsTauOneProngTauA1GenMatchedTaus.size() > 0)
			{
				RMFLV::BetaVector genPolVecA1 = product.m_polarimetricVectorsTauOneProngTauA1GenMatchedTaus[a1];
				RMFLV::BetaVector genPolVecOneProng = product.m_polarimetricVectorsTauOneProngTauA1GenMatchedTaus[oneProng];
				product.m_genMatchedPhiStarCPPolVecTauOneProngTauA1 = cpq.CalculatePhiStarCPPolVec(genTauA1->p4, genTauOneProng->p4, genPolVecA1, genPolVecOneProng, firstNegative);
				product.m_genMatchedPhiStarCPPolVecCombTauOneProngTauA1 = cpq.CalculatePhiStarCPPolVecComb(genTauA1->p4, genTauOneProng->p4, genPolVecA1, genIPLVOneProng, firstNegative);
			}
			if(product.m_polarimetricVectorsOneProngTauA1GenMatchedTaus.size() > 0)
			{
				RMFLV::BetaVector genPolVecA1 = product.m_polarimetricVectorsOneProngTauA1GenMatchedTaus[a1];
				RMFLV::BetaVector genPolVecOneProng = product.m_polarimetricVectorsOneProngTauA1GenMatchedTaus[oneProng];
				product.m_genMatchedPhiStarCPPolVecOneProngTauA1 = cpq.CalculatePhiStarCPPolVec(genTauA1->p4, genTauOneProng->visible.p4, genPolVecA1, genPolVecOneProng, firstNegative);
				product.m_genMatchedPhiStarCPPolVecCombOneProngTauA1 = cpq.CalculatePhiStarCPPolVecComb(genTauA1->p4, genTauOneProng->visible.p4, genPolVecA1, genIPLVOneProng, firstNegative);
			}
			if(product.m_polarimetricVectorsTauOneProngA1GenMatchedTaus.size() > 0)
			{
				RMFLV::BetaVector genPolVecA1 = product.m_polarimetricVectorsTauOneProngA1GenMatchedTaus[a1];
				RMFLV::BetaVector genPolVecOneProng = product.m_polarimetricVectorsTauOneProngA1GenMatchedTaus[oneProng];
				product.m_genMatchedPhiStarCPPolVecTauOneProngA1 = cpq.CalculatePhiStarCPPolVec(genTauA1->visible.p4, genTauOneProng->p4, genPolVecA1, genPolVecOneProng, firstNegative);
				product.m_genMatchedPhiStarCPPolVecCombTauOneProngA1 = cpq.CalculatePhiStarCPPolVecComb(genTauA1->visible.p4, genTauOneProng->p4, genPolVecA1, genIPLVOneProng, firstNegative);
			}
			if(product.m_polarimetricVectorsOneProngA1GenMatchedTaus.size() > 0)
			{
				RMFLV::BetaVector genPolVecA1 = product.m_polarimetricVectorsOneProngA1GenMatchedTaus[a1];
				RMFLV::BetaVector genPolVecOneProng = product.m_polarimetricVectorsOneProngA1GenMatchedTaus[oneProng];
				product.m_genMatchedPhiStarCPPolVecOneProngA1 = cpq.CalculatePhiStarCPPolVec(genTauA1->visible.p4, genTauOneProng->visible.p4, genPolVecA1, genPolVecOneProng, firstNegative);
				product.m_genMatchedPhiStarCPPolVecCombOneProngA1 = cpq.CalculatePhiStarCPPolVecComb(genTauA1->visible.p4, genTauOneProng->visible.p4, genPolVecA1, genIPLVOneProng, firstNegative);
			}
			if(product.m_polarimetricVectorsTauOneProngA1PiSSFromRhoGenMatchedTaus.size() > 0)
			{
				RMFLV::BetaVector genPolVecA1 = product.m_polarimetricVectorsTauOneProngA1PiSSFromRhoGenMatchedTaus[a1];
				RMFLV::BetaVector genPolVecOneProng = product.m_polarimetricVectorsTauOneProngA1PiSSFromRhoGenMatchedTaus[oneProng];
				product.m_genMatchedPhiStarCPPolVecTauOneProngA1PiSSFromRho = cpq.CalculatePhiStarCPPolVec(genA1PiSSFromRho, genTauOneProng->p4, genPolVecA1, genPolVecOneProng, firstNegative);
				product.m_genMatchedPhiStarCPPolVecCombTauOneProngA1PiSSFromRho = cpq.CalculatePhiStarCPPolVecComb(genA1PiSSFromRho, genTauOneProng->p4, genPolVecA1, genIPLVOneProng, firstNegative);
			}
			if(product.m_polarimetricVectorsTauOneProngA1PiHighPtGenMatchedTaus.size() > 0)
			{
				RMFLV::BetaVector genPolVecA1 = product.m_polarimetricVectorsTauOneProngA1PiHighPtGenMatchedTaus[a1];
				RMFLV::BetaVector genPolVecOneProng = product.m_polarimetricVectorsTauOneProngA1PiHighPtGenMatchedTaus[oneProng];
				product.m_genMatchedPhiStarCPPolVecTauOneProngA1PiHighPt = cpq.CalculatePhiStarCPPolVec(genA1PiSSHighPt, genTauOneProng->p4, genPolVecA1, genPolVecOneProng, firstNegative);
				product.m_genMatchedPhiStarCPPolVecCombTauOneProngA1PiHighPt = cpq.CalculatePhiStarCPPolVecComb(genA1PiSSHighPt, genTauOneProng->p4, genPolVecA1, genIPLVOneProng, firstNegative);
			}
			if(product.m_polarimetricVectorsOneProngA1PiSSFromRhoGenMatchedTaus.size() > 0)
			{
				RMFLV::BetaVector genPolVecA1 = product.m_polarimetricVectorsOneProngA1PiSSFromRhoGenMatchedTaus[a1];
				RMFLV::BetaVector genPolVecOneProng = product.m_polarimetricVectorsOneProngA1PiSSFromRhoGenMatchedTaus[oneProng];
				product.m_genMatchedPhiStarCPPolVecOneProngA1PiSSFromRho = cpq.CalculatePhiStarCPPolVec(genA1PiSSFromRho, genTauOneProng->visible.p4, genPolVecA1, genPolVecOneProng, firstNegative);
				product.m_genMatchedPhiStarCPPolVecCombOneProngA1PiSSFromRho = cpq.CalculatePhiStarCPPolVecComb(genA1PiSSFromRho, genTauOneProng->visible.p4, genPolVecA1, genIPLVOneProng, firstNegative);
			}
			if(product.m_polarimetricVectorsOneProngA1PiHighPtGenMatchedTaus.size() > 0)
			{
				RMFLV::BetaVector genPolVecA1 = product.m_polarimetricVectorsOneProngA1PiHighPtGenMatchedTaus[a1];
				RMFLV::BetaVector genPolVecOneProng = product.m_polarimetricVectorsOneProngA1PiHighPtGenMatchedTaus[oneProng];
				product.m_genMatchedPhiStarCPPolVecOneProngA1PiHighPt = cpq.CalculatePhiStarCPPolVec(genA1PiSSHighPt, genTauOneProng->visible.p4, genPolVecA1, genPolVecOneProng, firstNegative);
				product.m_genMatchedPhiStarCPPolVecCombOneProngA1PiHighPt = cpq.CalculatePhiStarCPPolVecComb(genA1PiSSHighPt, genTauOneProng->visible.p4, genPolVecA1, genIPLVOneProng, firstNegative);
			}
		} // if 2 gen taus
	}

}

std::vector<TLorentzVector> GenTauCPProducerBase::GetInputPion(product_type& product,KGenTau* genTau) const
{
	std::vector<TLorentzVector> input;
	if (genTau)
	{
		input = GenTauCPProducerBase::SetupInputsPion(product, genTau);
	}

	return input;
}

std::vector<TLorentzVector> GenTauCPProducerBase::GetInputRho(product_type& product,KGenTau* genTau) const
{
	std::vector<TLorentzVector> input;
	if (genTau)
	{
		input = GenTauCPProducerBase::SetupInputsRho(product, genTau);
	}

	return input;
}

std::vector<TLorentzVector> GenTauCPProducerBase::GetInputA1(product_type& product,KGenTau* genTau) const
{
	std::vector<TLorentzVector> input;
	if (genTau)
	{
		input = GenTauCPProducerBase::SetupInputsA1(product, genTau);
	}

	return input;
}

std::vector<TLorentzVector> GenMatchedTauCPProducer::GetInputPion(product_type& product, KLepton* lepton) const
{
	std::vector<TLorentzVector> input;
	KGenTau* genTau = SafeMap::GetWithDefault(product.m_genTauMatchedLeptons, lepton, static_cast<KGenTau*>(nullptr));
	if (genTau)
	{
		input = GenTauCPProducerBase::SetupInputsPion(product, genTau);
	}

	return input;
}

std::vector<TLorentzVector> GenMatchedTauCPProducer::GetInputRho(product_type& product, KLepton* lepton) const
{
	std::vector<TLorentzVector> input;
	KGenTau* genTau = SafeMap::GetWithDefault(product.m_genTauMatchedLeptons, lepton, static_cast<KGenTau*>(nullptr));
	if (genTau)
	{
		input = GenTauCPProducerBase::SetupInputsRho(product, genTau);
	}

	return input;
}

std::vector<TLorentzVector> GenMatchedTauCPProducer::GetInputA1(product_type& product, KLepton* lepton) const
{
	std::vector<TLorentzVector> input;
	KGenTau* genTau = SafeMap::GetWithDefault(product.m_genTauMatchedLeptons, lepton, static_cast<KGenTau*>(nullptr));
	if (genTau)
	{
		input = GenTauCPProducerBase::SetupInputsA1(product, genTau);
	}

	return input;
}

std::vector<TLorentzVector> GenTauCPProducerBase::SetupInputsPion(product_type& product, KGenTau* genTau) const
{
	std::vector<TLorentzVector> input;
	if (genTau)
	{
		RMFLV* genTauVisibleLV = &(genTau->visible.p4);

		input.push_back(Utility::ConvertPtEtaPhiMLorentzVector<RMFLV, TLorentzVector>(genTau->p4));
		input.push_back(Utility::ConvertPtEtaPhiMLorentzVector<RMFLV, TLorentzVector>(*genTauVisibleLV));
	}

	return input;
}

std::vector<TLorentzVector> GenTauCPProducerBase::SetupInputsRho(product_type& product, KGenTau* genTau) const
{
	std::vector<TLorentzVector> input;
	KGenParticle* genParticle = SafeMap::GetWithDefault(product.m_validGenParticlesMap, genTau, static_cast<KGenParticle*>(nullptr));
	if (genParticle)
	{
		std::vector<KGenParticle*> genTauChargedHadrons = SafeMap::GetWithDefault(product.m_validGenTausChargedHadronsMap, genParticle, std::vector<KGenParticle*>());
		std::vector<KGenParticle*> genTauNeutralHadrons = SafeMap::GetWithDefault(product.m_validGenTausNeutralHadronsMap, genParticle, std::vector<KGenParticle*>());
		if ((genTau->nProngs == 1) && (genTau->nPi0s == 1) &&
		    (genTauChargedHadrons.size() == 1) && (genTauNeutralHadrons.size() == 1))
		{
			input.push_back(Utility::ConvertPtEtaPhiMLorentzVector<RMFLV, TLorentzVector>(genTau->p4));

			input.push_back(Utility::ConvertPtEtaPhiMLorentzVector<RMFLV, TLorentzVector>(genTauChargedHadrons.front()->p4));
			input.push_back(Utility::ConvertPtEtaPhiMLorentzVector<RMFLV, TLorentzVector>(genTauNeutralHadrons.front()->p4));
		}
	}

	return input;
}

std::vector<TLorentzVector> GenTauCPProducerBase::SetupInputsA1(product_type& product, KGenTau* genTau) const
{
	std::vector<TLorentzVector> input;
	KGenParticle* genParticle = SafeMap::GetWithDefault(product.m_validGenParticlesMap, genTau, static_cast<KGenParticle*>(nullptr));
	if (genParticle)
	{
		std::vector<KGenParticle*> genTauChargedHadrons = SafeMap::GetWithDefault(product.m_validGenTausChargedHadronsMap, genParticle, std::vector<KGenParticle*>());
		std::vector<KGenParticle*> genTauNeutralHadrons = SafeMap::GetWithDefault(product.m_validGenTausNeutralHadronsMap, genParticle, std::vector<KGenParticle*>());
		if ((genTau->nProngs == 3) && (genTau->nPi0s == 0) &&
		    (genTauChargedHadrons.size() == 3) && (genTauNeutralHadrons.size() == 0))
		{
			input.push_back(Utility::ConvertPtEtaPhiMLorentzVector<RMFLV, TLorentzVector>(genTau->p4));

			// sort pions from a1 decay according to their charge
			RMFLV* piSingleChargeSign = nullptr;
			RMFLV* piDoubleChargeSign1 = nullptr;
			RMFLV* piDoubleChargeSign2 = nullptr;
			if ((genTauChargedHadrons.at(0)->charge() * genTauChargedHadrons.at(1)->charge()) > 0.0)
			{
				piSingleChargeSign = &(genTauChargedHadrons.at(2)->p4);
				piDoubleChargeSign1 = &(genTauChargedHadrons.at(0)->p4);
				piDoubleChargeSign2 = &(genTauChargedHadrons.at(1)->p4);
			}
			else if ((genTauChargedHadrons.at(0)->charge() * genTauChargedHadrons.at(2)->charge()) > 0.0)
			{
				piSingleChargeSign = &(genTauChargedHadrons.at(1)->p4);
				piDoubleChargeSign1 = &(genTauChargedHadrons.at(0)->p4);
				piDoubleChargeSign2 = &(genTauChargedHadrons.at(2)->p4);
			}
			else // if ((genTauChargedHadrons.at(1)->charge() * genTauChargedHadrons.at(2)->charge()) > 0.0)
			{
				piSingleChargeSign = &(genTauChargedHadrons.at(0)->p4);
				piDoubleChargeSign1 = &(genTauChargedHadrons.at(1)->p4);
				piDoubleChargeSign2 = &(genTauChargedHadrons.at(2)->p4);
			}

			input.push_back(Utility::ConvertPtEtaPhiMLorentzVector<RMFLV, TLorentzVector>(*piSingleChargeSign));
			input.push_back(Utility::ConvertPtEtaPhiMLorentzVector<RMFLV, TLorentzVector>(*piDoubleChargeSign1));
			input.push_back(Utility::ConvertPtEtaPhiMLorentzVector<RMFLV, TLorentzVector>(*piDoubleChargeSign2));
		}
	}

	return input;
}

/* Gen version for 4-momenta of charged pions from a1 decay in 3-prongs tau decay */
bool GenMatchedTauCPProducer::genPionsFromRho3Prongs(product_type& product, KLepton* lepton,
					    RMFLV& genPiSSFromRhoMomentum,
					    RMFLV& genPiOSMomentum,
					    RMFLV& genPiSSHighMomentum) const
{

	//Reset 4-momenta
	genPiSSFromRhoMomentum.SetCoordinates(0,0,0,0);
	genPiOSMomentum.SetCoordinates(0,0,0,0);
	genPiSSHighMomentum.SetCoordinates(0,0,0,0);

	//Not 3-prongs tau
	KGenTau* genTau = SafeMap::GetWithDefault(product.m_genTauMatchedLeptons, lepton, static_cast<KGenTau*>(nullptr));
	if (genTau)
	{
		KGenParticle* genParticle = SafeMap::GetWithDefault(product.m_validGenParticlesMap, genTau, static_cast<KGenParticle*>(nullptr));
		if (genParticle)
		{
			std::vector<KGenParticle*> genTauChargedHadrons = SafeMap::GetWithDefault(product.m_validGenTausChargedHadronsMap, genParticle, std::vector<KGenParticle*>());
			std::vector<KGenParticle*> genTauNeutralHadrons = SafeMap::GetWithDefault(product.m_validGenTausNeutralHadronsMap, genParticle, std::vector<KGenParticle*>());
			// if ((genTau->nProngs == 3) && (genTau->nPi0s == 0) &&
			//     (genTauChargedHadrons.size() == 3) && (genTauNeutralHadrons.size() == 0))
			if ((genTau->nProngs == 3) && (genTauChargedHadrons.size() == 3))
			{
				// sort pions from a1 decay according to their charge
				KGenParticle* piSingleChargeSign = nullptr;
				KGenParticle* piDoubleChargeSign1 = nullptr;
				KGenParticle* piDoubleChargeSign2 = nullptr;
				if ((genTauChargedHadrons.at(0)->charge() * genTauChargedHadrons.at(1)->charge()) > 0.0)
				{
					piSingleChargeSign = genTauChargedHadrons.at(2);
					piDoubleChargeSign1 = genTauChargedHadrons.at(0);
					piDoubleChargeSign2 = genTauChargedHadrons.at(1);
				}
				else if ((genTauChargedHadrons.at(0)->charge() * genTauChargedHadrons.at(2)->charge()) > 0.0)
				{
					piSingleChargeSign = genTauChargedHadrons.at(1);
					piDoubleChargeSign1 = genTauChargedHadrons.at(0);
					piDoubleChargeSign2 = genTauChargedHadrons.at(2);
				}
				else // if ((genTauChargedHadrons.at(1)->charge() * genTauChargedHadrons.at(2)->charge()) > 0.0)
				{
					piSingleChargeSign = genTauChargedHadrons.at(0);
					piDoubleChargeSign1 = genTauChargedHadrons.at(1);
					piDoubleChargeSign2 = genTauChargedHadrons.at(2);
				}
				genPiOSMomentum = piSingleChargeSign->p4;

				//Look for charged pions pair from rho decay
				RMFLV rho1 = genPiOSMomentum + piDoubleChargeSign1->p4;
				RMFLV rho2 = genPiOSMomentum + piDoubleChargeSign2->p4;
				if ((std::abs(rho1.M()-DefaultValues::RhoMass)) < (std::abs(rho2.M()-DefaultValues::RhoMass)))
				{
					genPiSSFromRhoMomentum = piDoubleChargeSign1->p4;
				}
				else
				{
					genPiSSFromRhoMomentum = piDoubleChargeSign2->p4;
				}
				if (piDoubleChargeSign1->p4.pt() > piDoubleChargeSign2->p4.pt())
				{
					genPiSSHighMomentum = piDoubleChargeSign1->p4;
				}
				else
				{
					genPiSSHighMomentum = piDoubleChargeSign2->p4;
				}
			}
		}
	}

	return (genPiOSMomentum.pt() > 0 && genPiSSFromRhoMomentum.pt() > 0 && genPiSSHighMomentum.pt() > 0); //Sanity check
}
