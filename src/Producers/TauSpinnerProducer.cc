
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/TauSpinnerProducer.h"
#include "Artus/KappaAnalysis/interface/KappaProduct.h"


void TauSpinnerProducer::InitGlobal(global_setting_type const& globalSettings)
{
	// interface to TauSpinner
	//Reading the settings from TauSpinnerSettings.json in following order:
	//name of PDF, CMSENE, Ipp, Ipol, nonSM2, nonSMN (see tau_reweight_lib.cxx),
	//boosted/unboosted to Higgs CMF
	stringvector tauSpinnerSettings = globalSettings.GetTauSpinnerSettings();
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




void TauSpinnerProducer::ProduceGlobal(HttEvent const& event, HttProduct& product,
									   HttGlobalSettings const& globalSettings) const
{
	std::vector<KappaProduct::MotherDaughterBundle> higgs = product.m_genBoson;


	//Conversion to SimpleParticles
	//select the particles to convert from Output of GenTauDecay Producer, which gives the mother boson, two boson daughters,
	//and the granddaughters.
	KGenParticle* selectedHiggs1 = higgs[0].node;
	KGenParticle* selectedTau1 = higgs[0].Daughters[0].node;
	KGenParticle* selectedTau2 = higgs[0].Daughters[1].node;
	std::vector<KappaProduct::MotherDaughterBundle> selectedTauDaughters1 = higgs[0].Daughters[0].Daughters;
	std::vector<KappaProduct::MotherDaughterBundle> selectedTauDaughters2 = higgs[0].Daughters[1].Daughters;
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
	product.m_genMassRoundOff1 = abs(selectedTau1->p4.mass() - TauDaughters1Sum.mass());
	product.m_genMassRoundOff2 = abs(selectedTau2->p4.mass() - TauDaughters2Sum.mass());


	//Boosting following vectors to the center of mass system of the Higgs, if nessesary: Higgs, Tau1, Tau2 and TauDaughters
	//Information about boosting is read from TauSpinnerSettings.json, seventh entry.
	RMDataLV vec = selectedHiggs1->p4;
	RMDataLV::BetaVector boostvec = vec.BoostToCM();
	ROOT::Math::Boost boostMat(boostvec);
	bool boosted = (globalSettings.GetTauSpinnerSettings()[6] == "boosted");
	if (boosted)
	{
		selectedHiggs1->p4 = boostMat * (selectedHiggs1->p4);
		selectedTau1->p4 = boostMat * (selectedTau1->p4);
		selectedTau2->p4 = boostMat * (selectedTau2->p4);
		for (unsigned int i = 0; i < selectedTauDaughters1.size(); ++i)
		{
			selectedTauDaughters1[i].node->p4 = boostMat * (selectedTauDaughters1[i].node->p4);
		}
		for (unsigned int i = 0; i < selectedTauDaughters2.size(); ++i)
		{
			selectedTauDaughters2[i].node->p4 = boostMat * (selectedTauDaughters2[i].node->p4);
		}
	}
	if (abs(selectedTau1->pdgId()) == 15) //TauSpinner considers only Taus and Tau-Neutrinos as daughters of a Boson (Higgs, W etc.)
	{
		LOG(DEBUG) << "		Tau1 PdgId: " << selectedTau1->pdgId();
		LOG(DEBUG) << "		Tau2 PdgId: " << selectedTau2->pdgId() << std::endl;

		TauSpinner::SimpleParticle X(selectedHiggs1->p4.px(), selectedHiggs1->p4.py(), selectedHiggs1->p4.pz(), selectedHiggs1->p4.e(), selectedHiggs1->pdgId());
		TauSpinner::SimpleParticle tau1(selectedTau1->p4.px(), selectedTau1->p4.py(), selectedTau1->p4.pz(), selectedTau1->p4.e(), selectedTau1->pdgId());
		TauSpinner::SimpleParticle tau2(selectedTau2->p4.px(), selectedTau2->p4.py(), selectedTau2->p4.pz(), selectedTau2->p4.e(), selectedTau2->pdgId());

		//choosing considered tau decay products for the TauSpinnerWeight calculaton
		//through the entry ChosenTauDaughters in the TauSpinnerSettings.json
		stringvector chosentaudaughters = globalSettings.GetChosenTauDaughters();
		bool choose = (chosentaudaughters[0] == "choose");
		std::vector<int> chosentd;
		for (unsigned int i = 1; i < chosentaudaughters.size(); i++)
		{
			chosentd.push_back(0);
			std::istringstream(chosentaudaughters[i]) >> chosentd[i - 1];
		}
		bool withoutchoise = true;
		int choosecomplete1 = 0;
		int choosecomplete2 = 0;

		std::vector<TauSpinner::SimpleParticle> tauDaughters1;

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
			tauDaughters1.push_back(TauSpinner::SimpleParticle(selectedTauDaughters1[i].node->p4.px(), selectedTauDaughters1[i].node->p4.py(), selectedTauDaughters1[i].node->p4.pz(), selectedTauDaughters1[i].node->p4.e(), selectedTauDaughters1[i].node->pdgId()));
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
			tauDaughters2.push_back(TauSpinner::SimpleParticle(selectedTauDaughters2[i].node->p4.px(), selectedTauDaughters2[i].node->p4.py(), selectedTauDaughters2[i].node->p4.pz(), selectedTauDaughters2[i].node->p4.e(), selectedTauDaughters2[i].node->pdgId()));
		}
		// Debug output for testing
		LOG(DEBUG) << selectedHiggs1->p4.px() << std::endl;
		LOG(DEBUG) << selectedTau1->p4.px() << std::endl;
		LOG(DEBUG) << selectedTau2->p4.px() << std::endl;
		LOG(DEBUG) << selectedTauDaughters1[1].node->p4.px() << std::endl;
		LOG(DEBUG) << selectedTauDaughters2[1].node->p4.px() << std::endl;

		LOG(DEBUG) << choosecomplete1 << "               " << choosecomplete2 << std::endl;
		if (((choosecomplete1 > 0) && (choosecomplete2) > 0) || withoutchoise)
		{
			//Decision for a certain weight calculation depending on BosonPdgId
			stringvector bosonPdgIdVector = globalSettings.GetBosonPdgId();
			int bosonPdgId;
			std::istringstream(bosonPdgIdVector[0]) >> bosonPdgId;

			double weight;
			if (abs(bosonPdgId) == 24) weight = calculateWeightFromParticlesWorHpn(X, tau1, tau2, tauDaughters1);
			else if (abs(bosonPdgId) == 25)  weight = calculateWeightFromParticlesH(X, tau1, tau2, tauDaughters1, tauDaughters2);
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
		else product.m_weights.insert(std::pair<std::string, double>("tauspinnerweight", UNDEFINED_VALUE));
	}// "if 1BosonDaughter is Tau"-end.
	else product.m_weights.insert(std::pair<std::string, double>("tauspinnerweight", UNDEFINED_VALUE));
}
