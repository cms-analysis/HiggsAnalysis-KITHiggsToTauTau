#include <boost/program_options.hpp>
#include <boost/program_options/options_description.hpp>
#include <boost/program_options/variables_map.hpp>
#include <boost/filesystem.hpp>
#include <stdexcept>

#include "TauAnalysis/SVfitStandalone/interface/SVfitStandaloneAlgorithm.h"
#include "Kappa/DataFormats/interface/Kappa.h"

#include <TSystem.h>

#include "Math/GenVector/LorentzVector.h"
#include "Math/GenVector/DisplacementVector3D.h"
#include "Math/SMatrix.h"

typedef ROOT::Math::DisplacementVector3D<ROOT::Math::Cartesian3D<float>,ROOT::Math::DefaultCoordinateSystemTag> RMDataV;
typedef ROOT::Math::SMatrix<double, 2, 2, ROOT::Math::MatRepSym<double, 2> > RMSM2x2;

// copied from StackOverflow. Must be perfect.
void removeCharsFromString( std::string &str, char* charsToRemove ) {
   for ( unsigned int i = 0; i < strlen(charsToRemove); ++i ) {
      str.erase( std::remove(str.begin(), str.end(), charsToRemove[i]), str.end() );
   }
}

int main(int argc, const char *argv[])
{

    boost::program_options::options_description args{"Svfit input calculator Options"};
    args.add_options()
        ("help,h", "tba")
        ("inputfile,i",  boost::program_options::value<std::string>(), "Path to the input rootfile")
        ("outputfile,o", boost::program_options::value<std::string>(), "Output filename")
        ("libkappa,l",   boost::program_options::value<std::string>()->default_value("Kappa/lib/libKappa.so"), "path to libKappa.so");

    // parse the options
    boost::program_options::variables_map vm;
    boost::program_options::store(boost::program_options::command_line_parser(argc, argv).options(args).run(), vm);
    boost::program_options::notify(vm);

    if(boost::filesystem::exists(vm["libkappa"].as<std::string>()))
    {
        gSystem->Load(vm["libkappa"].as<std::string>().c_str());
    }
    else if (boost::filesystem::exists("Kappa/lib/libKappa.so"))
    {
        gSystem->Load("Kappa/lib/libKappa.so");
    }
    else if (boost::filesystem::exists("libKappa.so"))
    {
        gSystem->Load("libKappa.so");
    }
    else
    {
        throw std::runtime_error("libKappa.so could not be found");
    }
    // Svfit Eventkey
    ULong64_t runLumiEvent;
    svFitStandalone::kDecayType decayType1, decayType2;
    int systematicShift;
    float systematicShiftSigma;
    int integrationMethod;
    ULong64_t hash;

    // Svfit Inputs
    RMFLV* leptonMomentum1 = new RMFLV();
    RMFLV* leptonMomentum2 = new RMFLV();
    RMDataV* metMomentum = new RMDataV();
    RMSM2x2* metCovariance = new RMSM2x2();
    int decayMode1, decayMode2;

    // keys for the output file
    ULong64_t outrunLumiEvent;
    ULong64_t outhash;
    int outdecayType1, outdecayType2;
    int outsystematicShift;
    float outsystematicShiftSigma;
    int outintegrationMethod;
    
    RMFLV momentum;//, momentumUncertainty;
    double transverseMass;//, transverseMassUncertainty;

    std::string inputfilename = vm["inputfile"].as<std::string>();
    char chars[] = "\"";
    removeCharsFromString(inputfilename, chars);
    TFile *infile = TFile::Open(inputfilename.c_str(),"READ");
    const char* directory = infile->GetListOfKeys()->At(0)->GetName();
    TTree *inputtree = (TTree*)infile->Get((std::string(directory)+std::string("/svfitCache")).c_str());

    TFile *outfile = new TFile((vm["outputfile"].as<std::string>()).c_str(),"RECREATE");
    TTree *outputtree = new TTree("svfitCache","svfitCache");

    // Svfit Eventkey
    inputtree->SetBranchAddress("runLumiEvent", &runLumiEvent);
    inputtree->SetBranchAddress("systematicShift", &systematicShift);
    inputtree->SetBranchAddress("systematicShiftSigma", &systematicShiftSigma);
    inputtree->SetBranchAddress("integrationMethod", &integrationMethod);
    inputtree->SetBranchAddress("decayType1", &decayType1);
    inputtree->SetBranchAddress("decayType2", &decayType2);
    inputtree->SetBranchAddress("hash", &hash);

    // Svfit Inputs
    inputtree->SetBranchAddress("leptonMomentum1", &leptonMomentum1);
    inputtree->SetBranchAddress("leptonMomentum2", &leptonMomentum2);
    inputtree->SetBranchAddress("metMomentum", &metMomentum);
    inputtree->SetBranchAddress("metCovariance", &metCovariance);
    inputtree->SetBranchAddress("decayMode1", &decayMode1);
    inputtree->SetBranchAddress("decayMode2", &decayMode2);

    // Svfit Eventkey
    inputtree->SetBranchStatus("runLumiEvent", true);
    inputtree->SetBranchStatus("systematicShift", true);
    inputtree->SetBranchStatus("systematicShiftSigma", true);
    inputtree->SetBranchStatus("integrationMethod", true);
    inputtree->SetBranchStatus("decayType1", true);
    inputtree->SetBranchStatus("decayType2", true);
    inputtree->SetBranchStatus("hash", true);

    // Svfit Inputs
    inputtree->SetBranchStatus("leptonMomentum1", true);
    inputtree->SetBranchStatus("leptonMomentum2", true);
    inputtree->SetBranchStatus("metMomentum", true);
    inputtree->SetBranchStatus("metCovariance", true);
    inputtree->SetBranchStatus("decayMode1", true);
    inputtree->SetBranchStatus("decayMode2", true);

    // Svfit Eventkey
    outputtree->Branch("runLumiEvent", &outrunLumiEvent, "runLumiEvent/l");
    outputtree->Branch("systematicShift", &outsystematicShift);
    outputtree->Branch("systematicShiftSigma", &outsystematicShiftSigma);
    outputtree->Branch("integrationMethod", &outintegrationMethod);
    outputtree->Branch("decayType1", &outdecayType1);
    outputtree->Branch("decayType2", &outdecayType2);
    outputtree->Branch("hash", &outhash, "hash/l");


    outputtree->Branch("svfitMomentum", &momentum);
    outputtree->Branch("svfitTransverseMass", &transverseMass, "svfitTransverseMass/D");

    TDirectory *savedir(gDirectory);
    TFile *savefile(gFile);
    TString cmsswBase = TString( getenv ("CMSSW_BASE") );
    TFile* inputFile_visPtResolution = new TFile(cmsswBase+"/src/TauAnalysis/SVfitStandalone/data/svFitVisMassAndPtResolutionPDF.root");
    gDirectory = savedir;
    gFile = savefile;

    unsigned int nEntries = inputtree->GetEntries();
    for(unsigned int entry = 0; entry < nEntries; entry++)
    {
        std::cout << "Entry: " << entry << " / " << nEntries << std::endl;
        inputtree->GetEntry(entry);

        outrunLumiEvent = runLumiEvent;
        outsystematicShift = systematicShift;
        outsystematicShiftSigma = systematicShiftSigma;
        outintegrationMethod = integrationMethod;
        outdecayType1 = decayType1;
        outdecayType2 = decayType2;
        outhash = hash;
        double leptonMass1 = 0;
        double leptonMass2 = 0;

        // execute integration
        //setup inputs for calculation
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

        std::vector<svFitStandalone::MeasuredTauLepton> measuredTauLeptons {
            svFitStandalone::MeasuredTauLepton(static_cast<svFitStandalone::kDecayType>(decayType1), leptonMomentum1->pt(), leptonMomentum1->eta(), leptonMomentum1->phi(), leptonMass1, decayMode1),
            svFitStandalone::MeasuredTauLepton(static_cast<svFitStandalone::kDecayType>(decayType2), leptonMomentum2->pt(), leptonMomentum2->eta(), leptonMomentum2->phi(), leptonMass2, decayMode2)
        };
        TMatrixD metCovarianceMatrix(2, 2);
        metCovarianceMatrix[0][0] = metCovariance->At(0, 0);
        metCovarianceMatrix[1][0] = metCovariance->At(1, 0);
        metCovarianceMatrix[0][1] = metCovariance->At(0, 1);
        metCovarianceMatrix[1][1] = metCovariance->At(1, 1);
        SVfitStandaloneAlgorithm svfitStandaloneAlgorithm = SVfitStandaloneAlgorithm(measuredTauLeptons, metMomentum->x(), metMomentum->y(), metCovarianceMatrix, false);
        svfitStandaloneAlgorithm.addLogM(false);
        svfitStandaloneAlgorithm.shiftVisPt(true, inputFile_visPtResolution);

        if (integrationMethod == 0)
        {
            svfitStandaloneAlgorithm.integrateMarkovChain();
        }
        else if (integrationMethod == 1)
        {
            svfitStandaloneAlgorithm.integrateVEGAS();
        }
        else if (integrationMethod == 2)
        {
            svfitStandaloneAlgorithm.fit();
        }

        // retrieve results
        momentum.SetPt(svfitStandaloneAlgorithm.pt());
        momentum.SetEta(svfitStandaloneAlgorithm.eta());
        momentum.SetPhi(svfitStandaloneAlgorithm.phi());
        momentum.SetM(svfitStandaloneAlgorithm.mass());

        transverseMass = svfitStandaloneAlgorithm.transverseMass();

        outputtree->Fill();
    }
    infile->Close();
    outputtree->Write();
    outfile->Close();
    return 0;
}
