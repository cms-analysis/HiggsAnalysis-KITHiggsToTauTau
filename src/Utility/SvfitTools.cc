
#include "HiggsAnalysis/KITHiggsToTauTau/interface/Utility/SvfitTools.h"

#include "Artus/Utility/interface/Utility.h"
#include "Artus/Utility/interface/CutRange.h"

#include "Kappa/DataFormats/interface/Hash.h"


SvfitEventKey::SvfitEventKey(ULong64_t const& runLumiEvent,
                             svFitStandalone::kDecayType const& decayType1, svFitStandalone::kDecayType const& decayType2,
                             HttEnumTypes::SystematicShift const& systematicShift,
                             float const& systematicShiftSigma, IntegrationMethod const& integrationMethod, ULong64_t const& hash)
{
	Set(runLumiEvent, decayType1, decayType2, systematicShift, systematicShiftSigma, integrationMethod, hash);
}

void SvfitEventKey::Set(ULong64_t const& runLumiEvent,
                        svFitStandalone::kDecayType const& decayType1, svFitStandalone::kDecayType const& decayType2,
                        HttEnumTypes::SystematicShift const& systematicShift,
                        float const& systematicShiftSigma, IntegrationMethod const& integrationMethod, ULong64_t const& hash)
{
	this->runLumiEvent = runLumiEvent;
	this->decayType1 = Utility::ToUnderlyingValue(decayType1);
	this->decayType2 = Utility::ToUnderlyingValue(decayType2);
	this->systematicShift = Utility::ToUnderlyingValue<HttEnumTypes::SystematicShift>(systematicShift);
	this->systematicShiftSigma = systematicShiftSigma;
	this->integrationMethod = Utility::ToUnderlyingValue<IntegrationMethod>(integrationMethod);
	this->hash = hash;
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
	tree->Branch("runLumiEvent", &runLumiEvent, "runLumiEvent/l");
	tree->Branch("decayType1", &decayType1);
	tree->Branch("decayType2", &decayType2);
	tree->Branch("systematicShift", &systematicShift);
	tree->Branch("systematicShiftSigma", &systematicShiftSigma);
	tree->Branch("integrationMethod", &integrationMethod);
	tree->Branch("hash", &hash, "hash/l");
}

void SvfitEventKey::SetBranchAddresses(TTree* tree)
{
	tree->SetBranchAddress("runLumiEvent", &runLumiEvent);
	tree->SetBranchAddress("decayType1", &decayType1);
	tree->SetBranchAddress("decayType2", &decayType2);
	tree->SetBranchAddress("systematicShift", &systematicShift);
	tree->SetBranchAddress("systematicShiftSigma", &systematicShiftSigma);
	tree->SetBranchAddress("integrationMethod", &integrationMethod);
	tree->SetBranchAddress("hash", &hash);
	ActivateBranches(tree, true);
}

void SvfitEventKey::ActivateBranches(TTree* tree, bool activate)
{
	tree->SetBranchStatus("runLumiEvent", activate);
	tree->SetBranchStatus("decayType1", activate);
	tree->SetBranchStatus("decayType2", activate);
	tree->SetBranchStatus("systematicShift", activate);
	tree->SetBranchStatus("systematicShiftSigma", activate);
	tree->SetBranchStatus("integrationMethod", activate);
	tree->SetBranchStatus("hash", activate);
}

