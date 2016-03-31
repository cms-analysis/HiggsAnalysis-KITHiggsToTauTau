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
        ("libkappa,l",   boost::program_options::value<std::string>(), "path to libKappa.so");

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
    ULong64_t run, lumi, event;
    svFitStandalone::kDecayType decayType1, decayType2;
    int systematicShift;
    float systematicShiftSigma;
    int integrationMethod;

    RMFLV* leptonMomentum1 = new RMFLV();
    RMFLV* leptonMomentum2 = new RMFLV();
    RMDataV* metMomentum = new RMDataV();
    RMSM2x2* metCovariance = new RMSM2x2();
    uint32_t hash;

    uint64_t outrun, outlumi, outevent;
    uint32_t outhash;
    int outdecayType1, outdecayType2;
    int outsystematicShift;
    float outsystematicShiftSigma;
    int outintegrationMethod;

    RMFLV momentum, momentumUncertainty;
    RMDataV fittedMET;
    double transverseMass, transverseMassUncertainty;
    std::string inputfilename = vm["inputfile"].as<std::string>();
    char chars[] = "\"";
    removeCharsFromString(inputfilename, chars);
    TFile *infile = TFile::Open(inputfilename.c_str(),"READ");
    const char* directory = infile->GetListOfKeys()->At(0)->GetName();
    TTree *inputtree = (TTree*)infile->Get((std::string(directory)+std::string("/svfitCache")).c_str());

    TFile *outfile = new TFile((vm["outputfile"].as<std::string>()).c_str(),"RECREATE");
    TTree *outputtree = new TTree("svfitCache","svfitCache");

    inputtree->SetBranchAddress("run", &run);
    inputtree->SetBranchAddress("lumi", &lumi);
    inputtree->SetBranchAddress("event", &event);
    inputtree->SetBranchAddress("systematicShift", &systematicShift);
    inputtree->SetBranchAddress("systematicShiftSigma", &systematicShiftSigma);
    inputtree->SetBranchAddress("integrationMethod", &integrationMethod);
    inputtree->SetBranchAddress("decayType1", &decayType1);
    inputtree->SetBranchAddress("decayType2", &decayType2);

    inputtree->SetBranchAddress("leptonMomentum1", &leptonMomentum1);
    inputtree->SetBranchAddress("leptonMomentum2", &leptonMomentum2);
    inputtree->SetBranchAddress("metMomentum", &metMomentum);
    inputtree->SetBranchAddress("metCovariance", &metCovariance);
    inputtree->SetBranchAddress("hash", &hash);

    inputtree->SetBranchStatus("run", true);
    inputtree->SetBranchStatus("lumi", true);
    inputtree->SetBranchStatus("event", true);
    inputtree->SetBranchStatus("systematicShift", true);
    inputtree->SetBranchStatus("systematicShiftSigma", true);
    inputtree->SetBranchStatus("integrationMethod", true);
    inputtree->SetBranchStatus("decayType1", true);
    inputtree->SetBranchStatus("decayType2", true);

    inputtree->SetBranchStatus("leptonMomentum1", true);
    inputtree->SetBranchStatus("leptonMomentum2", true);
    inputtree->SetBranchStatus("metMomentum", true);
    inputtree->SetBranchStatus("metCovariance", true);
    inputtree->SetBranchStatus("hash", true);

    outputtree->Branch("run", &outrun, "run/l");
    outputtree->Branch("lumi", &outlumi, "lumi/l");
    outputtree->Branch("event", &outevent, "event/l");
    outputtree->Branch("systematicShift", &outsystematicShift);
    outputtree->Branch("systematicShiftSigma", &outsystematicShiftSigma);
    outputtree->Branch("integrationMethod", &outintegrationMethod);
    outputtree->Branch("decayType1", &outdecayType1);
    outputtree->Branch("decayType2", &outdecayType2);

    //outputtree->Branch("leptonMomentum1", &leptonMomentum1);
    //outputtree->Branch("leptonMomentum2", &leptonMomentum2);
    //outputtree->Branch("metMomentum", &metMomentum);
    //outputtree->Branch("metCovariance", &metCovariance);
    outputtree->Branch("hash", &outhash);

    outputtree->Branch("svfitMomentum", &momentum);
    outputtree->Branch("svfitMomentumUncertainty", &momentumUncertainty);
    outputtree->Branch("svfitMet", &fittedMET);
    outputtree->Branch("svfitTransverseMass", &transverseMass, "svfitTransverseMass/D");
    outputtree->Branch("svfitTransverseMassUnc", &transverseMassUncertainty, "svfitTransverseMassUnc/D");
    unsigned int nEntries = inputtree->GetEntries();
    for(unsigned int entry = 0; entry < nEntries; entry++)
    {
        std::cout << "Entry: " << entry << " / " << nEntries << std::endl;
        inputtree->GetEntry(entry);

        outrun = run;
        outlumi = lumi;
        outevent = event;
        outsystematicShift = systematicShift;
        outsystematicShiftSigma = systematicShiftSigma;
        outintegrationMethod = integrationMethod;
        outdecayType1 = decayType1;
        outdecayType2 = decayType2;
        outhash = hash;

        // execute integration
        std::vector<svFitStandalone::MeasuredTauLepton> measuredTauLeptons {
            svFitStandalone::MeasuredTauLepton(static_cast<svFitStandalone::kDecayType>(decayType1), leptonMomentum1->pt(), leptonMomentum1->eta(), leptonMomentum1->phi(), leptonMomentum1->M()),
            svFitStandalone::MeasuredTauLepton(static_cast<svFitStandalone::kDecayType>(decayType2), leptonMomentum2->pt(), leptonMomentum2->eta(), leptonMomentum2->phi(), leptonMomentum2->M())
        };
        TMatrixD metCovarianceMatrix(2, 2);
        metCovarianceMatrix[0][0] = metCovariance->At(0, 0);
        metCovarianceMatrix[1][0] = metCovariance->At(1, 0);
        metCovarianceMatrix[0][1] = metCovariance->At(0, 1);
        metCovarianceMatrix[1][1] = metCovariance->At(1, 1);
        SVfitStandaloneAlgorithm svfitStandaloneAlgorithm = SVfitStandaloneAlgorithm(measuredTauLeptons, metMomentum->x(), metMomentum->y(), metCovarianceMatrix, false);
        svfitStandaloneAlgorithm.addLogM(false);

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
        fittedMET = svfitStandaloneAlgorithm.fittedMET();
        momentumUncertainty.SetPt(svfitStandaloneAlgorithm.ptUncert());
        momentumUncertainty.SetEta(svfitStandaloneAlgorithm.etaUncert());
        momentumUncertainty.SetPhi(svfitStandaloneAlgorithm.phiUncert());
        momentumUncertainty.SetM(svfitStandaloneAlgorithm.massUncert());

        momentum.SetPt(svfitStandaloneAlgorithm.pt());
        momentum.SetEta(svfitStandaloneAlgorithm.eta());
        momentum.SetPhi(svfitStandaloneAlgorithm.phi());
        momentum.SetM(svfitStandaloneAlgorithm.mass());

        transverseMass = svfitStandaloneAlgorithm.transverseMass();
        transverseMassUncertainty = svfitStandaloneAlgorithm.transverseMassUncert();

        outputtree->Fill();
    }
    infile->Close();
    outputtree->Write();
    outfile->Close();
}
