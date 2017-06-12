
#pragma once

#include "Artus/Utility/interface/ArtusLogging.h"

#include <map>

#include <TChain.h>
#include <TMemFile.h>

#include "TauAnalysis/ClassicSVfit/interface/ClassicSVfit.h"
#include "TauAnalysis/ClassicSVfit/interface/MeasuredTauLepton.h"
#include "TauAnalysis/ClassicSVfit/interface/svFitHistogramAdapter.h"

#include "Kappa/DataFormats/interface/Kappa.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttEnumTypes.h"


typedef ROOT::Math::DisplacementVector3D<ROOT::Math::Cartesian3D<float>,ROOT::Math::DefaultCoordinateSystemTag> RMDataV;
typedef ROOT::Math::SMatrix<double, 2, 2, ROOT::Math::MatRepSym<double, 2> > RMSM2x2;


class TauSVfitQuantity : public classic_svFit::SVfitQuantity
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
	virtual TH1* createHistogram(const classic_svFit::LorentzVector& vis1P4, const classic_svFit::LorentzVector& vis2P4, const classic_svFit::Vector& met) const;
	virtual double fitFunction(const classic_svFit::LorentzVector& tau1P4, const classic_svFit::LorentzVector& tau2P4, const classic_svFit::LorentzVector& vis1P4, const classic_svFit::LorentzVector& vis2P4, const classic_svFit::Vector& met) const;
};

class TauERatioSVfitQuantity : public TauSVfitQuantity
{
public:
	TauERatioSVfitQuantity(size_t tauIndex);
	virtual TH1* createHistogram(const classic_svFit::LorentzVector& vis1P4, const classic_svFit::LorentzVector& vis2P4, const classic_svFit::Vector& met) const;
	virtual double fitFunction(const classic_svFit::LorentzVector& tau1P4, const classic_svFit::LorentzVector& tau2P4, const classic_svFit::LorentzVector& vis1P4, const classic_svFit::LorentzVector& vis2P4, const classic_svFit::Vector& met) const;
};

class TauPtSVfitQuantity : public TauSVfitQuantity
{
public:
	TauPtSVfitQuantity(size_t tauIndex);
	virtual TH1* createHistogram(const classic_svFit::LorentzVector& vis1P4, const classic_svFit::LorentzVector& vis2P4, const classic_svFit::Vector& met) const;
	virtual double fitFunction(const classic_svFit::LorentzVector& tau1P4, const classic_svFit::LorentzVector& tau2P4, const classic_svFit::LorentzVector& vis1P4, const classic_svFit::LorentzVector& vis2P4, const classic_svFit::Vector& met) const;
};

class TauEtaSVfitQuantity : public TauSVfitQuantity
{
public:
	TauEtaSVfitQuantity(size_t tauIndex);
	virtual TH1* createHistogram(const classic_svFit::LorentzVector& vis1P4, const classic_svFit::LorentzVector& vis2P4, const classic_svFit::Vector& met) const;
	virtual double fitFunction(const classic_svFit::LorentzVector& tau1P4, const classic_svFit::LorentzVector& tau2P4, const classic_svFit::LorentzVector& vis1P4, const classic_svFit::LorentzVector& vis2P4, const classic_svFit::Vector& met) const;
};

class TauPhiSVfitQuantity : public TauSVfitQuantity
{
public:
	TauPhiSVfitQuantity(size_t tauIndex);
	virtual TH1* createHistogram(const classic_svFit::LorentzVector& vis1P4, const classic_svFit::LorentzVector& vis2P4, const classic_svFit::Vector& met) const;
	virtual double fitFunction(const classic_svFit::LorentzVector& tau1P4, const classic_svFit::LorentzVector& tau2P4, const classic_svFit::LorentzVector& vis1P4, const classic_svFit::LorentzVector& vis2P4, const classic_svFit::Vector& met) const;
};

class TauTauHistogramAdapter : public classic_svFit::DiTauSystemHistogramAdapter
{

public:
	TauTauHistogramAdapter(std::vector<classic_svFit::SVfitQuantity*> const& quantities = std::vector<classic_svFit::SVfitQuantity*>());

	RMFLV GetFittedHiggsLV() const;
	
	float GetFittedTau1ERatio() const;
	RMFLV GetFittedTau1LV() const;
	
