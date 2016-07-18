
#include <algorithm>
#include <math.h>

#include <boost/format.hpp>

#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/TauSpinnerProducer.h"
#include "Artus/KappaAnalysis/interface/KappaProduct.h"

#include "Artus/Utility/interface/DefaultValues.h"
#include "Artus/Utility/interface/SafeMap.h"
#include "Artus/Utility/interface/Utility.h"
#include "Artus/Consumer/interface/LambdaNtupleConsumer.h"

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

void TauSpinnerProducer::Init(setting_type const& settings)
{
	ProducerBase<HttTypes>::Init(settings);
	
	pipelineName = settings.GetName();
	
	// interface to TauSpinner
	// see the print out of this function or tau_reweight_lib.cxx for explanation of paramesters
	// $CMSSW_RELEASE_BASE/../../../external/tauolapp/1.1.5-cms2/include/TauSpinner/tau_reweight_lib.h
	// http://tauolapp.web.cern.ch/tauolapp/tau__reweight__lib_8cxx_source.html
	// http://tauolapp.web.cern.ch/tauolapp/namespaceTauSpinner.html
	// https://arxiv.org/pdf/1402.2068v1.pdf
	Tauolapp::Tauola::initialize();
	LHAPDF::initPDFSetByName(settings.GetTauSpinnerSettingsPDF());
	
	TauSpinner::initialize_spinner(settings.GetTauSpinnerSettingsIpp(),
	                               settings.GetTauSpinnerSettingsIpol(),
	                               settings.GetTauSpinnerSettingsNonSM2(),
	                               settings.GetTauSpinnerSettingsNonSMN(),
	                               settings.GetTauSpinnerSettingsCmsEnergy());
	
	
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("tauSpinnerPolarisation", [](event_type const& event, product_type const& product)
	{
		return product.m_tauSpinnerPolarisation;
	});
	
	for (std::vector<float>::const_iterator mixingAngleOverPiHalfIt = settings.GetTauSpinnerMixingAnglesOverPiHalf().begin();
	     mixingAngleOverPiHalfIt != settings.GetTauSpinnerMixingAnglesOverPiHalf().end();
	     ++mixingAngleOverPiHalfIt)
	{
		float mixingAngleOverPiHalf = *mixingAngleOverPiHalfIt;
		std::string mixingAngleOverPiHalfLabel = GetLabelForWeightsMap(mixingAngleOverPiHalf);
		LambdaNtupleConsumer<HttTypes>::AddFloatQuantity(mixingAngleOverPiHalfLabel, [mixingAngleOverPiHalfLabel](event_type const& event, product_type const& product)
		{
			return SafeMap::GetWithDefault(product.m_optionalWeights, mixingAngleOverPiHalfLabel, 0.0);
		});
	}
	
	
	if (settings.GetTauSpinnerMixingAnglesOverPiHalfSample() >= 0.0)
	{
		float mixingAngleOverPiHalfSample = settings.GetTauSpinnerMixingAnglesOverPiHalfSample();
	
		// if mixing angle for curent sample is defined, it has to be in the list TauSpinnerMixingAnglesOverPiHalf
		assert(std::find(settings.GetTauSpinnerMixingAnglesOverPiHalf().begin(),
		                 settings.GetTauSpinnerMixingAnglesOverPiHalf().end(),
		                 mixingAngleOverPiHalfSample) != settings.GetTauSpinnerMixingAnglesOverPiHalf().end());
		
		std::string mixingAngleOverPiHalfSampleLabel = GetLabelForWeightsMap(mixingAngleOverPiHalfSample);
		LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("tauSpinnerWeightSample", [mixingAngleOverPiHalfSampleLabel](event_type const& event, product_type const& product)
		{
			return SafeMap::GetWithDefault(product.m_optionalWeights, mixingAngleOverPiHalfSampleLabel, 0.0);
		});
		LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("tauSpinnerWeightInvSample", [mixingAngleOverPiHalfSampleLabel](event_type const& event, product_type const& product)
		{
			double weight = SafeMap::GetWithDefault(product.m_optionalWeights, mixingAngleOverPiHalfSampleLabel, 0.0);
			//return std::min(((weight > 0.0) ? (1.0 / weight) : 0.0), 10.0);   // no physics reason for this
			return ((weight > 0.0) ? (1.0 / weight) : 0.0);
		});
	}
}


