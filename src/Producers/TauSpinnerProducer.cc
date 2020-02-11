
#include <algorithm>
#include <cstdlib>
#include <math.h>

#include <boost/format.hpp>

#include "Artus/Utility/interface/SafeMap.h"
#include "Artus/Utility/interface/Utility.h"
#include "Artus/Consumer/interface/LambdaNtupleConsumer.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/TauSpinnerProducer.h"

#define NO_BOSON_FOUND -555
#define NO_HIGGS_FOUND -666
#define WEIGHT_NAN -777

TauSpinnerProducer::~TauSpinnerProducer()
{
	if (numberOfNanWeights > 0)
	{
		LOG(WARNING) << "Found " << numberOfNanWeights << " events with a 'NaN' TauSpinner weight in the pipeline \"" << pipelineName << "\"! "
		             << "The weight is set to zero in order to avoid considering such events in any plots.";
	}
}

void TauSpinnerProducer::Init(setting_type const& settings, metadata_type& metadata)
{
	ProducerBase<HttTypes>::Init(settings, metadata);
	
	pipelineName = settings.GetName();
	
	// interface to TauSpinner
	// see the print out of this function or tau_reweight_lib.cxx for explanation of paramesters
	// $CMSSW_RELEASE_BASE/../../../external/tauolapp/1.1.5-cms2/include/TauSpinner/tau_reweight_lib.h
	// http://tauolapp.web.cern.ch/tauolapp/tau__reweight__lib_8cxx_source.html
	// http://tauolapp.web.cern.ch/tauolapp/namespaceTauSpinner.html
	// https://arxiv.org/pdf/1402.2068v1.pdf
	Tauolapp::Tauola::initialize();
	Tauolapp::Tauola::setRandomGenerator(&TauSpinnerProducer::CustomRandomGenerator);
	
	LHAPDF::initPDFSetByName(settings.GetTauSpinnerSettingsPDF());
	
	TauSpinner::initialize_spinner(settings.GetTauSpinnerSettingsIpp(),
	                               settings.GetTauSpinnerSettingsIpol(),
	                               settings.GetTauSpinnerSettingsNonSM2(),
	                               settings.GetTauSpinnerSettingsNonSMN(),
	                               settings.GetTauSpinnerSettingsCmsEnergy());
	
	LambdaNtupleConsumer<HttTypes>::AddBoolQuantity(metadata, "tauSpinnerValidOutputs", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_tauSpinnerValidOutputs;
	});
	
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "tauSpinnerPolarisation", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_tauSpinnerPolarisation;
	});
	
	LambdaNtupleConsumer<HttTypes>::AddDoubleQuantity(metadata, "tauSpinnerPdgIdTau_1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_tauSpinnerPdgIdTau_1;
	});
	LambdaNtupleConsumer<HttTypes>::AddDoubleQuantity(metadata, "tauSpinnerPdgIdTau_2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_tauSpinnerPdgIdTau_2;
	});
	LambdaNtupleConsumer<HttTypes>::AddDoubleQuantity(metadata, "tauSpinnerETau_1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_tauSpinnerETau_1;
	});
	LambdaNtupleConsumer<HttTypes>::AddDoubleQuantity(metadata, "tauSpinnerETau_2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_tauSpinnerETau_2;
	});
	LambdaNtupleConsumer<HttTypes>::AddDoubleQuantity(metadata, "tauSpinnerEPi_1", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_tauSpinnerEPi_1;
	});
	LambdaNtupleConsumer<HttTypes>::AddDoubleQuantity(metadata, "tauSpinnerEPi_2", [](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
	{
		return product.m_tauSpinnerEPi_2;
	});
	
	m_validPdgIdsAndStatusCodes = Utility::ParseMapTypes<int, int>(Utility::ParseVectorToMap(settings.GetTauSpinnerValidPdgIdsAndStatusCodes()), m_validPdgIdsAndStatusCodesByString);
	
	m_useIC = settings.GetTauSpinnerUseIC();

	for (std::vector<float>::const_iterator mixingAngleOverPiHalfIt = settings.GetTauSpinnerMixingAnglesOverPiHalf().begin();
	     mixingAngleOverPiHalfIt != settings.GetTauSpinnerMixingAnglesOverPiHalf().end();
	     ++mixingAngleOverPiHalfIt)
	{
		float mixingAngleOverPiHalf = *mixingAngleOverPiHalfIt;
		std::string mixingAngleOverPiHalfLabel = GetLabelForWeightsMap(mixingAngleOverPiHalf);
		LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, mixingAngleOverPiHalfLabel, [mixingAngleOverPiHalfLabel](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
		{
			return SafeMap::GetWithDefault(product.m_optionalWeights, mixingAngleOverPiHalfLabel, 0.0);
		});
	}
	
	if (settings.GetTauSpinnerMixingAnglesOverPiHalfSample() >= 0.0)
	{
		float mixingAngleOverPiHalfSample = settings.GetTauSpinnerMixingAnglesOverPiHalfSample();
	
		// if mixing angle for curent sample is defined, it has to be in the list TauSpinnerMixingAnglesOverPiHalf
		assert(Utility::Contains(settings.GetTauSpinnerMixingAnglesOverPiHalf(), mixingAngleOverPiHalfSample));
		
		std::string mixingAngleOverPiHalfSampleLabel = GetLabelForWeightsMap(mixingAngleOverPiHalfSample);
		LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "tauSpinnerWeightSample", [mixingAngleOverPiHalfSampleLabel](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
		{
			return SafeMap::GetWithDefault(product.m_optionalWeights, mixingAngleOverPiHalfSampleLabel, 0.0);
		});
		LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(metadata, "tauSpinnerWeightInvSample", [mixingAngleOverPiHalfSampleLabel](event_type const& event, product_type const& product, setting_type const& settings, metadata_type const& metadata)
		{
			double weight = SafeMap::GetWithDefault(product.m_optionalWeights, mixingAngleOverPiHalfSampleLabel, 0.0);
			//return std::min(((weight > 0.0) ? (1.0 / weight) : 0.0), 10.0);   // no physics reason for this
			return ((weight > 0.0) ? (1.0 / weight) : 0.0);
		});
	}
}


