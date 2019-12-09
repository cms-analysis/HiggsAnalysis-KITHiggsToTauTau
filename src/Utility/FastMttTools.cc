
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Utility/FastMttTools.h"

#include "Artus/Utility/interface/DefaultValues.h"
#include "Artus/Utility/interface/Utility.h"

FastMttInputs::FastMttInputs(RMFLV const& leptonMomentum1,
			     classic_svFit::MeasuredTauLepton::kDecayType const& decayType1,
			     int const& decayMode1,
			     RMFLV const& leptonMomentum2,
			     classic_svFit::MeasuredTauLepton::kDecayType const& decayType2,
			     int const& decayMode2,
			     RMDataV const& metMomentum, RMSM2x2 const& metCovariance)
	: FastMttInputs()
{
        Set(leptonMomentum1, decayType1, decayMode1,
	    leptonMomentum2, decayType2, decayMode2,
	    metMomentum, metCovariance);
}

FastMttInputs::~FastMttInputs()
{
	/* TODO: freeing memory here creates segmentation faults
	if (leptonMomentum1)
	{
		delete leptonMomentum1;
	}
	if (leptonMomentum2)
	{
		delete leptonMomentum2;
	}
	if (metMomentum)
	{
		delete metMomentum;
	}
	if (metCovariance)
	{
		delete metCovariance;
	}
	*/
}

void FastMttInputs::Set(RMFLV const& leptonMomentum1,
			classic_svFit::MeasuredTauLepton::kDecayType const& decayType1,
			int const& decayMode1,
			RMFLV const& leptonMomentum2,
			classic_svFit::MeasuredTauLepton::kDecayType const& decayType2,
			int const& decayMode2,
			RMDataV const& metMomentum, RMSM2x2 const& metCovariance)
{
	if (! this->leptonMomentum1)
	{
		this->leptonMomentum1 = new RMFLV();
	}
	if (! this->leptonMomentum2)
	{
		this->leptonMomentum2 = new RMFLV();
	}
	if (! this->metMomentum)
	{
		this->metMomentum = new RMDataV();
	}
	if (! this->metCovariance)
	{
		this->metCovariance = new RMSM2x2();
	}

	*(this->leptonMomentum1) = leptonMomentum1;
	this->decayType1 = Utility::ToUnderlyingValue(decayType1);
	this->decayMode1 = decayMode1;
	*(this->leptonMomentum2) = leptonMomentum2;
	this->decayType2 = Utility::ToUnderlyingValue(decayType2);
	this->decayMode2 = decayMode2;
	*(this->metMomentum) = metMomentum;
	*(this->metCovariance) = metCovariance;
}

bool FastMttInputs::operator==(FastMttInputs const& rhs) const
{
	return (Utility::ApproxEqual(*leptonMomentum1, *(rhs.leptonMomentum1)) &&
		(decayType1 == rhs.decayType1) &&
                (decayMode1 == rhs.decayMode1) &&
	        Utility::ApproxEqual(*leptonMomentum2, *(rhs.leptonMomentum2)) &&
                (decayType2 == rhs.decayType2) &&
                (decayMode2 == rhs.decayMode2) &&
	        Utility::ApproxEqual(*metMomentum, *(rhs.metMomentum)) &&
	        Utility::ApproxEqual(*metCovariance, *(rhs.metCovariance)));
}

bool FastMttInputs::operator!=(FastMttInputs const& rhs) const
{
	return (! (*this == rhs));
}

void FastMttInputs::Integrate(FastMTT& fastmttAlgorithm) const
{
        fastmttAlgorithm.run(GetMeasuredTauLeptons(),
			     metMomentum->x(),
			     metMomentum->y(),
			     GetMetCovarianceMatrix()
	);
}

std::vector<classic_svFit::MeasuredTauLepton> FastMttInputs::GetMeasuredTauLeptons() const
{
	double leptonMass1, leptonMass2;
	if(decayType1 == 2)
	{
		leptonMass1 = 0.51100e-3;
	}
	else if(decayType1 == 3)
	{
		leptonMass1 = 105.658e-3;
	}
	else
	{
		leptonMass1 = leptonMomentum1->M();
	}
	if(decayType2 == 2)
	{
		leptonMass2 = 0.51100e-3;
	}
	else if(decayType2 == 3)
	{
		leptonMass2 = 105.658e-3;
	}
	else
	{
		leptonMass2 = leptonMomentum2->M();
	}
	std::vector<classic_svFit::MeasuredTauLepton> measuredTauLeptons {
		classic_svFit::MeasuredTauLepton(Utility::ToEnum<classic_svFit::MeasuredTauLepton::kDecayType>(decayType1), leptonMomentum1->pt(), leptonMomentum1->eta(), leptonMomentum1->phi(), leptonMass1, decayMode1),
		classic_svFit::MeasuredTauLepton(Utility::ToEnum<classic_svFit::MeasuredTauLepton::kDecayType>(decayType2), leptonMomentum2->pt(), leptonMomentum2->eta(), leptonMomentum2->phi(), leptonMass2, decayMode2)
	};
	return measuredTauLeptons;
}

