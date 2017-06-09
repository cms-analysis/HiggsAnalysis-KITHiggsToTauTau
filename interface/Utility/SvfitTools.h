
#pragma once

#include "Artus/Utility/interface/ArtusLogging.h"

#include <map>

#include <TChain.h>
#include <TMemFile.h>

#include "TauAnalysis/SVfitStandalone/interface/SVfitStandaloneAlgorithm.h"
#include "TauAnalysis/SVfitStandalone/interface/SVfitStandaloneQuantities.h"

#include "Kappa/DataFormats/interface/Kappa.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttEnumTypes.h"


typedef ROOT::Math::DisplacementVector3D<ROOT::Math::Cartesian3D<float>,ROOT::Math::DefaultCoordinateSystemTag> RMDataV;
typedef ROOT::Math::SMatrix<double, 2, 2, ROOT::Math::MatRepSym<double, 2> > RMSM2x2;


class TauSVfitQuantity : public svFitStandalone::SVfitQuantity
{

public:
	TauSVfitQuantity(size_t tauIndex);

protected:
	size_t m_tauIndex;
	std::string m_tauLabel;
};

class TauESVfitQuantity : public TauSVfitQuantity
{
public:
	TauESVfitQuantity(size_t tauIndex);
	virtual TH1* CreateHistogram(std::vector<svFitStandalone::LorentzVector> const& measuredTauLeptons, svFitStandalone::Vector const& measuredMET) const;
	virtual double FitFunction(std::vector<svFitStandalone::LorentzVector> const& fittedTauLeptons, std::vector<svFitStandalone::LorentzVector> const& measuredTauLeptons, svFitStandalone::Vector const& measuredMET) const;
};

class TauERatioSVfitQuantity : public TauSVfitQuantity
{
public:
	TauERatioSVfitQuantity(size_t tauIndex);
	virtual TH1* CreateHistogram(std::vector<svFitStandalone::LorentzVector> const& measuredTauLeptons, svFitStandalone::Vector const& measuredMET) const;
	virtual double FitFunction(std::vector<svFitStandalone::LorentzVector> const& fittedTauLeptons, std::vector<svFitStandalone::LorentzVector> const& measuredTauLeptons, svFitStandalone::Vector const& measuredMET) const;
};

class TauPtSVfitQuantity : public TauSVfitQuantity
{
public:
	TauPtSVfitQuantity(size_t tauIndex);
	virtual TH1* CreateHistogram(std::vector<svFitStandalone::LorentzVector> const& measuredTauLeptons, svFitStandalone::Vector const& measuredMET) const;
	virtual double FitFunction(std::vector<svFitStandalone::LorentzVector> const& fittedTauLeptons, std::vector<svFitStandalone::LorentzVector> const& measuredTauLeptons, svFitStandalone::Vector const& measuredMET) const;
};

class TauEtaSVfitQuantity : public TauSVfitQuantity
{
public:
	TauEtaSVfitQuantity(size_t tauIndex);
	virtual TH1* CreateHistogram(std::vector<svFitStandalone::LorentzVector> const& measuredTauLeptons, svFitStandalone::Vector const& measuredMET) const;
	virtual double FitFunction(std::vector<svFitStandalone::LorentzVector> const& fittedTauLeptons, std::vector<svFitStandalone::LorentzVector> const& measuredTauLeptons, svFitStandalone::Vector const& measuredMET) const;
};

class TauPhiSVfitQuantity : public TauSVfitQuantity
{
public:
	TauPhiSVfitQuantity(size_t tauIndex);
	virtual TH1* CreateHistogram(std::vector<svFitStandalone::LorentzVector> const& measuredTauLeptons, svFitStandalone::Vector const& measuredMET) const;
	virtual double FitFunction(std::vector<svFitStandalone::LorentzVector> const& fittedTauLeptons, std::vector<svFitStandalone::LorentzVector> const& measuredTauLeptons, svFitStandalone::Vector const& measuredMET) const;
};

