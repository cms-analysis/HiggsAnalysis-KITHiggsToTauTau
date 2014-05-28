
#pragma once

#include "Artus/KappaAnalysis/interface/KappaComputedObjects.h"
#include "Artus/Utility/interface/DefaultValues.h"

/**
   \brief Extends Kappa objects with additional members.

   Extends Kappa objects (e.g. KDataElectron, KDataMuon, etc...) adding extra members 
   (e.g., isolation variables, output of MVA discriminants, etc...).
*/

class HttMuonComputed : public KMuonComputed {

public:
	double iso = DefaultValues::UndefinedDouble;
	double isoOverPt = DefaultValues::UndefinedDouble;
};

class HttElectronComputed : public KElectronComputed {

public:
	double iso = DefaultValues::UndefinedDouble;
	double isoOverPt = DefaultValues::UndefinedDouble;
};

class HttTauComputed : public KTauComputed {

public:
	double iso = DefaultValues::UndefinedDouble;
	double isoOverPt = DefaultValues::UndefinedDouble;
};
