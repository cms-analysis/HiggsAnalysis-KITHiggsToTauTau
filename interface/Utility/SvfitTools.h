
#pragma once

#include "TauAnalysis/SVfitStandalone/interface/SVfitStandaloneAlgorithm.h"

#include "Kappa/DataFormats/interface/Kappa.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"


/**
 */
class SvfitInputs {

public:
	int decayType1;
	int decayType2;
	
	RMDataLV leptonMomentum1;
	RMDataLV leptonMomentum2;
	
	RMDataV metMomentum;
	RMSM2x2 metCovariance;
	
	SvfitInputs() {};
	SvfitInputs(svFitStandalone::kDecayType const& decayType1, svFitStandalone::kDecayType const& decayType2,
	            RMDataLV const& leptonMomentum1, RMDataLV const& leptonMomentum2,
	            RMDataV const& metMomentum, RMSM2x2 const& metCovariance);
	
	void Set(svFitStandalone::kDecayType const& decayType1, svFitStandalone::kDecayType const& decayType2,
	         RMDataLV const& leptonMomentum1, RMDataLV const& leptonMomentum2,
	         RMDataV const& metMomentum, RMSM2x2 const& metCovariance);
	
	SVfitStandaloneAlgorithm GetSvfitStandaloneAlgorithm(int verbosity=0, bool addLogM=false) const;

	
private:
	std::vector<svFitStandalone::MeasuredTauLepton> GetMeasuredTauLeptons() const;
	TMatrixD GetMetCovarianceMatrix() const;
};


/**
 */
class SvfitResults {

public:
	RMDataLV momentum;
	RMDataLV momentumUncertainty;
	
	SvfitResults() {};
	SvfitResults(RMDataLV const& momentum, RMDataLV const& momentumUncertainty);
	SvfitResults(SVfitStandaloneAlgorithm const& svfitStandaloneAlgorithm);
	
	void Set(RMDataLV const& momentum, RMDataLV const& momentumUncertainty);


private:
	RMDataLV GetMomentum(SVfitStandaloneAlgorithm const& svfitStandaloneAlgorithm) const;
	RMDataLV GetMomentumUncertainty(SVfitStandaloneAlgorithm const& svfitStandaloneAlgorithm) const;
};

