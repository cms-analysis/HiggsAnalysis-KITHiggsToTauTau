
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
}

bool RunLumiEvent::operator==(RunLumiEvent const& rhs) const
{
	return ((run == rhs.run) && (lumi == rhs.lumi) && (event == rhs.event));
}

SvfitInputs::SvfitInputs(svFitStandalone::kDecayType const& decayType1, svFitStandalone::kDecayType const& decayType2,
                         RMDataLV const& leptonMomentum1, RMDataLV const& leptonMomentum2,
                         RMDataV const& metMomentum, RMSM2x2 const& metCovariance)
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
	tree->Branch("metMomentum", "RMDataV", &metMomentum);
	tree->Branch("metCovariance", "RMSM2x2", &metCovariance);
}

void SvfitInputs::SetBranchAddresses(TTree* tree)
{
	tree->SetBranchAddress("decayType1", &decayType1);
	tree->SetBranchAddress("decayType2", &decayType2);
	tree->SetBranchAddress("leptonMomentum1", &leptonMomentum1);
	tree->SetBranchAddress("leptonMomentum2", &leptonMomentum2);
	tree->SetBranchAddress("metMomentum", &metMomentum);
	tree->SetBranchAddress("metCovariance", &metCovariance);
}

bool SvfitInputs::operator==(SvfitInputs const& rhs) const
{
	return ((decayType1 == rhs.decayType1) &&
	        (decayType2 == rhs.decayType2) &&
	        (leptonMomentum1 == rhs.leptonMomentum1) && // TODO: better comparison of float members?
	        (leptonMomentum2 == rhs.leptonMomentum2) && // TODO: better comparison of float members?
	        (metMomentum == rhs.metMomentum) && // TODO: better comparison of float members?
	        (metCovariance == rhs.metCovariance)); // TODO: better comparison of float members?
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

SvfitResults::SvfitResults(RMDataLV const& momentum, RMDataLV const& momentumUncertainty)
{
	Set(momentum, momentumUncertainty);
}

SvfitResults::SvfitResults(SVfitStandaloneAlgorithm const& svfitStandaloneAlgorithm)
{
	Set(svfitStandaloneAlgorithm);
}

void SvfitResults::Set(RMDataLV const& momentum, RMDataLV const& momentumUncertainty)
{
	this->momentum = momentum;
	this->momentumUncertainty= momentumUncertainty;
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
}

bool SvfitResults::operator==(SvfitResults const& rhs) const
{
	return ((momentum == rhs.momentum) && // TODO: better comparison of float members?
	        (momentumUncertainty == rhs.momentumUncertainty)); // TODO: better comparison of float members?
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

