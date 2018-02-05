
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Utility/SvfitTools.h"

#include "Artus/Utility/interface/DefaultValues.h"
#include "Artus/Utility/interface/Utility.h"
#include "Artus/Utility/interface/SafeMap.h"


TH1* PhiCPSVfitQuantity::createHistogram(const classic_svFit::LorentzVector& vis1P4, const classic_svFit::LorentzVector& vis2P4, const classic_svFit::Vector& met) const
{
	return new TH1D(std::string("svfitAlgorithm_histogram_phiCP").c_str(), std::string("svfitAlgorithm_histogram_phiCP").c_str(), 180, 0.0, 2.0*TMath::Pi());
}
double PhiCPSVfitQuantity::fitFunction(const classic_svFit::LorentzVector& tau1P4, const classic_svFit::LorentzVector& tau2P4, const classic_svFit::LorentzVector& vis1P4, const classic_svFit::LorentzVector& vis2P4, const classic_svFit::Vector& met) const
{
	return cpQuantities.CalculatePhiCP(
			Utility::ConvertPtEtaPhiMLorentzVector<classic_svFit::LorentzVector>(tau1P4+tau2P4),
			Utility::ConvertPtEtaPhiMLorentzVector<classic_svFit::LorentzVector>(tau1P4),
			Utility::ConvertPtEtaPhiMLorentzVector<classic_svFit::LorentzVector>(tau2P4),
			Utility::ConvertPtEtaPhiMLorentzVector<classic_svFit::LorentzVector>(vis1P4),
			Utility::ConvertPtEtaPhiMLorentzVector<classic_svFit::LorentzVector>(vis2P4)
	);
}

TH1* PhiStarCPSVfitQuantity::createHistogram(const classic_svFit::LorentzVector& vis1P4, const classic_svFit::LorentzVector& vis2P4, const classic_svFit::Vector& met) const
{
	return new TH1D(std::string("svfitAlgorithm_histogram_phiStarCP").c_str(), std::string("svfitAlgorithm_histogram_phiStarCP").c_str(), 180, 0.0, 2.0*TMath::Pi());
}
double PhiStarCPSVfitQuantity::fitFunction(const classic_svFit::LorentzVector& tau1P4, const classic_svFit::LorentzVector& tau2P4, const classic_svFit::LorentzVector& vis1P4, const classic_svFit::LorentzVector& vis2P4, const classic_svFit::Vector& met) const
{
	return cpQuantities.CalculatePhiStarCP(
			Utility::ConvertPtEtaPhiMLorentzVector<classic_svFit::LorentzVector>(tau1P4),
			Utility::ConvertPtEtaPhiMLorentzVector<classic_svFit::LorentzVector>(tau2P4),
			Utility::ConvertPtEtaPhiMLorentzVector<classic_svFit::LorentzVector>(vis1P4),
			Utility::ConvertPtEtaPhiMLorentzVector<classic_svFit::LorentzVector>(vis2P4)
	);
}

TauTauHistogramAdapter::TauTauHistogramAdapter(std::vector<classic_svFit::SVfitQuantity*> const& quantities) :
	classic_svFit::TauTauHistogramAdapter(quantities)
{
	indexTau1ERatio = registerQuantity(new classic_svFit::TauERatioSVfitQuantity(0));
	indexTau2ERatio = registerQuantity(new classic_svFit::TauERatioSVfitQuantity(1));
}

RMFLV TauTauHistogramAdapter::GetFittedHiggsLV() const
{
	return Utility::ConvertPtEtaPhiMLorentzVector<classic_svFit::LorentzVector>(classic_svFit::TauTauHistogramAdapter::GetFittedHiggsLV());
}

float TauTauHistogramAdapter::GetFittedTau1ERatio() const
{
	return extractValue(indexTau1ERatio);
}

RMFLV TauTauHistogramAdapter::GetFittedTau1LV() const
{
	return Utility::ConvertPtEtaPhiMLorentzVector<classic_svFit::LorentzVector>(classic_svFit::TauTauHistogramAdapter::GetFittedTau1LV());
}

float TauTauHistogramAdapter::GetFittedTau2ERatio() const
{
	return extractValue(indexTau2ERatio);
}

