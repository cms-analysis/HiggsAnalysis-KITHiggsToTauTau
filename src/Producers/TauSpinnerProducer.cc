
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/TauSpinnerProducer.h"



void TauSpinnerProducer::InitGlobal(global_setting_type const& globalSettings)
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




void TauSpinnerProducer::ProduceGlobal(HttEvent const& event, HttProduct& product,
	                           HttGlobalSettings const& globalSettings) const
{
	std::vector<KGenParticle*> higgs = product.m_genHiggs;
	std::vector<std::vector<KGenParticle*>> taus = product.m_genHiggsDaughters;
	std::vector<std::vector<std::vector<KGenParticle*>>> tauDaughters = product.m_genHiggsGranddaughters;


	//Conversion to SimpleParticles
	//select the particles to convert from Output of GenTauDecay Producer, which gives the mother boson, two boson daughters,
        //and the granddaughters.
	KGenParticle* selectedHiggs1 = higgs[0];
	KGenParticle* selectedTau1 = taus[0][0];
	KGenParticle* selectedTau2 = taus[0][1];
	std::vector<KGenParticle*> selectedTauDaughters1 = tauDaughters[0][0];
	std::vector<KGenParticle*> selectedTauDaughters2 = tauDaughters[0][1];
	//std::cout << "Higgs PdgId: " << selectedHiggs->pdgId();
	
	//MassRoudOff check
	RMDataLV TauDaughters1Sum = selectedTauDaughters1[0]->p4;
	for(unsigned int i=1; i<selectedTauDaughters1.size();i++)
	{
		TauDaughters1Sum+=selectedTauDaughters1[i]->p4;
	}
	RMDataLV TauDaughters2Sum = selectedTauDaughters2[0]->p4;
	for(unsigned int i=1; i<selectedTauDaughters2.size();i++)
	{
		TauDaughters2Sum+=selectedTauDaughters2[i]->p4;
	}
	product.m_MassRoundOff1 = abs(selectedTau1->p4.mass()- TauDaughters1Sum.mass());
	product.m_MassRoundOff2 = abs(selectedTau2->p4.mass()- TauDaughters2Sum.mass());


	//Boosting following vectors to the center of mass system of the Higgs, if nessesary: Higgs, Tau1, Tau2 and TauDaughters
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
		for(unsigned int i = 0; i < selectedTauDaughters1.size(); ++i)
		{
			selectedTauDaughters1[i]->p4 = boostMat*(selectedTauDaughters1[i]->p4);	
		}
		for(unsigned int i = 0; i < selectedTauDaughters2.size(); ++i)
		{
			selectedTauDaughters2[i]->p4 = boostMat*(selectedTauDaughters2[i]->p4);	
		}
	}
	if (abs(taus[0][0]->pdgId())==15) //TauSpinner considers only Taus and Tau-Neutrinos as daughters of a Boson (Higgs, W etc.)
	{		
		//std::cout << "		Tau1 PdgId: " << selectedTau1->pdgId();
		//std::cout << "		Tau2 PdgId: " << selectedTau2->pdgId() << std::endl;
		
		TauSpinner::SimpleParticle X(selectedHiggs1->p4.px(), selectedHiggs1->p4.py(), selectedHiggs1->p4.pz(), selectedHiggs1->p4.e(), selectedHiggs1->pdgId());
		TauSpinner::SimpleParticle tau1(selectedTau1->p4.px(), selectedTau1->p4.py(), selectedTau1->p4.pz(), selectedTau1->p4.e(), selectedTau1->pdgId());
		TauSpinner::SimpleParticle tau2(selectedTau2->p4.px(), selectedTau2->p4.py(), selectedTau2->p4.pz(), selectedTau2->p4.e(), selectedTau2->pdgId());
		
		stringvector chosentaudaughters = globalSettings.GetChosenTauDaughters();
		bool choose = (chosentaudaughters[0]=="choose");
		std::vector<int> chosentd;
		for (unsigned int i=1; i< chosentaudaughters.size(); i++)
		{
			chosentd.push_back(0);
			std::istringstream(chosentaudaughters[i]) >> chosentd[i-1];
		}
		bool withoutchoise = true;
		int choosecomplete1 = 0;
		int choosecomplete2 = 0;

		std::vector<TauSpinner::SimpleParticle> tauDaughters1;

		for(unsigned int i = 0; i < selectedTauDaughters1.size(); ++i)
		{	
			if(choose)
			{
				withoutchoise = false;	
				for(unsigned int j=0;j<chosentd.size();j++)
				{
					if(chosentd[j]==abs(selectedTauDaughters1[i]->pdgId()))   choosecomplete1++;					
				}										
			}
			tauDaughters1.push_back(TauSpinner::SimpleParticle(selectedTauDaughters1[i]->p4.px(), selectedTauDaughters1[i]->p4.py(), selectedTauDaughters1[i]->p4.pz(), selectedTauDaughters1[i]->p4.e(), selectedTauDaughters1[i]->pdgId()));		
		}

		std::vector<TauSpinner::SimpleParticle> tauDaughters2;

		for(unsigned int i = 0; i < selectedTauDaughters2.size(); ++i)
		{

			if(choose)
			{
				withoutchoise=false;	
				for(unsigned int j=0;j<chosentd.size();j++)
				{
					if(chosentd[j]==abs(selectedTauDaughters2[i]->pdgId()))   choosecomplete2++;					
				}										
			}
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
		//std::cout << choosecomplete1 << "               " << choosecomplete2 << std::endl;
		if(((choosecomplete1>0) && (choosecomplete2)>0) || withoutchoise)
		{
		//Decision for a certain weight calculation depending on BosonPdgId
		stringvector bosonPdgIdVector = globalSettings.GetBosonPdgId();
		int bosonPdgId;
		std::istringstream(bosonPdgIdVector[0]) >> bosonPdgId;
		if(abs(bosonPdgId)==24) product.m_tauSpinnerWeight = calculateWeightFromParticlesWorHpn(X, tau1, tau2, tauDaughters1);
		else if (abs(bosonPdgId)==25) product.m_tauSpinnerWeight = calculateWeightFromParticlesH(X, tau1, tau2, tauDaughters1, tauDaughters2);
		//std::cout << "tauSpinnerWeight: " << (product.m_tauSpinnerWeight==1.00) << std::endl;
		}
		else product.m_tauSpinnerWeight = UNDEFINED_VALUE;
	}// "if 1BosonDaughter is Tau"-end.
	else product.m_tauSpinnerWeight = UNDEFINED_VALUE;
	product.m_weights.insert(std::pair<std::string, double>("tauspinnerweight", product.m_tauSpinnerWeight));
}
