
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/TauSpinnerProducer.h"
#include "Artus/KappaAnalysis/interface/KappaProduct.h"

#include "Artus/Utility/interface/DefaultValues.h"



void TauSpinnerProducer::Init(setting_type const& settings)
{
	ProducerBase<HttTypes>::Init(settings);
	
	// interface to TauSpinner
	//Reading the settings from TauSpinnerSettings.json in following order:
	//name of PDF, CMSENE, Ipp, Ipol, nonSM2, nonSMN (see tau_reweight_lib.cxx),
	//boosted/unboosted to Higgs CMF
	stringvector tauSpinnerSettings = settings.GetTauSpinnerSettings();
	Tauolapp::Tauola::initialize();
	string name = tauSpinnerSettings[0];
	LHAPDF::initPDFSetByName(name);
	double CMSENE = atof(tauSpinnerSettings[1].c_str());
	bool Ipp;
	std::istringstream(tauSpinnerSettings[2]) >> std::boolalpha >> Ipp;
	int Ipol, nonSM2, nonSMN;
	std::istringstream(tauSpinnerSettings[3]) >> Ipol;
	std::istringstream(tauSpinnerSettings[4]) >> nonSM2;
	std::istringstream(tauSpinnerSettings[5]) >> nonSMN;
	std::cout << "initialize: " << std::endl;
	TauSpinner::initialize_spinner(Ipp, Ipol, nonSM2, nonSMN, CMSENE);
}