void TauSpinnerProducer::Produce(event_type const& event, product_type& product,
								 setting_type const& settings, metadata_type const& metadata) const
{
	assert(event.m_eventInfo);
	assert(! settings.GetBosonPdgIds().empty());
	
	// A generator level boson and its decay products must exist
	// The boson is searched for by a GenBosonProducer
	// and the decay tree is built by the GenTauDecayProducer
	product.m_tauSpinnerValidOutputs = false;
	if (product.m_genBosonTree.m_daughters.size() > 1)
	{
		GenParticleDecayTree* selectedTau1 = GetTau(&(product.m_genBosonTree.m_daughters[0]));
		GenParticleDecayTree* selectedTau2 = GetTau(&(product.m_genBosonTree.m_daughters[1]));
	
		//TauSpinner considers only Taus and Tau-Neutrinos as daughters of a Boson (Higgs, W etc.)
		// otherwise the weights are set to 1
		if (selectedTau1 && (std::abs(selectedTau1->m_genParticle->pdgId) == DefaultValues::pdgIdTau) &&
		    selectedTau2 && (std::abs(selectedTau2->m_genParticle->pdgId) == DefaultValues::pdgIdTau))
		{
			TauSpinner::SimpleParticle boson = GetSimpleParticle(product.m_genBosonLV, settings.GetBosonPdgIds()[0]);
			TauSpinner::SimpleParticle tau1 = GetSimpleParticle(selectedTau1->m_genParticle->p4, selectedTau1->m_genParticle->pdgId);
			TauSpinner::SimpleParticle tau2 = GetSimpleParticle(selectedTau2->m_genParticle->p4, selectedTau2->m_genParticle->pdgId);
			std::vector<TauSpinner::SimpleParticle> tauFinalStates1;
			GetFinalStates(*selectedTau1, tauFinalStates1, m_useIC);
			std::vector<TauSpinner::SimpleParticle> tauFinalStates2;
			GetFinalStates(*selectedTau2, tauFinalStates2, m_useIC);
			
			// debug information
			if (tauFinalStates1.size() == 2)
			{
				for (std::vector<TauSpinner::SimpleParticle>::iterator particle = tauFinalStates1.begin(); particle != tauFinalStates1.end(); ++particle)
				{
					if (std::abs(particle->pdgid()) == DefaultValues::pdgIdPiPlus)
					{
						product.m_tauSpinnerPdgIdTau_1 = tau1.pdgid();
						product.m_tauSpinnerETau_1 = tau1.e();
						product.m_tauSpinnerEPi_1 = particle->e();
					}
				}
			}
			
			if (tauFinalStates2.size() == 2)
			{
				for (std::vector<TauSpinner::SimpleParticle>::iterator particle = tauFinalStates2.begin(); particle != tauFinalStates2.end(); ++particle)
				{
					if (std::abs(particle->pdgid()) == DefaultValues::pdgIdPiPlus)
					{
						product.m_tauSpinnerPdgIdTau_2 = tau2.pdgid();
						product.m_tauSpinnerETau_2 = tau2.e();
						product.m_tauSpinnerEPi_2 = particle->e();
					}
				}
			}

			//LOG_N_TIMES(20, DEBUG) << "The event contains the following particles: " << std::endl;
			//LOG_N_TIMES(20, DEBUG) << "Boson " << std::to_string(boson) << std::endl;
			//LOG_N_TIMES(20, DEBUG) << std::string("Tau1") << std::to_string(tau1);
			//LOG_N_TIMES(20, DEBUG) << std::string("Tau2") << std::to_string(tau2);
			//LOG_N_TIMES(20, DEBUG) << std::string("Tau1FinalState") << std::to_string(tauFinalStates1);
			//LOG_N_TIMES(20, DEBUG) << std::string("Tau2FinalState") << std::to_string(tauFinalStates2);

			if ((tauFinalStates1.size() == 0) || (tauFinalStates2.size() == 0))
			{
				LOG_N_TIMES(20, WARNING) << "TauSpinnerProducer could not find enogh genParticles for the TauSpinner Algorithm" << std::endl;
				// product.m_tauSpinnerWeight = DefaultValues::UndefinedDouble; // TODO
				return;
			}
		
			//Decision for a certain weight calculation depending on BosonPdgId
			if (Utility::Contains(settings.GetBosonPdgIds(), std::abs(DefaultValues::pdgIdH)) ||
				Utility::Contains(settings.GetBosonPdgIds(), std::abs(DefaultValues::pdgIdHCPEven)) ||
				Utility::Contains(settings.GetBosonPdgIds(), std::abs(DefaultValues::pdgIdACPOdd)))
			{
				// set mixing angle
				// http://arxiv.org/pdf/1406.1647.pdf, section A.1, page 15
				if (settings.GetTauSpinnerMixingAnglesOverPiHalfSample() >= 0.0)
				{
					float mixingAngleOverPiHalfSample = settings.GetTauSpinnerMixingAnglesOverPiHalfSample();
					float twoTimesMixingAngleRadSample = M_PI * mixingAngleOverPiHalfSample;
					TauSpinner::setHiggsParametersTR(-cos(twoTimesMixingAngleRadSample), cos(twoTimesMixingAngleRadSample),-sin(twoTimesMixingAngleRadSample), -sin(twoTimesMixingAngleRadSample));

					srand(event.m_eventInfo->nEvent);
					product.m_optionalWeights["tauSpinnerWeight"] = TauSpinner::calculateWeightFromParticlesH(boson, tau1, tau2, tauFinalStates1, tauFinalStates2);
					product.m_tauSpinnerPolarisation = TauSpinner::getTauSpin(); // http://tauolapp.web.cern.ch/tauolapp/tau__reweight__lib_8cxx_source.html#l00020
					product.m_tauSpinnerValidOutputs = true;
				}
			}
			else if (Utility::Contains(settings.GetBosonPdgIds(), std::abs(DefaultValues::pdgIdZ)))
			{
				// call same function as for Higgs: http://tauolapp.web.cern.ch/tauolapp/namespaceTauSpinner.html#a33de132eef40cedcf39222fee0449d79
				srand(event.m_eventInfo->nEvent);
				product.m_optionalWeights["tauSpinnerWeight"] = TauSpinner::calculateWeightFromParticlesH(boson, tau1, tau2, tauFinalStates1, tauFinalStates2);
				product.m_tauSpinnerPolarisation = TauSpinner::getTauSpin(); // http://tauolapp.web.cern.ch/tauolapp/tau__reweight__lib_8cxx_source.html#l00020
				product.m_tauSpinnerValidOutputs = true;
			}
			else if (Utility::Contains(settings.GetBosonPdgIds(), std::abs(DefaultValues::pdgIdW)))
			{
				srand(event.m_eventInfo->nEvent);
				product.m_optionalWeights["tauSpinnerWeight"] = TauSpinner::calculateWeightFromParticlesWorHpn(boson, tau1, tau2, tauFinalStates1);
				product.m_tauSpinnerPolarisation = TauSpinner::getTauSpin(); // http://tauolapp.web.cern.ch/tauolapp/tau__reweight__lib_8cxx_source.html#l00020
				product.m_tauSpinnerValidOutputs = true;
			}
		
			// calculate the weights for different mixing angles
			for (std::vector<float>::const_iterator mixingAngleOverPiHalfIt = settings.GetTauSpinnerMixingAnglesOverPiHalf().begin();
				 mixingAngleOverPiHalfIt != settings.GetTauSpinnerMixingAnglesOverPiHalf().end();
				 ++mixingAngleOverPiHalfIt)
			{
				float mixingAngleOverPiHalf = *mixingAngleOverPiHalfIt;

				double tauSpinnerWeight = 1.0;
				if (Utility::Contains(settings.GetBosonPdgIds(), std::abs(DefaultValues::pdgIdH)) ||
					Utility::Contains(settings.GetBosonPdgIds(), std::abs(DefaultValues::pdgIdHCPEven)) ||
					Utility::Contains(settings.GetBosonPdgIds(), std::abs(DefaultValues::pdgIdACPOdd)))
				{
					// set mixing angle
					// http://arxiv.org/pdf/1406.1647.pdf, section A.1, page 15
					float twoTimesMixingAngleRad = M_PI * mixingAngleOverPiHalf;
					TauSpinner::setHiggsParametersTR(-cos(twoTimesMixingAngleRad), cos(twoTimesMixingAngleRad),
						                             -sin(twoTimesMixingAngleRad), -sin(twoTimesMixingAngleRad));
					
					srand(event.m_eventInfo->nEvent);
					tauSpinnerWeight = TauSpinner::calculateWeightFromParticlesH(boson, tau1, tau2, tauFinalStates1, tauFinalStates2);
				}
				else {
					tauSpinnerWeight = 0.0; // no Higgs boson;
				}

				// check for nan values // TODO: check inputs
				if (tauSpinnerWeight != tauSpinnerWeight)
				{
					tauSpinnerWeight = 0.0; // WEIGHT_NAN;
					++numberOfNanWeights;
					LOG_N_TIMES(20, DEBUG) << "Found a 'NaN' TauSpinner weight in (run, lumi, event) = ("
							   << event.m_eventInfo->nRun << ", " << event.m_eventInfo->nLumi << ", "
							   << event.m_eventInfo->nEvent << ") in the pipeline \"" << pipelineName << "\".";
				}
		
				product.m_optionalWeights[GetLabelForWeightsMap(mixingAngleOverPiHalf)] = tauSpinnerWeight;
			}
		}
	}
}

