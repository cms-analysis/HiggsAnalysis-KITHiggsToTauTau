
#include <iostream>

#include "TauSpinner/SimpleParticle.h"
#include "TauSpinner/tau_reweight_lib.h"


std::pair<double, double> GetTauSpinnerWeightSpin(
		TauSpinner::SimpleParticle boson,
		TauSpinner::SimpleParticle tau1,
		TauSpinner::SimpleParticle tau2,
		std::vector<TauSpinner::SimpleParticle> tauFinalStates1,
		std::vector<TauSpinner::SimpleParticle> tauFinalStates2,
		int nIterations=100
)
{
	double weight = 0.0;
	double spin = 0.0;
	for (int iteration = 0; iteration < nIterations; ++iteration)
	{
		weight = TauSpinner::calculateWeightFromParticlesH(boson, tau1, tau2, tauFinalStates1, tauFinalStates2);
		spin += TauSpinner::getTauSpin();
	}
	spin /= nIterations;
	if (spin > 0.0)
	{
		return std::pair<double, double>(weight, 1.0);
	}
	else if (spin < 0.0)
	{
		return std::pair<double, double>(weight, -1.0);
	}
	else
	{
		return std::pair<double, double>(weight, 0.0);
	}
}


int main(int argc, const char *argv[])
{
	Tauolapp::Tauola::initialize();
	LHAPDF::initPDFSetByName("MSTW2008nnlo90cl.LHgrid");
	
	TauSpinner::initialize_spinner(
			true, // Ipp
			2, // Ipol
			0, // NonSM2
			0, // NonSMN
			13000 // CmsEnergy()
	);
	
	TauSpinner::SimpleParticle boson(9.057124, 4.738310, 362.649353, 373.200989, 23);
	
	TauSpinner::SimpleParticle tau1(-7.145843, 32.856289, 59.924850, 68.736778, -15);
	
	std::vector<TauSpinner::SimpleParticle> tauFinalStates1;
	tauFinalStates1.push_back(TauSpinner::SimpleParticle(-0.471688, 3.796974, 7.760280, 8.652251, -16)); // neutrino
	tauFinalStates1.push_back(TauSpinner::SimpleParticle(-6.674153, 29.059315, 52.164566, 60.084522, 211)); // pion
	
	TauSpinner::SimpleParticle tau2(16.202969, -28.117977, 302.724579, 304.464264, 15);
	
	std::vector<TauSpinner::SimpleParticle> tauFinalStates2;
	tauFinalStates2.push_back(TauSpinner::SimpleParticle(13.371717, -21.770473, 237.549759, 238.919739, 16)); // neutrino
	tauFinalStates2.push_back(TauSpinner::SimpleParticle(2.831248, -6.347505, 65.174820, 65.544518, -211)); // pion

	std::pair<double, double> weightSpin = GetTauSpinnerWeightSpin(boson, tau1, tau2, tauFinalStates1, tauFinalStates2);
	std::cout << "weight = " << weightSpin.first << "; spin = " << weightSpin.second << std::endl;
	
	weightSpin = GetTauSpinnerWeightSpin(boson, tau1, tau2, tauFinalStates1, tauFinalStates2);
	std::cout << "weight = " << weightSpin.first << "; spin = " << weightSpin.second << std::endl;
	
	weightSpin = GetTauSpinnerWeightSpin(boson, tau1, tau2, tauFinalStates1, tauFinalStates2);
	std::cout << "weight = " << weightSpin.first << "; spin = " << weightSpin.second << std::endl;
	
	weightSpin = GetTauSpinnerWeightSpin(boson, tau1, tau2, tauFinalStates1, tauFinalStates2);
	std::cout << "weight = " << weightSpin.first << "; spin = " << weightSpin.second << std::endl;
	
	weightSpin = GetTauSpinnerWeightSpin(boson, tau1, tau2, tauFinalStates1, tauFinalStates2);
	std::cout << "weight = " << weightSpin.first << "; spin = " << weightSpin.second << std::endl;
	
	weightSpin = GetTauSpinnerWeightSpin(boson, tau1, tau2, tauFinalStates1, tauFinalStates2);
	std::cout << "weight = " << weightSpin.first << "; spin = " << weightSpin.second << std::endl;
	
	weightSpin = GetTauSpinnerWeightSpin(boson, tau1, tau2, tauFinalStates1, tauFinalStates2);
	std::cout << "weight = " << weightSpin.first << "; spin = " << weightSpin.second << std::endl;
	
	weightSpin = GetTauSpinnerWeightSpin(boson, tau1, tau2, tauFinalStates1, tauFinalStates2);
	std::cout << "weight = " << weightSpin.first << "; spin = " << weightSpin.second << std::endl;
	
	weightSpin = GetTauSpinnerWeightSpin(boson, tau1, tau2, tauFinalStates1, tauFinalStates2);
	std::cout << "weight = " << weightSpin.first << "; spin = " << weightSpin.second << std::endl;
	
	weightSpin = GetTauSpinnerWeightSpin(boson, tau1, tau2, tauFinalStates1, tauFinalStates2);
	std::cout << "weight = " << weightSpin.first << "; spin = " << weightSpin.second << std::endl;
	
	weightSpin = GetTauSpinnerWeightSpin(boson, tau1, tau2, tauFinalStates1, tauFinalStates2);
	std::cout << "weight = " << weightSpin.first << "; spin = " << weightSpin.second << std::endl;
	
	weightSpin = GetTauSpinnerWeightSpin(boson, tau1, tau2, tauFinalStates1, tauFinalStates2);
	std::cout << "weight = " << weightSpin.first << "; spin = " << weightSpin.second << std::endl;
	
	weightSpin = GetTauSpinnerWeightSpin(boson, tau1, tau2, tauFinalStates1, tauFinalStates2);
	std::cout << "weight = " << weightSpin.first << "; spin = " << weightSpin.second << std::endl;
	
	weightSpin = GetTauSpinnerWeightSpin(boson, tau1, tau2, tauFinalStates1, tauFinalStates2);
	std::cout << "weight = " << weightSpin.first << "; spin = " << weightSpin.second << std::endl;
	
	weightSpin = GetTauSpinnerWeightSpin(boson, tau1, tau2, tauFinalStates1, tauFinalStates2);
	std::cout << "weight = " << weightSpin.first << "; spin = " << weightSpin.second << std::endl;
	
	weightSpin = GetTauSpinnerWeightSpin(boson, tau1, tau2, tauFinalStates1, tauFinalStates2);
	std::cout << "weight = " << weightSpin.first << "; spin = " << weightSpin.second << std::endl;
	
	return 0;
}
