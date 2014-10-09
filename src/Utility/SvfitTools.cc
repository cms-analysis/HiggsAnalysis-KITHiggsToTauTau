
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Utility/SvfitTools.h"

#include "Artus/Utility/interface/Utility.h"


SvfitEventKey::SvfitEventKey(int const& run, int const& lumi, int const& event,
                             HttEnumTypes::SystematicShift const& systematicShift, float const& systematicShiftSigma,
                             IntegrationMethod const& integrationMethod)
{
	Set(run, lumi, event, systematicShift, systematicShiftSigma, integrationMethod);
}

void SvfitEventKey::Set(int const& run, int const& lumi, int const& event,
                        HttEnumTypes::SystematicShift const& systematicShift, float const& systematicShiftSigma,
                        IntegrationMethod const& integrationMethod)
{
	this->run = run;
	this->lumi = lumi;
	this->event = event;
	this->systematicShift = Utility::ToUnderlyingValue<HttEnumTypes::SystematicShift>(systematicShift);
	this->systematicShiftSigma = systematicShiftSigma;
	this->integrationMethod = Utility::ToUnderlyingValue<IntegrationMethod>(integrationMethod);
}

HttEnumTypes::SystematicShift SvfitEventKey::GetSystematicShift() const
{
	return Utility::ToEnum<HttEnumTypes::SystematicShift>(systematicShift);
}

SvfitEventKey::IntegrationMethod SvfitEventKey::GetIntegrationMethod() const
{
	return Utility::ToEnum<IntegrationMethod>(integrationMethod);
}

void SvfitEventKey::CreateBranches(TTree* tree)
{
	tree->Branch("run", &run);
	tree->Branch("lumi", &lumi);
	tree->Branch("event", &event);
	tree->Branch("systematicShift", &systematicShift);
	tree->Branch("systematicShiftSigma", &systematicShiftSigma);
	tree->Branch("integrationMethod", &integrationMethod);
}

void SvfitEventKey::SetBranchAddresses(TTree* tree)
{
	tree->SetBranchAddress("run", &run);
	tree->SetBranchAddress("lumi", &lumi);
	tree->SetBranchAddress("event", &event);
	tree->SetBranchAddress("systematicShift", &systematicShift);
	tree->SetBranchAddress("systematicShiftSigma", &systematicShiftSigma);
	tree->SetBranchAddress("integrationMethod", &integrationMethod);
	ActivateBranches(tree, true);
}

void SvfitEventKey::ActivateBranches(TTree* tree, bool activate)
{
	tree->SetBranchStatus("run", activate);
	tree->SetBranchStatus("lumi", activate);
	tree->SetBranchStatus("event", activate);
	tree->SetBranchStatus("systematicShift", activate);
	tree->SetBranchStatus("systematicShiftSigma", activate);
	tree->SetBranchStatus("integrationMethod", activate);
}

bool SvfitEventKey::operator==(SvfitEventKey const& rhs) const
{
	return ((run == rhs.run) && (lumi == rhs.lumi) && (event == rhs.event) &&
	        (systematicShift == rhs.systematicShift) && (systematicShiftSigma == rhs.systematicShiftSigma) &&
	        (integrationMethod == rhs.integrationMethod));
}

bool SvfitEventKey::operator!=(SvfitEventKey const& rhs) const
{
	return (! (*this == rhs));
}

std::string std::to_string(SvfitEventKey const& svfitEventKey)
{
	return std::string("SvfitEventKey(") +
			"run=" + std::to_string(svfitEventKey.run) + ", " +
			"lumi=" + std::to_string(svfitEventKey.lumi) + ", " +
			"event=" + std::to_string(svfitEventKey.event) + ", " +
			"systematicShift=" + std::to_string(svfitEventKey.systematicShift) + ", " +
			"systematicShiftSigma=" + std::to_string(svfitEventKey.systematicShiftSigma) + ", " +
			"integrationMethod=" + std::to_string(svfitEventKey.integrationMethod) + ")";
}

