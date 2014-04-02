
#pragma once

#include "Artus/Utility/interface/Utility.h"

#include "TauSpinner/SimpleParticle.h"
#include "TauSpinner/tau_reweight_lib.h"

#include "../HttTypes.h"

#include "Artus/Core/interface/GlobalInclude.h"
/**
   \brief GlobalProducer, for tau decays on generator level. Following quantities are calculated:
   
   -This producer has the product of the GenTauDecayProducer as input and calculates the TauSpinnerWeight 
   for these particles, where tau is the daughter of Higgs
   - the variable Phi* for the Higgs -> tau-tau+ (1-prong-decay), in this case currently only pions in the final state	


*/

class TauSpinnerProducer: public HttProducerBase {
public:
	
	virtual std::string GetProducerId() const ARTUS_CPP11_OVERRIDE {
		return "tauspinner";
	}
	
	TauSpinnerProducer() : HttProducerBase() {};

	void InitGlobal(global_setting_type const& globalSettings) ARTUS_CPP11_OVERRIDE
	{
		// interface to TauSpinner
		//Reading the settings from TauSpinnerSettings.json in following order:
		//name of PDF, CMSENE, Ipp, Ipol, nonSM2, nonSMN (see tau_reweight_lib.cxx), 
		//boosted/unboosted to Higgs CMF 
		stringvector tauSpinnerSettings = globalSettings.GetTauSpinnerSettings();
		Tauolapp::Tauola::initialize();
		string name= tauSpinnerSettings[0];
		LHAPDF::initPDFSetByName(name);
		double CMSENE = atof(tauSpinnerSettings[1].c_str());
		bool Ipp;
		std::istringstream(tauSpinnerSettings[2]) >> std::boolalpha >> Ipp;
		int Ipol,nonSM2,nonSMN;
		std::istringstream(tauSpinnerSettings[3]) >> Ipol;
		std::istringstream(tauSpinnerSettings[4]) >> nonSM2;
		std::istringstream(tauSpinnerSettings[5]) >> nonSMN;
		std::cout << "initialize: " << std::endl;
		TauSpinner::initialize_spinner(Ipp,Ipol,nonSM2,nonSMN,CMSENE);
	}