TMatrixD FastMttInputs::GetMetCovarianceMatrix() const
{
	TMatrixD metCovarianceMatrix(2, 2);
	metCovarianceMatrix[0][0] = metCovariance->At(0, 0);
	metCovarianceMatrix[1][0] = metCovariance->At(1, 0);
	metCovarianceMatrix[0][1] = metCovariance->At(0, 1);
	metCovarianceMatrix[1][1] = metCovariance->At(1, 1);
	return metCovarianceMatrix;
}


FastMttResults::FastMttResults(RMFLV const& fittedHiggsLV, float fittedTau1ERatio, RMFLV const& fittedTau1LV, float fittedTau2ERatio, RMFLV const& fittedTau2LV) :
	FastMttResults()
{
        Set(fittedHiggsLV, fittedTau1ERatio, fittedTau1LV, fittedTau2ERatio, fittedTau2LV);
}

FastMttResults::FastMttResults(FastMTT const& fastmttAlgorithm, float tau1Pt, float tau2Pt) :
	FastMttResults()
{
  Set(fastmttAlgorithm, tau1Pt, tau2Pt);
}

FastMttResults::~FastMttResults()
{
	/* TODO: freeing memory here creates segmentation faults
	if (fittedHiggsLV)
	{
		delete fittedHiggsLV;
	}
	if (fittedTau1LV)
	{
		delete fittedTau1LV;
	}
	if (fittedTau2LV)
	{
		delete fittedTau2LV;
	}
	*/
}

void FastMttResults::Set(RMFLV const& fittedHiggsLV, float fittedTau1ERatio, RMFLV const& fittedTau1LV, float fittedTau2ERatio, RMFLV const& fittedTau2LV)
{
	if (! this->fittedHiggsLV)
	{
		this->fittedHiggsLV = new RMFLV();
	}
	if (! this->fittedTau1LV)
	{
		this->fittedTau1LV = new RMFLV();
	}
	if (! this->fittedTau2LV)
	{
		this->fittedTau2LV = new RMFLV();
	}

	*(this->fittedHiggsLV) = fittedHiggsLV;
	this->fittedTau1ERatio = fittedTau1ERatio;
	*(this->fittedTau1LV) = fittedTau1LV;
	this->fittedTau2ERatio = fittedTau2ERatio;
	*(this->fittedTau2LV) = fittedTau2LV;
}

void FastMttResults::Set(FastMTT const& fastmttAlgorithm, float tau1Pt, float tau2Pt)
{
	if (fastmttAlgorithm.getBestP4().mass()>0)
	{
		Set(GetFittedHiggsLV(fastmttAlgorithm),
		    tau1Pt>0?tau1Pt/GetFittedTau1LV(fastmttAlgorithm).pt():DefaultValues::UndefinedFloat,
		    GetFittedTau1LV(fastmttAlgorithm),
		    tau2Pt>0?tau2Pt/GetFittedTau1LV(fastmttAlgorithm).pt():DefaultValues::UndefinedFloat,
		    GetFittedTau2LV(fastmttAlgorithm));
	}
	else
	{
		Set(DefaultValues::UndefinedRMFLV,
		    DefaultValues::UndefinedFloat,
		    DefaultValues::UndefinedRMFLV,
		    DefaultValues::UndefinedFloat,
		    DefaultValues::UndefinedRMFLV);
	}
}

bool FastMttResults::operator==(FastMttResults const& rhs) const
{
	return (Utility::ApproxEqual(*fittedHiggsLV, *(rhs.fittedHiggsLV)) &&
	        Utility::ApproxEqual(*fittedTau1LV, *(rhs.fittedTau1LV)) &&
	        Utility::ApproxEqual(*fittedTau2LV, *(rhs.fittedTau2LV)));
}

bool FastMttResults::operator!=(FastMttResults const& rhs) const
{
	return (! (*this == rhs));
}

RMFLV FastMttResults::GetFittedHiggsLV(FastMTT const& fastmttAlgorithm) const
{
        return Utility::ConvertPtEtaPhiMLorentzVector<ROOT::Math::LorentzVector<ROOT::Math::PxPyPzE4D<double> > >(fastmttAlgorithm.getBestP4());
}

RMFLV FastMttResults::GetFittedTau1LV(FastMTT const& fastmttAlgorithm) const
{
        return Utility::ConvertPtEtaPhiMLorentzVector<ROOT::Math::LorentzVector<ROOT::Math::PxPyPzE4D<double> > >(fastmttAlgorithm.getTau1P4());
}

RMFLV FastMttResults::GetFittedTau2LV(FastMTT const& fastmttAlgorithm) const
{
        return Utility::ConvertPtEtaPhiMLorentzVector<ROOT::Math::LorentzVector<ROOT::Math::PxPyPzE4D<double> > >(fastmttAlgorithm.getTau2P4());
}

FastMttTools::FastMttTools() :
	fastmttAlgorithm()
{
}

FastMttResults FastMttTools::GetResults(FastMttInputs const& fastmttInputs)
{
	// execute integration
	fastmttInputs.Integrate(this->fastmttAlgorithm);

	// retrieve results
	float tau1Pt = fastmttInputs.leptonMomentum1!=nullptr?fastmttInputs.leptonMomentum1->pt():-1.;
	float tau2Pt = fastmttInputs.leptonMomentum2!=nullptr?fastmttInputs.leptonMomentum2->pt():-1.;
	fastmttResults.Set(this->fastmttAlgorithm,tau1Pt,tau2Pt);

	return fastmttResults;
}

FastMttTools::~FastMttTools()
{}
