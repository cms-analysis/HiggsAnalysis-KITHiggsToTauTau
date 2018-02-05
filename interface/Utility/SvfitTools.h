
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
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Utility/CPQuantities.h"


typedef ROOT::Math::DisplacementVector3D<ROOT::Math::Cartesian3D<float>,ROOT::Math::DefaultCoordinateSystemTag> RMDataV;
typedef ROOT::Math::SMatrix<double, 2, 2, ROOT::Math::MatRepSym<double, 2> > RMSM2x2;


class PhiCPSVfitQuantity : public classic_svFit::SVfitQuantity
{
public:
	virtual TH1* createHistogram(const classic_svFit::LorentzVector& vis1P4, const classic_svFit::LorentzVector& vis2P4, const classic_svFit::Vector& met) const;
	virtual double fitFunction(const classic_svFit::LorentzVector& tau1P4, const classic_svFit::LorentzVector& tau2P4, const classic_svFit::LorentzVector& vis1P4, const classic_svFit::LorentzVector& vis2P4, const classic_svFit::Vector& met) const;

private:
	mutable CPQuantities cpQuantities;
};

class PhiStarCPSVfitQuantity : public classic_svFit::SVfitQuantity
{
public:
	virtual TH1* createHistogram(const classic_svFit::LorentzVector& vis1P4, const classic_svFit::LorentzVector& vis2P4, const classic_svFit::Vector& met) const;
	virtual double fitFunction(const classic_svFit::LorentzVector& tau1P4, const classic_svFit::LorentzVector& tau2P4, const classic_svFit::LorentzVector& vis1P4, const classic_svFit::LorentzVector& vis2P4, const classic_svFit::Vector& met) const;

private:
	mutable CPQuantities cpQuantities;
};

class TauTauHistogramAdapter : public classic_svFit::TauTauHistogramAdapter
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
	unsigned int indexTau2ERatio = 0;
};

/**
 */
class SvfitEventKey {

public:

	ULong64_t runLumiEvent;
	int decayType1;
	int decayType2;
	int decayMode1 = 0;
	int decayMode2 = 0;
	int systematicShift;
	float systematicShiftSigma;
	float diTauMassConstraint;

	SvfitEventKey() {};
	SvfitEventKey(ULong64_t const& runLumiEvent,
	              classic_svFit::MeasuredTauLepton::kDecayType const& decayType1, classic_svFit::MeasuredTauLepton::kDecayType const& decayType2,
	              int const& decayMode1, int const& decayMode2,
	              HttEnumTypes::SystematicShift const& systematicShift, float const& systematicShiftSigma,
	              float const& diTauMassConstraint);

	void Set(ULong64_t const& runLumiEvent,
	         classic_svFit::MeasuredTauLepton::kDecayType const& decayType1, classic_svFit::MeasuredTauLepton::kDecayType const& decayType2,
	         int const& decayMode1, int const& decayMode2,
	         HttEnumTypes::SystematicShift const& systematicShift, float const& systematicShiftSigma,
	         float const& diTauMassConstraint);

	HttEnumTypes::SystematicShift GetSystematicShift() const;

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

	SvfitInputs() {};
	SvfitInputs(RMFLV const& leptonMomentum1, RMFLV const& leptonMomentum2,
	            RMDataV const& metMomentum, RMSM2x2 const& metCovariance);
	~SvfitInputs();

	void Set(RMFLV const& leptonMomentum1, RMFLV const& leptonMomentum2,
	         RMDataV const& metMomentum, RMSM2x2 const& metCovariance);

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
