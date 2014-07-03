
#pragma once

#include "TauAnalysis/SVfitStandalone/interface/SVfitStandaloneAlgorithm.h"

#include "Kappa/DataFormats/interface/Kappa.h"


/**
 */
class SvfitTools {

public:

	typedef typename ROOT::Math::DisplacementVector3D<ROOT::Math::Cartesian3D<float>,ROOT::Math::DefaultCoordinateSystemTag> RMDataV;
	typedef typename ROOT::Math::SMatrix<double, 2, 2, ROOT::Math::MatRepSym<double, 2> > RMSM;

	enum class IntegrationMethod : int
	{
		MARKOV_CHAIN = 0,
		VEGAS = 1,
	};
	
	SvfitTools(svFitStandalone::kDecayType const& decayType1, svFitStandalone::kDecayType const& decayType2,
	           RMDataLV* leptonMomentum1, RMDataLV* leptonMomentum2,
	           RMDataV const& metMomentum, RMSM* metCovariance,
	           IntegrationMethod integrationMethod);
	
	RMDataLV GetTauTauMomentum();
	RMDataLV GetTauTauMomentumUncertainty();


private:
	int decayType1;
	int decayType2;
	
	RMDataLV* leptonMomentum1 = 0;
	RMDataLV* leptonMomentum2 = 0;
	
	RMDataV metMomentum;
	RMSM* metCovariance = 0;
	
	int integrationMethod;

	SVfitStandaloneAlgorithm* svfitStandaloneAlgorithm = 0;
	
	SVfitStandaloneAlgorithm* Calculate();
};

