
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/TauSpinnerProducer.h"
#include "Artus/KappaAnalysis/interface/KappaProduct.h"

#include "Artus/Utility/interface/DefaultValues.h"
#include "Artus/Consumer/interface/LambdaNtupleConsumer.h"
#include "Artus/KappaAnalysis/interface/KappaTypes.h"

#define NO_BOSON_FOUND -555
#define NO_HIGGS_FOUND -666
#define WEIGHT_NAN -777

void TauSpinnerProducer::Init(setting_type const& settings)
{
	ProducerBase<HttTypes>::Init(settings);
	// interface to TauSpinner
	// see tau_reweight_lib.cxx for explanation of paramesters
	Tauolapp::Tauola::initialize();
	string name = settings.GetTauSpinnerSettingsPDF();
	LHAPDF::initPDFSetByName(name);
	double CmsEnergy = settings.GetTauSpinnerSettingsCmsEnergy();
	bool ipp = settings.GetTauSpinnerSettingsIpp();
	int ipol = settings.GetTauSpinnerSettingsIpol();
	int nonSM2 = settings.GetTauSpinnerSettingsNonSM2();
	int nonSMN = settings.GetTauSpinnerSettingsNonSMN();
	TauSpinner::initialize_spinner(ipp, ipol, nonSM2, nonSMN, CmsEnergy);
	TauSpinner::setHiggsParametersTR(-1, 1, 0, 0);
	
	// add possible quantities for the lambda ntuples consumers
	LambdaNtupleConsumer<KappaTypes>::Quantities["tauSpinnerWeight"] = [](KappaEvent const& event, KappaProduct const& product) {
		return (static_cast<HttProduct const&>(product)).m_tauSpinnerWeight;
	};
}


void TauSpinnerProducer::Produce(event_type const& event, product_type& product,
								 setting_type const& settings) const
{
	std::vector<MotherDaughterBundle> higgs = product.m_genBoson;
	if (higgs.size() == 0)
	{
		product.m_tauSpinnerWeight = NO_HIGGS_FOUND;
		return;
	}

	KGenParticle* selectedHiggs1 = higgs[0].node;
	MotherDaughterBundle selectedTau1 = higgs[0].Daughters[0];
	MotherDaughterBundle selectedTau2 = higgs[0].Daughters[1];

	if ((abs(selectedTau1.node->pdgId()) != DefaultValues::pdgIdTau)
		|| (abs(selectedTau2.node->pdgId()) != DefaultValues::pdgIdTau)) //TauSpinner considers only Taus and Tau-Neutrinos as daughters of a Boson (Higgs, W etc.)
	{
		LOG_N_TIMES(20, WARNING) << "TauSpinnerProducer could not find two taus as daughters of Boson" << std::endl;
		product.m_tauSpinnerWeight = DefaultValues::UndefinedDouble;
		return;
	}

	TauSpinner::SimpleParticle X = getSimpleParticle(selectedHiggs1);
	TauSpinner::SimpleParticle tau1 = getSimpleParticle(selectedTau1.node);
	TauSpinner::SimpleParticle tau2 = getSimpleParticle(selectedTau2.node);
	std::vector<TauSpinner::SimpleParticle> tauFinalStates1;
	GetFinalStates(selectedTau1, &tauFinalStates1);
	std::vector<TauSpinner::SimpleParticle> tauFinalStates2;
	GetFinalStates(selectedTau2, &tauFinalStates2);

	LOG_N_TIMES(20, DEBUG) << "The event contains the following particles: " << std::endl;
	LOG_N_TIMES(20, DEBUG) << "Higgs " << std::to_string(X) << std::endl;
	LOG_N_TIMES(20, DEBUG) << std::string("Tau1") << std::to_string(tau1);
	LOG_N_TIMES(20, DEBUG) << std::string("Tau2") << std::to_string(tau2);
	LOG_N_TIMES(20, DEBUG) << std::string("Tau1FinalState") << std::to_string(tauFinalStates1);
	LOG_N_TIMES(20, DEBUG) << std::string("Tau2FinalState") << std::to_string(tauFinalStates2);


	if ((tauFinalStates1.size() == 0) || (tauFinalStates2.size() == 0))
	{
		LOG_N_TIMES(20, WARNING) << "TauSpinnerProducer could not find enogh genParticles for the TauSpinner Algorithm" << std::endl;
		product.m_tauSpinnerWeight = DefaultValues::UndefinedDouble;
		return;
	}

	//Decision for a certain weight calculation depending on BosonPdgId
	double tauSpinnerWeight;
	if (abs(settings.GetBosonPdgId()) == DefaultValues::pdgIdW)
		tauSpinnerWeight = calculateWeightFromParticlesWorHpn(X, tau1, tau2, tauFinalStates1);
	else if (abs(settings.GetBosonPdgId()) == DefaultValues::pdgIdH)
		tauSpinnerWeight = calculateWeightFromParticlesH(X, tau1, tau2, tauFinalStates1, tauFinalStates2);
	else
		tauSpinnerWeight = NO_BOSON_FOUND;

	if (tauSpinnerWeight == tauSpinnerWeight)
		product.m_tauSpinnerWeight = tauSpinnerWeight;
	else
	{
		LOG_N_TIMES(20, WARNING) << "Found a 'NaN' TauSpinner weight " << std::endl;
		product.m_tauSpinnerWeight = WEIGHT_NAN;
	}

}

