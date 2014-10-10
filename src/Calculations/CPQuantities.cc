
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Calculations/CPQuantities.h"

// this version uses tau 4-momenta to calculate decay planes (usefull for GenTauCPProducer)
double CPQuantities::CalculatePhiStarCP(RMDataLV tau1, RMDataLV tau2, RMDataLV chargPart1, RMDataLV chargPart2)
{
	//Momentum vectors of the Taus
	RMDataLV::BetaVector k1, k2;
	k1.SetXYZ(tau1.Px(), tau1.Py() , tau1.Pz());
	k2.SetXYZ(tau2.Px(), tau2.Py() , tau2.Pz());
	return this->CalculatePhiStarCPSame(k1, k2, chargPart1, chargPart2, "gen");
}
// this version uses track and vertex information to calculate the decay planes (usefull for RecoTauCPProducer)
double CPQuantities::CalculatePhiStarCP(KDataVertex pv, KDataTrack track1, KDataTrack track2,  RMDataLV chargPart1, RMDataLV chargPart2)
{
	//Primary vertex
	RMDataLV::BetaVector pvpos;
	pvpos.SetXYZ((pv.position).X(), (pv.position).Y(), (pv.position).Z());

	//Points on tau tracks
	RMDataLV::BetaVector track1pos, track2pos;
	track1pos.SetXYZ((track1.ref).X(), (track1.ref).Y(), (track1.ref).Z());
	track2pos.SetXYZ((track2.ref).X(), (track2.ref).Y(), (track2.ref).Z());

	//Flight direction of taus determined from pv and trackpos
	RMDataLV::BetaVector k1, k2;
	k1 = track1pos - pvpos;
	k2 = track2pos - pvpos;
	return this->CalculatePhiStarCPSame(k1, k2, chargPart1, chargPart2, "reco");

}
// calculation of variables Phi* and Phi*CP
double CPQuantities::CalculatePhiStarCPSame(RMDataLV::BetaVector k1, RMDataLV::BetaVector k2, RMDataLV chargPart1, RMDataLV chargPart2, std::string level)
{
	//Step 1: Creating a Boost M into the ZMF of the (chargPart1+, chargedPart2-) decay
	RMDataLV ProngImp = chargPart1 + chargPart2;
	RMDataLV::BetaVector boostvec = ProngImp.BoostToCM();
	ROOT::Math::Boost M(boostvec);
	//Step 2: Calculating impact parameter vectors n1 n2

	//Momentum vectors of the charged particles
	RMDataLV::BetaVector p1, p2;
	p1.SetXYZ(chargPart1.Px(), chargPart1.Py() , chargPart1.Pz());
	p2.SetXYZ(chargPart2.Px(), chargPart2.Py() , chargPart2.Pz());
	
	//Not normalized n1, n2
	RMDataLV::BetaVector n1 = k1 - ((k1.Dot(p1)) / (p1.Dot(p1))) * p1;
	RMDataLV::BetaVector n2 = k2 - ((k2.Dot(p2)) / (p2.Dot(p2))) * p2;
	
	if(level=="reco")
	{
		this->SetrecoIP1(n1.R());
		this->SetrecoIP2(n2.R());
	}
	//Normalized n1, n2
	n1 = n1.Unit();
	n2 = n2.Unit();

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

	if(level=="reco")
	{
		this->SetrecoPhiStar(acos(n2t.Dot(n1t)));
	}
	else if (level=="gen")
	{
		this->SetgenPhiStar(acos(n2t.Dot(n1t)));
	}
	//Step 5: Calculating Phi*CP
	double phiStarCP = 0;
	if(p1n.Dot(n2t.Cross(n1t))>=0)
	{
		phiStarCP = acos(n2t.Dot(n1t));
	}
	else
	{
		phiStarCP = 2*ROOT::Math::Pi()-acos(n2t.Dot(n1t));
	}
	return phiStarCP;
}
// calculation of the hadron Energies in the approximate diTau restframe
double CPQuantities::CalculateChargedHadronEnergy(RMDataLV diTauMomentum, RMDataLV chargHad)
{
	// Step 1: Creating Boost into diTau rest frame
	RMDataLV::BetaVector boostditau = diTauMomentum.BoostToCM();
	ROOT::Math::Boost Mditau(boostditau);
	// Step 2: Boosting hadron and extracting energy
	chargHad = Mditau * chargHad;
	return chargHad.E();
}
// estimation of the impact parameter error (used on recostruction level)
double CPQuantities::CalculateTrackReferenceError(KDataTrack track)
{
	return sqrt(track.errDz*track.errDz+track.errDxy*track.errDxy);
}
// calculation of the angle Phi between the tau decay planes
double CPQuantities::CalculatePhiCP(RMDataLV boson, RMDataLV tau1, RMDataLV tau2, RMDataLV chargPart1, RMDataLV chargPart2)
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
	RMDataLV::BetaVector km, pm, pp, nm, np, ez;
	km.SetXYZ(tau1.Px(),tau1.Py(),tau1.Pz());
	pm.SetXYZ(chargPart1.Px(),chargPart1.Py(),chargPart1.Pz());
	pp.SetXYZ(chargPart2.Px(),chargPart2.Py(),chargPart2.Pz());

	nm = (km.Cross(pm)).Unit(); np = (km.Cross(pp)).Unit(); ez = pm.Unit();

	// Step 4: Calculating PhiCP
	this->SetgenPhi(acos(np.Dot(nm)));
	double phiCP = 0;
	if(ez.Dot(np.Cross(nm))>=0)
	{
		phiCP = acos(np.Dot(nm));
	}
	else
	{
		phiCP = 2*ROOT::Math::Pi()-acos(np.Dot(nm));
	}
	return phiCP;
}
// calculation of the charged prong energy in tau restframe
double CPQuantities::CalculateChargedProngEnergy(RMDataLV tau, RMDataLV chargedProng)
{
	// Step 1: Creating boost to Tau restframe
	RMDataLV::BetaVector boosttauvect = tau.BoostToCM();
	ROOT::Math::Boost TauRestFrame(boosttauvect);

	// Step 2: Boosting charged Prong 4-momentum vector and extracting energy
	chargedProng = TauRestFrame * chargedProng;
	return chargedProng.E();
}
// calculation of the angle between the hadron and the tau-neutrino flight directions
double CPQuantities::CalculateThetaNuHadron(RMDataLV tau, RMDataLV nuTau, RMDataLV hadron)
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
	double theta  = acos(nuVec.Dot(hadVec));
	return theta;
}
// calculation of the angle between the tau-neutrino and the tau-antineutrino flight directions
double CPQuantities::CalculateAlphaTauNeutrinos(RMDataLV tauM, RMDataLV nuTauM, RMDataLV tauP, RMDataLV nuTauP)
{
	// Step 1: Creating boosts to tau restframes
	RMDataLV::BetaVector boostTauMVec = tauM.BoostToCM();
	RMDataLV::BetaVector boostTauPVec = tauP.BoostToCM();

	ROOT::Math::Boost TauMRestFrame(boostTauMVec);
	ROOT::Math::Boost TauPRestFrame(boostTauPVec);

	// Step 2: Boosting neutrino 4-momentum vectors
	nuTauM = TauMRestFrame * nuTauM;
	nuTauP = TauPRestFrame * nuTauP;

	// Step 3: Extracting boosted 3-momentum vectors and normalizing them
	RMDataLV::BetaVector nuMVec, nuPVec;
	nuMVec.SetXYZ(nuTauM.Px(),nuTauM.Py(),nuTauM.Pz());
	nuPVec.SetXYZ(nuTauP.Px(),nuTauP.Py(),nuTauP.Pz());

	nuMVec = nuMVec.Unit();
	nuPVec = nuPVec.Unit();

	// Step 4 Calculating Alpha
	double alpha  = acos(nuMVec.Dot(nuPVec));
	return alpha;
}
double CPQuantities::CalculateZPlusMinus(RMDataLV higgs, RMDataLV chargedPart)
{
	//calculating boost into higgs restframe
	RMDataLV::BetaVector boostHiggs = higgs.BoostToCM();
	ROOT::Math::Boost higgsRestFrame(boostHiggs);

	//boost particles into rest frame
	higgs = higgsRestFrame * higgs;
	chargedPart = higgsRestFrame * chargedPart;

	// calculate Z+-
	double zPlusMinus = 2 * chargedPart.E() / higgs.E();
	return zPlusMinus;
}
double CPQuantities::CalculateZs(double zPlus, double zMinus)
{
	//calculate the surface between z+ = z- and z+ = z- + a for each event
	//z+ and z- are in range [0,1]. So maximum surface is 0.5
	//negative a defines the surface below the diagonal line
	double a = zPlus - zMinus;
	double zs = 0;
	if (a >= 0)
	{
		zs = 0.5 * (1 - ((1 - a) * (1 - a)));
	}
	else
	{
		a = -a;
		zs = 0.5 * (1 - ((1 - a) * (1 - a)));
		zs = -zs;
	}
	return zs;
}
double CPQuantities::PhiTransform(double phi)
{
	phi = 	fmod((phi + ROOT::Math::Pi()),(2 * ROOT::Math::Pi()));
	return phi;
}
