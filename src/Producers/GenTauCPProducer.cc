

#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/GenTauCPProducer.h"

#include "Artus/Utility/interface/DefaultValues.h"

void GenTauCPProducer::ProduceGlobal(HttEvent const& event, HttProduct& product,
									 HttGlobalSettings const& globalSettings) const
{
	std::vector<KappaProduct::MotherDaughterBundle> higgs = product.m_genBoson;
	KGenParticle* selectedTau1 = higgs[0].Daughters[0].node;
	KGenParticle* selectedTau2 = higgs[0].Daughters[1].node;
	std::vector<KappaProduct::MotherDaughterBundle> selectedTauDaughters1 = higgs[0].Daughters[0].Daughters;
	std::vector<KappaProduct::MotherDaughterBundle> selectedTauDaughters2 = higgs[0].Daughters[1].Daughters;
	//Selection of the right channel

	if ((abs(selectedTau1->pdgId()) == 15) && (abs(selectedTau2->pdgId()) == 15) && (selectedTauDaughters1.size() == 2) && (selectedTauDaughters2.size() == 2))
	{
		//Initialization of Pions
		KGenParticle* Pion1 = selectedTauDaughters1[0].node;
		KGenParticle* Pion2 = selectedTauDaughters2[0].node;
		for (unsigned int i = 0; i < selectedTauDaughters1.size(); i++)
		{
			if (abs(selectedTauDaughters1[i].node->pdgId()) == 211) Pion1 = selectedTauDaughters1[i].node;
		}
		for (unsigned int i = 0; i < selectedTauDaughters2.size(); i++)
		{
			if (abs(selectedTauDaughters2[i].node->pdgId()) == 211) Pion2 = selectedTauDaughters2[i].node;
		}

		if ((abs(Pion1->pdgId()) == 211) && (abs(Pion2->pdgId()) == 211)) //check for the right channel
		{
			LOG(DEBUG) << Pion1->pdgId() << "               " << Pion2->pdgId() << std::endl;

			//Calculation of Phi* and Psi*CP itself

			GenTauCPProducer::PhiPsiStarCalc(selectedTau1->p4, selectedTau2->p4, Pion1->p4, Pion2->p4, product);
			
			// Calculatiion of the angle Phi as angle betweeen normal vectors of Tau- -> Pi- and Tau+ -> Pi+ 
			// decay planes 
			GenTauCPProducer::PhiCalc(higgs[0].node->p4, selectedTau1->p4, selectedTau2->p4, Pion1->p4, Pion2->p4, product);						
 		}
		else
		{
			product.m_genPhiStar = DefaultValues::UndefinedDouble;	 // Default value in case of a wrong channel
			product.m_genPsiStarCP = DefaultValues::UndefinedDouble;
			product.m_genPhi = DefaultValues::UndefinedDouble;
		}
	}
	else
	{
		product.m_genPhiStar = DefaultValues::UndefinedDouble;
		product.m_genPsiStarCP = DefaultValues::UndefinedDouble;
		product.m_genPhi = DefaultValues::UndefinedDouble;
	}

}