TauSpinner::SimpleParticle TauSpinnerProducer::getSimpleParticle(KGenParticle*& in) const
{
	return TauSpinner::SimpleParticle(in->p4.px(), in->p4.py(), in->p4.pz(), in->p4.e(), in->pdgId());
}

// recursive function to create a vector of final states particles in the way TauSpinner expects it
std::vector<TauSpinner::SimpleParticle>* TauSpinnerProducer::GetFinalStates(MotherDaughterBundle& mother,
		std::vector<TauSpinner::SimpleParticle>* resultVector) const
{
	for (unsigned int i = 0; i < mother.Daughters.size(); ++i)
	{
		// this if-condition has to define what particles go into TauSpinner
		int pdgId = abs(mother.Daughters[i].node->pdgId());
		if (pdgId == DefaultValues::pdgIdGamma ||
			pdgId == DefaultValues::pdgIdPiZero ||
			pdgId == DefaultValues::pdgIdPiPlus ||
			pdgId == DefaultValues::pdgIdKPlus ||
			pdgId == DefaultValues::pdgIdKLong ||
			pdgId == DefaultValues::pdgIdKShort ||
			pdgId == DefaultValues::pdgIdElectron ||
			pdgId == DefaultValues::pdgIdNuE ||
			pdgId == DefaultValues::pdgIdMuon ||
			pdgId == DefaultValues::pdgIdNuMu ||
			pdgId == DefaultValues::pdgIdNuTau)
		{
			resultVector->push_back(getSimpleParticle(mother.Daughters[i].node));
		}
		else
		{
			if (mother.Daughters[i].finalState)
			{
				LOG(FATAL) << "Could not find a proper final state that can be handled by TauSpinner" << std::endl;
			}
			LOG_N_TIMES(20, DEBUG) << "Recursion, pdgId " << pdgId << " is not considered being a final states" << std::endl;
			GetFinalStates(mother.Daughters[i], resultVector);
		}
	}
	return resultVector;
}


std::string std::to_string(TauSpinner::SimpleParticle& particle)
{
	return std::string("PdgId=" + std::to_string(particle.pdgid()) + "\t|"
			             "Px=" + std::to_string(particle.px()) + "\t|" +
			             "Py=" + std::to_string(particle.py()) + "\t|" +
			             "Pz=" + std::to_string(particle.pz()) + "\t|" +
			             "E="  + std::to_string(particle.e()) + "\t|" +
			             "Mass=" + std::to_string(pow(particle.e(), 2) - pow(particle.px(), 2) - pow(particle.py(), 2) - pow(particle.pz(), 2)) + "\t|");
}

std::string std::to_string(std::vector<TauSpinner::SimpleParticle>& particleVector)
{
	std::string result = "";
	for(size_t i = 0; i < particleVector.size(); i++)
	{
		result += ("\n\t" + std::to_string(i) + ") " + std::to_string(particleVector[i]));
	}
	return result;
}
