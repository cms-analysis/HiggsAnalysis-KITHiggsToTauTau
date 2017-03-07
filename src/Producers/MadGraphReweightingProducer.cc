
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
		Py_DECREF(m_madGraphMatrixElementTools);
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
	PyObject* madGraphMatrixElementToolsClass = PyDict_GetItemString(moduleDict, "MadGraphMatrixElementTools");
	
	PyObject* mixingAngles = PyTuple_New(settings.GetTauSpinnerMixingAnglesOverPiHalf().size());
	for (unsigned int indexMixingAngle = 0; indexMixingAngle < settings.GetTauSpinnerMixingAnglesOverPiHalf().size(); ++indexMixingAngle)
	{
		PyTuple_SetItem(mixingAngles, indexMixingAngle, PyFloat_FromDouble(settings.GetTauSpinnerMixingAnglesOverPiHalf()[indexMixingAngle]));
	}
	PyObject* arguments = PyTuple_Pack(3,
			mixingAngles,
			PyString_FromString(settings.GetMadGraphParamCard().c_str()),
			PyString_FromString(settings.GetMadGraphProcessDirectory().c_str())
	);
	
	m_madGraphMatrixElementTools = PyObject_CallObject(madGraphMatrixElementToolsClass, arguments);
	
	Py_DECREF(modulePath);
	Py_DECREF(module);
	Py_DECREF(moduleDict);
	Py_DECREF(mixingAngles);
	Py_DECREF(arguments);
	
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
	
	// TODO: should this be an assertion (including a filter to run before this producer)?
	if ((product.m_genBosonParticle != nullptr) &&
	    (product.m_genParticlesProducingBoson.size() > 1) &&
	    (product.m_genParticlesProducingBoson.at(0)->pdgId == DefaultValues::pdgIdGluon) &&
	    (product.m_genParticlesProducingBoson.at(1)->pdgId == DefaultValues::pdgIdGluon))
	{
		RMFLV gluon1LV = product.m_genParticlesProducingBoson.at(0)->p4;
		RMFLV gluon2LV = product.m_genParticlesProducingBoson.at(1)->p4;
		RMFLV higgsLV = product.m_genBosonParticle->p4;
		
		PyObject* function = PyString_FromString("matrix_element_squared");
		
		PyObject* mixingAngle = PyFloat_FromDouble(settings.GetTauSpinnerMixingAnglesOverPiHalfSample());
		PyObject* processDirectory = PyString_FromString(settings.GetMadGraphProcessDirectory().c_str());
		PyObject* gluon1Momentum = PyTuple_Pack(4,
				PyFloat_FromDouble(gluon1LV.E()),
				PyFloat_FromDouble(gluon1LV.Px()),
				PyFloat_FromDouble(gluon1LV.Py()),
				PyFloat_FromDouble(gluon1LV.Pz())
		);
		PyObject* gluon2Momentum = PyTuple_Pack(4,
				PyFloat_FromDouble(gluon2LV.E()),
				PyFloat_FromDouble(gluon2LV.Px()),
				PyFloat_FromDouble(gluon2LV.Py()),
				PyFloat_FromDouble(gluon2LV.Pz())
		);
		PyObject* higgsMomentum = PyTuple_Pack(4,
				PyFloat_FromDouble(higgsLV.E()),
				PyFloat_FromDouble(higgsLV.Px()),
				PyFloat_FromDouble(higgsLV.Py()),
				PyFloat_FromDouble(higgsLV.Pz())
		);
		
		PyObject* matrixElement2GGHSample = PyObject_CallMethodObjArgs(m_madGraphMatrixElementTools, function, mixingAngle, processDirectory, gluon1Momentum, gluon2Momentum, higgsMomentum, NULL);
		if (matrixElement2GGHSample != nullptr)
		{
			product.m_optionalWeights["madGraphWeight"] = PyFloat_AsDouble(matrixElement2GGHSample);
		}
		else
		{
			PyErr_Print();
		}
		// clean up
		Py_DECREF(mixingAngle);
		Py_DECREF(matrixElement2GGHSample);
		
		// calculate the weights for different mixing angles
		for (std::vector<float>::const_iterator mixingAngleOverPiHalfIt = settings.GetTauSpinnerMixingAnglesOverPiHalf().begin();
			 mixingAngleOverPiHalfIt != settings.GetTauSpinnerMixingAnglesOverPiHalf().end();
			 ++mixingAngleOverPiHalfIt)
		{
			float mixingAngleOverPiHalf = *mixingAngleOverPiHalfIt;
			mixingAngle = PyFloat_FromDouble(mixingAngleOverPiHalf);
			PyObject* matrixElement2GGH = PyObject_CallMethodObjArgs(m_madGraphMatrixElementTools, function, mixingAngle, processDirectory, gluon1Momentum, gluon2Momentum, higgsMomentum, NULL);
			if (matrixElement2GGH != nullptr)
			{
				product.m_optionalWeights[GetLabelForWeightsMap(mixingAngleOverPiHalf)] = PyFloat_AsDouble(matrixElement2GGH);
			}
			else
			{
				PyErr_Print();
			}
			Py_DECREF(matrixElement2GGH); // clean up
		}
		
		// clean up
		Py_DECREF(function);
		Py_DECREF(mixingAngle);
		Py_DECREF(processDirectory);
		Py_DECREF(gluon1Momentum);
		Py_DECREF(gluon2Momentum);
		Py_DECREF(higgsMomentum);
	}
}

std::string MadGraphReweightingProducer::GetLabelForWeightsMap(float mixingAngleOverPiHalf) const
{
	return ("madGraphWeight" + str(boost::format("%03d") % (mixingAngleOverPiHalf * 100.0)));
}