std::ostream& operator<<(std::ostream& os, SvfitEventKey const& svfitEventKey)
{
	return os << std::to_string(svfitEventKey);
}

SvfitInputs::SvfitInputs(svFitStandalone::kDecayType const& decayType1, svFitStandalone::kDecayType const& decayType2,
                         RMDataLV const& leptonMomentum1, RMDataLV const& leptonMomentum2,
                         RMDataV const& metMomentum, RMSM2x2 const& metCovariance)
	: SvfitInputs()
{
	Set(decayType1, decayType2, leptonMomentum1, leptonMomentum2, metMomentum, metCovariance);
}

void SvfitInputs::Set(svFitStandalone::kDecayType const& decayType1, svFitStandalone::kDecayType const& decayType2,
                      RMDataLV const& leptonMomentum1, RMDataLV const& leptonMomentum2,
                      RMDataV const& metMomentum, RMSM2x2 const& metCovariance)
{
	this->decayType1 = Utility::ToUnderlyingValue(decayType1);
	this->decayType2 = Utility::ToUnderlyingValue(decayType2);
	this->leptonMomentum1 = leptonMomentum1;
	this->leptonMomentum2 = leptonMomentum2;
	this->metMomentum = metMomentum;
	this->metCovariance = metCovariance;
}

void SvfitInputs::CreateBranches(TTree* tree)
{
	tree->Branch("decayType1", &decayType1);
	tree->Branch("decayType2", &decayType2);
	tree->Branch("leptonMomentum1", "RMDataLV", &leptonMomentum1);
	tree->Branch("leptonMomentum2", "RMDataLV", &leptonMomentum2);
	tree->Branch("metMomentum", "ROOT::Math::DisplacementVector3D<ROOT::Math::Cartesian3D<float>,ROOT::Math::DefaultCoordinateSystemTag>", &metMomentum);
	tree->Branch("metCovariance", "ROOT::Math::SMatrix<double, 2, 2, ROOT::Math::MatRepSym<double, 2> >", &metCovariance);
}

void SvfitInputs::SetBranchAddresses(TTree* tree)
{
	tree->SetBranchAddress("decayType1", &decayType1);
	tree->SetBranchAddress("decayType2", &decayType2);
	tree->SetBranchAddress("leptonMomentum1", &leptonMomentum1);
	tree->SetBranchAddress("leptonMomentum2", &leptonMomentum2);
	tree->SetBranchAddress("metMomentum", &metMomentum);
	tree->SetBranchAddress("metCovariance", &metCovariance);
	ActivateBranches(tree, true);
}

void SvfitInputs::ActivateBranches(TTree* tree, bool activate)
{
	tree->SetBranchStatus("decayType1", activate);
	tree->SetBranchStatus("decayType2", activate);
	tree->SetBranchStatus("leptonMomentum1", activate);
	tree->SetBranchStatus("leptonMomentum2", activate);
	tree->SetBranchStatus("metMomentum", activate);
	tree->SetBranchStatus("metCovariance", activate);
}

bool SvfitInputs::operator==(SvfitInputs const& rhs) const
{
	return ((decayType1 == rhs.decayType1) &&
	        (decayType2 == rhs.decayType2) &&
	        Utility::ApproxEqual(leptonMomentum1, rhs.leptonMomentum1) &&
	        Utility::ApproxEqual(leptonMomentum2, rhs.leptonMomentum2) &&
	        Utility::ApproxEqual(metMomentum, rhs.metMomentum) &&
	        Utility::ApproxEqual(metCovariance, rhs.metCovariance));
}

bool SvfitInputs::operator!=(SvfitInputs const& rhs) const
{
	return (! (*this == rhs));
}

SVfitStandaloneAlgorithm SvfitInputs::GetSvfitStandaloneAlgorithm(int verbosity, bool addLogM) const
{
	SVfitStandaloneAlgorithm svfitStandaloneAlgorithm = SVfitStandaloneAlgorithm(GetMeasuredTauLeptons(),
	                                                                             svFitStandalone::Vector(metMomentum),
	                                                                             GetMetCovarianceMatrix(),
	                                                                             verbosity);
	svfitStandaloneAlgorithm.addLogM(addLogM);
	return svfitStandaloneAlgorithm;
}