bool SvfitEventKey::operator<(SvfitEventKey const& rhs) const
{
	if (runLumiEvent == rhs.runLumiEvent)
	{
		if (decayType1 == rhs.decayType1)
		{
			if (decayType2 == rhs.decayType2)
			{
				if (integrationMethod == rhs.integrationMethod)
				{
					if (systematicShift == rhs.systematicShift)
					{
						if (hash == rhs.hash)
						{
							return (systematicShiftSigma < rhs.systematicShiftSigma);
						}
						else
						{
							return (hash < rhs.hash);
						}
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
	else {
		return (runLumiEvent < rhs.runLumiEvent);
	}
}

bool SvfitEventKey::operator==(SvfitEventKey const& rhs) const
{
	return ((runLumiEvent == rhs.runLumiEvent) &&
	        (decayType1 == rhs.decayType1) &&
	        (decayType2 == rhs.decayType2) &&
	        (integrationMethod == rhs.integrationMethod) &&
	        (systematicShift == rhs.systematicShift) &&
	        CutRange::EqualsCut(systematicShiftSigma).IsInRange(rhs.systematicShiftSigma) &&
	        (hash == rhs.hash));
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
			"systematicShift=" + std::to_string(svfitEventKey.systematicShift) + ", " +
			"systematicShiftSigma=" + std::to_string(svfitEventKey.systematicShiftSigma) + ", " +
			"integrationMethod=" + std::to_string(svfitEventKey.integrationMethod) + "," +
			"hash=" + std::to_string(svfitEventKey.hash) + ")";
}

std::ostream& operator<<(std::ostream& os, SvfitEventKey const& svfitEventKey)
{
	return os << std::to_string(svfitEventKey);
}

SvfitInputs::SvfitInputs(RMFLV const& leptonMomentum1, RMFLV const& leptonMomentum2,
                         RMDataV const& metMomentum, RMSM2x2 const& metCovariance,
                         int const& decayMode1, int const& decayMode2)
	: SvfitInputs()
{
	Set(leptonMomentum1, leptonMomentum2, metMomentum, metCovariance, decayMode1, decayMode2);
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
                      RMDataV const& metMomentum, RMSM2x2 const& metCovariance,
                      int const& decayMode1, int const& decayMode2)
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
	if (! this->decayMode1)
	{
		this->decayMode1 = new int;
	}
	if (! this->decayMode2)
	{
		this->decayMode2 = new int;
	}
	
	*(this->leptonMomentum1) = leptonMomentum1;
	*(this->leptonMomentum2) = leptonMomentum2;
	*(this->metMomentum) = metMomentum;
	*(this->metCovariance) = metCovariance;
	*(this->decayMode1) = decayMode1;
	*(this->decayMode2) = decayMode2;
}

void SvfitInputs::CreateBranches(TTree* tree)
{
	tree->Branch("leptonMomentum1", "RMFLV", &leptonMomentum1);
	tree->Branch("leptonMomentum2", "RMFLV", &leptonMomentum2);
	tree->Branch("metMomentum", "ROOT::Math::DisplacementVector3D<ROOT::Math::Cartesian3D<float>,ROOT::Math::DefaultCoordinateSystemTag>", &metMomentum);
	tree->Branch("metCovariance", "ROOT::Math::SMatrix<double, 2, 2, ROOT::Math::MatRepSym<double, 2> >", &metCovariance);
	tree->Branch("decayMode1", decayMode1);
	tree->Branch("decayMode2", decayMode2);
}

void SvfitInputs::SetBranchAddresses(TTree* tree)
{
	tree->SetBranchAddress("leptonMomentum1", &leptonMomentum1);
	tree->SetBranchAddress("leptonMomentum2", &leptonMomentum2);
	tree->SetBranchAddress("metMomentum", &metMomentum);
	tree->SetBranchAddress("metCovariance", &metCovariance);
	tree->SetBranchAddress("decayMode1", decayMode1);
	tree->SetBranchAddress("decayMode2", decayMode2);
	ActivateBranches(tree, true);
}

void SvfitInputs::ActivateBranches(TTree* tree, bool activate)
{
	tree->SetBranchStatus("leptonMomentum1", activate);
	tree->SetBranchStatus("leptonMomentum2", activate);
	tree->SetBranchStatus("metMomentum", activate);
	tree->SetBranchStatus("metCovariance", activate);
	tree->SetBranchStatus("decayMode1", activate);
	tree->SetBranchStatus("decayMode2", activate);
}

bool SvfitInputs::operator==(SvfitInputs const& rhs) const
{
	return (Utility::ApproxEqual(*leptonMomentum1, *(rhs.leptonMomentum1)) &&
	        Utility::ApproxEqual(*leptonMomentum2, *(rhs.leptonMomentum2)) &&
	        Utility::ApproxEqual(*metMomentum, *(rhs.metMomentum)) &&
	        Utility::ApproxEqual(*metCovariance, *(rhs.metCovariance)) &&
	        (*decayMode1 == *(rhs.decayMode1)) &&
	        (*decayMode2 == *(rhs.decayMode2)));
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
	std::vector<svFitStandalone::MeasuredTauLepton> measuredTauLeptons {
		svFitStandalone::MeasuredTauLepton(Utility::ToEnum<svFitStandalone::kDecayType>(svfitEventKey.decayType1), leptonMomentum1->pt(), leptonMomentum1->eta(), leptonMomentum1->phi(), leptonMass1, *decayMode1),
		svFitStandalone::MeasuredTauLepton(Utility::ToEnum<svFitStandalone::kDecayType>(svfitEventKey.decayType2), leptonMomentum2->pt(), leptonMomentum2->eta(), leptonMomentum2->phi(), leptonMass2, *decayMode2)
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
	recalculated = false;
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
	//tree->Branch("svfitMomentumUncertainty", &momentumUncertainty);
	//tree->Branch("svfitMet", &fittedMET);
	tree->Branch("svfitTransverseMass", transverseMass, "svfitTransverseMass/D");
	//tree->Branch("svfitTransverseMassUnc", transverseMassUnc, "svfitTransverseMassUnc/D");
}

void SvfitResults::SetBranchAddresses(TTree* tree)
{
	if(! transverseMass)
	{
		transverseMass = new double;
	}
	tree->SetBranchAddress("svfitMomentum", &momentum);
	//tree->SetBranchAddress("svfitMomentumUncertainty", &momentumUncertainty);
	//tree->SetBranchAddress("svfitMet", &fittedMET);
	tree->SetBranchAddress("svfitTransverseMass", transverseMass);
	//tree->SetBranchAddress("svfitTransverseMassUnc", transverseMassUnc);
	ActivateBranches(tree, true);
}

void SvfitResults::ActivateBranches(TTree* tree, bool activate)
{
	tree->SetBranchStatus("svfitMomentum", activate);
	//tree->SetBranchStatus("svfitMomentumUncertainty", activate);
	//tree->SetBranchStatus("svfitMet", activate);
	tree->SetBranchStatus("svfitTransverseMass", activate);
	//tree->SetBranchStatus("svfitTransverseMassUnc", activate);
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

std::map<std::string, TTree*> SvfitTools::svfitCacheInputTree;
std::map<std::string, TFile*> SvfitTools::svfitCacheInputFile;
std::map<std::string, std::map<SvfitEventKey, uint64_t>> SvfitTools::svfitCacheInputTreeIndices;
std::map<std::string, SvfitResults> SvfitTools::svfitResults;

void SvfitTools::Init(std::vector<std::string> const& fileNames, std::string const& treeName)
{
	cacheFileName = fileNames[0];
	if ( SvfitTools::svfitCacheInputTreeIndices.find(cacheFileName) == SvfitTools::svfitCacheInputTreeIndices.end())
	{
		TDirectory *savedir(gDirectory);
		TFile *savefile(gFile);

		SvfitTools::svfitCacheInputFile[cacheFileName] = TFile::Open(cacheFileName.c_str(), "CACHEREAD", cacheFileName.c_str());
		SvfitTools::svfitCacheInputTree[cacheFileName] = dynamic_cast<TTree*>(SvfitTools::svfitCacheInputFile.at(cacheFileName)->Get(treeName.c_str()));

		LOG(INFO) << "\tLoaded SVfit cache trees from file...";
		LOG(INFO) << "\t\t" << cacheFileName << "/" << treeName << " with " << SvfitTools::svfitCacheInputTree.at(cacheFileName)->GetEntries() << " Entries" << std::endl;

		svfitEventKey.SetBranchAddresses(SvfitTools::svfitCacheInputTree[cacheFileName]);
		SvfitTools::svfitCacheInputTreeIndices[cacheFileName] = std::map<SvfitEventKey, uint64_t>();
		for (uint64_t svfitCacheInputTreeIndex = 0;
		     svfitCacheInputTreeIndex < uint64_t(SvfitTools::svfitCacheInputTree.at(cacheFileName)->GetEntries());
		     ++svfitCacheInputTreeIndex)
		{
			SvfitTools::svfitCacheInputTree.at(cacheFileName)->GetEntry(svfitCacheInputTreeIndex);

			SvfitTools::svfitCacheInputTreeIndices.at(cacheFileName)[svfitEventKey] = svfitCacheInputTreeIndex;
			LOG_N_TIMES(10,DEBUG) << std::to_string(svfitEventKey) << " --> " << svfitCacheInputTreeIndex;
			LOG_N_TIMES(10, DEBUG) << svfitEventKey << " --> " << svfitCacheInputTreeIndex;
		}
		svfitEventKey.ActivateBranches(SvfitTools::svfitCacheInputTree.at(cacheFileName), false);
		LOG(DEBUG) << "\t\t" << SvfitTools::svfitCacheInputTreeIndices.at(cacheFileName).size() << " entries found.";
		
		svfitResults[cacheFileName] = SvfitResults();
		svfitResults.at(cacheFileName).SetBranchAddresses(SvfitTools::svfitCacheInputTree.at(cacheFileName));

		gDirectory = savedir;
		gFile = savefile;
	}
	else 
	{
		LOG(DEBUG) << "\tSVfit cache trees from file " << cacheFileName << " already loaded" << std::endl;
	}
}

SvfitResults SvfitTools::GetResults(SvfitEventKey const& svfitEventKey,
                                    SvfitInputs const& svfitInputs,
                                    bool& neededRecalculation,
                                    HttEnumTypes::SvfitCacheMissBehaviour svfitCacheMissBehaviour)
{
	neededRecalculation = true;
	if((cacheFileName != NULL) &&( SvfitTools::svfitCacheInputTreeIndices.find(cacheFileName) != SvfitTools::svfitCacheInputTreeIndices.end() ))
	{
		auto svfitCacheInputTreeIndicesItem = SvfitTools::svfitCacheInputTreeIndices.at(cacheFileName).find(svfitEventKey);
		if (svfitCacheInputTreeIndicesItem != SvfitTools::svfitCacheInputTreeIndices.at(cacheFileName).end())
		{
			SvfitTools::svfitCacheInputTree.at(cacheFileName)->GetEntry(svfitCacheInputTreeIndicesItem->second);
			svfitResults.at(cacheFileName).fromCache();
			neededRecalculation = false;
		}
	}
	if(neededRecalculation)
	{
		if(svfitCacheMissBehaviour == HttEnumTypes::SvfitCacheMissBehaviour::recalculate)
		{
			LOG_N_TIMES(30, INFO) << "SvfitCache miss: No corresponding entry to the current inputs found in SvfitCache file. Re-Running SvFit. Did your inputs change?" 
			<< std::endl << "Cache searched in file: " << cacheFileName << std::endl;
		}
		if(svfitCacheMissBehaviour == HttEnumTypes::SvfitCacheMissBehaviour::assert)
		{
			LOG(FATAL) << "SvfitCache miss: No corresponding entry to the current inputs found in SvfitCache file. Did your inputs change?" << std::endl;
		}
		if(svfitCacheMissBehaviour == HttEnumTypes::SvfitCacheMissBehaviour::undefined)
		{
			svfitResults[cacheFileName] = SvfitResults();
			svfitResults.at(cacheFileName).fromRecalculation();
			return svfitResults.at(cacheFileName);
		}
	}
	
	if (neededRecalculation)
	{
		// construct algorithm
		if(! m_inputFile_visPtResolution)
		{
			TDirectory *savedir(gDirectory);
			TFile *savefile(gFile);
			TString cmsswBase = TString( getenv ("CMSSW_BASE") );
			m_inputFile_visPtResolution = new TFile(cmsswBase+"/src/TauAnalysis/SVfitStandalone/data/svFitVisMassAndPtResolutionPDF.root");
			gDirectory = savedir;
			gFile = savefile;
		}
		SVfitStandaloneAlgorithm svfitStandaloneAlgorithm = svfitInputs.GetSvfitStandaloneAlgorithm(svfitEventKey);
		svfitStandaloneAlgorithm.shiftVisPt(true, m_inputFile_visPtResolution);
	
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
		svfitResults[cacheFileName].Set(svfitStandaloneAlgorithm);
		svfitResults.at(cacheFileName).fromRecalculation();
	}
	
	return svfitResults.at(cacheFileName);
}

SvfitTools::~SvfitTools()
{
	// do NOT call destructor for TTree and TFile here. They are static and the destructor is called several times when running the factory
	// We have to trust the OS does handle freeing the memory properly
}
