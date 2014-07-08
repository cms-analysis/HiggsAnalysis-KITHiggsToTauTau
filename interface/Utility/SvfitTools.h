
#pragma once

#include "Artus/Utility/interface/ArtusLogging.h"

#include <unordered_map>

#include <TChain.h>

#include "TauAnalysis/SVfitStandalone/interface/SVfitStandaloneAlgorithm.h"

#include "Kappa/DataFormats/interface/Kappa.h"


typedef ROOT::Math::DisplacementVector3D<ROOT::Math::Cartesian3D<float>,ROOT::Math::DefaultCoordinateSystemTag> RMDataV;
typedef ROOT::Math::SMatrix<double, 2, 2, ROOT::Math::MatRepSym<double, 2> > RMSM2x2;

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
	void ActivateBranches(TTree* tree, bool activate=true);
	
	bool operator==(RunLumiEvent const& rhs) const;
	bool operator!=(RunLumiEvent const& rhs) const;
};

/** Hashing function for RunLumiEvent. This is needed when RunLumiEvent is used
 *  as key type of a std::unordered_map.
 */
namespace std {
	template<>
	struct hash<RunLumiEvent>
	{
		std::size_t operator()(RunLumiEvent const& runLumiEvent) const
		{
			// Compute individual hash values for int members and
			// combine them using XOR and bit shifting
			return ((std::hash<int>()(runLumiEvent.run) ^
					(std::hash<int>()(runLumiEvent.lumi) << 1)) >> 1) ^
				    (std::hash<int>()(runLumiEvent.event) << 1);
		}
	};
}


/**
 */
class SvfitInputs {

public:
	int decayType1;
	int decayType2;
	
	RMDataLV* leptonMomentum1 = 0;
	RMDataLV* leptonMomentum2 = 0;
	
	RMDataV* metMomentum = 0;
	RMSM2x2* metCovariance = 0;
	
	SvfitInputs();
	SvfitInputs(svFitStandalone::kDecayType const& decayType1, svFitStandalone::kDecayType const& decayType2,
	            RMDataLV const& leptonMomentum1, RMDataLV const& leptonMomentum2,
	            RMDataV const& metMomentum, RMSM2x2 const& metCovariance);
	
	void Set(svFitStandalone::kDecayType const& decayType1, svFitStandalone::kDecayType const& decayType2,
	         RMDataLV const& leptonMomentum1, RMDataLV const& leptonMomentum2,
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
	
	int integrationMethod;
	RMDataLV* momentum = 0;
	RMDataLV* momentumUncertainty = 0;
	
	SvfitResults();
	SvfitResults(IntegrationMethod const& integrationMethod,
	             RMDataLV const& momentum, RMDataLV const& momentumUncertainty);
	SvfitResults(IntegrationMethod const& integrationMethod,
	             SVfitStandaloneAlgorithm const& svfitStandaloneAlgorithm);
	
	void Set(IntegrationMethod const& integrationMethod,
	         RMDataLV const& momentum, RMDataLV const& momentumUncertainty);
	void Set(IntegrationMethod const& integrationMethod,
	         SVfitStandaloneAlgorithm const& svfitStandaloneAlgorithm);
	
	void CreateBranches(TTree* tree);
	void SetBranchAddresses(TTree* tree);
	void ActivateBranches(TTree* tree, bool activate=true);
	
	bool operator==(SvfitResults const& rhs) const;
	bool operator!=(SvfitResults const& rhs) const;


private:
	RMDataLV GetMomentum(SVfitStandaloneAlgorithm const& svfitStandaloneAlgorithm) const;
	RMDataLV GetMomentumUncertainty(SVfitStandaloneAlgorithm const& svfitStandaloneAlgorithm) const;
};


/**
 */
class SvfitTools {

public:
	SvfitTools() {}
	SvfitTools(std::vector<std::string> const& fileNames, std::string const& treeName);
	
	void Init(std::vector<std::string> const& fileNames, std::string const& treeName);
	SvfitResults GetResults(RunLumiEvent const& runLumiEvent, SvfitInputs const& svfitInputs,
	                        SvfitResults::IntegrationMethod const& integrationMethod,
	                        bool& neededRecalculation);

private:
	TChain* svfitCacheInputTree = 0;
	std::unordered_map<RunLumiEvent, int> svfitCacheInputTreeIndices;
	
	SvfitInputs svfitInputs;
	SvfitResults svfitResults;
};