RMFLV TauTauHistogramAdapter::GetFittedTau2LV() const
{
	return Utility::ConvertPtEtaPhiMLorentzVector<classic_svFit::LorentzVector>(classic_svFit::TauTauHistogramAdapter::GetFittedTau2LV());
}


SvfitEventKey::SvfitEventKey(ULong64_t const& runLumiEvent,
                             classic_svFit::MeasuredTauLepton::kDecayType const& decayType1, classic_svFit::MeasuredTauLepton::kDecayType const& decayType2,
                             int const& decayMode1, int const& decayMode2,
                             HttEnumTypes::SystematicShift const& systematicShift, float const& systematicShiftSigma,
                             float const& diTauMassConstraint)
{
	Set(runLumiEvent, decayType1, decayType2, decayMode1, decayMode2, systematicShift, systematicShiftSigma, diTauMassConstraint);
}

void SvfitEventKey::Set(ULong64_t const& runLumiEvent,
                        classic_svFit::MeasuredTauLepton::kDecayType const& decayType1, classic_svFit::MeasuredTauLepton::kDecayType const& decayType2,
                        int const& decayMode1, int const& decayMode2,
                        HttEnumTypes::SystematicShift const& systematicShift, float const& systematicShiftSigma,
                        float const& diTauMassConstraint)
{
	this->runLumiEvent = runLumiEvent;
	this->decayType1 = Utility::ToUnderlyingValue(decayType1);
	this->decayType2 = Utility::ToUnderlyingValue(decayType2);
	this->decayMode1 = decayMode1;
	this->decayMode2 = decayMode2;
	this->systematicShift = Utility::ToUnderlyingValue<HttEnumTypes::SystematicShift>(systematicShift);
	this->systematicShiftSigma = systematicShiftSigma;
	this->diTauMassConstraint = diTauMassConstraint;
}

HttEnumTypes::SystematicShift SvfitEventKey::GetSystematicShift() const
{
	return Utility::ToEnum<HttEnumTypes::SystematicShift>(systematicShift);
}

void SvfitEventKey::CreateBranches(TTree* tree)
{
	tree->Branch("runLumiEvent", &runLumiEvent, "runLumiEvent/l");
	tree->Branch("decayType1", &decayType1);
	tree->Branch("decayType2", &decayType2);
	tree->Branch("decayMode1", &decayMode1);
	tree->Branch("decayMode2", &decayMode2);
	tree->Branch("systematicShift", &systematicShift);
	tree->Branch("systematicShiftSigma", &systematicShiftSigma);
	tree->Branch("diTauMassConstraint", &diTauMassConstraint);
}

void SvfitEventKey::SetBranchAddresses(TTree* tree)
{
	tree->SetBranchAddress("runLumiEvent", &runLumiEvent);
	tree->SetBranchAddress("decayType1", &decayType1);
	tree->SetBranchAddress("decayType2", &decayType2);
	tree->SetBranchAddress("decayMode1", &decayMode1);
	tree->SetBranchAddress("decayMode2", &decayMode2);
	tree->SetBranchAddress("systematicShift", &systematicShift);
	tree->SetBranchAddress("systematicShiftSigma", &systematicShiftSigma);
	tree->SetBranchAddress("diTauMassConstraint", &diTauMassConstraint);
	ActivateBranches(tree, true);
}

void SvfitEventKey::ActivateBranches(TTree* tree, bool activate)
{
	tree->SetBranchStatus("runLumiEvent", activate);
	tree->SetBranchStatus("decayType1", activate);
	tree->SetBranchStatus("decayType2", activate);
	tree->SetBranchStatus("decayMode1", activate);
	tree->SetBranchStatus("decayMode2", activate);
	tree->SetBranchStatus("systematicShift", activate);
	tree->SetBranchStatus("systematicShiftSigma", activate);
	tree->SetBranchStatus("diTauMassConstraint", activate);
}

