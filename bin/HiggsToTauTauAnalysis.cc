
#include <boost/algorithm/string.hpp>
#include <boost/property_tree/json_parser.hpp>
#include <boost/property_tree/ptree.hpp>

#include <TFile.h>

#include "Artus/Configuration/interface/ArtusConfig.h"
#include "Artus/Configuration/interface/RootEnvironment.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttTypes.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttEventProvider.h"
#include "HiggsAnalysis/KITHiggsToTauTau/interface/HttFactory.h"

/*
	This example implements a simple dummy anaylsis which
	reads entries from a root file and produces various pt plots

	It can be run with the config file data/exampleConfig.json
*/

int main(int argc, char** argv) {

	// parse the command line and load the
	ArtusConfig myConfig(argc, argv);

	// load the global settings from the config file
	HttGlobalSettings globalSettings = myConfig.GetGlobalSettings<HttGlobalSettings>();

	// create the output root environment, automatically saves the config into the root file
	RootEnvironment rootEnv(myConfig);

	// will load the Ntuples from the root file
	// this must be modified if you want to load more/new quantities
	FileInterface2 fileInterface(myConfig.GetInputFiles());
	HttEventProvider evtProvider(fileInterface, (globalSettings.GetInputIsData() ? DataInput : McInput));
	evtProvider.WireEvent(globalSettings);

	// the pipeline initializer will setup the pipeline, with
	// all the attached Producer, Filer and Consumer
	HttPipelineInitializer pInit;
	
	// the factory will manage the producers/filters/consumers
	HttFactory factory;

	// initialize the pipeline runner
	HttPipelineRunner runner;

	// load the pipeline with their configuration from the config file
	myConfig.LoadConfiguration(pInit, runner, factory, rootEnv.GetRootFile());

	// run all the configured pipelines and all their attached
	// consumers
	runner.RunPipelines(evtProvider, globalSettings);

	// close output root file
	rootEnv.Close();

	return 0;
}