std::vector<svFitStandalone::MeasuredTauLepton> SvfitInputs::GetMeasuredTauLeptons() const
{
	std::vector<svFitStandalone::MeasuredTauLepton> measuredTauLeptons {
		svFitStandalone::MeasuredTauLepton(Utility::ToEnum<svFitStandalone::kDecayType>(decayType1), svFitStandalone::LorentzVector(leptonMomentum1)),
		svFitStandalone::MeasuredTauLepton(Utility::ToEnum<svFitStandalone::kDecayType>(decayType2), svFitStandalone::LorentzVector(leptonMomentum2))
	};
	return measuredTauLeptons;
}

TMatrixD SvfitInputs::GetMetCovarianceMatrix() const
{
	TMatrixD metCovarianceMatrix(2, 2);
	metCovarianceMatrix[0][0] = metCovariance.At(0, 0);
	metCovarianceMatrix[1][0] = metCovariance.At(1, 0);
	metCovarianceMatrix[0][1] = metCovariance.At(0, 1);
	metCovarianceMatrix[1][1] = metCovariance.At(1, 1);
	return metCovarianceMatrix;
}

SvfitResults::SvfitResults(RMDataLV const& momentum, RMDataLV const& momentumUncertainty) :
	SvfitResults()
{
	Set(momentum, momentumUncertainty);
}

SvfitResults::SvfitResults(SVfitStandaloneAlgorithm const& svfitStandaloneAlgorithm) :
	SvfitResults()
{
	Set(svfitStandaloneAlgorithm);
}

void SvfitResults::Set(RMDataLV const& momentum, RMDataLV const& momentumUncertainty)
{
	this->momentum = momentum;
	this->momentumUncertainty = momentumUncertainty;
}

void SvfitResults::Set(SVfitStandaloneAlgorithm const& svfitStandaloneAlgorithm)
{
	Set(GetMomentum(svfitStandaloneAlgorithm),
	    GetMomentumUncertainty(svfitStandaloneAlgorithm));
}

void SvfitResults::CreateBranches(TTree* tree)
{
	tree->Branch("svfitMomentum", "RMDataLV", &momentum);
	tree->Branch("svfitMomentumUncertainty", "RMDataLV", &momentumUncertainty);
}

void SvfitResults::SetBranchAddresses(TTree* tree)
{
	tree->SetBranchAddress("svfitMomentum", &momentum);
	tree->SetBranchAddress("svfitMomentumUncertainty", &momentumUncertainty);
	ActivateBranches(tree, true);
}

void SvfitResults::ActivateBranches(TTree* tree, bool activate)
{
	tree->SetBranchStatus("svfitMomentum", activate);
	tree->SetBranchStatus("svfitMomentumUncertainty", activate);
}

bool SvfitResults::operator==(SvfitResults const& rhs) const
{
	return (Utility::ApproxEqual(momentum, rhs.momentum) &&
	        Utility::ApproxEqual(momentumUncertainty, rhs.momentumUncertainty));
}

bool SvfitResults::operator!=(SvfitResults const& rhs) const
{
	return (! (*this == rhs));
}

RMDataLV SvfitResults::GetMomentum(SVfitStandaloneAlgorithm const& svfitStandaloneAlgorithm) const
{
	RMDataLV momentum;
	momentum.SetPt(svfitStandaloneAlgorithm.pt());
	momentum.SetEta(svfitStandaloneAlgorithm.eta());
	momentum.SetPhi(svfitStandaloneAlgorithm.phi());
	momentum.SetM(svfitStandaloneAlgorithm.mass());
	return momentum;
}

