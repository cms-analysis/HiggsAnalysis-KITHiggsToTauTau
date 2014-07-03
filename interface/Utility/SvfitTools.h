
#pragma once

#include "TauAnalysis/SVfitStandalone/interface/SVfitStandaloneAlgorithm.h"

#include "Kappa/DataFormats/interface/Kappa.h"


typedef typename ROOT::Math::DisplacementVector3D<ROOT::Math::Cartesian3D<float>,ROOT::Math::DefaultCoordinateSystemTag> RMDataV;
typedef typename ROOT::Math::SMatrix<double, 2, 2, ROOT::Math::MatRepSym<double, 2> > RMSM2x2;


/**
 */
class RunLumiEvent { // TODO: move to a more general place?

public:
	int run;
	int lumi;
	int event;
	
	RunLumiEvent() {};
	RunLumiEvent(int run, int lumi, int event);
	
	void Set(int run, int lumi, int event);
	
	void CreateBranches(TTree* tree);
	void SetBranchAddresses(TTree* tree);
	
	bool operator==(RunLumiEvent const& rhs) const;
};


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
	
	void CreateBranches(TTree* tree);
	void SetBranchAddresses(TTree* tree);
	
	bool operator==(SvfitInputs const& rhs) const;
	
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
	void Set(SVfitStandaloneAlgorithm const& svfitStandaloneAlgorithm);
	
	void CreateBranches(TTree* tree);
	void SetBranchAddresses(TTree* tree);
	
	bool operator==(SvfitResults const& rhs) const;


private:
	RMDataLV GetMomentum(SVfitStandaloneAlgorithm const& svfitStandaloneAlgorithm) const;
	RMDataLV GetMomentumUncertainty(SVfitStandaloneAlgorithm const& svfitStandaloneAlgorithm) const;
};