bool SvfitEventKey::operator<(SvfitEventKey const& rhs) const
{
	if (runLumiEvent == rhs.runLumiEvent)
	{
		if (decayType1 == rhs.decayType1)
		{
			if (decayType2 == rhs.decayType2)
			{
				if (decayMode1 == rhs.decayMode1)
				{
					if (decayMode2 == rhs.decayMode2)
					{
						if (systematicShift == rhs.systematicShift)
						{
							if (Utility::ApproxEqual(systematicShiftSigma, rhs.systematicShiftSigma))
							{
								return (diTauMassConstraint < rhs.diTauMassConstraint);
							}
							else
							{
								return (systematicShiftSigma < rhs.systematicShiftSigma);
							}
						}
						else
						{
							return (systematicShift < rhs.systematicShift);
						}
					}
					else
					{
						return (decayMode2 < rhs.decayMode2);
					}
				}
				else
				{
					return (decayMode1 < rhs.decayMode1);
				}
			}
			else
			{
				return (decayType2 < rhs.decayType2);
			}
		}
		else
		{
			return (decayType1 < rhs.decayType1);
		}
	}
	else {
		return (runLumiEvent < rhs.runLumiEvent);
	}
}

bool SvfitEventKey::operator==(SvfitEventKey const& rhs) const
{
	return ((runLumiEvent == rhs.runLumiEvent) &&
	        (decayType1 == rhs.decayType1) &&
	        (decayType2 == rhs.decayType2) &&
	        (decayMode1 == rhs.decayMode1) &&
	        (decayMode2 == rhs.decayMode2) &&
	        (systematicShift == rhs.systematicShift) &&
	        Utility::ApproxEqual(systematicShiftSigma, rhs.systematicShiftSigma) &&
	        Utility::ApproxEqual(diTauMassConstraint, rhs.diTauMassConstraint));
}

bool SvfitEventKey::operator!=(SvfitEventKey const& rhs) const
{
	return (! (*this == rhs));
}

std::string std::to_string(SvfitEventKey const& svfitEventKey)
{
	return std::string("SvfitEventKey(") +
			"runLumiEvent=" + std::to_string(svfitEventKey.runLumiEvent) + ", " +
			"decayType1=" + std::to_string(svfitEventKey.decayType1) + ", " +
			"decayType2=" + std::to_string(svfitEventKey.decayType2) + ", " +
			"decayMode1=" + std::to_string(svfitEventKey.decayMode1) + ", " +
			"decayMode2=" + std::to_string(svfitEventKey.decayMode2) + ", " +
			"systematicShift=" + std::to_string(svfitEventKey.systematicShift) + ", " +
			"systematicShiftSigma=" + std::to_string(svfitEventKey.systematicShiftSigma) + ", " +
			"diTauMassConstraint=" + std::to_string(svfitEventKey.diTauMassConstraint) + ")";
}

std::ostream& operator<<(std::ostream& os, SvfitEventKey const& svfitEventKey)
{
	return os << std::to_string(svfitEventKey);
}

SvfitInputs::SvfitInputs(RMFLV const& leptonMomentum1, RMFLV const& leptonMomentum2,
                         RMDataV const& metMomentum, RMSM2x2 const& metCovariance)
	: SvfitInputs()
{
	Set(leptonMomentum1, leptonMomentum2, metMomentum, metCovariance);
}

SvfitInputs::~SvfitInputs()
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

void SvfitInputs::Set(RMFLV const& leptonMomentum1, RMFLV const& leptonMomentum2,
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
	*(this->leptonMomentum2) = leptonMomentum2;
	*(this->metMomentum) = metMomentum;
	*(this->metCovariance) = metCovariance;
}

void SvfitInputs::CreateBranches(TTree* tree)
{
	tree->Branch("leptonMomentum1", "RMFLV", &leptonMomentum1);
	tree->Branch("leptonMomentum2", "RMFLV", &leptonMomentum2);
	tree->Branch("metMomentum", "ROOT::Math::DisplacementVector3D<ROOT::Math::Cartesian3D<float>,ROOT::Math::DefaultCoordinateSystemTag>", &metMomentum);
	tree->Branch("metCovariance", "ROOT::Math::SMatrix<double, 2, 2, ROOT::Math::MatRepSym<double, 2> >", &metCovariance);
}