void TauSpinnerProducer::Produce(event_type const& event, product_type& product,
								 setting_type const& settings) const
{
	assert(event.m_eventInfo);
	
	// A generator level boson and its decay products must exist
	// The boson is searched for by a GenBosonProducer
	// and the decay tree is built by the GenTauDecayProducer
	assert(product.m_genBosonTree.m_daughters.size() > 1);
	
	assert(! settings.GetBosonPdgIds().empty());

	GenParticleDecayTree selectedTau1 = product.m_genBosonTree.m_daughters[0];
	GenParticleDecayTree selectedTau2 = product.m_genBosonTree.m_daughters[1];
	
	//TauSpinner considers only Taus and Tau-Neutrinos as daughters of a Boson (Higgs, W etc.)
	// otherwise the weights are set to 1
	if ((std::abs(selectedTau1.m_genParticle->pdgId) == DefaultValues::pdgIdTau) && (std::abs(selectedTau2.m_genParticle->pdgId) == DefaultValues::pdgIdTau))
	{
		TauSpinner::SimpleParticle boson = GetSimpleParticle(product.m_genBosonLV, settings.GetBosonPdgIds()[0]);
		TauSpinner::SimpleParticle tau1 = GetSimpleParticle(selectedTau1.m_genParticle->p4, selectedTau1.m_genParticle->pdgId);
		TauSpinner::SimpleParticle tau2 = GetSimpleParticle(selectedTau2.m_genParticle->p4, selectedTau2.m_genParticle->pdgId);
		std::vector<TauSpinner::SimpleParticle> tauFinalStates1;
		GetFinalStates(selectedTau1, tauFinalStates1);
		std::vector<TauSpinner::SimpleParticle> tauFinalStates2;
		GetFinalStates(selectedTau2, tauFinalStates2);

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
		    Utility::Contains(settings.GetBosonPdgIds(), std::abs(DefaultValues::pdgIdHCPOdd)) ||
		    Utility::Contains(settings.GetBosonPdgIds(), std::abs(DefaultValues::pdgIdACPOdd)))
		{
			// set mixing angle
			// http://arxiv.org/pdf/1406.1647.pdf, section A.1, page 15
			float mixingAngleOverPiHalfSample = settings.GetTauSpinnerMixingAnglesOverPiHalfSample();
			float twoTimesMixingAngleRadSample = M_PI * mixingAngleOverPiHalfSample;
			TauSpinner::setHiggsParametersTR(-cos(twoTimesMixingAngleRadSample), cos(twoTimesMixingAngleRadSample),
			                                 -sin(twoTimesMixingAngleRadSample), -sin(twoTimesMixingAngleRadSample));
			
			product.m_optionalWeights["tauSpinnerWeight"] = calculateWeightFromParticlesH(boson, tau1, tau2, tauFinalStates1, tauFinalStates2);
			product.m_tauSpinnerPolarisation = TauSpinner::getTauSpin(); // http://tauolapp.web.cern.ch/tauolapp/tau__reweight__lib_8cxx_source.html#l00020
		}
		else if (Utility::Contains(settings.GetBosonPdgIds(), std::abs(DefaultValues::pdgIdZ)))
		{
			// call same function as for Higgs: http://tauolapp.web.cern.ch/tauolapp/namespaceTauSpinner.html#a33de132eef40cedcf39222fee0449d79
			product.m_optionalWeights["tauSpinnerWeight"] = calculateWeightFromParticlesH(boson, tau1, tau2, tauFinalStates1, tauFinalStates2);
			product.m_tauSpinnerPolarisation = TauSpinner::getTauSpin(); // http://tauolapp.web.cern.ch/tauolapp/tau__reweight__lib_8cxx_source.html#l00020
		}
		else if (Utility::Contains(settings.GetBosonPdgIds(), std::abs(DefaultValues::pdgIdW)))
		{
			product.m_optionalWeights["tauSpinnerWeight"] = calculateWeightFromParticlesWorHpn(boson, tau1, tau2, tauFinalStates1);
			product.m_tauSpinnerPolarisation = TauSpinner::getTauSpin(); // http://tauolapp.web.cern.ch/tauolapp/tau__reweight__lib_8cxx_source.html#l00020
		}
		
		// calculate the weights for different mixing angles
		for (std::vector<float>::const_iterator mixingAngleOverPiHalfIt = settings.GetTauSpinnerMixingAnglesOverPiHalf().begin();
			 mixingAngleOverPiHalfIt != settings.GetTauSpinnerMixingAnglesOverPiHalf().end();
			 ++mixingAngleOverPiHalfIt)
		{
			float mixingAngleOverPiHalf = *mixingAngleOverPiHalfIt;

			double tauSpinnerWeight = 1.0;
			if (Utility::Contains(settings.GetBosonPdgIds(), std::abs(DefaultValues::pdgIdH)) ||
			    Utility::Contains(settings.GetBosonPdgIds(), std::abs(DefaultValues::pdgIdHCPOdd)) ||
			    Utility::Contains(settings.GetBosonPdgIds(), std::abs(DefaultValues::pdgIdACPOdd)))
			{
				// set mixing angle
				// http://arxiv.org/pdf/1406.1647.pdf, section A.1, page 15
				float twoTimesMixingAngleRad = M_PI * mixingAngleOverPiHalf;
				TauSpinner::setHiggsParametersTR(-cos(twoTimesMixingAngleRad), cos(twoTimesMixingAngleRad),
				                                 -sin(twoTimesMixingAngleRad), -sin(twoTimesMixingAngleRad));
				
				tauSpinnerWeight = calculateWeightFromParticlesH(boson, tau1, tau2, tauFinalStates1, tauFinalStates2);
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

TauSpinner::SimpleParticle TauSpinnerProducer::GetSimpleParticle(RMFLV const& particleLV, int particlePdgId) const
{
	return TauSpinner::SimpleParticle(particleLV.Px(), particleLV.Py(), particleLV.Pz(), particleLV.E(), particlePdgId);
}

// recursive function to create a vector of final states particles in the way TauSpinner expects it
std::vector<TauSpinner::SimpleParticle> TauSpinnerProducer::GetFinalStates(
		GenParticleDecayTree& mother,
		std::vector<TauSpinner::SimpleParticle>& resultVector) const
{
	for (unsigned int i = 0; i < mother.m_daughters.size(); ++i)
	{
		// this if-condition has to define what particles go into TauSpinner
		int pdgId = abs(mother.m_daughters[i].m_genParticle->pdgId);
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
			resultVector.push_back(GetSimpleParticle(mother.m_daughters[i].m_genParticle->p4, mother.m_daughters[i].m_genParticle->pdgId));
		}
		else
		{
			/*
			if (mother.m_daughters[i].m_finalState)
			{
				LOG(FATAL) << "Could not find a proper final state that can be handled by TauSpinner. Found particle with PDG ID " << mother.m_daughters[i].m_genParticle->pdgId << "." << std::endl;
			}
			*/
			LOG_N_TIMES(20, DEBUG) << "Recursion, pdgId " << pdgId << " is not considered being a final states" << std::endl;
			GetFinalStates(mother.m_daughters[i], resultVector);
		}
	}
	return resultVector;
}


std::string TauSpinnerProducer::GetLabelForWeightsMap(float mixingAngleOverPiHalf) const
{
	return ("tauSpinnerWeight" + str(boost::format("%03d") % (mixingAngleOverPiHalf * 100.0)));
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
