
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Utility/SvfitTools.h"

#include "Artus/Utility/interface/Utility.h"
#include "Artus/Utility/interface/CutRange.h"


SvfitEventKey::SvfitEventKey(uint64_t const& run, uint64_t const& lumi, uint64_t const& event,
                             svFitStandalone::kDecayType const& decayType1, svFitStandalone::kDecayType const& decayType2,
                             HttEnumTypes::SystematicShift const& systematicShift, float const& systematicShiftSigma,
                             IntegrationMethod const& integrationMethod)
{
	Set(run, lumi, event, decayType1, decayType2, systematicShift, systematicShiftSigma, integrationMethod);
}

void SvfitEventKey::Set(uint64_t const& run, uint64_t const& lumi, uint64_t const& event,
                        svFitStandalone::kDecayType const& decayType1, svFitStandalone::kDecayType const& decayType2,
                        HttEnumTypes::SystematicShift const& systematicShift, float const& systematicShiftSigma,
                        IntegrationMethod const& integrationMethod)
{
	this->run = run;
	this->lumi = lumi;
	this->event = event;
	this->decayType1 = Utility::ToUnderlyingValue(decayType1);
	this->decayType2 = Utility::ToUnderlyingValue(decayType2);
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
	tree->Branch("run", &run, "run/l");
	tree->Branch("lumi", &lumi, "lumi/l");
	tree->Branch("event", &event, "event/l");
	tree->Branch("decayType1", &decayType1);
	tree->Branch("decayType2", &decayType2);
	tree->Branch("systematicShift", &systematicShift);
	tree->Branch("systematicShiftSigma", &systematicShiftSigma);
	tree->Branch("integrationMethod", &integrationMethod);
}

void SvfitEventKey::SetBranchAddresses(TTree* tree)
{
	tree->SetBranchAddress("run", &run);
	tree->SetBranchAddress("lumi", &lumi);
	tree->SetBranchAddress("event", &event);
	tree->SetBranchAddress("decayType1", &decayType1);
	tree->SetBranchAddress("decayType2", &decayType2);
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
	tree->SetBranchStatus("decayType1", activate);
	tree->SetBranchStatus("decayType2", activate);
	tree->SetBranchStatus("systematicShift", activate);
	tree->SetBranchStatus("systematicShiftSigma", activate);
	tree->SetBranchStatus("integrationMethod", activate);
}