TauSpinner::SimpleParticle TauSpinnerProducer::GetSimpleParticle(RMFLV const& particleLV, int particlePdgId) const
{
	// http://tauolapp.web.cern.ch/tauolapp/classTauSpinner_1_1SimpleParticle.html
	TauSpinner::SimpleParticle particle(particleLV.Px(), particleLV.Py(), particleLV.Pz(), particleLV.E(), particlePdgId);
	
	// Adjust energy component to preseve mass. This is needed because of rounding problems in conversions of Lorentz vectors
	int iteration = 0;
	int maxIterations = 20;
	double almostZero = 1e-5;
	double targetMass2 = (particleLV.M2() > almostZero ? particleLV.M2() : 0.0);
	double currentMass2 = 0.0;
	do
	{
		double energy = std::sqrt(std::pow(particle.px(), 2.0) + std::pow(particle.py(), 2.0) + std::pow(particle.pz(), 2.0) + targetMass2);
		particle.setE(energy);
		currentMass2 = std::pow(particle.e(), 2.0) - std::pow(particle.px(), 2.0) - std::pow(particle.py(), 2.0) - std::pow(particle.pz(), 2.0);
		
		if ((targetMass2 < almostZero) && (iteration > maxIterations/2))
		{
			targetMass2 = std::pow(10.0, iteration-maxIterations-5+1);
		}
		
		++iteration;
	}
	while ((iteration < maxIterations) &&
	       ((currentMass2 < 0.0) ||
	        ((targetMass2 <= almostZero) && (currentMass2 > almostZero)) ||
	        ((targetMass2 > almostZero) && ((std::abs(currentMass2 - targetMass2) / targetMass2) > almostZero))));
	
	return particle;
}

