#include <boost/program_options.hpp>
#include <boost/program_options/options_description.hpp>
#include <boost/program_options/variables_map.hpp>

#include "HiggsAnalysis/KITHiggsToTauTau/interface/Utility/SvfitTools.h"

#include "Artus/Utility/interface/RootFileHelper.h"

int main(int argc, const char *argv[])
{
	boost::program_options::options_description args{"Svfit input calculator Options"};
	args.add_options()
		("help,h", "tba")
		("inputfile,i", boost::program_options::value<std::string>(), "Path to the input rootfile")
		("outputfile,o", boost::program_options::value<std::string>(), "Output filename")
		("treename,t", boost::program_options::value<std::string>(), "Name of the tree for the svfitCache");

	// parse the options
	boost::program_options::variables_map vm;
	boost::program_options::store(boost::program_options::command_line_parser(argc, argv).options(args).run(), vm);
	boost::program_options::notify(vm);
	
	SvfitEventKey svfitEventKey;
	SvfitInputs svfitInputs;
	SvfitResults svfitResults;
	
	TFile *infile = new TFile((vm["inputfile"].as<std::string>()).c_str(),"READ");
	TTree *inputtree = (TTree*)infile->Get((vm["treename"].as<std::string>()).c_str());
	
	TFile *outfile = new TFile((vm["outputfile"].as<std::string>()).c_str(),"RECREATE");
	TTree *outputtree = new TTree((vm["treename"].as<std::string>()).c_str(),(vm["treename"].as<std::string>()).c_str());

	svfitEventKey.SetBranchAddresses(inputtree);
	svfitInputs.SetBranchAddresses(inputtree);
	svfitResults.SetBranchAddresses(inputtree);
	
	for(unsigned int entry = 0; entry < inputtree->GetEntries(); entry++)
	{
		inputtree->GetEntry(entry);

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
		// retrieve results
		svfitResults.Set(svfitStandaloneAlgorithm);
		
		svfitEventKey.CreateBranches(outputtree); //needs to be improved!!!!
		svfitInputs.CreateBranches(outputtree);
		svfitResults.CreateBranches(outputtree);
		outputtree->Fill();
	}
	RootFileHelper::SafeCd(outfile, "");
	outputtree->Write();
}
