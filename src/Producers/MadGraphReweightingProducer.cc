
#include <algorithm>
#include <math.h>

#include <boost/format.hpp>

#include "Artus/Utility/interface/DefaultValues.h"
#include "Artus/Utility/interface/SafeMap.h"
#include "Artus/Utility/interface/Utility.h"
#include "Artus/Consumer/interface/LambdaNtupleConsumer.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/MadGraphReweightingProducer.h"


MadGraphReweightingProducer::~MadGraphReweightingProducer()
{
	// clean up
	if (m_initialised)
	{
		Py_DECREF(m_functionMadGraphWeightGGH);
		Py_Finalize();
	}
}

std::string MadGraphReweightingProducer::GetProducerId() const
{
	return "MadGraphReweightingProducer";
}

void MadGraphReweightingProducer::Init(setting_type const& settings)
{
	ProducerBase<HttTypes>::Init(settings);
	
	// initialise access to python code
	// https://www.codeproject.com/Articles/11805/Embedding-Python-in-C-C-Part-I
	Py_Initialize();
	PyObject* modulePath = PyString_FromString("HiggsAnalysis.KITHiggsToTauTau.madgraph.reweighting");
	PyObject* module = PyImport_Import(modulePath);
	PyObject* moduleDict = PyModule_GetDict(module);
	
	m_functionMadGraphWeightGGH = PyDict_GetItemString(moduleDict, "madgraph_weight_ggh");
	
	Py_DECREF(modulePath);
	Py_DECREF(module);
	Py_DECREF(moduleDict);
	assert(PyCallable_Check(m_functionMadGraphWeightGGH));
	
	m_initialised = true;
	
	// quantities for LambdaNtupleConsumer
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
		assert(Utility::Contains(settings.GetTauSpinnerMixingAnglesOverPiHalf(), mixingAngleOverPiHalfSample));
		
		std::string mixingAngleOverPiHalfSampleLabel = GetLabelForWeightsMap(mixingAngleOverPiHalfSample);
		LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("madGraphWeightSample", [mixingAngleOverPiHalfSampleLabel](event_type const& event, product_type const& product)
		{
			return SafeMap::GetWithDefault(product.m_optionalWeights, mixingAngleOverPiHalfSampleLabel, 0.0);
		});
		LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("madGraphWeightInvSample", [mixingAngleOverPiHalfSampleLabel](event_type const& event, product_type const& product)
		{
			double weight = SafeMap::GetWithDefault(product.m_optionalWeights, mixingAngleOverPiHalfSampleLabel, 0.0);
			//return std::min(((weight > 0.0) ? (1.0 / weight) : 0.0), 10.0);   // no physics reason for this
			return ((weight > 0.0) ? (1.0 / weight) : 0.0);
		});
	}
}


