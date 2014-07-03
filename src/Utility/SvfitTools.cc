
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Utility/SvfitTools.h"

#include "Artus/Utility/interface/Utility.h"


SvfitTools::SvfitTools(svFitStandalone::kDecayType const& decayType1, svFitStandalone::kDecayType const& decayType2,
                       RMDataLV* leptonMomentum1, RMDataLV* leptonMomentum2,
                       RMDataV const& metMomentum, RMSM* metCovariance,
                       IntegrationMethod integrationMethod) :
	decayType1(Utility::ToUnderlyingValue(decayType1)),
	decayType2(Utility::ToUnderlyingValue(decayType2)),
	leptonMomentum1(leptonMomentum1),
	leptonMomentum2(leptonMomentum2),
	metMomentum(metMomentum),
	metCovariance(metCovariance),
	integrationMethod(Utility::ToUnderlyingValue(integrationMethod))
{
	Calculate();
}


SvfitTools::~SvfitTools()
{
	delete svfitStandaloneAlgorithm;
}


SVfitStandaloneAlgorithm* SvfitTools::Calculate()
{
	std::vector<svFitStandalone::MeasuredTauLepton> measuredTauLeptons {
		svFitStandalone::MeasuredTauLepton(Utility::ToEnum<svFitStandalone::kDecayType>(decayType1), svFitStandalone::LorentzVector(*leptonMomentum1)),
		svFitStandalone::MeasuredTauLepton(Utility::ToEnum<svFitStandalone::kDecayType>(decayType2), svFitStandalone::LorentzVector(*leptonMomentum2))
	};
	
	TMatrixD metCovarianceMatrix(2, 2);
	metCovarianceMatrix[0][0] = metCovariance->At(0, 0);
	metCovarianceMatrix[1][0] = metCovariance->At(1, 0);
	metCovarianceMatrix[0][1] = metCovariance->At(0, 1);
	metCovarianceMatrix[1][1] = metCovariance->At(1, 1);

	int verbosity = 0;
	
	svfitStandaloneAlgorithm = new SVfitStandaloneAlgorithm(measuredTauLeptons,
	                                                        svFitStandalone::Vector(metMomentum),
	                                                        metCovarianceMatrix,
	                                                        verbosity);
	svfitStandaloneAlgorithm->addLogM(false);
	
	if (Utility::ToEnum<IntegrationMethod>(integrationMethod) == IntegrationMethod::MARKOV_CHAIN)
	{
		svfitStandaloneAlgorithm->integrateMarkovChain();
	}
	else if (Utility::ToEnum<IntegrationMethod>(integrationMethod) == IntegrationMethod::VEGAS)
	{
		svfitStandaloneAlgorithm->integrateVEGAS();
	}
	
	return svfitStandaloneAlgorithm;
}


RMDataLV SvfitTools::GetTauTauMomentum()
{
	RMDataLV momentum;
	momentum.SetPt(svfitStandaloneAlgorithm->pt());
	momentum.SetEta(svfitStandaloneAlgorithm->eta());
	momentum.SetPhi(svfitStandaloneAlgorithm->phi());
	momentum.SetM(svfitStandaloneAlgorithm->mass());
	return momentum;
}


RMDataLV SvfitTools::GetTauTauMomentumUncertainty()
{
	RMDataLV momentumUncertainty;
	momentumUncertainty.SetPt(svfitStandaloneAlgorithm->ptUncert());
	momentumUncertainty.SetEta(svfitStandaloneAlgorithm->etaUncert());
	momentumUncertainty.SetPhi(svfitStandaloneAlgorithm->phiUncert());
	momentumUncertainty.SetM(svfitStandaloneAlgorithm->massUncert());
	return momentumUncertainty;
}