void SvfitInputs::SetBranchAddresses(TTree* tree)
{
	tree->SetBranchAddress("leptonMomentum1", &leptonMomentum1);
	tree->SetBranchAddress("leptonMomentum2", &leptonMomentum2);
	tree->SetBranchAddress("metMomentum", &metMomentum);
	tree->SetBranchAddress("metCovariance", &metCovariance);
	ActivateBranches(tree, true);
}

void SvfitInputs::ActivateBranches(TTree* tree, bool activate)
{
	tree->SetBranchStatus("leptonMomentum1", activate);
	tree->SetBranchStatus("leptonMomentum2", activate);
	tree->SetBranchStatus("metMomentum", activate);
	tree->SetBranchStatus("metCovariance", activate);
}

bool SvfitInputs::operator==(SvfitInputs const& rhs) const
{
	return (Utility::ApproxEqual(*leptonMomentum1, *(rhs.leptonMomentum1)) &&
	        Utility::ApproxEqual(*leptonMomentum2, *(rhs.leptonMomentum2)) &&
	        Utility::ApproxEqual(*metMomentum, *(rhs.metMomentum)) &&
	        Utility::ApproxEqual(*metCovariance, *(rhs.metCovariance)));
}

bool SvfitInputs::operator!=(SvfitInputs const& rhs) const
{
	return (! (*this == rhs));
}

void SvfitInputs::Integrate(SvfitEventKey const& svfitEventKey, ClassicSVfit& svfitAlgorithm) const
{
	svfitAlgorithm.integrate(
			GetMeasuredTauLeptons(svfitEventKey),
			metMomentum->x(),
			metMomentum->y(),
			GetMetCovarianceMatrix()
	);
}

