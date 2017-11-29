
#pragma once

#include <Python.h> // https://www.codeproject.com/Articles/11805/Embedding-Python-in-C-C-Part-I

#include "Kappa/DataFormats/interface/Kappa.h"

#include "Artus/Utility/interface/ArtusLogging.h"


class MadGraphTools
{
public:
	MadGraphTools(float mixingAngleOverPiHalf, std::string madgraphProcessDirectory, std::string madgraphParamCard, float alphaS);
	virtual ~MadGraphTools();
	
	double GetMatrixElementSquared(std::vector<CartesianRMFLV*> const& particleMomenta, std::vector<int> const& particlepdgs) const;

private:
	PyObject* m_pyMadGraphTools = nullptr;
};

