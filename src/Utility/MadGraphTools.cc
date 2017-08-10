
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Utility/MadGraphTools.h"


MadGraphTools::MadGraphTools(float mixingAngleOverPiHalf, std::string madgraphProcessDirectory, std::string madgraphParamCard, float alphaS)
{
	// initialise interface to Python
	if (! Py_IsInitialized())
	{
		Py_Initialize();
	}
	PyObject* pyModulePath = PyString_FromString("HiggsAnalysis.KITHiggsToTauTau.madgraph.reweighting");
	PyObject* pyModule = PyImport_Import(pyModulePath);
	PyObject* pyModuleDict = PyModule_GetDict(pyModule);
	PyObject* pyClass = PyDict_GetItemString(pyModuleDict, "MadGraphTools");
	assert(pyClass != nullptr);
	
	// get instance of Python class MadGraphTools
	PyObject* pyMixingAngleOverPiHalf = PyFloat_FromDouble(mixingAngleOverPiHalf);
	PyObject* pyMadgraphProcessDirectory = PyString_FromString(madgraphProcessDirectory.c_str());
	PyObject* pyMadgraphParamCard = PyString_FromString(madgraphParamCard.c_str());
	PyObject* pyAlphaS = PyFloat_FromDouble(alphaS);
	PyObject* pyArguments = PyTuple_Pack(4, pyMixingAngleOverPiHalf, pyMadgraphProcessDirectory, pyMadgraphParamCard, pyAlphaS);
	m_pyMadGraphTools = PyObject_CallObject(pyClass, pyArguments);
	PyErr_Print();
	assert((m_pyMadGraphTools != nullptr) && PyObject_IsInstance(m_pyMadGraphTools, pyClass));
	
	// clean up; warning: http://stackoverflow.com/a/14678667
	Py_DECREF(pyModulePath);
	//Py_DECREF(pyModule);
	//Py_DECREF(pyModuleDict);
	//Py_DECREF(pyClass);
	Py_DECREF(pyMixingAngleOverPiHalf);
	Py_DECREF(pyMadgraphProcessDirectory);
	Py_DECREF(pyMadgraphParamCard);
	Py_DECREF(pyAlphaS);
	Py_DECREF(pyArguments);
}

MadGraphTools::~MadGraphTools()
{
	//Py_DECREF(m_pyMadGraphTools);
	
	if (Py_IsInitialized())
	{
		Py_Finalize();
	}
}

double MadGraphTools::GetMatrixElementSquared(std::vector<CartesianRMFLV*> const& particleFourMomenta) const
{
	// construct Python list of four-momenta
	PyObject* pyParticleFourMomenta = PyList_New(0);
	for (std::vector<CartesianRMFLV*>::const_iterator particleLV = particleFourMomenta.begin(); particleLV != particleFourMomenta.end(); ++particleLV)
	{
		PyObject* pyParticleFourMomentum = PyList_New(0);
		PyList_Append(pyParticleFourMomentum, PyFloat_FromDouble((*particleLV)->E()));
		PyList_Append(pyParticleFourMomentum, PyFloat_FromDouble((*particleLV)->Px()));
		PyList_Append(pyParticleFourMomentum, PyFloat_FromDouble((*particleLV)->Py()));
		PyList_Append(pyParticleFourMomentum, PyFloat_FromDouble((*particleLV)->Pz()));
		PyList_Append(pyParticleFourMomenta, pyParticleFourMomentum);
	}
	
	// call MadGraphTools.matrix_element_squared
	PyObject* pyMethodName = PyString_FromString("matrix_element_squared");
	PyObject* pyMatrixElementSquared = PyObject_CallMethodObjArgs(m_pyMadGraphTools, pyMethodName, pyParticleFourMomenta, NULL);
	PyErr_Print();
	double matrixElementSquared = -1.0;
	if (pyMatrixElementSquared != nullptr)
	{
		matrixElementSquared = PyFloat_AsDouble(pyMatrixElementSquared);
		Py_DECREF(pyMatrixElementSquared);
	}
	
	// clean up
	Py_DECREF(pyParticleFourMomenta);
	Py_DECREF(pyMethodName);
	
	return matrixElementSquared;
}

