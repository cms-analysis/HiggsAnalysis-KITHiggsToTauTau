
#pragma once

#include "Artus/Utility/interface/ArtusLogging.h"

#include <unordered_map>

#include <TChain.h>

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
	};
	static IntegrationMethod ToIntegrationMethod(std::string const& integrationMethod)
	{
		if (integrationMethod == "markovchain") return IntegrationMethod::MARKOV_CHAIN;
		else if (integrationMethod == "vegas") return IntegrationMethod::VEGAS;
		else return IntegrationMethod::NONE;
	}
	
	int run;
	int lumi;
	int event;
	int systematicShift;
	float systematicShiftSigma;
	int integrationMethod;
	
	SvfitEventKey() {};
	SvfitEventKey(int const& run, int const& lumi, int const& event,
	              HttEnumTypes::SystematicShift const& systematicShift, float const& systematicShiftSigma,
	              IntegrationMethod const& integrationMethod);
	
	void Set(int const& run, int const& lumi, int const& event,
	         HttEnumTypes::SystematicShift const& systematicShift, float const& systematicShiftSigma,
	         IntegrationMethod const& integrationMethod);
	
	HttEnumTypes::SystematicShift GetSystematicShift() const;
	IntegrationMethod GetIntegrationMethod() const;
	
	void CreateBranches(TTree* tree);
	void SetBranchAddresses(TTree* tree);
	void ActivateBranches(TTree* tree, bool activate=true);
	
	bool operator==(SvfitEventKey const& rhs) const;
	bool operator!=(SvfitEventKey const& rhs) const;
};

/** Hashing function for SvfitEventKey. This is needed when SvfitEventKey is used
 *  as key type of a std::unordered_map.
 */
namespace std {
	template<>
	struct hash<SvfitEventKey>
	{
		std::size_t operator()(SvfitEventKey const& svfitEventKey) const
		{
			return ((std::hash<int>()(svfitEventKey.run)) ^
			        (std::hash<int>()(svfitEventKey.lumi)) ^
			        (std::hash<int>()(svfitEventKey.event)) ^
			        (std::hash<int>()(svfitEventKey.systematicShift)) ^
			        (std::hash<float>()(svfitEventKey.systematicShiftSigma)) ^
			        (std::hash<int>()(svfitEventKey.integrationMethod)));
		}
	};
	
	string to_string(SvfitEventKey const& svfitEventKey);
}

std::ostream& operator<<(std::ostream& os, SvfitEventKey const& svfitEventKey);


/**
 */
class SvfitInputs {

public:
	int decayType1;
	int decayType2;
	
	RMFLV* leptonMomentum1 = 0;
	RMFLV* leptonMomentum2 = 0;
	
	RMDataV* metMomentum = 0;
	RMSM2x2* metCovariance = 0;
	
	SvfitInputs() {};
	SvfitInputs(svFitStandalone::kDecayType const& decayType1, svFitStandalone::kDecayType const& decayType2,
	            RMFLV const& leptonMomentum1, RMFLV const& leptonMomentum2,
	            RMDataV const& metMomentum, RMSM2x2 const& metCovariance);
	~SvfitInputs();
	
	void Set(svFitStandalone::kDecayType const& decayType1, svFitStandalone::kDecayType const& decayType2,
	         RMFLV const& leptonMomentum1, RMFLV const& leptonMomentum2,
	         RMDataV const& metMomentum, RMSM2x2 const& metCovariance);
	
	void CreateBranches(TTree* tree);
	void SetBranchAddresses(TTree* tree);
	void ActivateBranches(TTree* tree, bool activate=true);
	
	bool operator==(SvfitInputs const& rhs) const;
	bool operator!=(SvfitInputs const& rhs) const;
	
	SVfitStandaloneAlgorithm GetSvfitStandaloneAlgorithm(int verbosity=0, bool addLogM=false) const;

	
private:
	std::vector<svFitStandalone::MeasuredTauLepton> GetMeasuredTauLeptons() const;
	TMatrixD GetMetCovarianceMatrix() const;
};


/**
 */
class SvfitResults {

public:
	RMFLV* momentum = 0;
	RMFLV* momentumUncertainty = 0;
	
	SvfitResults() {};
	SvfitResults(RMFLV const& momentum, RMFLV const& momentumUncertainty);
	SvfitResults(SVfitStandaloneAlgorithm const& svfitStandaloneAlgorithm);
	~SvfitResults();
	
	void Set(RMFLV const& momentum, RMFLV const& momentumUncertainty);
	void Set(SVfitStandaloneAlgorithm const& svfitStandaloneAlgorithm);
	
	void CreateBranches(TTree* tree);
	void SetBranchAddresses(TTree* tree);
	void ActivateBranches(TTree* tree, bool activate=true);
	
	bool operator==(SvfitResults const& rhs) const;
	bool operator!=(SvfitResults const& rhs) const;


private:
	RMFLV GetMomentum(SVfitStandaloneAlgorithm const& svfitStandaloneAlgorithm) const;
	RMFLV GetMomentumUncertainty(SVfitStandaloneAlgorithm const& svfitStandaloneAlgorithm) const;
};


/**
 */
class SvfitTools {

public:
	SvfitTools() {}
	SvfitTools(std::vector<std::string> const& fileNames, std::string const& treeName);
	
	void Init(std::vector<std::string> const& fileNames, std::string const& treeName);
	SvfitResults GetResults(SvfitEventKey const& svfitEventKey, SvfitInputs const& svfitInputs,
	                        bool& neededRecalculation);

private:
	TChain* svfitCacheInputTree = 0;
	std::unordered_map<SvfitEventKey, int> svfitCacheInputTreeIndices;
	
	SvfitInputs svfitInputs;
	SvfitResults svfitResults;
};

