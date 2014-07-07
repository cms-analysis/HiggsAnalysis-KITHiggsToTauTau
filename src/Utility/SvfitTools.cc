
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Utility/SvfitTools.h"

#include "Artus/Utility/interface/Utility.h"


RunLumiEvent::RunLumiEvent(int run, int lumi, int event)
{
	Set(run, lumi, event);
}

void RunLumiEvent::Set(int run, int lumi, int event)
{
	this->run = run;
	this->lumi = lumi;
	this->event = event;
}

void RunLumiEvent::CreateBranches(TTree* tree)
{
	tree->Branch("run", &run);
	tree->Branch("lumi", &lumi);
	tree->Branch("event", &event);
}

void RunLumiEvent::SetBranchAddresses(TTree* tree)
{
	tree->SetBranchAddress("run", &run);
	tree->SetBranchAddress("lumi", &lumi);
	tree->SetBranchAddress("event", &event);
	ActivateBranches(tree, true);
}

void RunLumiEvent::ActivateBranches(TTree* tree, bool activate)
{
	tree->SetBranchStatus("run", activate);
	tree->SetBranchStatus("lumi", activate);
	tree->SetBranchStatus("event", activate);
}

bool RunLumiEvent::operator==(RunLumiEvent const& rhs) const
{
	return ((run == rhs.run) && (lumi == rhs.lumi) && (event == rhs.event));
}

bool RunLumiEvent::operator!=(RunLumiEvent const& rhs) const
{
	return (! (*this == rhs));
}

SvfitInputs::SvfitInputs()
{
	this->leptonMomentum1 = new RMDataLV();
	this->leptonMomentum2 = new RMDataLV();
	this->metMomentum = new RMDataV();
	this->metCovariance = new RMSM2x2();
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
	*(this->leptonMomentum1) = leptonMomentum1;
	*(this->leptonMomentum2) = leptonMomentum2;
	*(this->metMomentum) = metMomentum;
	*(this->metCovariance) = metCovariance;
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
	        (*leptonMomentum1 == *(rhs.leptonMomentum1)) && // TODO: better comparison of float members?
	        (*leptonMomentum2 == *(rhs.leptonMomentum2)) && // TODO: better comparison of float members?
	        (*metMomentum == *(rhs.metMomentum)) && // TODO: better comparison of float members?
	        (*metCovariance == *(rhs.metCovariance))); // TODO: better comparison of float members?
}

bool SvfitInputs::operator!=(SvfitInputs const& rhs) const
{
	return (! (*this == rhs));
}

SVfitStandaloneAlgorithm SvfitInputs::GetSvfitStandaloneAlgorithm(int verbosity, bool addLogM) const
{
	SVfitStandaloneAlgorithm svfitStandaloneAlgorithm = SVfitStandaloneAlgorithm(GetMeasuredTauLeptons(),
	                                                                             svFitStandalone::Vector(*metMomentum),
	                                                                             GetMetCovarianceMatrix(),
	                                                                             verbosity);
	svfitStandaloneAlgorithm.addLogM(addLogM);
	return svfitStandaloneAlgorithm;
}

std::vector<svFitStandalone::MeasuredTauLepton> SvfitInputs::GetMeasuredTauLeptons() const
{
	std::vector<svFitStandalone::MeasuredTauLepton> measuredTauLeptons {
		svFitStandalone::MeasuredTauLepton(Utility::ToEnum<svFitStandalone::kDecayType>(decayType1), svFitStandalone::LorentzVector(*leptonMomentum1)),
		svFitStandalone::MeasuredTauLepton(Utility::ToEnum<svFitStandalone::kDecayType>(decayType2), svFitStandalone::LorentzVector(*leptonMomentum2))
	};
	return measuredTauLeptons;
}

TMatrixD SvfitInputs::GetMetCovarianceMatrix() const
{
	TMatrixD metCovarianceMatrix(2, 2);
	metCovarianceMatrix[0][0] = metCovariance->At(0, 0);
	metCovarianceMatrix[1][0] = metCovariance->At(1, 0);
	metCovarianceMatrix[0][1] = metCovariance->At(0, 1);
	metCovarianceMatrix[1][1] = metCovariance->At(1, 1);
	return metCovarianceMatrix;
}

SvfitResults::SvfitResults()
{
	this->momentum = new RMDataLV();
	this->momentumUncertainty = new RMDataLV();
}

SvfitResults::SvfitResults(RMDataLV const& momentum, RMDataLV const& momentumUncertainty) :
	SvfitResults()
{
	Set(momentum, momentumUncertainty);
}

SvfitResults::SvfitResults(SVfitStandaloneAlgorithm const& svfitStandaloneAlgorithm)
{
	this->momentum = new RMDataLV();
	this->momentumUncertainty = new RMDataLV();
	Set(svfitStandaloneAlgorithm);
}

void SvfitResults::Set(RMDataLV const& momentum, RMDataLV const& momentumUncertainty)
{
	*(this->momentum) = momentum;
	*(this->momentumUncertainty) = momentumUncertainty;
}

void SvfitResults::Set(SVfitStandaloneAlgorithm const& svfitStandaloneAlgorithm)
{
	Set(GetMomentum(svfitStandaloneAlgorithm), GetMomentumUncertainty(svfitStandaloneAlgorithm));
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
	return ((*momentum == *(rhs.momentum)) && // TODO: better comparison of float members?
	        (*momentumUncertainty == *(rhs.momentumUncertainty))); // TODO: better comparison of float members?
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
		svfitCacheInputTree = new TChain(treeName.c_str());
		for (std::vector<std::string>::const_iterator fileName = fileNames.begin();
		     fileName != fileNames.end(); ++fileName)
		{
			svfitCacheInputTree->Add(fileName->c_str());
		}
		
		RunLumiEvent runLumiEvent;
		runLumiEvent.SetBranchAddresses(svfitCacheInputTree);
		for (int svfitCacheInputTreeIndex = 0;
		     svfitCacheInputTreeIndex < svfitCacheInputTree->GetEntries();
		     ++svfitCacheInputTreeIndex)
		{
			svfitCacheInputTree->GetEntry(svfitCacheInputTreeIndex);
			svfitCacheInputTreeIndices[runLumiEvent] = svfitCacheInputTreeIndex;
		}
		runLumiEvent.ActivateBranches(svfitCacheInputTree, false);
		
		svfitInputs.SetBranchAddresses(svfitCacheInputTree);
		svfitResults.SetBranchAddresses(svfitCacheInputTree);
	}
}

SvfitResults SvfitTools::GetResults(RunLumiEvent const& runLumiEvent,
                                        SvfitInputs const& svfitInputs,
                                        bool& neededRecalculation)
{
	neededRecalculation = false;
	
	auto svfitCacheInputTreeIndicesItem = svfitCacheInputTreeIndices.find(runLumiEvent);
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
		/*if (settings.GetSvfitUseVegasInsteadOfMarkovChain())
		{
			svfitStandaloneAlgorithm.integrateVEGAS();
		}
		else
		{*/
			svfitStandaloneAlgorithm.integrateMarkovChain();
		//}
	
		// retrieve results
		svfitResults.Set(svfitStandaloneAlgorithm);
	}
	
	return svfitResults;
}