GenParticleDecayTree* TauSpinnerProducer::GetTau(GenParticleDecayTree* currentParticle) const
{
	if ((std::abs(currentParticle->m_genParticle->pdgId) == DefaultValues::pdgIdTau) &&
	    (Utility::Contains(SafeMap::GetWithDefault(m_validPdgIdsAndStatusCodes, std::abs(currentParticle->m_genParticle->pdgId), {-1}), currentParticle->m_genParticle->status()) ||
	     Utility::Contains(SafeMap::GetWithDefault(m_validPdgIdsAndStatusCodes, std::abs(currentParticle->m_genParticle->pdgId), {-1}), -1)))
	{
		return currentParticle;
	}
	else
	{
		GenParticleDecayTree* result = nullptr;
		for (unsigned int daughterIndex = 0; daughterIndex < currentParticle->m_daughters.size(); ++daughterIndex)
		{
			result = GetTau(&(currentParticle->m_daughters[daughterIndex]));
			if (result) return result;
		}
		return result;
	}
}

// recursive function to create a vector of final states particles in the way TauSpinner expects it
std::vector<TauSpinner::SimpleParticle> TauSpinnerProducer::GetFinalStates(
		GenParticleDecayTree& currentParticle,
		std::vector<TauSpinner::SimpleParticle>& resultVector,
		bool useIC) const
{
        // create a vector of final states in Imperial College like style
        if (useIC) return GetFinalStatesIC(currentParticle, resultVector);

	// this if-condition has to define what particles go into TauSpinner
	int pdgId = currentParticle.m_genParticle->pdgId;
	const int status = currentParticle.m_genParticle->status();
	if ((std::abs(pdgId) != DefaultValues::pdgIdTau) &&
	    Utility::Contains(m_validPdgIdsAndStatusCodes, std::abs(pdgId)) &&
	    (Utility::Contains(m_validPdgIdsAndStatusCodes.at(std::abs(pdgId)), status) ||
	     Utility::Contains(m_validPdgIdsAndStatusCodes.at(std::abs(pdgId)), -1)))
	{
		// decend to last stage with given particles
		std::vector<TauSpinner::SimpleParticle> nextStageResultVector;
		
		for (unsigned int daughterIndex = 0; daughterIndex < currentParticle.m_daughters.size(); ++daughterIndex)
		{
			GetFinalStates(currentParticle.m_daughters[daughterIndex], nextStageResultVector);
		}
		
		if (nextStageResultVector.empty())
		{
			resultVector.push_back(GetSimpleParticle(currentParticle.m_genParticle->p4, pdgId));
		}
		else
		{
			resultVector.insert(resultVector.end(), nextStageResultVector.begin(), nextStageResultVector.end());
		}
	}
	else
	{
		for (unsigned int daughterIndex = 0; daughterIndex < currentParticle.m_daughters.size(); ++daughterIndex)
		{
			GetFinalStates(currentParticle.m_daughters[daughterIndex], resultVector);
		}
	}
	return resultVector;
}
//As above, but in Imperial College like style, it assumes that it is firstly called for final tau
std::vector<TauSpinner::SimpleParticle> TauSpinnerProducer::GetFinalStatesIC(
		GenParticleDecayTree& currentParticle,
		std::vector<TauSpinner::SimpleParticle>& resultVector) const
{
	// this if-condition has to define what particles go into TauSpinner
	std::set<int> allowedPdgIds = {22, 111, 211, 321, 130, 310, 11, 12, 13, 14, 16};
        for (unsigned int daughterIndex = 0; daughterIndex < currentParticle.m_daughters.size(); ++daughterIndex)
	{
	    int pdgId = currentParticle.m_daughters[daughterIndex].m_genParticle->pdgId;
	    if ( allowedPdgIds.find(std::abs(pdgId)) != allowedPdgIds.end() )
	    {
	      resultVector.push_back(GetSimpleParticle(currentParticle.m_daughters[daughterIndex].m_genParticle->p4, pdgId));
	    }
	    else
	    {
	      GetFinalStatesIC(currentParticle.m_daughters[daughterIndex], resultVector);
	    }
	}
	return resultVector;
}


std::string TauSpinnerProducer::GetLabelForWeightsMap(float mixingAngleOverPiHalf) const
{
	return ("tauSpinnerWeight" + str(boost::format("%03d") % (mixingAngleOverPiHalf * 100.0)));
}

double TauSpinnerProducer::CustomRandomGenerator()
{
	return static_cast<double>(rand()) / static_cast<double>(RAND_MAX);
}


std::string std::to_string(TauSpinner::SimpleParticle& particle)
{
	return std::string("TauSpinner::SimpleParticle(" +
			std::to_string(particle.px()) + ", " +
			std::to_string(particle.py()) + ", " +
			std::to_string(particle.pz()) + ", " +
			std::to_string(particle.e()) + ", " +
			std::to_string(particle.pdgid()) + "), mass=" +
			std::to_string(std::sqrt(std::pow(particle.e(), 2.0) - std::pow(particle.px(), 2.0) - std::pow(particle.py(), 2.0) - std::pow(particle.pz(), 2.0)))
	);
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