void TauSpinnerProducer::Produce(event_type const& event, product_type& product,
                                 setting_type const& settings) const
{
	std::vector<MotherDaughterBundle> higgs = product.m_genBoson;


	//Conversion to SimpleParticles
	//select the particles to convert from Output of GenTauDecay Producer, which gives the mother boson, two boson daughters,
	//and the granddaughters.
	KGenParticle* selectedHiggs1 = higgs[0].node;
//	KGenParticle* selectedTau1 = higgs[0].Daughters[0].node;
//	KGenParticle* selectedTau2 = higgs[0].Daughters[1].node;

	MotherDaughterBundle selectedTau1 = higgs[0].Daughters[0];
	MotherDaughterBundle selectedTau2 = higgs[0].Daughters[1];

	std::vector<MotherDaughterBundle> selectedTauDaughters1 = higgs[0].Daughters[0].Daughters;
	std::vector<MotherDaughterBundle> selectedTauDaughters2 = higgs[0].Daughters[1].Daughters;
	LOG(DEBUG) << "Higgs PdgId: " << selectedHiggs1->pdgId();

	//MassRoundOff check: calculation of the difference of the tau mass and the summarized mass of the tau daughters.
	RMDataLV TauDaughters1Sum = selectedTauDaughters1[0].node->p4;
	for (unsigned int i = 1; i < selectedTauDaughters1.size(); i++)
	{
		TauDaughters1Sum += selectedTauDaughters1[i].node->p4;
	}
	RMDataLV TauDaughters2Sum = selectedTauDaughters2[0].node->p4;
	for (unsigned int i = 1; i < selectedTauDaughters2.size(); i++)
	{
		TauDaughters2Sum += selectedTauDaughters2[i].node->p4;
	}
	product.m_genMassRoundOff1 = abs(selectedTau1.node->p4.mass() - TauDaughters1Sum.mass());
	product.m_genMassRoundOff2 = abs(selectedTau2.node->p4.mass() - TauDaughters2Sum.mass());


	//Boosting following vectors to the center of mass system of the Higgs, if nessesary: Higgs, Tau1, Tau2 and TauDaughters
	//Information about boosting is read from TauSpinnerSettings.json, seventh entry.
	RMDataLV vec = selectedHiggs1->p4;
	RMDataLV::BetaVector boostvec = vec.BoostToCM();
	ROOT::Math::Boost boostMat(boostvec);
	bool boosted = (settings.GetTauSpinnerSettings()[6] == "boosted");
	if (boosted)
	{
		selectedHiggs1->p4 = boostMat * (selectedHiggs1->p4);
		selectedTau1.node->p4 = boostMat * (selectedTau1.node->p4);
		selectedTau2.node->p4 = boostMat * (selectedTau2.node->p4);
		for (unsigned int i = 0; i < selectedTauDaughters1.size(); ++i)
		{
			selectedTauDaughters1[i].node->p4 = boostMat * (selectedTauDaughters1[i].node->p4);
		}
		for (unsigned int i = 0; i < selectedTauDaughters2.size(); ++i)
		{
			selectedTauDaughters2[i].node->p4 = boostMat * (selectedTauDaughters2[i].node->p4);
		}
	}
	if (abs(selectedTau1.node->pdgId()) == 15) //TauSpinner considers only Taus and Tau-Neutrinos as daughters of a Boson (Higgs, W etc.)
	{
		LOG(DEBUG) << "		Tau1 PdgId: " << selectedTau1.node->pdgId();
		LOG(DEBUG) << "		Tau2 PdgId: " << selectedTau2.node->pdgId() << std::endl;

		TauSpinner::SimpleParticle X = getSimpleParticle(selectedHiggs1);
		TauSpinner::SimpleParticle tau1 = getSimpleParticle(selectedTau1.node);
		TauSpinner::SimpleParticle tau2 = getSimpleParticle(selectedTau2.node);

		//choosing considered tau decay products for the TauSpinnerWeight calculaton
		//through the entry ChosenTauDaughters in the TauSpinnerSettings.json
		stringvector chosentaudaughters = settings.GetChosenTauDaughters();
		//bool choose = (chosentaudaughters[0] == "choose");
		std::vector<int> chosentd;
		for (unsigned int i = 1; i < chosentaudaughters.size(); i++)
		{
			chosentd.push_back(0);
			std::istringstream(chosentaudaughters[i]) >> chosentd[i - 1];
		}
		bool withoutchoise = true;
		int choosecomplete1 = 0;
		int choosecomplete2 = 0;

		// fill final states
		// auslesen aus tree oder selbst bestimmen

		// von selectedTauDaughters1, selectedTauDaughters2 final states mit pi0

		std::vector<TauSpinner::SimpleParticle> tauFinalStates1;
		getFinalStates(selectedTau1, &tauFinalStates1);
		std::vector<TauSpinner::SimpleParticle> tauFinalStates2;
		getFinalStates(selectedTau2, &tauFinalStates2);


//		std::vector<TauSpinner::SimpleParticle> tauDaughters2 = getFinalStates(selectedTauDaughters2);
/*
		for (unsigned int i = 0; i < selectedTauDaughters1.size(); ++i)
		{
			if (choose)
			{
				withoutchoise = false;
				for (unsigned int j = 0; j < chosentd.size(); j++)
				{
					if (chosentd[j] == abs(selectedTauDaughters1[i].node->pdgId()))   choosecomplete1++;
				}
			}
			tauDaughters1.push_back(getSimpleParticle(selectedTauDaughters1[i].node));
		}

		std::vector<TauSpinner::SimpleParticle> tauDaughters2;

		for (unsigned int i = 0; i < selectedTauDaughters2.size(); ++i)
		{

			if (choose)
			{
				withoutchoise = false;
				for (unsigned int j = 0; j < chosentd.size(); j++)
				{
					if (chosentd[j] == abs(selectedTauDaughters2[i].node->pdgId()))   choosecomplete2++;
				}
			}
			tauDaughters2.push_back(getSimpleParticle(selectedTauDaughters2[i].node));
		}
*/
		// Debug output for testing
		LOG(DEBUG) << selectedHiggs1->p4.px() << std::endl;
		LOG(DEBUG) << selectedTau1.node->p4.px() << std::endl;
		LOG(DEBUG) << selectedTau2.node->p4.px() << std::endl;
		LOG(DEBUG) << selectedTauDaughters1[1].node->p4.px() << std::endl;
		LOG(DEBUG) << selectedTauDaughters2[1].node->p4.px() << std::endl;

		LOG(DEBUG) << choosecomplete1 << "               " << choosecomplete2 << std::endl;
		if (((choosecomplete1 > 0) && (choosecomplete2) > 0) || withoutchoise)
		{
			//Decision for a certain weight calculation depending on BosonPdgId
			stringvector bosonPdgIdVector = settings.GetBosonPdgId();
			int bosonPdgId;
			std::istringstream(bosonPdgIdVector[0]) >> bosonPdgId;

			double weight;
			if (abs(bosonPdgId) == PDG_W) weight = calculateWeightFromParticlesWorHpn(X, tau1, tau2, tauFinalStates1);
			else if (abs(bosonPdgId) == PDG_H)  weight = calculateWeightFromParticlesH(X, tau1, tau2, tauFinalStates1, tauFinalStates2);
			if(weight == weight) product.m_weights.insert(std::pair<std::string, double>("tauspinnerweight", weight));
			else
			{
				// 'Nan' Debug output
				LOG(DEBUG) << "\nHiggsPx=" << product.m_genBoson[0].node->p4.Px() << "|"
						   << "HiggsPy=" << product.m_genBoson[0].node->p4.Py() << "|"
						   << "HiggsPz=" << product.m_genBoson[0].node->p4.Pz() << "|"
						   << "HiggsE=" << product.m_genBoson[0].node->p4.e() << "|"
						   << "HiggsPdgId=" << product.m_genBoson[0].node->pdgId() << "|"

						   << "1TauPx=" << product.m_genBoson[0].Daughters[0].node->p4.Px() << "|"
						   << "1TauPy=" << product.m_genBoson[0].Daughters[0].node->p4.Py() << "|"
						   << "1TauPz=" << product.m_genBoson[0].Daughters[0].node->p4.Pz() << "|"
						   << "1TauE=" << product.m_genBoson[0].Daughters[0].node->p4.e() << "|"
						   << "1TauPdgId=" << product.m_genBoson[0].Daughters[0].node->pdgId() << "|"

						   << "2TauPx=" << product.m_genBoson[0].Daughters[1].node->p4.Px() << "|"
						   << "2TauPy=" << product.m_genBoson[0].Daughters[1].node->p4.Py() << "|"
						   << "2TauPz=" << product.m_genBoson[0].Daughters[1].node->p4.Pz() << "|"
						   << "2TauE=" << product.m_genBoson[0].Daughters[1].node->p4.e() << "|"
						   << "2TauPdgId=" << product.m_genBoson[0].Daughters[1].node->pdgId() << "|";

				for (unsigned int i = 0; i < product.m_genBoson[0].Daughters[0].Daughters.size(); i++)
				{
					std::ostringstream index;
					index << i + 1;
					//std::string Index(index.str());
					std::string name = "1Tau" + index.str() + "Daughter";
					LOG(DEBUG) << name << "Px=" << product.m_genBoson[0].Daughters[0].Daughters[i].node->p4.Px() << "|"
							   << name << "Py=" << product.m_genBoson[0].Daughters[0].Daughters[i].node->p4.Py() << "|"
							   << name << "Pz=" << product.m_genBoson[0].Daughters[0].Daughters[i].node->p4.Pz() << "|"
							   << name << "E="  << product.m_genBoson[0].Daughters[0].Daughters[i].node->p4.e() << "|"
							   << name << "PdgId=" << product.m_genBoson[0].Daughters[0].Daughters[i].node->pdgId() << "|";
				}

				for (unsigned int i = 0; i < product.m_genBoson[0].Daughters[1].Daughters.size(); i++)
				{
					std::ostringstream index;
					index << i + 1;
					//std::string Index(index.str());
					std::string name = "2Tau" + index.str() + "Daughter";
					LOG(DEBUG) << name << "Px=" << product.m_genBoson[0].Daughters[1].Daughters[i].node->p4.Px() << "|"
							   << name << "Py=" << product.m_genBoson[0].Daughters[1].Daughters[i].node->p4.Py() << "|"
							   << name << "Pz=" << product.m_genBoson[0].Daughters[1].Daughters[i].node->p4.Pz() << "|"
							   << name << "E="  << product.m_genBoson[0].Daughters[1].Daughters[i].node->p4.e() << "|"
							   << name << "PdgId=" << product.m_genBoson[0].Daughters[1].Daughters[i].node->pdgId() << "|";
				product.m_weights.insert(std::pair<std::string, double>("tauspinnerweight", -777.0));			
				} // NaN debug output end
			}
		}
		else product.m_weights.insert(std::pair<std::string, double>("tauspinnerweight", DefaultValues::UndefinedDouble));
	}// "if 1BosonDaughter is Tau"-end.
	else product.m_weights.insert(std::pair<std::string, double>("tauspinnerweight", DefaultValues::UndefinedDouble));
}


TauSpinner::SimpleParticle TauSpinnerProducer::getSimpleParticle(KGenParticle*& in) const
{
	return TauSpinner::SimpleParticle(in->p4.px(), in->p4.py(), in->p4.pz(), in->p4.e(), in->pdgId());
}


// recursive function to create a vector of final states particles in the way TauSpinner expects it
std::vector<TauSpinner::SimpleParticle> *TauSpinnerProducer::getFinalStates(MotherDaughterBundle& mother,
                                        std::vector<TauSpinner::SimpleParticle> *resultVector) const
{
	for (unsigned int i = 0; i < mother.Daughters.size(); ++i)
	{
		if( abs(mother.Daughters[i].node->pdgId()) == PDG_PIZERO || mother.Daughters[i].finalState )
		{
			resultVector->push_back(getSimpleParticle(mother.Daughters[i].node));
			return resultVector;
		}
		else
		{
			getFinalStates(mother.Daughters[i], resultVector);
		}
	}
	return resultVector;
}

