

#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/GenTauCPProducer.h"

void GenTauCPProducer::ProduceGlobal(HttEvent const& event, HttProduct& product,
	                           HttGlobalSettings const& globalSettings) const
{	
	std::vector<KappaProduct::MotherDaughterBundle> higgs = product.m_genBoson;
	KGenParticle* selectedTau1 = higgs[0].Daughters[0].node;
	KGenParticle* selectedTau2 = higgs[0].Daughters[1].node;
	std::vector<KappaProduct::MotherDaughterBundle> selectedTauDaughters1 = higgs[0].Daughters[0].Daughters;
	std::vector<KappaProduct::MotherDaughterBundle> selectedTauDaughters2 = higgs[0].Daughters[1].Daughters;
	//Selection of the right channel
	if((abs(selectedTau1->pdgId())==15)&&(abs(selectedTau2->pdgId())==15)&&(selectedTauDaughters1.size()==2)&&(selectedTauDaughters2.size()==2))
	{
		//Initialization of Pions
		KGenParticle* Pion1 = selectedTauDaughters1[0].node; 
		KGenParticle* Pion2 = selectedTauDaughters2[0].node;
		for(unsigned int i = 0; i < selectedTauDaughters1.size(); i++) 
		{ 
			if(abs(selectedTauDaughters1[i].node->pdgId())==211) Pion1 = selectedTauDaughters1[i].node;
		}
		for(unsigned int i = 0; i < selectedTauDaughters2.size(); i++)
		{
			 if(abs(selectedTauDaughters2[i].node->pdgId())==211) Pion2 = selectedTauDaughters2[i].node;
		}			 
		
		if((abs(Pion1->pdgId())==211)&&(abs(Pion2->pdgId())==211)) //check for the right channel
		{
			LOG(DEBUG) << Pion1->pdgId() << "               " << Pion2->pdgId() << std::endl;
			
			//Calculation of Phi* and Psi*CP itself


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
			
			LOG(DEBUG) << n1.Dot(p1) << "            " << n2.Dot(p2) << std::endl;

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
			RMDataLV::BetaVector p1n = p1.Unit();
			LOG(DEBUG) <<  n1t.Dot(p1) << "                  " << n2t.Dot(p2) << std::endl;
			
			//Step 5: Calculating Phi* and Psi*CP
			product.m_PhiStar = acos(n1t.Dot(n2t));
			product.m_PsiStarCP = acos(p1n.Dot(n1t.Cross(n2t)));
			LOG(DEBUG)  << "Phi*: " << product.m_PhiStar << "   " <<  "Psi*CP: "  << product.m_PsiStarCP << std::endl;
		}
		else
		{
			product.m_PhiStar = UNDEFINED_VALUE;	 // Default value in case of a wrong channel
			product.m_PsiStarCP = UNDEFINED_VALUE;
		} 		
	}
	else
	{
		product.m_PhiStar = UNDEFINED_VALUE;
		product.m_PsiStarCP = UNDEFINED_VALUE;
	}
	
}