bool SvfitEventKey::operator<(SvfitEventKey const& rhs) const
{
	if (run == rhs.run)
	{
		if (lumi == rhs.lumi)
		{
			if (event == rhs.event)
			{
				if (decayType1 == rhs.decayType1)
				{
					if (decayType2 == rhs.decayType2)
					{
						if (integrationMethod == rhs.integrationMethod)
						{
							if (systematicShift == rhs.systematicShift)
							{
								return (systematicShiftSigma < rhs.systematicShiftSigma);
							}
							else
							{
								return (systematicShift < rhs.systematicShift);
							}
						}
						else
						{
							return (integrationMethod < rhs.integrationMethod);
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
			else
			{
				return (event < rhs.event);
			}
		}
		else
		{
			return (lumi < rhs.lumi);
		}
	}
	else {
		return (run < rhs.run);
	}
}

bool SvfitEventKey::operator==(SvfitEventKey const& rhs) const
{
	return ((run == rhs.run) && (lumi == rhs.lumi) && (event == rhs.event) &&
	        (decayType1 == rhs.decayType1) &&
	        (decayType2 == rhs.decayType2) &&
	        (integrationMethod == rhs.integrationMethod) &&
	        (systematicShift == rhs.systematicShift) &&
	        CutRange::EqualsCut(systematicShiftSigma).IsInRange(rhs.systematicShiftSigma));
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
			"decayType1=" + std::to_string(svfitEventKey.decayType1) + ", " +
			"decayType2=" + std::to_string(svfitEventKey.decayType2) + ", " +
			"systematicShift=" + std::to_string(svfitEventKey.systematicShift) + ", " +
			"systematicShiftSigma=" + std::to_string(svfitEventKey.systematicShiftSigma) + ", " +
			"integrationMethod=" + std::to_string(svfitEventKey.integrationMethod) + ")";
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

SVfitStandaloneAlgorithm SvfitInputs::GetSvfitStandaloneAlgorithm(SvfitEventKey const& svfitEventKey, int verbosity, bool addLogM) const
{
	SVfitStandaloneAlgorithm svfitStandaloneAlgorithm = SVfitStandaloneAlgorithm(GetMeasuredTauLeptons(svfitEventKey),
	                                                                             metMomentum->x(),
	                                                                             metMomentum->y(),
	                                                                             GetMetCovarianceMatrix(),
	                                                                             verbosity);
	svfitStandaloneAlgorithm.addLogM(addLogM);
	return svfitStandaloneAlgorithm;
}

std::vector<svFitStandalone::MeasuredTauLepton> SvfitInputs::GetMeasuredTauLeptons(SvfitEventKey const& svfitEventKey) const
{
	std::vector<svFitStandalone::MeasuredTauLepton> measuredTauLeptons {
		svFitStandalone::MeasuredTauLepton(Utility::ToEnum<svFitStandalone::kDecayType>(svfitEventKey.decayType1), leptonMomentum1->pt(), leptonMomentum1->eta(), leptonMomentum1->phi(), leptonMomentum1->M()),
		svFitStandalone::MeasuredTauLepton(Utility::ToEnum<svFitStandalone::kDecayType>(svfitEventKey.decayType2), leptonMomentum2->pt(), leptonMomentum2->eta(), leptonMomentum2->phi(), leptonMomentum2->M())
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

SvfitResults::SvfitResults(RMFLV const& momentum, RMFLV const& momentumUncertainty, RMDataV const& fittedMET, std::pair<double, double> transverseMass) :
	SvfitResults()
{
	Set(momentum, momentumUncertainty, fittedMET, transverseMass);
}

SvfitResults::SvfitResults(SVfitStandaloneAlgorithm const& svfitStandaloneAlgorithm) :
	SvfitResults()
{
	Set(svfitStandaloneAlgorithm);
}

SvfitResults::~SvfitResults()
{
	/* TODO: freeing memory here creates segmentation faults
	if (momentum)
	{
		delete momentum;
	}
	if (momentumUncertainty)
	{
		delete momentumUncertainty;
	}
	*/
}

void SvfitResults::Set(RMFLV const& momentum, RMFLV const& momentumUncertainty, RMDataV const& fittedMET, std::pair<double, double> transverseMass)
{
	if (! this->momentum)
	{
		this->momentum = new RMFLV();
	}
	if (! this->momentumUncertainty)
	{
		this->momentumUncertainty = new RMFLV();
	}
	if (! this->fittedMET)
	{
		this->fittedMET = new RMDataV();
	}
	if(! this->transverseMass)
	{
		this->transverseMass = new double;
	}
	if(! this->transverseMassUnc)
	{
		this->transverseMassUnc = new double;
	}
	
	*(this->momentum) = momentum;
	*(this->momentumUncertainty) = momentumUncertainty;
	*(this->fittedMET) = fittedMET;
	*(this->transverseMass) = transverseMass.first;
	*(this->transverseMassUnc) = transverseMass.second;
}

void SvfitResults::Set(SVfitStandaloneAlgorithm const& svfitStandaloneAlgorithm)
{
	Set(GetMomentum(svfitStandaloneAlgorithm),
	    GetMomentumUncertainty(svfitStandaloneAlgorithm),
	    GetFittedMET(svfitStandaloneAlgorithm),
	    GetFittedTransverseMass(svfitStandaloneAlgorithm));
}

void SvfitResults::CreateBranches(TTree* tree)
{
	tree->Branch("svfitMomentum", &momentum);
	tree->Branch("svfitMomentumUncertainty", &momentumUncertainty);
	tree->Branch("svfitMet", &fittedMET);
	tree->Branch("svfitTransverseMass", &transverseMass);
	tree->Branch("svfitTransverseMassUnc", &transverseMassUnc);
}

void SvfitResults::SetBranchAddresses(TTree* tree)
{
	tree->SetBranchAddress("svfitMomentum", &momentum);
	tree->SetBranchAddress("svfitMomentumUncertainty", &momentumUncertainty);
	tree->SetBranchAddress("svfitMet", &fittedMET);
	tree->SetBranchAddress("svfitTransverseMass", &transverseMass);
	tree->SetBranchAddress("svfitTransverseMassUnc", &transverseMassUnc);
	ActivateBranches(tree, true);
}

void SvfitResults::ActivateBranches(TTree* tree, bool activate)
{
	tree->SetBranchStatus("svfitMomentum", activate);
	tree->SetBranchStatus("svfitMomentumUncertainty", activate);
	tree->SetBranchStatus("svfitMet", activate);
	tree->SetBranchStatus("svfitTransverseMass", activate);
	tree->SetBranchStatus("svfitTransverseMassUnc", activate);
}

bool SvfitResults::operator==(SvfitResults const& rhs) const
{
	return (Utility::ApproxEqual(*momentum, *(rhs.momentum)) &&
	        Utility::ApproxEqual(*momentumUncertainty, *(rhs.momentumUncertainty)));
}

bool SvfitResults::operator!=(SvfitResults const& rhs) const
{
	return (! (*this == rhs));
}

RMFLV SvfitResults::GetMomentum(SVfitStandaloneAlgorithm const& svfitStandaloneAlgorithm) const
{
	RMFLV momentum;
	momentum.SetPt(svfitStandaloneAlgorithm.pt());
	momentum.SetEta(svfitStandaloneAlgorithm.eta());
	momentum.SetPhi(svfitStandaloneAlgorithm.phi());
	momentum.SetM(svfitStandaloneAlgorithm.mass());
	return momentum;
}

RMFLV SvfitResults::GetMomentumUncertainty(SVfitStandaloneAlgorithm const& svfitStandaloneAlgorithm) const
{
	RMFLV momentumUncertainty;
	momentumUncertainty.SetPt(svfitStandaloneAlgorithm.ptUncert());
	momentumUncertainty.SetEta(svfitStandaloneAlgorithm.etaUncert());
	momentumUncertainty.SetPhi(svfitStandaloneAlgorithm.phiUncert());
	momentumUncertainty.SetM(svfitStandaloneAlgorithm.massUncert());
	return momentumUncertainty;
}

RMDataV SvfitResults::GetFittedMET(SVfitStandaloneAlgorithm const& svfitStandaloneAlgorithm) const
{
	RMDataV fittedMET(svfitStandaloneAlgorithm.fittedMET());
	return fittedMET;
}

std::pair<double, double> SvfitResults::GetFittedTransverseMass(SVfitStandaloneAlgorithm const& svfitStandaloneAlgorithm) const
{
	return std::make_pair(svfitStandaloneAlgorithm.transverseMass(), svfitStandaloneAlgorithm.transverseMassUncert());
}

SvfitTools::SvfitTools(std::vector<std::string> const& fileNames, std::string const& treeName)
{
	Init(fileNames, treeName);
}

void SvfitTools::Init(std::vector<std::string> const& fileNames, std::string const& treeName)
{
	if (/*(! svfitCacheFile) && */(! svfitCacheInputTree) && svfitCacheInputTreeIndices.empty())
	{
		LOG(DEBUG) << "\tLoading SVfit cache trees from files...";
		//svfitCacheFile = new TMemFile("test", "RECREATE");
		svfitCacheInputTree = new TChain(treeName.c_str());
		for (std::vector<std::string>::const_iterator fileName = fileNames.begin();
		     fileName != fileNames.end(); ++fileName)
		{
			LOG(DEBUG) << "\t\t" << *fileName << "/" << treeName;
			svfitCacheInputTree->Add(fileName->c_str());
		}
		//svfitCacheInputTree->SetDirectory(svfitCacheFile);
		//svfitCacheFile->Write();
		//svfitCacheFile->Close();
		
		SvfitEventKey svfitEventKey;
		svfitEventKey.SetBranchAddresses(svfitCacheInputTree);
		for (uint64_t svfitCacheInputTreeIndex = 0;
		     svfitCacheInputTreeIndex < uint64_t(svfitCacheInputTree->GetEntries());
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
                                    bool& neededRecalculation,
                                    bool checkInputs)
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
		if (checkInputs)
		{
			neededRecalculation = (this->svfitInputs != svfitInputs);
		}
	}
	
	if (neededRecalculation)
	{
		// construct algorithm
		SVfitStandaloneAlgorithm svfitStandaloneAlgorithm = svfitInputs.GetSvfitStandaloneAlgorithm(svfitEventKey);
	
		// execute integration
		if (svfitEventKey.GetIntegrationMethod() == SvfitEventKey::IntegrationMethod::VEGAS)
		{
			svfitStandaloneAlgorithm.integrateVEGAS();
		}
		else if (svfitEventKey.GetIntegrationMethod() == SvfitEventKey::IntegrationMethod::MARKOV_CHAIN)
		{
			svfitStandaloneAlgorithm.integrateMarkovChain();
		}
		else if (svfitEventKey.GetIntegrationMethod() == SvfitEventKey::IntegrationMethod::FIT)
		{
			svfitStandaloneAlgorithm.fit();
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