	float GetFittedTau2ERatio() const;
	RMFLV GetFittedTau2LV() const;

private:
	unsigned int indexTau1ERatio = 0;
	unsigned int indexTau1Pt = 0;
	unsigned int indexTau1Eta = 0;
	unsigned int indexTau1Phi = 0;
	unsigned int indexTau2ERatio = 0;
	unsigned int indexTau2Pt = 0;
	unsigned int indexTau2Eta = 0;
	unsigned int indexTau2Phi = 0;
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
	float diTauMassConstraint;
	ULong64_t hash;
	
	SvfitEventKey() {};
	SvfitEventKey(ULong64_t const& runLumiEvent,
	              classic_svFit::MeasuredTauLepton::kDecayType const& decayType1, classic_svFit::MeasuredTauLepton::kDecayType const& decayType2,
	              HttEnumTypes::SystematicShift const& systematicShift,
	              float const& systematicShiftSigma, IntegrationMethod const& integrationMethod, float const& diTauMassConstraint, ULong64_t const &hash);
	
	void Set(ULong64_t const& runLumiEvent,
	         classic_svFit::MeasuredTauLepton::kDecayType const& decayType1, classic_svFit::MeasuredTauLepton::kDecayType const& decayType2,
	         HttEnumTypes::SystematicShift const& systematicShift,
	         float const& systematicShiftSigma, IntegrationMethod const& integrationMethod, float const& diTauMassConstraint, ULong64_t const &hash);
	
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
	
	void Integrate(SvfitEventKey const& svfitEventKey, ClassicSVfit& svfitAlgorithm) const;

private:
	std::vector<classic_svFit::MeasuredTauLepton> GetMeasuredTauLeptons(SvfitEventKey const& svfitEventKey) const;
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
	SvfitResults(ClassicSVfit const& svfitAlgorithm);
	~SvfitResults();
	
	void Set(double fittedTransverseMass, RMFLV const& fittedHiggsLV, float fittedTau1ERatio, RMFLV const& fittedTau1LV, float fittedTau2ERatio, RMFLV const& fittedTau2LV);
	void Set(ClassicSVfit const& svfitAlgorithm);
	inline void FromRecalculation() { recalculated = true; }
	inline void FromCache() { recalculated = false; }
	
	void CreateBranches(TTree* tree);
	void SetBranchAddresses(TTree* tree);
	void ActivateBranches(TTree* tree, bool activate=true);
	
	bool operator==(SvfitResults const& rhs) const;
	bool operator!=(SvfitResults const& rhs) const;
	
	bool recalculated;

private:
	double GetFittedTransverseMass(ClassicSVfit const& svfitAlgorithm) const;
	RMFLV GetFittedHiggsLV(ClassicSVfit const& svfitAlgorithm) const;
	float GetFittedTau1ERatio(ClassicSVfit const& svfitAlgorithm) const;
	RMFLV GetFittedTau1LV(ClassicSVfit const& svfitAlgorithm) const;
	float GetFittedTau2ERatio(ClassicSVfit const& svfitAlgorithm) const;
	RMFLV GetFittedTau2LV(ClassicSVfit const& svfitAlgorithm) const;
};


/**
 */
class SvfitTools {

public:
	SvfitTools();
	~SvfitTools();
	
	void Init(std::string const& cacheFileName, std::string const& cacheTreeName);
	SvfitResults GetResults(SvfitEventKey const& svfitEventKey, SvfitInputs const& svfitInputs,
	                        bool& neededRecalculation, HttEnumTypes::SvfitCacheMissBehaviour svfitCacheMissBehaviour, float const& svfitKappa=6.0);
	TFile * m_visPtResolutionFile = nullptr;

private:
	ClassicSVfit svfitAlgorithm;
	
	static std::map<std::string, TFile*> svfitCacheInputFiles;
	static std::map<std::string, TTree*> svfitCacheInputTrees;
	static std::map<std::string, std::map<SvfitEventKey, uint64_t> > svfitCacheInputTreeIndices;
	
	std::string cacheFileName;
	std::string cacheFileTreeName;
	
	SvfitEventKey svfitEventKey;
	SvfitInputs svfitInputs;
	SvfitResults svfitResults;
};

