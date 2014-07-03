
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Utility/SvfitTools.h"

#include "Artus/Utility/interface/Utility.h"

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
	Set(GetMomentum(svfitStandaloneAlgorithm), GetMomentumUncertainty(svfitStandaloneAlgorithm));
}

void SvfitResults::Set(RMDataLV const& momentum, RMDataLV const& momentumUncertainty)
{
	this->momentum = momentum;
	this->momentumUncertainty= momentumUncertainty;
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