class MCTauTauQuantitiesAdapter : public svFitStandalone::MCPtEtaPhiMassAdapter
{

public:
	MCTauTauQuantitiesAdapter();

	RMFLV GetFittedHiggsLV() const;
	
	float GetFittedTau1ERatio() const;
	RMFLV GetFittedTau1LV() const;
	
	float GetFittedTau2ERatio() const;
	RMFLV GetFittedTau2LV() const;
};

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

	int decayMode1 = 0;
	int decayMode2 = 0;
	
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
	
	SVfitStandaloneAlgorithm GetSvfitStandaloneAlgorithm(SvfitEventKey const& svfitEventKey, int verbosity, bool addLogM, TFile* &visPtResolutionFile) const;

private:
	std::vector<svFitStandalone::MeasuredTauLepton> GetMeasuredTauLeptons(SvfitEventKey const& svfitEventKey) const;
	TMatrixD GetMetCovarianceMatrix() const;
};


/**
 */
class SvfitResults {

public:
	double fittedTransverseMass;
	RMFLV* fittedHiggsLV = nullptr;
	float fittedTau1ERatio;
	RMFLV* fittedTau1LV = nullptr;
	float fittedTau2ERatio;
	RMFLV* fittedTau2LV = nullptr;
	
	SvfitResults() {};
	SvfitResults(double fittedTransverseMass, RMFLV const& fittedHiggsLV, float fittedTau1ERatio, RMFLV const& fittedTau1LV, float fittedTau2ERatio, RMFLV const& fittedTau2LV);
	SvfitResults(SVfitStandaloneAlgorithm const& svfitStandaloneAlgorithm);
	~SvfitResults();
	
	void Set(double fittedTransverseMass, RMFLV const& fittedHiggsLV, float fittedTau1ERatio, RMFLV const& fittedTau1LV, float fittedTau2ERatio, RMFLV const& fittedTau2LV);
	void Set(SVfitStandaloneAlgorithm const& svfitStandaloneAlgorithm);
	inline void FromRecalculation() { recalculated = true; }
	inline void FromCache() { recalculated = false; }
	
	void CreateBranches(TTree* tree);
	void SetBranchAddresses(TTree* tree);
	void ActivateBranches(TTree* tree, bool activate=true);
	
	bool operator==(SvfitResults const& rhs) const;
	bool operator!=(SvfitResults const& rhs) const;
	
	bool recalculated;

private:
	double GetFittedTransverseMass(SVfitStandaloneAlgorithm const& svfitStandaloneAlgorithm) const;
	RMFLV GetFittedHiggsLV(SVfitStandaloneAlgorithm const& svfitStandaloneAlgorithm) const;
	float GetFittedTau1ERatio(SVfitStandaloneAlgorithm const& svfitStandaloneAlgorithm) const;
	RMFLV GetFittedTau1LV(SVfitStandaloneAlgorithm const& svfitStandaloneAlgorithm) const;
	float GetFittedTau2ERatio(SVfitStandaloneAlgorithm const& svfitStandaloneAlgorithm) const;
	RMFLV GetFittedTau2LV(SVfitStandaloneAlgorithm const& svfitStandaloneAlgorithm) const;
};


/**
 */
class SvfitTools {

public:
	SvfitTools() {}
	~SvfitTools();
	
	void Init(std::string const& cacheFileName, std::string const& cacheTreeName);
	SvfitResults GetResults(SvfitEventKey const& svfitEventKey, SvfitInputs const& svfitInputs,
	                        bool& neededRecalculation, HttEnumTypes::SvfitCacheMissBehaviour svfitCacheMissBehaviour);
	TFile * m_visPtResolutionFile = nullptr;

private:
	static std::map<std::string, TTree*> svfitCacheInputTree;
	static std::map<std::string, TFile*> svfitCacheInputFile;
	static std::map<std::string, std::map<SvfitEventKey, uint64_t>> svfitCacheInputTreeIndices;
	std::string cacheFileName;
	SvfitInputs svfitInputs;
	static std::map<std::string, SvfitResults> svfitResults;
	SvfitEventKey svfitEventKey;
};