std::vector<classic_svFit::MeasuredTauLepton> SvfitInputs::GetMeasuredTauLeptons(SvfitEventKey const& svfitEventKey) const
{
	double leptonMass1, leptonMass2;
	if(svfitEventKey.decayType1 == 2)
	{
		leptonMass1 = 0.51100e-3;
	}
	else if(svfitEventKey.decayType1 == 3)
	{
		leptonMass1 = 105.658e-3;
	}
	else
	{
		leptonMass1 = leptonMomentum1->M();
	}
	if(svfitEventKey.decayType2 == 2)
	{
		leptonMass2 = 0.51100e-3;
	}
	else if(svfitEventKey.decayType2 == 3)
	{
		leptonMass2 = 105.658e-3;
	}
	else
	{
		leptonMass2 = leptonMomentum2->M();
	}
	std::vector<classic_svFit::MeasuredTauLepton> measuredTauLeptons {
		classic_svFit::MeasuredTauLepton(Utility::ToEnum<classic_svFit::MeasuredTauLepton::kDecayType>(svfitEventKey.decayType1), leptonMomentum1->pt(), leptonMomentum1->eta(), leptonMomentum1->phi(), leptonMass1, svfitEventKey.decayMode1),
		classic_svFit::MeasuredTauLepton(Utility::ToEnum<classic_svFit::MeasuredTauLepton::kDecayType>(svfitEventKey.decayType2), leptonMomentum2->pt(), leptonMomentum2->eta(), leptonMomentum2->phi(), leptonMass2, svfitEventKey.decayMode2)
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

SvfitResults::SvfitResults(double fittedTransverseMass, RMFLV const& fittedHiggsLV, float fittedTau1ERatio, RMFLV const& fittedTau1LV, float fittedTau2ERatio, RMFLV const& fittedTau2LV) :
	SvfitResults()
{
	Set(fittedTransverseMass, fittedHiggsLV, fittedTau1ERatio, fittedTau1LV, fittedTau2ERatio, fittedTau2LV);
	recalculated = false;
}

SvfitResults::SvfitResults(ClassicSVfit const& svfitAlgorithm) :
	SvfitResults()
{
	Set(svfitAlgorithm);
}

SvfitResults::~SvfitResults()
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

void SvfitResults::Set(double fittedTransverseMass, RMFLV const& fittedHiggsLV, float fittedTau1ERatio, RMFLV const& fittedTau1LV, float fittedTau2ERatio, RMFLV const& fittedTau2LV)
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
	
	this->fittedTransverseMass = fittedTransverseMass;
	*(this->fittedHiggsLV) = fittedHiggsLV;
	this->fittedTau1ERatio = fittedTau1ERatio;
	*(this->fittedTau1LV) = fittedTau1LV;
	this->fittedTau2ERatio = fittedTau2ERatio;
	*(this->fittedTau2LV) = fittedTau2LV;
}

void SvfitResults::Set(ClassicSVfit const& svfitAlgorithm)
{
	if (svfitAlgorithm.isValidSolution())
	{
		Set(GetFittedTransverseMass(svfitAlgorithm),
		    GetFittedHiggsLV(svfitAlgorithm),
		    GetFittedTau1ERatio(svfitAlgorithm),
		    GetFittedTau1LV(svfitAlgorithm),
		    GetFittedTau2ERatio(svfitAlgorithm),
		    GetFittedTau2LV(svfitAlgorithm));
	}
	else
	{
		Set(DefaultValues::UndefinedFloat,
		    DefaultValues::UndefinedRMFLV,
		    DefaultValues::UndefinedFloat,
		    DefaultValues::UndefinedRMFLV,
		    DefaultValues::UndefinedFloat,
		    DefaultValues::UndefinedRMFLV);
	}
}

void SvfitResults::CreateBranches(TTree* tree)
{
	tree->Branch("svfitTransverseMass", &fittedTransverseMass, "svfitTransverseMass/D");
	tree->Branch("svfitHiggsLV", &fittedHiggsLV);
	tree->Branch("svfitTau1ERatio", &fittedTau1ERatio, "svfitTau1ERatio/F");
	tree->Branch("svfitTau1LV", &fittedTau1LV);
	tree->Branch("svfitTau2ERatio", &fittedTau2ERatio, "svfitTau2ERatio/F");
	tree->Branch("svfitTau2LV", &fittedTau2LV);
}

void SvfitResults::SetBranchAddresses(TTree* tree)
{
	tree->SetBranchAddress("svfitTransverseMass", &fittedTransverseMass);
	tree->SetBranchAddress("svfitHiggsLV", &fittedHiggsLV);
	tree->SetBranchAddress("svfitTau1ERatio", &fittedTau1ERatio);
	tree->SetBranchAddress("svfitTau1LV", &fittedTau1LV);
	tree->SetBranchAddress("svfitTau2ERatio", &fittedTau2ERatio);
	tree->SetBranchAddress("svfitTau2LV", &fittedTau2LV);
	ActivateBranches(tree, true);
}

void SvfitResults::ActivateBranches(TTree* tree, bool activate)
{
	tree->SetBranchStatus("svfitTransverseMass", activate);
	tree->SetBranchStatus("svfitHiggsLV", activate);
	tree->SetBranchStatus("svfitTau1ERatio", activate);
	tree->SetBranchStatus("svfitTau1LV", activate);
	tree->SetBranchStatus("svfitTau2ERatio", activate);
	tree->SetBranchStatus("svfitTau2LV", activate);
}

bool SvfitResults::operator==(SvfitResults const& rhs) const
{
	return (Utility::ApproxEqual(fittedTransverseMass, rhs.fittedTransverseMass) &&
	        Utility::ApproxEqual(*fittedHiggsLV, *(rhs.fittedHiggsLV)) &&
	        Utility::ApproxEqual(fittedTau1ERatio, rhs.fittedTau1ERatio) &&
	        Utility::ApproxEqual(*fittedTau1LV, *(rhs.fittedTau1LV)) &&
	        Utility::ApproxEqual(fittedTau2ERatio, rhs.fittedTau2ERatio) &&
	        Utility::ApproxEqual(*fittedTau2LV, *(rhs.fittedTau2LV)));
}

bool SvfitResults::operator!=(SvfitResults const& rhs) const
{
	return (! (*this == rhs));
}

double SvfitResults::GetFittedTransverseMass(ClassicSVfit const& svfitAlgorithm) const
{
	return static_cast<TauTauHistogramAdapter*>(svfitAlgorithm.getHistogramAdapter())->getTransverseMass();
}
RMFLV SvfitResults::GetFittedHiggsLV(ClassicSVfit const& svfitAlgorithm) const
{
	return static_cast<TauTauHistogramAdapter*>(svfitAlgorithm.getHistogramAdapter())->GetFittedHiggsLV();
}
float SvfitResults::GetFittedTau1ERatio(ClassicSVfit const& svfitAlgorithm) const
{
	return static_cast<TauTauHistogramAdapter*>(svfitAlgorithm.getHistogramAdapter())->GetFittedTau1ERatio();
}
RMFLV SvfitResults::GetFittedTau1LV(ClassicSVfit const& svfitAlgorithm) const
{
	return static_cast<TauTauHistogramAdapter*>(svfitAlgorithm.getHistogramAdapter())->GetFittedTau1LV();
}
float SvfitResults::GetFittedTau2ERatio(ClassicSVfit const& svfitAlgorithm) const
{
	return static_cast<TauTauHistogramAdapter*>(svfitAlgorithm.getHistogramAdapter())->GetFittedTau2ERatio();
}
RMFLV SvfitResults::GetFittedTau2LV(ClassicSVfit const& svfitAlgorithm) const
{
	return static_cast<TauTauHistogramAdapter*>(svfitAlgorithm.getHistogramAdapter())->GetFittedTau2LV();
}


std::map<std::string, TFile*> SvfitTools::svfitCacheInputFiles;
std::map<std::string, TTree*> SvfitTools::svfitCacheInputTrees;
std::map<std::string, std::map<SvfitEventKey, uint64_t>> SvfitTools::svfitCacheInputTreeIndices;

SvfitTools::SvfitTools() :
	svfitAlgorithm(0)
{
	svfitAlgorithm.setHistogramAdapter(new TauTauHistogramAdapter());
}

void SvfitTools::Init(std::string const& cacheFileName, std::string const& cacheTreeName)
{
	this->cacheFileName = cacheFileName;
	this->cacheFileTreeName = cacheFileName+"/"+cacheTreeName;
	
	if (! Utility::Contains(SvfitTools::svfitCacheInputTreeIndices, cacheFileTreeName))
	{
		TDirectory* savedir(gDirectory);
		TFile* savefile(gFile);
		
		TFile* svfitCacheInputFile = nullptr;
		if (! Utility::Contains(SvfitTools::svfitCacheInputFiles, cacheFileName))
		{
			svfitCacheInputFile = TFile::Open(cacheFileName.c_str(), "READ", cacheFileName.c_str());
		}
		else
		{
			svfitCacheInputFile = SafeMap::Get(SvfitTools::svfitCacheInputFiles, cacheFileName);
		}
		
		if (svfitCacheInputFile)
		{
			TTree* svfitCacheInputTree = dynamic_cast<TTree*>(svfitCacheInputFile->Get(cacheTreeName.c_str()));
			if (svfitCacheInputTree)
			{
				LOG(DEBUG) << "\tLoaded SVfit cache trees from file...";
				LOG(DEBUG) << "\t\t" << cacheFileTreeName << " with " << svfitCacheInputTree->GetEntries() << " Entries";

				svfitEventKey.SetBranchAddresses(svfitCacheInputTree);
				std::map<SvfitEventKey, uint64_t> svfitCacheInputTreeIndices;
				for (uint64_t svfitCacheInputTreeIndex = 0;
					 svfitCacheInputTreeIndex < uint64_t(svfitCacheInputTree->GetEntries());
					 ++svfitCacheInputTreeIndex)
				{
					svfitCacheInputTree->GetEntry(svfitCacheInputTreeIndex);

					svfitCacheInputTreeIndices[svfitEventKey] = svfitCacheInputTreeIndex;
					LOG_N_TIMES(10, DEBUG) << std::to_string(svfitEventKey) << " --> " << svfitCacheInputTreeIndex;
					LOG_N_TIMES(10, DEBUG) << svfitEventKey << " --> " << svfitCacheInputTreeIndex;
				}
				svfitEventKey.ActivateBranches(svfitCacheInputTree, false);
				LOG(DEBUG) << "\t\t" << svfitCacheInputTreeIndices.size() << " entries found.";
		
				svfitResults.SetBranchAddresses(svfitCacheInputTree);
			
				SvfitTools::svfitCacheInputTrees[cacheFileTreeName] = svfitCacheInputTree;
				SvfitTools::svfitCacheInputTreeIndices[cacheFileTreeName] = svfitCacheInputTreeIndices;
			}
			else
			{
				LOG(WARNING) << "Could not read SVfit cache tree from \"" << cacheFileTreeName << "\"!";
			}
			
			SvfitTools::svfitCacheInputFiles[cacheFileName] = svfitCacheInputFile;
		}
		else
		{
			LOG(WARNING) << "Could not open SVfit cache file \"" << cacheFileName << "\"!";
		}

		gDirectory = savedir;
		gFile = savefile;
	}
	else
	{
		LOG(DEBUG) << "\tSVfit cache trees from file " << cacheFileName << " already loaded.";
	}
}

SvfitResults SvfitTools::GetResults(SvfitEventKey const& svfitEventKey,
                                    SvfitInputs const& svfitInputs,
                                    bool& neededRecalculation,
                                    HttEnumTypes::SvfitCacheMissBehaviour svfitCacheMissBehaviour,
									float const& svfitKappa)
{
	svfitAlgorithm.addLogM_fixed(true, svfitKappa);
	svfitAlgorithm.setDiTauMassConstraint(svfitEventKey.diTauMassConstraint);
	
	neededRecalculation = true;
	if (Utility::Contains(SvfitTools::svfitCacheInputTrees, cacheFileTreeName) && Utility::Contains(SvfitTools::svfitCacheInputTreeIndices, cacheFileTreeName))
	{
		if (Utility::Contains(SafeMap::Get(SvfitTools::svfitCacheInputTreeIndices, cacheFileTreeName), svfitEventKey))
		{
			SafeMap::Get(SvfitTools::svfitCacheInputTrees, cacheFileTreeName)->GetEntry(SafeMap::Get(SafeMap::Get(SvfitTools::svfitCacheInputTreeIndices, cacheFileTreeName), svfitEventKey));
			svfitResults.FromCache();
			neededRecalculation = false;
		}
	}
	if (neededRecalculation)
	{
		if(svfitCacheMissBehaviour == HttEnumTypes::SvfitCacheMissBehaviour::recalculate)
		{
			LOG_N_TIMES(30, INFO) << "SvfitCache miss: No corresponding entry to the current inputs found in SvfitCache file. Re-Running SvFit. Did your inputs change?"
			                      << std::endl << "Cache searched in tree: \"" << cacheFileTreeName << "\".";
		}
		if(svfitCacheMissBehaviour == HttEnumTypes::SvfitCacheMissBehaviour::assert)
		{
			LOG(FATAL) << "SvfitCache miss: No corresponding entry to the current inputs found in SvfitCache file. Did your inputs change?";
		}
		if(svfitCacheMissBehaviour == HttEnumTypes::SvfitCacheMissBehaviour::undefined)
		{
			svfitResults.FromRecalculation();
			return svfitResults;
		}
	
		// execute integration
		svfitInputs.Integrate(svfitEventKey, svfitAlgorithm);
	
		// retrieve results
		svfitResults.Set(svfitAlgorithm);
		svfitResults.FromRecalculation();
	}
	
	return svfitResults;
}

SvfitTools::~SvfitTools()
{
	if (m_visPtResolutionFile)
	{
		m_visPtResolutionFile->Close();
	}
	
	if (Utility::Contains(SvfitTools::svfitCacheInputFiles, cacheFileName) && SafeMap::Get(SvfitTools::svfitCacheInputFiles, cacheFileName)->IsOpen())
	{
		SafeMap::Get(SvfitTools::svfitCacheInputFiles, cacheFileName)->Close();
		delete SafeMap::Get(SvfitTools::svfitCacheInputFiles, cacheFileName);
		SvfitTools::svfitCacheInputFiles.erase(cacheFileName);
	}
	
	// do NOT call destructor for TTree and TFile here. They are static and the destructor is called several times when running the factory
	// We have to trust the OS does handle freeing the memory properly
}