RMDataLV SvfitResults::GetMomentumUncertainty(SVfitStandaloneAlgorithm const& svfitStandaloneAlgorithm) const
{
	RMDataLV momentumUncertainty;
	momentumUncertainty.SetPt(svfitStandaloneAlgorithm.ptUncert());
	momentumUncertainty.SetEta(svfitStandaloneAlgorithm.etaUncert());
	momentumUncertainty.SetPhi(svfitStandaloneAlgorithm.phiUncert());
	momentumUncertainty.SetM(svfitStandaloneAlgorithm.massUncert());
	return momentumUncertainty;
}

SvfitTools::SvfitTools(std::vector<std::string> const& fileNames, std::string const& treeName)
{
	Init(fileNames, treeName);
}

void SvfitTools::Init(std::vector<std::string> const& fileNames, std::string const& treeName)
{
	if ((! svfitCacheInputTree) && svfitCacheInputTreeIndices.empty())
	{
		LOG(DEBUG) << "\tLoading SVfit cache trees from files...";
		svfitCacheInputTree = new TChain(treeName.c_str());
		for (std::vector<std::string>::const_iterator fileName = fileNames.begin();
		     fileName != fileNames.end(); ++fileName)
		{
			LOG(DEBUG) << "\t\t" << *fileName << "/" << treeName;
			svfitCacheInputTree->Add(fileName->c_str());
		}
		
		SvfitEventKey svfitEventKey;
		svfitEventKey.SetBranchAddresses(svfitCacheInputTree);
		for (int svfitCacheInputTreeIndex = 0;
		     svfitCacheInputTreeIndex < svfitCacheInputTree->GetEntries();
		     ++svfitCacheInputTreeIndex)
		{
			svfitCacheInputTree->GetEntry(svfitCacheInputTreeIndex);
			svfitCacheInputTreeIndices[svfitEventKey] = svfitCacheInputTreeIndex;
			//LOG(DEBUG) << std::to_string(svfitEventKey) << " --> " << svfitCacheInputTreeIndex;
			//LOG(DEBUG) << svfitEventKey << " --> " << svfitCacheInputTreeIndex;
		}
		svfitEventKey.ActivateBranches(svfitCacheInputTree, false);
		LOG(DEBUG) << "\t\t" << svfitCacheInputTreeIndices.size() << " entries found.";
		
		svfitInputs.SetBranchAddresses(svfitCacheInputTree);
		svfitResults.SetBranchAddresses(svfitCacheInputTree);
	}
}

SvfitResults SvfitTools::GetResults(SvfitEventKey const& svfitEventKey,
                                    SvfitInputs const& svfitInputs,
                                    bool& neededRecalculation)
{
	neededRecalculation = false;
	
	auto svfitCacheInputTreeIndicesItem = svfitCacheInputTreeIndices.find(svfitEventKey);
	if (svfitCacheInputTreeIndicesItem == svfitCacheInputTreeIndices.end())
	{
		neededRecalculation = true;
	}
	else
	{
		svfitCacheInputTree->GetEntry(svfitCacheInputTreeIndicesItem->second);
		
		if (this->svfitInputs != svfitInputs)
		{
			neededRecalculation = true;
		}
		else
		{
			return svfitResults;
		}
	}
	
	if (neededRecalculation)
	{
		// construct algorithm
		SVfitStandaloneAlgorithm svfitStandaloneAlgorithm = svfitInputs.GetSvfitStandaloneAlgorithm();
	
		// execute integration
		if (svfitEventKey.GetIntegrationMethod() == SvfitEventKey::IntegrationMethod::VEGAS)
		{
			svfitStandaloneAlgorithm.integrateVEGAS();
		}
		else if (svfitEventKey.GetIntegrationMethod() == SvfitEventKey::IntegrationMethod::MARKOV_CHAIN)
		{
			svfitStandaloneAlgorithm.integrateMarkovChain();
		}
		else
		{
			LOG(FATAL) << "SVfit integration of type " << svfitEventKey.integrationMethod << " not yet implemented!";
		}
	
		// retrieve results
		svfitResults.Set(svfitStandaloneAlgorithm);
	}
	
	return svfitResults;
}
