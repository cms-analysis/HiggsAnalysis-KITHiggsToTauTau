
#pragma once

#include "Artus/Utility/interface/ArtusLogging.h"

#include "TauAnalysis/ClassicSVfit/interface/ClassicSVfit.h"
#include "TauAnalysis/ClassicSVfit/interface/MeasuredTauLepton.h"
#include "TauAnalysis/ClassicSVfit/interface/svFitHistogramAdapter.h"
#include "TauAnalysis/ClassicSVfit/interface/FastMTT.h"

#include "Kappa/DataFormats/interface/Kappa.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttEnumTypes.h"


typedef ROOT::Math::DisplacementVector3D<ROOT::Math::Cartesian3D<float>,ROOT::Math::DefaultCoordinateSystemTag> RMDataV;
typedef ROOT::Math::SMatrix<double, 2, 2, ROOT::Math::MatRepSym<double, 2> > RMSM2x2;


/**
 */
class FastMttInputs {

public:
	RMFLV* leptonMomentum1 = 0;
	int decayType1;
	int decayMode1 = 0;
	RMFLV* leptonMomentum2 = 0;
	int decayType2;
	int decayMode2 = 0;
	RMDataV* metMomentum = 0;
	RMSM2x2* metCovariance = 0;

	FastMttInputs() {};
	FastMttInputs(RMFLV const& leptonMomentum1,
		      classic_svFit::MeasuredTauLepton::kDecayType const& decayType1,
		      int const& decayMode1,
		      RMFLV const& leptonMomentum2,
		      classic_svFit::MeasuredTauLepton::kDecayType const& decayType2,
		      int const& decayMode2,
		      RMDataV const& metMomentum, RMSM2x2 const& metCovariance);
	~FastMttInputs();

	void Set(RMFLV const& leptonMomentum1,
		 classic_svFit::MeasuredTauLepton::kDecayType const& decayType1,
		 int const& decayMode1,
		 RMFLV const& leptonMomentum2,
		 classic_svFit::MeasuredTauLepton::kDecayType const& decayType2,
		 int const& decayMode2,
	         RMDataV const& metMomentum, RMSM2x2 const& metCovariance);

	bool operator==(FastMttInputs const& rhs) const;
	bool operator!=(FastMttInputs const& rhs) const;

	void Integrate(FastMTT& fastmtttAlgorithm) const;

private:
	std::vector<classic_svFit::MeasuredTauLepton> GetMeasuredTauLeptons() const;
	TMatrixD GetMetCovarianceMatrix() const;
};

/**
 */
class FastMttResults {

public:
	RMFLV* fittedHiggsLV = nullptr;
	float fittedTau1ERatio;
	RMFLV* fittedTau1LV = nullptr;
	float fittedTau2ERatio;
	RMFLV* fittedTau2LV = nullptr;

	FastMttResults() {};
	FastMttResults(RMFLV const& fittedHiggsLV, float fittedTau1ERatio, RMFLV const& fittedTau1LV, float fittedTau2ERatio, RMFLV const& fittedTau2LV);
	FastMttResults(FastMTT const& fastmttAlgorithm, float tau1Pt=-1, float tau2Pt=-1);
	~FastMttResults();

	void Set(RMFLV const& fittedHiggsLV, float fittedTau1ERatio, RMFLV const& fittedTau1LV, float fittedTau2ERatio, RMFLV const& fittedTau2LV);
	void Set(FastMTT const& fastmttAlgorithm, float tau1Pt=-1, float tau2Pt=-1);

	bool operator==(FastMttResults const& rhs) const;
	bool operator!=(FastMttResults const& rhs) const;

private:
	RMFLV GetFittedHiggsLV(FastMTT const& fastmttAlgorithm) const;
	RMFLV GetFittedTau1LV(FastMTT const& fastmttAlgorithm) const;
	RMFLV GetFittedTau2LV(FastMTT const& fastmttAlgorithm) const;
};

/**
 */
class FastMttTools {

public:
	FastMttTools();
	~FastMttTools();

	FastMttResults GetResults(FastMttInputs const& fastmttInputs);

private:
	FastMTT fastmttAlgorithm;

	//FastMttInputs fastmttInputs;
	FastMttResults fastmttResults;
};
