#include <algorithm>

#include "HiggsAnalysis/KITHiggsToTauTau/interface/Utility/MadGraphTools.h"
#include "Artus/Utility/interface/DefaultValues.h"

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

double MadGraphTools::GetMatrixElementSquared(std::vector<CartesianRMFLV*> const& particleFourMomenta, std::vector<int> const& particlepdgs) const
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
	
	//construct list of particle pdgs
	PyObject* pyParticlepdgs = PyList_New(0);
	for (std::vector<int>::const_iterator particlepdgId = particlepdgs.begin(); particlepdgId != particlepdgs.end(); ++particlepdgId)
	{
		PyList_Append(pyParticlepdgs, PyInt_FromLong(*particlepdgId));
	}	

	// call MadGraphTools.matrix_element_squared
	PyObject* pyMethodName = PyString_FromString("matrix_element_squared");
	PyObject* pyMatrixElementSquared = PyObject_CallMethodObjArgs(m_pyMadGraphTools, pyMethodName, pyParticleFourMomenta, pyParticlepdgs, NULL);
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

// pdgParticle->GetName() has no specific order
// madgraph sorts particle before antiparticle
// puts gluons first
// up type quarks second
// downtype quarks third
// => the order is: g u c d s b u_bar c_bar d_bar s_bar b_bar
bool MadGraphTools::MadGraphParticleOrderingLightBQuark(KLHEParticle* lheParticle1, KLHEParticle* lheParticle2)
{
	int pdgId1 = std::abs(lheParticle1->pdgId);
	int pdgId2 = std::abs(lheParticle2->pdgId);
	
	if ((lheParticle1->pdgId < 0) && (lheParticle2->pdgId > 0))
	{
		return false;
	}
	else if ((lheParticle1->pdgId > 0) && (lheParticle2->pdgId < 0))
	{
		return true;
	}
	else
	{
		if (pdgId1 == DefaultValues::pdgIdGluon)
		{
			return true;
		}
		else if (pdgId2 == DefaultValues::pdgIdGluon)
		{
			return false;
		}
		else if (pdgId1 == DefaultValues::pdgIdUp)
		{
			return true;
		}
		else if (pdgId2 == DefaultValues::pdgIdUp)
		{
			return false;
		}
		else if (pdgId1 == DefaultValues::pdgIdCharm)
		{
			return true;
		}
		else if (pdgId2 == DefaultValues::pdgIdCharm)
		{
			return false;
		}
		else if (pdgId1 == DefaultValues::pdgIdDown)
		{
			return true;
		}
		else if (pdgId2 == DefaultValues::pdgIdDown)
		{
			return false;
		}
		else if (pdgId1 == DefaultValues::pdgIdStrange)
		{
			return true;
		}
		else if (pdgId2 == DefaultValues::pdgIdStrange)
		{
			return false;
		}
		else if (pdgId1 == DefaultValues::pdgIdBottom)
		{
			return true;
		}
		else if (pdgId2 == DefaultValues::pdgIdBottom)
		{
			return false;
		}
		else
		{
			return true;
		}
	}
}

// pdgParticle->GetName() has no specific order
// madgraph sorts particle before antiparticle
// puts gluons first
// up type quarks second
// downtype quarks third
// heavy quarks last => the order is: g u c d s u_bar c_bar d_bar s_bar b b_bar
bool MadGraphTools::MadGraphParticleOrderingHeavyBQuark(KLHEParticle* lheParticle1, KLHEParticle* lheParticle2)
{
	int pdgId1 = std::abs(lheParticle1->pdgId);
	int pdgId2 = std::abs(lheParticle2->pdgId);
	
	if ((lheParticle1->pdgId < 0) && (lheParticle2->pdgId > 0) && (pdgId1 != DefaultValues::pdgIdBottom) && (pdgId2 == DefaultValues::pdgIdBottom))
	{
		return true;
	}
	else if ((lheParticle1->pdgId > 0) && (lheParticle2->pdgId < 0) && (pdgId1 == DefaultValues::pdgIdBottom) && (pdgId2 != DefaultValues::pdgIdBottom))
	{
		return false;
	}
	else
	{
		return MadGraphTools::MadGraphParticleOrderingLightBQuark(lheParticle1, lheParticle2);
	}
}

std::vector<CartesianRMFLV*> MadGraphTools::BoostedCartesianRMFLV(std::vector<KLHEParticle*> particles)
{
	std::vector<CartesianRMFLV*> particleFourMomenta;
	std::vector<CartesianRMFLV*> particleFourMomenta_HiggsCM;
	
	CartesianRMFLV higgsp4 = CartesianRMFLV(0,0,0,1);

	

	for (std::vector<KLHEParticle*>::iterator madGraphLheParticle = particles.begin();
	     madGraphLheParticle != particles.end(); ++madGraphLheParticle)
	{
		particleFourMomenta.push_back(&((*madGraphLheParticle)->p4));

		//extract 4-momentum of the higgs boson	
		if ((*madGraphLheParticle)->pdgId == 25) {
			 higgsp4 = (*madGraphLheParticle)->p4;
		}
	}
	// Calculate boost to Higgs CMRF and boost particle LV to it. 
	CartesianRMFLV::BetaVector boostvec = higgsp4.BoostToCM();
	ROOT::Math::Boost M(boostvec);
	
	for (std::vector<CartesianRMFLV*>::iterator particleLV= particleFourMomenta.begin(); particleLV != particleFourMomenta.end(); ++particleLV) 
	{		
		CartesianRMFLV tmpParticleLV = CartesianRMFLV((*particleLV)->Px(), (*particleLV)->Py(), (*particleLV)->Pz(), (*particleLV)->E());
	 	tmpParticleLV = M * tmpParticleLV;
		CartesianRMFLV* CmLV = new CartesianRMFLV(tmpParticleLV.Px(), tmpParticleLV.Py(), tmpParticleLV.Pz(), tmpParticleLV.E());
		particleFourMomenta_HiggsCM.push_back(CmLV);
	 }
	return particleFourMomenta_HiggsCM;
}


std::vector<int> MadGraphTools::pdgID(std::vector<KLHEParticle*> particles)
{
	std::vector<int> particlepdgs;
	for (std::vector<KLHEParticle*>::iterator madGraphLheParticle = particles.begin();
	     madGraphLheParticle != particles.end(); ++madGraphLheParticle)
	{
		particlepdgs.push_back((*madGraphLheParticle)->pdgId);
	}
	return particlepdgs;
}