void MadGraphReweightingProducer::Produce(event_type const& event, product_type& product,
								          setting_type const& settings) const
{
	assert(event.m_eventInfo);
	
	float mixingAngleOverPiHalf = 0.0; // TODO
	RMFLV gluon1LV; // TODO
	RMFLV gluon2LV; // TODO
	RMFLV higgsLV; // TODO
	
	PyObject* arguments = PyTuple_Pack(4,
			PyFloat_FromDouble(mixingAngleOverPiHalf),
			PyTuple_Pack(4,
				PyFloat_FromDouble(gluon1LV.Px()),
				PyFloat_FromDouble(gluon1LV.Py()),
				PyFloat_FromDouble(gluon1LV.Pz()),
				PyFloat_FromDouble(gluon1LV.E())
			),
			PyTuple_Pack(4,
				PyFloat_FromDouble(gluon2LV.Px()),
				PyFloat_FromDouble(gluon2LV.Py()),
				PyFloat_FromDouble(gluon2LV.Pz()),
				PyFloat_FromDouble(gluon2LV.E())
			),
			PyTuple_Pack(4,
				PyFloat_FromDouble(higgsLV.Px()),
				PyFloat_FromDouble(higgsLV.Py()),
				PyFloat_FromDouble(higgsLV.Pz()),
				PyFloat_FromDouble(higgsLV.E())
			)
	);
	
	PyObject* resultGGH = PyObject_CallObject(m_functionMadGraphWeightGGH, arguments);
	if (resultGGH)
	{
		//int result = PyInt_AsLong(resultGGH);
		//LOG(ERROR) << result;
	}
	else
	{
		PyErr_Print();
	}
	
	// clean up
	Py_DECREF(arguments);
	Py_DECREF(resultGGH);
	
	/*
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
			LOG_N_TIMES(20, WARNING) << "MadGraphReweightingProducer could not find enogh genParticles for the TauSpinner Algorithm" << std::endl;
			// product.m_madGraphWeight = DefaultValues::UndefinedDouble; // TODO
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
			
			product.m_optionalWeights["madGraphWeight"] = calculateWeightFromParticlesH(boson, tau1, tau2, tauFinalStates1, tauFinalStates2);
			product.m_tauSpinnerPolarisation = TauSpinner::getTauSpin(); // http://tauolapp.web.cern.ch/tauolapp/tau__reweight__lib_8cxx_source.html#l00020
		}
		else if (Utility::Contains(settings.GetBosonPdgIds(), std::abs(DefaultValues::pdgIdZ)))
		{
			// call same function as for Higgs: http://tauolapp.web.cern.ch/tauolapp/namespaceTauSpinner.html#a33de132eef40cedcf39222fee0449d79
			product.m_optionalWeights["madGraphWeight"] = calculateWeightFromParticlesH(boson, tau1, tau2, tauFinalStates1, tauFinalStates2);
			product.m_tauSpinnerPolarisation = TauSpinner::getTauSpin(); // http://tauolapp.web.cern.ch/tauolapp/tau__reweight__lib_8cxx_source.html#l00020
		}
		else if (Utility::Contains(settings.GetBosonPdgIds(), std::abs(DefaultValues::pdgIdW)))
		{
			product.m_optionalWeights["madGraphWeight"] = calculateWeightFromParticlesWorHpn(boson, tau1, tau2, tauFinalStates1);
			product.m_tauSpinnerPolarisation = TauSpinner::getTauSpin(); // http://tauolapp.web.cern.ch/tauolapp/tau__reweight__lib_8cxx_source.html#l00020
		}
		
		// calculate the weights for different mixing angles
		for (std::vector<float>::const_iterator mixingAngleOverPiHalfIt = settings.GetTauSpinnerMixingAnglesOverPiHalf().begin();
			 mixingAngleOverPiHalfIt != settings.GetTauSpinnerMixingAnglesOverPiHalf().end();
			 ++mixingAngleOverPiHalfIt)
		{
			float mixingAngleOverPiHalf = *mixingAngleOverPiHalfIt;

			double madGraphWeight = 1.0;
			if (Utility::Contains(settings.GetBosonPdgIds(), std::abs(DefaultValues::pdgIdH)) ||
			    Utility::Contains(settings.GetBosonPdgIds(), std::abs(DefaultValues::pdgIdHCPOdd)) ||
			    Utility::Contains(settings.GetBosonPdgIds(), std::abs(DefaultValues::pdgIdACPOdd)))
			{
				// set mixing angle
				// http://arxiv.org/pdf/1406.1647.pdf, section A.1, page 15
				float twoTimesMixingAngleRad = M_PI * mixingAngleOverPiHalf;
				TauSpinner::setHiggsParametersTR(-cos(twoTimesMixingAngleRad), cos(twoTimesMixingAngleRad),
				                                 -sin(twoTimesMixingAngleRad), -sin(twoTimesMixingAngleRad));
				
				madGraphWeight = calculateWeightFromParticlesH(boson, tau1, tau2, tauFinalStates1, tauFinalStates2);
			}
			else {
				madGraphWeight = 0.0; // no Higgs boson;
			}
		
			product.m_optionalWeights[GetLabelForWeightsMap(mixingAngleOverPiHalf)] = madGraphWeight;
		}
	}*/
}

std::string MadGraphReweightingProducer::GetLabelForWeightsMap(float mixingAngleOverPiHalf) const
{
	return ("madGraphWeight" + str(boost::format("%03d") % (mixingAngleOverPiHalf * 100.0)));
}

