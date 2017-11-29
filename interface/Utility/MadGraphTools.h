
#pragma once

#include <Python.h> // https://www.codeproject.com/Articles/11805/Embedding-Python-in-C-C-Part-I

#include "Kappa/DataFormats/interface/Kappa.h"

#include "Artus/Utility/interface/ArtusLogging.h"


class MadGraphTools
{
public:
	MadGraphTools(float mixingAngleOverPiHalf, std::string madgraphProcessDirectory, std::string madgraphParamCard, float alphaS,
	              bool madGraphSortingHeavyBQuark=false);
	virtual ~MadGraphTools();
	
	double GetMatrixElementSquared(std::vector<KLHEParticle*>& lheParticles) const; // the vector is sorted in-place to match MadGraph ordering scheme
	

private:
	static bool MadGraphParticleOrderingLightBQuark(KLHEParticle* lheParticle1, KLHEParticle* lheParticle2);
	static bool MadGraphParticleOrderingHeavyBQuark(KLHEParticle* lheParticle1, KLHEParticle* lheParticle2);
	
	static std::vector<CartesianRMFLV> BoostToHiggsCMS(std::vector<KLHEParticle*> lheParticles);
	static std::vector<int> GetPdgIds(std::vector<KLHEParticle*> lheParticles);
	
	bool m_madGraphSortingHeavyBQuark = false;
	
	PyObject* m_pyMadGraphTools = nullptr;
	
};

