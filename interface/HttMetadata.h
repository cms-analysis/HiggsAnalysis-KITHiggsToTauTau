
#pragma once

#include "Artus/KappaAnalysis/interface/KappaMetadata.h"

#include "ZZMatrixElement/MELA/interface/Mela.h"


class HttMetadata : public KappaMetadata
{
public:
	HttMetadata();
	virtual ~HttMetadata();

	Mela* m_mela = nullptr; // Fortran code behind this class should not be initialised multiple times
};