void GenTauCPProducer::PhiPsiStarCalc(RMDataLV tau1, RMDataLV tau2, RMDataLV pion1, RMDataLV pion2, HttProduct& product) const
{
	//Step 1: Creating a Boost M into the ZMF of the Pion+Pion- decay
	RMDataLV PionImp = pion1 + pion2;
	RMDataLV::BetaVector boostvec = PionImp.BoostToCM();
	ROOT::Math::Boost M(boostvec);



	//Step 2: Calculating impact parameter vectors n1 n2

	//Momentum vectors of the Pions
	RMDataLV::BetaVector p1, p2;
	p1.SetXYZ(pion1.Px(), pion1.Py() , pion1.Pz());
	p2.SetXYZ(pion2.Px(), pion2.Py() , pion2.Pz());

	//Momentum vectors of the Taus
	RMDataLV::BetaVector k1, k2;
	k1.SetXYZ(tau1.Px(), tau1.Py() , tau1.Pz());
	k2.SetXYZ(tau2.Px(), tau2.Py() , tau2.Pz());

	//Not normalized n1, n2
	RMDataLV::BetaVector n1 = k1 - ((k1.Dot(p1)) / (p1.Dot(p1))) * p1;
	RMDataLV::BetaVector n2 = k2 - ((k2.Dot(p2)) / (p2.Dot(p2))) * p2;
	//Normalized n1, n2
	n1 = n1.Unit();
	n2 = n2.Unit();

	LOG(DEBUG) << n1.Dot(p1) << "            " << n2.Dot(p2) << std::endl;

	//Step 3: Boosting 4-vectors (n1,0), (n2,0), p1, p2 with M
	RMDataLV n1_mu, n2_mu;
	n1_mu.SetPxPyPzE(n1.X(), n1.Y(), n1.Z(), 0);
	n2_mu.SetPxPyPzE(n2.X(), n2.Y(), n2.Z(), 0);

	n1_mu = M * n1_mu;
	n2_mu = M * n2_mu;
	pion1 = M * pion1;
	pion2 = M * pion2;

	//Step 4: Calculation of the transverse component of n1, n2 to p1, p2 (after Boosting)
	n1.SetXYZ(n1_mu.Px(), n1_mu.Py(), n1_mu.Pz());
	n2.SetXYZ(n2_mu.Px(), n2_mu.Py(), n2_mu.Pz());
	p1.SetXYZ(pion1.Px(), pion1.Py(), pion1.Pz());
	p2.SetXYZ(pion2.Px(), pion2.Py(), pion2.Pz());

	RMDataLV::BetaVector n1t = n1 - ((n1.Dot(p1)) / (p1.Dot(p1))) * p1;
	n1t = n1t.Unit();
	RMDataLV::BetaVector n2t = n2 - ((n2.Dot(p2)) / (p2.Dot(p2))) * p2;
	n2t = n2t.Unit();
	RMDataLV::BetaVector p1n = p1.Unit();
	LOG(DEBUG) <<  n1t.Dot(p1) << "                  " << n2t.Dot(p2) << std::endl;

	//Step 5: Calculating Phi* and Psi*CP
	product.m_genPhiStar = acos(n1t.Dot(n2t));
	product.m_genPsiStarCP = acos(p1n.Dot(n1t.Cross(n2t)));
	LOG(DEBUG)  << "Phi*: " << product.m_genPhiStar << "   " <<  "Psi*CP: "  << product.m_genPsiStarCP << std::endl;	
}

void GenTauCPProducer::PhiCalc(RMDataLV higgs, RMDataLV tau1, RMDataLV tau2, RMDataLV pion1, RMDataLV pion2, HttProduct& product) const
{
	// Step 1: Boosts into the Tau-(Tau+) rest frames to boost Pion 4-momentums
	RMDataLV::BetaVector boostvectm = tau1.BoostToCM();
	RMDataLV::BetaVector boostvectp = tau2.BoostToCM();
	RMDataLV::BetaVector boostvech = higgs.BoostToCM();			
	ROOT::Math::Boost Mtm(boostvectm);
	ROOT::Math::Boost Mtp(boostvectp);
	ROOT::Math::Boost Mh(boostvech);

	// Step 2: Boosting the 4-momentum vectors to respective rest frames: tau to Higgs rest frame, Pions 
	// to tau rest frames.
	tau1 = Mh * tau1;
	tau2 = Mh * tau2;

	//std::cout << tau1 << "               " << -1*tau2 << std::endl;

	pion1 = Mtm * pion1;
	pion2 = Mtp * pion2;

	// Step 3: Creating 3-momentum normal vectors on decay planes
	RMDataLV::BetaVector km, pm, pp, nm, np;
	km.SetXYZ(tau1.Px(),tau1.Py(),tau1.Pz());  
	pm.SetXYZ(pion1.Px(),pion1.Py(),pion1.Pz()); 
	pp.SetXYZ(pion2.Px(),pion2.Py(),pion2.Pz());
 
	nm = (km.Cross(pm)).Unit(); np = (km.Cross(pp)).Unit();

	// Step 4: Calculating Phi
	product.m_genPhi = acos(nm.Dot(np));
	//std::cout << product.m_genPhi << std::endl;

}

