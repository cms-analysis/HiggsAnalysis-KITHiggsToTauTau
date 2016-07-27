
#pragma once

#include "Artus/Utility/interface/ArtusLogging.h"

#include <map>

#include <TChain.h>
#include <TMemFile.h>

#include "TauAnalysis/SVfitStandalone/interface/SVfitStandaloneAlgorithm.h"

#include "Kappa/DataFormats/interface/Kappa.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttEnumTypes.h"


typedef ROOT::Math::DisplacementVector3D<ROOT::Math::Cartesian3D<float>,ROOT::Math::DefaultCoordinateSystemTag> RMDataV;
typedef ROOT::Math::SMatrix<double, 2, 2, ROOT::Math::MatRepSym<double, 2> > RMSM2x2;

/**
 */
class SvfitEventKey {

public:

	enum class IntegrationMethod : int
	{
		NONE = -1,
		MARKOV_CHAIN = 0,
		VEGAS = 1,
		FIT = 2,
	};
	static IntegrationMethod ToIntegrationMethod(std::string const& integrationMethod)
	{
		if (integrationMethod == "markovchain") return IntegrationMethod::MARKOV_CHAIN;
		else if (integrationMethod == "vegas") return IntegrationMethod::VEGAS;
		else if (integrationMethod == "fit") return IntegrationMethod::FIT;
		else return IntegrationMethod::NONE;
	}
	
	ULong64_t runLumiEvent;
	int decayType1;
	int decayType2;
	int systematicShift;
	float systematicShiftSigma;
	int integrationMethod;
	ULong64_t hash;
	
	SvfitEventKey() {};
	SvfitEventKey(ULong64_t const& runLumiEvent,
	              svFitStandalone::kDecayType const& decayType1, svFitStandalone::kDecayType const& decayType2,
	              HttEnumTypes::SystematicShift const& systematicShift,
	              float const& systematicShiftSigma, IntegrationMethod const& integrationMethod, ULong64_t const &hash);
	
	void Set(ULong64_t const& runLumiEvent,
	         svFitStandalone::kDecayType const& decayType1, svFitStandalone::kDecayType const& decayType2,
	         HttEnumTypes::SystematicShift const& systematicShift,
	         float const& systematicShiftSigma, IntegrationMethod const& integrationMethod, ULong64_t const &hash);
	
	HttEnumTypes::SystematicShift GetSystematicShift() const;
	IntegrationMethod GetIntegrationMethod() const;
	
	void CreateBranches(TTree* tree);
	void SetBranchAddresses(TTree* tree);
	void ActivateBranches(TTree* tree, bool activate=true);
	
	bool operator<(SvfitEventKey const& rhs) const;
	bool operator==(SvfitEventKey const& rhs) const;
	bool operator!=(SvfitEventKey const& rhs) const;
};

namespace std {
	string to_string(SvfitEventKey const& svfitEventKey);
}

std::ostream& operator<<(std::ostream& os, SvfitEventKey const& svfitEventKey);


/**
 */
class SvfitInputs {

public:
	RMFLV* leptonMomentum1 = 0;
	RMFLV* leptonMomentum2 = 0;
	
	RMDataV* metMomentum = 0;
	RMSM2x2* metCovariance = 0;

	int* decayMode1 = 0;
	int* decayMode2 = 0;
	
	SvfitInputs() {};
	SvfitInputs(RMFLV const& leptonMomentum1, RMFLV const& leptonMomentum2,
	            RMDataV const& metMomentum, RMSM2x2 const& metCovariance,
	            int const& decayMode1, int const& decayMode2);
	~SvfitInputs();
	
	void Set(RMFLV const& leptonMomentum1, RMFLV const& leptonMomentum2,
	         RMDataV const& metMomentum, RMSM2x2 const& metCovariance,
	         int const& decayMode1, int const& decayMode2);
	
	void CreateBranches(TTree* tree);
	void SetBranchAddresses(TTree* tree);
	void ActivateBranches(TTree* tree, bool activate=true);
	
	bool operator==(SvfitInputs const& rhs) const;
	bool operator!=(SvfitInputs const& rhs) const;
	
	SVfitStandaloneAlgorithm GetSvfitStandaloneAlgorithm(SvfitEventKey const& svfitEventKey, int verbosity=0, bool addLogM=false) const;

private:
	std::vector<svFitStandalone::MeasuredTauLepton> GetMeasuredTauLeptons(SvfitEventKey const& svfitEventKey) const;
	TMatrixD GetMetCovarianceMatrix() const;
};


/**
 */
class SvfitResults {

public:
	RMFLV* momentum = 0;
	RMFLV* momentumUncertainty = 0;
	RMDataV* fittedMET = 0;
	double*  transverseMass = 0;
	double*  transverseMassUnc = 0;
	
	SvfitResults() {};
	SvfitResults(RMFLV const& momentum, RMFLV const& momentumUncertainty, RMDataV const& fittedMET, std::pair<double, double> transverseMass);
	SvfitResults(SVfitStandaloneAlgorithm const& svfitStandaloneAlgorithm);
	~SvfitResults();
	
	void Set(RMFLV const& momentum, RMFLV const& momentumUncertainty, RMDataV const& fittedMET, std::pair<double, double> transverseMass);
	void Set(SVfitStandaloneAlgorithm const& svfitStandaloneAlgorithm);
	void fromRecalculation(){ recalculated = true; }
	void fromCache(){ recalculated = false; }
	
	void CreateBranches(TTree* tree);
	void SetBranchAddresses(TTree* tree);
	void ActivateBranches(TTree* tree, bool activate=true);
	
	bool operator==(SvfitResults const& rhs) const;
	bool operator!=(SvfitResults const& rhs) const;
	
	bool recalculated;

private:
	RMFLV GetMomentum(SVfitStandaloneAlgorithm const& svfitStandaloneAlgorithm) const;
	RMFLV GetMomentumUncertainty(SVfitStandaloneAlgorithm const& svfitStandaloneAlgorithm) const;
	RMDataV GetFittedMET(SVfitStandaloneAlgorithm const& svfitStandaloneAlgorithm) const;
	std::pair<double, double> GetFittedTransverseMass(SVfitStandaloneAlgorithm const& svfitStandaloneAlgorithm) const;
};


/**
 */
class SvfitTools {

public:
	SvfitTools() {}
	SvfitTools(std::vector<std::string> const& fileNames, std::string const& treeName);
	
	void Init(std::vector<std::string> const& fileNames, std::string const& treeName);
	SvfitResults GetResults(SvfitEventKey const& svfitEventKey, SvfitInputs const& svfitInputs,
	                        bool& neededRecalculation, HttEnumTypes::SvfitCacheMissBehaviour svfitCacheMissBehaviour);

private:
	TChain* svfitCacheInputTree;
	std::map<SvfitEventKey, uint64_t> svfitCacheInputTreeIndices;
	
	SvfitInputs svfitInputs;
	SvfitResults svfitResults;
	SvfitEventKey svfitEventKey;
	TFile * m_inputFile_visPtResolution = 0;
};

