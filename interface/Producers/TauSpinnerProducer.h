
#pragma once

#include "Artus/Utility/interface/EnumHelper.h"

#include "TauSpinner/SimpleParticle.h"
#include "TauSpinner/tau_reweight_lib.h"

#include "../HttTypes.h"

#include "Artus/Core/interface/GlobalInclude.h"



class TauSpinnerProducer: public HttProducerBase {
public:

	virtual std::string GetProducerId() const ARTUS_CPP11_OVERRIDE {
		return "tauspinner";
	}
	
	TauSpinnerProducer() : HttProducerBase() {};

	virtual void ProduceGlobal(HttEvent const& event, HttProduct& product,
	                           HttGlobalSettings const& globalSettings) const ARTUS_CPP11_OVERRIDE
	{

	///////////replace this part by output of GenTauDecay Producer
	std::cout << "ProduceGlobal aus TauSpinner" << std::endl;
	std::vector<KGenParticle*> higgs; // Higgs event
	std::vector<KGenParticle*> taus;// vector von taus
	std::vector<std::vector<KGenParticle*>> tauDaughters;// vector von vector von daughters

	for (KGenParticles::iterator part = event.m_genParticles->begin();
		 part != event.m_genParticles->end(); ++part)
	{
		if (abs(part->pdgId()) == 15) // found tau
		{
			taus.push_back(&(*part));
			std::vector<KGenParticle*> tauDaughter;
			for (unsigned int d=0; d<part->daughterIndices.size(); ++d)
			{
				
				if (part->daughterIndex(d) < event.m_genParticles->size())
				{
					tauDaughter.push_back(&(event.m_genParticles->at(part->daughterIndex(d))));
				}
			}
			tauDaughters.push_back(tauDaughter);
		}
		else if (abs(part->pdgId()) == 25) // found higgs
		{
			higgs.push_back(&(*part));
		}
	///////////end of replacement
	}


	//Conversion to SimpleParticles
	//select the particles to convert from Output of GenTauDecay Producer
	
	KGenParticle* selectedHiggs = higgs[0];
	KGenParticle* selectedTau1 = taus[2];
	KGenParticle* selectedTau2 = taus[3];
	std::vector<KGenParticle*> selectedTauDaughters1 = tauDaughters[2];
	std::vector<KGenParticle*> selectedTauDaughters2 = tauDaughters[3];

	TauSpinner::SimpleParticle X(selectedHiggs->p4.px(), selectedHiggs->p4.py(), selectedHiggs->p4.pz(), selectedHiggs->p4.e(), selectedHiggs->pdgId());
	TauSpinner::SimpleParticle tau1(selectedTau1->p4.px(), selectedTau1->p4.py(), selectedTau1->p4.pz(), selectedTau1->p4.e(), selectedTau1->pdgId());
	TauSpinner::SimpleParticle tau2(selectedTau2->p4.px(), selectedTau2->p4.py(), selectedTau2->p4.pz(), selectedTau2->p4.e(), selectedTau2->pdgId());


	std::vector<TauSpinner::SimpleParticle> tauDaughters1;
	for(unsigned int i = 0; i < selectedTauDaughters1.size(); ++i)
	{
		tauDaughters1.push_back(TauSpinner::SimpleParticle(selectedTauDaughters1[i]->p4.px(), selectedTauDaughters1[i]->p4.py(), selectedTauDaughters1[i]->p4.pz(), selectedTauDaughters1[i]->p4.e(), selectedTauDaughters1[i]->pdgId()));
	}

	std::vector<TauSpinner::SimpleParticle> tauDaughters2;
	for(unsigned int i = 0; i < selectedTauDaughters2.size(); ++i)
	{
		tauDaughters2.push_back(TauSpinner::SimpleParticle(selectedTauDaughters2[i]->p4.px(), selectedTauDaughters2[i]->p4.py(), selectedTauDaughters2[i]->p4.pz(), selectedTauDaughters2[i]->p4.e(), selectedTauDaughters2[i]->pdgId()));
	}
	// interface to TauSpinner

	Tauolapp::Tauola::initialize();
	string name="MSTW2008nnlo90cl.LHgrid";
	LHAPDF::initPDFSetByName(name);
	double CMSENE = 8000.0; // center of mass system energy.
	                        // used in PDF calculation. For pp collisions only
	bool Ipp = true;  // for pp collisions 
	// Initialize TauSpinner
	//Ipol - polarization of input sample
	//nonSM2 - nonstandard model calculations
	//nonSMN
	int Ipol=0,nonSM2=0,nonSMN=0;
	std::cout << "initialize: " << std::endl;
	TauSpinner::initialize_spinner(Ipp,Ipol,nonSM2,nonSMN,CMSENE);
	double tauSpinnerWeight; 
	std::cout << "getWeight: " << std::endl;
	/* Debug output for testing
	std::cout << selectedHiggs->p4.px() << std::endl;
	std::cout << selectedTau1->p4.px() << std::endl;
	std::cout << selectedTau2->p4.px() << std::endl;
	std::cout << selectedTauDaughters1[1]->p4.px() << std::endl;
	std::cout << selectedTauDaughters2[1]->p4.px() << std::endl;
	*/

	tauSpinnerWeight = calculateWeightFromParticlesH(X, tau1, tau2, tauDaughters1, tauDaughters2);
	std::cout << "tauSpinnerWeight: " << tauSpinnerWeight << std::endl;
	}
};


