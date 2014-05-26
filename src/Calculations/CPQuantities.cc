
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Calculations/CPQuantities.h"


std::pair<float, float> CPQuantities::CalculatePhiPsiStar(RMDataLV tau1, RMDataLV tau2, RMDataLV chargPart1, RMDataLV chargPart2)
{
	//Step 1: Creating a Boost M into the ZMF of the (chargPart1+, chargedPart2-) decay
	RMDataLV PionImp = chargPart1 + chargPart2;
	RMDataLV::BetaVector boostvec = PionImp.BoostToCM();
	ROOT::Math::Boost M(boostvec);

	//Step 2: Calculating impact parameter vectors n1 n2

	//Momentum vectors of the charged particles
	RMDataLV::BetaVector p1, p2;
	p1.SetXYZ(chargPart1.Px(), chargPart1.Py() , chargPart1.Pz());
	p2.SetXYZ(chargPart2.Px(), chargPart2.Py() , chargPart2.Pz());

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
	chargPart1 = M * chargPart1;
	chargPart2 = M * chargPart2;

	//Step 4: Calculation of the transverse component of n1, n2 to p1, p2 (after Boosting)
	n1.SetXYZ(n1_mu.Px(), n1_mu.Py(), n1_mu.Pz());
	n2.SetXYZ(n2_mu.Px(), n2_mu.Py(), n2_mu.Pz());
	p1.SetXYZ(chargPart1.Px(), chargPart1.Py(), chargPart1.Pz());
	p2.SetXYZ(chargPart2.Px(), chargPart2.Py(), chargPart2.Pz());

	RMDataLV::BetaVector n1t = n1 - ((n1.Dot(p1)) / (p1.Dot(p1))) * p1;
	n1t = n1t.Unit();
	RMDataLV::BetaVector n2t = n2 - ((n2.Dot(p2)) / (p2.Dot(p2))) * p2;
	n2t = n2t.Unit();
	RMDataLV::BetaVector p1n = p1.Unit();
	LOG(DEBUG) <<  n1t.Dot(p1) << "                  " << n2t.Dot(p2) << std::endl;

	//Step 5: Calculating Phi* and Psi*CP
	std::pair<float, float> phiPsiStar = std::make_pair(acos(n1t.Dot(n2t)), acos(p1n.Dot(n1t.Cross(n2t))));
	LOG(DEBUG)  << "Phi*: " << phiPsiStar.first << "   " <<  "Psi*CP: "  << phiPsiStar.second;
	return phiPsiStar;
}

float CPQuantities::CalculatePhi(RMDataLV boson, RMDataLV tau1, RMDataLV tau2, RMDataLV chargPart1, RMDataLV chargPart2)
{
	// Step 1: Boosts into the Tau-(Tau+) rest frames to boost charged particles 4-momentums
	RMDataLV::BetaVector boostvectm = tau1.BoostToCM();
	RMDataLV::BetaVector boostvectp = tau2.BoostToCM();
	RMDataLV::BetaVector boostvech = boson.BoostToCM();
	ROOT::Math::Boost Mtm(boostvectm);
	ROOT::Math::Boost Mtp(boostvectp);
	ROOT::Math::Boost Mh(boostvech);

	// Step 2: Boosting the 4-momentum vectors to respective rest frames: tau to boson rest frame,
	// charged particles to tau rest frames.
	tau1 = Mh * tau1;
	tau2 = Mh * tau2;

	//std::cout << tau1 << "               " << -1*tau2 << std::endl;

	chargPart1 = Mtm * chargPart1;
	chargPart2 = Mtp * chargPart2;

	// Step 3: Creating 3-momentum normal vectors on decay planes
	RMDataLV::BetaVector km, pm, pp, nm, np;
	km.SetXYZ(tau1.Px(),tau1.Py(),tau1.Pz());
	pm.SetXYZ(chargPart1.Px(),chargPart1.Py(),chargPart1.Pz());
	pp.SetXYZ(chargPart2.Px(),chargPart2.Py(),chargPart2.Pz());

	nm = (km.Cross(pm)).Unit(); np = (km.Cross(pp)).Unit();

	// Step 4: Calculating Phi
	float phi = acos(nm.Dot(np));
	LOG(DEBUG)  << "Phi: " << phi;
	return phi;
}
float CPQuantities::CalculateThetaNuHadron(RMDataLV tau, RMDataLV nuTau, RMDataLV hadron)
{
	// Step 1: Creating boost to Tau- restframe
	RMDataLV::BetaVector boosttauvect = tau.BoostToCM();
	ROOT::Math::Boost TauRestFrame(boosttauvect);

	// Step 2: Boosting neutrino and hadron 4-momentum vectors
	nuTau = TauRestFrame * nuTau;
	hadron = TauRestFrame * hadron;

	// Step 3: Extracting boosted 3-momentum vectors and normalizing them
	
	RMDataLV::BetaVector nuVec, hadVec;
	nuVec.SetXYZ(nuTau.Px(),nuTau.Py(),nuTau.Pz());
	hadVec.SetXYZ(hadron.Px(),hadron.Py(),hadron.Pz());

	nuVec = nuVec.Unit();
	hadVec = hadVec.Unit();

	// Step 4: Calculating Theta
	float theta  = acos(nuVec.Dot(hadVec));
	return theta;
}