	virtual void ProduceGlobal(HttEvent const& event, HttProduct& product,
	                           HttGlobalSettings const& globalSettings) const ARTUS_CPP11_OVERRIDE
	{
	std::vector<KGenParticle*> higgs = product.m_genHiggs;
	std::vector<std::vector<KGenParticle*>> taus = product.m_genHiggsDaughters;
	std::vector<std::vector<std::vector<KGenParticle*>>> tauDaughters = product.m_genHiggsGranddaughters;


	//Conversion to SimpleParticles
	//select the particles to convert from Output of GenTauDecay Producer
	KGenParticle* selectedHiggs1 = higgs[0];
	//std::cout << "Higgs PdgId: " << selectedHiggs->pdgId();
	if (abs(taus[0][0]->pdgId())==15) //TauSpinner considers only Taus and Tau-Neutrinos as daughters of a Boson (Higgs, W etc.)
	{ 
		KGenParticle* selectedTau1 = taus[0][0];
		//std::cout << "		Tau1 PdgId: " << selectedTau1->pdgId();
		KGenParticle* selectedTau2 = taus[0][1];
		//std::cout << "		Tau2 PdgId: " << selectedTau2->pdgId() << std::endl;
		std::vector<KGenParticle*> selectedTauDaughters1 = tauDaughters[0][0];
		std::vector<KGenParticle*> selectedTauDaughters2 = tauDaughters[0][1];
		//Boosting following vectors to the center of mass system of the Higgs, if nessesary: Higgs, Tau1, Tau2
		//Information about boosting is read from TauSpinnerSettings.json, seventh entry. 	
		RMDataLV vec=selectedHiggs1->p4;
		RMDataLV::BetaVector boostvec = vec.BoostToCM();
		ROOT::Math::Boost boostMat(boostvec);
		bool boosted = (globalSettings.GetTauSpinnerSettings()[6]=="boosted");
		if(boosted)
		{
			selectedHiggs1->p4 = boostMat*(selectedHiggs1->p4);
			selectedTau1->p4 = boostMat*(selectedTau1->p4);
			selectedTau2->p4 = boostMat*(selectedTau2->p4);
		}
		TauSpinner::SimpleParticle X(selectedHiggs1->p4.px(), selectedHiggs1->p4.py(), selectedHiggs1->p4.pz(), selectedHiggs1->p4.e(), selectedHiggs1->pdgId());
		TauSpinner::SimpleParticle tau1(selectedTau1->p4.px(), selectedTau1->p4.py(), selectedTau1->p4.pz(), selectedTau1->p4.e(), selectedTau1->pdgId());
		TauSpinner::SimpleParticle tau2(selectedTau2->p4.px(), selectedTau2->p4.py(), selectedTau2->p4.pz(), selectedTau2->p4.e(), selectedTau2->pdgId());


		std::vector<TauSpinner::SimpleParticle> tauDaughters1;
		for(unsigned int i = 0; i < selectedTauDaughters1.size(); ++i)
		{
			if (boosted) selectedTauDaughters1[i]->p4 = boostMat*(selectedTauDaughters1[i]->p4); // boosting Tau1Daughters, if nessesary
			tauDaughters1.push_back(TauSpinner::SimpleParticle(selectedTauDaughters1[i]->p4.px(), selectedTauDaughters1[i]->p4.py(), selectedTauDaughters1[i]->p4.pz(), selectedTauDaughters1[i]->p4.e(), selectedTauDaughters1[i]->pdgId()));
		}

		std::vector<TauSpinner::SimpleParticle> tauDaughters2;
		for(unsigned int i = 0; i < selectedTauDaughters2.size(); ++i)
		{
			if (boosted) selectedTauDaughters2[i]->p4 = boostMat*(selectedTauDaughters2[i]->p4); // boosting Tau1Daughters, if nessesary
			tauDaughters2.push_back(TauSpinner::SimpleParticle(selectedTauDaughters2[i]->p4.px(), selectedTauDaughters2[i]->p4.py(), selectedTauDaughters2[i]->p4.pz(), selectedTauDaughters2[i]->p4.e(), selectedTauDaughters2[i]->pdgId()));
		}
		//std::cout << "getWeight: " << std::endl;
		/* Debug output for testing
		std::cout << selectedHiggs->p4.px() << std::endl;
		std::cout << selectedTau1->p4.px() << std::endl;
		std::cout << selectedTau2->p4.px() << std::endl;
		std::cout << selectedTauDaughters1[1]->p4.px() << std::endl;
		std::cout << selectedTauDaughters2[1]->p4.px() << std::endl;
		*/
	
		//Decision for a certain weight calculation depending on BosonPdgId
		stringvector bosonPdgIdVector = globalSettings.GetBosonPdgId();
		int bosonPdgId;
		std::istringstream(bosonPdgIdVector[0]) >> bosonPdgId;
		if(abs(bosonPdgId)==24) product.m_tauSpinnerWeight = calculateWeightFromParticlesWorHpn(X, tau1, tau2, tauDaughters1);
		else if (abs(bosonPdgId)==25) product.m_tauSpinnerWeight = calculateWeightFromParticlesH(X, tau1, tau2, tauDaughters1, tauDaughters2);
		//std::cout << "tauSpinnerWeight: " << (product.m_tauSpinnerWeight==1.00) << std::endl;


		///Calculation of Phi* for Higgs -> Tau+Tau- -> Pion+Pion- + XXXX (1-prong decay)


		//Selection of the right channel
		if((abs(selectedTau2->pdgId())==15)&&(selectedTauDaughters1.size()==2)&&(selectedTauDaughters2.size()==2))
		{
			//Initialization of Pions
			KGenParticle* Pion1 = selectedTauDaughters1[0]; 
			KGenParticle* Pion2 = selectedTauDaughters2[0];
			for(unsigned int i = 0; i < selectedTauDaughters1.size(); i++) 
			{ 
				if(abs(selectedTauDaughters1[i]->pdgId())==211) Pion1 = selectedTauDaughters1[i];
			}
			for(unsigned int i = 0; i < selectedTauDaughters2.size(); i++)
			{
				 if(abs(selectedTauDaughters2[i]->pdgId())==211) Pion2 = selectedTauDaughters2[i];
			}			 
			
			if((abs(Pion1->pdgId())==211)&&(abs(Pion2->pdgId())==211)) //check for the right channel
			{
				//std::cout << Pion1->pdgId() << "               " << Pion2->pdgId() << std::endl;
				
				//Calculation of Phi* itself


				//Step 1: Creating a Boost M into the ZMF of the Pion+Pion- decay
				RMDataLV PionImp=Pion1->p4+Pion2->p4;
				RMDataLV::BetaVector boostvec = PionImp.BoostToCM();
				ROOT::Math::Boost M(boostvec);
				


				//Step 2: Calculating impact parameter vectors n1 n2
				
				//Momentum vectors of the Pions
				RMDataLV::BetaVector p1,p2; 
				p1.SetXYZ(Pion1->p4.Px(), Pion1->p4.Py() ,Pion1->p4.Pz());
				p2.SetXYZ(Pion2->p4.Px(), Pion2->p4.Py() ,Pion2->p4.Pz());

				//Momentum vectors of the Taus
				RMDataLV::BetaVector k1,k2;
				k1.SetXYZ(selectedTau1->p4.Px(), selectedTau1->p4.Py() , selectedTau1->p4.Pz());
				k2.SetXYZ(selectedTau2->p4.Px(), selectedTau2->p4.Py() , selectedTau2->p4.Pz());

				//Not normalized n1, n2
				RMDataLV::BetaVector n1 = k1 - ((k1.Dot(p1))/(p1.Dot(p1)))*p1;
				RMDataLV::BetaVector n2 = k2 - ((k2.Dot(p2))/(p2.Dot(p2)))*p2;
				//Normalized n1, n2
				n1 = n1.Unit(); n2 = n2.Unit();
				//std::cout << n1.Dot(p1) << "            " << n2.Dot(p2) << std::endl;

				//Step 3: Boosting 4-vectors (n1,0), (n2,0), p1, p2 with M
				RMDataLV n1_mu, n2_mu;
				n1_mu.SetPxPyPzE(n1.X(),n1.Y(),n1.Z(), 0);
				n2_mu.SetPxPyPzE(n2.X(),n2.Y(),n2.Z(), 0);

				n1_mu = M*n1_mu; n2_mu = M*n2_mu; Pion1->p4 = M*Pion1->p4; Pion2->p4 = M*Pion2->p4;


				//Step 4: Calculation of the transverse component of n1, n2 to p1, p2 (after Boosting)
				n1.SetXYZ(n1_mu.Px(), n1_mu.Py(), n1_mu.Pz()); n2.SetXYZ(n2_mu.Px(), n2_mu.Py(), n2_mu.Pz());
				p1.SetXYZ(Pion1->p4.Px(),Pion1->p4.Py(),Pion1->p4.Pz()); p2.SetXYZ(Pion2->p4.Px(),Pion2->p4.Py(),Pion2->p4.Pz());

				RMDataLV::BetaVector n1t = n1 - ((n1.Dot(p1))/(p1.Dot(p1)))*p1; n1t = n1t.Unit();
 				RMDataLV::BetaVector n2t = n2 - ((n2.Dot(p2))/(p2.Dot(p2)))*p2; n2t = n2t.Unit();
				
				//std::cout <<  n1t.Dot(p1) << "                  " << n2t.Dot(p2) << std::endl;
				
				//Step 5: Calculating Phi*
				//std::cout <<  n1t.Dot(n2t) << std::endl;
				product.m_PhiStar = acos(n1t.Dot(n2t));
			}
			else product.m_PhiStar = UNDEFINED_VALUE;	 // Default value in case of a wrong channel 		
		}
		else product.m_PhiStar = UNDEFINED_VALUE;
	}// "if 1BosonDaughter is Tau"-end.
	else product.m_tauSpinnerWeight = UNDEFINED_VALUE;
	}
};


